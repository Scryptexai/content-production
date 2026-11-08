"""
build_episode_kit.py — Phase 11: the on-screen graphics every episode needs.

These are the pieces the brand system never had because they only exist inside a cut:
lower thirds, chapter cards and the subtitle plate. All 1920 x 1080, all transparent where
they overlay footage, all drawn from the same tokens as the logo.

  09_EPISODE_KIT/onscreen/LOWER_THIRD_NAME.svg
  09_EPISODE_KIT/onscreen/LOWER_THIRD_LOCATION.svg
  09_EPISODE_KIT/onscreen/CHAPTER_CARD.svg
  09_EPISODE_KIT/onscreen/SUBTITLE_SAMPLE.svg
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import brand
from brand import INK, IVORY, ORANGE, SAGE, monogram_centered, svg_doc, text, f

ROOT = brand.ROOT
W, H = 1920, 1080
SAFE = 120              # 6.25 % of the width — inside YouTube's title-safe area


def write(path, content):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content)
    print("wrote", path)


def hairlines(g, x0, x1, y, opacity=0.10):
    g.append(f'<rect x="{x0}" y="{y}" width="{x1-x0}" height="1" fill="{SAGE}" opacity="{opacity}"/>')


# ------------------------------------------------------------------ lower thirds
def lower_third_name():
    """Narasumber strap. Labels are fields to fill, not sample copy."""
    g = []
    x, y, w, h = SAFE, 690, 620, 148
    g.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{INK}" opacity="0.92"/>')
    g.append(f'<rect x="{x}" y="{y}" width="6" height="{h}" fill="{ORANGE}"/>')
    g.append(text(x + 34, y + 40, "NARASUMBER", "inter", 600, 19, ORANGE, tracking=4.4, caps=True))
    g.append(text(x + 34, y + 92, "NAMA NARASUMBER", "grotesk", 700, 44, IVORY))
    g.append(text(x + 34, y + 128, "Jabatan · Institusi", "inter", 400, 24, SAGE))
    return svg_doc(W, H, "\n".join(g), bg=None, title="ODDCHAPTER — name strap")


def lower_third_location():
    """Place and year. Deliberately quiet — it should read as a caption, not a title."""
    g = []
    x, y = SAFE, 760
    g.append(f'<rect x="{x}" y="{y}" width="120" height="3" fill="{ORANGE}"/>')
    g.append(text(x, y + 46, "LOKASI · 2018", "inter", 600, 26, IVORY, tracking=4.2, caps=True))
    return svg_doc(W, H, "\n".join(g), bg=None, title="ODDCHAPTER — location strap")


# ------------------------------------------------------------------ chapter card
def chapter_card():
    g = [f'<rect width="{W}" height="{H}" fill="{INK}"/>']
    for yy in (270, 540, 810):
        hairlines(g, SAFE, W - SAFE, yy, 0.07)
    g.append(text(SAFE, 200, "ODDCHAPTER", "inter", 600, 20, SAGE, tracking=6.0, caps=True))
    g.append(text(W - SAFE, 200, "BAB 01 / 04", "inter", 600, 20, SAGE, tracking=4.0,
                  caps=True, anchor="end"))

    g.append(text(SAFE, 650, "01", "grotesk", 700, 340, ORANGE))
    g.append(text(SAFE, 772, "AWAL MULA", "grotesk", 700, 96, IVORY))
    g.append(f'<rect x="{SAFE}" y="812" width="200" height="5" fill="{IVORY}"/>')
    g.append(text(SAFE, 884, "Satu kalimat yang menjelaskan bab ini.", "inter", 400, 30,
                  IVORY, opacity=0.72))
    return svg_doc(W, H, "\n".join(g), bg=None, title="ODDCHAPTER — chapter card")


# ------------------------------------------------------------------ subtitles
def subtitle_sample():
    """Two lines at 42 px over a 90 % plate — the spec in BRAND_GUIDELINES.md §8."""
    g = [f'<rect width="{W}" height="{H}" fill="{INK}"/>']
    # a stand-in frame: dense hatch so the plate's job is visible
    g.append(f'<g opacity="0.5">')
    for i in range(-H, W, 46):
        g.append(f'<line x1="{i}" y1="{H}" x2="{i+H}" y2="0" stroke="{SAGE}" stroke-width="2" opacity="0.25"/>')
    g.append('</g>')

    plate_w, plate_h = 1080, 168
    px, py = (W - plate_w) / 2, 862
    g.append(f'<rect x="{f(px)}" y="{py}" width="{plate_w}" height="{plate_h}" fill="{INK}" opacity="0.90"/>')
    g.append(text(W / 2, py + 70, "Kapal itu meninggalkan pelabuhan", "inter", 500, 42, IVORY,
                  anchor="middle"))
    g.append(text(W / 2, py + 128, "dengan dua puluh sembilan orang.", "inter", 500, 42, IVORY,
                  anchor="middle"))
    return svg_doc(W, H, "\n".join(g), bg=None, title="ODDCHAPTER — subtitle plate sample")


def main():
    write("09_EPISODE_KIT/onscreen/LOWER_THIRD_NAME.svg", lower_third_name())
    write("09_EPISODE_KIT/onscreen/LOWER_THIRD_LOCATION.svg", lower_third_location())
    write("09_EPISODE_KIT/onscreen/CHAPTER_CARD.svg", chapter_card())
    write("09_EPISODE_KIT/onscreen/SUBTITLE_SAMPLE.svg", subtitle_sample())


if __name__ == "__main__":
    main()
