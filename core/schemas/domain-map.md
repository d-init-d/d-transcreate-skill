# Domain Map Schema

The Domain Map is the memory artifact for technical, legal, medical, financial, academic, product, or policy material. It captures domain-specific concepts, acronyms, units, governing standards, and formal-data conventions to ensure consistent and accurate translation across all chunks.

## When to Create

Create a Domain_Map when the source is classified as any of:

- Technical documentation
- Legal material
- Medical or pharmaceutical content
- Financial material
- Academic content
- Product documentation
- Policy material

## Form

```markdown
# Domain Map

## Domain
- Field:
- Audience expertise:
- Governing standards/laws:
- Canonical sources:

## Concepts
| Concept | Definition | Preferred translation | Source/evidence |
|---|---|---|---|

## Acronyms
| Acronym | Expansion | Translation policy | Notes |
|---|---|---|---|

## Units and Formal Data
| Item | Policy | Notes |
|---|---|---|
```

## Section Definitions

### Domain

| Field | Description | Example values |
|---|---|---|
| Field | Primary discipline and relevant subdisciplines | `Software engineering — cloud infrastructure`, `Cardiology — interventional`, `Corporate law — M&A` |
| Audience expertise | Expected reader's technical level | `expert`, `practitioner`, `informed layperson`, `general public` |
| Governing standards/laws | Standards, laws, regulations, or frameworks the source references or must comply with | `ISO 27001:2022`, `GDPR`, `21 CFR Part 11`, `RFC 2119` |
| Canonical sources | Authoritative references for terminology in the target language — official translations of standards, regulatory body glossaries, publisher style guides, professional association terminology databases | `Microsoft Language Portal (vi)`, `ISO Vietnamese translations`, `Bộ Tư pháp glossary` |

### Concepts

| Column | Description | Example |
|---|---|---|
| Concept | The domain-specific term or concept as it appears in the source | `containerization`, `force majeure`, `angioplasty` |
| Definition | Brief definition sufficient for a translator to understand the concept | `Packaging software with its dependencies into isolated units (containers) that run consistently across environments` |
| Preferred translation | The approved target-language translation for this concept | `container hóa`, `sự kiện bất khả kháng`, `nong mạch vành` |
| Source/evidence | Where the preferred translation was found or why it was chosen | `Microsoft Language Portal`, `Bộ luật Dân sự 2015 Điều 156`, `Hội Tim mạch Việt Nam guidelines` |

### Acronyms

| Column | Description | Example |
|---|---|---|
| Acronym | The acronym or initialism as it appears in the source | `API`, `GDPR`, `WHO` |
| Expansion | Full expansion in the source language | `Application Programming Interface`, `General Data Protection Regulation`, `World Health Organization` |
| Translation policy | One of: `retain`, `translate`, `expand-first`, `dual`, `context-dependent` | `retain` |
| Notes | Decision rationale, target-language expansion if applicable, usage context | `Vietnamese IT audience uses "API" universally; no translation needed` |

#### Translation Policy Values

| Policy | Rule |
|--------|------|
| `retain` | Keep the source-language acronym unchanged in the target text |
| `translate` | Replace with the target-language equivalent acronym or term |
| `expand-first` | Spell out on first occurrence in each chapter/section, then use the short form |
| `dual` | Show both source acronym and target expansion on first use, then source acronym only |
| `context-dependent` | Policy varies by audience or section; document the rule per context in Notes |

### Units and Formal Data

| Column | Description | Example |
|---|---|---|
| Item | The unit, format, or formal-data convention being documented | `Temperature units`, `Date format`, `Decimal separator`, `Currency` |
| Policy | The conversion or formatting rule to apply | `Convert °F to °C; retain original in parentheses`, `Use DD/MM/YYYY`, `Use comma as decimal separator`, `Retain USD; no conversion` |
| Notes | Additional context, source of the rule, or exceptions | `Per Translation_Brief section "Output"`, `Vietnamese locale standard`, `Exception: financial tables retain original notation` |

## Maintenance Rules

1. **Initial population** — populate during Phase 2 (Whole-Document Scan) based on the source material and Source_Map technical extensions.
2. **Per-chunk updates** — after translating each chunk (Pass D), add any new concepts or acronyms introduced in that chunk before marking the chunk complete.
3. **Consistency enforcement** — when a chunk references a concept or acronym already in the Domain_Map, apply the preferred translation recorded there. Do not introduce variant translations without updating the entry.
4. **Conflict resolution** — if a chunk uses a term in a new sense not covered by the existing entry, flag it in the Unresolved_Issues_Log and propose a Domain_Map update rather than silently diverging.

## Usage

- The Domain_Map is created once per translation task during Phase 2 and maintained throughout.
- The Coordinator_Subagent loads relevant Domain_Map excerpts when dispatching Worker_Subagents.
- The Domain_Map is persisted as a file in the workspace (`domain-map.md`) and is never stored only in chat history.
- The Terminology gate and Numbers/Formal Data gate in QA (Phase 7) verify that Domain_Map entries are applied consistently.
- For high-stakes material, all concept translations must have confidence = high with source evidence.
