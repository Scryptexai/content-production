"""
build_thumbs.py — Phase 4: three thumbnail systems, as editable SVG templates.

1280 x 720 each. The image area is an explicit, clipped slot (id="image-slot") so a
photo or a frame grab can be dropped in without touching the layout. Sample headlines
are real Indonesian copy, not lorem ipsum — replace them with each story's title.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import brand
from brand import INK, IVORY, ORANGE, SAGE, MW, MH, monogram, svg_doc, text, f

ROOT = brand.ROOT
W, H = 1280, 720


def write(path, content):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content)
    print("wrote", path)


def slot(x, y, w, h, cid, tone="#0F1114"):
    """A clipped image slot with an editorial placeholder treatment."""
    g = [f'<clipPath id="{cid}"><rect x="{x}" y="{y}" width="{w}" height="{h}"/></clipPath>',
         f'<g clip-path="url(#{cid})">',
         f'<rect id="image-slot" x="{x}" y="{y}" width="{w}" height="{h}" fill="{tone}"/>']
    for i in range(int(x) - int(h), int(x) + int(w) + int(h), 96):
        g.append(f'<line x1="{i}" y1="{y+h}" x2="{i+h}" y2="{y}" stroke="{SAGE}" stroke-width="1" opacity="0.10"/>')
    g.append(f'<rect x="{x+20}" y="{y+20}" width="{w-40}" height="{h-40}" fill="none" stroke="{SAGE}" '
             f'stroke-width="1.4" opacity="0.22" stroke-dasharray="10 8"/>')
    g.append(f'<text x="{x+w-32}" y="{y+h-28}" font-family="Inter" font-weight="600" font-size="14" '
             f'letter-spacing="2.6" fill="{SAGE}" opacity="0.55" text-anchor="end">FOTO · SLOT GAMBAR</text>')
    g.append('</g>')
    return "\n".join(g)


def chip(x, y, label, filled=True, size=15, padx=18, h=36):
    w = len(label) * size * 0.66 + padx * 2
    if filled:
        return (f'<rect x="{x}" y="{y}" width="{f(w)}" height="{h}" fill="{ORANGE}"/>'
                f'<text x="{x + w/2}" y="{y + h/2 + size*0.36}" font-family="Inter" font-weight="700" '
                f'font-size="{size}" letter-spacing="2" fill="{INK}" text-anchor="middle">{label}</text>')
    return (f'<rect x="{x}" y="{y}" width="{f(w)}" height="{h}" fill="none" stroke="{SAGE}" stroke-width="1.6"/>'
            f'<text x="{x + w/2}" y="{y + h/2 + size*0.36}" font-family="Inter" font-weight="600" '
            f'font-size="{size}" letter-spacing="2" fill="{IVORY}" text-anchor="middle">{label}</text>')


def sig(x, y, color=IVORY, hgt=48):
    sc = hgt / MH
    return monogram(x, y, sc, color)


def t1_extraordinary():
    """Full-bleed subject, title on a solid ink band. The default for event stories."""
    band = 236
    top = H - band
    g = [f'<rect width="{W}" height="{H}" fill="{INK}"/>']
    g.append(slot(0, 0, W, top, "slot1"))
    g.append(f'<rect x="0" y="{top}" width="{W}" height="{band}" fill="{INK}"/>')
    g.append(f'<rect x="0" y="{top}" width="{W}" height="3" fill="{ORANGE}"/>')
    g.append(f'<text x="64" y="{top+42}" font-family="Inter" font-weight="600" font-size="15" '
             f'letter-spacing="3.2" fill="{SAGE}">01 · PERISTIWA LUAR BIASA</text>')
    g.append(f'<text x="64" y="{top+112}" font-family="Space Grotesk" font-weight="700" font-size="62" '
             f'fill="{IVORY}">KAPAL YANG HILANG</text>')
    g.append(f'<text x="64" y="{top+178}" font-family="Space Grotesk" font-weight="700" font-size="62" '
             f'fill="{ORANGE}">TANPA JEJAK</text>')
    g.append(sig(W - 64 - 62 * (MW / MH), top + 60, IVORY, 62))
    g.append(f'<rect x="{W-64-96}" y="{top+150}" width="96" height="3" fill="{SAGE}" opacity="0.5"/>')
    g.append(chip(64, 40, "DOKUMENTER", filled=True))
    return svg_doc(W, H, "\n".join(g), bg=None,
                   title="ODDCHAPTER thumbnail template — extraordinary event")


def t2_survival():
    """Vertical split: ink panel for the title, subject on two thirds. Survival stories."""
    panel = 500
    g = [f'<rect width="{W}" height="{H}" fill="{INK}"/>']
    g.append(slot(panel, 0, W - panel, H, "slot2"))
    g.append(f'<rect x="0" y="0" width="{panel}" height="{H}" fill="{INK}"/>')
    g.append(f'<rect x="{panel-6}" y="0" width="6" height="{H}" fill="{ORANGE}"/>')
    g.append(f'<text x="64" y="96" font-family="Inter" font-weight="600" font-size="16" '
             f'letter-spacing="3.4" fill="{SAGE}">02 · BERTAHAN HIDUP</text>')
    g.append(f'<text x="64" y="250" font-family="Space Grotesk" font-weight="700" font-size="68" '
             f'fill="{IVORY}">BERTAHAN</text>')
    g.append(f'<text x="64" y="328" font-family="Space Grotesk" font-weight="700" font-size="68" '
             f'fill="{IVORY}">HIDUP</text>')
    g.append(f'<text x="64" y="404" font-family="Space Grotesk" font-weight="700" font-size="52" '
             f'fill="{ORANGE}">BERHARI-HARI</text>')
    g.append(f'<rect x="64" y="450" width="88" height="4" fill="{SAGE}"/>')
    g.append(f'<text x="64" y="498" font-family="Inter" font-weight="400" font-size="23" '
             f'fill="{IVORY}" opacity="0.72">di tengah laut terbuka</text>')
    g.append(sig(64, H - 130, IVORY, 62))
    return svg_doc(W, H, "\n".join(g), bg=None,
                   title="ODDCHAPTER thumbnail template — human survival")


def t3_science():
    """Top image band, two-line title below, monogram as a right-hand anchor."""
    band = 452
    g = [f'<rect width="{W}" height="{H}" fill="{INK}"/>']
    g.append(slot(0, 0, W, band, "slot3"))
    g.append(f'<rect x="0" y="{band}" width="{W}" height="{H-band}" fill="{INK}"/>')
    g.append(chip(48, band + 34, "SAINS ANEH", filled=True))
    g.append(f'<text x="48" y="{band+146}" font-family="Space Grotesk" font-weight="700" font-size="58" '
             f'fill="{IVORY}">TUBUH MANUSIA</text>')
    g.append(f'<text x="48" y="{band+210}" font-family="Space Grotesk" font-weight="700" font-size="58" '
             f'fill="{IVORY}">YANG MEMBEKU</text>')
    g.append(f'<rect x="48" y="{band+234}" width="{W-96}" height="2" fill="{SAGE}" opacity="0.35"/>')
    g.append(sig(W - 64 - 54 * (MW / MH), band + 118, IVORY, 54))
    return svg_doc(W, H, "\n".join(g), bg=None,
                   title="ODDCHAPTER thumbnail template — strange science")


def main():
    write("02_YOUTUBE/thumbnails/TEMPLATE_01_PERISTIWA.svg", t1_extraordinary())
    write("02_YOUTUBE/thumbnails/TEMPLATE_02_BERTAHAN_HIDUP.svg", t2_survival())
    write("02_YOUTUBE/thumbnails/TEMPLATE_03_SAINS_ANEH.svg", t3_science())


if __name__ == "__main__":
    main()
