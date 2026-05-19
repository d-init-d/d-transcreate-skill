#!/usr/bin/env python3
"""
Adapter Build Script for d-transcreate-skill.

Installs one adapter into a destination project at the mirrored layout,
optionally bringing core/ alongside, and produces an install manifest.

Requirements: Python 3.8+ standard library only.
Exit codes: 0 success, 1 error, 2 conflict.
"""

import argparse
import hashlib
import json
import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

VALID_PLATFORMS = ("codex", "claude-code", "cursor", "opencode", "generic")
VALID_MODES = ("copy", "symlink", "dry-run")
VALID_CORE_STRATEGIES = ("copy", "reference")
MANIFEST_FILENAME = ".d-transcreate-manifest.json"

EXIT_SUCCESS = 0
EXIT_ERROR = 1
EXIT_CONFLICT = 2


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------


def get_repo_root():
    """Return the repository root (parent of the scripts/ directory)."""
    return Path(__file__).resolve().parent.parent


def sha256_file(filepath):
    """Compute SHA-256 hex digest of a file."""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def collect_files(directory):
    """
    Recursively collect all files under a directory.
    Returns a list of Path objects relative to the directory.
    """
    directory = Path(directory)
    results = []
    for root, _dirs, files in os.walk(directory):
        for fname in files:
            full = Path(root) / fname
            results.append(full.relative_to(directory))
    return sorted(results)


def rewrite_core_references(content, shared_core_path):
    """
    Rewrite relative path references to core/ in adapter file content
    to point at the shared core path instead.

    Handles patterns like:
      - core/d-transcreate.md
      - ../core/workflows/long-document.md
      - ../../core/schemas/glossary.md
    """
    import re

    # Normalize shared_core_path to use forward slashes for consistency
    shared = shared_core_path.replace("\\", "/")
    if not shared.endswith("/"):
        shared += "/"

    # Replace patterns like (../)*core/ with the shared path
    # This handles relative references from adapter files to core/
    pattern = r'(\.\./)*core/'
    replacement = shared
    return re.sub(pattern, replacement, content)


def rewrite_core_paths_for_copy(content, rel_path):
    """
    Rewrite relative path references to core/ in adapter file content
    so they resolve correctly in the destination layout where core/ is
    at the destination root.

    For a file at relative path 'a/b/c/file.md', the correct prefix to
    reach the destination root is '../../../', so core/ references become
    '../../../core/'.
    """
    import re

    # Calculate how many directories deep the file is
    depth = len(Path(rel_path).parent.parts)
    if depth == 0:
        # File is at root level, core/ is directly accessible
        correct_prefix = "core/"
    else:
        correct_prefix = "../" * depth + "core/"

    # Replace patterns like (../)*core/ with the correct relative prefix
    pattern = r'(\.\./)*core/'
    return re.sub(pattern, correct_prefix, content)


# ---------------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------------


def detect_conflicts(adapter_files, core_files, dest, core_strategy):
    """
    Check which destination files already exist.
    Returns a list of conflicting destination paths.
    """
    conflicts = []
    for rel_path in adapter_files:
        dest_path = dest / rel_path
        if dest_path.exists():
            conflicts.append(str(rel_path))

    if core_strategy == "copy":
        for rel_path in core_files:
            dest_path = dest / "core" / rel_path
            if dest_path.exists():
                conflicts.append(str(Path("core") / rel_path))

    return conflicts


