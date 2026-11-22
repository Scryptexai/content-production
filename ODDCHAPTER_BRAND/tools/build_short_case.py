#!/usr/bin/env python3
"""Builder Short 9:16 ODDCHAPTER seri "angker" — generik per kasus.

Konfigurasi kasus ada di work/<slug>/case_cfg.py (IMAGES, SHOTS, OVL, KEYWORDS, …).
Pemakaian:
  python3 build_short_case.py <slug> shots|video|audio|mux|srt|all [--force]
"""
import importlib.util, json, os, subprocess, sys
from pathlib import Path

FF = os.environ.get("FFMPEG") or __import__("imageio_ffmpeg").get_ffmpeg_exe()

ROOT = Path(__file__).resolve().parents[2]
# Kartu akhir animasi (logo OC + wordmark + garis oranye + tagline) — dirender
# Remotion: node scripts/render-outro.mjs di 10_FILM/remotion/ -> output/short_outro_9x16.mp4
# (1080x1920,30 fps,5,00 s, tanpa audio). Dipakai dengan mode shot "outro".
OUTRO = ROOT / "ODDCHAPTER_BRAND" / "10_FILM" / "remotion" / "output" / "short_outro_9x16.mp4"
OUTRO_DUR = 5.00
SLUG = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("-") else "sengkon"
CASE = ROOT / "work" / SLUG
IMG = CASE / "img"
SHOTS = CASE / "shots"
AUD = CASE / "audio"
OUT = CASE / "out"
SUB = CASE / "subs.ass"
FONTS = CASE / "fonts"

W, H, FPS = 1080, 1920, 30
LEAD = 0.15                       # cut sebelum kata jangkar

RED = "&H002A2AD8&"               # #D82A2A
IVORY = "&H00E0ECF0&"             # #F0ECE0
GREY = "&H00D0D0D0&"


