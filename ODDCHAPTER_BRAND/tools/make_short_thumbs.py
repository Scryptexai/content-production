#!/usr/bin/env python3
"""Thumbnail 1080x1920 untuk tiap Short: satu frame video + judul besar."""
import json
import pathlib
import subprocess

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT.parent / "work" / "shorts"
THUMBS = ROOT / "11_CONTENT" / "06_UPLOAD" / "thumbs"
FONTS = ROOT / ".build" / "fonts"
SG7 = FONTS / "space-grotesk-latin-700-normal.ttf"
IN6 = FONTS / "inter-latin-600-normal.ttf"
FFMPEG = "ffmpeg"

INK = (8, 10, 12)
IVORY = (240, 236, 224)
ORANGE = (198, 96, 42)
SAGE = (198, 206, 190)

MASTER = ROOT.parent / "google_drive" / "EP01_ILLUMINATI_1920x1080_master_v3.mp4"

# frame diambil dari MASTER, bukan dari Short — kalau dari Short, judul yang sudah
# dibakar di videonya akan muncul dua kali di thumbnail.
SHORTS = [
    ("S1", "EP01SB_S1.mp4", "TEORI ILLUMINATI", "LAHIR DARI BUKU", "1797", 140.0,
     "Dua buku terbit 1797. Teorinya menyebar lebih cepat daripada buktinya."),
    ("S2", "EP01SB_S2.mp4", "SIMBOLNYA DIPINJAM", "BUKAN DICIPTAKAN", "1776", 230.0,
     "Mata satu, piramida, segel dollar: lambang lama yang diberi makna baru."),
    ("S3", "EP01SB_S3.mp4", "DOKUMEN SAMA", "KESIMPULAN BERLAWANAN", "1785", 276.0,
     "Ketiadaan bukti bisa dibaca dua arah. Keduanya punya celah."),
]


def frame(path, at=3.0):
    tmp = "/tmp/_thumb_src.png"
    subprocess.run([FFMPEG, "-hide_banner", "-loglevel", "error", "-y",
                    "-ss", str(at), "-i", str(path), "-frames:v", "1", tmp], check=True)
    return Image.open(tmp).convert("RGB")


def compose(fg):
    """16:9 di tengah kanvas 9:16, latar versi blur (sama seperti Short)."""
    bg = fg.resize((1080, 1920), Image.LANCZOS).filter(ImageFilter.GaussianBlur(26))
    bg = Image.blend(bg, Image.new("RGB", (1080, 1920), INK), 0.35)
    canvas = bg.copy()
    clip = fg.resize((1080, 607), Image.LANCZOS)
    canvas.paste(clip, (0, 468))
    d = ImageDraw.Draw(canvas, "RGBA")
    d.rectangle((0, 464, 1080, 467), fill=ORANGE + (220,))
    d.rectangle((0, 1075, 1080, 1078), fill=ORANGE + (110,))
    d.rectangle((0, 1092, 1080, 1612), fill=(6, 8, 10, 205))
    return canvas


def wrap(draw, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= max_w:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def build(sid, video, l1, l2, badge, at, claim):
    im = compose(frame(MASTER, at))
    d = ImageDraw.Draw(im, "RGBA")
    f_badge = ImageFont.truetype(str(IN6), 34)
    f1 = ImageFont.truetype(str(SG7), 86)
    f2 = ImageFont.truetype(str(SG7), 86)

    d.rectangle((64, 96, 64 + 14, 96 + 14), fill=ORANGE)
    d.text((96, 92), badge, font=f_badge, fill=ORANGE)
    d.text((64, 150), l1, font=f1, fill=IVORY)
    d.text((64, 250), l2, font=f2, fill=IVORY)
    d.rectangle((64, 366, 320, 372), fill=ORANGE)

    f_claim = ImageFont.truetype(str(IN6), 40)
    d.rectangle((64, 1164, 260, 1168), fill=ORANGE)
    y = 1204
    for line in wrap(d, claim, f_claim, 952):
        d.text((64, y), line, font=f_claim, fill=IVORY)
        y += 56

    d.text((64, 1738), "ODDCHAPTER", font=ImageFont.truetype(str(SG7), 40), fill=IVORY)
    d.text((64, 1798), "ILLUMINATI · BUKTI ATAU TAFSIR?", font=ImageFont.truetype(str(IN6), 28), fill=SAGE)

    out = THUMBS / f"EP01SB_{sid}_thumb.jpg"
    im.save(out, quality=88, optimize=True, progressive=True)
    print(out.name, f"{out.stat().st_size/1024:.0f} KB")
    return out.name


def main():
    THUMBS.mkdir(parents=True, exist_ok=True)
    rows = []
    for sid, video, l1, l2, badge, at, claim in SHORTS:
        rows.append({"id": sid, "video": video, "thumb": build(sid, video, l1, l2, badge, at, claim)})
    (OUT / "thumbs.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
