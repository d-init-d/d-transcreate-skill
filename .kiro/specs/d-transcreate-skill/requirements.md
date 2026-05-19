# Requirements Document

## Introduction

`d-transcreate-skill` là một bộ skill (hướng dẫn vận hành) được đóng gói cho các AI coding/writing agent dùng để dịch và chuyển ngữ (transcreate) sách, tài liệu dài, fiction, tài liệu kỹ thuật, pháp lý/chính sách, kịch bản, và tài liệu hỗn hợp định dạng. Mục tiêu của bộ skill là buộc agent thực hiện một quy trình đủ chặt để dịch sát ý nhất: quét toàn tài liệu trước khi dịch, lập glossary và style sheet từ nghiên cứu thuật ngữ, ghi nhớ mạch truyện hoặc bản đồ chuyên ngành, chia chunk theo ranh giới ngữ nghĩa, dịch theo nhiều pass, có thể chạy song song qua subagent, và đi qua các QA gate trước khi giao kết quả.

Bộ skill được thiết kế là **agent-agnostic**: dùng được với Codex, Claude Code, OpenCode, Cursor, và bất kỳ agent CLI/IDE nào hỗ trợ một dạng instruction file. Repo có một core duy nhất là single source of truth, các adapter chỉ là lớp mỏng để từng nền tảng biết khi nào nạp core đó. Bộ skill có chiến lược chống tràn context cho tài liệu dài, tuân thủ bản quyền (không sao chép bản dịch có bản quyền, chỉ học thuật ngữ và văn phong), và tích hợp tùy chọn với `d-research-skill` cho phần tra cứu thuật ngữ và văn phong.

Người dùng chính của bộ skill là **AI agent** (đọc và thực thi). Người dùng thứ cấp là **người dịch / khách hàng cuối** ra lệnh cho agent. Người dùng thứ ba là **maintainer** của repo skill.

## Glossary

- **D_Transcreate_Pack**: Toàn bộ repo `d-transcreate-skill`, gồm core library, adapter packs, examples, và scripts.
- **Core_Library**: Thư mục `core/` chứa entrypoint, workflow, schema, và prompt mẫu — là single source of truth cho mọi agent.
- **Adapter_Pack**: Một thư mục con trong `adapters/` đóng gói tài liệu hướng dẫn theo cách riêng của một nền tảng cụ thể (Codex, Claude Code, Cursor, OpenCode, Generic).
- **Translation_Agent**: Bất kỳ AI agent nào (Codex, Claude Code, OpenCode, Cursor, hoặc agent generic) đọc bộ skill và thực thi tác vụ dịch.
- **Coordinator_Subagent**: Subagent chịu trách nhiệm điều phối tổng thể, giữ quyết định về glossary/style/continuity, và thực hiện merge cuối.
- **Worker_Subagent**: Subagent thực hiện một scope hẹp (terminology research, style research, chunk translation, continuity review, fidelity review, formatting review).
- **Translation_Brief**: Artifact ghi nhận intake — nguồn, đích, audience, mode, output format, quality bar, ràng buộc.
- **Source_Map**: Artifact ghi nhận kết quả quét toàn tài liệu — cấu trúc, hazard, repeated blocks, phần rủi ro cao.
- **Glossary**: Artifact ghi nhận thuật ngữ và quyết định dịch (CSV hoặc tương đương), gồm preferred/forbidden translations, evidence, confidence, status.
- **Style_Sheet**: Artifact ghi nhận quyết định về register, sentence rhythm, dialogue punctuation, terms of address, honorifics, format conventions.
- **Story_Bible**: Artifact ghi nhớ mạch truyện cho fiction — characters, timeline, places, continuity threads, terms of address.
- **Domain_Map**: Artifact ghi nhớ bản đồ chuyên ngành cho technical/legal/medical — concepts, acronyms, units, formal data.
- **Chunk_Manifest**: Sổ theo dõi các chunk — id, source location, dependencies, assigned worker, status, output path, QA status.
- **Chunk_Summary**: Bản tóm tắt nén của một chunk sau khi dịch xong, dùng để tải lên context khi dịch chunk kế tiếp.
- **Unresolved_Issues_Log**: Sổ ghi các vấn đề mở chưa giải quyết trong quá trình dịch.
- **QA_Report**: Báo cáo QA cuối — completeness, fidelity, terminology, target-language quality, continuity, numbers, formatting, residual risks.
- **Validation_Script**: Script kiểm tra tính toàn vẹn của repo (file bắt buộc, frontmatter, link nội bộ, adapter trỏ đúng core).
- **Adapter_Build_Script**: Script `scripts/build-adapters` xuất một Adapter_Pack ra layout cài đặt cho nền tảng đích, hỗ trợ chế độ copy, symlink, và dry-run, đồng thời phát sinh manifest cài đặt.
- **D_Research_Skill**: Bộ skill `d-research-skill` (tùy chọn) cung cấp năng lực tra cứu nguồn và bằng chứng có cấu trúc. D_Research_Skill được coi là **accessible** với một Translation_Agent khi (a) nó được cài như sibling skill trong skill registry của agent, hoặc (b) nó hiện diện như sibling repo hoặc submodule có path tham chiếu được, hoặc (c) nó được explicitly enabled qua cấu hình.
- **EARS**: Easy Approach to Requirements Syntax — định dạng yêu cầu dùng trong tài liệu này.
- **Progressive_Disclosure**: Nguyên tắc thiết kế: entrypoint ngắn, chi tiết được lazy-load qua reference files khi agent thật sự cần.

## Requirements

### Requirement 1: Repository Architecture (Kiến trúc repo)

