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
END = 110.90
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
    hit(10.12, freq=46, amp=0.60)               # tanggal
    riser(18.6, 21.48, amp=0.42)                # menuju SOS
    hit(21.48, freq=41, amp=0.95, dur=2.4)      # "menjelang pukul satu"
    riser(26.4, 29.60, amp=0.50)
    hit(29.60, freq=40, amp=1.05, dur=2.5)      # "menurut kesaksian pertama"
    hit(39.80, freq=48, amp=0.6)                # Dornier
    hit(47.70, freq=52, amp=0.7, dur=1.8)       # nelayan turun ke laut
    hit(62.62, freq=44, amp=0.85, dur=2.2)      # kapten
    hit(68.48, freq=42, amp=0.7)                # 50 orang hilang
    hit(78.30, freq=46, amp=0.6)                # sembilan perahu
    riser(86.0, 90.14, amp=0.44)
    hit(90.14, freq=38, amp=0.85, dur=2.4)      # pelat besi
    hit(96.76, freq=36, amp=0.80, dur=2.6)      # "hari ini …"  

    def dip(a, b, depth, edge=0.7):
        i0, i1 = int(a * SR), int(b * SR)
        g = np.ones(i1 - i0)
        m = int(edge * SR)
        g[:m] = np.linspace(1, depth, m)
        g[-m:] = np.linspace(depth, 1, m)
        bed[i0:i1] *= g

    dip(21.60, 25.10, 0.45)                     # SOS tanpa posisi
    dip(94.30, 96.60, 0.26)                     # pelat besi di dinding
    dip(108.30, 110.90, 0.22)                   # kartu penutup

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
