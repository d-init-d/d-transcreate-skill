# Long Document Workflow

Use this workflow when translating books, manuals, research reports, policies, training material, scripts, subtitles, or any document too large to fit safely in one context window.

This file is the canonical phase-by-phase reference. The entrypoint (`core/d-transcreate.md`) summarizes the seven phases; this file provides the full procedural detail.

---

## Phase 1: Intake Contract

Produce a **Translation_Brief** artifact before any chunk translation begins. The brief is the binding contract for the entire project.

### Required Fields

| Field | Decision |
|---|---|
| Source files | Paths, URLs, or user-provided text |
| Source language | Include dialect or variant if relevant |
| Target language | Include locale, script, spelling standard |
| Target locale | Regional conventions (date, number, currency, units) |
| Audience | General readers, specialists, children, executives, fans, regulators |
| Translation mode | Faithful, localized, transcreated, annotated, summary-translation |
| Register | Formal, neutral, literary, conversational, technical, marketing |
| Output format | Chat answer, Markdown, DOCX, PDF, bilingual table, subtitles, etc. |
| Formatting constraints | Keep names, preserve layout, adapt units, preserve citations, etc. |
| Do-not-translate items | Proper nouns, brand names, code identifiers, UI strings to retain |
| Terminology authority | Official glossary, client-provided list, domain standard |
| Research depth | Minimal, standard, deep (triggers `d-research` integration) |
| Quality bar | Draft, publishable, legal/technical review, bilingual review |
| Open questions | Anything unresolved that needs user input |

### Intake Rules

- If a required field is missing and can be inferred at low risk, infer it and note the inference.
- If a required field is missing and cannot be inferred safely, ask the user a single focused question for that field before proceeding.
- When the user does not specify a translation mode, default to **faithful translation with light transcreation for idioms and dialogue**.
- Persist the Translation_Brief as a file in the workspace. Schema: `core/schemas/translation-brief.md`.

---

## Phase 2: Source Inventory and Whole-Document Scan

Perform a single whole-document scan after the Translation_Brief is produced and before any chunk translation begins.

### Source Inventory Steps

1. List all source files and formats.
2. Extract text while preserving section order.
3. Identify non-body content: footnotes, captions, sidebars, tables, figures, endnotes, references, indexes, appendices.
4. Detect repeated sections, boilerplate, headers/footers, OCR noise, broken hyphenation, missing pages, and encoding issues.
5. Record hazards in the Source_Map.

Use dedicated file-format skills when layout matters (document/PDF/spreadsheet/presentation skills for DOCX, PDF, XLSX, or PPTX).

### Source Map Contents

Create a **Source_Map** artifact with:

- Document purpose and genre
- Chapter/section outline (every chapter, section, table, figure, footnote, caption, appendix, reference, and repeated block)
- Recurring concepts and terms
- Named entities
- Style and register observations
- Formatting or extraction hazards (OCR noise, broken hyphenation, missing pages, encoding issues, ambiguous structure)
- High-risk sections needing extra review
- Likely external references to research

### Fiction Extensions

When the source is fiction, memoir, narrative non-fiction, script, game, or comic, also capture:

- Cast list and name forms
- Relationships and power dynamics
- Point of view per chapter or scene
- Timeline and time jumps
- Location continuity
- Emotional arc
- Motifs, catchphrases, jokes, foreshadowing, and reveals
- Terms of address and pronoun choices in the target language

### Technical/Professional Extensions

When the source is technical, legal, medical, financial, academic, product, or policy material, also capture:

- Domain and subdomain
- Governing standards, laws, regulations, APIs, tools, products, and protocols
- Acronyms and initialisms
- Units, quantities, currencies, dates, and measurement conventions
- Diagrams, tables, formulas, citations, and cross-references

### Pre-Translation Decisions

Resolve these before chunk work starts and store decisions in the Glossary, Style_Sheet, Story_Bible, or Domain_Map:

- Translate or retain proper nouns
- Title, subtitle, heading, and chapter naming conventions
- Terms of address, honorifics, pronouns, and relationship markers
- Number, date, currency, unit, and citation conventions
- Dialogue punctuation and paragraphing conventions
- How to handle footnotes, translator notes, wordplay, songs, poems, and quotations
- "Do not translate" items
- "Must be consistent" terms

Schema: `core/schemas/source-map.md`.

---

## Phase 3: Segmenting (Chunking)

Split the work by **semantic units**, not arbitrary token count. Never split in the middle of a sentence, paragraph, table row, or single dialogue exchange.

### Chunk Boundary Preference Order

1. Chapter or article section
2. Scene or subsection
3. Paragraph group
4. Table / figure / caption group
5. Footnote / endnote group tied to its anchor

### Recommended Chunk Sizes

| Material type | Source words per chunk |
|---|---|
| Routine prose | 1,200–2,500 |
| Dense technical / legal text | 600–1,500 |
| Fiction scene / dialogue | One scene or 800–2,000 |
| Tables / slides / subtitles | One logical table, slide group, or subtitle block |

### Chunk Sizing Constraint

Each chunk must be small enough to fit in active context alongside:

- The Translation_Brief
- The relevant Glossary slice
- The relevant Style_Sheet rules
- The relevant Story_Bible or Domain_Map slice
- The previous Chunk_Summary
- The next Chunk_Summary (when available)

### Chunk Identifiers

Assign each chunk a stable identifier following a predictable pattern:

- `ch03-sec02` (chapter-section)
- `p012-018` (page range)
- `scene-07` (scene number)

### Chunk Manifest

Create a **Chunk_Manifest** artifact recording for each chunk:

| Column | Description |
|---|---|
| chunk_id | Stable identifier |
| source_location | File path + section/page reference |
| word_or_page_range | Approximate scope |
| semantic_unit | Chapter, scene, section, table group, etc. |
| dependencies | Other chunks this one depends on |
| assigned_to | Worker subagent or "coordinator" |
| status | Current state (see status values below) |
| output_path | Where the translated chunk is written |
| qa_status | QA gate results |
| notes | Any relevant notes |

**Status values:** `planned`, `research-needed`, `ready`, `drafting`, `drafted`, `qa-needed`, `revising`, `done`, `blocked`.

Schema: `core/schemas/chunk-manifest.md`.

---

## Phase 4: Multi-Pass Translation

Use the same four passes for each chunk. Do not skip passes.

### Pass A: Draft

Translate the chunk using the current Translation_Brief, Glossary, Style_Sheet, Story_Bible or Domain_Map, and adjacent Chunk_Summary entries.

**Rules:**

- Preserve all meaning-bearing details.
- Keep paragraph order unless the output format explicitly allows adaptation.
- Preserve numbers, names, citations, references, and quoted material with extra care.
- Do not resolve ambiguous terms by guessing — mark them for review and add to the Unresolved_Issues_Log.

### Pass B: Source Compare

Compare sentence by sentence or paragraph by paragraph. Check for:

- Missing source content (omissions)
- Added content not supported by the source
- Mistranslated negation, modality, causality, chronology, or agency
- Wrong speaker or referent
- Inconsistent term or name usage against the Glossary
- Numbers, dates, formulas, citations, URLs, code identifiers, equation labels, table references — underlying values and identifiers must match the source exactly
- Table row/column alignment
- Formatting markers and footnote anchors

**Format conversion rule:** Date, unit, currency, and number notation conversions are applied only when explicitly specified in the Translation_Brief or Style_Sheet, and must follow the documented conversion rule recorded there.

### Pass C: Target-Language Revision

Revise for natural target-language prose:

- Improve flow without changing meaning
- Preserve author voice and genre conventions
- Keep technical precision where required
- Adapt idioms by function, not word-for-word
- Avoid over-explaining unless translator notes are requested
- Maintain consistency with the Style_Sheet

### Pass D: State Update

After completing passes A–C for a chunk:

