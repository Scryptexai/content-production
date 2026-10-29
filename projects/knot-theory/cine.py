#!/usr/bin/env python3
"""cine.py — renderer filmis 2.5D untuk Knot Theory (v5).

Kenapa file baru, bukan menambal anim2d.py: masalahnya bukan detail kecil.

  anim2d.py (v4)                        cine.py (v5)
  ------------------------------------  ------------------------------------------
  render 960x540 lalu di-upscale 2x     render native 1920x1080, supersample 2x
  figur 17% tinggi frame (tak terbaca)  figur 42-55% tinggi frame
  satu lapis gambar datar               5 lapis kedalaman, parallax + skala sendiri
  tanpa bayangan                        bayangan kontak + rim light matahari
  tanpa blur kedalaman                  depth of field per lapis
  tanpa kabut                           kabut atmosferik per kedalaman
  interpolasi linear (kaku)             anticipation, overshoot, follow-through, arc
  output datar                          bloom, halation, grade, vignette, grain

Semua yang di bawah ini diambil dari riset produksi faceless/animation
(lihat docs/FACELESS-QUALITY.md untuk sumber dan checklist-nya).
"""
from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

W, H = 1920, 1080
SS = 2                      # supersampling: digambar 3840x2160, diturunkan ke 1080p

# --------------------------------------------------------------------- warna
INK = (11, 15, 24)
INK2 = (19, 24, 38)
CREAM = (239, 231, 220)
ROSE = (217, 142, 115)
SAGE = (143, 169, 139)
LILAC = (167, 155, 200)
MUTED = (122, 132, 150)
SUN = (255, 214, 168)


# ------------------------------------------------------------------- utilitas
def clamp(v, a=0.0, b=1.0):
    return a if v < a else (b if v > b else v)


def lerp(a, b, t):
    return a + (b - a) * t


def mix(c1, c2, t):
    return tuple(int(lerp(c1[i], c2[i], t)) for i in range(3))


def smooth(t):
    t = clamp(t)
    return t * t * (3 - 2 * t)


def seg(t, t0, t1):
    if t1 <= t0:
        return 1.0 if t >= t1 else 0.0
    return smooth((t - t0) / (t1 - t0))


def ease_out(t):
    t = clamp(t)
    return 1 - (1 - t) ** 3


def ease_in(t):
    return clamp(t) ** 3


def overshoot(t, amt=0.12):
    """Ease-out yang melewati target lalu balik — follow-through."""
    t = clamp(t)
    return 1 - math.exp(-6 * t) * math.cos(8.5 * t) * (1 + amt * 0)


def arc(p, height):
    """Tinggi busur parabola untuk gerak 0..1 (kaki/lengan mengayun)."""
    return 4 * height * p * (1 - p)


def _dir(deg):
    r = math.radians(deg)
    return math.sin(r), math.cos(r)


# ---------------------------------------------------------------- transform
class TF:
    """Dunia → piksel kanvas untuk satu lapis kedalaman.

    `ss` = supersample lapis itu. Latar tidak butuh 2x: biayanya 4x lipat dan
    tepinya toh diblur/bloom. Hanya lapis karakter yang digambar 2x.
    """

    __slots__ = ("sc", "ox", "oy", "ss")

    def __init__(self, sc=1.0, ox=0.0, oy=0.0, ss=1):
        self.sc, self.ox, self.oy, self.ss = sc, ox, oy, ss

    def p(self, x, y):
        return (W * self.ss * 0.5 + x * self.sc * self.ss + self.ox * self.ss,
                H * self.ss * 0.5 + y * self.sc * self.ss + self.oy * self.ss)

    def s(self, v):
        return v * self.sc * self.ss


class Cam:
    """Kamera dunia. z = 1 memperlihatkan 1920x1080 dunia."""

    def __init__(self, x=0.0, y=0.0, z=1.0):
        self.x, self.y, self.z = x, y, z

    def tf(self, depth, ss=1):
        """depth 0 (paling jauh) .. 1 (paling dekat)."""
        par = 0.28 + 1.30 * depth          # lapis jauh hampir tidak bergeser
        sc = self.z * (0.90 + 0.26 * depth)
        return TF(sc, -self.x * par * sc, -self.y * par * sc, ss)


