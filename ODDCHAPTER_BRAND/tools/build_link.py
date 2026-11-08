"""
build_link.py — Phase 2.5: refinement of the approved concept 01 LINK.

Approved concept: LINK (interlock, transparent junction), owner-approved.
This script refines that concept only — no new directions.

Geometry change vs the approved concept (documented, minimal, reversible):
    centre distance 42 -> 44  (junction lens 12 -> 10 units)
    everything else identical: outer 27, counter 14, stroke 13, mouth 84 deg

Outputs
    01_LOGO/master/        LINK_MONOGRAM_MASTER.svg, LINK_PRIMARY_HORIZONTAL[_TAGLINE].svg
    01_LOGO/dark/          same, on Ink
    01_LOGO/light/         same, on Ivory
    01_LOGO/monochrome/    single-colour versions
    05_PREVIEWS/LINK_REFINEMENT.svg/.png
"""
import sys
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from oclib import (INK, IVORY, ORANGE, SAGE, ring, c_ring, mark_svg_body, place,
                   svg_doc, text, wordmark_path, f)

ROOT = HERE.parent

# ------------------------------------------------------------------ geometry
LINK23 = dict(name="LINK", bbox=(2, 23, 98, 77), centres=[(29, 50), (71, 50)])
OUTER, COUNTER, MOUTH = 27, 14, 84
DIST = 44
CX1, CX2, CY = 50 - DIST / 2, 50 + DIST / 2, 50
STROKE = OUTER - COUNTER
BX0, BY0, BX1, BY1 = CX1 - OUTER, CY - OUTER, CX2 + OUTER, CY + OUTER
W, H = BX1 - BX0, BY1 - BY0                      # 98 × 54

LINK = dict(
    name="LINK",
    parts=[dict(d=ring(CX1, CY, OUTER, COUNTER) + " " +
                c_ring(CX2, CY, OUTER, COUNTER, gap=MOUTH),
                fill="ink", rule="evenodd")],
    bbox=(BX0, BY0, BX1, BY1),
    centres=[(CX1, CY), (CX2, CY)],
)
LINK["mono"] = LINK["parts"]
LINK23_REF = dict(
    name="LINK (approved)",
    bbox=(2, 23, 98, 77),
    parts=[dict(d=ring(29, 50, 27, 14) + " " + c_ring(71, 50, 27, 14, gap=84),
                fill="ink", rule="evenodd")],
)
LINK23_REF["mono"] = LINK23_REF["parts"]

CAP = 0.7           # Space Grotesk cap height / em
MARK_CAP = 1.5      # monogram height = 1.5 x wordmark cap height
GAP_CAP = 0.62      # gap between monogram and wordmark, in cap units
TRACK = 0.02        # wordmark tracking, em


def at(cv, x, y, scale, pal, mono=False):
    """Place a concept so its bbox top-left lands exactly at (x, y), given a unit scale."""
    bx0, by0, _, _ = cv["bbox"]
    return (f'<g transform="translate({f(x - bx0 * scale)} {f(y - by0 * scale)}) '
            f'scale({f(scale, 6)})">{mark_svg_body(cv, pal, mono=mono)}</g>')


def wm(cap, color, x, cap_top, tracking=TRACK, weight=700):
    size = cap / CAP
    d, w = wordmark_path("ODDCHAPTER", "grotesk", weight, size, tracking)
    return (f'<g transform="translate({f(x)} {f(cap_top + cap)})"><path d="{d}" fill="{color}"/></g>'), w


# ------------------------------------------------------------------ builders
def monogram_parts(pal, mono=False):
    return mark_svg_body(LINK, pal, mono=mono)


def monogram_svg(bg, fg, clear=1.0, title="ODDCHAPTER OC monogram"):
    """Monogram with clear space = `clear` x stroke on all sides."""
    m = STROKE * clear
    cw, ch = W + 2 * m, H + 2 * m
    body = (f'<g transform="translate({f(m - BX0)} {f(m - BY0)})">'
            f'{mark_svg_body(LINK, {"ink": fg})}</g>')
    return svg_doc(round(cw, 3), round(ch, 3), body, bg=bg, title=title), cw, ch


