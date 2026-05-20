# Context Management

Use this workflow whenever the source is too large for one context window or translation spans multiple sessions.

## Context Budget Rule

Never load the full source document into active context unless it genuinely fits with room for QA.

## Context Plan Requirement

The coordinator must create a **Context_Plan** artifact (schema: `core/schemas/context-plan.md`) before finalizing the Chunk_Manifest. The Context_Plan records:

- Platform and model constraints.
- Effective context budget.
- Source material classification.
- Chunk-size limits derived from the budget.
- Artifact slicing policy.
- Fallback triggers.

If context window size is unknown, choose the conservative profile. Context assumptions must be written to disk — never rely on chat history for budget decisions.

## Context Length Discovery

The agent should determine context capacity from (in priority order):

1. Platform/tool documentation if available (e.g., adapter notes).
2. Model name/config if known (e.g., model card states context length).
3. User-provided constraint in the Translation_Brief.
4. Conservative fallback if unknown.

The workflow must not require live web lookup during translation to determine context capacity.

## Default Budget Profiles

| Profile | When used | Source chunk size | Max parallelism |
|---|---|---|---|
| conservative | Unknown/small context | Small (500–900 words prose) | 1–2 workers |
| standard | Known medium context | Medium (900–1,800 words prose) | 2–4 workers |
| large_context | Known large context | Larger (1,800–3,000 words prose) | 4+ only if dependencies allow |

Avoid hard-coding exact token counts as universal truth. Use word ranges and require conservative adjustment for dense material.

## Chunk Size Adjustment Rules

Reduce chunk size below the Context_Plan maximum when:

- Glossary slice for the chunk exceeds 2,000 words.
- Story_Bible or Domain_Map excerpt exceeds 1,500 words.
- QA compare cannot fit source + target in one pass.
- Output is too long for one pass (translation expands significantly).
- Worker reports `context_pressure: true`.
- The chunk contains dense tables, citations, or cross-references requiring extra context.

When reducing, split at the next safest lower-level semantic boundary.

Active context for a chunk SHALL contain only:

- Translation_Brief
- Relevant Style_Sheet rules
- Relevant Glossary rows (filtered to terms appearing in the chunk)
- Story_Bible or Domain_Map excerpt relevant to this chunk
- Previous Chunk_Summary
- Next Chunk_Summary (when available)
- Current source chunk text
- Unresolved_Issues entries that affect this chunk

Everything else belongs in workspace artifact files on disk.

## What Loads Per Chunk

Before translating a chunk, load only the minimum context:

1. **Translation_Brief** — always loaded (compact, sets global constraints).
2. **Glossary slice** — use search to pull only rows for terms appearing in the current chunk.
3. **Style_Sheet slice** — load only rules relevant to the chunk's content type (dialogue, narration, technical prose, etc.).
4. **Story_Bible or Domain_Map excerpt** — load only characters, places, concepts, or acronyms referenced in this chunk.
5. **Previous Chunk_Summary** — provides continuity from the preceding chunk.
6. **Next Chunk_Summary** — when available, provides forward context for foreshadowing or cross-references.
7. **Current source chunk** — the raw source text to translate.
8. **Unresolved_Issues** — filtered to entries scoped to this section, character, term, or domain.

Do NOT load:

- Full neighboring chunks (use summaries instead).
- The entire Glossary or Style_Sheet (use filtered slices).
- The full Source_Map (consult only if a structural question arises).
- Previously translated chunk outputs (use summaries).

## Summary Unloading

After completing a chunk translation (all passes A through D):

1. Write a compact Chunk_Summary for the completed chunk (see `core/schemas/chunk-summary.md`).
2. Update the Chunk_Manifest status to `done`.
3. Unload the raw source chunk text from working memory.
4. Unload the translated output from working memory (it is persisted to disk).
5. Retain only the Chunk_Summary for continuity into the next chunk.

The Chunk_Summary must capture: source range, what happened or main argument, terms introduced, continuity implications, unresolved issues, and next-chunk dependency. This compressed representation replaces the full chunk in context.

