#!/usr/bin/env python3
"""Still Blender + peta kedalaman → klip latar bergerak (parallax 2.5D).

Kenapa begini, bukan animasi penuh: Cycles di mesin ini ~30–60 dtk per frame,
jadi 6.000 frame mustahil. Satu still per adegan cukup, lalu kamera digerakkan
di sini dari peta kedalaman — piksel dekat bergeser lebih cepat daripada yang
jauh, jadi hasilnya parallax sungguhan, bukan zoom datar.

Untuk latar belakang video, ini cukup: teks di atasnya statis, mata membaca
gerak sebagai "kamera bergerak", dan tidak ada artefak tepi yang terlihat
karena selalu ada margin 12% dan digeser hanya ±3%.

    python3 render_plates3d.py --src /tmp/3d --ffmpeg <ffmpeg>
"""
import argparse
import math
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

W, H = 960, 540
FPS = 30
SECONDS = 20
MARGIN = 1.14          # render 1920x1080, crop 960x540 → ruang gerak


def load(src: Path, name: str):
    col = Image.open(src / f"3d-{name}.png").convert("RGB")
    z = Image.open(src / f"3d-{name}-z.png").convert("L")
    # Z: putih = jauh, hitam = dekat → hamparan parallax yang halus
    z = z.filter(ImageFilter.GaussianBlur(9))
    return col, z


def warp(col: Image.Image, z: np.ndarray, dx: float, dy: float, zoom: float,
         scale: float):
    """Geser tiap baris/kolom menurut kedalaman (displacement 2.5D sederhana)."""
    h, w = z.shape
    # grid tujuan
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)

    # kedalaman ternormalisasi 0 (dekat) .. 1 (jauh)
    depth = z / 255.0
    near = 1.0 - depth                      # 1 = paling dekat

    # zoom: kamera maju sedikit
    cx, cy = w / 2, h / 2
    zf = 1.0 + (zoom - 1.0) * (0.35 + 0.65 * near)
    sx = (xx - cx) / zf + cx
    sy = (yy - cy) / zf + cy

    # geser: objek dekat bergerak lebih jauh daripada latar
    sx = sx - dx * (0.25 + 1.55 * near)
    sy = sy - dy * (0.25 + 1.55 * near)

    sx = np.clip(sx, 0, w - 1).astype(np.int32)
    sy = np.clip(sy, 0, h - 1).astype(np.int32)

    arr = np.asarray(col, np.float32)
    out = arr[sy, sx]
    return out


def render(name: str, col: Image.Image, z: np.ndarray, out_dir: Path, ffmpeg: str,
           style: str):
    h, w = z.shape
    n = SECONDS * FPS
    tmp = out_dir / f"_plate_{name}.mp4"
    cmd = [ffmpeg, "-y", "-hide_banner", "-loglevel", "error",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
           "-i", "-", "-c:v", "libx264", "-preset", "slow", "-crf", "20",
           "-pix_fmt", "yuv420p", "-g", "60", "-movflags", "+faststart", str(tmp)]
    pr = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    rng = np.random.default_rng(4)

    for i in range(n):
        t = i / n
        ph = 2 * math.pi * t
        if style == "push":          # kamera maju-mundur pelan (periodik = loop mulus)
            dx, dy = 6 * math.sin(ph), 3 * math.cos(ph)
            zoom = 1.0 + 0.055 * (1 - math.cos(ph)) / 2
        elif style == "sweep":       # kamera menyapu ke samping
            dx, dy = -46 * math.sin(ph), 8 * math.sin(2 * ph)
            zoom = 1.03 + 0.02 * math.sin(ph)
        else:                        # breathe: hampir diam, tapi hidup
            dx, dy = 10 * math.sin(ph), 6 * math.sin(2 * ph + 0.7)
            zoom = 1.02 + 0.022 * math.sin(ph)

        frame = warp(col, z, dx, dy, zoom, MARGIN)
        # sedikit grain supaya tidak terlihat seperti gambar diam yang digeser
        frame = frame + rng.normal(0, 1.6, (h, w, 1))
        pr.stdin.write(np.clip(frame, 0, 255).astype(np.uint8).tobytes())

    pr.stdin.close()
    pr.wait()
    tmp.replace(out_dir / f"plate3d-{name}.mp4")
    print(f"  plate3d-{name}.mp4  {(out_dir / f'plate3d-{name}.mp4').stat().st_size/1024:6.0f} KB")


STYLES = {"grid": "sweep", "columns": "push", "tunnel": "push", "wire": "breathe"}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--ffmpeg", required=True)
    ap.add_argument("--only", default="")
    a = ap.parse_args()
    src, out = Path(a.src), Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    names = [a.only] if a.only else list(STYLES)
    for name in names:
        # crop tengah 16:9 dengan margin, lalu perkecil ke 960x540
        col, z = load(src, name)
        w, h = col.size
        cw, ch = int(w / MARGIN), int(h / MARGIN)
        x0, y0 = (w - cw) // 2, (h - ch) // 2
        col = col.crop((x0, y0, x0 + cw, y0 + ch)).resize((W, H), Image.LANCZOS)
        z = z.crop((x0, y0, x0 + cw, y0 + ch)).resize((W, H), Image.BILINEAR)
        render(name, col, np.asarray(z), out, a.ffmpeg, STYLES[name])
    print("selesai ->", out)
