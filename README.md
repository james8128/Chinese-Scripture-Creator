# 佛說天地八陽神咒經 — page generator & reader

Personal project: render the sutra as classical vertical pages, then read them in a simple web/Android viewer.

## Requirements

- Python 3 with [Pillow](https://pillow.readthedocs.io/) (`pip install Pillow`)
- Fonts in `font/` (Noto Serif TC). Weights used by default: SemiBold (body), Bold (title), Regular (translator / page number).

## Generate main pages

From the project root:

```bat
create_pages.cmd
```

or:

```bat
python create_pages.py
```

Output: `release/main/page_001.png`, …  
Layout and colors are tunable at the top of `create_pages.py`.

Source text: `T2897_佛說天地八陽神咒經.txt` (title + translator on the first lines, then body).

## Run the reader (local server)

```bat
cd release
server.cmd
```

Open **http://127.0.0.1:8081/** (use `http://`, not `https://`).

Page folders:

| Folder | Content |
|--------|---------|
| `release/front/` | Front matter (`.jpg`) |
| `release/main/`  | Sutra body (`.png`, from generator) |
| `release/after/` | Appendix / closing (`.jpg`) |

Navigation rules are in `release/index.html` (menu = whole book; gestures / Jump = main only).

## Notes

- This repo is intended as a **private backup** unless you change visibility on GitHub.
- Do not commit secrets; there should be none in this project.
