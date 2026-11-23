#!/usr/bin/env python3
"""fetch_map_assets.py — rakit peta asli dari tile provider → assets/maps/.

Dijalankan DI RUNNER (Actions): sandbox tidak punya akses keluar selain
registry paket; tile server OSM pernah memblokir IP cloud di tengah burst
(responses challenge ~103 B), jadi tiap tile punya rantai cadangan:
  openstreetmap.org → openstreetmap.de → cyclosm → esri street map.
Provider pertama yang sukses jadi "gaya utama" aset (diurutkan dulu untuk
tile berikutnya) supaya kanvas sebisa mungkin satu gaya; kredit di bounds.json
dipakai job MapZoom supaya sumber = yang benar-benar dipakai.

Untuk tiap aset di assets/maps/SOURCES.json (bbox + zoom):
  1. hitung rentang tile yang menutup bbox (matematika Web Mercator)
  2. unduh tile (jeda sopan + backoff, fallback antar provider per tile)
  3. rakit jadi PNG dengan Pillow + validasi variance (tolak placeholder)
  4. tulis <nama>.bounds.json — north/south/west/east hasil hitung presisi

Idempoten: PNG ≥ 10 KB dianggap selesai.

    python3 tools/fetch_map_assets.py
"""
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


# Rantai provider tile — probe sekali di awal; gagal di tengah burst (103 B)
# → fallback per tile ke provider berikutnya, provider sukses didahulukan.
PROVIDERS = [
    {
        "name": "openstreetmap.org",
        "url": "https://tile.openstreetmap.org/{z}/{x}/{y}.png",
        "credit": "© OpenStreetMap contributors",
    },
    {
        "name": "openstreetmap.de",
        "url": "https://tile.openstreetmap.de/{z}/{x}/{y}.png",
        "credit": "© OpenStreetMap contributors",
    },
    {
        "name": "cyclosm",
        "url": "https://tile.cyclosm.org/{z}/{x}/{y}.png",
        "credit": "© OpenStreetMap contributors · CyclOSM",
    },
    {
        # darurat terakhir — gaya berbeda, dipakai hanya bila OSM-family
        # mati semua supaya aset tetap terbentuk (kredit ikut diganti)
        "name": "esri-street",
        "url": "https://server.arcgisonline.com/ArcGIS/rest/services/"
               "World_Street_Map/MapServer/tile/{z}/{y}/{x}",
        "credit": "© Esri · HERE · Garmin · OpenStreetMap contributors",
    },
]


def _get(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def _check(data: bytes, where: str) -> bytes:
    if len(data) < 1000:
        body = data[:160].decode("utf-8", "replace").replace("\n", " ")
        raise RuntimeError(f"{where}: resp {len(data)} B: {body}")
    return data


def pick_provider(z: int, x: int, y: int) -> int:
    """Probe satu tile di tiap provider; kembalikan index yang pertama sukses."""
    errs = []
    for idx, prov in enumerate(PROVIDERS):
        url = prov["url"].format(z=z, x=x, y=y)
        for attempt in range(2):
            try:
                data = _check(_get(url), prov["name"])
                print(f"  provider OK: {prov['name']} ({len(data)} B)", flush=True)
                return idx
            except Exception as e:  # noqa: BLE001
                errs.append(f"{prov['name']}: {e}")
                time.sleep(2)
    raise RuntimeError("semua provider gagal -> " + " | ".join(errs))


def fetch_tile(order: list[int], z: int, x: int, y: int) -> tuple[bytes, int]:
    """Unduh satu tile; coba provider sesuai `order` sampai sukses → (data, idx)."""
    last: Exception | None = None
    for pos, idx in enumerate(order):
        prov = PROVIDERS[idx]
        url = prov["url"].format(z=z, x=x, y=y)
        tries = 2 if pos == 0 else 1
        for attempt in range(tries):
            try:
                data = _check(_get(url), prov["name"])
                return data, idx
            except Exception as e:  # noqa: BLE001
                last = e
                print(f"    {prov['name']} gagal: {e}", flush=True)
                time.sleep(4 * (attempt + 1))
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
    style_idx = pick_provider(z, x0, y0)  # gaya utama aset
    order = [style_idx] + [i for i in range(len(PROVIDERS)) if i != style_idx]
    used_style = style_idx
    for i, ty in enumerate(range(y0, y1)):
        for j, tx in enumerate(range(x0, x1)):
            data, used = fetch_tile(order, z, tx, ty)
            if used != used_style and used == order[0]:
                # provider berganti (mis. blokir menengah) → jadikan gaya utama
                used_style = used
                print(f"  gaya pindah ke {PROVIDERS[used]['name']}", flush=True)
            # sticky: provider terakhir yang dipakai didahulukan berikutnya
            order = [used] + [i for i in order if i != used]
            img = Image.open(BytesIO(data)).convert("RGB")
            canvas.paste(img, (j * TILE, i * TILE))
            n = i * w_tiles + j + 1
            if n % 5 == 0 or n == total:
                print(f"  tile {n}/{total} (via {PROVIDERS[used]['name']})", flush=True)
            time.sleep(1.0)

    # Validasi placeholder: peta kota pada z10 lazimnya didominasi blok jalan
    # pucat, jadi simpangan luminansinya bisa 9–12 (Istanbul/Khujut Rabu).
    # Ambang lama 14 salah menolak raster OSM sah. Placeholder sungguhan hampir
    # datar *dan* punya sangat sedikit warna; pakai dua sinyal agar tile kosong
    # tetap tertolak tanpa memaksa peta kota terlihat seperti citra satelit.
    import statistics
    sample = canvas.resize((64, 64)).convert("RGB")
    luma = sample.convert("L")
    stdev = statistics.pstdev(luma.getdata())
    colors = len(sample.getcolors(maxcolors=1_000_000) or [])
    if stdev < 4.0 or (stdev < 7.0 and colors < 64):
        raise RuntimeError(
            f"raster nyaris seragam (stdev={stdev:.1f}, colors={colors}) — "
            "provider mengembalikan placeholder"
        )
    print(f"  variance OK (stdev={stdev:.1f}, colors={colors})", flush=True)

    dst = OUT / entry["file"]
    dst.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(dst, "PNG", optimize=True)
    prov = PROVIDERS[used_style]
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
    print(f"  ok {entry['file']} {canvas.width}x{canvas.height} {dst.stat().st_size} B "
          f"(provider {prov['name']})")


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
                    fh.write("## Gagal merakit peta\n\n")
                    for t in details:
                        fh.write(f"- `{t}`\n")
            except Exception:
                pass
        sys.exit("::error::gagal peta: " + " || ".join(details))


if __name__ == "__main__":
    main()
