"""
oclib.py — ODDCHAPTER visual identity geometry library.

All marks are generated as exact vector geometry (arcs, not traced bitmaps).
Coordinates are authored on a 0..100 unit design grid per monogram.
"""
import math
from pathlib import Path

# ---------------------------------------------------------------- brand tokens
INK    = "#17191D"
IVORY  = "#F4F0E8"
ORANGE = "#F26A3D"
SAGE   = "#A7B0A1"

TOKENS = {"ink": INK, "ivory": IVORY, "orange": ORANGE, "sage": SAGE}

# ---------------------------------------------------------------- font access
BUILD = Path(__file__).resolve().parent.parent / ".build" / "fonts"

FONTS = {
    ("grotesk", 300): "space-grotesk-latin-300-normal.ttf",
    ("grotesk", 400): "space-grotesk-latin-400-normal.ttf",
    ("grotesk", 500): "space-grotesk-latin-500-normal.ttf",
    ("grotesk", 600): "space-grotesk-latin-600-normal.ttf",
    ("grotesk", 700): "space-grotesk-latin-700-normal.ttf",
    ("inter", 400):   "inter-latin-400-normal.ttf",
    ("inter", 500):   "inter-latin-500-normal.ttf",
    ("inter", 600):   "inter-latin-600-normal.ttf",
    ("inter", 700):   "inter-latin-700-normal.ttf",
}


def font_path(family, weight):
    return BUILD / FONTS[(family, weight)]


# ---------------------------------------------------------------- number utils
def f(v, nd=3):
    s = f"{v:.{nd}f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def pt(cx, cy, r, a):
    """Point on a circle. Angle in degrees, screen coordinates (y down)."""
    a = math.radians(a)
    return (cx + r * math.cos(a), cy + r * math.sin(a))


# ---------------------------------------------------------------- primitives
def ring(cx, cy, R, r, evenodd=True):
    """Annulus as a single path (outer circle + counter). Requires evenodd."""
    return (
        f"M {f(cx + R)} {f(cy)} "
        f"A {f(R)} {f(R)} 0 1 1 {f(cx - R)} {f(cy)} "
        f"A {f(R)} {f(R)} 0 1 1 {f(cx + R)} {f(cy)} Z "
        f"M {f(cx + r)} {f(cy)} "
        f"A {f(r)} {f(r)} 0 1 0 {f(cx - r)} {f(cy)} "
        f"A {f(r)} {f(r)} 0 1 0 {f(cx + r)} {f(cy)} Z"
    )


def arc_ring(cx, cy, R, r, a0, a1):
    """Annular sector sweeping a0 -> a1 (degrees, increasing = clockwise on screen)."""
    a1c = a1 if a1 >= a0 else a1 + 360
    large = 1 if (a1c - a0) > 180 else 0
    p0, p1 = pt(cx, cy, R, a0), pt(cx, cy, R, a1c)
    p2, p3 = pt(cx, cy, r, a1c), pt(cx, cy, r, a0)
    return (
        f"M {f(p0[0])} {f(p0[1])} "
        f"A {f(R)} {f(R)} 0 {large} 1 {f(p1[0])} {f(p1[1])} "
        f"L {f(p2[0])} {f(p2[1])} "
        f"A {f(r)} {f(r)} 0 {large} 0 {f(p3[0])} {f(p3[1])} Z"
    )


def c_ring(cx, cy, R, r, gap=84.0, rotate=0.0):
    """Letter C: annulus with an angular gap centred on the right (0 deg)."""
    return arc_ring(cx, cy, R, r, gap / 2 + rotate, 360 - gap / 2 + rotate)


def circle(cx, cy, r):
    return (
        f"M {f(cx + r)} {f(cy)} A {f(r)} {f(r)} 0 1 1 {f(cx - r)} {f(cy)} "
        f"A {f(r)} {f(r)} 0 1 1 {f(cx + r)} {f(cy)} Z"
    )


def rect(x, y, w, h, rx=0):
    if rx <= 0:
        return f"M {f(x)} {f(y)} H {f(x+w)} V {f(y+h)} H {f(x)} Z"
    return (
        f"M {f(x+rx)} {f(y)} H {f(x+w-rx)} A {f(rx)} {f(rx)} 0 0 1 {f(x+w)} {f(y+rx)} "
        f"V {f(y+h-rx)} A {f(rx)} {f(rx)} 0 0 1 {f(x+w-rx)} {f(y+h)} H {f(x+rx)} "
        f"A {f(rx)} {f(rx)} 0 0 1 {f(x)} {f(y+h-rx)} V {f(y+rx)} "
        f"A {f(rx)} {f(rx)} 0 0 1 {f(x+rx)} {f(y)} Z"
    )


# ---------------------------------------------------------------- monogram specs
# Each concept is a list of parts: dict(d=..., fill=color-key, rule="evenodd"|None)
# authored inside a 0..100 box; `bbox` is the tight drawing bbox.

def concept_link():
    """01 LINK — two equal rings; the crossing lens is knocked out (even-odd)."""
    d = ring(29, 50, 27, 14) + " " + c_ring(71, 50, 27, 14, gap=84)
    parts = [dict(d=d, fill="ink", rule="evenodd")]
    return dict(name="LINK", parts=parts, bbox=(2, 23, 98, 77), centres=[(29, 50), (71, 50)],
                logic="Interlock / transparent junction",
                note="Single colour by construction.",
                mono=parts)


