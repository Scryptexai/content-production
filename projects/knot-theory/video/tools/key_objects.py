#!/usr/bin/env python3
"""
key_objects.py — potong objek foto dari latar hijau jadi PNG transparan.

Kenapa tidak pakai chromakey bawaan ffmpeg: hasilnya menyisakan piksel
beralfa rendah di seluruh bidang (gradien lampu studio), sehingga tepi objek
tidak bisa dipotong rapat dan bayangan kontak tidak bisa ditempatkan. Di sini
alfa dihitung dari "seberapa hijau" piksel, lalu dinaikkan kontrasnya,
di-despill, dan kotaknya dipotong ke batas objek.

Aturan alfa:
  d  = seberapa jauh hijau mengungguli kanal merah/biru terbesar
  a  = 1 - clamp((d - T0) / (T1 - T0))   → 0 di latar, 1 di objek
Despill: kelebihan hijau dikurangi dari kanal hijau pada piksel tepi, supaya
tidak ada garis hijau di sekeliling objek saat diletakkan di latar gelap.
"""
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent / "public" / "objects"

# Ambang dari SELISIH hijau (g − max(r,b)), bukan rasio: pada keenam foto,
# latar turun paling rendah ke 96 dan badan objek naik paling tinggi ke 21.
# Rasio hijau gagal di sini karena latar yang lebih gelap punya rasio lebih
# rendah daripada logam yang memantulkan sedikit hijau.
T0, T1 = 44.0, 92.0
PAD = 8               # margin transparan di sekitar objek (px)
TRIM_ALPHA = 200      # ambang untuk menghitung kotak objek


def key(src: Path, dst: Path) -> tuple[int, int]:
    img = Image.open(src).convert("RGB")
    a = np.asarray(img).astype(np.float32)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    dom = np.maximum(r, b)
    green = g - dom

    alpha = 1.0 - np.clip((green - T0) / (T1 - T0), 0.0, 1.0)

    # Despill: cahaya hijau dari latar memantul ke sisi objek, jadi hijau harus
    # DIBATASI, bukan hanya dikurangi kelebihan di piksel tepi. Batasnya sedikit
    # di atas kanal merah/biru terbesar; objek di sini tidak ada yang hijau,
    # sehingga batas ini aman dan menghilangkan warna hijau di kayu ballot box.
    cap = dom * 1.06 + 6.0
    g2 = np.clip(np.minimum(g, cap), 0.0, 255.0)

    # pinggirkan alfa: piksel yang jelas objek jadi 255, latar jadi 0
    alpha = np.where(alpha > 0.86, 1.0, alpha)
    alpha = np.where(alpha < 0.14, 0.0, alpha)

    out = np.dstack([r, g2, b, alpha * 255.0]).astype(np.uint8)
    im = Image.fromarray(out, "RGBA")

    # kotak objek dari alfa > TRIM_ALPHA
    solid = (alpha * 255.0) > TRIM_ALPHA
    ys, xs = np.where(solid)
    if len(xs) == 0:
        raise SystemExit(f"tidak ada objek terdeteksi: {src.name}")
    x0, x1 = max(0, xs.min() - PAD), min(im.width, xs.max() + 1 + PAD)
    y0, y1 = max(0, ys.min() - PAD), min(im.height, ys.max() + 1 + PAD)
    im = im.crop((int(x0), int(y0), int(x1), int(y1)))

    dst.parent.mkdir(parents=True, exist_ok=True)
    im.save(dst)
    return im.width, im.height


def main() -> None:
    raws = sorted((ROOT / "raw").glob("*.png"))
    if not raws:
        raise SystemExit("tidak ada public/objects/raw/*.png")
    for src in raws:
        w, h = key(src, ROOT / f"{src.stem}.png")
        print(f"{src.stem:14s} -> {w}x{h}")


if __name__ == "__main__":
    main()
