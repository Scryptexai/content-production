#!/usr/bin/env python3
"""motion.py — retargeting gerakan + pijakan berbasis IK.

Masalah yang dipecahkan
-----------------------
Di versi sebelumnya pose ditentukan oleh SUDUT yang saya tulis manual
(hip=52°, knee=-56°, dst). Akibatnya:
  * telapak kaki tidak pernah benar-benar menempel di permukaan anak tangga
  * kaki melayang atau menembus batu, tergantung tinggi badan figur
  * kalau ukuran anak tangga diubah, geraknya rusak — harus dituning ulang

Pendekatan di sini dibalik: yang ditentukan adalah POSISI TELAPAK di dunia
(hasil dari geometri tangga), lalu sudut sendi dihitung dengan IK 2-tulang.
Ini yang di industri disebut retargeting: gerak didefinisikan oleh target di
ruang, bukan oleh rotasi sendi, sehingga bisa dipindah ke ukuran tubuh dan
ukuran tangga apa pun tanpa tuning.

Konvensi sudut sama dengan cine.py: 0° = bawah, 90° = kanan (searah jarum jam).
"""
from __future__ import annotations

import math

from cine import P, Pose, _dir, clamp, lerp, smooth

EPS = 1e-6


def _norm_deg(a):
    while a > 180:
        a -= 360
    while a < -180:
        a += 360
    return a


def two_bone_ik(hip_xy, target_xy, l1, l2, bend=-1):
    """IK dua tulang. Kembalikan (sudut_paha, sudut_lutut) dalam derajat.

    bend=-1 → lutut menekuk ke belakang (ke arah -x), seperti lutut manusia
    dalam pandangan samping menghadap kanan.
    """
    dx = target_xy[0] - hip_xy[0]
    dy = target_xy[1] - hip_xy[1]
    d = math.hypot(dx, dy)
    # jangkauan harus di dalam segitiga: |l1-l2| < d < l1+l2
    d = max(abs(l1 - l2) + 0.5, min(l1 + l2 - 0.5, d))
    ang = math.degrees(math.atan2(dx, dy))          # arah paha→telapak
    cos_a = clamp((l1 * l1 + d * d - l2 * l2) / (2 * l1 * d), -1.0, 1.0)
    a = math.degrees(math.acos(cos_a))
    hip_a = ang + bend * a
    kx = hip_xy[0] + _dir(hip_a)[0] * l1
    ky = hip_xy[1] + _dir(hip_a)[1] * l1
    shin_a = math.degrees(math.atan2(target_xy[0] - kx, target_xy[1] - ky))
    knee_a = _norm_deg(shin_a - hip_a)
    return hip_a, knee_a


def apply_foot_targets(ps: Pose):
    """Hitung ulang sudut kaki dari target telapak (kalau ada)."""
    h = ps.h
    l1 = P["thigh"] * h
    l2 = P["shin"] * h
    hip = (ps.x, ps.y)
    for side, target in (("l", ps.foot_l), ("r", ps.foot_r)):
        if target is None:
            continue
        hp = (hip[0] + (P["hip_dx"] if side == "l" else -P["hip_dx"]) * h, hip[1])
        # telepak: target adalah posisi MATA KAKI
        ha, ka = two_bone_ik(hp, target, l1, l2, bend=-1 if side == "l" else -1)
        if side == "l":
            ps.hip_l, ps.knee_l = ha, ka
        else:
            ps.hip_r, ps.knee_r = ha, ka
    return ps


def sole_offset(h):
    """Jarak mata kaki → telapak (dipakai untuk menaruh kaki tepat di permukaan)."""
    return (0.018 + P["foot_r"] * 0.92) * h


