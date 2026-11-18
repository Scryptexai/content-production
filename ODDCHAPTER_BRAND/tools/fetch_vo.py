#!/usr/bin/env python3
"""
fetch_vo.py — unduh satu berkas dari Drive untuk diproses di CI.

    python3 tools/fetch_vo.py --id <drive_file_id> --out vo.mp3

Dua jalur, sama seperti fetch_masters.py: gdown dulu (menangani halaman konfirmasi),
lalu unduhan langsung untuk berkas publik. Kalau Drive mengembalikan HTML, berkasnya
belum dibagikan — keluar dengan pesan yang menyebutkan itu, bukan error acak.
"""

import argparse
import pathlib
import shutil
import sys
import urllib.request


def gdown(fid, target):
    try:
        import gdown
    except ImportError:
        return False
    try:
        gdown.download(id=fid, output=str(target), quiet=False)
    except Exception as e:                      # noqa: BLE001
        print(f"  gdown gagal: {e}")
        return False
    return target.exists() and target.stat().st_size > 0


URLS = (
    "https://drive.usercontent.google.com/download?id={fid}&export=download&confirm=t",
    "https://drive.google.com/uc?export=download&id={fid}",
    "https://drive.usercontent.google.com/download?id={fid}&export=download",
)


def direct(fid, target):
    last = ""
    for tpl in URLS:
        url = tpl.format(fid=fid)
        print(f"  coba: {url}", flush=True)
        req = urllib.request.Request(url, headers={"User-Agent": "oddchapter-vo/1"})
        try:
            with urllib.request.urlopen(req, timeout=900) as r:
                ctype = r.headers.get("Content-Type", "")
                clen = r.headers.get("Content-Length", "?")
                print(f"    HTTP {r.status} · {ctype} · Content-Length {clen}", flush=True)
                if "text/html" in ctype:
                    body = r.read(600).decode("utf-8", "replace")
                    print(f"    isi HTML: {body[:300]!r}", flush=True)
                    last = "Drive mengembalikan HTML (berkas belum publik, atau kena kuota unduh)"
                    continue
                with open(target, "wb") as f:
                    shutil.copyfileobj(r, f, length=4 * 1024 * 1024)
            if target.exists() and target.stat().st_size > 0:
                print(f"    tersimpan {target.stat().st_size} byte", flush=True)
                return True
        except Exception as e:                   # noqa: BLE001
            last = f"{type(e).__name__}: {e}"
            print(f"    gagal: {last}", flush=True)
    target.unlink(missing_ok=True)
    sys.exit(f"::error::gagal mengunduh {fid} — {last}")
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--id", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    target = pathlib.Path(args.out)

    if gdown(args.id, target):
        print(f"  gdown: {target} ({target.stat().st_size} byte)")
        return
    print("  gdown tidak jalan, coba unduh langsung")
    if not direct(args.id, target):
        sys.exit(f"::error::gagal mengunduh {args.id}")


if __name__ == "__main__":
    main()
