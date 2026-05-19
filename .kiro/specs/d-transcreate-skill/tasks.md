# Implementation Plan: d-transcreate-skill

## Overview

This plan creates the complete `d-transcreate-skill` repository — an agent-agnostic skill pack delivering a strict, resumable, copyright-safe, multi-pass translation/transcreation workflow for long documents. The implementation builds on existing content already in `core/` (entrypoint, workflows, schemas, and one prompt), completes the remaining subagent prompts, creates all adapter packs with mirrored install layouts, builds three example bundles, implements two Python scripts (`scripts/validate_pack.py` and `scripts/build_adapters.py`), and produces top-level documentation. Legacy files (`SKILL.md`, `agents/openai.yaml`, `references/`) are migrated and removed at the end.

## Tasks

- [x] 1. Core library structure and entrypoint
  - [x] 1.1 Create `core/d-transcreate.md` canonical entrypoint
    - Operating principles, core workflow (7 phases), subagent role list, reference index, copyright rules
    - Keep within 200-line budget
    - _Requirements: 1.1, 2.1, 18.5, 27.1, 27.2_

  - [x] 1.2 Create `core/workflows/long-document.md`
    - Phase-by-phase staged workflow: intake, source inventory, segmenting, multi-pass translation passes A/B/C/D, merge, delivery
    - _Requirements: 2.2, 5, 6, 11, 12, 14_

  - [x] 1.3 Create `core/workflows/terminology-research.md`
    - Term mining, source priority order, `d-research` integration pattern + fallback, copyright rules for evidence quotes
    - _Requirements: 2.2, 7, 18.5, 19_

  - [x] 1.4 Create `core/workflows/fiction-continuity.md`
    - Story Bible maintenance, reveal-timing rules, character voice, terms of address
    - _Requirements: 2.2, 6.4, 9_

  - [x] 1.5 Create `core/workflows/technical-domain.md`
    - Domain Map maintenance, acronym/unit/standard handling, citation preservation
    - _Requirements: 2.2, 6.5, 10_

  - [x] 1.6 Create `core/workflows/qa-gates.md`
    - The 8 QA gates: completeness, fidelity, terminology, target-language quality, continuity, numbers, formatting, residual risk
    - _Requirements: 2.2, 15_

  - [x] 1.7 Create `core/workflows/context-management.md`
    - Context budget rule, what loads per chunk, summary unloading, resume procedure
    - _Requirements: 2.2, 16, 17_

  - [x] 1.8 Create `core/workflows/subagents.md`
    - Readiness gate, role responsibilities, prompt pattern, parallel rules, coordinator merge checklist
    - _Requirements: 2.2, 13, 14, 25_