def horizontal_svg(bg, fg, accent, tagline=False, title="ODDCHAPTER primary horizontal logo"):
    cap = 36.0
    mark_h = cap * MARK_CAP
    ms = mark_h / H
    gap = cap * GAP_CAP
    mark_w = W * ms
    pad = cap * 0.30

    x_wm = pad + mark_w + gap
    wpath, wwidth = wm(cap, fg, x_wm, pad)
    right = x_wm + wwidth

    extra = ""
    bottom = pad + mark_h
    if tagline:
        rule_y = pad + cap + cap * 0.52
        rt = max(1.6, cap * 0.035)
        extra += (f'<rect x="{f(x_wm)}" y="{f(rule_y)}" width="{f(wwidth)}" '
                  f'height="{f(rt)}" fill="{accent}"/>')
        tsize = cap * 0.235
        ttrack = 0.17 * tsize
        ty = rule_y + cap * 0.40
        extra += (f'<text x="{f(x_wm)}" y="{f(ty)}" font-family="Inter" font-weight="600" '
                  f'font-size="{f(tsize)}" letter-spacing="{f(ttrack)}" fill="{fg}">'
                  f'REAL STORIES. UNEXPECTED CHAPTERS.</text>')
        bottom = ty + cap * 0.10

    body = (f'{at(LINK, pad, pad, ms, {"ink": fg})}{wpath}{extra}')
    tw, th = right + pad, bottom + pad
    return svg_doc(round(tw, 2), round(th, 2), body, bg=bg, title=title), tw, th


