#!/usr/bin/env python3
"""Bed audio AK-EP03 (Dyatlov Pass): angin dingin, derak salju, drone rendah.

Tanpa musik dramatis. Bed diheningkan di dua titik: setelah "tak ada seorang pun"
(41,3–45,7) dan sepanjang adegan minum di tenda (59,6–75,0) — ironi dibiarkan
bekerja sendiri. Dipanggil oleh build_short_case.py lewat CFG.BED_BUILDER.
"""
import wave
from pathlib import Path

import numpy as np

SR = 48000
END = 101.60
OUT = Path(__file__).resolve().parent / "audio" / "bed.wav"


def main():
    n = int(END * SR)
    t = np.arange(n) / SR
    rng = np.random.default_rng(41)

    # angin: noise low-pass dua lapis + modulasi lambat
    noise = rng.standard_normal(n)
    k1 = np.ones(int(0.010 * SR)) / int(0.010 * SR)     # ~100 Hz low-pass
    wind = np.convolve(noise, k1, mode="same")
    k2 = np.ones(int(0.045 * SR)) / int(0.045 * SR)     # gust bodi
    gust = np.convolve(rng.standard_normal(n), k2, mode="same")
    wind = 0.75 * wind + 1.35 * gust
    wind *= 0.55 + 0.45 * np.sin(2 * np.pi * 0.043 * t + 0.7) * np.sin(2 * np.pi * 0.011 * t)
    wind = np.tanh(1.6 * wind)

    # drone: 43 Hz + 64,5 Hz, sangat rendah
    drone = (0.50 * np.sin(2 * np.pi * 43 * t)
             + 0.26 * np.sin(2 * np.pi * 64.5 * t + 1.1)
             + 0.14 * np.sin(2 * np.pi * 86 * t + 2.2))
    drone *= 0.65 + 0.35 * np.sin(2 * np.pi * 0.06 * t)

    # derak salju: butiran impuls jarang, pendek, ter-mask angin
    creak = np.zeros(n)
    for _ in range(int(END * 2.4)):
        at = rng.uniform(0, END - 0.2)
        i0 = int(at * SR)
        ln = int(rng.uniform(0.02, 0.09) * SR)
        env = np.exp(-np.linspace(0, 6, ln))
        creak[i0:i0 + ln] += rng.uniform(0.25, 0.8) * env * rng.standard_normal(ln)

    bed = 1.00 * wind + 0.85 * drone + 0.55 * creak

    def hit(at, freq=48.0, amp=0.9, dur=1.9):
        i0 = int(at * SR)
        ln = min(int(dur * SR), n - i0)
        if ln <= 0:
            return
        tt = np.arange(ln) / SR
        env = np.exp(-tt * 2.8)
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
        bed[i0:i1] += amp * hp * (tt ** 2.4)

    hit(0.10, freq=44, amp=0.8)
    riser(29.6, 32.15, amp=0.55)
    hit(32.20, freq=41, amp=1.0, dur=2.4)
    hit(41.30, freq=38, amp=0.55, dur=2.6)
    hit(75.05, freq=46, amp=0.8)
    riser(93.2, 96.85, amp=0.42)
    hit(96.90, freq=40, amp=0.85, dur=2.6)

    # hening terarah: turunkan bed (bukan mati total — angin tetap ada)
    def dip(a, b, depth, edge=0.6):
        i0, i1 = int(a * SR), int(b * SR)
        g = np.ones(i1 - i0)
        m = int(edge * SR)
        g[:m] = np.linspace(1, depth, m)
        g[-m:] = np.linspace(depth, 1, m)
        bed[i0:i1] *= g

    dip(41.35, 45.70, 0.34)
    dip(59.60, 68.20, 0.46)
    dip(68.25, 75.00, 0.30)

    fi = int(1.1 * SR)
    bed[:fi] *= np.linspace(0, 1, fi)
    fo = int(3.2 * SR)
    bed[-fo:] *= np.linspace(1, 0, fo)
    bed = bed / (np.max(np.abs(bed)) + 1e-9) * 0.62
    stereo = np.stack([bed, np.roll(bed, int(0.009 * SR))], axis=1)
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
