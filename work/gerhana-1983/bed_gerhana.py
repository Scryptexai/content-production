#!/usr/bin/env python3
"""Bed audio AK-EP09 (Gerhana 1983): hening siang jadi malam, drone rendah, detak.

Tanpa musik dramatis — pola EP04–EP08. Hit di awal beat Curiosity Loop (B3
rakyat patuh, B4 aparat, B6 ayah Semarang, B7 fakta LIPI, B8 debat), riser
menuju B7, dip kartu penutup. Dipanggil build_short_case.py via CFG.BED_BUILDER.
"""
import wave
from pathlib import Path

import numpy as np

SR = 48000
END = 93.20
OUT = Path(__file__).resolve().parent / "audio" / "bed.wav"


def main():
    n = int(END * SR)
    t = np.arange(n) / SR
    rng = np.random.default_rng(1983)

    # angin siang yang mengecil jadi senyap: noise + dua lapis lambat
    noise = rng.standard_normal(n)
    k1 = np.ones(int(0.024 * SR)) / int(0.024 * SR)
    air = np.convolve(noise, k1, mode="same")
    k2 = np.ones(int(0.100 * SR)) / int(0.100 * SR)
    drift = np.convolve(rng.standard_normal(n), k2, mode="same")
    air = 1.05 * air + 1.20 * drift
    air *= (0.45 + 0.55 * np.sin(2 * np.pi * 0.036 * t + 0.7)
            * np.sin(2 * np.pi * 0.011 * t + 2.4))
    air = np.tanh(1.2 * air)

    # drone rendah
    drone = (0.50 * np.sin(2 * np.pi * 45 * t)
             + 0.22 * np.sin(2 * np.pi * 67.5 * t + 1.1)
             + 0.11 * np.sin(2 * np.pi * 90 * t + 2.2))
    drone *= 0.60 + 0.40 * np.sin(2 * np.pi * 0.038 * t)

    # detak (jarum waktu siang yang berhenti)
    tick = np.zeros(n)
    k = 0
    while k * 1.50 < END:
        idx = int(k * 1.50 * SR); ln = int(0.045 * SR)
        if idx + ln < n:
            tick[idx:idx + ln] += 0.36 * np.exp(-np.linspace(0, 13, ln)) * rng.standard_normal(ln)
        k += 1

    bed = 1.00 * air + 0.82 * drone + 0.44 * tick

    def hit(at, freq=47.0, amp=0.9, dur=1.9):
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
        nz = rng.standard_normal(n)
        hp = np.diff(nz, prepend=nz[0])
        bed[i0:i1] += amp * hp[i0:i1] * (tt ** 2.3)

    def dip(a, b, depth, edge=0.7):
        i0, i1 = int(a * SR), int(b * SR)
        g = np.ones(i1 - i0)
        m = int(edge * SR)
        g[:m] = np.linspace(1, depth, m)
        g[-m:] = np.linspace(depth, 1, m)
        bed[i0:i1] *= g

    hit(0.10, freq=44, amp=0.75)                  # pembuka — tengah hari jadi malam
    hit(24.34, freq=46, amp=0.70)                 # B3 rakyat patuh
    hit(39.48, freq=44, amp=0.80, dur=2.0)        # B4 aparat
    hit(58.90, freq=42, amp=0.74)                 # B6 ayah Semarang
    riser(74.00, 79.68, amp=0.45)                 # menuju kritik LIPI
    hit(79.68, freq=40, amp=0.90, dur=2.3)        # B8 debat (sekaligus puncak)
    hit(67.06, freq=45, amp=0.70)                 # B7 fakta Yogyakarta

    dip(88.64, 93.20, 0.25, edge=0.5)             # kartu penutup

    fi = int(1.2 * SR)
    bed[:fi] *= np.linspace(0, 1, fi)
    fo = int(2.4 * SR)
    bed[-fo:] *= np.linspace(1, 0, fo)
    bed = bed / (np.max(np.abs(bed)) + 1e-9) * 0.40
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