- [x] 2. Create artifact schemas
  - [x] 2.1 Create `core/schemas/translation-brief.md`
    - Required fields: source files, source language, target language, target locale, audience, mode, register, output format, formatting constraints, do-not-translate, terminology authority, research depth, QA bar, open questions
    - _Requirements: 2.3, 5.2, 5.5, 21.1_

  - [x] 2.2 Create `core/schemas/source-map.md`
    - Overview section, structure table, high-risk items table, fiction-specific and technical-specific extensions
    - _Requirements: 2.3, 6.2, 6.3, 6.4, 6.5, 21.1_

  - [x] 2.3 Create `core/schemas/glossary.md`
    - CSV column spec + Markdown table form; columns: term, preferred_translation, forbidden_translation, term_class, context, source_location, evidence, confidence, status, notes
    - Status enum: {proposed, approved, needs-review, deprecated}; Confidence enum: {high, medium, low}
    - _Requirements: 2.3, 7.2, 7.3, 21.1, 21.2_

  - [x] 2.4 Create `core/schemas/style-sheet.md`
    - Sections: voice, language conventions, adaptation rules, forbidden patterns
    - _Requirements: 2.3, 8.2, 8.5, 21.1_

  - [x] 2.5 Create `core/schemas/story-bible.md`
    - Tables for characters, timeline events, places, continuity threads, terms of address
    - _Requirements: 2.3, 9.2, 9.6, 21.1_

  - [x] 2.6 Create `core/schemas/domain-map.md`
    - Sections: domain field, audience expertise, governing standards/laws, canonical sources, concepts, acronyms, units
    - _Requirements: 2.3, 10.2, 10.5, 21.1_

  - [x] 2.7 Create `core/schemas/chunk-manifest.md`
    - CSV column spec + Markdown table form; columns: chunk_id, source_location, word_or_page_range, semantic_unit, dependencies, assigned_to, status, output_path, qa_status, notes
    - Status enum: {planned, research-needed, ready, drafting, drafted, qa-needed, revising, done, blocked}
    - _Requirements: 2.3, 11.5, 11.6, 21.1, 21.3_

  - [x] 2.8 Create `core/schemas/chunk-summary.md`
    - Repeating Markdown blocks per chunk_id; fields: source range, what happened/main argument, terms introduced, continuity implications, unresolved issues, next-chunk dependency
    - _Requirements: 2.3, 21.1_

  - [x] 2.9 Create `core/schemas/unresolved-issues.md`
    - Markdown table with columns: id, location, issue, options, owner, status
    - _Requirements: 2.3, 21.1_

  - [x] 2.10 Create `core/schemas/qa-report.md`
    - Sections: scope, artifacts checked, checks performed, issues table, residual risks
    - _Requirements: 2.3, 15.6, 21.1_

- [x] 3. Checkpoint - Ensure core library foundations are complete
  - Verify all core workflow and schema files exist and cross-reference each other correctly; ask the user only if blocked.

- [x] 4. Create subagent prompt files
  - [x] 4.1 Create `core/prompts/transcreate-coordinator.md`
    - Define role scope, inputs, output contract, procedure, boundaries
    - Authority: final say on Glossary, Style_Sheet, voice, continuity, merge
    - _Requirements: 2.4, 13.2, 14, 20.1, 20.2_

  - [x] 4.2 Create `core/prompts/terminology-researcher.md`
    - Define role scope, inputs, output contract, procedure, boundaries
    - Authority: proposes only, never writes global Glossary directly
    - _Requirements: 2.4, 20.1, 20.3_

  - [x] 4.3 Create `core/prompts/style-researcher.md`
    - Define role scope, inputs, output contract, procedure, boundaries
    - Authority: proposes only, never writes global Style_Sheet directly
    - _Requirements: 2.4, 20.1, 20.4_

  - [x] 4.4 Create `core/prompts/chunk-translator.md`
    - Define role scope, inputs, output contract, procedure, boundaries
    - Authority: owns one chunk, proposes Glossary/Style_Sheet edits
    - _Requirements: 2.4, 12, 20.1, 20.5_

  - [x] 4.5 Create `core/prompts/continuity-reviewer.md`
    - Define role scope, inputs, output contract, procedure, boundaries
    - Authority: flags only, writes to Unresolved_Issues_Log
    - _Requirements: 2.4, 20.1, 20.6_

  - [x] 4.6 Create `core/prompts/fidelity-reviewer.md`
    - Define role scope, inputs, output contract, procedure, boundaries
    - Authority: flags only, writes to Unresolved_Issues_Log
    - _Requirements: 2.4, 20.1, 20.7_

  - [x] 4.7 Create `core/prompts/formatting-reviewer.md`
    - Define role scope, inputs, output contract, procedure, boundaries
    - Authority: flags only, writes to Unresolved_Issues_Log
    - _Requirements: 2.4, 20.1, 20.8_

- [x] 5. Checkpoint - Ensure core library is complete
  - Verify all core/ files (entrypoint, workflows, schemas, prompts) exist and cross-reference correctly; ask the user only if blocked.

