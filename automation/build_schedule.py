#!/usr/bin/env python3
"""Bangun jadwal 7 hari dari content/scripts.json.

Menghasilkan:
  content/day-01.md … day-07.md          skrip yang dibaca manusia
  content/calendar-7-days.md             ringkasan 35 konten
  automation/zernio/content/calendar.json  105 draf (35 video x 3 platform)
  automation/zernio/content/schedule.csv   versi lembar kerja

Aturan:
  - 5 konten/hari: 3 beauty (06:30, 16:30, 21:30 WIB) + 2 relationship (11:45, 20:00 WIB)
  - setiap konten jadi 3 draf: youtube, tiktok, instagram
  - publishAt disimpan UTC (WIB = UTC+7); status DRAFT, autoPublish false
  - tidak ada kredensial di sini; channel id platform diisi di .env mesin publish
"""
import json
import csv
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "content" / "scripts.json"
ZDIR = ROOT / "automation" / "zernio"
CALENDAR = ZDIR / "content" / "calendar.json"
CSVOUT = ZDIR / "content" / "schedule.csv"

WIB = timezone(timedelta(hours=7))
DAY1 = datetime(2026, 11, 2, tzinfo=WIB)  # Senin

SLOTS = [  # (waktu WIB, niche)
    ("06:30", "beauty"),
    ("11:45", "relationship"),
    ("16:30", "beauty"),
    ("20:00", "relationship"),
    ("21:30", "beauty"),
]

PLATFORMS = ["youtube", "tiktok", "instagram"]

# tag tambahan per platform (di luar tag inti per niche)
EXTRA_TAGS = {
    "beauty": {
        "tiktok": ["#skincareindonesia", "#ilmukulit"],
        "instagram": ["#skincaretropis", "#skintellectual", "#skincareindonesia", "#bahanaktif", "#spfsetiaphari"],
        "youtube": ["#skincare", "#skincaretropis"],
    },
    "relationship": {
        "tiktok": ["#psikologihubungan", "#hubungansehat"],
        "instagram": ["#psikologihubungan", "#hubungansehat", "#komunikasipasangan", "#selfawareness", "#mentalhealthindonesia"],
        "youtube": ["#psikologihubungan", "#hubungansehat"],
    },
}

DISCLOSURE = (
    "Bukan saran medis · narasi & grafik dibuat dengan bantuan AI · "
    "tidak ada afiliasi tersembunyi"
)


def load():
    data = json.loads(SCRIPTS.read_text(encoding="utf-8"))
    items = data["contents"]
    assert len(items) == 35, f"harus 35 konten, ada {len(items)}"
    beauty = [c for c in items if c["niche"] == "beauty"]
    rel = [c for c in items if c["niche"] == "relationship"]
    assert len(beauty) == 21, len(beauty)
    assert len(rel) == 14, len(rel)
    return data, items


