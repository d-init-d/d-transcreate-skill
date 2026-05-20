# Context Plan Schema

The Context Plan is the orchestration artifact produced before final chunking and before any subagent dispatch. It records the effective context budget, the chunk-sizing policy, and the fallback rules that govern the whole translation run.

The Context Plan exists to prevent two failure modes:

1. The agent loads more content than the platform/model can safely process, leading to dropped instructions, partial output, or context-pressure hallucinations.
2. The agent produces a Chunk Manifest that is technically correct but operationally unsafe, because individual chunks plus required artifact slices exceed the usable budget.

The Coordinator owns the Context Plan. Workers read it but never modify it.

## Required Fields

| Field | Type | Required | Description |
|---|---|---|---|
| `skill_version` | string | yes | Version of the d-transcreate-skill in use (e.g., `0.2.0`). Recorded for auditability. |
| `platform` | string | yes | Agent platform or runtime (e.g., `Claude Code`, `Codex`, `Cursor`, `OpenCode`, `Generic`). |
| `model_or_agent` | string | no | Model or agent name if known (e.g., `claude-sonnet-4`, `gpt-5`, `unknown`). |
| `known_context_window` | string | no | Stated context length when documented (e.g., `200k tokens`, `128k tokens`, `unknown`). |
| `effective_context_budget` | string | yes | Conservative usable budget after subtracting system prompt, tool overhead, and safety margin. |
| `source_material_class` | enum | yes | One of: `routine_prose`, `fiction`, `dense_technical`, `legal`, `medical`, `mixed`. |
| `context_mode` | enum | yes | One of: `conservative`, `standard`, `large_context`. |
| `max_source_words_per_chunk` | integer | yes | Upper bound on source words per chunk for this run. |
| `artifact_slice_policy` | string | yes | Description of how Glossary/Style_Sheet/Story_Bible/Domain_Map slices are selected per chunk. |
| `reserved_input_budget` | string | yes | Portion of context reserved for source chunk + artifact slices (typical: 60–70%). |
| `reserved_output_budget` | string | yes | Portion of context reserved for the translated output (typical: 20–30%). |
| `reserved_qa_budget` | string | yes | Portion of context reserved for source-compare and revision passes (typical: 10–15%). |
| `safety_margin` | string | yes | Unused buffer to absorb unexpected expansion (typical: 10–15%). |
| `max_parallel_workers` | integer | yes | Maximum number of Worker_Subagents allowed to run concurrently for this run. |
| `fallback_triggers` | list | yes | Conditions that force smaller chunks or sequential mode (see Fallback Triggers below). |
| `notes` | string | no | Run-specific constraints, observations, or platform quirks. |

## Enumerations

### `source_material_class`

| Value | Use For |
|---|---|
| `routine_prose` | General articles, blog posts, narrative non-fiction without dense terminology. |
| `fiction` | Novels, short stories, scripts, dialogue-heavy material with continuity needs. |
| `dense_technical` | API references, engineering docs, scientific papers, specifications. |
| `legal` | Contracts, policies, statutes, terms of service, compliance documents. |
| `medical` | Clinical guidelines, drug information, medical records, patient material. |
| `mixed` | Documents combining two or more of the above (treat as the densest class present). |

### `context_mode`

| Value | When To Use | Behavior |
|---|---|---|
| `conservative` | Context window is unknown, small (<32k tokens equivalent), or platform overhead is unclear. | Smallest chunks, 1–2 workers, fewer artifact slices loaded per chunk. |
| `standard` | Context window is known and medium (≈32k–100k tokens equivalent). | Medium chunks, 2–4 workers, full required slices per chunk. |
| `large_context` | Context window is known and large (≥100k tokens equivalent). | Larger chunks allowed, 4+ workers if dependencies permit, broader slices acceptable. |

The agent SHOULD default to `conservative` when in doubt. Upgrading to `standard` or `large_context` requires evidence (platform documentation, user-stated capacity, or successful prior runs).

## Default Budget Policy

Unless overridden by user instruction or platform documentation, allocate the effective budget as:

```text
Input  (source chunk + artifact slices) :  60–70%
Output (translation draft + revision)   :  20–30%
QA     (source-compare + uncertainty)   :  10–15%
Safety margin                           :  10–15%
```

Sum must not exceed 100%. Overlap between QA and safety margin is acceptable when the run is short.

## Suggested Chunk Size Presets

These are defaults; the actual `max_source_words_per_chunk` MUST be reduced when fallback triggers fire.

### `conservative` mode

