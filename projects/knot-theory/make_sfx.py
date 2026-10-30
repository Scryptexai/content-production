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


def build_reel(dur):
    """Bunyi untuk reel identitas 14 dtk dengan tiga beat.

    Aturannya: bunyi hanya di titik gerak yang nyata.
      * beat 1 (jalan)   : ambience angin tipis + sepatu di lantai, pelan
      * potongan 4.7 dtk : satu hentakan rendah, bukan whoosh
      * beat 2 (tangga)  : naik, ambience menebal sedikit
      * potongan 9.5 dtk : hentakan kedua, lebih pelan
      * 11.0 dtk         : nada simpul (dua sinus, kuint) — satu-satunya nada
      * ekor             : dengung rendah yang memudar
    """
    n = int(dur * SR)
    L = np.zeros(n, np.float32)
    R = np.zeros(n, np.float32)

    def place(buf, x, at, gain):
        i = int(at * SR)
        if i >= n:
            return
        m = min(len(x), n - i)
        buf[i:i + m] += x[:m] * gain

    # --- ambience: angin malam, sangat pelan
    rng = np.random.default_rng(1201)
    wind = bandpass(rng.normal(0, 1, n).astype(np.float32), 120, 900)
    swell = 0.5 + 0.5 * np.sin(np.linspace(0, 5.2, n))
    wind *= swell * 0.055
    L += wind
    R += np.roll(wind, 900) * 0.95

    # --- hentakan potongan: sinus 58 Hz turun cepat — bukan whoosh
    for at, g in ((4.70, 0.42), (9.50, 0.34)):
        m = int(0.55 * SR)
        tt = np.arange(m) / SR
        f = 58 * np.exp(-tt * 4.0) + 34
        boom = np.sin(2 * np.pi * np.cumsum(f) / SR).astype(np.float32)
        boom *= np.exp(-tt * 7.5)
        place(L, boom, at, g)
        place(R, boom, at, g)

    # --- sepatu di lantai: klik pendek tiap langkah (0.5 dtk)
    rng2 = np.random.default_rng(77)
    step = bandpass(rng2.normal(0, 1, int(0.09 * SR)).astype(np.float32), 240, 2400)
    step *= np.exp(-np.arange(len(step)) / SR * 55)
    t = 0.18
    while t < 4.6:
        g = 0.055 * (0.7 + 0.3 * math.sin(t * 2.1))
        place(L, step, t, g)
        place(R, step, t + 0.004, g * 0.9)
        t += 0.52

    # --- langkah di tangga: lebih berat, lebih rendah
    rng3 = np.random.default_rng(78)
    st2 = bandpass(rng3.normal(0, 1, int(0.14 * SR)).astype(np.float32), 150, 1500)
    st2 *= np.exp(-np.arange(len(st2)) / SR * 32)
    t = 5.15
    while t < 9.3:
        place(L, st2, t, 0.075)
        place(R, st2, t + 0.006, 0.068)
        t += 0.86

    # --- nada simpul: 392 + 587 Hz (kuint), masuk pelan, bergetar
    at = 11.05
    m = int(2.4 * SR)
    tt = np.arange(m) / SR
    tone = (np.sin(2 * np.pi * 392 * tt) * 0.5 + np.sin(2 * np.pi * 587.3 * tt) * 0.34
            + np.sin(2 * np.pi * 784 * tt) * 0.12)
    vib = 1 + 0.012 * np.sin(2 * np.pi * 5.1 * tt)
    tone = (tone * vib).astype(np.float32) * np.exp(-tt * 1.25)
    tone *= np.clip(tt / 0.08, 0, 1)
    place(L, tone, at, 0.16)
    place(R, tone, at + 0.012, 0.15)

    # --- dengung bawah dari tabrakan senar (mengisi ekor)
    m = int(3.2 * SR)
    tt = np.arange(m) / SR
    hum = np.sin(2 * np.pi * 98 * tt + 0.4 * np.sin(2 * np.pi * 0.7 * tt)).astype(np.float32)
    hum *= np.exp(-tt * 0.75) * 0.075
    place(L, hum, 11.1, 1.0)
    place(R, hum, 11.16, 1.0)

    L = reverb(L, 0.34)
    R = reverb(R, 0.34)

    st = np.stack([L, R], axis=1)
    fade = int(0.35 * SR)
    st[:fade] *= np.linspace(0, 1, fade)[:, None]
    st[-int(0.9 * SR):] *= np.linspace(1, 0, int(0.9 * SR))[:, None]
    pk = np.abs(st).max()
    if pk > 0:
        st = st / pk * 0.72
    return st