**User Story:** Là một maintainer, tôi muốn repo có cấu trúc cố định và rõ ràng, để bất kỳ adapter mới hay subagent mới đều có chỗ đặt xác định và không xung đột với phần khác.

#### Acceptance Criteria

1. THE D_Transcreate_Pack SHALL contain a top-level `core/` directory that holds the single source of truth for all workflows, schemas, and prompts.
2. THE D_Transcreate_Pack SHALL contain a top-level `adapters/` directory with one subdirectory per supported platform: `codex/`, `claude-code/`, `cursor/`, `opencode/`, and `generic/`.
3. THE D_Transcreate_Pack SHALL contain a top-level `examples/` directory with at least one fiction example, one technical example, and one legal/policy example.
4. THE D_Transcreate_Pack SHALL contain a top-level `scripts/` directory with at least one validation script.
5. THE D_Transcreate_Pack SHALL contain a top-level `README.md` and a top-level `AGENTS.md`.
6. THE D_Transcreate_Pack SHALL place all reusable workflow content under `core/workflows/`, all artifact schemas under `core/schemas/`, and all subagent prompts under `core/prompts/`.
7. IF a maintainer adds a new adapter, THEN THE Adapter_Pack SHALL reside under `adapters/<platform-name>/` and SHALL NOT duplicate workflow content already present in `core/`.

### Requirement 2: Single Source of Truth (Core là nguồn duy nhất)

**User Story:** Là một maintainer, tôi muốn workflow logic chỉ được viết một lần ở core, để các adapter không bị lệch nội dung và việc cập nhật chỉ diễn ra ở một chỗ.

#### Acceptance Criteria

1. THE Core_Library SHALL contain the canonical entrypoint document `core/d-transcreate.md` describing operating principles and the core workflow.
2. THE Core_Library SHALL contain workflow files under `core/workflows/` covering at minimum: long-document, terminology-research, fiction-continuity, technical-domain, qa-gates, context-management, and subagents.
3. THE Core_Library SHALL contain artifact schema files under `core/schemas/` covering at minimum: translation-brief, source-map, glossary, style-sheet, story-bible, domain-map, chunk-manifest, and qa-report.
4. THE Core_Library SHALL contain subagent prompt files under `core/prompts/` covering at minimum: coordinator, terminology-researcher, style-researcher, chunk-translator, continuity-reviewer, fidelity-reviewer, and formatting-reviewer.
5. WHEN an Adapter_Pack needs workflow content, THE Adapter_Pack SHALL reference files under `core/` by relative path instead of duplicating their text.
6. THE Adapter_Pack SHALL reference at least one file under `core/` either by relative path link or by an explicit pointer in adapter content. AN Adapter_Pack entrypoint SHALL NOT exceed a configurable line budget (default 200 lines for the primary entrypoint file).

### Requirement 3: Multi-Adapter Support (Hỗ trợ nhiều nền tảng agent)

**User Story:** Là một AI agent chạy trên một nền tảng cụ thể, tôi muốn tìm thấy entrypoint phù hợp với cơ chế tải hướng dẫn của nền tảng mình, để tôi có thể bắt đầu dịch mà không cần biết về các nền tảng khác.

#### Acceptance Criteria

1. THE Adapter_Pack for Codex SHALL provide a `SKILL.md` file with valid frontmatter and SHALL provide an `agents/openai.yaml` interface descriptor.
2. THE Adapter_Pack for Claude Code SHALL provide `.claude/skills/d-transcreate/SKILL.md` with YAML frontmatter, SHALL provide subagent files under `.claude/agents/`, and SHALL provide a project-level `CLAUDE.md` bootstrap.
3. THE Adapter_Pack for Cursor SHALL provide `.cursor/rules/d-transcreate.mdc` configured as Agent-Requested or Manual rule type, and SHALL provide a root `AGENTS.md` bootstrap.
4. THE Adapter_Pack for OpenCode SHALL provide a project-level `AGENTS.md`, an `opencode.json` referencing the Core_Library via the `instructions` field, and subagent files under `.opencode/agents/`.
5. THE Adapter_Pack for Generic agents SHALL provide a plain `AGENTS.md` and a plain `d-transcreate.md` that do not depend on any tool-specific syntax.
6. WHERE a Cursor rule is provided, THE Cursor Adapter_Pack SHALL NOT configure the rule as always-loaded.
7. WHEN a Translation_Agent reads its platform's adapter entrypoint, THE Adapter_Pack SHALL provide enough information to locate and read the Core_Library without requiring the agent to scan the full repository.
8. EACH Adapter_Pack under `adapters/<platform>/` SHALL be a **template/source layout**, not a set of files intended to be loaded directly from `adapters/<platform>/` at runtime by the consumer project.
9. THE Adapter_Pack SHALL store its files at paths that **mirror the destination project layout**, so installation can be done by copying or symlinking the adapter folder into the consumer project (or via the Adapter_Build_Script defined in Requirement 29). Examples of mirrored paths: `adapters/cursor/.cursor/rules/d-transcreate.mdc`, `adapters/cursor/AGENTS.md`, `adapters/opencode/AGENTS.md`, `adapters/opencode/opencode.json`, `adapters/opencode/.opencode/agents/<role>.md`, `adapters/claude-code/.claude/skills/d-transcreate/SKILL.md`, `adapters/claude-code/.claude/agents/<role>.md`, `adapters/claude-code/CLAUDE.md`, `adapters/codex/SKILL.md`, `adapters/codex/agents/openai.yaml`, `adapters/generic/AGENTS.md`, `adapters/generic/d-transcreate.md`.
10. WHEN a maintainer or end user installs the pack into a target project, THE installation SHALL be performed either by manually copying or symlinking the adapter folder into the target project, or by running the Adapter_Build_Script defined in Requirement 29; THE Adapter_Pack SHALL NOT require additional file rewriting beyond what the Adapter_Build_Script performs.

