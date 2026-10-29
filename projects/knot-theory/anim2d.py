#!/usr/bin/env python3
"""Engine animasi 2D ber-rig untuk video Knot Theory.

Yang digambar bukan teks: karakter manusia abstrak yang benar-benar di-rig
(tulang belakang, lengan, kaki punya sudut), lalu dianimasikan — berjalan,
menunjuk, mengangkat, memanjat tangga, duduk, terkulai. Ditambah properti
adegan (meja, kolom data, tangga, pintu, frame) dan kamera yang bergerak.

Prinsip gaya:
  - siluet tebal dengan ujung membulat (capsule), bukan garis tipis
  - palet gelap: ink di belakang, krem di depan, rose/sage sebagai aksen
  - kedalaman atmosferik: yang jauh lebih pudar dan lebih kecil
  - glow lembut di sumber cahaya
"""
import math

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

W, H = 960, 540
SS = 2                      # supersampling
INK = (10, 13, 21)
INK2 = (18, 23, 34)
CREAM = (239, 231, 220)
ROSE = (217, 142, 115)
SAGE = (143, 169, 139)
LILAC = (167, 155, 200)
MUTED = (122, 132, 150)


# ------------------------------------------------------------------ utilitas
def clamp(v, a=0.0, b=1.0):
    return max(a, min(b, v))


def ease_in_out(t):
    t = clamp(t)
    return t * t * (3 - 2 * t)


def ease_out(t):
    t = clamp(t)
    return 1 - (1 - t) ** 3


def ease_in(t):
    t = clamp(t)
    return t ** 3


def lerp(a, b, t):
    return a + (b - a) * t


def seg(t, t0, t1):
    """0 sebelum t0, 1 sesudah t1, halus di antaranya."""
    if t1 <= t0:
        return 1.0 if t >= t1 else 0.0
    return ease_in_out((t - t0) / (t1 - t0))


def fog(color, depth):
    """depth 0 (dekat) .. 1 (jauh)"""
    d = clamp(depth)
    return tuple(int(c * (1 - 0.72 * d) + INK[i] * 0.72 * d) for i, c in enumerate(color))


# ------------------------------------------------------------------ kanvas
class Canvas:
    """Kanvas dengan kamera (geser + zoom) dan transform dunia→layar."""

    def __init__(self):
        self.img = Image.new("RGB", (W * SS, H * SS), INK)
        self.d = ImageDraw.Draw(self.img)
        self.cx = W * SS / 2
        self.cy = H * SS / 2
        self.zoom = 1.0
        self.ox = 0.0
        self.oy = 0.0
        self.glow_layer = Image.new("RGB", (W, H), (0, 0, 0))
        self.gd = ImageDraw.Draw(self.glow_layer)

    # kamera
    def cam(self, zoom=1.0, ox=0.0, oy=0.0):
        self.zoom = zoom
        self.ox, self.oy = ox, oy

    def p(self, x, y):
        """titik dunia (960x540, titik pusat) → piksel kanvas."""
        sx = (x - self.cx / SS + self.ox) * self.zoom + self.cx / SS
        sy = (y - self.cy / SS + self.oy) * self.zoom + self.cy / SS
        return (sx * SS, sy * SS)

    def s(self, v):
        return v * self.zoom * SS

    # bentuk
    def rect(self, x, y, w, h, fill, radius=0, outline=None, width=1):
        a = self.p(x, y)
        b = self.p(x + w, y + h)
        box = [min(a[0], b[0]), min(a[1], b[1]), max(a[0], b[0]), max(a[1], b[1])]
        r = max(0, min(self.s(radius), (box[2] - box[0]) / 2, (box[3] - box[1]) / 2))
        if r > 0:
            self.d.rounded_rectangle(box, radius=r, fill=fill, outline=outline,
                                     width=int(self.s(width)) if outline else 0)
        else:
            self.d.rectangle(box, fill=fill, outline=outline,
                             width=int(self.s(width)) if outline else 0)

    def circle(self, x, y, r, fill=None, outline=None, width=1):
        c = self.p(x, y)
        rr = self.s(r)
        box = [c[0] - rr, c[1] - rr, c[0] + rr, c[1] + rr]
        self.d.ellipse(box, fill=fill, outline=outline,
                       width=int(self.s(width)) if outline else 0)

    def capsule(self, x1, y1, x2, y2, r, fill):
        a, b = self.p(x1, y1), self.p(x2, y2)
        rr = max(1, self.s(r))
        self.d.line([a, b], fill=fill, width=int(rr * 2))
        for pt in (a, b):
            self.d.ellipse([pt[0] - rr, pt[1] - rr, pt[0] + rr, pt[1] + rr], fill=fill)

    def poly(self, pts, fill, outline=None, width=1):
        pp = [self.p(x, y) for x, y in pts]
        self.d.polygon(pp, fill=fill, outline=outline,
                       width=int(self.s(width)) if outline else 0)

    def line(self, pts, fill, width=2):
        pp = [self.p(x, y) for x, y in pts]
        self.d.line(pp, fill=fill, width=max(1, int(self.s(width))), joint="curve")

    # glow (resolusi rendah supaya cepat)
    def glow(self, x, y, r, color, strength=0.7):
        c = self.p(x, y)
        rr = max(2, int(self.s(r) / SS))
        cx, cy = int(c[0] / SS), int(c[1] / SS)
        self.gd.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=color)
        self._glow_ops.append((strength,))

    def begin(self):
        self.img = Image.new("RGB", (W * SS, H * SS), INK)
        self.d = ImageDraw.Draw(self.img)
        self.glow_layer = Image.new("RGB", (W, H), (0, 0, 0))
        self.gd = ImageDraw.Draw(self.glow_layer)
        self._glow_ops = []

    def finish(self):
        img = self.img
        if self._glow_ops:
            g = self.glow_layer.filter(ImageFilter.GaussianBlur(14))
            g = g.resize(img.size, Image.BILINEAR)
            img = Image.blend(img, Image.blend(img, g, 0.0), 0.0)  # placeholder
            arr = np.asarray(img, np.float32) + np.asarray(g, np.float32) * 0.9
            img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
        return img.resize((W, H), Image.LANCZOS)


