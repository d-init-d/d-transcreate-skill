# Fiction Continuity Workflow

This workflow governs Story Bible creation, maintenance, and application for fiction and narrative material. It applies whenever the source is classified as fiction, memoir, narrative non-fiction, script, game, or comic.

## When This Workflow Applies

Activate this workflow when the Source_Map classifies the material as any of:

- Novel, novella, short-story collection
- Memoir or narrative non-fiction
- Screenplay, stage play, radio drama
- Game narrative (visual novel, RPG script, interactive fiction)
- Comic, manga, graphic novel
- Any hybrid document whose primary mode is storytelling

If the material is technical, legal, medical, financial, academic, product, or policy, use `core/workflows/technical-domain.md` instead.

## Story Bible Creation

During the whole-document scan (Phase 2), build the Story_Bible artifact using the schema defined in `core/schemas/story-bible.md`. The scan must capture:

- **Cast list**: every named or significant unnamed character
- **Relationships**: family, romantic, professional, adversarial, secret
- **Point of view per chapter/scene**: who narrates or focalizes
- **Timeline**: chronological events, flashbacks, time skips, parallel timelines
- **Locations**: named places, settings, spatial relationships
- **Motifs**: recurring symbols, phrases, imagery, thematic threads
- **Reveal structure**: twists, hidden facts, deferred information (see Reveal-Timing Rules below)

## Story Bible Tables

The Story_Bible must contain the following tables (see `core/schemas/story-bible.md` for full column definitions):

### Characters Table

Each character entry records:

| Field | Purpose |
|---|---|
| Name forms | Source name, transliterated form, chosen target-language form, nicknames, aliases |
| Voice | Speech register, dialect markers, verbal tics, formality level, idiolect notes |
| Relationships | Links to other characters with relationship type and visibility status |
| First appearance | Chapter/scene where the character is introduced |
| Arc notes | Key transformations relevant to translation choices |

### Timeline Events Table

Chronological record of plot events with chapter references, enabling the translator to verify temporal consistency across chunks.

### Places Table

Named locations with descriptions, cultural associations, and any translation decisions (transliterate vs. translate vs. adapt).

### Continuity Threads Table

Tracks ongoing narrative threads: foreshadowing, unresolved questions, promises to the reader, and callbacks. Each thread records its introduction point, resolution point (if known), and current status.

### Terms of Address Table

Records how characters address each other, including:

- Honorifics and their target-language equivalents
- Shifts in address that signal relationship changes
- Formal/informal register per relationship pair
- Cultural adaptation decisions (e.g., source honorific system mapped to target conventions)

## Reveal-Timing Rules

These rules prevent the translation from exposing information before the source does.

### Principle

The target text must not reveal a hidden relationship, gender, twist, identity, or worldbuilding fact earlier than the source text reveals it. The translator must choose wording that preserves ambiguity where the source is ambiguous.

### Procedure

1. **During scan**: identify every deferred reveal in the source. Record each in the Story_Bible continuity threads table with:
   - What is hidden (the fact)
   - Where it is hidden (chapters/scenes that must remain ambiguous)
   - Where it is revealed (the reveal point)
   - Linguistic markers in the source that maintain ambiguity (e.g., gender-neutral pronouns, vague descriptions)

2. **During chunk translation**: before translating any chunk that falls within a hidden-fact zone, load the relevant continuity thread rows. Choose target-language constructions that:
   - Avoid gendered pronouns if the source conceals gender
   - Avoid naming a relationship if the source uses indirection
   - Avoid clarifying a timeline if the source deliberately obscures sequence
   - Preserve misdirection if the source employs deliberate red herrings

3. **After the reveal point**: once the source has disclosed the fact, the translator may use explicit target-language forms freely in subsequent chunks.

4. **Edge cases**:
   - If the target language grammatically forces a reveal (e.g., gendered verb agreement), record the conflict in the Unresolved_Issues_Log and propose the least-revealing alternative.
   - If no satisfactory ambiguous construction exists, flag the issue for human review before finalizing.

## Character Voice Consistency

### Principle

Each character's speech must sound distinctly like that character across all chunks, regardless of which worker or session translates them.

### Procedure

1. **During scan**: for each significant character, note in the Story_Bible:
   - Register (formal, casual, vulgar, archaic, etc.)
   - Sentence patterns (short/clipped, verbose, rhetorical questions, etc.)
   - Verbal tics or catchphrases
   - Dialect or sociolect markers
   - How their voice changes under stress, intimacy, or authority

2. **During chunk translation**: when a character speaks or focalizes, load their voice entry from the Story_Bible. Match the target-language register and patterns to the documented profile.

3. **Cross-chunk consistency check**: during the merge and final voice pass (Phase 6), verify that no character's voice drifts between chunks translated by different workers or sessions.

4. **Voice evolution**: if a character's voice intentionally changes (e.g., a child growing up, a character code-switching), record the transition point in the Story_Bible and ensure the shift appears at the correct chapter boundary.

## Terms of Address

### Principle

How characters address each other carries relationship information, power dynamics, and cultural context. Translation must preserve these signals consistently.

### Procedure

1. **Map the source system**: identify the source language's address conventions (e.g., T-V distinction, honorific tiers, first-name vs. surname norms).

2. **Map the target system**: identify the target language's address conventions and determine the closest functional equivalents.

3. **Record decisions**: for each character pair, record in the Terms of Address table:
   - Source form used (e.g., "vous", "先生", first name)
   - Target form chosen (e.g., "anh/chị", "-san", formal "you")
   - Rationale for the mapping
   - Any shift points where address changes (and what triggers the shift)

4. **Apply consistently**: every chunk translator must consult the Terms of Address table before rendering dialogue or narration that involves direct address.

5. **Handle asymmetry**: when characters use different levels of formality toward each other (e.g., a student says "sensei" while the teacher uses the student's first name), preserve the asymmetry in the target language.

## Story Bible Maintenance

The Story_Bible is a living artifact updated throughout the translation process.

### When to Update

- After translating any chunk that introduces a new character, place, relationship, or motif
- After translating any chunk that resolves a continuity thread
- After translating any chunk that shifts a character's voice or address pattern
- When a continuity reviewer flags an inconsistency

### Update Procedure

1. The chunk translator (Pass D — state update) proposes additions or changes to the Story_Bible.
2. The coordinator reviews proposals for consistency with existing entries.
3. Approved changes are written to the Story_Bible file.
4. If a change contradicts an existing entry, the coordinator resolves the conflict and records the rationale.

### Loading Strategy

When translating a chunk, load only the Story_Bible rows relevant to that chunk:

- Characters who appear or are referenced in the chunk
- Continuity threads active in the chunk's timeline position
- Terms of address for character pairs present in the chunk
- Any reveal-timing constraints that apply to the chunk's position

Do not load the entire Story_Bible into context. See `core/workflows/context-management.md` for the full context budget rule.

## Integration with Other Workflows

- **Whole-document scan** (`core/workflows/long-document.md`): the scan phase populates the initial Story_Bible.
- **Terminology research** (`core/workflows/terminology-research.md`): character names and place names flow into the Glossary; the Story_Bible records the narrative context that informs naming decisions.
- **QA gates** (`core/workflows/qa-gates.md`): the continuity gate checks Story_Bible consistency across the final merged output.
- **Context management** (`core/workflows/context-management.md`): defines how much of the Story_Bible loads per chunk.
- **Subagents** (`core/workflows/subagents.md`): the continuity-reviewer role uses the Story_Bible as its primary reference artifact.
