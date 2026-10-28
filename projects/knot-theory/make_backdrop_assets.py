#!/usr/bin/env python3
"""Aset latar untuk Remotion: simpul besar (PNG) + tile grain (PNG).

Dua gambar kecil ini menggantikan filter SVG per frame. Animasi di Remotion
cukup memakai CSS transform + pergeseran background, jadi render tetap cepat.

    python3 make_backdrop_assets.py
"""
import re
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).parent
PUB = ROOT / "remotion" / "public" / "backdrop"
PUB.mkdir(parents=True, exist_ok=True)
SVG = ROOT.parent.parent / "brand" / "knot-theory" / "assets" / "logo-mark.svg"

SIZE = 1400          # kanvas simpul
STROKE = 0.055       # tebal relatif (tipis, karena ini ornamen bukan logo)


def load_paths():
    src = SVG.read_text(encoding="utf-8")
    return re.findall(r'<path d="([^"]+)"', src)


def knot_png():
    """Simpul digambar dari path SVG asli, diburamkan, disimpan sebagai PNG putih."""
    paths = load_paths()
    # render SVG -> PNG lewat ffmpeg tidak tersedia; pakai jalur sendiri:
    # ambil titik dari path (polyline) dan gambar dengan PIL
    im = Image.new("L", (SIZE, SIZE), 0)
    d = ImageDraw.Draw(im)
    for p in paths:
        pts = []
        for chunk in p.split(" L "):
            chunk = chunk.replace("M ", "").strip()
            x, y = chunk.split()
            pts.append((float(x), float(y)))
        if len(pts) < 2:
            continue
        scale = SIZE / 512
        poly = [(px * scale, py * scale) for px, py in pts]
        d.line(poly, fill=255, width=int(43.52 * scale), joint="curve")
        r = 43.52 * scale / 2
        for px, py in (poly[0], poly[-1]):
            d.ellipse([px - r, py - r, px + r, py + r], fill=255)
    # sengaja tanpa blur: ornamen harus tajam, bukan kabut
    white = Image.new("RGBA", (SIZE, SIZE), (255, 255, 255, 0))
    white.putalpha(im)
    white.save(PUB / "knot-mark.png", optimize=True)
    print('  knot-mark.png (tajam)')
    print(f"  knot-glow.png  {SIZE}x{SIZE}  {(PUB / 'knot-glow.png').stat().st_size//1024} KB")


TONES = {
    # nama: (warna bloom hangat, warna bloom dingin)
    "ink":   ((78, 104, 156), (34, 44, 70)),
    "rose":  ((196, 122, 96), (36, 44, 72)),
    "sage":  ((104, 146, 112), (34, 46, 76)),
    "lilac": ((140, 124, 186), (34, 46, 78)),
}

BLOOM = 900


def bloom_pngs():
    """Dua bloom per tone, warnanya sudah dibakar ke PNG.

    Animasi di Remotion cuma memindahkan gambar ini (transform), jadi tidak ada
    repaint gradien per frame — itu yang bikin render lambat.
    """
    n = BLOOM
    yy, xx = np.mgrid[0:n, 0:n].astype(np.float32) / n
    d = np.sqrt((xx - 0.5) ** 2 + (yy - 0.5) ** 2) / 0.5
    alpha = np.clip(1 - d, 0, 1) ** 2.3
    for name, (warm, cool) in TONES.items():
        for kind, col in (("warm", warm), ("cool", cool)):
            rgba = np.zeros((n, n, 4), dtype=np.uint8)
            rgba[..., 0], rgba[..., 1], rgba[..., 2] = col
            rgba[..., 3] = (alpha * (150 if kind == "warm" else 130)).astype(np.uint8)
            Image.fromarray(rgba, "RGBA").save(
                PUB / f"bloom-{name}-{kind}.png", optimize=True)
    print(f"  bloom: {len(TONES) * 2} berkas 900x900")


def grain_png(n=220):
    rng = np.random.default_rng(11)
    a = (rng.normal(128, 26, (n, n))).clip(0, 255).astype(np.uint8)
    Image.fromarray(a, mode="L").save(PUB / "grain.png")
    print(f"  grain.png  {n}x{n}  {(PUB / 'grain.png').stat().st_size//1024} KB")


if __name__ == "__main__":
    (PUB).mkdir(parents=True, exist_ok=True)
    knot_png()
    bloom_pngs()
    grain_png()
    print("selesai ->", PUB)
