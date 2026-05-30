# Glossary Schema

The Glossary artifact records terminology decisions for a translation project. It is the single authoritative source for how terms are rendered in the target language. The Coordinator_Subagent holds final authority over Glossary entries; Worker_Subagents propose changes only.

## Columns

| Column | Type | Required | Description |
|---|---|---|---|
| `term` | string | yes | Source-language term exactly as it appears in the source text. |
| `preferred_translation` | string | yes | Approved target-language rendering. |
| `forbidden_translation` | string | no | Known incorrect or misleading renderings that must not be used. Separate multiple values with a semicolon. |
| `term_class` | string | yes | Grammatical or domain class (e.g., `noun`, `verb`, `proper-name`, `acronym`, `UI-string`, `unit`, `legal-term`). |
| `context` | string | no | Brief note on where or how the term is used, to disambiguate homonyms. |
| `source_location` | string | yes | First or most representative occurrence in the source (e.g., `ch03-p42`, `§2.1`). |
| `evidence` | string | no | Short attributed quote or paraphrased observation supporting the preferred translation. Must comply with copyright rules (no extended reproduction). |
| `confidence` | enum | yes | One of: `high`, `medium`, `low`. |
| `status` | enum | yes | One of: `proposed`, `approved`, `needs-review`, `deprecated`. |
| `notes` | string | no | Free-form notes — rationale, alternative candidates considered, links to Unresolved_Issues_Log entries. |

## Enumerations

### `status`

| Value | Meaning |
|---|---|
| `proposed` | Candidate entry awaiting coordinator review. |
| `approved` | Accepted by coordinator; all chunks must use this rendering. |
| `needs-review` | High-impact term with insufficient evidence; logged in Unresolved_Issues_Log. |
| `deprecated` | Previously approved but superseded; retained for audit trail. |

### `confidence`

| Value | Meaning |
|---|---|
| `high` | Supported by official localized source, rights-holder glossary, or authoritative reference. |
| `medium` | Supported by multiple credible secondary sources or established community usage. |
| `low` | Based on inference, single informal source, or machine-translation output. |

## CSV Form

Use this format when the Glossary is persisted as `glossary.csv`:

```csv
term,preferred_translation,forbidden_translation,term_class,context,source_location,evidence,confidence,status,notes
```

Rules:
- Header row is mandatory.
- Fields containing commas, quotes, or newlines must be enclosed in double quotes.
- Use UTF-8 encoding without BOM.
- One row per term. If a term has multiple senses, create separate rows with disambiguating `context` values.

### Example

```csv
term,preferred_translation,forbidden_translation,term_class,context,source_location,evidence,confidence,status,notes
Horcrux,Trường sinh linh giá,Hộp linh hồn;Vật chứa linh hồn,proper-name,dark magic artifact,ch06-p112,"Official VN publisher edition uses 'Trường sinh linh giá'",high,approved,
Muggle,Muggle,Ma-gồ;Người thường,proper-name,non-magical person,ch01-p7,"Rights-holder style guide mandates untranslated 'Muggle'",high,approved,Keep original per publisher directive
Apparition,Hiện hình,Dịch chuyển tức thời,noun,magical teleportation,ch04-p58,"Paraphrased from official glossary appendix",medium,proposed,Verify against latest edition
```

## Markdown Table Form

Use this format when the Glossary is embedded in a Markdown document (e.g., for inline review or when CSV tooling is unavailable):

```markdown
# Glossary

| term | preferred_translation | forbidden_translation | term_class | context | source_location | evidence | confidence | status | notes |
|---|---|---|---|---|---|---|---|---|---|
| Horcrux | Trường sinh linh giá | Hộp linh hồn; Vật chứa linh hồn | proper-name | dark magic artifact | ch06-p112 | Official VN publisher edition uses 'Trường sinh linh giá' | high | approved | |
| Muggle | Muggle | Ma-gồ; Người thường | proper-name | non-magical person | ch01-p7 | Rights-holder style guide mandates untranslated 'Muggle' | high | approved | Keep original per publisher directive |
| Apparition | Hiện hình | Dịch chuyển tức thời | noun | magical teleportation | ch04-p58 | Paraphrased from official glossary appendix | medium | proposed | Verify against latest edition |
```

## Usage Rules

1. **Before chunk translation begins**, the Glossary must contain at least the core terms mined during the terminology research phase (Phase 3).
2. **During translation**, a chunk-translator loads only the Glossary rows relevant to its assigned chunk (not the full Glossary).
3. **Proposals**: Worker_Subagents propose new entries or edits by returning structured proposals in their output. The Coordinator_Subagent reviews and either approves (setting `status` to `approved`) or rejects.
4. **QA enforcement**: The terminology QA gate verifies that every `approved` entry is applied consistently across all chunks and that no `forbidden_translation` value appears in the output.
5. **Conflict resolution**: When multiple sources disagree, record both candidates with their evidence. The Coordinator resolves based on the source priority order defined in `core/workflows/terminology-research.md`.
6. **Unresolved terms**: If a term is high-impact and no high-confidence evidence is found, set `status` to `needs-review` and add an entry to the Unresolved_Issues_Log.
7. **Low-impact terms**: If research yields no new candidates for a low-impact term, mark it as `proposed` with `confidence: low` and continue translation rather than blocking.

## References

- Column requirements, status, and confidence enumerations: defined in the schema tables above.
- Source priority order: `core/workflows/terminology-research.md`
- QA terminology gate: `core/workflows/qa-gates.md`
- Schema existence validation: enforced by `scripts/validate_pack.py`
