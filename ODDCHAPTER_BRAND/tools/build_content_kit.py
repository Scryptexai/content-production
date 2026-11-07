"""
build_content_kit.py — dari content_data.py ke artefak siap tayang.

Menghasilkan:
  02_SCRIPT/EPxx_*.md        21 script, satu file per episode
  02_SCRIPT/ALL_SCRIPTS.md   satu dokumen, untuk review cepat
  01_IDEA/CONTENT_CALENDAR.csv  jadwal 7 hari x 3 slot x 3 platform
  03_THUMBNAIL/EPxx_*.svg    template vektor (bisa diedit)
  03_THUMBNAIL/EPxx_*.png    1080x1920 siap upload
  03_THUMBNAIL/CONTACT_SHEET.png
"""
import csv
import json
import math
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from content_data import EPISODES  # noqa: E402
import oclib  # noqa: E402
from oclib import INK, IVORY, ORANGE, SAGE, f, ring  # noqa: E402

ROOT = HERE.parent
CONTENT = ROOT / "11_CONTENT"
SCRIPTS = CONTENT / "02_SCRIPT"
THUMBS = CONTENT / "03_THUMBNAIL"
IDEAS = CONTENT / "01_IDEA"

SLOT_LABEL = {"pagi": "PAGI 07.00 WIB", "siang": "SIANG 12.30 WIB", "malam": "MALAM 19.30 WIB"}
POV_LABEL = {
    "A": "A — “KAMU” (orang kedua; penonton berdiri di dalam adegan)",
    "B": "B — “SAKSI” (orang ketiga + arsip; yang dibicarakan adalah bukti)",
    "D": "D — “KITA” (kolektif; yang dibicarakan adalah asumsi bersama)",
}
PLATFORMS = [
    ("TikTok", "vertikal 1080x1920, caption <=150 karakter, 3–5 hashtag"),
    ("YouTube Shorts", "judul <=60 karakter, deskripsi 2 baris + sumber"),
    ("Facebook Reels", "caption 1 kalimat hook + 1 kalimat loop, tanpa link"),
]


def slug(s):
    keep = []
    for ch in s.lower():
        if ch.isalnum():
            keep.append(ch)
        elif keep and keep[-1] != "-":
            keep.append("-")
    out = "".join(keep).strip("-")
    if len(out) > 52:
        out = out[:52]
        if "-" in out:
            out = out[:out.rindex("-")]
    return out.rstrip("-")


# ---------------------------------------------------------------- script docs
def episode_md(e):
    n = int(e["ep"][2:])
    total = e["durasi"]
    lines = [
        f"# {e['ep']} — {e['title']}",
        "",
        f"**Headline:** {e['title']}  ",
        f"**Seri:** {e['series']} · **Slot:** {SLOT_LABEL[e['slot']]} · **Hari:** H{e['day']}  ",
        f"**POV:** {POV_LABEL[e['pov']]}  ",
        f"**Durasi target:** {total} detik · **Kata VO:** {sum(len(b[1].split()) for b in e['beats'])}",
        "",
        "---",
        "",
        "## 1 · HOOK (0–3 s)",
        "",
        f"> {e['hook']}",
        "",
        "Visual pembuka: satu objek, tanpa gerakan kamera. Teks hook tidak boleh sama",
        "dengan kalimat VO — teks di layar memotong, bukan mengulang.",
        "",
        "## 2 · BEAT (3 s → selesai)",
        "",
        "| detik | VO |",
        "|---|---|",
    ]
    for t, txt in e["beats"]:
        lines.append(f"| {t:02d} | {txt} |")
    lines += [
        "",
        f"## 3 · TITIK BALIK",
        "",
        f"> {e['turn']}",
        "",
        "## 4 · LOOP (kalimat terakhir, harus menyambung ke hook)",
        "",
        f"> {e['loop']}",
        "",
        "## 5 · TEKS DI LAYAR",
        "",
    ]
    for i, c in enumerate(e["cues"], 1):
        lines.append(f"{i}. `{c}`")
    lines += [
        "",
        "Maksimal lima cue. Setiap cue tampil 1,5–2 detik, huruf kapital, Inter 600.",
        "",
        "## 6 · VISUAL SIGNATURE",
        "",
        e["visual"],
        "",
        "Detail lengkap ada di `05_VISUAL_PLAN.md` (dibuat setelah thumbnail disetujui).",
        "",
        "## 7 · DISTRIBUSI",
        "",
        "| platform | format |",
        "|---|---|",
    ]
    for p, note in PLATFORMS:
        lines.append(f"| {p} | {note} |")
    lines += [
        "",
        "Satu episode, tiga platform, satu file master vertikal. Tidak ada versi horizontal.",
        "",
        "## 8 · SUMBER",
        "",
        f"`SRC: NEEDS-SOURCE` — {e['sumber']}",
        "",
        "Status `NEEDS-SOURCE` berarti script ini **belum boleh tayang** sampai rujukan",
        "primernya dibaca dan baris ini diubah jadi `VERIFIED` (lihat `00_STRATEGI.md` §6).",
        "",
        "## 9 · HOOK ALTERNATIF (untuk A/B)",
        "",
        f"- {e['hook_alt']}",
        "",
        "---",
        "",
        f"*Hook A/B diuji di 3 detik pertama. Yang menang di retensi 3 detik dipakai permanen.*",
    ]
    return "\n".join(lines), n


