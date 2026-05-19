# Research And Style Workflow

Use this file before translating specialized domains, fiction with established fandom terms, marketing copy, legal/technical material, or any work where popular translations and genre conventions matter.

## Research Goals

Research should answer:

- What are the canonical translations of names, terms, standards, products, laws, and titles?
- Which translations are common, official, outdated, disputed, or context-specific?
- What target-language register fits this genre and audience?
- What parallel texts show the expected sentence rhythm, heading style, dialogue style, or terminology pattern?
- Which sources justify each high-impact decision?

## Candidate Term Mining

Before web research, mine the source for:

- repeated nouns and noun phrases
- capitalized names, organizations, places, products, and works
- acronyms, abbreviations, symbols, and formulas
- chapter titles, headings, labels, UI strings, and table headers
- culture-specific concepts, idioms, slang, jokes, songs, poems, and slogans
- legal, medical, financial, academic, engineering, or safety terms
- fiction-specific terms: magic systems, ranks, titles, species, artifacts, organizations, attacks, places

Classify each candidate:

| Class | Examples | Handling |
|---|---|---|
| Must-research | laws, standards, product names, official titles | Verify before translating |
| Must-consist | named entities, recurring concepts, titles | Put in glossary |
| Contextual | idioms, jokes, metaphors, slang | Decide per passage, document pattern |
| Leave-as-source | trademarks, code identifiers, proper names | Add to do-not-translate list |
| Watchlist | ambiguous terms, polysemy, pronouns | Track unresolved cases |

## Using d-research

If `$d-research` is available, use it as the research layer for terminology, source discovery, and evidence quality.

Recommended prompts:

```text
Use $d-research to find official and common target-language translations for these source terms. Prefer primary sources, official localization, standards, laws, publisher pages, reputable glossaries, and high-quality bilingual references. Return a concise evidence ledger with source URL, term, candidate translation, confidence, and notes.
```

```text
Use $d-research to study target-language style conventions for this genre/domain. Find lawful public examples and summarize patterns for register, headings, sentence length, dialogue punctuation, terminology, and translator notes. Do not copy extended copyrighted text.
```

For multilingual research, ask `$d-research` to search in both source and target languages. Prefer original-language sources when verifying domain terms.

## Source Priority

Rank evidence in this order:

1. official localized source from the rights holder, publisher, standards body, regulator, product owner, or author
2. official bilingual law, standard, product documentation, API docs, glossary, or terminology database
3. established publisher edition or licensed translation
4. academic or professional glossary
5. reputable domain media or expert publication
6. high-quality community consensus with visible rationale
7. machine translation, AI output, unsourced lists, or scraped aggregations

When sources disagree, keep the conflict visible in the glossary notes and choose based on source quality, date, audience fit, and target-market convention.

## Learning From Popular Translations

Use existing translations to learn conventions, not to copy prose.

Allowed:

- identify official term choices
- compare title and name conventions
- observe punctuation, register, paragraphing, and translator-note patterns
- quote only short excerpts when legally and policy-compliant
- paraphrase style principles in your own words

Avoid:

- reproducing long passages from copyrighted translations
- translating by patching together existing translations
- treating fan translations as authoritative without verification
- hiding the influence source when a term choice depends on it

## Glossary Decision Rules

Each important term should have:

- source term
- preferred translation
- forbidden or deprecated translations when needed
- part of speech or term class
- context or chapter where it appears
- rationale
- source or evidence note
- confidence level
- status: proposed, approved, needs-review, deprecated

Prefer stable terms over clever one-off choices. For fiction, preserve reveal timing. Do not choose a translation that exposes a hidden relationship, gender, twist, or worldbuilding fact earlier than the source.

## Style Sheet Decision Rules

Capture target-language style decisions:

- register and formality
- sentence rhythm and paragraph density
- dialogue punctuation
- terms of address and pronoun hierarchy
- honorifics and titles
- humor and idiom adaptation strategy
- handling of metaphors, repetition, and rhetorical parallelism
- title and heading capitalization
- date, number, unit, and currency format
- footnote and translator-note policy

For literary work, include voice constraints:

- narrator distance
- interiority level
- lyricism vs plainness
- archaic, colloquial, regional, or technical flavor
- recurring verbal tics
- how much ambiguity to preserve

## Research Stop Rule

Stop research when one of these is true:

- official/canonical translation is found and confirmed
- two or more high-quality independent sources converge
- added searching yields no new candidates
- the term is low impact and can be marked as provisional
- the user asks to prioritize speed over research depth

Do not block translation indefinitely on low-impact terms. Mark them and continue.
