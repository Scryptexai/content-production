#!/usr/bin/env python3
"""Gabung video senyap + musik latar (ducking) → MP4 final + QC.

    python3 mix.py --video out/RW1L-silent.mp4 --music remotion/public/music/ink.mp3 \
                   --out out/RW1L.mp4

QC yang dijalankan: durasi, resolusi, fps, loudness (−16 LUFS ±1,5),
true peak (≤ −1,5 dBTP).
"""
import argparse
import json
import re
import subprocess
import sys


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def probe(ff, path):
    p = run([ff, "-hide_banner", "-i", str(path)])
    out = {}
    m = re.search(r"Duration: (\d+):(\d+):(\d+\.\d+)", p.stderr)
    if m:
        h, mn, s = m.groups()
        out["dur"] = int(h) * 3600 + int(mn) * 60 + float(s)
    m = re.search(r"Video: .*?, (\d+)x(\d+)", p.stderr)
    if m:
        out["w"], out["h"] = int(m.group(1)), int(m.group(2))
    m = re.search(r"(\d+(?:\.\d+)?) fps", p.stderr)
    if m:
        out["fps"] = float(m.group(1))
    return out


def loudness(ff, path):
    p = run([ff, "-hide_banner", "-nostats", "-i", str(path), "-af",
             "loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"])
    m = re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", p.stderr, re.S)
    if not m:
        return None
    d = json.loads(m.group(0))
    return float(d["input_i"]), float(d["input_tp"]), float(d["input_lra"])


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True)
    ap.add_argument("--music", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--music-gain", default="0.26")
    ap.add_argument("--ffmpeg", default="ffmpeg")
    ap.add_argument("--min-sec", type=float, default=10)
    a = ap.parse_args()
    ff = a.ffmpeg

    fc = (
        f"[1:a]volume={a.music_gain},highpass=f=45,lowpass=f=9000,"
        "afade=t=in:st=0:d=2.0[mus];"
        "[mus][0:a]sidechaincompress=threshold=0.05:ratio=8:attack=20:release=380[duck];"
        "[0:a][duck]amix=inputs=2:duration=first:normalize=0,"
        "loudnorm=I=-16:TP=-2.0:LRA=11[a]"
    )
    r = run([ff, "-y", "-hide_banner", "-loglevel", "error",
             "-i", a.video, "-i", a.music,
             "-filter_complex", fc, "-map", "0:v", "-map", "[a]",
             "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
             "-shortest", "-movflags", "+faststart", a.out])
    if r.returncode != 0:
        print("mix gagal:", r.stderr[-500:])
        sys.exit(1)

    info = probe(ff, a.out)
    lr = loudness(ff, a.out)
    ok = True
    problems = []
    if info.get("dur", 0) < a.min_sec:
        problems.append(f"durasi {info.get('dur'):.1f} dtk")
        ok = False
    if (info.get("w"), info.get("h")) not in [(1920, 1080), (1080, 1920)]:
        problems.append(f"resolusi {info.get('w')}x{info.get('h')}")
        ok = False
    if lr:
        if abs(lr[0] + 16) > 1.5:
            problems.append(f"loudness {lr[0]:.1f} LUFS")
            ok = False
        if lr[1] > -1.5:
            problems.append(f"true peak {lr[1]:.1f} dBTP")
            ok = False

    print(f"{'✓' if ok else '✗'} {a.out}")
    print(f"  {info.get('dur', 0):.1f} dtk · {info.get('w')}x{info.get('h')} · "
          f"{info.get('fps')} fps"
          + (f" · {lr[0]:.1f} LUFS · TP {lr[1]:.1f} dBTP · LRA {lr[2]:.1f}" if lr else ""))
    for p in problems:
        print("  · " + p)
    sys.exit(0 if ok else 1)
