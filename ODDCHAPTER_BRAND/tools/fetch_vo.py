#!/usr/bin/env python3
"""
fetch_vo.py — unduh satu berkas dari Drive untuk diproses di CI.

    python3 tools/fetch_vo.py --id <drive_file_id> --out vo.mp3

Dua jalur, sama seperti fetch_masters.py: gdown dulu (menangani halaman konfirmasi),
lalu unduhan langsung untuk berkas publik. Kalau Drive mengembalikan HTML, berkasnya
belum dibagikan — keluar dengan pesan yang menyebutkan itu, bukan error acak.
"""

import argparse
import shutil
import sys
import urllib.request


def gdown(fid, target):
    try:
        import gdown
    except ImportError:
        return False
    try:
        gdown.download(id=fid, output=str(target), quiet=False, fuzzy=False)
    except Exception as e:                      # noqa: BLE001
        print(f"  gdown gagal: {e}")
        return False
    return target.exists() and target.stat().st_size > 0


def direct(fid, target):
    url = (f"https://drive.usercontent.google.com/download?id={fid}"
           f"&export=download&confirm=t")
    req = urllib.request.Request(url, headers={"User-Agent": "oddchapter-vo/1"})
    with urllib.request.urlopen(req, timeout=900) as r, open(target, "wb") as f:
        ctype = r.headers.get("Content-Type", "")
        if "text/html" in ctype:
            target.unlink(missing_ok=True)
            sys.exit(f"::error::Drive mengembalikan HTML untuk {fid} — berkas belum publik. "
                     f"Bagikan dulu (anyone with the link → Viewer).")
        shutil.copyfileobj(r, f, length=4 * 1024 * 1024)
    return target.exists() and target.stat().st_size > 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--id", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    if gdown(args.id, args.out):
        print(f"  gdown: {args.out}")
        return
    print("  gdown tidak jalan, coba unduh langsung")
    if not direct(args.id, args.out):
        sys.exit(f"::error::gagal mengunduh {args.id}")


if __name__ == "__main__":
    main()
