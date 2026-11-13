# Locale Profile: Vietnamese (`vi` / `vi-VN`)

Auto-load this profile whenever `Translation_Brief` specifies `target_language` as `vi`, `vi-VN`, or `Vietnamese`. Record project-specific overrides in `style-sheet.md` and `research-dossier.md`.

---

## 1. Vietnamese Pronoun and Terms of Address System

Vietnamese pronouns encode age, kinship, hierarchy, intimacy, gender, and emotional stance in every utterance. Never translate `I` and `you` mechanically as `toi` and `ban` across a book.

### 1.1 Core Axes

- **Age and Kinship**: `anh/em`, `chi/em`, `chu/chau`, `bac/chau`, `co/chau`, `ong/chau`, `ba/chau`, `bo-cha/con`, `me-ma/con`.
- **Hierarchy and Respect**: `ngai` (dignitary/official), `ong/ba` (formal adult), `quy vi` (plural formal audience), `thay/con` or `thay/em` (teacher-student), `su phu/de tu` (master-disciple), `be ha / than` (monarch-subject).
- **Intimacy and Peer Dynamics**: `cau/to` (warm school/young-adult peers), `minh/cau` or `anh/em` (affectionate), `may/tao` (childhood best friends, street slang, or open hostility), `han/y/ga/mu` (third-person distance, suspicion, or contempt).

### 1.2 Genre Presets

| Genre / Domain | Default Pronoun Baseline | Guidance |
|---|---|---|
| Historical / Fantasy / Wuxia / Xianxia | `ta/nguoi`, `tai ha/cac ha`, `huynh/de`, `ty/muoi`, `tien sinh`, `ton gia`, `be ha` | Match period gravity and martial/court hierarchy; avoid modern urban pronouns (`cau/to`, `ban`) unless deliberate comic contrast. |
| Modern Western Fiction | `toi/anh`, `anh/em`, `toi/co`, `cau/to`, `may/tao` | Infer age and intimacy from context and `Story_Bible`; reserve `toi/ban` for wary strangers, business equals, or cold politeness. |
| Non-Fiction / Technical / Legal | `ban` or `chung ta` (reader-inclusive), `quy doc gia`, `tac gia`, impersonal/active phrasing | Keep consistent across the whole book; avoid shifting randomly between `ban`, `cac ban`, and `quy vi`. |

### 1.3 Mid-Scene Shifts and Continuity

- Map every recurring speaker-addressee pair in the `Research_Dossier` Pronoun and Address Matrix before Phase 5 begins.
- A mid-scene pronoun shift (e.g., `toi/anh` -> `em/anh` or `cau/to` -> `may/tao`) is valid **only** when triggered by an emotional rupture, confession, rank reversal, or reveal.
- Document intentional shifts in `Story_Bible` and `Chunk_Summary` so `continuity-reviewer` distinguishes deliberate narrative pivots from accidental drift.

---

## 2. Sino-Vietnamese (Han-Viet) vs. Native Vietnamese (Thuan Viet) Balance

Vietnamese prose draws tonal weight from balancing two lexical strata:

- **Sino-Vietnamese (Han-Viet)** — conveys formality, philosophical abstraction, legal authority, historical gravitas, and mythic scale (e.g., `cong ly`, `giao uoc`, `dinh menh`, `co vat`, `tham quyen`, `bien nien su`).
- **Native Vietnamese (Thuan Viet)** — conveys sensory immediacy, physical action, emotional warmth, humor, and colloquial speech (e.g., `dau thuong`, `run ray`, `nong ran`, `gion mat`, `chia tay`).

### Register Calibration Rules

1. Match the stratum to the narrator and speaker: an archaic chronicler or legal code leans Han-Viet; a street urchin's dialogue leans Thuan Viet.
2. Avoid tonal whiplash within one sentence (for example, pairing high-court Han-Viet phrasing with modern internet slang unless parody is intended).
3. Use `memory/glossary-vi.csv` for pre-solved canonical renderings of recurring literary, legal, psychological, and technical concepts.

---

## 3. Proper Noun and Special Term Policy

Follow the `Research_Dossier` classification (`official_published`, `community_established`, `partial`, or `none`):

