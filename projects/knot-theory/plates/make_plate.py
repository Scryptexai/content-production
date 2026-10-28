#!/usr/bin/env python3
"""Plate latar bergerak untuk Knot Theory (tanpa Blender).

Tiap plate 12 detik, 1080x1920, 30 fps, dan punya tiga lapis gerak:

1. simpul trefoil raksasa yang berputar + melayang (gerak utama, terlihat)
2. dua bloom cahaya yang bernapas dengan fase berbeda (gerak halus)
3. grain yang bergerak tiap frame (tekstur, bukan objek)

Kontras dijaga <= 20% di area teks supaya narasi tetap terbaca.

    python3 make_plate.py                    # semua varian
    python3 make_plate.py --variant rose     # satu varian
"""
import argparse
import math
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).parent
OUT = ROOT.parent / "remotion" / "public" / "plates"
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1080, 1920
SW, SH = 540, 960            # kanvas kerja; di-upscale ke 1080x1920
FPS = 30
SECONDS = 12

INK_TOP = np.array([12, 16, 24], dtype=np.float32)
INK_BOTTOM = np.array([21, 27, 40], dtype=np.float32)

# nama: (bloom A, bloom B, kekuatan, warna garis simpul, terang simpul 0..1)
VARIANTS = {
    "ink":   ((60, 82, 126), (36, 46, 74), 1.00, (118, 136, 172), 0.20),
    "rose":  ((152, 96, 78), (50, 58, 92), 0.90, (156, 120, 106), 0.18),
    "sage":  ((86, 116, 92), (44, 56, 84), 0.90, (124, 148, 124), 0.18),
    "lilac": ((114, 102, 152), (44, 56, 88), 0.90, (138, 130, 176), 0.18),
}

# kurva trefoil (2,3) yang sama dengan logo
CURVE_T = np.linspace(0, 2 * np.pi, 900, endpoint=False)
CX = np.sin(CURVE_T) + 2 * np.sin(2 * CURVE_T)
CY = np.cos(CURVE_T) - 2 * np.cos(2 * CURVE_T)
C_SPAN = max(CX.max() - CX.min(), CY.max() - CY.min())


def knot_layer(t, size, angle, cx, cy, color, brightness):
    """Simpul sebagai garis, digambar di kanvas kecil lalu diburamkan."""
    layer = Image.new("RGB", (SW, SH), (0, 0, 0))
    d = ImageDraw.Draw(layer)
    s = size / C_SPAN
    ca, sa = math.cos(angle), math.sin(angle)
    x = CX * s
    y = -CY * s
    xs = cx + (x * ca - y * sa)
    ys = cy + (x * sa + y * ca)
    pts = list(zip(xs.tolist(), ys.tolist())) + [(xs[0], ys[0])]
    c = tuple(int(v * brightness) for v in color)
    d.line(pts, fill=c, width=max(2, int(size * 0.012)), joint="curve")
    return layer


def frame(t, colors, strength, line_color, line_bright):
    """t detik -> array RGB (SH, SW, 3) uint8."""
    ys = np.linspace(0, 1, SH, dtype=np.float32)[:, None, None]
    base = INK_TOP[None, None, :] + (INK_BOTTOM - INK_TOP)[None, None, :] * (ys ** 0.75)
    img = np.broadcast_to(base, (SH, SW, 3)).astype(np.float32).copy()

    # --- 1. simpul: berputar 24 derajat & melayang selama 12 dtk --------------
    phase = 2 * math.pi * t / SECONDS
    kx = SW * (0.50 + 0.045 * math.sin(phase))
    ky = SH * (0.50 + 0.070 * math.cos(phase * 0.85))
    size = SH * (0.92 + 0.05 * math.sin(phase * 0.7))
    layer = knot_layer(t, size, 0.42 * phase, kx, ky, line_color, line_bright)
    layer = layer.filter(ImageFilter.GaussianBlur(2.4))
    img += np.asarray(layer, dtype=np.float32)

    # --- 2. bloom cahaya ----------------------------------------------------
    xy = np.mgrid[0:SW, 0:SH]
    xs_n = xy[0].T.astype(np.float32) / SW
    ys_n = xy[1].T.astype(np.float32) / SH
    blooms = [
        (colors[0], 0.030 * math.sin(phase * 1.3), 0.024 * math.cos(phase * 1.05), 0.50, 0.34),
        (colors[1], 0.034 * math.sin(phase * 0.9 + 2.1), 0.030 * math.cos(phase * 1.15 + 1.2), 0.56, 0.30),
    ]
    for color, dx, dy, radius, amp in blooms:
        cxx, cyy = 0.5 + dx, 0.46 + dy
        d = np.sqrt(((xs_n - cxx) / (radius * SW / SH * 1.9)) ** 2 + ((ys_n - cyy) / radius) ** 2)
        falloff = np.clip(1.0 - d, 0.0, 1.0) ** 2.4
        img += np.array(color, dtype=np.float32)[None, None, :] * falloff[..., None] * amp * strength

    # --- 3. grain yang bergerak --------------------------------------------
    rng = np.random.default_rng(int(t * 1000) % 7919)
    img += rng.normal(0, 2.6, (SH, SW, 1)).astype(np.float32)

    return np.clip(img, 0, 255).astype(np.uint8)


def build(name, colors, strength, line_color, line_bright, ffmpeg):
    tmp = OUT / f"_plate_{name}.mp4"
    cmd = [
        ffmpeg, "-y", "-hide_banner", "-loglevel", "error",
        "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{SW}x{SH}",
        "-r", str(FPS), "-i", "-",
        "-vf", f"scale=540:960:flags=lanczos,gblur=sigma=0.8,vignette=PI/4.6",
        "-c:v", "libx264", "-preset", "slow", "-crf", "24", "-tune", "film",
        "-g", "60", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(tmp),
    ]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(FPS * SECONDS):
        p.stdin.write(frame(i / FPS, colors, strength, line_color, line_bright).tobytes())
    p.stdin.close()
    p.wait()
    final = OUT / f"{name}-loop.mp4"
    tmp.replace(final)
    print(f"  {final.name}  {final.stat().st_size/1024:6.0f} KB")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--variant", default="all")
    ap.add_argument("--ffmpeg", default="ffmpeg")
    args = ap.parse_args()

    names = list(VARIANTS) if args.variant == "all" else [args.variant]
    for n in names:
        a, b, s, lc, lb = VARIANTS[n]
        build(n, (a, b), s, lc, lb, args.ffmpeg)
    print("selesai ->", OUT)
