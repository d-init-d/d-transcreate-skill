# Chunk Summary Schema

## Purpose

A Chunk Summary is a compact record written after each chunk's translation is complete (Pass D — state update). It serves two functions:

1. **Context continuity** — When translating the next chunk, the agent loads the previous and next Chunk Summary entries instead of the full translated text, keeping context usage minimal.
2. **Resumability** — After a context reset or session interruption, Chunk Summaries allow the agent to reconstruct narrative or argumentative continuity without re-reading completed chunks.

## Format

The file `chunk-summaries.md` contains one repeating Markdown block per chunk. Each block is identified by its `chunk_id` (matching the Chunk Manifest).

## Schema

```markdown
# Chunk Summaries

## <chunk_id>
- **Source range:** <start–end location in source document (e.g., "pp. 12–14", "ch03 ¶4–¶19")>
- **What happened / main argument:** <1–3 sentence summary of narrative events, thesis, or key content>
- **Terms introduced:** <comma-separated list of new terms first appearing in this chunk, with approved translations>
- **Continuity implications:** <facts, reveals, tone shifts, or state changes that downstream chunks must respect>
- **Unresolved issues:** <any open questions or uncertain decisions logged for this chunk (reference Unresolved Issues Log IDs if applicable)>
- **Next-chunk dependency:** <what the immediately following chunk needs to know from this chunk to maintain coherence>
```

## Field Definitions

| Field | Required | Description |
|---|---|---|
| `chunk_id` | Yes | Stable identifier matching the Chunk Manifest (e.g., `ch03-sec02`, `p012-018`). |
| Source range | Yes | Human-readable location in the source document. Must be precise enough to locate the original text. |
| What happened / main argument | Yes | Concise summary (1–3 sentences). For fiction: plot events, character actions, emotional beats. For non-fiction: thesis, evidence presented, conclusions drawn. |
| Terms introduced | Yes (may be "None") | New glossary-relevant terms that first appear in this chunk, paired with their approved translations. Enables the next chunk's translator to use them consistently. |
| Continuity implications | Yes (may be "None") | Any fact, reveal, tone shift, relationship change, or state change that later chunks must respect. For fiction: foreshadowing planted, secrets revealed, POV shifts. For technical: definitions established, constraints introduced, cross-references created. |
| Unresolved issues | Yes (may be "None") | Open questions or uncertain translation decisions. Reference Unresolved Issues Log entry IDs when available. |
| Next-chunk dependency | Yes (may be "None") | Specific information the immediately following chunk needs for coherence — e.g., a sentence left mid-thought, a dialogue exchange continuing, a list that spans chunks, or a pronoun whose antecedent is in this chunk. |

## Example

```markdown
# Chunk Summaries

## ch01-sec01
- **Source range:** pp. 1–4, Chapter 1 "The Arrival" ¶1–¶12
- **What happened / main argument:** Protagonist Mira arrives at the coastal town of Dunhaven by train. She observes the decayed station and recalls her grandmother's letters. A stranger offers to carry her bag; she refuses.
- **Terms introduced:** Dunhaven → Dunhaven (keep original), the Saltway → con đường Muối, Mrs. Fairweather → Bà Fairweather
- **Continuity implications:** Mira's grandmother is deceased (revealed obliquely — do not state death explicitly until ch03). The stranger is not named yet — will be identified as Oren in ch01-sec03.
- **Unresolved issues:** None
- **Next-chunk dependency:** Mira is standing outside the station with her suitcase, looking toward the harbor. Next chunk opens mid-description of the harbor view.

## ch01-sec02
- **Source range:** pp. 4–7, Chapter 1 "The Arrival" ¶13–¶25
- **What happened / main argument:** Mira walks to the harbor, describes the fishing boats and the lighthouse. She finds her grandmother's cottage locked and sits on the porch to wait.
- **Terms introduced:** Widow's Light → Ngọn Hải Đăng Góa Phụ, the cottage → ngôi nhà nhỏ
- **Continuity implications:** The lighthouse name "Widow's Light" carries thematic weight — maintain the "widow" element in translation. The cottage key is missing — this becomes a plot point in ch02.
- **Unresolved issues:** UI-003 — "Widow's Light" translation: confirm with user whether to keep poetic register or use neutral geographic name.
- **Next-chunk dependency:** Mira is sitting on the porch at dusk. A light appears in the lighthouse (cliffhanger). Next chunk must open with her reaction to the light.
```

## Usage Rules

1. Write one Chunk Summary block immediately after completing Pass D (state update) for a chunk.
2. Keep summaries compact — they must fit in context alongside the Translation Brief, Glossary slice, Style Sheet rules, Story Bible / Domain Map excerpt, and the current source chunk.
3. When translating chunk N, load at minimum the summary for chunk N−1 (previous) and chunk N+1 (next, when available from the Source Map or a prior planning pass).
4. After a context reset, re-read the Chunk Manifest first, then load summaries for the chunks adjacent to the resumption point.
5. Do not include translated text in the summary — only metadata about what was translated and its implications.
