#!/usr/bin/env python3
"""Builder Short 9:16 ODDCHAPTER seri "angker" (dokumenter arsip) — ffmpeg murni.

Menerjemahkan aturan Dukun AS v2 / Panduan Teknis ODDCHAPTER ke satu skrip:
  * shot per beat, cut = onset kata - LEAD (0,15 s), Ken Burns selang-seling
  * grade dingin (eq/colorbalance/curves), vignette, grain, flicker
  * caption kinetik ASS (Barlow Condensed ExtraBold 800) di zona aman, kata kunci merah
  * sumber foto selalu diberi tag, kredit di kartu akhir
  * bed audio sintesis (numpy) + ducking sidechain, mix ke -15 LUFS / TP -1,5 dBFS

Pemakaian:
  python3 build_short_angker.py shots|video|audio|mux|all [--force]
"""
import json, os, subprocess, sys
from pathlib import Path

FF = os.environ.get("FFMPEG") or __import__("imageio_ffmpeg").get_ffmpeg_exe()

ROOT = Path(__file__).resolve().parents[2]          # .../content-production
CASE = ROOT / "work" / "sengkon"
IMG = CASE / "img"
SHOTS = CASE / "shots"
AUD = CASE / "audio"
OUT = CASE / "out"
SUB = CASE / "subs.ass"
FONTS = CASE / "fonts"

W, H, FPS = 1080, 1920, 30
END = 116.60                      # durasi total
LEAD = 0.15                       # cut sebelum kata jangkar

RED = "&H002A2AD8&"               # #D82A2A
IVORY = "&H00E0ECF0&"             # #F0ECE0
GREY = "&H00D0D0D0&"

IMG_FILES = {
    "A": "A_kompas_halaman1.jpg",
    "B": "B_sengkon_rsu.jpg",
    "C": "C_karta_dipeluk.jpg",
    "D": "D_sinarharapan.jpg",
    "E": "E_oemar.jpg",
    "G": "G_hasibuan.png",
    "H": "H_gedung_ma.jpg",
}
IMG_DIM = {
    "A": (1024, 576), "B": (1200, 800), "C": (1024, 576), "D": (1280, 963),
    "E": (644, 895), "G": (300, 300), "H": (1600, 1200),
}

# (t0, t1, img, mode, zoom_start, zoom_end, extras)
SHOT_LIST = [
    (0.00,   2.30, "A", "card",   1.00, 1.04, {}),
    (2.30,   8.35, "A", "canvas", 1.00, 1.09, {"tag": "FOTO: ARSIP KOMPAS / KARTONO RYADI · 5 NOV 1980"}),
    (8.35,  12.40, "D", "canvas", 1.09, 1.00, {"tag": "FOTO: SINAR HARAPAN / PERPUSNAS RI · 5 NOV 1980"}),
    (12.40, 17.40, "A", "canvas", 1.00, 1.12, {"top": 1}),
    (17.40, 22.45, "A", "card",   1.06, 1.00, {}),
    (22.45, 26.60, "D", "canvas", 1.00, 1.10, {"focusx": 0.72}),
    (26.60, 30.00, "D", "card",   1.00, 1.06, {}),
    (30.00, 35.80, "A", "canvas", 1.12, 1.00, {}),
    (35.80, 39.60, "H", "canvas", 1.00, 1.08, {"tag": "ILUSTRASI: GEDUNG MAHKAMAH AGUNG RI · WIKIMEDIA"}),
    (39.60, 43.40, "H", "card",   1.08, 1.00, {}),
    (43.40, 46.00, "A", "canvas", 1.00, 1.08, {}),
    (46.00, 49.20, "A", "card",   1.05, 1.00, {}),
    (49.20, 51.80, "H", "canvas", 1.08, 1.00, {}),
    (51.80, 55.20, "A", "canvas", 1.00, 1.10, {"top": 1}),
    (55.20, 56.80, "A", "card",   1.02, 1.06, {}),
    (56.80, 61.20, "D", "canvas", 1.00, 1.14, {}),
    (61.20, 64.40, "A", "card",   1.00, 1.05, {}),
    (64.40, 69.00, "D", "canvas", 1.10, 1.00, {"focusx": 0.30}),
    (69.00, 72.20, "A", "canvas", 1.00, 1.10, {}),
    (72.20, 76.10, "E", "canvas", 1.00, 1.10, {"tag": "FOTO: WIKIMEDIA COMMONS · DOMAIN PUBLIK"}),
    (76.10, 79.40, "E", "card",   1.10, 1.00, {}),
    (79.40, 81.40, "A", "canvas", 1.10, 1.00, {}),
    (81.40, 86.10, "C", "card",   1.00, 1.06, {}),
    (86.10, 88.30, "B", "canvas", 1.00, 1.10, {"tag": "FOTO: ARSIP KOMPAS · RSU BEKASI, 4 NOV 1980"}),
    (88.30, 91.90, "B", "fill",   1.00, 1.10, {}),
    (91.90, 94.10, "C", "canvas", 1.00, 1.09, {"tag": "FOTO: ARSIP KOMPAS · 4 NOV 1980"}),
    (94.10, 99.20, "C", "fill",   1.10, 1.00, {}),
    (99.20, 104.10, "A", "card",  1.00, 1.05, {}),
    (104.10, 106.60, "H", "canvas", 1.00, 1.08, {"tag": "ILUSTRASI: GEDUNG MAHKAMAH AGUNG RI · WIKIMEDIA"}),
    (106.60, 110.90, "H", "card", 1.08, 1.00, {}),
    (110.90, 113.70, "A", "card", 1.00, 1.10, {}),
    (113.70, 116.60, None, "black", 1.0, 1.0, {}),
]

