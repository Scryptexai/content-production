"""
build_sheets.py — presentation sheets for Phases 5 and 6.

 04_MOTION/animation_reference/ANIMATION_STORYBOARD.svg   timing + frames
 05_PREVIEWS/USAGE_DO_DONT.svg                            correct / incorrect usage
 05_PREVIEWS/CONTACT_SHEET.svg                            the whole system at a glance

Sheets are documentation: they may contain <text>. The logo files themselves never do.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import brand
from brand import (INK, IVORY, ORANGE, SAGE, MW, MH, MONO_PATH, monogram, lockup,
                   svg_doc, text, f, wordmark)

ROOT = brand.ROOT
CAP = 0.7


def write(path, content):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content)
    print("wrote", path)


def fit_lockup(width, colors, tagline=False):
    body, w, h = lockup(colors=colors, tagline=tagline)
    sc = width / w
    return f'<g transform="scale({f(sc,6)})">{body}</g>', w * sc, h * sc


# ------------------------------------------------------------------ 1. motion
FRAMES = [
    ("00:00.00", "0 ms", "Monogram draws", "O ring and C arc scale in from 92 % to 100 % together, "
     "opacity 0 to 100. Duration 180 ms, cubic-bezier(.2,.7,.2,1)."),
    ("00:00.18", "180 ms", "Junction locks", "Both layers land. No bounce, no overshoot — the mark is "
     "a fact, not a trick. Hold 120 ms."),
    ("00:00.30", "300 ms", "Wordmark wipes in", "ODDCHAPTER reveals left to right behind a clip path, "
     "240 ms. The monogram does not move."),
    ("00:00.54", "540 ms", "Accent rule draws", "The orange rule grows from 0 to 100 % width in 180 ms, "
     "left to right. This is the only colour that animates."),
    ("00:00.72", "720 ms", "Tagline fades up", "Tagline rises 12 px and fades in over 180 ms. "
     "End state is the approved lockup, pixel-identical to the static master."),
    ("00:00.90", "900 ms", "Hold, then cut", "Hold the finished lockup for 300 ms. Cut to the opening "
     "scene — no zoom, no dissolve, no logo build."),
]


def storyboard():
    W, PAD = 2400, 80
    cols, cellw, gap, pitch = 3, 720, 40, 640
    b = [text(PAD, 92, "ODDCHAPTER — MOTION STORYBOARD", "grotesk", 700, 44, INK),
         text(PAD, 126, "1.2 seconds, six states, one cut. Nothing else is needed.",
              "inter", 400, 18, INK, opacity=0.65)]

    # lockup parts, built once so each frame draws an exact subset
    cap = 36.0
    ms = (cap * brand.MARK_TO_CAP) / MH
    mark_w = MW * ms
    gapx = cap * brand.GAP_TO_CAP
    x_wm = mark_w + gapx
    wm_svg, wm_w = brand.wordmark(cap, IVORY, x_wm, 0)
    rule_y = cap + cap * 0.52
    tag_y = rule_y + cap * 0.40
    total_w = x_wm + wm_w
    total_h = tag_y + cap * 0.10

    frames = [
        (0.0, "Monogram draws", "Scale 92 to 100 %, opacity 0 to 100. 180 ms, cubic-bezier(.2,.7,.2,1).",
         dict(mono_op=0.55, mono_sc=0.94)),
        (180, "Junction locks", "Both letters land together. No bounce, no overshoot. Hold 120 ms.",
         dict(mono_op=1.0, mono_sc=1.0)),
        (300, "Wordmark wipes in", "ODDCHAPTER reveals left to right behind a clip path. 240 ms. The monogram does not move.",
         dict(word=0.55)),
        (540, "Accent rule draws", "The orange rule grows 0 to 100 % width in 180 ms. The only colour that animates.",
         dict(word=1.0, rule=1.0)),
        (720, "Tagline fades up", "Tagline rises 12 px and fades in over 180 ms. Ends on the approved lockup.",
         dict(word=1.0, rule=1.0, tag=0.6)),
        (900, "Hold, then cut", "Hold the finished lockup 300 ms, then cut to the opening scene — no dissolve, no logo build.",
         dict(word=1.0, rule=1.0, tag=1.0)),
    ]

    for i, (tms, title, note, state) in enumerate(frames):
        r, c = divmod(i, cols)
        x = PAD + c * (cellw + gap)
        y = 190 + r * pitch
        b.append(text(x, y, f"{i+1:02d}", "grotesk", 700, 20, ORANGE))
        b.append(text(x + 40, y, title, "grotesk", 700, 22, INK))
        b.append(text(x + 40, y + 22, f"00:00.{int(tms):02d}" if tms < 1000 else "00:00.90",
                      "inter", 500, 13, INK, opacity=0.5))

        pw = cellw
        ph = cellw * 9 / 16
        b.append(f'<rect x="{x}" y="{y+36}" width="{pw}" height="{f(ph)}" fill="{INK}"/>')

        lsc = (pw * 0.80) / total_w
        ox = x + (pw - total_w * lsc) / 2
        oy = y + 36 + (ph - total_h * lsc) / 2

        parts = []
        parts.append(f'<g transform="translate({f(ox)} {f(oy)}) scale({f(lsc,6)})">')
        msc = state.get("mono_sc", 1.0)
        mop = state.get("mono_op", 1.0)
        # monogram (scales about its own centre)
        parts.append(f'<g opacity="{mop}" transform="translate({f(MW*(1-msc)/2*ms)} {f(MH*(1-msc)/2*ms)}) '
                     f'scale({msc})">{brand.monogram(0, 0, ms, IVORY)}</g>')
        word = state.get("word", 0.0)
        if word > 0:
            cid = f"w{i}"
            parts.append(f'<clipPath id="{cid}"><rect x="{f(x_wm-4)}" y="-40" '
                         f'width="{f(wm_w*word+4)}" height="{f(total_h+80)}"/></clipPath>')
            parts.append(f'<g clip-path="url(#{cid})">{wm_svg}</g>')
        rule = state.get("rule", 0.0)
        if rule > 0:
            parts.append(f'<rect x="{f(x_wm)}" y="{f(rule_y)}" width="{f(wm_w*rule)}" '
                         f'height="{f(max(1.6, cap*0.035))}" fill="{ORANGE}"/>')
        tag = state.get("tag", 0.0)
        if tag > 0:
            parts.append(f'<g opacity="{tag}" transform="translate(0 {f((1-tag)*12)})">'
                         f'<text x="{f(x_wm)}" y="{f(tag_y)}" font-family="Inter" font-weight="600" '
                         f'font-size="{f(cap*0.235)}" letter-spacing="{f(0.17*cap*0.235)}" '
                         f'fill="{IVORY}">{brand.TAGLINE}</text></g>')
        parts.append('</g>')
        b.append("".join(parts))

        # wrapped note
        lines, line = [], ""
        for wd in note.split():
            if len(line) + len(wd) + 1 > 58:
                lines.append(line); line = wd
            else:
                line = (line + " " + wd).strip()
        lines.append(line)
        for j, ln in enumerate(lines[:3]):
            b.append(text(x, y + 36 + ph + 40 + j * 20, ln, "inter", 400, 14, INK, opacity=0.68))

    rows = (len(frames) + cols - 1) // cols
    fy = 190 + rows * pitch + 10
    b.append(f'<rect x="{PAD}" y="{fy}" width="{W-2*PAD}" height="1.2" fill="{SAGE}"/>')
    b.append(text(PAD, fy + 34, "SPEC", "inter", 600, 12, INK, tracking=2.4, caps=True, opacity=0.45))
    specs = ["Canvas 1920 × 1080 · 25 fps · keep the build inside the central 5 % safe margin",
             "Total build 1.2 s, hold 0.3 s, then cut — never dissolve into the opening scene",
             "Easing: cubic-bezier(.2,.7,.2,1) for entrances; linear for the rule only",
             "Orange animates once (the rule). Nothing else changes colour.",
             "Layers: O ring · C arc · wordmark · rule · tagline — see 04_MOTION/svg_components"]
    for i, sp in enumerate(specs):
        b.append(text(PAD, fy + 64 + i * 22, sp, "inter", 400, 15, INK, opacity=0.72))
    return svg_doc(W, fy + 200, "\n".join(b), bg=IVORY, title="ODDCHAPTER — motion storyboard")


# ------------------------------------------------------------------ 2. usage
def usage_sheet():
    W, PAD = 2400, 80
    cellw, cellh, gap = 540, 300, 30
    b = [text(PAD, 92, "LOGO USAGE — CORRECT AND INCORRECT", "grotesk", 700, 42, INK),
         text(PAD, 126, "Sage panels are allowed. Orange panels are not, and each one states why.",
              "inter", 400, 17, INK, opacity=0.65)]

    def frame(x, y, w, h, bg, ok, label, reason):
        g = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{bg}"/>']
        g.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="{SAGE if ok else ORANGE}" stroke-width="1.4"/>')
        c = SAGE if ok else ORANGE
        g.append(f'<rect x="{x}" y="{y}" width="6" height="{h}" fill="{c}"/>')
        g.append(text(x + 24, y + h + 24, ("ALLOWED — " if ok else "NOT ALLOWED — ") + label,
                      "inter", 600, 13, c, tracking=1.6, caps=True))
        g.append(text(x + 24, y + h + 45, reason, "inter", 400, 14, INK, opacity=0.62))
        return "\n".join(g)

    def lk(width, colors, tagline=False):
        body, w, h = lockup(colors=colors, tagline=tagline)
        sc = width / w
        return f'<g transform="scale({f(sc,6)})">{body}</g>', w * sc, h * sc

    def place(x, y, w, h, body, extra=""):
        return f'<g transform="translate({f(x)} {f(y)})">{body}{extra}</g>'

    y = 190
    # ---- row 1: colour
    specs = [
        (INK, True, "IVORY ON INK", "The default. Highest contrast, best for video.",
         dict(width=400, colors={"word": IVORY, "accent": ORANGE})),
        (IVORY, True, "INK ON IVORY", "The reversed default for light pages and print.",
         dict(width=400, colors={"word": INK, "accent": ORANGE})),
        (INK, False, "ORANGE WORDMARK", "Orange is an accent at 5.79:1 — as a wordmark it stops being one.",
         dict(width=400, colors={"word": ORANGE, "accent": ORANGE})),
        (INK, False, "OUTSIDE THE PALETTE", "No colour enters the identity that is not one of the four tokens.",
         dict(width=400, colors={"word": "#4A7CF2", "accent": "#4A7CF2"})),
    ]
    x = PAD
    for bg, ok, label, reason, kw in specs:
        g, w, h = lk(kw["width"], kw["colors"])
        b.append(frame(x, y, cellw, cellh, bg, ok, label, reason))
        b.append(place(x + (cellw - w) / 2, y + (cellh - h) / 2, w, h, g))
        x += cellw + gap

    # ---- row 2: geometry
    y += cellh + 96
    x = PAD
    g, w, h = lk(400, {"word": IVORY, "accent": ORANGE})
    b.append(frame(x, y, cellw, cellh, INK, True, "PROPORTIONS LOCKED", "Monogram 1.5 × cap, gap 0.62 × cap. Scale only uniformly."))
    b.append(place(x + (cellw - w) / 2, y + (cellh - h) / 2, w, h, g))

    x += cellw + gap
    g2, w2, h2 = lk(250, {"word": IVORY, "accent": ORANGE})
    b.append(frame(x, y, cellw, cellh, INK, False, "STRETCHED", "Never scale non-uniformly — circles become ellipses."))
    b.append(f'<g transform="translate({f(x + cellw/2 - w2*1.55/2)} {f(y + (cellh-h2)/2)}) scale(1.55 1)">{g2}</g>')

    x += cellw + gap
    g3, w3, h3 = lk(330, {"word": IVORY, "accent": ORANGE})
    b.append(frame(x, y, cellw, cellh, INK, False, "ROTATED", "The lockup is horizontal. Rotation reads as a sticker, not a logo."))
    b.append(f'<g transform="translate({f(x + cellw/2)} {f(y + cellh/2)}) rotate(-8) translate({f(-w3/2)} {f(-h3/2)})">{g3}</g>')

    x += cellw + gap
    g4, w4, h4 = lk(360, {"word": IVORY, "accent": ORANGE})
    b.append(frame(x, y, cellw, cellh, INK, False, "SYMBOL ADDED", "No play button, book, eye or camera. The monogram is the whole mark."))
    cx, cy = x + cellw / 2, y + cellh / 2
    b.append(place(cx - w4 / 2, cy - h4 / 2, w4, h4, g4))
    b.append(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="126" fill="none" stroke="{SAGE}" stroke-width="2" opacity="0.45"/>')
    b.append(f'<circle cx="{f(cx + w4/2 + 46)}" cy="{f(cy)}" r="26" fill="{ORANGE}" opacity="0.85"/>')
    b.append(f'<polygon points="{f(cx + w4/2 + 39)},{f(cy-11)} {f(cx + w4/2 + 39)},{f(cy+11)} {f(cx + w4/2 + 56)},{f(cy)}" fill="{INK}"/>')

    # ---- row 3: space and size
    y += cellh + 96
    x = PAD
    g, w, h = lk(230, {"word": IVORY, "accent": ORANGE})
    bar = 230 * (13 / 98)
    bw, bh = w + 2 * bar, h + 2 * bar
    b.append(frame(x, y, cellw, cellh, INK, True, "CLEAR SPACE", "At least one stroke width of the monogram on every side."))
    b.append(f'<rect x="{f(x + cellw/2 - bw/2)}" y="{f(y + cellh/2 - bh/2)}" width="{f(bw)}" height="{f(bh)}" '
             f'fill="none" stroke="{SAGE}" stroke-width="1" stroke-dasharray="8 6" opacity="0.7"/>')
    b.append(place(x + cellw / 2 - w / 2, y + cellh / 2 - h / 2, w, h, g))

    x += cellw + gap
    g, w, h = lk(330, {"word": IVORY, "accent": ORANGE})
    b.append(frame(x, y, cellw, cellh, INK, False, "CROWDED", "Anything closer than the clear space breaks the mark."))
    b.append(place(x + 24, y + cellh / 2 - h / 2, w, h, g))
    b.append(text(x + 24 + w + 6, y + cellh / 2 - 6, "TEKS", "inter", 700, 20, IVORY))
    b.append(text(x + 24 + w + 6, y + cellh / 2 + 22, "MENEMPEL", "inter", 400, 18, IVORY))

    x += cellw + gap
    g, w, h = lk(200, {"word": IVORY, "accent": ORANGE}, tagline=True)
    b.append(frame(x, y, cellw, cellh, INK, True, "MINIMUM SIZE", "32 px monogram · 240 px lockup · 420 px with tagline."))
    b.append(place(x + cellw / 2 - w / 2, y + cellh / 2 - h / 2, w, h, g))

    x += cellw + gap
    g, w, h = lk(84, {"word": IVORY, "accent": ORANGE}, tagline=True)
    b.append(frame(x, y, cellw, cellh, INK, False, "TOO SMALL", "Below the floor the junction closes and the tagline turns to noise."))
    b.append(place(x + cellw / 2 - w / 2, y + cellh / 2 - h / 2, w, h, g))

    return svg_doc(W, y + cellh + 130, "\n".join(b), bg=IVORY, title="ODDCHAPTER — logo usage")


# ------------------------------------------------------------------ 3. contact
def contact_sheet():
    import base64

    def img(path, x, y, w, h):
        f_ = ROOT / path
        if not f_.exists():
            return ""
        data = base64.b64encode(f_.read_bytes()).decode()
        return (f'<image x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" '
                f'href="data:image/png;base64,{data}" preserveAspectRatio="xMidYMid meet"/>')

    W, PAD = 2600, 80
    b = [text(PAD, 96, "ODDCHAPTER — BRAND SYSTEM", "grotesk", 700, 64, INK),
         text(PAD, 140, "One geometry, every surface. Every asset is generated from tools/brand.py.",
              "inter", 400, 21, INK, opacity=0.66)]
    wsvg, _ = wordmark(22, INK, W - PAD - 330, 68, 0.16)
    b.append(wsvg)

    # 1 · hero
    y = 200
    b.append(f'<rect x="{PAD}" y="{y}" width="{W-2*PAD}" height="300" fill="{INK}"/>')
    lk, lw, lh = fit_lockup(1100, {"word": IVORY, "accent": ORANGE}, tagline=True)
    b.append(f'<g transform="translate({f(W/2-lw/2)} {f(y + (300-lh)/2)})">{lk}</g>')

    # 2 · marks
    y = 560
    tiles = [("AVATAR 800 × 800", "02_YOUTUBE/avatar/YOUTUBE_AVATAR_800.png"),
             ("PROFILE 1024 × 1024", "03_SOCIAL/profile/SOCIAL_PROFILE_1024.png"),
             ("MONOGRAM — REVERSED", "01_LOGO/dark/MONOGRAM_DARK_1200.png"),
             ("WATERMARK 800", "02_YOUTUBE/watermark/WATERMARK_LIGHT_800.png")]
    b.append(text(PAD, y - 18, "MARKS", "inter", 600, 12, INK, tracking=2.4, caps=True, opacity=0.45))
    tw = (W - 2 * PAD - 3 * 30) / 4
    for i, (label, path) in enumerate(tiles):
        x = PAD + i * (tw + 30)
        b.append(f'<rect x="{f(x)}" y="{f(y)}" width="{f(tw)}" height="{f(tw)}" fill="{INK}"/>')
        b.append(img(path, x, y, tw, tw))
        b.append(text(x, y + tw + 24, label, "inter", 500, 12, INK, tracking=1.8, caps=True, opacity=0.5))

    # 3 · banner
    y += tw + 90
    b.append(text(PAD, y - 18, "YOUTUBE BANNER 2560 × 1440", "inter", 600, 12, INK, tracking=2.4, caps=True, opacity=0.45))
    bw = 1500
    bh = bw * 9 / 16
    bx = W / 2 - bw / 2
    b.append(f'<rect x="{f(bx)}" y="{f(y)}" width="{f(bw)}" height="{f(bh)}" fill="{INK}"/>')
    b.append(img("02_YOUTUBE/banner/YOUTUBE_BANNER_2560x1440.png", bx, y, bw, bh))
    b.append(f'<rect x="{f(bx)}" y="{f(y)}" width="{f(bw)}" height="{f(bh)}" fill="none" stroke="{SAGE}" stroke-width="1" opacity="0.4"/>')

    # 4 · thumbnails
    y += bh + 90
    b.append(text(PAD, y - 18, "THUMBNAIL SYSTEMS", "inter", 600, 12, INK, tracking=2.4, caps=True, opacity=0.45))
    tw3 = (W - 2 * PAD - 2 * 30) / 3
    for i, name in enumerate(["TEMPLATE_01_PERISTIWA", "TEMPLATE_02_BERTAHAN_HIDUP", "TEMPLATE_03_SAINS_ANEH"]):
        x = PAD + i * (tw3 + 30)
        b.append(f'<rect x="{f(x)}" y="{f(y)}" width="{f(tw3)}" height="{f(tw3*9/16)}" fill="{INK}"/>')
        b.append(img(f"02_YOUTUBE/thumbnails/{name}.png", x, y, tw3, tw3 * 9 / 16))

    # 5 · palette
    y3 = y + tw3 * 9 / 16 + 90
    b.append(f'<rect x="{PAD}" y="{y3}" width="{W-2*PAD}" height="1.2" fill="{SAGE}"/>')
    px = PAD
    for hexv, name, code in [(INK, "INK", "#17191D"), (IVORY, "IVORY", "#F4F0E8"),
                             (ORANGE, "SIGNAL ORANGE", "#F26A3D"), (SAGE, "SAGE", "#A7B0A1")]:
        b.append(f'<rect x="{px}" y="{y3+40}" width="60" height="60" fill="{hexv}"/>')
        b.append(f'<rect x="{px+0.6}" y="{f(y3+40.6)}" width="58.8" height="58.8" fill="none" stroke="{SAGE}" stroke-width="1.2"/>')
        b.append(text(px + 76, y3 + 66, name, "inter", 600, 15, INK))
        b.append(text(px + 76, y3 + 88, code, "inter", 400, 14, INK, opacity=0.55))
        px += 420
    b.append(text(W - PAD, y3 + 66, "SPACE GROTESK · INTER", "inter", 600, 15, INK, anchor="end", opacity=0.7))
    b.append(text(W - PAD, y3 + 88, "SIL OFL 1.1", "inter", 400, 14, INK, anchor="end", opacity=0.5))
    return svg_doc(W, y3 + 150, "\n".join(b), bg=IVORY, title="ODDCHAPTER — contact sheet")


def main():
    write("04_MOTION/animation_reference/ANIMATION_STORYBOARD.svg", storyboard())
    write("05_PREVIEWS/USAGE_DO_DONT.svg", usage_sheet())
    write("05_PREVIEWS/CONTACT_SHEET.svg", contact_sheet())


if __name__ == "__main__":
    main()
