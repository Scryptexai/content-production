#!/usr/bin/env python3
"""make_sfx.py — desain bunyi prosedural untuk video Knot Theory.

Riset bunyi (lihat docs/FACELESS-QUALITY.md §2.5) menyimpulkan tiga hal:
  * whoosh hanya di titik gerakan, bukan di setiap potongan
  * ambience memberi tempat dan kontinuitas
  * efek harus cukup pelan supaya terasa subliminal

Semua disintesis dari noise + osilator, jadi bebas lisensi dan kecil.
Output: satu file WAV stereo 48 kHz.

    python3 make_sfx.py --out remotion/public/sfx/climb.wav --dur 15
    python3 make_sfx.py --preset climb --dur 15 --out ...
"""
from __future__ import annotations

import argparse
import math
import wave
from pathlib import Path

import numpy as np

SR = 48000


def env_ad(n, attack, decay, curve=3.0):
    """Amplop attack-decay (detik)."""
    a = max(1, int(attack * SR))
    d = max(1, int(decay * SR))
    e = np.zeros(n, np.float32)
    e[:a] = np.linspace(0, 1, a) ** 0.6
    d = min(d, n - a)
    e[a:a + d] = (1 - np.linspace(0, 1, d)) ** curve
    return e


def bandpass(x, lo, hi, order=2):
    """Band-pass kasar lewat FFT: cukup untuk noise tekstur."""
    n = len(x)
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(n, 1 / SR)
    m = ((f >= lo) & (f <= hi)).astype(np.float32)
    # tepi lembut
    for i in range(len(f)):
        if lo * 0.7 <= f[i] < lo:
            m[i] *= (f[i] - lo * 0.7) / (lo * 0.3)
        elif hi < f[i] <= hi * 1.35:
            m[i] *= (hi * 1.35 - f[i]) / (hi * 0.35)
    return np.fft.irfft(X * m, n).astype(np.float32)


def whoosh(dur, lo=180, hi=2600, rise=True):
    n = int(dur * SR)
    rng = np.random.default_rng(3)
    x = rng.normal(0, 1, n).astype(np.float32)
    # sapuan filter: waktu → frekuensi
    out = np.zeros(n, np.float32)
    seg = 16
    for k in range(seg):
        i0, i1 = k * n // seg, (k + 1) * n // seg
        q = k / (seg - 1)
        c = lo + (hi - lo) * (q if rise else 1 - q)
        out[i0:i1] = bandpass(x[i0:i1], c * 0.55, c * 1.5)
    e = np.sin(np.linspace(0, math.pi, n)) ** 1.6
    return out * e


def thud(dur=0.34, f0=68, f1=42):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = f0 + (f1 - f0) * (t / dur)
    ph = 2 * math.pi * np.cumsum(f) / SR
    body = np.sin(ph) * env_ad(n, 0.004, dur, 2.6)
    rng = np.random.default_rng(7)
    click = bandpass(rng.normal(0, 1, n).astype(np.float32), 900, 4200)
    click *= env_ad(n, 0.001, 0.045, 3.0)
    return body * 0.9 + click * 0.22


def wind(dur, lo=90, hi=900):
    n = int(dur * SR)
    rng = np.random.default_rng(11)
    x = bandpass(rng.normal(0, 1, n).astype(np.float32), lo, hi, 3)
    # napas lambat
    t = np.arange(n) / SR
    mod = 0.55 + 0.45 * np.sin(2 * math.pi * 0.06 * t + 0.7) ** 2
    mod *= 0.7 + 0.3 * np.sin(2 * math.pi * 0.017 * t)
    return x * mod


