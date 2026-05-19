# Requirements Document

## Introduction

The **Transcreate Skill Kit** is a Kiro Power (skill package) that instructs AI agents on how to perform high-quality translation and transcreation of books and long-form documents. The deliverable is NOT a runtime application; it is a structured set of Markdown documents — `POWER.md`, steering files, workflow guides, prompt templates, and worksheet templates — that, when installed, teach an agent a rigorous multi-phase workflow: scan the source material, extract terminology, research existing translations for stylistic reference, build persistent memory artifacts (glossary, style guide, story bible), translate in chunks (optionally via parallel sub-agents), and review for consistency.

The skill is designed to produce translations that preserve original meaning while reading naturally in the target language (transcreation philosophy, not literal translation). It must support both fiction (novels, short stories) and non-fiction (technical documents, business books, academic papers), prioritize the English → Vietnamese pair while remaining language-pair-agnostic, integrate with the `d-init-d/d-research-skill` for online research, support parallel sub-agent execution, and prescribe explicit context-window management strategies for long documents.

## Glossary

- **Transcreate_Skill**: The Kiro Power being specified by this document — the bundle of Markdown instructions installed at `.kiro/skills/transcreate/` (or as a Power) that guides agents through translation work.
- **Operating_Agent**: The AI agent that has the Transcreate_Skill activated and is performing a translation job by following the skill's instructions.
- **Sub_Agent**: A child agent spawned by the Operating_Agent to handle a discrete translation unit (e.g., one chapter) in parallel.
- **Source_Document**: The original-language document the user wants translated (a single file, a directory of chapters, or a multi-file project).
- **Target_Language**: The language the Source_Document is being translated into (e.g., Vietnamese).
- **Source_Language**: The language of the Source_Document (e.g., English).
- **Translation_Workspace**: A working directory the skill instructs the Operating_Agent to create for each job, containing all intermediate artifacts (scan report, glossary, style guide, story bible, chunked translations, review notes).
- **Glossary**: A persistent JSON or Markdown file mapping Source_Language terminology to agreed Target_Language renderings, with notes on context.
- **Style_Guide**: A persistent Markdown file capturing tone, register, sentence-rhythm conventions, and stylistic decisions for the job, learned from reference translations.
- **Story_Bible**: A persistent Markdown file (used for fiction only) tracking characters, locations, plot threads, timeline, and recurring motifs.
- **Scan_Report**: A Markdown file produced in the first phase summarizing document structure, length, content type, key terminology candidates, and recommended chunking strategy.
- **Chunk**: A unit of source text small enough to translate in a single agent turn without context overflow (typically a chapter, section, or fixed-token slice).
- **Research_Skill**: The external skill `d-init-d/d-research-skill` (referenced via its repository) which the Transcreate_Skill delegates online research to.
- **POWER.md**: The top-level entry document of the skill, loaded when an agent activates the skill.
- **Steering_File**: A focused Markdown guide (loaded on demand) that documents one phase or topic in detail.
- **Worksheet_Template**: A blank Markdown or JSON template the Operating_Agent fills in (e.g., glossary template, scan report template).
- **Quality_Gate**: A required checkpoint between phases where the Operating_Agent must verify acceptance criteria before proceeding.
- **Round_Trip_Check**: A sanity-check step where a translated Chunk is briefly back-translated (or summarized) into the Source_Language to confirm meaning preservation.

## Requirements

### Requirement 1: Skill Package Structure

**User Story:** As an agent author, I want to install the Transcreate_Skill as a single self-contained package, so that any compatible agent can activate it and immediately access the full workflow.

#### Acceptance Criteria

1. THE Transcreate_Skill SHALL provide a top-level `POWER.md` file at the package root that summarizes the skill, lists available steering files, and states activation keywords (e.g., "translate", "transcreate", "dịch", "chuyển ngữ").
2. THE Transcreate_Skill SHALL organize detailed phase instructions into separate Steering_File documents stored under a `steering/` subdirectory.
3. THE Transcreate_Skill SHALL store all reusable Worksheet_Template files (glossary, style guide, story bible, scan report, review checklist) under a `templates/` subdirectory.
4. THE Transcreate_Skill SHALL include a `README.md` at the package root describing installation, supported language pairs, and external dependencies.
5. WHERE the package is published as a git repository, THE Transcreate_Skill SHALL include a license file and a versioning note in `README.md`.
6. IF a referenced Steering_File or Worksheet_Template is missing from the package, THEN THE Transcreate_Skill SHALL fail validation during a self-check step documented in `README.md`.

