#!/usr/bin/env python3
"""
build_long_timing.py — dari SCRIPT.md ke timing.json untuk komposisi 16:9.

Tidak mengarang durasi. Yang dihitung:

  durasi babak = jumlah kata narasi ÷ 150 kata/menit + jeda 0,6 s per pergantian babak

150 kata/menit adalah tempo narasi yang dipakai kanal ini (sama dengan gerbang
`check_longform.py`). Kalau nanti audio sungguhan lebih lambat/cepat, timing.json
yang ditimpa dari durasi audio — bukan sebaliknya. Naskah tidak boleh dipotong
supaya cocok dengan asumsi.

    python3 tools/build_long_timing.py LF01
"""
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
LONGFORM = ROOT / "11_CONTENT" / "07_LONGFORM"

WPM = 150
FPS = 30
GAP_SECONDS = 0.6


def vo_and_plates(block):
    vo, plates = [], []
    for line in block.splitlines():
        if line.startswith(">"):
            body = line.lstrip("> ").strip()
            if body and not body.startswith("**"):
                vo.append(body)
        for m in re.finditer(r"\bV(\d{2})\b", line):
            if line.startswith("`VISUAL`") or line.startswith("`TEKS`") or "VISUAL" in line:
                tag = f"V{m.group(1)}"
                if tag not in plates:
                    plates.append(tag)
    return vo, plates


def parse(script_text):
    raw_acts, current = [], None
    for line in script_text.splitlines():
        if line.startswith("### BABAK"):
            title = line.strip("# ").split("·")[0].strip()
            current = {"title": title, "lines": []}
            raw_acts.append(current)
        elif current is not None:
            current["lines"].append(line)

    acts, t = [], 0.0
    for act in raw_acts:
        vo, plates = vo_and_plates("\n".join(act["lines"]))
        words = len(re.findall(r"\S+", " ".join(vo)))
        seconds = round(words / (WPM / 60), 1)
        start = t
        t = round(t + seconds + GAP_SECONDS, 1)
        acts.append({
            "title": act["title"],
            "words": words,
            "seconds": seconds,
            "start": start,
            "end": t,
            "start_frame": round(start * FPS),
            "frames": round(seconds * FPS),
            "plates": plates,
        })
    return acts, round(t, 1)


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "LF01"
    folders = sorted(LONGFORM.glob(f"{target}_*")) or sorted(LONGFORM.glob(target))
    if not folders:
        sys.exit(f"tidak ada folder {target} di {LONGFORM}")
    folder = folders[0]

    script = (folder / "SCRIPT.md").read_text(encoding="utf-8")
    acts, total = parse(script)

    missing = [p for act in acts for p in act["plates"]
               if not list((folder / "plates").glob(f"{p}_*.jpg"))]
    if missing:
        print("  ! plate belum ada: " + ", ".join(sorted(set(missing))))

    data = {
        "episode": folder.name,
        "canvas": {"width": 1920, "height": 1080, "fps": FPS},
        "wpm": WPM,
        "gap_seconds": GAP_SECONDS,
        "total_seconds": total,
        "total_frames": round(total * FPS),
        "acts": acts,
    }
    out = folder / "timing.json"
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    mm, ss = divmod(round(total), 60)
    print(f"{folder.name}: {len(acts)} babak · {total:.1f} s ({mm}:{ss:02d}) · "
          f"{data['total_frames']} frame @ {FPS} fps")
    for act in acts:
        print(f"  {act['start']:6.1f}–{act['end']:6.1f}  {act['words']:4d} kata  "
              f"{','.join(act['plates']) or '—':28s} {act['title']}")
    print(f"→ {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
