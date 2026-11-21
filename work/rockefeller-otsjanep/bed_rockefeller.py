#!/usr/bin/env python3
"""Bed audio AK-EP07 (Rockefeller/Otsjanep): deru laut jauh, drone rendah, detak.

Tanpa musik dramatis — pola EP04–EP06. Hit di awal beat Curiosity Loop (B3
pencarian, B4 pengakuan "dibunuh", B6 laporan, B7 fakta1964, B8 debat), riser
menuju fakta, dip saat kartu penutup. Dipanggil build_short_case.py via
CFG.BED_BUILDER.
"""
import wave
from pathlib import Path

import numpy as np

SR = 48000
END = 107.80
OUT = Path(__file__).resolve().parent / "audio" / "bed.wav"


def main():
    n = int(END * SR)
    t = np.arange(n) / SR
    rng = np.random.default_rng(1961)

    # deru laut jauh: noise low-pass + dua lapis gelombang lambat
    noise = rng.standard_normal(n)
    k1 = np.ones(int(0.022 * SR)) / int(0.022 * SR)
    surf = np.convolve(noise, k1, mode="same")
    k2 = np.ones(int(0.090 * SR)) / int(0.090 * SR)
    swell = np.convolve(rng.standard_normal(n), k2, mode="same")
    surf = 1.10 * surf + 1.35 * swell
    surf *= (0.45 + 0.55 * np.sin(2 * np.pi * 0.048 * t + 0.6)
             * np.sin(2 * np.pi * 0.013 * t + 2.1))
    surf = np.tanh(1.25 * surf)

    # drone rendah
    drone = (0.50 * np.sin(2 * np.pi * 41 * t)
             + 0.23 * np.sin(2 * np.pi * 61.5 * t + 1.1)
             + 0.11 * np.sin(2 * np.pi * 82 * t + 2.2))
    drone *= 0.60 + 0.40 * np.sin(2 * np.pi * 0.040 * t)

    # detak jarang (jarum waktu)
    tick = np.zeros(n)
    k = 0
    while k * 1.55 < END:
        idx = int(k * 1.55 * SR); ln = int(0.045 * SR)
        if idx + ln < n:
            tick[idx:idx + ln] += 0.38 * np.exp(-np.linspace(0, 13, ln)) * rng.standard_normal(ln)
        k += 1

    bed = 1.00 * surf + 0.82 * drone + 0.46 * tick

    def hit(at, freq=46.0, amp=0.9, dur=1.9):
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

    hit(0.10, freq=42, amp=0.75)                  # pembuka — tiga titik
    hit(24.78, freq=46, amp=0.72)                 # B3 pencarian besar
    hit(43.26, freq=40, amp=0.92, dur=2.2)        # B4 pengakuan: ia dibunuh
    hit(68.62, freq=44, amp=0.70)                 # B6 laporan dikubur
    riser(79.00, 83.06, amp=0.45)                 # menuju fakta1964
    hit(83.06, freq=40, amp=0.90, dur=2.3)        # B7 tanpa bukti
    hit(96.10, freq=46, amp=0.72)                 # B8 debat

    dip(103.26, 107.80, 0.25, edge=0.5)           # kartu penutup

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
