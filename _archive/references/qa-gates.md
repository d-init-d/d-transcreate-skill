# QA Gates

Use these gates before delivering a translation or after each major batch.

## Gate 1: Completeness

Check:

- every source chunk has translated output
- all headings, captions, footnotes, tables, lists, figures, appendices, references, and callouts are accounted for
- no paragraph, bullet, row, subtitle, or speaker line is dropped
- repeated boilerplate is translated consistently
- placeholders, variables, code identifiers, formulas, citations, and URLs are preserved

For documents, compare source map against output structure.

## Gate 2: Fidelity

Check for:

- mistranslated negation
- changed causality
- changed chronology
- softened or strengthened claims
- incorrect modality: must, may, should, can, likely
- wrong speaker, subject, object, or referent
- lost irony, ambiguity, foreshadowing, or rhetorical emphasis
- added explanation not present in source
- over-localization that changes meaning

For high-risk passages, do paragraph-level source comparison.

## Gate 3: Terminology

Check:

- glossary terms are applied consistently
- official terms match source-backed decisions
- forbidden translations do not appear
- acronyms are expanded or retained according to style sheet
- names, titles, ranks, organizations, product names, laws, and standards are consistent
- ambiguous terms are resolved or listed as unresolved

For fiction, check terms of address, titles, pronouns, nicknames, and relationship markers.

## Gate 4: Target-Language Quality

Check:

- prose reads naturally for the target audience
- register stays consistent
- sentence rhythm fits genre and voice
- dialogue sounds speakable
- technical sentences stay precise
- marketing/adaptation copy preserves intent and effect
- repeated motifs and rhetorical patterns remain recognizable

Avoid making every sentence smoother if roughness is part of the source style.

## Gate 5: Continuity

For narrative work, check:

- names and aliases
- timeline
- locations
- relationships
- point of view
- character voice
- recurring objects and clues
- reveal timing
- unresolved story threads

For professional work, check:

- cross-references
- definitions
- section numbering
- terminology introduced before use
- consistency between executive summary, body, tables, and appendices

## Gate 6: Numbers And Formal Data

Check:

- numbers, dates, times, currencies, percentages, ranges, equations, units
- table row/column alignment
- labels, legends, figure numbers, and references
- citations and bibliography entries
- legal clauses, standards, article numbers, API names, command names
- UI strings, placeholders, tags, variables, and markdown/HTML syntax

Never "smooth" numbers or identifiers.

## Gate 7: Formatting

Check:

- output format matches user request
- headings, hierarchy, lists, tables, footnotes, captions, and links survive
- bilingual layout stays aligned if requested
- markdown fences, XML/HTML tags, placeholders, and page references are intact
- document exports render cleanly when layout matters

Use visual or rendered checks for PDFs, DOCX, PPTX, and complex tables.

## Gate 8: Residual Risk Report

Before final delivery, list only useful residual risks:

- unresolved terminology
- source extraction defects
- sources that could not be verified
- high-impact ambiguous passages
- layout elements not preserved
- sections needing human domain review

Keep the report short. Do not expose scratch reasoning.
