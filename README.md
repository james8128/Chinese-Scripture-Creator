# Chinese Scripture Creator

**佛說天地八陽神咒經** — generate classical vertical book pages from plain text, then read them in a simple web or **Android** viewer.

**GitHub:** [james8128/Chinese-Scripture-Creator](https://github.com/james8128/Chinese-Scripture-Creator)

---

## What this project is

This toolkit helps anyone who wants to **typeset and customize their own reading edition** of a Chinese scripture — fonts, colors, margins, and page images — then view them on a phone or in a browser.

It is **not** a critical scholarly edition of the canon. There are **minor textual varieties** of 《佛說天地八陽神咒經》 in circulation. For the standard text, variants, and full bibliographic detail, please always refer to **CBETA** (see credit below). This project is meant to help you **produce a personal, well-laid-out copy** if you wish.

The pipeline has two main parts:

1. **`create_pages.py`** — lays out the sutra like a traditional book  
   (vertical columns, right → left, double frame, parchment colors) and writes PNG pages.  
   Swap in your preferred text, tune the parameters, and regenerate.
2. **`release/`** — a full-screen HTML reader (pages + `index.html`) that can run:
   - inside an **Android WebView app** (recommended path for daily reading), or  
   - via a small **local HTTP server** on a PC for preview.

### Scripture text source (please credit)

The working body text shipped in this repository is based on the CBETA Online edition of the Taishō Tripitaka text **T2897** 《佛說天地八陽神咒經》 (translator traditionally given as Tang **義淨**):

- **CBETA Online:** [https://cbetaonline.dila.edu.tw/zh/T2897](https://cbetaonline.dila.edu.tw/zh/T2897)

**Full credit:** text content derives from the Chinese Buddhist Electronic Text Association (**CBETA**) and the underlying Taishō canon edition as presented on CBETA Online (Dharma Drum Institute of Liberal Arts / related CBETA partners).  
This project is an independent layout and reader tool; it is **not** affiliated with CBETA. Any formatting or punctuation normalization in `T2897_佛說天地八陽神咒經.txt` is for page generation convenience only — **canonical wording and variant readings should be checked against CBETA T2897**.

If you redistribute pages or a modified text, please retain a clear pointer to CBETA T2897 and respect CBETA’s terms of use for the source text.

### Front / after page images (please credit)

Page images **outside the main session** (`release/front/` and `release/after/`, i.e. not generated from the text file by `create_pages.py`) were downloaded from **善書圖書館** (Tao Library):

- **Source page:** [https://simple.taolibrary.com/category/category50/c50074.htm](https://simple.taolibrary.com/category/category50/c50074.htm)  
- **Site:** [taolibrary.com](https://simple.taolibrary.com/) (善書圖書館)

**Main** body pages (`release/main/`) are produced by this project’s generator from the CBETA-based text file.  
This project is **not** affiliated with 善書圖書館 / taolibrary.com. If you redistribute those front/after images, please credit the library and respect their terms of use.

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
├── learn-by-listening/      # optional Cantonese TTS audio (not in APK/HTML)
│   ├── T2897_cantonese-reading.zh-HK.ogg
│   └── T2897_google-tts-source.zh-HK.txt
├── font/                    # CJK fonts for generation
├── reference/               # sample pages / notes (optional)
├── apk-sample-output/       # sample Android APK (unsigned)
│   └── 八陽神咒經.apk
└── release/                 # reader package (HTML + page images)
    ├── index.html           # viewer UI + navigation
    ├── server.py / server.cmd   # PC preview only (not needed for APK)
    ├── front/               # front matter  (page_001.jpg …)
    ├── main/                # sutra body    (page_001.png …)  ← generator output
    └── after/               # appendix      (page_001.jpg …)
```

---

## Learn by listening (optional Cantonese audio)

Folder: **`learn-by-listening/`**

This optional package is for anyone who wants to **hear** the sutra — learners, elders, people with low vision, or anyone who prefers listening while reading the page images. It is meant to **lower barriers** so more people can study and understand freely; it is **not** wired into the APK or `index.html`. Open the audio file in any player you like (phone, PC, browser, etc.).

| File | Role |
|------|------|
| [`T2897_cantonese-reading.zh-HK.ogg`](learn-by-listening/T2897_cantonese-reading.zh-HK.ogg) | Full reading voice (Cantonese, Google TTS). Play separately; **not** controlled by the app or web viewer. |
| [`T2897_google-tts-source.zh-HK.txt`](learn-by-listening/T2897_google-tts-source.zh-HK.txt) | Text prepared for **Google TTS Cantonese (zh-HK)** generation. Based on the root `T2897_佛說天地八陽神咒經.txt`, with **manual character-level adjustments** so the engine reads more naturally. Use this file if you regenerate or adapt the audio. |

### How this text differs from the page-generation source

- **Root** `T2897_佛說天地八陽神咒經.txt` — working text for **`create_pages.py`** / printed pages. Prefer CBETA T2897 for canonical wording.
- **TTS source** — practical speech script only (pronunciation-friendly edits). It is **not** a second critical edition of the canon.

### Supplementary Bodhisattva names (voice version only)

In the spoken / TTS script, **7 of the 8 Bodhisattvas** include short bilingual notes of the form  
`(Bhadrapāla，賢護)` (Sanskrit romanization + Chinese).

These are **personal study aids** only — extra reference so listeners can link traditional names with common Sanskrit / Chinese labels. They are **not** an academic amendment of the Taishō / CBETA text, and they are **not** part of the generated page images unless you deliberately add them elsewhere.

### What is *not* included

- The APK and HTML reader **do not** embed or play this audio.
- You do **not** need the audio folder to build pages or to use the reader.

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

## Android app (APK)

The **`release/`** package — **excluding** the PC-only helper files `server.py` / `server.cmd` — is ready to wrap as an Android app with a **third-party free online APK / WebView builder** (point the builder at `index.html` and include `front/`, `main/`, `after/`).

| Item | Detail |
|------|--------|
| **What to package** | `release/index.html` + `front/` + `main/` + `after/` |
| **Not required for APK** | `server.py`, `server.cmd` (those are for PC browser preview only) |
| **Sample APK** | [`apk-sample-output/八陽神咒經.apk`](apk-sample-output/八陽神咒經.apk) |
| **App display name** | **天地八陽經** — shorter than 佛說天地八陽神咒經 so it fits better on the Android home screen / app list |
| **Signing** | The sample APK is **unsigned**. For sideloading or store release you should sign it with your own key (or use a builder that signs for you). |

### Navigation status

| Platform | Status |
|----------|--------|
| **Android** (sample APK / WebView) | Touch gestures + menu; **top-right tap = Back / undo**; top-left = menu. Desktop side rail / hints / dashboard are hidden and do not intercept taps. |
| **PC browser** (`server.py`) | Desktop chrome (side buttons, progress dash, hints) when pointer is fine + wide enough. Session-scoped page turns; center / Home = main first page; **Back** = `B` / **top-right** click (history, unlimited). |

---

## Run the reader on a PC (preview)

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

Remember: **Android navigation is the primary, finished path**; PC browser navigation is still being worked on.

### Page folders

| Folder | Role | Format |
|--------|------|--------|
| `front/` | Cover / front matter | `.jpg` |
| `main/`  | Sutra body (from generator) | `.png` |
| `after/` | Afterword / appendix | `.jpg` |

Each folder is numbered from `page_001`. Counts are **auto-detected**; you can add or remove pages without editing `index.html`, as long as numbering stays continuous.

### Navigation map (Android / intended behavior)

| Control | Behavior |
|---------|----------|
| **Navbar Next / Prev** | Whole book: front → main → after |
| **Home / End / Jump / most gestures** | **Main** section only |
| **Page labels** | Cover / Roman (front), `1 / N` (main), `附 n` (after), `完` (last page) |
| **Top-left tap** | Show / hide menu |
| **Top-right tap** | Back / undo (page history) |

---

## Source text notes

- Working file: `T2897_佛說天地八陽神咒經.txt` (UTF-8), based on **[CBETA Online T2897](https://cbetaonline.dila.edu.tw/zh/T2897)**.
- **Variants:** different printings and traditions of 《佛說天地八陽神咒經》 can differ slightly (wording, punctuation, chaptering). This repo’s file is one practical working copy only. For authoritative text and notes on variants, consult **CBETA T2897**, not this generator alone.
- **Customization:** replace or edit the `.txt` file with your preferred wording, then re-run `create_pages.py` to build your own page set — that is the main intent of the project.
- **Optional TTS script:** `learn-by-listening/T2897_google-tts-source.zh-HK.txt` is derived from the working file for Cantonese speech only (see [Learn by listening](#learn-by-listening-optional-cantonese-audio)).

---

## Fonts & license notes

- **Noto Serif TC** fonts are typically under the **SIL Open Font License**; keep license notices if you redistribute the font files.
- This project’s **code** is provided as-is for personal and educational use. Add a formal `LICENSE` file if you need clearer terms for reuse.
- The sample APK is unsigned and provided as a convenience demo; use at your own risk when installing on a device.

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

Ignored locally (see `.gitignore`): `__pycache__/`, old `pages/` output, experiment folders, zip packaging, and other APKs **except** the sample under `apk-sample-output/`.

---

## Credits

- **Scripture text:** 《佛說天地八陽神咒經》 **T2897**, via **[CBETA Online](https://cbetaonline.dila.edu.tw/zh/T2897)** (Chinese Buddhist Electronic Text Association). Please credit CBETA when referring to or redistributing the textual content.
- **Front / after page images:** downloaded from **[善書圖書館 (Tao Library)](https://simple.taolibrary.com/category/category50/c50074.htm)** on taolibrary.com — not generated by `create_pages.py`. Please credit 善書圖書館 when redistributing those images.
- **Main page images:** generated by this repository from the working text file.
- **Optional Cantonese reading audio:** Google TTS–based OGG in `learn-by-listening/` (open separately; not part of the APK/HTML controls). Supplementary Bodhisattva name glosses in that track are for personal reference only.
- **Layout generator & web reader:** this repository (Chinese Scripture Creator)
- **Default typeface:** Noto Serif TC  

Contributions and feedback are welcome via GitHub issues or pull requests.