def execute_copy(adapter_dir, adapter_files, core_dir, core_files, dest,
                 core_strategy, shared_core_path, force):
    """
    Copy adapter files (and optionally core/) to destination.
    Returns list of file records for the manifest.
    """
    repo_root = get_repo_root()
    file_records = []

    for rel_path in adapter_files:
        src = adapter_dir / rel_path
        dst = dest / rel_path
        dst.parent.mkdir(parents=True, exist_ok=True)

        if core_strategy == "reference" and shared_core_path:
            # Read and rewrite core references for text files
            try:
                content = src.read_text(encoding="utf-8")
                rewritten = rewrite_core_references(content, shared_core_path)
                dst.write_text(rewritten, encoding="utf-8")
            except (UnicodeDecodeError, ValueError):
                # Binary file — just copy
                shutil.copy2(src, dst)
        elif core_strategy == "copy":
            # Rewrite relative core/ paths so they resolve in the destination layout
            try:
                content = src.read_text(encoding="utf-8")
                rewritten = rewrite_core_paths_for_copy(content, rel_path)
                dst.write_text(rewritten, encoding="utf-8")
            except (UnicodeDecodeError, ValueError):
                # Binary file — just copy
                shutil.copy2(src, dst)
        else:
            shutil.copy2(src, dst)

        file_records.append({
            "path": str(rel_path).replace("\\", "/"),
            "sha256": sha256_file(dst),
            "from": str(
                src.relative_to(repo_root)
            ).replace("\\", "/"),
        })

    if core_strategy == "copy":
        for rel_path in core_files:
            src = core_dir / rel_path
            dst = dest / "core" / rel_path
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)

            file_records.append({
                "path": str(Path("core") / rel_path).replace("\\", "/"),
                "sha256": sha256_file(dst),
                "from": str(
                    src.relative_to(repo_root)
                ).replace("\\", "/"),
            })

    return file_records


def execute_symlink(adapter_dir, adapter_files, core_dir, core_files, dest,
                    core_strategy, shared_core_path, force):
    """
    Create symlinks from destination to source files.
    Returns list of file records for the manifest.
    """
    repo_root = get_repo_root()
    file_records = []

    for rel_path in adapter_files:
        src = adapter_dir / rel_path
        dst = dest / rel_path
        dst.parent.mkdir(parents=True, exist_ok=True)

        if dst.exists() or dst.is_symlink():
            dst.unlink()

        os.symlink(src.resolve(), dst)

        file_records.append({
            "path": str(rel_path).replace("\\", "/"),
            "sha256": sha256_file(src),
            "from": str(
                src.relative_to(repo_root)
            ).replace("\\", "/"),
        })

    if core_strategy == "copy":
        for rel_path in core_files:
            src = core_dir / rel_path
            dst = dest / "core" / rel_path
            dst.parent.mkdir(parents=True, exist_ok=True)

            if dst.exists() or dst.is_symlink():
                dst.unlink()

            os.symlink(src.resolve(), dst)

            file_records.append({
                "path": str(Path("core") / rel_path).replace("\\", "/"),
                "sha256": sha256_file(src),
                "from": str(
                    src.relative_to(repo_root)
                ).replace("\\", "/"),
            })

    return file_records


def execute_dry_run(adapter_dir, adapter_files, core_dir, core_files, dest,
                    core_strategy, shared_core_path):
    """
    Print planned operations without writing anything.
    """
    repo_root = get_repo_root()

    print("=== DRY RUN: Planned operations ===\n")

    for rel_path in adapter_files:
        src = adapter_dir / rel_path
        dst = dest / rel_path
        src_display = str(src.relative_to(repo_root)).replace("\\", "/")
        dst_display = str(dst).replace("\\", "/")

        if core_strategy == "reference" and shared_core_path:
            print(f"  COPY (rewrite core refs): {src_display} -> {dst_display}")
        else:
            print(f"  COPY: {src_display} -> {dst_display}")

    if core_strategy == "copy":
        for rel_path in core_files:
            src = core_dir / rel_path
            dst = dest / "core" / rel_path
            src_display = str(src.relative_to(repo_root)).replace("\\", "/")
            dst_display = str(dst).replace("\\", "/")
            print(f"  COPY: {src_display} -> {dst_display}")

    if core_strategy == "reference" and shared_core_path:
        print(f"\n  Core references rewritten to: {shared_core_path}")

    print(f"\n  Total files: {len(adapter_files) + (len(core_files) if core_strategy == 'copy' else 0)}")
    print("  Manifest: NOT written (dry-run mode)")


