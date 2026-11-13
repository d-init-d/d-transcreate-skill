# D Transcreate — Antigravity Runtime Guide

This workspace hosts the `d-transcreate` skill pack for Antigravity agents (`SKILL.md` is the skill entrypoint; `core/` holds the single source of truth).

## Swarm & Subagent Coordination

1. **Coordinator Ownership**: The main agent acts as `Transcreate Coordinator` (`core/prompts/transcreate-coordinator.md`). Workers propose updates; only the Coordinator approves and writes shared artifacts (`glossary.csv`, `style-sheet.md`, `story-bible.md`, `domain-map.md`, `chunk-manifest.csv`, `unresolved-issues.md`).
2. **Runtime Modes** (`core/workflows/subagents.md`):
   - **Native Swarm (`swarm` / `post_message` / `read_board`)**: Assign scoped chunks or review waves, use `@<role>` mentions for direct Peer Cross-Check handoffs, and lock recurring terms via `glossary-inbox.jsonl` + `scripts/book_ops.py sync-glossary`.
   - **Subagent Spawner (`invoke_subagent` / `send_message`)**: Dispatch waves bounded by `Context_Plan` and `Subagent_Dispatch_Plan`, syncing `glossary-inbox.jsonl` between waves.
   - **Sequential Fallback**: Execute the same seven role contracts sequentially when subagent tools are unavailable.
3. **Mandatory Worker Rules**: Every dispatched worker prompt must begin with the `WORKER CONTRACT CARD` from `core/workflows/subagents.md`. Never pass full books to chunk workers; slice context per `core/workflows/context-management.md`.

## Mandatory Book Pipeline & Research

- Initialize, convert `.pdf` sources, scan, sync glossary, verify coverage/anti-omission, and merge into `.txt`, `.epub`, or `.md` via `scripts/book_ops.py`.
- Execute `core/workflows/d-research-module.md` in Phase 3 to produce `Research_Dossier` (`core/schemas/research-dossier.md`) before translating any chunk.
- Load `core/locales/vi-VN.md` and seed from `memory/glossary-vi.csv` for Vietnamese targets.
