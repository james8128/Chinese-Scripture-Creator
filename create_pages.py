"""
Render the sutra text as classical Chinese book pages:

  - double black border
  - vertical columns, right → left, top → bottom
  - page 1: large title + small translator column + body
  - later pages: continuous body text
  - page number below the frame:  - N -

Tune layout in the 「TUNABLE PARAMETERS」 section below.
"""

from PIL import Image, ImageDraw, ImageFont
import os
import re

# =============================================================================
# TUNABLE PARAMETERS
# -----------------------------------------------------------------------------
# Edit the numbers in this section. Everything is in *base units*.
# SCALE multiplies them for the final image (SCALE=2 → 1 base unit = 2 pixels).
#
# Quick guide:
#   COLOR_*           → page colors (hex strings, e.g. "#FAF4E8")
#   FONT_FAMILY       → typeface name (prefix of files in FONT_DIR)
#   *_FONT_WEIGHT     → Regular / Bold / Medium / … for each role
#   BORDER_MARGIN_*   → how far the frame sits from the page edges
#                       (larger bottom = shorter frame, more room for page #)
#   TEXT_MARGIN_*     → air between the outer border and the text block
#   PAGE_NUM_*        → page-number size and position under the frame
#   *_FONT_SIZE       → type sizes
#   LINE_SPACING      → vertical gap between characters in a column
#   COLUMN_SPACING    → horizontal gap between columns
# =============================================================================

INPUT_FILE = "T2897_佛說天地八陽神咒經.txt"
# Main sutra images for the Android/web reader (release/index.html loads this folder)
OUTPUT_DIR = os.path.join("release", "main")
OUTPUT_EXT = "png"              # main pages: png (front/after stay jpg in the reader)

# --- Color scheme (edit these hex codes to restyle the page) ---
# Warm parchment paper + dark ink + brown double frame
COLOR_BACKGROUND = "#FAF4E8"              # page paper
COLOR_TEXT = "#222222"                    # body, title, translator, page number
OUTER_BORDER_COLOR = "#7A5C3E"            # outer frame line
INNER_BORDER_ACCENT_COLOR = "#8C7053"     # inner frame line (accent)

# --- Font family (files live under FONT_DIR) ---
# Change FONT_FAMILY to switch typefaces. File names must look like:
#   {FONT_FAMILY}-{Weight}.{ext}   e.g. SourceHanSerifTW-Regular.otf
#                                    NotoSerifTC-Regular.ttf
# Available in ./font/ right now:
#   SourceHanSerifTW  (*.otf)   NotoSerifTC  (*.ttf)
FONT_DIR = "font"               # folder next to this script
FONT_FAMILY = "NotoSerifTC"
# Weights used for each role (must match the suffix in the filename)
BODY_FONT_WEIGHT = "SemiBold"    # main body text
TITLE_FONT_WEIGHT = "Bold"      # large title on page 1
TRANS_FONT_WEIGHT = "Regular"   # translator / author line
PAGE_NUM_FONT_WEIGHT = "Regular"
# Optional: force extension ("otf" / "ttf"). None = auto-detect in FONT_DIR.
FONT_EXT = None

# --- Output resolution ---
SCALE = 2                       # 1 = draft size, 2 = high-res (recommended)
PAGE_WIDTH_BASE = 550           # page width in base units
PAGE_HEIGHT_BASE = 890          # page height in base units

# --- Font sizes (base units) ---
BODY_FONT_SIZE = 28             # main sutra text
TITLE_FONT_SIZE = 42            # title on page 1
TRANS_FONT_SIZE = 20            # translator line on page 1
PAGE_NUM_FONT_SIZE = 22         # "- N -" under the frame

# --- Column rhythm (base units) ---
LINE_SPACING = 42               # vertical step between characters (≈ body size × 1.4)
COLUMN_SPACING = 62             # horizontal step between columns
COLUMNS_PER_PAGE = 6            # max body columns per page (title page uses leftover width)
# Title / translator use their own vertical steps (usually a bit looser than body)
TITLE_LINE_SPACING = 56
TRANS_LINE_SPACING = 28

# --- Border: distance from PAGE EDGE → outer frame (base units) ---
# Larger values push the frame inward. Bottom is usually larger so the
# page number has room outside the frame.
BORDER_MARGIN_TOP = 55
BORDER_MARGIN_BOTTOM = 90       # ↑ larger = shorter frame
BORDER_MARGIN_LEFT = 55
BORDER_MARGIN_RIGHT = 55

# --- Border line thickness / gap (base units) ---
BORDER_OUTER_WIDTH = 3          # outer frame line thickness
BORDER_GAP = 5                  # gap between the two border lines (shows background)
BORDER_INNER_WIDTH = 2          # inner frame line thickness