ASS_HEAD = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Sub,Barlow Condensed ExtraBold,112,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,0,0,0,0,100,100,1.5,0,1,8,3,2,60,60,672,1
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


NUM_PHRASES = [
    (["seribu", "sembilan", "ratus", "tujuh", "puluh", "empat"], "1974"),
    (["seribu", "sembilan", "ratus", "tujuh", "puluh", "tujuh"], "1977"),
    (["seribu", "sembilan", "ratus", "delapan", "puluh", "delapan"], "1988"),
    (["seribu", "sembilan", "ratus", "delapan", "puluh", "dua"], "1982"),
    (["seribu", "sembilan", "ratus", "delapan", "puluh"], "1980"),
    (["dua", "belas"], "12"),
]

KEYWORDS = {"SENGKON", "KARTA", "GENUL", "CIPINANG", "PEMBUNUH", "PEMBUNUHNYA", "DISIKSA",
            "TBC", "FINAL", "BEBAS", "SALAH", "PENJARA", "BEKASI", "INKRACHT", "MENOLONG",
            "12", "7", "1974", "1977", "1980", "1982", "1988", "HUKUM"}


def load_words():
    data = json.loads((CASE / "vo_alignment.json").read_text())
    words = [{"w": x["word"], "t0": float(x["start"]), "t1": float(x["end"])} for x in data["words"]]
    merged, i = [], 0
    while i < len(words):
        if words[i]["w"].lower() == "menanda" and i + 1 < len(words) and words[i + 1]["w"].lower().startswith("tangani"):
            merged.append({"w": "menandatangani.", "t0": words[i]["t0"], "t1": words[i + 1]["t1"]})
            i += 2
            continue
        if words[i]["w"].lower() == "apa" and i + 1 < len(words) and words[i + 1]["w"].lower().startswith("-apa"):
            merged.append({"w": "apa-apa.", "t0": words[i]["t0"], "t1": words[i + 1]["t1"]})
            i += 2
            continue
        merged.append(words[i]); i += 1
    words = merged
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
    for k in range(len(out) - 1):
        if out[k]["w"].strip(",.?!").lower() == "tujuh" and out[k + 1]["w"].lower().startswith("tahun"):
            out[k]["w"] = "7"
    return out


def build_captions(words):
    events, group = [], []
    for w in words:
        display = w["w"].strip().rstrip(",.")
        gap = w["t0"] - group[-1]["t1"] if group else 0
        chars = sum(len(g["w"].strip().rstrip(",.")) + 1 for g in group) + len(display)
        end_punct = bool(group) and group[-1]["w"][-1] in ".?"
        if group and (len(group) >= 3 or chars > 22 or gap > 0.30 or end_punct):
            events.append(group); group = []
        group.append({"w": display, "t0": w["t0"], "t1": w["t1"]})
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
            parts.append(f"{{\\c{RED}}}{up}{{\\c&H00FFFFFF&}}" if up in KEYWORDS else up)
        txt = "{\\fscx118\\fscy118\\t(0,90,\\fscx100\\fscy100)}" + " ".join(parts)
        lines.append(ev(t0, t1, "Sub", txt))
    return lines, events


