# Subagent Dispatch Plan

## Run Metadata
- run_id: legal-policy-example-01
- skill_version: 0.2.0
- coordinator: main-agent
- mode: sequential
- context_plan_ref: seed-artifacts/context-plan.md
- chunk_manifest_ref: chunk-manifest.md
- global_artifact_owner: coordinator
- max_parallel_workers: 1

## Policies
- merge_policy: Coordinator merges sections in source order after each completes.
- qa_policy: Fidelity review mandatory for every section; formatting review after merge for numbering and cross-references.
- fallback_policy: If chunk fails, reduce size to 350 words and retry. If repeated failure, flag for user intervention.

## Dispatch Units

### Unit: term-research-01
- unit_id: term-research-01
- role: terminology-researcher
- assigned_to: coordinator
- scope: All defined terms, statutory references, and legal concepts from the full policy document
- chunk_ids: []
- dependencies: []
- input_files: [source/privacy-policy.md]
- artifact_slices: [translation-brief.md, glossary.csv, domain-map.md]
- allowed_write_paths: [workspace/proposals/term-research-01.md]
- forbidden_write_paths: [glossary.csv, style-sheet.md, domain-map.md]
- output_contract: glossary_proposals with evidence, confidence, and legal authority source
- status: planned
- return_path: workspace/proposals/term-research-01.md

### Unit: translate-sec-01
- unit_id: translate-sec-01
- role: chunk-translator
- assigned_to: coordinator
- scope: Section 1 — Definitions and Scope (~450 words)
- chunk_ids: [sec-01-definitions]
- dependencies: [term-research-01]
- input_files: [source/section-01-definitions.md]
- artifact_slices: [glossary-slice, style-sheet, domain-map-slice]
- allowed_write_paths: [output/sec-01.md, workspace/summaries/sec-01.md]
- forbidden_write_paths: [glossary.csv, style-sheet.md, domain-map.md]
- output_contract: translated_text + glossary_proposals + chunk_summary + context_pressure
- status: planned
- return_path: output/sec-01.md

### Unit: translate-sec-02
- unit_id: translate-sec-02
- role: chunk-translator
- assigned_to: coordinator
- scope: Section 2 — Data Collection (~500 words)
- chunk_ids: [sec-02-collection]
- dependencies: [translate-sec-01]
- input_files: [source/section-02-collection.md]
- artifact_slices: [glossary-slice, style-sheet, domain-map-slice, prev-summary]
- allowed_write_paths: [output/sec-02.md, workspace/summaries/sec-02.md]
- forbidden_write_paths: [glossary.csv, style-sheet.md, domain-map.md]
- output_contract: translated_text + glossary_proposals + chunk_summary + context_pressure
- status: planned
- return_path: output/sec-02.md

### Unit: fidelity-review-01
- unit_id: fidelity-review-01
- role: fidelity-reviewer
- assigned_to: coordinator
- scope: Source-vs-target comparison for all sections (legal fidelity is critical)
- chunk_ids: [sec-01-definitions, sec-02-collection]
- dependencies: [translate-sec-01, translate-sec-02]
- input_files: [source/section-01-definitions.md, source/section-02-collection.md, output/sec-01.md, output/sec-02.md]
- artifact_slices: [glossary.csv, domain-map.md]
- allowed_write_paths: [workspace/reviews/fidelity-review-01.md]
- forbidden_write_paths: [glossary.csv, style-sheet.md, domain-map.md, output/sec-01.md, output/sec-02.md]
- output_contract: defect_list with chunk_id, paragraph, category, source_text, target_text, issue, severity
- status: planned
- return_path: workspace/reviews/fidelity-review-01.md
