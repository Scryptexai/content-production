"""
build_channel.py — Phase 4: YouTube and social assets.

Every asset is generated from tools/brand.py (the approved LINK geometry).
No raster master is produced; PNGs are exports of the SVG sources.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import brand
from brand import (monogram_centered, INK, IVORY, ORANGE, SAGE, MW, MH, STROKE, MONO_PATH,
                   monogram, lockup, svg_doc, text, f)

ROOT = brand.ROOT


def write(path, content):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content)
    print("wrote", path)
    return p


def centered_lockup(cx, y_top, width, colors, tagline=False, cap=None):
    """Return (svg, w, h) of the lockup scaled to `width`, left edge at cx-width/2."""
    body, w, h = lockup(colors=colors, cap=cap or 36, tagline=tagline)
    sc = width / w
    return (f'<g transform="translate({f(cx - (w*sc)/2)} {f(y_top)}) scale({f(sc,6)})">{body}</g>',
            width, h * sc)


def fit_monogram(cx, cy, w_target, color):
    return monogram_centered(cx, cy, w_target, color)


# ------------------------------------------------------------------ YouTube
AV_W = 800


def avatar():
    S = 800
    g = []
    g.append(f'<rect width="{S}" height="{S}" fill="{INK}"/>')
    g.append(f'<circle cx="{S/2}" cy="{S/2}" r="{S/2}" fill="{INK}"/>')
    g.append(monogram_centered(S / 2, S / 2, S * 0.60, IVORY, ids=True))
    return svg_doc(S, S, "\n".join(g), bg=None,
                   title="ODDCHAPTER — YouTube avatar 800 x 800")


def banner():
    """Editorial field: hairline grid, generous ink, the lockup inside the safe area."""
    W, H = 2560, 1440
    g = [f'<rect width="{W}" height="{H}" fill="{INK}"/>']

    # editorial hairline grid — structure, not decoration; opacity keeps it quiet
    for x in range(320, W, 320):
        g.append(f'<rect x="{x-0.5}" y="0" width="1" height="{H}" fill="{SAGE}" opacity="0.07"/>')
    for y in (360, 720, 1080):
        g.append(f'<rect x="0" y="{y-0.5}" width="{W}" height="1" fill="{SAGE}" opacity="0.07"/>')

    # margin frame, visible mostly on the TV crop
    g.append(f'<rect x="120" y="120" width="{W-240}" height="{H-240}" fill="none" '
             f'stroke="{SAGE}" stroke-width="2" opacity="0.20"/>')

    # the lockup, well inside the 1546 x 423 safe area
    lk, lw, lh = centered_lockup(W / 2, 0, 1080, {"word": IVORY, "accent": ORANGE}, tagline=True)
    ty = (H - lh) / 2
    g.append(f'<g transform="translate(0 {f(ty)})">{lk}</g>')
    return svg_doc(W, H, "\n".join(g), bg=None,
                   title="ODDCHAPTER — YouTube channel banner 2560 x 1440")


def banner_guide():
    """Crop-check sheet: the same file through each YouTube surface crop."""
    W, H, PAD, MAXW = 2560, 1440, 80, 2140
    panels = [
        ("TV / FULL BLEED", 2560, 1440, "the entire 2560 × 1440 file"),
        ("DESKTOP", 2560, 423, "centre band, 2560 × 423"),
        ("MOBILE", 1546, 423, "centre band, 1546 × 423"),
    ]
    b = [text(PAD, 92, "YOUTUBE BANNER — CROP CHECK", "grotesk", 700, 44, INK),
         text(PAD, 126, "One file, three surfaces. Nothing essential may fall outside the mobile band.",
              "inter", 400, 17, INK, opacity=0.65)]
    y = 196
    for label, cw, ch, note in panels:
        sc = min(MAXW / cw, 660 / ch)
        pw, ph = cw * sc, ch * sc
        cx = PAD + (MAXW - pw) / 2
        b.append(text(PAD, y - 16, label, "inter", 600, 13, ORANGE, tracking=2.4, caps=True))
        b.append(text(PAD + 220, y - 16, note, "inter", 400, 13, INK, opacity=0.5))
        cid = f'crop{label[:2].strip().replace("/", "")}'
        b.append(f'<clipPath id="{cid}"><rect x="{f(cx)}" y="{f(y)}" width="{f(pw)}" height="{f(ph)}"/></clipPath>')
        b.append(f'<rect x="{f(cx)}" y="{f(y)}" width="{f(pw)}" height="{f(ph)}" fill="{INK}"/>')
        ix = cx - (W - cw) / 2 * sc
        iy = y - (H - ch) / 2 * sc
        b.append(f'<g clip-path="url(#{cid})"><g transform="translate({f(ix)} {f(iy)}) scale({f(sc,6)})">'
                 f'{banner_body()}</g></g>')
        b.append(f'<rect x="{f(cx)}" y="{f(y)}" width="{f(pw)}" height="{f(ph)}" fill="none" '
                 f'stroke="{ORANGE}" stroke-width="1.6"/>')
        y += ph + 108

    sc = min(MAXW / W, 520 / H)
    b.append(text(PAD, y - 16, "SAFE AREA DIAGRAM", "inter", 600, 13, ORANGE, tracking=2.4, caps=True))
    b.append(f'<rect x="{PAD}" y="{f(y)}" width="{f(W*sc)}" height="{f(H*sc)}" fill="{INK}"/>')
    b.append(f'<g transform="translate({PAD} {f(y)}) scale({f(sc,6)})">{banner_body()}</g>')
    b.append(f'<rect x="{f(PAD + (W-1546)/2*sc)}" y="{f(y + (H-423)/2*sc)}" '
             f'width="{f(1546*sc)}" height="{f(423*sc)}" fill="none" stroke="{ORANGE}" '
             f'stroke-width="3" stroke-dasharray="14 10"/>')
    b.append(text(PAD + W * sc + 40, y + 40, "1546 × 423", "inter", 700, 20, INK))
    b.append(text(PAD + W * sc + 40, y + 68, "all-device safe area", "inter", 400, 15, INK, opacity=0.6))
    b.append(text(PAD + W * sc + 40, y + 104, "lockup: 1080 wide", "inter", 400, 15, INK, opacity=0.6))
    b.append(text(PAD + W * sc + 40, y + 126, "= 70 % of safe width", "inter", 400, 15, INK, opacity=0.6))
    b.append(text(PAD, y + H * sc + 40,
                  "Critical content sits inside the mobile band, so no crop loses the lockup or the tagline.",
                  "inter", 400, 15, INK, opacity=0.7))
    return svg_doc(2400, y + H * sc + 90, "\n".join(b), bg=IVORY,
                   title="ODDCHAPTER — banner crop check")


def banner_body():
    """The banner artwork without the outer <svg> wrapper (for compositing into crops)."""
    doc = banner()
    return doc.split("<svg", 1)[1].split(">", 1)[1].rsplit("</svg>", 1)[0]


def watermark():
    out = {}
    S = 150
    for name, color in [("WATERMARK_LIGHT", IVORY), ("WATERMARK_DARK", INK)]:
        out[name] = svg_doc(S, S, monogram_centered(S / 2, S / 2, S * 0.80, color), bg=None,
                            title=f"ODDCHAPTER watermark {S} x {S}")
    return out


# ------------------------------------------------------------------ social
def social_profile():
    S = 1024
    body = (f'<rect width="{S}" height="{S}" fill="{INK}"/>'
            + monogram_centered(S / 2, S / 2, S * 0.60, IVORY))
    return svg_doc(S, S, body, bg=None, title="ODDCHAPTER — social profile icon 1024 x 1024")


def social_horizontal(bg, colors, suffix):
    W, H = 1500, 500
    lk, lw, lh = centered_lockup(W / 2, 0, 900, colors, tagline=True)
    ty = (H - lh) / 2
    body = (f'<rect width="{W}" height="{H}" fill="{bg}"/>'
            f'<g transform="translate(0 {f(ty)})">{lk}</g>')
    return svg_doc(W, H, body, bg=None, title=f"ODDCHAPTER — social header {suffix}")


def social_post():
    """1080 x 1080 editorial post template: image slot + brand block."""
    S = 1080
    pad = 72
    img_h = 560
    g = [f'<rect width="{S}" height="{S}" fill="{INK}"/>']

    # image slot (clipped, documented as a slot rather than a fake photo)
    g.append(f'<clipPath id="imgslot"><rect x="{pad}" y="{pad}" width="{S-2*pad}" height="{img_h}" rx="0"/></clipPath>')
    g.append(f'<g clip-path="url(#imgslot)">')
    g.append(f'<rect x="{pad}" y="{pad}" width="{S-2*pad}" height="{img_h}" fill="#0F1114"/>')
    g.append(f'<text x="{pad + 28}" y="{pad + img_h - 28}" font-family="Inter" font-weight="600" '
             f'font-size="15" letter-spacing="2.6" fill="{SAGE}" opacity="0.75">IMAGE SLOT · 936 × 560</text>')
    g.append('</g>')
    g.append(f'<rect x="{pad}" y="{pad}" width="{S-2*pad}" height="{img_h}" fill="none" '
             f'stroke="{SAGE}" stroke-width="1.4" opacity="0.35"/>')

    # category chip
    g.append(f'<rect x="{pad}" y="{pad + img_h + 56}" width="196" height="34" fill="{ORANGE}"/>')
    g.append(f'<text x="{pad + 98}" y="{pad + img_h + 79}" font-family="Inter" font-weight="700" '
             f'font-size="15" letter-spacing="2.2" fill="{INK}" text-anchor="middle">KATEGORI</text>')

    # headline (real sample copy, not placeholder)
    g.append(f'<text x="{pad}" y="{pad + img_h + 172}" font-family="Space Grotesk" font-weight="700" '
             f'font-size="62" fill="{IVORY}">Judul cerita</text>')
    g.append(f'<text x="{pad}" y="{pad + img_h + 240}" font-family="Space Grotesk" font-weight="700" '
             f'font-size="62" fill="{IVORY}">dalam dua baris.</text>')

    # footer: rule + monogram + handle line
    g.append(f'<rect x="{pad}" y="{S-pad-58}" width="{S-2*pad}" height="2" fill="{SAGE}" opacity="0.45"/>')
    sc = 40 / MH
    g.append(monogram(pad, S - pad - 44, sc, IVORY))
    g.append(f'<text x="{S-pad}" y="{S-pad-32}" font-family="Inter" font-weight="500" font-size="17" '
             f'letter-spacing="2.4" fill="{SAGE}" text-anchor="end">ODDCHAPTER</text>')
    return svg_doc(S, S, "\n".join(g), bg=None, title="ODDCHAPTER — social post template 1080 x 1080")


def main():
    write("02_YOUTUBE/avatar/YOUTUBE_AVATAR_800.svg", avatar())
    write("02_YOUTUBE/banner/YOUTUBE_BANNER_2560x1440.svg", banner())
    write("02_YOUTUBE/banner/BANNER_CROP_CHECK.svg", banner_guide())
    for name, doc in watermark().items():
        write(f"02_YOUTUBE/watermark/{name}_150.svg", doc)
    write("03_SOCIAL/profile/SOCIAL_PROFILE_1024.svg", social_profile())
    write("03_SOCIAL/profile/SOCIAL_HEADER_DARK.svg", social_horizontal(INK, {"word": IVORY, "accent": ORANGE}, "dark"))
    write("03_SOCIAL/profile/SOCIAL_HEADER_LIGHT.svg", social_horizontal(IVORY, {"word": INK, "accent": ORANGE}, "light"))
    write("03_SOCIAL/post_templates/SOCIAL_POST_1080.svg", social_post())


if __name__ == "__main__":
    main()
