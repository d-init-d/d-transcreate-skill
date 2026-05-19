# Subagent Orchestration

Use this file when the translation task benefits from parallel or sequential subagent dispatch. It covers the readiness gate, role responsibilities, prompt pattern, parallel execution rules, and the coordinator merge checklist.

## Subagent Readiness Gate

Do NOT dispatch any Worker_Subagent until ALL of the following artifacts exist on disk:

1. **Translation_Brief** — completed intake with source, target, audience, mode, quality bar.
2. **Source_Map** — whole-document scan with structure, hazards, and material classification.
3. **Glossary** — at minimum proposed core terms with evidence and confidence.
4. **Style_Sheet** — register, rhythm, adaptation rules, and forbidden patterns recorded.
5. **Chunk_Manifest** — all chunks planned with stable IDs, dependencies, and initial status.
6. **Story_Bible** (fiction-class) or **Domain_Map** (technical/legal/medical class) — whichever applies.

If any artifact is missing or incomplete, the Coordinator must produce it before dispatching workers. This gate prevents inconsistent parallel output caused by workers operating without shared decisions.

## Role Responsibilities

The pack defines seven fixed roles. Each role has a disjoint scope. Workers propose; the Coordinator approves.

| Role | Authority | Scope | Returns |
|---|---|---|---|
| **Coordinator** (`transcreate-coordinator`) | Final say on Glossary, Style_Sheet, voice, continuity, merge | All artifacts (read); Glossary, Style_Sheet, Story_Bible/Domain_Map, Chunk_Manifest (write) | Final merged document, accept/reject decisions on proposals |
| **Terminology Researcher** (`terminology-researcher`) | Proposes only | A term list or chapter range | Glossary proposal rows with evidence and source URL |
| **Style Researcher** (`style-researcher`) | Proposes only | Target genre/domain conventions | Style observations with paraphrased rationale and source notes |
| **Chunk Translator** (`chunk-translator`) | Owns one chunk | One chunk's output file, its Chunk_Summary, scoped Unresolved_Issues entries | Translated chunk + uncertain items + Glossary/Style_Sheet change proposals + continuity notes |
| **Continuity Reviewer** (`continuity-reviewer`) | Flags only | One chapter range or chunk set | Defect list: contradictions, timeline/name/pronoun issues with chunk_id and source location |
| **Fidelity Reviewer** (`fidelity-reviewer`) | Flags only | Source-vs-target comparison | Defect list keyed to source-target paragraph diff (omissions, additions, meaning shifts) |
| **Formatting Reviewer** (`formatting-reviewer`) | Flags only | Output document layout | Defect list for tables, footnotes, headings, citations, anchors, layout |

**Key constraint:** Workers never write the global Glossary or Style_Sheet directly. They return proposals. The Coordinator reviews, accepts or rejects, and applies accepted changes to the canonical artifacts.

## Prompt Pattern for Worker Subagents

When dispatching a Worker_Subagent, the Coordinator provides a structured prompt containing:

1. **Role declaration** — which role this worker fills and the chunk or scope ID.
2. **Source material** — the source chunk text, or the term list, or the output chunk for review.
3. **Target context** — target language, locale, audience, and translation mode.
4. **Artifact slices** (not full artifacts):
   - Relevant Translation_Brief excerpt (scope, constraints, quality bar).
   - Relevant Glossary rows (only terms appearing in or adjacent to this chunk).
   - Relevant Style_Sheet rules (only rules applicable to this chunk's content type).
   - Relevant Story_Bible or Domain_Map notes (only entries for characters, concepts, or terms in this chunk).
5. **Adjacent summaries** — previous Chunk_Summary and next Chunk_Summary when available.
6. **Exact output contract** — the structured fields the worker MUST return.

### Example Prompt Skeleton

```text
You are the chunk-translator for chunk {chunk_id}.
Target: {target_language} for {audience}.
Mode: {translation_mode}.

## Inputs
- Source chunk: [attached below]
- Glossary slice: [attached below]
- Style rules: [attached below]
- Story Bible excerpt: [attached below]
- Previous summary: [attached below]
- Next summary: [attached below]

## Output Contract
Return a structured response with:
1. translated_text — the full translated chunk
2. uncertain_items — list of terms or passages with low confidence
3. glossary_proposals — new or changed entries (term, preferred, evidence, confidence)
4. style_proposals — new observations or rule suggestions
5. continuity_notes — any facts that should update Story_Bible or Domain_Map
6. changed_files — list of files this output affects

Do not translate outside this chunk. Do not modify the global Glossary or Style_Sheet directly.
```

## Parallel Execution Rules

When the platform supports parallel subagents:

1. **Disjoint assignment** — assign each worker a non-overlapping scope (different chunks, different term lists, different review ranges). Two workers must never operate on the same chunk simultaneously.
2. **No shared file writes** — two Worker_Subagent instances SHALL NOT edit the same output file in parallel. Each worker writes only to its own designated output path.
3. **Structured returns** — every worker MUST list changed files or produced artifacts in its return payload. The Coordinator uses this list for merge tracking.
4. **Central merge** — all worker outputs flow back to the Coordinator. Workers do not merge with each other.
5. **Glossary conflict resolution** — when two workers propose conflicting Glossary entries for the same term, the Coordinator resolves the conflict before the final voice pass. Resolution is recorded in the Glossary notes with rationale.
6. **Cross-chunk QA after parallel translation** — after all parallel chunks are drafted, run continuity and fidelity review across the full set before the final voice pass.

### Sequential Fallback

Where a platform does not support parallel subagents, the Translation_Agent executes the same role responsibilities sequentially while preserving the same artifact handoff contract. The workflow order is:

1. Terminology Researcher (if research-needed chunks exist)
2. Style Researcher (if style decisions are pending)
3. Chunk Translator (one chunk at a time, in source order)
4. Continuity Reviewer (after each chapter or logical group)
5. Fidelity Reviewer (after each chunk or group)
6. Formatting Reviewer (after merge)

The Coordinator role is performed by the main agent thread in sequential mode.

## Coordinator Merge Checklist

After all assigned Worker_Subagent outputs are received, the Coordinator performs:

### Completeness Check
- [ ] Every assigned chunk was returned with a valid output.
- [ ] No chunk is missing from the Chunk_Manifest with status `done`.
- [ ] Every worker's `changed_files` list accounts for expected outputs.

### Source Fidelity
- [ ] Compare merged output against source for omissions and additions.
- [ ] Verify no chunk boundaries introduced gaps or overlaps.

### Terminology Normalization
- [ ] Normalize term choices across all chunks against the approved Glossary.
- [ ] Resolve any conflicting Glossary applications (different translations of the same term in different chunks).
- [ ] Merge accepted Glossary proposals from workers into the canonical Glossary.
- [ ] Record rejected proposals with reason (for future reference when the same term recurs).

### Style and Voice Consistency
- [ ] Verify Style_Sheet rules are applied uniformly across chunks.
- [ ] Run a single final voice pass over the merged output centrally (not per-chunk).
- [ ] Ensure author voice, register, and rhythm are consistent from start to finish.

### State Updates
- [ ] Update Story_Bible or Domain_Map with continuity facts accepted from worker outputs.
- [ ] Update Chunk_Summaries for all completed chunks.
- [ ] Update Chunk_Manifest: set all merged chunks to status `done`.

### Residual Issues
- [ ] Queue any unresolved cross-chunk consistency issues for the QA gates.
- [ ] Ensure the Unresolved_Issues_Log reflects all open items from worker returns.

## Consistency Guarantee

Within a single translation run:

- Approved Glossary entries are applied identically across ALL chunks.
- Style_Sheet decisions are applied identically across ALL chunks.
- If a chunk-level decision conflicts with the Glossary or Style_Sheet, the Coordinator either updates the canonical artifact (with rationale) or rejects the chunk-level decision before merge.
- When parallel workers propose conflicting changes, the Coordinator resolves before final merge and records the resolution in artifact notes.

## References

- Subagent prompt definitions: `core/prompts/transcreate-coordinator.md`, `core/prompts/terminology-researcher.md`, `core/prompts/style-researcher.md`, `core/prompts/chunk-translator.md`, `core/prompts/continuity-reviewer.md`, `core/prompts/fidelity-reviewer.md`, `core/prompts/formatting-reviewer.md`
- Artifact schemas: `core/schemas/glossary.md`, `core/schemas/style-sheet.md`, `core/schemas/chunk-manifest.md`, `core/schemas/story-bible.md`, `core/schemas/domain-map.md`
- Context management and resume: `core/workflows/context-management.md`
- QA gates (post-merge): `core/workflows/qa-gates.md`
- Long-document workflow (phases): `core/workflows/long-document.md`
