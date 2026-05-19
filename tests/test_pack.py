#!/usr/bin/env python3
"""Smoke tests for d-transcreate-skill packaging and validation."""

import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATE = REPO_ROOT / "scripts" / "validate_pack.py"
BUILD = REPO_ROOT / "scripts" / "build_adapters.py"
PLATFORMS = ("codex", "claude-code", "cursor", "opencode", "generic")


def run_command(*args, check=True):
    return subprocess.run(
        [str(arg) for arg in args],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=check,
    )


def copy_repo_without_git(dest):
    def ignore(_dir, names):
        ignored = {".git", "_tmp_validate", "__pycache__", ".pytest_cache"}
        return {name for name in names if name in ignored or name.endswith(".pyc")}

    shutil.copytree(REPO_ROOT, dest, ignore=ignore)


class PackSmokeTests(unittest.TestCase):
    def test_repo_validates(self):
        result = run_command("python3", VALIDATE, REPO_ROOT, "--json")
        self.assertTrue(json.loads(result.stdout)["summary"]["passed"])

    def test_all_copy_adapters_build_and_validate(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            for platform in PLATFORMS:
                with self.subTest(platform=platform):
                    dest = tmp_path / platform
                    run_command("python3", BUILD, "--platform", platform, "--dest", dest)
                    run_command("python3", VALIDATE, dest)

                    manifest = json.loads((dest / ".d-transcreate-manifest.json").read_text())
                    self.assertEqual(manifest["pack_version"], "0.2.0")
                    self.assertTrue(manifest["source_commit"])
                    manifest_paths = {entry["path"] for entry in manifest["files"]}
                    self.assertTrue({"README.md", "LICENSE", "VERSION", "CHANGELOG.md"} <= manifest_paths)

    def test_reference_core_install_validates(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "generic-reference"
            run_command(
                "python3",
                BUILD,
                "--platform",
                "generic",
                "--dest",
                dest,
                "--core-strategy",
                "reference",
                "--shared-core-path",
                REPO_ROOT / "core",
            )
            run_command("python3", VALIDATE, dest)

    def test_conflicts_require_force(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "conflict"
            dest.mkdir()
            (dest / "README.md").write_text("existing\n", encoding="utf-8")
            result = run_command("python3", BUILD, "--platform", "generic", "--dest", dest, check=False)
            self.assertEqual(result.returncode, 2)
            self.assertIn("README.md", result.stderr)

    def test_skill_frontmatter_requires_description(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo_copy = Path(tmp) / "repo"
            copy_repo_without_git(repo_copy)
            skill_file = repo_copy / "adapters" / "codex" / "SKILL.md"
            skill_file.write_text(
                skill_file.read_text(encoding="utf-8").replace("description:", "summary:", 1),
                encoding="utf-8",
            )
            result = run_command("python3", VALIDATE, repo_copy, check=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Frontmatter missing required field: description", result.stdout)


if __name__ == "__main__":
    unittest.main()
