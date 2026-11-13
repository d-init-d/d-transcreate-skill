# D-Research Module Workflow

This workflow defines how `d-transcreate` activates `d-research` (`d-research-skill`) as a modular Phase 3 research engine to produce **Research_Dossier** (`research-dossier.md`) before any chunk translation begins.

Run this workflow at the start of Phase 3 (after `Translation_Brief` and `Source_Map` exist on disk) so terminology, style, pronoun/address, and transcreation-mindset decisions are grounded in live evidence before Phase 4 planning and Phase 5 translation.

---

## Module Discovery (3-Tier Resolution)

Resolve the `d-research` engine in strict tier order unless the `Translation_Brief` explicitly disables live web research:

1. **Tier 1 — Host-installed `d-research` skill:**
   Check standard host skill locations:
   - `~/.gemini/config/skills/d-research-skill/SKILL.md`
   - `.claude/skills/d-research/SKILL.md`
   - `.agents/skills/d-research/SKILL.md`
2. **Tier 2 — Bundled or linked module directory:**
   If Tier 1 is not present, check inside the skill pack or adjacent workspace:
   - `modules/d-research/SKILL.md`
   - `../d-research-skill/SKILL.md`
3. **Tier 3 — Internal search fallback:**
   If neither Tier 1 nor Tier 2 is present (or `d-research` is disabled), execute the exact same Phase 3 protocol using the host platform's native web search and browser/fetch tools. If no network/search tools are available, run offline reconnaissance from source text and training knowledge while marking unverified entries `medium` or `low` confidence.

Under **all three tiers**, produce the exact same workspace artifacts (`research-dossier.md`, `evidence-ledger.jsonl`, and `research-coverage.json`) so the translation workflow never blocks.

---

## Workspace Telemetry Sync

Whenever Phase 3 research runs (under Tier 1, Tier 2, or Tier 3), keep research telemetry synchronized in the project workspace:

- **`evidence-ledger.jsonl`** (or `evidence-ledger.csv` when CSV tooling is used): Append one structured evidence record per verified source or claim (`claim_id`, `sub_question`, `source_title`, `source_url`, `source_type`, `date_accessed`, `access_method`, `evidence`, `quote_or_anchor`, `contradiction`, `confidence`, `notes`).
- **`research-coverage.json`**: Record which discovery branches (`documentary`, `community_social`), language queries, and sub-questions were executed, deferred, or blocked, along with `d_research_mode`.
- Record `d_research_mode` in `research-dossier.md` as one of:
  - `skill_host` (Tier 1)
  - `module_bundled` (Tier 2)
  - `internal_search_fallback` (Tier 3 with live search/browser)
  - `offline_knowledge_fallback` (Tier 3 offline)

---

## Step 1 — Work & Prior-Translation Reconnaissance (`Work_Classification`)

Start **dual-track discovery** in round one for the source work, author, and target language:

- **Documentary track:** Search official publishers, rights-holder portals, national library catalogs, major bookstores, standards bodies, and academic databases.
- **Community and social track:** Search Goodreads, reader forums, book blogs, translation wikis, and specialist review threads.

When `d-research` reference modules exist in the resolved skill directory, load and apply them as needed:

- `references/multilingual-research.md` — cross-language query generation in both source and target languages.
- `references/vietnamese-source-discovery.md` — Vietnamese alias construction (with and without diacritics) and local publishing/news/community basins when Vietnamese is the source or target language.
- `references/register-and-jargon-expansion.md` — bidirectional 4-rung register expansion when domain or community recall is thin.

Classify `prior_translation_status` in `research-dossier.md` under `## Work Classification`:

| Status | Criteria | Track to Execute |
|---|---|---|
| `official_published` | Licensed/official target-language edition exists | Track A (plus voice grounding) |
| `community_established` | Unofficial/fan translation ecosystem has stabilized canonical terms | Track A (plus voice grounding) |
| `partial` | Excerpts, serialized chapters, summaries, or same-universe works exist | Track A + Track B |
| `none` | Uncharted work with no known target-language translation | Track B |

---

## Step 2A — Track A: Prior-Translation Harvesting (`official_published` | `community_established` | `partial`)

When an existing target-language translation or ecosystem exists, perform structured **prior-translation harvesting**:

1. **Harvest canonical renderings** across:
   - Character names, nicknames, and epithets
   - Place names (toponyms) and landmarks
   - Organizations, factions, ranks, and official titles
   - Skill, magic, technology, and worldbuilding terms
   - Recurring motifs, artifacts, and specialized domain concepts
