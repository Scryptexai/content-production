#!/usr/bin/env python3
"""Adegan animasi 2D untuk video RW1 (Peter Principle).

Tiap adegan bercerita dengan gambar bergerak: karakter berjalan, memanjat
tangga, tim yang merosot, kolom data yang tumbuh. Teks sengaja sangat sedikit
— hanya penanda kecil — karena yang diminta adalah visual, bukan slide.

    python3 make_anim.py --out remotion/public/anim --proof
    python3 make_anim.py --out remotion/public/anim --ffmpeg <ffmpeg>
"""
import argparse
import math
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from anim2d import (W, H, CREAM, ROSE, SAGE, LILAC, MUTED, INK, clothes,
                    Canvas, Pose, draw_person, walk_pose, idle_pose, point_pose,
                    slump_pose, climb_pose, carry_pose, seg, ease_in_out, ease_out,
                    lerp, fog, clamp)

ROOT = Path(__file__).parent
FONT_S = ROOT / "remotion" / "public" / "fonts" / "IBMPlexMono-Regular.ttf"
FONT_SER = ROOT / "remotion" / "public" / "fonts" / "InstrumentSerif-Regular.ttf"
GROUND = 470.0


# ------------------------------------------------------------------ properti
def backdrop(c: Canvas, tint=(14, 19, 29), arches=True):
    """Latar: gradien + deret lengkung jendela jauh + kabut lantai.

    Bagian atas frame tidak boleh kosong — itu yang membuat video terasa
    seperti slide.
    """
    c.d.rectangle([0, 0, W * 2, H * 2], fill=tint)
    for i in range(12):
        k = i / 11
        y0 = k * H
        col = tuple(int(INK[j] * (1 - k) + tint[j] * k) for j in range(3))
        c.d.rectangle([0, y0 * 2, W * 2, (y0 + H / 11 + 1) * 2], fill=col)
    if arches:
        # deret kolom berpilar: memberi kedalaman tanpa mengganggu subjek
        for i in range(9):
            x = -40 + i * 122
            c.rect(x, 84, 26, 296, fill=(21, 27, 39))
            c.rect(x + 3, 84, 6, 296, fill=(30, 38, 54))
            c.glow(x + 13, 150, 40, (22, 30, 46), 0.5)
        # balok atas (langit-langit)
        c.rect(-400, 60, 1800, 26, fill=(17, 22, 32))
    # kabut lantai
    for i in range(6):
        c.rect(-400, 392 + i * 12, 1800, 12, fill=(16, 21, 31), radius=0)


def floor(c: Canvas, y=GROUND, depth=0.0, col=(30, 37, 50), line=True):
    c.rect(-400, y, 1700, 400, fill=fog(col, depth))
    if line:
        c.line([(-400, y), (1300, y)], fill=fog((70, 82, 102), depth), width=1.6)


def desk(c: Canvas, x, y, w=46, s=1.0, depth=0.0, screen=True, shake=0.0):
    col = fog((46, 56, 74), depth)
    c.rect(x, y - 26 * s, w * s, 4 * s, fill=col)
    c.rect(x + 3 * s, y - 24 * s, 3 * s, 24 * s, fill=fog((34, 42, 58), depth))
    c.rect(x + w * s - 6 * s, y - 24 * s, 3 * s, 24 * s, fill=fog((34, 42, 58), depth))
    if screen:
        sx = x + w * s * 0.18
        c.rect(sx, y - 46 * s, 20 * s, 14 * s, fill=fog((88, 118, 165), depth))
        c.rect(sx + 8 * s, y - 32 * s, 3 * s, 6 * s, fill=fog((46, 56, 74), depth))
        c.glow(sx + 10 * s, y - 39 * s, 16 * s, (26, 40, 64), 0.5)


def bar(c: Canvas, x, y, w, h, col, depth=0.0, glow=False):
    if h <= 0.5:
        return
    c.rect(x, y - h, w, h, fill=fog(col, depth), radius=min(3.0, w / 2))
    if glow:
        c.glow(x + w / 2, y - h / 2, 26, tuple(int(v * 0.5) for v in col), 0.5)


def stairs(c: Canvas, x0, y0, n, sw=64, sh=40, depth=0.0,
           col=(44, 53, 70), edge=(92, 104, 126)):
    for i in range(n):
        c.rect(x0 + i * sw, y0 - sh * (i + 1), sw, sh * (i + 1), fill=fog(col, depth))
        c.line([(x0 + i * sw, y0 - sh * (i + 1)), (x0 + (i + 1) * sw, y0 - sh * (i + 1))],
               fill=fog(edge, depth), width=1.5)


