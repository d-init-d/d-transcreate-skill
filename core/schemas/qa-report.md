# QA Report Schema

The QA_Report is the final artifact produced after running all eight QA gates (see `core/workflows/qa-gates.md`). It summarizes the quality assurance pass and documents any residual risks before delivery.

Persist this artifact as `qa-report.md` in the workspace alongside the translated output.

---

## Scope

Describe the boundaries of this QA pass.

```markdown
## Scope

- Project: <project or document title>
- Source language: <source language>
- Target language: <target language>
- Chunks covered: <all | list of chunk_ids>
- Gates executed: <all 8 | list of gate names>
- Date: <ISO-8601 date>
- Reviewer: <Coordinator_Subagent | human reviewer name>
```

---

## Artifacts Checked

List every artifact consulted during the QA pass.

```markdown
## Artifacts Checked

| Artifact | Version / Timestamp | Notes |
|----------|---------------------|-------|
| Translation_Brief | <timestamp or commit> | |
| Source_Map | <timestamp or commit> | |
| Glossary | <timestamp or commit> | <N approved entries, M needs-review> |
| Style_Sheet | <timestamp or commit> | |
| Story_Bible / Domain_Map | <timestamp or commit> | <which one, or N/A> |
| Chunk_Manifest | <timestamp or commit> | <N chunks total, all done> |
| Chunk_Summaries | <timestamp or commit> | |
| Unresolved_Issues_Log | <timestamp or commit> | <N open items> |
```

---

## Checks Performed

Record which gates were executed and their pass/fail status.

```markdown
## Checks Performed

| Gate | Name | Status | Findings |
|------|------|--------|----------|
| 1 | Completeness | pass / fail / partial | <summary or "no issues"> |
| 2 | Fidelity | pass / fail / partial | <summary or "no issues"> |
| 3 | Terminology | pass / fail / partial | <summary or "no issues"> |
| 4 | Target-Language Quality | pass / fail / partial | <summary or "no issues"> |
| 5 | Continuity | pass / fail / partial | <summary or "no issues"> |
| 6 | Numbers and Formal Data | pass / fail / partial | <summary or "no issues"> |
| 7 | Formatting | pass / fail / partial | <summary or "no issues"> |
| 8 | Residual Risk Report | pass / fail / partial | <summary or "no issues"> |
```

Status values:

- `pass` — gate completed with no issues found.
- `fail` — gate found issues that were resolved before delivery.
- `partial` — gate could not be fully executed (document reason in Findings).

---

## Issues Table

Log every issue found during the QA pass. Each row represents one defect or concern.

```markdown
## Issues

| ID | Gate | Location | Severity | Description | Resolution | Status |
|----|------|----------|----------|-------------|------------|--------|
| QA-001 | <gate number or name> | <chunk_id, paragraph, or page> | critical / major / minor | <what is wrong> | <how it was fixed or escalated> | resolved / escalated / accepted-risk |
```

Severity values:

- `critical` — meaning is wrong, data is corrupted, or content is missing. Must be resolved before delivery.
- `major` — noticeable quality issue (inconsistency, awkward phrasing, terminology drift). Should be resolved.
- `minor` — cosmetic or stylistic preference. May be accepted as residual risk.

Status values:

- `resolved` — issue was fixed in the output.
- `escalated` — issue requires human decision; added to Unresolved_Issues_Log.
- `accepted-risk` — issue is documented but delivery proceeds (recorded in Residual Risks below).

---

## Residual Risks

Document remaining uncertainties and known limitations carried forward to delivery. Keep this section short and actionable for the end user.

```markdown
## Residual Risks

| ID | Category | Description | Impact | Recommendation |
|----|----------|-------------|--------|----------------|
| RR-001 | terminology | <term> remains marked needs-review in Glossary | <potential misunderstanding> | Human domain expert review recommended |
| RR-002 | source-quality | <pages/sections> had OCR noise; best-effort reconstruction applied | <possible inaccuracy> | Compare against physical source |
| RR-003 | ambiguity | <passage> has multiple valid interpretations | <reader may misread intent> | Author clarification recommended |
| RR-004 | formatting | <element> could not be preserved in target format | <layout difference> | Manual adjustment in final layout |
| RR-005 | domain-confidence | <section> confidence below high for high-stakes material | <risk of inaccuracy> | Human domain review required |
```

Category values:

- `terminology` — unresolved or low-confidence term decisions.
- `source-quality` — extraction defects (OCR, encoding, missing pages).
- `verification` — sources that could not be independently verified.
- `ambiguity` — high-impact passages with multiple valid readings.
- `formatting` — layout elements not fully preserved.
- `domain-confidence` — sections needing human domain review.

---

## High-Stakes Material Addendum

When the source is high-stakes legal, medical, financial, academic, or safety material, the QA_Report must additionally:

1. Confirm that all terminology decisions are source-backed (no provisional terms in final output).
2. Include explicit residual-risk notes for any section where confidence is below `high`.
3. Flag sections requiring mandatory human domain review before publication.

```markdown
## High-Stakes Addendum

- All terminology decisions source-backed: yes / no (list exceptions)
- Sections requiring human review: <list of chunk_ids or section references>
- Confidence below high: <list of items with rationale>
```

---

## Usage Notes

- The QA_Report is produced by the Coordinator_Subagent after all eight gates complete.
- Worker_Subagents write findings to the Unresolved_Issues_Log; the Coordinator compiles the final report.
- The report must be persisted to the workspace (not kept only in chat history).
- On resume after interruption, the agent checks whether a QA_Report already exists and whether it covers all chunks currently at `done` status.
