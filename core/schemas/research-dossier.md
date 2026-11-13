# Research Dossier Schema

The Research Dossier (`research-dossier.md`) is the canonical Phase 3 reconnaissance and transcreation-compass artifact produced by `core/workflows/d-research-module.md` before chunk translation begins. It captures work classification, prior-translation audits (Track A), authorial intent and transcreation mindset (Track B), the pronoun/address matrix, and harvested special terms.

The Coordinator holds final write authority over `research-dossier.md`. Dispatched researchers (`terminology-researcher` and `style-researcher`) return structured proposals that the Coordinator reviews and consolidates into this artifact.

**Copyright rule:** Existing translations may inform terminology, naming, and style observations only. Never reproduce extended passages from copyrighted translations; record short attributed evidence quotes (one sentence maximum) or paraphrased observations.

---

## Template

```markdown
# Research Dossier

## Work Classification
- source_title:
- author:
- source_language:
- target_language:
- genre_or_domain:
- prior_translation_status:
- d_research_mode:

## Authorial Intent and Context
- historical_cultural_setting:
- authorial_intent:
- core_themes:
- source_voice_signature:

## Existing Translations Audit
| Edition / Source | Translator / Publisher | Status | Strengths to Inherit | Mistranslations / Pitfalls to Avoid |
|---|---|---|---|---|

## Transcreation Mindset and Voice Compass
- mindset_summary:
- target_style_anchor:
- register_ladder_target:
- vocabulary_balance:
- neologism_and_adaptation_policy:

## Pronoun and Address Matrix
| Speaker | Addressee | Relationship / Dynamic | Source Form | Target Form | Shift / Reveal Rule |
|---|---|---|---|---|---|

## Harvested Special Terms and Proper Nouns
| Term | Category | Preferred Rendering | Forbidden Rendering | Source / Evidence | Confidence |
|---|---|---|---|---|---|
```

---

## Section and Field Reference

### Work Classification

| Field | Allowed / Expected Values | Description |
|---|---|---|
| `source_title` | string | Canonical title of the source work |
| `author` | string | Author or issuing organization |
| `source_language` | BCP-47 or language name | Language of the source material |
| `target_language` | BCP-47 or language name | Target language and locale |
| `genre_or_domain` | string | Literary genre or technical/legal/policy domain |
| `prior_translation_status` | `official_published`, `community_established`, `partial`, `none` | Governs Track A vs. Track B execution |
| `d_research_mode` | `skill_host`, `module_bundled`, `internal_search_fallback`, `offline_knowledge_fallback` | Discovery tier used during Phase 3 |

### Authorial Intent and Context

| Field | Description |
|---|---|
| `historical_cultural_setting` | Era, geographical/cultural setting, social hierarchy, philosophical backdrop, or domain environment |
| `authorial_intent` | Why the author wrote the work, intended emotional/intellectual impact, and core purpose |
| `core_themes` | Central motifs, arguments, or narrative tensions that must survive transcreation |
| `source_voice_signature` | Defining rhythmic, lexical, tonal, and syntactic traits of the source author |

### Existing Translations Audit

Tracks prior target-language editions, partial translations, or community equivalents (Track A). Leave empty with a single `N/A — uncharted work` note row when `prior_translation_status` is `none`.

| Column | Description |
|---|---|
| `Edition / Source` | Edition title, publisher page, wiki, or URL reference |
| `Translator / Publisher` | Translator name and publisher/community group |
| `Status` | `official_published`, `community_established`, `partial`, or `deprecated` |
| `Strengths to Inherit` | Naming conventions, tone choices, or structural solutions worth preserving |
| `Mistranslations / Pitfalls to Avoid` | Known errors, awkward calques, or inconsistent renderings to feed into `forbidden_translation` / Forbidden Patterns |

### Transcreation Mindset and Voice Compass

| Field | Description |
|---|---|
| `mindset_summary` | Overall transcreation philosophy and balance between literal fidelity and natural target-language expression |
| `target_style_anchor` | Reference target-language literary or domain register benchmark |
| `register_ladder_target` | Mapping across all 4 register rungs (`Canonical/Formal` <-> `Mainstream/Lay` <-> `Community/Domain Jargon` <-> `Vernacular/Slang`) |
| `vocabulary_balance` | Policy balancing classical/Sino-target vocabulary vs. native vernacular vocabulary |
| `neologism_and_adaptation_policy` | Rules for coining new terms, retain-vs-translate proper nouns, and handling culture-bound concepts |

### Pronoun and Address Matrix

| Column | Description |
|---|---|
| `Speaker` | Speaking character, narrator, or institutional voice |
| `Addressee` | Addressed character, group, or reader persona |
| `Relationship / Dynamic` | Age, rank, kinship, power, or intimacy dynamic |
| `Source Form` | Source pronoun, title, or address form |
| `Target Form` | Approved target-language pronoun/address pair |
| `Shift / Reveal Rule` | Conditions under which address shifts, or reveal-timing constraints |

### Harvested Special Terms and Proper Nouns

| Column | Description |
|---|---|
| `Term` | Source-language term or proper noun |
| `Category` | `character`, `place`, `organization`, `rank_title`, `magic_skill`, `motif`, `domain_concept`, or `neologism` |
| `Preferred Rendering` | Proposed or approved target-language rendering |
| `Forbidden Rendering` | Known mistranslations or deprecated variants (semicolon-separated) |
| `Source / Evidence` | Citation URL, edition note, or research method |
| `Confidence` | `high`, `medium`, or `low` |

---

## Maintenance Rules

1. **Create before translation:** Produce `research-dossier.md` in Phase 3 before Phase 4 chunk dispatch or Phase 5 translation begins.
2. **Seed downstream artifacts:** Copy approved terms into `glossary.csv`, voice/register rules into `style-sheet.md`, and character/address/concept entries into `story-bible.md` or `domain-map.md`.
3. **Single-writer authority:** Only the Coordinator edits `research-dossier.md` directly; workers propose updates via `dossier_proposals`.
4. **Consume during execution:** Chunk Translators consult the Mindset & Voice Compass and Pronoun Matrix before Pass A; Continuity Reviewers verify adherence during Peer Cross-Check; the Coordinator uses it during the Phase 6 final voice pass.
