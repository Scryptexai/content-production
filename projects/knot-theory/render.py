#!/usr/bin/env python3
"""Render satu (atau semua) video Knot Theory: Remotion → mix audio → QC.

    python3 render.py RW1
    python3 render.py --all
    python3 render.py RW1 --dry        # cek durasi & timing tanpa render

Tahap:
1. build_timing.py  → src/shots.ts (durasi tiap beat dari audio TTS)
2. remotion render  → out/<ID>-silent.mp4 (VO sudah di dalamnya)
3. ffmpeg           → musik + ducking + loudnorm -16 LUFS → out/<ID>.mp4
4. QC               → durasi, resolusi, loudness, true peak
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
REMOTION = ROOT / "remotion"
OUT = ROOT / "out"
PUBLIC = REMOTION / "public"


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def probe(ffmpeg, path):
    p = run([ffmpeg, "-hide_banner", "-i", str(path)])
    info = {}
    m = re.search(r"Duration: (\d+):(\d+):(\d+\.\d+)", p.stderr)
    if m:
        h, mnt, s = m.groups()
        info["duration"] = int(h) * 3600 + int(mnt) * 60 + float(s)
    m = re.search(r"Video: .*?, (\d+)x(\d+)", p.stderr)
    if m:
        info["width"], info["height"] = int(m.group(1)), int(m.group(2))
    m = re.search(r"(\d+(?:\.\d+)?) fps", p.stderr)
    if m:
        info["fps"] = float(m.group(1))
    return info


def loudness(ffmpeg, path):
    """Ukur loudness lewat loudnorm print_format=json (tanpa ffprobe)."""
    p = run([ffmpeg, "-hide_banner", "-nostats", "-i", str(path), "-af",
             "loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"])
    m = re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", p.stderr, re.S)
    if not m:
        return None
    try:
        d = json.loads(m.group(0))
        return float(d["input_i"]), float(d["input_tp"]), float(d["input_lra"])
    except Exception:
        return None


def mix(ffmpeg, silent, music, target, voice_offset=0.0):
    """VO + musik dengan ducking, lalu loudnorm ke -16 LUFS."""
    fc = (
        "[1:a]volume=0.30,highpass=f=45,lowpass=f=9000,"
        "afade=t=in:st=0:d=1.2[mus];"
        "[mus][0:a]sidechaincompress=threshold=0.05:ratio=8:attack=20:release=380[duck];"
        "[0:a][duck]amix=inputs=2:duration=first:normalize=0,"
        "loudnorm=I=-16:TP=-1.5:LRA=11[a]"
    )
    cmd = [ffmpeg, "-y", "-hide_banner", "-loglevel", "error",
           "-i", str(silent), "-i", str(music),
           "-filter_complex", fc, "-map", "0:v", "-map", "[a]",
           "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
           "-shortest", "-movflags", "+faststart", str(target)]
    p = run(cmd)
    if p.returncode != 0:
        print("  mix gagal:", p.stderr[-400:])
        return False
    return True


def build(shot_id, ffmpeg, browser, dry=False, skip_render=False):
    shot = json.loads((ROOT / "shots" / f"{shot_id}.json").read_text(encoding="utf-8"))
    plate = shot["plate"]

    print(f"\n=== {shot_id} — {shot['title'][:60]}")
    p = run([sys.executable, str(ROOT / "build_timing.py"), shot_id,
             "--ffmpeg", ffmpeg, "--strict"])
    print("  " + (p.stdout.strip() or p.stderr.strip())[-300:])
    if p.returncode != 0:
        return False
    if dry:
        return True

    OUT.mkdir(exist_ok=True)
    silent = OUT / f"{shot_id}-silent.mp4"
    final = OUT / f"{shot_id}.mp4"

    if not skip_render:
        cmd = ["npx", "remotion", "render", "src/index.ts", f"KT-{shot_id}",
               str(silent), f"--browser-executable={browser}",
               "--concurrency=2", "--crf=20", "--log=error"]
        r = run(cmd, cwd=str(REMOTION), env={**__import__("os").environ,
                                             "LD_LIBRARY_PATH": "/tmp/al2023/lib"})
        if r.returncode != 0:
            print("  render gagal:", (r.stderr or r.stdout)[-600:])
            return False
        print(f"  render → {silent.name}")

    music = PUBLIC / "music" / f"{plate}.mp3"
    if not mix(ffmpeg, silent, music, final):
        return False

    info = probe(ffmpeg, final)
    lr = loudness(ffmpeg, final)
    ok = True
    notes = []
    if info.get("duration", 0) < 40:
        notes.append(f"durasi {info.get('duration'):.1f} dtk terlalu pendek")
        ok = False
    if (info.get("width"), info.get("height")) != (1080, 1920):
        notes.append(f"resolusi {info.get('width')}x{info.get('height')}")
        ok = False
    if lr:
        if abs(lr[0] + 16) > 1.5:
            notes.append(f"loudness {lr[0]:.1f} LUFS (target -16 ±1,5)")
            ok = False
        if lr[1] > -1.5:
            notes.append(f"true peak {lr[1]:.1f} dBTP (maks -1,5)")
            ok = False
    print(f"  {'✓' if ok else '✗'} {final.name} · "
          f"{info.get('duration', 0):.1f} dtk · "
          f"{info.get('width')}x{info.get('height')} · "
          + (f"{lr[0]:.1f} LUFS / TP {lr[1]:.1f}" if lr else "loudness ?"))
    for n in notes:
        print("    · " + n)
    return ok


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("ids", nargs="*")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--dry", action="store_true")
    ap.add_argument("--skip-render", action="store_true")
    ap.add_argument("--ffmpeg", default="ffmpeg")
    ap.add_argument("--browser", default="/tmp/chromium")
    a = ap.parse_args()

    ids = a.ids or ([p.stem for p in sorted((ROOT / "shots").glob("*.json"))]
                    if a.all else [])
    if not ids:
        print("sebutkan id atau --all")
        sys.exit(1)
    results = {i: build(i, a.ffmpeg, a.browser, a.dry, a.skip_render) for i in ids}
    print("\nringkas:", ", ".join(f"{k}={'ok' if v else 'gagal'}" for k, v in results.items()))
    sys.exit(0 if all(results.values()) else 1)
