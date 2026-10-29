#!/usr/bin/env python3
"""make_proof.py — shot uji "The Climb" (15 dtk, 1080p, TANPA teks).

Satu shot, satu aksi: siluet seseorang menaiki tangga menuju matahari.

Kenapa siluet: pada uji sebelumnya figur berwarna terang terbaca seperti
manekin karet — anatomi prosedural selalu kalah dari anatomi asli, tapi
SILUET tidak. Mata manusia membaca siluet sebagai manusia utuh, dan cahaya
tepi (rim light) memberi tahu dari mana matahari datang. Ini teknik yang
dipakai di film animasi 2D mahal, dan justru menyembunyikan titik lemah.

    python3 make_proof.py --ffmpeg "$FF" --out out/proof.mp4     # render penuh
    python3 make_proof.py --still 5.0 --out out/x.mp4             # satu frame
    python3 make_proof.py --sheet out/sheet.png                   # lembar kontak
"""
from __future__ import annotations

import argparse
import math
import multiprocessing as mpr
import os
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from motion import Climb

import cine
from cine import (H, INK, SS, SUN, W, Cam, Pen, Pose, clamp, draw_figure, lerp,
                  mix, place_feet, seg, smooth, sole_y)

FPS = 30
DUR = 12.0
NF = int(FPS * DUR)

# ------------------------------------------------------------------ dunia
X0, Y0 = -540.0, 300.0
TREAD, RISER = 172.0, 74.0
NSTEP = 6
HFIG = 500.0
STEP_SEC = 1.30
CLIMB_T0 = 1.10
SUN_W = (860.0, -350.0)
SUN_R = 118.0

SKY_STOPS = [(0.00, (7, 10, 20)), (0.20, (13, 18, 36)), (0.38, (28, 29, 52)),
             (0.55, (62, 44, 62)), (0.70, (108, 64, 68)), (0.84, (172, 100, 86)),
             (1.00, (223, 143, 104))]
HORIZON = (206, 137, 105)

C_RIDGE_FAR = (26, 26, 44)
C_RIDGE = (16, 18, 30)
C_TOWN = (26, 24, 40)
C_MID = (12, 16, 26)
C_STAIR = (10, 13, 20)
C_STAIR_TOP = (44, 40, 52)
C_STAIR_LIP = (226, 158, 116)
C_NEAR = (5, 6, 10)
FIG = (8, 8, 12)


def step_top(i):
    return (X0 + i * TREAD, Y0 - i * RISER)


def climb_u(t):
    return clamp((t - CLIMB_T0) / STEP_SEC, 0.0, NSTEP)


CLIP = None


def person_at(t):
    """Pose dari klip retargeting (IK + pijakan di tapak)."""
    u = climb_u(t)
    if u >= NSTEP:
        tt = t - (CLIMB_T0 + NSTEP * STEP_SEC)
        k = smooth(clamp((tt - 1.4) / 1.4))
        return CLIP.standing(NSTEP, t, raise_arm=k), CLIP.ankle_target(NSTEP)
    p = CLIP.pose(u, t)
    return p, (p.foot_l[0] if p.foot_l else 0.0, 0.0)


def foot_sole_of(pose):
    import cine as _c
    sk = _c.skeleton(pose)
    return [a[1] + _c.sole_offset(pose.h) for _, _, a in sk["legs"]]


SHOTS = [
    # (nama, t0, t1, zoom, target: 'body' | 'feet' | 'upper' | 'world')
    ("wide", 0.00, 4.20, 1.00, "world"),
    ("medium", 4.20, 8.30, 1.55, "body"),
    ("feet", 8.30, 10.10, 1.55, "feet"),
    ("upper", 10.10, 12.00, 1.42, "upper"),
]


def shot_of(t):
    for k, sh in enumerate(SHOTS):
        if sh[1] <= t < sh[2]:
            return k, sh
    return len(SHOTS) - 1, SHOTS[-1]


def targets(t):
    """Titik yang dibidik kamera untuk detik t."""
    pose, _ = person_at(t)
    sk = cine.skeleton(pose)
    idx, sh = shot_of(t)
    kind = sh[4]
    if kind == "feet":
        a, b = [a for _, _, a in sk["legs"]]
        return (a[0] + b[0]) * 0.5, max(a[1], b[1]) - 110
    if kind == "upper":
        return sk["head"][0] - 40, sk["head"][1] + 250
    if kind == "body":
        return pose.x + 40, pose.y - 200
    return pose.x + 300, pose.y - 250


