#!/usr/bin/env python3
"""export_joints.py — ekspor SENDI (bukan bentuk) untuk karakter Knot Theory.

Kenapa sendi, bukan gambar jadi
--------------------------------
`export_figure.py` mengekspor daftar primitif gambar (garis menebal) — cara itu
mengunci BENTUK karakter. Selama bentuk terkunci di JSON, karakter tidak bisa
di-redesign tanpa membuang seluruh data gerak yang sudah tervalidasi.

File ini memisahkan dua hal yang memang berbeda:

    rig + IK  →  sendi tiap frame  (file ini, Python, sudah divalidasi)
    bentuk    →  cara menggambar sendi itu (JS/SVG, bebas diganti kapan saja)

Karena itu desain ulang karakter cukup mengubah `film/char/character.js`.
Pijakan kaki tetap 0,00 px karena posisi telapak datang dari IK, bukan dari
gaya gambar.

Keluaran: film/assets/char-joints.json

    python3 film/char/export_joints.py

Klip yang diekspor
------------------
    climb   memanjat 6 anak tangga (dipakai scene The Climb)
    walk    jalan di tanah datar, dipakai ulang untuk semua scene lain
    idle    berdiri, napas + ayun pandang (untuk close-up)
    reach   mengulurkan tangan dan mengikat simpul (interaksi dengan diagram)
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent     # projects/knot-theory
sys.path.insert(0, str(ROOT))

import cine                                        # noqa: E402
from cine import P, Pose, _dir, clamp, lerp, smooth  # noqa: E402
from motion import Climb, apply_foot_targets       # noqa: E402

FPS = 30
HFIG = 430.0

# Geometri tangga — WAJIB sama dengan scenes/climb/index.html dan export_figure.py
X0, Y0 = 430.0, 940.0
TREAD, RISER, NSTEP = 158.0, 54.0, 6
STEP_SEC = 1.15
T0 = 0.95

OUT = HERE.parent / "assets" / "char-joints.json"


# ------------------------------------------------------------------ util
def ease(q, kind="inout"):
    q = clamp(q)
    if kind == "snap":
        return 1 - (1 - q) ** 4
    if kind == "out":
        return 1 - (1 - q) ** 3
    if kind == "in":
        return q ** 3
    if kind == "back":
        s = 1.70158
        return 1 + (s + 1) * (q - 1) ** 3 + s * (q - 1) ** 2
    return q * q * (3 - 2 * q)


def keys(t, table):
    """Interpolasi tabel [(t, nilai, easing?)] — nilai boleh skalar."""
    if t <= table[0][0]:
        return table[0][1]
    for (ta, va, *ea), (tb, vb, *eb) in zip(table, table[1:]):
        if t <= tb:
            k = eb[0] if eb else "inout"
            q = ease((t - ta) / (tb - ta), k)
            return lerp(va, vb, q)
    return table[-1][1]


# ------------------------------------------------------------------ klip
def climb_pose(clip, t):
    """Sama persis dengan pose_at() di export_figure.py — jangan diubah."""
    u = clamp((t - T0) / STEP_SEC, 0.0, NSTEP)
    if u >= NSTEP:
        tt = t - (T0 + NSTEP * STEP_SEC)
        k = smooth(clamp((tt - 1.2) / 1.4))
        p = clip.standing(NSTEP, t, raise_arm=0.22 * k)
        p.head = -12 - 18 * k
        return p, 0.35
    p = clip.pose(u, t)
    return p, 0.15


def flat_walk_pose(clip, t):
    """Jalan di tanah datar. Fase langkah sama dengan klip tangga, jadi
    geraknya konsisten di seluruh film (satu karakter, satu cara berjalan).

    Lengan di sini TIDAK boleh memakai lengan klip tangga: klip tangga
    mengulurkan tangan ke atas untuk meraih anak tangga, dan kalau dipakai
    untuk berjalan hasilnya terbaca seperti orang meraba. Jadi ayunan lengan
    diturunkan dari fase langkah: berlawanan dengan kaki."""
    u = clamp((t - 0.30) / 0.98, 0.0, 200)
    p = clip.pose(u, t)
    ph = u - int(u)
    swing = math.sin(2 * math.pi * clamp((ph - 0.10) / 0.82))   # +1 = kaki depan maju
    p.spine = 3.0
    p.head = -3.0
    # Ayunan lengan: depan berlawanan arah kaki, belakang sebaliknya.
    # Siku SELALU menekuk ke arah yang sama (negatif untuk lengan belakang),
    # kalau tidak siku terlihat patah.
    p.arm_l = 20 - 26 * swing
    p.elbow_l = 16 + 12 * abs(swing)
    p.arm_r = -20 - 26 * swing
    p.elbow_r = -(16 + 12 * abs(swing))
    p.coat = -0.4 * swing
    p.scarf = (250 + 4 * swing, 18 + 6 * math.sin(t * 2.2))
    return p, 0.30 + 0.10 * swing


def idle_pose(clip, t):
    """Berdiri. Napas 3,4 dtk, pandangan menyapu pelan, bahu ikut turun-naik
    sedikit. Semua di bawah 2% tinggi badan — kalau lebih, terbaca goyang."""
    br = math.sin(2 * math.pi * t / 3.4)
    sc = math.sin(2 * math.pi * t / 5.1)
    p = clip.standing(0, t)
    p.spine = 1.0 + 1.7 * br
    p.head = -11 + 3.2 * sc
    p.arm_r, p.elbow_r = -12 + 2.0 * br, 16 - 1.5 * br
    p.arm_l, p.elbow_l = 12 - 2.0 * br, 18 + 1.5 * br
    apply_foot_targets(p)
    return p, 0.55 * sc + 0.15


def tie_pose(clip, t):
    """Berdiri di PUNCAK tangga dan mengikat benang.

    Berbeda dari reach_pose: kaki sudah di tapak ke-6 (bukan di lantai), dan
    geraknya tiga tahap — angkat tangan, pegang, tarik. Dipakai untuk bidikan
    penutup, jadi tidak boleh ada gerak yang tidak perlu.
    """
    lift = keys(t, [(0.0, 0.0), (0.35, 1.0, "out")])
    arm = keys(t, [(0.0, 8.0), (0.30, -12.0, "out"), (0.85, 62.0, "back"),
                   (1.55, 68.0), (2.15, 54.0), (2.60, 40.0)])
    elbow = keys(t, [(0.0, 8.0), (0.30, 4.0), (0.85, 62.0, "back"),
                     (1.55, 58.0), (2.15, 44.0), (2.60, 30.0)])
    # tarikan kecil berulang saat mengencangkan simpul
    tug = 6.0 * math.sin(2 * math.pi * clamp((t - 1.5) / 1.1) * 2.0) if 1.5 < t < 2.6 else 0.0
    lean = keys(t, [(0.0, 2.0), (0.3, -1.0), (0.85, 7.0), (1.6, 8.0), (2.6, 4.0)])
    gaze = keys(t, [(0.0, 0.1), (0.3, -0.1), (0.85, 0.85), (2.2, 0.9), (2.6, 0.6)])

    p = clip.standing(NSTEP, t, raise_arm=0.18 * lift)
    p.spine = lean
    p.head = -12 + 8 * gaze
    p.arm_l = arm + tug
    p.elbow_l = elbow - tug * 0.8
    p.arm_r = 10 - 4 * lift
    p.elbow_r = -8
    p.scarf = (250 + 5 * math.sin(t * 1.6), 18 + 6 * math.sin(t * 2.0))
    apply_foot_targets(p)
    return p, gaze


def reach_pose(clip, t):
    """Mengulur tangan ke depan-atas lalu menarik benang. Dipakai untuk bidikan
    interaksi: tangan karakter menyentuh node diagram, bukan sekadar menunjuk."""
    arm = keys(t, [(0.0, 5.0), (0.45, -14.0, "out"), (1.05, 56.0, "back"),
                   (1.65, 60.0), (2.30, 20.0, "inout"), (3.00, 5.0)])
    # putaran pergelangan: gerak memutar kecil saat mengikat
    stir = 9.0 * math.sin(2 * math.pi * clamp((t - 1.05) / 1.25) * 2.0) if 1.05 < t < 2.30 else 0.0
    elbow = keys(t, [(0.0, 8.0), (0.45, 2.0), (1.05, 78.0, "back"),
                     (1.65, 82.0), (2.30, 40.0), (3.00, 8.0)])
    lean = keys(t, [(0.0, 1.0), (0.45, -1.5), (1.05, 6.5), (1.65, 7.0),
                    (2.30, 2.0), (3.00, 1.0)])
    gaze = keys(t, [(0.0, 0.2), (0.45, -0.2), (1.05, 0.9), (2.30, 0.8), (3.00, 0.2)])
    p = clip.standing(0, t)
    p.spine = lean
    p.head = -12 + 9 * gaze
    p.arm_l = arm + stir * 0.55
    p.elbow_l = elbow - stir
    p.arm_r = 6.0 - 3.0 * (lean - 1.0) / 6.0
    p.elbow_r = 8.0
    apply_foot_targets(p)
    return p, gaze


# ------------------------------------------------------------------ bentuk
def frame_of(p, gaze, t):
    """Satu frame = sendi dalam koordinat dunia + data yang dibutuhkan
    penggambar (arah hadap, tinggi badan, fase)."""
    sk = cine.skeleton(p)
    h = p.h
    # artefak gulir badan: dipakai untuk rambut/kain yang tertinggal
    return {
        "h": round(h, 1),
        "hip": [round(v, 2) for v in sk["hip"]],
        "chest": [round(v, 2) for v in sk["chest"]],
        "neck": [round(v, 2) for v in sk["neck"]],
        "head": [round(v, 2) for v in sk["head"]],
        "hd": [round(sk["hd"][0], 4), round(sk["hd"][1], 4)],
        "armR": [[round(v, 2) for v in q] for q in sk["arms"][0]],
        "armL": [[round(v, 2) for v in q] for q in sk["arms"][1]],
        "legR": [[round(v, 2) for v in q] for q in sk["legs"][0]],
        "legL": [[round(v, 2) for v in q] for q in sk["legs"][1]],
        "gaze": round(float(gaze), 3),
    }


def build(name, fn, dur, clip, n=None):
    n = n or int(round(dur * FPS))
    out = []
    for i in range(n):
        t = i / FPS
        p, gaze = fn(clip, t)
        out.append(frame_of(p, gaze, t))
    return {"frames": n, "poses": out}


def main():
    climb = Climb(X0, Y0, TREAD, RISER, NSTEP, HFIG)
    flat = Climb(X0 - 150.0, Y0, 196.0, 0.0, 200, HFIG, lift=54.0)

    clips = {
        "climb": build("climb", climb_pose, 12.0, climb),
        "walk": build("walk", flat_walk_pose, 12.0, flat),
        "idle": build("idle", idle_pose, 8.0, flat),
        "reach": build("reach", reach_pose, 3.0, flat),
        "tie": build("tie", tie_pose, 3.2, climb),
    }

    payload = {
        "fps": FPS,
        "unit": "px (dunia 1920x1080 pada zoom 1)",
        "note": "sendi saja; bentuk digambar oleh char/character.js",
        "clips": clips,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, separators=(",", ":")))
    for k, v in clips.items():
        print(f"  {k:6s} {v['frames']:4d} frame")
    print(f"→ {OUT}  ({OUT.stat().st_size / 1024:.0f} KB)")

    # QC pijakan. Metriknya HARUS sama dengan export_figure.py, kalau tidak
    # hasilnya menyesatkan: pada tiap frame ada kaki yang sedang melayang,
    # jadi yang dinilai adalah kaki PENOPANG = galat terkecil di frame itu,
    # lalu yang terburuk di seluruh klip.
    worst = 0.0
    for f in clips["climb"]["poses"]:
        errs = []
        for leg in (f["legR"], f["legL"]):
            ankle = leg[2]
            sole = ankle[1] + cine.sole_offset(HFIG)
            step = max(0, min(NSTEP, int(round((ankle[0] - X0) / TREAD))))
            errs.append(abs(sole - (Y0 - step * RISER)))
        worst = max(worst, min(errs))
    print(f"QC pijakan (klip climb, kaki penopang) = {worst:.3f} px")


if __name__ == "__main__":
    main()
