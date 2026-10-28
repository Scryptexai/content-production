#!/usr/bin/env python3
"""Timing video panjang (YouTube 16:9) → src/shots-long.ts.

Durasi tiap blok dibaca dari file audio (ffmpeg -i, tanpa ffprobe).

    python3 build_long.py RW1-long           # ukur audio
    python3 build_long.py RW1-long --estimate  # pratinjau desain tanpa audio
"""
import argparse
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent
AUDIO = ROOT / "remotion" / "public" / "audio"
SHOTS = ROOT / "shots"
SRC = ROOT / "remotion" / "src"
OUT = ROOT / "out"
FPS = 30
GAP = 0.45
HEAD = 0.8
TAIL = 1.6


def duration(path: Path, ffmpeg: str) -> float:
    p = subprocess.run([ffmpeg, "-hide_banner", "-i", str(path)],
                       capture_output=True, text=True)
    m = re.search(r"Duration: (\d+):(\d+):(\d+\.\d+)", p.stderr)
    if not m:
        raise RuntimeError(f"tidak bisa membaca durasi: {path}")
    h, mn, s = m.groups()
    return int(h) * 3600 + int(mn) * 60 + float(s)


def build(shot_id: str, ffmpeg: str, estimate: bool):
    data = json.loads((SHOTS / f"{shot_id}.json").read_text(encoding="utf-8"))
    t = HEAD
    blocks, missing = [], []
    for b in data["blocks"]:
        name = f"{data['id']}-{b['key']}.mp3"
        path = AUDIO / name
        if path.exists() and not estimate:
            d = duration(path, ffmpeg)
        else:
            missing.append(name)
            d = max(4.0, len(b["vo"]) / 15.0)
        blocks.append({
            **{k: v for k, v in b.items() if k != "vo"},
            "vo": name,
            "from": round(t * FPS),
            "to": round((t + d) * FPS),
        })
        t += d + GAP

    total = round((t - GAP + TAIL) * FPS)
    props = {
        "id": data["id"],
        "tone": data["tone"],
        "chapter": data["chapter"],
        "source": data["source"],
        "preview": bool(missing),
        "blocks": blocks,
    }
    OUT.mkdir(exist_ok=True)
    (OUT / f"{shot_id}-props.json").write_text(
        json.dumps(props, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"{'·' if missing else '✓'} {shot_id}: {len(blocks)} blok · "
          f"{total / FPS:.1f} dtk ({total / FPS / 60:.1f} mnt)"
          + (f" · {len(missing)} blok estimasi" if missing else ""))
    return props


def write_ts(props: dict):
    body = json.dumps(props, ensure_ascii=False, indent=2)
    (SRC / "shots-long.ts").write_text(
        'import type { LongProps } from "./LongForm";\n\n'
        f"export const LONG: LongProps = {body} as unknown as LongProps;\n",
        encoding="utf-8")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("id")
    ap.add_argument("--estimate", action="store_true")
    ap.add_argument("--ffmpeg", default="ffmpeg")
    a = ap.parse_args()
    write_ts(build(a.id, a.ffmpeg, a.estimate))
    print("→", SRC / "shots-long.ts")
