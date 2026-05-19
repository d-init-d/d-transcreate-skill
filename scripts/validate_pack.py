#!/usr/bin/env python3
"""
validate_pack.py — Validation script for the d-transcreate-skill pack.

Checks repository invariants at every commit and at every install destination.
Python 3.8+ standard library only. Exit non-zero on ERROR; warnings do not fail.

Usage:
    python scripts/validate_pack.py [PATH] [--line-budget N] [--duplication-threshold N] [--json]
"""

import argparse
import json
import re
import sys

from pathlib import Path
from collections import defaultdict
from typing import List, Dict, Tuple, Optional, Set


# ---------------------------------------------------------------------------
# Minimal YAML frontmatter parser (stdlib only, no PyYAML dependency)
# ---------------------------------------------------------------------------

def parse_frontmatter(text: str) -> Optional[Dict[str, str]]:
    """
    Parse YAML frontmatter delimited by --- lines at the top of a file.
    Returns a dict of key: value (all values as strings) or None if no frontmatter.
    Only handles simple key: value pairs (no nested structures).
    """
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return None
    end_idx = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_idx = i
            break
    if end_idx is None:
        return None
    fm_lines = lines[1:end_idx]
    result = {}
    for line in fm_lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            key, _, value = line.partition(":")
            result[key.strip()] = value.strip().strip('"').strip("'")
    return result


# ---------------------------------------------------------------------------
# Result types
# ---------------------------------------------------------------------------

class Finding:
    """A single validation finding (error or warning)."""

    def __init__(self, check_id: str, level: str, message: str, path: str = ""):
        self.check_id = check_id
        self.level = level  # "error" or "warning"
        self.message = message
        self.path = path

    def to_dict(self) -> dict:
        d = {"check": self.check_id, "level": self.level, "message": self.message}
        if self.path:
            d["path"] = self.path
        return d

    def __str__(self) -> str:
        prefix = "ERROR" if self.level == "error" else "WARN"
        loc = f" [{self.path}]" if self.path else ""
        return f"[{self.check_id}] {prefix}{loc}: {self.message}"


# ---------------------------------------------------------------------------
# Check implementations
# ---------------------------------------------------------------------------

def check_c1_required_files(root: Path) -> List[Finding]:
    """C1: Required files exist."""
    findings: List[Finding] = []

    required = [
        "core/d-transcreate.md",
    ]

    # core/workflows/*.md — at least one
    workflows_dir = root / "core" / "workflows"
    if workflows_dir.is_dir():
        md_files = list(workflows_dir.glob("*.md"))
        if not md_files:
            findings.append(Finding("C1", "error", "No .md files found in core/workflows/"))
    else:
        findings.append(Finding("C1", "error", "Directory core/workflows/ does not exist"))

    # core/schemas/*.md — at least one
    schemas_dir = root / "core" / "schemas"
    if schemas_dir.is_dir():
        md_files = list(schemas_dir.glob("*.md"))
        if not md_files:
            findings.append(Finding("C1", "error", "No .md files found in core/schemas/"))
    else:
        findings.append(Finding("C1", "error", "Directory core/schemas/ does not exist"))

    # core/prompts/*.md — at least one
    prompts_dir = root / "core" / "prompts"
    if prompts_dir.is_dir():
        md_files = list(prompts_dir.glob("*.md"))
        if not md_files:
            findings.append(Finding("C1", "error", "No .md files found in core/prompts/"))
    else:
        findings.append(Finding("C1", "error", "Directory core/prompts/ does not exist"))

    # Check individual required files
    for rel in required:
        if not (root / rel).is_file():
            findings.append(Finding("C1", "error", f"Required file missing: {rel}", rel))

    return findings


def check_c2_frontmatter(root: Path) -> List[Finding]:
    """C2: Frontmatter YAML is valid for files that have it (SKILL.md, .mdc files)."""
    findings: List[Finding] = []

    # Find all SKILL.md and .mdc files
    targets: List[Path] = []
    for p in root.rglob("SKILL.md"):
        targets.append(p)
    for p in root.rglob("*.mdc"):
        targets.append(p)

    for filepath in targets:
        rel = filepath.relative_to(root).as_posix()
        try:
            text = filepath.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError) as e:
            findings.append(Finding("C2", "error", f"Cannot read file: {e}", rel))
            continue

        fm = parse_frontmatter(text)
        if fm is None:
            findings.append(Finding("C2", "error", "No YAML frontmatter found", rel))
            continue

        # Check that frontmatter has at least one key
        if not fm:
            findings.append(Finding("C2", "error", "Frontmatter is empty (no key-value pairs)", rel))

    return findings