### Requirement 2: Workflow Phase Definition

**User Story:** As an Operating_Agent, I want the skill to define a clear, ordered set of workflow phases, so that I can execute translations consistently without skipping steps.

#### Acceptance Criteria

1. THE Transcreate_Skill SHALL define exactly six ordered phases: (1) Intake, (2) Scan, (3) Terminology Extraction, (4) Reference Research, (5) Translation, (6) Review and Assembly.
2. FOR EACH phase, THE Transcreate_Skill SHALL specify the phase objective, required inputs, produced artifacts, success criteria, and the next phase to enter.
3. THE Transcreate_Skill SHALL require the Operating_Agent to complete a Quality_Gate before transitioning between phases.
4. WHEN the Operating_Agent enters a phase, THE Transcreate_Skill SHALL instruct the Operating_Agent to read the corresponding Steering_File before taking action.
5. IF a phase's required input artifacts are missing, THEN THE Transcreate_Skill SHALL instruct the Operating_Agent to halt and either return to the prior phase or report the gap to the user.
6. WHERE the Source_Document is fiction, THE Transcreate_Skill SHALL require the Story_Bible artifact to be initialized during the Scan phase and updated during the Translation phase.

### Requirement 3: Intake Phase

**User Story:** As an Operating_Agent starting a job, I want the skill to define the intake checklist, so that I gather all parameters before doing real work.

#### Acceptance Criteria

1. THE Transcreate_Skill SHALL instruct the Operating_Agent to confirm with the user the following parameters before proceeding: Source_Language, Target_Language, content type (fiction or non-fiction), domain (e.g., fantasy, legal, medical), target audience, desired register (formal, casual, literary), and delivery format (single file, per-chapter files).
2. THE Transcreate_Skill SHALL instruct the Operating_Agent to create a Translation_Workspace directory at a user-confirmed path and record the intake parameters in a `job.md` file inside it.
3. WHEN the user does not specify the Target_Language, THE Transcreate_Skill SHALL instruct the Operating_Agent to ask the user explicitly rather than assume.
4. IF the Source_Document is not accessible at the path provided by the user, THEN THE Transcreate_Skill SHALL instruct the Operating_Agent to report the error and halt.
5. THE Transcreate_Skill SHALL provide a Worksheet_Template `templates/job.md` with all intake fields pre-listed.

### Requirement 4: Scan Phase

**User Story:** As an Operating_Agent, I want the skill to define how to scan the entire Source_Document before translating, so that I understand structure, length, and special concerns up front.

#### Acceptance Criteria

1. THE Transcreate_Skill SHALL instruct the Operating_Agent to perform a full structural pass over the Source_Document and record findings in a Scan_Report at `<workspace>/scan-report.md`.
2. THE Scan_Report SHALL contain: total token estimate, chapter or section list with token counts, content classification (fiction vs non-fiction confirmation), top-level themes, candidate specialized terminology, named entities (characters, places, organizations), and a proposed Chunk plan.
3. WHEN the Source_Document exceeds a configurable token threshold (default: 50,000 tokens), THE Transcreate_Skill SHALL instruct the Operating_Agent to perform the scan in passes (one pass per file or chapter) and merge the results, rather than loading the full document into a single turn.
4. THE Transcreate_Skill SHALL instruct the Operating_Agent to propose a Chunk plan in which no individual Chunk exceeds a configurable token budget (default: 4,000 source tokens per chunk).
5. WHERE the Source_Document is fiction, THE Scan_Report SHALL include an initial character list and a one-line plot summary per chapter.
6. THE Transcreate_Skill SHALL provide a Worksheet_Template `templates/scan-report.md` with all required sections pre-listed.

### Requirement 5: Terminology Extraction

**User Story:** As an Operating_Agent, I want the skill to define how to extract and lock down domain terminology, so that translations stay consistent across chunks and sub-agents.

#### Acceptance Criteria