### Requirement 4: Documentation Language Policy (Chính sách ngôn ngữ tài liệu)

**User Story:** Là một AI agent đa nền tảng, tôi cần tài liệu lõi viết bằng tiếng Anh ổn định để hiểu chính xác, trong khi người dùng cuối Việt Nam vẫn cần đọc README dễ dàng.

#### Acceptance Criteria

1. THE Core_Library SHALL be written in English.
2. THE Adapter_Pack entrypoints SHALL be written in English.
3. THE top-level `README.md` SHALL contain both an English section and a Vietnamese section, in that order.
4. THE Validation_Script SHALL verify that every file under `core/` and `adapters/` is valid UTF-8 encoded text. THE Validation_Script MAY emit a warning when files under `core/` contain a high ratio of non-ASCII characters that suggest non-English instructional prose, but THE Validation_Script SHALL NOT fail the build on language content alone.
5. WHERE a maintainer adds a localized README, THE additional README SHALL reside at the top level with a locale suffix (for example, `README.vi.md`) and SHALL NOT replace the bilingual `README.md`.

### Requirement 5: Intake and Translation Brief (Intake và brief dịch)

**User Story:** Là một Translation_Agent, tôi cần một bước intake bắt buộc để xác định nguồn, đích, audience, mode, format, và quality bar trước khi dịch, để tránh dịch sai mục tiêu.

#### Acceptance Criteria

1. WHEN a Translation_Agent starts a translation task, THE Core_Library SHALL require the agent to produce a Translation_Brief artifact before any chunk translation begins.
2. THE Translation_Brief SHALL capture the following fields: source files, source language, target language, target locale, audience, translation mode, register, output format, formatting constraints, do-not-translate items, terminology authority, research depth, quality bar, and open questions.
3. IF a required Translation_Brief field is missing and cannot be inferred at low risk, THEN THE Translation_Agent SHALL ask the user a single focused question for that field before proceeding.
4. WHEN the user does not specify a translation mode, THE Translation_Agent SHALL default to faithful translation with light transcreation for idioms and dialogue.
5. THE Core_Library SHALL provide a Translation_Brief schema under `core/schemas/translation-brief.md` that the agent populates.

### Requirement 6: Whole-Document Scan and Source Map (Quét toàn tài liệu)

**User Story:** Là một Translation_Agent, tôi cần quét toàn tài liệu một lần trước khi dịch, để phát hiện hazard và lập source map làm cơ sở cho mọi quyết định sau đó.

#### Acceptance Criteria

1. WHEN a Translation_Brief has been produced, THE Translation_Agent SHALL perform a single whole-document scan before producing any chunk translation.
2. THE Source_Map SHALL list every chapter, section, table, figure, footnote, caption, appendix, reference, and repeated block detected during the scan.
3. THE Source_Map SHALL flag formatting hazards including OCR noise, broken hyphenation, missing pages, encoding issues, and ambiguous structure.
4. WHEN the source is fiction, THE Translation_Agent SHALL also capture cast list, relationships, point of view per chapter, timeline, locations, motifs, and reveal structure during the scan.
5. WHEN the source is technical, legal, medical, financial, or academic, THE Translation_Agent SHALL also capture domain, governing standards or laws, acronyms, units, and canonical sources during the scan.
6. THE Core_Library SHALL provide a Source_Map schema under `core/schemas/source-map.md`.

### Requirement 7: Terminology Research and Glossary (Nghiên cứu thuật ngữ)

**User Story:** Là một Translation_Agent, tôi cần một quy trình rõ ràng để mine thuật ngữ, tra cứu bản dịch chính thống, và lập glossary trước khi dịch chunk, để bản dịch nhất quán và có bằng chứng.

#### Acceptance Criteria

1. WHEN the Source_Map has been produced, THE Translation_Agent SHALL mine candidate terms from the source before assigning any chunk for translation.
2. THE Glossary SHALL contain at minimum the following columns: source term, preferred translation, forbidden translation, term class, context, source location, evidence, confidence, status, and notes.
3. THE Glossary SHALL use status values from the set {`proposed`, `approved`, `needs-review`, `deprecated`} and confidence values from the set {`high`, `medium`, `low`}.
4. WHEN multiple sources disagree on a term translation, THE Translation_Agent SHALL record both candidates with their evidence and SHALL choose based on source priority defined in `core/workflows/terminology-research.md`.
5. THE Core_Library SHALL define a source priority order with official localized sources from the rights holder ranked highest and machine-translated or unsourced aggregations ranked lowest.
6. IF a term is high impact and no high-confidence evidence is found, THEN THE Translation_Agent SHALL mark the term as `needs-review` and SHALL add it to the Unresolved_Issues_Log.
7. IF a term is low impact and research yields no new candidates, THEN THE Translation_Agent SHALL mark the term as provisional and SHALL continue translation rather than blocking.

### Requirement 8: Style Research and Style Sheet (Nghiên cứu văn phong)

**User Story:** Là một Translation_Agent, tôi cần học văn phong của thể loại và thị trường đích bằng cách tham khảo bản dịch phổ biến, để bản dịch nghe tự nhiên với người đọc đích, mà không vi phạm bản quyền.

#### Acceptance Criteria

