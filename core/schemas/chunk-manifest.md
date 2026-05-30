# Chunk Manifest Schema

The Chunk Manifest artifact is the authoritative status ledger for all translation chunks in a project. It tracks each chunk's identity, source location, assignment, workflow status, and QA outcome. The Coordinator_Subagent owns status transitions; Worker_Subagents report completion but do not directly update the manifest.

The Chunk Manifest is the resume point of truth: when a Translation_Agent resumes after interruption, it reads the Chunk Manifest first to determine the next chunk to process. If a chunk file exists on disk but the manifest does not record it as `done`, the agent treats the chunk as not yet complete.

## Columns

| Column | Type | Required | Description |
|---|---|---|---|
| `chunk_id` | string | yes | Stable identifier following a predictable pattern (e.g., `ch03-sec02`, `p012-018`, `art05-para03`). |
| `source_location` | string | yes | Human-readable pointer to where the chunk starts in the source (e.g., `Chapter 3, Section 2`, `pages 12–18`, `Article 5 §3`). |
| `word_or_page_range` | string | yes | Approximate size indicator — word count range or page range (e.g., `~1200 words`, `pp. 12–18`, `¶4–¶9`). |
| `semantic_unit` | string | yes | Type of semantic boundary used for this chunk (e.g., `chapter`, `scene`, `subsection`, `paragraph-group`, `table-group`, `footnote-group`). |
| `dependencies` | string | no | Comma-separated list of `chunk_id` values that must be completed before this chunk can start (e.g., `ch03-sec01` for continuity). Empty if no dependencies. |
| `assigned_to` | string | no | Role or subagent instance assigned to this chunk (e.g., `chunk-translator-1`, `coordinator`). Empty if unassigned. |
| `status` | enum | yes | Current workflow status. One of: `planned`, `research-needed`, `ready`, `drafting`, `drafted`, `qa-needed`, `revising`, `done`, `blocked`. |
| `output_path` | string | no | Relative path to the translated output file for this chunk (e.g., `output/ch03-sec02.md`). Empty until drafting begins. |
| `qa_status` | string | no | Summary of QA outcome (e.g., `pass`, `2 issues found`, `pending`). Empty until QA is performed. |
| `notes` | string | no | Free-form notes — blockers, special instructions, cross-references to Unresolved_Issues_Log entries. |

## Enumerations

### `status`

| Value | Meaning |
|---|---|
| `planned` | Chunk identified and registered; not yet ready for translation. |
| `research-needed` | Chunk requires terminology or style research before translation can begin. |
| `ready` | All dependencies satisfied and research complete; chunk can be assigned for drafting. |
| `drafting` | Pass A (draft translation) is in progress. |
| `drafted` | Pass A complete; chunk awaits source-compare and revision passes. |
| `qa-needed` | Draft complete; entering Pass B (source-compare) and Pass C (revision). |
| `revising` | Defects found during QA passes; chunk is being revised. |
| `done` | All passes complete, state updated, chunk accepted by coordinator. |
| `blocked` | External dependency or unresolved decision prevents progress; see `notes` for details. |

### Status Transitions

```
planned ──→ research-needed ──→ ready ──→ drafting ──→ drafted ──→ qa-needed ──→ done
   │                              ↑                                    │
   └──────────────────────────────┘                                    ↓
              (dependencies met)                                   revising
                                                                       │
                                                                       ↓
                                                                  qa-needed
                                                                  (re-check)

Any status ──→ blocked (when blocker arises)
blocked ──→ ready (when blocker cleared)
```

## CSV Form

Use this format when the Chunk Manifest is persisted as `chunk-manifest.csv`:

```csv
chunk_id,source_location,word_or_page_range,semantic_unit,dependencies,assigned_to,status,output_path,qa_status,notes
```

Rules:
- Header row is mandatory.
- Fields containing commas, quotes, or newlines must be enclosed in double quotes.
- Use UTF-8 encoding without BOM.
- One row per chunk. Chunks are listed in source order.
- The `dependencies` field uses semicolons to separate multiple chunk IDs within the CSV (to avoid ambiguity with the CSV comma delimiter).

### Example

