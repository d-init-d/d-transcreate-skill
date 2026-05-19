# Context Management

Use this workflow whenever the source is too large for one context window or translation spans multiple sessions.

## Context Budget Rule

Never load the full source document into active context unless it genuinely fits with room for QA.

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

## References

- Schema: `core/schemas/chunk-manifest.md`
- Schema: `core/schemas/chunk-summary.md`
- Schema: `core/schemas/unresolved-issues.md`
- Workflow: `core/workflows/long-document.md`
- Workflow: `core/workflows/subagents.md`
