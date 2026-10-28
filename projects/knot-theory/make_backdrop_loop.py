#!/usr/bin/env python3
"""Bakar latar bergerak menjadi video loop 24 dtk (960x540) per tone.

Desain ulang setelah uji tayang: simpul raksasa di tengah membuat teks tenggelam.
Sekarang:

  - area teks (kiri 0–58%) sengaja dibiarkan gelap & rata
  - simpul jadi ORNAMEN TAJAM di kanan, kecil (0,52 H), berputar sangat lambat
  - dua bloom sangat lembut, satu di kanan-atas, satu di kanan-bawah
  - grain halus

Alasan tetap dibakar jadi video: di Remotion, gambar berlapis yang dianimasikan
per frame memakan 1,6 dtk/frame; satu video loop hanya 0,3 dtk/frame.

    python3 make_backdrop_loop.py --ffmpeg <ffmpeg> [--tone ink]
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
SECONDS = 24

TONES = {
    "ink":   ((70, 96, 148), (30, 40, 64)),
    "rose":  ((176, 108, 84), (32, 40, 66)),
    "sage":  ((92, 132, 100), (30, 42, 68)),
    "lilac": ((126, 110, 172), (30, 42, 70)),
}


def base_canvas():
    """Gradien ink + bidang gelap yang menahan teks di kiri."""
    ys = np.linspace(0, 1, H, dtype=np.float32)[:, None, None]
    xs = np.linspace(0, 1, W, dtype=np.float32)[None, :, None]
    top = np.array([11, 15, 22], np.float32)
    bot = np.array([20, 26, 38], np.float32)
    g = top[None, None, :] + (bot - top)[None, None, :] * (ys ** 0.8)
    img = np.broadcast_to(g, (H, W, 3)).astype(np.float32).copy()
    # bidang teks: digelapkan halus dari kiri sampai 58%
    hold = np.clip((0.60 - xs) / 0.60, 0, 1) ** 1.4
    img *= (1.0 - 0.16 * hold)
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8), "RGB").convert("RGBA")


def soft_disc(col, size=460):
    n = size
    yy, xx = np.mgrid[0:n, 0:n].astype(np.float32) / n
    d = np.sqrt((xx - 0.5) ** 2 + (yy - 0.5) ** 2) / 0.5
    a = (np.clip(1 - d, 0, 1) ** 3.0) * 0.42
    img = np.zeros((n, n, 4), np.float32)
    img[..., 0], img[..., 1], img[..., 2] = col
    img[..., 3] = a
    return Image.fromarray((img * 255).astype(np.uint8), "RGBA")


def build(tone, colors, knot_src, ffmpeg, total_seconds=SECONDS, suffix=""):
    base = base_canvas()
    warm = soft_disc(colors[0])
    cool = soft_disc(colors[1])
    knot = knot_src.resize((int(H * 0.52 * 1.4), int(H * 0.52 * 1.4)), Image.LANCZOS)

    frames = FPS * int(total_seconds)
    tmp = PUB / f"_loop_{tone}{suffix}.mp4"
    cmd = [ffmpeg, "-y", "-hide_banner", "-loglevel", "error",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "-",
           "-c:v", "libx264", "-preset", "slow", "-crf", "23", "-tune", "film",
           "-pix_fmt", "yuv420p", "-g", "60", "-movflags", "+faststart", str(tmp)]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    rng = np.random.default_rng(5)

    kx = W * 0.80
    ky = H * 0.50

    for i in range(frames):
        t = i / FPS
        ph = 2 * math.pi * t / SECONDS
        frame = base.copy()

        # bloom: hanya di sisi kanan, sangat lembut
        for layer, cxf, cyf, phase, op in (
            (warm, 0.86, 0.28, ph, 0.55),
            (cool, 0.74, 0.80, 2 * ph + 1.1, 0.50),
        ):
            cx = W * cxf + 34 * math.sin(phase)
            cy = H * cyf + 26 * math.cos(phase * 1.5)
            lay = layer
            if op < 1.0:
                a = lay.getchannel("A").point(lambda v, o=op: int(v * o))
                lay = lay.copy()
                lay.putalpha(a)
            frame.alpha_composite(lay, (int(cx - lay.width / 2), int(cy - lay.height / 2)))

        # ornamen simpul: tajam, kecil, berputar 1 putaran / 24 dtk
        ang = -t / SECONDS * 120   # trefoil bersimetri 3 lipat → mulus, tampak 3x lebih tenang
        s = 1 + 0.03 * math.sin(2 * ph)
        k = knot.rotate(ang, resample=Image.BICUBIC, expand=False)
        k = k.resize((int(k.width * s), int(k.height * s)), Image.BILINEAR)
        a = k.getchannel("A").point(lambda v: int(v * 0.13))
        k.putalpha(a)
        frame.alpha_composite(
            k, (int(kx + 22 * math.cos(2 * ph) - k.width / 2),
                int(ky + 30 * math.sin(2 * ph) - k.height / 2)))

        arr = np.asarray(frame.convert("RGB"), np.float32)
        arr += rng.normal(0, 2.2, (H, W, 1))
        proc.stdin.write(np.clip(arr, 0, 255).astype(np.uint8).tobytes())

    proc.stdin.close()
    proc.wait()
    final = PUB / f"loop-{tone}{suffix}.mp4"
    tmp.replace(final)
    print(f"  {final.name}  {final.stat().st_size/1024:6.0f} KB")

    return final


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--ffmpeg", required=True)
    ap.add_argument("--tone", default="all")
    a = ap.parse_args()
    src = Image.open(PUB / "knot-mark.png").convert("RGBA")
    white = Image.new("RGBA", src.size, (255, 255, 255, 0))
    white.putalpha(src.getchannel("A"))
    names = list(TONES) if a.tone == "all" else [a.tone]
    for tone in names:
        build(tone, TONES[tone], white, a.ffmpeg)          # satu putaran 24 dtk
        # Berkas panjang untuk render: digambar kontinu, bukan hasil concat.
        # Concat mp4 terbukti menyisipkan loncatan di setiap sambungan 24 dtk.
        build(tone, TONES[tone], white, a.ffmpeg, 312, "-long")
    print("selesai ->", PUB)
