# Translation Brief Schema

The Translation Brief is the intake artifact produced at the start of every translation task (Phase 1). It captures the project scope, constraints, and quality expectations before any chunk translation begins.

## Required Fields

The Translation_Agent MUST populate every field below. If a required field is missing and cannot be inferred at low risk, the agent SHALL ask the user a single focused question for that field before proceeding.

## Form

```markdown
# Translation Brief

## Source
- Source files:
- Source language:

## Target
- Target language:
- Target locale:

## Audience
- Audience:

## Translation Parameters
- Mode:
- Register:

## Output
- Output format:
- Formatting constraints:

## Constraints
- Do-not-translate items:
- Terminology authority:
- Research depth:

## Quality
- QA bar:

## Open Questions
- Open questions:
```

## Field Definitions

| Field | Description | Example values |
|---|---|---|
| Source files | Paths or identifiers of the source document(s) to translate | `source/chapter-01.md`, `source/manual.pdf` |
| Source language | BCP-47 language tag or plain name of the source language | `en`, `English`, `ja` |
| Target language | BCP-47 language tag or plain name of the target language | `vi`, `Vietnamese`, `fr` |
| Target locale | Regional variant or market for the target language | `vi-VN`, `fr-CA`, `pt-BR` |
| Audience | Description of the intended reader of the translated output | `General adult readers`, `Senior developers`, `Legal professionals` |
| Mode | Translation approach — faithful, transcreation, localization, or hybrid | `faithful`, `faithful + light transcreation for idioms`, `full transcreation` |
| Register | Formality and tone level for the target text | `formal`, `neutral`, `informal`, `literary` |
| Output format | File format and structure of the delivered translation | `Markdown`, `DOCX`, `plain text`, `same as source` |
| Formatting constraints | Rules about layout, line length, heading style, or structural requirements | `Preserve heading hierarchy`, `Max 80 chars/line`, `Keep table structure` |
| Do-not-translate items | Terms, names, code identifiers, or strings that must remain in the source language | `API names`, `brand names`, `code blocks`, specific terms list |
| Terminology authority | Primary source for term decisions — client glossary, official localization, domain standard | `Client-provided glossary`, `Microsoft Language Portal`, `ISO standards` |
| Research depth | How deeply the agent should research terminology and style before translating | `thorough` (full research), `standard` (key terms only), `minimal` (use existing glossary) |
| QA bar | Minimum quality standard the translation must meet before delivery | `publication-ready`, `internal review draft`, `machine-assisted first pass` |
| Open questions | Unresolved issues or ambiguities the agent needs clarified before or during translation | List of questions for the user or client |

## Defaults

When the user does not specify a value:

- **Mode**: defaults to `faithful translation with light transcreation for idioms and dialogue`
- **Research depth**: defaults to `standard`
- **QA bar**: defaults to `publication-ready`
- **Output format**: defaults to `same as source`

## Usage

- The Translation_Brief is produced once per translation task during Phase 1 (Intake).
- All subsequent phases (Scan, Research, Plan, Translate, Merge, QA) reference the brief.
- The brief is persisted as a file in the workspace (`translation-brief.md`) and is never stored only in chat history.
- The Coordinator_Subagent loads the brief (or relevant excerpt) when dispatching any Worker_Subagent.