# ------------------------------------------------------------------ sheet
def sheet():
    WD, MG = 2400, 80
    b = []

    def inner(svg):
        return svg.split("<svg", 1)[1].split(">", 1)[1].rsplit("</svg>", 1)[0]

    # header
    b.append(f'<rect x="{MG}" y="70" width="64" height="6" fill="{ORANGE}"/>')
    b.append(text(MG, 112, "ODDCHAPTER  ·  CONCEPT 01 APPROVED  ·  REFINEMENT PREVIEW", "inter", 600, 15,
                  INK, tracking=3, caps=True, opacity=0.6))
    b.append(text(MG, 200, "01 LINK — refined", "grotesk", 700, 72, INK))
    b.append(text(MG, 246, "Same concept, tightened. Nothing was redesigned; one parameter moved.",
                  "inter", 400, 24, INK, opacity=0.66))
    wmp, _ = wm(26, INK, WD - MG - 380, 88, 0.16)
    b.append(wmp)
    b.append(f'<rect x="{MG}" y="286" width="{WD-2*MG}" height="1.2" fill="{SAGE}"/>')

    # ---- A: before / after
    y = 330
    b.append(text(MG, y + 14, "A · WHAT CHANGED", "inter", 600, 13, ORANGE, tracking=2.6, caps=True))
    tw, th = 520, 264
    for i, (cv, label, sub) in enumerate([
            (LINK23_REF, "APPROVED CONCEPT", "centres 42 u apart · junction lens 12 u"),
            (LINK, "REFINED", "centres 44 u apart · junction lens 10 u")]):
        x = MG + i * (tw + 40)
        b.append(f'<rect x="{x}" y="{y+34}" width="{tw}" height="{th}" fill="{INK}"/>')
        inner_w = tw - 80
        sc = inner_w / (cv["bbox"][2] - cv["bbox"][0])
        hh = (cv["bbox"][3] - cv["bbox"][1]) * sc
        b.append(at(cv, x + 40, y + 34 + (th - hh) / 2, sc, {"ink": IVORY}))
        b.append(text(x, y + 34 + th + 26, label, "grotesk", 700, 17, INK, tracking=1.6, caps=True))
        b.append(text(x, y + 34 + th + 48, sub, "inter", 400, 15, INK, opacity=0.6))

    ax = MG + 2 * (tw + 40) + 24
    b.append(f'<path d="M {ax} {y+160} h 40 m -11 -8 l 11 8 l -11 8" stroke="{ORANGE}" '
             f'stroke-width="3" fill="none"/>')

    dx = ax + 96
    b.append(text(dx, y + 52, "CHANGE", "inter", 600, 12, INK, tracking=2.2, caps=True, opacity=0.45))
    rows = [("centre distance", "42 to 44 u"), ("junction lens", "12 to 10 u"), ("stroke", "13 u (unchanged)"),
            ("mouth", "84° (unchanged)"), ("outer / counter", "27 / 14 (unchanged)")]
    ry = y + 84
    for k, v in rows:
        b.append(text(dx, ry, k, "inter", 400, 15, INK, opacity=0.62))
        b.append(text(dx + 235, ry, v, "inter", 600, 15, INK))
        ry += 27
    note = ["Why: at 42 the lens tips came to within 1 unit",
            "of the counters, pinching the junction. At 44 the",
            "letters read separately while still interlocking."]
    for i, ln in enumerate(note):
        b.append(text(dx, ry + 24 + i * 20, ln, "inter", 400, 14, INK, opacity=0.62))

    # ---- B: construction
    y = 790
    b.append(f'<rect x="{MG}" y="{y}" width="{WD-2*MG}" height="1.2" fill="{SAGE}"/>')
    b.append(text(MG, y + 40, "B · CONSTRUCTION", "inter", 600, 13, ORANGE, tracking=2.6, caps=True))
    pw, ph = 700, 330
    b.append(f'<rect x="{MG}" y="{y+58}" width="{pw}" height="{ph}" fill="{IVORY}"/>')
    b.append(f'<rect x="{MG+0.6}" y="{y+58.6}" width="{pw-1.2}" height="{ph-1.2}" fill="none" '
             f'stroke="{SAGE}" stroke-width="1.2"/>')
    sc = (pw - 140) / W
    hh = H * sc
    mx, my = MG + 70, y + 58 + (ph - hh) / 2
    b.append(at(LINK, mx, my, sc, {"ink": INK}))
    for (cu, cv) in LINK["centres"]:
        px, py = mx + (cu - BX0) * sc, my + (cv - BY0) * sc
        b.append(f'<line x1="{f(px-16)}" y1="{f(py)}" x2="{f(px+16)}" y2="{f(py)}" stroke="{ORANGE}" stroke-width="2"/>')
        b.append(f'<line x1="{f(px)}" y1="{f(py-16)}" x2="{f(px)}" y2="{f(py+16)}" stroke="{ORANGE}" stroke-width="2"/>')
    b.append(text(MG, y + 58 + ph + 24, "dashed = protected drawing box 98 × 54 u · crosses = letter centres",
                  "inter", 400, 14, INK, opacity=0.55))

    sx = MG + pw + 70
    specs = [("outer radius", "27 u"), ("counter radius", "14 u"), ("stroke", "13 u"),
             ("centre distance", "44 u"), ("C mouth", "84°"), ("drawing box", "98 × 54 u"),
             ("junction", "fill-rule even-odd")]
    b.append(text(sx, y + 92, "PARAMETERS", "inter", 600, 12, INK, tracking=2.2, caps=True, opacity=0.45))
    ry = y + 124
    for k, v in specs:
        b.append(text(sx, ry, k, "inter", 400, 15, INK, opacity=0.62))
        b.append(text(sx + 260, ry, v, "inter", 600, 15, INK))
        ry += 26
    b.append(text(sx, ry + 24, "The junction is the mathematical intersection of two", "inter", 400, 14, INK, opacity=0.6))
    b.append(text(sx, ry + 44, "annuli — no drawn shape, so it can never drift.", "inter", 400, 14, INK, opacity=0.6))

    # ---- C: lockups
    y = 1210
    b.append(f'<rect x="{MG}" y="{y}" width="{WD-2*MG}" height="1.2" fill="{SAGE}"/>')
    b.append(text(MG, y + 40, "C · PRIMARY HORIZONTAL LOCKUP", "inter", 600, 13, ORANGE, tracking=2.6, caps=True))

    lk, lw, lh = horizontal_svg(None, IVORY, ORANGE)
    bandw, bandh = WD - 2 * MG, 280
    s1 = min(1300 / lw, (bandh - 96) / lh)
    b.append(f'<rect x="{MG}" y="{y+58}" width="{bandw}" height="{bandh}" fill="{INK}"/>')
    b.append(f'<g transform="translate({f(MG + (bandw - lw*s1)/2)} {f(y+58 + (bandh - lh*s1)/2)}) '
             f'scale({f(s1,5)})">{inner(lk)}</g>')
    b.append(text(MG + 24, y + 58 + bandh - 18, "monogram height = 1.5 × cap height · gap = 0.62 × cap",
                  "inter", 500, 13, IVORY, opacity=0.4))

    lk2, lw2, lh2 = horizontal_svg(None, INK, ORANGE, tagline=True)
    band2h = 340
    s2 = s1
    b.append(f'<rect x="{MG}" y="{y+bandh+28}" width="{bandw}" height="{band2h}" fill="{IVORY}"/>')
    b.append(f'<rect x="{MG+0.6}" y="{f(y+bandh+28.6)}" width="{bandw-1.2}" height="{band2h-1.2}" '
             f'fill="none" stroke="{SAGE}" stroke-width="1.2"/>')
    b.append(f'<g transform="translate({f(MG + (bandw - lw2*s2)/2)} {f(y+bandh+28 + (band2h - lh2*s2)/2)}) '
             f'scale({f(s2,5)})">{inner(lk2)}</g>')
    b.append(text(MG + 24, y + bandh + 28 + band2h - 18,
                  "tagline: Inter SemiBold · +0.17 em · rule above is the only accent",
                  "inter", 500, 13, INK, opacity=0.4))

    # ---- D: sizes + clear space
    y = 1900
    b.append(f'<rect x="{MG}" y="{y}" width="{WD-2*MG}" height="1.2" fill="{SAGE}"/>')
    b.append(text(MG, y + 40, "D · SMALL SIZES & CLEAR SPACE", "inter", 600, 13, ORANGE, tracking=2.6, caps=True))

    m = STROKE
    cwid, chgt = W + 2 * m, H + 2 * m
    s = 250 / max(cwid, chgt)
    bx, by = MG, y + 60
    b.append(f'<rect x="{f(bx)}" y="{f(by)}" width="{f(cwid*s)}" height="{f(chgt*s)}" fill="none" '
             f'stroke="{ORANGE}" stroke-width="1.4" stroke-dasharray="8 6"/>')
    b.append(f'<rect x="{f(bx + m*s)}" y="{f(by + m*s)}" width="{f(W*s)}" height="{f(H*s)}" fill="none" '
             f'stroke="{SAGE}" stroke-width="1.2"/>')
    b.append(at(LINK, bx + m * s, by + m * s, s, {"ink": INK}))
    b.append(text(MG, by + chgt * s + 26, "clear space = 1 × stroke (13 u) on all four sides",
                  "inter", 400, 14, INK, opacity=0.62))

    sxs = MG + 430
    for px in (160, 96, 48, 32, 24):
        sc3 = px / H
        wpx = W * sc3
        ty = by + (160 - px) / 2
        b.append(f'<rect x="{f(sxs)}" y="{f(ty)}" width="{f(wpx)}" height="{px}" fill="{INK}"/>')
        b.append(at(LINK, sxs, ty, sc3, {"ink": IVORY}))
        b.append(text(sxs + wpx / 2, by + 160 + 24, f"{px} px high", "inter", 500, 12, INK,
                      anchor="middle", opacity=0.55))
        sxs += wpx + 40

    b.append(text(MG, by + 236, "Minimum digital size: 32 px high for the monogram; 24 px is the hard floor.",
                  "inter", 400, 15, INK, opacity=0.7))
    b.append(text(MG, by + 260, "Minimum print size: 8 mm wide. In favicon-less contexts the junction is the first thing to go — expected, not a defect.",
                  "inter", 400, 15, INK, opacity=0.7))

    fy = by + 330
    b.append(f'<rect x="{MG}" y="{fy}" width="{WD-2*MG}" height="1.2" fill="{SAGE}"/>')
    b.append(text(MG, fy + 36, "STATUS", "inter", 600, 12, INK, tracking=2.2, caps=True, opacity=0.45))
    b.append(text(MG, fy + 62, "Refined preview only. No YouTube, social, thumbnail or motion asset has been produced yet.",
                  "inter", 400, 16, INK, opacity=0.72))
    b.append(text(WD - MG, fy + 36, "AWAITING APPROVAL OF THE REFINEMENT", "inter", 600, 14, ORANGE,
                  tracking=2.2, anchor="end", caps=True))
    b.append(text(WD - MG, fy + 62, "vector masters · no raster master · wordmark outlined",
                  "inter", 400, 14, INK, anchor="end", opacity=0.5))

    return svg_doc(WD, fy + 110, "\n".join(b), bg=IVORY, title="ODDCHAPTER — LINK refinement preview"), WD, fy + 110


