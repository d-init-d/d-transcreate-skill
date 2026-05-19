# Translation Brief

## Source
- Source files: `source/section-01-overview.md`, `source/section-02-installation.md`, `source/section-03-configuration.md`
- Source language: en

## Target
- Target language: vi
- Target locale: vi-VN

## Audience
- Audience: Vietnamese software engineers and DevOps practitioners with intermediate-to-advanced technical proficiency. Readers are comfortable with English technical terms but prefer Vietnamese prose for explanations and procedural instructions.

## Translation Parameters
- Mode: faithful translation with light localization for formatting conventions
- Register: formal-technical (professional documentation tone, not academic)

## Output
- Output format: Markdown (same as source)
- Formatting constraints: Preserve all code blocks verbatim (do not translate code, CLI commands, YAML keys, or variable names). Preserve table structure. Keep heading hierarchy unchanged.

## Constraints
- Do-not-translate items: product name "StreamForge", CLI tool name "sfctl", all YAML keys, all code identifiers, all URLs, Kubernetes resource names, environment variable names (e.g., `SF_CLUSTER_ID`), connector names (e.g., `kafka-source`, `bigquery-sink`), gRPC, Protocol Buffers, Helm, Docker, Podman, Kubernetes, Prometheus
- Terminology authority: Glossary provided in `seed-artifacts/glossary.csv`. For terms not in the glossary, prefer translations established by the Vietnamese Kubernetes and cloud-native community.
- Research depth: standard (verify key terms against community usage; do not block on low-impact terms)

## Quality
- QA bar: publication-ready (suitable for official product documentation site)

## Open Questions
- Open questions: None at this time.