1. WHEN preparing for chunk translation, THE Translation_Agent SHALL research target-language style conventions for the relevant genre or domain and SHALL record decisions in the Style_Sheet.
2. THE Style_Sheet SHALL capture register, formality, sentence rhythm, dialogue punctuation, terms of address, honorifics, number/date/unit conventions, citation conventions, footnote policy, and adaptation rules for idioms, humor, cultural references, metaphors, repetition, and quoted material.
3. THE Translation_Agent SHALL use existing translations to learn conventions only and SHALL NOT reproduce extended passages from copyrighted translations.
4. THE Translation_Agent SHALL document, for each non-trivial style decision, the rationale and source observation in the Style_Sheet notes.
5. THE Core_Library SHALL provide a Style_Sheet schema under `core/schemas/style-sheet.md`.

### Requirement 9: Memory Setup for Fiction (Story Bible)

**User Story:** Là một Translation_Agent dịch fiction, tôi cần một story bible để theo dõi nhân vật, timeline, và các thread liên tục, để không làm lộ twist sớm hoặc gây mâu thuẫn giữa các chương.

#### Acceptance Criteria

1. WHEN the source is classified as fiction, memoir, narrative non-fiction, script, game, or comic, THE Translation_Agent SHALL create and maintain a Story_Bible artifact.
2. THE Story_Bible SHALL contain tables for characters (with name forms, voice, relationships), timeline events, places, continuity threads, and terms of address.
3. WHEN a character is referenced in a chunk being translated, THE Translation_Agent SHALL load the relevant Story_Bible rows into context for that chunk.
4. WHEN the source contains a hidden relationship, gender, twist, or worldbuilding fact that is revealed later, THE Translation_Agent SHALL choose target-language wording that does not expose the reveal earlier than the source.
5. WHEN a chunk introduces a new character, place, relationship, or motif, THE Translation_Agent SHALL update the Story_Bible after translating that chunk.
6. THE Core_Library SHALL provide a Story_Bible schema under `core/schemas/story-bible.md`.

### Requirement 10: Memory Setup for Technical/Legal/Medical (Domain Map)

**User Story:** Là một Translation_Agent dịch tài liệu chuyên ngành, tôi cần một domain map để giữ nhất quán khái niệm, acronym, đơn vị, và tham chiếu pháp lý/chuẩn, để không làm sai dữ liệu hoặc tham chiếu chéo.

#### Acceptance Criteria

1. WHEN the source is classified as technical, legal, medical, financial, academic, product, or policy material, THE Translation_Agent SHALL create and maintain a Domain_Map artifact.
2. THE Domain_Map SHALL capture domain field, audience expertise, governing standards or laws, canonical sources, concepts (with definitions and preferred translations), acronyms (with translation policy), and units and formal-data conventions.
3. WHEN a chunk references a concept already present in the Domain_Map, THE Translation_Agent SHALL apply the preferred translation recorded there.
4. IF a chunk introduces a new concept or acronym not yet in the Domain_Map, THEN THE Translation_Agent SHALL add it to the Domain_Map before completing the chunk.
5. THE Core_Library SHALL provide a Domain_Map schema under `core/schemas/domain-map.md`.

### Requirement 11: Chunking by Semantic Boundaries (Chia chunk theo ngữ nghĩa)

**User Story:** Là một Translation_Agent dịch tài liệu dài, tôi cần chia chunk theo ranh giới ngữ nghĩa thay vì cắt máy móc theo token, để tránh phá vỡ mạch lập luận hoặc câu thoại.

#### Acceptance Criteria

1. THE Translation_Agent SHALL segment work by semantic units in this preference order: chapter or article section, scene or subsection, paragraph group, table or figure or caption group, footnote or endnote group tied to its anchor.
2. THE Translation_Agent SHALL NOT split a chunk in the middle of a sentence, a paragraph, a table row, or a single dialogue exchange.
3. THE Translation_Agent SHALL keep each chunk small enough to fit, in active context, alongside the Translation_Brief, the relevant Glossary slice, the relevant Style_Sheet rules, the relevant Story_Bible or Domain_Map slice, and the previous and next Chunk_Summary.
4. THE Translation_Agent SHALL assign each chunk a stable identifier following a predictable pattern such as `ch03-sec02` or `p012-018`.
5. THE Chunk_Manifest SHALL record, for each chunk, the chunk identifier, source location, word or page range, semantic unit, dependencies, assigned worker, status, output path, QA status, and notes.
6. THE Chunk_Manifest status field SHALL use values from the set {`planned`, `research-needed`, `ready`, `drafting`, `drafted`, `qa-needed`, `revising`, `done`, `blocked`}.

### Requirement 12: Multi-Pass Translation (Dịch nhiều pass)

**User Story:** Là một Translation_Agent, tôi cần dịch mỗi chunk qua nhiều pass có mục đích khác nhau, để vừa giữ trung thành với nguồn vừa đạt độ trôi chảy ở ngôn ngữ đích.

#### Acceptance Criteria

1. WHEN translating a chunk, THE Translation_Agent SHALL perform a draft pass that produces a faithful translation using the current Translation_Brief, Glossary, Style_Sheet, Story_Bible or Domain_Map, and adjacent Chunk_Summary entries.
2. WHEN the draft pass is complete, THE Translation_Agent SHALL perform a source-compare pass that checks for omissions, additions, mistranslated negation, modality, causality, chronology, agency, and consistency of names, numbers, citations, and formatting.
3. WHEN the source-compare pass is complete, THE Translation_Agent SHALL perform a target-language revision pass that improves fluency without changing meaning, preserves author voice, and keeps technical precision.
4. WHEN the revision pass is complete, THE Translation_Agent SHALL perform a state-update pass that updates the Glossary, Style_Sheet, Story_Bible or Domain_Map, Chunk_Summary, and Unresolved_Issues_Log for the chunk just completed.
5. IF the chunk contains numbers, dates, currencies, formulas, citations, URLs, code identifiers, UI strings, equation labels, or table references, THEN THE source-compare pass SHALL preserve the underlying values and identifiers exactly. Format conversions for dates, units, currencies, and number notation SHALL be applied only when explicitly specified in the Translation_Brief or Style_Sheet, and SHALL follow the documented conversion rule recorded there.
6. IF a term in the chunk is ambiguous and no glossary entry resolves it, THEN THE Translation_Agent SHALL mark the term as uncertain in the chunk output and SHALL add it to the Unresolved_Issues_Log instead of guessing.

