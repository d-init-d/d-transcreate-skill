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
- source_material_class: legal
- context_mode: conservative
- max_source_words_per_chunk: 500

## Slicing
- artifact_slice_policy: |
    Glossary slice: rows for legal terms appearing in current chunk + global defined terms.
    Style_Sheet slice: rules for legal prose, citation format, and numbering conventions.
    Domain_Map slice: defined terms, statutory references, and cross-references in chunk.
    Chunk_Summaries: previous and next only.
    Unresolved_Issues: scoped to current chunk or related defined term.

## Concurrency
- max_parallel_workers: 1

## Fallback Triggers
- Glossary slice for a chunk exceeds 2,000 tokens.
- Domain_Map excerpt for a chunk exceeds 1,500 tokens.
- Source-compare cannot fit source + target + glossary slice in one pass.
- Output draft exceeds reserved output budget.
- Worker returns context_pressure: true.
- Chunk contains cross-references to more than 5 other sections.

## Notes
- Legal text requires maximum fidelity; no creative adaptation.
- Context window unknown; using conservative mode with sequential execution.
- Defined terms must be translated identically throughout; glossary is critical.
- Reduce max_source_words_per_chunk to 350 if any chunk triggers a fallback.
