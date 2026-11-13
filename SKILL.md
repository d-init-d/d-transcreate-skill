---
name: d-transcreate
description: Translation, transcreation, localization, glossary, terminology, style sheet, chunking, continuity, and QA workflow for long or high-stakes documents. Use when translating books, manuals, legal or policy texts, fiction, subtitles, scripts, technical documentation, or any substantial source material that needs controlled terminology, preserved structure, context-safe chunking, durable artifacts, and QA gates.
---

# D Transcreate

## Mission

Use this skill to translate or transcreate substantial documents with fidelity, controlled terminology, style continuity, context-safe chunking, and audit-ready QA.

## Core Workflow

Read `core/d-transcreate.md` first for the canonical eight-phase workflow: Intake → Scan → Research → Plan → Translate → Merge → QA → Delivery.

## Portable Operating Model

- Use this root workflow directly in any agent runtime; no host adapter is required.
- Use `adapters/` only when the host platform supports a native skill or agent format and you want auto-discovery (including `adapters/antigravity/` for Antigravity).
- **Zero-Config Book Mode**: use `scripts/book_ops.py` (`init`, `convert`, `scan`, `sync-glossary`, `verify`, `merge`) for `.pdf` -> `.txt`/`.epub` conversion, deterministic multi-chapter initialization, semantic boundary scanning, shared glossary sync, anti-omission/anti-truncation verification, and final `.txt` / `.epub` / `.md` book merge (including Layout-Preserving EPUB Mode: `.epub` input -> `.epub` output keeps all CSS, fonts, images, cover art, and XHTML DOM wrappers/classes intact while replacing only translated text and TOC titles).
- **Modular Phase 3 Research**: run `core/workflows/d-research-module.md` to produce `Research_Dossier` (`research-dossier.md`) via Track A (prior-translation term harvesting) or Track B (authorial intent and transcreation mindset compass), seeding from persistent memory (`memory/glossary-vi.csv`) and locale profiles (`core/locales/vi-VN.md`).
- If the runtime supports subagents (native swarm, spawner, or host agents), dispatch roles via the `Subagent_Dispatch_Plan`, start every worker prompt with the Worker Contract Card from `core/workflows/subagents.md`, sync new terms via `glossary-inbox.jsonl`, and enforce Peer Cross-Check before marking any chunk `done`.
- If subagents are unavailable, the main agent runs the same role contract sequentially. Artifacts remain mandatory in both modes so work can resume and be audited.

## Required Artifacts

Persist every decision as a file on disk, not in chat history:

- Translation_Brief
- Source_Map
- Research_Dossier
- Glossary (two-tier: persistent `memory/glossary-vi.csv` + project `glossary.csv` / `glossary-inbox.jsonl`)
- Style_Sheet (incorporating `core/locales/vi-VN.md` for Vietnamese targets)
- Story_Bible or Domain_Map
- Context_Plan
- Chunk_Manifest
- Subagent_Dispatch_Plan (when delegating, or when simulating delegation sequentially)
- Chunk_Summary entries
- Unresolved_Issues_Log
- QA_Report

## Role Model

Seven roles drive the workflow; workers propose and a single coordinator approves: Transcreate Coordinator, Terminology Researcher, Style Researcher, Chunk Translator, Continuity Reviewer, Fidelity Reviewer, Formatting Reviewer. Only the Coordinator writes shared artifacts (including the Unresolved_Issues_Log). In a sequential runtime, the main agent performs each role in turn.

## Reference Index

- `core/d-transcreate.md` — canonical entrypoint and operating principles
- `core/workflows/long-document.md` — full staged workflow
- `core/workflows/d-research-module.md` — modular Phase 3 research engine and Track A/B dossier synthesis
- `core/workflows/context-management.md` — context budget, chunk loading, resume
- `core/workflows/subagents.md` — readiness gate, runtime auto-detection, live glossary sync, Peer Cross-Check, sequential fallback
- `core/workflows/qa-gates.md` — the eight QA gates
- `core/workflows/terminology-research.md`, `core/workflows/fiction-continuity.md`, `core/workflows/technical-domain.md`
- `core/locales/vi-VN.md` — Vietnamese book transcreation and pronoun/register profile
- `core/schemas/` — artifact contracts (including `core/schemas/research-dossier.md`)
- `core/prompts/` — role prompts
- `memory/glossary-vi.csv` — persistent cross-book Vietnamese translation memory
- `scripts/book_ops.py` — deterministic book pipeline CLI (`init`, `convert`, `scan`, `sync-glossary`, `verify`, `merge`) with `.pdf` -> `.txt`/`.epub` conversion
- `templates/` — blank artifact templates to copy and fill
