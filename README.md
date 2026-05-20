# D Transcreate Skill

**Production-grade translation and transcreation workflow for AI agents.**

Version: **0.3.0**<br>
License: **PolyForm Noncommercial 1.0.0**<br>
Status: **Ready to use for noncommercial projects**

D Transcreate Skill turns a general-purpose coding agent into a disciplined
translation/transcreation operator for long-form, high-stakes documents. It is
built for projects where quality depends on more than sentence-by-sentence
translation: terminology control, register, continuity, chunk planning,
fidelity review, formatting preservation, and resumable state.

It works across multiple agent platforms while keeping one canonical workflow in
`core/`.

## Why this exists

Long documents fail in AI translation when the agent loses global context,
invents terminology, changes character voice, drops details, or cannot resume
cleanly after a context reset. This pack solves those problems by making the
agent operate through durable artifacts:

- a translation brief before work begins;
- source maps, context plans, and chunk manifests before translation;
- glossaries, style sheets, story bibles, and domain maps as shared memory;
- subagent dispatch plans when work is delegated;
- per-chunk summaries for resumability;
- mandatory QA gates before delivery.

## Best for

- Books, fiction, web novels, scripts, subtitles, and dialogue-heavy material.
- Technical manuals, API docs, product documentation, and developer guides.
- Legal, policy, compliance, and other terminology-sensitive documents.
- Mixed-format sources where structure, code blocks, variables, tables, links,
  and citations must be preserved.
- Any project that needs faithful translation with controlled transcreation.

## Supported agent platforms

| Platform | Adapter path | Entry point |
|---|---|---|
| OpenAI Codex | `adapters/codex/` | `SKILL.md` |
| Claude Code | `adapters/claude-code/` | `.claude/skills/d-transcreate/SKILL.md` |
| Cursor | `adapters/cursor/` | `.cursor/rules/d-transcreate.mdc` |
| OpenCode | `adapters/opencode/` | `opencode.json` |
| Generic agents | `adapters/generic/` | `d-transcreate.md` |

## What is included

```text
d-transcreate-skill/
├── core/                    # Single source of truth
│   ├── d-transcreate.md     # Canonical entrypoint
│   ├── workflows/           # 7 workflow guides
│   ├── schemas/             # 12 artifact schemas
│   └── prompts/             # 7 subagent role prompts
├── adapters/                # Platform-specific thin wrappers
├── examples/                # Fiction, technical, and legal/policy examples
├── scripts/                 # Validation and adapter build tooling
├── tests/                   # Smoke tests for packaging and validation
├── AGENTS.md                # Generic-agent bootstrap
├── CHANGELOG.md             # Release notes
├── LICENSE                  # Noncommercial license terms
└── VERSION                  # Current version
```

## Core workflow

Every serious translation job follows the same seven phases:

1. **Intake** — define source, target, audience, register, quality bar, and constraints.
2. **Scan** — inspect the whole document before translating any chunk.
3. **Research** — establish terminology, style, domain rules, and continuity facts.
4. **Plan** — create a context plan, segment into safe semantic chunks, and create a manifest.
5. **Translate** — draft, compare, revise, and summarize each chunk.
6. **Coordinate** — create a dispatch plan when delegating, merge chunks, resolve conflicts, and run a unified voice pass.
7. **QA** — run fidelity, terminology, language-quality, continuity, data, and formatting gates.

The canonical entry point is `core/d-transcreate.md`.

## Install an adapter into a consumer project

From the repository root:

```bash
python3 scripts/build_adapters.py \
  --platform <codex|claude-code|cursor|opencode|generic> \
  --dest <path-to-consumer-project>
```

Common options:

- `--mode copy` — copy files into the destination project (default).
- `--mode symlink` — symlink files for local development.
- `--mode dry-run` — preview the install without writing files.
- `--core-strategy copy` — install the canonical `core/` directory into the destination (default).
- `--core-strategy reference --shared-core-path <path>` — keep one shared `core/` and rewrite adapter references.
- `--force` — overwrite existing destination files.

Each install writes `.d-transcreate-manifest.json` with the target platform,
pack version, source commit, install options, and file hashes.

## Use the skill as an agent

1. Open the adapter entry point for your platform.
2. Follow its pointer to `core/d-transcreate.md`.
3. Create the required artifacts before translating:
   - `translation-brief.md`
   - `source-map.md`
   - `glossary.md`
   - `style-sheet.md`
   - `context-plan.md`
   - `chunk-manifest.md`
4. Add `story-bible.md` for narrative work or `domain-map.md` for technical/legal work.
5. If delegating work, create `subagent-dispatch-plan.md` before dispatching workers.
6. Translate chunk-by-chunk and persist chunk summaries.
7. Run the QA gates before presenting the final output.

## Validate the pack

Run these checks before every release:

```bash
python3 -m py_compile scripts/validate_pack.py scripts/build_adapters.py tests/test_pack.py
python3 scripts/validate_pack.py .
python3 tests/test_pack.py
```

