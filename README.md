# D Transcreate Skill

An agent-agnostic skill pack for translating and transcreating long documents with
controlled terminology, consistent voice, and durable state across context windows.

Supports fiction, technical manuals, legal/policy material, scripts, subtitles, and
mixed-format sources. Works with Codex, Claude Code, Cursor, OpenCode, and any
generic agent that reads instruction files.

## Repository Layout

```
d-transcreate-skill/
├── core/                    # Single source of truth
│   ├── d-transcreate.md     # Canonical entrypoint (≤ 200 lines)
│   ├── workflows/           # 7 workflow guides
│   ├── schemas/             # 10 artifact schemas
│   └── prompts/             # 7 subagent role prompts
├── adapters/                # Platform-specific template layouts
│   ├── codex/               # OpenAI Codex adapter
│   ├── claude-code/         # Claude Code adapter
│   ├── cursor/              # Cursor adapter
│   ├── opencode/            # OpenCode adapter
│   └── generic/             # Any agent (no tool-specific syntax)
├── examples/                # Runnable example bundles
│   ├── fiction-short/       # Fiction translation demo
│   ├── technical-manual/    # Technical manual demo
│   └── legal-policy/        # Legal/policy demo
├── scripts/                 # Maintainer tooling
│   ├── validate_pack.py     # Repository integrity checks
│   └── build_adapters.py    # Install adapter into consumer project
├── README.md                # This file (bilingual EN/VI)
└── AGENTS.md                # Generic-agent bootstrap
```

## Quick Start

### For Translation Agents

1. Identify your platform adapter under `adapters/`.
2. Read the adapter entrypoint (e.g., `SKILL.md`, `CLAUDE.md`, or `AGENTS.md`).
3. Follow the pointer to `core/d-transcreate.md` for the canonical workflow.
4. Execute the seven-phase workflow: Intake → Scan → Research → Plan → Translate → Merge → QA.

### For Maintainers

1. Edit content only under `core/`. Adapters are thin pointers — never duplicate workflow text.
2. Validate after every change:
   ```bash
   python scripts/validate_pack.py .
   ```
3. Build an adapter into a consumer project:
   ```bash
   python scripts/build_adapters.py --platform <name> --dest <path>
   ```
4. Validate the installed destination:
   ```bash
   python scripts/validate_pack.py <path>
   ```

## Validation and Build Commands

### Validate the repository

```bash
python scripts/validate_pack.py .
```

Options:
- `--line-budget N` — Maximum lines for adapter entrypoints (default: 200)
- `--duplication-threshold N` — Warn on duplicated blocks of N+ lines (default: 20)
- `--json` — Machine-readable JSON output

Exit code is non-zero on any error. Warnings (duplication, language ratio) do not fail.

### Build an adapter into a project

```bash
python scripts/build_adapters.py --platform <codex|claude-code|cursor|opencode|generic> --dest <path>
```

Options:
- `--mode <copy|symlink|dry-run>` — Installation mode (default: copy)
- `--core-strategy <copy|reference>` — How to handle core files (default: copy)
- `--shared-core-path <path>` — Path to shared core when using reference strategy
- `--force` — Overwrite existing files at destination

The build script produces a `.d-transcreate-manifest.json` at the destination.

## Maintainer Update Workflow

1. Make changes under `core/` (workflows, schemas, or prompts).
2. Run `python scripts/validate_pack.py .` to catch broken links, missing files, or budget violations.
3. If adapters need updating (rare — they are pointers), edit under `adapters/<platform>/`.
4. Re-validate.
5. To propagate changes to consumer projects, re-run `build_adapters.py` for each installed destination.

## Design Principles

- **Single source of truth** — All workflow logic lives once under `core/`.
- **Mirrored install layout** — Adapter paths match destination project paths.
- **Artifact-as-state** — Decisions persist as workspace files, never in chat history.
- **Progressive disclosure** — Entrypoints are short; details load lazily.
- **Copyright safety** — Existing translations inform style only; no extended reproduction.

## License

See `LICENSE` file.

---

# D Transcreate Skill (Tiếng Việt)

Bộ skill dịch và chuyển ngữ (transcreate) tài liệu dài, dùng được với mọi AI agent.
Hỗ trợ fiction, tài liệu kỹ thuật, pháp lý/chính sách, kịch bản, phụ đề, và tài liệu
hỗn hợp định dạng.

## Cấu trúc thư mục

