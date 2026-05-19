# Story Bible Schema

The Story Bible is the continuity-tracking artifact for fiction, memoir, narrative non-fiction, scripts, games, and comics. It records characters, timeline, places, continuity threads, and terms of address so that translation decisions remain consistent across chapters and do not inadvertently expose reveals, break voice, or create contradictions.

## When to Create

The Translation_Agent SHALL create and maintain a Story_Bible when the source is classified as fiction, memoir, narrative non-fiction, script, game, or comic (Requirement 9.1).

## Form

```markdown
# Story Bible

## Characters

| Character | Name forms | Voice | Relationships | Notes |
|---|---|---|---|---|

## Timeline

| Event | Source location | Time marker | Notes |
|---|---|---|---|

## Places

| Place | Translation | Description | Notes |
|---|---|---|---|

## Continuity Threads

| Thread | First seen | Later payoff | Translation risk |
|---|---|---|---|

## Terms of Address

| Speaker | Addressee | Source form | Target form | Rule |
|---|---|---|---|---|
```

## Table Definitions

### Characters

Tracks every named or significant character with enough detail to maintain consistent voice and naming across chunks.

| Column | Description | Example values |
|---|---|---|
| Character | Canonical identifier for the character | `Elara`, `The Narrator`, `Detective Kim` |
| Name forms | All name variants used in the source — full name, nickname, title, alias, pronoun patterns | `Elara Voss / Elara / "E" / Dr. Voss` |
| Voice | Distinctive speech patterns, register, dialect, verbal tics, or idiolect markers | `formal, clipped sentences, avoids contractions`, `teenage slang, sentence fragments` |
| Relationships | Key relationships to other characters relevant to translation choices | `sister of Maren; mentor to Jin; secretly married to Kael` |
| Notes | Translation-relevant notes — gender ambiguity, hidden identity, name etymology, reveal timing | `Gender not revealed until ch. 12 — use neutral forms until then` |

### Timeline

Tracks events in narrative order to prevent chronological contradictions in translation.

| Column | Description | Example values |
|---|---|---|
| Event | Brief description of the narrative event | `Elara arrives at the academy`, `The fire at the mill` |
| Source location | Chapter, section, or page where the event occurs | `ch03-sec01`, `p.47` |
| Time marker | In-story time reference (date, season, relative marker) | `spring of year 3`, `two days after the trial`, `dawn` |
| Notes | Translation-relevant notes — foreshadowing, unreliable narrator cues, parallel events | `Narrator says "weeks" but timeline implies days — preserve ambiguity` |

### Places

Tracks locations and their translated forms for consistency.

| Column | Description | Example values |
|---|---|---|
| Place | Source-language place name | `Thornfield`, `The Undercity`, `Rue de la Paix` |
| Translation | Chosen target-language form (translated, transliterated, or kept as-is) | `Thornfield` (keep), `Thành phố Ngầm` (translate), `Rue de la Paix` (keep) |
| Description | Brief description relevant to translation choices | `Fictional city; gothic atmosphere`, `Real Paris street` |
| Notes | Translation-relevant notes — naming conventions, cultural adaptation decisions | `Keep English name per client brief; add translator footnote on first occurrence` |

### Continuity Threads

Tracks narrative threads that span multiple chunks and carry translation risk — foreshadowing, hidden identities, motifs, recurring symbols, and delayed reveals.

| Column | Description | Example values |
|---|---|---|
| Thread | Name or description of the continuity thread | `The locked room motif`, `Kael's true parentage`, `The recurring dream` |
| First seen | Source location where the thread is introduced | `ch01-sec03`, `p.12` |
| Later payoff | Source location(s) where the thread resolves or recurs | `ch09-sec02, ch12-sec04` |
| Translation risk | What could go wrong if the translator is unaware of this thread | `Target pronoun system may reveal gender before ch.12 reveal`, `Wordplay on "key" lost if translated literally` |

### Terms of Address

Tracks how characters address each other — critical for languages with complex honorific or pronoun systems (e.g., Vietnamese, Japanese, Korean, Thai).

| Column | Description | Example values |
|---|---|---|
| Speaker | The character speaking | `Jin`, `Elara`, `Narrator` |
| Addressee | The character being addressed | `Elara`, `Jin's mother`, `The King` |
| Source form | The address form used in the source language | `you`, `ma'am`, `Your Majesty` |
| Target form | The chosen target-language address form | `chị` (Vietnamese), `ngài` (Vietnamese), `anh` |
| Rule | Rationale or condition governing this choice | `Jin is younger; shifts to first-name after ch.7 reconciliation`, `Formal until knighting scene` |

## Maintenance Rules

1. The Story_Bible is created during Phase 2 (Whole-Document Scan) with initial entries from the cast list, relationships, timeline, and locations detected in the source.
2. When a chunk introduces a new character, place, relationship, or motif, the Translation_Agent SHALL update the Story_Bible after translating that chunk (Requirement 9.5).
3. When a character is referenced in a chunk being translated, the Translation_Agent SHALL load the relevant Story_Bible rows into context for that chunk (Requirement 9.3).
4. When the source contains a hidden relationship, gender, twist, or worldbuilding fact revealed later, the Translation_Agent SHALL choose target-language wording that does not expose the reveal earlier than the source (Requirement 9.4).
5. The Coordinator_Subagent holds final authority over Story_Bible updates when subagents are active. Worker_Subagents propose updates; the coordinator approves.

## Usage

- The Story_Bible is persisted as a file in the workspace (`story-bible.md`) and is never stored only in chat history.
- During chunk translation, only the relevant rows are loaded into context (not the entire bible) to respect context budget constraints.
- The Continuity Reviewer subagent uses the Story_Bible as its primary reference when checking for timeline contradictions, voice drift, and premature reveals.
- The Story_Bible is referenced by the QA gates (continuity gate) during Phase 7.