def slot_map(items):
    """Tentukan (hari, slot) deterministik: beauty 3/hari, relationship 2/hari."""
    out = {}
    b = sorted([c for c in items if c["niche"] == "beauty"], key=lambda c: c["id"])
    r = sorted([c for c in items if c["niche"] == "relationship"], key=lambda c: c["id"])
    for i, c in enumerate(b):
        out[c["id"]] = (i // 3 + 1, [0, 2, 4][i % 3])
    for i, c in enumerate(r):
        out[c["id"]] = (i // 2 + 1, [1, 3][i % 2])
    return out


def publish_at(day: int, slot: int) -> datetime:
    hh, mm = SLOTS[slot][0].split(":")
    dt = DAY1 + timedelta(days=day - 1)
    return dt.replace(hour=int(hh), minute=int(mm))


def caption_for(c, platform: str) -> tuple[str, str]:
    niche = c["niche"]
    tags = list(dict.fromkeys(c["hashtags"] + EXTRA_TAGS[niche][platform]))
    if platform == "tiktok":
        body = f"{c['caption']}\n\n{' '.join(tags[:6])}"
        return c["title"], body
    if platform == "instagram":
        body = (
            f"{c['caption']}\n\n{c['tool']}\n\n"
            f"{' '.join(tags[:12])}\n\n{DISCLOSURE}"
        )
        return c["title"], body
    body = (
        f"{c['caption']}\n\n"
        f"{c['tool']}\n\n"
        f"Sumber: {c['source']}\n\n"
        f"Seri: {c['series']}\n\n"
        f"{DISCLOSURE}\n"
        f"{' '.join(tags[:5])}"
    )
    return c["title"][:100], body


def main():
    data, items = load()
    slots = slot_map(items)
    drafts = []

    for c in items:
        day, slot = slots[c["id"]]
        when = publish_at(day, slot)
        for platform in PLATFORMS:
            title, body = caption_for(c, platform)
            drafts.append({
                "id": f"{c['id'].lower()}-{platform[:2]}",
                "contentId": c["id"],
                "niche": c["niche"],
                "series": c["series"],
                "channelId": f"{c['niche']}-{platform}",
                "platform": platform,
                "publishAt": when.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"),
                "publishAtWib": when.strftime("%Y-%m-%d %H:%M"),
                "status": "DRAFT",
                "title": title,
                "body": body,
                "hook": c["hook"],
                "durationSec": c["durationSec"],
                "media": {
                    "video": f"/assets/video/{c['id']}.mp4",
                    "poster": f"/assets/video/{c['id']}.jpg",
                },
                "reviewNote": "Draf otomatis M2; butuh approve pemilik sebelum dijadwalkan.",
            })

    drafts.sort(key=lambda d: (d["publishAt"], d["channelId"]))
    CALENDAR.write_text(json.dumps({
        "meta": {
            "generatedBy": "automation/build_schedule.py",
            "startDate": DAY1.date().isoformat(),
            "days": 7,
            "contents": len(items),
            "drafts": len(drafts),
            "timezone": "UTC",
            "note": "Semua draf berstatus DRAFT. Tidak ada autoPublish.",
        },
        "drafts": drafts,
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    with CSVOUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["publishAtWib", "contentId", "niche", "platform", "title", "durationSec", "status"])
        for d in drafts:
            w.writerow([d["publishAtWib"], d["contentId"], d["niche"], d["platform"], d["title"], d["durationSec"], d["status"]])

    # ---- markdown per hari
    for day in range(1, 8):
        rows = [c for c in items if slots[c["id"]][0] == day]
        rows.sort(key=lambda c: slots[c["id"]][1])
        lines = [f"# Hari {day} — {DAY1.date() + timedelta(days=day - 1)}", ""]
        lines.append("| Slot WIB | ID | Niche | Judul | Durasi |")
        lines.append("|---|---|---|---|---|")
        for c in rows:
            lines.append(f"| {SLOTS[slots[c['id']][1]][0]} | {c['id']} | {c['niche']} | {c['title']} | {c['durationSec']}s |")
        lines.append("")
        for c in rows:
            lines.append("---")
            lines.append("")
            lines.append(f"## {c['id']} · {c['title']}")
            lines.append("")
            lines.append(f"**Niche:** {c['niche']} · **Seri:** {c['series']} · "
                         f"**Slot:** {SLOTS[slots[c['id']][1]][0]} WIB · **Durasi:** ~{c['durationSec']} dtk")
            lines.append("")
            lines.append(f"**Hook (0–3 dtk):** {c['hook']}")
            lines.append("")
            lines.append("**VO:**")
            lines.append("")
            for i, beat in enumerate(c["vo"], 1):
                lines.append(f"{i}. {beat}")
            lines.append("")
            lines.append("**Teks di layar:** " + " · ".join(f"`{t}`" for t in c["onscreen"]))
            lines.append("")
            lines.append(f"**Visual:** {c['visual']}")
            lines.append("")
            lines.append(f"**Alat/penutup:** {c['tool']}")
            lines.append("")
            lines.append(f"**Caption:** {c['caption']}")
            lines.append("")
            lines.append("**Hashtag inti:** " + " ".join(c["hashtags"]))
            lines.append("")
            lines.append(f"**Sumber:** {c['source']}")
            lines.append("")
        (ROOT / "content" / f"day-0{day}.md").write_text("\n".join(lines), encoding="utf-8")

    # ---- ringkasan
    out = ["# Kalender 7 hari — 35 konten, 105 post", "",
           "Dibuat oleh `automation/build_schedule.py` dari `content/scripts.json`.",
           "Semua jam WIB. Konten yang sama tayang di 3 platform dengan caption berbeda.", "",
           "| Hari | 06:30 | 11:45 | 16:30 | 20:00 | 21:30 |", "|---|---|---|---|---|---|"]
    for day in range(1, 8):
        cells = []
        for slot in range(5):
            hit = [c for c in items if slots[c["id"]] == (day, slot)]
            cells.append(f"{hit[0]['id']} {hit[0]['title']}" if hit else "—")
        out.append(f"| {day} | " + " | ".join(cells) + " |")
    out += ["", f"Total: **{len(items)} video × 3 platform = {len(drafts)} post**.", "",
            "Cek duplikasi: satu video = satu file `assets/video/{ID}.mp4`, tiga caption."]
    (ROOT / "content" / "calendar-7-days.md").write_text("\n".join(out), encoding="utf-8")

    print(f"ok: {len(items)} konten, {len(drafts)} draf → {CALENDAR.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
