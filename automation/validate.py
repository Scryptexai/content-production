#!/usr/bin/env python3
"""QC jadwal: pastikan 35 konten × 3 platform utuh, urut, dan bertanggal benar."""
import json
from collections import Counter
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
cal = json.loads((ROOT / "automation/zernio/content/calendar.json").read_text(encoding="utf-8"))
scripts = json.loads((ROOT / "content/scripts.json").read_text(encoding="utf-8"))["contents"]
drafts = cal["drafts"]
errs = []

if len(scripts) != 35:
    errs.append(f"scripts.json harus 35, ada {len(scripts)}")
if len(drafts) != 105:
    errs.append(f"calendar harus 105 draf, ada {len(drafts)}")

per_content = Counter(d["contentId"] for d in drafts)
for cid, n in per_content.items():
    if n != 3:
        errs.append(f"{cid}: {n} platform (harus 3)")

ids = {c["id"] for c in scripts}
for cid in per_content:
    if cid not in ids:
        errs.append(f"draf untuk konten tak dikenal: {cid}")

fields = ["id", "contentId", "channelId", "platform", "publishAt", "title", "body", "media"]
for d in drafts:
    for f in fields:
        if not d.get(f):
            errs.append(f"{d.get('id')}: field kosong {f}")
    if d["status"] != "DRAFT":
        errs.append(f"{d['id']}: status bukan DRAFT")
    if len(d["title"]) > 100:
        errs.append(f"{d['id']}: judul {len(d['title'])} karakter (>100, akan terpotong)")
    if not d["publishAt"].endswith("Z"):
        errs.append(f"{d['id']}: publishAt bukan UTC")

# slot: 5 per hari, 7 hari, jam sesuai
by_day = Counter(d["publishAtWib"][:10] for d in drafts)
for day, n in sorted(by_day.items()):
    if n != 15:
        errs.append(f"{day}: {n} draf (harus 15 = 5 konten × 3 platform)")

slots = sorted({d["publishAtWib"][11:] for d in drafts})
if slots != ["06:30", "11:45", "16:30", "20:00", "21:30"]:
    errs.append(f"slot tidak sesuai: {slots}")

# urutan waktu naik & tidak ada duplikat judul+platform+jam
times = [datetime.fromisoformat(d["publishAt"].replace("Z", "+00:00")) for d in drafts]
if times != sorted(times):
    errs.append("draf tidak urut waktu")

trips = Counter((d["contentId"], d["platform"]) for d in drafts)
dups = [k for k, v in trips.items() if v > 1]
if dups:
    errs.append(f"duplikat konten+platform: {dups}")

# caption platform
for d in drafts:
    if d["platform"] == "tiktok" and len(d["body"]) > 2200:
        errs.append(f"{d['id']}: caption TikTok >2200 karakter")
    if d["platform"] == "instagram" and len(d["body"]) > 2200:
        errs.append(f"{d['id']}: caption IG >2200 karakter")
    if d["platform"] == "youtube" and len(d["body"]) > 5000:
        errs.append(f"{d['id']}: deskripsi YouTube >5000 karakter")

if errs:
    print(f"✗ {len(errs)} masalah")
    for e in errs:
        print("  -", e)
    raise SystemExit(1)
print(f"✓ {len(drafts)} draf valid · {len(scripts)} konten · {len(by_day)} hari · slot {', '.join(slots)}")
