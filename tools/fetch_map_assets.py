#!/usr/bin/env python3
"""fetch_map_assets.py — unduh peta asli (Wikimedia Commons) ke assets/maps/.

Dijalankan DI RUNNER (Actions) — sandbox tidak punya akses ke
upload.wikimedia.org. Sumber: assets/maps/SOURCES.json. File yang sudah ada
dan tidak kosong dilewati supaya idempoten.

    python3 tools/fetch_map_assets.py
"""
import json
import pathlib
import sys
import urllib.request

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
SRC = ROOT / "assets" / "maps" / "SOURCES.json"
OUT = ROOT / "assets" / "maps"
UA = "OddchapterAssetFetcher/1.0 (YouTube channel @oddchapter7)"


def main():
    spec = json.loads(SRC.read_text(encoding="utf-8"))
    failed = []
    for a in spec["assets"]:
        dst = OUT / a["file"]
        if dst.exists() and dst.stat().st_size > 0:
            print(f"  ada  {a['file']} ({dst.stat().st_size} B)")
            continue
        print(f"unduh {a['file']} ← {a['url']}", flush=True)
        try:
            req = urllib.request.Request(a["url"], headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=300) as r:
                data = r.read()
            if len(data) < 1024:
                raise RuntimeError(f"terlalu kecil ({len(data)} B)")
            dst.write_bytes(data)
            print(f"  ok   {dst.stat().st_size} B")
        except Exception as e:  # noqa: BLE001
            print(f"  GAGAL {a['file']}: {e}", file=sys.stderr)
            failed.append(a["file"])
    if failed:
        sys.exit(f"::error::gagal mengunduh: {', '.join(failed)}")


if __name__ == "__main__":
    main()