The validator checks required files, adapter frontmatter, internal links,
placeholder markers, core references, line budgets, duplicated adapter text,
UTF-8 readability, schema references, example READMEs, install manifests, and
context/subagent orchestration references.

Machine-readable output is available with:

```bash
python3 scripts/validate_pack.py . --json
```

## Release checklist

- [ ] `VERSION` contains the intended release version.
- [ ] `CHANGELOG.md` has a dated entry for the release.
- [ ] `python3 scripts/validate_pack.py .` passes with zero errors.
- [ ] `python3 tests/test_pack.py` passes.
- [ ] All five adapters build and validate.
- [ ] License terms match the intended distribution policy.
- [ ] Orchestration docs mention `Context_Plan` and `Subagent_Dispatch_Plan` consistently.

## Design principles

- **Single source of truth** — workflow logic lives once under `core/`.
- **Thin adapters** — platform files point to the canonical workflow instead of duplicating it.
- **Artifacts as state** — decisions are stored in files, not ephemeral chat history.
- **Context-safe operation** — context plans, chunking, artifact slices, and summaries make long projects resumable.
- **Coordinator-controlled delegation** — dispatch plans let workers operate on scoped slices while the coordinator owns final decisions.
- **Fidelity first** — meaning, structure, facts, and register come before surface fluency.
- **Copyright safety** — existing translations may inform terminology or style only; do not copy them.

## License

This project is licensed under **PolyForm Noncommercial License 1.0.0**.

You may use, copy, modify, and redistribute this software for noncommercial
purposes. Commercial use is not permitted without a separate commercial license
from the copyright holder.

See `LICENSE` for the full terms.

---

# D Transcreate Skill (Tiếng Việt)

**Workflow dịch và chuyển ngữ chuyên nghiệp cho AI agent.**

Phiên bản: **0.3.0**<br>
Giấy phép: **PolyForm Noncommercial 1.0.0**<br>
Trạng thái: **Sẵn sàng dùng cho dự án phi thương mại**

D Transcreate Skill biến một coding agent tổng quát thành một operator dịch/
chuyển ngữ có quy trình chặt chẽ cho tài liệu dài và tài liệu đòi hỏi chất
lượng cao. Pack này tập trung vào những yếu tố làm nên bản dịch tốt: thuật ngữ
nhất quán, giọng văn, continuity, chia chunk, kiểm tra fidelity, giữ formatting,
và khả năng resume sau khi context bị reset.

Pack hỗ trợ nhiều nền tảng agent nhưng chỉ duy trì một workflow chuẩn trong
`core/`.

## Vì sao cần pack này

Dịch tài liệu dài bằng AI thường hỏng vì agent mất context tổng thể, tự chế
thuật ngữ, đổi giọng nhân vật, bỏ sót ý, hoặc không resume sạch sau khi hết
context. Pack này giải quyết bằng cách bắt agent làm việc qua các artifact bền
vững:

- translation brief trước khi bắt đầu;
- source map, context plan và chunk manifest trước khi dịch;
- glossary, style sheet, story bible, domain map làm bộ nhớ chung;
- subagent dispatch plan khi có giao việc cho worker;
- summary từng chunk để resume;
- QA gates bắt buộc trước khi giao bản cuối.

## Phù hợp cho

- Sách, fiction, web novel, kịch bản, phụ đề, và nội dung nhiều hội thoại.
- Manual kỹ thuật, API docs, product docs, developer guides.
- Tài liệu pháp lý, chính sách, compliance, và tài liệu nhạy cảm về thuật ngữ.
- Source hỗn hợp định dạng cần giữ cấu trúc, code block, biến, bảng, link, citation.
- Dự án cần dịch faithful nhưng vẫn transcreate có kiểm soát khi cần.

## Nền tảng hỗ trợ

| Nền tảng | Adapter | Entry point |
|---|---|---|
| OpenAI Codex | `adapters/codex/` | `SKILL.md` |
| Claude Code | `adapters/claude-code/` | `.claude/skills/d-transcreate/SKILL.md` |
| Cursor | `adapters/cursor/` | `.cursor/rules/d-transcreate.mdc` |
| OpenCode | `adapters/opencode/` | `opencode.json` |
| Agent bất kỳ | `adapters/generic/` | `d-transcreate.md` |

## Bên trong có gì

```text
d-transcreate-skill/
├── core/                    # Nguồn chuẩn duy nhất
│   ├── d-transcreate.md     # Entrypoint canonical
│   ├── workflows/           # 7 hướng dẫn workflow
│   ├── schemas/             # 12 schema artifact
│   └── prompts/             # 7 prompt cho subagent
├── adapters/                # Wrapper mỏng theo nền tảng
├── examples/                # Ví dụ fiction, kỹ thuật, pháp lý/chính sách
├── scripts/                 # Công cụ validate và build adapter
├── tests/                   # Smoke test cho packaging và validation
├── AGENTS.md                # Bootstrap cho generic agent
├── CHANGELOG.md             # Ghi chú phát hành
├── LICENSE                  # Điều khoản phi thương mại
└── VERSION                  # Phiên bản hiện tại
```

