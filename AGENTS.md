# D Transcreate Skill

This repository is a portable translation and transcreation skill package for AI agents. Use it for books, manuals, legal or policy texts, fiction, scripts, subtitles, technical documentation, or any substantial source material that needs controlled terminology, preserved structure, context-safe chunking, durable artifacts, and audit-ready QA.

## Portable Entry Point

Start at the root `SKILL.md` in any runtime that supports skills. If the host loads instruction files instead, this `AGENTS.md` provides the same portable bootstrap and points to the canonical workflow in `core/d-transcreate.md`.

Platform adapters under `adapters/` are optional compatibility layers for host-native discovery. They do not change the workflow or artifact contract.

## Core Workflow

1. Read `core/d-transcreate.md` for operating principles and the seven-phase workflow.
2. Follow the phase sequence: Intake → Scan → Research → Plan → Translate → Coordinate → QA.
3. Persist all decisions as workspace artifacts on disk, not in chat history.
4. If subagents are available, dispatch scoped roles through `Subagent_Dispatch_Plan`.
5. If subagents are unavailable, run the same role contract sequentially; the artifacts remain mandatory for resume and auditability.

## Core Library

The single source of truth lives under `core/`:

- `core/d-transcreate.md` — canonical entrypoint with operating principles and workflow overview.
- `core/workflows/long-document.md` — phase-by-phase staged workflow.
- `core/workflows/terminology-research.md` — term mining, source priority, evidence rules.
- `core/workflows/fiction-continuity.md` — Story_Bible, reveal timing, character voice.
- `core/workflows/technical-domain.md` — Domain_Map, acronyms, units, standards.
- `core/workflows/context-management.md` — context budget, chunk loading, resume procedure.
- `core/workflows/subagents.md` — readiness gate, dispatch rules, sequential fallback.
- `core/workflows/qa-gates.md` — the eight mandatory QA gates.
- `core/schemas/` — artifact contracts and templates.
- `core/prompts/` — runtime-neutral role prompts.

## Required Artifacts

Create or maintain these files during a substantial translation run:

- Translation_Brief and Source_Map
- Glossary and Style_Sheet
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
| Claude Code | `adapters/claude-code/` | `.claude/skills/d-transcreate/SKILL.md` |
| OpenCode | `adapters/opencode/` | `AGENTS.md` + `opencode.json` |
| Cursor | `adapters/cursor/` | `.cursor/rules/d-transcreate.mdc` |
| Codex | `adapters/codex/` | `SKILL.md` |
| Generic | `adapters/generic/` | `AGENTS.md` + `d-transcreate.md` |

Install a portable or host-native layout with:

```bash
python scripts/build_adapters.py --platform <portable|claude-code|opencode|cursor|codex|generic> --dest <path>
```

## Subagent Roles

The skill defines seven fixed roles. Workers propose; the coordinator approves and writes global artifacts.

1. **Transcreate Coordinator** — final authority on glossary, style, voice, continuity, merge, and QA.
2. **Terminology Researcher** — mines and proposes evidence-backed terms.
3. **Style Researcher** — proposes target-language style and register rules.
4. **Chunk Translator** — translates one assigned chunk through the multi-pass cycle.
5. **Continuity Reviewer** — flags cross-chunk story or domain continuity defects.
6. **Fidelity Reviewer** — flags omissions, additions, distortions, and formal-data mismatches.
7. **Formatting Reviewer** — flags structure, layout, table, link, citation, and code-block defects.

For full details, read `core/d-transcreate.md` and the referenced workflow files on demand.