### Requirement 13: Subagent Orchestration (Điều phối subagent)

**User Story:** Là một Translation_Agent, tôi muốn dùng subagent chạy song song khi nền tảng cho phép, để rút ngắn thời gian dịch trong khi vẫn giữ được tính nhất quán toàn cục.

#### Acceptance Criteria

1. THE Translation_Agent SHALL NOT dispatch any Worker_Subagent before the Translation_Brief, Source_Map, Glossary with proposed core terms, Style_Sheet, Chunk_Manifest, and Story_Bible or Domain_Map exist.
2. THE Coordinator_Subagent SHALL retain final authority over Glossary changes, Style_Sheet decisions, voice consistency, and continuity across chunks.
3. THE Translation_Agent SHALL assign each Worker_Subagent a disjoint scope from the role set: terminology research, style research, chunk translation, continuity review, fidelity review, or formatting review.
4. WHEN dispatching a Worker_Subagent, THE Coordinator_Subagent SHALL provide only the relevant Translation_Brief excerpt, relevant Glossary rows, relevant Style_Sheet rules, relevant Story_Bible or Domain_Map notes, and the chunk text or term list, instead of the full document.
5. THE Worker_Subagent SHALL return a structured output containing at minimum: produced artifact or translated text, list of changed files, uncertain items, and proposals for Glossary or Style_Sheet changes.
6. THE Translation_Agent SHALL NOT allow two Worker_Subagent instances to edit the same output file in parallel.
7. WHERE a platform does not support parallel subagents, THE Translation_Agent SHALL execute the same role responsibilities sequentially while preserving the same artifact handoff contract.

### Requirement 14: Merge and Final Voice Pass (Gộp và pass voice cuối)

**User Story:** Là một Coordinator_Subagent, tôi cần gộp output của các chunk theo thứ tự nguồn và chạy một pass voice cuối tập trung, để loại bỏ mạch không liền và lệch văn phong giữa các chunk.

#### Acceptance Criteria

1. WHEN all assigned chunks have status `done` in the Chunk_Manifest, THE Coordinator_Subagent SHALL merge their outputs in source order.
2. THE Coordinator_Subagent SHALL run cross-chunk consistency checks for terminology, headings, table labels, captions, footnotes, references, and punctuation.
3. WHEN cross-chunk consistency checks complete, THE Coordinator_Subagent SHALL run a single final voice pass over the merged output centrally instead of letting individual Worker_Subagent instances perform it.
4. IF the merge step detects conflicting Glossary applications across chunks, THEN THE Coordinator_Subagent SHALL resolve them against the approved Glossary entries before producing the final output.
5. THE Coordinator_Subagent SHALL update the Story_Bible or Domain_Map with any continuity facts emitted by Worker_Subagent outputs that were accepted.

### Requirement 15: QA Gates (Cổng QA bắt buộc)

**User Story:** Là một Translation_Agent, tôi cần đi qua tất cả các QA gate trước khi giao kết quả, để bắt được thiếu sót, sai trung thành, lệch thuật ngữ, và lỗi định dạng.

#### Acceptance Criteria

1. THE Translation_Agent SHALL run the following QA gates before final delivery: completeness, fidelity, terminology, target-language quality, continuity, numbers and formal data, formatting, and residual risk reporting.
2. THE completeness gate SHALL verify that every source chunk has translated output and that headings, captions, footnotes, tables, lists, figures, appendices, references, and callouts are accounted for.
3. THE fidelity gate SHALL check for mistranslated negation, changed causality, changed chronology, softened or strengthened claims, incorrect modality, wrong speaker or referent, and added explanation not present in the source.
4. THE terminology gate SHALL verify that approved Glossary terms are applied consistently and that forbidden translations do not appear.
5. THE numbers and formal data gate SHALL verify that the underlying values and identifiers (citations, URLs, code identifiers, equation labels, table references) match the source exactly, and SHALL verify that any format conversions applied (date format, unit conversion, currency conversion, number notation) follow conversion rules documented in the Translation_Brief or Style_Sheet.
6. THE Translation_Agent SHALL produce a QA_Report artifact summarizing the checks performed, issues found, resolutions, and residual risks.
7. WHERE the source is high-stakes legal, medical, financial, academic, or safety material, THE Translation_Agent SHALL require source-backed terminology decisions and SHALL include explicit residual-risk notes in the QA_Report.

### Requirement 16: Context Overflow Strategy (Chiến lược chống tràn context)

**User Story:** Là một Translation_Agent đang dịch tài liệu rất dài, tôi cần một chiến lược nạp context theo nhu cầu chunk-by-chunk, để không bao giờ phải nạp toàn bộ tài liệu vào context cùng lúc.

#### Acceptance Criteria

