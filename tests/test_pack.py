#!/usr/bin/env python3
"""Smoke tests for d-transcreate-skill packaging and validation."""

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATE = REPO_ROOT / "scripts" / "validate_pack.py"
BUILD = REPO_ROOT / "scripts" / "build_adapters.py"
PLATFORMS = ("codex", "claude-code", "cursor", "opencode", "generic")
PYTHON = sys.executable


def run_command(*args, check=True):
    return subprocess.run(
        [str(arg) for arg in args],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=check,
        encoding="utf-8",
    )


def copy_repo_without_git(dest):
    def ignore(_dir, names):
        ignored = {".git", "_tmp_validate", "__pycache__", ".pytest_cache"}
        return {name for name in names if name in ignored or name.endswith(".pyc")}

    shutil.copytree(REPO_ROOT, dest, ignore=ignore)


class PackSmokeTests(unittest.TestCase):
    def test_repo_validates(self):
        result = run_command(PYTHON, VALIDATE, REPO_ROOT, "--json")
        self.assertTrue(json.loads(result.stdout)["summary"]["passed"])

    def test_all_copy_adapters_build_and_validate(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            for platform in PLATFORMS:
                with self.subTest(platform=platform):
                    dest = tmp_path / platform
                    run_command(PYTHON, BUILD, "--platform", platform, "--dest", dest)
                    run_command(PYTHON, VALIDATE, dest)

                    manifest = json.loads((dest / ".d-transcreate-manifest.json").read_text())
                    self.assertEqual(manifest["pack_version"], "0.3.0")
                    self.assertTrue(manifest["source_commit"])
                    manifest_paths = {entry["path"] for entry in manifest["files"]}
                    self.assertTrue({"README.md", "LICENSE", "VERSION", "CHANGELOG.md"} <= manifest_paths)

    def test_reference_core_install_validates(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "generic-reference"
            run_command(
                PYTHON,
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
            run_command(PYTHON, VALIDATE, dest)

    def test_conflicts_require_force(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "conflict"
            dest.mkdir()
            (dest / "README.md").write_text("existing\n", encoding="utf-8")
            result = run_command(PYTHON, BUILD, "--platform", "generic", "--dest", dest, check=False)
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
            result = run_command(PYTHON, VALIDATE, repo_copy, check=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Frontmatter missing required field: description", result.stdout)

    def test_orchestration_schemas_exist(self):
        """Verify that context-plan.md and subagent-dispatch-plan.md exist in core/schemas/."""
        schemas_dir = REPO_ROOT / "core" / "schemas"
        self.assertTrue((schemas_dir / "context-plan.md").is_file(),
                        "core/schemas/context-plan.md must exist")
        self.assertTrue((schemas_dir / "subagent-dispatch-plan.md").is_file(),
                        "core/schemas/subagent-dispatch-plan.md must exist")

    def test_orchestration_references_in_core(self):
        """Verify that core workflow files reference orchestration artifacts."""
        context_mgmt = (REPO_ROOT / "core" / "workflows" / "context-management.md").read_text(encoding="utf-8")
        self.assertIn("Context_Plan", context_mgmt)

        subagents = (REPO_ROOT / "core" / "workflows" / "subagents.md").read_text(encoding="utf-8")
        self.assertIn("Subagent_Dispatch_Plan", subagents)

        long_doc = (REPO_ROOT / "core" / "workflows" / "long-document.md").read_text(encoding="utf-8")
        self.assertIn("Context_Plan", long_doc)

        coordinator = (REPO_ROOT / "core" / "prompts" / "transcreate-coordinator.md").read_text(encoding="utf-8")
        self.assertIn("Context_Plan", coordinator)
        self.assertIn("Subagent_Dispatch_Plan", coordinator)

    def test_examples_include_orchestration_artifacts(self):
        """Verify that examples include context-plan and subagent-dispatch-plan files."""
        examples_dir = REPO_ROOT / "examples"
        for example_dir in examples_dir.iterdir():
            if not example_dir.is_dir() or example_dir.name.startswith("."):
                continue
            seed_dir = example_dir / "seed-artifacts"
            if seed_dir.is_dir():
                with self.subTest(example=example_dir.name):
                    self.assertTrue(
                        (seed_dir / "context-plan.md").is_file(),
                        f"{example_dir.name}/seed-artifacts/context-plan.md must exist"
                    )
                    self.assertTrue(
                        (seed_dir / "subagent-dispatch-plan.md").is_file(),
                        f"{example_dir.name}/seed-artifacts/subagent-dispatch-plan.md must exist"
                    )

    def test_adapters_reference_orchestration(self):
        """Verify that built adapters reference context/subagent orchestration."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            for platform in PLATFORMS:
                with self.subTest(platform=platform):
                    dest = tmp_path / platform
                    run_command(PYTHON, BUILD, "--platform", platform, "--dest", dest)
                    # Check that at least one file references context management
                    found_context = False
                    found_subagent = False
                    for filepath in dest.rglob("*"):
                        if not filepath.is_file():
                            continue
                        try:
                            text = filepath.read_text(encoding="utf-8")
                        except (UnicodeDecodeError, OSError):
                            continue
                        if "context-management" in text or "Context_Plan" in text or "context-plan" in text:
                            found_context = True
                        if "subagents" in text or "Subagent_Dispatch_Plan" in text or "subagent-dispatch-plan" in text:
                            found_subagent = True
                        if found_context and found_subagent:
                            break
                    self.assertTrue(found_context, f"Adapter {platform} must reference context management")
                    self.assertTrue(found_subagent, f"Adapter {platform} must reference subagent orchestration")


if __name__ == "__main__":
    unittest.main()