1. THE Transcreate_Skill SHALL instruct the Operating_Agent to produce a Glossary file at `<workspace>/glossary.json` containing entries with the fields: source_term, target_term, part_of_speech, domain, first_occurrence, notes, status (proposed, approved).
2. THE Transcreate_Skill SHALL instruct the Operating_Agent to extract terminology candidates from the Scan_Report and any high-frequency unique tokens in the Source_Document.
3. WHEN a terminology candidate has more than one plausible Target_Language rendering, THE Transcreate_Skill SHALL instruct the Operating_Agent to list all candidates in the entry's notes field and mark status as "proposed".
4. THE Transcreate_Skill SHALL instruct the Operating_Agent to present the proposed Glossary to the user for review and lock approved entries before the Translation phase begins.
5. WHILE the Translation phase is active, THE Transcreate_Skill SHALL instruct the Operating_Agent to treat the approved Glossary as read-mostly: new entries may be appended with status "proposed" but approved entries SHALL NOT be silently changed.
6. IF a Sub_Agent encounters a Source_Language term not present in the Glossary, THEN THE Transcreate_Skill SHALL instruct the Sub_Agent to record the term in a per-chunk `pending-terms.md` file rather than coining a new translation in isolation.
7. THE Transcreate_Skill SHALL provide a Worksheet_Template `templates/glossary.json` with one example entry.

### Requirement 6: Reference Research Phase

**User Story:** As an Operating_Agent, I want the skill to define how to study existing published translations of similar works, so that my output adopts natural, idiomatic Target_Language style.

#### Acceptance Criteria

1. THE Transcreate_Skill SHALL instruct the Operating_Agent to delegate online research for existing translations and stylistic references to the Research_Skill (`d-init-d/d-research-skill`).
2. THE Transcreate_Skill SHALL instruct the Operating_Agent to issue research queries that target: (a) published Target_Language translations of the same work if any exist, (b) published Target_Language translations of works in the same genre and era, (c) Target_Language style guides for the relevant domain.
3. THE Transcreate_Skill SHALL instruct the Operating_Agent to record research outputs as excerpts and citations in a `<workspace>/references.md` file.
4. THE Transcreate_Skill SHALL instruct the Operating_Agent to derive a Style_Guide at `<workspace>/style-guide.md` from the references, covering: register, sentence length tendencies, dialogue conventions, honorifics or pronoun policy, idiom strategy, and how to handle culture-specific items.
5. IF the Research_Skill is not installed, THEN THE Transcreate_Skill SHALL instruct the Operating_Agent to inform the user, offer to proceed using only intrinsic knowledge, and clearly mark the Style_Guide as "research-skipped".
6. THE Transcreate_Skill SHALL instruct the Operating_Agent to never reproduce more than 30 consecutive words verbatim from any single referenced source and to cite each reference inline.
7. THE Transcreate_Skill SHALL provide a Worksheet_Template `templates/style-guide.md` with section headings pre-listed.

### Requirement 7: Story Bible for Fiction

**User Story:** As an Operating_Agent translating a novel, I want the skill to define how to maintain a Story_Bible across chapters, so that character voice, plot continuity, and naming stay consistent over the whole book.

#### Acceptance Criteria

1. WHERE the content type is fiction, THE Transcreate_Skill SHALL instruct the Operating_Agent to create a Story_Bible at `<workspace>/story-bible.md` during the Scan phase.
2. THE Story_Bible SHALL contain the sections: Characters (name, role, relationships, voice notes), Locations, Timeline, Recurring Motifs, Open Questions, and Resolved Decisions.
3. WHEN a Sub_Agent translates a Chunk, THE Transcreate_Skill SHALL instruct the Sub_Agent to read the current Story_Bible before translating and append a "Story_Bible delta" to its handoff report.
4. AFTER each Translation Chunk is completed, THE Transcreate_Skill SHALL instruct the coordinating Operating_Agent to merge approved Story_Bible deltas into the main Story_Bible before the next Chunk begins or before parallel Chunks are dispatched.
5. WHERE the content type is non-fiction, THE Transcreate_Skill SHALL instruct the Operating_Agent to skip Story_Bible creation and instead maintain a `concepts.md` file tracking key concepts and their definitions.
6. THE Transcreate_Skill SHALL provide a Worksheet_Template `templates/story-bible.md` and `templates/concepts.md`.

### Requirement 8: Translation Phase Per-Chunk Procedure

**User Story:** As an Operating_Agent translating a Chunk, I want the skill to define a strict per-chunk procedure, so that each chunk respects the Glossary, Style_Guide, and Story_Bible.

#### Acceptance Criteria

