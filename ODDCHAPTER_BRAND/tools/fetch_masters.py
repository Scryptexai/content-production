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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--media-dir", default="media")
    args = ap.parse_args()

    sel = (os.environ.get("EPISODE_SELECT") or "ALL").strip()
    media = pathlib.Path(args.media_dir)
    media.mkdir(parents=True, exist_ok=True)

    try:
        import gdown
    except ImportError:
        sys.exit("::error::gdown belum terpasang — pip install gdown")

    for ep in selected_episodes(sel):
        meta = json.loads((META_DIR / f"{ep}.json").read_text(encoding="utf-8"))
        video = media / meta["video"]
        if not video.exists():
            fid = meta.get("drive_file_id")
            if not fid:
                sys.exit(f"::error::{ep}: drive_file_id kosong di metadata")
            print(f"unduh {ep} ← Drive {fid}", flush=True)
            gdown.download(id=fid, output=str(video), quiet=True, fuzzy=False)
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
