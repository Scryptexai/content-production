"""
export_brand_json.py — brand geometry as JSON for the Remotion composition.

The film renders in a browser, so it must not depend on live text for the marks:
the monogram and wordmark ship as exact outline paths (same geometry as the SVG
masters, from tools/oclib.py). Body type is loaded from local TTF files.

  python3 tools/export_brand_json.py   ->  10_FILM/remotion/src/brand.json
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import brand
from oclib import INK, IVORY, ORANGE, SAGE

OUT = HERE.parent / "10_FILM" / "remotion" / "src" / "brand.json"

# wordmark authored at cap height 100, sitting on y = 0
wm_d, wm_w = brand.wordmark_path("ODDCHAPTER", "grotesk", 700, 100 / brand.CAP_RATIO, brand.WM_TRACK)
tag_d, tag_w = brand.wordmark_path(brand.TAGLINE, "inter", 600, 30, 0.17)

data = {
    "colors": {"ink": INK, "ivory": IVORY, "orange": ORANGE, "sage": SAGE},
    "monogram": {
        "d": brand.MONO_PATH,
        "viewBox": [0, 0, 100, 100],
        "inkBox": [brand.IX0, brand.BY0, brand.IX1, brand.BY1],
        "note": "98 x 54 units; centre on the ink box, not the 100 box",
    },
    "wordmark": {"d": wm_d, "width": round(wm_w, 3), "capHeight": 100},
    "tagline": {"d": tag_d, "width": round(tag_w, 3), "size": 30, "text": brand.TAGLINE},
    "ratios": {"markToCap": brand.MARK_TO_CAP, "gapToCap": brand.GAP_TO_CAP},
}
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(data, indent=2))
print(f"{OUT.relative_to(HERE.parent)}  monogram {len(brand.MONO_PATH)} chars · "
      f"wordmark {wm_w:.1f} @cap100 · tagline {tag_w:.1f}")
