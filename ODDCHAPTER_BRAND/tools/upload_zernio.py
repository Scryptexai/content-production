#!/usr/bin/env python3
"""
upload_zernio.py — unggah satu episode ke YouTube lewat API Zernio.

    python3 tools/upload_zernio.py EP01                    # dry-run: cetak payload
    python3 tools/upload_zernio.py EP01 --send             # benar-benar unggah
    python3 tools/upload_zernio.py --all --send

Kenapa lewat Zernio dan bukan YouTube Data API langsung: satu endpoint untuk
video/Shorts, tanpa OAuth app review, tanpa kuota 10.000 unit per hari yang
harus dikelola sendiri. Kontraknya (dibaca dari docs.zernio.com, 2026-11-08):

  1. POST /v1/media/presign        {filename, contentType, size}
       → {uploadUrl, publicUrl, key, expiresIn}
  2. PUT  <uploadUrl>              isi file mentah
  3. POST /v1/posts                {content, tags, mediaItems, platforms, publishNow}
       → {post: {_id, status, platforms:[{platformPostUrl}]}}

Kredensial (jangan pernah ditulis di repo):
  ZERNIO_API_KEY               API key dari dashboard Zernio
  ZERNIO_YOUTUBE_ACCOUNT_ID    accountId kanal YouTube yang sudah terhubung
  ZERNIO_PLAYLIST_ID           opsional, playlist tujuan

Metadata per episode: 11_CONTENT/06_UPLOAD/EPxx.json
"""

import argparse
import hashlib
import json
import mimetypes
import os
import pathlib
import sys
import time
import urllib.error
import urllib.request

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
META_DIR = ROOT / "11_CONTENT" / "06_UPLOAD"
LOG_DIR = ROOT / "11_CONTENT" / "06_UPLOAD" / "upload-log"

API = os.environ.get("ZERNIO_API_BASE", "https://zernio.com/api/v1").rstrip("/")
VIDEO_LIMIT = 5 * 1024 ** 3          # presign: maks 5 GB
THUMB_LIMIT = 2 * 1024 ** 2          # YouTube: maks 2 MB untuk thumbnail kustom


def fail(msg):
    print(f"::error::{msg}" if os.environ.get("GITHUB_ACTIONS") else f"GAGAL: {msg}")
    raise SystemExit(1)