# ------------------------------------------------------------------ karakter
class Pose:
    """Sudut dalam derajat, 0 = mengarah ke bawah, positif = searah jarum jam."""

    __slots__ = ("x", "y", "spine", "arm_l", "elbow_l", "arm_r", "elbow_r",
                 "hip_l", "knee_l", "hip_r", "knee_r", "head", "scale")

    def __init__(self, x=0.0, y=0.0):
        self.x, self.y = x, y
        self.spine = 0.0
        self.arm_l = 8.0
        self.elbow_l = 6.0
        self.arm_r = -8.0
        self.elbow_r = 6.0
        self.hip_l = 4.0
        self.knee_l = 3.0
        self.hip_r = -4.0
        self.knee_r = 3.0
        self.head = 0.0
        self.scale = 1.0


def _dir(deg):
    """arah untuk sudut: 0 = bawah, 90 = kanan."""
    r = math.radians(deg)
    return math.sin(r), math.cos(r)


L = dict(torso=31.0, neck=4.8, head=10.2, upper=17.5, fore=16.0,
         thigh=19.0, shin=18.5, r_limb=4.7, r_leg=5.3, r_torso=8.4)


CLOTHES = [CREAM, (198, 204, 214), SAGE, (206, 176, 152), LILAC, (176, 186, 198)]


def clothes(i):
    return CLOTHES[i % len(CLOTHES)]


def draw_person(c: Canvas, pose: Pose, body=CREAM, depth=0.0, alpha=1.0,
                arm_far=None, leg_far=None, style=0):
    """Gambar satu karakter. `arm_far`/`leg_far` = warna anggota badan sisi jauh
    (dipakai untuk memberi kesan kedalaman: lebih gelap)."""
    s = pose.scale
    k = lambda v: v * s
    hip = (pose.x, pose.y)
    sd = _dir(pose.spine)
    chest = (hip[0] + sd[0] * k(L["torso"]), hip[1] - sd[1] * k(L["torso"]))

    col = body if alpha >= 0.999 else tuple(int(lerp(INK[i], body[i], alpha)) for i in range(3))
    col = fog(col, depth)
    far = arm_far or tuple(int(x * 0.62) for x in col)
    far = fog(far, depth + 0.05)

    # kaki
    hip_shift = 2.2 * s
    for side, (ha, ka, c_leg) in enumerate((
            (pose.hip_r, pose.knee_r, far), (pose.hip_l, pose.knee_l, col))):
        h = (hip[0] + (-hip_shift if side else hip_shift), hip[1])
        dd = _dir(ha)
        knee = (h[0] + dd[0] * k(L["thigh"]), h[1] + dd[1] * k(L["thigh"]))
        dd2 = _dir(ha + ka)
        ankle = (knee[0] + dd2[0] * k(L["shin"]), knee[1] + dd2[1] * k(L["shin"]))
        c.capsule(h[0], h[1], knee[0], knee[1], k(L["r_leg"]), c_leg)
        c.capsule(knee[0], knee[1], ankle[0], ankle[1], k(L["r_leg"]) * 0.86, c_leg)
        c.capsule(ankle[0] - 2.0 * s, ankle[1], ankle[0] + 3.4 * s, ankle[1],
                  k(L["r_leg"]) * 0.8, c_leg)

    # torso
    c.capsule(hip[0], hip[1], chest[0], chest[1], k(L["r_torso"]), col)

    # lengan
    sh = (chest[0], chest[1] + 2.0 * s)
    for aa, ea, c_arm, dx in ((pose.arm_r, pose.elbow_r, far, -2.0),
                              (pose.arm_l, pose.elbow_l, col, 2.0)):
        s0 = (sh[0] + dx * s, sh[1])
        dd = _dir(aa)
        elbow = (s0[0] + dd[0] * k(L["upper"]), s0[1] + dd[1] * k(L["upper"]))
        dd2 = _dir(aa + ea)
        wrist = (elbow[0] + dd2[0] * k(L["fore"]), elbow[1] + dd2[1] * k(L["fore"]))
        c.capsule(s0[0], s0[1], elbow[0], elbow[1], k(L["r_limb"]), c_arm)
        c.capsule(elbow[0], elbow[1], wrist[0], wrist[1], k(L["r_limb"]) * 0.9, c_arm)
        c.circle(wrist[0], wrist[1], k(L["r_limb"]) * 1.05, fill=c_arm)

    # kepala
    hd = _dir(pose.spine + pose.head)
    neck = (chest[0] + hd[0] * k(L["neck"]), chest[1] - hd[1] * k(L["neck"]))
    c.capsule(chest[0], chest[1], neck[0], neck[1], k(2.9), col)
    head = (neck[0] + hd[0] * k(L["head"] * 0.88), neck[1] - hd[1] * k(L["head"] * 0.88))
    r = k(L["head"])
    c.circle(head[0], head[1], r, fill=col)
    # variasi siluet supaya bukan barisan orang identik
    if style == 1:      # kuncir
        c.capsule(head[0] - hd[0] * r * 0.9, head[1] + r * 0.9,
                  head[0] - hd[0] * r * 1.7, head[1] + r * 2.0, r * 0.34, col)
    elif style == 2:    # rambut pendek / helm
        c.circle(head[0], head[1] - r * 0.30, r * 0.94, fill=col)
        c.rect(head[0] - r * 1.05, head[1] - r * 0.35, r * 2.1, r * 0.7, fill=col, radius=r * 0.35)
    elif style == 3:    # bahu lebar (jaket)
        c.capsule(chest[0] - k(4.5), chest[1] + k(1.5), chest[0] + k(4.5), chest[1] + k(1.5),
                  k(3.4), col)
    return head