def partition(c: Canvas, x, y, h=120, depth=0.0):
    c.rect(x, y - h, 5, h, fill=fog((40, 48, 64), depth))


def brace(c: Canvas, x0, x1, y, depth=0.0, col=(120, 132, 152)):
    """Kurung pengukur antara dua titik."""
    c.line([(x0, y), (x1, y)], fill=fog(col, depth), width=2)
    for x in (x0, x1):
        c.line([(x, y - 7), (x, y + 7)], fill=fog(col, depth), width=2)


def particle(c: Canvas, x, y, a, col=(150, 170, 210)):
    if a <= 0.02:
        return
    c.circle(x, y, 1.2, fill=tuple(int(v * a) for v in col))


# ------------------------------------------------------------------ adegan
def s1_hall(t, dur):
    """Lorong penjualan: puluhan meja, kamera mundur, satu orang disorot."""
    c = Canvas(); c.begin(); backdrop(c)
    p = seg(t, 0, dur)
    c.cam(zoom=1.34 - 0.42 * ease_out(p), ox=-96 + 96 * ease_out(p), oy=-18)

    rows = [(GROUND, 1.0, 0.0), (GROUND - 66, 0.62, 0.52), (GROUND - 104, 0.44, 0.78)]
    for ry, s, dep in reversed(rows):
        floor(c, ry + 8, depth=dep, line=True)
        for i in range(-2, 11):
            x = -140 + i * 108 + (0 if s > 0.8 else 26)
            desk(c, x, ry, w=54, s=s / 1.0, depth=dep)
            # pekerja duduk di belakang meja
            bob = math.sin(t * 1.4 + i * 0.9) * 1.2 * s
            pose = idle_pose(t + i * 0.7, x + 20 * s, ry - 4 + bob, scale=s * 0.52, breathe=0.6)
            pose.arm_l, pose.arm_r = 52, -46
            pose.elbow_l, pose.elbow_r = -28, -26
            draw_person(c, pose, clothes(i + 2), depth=dep)

    # satu orang utama: berdiri, menunjuk papan
    main = point_pose(t, 592, GROUND - 2, reach=seg(t, dur * 0.45, dur * 0.72), scale=1.06)
    c.glow(main.x, main.y - 50, 60, (34, 44, 66), 0.8)
    draw_person(c, main, CREAM, depth=0.0)

    # papan angka di kanan
    bh = 96 * seg(t, dur * 0.55, dur * 0.9)
    bar(c, 700, GROUND - 4, 26, bh, ROSE, glow=True)
    bar(c, 736, GROUND - 4, 26, bh * 0.62, SAGE)
    bar(c, 772, GROUND - 4, 26, bh * 0.38, (110, 120, 140))

    for i in range(26):
        particle(c, (i * 137 + t * 12) % 960, 60 + (i * 71) % 320, 0.10)
    return c