# --------------------------------------------------------------- klip gerak
class Climb:
    """Klip memanjat tangga yang diturunkan dari GEOMETRI, bukan dari sudut.

    Parameter geometri (x0, y0, tread, riser, n) boleh berubah; klip ini
    otomatis menyesuaikan langkah dan tinggi panggul.
    """

    def __init__(self, x0, y0, tread, riser, n, h, edge=0.42, hip_frac=0.470):
        self.x0, self.y0 = x0, y0
        self.tread, self.riser, self.n = tread, riser, n
        self.h = h
        self.edge = edge          # posisi telapak relatif terhadap tapak (0..1)
        self.hip_frac = hip_frac  # tinggi panggul sebagai fraksi tinggi badan

    # -- geometri ------------------------------------------------------
    def surface_y(self, i):
        return self.y0 - i * self.riser

    def foot_x(self, i):
        return self.x0 + i * self.tread + self.tread * self.edge

    def ankle_target(self, i):
        """Posisi mata kaki supaya telapak menempel di tapak ke-i."""
        return (self.foot_x(i), self.surface_y(i) - sole_offset(self.h))

    # -- pose ----------------------------------------------------------
    def pose(self, u, t=0.0):
        """u = progres dalam satuan anak tangga (0..n)."""
        h = self.h
        i = min(int(u), self.n)
        ph = clamp(u - i, 0.0, 1.0)

        # dua kaki bergantian: yang menopang di tangga i, yang melangkah dari i-1
        lead = 1 if i % 2 == 0 else -1      # kaki mana yang melangkah lebih dulu
        if i >= 1:
            swing_from = self.ankle_target(i - 1)
        else:
            swing_from = (self.foot_x(0) - self.tread, self.surface_y(0) - sole_offset(h))
        swing_to = self.ankle_target(min(i + 1, self.n)) if i < self.n else self.ankle_target(i)
        support = self.ankle_target(i)

        # fase langkah: 0.00-0.16 tumpu, 0.16-0.62 angkat, 0.62-0.80 tapak, 0.80-1.00 tenang
        if ph < 0.16:
            q = 0.0
        elif ph < 0.62:
            q = smooth((ph - 0.16) / 0.46)
        elif ph < 0.80:
            q = 1.0
        else:
            q = 1.0
        # busur angkat: kaki naik melewati tanjakan, tidak menabrak
        lift = math.sin(math.pi * clamp((ph - 0.16) / 0.46)) * self.riser * 0.62
        swing = (lerp(swing_from[0], swing_to[0], q),
                 lerp(swing_from[1], swing_to[1], q) - lift)

        # panggul: di antara kedua telapak, sedikit condong ke depan
        px = (swing[0] + support[0]) * 0.5 + self.tread * 0.06
        py = support[1] - h * self.hip_frac
        # anticipation: turun sebelum mengangkat; mendarat: tertekan sebentar
        dip = math.sin(math.pi * clamp(ph / 0.18)) * h * 0.014
        settle = math.sin(math.pi * clamp((ph - 0.62) / 0.20)) * h * 0.010
        py += dip - settle

        # pastikan kedua telapak terjangkau: turunkan panggul bila perlu
        lmax = (P["thigh"] + P["shin"]) * h * 0.965
        for ft in (swing, support):
            for _ in range(8):
                dx = ft[0] - px
                dy = ft[1] - py
                if math.hypot(dx, dy) <= lmax:
                    break
                py += h * 0.004

        p = Pose(px, py, h)
        p.body = (8, 8, 12)
        p.hair = 1
        if lead > 0:
            p.foot_l, p.foot_r = swing, support
        else:
            p.foot_r, p.foot_l = swing, support

        # -- badan atas: tetap memakai sudut, karena tidak menyentuh apa pun
        sw = math.sin(math.pi * clamp((ph - 0.12) / 0.50)) if ph >= 0.12 else 0.0
        p.spine = 11 - 5 * sw
        p.head = -8
        reach = 10 + 138 * sw
        elbow = -40 * sw - 6
        if lead > 0:
            p.arm_r, p.elbow_r = reach, elbow
            p.arm_l, p.elbow_l = 14, 8
        else:
            p.arm_l, p.elbow_l = reach, elbow
            p.arm_r, p.elbow_r = 14, 8
        p.coat = -0.5 * sw
        # mengalir ke belakang hampir mendatar, dengan sedikit naik-turun
        gust = 258 - 18 * sw + 6 * math.sin(t * 2.1)
        p.scarf = (gust, 22 + 10 * math.sin(t * 2.7 + 1.0))
        apply_foot_targets(p)
        return p

    def standing(self, i, t=0.0, raise_arm=0.0):
        """Berdiri di tapak ke-i (dipakai untuk akhir shot)."""
        h = self.h
        a = self.ankle_target(i)
        b = (a[0] - self.tread * 0.42, a[1])
        px = (a[0] + b[0]) * 0.5
        py = a[1] - h * 0.478
        p = Pose(px, py, h)
        p.body, p.hair = (8, 8, 12), 1
        p.foot_r, p.foot_l = a, b
        p.spine = 1.0
        p.head = -12 - 5 * raise_arm
        # lengan sedikit terbuka saat tiba — gestur kecil lebih jujur daripada
        # tangan terangkat tinggi yang terbaca seperti orang-orangan sawah
        p.arm_r = lerp(6, 34, raise_arm)
        p.elbow_r = lerp(7, 14, raise_arm)
        p.arm_l = lerp(5, -22, raise_arm)
        p.elbow_l = lerp(6, 12, raise_arm)
        p.scarf = (252 + 6 * math.sin(t * 1.7), 20 + 7 * math.sin(t * 2.2))
        apply_foot_targets(p)
        return p


# --------------------------------------------------------- keyframe driver
def ease_pose(q, kind="inout"):
    """Kurva antar-keyframe. Slow in/out adalah default; `snap` untuk aksi cepat
    yang butuh hentakan (anticipation tetap di klip, bukan di sini)."""
    q = max(0.0, min(1.0, q))
    if kind == "snap":
        return 1 - (1 - q) ** 4
    if kind == "hold":
        return 0.0 if q < 0.999 else 1.0
    return q * q * (3 - 2 * q)


def pose_between(clip, kf_a, kf_b, q, t=0.0, ease="inout"):
    """Satu pose di antara dua keyframe.

    Keyframe berisi parameter RUANG (u, arm, gaze) — bukan sudut sendi. Karena
    itu rencana ini bisa dijalankan pada tangga dan ukuran tubuh apa pun tanpa
    dituning ulang. Inilah sisi "retargeting" dari rencana shot.
    """
    e = ease_pose(q, ease)
    u = lerp(kf_a["u"], kf_b["u"], e)
    arm = lerp(kf_a["arm"], kf_b["arm"], e)
    gaze = lerp(kf_a["gaze"], kf_b["gaze"], e)

    # di puncak: pakai pose berdiri (bukan pose memanjat)
    if u >= clip.n - 0.001:
        p = clip.standing(clip.n, t, raise_arm=arm)
        p.head = -12 - 26 * gaze
    else:
        p = clip.pose(u, t)
        # lengan & pandangan ditimpa dari keyframe (bukan dari fase klip)
        reach = 12 + 150 * arm
        if p.arm_r > 30:                       # lengan kanan yang aktif
            p.arm_r, p.elbow_r = reach, -40 * arm - 6
        else:
            p.arm_l, p.elbow_l = reach, -40 * arm - 6
        p.head = -6 - 22 * gaze
    return p


def sample_shot(clip, shot, t_local, dur, ease="inout"):
    """Pose pada detik ke-t_local di dalam satu shot."""
    q = 0.0 if dur <= 0 else max(0.0, min(1.0, t_local / dur))
    return pose_between(clip, shot["kf_a"], shot["kf_b"], q, t_local, ease)
