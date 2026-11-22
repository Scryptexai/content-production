#!/usr/bin/env python3
"""fetch_map_assets.py — rakit peta asli dari tile OpenStreetMap → assets/maps/.

Dijalankan DI RUNNER (Actions): sandbox tidak punya akses keluar selain
registry paket; Wikimedia juga memblokir IP cloud (HTTP 429), jadi sumbernya
tile.openstreetmap.org (lisensi ODbL, kredit © OpenStreetMap contributors).

Untuk tiap aset di assets/maps/SOURCES.json (bbox + zoom):
  1. hitung rentang tile yang menutup bbox (matematika Web Mercator)
  2. unduh tile (jeda sopan + backoff)
  3. rakit jadi PNG dengan Pillow
  4. tulis <nama>.bounds.json — north/south/west/east hasil hitung presisi
     (dipakai job JSON MAP-ZOOM supaya lat/lon peta = lat/lon narasi)

Idempoten: PNG ≥ 10 KB dianggap selesai.

    python3 tools/fetch_map_assets.py
"""
import hashlib
import json
import math
import os
import pathlib
import sys
import time
import urllib.request

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
SRC = ROOT / "assets" / "maps" / "SOURCES.json"
OUT = ROOT / "assets" / "maps"
UA = "OddchapterAssetFetcher/1.0 (YouTube channel @oddchapter7; contact: ops@oddchapter)"
TILE = 256


def tlon(lon: float, z: int) -> float:
    return (lon + 180.0) / 360.0 * (1 << z)


def tlat(lat: float, z: int) -> float:
    s = math.sin(math.radians(lat))
    return (0.5 - math.log((1 + s) / (1 - s)) / (4 * math.pi)) * (1 << z)


def y2lat(y: float, z: int) -> float:
    n = math.pi * (1 - 2 * y / (1 << z))
    return math.degrees(math.atan(math.sinh(n)))


def x2lon(x: float, z: int) -> float:
    return x / (1 << z) * 360.0 - 180.0


# Rantai provider tile — probe sekali di awal, pakai SATU provider untuk
# seluruh raster (gaya campuran = jahitan jelek). OSM.org pernah memblokir
# IP cloud (resp103 B), jadi ada cadangan.
PROVIDERS = [
    {
        "name": "openstreetmap.org",
        "url": "https://tile.openstreetmap.org/{z}/{x}/{y}.png",
        "credit": "\u00a9 OpenStreetMap contributors",
    },
    {
        "name": "openstreetmap.de",
        "url": "https://tile.openstreetmap.de/{z}/{x}/{y}.png",
        "credit": "\u00a9 OpenStreetMap contributors",
    },
    {
        "name": "cyclosm",
        "url": "https://tile.cyclosm.org/{z}/{x}/{y}.png",
        "credit": "\u00a9 OpenStreetMap contributors \u00b7 CyclOSM",
    },
]