def s2_measure(t, dur):
    """Dua kelompok (sebelum/sesudah) dan garis ukur di antaranya."""
    c = Canvas(); c.begin(); backdrop(c)
    c.cam(zoom=1.06, ox=0, oy=6)
    floor(c)

    # tim kiri: 3 orang berdiri
    for i, x in enumerate((116, 168, 220)):
        pose = idle_pose(t + i * 0.5, x, GROUND - 2, scale=0.92)
        draw_person(c, pose, fog(clothes(i), 0.12), depth=0.12)
    labels_y = GROUND - 108
    c.line([(96, labels_y), (250, labels_y)], fill=fog((90, 100, 120), 0.1), width=1.2)

    # panah di tengah
    ax0, ax1 = 292, 388
    prog = seg(t, dur * 0.18, dur * 0.5)
    xe = lerp(ax0, ax1, prog)
    c.line([(ax0, GROUND - 46), (xe, GROUND - 46)], fill=ROSE, width=3)
    if prog > 0.05:
        c.poly([(xe, GROUND - 46), (xe - 12, GROUND - 52), (xe - 12, GROUND - 40)], fill=ROSE)

    # tim kanan
    for i, x in enumerate((430, 482, 534)):
        pose = idle_pose(t * 1.1 + i * 0.5, x, GROUND - 2, scale=0.92)
        draw_person(c, pose, clothes(i + 3), depth=0.0)

    # kurung pengukur + angka garis (tanpa teks besar)
    brace(c, 96, 250, GROUND - 128)
    brace(c, 410, 560, GROUND - 128)

    # grafik garis yang tumbuh di kanan atas
    gx, gy = 620, GROUND - 168
    c.line([(gx, gy), (gx, gy + 150), (gx + 250, gy + 150)], fill=fog((80, 92, 112), 0.1), width=1.5)
    pts = []
    for i in range(41):
        u = i / 40
        xx = gx + 10 + u * 236
        yy = gy + 150 - (150 * (0.18 + 0.78 * u ** 1.7)) * seg(t, dur * 0.2 + u * dur * 0.35, dur * 0.2 + u * dur * 0.35 + 0.3)
        pts.append((xx, yy))
    if len(pts) > 1:
        c.line(pts, fill=SAGE, width=3)
        c.circle(pts[-1][0], pts[-1][1], 4, fill=CREAM)
        c.glow(pts[-1][0], pts[-1][1], 26, (40, 60, 46), 0.7)

    # kolom di depan sebagai ritme
    for i in range(9):
        h = 22 + 58 * abs(math.sin(i * 0.8 + 0.4)) * seg(t, dur * 0.1 + i * 0.08, dur * 0.5 + i * 0.08)
        bar(c, 640 + i * 30, GROUND + 40, 16, h, (72, 84, 104), depth=0.35)
    return c


def s3_sales(t, dur):
    """Penjualan berlipat dua → satu langkah naik."""
    c = Canvas(); c.begin(); backdrop(c)
    c.cam(zoom=1.1, ox=-30, oy=8)
    floor(c)
    stairs(c, 470, GROUND, 4, sw=76, sh=44, depth=0.0)

    # penjual di depan meja
    x = 176
    desk(c, x - 30, GROUND - 2, w=64, screen=True)
    pose = idle_pose(t, x + 6, GROUND - 2, scale=1.0)
    # lambaikan tangan saat angka naik
    wave = seg(t, dur * 0.34, dur * 0.5)
    pose.arm_r = -10 - 96 * wave
    pose.elbow_r = 10 + 18 * math.sin(t * 7) * wave
    draw_person(c, pose, CREAM)

    # kolom penjualan berlipat dua
    grow = seg(t, dur * 0.22, dur * 0.42)
    h1 = 52 * (1 + grow)
    bar(c, 92, GROUND - 4, 26, h1, ROSE, glow=True)
    # penanda "dua kali": garis putus-putus setinggi puncak lama
    c.line([(84, GROUND - 4 - 52), (128, GROUND - 4 - 52)],
           fill=fog((150, 160, 180), 0.1), width=1.2)

    # panah naik ke tangga
    up = seg(t, dur * 0.52, dur * 0.72)
    if up > 0.02:
        ax, ay = lerp(236, 500, up), lerp(GROUND - 96, GROUND - 62, up)
        c.line([(236, GROUND - 96), (ax, ay)], fill=ROSE, width=2.4)
        c.circle(ax, ay, 3.4, fill=ROSE)
        c.glow(ax, ay, 22, (40, 22, 18), 0.7)

    # orang yang dipromosikan naik satu tingkat
    if t > dur * 0.62:
        u = seg(t, dur * 0.62, dur * 0.9)
        step = ease_in_out(u)
        nx = lerp(300, 470 + 38, step)
        ny = GROUND - 44 * step
        walk = walk_pose(t * 7, nx, ny, 1.0, 1.0)
        if step > 0.95:
            walk = idle_pose(t, nx, ny, 1.0)
        draw_person(c, walk, CREAM)
    return c


