"""
build_longform.py — satu episode long-form dari VO pemilik, versi 2 (berjeda).

Perubahan v2 (16 Nov 2026, keluhan pemilik: "terasa seperti baca koran tanpa
jeda"):
  · narasi DIPOTONG di jeda bicara (silencedetect), bukan di sembarang tempat,
    lalu diberi JEDA buatan untuk kartu bab / interstitial.
  · setiap potongan VO diverifikasi jatuh di dalam keheningan ≥0,30 dtk; kalau
    tidak, build gagal — supaya tidak ada kata yang terbelah.
  · kartu bab: 2,6 dtk (judul + kicker + sfx), interstitial: 3,0 dtk.
  · caption ikut bergeser karena dihitung ulang dari potongan, bukan dari
    timestamp asli.

Masukan : 11_CONTENT/02_SCRIPT/LONGFORM/EPxx_*.json
Plate   : 10_FILM/assets/SB-EP01/  → disalin ke public/plates/EPxxLF/
Keluaran: src/longform.generated.json  +  public/audio/EPxxLF/mix.wav
"""
import json
import pathlib
import re
import shutil
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
REPO = ROOT.parent
SRC = ROOT / "11_CONTENT" / "02_SCRIPT" / "LONGFORM"
OUT_JSON = ROOT / "10_FILM" / "remotion" / "src" / "longform.generated.json"
PUB = ROOT / "10_FILM" / "remotion" / "public"
FFMPEG, FFPROBE = "ffmpeg", "ffprobe"

CAP_WORDS = 8
MIN_SIL = 0.30
SNAP_MAX = 1.4          # detik: batas geser potongan ke tengah keheningan


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        raise SystemExit("gagal: " + " ".join(cmd[:6]) + "\n" + r.stderr[-1500:])
    return r


def probe_duration(p):
    return float(run([FFPROBE, "-v", "error", "-show_entries", "format=duration",
                      "-of", "default=nw=1:nk=1", str(p)]).stdout.strip())


def silences(path, noise="-32dB", dur=0.30):
    r = subprocess.run([FFMPEG, "-hide_banner", "-nostats", "-i", str(path), "-af",
                        f"silencedetect=noise={noise}:d={dur}", "-f", "null", "-"],
                       capture_output=True, text=True)
    out, cur = [], None
    for line in r.stderr.splitlines():
        m = re.search(r"silence_start: ([\d.]+)", line)
        if m:
            cur = float(m.group(1))
        m = re.search(r"silence_end: ([\d.]+)", line)
        if m and cur is not None:
            out.append((cur, float(m.group(1))))
            cur = None
    return out


def snap(t, sils):
    """Titik potong → tengah keheningan terdekat (maks SNAP_MAX detik)."""
    best, bd = None, 1e9
    for a, b in sils:
        c = (a + b) / 2
        d = abs(c - t)
        if d < bd:
            best, bd = c, d
    if best is not None and bd <= SNAP_MAX and bd > 0:
        return round(best, 3), round(bd, 3)
    return None, None


def chunk(text, max_words=CAP_WORDS):
    text = re.sub(r"\s+", " ", text).strip()
    lines = []
    for p in re.split(r"(?<=[.!?])\s+", text):
        words = p.split()
        if len(words) <= max_words:
            lines.append(p)
            continue
        cur = []
        for w in words:
            cur.append(w)
            if len(cur) >= max_words and (w.endswith(",") or len(cur) >= max_words + 2):
                lines.append(" ".join(cur))
                cur = []
        if cur:
            lines.append(" ".join(cur))
    return [l for l in lines if l.strip()]


