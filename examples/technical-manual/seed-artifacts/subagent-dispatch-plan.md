# Subagent Dispatch Plan

## Run Metadata
- run_id: tech-manual-example-01
- skill_version: 0.3.0
- coordinator: main-agent
- mode: sequential
- context_plan_ref: seed-artifacts/context-plan.md
- chunk_manifest_ref: chunk-manifest.md
- global_artifact_owner: coordinator
- max_parallel_workers: 1

## Policies
- merge_policy: Coordinator merges sections in source order after each completes.
- qa_policy: Fidelity review per section; formatting review after merge (tables, code blocks, cross-references).
- fallback_policy: If chunk fails, reduce size to 400 words and retry. If repeated failure, flag for user intervention.

## Dispatch Units

### Unit: term-research-01
- unit_id: term-research-01
- role: terminology-researcher
- assigned_to: coordinator
- scope: All acronyms, API identifiers, units, and domain terms from sections 1-4
- chunk_ids: []
- dependencies: []
- input_files: [source/section-01-overview.md, source/section-02-installation.md, source/section-03-configuration.md, source/section-04-api-reference.md]
- artifact_slices: [translation-brief.md, glossary.csv, domain-map.md]
- allowed_write_paths: [workspace/proposals/term-research-01.md]
- forbidden_write_paths: [glossary.csv, style-sheet.md, domain-map.md]
- output_contract: glossary_proposals with evidence, confidence, and domain classification
- status: planned
- return_path: workspace/proposals/term-research-01.md

### Unit: translate-sec-01
- unit_id: translate-sec-01
- role: chunk-translator
- assigned_to: coordinator
- scope: Section 01 — Product Overview (~500 words)
- chunk_ids: [sec-01]
- dependencies: [term-research-01]
- input_files: [source/section-01-overview.md]
- artifact_slices: [glossary-slice, style-sheet, domain-map-slice, prev-summary]
- allowed_write_paths: [output/sec-01.md, workspace/summaries/sec-01.md]
- forbidden_write_paths: [glossary.csv, style-sheet.md, domain-map.md]
- output_contract: translated_text + glossary_proposals + continuity_notes + chunk_summary + context_pressure
- status: planned
- return_path: output/sec-01.md

### Unit: translate-sec-02
- unit_id: translate-sec-02
- role: chunk-translator
- assigned_to: coordinator
- scope: Section 02 — Installation Guide (~600 words, includes code blocks)
- chunk_ids: [sec-02]
- dependencies: [translate-sec-01]
- input_files: [source/section-02-installation.md]
- artifact_slices: [glossary-slice, style-sheet, domain-map-slice, prev-summary]
- allowed_write_paths: [output/sec-02.md, workspace/summaries/sec-02.md]
- forbidden_write_paths: [glossary.csv, style-sheet.md, domain-map.md]
- output_contract: translated_text + glossary_proposals + continuity_notes + chunk_summary + context_pressure
- status: planned
- return_path: output/sec-02.md

### Unit: translate-sec-03
- unit_id: translate-sec-03
- role: chunk-translator
- assigned_to: coordinator
- scope: Section 03 — Configuration (~550 words, includes tables)
- chunk_ids: [sec-03]
- dependencies: [translate-sec-02]
- input_files: [source/section-03-configuration.md]
- artifact_slices: [glossary-slice, style-sheet, domain-map-slice, prev-summary]
- allowed_write_paths: [output/sec-03.md, workspace/summaries/sec-03.md]
- forbidden_write_paths: [glossary.csv, style-sheet.md, domain-map.md]
- output_contract: translated_text + glossary_proposals + continuity_notes + chunk_summary + context_pressure
- status: planned
- return_path: output/sec-03.md

### Unit: translate-sec-04
- unit_id: translate-sec-04
- role: chunk-translator
- assigned_to: coordinator
- scope: Section 04 — API Reference (~600 words, dense with identifiers)
- chunk_ids: [sec-04]
- dependencies: [translate-sec-03]
- input_files: [source/section-04-api-reference.md]
- artifact_slices: [glossary-slice, style-sheet, domain-map-slice, prev-summary]
- allowed_write_paths: [output/sec-04.md, workspace/summaries/sec-04.md]
- forbidden_write_paths: [glossary.csv, style-sheet.md, domain-map.md]
- output_contract: translated_text + glossary_proposals + continuity_notes + chunk_summary + context_pressure
- status: planned
- return_path: output/sec-04.md

### Unit: fidelity-review-01
- unit_id: fidelity-review-01
- role: fidelity-reviewer
- assigned_to: coordinator
- scope: Source-vs-target comparison for all sections
- chunk_ids: [sec-01, sec-02, sec-03, sec-04]
- dependencies: [translate-sec-01, translate-sec-02, translate-sec-03, translate-sec-04]
- input_files: [source/section-01-overview.md, source/section-02-installation.md, source/section-03-configuration.md, source/section-04-api-reference.md, output/sec-01.md, output/sec-02.md, output/sec-03.md, output/sec-04.md]
- artifact_slices: [glossary.csv, domain-map.md]
- allowed_write_paths: [workspace/reviews/fidelity-review-01.md]
- forbidden_write_paths: [glossary.csv, style-sheet.md, domain-map.md, output/sec-01.md, output/sec-02.md, output/sec-03.md, output/sec-04.md]
- output_contract: defect_list with chunk_id, paragraph, category, source_text, target_text, issue, severity
- status: planned
- return_path: workspace/reviews/fidelity-review-01.md

### Unit: formatting-review-01
- unit_id: formatting-review-01
- role: formatting-reviewer
- assigned_to: coordinator
- scope: Table alignment, code block integrity, heading hierarchy, cross-references
- chunk_ids: [sec-01, sec-02, sec-03, sec-04]
- dependencies: [fidelity-review-01]
- input_files: [output/sec-01.md, output/sec-02.md, output/sec-03.md, output/sec-04.md]
- artifact_slices: [style-sheet.md]
- allowed_write_paths: [workspace/reviews/formatting-review-01.md]
- forbidden_write_paths: [output/sec-01.md, output/sec-02.md, output/sec-03.md, output/sec-04.md]
- output_contract: defect_list with chunk_id, element_type, location, issue, suggested_fix
- status: planned
- return_path: workspace/reviews/formatting-review-01.md
