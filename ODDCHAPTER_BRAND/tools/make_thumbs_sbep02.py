#!/usr/bin/env python3
"""Thumbnail SB-EP02: satu 16:9 untuk master + lima 9:16 untuk Shorts.

Frame diambil dari MASTER (bukan dari Short): di Short sudah ada hook yang
dibakar, jadi thumbnail akan memuat judul dua kali. Posisi frame dipilih di
dalam segmen yang memang berisi bahasan Short itu.

    python3 tools/make_thumbs_sbep02.py
"""
import json
import pathlib
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
REM = ROOT / "10_FILM" / "remotion"
MASTER = REM / "output" / "episodes" / "SB-EP02_MH370_1920x1080_master.mp4"
THUMBS = ROOT / "11_CONTENT" / "06_UPLOAD" / "thumbs"
FONTS = ROOT / ".build" / "fonts"
SG7 = FONTS / "space-grotesk-latin-700-normal.ttf"
IN6 = FONTS / "inter-latin-600-normal.ttf"
FFMPEG = "ffmpeg"

INK = (8, 10, 12)
IVORY = (240, 236, 224)
ORANGE = (198, 96, 42)
SAGE = (198, 206, 190)
SERIES = "MH370 · SATU BUSUR SATELIT"

# (id, detik di master, baris 1, baris 2, badge, klaim)
SHORTS = [
    ("S1", 8.0, "TERLACAK 7 KALI", "TETAP HILANG", "MH370 · 02:25–08:19",
     "Tujuh handshake Inmarsat tidak membawa posisi."),
    ("S2", 150.0, "SATU ANGKA DOPPLER", "UTARA GUGUR", "MH370 · BTO & BFO",
     "BFO membaca arah; busur ketujuh jadi dasar pencarian."),
    ("S3", 292.0, "PENCARIAN TERMAHAL", "DITEMUKAN TUKANG PANTAI", "MH370 · 3 SERPIHAN",
     "Tiga serpihan mengunci arah, bukan titik."),
    ("S4", 240.0, "28 HARI, 7.571 km²", "HASILNYA NOL", "MH370 · 2025–2026",
     "Fase 2025–26 ditutup 23 Januari 2026 tanpa bangkai."),
    ("S5", 345.0, "DATA SAMA", "DUA PEMBACAAN", "MH370 · KOTAK HITAM",
     "Pembedanya cuma kecepatan turun di menit terakhir."),
]


def frame(at):
    tmp = "/tmp/_thumb_src.png"
    subprocess.run([FFMPEG, "-hide_banner", "-loglevel", "error", "-y",
                    "-ss", str(at), "-i", str(MASTER), "-frames:v", "1", tmp], check=True)
    return Image.open(tmp).convert("RGB")


def grade(im):
    """Frame master sudah di-grade; di sini cuma digelapkan sedikit untuk teks."""
    dark = Image.new("RGB", im.size, INK)
    return Image.blend(im, dark, 0.22)


def wrap(draw, text, font, max_w, max_lines=3):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = f"{cur} {w}".strip()
        if draw.textlength(t, font=font) <= max_w:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines[:max_lines]



def fade_band(canvas, y0, y1, alpha_max=240, hold_to=None):
    """Gelapkan pita tempat caption bakar master berada (bawah 27% frame).

    Frame diambil dari master, jadi subtitle-nya ikut. Pita ini menutupnya
    sampai tak terbaca tanpa memotong gambar.
    """
    band = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(band)
    y1 = y1 if hold_to is None else hold_to
    for y in range(y0, min(y1, canvas.size[1])):
        t = (y - y0) / max(1, (y1 - y0))
        a = int(alpha_max * min(1.0, t * 2.2))
        d.line([(0, y), (canvas.size[0], y)], fill=(6, 8, 10, a))
    return Image.alpha_composite(canvas.convert("RGBA"), band).convert("RGB")


