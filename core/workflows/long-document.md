# Long Document Workflow

Use this workflow when translating books, manuals, research reports, policies, training material, scripts, subtitles, or any document too large to fit safely in one context window.

This file is the canonical phase-by-phase reference. The entrypoint (`core/d-transcreate.md`) summarizes the eight phases; this file provides the full procedural detail. The phase numbers used here are the same across every workflow, schema, prompt, and adapter in this pack.

---

## Phase 1: Intake Contract

Produce a **Translation_Brief** artifact before any chunk translation begins. The brief is the binding contract for the entire project.

### Required Fields

| Field | Decision |
|---|---|
| Source files | Paths, URLs, or user-provided text |
| Skill version | Version from `core/d-transcreate.md` or `VERSION` |
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

### Zero-Config Book Mode

When a user drops a book or manuscript and specifies only the source path and target language, do not block on manual scaffolding. Run the deterministic initializer:

```bash
python3 scripts/book_ops.py init --source <path> --target-lang <lang> --workspace <dir>
```

This command creates `<workspace>/`, `output/`, `summaries/`, and `proposals/`, populates `translation-brief.md` with safe defaults (`Skill version: 1.0.0`, mode `"faithful translation with light transcreation for idioms and dialogue"`), initializes empty `glossary-inbox.jsonl`, `evidence-ledger.jsonl`, and `research-coverage.json`, seeds `glossary.csv` from `memory/glossary-<lang>.csv` when available, and links `core/locales/vi-VN.md` in `style-sheet.md` when the target language is Vietnamese.

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

### Deterministic Book Scan (`scripts/book_ops.py scan`)

For `.pdf`, `.epub`, `.md`, `.txt`, `.html`/`.htm` files, or directories of source files, run:

```bash
python3 scripts/book_ops.py scan --source <path> --workspace <dir> --max-words 1500
```

When the input includes a `.pdf` book, `scan` automatically extracts chapters (stripping running headers/footers and page numbers, reflowing hard-wrapped paragraphs), saves clean `<workspace>/converted_source/<stem>.txt` and `<workspace>/converted_source/<stem>.epub` working copies, and records both converted paths in `.book-scan-meta.json` and `source-map.md`. You can also run standalone conversion via `python3 scripts/book_ops.py convert --source <book.pdf> --out <book.epub> --also-out <book.txt>`.

`scan` sorts directory files naturally, detects chapter/section or EPUB spine boundaries, splits oversized units cleanly at paragraph boundaries (`\n\n`) without mid-paragraph breaks, materializes exact per-chunk source files under `<workspace>/source_chunks/<chunk_id>.md`, populates `source-map.md` and `chunk-manifest.csv` (`status=ready`), and records baseline chunk metrics (`source_words`, `source_chars`, `source_paragraphs`, `source_headings`, `source_tables`) in `<workspace>/.book-scan-meta.json`. When the source is a single `.epub` file, `scan` also archives `<workspace>/.source-template.epub` and maps each chunk to its exact DOM leaf-block range (`epub_href`, `epub_block_start`, `epub_block_end`) so `merge` can preserve original EPUB layout and styling verbatim.

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

## Phase 3: Research Terminology and Style

Research runs after the Source_Map exists and before chunk boundaries are finalized. Activate `core/workflows/d-research-module.md` to build the **Research_Dossier** (`core/schemas/research-dossier.md`) before chunk translation starts, combining:

- **Tier-1 Shared Memory Seeding**: Run `python3 scripts/book_ops.py sync-glossary --workspace <dir> --seed --target-lang <lang>` (if not already seeded by `init`) to import approved cross-book terms from `memory/glossary-<lang>.csv`, and load the target locale profile (such as `core/locales/vi-VN.md`).
- **Track A (Prior-Translation Harvesting)**: When existing translations exist, harvest canonical character names, toponyms, titles, worldbuilding/domain terms, and pronoun pairings, and log known mistranslations in `forbidden_translation` (paraphrased/attributed evidence only; never copy extended prose).
- **Track B (Authorial Intent and Transcreation Mindset)**: When no target translation exists (or for fresh adaptation), establish the historical/cultural context, authorial intent, 4-rung register ladder, and target-language transcreation mindset compass.

The full procedure — candidate term mining, term classification, source priority order, `d-research` integration, copyright rules, and the research stop rule — is defined in `core/workflows/terminology-research.md`.

Phase outputs:

- **Research_Dossier** (`research-dossier.md`) plus telemetry in `evidence-ledger.jsonl` and `research-coverage.json`.
- **Glossary** containing at minimum the seeded and proposed core terms, each with evidence and confidence (schema: `core/schemas/glossary.md`).
- **Initial Style_Sheet** covering register, dialogue conventions, terms of address, and adaptation rules discovered so far (schema: `core/schemas/style-sheet.md`).
- High-impact unresolved terms recorded in the Unresolved_Issues_Log by the Coordinator.

If the platform supports subagents, the terminology-researcher and style-researcher roles may be dispatched in this phase under the **research-tier gate** (see `core/workflows/subagents.md`): Translation_Brief and Source_Map exist on disk, and the research units are recorded in a Subagent_Dispatch_Plan. Translation and review roles are never dispatched this early.

Do not block on low-impact terms: mark them provisional and continue (research stop rule).

---

## Phase 4: Plan (Context Plan and Chunking)

Create a **Context_Plan** (schema: `core/schemas/context-plan.md`) before finalizing chunk boundaries. The Context_Plan determines the effective chunk-size limits based on platform, model, and material class.

Split the work by **semantic units**, not arbitrary token count. Never split in the middle of a sentence, paragraph, table row, or single dialogue exchange.

If a semantic unit is too large for the Context_Plan's chunk-size limits, split at the next safest lower-level boundary.

### Chunk Boundary Preference Order

1. Chapter or article section
2. Scene or subsection
3. Paragraph group
4. Table / figure / caption group
5. Footnote / endnote group tied to its anchor

### Chunk Sizes and Resizing

Chunk-size presets per context mode and material class are defined once in `core/schemas/context-plan.md` (Suggested Chunk Size Presets). The triggers that force a chunk below the Context_Plan maximum are defined once in `core/workflows/context-management.md` (Chunk Size Adjustment Rules). Do not duplicate those tables here — consult them when planning.

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

### Subagent Dispatch Plan

When work will be delegated — or delegation is simulated sequentially — create a **Subagent_Dispatch_Plan** (schema: `core/schemas/subagent-dispatch-plan.md`) at the end of Phase 4, before any translation dispatch. The plan records mode, worker assignments, scopes, dependencies, artifact slices, output contracts, and fallback policy. Even in sequential mode the plan is required to maintain the artifact contract and enable resume.

---

## Phase 5: Translate

Translation may run through dispatched Worker_Subagents (parallel or hybrid) or sequentially in the main agent thread. Both paths follow the same multi-pass procedure and the same artifact contract.

### Dispatch (When Subagents Are Available)

Do NOT dispatch any chunk-translator or reviewer before the **full readiness gate** passes — all of the following exist on disk: Translation_Brief, Source_Map, Glossary (with proposed core terms), Style_Sheet, Chunk_Manifest, Story_Bible or Domain_Map (as applicable), Context_Plan, and Subagent_Dispatch_Plan. (Researcher roles use the lighter research-tier gate defined in `core/workflows/subagents.md`.)

Dispatch rules:

- Paste the **Worker Contract Card** (`core/workflows/subagents.md`) at the top of every worker prompt — it re-anchors the binding rules at every dispatch.
- Assign each Worker_Subagent a disjoint scope from the role set: terminology research, style research, chunk translation, continuity review, fidelity review, or formatting review.
- Provide each worker only the relevant artifact slices and chunk text, not the full document.
- Never allow two workers to edit the same output file in parallel.
- Between parallel waves, synchronize newly discovered recurring terms posted to `<workspace>/glossary-inbox.jsonl` by running `python3 scripts/book_ops.py sync-glossary --workspace <dir>`, resolving any reported conflicts before dispatching the next wave.
- Enforce **Mandatory Peer Cross-Check**: no chunk transitions from `drafted` to `done` by the translator alone; `fidelity-reviewer` and `continuity-reviewer` cross-check completeness, boundary handshakes, pronoun/address consistency, and shared glossary adherence first.
- The Coordinator retains final authority over Glossary changes, Style_Sheet decisions, voice consistency, and continuity across chunks. Workers return proposals; only the Coordinator writes shared artifacts.

If the platform does not support parallel subagents, use `mode: sequential` in the Subagent_Dispatch_Plan and execute the same role responsibilities in sequence. See `core/workflows/subagents.md` for full orchestration details.

### Multi-Pass Procedure

Use the same four passes for each chunk. Do not skip passes.

### Pass A: Draft

Translate the chunk using the current Translation_Brief, Glossary, Style_Sheet, Story_Bible or Domain_Map, and adjacent Chunk_Summary entries.

**Rules:**

- Preserve all meaning-bearing details.
- Keep paragraph order unless the output format explicitly allows adaptation.
- Preserve numbers, names, citations, references, and quoted material with extra care.
- Do not resolve ambiguous terms by guessing — mark them for review and report them as `unresolved_items` (the Coordinator records them in the Unresolved_Issues_Log).

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

