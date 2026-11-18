#!/usr/bin/env python3
"""Ambil footage Coverr di GitHub Actions (sandbox tidak bisa akses cdn.coverr.co).

Alur: query API Coverr → pilih klip non-premium 16:9 → coba beberapa pola URL
unduh (cdn 1080p / Mux mp4 / Mux HLS) → normalisasi 1920x1080 30fps tanpa audio
→ taruh di footage/ untuk diunggah sebagai artifact.
"""
import argparse, json, os, pathlib, subprocess, sys, urllib.parse, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# (query, jumlah klip) — disusun mengikuti bab EP01 (dipakai kalau tidak ada --spec)
QUERIES = [
    ("old paper texture", 2), ("candle flame", 2), ("light beam dust", 2),
    ("quill pen", 2), ("ink well", 1), ("old map", 2),
    ("portrait painting", 2), ("candles church dark", 2), ("stone staircase", 1),
    ("shadow window light", 2), ("stack of books", 2), ("archive shelves", 2),
    ("coins money", 1), ("bank building", 1), ("old newspaper", 2),
    ("human eye macro", 1), ("cathedral dome", 1), ("moon night sky", 1),
    ("fog night street", 2), ("wooden table dark", 2), ("hands holding letter", 2),
    ("library reading", 2), ("black smoke", 1), ("typewriter keys", 1),
]
UA = {"User-Agent": "Mozilla/5.0 (footage-fetch)", "Accept": "application/json"}


def fetch_json(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))


def try_download(url, dest):
    """curl bisa menarik mp4 maupun HLS (ffmpeg lewat curl tidak; pakai ffmpeg bila .m3u8)."""
    if url.endswith(".m3u8"):
        cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", url,
               "-t", "6", "-an", "-c:v", "libx264", "-crf", "20", "-preset", "veryfast", dest]
    else:
        tmp = dest + ".part"
        cmd = ["curl", "-fsSL", "--max-time", "180", "-o", tmp, url]
        if subprocess.run(cmd).returncode != 0:
            return False
        sz = os.path.getsize(tmp) if os.path.exists(tmp) else 0
        if sz < 200_000:
            os.path.exists(tmp) and os.remove(tmp)
            return False
        cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", tmp,
               "-an", "-c:v", "libx264", "-crf", "20", "-preset", "veryfast", dest]
    try:
        if subprocess.run(cmd).returncode != 0:
            return False
    except OSError:
        return False
    return os.path.exists(dest) and os.path.getsize(dest) > 100_000


def normalize(src, dest):
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", src, "-t", "6",
           "-vf", "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,fps=30",
           "-an", "-c:v", "libx264", "-crf", "20", "-preset", "veryfast",
           "-pix_fmt", "yuv420p", "-movflags", "+faststart", dest]
    if subprocess.run(cmd).returncode != 0:
        return False
    if os.path.exists(src) and os.path.abspath(src) != os.path.abspath(dest):
        os.remove(src)
    return True


def run(queries, out_dir, report_path):
  report = {"ok": [], "failed": [], "candidates": {}}
  print(f"spec: {len(queries)} kueri -> {out_dir}", flush=True)
  for q, want in queries:
    url = ("https://coverr.co/api/videos?query=" + urllib.parse.quote(q) +
           "&page_size=20&is_premium=false")
    try:
        data = fetch_json(url)
    except Exception as e:  # noqa: BLE001
        report["failed"].append({"query": q, "why": f"api: {e}"})
        continue
    picks = [h for h in data.get("hits", [])
             if not h.get("is_premium") and not h.get("is_vertical")
             and float(h.get("duration") or 0) >= 6]
    if picks:
        report["candidates"][q] = [
            {k: p.get(k) for k in ("title", "base_filename", "playback_id", "duration",
                                   "max_height", "fps", "slug")} | {"urls": p.get("urls")}
            for p in picks[:3]
        ]
    slug = q.replace(" ", "_")
    got = 0
    for h in picks:
        if got >= want:
            break
        base, pb = h["base_filename"], h.get("playback_id")
        dest = os.path.join(out_dir, f"{slug}__{base}.mp4")
        tmp = os.path.join(out_dir, f"_tmp_{base}.mp4")
        if os.path.exists(dest) and os.path.getsize(dest) > 100_000:
            print(f"  lewati (sudah ada): {os.path.basename(dest)}", flush=True)
            got += 1
            continue
        cands = [f"https://cdn.coverr.co/videos/{base}/1080p.mp4",
                 f"https://cdn.coverr.co/videos/{base}/1080p?download=true",
                 f"https://cdn.coverr.co/videos/{base}/720p.mp4"]
        if pb:
            cands += [f"https://stream.mux.com/{pb}/high.mp4",
                      f"https://stream.mux.com/{pb}/medium.mp4",
                      f"https://stream.mux.com/{pb}.m3u8"]
        used = None
        for c in cands:
            if try_download(c, tmp):
                used = c
                break
        if not used:
            report["failed"].append({"query": q, "why": "semua pola URL gagal", "base": base})
            continue
        if not normalize(tmp, dest):
            report["failed"].append({"query": q, "why": "normalize gagal", "base": base})
            continue
        got += 1
        report["ok"].append({"query": q, "file": os.path.basename(dest), "via": used,
                             "duration": h.get("duration"), "title": h.get("title")})

  with open(report_path, "w") as f:
      json.dump(report, f, indent=1)
  print(json.dumps({"ok": len(report["ok"]), "failed": len(report["failed"])}), flush=True)
  return report


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", default="", help="berkas JSON daftar kueri")
    ap.add_argument("--out", default="footage")
    ap.add_argument("--report", default="footage-report.json")
    args = ap.parse_args()

    if args.spec:
        spec = json.loads(pathlib.Path(args.spec).read_text(encoding="utf-8"))
        queries = [(q["q"], int(q.get("want", 2))) for q in spec["queries"]]
        out_dir = os.path.join(ROOT, spec.get("target_dir", args.out))
        report_path = os.path.join(ROOT, spec.get("report", args.report))
    else:
        queries = [(q, w) for q, w in QUERIES]
        out_dir = os.path.join(ROOT, args.out)
        report_path = os.path.join(ROOT, args.report)

    os.makedirs(out_dir, exist_ok=True)
    for f in os.listdir(out_dir):
        if f.startswith("_tmp_") or f.endswith(".part"):
            os.remove(os.path.join(out_dir, f))
    rep = run(queries, out_dir, report_path)
    sys.exit(0 if rep["ok"] else 1)


if __name__ == "__main__":
    main()
