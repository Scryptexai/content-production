"""
brand.py — ODDCHAPTER identity core.

Single source of truth for the approved, refined LINK monogram and the lockup.
Every asset in Phase 3-6 imports from here, so geometry can never drift between
the logo, the avatar, the banner, the thumbnails and the motion layers.

Approved:   concept 01 LINK  (owner, 2026-11-06)
Refined:    centre distance 44 u  (owner approved 2026-11-06)
"""
from pathlib import Path
import math
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from oclib import (INK, IVORY, ORANGE, SAGE, ring, c_ring, rect, svg_doc, text,
                   f, wordmark_path)

ROOT = HERE.parent

# ------------------------------------------------------------------ tokens
COLORS = {"ink": INK, "ivory": IVORY, "orange": ORANGE, "sage": SAGE}
INK_HEX, IVORY_HEX, ORANGE_HEX, SAGE_HEX = INK, IVORY, ORANGE, SAGE

# ------------------------------------------------------------------ geometry
OUTER, COUNTER, MOUTH, DIST = 27, 14, 84, 44
CX1, CX2, CY = 50 - DIST / 2, 50 + DIST / 2, 50      # 28, 72, 50
STROKE = OUTER - COUNTER                              # 13
BX0, BY0 = CX1 - OUTER, CY - OUTER                    # 1, 23
BX1, BY1 = CX2 + OUTER, CY + OUTER                    # 99, 77
MW, MH = BX1 - BX0, BY1 - BY0                         # 98 x 54

#: O ring alone (closed annulus, even-odd)
O_PATH = ring(CX1, CY, OUTER, COUNTER)
#: C alone (annulus with an 84 deg mouth facing right)
C_PATH = c_ring(CX2, CY, OUTER, COUNTER, gap=MOUTH)
#: ink bounding box — the geometric box (98 x 54) is wider than the drawn ink on the
#: right, because the C mouth carves that corner away. Centre on the ink, not the box.
_COS_HALF = math.cos(math.radians(MOUTH / 2))
IX0, IX1 = BX0, CX2 + OUTER * _COS_HALF          # 1 .. 92.065
IY0, IY1 = CY - OUTER, CY + OUTER                # 23 .. 77
IW, IH = IX1 - IX0, IY1 - IY0                    # 91.065 x 54

#: the monogram as one shape; the junction lens comes from even-odd
MONO_PATH = f"{O_PATH} {C_PATH}"

# ------------------------------------------------------------------ type
CAP_RATIO = 0.7          # Space Grotesk cap height / em
MARK_TO_CAP = 1.5        # monogram height / wordmark cap height
GAP_TO_CAP = 0.62        # monogram-to-wordmark gap / cap height
WM_TRACK = 0.02          # wordmark tracking, em
TAGLINE = "REAL STORIES. UNEXPECTED CHAPTERS."


def wordmark(cap, color, x, cap_top, tracking=WM_TRACK, weight=700):
    """ODDCHAPTER as outlines. Returns (svg, width)."""
    size = cap / CAP_RATIO
    d, w = wordmark_path("ODDCHAPTER", "grotesk", weight, size, tracking)
    return (f'<g transform="translate({f(x)} {f(cap_top + cap)})"><path d="{d}" fill="{color}"/></g>', w)


def tagline_outline(size, color, x, baseline, tracking=0.17, weight=600, ids=False):
    """Tagline as outlines. Returns (svg, width). No live text in any logo file."""
    d, w = wordmark_path(TAGLINE, "inter", weight, size, tracking)
    i = ' id="layer-tagline"' if ids else ""
    return (f'<g{i} transform="translate({f(x)} {f(baseline)})"><path d="{d}" fill="{color}"/></g>', w)


def monogram(x, y, scale, color, ids=False, layers=False):
    """Place the monogram with its bbox top-left at (x, y)."""
    tx, ty = x - BX0 * scale, y - BY0 * scale
    if layers:
        o = f'<path id="layer-o" d="{O_PATH}" fill="{color}" fill-rule="evenodd"/>'
        c = f'<path id="layer-c" d="{C_PATH}" fill="{color}"/>'
        return f'<g id="monogram" transform="translate({f(tx)} {f(ty)}) scale({f(scale,6)})">{o}{c}</g>'
    i = ' id="monogram"' if ids else ""
    return (f'<g{i} transform="translate({f(tx)} {f(ty)}) scale({f(scale,6)})">'
            f'<path d="{MONO_PATH}" fill="{color}" fill-rule="evenodd"/></g>')


def monogram_centered(cx, cy, fit_w, color, ids=False):
    """Monogram scaled so its *ink* is `fit_w` wide, centred optically on (cx, cy)."""
    sc = fit_w / IW
    tx = cx - (IX0 + IX1) / 2 * sc
    ty = cy - (IY0 + IY1) / 2 * sc
    i = ' id="monogram"' if ids else ""
    return (f'<g{i} transform="translate({f(tx)} {f(ty)}) scale({f(sc,6)})">'
            f'<path d="{MONO_PATH}" fill="{color}" fill-rule="evenodd"/></g>')


def monogram_svg(bg=None, fg=INK, clear=1.0, title="ODDCHAPTER — OC monogram"):
    """Standalone monogram with `clear` x stroke of clear space baked into the canvas."""
    m = STROKE * clear
    cw, ch = MW + 2 * m, MH + 2 * m
    body = monogram(m, m, 1.0, fg, ids=True)
    return svg_doc(round(cw, 3), round(ch, 3), body, bg=bg, title=title), cw, ch


def lockup(colors=None, cap=36.0, tagline=False, x=0.0, y=0.0, ids=False):
    """Primary horizontal lockup. Returns (svg, width, height).

    colours: dict(word, accent). Nothing else may be coloured.
    """
    c = colors or {"word": INK, "accent": ORANGE}
    mark_h = cap * MARK_TO_CAP
    ms = mark_h / MH
    gap = cap * GAP_TO_CAP
    mark_w = MW * ms

    x_wm = x + mark_w + gap
    wsvg, wwidth = wordmark(cap, c["word"], x_wm, y)
    right = x_wm + wwidth
    bottom = y + mark_h

    extra = ""
    if tagline:
        rule_y = y + cap + cap * 0.52
        rt = max(1.6, cap * 0.035)
        extra += (f'<rect id="layer-rule" x="{f(x_wm)}" y="{f(rule_y)}" width="{f(wwidth)}" '
                  f'height="{f(rt)}" fill="{c["accent"]}"/>')
        tsize = cap * 0.235
        ty = rule_y + cap * 0.40
        tsvg, twidth = tagline_outline(tsize, c["word"], x_wm, ty, ids=ids)
        extra += tsvg
        right = max(right, x_wm + twidth)
        bottom = ty + cap * 0.10

    body = f'{monogram(x, y, ms, c["word"], ids=ids)}{wsvg}{extra}'
    return body, right - x, bottom - y


def lockup_svg(bg=None, colors=None, cap=36.0, tagline=False, pad=0.30,
               title="ODDCHAPTER — primary horizontal logo"):
    body, w, h = lockup(colors=colors, cap=cap, tagline=tagline)
    p = cap * pad
    doc = (f'<g transform="translate({f(p)} {f(p)})">{body}</g>')
    return svg_doc(round(w + 2 * p, 2), round(h + 2 * p, 2), doc, bg=bg, title=title), w + 2 * p, h + 2 * p


def svg_inner(doc):
    """Strip the outer <svg> wrapper so a document can be nested."""
    return doc.split("<svg", 1)[1].split(">", 1)[1].rsplit("</svg>", 1)[0]
