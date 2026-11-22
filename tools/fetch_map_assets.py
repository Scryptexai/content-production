#!/usr/bin/env python3
"""fetch_map_assets.py — unduh peta asli (Wikimedia Commons) ke assets/maps/.

Dijalankan DI RUNNER (Actions) — sandbox tidak punya akses ke
upload.wikimedia.org. Sumber: assets/maps/SOURCES.json. File yang sudah ada
dan tidak kosong dilewati supaya idempoten.

    python3 tools/fetch_map_assets.py
"""
import json
import os
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
    failures_detail = []
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
            failures_detail.append(f"{a['file']}: {type(e).__name__}: {e}")
    if failed:
        summary = pathlib.Path(os.environ.get("GITHUB_STEP_SUMMARY", "/dev/null"))
        try:
            with summary.open("a", encoding="utf-8") as fh:
                fh.write("## Gagal unduh peta\n\n")
                fh.write(", ".join(failed) + "\n")
                for t in failures_detail:
                    fh.write(f"- `{t}`\n")
        except Exception:
            pass
        detail = "; ".join(failures_detail) if failures_detail else ", ".join(failed)
        sys.exit(f"::error::gagal mengunduh: {detail}")


if __name__ == "__main__":
    main()
