#!/usr/bin/env python3
"""Dari shots/<ID>.json + audio TTS → src/shots.ts untuk Remotion.

Durasi tiap beat diambil dari file audio (dibaca lewat ffmpeg -i). Kalau audio
belum ada, dipakai estimasi dari jumlah karakter (dipakai hanya untuk uji
komposisi; render final wajib memakai audio asli).

    python3 build_timing.py RW1            # satu video
    python3 build_timing.py --all
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
AUDIO = ROOT / "remotion" / "public" / "audio"
SHOTS = ROOT / "shots"
SRC = ROOT / "remotion" / "src"
OUT = ROOT / "out"
FPS = 30
GAP = 0.22          # jeda antar beat (detik)
TAIL = 0.55         # ekor di beat terakhir


def duration(path: Path, ffmpeg: str) -> float:
    """Durasi audio dari stderr ffmpeg -i (tanpa ffprobe)."""
    p = subprocess.run([ffmpeg, "-hide_banner", "-i", str(path)],
                       capture_output=True, text=True)
    m = re.search(r"Duration: (\d+):(\d+):(\d+\.\d+)", p.stderr)
    if not m:
        raise RuntimeError(f"tidak bisa membaca durasi: {path}")
    h, mnt, s = m.groups()
    return int(h) * 3600 + int(mnt) * 60 + float(s)


def estimate(text: str) -> float:
    """Perkiraan kasar bahasa Indonesia: ~15 karakter per detik."""
    return max(2.4, len(text) / 15.0)


def build(shot_id: str, ffmpeg: str, strict: bool, estimate_only: bool = False):
    data = json.loads((SHOTS / f"{shot_id}.json").read_text(encoding="utf-8"))
    frames = []
    t = 0.0
    missing = []
    for b in data["beats"]:
        name = f"{shot_id}-{b['key']}.mp3"
        path = AUDIO / name
        if path.exists() and not estimate_only:
            d = duration(path, ffmpeg)
        else:
            missing.append(name)
            d = estimate(b["vo"])
        start = round(t * FPS)
        end = round((t + d) * FPS)
        frames.append({
            "kind": b["kind"],
            "vo": name,
            "text": b["text"],
            "screen": b.get("screen", []),
            "from": start,
            "to": end,
        })
        t += d + GAP

    total = round((t + TAIL) * FPS)
    props = {
        "id": data["id"],
        "plate": data["plate"],
        "accent": data["accent"],
        "beats": frames,
    }
    if estimate_only:
        props["preview"] = True          # pratinjau desain: audio tidak dimuat
    OUT.mkdir(exist_ok=True)
    (OUT / f"{shot_id}-props.json").write_text(
        json.dumps(props, ensure_ascii=False, indent=2), encoding="utf-8")

    if missing and strict:
        print(f"✗ {shot_id}: audio belum lengkap ({len(missing)} berkas): "
              + ", ".join(missing[:4]) + ("…" if len(missing) > 4 else ""))
        return None

    print(f"{'✓' if not missing else '·'} {shot_id}: {len(frames)} beat · "
          f"{total}-{FPS} = {total / FPS:.1f} dtk"
          + (f" · {len(missing)} beat masih estimasi" if missing else ""))
    return props


def write_ts(all_props: dict):
    body = json.dumps(all_props, ensure_ascii=False, indent=2)
    (SRC / "shots.ts").write_text(
        'import type { ShortProps } from "./Short";\n\n'
        f"export const SHOTS: Record<string, ShortProps> = {body} as const;\n",
        encoding="utf-8")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("ids", nargs="*", default=[])
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--strict", action="store_true",
                    help="gagal kalau ada audio yang belum ada")
    ap.add_argument("--ffmpeg", default="ffmpeg")
    ap.add_argument("--estimate", action="store_true",
                    help="abaikan audio, pakai estimasi panjang teks (pratinjau desain)")
    args = ap.parse_args()

    ids = args.ids or ([p.stem for p in sorted(SHOTS.glob("*.json"))] if args.all else [])
    if not ids:
        print("sebutkan id (mis. RW1) atau --all")
        sys.exit(1)

    existing = {}
    ts = SRC / "shots.ts"
    if ts.exists():
        m = re.search(r"= (\{.*\}) as const;", ts.read_text(encoding="utf-8"), re.S)
        if m:
            existing = json.loads(m.group(1))

    for sid in ids:
        props = build(sid, args.ffmpeg, args.strict, args.estimate)
        if props:
            existing[sid] = props
    write_ts(existing)
    print("→", ts)
