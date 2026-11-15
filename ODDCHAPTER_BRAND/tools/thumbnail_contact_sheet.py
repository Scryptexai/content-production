"""thumbnail_contact_sheet.py — satu lembar untuk meninjau 16 berkas sekaligus.

    python3 tools/thumbnail_contact_sheet.py
"""

import pathlib

from PIL import Image, ImageDraw, ImageFont

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
FINAL = ROOT / "11_CONTENT" / "03_THUMBNAIL" / "final"
FONTS = ROOT / "11_CONTENT" / "03_THUMBNAIL" / "assets" / "fonts"
EPS = [f"EP{i:02d}" for i in range(1, 9)]

INK = (23, 25, 29)
IVORY = (244, 240, 232)
SAGE = (167, 176, 161)
ORANGE = (242, 106, 61)

W = 2560
PAD = 30
GAP = 20


def main():
    big = ImageFont.truetype(str(FONTS / "ArchivoBlack-Regular.ttf"), 46)
    small = ImageFont.truetype(str(FONTS / "ArchivoBlack-Regular.ttf"), 24)

    tw = (W - PAD * 2 - GAP * 3) // 4
    th = round(tw * 9 / 16)
    sw = (W - PAD * 2 - GAP * 7) // 8
    sh = round(sw * 16 / 9)

    H = PAD + 70 + 34 + th * 2 + GAP + 70 + sh + PAD
    sheet = Image.new("RGB", (W, H), INK)
    d = ImageDraw.Draw(sheet)

    d.text((PAD, PAD), "16:9 — THUMBNAIL LONG", font=big, fill=IVORY)
    d.rectangle([PAD, PAD + 62, PAD + 220, PAD + 70], fill=ORANGE)

    y = PAD + 104
    for i, ep in enumerate(EPS):
        col, row = i % 4, i // 4
        x = PAD + col * (tw + GAP)
        yy = y + row * (th + GAP)
        sheet.paste(Image.open(FINAL / "16x9" / f"{ep}_16x9_1280x720.jpg").resize((tw, th), Image.LANCZOS), (x, yy))
        d.rectangle([x, yy, x + tw - 1, yy + th - 1], outline=(60, 62, 68))

    y2 = y + th * 2 + GAP + 60
    d.text((PAD, y2 - 56), "9:16 — COVER SHORT", font=big, fill=IVORY)
    d.rectangle([PAD, y2 - 2, PAD + 220, y2 + 6], fill=ORANGE)
    for i, ep in enumerate(EPS):
        x = PAD + i * (sw + GAP)
        sheet.paste(Image.open(FINAL / "9x16" / f"{ep}_9x16_1080x1920.jpg").resize((sw, sh), Image.LANCZOS), (x, y2 + 18))
        d.rectangle([x, y2 + 18, x + sw - 1, y2 + 18 + sh - 1], outline=(60, 62, 68))
        d.text((x + 4, y2 + 18 + sh + 8), ep, font=small, fill=SAGE)

    out = FINAL / "_KONTAK_SHEET.jpg"
    sheet.save(out, "JPEG", quality=90, optimize=True)
    print(f"{out.relative_to(ROOT)}  {sheet.size[0]}x{sheet.size[1]}  {out.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
