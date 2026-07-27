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

This skill defines seven specialized roles that can be dispatched as subagents: Transcreate Coordinator, Terminology Researcher, Style Researcher, Chunk Translator, Continuity Reviewer, Fidelity Reviewer, and Formatting Reviewer. Workers propose; only the Coordinator writes shared artifacts. The authoritative role table lives in `core/workflows/subagents.md`.

Subagent definitions are located under `.claude/agents/`. Start every dispatched worker prompt with the Worker Contract Card from `core/workflows/subagents.md`.

## Key Directories

- `core/` — Single source of truth: workflows, schemas, and subagent prompts.
- `core/workflows/` — Detailed workflow guides (long-document, terminology, QA, etc.).
- `core/schemas/` — Artifact templates (glossary, style-sheet, chunk-manifest, etc.).
- `core/prompts/` — Canonical role prompts for the seven subagent roles.
- `.claude/agents/` — Claude-specific subagent wrappers pointing to core prompts.

## Quick Start

1. Read `.claude/skills/d-transcreate/SKILL.md` for the skill overview.
2. Follow the eight-phase workflow: Intake → Scan → Research → Plan → Translate → Merge → QA → Delivery.
3. Persist all artifacts (brief, glossary, style sheet, manifest, summaries) as workspace files.
4. When dispatching subagents, use the files under `.claude/agents/`.
