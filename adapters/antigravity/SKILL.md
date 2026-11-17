---
name: d-transcreate
description: Translation, transcreation, book localization, terminology research, style control, chunking, continuity, and QA workflow for Antigravity. Use when translating or adapting books, manuals, fiction, legal texts, scripts, or multi-chapter documents with durable artifacts and parallel subagent verification.
---

# D Transcreate — Antigravity Skill

Canonical workflow: `core/d-transcreate.md` (use root-relative `core/` paths from the project working directory).

## Antigravity Execution Flow

1. **Zero-Config Book Setup**: For multi-chapter books or long documents (including `.pdf`, `.epub`, `.md`, `.txt`), initialize, convert, scan, and mine terms via `scripts/book_ops.py`:
   - `python scripts/book_ops.py init --source <path> --target-lang <lang> --workspace <dir> [--domain <domain>]`
   - `python scripts/book_ops.py scan --source <path> --workspace <dir> --max-words 1500` (auto-converts `.pdf` into `<workspace>/converted_source/`, emits `<!-- @bN -->` anchor-locked EPUB chunks, and auto-mines `candidate-terms.json`)
   - `python scripts/book_ops.py sync-glossary --workspace <dir> --seed --target-lang <lang> --filter-to-source`
2. **Modular Phase 3 Research**: Run `core/workflows/d-research-module.md` (using `candidate-terms.json`) to build `Research_Dossier` (`research-dossier.md`, schema at `core/schemas/research-dossier.md`). Use Track A (prior-translation term harvesting and pitfall audit) or Track B (authorial intent, register ladder, transcreation mindset compass, and `Golden Voice Calibration Sample` in `style-sheet.md`). Load `core/locales/vi-VN.md` and seed from `memory/glossary-vi.csv` when targeting Vietnamese.
3. **Context & Dispatch Planning**: Before final chunking or worker delegation, create `Context_Plan` (`core/schemas/context-plan.md`) and `Subagent_Dispatch_Plan` (`core/schemas/subagent-dispatch-plan.md`). See `core/workflows/context-management.md` for slice budgets and resume order.
4. **Swarm / Subagent Execution & Peer Cross-Check**: Follow `core/workflows/subagents.md` for runtime auto-detection (`swarm` / `post_message` / `invoke_subagent` or sequential fallback). Assemble scoped worker prompts via `scripts/book_ops.py bundle-chunk`, keep `<!-- @bN -->` anchors intact, sync new recurring terms via `glossary-inbox.jsonl` and `scripts/book_ops.py sync-glossary [--approve-clean]`, and require independent Fidelity and Continuity cross-checks before marking any chunk `done`.
5. **Sliding-Window Voice Pass, Verify & Merge**: Run a centralized Sliding-Window Voice & Seam Pass directly on `output/<chunk_id>.md`, then run `python scripts/book_ops.py verify --workspace <dir> --require-dossier --enforce-glossary` and `python scripts/book_ops.py merge --workspace <dir> --out <merged_book.epub> --format both` (outputs clean `.txt` and Anchor-Locked Layout-Preserving `.epub` with inline footnotes, CSS, fonts, images, and cover intact), complete all eight QA gates (`core/workflows/qa-gates.md`), and promote reusable terms (`--promote`).

## Key Core & Module References

- `core/d-transcreate.md` — eight-phase canonical workflow
- `core/workflows/long-document.md` — staged book pipeline
- `core/workflows/d-research-module.md` — `d-research` discovery (host skill, `modules/d-research/`, or internal fallback)
- `core/workflows/context-management.md` — context budget, chunk loading, resume protocol
- `core/workflows/subagents.md` — role table, Worker Contract Card, live glossary sync, Peer Cross-Check
- `core/workflows/qa-gates.md` — eight mandatory QA gates
- `core/locales/vi-VN.md` & `memory/glossary-vi.csv` — Vietnamese localization profile and Tier-1 shared memory
- `core/prompts/` & `core/schemas/` — runtime-neutral role prompts and artifact schemas
