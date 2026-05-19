---
name: d-transcreate
description: Faithful translation and transcreation workflow for books, long-form documents, technical material, fiction, scripts, and mixed-format source files. Use when Claude needs to translate, localize, adapt, or quality-check a substantial document with terminology research, style control, glossary management, continuity tracking, chunking, and optional parallel subagents.
---

# D Transcreate Skill

> **Canonical workflow:** [`core/d-transcreate.md`](../../../../core/d-transcreate.md)

Use this skill to translate or transcreate long documents with controlled terminology,
consistent voice, and durable state across context windows.

## Quick Start

1. Read `core/d-transcreate.md` for operating principles and the 7-phase workflow.
2. Follow the phase sequence: Intake → Scan → Research → Plan → Translate → Coordinate → QA.
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
| 3. Research | Mine terms, research style, build glossary | Glossary + Style Sheet |
| 4. Plan | Segment by semantic boundaries, create manifest | Chunk Manifest |
| 5. Translate | Multi-pass per chunk: draft → compare → revise → update | Chunk outputs |
| 6. Coordinate | Dispatch subagents (if parallel), merge, voice pass | Merged output |
| 7. QA | Run all QA gates before delivery | QA Report |

## Subagent Roles

When dispatching subagents, use the agent files under `.claude/agents/`:

1. **Transcreate Coordinator** — final authority on glossary, style, voice, continuity, and merge.
2. **Terminology Researcher** — mines and proposes terms; never writes global glossary directly.
3. **Style Researcher** — researches target-language conventions; proposes style rules.
4. **Chunk Translator** — owns one chunk through the multi-pass cycle.
5. **Continuity Reviewer** — checks cross-chunk consistency and story/domain continuity.
6. **Fidelity Reviewer** — checks source faithfulness (omissions, additions, distortions).
7. **Formatting Reviewer** — checks structural and formatting integrity.

See `core/prompts/` for full canonical role definitions.

## Workflow Reference Files

- `core/workflows/long-document.md` — full staged workflow for books and large documents.
- `core/workflows/terminology-research.md` — term mining, source priority, d-research integration.
- `core/workflows/fiction-continuity.md` — story bible, reveal timing, character voice.
- `core/workflows/technical-domain.md` — domain map, acronyms, units, standards.
- `core/workflows/qa-gates.md` — the 8 QA gates.
- `core/workflows/context-management.md` — context budget, chunk loading, resume procedure.
- `core/workflows/subagents.md` — readiness gate, role dispatch, parallel rules.

## Artifact Schemas

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

## Context Management

- Never load the full source document into context unless it genuinely fits with room for QA.
- Per chunk, load only: brief, glossary slice, style rules, story bible/domain map excerpt, previous + next chunk summaries, current source chunk, and relevant unresolved issues.
- After completing a chunk, write a compact summary and unload the raw source.
- On context reset, re-open the chunk manifest first, then brief, style sheet, glossary, and current chunk source.

See `core/workflows/context-management.md` for the full resume procedure.
