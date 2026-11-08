"""
build_motion.py — Phase 7: the motion build as an actual artefact.

 04_MOTION/preview/OPENER_BUILD_960x540.gif     38 frames @ 25 fps, 1.5 s
 04_MOTION/preview/OPENER_POSTER_1920x1080.png  final state at 1.2 s, full size
 04_MOTION/preview/OPENER_ANIMATED.svg          the same build as SMIL, self-contained

The timing here is the spec in MOTION_IDENTITY.md — if one changes, the other must too.

Easing is cubic-bezier(.2, .7, .2, 1) everywhere except the rule, which is linear.
"""
import math
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import brand
from brand import INK, IVORY, ORANGE, SAGE, MW, MH, IX0, IX1, monogram, svg_doc, f

ROOT = brand.ROOT
W, H = 1920, 1080
FPS = 25
DUR_MS = 1500
LOCKUP_W = 1200

# ------------------------------------------------------------------ timing
T_MONO, T_MONO_END = 0, 180
T_WORD, T_WORD_END = 300, 540
T_RULE, T_RULE_END = 540, 720
T_TAG, T_TAG_END = 720, 900


def _bezier(t, p1, p2, p3, p4):
    return (3 * (1 - t) ** 2 * t * p1 + 3 * (1 - t) * t ** 2 * p2 + t ** 3 * p3
            + (1 - t) ** 3 * p4)


def ease(x):
    """cubic-bezier(.2,.7,.2,1) — solve for y given x by bisection."""
    x = min(max(x, 0.0), 1.0)
    lo, hi = 0.0, 1.0
    for _ in range(24):
        mid = (lo + hi) / 2
        if _bezier(mid, 0.2, 0.7, 0.2, 1.0) is None:
            break
        # x(t) uses the x control points .2 and .2
        xt = 3 * (1 - mid) ** 2 * mid * 0.2 + 3 * (1 - mid) * mid ** 2 * 0.2 + mid ** 3
        if xt < x:
            lo = mid
        else:
            hi = mid
    t = (lo + hi) / 2
    return 3 * (1 - t) ** 2 * t * 0.7 + 3 * (1 - t) * t ** 2 * 1.0 + t ** 3


def ramp(t, a, b):
    if t <= a:
        return 0.0
    if t >= b:
        return 1.0
    return (t - a) / (b - a)


# ------------------------------------------------------------------ geometry
CAP = 36.0
MS = (CAP * brand.MARK_TO_CAP) / MH
MARK_W = MW * MS
GAP = CAP * brand.GAP_TO_CAP
X_WM = MARK_W + GAP
WM_SVG, WM_W = brand.wordmark(CAP, IVORY, X_WM, 0)
RULE_Y = CAP + CAP * 0.52
TAG_Y = RULE_Y + CAP * 0.40
TOTAL_W = X_WM + WM_W
TOTAL_H = TAG_Y + CAP * 0.10
LSC = LOCKUP_W / TOTAL_W
OX = (W - TOTAL_W * LSC) / 2
OY = (H - TOTAL_H * LSC) / 2

# ink centre of the monogram in frame coordinates (scaling pivots here)
MONO_CX = OX + (IX0 + IX1) / 2 * MS * LSC
MONO_CY = OY + 50 * MS * LSC
TAG_SVG, TAG_W = brand.tagline_outline(CAP * 0.235, IVORY, X_WM, TAG_Y)


def state(t):
    e_mono = ease(ramp(t, T_MONO, T_MONO_END))
    e_word = ease(ramp(t, T_WORD, T_WORD_END))
    p_rule = ramp(t, T_RULE, T_RULE_END)          # linear by spec
    e_tag = ease(ramp(t, T_TAG, T_TAG_END))
    return {
        "mono_scale": 0.92 + 0.08 * e_mono,
        "mono_opacity": e_mono,
        "word": e_word,
        "rule": p_rule,
        "tag_opacity": e_tag,
        "tag_rise": (1 - e_tag) * 12,
    }


def frame(t, width=W):
    s = state(t)
    sc = LSC * (width / W)
    ox, oy = OX * (width / W), OY * (width / W)
    h = H * (width / W)

    g = [f'<rect width="{width}" height="{f(h)}" fill="{INK}"/>']
    g.append(f'<g transform="translate({f(ox)} {f(oy)}) scale({f(sc,6)})">')

    # monogram, scaled about its own ink centre
    cx, cy = (MONO_CX - OX) , (MONO_CY - OY)
    g.append(f'<g opacity="{f(s["mono_opacity"],4)}" '
             f'transform="translate({f(cx)} {f(cy)}) scale({f(s["mono_scale"],6)}) '
             f'translate({f(-cx)} {f(-cy)})">')
    g.append(monogram(0, 0, MS, IVORY))
    g.append('</g>')

    # wordmark wipe
    if s["word"] > 0:
        g.append(f'<clipPath id="wipe"><rect x="{f(X_WM-8)}" y="-40" '
                 f'width="{f(WM_W*s["word"]+8)}" height="{f(TOTAL_H+80)}"/></clipPath>')
        g.append(f'<g clip-path="url(#wipe)">{WM_SVG}</g>')

    # rule
    if s["rule"] > 0:
        g.append(f'<rect x="{f(X_WM)}" y="{f(RULE_Y)}" width="{f(WM_W*s["rule"])}" '
                 f'height="{f(max(1.6, CAP*0.035))}" fill="{ORANGE}"/>')

    # tagline
    if s["tag_opacity"] > 0:
        g.append(f'<g opacity="{f(s["tag_opacity"],4)}" transform="translate(0 {f(s["tag_rise"])})">'
                 f'{TAG_SVG}</g>')
    g.append('</g>')
    return svg_doc(width, round(h, 2), "\n".join(g), bg=None,
                   title=f"ODDCHAPTER — opener frame t={t} ms")


