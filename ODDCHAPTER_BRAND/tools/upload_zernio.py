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


def api_post(path, payload, key, timeout=120, extra_headers=None, attempts=4):
    """POST JSON. 409/429/5xx dicoba ulang dengan header yang sama persis.

    Zernio membuat post dalam <Idempotency-Key> selama 24 jam: percobaan ulang
    dengan kunci yang sama mengembalikan post yang sudah ada (HTTP 200), bukan
    membuat video kedua. Itu satu-satunya cara aman mengulang setelah timeout,
    karena kita tidak pernah tahu apakah request pertama sampai.
    """
    body = json.dumps(payload).encode("utf-8")
    headers = {"Authorization": f"Bearer {key}",
               "Content-Type": "application/json",
               "Accept": "application/json"}
    headers.update(extra_headers or {})

    for attempt in range(1, attempts + 1):
        req = urllib.request.Request(f"{API}{path}", data=body, method="POST", headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                data = json.loads(r.read().decode("utf-8") or "{}")
                data["_http_status"] = r.status
                return data
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", "replace")[:900]
            retry_after = e.headers.get("Retry-After") if e.headers else None
            transient = e.code in (409, 429, 500, 502, 503, 504)
            if transient and attempt < attempts:
                wait = float(retry_after) if (retry_after or "").strip().isdigit() else 2 ** attempt
                print(f"  HTTP {e.code} · coba lagi dalam {wait:.0f} dtk "
                      f"(percobaan {attempt}/{attempts}) · {detail[:160]}")
                time.sleep(wait)
                continue
            if e.code == 401:
                fail(f"POST {path} → 401 Unauthorized. ZERNIO_API_KEY salah atau dicabut. {detail}")
            if e.code == 403:
                fail(f"POST {path} → 403. API key ini tidak punya akses ke accountId "
                     f"tersebut. {detail}")
            if e.code == 400 and "accountId" in detail:
                fail(f"POST {path} → 400. accountId tidak dikenal Zernio — cek "
                     f"GET /v1/profiles dan perbarui secret. {detail}")
            fail(f"POST {path} → HTTP {e.code}: {detail}")
        except urllib.error.URLError as e:
            if attempt < attempts:
                wait = 2 ** attempt
                print(f"  jaringan gagal ({e.reason}) · coba lagi dalam {wait} dtk")
                time.sleep(wait)
                continue
            fail(f"POST {path} → jaringan gagal: {e.reason}. Post mungkin sudah dibuat; "
                 f"periksa dashboard Zernio sebelum menjalankan ulang.")


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


def idempotency_key(ep, meta):
    """Kunci tetap per episode+file: aman diulang, tidak bisa jadi dua video.

    Berbasis sha256 master (bukan waktu), jadi menjalankan ulang workflow untuk
    file yang sama akan mengembalikan post yang sama selama 24 jam. Render baru
    menghasilkan hash baru — dan memang boleh jadi video baru.
    """
    basis = (meta.get("sha256") or "") + "|" + meta.get("title", "")
    digest = hashlib.sha256(basis.encode("utf-8")).hexdigest()[:32]
    return f"oddc-{ep.lower()}-{digest}"


def api_get(path, key, timeout=60):
    req = urllib.request.Request(f"{API}{path}", method="GET",
                                 headers={"Authorization": f"Bearer {key}",
                                          "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode("utf-8") or "{}")
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")[:400]
        fail(f"GET {path} → HTTP {e.code}: {detail}. Kalau 401, ZERNIO_API_KEY salah.")


def discover_accounts(key):
    """Cari akun YouTube dari API, bukan dari tebakan di secret.

    Bentuk respons Zernio berbeda antar endpoint (/accounts datar, /profiles
    berisi platforms[]), jadi keduanya dicoba dan hasilnya disamaratakan.
    """
    out = []
    for path in ("/accounts", "/profiles"):
        try:
            data = api_get(path, key)
        except SystemExit:
            continue
        raw = data.get("accounts") or data.get("profiles") or data.get("data") or []
        if isinstance(raw, dict):
            raw = raw.get("accounts") or raw.get("profiles") or []
        for item in raw if isinstance(raw, list) else []:
            if not isinstance(item, dict):
                continue
            if (item.get("platform") or "").lower() == "youtube":
                out.append(item)
            for child in (item.get("platforms") or item.get("accounts") or []):
                if isinstance(child, dict) and (child.get("platform") or "").lower() == "youtube":
                    merged = {**item, **child}
                    merged.setdefault("profileName", item.get("name"))
                    out.append(merged)
        if out:
            break
    seen, uniq = set(), []
    for acc in out:
        aid = acc.get("accountId") or acc.get("_id") or acc.get("id")
        if not aid or aid in seen:
            continue
        if acc.get("isActive") is False or acc.get("status") == "inactive":
            continue
        seen.add(aid)
        uniq.append({
            "accountId": aid,
            "name": acc.get("username") or acc.get("name") or acc.get("handle") or "?",
            "profile": acc.get("profileName") or acc.get("profile") or "-",
        })
    return uniq


def resolve_account(key, want=None):
    """env → permintaan → pencarian otomatis. Yang terakhir jadi andalan."""
    want = (want or os.environ.get("ZERNIO_YOUTUBE_ACCOUNT_ID", "")).strip()
    accounts = discover_accounts(key)
    ids = {a["accountId"] for a in accounts}

    if want and want in ids:
        return want
    if want and not ids:
        print(f"  ! daftar akun tidak terbaca; memakai ZERNIO_YOUTUBE_ACCOUNT_ID={want}")
        return want
    if want and want not in ids:
        print(f"  ! ZERNIO_YOUTUBE_ACCOUNT_ID={want} tidak ada di akun Zernio; "
              f"memakai akun yang ditemukan otomatis.")
    if not accounts:
        fail("Tidak ada akun YouTube di API key ini. Hubungkan kanal dulu: "
             "Zernio → Accounts → Connect → YouTube.")
    chosen = accounts[0]
    print(f"  akun YouTube dipakai: {chosen['accountId']} ({chosen['name']})")
    return chosen["accountId"]


def check_account():
    """Sebelum 20 MB diunggah: pastikan key hidup dan kanal YouTube-nya ketemu."""
    key = os.environ.get("ZERNIO_API_KEY", "").strip() or os.environ.get("ZERNIO_KEY", "").strip()
    if not key:
        fail("ZERNIO_API_KEY kosong. Di Actions: Settings → Secrets → Actions.")
    accounts = discover_accounts(key)
    if not accounts:
        fail("API key hidup, tapi tidak ada akun YouTube yang tersambung.")
    print(f"  {len(accounts)} akun YouTube di API key ini:")
    want = os.environ.get("ZERNIO_YOUTUBE_ACCOUNT_ID", "").strip()
    for acc in accounts:
        mark = "  ← dipakai" if acc["accountId"] == want else ""
        print(f"    {acc['accountId']}  {acc['name']}  [{acc['profile']}]{mark}")
    if want and want not in {a["accountId"] for a in accounts}:
        print("  ! secret ZERNIO_YOUTUBE_ACCOUNT_ID tidak cocok — akun pertama akan "
              "dipakai otomatis, jadi unggahan tetap jalan.")
    print("  siap.")


# ---------- buku besar: mencegah satu episode terunggah dua kali ----------
LEDGER = ROOT / "11_CONTENT" / "06_UPLOAD" / "published.json"


def load_ledger():
    if not LEDGER.exists():
        return {}
    try:
        data = json.loads(LEDGER.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def save_ledger(ledger):
    LEDGER.write_text(json.dumps(ledger, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                      encoding="utf-8")


def load_request(path):
    req = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
    ep = req.get("episode")
    if not ep:
        fail(f"{path}: tidak ada field 'episode'")
    return ep, req


def load_meta(ep):
    p = META_DIR / f"{ep}.json"
    if not p.exists():
        fail(f"metadata tidak ada: {p.relative_to(ROOT)}")
    return json.loads(p.read_text(encoding="utf-8"))


# Bukan aturan YouTube, aturan kanal: judul harus bisa dibaca di 40 karakter
# pertama (di feed Shorts selebihnya terpotong), dan tanpa kata yang sudah
# dipakai semua orang sampai tidak berarti apa-apa lagi.
CLICHE = ("misteri", "ternyata", "fakta mengejutkan", "jangan percaya", "auto")
WARNS = []


def style(title):
    w = []
    if not any(ch.isdigit() for ch in title[:40]):
        w.append("angka/tanggal tidak muncul di 40 karakter pertama — di feed Shorts "
                 "sisanya terpotong, jadi detail mustahilnya tidak terbaca")
    low = title.lower()
    for c in CLICHE:
        if c in low:
            w.append(f"judul memuat “{c}” — kata yang sudah dipakai semua kanal, tidak memilih siapa pun")
    if title.isupper():
        w.append("judul huruf besar semua — terbaca seperti iklan, bukan cerita")
    return w


def validate(meta, media_dir, check_media=True):
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
    if check_media:
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

    if title.strip():
        WARNS.extend(style(title))
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


def run(ep, media_dir, send, visibility, check_media=True, request=None, force=False):
    WARNS.clear()
    meta = load_meta(ep)
    print(f"\n=== {ep} · {meta['title']} ({len(meta['title'])} karakter) ===")
    validate(meta, media_dir, check_media)

    key = (os.environ.get("ZERNIO_API_KEY", "").strip()
           or os.environ.get("ZERNIO_KEY", "").strip())
    visibility = visibility or (request or {}).get("visibility")
    force = force or bool((request or {}).get("force"))
    ledger = load_ledger()
    if send and ep in ledger and not force:
        print(f"  dilewati: {ep} sudah tayang {ledger[ep].get('uploaded_at')} · "
              f"{ledger[ep].get('youtube_url')} (pakai --force untuk mengulang)")
        return {"episode": ep, "skipped": True, **ledger[ep]}

    for w in WARNS:
        print(f"::warning file=11_CONTENT/06_UPLOAD/{ep}.json::{w}"
              if os.environ.get("GITHUB_ACTIONS") else f"  ! {w}")

    if not send:
        payload = build_payload(meta, f"<publicUrl {meta['video']}>",
                                f"<publicUrl {meta['thumbnail']}>", visibility)
        payload["platforms"][0]["accountId"] = (
            os.environ.get("ZERNIO_YOUTUBE_ACCOUNT_ID", "").strip()
            or "<akun YouTube, dicari otomatis dari GET /v1/accounts>")
        if not check_media:
            print("  catatan: --text-only — file video/thumbnail TIDAK diperiksa. "
                  "Jalankan tanpa flag ini sebelum --send.")
        print("  dry-run: tidak ada yang dikirim. Payload POST /v1/posts:")
        print("\n".join("    " + l for l in json.dumps(payload, ensure_ascii=False, indent=2).splitlines()))
        return {"episode": ep, "dry_run": True, "payload": payload}

    if not key:
        fail("ZERNIO_API_KEY kosong — tambahkan sebagai secret repo, jangan di file")
    account = resolve_account(key, (request or {}).get("accountId"))
    os.environ["ZERNIO_YOUTUBE_ACCOUNT_ID"] = account

    video_url = upload_media(media_dir / meta["video"], key, "video")
    thumb_url = upload_media(media_dir / meta["thumbnail"], key, "thumbnail")

    payload = build_payload(meta, video_url, thumb_url, visibility)
    idem = idempotency_key(ep, meta)
    print(f"  POST /v1/posts · Idempotency-Key: {idem}")
    result = api_post("/posts", payload, key, extra_headers={"Idempotency-Key": idem})

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
        "idempotency_key": idem,
        "uploaded_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    print(f"  published: {out['status']} · {out['youtube_url']}")
    if ep in ledger:
        print(f"  catatan: {ep} sudah ada di buku besar ({ledger[ep].get('youtube_url')}); "
              f"catatan lama TIDAK ditimpa. Salinan ini: {out['youtube_url']}")
    else:
        ledger[ep] = {"post_id": out["post_id"], "status": out["status"],
                      "youtube_url": out["youtube_url"], "uploaded_at": out["uploaded_at"],
                      "title": out["title"]}
        save_ledger(ledger)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("episode", nargs="?", help="EP01, EP02, …")
    ap.add_argument("--all", action="store_true", help="semua metadata di 06_UPLOAD")
    ap.add_argument("--media-dir", default=str(ROOT / "10_FILM" / "remotion" / "output" / "episodes"))
    ap.add_argument("--send", action="store_true", help="benar-benar unggah (tanpa ini = dry-run)")
    ap.add_argument("--visibility", choices=["public", "unlisted", "private"])
    ap.add_argument("--request", help="berkas antrean (11_CONTENT/06_UPLOAD/queue/*.json)")
    ap.add_argument("--force", action="store_true",
                    help="abaikan buku besar: unggah walau episode sudah tayang")
    ap.add_argument("--check", action="store_true",
                    help="uji ZERNIO_API_KEY + ZERNIO_YOUTUBE_ACCOUNT_ID lewat GET /v1/profiles")
    ap.add_argument("--text-only", action="store_true",
                    help="dry-run hanya untuk teks: lewati pemeriksaan file/hash "
                         "(dipakai saat master belum ada di mesin ini)")
    args = ap.parse_args()

    if args.check:
        print("cek kredensial Zernio")
        check_account()
        return 0

    request = None
    if args.request:
        ep_from_request, request = load_request(args.request)
        args.episode = ep_from_request
        print(f"permintaan: {args.request} → {ep_from_request} "
              f"(status {(request.get('status') or '?')})")

    eps = ([p.stem for p in sorted(META_DIR.glob("EP*.json"))]
           if args.all else [args.episode])
    if not eps or not eps[0]:
        fail("sebut episode (EP01) atau --all")

    media_dir = pathlib.Path(args.media_dir)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    if args.text_only and args.send:
        fail("--text-only hanya untuk dry-run; jangan digabung dengan --send")
    results = [run(ep, media_dir, args.send, args.visibility, not args.text_only,
                   request, args.force)
               for ep in eps]

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
