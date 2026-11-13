# Shared Translation Memory (`memory/`)

This directory implements **Tier 1 (Global Persistent Memory)** of the Two-Tier Shared Glossary architecture in `d-transcreate`.

## Two-Tier Shared Glossary Architecture

| Tier | Files | Scope & Lifetime | Authority |
|---|---|---|---|
| **Tier 1: Global Persistent Memory** | `memory/glossary-<lang>.csv` (e.g., `memory/glossary-vi.csv`) | Cross-book reusable memory shipped and maintained in the skill pack | Updated via `--promote` after Phase 8 QA passes |
| **Tier 2: Project Live Glossary** | `<workspace>/glossary.csv` + `<workspace>/glossary-inbox.jsonl` | Single book / document translation workspace | Coordinator owns `glossary.csv`; workers append proposals to `glossary-inbox.jsonl` |

## Synchronization Lifecycle (`scripts/book_ops.py`)

All glossary synchronization is deterministic and managed through `scripts/book_ops.py`:

1. **Seed (Phase 1 / Phase 3)**:
   `python3 scripts/book_ops.py init ...` or `python3 scripts/book_ops.py sync-glossary --workspace <dir> --seed --target-lang vi`
   Imports `approved` entries from `memory/glossary-<lang>.csv` into `<workspace>/glossary.csv` without overwriting existing project-specific decisions.
2. **Live Wave Sync (Phase 5)**:
   Parallel `chunk-translator` workers emit newly discovered recurring terms into `<workspace>/glossary-inbox.jsonl` (or post to `@coordinator` / `@terminology-researcher` on a swarm board). Between waves, the Coordinator runs:
   `python3 scripts/book_ops.py sync-glossary --workspace <dir>`
   This deduplicates proposals by `(term, context)`, surfaces conflicts, and locks approved entries in `<workspace>/glossary.csv` for downstream chunks and peer cross-checkers.
3. **Promote (Phase 8)**:
   After QA gates pass and the book is merged, the Coordinator promotes durable, high-confidence project terms (`status == "approved"` and `confidence == "high"`) back into Tier 1 memory:
   `python3 scripts/book_ops.py sync-glossary --workspace <dir> --promote --target-lang vi`

## Format Contract

Every `memory/glossary-<lang>.csv` file MUST follow `core/schemas/glossary.md`:

- UTF-8 encoding without BOM, RFC 4180 CSV.
- Exact 10-column header:
  `term,preferred_translation,forbidden_translation,term_class,context,source_location,evidence,confidence,status,notes`
- Only `status=approved` and `confidence=high` entries belong in Tier 1 memory.
- Short attributed evidence only — never reproduce extended copyrighted passages.
