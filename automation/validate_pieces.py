#!/usr/bin/env python3
"""QC slate v2 (relationship): naskah utuh, struktur tidak berulang, label fakta ada.

Dipakai setelah menambah/mengubah naskah di content/relationship/pieces/.
Bukan pengganti validate.py (itu untuk kalender lama 35 konten × 3 platform).
"""
import json
import re
import sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "content/relationship"
idx = json.loads((BASE / "pieces.json").read_text(encoding="utf-8"))
pieces = idx["pieces"]
errs, warns = [], []

# --- 1. indeks ------------------------------------------------------------
if len(pieces) != 7:
    errs.append(f"indeks harus 7 naskah, ada {len(pieces)}")
for p in pieces:
    for k in ("ytTitle", "hookForm", "publishDate", "durationSec"):
        if not p.get(k):
            errs.append(f"{p['id']}: field indeks kosong {k}")

ids = [p["id"] for p in pieces]
if len(set(ids)) != len(ids):
    errs.append(f"id duplikat: {ids}")

start = date.fromisoformat(idx["meta"]["startDate"])
for i, p in enumerate(pieces, start=1):
    if p["day"] != i:
        errs.append(f"{p['id']}: day {p['day']} (harus {i})")
    want = start + timedelta(days=i - 1)
    if p["publishDate"] != want.isoformat():
        errs.append(f"{p['id']}: publishDate {p['publishDate']} (harus {want})")

# --- 2. struktur & hook tidak berulang ------------------------------------
structs = [p["structure"] for p in pieces]
for a, b in zip(structs, structs[1:]):
    if a == b:
        errs.append(f"struktur berulang berurutan: {a} → {b}")
if len(set(structs)) != len(structs):
    errs.append(f"struktur dipakai lebih dari sekali: {structs}")

hooks = [p["hookForm"] for p in pieces]
if len(set(hooks)) != len(hooks):
    errs.append(f"bentuk hook berulang: {hooks}")

terr = [p["territory"] for p in pieces]
if len(set(terr)) != len(terr):
    errs.append(f"wilayah primer berulang: {terr}")
expected = set("ABCDEFGHI")
missing = expected - set(terr) - {t for p in pieces for t in p["secondary"]}
if missing:
    warns.append(f"wilayah belum tersentuh sepanjang slate: {sorted(missing)}")

# --- 3. isi tiap naskah ---------------------------------------------------
BANNED = [
    "pernahkah kamu", "di dunia yang", "kita semua tahu", "jarang dibahas",
    "fakta mengejutkan", "tapi tunggu", "inilah twist", "let that sink in",
    "baca sampai habis", "simak baik-baik", "intinya adalah",
    "apa pelajarannya", "semoga bermanfaat", "jangan lupa follow",
    "para ahli sepakat", "banyak orang percaya", "di era modern ini",
    "red flag", "narsis", "toxic", "wajib punya", "auto bagus",
]

for p in pieces:
    f = BASE / "pieces" / p["file"]
    if not f.exists():
        errs.append(f"{p['id']}: file hilang {p['file']}")
        continue
    t = f.read_text(encoding="utf-8")
    low = t.lower()

    if not t.startswith("# " + p["id"]):
        errs.append(f"{p['id']}: judul H1 tidak diawali '{p['id']} —'")

    m = re.search(r"\| \*\*Target durasi\*\* \| (\d+)", t)
    if not m:
        errs.append(f"{p['id']}: baris Target durasi tidak ada")
    elif int(m.group(1)) != p["durationSec"]:
        errs.append(f"{p['id']}: durasi {m.group(1)} ≠ indeks {p['durationSec']}")

    for need, label in [
        ("## Kenapa ini layak", "bagian 'Kenapa ini layak'"),
        ("## Fact ledger", "fact ledger"),
        ("## Caption", "caption"),
        ("## Outline long-form", "outline long-form"),
        ("## Visual & audio", "catatan visual & audio"),
        ("Batas data", "batas data"),
        ("TIDAK-DIKETAHUI", "label TIDAK-DIKETAHUI"),
    ]:
        if need not in t:
            errs.append(f"{p['id']}: tidak ada {label}")

    if "FAKTA" not in t:
        errs.append(f"{p['id']}: tidak ada satu pun klaim berlabel FAKTA")
    if "TAFSIRAN-PENULIS" not in t:
        warns.append(f"{p['id']}: tidak memisahkan tafsiran penulis dari fakta")

    # sumber yang bisa dicek: doi, url, atau nama jurnal
    if not re.search(r"(doi\.org|https?://|\bQJE\b|\bJEEA\b|American Psychologist|"
                     r"Ostrom|Netting|IFLS|Garante|OJK|Survey Center|American Perspectives)", t):
        errs.append(f"{p['id']}: tidak ada sumber yang bisa dicek pembaca")

    # hook: tiga varian
    rows = re.findall(r"^\| ([ABC]) \|", t, re.M)
    if sorted(set(rows)) != ["A", "B", "C"]:
        errs.append(f"{p['id']}: varian hook tidak lengkap (A/B/C)")

    # platform
    for plat in ["**TikTok**", "**Instagram**"]:
        if plat not in t:
            errs.append(f"{p['id']}: caption {plat} tidak ada")
    yt = re.search(r"\*\*YouTube \(judul ≤ 60\)\*\*\n```\n(.+?)\n```", t, re.S)
    if not yt:
        errs.append(f"{p['id']}: judul YouTube tidak ada")
    else:
        jt = yt.group(1).strip()
        if len(jt) > 60:
            errs.append(f"{p['id']}: judul YouTube {len(jt)} karakter (>60)")
        if jt != p["ytTitle"]:
            warns.append(f"{p['id']}: judul YouTube di berkas ≠ indeks")

    # caption tidak boleh identik antar platform
    blocks = re.findall(r"\*\*(TikTok|Instagram)\*\*\n```\n(.+?)\n```", t, re.S)
    cap = {k: v.strip() for k, v in blocks}
    if len(cap) == 2:
        if cap["TikTok"] == cap["Instagram"]:
            errs.append(f"{p['id']}: caption TikTok = Instagram (tidak ada adaptasi)")
        if len(cap["TikTok"]) > 2200 or len(cap["Instagram"]) > 2200:
            errs.append(f"{p['id']}: caption > 2200 karakter")
        for k, v in cap.items():
            if "#" not in v:
                warns.append(f"{p['id']}: caption {k} tanpa hashtag")

    # frasa terlarang
    for b in BANNED:
        if b in low:
            errs.append(f"{p['id']}: frasa terlarang → '{b}'")

    # penutup tidak boleh merangkum (heuristik kasar: kata 'kesimpulannya/jadi intinya')
    for b in ["kesimpulannya,", "sebagai kesimpulan", "jadi intinya"]:
        if b in low:
            warns.append(f"{p['id']}: penutup terasa merangkum ('{b}')")

# --- 4. laporan -----------------------------------------------------------
for w in warns:
    print(f"· {w}")
if errs:
    print(f"\n✗ {len(errs)} masalah:")
    for e in errs:
        print("  -", e)
    sys.exit(1)

total = sum(p["durationSec"] for p in pieces)
print(f"✓ {len(pieces)} topik · {len(pieces) * 3} video "
      f"(1 YouTube + 1 TikTok + 1 Reels per topik) · {total} dtk short · "
      f"struktur S1–S7 sekali pakai")