def build_promo(dur):
    """Bunyi untuk scene papan promosi 13 dtk.

    Tiga lapis, sesuai isi gambarnya:
      * ambience ruang besar (dengung rendah, bukan angin)
      * langkah kaki: 6 langkah saat masuk, lalu diam (dia berhenti mengikat)
      * nada naik: tiap kali simpul naik satu jenjang, satu nada — tangga
        pentatonik, jadi rasanya menanjak, bukan acak
      * satu nada tinggi kosong saat simpul berubah jadi cincin kosong
    """
    n = int(dur * SR)
    L = np.zeros(n, np.float32)
    R = np.zeros(n, np.float32)

    def place(buf, x, at, gain):
        i = int(at * SR)
        if i >= n:
            return
        m = min(len(x), n - i)
        buf[i:i + m] += x[:m] * gain

    # ambience: dengung ruang, dua sinus rendah yang saling bergeser
    tt = np.arange(n) / SR
    room = (0.5 * np.sin(2 * np.pi * 55 * tt + 0.6 * np.sin(2 * np.pi * 0.13 * tt))
            + 0.3 * np.sin(2 * np.pi * 82.5 * tt + 0.9 * np.sin(2 * np.pi * 0.09 * tt)))
    room = room.astype(np.float32) * 0.05
    L += room
    R += np.roll(room, 2400) * 0.9

    # langkah: 6 langkah dari 0.2 sampai 3.2 dtk
    rng = np.random.default_rng(311)
    step = bandpass(rng.normal(0, 1, int(0.11 * SR)).astype(np.float32), 200, 2200)
    step *= np.exp(-np.arange(len(step)) / SR * 46)
    for k in range(6):
        at = 0.22 + k * 0.52
        place(L, step, at, 0.06)
        place(R, step, at + 0.005, 0.055)

    # nada naik: pentatonik 5 jenjang, mulai saat simpul mulai naik
    PENT = [392.0, 440.0, 523.25, 587.33, 698.46]
    for k, f in enumerate(PENT):
        at = 6.30 + k * 1.06
        m = int(1.5 * SR)
        t2 = np.arange(m) / SR
        tone = (np.sin(2 * np.pi * f * t2) * 0.6
                + np.sin(2 * np.pi * f * 2 * t2) * 0.16
                + np.sin(2 * np.pi * f * 3 * t2) * 0.05).astype(np.float32)
        tone *= np.exp(-t2 * 2.0) * np.clip(t2 / 0.05, 0, 1)
        place(L, tone, at, 0.13)
        place(R, tone, at + 0.014, 0.12)

    # cincin kosong: nada tinggi tanpa dasar (hanya harmonik ganjil)
    at = 11.62
    m = int(1.7 * SR)
    t3 = np.arange(m) / SR
    hollow = (np.sin(2 * np.pi * 1174.7 * t3) * 0.4
              + np.sin(2 * np.pi * 1760 * t3) * 0.22
              + np.sin(2 * np.pi * 2349 * t3) * 0.1).astype(np.float32)
    hollow *= np.exp(-t3 * 1.5) * np.clip(t3 / 0.25, 0, 1)
    place(L, hollow, at, 0.085)
    place(R, hollow, at + 0.02, 0.08)

    L = reverb(L, 0.42)
    R = reverb(R, 0.42)

    st = np.stack([L, R], axis=1)
    fade = int(0.4 * SR)
    st[:fade] *= np.linspace(0, 1, fade)[:, None]
    st[-int(0.9 * SR):] *= np.linspace(1, 0, int(0.9 * SR))[:, None]
    pk = np.abs(st).max()
    if pk > 0:
        st = st / pk * 0.70
    return st


