# Source Map Schema

The Source Map is produced during Phase 2 (Whole-Document Scan) and records the
complete structural inventory of the source document, formatting hazards, and
high-risk items that require special attention during translation.

The agent populates this artifact **before** any chunk translation begins.

---

## Overview

| Field | Description |
|---|---|
| Genre/domain | The material class (fiction, technical, legal, medical, financial, academic, policy, script, mixed). Determines which extensions apply. |
| Purpose | Why the document exists and what it accomplishes for its audience. |
| Source quality | Assessment of the source file condition: clean digital, OCR with noise, scan with artifacts, hand-typed with typos, mixed. |
| Extraction hazards | Known issues that may affect parsing or translation: OCR noise, broken hyphenation, missing pages, encoding issues, ambiguous structure, embedded images with text, non-standard formatting. |

### Template

```markdown
# Source Map

## Overview
- Genre/domain:
- Purpose:
- Source quality:
- Extraction hazards:
```

---

## Structure Table

Lists every structural element detected during the whole-document scan. Every
chapter, section, table, figure, footnote, caption, appendix, reference, and
repeated block must appear here.

| Column | Description |
|---|---|
| ID | Stable identifier for the structural element (e.g., `ch01`, `sec03.2`, `fig07`, `fn12`). |
| Source location | Page, paragraph, or line range in the source. |
| Type | One of: chapter, section, subsection, paragraph-group, table, figure, caption, footnote, endnote, appendix, reference, repeated-block, frontmatter, backmatter, epigraph, dedication, TOC, index. |
| Notes | Brief description of content or purpose. |
| Risk | Risk level for translation: `low`, `medium`, `high`. High-risk items also appear in the High-Risk Items table. |

### Template

```markdown
## Structure
| ID | Source location | Type | Notes | Risk |
|---|---|---|---|---|
| ch01 | pp. 1–12 | chapter | Introduction — sets up premise | low |
| fig03 | p. 15 | figure | Diagram with embedded text labels | high |
| fn07 | p. 22 | footnote | Citation to foreign-language source | medium |
```

---

## High-Risk Items Table

Items flagged as high-risk in the Structure table are expanded here with the
specific risk description and the action needed before or during translation.

| Column | Description |
|---|---|
| Item | Reference to the structural element (matches Structure table ID or description). |
| Location | Page, paragraph, or line range. |
| Risk | Description of the specific translation risk. |
| Needed action | What the agent must do to mitigate the risk (e.g., confirm with user, research term, flag for QA, preserve formatting exactly). |

### Template

```markdown
## High-Risk Items
| Item | Location | Risk | Needed action |
|---|---|---|---|
| fig03 | p. 15 | Embedded text in image — cannot translate inline | Flag for user; provide translated caption separately |
| sec05 | pp. 30–35 | Dense legal citations with jurisdiction-specific format | Preserve citation format exactly; verify against target jurisdiction conventions |
```

---

## Fiction-Specific Extensions

**Applies when:** Genre/domain is fiction, memoir, narrative non-fiction, script,
game, comic, or any material with narrative structure.

These extensions are populated during the whole-document scan alongside the
base Structure and High-Risk Items tables.

### Cast

| Column | Description |
|---|---|
| Character | Character name as it appears in the source. |
| Role | Protagonist, antagonist, supporting, minor, mentioned-only. |
| First appearance | Source location where the character first appears. |
| Name variants | Other names, nicknames, titles used for this character. |
| Notes | Key traits, voice markers, or translation considerations. |

```markdown
### Cast
| Character | Role | First appearance | Name variants | Notes |
|---|---|---|---|---|
```

### Point of View

| Column | Description |
|---|---|
| Chapter/section | Structural element ID. |
| POV character | Who narrates or whose perspective is shown. |
| POV type | First-person, third-limited, third-omniscient, second-person, shifting. |
| Notes | Tense, voice markers, or special considerations. |

```markdown
### Point of View
| Chapter/section | POV character | POV type | Notes |
|---|---|---|---|
```

### Timeline

| Column | Description |
|---|---|
| Event | Brief description of the narrative event. |
| Source location | Where in the source this event occurs. |
| Time marker | In-story time reference (date, relative time, season, etc.). |
| Notes | Chronology dependencies, flashbacks, time jumps. |

```markdown
### Timeline
| Event | Source location | Time marker | Notes |
|---|---|---|---|
```

### Motifs and Reveals

| Column | Description |
|---|---|
| Motif/reveal | Name or description of the recurring motif or hidden reveal. |
| First planted | Source location where it first appears. |
| Payoff location | Where the motif pays off or the reveal occurs. |
| Translation risk | How this could be accidentally exposed or lost in translation. |

```markdown
### Motifs and Reveals
| Motif/reveal | First planted | Payoff location | Translation risk |
|---|---|---|---|
```

---

## Technical-Specific Extensions

**Applies when:** Genre/domain is technical, legal, medical, financial, academic,
product, policy, or any material with specialized domain knowledge.

These extensions are populated during the whole-document scan alongside the
base Structure and High-Risk Items tables.

### Domain

| Field | Description |
|---|---|
| Field | The specific technical or professional domain. |
| Governing standards/laws | Standards, regulations, or laws that govern terminology and format (e.g., ISO 9001, GDPR, IEC 60601). |
| Canonical sources | Authoritative references for terminology in the target language. |

```markdown
### Domain
- Field:
- Governing standards/laws:
- Canonical sources:
```

### Acronyms

| Column | Description |
|---|---|
| Acronym | The acronym as it appears in the source. |
| Expansion | Full form in the source language. |
| First occurrence | Source location where it first appears. |
| Frequency | How often it appears (once, few, frequent). |
| Notes | Whether it should be translated, kept as-is, or expanded on first use. |

```markdown
### Acronyms
| Acronym | Expansion | First occurrence | Frequency | Notes |
|---|---|---|---|---|
```

### Units and Formal Data

| Column | Description |
|---|---|
| Item | The unit, measurement system, or formal data element. |
| Source convention | How it appears in the source (e.g., imperial, metric, specific date format). |
| Target convention | Expected convention in the target locale (if conversion needed). |
| Policy | Keep as-is, convert, or dual-display. |

```markdown
### Units and Formal Data
| Item | Source convention | Target convention | Policy |
|---|---|---|---|
```

---

## Usage Notes

1. The Source Map is produced once per translation project during Phase 2 and
   updated only if the source document changes.
2. The Structure table must account for **every** structural element — omissions
   here lead to missed content in the completeness QA gate.
3. Fiction-specific and technical-specific extensions are not mutually exclusive;
   a narrative non-fiction work about medicine may use both.
4. High-risk items drive research priorities in Phase 3 and receive extra
   attention during QA gates in Phase 7.
5. The Source Map is referenced by the Chunk_Manifest (for segmentation
   decisions) and by QA gates (for completeness verification).
