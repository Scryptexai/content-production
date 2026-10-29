#!/usr/bin/env python3
"""Timing video panjang (YouTube 16:9) → src/shots-long.ts.

Durasi tiap blok dibaca dari file audio (ffmpeg -i, tanpa ffprobe).
Di dalam tiap blok, narasi dipecah per kalimat dan tiap kalimat dapat satu
"beat" visual. Waktu tiap beat dibagi menurut panjang karakter kalimat itu,
karena tempo bicara relatif rata. Hasilnya: potongan gambar tiap 3-7 detik,
bukan satu slide yang bertahan 20 detik.

    python3 build_long.py RW1-long            # ukur audio
    python3 build_long.py RW1-long --estimate # pratinjau desain tanpa audio
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


def split_sentences(text: str):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]


def build(shot_id: str, ffmpeg: str, estimate: bool):
    data = json.loads((SHOTS / f"{shot_id}.json").read_text(encoding="utf-8"))
    plan = json.loads((SHOTS / f"{shot_id}-beats.json").read_text(encoding="utf-8"))["beats"]
    t = HEAD
    blocks, missing, beats = [], [], []
    for b in data["blocks"]:
        name = f"{data['id']}-{b['key']}.mp3"
        path = AUDIO / name
        if path.exists() and not estimate:
            d = duration(path, ffmpeg)
        else:
            missing.append(name)
            d = max(4.0, len(b["vo"]) / 15.0)
        b_from, b_to = round(t * FPS), round((t + d) * FPS)
        blocks.append({
            **{k: v for k, v in b.items() if k != "vo"},
            "anim": b.get("anim", ""),
            "vo": name,
            "from": b_from,
            "to": b_to,
        })

        # ---- pecah blok jadi beat visual menurut panjang kalimat
        mine = [p for p in plan if p["block"] == b["key"]]
        sents = split_sentences(b["vo"])
        n = len(sents)
        # `span` = berapa bagian kalimat yang dipakai beat ini. Dipakai untuk
        # memecah satu kalimat panjang jadi dua gambar.
        spans = [float(p.get("span", 1)) for p in mine]
        if abs(sum(spans) - n) > 1e-6:
            if len(mine) == n:
                spans = [1.0] * len(mine)
            else:
                print(f"  ! {b['key']}: span {sum(spans):g} vs {n} kalimat — dibagi rata")
                spans = [n / len(mine)] * len(mine)
        # bobot = porsi kalimat x panjang karakter kalimat itu
        share = []
        acc_s = 0.0
        for sp in spans:
            lo, hi = acc_s, acc_s + sp
            overlap = 0.0
            for i, s in enumerate(sents):
                a, bb = max(lo, i), min(hi, i + 1)
                if bb > a:
                    overlap += (bb - a) * max(1, len(s))
            share.append(max(1.0, overlap))
            acc_s = hi
        total_share = sum(share) or 1
        acc = 0.0
        for i, p in enumerate(mine):
            fr = b_from + round((b_to - b_from) * acc / total_share)
            acc += share[i]
            to_f = b_from + round((b_to - b_from) * acc / total_share)
            beat = {k: v for k, v in p.items() if k != "block"}
            beat["key"] = f"{b['key']}-{i + 1}"
            beat["block"] = b["key"]
            beat["from"] = fr
            beat["to"] = max(fr + 12, to_f)
            beat["plateFrom"] = (i * 97) % 420   # offset berbeda dalam klip plate
            beats.append(beat)

        t += d + GAP

    # Tidak boleh ada celah antar-beat: kalau celah, layar kosong di sela blok.
    # Beat terakhir tiap blok diperpanjang sampai beat berikutnya mulai.
    for i in range(len(beats) - 1):
        beats[i]["to"] = beats[i + 1]["from"]
    if beats:
        beats[-1]["to"] = round((t - GAP + TAIL) * FPS)

    total = round((t - GAP + TAIL) * FPS)
    props = {
        "id": data["id"],
        "tone": data["tone"],
        "chapter": data["chapter"],
        "source": data["source"],
        "preview": bool(missing),
        "blocks": blocks,
        "beats": beats,
    }
    OUT.mkdir(exist_ok=True)
    (OUT / f"{shot_id}-props.json").write_text(
        json.dumps(props, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"{'·' if missing else '✓'} {shot_id}: {len(blocks)} blok · {len(beats)} beat · "
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