# --- Text: distance from OUTER BORDER → text (base units) ---
# Measured from the outer frame inward to the text block.
# Left/right are to the *center* of the outermost column.
TEXT_MARGIN_TOP = 55            # border top  → first character
TEXT_MARGIN_BOTTOM = 55         # last character → border bottom  (match top for balance)
TEXT_MARGIN_LEFT = 60           # border left  → leftmost column center
TEXT_MARGIN_RIGHT = 60          # border right → rightmost column center

# --- Page number (drawn OUTSIDE the frame, in the bottom page margin) ---
# Position is measured downward from the bottom of the outer border.
#   0  = flush under the border
#   larger = lower on the page
PAGE_NUM_GAP_BELOW_BORDER = 20

# =============================================================================
# DERIVED VALUES (do not edit — computed from the parameters above)
# =============================================================================

PAGE_WIDTH = PAGE_WIDTH_BASE * SCALE
PAGE_HEIGHT = PAGE_HEIGHT_BASE * SCALE

# Font sizes → pixels
FONT_SIZE = BODY_FONT_SIZE * SCALE
TITLE_FONT_SIZE_PX = TITLE_FONT_SIZE * SCALE
TRANS_FONT_SIZE_PX = TRANS_FONT_SIZE * SCALE
PAGE_NUM_FONT_SIZE_PX = PAGE_NUM_FONT_SIZE * SCALE

# Spacing → pixels
LINE_SPACING_PX = LINE_SPACING * SCALE
COLUMN_SPACING_PX = COLUMN_SPACING * SCALE
TITLE_LINE_SPACING_PX = TITLE_LINE_SPACING * SCALE
TRANS_LINE_SPACING_PX = TRANS_LINE_SPACING * SCALE

# Border margins → pixels
BORDER_MT = BORDER_MARGIN_TOP * SCALE
BORDER_MB = BORDER_MARGIN_BOTTOM * SCALE
BORDER_ML = BORDER_MARGIN_LEFT * SCALE
BORDER_MR = BORDER_MARGIN_RIGHT * SCALE

BORDER_OUTER = max(2, BORDER_OUTER_WIDTH * SCALE)
BORDER_GAP_PX = max(2, BORDER_GAP * SCALE)
BORDER_INNER = max(1, BORDER_INNER_WIDTH * SCALE)

# Page edge → column center (= border margin + text margin)
MARGIN_LEFT = (BORDER_MARGIN_LEFT + TEXT_MARGIN_LEFT) * SCALE
MARGIN_RIGHT = (BORDER_MARGIN_RIGHT + TEXT_MARGIN_RIGHT) * SCALE
TEXT_TOP = (BORDER_MARGIN_TOP + TEXT_MARGIN_TOP) * SCALE

# Page number Y (below outer border)
PAGE_NUM_Y = PAGE_HEIGHT - BORDER_MB + PAGE_NUM_GAP_BELOW_BORDER * SCALE

# Auto: characters per column from top/bottom text margins
_text_max_bottom = PAGE_HEIGHT - BORDER_MB - TEXT_MARGIN_BOTTOM * SCALE
CHARS_PER_COLUMN = max(
    1,
    (_text_max_bottom - TEXT_TOP - FONT_SIZE) // LINE_SPACING_PX + 1,
)

_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_DIR_PATH = (
    FONT_DIR if os.path.isabs(FONT_DIR) else os.path.join(_BASE_DIR, FONT_DIR)
)

# System fallbacks if the chosen family file is missing
SYSTEM_FONT_FALLBACKS = [
    "C:/Windows/Fonts/simsun.ttc",
    "C:/Windows/Fonts/mingliu.ttc",
    "C:/Windows/Fonts/kaiu.ttf",
    "C:/Windows/Fonts/msyh.ttc",
]

os.makedirs(OUTPUT_DIR, exist_ok=True)


def resolve_font_file(family: str, weight: str, ext=None) -> str | None:
    """
    Find {family}-{weight}.{ext} under FONT_DIR_PATH.
    If ext is None, try common extensions (otf, ttf, ttc, otc).
    """
    weight = weight.strip()
    family = family.strip()
    stem = f"{family}-{weight}"
    extensions = [ext.lstrip(".")] if ext else ["otf", "ttf", "ttc", "otc"]
    for e in extensions:
        path = os.path.join(FONT_DIR_PATH, f"{stem}.{e}")
        if os.path.isfile(path):
            return path
    return None