def pad(dur, base=110.0, partials=(1, 1.5, 2, 3, 4.5)):
    """Drone hangat untuk momen puncak."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    out = np.zeros(n, np.float32)
    for k, p in enumerate(partials):
        amp = 1.0 / (1 + k * 0.9)
        detune = 1 + 0.0015 * (k % 2 * 2 - 1)
        out += amp * np.sin(2 * math.pi * base * p * detune * t)
    return out / (1 + len(partials) * 0.4)


def shimmer(dur=2.6, base=880.0):
    n = int(dur * SR)
    t = np.arange(n) / SR
    out = np.zeros(n, np.float32)
    for k, m in enumerate((1, 1.5, 2.0, 3.0)):
        out += (0.7 / (1 + k)) * np.sin(2 * np.pi * base * m * t
                                        + np.sin(2 * np.pi * 5.2 * t) * 0.4)
    return out * np.sin(np.linspace(0, math.pi, n)) ** 2.0


def place(track, sig, at, gain=1.0):
    i = max(0, int(at * SR))
    n = min(len(sig), len(track) - i)
    if n <= 0:
        return
    track[i:i + n] += sig[:n] * gain


def reverb(x, mix=0.32, decay=1.9):
    """Reverb sederhana: denah Schroeder mini (4 comb + 2 allpass)."""
    out = np.zeros_like(x)
    for delay, g in ((0.0297, 0.78), (0.0371, 0.74), (0.0411, 0.71), (0.0437, 0.68)):
        d = int(delay * SR * decay)
        buf = np.zeros_like(x)
        for i in range(d, len(x)):
            buf[i] = x[i] + g * buf[i - d]
        out += buf * 0.25
    return x * (1 - mix) + out * mix


def build_climb(dur):
    n = int(dur * SR)
    L = np.zeros(n, np.float32)
    R = np.zeros(n, np.float32)

    # --- ambience: angin lembut sepanjang video, menguat di ketinggian
    w = wind(dur)
    for k in range(2):
        L += w * 0.115 * (1 + 0.05 * k)
        R += np.roll(w, 900 + k * 300) * 0.115
    # dengung rendah: ruang
    t = np.arange(n) / SR
    drone = 0.035 * np.sin(2 * math.pi * 55 * t) + 0.022 * np.sin(2 * math.pi * 82.5 * t)
    L += drone
    R += np.roll(drone, 480)

    # --- langkah: 6 anak tangga, tiap hentakan tanjakan → thud + kerikil
    step_sec = 1.30
    t0 = 1.10
    for k in range(6):
        at = t0 + k * step_sec + 0.80 * step_sec   # saat menapak
        th = thud()
        place(L, th, at, 0.34)
        place(R, th, at + 0.004, 0.34)
        # kerikil
        rng = np.random.default_rng(100 + k)
        grit = bandpass(rng.normal(0, 1, int(0.18 * SR)).astype(np.float32), 1800, 7000)
        grit *= env_ad(len(grit), 0.002, 0.16, 2.2)
        place(L, grit, at + 0.02, 0.10)
        place(R, grit, at + 0.03, 0.07)

    # --- whoosh: hanya di dua titik gerak kamera, bukan di setiap cut
    place(L, whoosh(1.9, 140, 1900), 0.05, 0.15)
    place(R, whoosh(1.9, 140, 1900), 0.09, 0.15)

    # --- puncak: badan berhenti, lengan terangkat → hirup + pad naik
    peak = t0 + 6 * step_sec + 1.6
    place(L, shimmer(3.4, 660), peak, 0.10)
    place(R, shimmer(3.4, 990), peak + 0.06, 0.09)
    pd = pad(6.5, 110.0)
    e = np.ones(len(pd), np.float32)
    a = int(2.2 * SR)
    e[:a] = np.linspace(0, 1, a) ** 1.8
    place(L, pd * e, peak - 0.4, 0.16)
    place(R, pd * e, peak - 0.36, 0.16)

    # --- napas: satu, di puncak
    rng = np.random.default_rng(55)
    br = bandpass(rng.normal(0, 1, int(0.9 * SR)).astype(np.float32), 320, 1900)
    br *= env_ad(len(br), 0.22, 0.6, 2.0)
    place(L, br, peak + 0.25, 0.07)
    place(R, br, peak + 0.27, 0.07)

    L = reverb(L, 0.30)
    R = reverb(R, 0.30)

    # master: normalisasi + loop-safe fade
    st = np.stack([L, R], axis=1)
    fade = int(0.5 * SR)
    st[:fade] *= np.linspace(0, 1, fade)[:, None]
    st[-fade:] *= np.linspace(1, 0, fade)[:, None]
    peakv = np.abs(st).max()
    if peakv > 0:
        st = st / peakv * 0.78
    return st


PRESETS = {"climb": build_climb}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--preset", default="climb")
    ap.add_argument("--dur", type=float, default=15.0)
    ap.add_argument("--out", default="remotion/public/sfx/climb.wav")
    a = ap.parse_args()
    st = PRESETS[a.preset](a.dur)
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
    with wave.open(str(out), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    print("sfx →", out, f"{out.stat().st_size/1e6:.2f} MB")


if __name__ == "__main__":
    main()
