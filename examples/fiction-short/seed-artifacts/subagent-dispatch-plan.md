# Subagent Dispatch Plan

## Run Metadata
- run_id: fiction-short-example-01
- skill_version: 0.3.0
- coordinator: main-agent
- mode: hybrid
- context_plan_ref: seed-artifacts/context-plan.md
- chunk_manifest_ref: chunk-manifest.md
- global_artifact_owner: coordinator
- max_parallel_workers: 2

## Policies
- merge_policy: Coordinator merges scenes in source order after each completes; final voice pass over full output.
- qa_policy: Continuity review after all scenes drafted; fidelity review per scene; formatting review after merge.
- fallback_policy: If a scene translation fails or returns context_pressure, reduce chunk size and retry sequentially. If repeated failure, flag for user.

## Dispatch Units

### Unit: term-research-01
- unit_id: term-research-01
- role: terminology-researcher
- assigned_to: coordinator
- scope: Character names, key terms, and cultural references from all 3 scenes
- chunk_ids: []
- dependencies: []
- input_files: [source/scene-01.md, source/scene-02.md, source/scene-03.md]
- artifact_slices: [translation-brief.md, glossary.csv]
- allowed_write_paths: [workspace/proposals/term-research-01.md]
- forbidden_write_paths: [glossary.csv, style-sheet.md, story-bible.md]
- output_contract: glossary_proposals with evidence and confidence
- status: planned
- return_path: workspace/proposals/term-research-01.md

### Unit: style-research-01
- unit_id: style-research-01
- role: style-researcher
- assigned_to: coordinator
- scope: Target-language dialogue conventions and narrative register for literary fiction
- chunk_ids: []
- dependencies: []
- input_files: [source/scene-01.md]
- artifact_slices: [translation-brief.md, style-sheet.md]
- allowed_write_paths: [workspace/proposals/style-research-01.md]
- forbidden_write_paths: [style-sheet.md, glossary.csv]
- output_contract: style_proposals with rationale and source observations
- status: planned
- return_path: workspace/proposals/style-research-01.md

### Unit: translate-scene-01
- unit_id: translate-scene-01
- role: chunk-translator
- assigned_to: coordinator
- scope: Scene 01 — opening scene, character introduction
- chunk_ids: [scene-01]
- dependencies: [term-research-01, style-research-01]
- input_files: [source/scene-01.md]
- artifact_slices: [glossary-slice, style-sheet, story-bible-slice, prev-summary]
- allowed_write_paths: [output/scene-01.md, workspace/summaries/scene-01.md]
- forbidden_write_paths: [glossary.csv, style-sheet.md, story-bible.md]
- output_contract: translated_text + uncertain_items + glossary_proposals + chunk_summary + context_pressure
- status: planned
- return_path: output/scene-01.md

### Unit: translate-scene-02
- unit_id: translate-scene-02
- role: chunk-translator
- assigned_to: coordinator
- scope: Scene 02 — rising action
- chunk_ids: [scene-02]
- dependencies: [translate-scene-01]
- input_files: [source/scene-02.md]
- artifact_slices: [glossary-slice, style-sheet, story-bible-slice, prev-summary, next-summary]
- allowed_write_paths: [output/scene-02.md, workspace/summaries/scene-02.md]
- forbidden_write_paths: [glossary.csv, style-sheet.md, story-bible.md]
- output_contract: translated_text + uncertain_items + glossary_proposals + chunk_summary + context_pressure
- status: planned
- return_path: output/scene-02.md

### Unit: translate-scene-03
- unit_id: translate-scene-03
- role: chunk-translator
- assigned_to: coordinator
- scope: Scene 03 — climax and resolution
- chunk_ids: [scene-03]
- dependencies: [translate-scene-02]
- input_files: [source/scene-03.md]
- artifact_slices: [glossary-slice, style-sheet, story-bible-slice, prev-summary]
- allowed_write_paths: [output/scene-03.md, workspace/summaries/scene-03.md]
- forbidden_write_paths: [glossary.csv, style-sheet.md, story-bible.md]
- output_contract: translated_text + uncertain_items + glossary_proposals + chunk_summary + context_pressure
- status: planned
- return_path: output/scene-03.md

### Unit: continuity-review-01
- unit_id: continuity-review-01
- role: continuity-reviewer
- assigned_to: coordinator
- scope: Cross-scene continuity check (names, timeline, voice, pronouns)
- chunk_ids: [scene-01, scene-02, scene-03]
- dependencies: [translate-scene-01, translate-scene-02, translate-scene-03]
- input_files: [output/scene-01.md, output/scene-02.md, output/scene-03.md]
- artifact_slices: [story-bible.md, glossary-slice, chunk-summaries]
- allowed_write_paths: [workspace/reviews/continuity-review-01.md]
- forbidden_write_paths: [glossary.csv, style-sheet.md, story-bible.md, output/scene-01.md, output/scene-02.md, output/scene-03.md]
- output_contract: defect_list with chunk_id, location, category, description, and suggested_fix
- status: planned
- return_path: workspace/reviews/continuity-review-01.md