def s4_team_drop(t, dur):
    """Manajer baru di depan; penjualan timnya justru turun."""
    c = Canvas(); c.begin(); backdrop(c)
    c.cam(zoom=1.12, ox=-40, oy=10)
    floor(c)
    stairs(c, 560, GROUND, 3, sw=80, sh=46)

    # manajer di tingkat atas
    boss = idle_pose(t, 640, GROUND - 92, scale=1.0, breathe=0.8)
    boss.spine = 2 + 3 * seg(t, dur * 0.45, dur * 0.75)
    draw_person(c, boss, CREAM)
    c.glow(640, GROUND - 130, 46, (30, 38, 56), 0.6)

    # tim di bawah: makin lama makin terkulai
    drop = seg(t, dur * 0.35, dur * 0.85)
    for i, x in enumerate((150, 232, 314)):
        pose = slump_pose(t + i * 0.4, x, GROUND - 2, amount=drop, scale=0.94)
        draw_person(c, pose, fog(clothes(i), 0.1), depth=0.1)

    # kolom tim menyusut
    for i, x in enumerate((150, 232, 314)):
        h = lerp(78, 34, drop) * (0.82 + 0.18 * math.sin(i))
        bar(c, x - 46, GROUND - 4, 20, h, ROSE if i == 0 else (96, 106, 126), depth=0.2)

    # garis turun di kanan
    gx, gy = 760, 250
    c.line([(gx, gy), (gx, gy + 160), (gx + 160, gy + 160)], fill=fog((70, 80, 98), 0.2), width=1.4)
    pts = [(gx + 8 + u * 146, gy + 150 - (150 * (1 - 0.45 * u * drop)) * (1 - u * 0.0) )
           for u in [i / 24 for i in range(25)]]
    c.line([(px, py - 92 * (1 - i / 24) * 0) for i, (px, py) in enumerate(pts)],
           fill=fog((60, 70, 88), 0.2), width=1)
    line2 = [(gx + 8 + u * 146, gy + 40 + (110 * u * drop * 0.9)) for u in [i / 24 for i in range(25)]]
    c.line(line2, fill=ROSE, width=3)
    return c


def s5_cross_team(t, dur):
    """Satu orang berjalan menembus tiga tim; jejaknya menyala."""
    c = Canvas(); c.begin(); backdrop(c)
    cam = 1.04 + 0.03 * math.sin(t * 0.3)
    c.cam(zoom=cam, ox=0, oy=8)
    floor(c)
    for i, x in enumerate((250, 500, 750)):
        partition(c, x, GROUND, h=130)
        for j, dx in enumerate((-108, -54, 12)):
            pose = idle_pose(t + i + j, x + dx, GROUND - 2, scale=0.78)
            draw_person(c, pose, fog(clothes(i * 2 + j), 0.34), depth=0.34)

    # pejalan
    p = seg(t, 0.06, 0.94)
    x = lerp(70, 900, ease_in_out(p))
    walking = walk_pose(x * 0.052, x, GROUND - 2, 1.0, 1.05)
    draw_person(c, walking, CREAM)

    # jejak menyala
    for i in range(30):
        tx = lerp(70, x, i / 30)
        if tx > x - 4:
            continue
        a = 0.42 * (i / 30) ** 1.6
        c.circle(tx, GROUND - 1, 3.2, fill=tuple(int(ROSE[j] * a + INK[j] * (1 - a)) for j in range(3)))
        if i % 6 == 0:
            c.glow(tx, GROUND - 6, 14, (40, 24, 20), 0.5 * a)
    return c


def s6_towers(t, dur):
    """Dua jalur karier: kiri dari penjualan, kanan dari kompetensi."""
    c = Canvas(); c.begin(); backdrop(c)
    c.cam(zoom=1.0 + 0.05 * seg(t, 0, dur), ox=0, oy=14)
    floor(c)

    # menara kiri: dari penjualan → berhenti di tengah
    bx = 150
    left_n = 4
    for i in range(left_n):
        c.rect(bx, GROUND - 52 * (i + 1), 92, 52 * (i + 1), fill=fog((46, 55, 72), 0.12))
    # menara kanan: lebih tinggi, tiap tingkat ada orang yang bekerja
    rx = 560
    right_n = int(lerp(1, 7, seg(t, dur * 0.1, dur * 0.85)))
    for i in range(7):
        if i < right_n:
            c.rect(rx, GROUND - 52 * (i + 1), 92, 52 * (i + 1), fill=fog((52, 64, 78), 0.04))
            c.line([(rx, GROUND - 52 * (i + 1)), (rx + 92, GROUND - 52 * (i + 1))],
                   fill=SAGE, width=1.6)

    # figur di puncak masing-masing menara
    ly = GROUND - 52 * left_n
    pose = slump_pose(t, bx + 30, ly - 2, amount=0.55, scale=0.72)
    draw_person(c, pose, fog(CREAM, 0.18), depth=0.18)

    if right_n > 0:
        ry = GROUND - 52 * right_n
        top = idle_pose(t, rx + 30, ry - 2, scale=0.72)
        top.arm_r = -70 + 8 * math.sin(t * 2.2)
        draw_person(c, top, CREAM)
        c.glow(rx + 46, ry - 40, 40, (30, 44, 34), 0.7)

    # garis dasar & tanda +30% sebagai bentuk (bukan teks)
    c.line([(120, GROUND + 6), (700, GROUND + 6)], fill=fog((70, 80, 98), 0.2), width=1.2)
    return c


