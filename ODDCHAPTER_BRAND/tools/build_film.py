"""
build_film.py — the brand film, rendered for real.

  ODDCHAPTER_BRAND/10_FILM/ODDCHAPTER_FILM_KISAH-NYATA_1080x1920.mp4

1080 x 1920, 25 fps, H.264 / yuv420p / AAC 48 kHz stereo, target -14 LUFS.
Timing is driven by the three narration WAVs in 10_FILM/audio/ — the cut is
measured from the speech, never guessed:

  build    0.00 - 1.60   monogram draws, wordmark wipes
  scene 1  1.60 - 7.60   "Setiap minggu, satu kisah nyata ..."
  scene 2  7.60 - 13.60  "Yang sebenarnya terjadi ..."
  card    13.60 - 20.40  signature line

Every on-screen word is the narration, verbatim: no claim is made that the
narration does not make. Frames are authored as SVG (10_FILM/source/) and
rasterised with resvg, then assembled with ffmpeg.

Run:  python3 tools/build_film.py
"""
import array
import json
import re
import shutil
import subprocess
import sys
import wave
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import brand
from brand import INK, IVORY, ORANGE, SAGE, f, svg_doc
from oclib import font_path

ROOT = brand.ROOT
FILM = ROOT / "10_FILM"
AUDIO = FILM / "audio"
SOURCE = FILM / "source"
OUT = FILM / "ODDCHAPTER_FILM_KISAH-NYATA_1080x1920.mp4"
POSTER = FILM / "ODDCHAPTER_FILM_POSTER_1080x1920.png"

W, H = 1080, 1920
FPS = 25
M = 96                      # side margin
SAFE_TOP, SAFE_BOT = 300, 1500   # keep type clear of Shorts / Reels / TikTok UI

# ------------------------------------------------------------------ measuring
_FONTS = {}


def _tt(family, weight):
    key = (family, weight)
    if key not in _FONTS:
        from fontTools.ttLib import TTFont
        p = font_path(family, weight)
        font = TTFont(str(p))
        _FONTS[key] = (font["head"].unitsPerEm, font.getBestCmap(), font["hmtx"],
                       font.getGlyphSet())
    return _FONTS[key]


def measure(s, family, weight, size, tracking=0.0):
    """Advance width in px at `size`, `tracking` in em."""
    upm, cmap, hmtx, _ = _tt(family, weight)
    w = 0.0
    for ch in s:
        g = cmap.get(ord(ch))
        if g is None:
            raise SystemExit(f"glyph missing: {ch!r} in {family} {weight}")
        w += hmtx[g][0] / upm * size
    w += tracking * size * (len(s) - 1)
    return w


def fit(s, family, weight, tracking, maxw, ceiling):
    """Largest size <= ceiling that keeps `s` inside `maxw`."""
    k = measure(s, family, weight, 1.0, tracking)
    return min(ceiling, maxw / k)


def ink_width(s, family, weight, size, tracking=0.0):
    """True ink width (glyph bounds, not advances) — what the eye sees as the margin."""
    from fontTools.pens.boundsPen import BoundsPen
    from fontTools.pens.transformPen import TransformPen
    upm, cmap, hmtx, gs = _tt(family, weight)
    scale = size / upm
    x = 0.0
    lo, hi = None, None
    for ch in s:
        gname = cmap.get(ord(ch))
        if gname is None:
            raise SystemExit(f"glyph missing: {ch!r} in {family} {weight}")
        glyph = gs[gname]
        pen = BoundsPen(gs)
        glyph.draw(TransformPen(pen, (scale, 0, 0, -scale, x, 0)))
        if pen.bounds:            # already in transformed (page) space
            a, _, b, _ = pen.bounds
            lo = a if lo is None else min(lo, a)
            hi = b if hi is None else max(hi, b)
        x += glyph.width * scale + tracking * size
    return (hi - lo) if hi is not None else 0.0


def fit_ink(s, family, weight, tracking, maxw, ceiling):
    """Largest size <= ceiling whose *ink* fits maxw (fontTools bounds)."""
    k = ink_width(s, family, weight, ceiling, tracking)
    return min(ceiling, ceiling * maxw / k)


