---
name: d-transcreate
description: Faithful translation and transcreation workflow for books, long-form documents, technical material, fiction, scripts, and mixed-format source files. Use when Codex needs to translate, localize, adapt, or quality-check a substantial document with terminology research, style control, glossary management, continuity tracking, chunking, and optional parallel subagents.
---

# D Transcreate Skill

> **Canonical workflow:** `core/d-transcreate.md` (all paths are relative to the project root)

Use this skill to translate or transcreate long documents with controlled terminology,
consistent voice, and durable state across context windows.

## Quick Start

1. Read `core/d-transcreate.md` for operating principles and the 8-phase workflow.
2. Follow the phase sequence: Intake → Scan → Research → Plan → Translate → Merge → QA → Delivery.
3. Persist all artifacts (brief, glossary, style sheet, manifest, summaries) as workspace files.

## Operating Principles

- Preserve meaning, intent, register, structure, and factual accuracy before surface fluency.
- Translate literally only when literal wording carries the intended effect.
- Prefer natural target-language prose when idioms, humor, slogans, dialogue, or cultural references need adaptation.
- Never silently invent, omit, simplify, or reorder source meaning.
- Mark uncertainty with a concrete note and a proposed resolution path.
- Do not copy existing copyrighted translations — use lawful samples only to infer terminology, register, and structural conventions.
- Keep reusable decisions in artifacts (files on disk), not in chat history.

## Core Workflow (Summary)

| Phase | Action | Key Artifact |
|-------|--------|--------------|
| 1. Intake | Identify source, target, audience, mode, quality bar | Translation Brief |
| 2. Scan | Whole-document inventory before any translation | Source Map |
| 3. Research | Mine terms, run `core/workflows/d-research-module.md`, build dossier | Research_Dossier + Glossary + Style Sheet |
| 4. Plan | Create Context_Plan, segment by semantic boundaries, plan dispatch | Context_Plan + Chunk Manifest + Subagent_Dispatch_Plan |
| 5. Translate | Dispatch per plan; sync `glossary-inbox.jsonl`; pass + Peer Cross-Check | Chunk outputs |
| 6. Merge | Verify coverage (`scripts/book_ops.py verify`) and merge in order | Merged output |
| 7. QA | Run all eight QA gates | QA Report |
| 8. Delivery | Deliver output + translator note after gates pass | Deliverable |

## Subagent Roles

When the platform supports parallel execution, seven roles may be dispatched: Transcreate Coordinator, Terminology Researcher, Style Researcher, Chunk Translator, Continuity Reviewer, Fidelity Reviewer, and Formatting Reviewer. Workers propose; only the Coordinator writes shared artifacts. Start every worker prompt with the Worker Contract Card from `core/workflows/subagents.md`.

See `core/prompts/` for full role definitions and `core/workflows/subagents.md` for the authoritative role table.

## Workflow Reference Files

- `core/workflows/long-document.md` — full staged workflow for books and large documents.
- `core/workflows/d-research-module.md` — modular Phase 3 research engine producing `Research_Dossier` (`core/schemas/research-dossier.md`).
- `core/workflows/terminology-research.md` — term mining, source priority, d-research integration.
- `core/workflows/fiction-continuity.md` — story bible, reveal timing, character voice.
- `core/workflows/technical-domain.md` — domain map, acronyms, units, standards.
- `core/workflows/qa-gates.md` — the 8 QA gates.
- `core/workflows/context-management.md` — context budget, chunk loading, resume procedure.
- `core/workflows/subagents.md` — readiness gate, role dispatch, live glossary sync, Peer Cross-Check.
- `scripts/book_ops.py` — deterministic book pipeline CLI (`init`, `scan`, `sync-glossary`, `verify`, `merge`).

## Artifact Schemas

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

## Orchestration Contract

Before chunking, create a **Context_Plan** (`core/schemas/context-plan.md`) to record context budget and chunk-size limits. Before dispatching any worker role, create a **Subagent_Dispatch_Plan** (`core/schemas/subagent-dispatch-plan.md`).

If Codex does not support real parallel subagents, execute the same role contract sequentially while preserving the artifact handoff rules. See `core/workflows/subagents.md` for the sequential fallback procedure.

## Default Deliverables

For a substantial translation task, produce or maintain these artifacts in the workspace:

- Translation Brief
- Source Map
- Glossary
- Style Sheet
- Story Bible (fiction) or Domain Map (technical/legal/medical)
- Context Plan
- Chunk Manifest
- Subagent Dispatch Plan (when delegating work)
- Chunk Summaries
- Unresolved Issues Log
- QA Report

For short tasks, apply the same logic mentally and return only the translated text plus any necessary notes.

## Context Management

- Never load the full source document into context unless it genuinely fits with room for QA.
- Per chunk, load only: brief, glossary slice, style rules, story bible/domain map excerpt, previous + next chunk summaries, current source chunk, and relevant unresolved issues.
- After completing a chunk, write a compact summary and unload the raw source.
- On context reset, re-open the chunk manifest first, then the context plan, then brief, style sheet, glossary, and current chunk source.

See `core/workflows/context-management.md` for the full resume procedure.