# ------------------------------------------------------------------- lapisan
class Pen:
    """Kanvas RGBA transparan untuk satu lapis kedalaman."""

    def __init__(self, tf: TF, fill=None):
        self.tf = tf
        self.img = Image.new("RGBA", (W * tf.ss, H * tf.ss), (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.img)
        if fill is not None:
            self.d.rectangle([0, 0, W * tf.ss, H * tf.ss], fill=fill)

    # -- primitif -------------------------------------------------------
    def p(self, x, y):
        return self.tf.p(x, y)

    def s(self, v):
        return self.tf.s(v)

    def taper(self, x1, y1, x2, y2, r1, r2, fill):
        """Batang mengecil dari r1 ke r2. Tanpa ini, ujung kapsul yang
        bertumpuk di sendi membuat tonjolan bola saat kaki menekuk."""
        a, b = self.p(x1, y1), self.p(x2, y2)
        R1, R2 = max(1.0, self.s(r1)), max(1.0, self.s(r2))
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / L, dx / L
        self.d.polygon([(a[0] + nx * R1, a[1] + ny * R1),
                        (b[0] + nx * R2, b[1] + ny * R2),
                        (b[0] - nx * R2, b[1] - ny * R2),
                        (a[0] - nx * R1, a[1] - ny * R1)], fill=fill)
        self.d.ellipse([a[0] - R1, a[1] - R1, a[0] + R1, a[1] + R1], fill=fill)
        self.d.ellipse([b[0] - R2, b[1] - R2, b[0] + R2, b[1] + R2], fill=fill)

    def capsule(self, x1, y1, x2, y2, r, fill):
        a, b = self.p(x1, y1), self.p(x2, y2)
        rr = max(1.0, self.s(r))
        self.d.line([a, b], fill=fill, width=int(rr * 2))
        for pt in (a, b):
            self.d.ellipse([pt[0] - rr, pt[1] - rr, pt[0] + rr, pt[1] + rr], fill=fill)

    def circle(self, x, y, r, fill):
        c, rr = self.p(x, y), self.s(r)
        self.d.ellipse([c[0] - rr, c[1] - rr, c[0] + rr, c[1] + rr], fill=fill)

    def ellipse(self, x, y, rx, ry, fill):
        c = self.p(x, y)
        self.d.ellipse([c[0] - self.s(rx), c[1] - self.s(ry),
                        c[0] + self.s(rx), c[1] + self.s(ry)], fill=fill)

    def poly(self, pts, fill):
        self.d.polygon([self.p(x, y) for x, y in pts], fill=fill)

    def quad(self, pts, fill):
        self.poly(pts, fill)

    def line(self, pts, fill, width=2):
        self.d.line([self.p(x, y) for x, y in pts], fill=fill,
                    width=max(1, int(self.s(width))), joint="curve")

    def rect(self, x, y, w, h, fill):
        a, b = self.p(x, y), self.p(x + w, y + h)
        self.d.rectangle([min(a[0], b[0]), min(a[1], b[1]),
                          max(a[0], b[0]), max(a[1], b[1])], fill=fill)

    def soft_shadow(self, x, y, rx, ry, alpha=0.5, steps=6):
        """Bayangan kontak lembut tanpa GaussianBlur (murah)."""
        for i in range(steps, 0, -1):
            k = i / steps
            a = int(255 * alpha * (1 - k) ** 1.6 / steps * 2.2)
            if a <= 0:
                continue
            self.ellipse(x, y, rx * k * 1.5, ry * k * 1.5, (0, 0, 0, a))


# ------------------------------------------------------------------ karakter
class Pose:
    """Sudut derajat: 0 = bawah, positif = searah jarum jam."""

    __slots__ = ("x", "y", "h", "spine", "head",
                 "arm_l", "elbow_l", "arm_r", "elbow_r",
                 "hip_l", "knee_l", "hip_r", "knee_r",
                 "coat", "alpha", "body", "hair", "scarf",
                 "foot_l", "foot_r")

    def __init__(self, x=0.0, y=0.0, h=420.0):
        self.x, self.y, self.h = x, y, h
        self.spine = 0.0
        self.head = 0.0
        self.arm_l, self.elbow_l = 9.0, 8.0
        self.arm_r, self.elbow_r = -9.0, 8.0
        self.hip_l, self.knee_l = 4.0, 3.0
        self.hip_r, self.knee_r = -4.0, 3.0
        self.coat = 0.0
        self.alpha = 1.0
        self.body = CREAM
        self.hair = 0
        # selendang: [sudut1, sudut2] derajat untuk dua segmen yang tertinggal
        self.scarf = None
        # target mata kaki di koordinat dunia (retargeting IK). None = sudut manual
        self.foot_l = None
        self.foot_r = None


# proporsi (fraksi tinggi badan). Dibuat lebih langsing dari v4: torso tidak
# lagi selebar kepala, lengan & kaki tidak menempel badan.
P = dict(
    torso=0.272, neck=0.030, head_r=0.077, head_lift=0.074,
    hip_r=0.076, torso_r=0.064, shoulder=0.084, shoulder_r=0.046,
    upper=0.160, fore=0.148, arm_r=0.031, hand_r=0.034,
    thigh=0.236, shin=0.226, leg_r=0.045, foot_r=0.029,
    hip_dx=0.026, sh_dx=0.074, sole=0.046,
)


def _ik(hip_xy, target_xy, l1, l2):
    """IK dua tulang; lutut menekuk ke belakang seperti lutut manusia."""
    dx = target_xy[0] - hip_xy[0]
    dy = target_xy[1] - hip_xy[1]
    d = max(abs(l1 - l2) + 0.5, min(l1 + l2 - 0.5, math.hypot(dx, dy)))
    ang = math.degrees(math.atan2(dx, dy))
    cos_a = max(-1.0, min(1.0, (l1 * l1 + d * d - l2 * l2) / (2 * l1 * d)))
    a = math.degrees(math.acos(cos_a))
    hip_a = ang - a
    kx = hip_xy[0] + _dir(hip_a)[0] * l1
    ky = hip_xy[1] + _dir(hip_a)[1] * l1
    shin_a = math.degrees(math.atan2(target_xy[0] - kx, target_xy[1] - ky))
    knee_a = shin_a - hip_a
    while knee_a > 180:
        knee_a -= 360
    while knee_a < -180:
        knee_a += 360
    return hip_a, knee_a


def skeleton(ps: Pose):
    """Titik-titik rangka: hip, chest, neck, head, dua lengan, dua kaki."""
    h = ps.h
    hip = (ps.x, ps.y)
    sd = _dir(ps.spine)
    chest = (hip[0] + sd[0] * P["torso"] * h, hip[1] - sd[1] * P["torso"] * h)

    legs = []
    for ha, ka, dx, tgt in ((ps.hip_r, ps.knee_r, -P["hip_dx"], ps.foot_r),
                            (ps.hip_l, ps.knee_l, P["hip_dx"], ps.foot_l)):
        hp = (hip[0] + dx * h, hip[1])
        if tgt is not None:
            ha, ka = _ik(hp, tgt, P["thigh"] * h, P["shin"] * h)
        d1 = _dir(ha)
        knee = (hp[0] + d1[0] * P["thigh"] * h, hp[1] + d1[1] * P["thigh"] * h)
        d2 = _dir(ha + ka)
        ankle = (knee[0] + d2[0] * P["shin"] * h, knee[1] + d2[1] * P["shin"] * h)
        if tgt is not None:            # jepit sisa pembulatan: telapak harus di target
            ankle = tgt
        legs.append((hp, knee, ankle))

    arms = []
    sh = (chest[0], chest[1] + 0.012 * h)
    for aa, ea, dx in ((ps.arm_r, ps.elbow_r, -P["sh_dx"]),
                       (ps.arm_l, ps.elbow_l, P["sh_dx"])):
        s0 = (sh[0] + dx * h, sh[1])
        d1 = _dir(aa)
        elbow = (s0[0] + d1[0] * P["upper"] * h, s0[1] + d1[1] * P["upper"] * h)
        d2 = _dir(aa + ea)
        wrist = (elbow[0] + d2[0] * P["fore"] * h, elbow[1] + d2[1] * P["fore"] * h)
        arms.append((s0, elbow, wrist))

    hd = _dir(ps.spine + ps.head)
    neck = (chest[0] + hd[0] * P["neck"] * h, chest[1] - hd[1] * P["neck"] * h)
    hc = (neck[0] + hd[0] * P["head_lift"] * h, neck[1] - hd[1] * P["head_lift"] * h)
    return dict(hip=hip, chest=chest, neck=neck, head=hc, hd=hd, sd=sd,
                legs=legs, arms=arms, sh=sh)


def sole_offset(h):
    """Jarak mata kaki → telapak (sama persis dengan gambar kapsul sepatu)."""
    return (0.018 + P["foot_r"] * 0.92) * h


def sole_y(ps: Pose):
    """Titik terendah telapak kaki — untuk menempelkan figur ke permukaan."""
    sk = skeleton(ps)
    return max(a[1] for _, _, a in sk["legs"]) + sole_offset(ps.h)


def place_feet(ps: Pose, ground_y):
    """Geser badan supaya telapak yang menapak tepat di permukaan."""
    ps.y += ground_y - sole_y(ps)
    return ps


def draw_figure(pen: Pen, ps: Pose, far_mul=0.42, edge=None, edge_col=INK):
    """Karakter proporsional (±7 kepala) dengan tepi potong ala papercut.

    `edge` = lebar garis tepi dalam piksel dunia. Digambar dua kali: siluet
    yang dilebarkan berwarna ink, lalu figur sebenarnya di atasnya. Itu yang
    membuat figur terbaca dari latar terang maupun gelap.
    """
    h = ps.h
    if edge:
        _draw_body(pen, ps, tuple(edge_col), tuple(edge_col), grow=edge)

    col = ps.body
    far = tuple(int(c * far_mul) for c in col)
    _draw_body(pen, ps, col, far)
    return skeleton(ps)["head"]


def _draw_body(pen: Pen, ps: Pose, col, far, grow=0.0):
    """Badan digambar sebagai MASA TUNGGAL: torso poligon (pinggul→bahu),
    kapsul untuk anggota badan, kepala elips. Tujuannya satu siluet bersih —
    tumpukan kapsul menghasilkan bentuk bergelambir.
    """
    h = ps.h
    sk = skeleton(ps)
    hip, chest = sk["hip"], sk["chest"]
    g = grow
    sd = sk["sd"]
    perp = (-sd[1], sd[0])

    def cap(a, b, r, c):
        pen.capsule(a[0], a[1], b[0], b[1], r + g, c)

    def cir(p, r, c):
        pen.circle(p[0], p[1], r + g, c)

    # --- kaki (sisi jauh dulu): mengecil dari paha ke pergelangan
    rl = P["leg_r"] * h
    for (hp, knee, ankle), c in zip(sk["legs"], (far, col)):
        pen.taper(hp[0], hp[1], knee[0], knee[1], rl * 1.06 + g, rl * 0.92 + g, c)
        pen.taper(knee[0], knee[1], ankle[0], ankle[1], rl * 0.92 + g, rl * 0.70 + g, c)
        cap((ankle[0] - 0.016 * h, ankle[1] + 0.018 * h),
            (ankle[0] + 0.042 * h, ankle[1] + 0.018 * h), P["foot_r"] * h * 0.92, c)

    # --- torso: satu poligon dari pinggul ke bahu, sisi dibulatkan
    hipw, shw = 0.052 * h + g, 0.078 * h + g
    prof = [(hip[0] - hipw * perp[0], hip[1] - hipw * perp[1]),
            (hip[0] + hipw * perp[0], hip[1] + hipw * perp[1]),
            (chest[0] + shw * perp[0], chest[1] + shw * perp[1]),
            (chest[0] - shw * perp[0], chest[1] - shw * perp[1])]
    pen.poly([prof[0], prof[1], prof[2], prof[3]], col)
    # bahu membulat menutup sudut poligon
    cir(chest, 0.030 * h, col)

    # --- mantel/rok: satu massa membulat yang menempel di pinggul
    if ps.coat:
        cx, cy = hip[0] + ps.coat * 0.03 * h, hip[1] + 0.035 * h
        pen.ellipse(cx, cy, 0.062 * h + g, 0.072 * h + g, col)

    # --- lengan: mengecil dari bahu ke pergelangan
    ra = P["arm_r"] * h
    for (s0, elbow, wrist), c in zip(sk["arms"], (far, col)):
        pen.taper(s0[0], s0[1], elbow[0], elbow[1], ra * 1.12 + g, ra * 0.92 + g, c)
        pen.taper(elbow[0], elbow[1], wrist[0], wrist[1], ra * 0.92 + g, ra * 0.74 + g, c)
        cir(wrist, P["hand_r"] * h * 0.72, c)

    # --- selendang: dua segmen yang tertinggal dari badan (follow-through)
    if ps.scarf:
        a1, a2 = ps.scarf           # derajat absolut: 270 = kiri, 180 = atas
        # pangkal di PUNGGUNG (bukan leher), supaya tidak menyeberang wajah
        d1 = _dir(a1)
        sx = chest[0] - sk["sd"][0] * 0.02 * h
        sy = chest[1] + 0.045 * h
        p1 = (sx + d1[0] * 0.080 * h, sy + d1[1] * 0.080 * h)
        d2 = _dir(a1 + a2)
        p2 = (p1[0] + d2[0] * 0.070 * h, p1[1] + d2[1] * 0.070 * h)
        pen.taper(sx, sy, p1[0], p1[1], 0.019 * h + g, 0.015 * h + g, col)
        pen.taper(p1[0], p1[1], p2[0], p2[1], 0.015 * h + g, 0.010 * h + g, col)

    # --- leher (menyambung, bukan celah) + kepala
    cap(chest, sk["neck"], 0.032 * h, col)
    hc = sk["head"]
    pen.ellipse(hc[0], hc[1], P["head_r"] * h * 0.98 + g,
                P["head_r"] * h * 1.06 + g, col)
    if ps.hair:
        pen.ellipse(hc[0] - sk["hd"][0] * 0.026 * h, hc[1] - sk["hd"][1] * 0.010 * h,
                    P["head_r"] * h * 1.00 + g, P["head_r"] * h * 0.70 + g, col)


# ------------------------------------------------------------------ gerak
def idle_pose(t, x, y, h, breathe=1.0):
    p = Pose(x, y, h)
    b = math.sin(t * 1.35) * breathe
    p.spine = 1.2 + 0.7 * b
    p.arm_l = 7 + 1.6 * b
    p.arm_r = -7 - 1.6 * b
    p.elbow_l = p.elbow_r = 6
    p.head = 1.2 * b
    p.y = y + 0.8 * b
    return p


def walk_pose(phase, x, y, h, speed=1.0):
    p = Pose(x, y, h)
    sw = math.sin(phase)
    p.hip_l = 24 * sw * speed
    p.knee_l = -(30 * max(0, -math.sin(phase - 0.7)) + 4)
    p.hip_r = -24 * sw * speed
    p.knee_r = -(30 * max(0, math.sin(phase - 0.7)) + 4)
    p.arm_l = -19 * sw * speed
    p.elbow_l = 12 + 9 * max(0, sw)
    p.arm_r = 19 * sw * speed
    p.elbow_r = 12 + 9 * max(0, -sw)
    p.spine = 2.4 + 1.1 * math.sin(phase * 2)
    p.head = -1.5
    p.y = y - abs(math.sin(phase)) * 0.010 * h
    return p


def climb_pose(phase, x, y, h, lead=1, rise=0.0):
    """Satu langkah tangga = satu `phase` (0..1).

    0.00-0.22 anticipation : badan turun, berat pindah ke kaki penopang
    0.22-0.55 lift         : kaki depan naik lewat busur, badan mulai naik
    0.55-0.68 plant        : kaki menapak, badan tertekan sedikit
    0.68-1.00 settle       : badan tegak lagi, lengan selesai mengayun
    """
    p = Pose(x, y, h)
    ph = phase % 1.0
    dip = math.sin(math.pi * clamp(ph / 0.22)) * 0.016
    rise_c = smooth(clamp((ph - 0.22) / 0.33))
    plant = math.sin(math.pi * clamp((ph - 0.55) / 0.13)) * 0.014
    p.y = y - (rise_c - dip - plant) * h * 0.55

    # Mengangkat kaki ke anak tangga berikutnya: paha maju-atas, tulang kering
    # menggantung ke bawah (lutut menekuk ke belakang), lalu menapak.
    # `lead` hanya memilih KAKI MANA - arah langkah selalu ke depan.
    if 0.22 <= ph < 0.55:
        q = (ph - 0.22) / 0.33
        k = math.sin(math.pi * q)
        hip_a = 52 * k
        knee_a = -(56 * k + 6)
    elif 0.55 <= ph < 0.68:
        q = (ph - 0.55) / 0.13
        hip_a = 34 * (1 - q) + 3
        knee_a = -(30 * (1 - q) + 9)
    else:
        hip_a, knee_a = 3, -6
    if lead > 0:
        p.hip_l, p.knee_l = hip_a, knee_a
        p.hip_r, p.knee_r = -3, -8
    else:
        p.hip_r, p.knee_r = hip_a, knee_a
        p.hip_l, p.knee_l = -3, -8

    swing = math.sin(math.pi * clamp((ph - 0.18) / 0.42)) if ph >= 0.18 else 0.0
    # 0 derajat = bawah, 150 = depan-atas (menjangkau). Lengan yang menarik
    # badan ke atas mengayun dari tergantung (12) ke menjangkau (150).
    reach = 10 + 142 * swing
    elbow = -44 * swing - 6
    if lead > 0:
        p.arm_r, p.elbow_r = reach, elbow
        p.arm_l, p.elbow_l = 12, 10
    else:
        p.arm_l, p.elbow_l = reach, elbow
        p.arm_r, p.elbow_r = 12, 10
    p.spine = 10 - 4 * rise_c
    p.head = -7
    p.coat = -0.5 * swing
    return p


# ---------------------------------------------------------------- post-fx
def rim_light(img: np.ndarray, color, dx=3.0, dy=3.0, strength=0.85, width=1.6):
    """Garis tipis terang di sisi yang menghadap cahaya (matahari kanan-atas)."""
    a = img[:, :, 3].astype(np.float32) / 255.0
    dxi, dyi = int(round(dx)), int(round(dy))
    if abs(dxi) >= 1:
        a_r = np.roll(a, -dxi, axis=1)
    else:
        a_r = a
    if abs(dyi) >= 1:
        a_t = np.roll(a, dyi, axis=0)
    else:
        a_t = a
    rim = np.clip(a * 0.55 + 0.45 * a - (0.45 * a_r + 0.55 * a_t), 0, 1)
    rim = np.clip((a - a_r) * 0.7 + (a - a_t) * 1.0, 0, 1)
    if rim.max() <= 0:
        return img
    rim_l = Image.fromarray((rim * 255).astype(np.uint8)).filter(
        ImageFilter.GaussianBlur(width * SS / 2))
    rim = np.asarray(rim_l, np.float32) / 255.0
    mask = (rim * strength)[:, :, None]
    col = np.array(color, np.float32)[None, None, :]
    rgb = img[:, :, :3].astype(np.float32)
    rgb = rgb + mask * col
    img = img.copy()
    img[:, :, :3] = np.clip(rgb, 0, 255).astype(np.uint8)
    return img


_PAPER = None


def paper_texture(seed=13):
    """Tekstur kertas: bintik halus + serat. Disimpan sekali, dipakai tiap frame."""
    global _PAPER
    if _PAPER is not None:
        return _PAPER
    rng = np.random.default_rng(seed)
    fine = rng.normal(0, 1, (H // 2, W // 2)).astype(np.float32)
    fib = rng.normal(0, 1, (H // 2, W // 2)).astype(np.float32)
    from PIL import ImageFilter as _IF
    a = Image.fromarray(((fine * 0.5 + 0.5) * 255).astype(np.uint8)).filter(
        _IF.GaussianBlur(0.6)).resize((W, H), Image.BILINEAR)
    b = Image.fromarray(((fib * 0.5 + 0.5) * 255).astype(np.uint8)).filter(
        _IF.GaussianBlur(2.2)).resize((W, H), Image.BILINEAR)
    t = (np.asarray(a, np.float32) - 127) / 255.0 * 0.55 + \
        (np.asarray(b, np.float32) - 127) / 255.0 * 0.45
    _PAPER = t[:, :, None].astype(np.float32)
    return _PAPER


def drop_shadow(a, dx=7, dy=11, blur=9, alpha=0.55):
    """Bayangan antar lapis: inilah yang membuat potongan kertas terasa
    menumpuk di ruang nyata, bukan ditempel rata."""
    al = Image.fromarray(a[:, :, 3].astype(np.uint8))
    al = al.filter(ImageFilter.GaussianBlur(blur))
    al = np.asarray(al, np.float32) / 255.0 * alpha
    al = np.roll(al, dy, axis=0)
    al = np.roll(al, dx, axis=1)
    al[0:max(0, dy), :] = 0
    al[:, 0:max(0, dx)] = 0
    return al[:, :, None]


def down(img) -> np.ndarray:
    """Turunkan kanvas supersample (3840x2160) ke 1920x1080. Terima Image/ndarray."""
    if not isinstance(img, Image.Image):
        img = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
    if img.size == (W, H):
        return np.asarray(img, dtype=np.float32)
    return np.asarray(img.resize((W, H), Image.LANCZOS), dtype=np.float32)


def blur_img(arr: np.ndarray, r: float) -> np.ndarray:
    if r < 0.4:
        return arr
    im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    im = im.filter(ImageFilter.GaussianBlur(r))
    return np.asarray(im, dtype=np.float32)


def over(dst, src):
    """Alpha compositing: dst RGB (float32) <- src RGBA (float32, straight alpha)."""
    a = src[:, :, 3:4] / 255.0
    return dst * (1 - a) + src[:, :, :3] * a


def sky_gradient(stops, size=(W, H)):
    """stops = [(posisi 0..1, (r,g,b)), ...] dari atas ke bawah."""
    hgt, wid = size[1], size[0]
    ys = np.linspace(0, 1, hgt, dtype=np.float32)
    out = np.zeros((hgt, 3), np.float32)
    for i in range(len(stops) - 1):
        p0, c0 = stops[i]
        p1, c1 = stops[i + 1]
        m = (ys >= p0) & (ys <= p1)
        if not m.any():
            continue
        t = ((ys[m] - p0) / max(1e-6, p1 - p0))[:, None]
        out[m] = np.array(c0, np.float32) * (1 - t) + np.array(c1, np.float32) * t
    out[ys < stops[0][0]] = stops[0][1]
    out[ys > stops[-1][0]] = stops[-1][1]
    return np.repeat(out[:, None, :], wid, axis=1)


def radial(size, cx, cy, r, color, power=2.2, scale=2):
    """Medan radial. `scale` = faktor komputasi (2 = hitung di setengah resolusi)."""
    hgt, wid = size[1], size[0]
    hh, ww = hgt // scale, wid // scale
    yy, xx = np.mgrid[0:hh, 0:ww].astype(np.float32)
    d = np.sqrt((xx - cx / scale) ** 2 + (yy - cy / scale) ** 2) / max(1.0, r / scale)
    f = np.clip(1 - d, 0, 1) ** power
    big = np.asarray(Image.fromarray((f * 255).astype(np.uint8)).resize(
        (wid, hgt), Image.BILINEAR), np.float32) / 255.0
    return big[:, :, None] * np.array(color, np.float32)[None, None, :]


def aces(x):
    a, b, c, d, e = 2.51, 0.03, 2.43, 0.59, 0.14
    return np.clip((x * (a * x + b)) / (x * (c * x + d) + e), 0, 1)


_VIG = None


def _vignette(vig):
    global _VIG
    if _VIG is not None and _VIG[0] == vig:
        return _VIG[1]
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    dx = (xx - W / 2) / (W / 2)
    dy = (yy - H / 2) / (H / 2)
    d = np.sqrt(dx * dx * 0.85 + dy * dy)
    v = (1 - vig * np.clip(d - 0.30, 0, 1.4) ** 1.9)[:, :, None].astype(np.float32)
    _VIG = (vig, v)
    return v


def grade(rgb: np.ndarray, frame_i: int, exposure=1.12, grain=0.016, vig=0.66):
    x = rgb / 255.0 * exposure
    # kurva filmis lembut + lift hitam
    x = 0.55 * x + 0.45 * aces(x)
    x = 0.016 + x * 0.984
    # split-tone: bayangan ke biru, highlight ke hangat
    lum = (x[:, :, 0] * 0.299 + x[:, :, 1] * 0.587 + x[:, :, 2] * 0.114)[:, :, None]
    sh = (1 - lum) ** 1.7
    hi = lum ** 1.7
    x = x + sh * np.array([-0.012, 0.004, 0.026], np.float32)
    x = x + hi * np.array([0.030, 0.010, -0.024], np.float32)
    # vignette (mask di-cache)
    x = x * _vignette(vig)
    # tekstur kertas + grain halus
    x = x + paper_texture() * 0.020 * (0.35 + 0.65 * (1 - lum))
    rng = np.random.default_rng(9000 + frame_i)
    g = rng.normal(0, grain, (H, W, 1)).astype(np.float32)
    x = x + g * (1.0 - 0.55 * lum)
    return np.clip(x, 0, 1)


def bloom(rgb, thresh=0.80, radius=38, strength=0.34, warm=(1.0, 0.80, 0.58)):
    lum = (rgb[:, :, 0] * 0.299 + rgb[:, :, 1] * 0.587 + rgb[:, :, 2] * 0.114)
    m = np.clip((lum - thresh) / max(1e-3, 1 - thresh), 0, 1)[:, :, None] ** 1.6
    bright = rgb * m
    half = np.asarray(Image.fromarray(np.clip(bright, 0, 255).astype(np.uint8)).resize(
        (W // 2, H // 2), Image.BILINEAR), np.float32)
    hb = blur_img(half, radius / 2)
    hb2 = blur_img(half, radius * 1.3)
    b = np.asarray(Image.fromarray(np.clip(hb, 0, 255).astype(np.uint8)).resize(
        (W, H), Image.BILINEAR), np.float32)
    bright = bright * 0.25
    b = b + 0.0
    b = b
    b2 = np.asarray(Image.fromarray(np.clip(hb2, 0, 255).astype(np.uint8)).resize(
        (W, H), Image.BILINEAR), np.float32)
    col = np.array(warm, np.float32)[None, None, :]
    return rgb + (b * 0.85 + b2 * 0.55) * strength * col


def chroma(rgb, amt=0.0012):
    """Aberasi kromatik di tepi — satu detail kecil yang menandakan lensa, bukan
    gambar komputer."""
    if amt <= 0:
        return rgb
    im = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8))
    ch = list(im.split())
    out = []
    for i, c in enumerate(ch):
        k = 1.0 + (amt if i == 0 else (-amt if i == 2 else 0))
        w2, h2 = int(W * k), int(H * k)
        cc = c.resize((w2, h2), Image.BICUBIC)
        l = (w2 - W) // 2
        t = (h2 - H) // 2
        out.append(cc.crop((l, t, l + W, t + H)))
    return np.stack([np.asarray(c, np.float32) for c in out], axis=2)


# ---------------------------------------------------------------- komposisi
def compose(bg_rgb, layers, frame_i=0, exposure=1.12):
    """layers = [(depth, rgba uint8 HxWx4, dof_px, haze 0..1), ...] dekat→jauh
    atau jauh→dekat sesuai urutan; di sini urutan diberikan jauh→dekat."""
    out = bg_rgb.astype(np.float32).copy()
    for depth, arr, dof, haze, haze_col in layers:
        a = arr.astype(np.float32)
        if dof > 0.4:
            a[:, :, :3] = blur_img(a[:, :, :3], dof)
            a[:, :, 3] = blur_img(a[:, :, 3:4].repeat(3, axis=2), dof)[:, :, 0]
        if haze > 0:
            hc = np.array(haze_col, np.float32)[None, None, :]
            a[:, :, :3] = a[:, :, :3] * (1 - haze) + hc * haze
        out = over(out, a)
    out = bloom(out, strength=0.40)
    out = chroma(out, 0.0011)
    out = grade(out, frame_i, exposure=exposure)
    return (out * 255).astype(np.uint8)
