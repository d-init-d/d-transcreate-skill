---
name: d-transcreate
description: Translation, transcreation, localization, glossary, terminology, style sheet, chunking, continuity, and QA workflow for long or high-stakes documents. Use when translating books, manuals, legal or policy texts, fiction, subtitles, scripts, technical documentation, or any substantial source material that needs controlled terminology, preserved structure, context-safe chunking, durable artifacts, and QA gates.
---

# D Transcreate

## Mission

Use this skill to translate or transcreate substantial documents with fidelity, controlled terminology, style continuity, context-safe chunking, and audit-ready QA.

## Core Workflow

Read `core/d-transcreate.md` first for the canonical seven-phase workflow: Intake → Scan → Research → Plan → Translate → Coordinate → QA.

## Portable Operating Model

- Use this root workflow directly in any agent runtime; no host adapter is required.
- Use `adapters/` only when the host platform supports a native skill or agent format and you want auto-discovery.
- If the runtime supports subagents, dispatch roles in parallel or hybrid via the `Subagent_Dispatch_Plan`.
- If subagents are unavailable, the main agent runs the same role contract sequentially. Artifacts remain mandatory in both modes so work can resume and be audited.

## Required Artifacts

Persist every decision as a file on disk, not in chat history:

- Translation_Brief
- Source_Map
- Glossary
- Style_Sheet
- Story_Bible or Domain_Map
- Context_Plan
- Chunk_Manifest
- Subagent_Dispatch_Plan (when delegating, or when simulating delegation sequentially)
- Chunk_Summary entries
- Unresolved_Issues_Log
- QA_Report

## Role Model

Seven roles drive the workflow; workers propose and a single coordinator approves: Transcreate Coordinator, Terminology Researcher, Style Researcher, Chunk Translator, Continuity Reviewer, Fidelity Reviewer, Formatting Reviewer. In a sequential runtime, the main agent performs each role in turn.

## Reference Index

- `core/d-transcreate.md` — canonical entrypoint and operating principles
- `core/workflows/long-document.md` — full staged workflow
- `core/workflows/context-management.md` — context budget, chunk loading, resume
- `core/workflows/subagents.md` — readiness gate, dispatch, parallel rules, sequential fallback
- `core/workflows/qa-gates.md` — the eight QA gates
- `core/workflows/terminology-research.md`, `core/workflows/fiction-continuity.md`, `core/workflows/technical-domain.md`
- `core/schemas/` — artifact contracts
- `core/prompts/` — role prompts
- `templates/` — optional blank artifact templates to copy and fill
