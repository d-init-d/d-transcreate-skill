# Subagent Dispatch Plan Schema

## Purpose

The Subagent_Dispatch_Plan records how the coordinator assigns work to workers, what each worker may read/write, and how outputs are merged. It is required before dispatching any worker, even in sequential mode.

## Required Fields

| Field | Type | Required | Description |
|---|---|---|---|
| run_id | string | yes | Stable run identifier |
| skill_version | string | yes | d-transcreate-skill version |
| coordinator | string | yes | Main/coordinator agent identifier |
| mode | enum | yes | One of: sequential, parallel, hybrid |
| context_plan_ref | path | yes | Path to Context_Plan artifact |
| chunk_manifest_ref | path | yes | Path to Chunk_Manifest artifact |
| global_artifact_owner | string | yes | Usually "coordinator" |
| max_parallel_workers | integer | yes | Derived from Context_Plan/platform |
| dispatch_units | list | yes | Worker assignments (see below) |
| merge_policy | string | yes | How returned work is merged |
| qa_policy | string | yes | Required review gates after translation |
| fallback_policy | string | yes | What to do if worker/context fails |

## Dispatch Unit Fields

Each entry in `dispatch_units`:

| Field | Type | Required | Description |
|---|---|---|---|
| unit_id | string | yes | Unique dispatch unit identifier |
| role | string | yes | One of the seven role names |
| assigned_to | string | yes | Worker identifier or "coordinator" |
| scope | string | yes | Description of assigned scope |
| chunk_ids | list | yes | Chunk IDs this unit covers (empty for researchers) |
| dependencies | list | yes | unit_ids that must complete first |
| input_files | list | yes | Files the worker may read |
| artifact_slices | list | yes | Which artifact slices to provide |
| allowed_write_paths | list | yes | Paths the worker may write to |
| forbidden_write_paths | list | yes | Paths the worker must not touch |
| output_contract | string | yes | Expected structured return format |
| status | enum | yes | One of: planned, dispatched, in_progress, completed, failed, blocked |
| return_path | string | yes | Where worker output is written/returned |

## Rules

- Workers never write global Glossary, Style_Sheet, Story_Bible, Domain_Map, or final merged output directly.
- Workers may write only their own assigned output path, or return structured proposals.
- No two workers may write the same file in parallel.
- No two workers may translate the same chunk in parallel.
- Coordinator owns conflict resolution, final voice pass, and final QA/reporting.
- If platform has no real subagents, use `mode: sequential` but still follow the same role/output contract.

## Examples

### Sequential Mode

```yaml
run_id: "fiction-short-2024-01"
skill_version: "0.3.0"
coordinator: "main-agent"
mode: sequential
context_plan_ref: "context-plan.md"
chunk_manifest_ref: "chunk-manifest.md"
global_artifact_owner: "coordinator"
max_parallel_workers: 1
merge_policy: "Coordinator merges in source order after each chunk completes"
qa_policy: "Continuity review after each scene group; fidelity + formatting after merge"
fallback_policy: "If chunk fails, reduce size and retry; if repeated failure, flag for user"
dispatch_units:
  - unit_id: "term-research-01"
    role: "terminology-researcher"
    assigned_to: "coordinator"
    scope: "All character names and key terms from scenes 1-3"
    chunk_ids: []
    dependencies: []
    input_files: ["source/scene-01.md", "source/scene-02.md", "source/scene-03.md"]
    artifact_slices: ["translation-brief.md", "glossary.md"]
    allowed_write_paths: ["workspace/proposals/term-research-01.md"]
    forbidden_write_paths: ["glossary.md", "style-sheet.md"]
    output_contract: "glossary_proposals + evidence"
    status: planned
    return_path: "workspace/proposals/term-research-01.md"
  - unit_id: "translate-scene-01"
    role: "chunk-translator"
    assigned_to: "coordinator"
    scope: "Scene 01 translation"
    chunk_ids: ["scene-01"]
    dependencies: ["term-research-01"]
    input_files: ["source/scene-01.md"]
    artifact_slices: ["glossary-slice", "style-sheet", "story-bible-slice", "prev-summary"]
    allowed_write_paths: ["output/scene-01.md", "workspace/summaries/scene-01.md"]
    forbidden_write_paths: ["glossary.md", "style-sheet.md", "story-bible.md"]
    output_contract: "translated_text + uncertain_items + glossary_proposals + chunk_summary"
    status: planned
    return_path: "output/scene-01.md"
```

### Parallel Chunk Translation Mode