# --------------------------------------------------------------- langit
def make_sky(cam: Cam, t):
    img = cine.sky_gradient(SKY_STOPS)
    tf = cam.tf(0.00)
    sx, sy = tf.p(*SUN_W)
    sx, sy = sx / SS, sy / SS
    r = SUN_R * tf.sc

    # bintang: hanya di bagian gelap
    rng = np.random.default_rng(5)
    for k in range(150):
        bx, by = rng.uniform(0, W), rng.uniform(0, H * 0.42)
        edge = 1.0 - by / (H * 0.42)
        tw = 0.55 + 0.45 * math.sin(t * 1.7 + k * 3.1)
        a = edge ** 1.3 * tw * 0.9
        if a < 0.04:
            continue
        rr = 0.8 + rng.random() * 1.1
        img[int(by) - 2:int(by) + 3, int(bx) - 2:int(bx) + 3] += a * 150 * np.array([0.85, 0.9, 1.0], np.float32)

    # halo bertingkat (jadi bloom saat compositing)
    for k, a in ((5.2, 0.16), (3.1, 0.24), (1.85, 0.44)):
        img = img + cine.radial((W, H), sx, sy, r * k, (255, 198, 156), power=2.1, scale=3) * a
    disc = cine.radial((W, H), sx, sy, r * 1.0, (255, 196, 140), power=0.10, scale=2)
    img = img + disc * 0.55
    core = cine.radial((W, H), sx, sy, r * 0.74, (255, 244, 222), power=0.35, scale=2)
    img = img + core * 1.00

    # berkas cahaya ke bawah-kiri (menuju tangga)
    sh = Image.new("L", (W // 4, H // 4), 0)
    d = ImageDraw.Draw(sh)
    for ang, wid, a in ((96, 150, 26), (112, 240, 18), (82, 96, 22),
                        (130, 320, 13), (150, 210, 10)):
        rad = math.radians(ang - 90)          # 0 = ke bawah
        px, py = sx / 4, sy / 4
        L = 1600
        nx, ny = -math.sin(rad), math.cos(rad)
        d.polygon([(px, py),
                   (px + nx * L / 4 + math.cos(rad) * wid / 8,
                    py + ny * L / 4 + math.sin(rad) * wid / 8),
                   (px + nx * L / 4 - math.cos(rad) * wid / 8,
                    py + ny * L / 4 - math.sin(rad) * wid / 8)], fill=a)
    sh = sh.filter(ImageFilter.GaussianBlur(11)).resize((W, H), Image.BILINEAR)
    rays = np.asarray(sh, np.float32)[:, :, None] / 255.0
    img = img + rays * np.array([255, 202, 158], np.float32) * 0.55
    return img


def birds(cam, t):
    pen = Pen(cam.tf(0.05))
    for k, (bx, by, sp, sz) in enumerate(((-560, -470, 8.5, 8), (-470, -510, 10, 6),
                                          (-650, -430, 7.5, 5))):
        x = bx + sp * t
        y = by + math.sin(t * 0.9 + k) * 5
        flap = math.sin(t * 5.0 + k * 1.7)
        pen.line([(x - sz, y - sz * 0.5 * flap), (x, y),
                  (x + sz, y - sz * 0.5 * flap)], (16, 17, 28, 220), 1.5)
    return pen, 0.0, 0.45


def layer_ridge(cam):
    pen = Pen(cam.tf(0.05))
    rng = np.random.default_rng(7)
    for band, (yo, amp, col, haze) in enumerate((
            (135, 120, C_RIDGE_FAR, 0.40), (250, 80, C_RIDGE, 0.24))):
        hi = mix(col, HORIZON, haze)
        pts = [(-1700, 780)]
        x = -1700.0
        while x < 1800:
            x += 110 + rng.random() * 120
            pts.append((x, yo + math.sin(x * 0.0040 + band * 2.1) * amp
                        + (rng.random() - 0.5) * 40))
        pts += [(1800, 780)]
        pen.poly(pts, hi)
    return pen, 0.8, 0.0


def layer_town(cam, t):
    """Kota jauh: rendah, jarang, tenggelam kabut. Bukan deret barcode."""
    pen = Pen(cam.tf(0.19))
    rng = np.random.default_rng(21)
    base = 330.0
    x = -1750.0
    while x < 1750:
        w = 26 + rng.random() * 52
        hgt = 22 + rng.random() ** 2.6 * 150
        pen.rect(x, base - hgt, w, hgt + 480, C_TOWN)
        x += w + 26 + rng.random() * 90
    for k in range(150):
        wx = rng.uniform(-1750, 1750)
        wy = rng.uniform(base - 200, base + 90)
        if rng.random() < 0.6:
            continue
        fl = 0.4 + 0.6 * math.sin(t * 0.55 + k * 2.3)
        pen.ellipse(wx, wy, 1.6, 2.1, (240, 184, 128, int(16 + 44 * fl)))
    return pen, 0.0, 0.46


def layer_mid(cam):
    """Daratan gelap yang rendah + tebing kanan. Tidak ada bidang terang besar:
    bagian bawah frame harus tetap gelap supaya tangga dan figur menonjol."""
    pen = Pen(cam.tf(0.40))
    col = mix(C_MID, HORIZON, 0.16)
    pen.poly([(-1800, 470), (-400, 452), (300, 486), (900, 470), (1800, 500),
              (1800, 1000), (-1800, 1000)], col)
    pen.poly([(1150, 1000), (1800, 1000), (1800, -260), (1580, -230),
              (1440, 140), (1340, 580)], col)
    return pen, 0.0, 0.22


def layer_stairs(cam, t, pose, feet):
    """Tangga sebagai satu pita bersambung. Ekornya melarut ke kabut, jadi
    tidak ada massa besar dan tidak ada anak tangga yang terlepas.
    """
    pen = Pen(cam.tf(0.60, ss=2))
    TH = 54.0
    ax, ay = X0 + NSTEP * TREAD, Y0 - NSTEP * RISER
    plat_w = 520.0

    # profil atas: zigzag tapak-tanjakan
    prof = [(X0 - 60, Y0 + 34), (X0 - 60, Y0)]
    for i in range(NSTEP):
        x = X0 + i * TREAD
        y = Y0 - i * RISER
        prof.append((x + TREAD, y))
        prof.append((x + TREAD, y - RISER))
    prof.append((ax + plat_w, ay))
    prof += [(ax + plat_w, ay + TH), (X0 - 60, Y0 + TH + 34)]
    pen.poly(prof, C_STAIR)

    # tapak: garis hangat; tanjakan: muka lebih terang sedikit
    for i in range(NSTEP):
        x, y = X0 + i * TREAD, Y0 - i * RISER
        pen.rect(x, y - 7, TREAD, 7, C_STAIR_TOP)
        pen.rect(x, y - 8.2, TREAD, 1.6, C_STAIR_LIP)
        pen.rect(x + 1, y, TREAD - 2, RISER - 7, mix(C_STAIR, (40, 36, 48), 0.45))
        pen.rect(x + TREAD - 1.4, y - RISER, 1.4, RISER - 7,
                 mix(C_STAIR, (58, 48, 54), 0.6))
    pen.rect(ax, ay - 7, plat_w, 7, C_STAIR_TOP)
    pen.rect(ax, ay - 8.2, plat_w, 1.6, C_STAIR_LIP)
    pen.rect(ax, ay, plat_w, TH, C_STAIR)

    # ekor pita melarut: sapuan warna horizon makin jauh makin kuat
    n_haze = 26
    for k in range(n_haze):
        q = (k + 1) / n_haze
        y0 = Y0 - q * 190 + TH * 0.4
        a = int(150 * q ** 1.5)
        pen.rect(X0 - 260 - q * 260, y0 + 10, 240, TH + 40, (*HORIZON, a))

    for f in (pose.foot_l, pose.foot_r):
        if f is not None:
            pen.soft_shadow(f[0] + 8, f[1] + 22, 34, 6, alpha=0.75)
    draw_figure(pen, pose, far_mul=1.0)
    return pen, 2.2, 0.02


def motes(cam, t):
    pen = Pen(cam.tf(0.70))
    rng = np.random.default_rng(11)
    for k in range(70):
        bx = rng.uniform(-1500, 1500)
        by = rng.uniform(-800, 760)
        sp = 9 + rng.random() * 22
        x = bx + math.sin(t * 0.35 + k) * 32
        y = by - (t * sp) % 1700 + 850
        a = 0.10 + 0.40 * rng.random()
        pen.circle(x, y, 1.4 + rng.random() * 1.8, (255, 232, 200, int(255 * a)))
    return pen, 5.0, 0.0


def layer_near(cam, t):
    """Bebatuan depan bawah: memberi bingkai dan skala."""
    pen = Pen(cam.tf(0.82))
    rng = np.random.default_rng(3)
    for k in range(7):
        bx = -1900 + k * 620 + rng.random() * 180
        bw = 320 + rng.random() * 300
        bh = 170 + rng.random() * 190
        pen.poly([(bx, 1000), (bx + bw * 0.16, 1000 - bh),
                  (bx + bw, 1000 - bh * 0.66), (bx + bw * 1.18, 1000)], C_NEAR)
    return pen, 7.0, 0.0


def layer_fg(cam, t):
    pen = Pen(cam.tf(1.0))
    sway = math.sin(t * 0.5) * 10
    # bingkai bawah
    pen.poly([(-2000, 1200), (-2000, 880 + sway), (-1300, 842), (-600, 900),
              (200, 856 + sway), (1100, 892), (1800, 858), (2000, 900),
              (2000, 1200)], C_NEAR)
    # bongkahan lewat di depan pada menit ke-7..11 (parallax paling kuat)
    if 6.0 < t < 11.5:
        q = seg(t, 6.0, 11.5)
        bx = lerp(2100, -900, q)
        by = lerp(980, 900, q)
        pen.poly([(bx, by + 400), (bx + 90, by - 60), (bx + 300, by - 130),
                  (bx + 470, by + 60), (bx + 430, by + 400)], C_NEAR)
    return pen, 14.0, 0.0


# --------------------------------------------------------------------- frame
def frame(i):
    t = i / FPS
    cam = CAM[i]
    pose, feet = person_at(t)

    out = make_sky(cam, t).astype(np.float32)
    passes = (
        ("ridge", lambda: layer_ridge(cam)),
        ("birds", lambda: birds(cam, t)),
        ("mid", lambda: layer_mid(cam)),
        ("stairs", lambda: layer_stairs(cam, t, pose, feet)),
        ("motes", lambda: motes(cam, t)),
        ("near", lambda: layer_near(cam, t)),
        ("fg", lambda: layer_fg(cam, t)),
    )
    for name, fn in passes:
        pen, dof, haze = fn()
        a = cine.down(np.asarray(pen.img))
        if pen.tf.ss == 1 and a[:, :, 3].max() > 0:
            # tepi tanpa supersample dihaluskan 1px: cukup, dan 4x lebih murah
            a[:, :, 3] = cine.blur_img(a[:, :, 3:4].repeat(3, 2), 0.7)[:, :, 0]
        if dof > 0.4:
            dz = dof * (cam.z ** 1.6 if name != "stairs" else 1.0)
            a[:, :, :3] = cine.blur_img(a[:, :, :3], dz)
            a[:, :, 3] = cine.blur_img(a[:, :, 3:4].repeat(3, 2), dz)[:, :, 0]
        if haze > 0:
            hc = np.array(HORIZON, np.float32)[None, None, :]
            a[:, :, :3] = a[:, :, :3] * (1 - haze) + hc * haze
        if name in ("stairs", "near", "fg"):
            # bayangan antar-lapis: potongan kertas menumpuk di ruang nyata
            sh = cine.drop_shadow(a, dx=8, dy=13, blur=10, alpha=0.55)
            out = out * (1 - sh * np.clip(a[:, :, 3:4] / 255.0 + 0.55, 0, 1))
            a = cine.rim_light(a, SUN, dx=4.0, dy=4.0,
                               strength=0.95 / (1 + 0.5 * max(0.0, cam.z - 1.4)),
                               width=1.1)
        out = cine.over(out, a)

    out = cine.bloom(out, thresh=0.72, strength=0.40, radius=30)
    out = cine.chroma(out, 0.0009)
    out = cine.grade(out, i, exposure=1.05)
    fade = min(1.0, seg(t, 0.0, 0.9), 1.0 - seg(t, 11.1, 12.0))
    out = out * fade
    return (np.clip(out, 0, 1) * 255).astype(np.uint8)


def build_camera():
    cams = []
    cx = cy = None
    for i in range(NF):
        t = i / FPS
        tx, ty = targets(t)
        idx, sh = shot_of(t)
        z = sh[3]
        if cx is None:
            cx, cy = tx, ty
        else:
            # tiap shot punya pergerakan kamera sendiri: pelan, tidak seragam
            span = max(0.1, sh[2] - sh[1])
            k = 1 - math.exp(-1.0 / (0.55 * FPS))
            cx += (tx - cx) * k
            cy += (ty - cy) * k
        # dorongan halus di dalam shot (bukan zoom yang sama tiap shot)
        prog = clamp((t - sh[1]) / max(0.1, sh[2] - sh[1]))
        zz = z * (1.0 + (0.045 if idx % 2 == 0 else -0.035) * smooth(prog))
        cams.append(Cam(cx, cy, zz))
    return cams


CAM = None


def _init():
    global CAM
    CAM = build_camera()


def _work(i):
    return i, frame(i).tobytes()


def main():
    global CAM
    ap = argparse.ArgumentParser()
    ap.add_argument("--ffmpeg", default="ffmpeg")
    ap.add_argument("--out", default="out/proof.mp4")
    ap.add_argument("--still", type=float, default=None)
    ap.add_argument("--sheet", default=None)
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--qc", action="store_true", help="ukur galat pijakan + uji retargeting")
    a = ap.parse_args()

    global CLIP
    CLIP = Climb(X0, Y0, TREAD, RISER, NSTEP, HFIG)
    CAM = build_camera()

    if a.qc:
        worst = 0.0
        for k in range(0, int(DUR * FPS), 3):
            tt = k / FPS
            u = climb_u(tt)
            if u >= NSTEP:
                continue
            i = int(u)
            soles = foot_sole_of(CLIP.pose(u, tt))
            surf = CLIP.surface_y(i)
            err = min(abs(s_ - surf) for s_ in soles)      # kaki penopang terdekat
            worst = max(worst, err)
        print(f"QC pijakan: galat maksimum kaki penopang vs permukaan = {worst:.2f} px")
        # bukti retargeting: ubah geometri tangga, cek ulang
        for tread, riser, h in ((120, 62, 430), (172, 74, 500), (240, 96, 560)):
            c = Climb(-540, 250, tread, riser, 6, h)
            w = 0.0
            for k in range(1200):
                u = k / 200
                if u >= 6:
                    break
                soles = foot_sole_of(c.pose(u, k / 60))
                w = max(w, min(abs(s_ - c.surface_y(int(u))) for s_ in soles))
            print(f"  tangga {tread}x{riser}, figur {h}px → galat {w:.2f} px")
        return

    if a.sheet:
        times = [0.8, 2.6, 4.4, 6.6, 9.4, 12.8]
        tw, th = 640, 360
        sheet = Image.new("RGB", (tw * 3, th * 2), (0, 0, 0))
        for k, tt in enumerate(times):
            im = Image.fromarray(frame(min(NF - 1, int(tt * FPS))))
            sheet.paste(im.resize((tw, th), Image.LANCZOS), ((k % 3) * tw, (k // 3) * th))
        sheet.save(a.sheet)
        print("sheet →", a.sheet)
        return

    if a.still is not None:
        png = Path(a.out).with_suffix(".png")
        png.parent.mkdir(parents=True, exist_ok=True)
        Image.fromarray(frame(int(a.still * FPS))).save(png)
        print("still →", png)
        return

    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    cmd = [a.ffmpeg, "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-c:v", "libx264", "-preset", "slow", "-crf", "17",
           "-pix_fmt", "yuv420p", str(out)]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL)
    with mpr.Pool(a.workers, initializer=_init) as pool:
        for k, (i, buf) in enumerate(pool.imap(_work, range(NF), chunksize=4)):
            p.stdin.write(buf)
            if k % 60 == 0:
                print(f"  {i}/{NF}", flush=True)
    p.stdin.close()
    p.wait()
    print("selesai →", out)


if __name__ == "__main__":
    main()
