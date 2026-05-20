# D Transcreate Skill

This project contains a translation and transcreation skill pack for long documents.
Use it when you need to translate books, technical manuals, legal texts, fiction,
scripts, or any substantial document with controlled terminology, consistent voice,
and durable state across sessions.

## Getting Started

1. Read `core/d-transcreate.md` for the canonical workflow and operating principles.
2. Use the Cursor rule `.cursor/rules/d-transcreate.mdc` to activate the skill
   when working on a translation task.
3. Follow the seven-phase workflow described in the core entrypoint.

## Key Directories

- `core/` — Single source of truth: workflows, schemas, and subagent prompts.
- `core/workflows/` — Detailed workflow guides (long-document, terminology, QA, etc.).
- `core/schemas/` — Artifact templates (glossary, style-sheet, chunk-manifest, etc.).
- `core/prompts/` — Role prompts for the seven subagent roles.

## Subagent Roles

1. **Transcreate Coordinator** — `core/prompts/transcreate-coordinator.md`
2. **Terminology Researcher** — `core/prompts/terminology-researcher.md`
3. **Style Researcher** — `core/prompts/style-researcher.md`
4. **Chunk Translator** — `core/prompts/chunk-translator.md`
5. **Continuity Reviewer** — `core/prompts/continuity-reviewer.md`
6. **Fidelity Reviewer** — `core/prompts/fidelity-reviewer.md`
7. **Formatting Reviewer** — `core/prompts/formatting-reviewer.md`

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

For full details, read `core/d-transcreate.md`.
