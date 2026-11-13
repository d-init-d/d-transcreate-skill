# D Transcreate — Canonical Entrypoint

Version: 1.0.0

Use this skill to translate or transcreate long documents with controlled terminology,
consistent voice, and durable state across context windows.

## Operating Principles

0. Record the skill version in the Translation_Brief and final QA_Report so the
   translation can be reproduced or audited later.
1. Preserve meaning, intent, register, structure, and factual accuracy before surface fluency.
2. Translate literally only when literal wording carries the intended effect.
3. Prefer natural target-language prose when idioms, humor, slogans, dialogue, or cultural references need adaptation.
4. Never silently invent, omit, simplify, or reorder source meaning.
5. Mark uncertainty with a concrete note and a proposed resolution path.
6. Do not copy existing copyrighted translations — use lawful samples only to infer terminology, register, and structural conventions.
7. Keep reusable decisions in artifacts (files on disk), not in chat history.
8. Before chunking or subagent dispatch, create a Context_Plan that records context assumptions, budget, chunk-size limits, and fallback mode.
9. Use a Subagent_Dispatch_Plan whenever work is delegated; workers receive scoped slices and proposals flow back to the Coordinator.

## Core Workflow

The workflow has eight phases. This numbering is canonical: every workflow,
schema, prompt, and adapter in this pack uses the same phase numbers.

### Phase 1 — Intake

Identify source files, target language, audience, output format, translation mode, and quality bar.
Default to faithful translation with light transcreation for idioms and dialogue when mode is unspecified.
In **Zero-Config Book Mode**, run `scripts/book_ops.py init` to scaffold the workspace, populate defaults in the **Translation_Brief**, seed the project glossary from `memory/glossary-<lang>.csv`, and link target locale profiles (such as `core/locales/vi-VN.md`).
Produce a **Translation_Brief** before any chunk translation begins.

### Phase 2 — Whole-Document Scan

Inspect the full document once. For books and multi-file sources (including `.pdf`, `.epub`, `.md`, `.txt`, and `.html`), run `scripts/book_ops.py scan` to detect chapters/sections, automatically convert `.pdf` inputs into clean `.txt` and `.epub` files under `<workspace>/converted_source/`, split oversized units at paragraph boundaries, materialize `source_chunks/`, and generate `source-map.md`, `chunk-manifest.csv`, and `.book-scan-meta.json`. You can also run `scripts/book_ops.py convert` directly to normalize a `.pdf` into `.epub` and/or `.txt`.
Create a **Source_Map**: sections, chapters, tables, figures, notes, references, captions, appendices, repeated blocks, and formatting hazards.
For fiction: build a **Story_Bible** (characters, timeline, POV, motifs, terms of address).
For technical/legal/medical: build a **Domain_Map** (concepts, standards, acronyms, units, formal data).

### Phase 3 — Research Terminology and Style

Mine candidate terms before translating. Activate `core/workflows/d-research-module.md` to produce a **Research_Dossier** (`core/schemas/research-dossier.md`) covering Track A (prior-translation term harvesting and pitfall auditing) and Track B (context, authorial intent, and transcreation mindset compass) before chunk translation starts.
Seed `glossary.csv` from Tier-1 shared memory (`memory/glossary-<lang>.csv`) and build an initial **Style_Sheet** aligned with the target locale profile (e.g., `core/locales/vi-VN.md`).
If `d-research-skill` is accessible, use it for source discovery and evidence logging (`evidence-ledger.jsonl` and `research-coverage.json`).
Researcher roles may be dispatched in this phase under the research-tier gate defined in `core/workflows/subagents.md`.

### Phase 4 — Plan

Create a **Context_Plan** first to record context budget, chunk-size limits, and fallback triggers.
Then segment by semantic boundaries (chapter, scene, section, subsection, table/figure group) within the Context_Plan's chunk-size limits.
Keep each chunk small enough for one pass with room for brief, glossary slice, style rules, adjacent summaries, and QA notes.
Create a **Chunk_Manifest** as the authoritative status ledger.
When work will be delegated — or delegation is simulated sequentially — create a **Subagent_Dispatch_Plan** before any translation dispatch.

### Phase 5 — Translate in Passes

Dispatch chunk translators per the Subagent_Dispatch_Plan once the full readiness gate passes (see `core/workflows/subagents.md`), or execute the same plan sequentially. Paste the Worker Contract Card at the top of every worker prompt.
Synchronize newly proposed recurring terms between waves via `glossary-inbox.jsonl` and `scripts/book_ops.py sync-glossary`. Every drafted chunk must pass independent Peer Cross-Check (`fidelity-reviewer` and `continuity-reviewer`) before transitioning to `done`.
Each chunk goes through four mandatory passes:

- **Pass A** — Draft faithful translation of one chunk.
- **Pass B** — Compare against source for omissions, additions, wrong emphasis, numbers, names, formatting, and term consistency.
- **Pass C** — Revise for target-language fluency while preserving source intent.
- **Pass D** — Update state: Chunk_Summary, Chunk_Manifest status, and proposals for Glossary, Style_Sheet, Story_Bible/Domain_Map, and the Unresolved_Issues_Log (the Coordinator writes the shared artifacts).

### Phase 6 — Merge and Final Voice Pass

Run `scripts/book_ops.py merge` (or merge chunk outputs in source order) once all assigned chunks are `done` to assemble the book into clean `.txt`, `.epub`, `.md`, or both (`.txt` + `.epub` via `--format both`), generate a Table of Contents, and record a Completeness Audit. When the input source is an `.epub` and the output is `.epub`, Layout-Preserving EPUB Mode copies the original package into `.source-template.epub` and retains all original CSS, fonts, images, cover art, OPF metadata/manifest/spine structure, and XHTML DOM containers/classes, substituting only translated text and localized TOC entries.
Run cross-chunk consistency checks (terminology, headings, continuity, formal data), then a single centralized final voice pass. The voice pass is never delegated and never changes meaning.