def list_font_family_files(family: str) -> list[str]:
    """List weight files for a family that exist in FONT_DIR_PATH."""
    if not os.path.isdir(FONT_DIR_PATH):
        return []
    prefix = f"{family}-"
    found = []
    for name in sorted(os.listdir(FONT_DIR_PATH)):
        lower = name.lower()
        if not name.startswith(prefix):
            continue
        if lower.endswith((".otf", ".ttf", ".ttc", ".otc")):
            found.append(os.path.join(FONT_DIR_PATH, name))
    return found


def load_font(size: int, weight: str, family: str | None = None) -> ImageFont.FreeTypeFont:
    """
    Load a font by family + weight from FONT_DIR, with fallbacks:
      1) exact {family}-{weight}
      2) other weights of the same family (Regular preferred)
      3) system CJK fonts
    """
    fam = family or FONT_FAMILY
    candidates: list[str] = []

    exact = resolve_font_file(fam, weight, FONT_EXT)
    if exact:
        candidates.append(exact)

    # Prefer common weights if the requested one is missing
    for w in ("Regular", "Medium", "SemiBold", "Bold", "Light"):
        if w.lower() == weight.lower():
            continue
        p = resolve_font_file(fam, w, FONT_EXT)
        if p and p not in candidates:
            candidates.append(p)

    for p in list_font_family_files(fam):
        if p not in candidates:
            candidates.append(p)

    for p in SYSTEM_FONT_FALLBACKS:
        if p not in candidates:
            candidates.append(p)

    last_err = None
    for path in candidates:
        if not os.path.isfile(path):
            continue
        try:
            font = ImageFont.truetype(path, size)
            return font, path
        except OSError as e:
            last_err = e

    available = list_font_family_files(fam)
    hint = (
        f" Found for '{fam}': " + ", ".join(os.path.basename(p) for p in available)
        if available
        else f" No files matching '{fam}-*.{{otf,ttf}}' in '{FONT_DIR_PATH}'."
    )
    raise FileNotFoundError(
        f"Could not load font family={fam!r} weight={weight!r} ({last_err}).{hint}"
    )


font_body, font_body_path = load_font(FONT_SIZE, BODY_FONT_WEIGHT)
font_title, font_title_path = load_font(TITLE_FONT_SIZE_PX, TITLE_FONT_WEIGHT)
font_trans, font_trans_path = load_font(TRANS_FONT_SIZE_PX, TRANS_FONT_WEIGHT)
font_pagenum, font_pagenum_path = load_font(PAGE_NUM_FONT_SIZE_PX, PAGE_NUM_FONT_WEIGHT)

print(f"Font family: {FONT_FAMILY}")
print(f"  body     [{BODY_FONT_WEIGHT}]: {font_body_path}")
print(f"  title    [{TITLE_FONT_WEIGHT}]: {font_title_path}")
print(f"  trans    [{TRANS_FONT_WEIGHT}]: {font_trans_path}")
print(f"  page_num [{PAGE_NUM_FONT_WEIGHT}]: {font_pagenum_path}")
print(
    f"Page {PAGE_WIDTH}×{PAGE_HEIGHT}  body={FONT_SIZE}px  title={TITLE_FONT_SIZE_PX}px  "
    f"chars/col={CHARS_PER_COLUMN}  "
    f"border T/B/L/R={BORDER_MARGIN_TOP}/{BORDER_MARGIN_BOTTOM}/"
    f"{BORDER_MARGIN_LEFT}/{BORDER_MARGIN_RIGHT}  "
    f"text T/B/L/R={TEXT_MARGIN_TOP}/{TEXT_MARGIN_BOTTOM}/"
    f"{TEXT_MARGIN_LEFT}/{TEXT_MARGIN_RIGHT}  "
    f"page_num_gap={PAGE_NUM_GAP_BELOW_BORDER}"
)


# Print-time punctuation normalization for vertical Chinese layout.
# 1) ASCII → fullwidth CJK (fonts may not map these automatically)
# 2) Horizontal brackets → vertical presentation forms
PUNCT_FOR_VERTICAL = str.maketrans({
    ",": "，",   # ASCII comma → ideographic comma
    "「": "﹁",  # U+FE41 vertical left corner bracket
    "」": "﹂",  # U+FE42 vertical right corner bracket
    "《": "︽",  # U+FE3D vertical left double angle bracket
    "》": "︾",  # U+FE3E vertical right double angle bracket
})


def to_vertical_punct(s: str) -> str:
    """Normalize punctuation for vertical printout (comma, 「」《》, …)."""
    return s.translate(PUNCT_FOR_VERTICAL)


