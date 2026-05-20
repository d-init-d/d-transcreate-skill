# D Transcreate Skill

This project contains a translation and transcreation skill pack for long documents.
Use it when you need to translate books, technical manuals, legal texts, fiction,
scripts, or any substantial document with controlled terminology, consistent voice,
and durable state across sessions.

## Getting Started

1. Read `core/d-transcreate.md` for the canonical workflow and operating principles.
2. Read `adapters/generic/d-transcreate.md` for the skill entrypoint and role index.
3. Follow the seven-phase workflow described in the core entrypoint.

## Key Directories

- `core/` — Single source of truth: workflows, schemas, and subagent prompts.
- `core/workflows/` — Detailed workflow guides (long-document, terminology, QA, etc.).
- `core/schemas/` — Artifact templates (glossary, style-sheet, chunk-manifest, etc.).
- `core/prompts/` — Role prompts for the seven subagent roles.

## Quick Reference

When starting a translation task:

1. Produce a Translation Brief before translating anything.
2. Scan the full document and create a Source Map.
3. Research terminology and build a Glossary and Style Sheet.
4. Create a **Context_Plan** (`core/schemas/context-plan.md`) to record context budget and chunk-size limits.
5. Segment into chunks by semantic boundaries within the Context_Plan's limits.
6. Create a **Subagent_Dispatch_Plan** (`core/schemas/subagent-dispatch-plan.md`) before dispatching workers.
7. Translate each chunk in multiple passes (draft, source-compare, revise, state-update).
8. Run QA gates before delivery.

## Orchestration Contract

If the platform does not support real parallel subagents, execute the same role contract sequentially while preserving the artifact handoff rules. The Context_Plan and Subagent_Dispatch_Plan are still required for auditability and resume support.

See `core/workflows/subagents.md` and `core/workflows/context-management.md` for full details.

For full details, read `core/d-transcreate.md`.
