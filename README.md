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
3. The agent reads `core/d-transcreate.md` and runs the seven-phase workflow, persisting artifacts as files.

If your runtime supports subagents, the workflow dispatches roles in parallel via the `Subagent_Dispatch_Plan`. If it does not, the same role contract runs sequentially — artifacts are still produced so work can resume and be audited.

## Host-Native Adapters (Optional)

Adapters improve auto-discovery on specific hosts but do not change the canonical workflow. Install one with the build script:

```bash
python scripts/build_adapters.py --platform <portable|claude-code|opencode|cursor|codex|generic> --dest <path>
```

The build stages files atomically and validates the destination after install (disable with `--no-validate-after-build`). An existing `opencode.json` (or any existing file) is preserved unless you pass `--force`.

### Compatibility Matrix

| Runtime | Portable root SKILL.md | AGENTS.md | Native adapter | Subagents |
|---|---:|---:|---:|---:|
| Generic Markdown agent | yes | yes | generic | sequential fallback |
| Claude Code | yes | yes | claude-code | yes, via `.claude/agents` |
| OpenCode | yes | yes | opencode | yes, via `.opencode/agents` |
| Cursor | partial | yes | cursor | sequential or host-dependent |
| Codex | yes | yes | codex | sequential or host-dependent |

## Workflow Lifecycle

Intake → Scan → Research → Plan → Translate → Coordinate → QA. The full definition lives in `core/d-transcreate.md` and `core/workflows/`; this README does not duplicate it.

## Artifacts

Every durable decision is a file on disk, never just chat history:

- Translation_Brief, Source_Map
- Glossary, Style_Sheet
- Story_Bible (fiction) or Domain_Map (technical/legal)
- Context_Plan (context budget and chunk-sizing, before final chunking)
- Chunk_Manifest (authoritative status ledger)
- Subagent_Dispatch_Plan (before delegating, or when simulating delegation sequentially)
- Chunk_Summary entries, Unresolved_Issues_Log
- QA_Report

Artifact contracts are defined under `core/schemas/`.

## Examples and Templates

- `examples/` — worked example bundles (technical manual, legal policy, fiction) with original source text and seed artifacts.
- `templates/` — blank, runtime-neutral artifact templates to copy and fill (`translation-brief.md`, `glossary.csv`, `chunk-manifest.csv`, `context-plan.md`, `subagent-dispatch-plan.yaml`, and more).

## For Agents

Start at `SKILL.md` (portable entrypoint) or `AGENTS.md` (generic instructions). Both point to `core/d-transcreate.md`.

## For Maintainers

Validate, test, and build:

```bash
python -m py_compile scripts/validate_pack.py scripts/build_adapters.py tests/test_pack.py
python scripts/validate_pack.py . --json          # source validation (warnings allowed)
python scripts/validate_pack.py . --release        # release gate (hygiene/requirement refs become errors)
python tests/test_pack.py                          # full test suite
```

### Release Checklist

1. Bump `VERSION`, the `Version:` line in `core/d-transcreate.md`, and add a `CHANGELOG.md` entry.
2. Run the commands above; `--release` must pass on the packaged tree.
3. Package the distribution, excluding the dev-only paths listed in `.distignore` (`_archive/`, `.kiro/`, `.github/`, etc.). `git archive` honors the `export-ignore` rules in `.gitattributes`.

## License

PolyForm Noncommercial 1.0.0 — use, modify, and redistribute for noncommercial purposes only. See `LICENSE`.