### Phase 7 — QA Gates

Run `scripts/book_ops.py verify` for deterministic completeness, length/paragraph/heading parity, placeholder detection, and glossary compliance, alongside all eight mandatory QA gates: completeness, fidelity, terminology, target-language quality, continuity, numbers/formal-data, formatting, and residual-risk reporting. Produce the **QA_Report**.
For high-stakes material, require source-backed terminology decisions and explicit residual-risk notes.

### Phase 8 — Delivery

Promote durable, approved high-confidence glossary terms back to Tier-1 shared memory via `scripts/book_ops.py sync-glossary --promote` after all QA gates pass.
Deliver the translated output plus a short translator note: scope, assumptions, unresolved issues, terminology worth reviewing, QA checks performed, skill version, and residual risks.
Deliver only after every QA gate has passed or its residual risks are documented in the QA_Report.

## Subagent Roles

| # | Role | Scope |
|---|------|-------|
| 1 | **Transcreate Coordinator** | Final authority on glossary, style, voice, continuity, and merge decisions. |
| 2 | **Terminology Researcher** | Mines terms, searches evidence, proposes glossary entries (never writes directly). |
| 3 | **Style Researcher** | Studies target-language conventions, proposes style-sheet rules (never writes directly). |
| 4 | **Chunk Translator** | Owns one chunk through passes A–D; proposes glossary/style edits. |
| 5 | **Continuity Reviewer** | Flags cross-chunk continuity defects (names, timeline, voice drift). |
| 6 | **Fidelity Reviewer** | Flags meaning divergence between source and target (omissions, additions, distortions). |
| 7 | **Formatting Reviewer** | Flags layout, table, footnote, heading, citation, and numbering defects. |

Workers propose; the Coordinator approves. No worker writes any shared artifact directly — Glossary, Style_Sheet, Story_Bible/Domain_Map, Chunk_Manifest, and the Unresolved_Issues_Log are written only by the Coordinator. Every dispatched worker prompt starts with the Worker Contract Card defined in `core/workflows/subagents.md`, so the binding rules are re-anchored at every dispatch.

## Reference Index

### Workflows

| File | Concern |
|------|---------|
| `core/workflows/long-document.md` | Full staged workflow for books and large documents |
| `core/workflows/d-research-module.md` | Modular Phase 3 `d-research` engine (Track A harvesting and Track B mindset formation) |
| `core/workflows/terminology-research.md` | Term mining, source priority, d-research integration |
| `core/workflows/fiction-continuity.md` | Story Bible maintenance, reveal-timing, character voice |
| `core/workflows/technical-domain.md` | Domain Map maintenance, acronyms, units, citations |
| `core/workflows/qa-gates.md` | The 8 QA gates (completeness through residual risk) |
| `core/workflows/context-management.md` | Context budget, chunk loading, resume procedure |
| `core/workflows/subagents.md` | Readiness gate, role dispatch, parallel rules, merge checklist |

### Schemas

| File | Artifact |
|------|----------|
| `core/schemas/translation-brief.md` | Translation_Brief |
| `core/schemas/research-dossier.md` | Research_Dossier |
| `core/schemas/source-map.md` | Source_Map |
| `core/schemas/glossary.md` | Glossary (CSV + Markdown forms) |
| `core/schemas/style-sheet.md` | Style_Sheet |
| `core/schemas/story-bible.md` | Story_Bible |
| `core/schemas/domain-map.md` | Domain_Map |
| `core/schemas/chunk-manifest.md` | Chunk_Manifest (CSV + Markdown forms) |
| `core/schemas/chunk-summary.md` | Chunk_Summary |
| `core/schemas/context-plan.md` | Context_Plan |
| `core/schemas/subagent-dispatch-plan.md` | Subagent_Dispatch_Plan |
| `core/schemas/unresolved-issues.md` | Unresolved_Issues_Log |
| `core/schemas/qa-report.md` | QA_Report |

### Locale Profiles and Book Pipeline Tooling

| File | Concern |
|------|---------|
| `core/locales/vi-VN.md` | Vietnamese localization, pronoun matrix, Han-Viet balance, anti-translatorese rules |
| `memory/glossary-vi.csv` | Tier-1 cross-book Vietnamese shared translation memory |
| `scripts/book_ops.py` | Deterministic book pipeline CLI (`init`, `convert`, `scan`, `sync-glossary`, `verify`, `merge`) |

### Prompts

| File | Role |
|------|------|
| `core/prompts/transcreate-coordinator.md` | Transcreate Coordinator |
| `core/prompts/terminology-researcher.md` | Terminology Researcher |
| `core/prompts/style-researcher.md` | Style Researcher |
| `core/prompts/chunk-translator.md` | Chunk Translator |
| `core/prompts/continuity-reviewer.md` | Continuity Reviewer |
| `core/prompts/fidelity-reviewer.md` | Fidelity Reviewer |
| `core/prompts/formatting-reviewer.md` | Formatting Reviewer |

## Copyright Rules

Existing translations may inform terminology and style **only** as paraphrased observations with short, attributed evidence quotes. The agent SHALL NOT:

- Reproduce extended passages from copyrighted translations.
- Translate by patching together fragments of existing translations.
- Use fan or unofficial translations as authoritative without independent verification.
- Hide the influence source when a term choice depends on a prior translation.

When quoting evidence, keep quotes short (a few words to one sentence), attribute the source, and use the quote solely to justify a terminology or style decision — never as part of the delivered translation output.