def check_c3_internal_links(root: Path) -> List[Finding]:
    """C3: Internal Markdown links resolve (relative links point to existing files)."""
    findings: List[Finding] = []

    # Pattern for Markdown links: [text](path) — exclude URLs
    link_pattern = re.compile(r'\[([^\]]*)\]\(([^)]+)\)')

    md_files = list(root.rglob("*.md")) + list(root.rglob("*.mdc"))

    for filepath in md_files:
        # Skip .git directory
        if ".git" in filepath.parts:
            continue
        # Skip .kiro directory
        if ".kiro" in filepath.parts:
            continue

        rel = filepath.relative_to(root).as_posix()
        try:
            text = filepath.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue

        # Determine if this file is inside an adapter directory.
        # Adapter files use links relative to the destination project root,
        # not relative to their position in the source repo. We find the
        # adapter's install root (the adapter subdirectory) and resolve
        # links relative to that root as well.
        adapter_root: Optional[Path] = None
        if rel.startswith("adapters/"):
            parts = rel.split("/")
            if len(parts) >= 2:
                adapter_root = root / parts[0] / parts[1]

        for match in link_pattern.finditer(text):
            link_target = match.group(2)

            # Skip external URLs
            if link_target.startswith(("http://", "https://", "mailto:", "#")):
                continue

            # Skip anchors within the same file
            if link_target.startswith("#"):
                continue

            # Remove anchor from link
            link_path = link_target.split("#")[0]
            if not link_path:
                continue

            # Resolve relative to the file's directory
            resolved = (filepath.parent / link_path).resolve()
            if resolved.exists():
                continue

            # For adapter files, also try resolving relative to the adapter root
            # (mirrored destination layout) and relative to the repo root
            if adapter_root is not None:
                resolved_from_adapter = (adapter_root / link_path).resolve()
                if resolved_from_adapter.exists():
                    continue
                # Also try from repo root (adapters reference core/ at repo level)
                resolved_from_root = (root / link_path).resolve()
                if resolved_from_root.exists():
                    continue
                # Try resolving relative path from the adapter root
                # (the file's relative position within the adapter determines
                # how many ../ are needed to reach the adapter root)
                file_rel_to_adapter = filepath.relative_to(adapter_root)
                resolved_within_adapter = (adapter_root / file_rel_to_adapter.parent / link_path).resolve()
                if resolved_within_adapter.exists():
                    continue
                # Final fallback: strip leading ../ segments and resolve from root
                # This handles cases where links are designed for the installed
                # destination layout and use ../ to navigate to core/
                stripped = link_path
                while stripped.startswith("../"):
                    stripped = stripped[3:]
                if stripped != link_path:
                    resolved_stripped = (root / stripped).resolve()
                    if resolved_stripped.exists():
                        continue

            findings.append(Finding(
                "C3", "error",
                f"Broken link: [{match.group(1)}]({link_target}) — target does not exist",
                rel
            ))

    return findings


def check_c4_todo_markers(root: Path) -> List[Finding]:
    """C4: No TODO/TBD/FIXME markers in content."""
    findings: List[Finding] = []

    marker_pattern = re.compile(r'\b(TODO|TBD|FIXME)\b')

    # Check files under core/ and adapters/
    search_dirs = [root / "core", root / "adapters"]

    for search_dir in search_dirs:
        if not search_dir.is_dir():
            continue
        for filepath in search_dir.rglob("*"):
            if not filepath.is_file():
                continue
            if filepath.suffix not in (".md", ".mdc", ".yaml", ".yml", ".json"):
                continue

            rel = filepath.relative_to(root).as_posix()
            try:
                text = filepath.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue

            for i, line in enumerate(text.split("\n"), 1):
                if marker_pattern.search(line):
                    findings.append(Finding(
                        "C4", "error",
                        f"Placeholder marker found on line {i}: {line.strip()[:80]}",
                        rel
                    ))

    return findings


