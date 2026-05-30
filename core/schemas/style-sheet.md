# Style Sheet Schema

The Style Sheet records all voice, register, and language-convention decisions for a translation project. It is produced during the Research phase (Phase 3) and consumed by every chunk translation pass, the merge/voice pass, and QA gates.

The Translation_Agent populates this artifact by researching target-language style conventions for the relevant genre or domain. Each non-trivial decision must include a rationale and source observation in the notes (style rationale).

**Copyright rule:** Existing translations may inform style observations only. Do not reproduce extended passages from copyrighted translations. Record paraphrased observations with short attributed evidence quotes.

---

## Template

```markdown
# Style Sheet

## Voice

### Register
<!-- e.g., literary, conversational, formal academic, journalistic, legal -->

### Formality
<!-- e.g., high formality with full verb forms; moderate with occasional contractions -->

### Sentence Rhythm
<!-- e.g., mirror source paragraph length; prefer short sentences for dialogue;
     allow complex subordination in exposition -->

### Genre Constraints
<!-- e.g., maintain noir tone; avoid modern slang in period fiction;
     preserve dry understatement in technical prose -->

### Notes
<!-- Rationale and source observations for voice decisions -->

---

## Language Conventions

### Dialogue Punctuation
<!-- e.g., use em-dash for dialogue opening (Vietnamese convention);
     use guillemets for inner quotes; comma before dialogue tag -->

### Titles and Headings
<!-- e.g., sentence case for chapter titles; preserve original numbering;
     translate subtitle but keep series name in source language -->

### Names
<!-- e.g., keep Western names in source form; transliterate non-Latin names;
     use target-language name order for East Asian names -->

### Terms of Address
<!-- e.g., map "you" to appropriate Vietnamese pronouns based on age/status;
     use "anh/chị/em" system; document speaker-addressee mapping -->

### Honorifics
<!-- e.g., retain "Dr." as "TS." or "Bác sĩ" depending on context;
     map "Mr./Mrs." to "Ông/Bà"; drop honorifics in informal dialogue -->

### Number, Date, and Unit Conventions
<!-- e.g., use dd/mm/yyyy; use metric units; use dot as thousands separator
     and comma as decimal separator; spell out numbers below 10 in prose -->

### Citation Conventions
<!-- e.g., preserve original citation format (APA/Chicago/legal);
     translate "ibid." to target equivalent; keep DOIs and URLs unchanged -->

### Footnote and Translator-Note Policy
<!-- e.g., translator notes in square brackets marked [ND];
     footnotes numbered continuously per chapter;
     cultural explanations as endnotes, not inline -->

### Notes
<!-- Rationale and source observations for language-convention decisions -->

---

## Adaptation Rules

### Idioms
<!-- e.g., replace with target-language equivalent idiom when natural;
     if no equivalent exists, paraphrase meaning and note in brackets -->

### Humor
<!-- e.g., preserve comedic timing over literal meaning;
     adapt wordplay to target-language pun when possible;
     if untranslatable, preserve tone and add translator note -->

### Cultural References
<!-- e.g., retain source reference with brief gloss if obscure;
     replace only when source reference is completely opaque to target audience
     and a natural equivalent exists -->

### Metaphors
<!-- e.g., preserve source metaphor when comprehensible in target;
     adapt vehicle only when source metaphor is dead/opaque in target culture -->

### Repetition
<!-- e.g., preserve deliberate rhetorical repetition;
     vary accidental repetition for target-language fluency -->

### Songs, Poems, and Quoted Material
<!-- e.g., provide faithful prose translation; preserve line breaks;
     do not attempt rhyme unless brief specifies creative adaptation;
     quoted material from published works: cite source, do not re-translate
     if official translation exists -->

### Notes
<!-- Rationale and source observations for adaptation decisions -->

---

## Forbidden Patterns

<!-- List patterns that must NOT appear in the target text.
     Each entry: pattern description + reason for prohibition. -->

| Pattern | Reason |
|---------|--------|
| <!-- e.g., "Translatorese" passive constructions --> | <!-- e.g., Unnatural in target language --> |
| <!-- e.g., Mixing formal/informal register mid-paragraph --> | <!-- e.g., Breaks voice consistency --> |
| <!-- e.g., Loan words when approved target equivalent exists --> | <!-- e.g., Glossary mandates target term --> |
| <!-- e.g., Literal calques of source idioms --> | <!-- e.g., Incomprehensible to target reader --> |

### Notes
<!-- Rationale for forbidden-pattern decisions -->
```

---

## Field Reference

| Section | Field | Description |
|---------|-------|-------------|
| Voice | Register | The linguistic register (literary, conversational, formal, etc.) |
| Voice | Formality | Degree of formality in grammar and vocabulary |
| Voice | Sentence rhythm | Sentence length and complexity preferences |
| Voice | Genre constraints | Style constraints imposed by genre or domain |
| Language Conventions | Dialogue punctuation | Punctuation marks and formatting for dialogue |
| Language Conventions | Titles and headings | Capitalization and formatting rules for headings |
| Language Conventions | Names | Transliteration and name-order policies |
| Language Conventions | Terms of address | Pronoun and address-form mapping rules |
| Language Conventions | Honorifics | How source honorifics map to target equivalents |
| Language Conventions | Number/date/unit conventions | Formatting rules for numbers, dates, and units |
| Language Conventions | Citation conventions | How citations and references are handled |
| Language Conventions | Footnote/translator-note policy | When and how translator notes are inserted |
| Adaptation Rules | Idioms | Strategy for translating idiomatic expressions |
| Adaptation Rules | Humor | Strategy for preserving or adapting humor |
| Adaptation Rules | Cultural references | Strategy for culture-specific references |
| Adaptation Rules | Metaphors | Strategy for translating figurative language |
| Adaptation Rules | Repetition | When to preserve vs. vary repeated elements |
| Adaptation Rules | Songs/poems/quoted material | Strategy for verse and quoted passages |
| Forbidden Patterns | (table) | Patterns explicitly prohibited in target output |

---

## Usage Notes

1. **Populate incrementally.** Not all fields apply to every project. Leave inapplicable fields blank or mark "N/A".
2. **Document rationale.** Each Notes sub-section captures why a decision was made and what source observation informed it (style rationale).
3. **Propose, don't overwrite.** Worker_Subagents propose Style_Sheet changes; only the Coordinator approves and writes final entries.
4. **Reference, don't inline.** Workflow and prompt files reference this schema by path (`core/schemas/style-sheet.md`); they do not duplicate its content.
5. **Keep living.** The Style_Sheet is updated during Pass D (state-update) of each chunk translation when new style decisions emerge.
