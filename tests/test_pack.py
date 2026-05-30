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
PACK_VERSION = (REPO_ROOT / "VERSION").read_text(encoding="utf-8").strip()
GLOSSARY_HEADER = ("term,preferred_translation,forbidden_translation,term_class,"
                   "context,source_location,evidence,confidence,status,notes")


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
                    self.assertEqual(manifest["pack_version"], PACK_VERSION)
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

    def test_root_skill_frontmatter_valid(self):
        skill = REPO_ROOT / "SKILL.md"
        self.assertTrue(skill.is_file(), "Portable root SKILL.md must exist")
        text = skill.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---"), "Root SKILL.md must start with frontmatter")
        self.assertIn("name: d-transcreate", text)
        self.assertIn("description:", text)

    def test_claude_agents_have_frontmatter(self):
        agents_dir = REPO_ROOT / "adapters" / "claude-code" / ".claude" / "agents"
        files = sorted(agents_dir.glob("*.md"))
        self.assertEqual(len(files), 7, "Expected 7 Claude agent files")
        for f in files:
            with self.subTest(agent=f.name):
                text = f.read_text(encoding="utf-8")
                self.assertTrue(text.startswith("---"), f"{f.name} missing frontmatter")
                self.assertIn(f"name: {f.stem}", text)
                self.assertIn("description:", text)

    def test_opencode_agents_have_frontmatter(self):
        agents_dir = REPO_ROOT / "adapters" / "opencode" / ".opencode" / "agents"
        files = sorted(agents_dir.glob("*.md"))
        self.assertEqual(len(files), 7, "Expected 7 OpenCode agent files")
        for f in files:
            with self.subTest(agent=f.name):
                text = f.read_text(encoding="utf-8")
                self.assertTrue(text.startswith("---"), f"{f.name} missing frontmatter")
                self.assertIn("description:", text)
                self.assertIn("mode: subagent", text)

    def test_validator_rejects_missing_claude_agent_frontmatter(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo_copy = Path(tmp) / "repo"
            copy_repo_without_git(repo_copy)
            agent = repo_copy / "adapters" / "claude-code" / ".claude" / "agents" / "chunk-translator.md"
            body = agent.read_text(encoding="utf-8").split("---", 2)[-1].lstrip()
            agent.write_text(body, encoding="utf-8")
            result = run_command(PYTHON, VALIDATE, repo_copy, check=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("C2B", result.stdout)

    def test_validator_rejects_missing_opencode_mode(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo_copy = Path(tmp) / "repo"
            copy_repo_without_git(repo_copy)
            agent = repo_copy / "adapters" / "opencode" / ".opencode" / "agents" / "chunk-translator.md"
            agent.write_text(
                agent.read_text(encoding="utf-8").replace("mode: subagent\n", ""),
                encoding="utf-8",
            )
            result = run_command(PYTHON, VALIDATE, repo_copy, check=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("C2C", result.stdout)

    def test_opencode_json_shape_valid(self):
        cfg = json.loads((REPO_ROOT / "adapters" / "opencode" / "opencode.json").read_text(encoding="utf-8"))
        self.assertNotIn("name", cfg)
        self.assertNotIn("description", cfg)
        self.assertIsInstance(cfg.get("instructions"), list)
        with tempfile.TemporaryDirectory() as tmp:
            repo_copy = Path(tmp) / "repo"
            copy_repo_without_git(repo_copy)
            cfg_path = repo_copy / "adapters" / "opencode" / "opencode.json"
            cfg_path.write_text(
                json.dumps({"name": "d-transcreate", "instructions": "core/d-transcreate.md"}),
                encoding="utf-8",
            )
            result = run_command(PYTHON, VALIDATE, repo_copy, check=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("C2D", result.stdout)

    def test_version_consistency(self):
        core = (REPO_ROOT / "core" / "d-transcreate.md").read_text(encoding="utf-8")
        self.assertIn(f"Version: {PACK_VERSION}", core)
        changelog = (REPO_ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        self.assertIn(PACK_VERSION, changelog)

    def test_examples_seed_artifacts_have_required_fields(self):
        examples_dir = REPO_ROOT / "examples"
        for ex in sorted(examples_dir.iterdir()):
            if not ex.is_dir() or ex.name.startswith("."):
                continue
            seed = ex / "seed-artifacts"
            if not seed.is_dir():
                continue
            with self.subTest(example=ex.name):
                cp = (seed / "context-plan.md").read_text(encoding="utf-8")
                for field in ("skill_version", "platform", "max_source_words_per_chunk", "max_parallel_workers"):
                    self.assertIn(field, cp)
                dp = (seed / "subagent-dispatch-plan.md").read_text(encoding="utf-8")
                for field in ("run_id", "mode", "context_plan_ref", "chunk_manifest_ref"):
                    self.assertIn(field, dp)
                header = (seed / "glossary.csv").read_text(encoding="utf-8").splitlines()[0].strip()
                self.assertEqual(header, GLOSSARY_HEADER)

    def test_release_hygiene_warns_or_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo_copy = Path(tmp) / "repo"
            copy_repo_without_git(repo_copy)
            archive = repo_copy / "_archive"
            archive.mkdir(exist_ok=True)
            (archive / "old.md").write_text("old\n", encoding="utf-8")
            normal = run_command(PYTHON, VALIDATE, repo_copy, "--json", check=False)
            self.assertTrue(json.loads(normal.stdout)["summary"]["passed"])
            release = run_command(PYTHON, VALIDATE, repo_copy, "--release", check=False)
            self.assertNotEqual(release.returncode, 0)
            self.assertIn("C13", release.stdout)


if __name__ == "__main__":
    unittest.main()
