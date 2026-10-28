#!/usr/bin/env python3
"""Uji konsep: adegan 3D prosedural (proyeksi perspektif + nyala) → video.

Blender tidak bisa dipakai di sandbox ini (tidak ada library X11/OpenGL, tidak
ada root). Jadi adegan 3D-nya dihitung sendiri dengan numpy lalu digambar
sebagai poligon: kamera bisa bergerak, kedalaman memberi parallax, dan cahaya
dihitung dari arah. Hasilnya bukan foto diam — kameranya benar-benar jalan.

    python3 proof_scene.py --ffmpeg <ffmpeg>
"""
import argparse
import math
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

W, H = 960, 540
FPS = 30
PUB = Path(__file__).parent / "remotion" / "public" / "backdrop"

INK = (10, 14, 22)
CREAM = (239, 231, 220)
ROSE = (217, 142, 115)
SAGE = (143, 169, 139)
MUTED = (138, 147, 163)


# ------------------------------------------------------------------ kamera
class Cam:
    def __init__(self, eye, look, fov=52.0, w=W, h=H):
        self.eye = np.array(eye, float)
        f = np.array(look, float) - self.eye
        f /= np.linalg.norm(f)
        up = np.array([0.0, -1.0, 0.0])
        r = np.cross(f, up)
        r /= np.linalg.norm(r)
        u = np.cross(r, f)
        self.f, self.r, self.u = f, r, u
        self.focal = (h / 2) / math.tan(math.radians(fov) / 2)
        self.cx, self.cy = w / 2, h / 2

    def project(self, pts):
        pts = np.asarray(pts, float)
        d = pts - self.eye
        z = d @ self.f
        x = d @ self.r
        y = d @ self.u
        z = np.maximum(z, 0.05)
        return np.stack([self.cx + self.focal * x / z,
                         self.cy - self.focal * y / z, z], axis=-1)


def shade(base, normal, light, amb=0.42, gain=0.72):
    n = np.asarray(normal, float)
    n /= np.linalg.norm(n)
    l = np.asarray(light, float)
    l /= np.linalg.norm(l)
    k = amb + gain * max(0.0, float(n @ l))
    return tuple(min(255, int(c * k)) for c in base)


def fog(col, z, near=6.0, far=26.0, fg=(9, 12, 19)):
    t = np.clip((z - near) / (far - near), 0, 1) ** 1.4
    return tuple(int(col[i] * (1 - t) + fg[i] * t) for i in range(3))


def box_faces(x, y, z, sx, sy, sz):
    """8 titik + 5 sisi (tanpa alas) sebuah balok."""
    p = np.array([[x, y, z], [x + sx, y, z], [x + sx, y, z + sz], [x, y, z + sz],
                  [x, y + sy, z], [x + sx, y + sy, z], [x + sx, y + sy, z + sz],
                  [x, y + sy, z + sz]], float)
    faces = [((0, 1, 2, 3), (0, 1, 0)), ((4, 5, 6, 7), (0, -1, 0)),
             ((0, 1, 5, 4), (0, 0, -1)), ((3, 2, 6, 7), (0, 0, 1)),
             ((1, 2, 6, 5), (1, 0, 0)), ((0, 3, 7, 4), (-1, 0, 0))]
    return p, faces


def add_glow(arr, pts, radius=26, col=(120, 150, 200), strength=0.55):
    """Nyala lembut di sekitar satu titik layar (aditif)."""
    x, y = int(pts[0]), int(pts[1])
    if not (0 <= x < W and 0 <= y < H):
        return
    r = radius
    x0, x1 = max(0, x - r), min(W, x + r + 1)
    y0, y1 = max(0, y - r), min(H, y + r + 1)
    yy, xx = np.mgrid[y0:y1, x0:x1]
    d = np.sqrt((xx - x) ** 2 + (yy - y) ** 2) / r
    k = np.clip(1 - d, 0, 1) ** 2.2 * strength
    for c in range(3):
        arr[y0:y1, x0:x1, c] += col[c] * k


