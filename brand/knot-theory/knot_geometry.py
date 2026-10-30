#!/usr/bin/env python3
"""Geometri mark Knot Theory: trefoil (2,3) dengan over/under yang benar.

Kurva: x = sin t + 2 sin 2t, y = cos t - 2 cos 2t, z = -sin 3t.
z dipakai untuk memutuskan untaian mana yang lewat di atas pada tiap persilangan,
jadi ilusi anyaman bukan tebakan.

Keluaran: daftar subpath (polyline) siap digambar, dengan celah di persilangan
bawah selebar ~1,7x tebal garis.
"""
import math

SAMPLES = 2880


def curve(t):
    return (math.sin(t) + 2 * math.sin(2 * t),
            math.cos(t) - 2 * math.cos(2 * t),
            -math.sin(3 * t))


def _intersect(p1, p2, p3, p4):
    x1, y1 = p1; x2, y2 = p2; x3, y3 = p3; x4, y4 = p4
    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if abs(den) < 1e-12:
        return None
    ta = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
    tb = ((x1 - x3) * (y1 - y2) - (y1 - y3) * (x1 - x2)) / den
    if 0 <= ta <= 1 and 0 <= tb <= 1:
        return ta, tb
    return None


def crossings():
    pts = [curve(2 * math.pi * i / SAMPLES) for i in range(SAMPLES)]
    found = []
    for i in range(SAMPLES):
        a1, a2 = pts[i], pts[(i + 1) % SAMPLES]
        for j in range(i + 80, SAMPLES):
            if min(j - i, SAMPLES - (j - i)) < 80:
                continue
            b1, b2 = pts[j], pts[(j + 1) % SAMPLES]
            r = _intersect(a1[:2], a2[:2], b1[:2], b2[:2])
            if r:
                ta, _ = r
                found.append((2 * math.pi * (i + ta) / SAMPLES, 2 * math.pi * j / SAMPLES,
                              pts[j][2]))
    out = []
    for t1, t2, _ in sorted(found):
        if out and abs(t1 - out[-1][0]) < 0.08:
            continue
        out.append((t1, t2))
    return out


def strand_points(size, cx, cy, inset=0.055):
    """Titik kurva dalam piksel, diskalakan agar muat dalam kotak `size`."""
    raw = [curve(2 * math.pi * i / SAMPLES) for i in range(SAMPLES)]
    xs = [p[0] for p in raw]; ys = [p[1] for p in raw]
    span = max(max(xs) - min(xs), max(ys) - min(ys))
    scale = size * (1 - 2 * inset) / span
    mx = (max(xs) + min(xs)) / 2
    my = (max(ys) + min(ys)) / 2
    return [(cx + (x - mx) * scale, cy - (y - my) * scale) for x, y, _ in raw], scale


def build(size, cx, cy, stroke_px, inset=0.055):
    """Kembalikan (subpaths, crossings) — subpaths: list[list[(x, y)]]."""
    pts, scale = strand_points(size, cx, cy, inset)
    cross = crossings()

    under_idx = []
    for t1, t2 in cross:
        z1 = curve(t1)[2]; z2 = curve(t2)[2]
        t_under = t1 if z1 < z2 else t2
        under_idx.append(int(round(t_under / (2 * math.pi) * SAMPLES)) % SAMPLES)

    gap_px = 0.85 * stroke_px
    cut = [False] * SAMPLES
    for iu in under_idx:
        # jalan keluar dari titik persilangan sampai jarak gap_px
        for direction in (-1, 1):
            i = iu
            while True:
                j = (i + direction) % SAMPLES
                d = math.dist(pts[iu], pts[j])
                if d > gap_px or j == iu:
                    break
                cut[j] = True
                i = j
        cut[iu] = True

    subpaths, cur = [], []
    for i in range(SAMPLES):
        if cut[i]:
            if len(cur) > 1:
                subpaths.append(cur)
            cur = []
        else:
            cur.append(pts[i])
    if len(cur) > 1:
        subpaths.append(cur)
    # tutup kurva: satukan subpath pertama & terakhir bila titik 0 tidak terpotong
    if len(subpaths) > 1 and not cut[0]:
        subpaths = [subpaths[-1] + subpaths[0]] + subpaths[1:-1]
    return subpaths, cross


def svg_path(subpaths):
    return " ".join(
        "M " + " L ".join(f"{x:.2f},{y:.2f}" for x, y in sp) for sp in subpaths
    )


def simplify(points, tol=0.6):
    """Douglas-Peucker sederhana, untuk SVG yang ringan."""
    if len(points) < 3:
        return points

    def dp(pts):
        if len(pts) < 3:
            return pts
        (x1, y1), (x2, y2) = pts[0], pts[-1]
        dx, dy = x2 - x1, y2 - y1
        norm = math.hypot(dx, dy) or 1e-9
        idx, best = 0, -1.0
        for i in range(1, len(pts) - 1):
            x0, y0 = pts[i]
            dist = abs(dy * (x0 - x1) - dx * (y0 - y1)) / norm
            if dist > best:
                idx, best = i, dist
        if best > tol:
            left = dp(pts[:idx + 1])
            right = dp(pts[idx:])
            return left[:-1] + right
        return [pts[0], pts[-1]]

    return dp(points)
