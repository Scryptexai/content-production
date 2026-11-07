"""
build_print.py — Phase 8: print and physical artwork.

Everything here is authored in millimetres (viewBox in mm, 1 unit = 1 mm), so a printer gets
real measurements rather than pixels. Bleed is baked into the canvas; trim is documented in
PRINT_SPEC.md and never drawn into the artwork.

  07_PRINT/one_colour/LOGO_100K.svg              single-ink lockup, 100 % K
  07_PRINT/one_colour/MONOGRAM_100K.svg          single-ink monogram, 100 % K
  07_PRINT/stationery/LETTERHEAD_A4_210x297.svg
  07_PRINT/stationery/BUSINESS_CARD_FRONT_91x61.svg   (85 x 55 trim + 3 mm bleed)
  07_PRINT/stationery/BUSINESS_CARD_BACK_91x61.svg
  07_PRINT/poster/POSTER_A2_420x594.svg          (420 x 594 trim + 3 mm bleed)
  07_PRINT/merch/STICKER_DIECUT_75mm.svg         (75 mm circle, 3 mm bleed, die line on a layer)
  07_PRINT/merch/TEE_ART_A3_297x420.svg          (A3 print area, chest placement)
  07_PRINT/PRINT_SCALE_TEST.svg                  minimum-size proof sheet
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import brand
from brand import INK, IVORY, ORANGE, SAGE, MW, MH, IX0, IX1, monogram_centered, lockup, f

ROOT = brand.ROOT
K100 = "#000000"

MM_PER_PT = 0.352778


def pt(p):
    """Points to millimetres — type sizes in this file are quoted in points."""
    return p * MM_PER_PT


def print_doc(w, h, body, title):
    return (f'<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}mm" height="{h}mm" '
            f'viewBox="0 0 {w} {h}" role="img" aria-label="{title}">\n'
            f'<title>{title}</title>\n{body}\n</svg>\n')


def txt(x, y, s, size_mm, color, family="inter", weight=400, tracking=0.0, anchor="start",
        caps=False, opacity=None):
    s = s.upper() if caps else s
    ls = f' letter-spacing="{f(tracking * size_mm, 4)}"' if tracking else ""
    op = f' opacity="{opacity}"' if opacity is not None else ""
    return (f'<text x="{f(x)}" y="{f(y)}" font-family="{family}" font-weight="{weight}" '
            f'font-size="{f(size_mm, 4)}"{ls} fill="{color}" text-anchor="{anchor}"{op}>{s}</text>')


def outline(s, x, y, size, color, family="grotesk", weight=700, tracking=0.0):
    """Display type as outlines — a poster is artwork, not a document."""
    from oclib import wordmark_path
    d, w = wordmark_path(s, family, weight, size, tracking)
    return (f'<g transform="translate({f(x)} {f(y)})"><path d="{d}" fill="{color}"/></g>', w)


def fit_size(strings, max_w, family="grotesk", weight=700, tracking=0.0):
    """Largest size at which every string fits `max_w` millimetres."""
    from oclib import wordmark_path
    widest = 0.0
    for st in strings:
        _, w = wordmark_path(st, family, weight, 100, tracking)
        widest = max(widest, w)
    return max_w / (widest / 100)


def lockup_mm(width_mm, colors, tagline=False):
    """Lockup scaled to a physical width in millimetres. Returns (svg, w, h)."""
    body, w, h = lockup(colors=colors, tagline=tagline)
    sc = width_mm / w
    return body, sc, width_mm, h * sc


def write(path, content):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content)
    print("wrote", path)


# ------------------------------------------------------------------ one colour
def one_colour_lockup():
    """140 mm wide — the monogram lands at 10.2 mm, comfortably over the 8 mm print floor."""
    body, w, h = lockup(colors={"word": K100, "accent": K100}, tagline=False)
    sc = 140.0 / w
    W, H = w * sc, h * sc
    pad = 5.0
    return print_doc(f(round(W + 2 * pad, 2)), f(round(H + 2 * pad, 2)),
                     f'<g transform="translate({pad} {pad}) scale({f(sc, 8)})">{body}</g>',
                     "ODDCHAPTER — one colour lockup, 100 K")


def one_colour_monogram():
    """30 mm wide monogram (well over the 8 mm floor) with one stroke of clear space."""
    target_w = 30.0
    pad = 4.0
    W, H = target_w + 2 * pad, target_w * (MH / MW) + 2 * pad
    return print_doc(f(round(W, 2)), f(round(H, 2)),
                     monogram_centered(W / 2, H / 2, target_w, K100),
                     "ODDCHAPTER — one colour monogram, 100 K")


# ------------------------------------------------------------------ letterhead
def letterhead():
    W, H = 210, 297
    g = [f'<rect width="{W}" height="{H}" fill="{IVORY}"/>']
    body, sc, lw, lh = lockup_mm(60, {"word": INK, "accent": ORANGE})
    g.append(f'<g transform="translate(20 18) scale({f(sc,6)})">{body}</g>')
    # footer
    g.append(f'<rect x="20" y="258" width="170" height="0.25" fill="{SAGE}"/>')
    g.append(txt(20, 265, "REAL STORIES. UNEXPECTED CHAPTERS.", pt(7.5), INK,
                 weight=600, tracking=0.16, caps=True, opacity=0.8))
    g.append(txt(190, 265, "DOKUMENTER · INDONESIA", pt(7.5), INK, weight=500,
                 tracking=0.16, caps=True, anchor="end", opacity=0.55))
    return print_doc(W, H, "\n".join(g), "ODDCHAPTER — letterhead A4")


# ------------------------------------------------------------------ business card
def card_front():
    W, H = 91, 61
    g = [f'<rect width="{W}" height="{H}" fill="{INK}"/>']
    body, sc, lw, lh = lockup_mm(66, {"word": IVORY, "accent": ORANGE})
    g.append(f'<g transform="translate({f((W - lw) / 2)} {f((H - lh) / 2)}) scale({f(sc,6)})">{body}</g>')
    return print_doc(W, H, "\n".join(g), "ODDCHAPTER — business card front, 85 x 55 + 3 mm bleed")


def card_back():
    W, H = 91, 61
    g = [f'<rect width="{W}" height="{H}" fill="{IVORY}"/>']
    g.append(monogram_centered(8 + 5.5, 8 + 5.5, 11, INK))
    g.append(f'<rect x="8" y="42.5" width="18" height="0.6" fill="{ORANGE}"/>')
    g.append(txt(8, 49.4, "REAL STORIES. UNEXPECTED CHAPTERS.", pt(6.2), INK,
                 weight=600, tracking=0.17, caps=True))
    g.append(txt(8, 53.6, "DOKUMENTER · INDONESIA", pt(6.2), INK, weight=400,
                 tracking=0.16, caps=True, opacity=0.6))
    return print_doc(W, H, "\n".join(g), "ODDCHAPTER — business card back, 85 x 55 + 3 mm bleed")


# ------------------------------------------------------------------ poster
def poster():
    W, H = 426, 600          # 420 x 594 trim + 3 mm bleed
    x0 = 3 + 30              # trim + margin
    g = [f'<rect width="{W}" height="{H}" fill="{INK}"/>']
    # hairline field
    for yy in (150, 300, 450):
        g.append(f'<rect x="{x0}" y="{yy}" width="{W - 2*x0}" height="0.3" fill="{SAGE}" opacity="0.14"/>')

    g.append(txt(x0, 46, "ODDCHAPTER", pt(11), SAGE, weight=600, tracking=0.3, caps=True))
    g.append(txt(W - x0, 46, "01", pt(11), ORANGE, family="grotesk", weight=700, anchor="end"))

    lines = ["REAL STORIES.", "UNEXPECTED", "CHAPTERS."]
    size = fit_size(lines, W - 2 * x0 - 6, tracking=-0.02)
    lead = size * 1.02
    y = 118 + size
    for i, ln in enumerate(lines):
        svg, _ = outline(ln, x0, y + i * lead, size, IVORY, tracking=-0.02)
        g.append(svg)
    base = y + 2 * lead
    g.append(f'<rect x="{x0}" y="{f(base + 26)}" width="120" height="4" fill="{ORANGE}"/>')
    g.append(txt(x0, base + 62, "KISAH NYATA. DI LUAR DUGAAN.", pt(13), IVORY,
                 weight=500, tracking=0.18, caps=True, opacity=0.85))

    body, sc, lw, lh = lockup_mm(120, {"word": IVORY, "accent": ORANGE}, tagline=True)
    g.append(f'<g transform="translate({f(x0)} {f(H - 3 - 46 - lh)}) scale({f(sc,6)})">{body}</g>')
    return print_doc(W, H, "\n".join(g), "ODDCHAPTER — poster A2")


# ------------------------------------------------------------------ merch
def sticker():
    W = H = 81               # 75 mm circle + 3 mm bleed
    c = W / 2
    g = [f'<rect width="{W}" height="{H}" fill="none"/>',
         f'<circle cx="{c}" cy="{c}" r="{W/2}" fill="{INK}"/>']
    g.append(monogram_centered(c, c - 9, 40, IVORY))
    wm, ww = brand.wordmark(7.0, IVORY, 0, 0)   # cap 7 mm
    g.append(f'<g transform="translate({f(c - ww/2)} {f(c + 6)})">{wm}</g>')
    g.append(txt(c, c + 24, "REAL STORIES. UNEXPECTED CHAPTERS.", pt(5.4), SAGE,
                 weight=600, tracking=0.17, caps=True, anchor="middle"))
    # die line — separate layer, must be removed or set as a die cut by the printer
    g.append(f'<g id="die-line"><circle cx="{c}" cy="{c}" r="{37.5}" fill="none" '
             f'stroke="#FF00FF" stroke-width="0.25" stroke-dasharray="2 1.5"/></g>')
    return print_doc(W, H, "\n".join(g), "ODDCHAPTER — 75 mm die-cut sticker")


def tee_art():
    W, H = 297, 420
    body, sc, lw, lh = lockup_mm(150, {"word": K100, "accent": K100}, tagline=False)
    top = 150
    g = [f'<g transform="translate({f((W - lw) / 2)} {top}) scale({f(sc,6)})">{body}</g>',
         f'<rect x="{f((W-40)/2)}" y="{f(top + lh + 14)}" width="40" height="0.5" fill="{K100}"/>',
         txt(W / 2, top + lh + 30, "KISAH NYATA. DI LUAR DUGAAN.", pt(9), K100, weight=500,
             tracking=0.18, caps=True, anchor="middle")]
    return print_doc(W, H, "\n".join(g), "ODDCHAPTER — tee artwork A3 print area, one colour")


# ------------------------------------------------------------------ scale test
def scale_test():
    sizes = [(5, "below the floor"), (8, "minimum"), (10, "safe"), (14, "comfortable"), (20, "large")]
    W, H = 180, 90
    g = [f'<rect width="{W}" height="{H}" fill="{IVORY}"/>']
    g.append(txt(8, 12, "PRINT MINIMUM SIZE — TRUE MILLIMETRES", pt(8), INK, weight=600,
                 tracking=0.2, caps=True))
    x = 10
    for mm, label in sizes:
        g.append(monogram_centered(x + mm / 2, 34, mm, INK))
        g.append(f'<rect x="{x}" y="26" width="{mm}" height="0.15" fill="{SAGE}"/>')
        g.append(f'<rect x="{x}" y="42" width="{mm}" height="0.15" fill="{SAGE}"/>')
        g.append(txt(x, 50, f"{mm} mm", pt(6.5), INK, weight=600))
        g.append(txt(x, 55, "OK" if mm >= 8 else "TOO SMALL", pt(5.5),
                     SAGE if mm >= 8 else ORANGE, weight=600, tracking=0.15, caps=True))
        x += 33
    g.append(f'<rect x="10" y="62" width="{W-20}" height="0.2" fill="{SAGE}"/>')
    g.append(txt(10, 69, "Print the sheet at 100 % and check the 8 mm mark at arm's length.",
                 pt(6.5), INK, opacity=0.7))
    g.append(txt(10, 74, "A 100 % scale print is the only test that means anything — a screen cannot fake it.",
                 pt(6.5), INK, opacity=0.7))
    return print_doc(W, H, "\n".join(g), "ODDCHAPTER — print minimum size test")


def main():
    write("07_PRINT/one_colour/LOGO_100K.svg", one_colour_lockup())
    write("07_PRINT/one_colour/MONOGRAM_100K.svg", one_colour_monogram())
    write("07_PRINT/stationery/LETTERHEAD_A4_210x297.svg", letterhead())
    write("07_PRINT/stationery/BUSINESS_CARD_FRONT_91x61.svg", card_front())
    write("07_PRINT/stationery/BUSINESS_CARD_BACK_91x61.svg", card_back())
    write("07_PRINT/poster/POSTER_A2_420x594.svg", poster())
    write("07_PRINT/merch/STICKER_DIECUT_75mm.svg", sticker())
    write("07_PRINT/merch/TEE_ART_A3_297x420.svg", tee_art())
    write("07_PRINT/PRINT_SCALE_TEST.svg", scale_test())


if __name__ == "__main__":
    main()
