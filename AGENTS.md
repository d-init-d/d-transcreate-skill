# D Transcreate Skill

This repository is a portable translation and transcreation skill package for AI agents. Use it for books, manuals, legal or policy texts, fiction, scripts, subtitles, technical documentation, or any substantial source material that needs controlled terminology, preserved structure, context-safe chunking, durable artifacts, and audit-ready QA.

## Portable Entry Point

Start at the root `SKILL.md` in any runtime that supports skills. If the host loads instruction files instead, this `AGENTS.md` provides the same portable bootstrap and points to the canonical workflow in `core/d-transcreate.md`.

Platform adapters under `adapters/` are optional compatibility layers for host-native discovery. They do not change the workflow or artifact contract.

## Core Workflow

1. Read `core/d-transcreate.md` for operating principles and the eight-phase workflow.
2. Follow the phase sequence: Intake → Scan → Research → Plan → Translate → Merge → QA → Delivery.
3. Persist all decisions as workspace artifacts on disk, not in chat history.
4. If subagents are available, dispatch scoped roles through `Subagent_Dispatch_Plan`, starting every worker prompt with the Worker Contract Card from `core/workflows/subagents.md`.
5. If subagents are unavailable, run the same role contract sequentially; the artifacts remain mandatory for resume and auditability.

## Core Library

The single source of truth lives under `core/`:

- `core/d-transcreate.md` — canonical entrypoint with operating principles and workflow overview.
- `core/workflows/long-document.md` — phase-by-phase staged workflow (including Zero-Config Book Mode via `scripts/book_ops.py`).
- `core/workflows/d-research-module.md` — modular Phase 3 research engine producing `Research_Dossier` (Track A prior-translation term harvesting and Track B authorial intent / transcreation mindset formation).
- `core/workflows/terminology-research.md` — term mining, source priority, evidence rules.
- `core/workflows/fiction-continuity.md` — Story_Bible, reveal timing, character voice.
- `core/workflows/technical-domain.md` — Domain_Map, acronyms, units, standards.
- `core/workflows/context-management.md` — context budget, chunk loading, resume procedure.
- `core/workflows/subagents.md` — readiness gate, runtime auto-detection, live `glossary-inbox.jsonl` sync, Peer Cross-Check, sequential fallback.
- `core/workflows/qa-gates.md` — the eight mandatory QA gates.
- `core/locales/vi-VN.md` — Vietnamese localization and book transcreation profile.
- `core/schemas/` — artifact contracts and templates (including `core/schemas/research-dossier.md`).
- `core/prompts/` — runtime-neutral role prompts.

## Shared Memory & Book CLI

- `memory/glossary-vi.csv` — persistent Tier-1 cross-book Vietnamese translation memory (`memory/README.md`).
- `scripts/book_ops.py` — deterministic book pipeline CLI (`init`, `convert`, `scan`, `sync-glossary`, `verify`, `merge`) for `.pdf` -> `.txt`/`.epub` conversion, Zero-Config Book Mode, `.txt`/`.epub` output generation, and 100% chapter coverage verification.

## Required Artifacts

Create or maintain these files during a substantial translation run:

- Translation_Brief and Source_Map
- Research_Dossier (`research-dossier.md`)
- Glossary (`glossary.csv` + `glossary-inbox.jsonl`) and Style_Sheet
- Story_Bible for narrative work, or Domain_Map for technical/legal/domain-heavy work
- Context_Plan before final chunking
- Chunk_Manifest as the authoritative status ledger
- Subagent_Dispatch_Plan before delegation, or before simulating delegation sequentially
- Chunk_Summary entries and Unresolved_Issues_Log
- QA_Report before delivery

## Optional Host Adapters

Use adapters only when the host benefits from native files:

| Platform | Adapter location | Entrypoint |
|----------|------------------|------------|
| Portable | root | `SKILL.md` |
| Antigravity | `adapters/antigravity/` | `SKILL.md` + `AGENTS.md` |
| Claude Code | `adapters/claude-code/` | `.claude/skills/d-transcreate/SKILL.md` |
| OpenCode | `adapters/opencode/` | `AGENTS.md` + `opencode.json` |
| Cursor | `adapters/cursor/` | `.cursor/rules/d-transcreate.mdc` |
| Codex | `adapters/codex/` | `SKILL.md` |
| Generic | `adapters/generic/` | `AGENTS.md` + `d-transcreate.md` |

Install a portable or host-native layout with:

```bash
python scripts/build_adapters.py --platform <portable|antigravity|claude-code|opencode|cursor|codex|generic> --dest <path>
```

## Subagent Roles

The skill defines seven fixed roles: Transcreate Coordinator, Terminology Researcher, Style Researcher, Chunk Translator, Continuity Reviewer, Fidelity Reviewer, and Formatting Reviewer. Workers propose; only the Coordinator approves and writes shared artifacts. The authoritative role table (authority, scope, and returns per role) lives in `core/workflows/subagents.md`.

For full details, read `core/d-transcreate.md` and the referenced workflow files on demand.