def raster_ink(s, family, weight, size, tracking=0.0):
    """Ink width as resvg actually sets it — GPOS kerning included."""
    probe = Path("/tmp/film/_probe.svg")
    probe.parent.mkdir(parents=True, exist_ok=True)
    w = int(size * (len(s) + 2))
    h = int(size * 2.4)
    probe.write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}">'
        f'<rect width="{w}" height="{h}" fill="#000"/>{T(2, size * 1.6, s, family, weight, size, "#FFF", tracking, caps=True)}</svg>')
    png = probe.with_suffix(".png")
    run(["node", str(HERE / "render.mjs"), str(probe), str(png), str(w), "none"])
    raw = probe.with_suffix(".raw")
    run([ffmpeg(), "-y", "-hide_banner", "-loglevel", "error", "-i", str(png),
         "-vf", "format=gray", "-f", "rawvideo", str(raw)])
    d = raw.read_bytes()
    cols = [x for x in range(w) if max(d[y * w + x] for y in range(h)) > 90]
    return (cols[-1] - cols[0] + 1) if cols else size * len(s)


def fit_display(s, family, weight, maxw, ceiling):
    """Display size that lands the *rendered* ink on maxw."""
    k = raster_ink(s, family, weight, ceiling)
    return min(ceiling, ceiling * maxw / k)


def T(x, y, s, family="inter", weight=400, size=30, fill=IVORY, tracking=0.0,
      anchor="start", opacity=None, caps=False):
    """Text element (same contract as oclib.text, measured here)."""
    fam = "Space Grotesk" if family == "grotesk" else "Inter"
    txt = s.upper() if caps else s
    ls = f' letter-spacing="{f(tracking * size)}"' if tracking else ""
    op = f' opacity="{f(opacity, 3)}"' if opacity is not None else ""
    esc = txt.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return (f'<text x="{f(x)}" y="{f(y)}" font-family="{fam}" font-weight="{weight}" '
            f'font-size="{f(size, 2)}"{ls} fill="{fill}" text-anchor="{anchor}"{op}>{esc}</text>')


def wordmark_fit(maxw, color=IVORY, weight=700):
    """ODDCHAPTER outlines fitted to `maxw` px wide. Returns (svg, width, cap)."""
    probe, probe_w = brand.wordmark(100.0, color, 0, 0, weight=weight)
    cap = 100.0 * maxw / probe_w
    svg, w = brand.wordmark(cap, color, 0, 0, weight=weight)
    return svg, w, cap


def rule(x, y, w, h=4, fill=ORANGE):
    return f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" fill="{fill}"/>'


# ------------------------------------------------------------------ audio timing
def speech_bounds(path):
    """(total, onset, offset) in seconds — 20 ms window, peak-based."""
    w = wave.open(str(path))
    sr = w.getframerate()
    a = array.array("h")
    a.frombytes(w.readframes(w.getnframes()))
    win = int(sr * 0.02)
    peaks = [max(abs(min(a[i:i + win])), abs(max(a[i:i + win])))
             for i in range(0, len(a) - win, win)]
    thr = max(peaks) * 0.02
    first = next(i for i, v in enumerate(peaks) if v > thr)
    last = max(i for i, v in enumerate(peaks) if v > thr)
    return len(a) / sr, first * 0.02, (last + 1) * 0.02


def snap(t):
    """Snap a time to the frame grid so audio and picture agree exactly."""
    return round(t * FPS) / FPS


def timeline():
    d1, o1, e1 = speech_bounds(AUDIO / "vo_01.wav")
    d2, o2, e2 = speech_bounds(AUDIO / "vo_02.wav")
    d3, o3, e3 = speech_bounds(AUDIO / "signature.wav")

    lead = 0.30                          # air after the cut before speech
    build_dur = 1.60
    s1 = snap(build_dur)
    s2 = snap(s1 + max(6.0, (e1 - o1) + 1.55))
    s3 = snap(s2 + max(6.0, (e2 - o2) + 1.55))
    end = snap(s3 + max(6.8, (e3 - o3) + lead + 0.85))

    tl = dict(
        build=(0.0, s1),
        s1=(s1, s2),
        s2=(s2, s3),
        s3=(s3, end),
        total=end,
        # clip start times, back-computed from the speech onset in each file
        vo1=snap(s1 + lead - o1),
        vo2=snap(s2 + lead - o2),
        sig=snap(s3 + lead - o3),
        speech=[(o1, e1), (o2, e2), (o3, e3)],
    )
    return tl


# ------------------------------------------------------------------ frames
def ease(x):
    """cubic-bezier(.2,.7,.2,1) — the brand's curve."""
    x = min(max(x, 0.0), 1.0)
    lo, hi = 0.0, 1.0
    for _ in range(24):
        mid = (lo + hi) / 2
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


