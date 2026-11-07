"""
build_timing.py — timing.json untuk Remotion.

Sumber kebenaran waktu. Dua mode:

1. ESTIMASI (sekarang): durasi tiap segmen dihitung dari jumlah kata pada
   kecepatan baca 2,45 kata/detik (Indonesia, narasi tenang) + jeda.
2. AUDIO (setelah narasi jadi): kalau public/audio/<EP>/<segmen>.mp3 ada,
   durasinya dibaca dari ffprobe dan menggantikan estimasi. Ini yang wajib
   dipakai untuk render final — caption harus ikut audio nyata, bukan perkiraan.

Output: remotion/src/timing.generated.json
"""

import json
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
from content_data import EPISODES  # noqa: E402

AUDIO_DIR = ROOT / "10_FILM" / "remotion" / "public" / "audio"
OUT = ROOT / "10_FILM" / "remotion" / "src" / "timing.generated.json"
FPS = 30
WPS = 2.45          # kata per detik
GAP = 0.30          # jeda antar segmen
HOOK_HOLD = 0.5     # nafas setelah hook
TAIL = 1.2          # ekor sebelum loop menutup


def _ffmpeg():
    """ffprobe tidak ada di image ini; ffmpeg ada lewat imageio_ffmpeg."""
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return "ffmpeg"


def audio_duration(path):
    """Durasi audio nyata. ffprobe kalau ada, kalau tidak parse stderr ffmpeg."""
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
            capture_output=True, text=True, check=True,
        )
        return float(out.stdout.strip())
    except Exception:
        pass
    try:
        out = subprocess.run([_ffmpeg(), "-i", str(path)], capture_output=True, text=True)
        for line in out.stderr.splitlines():
            if "Duration:" in line:
                hms = line.split("Duration:")[1].split(",")[0].strip()
                h, m, sec = hms.split(":")
                return int(h) * 3600 + int(m) * 60 + float(sec)
    except Exception:
        return None
    return None


def dur_of(text, wps=WPS):
    return max(1.6, len(text.split()) / wps)


def build(ep):
    segs = []

    def add(kind, text, key, part=None):
        path = AUDIO_DIR / ep["ep"] / f"{key}.mp3"
        measured = audio_duration(path) if path.exists() else None
        segs.append({
            "kind": kind,
            "part": part,
            "key": key,
            "text": text,
            "dur": round(measured if measured else dur_of(text), 3),
            "measured": bool(measured),
        })

    add("hook", ep["hook"], "00_hook")
    for i, (part, txt) in enumerate(ep["beats"]):
        add("beat", txt, f"{i + 1:02d}_{part}", part)

    add("loop", ep["loop"], "99_loop")

    # kutipan + pembalik dipasang di segmen turn pertama
    for s in segs:
        if s["part"] == "turn":
            s["quote"] = ep.get("turn_quote", "")
            s["verdict"] = ep.get("turn_verdict", "")
            break

    # cue menempel di beat tension, satu per satu, lalu di consequence kalau sisa
    cues = list(ep["cues"])
    for part in ("tension", "consequence", "setup"):
        for s in segs:
            if cues and s.get("part") == part and "cue" not in s:
                s["cue"] = cues.pop(0)
        if not cues:
            break

    t = 0.6  # lead-in
    for s in segs:
        s["start"] = round(t, 3)
        t += s["dur"] + GAP
    total = round(t + TAIL, 3)

    for s in segs:
        s["startFrame"] = round(s["start"] * FPS)
        s["durFrames"] = max(1, round(s["dur"] * FPS))

    return {
        "ep": ep["ep"],
        "title": ep["title"],
        "series": ep["series"],
        "slot": ep["slot"],
        "fps": FPS,
        "total": total,
        "totalFrames": round(total * FPS),
        "audioMeasured": all(s["measured"] for s in segs),
        "segments": segs,
    }


if __name__ == "__main__":
    ids = sys.argv[1:] or [e["ep"] for e in EPISODES]
    out = {}
    for ep in EPISODES:
        if ep["ep"] in ids:
            out[ep["ep"]] = build(ep)
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2))
    for k, v in out.items():
        print(f"{k}: {v['total']:.1f}s  {v['totalFrames']} frames  "
              f"audio={'measured' if v['audioMeasured'] else 'estimated'}  "
              f"target_script={[e['durasi'] for e in EPISODES if e['ep']==k][0]}s")
    print("wrote", OUT.relative_to(ROOT))
