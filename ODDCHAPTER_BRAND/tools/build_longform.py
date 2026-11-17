"""
build_longform.py — satu episode long-form dari VO pemilik.

Beda dengan build_timing.py (short, VO dipecah jadi 9 file): di sini narasi
adalah SATU berkas bersambung yang panjangnya 5–11 menit. Yang memotong gambar
adalah timestamp pemilik, bukan estimasi.

Masukan:
    11_CONTENT/02_SCRIPT/LONGFORM/EPxx_*.json
        id, title, vo, music, sfx, segments[{start, end, chapter, plates, text}]

Keluaran:
    10_FILM/remotion/src/longform.generated.json   (dibaca LongForm.tsx)
    10_FILM/remotion/public/audio/EPxxLF/mix.wav   (VO + musik ducked + sfx)

Aturan yang dijaga skrip ini (gagal keras, bukan saran):
  1. Segmen mulai di detik 0, bersambung, dan berakhir tepat di durasi VO.
     Celah > 0,3 dtk berarti ada bagian narasi tanpa gambar — ditolak.
  2. Tiap segmen punya minimal satu plate dan minimal satu baris caption.
  3. Tidak ada teks yang ditulis ulang di sini: caption adalah potongan
     transkrip pemilik, jadi layar tidak pernah lebih pintar dari narasi.

Campuran audio (AUDIO PRODUCTION §12 — VO dulu, lalu efek, musik, ambience):
  VO      loudnorm ke −16 LUFS (VO pemilik −25,2 LUFS, jadi dinaikkan)
  musik   −18 dB relatif, di-ducking sidechain −14 dB saat VO bicara
  sfx     +12 dB, ditempel di penanda pemilik (bukan di setiap potongan)

Jalankan: python3 tools/build_longform.py EP01 [-v]
"""
import json
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
SRC = ROOT / "11_CONTENT" / "02_SCRIPT" / "LONGFORM"
OUT_JSON = ROOT / "10_FILM" / "remotion" / "src" / "longform.generated.json"
PUB = ROOT / "10_FILM" / "remotion" / "public"
FFMPEG = "ffmpeg"
FFPROBE = "ffprobe"

CAP_WORDS = 9          # kata per baris caption
MAX_GAP = 0.30         # detik


def run(cmd, **kw):
    return subprocess.run(cmd, check=True, capture_output=True, text=True, **kw)


def probe_duration(path):
    out = run([FFPROBE, "-v", "error", "-show_entries", "format=duration",
               "-of", "default=nw=1:nk=1", str(path)]).stdout.strip()
    return float(out)


