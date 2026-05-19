# Example: Technical Manual — StreamForge Data Pipeline Tool

## Overview

This example demonstrates how to use the `d-transcreate-skill` pack to translate a technical product manual from English to Vietnamese. The source material is an original, fictional developer tool called **StreamForge** — a data pipeline orchestration platform.

## Contents

```
technical-manual/
├── README.md                              ← You are here
├── source/
│   ├── section-01-overview.md             ← Product overview (~300 words)
│   ├── section-02-installation.md         ← Installation guide (~300 words)
│   └── section-03-configuration.md        ← Configuration reference (~300 words)
└── seed-artifacts/
    ├── translation-brief.md               ← Filled-in brief for EN→VI
    ├── glossary.csv                        ← 10 technical term entries
    └── style-sheet.md                      ← 7 style rules for technical writing
```

## How to Use

1. **Install the skill** into your agent platform using the appropriate adapter.
2. **Point the agent** at this directory as the project workspace.
3. **Invoke the translation task** — the agent will read the `seed-artifacts/translation-brief.md` to understand scope, load the glossary and style sheet, then proceed through the standard workflow (scan → research → plan → translate → QA).

## Notes

- All source text is **original content** created for this example. It does not come from any real product documentation.
- The seed artifacts are pre-filled to demonstrate the expected format. In a real project, the agent would produce these during the Research phase.
- Target language: Vietnamese (vi-VN).
- Domain: Developer tooling / data engineering.

## Expected Outcome

After running the full workflow, you should have:
- A Vietnamese translation of all three source sections
- An expanded glossary with any new terms discovered during translation
- A QA report confirming completeness, fidelity, and terminology consistency