## Workflow chính

Mỗi job dịch nghiêm túc đi qua 7 phase:

1. **Intake** — xác định source, target, audience, register, quality bar, constraints.
2. **Scan** — quét toàn tài liệu trước khi dịch bất kỳ chunk nào.
3. **Research** — chốt thuật ngữ, style, domain rules, continuity facts.
4. **Plan** — tạo context plan, chia semantic chunk an toàn, và tạo manifest.
5. **Translate** — draft, compare, revise, summarize từng chunk.
6. **Coordinate** — tạo dispatch plan khi giao việc, merge chunk, xử lý conflict, và chạy voice pass thống nhất.
7. **QA** — kiểm tra fidelity, thuật ngữ, chất lượng ngôn ngữ, continuity, dữ liệu, formatting.

Entrypoint chuẩn là `core/d-transcreate.md`.

## Cài adapter vào project dùng thật

Chạy từ root repo:

```bash
python3 scripts/build_adapters.py \
  --platform <codex|claude-code|cursor|opencode|generic> \
  --dest <đường-dẫn-project-đích>
```

Tùy chọn thường dùng:

- `--mode copy` — copy file vào project đích (mặc định).
- `--mode symlink` — symlink file để phát triển local.
- `--mode dry-run` — xem trước mà không ghi file.
- `--core-strategy copy` — cài cả thư mục `core/` vào project đích (mặc định).
- `--core-strategy reference --shared-core-path <path>` — dùng chung một `core/` và rewrite reference.
- `--force` — ghi đè file đã tồn tại.

Mỗi lần cài tạo `.d-transcreate-manifest.json` gồm nền tảng đích, version, commit
nguồn, tùy chọn cài đặt, và hash file.

## Cách agent dùng skill

1. Mở entry point adapter đúng nền tảng.
2. Theo con trỏ đến `core/d-transcreate.md`.
3. Tạo các artifact bắt buộc trước khi dịch:
   - `translation-brief.md`
   - `source-map.md`
   - `glossary.md`
   - `style-sheet.md`
   - `context-plan.md`
   - `chunk-manifest.md`
4. Thêm `story-bible.md` cho fiction hoặc `domain-map.md` cho kỹ thuật/pháp lý.
5. Nếu có giao việc cho worker, tạo `subagent-dispatch-plan.md` trước khi dispatch.
6. Dịch từng chunk và lưu summary.
7. Chạy QA gates trước khi giao bản cuối.

## Validate pack

Chạy các lệnh này trước mỗi release:

```bash
python3 -m py_compile scripts/validate_pack.py scripts/build_adapters.py tests/test_pack.py
python3 scripts/validate_pack.py .
python3 tests/test_pack.py
```

Validator kiểm tra file bắt buộc, frontmatter adapter, link nội bộ, placeholder,
reference tới core, line budget, duplicate adapter text, UTF-8, schema reference,
README của examples, install manifest, và reference orchestration context/subagent.

Xuất JSON:

```bash
python3 scripts/validate_pack.py . --json
```

## Checklist release

- [ ] `VERSION` đúng với release dự định.
- [ ] `CHANGELOG.md` có entry theo ngày.
- [ ] `python3 scripts/validate_pack.py .` pass với 0 error.
- [ ] `python3 tests/test_pack.py` pass.
- [ ] Cả 5 adapter build và validate được.
- [ ] License đúng chính sách phân phối mong muốn.
- [ ] Tài liệu orchestration nhắc đến `Context_Plan` và `Subagent_Dispatch_Plan` đồng nhất.

## Nguyên tắc thiết kế

- **Nguồn chuẩn duy nhất** — workflow logic chỉ nằm trong `core/`.
- **Adapter mỏng** — file theo nền tảng chỉ trỏ về workflow chuẩn, không duplicate logic.
- **Artifact là state** — quyết định lưu trong file, không phụ thuộc chat history.
- **An toàn context** — context plan, chunking, artifact slice và summary giúp dự án dài resume được.
- **Coordinator kiểm soát giao việc** — dispatch plan giúp worker chỉ làm trên scope được giao, coordinator giữ quyền quyết định cuối.
- **Fidelity trước tiên** — nghĩa, cấu trúc, dữ kiện, register quan trọng hơn fluency bề mặt.
- **An toàn bản quyền** — bản dịch có sẵn chỉ dùng để tham khảo thuật ngữ/style; không copy.

## Giấy phép

Dự án dùng **PolyForm Noncommercial License 1.0.0**.

Bạn có thể dùng, copy, sửa, và phân phối lại phần mềm này cho mục đích phi
thương mại. Không được dùng thương mại nếu chưa có giấy phép thương mại riêng
từ chủ sở hữu bản quyền.

Xem `LICENSE` để biết đầy đủ điều khoản.