def build_frame(t):
    """t in 0..1.6 s — monogram draws in, wordmark wipes, tagline stays for scene 1."""
    MS = 380 / brand.MW                       # monogram 380 px wide
    mk_h = brand.MH * MS
    cx, cy = W / 2, 700
    mx, my = cx - 380 / 2, cy - mk_h / 2

    wm_svg, wm_w, cap = wordmark_fit(800)
    wx = cx - wm_w / 2
    wy = my + mk_h + 150

    e_m = ease(ramp(t, 0.10, 0.95))
    e_w = ease(ramp(t, 0.80, 1.30))

    g = [f'<rect width="{W}" height="{H}" fill="{INK}"/>']
    g.append(f'<g opacity="{f(e_m, 4)}" transform="translate({f(cx)} {f(cy)}) '
             f'scale({f(0.93 + 0.07 * e_m, 5)}) translate({f(-cx)} {f(-cy)})">')
    g.append(brand.monogram(mx, my, MS, IVORY))
    g.append('</g>')
    if e_w > 0:
        g.append('<clipPath id="wipe">'
                 f'<rect x="-4" y="-{f(cap * 0.35)}" width="{f(wm_w * e_w + 4)}" '
                 f'height="{f(cap * 1.55)}"/></clipPath>')
        g.append(f'<g transform="translate({f(wx)} {f(wy)})">'
                 f'<g clip-path="url(#wipe)">{wm_svg}</g></g>')
    return svg_doc(W, H, "\n".join(g), bg=None, title=f"ODDCHAPTER film — build {t:.2f}s")


def scene1():
    g = [f'<rect width="{W}" height="{H}" fill="{INK}"/>']
    g.append(rule(M, 470, 96))
    g.append(T(M, 546, "SETIAP MINGGU", weight=600, size=30, fill=SAGE,
               tracking=0.28, caps=True))
    s = fit_display("SATU KISAH NYATA", "grotesk", 700, W - 2 * M, 108)
    g.append(T(M, 700, "SATU KISAH NYATA", "grotesk", 700, s, IVORY, caps=True))
    for i, line in enumerate(["YANG BERAKHIR", "JAUH DARI", "DUGAAN."]):
        g.append(T(M, 800 + i * 76, line, "grotesk", 300, 56, IVORY,
                   opacity=0.74, caps=True, tracking=0.02))
    g.append(T(M, 1400, "ODDCHAPTER", "grotesk", 700, 22, SAGE, tracking=0.22, caps=True))
    return svg_doc(W, H, "\n".join(g), bg=None, title="ODDCHAPTER film — scene 1")


def scene2():
    g = [f'<rect width="{W}" height="{H}" fill="{INK}"/>']
    g.append(rule(M, 470, 96))
    g.append(T(M, 546, "YANG SEBENARNYA TERJADI", weight=600, size=30,
               fill=SAGE, tracking=0.20, caps=True))
    size = min(fit_display("LEBIH", "grotesk", 700, W - 2 * M, 190),
               fit_display("ANEH", "grotesk", 700, W - 2 * M, 190))
    g.append(T(M, 780, "LEBIH", "grotesk", 700, size, IVORY, caps=True))
    g.append(T(M, 962, "ANEH", "grotesk", 700, size, IVORY, caps=True))
    g.append(T(M, 1084, "DARIPADA YANG KITA BAYANGKAN", "grotesk", 300, 44,
               IVORY, opacity=0.70, caps=True, tracking=0.02))
    g.append(T(M, 1400, "ODDCHAPTER", "grotesk", 700, 22, SAGE, tracking=0.22, caps=True))
    return svg_doc(W, H, "\n".join(g), bg=None, title="ODDCHAPTER film — scene 2")


def end_card():
    MS = 300 / brand.MW
    mk_h = brand.MH * MS
    mtop = 620
    g = [f'<rect width="{W}" height="{H}" fill="{INK}"/>']
    g.append(brand.monogram((W - 300) / 2, mtop, MS, IVORY))

    wm_svg, wm_w, cap = wordmark_fit(720)
    wy = mtop + mk_h + 170
    g.append(f'<g transform="translate({f((W - wm_w) / 2)} {f(wy)})">{wm_svg}</g>')

    rule_y = wy + cap + 62
    g.append(rule((W - 120) / 2, rule_y, 120, 4))

    tag = "KISAH NYATA. DI LUAR DUGAAN."
    tsize = fit(tag, "inter", 600, 0.20, W - 2 * M, 32)
    g.append(T(W / 2, rule_y + 78, tag, weight=600, size=tsize, fill=SAGE,
               tracking=0.20, anchor="middle", caps=True))
    return svg_doc(W, H, "\n".join(g), bg=None, title="ODDCHAPTER film — end card")


