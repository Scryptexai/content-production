#!/usr/bin/env python3
"""fetch_map_assets.py — unduh peta asli (Wikimedia Commons) ke assets/maps/.

Dijalankan DI RUNNER (Actions) — sandbox tidak punya akses ke
upload.wikimedia.org. Sumber: assets/maps/SOURCES.json. File yang sudah ada
dan tidak kosong dilewati supaya idempoten.

Strategi anti-429 (IP runner pernah di-rate-limit Wikimedia):
  1. Special:FilePath (redirect ke path hash) — 2 percobaan + backoff
  2. web.archive.org id_ mirror (URL hash dihitung lokal via MD5)
  3. upload.wikimedia.org langsung (path hash) — 1 percobaan
Jeda 6 detik antar-aset. Gagal total → exit 1 + detail di annotasi/summary.

    python3 tools/fetch_map_assets.py
"""
import hashlib
import json
import os
import pathlib
import sys
import time
import urllib.parse
import urllib.request

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
SRC = ROOT / "assets" / "maps" / "SOURCES.json"
OUT = ROOT / "assets" / "maps"
UA = "OddchapterAssetFetcher/1.0 (YouTube channel @oddchapter7; contact: ops@oddchapter)"


def upload_url(filename: str) -> str:
    """URL upload.wikimedia.org resmi — path hash = MD5 nama berunderscore."""
    name = filename.replace(" ", "_")
    h = hashlib.md5(name.encode("utf-8")).hexdigest()
    quoted = urllib.parse.quote(name)
    return f"https://upload.wikimedia.org/wikipedia/commons/{h[0]}/{h[:2]}/{quoted}"


def fetch_bytes(url: str, tries: int = 2, pause: int = 12) -> bytes:
    last: Exception | None = None
    for attempt in range(tries):
        try:
            req = urllib.request.Request(
                url, headers={"User-Agent": UA, "Accept": "*/*"}
            )
            with urllib.request.urlopen(req, timeout=120) as r:
                data = r.read()
            if len(data) < 1024:
                raise RuntimeError(f"terlalu kecil ({len(data)} B)")
            return data
        except Exception as e:  # noqa: BLE001
            last = e
            print(f"    percobaan {attempt + 1}/{tries} gagal: {e}", flush=True)
            if attempt < tries - 1:
                time.sleep(pause)
    assert last is not None
    raise last


def main():
    spec = json.loads(SRC.read_text(encoding="utf-8"))
    failed = []
    details = []
    for i, a in enumerate(spec["assets"]):
        dst = OUT / a["file"]
        if dst.exists() and dst.stat().st_size > 0:
            print(f"  ada  {a['file']} ({dst.stat().st_size} B)")
            continue
        direct = upload_url(a["file"])
        chain = [
            ("commons", a["url"]),
            ("archive", f"https://web.archive.org/web/0id_/{direct}"),
            ("upload", direct),
        ]
        print(f"unduh {a['file']}", flush=True)
        errors = []
        done = False
        for label, url in chain:
            try:
                data = fetch_bytes(url, tries=2 if label != "upload" else 1)
                dst.write_bytes(data)
                print(f"  ok   {label}: {dst.stat().st_size} B")
                done = True
                break
            except Exception as e:  # noqa: BLE001
                errors.append(f"{label}: {type(e).__name__}: {e}")
                print(f"  lewat {label}: {e}", flush=True)
        if not done:
            failed.append(a["file"])
            details.append(f"{a['file']} -> " + " | ".join(errors))
        if i < len(spec["assets"]) - 1:
            time.sleep(6)
    if failed:
        summary_path = os.environ.get("GITHUB_STEP_SUMMARY", "")
        if summary_path:
            try:
                with open(summary_path, "a", encoding="utf-8") as fh:
                    fh.write("## Gagal unduh peta\n\n")
                    for t in details:
                        fh.write(f"- `{t}`\n")
            except Exception:
                pass
        sys.exit(f"::error::gagal mengunduh: " + " || ".join(details))


if __name__ == "__main__":
    main()