def check_c5_adapter_references_core(root: Path) -> List[Finding]:
    """C5: Each adapter dir has at least one reference to core/."""
    findings: List[Finding] = []

    adapters_dir = root / "adapters"
    if not adapters_dir.is_dir():
        # If no adapters dir, skip (C1 would catch this if required)
        return findings

    core_ref_pattern = re.compile(r'core/')

    for adapter_dir in sorted(adapters_dir.iterdir()):
        if not adapter_dir.is_dir():
            continue

        adapter_name = adapter_dir.name
        found_ref = False

        for filepath in adapter_dir.rglob("*"):
            if not filepath.is_file():
                continue
            try:
                text = filepath.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue

            if core_ref_pattern.search(text):
                found_ref = True
                break

        if not found_ref:
            findings.append(Finding(
                "C5", "error",
                f"Adapter '{adapter_name}' does not reference any file under core/",
                f"adapters/{adapter_name}"
            ))

    return findings


def check_c6_line_budget(root: Path, line_budget: int) -> List[Finding]:
    """C6: Adapter entrypoints ≤ line-budget lines."""
    findings: List[Finding] = []

    # Identify adapter entrypoints: SKILL.md, CLAUDE.md, AGENTS.md, .mdc files,
    # d-transcreate.md in generic adapter, opencode.json
    entrypoint_names = {"SKILL.md", "CLAUDE.md", "AGENTS.md", "d-transcreate.md"}

    adapters_dir = root / "adapters"
    if not adapters_dir.is_dir():
        return findings

    for adapter_dir in sorted(adapters_dir.iterdir()):
        if not adapter_dir.is_dir():
            continue

        # Check top-level entrypoints in the adapter
        for name in entrypoint_names:
            filepath = adapter_dir / name
            if filepath.is_file():
                try:
                    text = filepath.read_text(encoding="utf-8")
                    line_count = len(text.split("\n"))
                    if line_count > line_budget:
                        rel = filepath.relative_to(root).as_posix()
                        findings.append(Finding(
                            "C6", "error",
                            f"Entrypoint exceeds line budget: {line_count} lines (limit: {line_budget})",
                            rel
                        ))
                except (UnicodeDecodeError, OSError):
                    pass

        # Check .mdc files
        for filepath in adapter_dir.rglob("*.mdc"):
            try:
                text = filepath.read_text(encoding="utf-8")
                line_count = len(text.split("\n"))
                if line_count > line_budget:
                    rel = filepath.relative_to(root).as_posix()
                    findings.append(Finding(
                        "C6", "error",
                        f"Entrypoint exceeds line budget: {line_count} lines (limit: {line_budget})",
                        rel
                    ))
            except (UnicodeDecodeError, OSError):
                pass

        # Check nested SKILL.md files (e.g., .claude/skills/d-transcreate/SKILL.md)
        for filepath in adapter_dir.rglob("SKILL.md"):
            if filepath == adapter_dir / "SKILL.md":
                continue  # Already checked above
            try:
                text = filepath.read_text(encoding="utf-8")
                line_count = len(text.split("\n"))
                if line_count > line_budget:
                    rel = filepath.relative_to(root).as_posix()
                    findings.append(Finding(
                        "C6", "error",
                        f"Entrypoint exceeds line budget: {line_count} lines (limit: {line_budget})",
                        rel
                    ))
            except (UnicodeDecodeError, OSError):
                pass

    return findings