1. Write a compact **Chunk_Summary** for this chunk (used by adjacent chunks for continuity).
2. Collect Glossary proposals for new terms or changed decisions.
3. Collect Style_Sheet proposals for new decisions.
4. Collect continuity notes for the Story_Bible or Domain_Map.
5. Report QA issues, uncertain items, and follow-ups as `unresolved_items` in the structured return.
6. The Coordinator then reviews the return, writes accepted changes to the canonical artifacts, records `unresolved_items` in the Unresolved_Issues_Log, and updates the Chunk_Manifest status. In sequential mode the main agent performs both sides of this handoff, in the same order.

If a term in the chunk is ambiguous and no glossary entry resolves it, mark the term as uncertain in the chunk output and report it as an unresolved item instead of guessing.

---

## Phase 6: Merge and Final Voice Pass

After all assigned chunks have status `done` in the Chunk_Manifest:

### Merge Steps

1. **Deterministic verified assembly.** Run `python3 scripts/book_ops.py merge --workspace <dir> --out <output_path>` (supporting `.txt`, `.epub`, `.md`, or `--format both` to produce both clean `.txt` and valid `.epub`) to verify completeness and assemble all chunk outputs in exact `chunk-manifest.csv` order with a generated Table of Contents and Completeness Audit in `qa-report.md`. When the workspace was scanned from an `.epub` template (`.source-template.epub`), `.epub` output automatically uses Layout-Preserving EPUB Mode: all CSS stylesheets, fonts, images, cover art, OPF manifest/spine structure, and XHTML container tags/classes stay untouched while only translatable text blocks, `<title>`, `toc.ncx`/`nav.xhtml` chapter labels, and `<dc:language>` (plus `<dc:title>` if `--title` is supplied) are localized.
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

## Phase 7: QA Gates

After the merge and final voice pass, run `python3 scripts/book_ops.py verify --workspace <dir>` (which checks 100% manifest completeness, length/paragraph/heading parity, placeholder markers such as `[omitted]`, `[truncated]`, or unresolved task markers, unclosed code fences, and glossary compliance) alongside the eight mandatory QA gates defined in `core/workflows/qa-gates.md`: completeness, fidelity, terminology, target-language quality, continuity, numbers/formal-data, formatting, and residual-risk reporting.

- Every gate must pass or produce documented residual risks before delivery.
- Gates may also run incrementally after each major batch of chunks reaches `done`.
- The pass produces the **QA_Report** artifact (schema: `core/schemas/qa-report.md`), compiled by the Coordinator.

---

## Phase 8: Delivery

After all Phase 7 gates pass, promote durable high-confidence project terms (`status=approved`, `confidence=high`) back to Tier-1 shared memory:

```bash
python3 scripts/book_ops.py sync-glossary --workspace <dir> --promote --target-lang <lang>
```

Deliver the translated artifact plus a short translator note covering:

- Scope translated
- Assumptions made
- Unresolved issues (reference the Unresolved_Issues_Log)
- Terminology choices worth reviewing
- Known extraction or formatting limitations
- QA checks performed (reference the QA_Report)
- Skill version used for the work
- Residual risks

Do not include internal scratch notes unless the user asks for them.

Deliver only after every Phase 7 gate has passed or its residual risks are documented in the QA_Report.

---

## Summary of Artifacts Produced

| Artifact | Phase | Schema |
|---|---|---|
| Translation_Brief | Phase 1 | `core/schemas/translation-brief.md` |
| Source_Map | Phase 2 | `core/schemas/source-map.md` |
| Research_Dossier | Phase 3 | `core/schemas/research-dossier.md` |
| Glossary | Phase 3–5 | `core/schemas/glossary.md` |
| Style_Sheet | Phase 3–5 | `core/schemas/style-sheet.md` |
| Story_Bible / Domain_Map | Phase 2–5 | `core/schemas/story-bible.md` / `core/schemas/domain-map.md` |
| Context_Plan | Phase 4 (before final chunking) | `core/schemas/context-plan.md` |
| Chunk_Manifest | Phase 4–6 | `core/schemas/chunk-manifest.md` |
| Subagent_Dispatch_Plan | Phase 4 (before dispatch; research units may be added in Phase 3) | `core/schemas/subagent-dispatch-plan.md` |
| Chunk_Summary (per chunk) | Phase 5 (Pass D) | `core/schemas/chunk-summary.md` |
| Unresolved_Issues_Log | Throughout (written by the Coordinator) | `core/schemas/unresolved-issues.md` |
| QA_Report | Phase 7 | `core/schemas/qa-report.md` |