1. THE Translation_Agent SHALL NOT load the full source document into active context unless the document genuinely fits with room for QA.
2. WHEN translating a chunk, THE Translation_Agent SHALL load only the Translation_Brief, the relevant Glossary slice, the relevant Style_Sheet rules, the relevant Story_Bible or Domain_Map excerpt, the previous Chunk_Summary, the next Chunk_Summary when available, the current source chunk, and Unresolved_Issues entries that affect this chunk.
3. WHEN a chunk translation is complete, THE Translation_Agent SHALL write a compact Chunk_Summary and SHALL unload the raw source chunk from working memory.
4. WHEN a context reset occurs, THE Translation_Agent SHALL re-open the Chunk_Manifest first, then the Translation_Brief, Style_Sheet, Glossary, and the current chunk source, and SHALL reconstruct only the continuity needed from Chunk_Summary entries.
5. IF a platform does not support lazy reference loading natively, THEN the corresponding Adapter_Pack entrypoint SHALL instruct the Translation_Agent to read related artifact files on demand by file path.
6. THE Core_Library SHALL document this context budget rule in `core/workflows/context-management.md`.

### Requirement 17: Resumability (Khả năng tiếp tục sau gián đoạn)

**User Story:** Là một Translation_Agent bị gián đoạn giữa chừng (timeout, context reset, chuyển phiên), tôi cần khôi phục trạng thái dịch chỉ từ artifacts ghi trên đĩa, để tiếp tục từ chunk chưa xong mà không làm lại phần đã hoàn thành.

#### Acceptance Criteria

1. THE Translation_Agent SHALL persist the Translation_Brief, Source_Map, Glossary, Style_Sheet, Story_Bible or Domain_Map, Chunk_Manifest, Chunk_Summary entries, Unresolved_Issues_Log, and QA_Report as files in the workspace, not in chat history.
2. WHEN a Translation_Agent resumes a translation task, THE Translation_Agent SHALL read the Chunk_Manifest first to determine the first chunk whose status is not `done` and SHALL load the artifacts required for that chunk.
3. THE Chunk_Manifest SHALL be the authoritative status ledger; if a chunk file exists on disk but the Chunk_Manifest does not record it as `done`, THE Translation_Agent SHALL treat the chunk as not yet complete.
4. THE Core_Library SHALL document the resume procedure in `core/workflows/context-management.md`.

### Requirement 18: Copyright and Source Safety (An toàn bản quyền)

**User Story:** Là một maintainer chịu trách nhiệm pháp lý, tôi muốn bộ skill ngăn agent sao chép bản dịch có bản quyền, để tránh rủi ro vi phạm.

#### Acceptance Criteria

1. THE Translation_Agent SHALL NOT reproduce extended passages from copyrighted translations and SHALL NOT translate by patching together existing translations.
2. THE Translation_Agent SHALL use existing translations only to identify official term choices, observe punctuation and register patterns, and paraphrase style principles in its own words.
3. WHEN the Translation_Agent quotes from an existing translation for evidence in the Glossary or Style_Sheet, THE quoted excerpt SHALL be short and SHALL include a source reference in the artifact notes.
4. IF a term choice depends on observation of an existing translation, THEN THE Translation_Agent SHALL record that influence source in the Glossary notes rather than hide it.
5. THE Core_Library SHALL state these copyright rules explicitly in `core/d-transcreate.md` and in `core/workflows/terminology-research.md`.

### Requirement 19: Optional d-research Integration (Tích hợp d-research tùy chọn)

**User Story:** Là một Translation_Agent có quyền truy cập `d-research-skill`, tôi muốn ủy quyền việc tra cứu nguồn và bằng chứng cho `d-research`, để tận dụng khả năng tìm kiếm có cấu trúc và đánh giá chất lượng nguồn.

#### Acceptance Criteria

1. WHERE D_Research_Skill is accessible AND the user has not disabled it in the Translation_Brief, THE Translation_Agent SHOULD delegate terminology source discovery, multilingual research, evidence logging, and source-quality checks to D_Research_Skill.
2. WHERE D_Research_Skill is not accessible or has been disabled, THE Translation_Agent SHALL fall back to the research protocol defined in `core/workflows/terminology-research.md` without blocking the translation workflow.
3. THE D_Transcreate_Pack SHALL NOT declare D_Research_Skill as a hard dependency in any adapter manifest.
4. THE Core_Library SHALL document both the integration pattern and the fallback protocol in `core/workflows/terminology-research.md`.

### Requirement 20: Subagent Pack Definitions (Bộ subagent chuẩn)

**User Story:** Là một maintainer, tôi muốn bộ subagent có vai trò và scope cố định, để adapter của bất kỳ nền tảng nào cũng map được sang cùng một cấu trúc trách nhiệm.

#### Acceptance Criteria

1. THE Core_Library SHALL define the following subagent roles with documented scopes and output contracts: `transcreate-coordinator`, `terminology-researcher`, `style-researcher`, `chunk-translator`, `continuity-reviewer`, `fidelity-reviewer`, and `formatting-reviewer`.
2. THE `transcreate-coordinator` role SHALL be responsible for planning, holding Glossary, Style_Sheet, and continuity authority, and performing the final merge.
3. THE `terminology-researcher` role SHALL be responsible for finding terms, identifying official sources, and producing Glossary proposals with evidence.
4. THE `style-researcher` role SHALL be responsible for studying genre and target-market style conventions and producing Style_Sheet observations with source notes.
5. THE `chunk-translator` role SHALL be responsible for translating one assigned chunk according to the Translation_Brief, Glossary, and Style_Sheet.
6. THE `continuity-reviewer` role SHALL be responsible for checking story continuity, character voice, timeline, and reveal timing for narrative material.
7. THE `fidelity-reviewer` role SHALL be responsible for source-versus-target comparison and detection of omissions, additions, and meaning shifts.
8. THE `formatting-reviewer` role SHALL be responsible for checking tables, footnotes, headings, citations, and layout fidelity.
9. THE Core_Library SHALL provide a prompt file under `core/prompts/` for each role listed in this requirement.

