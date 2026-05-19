# D Transcreate — Canonical Entrypoint

Version: 0.1.0

Use this skill to translate or transcreate long documents with controlled terminology,
consistent voice, and durable state across context windows.

## Operating Principles

0. Record the skill version in the Translation_Brief and final QA_Report so the
   translation can be reproduced or audited later.
1. Preserve meaning, intent, register, structure, and factual accuracy before surface fluency.
2. Translate literally only when literal wording carries the intended effect.
3. Prefer natural target-language prose when idioms, humor, slogans, dialogue, or cultural references need adaptation.
4. Never silently invent, omit, simplify, or reorder source meaning.
5. Mark uncertainty with a concrete note and a proposed resolution path.
6. Do not copy existing copyrighted translations — use lawful samples only to infer terminology, register, and structural conventions.
7. Keep reusable decisions in artifacts (files on disk), not in chat history.

## Core Workflow

### Phase 1 — Intake

Identify source files, target language, audience, output format, translation mode, and quality bar.
Default to faithful translation with light transcreation for idioms and dialogue when mode is unspecified.
Produce a **Translation_Brief** before any chunk translation begins.

### Phase 2 — Whole-Document Scan

Inspect the full document once. Create a **Source_Map**: sections, chapters, tables, figures, notes, references, captions, appendices, repeated blocks, and formatting hazards.
For fiction: build a **Story_Bible** (characters, timeline, POV, motifs, terms of address).
For technical/legal/medical: build a **Domain_Map** (concepts, standards, acronyms, units, formal data).

### Phase 3 — Research Terminology and Style

Mine candidate terms before translating. Search for official translations, domain glossaries, and reputable parallel texts. Build a **Glossary** and **Style_Sheet**.
If `d-research-skill` is accessible, use it for source discovery and evidence logging.

### Phase 4 — Plan Chunks

Segment by semantic boundaries (chapter, scene, section, subsection, table/figure group).
Keep each chunk small enough for one pass with room for brief, glossary slice, style rules, adjacent summaries, and QA notes.
Create a **Chunk_Manifest** as the authoritative status ledger.

### Phase 5 — Translate in Passes

- **Pass A** — Draft faithful translation of one chunk.
- **Pass B** — Compare against source for omissions, additions, wrong emphasis, numbers, names, formatting, and term consistency.
- **Pass C** — Revise for target-language fluency while preserving source intent.
- **Pass D** — Update Glossary, Style_Sheet, Story_Bible/Domain_Map, Chunk_Summary, and Unresolved_Issues_Log.

### Phase 6 — Coordinate and Merge

Use subagents only after the Translation_Brief, Glossary, Style_Sheet, Chunk_Manifest, and Story_Bible/Domain_Map exist.
Assign disjoint scopes. Keep one coordinator responsible for final terminology, voice, and continuity.
Merge chunk outputs in source order and run a final voice pass.

### Phase 7 — QA Gates

Run all QA gates before delivery: completeness, fidelity, terminology, target-language quality, continuity, numbers/formal-data, formatting, and residual-risk reporting.
For high-stakes material, require source-backed terminology decisions and explicit residual-risk notes.

## Subagent Roles

| # | Role | Scope |
|---|------|-------|
| 1 | **Transcreate Coordinator** | Final authority on glossary, style, voice, continuity, and merge decisions. |
| 2 | **Terminology Researcher** | Mines terms, searches evidence, proposes glossary entries (never writes directly). |
| 3 | **Style Researcher** | Studies target-language conventions, proposes style-sheet rules (never writes directly). |
| 4 | **Chunk Translator** | Owns one chunk through passes A–D; proposes glossary/style edits. |
| 5 | **Continuity Reviewer** | Flags cross-chunk continuity defects (names, timeline, voice drift). |
| 6 | **Fidelity Reviewer** | Flags meaning divergence between source and target (omissions, additions, distortions). |
| 7 | **Formatting Reviewer** | Flags layout, table, footnote, heading, citation, and numbering defects. |

Workers propose; the Coordinator approves. No worker writes the global Glossary or Style_Sheet directly.

## Reference Index

### Workflows

| File | Concern |
|------|---------|
| `core/workflows/long-document.md` | Full staged workflow for books and large documents |
| `core/workflows/terminology-research.md` | Term mining, source priority, d-research integration |
| `core/workflows/fiction-continuity.md` | Story Bible maintenance, reveal-timing, character voice |
| `core/workflows/technical-domain.md` | Domain Map maintenance, acronyms, units, citations |
| `core/workflows/qa-gates.md` | The 8 QA gates (completeness through residual risk) |
| `core/workflows/context-management.md` | Context budget, chunk loading, resume procedure |
| `core/workflows/subagents.md` | Readiness gate, role dispatch, parallel rules, merge checklist |

### Schemas

| File | Artifact |
|------|----------|
| `core/schemas/translation-brief.md` | Translation_Brief |
| `core/schemas/source-map.md` | Source_Map |
| `core/schemas/glossary.md` | Glossary (CSV + Markdown forms) |
| `core/schemas/style-sheet.md` | Style_Sheet |
| `core/schemas/story-bible.md` | Story_Bible |
| `core/schemas/domain-map.md` | Domain_Map |
| `core/schemas/chunk-manifest.md` | Chunk_Manifest (CSV + Markdown forms) |
| `core/schemas/chunk-summary.md` | Chunk_Summary |
| `core/schemas/unresolved-issues.md` | Unresolved_Issues_Log |
| `core/schemas/qa-report.md` | QA_Report |

### Prompts

| File | Role |
|------|------|
| `core/prompts/transcreate-coordinator.md` | Transcreate Coordinator |
| `core/prompts/terminology-researcher.md` | Terminology Researcher |
| `core/prompts/style-researcher.md` | Style Researcher |
| `core/prompts/chunk-translator.md` | Chunk Translator |
| `core/prompts/continuity-reviewer.md` | Continuity Reviewer |
| `core/prompts/fidelity-reviewer.md` | Fidelity Reviewer |
| `core/prompts/formatting-reviewer.md` | Formatting Reviewer |

## Copyright Rules

Existing translations may inform terminology and style **only** as paraphrased observations with short, attributed evidence quotes. The agent SHALL NOT:

- Reproduce extended passages from copyrighted translations.
- Translate by patching together fragments of existing translations.
- Use fan or unofficial translations as authoritative without independent verification.
- Hide the influence source when a term choice depends on a prior translation.

When quoting evidence, keep quotes short (a few words to one sentence), attribute the source, and use the quote solely to justify a terminology or style decision — never as part of the delivered translation output.
