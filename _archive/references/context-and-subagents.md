# Context And Subagent Control

Use this file whenever the source is too large for one context window, translation spans multiple sessions, or subagents can help.

## Context Budget Rule

Never keep the full book or full document in active context unless it genuinely fits with room for QA.

Active context for a chunk should contain only:

- translation brief
- relevant style-sheet rules
- relevant glossary rows
- story bible/domain-map excerpt
- previous chunk summary
- next chunk summary when available
- current source chunk
- unresolved issues that affect this chunk

Everything else belongs in workspace artifacts.

## State Files

Maintain durable state:

- `translation-brief.md`
- `source-map.md`
- `glossary.csv` or `glossary.md`
- `style-sheet.md`
- `story-bible.md` or `domain-map.md`
- `chunk-manifest.csv`
- `chunk-summaries.md`
- `unresolved-issues.md`
- `qa-report.md`

Use stable chunk IDs everywhere. Save decisions, not long discussions.

## Chunk Manifest

Each chunk record should include:

- chunk ID
- source location
- word/page range
- semantic unit
- dependencies
- assigned worker
- status
- output path
- QA status
- notes

Statuses:

- `planned`
- `research-needed`
- `ready`
- `drafting`
- `drafted`
- `qa-needed`
- `revising`
- `done`
- `blocked`

## Overflow Prevention

Before translating a chunk:

1. Load only relevant artifact excerpts.
2. Use search to pull glossary rows for terms appearing in the chunk.
3. Include previous and next summaries, not full neighboring chunks.
4. Keep unresolved issues filtered to this section, character, term, or domain.
5. After translation, write a compact summary and unload raw source from working memory.

For context resets:

1. Re-open the manifest.
2. Re-open the brief, style sheet, glossary, and current chunk.
3. Reconstruct only the needed continuity from summaries.
4. Continue from the first non-done chunk.

## Subagent Readiness Gate

Do not use subagents until these exist:

- translation brief
- source map
- glossary with proposed core terms
- style sheet
- chunk manifest
- story bible or domain map when relevant

Subagents should not make global style decisions independently. They can propose changes, but the coordinator approves them.

## Good Subagent Roles

Use separate roles with non-overlapping scopes:

| Role | Scope | Output |
|---|---|---|
| Terminology researcher | A term list or chapter | glossary proposals with sources |
| Style researcher | Target genre/domain | style observations and source notes |
| Chunk translator | One chunk or chapter section | translated chunk plus uncertainty notes |
| Continuity reviewer | One chapter range | contradictions, timeline/name/pronoun issues |
| Technical QA reviewer | Tables, citations, numbers, units | defect list with source locations |
| Formatting reviewer | Output document | layout, anchors, headings, footnotes |

## Subagent Prompt Pattern

Give each subagent:

- role and chunk ID
- source chunk or term list
- target language and audience
- relevant brief excerpt
- relevant glossary rows
- relevant style-sheet rules
- relevant story/domain notes
- exact output contract

Example:

```text
You are translating chunk ch04-sc02 into Vietnamese for a faithful literary translation. Use the provided glossary and style rules. Return: (1) translated text, (2) uncertain terms, (3) glossary change proposals, (4) continuity notes. Do not translate outside this chunk.
```

## Parallel Work Rules

- Assign disjoint chunks or disjoint research scopes.
- Do not let two subagents edit the same output file.
- Require every subagent to list changed files or produced artifacts.
- Merge centrally.
- Resolve glossary conflicts before final voice pass.
- Run cross-chunk QA after parallel translation.

## Coordinator Merge Checklist

After subagent work:

- Check that every assigned chunk was returned.
- Compare against source for omissions and additions.
- Normalize term choices against glossary.
- Merge accepted glossary proposals.
- Update story bible/domain map.
- Update chunk summaries.
- Record rejected proposals with reason when they may recur.
- Queue global consistency issues for final QA.
