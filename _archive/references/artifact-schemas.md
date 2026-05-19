# Artifact Schemas

Use these lightweight schemas to keep long translation projects restartable and subagent-safe.

## translation-brief.md

```markdown
# Translation Brief

Source:
Target language:
Target locale:
Audience:
Mode:
Register:
Output format:
Formatting constraints:
Do-not-translate items:
Terminology authority:
Research depth:
QA bar:
Open questions:
```

## source-map.md

```markdown
# Source Map

## Overview
- Genre/domain:
- Purpose:
- Source quality:
- Extraction hazards:

## Structure
| ID | Source location | Type | Notes | Risk |
|---|---|---|---|---|

## High-Risk Items
| Item | Location | Risk | Needed action |
|---|---|---|---|
```

## glossary.csv

Recommended columns:

```csv
term,preferred_translation,forbidden_translation,term_class,context,source_location,evidence,confidence,status,notes
```

Status values:

- `proposed`
- `approved`
- `needs-review`
- `deprecated`

Confidence values:

- `high`
- `medium`
- `low`

## style-sheet.md

```markdown
# Style Sheet

## Voice
- Register:
- Formality:
- Sentence rhythm:
- Genre constraints:

## Language Conventions
- Dialogue punctuation:
- Titles/headings:
- Names:
- Terms of address:
- Honorifics:
- Numbers/dates/units:
- Citations:
- Footnotes/translator notes:

## Adaptation Rules
- Idioms:
- Humor:
- Cultural references:
- Metaphors:
- Repetition:
- Songs/poems/quoted material:

## Forbidden Patterns
- 
```

## story-bible.md

Use for fiction, memoir, narrative non-fiction, scripts, games, and comics.

```markdown
# Story Bible

## Characters
| Character | Name forms | Voice | Relationships | Notes |
|---|---|---|---|---|

## Timeline
| Event | Source location | Time marker | Notes |
|---|---|---|---|

## Places
| Place | Translation | Description | Notes |
|---|---|---|---|

## Continuity Threads
| Thread | First seen | Later payoff | Translation risk |
|---|---|---|---|

## Terms Of Address
| Speaker | Addressee | Source form | Target form | Rule |
|---|---|---|---|---|
```

## domain-map.md

Use for technical, legal, medical, financial, academic, product, or policy documents.

```markdown
# Domain Map

## Domain
- Field:
- Audience expertise:
- Governing standards/laws:
- Canonical sources:

## Concepts
| Concept | Definition | Preferred translation | Source/evidence |
|---|---|---|---|

## Acronyms
| Acronym | Expansion | Translation policy | Notes |
|---|---|---|---|

## Units And Formal Data
| Item | Policy | Notes |
|---|---|---|
```

## chunk-manifest.csv

Recommended columns:

```csv
chunk_id,source_location,word_or_page_range,semantic_unit,dependencies,assigned_to,status,output_path,qa_status,notes
```

## chunk-summaries.md

```markdown
# Chunk Summaries

## ch01-sec01
- Source range:
- What happened / main argument:
- Terms introduced:
- Continuity implications:
- Unresolved issues:
- Next chunk dependency:
```

## unresolved-issues.md

```markdown
# Unresolved Issues

| ID | Location | Issue | Options | Owner | Status |
|---|---|---|---|---|---|
```

## qa-report.md

```markdown
# QA Report

Scope checked:
Artifacts checked:
Checks performed:

| Issue | Location | Severity | Resolution |
|---|---|---|---|

Residual risks:
```
