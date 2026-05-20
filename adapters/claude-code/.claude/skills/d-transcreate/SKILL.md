---
name: d-transcreate
description: Faithful translation and transcreation workflow for books, long-form documents, technical material, fiction, scripts, and mixed-format source files. Use when Claude needs to translate, localize, adapt, or quality-check a substantial document with terminology research, style control, glossary management, continuity tracking, chunking, and optional parallel subagents.
---

# D Transcreate Skill

Canonical workflow: [`core/d-transcreate.md`](../../../../core/d-transcreate.md)

Use this skill for long-form translation/transcreation work that needs controlled
terminology, stable voice, chunking, QA, and durable state across Claude Code
sessions.

## Claude Code Procedure

1. Read `core/d-transcreate.md`.
2. Create the Translation_Brief before translating any chunk.
3. Build the Source_Map, then the Glossary and Style_Sheet.
4. Add a Story_Bible for narrative work or a Domain_Map for technical/legal work.
5. Create a **Context_Plan** (`core/schemas/context-plan.md`) to record context budget, chunk-size limits, and fallback triggers.
6. Create the Chunk_Manifest within the Context_Plan's chunk-size limits.
7. Create a **Subagent_Dispatch_Plan** (`core/schemas/subagent-dispatch-plan.md`) before dispatching any worker.
8. Use `.claude/agents/` role files only after the readiness gate is satisfied.
9. Merge centrally, run the final voice pass, then run all QA gates.

## Orchestration Model

The main Claude thread acts as the **Coordinator**. It owns all global artifacts and dispatches subagents with scoped artifact slices only — never the full project context.

- Coordinator creates and maintains the Context_Plan and Subagent_Dispatch_Plan.
- Subagents receive only their assigned chunk text and relevant artifact slices.
- Subagents return structured proposals; the Coordinator accepts/rejects and writes canonical artifacts.
- If context pressure is detected, the Coordinator reduces chunk size and updates the plan.

See `core/workflows/subagents.md` and `core/workflows/context-management.md` for full rules.

## Claude Subagents

Claude-specific wrappers live in `.claude/agents/`:

| Role | Claude file | Canonical prompt |
|---|---|---|
| Coordinator | `.claude/agents/transcreate-coordinator.md` | `core/prompts/transcreate-coordinator.md` |
| Terminology | `.claude/agents/terminology-researcher.md` | `core/prompts/terminology-researcher.md` |
| Style | `.claude/agents/style-researcher.md` | `core/prompts/style-researcher.md` |
| Chunk | `.claude/agents/chunk-translator.md` | `core/prompts/chunk-translator.md` |
| Continuity | `.claude/agents/continuity-reviewer.md` | `core/prompts/continuity-reviewer.md` |
| Fidelity | `.claude/agents/fidelity-reviewer.md` | `core/prompts/fidelity-reviewer.md` |
| Formatting | `.claude/agents/formatting-reviewer.md` | `core/prompts/formatting-reviewer.md` |

Workers propose changes. The coordinator owns final glossary, style, continuity,
merge, and QA decisions.

## Files to Load on Demand

Workflow guides:

- `core/workflows/long-document.md`
- `core/workflows/terminology-research.md`
- `core/workflows/fiction-continuity.md`
- `core/workflows/technical-domain.md`
- `core/workflows/qa-gates.md`
- `core/workflows/context-management.md`
- `core/workflows/subagents.md`

Artifact templates:

- `core/schemas/translation-brief.md`
- `core/schemas/source-map.md`
- `core/schemas/glossary.md`
- `core/schemas/style-sheet.md`
- `core/schemas/story-bible.md`
- `core/schemas/domain-map.md`
- `core/schemas/chunk-manifest.md`
- `core/schemas/chunk-summary.md`
- `core/schemas/context-plan.md`
- `core/schemas/subagent-dispatch-plan.md`
- `core/schemas/unresolved-issues.md`
- `core/schemas/qa-report.md`

## Context Management

Keep large sources out of active context. For each chunk, load only the brief,
relevant glossary/style slices, relevant Story_Bible or Domain_Map excerpt,
neighboring chunk summaries, current source chunk, and scoped unresolved issues.
After finishing a chunk, persist its output and summary, then continue from the
Chunk_Manifest on resume.