1. THE Transcreate_Skill SHALL instruct the Operating_Agent (or Sub_Agent) handling a Chunk to load, in order, the Glossary, Style_Guide, and Story_Bible (if applicable) before reading the Chunk's source text.
2. THE Transcreate_Skill SHALL instruct the Operating_Agent to produce a draft translation for the Chunk and write it to `<workspace>/chunks/<chunk_id>/draft.md`.
3. THE Transcreate_Skill SHALL instruct the Operating_Agent to perform a Round_Trip_Check on at least three sampled paragraphs per Chunk by briefly summarizing the draft back into the Source_Language and comparing it against the source.
4. WHEN the Round_Trip_Check reveals a meaning shift the Operating_Agent classifies as material, THE Transcreate_Skill SHALL instruct the Operating_Agent to revise the draft and re-record the check before completing the Chunk.
5. THE Transcreate_Skill SHALL instruct the Operating_Agent to write a per-chunk handoff report at `<workspace>/chunks/<chunk_id>/handoff.md` containing: glossary additions proposed, style observations, Story_Bible delta, unresolved questions.
6. IF a Chunk's source text exceeds the configured per-chunk token budget, THEN THE Transcreate_Skill SHALL instruct the Operating_Agent to split the Chunk further before drafting, rather than truncating.
7. THE Transcreate_Skill SHALL provide a Worksheet_Template `templates/chunk-handoff.md`.

### Requirement 9: Parallel Sub-Agent Coordination

**User Story:** As an Operating_Agent, I want the skill to define how to dispatch parallel Sub_Agents safely, so that I can translate independent chunks concurrently without losing consistency.

#### Acceptance Criteria

1. THE Transcreate_Skill SHALL instruct the Operating_Agent to dispatch a Sub_Agent only after the Glossary has reached "approved" status for at least the entries that appear in the target Chunk's source text per the Scan_Report.
2. THE Transcreate_Skill SHALL instruct the Operating_Agent to pass each Sub_Agent a context bundle consisting of: the Chunk's source text, the current Glossary, the current Style_Guide, the current Story_Bible (if fiction), and the per-chunk handoff template.
3. THE Transcreate_Skill SHALL instruct the Operating_Agent to never dispatch parallel Sub_Agents for chunks whose dependencies on each other are unresolved (for example, a flashback chapter that depends on a not-yet-translated reveal). The Scan_Report SHALL classify each Chunk as either "independent" or "sequential" to support this.
4. WHEN a Sub_Agent completes, THE Transcreate_Skill SHALL instruct the Operating_Agent to validate the Sub_Agent's handoff report against the schema in `templates/chunk-handoff.md` before merging the chunk's draft.
5. IF two Sub_Agents propose conflicting Glossary or Story_Bible deltas, THEN THE Transcreate_Skill SHALL instruct the Operating_Agent to resolve the conflict by reviewing both proposals, choosing or merging, and writing the rationale to `<workspace>/decisions.md` before continuing.
6. THE Transcreate_Skill SHALL recommend a default maximum parallelism (3 Sub_Agents) and require this to be configurable per job in `job.md`.

### Requirement 10: Context Overflow Management

**User Story:** As an Operating_Agent, I want the skill to define explicit context-window management techniques, so that long documents do not cause context overflow or quality degradation.

#### Acceptance Criteria

1. THE Transcreate_Skill SHALL prescribe a chunking strategy in which each translation Chunk fits inside the configured per-chunk token budget alongside the Glossary, Style_Guide, and Story_Bible.
2. THE Transcreate_Skill SHALL instruct the Operating_Agent to maintain the Glossary, Style_Guide, and Story_Bible as compact, summarized artifacts and to refactor any of these artifacts that exceeds a configurable size threshold (default: 4,000 tokens) into a layered summary plus a detail file.
3. WHEN the Operating_Agent's working context approaches a configurable threshold (default: 70% of the agent's stated context window), THE Transcreate_Skill SHALL instruct the Operating_Agent to write progress to disk, summarize prior turns into a `<workspace>/session-notes.md` file, and resume on a fresh context.
4. THE Transcreate_Skill SHALL instruct the Operating_Agent to never load the entire Source_Document into a single context window during the Translation phase; instead, only the active Chunk plus the persistent artifacts SHALL be in context.
5. WHERE a Chunk references content from another Chunk (e.g., a quoted earlier passage), THE Transcreate_Skill SHALL instruct the Operating_Agent to load only the referenced passage from the prior Chunk's draft, not the full prior Chunk.
6. THE Transcreate_Skill SHALL include a Steering_File `steering/context-management.md` documenting the above strategies with concrete examples.

### Requirement 11: Review and Assembly Phase

**User Story:** As an Operating_Agent finishing a job, I want the skill to define a review and assembly procedure, so that the final deliverable is consistent and complete.