```csv
chunk_id,source_location,word_or_page_range,semantic_unit,dependencies,assigned_to,status,output_path,qa_status,notes
ch01-sec01,"Chapter 1, Section 1",~800 words,scene,,chunk-translator-1,done,output/ch01-sec01.md,pass,
ch01-sec02,"Chapter 1, Section 2",~1100 words,scene,ch01-sec01,chunk-translator-1,done,output/ch01-sec02.md,pass,Continuity: introduces protagonist's alias
ch02-sec01,"Chapter 2, Section 1",~950 words,scene,ch01-sec02,chunk-translator-2,drafting,output/ch02-sec01.md,,
ch02-sec02,"Chapter 2, Section 2",~1300 words,scene,ch02-sec01,,planned,,,Contains reveal — check Story_Bible before translating
ch02-sec03,"Chapter 2, Section 3",~600 words,scene,ch02-sec01,,research-needed,,,New technical terms need glossary entries
appendix-a,"Appendix A",~400 words,table-group,,,ready,,,Standalone table; no continuity dependencies
```

## Markdown Table Form

Use this format when the Chunk Manifest is embedded in a Markdown document (e.g., for inline review or when CSV tooling is unavailable):

```markdown
# Chunk Manifest

| chunk_id | source_location | word_or_page_range | semantic_unit | dependencies | assigned_to | status | output_path | qa_status | notes |
|---|---|---|---|---|---|---|---|---|---|
| ch01-sec01 | Chapter 1, Section 1 | ~800 words | scene | | chunk-translator-1 | done | output/ch01-sec01.md | pass | |
| ch01-sec02 | Chapter 1, Section 2 | ~1100 words | scene | ch01-sec01 | chunk-translator-1 | done | output/ch01-sec02.md | pass | Continuity: introduces protagonist's alias |
| ch02-sec01 | Chapter 2, Section 1 | ~950 words | scene | ch01-sec02 | chunk-translator-2 | drafting | output/ch02-sec01.md | | |
| ch02-sec02 | Chapter 2, Section 2 | ~1300 words | scene | ch02-sec01 | | planned | | | Contains reveal — check Story_Bible before translating |
| ch02-sec03 | Chapter 2, Section 3 | ~600 words | scene | ch02-sec01 | | research-needed | | | New technical terms need glossary entries |
| appendix-a | Appendix A | ~400 words | table-group | | | ready | | | Standalone table; no continuity dependencies |
```

## Usage Rules

1. **Creation**: The Chunk Manifest is produced during Phase 4 (Planning/Chunking) after the Source_Map, Glossary, and Style_Sheet exist. Every identified semantic unit in the source receives a row.
2. **Ordering**: Chunks are listed in source document order. The `chunk_id` pattern must be predictable and stable across sessions.
3. **Dependencies**: A chunk with non-empty `dependencies` cannot transition to `ready` until all listed dependency chunks have status `done`.
4. **Assignment**: The Coordinator_Subagent assigns chunks to Worker_Subagents. No two workers may be assigned the same chunk simultaneously.
5. **Status authority**: Only the Coordinator_Subagent (or the Translation_Agent in sequential mode) may update the `status` field. Workers report completion; the coordinator confirms.
6. **Resume**: On session resume, the agent reads the Chunk Manifest to find the first chunk whose status is not `done` and loads the artifacts required for that chunk.
7. **Parallel safety**: When subagents run in parallel, each is assigned a disjoint set of chunks. The manifest prevents two workers from editing the same output file.
8. **Blocked chunks**: When a chunk cannot proceed (e.g., unresolved terminology, missing context from a dependency), set status to `blocked` and record the reason in `notes`. The coordinator clears blockers and transitions back to `ready`.
9. **QA integration**: After all passes complete for a chunk, the `qa_status` field records the outcome. The chunk transitions to `done` only when QA passes or residual issues are documented and accepted.

## References

- Chunk identifier pattern, column requirements, and status enumeration: defined in the field tables above.
- Resume procedure: `core/workflows/context-management.md`
- Subagent dispatch rules: `core/workflows/subagents.md`
- Schema existence validation: enforced by `scripts/validate_pack.py`
