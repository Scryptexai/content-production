"""
build_concepts.py — Phase 2 deliverable builder.

Generates:
  01_LOGO/concepts/LOGO_CONCEPTS.svg          (the three concepts, side by side)
  01_LOGO/concepts/concept-XX-<slug>/...      (per-concept dark / light / mono / construction)

Everything is emitted as vector. PNGs are produced separately by tools/render.mjs.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from oclib import (CONCEPTS, INK, IVORY, ORANGE, SAGE, mark_svg_body, place,
                   svg_doc, text, rule, wordmark_path, f)

ROOT = HERE.parent
OUT = ROOT / "01_LOGO" / "concepts"

DARK = {"ink": IVORY, "orange": ORANGE, "sage": SAGE}
LIGHT = {"ink": INK, "orange": ORANGE, "sage": SAGE}

CAP = 0.7  # Space Grotesk cap height / em


def wordmark(s, cap_height, x, y_top, color, weight=700, tracking=0.0):
    """Wordmark as outlines. (x, y_top) = left edge / cap-height line."""
    size = cap_height / CAP
    d, w = wordmark_path(s, "grotesk", weight, size, tracking)
    return (f'<g transform="translate({f(x)} {f(y_top + cap_height)})">'
            f'<path d="{d}" fill="{color}"/></g>', w)


def mark(concept, x, y, size, pal, mono=False):
    tr, _ = place(concept, x, y, size)
    return f'<g transform="{tr}">{mark_svg_body(concept, pal, mono=mono)}</g>'


# ------------------------------------------------------------------ sheet parts
def wrap(s, width):
    out, line = [], ""
    for word in s.split():
        if len(line) + len(word) + 1 > width:
            out.append(line)
            line = word
        else:
            line = (line + " " + word).strip()
    if line:
        out.append(line)
    return out


def build_sheet():
    W, MARGIN, GAP = 2600, 80, 32
    COLW = (W - 2 * MARGIN - 2 * GAP) / 3
    body = []

    # ---- header
    body.append(rule(MARGIN, 80, 64, 6))
    body.append(text(MARGIN, 122, "ODDCHAPTER  ·  BRAND IDENTITY  ·  PHASE 2", "inter", 600,
                     15, INK, tracking=3.2, caps=True, opacity=0.62))
    body.append(text(MARGIN, 214, "OC monogram — three directions", "grotesk", 700, 78, INK))
    body.append(text(MARGIN, 262, "Concepts for approval. Every mark below is exact vector geometry, "
                     "authored on a 100-unit grid — no raster lettering.", "inter", 400, 24, INK, opacity=0.66))
    # wordmark proof (type direction)
    wm, wmw = wordmark("ODDCHAPTER", 26, W - MARGIN - 372, 92, INK, 700, 0.16)
    body.append(wm)
    body.append(text(W - MARGIN, 148, "TYPE PROOF · SPACE GROTESK 700 · TRACKED", "inter", 500, 12,
                     INK, tracking=2.4, anchor="end", opacity=0.45))
    body.append(f'<rect x="{MARGIN}" y="300" width="{W-2*MARGIN}" height="1.2" fill="{SAGE}"/>')

    # ---- concept columns
    notes = {
        "link": ["Two equal rings. The crossing is knocked out, so each letter",
                 "passes through the other instead of sitting beside it.",
                 "Single colour by construction — no accent needed."],
        "stack": ["Compact vertical ligature; strongest recognition in a square",
                  "or circular crop. The Signal Orange rule is the joint.",
                  "Only the rule carries colour, keeping orange as an accent."],
        "cascade": ["Two letters of equal weight on an offset axis, joined at a",
                    "shallow junction so the pair reads as one moving unit.",
                    "Accent sits on the open letter — orange marks the opening."],
    }
    smalls = [48, 32, 24]
    for i, (num, slug, c) in enumerate(CONCEPTS):
        x = MARGIN + i * (COLW + GAP)
        body.append(text(x, 366, num, "grotesk", 700, 26, ORANGE))
        body.append(text(x + 44, 368, c["name"], "grotesk", 700, 46, INK))
        body.append(text(x + 44, 396, c["logic"], "inter", 500, 15, INK,
                         tracking=1.6, caps=True, opacity=0.55))

        # dark application
        ty = 430
        body.append(f'<rect x="{f(x)}" y="{ty}" width="{f(COLW)}" height="400" fill="{INK}"/>')
        body.append(mark(c, x + (COLW - 250) / 2, ty + 75, 250, DARK))
        body.append(text(x + 24, ty + 376, "ON INK  ·  PRIMARY", "inter", 500, 12, IVORY,
                         tracking=2.2, caps=True, opacity=0.5))

        # light application
        ty = 850
        body.append(f'<rect x="{f(x)}" y="{ty}" width="{f(COLW)}" height="400" fill="{IVORY}"/>')
        body.append(f'<rect x="{f(x+0.6)}" y="{f(ty+0.6)}" width="{f(COLW-1.2)}" height="398.8" '
                    f'fill="none" stroke="{SAGE}" stroke-width="1.2"/>')
        body.append(mark(c, x + (COLW - 250) / 2, ty + 75, 250, LIGHT))
        body.append(text(x + 24, ty + 376, "ON IVORY  ·  REVERSED", "inter", 500, 12, INK,
                         tracking=2.2, caps=True, opacity=0.45))

        # small sizes + circular crop
        ty = 1282
        body.append(text(x, ty + 12, "SMALL-SIZE TEST", "inter", 500, 12, INK,
                         tracking=2.2, caps=True, opacity=0.45))
        cells = [(sm, DARK, INK, 96, False) for sm in smalls] + \
                [(sm, LIGHT, IVORY, 96, False) for sm in smalls]
        cx = x
        for sm, pal, bg, box, _ in cells:
            body.append(f'<rect x="{f(cx)}" y="{ty+28}" width="{box}" height="{box}" fill="{bg}"/>')
            if bg == IVORY:
                body.append(f'<rect x="{f(cx+0.6)}" y="{f(ty+28.6)}" width="{f(box-1.2)}" height="{f(box-1.2)}" '
                            f'fill="none" stroke="{SAGE}" stroke-width="1.2"/>')
            body.append(mark(c, cx + (box - sm) / 2, ty + 28 + (box - sm) / 2, sm, pal, mono=True))
            cx += box + 10
        # circular avatar crop
        cx += 26
        cid = f"clip{slug}"
        body.append(f'<clipPath id="{cid}"><circle cx="{f(cx+48)}" cy="{f(ty+76)}" r="48"/></clipPath>')
        body.append(f'<circle cx="{f(cx+48)}" cy="{f(ty+76)}" r="48" fill="{INK}"/>')
        body.append(f'<g clip-path="url(#{cid})">{mark(c, cx, ty + 28, 96, DARK)}</g>')

        # notes
        ny = 1428
        for ln in notes[slug]:
            body.append(text(x, ny, ln, "inter", 400, 15.5, INK, opacity=0.78))
            ny += 25

    # ---- footer
    fy = 1530
    body.append(f'<rect x="{MARGIN}" y="{fy}" width="{W-2*MARGIN}" height="1.2" fill="{SAGE}"/>')
    body.append(text(MARGIN, fy + 34, "PALETTE", "inter", 500, 12, INK, tracking=2.4, caps=True, opacity=0.45))
    pal = [(INK, "INK", "#17191D", "primary dark / background"),
           (IVORY, "IVORY", "#F4F0E8", "primary light / typography"),
           (ORANGE, "SIGNAL ORANGE", "#F26A3D", "accent only"),
           (SAGE, "SAGE", "#A7B0A1", "secondary support")]
    px = MARGIN
    for hexv, name, code, role in pal:
        body.append(f'<rect x="{px}" y="{fy+52}" width="56" height="56" fill="{hexv}"/>')
        body.append(f'<rect x="{px+0.6}" y="{fy+52.6}" width="54.8" height="54.8" fill="none" '
                    f'stroke="{SAGE}" stroke-width="1.2"/>')
        body.append(text(px + 70, fy + 76, name, "inter", 600, 16, INK))
        body.append(text(px + 70, fy + 98, code, "inter", 400, 15, INK, opacity=0.55))
        px += 300
    body.append(text(W - MARGIN, fy + 76, "AWAITING OWNER APPROVAL", "inter", 600, 15, ORANGE,
                     tracking=2.2, anchor="end", caps=True))
    body.append(text(W - MARGIN, fy + 98, "No logo, avatar, banner or template has been produced yet.",
                     "inter", 400, 14, INK, anchor="end", opacity=0.55))
    body.append(text(MARGIN, fy + 156, "Construction: circular arcs on a 100 × 100 unit grid  ·  "
                     "Wordmark outlined from Space Grotesk (SIL Open Font Licence)  ·  "
                     "Vector only — no generated raster used as a master.", "inter", 400, 14, INK, opacity=0.5))

    H = fy + 200
    return svg_doc(W, H, "\n".join(body), bg=IVORY,
                   title="ODDCHAPTER — OC monogram concepts"), W, H


# ------------------------------------------------------------------ per concept
def per_concept(num, slug, c):
    d = OUT / f"concept-{num}-{slug}"
    d.mkdir(parents=True, exist_ok=True)
    S = 1024
    pad = 190
    size = S - 2 * pad
    files = {}

    files[f"concept-{num}-{slug}-dark.svg"] = svg_doc(
        S, S, mark(c, pad, pad, size, DARK), bg=INK,
        title=f"ODDCHAPTER concept {num} {c['name']} — dark background")
    files[f"concept-{num}-{slug}-light.svg"] = svg_doc(
        S, S, mark(c, pad, pad, size, LIGHT), bg=IVORY,
        title=f"ODDCHAPTER concept {num} {c['name']} — light background")
    files[f"concept-{num}-{slug}-mono.svg"] = svg_doc(
        S, S, mark(c, pad, pad, size, {"ink": INK, "orange": INK}, mono=True),
        bg=None, title=f"ODDCHAPTER concept {num} {c['name']} — single colour")

    # construction sheet
    CW, pad2 = 1200, 210
    gsize = CW - 2 * pad2
    tr, sc = place(c, pad2, pad2, gsize)
    bx0, by0, bx1, by1 = c["bbox"]
    def P(u, v):  # concept-space -> canvas space
        import re
        nums = tr.replace("translate(", "").replace(")", " ").replace("scale(", " ").split()
        tx, ty, s = float(nums[0]), float(nums[1]), float(nums[2])
        return tx + u * s, ty + v * s

    g = []
    # 10-unit grid over the drawing area
    gx0 = (int(bx0 // 10) - 1) * 10
    gx1 = (int(bx1 // 10) + 1) * 10
    for gv in range(int(gx0), int(gx1) + 1, 10):
        a, b = P(gv, by0 - 12), P(gv, by1 + 12)
        heavy = gv % 50 == 0
        g.append(f'<line x1="{f(a[0])}" y1="{f(a[1])}" x2="{f(b[0])}" y2="{f(b[1])}" '
                 f'stroke="{SAGE}" stroke-width="{"1.6" if heavy else "0.8"}" opacity="{0.55 if heavy else 0.32}"/>')
    for gv in range(int((by0 // 10 - 1) * 10), int((by1 // 10 + 2) * 10) + 1, 10):
        a, b = P(bx0 - 12, gv), P(bx1 + 12, gv)
        heavy = gv % 50 == 0
        g.append(f'<line x1="{f(a[0])}" y1="{f(a[1])}" x2="{f(b[0])}" y2="{f(b[1])}" '
                 f'stroke="{SAGE}" stroke-width="{"1.6" if heavy else "0.8"}" opacity="{0.55 if heavy else 0.32}"/>')
    # bbox + centre marks
    for (u, v) in [(bx0, by0), (bx1, by1)]:
        a = P(u, v)
        g.append(f'<line x1="{f(a[0]-14)}" y1="{f(a[1])}" x2="{f(a[0]+14)}" y2="{f(a[1])}" stroke="{ORANGE}" stroke-width="1.4"/>')
        g.append(f'<line x1="{f(a[0])}" y1="{f(a[1]-14)}" x2="{f(a[0])}" y2="{f(a[1]+14)}" stroke="{ORANGE}" stroke-width="1.4"/>')
    g.append(f'<g transform="{tr}">{mark_svg_body(c, LIGHT)}</g>')
    a, b = P(bx0, by0), P(bx1, by1)
    g.append(f'<rect x="{f(a[0])}" y="{f(a[1])}" width="{f(b[0]-a[0])}" height="{f(b[1]-a[1])}" '
             f'fill="none" stroke="{ORANGE}" stroke-width="1.4" stroke-dasharray="10 8"/>')
    for (cu, cv) in c["centres"]:
        a = P(cu, cv)
        g.append(f'<line x1="{f(a[0]-17)}" y1="{f(a[1])}" x2="{f(a[0]+17)}" y2="{f(a[1])}" '
                 f'stroke="{ORANGE}" stroke-width="1.8"/>')
        g.append(f'<line x1="{f(a[0])}" y1="{f(a[1]-17)}" x2="{f(a[0])}" y2="{f(a[1]+17)}" '
                 f'stroke="{ORANGE}" stroke-width="1.8"/>')

    cap = {"link": "Orange crosses mark the two letter centres on the 10-unit grid. The junction lens is the "
                   "intersection of two annuli — produced by fill-rule, not drawn, so it stays exact at any size.",
           "stack": "Both letters belong to one radius family (outer 22, counter 10, stroke 12). The "
                    "rule sits in the 10-unit gap, so the joint is a real space, not an overlap.",
           "cascade": "Two annuli of equal weight (outer 27, counter 14) set on a rising diagonal, meeting at "
                      "a 4-unit overlap. The accent is assigned to the open letter, so colour follows form."}[slug]
    spec = {"link": f"Drawing box {f(bx1-bx0,1)} × {f(by1-by0,1)} u  ·  outer radius 27  ·  counter 14  ·  "
                    f"stroke 13 u  ·  centres 42 u apart  ·  mouth 84°",
            "stack": f"Drawing box {f(bx1-bx0,1)} × {f(by1-by0,1)} u  ·  outer radius 22  ·  counter 10  ·  "
                     f"stroke 12 u  ·  rule 40 × 9 u  ·  mouth 76°",
            "cascade": f"Drawing box {f(bx1-bx0,1)} × {f(by1-by0,1)} u  ·  outer radius 27  ·  counter 14  ·  "
                       f"stroke 13 u  ·  centres 50 u apart  ·  overlap 4 u  ·  mouth 84°"}[slug]
    g.append(text(pad2, 96, f"{num} — {c['name']}", "grotesk", 700, 40, INK))
    g.append(text(pad2, 130, "GEOMETRIC CONSTRUCTION · 100 UNIT GRID", "inter", 600, 14, INK,
                 tracking=2.4, caps=True, opacity=0.55))
    cap_lines = wrap(cap, 104)
    for i, line in enumerate(reversed(cap_lines)):
        g.append(text(pad2, CW - 108 - i * 26, line, "inter", 400, 16, INK, opacity=0.68))
    g.append(text(pad2, CW - 62, spec, "inter", 400, 14, INK, opacity=0.5))
    g.append(text(CW - pad2, 96, "CONCEPT — NOT A FINAL ASSET", "inter", 600, 13, ORANGE,
                 tracking=2.2, caps=True, anchor="end"))
    files[f"concept-{num}-{slug}-construction.svg"] = svg_doc(CW, CW, "\n".join(g), bg=IVORY,
                                                               title=f"ODDCHAPTER concept {num} — construction")
    for name, content in files.items():
        (d / name).write_text(content)
    return d


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    doc, W, H = build_sheet()
    (OUT / "LOGO_CONCEPTS.svg").write_text(doc)
    for num, slug, c in CONCEPTS:
        per_concept(num, slug, c)
    print(f"sheet {W}x{H}; concepts written to {OUT}")


if __name__ == "__main__":
    main()