def write_scripts():
    SCRIPTS.mkdir(parents=True, exist_ok=True)
    index = []
    for e in EPISODES:
        md, n = episode_md(e)
        name = f"{e['ep']}_{slug(e['title'])}.md"
        (SCRIPTS / name).write_text(md)
        index.append((e, name))
    # satu dokumen gabungan
    big = [
        "# ODDCHAPTER — 21 SCRIPT, 7 HARI",
        "",
        "Satu episode = satu hari-slot = tiga platform. Semua script di bawah memakai",
        "struktur yang sama (HOOK 0–3 · BEAT · TITIK BALIK · LOOP) dan semuanya masih",
        "berstatus `NEEDS-SOURCE` sampai rujukannya dibaca.",
        "",
        "| # | Hari | Slot | Seri | Headline | POV | Detik |",
        "|---|---|---|---|---|---|---|",
    ]
    for e, _ in index:
        big.append(f"| {int(e['ep'][2:])} | H{e['day']} | {e['slot']} | {e['series']} | "
                   f"{e['title']} | {e['pov']} | {e['durasi']} |")
    for e, name in index:
        md, _ = episode_md(e)
        big += ["", "---", "", md.replace("# ", "## ", 1)]
    (SCRIPTS / "ALL_SCRIPTS.md").write_text("\n".join(big))
    print(f"scripts: {len(index)} file + ALL_SCRIPTS.md")
    return index