def build(ep_id, verbose=False):
    files = sorted(SRC.glob(f"{ep_id}_*.json"))
    data = json.loads(files[0].read_text())
    asset = lambda p: pathlib.Path(p) if pathlib.Path(p).is_absolute() else REPO / p
    vo = asset(data["vo"])
    vo_dur = probe_duration(vo)
    fps = data.get("fps", 30)
    cards = sorted(data.get("cards", []), key=lambda c: c["at"])

    # 1 · potong VO tepat di keheningan
    sils = silences(vo)
    cuts = [("interstitial" if c.get("type") == "interstitial" else f"card{i}", c["at"], c)
            for i, c in enumerate(cards)]
    snapped, fails = [], []
    for name, at, card in cuts:
        s, d = snap(at, sils)
        if s is None:
            fails.append(f"{name}: tidak ada keheningan dalam ±{SNAP_MAX}s dari {at}s")
            s = at
        snapped.append((s, card, at, d))
    if fails:
        for f in fails:
            print("  ✗", f)
        raise SystemExit("potongan VO tidak aman — VO tidak jadi dibelah")

    # 2 · garis waktu = potongan VO di antara kartu (bukan batas blok)
    #     Blok naskah hanya metadata (teks, plate, bab). Kalau potongan dibuat
    #     dari batas blok, sisa 0,1–0,6 dtk muncul sebagai segmen hantu.
    blocks = data["segments"]
    cut_times = [c[0] for c in snapped]
    # potongan juga dipecah saat layout berubah (footage → diagram), walau tidak
    # ada kartu di antaranya. Tanpa ini dua blok berbeda layout tergabung dan
    # salah satunya hilang (mis. blok diagram kehilangan kartu-kartunya).
    def signature(b):
        dg = b.get("diagram") or {}
        return (b.get("layout", "footage"), dg.get("title", ""), tuple(b.get("footage") or ()))

    layout_edges = []
    for b0, b1 in zip(blocks, blocks[1:]):
        # dua blok diagram berturut-turut tetap harus dipisah kalau diagramnya
        # berbeda — kalau tidak, diagram blok kedua tidak pernah tampil.
        if signature(b0) != signature(b1):
            layout_edges.append(b1["start"])
    # Potongan kartu TIDAK boleh dibuang (kalau batasnya hilang, kartunya ikut
    # hilang dan VO jadi lebih pendek). Yang dibuang hanya batas layout yang
    # menempel terlalu dekat — ini sumber sliver 0,3–0,9 dtk.
    edges = sorted({0.0, *cut_times, vo_dur})
    for e in sorted(layout_edges):
        if all(abs(e - x) >= 2.5 for x in edges):
            edges.append(e)
    edges = sorted(edges)

    cards_by_orig = {round(c[0], 3): c[1] for c in snapped}

    def block_at(t):
        for bi, b in enumerate(blocks):
            if b["start"] <= t < b["end"]:
                return bi, b
        return len(blocks) - 1, blocks[-1]

    pieces = []
    # preflight: plate harus ada. Render 50 menit tidak boleh gugur karena satu
    # nama berkas salah (pernah terjadi: barruel.jpg 404 di tengah render).
    avail = {f.name for f in (ROOT / "10_FILM" / "assets" / f"SB-{ep_id}").glob("*.jpg")}
    missing = sorted({f for b in blocks for f, _ in b["plates"] if f not in avail})
    if missing:
        raise SystemExit("plate tidak ada di assets/SB-" + ep_id + ": " + ", ".join(missing))

    for k in range(len(edges) - 1):
        a, b = edges[k], edges[k + 1]
        if b - a < 0.05:
            continue
        bi, blk = block_at((a + b) / 2)
        span = blk["end"] - blk["start"]
        pieces.append({
            "block": bi, "start": a, "end": b,
            "shareA": (a - blk["start"]) / span, "shareB": (b - blk["start"]) / span,
            "card": cards_by_orig.get(round(a, 3)),
        })

    # 3 · susun garis waktu baru
    t, timeline_cards, timeline_segments, audio_map = 0.0, [], [], []
    for p_ in pieces:
        c = p_["card"]
        if c:
            dur = float(c.get("dur", 2.6))
            timeline_cards.append({
                "type": c.get("type", "chapter"), "num": c.get("num", 0),
                "kicker": c.get("kicker", ""), "title": c.get("title", ""),
                "sub": c.get("sub", ""), "start": round(t, 3), "end": round(t + dur, 3),
                "dur": dur, "atOrig": p_["start"],
            })
            t += dur
        blk = blocks[p_["block"]]
        dur = p_["end"] - p_["start"]
        # plate: pilih slot yang jatuh di rentang potongan ini
        n = len(blk["plates"])
        picks = [f for k2, (f, fit) in enumerate(blk["plates"])
                 if (k2 + 1) / n > p_["shareA"] + 1e-6 and k2 / n < p_["shareB"] - 1e-6]
        if not picks:
            k2 = min(n - 1, int(p_["shareA"] * n))
            picks = [blk["plates"][k2][0]]
        fits = {f: fit for f, fit in blk["plates"]}
        audio_map.append((round(t, 3), p_["start"], p_["end"]))
        layout = blk.get("layout", "footage")
        seg = {
            "i": p_["block"], "chapter": blk["chapter"], "start": round(t, 3),
            "end": round(t + dur, 3),
            "startFrame": round(t * fps), "endFrame": round((t + dur) * fps),
            "origStart": p_["start"], "origEnd": p_["end"],
            "layout": layout,
            "plates": [{"plate": f"plates/{ep_id}LF/{f}", "fit": fits[f]} for f in picks],
            "captions": [],
        }
        if layout == "diagram":
            dg = dict(blk.get("diagram") or {})
            dg["cards"] = [
                {"plate": f"plates/{ep_id}LF/{c['plate']}", "label": c.get("label", ""),
                 "sub": c.get("sub", ""), "num": k + 1}
                for k, c in enumerate(dg.get("cards", []))
            ]
            seg["diagram"] = dg
        else:
            # footage: potong jadi beberapa klip ±6,5 dtk, klip diputar bergiliran
            clips = blk.get("footage") or []
            ncut = max(1, round(dur / 6.5))
            cuts = []
            for k in range(ncut):
                clip = clips[k % len(clips)] if clips else None
                if not clip:
                    continue
                cuts.append({
                    "clip": f"footage/{clip}",
                    "start": round(t + dur * k / ncut, 3),
                    "end": round(t + dur * (k + 1) / ncut, 3),
                    "offset": round((k * 2.3) % 3.5, 2),
                    "motion": (p_["block"] + k) % 4,
                })
            seg["footage"] = cuts
        timeline_segments.append(seg)
        t += dur
    total = round(t, 3)

    # 4 · caption: chunk dari semua blok, lalu tempel ke potongan yang memuat
    #     titik tengahnya. Dilakukan global (bukan per blok) karena satu potongan
    #     bisa memuat dua blok sekaligus ketika tidak ada kartu di antaranya.
    caps_all = []
    for b in blocks:
        lines = chunk(b["text"])
        tot = sum(len(l) for l in lines) or 1
        cur = b["start"]
        for l in lines:
            d = len(l) / tot * (b["end"] - b["start"])
            caps_all.append({"t0": cur, "t1": cur + d, "text": l})
            cur += d
    for seg in timeline_segments:
        for c in caps_all:
            mid = (c["t0"] + c["t1"]) / 2
            if not (seg["origStart"] <= mid < seg["origEnd"]):
                continue
            t0 = seg["start"] + max(0.0, c["t0"] - seg["origStart"])
            t1 = seg["start"] + min(seg["end"] - seg["start"], c["t1"] - seg["origStart"])
            if t1 - t0 > 0.3:
                seg["captions"].append({"t0": round(t0, 3), "t1": round(t1, 3), "text": c["text"]})

    # 5 · potongan plate + preset gerak di dalam segmen
    for seg in timeline_segments:
        n = len(seg["plates"])
        span = seg["end"] - seg["start"]
        for k, pl in enumerate(seg["plates"]):
            pl["start"] = round(seg["start"] + span * k / n, 3)
            pl["end"] = round(seg["start"] + span * (k + 1) / n, 3)
            pl["motion"] = (seg["i"] + k) % 5

    # 6 · audio: VO dipotong + jeda + musik ducking + sfx di kartu
    outdir = PUB / "audio" / f"{ep_id}LF"
    outdir.mkdir(parents=True, exist_ok=True)
    plates_out = PUB / "plates" / f"{ep_id}LF"
    plates_out.mkdir(parents=True, exist_ok=True)
    for f in (ROOT / "10_FILM" / "assets" / f"SB-{ep_id}").glob("*.jpg"):
        shutil.copy(f, plates_out / f.name)

    # footage Coverr (hasil GitHub Actions) → public/footage
    fsrc = REPO / "footage"
    fdst = PUB / "footage"
    fdst.mkdir(parents=True, exist_ok=True)
    nfoot = 0
    if fsrc.exists():
        for f in fsrc.glob("*.mp4"):
            if not (fdst / f.name).exists():
                shutil.copy(f, fdst / f.name)
            nfoot += 1
    need = sorted({c["clip"].split("/", 1)[1] for s_ in timeline_segments
                   for c in s_.get("footage", [])})
    gone = [c for c in need if not (fdst / c).exists()]
    if gone:
        raise SystemExit("footage tidak ada di public/footage: " + ", ".join(gone))

    sfx = asset(data["sfx"])
    sfx_rev = outdir / "sfx_rev.wav"
    run([FFMPEG, "-y", "-i", str(sfx), "-af", "areverse", "-ar", "48000", "-ac", "2",
         "-c:a", "pcm_s16le", str(sfx_rev)])

    filt, labels = [], []
    # satu label filter hanya boleh dipakai SEKALI di ffmpeg → asplit dulu
    npiece = len(audio_map)
    filt.append(f"[0:a]aresample=48000,aformat=channel_layouts=stereo,asplit={npiece}" +
                "".join(f"[vs{k}]" for k in range(npiece)))
    for k, (ns, os_, oe) in enumerate(audio_map):
        d = oe - os_
        fade = min(0.08, d / 4)
        filt.append(f"[vs{k}]atrim={os_}:{oe},asetpts=N/SR/TB,"
                    f"afade=t=in:st=0:d={fade:.3f},afade=t=out:st={d - fade:.3f}:d={fade:.3f}[p{k}]")
        labels.append(f"[p{k}]")
    # jeda untuk kartu (diletakkan sebelum potongan yang mengikutinya)
    gaps = {round(c["end"], 3): c["dur"] for c in timeline_cards}
    # susun ulang: jeda terjadi sebelum potongan yang new_start-nya = card.end
    seq, prev_end = [], 0.0
    for k, (ns, os_, oe) in enumerate(audio_map):
        g = round(ns - prev_end, 3)
        if g > 0.01:
            filt.append(f"anullsrc=r=48000:cl=stereo,atrim=0:{g}[g{k}]")
            seq.append(f"[g{k}]")
        seq.append(f"[p{k}]")
        prev_end = ns + (oe - os_)
    filt.append("".join(seq) + f"concat=n={len(seq)}:v=0:a=1[voice]")
    filt.append("[voice]loudnorm=I=-16:TP=-1.5:LRA=11[voLN]")

    # sfx: satu dentuman di tiap kartu (paper = reversed, interstitial = normal)
    sfx_labels = []
    n_int = sum(1 for c in timeline_cards if c["type"] == "interstitial")
    n_rev = len(timeline_cards) - n_int
    if n_int:
        filt.append("[1:a]aresample=48000,aformat=channel_layouts=stereo,"
                    f"asplit={n_int}" + "".join(f"[ia{k}]" for k in range(n_int)))
    if n_rev:
        filt.append("[2:a]aresample=48000,aformat=channel_layouts=stereo,"
                    f"asplit={n_rev}" + "".join(f"[ra{k}]" for k in range(n_rev)))
    ii = ri = 0
    for k, c in enumerate(timeline_cards):
        if c["type"] == "interstitial":
            src, ii = f"[ia{ii}]", ii + 1
        else:
            src, ri = f"[ra{ri}]", ri + 1
        filt.append(f"{src}adelay={int(c['start'] * 1000)}|{int(c['start'] * 1000)}[sx{k}]")
        sfx_labels.append(f"[sx{k}]")
    if sfx_labels:
        n = len(sfx_labels)
        filt.append("".join(sfx_labels) + f"amix=inputs={n}:dropout_transition=0,volume={n}[sfxall]")
        filt.append("[voLN][sfxall]amix=inputs=2:dropout_transition=0,volume=2[voice2]")
        voice = "[voice2]"
    else:
        voice = "[voLN]"

    music = asset(data["music"])
    # Musik harus terasa sepanjang video. Sebelumnya -20 dB + ducking rasio 12
    # membuat musik nyaris hilang tiap VO masuk, jadi terdengar "hanya di beberapa
    # bagian". Sekarang musik -14 dB dengan ducking ringan (rasio 5).
    filt.append(f"[3:a]atrim=0:{total:.3f},volume=-14dB,aresample=48000,"
                f"aformat=channel_layouts=stereo[mus]")
    filt.append(f"{voice}asplit=2[vkey][vmix]")
    filt.append("[mus][vkey]sidechaincompress=threshold=0.05:ratio=5:attack=12:release=520[musd]")
    filt.append("[musd][vmix]amix=inputs=2:dropout_transition=0,volume=2[mixed]")
    filt.append(f"[mixed]volume=-2dB,alimiter=limit=0.85,volume=-1dB,atrim=0:{total:.3f}[out]")

    mix = outdir / "mix.wav"
    run([FFMPEG, "-y", "-i", str(vo), "-i", str(sfx), "-i", str(sfx_rev),
         "-stream_loop", "-1", "-i", str(music),
         "-filter_complex", ";".join(filt), "-map", "[out]",
         "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", str(mix)])

    # 7 · json untuk Remotion
    payload = {
        "id": data["id"], "series": data.get("series", "ANEH"), "title": data["title"],
        "vo": f"audio/{ep_id}LF/mix.wav", "fps": fps, "duration": total,
        "totalFrames": round(total * fps), "width": 1920, "height": 1080,
        "cards": timeline_cards,
        "segments": timeline_segments, "sumber": data.get("sumber", {}),
    }
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=1))

    if verbose:
        print(f"VO asli {vo_dur:.2f}s → {total:.2f}s ({len(timeline_cards)} kartu, "
              f"+{total - vo_dur:.1f}s jeda)")
        for c in timeline_cards:
            print(f"  kartu {c['start']:7.2f}–{c['end']:7.2f}  {c['type']:12s} {c['title']}")
        for s in timeline_segments:
            print(f"  seg   {s['start']:7.2f}–{s['end']:7.2f}  {s['chapter'][:26]:26s} "
                  f"{len(s['captions']):2d} caption · {len(s['plates'])} plate")
    print(f"mix  : {mix.relative_to(ROOT)}  ({mix.stat().st_size / 1e6:.1f} MB)")
    print(f"json : {OUT_JSON.relative_to(ROOT)}  {total:.2f}s · {round(total * fps)} frame")
    return 0


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    sys.exit(build(args[0] if args else "EP01", "-v" in sys.argv or "--verbose" in sys.argv))