2. **Enforce strict copyright rules:** Extract terms, naming policies, structural observations, and short attributed quotes (one sentence maximum) only. Never copy extended prose or patch together existing translations.
3. **Audit existing editions and extract pitfalls:**
   - Record each examined edition/source in `## Existing Translations Audit` with strengths to inherit and mistranslations or pitfalls to avoid.
   - Record accepted canonical terms as `preferred_translation` (with `evidence` and `confidence`).
   - Record known mistranslations, awkward literal calques, or outdated/disputed renderings in `forbidden_translation` (semicolon-separated) so deterministic QA enforces avoidance.
4. **Map established address pairings:** Record established pronoun and terms-of-address pairings used between key characters in `## Pronoun and Address Matrix`.
5. **Ground authorial voice:** Briefly complete `## Authorial Intent and Context` and `## Transcreation Mindset and Voice Compass` so translators preserve the source's voice while adhering to harvested canonical terms.

---

## Step 2B — Track B: Authorial Intent & Mindset Formation (`none` — Uncharted Work)

When no prior target-language translation exists (or when `partial` coverage leaves core voice/terminology unmapped), perform **authorial intent** analysis and **mindset formation** to build the Transcreation Mindset & Voice Compass from primary context:

1. **Historical, Cultural & Domain Context:** Research the era, geopolitical/cultural setting, social hierarchy, philosophical or religious backdrop, or technical/legal domain norms underlying the source work.
2. **Authorial Intent & Core Purpose:** Investigate why the author wrote the work, its emotional and intellectual core, narrative pacing, target readership in the source culture, and `source_voice_signature`.
3. **Register Ladder Mapping:** Map how the work moves across the 4-rung register ladder (`Canonical / Formal` <-> `Mainstream / Lay` <-> `Community / Domain Jargon` <-> `Vernacular / Slang`) in both directions so target-language prose hits the intended rung on every passage without flattening.
4. **Transcreation Mindset & Voice Compass:** Formulate concrete target-language guidance in `research-dossier.md`:
   - `mindset_summary` — core transcreation stance and fidelity-vs-adaptation balance.
   - `target_style_anchor` — comparable target-language literary or domain style benchmark.
   - `register_ladder_target` — concrete target-language equivalents for each of the 4 register rungs.
   - `vocabulary_balance` — target ratio and usage boundaries between classical/Sino-target loan vocabulary and native vernacular vocabulary.
   - `Pronoun and Address Matrix` — speaker/addressee dynamic, target pronouns, and shift/reveal rules.
   - `neologism_and_adaptation_policy` — rules for coining new terms, translating vs. retaining proper nouns, and handling culture-bound concepts.

---

## Step 3 — Handoff to Project Artifacts

Workers propose research findings; only the Coordinator writes shared project artifacts. Once Phase 3 proposals are reviewed and approved, the Coordinator updates:

1. **`research-dossier.md`** (`core/schemas/research-dossier.md`) — canonical Phase 3 record stored in the workspace.
2. **`glossary.csv`** (`core/schemas/glossary.md`) — populated via **Two-Tier Glossary Seeding**:
   - First seed pre-solved terms from Global Translation Memory (`memory/glossary-<target_lang>.csv`, e.g., `memory/glossary-vi.csv`) using `scripts/book_ops.py sync-glossary --workspace <dir> --seed --target-lang <lang>`.
   - Then merge approved Track A harvested terms (including `forbidden_translation` pitfalls) and Track B coined/verified terms.
3. **`style-sheet.md`** (`core/schemas/style-sheet.md`) — populated with the Voice Compass, register rules, target locale profile (e.g., `core/locales/vi-VN.md` when Vietnamese), and Forbidden Patterns derived from Track A mistranslations and Track B anti-translatorese guards.
4. **`story-bible.md`** or **`domain-map.md`** — seeded with `Pronoun and Address Matrix` entries, character/place/concept entries, and reveal-timing protections.

High-impact terms or style conflicts without high-confidence resolution are logged by the Coordinator in `unresolved-issues.md` (`core/schemas/unresolved-issues.md`).

---

## References

- Research Dossier schema: `core/schemas/research-dossier.md`
- Research Dossier template: `templates/research-dossier.md`
- Terminology research workflow: `core/workflows/terminology-research.md`
- Glossary schema: `core/schemas/glossary.md`
- Style Sheet schema: `core/schemas/style-sheet.md`
- Subagent orchestration and single-writer boundaries: `core/workflows/subagents.md`
