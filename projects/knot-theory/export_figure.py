#!/usr/bin/env python3
"""export_figure.py — ekspor rig figur ke daftar gambar (draw list) JSON.

Kenapa diekspor, bukan digambar ulang di React: rig di cine.py/motion.py sudah
divalidasi (pijakan galat 0,00 px pada tiga geometri tangga). Menggambar ulang
di TypeScript berarti mengulang seluruh perhitungan IK dan berisiko regresi.

Yang diekspor adalah **primitif gambar** (garis menebal + lingkaran) di
koordinat panggung (world 1920x1080). Remotion tinggal menggambarnya sebagai
<line>/<circle> SVG, lalu lapis itu ikut transform parallax seperti lapis lain.

    python3 export_figure.py --out remotion/public/parallax/figure.json
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import cine
from cine import P, _dir, clamp, lerp, smooth
from motion import Climb

FPS = 30
DUR = 10.0
NF = int(FPS * DUR)

# panggung: koordinat layar 1920x1080 pada zoom 1
X0, Y0 = 430.0, 940.0
TREAD, RISER, NSTEP = 158.0, 54.0, 6
HFIG = 430.0
STEP_SEC = 1.15
T0 = 0.95
FIG = (9, 9, 14)          # siluet nyaris hitam, bukan hitam pekat


def climb_u(t):
    return clamp((t - T0) / STEP_SEC, 0.0, NSTEP)


def pose_at(clip, t):
    u = climb_u(t)
    if u >= NSTEP:
        tt = t - (T0 + NSTEP * STEP_SEC)
        k = smooth(clamp((tt - 1.2) / 1.4))
        p = clip.standing(NSTEP, t, raise_arm=0.22 * k)
        p.head = -12 - 18 * k
        return p
    return clip.pose(u, t)


def emit(p, out):
    """Ubah Pose jadi primitif gambar."""
    h = p.h
    sk = cine.skeleton(p)
    hip, chest = sk["hip"], sk["chest"]
    sd = sk["sd"]
    perp = (-sd[1], sd[0])
    col = "#%02x%02x%02x" % p.body

    def seg(a, b, r1, r2):
        out.append({"t": "seg", "x1": round(a[0], 2), "y1": round(a[1], 2),
                    "x2": round(b[0], 2), "y2": round(b[1], 2),
                    "r1": round(r1, 2), "r2": round(r2, 2), "c": col})

    def dot(p_, r):
        out.append({"t": "dot", "x": round(p_[0], 2), "y": round(p_[1], 2),
                    "r": round(r, 2), "c": col})

    # kaki: paha → betis → telapak
    rl = P["leg_r"] * h
    for hp, knee, ankle in sk["legs"]:
        seg(hp, knee, rl * 1.06, rl * 0.92)
        seg(knee, ankle, rl * 0.92, rl * 0.70)
        seg((ankle[0] - 0.016 * h, ankle[1] + 0.018 * h),
            (ankle[0] + 0.042 * h, ankle[1] + 0.018 * h),
            P["foot_r"] * h * 0.92, P["foot_r"] * h * 0.92)

    # torso sebagai poligon (masa tunggal, bukan tumpukan kapsul)
    hipw, shw = 0.052 * h, 0.078 * h
    out.append({"t": "poly", "c": col, "pts": [
        [round(hip[0] - hipw * perp[0], 2), round(hip[1] - hipw * perp[1], 2)],
        [round(hip[0] + hipw * perp[0], 2), round(hip[1] + hipw * perp[1], 2)],
        [round(chest[0] + shw * perp[0], 2), round(chest[1] + shw * perp[1], 2)],
        [round(chest[0] - shw * perp[0], 2), round(chest[1] - shw * perp[1], 2)],
    ]})
    dot(chest, 0.030 * h)

    # lengan
    ra = P["arm_r"] * h
    for s0, elbow, wrist in sk["arms"]:
        seg(s0, elbow, ra * 1.12, ra * 0.92)
        seg(elbow, wrist, ra * 0.92, ra * 0.74)
        dot(wrist, P["hand_r"] * h * 0.72)

    # selendang (follow-through)
    if p.scarf:
        a1, a2 = p.scarf
        d1 = _dir(a1)
        sx = chest[0] - sd[0] * 0.02 * h
        sy = chest[1] + 0.045 * h
        p1 = (sx + d1[0] * 0.080 * h, sy + d1[1] * 0.080 * h)
        d2 = _dir(a1 + a2)
        p2 = (p1[0] + d2[0] * 0.070 * h, p1[1] + d2[1] * 0.070 * h)
        seg((sx, sy), p1, 0.019 * h, 0.015 * h)
        seg(p1, p2, 0.015 * h, 0.010 * h)

    # leher + kepala
    seg(chest, sk["neck"], 0.032 * h, 0.032 * h)
    hc, hd = sk["head"], sk["hd"]
    out.append({"t": "ell", "x": round(hc[0], 2), "y": round(hc[1], 2),
                "rx": round(P["head_r"] * h * 0.98, 2),
                "ry": round(P["head_r"] * h * 1.06, 2), "c": col})
    if p.hair:
        out.append({"t": "ell",
                    "x": round(hc[0] - hd[0] * 0.026 * h, 2),
                    "y": round(hc[1] - hd[1] * 0.010 * h, 2),
                    "rx": round(P["head_r"] * h * 1.00, 2),
                    "ry": round(P["head_r"] * h * 0.70, 2), "c": col})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="remotion/public/parallax/figure.json")
    a = ap.parse_args()

    clip = Climb(X0, Y0, TREAD, RISER, NSTEP, HFIG)
    frames = []
    for i in range(NF):
        t = i / FPS
        p = pose_at(clip, t)
        p.body = FIG
        p.hair = 1
        draw = []
        emit(p, draw)
        sk = cine.skeleton(p)
        sole = max(ax[1] + cine.sole_offset(p.h) for _, _, ax in sk["legs"])
        frames.append({
            "i": i,
            "hip": [round(sk["hip"][0], 2), round(sk["hip"][1], 2)],
            "head": [round(sk["head"][0], 2), round(sk["head"][1], 2)],
            "sole": round(sole, 2),
            "draw": draw,
        })

    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "fps": FPS, "frames": NF,
        "stage": {"w": 1920, "h": 1080,
                  "x0": X0, "y0": Y0, "tread": TREAD, "riser": RISER, "n": NSTEP,
                  "h": HFIG},
        "poses": frames,
    }
    out.write_text(json.dumps(payload, separators=(",", ":")))
    print(f"figur → {out}  ({out.stat().st_size/1024:.0f} KB, {NF} frame)")

    # QC pijakan tetap dipertahankan: telapak harus menyentuh tapak tangga
    # QC jujur: untuk TIAP telapak, cari anak tangga di bawahnya sendiri,
    # lalu ambil galat terkecil (kaki penopang). Bukan rata-rata, bukan pinggul.
    worst = 0.0
    for f in frames:
        errs = []
        for d in f["draw"]:
            if d["t"] == "seg" and abs(d["y1"] - d["y2"]) < 2.0 and d["r1"] > 8:
                x, y = d["x1"], d["y1"] + d["r1"]      # dasar telapak
                step = max(0, min(NSTEP, int(round((x - X0) / TREAD))))
                errs.append(abs(y - (Y0 - step * RISER)))
        if errs:
            worst = max(worst, min(errs))
    print(f"QC: galat kaki penopang vs permukaan (maks) = {worst:.1f} px")


if __name__ == "__main__":
    main()
