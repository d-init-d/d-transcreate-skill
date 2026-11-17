# Changelog

All notable changes to this skill pack are documented here.

This project follows semantic versioning.

## 1.1.0 — 2026-11-17

Reliability, intelligence, and QA depth release: eliminates EPUB DOM layout drift on paragraph splits, upgrades PDF header/footnote extraction, adds whole-book entity mining and zero-overhead worker packet bundling, guards cross-book translation memory against domain pollution, and authenticates the Vietnamese publishing profile.

### Added

- **Anchor-Locked EPUB DOM & Inline Asset Engine** (`scripts/book_ops.py`): `scan` now tags EPUB leaf blocks with `<!-- @bN -->` block anchors while preserving inline footnotes/cross-references (`<a href>` + `<sup>`) and mid-block images as Markdown inline links and image spans. During `merge`, translated blocks lock deterministically to their original XHTML containers—preventing Vietnamese dialogue splits (`—`) or paragraph merges from shifting downstream CSS classes, headings, or `<td>`/`<th>` table cells—while cloning unique attributes without duplicate XML `id`s.
- **Whole-Book Term & Entity Mining (`book_ops.py mine-terms`)**: Automatically executed during `scan` (and runnable standalone) across all `source_chunks/*.md` to surface recurring proper nouns, capitalized phrases, acronyms, CJK bracketed names, and italicized terms across the entire book into `candidate-terms.json` and `source-map.md`.
- **Scoped Worker Packet Bundler (`book_ops.py bundle-chunk`)**: Generates self-contained per-chunk prompt packets under `packets/<chunk_id>-<role>.md` pre-loaded with the `WORKER CONTRACT CARD`, filtered `glossary.csv` + `glossary-inbox.jsonl` slices, filtered `Story_Bible` / `Domain_Map` rows, adjacent `Chunk_Summary` entries, and `Style_Sheet`.
- **Golden Voice Calibration Sample** (`templates/style-sheet.md`, `core/schemas/style-sheet.md`): Locks a vetted 300–500 word anchor sample in `style-sheet.md` before parallel Phase 5 dispatch.
- **Bidirectional 37-Column `d-research` v3.3 Ledger Bridge & Domain-Safe Memory Controls** (`scripts/book_ops.py`, `memory/README.md`): Initializes and synchronizes `evidence-ledger.jsonl` alongside 37-column `evidence-ledger.csv`; adds `--domain`, `--filter-to-source`, `--approve-clean`, and automatic proper-noun `--promote` guards (`--include-proper-nouns` override).
- **Deep Deterministic QA Checks & Validator Check C24** (`scripts/book_ops.py verify`, `scripts/validate_pack.py`): Adds `--require-dossier`, `--enforce-glossary`, language-pair-calibrated word-ratio defaults, URL/number formal-data parity checks, untranslated CJK script-leakage detection, Vietnamese dialogue/calque linting (`locale-vi`), retroactive cross-chunk glossary drift warnings, and `check_c24_locale_profiles`.
- **Six new end-to-end integration tests** in `tests/test_pack.py` (39 tests total).

### Changed

- **Sliding-Window Phase 6 Voice Pass** (`core/d-transcreate.md`, `core/workflows/long-document.md`, `core/prompts/transcreate-coordinator.md`): Replaced single-turn monolithic post-merge regeneration on large books with a centralized Sliding-Window Voice & Seam Pass directly on `output/<chunk_id>.md` before final `verify` and `merge`, preventing output truncation and keeping `.txt`, `.md`, and `.epub` synchronized.
- **PDF Ingestion Engine** (`scripts/book_ops.py`): Added normalized digit-masked detection for alternating recto/verso and per-chapter running headers/footers plus page-bottom footnote detachment so cross-page sentences reflow cleanly.
- **Authentic Accented Vietnamese Locale Profile** (`core/locales/vi-VN.md`, `scripts/validate_pack.py`): Restored full Vietnamese diacritics and concrete before/after anti-translatorese remedies; exempted `core/locales/` from C8 non-ASCII warnings while enforcing UTF-8 authenticity via C24.
- Updated `VERSION`, `pyproject.toml`, `core/`, `schemas/`, `templates/`, `adapters/`, and `examples/` to `1.1.0`.

