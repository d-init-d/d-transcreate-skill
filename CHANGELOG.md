# Changelog

All notable changes to this skill pack are documented here.

This project follows semantic versioning.

## 0.3.0 — 2026-05-19

- Add context-aware orchestration with `Context_Plan` and `Subagent_Dispatch_Plan` schemas.
- Require context planning before final chunking and dispatch planning before worker delegation.
- Strengthen coordinator/subagent responsibilities, context slicing, overflow fallback, and sequential fallback rules.
- Add example orchestration artifacts and validator/test coverage for the orchestration contract.
- Polish README, AGENTS, and adapter docs to keep release documentation aligned with the new workflow.

## 0.2.0 — 2026-05-19

- Change licensing from MIT to PolyForm Noncommercial 1.0.0 so the pack can be
  used, changed, and redistributed for noncommercial purposes only.
- Rewrite the README into a product-ready guide with clearer positioning,
  supported platforms, installation, validation, operational workflow, and
  licensing guidance.
- Clarify that this repository is a source distribution pack: users install one
  target adapter, while all platforms share the canonical workflow in `core/`.

## 0.1.0 — 2026-05-19

- Initial public skill pack with canonical core workflow, cross-platform adapters,
  artifact schemas, role prompts, examples, and validation/build tooling.