def check_c7_duplication(root: Path, threshold: int) -> List[Finding]:
    """C7: Duplication warning — warn if same block of N+ lines appears in multiple files."""
    findings: List[Finding] = []

    # Collect content from core/ and adapters/
    file_lines: Dict[str, List[str]] = {}

    search_dirs = [root / "core", root / "adapters"]
    for search_dir in search_dirs:
        if not search_dir.is_dir():
            continue
        for filepath in search_dir.rglob("*"):
            if not filepath.is_file():
                continue
            if filepath.suffix not in (".md", ".mdc"):
                continue
            try:
                text = filepath.read_text(encoding="utf-8")
                rel = filepath.relative_to(root).as_posix()
                file_lines[rel] = text.split("\n")
            except (UnicodeDecodeError, OSError):
                continue

    if threshold < 2:
        return findings

    # Build blocks of `threshold` consecutive lines from each file
    # and check for duplicates across files
    block_locations: Dict[str, List[str]] = defaultdict(list)

    for rel, lines in file_lines.items():
        if len(lines) < threshold:
            continue
        for i in range(len(lines) - threshold + 1):
            block = "\n".join(lines[i:i + threshold])
            # Skip blocks that are mostly empty
            non_empty = sum(1 for l in lines[i:i + threshold] if l.strip())
            if non_empty < threshold // 2:
                continue
            block_locations[block].append(rel)

    # Report blocks that appear in more than one file
    reported_pairs: Set[Tuple[str, str]] = set()
    for block, locations in block_locations.items():
        unique_files = sorted(set(locations))
        if len(unique_files) > 1:
            pair_key = (unique_files[0], unique_files[1])
            if pair_key not in reported_pairs:
                reported_pairs.add(pair_key)
                findings.append(Finding(
                    "C7", "warning",
                    f"Duplicated block of {threshold}+ lines found in: {', '.join(unique_files[:3])}",
                ))

    return findings


def check_c8_utf8_encoding(root: Path) -> List[Finding]:
    """C8: UTF-8 encoding check + non-ASCII warning for core/ files."""
    findings: List[Finding] = []

    search_dirs = [root / "core", root / "adapters"]

    for search_dir in search_dirs:
        if not search_dir.is_dir():
            continue
        for filepath in search_dir.rglob("*"):
            if not filepath.is_file():
                continue
            rel = filepath.relative_to(root).as_posix()

            # Check valid UTF-8
            try:
                content = filepath.read_bytes()
                text = content.decode("utf-8")
            except UnicodeDecodeError:
                findings.append(Finding(
                    "C8", "error",
                    "File is not valid UTF-8",
                    rel
                ))
                continue
            except OSError:
                continue

            # Non-ASCII warning for core/ files only
            if rel.startswith("core/") and filepath.suffix in (".md", ".mdc"):
                total_chars = len(text)
                if total_chars > 0:
                    non_ascii = sum(1 for c in text if ord(c) > 127)
                    ratio = non_ascii / total_chars
                    if ratio > 0.1:  # More than 10% non-ASCII
                        findings.append(Finding(
                            "C8", "warning",
                            f"High non-ASCII ratio ({ratio:.1%}) — may contain non-English prose",
                            rel
                        ))

    return findings


def check_c9_schema_existence(root: Path) -> List[Finding]:
    """C9: All schemas referenced in core/d-transcreate.md exist."""
    findings: List[Finding] = []

    entrypoint = root / "core" / "d-transcreate.md"
    if not entrypoint.is_file():
        return findings  # C1 would catch this

    # Also check workflow and prompt files for schema references
    files_to_check: List[Path] = [entrypoint]
    for subdir in ["workflows", "prompts"]:
        d = root / "core" / subdir
        if d.is_dir():
            files_to_check.extend(d.rglob("*.md"))

    schema_ref_pattern = re.compile(r'core/schemas/([a-z0-9_-]+\.md)')

    referenced_schemas: Set[str] = set()
    for filepath in files_to_check:
        try:
            text = filepath.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for match in schema_ref_pattern.finditer(text):
            referenced_schemas.add(match.group(1))

    schemas_dir = root / "core" / "schemas"
    for schema_name in sorted(referenced_schemas):
        schema_path = schemas_dir / schema_name
        if not schema_path.is_file():
            findings.append(Finding(
                "C9", "error",
                f"Referenced schema does not exist: core/schemas/{schema_name}",
                f"core/schemas/{schema_name}"
            ))

    return findings


def check_c10_example_readme(root: Path) -> List[Finding]:
    """C10: Each example dir has README.md."""
    findings: List[Finding] = []

    examples_dir = root / "examples"
    if not examples_dir.is_dir():
        return findings

    for entry in sorted(examples_dir.iterdir()):
        if not entry.is_dir():
            continue
        # Skip hidden directories
        if entry.name.startswith("."):
            continue
        readme = entry / "README.md"
        if not readme.is_file():
            rel = entry.relative_to(root).as_posix()
            findings.append(Finding(
                "C10", "error",
                f"Example directory missing README.md",
                rel
            ))

    return findings