#### Acceptance Criteria

1. AFTER all Chunks are drafted, THE Transcreate_Skill SHALL instruct the Operating_Agent to run a consistency review across all chunks against the final Glossary, Style_Guide, and Story_Bible.
2. THE Transcreate_Skill SHALL instruct the Operating_Agent to record the consistency review findings in `<workspace>/review.md` with one entry per finding (chunk_id, finding, severity, fix).
3. THE Transcreate_Skill SHALL instruct the Operating_Agent to apply fixes for findings classified as "blocker" or "major" before assembly, and to list "minor" findings as known issues.
4. WHEN review fixes are complete, THE Transcreate_Skill SHALL instruct the Operating_Agent to assemble the final translation according to the delivery format declared in `job.md` (single file or per-chapter files) and write it to `<workspace>/output/`.
5. THE Transcreate_Skill SHALL instruct the Operating_Agent to produce a final job summary at `<workspace>/output/SUMMARY.md` listing chunks translated, glossary size, references consulted, known issues, and total source/target token counts.
6. THE Transcreate_Skill SHALL provide a Worksheet_Template `templates/review.md`.

### Requirement 12: Quality Gates

**User Story:** As an Operating_Agent, I want the skill to define explicit pass/fail Quality_Gates between phases, so that I never advance with broken inputs.

#### Acceptance Criteria

1. THE Transcreate_Skill SHALL define a Quality_Gate between every adjacent phase pair (Intake→Scan, Scan→Terminology, Terminology→Research, Research→Translation, Translation→Review, Review→Assembly).
2. EACH Quality_Gate SHALL specify the artifacts that must exist, the fields within those artifacts that must be populated, and a short verification checklist.
3. WHEN a Quality_Gate fails, THE Transcreate_Skill SHALL instruct the Operating_Agent to either (a) return to the prior phase to remediate, or (b) escalate to the user with a description of the gap.
4. THE Transcreate_Skill SHALL provide a Steering_File `steering/quality-gates.md` enumerating every gate.

### Requirement 13: Translation Quality Principles

**User Story:** As an Operating_Agent, I want the skill to encode the transcreation philosophy in concrete principles, so that I produce natural, faithful translations rather than literal ones.

#### Acceptance Criteria

1. THE Transcreate_Skill SHALL document the following principles in a Steering_File `steering/translation-principles.md`: meaning over form, naturalness in Target_Language, register consistency, glossary discipline, and cultural adaptation with citation.
2. THE Transcreate_Skill SHALL instruct the Operating_Agent to prefer the natural Target_Language phrasing when literal translation would produce awkward output, and to record the decision in the chunk handoff report.
3. THE Transcreate_Skill SHALL instruct the Operating_Agent to preserve author intent for proper nouns, idioms, and cultural items by either (a) keeping the Source_Language form with a Target_Language gloss on first occurrence, or (b) substituting a Target_Language equivalent only when the Style_Guide approves it.
4. WHEN the Source_Document contains content the Operating_Agent classifies as ambiguous in meaning, THE Transcreate_Skill SHALL instruct the Operating_Agent to record the ambiguity in `<workspace>/decisions.md` with the chosen interpretation and reasoning, rather than guessing silently.

### Requirement 14: Language Pair Flexibility

**User Story:** As a user, I want the skill to work for any language pair, so that I am not locked into one direction.

#### Acceptance Criteria

1. THE Transcreate_Skill SHALL be written so that no Steering_File hardcodes a specific Source_Language or Target_Language; both SHALL be parameters drawn from `job.md`.
2. THE Transcreate_Skill SHALL include a Steering_File `steering/language-pair-notes/en-vi.md` that captures English-to-Vietnamese specific guidance (pronoun conventions, honorifics, classifier usage, common false friends).
3. THE Transcreate_Skill SHALL allow additional `steering/language-pair-notes/<src>-<tgt>.md` files to be added without modifying any other file.
4. WHEN no language-pair-specific note exists for the active pair, THE Transcreate_Skill SHALL instruct the Operating_Agent to operate from the general principles only and to record the absence in `<workspace>/session-notes.md`.

### Requirement 15: Activation and Discovery

**User Story:** As a user invoking an agent, I want the skill to advertise its activation triggers clearly, so that the agent knows when to engage the skill.

#### Acceptance Criteria