def write_calendar():
    IDEAS.mkdir(parents=True, exist_ok=True)
    rows = []
    for e in sorted(EPISODES, key=lambda x: (x["day"], ["pagi", "siang", "malam"].index(x["slot"]))):
        for platform, note in PLATFORMS:
            rows.append({
                "hari": f"H{e['day']}",
                "tanggal_relatif": f"H+{e['day']-1}",
                "jam_wib": e["jam"],
                "slot": e["slot"],
                "episode": e["ep"],
                "headline": e["title"],
                "seri": e["series"],
                "pov": e["pov"],
                "platform": platform,
                "format": note,
                "durasi_detik": e["durasi"],
                "status_sumber": "NEEDS-SOURCE",
                "thumbnail": f"03_THUMBNAIL/{e['ep']}_{slug(e['title'])}.png",
                "script": f"02_SCRIPT/{e['ep']}_{slug(e['title'])}.md",
            })
    path = IDEAS / "CONTENT_CALENDAR.csv"
    with path.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    (IDEAS / "CONTENT_CALENDAR.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2))
    print(f"calendar: {len(rows)} baris ({len(EPISODES)} episode x {len(PLATFORMS)} platform)")


# ---------------------------------------------------------------- thumbnails
def measure(txt, size, weight=700, family="grotesk"):
    """Perkiraan lebar teks, cukup akurat untuk Space Grotesk caps / Inter."""
    narrow = set("IİJ1·|")
    wide = set("MWQ@")
    total = 0.0
    for ch in txt:
        if ch in narrow:
            total += 0.30
        elif ch in wide:
            total += 0.82
        elif ch == " ":
            total += 0.24
        elif ch.isupper():
            total += 0.64 if family == "grotesk" else 0.63
        else:
            total += 0.52 if family == "grotesk" else 0.50
    return total * size


def wrap(txt, size, maxw, **kw):
    words, lines, cur = txt.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if measure(trial, size, **kw) <= maxw or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def motif(series, cx, cy, w, h):
    """Satu lambang geometris per seri. Tidak ada ilustrasi literal — semuanya
    bisa digambar ulang sebagai vektor di Remotion tanpa aset luar."""
    g = []
    O = ORANGE
    if series == "HILANG":
        # menara + berkas cahaya + satu sosok yang tidak lagi di tempatnya
        base, top = cy + h * 0.36, cy - h * 0.30
        g.append(f'<line x1="{f(cx-w*0.46)}" y1="{f(base)}" x2="{f(cx+w*0.46)}" y2="{f(base)}" stroke="{SAGE}" stroke-width="1.6" opacity="0.42"/>')
        for i in range(1, 7):
            yy = base + i * 11
            g.append(f'<line x1="{f(cx-w*0.46)}" y1="{f(yy)}" x2="{f(cx+w*0.46)}" y2="{f(yy)}" stroke="{SAGE}" '
                     f'stroke-width="1" opacity="{max(0.02, 0.17 - i*0.023):.3f}"/>')
        g.append(f'<path d="M {f(cx-64)} {f(base)} L {f(cx-32)} {f(top)} L {f(cx+32)} {f(top)} L {f(cx+64)} {f(base)} Z" '
                 f'fill="{INK}" stroke="{IVORY}" stroke-width="2.6"/>')
        g.append(f'<rect x="{f(cx-44)}" y="{f(top-52)}" width="88" height="52" fill="{INK}" stroke="{IVORY}" stroke-width="2.6"/>')
        g.append(f'<path d="M {f(cx-52)} {f(top-52)} L {f(cx)} {f(top-96)} L {f(cx+52)} {f(top-52)} Z" fill="{INK}" stroke="{IVORY}" stroke-width="2.6"/>')
        g.append(f'<circle cx="{f(cx)}" cy="{f(top-26)}" r="9" fill="{O}"/>')
        g.append(f'<path d="M {f(cx-30)} {f(top-40)} L {f(cx-w*0.44)} {f(top-118)} L {f(cx-w*0.44)} {f(top-4)} Z" fill="{O}" opacity="0.12"/>')
        g.append(f'<path d="M {f(cx+30)} {f(top-40)} L {f(cx+w*0.44)} {f(top-118)} L {f(cx+w*0.44)} {f(top-4)} Z" fill="{O}" opacity="0.07"/>')
        # sosok kecil, punggung menghadap kamera
        px, py = cx + w * 0.30, base
        g.append(f'<circle cx="{f(px)}" cy="{f(py-56)}" r="7" fill="{SAGE}"/>')
        g.append(f'<line x1="{f(px)}" y1="{f(py-49)}" x2="{f(px)}" y2="{f(py-16)}" stroke="{SAGE}" stroke-width="3"/>')
        g.append(f'<line x1="{f(px)}" y1="{f(py-16)}" x2="{f(px-9)}" y2="{f(py)}" stroke="{SAGE}" stroke-width="3"/>')
        g.append(f'<line x1="{f(px)}" y1="{f(py-16)}" x2="{f(px+9)}" y2="{f(py)}" stroke="{SAGE}" stroke-width="3"/>')
    elif series == "TERSEMBUNYI":
        # pintu yang terbuka sedikit — cahaya keluar, bukan masuk
        dw, dh = w * 0.34, h * 0.74
        for i, r in enumerate((w * 0.52, w * 0.44, w * 0.36)):
            g.append(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="none" stroke="{SAGE}" stroke-width="1" opacity="{0.14 - i*0.03:.2f}"/>')
        g.append(f'<rect x="{f(cx-dw/2)}" y="{f(cy-dh/2)}" width="{f(dw)}" height="{f(dh)}" fill="{INK}" stroke="{IVORY}" stroke-width="2.6"/>')
        g.append(f'<rect x="{f(cx-dw/2+14)}" y="{f(cy-dh/2+14)}" width="{f(dw-28)}" height="{f(dh-28)}" fill="none" stroke="{SAGE}" stroke-width="1.2" opacity="0.5"/>')
        g.append(f'<path d="M {f(cx-dw/2+30)} {f(cy-dh/2+34)} L {f(cx+dw/2-64)} {f(cy-dh/2+58)} L {f(cx+dw/2-64)} {f(cy+dh/2-34)} L {f(cx-dw/2+30)} {f(cy+dh/2-34)} Z" fill="{IVORY}" opacity="0.06"/>')
        g.append(f'<path d="M {f(cx+dw/2-64)} {f(cy-dh/2+58)} L {f(cx+dw/2-30)} {f(cy-dh/2+42)} L {f(cx+dw/2-30)} {f(cy+dh/2-18)} L {f(cx+dw/2-64)} {f(cy+dh/2-34)} Z" fill="{O}" opacity="0.9"/>')
        for k in range(3):
            yy = cy - dh * 0.24 + k * dh * 0.22
            g.append(f'<line x1="{f(cx-dw/2+30)}" y1="{f(yy)}" x2="{f(cx+dw/2-64)}" y2="{f(yy)}" stroke="{SAGE}" stroke-width="1" opacity="0.22"/>')
    elif series == "ANEH":
        # satu sinyal yang muncul sekali, lalu tidak pernah mengulang
        bx = cy + h * 0.30
        g.append(f'<line x1="{f(cx-w*0.46)}" y1="{f(bx)}" x2="{f(cx+w*0.46)}" y2="{f(bx)}" stroke="{SAGE}" stroke-width="1.6" opacity="0.62"/>')
        for i in range(0, 25):
            x = cx - w * 0.44 + i * (w * 0.88 / 24)
            g.append(f'<line x1="{f(x)}" y1="{f(bx)}" x2="{f(x)}" y2="{f(bx+10)}" stroke="{SAGE}" stroke-width="1" opacity="0.30"/>')
        for k in range(3):
            amp = 126 - k * 26
            pts = []
            for i in range(0, 161):
                x = cx - w * 0.46 + (w * 0.92 * i / 160)
                ph = (i / 160) * math.pi * 5.0
                env = math.exp(-(((i / 160) - 0.5) ** 2) * 22)
                y = bx - 22 + math.sin(ph - k * 0.5) * amp * env
                pts.append(f"{f(x)},{f(y)}")
            col = O if k == 0 else SAGE
            op = 0.95 if k == 0 else 0.30 - k * 0.07
            g.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{col}" stroke-width="{3.0 if k==0 else 1.3}" opacity="{op:.2f}"/>')
        g.append(f'<line x1="{f(cx)}" y1="{f(bx-142)}" x2="{f(cx)}" y2="{f(bx-24)}" stroke="{O}" stroke-width="1.4" opacity="0.45" stroke-dasharray="7 7"/>')
    elif series == "BENCANA":
        # gelombang tekanan: sumbernya di luar bingkai
        ox, oy = cx, cy + h * 0.94
        g.append(f'<circle cx="{f(ox)}" cy="{f(oy)}" r="{f(h*0.52)}" fill="{INK}"/>')
        for i in range(-11, 12):
            a = math.radians(-90 + i * 4.6)
            x2 = ox + math.cos(a) * h * 1.9
            y2 = oy + math.sin(a) * h * 1.9
            col = O if i == 0 else SAGE
            op = 0.9 if i == 0 else max(0.06, 0.24 - abs(i) * 0.014)
            g.append(f'<line x1="{f(ox)}" y1="{f(oy)}" x2="{f(x2)}" y2="{f(y2)}" stroke="{col}" stroke-width="{2.6 if i==0 else 1.1}" opacity="{op:.2f}"/>')
        for r in (h * 0.42, h * 0.62, h * 0.84):
            g.append(f'<path d="M {f(ox-r)} {f(oy)} A {f(r)} {f(r)} 0 0 1 {f(ox+r)} {f(oy)}" fill="none" stroke="{O if r==h*0.42 else SAGE}" stroke-width="{2.0 if r==h*0.42 else 1.1}" opacity="{0.55 if r==h*0.42 else 0.20}"/>')
        g.append(f'<circle cx="{f(ox)}" cy="{f(oy)}" r="{f(h*0.52)}" fill="none" stroke="{SAGE}" stroke-width="1.2" opacity="0.30"/>')
        g.append(f'<circle cx="{f(ox)}" cy="{f(oy)}" r="10" fill="{O}"/>')
    else:  # HARGA
        n = 17
        for i in range(n):
            x = cx - w * 0.46 + i * (w * 0.92 / (n - 1))
            ln = 22 + (1 - (i / (n - 1))) * h * 0.30 + ((i * 53) % 26)
            op = 0.75 if i % 4 == 0 else 0.42
            g.append(f'<line x1="{f(x)}" y1="{f(cy-ln)}" x2="{f(x)}" y2="{f(cy+ln*0.5)}" stroke="{SAGE}" stroke-width="2.0" opacity="{op}"/>')
        g.append(f'<line x1="{f(cx-w*0.5)}" y1="{f(cy)}" x2="{f(cx+w*0.5)}" y2="{f(cy)}" stroke="{O}" stroke-width="3.0"/>')
        for i in range(5):
            x = cx + w * 0.10 + i * 26
            g.append(f'<circle cx="{f(x)}" cy="{f(cy + 52 + i*9)}" r="{f(6 - i*0.6)}" fill="{O}" opacity="{0.9 - i*0.16:.2f}"/>')
    return "\n".join(g)


def thumb_svg(e):
    W, H = 1080, 1920
    n = int(e["ep"][2:])
    L, R = 96, 984
    inner = W - 2 * 96
    parts = [
        '<defs>',
        '<linearGradient id="bg" x1="0" y1="0" x2="0.35" y2="1">',
        f'<stop offset="0" stop-color="#1E2126"/><stop offset="0.5" stop-color="{INK}"/><stop offset="1" stop-color="#0E1013"/>',
        '</linearGradient>',
        '<radialGradient id="glow" cx="0.5" cy="0.33" r="0.5">',
        f'<stop offset="0" stop-color="{IVORY}" stop-opacity="0.055"/><stop offset="1" stop-color="{IVORY}" stop-opacity="0"/>',
        '</radialGradient>',
        f'<clipPath id="frame"><rect x="0" y="0" width="{W}" height="{H}"/></clipPath>',
        '</defs>',
        '<g clip-path="url(#frame)">',
        f'<rect width="{W}" height="{H}" fill="url(#bg)"/>',
        f'<rect width="{W}" height="{H}" fill="url(#glow)"/>',
    ]
    # garis tepi editorial: memberi bingkai tanpa mengganggu teks
    parts.append(f'<line x1="{L-34}" y1="300" x2="{L-34}" y2="1560" stroke="{SAGE}" stroke-width="1" opacity="0.22"/>')
    parts.append(f'<line x1="{L-34}" y1="300" x2="{L-34+18}" y2="300" stroke="{SAGE}" stroke-width="1" opacity="0.45"/>')
    parts.append(f'<line x1="{L-34}" y1="1560" x2="{L-34+18}" y2="1560" stroke="{SAGE}" stroke-width="1" opacity="0.45"/>')
    # chip seri
    chip_txt = e["series"]
    chip_w = measure(chip_txt, 28, family="inter") + 46
    parts.append(f'<rect x="{L}" y="300" width="{f(chip_w)}" height="58" fill="{ORANGE}"/>')
    parts.append(f'<text x="{f(L + chip_w/2)}" y="340" font-family="Inter" font-weight="700" font-size="27" '
                 f'letter-spacing="3.4" text-anchor="middle" fill="{INK}">{chip_txt}</text>')
    parts.append(f'<text x="{R}" y="340" font-family="Inter" font-weight="600" font-size="27" letter-spacing="3.4" '
                 f'text-anchor="end" fill="{SAGE}" opacity="0.85">EP {n:02d} · H{e["day"]}</text>')
    # lambang seri
    parts.append(motif(e["series"], W / 2, 655, inner * 0.92, 350))
    # headline
    size = 158
    lines = e["thumb"]
    while size > 98 and max(measure(t, size) for t in lines) > inner:
        size -= 4
    lead = size * 1.00
    y0 = 1210 - (len(lines) - 1) * lead * 0.5
    for i, t in enumerate(lines):
        parts.append(f'<text x="{L}" y="{f(y0 + i*lead)}" font-family="Space Grotesk" font-weight="700" '
                     f'font-size="{size}" letter-spacing="-3" fill="{IVORY}">{esc(t)}</text>')
    # subline: satu kalimat, maksimal dua baris
    sub = e["hook"].split(". ")[0].rstrip(".")
    sub_lines = wrap(sub, 40, inner, family="inter")[:2]
    sy = y0 + (len(lines) - 1) * lead + 84
    for i, t in enumerate(sub_lines):
        parts.append(f'<text x="{L}" y="{f(sy + i*58)}" font-family="Inter" font-weight="500" font-size="41" '
                     f'fill="{SAGE}" opacity="0.95">{esc(t)}</text>')
    # kaki di dalam zona aman
    parts.append(f'<line x1="{L}" y1="1466" x2="{R}" y2="1466" stroke="{SAGE}" stroke-width="1.2" opacity="0.35"/>')
    parts.append(f'<text x="{L}" y="1516" font-family="Space Grotesk" font-weight="700" font-size="34" '
                 f'letter-spacing="9" fill="{IVORY}">ODDCHAPTER</text>')
    parts.append(f'<text x="{R}" y="1516" font-family="Inter" font-weight="600" font-size="26" letter-spacing="3" '
                 f'text-anchor="end" fill="{SAGE}">{SLOT_LABEL[e["slot"]]}</text>')
    # nama seri raksasa yang terpotong bingkai bawah: mengisi zona UI, tidak menyaingi teks
    parts.append(f'<text x="{L-8}" y="1908" font-family="Space Grotesk" font-weight="700" font-size="230" '
                 f'letter-spacing="-6" fill="none" stroke="{SAGE}" stroke-width="2" opacity="0.05">{esc(e["series"])}</text>')
    parts.append('</g>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
            f'viewBox="0 0 {W} {H}">' + "".join(parts) + "</svg>")


def build_thumbs():
    THUMBS.mkdir(parents=True, exist_ok=True)
    made = []
    for e in EPISODES:
        svg = thumb_svg(e)
        base = f"{e['ep']}_{slug(e['title'])}"
        sp = THUMBS / f"{base}.svg"
        pp = THUMBS / f"{base}.png"
        sp.write_text(svg)
        subprocess.run(["node", str(HERE / "render.mjs"),	str(sp), str(pp)], check=True,
                       cwd=HERE, stdout=subprocess.DEVNULL)
        made.append(pp)
    print(f"thumbnails: {len(made)} png + svg")
    return made


def contact_sheet(paths):
    """Grid 7x3 pratinjau, satu file untuk melihat semuanya sekaligus."""
    import base64
    cols, rows = 7, 3
    tw, th, gap, pad = 264, 469, 20, 56
    W = pad * 2 + cols * tw + (cols - 1) * gap
    H = pad * 2 + 90 + rows * th + (rows - 1) * gap
    parts = [f'<rect width="{W}" height="{H}" fill="{INK}"/>',
             f'<text x="{pad}" y="{pad+34}" font-family="Space Grotesk" font-weight="700" font-size="34" '
             f'letter-spacing="8" fill="{IVORY}">ODDCHAPTER · 21 THUMBNAIL</text>',
             f'<text x="{W-pad}" y="{pad+34}" font-family="Inter" font-weight="600" font-size="24" '
             f'letter-spacing="2" text-anchor="end" fill="{SAGE}">1080 × 1920 · 7 HARI × 3 SLOT</text>']
    order = sorted(paths, key=lambda p: (int(p.name[2:4])))
    for i, p in enumerate(order):
        c, r = i // rows, i % rows
        x = pad + c * (tw + gap)
        y = pad + 90 + r * (th + gap)
        b64 = base64.b64encode(p.read_bytes()).decode()
        parts.append(f'<image x="{x}" y="{y}" width="{tw}" height="{th}" href="data:image/png;base64,{b64}"/>')
        parts.append(f'<rect x="{x}" y="{y}" width="{tw}" height="{th}" fill="none" stroke="{SAGE}" '
                     f'stroke-width="1" opacity="0.35"/>')
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">' + "".join(parts) + "</svg>"
    sp = THUMBS / "CONTACT_SHEET.svg"
    sp.write_text(svg)
    subprocess.run(["node", str(HERE / "render.mjs"), str(sp), str(THUMBS / "CONTACT_SHEET.png")],
                   check=True, cwd=HERE, stdout=subprocess.DEVNULL)
    print("contact sheet:", W, "x", H)


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    if what in ("all", "scripts"):
        write_scripts()
        write_calendar()
    if what in ("all", "thumbs"):
        paths = build_thumbs()
        contact_sheet(paths)