def check_c11_install_manifest(root: Path) -> List[Finding]:
    """C11: Install manifest at destination (check for .d-transcreate-manifest.json if validating a built destination)."""
    findings: List[Finding] = []

    manifest_path = root / ".d-transcreate-manifest.json"
    if not manifest_path.is_file():
        # Not a built destination — skip this check silently
        return findings

    # If manifest exists, validate it
    try:
        text = manifest_path.read_text(encoding="utf-8")
        manifest = json.loads(text)
    except (json.JSONDecodeError, OSError) as e:
        findings.append(Finding(
            "C11", "error",
            f"Install manifest is not valid JSON: {e}",
            ".d-transcreate-manifest.json"
        ))
        return findings

    # Check required fields
    required_fields = ["manifest_version", "target_platform", "files"]
    for field in required_fields:
        if field not in manifest:
            findings.append(Finding(
                "C11", "error",
                f"Install manifest missing required field: {field}",
                ".d-transcreate-manifest.json"
            ))

    # Check that all listed files exist
    if "files" in manifest and isinstance(manifest["files"], list):
        for entry in manifest["files"]:
            if isinstance(entry, dict) and "path" in entry:
                file_path = root / entry["path"]
                if not file_path.is_file():
                    findings.append(Finding(
                        "C11", "error",
                        f"Manifest lists file that does not exist: {entry['path']}",
                        entry["path"]
                    ))

    return findings


# ---------------------------------------------------------------------------
# Main orchestration
# ---------------------------------------------------------------------------

def run_all_checks(root: Path, line_budget: int, duplication_threshold: int) -> List[Finding]:
    """Run all validation checks and return findings."""
    findings: List[Finding] = []

    findings.extend(check_c1_required_files(root))
    findings.extend(check_c2_frontmatter(root))
    findings.extend(check_c3_internal_links(root))
    findings.extend(check_c4_todo_markers(root))
    findings.extend(check_c5_adapter_references_core(root))
    findings.extend(check_c6_line_budget(root, line_budget))
    findings.extend(check_c7_duplication(root, duplication_threshold))
    findings.extend(check_c8_utf8_encoding(root))
    findings.extend(check_c9_schema_existence(root))
    findings.extend(check_c10_example_readme(root))
    findings.extend(check_c11_install_manifest(root))

    return findings


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate the d-transcreate-skill pack for structural integrity."
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Path to validate (defaults to current directory / repo root)"
    )
    parser.add_argument(
        "--line-budget",
        type=int,
        default=200,
        help="Maximum lines allowed for adapter entrypoints (default: 200)"
    )
    parser.add_argument(
        "--duplication-threshold",
        type=int,
        default=20,
        help="Minimum consecutive lines to flag as duplication (default: 20)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="json_output",
        help="Output results in JSON format"
    )

    args = parser.parse_args()
    root = Path(args.path).resolve()

    if not root.is_dir():
        print(f"Error: path '{args.path}' is not a directory", file=sys.stderr)
        return 1

    findings = run_all_checks(root, args.line_budget, args.duplication_threshold)

    errors = [f for f in findings if f.level == "error"]
    warnings = [f for f in findings if f.level == "warning"]

    if args.json_output:
        output = {
            "path": str(root),
            "summary": {
                "errors": len(errors),
                "warnings": len(warnings),
                "passed": len(errors) == 0,
            },
            "findings": [f.to_dict() for f in findings],
        }
        print(json.dumps(output, indent=2))
    else:
        if not findings:
            print(f"✓ All checks passed for: {root}")
        else:
            if errors:
                print(f"\n{'='*60}")
                print(f"ERRORS ({len(errors)}):")
                print(f"{'='*60}")
                for f in errors:
                    print(f"  {f}")

            if warnings:
                print(f"\n{'='*60}")
                print(f"WARNINGS ({len(warnings)}):")
                print(f"{'='*60}")
                for f in warnings:
                    print(f"  {f}")

            print(f"\n{'='*60}")
            print(f"Summary: {len(errors)} error(s), {len(warnings)} warning(s)")
            if errors:
                print("FAILED — fix errors above before proceeding.")
            else:
                print("PASSED (with warnings).")
            print(f"{'='*60}")

    # Exit non-zero on errors; warnings do not fail
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
