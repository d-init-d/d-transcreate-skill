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


def load_install_manifest(root: Path) -> Optional[dict]:
    """Return the install manifest dict if present and parseable."""
    manifest_path = root / ".d-transcreate-manifest.json"
    if not manifest_path.is_file():
        return None
    try:
        return json.loads(manifest_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def get_referenced_core_dir(root: Path) -> Optional[Path]:
    """Return shared core/ for reference installs, if declared and present."""
    manifest = load_install_manifest(root)
    if not manifest:
        return None
    if manifest.get("core_strategy") != "reference":
        return None
    shared_core_path = manifest.get("shared_core_path")
    if not isinstance(shared_core_path, str) or not shared_core_path.strip():
        return None
    shared_core = Path(shared_core_path).expanduser().resolve()
    if shared_core.is_dir():
        return shared_core
    return None


def get_core_dir(root: Path) -> Optional[Path]:
    """Return local core/ or the shared core/ for reference installs."""
    local_core = root / "core"
    if local_core.is_dir():
        return local_core
    return get_referenced_core_dir(root)


# ---------------------------------------------------------------------------
# Check implementations
# ---------------------------------------------------------------------------

def check_c1_required_files(root: Path) -> List[Finding]:
    """C1: Required files exist."""
    findings: List[Finding] = []

    required_top_level = [
        "README.md",
        "LICENSE",
        "VERSION",
        "CHANGELOG.md",
    ]

    for rel in required_top_level:
        if not (root / rel).is_file():
            findings.append(Finding("C1", "error", f"Required file missing: {rel}", rel))

    core_dir = get_core_dir(root)
    if core_dir is None:
        manifest = load_install_manifest(root)
        if manifest and manifest.get("core_strategy") == "reference":
            findings.append(Finding(
                "C1", "error",
                "Referenced shared_core_path does not exist or is not a directory",
                ".d-transcreate-manifest.json",
            ))

    # core/workflows/*.md — at least one
    workflows_dir = core_dir / "workflows" if core_dir else root / "core" / "workflows"
    if workflows_dir.is_dir():
        md_files = list(workflows_dir.glob("*.md"))
        if not md_files:
            findings.append(Finding("C1", "error", "No .md files found in core/workflows/"))
    else:
        findings.append(Finding("C1", "error", "Directory core/workflows/ does not exist"))

    # core/schemas/*.md — at least one
    schemas_dir = core_dir / "schemas" if core_dir else root / "core" / "schemas"
    if schemas_dir.is_dir():
        md_files = list(schemas_dir.glob("*.md"))
        if not md_files:
            findings.append(Finding("C1", "error", "No .md files found in core/schemas/"))
    else:
        findings.append(Finding("C1", "error", "Directory core/schemas/ does not exist"))

    # core/prompts/*.md — at least one
    prompts_dir = core_dir / "prompts" if core_dir else root / "core" / "prompts"
    if prompts_dir.is_dir():
        md_files = list(prompts_dir.glob("*.md"))
        if not md_files:
            findings.append(Finding("C1", "error", "No .md files found in core/prompts/"))
    else:
        findings.append(Finding("C1", "error", "Directory core/prompts/ does not exist"))

    entrypoint = core_dir / "d-transcreate.md" if core_dir else root / "core" / "d-transcreate.md"
    if not entrypoint.is_file():
        findings.append(Finding("C1", "error", "Required file missing: core/d-transcreate.md", "core/d-transcreate.md"))

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
            continue

        if filepath.name == "SKILL.md":
            required_keys = ("name", "description")
        elif filepath.suffix == ".mdc":
            required_keys = ("description",)
        else:
            required_keys = ()

        for key in required_keys:
            if not fm.get(key):
                findings.append(Finding(
                    "C2", "error",
                    f"Frontmatter missing required field: {key}",
                    rel,
                ))

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

    core_dir = get_core_dir(root)
    if core_dir is None:
        return findings  # C1 would catch this

    entrypoint = core_dir / "d-transcreate.md"
    if not entrypoint.is_file():
        return findings  # C1 would catch this

    # Also check workflow and prompt files for schema references
    files_to_check: List[Path] = [entrypoint]
    for subdir in ["workflows", "prompts"]:
        d = core_dir / subdir
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

    schemas_dir = core_dir / "schemas"
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
    required_fields = ["manifest_version", "pack_version", "source_commit", "target_platform", "files"]
    for field in required_fields:
        if field not in manifest:
            findings.append(Finding(
                "C11", "error",
                f"Install manifest missing required field: {field}",
                ".d-transcreate-manifest.json"
            ))

    for field in ["pack_version", "source_commit"]:
        value = manifest.get(field)
        if not isinstance(value, str) or not value.strip():
            findings.append(Finding(
                "C11", "error",
                f"Install manifest field must be a non-empty string: {field}",
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


def check_c12_orchestration_content(root: Path) -> List[Finding]:
    """C12: Orchestration schemas exist and key files reference them."""
    findings: List[Finding] = []

    core_dir = get_core_dir(root)
    if core_dir is None:
        return findings  # C1 would catch this

    # Check that orchestration schema files exist
    required_schemas = [
        "context-plan.md",
        "subagent-dispatch-plan.md",
    ]
    schemas_dir = core_dir / "schemas"
    for schema_name in required_schemas:
        schema_path = schemas_dir / schema_name
        if not schema_path.is_file():
            findings.append(Finding(
                "C12", "error",
                f"Required orchestration schema missing: core/schemas/{schema_name}",
                f"core/schemas/{schema_name}"
            ))

    # Content checks: key files must mention orchestration concepts
    content_checks = [
        (core_dir / "workflows" / "context-management.md", "Context_Plan",
         "context-management.md must reference Context_Plan"),
        (core_dir / "workflows" / "subagents.md", "Subagent_Dispatch_Plan",
         "subagents.md must reference Subagent_Dispatch_Plan"),
        (core_dir / "workflows" / "long-document.md", "Context_Plan",
         "long-document.md must reference context-aware chunk sizing via Context_Plan"),
        (core_dir / "prompts" / "transcreate-coordinator.md", "Context_Plan",
         "Coordinator prompt must reference Context_Plan"),
        (core_dir / "prompts" / "transcreate-coordinator.md", "Subagent_Dispatch_Plan",
         "Coordinator prompt must reference Subagent_Dispatch_Plan"),
    ]

    # Lenient content checks for top-level docs (accept underscore or space variants)
    lenient_doc_checks = [
        (root / "README.md", ["Context_Plan", "Context Plan", "context-plan"],
         "README.md must reference Context_Plan (or Context Plan / context-plan)"),
        (root / "README.md", ["Subagent_Dispatch_Plan", "Subagent Dispatch Plan", "subagent-dispatch-plan"],
         "README.md must reference Subagent_Dispatch_Plan (or Subagent Dispatch Plan / subagent-dispatch-plan)"),
        (root / "AGENTS.md", ["Context_Plan", "Context Plan", "context-plan"],
         "AGENTS.md must reference Context_Plan (or Context Plan / context-plan)"),
        (root / "AGENTS.md", ["Subagent_Dispatch_Plan", "Subagent Dispatch Plan", "subagent-dispatch-plan"],
         "AGENTS.md must reference Subagent_Dispatch_Plan (or Subagent Dispatch Plan / subagent-dispatch-plan)"),
    ]

    for filepath, keyword, message in content_checks:
        if not filepath.is_file():
            continue  # Other checks will catch missing files
        try:
            text = filepath.read_text(encoding="utf-8")
            if keyword not in text:
                rel = filepath.relative_to(root).as_posix() if root in filepath.parents else str(filepath)
                findings.append(Finding("C12", "error", message, rel))
        except (UnicodeDecodeError, OSError):
            continue

    for filepath, keywords, message in lenient_doc_checks:
        if not filepath.is_file():
            continue
        try:
            text = filepath.read_text(encoding="utf-8")
            if not any(kw in text for kw in keywords):
                rel = filepath.relative_to(root).as_posix() if root in filepath.parents else filepath.name
                findings.append(Finding("C12", "error", message, rel))
        except (UnicodeDecodeError, OSError):
            continue

    # Check that all seven prompt files exist
    required_prompts = [
        "transcreate-coordinator.md",
        "terminology-researcher.md",
        "style-researcher.md",
        "chunk-translator.md",
        "continuity-reviewer.md",
        "fidelity-reviewer.md",
        "formatting-reviewer.md",
    ]
    prompts_dir = core_dir / "prompts"
    for prompt_name in required_prompts:
        prompt_path = prompts_dir / prompt_name
        if not prompt_path.is_file():
            findings.append(Finding(
                "C12", "error",
                f"Required prompt file missing: core/prompts/{prompt_name}",
                f"core/prompts/{prompt_name}"
            ))

    # Check adapter references to context/subagent workflows
    adapters_dir = root / "adapters"
    if adapters_dir.is_dir():
        context_ref_pattern = re.compile(r'context-management\.md|Context_Plan|context-plan\.md')
        subagent_ref_pattern = re.compile(r'subagents\.md|Subagent_Dispatch_Plan|subagent-dispatch-plan\.md')

        for adapter_dir in sorted(adapters_dir.iterdir()):
            if not adapter_dir.is_dir():
                continue
            adapter_name = adapter_dir.name
            found_context_ref = False
            found_subagent_ref = False

            for filepath in adapter_dir.rglob("*"):
                if not filepath.is_file():
                    continue
                if filepath.suffix not in (".md", ".mdc", ".yaml", ".yml", ".json"):
                    continue
                try:
                    text = filepath.read_text(encoding="utf-8")
                except (UnicodeDecodeError, OSError):
                    continue
                if context_ref_pattern.search(text):
                    found_context_ref = True
                if subagent_ref_pattern.search(text):
                    found_subagent_ref = True
                if found_context_ref and found_subagent_ref:
                    break

            if not found_context_ref:
                findings.append(Finding(
                    "C12", "warning",
                    f"Adapter '{adapter_name}' does not reference context management or Context_Plan",
                    f"adapters/{adapter_name}"
                ))
            if not found_subagent_ref:
                findings.append(Finding(
                    "C12", "warning",
                    f"Adapter '{adapter_name}' does not reference subagent orchestration or Subagent_Dispatch_Plan",
                    f"adapters/{adapter_name}"
                ))

    return findings


# ---------------------------------------------------------------------------
# Portable-first checks (C2A–C2D, C13–C16)
# ---------------------------------------------------------------------------

PORTABLE_PLATFORMS = ("portable", "root")


def _find_host_agent_files(root: Path, host_dir: str) -> List[Path]:
    """Find *.md files located in any <host_dir>/agents/ directory (source or dest layout)."""
    results: List[Path] = []
    for p in root.rglob("*.md"):
        parts = p.parts
        if ".git" in parts:
            continue
        for i in range(len(parts) - 2):
            if parts[i] == host_dir and parts[i + 1] == "agents":
                results.append(p)
                break
    return results


def check_c2a_root_skill(root: Path) -> List[Finding]:
    """C2A: Portable root SKILL.md frontmatter (skip for host-adapter destinations)."""
    findings: List[Finding] = []
    manifest = load_install_manifest(root)
    if manifest is not None and manifest.get("target_platform") not in PORTABLE_PLATFORMS:
        return findings  # host adapter destination — root SKILL.md not expected

    skill = root / "SKILL.md"
    if not skill.is_file():
        findings.append(Finding("C2A", "error", "Portable root SKILL.md is missing", "SKILL.md"))
        return findings
    try:
        text = skill.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError) as e:
        findings.append(Finding("C2A", "error", f"Cannot read root SKILL.md: {e}", "SKILL.md"))
        return findings

    fm = parse_frontmatter(text)
    if not fm:
        findings.append(Finding("C2A", "error", "Root SKILL.md has no YAML frontmatter", "SKILL.md"))
        return findings
    name = fm.get("name", "")
    desc = fm.get("description", "")
    if name != "d-transcreate":
        findings.append(Finding("C2A", "error", f"Root SKILL.md name must be 'd-transcreate' (found: '{name}')", "SKILL.md"))
    if not desc:
        findings.append(Finding("C2A", "error", "Root SKILL.md frontmatter missing description", "SKILL.md"))
    elif "translat" not in desc.lower():
        findings.append(Finding("C2A", "error", "Root SKILL.md description lacks trigger language (translation/transcreation)", "SKILL.md"))
    return findings


def check_c2b_claude_agents(root: Path) -> List[Finding]:
    """C2B: Claude agent files have name (matching stem) and description frontmatter."""
    findings: List[Finding] = []
    for fp in _find_host_agent_files(root, ".claude"):
        rel = fp.relative_to(root).as_posix()
        try:
            fm = parse_frontmatter(fp.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, OSError) as e:
            findings.append(Finding("C2B", "error", f"Cannot read Claude agent file: {e}", rel))
            continue
        if not fm:
            findings.append(Finding("C2B", "error", "Claude agent file missing YAML frontmatter", rel))
            continue
        name = fm.get("name", "")
        if not name:
            findings.append(Finding("C2B", "error", "Claude agent frontmatter missing 'name'", rel))
        elif name != fp.stem:
            findings.append(Finding("C2B", "error", f"Claude agent 'name' ('{name}') must match filename stem ('{fp.stem}')", rel))
        if not fm.get("description"):
            findings.append(Finding("C2B", "error", "Claude agent frontmatter missing 'description'", rel))
    return findings


def check_c2c_opencode_agents(root: Path) -> List[Finding]:
    """C2C: OpenCode agent files have description and mode: subagent frontmatter."""
    findings: List[Finding] = []
    for fp in _find_host_agent_files(root, ".opencode"):
        rel = fp.relative_to(root).as_posix()
        try:
            fm = parse_frontmatter(fp.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, OSError) as e:
            findings.append(Finding("C2C", "error", f"Cannot read OpenCode agent file: {e}", rel))
            continue
        if not fm:
            findings.append(Finding("C2C", "error", "OpenCode agent file missing YAML frontmatter", rel))
            continue
        if not fm.get("description"):
            findings.append(Finding("C2C", "error", "OpenCode agent frontmatter missing 'description'", rel))
        mode = fm.get("mode", "")
        if not mode:
            findings.append(Finding("C2C", "error", "OpenCode agent frontmatter missing 'mode'", rel))
        elif mode not in ("subagent", "primary", "all"):
            findings.append(Finding("C2C", "error", f"OpenCode agent 'mode' must be subagent/primary/all (found: '{mode}')", rel))
        elif mode != "subagent":
            findings.append(Finding("C2C", "error", f"OpenCode role agent 'mode' must be 'subagent' (found: '{mode}')", rel))
    return findings


def check_c2d_opencode_config(root: Path) -> List[Finding]:
    """C2D: opencode.json shape is valid (no top-level name/description; instructions is list)."""
    findings: List[Finding] = []
    for cfg in root.rglob("opencode.json"):
        if ".git" in cfg.parts:
            continue
        rel = cfg.relative_to(root).as_posix()
        try:
            data = json.loads(cfg.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as e:
            findings.append(Finding("C2D", "error", f"opencode.json is not valid JSON: {e}", rel))
            continue
        if not isinstance(data, dict):
            findings.append(Finding("C2D", "error", "opencode.json must be a JSON object", rel))
            continue
        for bad in ("name", "description"):
            if bad in data:
                findings.append(Finding("C2D", "error", f"opencode.json must not have top-level '{bad}'", rel))
        if "instructions" in data:
            instr = data["instructions"]
            if not (isinstance(instr, list) and all(isinstance(x, str) for x in instr)):
                findings.append(Finding("C2D", "error", "opencode.json 'instructions' must be a list of strings", rel))
        schema = data.get("$schema")
        if schema is not None and schema != "https://opencode.ai/config.json":
            findings.append(Finding("C2D", "error", "opencode.json '$schema' must be https://opencode.ai/config.json", rel))
    return findings


def check_c13_hygiene(root: Path, release: bool) -> List[Finding]:
    """C13: Distribution hygiene — warn in source mode, error in --release mode."""
    findings: List[Finding] = []
    level = "error" if release else "warning"
    for name in ("_archive", ".kiro", "_tmp_build", "_tmp_validate"):
        if (root / name).is_dir():
            findings.append(Finding("C13", level, f"Distribution should not include '{name}/'", name))
    manifest_at_root = root / ".d-transcreate-manifest.json"
    if release and manifest_at_root.is_file() and (root / "scripts").is_dir():
        findings.append(Finding("C13", "error", "Source tree should not contain a build manifest at root", ".d-transcreate-manifest.json"))
    return findings


def check_c14_examples(root: Path) -> List[Finding]:
    """C14: Example seed artifacts have required headings, fields, and exact glossary header."""
    findings: List[Finding] = []
    examples_dir = root / "examples"
    if not examples_dir.is_dir():
        return findings

    expected_header = ("term,preferred_translation,forbidden_translation,term_class,"
                       "context,source_location,evidence,confidence,status,notes")
    brief_headings = ["## Source", "## Target", "## Audience",
                      "## Translation Parameters", "## Output", "## Constraints", "## Quality"]
    cp_fields = ["skill_version", "platform", "max_source_words_per_chunk", "max_parallel_workers"]
    dp_fields = ["run_id", "mode", "context_plan_ref", "chunk_manifest_ref"]

    def read(p: Path) -> str:
        try:
            return p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            return ""

    for ex in sorted(examples_dir.iterdir()):
        if not ex.is_dir() or ex.name.startswith("."):
            continue
        seed = ex / "seed-artifacts"
        if not seed.is_dir():
            continue
        seed_rel = seed.relative_to(root).as_posix()

        tb = seed / "translation-brief.md"
        if not tb.is_file():
            findings.append(Finding("C14", "error", "Missing seed-artifacts/translation-brief.md", seed_rel))
        else:
            t = read(tb)
            missing = [h for h in brief_headings if h not in t]
            if missing:
                findings.append(Finding("C14", "error", f"translation-brief.md missing headings: {', '.join(missing)}", tb.relative_to(root).as_posix()))

        cp = seed / "context-plan.md"
        if not cp.is_file():
            findings.append(Finding("C14", "error", "Missing seed-artifacts/context-plan.md", seed_rel))
        else:
            t = read(cp)
            missing = [f for f in cp_fields if f not in t]
            if missing:
                findings.append(Finding("C14", "error", f"context-plan.md missing fields: {', '.join(missing)}", cp.relative_to(root).as_posix()))

        dp = seed / "subagent-dispatch-plan.md"
        if not dp.is_file():
            findings.append(Finding("C14", "error", "Missing seed-artifacts/subagent-dispatch-plan.md", seed_rel))
        else:
            t = read(dp)
            missing = [f for f in dp_fields if f not in t]
            if missing:
                findings.append(Finding("C14", "error", f"subagent-dispatch-plan.md missing fields: {', '.join(missing)}", dp.relative_to(root).as_posix()))
            if not ("Dispatch Units" in t or "dispatch_units" in t or "unit_id" in t):
                findings.append(Finding("C14", "error", "subagent-dispatch-plan.md has no dispatch units", dp.relative_to(root).as_posix()))

        gl = seed / "glossary.csv"
        if not gl.is_file():
            findings.append(Finding("C14", "error", "Missing seed-artifacts/glossary.csv", seed_rel))
        else:
            lines = read(gl).splitlines()
            header = lines[0].strip() if lines else ""
            if header != expected_header:
                findings.append(Finding("C14", "error", "glossary.csv header does not match schema header", gl.relative_to(root).as_posix()))

        if not (seed / "style-sheet.md").is_file():
            findings.append(Finding("C14", "error", "Missing seed-artifacts/style-sheet.md", seed_rel))

        readme_text = read(ex / "README.md").lower()
        name_l = ex.name.lower()
        if "fiction" in name_l:
            if not (seed / "story-bible.md").is_file() and "story-bible" not in readme_text and "story bible" not in readme_text:
                findings.append(Finding("C14", "warning", "Fiction example has no story-bible.md and README does not explain the omission", seed_rel))
        elif any(k in name_l for k in ("technical", "legal", "manual", "policy", "medical")):
            if not (seed / "domain-map.md").is_file() and "domain-map" not in readme_text and "domain map" not in readme_text:
                findings.append(Finding("C14", "warning", "Technical/legal example has no domain-map.md and README does not explain the omission", seed_rel))

    return findings


def check_c15_version(root: Path) -> List[Finding]:
    """C15: VERSION matches core/d-transcreate.md version line and appears in CHANGELOG.md."""
    findings: List[Finding] = []
    version_file = root / "VERSION"
    if not version_file.is_file():
        return findings  # C1 catches missing VERSION
    try:
        version = version_file.read_text(encoding="utf-8").strip()
    except (UnicodeDecodeError, OSError):
        return findings
    if not version:
        findings.append(Finding("C15", "error", "VERSION file is empty", "VERSION"))
        return findings

    core_dir = get_core_dir(root)
    if core_dir:
        entry = core_dir / "d-transcreate.md"
        if entry.is_file():
            try:
                t = entry.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                t = ""
            m = re.search(r'(?mi)^Version:\s*(.+?)\s*$', t)
            if not m:
                findings.append(Finding("C15", "error", "core/d-transcreate.md has no 'Version:' line", "core/d-transcreate.md"))
            elif m.group(1).strip() != version:
                findings.append(Finding("C15", "error", f"core/d-transcreate.md version ('{m.group(1).strip()}') does not match VERSION ('{version}')", "core/d-transcreate.md"))

    changelog = root / "CHANGELOG.md"
    if changelog.is_file():
        try:
            if version not in changelog.read_text(encoding="utf-8"):
                findings.append(Finding("C15", "error", f"CHANGELOG.md has no entry for version {version}", "CHANGELOG.md"))
        except (UnicodeDecodeError, OSError):
            pass
    return findings


def check_c16_requirement_refs(root: Path, release: bool) -> List[Finding]:
    """C16: No internal Requirement/Req N references in distributed docs (error in --release)."""
    findings: List[Finding] = []
    level = "error" if release else "warning"
    pattern = re.compile(r'\b(Requirement|Req)\s+[0-9]')

    targets: List[Path] = []
    for rel in ("SKILL.md", "AGENTS.md"):
        p = root / rel
        if p.is_file():
            targets.append(p)
    for sub in ("core", "adapters", "examples"):
        d = root / sub
        if d.is_dir():
            for p in d.rglob("*"):
                if p.is_file() and p.suffix in (".md", ".mdc", ".csv", ".yaml", ".yml", ".json", ".txt"):
                    targets.append(p)

    for p in targets:
        if ".git" in p.parts or ".kiro" in p.parts:
            continue
        try:
            text = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for i, line in enumerate(text.split("\n"), 1):
            if pattern.search(line):
                findings.append(Finding("C16", level, f"Internal requirement reference on line {i}: {line.strip()[:80]}", p.relative_to(root).as_posix()))
                break
    return findings


def check_c17_templates(root: Path) -> List[Finding]:
    """C17: Template headers match the artifact schemas (only when templates/ exists)."""
    findings: List[Finding] = []
    templates = root / "templates"
    if not templates.is_dir():
        return findings

    csv_checks = [
        ("glossary.csv", "term,preferred_translation,forbidden_translation,term_class,"
                         "context,source_location,evidence,confidence,status,notes"),
        ("chunk-manifest.csv", "chunk_id,source_location,word_or_page_range,semantic_unit,"
                              "dependencies,assigned_to,status,output_path,qa_status,notes"),
    ]
    for name, expected in csv_checks:
        p = templates / name
        if not p.is_file():
            findings.append(Finding("C17", "error", f"Missing template: templates/{name}", f"templates/{name}"))
            continue
        try:
            lines = p.read_text(encoding="utf-8").splitlines()
        except (UnicodeDecodeError, OSError):
            lines = []
        if (lines[0].strip() if lines else "") != expected:
            findings.append(Finding("C17", "error", f"templates/{name} header does not match schema", f"templates/{name}"))

    tb = templates / "translation-brief.md"
    if tb.is_file():
        t = tb.read_text(encoding="utf-8", errors="replace")
        missing = [h for h in ("## Source", "## Target", "## Audience", "## Output", "## Constraints", "## Quality") if h not in t]
        if missing:
            findings.append(Finding("C17", "error", f"templates/translation-brief.md missing headings: {', '.join(missing)}", "templates/translation-brief.md"))

    cp = templates / "context-plan.md"
    if cp.is_file():
        t = cp.read_text(encoding="utf-8", errors="replace")
        missing = [f for f in ("skill_version", "platform", "max_source_words_per_chunk", "max_parallel_workers") if f not in t]
        if missing:
            findings.append(Finding("C17", "error", f"templates/context-plan.md missing fields: {', '.join(missing)}", "templates/context-plan.md"))

    return findings


# ---------------------------------------------------------------------------
# Main orchestration
# ---------------------------------------------------------------------------

def run_all_checks(root: Path, line_budget: int, duplication_threshold: int, release: bool = False) -> List[Finding]:
    """Run all validation checks and return findings."""
    findings: List[Finding] = []

    findings.extend(check_c1_required_files(root))
    findings.extend(check_c2_frontmatter(root))
    findings.extend(check_c2a_root_skill(root))
    findings.extend(check_c2b_claude_agents(root))
    findings.extend(check_c2c_opencode_agents(root))
    findings.extend(check_c2d_opencode_config(root))
    findings.extend(check_c3_internal_links(root))
    findings.extend(check_c4_todo_markers(root))
    findings.extend(check_c5_adapter_references_core(root))
    findings.extend(check_c6_line_budget(root, line_budget))
    findings.extend(check_c7_duplication(root, duplication_threshold))
    findings.extend(check_c8_utf8_encoding(root))
    findings.extend(check_c9_schema_existence(root))
    findings.extend(check_c10_example_readme(root))
    findings.extend(check_c11_install_manifest(root))
    findings.extend(check_c12_orchestration_content(root))
    findings.extend(check_c13_hygiene(root, release))
    findings.extend(check_c14_examples(root))
    findings.extend(check_c15_version(root))
    findings.extend(check_c16_requirement_refs(root, release))
    findings.extend(check_c17_templates(root))

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
    parser.add_argument(
        "--release",
        action="store_true",
        default=False,
        help="Release mode: escalate distribution-hygiene and requirement-reference findings to errors"
    )

    args = parser.parse_args()
    root = Path(args.path).resolve()

    if not root.is_dir():
        print(f"Error: path '{args.path}' is not a directory", file=sys.stderr)
        return 1

    findings = run_all_checks(root, args.line_budget, args.duplication_threshold, args.release)

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
    import io
    if sys.stdout.encoding != "utf-8":
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    if sys.stderr.encoding != "utf-8":
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
    sys.exit(main())