def draw_scene(draw, cam, items, light):
    """items: list of (depth, points2d, color, outline) — digambar jauh→dekat."""
    for depth, poly, col, edge in sorted(items, key=lambda t: -t[0]):
        draw.polygon([tuple(map(float, q)) for q in poly], fill=col,
                     outline=edge)


# ------------------------------------------------------- adegan 1: lantai kantor
def shot_office(t, dur):
    """Lantai isometrik dengan deretan meja; beberapa titik bergerak pelan."""
    img = Image.new("RGB", (W, H), INK)
    d = ImageDraw.Draw(img)
    # langit-langit: gradien sederhana
    for y in range(0, H):
        k = y / H
        d.line([(0, y), (W, y)], fill=(int(9 + 6 * k), int(12 + 8 * k), int(19 + 11 * k)))

    p = t / dur
    cam = Cam(eye=(-3.4 + 6.4 * p, -2.6 + 3.0 * p, 1.42),
              look=(-0.6 + 5.0 * p, 4.4, 0.92), fov=42)
    light = (0.35, 0.85, -0.4)
    items, glows = [], []

    # lantai: petak besar supaya ada acuan gerak
    for gx in range(-9, 10):
        for gy in range(-4, 15):
            x, y = gx * 1.15, gy * 1.15
            quad = np.array([[x, y, 0], [x + 1.15, y, 0], [x + 1.15, y + 1.15, 0], [x, y + 1.15, 0]], float)
            pr = cam.project(quad)
            z = pr[:, 2].mean()
            if z < 0.4 or z > 30:
                continue
            base = (17, 22, 32) if (gx + gy) % 2 == 0 else (14, 19, 28)
            items.append((z, pr[:, :2], fog(base, z), None))

    # meja-meja
    rng = np.random.default_rng(7)
    for gx in range(-6, 7):
        for gy in range(0, 11):
            x, y = gx * 1.9 + 0.3, gy * 1.9 + 1.0
            hgt = 0.72
            pts, faces = box_faces(x, y, 0, 1.25, 0.66, hgt)
            pr = cam.project(pts)
            z = pr[:, 2].mean()
            if z < 0.5 or z > 26:
                continue
            for idx, nrm in faces:
                poly = pr[list(idx)]
                if poly[:, 2].min() <= 0.5:
                    continue
                lit = shade((30, 38, 52), nrm, light)
                if nrm == (0, 0, 1):
                    lit = shade((44, 54, 70), nrm, light)
                items.append((poly[:, 2].mean(), poly[:, :2], fog(lit, z), None))
            # layar monitor menyala
            sx, sy = x + 0.42, y + 0.18
            sp, sf = box_faces(sx, sy, hgt, 0.42, 0.05, 0.34)
            spr = cam.project(sp)
            sz = spr[:, 2].mean()
            for idx, nrm in sf:
                if nrm != (0, -1, 0):
                    continue
                poly = spr[list(idx)]
                if poly[:, 2].min() <= 0.5:
                    continue
                glow = (98, 126, 168) if (gx + gy) % 3 else (150, 122, 108)
                items.append((poly[:, 2].mean(), poly[:, :2], fog(glow, sz, far=22), None))
                glows.append((poly[:, :2].mean(axis=0), glow, max(6, int(26 * 8 / max(4, sz)))))

    # orang: titik tinggi yang bergerak, sedikit berayun
    for i in range(26):
        gx = rng.integers(-6, 7)
        gy = float(rng.integers(0, 11))
        speed = 0.35 + 0.25 * rng.random()
        yy = (gy + speed * t) % 11.0
        x, y = gx * 1.9 + 0.9, yy * 1.9 + 1.0
        sway = 0.06 * math.sin(t * 2.0 + i)
        pts, faces = box_faces(x + sway, y, 0, 0.26, 0.26, 1.28)
        pr = cam.project(pts)
        z = pr[:, 2].mean()
        if z < 0.5 or z > 24:
            continue
        for idx, nrm in faces:
            poly = pr[list(idx)]
            if poly[:, 2].min() <= 0.5:
                continue
            base = (206, 196, 182) if i % 5 else (176, 122, 102)
            items.append((poly[:, 2].mean(), poly[:, :2], fog(shade(base, nrm, light), z), None))

    draw_scene(d, cam, items, light)
    arr = np.asarray(img, dtype=np.float32)
    for (pt, col, rad) in glows:
        add_glow(arr, pt, radius=rad, col=col, strength=0.30)
    return arr


