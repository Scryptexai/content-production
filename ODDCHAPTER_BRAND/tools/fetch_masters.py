#!/usr/bin/env python3
"""
fetch_masters.py — ambil file master dari Drive ke satu folder media/.

    EPISODE_SELECT=EP01 python3 tools/fetch_masters.py            # default: media/
    EPISODE_SELECT=ALL  python3 tools/fetch_masters.py --media-dir media

Kenapa begini: MP4 17–22 MB tinggal di Drive (`video ready`), bukan di Git.
Workflow hanya butuh id file — tercatat di 11_CONTENT/06_UPLOAD/EPxx.json
sebagai drive_file_id bersama size_bytes + sha256. Setelah unduh, upload_zernio.py
memeriksa ukuran dan hash; kalau tidak sama, unggahan dibatalkan.

Thumbnail tidak diunduh: JPEG-nya (±0,3 MB) ikut di repo di
11_CONTENT/06_UPLOAD/thumbs/, jadi selalu versi yang sama dengan yang di-commit.
"""

import argparse
import json
import os
import pathlib
import shutil
import sys
import urllib.request

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
META_DIR = ROOT / "11_CONTENT" / "06_UPLOAD"
THUMB_DIR = META_DIR / "thumbs"


def selected_episodes(sel):
    eps = [p.stem for p in sorted(META_DIR.glob("EP*.json"))]
    if sel.upper() == "ALL":
        return eps
    if sel not in eps:
        sys.exit(f"::error::{sel} tidak punya metadata di 11_CONTENT/06_UPLOAD/")
    return [sel]


def gdown_download(fid, target):
    """Jalur utama: gdown menangani halaman konfirmasi Drive."""
    try:
        import gdown
    except ImportError:
        return False
    try:
        gdown.download(id=fid, output=str(target), quiet=True, fuzzy=False)
    except Exception as e:                     # noqa: BLE001 — apa pun, kita punya cadangan
        print(f"  gdown gagal: {e}")
        return False
    return target.exists() and target.stat().st_size > 0


def direct_download(fid, target):
    """Cadangan untuk file yang sudah publik (anyone with the link).

    Tidak butuh cookie; kalau Drive mengembalikan halaman HTML, artinya file
    tidak publik dan cadangan ini juga akan gagal dengan pesan yang jelas.
    """
    url = (f"https://drive.usercontent.google.com/download?id={fid}"
           f"&export=download&confirm=t")
    req = urllib.request.Request(url, headers={"User-Agent": "oddchapter-upload/1"})
    with urllib.request.urlopen(req, timeout=600) as r, open(target, "wb") as f:
        ctype = r.headers.get("Content-Type", "")
        if "text/html" in ctype:
            target.unlink(missing_ok=True)
            sys.exit(f"::error::Drive mengembalikan HTML untuk {fid} — file tidak publik. "
                     "Buka Drive → bagikan (anyone with the link → Viewer), lalu ulangi.")
        shutil.copyfileobj(r, f, length=4 * 1024 * 1024)
    return target.exists() and target.stat().st_size > 0


def fetch(fid, target):
    if gdown_download(fid, target):
        return
    print("  gdown tidak jalan, coba unduh langsung")
    if not direct_download(fid, target):
        sys.exit(f"::error::gagal mengunduh {fid}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--media-dir", default="media")
    args = ap.parse_args()

    sel = (os.environ.get("EPISODE_SELECT") or "ALL").strip()
    media = pathlib.Path(args.media_dir)
    media.mkdir(parents=True, exist_ok=True)

    for ep in selected_episodes(sel):
        meta = json.loads((META_DIR / f"{ep}.json").read_text(encoding="utf-8"))
        video = media / meta["video"]
        if not video.exists():
            fid = meta.get("drive_file_id")
            if not fid:
                sys.exit(f"::error::{ep}: drive_file_id kosong di metadata")
            print(f"unduh {ep} ← Drive {fid}", flush=True)
            fetch(fid, video)
            if not video.exists() or video.stat().st_size == 0:
                sys.exit(f"::error::{ep}: unduhan gagal atau kosong")
        print(f"  {ep}  {video.name}  {video.stat().st_size / 1024 ** 2:.1f} MB")

        thumb = media / meta["thumbnail"]
        if not thumb.exists():
            src = THUMB_DIR / meta["thumbnail"]
            if not src.exists():
                sys.exit(f"::error::{ep}: thumbnail tidak ada di {src.relative_to(ROOT)}")
            shutil.copy2(src, thumb)
        print(f"  {ep}  {thumb.name}  {thumb.stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    main()
