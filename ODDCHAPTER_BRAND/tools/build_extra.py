"""
build_extra.py — Phase 7: surfaces the first six phases did not cover.

 03_SOCIAL/stories/SOCIAL_STORY_1080x1920          vertical story template
 03_SOCIAL/stories/SOCIAL_STORY_COVER_1080x1920    vertical cover / teaser
 03_SOCIAL/link_preview/OPEN_GRAPH_1200x630        link + OG card
 02_YOUTUBE/end_card/YOUTUBE_END_CARD_1920x1080    end screen

Same rules as every other surface: Ink ground, one orange element per composition,
image areas are clipped slots with id="image-slot", sample copy is real Indonesian.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import brand
from brand import INK, IVORY, ORANGE, SAGE, MW, MH, monogram_centered, svg_doc, text, f, lockup
from build_thumbs import chip

ROOT = brand.ROOT


def write(path, content):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content)
    print("wrote", path)


def slot(x, y, w, h, cid, tone="#0F1114", caption="FOTO · SLOT GAMBAR"):
    """Clipped image slot with the house hatch. Segments are computed inside the box —
    the naive full-plane hatch makes resvg panic on tall canvases."""
    g = [f'<clipPath id="{cid}"><rect x="{x}" y="{y}" width="{w}" height="{h}"/></clipPath>',
         f'<g clip-path="url(#{cid})">',
         f'<rect id="image-slot" x="{x}" y="{y}" width="{w}" height="{h}" fill="{tone}"/>']
    step = 96
    c = (y + x) - (y + x) % step
    while c < y + h + x + w:
        xa, xb = max(x, c - (y + h)), min(x + w, c - y)
        if xb - xa > 0.5:
            g.append(f'<line x1="{f(xa)}" y1="{f(c - xa)}" x2="{f(xb)}" y2="{f(c - xb)}" '
                     f'stroke="{SAGE}" stroke-width="1" opacity="0.10"/>')
        c += step
    g.append(f'<rect x="{x+20}" y="{y+20}" width="{w-40}" height="{h-40}" fill="none" stroke="{SAGE}" '
             f'stroke-width="1.4" opacity="0.22" stroke-dasharray="10 8"/>')
    g.append(f'<text x="{x+w-32}" y="{y+h-28}" font-family="Inter" font-weight="600" font-size="14" '
             f'letter-spacing="2.6" fill="{SAGE}" opacity="0.55" text-anchor="end">{caption}</text>')
    g.append('</g>')
    return "\n".join(g)


def headline(lines, x, y, size=92, color=IVORY, leading=1.02, weight=700):
    out = []
    for i, ln in enumerate(lines):
        out.append(text(x, y + i * size * leading, ln, "grotesk", weight, size, color))
    return "\n".join(out), y + (len(lines) - 1) * size * leading


def rule(x, y, w, color=ORANGE, h=4):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{color}"/>'


# ------------------------------------------------------------------ 9:16 story
def story():
    W, H = 1080, 1920
    band_y = 1180
    g = [f'<rect width="{W}" height="{H}" fill="{INK}"/>']
    g.append(slot(0, 0, W, band_y, "story-slot"))

    # top label, outside the platform's UI zones
    g.append(f'<rect x="64" y="120" width="230" height="52" fill="{ORANGE}"/>')
    g.append(text(64 + 115, 120 + 34, "EPISODE 01", "inter", 700, 22, INK, tracking=3.2,
                  caps=True, anchor="middle"))
    g.append(text(W - 64, 156, "ODDCHAPTER", "inter", 600, 20, IVORY, tracking=4.2,
                  caps=True, anchor="end", opacity=0.85))

    # bottom band carries the whole message
    g.append(f'<rect x="0" y="{band_y}" width="{W}" height="{H-band_y}" fill="{INK}"/>')
    g.append(rule(64, band_y + 4, 120, SAGE, 2))

    g.append(text(64, band_y + 92, "PERISTIWA LUAR BIASA", "inter", 600, 24, SAGE,
                  tracking=5.2, caps=True))
    body, last = headline(["KAPAL YANG", "HILANG TANPA", "JEJAK"], 64, band_y + 206, size=96)
    g.append(body)
    g.append(rule(64, last + 54, 180, ORANGE, 6))
    g.append(text(64, last + 122, "Kisah nyata. Di luar dugaan.", "inter", 400, 30, IVORY,
                  opacity=0.8))
    g.append(chip(64, last + 168, "GESER KE ATAS", filled=False, size=17, padx=26, h=52))
    g.append(monogram_centered(W - 150, H - 150, 132, IVORY))
    return svg_doc(W, H, "\n".join(g), bg=None, title="ODDCHAPTER — story 1080 x 1920")


def story_cover():
    W, H = 1080, 1920
    g = [f'<rect width="{W}" height="{H}" fill="{INK}"/>']
    for y in range(0, H, 240):
        g.append(f'<rect x="0" y="{y}" width="{W}" height="1" fill="{SAGE}" opacity="0.06"/>')

    body, lw, lh = lockup(colors={"word": IVORY, "accent": ORANGE}, tagline=True)
    sc = 720 / lw
    g.append(f'<g transform="translate({f(W/2 - lw*sc/2)} {f(H/2 - lh*sc/2)}) scale({f(sc,6)})">{body}</g>')
    g.append(rule(W / 2 - 60, H / 2 + 210, 120, SAGE, 2))
    g.append(text(W / 2, H / 2 + 290, "KISAH NYATA. DI LUAR DUGAAN.", "inter", 600, 26, IVORY,
                  tracking=4.4, caps=True, anchor="middle", opacity=0.82))
    g.append(text(W / 2, H - 120, "SEGERA HADIR", "inter", 600, 22, SAGE, tracking=6, caps=True,
                  anchor="middle"))
    return svg_doc(W, H, "\n".join(g), bg=None, title="ODDCHAPTER — story cover 1080 x 1920")


# ------------------------------------------------------------------ OG card
def og_card():
    W, H = 1200, 630
    g = [f'<rect width="{W}" height="{H}" fill="{INK}"/>']
    g.append(f'<rect x="40" y="40" width="{W-80}" height="{H-80}" fill="none" stroke="{SAGE}" '
             f'stroke-width="1" opacity="0.16"/>')
    body, lw, lh = lockup(colors={"word": IVORY, "accent": ORANGE}, tagline=True)
    sc = 660 / lw
    g.append(f'<g transform="translate({f(W/2 - lw*sc/2)} {f(H/2 - lh*sc/2 - 10)}) scale({f(sc,6)})">{body}</g>')
    g.append(text(W / 2, H - 96, "DOKUMENTER · INDONESIA", "inter", 600, 18, SAGE, tracking=5.4,
                  caps=True, anchor="middle"))
    return svg_doc(W, H, "\n".join(g), bg=None, title="ODDCHAPTER — link preview 1200 x 630")


# ------------------------------------------------------------------ end card
def end_card():
    W, H = 1920, 1080
    g = [f'<rect width="{W}" height="{H}" fill="{INK}"/>']
    # hairline field
    for x in (160, 760, 1360, 1760):
        g.append(f'<rect x="{x}" y="120" width="1" height="{H-240}" fill="{SAGE}" opacity="0.07"/>')

    body, lw, lh = lockup(colors={"word": IVORY, "accent": ORANGE}, tagline=True)
    sc = 560 / lw
    lx, ly = 160, 440
    g.append(f'<g transform="translate({f(lx)} {f(ly)}) scale({f(sc,6)})">{body}</g>')
    g.append(text(160, 386, "EPISODE BERIKUTNYA", "inter", 600, 22, SAGE, tracking=5.2, caps=True))
    g.append(text(160, 640, "Tonton kartu di samping,", "inter", 400, 30, IVORY, opacity=0.75))
    g.append(text(160, 684, "atau pilih episode lain di bawah.", "inter", 400, 30, IVORY, opacity=0.75))

    # next-video slot (YouTube places its own elements over the right third)
    g.append(slot(1120, 300, 660, 371, "endcard-slot"))
    g.append(text(1120, 720, "SLOT VIDEO · KARTU AKHIR", "inter", 600, 18, SAGE, tracking=3.4,
                  caps=True))
    g.append(text(1120, 752, "Kosongkan jika memakai elemen bawaan YouTube.", "inter", 400, 20,
                  IVORY, opacity=0.6))

    # bottom bar
    g.append(f'<rect x="160" y="{H-160}" width="{W-320}" height="1.4" fill="{SAGE}" opacity="0.25"/>')
    g.append(monogram_centered(220, H - 96, 96, IVORY))
    g.append(text(300, H - 88, "ODDCHAPTER", "inter", 600, 22, IVORY, tracking=5.6, caps=True))
    g.append(text(W - 160, H - 88, "REAL STORIES. UNEXPECTED CHAPTERS.", "inter", 600, 20, SAGE,
                  tracking=4.2, caps=True, anchor="end"))
    return svg_doc(W, H, "\n".join(g), bg=None, title="ODDCHAPTER — YouTube end card 1920 x 1080")


def main():
    write("03_SOCIAL/stories/SOCIAL_STORY_1080x1920.svg", story())
    write("03_SOCIAL/stories/SOCIAL_STORY_COVER_1080x1920.svg", story_cover())
    write("03_SOCIAL/link_preview/OPEN_GRAPH_1200x630.svg", og_card())
    write("02_YOUTUBE/end_card/YOUTUBE_END_CARD_1920x1080.svg", end_card())


if __name__ == "__main__":
    main()
