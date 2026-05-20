# Context Plan

## Identification
- skill_version: 0.3.0
- platform: Claude Code
- model_or_agent: claude-sonnet-4 (assumed)
- known_context_window: 200k tokens (platform stated)

## Budget
- effective_context_budget: ~150k tokens (after system prompt + tool overhead + 10% safety)
- reserved_input_budget: 65% (source + artifact slices)
- reserved_output_budget: 20% (translation + revision)
- reserved_qa_budget: 10% (source-compare + uncertainty handling)
- safety_margin: 10%

## Material
- source_material_class: fiction
- context_mode: standard
- max_source_words_per_chunk: 1,200

## Slicing
- artifact_slice_policy: |
    Glossary slice: rows for terms appearing in current chunk + global recurring terms (top 20).
    Style_Sheet slice: rules tagged for "fiction" and "dialogue".
    Story_Bible slice: characters, places, and timeline entries appearing in chunk + adjacent scene continuity.
    Chunk_Summaries: previous and next only.
    Unresolved_Issues: scoped to current chunk, character, or term.

## Concurrency
- max_parallel_workers: 2

## Fallback Triggers
- Glossary slice for a chunk exceeds 1,500 tokens.
- Story_Bible excerpt for a chunk exceeds 1,200 tokens.
- Source-compare requires loading more than two adjacent chunk outputs.
- Worker returns context_pressure: true.
- Output draft exceeds 30% of effective budget.
- Platform truncation event observed.

## Notes
- Adjacent fiction scenes will not be dispatched in parallel until voice is stable after scene 1.
- Reduce to conservative mode if any worker returns context_pressure twice in a row.
- This is a short fiction piece (3 scenes); hybrid mode with terminology research first, then sequential scene translation is preferred to avoid voice drift.