## State Files (Durable Persistence)

All translation state SHALL be persisted as files in the workspace — never solely in chat history:

- `translation-brief.md`
- `source-map.md`
- `glossary.csv` or `glossary.md`
- `style-sheet.md`
- `story-bible.md` or `domain-map.md`
- `chunk-manifest.csv` or `chunk-manifest.md`
- `chunk-summaries.md`
- `unresolved-issues.md`
- `qa-report.md`

Use stable chunk IDs everywhere. Save decisions, not long discussions.

## Resume Procedure

When a Translation_Agent resumes after interruption (timeout, context reset, session change):

1. **Read the Chunk_Manifest first.** This is the authoritative status ledger. Determine the first chunk whose status is NOT `done`.
2. **Re-open the Translation_Brief.** Restore global constraints (languages, audience, mode, quality bar).
3. **Re-open the Style_Sheet.** Restore voice and formatting decisions.
4. **Re-open the Glossary.** Restore terminology decisions (or the relevant slice for the current chunk).
5. **Load the current chunk source.** The first non-done chunk identified in step 1.
6. **Reconstruct continuity from Chunk_Summaries.** Load the summary of the immediately preceding chunk (and next chunk if available). Do NOT reload full translated outputs of prior chunks.
7. **Load relevant Story_Bible or Domain_Map excerpt.** Only the entries pertinent to the current chunk.
8. **Load relevant Unresolved_Issues entries.** Only those scoped to the current chunk or its dependencies.
9. **Continue translation from the identified chunk.** Do not redo chunks already marked `done`.

### Manifest as Source of Truth

The Chunk_Manifest is authoritative for status. If a chunk output file exists on disk but the Chunk_Manifest does not record it as `done`, the Translation_Agent SHALL treat the chunk as not yet complete and SHALL re-process it.

### Platform Adaptation

If a platform does not support lazy reference loading natively, the corresponding Adapter_Pack entrypoint SHALL instruct the Translation_Agent to read related artifact files on demand by file path rather than expecting them to be pre-loaded.

## Artifact Slicing Protocol

When loading context for a chunk, select artifact slices as follows:

- **Glossary slice**: Terms appearing in the current chunk + recurring global terms (high-frequency entries used across many chunks).
- **Style_Sheet slice**: Only rules relevant to the chunk's content type (dialogue, narration, technical prose, tables, etc.).
- **Story_Bible slice**: Characters, places, and timeline items appearing in the chunk + adjacent scene continuity threads.
- **Domain_Map slice**: Acronyms, concepts, standards, and units appearing in the chunk.
- **Chunk_Summary slices**: Previous and next summaries only; never load full neighboring chunks by default.
- **Unresolved_Issues slice**: Only issues scoped to the current chunk, its dependencies, or related characters/terms/concepts.

Never load full artifacts when slices suffice. The Context_Plan's `artifact_slice_policy` field documents the slicing approach for the run.

## Context Overflow Fallback

If the agent notices context pressure during translation (output truncation, degraded quality, inability to complete QA compare):

1. **Stop expanding context.** Do not load additional artifacts or neighboring chunks.
2. **Persist current state.** Save any partial work (draft, notes, proposals) to disk.
3. **Split current chunk.** Divide at the next safest semantic boundary within the chunk.
4. **Regenerate affected Chunk_Manifest rows.** Add new chunk IDs for the split pieces.
5. **Update Context_Plan.** Record the overflow event and adjusted chunk sizes.
6. **Resume from first incomplete subchunk.** Follow the standard resume procedure.

If overflow recurs after splitting, switch to conservative mode and reduce max_parallel_workers to 1.

## References

- Schema: `core/schemas/context-plan.md`
- Schema: `core/schemas/chunk-manifest.md`
- Schema: `core/schemas/chunk-summary.md`
- Schema: `core/schemas/unresolved-issues.md`
- Schema: `core/schemas/subagent-dispatch-plan.md`
- Workflow: `core/workflows/long-document.md`
- Workflow: `core/workflows/subagents.md`