```
d-transcreate-skill/
├── core/                    # Nguồn duy nhất (single source of truth)
│   ├── d-transcreate.md     # Entrypoint chính (≤ 200 dòng)
│   ├── workflows/           # 7 hướng dẫn workflow
│   ├── schemas/             # 10 schema artifact
│   └── prompts/             # 7 prompt cho subagent
├── adapters/                # Template theo từng nền tảng
│   ├── codex/               # OpenAI Codex
│   ├── claude-code/         # Claude Code
│   ├── cursor/              # Cursor
│   ├── opencode/            # OpenCode
│   └── generic/             # Agent bất kỳ
├── examples/                # Ví dụ chạy được
│   ├── fiction-short/       # Demo dịch fiction
│   ├── technical-manual/    # Demo dịch kỹ thuật
│   └── legal-policy/        # Demo dịch pháp lý
├── scripts/                 # Công cụ cho maintainer
│   ├── validate_pack.py     # Kiểm tra tính toàn vẹn repo
│   └── build_adapters.py    # Cài adapter vào project đích
├── README.md                # File này (song ngữ EN/VI)
└── AGENTS.md                # Bootstrap cho agent
```

## Bắt đầu nhanh

### Dành cho AI Agent

1. Tìm adapter phù hợp nền tảng của bạn trong `adapters/`.
2. Đọc entrypoint của adapter (ví dụ: `SKILL.md`, `CLAUDE.md`, hoặc `AGENTS.md`).
3. Theo con trỏ đến `core/d-transcreate.md` để đọc workflow chính.
4. Thực hiện 7 phase: Intake → Quét → Nghiên cứu → Lập kế hoạch → Dịch → Gộp → QA.

### Dành cho Maintainer

1. Chỉ sửa nội dung trong `core/`. Adapter chỉ là con trỏ — không bao giờ copy nội dung workflow.
2. Kiểm tra sau mỗi thay đổi:
   ```bash
   python scripts/validate_pack.py .
   ```
3. Cài adapter vào project đích:
   ```bash
   python scripts/build_adapters.py --platform <tên> --dest <đường_dẫn>
   ```
4. Kiểm tra project đích:
   ```bash
   python scripts/validate_pack.py <đường_dẫn>
   ```

## Lệnh kiểm tra và build

### Kiểm tra repo

```bash
python scripts/validate_pack.py .
```

Tùy chọn:
- `--line-budget N` — Giới hạn dòng cho entrypoint adapter (mặc định: 200)
- `--duplication-threshold N` — Cảnh báo khi block trùng lặp ≥ N dòng (mặc định: 20)
- `--json` — Xuất JSON

Exit code khác 0 khi có lỗi. Cảnh báo (trùng lặp, tỷ lệ ngôn ngữ) không gây fail.

### Build adapter vào project

```bash
python scripts/build_adapters.py --platform <codex|claude-code|cursor|opencode|generic> --dest <đường_dẫn>
```

Tùy chọn:
- `--mode <copy|symlink|dry-run>` — Chế độ cài đặt (mặc định: copy)
- `--core-strategy <copy|reference>` — Cách xử lý core (mặc định: copy)
- `--shared-core-path <path>` — Đường dẫn core dùng chung (khi dùng reference)
- `--force` — Ghi đè file đã tồn tại

Script tạo file `.d-transcreate-manifest.json` tại đích.

## Quy trình cập nhật cho Maintainer

1. Sửa nội dung trong `core/` (workflows, schemas, hoặc prompts).
2. Chạy `python scripts/validate_pack.py .` để phát hiện link hỏng, file thiếu, hoặc vượt giới hạn dòng.
3. Nếu adapter cần cập nhật (hiếm khi — chúng chỉ là con trỏ), sửa trong `adapters/<platform>/`.
4. Kiểm tra lại.
5. Để cập nhật project đích, chạy lại `build_adapters.py` cho từng đích đã cài.

## Nguyên tắc thiết kế

- **Nguồn duy nhất** — Toàn bộ logic workflow chỉ nằm một lần trong `core/`.
- **Layout cài đặt phản chiếu** — Đường dẫn adapter khớp với đường dẫn project đích.
- **Artifact-as-state** — Quyết định lưu thành file, không lưu trong chat history.
- **Progressive disclosure** — Entrypoint ngắn; chi tiết nạp khi cần.
- **An toàn bản quyền** — Bản dịch có sẵn chỉ dùng để học văn phong; không sao chép.

## Giấy phép

Xem file `LICENSE`.
