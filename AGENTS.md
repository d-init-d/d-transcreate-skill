# D Transcreate Skill

This project is a translation and transcreation skill pack for long documents.
Use it when you need to translate books, technical manuals, legal texts, fiction,
scripts, or any substantial document with controlled terminology, consistent voice,
and durable state across sessions.

## Getting Started

1. Read `core/d-transcreate.md` for the canonical workflow and operating principles.
2. Follow the seven-phase workflow: Intake → Scan → Research → Plan → Translate → Merge → QA.
3. Persist all decisions as workspace artifacts (files on disk), not in chat history.

## Core Library

The single source of truth lives under `core/`:

- `core/d-transcreate.md` — Canonical entrypoint with operating principles and workflow overview.
- `core/workflows/` — Detailed workflow guides:
  - `long-document.md` — Full phase-by-phase staged workflow.
  - `terminology-research.md` — Term mining, source priority, evidence rules.
  - `fiction-continuity.md` — Story Bible, reveal timing, character voice.
  - `technical-domain.md` — Domain Map, acronyms, units, standards.
  - `qa-gates.md` — The 8 mandatory QA gates.
  - `context-management.md` — Context budget, chunk loading, resume procedure.
  - `subagents.md` — Readiness gate, role dispatch, parallel rules.
- `core/schemas/` — Artifact templates (glossary, style-sheet, chunk-manifest, etc.).
- `core/prompts/` — Role prompts for the seven subagent roles.

## Platform-Specific Adapters

If your platform has a dedicated adapter, use it for optimized integration:

| Platform | Adapter location | Entrypoint |
|----------|-----------------|------------|
| Codex | `adapters/codex/` | `SKILL.md` |
| Claude Code | `adapters/claude-code/` | `CLAUDE.md` |
| Cursor | `adapters/cursor/` | `.cursor/rules/d-transcreate.mdc` |
| OpenCode | `adapters/opencode/` | `AGENTS.md` + `opencode.json` |
| Generic | `adapters/generic/` | `AGENTS.md` + `d-transcreate.md` |

Each adapter is a template layout. To install into a consumer project, use:

```bash
python scripts/build_adapters.py --platform <name> --dest <path>
```

Or manually copy the adapter folder contents into your project root.

## Subagent Roles

The skill defines seven fixed roles that can be dispatched as subagents:

1. **Transcreate Coordinator** — Final authority on glossary, style, voice, continuity, and merge.
2. **Terminology Researcher** — Mines and proposes terms; never writes global glossary directly.
3. **Style Researcher** — Researches target-language conventions; proposes style rules.
4. **Chunk Translator** — Owns one chunk through the multi-pass translation cycle.
5. **Continuity Reviewer** — Checks cross-chunk consistency and story/domain continuity.
6. **Fidelity Reviewer** — Checks source faithfulness (omissions, additions, distortions).
7. **Formatting Reviewer** — Checks structural and formatting integrity.

Role prompts are at `core/prompts/<role-name>.md`.

## Quick Reference

When starting a translation task:

1. Produce a **Translation Brief** before translating anything.
2. Scan the full document and create a **Source Map**.
3. Research terminology → build **Glossary** and **Style Sheet**.
4. For fiction: build a **Story Bible**. For technical/legal: build a **Domain Map**.
5. Segment into chunks by semantic boundaries → **Chunk Manifest**.
6. Translate each chunk in multiple passes (draft → source-compare → revise → state-update).
7. Merge chunks and run a final voice pass.
8. Run all QA gates before delivery.

For full details, read `core/d-transcreate.md`.
