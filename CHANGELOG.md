# Changelog

All notable changes to this skill pack are documented here.

This project follows semantic versioning.

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
