#!/usr/bin/env python3
"""Build the two source-safe JPEG thumbnails required by the authorized uploads.

These are original information-design thumbnails: no stock photo, victim imagery,
or documentary-looking reconstruction.  They deliberately repeat the factual
boundaries that appear in the corresponding masters.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "11_CONTENT" / "06_UPLOAD" / "thumbs"
FONTS = ROOT / "10_FILM" / "remotion" / "public" / "fonts"
W, H = 1280, 720
INK = "#080A0C"
IVORY = "#EFE9DB"
SAGE = "#BBC7BA"
ORANGE = "#E46E3B"


def font(name: str, size: int):
    return ImageFont.truetype(str(FONTS / name), size)


BOLD = "space-grotesk-latin-700-normal.ttf"
MEDIUM = "inter-latin-600-normal.ttf"
REGULAR = "inter-latin-500-normal.ttf"


def base():
    im = Image.new("RGB", (W, H), INK)
    d = ImageDraw.Draw(im, "RGBA")
    # Restrained technical grid shared by the masters.
    for y in range(54, H, 68):
        d.line((0, y, W, y), fill=(187, 199, 186, 20), width=1)
    for x in range(64, W, 96):
        d.line((x, 0, x, H), fill=(187, 199, 186, 12), width=1)
    for r in range(520, 20, -18):
        a = int(0.25 * (1 - r / 540) * 255)
        d.ellipse((950 - r, 270 - r * 0.52, 950 + r, 270 + r * 0.52), fill=(228, 110, 59, a))
    return im, d


def label(d, text, xy):
    d.text(xy, text, font=font(MEDIUM, 20), fill=ORANGE, spacing=0)


def wordmark(d):
    d.text((1004, 52), "ODDCHAPTER", font=font(BOLD, 22), fill=IVORY)


def save(im, name):
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / name
    im.save(path, "JPEG", quality=92, optimize=True, progressive=True)
    assert path.stat().st_size < 2 * 1024 * 1024, f"thumbnail too large: {path}"
    print(f"{path.relative_to(ROOT)} · {path.stat().st_size} bytes")


def tambora():
    im, d = base()
    wordmark(d)
    label(d, "KASUS NYATA · SUMBAWA", (78, 80))
    d.text((76, 124), "TAMBORA 1815", font=font(BOLD, 91), fill=IVORY)
    d.text((80, 230), "LIMA LAPISAN ABU", font=font(BOLD, 43), fill=ORANGE)
    d.text((80, 286), "Doro Bente · stratigrafi 1815", font=font(REGULAR, 28), fill=SAGE)

    # The right-hand diagram is an original strata/caldera cue, not a map or a
    # reconstruction of people or the event.
    cx, cy = 940, 352
    d.ellipse((cx - 152, cy - 102, cx + 152, cy + 102), outline=(239, 233, 219, 210), width=8)
    d.ellipse((cx - 92, cy - 46, cx + 92, cy + 46), outline=(228, 110, 59, 235), width=10)
    for idx, color in enumerate(((91, 119, 135, 255), (105, 128, 141, 255), (117, 133, 144, 255),
                                  (156, 118, 87, 255), (180, 107, 62, 255), (209, 125, 70, 255),
                                  (228, 110, 59, 255), (239, 145, 83, 255))):
        y = 482 + idx * 20
        d.rounded_rectangle((664, y, 1192, y + 14), radius=7, fill=color)
    d.text((666, 654), "3 LAPISAN LEBIH TUA  ·  5 LAPISAN PIROKLASTIK", font=font(MEDIUM, 16), fill=SAGE)
    d.line((76, 654, 570, 654), fill=(228, 110, 59, 220), width=4)
    d.text((76, 674), "BRIN 2024 · GVP · SCHURER ET AL. 2019", font=font(MEDIUM, 15), fill=SAGE)
    save(im, "LF04_Tambora-1815_thumbnail_16x9.jpg")


def sinar_bangun():
    im, d = base()
    wordmark(d)
    label(d, "DANAU TOBA · DATA POSKO", (78, 80))
    d.text((74, 144), "188", font=font(BOLD, 235), fill=ORANGE)
    d.text((78, 372), "BUKAN MANIFEST", font=font(BOLD, 56), fill=IVORY)
    d.text((82, 444), "VERIFIKASI HARI KE-9 · KNKT", font=font(MEDIUM, 25), fill=SAGE)

    # Abstract route and boat icon: it represents the data question and makes no
    # claim to depict the incident, passengers, or victims.
    d.line((690, 444, 1144, 444), fill=(228, 110, 59, 190), width=4)
    for x, y, r in ((720, 378, 14), (813, 332, 10), (914, 365, 18), (1022, 290, 9), (1120, 338, 13)):
        d.ellipse((x-r, y-r, x+r, y+r), fill=(187, 199, 186, 160))
    d.polygon(((805, 530), (1090, 530), (1036, 584), (850, 584)), outline=IVORY, fill=(18, 25, 29, 255), width=5)
    d.line((942, 404, 942, 530), fill=ORANGE, width=6)
    d.polygon(((948, 418), (1046, 492), (948, 492)), fill=(228, 110, 59, 220))
    for i in range(4):
        y = 608 + i * 17
        d.arc((720, y, 1130, y + 26), 195, 345, fill=(187, 199, 186, 130), width=3)
    d.line((78, 654, 570, 654), fill=(228, 110, 59, 220), width=4)
    d.text((78, 674), "21 SELAMAT · 3 MENINGGAL · 164 HILANG", font=font(MEDIUM, 15), fill=SAGE)
    save(im, "AK-EP12_Sinar-Bangun_thumbnail_16x9.jpg")


if __name__ == "__main__":
    tambora()
    sinar_bangun()