# ------------------------------------------------------------------ SMIL
def animated_svg():
    """Self-contained SMIL build. Holds forever on the final state."""
    dur = f"{DUR_MS} ms"
    k = lambda ms: f"{ms / DUR_MS:.4f}"
    g = [f'<rect width="{W}" height="{H}" fill="{INK}"/>',
         f'<g transform="translate({f(OX)} {f(OY)}) scale({f(LSC,6)})">']

    # monogram — scale and opacity, 0..180 ms
    g.append(f'<g opacity="1" transform="translate({f(MONO_CX-OX)} {f(MONO_CY-OY)})">')
    g.append('<g>')
    g.append(f'<animateTransform attributeName="transform" type="scale" '
             f'values="0.92;1" keyTimes="0;{k(T_MONO_END)}" dur="{dur}" fill="freeze" '
             f'calcMode="spline" keySplines="0.2 0.7 0.2 1"/>')
    g.append('<animate attributeName="opacity" from="0" to="1" '
             f'keyTimes="0;{k(T_MONO_END)}" dur="{dur}" fill="freeze" '
             f'calcMode="spline" keySplines="0.2 0.7 0.2 1"/>')
    g.append(f'<g transform="translate({f(-(MONO_CX-OX))} {f(-(MONO_CY-OY))})">')
    g.append(monogram(0, 0, MS, IVORY))
    g.append('</g></g></g>')

    # wordmark clip wipe
    g.append(f'<clipPath id="smil-wipe"><rect x="{f(X_WM-8)}" y="-40" width="0" '
             f'height="{f(TOTAL_H+80)}">'
             f'<animate attributeName="width" from="0" to="{f(WM_W+8)}" begin="{T_WORD}ms" '
             f'dur="{T_WORD_END-T_WORD}ms" fill="freeze" calcMode="spline" '
             f'keySplines="0.2 0.7 0.2 1" keyTimes="0;1"/>'
             f'</rect></clipPath>')

    g.append(f'<g clip-path="url(#smil-wipe)">{WM_SVG}</g>')

    # rule (linear)
    g.append(f'<rect x="{f(X_WM)}" y="{f(RULE_Y)}" width="0" height="{f(max(1.6, CAP*0.035))}" fill="{ORANGE}">'
             f'<animate attributeName="width" from="0" to="{f(WM_W)}" begin="{T_RULE}ms" '
             f'dur="{T_RULE_END-T_RULE}ms" fill="freeze" calcMode="linear"/></rect>')

    # tagline
    g.append(f'<g opacity="0" transform="translate(0 12)">')
    g.append(f'<animate attributeName="opacity" from="0" to="1" begin="{T_TAG}ms" '
             f'dur="{T_TAG_END-T_TAG}ms" fill="freeze" calcMode="spline" keySplines="0.2 0.7 0.2 1"/>')
    g.append(f'<animateTransform attributeName="transform" type="translate" from="0 12" to="0 0" '
             f'begin="{T_TAG}ms" dur="{T_TAG_END-T_TAG}ms" fill="freeze" calcMode="spline" '
             f'keySplines="0.2 0.7 0.2 1"/>')
    g.append(f'{TAG_SVG}</g>')

    g.append('</g>')
    return svg_doc(W, H, "\n".join(g), bg=None,
                   title="ODDCHAPTER — opener (SMIL, 1.5 s, holds on final state)")


# ------------------------------------------------------------------ render
def render_frames(tmp=Path("/tmp/opener_frames")):
    tmp.mkdir(parents=True, exist_ok=True)
    for p in tmp.glob("*.png"):
        p.unlink()
    n = int(round(DUR_MS / 1000 * FPS))
    for i in range(n):
        t = i * (1000 / FPS)
        svg = tmp / f"f{i:03d}.svg"
        svg.write_text(frame(t, 960))
        subprocess.run(["node", str(HERE / "render.mjs"), str(svg), str(tmp / f"f{i:03d}.png"),
                        "960", "none"], check=True, capture_output=True)
    print(f"rendered {n} frames")
    return tmp, n


def main():
    out = ROOT / "04_MOTION/preview"
    out.mkdir(parents=True, exist_ok=True)

    (out / "OPENER_ANIMATED.svg").write_text(animated_svg())
    print("wrote 04_MOTION/preview/OPENER_ANIMATED.svg")

    # poster: final state at full size
    poster_svg = Path("/tmp/opener_poster.svg")
    poster_svg.write_text(frame(1200, W))
    subprocess.run(["node", str(HERE / "render.mjs"), str(poster_svg),
                    str(out / "OPENER_POSTER_1920x1080.png"), str(W), "none"], check=True)
    print("wrote 04_MOTION/preview/OPENER_POSTER_1920x1080.png")

    tmp, n = render_frames()
    gif = out / "OPENER_BUILD_960x540.gif"
    subprocess.run(["convert", "-delay", str(int(100 / FPS)), "-dispose", "previous"]
                   + [str(tmp / f"f{i:03d}.png") for i in range(n)]
                   + ["-loop", "0", "-layers", "Optimize", str(gif)], check=True)
    print("wrote", gif.relative_to(ROOT), f"{gif.stat().st_size/1024:.0f} KB")


if __name__ == "__main__":
    main()
