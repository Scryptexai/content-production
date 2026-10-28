#!/usr/bin/env python3
"""Musik latar Knot Theory: drone + pulse + tekstur, tanpa sampel eksternal.

Semua disintesis dari osilator dasar, jadi tidak ada masalah lisensi dan
ukurannya kecil. Satu lagu per akar nada, supaya tiap episode tidak terdengar
persis sama tanpa harus bikin 21 lagu.

    python3 make_music.py              # 4 varian, 90 dtk
    python3 make_music.py --sec 120
"""
import argparse
import subprocess
import wave
from pathlib import Path

import numpy as np

ROOT = Path(__file__).parent
OUT = ROOT / "remotion" / "public" / "music"
OUT.mkdir(parents=True, exist_ok=True)

SR = 48000

# akar nada (Hz) + warna. Sengaja rendah & dekat satu sama lain: ruang tenang.
VARIANTS = {
    "ink":   (55.00, "A1", (0.0, 7.0, 12.0, 19.0)),
    "rose":  (61.74, "B1", (0.0, 5.0, 10.0, 17.0)),
    "sage":  (49.00, "G1", (0.0, 7.0, 14.0, 21.0)),
    "lilac": (58.27, "A#1", (0.0, 6.0, 11.0, 18.0)),
}


def synth(root, intervals, seconds):
    n = int(SR * seconds)
    t = np.arange(n, dtype=np.float32) / SR
    out = np.zeros(n, dtype=np.float32)

    # 1. drone: tiga oktaf, sedikit detune supaya "hidup"
    for mult, amp in ((1, 0.42), (2, 0.17), (3, 0.07)):
        f = root * mult
        for det in (-0.14, 0.0, 0.14):
            out += amp * np.sin(2 * np.pi * (f + det) * t + det)
    # 2. pad: nada atas yang sangat pelan masuk-keluar
    for i, semi in enumerate(intervals):
        f = root * (2 ** (semi / 12))
        lfo = 0.5 + 0.5 * np.sin(2 * np.pi * (0.017 + 0.004 * i) * t + i)
        out += 0.055 * lfo * np.sin(2 * np.pi * f * t)

    # 3. pulse: satu ketukan tiap 2,4 dtk, sangat lembut
    period = 2.4
    for start in np.arange(0, seconds, period):
        i0 = int(start * SR)
        ln = int(0.9 * SR)
        if i0 + ln > n:
            break
        env = np.exp(-np.linspace(0, 7, ln)).astype(np.float32)
        body = np.sin(2 * np.pi * root * 2 * np.linspace(0, 0.9, ln)).astype(np.float32)
        out[i0:i0 + ln] += 0.16 * env * body

    # 4. tekstur: noise sangat rendah, di-filter dengan rata-rata bergerak
    rng = np.random.default_rng(7)
    noise = rng.normal(0, 1, n).astype(np.float32)
    k = 900
    kernel = np.ones(k, dtype=np.float32) / k
    sm = np.convolve(noise, kernel, mode="same")
    out += 0.30 * sm / (np.abs(sm).max() + 1e-9) * 0.25

    # 5. fade masuk/keluar supaya bisa di-loop tanpa klik
    fade = int(2.0 * SR)
    out[:fade] *= np.linspace(0, 1, fade) ** 1.5
    out[-fade:] *= np.linspace(1, 0, fade) ** 1.5

    out = np.tanh(out * 1.1) * 0.5
    peak = np.abs(out).max()
    return (out / peak * 0.72).astype(np.float32)


def write_mp3(path_wav, ffmpeg):
    """WAV 48 kHz → MP3 192k (kecil, cukup untuk bed musik)."""
    mp3 = path_wav.with_suffix(".mp3")
    subprocess.run([ffmpeg, "-y", "-hide_banner", "-loglevel", "error",
                    "-i", str(path_wav), "-c:a", "libmp3lame", "-b:a", "192k",
                    str(mp3)], check=True)
    path_wav.unlink()
    print(f"  {mp3.name}  {mp3.stat().st_size/1024/1024:5.1f} MB")


def write_wav(path, mono):
    stereo = np.stack([mono, mono * 0.985], axis=1)
    pcm = (np.clip(stereo, -1, 1) * 32767).astype("<i2")
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    print(f"  {path.name}  {path.stat().st_size/1024/1024:5.1f} MB")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--sec", type=float, default=90)
    ap.add_argument("--variant", default="all")
    ap.add_argument("--ffmpeg", default="ffmpeg")
    args = ap.parse_args()
    names = list(VARIANTS) if args.variant == "all" else [args.variant]
    for nm in names:
        root, label, intervals = VARIANTS[nm]
        wav = OUT / f"{nm}.wav"
        write_wav(wav, synth(root, intervals, args.sec + 4))
        write_mp3(wav, args.ffmpeg)
    print("selesai ->", OUT)