- [x] 6. Create Codex adapter pack
  - [x] 6.1 Create `adapters/codex/SKILL.md`
    - Bootstrap + pointers to core, valid YAML frontmatter with `name` and `description` fields
    - Reference `core/d-transcreate.md` via relative path
    - Stay within 200-line budget
    - _Requirements: 3.1, 3.7, 3.8, 3.9_

  - [x] 6.2 Create `adapters/codex/agents/openai.yaml`
    - Include `display_name`, `short_description`, `default_prompt` fields
    - Migrate from existing `agents/openai.yaml`
    - _Requirements: 3.1_

- [x] 7. Create Claude Code adapter pack
  - [x] 7.1 Create `adapters/claude-code/CLAUDE.md`
    - Project-level bootstrap pointing to Claude skill file
    - List the seven subagent roles
    - _Requirements: 3.2_

  - [x] 7.2 Create `adapters/claude-code/.claude/skills/d-transcreate/SKILL.md`
    - Claude skill entrypoint with YAML frontmatter
    - Reference `core/d-transcreate.md` via relative path
    - Stay within 200-line budget
    - _Requirements: 3.2, 3.7, 3.8, 3.9_

  - [x] 7.3 Create Claude Code subagent files under `adapters/claude-code/.claude/agents/`
    - Create one file per role: `transcreate-coordinator.md`, `terminology-researcher.md`, `style-researcher.md`, `chunk-translator.md`, `continuity-reviewer.md`, `fidelity-reviewer.md`, `formatting-reviewer.md`
    - Each wraps `core/prompts/<role>.md` with Claude-specific metadata
    - _Requirements: 3.2, 20_

- [x] 8. Create Cursor adapter pack
  - [x] 8.1 Create `adapters/cursor/AGENTS.md`
    - Root-level bootstrap in English
    - Reference core library files
    - _Requirements: 3.3_

  - [x] 8.2 Create `adapters/cursor/.cursor/rules/d-transcreate.mdc`
    - Configure as Agent-Requested or Manual rule type (never `alwaysApply: true`)
    - Include `description` and `globs` fields
    - Point agent to `core/prompts/transcreate-coordinator.md` for coordinator behavior
    - Reference `core/d-transcreate.md`
    - _Requirements: 3.3, 3.6_

- [x] 9. Create OpenCode adapter pack
  - [x] 9.1 Create `adapters/opencode/AGENTS.md`
    - Project-level bootstrap in English
    - _Requirements: 3.4_

  - [x] 9.2 Create `adapters/opencode/opencode.json`
    - Reference `core/d-transcreate.md` via `instructions` field
    - _Requirements: 3.4_

  - [x] 9.3 Create OpenCode subagent files under `adapters/opencode/.opencode/agents/`
    - Create one file per role mirroring `core/prompts/<role>.md` with platform-specific frontmatter
    - _Requirements: 3.4, 20_

- [x] 10. Create Generic adapter pack
  - [x] 10.1 Create `adapters/generic/AGENTS.md`
    - Plain bootstrap, no tool-specific syntax
    - _Requirements: 3.5_

  - [x] 10.2 Create `adapters/generic/d-transcreate.md`
    - Plain pointer to `core/d-transcreate.md` and the seven role prompts
    - No frontmatter, no special directives
    - _Requirements: 3.5_

- [x] 11. Checkpoint - Ensure all adapters are complete
  - Verify all 5 adapter packs are created with correct mirrored layouts and reference core/ files; ask the user only if blocked.

- [x] 12. Create example bundles
  - [x] 12.1 Create `examples/fiction-short/` example bundle
    - Create `README.md`, `source/` with 2-3 short original fiction scenes, `seed-artifacts/translation-brief.md`, `seed-artifacts/glossary.csv` (5-15 entries), `seed-artifacts/style-sheet.md` (5-10 rules)
    - _Requirements: 1.3, 23.1, 23.4, 23.5, 23.6, 24.4_

  - [x] 12.2 Create `examples/technical-manual/` example bundle
    - Create `README.md`, `source/` with 2-3 sections of a tooling manual, `seed-artifacts/translation-brief.md`, `seed-artifacts/glossary.csv` (5-15 entries), `seed-artifacts/style-sheet.md` (5-10 rules)
    - _Requirements: 1.3, 23.2, 23.4, 23.5, 23.6, 24.4_

  - [x] 12.3 Create `examples/legal-policy/` example bundle
    - Create `README.md`, `source/` with one short policy excerpt, `seed-artifacts/translation-brief.md`, `seed-artifacts/glossary.csv` (5-15 entries), `seed-artifacts/style-sheet.md` (5-10 rules)
    - _Requirements: 1.3, 23.3, 23.4, 23.5, 23.6, 24.4_