def s7_reward(t, dur):
    """Memanjat tangga untuk hadiah; yang di bawah menonton."""
    c = Canvas(); c.begin(); backdrop(c)
    c.cam(zoom=1.06, ox=-20, oy=6)
    floor(c)
    n = 6
    stairs(c, 330, GROUND, n, sw=72, sh=40, col=(44, 53, 70), edge=(96, 108, 130))

    # hadiah bercahaya di puncak
    tx = 330 + (n - 1) * 72 + 36
    ty = GROUND - n * 40 - 26
    pulse = 0.7 + 0.3 * math.sin(t * 2.4)
    c.glow(tx, ty, 44 * pulse, (60, 40, 30), 0.9)
    c.rect(tx - 11, ty - 11, 22, 22, fill=ROSE, radius=3)
    c.line([(tx, ty - 11), (tx, ty + 11)], fill=(250, 235, 225), width=1.6)

    # pemanjat
    prog = seg(t, dur * 0.06, dur * 0.82)
    step_f = prog * (n - 1)
    idx = int(step_f)
    frac = step_f - idx
    x = 330 + (idx + frac) * 72 + 20
    y = GROUND - (idx + (1 if frac > 0.5 else 0)) * 40 - 2
    pose = climb_pose(t * 8, x, y, 0.82)
    draw_person(c, pose, CREAM)

    # penonton di bawah
    for i, oy in enumerate((0, 26)):
        for x2 in (-60 + oy, 20 + oy, 90 + oy, 160 + oy, 230 + oy):
            look = idle_pose(t + i + x2 * 0.01, x2, GROUND + oy * 0.4 - 2, scale=0.62 - oy * 0.002)
            look.spine = -6
            look.head = -10
            draw_person(c, look, fog(CREAM, 0.42), depth=0.42)
    return c


def s8_peter(t, dur):
    """Tangga panjang naik keluar layar: berhenti di satu tingkat."""
    c = Canvas(); c.begin(); backdrop(c)
    c.cam(zoom=1.02, ox=30 - 30 * seg(t, 0, dur), oy=24)
    floor(c, GROUND + 20)
    n = 11
    stairs(c, -120, GROUND + 20, n, sw=88, sh=42, col=(40, 48, 64), edge=(90, 102, 124))

    # orang naik lalu berhenti
    stop = 6
    prog = seg(t, dur * 0.05, dur * 0.62)
    step_f = min(prog * stop, stop)
    idx = int(step_f)
    frac = step_f - idx
    moving = step_f < stop - 0.01
    x = -120 + (idx + frac) * 88 + 26
    y = GROUND + 20 - (idx + (1 if frac > 0.5 else 0)) * 42 - 2
    pose = climb_pose(t * 7, x, y, 0.8) if moving else idle_pose(t, x, y, 0.8, 0.8)
    if not moving:
        pose.spine = 4
        pose.head = 8
    draw_person(c, pose, CREAM)

    # yang lain sudah berhenti di berbagai tingkat (statis, diam)
    for i, (sx, sy) in enumerate(((300, 3), (620, 5), (820, 8))):
        px = -120 + sx + 26
        py = GROUND + 20 - sy * 42 - 2
        idle = idle_pose(t * 0.6 + i, px, py, 0.76, 0.35)
        idle.head = 6
        draw_person(c, idle, fog(CREAM, 0.3), depth=0.3)

    # debu waktu
    for i in range(20):
        particle(c, (i * 211 + t * 8) % 960, 120 + (i * 97) % 300, 0.08)
    return c


