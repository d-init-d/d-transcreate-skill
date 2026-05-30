# Legal Policy — Example Bundle

This example demonstrates the d-transcreate skill on a short original privacy policy excerpt from a fictional technology company.

## Source Material

- **Genre:** Legal / Policy
- **Title:** *NovaTech Solutions — Privacy Policy (Excerpt)*
- **Language:** English
- **Word count:** ~400 words

The excerpt covers data collection practices, user consent mechanisms, and data retention policies for NovaTech Solutions, a fictional cloud-based project management platform. The language is formal, precise, and unambiguous — typical of corporate privacy policies intended for a general audience.

## Translation Target

- **Target language:** Vietnamese (vi-VN)
- **Mode:** Faithful translation
- **Register:** Formal
- **Audience:** Vietnamese users of the NovaTech platform; legal/compliance reviewers

## Seed Artifacts

| Artifact | Description |
|----------|-------------|
| `seed-artifacts/translation-brief.md` | Filled-in brief specifying scope, constraints, and quality bar |
| `seed-artifacts/glossary.csv` | 12 legal/policy terms with preferred Vietnamese renderings |
| `seed-artifacts/style-sheet.md` | 8 style rules covering voice, conventions, and forbidden patterns |

## How to Use

1. Point the d-transcreate skill at this directory as the project workspace.
2. The skill will load the seed artifacts during Phase 1 (Intake) and Phase 3 (Research).
3. Source files in `source/` will be scanned, chunked, and translated according to the brief.

## Content Notice

All source text in this example is **original content** created specifically for demonstration purposes. NovaTech Solutions is a fictional company. This policy is not derived from any real company's privacy policy or legal document.

This example omits an explicit `domain-map.md` (Domain_Map); for this short excerpt the glossary captures the controlled legal terms. A full legal project would build a Domain_Map during Phase 2.