1. THE `POWER.md` SHALL list activation keywords in both English and Vietnamese, including at minimum: "translate", "transcreate", "localize", "dịch", "chuyển ngữ", "dịch sách", "dịch tài liệu".
2. THE `POWER.md` SHALL include a one-paragraph "When to use this skill" section and a one-paragraph "When NOT to use this skill" section.
3. THE `POWER.md` SHALL list every Steering_File with a one-line description and explicit guidance on when to load each.
4. WHEN an Operating_Agent activates the skill, THE Transcreate_Skill SHALL instruct it to read `POWER.md` first and load only the Steering_Files relevant to the current phase.

### Requirement 16: External Dependency Handling

**User Story:** As a user, I want the skill to behave gracefully when optional external dependencies are unavailable, so that my translation job is not blocked by environment gaps.

#### Acceptance Criteria

1. THE Transcreate_Skill SHALL declare the Research_Skill (`d-init-d/d-research-skill`) as an optional dependency in `README.md`.
2. WHEN the Research_Skill is available, THE Transcreate_Skill SHALL instruct the Operating_Agent to use it for the Reference Research phase.
3. IF the Research_Skill is unavailable, THEN THE Transcreate_Skill SHALL instruct the Operating_Agent to proceed with research-skipped mode as defined in Requirement 6 acceptance criterion 5.
4. THE Transcreate_Skill SHALL not require any other external dependency to complete an end-to-end translation job.

### Requirement 17: User Confirmation Checkpoints

**User Story:** As a user, I want the skill to pause at decision points and ask me for confirmation, so that I retain control over translation choices.

#### Acceptance Criteria

1. THE Transcreate_Skill SHALL instruct the Operating_Agent to seek explicit user confirmation at the following points: (a) after Intake, before scanning; (b) after the Scan_Report is produced, before terminology extraction; (c) after the Glossary is proposed, before research; (d) after the Style_Guide is drafted, before translation; (e) before final assembly.
2. WHEN the user requests a "fast mode" in `job.md`, THE Transcreate_Skill SHALL allow the Operating_Agent to consolidate confirmation checkpoints (a) through (d) into a single confirmation, while still requiring confirmation before final assembly.
3. THE Transcreate_Skill SHALL instruct the Operating_Agent to summarize, at each checkpoint, what was produced and what will be produced next, in fewer than 200 words.

### Requirement 18: Localization of the Skill Itself

**User Story:** As a Vietnamese-speaking user, I want the skill's user-facing prompts and summaries to be available in Vietnamese, so that I can review checkpoints comfortably.

#### Acceptance Criteria

1. THE `POWER.md` SHALL be authored in English (the agent-internal language).
2. THE Transcreate_Skill SHALL provide user-facing checkpoint prompt templates in both English and Vietnamese under `templates/prompts/<lang>/`.
3. WHEN the active job's Target_Language is Vietnamese or the user has indicated Vietnamese as their preferred language in `job.md`, THE Transcreate_Skill SHALL instruct the Operating_Agent to use the Vietnamese checkpoint prompts.
4. THE Transcreate_Skill SHALL allow additional language directories under `templates/prompts/` without modifying any other file.

### Requirement 19: Versioning and Self-Identification

**User Story:** As an agent or user inspecting outputs, I want the skill to identify itself and its version, so that I can reproduce or audit a translation later.

#### Acceptance Criteria

1. THE `POWER.md` SHALL declare a semantic version string at the top of the file.
2. THE Transcreate_Skill SHALL instruct the Operating_Agent to record the skill version in every `<workspace>/output/SUMMARY.md` produced.
3. WHEN the skill version changes, THE Transcreate_Skill SHALL include a `CHANGELOG.md` entry summarizing the change.

### Requirement 20: Failure Recovery and Resumability

**User Story:** As a user, I want the skill to instruct the agent to make every job resumable, so that interruptions do not waste prior work.

#### Acceptance Criteria

1. THE Transcreate_Skill SHALL instruct the Operating_Agent to write all intermediate artifacts to disk before exiting any phase.
2. WHEN the Operating_Agent resumes a job, THE Transcreate_Skill SHALL instruct it to detect the latest completed phase from the artifacts present in `<workspace>/` and resume from the next phase.
3. IF artifacts indicate inconsistent state (e.g., a chunk draft exists without a handoff report), THEN THE Transcreate_Skill SHALL instruct the Operating_Agent to flag the inconsistency in `<workspace>/decisions.md` and ask the user how to proceed.
4. THE Transcreate_Skill SHALL provide a Steering_File `steering/resumability.md` documenting how to detect and resume from each phase.
