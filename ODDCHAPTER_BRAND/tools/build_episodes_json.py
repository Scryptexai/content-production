"""
build_episodes_json.py — content_data.py  ->  remotion/src/episodes.generated.json

Kenapa file ini ada: sebelumnya `episodes.generated.json` tidak punya generator,
jadi judul/hook di layar bisa tertinggal dari script (EP01 sempat menampilkan
judul lama). Sekarang satu sumber: content_data.py. Kalau script berubah,
video ikut berubah setelah `python3 tools/build_episodes_json.py`.

Jalankan:
    python3 tools/build_episodes_json.py
"""

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from content_data import EPISODES  # noqa: E402

OUT = HERE.parent / "10_FILM" / "remotion" / "src" / "episodes.generated.json"

PLATES = {"tower", "vessel", "shelter", "road", "paper", "signal", "plume", "water", "dial", "ridge"}


def build():
    out = []
    for e in EPISODES:
        plate = e.get("plate", "tower")
        if plate not in PLATES:
            raise SystemExit(f"{e['ep']}: plate '{plate}' tidak ada di PlateArt.tsx ({sorted(PLATES)})")
        out.append(
            {
                "id": e["ep"],
                "day": e["day"],
                "slot": e["slot"],
                "jam": e["jam"],
                "series": e["series"],
                "pov": e["pov"],
                "title": e["title"],
                "hook": e["hook"],
                "celah": e.get("celah", ""),
                "gambarMelekat": e.get("gambar_melekat", ""),
                "beats": [{"text": b[1]} if isinstance(b, (list, tuple)) else b for b in e["beats"]],
                "turn": {"quote": e["turn_quote"], "verdict": e["turn_verdict"]},
                "loop": e["loop"],
                "cues": e["cues"],
                "durasi": e["durasi"],
                "plate": plate,
                "photos": [f"plates/{e['ep']}/{n}.jpg" for n in e.get("photos", [])],
                "bed": e.get("bed", ""),
                "sfx": (f"audio/{e['ep']}/sfx.wav" if (HERE.parent / "10_FILM" / "remotion" / "public" / "audio" / e["ep"] / "sfx.wav").exists() else ""),
                "sumber": e["sumber"],
            }
        )
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"written {OUT.relative_to(HERE.parent)}  ({len(out)} episode)")
    for item in out:
        print(f"  {item['id']}  {item['plate']:8s} {item['title']}")


if __name__ == "__main__":
    build()