def build_overlays():
    L = []
    L.append(ev(0.35, 2.30, "Kicker", f"{{\\pos(540,700)\\an5\\fs78\\c{IVORY}\\fad(250,0)}}PEMBUNUH ASLINYA"))
    L.append(ev(0.75, 2.30, "Big", f"{{\\pos(540,830)\\an5\\c{RED}\\fad(200,0)\\t(0,2400,\\fscx104\\fscy104)}}SATU PENJARA"))
    L.append(ev(17.55, 22.35, "Kicker", f"{{\\pos(540,660)\\an5\\fs66\\fad(200,200)}}BOJONGSARI, BEKASI"))
    L.append(ev(17.85, 22.35, "Big", f"{{\\pos(540,800)\\an5\\fs200\\c{RED}\\fad(200,200)}}1974"))
    L.append(ev(26.75, 29.90, "Big", "{\\pos(540,780)\\an5\\fs104\\fad(180,180)}MEREKA\\NMENYANGKAL"))
    L.append(ev(39.80, 43.30, "Stamp", "{\\pos(540,400)\\an5\\fs150\\frz-6\\fad(160,0)\\t(0,110,\\fscx94\\fscy94)\\t(110,240,\\fscx100\\fscy100)}OKT 1977"))
    L.append(ev(40.25, 43.30, "Kicker", "{\\pos(540,540)\\an5\\fs58\\fad(200,180)}PN BEKASI · PASAL 338 KUHP"))
    L.append(ev(43.60, 45.95, "Stamp", "{\\pos(540,330)\\an5\\fs76\\frz-4\\fad(140,0)}SENGKON · 12 TAHUN"))
    L.append(ev(46.20, 49.10, "Kicker", "{\\pos(540,470)\\an5\\fs58\\fad(150,0)}KARTA"))
    L.append(ev(46.45, 49.10, "Big", f"{{\\pos(540,610)\\an5\\fs300\\c{RED}\\fad(150,120)}}7"))
    L.append(ev(46.90, 49.10, "Kicker", "{\\pos(540,790)\\an5\\fs54\\fsp8\\c&H00E0ECF0&\\fad(200,120)}TAHUN PENJARA"))
    L.append(ev(55.35, 56.75, "Big", "{\\pos(540,800)\\an5\\fs92\\fad(120,120)}SATU TEMBOK"))
    L.append(ev(61.35, 64.30, "Big", f"{{\\pos(540,700)\\an5\\fs320\\c{RED}\\fad(90,220)\\t(0,140,\\fscx112\\fscy112)\\t(140,400,\\fscx100\\fscy100)}}GENUL"))
    L.append(ev(61.95, 64.30, "Kicker", "{\\pos(540,930)\\an5\\fs56\\fad(300,200)}KEPONAKAN SENGKON · TAHANAN YANG SAMA"))
    L.append(ev(72.35, 76.00, "Big", "{\\pos(540,760)\\an5\\fs92\\fad(180,180)}PINTU SEL\\NTETAP TERKUNCI"))
    L.append(ev(76.25, 79.30, "Stamp", "{\\pos(540,400)\\an5\\fs130\\frz-8\\fad(120,180)}INKRACHT"))
    L.append(ev(76.80, 79.30, "Kicker", "{\\pos(540,540)\\an5\\fs52\\fad(300,180)}PUTUSAN BERKEKUATAN HUKUM TETAP"))
    L.append(ev(81.55, 86.00, "Kicker", "{\\pos(540,660)\\an5\\fs60\\fad(200,180)}LP CIPINANG · ±14.10"))
    L.append(ev(81.85, 86.00, "Big", f"{{\\pos(540,800)\\an5\\fs132\\c{IVORY}\\fad(200,180)}}4 NOVEMBER 1980"))
    L.append(ev(94.30, 96.60, "Kicker", f"{{\\pos(540,1140)\\an5\\fs54\\c{GREY}\\fad(200,200)}}KARTA · FEBRUARI 1982"))
    L.append(ev(99.35, 104.00, "Kicker", f"{{\\pos(540,1140)\\an5\\fs54\\c{GREY}\\fad(200,200)}}SENGKON · MARET 1988"))
    L.append(ev(106.75, 110.85, "Big", "{\\pos(540,720)\\an5\\fs116\\fad(200,180)}PENINJAUAN\\NKEMBALI"))
    L.append(ev(107.20, 110.85, "Kicker", f"{{\\pos(540,910)\\an5\\fs56\\c{RED}\\fad(250,180)}}PERMA NO. 1 TAHUN 1980"))
    L.append(ev(113.80, 116.55, "Big", "{\\pos(540,760)\\an5\\fs104\\fad(280,0)}ODDCHAPTER"))
    L.append(ev(114.05, 116.55, "Kicker", f"{{\\pos(540,880)\\an5\\fs44\\c{RED}\\fad(360,0)}}KASUS NYATA · ARSIP ASLI"))
    L.append(ev(114.40, 116.55, "Credit", f"{{\\pos(540,1010)\\an5\\fs30\\c{GREY}\\fad(420,0)}}Foto: Arsip Kompas / Kartono Ryadi · Sinar Harapan / Perpusnas RI\\NWikimedia Commons (domain publik)\\NSumber: Kompas, Tempo, Tirto, Detik, Historia"))
    return L


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
            f"[bgb][fgv]overlay=(1080-{fw})/2:{y}:shortest=1" + POST + fade
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
        "gblur=sigma=28,eq=brightness=-0.56:saturation=0.18,"
        f"scale=2160:3840,setsar=1,zoompan=z='{zex}':x='{xex}':y='{yex}':d={n}:s=1080x1920:fps={FPS},setsar=1"
        + POST + fade
    )


def render_shots(force=False):
    SHOTS.mkdir(parents=True, exist_ok=True)
    for i, (t0, t1, img, mode, z0, z1, extra) in enumerate(SHOT_LIST):
        dur = t1 - t0
        outp = SHOTS / f"{i:02d}.mp4"
        if outp.exists() and not force:
            continue
        n = max(2, round(dur * FPS))
        if mode == "black":
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
    vo = CASE / "vo_sengkon-karta.mp3"
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
    final = OUT / "SB-SENGKON_short_v1.mp4"
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
    dst = ROOT / "ODDCHAPTER_BRAND" / "11_CONTENT" / "06_UPLOAD" / "AK-EP01.id.srt"
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text("\n".join(out))
    print("srt:", dst, len(groups), "cue")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "all"
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


