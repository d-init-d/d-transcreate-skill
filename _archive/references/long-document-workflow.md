# Long Document Workflow

Use this file when translating books, manuals, research reports, policies, training material, scripts, subtitles, or any document too large to fit safely in one context window.

## 1. Intake Contract

Capture these fields before production translation:

| Field | Decision |
|---|---|
| Source files | Paths, URLs, or user-provided text |
| Source language | Include dialect or variant if relevant |
| Target language | Include locale, script, spelling, and audience |
| Output format | Chat answer, Markdown, DOCX, PDF, bilingual table, subtitles, etc. |
| Translation mode | Faithful, localized, transcreated, annotated, summary-translation |
| Audience | General readers, specialists, children, executives, fans, regulators |
| Register | Formal, neutral, literary, conversational, technical, marketing |
| Constraints | Keep names, preserve layout, adapt units, preserve citations, etc. |
| Quality bar | Draft, publishable, legal/technical review, bilingual review |

If a required field is missing, infer only when low risk. Otherwise ask a focused question.

## 2. Source Inventory

Inspect all files before translating:

1. List files and formats.
2. Extract text while preserving section order.
3. Identify non-body content: footnotes, captions, sidebars, tables, figures, endnotes, references, indexes.
4. Detect repeated sections, boilerplate, headers/footers, OCR noise, broken hyphenation, missing pages, and encoding issues.
5. Record hazards in the source map.

Use dedicated file-format skills when layout matters. For example, use document/PDF/spreadsheet/presentation skills for DOCX, PDF, XLSX, or PPTX.

## 3. Whole-Document Scan

Do one fast scan before translation. The goal is orientation, not polished output.

Create a source map with:

- document purpose and genre
- chapter/section outline
- recurring concepts and terms
- named entities
- style and register observations
- formatting or extraction hazards
- high-risk sections needing extra review
- likely external references to research

For fiction, also capture:

- cast list and name forms
- relationships and power dynamics
- point of view per chapter or scene
- timeline and time jumps
- location continuity
- emotional arc
- motifs, catchphrases, jokes, foreshadowing, and reveals
- terms of address and pronoun choices in the target language

For technical/professional material, also capture:

- domain and subdomain
- standards, laws, regulations, APIs, tools, products, and protocols
- acronyms and initialisms
- units, quantities, currencies, dates, and measurement conventions
- diagrams, tables, formulas, citations, and cross-references

## 4. Pre-Translation Decisions

Resolve these before chunk work starts:

- Translate or retain proper nouns.
- Choose title, subtitle, heading, and chapter naming conventions.
- Choose terms of address, honorifics, pronouns, and relationship markers.
- Choose number, date, currency, unit, and citation conventions.
- Choose dialogue punctuation and paragraphing conventions.
- Choose how to handle footnotes, translator notes, wordplay, songs, poems, and quotations.
- Define "do not translate" items.
- Define "must be consistent" terms.

Store decisions in the glossary, style sheet, story bible, or domain map.

## 5. Segmenting

Split the work by semantic units, not arbitrary token count.

Preferred chunk order:

1. chapter or article section
2. scene or subsection
3. paragraph group
4. table/figure/caption group
5. footnote/endnote group tied to its anchor

Recommended chunk size:

- routine prose: 1,200 to 2,500 source words
- dense technical/legal text: 600 to 1,500 source words
- fiction scene/dialogue: one scene or 800 to 2,000 source words
- tables/slides/subtitles: one logical table, slide group, or subtitle block

Each chunk needs stable IDs such as `ch03-sec02` or `p012-018`.

## 6. Translation Passes

Use the same passes for each chunk:

### Pass A: Draft

Translate the chunk using the current brief, glossary, style sheet, story bible/domain map, and adjacent summaries.

Rules:

- Preserve all meaning-bearing details.
- Keep paragraph order unless the output format explicitly allows adaptation.
- Preserve numbers, names, citations, references, and quoted material with extra care.
- Do not resolve ambiguous terms by guessing. Mark them for review.

### Pass B: Source Compare

Compare sentence by sentence or paragraph by paragraph:

- missing source content
- added content not supported by the source
- mistranslated negation, modality, causality, chronology, or agency
- wrong speaker or referent
- inconsistent term or name
- numbers, dates, formulas, citations, URLs, labels
- table row/column alignment
- formatting markers and footnote anchors

### Pass C: Target-Language Revision

Revise for natural target-language prose:

- improve flow without changing meaning
- preserve author voice and genre
- keep technical precision where required
- adapt idioms by function, not word-for-word
- avoid over-explaining unless translator notes are requested

### Pass D: State Update

After each chunk:

- update chunk status
- update glossary changes and unresolved terms
- update style sheet decisions
- update story bible/domain map facts
- write a compact chunk summary
- log QA issues and follow-ups

## 7. Merge and Final Voice Pass

After all chunks are translated:

1. Merge in source order.
2. Run cross-chapter consistency checks.
3. Resolve glossary conflicts.
4. Normalize headings, table labels, captions, footnotes, references, and punctuation.
5. Read across boundaries between chunks.
6. Run one final voice pass centrally, not as independent chunk work.

## 8. Delivery

Deliver the translated artifact plus a short translator note when useful:

- scope translated
- assumptions made
- unresolved issues
- terminology choices worth reviewing
- known extraction or formatting limitations
- QA checks performed

Do not include internal scratch notes unless the user asks for them.
