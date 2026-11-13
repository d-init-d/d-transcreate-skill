---
name: d-transcreate
description: Translation, transcreation, book localization, terminology research, style control, chunking, continuity, and QA workflow for Antigravity. Use when translating or adapting books, manuals, fiction, legal texts, scripts, or multi-chapter documents with durable artifacts and parallel subagent verification.
---

# D Transcreate — Antigravity Skill

Canonical workflow: `core/d-transcreate.md` (use root-relative `core/` paths from the project working directory).

## Antigravity Execution Flow

1. **Zero-Config Book Setup**: For multi-chapter books or long documents (including `.pdf`, `.epub`, `.md`, `.txt`), initialize, convert, and scan via `scripts/book_ops.py`:
   - `python scripts/book_ops.py init --source <path> --target-lang <lang> --workspace <dir>`
   - `python scripts/book_ops.py scan --source <path> --workspace <dir> --max-words 1500` (auto-converts `.pdf` into `<workspace>/converted_source/<stem>.txt` and `.epub`)
   - `python scripts/book_ops.py sync-glossary --workspace <dir> --seed --target-lang <lang>`
2. **Modular Phase 3 Research**: Run `core/workflows/d-research-module.md` to build `Research_Dossier` (`research-dossier.md`, schema at `core/schemas/research-dossier.md`). Use Track A (prior-translation term harvesting and pitfall audit) or Track B (authorial intent, register ladder, and transcreation mindset compass). Load `core/locales/vi-VN.md` and seed from `memory/glossary-vi.csv` when targeting Vietnamese.
3. **Context & Dispatch Planning**: Before final chunking or worker delegation, create `Context_Plan` (`core/schemas/context-plan.md`) and `Subagent_Dispatch_Plan` (`core/schemas/subagent-dispatch-plan.md`). See `core/workflows/context-management.md` for slice budgets and resume order.
4. **Swarm / Subagent Execution & Peer Cross-Check**: Follow `core/workflows/subagents.md` for runtime auto-detection (`swarm` / `post_message` / `invoke_subagent` or sequential fallback). Prefix every worker prompt with the Worker Contract Card. Sync new recurring terms via `glossary-inbox.jsonl` and `scripts/book_ops.py sync-glossary`. Require independent Fidelity and Continuity cross-checks before marking any chunk `done`.
5. **Deterministic Verify & Merge**: Run `python scripts/book_ops.py verify --workspace <dir>` and `python scripts/book_ops.py merge --workspace <dir> --out <merged_book.epub> --format both` (outputs clean `.txt` and `.epub`, or `.md`; `.epub` inputs merged to `.epub` run in Layout-Preserving EPUB Mode, keeping original CSS, fonts, images, cover, and XHTML DOM design intact), then complete all eight QA gates (`core/workflows/qa-gates.md`) and promote approved high-confidence terms (`--promote`).

## Key Core & Module References

- `core/d-transcreate.md` — eight-phase canonical workflow
- `core/workflows/long-document.md` — staged book pipeline
- `core/workflows/d-research-module.md` — `d-research` discovery (host skill, `modules/d-research/`, or internal fallback)
- `core/workflows/context-management.md` — context budget, chunk loading, resume protocol
- `core/workflows/subagents.md` — role table, Worker Contract Card, live glossary sync, Peer Cross-Check
- `core/workflows/qa-gates.md` — eight mandatory QA gates
- `core/locales/vi-VN.md` & `memory/glossary-vi.csv` — Vietnamese localization profile and Tier-1 shared memory
- `core/prompts/` & `core/schemas/` — runtime-neutral role prompts and artifact schemas