def concept_stack():
    """02 STACK — O over C, joined by a Signal Orange editorial rule."""
    parts = [
        dict(d=ring(50, 23, 22, 10), fill="ink", rule="evenodd"),
        dict(d=c_ring(50, 77, 22, 10, gap=76), fill="ink", rule=None),
        dict(d=rect(30, 45.5, 40, 9, rx=4.5), fill="orange", rule=None),
    ]
    mono = [
        dict(d=ring(50, 23, 22, 10), fill="ink", rule="evenodd"),
        dict(d=c_ring(50, 77, 22, 10, gap=76), fill="ink", rule=None),
        dict(d=rect(30, 45.5, 40, 9, rx=4.5), fill="ink", rule=None),
    ]
    return dict(name="STACK", parts=parts, bbox=(28, 1, 72, 99), centres=[(50, 23), (50, 77)],
                logic="Stacked ligature / colour bridge",
                note="Orange rule is the only accent.",
                mono=mono)


def concept_cascade():
    """03 CASCADE — shallow diagonal junction; the accent rides the open letter."""
    parts = [
        dict(d=ring(29, 61, 27, 14), fill="orange", rule="evenodd"),
        dict(d=c_ring(72, 35, 27, 14, gap=84), fill="ink", rule=None),
    ]
    mono = [
        dict(d=ring(29, 61, 27, 14), fill="ink", rule="evenodd"),
        dict(d=c_ring(72, 35, 27, 14, gap=84), fill="ink", rule=None),
    ]
    return dict(name="CASCADE", parts=parts, bbox=(2, 8, 99, 88), centres=[(29, 61), (72, 35)],
                logic="Offset axis / accent on the open letter",
                note="Orange sits on the C only.",
                mono=mono)


CONCEPTS = [
    ("01", "link", concept_link()),
    ("02", "stack", concept_stack()),
    ("03", "cascade", concept_cascade()),
]


# ---------------------------------------------------------------- svg emission
def mark_svg_body(concept, palette, mono=False, extra_attrs=""):
    """Return the <path> elements for a concept in its own 0..100 space."""
    parts = concept["mono"] if mono else concept["parts"]
    out = []
    for p in parts:
        fill = palette.get(p["fill"], p["fill"]) if not mono else palette.get("ink", INK)
        rule = f' fill-rule="{p["rule"]}"' if p.get("rule") else ""
        out.append(f'<path d="{p["d"]}" fill="{fill}"{rule}{extra_attrs}/>')
    return "\n    ".join(out)


def place(concept, x, y, size, viewbox=100):
    """Transform that fits a concept's bbox into a `size` box at (x, y)."""
    bx0, by0, bx1, by1 = concept["bbox"]
    w, h = bx1 - bx0, by1 - by0
    s = size / max(w, h)
    tx = x + (size - w * s) / 2 - bx0 * s
    ty = y + (size - h * s) / 2 - by0 * s
    return f"translate({f(tx)} {f(ty)}) scale({f(s, 6)})", s


def svg_doc(w, h, body, bg=None, title="", extra_defs=""):
    bgrect = f'<rect width="{f(w)}" height="{f(h)}" fill="{bg}"/>' if bg else ""
    return (
        f'<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{f(w)}" height="{f(h)}" '
        f'viewBox="0 0 {f(w)} {f(h)}" role="img" aria-label="{title}">\n'
        f'<title>{title}</title>\n'
        f'<defs>{extra_defs}</defs>\n'
        f'{bgrect}\n{body}\n</svg>\n'
    )


def text(x, y, s, font="inter", weight=400, size=16, fill=INK, tracking=0,
         anchor="start", opacity=None, caps=False):
    fam = "Space Grotesk" if font == "grotesk" else "Inter"
    ls = f' letter-spacing="{f(tracking)}"' if tracking else ""
    op = f' opacity="{opacity}"' if opacity is not None else ""
    s = s.upper() if caps else s
    esc = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return (f'<text x="{f(x)}" y="{f(y)}" font-family="{fam}" font-weight="{weight}" '
            f'font-size="{f(size)}"{ls} fill="{fill}" text-anchor="{anchor}"{op}>{esc}</text>')


def rule(x, y, w, h=3, fill=ORANGE):
    return f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" fill="{fill}"/>'


# ---------------------------------------------------------------- wordmark
def wordmark_path(text_str, family="grotesk", weight=700, size=100, tracking=0.0,
                  rotate=0):
    """Live text -> exact vector outlines (glyph paths) at `size` cap units."""
    from fontTools.ttLib import TTFont
    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.pens.transformPen import TransformPen

    font = TTFont(str(font_path(family, weight)))
    upm = font["head"].unitsPerEm
    cmap = font.getBestCmap()
    gs = font.getGlyphSet()
    scale = size / upm
    x = 0.0
    d = []
    for ch in text_str:
        gname = cmap.get(ord(ch))
        if gname is None:
            raise SystemExit(f"glyph missing: {ch!r} in {family} {weight}")
        glyph = gs[gname]
        pen = SVGPathPen(gs)
        glyph.draw(TransformPen(pen, (scale, 0, 0, -scale, x, 0)))
        d.append(pen.getCommands())
        x += glyph.width * scale + tracking * size
    return " ".join(d), x - (tracking * size if text_str else 0)
