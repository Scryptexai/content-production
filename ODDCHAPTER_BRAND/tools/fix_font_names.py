"""
fix_font_names.py — make resvg find the brand fonts.

The @fontsource files ship with one name table per *weight file*: every
Space Grotesk file claims the family "Space Grotesk Light" (nameID 1) with
subfamily "Bold" at 700, and Inter 600 claims "Inter SemiBold". resvg matches
on nameID 1, so `font-family="Space Grotesk" font-weight="700"` matched nothing
and fell back to DejaVu Sans — every live-text render was in the wrong typeface.

This rewrites nameID 1/2/4/6/16/17 in .build/fonts (a generated directory, not
committed) to the real family and weight. Idempotent; safe to re-run.

  python3 tools/fix_font_names.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from oclib import BUILD  # noqa: E402

FONTDIR = BUILD          # oclib.BUILD already points at .build/fonts

STYLE = {300: "Light", 400: "Regular", 500: "Medium", 600: "SemiBold", 700: "Bold"}
FAMILY = {"space-grotesk": "Space Grotesk", "inter": "Inter"}


def parse(path):
    m = re.match(r"([a-z-]+)-latin-(\d{3})-normal\.ttf$", path.name)
    if not m or m.group(1) not in FAMILY:
        return None
    family = FAMILY[m.group(1)]
    weight = int(m.group(2))
    return family, weight


def main():
    from fontTools.ttLib import TTFont
    files = sorted(FONTDIR.glob("*.ttf"))
    if not files:
        raise SystemExit("no fonts in .build/fonts — run bash tools/fetch_fonts.sh")
    for path in files:
        got = parse(path)
        if not got:
            print(f"skip   {path.name}")
            continue
        family, weight = got
        style = STYLE[weight]
        full = family if weight == 400 else f"{family} {style}"
        ps = f"{family.replace(' ', '')}-{style}"
        font = TTFont(str(path))
        name = font["name"]
        records = {1: family, 2: style, 3: ps, 4: full, 6: ps, 16: family, 17: style}
        for nid, value in records.items():
            name.setName(value, nid, 3, 1, 0x409)
            name.setName(value, nid, 1, 0, 0)
        font["OS/2"].usWeightClass = weight
        font["OS/2"].fsSelection = (font["OS/2"].fsSelection & ~0x21) | (0x20 if weight >= 700 else 0x40)
        font["head"].macStyle = (font["head"].macStyle & ~0x01) | (0x01 if weight >= 700 else 0)
        font.save(str(path))
        print(f"{path.name:38s} -> {family} {style}  ({weight})")


if __name__ == "__main__":
    main()