def s9_bounds(t, dur):
    """Dunia ini ada di dalam satu bingkai; di luarnya tidak terukur."""
    c = Canvas(); c.begin(); backdrop(c)
    z = 1.28 - 0.30 * seg(t, 0, dur * 0.9)
    c.cam(zoom=z, ox=0, oy=0)
    floor(c)

    # isi bingkai
    for i, x in enumerate((300, 380, 460, 540, 620)):
        pose = idle_pose(t + i * 0.4, x, GROUND - 2, scale=0.86)
        draw_person(c, pose, clothes(i))

    # bingkai data
    if t > dur * 0.25:
        f = seg(t, dur * 0.25, dur * 0.55)
        pad = lerp(160, 18, f)
        c.rect(250 - pad, 150 - pad * 0.4, 430 + pad * 2, 330 + pad * 0.8,
               fill=None, outline=LILAC, width=2)
        # sudut tebal
        for (cx, cy, dx, dy) in ((250 - pad, 150 - pad * 0.4, 1, 1),
                                 (680 + pad, 150 - pad * 0.4, -1, 1),
                                 (250 - pad, 480 + pad * 0.4, 1, -1),
                                 (680 + pad, 480 + pad * 0.4, -1, -1)):
            c.line([(cx, cy), (cx + 26 * dx, cy)], fill=LILAC, width=3)
            c.line([(cx, cy), (cx, cy + 26 * dy)], fill=LILAC, width=3)

    # di luar bingkai: profesi lain, pudar
    if t > dur * 0.4:
        a = seg(t, dur * 0.4, dur * 0.75)
        for i, x2 in enumerate((120, 176, 800, 856)):
            pose = idle_pose(t * 0.8 + i, x2, GROUND - 2, scale=0.8)
            draw_person(c, pose, CREAM, depth=0.0, alpha=0.20 * a)
    return c


def s10_question(t, dur):
    """Satu orang di tingkat atas; di bawah, antrean yang menunggu."""
    c = Canvas(); c.begin(); backdrop(c)
    c.cam(zoom=1.0 + 0.16 * seg(t, 0, dur), ox=-10, oy=10)
    floor(c)
    stairs(c, 420, GROUND, 4, sw=84, sh=46)

    top_x, top_y = 420 + 3 * 84 + 30, GROUND - 4 * 46 - 2
    boss = idle_pose(t, top_x, top_y, 1.02, 0.9)
    boss.head = 10
    boss.spine = 3
    draw_person(c, boss, CREAM)
    c.glow(top_x, top_y - 52, 56, (32, 40, 60), 0.85)

    # antrean menunggu di bawah
    for i in range(6):
        x = 60 + i * 56
        pose = idle_pose(t * 0.9 + i * 0.6, x, GROUND - 2, 0.82, 0.5)
        pose.head = -6
        draw_person(c, pose, fog(clothes(i), 0.28), depth=0.28)

    # satu orang sedang naik
    prog = seg(t, dur * 0.3, dur * 0.8)
    idx = int(prog * 3)
    x = 420 + idx * 84 + 20
    y = GROUND - (idx + 1) * 46 + 44
    walk = climb_pose(t * 6, x, y, 0.86)
    draw_person(c, walk, fog(CREAM, 0.12), depth=0.12)
    return c


SCENES = {
    "s1_hall": s1_hall,
    "s2_measure": s2_measure,
    "s3_sales": s3_sales,
    "s4_team_drop": s4_team_drop,
    "s5_cross_team": s5_cross_team,
    "s6_towers": s6_towers,
    "s7_reward": s7_reward,
    "s8_peter": s8_peter,
    "s9_bounds": s9_bounds,
    "s10_question": s10_question,
}


# ------------------------------------------------------------------ render
def render_scene(name, duration, out_path, ffmpeg, fps=30):
    fn = SCENES[name]
    n = max(2, int(round(duration * fps)))
    cmd = [ffmpeg, "-y", "-hide_banner", "-loglevel", "error",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(fps),
           "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
           "-pix_fmt", "yuv420p", "-g", "48", "-movflags", "+faststart", str(out_path)]
    pr = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    rng = np.random.default_rng(9)
    for i in range(n):
        t = i / fps
        c = fn(t, duration)
        img = c.finish()
        arr = np.asarray(img, np.float32) + rng.normal(0, 1.4, (H, W, 1))
        pr.stdin.write(np.clip(arr, 0, 255).astype(np.uint8).tobytes())
    pr.stdin.close()
    pr.wait()
    print(f"  {name:14s} {n:5d} frame  {out_path.stat().st_size/1024:6.0f} KB")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--ffmpeg", default="ffmpeg")
    ap.add_argument("--only", default="")
    ap.add_argument("--proof", action="store_true")
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    names = [a.only] if a.only else list(SCENES)
    for n in names:
        render_scene(n, 7.0 if a.proof else 14.0, out / f"{n}.mp4", a.ffmpeg)
    print("selesai ->", out)