# ------------------------------------------------------------------ ffmpeg
def ffmpeg():
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        p = shutil.which("ffmpeg")
        if not p:
            raise SystemExit("ffmpeg not found — pip3 install --break-system-packages imageio-ffmpeg")
        return p


def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode != 0:
        raise SystemExit(f"command failed ({r.returncode}):\n  {' '.join(map(str, cmd))}\n"
                         f"{r.stderr[-3000:]}")
    return r


def render_png(svg_path, png_path, width=W):
    run(["node", str(HERE / "render.mjs"), str(svg_path), str(png_path), str(width), "none"])


def build_audio(tl, ff, dest):
    """Place the three clips on a silent bed, then normalise to -14 LUFS two-pass."""
    total = tl["total"]
    srcs = [AUDIO / "vo_01.wav", AUDIO / "vo_02.wav", AUDIO / "signature.wav"]
    delays = [int(round(tl["vo1"] * 1000)), int(round(tl["vo2"] * 1000)), int(round(tl["sig"] * 1000))]

    graph = []
    for i, (d, n) in enumerate(zip(delays, ["a0", "a1", "a2"])):
        graph.append(f"[{i}:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=mono,"
                     f"adelay={d}|{d}[{n}]")
    graph.append("[a0][a1][a2]amix=inputs=3:normalize=0:dropout_transition=0,"
                 f"apad=whole_dur={total}[mix]")

    def cmd(filtergraph, out_args):
        return [ff, "-y", "-hide_banner",
                *sum([["-i", str(s)] for s in srcs], []),
                "-filter_complex", filtergraph, *out_args]

    # pass 1 — measure
    probe = run(cmd(";".join(graph) + ";[mix]loudnorm=I=-14:TP=-1:LRA=7:print_format=json[out]",
                    ["-map", "[out]", "-f", "null", "-"]))
    m = re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", probe.stderr, re.S)
    if not m:
        raise SystemExit("loudnorm pass 1 gave no measurements:\n" + probe.stderr[-1500:])
    meas = json.loads(m.group(0))

    # pass 2 — apply the measurement linearly
    ln = (f"loudnorm=I=-14:TP=-1:LRA=7:measured_I={meas['input_i']}"
          f":measured_TP={meas['input_tp']}:measured_LRA={meas['input_lra']}"
          f":measured_thresh={meas['input_thresh']}:offset={meas['target_offset']}"
          f":linear=true")
    graph2 = graph + [f"[mix]{ln},aresample=48000,apad=whole_dur={total},"
                      f"atrim=0:{total},asetpts=N/SR/TB[out]"]
    run(cmd(";".join(graph2),
            ["-map", "[out]", "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", str(dest)]))
    return meas


