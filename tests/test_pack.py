#!/usr/bin/env python3
"""Smoke tests for d-transcreate-skill packaging and validation."""

import csv
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATE = REPO_ROOT / "scripts" / "validate_pack.py"
BUILD = REPO_ROOT / "scripts" / "build_adapters.py"
BOOK_OPS = REPO_ROOT / "scripts" / "book_ops.py"
PLATFORMS = ("codex", "claude-code", "cursor", "opencode", "antigravity", "generic")
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

    def test_built_adapters_use_root_relative_core_paths(self):
        """Built adapters must never contain ../-escaping core/ references —
        agent runtimes resolve paths from the project root, so ../core/ breaks
        at runtime and workers lose their role prompts."""
        import re
        escape_pattern = re.compile(r'(?:\.\./)+core/')
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            for platform in PLATFORMS:
                with self.subTest(platform=platform):
                    dest = tmp_path / platform
                    run_command(PYTHON, BUILD, "--platform", platform, "--dest", dest)
                    for filepath in dest.rglob("*"):
                        if not filepath.is_file():
                            continue
                        if filepath.suffix not in (".md", ".mdc", ".yaml", ".yml", ".json"):
                            continue
                        # Metadata prose (changelog/readme) may mention the
                        # broken pattern historically; instructions may not.
                        if filepath.parent == dest and filepath.name in ("CHANGELOG.md", "README.md"):
                            continue
                        text = filepath.read_text(encoding="utf-8", errors="replace")
                        self.assertIsNone(
                            escape_pattern.search(text),
                            f"{platform}: {filepath} contains a parent-escaping core/ reference",
                        )

    def test_built_claude_agents_keep_core_prompt_references(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "claude-code"
            run_command(PYTHON, BUILD, "--platform", "claude-code", "--dest", dest)
            agent = dest / ".claude" / "agents" / "chunk-translator.md"
            text = agent.read_text(encoding="utf-8")
            self.assertIn("core/prompts/chunk-translator.md", text)
            self.assertNotIn("../core/", text)

    def test_validator_rejects_parent_escaping_core_refs(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo_copy = Path(tmp) / "repo"
            copy_repo_without_git(repo_copy)
            agent = repo_copy / "adapters" / "claude-code" / ".claude" / "agents" / "chunk-translator.md"
            agent.write_text(
                agent.read_text(encoding="utf-8").replace(
                    "core/prompts/chunk-translator.md",
                    "../../core/prompts/chunk-translator.md",
                    1,
                ),
                encoding="utf-8",
            )
            result = run_command(PYTHON, VALIDATE, repo_copy, check=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("C18", result.stdout)

    def test_phase_canon_is_consistent(self):
        """Entrypoint and long-document workflow declare the same 8 phases."""
        import re
        entry = (REPO_ROOT / "core" / "d-transcreate.md").read_text(encoding="utf-8")
        long_doc = (REPO_ROOT / "core" / "workflows" / "long-document.md").read_text(encoding="utf-8")
        entry_phases = [int(m.group(1)) for m in re.finditer(r'(?m)^###\s+Phase\s+(\d+)\s+—', entry)]
        long_phases = [int(m.group(1)) for m in re.finditer(r'(?m)^##\s+Phase\s+(\d+):', long_doc)]
        self.assertEqual(entry_phases, list(range(1, 9)))
        self.assertEqual(long_phases, list(range(1, 9)))

    def test_validator_rejects_phase_drift(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo_copy = Path(tmp) / "repo"
            copy_repo_without_git(repo_copy)
            long_doc = repo_copy / "core" / "workflows" / "long-document.md"
            long_doc.write_text(
                long_doc.read_text(encoding="utf-8").replace(
                    "## Phase 3: Research Terminology and Style",
                    "## Phase 3: Segmenting (Chunking)",
                    1,
                ),
                encoding="utf-8",
            )
            result = run_command(PYTHON, VALIDATE, repo_copy, check=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("C19", result.stdout)

    def test_contract_card_present_and_enforced(self):
        subagents = (REPO_ROOT / "core" / "workflows" / "subagents.md").read_text(encoding="utf-8")
        self.assertIn("Worker Contract Card", subagents)
        self.assertIn("WORKER CONTRACT CARD", subagents)
        coordinator = (REPO_ROOT / "core" / "prompts" / "transcreate-coordinator.md").read_text(encoding="utf-8")
        self.assertIn("Contract Card", coordinator)
        with tempfile.TemporaryDirectory() as tmp:
            repo_copy = Path(tmp) / "repo"
            copy_repo_without_git(repo_copy)
            f = repo_copy / "core" / "workflows" / "subagents.md"
            f.write_text(
                f.read_text(encoding="utf-8").replace("Worker Contract Card", "Worker Rules"),
                encoding="utf-8",
            )
            result = run_command(PYTHON, VALIDATE, repo_copy, check=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("C20", result.stdout)

    def test_single_writer_rule_for_unresolved_issues(self):
        """No distributed doc may instruct workers to write the log directly."""
        offenders = []
        for sub in ("core", "adapters"):
            for p in (REPO_ROOT / sub).rglob("*"):
                if not p.is_file() or p.suffix not in (".md", ".mdc"):
                    continue
                text = p.read_text(encoding="utf-8", errors="replace").lower()
                if "write findings to the unresolved" in text or "writing findings to the unresolved" in text:
                    offenders.append(p.relative_to(REPO_ROOT).as_posix())
        self.assertEqual(offenders, [], f"Docs still tell workers to write the log: {offenders}")

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

    def test_d_research_module_and_dossier_exist(self):
        mod = REPO_ROOT / "core" / "workflows" / "d-research-module.md"
        schema = REPO_ROOT / "core" / "schemas" / "research-dossier.md"
        tpl = REPO_ROOT / "templates" / "research-dossier.md"
        locale_vi = REPO_ROOT / "core" / "locales" / "vi-VN.md"
        for p in (mod, schema, tpl, locale_vi):
            self.assertTrue(p.is_file(), f"Missing required v1.0.0 file: {p}")
        low = mod.read_text(encoding="utf-8").lower()
        self.assertIn("harvest", low)
        self.assertIn("authorial intent", low)
        self.assertIn("mindset", low)

        with tempfile.TemporaryDirectory() as tmp:
            repo_copy = Path(tmp) / "repo"
            copy_repo_without_git(repo_copy)
            (repo_copy / "core" / "workflows" / "d-research-module.md").unlink()
            res = run_command(PYTHON, VALIDATE, repo_copy, check=False)
            self.assertNotEqual(res.returncode, 0)
            self.assertIn("C21", res.stdout)

    def test_shared_memory_glossary_vi_valid(self):
        readme = REPO_ROOT / "memory" / "README.md"
        gl = REPO_ROOT / "memory" / "glossary-vi.csv"
        self.assertTrue(readme.is_file(), "memory/README.md must exist")
        self.assertTrue(gl.is_file(), "memory/glossary-vi.csv must exist")

        raw = gl.read_bytes()
        self.assertFalse(raw.startswith(b"\xef\xbb\xbf"), "memory/glossary-vi.csv must not have UTF-8 BOM")
        text = raw.decode("utf-8")
        with gl.open("r", encoding="utf-8", newline="") as f:
            rows = list(csv.reader(f))
        self.assertGreaterEqual(len(rows), 21, "memory/glossary-vi.csv must have header + >= 20 rows")
        self.assertEqual(",".join(rows[0]), GLOSSARY_HEADER)

        with tempfile.TemporaryDirectory() as tmp:
            repo_copy = Path(tmp) / "repo"
            copy_repo_without_git(repo_copy)
            (repo_copy / "memory" / "glossary-vi.csv").write_text(GLOSSARY_HEADER + "\n", encoding="utf-8")
            res = run_command(PYTHON, VALIDATE, repo_copy, check=False)
            self.assertNotEqual(res.returncode, 0)
            self.assertIn("C22", res.stdout)

    def test_validator_c23_book_ops_subcommands(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo_copy = Path(tmp) / "repo"
            copy_repo_without_git(repo_copy)
            bo = repo_copy / "scripts" / "book_ops.py"
            bo.write_text(
                bo.read_text(encoding="utf-8").replace('"sync-glossary"', '"sync_disabled"'),
                encoding="utf-8",
            )
            res = run_command(PYTHON, VALIDATE, repo_copy, check=False)
            self.assertNotEqual(res.returncode, 0)
            self.assertIn("C23", res.stdout)

    def test_book_ops_full_lifecycle(self):
        source_dir = REPO_ROOT / "examples" / "fiction-short" / "source"
        with tempfile.TemporaryDirectory() as tmp:
            ws = Path(tmp) / "book-ws"
            # 1. init & scan
            init_res = run_command(
                PYTHON, BOOK_OPS, "init",
                "--source", source_dir,
                "--target-lang", "vi",
                "--workspace", ws,
                "--json",
            )
            init_data = json.loads(init_res.stdout)
            self.assertGreaterEqual(init_data["seeded_glossary_rows"], 20)
            run_command(
                PYTHON, BOOK_OPS, "scan",
                "--source", source_dir,
                "--workspace", ws,
            )

            # 2. Add an inbox term with a forbidden translation, then sync-glossary --seed
            inbox_entry = {
                "term": "Ashveil",
                "preferred_translation": "Ashveil",
                "forbidden_translation": "Tro Tan Man",
                "term_class": "place",
                "context": "fiction-short",
                "status": "approved",
                "confidence": "high",
            }
            (ws / "glossary-inbox.jsonl").write_text(
                json.dumps(inbox_entry) + "\n",
                encoding="utf-8",
            )
            sync_res = run_command(
                PYTHON, BOOK_OPS, "sync-glossary",
                "--workspace", ws,
                "--seed",
                "--target-lang", "vi",
                "--json",
            )
            sync_data = json.loads(sync_res.stdout)
            self.assertGreaterEqual(sync_data["total_project_rows"], 21)
            self.assertEqual(sync_data["inbox_added"], 1)

            # 3. verify MUST FAIL when chunks are not 'done'
            res_not_done = run_command(PYTHON, BOOK_OPS, "verify", "--workspace", ws, check=False)
            self.assertNotEqual(res_not_done.returncode, 0)

            # Populate all chunks properly and mark manifest rows 'done'
            manifest_path = ws / "chunk-manifest.csv"
            with manifest_path.open("r", encoding="utf-8", newline="") as f:
                manifest_rows = list(csv.DictReader(f))
                fieldnames = list(manifest_rows[0].keys())

            self.assertEqual(len(manifest_rows), 3)
            valid_outputs = {}
            for idx, row in enumerate(manifest_rows, 1):
                cid = row["chunk_id"]
                src_text = (ws / "source_chunks" / f"{cid}.md").read_text(encoding="utf-8")
                # Keep full paragraph structure and sufficient word count with scene markers
                paras = [p.strip() for p in src_text.split("\n\n") if p.strip()]
                paras[0] = f"# Scene {idx} Translated ({cid})"
                translated = "\n\n".join(paras) + "\n"
                valid_outputs[cid] = translated
                out_file = ws / row["output_path"]
                out_file.parent.mkdir(parents=True, exist_ok=True)
                out_file.write_text(translated, encoding="utf-8")
                row["status"] = "done"
                row["qa_status"] = "passed"

            with manifest_path.open("w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
                writer.writeheader()
                writer.writerows(manifest_rows)

            # 4. verify MUST FAIL when a translated chunk is truncated below word ratio
            first_cid = manifest_rows[0]["chunk_id"]
            first_out = ws / manifest_rows[0]["output_path"]
            first_out.write_text("# Scene 1\n\nShort summary.\n", encoding="utf-8")
            res_trunc = run_command(PYTHON, BOOK_OPS, "verify", "--workspace", ws, "--json", check=False)
            self.assertNotEqual(res_trunc.returncode, 0)
            trunc_data = json.loads(res_trunc.stdout)
            self.assertFalse(trunc_data["passed"])
            self.assertTrue(any(e["check"] == "parity" for e in trunc_data["errors"]))
            first_out.write_text(valid_outputs[first_cid], encoding="utf-8")

            # 5. verify MUST FAIL when a forbidden_translation term appears
            second_cid = manifest_rows[1]["chunk_id"]
            second_out = ws / manifest_rows[1]["output_path"]
            second_out.write_text(valid_outputs[second_cid] + "\nTro Tan Man xuất hiện ở đây.\n", encoding="utf-8")
            res_forb = run_command(PYTHON, BOOK_OPS, "verify", "--workspace", ws, "--json", check=False)
            self.assertNotEqual(res_forb.returncode, 0)
            forb_data = json.loads(res_forb.stdout)
            self.assertFalse(forb_data["passed"])
            self.assertTrue(any(e["check"] == "glossary" for e in forb_data["errors"]))
            second_out.write_text(valid_outputs[second_cid], encoding="utf-8")

            # 6. verify PASSES and merge produces complete book containing all 3 scenes
            res_ok = run_command(PYTHON, BOOK_OPS, "verify", "--workspace", ws, "--json")
            self.assertTrue(json.loads(res_ok.stdout)["passed"])

            merged_out = ws / "merged-book.md"
            merge_res = run_command(
                PYTHON, BOOK_OPS, "merge",
                "--workspace", ws,
                "--out", merged_out,
                "--json",
            )
            merge_data = json.loads(merge_res.stdout)
            self.assertTrue(merge_data["merged"])
            self.assertEqual(merge_data["chunks_merged"], 3)
            merged_text = merged_out.read_text(encoding="utf-8")
            for idx, row in enumerate(manifest_rows, 1):
                self.assertIn(f"# Scene {idx} Translated ({row['chunk_id']})", merged_text)
            self.assertIn("## Completeness Audit", (ws / "qa-report.md").read_text(encoding="utf-8"))

    def test_antigravity_adapter_builds_and_validates(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            mock_d_research = tmp_path / "mock-d-research"
            (mock_d_research / ".git").mkdir(parents=True)
            (mock_d_research / ".git" / "HEAD").write_text("ref: refs/heads/main\n", encoding="utf-8")
            (mock_d_research / "__pycache__").mkdir()
            (mock_d_research / "__pycache__" / "mod.pyc").write_bytes(b"00")
            (mock_d_research / "SKILL.md").write_text("---\nname: d-research\ndescription: research\n---\n", encoding="utf-8")

            dest = tmp_path / "antigravity-dest"
            run_command(
                PYTHON, BUILD,
                "--platform", "antigravity",
                "--dest", dest,
                "--with-d-research", mock_d_research,
            )

            self.assertTrue((dest / "SKILL.md").is_file())
            self.assertTrue((dest / "AGENTS.md").is_file())
            self.assertTrue((dest / "memory" / "glossary-vi.csv").is_file())
            self.assertTrue((dest / "memory" / "README.md").is_file())
            self.assertTrue((dest / "templates" / "research-dossier.md").is_file())
            self.assertTrue((dest / "scripts" / "book_ops.py").is_file())
            self.assertTrue((dest / "modules" / "d-research" / "SKILL.md").is_file())
            self.assertFalse((dest / "modules" / "d-research" / ".git").exists())
            self.assertFalse((dest / "modules" / "d-research" / "__pycache__").exists())

            run_command(PYTHON, VALIDATE, dest)
            run_command(PYTHON, VALIDATE, dest, "--release")

    def test_book_ops_cjk_novel_support(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            cjk_book = tmp_path / "novel-zh.txt"
            cjk_book.write_text(
                "第一章 灰幕之门\n\n"
                "夜雾悄然笼罩了整座古城，钟楼上的铜铃在寒风中低沉地作响，街角的灯火一盏接一盏地熄灭。\n\n"
                "林默站在石阶尽头，注视着那扇尘封百年的铁门，心中却早已明白此行绝无退路可言。\n\n"
                "第二章 雾中孤塔\n\n"
                "石梯盘旋向上延伸，潮湿的青苔几乎覆盖了每一级台阶，远处隐约传来低沉的回响声。\n\n"
                "当他终于推开塔顶木门时，星图正悬在半空缓缓旋转，映照出整片沉睡的山谷。\n",
                encoding="utf-8",
            )
            ws = tmp_path / "cjk-ws"
            run_command(
                PYTHON, BOOK_OPS, "init",
                "--source", cjk_book,
                "--source-lang", "Chinese",
                "--target-lang", "vi",
                "--workspace", ws,
            )
            scan_res = run_command(
                PYTHON, BOOK_OPS, "scan",
                "--source", cjk_book,
                "--workspace", ws,
                "--json",
            )
            scan_data = json.loads(scan_res.stdout)
            self.assertEqual(scan_data["total_chunks"], 2)
            self.assertGreater(scan_data["total_words"], 100)

            manifest_path = ws / "chunk-manifest.csv"
            with manifest_path.open("r", encoding="utf-8", newline="") as f:
                manifest_rows = list(csv.DictReader(f))
                fieldnames = list(manifest_rows[0].keys())

            translations = [
                (
                    "# Chương 1: Cánh Cổng Màn Tro\n\n"
                    "Màn sương đêm lặng lẽ bao trùm toàn bộ cổ thành, chiếc chuông đồng trên tháp ngân lên trầm đục giữa gió lạnh, những ngọn đèn góc phố lần lượt vụt tắt trong bóng tối mịt mù.\n\n"
                    "Lâm Mặc đứng ở cuối bậc đá, lặng nhìn cánh cửa sắt phủ bụi trăm năm trước mặt, trong lòng đã sớm hiểu rằng chuyến đi này tuyệt đối không còn đường quay lui nữa."
                ),
                (
                    "# Chương 2: Ngọn Tháp Cô Độc Trong Sương\n\n"
                    "Cầu thang đá xoắn ốc vươn lên cao mãi, lớp rêu ẩm ướt gần như phủ kín từng bậc thềm lạnh lẽo, từ phía xa vọng lại những âm thanh trầm thấp vang dội không dứt.\n\n"
                    "Khi anh cuối cùng cũng đẩy mở cánh cửa gỗ trên đỉnh tháp, bức tinh đồ đang lơ lửng giữa không trung chậm rãi xoay tròn, phản chiếu ánh sáng xuống cả thung lũng đang say giấc."
                ),
            ]
            for row, content in zip(manifest_rows, translations):
                out_file = ws / row["output_path"]
                out_file.parent.mkdir(parents=True, exist_ok=True)
                out_file.write_text(content + "\n", encoding="utf-8")
                row["status"] = "done"
                row["qa_status"] = "passed"

            with manifest_path.open("w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
                writer.writeheader()
                writer.writerows(manifest_rows)

            verify_res = run_command(
                PYTHON, BOOK_OPS, "verify",
                "--workspace", ws,
                "--strict",
                "--json",
            )
            self.assertTrue(json.loads(verify_res.stdout)["passed"])

            merged_out = ws / "merged-zh-vi.md"
            merge_res = run_command(
                PYTHON, BOOK_OPS, "merge",
                "--workspace", ws,
                "--out", merged_out,
                "--json",
            )
            merge_data = json.loads(merge_res.stdout)
            self.assertTrue(merge_data["merged"])
            self.assertEqual(merge_data["chunks_merged"], 2)

    def test_book_ops_pdf_to_epub_and_txt_pipeline(self):
        def _build_minimal_pdf(pages_lines):
            def _pdf_esc(s):
                return s.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")

            objects = []
            # 1: Catalog, 2: Pages, 3: Font, then pairs of (Page, ContentStream)
            page_ids = []
            next_id = 4
            for _ in pages_lines:
                page_ids.append(next_id)
                next_id += 2

            objects.append(b"<< /Type /Catalog /Pages 2 0 R >>")
            kids = " ".join(f"{pid} 0 R" for pid in page_ids).encode("ascii")
            objects.append(b"<< /Type /Pages /Kids [ " + kids + f" ] /Count {len(page_ids)} >>".encode("ascii"))
            objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")

            for idx, lines in enumerate(pages_lines):
                p_id = page_ids[idx]
                c_id = p_id + 1
                objects.append(
                    f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
                    f"/Resources << /Font << /F1 3 0 R >> >> /Contents {c_id} 0 R >>".encode("ascii")
                )
                stream_cmds = ["BT", "/F1 12 Tf", "72 720 Td", "16 TL"]
                for ln in lines:
                    stream_cmds.append(f"({_pdf_esc(ln)}) Tj T*")
                stream_cmds.append("ET")
                stream_bytes = "\n".join(stream_cmds).encode("latin-1")
                objects.append(
                    f"<< /Length {len(stream_bytes)} >>\nstream\n".encode("ascii")
                    + stream_bytes
                    + b"\nendstream"
                )

            out = bytearray(b"%PDF-1.4\n")
            offsets = [0]
            for obj_num, body in enumerate(objects, 1):
                offsets.append(len(out))
                out.extend(f"{obj_num} 0 obj\n".encode("ascii"))
                out.extend(body)
                out.extend(b"\nendobj\n")
            xref_pos = len(out)
            out.extend(f"xref\n0 {len(objects) + 1}\n0000000000 65535 f \n".encode("ascii"))
            for off in offsets[1:]:
                out.extend(f"{off:010d} 00000 n \n".encode("ascii"))
            out.extend(
                f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref_pos}\n%%EOF\n".encode("ascii")
            )
            return bytes(out)

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            pdf_file = tmp_path / "chronicles.pdf"
            pdf_bytes = _build_minimal_pdf([
                [
                    "Chronicles Running Header",
                    "Chapter 1: Dawn Over the Harbor",
                    "The harbor lantern flickered against the pale mist while sailors secured",
                    "the heavy oak ropes along the pier before sunrise.",
                    "A lone messenger climbed the stone steps carrying a sealed letter.",
                    "1",
                ],
                [
                    "Chronicles Running Header",
                    "Chapter 2: The Glass Observatory",
                    "High above the old rooftops stood a dome of green glass built to chart",
                    "winter storms and passing comets across the northern sky.",
                    "Inside the hall, brass instruments hummed beside open star ledgers.",
                    "2",
                ],
                [
                    "Chronicles Running Header",
                    "Closing notes for the second chapter continue with clear records",
                    "preserved inside the archive vault for future navigators.",
                    "3",
                ],
            ])
            pdf_file.write_bytes(pdf_bytes)

            # 1. Standalone convert subcommand -> writes both .txt and .epub
            conv_dir = tmp_path / "converted_standalone"
            conv_res = run_command(
                PYTHON, BOOK_OPS, "convert",
                "--source", pdf_file,
                "--out-dir", conv_dir,
                "--title", "Chronicles",
                "--author", "Test Author",
                "--lang", "en",
                "--json",
            )
            conv_data = json.loads(conv_res.stdout)
            self.assertEqual(conv_data["sections"], 2)
            self.assertTrue((conv_dir / "chronicles.txt").is_file())
            self.assertTrue((conv_dir / "chronicles.epub").is_file())

            # 2. init + scan directly on the .pdf
            ws = tmp_path / "pdf-ws"
            run_command(
                PYTHON, BOOK_OPS, "init",
                "--source", pdf_file,
                "--source-lang", "English",
                "--target-lang", "vi",
                "--workspace", ws,
            )
            brief_txt = (ws / "translation-brief.md").read_text(encoding="utf-8")
            self.assertIn("- Output format: txt, epub", brief_txt)

            scan_res = run_command(
                PYTHON, BOOK_OPS, "scan",
                "--source", pdf_file,
                "--workspace", ws,
                "--json",
            )
            scan_data = json.loads(scan_res.stdout)
            self.assertEqual(scan_data["total_chunks"], 2)
            self.assertEqual(len(scan_data["converted_sources"]), 1)
            self.assertTrue((ws / "converted_source" / "chronicles.txt").is_file())
            self.assertTrue((ws / "converted_source" / "chronicles.epub").is_file())

            # 3. Populate translated chunks, verify, and merge into BOTH .txt and .epub
            manifest_path = ws / "chunk-manifest.csv"
            with manifest_path.open("r", encoding="utf-8", newline="") as f:
                manifest_rows = list(csv.DictReader(f))
                fieldnames = list(manifest_rows[0].keys())

            vi_chapters = [
                (
                    "# Chương 1: Bình Minh Trên Bến Cảng\n\n"
                    "Ngọn đèn hải đăng nơi bến cảng chập chờn trong màn sương nhạt trong lúc những thủy thủ buộc chặt "
                    "các sợi dây thừng gỗ sồi nặng trĩu dọc theo cầu tàu trước lúc rạng đông.\n\n"
                    "Một người đưa tin đơn độc bước lên những bậc đá cao và mang theo một bức thư niêm phong **quan trọng**."
                ),
                (
                    "# Chương 2: Đài Thiên Văn Bằng Kính\n\n"
                    "Trên cao phía trên những mái nhà cổ kính sừng sững một mái vòm bằng kính xanh được xây dựng để vẽ bản đồ "
                    "những cơn bão mùa đông và các sao chổi đi ngang qua bầu trời phương bắc.\n\n"
                    "Bên trong sảnh lớn, những thiết bị bằng đồng ngân vang bên cạnh các cuốn sổ tinh đồ đang mở rộng, "
                    "ghi chép rõ ràng cho những nhà hàng hải tương lai trong kho lưu trữ cổ xưa."
                ),
            ]
            for row, content in zip(manifest_rows, vi_chapters):
                out_file = ws / row["output_path"]
                out_file.parent.mkdir(parents=True, exist_ok=True)
                out_file.write_text(content + "\n", encoding="utf-8")
                row["status"] = "done"
                row["qa_status"] = "passed"

            with manifest_path.open("w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
                writer.writeheader()
                writer.writerows(manifest_rows)

            verify_res = run_command(
                PYTHON, BOOK_OPS, "verify",
                "--workspace", ws,
                "--strict",
                "--json",
            )
            self.assertTrue(json.loads(verify_res.stdout)["passed"])

            out_stem = ws / "translated_chronicles.epub"
            merge_res = run_command(
                PYTHON, BOOK_OPS, "merge",
                "--workspace", ws,
                "--out", out_stem,
                "--format", "both",
                "--title", "Biên Niên Sử",
                "--author", "Tác Giả",
                "--json",
            )
            merge_data = json.loads(merge_res.stdout)
            self.assertTrue(merge_data["merged"])
            self.assertEqual(merge_data["chunks_merged"], 2)

            txt_out = ws / "translated_chronicles.txt"
            epub_out = ws / "translated_chronicles.epub"
            self.assertTrue(txt_out.is_file())
            self.assertTrue(epub_out.is_file())

            txt_content = txt_out.read_text(encoding="utf-8")
            self.assertIn("Chương 1: Bình Minh Trên Bến Cảng", txt_content)
            self.assertIn("quan trọng", txt_content)
            self.assertNotIn("**quan trọng**", txt_content)
            self.assertNotIn("# Chương 1", txt_content)

            # Re-scan the generated EPUB to confirm valid EPUB spine and chapter integrity
            re_ws = tmp_path / "rescan-epub"
            re_scan = run_command(
                PYTHON, BOOK_OPS, "scan",
                "--source", epub_out,
                "--workspace", re_ws,
                "--json",
            )
            re_data = json.loads(re_scan.stdout)
            self.assertEqual(re_data["total_chunks"], 2)

    def test_book_ops_epub_layout_and_design_preservation(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            src_epub = tmp_path / "styled_novel.epub"
            ws = tmp_path / "ws-epub"

            css_bytes = (
                "body { font-family: 'Crimson Pro', Georgia, serif; margin: 5%; }\n"
                ".header-box { text-align: center; border-bottom: 2px solid #8a6d3b; }\n"
                ".dropcap::first-letter { float: left; font-size: 3.2em; }\n"
                ".scene-divider { text-align: center; margin: 1.5em 0; }\n"
            ).encode("utf-8")
            svg_bytes = (
                "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"64\" height=\"16\" viewBox=\"0 0 64 16\">"
                "<path d=\"M2 8h60\" stroke=\"#8a6d3b\" stroke-width=\"2\"/></svg>\n"
            ).encode("utf-8")

            container_xml = (
                "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
                "<container version=\"1.0\" xmlns=\"urn:oasis:names:tc:opendocument:xmlns:container\">\n"
                "  <rootfiles>\n"
                "    <rootfile full-path=\"OEBPS/content.opf\" media-type=\"application/oebpf-package+xml\"/>\n"
                "  </rootfiles>\n"
                "</container>\n"
            )
            opf_xml = (
                "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
                "<package xmlns=\"http://www.idpf.org/2007/opf\" unique-identifier=\"bookid\" version=\"3.0\">\n"
                "  <metadata xmlns:dc=\"http://purl.org/dc/elements/1.1/\">\n"
                "    <dc:identifier id=\"bookid\">urn:uuid:11112222-3333-4444-5555-666677778888</dc:identifier>\n"
                "    <dc:title>The Silver Clock</dc:title>\n"
                "    <dc:language>en</dc:language>\n"
                "  </metadata>\n"
                "  <manifest>\n"
                "    <item id=\"css\" href=\"styles/custom-theme.css\" media-type=\"text/css\"/>\n"
                "    <item id=\"ornament\" href=\"images/flourish.svg\" media-type=\"image/svg+xml\"/>\n"
                "    <item id=\"nav\" href=\"nav.xhtml\" media-type=\"application/xhtml+xml\" properties=\"nav\"/>\n"
                "    <item id=\"ncx\" href=\"toc.ncx\" media-type=\"application/x-dtbncx+xml\"/>\n"
                "    <item id=\"ch1\" href=\"ch1.xhtml\" media-type=\"application/xhtml+xml\"/>\n"
                "    <item id=\"ch2\" href=\"ch2.xhtml\" media-type=\"application/xhtml+xml\"/>\n"
                "  </manifest>\n"
                "  <spine toc=\"ncx\">\n"
                "    <itemref idref=\"ch1\"/>\n"
                "    <itemref idref=\"ch2\"/>\n"
                "  </spine>\n"
                "</package>\n"
            )
            ncx_xml = (
                "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
                "<ncx xmlns=\"http://www.daisy.org/z3986/2005/ncx/\" version=\"2005-1\">\n"
                "  <head><meta name=\"dtb:uid\" content=\"urn:uuid:11112222\"/></head>\n"
                "  <docTitle><text>The Silver Clock</text></docTitle>\n"
                "  <navMap>\n"
                "    <navPoint id=\"navPoint-1\" playOrder=\"1\">\n"
                "      <navLabel><text>Chapter 1: The Silver Clock</text></navLabel>\n"
                "      <content src=\"ch1.xhtml\"/>\n"
                "    </navPoint>\n"
                "    <navPoint id=\"navPoint-2\" playOrder=\"2\">\n"
                "      <navLabel><text>Chapter 2: The Glass Harbor</text></navLabel>\n"
                "      <content src=\"ch2.xhtml\"/>\n"
                "    </navPoint>\n"
                "  </navMap>\n"
                "</ncx>\n"
            )
            nav_xhtml = (
                "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
                "<html xmlns=\"http://www.w3.org/1999/xhtml\" xmlns:epub=\"http://www.idpf.org/2007/ops\">\n"
                "<head><title>Table of Contents</title></head>\n"
                "<body>\n"
                "  <nav epub:type=\"toc\">\n"
                "    <ol>\n"
                "      <li><a href=\"ch1.xhtml\">Chapter 1: The Silver Clock</a></li>\n"
                "      <li><a href=\"ch2.xhtml\">Chapter 2: The Glass Harbor</a></li>\n"
                "    </ol>\n"
                "  </nav>\n"
                "</body>\n"
                "</html>\n"
            )
            ch1_xhtml = (
                "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
                "<html xmlns=\"http://www.w3.org/1999/xhtml\" xmlns:epub=\"http://www.idpf.org/2007/ops\">\n"
                "<head>\n"
                "  <title>Chapter 1: The Silver Clock</title>\n"
                "  <link rel=\"stylesheet\" type=\"text/css\" href=\"styles/custom-theme.css\"/>\n"
                "</head>\n"
                "<body class=\"book-body\">\n"
                "  <section class=\"chapter-wrap\" epub:type=\"chapter\">\n"
                "    <div class=\"header-box\">\n"
                "      <img src=\"images/flourish.svg\" class=\"ornament\" alt=\"\"/>\n"
                "      <h1 class=\"ch-title\"><span class=\"ch-num\">Chapter 1: The Silver Clock</span></h1>\n"
                "    </div>\n"
                "    <p class=\"dropcap\">First paragraph inside dropcap block describing the quiet brass gears of the observatory tower at midnight while snow settles along the parapet.</p>\n"
                "    <div class=\"scene-divider\"><img src=\"images/flourish.svg\" alt=\"***\"/></div>\n"
                "    <p class=\"indent-para\">Second paragraph inside indented block continuing the watchmaker inspection with careful lantern light across the stone gallery and cedar shelves.</p>\n"
                "  </section>\n"
                "</body>\n"
                "</html>\n"
            )
            ch2_xhtml = (
                "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
                "<html xmlns=\"http://www.w3.org/1999/xhtml\" xmlns:epub=\"http://www.idpf.org/2007/ops\">\n"
                "<head>\n"
                "  <title>Chapter 2: The Glass Harbor</title>\n"
                "  <link rel=\"stylesheet\" type=\"text/css\" href=\"styles/custom-theme.css\"/>\n"
                "</head>\n"
                "<body class=\"book-body\">\n"
                "  <section class=\"chapter-wrap\" epub:type=\"chapter\">\n"
                "    <h1 class=\"ch-title\">Chapter 2: The Glass Harbor</h1>\n"
                "    <p class=\"lead\">Third chapter paragraph about sails and salt wind along the northern pier before sunrise with wooden lanterns glowing through sea fog.</p>\n"
                "  </section>\n"
                "</body>\n"
                "</html>\n"
            )

            with zipfile.ZipFile(src_epub, "w") as zf:
                zf.writestr("mimetype", "application/epub+zip", compress_type=zipfile.ZIP_STORED)
                zf.writestr("META-INF/container.xml", container_xml)
                zf.writestr("OEBPS/content.opf", opf_xml)
                zf.writestr("OEBPS/toc.ncx", ncx_xml)
                zf.writestr("OEBPS/nav.xhtml", nav_xhtml)
                zf.writestr("OEBPS/styles/custom-theme.css", css_bytes)
                zf.writestr("OEBPS/images/flourish.svg", svg_bytes)
                zf.writestr("OEBPS/ch1.xhtml", ch1_xhtml)
                zf.writestr("OEBPS/ch2.xhtml", ch2_xhtml)

            run_command(
                PYTHON, BOOK_OPS, "init",
                "--source", src_epub,
                "--target-lang", "vi",
                "--workspace", ws,
                "--json",
            )
            scan_res = run_command(
                PYTHON, BOOK_OPS, "scan",
                "--source", src_epub,
                "--workspace", ws,
                "--max-words", "500",
                "--json",
            )
            scan_data = json.loads(scan_res.stdout)
            self.assertEqual(scan_data["total_chunks"], 2)
            self.assertTrue(scan_data["layout_preserving_epub"])
            self.assertTrue((ws / ".source-template.epub").is_file())

            scan_meta = json.loads((ws / ".book-scan-meta.json").read_text(encoding="utf-8"))
            self.assertEqual(scan_meta["source_epub_template"], ".source-template.epub")
            self.assertEqual(scan_meta["chunks"][0]["epub_href"], "OEBPS/ch1.xhtml")
            self.assertEqual(scan_meta["chunks"][0]["epub_block_start"], 0)
            self.assertEqual(scan_meta["chunks"][0]["epub_block_end"], 3)

            manifest_path = ws / "chunk-manifest.csv"
            with manifest_path.open("r", encoding="utf-8", newline="") as f:
                reader = csv.DictReader(f)
                fieldnames = reader.fieldnames
                manifest_rows = list(reader)

            vi_chunks = [
                (
                    "# Chương 1: Chiếc Đồng Hồ Bạc\n\n"
                    "Đoạn mở đầu có chữ hoa lớn mô tả những bánh răng bằng đồng tĩnh lặng trong tháp thiên văn lúc nửa đêm khi tuyết rơi dọc theo lan can đá.\n\n"
                    "Đoạn thứ hai thụt lề tiếp tục cuộc kiểm tra tỉ mỉ của người thợ đồng hồ dưới ánh đèn lồng dịu nhẹ qua hành lang đá và kệ gỗ tuyết tùng."
                ),
                (
                    "# Chương 2: Bến Cảng Thủy Tinh\n\n"
                    "Đoạn chương hai kể về những cánh buồm và làn gió mặn dọc bến tàu phía bắc trước bình minh với những chiếc đèn lồng gỗ tỏa sáng xuyên màn sương biển."
                ),
            ]
            for row, content in zip(manifest_rows, vi_chunks):
                out_file = ws / row["output_path"]
                out_file.parent.mkdir(parents=True, exist_ok=True)
                out_file.write_text(content + "\n", encoding="utf-8")
                row["status"] = "done"
                row["qa_status"] = "passed"

            with manifest_path.open("w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
                writer.writeheader()
                writer.writerows(manifest_rows)

            verify_res = run_command(
                PYTHON, BOOK_OPS, "verify",
                "--workspace", ws,
                "--strict",
                "--json",
            )
            self.assertTrue(json.loads(verify_res.stdout)["passed"])

            out_epub = ws / "translated_styled.epub"
            merge_res = run_command(
                PYTHON, BOOK_OPS, "merge",
                "--workspace", ws,
                "--out", out_epub,
                "--title", "Chiếc Đồng Hồ Bạc",
                "--json",
            )
            merge_data = json.loads(merge_res.stdout)
            self.assertTrue(merge_data["merged"])
            self.assertTrue(merge_data["epub_layout_preserved"])
            self.assertTrue(out_epub.is_file())

            with zipfile.ZipFile(out_epub, "r") as out_zf:
                self.assertEqual(out_zf.read("OEBPS/styles/custom-theme.css"), css_bytes)
                self.assertEqual(out_zf.read("OEBPS/images/flourish.svg"), svg_bytes)

                out_ch1 = out_zf.read("OEBPS/ch1.xhtml").decode("utf-8")
                self.assertIn('<section class="chapter-wrap" epub:type="chapter">', out_ch1)
                self.assertIn('<div class="header-box">', out_ch1)
                self.assertIn('<h1 class="ch-title"><span class="ch-num">Chương 1: Chiếc Đồng Hồ Bạc</span></h1>', out_ch1)
                self.assertIn('<p class="dropcap">', out_ch1)
                self.assertIn('<div class="scene-divider"><img src="images/flourish.svg" alt="***"/></div>', out_ch1)
                self.assertIn('<p class="indent-para">', out_ch1)
                self.assertIn("bánh răng bằng đồng tĩnh lặng", out_ch1)
                self.assertIn("người thợ đồng hồ", out_ch1)
                self.assertNotIn("The Silver Clock", out_ch1)
                self.assertNotIn("quiet brass gears", out_ch1)
                self.assertNotIn("watchmaker inspection", out_ch1)

                out_ncx = out_zf.read("OEBPS/toc.ncx").decode("utf-8")
                self.assertIn("Chương 1: Chiếc Đồng Hồ Bạc", out_ncx)
                self.assertIn("Chương 2: Bến Cảng Thủy Tinh", out_ncx)

                out_nav = out_zf.read("OEBPS/nav.xhtml").decode("utf-8")
                self.assertIn("Chương 1: Chiếc Đồng Hồ Bạc", out_nav)
                self.assertIn("Chương 2: Bến Cảng Thủy Tinh", out_nav)

                out_opf = out_zf.read("OEBPS/content.opf").decode("utf-8")
                self.assertIn("<dc:language>vi</dc:language>", out_opf)
                self.assertIn("Chiếc Đồng Hồ Bạc", out_opf)


if __name__ == "__main__":
    unittest.main()