def load_cfg():
    spec = importlib.util.spec_from_file_location(f"cfg_{SLUG}", CASE / "case_cfg.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


CFG = load_cfg()
END = CFG.END
IMAGES = CFG.IMAGES
SHOT_LIST = CFG.SHOTS
IMG_FILES = {k: v[0] for k, v in IMAGES.items()}
IMG_DIM = {k: (v[1], v[2]) for k, v in IMAGES.items()}
KEYWORDS = getattr(CFG, "KEYWORDS", set())
NUM_PHRASES = getattr(CFG, "NUM_PHRASES", [])
MERGE = getattr(CFG, "MERGE", [])
WORD_FIX = getattr(CFG, "WORD_FIX", {})
CREDITS = getattr(CFG, "CREDITS", "")
OUT_NAME = getattr(CFG, "OUT_NAME", "short.mp4")
CLIPS = getattr(CFG, "CLIPS", {})          # key -> (file, start, dur) di work/<slug>/footage/
CLIP_DIR = CASE / "footage"
ASS_HEAD = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Sub,Barlow Condensed ExtraBold,100,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,0,0,0,0,100,100,1.5,0,1,8,3,2,60,60,672,1
Style: Kicker,Barlow Condensed ExtraBold,74,&H00E0ECF0,&H00E0ECF0,&H00000000,&H80000000,0,0,0,0,100,100,6,0,1,6,2,5,60,60,0,1
Style: Big,Anton,170,&H00FFFFFF,&H00FFFFFF,&H00000000,&H60000000,0,0,0,0,100,100,0,0,1,10,4,5,40,40,0,1
Style: Stamp,Anton,120,&H00000000,&H00000000,&H002A2AD8,&H00000000,0,0,0,0,100,100,0,0,3,14,0,5,40,40,0,1
Style: Tag,Barlow Condensed ExtraBold,34,&H00D0D0D0,&H00D0D0D0,&H00000000,&H80000000,0,0,0,0,100,100,1.2,0,1,3,1,7,60,60,300,1
Style: Credit,Barlow Condensed ExtraBold,40,&H00D0D0D0,&H00D0D0D0,&H00000000,&H80000000,0,0,0,0,100,100,1,0,1,3,1,5,60,60,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


def ass_t(t):
    t = max(0.0, t)
    h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def ev(t0, t1, style, text, layer=0):
    return f"Dialogue: {layer},{ass_t(t0)},{ass_t(t1)},{style},,0,0,0,,{text}\n"


def load_words():
    data = json.loads((CASE / "vo_alignment.json").read_text())
    words = [{"w": x["word"], "t0": float(x["start"]), "t1": float(x["end"])} for x in data["words"]]

    # 1) gabung potongan kata yang terpecah (mis. "menanda" + "tangani")
    merged, i = [], 0
    while i < len(words):
        hit = None
        for entry in MERGE:
            parts, disp = entry[0], entry[1]
            n = len(parts)
            chunk = [w["w"].strip(",.?!").lower() for w in words[i:i + n]]
            if chunk == [p.lower() for p in parts]:
                hit = (disp, n)
                break
        if hit:
            merged.append({"w": hit[0], "t0": words[i]["t0"], "t1": words[i + hit[1] - 1]["t1"]})
            i += hit[1]
            continue
        merged.append(words[i]); i += 1
    words = merged

    # 2) angka yang dieja -> digit (sesuai fakta.md)
    out, i = [], 0
    while i < len(words):
        matched = False
        for phrase, digits in NUM_PHRASES:
            n = len(phrase)
            chunk = [w["w"].strip(",.?!").lower() for w in words[i:i + n]]
            if chunk == phrase:
                out.append({"w": digits, "t0": words[i]["t0"], "t1": words[i + n - 1]["t1"]})
                i += n; matched = True; break
        if not matched:
            out.append(words[i]); i += 1

    # 3) ejaan nama/judul yang dirapikan untuk caption
    for tok in out:
        key = tok["w"].strip(",.?!").lower()
        if key in WORD_FIX:
            tail = tok["w"][len(tok["w"].rstrip(",.?!")):] or ""
            tok["w"] = WORD_FIX[key] + tail
    return out


def build_captions(words):
    events, group = [], []
    for w in words:
        raw = w["w"].strip()
        display = raw.rstrip(",.")
        gap = w["t0"] - group[-1]["t1"] if group else 0
        chars = sum(len(g["w"].strip().rstrip(",.")) + 1 for g in group) + len(display)
        end_punct = bool(group) and (group[-1]["raw"][-1] in ".?"
                                     or (group[-1]["raw"][-1] == "," and len(group) >= 2))
        if group and (len(group) >= 3 or chars > 18 or gap > 0.30 or end_punct):
            events.append(group); group = []
        group.append({"w": display, "raw": raw, "t0": w["t0"], "t1": w["t1"]})
    if group:
        events.append(group)

    lines = []
    for gi, g in enumerate(events):
        t0 = g[0]["t0"] - 0.06
        t1 = g[-1]["t1"] + 0.14
        if gi + 1 < len(events):
            t1 = min(t1, events[gi + 1][0]["t0"] - 0.02)
        parts = []
        for tok in g:
            up = tok["w"].upper()
            # cocokkan KEYWORDS tanpa tanda baca di ujung ("KUGELBLITZ," = KUGELBLITZ)
            hit = up.rstrip(",.") in KEYWORDS
            parts.append(f"{{\\c{RED}}}{up}{{\\c&H00FFFFFF&}}" if hit else up)
        plain = " ".join(w["w"].upper() for w in g)
        est = len(plain) * 0.427 * 100          # lebar perkiraan @ fs 100
        if est > 860:                            # baris kepanjangan -> kecilkan font
            fs = max(56, int(860 / (len(plain) * 0.427)))
            txt = f"{{\\fs{fs}}}" + " ".join(parts)
        else:
            txt = "{\\fscx118\\fscy118\\t(0,90,\\fscx100\\fscy100)}" + " ".join(parts)
        lines.append(ev(t0, t1, "Sub", txt))
    return lines, events


def build_overlays():
    return [ev(t0, t1, style, text) for (t0, t1, style, text) in CFG.OVL]


def build_tags():
    L = []
    for (t0, t1, img, mode, z0, z1, extra) in SHOT_LIST:
        tag = extra.get("tag")
        if tag:
            L.append(ev(t0 + 0.25, t1 - 0.10, "Tag", tag))
        if mode in ("canvas", "fill"):
            L.append(ev(t0 + 0.25, t1 - 0.10, "Tag",
                        f"{{\\an9\\pos(1020,300)\\fs26\\fsp4\\c{GREY}\\alpha&H60&}}ODDCHAPTER"))
    return L


def write_ass():
    words = load_words()
    caps, groups = build_captions(words)
    body = "".join(build_tags()) + "".join(build_overlays()) + "".join(caps)
    SUB.write_text(ASS_HEAD + body)
    json.dump(groups, open(CASE / "caption_groups.json", "w"), ensure_ascii=False, indent=1)
    print(f"subs.ass: {len(caps)} caption, {len(build_overlays())} overlay")


def run(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        sys.stderr.write(" ".join(cmd) + "\n" + p.stderr[-4000:])
        raise SystemExit(1)
    return p


GRADE = ("eq=saturation=0.30:contrast=1.18:brightness=-0.05:gamma=0.85,"
         "colorbalance=bs=0.07:rs=-0.04,curves=master='0/0 0.5/0.38 1/0.88'")
POST = (f",{GRADE},vignette=angle=PI/4.2,noise=alls=7:allf=t,"
        "eq=brightness='-0.015+0.02*sin(t*19)*sin(t*3.1)':eval=frame,format=yuv420p")


def fg_box(img, top=False):
    iw, ih = IMG_DIM[img]
    maxw, maxh = 1000, (1000 if top else 1150)
    if iw / ih > maxw / maxh:
        fw = maxw; fh = round(maxw * ih / iw)
    else:
        fh = maxh; fw = round(maxh * iw / ih)
    fw -= fw % 2; fh -= fh % 2
    return fw, fh


def shot_filter(img, mode, z0, z1, dur, extra):
    n = max(2, round(dur * FPS))
    cx = extra.get("focusx", 0.5); cy = extra.get("focusy", 0.5)
    zex = f"{z0}+({z1}-{z0})*on/{n - 1}"
    xex = f"(iw-iw/zoom)*{cx}"; yex = f"(ih-ih/zoom)*{cy}"
    fade = f",fade=t=in:st=0:d=0.14,fade=t=out:st={max(0, dur - 0.12):.3f}:d=0.12"

    if mode == "canvas":
        fw, fh = fg_box(img, top=bool(extra.get("top")))
        y = 720 - fh // 2
        y = max(150, y)
        return (
            "[0:v]split=2[bgs][fgs];"
            "[bgs]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
            "gblur=sigma=26,eq=brightness=-0.50:saturation=0.26[bgb];"
            f"[fgs]scale={2*fw}:{2*fh},setsar=1,"
            f"zoompan=z='{zex}':x='{xex}':y='{yex}':d={n}:s={fw}x{fh}:fps={FPS},setsar=1[fgv];"
            f"[bgb][fgv]overlay=(1080-{fw})/2:{y}:shortest=1" + CLIP_POST + fade
        )
    if mode == "fill":
        return (
            "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
            f"scale=2160:3840,setsar=1,zoompan=z='{zex}':x='{xex}':y='{yex}':d={n}:s=1080x1920:fps={FPS},setsar=1"
            + POST + fade
        )
    # card
    return (
        "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
        "gblur=sigma=16,eq=brightness=-0.28:saturation=0.36,"
        f"scale=2160:3840,setsar=1,zoompan=z='{zex}':x='{xex}':y='{yex}':d={n}:s=1080x1920:fps={FPS},setsar=1"
        + POST + fade
    )


CLIP_BG_BRIGHT = getattr(CFG, "CLIP_BG_BRIGHT", "-0.55")

CLIP_POST = (",eq=saturation=0.16:contrast=1.28:brightness=0.02:gamma=0.92,colorbalance=bs=0.08,"
             "vignette=angle=PI/5.0,noise=alls=6:allf=t,format=yuv420p")


def clip_filter(key, dur, extra):
    """Footage asli — aturan pemilik (21 Nov 2026): klip16:9 DIPERBESAR full
    layar9:16 (cover-crop), bukan jendela di atas latar blur. Gaya lama bisa
    dipakai lagi per-shot dengan extra={"window": True}."""
    fn, cs, cd = CLIPS[key]
    fade = f",fade=t=in:st=0:d=0.12,fade=t=out:st={max(0, dur - 0.12):.3f}:d=0.12"
    if extra.get("raw"):
        # render eksternal (mis. shot peta MAP-ZOOM) — tanpa grade CLIP_POST,
        # tanpa fade (MapZoom sudah punya fade bawaan), cover-crop saja bila
        # aspek beda; peta9:16 sudah pas → langsung fps+format.
        return (
            "[0:v]fps=30,scale=1080:1920:force_original_aspect_ratio=increase,"
            "crop=1080:1920,setsar=1,format=yuv420p"
        )
    if extra.get("window"):
        # gaya lama: jendela16:9/4:3 di atas latar blur
        fw, fh = extra.get("box", (1000, 750))
        fw -= fw % 2; fh -= fh % 2
        y = 720 - fh // 2
        bg_b = extra.get("bg", CLIP_BG_BRIGHT)
        return (
            "[0:v]split=2[bgs][fgs];"
            "[bgs]fps=30,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
            f"gblur=sigma=30,eq=brightness={bg_b}:saturation=0.22[bgb];"
            f"[fgs]fps=30,scale={fw}:{fh}:force_original_aspect_ratio=increase,crop={fw}:{fh},setsar=1[fgv];"
            f"[bgb][fgv]overlay=(1080-{fw})/2:{y}:shortest=1" + CLIP_POST + fade
        )
    # default: cover-crop full layar9:16 (16:9 diperbesar sampai menutup frame)
    return (
        "[0:v]fps=30,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
        "setsar=1" + CLIP_POST + fade
    )


def clip_fill_filter(key, dur, extra):
    """Footage asli penuh layar 9:16 (untuk klip vertikal / tekstur salju)."""
    fn, cs, cd = CLIPS[key]
    n = max(2, round(dur * FPS))
    fade = f",fade=t=in:st=0:d=0.12,fade=t=out:st={max(0, dur - 0.12):.3f}:d=0.12"
    return (
        "[0:v]fps=30,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
        "setsar=1" + CLIP_POST + fade
    )


def render_shots(force=False):
    SHOTS.mkdir(parents=True, exist_ok=True)
    for i, (t0, t1, img, mode, z0, z1, extra) in enumerate(SHOT_LIST):
        dur = t1 - t0
        outp = SHOTS / f"{i:02d}.mp4"
        if outp.exists() and not force:
            continue
        n = max(2, round(dur * FPS))
        if mode == "clip":
            fn, cs, cd = CLIPS[img]
            src = CLIP_DIR / fn
            filt = clip_filter(img, dur, extra)
            run([FF, "-y", "-ss", f"{cs:.3f}", "-t", f"{min(cd, dur):.3f}", "-i", str(src),
                 "-filter_complex", filt, "-frames:v", str(n), "-r", str(FPS),
                 "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p",
                 "-an", str(outp)])
        elif mode == "clipfill":
            fn, cs, cd = CLIPS[img]
            src = CLIP_DIR / fn
            filt = clip_fill_filter(img, dur, extra)
            run([FF, "-y", "-ss", f"{cs:.3f}", "-t", f"{min(cd, dur):.3f}", "-i", str(src),
                 "-filter_complex", filt, "-frames:v", str(n), "-r", str(FPS),
                 "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p",
                 "-an", str(outp)])
        elif mode == "outro":
            # Lockup merek Remotion — TANPA grade (warna brand harus persis).
            if dur > OUTRO_DUR + 0.05:
                raise SystemExit(
                    f"shot outro durasi {dur:.2f}s > {OUTRO_DUR:.2f}s — "
                    f"pakai (END - {OUTRO_DUR:.2f}) sebagai awal segmen terakhir"
                )
            if not OUTRO.exists():
                print(f"  ! {OUTRO} tidak ada — fallback hitam "
                      f"(render dulu: node10_FILM/remotion/scripts/render-outro.mjs)",
                      flush=True)
                run([FF, "-y", "-f", "lavfi", "-i", f"color=c=black:s={W}x{H}:r={FPS}",
                     "-filter_complex", "fade=t=in:st=0:d=0.14",
                     "-frames:v", str(n), "-r", str(FPS), "-c:v", "libx264", "-preset", "veryfast",
                     "-crf", "16", "-pix_fmt", "yuv420p", "-an", str(outp)])
            else:
                run([FF, "-y", "-t", f"{dur:.3f}", "-i", str(OUTRO),
                     "-filter_complex",
                     f"fps={FPS},scale={W}:{H}:force_original_aspect_ratio=increase,"
                     f"crop={W}:{H},setsar=1,fade=t=in:st=0:d=0.14,format=yuv420p",
                     "-frames:v", str(n), "-r", str(FPS), "-c:v", "libx264", "-preset", "veryfast",
                     "-crf", "16", "-pix_fmt", "yuv420p", "-an", str(outp)])
        elif mode == "black":
            run([FF, "-y", "-f", "lavfi", "-i", f"color=c=black:s={W}x{H}:r={FPS}",
                 "-filter_complex", POST.lstrip(",") + f",fade=t=in:st=0:d=0.14",
                 "-frames:v", str(n), "-r", str(FPS), "-c:v", "libx264", "-preset", "veryfast",
                 "-crf", "16", "-pix_fmt", "yuv420p", "-an", str(outp)])
        else:
            src = IMG / IMG_FILES[img]
            filt = shot_filter(img, mode, z0, z1, dur, extra)
            run([FF, "-y", "-loop", "1", "-i", str(src), "-filter_complex", filt,
                 "-frames:v", str(n), "-r", str(FPS), "-c:v", "libx264", "-preset", "veryfast",
                 "-crf", "16", "-pix_fmt", "yuv420p", "-an", str(outp)])
        print(f"shot {i:02d} {t0:6.2f}-{t1:6.2f} {mode:6s} ok", flush=True)


def concat_shots():
    lst = CASE / "concat.txt"
    lst.write_text("".join(f"file '{SHOTS / f'{i:02d}.mp4'}'\n" for i in range(len(SHOT_LIST))))
    cat = CASE / "cat.mp4"
    run([FF, "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(cat)])
    return cat


def render_video():
    write_ass()
    cat = concat_shots()
    outp = OUT / "video.mp4"
    filt = f"ass={SUB}:fontsdir={FONTS},scale=out_range=tv:out_color_matrix=bt709,format=yuv420p"
    run([FF, "-y", "-i", str(cat), "-vf", filt,
         "-r", str(FPS), "-c:v", "libx264", "-preset", "medium", "-crf", "24",
         "-maxrate", "3.6M", "-bufsize", "7.2M", "-profile:v", "high", "-pix_fmt", "yuv420p",
         "-an", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
         "-color_range", "tv", "-movflags", "+faststart", "-t", f"{END:.2f}", str(outp)])
    print("video:", outp, outp.stat().st_size)


def synth_bed():
    custom = getattr(CFG, "BED_BUILDER", None)
    if custom:
        run([sys.executable, str(CASE / custom)])
        return
    import numpy as np, wave
    sr = 48000
    n = int(END * sr)
    t = np.arange(n) / sr
    rng = np.random.default_rng(7)

    drone = (0.55 * np.sin(2 * np.pi * 55 * t)
             + 0.30 * np.sin(2 * np.pi * 82.5 * t + 0.6)
             + 0.18 * np.sin(2 * np.pi * 110 * t + 1.2))
    drone *= 0.75 + 0.25 * np.sin(2 * np.pi * 0.07 * t)

    noise = rng.standard_normal(n)
    wind = np.convolve(noise, np.ones(420) / 420, mode="same")
    wind *= 0.6 + 0.4 * np.sin(2 * np.pi * 0.05 * t + 1.0)

    clock = np.zeros(n)
    k = 0
    while k * 1.0 < END:
        idx = int(k * sr); ln = int(0.05 * sr)
        if idx + ln < n:
            clock[idx:idx + ln] += 0.5 * np.exp(-np.linspace(0, 14, ln)) * rng.standard_normal(ln)
        k += 1

    bed = 1.00 * drone + 1.5 * wind + 0.35 * clock

    def add_hit(at, freq=52.0, amp=1.0, dur=1.6):
        i0 = int(at * sr); ln = min(int(dur * sr), n - i0)
        if ln <= 0:
            return
        tt = np.arange(ln) / sr
        env = np.exp(-tt * 3.2)
        sig = amp * (0.8 * np.sin(2 * np.pi * freq * tt)
                     + 0.5 * rng.standard_normal(ln) * np.exp(-tt * 9))
        bed[i0:i0 + ln] += sig * env

    def add_riser(t0, t1):
        i0, i1 = int(t0 * sr), int(t1 * sr)
        ln = i1 - i0
        if ln <= 0:
            return
        tt = np.linspace(0, 1, ln)
        nz = rng.standard_normal(ln)
        hp = nz - np.concatenate([[0], nz[:-1]])
        bed[i0:i1] += 0.55 * hp * (tt ** 2.2)

    for at in [0.05, 8.5, 39.65, 61.25, 81.45, 104.15]:
        add_hit(at, amp=0.9)
    add_hit(88.3, freq=46, amp=1.1, dur=2.2)
    add_riser(57.0, 61.2)
    add_riser(78.0, 81.4)

    fi = int(1.2 * sr); bed[:fi] *= np.linspace(0, 1, fi)
    fo = int(3.0 * sr); bed[-fo:] *= np.linspace(1, 0, fo)
    bed = bed / (np.max(np.abs(bed)) + 1e-9) * 0.7
    stereo = np.stack([bed, np.roll(bed, int(0.008 * sr))], axis=1)
    pcm = (np.clip(stereo, -1, 1) * 32767).astype("<i2")
    with wave.open(str(AUD / "bed.wav"), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes(pcm.tobytes())
    print("bed.wav ok", (AUD / "bed.wav").stat().st_size)


def mix_audio():
    vo = CASE / CFG.VO_FILE
    bed = AUD / "bed.wav"
    filt = (
        "[0:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo,"
        "volume=2.4,highpass=f=70,lowpass=f=13000,"
        "acompressor=threshold=0.12:ratio=3:attack=15:release=180,asplit=2[vo][sc];"
        "[1:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo[bed];"
        "[bed][sc]sidechaincompress=threshold=0.045:ratio=7:attack=25:release=380[bedd];"
        "[vo][bedd]amix=inputs=2:normalize=0:dropout_transition=0,"
        "alimiter=limit=0.84:level=false[out]"
    )
    raw = AUD / "mix_raw.wav"
    run([FF, "-y", "-i", str(vo), "-i", str(bed), "-filter_complex", filt,
         "-map", "[out]", "-t", f"{END:.2f}", "-ar", "48000", "-ac", "2", str(raw)])
    p = run([FF, "-hide_banner", "-nostats", "-i", str(raw), "-af",
             "loudnorm=I=-15:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"])
    j = p.stderr[p.stderr.rfind("{"):p.stderr.rfind("}") + 1]
    m = json.loads(j)
    ln = (f"loudnorm=I=-15:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
          f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:"
          f"offset={m['target_offset']}:linear=true:print_format=summary")
    master = AUD / "master.wav"
    run([FF, "-y", "-i", str(raw), "-af", ln + ",alimiter=limit=0.89:level=false",
         "-ar", "48000", "-ac", "2", "-t", f"{END:.2f}", str(master)])
    print("master.wav ok")


def mux():
    v = OUT / "video.mp4"
    a = AUD / "master.wav"
    final = OUT / OUT_NAME
    run([FF, "-y", "-i", str(v), "-i", str(a), "-map", "0:v", "-map", "1:a",
         "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "44100",
         "-t", f"{END:.2f}", "-movflags", "+faststart", str(final)])
    print("final:", final, final.stat().st_size)



def write_srt():
    words = load_words()
    _, groups = build_captions(words)
    def ts(t):
        h = int(t // 3600); m = int(t % 3600 // 60); sec = t % 60
        return f"{h:02d}:{m:02d}:{sec:06.3f}".replace(".", ",")
    out = []
    for i, g in enumerate(groups, 1):
        t0 = max(0.0, g[0]["t0"] - 0.06)
        t1 = g[-1]["t1"] + 0.14
        if i < len(groups):
            t1 = min(t1, groups[i][0]["t0"] - 0.02)
        out.append(f"{i}\n{ts(t0)} --> {ts(t1)}\n" + " ".join(w["w"].upper() for w in g) + "\n")
    dst = ROOT / "ODDCHAPTER_BRAND" / "11_CONTENT" / "06_UPLOAD" / getattr(CFG, "SRT_NAME", f"{SLUG}.id.srt")
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text("\n".join(out))
    print("srt:", dst, len(groups), "cue")


if __name__ == "__main__":
    cmd = sys.argv[2] if len(sys.argv) > 2 else "all"
    if cmd in ("shots", "all"):
        render_shots(force="--force" in sys.argv)
    if cmd in ("video", "all"):
        render_video()
    if cmd in ("audio", "all"):
        synth_bed(); mix_audio()
    if cmd in ("mux", "all"):
        mux()
    if cmd in ("srt", "all"):
        write_srt()