def chunk(text, max_words=CAP_WORDS):
    """Potong transkrip jadi baris caption: ikut tanda baca, lalu jumlah kata."""
    text = re.sub(r"\s+", " ", text).strip()
    parts = re.split(r"(?<=[.!?])\s+", text)
    lines = []
    for p in parts:
        words = p.split()
        if len(words) <= max_words:
            lines.append(p)
            continue
        # kalimat panjang: pecah di koma terdekat, kalau tidak ada di tengah
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
    if not files:
        raise SystemExit(f"tidak ada naskah long-form untuk {ep_id} di {SRC}")
    data = json.loads(files[0].read_text())

    REPO = ROOT.parent
    def asset(p):
        q = pathlib.Path(p)
        return q if q.is_absolute() else (REPO / q)
    vo = asset(data["vo"])
    if not vo.exists():
        raise SystemExit(f"VO tidak ada: {vo}")
    dur = probe_duration(vo)
    segs = data["segments"]
    fails = []

    # 1 · sambungan timestamp
    if segs[0]["start"] > 0.001:
        fails.append(f"segmen pertama mulai di {segs[0]['start']}, bukan 0")
    last_end = segs[-1]["end"]
    if abs(last_end - dur) > 0.5:
        fails.append(f"segmen terakhir berakhir di {last_end}s, VO {dur:.2f}s")
    for a, b in zip(segs, segs[1:]):
        gap = b["start"] - a["end"]
        if abs(gap) > MAX_GAP:
            fails.append(f"celah {gap:+.2f}s antara '{a['chapter']}' dan '{b['chapter']}'")
    for s in segs:
        if s["end"] <= s["start"]:
            fails.append(f"segmen '{s['chapter']}' durasinya ≤ 0")
        if not s.get("plates"):
            fails.append(f"segmen '{s['chapter']}' tanpa plate")
        if not chunk(s.get("text", "")):
            fails.append(f"segmen '{s['chapter']}' tanpa caption")

    # 2 · caption + peta plate
    fps = data.get("fps", 30)
    built = []
    for i, s in enumerate(segs):
        lines = chunk(s["text"])
        t0, t1 = s["start"], s["end"]
        total_chars = sum(len(l) for l in lines) or 1
        cur = t0
        caps = []
        for l in lines:
            share = len(l) / total_chars * (t1 - t0)
            caps.append({"t0": round(cur, 3), "t1": round(cur + share, 3), "text": l})
            cur += share
        plates = s["plates"]
        # plate kedua mulai di tengah segmen, supaya gambar ikut berubah walau
        # timestamp pemilik hanya memberi satu blok narasi
        cuts = []
        for k, (f, fit) in enumerate(plates):
            st = t0 + (t1 - t0) * (k / len(plates))
            en = t0 + (t1 - t0) * ((k + 1) / len(plates))
            cuts.append({"plate": f"plates/{ep_id}LF/{f}", "fit": fit,
                         "start": round(st, 3), "end": round(en, 3)})
        built.append({
            "i": i, "chapter": s["chapter"], "start": t0, "end": t1,
            "startFrame": round(t0 * fps), "endFrame": round(t1 * fps),
            "cuts": cuts, "captions": caps,
        })

    # 3 · audio mix
    # ffmpeg di sandbox ini versi lama: `amix` belum punya opsi normalize, jadi
    # jumlah dibuat eksplisit (amix membagi rata jumlah input → dikali lagi).
    outdir = PUB / "audio" / f"{ep_id}LF"
    outdir.mkdir(parents=True, exist_ok=True)
    mix = outdir / "mix.wav"
    music = asset(data["music"]) if data.get("music") else None
    sfx = asset(data["sfx"]) if data.get("sfx") else None
    cues = data.get("sfx_cues", [])

    inputs = ["-i", str(vo)]
    filt = ["[0:a]loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000,"
            "aformat=channel_layouts=stereo[vo]"]
    idx = 1
    sfx_label = None
    if sfx and sfx.exists() and cues:
        inputs += ["-i", str(sfx)]
        n = len(cues)
        filt.append(f"[{idx}:a]volume=12dB,aresample=48000,"
                    f"aformat=channel_layouts=stereo,asplit={n}" +
                    "".join(f"[x{k}]" for k in range(n)))
        for k, c in enumerate(cues):
            filt.append(f"[x{k}]adelay={int(c * 1000)}|{int(c * 1000)}[s{k}]")
        filt.append("".join(f"[s{k}]" for k in range(n)) +
                    f"amix=inputs={n}:dropout_transition=0,volume={n}[sfx]")
        sfx_label = "[sfx]"
        idx += 1
    if sfx_label:
        filt.append(f"[vo]{sfx_label}amix=inputs=2:dropout_transition=0,volume=2[voice]")
    else:
        filt.append("[vo]anull[voice]")

    if music and music.exists():
        inputs += ["-stream_loop", "-1", "-i", str(music)]
        filt.append(f"[{idx}:a]atrim=0:{dur:.3f},volume=-18dB,aresample=48000,"
                    f"aformat=channel_layouts=stereo[mus]")
        filt.append("[voice]asplit=2[vkey][vmix]")
        filt.append("[mus][vkey]sidechaincompress=threshold=0.03:ratio=12:attack=8:"
                    "release=420[musd]")
        filt.append("[musd][vmix]amix=inputs=2:dropout_transition=0,volume=2[mixed]")
        last = "[mixed]"
    else:
        last = "[voice]"

    filt.append(f"{last}volume=-2dB,alimiter=limit=0.85,volume=-1dB,atrim=0:{dur:.3f}[out]")
    cmd = [FFMPEG, "-hide_banner", "-loglevel", "error", "-y", *inputs,
           "-filter_complex", ";".join(filt), "-map", "[out]",
           "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", str(mix)]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        raise SystemExit("ffmpeg gagal:\n" + res.stderr[-1200:])

    # 4 · tulis json untuk Remotion
    payload = {
        "id": data["id"], "series": data.get("series", "ANEH"), "title": data["title"],
        "vo": f"audio/{ep_id}LF/mix.wav", "fps": fps, "duration": round(dur, 3),
        "totalFrames": round(dur * fps), "segments": built,
        "sumber": data.get("sumber", {}),
    }
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=1))

    if verbose:
        print(f"naskah : {files[0].name}")
        print(f"VO     : {vo.name}  {dur:.2f}s  ({dur / 60:.2f} menit)")
        for b in built:
            print(f"  {int(b['start']) // 60}:{int(b['start']) % 60:02d}–"
                  f"{int(b['end']) // 60}:{int(b['end']) % 60:02d}  "
                  f"{b['chapter']:24s} {len(b['captions']):2d} caption · "
                  f"{len(b['cuts'])} plate")
    print(f"mix    : {mix.relative_to(ROOT)}  ({mix.stat().st_size / 1e6:.1f} MB)")
    print(f"json   : {OUT_JSON.relative_to(ROOT)}  {len(built)} segmen · "
          f"{round(dur * fps)} frame")
    for f in fails:
        print(f"  ✗ {f}")
    return 0 if not fails else 1


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    sys.exit(build(args[0] if args else "EP01", "-v" in sys.argv or "--verbose" in sys.argv))
