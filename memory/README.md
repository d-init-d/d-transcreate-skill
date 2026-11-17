# Shared Translation Memory (`memory/`)

This directory implements **Tier 1 (Global Persistent Memory)** of the Two-Tier Shared Glossary architecture in `d-transcreate`.

## Two-Tier Shared Glossary Architecture

| Tier | Files | Scope & Lifetime | Authority |
|---|---|---|---|
| **Tier 1: Global Persistent Memory** | `memory/glossary-<lang>.csv` (e.g., `memory/glossary-vi.csv`) | Cross-book reusable memory shipped and maintained in the skill pack | Updated via `--promote` after Phase 8 QA passes |
| **Tier 2: Project Live Glossary** | `<workspace>/glossary.csv` + `<workspace>/glossary-inbox.jsonl` | Single book / document translation workspace | Coordinator owns `glossary.csv`; workers append proposals to `glossary-inbox.jsonl` |

## Synchronization Lifecycle (`scripts/book_ops.py`)

All glossary synchronization is deterministic and managed through `scripts/book_ops.py`:

1. **Domain-Aware Seed (Phase 1 / Phase 3)**:
   `python3 scripts/book_ops.py init ... [--domain <all|fiction|technical|legal|general>]`
   or `python3 scripts/book_ops.py sync-glossary --workspace <dir> --seed --target-lang vi [--domain <domain>] [--filter-to-source]`
   Imports `approved` entries from `memory/glossary-<lang>.csv` into `<workspace>/glossary.csv` without overwriting existing project-specific decisions. Passing `--domain` filters out unrelated domain rows (e.g., fantasy lore `Artifact -> Cổ vật` will not pollute a software engineering book), and `--filter-to-source` after `scan` prunes seeded terms that never appear in `<workspace>/source_chunks/`.
2. **Live Wave Sync & Auto-Lock (Phase 5)**:
   Parallel `chunk-translator` workers emit newly discovered recurring terms into `<workspace>/glossary-inbox.jsonl` (or post to `@coordinator` / `@terminology-researcher` on a swarm board). Between waves, the Coordinator runs:
   `python3 scripts/book_ops.py sync-glossary --workspace <dir> [--approve-clean]`
   This deduplicates proposals by `(term, context)`, surfaces conflicts, optionally locks clean `high`/`medium`-confidence non-conflicting proposals (`--approve-clean`), and bridges telemetry between `evidence-ledger.jsonl` and 37-column `evidence-ledger.csv`.
3. **Guarded Promote (Phase 8)**:
   After QA gates pass and the book is merged, the Coordinator promotes durable, reusable high-confidence project terms (`status == "approved"` and `confidence == "high"`) back into Tier 1 memory:
   `python3 scripts/book_ops.py sync-glossary --workspace <dir> --promote --target-lang vi`
   By default, project-specific entities (`term_class` in `proper-name`, `character`, `place`, `person`, `organization`, `work-specific`, or notes tagged `[no-promote]` / `project-only`) are **skipped automatically** to prevent cross-book memory pollution unless `--include-proper-nouns` is explicitly supplied.

## Format Contract

Every `memory/glossary-<lang>.csv` file MUST follow `core/schemas/glossary.md`:

- UTF-8 encoding without BOM, RFC 4180 CSV.
- Exact 10-column header:
  `term,preferred_translation,forbidden_translation,term_class,context,source_location,evidence,confidence,status,notes`
- Only `status=approved` and `confidence=high` reusable entries belong in Tier 1 memory.
- Short attributed evidence only — never reproduce extended copyrighted passages.