def prepare_body_text(s: str) -> str:
    """
    Prepare body text for layout:
      - blank lines are dropped (skipped)
      - non-blank line feeds are kept as '\\n' column breaks
      - spaces/tabs removed; parenthetical notes like (捺) dropped
      - ASCII comma "," → Chinese "，"
      - 「」《》 → vertical forms ﹁﹂︽︾
    """
    s = s.replace("\r\n", "\n").replace("\r", "\n")
    s = re.sub(r"[ \t]+", "", s)
    # Drop parenthetical notes like (捺)
    s = re.sub(r"\([^)]*\)", "", s)
    # Keep only non-blank lines; join with \\n so each source line starts a new column
    lines = [ln.strip() for ln in s.split("\n") if ln.strip()]
    return to_vertical_punct("\n".join(lines))


def extract_column(text: str, cursor: int, max_chars: int) -> tuple[str, int]:
    """
    Take characters for one vertical column from text[cursor:].

    Fills up to max_chars, or stops early at a source line feed ('\\n').
    A line feed ends the column (rest of the column stays empty) and the
    next column begins after it. Newlines are never drawn.
    """
    n = len(text)
    # Skip any leading newlines
    while cursor < n and text[cursor] == "\n":
        cursor += 1
    if cursor >= n:
        return "", cursor

    chars: list[str] = []
    while cursor < n and len(chars) < max_chars:
        ch = text[cursor]
        if ch == "\n":
            # End this column; next column starts after the line break
            cursor += 1
            break
        chars.append(ch)
        cursor += 1
    return "".join(chars), cursor


def parse_front_matter(raw: str):
    """
    Split title, translator, body from:
      【佛說天地八陽神咒經】
      唐三藏法師 義淨 奉詔譯

      如是我聞：
    """
    lines = [ln.strip() for ln in raw.replace("\r\n", "\n").split("\n")]
    title = "佛說天地八陽神咒經"
    translator = "唐三藏法師義淨奉詔譯"
    body_start = 0

    for i, ln in enumerate(lines):
        if not ln:
            continue
        if i < 5 and ("經" in ln or "咒" in ln) and ("佛" in ln or "【" in ln):
            title = re.sub(r"[【】\[\]]", "", ln)
            body_start = i + 1
            continue
        if i < 6 and ("譯" in ln or "法師" in ln):
            translator = re.sub(r"[ \t]+", "", ln)
            body_start = i + 1
            continue
        if i >= body_start and ln and "譯" not in ln:
            body_start = i
            break

    body = prepare_body_text("\n".join(lines[body_start:]))
    return title, translator, body


with open(INPUT_FILE, encoding="utf-8") as f:
    raw = f.read()

TITLE, TRANSLATOR, body_text = parse_front_matter(raw)
_body_char_count = sum(1 for c in body_text if c != "\n")
_body_line_count = body_text.count("\n") + (1 if body_text else 0)
print(f"Title: {TITLE}")
print(f"Translator: {TRANSLATOR}")
print(f"Body chars: {_body_char_count}  source lines: {_body_line_count}")


def draw_double_border(draw: ImageDraw.ImageDraw, width: int, height: int):
    """Double frame inset from page edges (uses BORDER_MARGIN_* / COLOR_*)."""
    mt, mb, ml, mr = BORDER_MT, BORDER_MB, BORDER_ML, BORDER_MR
    o = BORDER_OUTER
    # Outer rectangle: stroke centered on the path; pad by half stroke so full line stays inside
    half_o = o // 2
    x0 = ml + half_o
    y0 = mt + half_o
    x1 = width - mr - half_o - 1
    y1 = height - mb - half_o - 1
    draw.rectangle([x0, y0, x1, y1], outline=OUTER_BORDER_COLOR, width=o)
    # Inner rectangle, further inset by gap + half of each stroke
    pad = o + BORDER_GAP_PX + BORDER_INNER // 2
    draw.rectangle(
        [ml + pad, mt + pad, width - mr - pad - 1, height - mb - pad - 1],
        outline=INNER_BORDER_ACCENT_COLOR,
        width=BORDER_INNER,
    )


