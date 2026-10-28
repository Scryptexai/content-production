#!/usr/bin/env python3
"""Bakar 8 "plate" latar 960x540 untuk video 16:9.

Kenapa 8, bukan 1: video sebelumnya terasa seperti presentasi karena latar
yang sama dipakai 3,5 menit. Di sini tiap ±6 detik latar berganti plate yang
tampilannya jelas berbeda (terang/gelap, garis, cincin, bidang besar), jadi
mata dapat perubahan walau gambar di atasnya sedang tenang.

    python3 make_plates.py --ffmpeg <ffmpeg>
"""
import argparse
import math
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).parent
PUB = ROOT / "remotion" / "public" / "backdrop"
W, H = 960, 540
FPS = 30
SECONDS = 20
N = FPS * SECONDS

INK_TOP = np.array([8, 11, 18], np.float32)
INK_BOT = np.array([19, 25, 37], np.float32)
CREAM = np.array([239, 231, 220], np.float32)
ROSE = np.array([217, 142, 115], np.float32)
SAGE = np.array([143, 169, 139], np.float32)
LILAC = np.array([167, 155, 200], np.float32)

YY, XX = np.mgrid[0:H, 0:W].astype(np.float32)
XN = XX / W
YN = YY / H


def knot_at(angle, px, py, scale, alpha):
    """Simpul sebagai RGBA numpy, sudah diputar & ditempatkan."""
    return ("knot", angle, px, py, scale, alpha)


class KnotSprite:
    """Rotasi simpul di-cache: 72 sudut cukup untuk gerak lambat."""

    def __init__(self, path):
        src = Image.open(path).convert("RGBA")
        self.base = src
        self.cache = {}

    def get(self, angle_deg, size):
        key = (int(round(angle_deg)) % 360, size)
        if key not in self.cache:
            im = self.base.rotate(-key[0], resample=Image.BICUBIC, expand=False)
            im = im.resize((size, size), Image.LANCZOS)
            self.cache[key] = np.asarray(im, np.float32)
        return self.cache[key]


def ink_base():
    g = INK_TOP[None, None, :] + (INK_BOT - INK_TOP)[None, None, :] * (YN[..., None] ** 0.8)
    return np.broadcast_to(g, (H, W, 3)).astype(np.float32).copy()


def blend(img, rgb, alpha):
    """alpha: (H,W) atau skalar."""
    a = alpha[..., None] if isinstance(alpha, np.ndarray) and alpha.ndim == 2 else alpha
    return img * (1 - a) + np.asarray(rgb, np.float32)[None, None, :] * a


def radial(cx, cy, radius, power=2.4):
    d = np.sqrt((XX - cx) ** 2 + (YY - cy) ** 2) / radius
    return np.clip(1 - d, 0, 1) ** power


# ---------------------------------------------------------------- plates
def plate_field(t, knot):
    """Bidang ink + sapuan cahaya diagonal bergerak lambat."""
    img = ink_base()
    ph = 2 * math.pi * t / SECONDS
    cx = W * (0.25 + 0.55 * (0.5 + 0.5 * math.sin(ph)))
    glow = radial(cx, H * 0.34, 520, 2.0) * 0.30
    img = blend(img, (86, 104, 150), glow)
    k = knot.get(t / SECONDS * 60, 900)
    x0 = int(W * 0.72 - k.shape[0] / 2 + 30 * math.sin(ph))
    y0 = int(H * 0.5 - k.shape[0] / 2)
    return paste(img, k, x0, y0, 0.16)


