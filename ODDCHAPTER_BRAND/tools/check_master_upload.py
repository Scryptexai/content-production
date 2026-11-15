"""
check_master_upload.py — gerbang serah-terima.

Setiap master yang selesai dirender wajib diunggah ke Drive di sesi yang sama,
dan id-nya dicatat di `11_CONTENT/04_VIDEO_READY/MASTER_UPLOAD.md`. Skrip ini
membandingkan berkas lokal dengan tabel itu.

    python3 tools/check_master_upload.py          # semua
    python3 tools/check_master_upload.py EP09     # satu episode

Status keluar ≠ 0 kalau ada master lokal yang belum punya id Drive — jadi
"render selesai" tidak bisa lagi dianggap "beres" tanpa unggahan.
"""

import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
MASTERS = ROOT / "10_FILM" / "remotion" / "output" / "episodes"
LEDGER = ROOT / "11_CONTENT" / "04_VIDEO_READY" / "MASTER_UPLOAD.md"

ID_RX = re.compile(r"`(1[0-9A-Za-z_\-]{20,})`")


def ledger_rows():
    """{ep: drive_id} untuk master aktif (tabel pertama setelah '## Master aktif')."""
    if not LEDGER.exists():
        return {}
    text = LEDGER.read_text(encoding="utf-8")
    try:
        block = text.split("## Master aktif", 1)[1].split("##", 1)[0]
    except IndexError:
        return {}
    rows = {}
    for line in block.splitlines():
        if not line.startswith("| EP"):
            continue
        cols = [c.strip() for c in line.strip("|").split("|")]
        ep = cols[0]
        ids = ID_RX.findall(line)
        rows[ep] = ids[0] if ids else ""
    return rows


def main():
    want = sys.argv[1:] or None
    rows = ledger_rows()
    local = sorted(MASTERS.glob("*_master*.mp4")) if MASTERS.is_dir() else []

    print(f"{'ep':5s} {'berkas lokal':42s} {'id Drive':34s} status")
    bad, seen = 0, set()
    for f in local:
        ep = f.name.split("_")[0]
        if want and ep not in want:
            continue
        seen.add(ep)
        did = rows.get(ep, "")
        status = "tercatat" if did else "BELUM DIUNGGAH / belum dicatat"
        if not did:
            bad += 1
        print(f"{ep:5s} {f.name[:42]:42s} {(did or '—')[:34]:34s} {status}")

    # episode yang tercatat tapi master lokalnya sudah tidak ada (arsip/ganti mesin)
    for ep, did in sorted(rows.items()):
        if ep not in seen and (not want or ep in want):
            print(f"{ep:5s} {'—':42s} {did[:34]:34s} catatan saja (berkas lokal tidak ada)")

    print(f"\n{len(seen)} master lokal · {bad} belum tercatat di {LEDGER.name}")
    if bad:
        print("Unggah ke folder 'video ready' (1fVoOvZgiYB3V7S2C5LfMrCpo-c4Xxzo2),")
        print("lalu tambahkan barisnya di tabel '## Master aktif'.")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
