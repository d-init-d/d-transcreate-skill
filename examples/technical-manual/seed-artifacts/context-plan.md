# Context Plan

## Identification
- skill_version: 0.2.0
- platform: Generic
- model_or_agent: unknown
- known_context_window: unknown

## Budget
- effective_context_budget: conservative estimate (~80k tokens assumed)
- reserved_input_budget: 60% (source + artifact slices)
- reserved_output_budget: 25% (translation + revision)
- reserved_qa_budget: 10% (source-compare + uncertainty handling)
- safety_margin: 15%

## Material
- source_material_class: dense_technical
- context_mode: conservative
- max_source_words_per_chunk: 600

## Slicing
- artifact_slice_policy: |
    Glossary slice: rows for terms/acronyms appearing in current chunk + global high-frequency terms.
    Style_Sheet slice: rules for technical prose, tables, and code formatting.
    Domain_Map slice: acronyms, units, API identifiers, and standards referenced in chunk.
    Chunk_Summaries: previous and next only.
    Unresolved_Issues: scoped to current chunk or related domain concept.

## Concurrency
- max_parallel_workers: 1

## Fallback Triggers
- Glossary slice for a chunk exceeds 2,000 tokens.
- Domain_Map excerpt for a chunk exceeds 1,500 tokens.
- Source-compare cannot fit source + target + glossary slice in one pass.
- Output draft exceeds reserved output budget.
- Worker returns context_pressure: true.
- Chunk contains more than 3 tables requiring alignment verification.

## Notes
- Context window is unknown; using conservative mode with sequential execution.
- Dense technical content with many acronyms requires terminology researcher to complete before chunk translation begins.
- Tables and code blocks require formatting reviewer after merge.
- Reduce max_source_words_per_chunk to 400 if any chunk triggers a fallback.