def build_ep01(dur):
    """Bunyi EP01 (60 dtk, vertikal). Sesuai riset: mikro-SFX hanya di titik
    gerak & perubahan informasi, ambience untuk tempat.

    Peta waktu:
      0.0–6.4   jalan      : angin pesisir + 12 langkah
      6.4–18    hitung     : titik menyala satu per satu (klik halus, 3 kali)
                             + satu nada rendah saat angka −3,2 muncul
      18–22.6   jalan lagi  : langkah, ambience sama (kontinuitas tempat)
      22.6–34   banding    : dua batang tumbuh → dua nada pendek, lalu hening
      34–38.6   jalan lagi  : langkah
      38.6–60   simpul     : gesekan tali saat diikat, denyut mengendor,
                             satu nada tinggi untuk "hampir nol", lalu ekor
                             ambience yang memudar.
    """
    n = int(dur * SR)
    L = np.zeros(n, np.float32)
    R = np.zeros(n, np.float32)

    def place(buf, x, at, gain):
        i = int(at * SR)
        if i >= n:
            return
        m = min(len(x), n - i)
        buf[i:i + m] += x[:m] * gain

    # --- ambience pesisir: angin + gum laut rendah
    tt = np.arange(n) / SR
    rng = np.random.default_rng(9001)
    wind = bandpass(rng.normal(0, 1, n).astype(np.float32), 90, 1100)
    wind *= (0.55 + 0.45 * np.sin(2 * np.pi * 0.06 * tt + 0.7)) * 0.06
    L += wind
    R += np.roll(wind, 1400) * 0.92
    sea = (np.sin(2 * np.pi * 41 * tt + 1.2 * np.sin(2 * np.pi * 0.11 * tt)) * 0.05).astype(np.float32)
    L += sea
    R += np.roll(sea, 900) * 0.8

    # --- langkah: tiga rangkaian jalan
    rng2 = np.random.default_rng(4211)
    step = bandpass(rng2.normal(0, 1, int(0.12 * SR)).astype(np.float32), 180, 2200)
    step *= np.exp(-np.arange(len(step)) / SR * 42)
    for t0, t1 in ((0.15, 6.3), (18.05, 22.5), (34.05, 38.5)):
        t = t0
        while t < t1:
            g = 0.062 * (0.75 + 0.25 * math.sin(t * 1.7))
            place(L, step, t, g)
            place(R, step, t + 0.006, g * 0.92)
            t += 0.52

    # --- klik titik: tiga klik saat hitungan naik
    rng3 = np.random.default_rng(88)
    tick = bandpass(rng3.normal(0, 1, int(0.05 * SR)).astype(np.float32), 1800, 7200)
    tick *= np.exp(-np.arange(len(tick)) / SR * 90)
    for k, at in enumerate((9.4, 10.9, 12.3)):
        place(L, tick, at, 0.075)
        place(R, tick, at + 0.004, 0.07)

    # --- nada bawah saat −3,2 muncul
    m = int(1.4 * SR)
    t2 = np.arange(m) / SR
    low = np.sin(2 * np.pi * 116.5 * t2).astype(np.float32)
    low *= np.exp(-t2 * 2.2) * np.clip(t2 / 0.04, 0, 1)
    place(L, low, 12.55, 0.10)
    place(R, low, 12.57, 0.10)

    # --- dua batang tumbuh: dua nada pendek, kuart
    for f, at in ((174.6, 24.3), (233.1, 25.6)):
        m = int(0.9 * SR)
        t3 = np.arange(m) / SR
        tone = (np.sin(2 * np.pi * f * t3) * 0.55 + np.sin(2 * np.pi * f * 2 * t3) * 0.14)
        tone = tone.astype(np.float32) * np.exp(-t3 * 3.4) * np.clip(t3 / 0.03, 0, 1)
        place(L, tone, at, 0.10)
        place(R, tone, at + 0.01, 0.095)

    # --- gesekan tali saat simpul diikat (noise pita sempit, naik pelan)
    m = int(3.0 * SR)
    rng4 = np.random.default_rng(5150)
    rub = bandpass(rng4.normal(0, 1, m).astype(np.float32), 420, 2600)
    env = np.sin(np.linspace(0, np.pi, m)) ** 1.5
    rub *= env * 0.055
    place(L, rub, 39.6, 1.0)
    place(R, rub, 39.66, 0.95)

    # --- denyut mengendor: 5 ketukan pelan makin renggang
    at = 47.4
    gap = 0.34
    for k in range(5):
        m = int(0.5 * SR)
        t4 = np.arange(m) / SR
        thud = np.sin(2 * np.pi * 78 * t4).astype(np.float32) * np.exp(-t4 * 9)
        place(L, thud, at, 0.085)
        place(R, thud, at + 0.008, 0.08)
        at += gap
        gap += 0.16

    # --- "hampir nol": nada tinggi bersih, tanpa dasar
    m = int(2.6 * SR)
    t5 = np.arange(m) / SR
    hi = (np.sin(2 * np.pi * 1046.5 * t5) * 0.4 + np.sin(2 * np.pi * 1568 * t5) * 0.18).astype(np.float32)
    hi *= np.exp(-t5 * 1.3) * np.clip(t5 / 0.06, 0, 1)
    place(L, hi, 47.2, 0.075)
    place(R, hi, 47.22, 0.072)

    # --- penutup: satu akor rendah yang menutup, bukan menggelembung
    m = int(4.4 * SR)
    t6 = np.arange(m) / SR
    close = (np.sin(2 * np.pi * 98 * t6) * 0.5 + np.sin(2 * np.pi * 147 * t6) * 0.3
             + np.sin(2 * np.pi * 196 * t6) * 0.18).astype(np.float32)
    close *= np.exp(-t6 * 0.55) * np.clip(t6 / 0.5, 0, 1)
    place(L, close, 55.6, 0.11)
    place(R, close, 55.65, 0.105)

    L = reverb(L, 0.34)
    R = reverb(R, 0.34)

    st = np.stack([L, R], axis=1)
    fade = int(0.6 * SR)
    st[:fade] *= np.linspace(0, 1, fade)[:, None]
    st[-int(1.2 * SR):] *= np.linspace(1, 0, int(1.2 * SR))[:, None]
    pk = np.abs(st).max()
    if pk > 0:
        st = st / pk * 0.74
    return st