### Requirement 21: Artifact Schema Stability (Ổn định schema artifact)

**User Story:** Là một subagent ở bất kỳ nền tảng nào, tôi cần các artifact có schema cố định, để output của tôi tương thích với coordinator và với QA gates mà không cần điều chỉnh.

#### Acceptance Criteria

1. THE Core_Library SHALL define schemas for Translation_Brief, Source_Map, Glossary, Style_Sheet, Story_Bible, Domain_Map, Chunk_Manifest, Chunk_Summary, Unresolved_Issues_Log, and QA_Report.
2. THE Glossary schema SHALL be expressible as either CSV with documented columns or as a Markdown table with the same columns.
3. THE Chunk_Manifest schema SHALL be expressible as either CSV with documented columns or as a Markdown table with the same columns.
4. WHEN a schema field is added or removed, THE maintainer SHALL update both the schema file in `core/schemas/` and any prompt files in `core/prompts/` that reference the field.
5. THE Validation_Script SHALL verify that every schema referenced from a workflow file or prompt file exists in `core/schemas/`.

### Requirement 22: Validation Script (Script kiểm tra repo)

**User Story:** Là một maintainer, tôi muốn một script kiểm tra tự động đảm bảo repo không gãy link, không thiếu file bắt buộc, và không có placeholder TODO, để mỗi commit đều ở trạng thái dùng được.

#### Acceptance Criteria

1. THE D_Transcreate_Pack SHALL provide a `scripts/validate-pack` Validation_Script implemented in a portable form (for example, Python or Node) and runnable from the repo root.
2. THE Validation_Script SHALL verify that every required file listed in Requirements 1, 2, 3, 20, and 21 exists.
3. THE Validation_Script SHALL verify that adapter entrypoints with frontmatter contain valid YAML frontmatter and required fields.
4. THE Validation_Script SHALL verify that every internal Markdown link in `core/`, `adapters/`, and top-level documents resolves to an existing file or anchor.
5. THE Validation_Script SHALL verify that no file under `core/` or `adapters/` contains the literal strings `TODO`, `TBD`, or `FIXME` as placeholder content.
6. THE Validation_Script SHALL verify that every Adapter_Pack references at least one file under `core/`, and SHALL verify that every Adapter_Pack entrypoint stays within the configured line budget. THE Validation_Script MAY emit a warning (not an error) when a contiguous block of 20 or more lines in an Adapter_Pack file matches a block in any `core/` file at exact text or near-duplicate similarity, leaving the duplication threshold configurable.
7. THE Validation_Script SHALL exit with a non-zero status code when any check fails and SHALL print the failing file path and reason for each failure.

### Requirement 23: Example Tests (Bộ ví dụ kiểm thử)

**User Story:** Là một maintainer, tôi muốn ba ví dụ ngắn (fiction, technical, legal) để xác minh rằng một agent mới có thể chạy bộ skill end-to-end mà không cần context ngoài.

#### Acceptance Criteria

1. THE D_Transcreate_Pack SHALL provide an `examples/fiction-short/` example containing a short fiction source of two to three scenes.
2. THE D_Transcreate_Pack SHALL provide an `examples/technical-manual/` example containing two to three technical sections.
3. THE D_Transcreate_Pack SHALL provide an `examples/legal-policy/` example containing a short legal or policy excerpt.
4. WHEN a Translation_Agent runs an example end-to-end, THE example SHALL guide the agent to produce all default artifacts (Translation_Brief, Source_Map, Glossary, Style_Sheet, Story_Bible or Domain_Map, Chunk_Manifest, Chunk_Summary entries, Unresolved_Issues_Log, and QA_Report) and a translated output.
5. THE Validation_Script SHALL verify that each example folder contains a `README.md` describing the example, the source file or files, and the expected artifact set.
6. THE D_Transcreate_Pack SHALL NOT commit copyrighted source material into examples; example sources SHALL be either original content authored for the repo or excerpts under a permissive license with attribution.

### Requirement 24: Onboarding Guarantee for New Agents (Bảo đảm onboarding)

**User Story:** Là một AI agent lần đầu mở repo, tôi cần đọc adapter của nền tảng mình rồi dịch được example mà không cần thêm context bên ngoài, để bộ skill thực sự cross-platform.

#### Acceptance Criteria

1. WHEN a Translation_Agent on a supported platform reads only its Adapter_Pack entrypoint and the files that entrypoint references, THE Translation_Agent SHALL have enough information to complete any of the three example tasks defined in Requirement 23.
2. THE Adapter_Pack entrypoint SHALL list the Core_Library files needed for a minimal translation run and SHALL describe in what order to read them.
3. THE Translation_Agent SHALL NOT be required to load the entire repository to complete an example.
4. WHEN two different Translation_Agent instances on two different supported platforms run the same example with the same Translation_Brief, the same seed Glossary, and the same seed Style_Sheet, THE produced translated outputs SHALL apply every approved seed Glossary entry and every approved seed Style_Sheet rule identically across both runs.
5. WHEN two different Translation_Agent instances on two different supported platforms run the same example, THE produced artifact set SHALL include the same artifact files, SHALL use the same schema columns, and SHALL populate the same required fields. Differences in newly proposed (non-seeded) Glossary or Style_Sheet entries are acceptable as long as schema and required fields remain consistent.

### Requirement 25: Output Determinism within a Run (Tính nhất quán trong một run)

**User Story:** Là một người dùng cuối, tôi cần bản dịch của một tài liệu giữ nhất quán thuật ngữ và văn phong từ đầu đến cuối, ngay cả khi nhiều chunk được dịch song song.

#### Acceptance Criteria