def vertical(at, l1, l2, badge, claim, out):
    fg = grade(frame(at))
    bg = fg.resize((1080, 1920), Image.LANCZOS).filter(ImageFilter.GaussianBlur(26))
    bg = Image.blend(bg, Image.new("RGB", (1080, 1920), INK), 0.35)
    canvas = bg.copy()
    canvas.paste(fg.resize((1080, 607), Image.LANCZOS), (0, 468))
    # caption master ada 162–290 px dari bawah frame → pita 890–1092
    canvas = fade_band(canvas, 796, 940, 250, hold_to=1092)
    d = ImageDraw.Draw(canvas, "RGBA")
    d.rectangle((0, 464, 1080, 467), fill=ORANGE + (220,))
    d.rectangle((0, 1075, 1080, 1078), fill=ORANGE + (110,))
    d.rectangle((0, 1092, 1080, 1920), fill=(6, 8, 10, 226))

    d.rectangle((64, 96, 78, 110), fill=ORANGE)
    d.text((96, 92), badge, font=ImageFont.truetype(str(IN6), 34), fill=ORANGE)

    size = 86 if max(len(l1), len(l2)) <= 20 else 70
    f = ImageFont.truetype(str(SG7), size)
    d.text((64, 150), l1, font=f, fill=IVORY)
    d.text((64, 150 + size + 14), l2, font=f, fill=IVORY)
    d.rectangle((64, 150 + (size + 14) * 2 + 24, 320, 150 + (size + 14) * 2 + 30), fill=ORANGE)

    fc = ImageFont.truetype(str(IN6), 40)
    d.rectangle((64, 1164, 264, 1168), fill=ORANGE)
    y = 1204
    for line in wrap(d, claim, fc, 952):
        d.text((64, y), line, font=fc, fill=IVORY)
        y += 56

    d.text((64, 1738), "ODDCHAPTER", font=ImageFont.truetype(str(SG7), 40), fill=IVORY)
    d.text((64, 1798), SERIES, font=ImageFont.truetype(str(IN6), 28), fill=SAGE)
    canvas.save(out, quality=88, optimize=True, progressive=True)
    print(out.name, f"{out.stat().st_size / 1024:.0f} KB", f"{canvas.size[0]}x{canvas.size[1]}")


def horizontal(at, l1, l2, badge, claim, out):
    fg = grade(frame(at))
    canvas = fg.resize((1280, 720), Image.LANCZOS)
    # scrim kiri supaya teks terbaca di atas footage apa pun
    scrim = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(scrim)
    for x in range(1280):
        a = int(214 * max(0.0, 1 - x / 980) ** 1.25)
        sd.line([(x, 0), (x, 720)], fill=(6, 8, 10, a))
    canvas = Image.alpha_composite(canvas.convert("RGBA"), scrim).convert("RGB")
    canvas = fade_band(canvas, 500, 640, 238)
    d = ImageDraw.Draw(canvas, "RGBA")

    d.rectangle((56, 54, 68, 66), fill=ORANGE)
    d.text((84, 50), badge, font=ImageFont.truetype(str(IN6), 24), fill=ORANGE)

    f = ImageFont.truetype(str(SG7), 78)
    d.text((54, 150), l1, font=f, fill=IVORY)
    d.text((54, 240), l2, font=f, fill=IVORY)
    d.rectangle((56, 352, 300, 358), fill=ORANGE)

    fc = ImageFont.truetype(str(IN6), 27)
    y = 386
    for line in wrap(d, claim, fc, 660, 2):
        d.text((56, y), line, font=fc, fill=SAGE)
        y += 38

    d.text((54, 638), "ODDCHAPTER", font=ImageFont.truetype(str(SG7), 26), fill=IVORY)
    d.text((240, 640), SERIES, font=ImageFont.truetype(str(IN6), 19), fill=SAGE)
    canvas.save(out, quality=90, optimize=True, progressive=True)
    print(out.name, f"{out.stat().st_size / 1024:.0f} KB", "1280x720")


def main():
    if not MASTER.exists():
        sys.exit(f"master belum ada: {MASTER}")
    THUMBS.mkdir(parents=True, exist_ok=True)
    rows = []
    for sid, at, l1, l2, badge, claim in SHORTS:
        out = THUMBS / f"SB-EP02_{sid}_thumbnail.jpg"
        vertical(at, l1, l2, badge, claim, out)
        rows.append({"id": sid, "thumb": out.name, "master_at": at, "hook": f"{l1} {l2}"})
    long_out = THUMBS / "SB-EP02_thumbnail.jpg"
    horizontal(12.0, "TERLACAK 7 KALI,", "TETAP HILANG", "MH370 · 8 MARET 2014",
               "Tujuh handshake setelah transponder mati. Dua belas tahun, nol bangkai.", long_out)
    (THUMBS / "thumbs_sb-ep02.json").write_text(
        json.dumps({"long": long_out.name, "shorts": rows}, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
