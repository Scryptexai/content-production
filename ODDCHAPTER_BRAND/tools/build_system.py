"""
build_system.py — Phase 3: the logo system.

Writes the production masters and variants. Nothing here invents new geometry:
everything is generated from tools/brand.py, which holds the approved LINK drawing.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import brand
from brand import (INK, IVORY, ORANGE, SAGE, MONO_PATH, O_PATH, C_PATH, MW, MH, monogram_centered,
                   STROKE, monogram, monogram_svg, lockup_svg, svg_doc, text, f, ring, c_ring)

ROOT = brand.ROOT
A = "#%s"  # (no-op helper to keep f-strings short)


def write(path, content):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content)
    return p


# ------------------------------------------------------------------ masters
def logo_master():
    body, w, h = brand.lockup(colors={"word": INK, "accent": ORANGE}, ids=True)
    p = 36 * 0.30
    doc = svg_doc(round(w + 2 * p, 2), round(h + 2 * p, 2),
                  f'<g transform="translate({f(p)} {f(p)})">{body}</g>',
                  title="ODDCHAPTER — primary horizontal logo, master")
    return doc


def main():
    made = []

    # --- primary + tagline lockups
    made.append(write("01_LOGO/master/LOGO_MASTER.svg", logo_master()))
    for name, bg, cols in [
        ("01_LOGO/dark/LOGO_DARK.svg", INK, {"word": IVORY, "accent": ORANGE}),
        ("01_LOGO/light/LOGO_LIGHT.svg", IVORY, {"word": INK, "accent": ORANGE}),
        ("01_LOGO/monochrome/LOGO_MONO.svg", None, {"word": INK, "accent": INK}),
    ]:
        made.append(write(name, lockup_svg(bg=bg, colors=cols)[0]))

    for name, bg, cols, pad in [
        ("01_LOGO/master/LOGO_MASTER_TAGLINE.svg", None, {"word": INK, "accent": ORANGE}, 0.30),
        ("01_LOGO/dark/LOGO_DARK_TAGLINE.svg", INK, {"word": IVORY, "accent": ORANGE}, 0.30),
        ("01_LOGO/light/LOGO_LIGHT_TAGLINE.svg", IVORY, {"word": INK, "accent": ORANGE}, 0.30),
    ]:
        body, w, h = brand.lockup(colors=cols, tagline=True)
        p = 36 * pad
        doc = svg_doc(round(w + 2 * p, 2), round(h + 2 * p, 2),
                      f'<g transform="translate({f(p)} {f(p)})">{body}</g>',
                      bg=bg, title="ODDCHAPTER — horizontal logo with tagline")
        made.append(write(name, doc))

    # --- monogram
    made.append(write("01_LOGO/master/MONOGRAM_MASTER.svg", monogram_svg(None, INK)[0]))
    made.append(write("01_LOGO/dark/MONOGRAM_DARK.svg", monogram_svg(INK, IVORY)[0]))
    made.append(write("01_LOGO/light/MONOGRAM_LIGHT.svg", monogram_svg(IVORY, INK)[0]))
    made.append(write("01_LOGO/monochrome/MONOGRAM_MONO.svg", monogram_svg(None, INK)[0]))

    # --- square icon (favicon / app icon): the monogram, optically centred on 1:1
    made.append(write("01_LOGO/master/ICON_SQUARE.svg", icon_square(None, INK)))
    made.append(write("01_LOGO/dark/ICON_SQUARE_DARK.svg", icon_square(INK, IVORY)))

    # --- compact avatar lock: monogram optically scaled for a circle
    made.append(write("01_LOGO/master/AVATAR_COMPACT.svg", avatar_lock()))

    # --- layered source for motion (separate O / C / wordmark)
    made.append(write("04_MOTION/svg_components/monogram_layers.svg", motion_monogram()))
    made.append(write("04_MOTION/svg_components/wordmark_layer.svg", motion_wordmark()))
    made.append(write("04_MOTION/svg_components/tagline_layer.svg", motion_tagline()))

    for p in made:
        print("wrote", p.relative_to(ROOT))


def icon_square(bg, fg):
    """1:1 canvas for favicons and app icons; the mark is centred, not cropped."""
    S = 100
    body = ((f'<rect width="{S}" height="{S}" fill="{bg}"/>' if bg else " ")
            + monogram_centered(S / 2, S / 2, S * 0.76, fg))
    return svg_doc(S, S, body, bg=None, title="ODDCHAPTER — square icon")


def avatar_lock():
    """Monogram inside a 100 x 100 avatar box, sized to the circular safe zone."""
    S = 100
    safe = 0.62                      # diameter share of the circle
    mark_w = S * safe
    sc = mark_w / MW
    x = (S - MW * sc) / 2
    y = (S - MH * sc) / 2
    body = (f'<circle id="safe-circle" cx="{S/2}" cy="{S/2}" r="{S/2}" fill="{INK}"/>'
            + monogram(x, y, sc, IVORY, ids=True))
    return svg_doc(S, S, body, bg=None, title="ODDCHAPTER — compact avatar lock")


def motion_monogram():
    body = brand.monogram(10, 10, 1.0, "#000000", layers=True)
    return svg_doc(MW + 20, MH + 20, body, bg=None,
                   title="ODDCHAPTER — monogram layers (O / C) for animation")


def motion_wordmark():
    d, w = brand.wordmark(100, "#000000", 0, 0)
    return svg_doc(round(w + 20, 2), 120, f'<g id="wordmark" transform="translate(10 10)">{d}</g>',
                   bg=None, title="ODDCHAPTER — wordmark layer")


def motion_tagline():
    """Tagline as outlines, so the motion layer carries no font dependency."""
    size = 100
    from oclib import wordmark_path
    d, w = wordmark_path(brand.TAGLINE, "inter", 600, size, 0.17)
    body = f'<g id="tagline" transform="translate(10 10)"><path d="{d}" fill="#000000"/></g>'
    return svg_doc(round(w + 20, 2), round(size * 1.05 + 20, 2), body, bg=None,
                   title="ODDCHAPTER — tagline layer")


if __name__ == "__main__":
    main()