def main():
    for d in ("01_LOGO/master", "01_LOGO/dark", "01_LOGO/light", "01_LOGO/monochrome", "05_PREVIEWS"):
        (ROOT / d).mkdir(parents=True, exist_ok=True)

    outs = {
        "01_LOGO/master/LINK_MONOGRAM_MASTER.svg": monogram_svg(None, INK)[0],
        "01_LOGO/dark/LINK_MONOGRAM_DARK.svg": monogram_svg(INK, IVORY)[0],
        "01_LOGO/light/LINK_MONOGRAM_LIGHT.svg": monogram_svg(IVORY, INK)[0],
        "01_LOGO/monochrome/LINK_MONOGRAM_MONO.svg": monogram_svg(None, INK)[0],
        "01_LOGO/master/LINK_PRIMARY_HORIZONTAL.svg": horizontal_svg(None, INK, ORANGE)[0],
        "01_LOGO/dark/LINK_PRIMARY_HORIZONTAL_DARK.svg": horizontal_svg(INK, IVORY, ORANGE)[0],
        "01_LOGO/light/LINK_PRIMARY_HORIZONTAL_LIGHT.svg": horizontal_svg(IVORY, INK, ORANGE)[0],
        "01_LOGO/monochrome/LINK_PRIMARY_HORIZONTAL_MONO.svg": horizontal_svg(None, INK, INK)[0],
        "01_LOGO/master/LINK_PRIMARY_HORIZONTAL_TAGLINE.svg": horizontal_svg(None, INK, ORANGE, tagline=True)[0],
        "01_LOGO/dark/LINK_PRIMARY_HORIZONTAL_TAGLINE_DARK.svg": horizontal_svg(INK, IVORY, ORANGE, tagline=True)[0],
    }
    for path, content in outs.items():
        (ROOT / path).write_text(content)

    doc, w, h = sheet()
    (ROOT / "05_PREVIEWS/LINK_REFINEMENT.svg").write_text(doc)
    print(f"wrote {len(outs)} masters + refinement sheet {w}x{h}")


if __name__ == "__main__":
    main()
