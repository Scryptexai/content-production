#!/usr/bin/env python3
"""Bed audio AK-EP04 (Van der Wijck 1936): laut malam, angin, drone rendah, derak kayu.

Tanpa musik dramatis. Bed diturunkan saat "tidak ada kapal besar" (39,8–44,6) supaya
kesunyian itu terasa, dan dinaikkan lagi saat perahu nelayan masuk. Dipanggil oleh
build_short_case.py lewat CFG.BED_BUILDER.
"""
import wave
from pathlib import Path

import numpy as np

SR = 48000
END = 95.70
OUT = Path(__file__).resolve().parent / "audio" / "bed.wav"


def main():
    n = int(END * SR)
    t = np.arange(n) / SR
    rng = np.random.default_rng(1936)

    # laut: noise low-pass panjang (gulungan air) + lapisan gust (angin di dek)
    noise = rng.standard_normal(n)
    k1 = np.ones(int(0.018 * SR)) / int(0.018 * SR)      # ~55 Hz
    sea = np.convolve(noise, k1, mode="same")
    k2 = np.ones(int(0.060 * SR)) / int(0.060 * SR)      # bodi ombak
    swell = np.convolve(rng.standard_normal(n), k2, mode="same")
    sea = 1.10 * sea + 1.45 * swell
    sea *= 0.50 + 0.50 * np.sin(2 * np.pi * 0.055 * t + 0.4) * np.sin(2 * np.pi * 0.013 * t + 2.1)
    sea = np.tanh(1.5 * sea)

    # drone: 46 Hz + 69 Hz + 92 Hz, sangat rendah
    drone = (0.52 * np.sin(2 * np.pi * 46 * t)
             + 0.24 * np.sin(2 * np.pi * 69 * t + 1.2)
             + 0.12 * np.sin(2 * np.pi * 92 * t + 2.4))
    drone *= 0.62 + 0.38 * np.sin(2 * np.pi * 0.045 * t)

    # derak kayu perahu: impuls jarang, pendek, disaring
    creak = np.zeros(n)
    for _ in range(int(END * 1.8)):
        at = rng.uniform(0, END - 0.2)
        i0 = int(at * SR)
        ln = int(rng.uniform(0.05, 0.16) * SR)
        env = np.exp(-np.linspace(0, 7, ln))
        tone = np.sin(2 * np.pi * rng.uniform(75, 140) * np.arange(ln) / SR)
        creak[i0:i0 + ln] += rng.uniform(0.25, 0.7) * env * (0.7 * tone + 0.3 * rng.standard_normal(ln))

    bed = 1.00 * sea + 0.80 * drone + 0.40 * creak

    def hit(at, freq=48.0, amp=0.9, dur=1.9):
        i0 = int(at * SR)
        ln = min(int(dur * SR), n - i0)
        if ln <= 0:
            return
        tt = np.arange(ln) / SR
        env = np.exp(-tt * 2.7)
        bed[i0:i0 + ln] += amp * env * (0.85 * np.sin(2 * np.pi * freq * tt)
                                        + 0.45 * rng.standard_normal(ln) * np.exp(-tt * 9))

    def riser(t0, t1, amp=0.5):
        i0, i1 = int(t0 * SR), int(t1 * SR)
        ln = i1 - i0
        if ln <= 0:
            return
        tt = np.linspace(0, 1, ln)
        nz = rng.standard_normal(ln)
        hp = np.diff(nz, prepend=nz[0])
        bed[i0:i1] += amp * hp * (tt ** 2.3)

    hit(0.10, freq=44, amp=0.75)
    riser(28.4, 32.30, amp=0.50)
    hit(32.30, freq=40, amp=1.05, dur=2.5)      # "6 menit"
    hit(44.70, freq=52, amp=0.55, dur=1.6)      # perahu masuk
    hit(56.85, freq=46, amp=0.6)
    hit(71.95, freq=42, amp=0.8, dur=2.2)       # angka korban
    riser(78.0, 81.35, amp=0.40)
    hit(81.35, freq=38, amp=0.70, dur=2.4)      # bangkai 2021

    def dip(a, b, depth, edge=0.7):
        i0, i1 = int(a * SR), int(b * SR)
        g = np.ones(i1 - i0)
        m = int(edge * SR)
        g[:m] = np.linspace(1, depth, m)
        g[-m:] = np.linspace(depth, 1, m)
        bed[i0:i1] *= g

    dip(39.90, 44.60, 0.30)                     # "tidak ada kapal besar"
    dip(93.20, 95.60, 0.22)                     # kartu penutup

    fi = int(1.2 * SR)
    bed[:fi] *= np.linspace(0, 1, fi)
    fo = int(2.4 * SR)
    bed[-fo:] *= np.linspace(1, 0, fo)
    bed = bed / (np.max(np.abs(bed)) + 1e-9) * 0.33
    stereo = np.stack([bed, np.roll(bed, int(0.010 * SR))], axis=1)
    pcm = (np.clip(stereo, -1, 1) * 32767).astype("<i2")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(OUT), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    print("bed.wav ok", OUT.stat().st_size)


if __name__ == "__main__":
    main()