def text_size(draw: ImageDraw.ImageDraw, s: str, font) -> tuple[int, int]:
    bbox = draw.textbbox((0, 0), s, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def draw_vertical_column(
    draw, x_center, y_start, chars, font, line_spacing, fill=None
):
    """Draw characters top→bottom; converts 「」《》 to vertical forms if needed."""
    if fill is None:
        fill = COLOR_TEXT
    y = y_start
    for ch in chars:
        ch = to_vertical_punct(ch)
        if ch == "\n":
            continue
        tw, _ = text_size(draw, ch, font)
        draw.text((x_center - tw / 2, y), ch, font=font, fill=fill)
        y += line_spacing
    return y


def draw_page_number(draw, page_no: int):
    """Centered in the bottom margin, below (outside) the double border."""
    label = f"- {page_no} -"
    tw, _ = text_size(draw, label, font_pagenum)
    draw.text(
        ((PAGE_WIDTH - tw) / 2, PAGE_NUM_Y),
        label,
        font=font_pagenum,
        fill=COLOR_TEXT,
    )


def new_page_canvas():
    img = Image.new("RGB", (PAGE_WIDTH, PAGE_HEIGHT), COLOR_BACKGROUND)
    draw = ImageDraw.Draw(img)
    draw_double_border(draw, PAGE_WIDTH, PAGE_HEIGHT)
    return img, draw


def render_title_page(title: str, translator: str, body: str, page_no: int):
    """
    Title page (right → left):
      [body columns …] [translator — one column, near bottom] [large title]
    """
    img, draw = new_page_canvas()
    x = PAGE_WIDTH - MARGIN_RIGHT

    # --- Large title (far right, from the top) ---
    draw_vertical_column(
        draw, x, TEXT_TOP, title, font_title, TITLE_LINE_SPACING_PX
    )
    x -= int(COLUMN_SPACING_PX * 1.0)

    # --- Translator / author: one unbroken vertical column, near bottom ---
    # Aligns with the bottom of the text area inside the frame.
    text_bottom = PAGE_HEIGHT - BORDER_MB - TEXT_MARGIN_BOTTOM * SCALE
    if translator:
        n = len(translator)
        if n <= 1:
            trans_y = text_bottom - TRANS_FONT_SIZE_PX
        else:
            # Last character sits at the bottom of the text area
            trans_y = (
                text_bottom
                - TRANS_FONT_SIZE_PX
                - (n - 1) * TRANS_LINE_SPACING_PX
            )
        trans_y = max(TEXT_TOP, int(trans_y))
        draw_vertical_column(
            draw, x, trans_y, translator, font_trans, TRANS_LINE_SPACING_PX
        )
    x -= int(COLUMN_SPACING_PX * 1.0)

    # --- Body columns for the rest of the width ---
    # Source line feeds start a new column; blank lines already removed.
    left_limit = MARGIN_LEFT
    cursor = 0
    while x >= left_limit and cursor < len(body):
        col, cursor = extract_column(body, cursor, CHARS_PER_COLUMN)
        if not col and cursor >= len(body):
            break
        if col:
            draw_vertical_column(draw, x, TEXT_TOP, col, font_body, LINE_SPACING_PX)
            x -= COLUMN_SPACING_PX
        # If col is empty but cursor advanced (only newlines), keep going without moving x

    draw_page_number(draw, page_no)
    return img, body[cursor:]


def render_body_page(text: str, page_no: int):
    """Body page: columns right→left; each source line feed starts a new column."""
    img, draw = new_page_canvas()
    x = PAGE_WIDTH - MARGIN_RIGHT
    left_limit = MARGIN_LEFT
    cursor = 0
    columns_drawn = 0

    while columns_drawn < COLUMNS_PER_PAGE and cursor < len(text) and x >= left_limit:
        col, cursor = extract_column(text, cursor, CHARS_PER_COLUMN)
        if not col and cursor >= len(text):
            break
        if col:
            draw_vertical_column(draw, x, TEXT_TOP, col, font_body, LINE_SPACING_PX)
            x -= COLUMN_SPACING_PX
            columns_drawn += 1

    draw_page_number(draw, page_no)
    return img, text[cursor:]


# --- GENERATE ---
# Remove previous main pages (jpg leftovers and old png) so the reader sees a clean sequence
for name in os.listdir(OUTPUT_DIR):
    if name.lower().endswith((".jpg", ".png", ".jpeg")):
        os.remove(os.path.join(OUTPUT_DIR, name))

remaining = body_text
page_no = 1


def save_page(img, page_no: int) -> str:
    out = os.path.join(OUTPUT_DIR, f"page_{page_no:03d}.{OUTPUT_EXT}")
    if OUTPUT_EXT.lower() == "png":
        img.save(out, format="PNG", optimize=True)
    else:
        img.save(out, quality=95)
    return out


img, remaining = render_title_page(TITLE, TRANSLATOR, remaining, page_no)
print(f"Wrote {save_page(img, page_no)}")
page_no += 1

while remaining:
    img, remaining = render_body_page(remaining, page_no)
    print(f"Wrote {save_page(img, page_no)}")
    page_no += 1

print(f"Generated {page_no - 1} pages ({OUTPUT_EXT}) in '{OUTPUT_DIR}/'")
