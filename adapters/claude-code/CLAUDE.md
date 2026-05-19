# D Transcreate Skill

This project contains a translation and transcreation skill pack for long documents.
Use it when you need to translate books, technical manuals, legal texts, fiction,
scripts, or any substantial document with controlled terminology, consistent voice,
and durable state across sessions.

## Skill Entrypoint

Read the Claude skill file for full instructions:

→ `.claude/skills/d-transcreate/SKILL.md`

That file references the canonical workflow at `core/d-transcreate.md`.

## Subagent Roles

This skill defines seven specialized roles that can be dispatched as subagents:

1. **Transcreate Coordinator** — final authority on glossary, style, voice, continuity, and merge.
2. **Terminology Researcher** — mines and proposes terms; never writes global glossary directly.
3. **Style Researcher** — researches target-language conventions; proposes style rules.
4. **Chunk Translator** — owns one chunk through the multi-pass translation cycle.
5. **Continuity Reviewer** — checks cross-chunk consistency and story/domain continuity.
6. **Fidelity Reviewer** — checks source faithfulness (omissions, additions, distortions).
7. **Formatting Reviewer** — checks structural and formatting integrity.

Subagent definitions are located under `.claude/agents/`.

## Key Directories

- `core/` — Single source of truth: workflows, schemas, and subagent prompts.
- `core/workflows/` — Detailed workflow guides (long-document, terminology, QA, etc.).
- `core/schemas/` — Artifact templates (glossary, style-sheet, chunk-manifest, etc.).
- `core/prompts/` — Canonical role prompts for the seven subagent roles.
- `.claude/agents/` — Claude-specific subagent wrappers pointing to core prompts.

## Quick Start

1. Read `.claude/skills/d-transcreate/SKILL.md` for the skill overview.
2. Follow the seven-phase workflow: Intake → Scan → Research → Plan → Translate → Coordinate → QA.
3. Persist all artifacts (brief, glossary, style sheet, manifest, summaries) as workspace files.
4. When dispatching subagents, use the files under `.claude/agents/`.
