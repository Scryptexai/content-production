#!/usr/bin/env python3
"""plan.py — perencana shot berbasis keyframe (diambil dari agnes-video-generator).

Kenapa ada file ini
-------------------
Dari kajian `docs/AGNES-REVIEW.md` §3, tiga teknik di sana bisa dipakai tanpa
API mereka. Salah satunya bukan kode, tapi **kontrak**: setiap shot ditulis
sebagai sepasang pose konkret (frame awal → frame akhir) plus gerak di
antaranya, dan frame akhir itu dipakai ulang sebagai frame awal shot berikutnya.

Kontrak itu yang memaksa "seleksi" dan "retargeting" terjadi SEBELUM render,
bukan setelah. Animator yang menggerakkan fungsi sinus terus-menerus tidak
pernah bisa menyambung shot; animator yang menulis dua pose per shot bisa.

Struktur
--------
    keyframes[ id ] = pose konkret (parameter klip, dalam satuan ruang)
    shots[ i ]     = {kf_from, kf_to, dur, framing, variation, cam}

Aturan yang divalidasi:
  R1  Rantai: kf_to shot i  ==  kf_from shot i+1  (tidak boleh yatim)
  R2  Variasi: nilai `variation` boleh berulang paling banyak dua kali
  R3  Framing: dua shot berturut tidak boleh sama persis
  R4  Durasi: 6–13 dtk per shot (long-form; lebih cepat terasa gelisah)
  R5  Shot pertama tiap babak = `large` (menetapkan tempat)

    python3 plan.py RW2-long --check
    python3 plan.py RW2-long --out shots/RW2-plan.json
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).parent

# ---------------------------------------------------------------------------
# Definisi keyframe: parameter diksi ruang, BUKAN sudut sendi.
# `u` = progres klip tangga (satuan anak tangga); `arm` = 0..1 (0 = lengan
# di samping, 1 = menjangkau penuh); `gaze` = kemiringan kepala ke atas.
# Karena semuanya ruang, satu pose bisa dipakai di figur 430px maupun 560px.
# ---------------------------------------------------------------------------
KEYFRAMES = {
    # --- babak 1: membuka dunia
    "kf_base":      dict(u=0.00, arm=0.10, gaze=0.00, note="berdiri di dasar tangga"),
    "kf_lift1":     dict(u=0.35, arm=0.45, gaze=0.10, note="kaki terangkat, tangan mulai naik"),
    "kf_land2":     dict(u=2.00, arm=0.35, gaze=0.10, note="tapak kedua"),
    # --- babak 2: kerja
    "kf_mid":       dict(u=3.00, arm=0.30, gaze=0.15, note="tengah tangga, ritme stabil"),
    "kf_mid_up":    dict(u=3.60, arm=0.60, gaze=0.20, note="menjangkau anak tangga berikut"),
    "kf_high":      dict(u=4.60, arm=0.25, gaze=0.30, note="hampir puncak"),
    "kf_high_up":   dict(u=5.20, arm=0.70, gaze=0.35, note="tarikan terakhir"),
    # --- babak 3: puncak
    "kf_top":       dict(u=6.00, arm=0.15, gaze=0.45, note="berdiri di pelataran puncak"),
    "kf_top_still": dict(u=6.00, arm=0.10, gaze=0.60, note="diam, menatap matahari"),
    "kf_top_open":  dict(u=6.00, arm=0.32, gaze=0.55, note="lengan sedikit terbuka"),
    "kf_end":       dict(u=6.00, arm=0.28, gaze=0.50, note="tahan, fade out"),
}


def shot(kf_from, kf_to, dur, framing, variation, cam, blok, isi):
    return dict(kf_from=kf_from, kf_to=kf_to, dur=dur, framing=framing,
                variation=variation, cam=cam, blok=blok, isi=isi)


# Rencana untuk RW2L (10 blok). 23 shot, ±207 dtk.
PLAN = [
    # blok 1 — membuka: dua shot `large` untuk menetapkan dunia
    shot("kf_base", "kf_lift1", 9, "wide", "large", "push-in lambat", "b1", "dunia: tangga tergantung, matahari"),
    shot("kf_lift1", "kf_land2", 10, "medium", "medium", "ikuti badan", "b1", "orang mulai naik"),

    # blok 2 — metode
    shot("kf_land2", "kf_mid", 10, "wide", "large", "tarik mundur", "b2", "tangga penuh terlihat"),
    shot("kf_mid", "kf_mid_up", 9, "close-feet", "small", "statis, fokus tapak", "b2", "tapak menempel, debu jatuh"),

    # blok 3 — angka
    shot("kf_mid_up", "kf_high", 11, "medium", "medium", "dorong masuk", "b3", "ritme naik stabil"),
    shot("kf_high", "kf_high_up", 9, "close-hand", "small", "statis", "b3", "tangan meraih tepi anak tangga"),

    # blok 4 — temuan 1
    shot("kf_high_up", "kf_top", 12, "wide", "large", "tarik mundur, buka langit", "b4", "puncak terlihat"),
    shot("kf_top", "kf_top_still", 10, "medium", "small", "dorong pelan", "b4", "berhenti, dada turun-naik"),

    # blok 5 — temuan 2
    shot("kf_top_still", "kf_top_open", 11, "close-upper", "medium", "statis", "b5", "siluet lawan matahari"),
    shot("kf_top_open", "kf_end", 9, "wide", "large", "tahan, jangan gerak", "b5", "ruang kosong di sekeliling"),

    # blok 6 — penjelasan
    shot("kf_end", "kf_top_open", 10, "medium", "small", "sangat lambat keluar", "b6", "kamera menjauh, figur mengecil"),
    shot("kf_top_open", "kf_top_still", 10, "close-feet", "medium", "statis", "b6", "tapak di batu, dua kaki rapat"),

    # blok 7 — kontrafaktual
    shot("kf_top_still", "kf_top_open", 11, "medium", "medium", "orbit kecil", "b7", "badan berputar sedikit"),
    shot("kf_top_open", "kf_end", 9, "close-upper", "small", "statis", "b7", "wajah siluet, tidak terlihat"),

    # blok 8 — kutipan
    shot("kf_end", "kf_top_open", 12, "wide", "large", "kembali ke lebar", "b8", "tangga + langit utuh"),
    shot("kf_top_open", "kf_top_still", 10, "medium", "small", "dorong", "b8", "diam"),

    # blok 9 — batas kejelasan
    shot("kf_top_still", "kf_end", 11, "close-feet", "medium", "statis", "b9", "pijakan: satu-satunya yang pasti"),
    shot("kf_end", "kf_end", 10, "wide", "large", "tarik jauh", "b9", "figur kecil, dunia besar"),

    # blok 10 — pertanyaan
    shot("kf_end", "kf_top_open", 10, "medium", "medium", "dorong terakhir", "b10", "kembali ke figur"),
    shot("kf_top_open", "kf_end", 9, "wide", "large", "tahan", "b10", "fade"),
]


def check(plan, kfs, verbose=True):
    errs, warns = [], []

    # R1 rantai keyframe
    for i in range(len(plan) - 1):
        if plan[i]["kf_to"] != plan[i + 1]["kf_from"]:
            errs.append(f"R1 shot {i+1}→{i+2}: kf_to={plan[i]['kf_to']} "
                        f"≠ kf_from={plan[i+1]['kf_from']}")

    # R2 variasi
    run = 1
    for i in range(1, len(plan)):
        run = run + 1 if plan[i]["variation"] == plan[i - 1]["variation"] else 1
        if run > 2:
            warns.append(f"R2 shot {i+1}: '{plan[i]['variation']}' 3x berturut")
    # R3 framing
    for i in range(1, len(plan)):
        if plan[i]["framing"] == plan[i - 1]["framing"]:
            warns.append(f"R3 shot {i}→{i+1}: framing sama ('{plan[i]['framing']}')")
    # R4 durasi
    for i, s in enumerate(plan):
        if not 6 <= s["dur"] <= 13:
            errs.append(f"R4 shot {i+1}: {s['dur']} dtk di luar 6–13")
    # R5 jarak variasi: jangan biarkan grammar membeku — minimal satu 'large'
    # dalam setiap rentang 5 shot, dan shot pertama episode wajib 'large'.
    if plan and plan[0]["variation"] != "large":
        errs.append("R5 shot 1: pembuka episode wajib 'large'")
    for i in range(len(plan)):
        window = plan[i:i + 5]
        if len(window) == 5 and not any(x["variation"] == "large" for x in window):
            warns.append(f"R5 shot {i+1}–{i+5}: tidak ada 'large' dalam 5 shot")

    # keyframe dipakai?
    used = {s["kf_from"] for s in plan} | {s["kf_to"] for s in plan}
    for k in kfs:
        if k not in used:
            warns.append(f"keyframe '{k}' tidak dipakai")
    for k in used:
        if k not in kfs:
            errs.append(f"keyframe '{k}' dirujuk tapi tidak ada")

    total = sum(s["dur"] for s in plan)
    if verbose:
        print(f"shot: {len(plan)} · total {total} dtk "
              f"({total/60:.1f} mnt) · {len(plan)/(total/60):.1f} shot/mnt")
        print(f"galat: {len(errs)} · peringatan: {len(warns)}")
        for e in errs:
            print("  ✗", e)
        for w in warns:
            print("  !", w)
        if not errs and not warns:
            print("  ✓ semua aturan lolos")
        print("\n%-3s %-6s %-11s %-9s %-4s %s" % ("#", "blok", "framing", "variation", "dtk", "isi"))
        for i, s in enumerate(plan):
            print("%-3d %-6s %-11s %-9s %-4d %s" % (
                i + 1, s["blok"], s["framing"], s["variation"], s["dur"], s["isi"]))
    return errs, warns, total


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("episode", nargs="?", default="RW2-long")
    ap.add_argument("--out", default=None)
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()

    errs, warns, total = check(PLAN, KEYFRAMES)

    payload = {
        "episode": a.episode,
        "totalSec": total,
        "keyframes": KEYFRAMES,
        "shots": PLAN,
        "rules": ["R1 rantai keyframe", "R2 variasi", "R3 framing",
                  "R4 durasi 6-13", "R5 buka babak dengan large"],
    }
    out = a.out or f"{a.episode}-plan.json"
    p = ROOT / out
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(payload, ensure_ascii=False, indent=2))
    print(f"\nrencana → {p}")
    raise SystemExit(1 if errs else 0)


if __name__ == "__main__":
    main()