def plate_grid(t, knot):
    """Grid perspektif yang bergerak ke arah penonton: terasa seperti ruang."""
    img = ink_base()
    horizon = H * 0.58
    vp_x = W * 0.5
    ph = t / 2.1
    # garis horizontal: jarak makin lebar ke bawah, digeser terus
    for i in range(26):
        k = ((i + ph) % 26) / 26
        y = horizon + (k ** 2.3) * (H - horizon) * 1.15
        if y >= H:
            continue
        a = 0.34 * (1 - k) ** 0.55
        row = int(y)
        if 0 <= row < H:
            img[row, :, :] = img[row, :, :] * (1 - a) + np.array([150, 180, 230], np.float32) * a
    # garis vertikal menuju titik hilang
    for j in range(-9, 10):
        x_bottom = vp_x + j * W * 0.115
        for yy in range(int(horizon), H):
            f = (yy - horizon) / max(1, (H - horizon))
            x = vp_x + (x_bottom - vp_x) * f
            xi = int(x)
            if 0 <= xi < W:
                a = 0.26 * f
                img[yy, xi, :] = img[yy, xi, :] * (1 - a) + np.array([140, 170, 220], np.float32) * a
    glow = radial(vp_x, horizon, 460, 1.7) * 0.42
    img = blend(img, (70, 92, 140), glow)
    return img


def plate_band(t, knot):
    """Pita warna rose melintas naik-turun: potongan yang hangat."""
    img = ink_base()
    ph = 2 * math.pi * t / SECONDS
    cy = H * (0.5 + 0.28 * math.sin(ph))
    band = np.exp(-((YY - cy) / 120.0) ** 2) * 0.55
    img = blend(img, ROSE * 0.62, band)
    img = blend(img, (40, 26, 24), np.exp(-((YY - cy) / 44.0) ** 2) * 0.25)
    k = knot.get(180 + t / SECONDS * 40, 640)
    return paste(img, k, int(W * 0.80 - 320), int(H * 0.5 - 320), 0.10)


def plate_streak(t, knot):
    """Garis-garis vertikal bergerak horizontal dengan kecepatan beda."""
    img = ink_base()
    for i, (speed, off, col, wdt) in enumerate((
        (0.55, 0.0, (150, 120, 190), 26),
        (0.32, 0.33, (110, 150, 180), 40),
        (0.80, 0.70, (190, 150, 160), 16),
    )):
        cx = ((t * speed / SECONDS + off) % 1.0) * (W + 400) - 200
        band = np.exp(-((XX - cx) / wdt) ** 2) * 0.42
        img = blend(img, col, band)
    img = blend(img, LILAC * 0.5, radial(W * 0.5, H * 0.2, 560, 2.2) * 0.30)
    return img


def plate_rings(t, knot):
    """Cincin yang mengembang dari kiri-bawah, seperti gelombang data."""
    img = ink_base()
    ox, oy = W * 0.28, H * 0.78
    d = np.sqrt((XX - ox) ** 2 + (YY - oy) ** 2)
    for i in range(4):
        r = ((t * 40 + i * 96) % 430)
        ring = np.exp(-((d - r) / 26.0) ** 2) * (0.30 * (1 - r / 430))
        img = blend(img, SAGE * 0.75, ring)
    img = blend(img, (54, 78, 64), radial(ox, oy, 360, 2.2) * 0.20)
    return img


def plate_knot(t, knot):
    """Simpul besar memotong dari kanan. Kontras tinggi, dramatis."""
    img = ink_base() * 0.85
    ph = 2 * math.pi * t / SECONDS
    k = knot.get(t / SECONDS * 120, 1500)
    x0 = int(W * 0.86 - k.shape[0] / 2 + 40 * math.cos(ph))
    y0 = int(H * 0.5 - k.shape[0] / 2 + 40 * math.sin(ph))
    img = paste(img, k, x0, y0, 0.30)
    img = blend(img, (90, 110, 150), radial(W * 0.15, H * 0.5, 620, 2.2) * 0.22)
    return img


