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
GAP = 0.42          # jeda antar segmen
HOOK_HOLD = 0.5     # nafas setelah hook
TAIL = 1.6          # ekor sebelum loop menutup


def audio_duration(path):
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
            capture_output=True, text=True, check=True,
        )
        return float(out.stdout.strip())
    except Exception:
        return None


def dur_of(text, wps=WPS):
    return max(1.6, len(text.split()) / wps)


def build(ep):
    segs = []

    def add(kind, text, key):
        path = AUDIO_DIR / ep["ep"] / f"{key}.mp3"
        measured = audio_duration(path) if path.exists() else None
        segs.append({
            "kind": kind,
            "key": key,
            "text": text,
            "dur": round(measured if measured else dur_of(text), 3),
            "measured": bool(measured),
        })

    add("hook", ep["hook"], "00_hook")
    for i, (t, txt) in enumerate(ep["beats"]):
        add("beat", txt, f"{i + 1:02d}_beat")
    add("turn", ep["turn"], "90_turn")
    segs[-1]["quote"] = ep.get("turn_quote", "")
    segs[-1]["verdict"] = ep.get("turn_verdict", "")
    add("loop", ep["loop"], "99_loop")

    # cue diambil berurutan, satu cue per satu-dua segmen beat
    cues = ep["cues"]
    beat_idx = [i for i, s in enumerate(segs) if s["kind"] == "beat"]
    for n, i in enumerate(beat_idx):
        if n % 2 == 0 and n // 2 < len(cues):
            segs[i]["cue"] = cues[n // 2]

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
