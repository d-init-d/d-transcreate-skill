# Fiction Short — Example Bundle

This example demonstrates the d-transcreate skill on a short original fantasy/adventure fiction piece (3 scenes, ~900 words total).

## Source Material

- **Genre:** Fantasy / Adventure
- **Title:** *The Lantern of Kael Morrow*
- **Language:** English
- **Word count:** ~900 words across 3 scenes

The story follows a young cartographer named Seren who discovers a magical lantern in a ruined tower. The lantern reveals hidden paths on any map it illuminates, but each use draws the attention of the Hollow — spectral entities that guard forgotten places.

## Translation Target

- **Target language:** Vietnamese (vi-VN)
- **Mode:** Faithful translation with light transcreation for idioms and dialogue
- **Register:** Literary
- **Audience:** General adult readers of fantasy fiction

## Seed Artifacts

| Artifact | Description |
|----------|-------------|
| `seed-artifacts/translation-brief.md` | Filled-in brief specifying scope, constraints, and quality bar |
| `seed-artifacts/glossary.csv` | 10 key terms with preferred Vietnamese renderings |
| `seed-artifacts/style-sheet.md` | 7 style rules covering voice, dialogue, and adaptation |

## How to Use

1. Point the d-transcreate skill at this directory as the project workspace.
2. The skill will load the seed artifacts during Phase 1 (Intake) and Phase 3 (Research).
3. Source files in `source/` will be scanned, chunked, and translated according to the brief.

## Content Notice

All source text in this example is **original fiction** created specifically for demonstration purposes. It is not derived from any published work.
