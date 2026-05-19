# Archive — Legacy Files

This directory contains legacy files that have been superseded by the canonical
`core/` library and `adapters/` structure. They are preserved here for reference
only and are **not** part of the active skill pack.

## Archived Files

| Legacy location | Migrated to |
|---|---|
| `SKILL.md` (root) | `core/d-transcreate.md` + `adapters/codex/SKILL.md` |
| `agents/openai.yaml` | `adapters/codex/agents/openai.yaml` |
| `references/long-document-workflow.md` | `core/workflows/long-document.md` |
| `references/research-and-style.md` | `core/workflows/terminology-research.md` |
| `references/context-and-subagents.md` | `core/workflows/context-management.md` + `core/workflows/subagents.md` |
| `references/qa-gates.md` | `core/workflows/qa-gates.md` |
| `references/artifact-schemas.md` | `core/schemas/` (individual schema files) |

## Why Archived (Not Deleted)

These files are kept for traceability during the migration period. Once the team
confirms the new structure is stable, this `_archive/` directory may be removed
entirely.

Do **not** reference these files from any adapter, workflow, or script. The
canonical source of truth is always `core/`.
