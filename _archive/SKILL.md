---
name: d-transcreate-skill
description: Faithful translation and transcreation workflow for books, long-form documents, technical material, fiction, scripts, and mixed-format source files. Use when Codex needs to translate, localize, adapt, or quality-check a substantial document with terminology research, style control, glossary management, continuity tracking, chunking, and optional parallel subagents. Also use when the user asks for a strict workflow for book/document translation or wants to integrate translation work with d-research.
---

# D Transcreate Skill

Use this skill to translate or transcreate long documents with controlled terminology, consistent voice, and durable state across context windows.

## Operating Principles

- Preserve meaning, intent, register, structure, and factual accuracy before surface fluency.
- Translate literally only when literal wording carries the intended effect.
- Prefer natural target-language prose when idioms, humor, slogans, dialogue, or cultural references need adaptation.
- Never silently invent, omit, simplify, or reorder source meaning.
- Mark uncertainty with a concrete note and a proposed resolution path.
- Do not copy existing copyrighted translations. Use lawful samples only to infer terminology, register, and structural conventions.
- Keep reusable decisions in artifacts, not in chat history.

## Core Workflow

1. **Intake**
   - Identify source files, target language, audience, expected output format, translation mode, deadline, and quality bar.
   - If the user has not specified mode, default to faithful translation with light transcreation for idioms and dialogue.
   - If files are PDF, DOCX, PPTX, XLSX, EPUB, HTML, or scanned images, use the relevant document/file skill or extraction tool before translating.

2. **Inventory and whole-document scan**
   - Inspect the full document once before translating.
   - Create a source map: sections, chapters, tables, figures, notes, references, captions, appendices, repeated blocks, and formatting hazards.
   - For fiction, create a story bible: characters, relationships, timeline, POV, scene goals, unresolved threads, terms of address, repeated motifs, and tone shifts.
   - For technical or professional documents, create a domain map: concepts, standards, product names, acronyms, units, legal or regulatory references, and canonical terminology.

3. **Research terminology and style**
   - Mine candidate terms, names, acronyms, idioms, recurring phrases, and culturally loaded expressions before translating.
   - Search for official translations, domain glossaries, localized product/docs, laws/standards, publisher conventions, and reputable parallel texts.
   - If `$d-research` is available, use it for source discovery, multilingual research, evidence logging, and source-quality checks. Read `references/research-and-style.md` for the integration pattern.
   - Build a glossary and style sheet before assigning translation chunks.

4. **Plan chunks and state**
   - Segment by semantic boundaries: chapter, scene, section, subsection, table, or figure group.
   - Keep each active chunk small enough for one pass with room for brief, glossary slice, style rules, previous/next summaries, and QA notes.
   - Create a chunk manifest and status ledger. Read `references/context-and-subagents.md` before long work or parallel work.

5. **Translate in passes**
   - Pass A: draft faithful translation of one chunk.
   - Pass B: compare against the source for omissions, additions, wrong emphasis, numbers, names, formatting, and term consistency.
   - Pass C: revise for target-language fluency while preserving source intent.
   - Pass D: update glossary, style sheet, story bible, chunk summary, and unresolved-issues list.

6. **Coordinate subagents when useful**
   - Use subagents only after the translation brief, glossary, style sheet, and chunk manifest exist.
   - Assign disjoint scopes: terminology research, style research, chunk drafting, continuity QA, or formatting QA.
   - Keep one coordinator responsible for final terminology, voice, and continuity.
   - Give subagents only the needed artifact slices and chunk text, not the whole book.

7. **Run QA gates**
   - Before delivery, run the checks in `references/qa-gates.md`.
   - For high-stakes legal, medical, financial, academic, or safety-related material, require source-backed terminology decisions and explicit residual-risk notes.

## Reference Files

- `references/long-document-workflow.md`: full staged workflow for books and large documents.
- `references/research-and-style.md`: terminology mining, popular translation research, and `$d-research` integration.
- `references/context-and-subagents.md`: context control, chunking, state files, and parallel subagent rules.
- `references/qa-gates.md`: completeness, fidelity, terminology, formatting, and risk QA.
- `references/artifact-schemas.md`: recommended ledgers, tables, and reusable artifact templates.

## Default Deliverables

For a substantial translation task, produce or maintain these artifacts in the workspace:

- translation brief
- source map
- glossary
- style sheet
- story bible or domain map
- chunk manifest
- chunk summaries
- unresolved-issues log
- QA report

For short tasks, use the same logic mentally and return only the translated text plus any necessary notes.
