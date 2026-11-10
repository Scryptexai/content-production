#!/usr/bin/env python3
"""
measure_audio.py — timing dari audio sungguhan, bukan dari asumsi kata/menit.

`build_long_timing.py` menebak durasi dari jumlah kata. Tebakan itu berguna untuk
menyusun naskah, tapi salah untuk render: narator sungguhan lebih lambat
(terukur 132–143 kata/menit, bukan 150).

Aturan yang dipegang: yang menyesuaikan diri adalah timing, bukan naskah.
Babak yang audionya sudah ada memakai durasi terukur; babak yang belum ada
memakai tempo rata-rata terukur (bukan 150).

    python3 tools/measure_audio.py LF01
"""
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build_long_timing as blt  # noqa: E402

try:
    from mutagen.mp3 import MP3
except ImportError:  # pragma: no cover
    MP3 = None


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "LF01"
    folder = sorted(blt.LONGFORM.glob(f"{target}_*"))[0]
    acts, _ = blt.parse((folder / "SCRIPT.md").read_text(encoding="utf-8"))

    audio = {}
    for i in range(len(acts)):
        path = folder / "audio" / f"act{i}.mp3"
        if path.exists() and MP3 is not None:
            audio[i] = round(MP3(path).info.length, 1)

    if not audio:
        sys.exit("belum ada audio; jalankan build_long_timing.py saja")

    measured_words = sum(acts[i]["words"] for i in audio)
    measured_seconds = sum(audio.values())
    wpm = measured_words / (measured_seconds / 60)
    print(f"tempo terukur: {wpm:.0f} kata/menit dari {len(audio)} babak "
          f"({measured_words} kata, {measured_seconds:.1f} s)")

    t, out_acts = 0.0, []
    for i, act in enumerate(acts):
        if i in audio:
            seconds, source = audio[i], "audio"
        else:
            seconds, source = round(act["words"] / (wpm / 60), 1), "estimasi"
        start = t
        t = round(t + seconds + blt.GAP_SECONDS, 1)
        out_acts.append({
            "title": act["title"],
            "words": act["words"],
            "seconds": seconds,
            "source": source,
            "start": start,
            "end": t,
            "start_frame": round(start * blt.FPS),
            "frames": round(seconds * blt.FPS),
            "plates": act["plates"],
        })

    data = {
        "episode": folder.name,
        "canvas": {"width": 1920, "height": 1080, "fps": blt.FPS},
        "wpm_measured": round(wpm, 1),
        "gap_seconds": blt.GAP_SECONDS,
        "total_seconds": round(t, 1),
        "total_frames": round(t * blt.FPS),
        "complete": len(audio) == len(acts),
        "acts": out_acts,
    }
    (folder / "timing.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n",
                                        encoding="utf-8")

    mm, ss = divmod(round(t), 60)
    print(f"{folder.name}: {t:.1f} s ({mm}:{ss:02d}) · {data['total_frames']} frame · "
          f"{'lengkap' if data['complete'] else f'{len(audio)}/{len(acts)} babak ber-audio'}")
    for a in out_acts:
        print(f"  {a['start']:6.1f}–{a['end']:6.1f}  {a['seconds']:5.1f} s  "
              f"{a['source']:9s} {a['title']}")


if __name__ == "__main__":
    main()
