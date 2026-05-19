# Terminology Research Workflow

This workflow governs how a Translation_Agent mines candidate terms from the source, discovers evidence-backed translations, integrates with `d-research-skill` when available, and populates the Glossary before chunk translation begins.

Load this file after the Source_Map is complete and before assigning any chunk for translation.

## Research Goals

Research should answer:

- What are the canonical translations of names, terms, standards, products, laws, and titles?
- Which translations are common, official, outdated, disputed, or context-specific?
- What target-language register fits this genre and audience?
- What parallel texts show the expected terminology pattern?
- Which sources justify each high-impact decision?

## Candidate Term Mining

Before web research, mine the source document (using the Source_Map) for:

- Repeated nouns and noun phrases
- Capitalized names, organizations, places, products, and works
- Acronyms, abbreviations, symbols, and formulas
- Chapter titles, headings, labels, UI strings, and table headers
- Culture-specific concepts, idioms, slang, jokes, songs, poems, and slogans
- Legal, medical, financial, academic, engineering, or safety terms
- Fiction-specific terms: magic systems, ranks, titles, species, artifacts, organizations, attacks, places

### Term Classification

Classify each candidate into one of the following classes:

| Class | Examples | Handling |
|---|---|---|
| Must-research | Laws, standards, product names, official titles | Verify before translating |
| Must-consist | Named entities, recurring concepts, titles | Put in Glossary immediately |
| Contextual | Idioms, jokes, metaphors, slang | Decide per passage, document pattern in Style_Sheet |
| Leave-as-source | Trademarks, code identifiers, proper names per brief | Add to do-not-translate list in Translation_Brief |
| Watchlist | Ambiguous terms, polysemy, pronouns | Track in Unresolved_Issues_Log until resolved |

## Source Priority Order

Rank evidence for term translations in this order (highest authority first):

1. **Official localized source** from the rights holder, publisher, standards body, regulator, product owner, or author
2. **Official bilingual document** — law, standard, product documentation, API docs, glossary, or terminology database
3. **Established publisher edition** or licensed translation
4. **Academic or professional glossary**
5. **Reputable domain media** or expert publication
6. **High-quality community consensus** with visible rationale
7. **Machine translation, AI output, unsourced lists, or scraped aggregations** (lowest confidence)

When sources disagree:

- Record both candidates with their evidence in the Glossary `notes` field.
- Choose based on source quality, publication date, audience fit, and target-market convention.
- Keep the conflict visible; do not silently discard the alternative.
- If the term is high impact and no high-confidence evidence is found, mark it `needs-review` and add it to the Unresolved_Issues_Log.

## d-research Integration

### When d-research-skill Is Available

If `d-research-skill` is accessible (installed as a sibling skill, present as a sibling repo or submodule, or explicitly enabled in configuration) AND the user has not disabled it in the Translation_Brief, delegate the following to `d-research`:

- Terminology source discovery (finding official and common target-language translations)
- Multilingual research (searching in both source and target languages)
- Evidence logging (structured evidence ledger with source URL, term, candidate, confidence, notes)
- Source-quality checks (ranking sources per the priority order above)

Recommended delegation prompts:

```text
Use $d-research to find official and common target-language translations for these source terms. Prefer primary sources, official localization, standards, laws, publisher pages, reputable glossaries, and high-quality bilingual references. Return a concise evidence ledger with source URL, term, candidate translation, confidence, and notes.
```

```text
Use $d-research to search in both source and target languages for canonical translations of [TERM_LIST]. Prefer original-language sources when verifying domain terms.
```

### When d-research-skill Is Not Available (Fallback Protocol)

If `d-research-skill` is not accessible or has been disabled, the Translation_Agent SHALL fall back to this protocol without blocking the translation workflow:

1. Use any available search or browsing tools provided by the agent platform.
2. If no search tools are available, rely on the agent's training knowledge and clearly mark confidence as `medium` or `low` for terms that cannot be verified against a live source.
3. Apply the Source Priority Order above to any evidence found.
4. Record the research method used (e.g., "agent knowledge only — no live search available") in the Glossary `evidence` column.
5. Mark unverified high-impact terms as `needs-review` in the Glossary and add them to the Unresolved_Issues_Log.

The translation workflow MUST NOT block on the absence of `d-research-skill`. The pack does not declare `d-research-skill` as a hard dependency.

## Copyright Rules for Evidence Quotes

When researching terminology and recording evidence in the Glossary or Style_Sheet, the following rules apply:

1. **No extended reproduction.** Do not reproduce extended passages from copyrighted translations.
2. **No patchwork translation.** Do not translate by patching together existing translations.
3. **Observation only.** Use existing translations only to identify official term choices, observe punctuation and register patterns, and paraphrase style principles in your own words.
4. **Short quotes with attribution.** When quoting from an existing translation for evidence, the excerpt must be short (a few words to one sentence maximum) and must include a source reference in the artifact notes.
5. **Disclose influence.** If a term choice depends on observation of an existing translation, record that influence source in the Glossary `notes` field rather than hiding it.

These rules protect against copyright infringement while allowing legitimate terminology research.

## Glossary Population Rules

For each important term discovered during research, create a Glossary row with:

| Field | Content |
|---|---|
| `term` | Source-language term exactly as it appears |
| `preferred_translation` | Best target-language translation based on evidence |
| `forbidden_translation` | Known incorrect or deprecated translations (if any) |
| `term_class` | Part of speech or domain class |
| `context` | Chapter, section, or passage where the term appears |
| `source_location` | File and line/page reference in the source |
| `evidence` | Source URL, document title, or research method used |
| `confidence` | `high`, `medium`, or `low` |
| `status` | `proposed`, `approved`, `needs-review`, or `deprecated` |
| `notes` | Rationale, alternative candidates, influence sources, conflicts |

### Decision Guidelines

- Prefer stable, widely recognized terms over clever one-off choices.
- For fiction, preserve reveal timing: do not choose a translation that exposes a hidden relationship, gender, twist, or worldbuilding fact earlier than the source.
- For technical material, prefer the term used in the governing standard or official documentation.
- When two high-quality sources disagree, record both and escalate to `needs-review` if the term is high impact.

## Research Stop Rule

Stop researching a term when one of these conditions is met:

1. An official or canonical translation is found and confirmed.
2. Two or more high-quality independent sources converge on the same translation.
3. Additional searching yields no new candidates.
4. The term is low impact and can be marked as provisional (`proposed` status, `medium` or `low` confidence) without blocking translation.
5. The user explicitly asks to prioritize speed over research depth.

Do not block translation indefinitely on low-impact terms. Mark them as provisional and continue. High-impact unresolved terms go to the Unresolved_Issues_Log.

## Schema Reference

- Glossary schema: `core/schemas/glossary.md`
- Unresolved Issues schema: `core/schemas/unresolved-issues.md`
- Translation Brief schema: `core/schemas/translation-brief.md`
