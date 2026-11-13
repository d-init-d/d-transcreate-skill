# D Transcreate Skill

A portable translation and transcreation skill for AI agents. Use it to translate books, manuals, legal and policy texts, fiction, subtitles, scripts, and other substantial documents with controlled terminology, consistent voice, context-safe chunking, durable artifacts, and audit-ready QA.

The repository is a **portable skill package**: the root `SKILL.md` and `core/` work in any agent runtime. Platform adapters under `adapters/` are optional compatibility layers for hosts that support native skill or agent formats.

## When to Use

Reach for this skill when a translation needs more than a single pass:

- Long or multi-file documents that exceed one context window.
- High-stakes material (legal, medical, technical) needing source-backed terminology.
- Fiction or scripts needing voice continuity and reveal-timing control.
- Any job where terminology, style, and progress must persist across sessions.

## Portable Quick Start

No adapter required:

1. Clone or copy this repository (or a release tarball) into your workspace.
2. Point your agent at the root `SKILL.md`, or at `AGENTS.md` if your host loads instruction files.
3. The agent reads `core/d-transcreate.md` and runs the eight-phase workflow, persisting artifacts as files.

If your runtime supports subagents, the workflow dispatches roles in parallel via the `Subagent_Dispatch_Plan`. If it does not, the same role contract runs sequentially — artifacts are still produced so work can resume and be audited.

## Host-Native Adapters (Optional)

Adapters improve auto-discovery on specific hosts but do not change the canonical workflow. Every build also installs `memory/`, `templates/`, and `scripts/book_ops.py` so the destination workspace is ready to run immediately. Install one with the build script:

```bash
python scripts/build_adapters.py --platform <portable|antigravity|claude-code|opencode|cursor|codex|generic> --dest <path> [--with-d-research <path>]
```

The build stages files atomically and validates the destination after install (disable with `--no-validate-after-build`). Pass `--with-d-research <path>` to bundle a local `d-research-skill` copy into `<dest>/modules/d-research`. An existing `opencode.json` (or any existing file) is preserved unless you pass `--force`.

### Compatibility Matrix

| Runtime | Portable root SKILL.md | AGENTS.md | Native adapter | Subagents |
|---|---:|---:|---:|---:|
| Antigravity | yes | yes | antigravity | yes, native swarm or `invoke_subagent` |
| Generic Markdown agent | yes | yes | generic | sequential fallback |
| Claude Code | yes | yes | claude-code | yes, via `.claude/agents` |
| OpenCode | yes | yes | opencode | yes, via `.opencode/agents` |
| Cursor | partial | yes | cursor | sequential or host-dependent |
| Codex | yes | yes | codex | sequential or host-dependent |

## Zero-Config Book Mode (`scripts/book_ops.py`)

For multi-chapter books and long manuals (`.pdf`, `.epub`, `.md`, `.txt`, `.html`), `scripts/book_ops.py` automates workspace initialization, `.pdf` -> `.txt`/`.epub` conversion, Layout-Preserving EPUB Mode (`.epub` input -> `.epub` output keeps original CSS, fonts, images, cover art, and XHTML DOM wrappers/classes intact), chapter/paragraph-safe scanning, two-tier glossary sync, deterministic verification, and final assembly into clean `.txt`, `.epub`, or `.md`:

```bash
python scripts/book_ops.py init --source <book_path> --target-lang vi --workspace <dir>
python scripts/book_ops.py scan --source <book_path> --workspace <dir> --max-words 1500
python scripts/book_ops.py sync-glossary --workspace <dir> --seed --target-lang vi
python scripts/book_ops.py verify --workspace <dir>
python scripts/book_ops.py merge --workspace <dir> --out <translated_book.epub> --format both
```

Standalone format conversion (`.pdf` -> `.txt` / `.epub`):

```bash
python scripts/book_ops.py convert --source book.pdf --out-dir ./converted/
```

## Modular Research & Persistent Memory

- **Phase 3 Research Engine** (`core/workflows/d-research-module.md`): auto-discovers `d-research` (or falls back to internal search) to produce `Research_Dossier` (`research-dossier.md`). Works with prior translations use **Track A** (harvest canonical terms and audit pitfalls); uncharted works use **Track B** (context, authorial intent, register ladder, and transcreation mindset compass).
- **Two-Tier Shared Glossary**: persistent cross-book memory in `memory/glossary-vi.csv` seeds project `glossary.csv`, while parallel translators emit new recurring terms to `glossary-inbox.jsonl` for live Coordinator sync (`sync-glossary`) and post-QA promotion (`--promote`).
- **Locale Profiles**: `core/locales/vi-VN.md` provides Vietnamese pronoun/address matrices, Sino-Vietnamese vs. native register guidance, and anti-translatorese rules.

## Workflow Lifecycle

Intake → Scan → Research → Plan → Translate → Merge → QA → Delivery. The full definition lives in `core/d-transcreate.md` and `core/workflows/`; this README does not duplicate it.

## Artifacts

Every durable decision is a file on disk, never just chat history:

- Translation_Brief, Source_Map
- Research_Dossier (`research-dossier.md`)
- Glossary (`glossary.csv` + `glossary-inbox.jsonl`), Style_Sheet
- Story_Bible (fiction) or Domain_Map (technical/legal)
- Context_Plan (context budget and chunk-sizing, before final chunking)
- Chunk_Manifest (authoritative status ledger)
- Subagent_Dispatch_Plan (before delegating, or when simulating delegation sequentially)
- Chunk_Summary entries, Unresolved_Issues_Log
- QA_Report

Artifact contracts are defined under `core/schemas/`.

## Examples and Templates

- `examples/` — worked example bundles (technical manual, legal policy, fiction) with original source text and seed artifacts.
- `templates/` — blank, runtime-neutral artifact templates to copy and fill (`translation-brief.md`, `research-dossier.md`, `glossary.csv`, `chunk-manifest.csv`, `context-plan.md`, `subagent-dispatch-plan.yaml`, and more).

## For Agents

Start at `SKILL.md` (portable entrypoint) or `AGENTS.md` (generic instructions). Both point to `core/d-transcreate.md`.

## For Maintainers

Validate, test, and build:

```bash
python -m py_compile scripts/validate_pack.py scripts/build_adapters.py scripts/book_ops.py tests/test_pack.py
python scripts/validate_pack.py . --json          # source validation (warnings allowed)
python scripts/validate_pack.py . --release        # release gate (hygiene/requirement refs become errors)
python tests/test_pack.py                          # full test suite
```

### Release Checklist

1. Bump `VERSION`, the `Version:` line in `core/d-transcreate.md`, and add a `CHANGELOG.md` entry.
2. Run the commands above; `--release` must pass on the packaged tree.
3. Write the release notes at `.github/releases/v<version>.md`.
4. Push an annotated tag `v<version>` that matches `VERSION`. The `release` workflow re-validates, re-tests, rebuilds every adapter target, packages the distribution tarball (`git archive` honors the `export-ignore` rules in `.gitattributes`), and publishes the GitHub release with those notes.

## License

PolyForm Noncommercial 1.0.0 — use, modify, and redistribute for noncommercial purposes only. See `LICENSE`.