- [x] 13. Implement `scripts/validate_pack.py` (Validation Script)
  - [x] 13.1 Create `scripts/validate_pack.py` Python script
    - CLI: `[PATH]` (defaults to repo root), `--line-budget N` (default 200), `--duplication-threshold N` (default 20), `--json`
    - Checks: C1 required files, C2 frontmatter YAML, C3 internal link resolution, C4 no TODO/TBD/FIXME, C5 adapter references core, C6 line budget, C7 duplication warning, C8 UTF-8 + non-ASCII warning, C9 schema existence, C10 example README, C11 install manifest at destination
    - Python 3.8+ standard library only; exit non-zero on error; warnings do not fail
    - _Requirements: 1.4, 4.4, 21.5, 22.1, 22.2, 22.3, 22.4, 22.5, 22.6, 22.7, 23.5_

  - [ ]* 13.2 Write unit tests for `scripts/validate_pack.py`
    - Test each check (C1-C11) with passing and failing fixtures
    - Test CLI argument parsing and exit code behavior
    - _Requirements: 22_

- [x] 14. Implement `scripts/build_adapters.py` (Adapter Build Script)
  - [x] 14.1 Create `scripts/build_adapters.py` Python script
    - CLI: `--platform <codex|claude-code|cursor|opencode|generic>`, `--dest <path>`, `--mode <copy|symlink|dry-run>`, `--core-strategy <copy|reference>`, `--shared-core-path <path>`, `--force`
    - Implement copy, symlink, dry-run modes; core-strategy copy/reference; conflict detection; manifest generation (`.d-transcreate-manifest.json`)
    - Python 3.8+ standard library only
    - _Requirements: 1.4, 29.1, 29.2, 29.3, 29.4, 29.5, 29.6, 29.7_

  - [ ]* 14.2 Write unit tests for `scripts/build_adapters.py`
    - Test each mode, core-strategy options, conflict detection, manifest schema
    - _Requirements: 29_

- [x] 15. Smoke-test the scripts
  - [x] 15.1 Run `python scripts/validate_pack.py .` against the repo root
    - Confirm exit code 0 and no errors
    - _Requirements: 22.1, 22.7_

  - [x] 15.2 Run `python scripts/build_adapters.py --platform codex --dest <temp-dir> --mode dry-run`
    - Confirm script prints planned operations without writing files
    - _Requirements: 29.2_

  - [x] 15.3 Build each platform adapter into a temporary destination using copy mode
    - Run for each platform: codex, claude-code, cursor, opencode, generic
    - Confirm each completes with exit code 0 and produces `.d-transcreate-manifest.json`
    - _Requirements: 29.1, 29.2, 29.7_

  - [x] 15.4 Validate each built destination with `python scripts/validate_pack.py <temp-dir>/<platform>`
    - Confirm exit code 0 for each
    - _Requirements: 22.1, 29.8_

  - [x] 15.5 Test conflict detection: re-run install without `--force` and expect non-zero exit
    - _Requirements: 29.5_

- [x] 16. Checkpoint - Ensure scripts and smoke tests pass
  - Ensure validation passes, all adapter builds succeed, and conflict detection works; ask the user only if blocked.