1. **Retain Source Spelling**: Keep modern Western, Latin-script personal names, brands, and contemporary places in original form (`Sherlock Holmes`, `London`, `MIT`) when standard in modern Vietnamese publishing.
2. **Track A Canon First**: If an official or widely established Vietnamese translation exists, inherit its canonical personal names, toponyms, and signature terms unless `Translation_Brief` specifies a fresh re-translation.
3. **East Asian Classical / Historical Names**: Follow standard Han-Viet reading for classical Chinese/historical names and titles when appropriate to the genre and target-market canon.
4. **Descriptive Epithets, Titles, and Organizations**: Translate meaningful titles, ranks, guilds, artifacts, and spells (`The High Council` -> `Hoi dong Toi cao` / approved canon) and lock them in `glossary.csv`.
5. **First-Mention Glosses**: When an opaque cultural term or neologism needs clarification and `Style_Sheet` allows notes, add a single concise inline parenthetical or `[ND: ...]` footnote on first mention only; never repeat glosses in later chunks.

---

## 4. Anti-Translatorese Forbidden Patterns

Check every chunk during Pass C (`chunk-translator`) and Peer Cross-Check (`continuity-reviewer`) to eliminate mechanical calques from English or other source languages:

| Forbidden Pattern | Why It Fails in Vietnamese | Preferred Natural Remedy |
|---|---|---|
| Mechanical passive `bi` / `duoc` | Overusing `bi` for neutral events or `duoc` for inanimate subjects (`canh cua duoc mo boi anh ay`) sounds robotic. | Use active voice (`anh mo cua`) or natural Vietnamese topic-comment order (`cua da mo`). Reserve `bi` for adverse events and `duoc` for genuine benefit/receipt. |
| Mechanical `-ly` adverbial calques (`mot cach ...`) | Strings like `anh nhin co mot cach buon ba` feel stiff and translated. | Use direct verb-adjective combinations or idiomatic adverbs (`anh nhin co buon ba`, `anh buon ba nhin co`). |
| Abstract nominalization bloat (`su ...`, `viec ...`, `tinh ...`) | Literal noun chains (`viec thuc hien su phat trien cua ...`) weigh down prose. | Convert abstract nouns back into clear verbs and actors (`phat trien ...`, `khi ho thuc hien ...`). |
| Stiff relative-clause chains (`ma`, `cai ma`, `nguoi ma`, `noi ma`) | Chaining multiple `ma` clauses mirrors English `which/who/where` syntax awkwardly. | Split long sentences into natural sequential clauses or omit redundant `ma` connectors. |
| Redundant possessives (`cua toi`, `cua anh ay`, `cua co ay`) | Translating every `his/her/my` (`anh ta dat tay cua anh ta len vai cua co ta`) bloats dialogue and action. | Drop `cua` when ownership is obvious from context (`anh dat tay len vai co`). |
| Calqued copulas and tense markers (`la mot`, `da va dang`, `o trong`) | Mechanical `da va dang` or `la mot nguoi dan ong cao lon` reads like machine translation. | Use natural aspect markers (`van dang`, `tung`) or drop redundant `mot` before predicative adjectives/nouns. |

---

## 5. Vietnamese Book Typography and Dialogue Conventions

Record the chosen option in `style-sheet.md` and enforce it uniformly across all chunks:

1. **Dialogue Punctuation** (pick ONE convention per project, never mix):
   - *Traditional Vietnamese Book Style*: leading em-dash (`—`) at the start of each spoken turn on a new line; reporting tags separated by em-dash or comma.
   - *Modern Quoted Style*: curly double quotes (`"..."`) for spoken dialogue and single quotes (`'...'`) for nested quotes.
2. **Numbers and Decimals**:
   - Standard Vietnamese prose/tables use dot `.` as thousands separator (`1.250.000`) and comma `,` as decimal separator (`3,14`), unless `Translation_Brief` preserves source technical/financial notation.
   - Never alter numbers inside code identifiers, URLs, semantic versions (`1.0.0`), or formal citations.
3. **Dates**:
   - Use `dd/mm/yyyy` for numeric dates and `ngay D thang M nam YYYY` in narrative prose unless the source is an ISO technical specification.
4. **Structural Headings**:
   - Use consistent Vietnamese structural labels matching `memory/glossary-vi.csv` (`Loi mo dau`, `Chuong 1`, `Loi ket`, `Phu luc`, `Muc luc`, `Chu thich cuoi trang`).
5. **Code, URLs, and Formal Anchors**:
   - Preserve URLs, markdown anchors, table alignments, and code blocks verbatim.

---

## References

- Shared Vietnamese glossary memory: `memory/glossary-vi.csv`
- Two-tier glossary workflow: `memory/README.md`
- Research dossier schema: `core/schemas/research-dossier.md`
- Style sheet schema: `core/schemas/style-sheet.md`
