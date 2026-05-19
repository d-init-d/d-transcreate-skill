# Style Sheet

## Voice

### Register
Formal-technical: professional documentation tone suitable for a product manual. Clear, direct, and instructional without being academic or overly casual.

### Formality
High formality with full verb forms. No contractions, no slang. Use complete sentences in procedural instructions.

### Sentence Rhythm
Prefer short-to-medium sentences (15–25 words). Break complex English compound sentences into multiple Vietnamese sentences when doing so improves clarity. Keep procedural steps as single imperative sentences.

### Genre Constraints
Maintain dry, precise technical prose. Avoid metaphor and humor. Prioritize clarity and scannability over literary style. Use parallel structure in lists and tables.

### Notes
Technical documentation readers scan rather than read linearly. Short paragraphs and clear topic sentences aid comprehension. Vietnamese technical prose tends toward shorter sentences than English equivalents.

---

## Language Conventions

### Dialogue Punctuation
N/A — no dialogue in technical documentation.

### Titles and Headings
Preserve original heading hierarchy and numbering. Translate heading text into Vietnamese but keep product names, CLI commands, and code identifiers in English within headings.

### Names
Keep all product names, tool names, service names, and technology names in their original English form: StreamForge, sfctl, Kubernetes, Docker, Helm, Prometheus, BigQuery, Kafka.

### Terms of Address
Use impersonal constructions ("cần đảm bảo", "thực hiện lệnh sau") rather than second-person address. Where direct address is unavoidable, use "bạn" (informal-neutral, standard in Vietnamese tech docs).

### Honorifics
N/A — technical documentation does not use honorifics.

### Number, Date, and Unit Conventions
Use international notation for numbers (dot as decimal separator, comma as thousands separator is acceptable but not required). Keep storage units in English notation: GB, MB, Gi, Mi. Keep duration notation as-is: `30s`, `15m`. Do not convert units.

### Citation Conventions
N/A — no academic citations in this material.

### Footnote and Translator-Note Policy
No translator notes needed for this material. If a concept requires cultural explanation, add a brief parenthetical gloss inline rather than a footnote.

### Notes
Vietnamese technical documentation conventions follow international software documentation standards closely. The community has established strong conventions for DevOps and cloud-native terminology through Kubernetes Vietnamese localization efforts.

---

## Adaptation Rules

### Idioms
N/A — source material does not contain idiomatic expressions.

### Humor
N/A — source material does not contain humor.

### Cultural References
N/A — source material does not contain culture-specific references.

### Metaphors
Translate conceptual metaphors literally when they are standard in computing (e.g., "pipeline", "pool", "sink"). These are established technical metaphors understood internationally.

### Repetition
Preserve deliberate repetition of technical terms for consistency. Do not vary terminology for stylistic reasons — consistency is more important than variety in technical documentation.

### Songs, Poems, and Quoted Material
N/A — no such material in this source.

### Notes
Technical documentation prioritizes precision and consistency over stylistic variation. Every instance of a term should use the same translation as recorded in the glossary.

---

## Forbidden Patterns

| Pattern | Reason |
|---------|--------|
| Translating code blocks, CLI commands, or YAML content | Code must remain executable; translation would break functionality |
| Using "phát triển" for "deployment" | "Phát triển" means "development"; correct term is "triển khai" |
| Mixing Vietnamese and English mid-word (e.g., "các pipeline-s") | Unnatural; use "các pipeline" without English plural suffix |
| Translating established English loanwords (pipeline, connector, worker pool, backpressure) | These terms are used as-is in Vietnamese technical community |
| Using overly academic Vietnamese for simple technical concepts | Target audience prefers direct, practical language over formal academic register |
| Adding explanatory content not present in the source | Fidelity requirement: do not add information the author did not include |
| Translating environment variable names or configuration keys | These are code identifiers that must remain unchanged for functionality |

### Notes
The forbidden patterns above protect both the technical accuracy and the usability of the translated documentation. Code-adjacent content must remain in English to preserve functionality.