def api_post(path, payload, key, timeout=120):
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{API}{path}", data=body, method="POST",
        headers={"Authorization": f"Bearer {key}",
                 "Content-Type": "application/json",
                 "Accept": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")[:900]
        fail(f"POST {path} → HTTP {e.code}: {detail}")


def put_file(upload_url, path):
    data = path.read_bytes()
    req = urllib.request.Request(
        upload_url, data=data, method="PUT",
        headers={"Content-Type": mimetypes.guess_type(path.name)[0] or "application/octet-stream",
                 "Content-Length": str(len(data))},
    )
    try:
        with urllib.request.urlopen(req, timeout=900) as r:
            if r.status not in (200, 201, 204):
                fail(f"PUT {upload_url[:60]}… → HTTP {r.status}")
    except urllib.error.HTTPError as e:
        fail(f"PUT unggah media → HTTP {e.code}: {e.read().decode('utf-8', 'replace')[:400]}")


def upload_media(path, key, kind):
    """presign → PUT → publicUrl. kind cuma untuk pesan log."""
    size = path.stat().st_size
    limit = VIDEO_LIMIT if kind == "video" else THUMB_LIMIT
    if size > limit:
        fail(f"{path.name}: {size / 1024 ** 2:.1f} MB, batas {limit / 1024 ** 2:.0f} MB untuk {kind}")
    ctype = "video/mp4" if kind == "video" else "image/jpeg"
    presigned = api_post("/media/presign",
                         {"filename": path.name, "contentType": ctype, "size": size}, key)
    put_file(presigned["uploadUrl"], path)
    print(f"  {kind:9s} {path.name}  {size / 1024 ** 2:6.1f} MB → {presigned['publicUrl']}")
    return presigned["publicUrl"]


def load_meta(ep):
    p = META_DIR / f"{ep}.json"
    if not p.exists():
        fail(f"metadata tidak ada: {p.relative_to(ROOT)}")
    return json.loads(p.read_text(encoding="utf-8"))


def validate(meta, media_dir):
    """Yang gagal di sini adalah yang ditolak YouTube, bukan selera kita."""
    errs = []
    title = meta.get("title", "")
    if not title.strip():
        errs.append("judul kosong")
    if len(title) > 100:
        errs.append(f"judul {len(title)} karakter, batas YouTube 100")
    hook = meta.get("hook", "")
    if not hook.strip():
        errs.append("hook kosong — baris pertama deskripsi")
    if hook and not (hook.strip().endswith("?") or any(ch.isdigit() for ch in hook)):
        errs.append("hook bukan pertanyaan dan tidak memuat angka")
    desc = meta.get("description", "")
    if len(desc) > 5000:
        errs.append(f"deskripsi {len(desc)} karakter, batas 5000")
    if desc and hook and not desc.startswith(hook):
        errs.append("deskripsi tidak dibuka dengan hook yang sama")
    tags = meta.get("tags") or []
    joined = sum(len(t) for t in tags)
    if joined > 500:
        errs.append(f"tag {joined} karakter gabungan, batas 500")
    if any(len(t) > 100 for t in tags):
        errs.append("ada tag > 100 karakter")
    video = media_dir / meta["video"]
    if not video.exists():
        errs.append(f"file video tidak ada: {video}")
    else:
        size = video.stat().st_size
        if size == 0:
            errs.append("file video 0 byte")
        # Master tinggal di Drive, bukan di Git. Kalau yang terunduh bukan file
        # yang sama dengan yang sudah ditonton dan disetujui, jangan diunggah.
        if meta.get("size_bytes") and size != meta["size_bytes"]:
            errs.append(f"ukuran {meta['video']} {size} byte, metadata bilang "
                        f"{meta['size_bytes']} — file di Drive berubah?")
        elif meta.get("sha256") and hashlib.sha256(video.read_bytes()).hexdigest() != meta["sha256"]:
            errs.append(f"sha256 {meta['video']} tidak cocok dengan metadata")
    thumb = media_dir / meta["thumbnail"]
    if not thumb.exists():
        errs.append(f"file thumbnail tidak ada: {thumb}")
    elif thumb.stat().st_size > THUMB_LIMIT:
        errs.append(f"thumbnail {thumb.stat().st_size / 1024 ** 2:.1f} MB, batas YouTube 2 MB")
    if meta.get("madeForKids") is True:
        errs.append("madeForKids=true mematikan komentar — diskusi akan hilang")
    if errs:
        for e in errs:
            print(f"::error::{e}" if os.environ.get("GITHUB_ACTIONS") else f"  ✗ {e}")
        raise SystemExit(1)


def build_payload(meta, video_url, thumb_url, visibility=None):
    account = os.environ.get("ZERNIO_YOUTUBE_ACCOUNT_ID", "").strip()
    playlist = os.environ.get("ZERNIO_PLAYLIST_ID", "").strip()
    psd = {
        "title": meta["title"],
        "visibility": visibility or meta.get("visibility", "public"),
        "categoryId": str(meta.get("categoryId", "24")),
        "madeForKids": bool(meta.get("madeForKids", False)),
        "containsSyntheticMedia": bool(meta.get("containsSyntheticMedia", True)),
    }
    if playlist:
        psd["playlistId"] = playlist
    if meta.get("first_comment"):
        psd["firstComment"] = meta["first_comment"]
    return {
        "content": meta["description"],
        "tags": meta.get("tags", []),
        "mediaItems": [{"type": "video", "url": video_url, "thumbnail": thumb_url}],
        "platforms": [{"platform": "youtube", "accountId": account, "platformSpecificData": psd}],
        "publishNow": True,
    }


def run(ep, media_dir, send, visibility):
    meta = load_meta(ep)
    print(f"\n=== {ep} · {meta['title']} ({len(meta['title'])} karakter) ===")
    validate(meta, media_dir)

    key = os.environ.get("ZERNIO_API_KEY", "").strip()
    account = os.environ.get("ZERNIO_YOUTUBE_ACCOUNT_ID", "").strip()

    if not send:
        payload = build_payload(meta, f"<publicUrl {meta['video']}>",
                                f"<publicUrl {meta['thumbnail']}>", visibility)
        payload["platforms"][0]["accountId"] = account or "<ZERNIO_YOUTUBE_ACCOUNT_ID>"
        print("  dry-run: tidak ada yang dikirim. Payload POST /v1/posts:")
        print("\n".join("    " + l for l in json.dumps(payload, ensure_ascii=False, indent=2).splitlines()))
        return {"episode": ep, "dry_run": True, "payload": payload}

    if not key:
        fail("ZERNIO_API_KEY kosong — tambahkan sebagai secret repo, jangan di file")
    if not account:
        fail("ZERNIO_YOUTUBE_ACCOUNT_ID kosong — lihat GET /v1/profiles di dashboard Zernio")

    video_url = upload_media(media_dir / meta["video"], key, "video")
    thumb_url = upload_media(media_dir / meta["thumbnail"], key, "thumbnail")

    payload = build_payload(meta, video_url, thumb_url, visibility)
    result = api_post("/posts", payload, key)

    post = (result or {}).get("post", {})
    yt = next((p for p in post.get("platforms", []) if p.get("platform") == "youtube"), {})
    out = {
        "episode": ep,
        "dry_run": False,
        "title": meta["title"],
        "post_id": post.get("_id"),
        "status": post.get("status"),
        "youtube_url": yt.get("platformPostUrl"),
        "video_url_in_zernio": video_url,
        "uploaded_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    print(f"  published: {out['status']} · {out['youtube_url']}")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("episode", nargs="?", help="EP01, EP02, …")
    ap.add_argument("--all", action="store_true", help="semua metadata di 06_UPLOAD")
    ap.add_argument("--media-dir", default=str(ROOT / "10_FILM" / "remotion" / "output" / "episodes"))
    ap.add_argument("--send", action="store_true", help="benar-benar unggah (tanpa ini = dry-run)")
    ap.add_argument("--visibility", choices=["public", "unlisted", "private"])
    args = ap.parse_args()

    eps = ([p.stem for p in sorted(META_DIR.glob("EP*.json"))]
           if args.all else [args.episode])
    if not eps or not eps[0]:
        fail("sebut episode (EP01) atau --all")

    media_dir = pathlib.Path(args.media_dir)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    results = [run(ep, media_dir, args.send, args.visibility) for ep in eps]

    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    log = LOG_DIR / f"{stamp}{'' if args.send else '-dryrun'}.json"
    log.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nlog: {log.relative_to(ROOT)}")

    if os.environ.get("GITHUB_STEP_SUMMARY"):
        lines = ["## Upload YouTube (Zernio)", "",
                 "| episode | status | tautan |", "|---|---|---|"]
        for r in results:
            lines.append(f"| {r['episode']} | {'dry-run' if r['dry_run'] else r.get('status')} "
                         f"| {r.get('youtube_url') or '—'} |")
        pathlib.Path(os.environ["GITHUB_STEP_SUMMARY"]).write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