def plate_paper(t, knot):
    """Bidang krem bersih: satu garis tenang, simpul besar samar.

    Sengaja nyaris polos — di antara plate gelap yang ramai, plate ini jadi
    jeda mata. Teks di atasnya memakai tinta gelap.
    """
    img = np.broadcast_to(CREAM[None, None, :], (H, W, 3)).astype(np.float32).copy()
    ph = 2 * math.pi * t / SECONDS
    img = blend(img, (226, 210, 190), radial(W * (0.72 + 0.06 * math.sin(ph)), H * 0.28, 700, 1.7) * 0.50)
    k = knot.get(200 + t / SECONDS * 40, 1700)
    img = paste(img, k, int(W * 0.30 - 900) + int(20 * math.cos(ph)), int(H * 0.55 - 900), 0.075, dark=True)
    # satu garis tipis: cukup untuk menyatakan struktur
    y0 = H * (0.80 + 0.02 * math.sin(ph))
    for dy in range(-1, 2):
        row = int(y0) + dy
        if 0 <= row < H:
            a = 0.55 if dy == 0 else 0.16
            img[row, :, :] = img[row, :, :] * (1 - a) + ROSE * 0.85 * a
    v = radial(W * 0.5, H * 0.5, 860, 1.1)
    img = blend(img, (214, 202, 186), (1 - v) * 0.28)
    return img


def plate_bars(t, knot):
    """Dinding batang vertikal yang bergerak: bahasa data, bukan gραφik."""
    img = ink_base()
    n = 34
    bw = W / n
    ph = t / SECONDS
    for i in range(n):
        h = (0.35 + 0.3 * math.sin(i * 0.7 + ph * 2 * math.pi * 1.0)
             + 0.18 * math.sin(i * 0.23 - ph * 2 * math.pi * 0.6))
        h = max(0.08, min(0.95, h))
        x0 = int(i * bw + bw * 0.18)
        x1 = int(i * bw + bw * 0.82)
        y0 = int(H * (1 - h))
        col = (120, 140, 185) if i % 3 else (170, 130, 120)
        img[y0:H, x0:x1, :] = img[y0:H, x0:x1, :] * 0.45 + np.array(col, np.float32) * 0.28
    img = blend(img, (70, 90, 130), radial(W * 0.5, H * 0.05, 520, 2.0) * 0.25)
    return img


def paste(img, sprite, x0, y0, alpha, dark=False):
    """Tempel RGBA numpy ke img pada (x0,y0), terpotong di tepi."""
    sh, sw = sprite.shape[:2]
    x1, y1 = x0 + sw, y0 + sh
    cx0, cy0 = max(0, x0), max(0, y0)
    cx1, cy1 = min(W, x1), min(H, y1)
    if cx1 <= cx0 or cy1 <= cy0:
        return img
    sub = sprite[cy0 - y0:cy1 - y0, cx0 - x0:cx1 - x0]
    a = (sub[..., 3:4] / 255.0) * alpha
    tint = np.array([10, 14, 22], np.float32) if dark else np.array([235, 238, 245], np.float32)
    region = img[cy0:cy1, cx0:cx1, :]
    img[cy0:cy1, cx0:cx1, :] = region * (1 - a) + tint[None, None, :] * a
    return img


PLATES = {
    "field": plate_field,
    "grid": plate_grid,
    "band": plate_band,
    "streak": plate_streak,
    "rings": plate_rings,
    "knot": plate_knot,
    "paper": plate_paper,
    "bars": plate_bars,
}


def build(name, fn, knot, ffmpeg):
    out = PUB / f"plate-{name}.mp4"
    cmd = [ffmpeg, "-y", "-hide_banner", "-loglevel", "error",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-pix_fmt", "yuv420p",
           "-g", "48", "-movflags", "+faststart", str(out)]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    rng = np.random.default_rng(11)
    for i in range(N):
        img = fn(i / FPS, knot)
        img = img + rng.normal(0, 2.0, (H, W, 1))
        proc.stdin.write(np.clip(img, 0, 255).astype(np.uint8).tobytes())
    proc.stdin.close()
    proc.wait()
    print(f"  {out.name:22s} {out.stat().st_size/1024:6.0f} KB")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--ffmpeg", required=True)
    ap.add_argument("--only", default="")
    a = ap.parse_args()
    knot = KnotSprite(PUB / "knot-mark.png")
    names = [a.only] if a.only else list(PLATES)
    for n in names:
        build(n, PLATES[n], knot, a.ffmpeg)
    print("selesai ->", PUB)
