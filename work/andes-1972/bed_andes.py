#!/usr/bin/env python3
"""Bed audio AK-EP05 (Andes 1972): angin dingin, drone rendah, detak jarum.

Tanpa musik dramatis — sama seperti EP04. Hit dipasang di awal beat format
Curiosity Loop (B3 radio, B4 pertaruhan, B5 tekanan, B6 pakta, B7 payoff,
B8 debat), riser menuju B5, dip saat kartu penutup. Dipanggil oleh
build_short_case.py lewat CFG.BED_BUILDER.
"""
import wave
from pathlib import Path

import numpy as np

SR = 48000
END = 91.40
OUT = Path(__file__).resolve().parent / "audio" / "bed.wav"


def main():
    n = int(END * SR)
    t = np.arange(n) / SR
    rng = np.random.default_rng(1972)

    # angin pegunungan: noise low-pass panjang + gust lambat
    noise = rng.standard_normal(n)
    k1 = np.ones(int(0.020 * SR)) / int(0.020 * SR)
    wind = np.convolve(noise, k1, mode="same")
    k2 = np.ones(int(0.070 * SR)) / int(0.070 * SR)
    gust = np.convolve(rng.standard_normal(n), k2, mode="same")
    wind = 1.15 * wind + 1.30 * gust
    wind *= 0.45 + 0.55 * np.sin(2 * np.pi * 0.043 * t + 0.8) * np.sin(2 * np.pi * 0.011 * t + 2.0)
    wind = np.tanh(1.3 * wind)

    # drone: 46 + 69 + 92 Hz, sangat rendah
    drone = (0.52 * np.sin(2 * np.pi * 46 * t)
             + 0.24 * np.sin(2 * np.pi * 69 * t + 1.2)
             + 0.12 * np.sin(2 * np.pi * 92 * t + 2.4))
    drone *= 0.62 + 0.38 * np.sin(2 * np.pi * 0.045 * t)

    # detak jarum jarang (teknan waktu)
    tick = np.zeros(n)
    k = 0
    while k * 1.35 < END:
        idx = int(k * 1.35 * SR); ln = int(0.045 * SR)
        if idx + ln < n:
            tick[idx:idx + ln] += 0.42 * np.exp(-np.linspace(0, 13, ln)) * rng.standard_normal(ln)
        k += 1

    bed = 1.00 * wind + 0.85 * drone + 0.50 * tick

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

    hit(0.10, freq=44, amp=0.75)                  # pembuka dilema
    hit(10.75, freq=46, amp=0.70)                 # B3 radio: SAR dihentikan
    hit(15.72, freq=44, amp=0.65)                 # B4 pertaruhan nyawa
    riser(21.50, 25.38, amp=0.45)                 # menuju B5
    hit(25.38, freq=42, amp=0.90, dur=2.2)        # B5 tekanan situasi
    hit(51.30, freq=38, amp=0.95, dur=2.6)        # B6 pakta di tengah es
    hit(64.71, freq=46, amp=0.75)                 # B7 payoff
    hit(74.68, freq=40, amp=0.90, dur=2.4)        # B8 debat komentar

    dip(87.31, 91.40, 0.25, edge=0.5)           # kartu penutup

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
