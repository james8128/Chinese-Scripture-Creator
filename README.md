# Chinese Scripture Creator

**佛說天地八陽神咒經** — generate classical vertical book pages from plain text, then read them in a simple web (or Android WebView) viewer.

**GitHub:** [james8128/Chinese-Scripture-Creator](https://github.com/james8128/Chinese-Scripture-Creator)

---

## What this project is

This is a small personal toolkit for Chinese Buddhist scripture pages:

1. **`create_pages.py`** — lays out the sutra like a traditional book  
   (vertical columns, right → left, double frame, parchment colors) and writes PNG pages.
2. **`release/`** — a full-screen page reader with touch-friendly navigation,  
   suitable for a local server or embedding in an Android app.

The main text is **《佛說天地八陽神咒經》** (Taishō-style id **T2897** in the filename), traditionally associated with the Tang translator **義淨**. The repo ships a cleaned working text file and pre-built page images so you can run the reader without regenerating first.

---

## Requirements

- **Python 3**
- **[Pillow](https://pillow.readthedocs.io/)**  
  ```bat
  pip install Pillow
  ```
- **Fonts** in `font/` — family name must match files like  
  `{FONT_FAMILY}-{Weight}.ttf`  
  Default: **Noto Serif TC** (`NotoSerifTC-*.ttf`), already included.  
  Weights used by default: **SemiBold** (body), **Bold** (title), **Regular** (translator / page number).

---

## Project layout

```text
.
├── create_pages.py          # page generator (edit colors / margins here)
├── create_pages.cmd         # Windows helper to run the generator
├── T2897_佛說天地八陽神咒經.txt   # source text (title, translator, body)
├── font/                    # CJK fonts for generation
├── reference/               # sample pages / notes (optional)
└── release/                 # reader + page images
    ├── index.html           # viewer UI + navigation
    ├── server.py / server.cmd
    ├── front/               # front matter  (page_001.jpg …)
    ├── main/                # sutra body    (page_001.png …)  ← generator output
    └── after/               # appendix      (page_001.jpg …)
```

---

## Generate main pages

From the **project root**:

```bat
create_pages.cmd
```

or:

```bat
python create_pages.py
```

- **Input:** `T2897_佛說天地八陽神咒經.txt`  
  - Line 1: title  
  - Line 2: translator / author  
  - Then body (blank lines skipped; other line breaks start a new vertical column)
- **Output:** `release/main/page_001.png`, `page_002.png`, …  
  (old images in that folder are cleared first)

### Tunable options (top of `create_pages.py`)

Edit the **TUNABLE PARAMETERS** block — no need to dig through drawing code:

| Group | Examples |
|--------|-----------|
| **Colors** | `COLOR_BACKGROUND`, `COLOR_TEXT`, `OUTER_BORDER_COLOR`, `INNER_BORDER_ACCENT_COLOR` |
| **Font** | `FONT_FAMILY`, `BODY_FONT_WEIGHT`, `TITLE_FONT_WEIGHT`, … |
| **Page size / scale** | `SCALE`, `PAGE_WIDTH_BASE`, `PAGE_HEIGHT_BASE` |
| **Type size / spacing** | `BODY_FONT_SIZE`, `LINE_SPACING`, `COLUMN_SPACING` |
| **Margins** | `BORDER_MARGIN_*`, `TEXT_MARGIN_*`, `PAGE_NUM_GAP_BELOW_BORDER` |

Default look: warm parchment paper (`#FAF4E8`), dark ink (`#222222`), brown double frame.

Punctuation for vertical layout is normalized (e.g. `,` → `，`, `「」《》` → vertical forms).

---

## Run the reader

### Start the server

```bat
cd release
server.cmd
```

The server always uses the `release/` folder as its document root.

### Open in a browser

Use **HTTP**, not HTTPS:

```text
http://127.0.0.1:8081/
```

(Chrome may force HTTPS on `localhost`; prefer `127.0.0.1` if you see errors about “Bad request version”.)

### Page folders

| Folder | Role | Format |
|--------|------|--------|
| `front/` | Cover / front matter | `.jpg` |
| `main/`  | Sutra body (from generator) | `.png` |
| `after/` | Afterword / appendix | `.jpg` |

Each folder is numbered from `page_001`. Counts are **auto-detected**; you can add or remove pages without editing `index.html`, as long as numbering stays continuous.

### Navigation (summary)

| Control | Behavior |
|---------|----------|
| **Navbar Next / Prev** | Whole book: front → main → after |
| **Home / End / Jump / most gestures** | **Main** section only |
| **Page labels** | Cover / Roman (front), `1 / N` (main), `附 n` (after), `完` (last page) |
| **Top-left tap** | Show / hide menu |

---

## Source text notes

- Working file: `T2897_佛說天地八陽神咒經.txt` (UTF-8).
- Parenthetical notes such as `(捺)` are stripped when generating pages.
- For a public scholarly edition, prefer a canonical CBETA / Taishō source and keep attribution if you redistribute the text widely.

---

## Fonts & license notes

- **Noto Serif TC** fonts are typically under the **SIL Open Font License**; keep license notices if you redistribute the font files.
- This project’s **code** is provided as-is for personal and educational use. Add a formal `LICENSE` file if you need clearer terms for reuse.

---

## Git / backup (quick reminder)

```bat
git add .
git commit -m "Describe your change"
git push
```

- **Commit** = save a snapshot on your PC (with a message).  
- **Push** = upload commits to GitHub.  
- You can commit many times, then push once.

Ignored locally (see `.gitignore`): `__pycache__/`, old `pages/` output, experiment folders, zip/apk packaging files.

---

## Credits

- Scripture: 佛說天地八陽神咒經  
- Layout generator & web reader: this repository  
- Default typeface: Noto Serif TC  

Contributions and feedback are welcome via GitHub issues or pull requests.