def main():
    SOURCE.mkdir(parents=True, exist_ok=True)
    tl = timeline()
    ff = ffmpeg()
    tmp = Path("/tmp/film")
    shutil.rmtree(tmp, ignore_errors=True)
    (tmp / "build").mkdir(parents=True)

    print(f"timeline   build 0.00–{tl['build'][1]:.2f}   scene1 {tl['s1'][0]:.2f}–{tl['s1'][1]:.2f}   "
          f"scene2 {tl['s2'][0]:.2f}–{tl['s2'][1]:.2f}   card {tl['s3'][0]:.2f}–{tl['total']:.2f}")
    print(f"voice      vo1 @{tl['vo1']:.2f}s   vo2 @{tl['vo2']:.2f}s   signature @{tl['sig']:.2f}s   "
          f"duration {tl['total']:.2f}s")

    # ---- source SVG (editable, committed)
    stills = {"SCENE_1": scene1(), "SCENE_2": scene2(), "END_CARD": end_card()}
    for name, doc in stills.items():
        (SOURCE / f"{name}.svg").write_text(doc)
    # the build as a held final state, for hand-editing
    (SOURCE / "BUILD_FINAL_STATE.svg").write_text(build_frame(1.6))

    n_build = int(round((tl["build"][1] - tl["build"][0]) * FPS))
    for i in range(n_build):
        t = (i + 1) / FPS
        p = tmp / "build" / f"f{i:04d}.svg"
        p.write_text(build_frame(t))
        render_png(p, tmp / "build" / f"f{i:04d}.png")
    print(f"frames     build {n_build} rendered")

    for name, doc in stills.items():
        svg = SOURCE / f"{name}.svg"
        render_png(svg, tmp / f"{name.lower()}.png")
        run([ff, "-y", "-hide_banner", "-loglevel", "error", "-i", str(tmp / f"{name.lower()}.png"),
             "-frames:v", "1", str(tmp / f"{name.lower()}_check.png")])

    shutil.copy(tmp / "end_card.png", POSTER)

    # ---- segments
    ENC = ["-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p",
           "-profile:v", "high", "-level", "4.0", "-g", "50", "-r", str(FPS),
           "-video_track_timescale", "12800"]

    segs = []
    seg0 = tmp / "seg0.mp4"
    run([ff, "-y", "-hide_banner", "-loglevel", "error", "-framerate", str(FPS),
         "-i", str(tmp / "build" / "f%04d.png"), *ENC, str(seg0)])
    segs.append(seg0)

    plan = [("scene_1", tl["s1"], 1.035), ("scene_2", tl["s2"], 1.035), ("end_card", tl["s3"], 1.02)]
    for i, (name, (a, b), zmax) in enumerate(plan, start=1):
        n = int(round((b - a) * FPS))
        seg = tmp / f"seg{i}.mp4"
        vf = (f"scale={W * 2}:{H * 2}:flags=lanczos,"
              f"zoompan=z='min(1+{zmax - 1}*on/{max(n - 1, 1)},{zmax})'"
              f":x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)-{H * 0.006}*on/{max(n - 1, 1)}'"
              f":d={n}:s={W}x{H}:fps={FPS},format=yuv420p")
        if name == "end_card":
            vf += f",fade=t=out:st={(n - 9) / FPS:.3f}:d=0.36"
        run([ff, "-y", "-hide_banner", "-loglevel", "error", "-i", str(tmp / f"{name}.png"),
             "-vf", vf, "-frames:v", str(n), *ENC, str(seg)])
        segs.append(seg)
        print(f"segment    {name:9s} {n:3d} frames  {(b - a):.2f}s")

    lst = tmp / "concat.txt"
    lst.write_text("".join(f"file '{s}'\n" for s in segs))
    silent = tmp / "picture.mp4"
    run([ff, "-y", "-hide_banner", "-loglevel", "error", "-f", "concat", "-safe", "0",
         "-i", str(lst), "-c", "copy", str(silent)])

    # ---- sound
    wav = tmp / "master.wav"
    meas = build_audio(tl, ff, wav)
    run([ff, "-y", "-hide_banner", "-loglevel", "error", "-i", str(silent), "-i", str(wav),
         "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
         "-ar", "48000", "-shortest", "-movflags", "+faststart", str(OUT)])

    info = subprocess.run([ff, "-hide_banner", "-i", str(OUT)],
                          capture_output=True, text=True).stderr
    dur = re.search(r"Duration: (\d+):(\d+):([\d.]+)", info)
    vid = re.search(r"Video: (\w+).*?, (\d{3,4})x(\d{3,4}).*?, ([\d.]+) fps", info)
    aud = re.search(r"Audio: (\w+).*?, (\d+) Hz, (\w+)", info)
    if not (dur and vid and aud):
        raise SystemExit("could not read back the encode:\n" + info[-1500:])
    seconds = int(dur.group(1)) * 3600 + int(dur.group(2)) * 60 + float(dur.group(3))
    size = OUT.stat().st_size / 1e6
    print(f"\nwritten    {OUT.relative_to(ROOT)}")
    print(f"           {vid.group(2)}x{vid.group(3)} {vid.group(1)} {vid.group(4)} fps · "
          f"{aud.group(1)} {aud.group(2)} Hz {aud.group(3)} · {seconds:.2f}s · {size:.1f} MB")
    print(f"loudness   input {meas['input_i']} LUFS → target -14 LUFS linear, TP -1 dBTP")
    print(f"poster     {POSTER.relative_to(ROOT)}")
    if abs(seconds - tl["total"]) > 0.12:
        raise SystemExit(f"duration drift: {seconds:.2f}s vs planned {tl['total']:.2f}s")


if __name__ == "__main__":
    main()