1. WITHIN a single translation run, THE Translation_Agent SHALL apply approved Glossary entries identically across all chunks.
2. WITHIN a single translation run, THE Translation_Agent SHALL apply Style_Sheet decisions identically across all chunks.
3. IF a chunk-level decision conflicts with the Glossary or Style_Sheet, THEN THE Coordinator_Subagent SHALL either update the Glossary or Style_Sheet (with rationale) or reject the chunk-level decision before merge.
4. WHEN parallel Worker_Subagent instances propose conflicting Glossary or Style_Sheet changes, THE Coordinator_Subagent SHALL resolve the conflict before final merge and SHALL record the resolution in the artifact notes.

### Requirement 26: Error and Edge-Case Handling (Xử lý lỗi và biên)

**User Story:** Là một Translation_Agent, tôi cần xử lý rõ ràng các tình huống lỗi (file hỏng, OCR sai, ngôn ngữ trộn, định dạng lạ), để không tạo bản dịch kém chất lượng trong im lặng.

#### Acceptance Criteria

1. IF the source file cannot be extracted to text, THEN THE Translation_Agent SHALL stop the workflow, record the extraction failure in the Source_Map, and ask the user how to proceed.
2. IF the source contains mixed languages and the Translation_Brief does not specify how to handle them, THEN THE Translation_Agent SHALL ask the user before proceeding and SHALL record the decision in the Style_Sheet.
3. IF a chunk contains content that violates the user's do-not-translate list, THEN THE Translation_Agent SHALL preserve the source form unchanged and SHALL note the preservation in the Chunk_Summary.
4. IF the Translation_Agent detects OCR noise, broken hyphenation, or encoding corruption that would change meaning, THEN THE Translation_Agent SHALL flag the affected lines in the Source_Map and the Unresolved_Issues_Log instead of guessing the original text.
5. THE Translation_Agent SHALL never silently invent, omit, simplify, or reorder source meaning to make the chunk easier to translate.

### Requirement 27: Progressive Disclosure (Tiết lộ thông tin theo nhu cầu)

**User Story:** Là một AI agent có giới hạn context, tôi muốn entrypoint ngắn và chỉ phải đọc reference khi thật sự cần, để không lãng phí context budget vào hướng dẫn không liên quan.

#### Acceptance Criteria

1. THE entrypoint document `core/d-transcreate.md` SHALL contain only operating principles, the high-level core workflow, and pointers to reference files.
2. THE entrypoint document `core/d-transcreate.md` SHALL NOT exceed an instructional length that would dominate a typical agent context window when combined with the user's source.
3. THE Core_Library SHALL split detailed workflow content across separate files under `core/workflows/` so that an agent loads only the workflow files relevant to the current step.
4. EACH Adapter_Pack entrypoint SHALL follow the same progressive-disclosure rule: short bootstrap content with explicit references to the Core_Library files for detail.

### Requirement 28: Maintainer Update Workflow (Quy trình cập nhật cho maintainer)

**User Story:** Là một maintainer, tôi muốn quy trình cập nhật rõ ràng, để khi sửa core thì các adapter và validation script vẫn nhất quán.

#### Acceptance Criteria

1. WHEN a maintainer modifies a file under `core/`, THE Validation_Script SHALL be runnable to detect any broken references, missing schemas, or duplicated workflow text in adapters.
2. WHEN a maintainer adds a new subagent role, THE maintainer SHALL add the role definition to `core/d-transcreate.md`, add the role prompt to `core/prompts/`, and update each Adapter_Pack to expose the role using the platform's native subagent mechanism.
3. WHEN a maintainer adds a new artifact schema, THE maintainer SHALL add the schema file to `core/schemas/` and update any workflow or prompt file that references it.
4. THE top-level `README.md` SHALL document the maintainer update workflow and the command to run the Validation_Script.

### Requirement 29: Adapter Build and Export (Build/Export adapter pack)

**User Story:** Là một maintainer hoặc end user cài skill vào dự án, tôi muốn có một script export adapter cho nền tảng đã chọn, copy đúng layout vào dự án đích, và phát sinh install manifest, để việc cài đặt có thể tự động hóa và tái lập được.

#### Acceptance Criteria

1. THE D_Transcreate_Pack SHALL provide an `scripts/build-adapters` Adapter_Build_Script implemented in a portable form (for example, Python or Node) and runnable from the repo root.
2. THE Adapter_Build_Script SHALL accept at minimum these parameters: target platform (one of `codex`, `claude-code`, `cursor`, `opencode`, `generic`), destination path (default current working directory), and operation mode (one of `copy`, `symlink`, `dry-run`).
3. WHEN invoked with a target platform, THE Adapter_Build_Script SHALL place the corresponding `adapters/<platform>/` contents at the destination using the same relative paths as in the adapter folder, so the layout matches the platform's expected install location.
4. WHEN core references are needed at the destination, THE Adapter_Build_Script SHALL either copy the referenced `core/` files alongside the adapter at the destination, or rewrite relative path references in adapter files to point at a configurable shared core location.
5. WHERE the destination already contains files that would be overwritten, THE Adapter_Build_Script SHALL refuse to overwrite unless an explicit `--force` flag is provided, and SHALL exit with a non-zero status code listing the conflicting paths.
6. WHEN run in `dry-run` mode, THE Adapter_Build_Script SHALL print every file operation it would perform without modifying the filesystem.
7. WHEN an install completes, THE Adapter_Build_Script SHALL write a manifest file `.d-transcreate-manifest.json` at the destination recording the source repo commit or version, the target platform, the timestamp, and the list of files installed.
8. THE Validation_Script SHALL be runnable against the destination after install to confirm completeness and that internal references resolve.