def build_ep02(dur):
    """Bunyi EP02 — kantor malam. Tempatnya interior, jadi ambience-nya
    dengung ruangan, bukan angin. Mikro-SFX hanya di titik perubahan:
    titik menyala, satu orang naik, dua batang tumbuh, satu kalimat penutup.

    Peta waktu:
      0.0–6.4   jalan     : dengung ruangan + 12 langkah di lantai keras
      6.4–18    hitung    : 4 klik tipis saat titik menyala, lalu nada rendah
                            saat "4 dari 100" masuk
      18–22.6   jalan     : langkah, dengung sama
      22.6–34   board     : satu nada naik pelan (titik menembus 5 jenjang),
                            ketukan kecil tiap jenjang, lalu satu thud saat
                            baris di bawahnya meredup
      34–38.6   jalan     : langkah
      38.6–52   banding   : gesekan batang tumbuh + satu nada saat +30 %
      52–60     penutup   : dua nada rendah untuk dua baris terakhir, ekor
                            dengung memudar
    """
    n = int(dur * SR)
    L = np.zeros(n, np.float32)
    R = np.zeros(n, np.float32)

    def place(buf, x, at, gain):
        i = int(at * SR)
        if i >= n:
            return
        m = min(len(x), n - i)
        buf[i:i + m] += x[:m] * gain

    # --- ambience ruangan: dengung 58 Hz + derau pita lebar yang sangat tipis
    tt = np.arange(n) / SR
    rng = np.random.default_rng(3307)
    air = bandpass(rng.normal(0, 1, n).astype(np.float32), 140, 1500)
    air *= (0.6 + 0.4 * np.sin(2 * np.pi * 0.045 * tt)) * 0.045
    L += air
    R += np.roll(air, 2200) * 0.9
    hum = (np.sin(2 * np.pi * 58 * tt) * 0.030
           + np.sin(2 * np.pi * 116 * tt) * 0.012).astype(np.float32)
    L += hum
    R += np.roll(hum, 700) * 0.95

    # --- langkah: lantai keras, lebih pendek dan lebih terang dari EP01
    rng2 = np.random.default_rng(6120)
    step = bandpass(rng2.normal(0, 1, int(0.10 * SR)).astype(np.float32), 320, 3800)
    step *= np.exp(-np.arange(len(step)) / SR * 58)
    for t0, t1 in ((0.15, 6.3), (18.05, 22.5), (34.05, 38.5)):
        t = t0
        while t < t1:
            g = 0.055 * (0.8 + 0.2 * math.sin(t * 2.1))
            place(L, step, t, g)
            place(R, step, t + 0.005, g * 0.94)
            t += 0.52

    # --- 4 titik menyala
    rng3 = np.random.default_rng(191)
    tick = bandpass(rng3.normal(0, 1, int(0.045 * SR)).astype(np.float32), 2400, 8200)
    tick *= np.exp(-np.arange(len(tick)) / SR * 105)
    for at in (9.2, 10.4, 11.6, 12.7):
        place(L, tick, at, 0.070)
        place(R, tick, at + 0.003, 0.066)

    # --- "4 dari 100": nada rendah pendek
    m = int(1.2 * SR)
    t2 = np.arange(m) / SR
    low = np.sin(2 * np.pi * 98 * t2).astype(np.float32)
    low *= np.exp(-t2 * 2.6) * np.clip(t2 / 0.04, 0, 1)
    place(L, low, 12.9, 0.10)
    place(R, low, 12.92, 0.10)

    # --- satu orang naik: glide naik 5 jenjang, ketukan tiap jenjang
    m = int(2.9 * SR)
    t3 = np.arange(m) / SR
    f0, f1 = 196.0, 392.0
    glide = np.sin(2 * np.pi * (f0 * t3 + (f1 - f0) * t3 * t3 / (2 * 2.9))).astype(np.float32)
    glide *= np.clip(t3 / 0.5, 0, 1) * np.clip((2.9 - t3) / 0.35, 0, 1) * 0.055
    place(L, glide, 26.2, 1.0)
    place(R, glide, 26.24, 0.95)
    for k in range(5):
        m = int(0.3 * SR)
        t4 = np.arange(m) / SR
        click = bandpass(rng3.normal(0, 1, m).astype(np.float32), 900, 5000)
        click *= np.exp(-t4 * 60)
        place(L, click, 26.4 + k * 0.56, 0.045)
        place(R, click, 26.41 + k * 0.56, 0.042)

    # --- thud saat baris di bawahnya meredup
    m = int(0.7 * SR)
    t5 = np.arange(m) / SR
    thud = (np.sin(2 * np.pi * 72 * t5) * 0.9).astype(np.float32) * np.exp(-t5 * 7)
    place(L, thud, 29.0, 0.085)
    place(R, thud, 29.01, 0.08)

    # --- dua batang tumbuh: gesekan pendek + satu nada saat +30 %
    m = int(2.6 * SR)
    rng5 = np.random.default_rng(7702)
    rub = bandpass(rng5.normal(0, 1, m).astype(np.float32), 500, 3200)
    rub *= (np.sin(np.linspace(0, np.pi, m)) ** 1.4) * 0.040
    place(L, rub, 39.7, 1.0)
    place(R, rub, 39.75, 0.95)
    m = int(1.8 * SR)
    t6 = np.arange(m) / SR
    tone = (np.sin(2 * np.pi * 261.6 * t6) * 0.45
            + np.sin(2 * np.pi * 392.0 * t6) * 0.22).astype(np.float32)
    tone *= np.exp(-t6 * 1.9) * np.clip(t6 / 0.05, 0, 1)
    place(L, tone, 41.0, 0.085)
    place(R, tone, 41.02, 0.082)

    # --- penutup: dua nada, lalu akor rendah yang tidak menggelembung
    for f, at in ((146.8, 48.6), (110.0, 49.9)):
        m = int(1.6 * SR)
        t7 = np.arange(m) / SR
        v = (np.sin(2 * np.pi * f * t7) * 0.6 + np.sin(2 * np.pi * f * 2 * t7) * 0.15)
        v = v.astype(np.float32) * np.exp(-t7 * 1.8) * np.clip(t7 / 0.05, 0, 1)
        place(L, v, at, 0.085)
        place(R, v, at + 0.008, 0.082)
    m = int(5.0 * SR)
    t8 = np.arange(m) / SR
    close = (np.sin(2 * np.pi * 73.4 * t8) * 0.5 + np.sin(2 * np.pi * 110 * t8) * 0.28
             + np.sin(2 * np.pi * 146.8 * t8) * 0.16).astype(np.float32)
    close *= np.exp(-t8 * 0.5) * np.clip(t8 / 0.6, 0, 1)
    place(L, close, 54.8, 0.11)
    place(R, close, 54.85, 0.105)

    L = reverb(L, 0.30)
    R = reverb(R, 0.30)

    st = np.stack([L, R], axis=1)
    fade = int(0.6 * SR)
    st[:fade] *= np.linspace(0, 1, fade)[:, None]
    st[-int(1.2 * SR):] *= np.linspace(1, 0, int(1.2 * SR))[:, None]
    pk = np.abs(st).max()
    if pk > 0:
        st = st / pk * 0.74
    return st


PRESETS = {"climb": build_climb, "reel": build_reel, "promo": build_promo,
           "ep01": build_ep01, "ep02": build_ep02}


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