- [x] 17. Create top-level documentation
  - [x] 17.1 Create top-level `README.md`
    - English section first, then Vietnamese section
    - Project overview, repository layout, quick start, maintainer update workflow
    - Document validation and build commands
    - _Requirements: 1.5, 4.3, 28.4_

  - [x] 17.2 Create top-level `AGENTS.md`
    - Generic-agent bootstrap at top level
    - Point to core library and explain how to find platform-specific adapters
    - _Requirements: 1.5_

- [x] 18. Migration cleanup and final wiring
  - [x] 18.1 Verify migrated content coverage before removal
    - Confirm root `SKILL.md` content is in `core/d-transcreate.md` and `adapters/codex/SKILL.md`
    - Confirm `agents/openai.yaml` content is in `adapters/codex/agents/openai.yaml`
    - Confirm `references/` content is migrated to `core/workflows/` and `core/schemas/`
    - Run `python scripts/validate_pack.py .` and confirm pass
    - _Requirements: 1, 2, 3.1, 20, 21_

  - [x] 18.2 Remove or archive legacy files (only after 18.1 passes)
    - Remove root `SKILL.md`, `agents/openai.yaml`, `references/` directory
    - If unsure, move to `_archive/` instead of deleting
    - _Requirements: 1, 2, 3.1, 20, 21_

- [x] 19. Final integration validation
  - [x] 19.1 Validate repo root with `python scripts/validate_pack.py .`
    - Confirm exit code 0, no errors, review warnings
    - _Requirements: 22.1, 22.7_

  - [x] 19.2 Build all adapters into temporary destinations and validate each
    - For each platform: build with copy mode + core-strategy copy, then validate
    - _Requirements: 29.1, 29.8_

  - [x] 19.3 Confirm no adapter entrypoint exceeds the line budget (≤ 200 lines)
    - _Requirements: 2.6, 22.6_

  - [x] 19.4 Confirm every adapter references `core/`
    - _Requirements: 2.5, 22.6_

  - [x] 19.5 Confirm examples contain required artifacts
    - Each: `README.md`, source files, seed artifacts (translation-brief.md, glossary.csv, style-sheet.md)
    - _Requirements: 23.4, 23.5, 23.6, 24.4_

- [x] 20. Final checkpoint - Ensure all validations pass
  - Run `python scripts/validate_pack.py .` and ensure no errors
  - Ensure all internal links resolve, all required files exist, all adapters reference core
  - Ensure smoke tests from task 15 still pass after migration cleanup

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- The implementation language for scripts is **Python** (single-file, standard library only — Python 3.8+ stdlib)
- All documentation content (core/, adapters/, examples/) is written in Markdown
- Core library content is written in English (Req 4.1, 4.2)
- The top-level README.md is bilingual: English then Vietnamese (Req 4.3)
- Legacy files (root `SKILL.md`, `agents/openai.yaml`, `references/`) are NOT deleted until migrated content exists AND `python scripts/validate_pack.py .` passes
- Smoke tests (task 15) are REQUIRED, not optional. Full unit tests (13.2, 14.2) are optional.
- Tasks 1.x and 2.x are marked complete because the files already exist in the workspace

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["4.1", "4.3", "4.4", "4.5", "4.6", "4.7"] },
    { "id": 1, "tasks": ["6.1", "6.2", "7.1", "7.2", "7.3", "8.1", "8.2", "9.1", "9.2", "9.3", "10.1", "10.2"] },
    { "id": 2, "tasks": ["12.1", "12.2", "12.3"] },
    { "id": 3, "tasks": ["13.1", "14.1"] },
    { "id": 4, "tasks": ["13.2", "14.2"] },
    { "id": 5, "tasks": ["15.1", "15.2"] },
    { "id": 6, "tasks": ["15.3"] },
    { "id": 7, "tasks": ["15.4", "15.5"] },
    { "id": 8, "tasks": ["17.1", "17.2"] },
    { "id": 9, "tasks": ["18.1"] },
    { "id": 10, "tasks": ["18.2"] },
    { "id": 11, "tasks": ["19.1", "19.2", "19.3", "19.4", "19.5"] }
  ]
}
```
