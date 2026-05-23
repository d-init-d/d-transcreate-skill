# D Transcreate Skill

**Production-grade translation and transcreation skill for AI agents: long-document planning, terminology control, style continuity, context-safe chunking, subagent coordination, and QA gates.**

[![License: PolyForm Noncommercial 1.0.0](https://img.shields.io/badge/License-PolyForm%20Noncommercial%201.0.0-lightgrey.svg)](https://polyformproject.org/licenses/noncommercial/1.0.0/)
[![Release](https://img.shields.io/github/v/release/d-init-d/d-transcreate-skill?sort=semver)](https://github.com/d-init-d/d-transcreate-skill/releases)

> D Transcreate turns ad hoc AI translation into an auditable production workflow: understand the source, define the target audience, research terminology and register, map the document, split work into context-safe chunks, translate with persistent artifacts, coordinate subagents when useful, and verify the final output before delivery.

---

## At a glance

| Area | What D Transcreate provides |
|---|---|
| Primary users | AI agents, agent operators, translators, editors, localization teams, and technical writers who need reliable translation or controlled transcreation for long or high-stakes documents. |
| Product model | A source-available skill package with one canonical workflow in `core/` and thin adapters for Codex, Claude Code, Cursor, OpenCode, and generic agent runtimes. |
| State model | Durable artifacts on disk: Translation_Brief, Source_Map, Glossary, Style_Sheet, Story_Bible or Domain_Map, Context_Plan, Chunk_Manifest, Chunk_Summary, Subagent_Dispatch_Plan, Unresolved_Issues_Log, and QA_Report. |
| Best fit | Books, fiction, scripts, subtitles, technical manuals, API docs, product documentation, legal/policy material, compliance documents, and mixed-format sources where structure matters. |
| Verification | Structural pack validation, adapter build tests, required orchestration references, example artifact checks, and mandatory delivery QA gates. |
| Safety posture | Fidelity first. Do not invent, omit, reorder, or silently simplify meaning. Existing translations may inform terminology and style only; they must not be copied into the delivered work. |

## When to use it

Use D Transcreate when an agent needs to:

- translate a long document without losing terminology, register, character voice, or cross-chapter continuity;
- preserve source structure such as headings, tables, footnotes, citations, code blocks, variables, placeholders, links, and numbering;
- adapt idioms, humor, dialogue, slogans, or culturally specific references while keeping source intent intact;
- prepare a glossary and style sheet before translation begins;
- split a large source into semantic chunks that fit the available context window;
- resume cleanly after context reset by relying on written artifacts instead of chat memory;
- coordinate multiple workers while one coordinator remains responsible for terminology, voice, continuity, and final merge decisions;
- run explicit QA gates before presenting the final translation.

Do **not** use it to mass-produce low-care translations, bypass copyright restrictions, copy existing translations, or hide uncertainty in high-stakes legal, medical, financial, policy, or technical material.

## Product scope

This is **a skill package**, not a hosted localization platform, API service, CAT tool, Python package, or model provider.

An agent reads the adapter entry point for its runtime, follows the canonical workflow in `core/d-transcreate.md`, and writes the required artifacts into the consumer project. The repository ships workflow instructions, artifact schemas, role prompts, examples, adapter wrappers, and maintainer validation scripts. The scripts help package and validate the skill; they do not replace the agent.

Concretely, the repo contains:

- `core/d-transcreate.md` - the canonical entry point for the workflow.
- `core/workflows/` - deep-dive guides for long documents, terminology research, fiction continuity, technical domains, context management, subagents, and QA gates.
- `core/schemas/` - required artifact schemas for planning, translation state, orchestration, review, and delivery.
- `core/prompts/` - role prompts for the coordinator and specialized reviewers/workers.
- `adapters/` - platform-specific wrappers for Codex, Claude Code, Cursor, OpenCode, and generic agents.
- `examples/` - worked examples for fiction, technical documentation, and legal/policy sources.
- `scripts/build_adapters.py` - installs one adapter layout into a consumer project.
- `scripts/validate_pack.py` - validates the source pack or an installed destination.
- `tests/test_pack.py` - smoke tests for validation, adapter builds, manifests, and orchestration references.
- `AGENTS.md` - root-level instructions for agentic frameworks that read this file.
- `CHANGELOG.md`, `VERSION`, and `LICENSE` - release metadata and licensing terms.

There is **no API server**, **no translation memory database**, **no machine translation engine**, **no hosted dashboard**, **no Docker image**, and **no runtime credential store** in this repository.

---

## Workflow lifecycle

D Transcreate is organized around seven translation lifecycle phases. Each phase creates or updates artifacts that the next phase consumes.

| # | Phase | What happens | Key files |
|---|---|---|---|
| 1 | **intake** | Define source files, target language, audience, register, output format, quality bar, constraints, and translation mode. | `core/schemas/translation-brief.md` |
| 2 | **scan** | Inspect the whole source before translating. Map chapters, sections, tables, figures, notes, references, repeated blocks, and formatting hazards. | `core/schemas/source-map.md` |
| 3 | **research** | Establish terminology, style rules, domain conventions, named entities, formal data, and continuity facts before drafting. | `core/workflows/terminology-research.md`, `core/schemas/glossary.md`, `core/schemas/style-sheet.md` |
| 4 | **plan** | Create a Context_Plan, set context budgets, segment by semantic boundaries, and create the authoritative Chunk_Manifest. | `core/workflows/context-management.md`, `core/schemas/context-plan.md`, `core/schemas/chunk-manifest.md` |
| 5 | **translate** | Draft one chunk, compare against source, revise for target-language quality, then persist a Chunk_Summary and unresolved issues. | `core/workflows/long-document.md`, `core/schemas/chunk-summary.md`, `core/schemas/unresolved-issues.md` |
| 6 | **coordinate** | Use a Subagent_Dispatch_Plan when delegating. Merge outputs in source order and run a unified terminology, voice, and continuity pass. | `core/workflows/subagents.md`, `core/schemas/subagent-dispatch-plan.md` |
| 7 | **QA** | Run completeness, fidelity, terminology, language-quality, continuity, formal-data, formatting, and residual-risk gates. | `core/workflows/qa-gates.md`, `core/schemas/qa-report.md` |

For the full release history, see [CHANGELOG.md](CHANGELOG.md).

---

## Core capabilities

1. **Canonical long-document workflow** - intake -> whole-document scan -> terminology/style research -> context planning -> chunk translation -> coordination -> QA. See `core/d-transcreate.md`.
2. **Artifact-first translation state** - important decisions live in files, not volatile conversation history.
3. **Translation brief** - records source, target, audience, register, quality bar, allowed transcreation level, constraints, and delivery format.
4. **Source mapping** - identifies structure, repeated elements, formatting hazards, figures, tables, footnotes, citations, appendices, and source-order rules before translation begins.
5. **Terminology control** - builds a glossary before drafting and keeps term decisions traceable across chunks.
6. **Style control** - captures voice, register, sentence rhythm, formality, punctuation rules, localization choices, and target-language conventions.
7. **Fiction continuity** - maintains Story_Bible artifacts for characters, relationships, timeline, POV, motifs, terms of address, and reveal timing.
8. **Technical and legal domain support** - maintains Domain_Map artifacts for acronyms, units, standards, APIs, UI strings, citations, definitions, and formal data.
9. **Context_Plan for large work** - records context window assumptions, chunk-size limits, artifact slices, overflow triggers, and resume strategy before final chunking.
10. **Chunk_Manifest ledger** - tracks every chunk's status, owner, dependencies, source span, artifact dependencies, QA state, and final merge readiness.
11. **Pass-based chunk translation** - each chunk goes through faithful draft, source comparison, target-language revision, and artifact update.
12. **Subagent_Dispatch_Plan** - lets workers handle scoped slices while the coordinator keeps final authority over glossary, style, continuity, and merge decisions.
13. **Specialized reviewer roles** - continuity, fidelity, and formatting reviewers check different failure modes instead of relying on one generic pass.
14. **Mandatory QA gates** - delivery requires checks for completeness, fidelity, terminology, target-language quality, continuity, numbers/formal data, formatting, and residual risk.
15. **Copyright-aware transcreation** - existing translations may guide terminology or style only as attributed, limited observations. The delivered translation must be original work.
16. **Cross-platform adapters** - one workflow can be installed into several agent runtimes without duplicating the core logic.
17. **Pack validation and build tests** - maintainers can validate source files, adapter frontmatter, internal links, orchestration references, manifests, and example structure.

---

## Feature matrix

| Area | What users get | Main files / commands |
|---|---|---|
| Agent workflow | A complete artifact-driven translation and transcreation process | `core/d-transcreate.md`, `AGENTS.md` |
| Platform adapters | Thin wrappers for Codex, Claude Code, Cursor, OpenCode, and generic agents | `adapters/` |
| Long-document planning | Source map, context plan, chunk manifest, resume strategy | `core/workflows/long-document.md`, `core/workflows/context-management.md` |
| Terminology | Glossary creation, source priority, consistency checks | `core/workflows/terminology-research.md`, `core/schemas/glossary.md` |
| Style and register | Style sheet for voice, tone, formality, localization, punctuation, and formatting conventions | `core/schemas/style-sheet.md` |
| Fiction | Character voice, timeline, POV, motif, relationship, and reveal tracking | `core/workflows/fiction-continuity.md`, `core/schemas/story-bible.md` |
| Technical/legal | Acronyms, standards, definitions, units, citations, formal data, and risk notes | `core/workflows/technical-domain.md`, `core/schemas/domain-map.md` |
| Subagents | Portable delegation contract with scoped worker inputs and coordinator-owned merge | `core/workflows/subagents.md`, `core/schemas/subagent-dispatch-plan.md` |
| QA | Completeness, fidelity, terminology, language quality, continuity, formal data, formatting, residual risk | `core/workflows/qa-gates.md`, `core/schemas/qa-report.md` |
| Packaging | Build one adapter into a consumer project and write a manifest | `python scripts/build_adapters.py --platform <platform> --dest <path>` |
| Validation | Check source pack or installed destination before release/use | `python scripts/validate_pack.py .` |

---

## Supported agent platforms

| Platform | Source adapter | Installed entry point |
|---|---|---|
| OpenAI Codex | `adapters/codex/` | `SKILL.md` |
| Claude Code | `adapters/claude-code/` | `.claude/skills/d-transcreate/SKILL.md` |
| Cursor | `adapters/cursor/` | `.cursor/rules/d-transcreate.mdc` |
| OpenCode | `adapters/opencode/` | `opencode.json` |
| Generic agents | `adapters/generic/` | `d-transcreate.md` |

The adapter files are intentionally small. They point to the same canonical workflow under `core/`, so each runtime gets the same behavior and artifact contract.

## Source pack vs installed skill

This repository is the **source distribution pack**. It is not meant to be copied wholesale into every consumer project.

The pack has two layers:

1. **Canonical source** - `core/` contains the reusable workflow, schemas, and role prompts. This is the source of truth.
2. **Platform adapters** - `adapters/<platform>/` contains the wrapper files needed by one target tool.

When you install the pack, `scripts/build_adapters.py` selects one adapter and generates the layout expected by that tool. A consumer project normally receives one adapter plus the canonical `core/` directory and release metadata.

Example Claude Code destination layout:

```text
my-project/
|-- .claude/
|   |-- skills/
|   |   `-- d-transcreate/
|   |       `-- SKILL.md
|   `-- agents/
|       |-- transcreate-coordinator.md
|       |-- terminology-researcher.md
|       |-- style-researcher.md
|       `-- ...
|-- core/
|   |-- d-transcreate.md
|   |-- workflows/
|   |-- schemas/
|   `-- prompts/
|-- README.md
|-- LICENSE
|-- VERSION
|-- CHANGELOG.md
`-- .d-transcreate-manifest.json
```

For Cursor, Codex, OpenCode, or generic agents, the entry point changes to the file that runtime expects, but the canonical workflow remains the same.

---

## Repository layout

```text
.
|-- README.md
|-- LICENSE
|-- VERSION
|-- CHANGELOG.md
|-- AGENTS.md
|-- core/
|   |-- d-transcreate.md
|   |-- workflows/
|   |   |-- long-document.md
|   |   |-- terminology-research.md
|   |   |-- fiction-continuity.md
|   |   |-- technical-domain.md
|   |   |-- context-management.md
|   |   |-- subagents.md
|   |   `-- qa-gates.md
|   |-- schemas/
|   |   |-- translation-brief.md
|   |   |-- source-map.md
|   |   |-- glossary.md
|   |   |-- style-sheet.md
|   |   |-- story-bible.md
|   |   |-- domain-map.md
|   |   |-- context-plan.md
|   |   |-- chunk-manifest.md
|   |   |-- chunk-summary.md
|   |   |-- subagent-dispatch-plan.md
|   |   |-- unresolved-issues.md
|   |   `-- qa-report.md
|   `-- prompts/
|       |-- transcreate-coordinator.md
|       |-- terminology-researcher.md
|       |-- style-researcher.md
|       |-- chunk-translator.md
|       |-- continuity-reviewer.md
|       |-- fidelity-reviewer.md
|       `-- formatting-reviewer.md
|-- adapters/
|   |-- codex/
|   |-- claude-code/
|   |-- cursor/
|   |-- opencode/
|   `-- generic/
|-- examples/
|   |-- fiction-short/
|   |-- technical-manual/
|   `-- legal-policy/
|-- scripts/
|   |-- build_adapters.py
|   `-- validate_pack.py
`-- tests/
    `-- test_pack.py
```

---

## Installation

### For humans

#### Option A: Let an LLM agent install it

Paste this into an agent or IDE assistant that can edit your project files:

```text
Install the D Transcreate skill from https://github.com/d-init-d/d-transcreate-skill.git into this project. Choose the adapter that matches this runtime, copy the canonical core workflow, preserve the manifest, and run the validator if Python is available.
```

#### Option B: Manual setup

1. Clone the source pack:

```bash
git clone https://github.com/d-init-d/d-transcreate-skill.git
cd d-transcreate-skill
```

2. Build the adapter for your target runtime:

```bash
python scripts/build_adapters.py \
  --platform <codex|claude-code|cursor|opencode|generic> \
  --dest <path-to-consumer-project>
```

On systems where the Python command is named `python3`, use:

```bash
python3 scripts/build_adapters.py \
  --platform <codex|claude-code|cursor|opencode|generic> \
  --dest <path-to-consumer-project>
```

3. Point your agent or IDE at the installed entry point for that platform.

4. Optional: validate the installed destination:

```bash
python scripts/validate_pack.py <path-to-consumer-project>
```

### Build options

```bash
python scripts/build_adapters.py \
  --platform <codex|claude-code|cursor|opencode|generic> \
  --dest <path-to-consumer-project> \
  --mode <copy|symlink|dry-run> \
  --core-strategy <copy|reference>
```

Common options:

- `--mode copy` - copy files into the destination project. This is the default.
- `--mode symlink` - create symlinks for local development.
- `--mode dry-run` - preview planned operations without writing files.
- `--core-strategy copy` - copy the canonical `core/` directory into the destination. This is the default.
- `--core-strategy reference --shared-core-path <path>` - keep one shared `core/` directory and rewrite adapter references to it.
- `--force` - overwrite existing destination files after you have reviewed the conflicts.

Every successful install writes `.d-transcreate-manifest.json` with the target platform, pack version, source commit, install options, and file hashes.

---

## Quick start

### As an agent skill

1. Open the installed adapter entry point for your runtime.
2. Follow its pointer to `core/d-transcreate.md`.
3. Create the required artifacts before translating:
   - `translation-brief.md`
   - `source-map.md`
   - `glossary.md`
   - `style-sheet.md`
   - `context-plan.md`
   - `chunk-manifest.md`
4. Add `story-bible.md` for narrative work or `domain-map.md` for technical, legal, policy, or domain-heavy work.
5. If delegating work, create `subagent-dispatch-plan.md` before dispatching workers.
6. Translate chunk by chunk. After each chunk, write or update the relevant `chunk-summary.md`, glossary entries, style notes, and unresolved issues.
7. Run the QA gates and write `qa-report.md` before presenting the final output.

### Minimal user prompt

```text
Use the D Transcreate skill to translate this document into Vietnamese. Preserve structure, terminology, links, tables, and code blocks. Create the required artifacts first, show me unresolved terminology questions before drafting, translate in chunks, and run the QA gates before final delivery.
```

### High-stakes prompt

```text
Use the D Transcreate skill for this legal/policy document. Treat fidelity and terminology as higher priority than fluency. Create a Translation_Brief, Source_Map, Domain_Map, Glossary, Style_Sheet, Context_Plan, Chunk_Manifest, and QA_Report. Mark every uncertain term or legal interpretation in an Unresolved_Issues_Log instead of guessing.
```

### Fiction prompt

```text
Use the D Transcreate skill for this fiction manuscript. Preserve character voice, timeline, point of view, reveal timing, terms of address, motifs, and dialogue rhythm. Create a Story_Bible and Style_Sheet before translating the first chunk.
```

---

## Validation

Run these checks before every release or before vendoring the skill into another project:

```bash
python -m py_compile scripts/validate_pack.py scripts/build_adapters.py tests/test_pack.py
python scripts/validate_pack.py .
python tests/test_pack.py
```

On systems where the Python command is named `python3`, use:

```bash
python3 -m py_compile scripts/validate_pack.py scripts/build_adapters.py tests/test_pack.py
python3 scripts/validate_pack.py .
python3 tests/test_pack.py
```

The validator checks required files, adapter frontmatter, internal links, placeholder markers, adapter references to `core/`, adapter line budgets, duplicated adapter text, UTF-8 readability, schema references, example README files, install manifests, Context_Plan references, Subagent_Dispatch_Plan references, and required role prompts.

Machine-readable output is available with:

```bash
python scripts/validate_pack.py . --json
```

## Release checklist

- [ ] `VERSION` contains the intended release version.
- [ ] `CHANGELOG.md` has a dated entry for the release.
- [ ] `python scripts/validate_pack.py .` passes with zero errors.
- [ ] `python tests/test_pack.py` passes.
- [ ] All five adapters build and validate.
- [ ] Example directories include current seed artifacts.
- [ ] README references Context_Plan and Subagent_Dispatch_Plan.
- [ ] License terms match the intended distribution policy.

---

## Design principles

- **Single source of truth** - workflow logic lives once under `core/`.
- **Thin adapters** - runtime-specific files point to the canonical workflow instead of duplicating it.
- **Artifacts as state** - decisions are written to files so the job can be resumed and audited.
- **Context-safe operation** - Context_Plan, chunking, artifact slices, and summaries keep long projects manageable.
- **Coordinator-owned quality** - workers may propose edits, but one coordinator owns final glossary, style, continuity, merge, and QA decisions.
- **Fidelity first** - meaning, structure, facts, register, and formal data matter more than surface fluency.
- **Controlled transcreation** - adapt only where the source effect requires it, and record the reasoning when the choice is material.
- **Copyright safety** - do not copy existing translations into the delivered work.
- **Explicit uncertainty** - unresolved terms, ambiguous source passages, and risk notes must be written down instead of hidden.

## Safety and copyright boundary

D Transcreate is designed for faithful, auditable translation work. It does not authorize copyright infringement or low-quality paraphrase laundering.

The agent must not:

- reproduce extended passages from an existing copyrighted translation;
- translate by stitching together fragments from prior translations;
- treat fan or unofficial translations as authoritative without independent verification;
- hide the influence source when a terminology or style choice depends on prior material;
- silently invent, omit, simplify, reorder, or normalize source meaning;
- erase ambiguity in legal, medical, financial, policy, or technical content;
- deliver high-stakes material without residual-risk notes when uncertainty remains.

Existing translations may be used only to infer terminology, register, or style conventions. Evidence quotes should be short, attributed, and used for decision support rather than as delivered translation text.

## Compatibility

D Transcreate is framework-agnostic. It has adapters for common agent runtimes and a generic Markdown entry point for tools that can read instructions from project files.

The maintainer scripts require Python 3.8+ and use only the standard library. No Node.js, npm package, API key, model credential, or hosted service is required to validate or install the skill pack.

Runtime model routing, API keys, account login, real subagent invocation, and file-access policy are intentionally configured outside this repository in the agent host or IDE.

## License

This project is source-available for noncommercial use under the **PolyForm Noncommercial License 1.0.0**. See [LICENSE](LICENSE).

You may use, copy, modify, and redistribute this software for noncommercial purposes. Commercial use is not permitted without a separate commercial license from the copyright holder.

Commercial use includes, but is not limited to, resale, paid redistribution, SaaS packaging, marketplace distribution, paid agent bundles, or embedding this skill in a paid product or service.

The copyright holder may offer separate commercial licenses on request.
