#!/usr/bin/env python3
"""Bed audio AK-EP08 (Ponari/antrean): deru kerumunan jauh, drone rendah, detak.

Tanpa musik dramatis — pola EP04–EP07. Hit di awal beat Curiosity Loop (B3
penuh sesak, B4 korban, B6 Kenapa?, B7 korban kelima, B8 debat), riser menuju
B7, dip kartu penutup. Dipanggil build_short_case.py via CFG.BED_BUILDER.
"""
import wave
from pathlib import Path

import numpy as np

SR = 48000
END = 82.90
OUT = Path(__file__).resolve().parent / "audio" / "bed.wav"


def main():
    n = int(END * SR)
    t = np.arange(n) / SR
    rng = np.random.default_rng(2009)

    # deru kerumunan jauh: noise band-rendah + denyut lambat
    noise = rng.standard_normal(n)
    k1 = np.ones(int(0.030 * SR)) / int(0.030 * SR)
    crowd = np.convolve(noise, k1, mode="same")
    k2 = np.ones(int(0.120 * SR)) / int(0.120 * SR)
    murmur = np.convolve(rng.standard_normal(n), k2, mode="same")
    crowd = 1.05 * crowd + 1.25 * murmur
    crowd *= (0.42 + 0.58 * np.sin(2 * np.pi * 0.052 * t + 0.9)
              * np.sin(2 * np.pi * 0.016 * t + 1.7))
    crowd = np.tanh(1.25 * crowd)

    # drone rendah
    drone = (0.50 * np.sin(2 * np.pi * 43 * t)
             + 0.22 * np.sin(2 * np.pi * 64.5 * t + 1.0)
             + 0.11 * np.sin(2 * np.pi * 86 * t + 2.1))
    drone *= 0.60 + 0.40 * np.sin(2 * np.pi * 0.042 * t)

    # detak antrean
    tick = np.zeros(n)
    k = 0
    while k * 1.45 < END:
        idx = int(k * 1.45 * SR); ln = int(0.045 * SR)
        if idx + ln < n:
            tick[idx:idx + ln] += 0.40 * np.exp(-np.linspace(0, 13, ln)) * rng.standard_normal(ln)
        k += 1

    bed = 1.00 * crowd + 0.82 * drone + 0.48 * tick

    def hit(at, freq=45.0, amp=0.9, dur=1.9):
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

    hit(0.10, freq=44, amp=0.75)                  # pembuka — puluhan ribu
    hit(21.54, freq=46, amp=0.70)                 # B3 penuh sesak
    hit(33.34, freq=40, amp=0.92, dur=2.2)        # B4 kerumunan menelan korban
    hit(52.64, freq=46, amp=0.70)                 # B6 Kenapa?
    riser(57.50, 61.86, amp=0.45)                 # menuju korban kelima
    hit(61.86, freq=40, amp=0.90, dur=2.3)        # B7 korban kelima
    hit(69.14, freq=46, amp=0.72)                 # B8 debat

    dip(78.40, 82.90, 0.25, edge=0.5)             # kartu penutup

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
