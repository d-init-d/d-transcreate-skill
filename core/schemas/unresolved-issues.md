# Unresolved Issues Log — Schema

This schema defines the **Unresolved_Issues_Log** artifact used throughout the translation workflow to track open questions, ambiguous terms, unresolved decisions, and any issue that cannot be resolved immediately during a translation pass.

## Purpose

The Unresolved Issues Log serves as a living record of items that require human input, further research, or coordinator decision before the translation can be finalized. It is written to by multiple roles (chunk translators, reviewers, terminology researchers) and consumed during QA gates and delivery.

## When to Create

- During terminology research when a high-impact term has no high-confidence evidence.
- During chunk translation when a term is ambiguous and no glossary entry resolves it.
- During any QA gate when a defect cannot be auto-resolved.
- Whenever a Worker_Subagent encounters an issue outside its authority.

## Persistence

File name: `unresolved-issues.md` in the workspace artifact directory.

## Schema

### Markdown Table Form

```markdown
# Unresolved Issues

| ID | Location | Issue | Options | Owner | Status |
|---|---|---|---|---|---|
| UI-001 | ch03-sec02, para 4 | Ambiguous pronoun "they" — unclear referent | A) "họ" (plural); B) "người đó" (singular neutral) | coordinator | open |
| UI-002 | glossary, row 12 | Term "compliance" — no high-confidence TL equivalent found | A) "tuân thủ"; B) "sự phù hợp"; C) escalate to client | terminology-researcher | open |
```

### Column Definitions

| Column | Type | Description |
|---|---|---|
| `ID` | string | Unique identifier. Use prefix `UI-` followed by a sequential number (e.g., `UI-001`, `UI-002`). |
| `Location` | string | Where the issue occurs — chunk ID, paragraph, glossary row, or artifact name. Use the same location identifiers as the Chunk_Manifest and Source_Map. |
| `Issue` | string | Clear, concise description of the unresolved problem. |
| `Options` | string | Candidate resolutions labeled A), B), C), etc. If no options are known yet, write "Needs research". |
| `Owner` | string | Role or person responsible for resolving. One of: `coordinator`, `terminology-researcher`, `style-researcher`, `chunk-translator`, `continuity-reviewer`, `fidelity-reviewer`, `formatting-reviewer`, or `client`. |
| `Status` | enum | Current resolution state. One of the values defined below. |

### Status Values

| Value | Meaning |
|---|---|
| `open` | Issue is unresolved and awaiting action. |
| `in-progress` | Owner is actively investigating or awaiting input. |
| `resolved` | A decision has been made; record the chosen option in the Notes or update the relevant artifact. |
| `deferred` | Intentionally postponed to a later phase or delivery cycle. |
| `wont-fix` | Accepted as-is after deliberate decision; rationale should be noted. |

## Usage Rules

1. Any role may **add** entries to the log.
2. Only the **Coordinator_Subagent** or the **client** may change status to `resolved` or `wont-fix`.
3. When an issue is resolved, the resolver should update the relevant artifact (Glossary, Style_Sheet, Story_Bible, Domain_Map, or chunk output) to reflect the decision.
4. The QA gates consume this log to verify that no `open` issues remain for the scope being checked.
5. Residual `open` or `deferred` items at delivery time must be reported in the QA_Report under residual risks.

## Cross-References

- Referenced by: `core/workflows/long-document.md` (Pass D state update), `core/workflows/terminology-research.md`, `core/workflows/qa-gates.md` (residual risk gate).
- Consumed by: `core/prompts/transcreate-coordinator.md`, `core/prompts/continuity-reviewer.md`, `core/prompts/fidelity-reviewer.md`, `core/prompts/formatting-reviewer.md`.
- Schema location: `core/schemas/unresolved-issues.md`.