```yaml
run_id: "tech-manual-2024-02"
skill_version: "0.3.0"
coordinator: "main-agent"
mode: parallel
context_plan_ref: "context-plan.md"
chunk_manifest_ref: "chunk-manifest.md"
global_artifact_owner: "coordinator"
max_parallel_workers: 3
merge_policy: "Coordinator merges all chunks in source order after all complete"
qa_policy: "Fidelity review per chunk; formatting review after merge"
fallback_policy: "Failed worker retried once with smaller scope; then sequential fallback"
dispatch_units:
  - unit_id: "translate-sec-01"
    role: "chunk-translator"
    assigned_to: "worker-1"
    scope: "Section 01 Overview"
    chunk_ids: ["sec-01"]
    dependencies: []
    input_files: ["source/section-01-overview.md"]
    artifact_slices: ["glossary-slice", "style-sheet", "domain-map-slice"]
    allowed_write_paths: ["output/sec-01.md"]
    forbidden_write_paths: ["glossary.md", "style-sheet.md", "domain-map.md"]
    output_contract: "translated_text + glossary_proposals + continuity_notes"
    status: planned
    return_path: "output/sec-01.md"
  - unit_id: "translate-sec-02"
    role: "chunk-translator"
    assigned_to: "worker-2"
    scope: "Section 02 Installation"
    chunk_ids: ["sec-02"]
    dependencies: []
    input_files: ["source/section-02-installation.md"]
    artifact_slices: ["glossary-slice", "style-sheet", "domain-map-slice"]
    allowed_write_paths: ["output/sec-02.md"]
    forbidden_write_paths: ["glossary.md", "style-sheet.md", "domain-map.md"]
    output_contract: "translated_text + glossary_proposals + continuity_notes"
    status: planned
    return_path: "output/sec-02.md"
```

### Hybrid Mode

```yaml
run_id: "fiction-novel-2024-03"
skill_version: "0.3.0"
coordinator: "main-agent"
mode: hybrid
context_plan_ref: "context-plan.md"
chunk_manifest_ref: "chunk-manifest.md"
global_artifact_owner: "coordinator"
max_parallel_workers: 2
merge_policy: "Sequential merge by chapter after parallel chunks within chapter complete"
qa_policy: "Continuity review per chapter; fidelity per chunk; formatting after full merge"
fallback_policy: "Switch to sequential if continuity drift detected between parallel chunks"
dispatch_units:
  - unit_id: "term-research"
    role: "terminology-researcher"
    assigned_to: "worker-1"
    scope: "Character names and world terms for chapters 1-3"
    chunk_ids: []
    dependencies: []
    input_files: ["source/ch01.md", "source/ch02.md", "source/ch03.md"]
    artifact_slices: ["translation-brief.md"]
    allowed_write_paths: ["workspace/proposals/terms.md"]
    forbidden_write_paths: ["glossary.md"]
    output_contract: "glossary_proposals with evidence"
    status: planned
    return_path: "workspace/proposals/terms.md"
  - unit_id: "style-research"
    role: "style-researcher"
    assigned_to: "worker-2"
    scope: "Target-language dialogue and narration conventions"
    chunk_ids: []
    dependencies: []
    input_files: ["source/ch01.md"]
    artifact_slices: ["translation-brief.md", "style-sheet.md"]
    allowed_write_paths: ["workspace/proposals/style.md"]
    forbidden_write_paths: ["style-sheet.md"]
    output_contract: "style_proposals with rationale"
    status: planned
    return_path: "workspace/proposals/style.md"
  - unit_id: "translate-ch01-scene-a"
    role: "chunk-translator"
    assigned_to: "worker-1"
    scope: "Chapter 1 Scene A"
    chunk_ids: ["ch01-scene-a"]
    dependencies: ["term-research", "style-research"]
    input_files: ["source/ch01-scene-a.md"]
    artifact_slices: ["glossary-slice", "style-sheet", "story-bible-slice", "prev-summary"]
    allowed_write_paths: ["output/ch01-scene-a.md"]
    forbidden_write_paths: ["glossary.md", "style-sheet.md", "story-bible.md"]
    output_contract: "translated_text + proposals + chunk_summary"
    status: planned
    return_path: "output/ch01-scene-a.md"
```

## References

- Context Plan schema: `core/schemas/context-plan.md`
- Chunk Manifest schema: `core/schemas/chunk-manifest.md`
- Subagent orchestration workflow: `core/workflows/subagents.md`
- Context management workflow: `core/workflows/context-management.md`
- Role prompts: `core/prompts/transcreate-coordinator.md`
