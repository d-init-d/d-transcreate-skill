# QA Gates

This workflow defines the eight mandatory QA gates that the Translation_Agent runs before final delivery. Every gate must pass or produce documented residual risks before the translated output is released.

Run these gates after the merge and final voice pass (Phase 7), or after each major batch when working incrementally.

## When to Run

- After the Coordinator_Subagent completes the merge and final voice pass.
- After each major batch of chunks reaches `done` status in the Chunk_Manifest.
- Before any delivery to the end user.

## Gate Sequence

The eight gates run in order. Each gate produces findings that feed into the QA_Report (see `core/schemas/qa-report.md`).

---

## Gate 1: Completeness

**Purpose:** Verify that nothing from the source was dropped or overlooked.

Check:

- Every source chunk in the Chunk_Manifest has translated output with status `done`.
- All headings, captions, footnotes, tables, lists, figures, appendices, references, and callouts are accounted for.
- No paragraph, bullet, row, subtitle, or speaker line is dropped.
- Repeated boilerplate is translated consistently.
- Placeholders, variables, code identifiers, formulas, citations, and URLs are preserved.

**Method:** Compare the Source_Map structure against the output structure. Every entry in the Source_Map must have a corresponding translated element.

---

## Gate 2: Fidelity

**Purpose:** Verify that the translation faithfully represents the source meaning.

Check for:

- Mistranslated negation.
- Changed causality.
- Changed chronology.
- Softened or strengthened claims.
- Incorrect modality (must, may, should, can, likely).
- Wrong speaker, subject, object, or referent.
- Lost irony, ambiguity, foreshadowing, or rhetorical emphasis.
- Added explanation not present in the source.
- Over-localization that changes meaning.

**Method:** For high-risk passages, perform paragraph-level source-target comparison. Flag any semantic drift.

---

## Gate 3: Terminology

**Purpose:** Verify that approved Glossary terms are applied consistently and forbidden translations do not appear.

Check:

- Glossary terms with status `approved` are applied consistently throughout.
- Forbidden translations recorded in the Glossary do not appear anywhere in the output.
- Official terms match source-backed decisions.
- Acronyms are expanded or retained according to the Style_Sheet.
- Names, titles, ranks, organizations, product names, laws, and standards are consistent.
- Ambiguous terms are resolved or listed in the Unresolved_Issues_Log.

**Fiction-specific:** Check terms of address, titles, pronouns, nicknames, and relationship markers against the Story_Bible.

---

## Gate 4: Target-Language Quality

**Purpose:** Verify that the output reads naturally for the target audience without sacrificing accuracy.

Check:

- Prose reads naturally for the target audience.
- Register stays consistent with the Style_Sheet.
- Sentence rhythm fits genre and voice.
- Dialogue sounds speakable.
- Technical sentences stay precise.
- Marketing or adaptation copy preserves intent and effect.
- Repeated motifs and rhetorical patterns remain recognizable.

**Caution:** Do not smooth every sentence if roughness is part of the source style. Preserve the author's voice.

---

## Gate 5: Continuity

**Purpose:** Verify internal consistency across the full translated document.

### For narrative work (fiction, memoir, script, game, comic):

- Names and aliases are consistent.
- Timeline is coherent.
- Locations are consistent.
- Relationships are accurately maintained.
- Point of view is preserved per chapter or scene.
- Character voice is distinct and consistent.
- Recurring objects and clues are tracked.
- Reveal timing is preserved (no early exposure of twists).
- Unresolved story threads are not accidentally closed or contradicted.

### For professional work (technical, legal, medical, financial, academic):

- Cross-references resolve correctly.
- Definitions are consistent with first use.
- Section numbering is sequential and correct.
- Terminology is introduced before use (or defined at first use).
- Consistency between executive summary, body, tables, and appendices.

---

## Gate 6: Numbers and Formal Data

**Purpose:** Verify that all numeric values, identifiers, and formal data match the source exactly, with format conversions applied only when explicitly documented.

Check:

- Numbers, dates, times, currencies, percentages, ranges, equations, and units match source values.
- Table row/column alignment is preserved.
- Labels, legends, figure numbers, and references are intact.
- Citations and bibliography entries are preserved exactly.
- Legal clauses, standards, article numbers, API names, and command names are unchanged.
- UI strings, placeholders, tags, variables, and markdown/HTML syntax are intact.
- Any format conversions applied (date format, unit conversion, currency conversion, number notation) follow conversion rules documented in the Translation_Brief or Style_Sheet.

**Rule:** Never "smooth" numbers or identifiers. Underlying values and identifiers must match the source exactly.

---

## Gate 7: Formatting

**Purpose:** Verify that the output format matches the user's request and structural elements survive translation.

Check:

- Output format matches the format specified in the Translation_Brief.
- Headings, hierarchy, lists, tables, footnotes, captions, and links survive.
- Bilingual layout stays aligned if requested.
- Markdown fences, XML/HTML tags, placeholders, and page references are intact.
- Document exports render cleanly when layout matters.

**Method:** Use visual or rendered checks for PDFs, DOCX, PPTX, and complex tables.

---

## Gate 8: Residual Risk Report

**Purpose:** Document remaining uncertainties and risks for the end user before final delivery.

Before final delivery, compile a concise residual risk list covering:

- Unresolved terminology (items still marked `needs-review` in the Glossary).
- Source extraction defects (OCR noise, missing pages, encoding issues from the Source_Map).
- Sources that could not be verified.
- High-impact ambiguous passages.
- Layout elements not preserved.
- Sections needing human domain review.

### High-stakes material

Where the source is high-stakes legal, medical, financial, academic, or safety material:

- Require source-backed terminology decisions (no provisional terms in final output).
- Include explicit residual-risk notes in the QA_Report.
- Flag any section where confidence is below `high` for human review.

**Rule:** Keep the report short and actionable. Do not expose scratch reasoning or internal process notes.

---

## QA_Report Artifact

After running all eight gates, produce a QA_Report artifact (schema: `core/schemas/qa-report.md`) summarizing:

- Scope of the QA pass (which chunks, which gates).
- Artifacts checked (Glossary, Style_Sheet, Story_Bible/Domain_Map, Chunk_Manifest).
- Checks performed per gate.
- Issues found (with severity, location, and resolution or escalation).
- Residual risks carried forward to delivery.

The QA_Report is the final artifact before delivery and must be persisted to the workspace alongside the translated output.

---

## Assigning QA Work to Subagents

When subagents are available, the Coordinator_Subagent may dispatch QA checks to specialized Worker_Subagents:

| Gate | Assignable to |
|------|---------------|
| Completeness | Formatting Reviewer |
| Fidelity | Fidelity Reviewer |
| Terminology | Terminology Researcher (verify mode) |
| Target-Language Quality | Coordinator (cannot delegate voice judgment) |
| Continuity | Continuity Reviewer |
| Numbers and Formal Data | Fidelity Reviewer or Formatting Reviewer |
| Formatting | Formatting Reviewer |
| Residual Risk Report | Coordinator (owns final delivery decision) |

Worker_Subagents performing QA write findings to the Unresolved_Issues_Log. The Coordinator_Subagent reviews findings, resolves what can be resolved, and compiles the final QA_Report.