# --------------------------------------------------- adegan 2: kota data
def shot_data_city(t, dur):
    """Kamera menyusuri lapangan batang data yang tumbuh."""
    img = Image.new("RGB", (W, H), INK)
    d = ImageDraw.Draw(img)
    for y in range(0, H):
        k = y / H
        d.line([(0, y), (W, y)], fill=(int(9 + 5 * k), int(12 + 7 * k), int(20 + 10 * k)))

    p = t / dur
    cam = Cam(eye=(-5.0 + 7.0 * p, -6.4 + 5.0 * p, 1.9),
              look=(0.6 + 1.2 * p, 3.4, 1.0), fov=44)
    light = (0.5, 0.75, -0.45)
    items = []

    # alas gelap
    for gy in range(-3, 14):
        for gx in range(-8, 9):
            x, y = gx * 1.0, gy * 1.0
            quad = np.array([[x, y, 0], [x + 1, y, 0], [x + 1, y + 1, 0], [x, y + 1, 0]], float)
            pr = cam.project(quad)
            z = pr[:, 2].mean()
            if z < 0.4 or z > 32:
                continue
            base = (13, 17, 26)
            items.append((z, pr[:, :2], fog(base, z, far=30), None))

    for gy in range(0, 13):
        for gx in range(-7, 8):
            h = 0.35 + 1.9 * (0.5 + 0.5 * math.sin(gx * 0.55 + gy * 0.34 - t * 0.8)) ** 1.6
            x, y = gx * 1.0 + 0.15, gy * 1.0 + 0.15
            pts, faces = box_faces(x, y, 0, 0.7, 0.7, h)
            pr = cam.project(pts)
            z = pr[:, 2].mean()
            if z < 0.5 or z > 30:
                continue
            for idx, nrm in faces:
                poly = pr[list(idx)]
                if poly[:, 2].min() <= 0.5:
                    continue
                top = nrm == (0, 0, 1)
                base = (126, 152, 132) if (gx + gy) % 4 else (186, 138, 118)
                if top:
                    base = tuple(min(255, int(c * 1.35)) for c in base)
                lit = shade(base, nrm, light, amb=0.38, gain=0.62)
                items.append((poly[:, 2].mean(), poly[:, :2], fog(lit, z, far=27), None))

    draw_scene(d, cam, items, light)
    return np.asarray(img, dtype=np.float32)


def encode(name, fn, seconds, ffmpeg):
    out = Path("/tmp") / name
    cmd = [ffmpeg, "-y", "-hide_banner", "-loglevel", "error", "-f", "rawvideo",
           "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
           "-movflags", "+faststart", str(out)]
    pr = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    n = int(seconds * FPS)
    rng = np.random.default_rng(3)
    for i in range(n):
        arr = fn(i / FPS, seconds)
        arr = arr + rng.normal(0, 1.8, (H, W, 1))
        pr.stdin.write(np.clip(arr, 0, 255).astype(np.uint8).tobytes())
    pr.stdin.close()
    pr.wait()
    print("  ", out, out.stat().st_size // 1024, "KB")
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--ffmpeg", required=True)
    a = ap.parse_args()
    o = encode("shot-office.mp4", shot_office, 4.0, a.ffmpeg)
    c = encode("shot-city.mp4", shot_data_city, 4.0, a.ffmpeg)
    Path("/tmp/proof_list.txt").write_text(f"file '{o}'\nfile '{c}'\n")
    subprocess.run([a.ffmpeg, "-y", "-hide_banner", "-loglevel", "error",
                    "-f", "concat", "-safe", "0", "-i", "/tmp/proof_list.txt",
                    "-c", "copy", "/tmp/proof-3d.mp4"], check=True)
    print("proof -> /tmp/proof-3d.mp4")