| Material class | Source words per chunk |
|---|---|
| `routine_prose` | 500–900 |
| `fiction` | one short scene, or 500–900 words |
| `dense_technical` | 300–700 |
| `legal` | 300–700 |
| `medical` | 300–700 |
| `mixed` | use the lower bound of the densest class present |

### `standard` mode

| Material class | Source words per chunk |
|---|---|
| `routine_prose` | 900–1,800 |
| `fiction` | one scene, or 800–1,500 words |
| `dense_technical` | 600–1,200 |
| `legal` | 600–1,200 |
| `medical` | 600–1,200 |
| `mixed` | lower bound of the densest class present |

### `large_context` mode

| Material class | Source words per chunk |
|---|---|
| `routine_prose` | 1,800–3,000 |
| `fiction` | one scene, or 1,200–2,500 words |
| `dense_technical` | 1,000–1,800 |
| `legal` | 1,000–1,800 |
| `medical` | 1,000–1,800 |
| `mixed` | lower bound of the densest class present |

## Fallback Triggers

The Context Plan MUST list explicit conditions that force chunk-size reduction or a switch to sequential mode. At minimum, include:

- Glossary slice for a chunk exceeds the artifact-slice budget.
- Story_Bible or Domain_Map excerpt for a chunk exceeds the artifact-slice budget.
- Source-compare cannot fit source + draft + glossary slice in one pass.
- Output draft exceeds the reserved output budget.
- A worker returns `context_pressure: true`.
- A chunk requires more than three adjacent Chunk_Summaries to disambiguate.
- A platform timeout, rate-limit, or truncation event occurs.

When any trigger fires, the Coordinator SHALL:

1. Pause new dispatches.
2. Persist current state.
3. Reduce `max_source_words_per_chunk` by at least 30% or split the affected chunk at the next semantic boundary below the current one.
4. Regenerate affected Chunk_Manifest rows.
5. Update the Context Plan and record the trigger in `notes`.
6. Resume from the first incomplete subchunk.

## Form

```markdown
# Context Plan

## Identification
- skill_version: 0.2.0
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
- max_parallel_workers: 3

## Fallback Triggers
- Glossary slice for a chunk exceeds 1,500 tokens.
- Source-compare requires loading more than two adjacent chunk outputs.
- Worker returns context_pressure: true.
- Output draft exceeds 30% of effective budget.
- Platform truncation event observed.

## Notes
- Adjacent fiction scenes will not be dispatched in parallel until voice is stable.
- Reduce to conservative mode if any worker returns context_pressure twice in a row.
```

## CSV Form

The Context Plan is normally Markdown only; a CSV form is not required. If a CSV companion is needed for tooling, store one row per field with columns `field`, `value`.

## Usage Rules

1. **Creation order:** The Context Plan is created in Phase 3 (Research/Planning), AFTER the Translation_Brief and Source_Map exist, and BEFORE the Chunk_Manifest is finalized.
2. **Authority:** Only the Coordinator may write or update the Context Plan. Workers read the Plan when assembling worker prompts and may report context-pressure findings, but they do not modify the Plan.
3. **Before dispatch:** The Subagent_Dispatch_Plan MUST reference an existing Context Plan via `context_plan_ref`. Dispatch without a Context Plan is forbidden.
4. **Manifest binding:** When the Context Plan changes (e.g., chunk size reduced after a fallback trigger), the Chunk_Manifest MUST be updated to reflect the new boundaries. Both artifacts must agree.
5. **Resume:** On session resume, the Coordinator reads the Context Plan first, then the Chunk_Manifest. If the Plan does not exist, treat the run as not yet ready for dispatch.
6. **Conservative default:** When the platform's context window is unknown, use `context_mode: conservative` and the smallest chunk preset for the material class. Upgrade only with evidence.
7. **Never allocate the full window to source:** Even in `large_context` mode, the source + slices budget MUST leave room for output, QA, and safety margin.

## Audit Trail

The Context Plan participates in the run's audit trail along with the Translation_Brief and the QA_Report:

- The `skill_version`, `platform`, and `model_or_agent` fields enable later reproduction.
- The `fallback_triggers` and `notes` sections record any mid-run adjustments and their reasons.
- The QA_Report SHOULD reference the final Context Plan state when listing residual risks.

## References

- Translation_Brief schema: `core/schemas/translation-brief.md`
- Source_Map schema: `core/schemas/source-map.md`
- Chunk_Manifest schema: `core/schemas/chunk-manifest.md`
- Subagent_Dispatch_Plan schema: `core/schemas/subagent-dispatch-plan.md`
- Context management workflow: `core/workflows/context-management.md`
- Subagent orchestration workflow: `core/workflows/subagents.md`
- Long document workflow: `core/workflows/long-document.md`