1. Update the Chunk_Manifest status for this chunk.
2. Update the Glossary with any new terms or changed decisions.
3. Update the Style_Sheet with any new decisions.
4. Update the Story_Bible or Domain_Map with new facts.
5. Write a compact **Chunk_Summary** for this chunk (used by adjacent chunks for continuity).
6. Log any QA issues, uncertain items, or follow-ups in the Unresolved_Issues_Log.

If a term in the chunk is ambiguous and no glossary entry resolves it, mark the term as uncertain in the chunk output and add it to the Unresolved_Issues_Log instead of guessing.

---

## Phase 5: Subagent Dispatch (When Available)

This phase applies only when the platform supports parallel subagents. If not, execute the same role responsibilities sequentially.

### Readiness Gate

Do NOT dispatch any Worker_Subagent before ALL of the following exist on disk:

- Translation_Brief
- Source_Map
- Glossary (with proposed core terms)
- Style_Sheet
- Chunk_Manifest
- Story_Bible or Domain_Map (as applicable)

### Dispatch Rules

- Assign each Worker_Subagent a disjoint scope from the role set: terminology research, style research, chunk translation, continuity review, fidelity review, or formatting review.
- Provide each worker only the relevant artifact slices and chunk text, not the full document.
- Never allow two workers to edit the same output file in parallel.
- The Coordinator_Subagent retains final authority over Glossary changes, Style_Sheet decisions, voice consistency, and continuity across chunks.

See `core/workflows/subagents.md` for full orchestration details.

---

## Phase 6: Merge and Final Voice Pass

After all assigned chunks have status `done` in the Chunk_Manifest:

### Merge Steps

1. **Merge in source order.** Concatenate chunk outputs following the original document structure.
2. **Cross-chunk consistency checks.** Verify terminology, headings, table labels, captions, footnotes, references, and punctuation are consistent across chunk boundaries.
3. **Resolve glossary conflicts.** If the merge step detects conflicting Glossary applications across chunks, resolve them against the approved Glossary entries before producing the final output.
4. **Normalize formatting.** Headings, table labels, captions, footnotes, references, and punctuation must follow a single convention throughout.
5. **Read across boundaries.** Check transitions between chunks for flow and continuity.

### Final Voice Pass

Run a single final voice pass over the merged output **centrally** — not as independent chunk work. This pass:

- Smooths transitions between chunks
- Ensures consistent register and voice throughout
- Catches any remaining inconsistencies that only appear at document scale
- Does NOT change meaning or terminology decisions already approved

### Post-Merge State Update

- Update the Story_Bible or Domain_Map with any continuity facts emitted by Worker_Subagent outputs that were accepted during merge.
- Update the Chunk_Manifest to reflect final status.

---

## Phase 7: Delivery

Deliver the translated artifact plus a short translator note covering:

- Scope translated
- Assumptions made
- Unresolved issues (reference the Unresolved_Issues_Log)
- Terminology choices worth reviewing
- Known extraction or formatting limitations
- QA checks performed (reference the QA_Report)
- Residual risks

Do not include internal scratch notes unless the user asks for them.

Before delivery, all QA gates defined in `core/workflows/qa-gates.md` must pass.

---

## Summary of Artifacts Produced

| Artifact | Phase | Schema |
|---|---|---|
| Translation_Brief | Phase 1 | `core/schemas/translation-brief.md` |
| Source_Map | Phase 2 | `core/schemas/source-map.md` |
| Glossary | Phase 2–4 | `core/schemas/glossary.md` |
| Style_Sheet | Phase 2–4 | `core/schemas/style-sheet.md` |
| Story_Bible / Domain_Map | Phase 2–4 | `core/schemas/story-bible.md` / `core/schemas/domain-map.md` |
| Chunk_Manifest | Phase 3–6 | `core/schemas/chunk-manifest.md` |
| Chunk_Summary (per chunk) | Phase 4 (Pass D) | `core/schemas/chunk-summary.md` |
| Unresolved_Issues_Log | Throughout | `core/schemas/unresolved-issues.md` |
| QA_Report | Phase 7 | `core/schemas/qa-report.md` |
