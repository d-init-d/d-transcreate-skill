# D Transcreate — Generic Adapter

This file is the skill entrypoint for any AI agent that does not have a
platform-specific adapter. It contains no frontmatter, no tool-specific syntax,
and no special directives — just plain Markdown.

## Core Workflow

Read and follow the canonical entrypoint:

→ `core/d-transcreate.md`

That document defines the operating principles and the seven-phase workflow:
Intake, Whole-Document Scan, Research Terminology and Style, Plan Chunks,
Translate in Passes, Coordinate Subagents, and Run QA Gates.

## Subagent Role Prompts

When you need to adopt a specific role or dispatch work to a subagent,
read the corresponding prompt file:

| Role | Prompt File |
|------|-------------|
| Transcreate Coordinator | `core/prompts/transcreate-coordinator.md` |
| Terminology Researcher | `core/prompts/terminology-researcher.md` |
| Style Researcher | `core/prompts/style-researcher.md` |
| Chunk Translator | `core/prompts/chunk-translator.md` |
| Continuity Reviewer | `core/prompts/continuity-reviewer.md` |
| Fidelity Reviewer | `core/prompts/fidelity-reviewer.md` |
| Formatting Reviewer | `core/prompts/formatting-reviewer.md` |

## Artifact Schemas

All artifact templates live under `core/schemas/`. Key schemas:

- `core/schemas/translation-brief.md`
- `core/schemas/source-map.md`
- `core/schemas/glossary.md`
- `core/schemas/style-sheet.md`
- `core/schemas/story-bible.md`
- `core/schemas/domain-map.md`
- `core/schemas/chunk-manifest.md`
- `core/schemas/chunk-summary.md`
- `core/schemas/unresolved-issues.md`
- `core/schemas/qa-report.md`

## Workflow Guides

Detailed workflow instructions live under `core/workflows/`:

- `core/workflows/long-document.md` — Full staged workflow for books and large documents.
- `core/workflows/terminology-research.md` — Term mining and source priority.
- `core/workflows/fiction-continuity.md` — Story Bible and reveal-timing rules.
- `core/workflows/technical-domain.md` — Domain Map and formal-data handling.
- `core/workflows/qa-gates.md` — The eight mandatory QA gates.
- `core/workflows/context-management.md` — Context budget and resume procedure.
- `core/workflows/subagents.md` — Subagent orchestration and parallel rules.

## Notes

- This adapter does not depend on any tool-specific syntax or platform features.
- All workflow logic lives in `core/` — this file only points you there.
- If your platform supports lazy file loading, read files on demand as the
  workflow requires them rather than loading everything upfront.