def _get(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def pick_provider(z: int, x: int, y: int) -> dict:
    """Probe satu tile di tiap provider; kembalikan yang pertama sukses."""
    errs = []
    for prov in PROVIDERS:
        url = prov["url"].format(z=z, x=x, y=y)
        for attempt in range(2):
            try:
                data = _get(url)
                if len(data) < 1000:
                    body = data[:160].decode("utf-8", "replace").replace("\n", " ")
                    raise RuntimeError(f"resp {len(data)} B: {body}")
                print(f"  provider OK: {prov['name']} ({len(data)} B)", flush=True)
                return prov
            except Exception as e:  # noqa: BLE001
                errs.append(f"{prov['name']}: {e}")
                time.sleep(2)
    raise RuntimeError("semua provider gagal -> " + " | ".join(errs))


def fetch_tile(url_tpl: str, z: int, x: int, y: int, tries: int = 3) -> bytes:
    last: Exception | None = None
    url = url_tpl.format(z=z, x=x, y=y)
    for attempt in range(tries):
        try:
            data = _get(url)
            if len(data) < 1000:
                body = data[:160].decode("utf-8", "replace").replace("\n", " ")
                raise RuntimeError(f"resp {len(data)} B: {body}")
            return data
        except Exception as e:  # noqa: BLE001
            last = e
            wait = 4 * (attempt + 1)
            print(f"    tile gagal ({e}); tunggu {wait}s", flush=True)
            time.sleep(wait)
    assert last is not None
    raise last


def render(entry: dict) -> None:
    from io import BytesIO

    from PIL import Image

    north, south, west, east = entry["bbox"]
    z = int(entry["zoom"])
    x0 = int(math.floor(tlon(west, z)))
    x1 = int(math.ceil(tlon(east, z)))
    y0 = int(math.floor(tlat(north, z)))
    y1 = int(math.ceil(tlat(south, z)))
    if x1 <= x0:
        x1 = x0 + 1
    if y1 <= y0:
        y1 = y0 + 1
    w_tiles, h_tiles = x1 - x0, y1 - y0
    print(f"  tile grid {w_tiles}x{h_tiles} @z{z}", flush=True)

    canvas = Image.new("RGB", (w_tiles * TILE, h_tiles * TILE), (240, 240, 240))
    total = w_tiles * h_tiles
    prov = pick_provider(z, x0, y0)
    for i, ty in enumerate(range(y0, y1)):
        for j, tx in enumerate(range(x0, x1)):
            data = fetch_tile(prov["url"], z, tx, ty)
            img = Image.open(BytesIO(data)).convert("RGB")
            canvas.paste(img, (j * TILE, i * TILE))
            n = i * w_tiles + j + 1
            if n % 5 == 0 or n == total:
                print(f"  tile {n}/{total}", flush=True)
            time.sleep(0.7)

    # validasi: tile placeholder (mis. "API KEY REQUIRED") hampir seragam — tolak
    import statistics
    sample = canvas.resize((64, 64)).convert("L")
    stdev = statistics.pstdev(sample.getdata())
    if stdev < 14:
        raise RuntimeError(
            f"raster seragam (stdev={stdev:.1f}) — provider mengembalikan placeholder"
        )
    print(f"  variance OK (stdev={stdev:.1f})", flush=True)

    dst = OUT / entry["file"]
    dst.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(dst, "PNG", optimize=True)
    bounds = {
        "north": y2lat(y0, z),
        "south": y2lat(y1, z),
        "west": x2lon(x0, z),
        "east": x2lon(x1, z),
        "zoom": z,
        "size": [canvas.width, canvas.height],
        "credit": prov["credit"],
        "provider": prov["name"],
    }
    (OUT / (pathlib.Path(entry["file"]).stem + ".bounds.json")).write_text(
        json.dumps(bounds, indent=1) + "\n", encoding="utf-8"
    )
    print(f"  ok {entry['file']} {canvas.width}x{canvas.height} {dst.stat().st_size} B")


def main():
    spec = json.loads(SRC.read_text(encoding="utf-8"))
    failed, details = [], []
    for i, entry in enumerate(spec["assets"]):
        dst = OUT / entry["file"]
        if dst.exists() and dst.stat().st_size > 10_000:
            print(f"  ada  {entry['file']} ({dst.stat().st_size} B)")
            continue
        print(f"rakit {entry['file']} ← bbox {entry['bbox']} z{entry['zoom']}", flush=True)
        try:
            render(entry)
        except Exception as e:  # noqa: BLE001
            failed.append(entry["file"])
            details.append(f"{entry['file']}: {type(e).__name__}: {e}")
            print(f"  GAGAL {entry['file']}: {e}", file=sys.stderr, flush=True)
        if i < len(spec["assets"]) - 1:
            time.sleep(3)
    if failed:
        summary_path = os.environ.get("GITHUB_STEP_SUMMARY", "")
        if summary_path:
            try:
                with open(summary_path, "a", encoding="utf-8") as fh:
                    fh.write("## Gagal merakit peta OSM\n\n")
                    for t in details:
                        fh.write(f"- `{t}`\n")
            except Exception:
                pass
        sys.exit("::error::gagal peta: " + " || ".join(details))


if __name__ == "__main__":
    main()