### Fixed

- Fixed positional XHTML DOM drift when translators split one EPUB paragraph into multiple dialogue lines or merge paragraphs before subheadings.
- Fixed loss of inline `<a epub:type="noteref"><sup>...</sup></a>` footnote references and table cell deletion during EPUB DOM reconstruction.
- Fixed `pyproject.toml` lagging at `0.5.0` and out-of-domain fantasy/technical term cross-pollution in Tier-1 memory seeding/promotion.

## 1.0.0 — 2026-11-13

Production release: book-scale automation, layout-preserving EPUB rebuild, modular pre-translation research, and persistent cross-book translation memory.

### Added

- **Modular `d-research` integration** (`core/workflows/d-research-module.md`, `core/schemas/research-dossier.md`, `templates/research-dossier.md`): 3-tier module discovery with internal fallback producing `Research_Dossier` (`research-dossier.md`) via Track A (prior-translation term harvesting & pitfall audit) and Track B (context, authorial intent, register ladder, and transcreation mindset compass formation).
- **Two-tier persistent shared glossary** (`memory/glossary-vi.csv`, `memory/README.md`) and Vietnamese book localization profile (`core/locales/vi-VN.md`).
- **Live Sub-Agent glossary sync & Peer Cross-Check** (`core/workflows/subagents.md`): runtime capability auto-detection (Native Swarm, Subagent Spawner, Sequential fallback), `glossary-inbox.jsonl` wave synchronization, and mandatory independent cross-review before marking chunks `done`.
- **Deterministic book pipeline CLI** (`scripts/book_ops.py`): `init`, `convert`, `scan`, `sync-glossary`, `verify`, and `merge` subcommands supporting `.pdf` -> clean `.txt`/`.epub` conversion, Layout-Preserving EPUB Mode (`.epub` input -> `.epub` output keeps all original CSS, fonts, images, cover art, and XHTML DOM layout/classes intact), 100% chapter coverage, anti-summarization/anti-truncation parity, glossary compliance, and `.txt`/`.epub`/`.md` merged book output.
- **Antigravity adapter** (`adapters/antigravity/SKILL.md`, `adapters/antigravity/AGENTS.md`), `--with-d-research` build option in `scripts/build_adapters.py`, and validator checks **C21–C23** in `scripts/validate_pack.py`.

### Changed

- `scripts/build_adapters.py` now installs `memory/`, `templates/`, and `scripts/book_ops.py` into all adapter and portable destinations so every installed workspace has the shared glossary and book CLI ready to run.
- Example seed artifacts updated to `skill_version: 1.0.0`.

## 0.5.0 — 2026-07-27

Agent-compliance release: one canon, one writer, one path form. Fixes the
failure modes observed on long-book runs, where workers drifted from the spec
or never received it at all.

### Fixed

- **Installed adapters lost their role prompts.** The build script rewrote
  `core/...` references into depth-based parent-relative paths, but agent
  runtimes resolve paths from the project root — so dispatched workers ran on
  a ~170-word wrapper stub instead of their full role prompt. All references
  are now normalized to root-relative `core/...` at build time, the Claude
  skill entrypoint link is root-relative, and every wrapper now instructs the
  worker to STOP with `blocked: missing-role-prompt` if the prompt cannot be
  read.
- **Two competing phase numberings.** The entrypoint and the long-document
  workflow disagreed (the latter had no Research phase and shifted every
  number after Phase 2). Both now follow one canonical eight-phase workflow:
  Intake → Scan → Research → Plan → Translate → Merge → QA → Delivery. All
  schemas, prompts, examples, and adapters reference the same numbers.