def write_manifest(dest, platform, mode, core_strategy, shared_core_path,
                   file_records):
    """
    Write .d-transcreate-manifest.json to the destination.

    Required fields per validate_pack.py C11 check:
      manifest_version, target_platform, files
    """
    repo_root = get_repo_root()

    manifest = {
        "manifest_version": "1.0",
        "target_platform": platform,
        "mode": mode,
        "core_strategy": core_strategy,
        "source_path": str(repo_root).replace("\\", "/"),
        "build_timestamp": datetime.now(timezone.utc).isoformat(),
        "files": [{"path": r["path"], "sha256": r["sha256"]} for r in file_records],
    }

    if core_strategy == "reference" and shared_core_path:
        manifest["shared_core_path"] = shared_core_path

    manifest_path = dest / MANIFEST_FILENAME
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    return manifest_path


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def build_parser():
    """Build the argument parser."""
    parser = argparse.ArgumentParser(
        prog="build_adapters",
        description="Install a d-transcreate adapter pack into a destination project.",
    )
    parser.add_argument(
        "--platform",
        required=True,
        choices=VALID_PLATFORMS,
        help="Target platform adapter to install.",
    )
    parser.add_argument(
        "--dest",
        required=True,
        type=str,
        help="Destination directory path.",
    )
    parser.add_argument(
        "--mode",
        choices=VALID_MODES,
        default="copy",
        help="Operation mode: copy, symlink, or dry-run. Default: copy.",
    )
    parser.add_argument(
        "--core-strategy",
        choices=VALID_CORE_STRATEGIES,
        default="copy",
        dest="core_strategy",
        help="How to handle core/ files: copy them to dest, or reference a shared path. Default: copy.",
    )
    parser.add_argument(
        "--shared-core-path",
        type=str,
        default=None,
        dest="shared_core_path",
        help="Path to shared core/ location. Used with --core-strategy=reference.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Overwrite existing files without conflict check.",
    )
    return parser


def main():
    """Main entry point."""
    parser = build_parser()
    args = parser.parse_args()

    # Validate arguments
    if args.core_strategy == "reference" and not args.shared_core_path:
        print("ERROR: --shared-core-path is required when --core-strategy=reference",
              file=sys.stderr)
        sys.exit(EXIT_ERROR)

    repo_root = get_repo_root()
    adapter_dir = repo_root / "adapters" / args.platform
    core_dir = repo_root / "core"
    dest = Path(args.dest).resolve()

    # Validate source directories exist
    if not adapter_dir.is_dir():
        print(f"ERROR: Adapter directory not found: {adapter_dir}", file=sys.stderr)
        sys.exit(EXIT_ERROR)

    if not core_dir.is_dir():
        print(f"ERROR: Core directory not found: {core_dir}", file=sys.stderr)
        sys.exit(EXIT_ERROR)

    # Collect files
    adapter_files = collect_files(adapter_dir)
    core_files = collect_files(core_dir) if args.core_strategy == "copy" else []

    if not adapter_files:
        print(f"ERROR: No files found in adapter directory: {adapter_dir}",
              file=sys.stderr)
        sys.exit(EXIT_ERROR)

    # Dry-run mode: print and exit
    if args.mode == "dry-run":
        execute_dry_run(
            adapter_dir, adapter_files, core_dir, core_files, dest,
            args.core_strategy, args.shared_core_path,
        )
        sys.exit(EXIT_SUCCESS)

    # Conflict detection (skip if --force)
    if not args.force:
        conflicts = detect_conflicts(
            adapter_files, core_files, dest, args.core_strategy,
        )
        if conflicts:
            print("CONFLICT: The following files already exist at the destination:",
                  file=sys.stderr)
            for c in conflicts:
                print(f"  - {c}", file=sys.stderr)
            print("\nUse --force to overwrite.", file=sys.stderr)
            sys.exit(EXIT_CONFLICT)

    # Create destination directory
    dest.mkdir(parents=True, exist_ok=True)

    # Execute the operation
    if args.mode == "copy":
        file_records = execute_copy(
            adapter_dir, adapter_files, core_dir, core_files, dest,
            args.core_strategy, args.shared_core_path, args.force,
        )
    elif args.mode == "symlink":
        file_records = execute_symlink(
            adapter_dir, adapter_files, core_dir, core_files, dest,
            args.core_strategy, args.shared_core_path, args.force,
        )
    else:
        print(f"ERROR: Unknown mode: {args.mode}", file=sys.stderr)
        sys.exit(EXIT_ERROR)

    # Write manifest
    manifest_path = write_manifest(
        dest, args.platform, args.mode, args.core_strategy,
        args.shared_core_path, file_records,
    )

    # Summary
    print(f"Successfully installed {args.platform} adapter to: {dest}")
    print(f"  Mode: {args.mode}")
    print(f"  Core strategy: {args.core_strategy}")
    print(f"  Files written: {len(file_records)}")
    print(f"  Manifest: {manifest_path}")

    sys.exit(EXIT_SUCCESS)


if __name__ == "__main__":
    main()
