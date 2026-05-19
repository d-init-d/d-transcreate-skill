# Technical Domain Workflow

Use this workflow when the source material is classified as technical, legal, medical,
financial, academic, product, or policy material. It governs the creation and ongoing
maintenance of the **Domain_Map** artifact and defines rules for handling acronyms,
units, standards, and citations throughout the translation.

## When to Activate

Activate this workflow during Phase 2 (Whole-Document Scan) when the source matches
any of these material classes:

- Technical documentation (APIs, manuals, specifications, engineering)
- Legal material (contracts, statutes, regulations, compliance)
- Medical or pharmaceutical content (clinical, regulatory, patient-facing)
- Financial material (reports, filings, audits, prospectuses)
- Academic content (papers, theses, textbooks, curricula)
- Product documentation (user guides, release notes, knowledge bases)
- Policy material (internal policies, government policy, standards bodies)

If the material class is ambiguous, default to activating this workflow when the source
contains domain-specific terminology, regulatory references, or formal data conventions
that require consistent handling.

## Domain Map Creation

### Initial Population (Phase 2)

During the whole-document scan, capture the following in the Domain_Map:

1. **Domain field** — the primary discipline and any relevant subdisciplines.
2. **Audience expertise** — the expected reader's technical level (expert, practitioner, informed layperson, general public).
3. **Governing standards or laws** — any standards (ISO, IEEE, RFC, W3C), laws, regulations, or frameworks the source references or must comply with.
4. **Canonical sources** — authoritative references for terminology in the target language (official translations of standards, regulatory body glossaries, publisher style guides, professional association terminology databases).
5. **Concepts** — domain-specific concepts with their definitions and preferred target-language translations.
6. **Acronyms** — every acronym or initialism found, with expansion, translation policy, and usage notes.
7. **Units and formal-data conventions** — measurement systems, date formats, number notation, currency conventions, and any conversion rules specified in the Translation_Brief or Style_Sheet.

### Schema Reference

The Domain_Map artifact follows the schema defined in `core/schemas/domain-map.md`.

## Domain Map Maintenance

### Per-Chunk Updates (Pass D)

After translating each chunk, update the Domain_Map:

1. **New concepts** — if a chunk introduces a concept not yet recorded, add it with definition, preferred translation, and source evidence before completing the chunk.
2. **New acronyms** — if a chunk introduces an acronym not yet recorded, add it with expansion and translation policy before completing the chunk.
3. **Refinements** — if translation reveals that an existing entry needs clarification, a better translation, or additional context, update the entry and note the chunk where the change originated.
4. **Cross-references** — if a concept relates to another concept already in the map, note the relationship.

### Consistency Enforcement

When a chunk references a concept or acronym already present in the Domain_Map:

- Apply the preferred translation recorded there.
- Do not introduce variant translations without updating the Domain_Map entry.
- If the source uses the term in a new sense not covered by the existing entry, flag it in the Unresolved_Issues_Log and propose a Domain_Map update rather than silently diverging.

## Acronym Handling

### Translation Policy Categories

Each acronym entry in the Domain_Map must specify one of these policies:

| Policy | Rule | Example |
|--------|------|---------|
| **retain** | Keep the source-language acronym unchanged in the target text. | API, HTTP, DNA, SQL |
| **translate** | Replace with the target-language equivalent acronym or term. | UN → LHQ (Vietnamese) |
| **expand-first** | Spell out on first occurrence in each chapter/section, then use the short form. | GDPR (General Data Protection Regulation) → first use expanded, then GDPR |
| **dual** | Show both source acronym and target expansion on first use, then source acronym only. | WHO (Tổ chức Y tế Thế giới) → WHO |
| **context-dependent** | Policy varies by audience or section; document the rule per context. | — |

### Decision Criteria

When deciding acronym policy:

1. If the target audience routinely uses the source-language acronym (e.g., IT professionals using "API"), prefer **retain**.
2. If an official target-language equivalent exists and is widely recognized, prefer **translate**.
3. If the acronym is unfamiliar to the target audience, prefer **expand-first** or **dual**.
4. Record the decision rationale in the Domain_Map notes column.

## Units and Formal Data

### Conversion Rules

Unit and formal-data conversions are applied **only** when explicitly specified in the
Translation_Brief or Style_Sheet. The agent does not convert units by default.

When conversions are specified:

1. Record the conversion rule in the Domain_Map (e.g., "Convert imperial to metric; retain original in parentheses").
2. Apply the rule consistently across all chunks.
3. Preserve the original value alongside the converted value when the Translation_Brief or Style_Sheet requires it.
4. Verify converted values for mathematical accuracy during Pass B (source-compare).

### Number Notation

Follow the target-locale conventions documented in the Style_Sheet for:

- Decimal separators (period vs. comma)
- Thousands separators (comma, period, thin space, or none)
- Percentage notation (50% vs. 50 %)
- Large-number abbreviation conventions

### Date and Time Formats

- Apply the target-locale date format specified in the Style_Sheet.
- Preserve the underlying date value exactly; only the display format changes.
- When timezone information is present, retain it unless the Translation_Brief specifies conversion.

### Currency

- Retain original currency codes and amounts unless the Translation_Brief specifies conversion.
- When conversion is specified, document the exchange rate or conversion rule in the Domain_Map and apply it consistently.

## Standards and Regulatory References

### Preservation Rules

1. **Standard identifiers** — preserve exactly as written (e.g., ISO 9001:2015, RFC 2119, 21 CFR Part 11). Do not translate standard numbers or codes.
2. **Law and regulation citations** — preserve the original citation format. If a target-language equivalent citation exists and is specified in the Translation_Brief, provide both.
3. **Section and clause references** — preserve numbering exactly (e.g., "Section 4.2.1", "Article 12(3)(b)").
4. **Version numbers and release identifiers** — preserve exactly.

### Target-Language Equivalents

When the Translation_Brief or Domain_Map specifies that a standard has an official target-language equivalent:

1. Use the official target-language title on first reference.
2. Include the original identifier in parentheses on first reference.
3. Use the short form (original identifier) in subsequent references.
4. Record the mapping in the Domain_Map.

## Citation Preservation

### General Rules

1. **Bibliographic citations** — preserve author names, publication years, titles, journal names, volume/issue/page numbers, DOIs, and URLs exactly as they appear in the source.
2. **In-text citation markers** — preserve the citation style (numbered, author-year, footnote) and numbering/labeling exactly.
3. **Cross-references** — preserve internal reference labels (Figure 1, Table 3, Equation 2.1, Section 4.3) exactly. Translate only the reference-type word (e.g., "Figure" → target equivalent) while keeping the number unchanged.
4. **URLs and URIs** — preserve exactly; do not translate URL paths or query parameters.
5. **Code identifiers** — preserve variable names, function names, class names, file paths, command-line arguments, and API endpoints exactly as written.
6. **Equation labels** — preserve equation numbering and any label identifiers exactly.

### Footnotes and Endnotes

- Preserve footnote/endnote numbering and anchor positions.
- Translate footnote content but preserve any citations, URLs, or formal references within them.
- If the source uses author footnotes vs. translator footnotes, maintain the distinction.

## Integration with QA Gates

The following QA gates (defined in `core/workflows/qa-gates.md`) have heightened
importance for technical/domain material:

- **Terminology gate** — verify that Domain_Map preferred translations are applied consistently and that no forbidden translations appear.
- **Numbers and formal data gate** — verify that underlying values, identifiers, citations, URLs, code identifiers, equation labels, and table references match the source exactly; verify that any format conversions follow documented rules.
- **Fidelity gate** — pay special attention to modality (shall/should/may), causality, and claims that carry regulatory or legal weight.
- **Completeness gate** — verify that all tables, figures, appendices, references, and cross-references are accounted for.

For high-stakes legal, medical, financial, academic, or safety material:

- Require source-backed terminology decisions (confidence = high, with evidence).
- Include explicit residual-risk notes in the QA_Report for any term with confidence < high.
- Flag any unit conversion, date conversion, or formal-data transformation for manual verification.

## Relationship to Other Artifacts

| Artifact | Relationship |
|----------|-------------|
| **Translation_Brief** | Specifies domain, audience, conversion rules, and quality bar |
| **Source_Map** | Technical extensions (domain, standards, acronyms, units) feed initial Domain_Map |
| **Glossary** | Domain_Map concepts inform glossary entries; glossary tracks translation decisions |
| **Style_Sheet** | Records number/date/unit/citation format conventions referenced by this workflow |
| **Chunk_Manifest** | Chunks may have status `research-needed` when new domain concepts require investigation |
| **Unresolved_Issues_Log** | Receives entries when domain terms cannot be resolved with high confidence |
| **QA_Report** | Reports domain-specific checks and residual risks |