- **Four conflicting rules about who writes the Unresolved_Issues_Log.**
  Canon now: workers return `unresolved_items` in structured output; the
  Coordinator is the log's only writer (in sequential mode the main agent
  acting as Coordinator). This also removes a parallel-write conflict between
  concurrent reviewers.
- **Split severity scales.** The formatting reviewer used high/medium/low
  while every other reviewer and the QA_Report used critical/major/minor.
  One scale now: critical / major / minor.
- **Contradictory resume order.** Canonical order: Chunk_Manifest first
  (status truth), then Context_Plan (constraints), then brief/style/glossary
  slices — stated identically in context-management, context-plan, and the
  adapters.
- **Context budget example summed to 105%** directly under the "must not
  exceed 100%" rule. Policy and every example now sum to exactly 100%.
- **Researcher-dispatch deadlock.** The readiness gate required a Glossary
  before dispatching any worker — but the Glossary is the researcher's
  output. The gate is now two-tier: a light research-tier gate (Phase 3) and
  the full eight-artifact gate for translation and review dispatch.

### Added

- **Worker Contract Card** (`core/workflows/subagents.md`): a compact card
  the Coordinator pastes verbatim at the top of every worker prompt,
  re-anchoring the binding rules (role fidelity, propose-don't-write,
  never-guess, formal-data preservation, reveal timing, severity scale,
  context-pressure honesty) at every dispatch instead of once per session.
- Validator checks: **C18** rejects parent-escaping `../core/` references in
  distributed instruction files; **C19** enforces the canonical eight-phase
  numbering in both canon files; **C20** requires the Worker Contract Card
  and its use by the Coordinator prompt.
- Release automation: pushing a `v*` tag now validates, tests, builds all
  adapters, and publishes a GitHub release with the curated notes.

### Changed

- Deduplicated instruction text so each rule has one canonical home: role
  authority table and readiness gates live in `core/workflows/subagents.md`;
  chunk-size presets in `core/schemas/context-plan.md`; resize triggers and
  per-chunk loading rules in `core/workflows/context-management.md`. Other
  files point instead of repeating.
- Adapter entrypoints trimmed to pointers; example seed artifacts and schema
  examples updated to `skill_version: 0.5.0` and 100% budget allocations.

## 0.4.0 — 2026-05-30

- Add portable root `SKILL.md` entrypoint so the repo works as a portable skill without choosing a host adapter.
- Make host adapters optional compatibility layers and keep `core/` runtime-neutral.
- Add Claude Code and OpenCode subagent frontmatter, and fix the OpenCode `opencode.json` config shape.
- Add a portable install target, atomic staging, and a validate-after-build option to the build script.
- Expand validator coverage: root skill and agent frontmatter, OpenCode config shape, example artifacts, template headers, version consistency, distribution hygiene, and internal requirement references (with a `--release` gate).
- Add blank artifact templates under `templates/`, CI workflow, and release packaging metadata.
- Remove internal requirement references from distributed core docs.

## 0.3.0 — 2026-05-19

- Add context-aware orchestration with `Context_Plan` and `Subagent_Dispatch_Plan` schemas.
- Require context planning before final chunking and dispatch planning before worker delegation.
- Strengthen coordinator/subagent responsibilities, context slicing, overflow fallback, and sequential fallback rules.
- Add example orchestration artifacts and validator/test coverage for the orchestration contract.
- Polish README, AGENTS, and adapter docs to keep release documentation aligned with the new workflow.

## 0.2.0 — 2026-05-19

- Change licensing from MIT to PolyForm Noncommercial 1.0.0 so the pack can be
  used, changed, and redistributed for noncommercial purposes only.
- Rewrite the README into a product-ready guide with clearer positioning,
  supported platforms, installation, validation, operational workflow, and
  licensing guidance.
- Clarify that this repository is a source distribution pack: users install one
  target adapter, while all platforms share the canonical workflow in `core/`.

## 0.1.0 — 2026-05-19

- Initial public skill pack with canonical core workflow, cross-platform adapters,
  artifact schemas, role prompts, examples, and validation/build tooling.
