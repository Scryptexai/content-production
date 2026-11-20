#!/usr/bin/env python3
"""Retime case_cfg.py + bed_andes.py ke beat start baru hasil build_vo.py.

Peta linear per segmen antar anchor beat lama → baru; boundary yang sama
(selalu ada di titik beat) selalu menghasilkan nilai sama → SHOTS tetap kontigu.
"""
from pathlib import Path

OLD = [0.00, 10.04, 21.23, 38.55, 57.10, 81.33, 102.79, 115.46, 133.69, 156.24, 169.91, 174.00]
NEW = [0.00, 10.04, 19.77, 37.79, 56.35, 80.57, 102.03, 114.70, 132.93, 155.46, 169.12, 173.21]


def m(t):
    for i in range(len(OLD) - 1):
        if t <= OLD[i + 1] + 1e-9:
            f = (t - OLD[i]) / (OLD[i + 1] - OLD[i])
            return round(NEW[i] + f * (NEW[i + 1] - NEW[i]), 2)
    return t


CASE = Path(__file__).resolve().parent
cc = (CASE / "case_cfg.py").read_text()
bed = (CASE / "bed_andes.py").read_text()

# ── case_cfg: SHOTS + OVL (dua angka pertama tiap tuple), hanya baris data
import re

def retuple(text, header):
    out, in_sec = [], False
    for line in text.splitlines():
        if line.startswith(header):
            in_sec = True
        elif in_sec and line.startswith("]"):
            in_sec = False
        if in_sec:
            mm = re.match(r"^(\s*\()(\d+\.\d+)(,\s+)(\d+\.\d+)(,.*)$", line)
            if mm:
                line = f"{mm.group(1)}{m(float(mm.group(2))):.2f}{mm.group(3)}{m(float(mm.group(4))):.2f}{mm.group(5)}"
        out.append(line)
    return "\n".join(out) + "\n"

cc = retuple(cc, "SHOTS = [")
cc = retuple(cc, "OVL = [")
cc = cc.replace("END = 174.00", "END = 173.21")
cc = cc.replace("Durasi VO 169,91 s; END 174,00 s (kartu penutup 4,1 s).",
                "Durasi VO 169,12 s; END 173,21 s (kartu penutup 4,1 s).")
# komentar rentang beat ikut diperbarui (cosmetic)
for a, b in zip(OLD, OLD[1:]):
    ca = f"({a:.2f}".replace(".", ",")
    cb = f"{b:.2f})".replace(".", ",")
    na = f"({m(a):.2f}".replace(".", ",")
    nb = f"{m(b):.2f})".replace(".", ",")
    cc = cc.replace(ca + "–" + cb, na + "–" + nb)

# teks overlay: opsi wajar + perjelas gunung
cc = cc.replace("PASTI KALIAN CARI DAUN & AKAR", "PASTI KALIAN CARI BUAH-BUAHAN")
cc = cc.replace("HARI DI GUNUNG", "HARI DI ANDES")

# ── bed_andes: hit/riser/dip + END
bed = bed.replace("END = 174.00", "END = 173.21")
bed = bed.replace("hit(21.23,", f"hit({m(21.23):.2f},")
bed = bed.replace("hit(38.55,", f"hit({m(38.55):.2f},")
bed = bed.replace("riser(53.00, 57.10,", f"riser({m(53.00):.2f}, {m(57.10):.2f},")
bed = bed.replace("hit(57.10,", f"hit({m(57.10):.2f},")
bed = bed.replace("hit(81.33,", f"hit({m(81.33):.2f},")
bed = bed.replace("hit(102.79,", f"hit({m(102.79):.2f},")
bed = bed.replace("riser(129.00, 133.69,", f"riser({m(129.00):.2f}, {m(133.69):.2f},")
bed = bed.replace("hit(133.69,", f"hit({m(133.69):.2f},")
bed = bed.replace("hit(156.24,", f"hit({m(156.24):.2f},")
bed = bed.replace("dip(169.91, 174.00,", f"dip({m(169.91):.2f}, {m(174.00):.2f},")

(CASE / "case_cfg.py").write_text(cc)
(CASE / "bed_andes.py").write_text(bed)

# ── verifikasi: import case_cfg, cek kontigu & rentang
import importlib.util
spec = importlib.util.spec_from_file_location("case_cfg", CASE / "case_cfg.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
prev = 0.0
for s, e, *_ in mod.SHOTS:
    assert abs(s - prev) < 1e-6, f"tidak kontigu: {s} vs {prev}"
    assert e > s, f"durasi negatif {s}-{e}"
    prev = e
assert abs(prev - mod.END) < 1e-6, f"SHOTS end {prev} != END {mod.END}"
for a, b, *_ in mod.OVL:
    assert 0 <= a < b <= mod.END + 1e-6, f"OVL rentang salah {a}-{b}"
print(f"OK: {len(mod.SHOTS)} shots kontigu 0→{mod.END}, {len(mod.OVL)} OVL valid")
print("beat baru:", NEW)
