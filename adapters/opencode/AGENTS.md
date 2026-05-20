# D Transcreate Skill

This project contains a translation and transcreation skill pack for long documents.
Use it when you need to translate books, technical manuals, legal texts, fiction,
scripts, or any substantial document with controlled terminology, consistent voice,
and durable state across sessions.

## Getting Started

1. Read `core/d-transcreate.md` for the canonical workflow and operating principles.
2. The `opencode.json` in this directory configures the skill instructions for OpenCode.
3. Subagent role prompts are available under `.opencode/agents/`.

## Key Directories

- `core/` — Single source of truth: workflows, schemas, and subagent prompts.
- `core/workflows/` — Detailed workflow guides (long-document, terminology, QA, etc.).
- `core/schemas/` — Artifact templates (glossary, style-sheet, chunk-manifest, etc.).
- `core/prompts/` — Role prompts for the seven subagent roles.
- `.opencode/agents/` — OpenCode-specific subagent wrappers.

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

If OpenCode does not support real parallel subagents, execute the same role contract sequentially while preserving the artifact handoff rules. The Context_Plan and Subagent_Dispatch_Plan are still required for auditability and resume support.

See `core/workflows/subagents.md` and `core/workflows/context-management.md` for full details.

## Subagent Roles

The following roles can be dispatched as subagents:

1. **Transcreate Coordinator** — final authority on glossary, style, voice, continuity, and merge.
2. **Terminology Researcher** — mines and proposes terms; never writes global glossary directly.
3. **Style Researcher** — researches target-language conventions; proposes style rules.
4. **Chunk Translator** — owns one chunk through the multi-pass cycle.
5. **Continuity Reviewer** — checks cross-chunk consistency and story/domain continuity.
6. **Fidelity Reviewer** — checks source faithfulness (omissions, additions, distortions).
7. **Formatting Reviewer** — checks structural and formatting integrity.

For full details, read `core/d-transcreate.md`.