# ------------------------------------------------------------------ gerak
def walk_pose(phase, x, y, speed=1.0, scale=1.0):
    """Siklus jalan; phase dalam radian."""
    p = Pose(x, y)
    p.scale = scale
    sw = math.sin(phase)
    p.hip_l = 26 * sw * speed
    p.knee_l = 34 * max(0, -math.sin(phase - 0.7)) + 4
    p.hip_r = -26 * sw * speed
    p.knee_r = 34 * max(0, math.sin(phase - 0.7)) + 4
    p.arm_l = -22 * sw * speed
    p.elbow_l = 16 + 10 * max(0, sw)
    p.arm_r = 22 * sw * speed
    p.elbow_r = 16 + 10 * max(0, -sw)
    p.spine = 3 + 1.6 * math.sin(phase * 2)
    p.head = -2
    p.y = y - abs(math.sin(phase)) * 1.6 * scale
    return p


def idle_pose(t, x, y, scale=1.0, breathe=1.0):
    p = Pose(x, y)
    p.scale = scale
    b = math.sin(t * 1.6) * breathe
    p.spine = 1.5 + 0.8 * b
    p.arm_l = 10 + 2 * b
    p.arm_r = -10 - 2 * b
    p.elbow_l = 8
    p.elbow_r = 8
    p.head = 1.5 * b
    p.y = y + 0.7 * b
    return p


def point_pose(t, x, y, reach=1.0, scale=1.0, arm_deg=100):
    p = idle_pose(t, x, y, scale, 0.7)
    p.arm_r = -arm_deg * reach
    p.elbow_r = 4 + 10 * (1 - reach)
    p.spine = -4 * reach
    p.head = -6 * reach
    return p


def slump_pose(t, x, y, amount=1.0, scale=1.0):
    p = Pose(x, y)
    p.scale = scale
    p.spine = 16 * amount + 1.2 * math.sin(t * 1.1)
    p.head = 14 * amount
    p.arm_l = 12 + 6 * amount
    p.arm_r = -12 - 6 * amount
    p.elbow_l = 10 + 16 * amount
    p.elbow_r = 10 + 16 * amount
    p.hip_l = 6
    p.hip_r = -6
    p.y = y + 2.5 * amount
    return p


def climb_pose(phase, x, y, scale=1.0):
    """Memanjat: satu kaki terangkat tinggi, lengan naik bergantian."""
    p = Pose(x, y)
    p.scale = scale
    sw = math.sin(phase)
    p.hip_l = 62 * max(0, sw) - 6
    p.knee_l = 58 * max(0, sw) + 6
    p.hip_r = 62 * max(0, -sw) - 6
    p.knee_r = 58 * max(0, -sw) + 6
    p.arm_l = -104 * max(0, sw) - 20
    p.elbow_l = 26
    p.arm_r = 104 * max(0, -sw) + 20
    p.elbow_r = 26
    p.spine = 10
    p.head = -10
    p.y = y - 1.2 * scale
    return p


def carry_pose(t, x, y, scale=1.0):
    p = Pose(x, y)
    p.scale = scale
    p.arm_l = 74
    p.elbow_l = -62
    p.arm_r = -74
    p.elbow_r = -62
    p.spine = 5
    p.head = 3
    p.hip_l = 8
    p.hip_r = -8
    return p
