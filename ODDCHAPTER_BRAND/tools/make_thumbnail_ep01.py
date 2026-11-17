#!/usr/bin/env python3
"""Buat thumbnail 1280x720 untuk YouTube (16:9) dari plate kampanye EP01.

Dua varian:
  A — arsip: potret Weishaupt di kartu miring, judul besar di kiri.
  B — simbol: kolase mata-segitiga penuh, judul menimpa, pita tahun di bawah.

Keduanya pakai palet brand (ink/ivory/sage + oranye) dan font brand, supaya
thumbnail tidak terlihat dari kanal lain.
"""
import pathlib
import sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
ASSETS = ROOT / "10_FILM" / "assets" / "SB-EP01"
PORTRAIT = ROOT.parent / "image-search" / "adam-weishaupt-portrait-engraving-founde-1.jpg"
BG_EYE = ROOT / "11_CONTENT" / "06_UPLOAD" / "thumbs" / "_bg_eye.jpg"
FONTS = ROOT / ".build" / "fonts"
OUT = ROOT / "11_CONTENT" / "06_UPLOAD" / "thumbs"

INK = (8, 10, 12)
IVORY = (240, 236, 224)
SAGE = (198, 208, 190)
ORANGE = (198, 96, 42)
W, H = 1280, 720


def f(name, size):
    return ImageFont.truetype(str(FONTS / name), size)


SG7 = lambda s: f("space-grotesk-latin-700-normal.ttf", s)  # noqa: E731
SG5 = lambda s: f("space-grotesk-latin-500-normal.ttf", s)  # noqa: E731
IN6 = lambda s: f("inter-latin-600-normal.ttf", s)  # noqa: E731
IN5 = lambda s: f("inter-latin-500-normal.ttf", s)  # noqa: E731


def cover(path, w, h, focus_y=0.42):
    im = Image.open(path).convert("RGB")
    sc = max(w / im.width, h / im.height)
    im = im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.LANCZOS)
    x = (im.width - w) // 2
    y = int((im.height - h) * focus_y)
    return im.crop((x, y, x + w, y + h))


def vignette(canvas, strength=0.85):
    w, h = canvas.size
    mask = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(mask)
    d.ellipse((-w * 0.25, -h * 0.35, w * 1.25, h * 1.35), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(140))
    dark = Image.new("RGB", (w, h), INK)
    return Image.composite(canvas, Image.blend(canvas, dark, strength), mask)


def grain(canvas, amount=9):
    import random
    random.seed(7)
    d = ImageDraw.Draw(canvas, "RGBA")
    for _ in range(14000):
        x, y = random.randrange(W), random.randrange(H)
        a = random.randint(6, amount)
        d.point((x, y), fill=(255, 248, 232, a))
    return canvas


def tracked(draw, xy, text, font, fill, track=6):
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += draw.textlength(ch, font=font) + track
    return x


def wrap(draw, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if draw.textlength(t, font=font) <= max_w:
            cur = t
        else:
            lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def eye_triangle(draw, cx, cy, r, color, width=4, alpha=255):
    """Ikon mata-segitiga garis, dipakai sebagai latar tipis / aksen."""
    c = color + (alpha,)
    draw.line([(cx, cy - r), (cx + r * 0.95, cy + r * 0.72), (cx - r * 0.95, cy + r * 0.72), (cx, cy - r)],
              fill=c, width=width, joint="curve")
    ey = cy + r * 0.28
    draw.ellipse((cx - r * 0.34, ey - r * 0.2, cx + r * 0.34, ey + r * 0.2), outline=c, width=width)
    draw.ellipse((cx - r * 0.08, ey - r * 0.08, cx + r * 0.08, ey + r * 0.08), fill=c)


def glow_engraving(path, w, h, tint=(238, 232, 218), bg=(10, 12, 14), gamma=1.0):
    """Engraving putih-hitam diubah jadi garis terang di atas latar gelap.

    Foto arsip asli berlatar putih; di thumbnail gelap, putih itu jadi kotak yang
    memantul. Inversi + tint ivory membuatnya terbaca seperti ukiran menyala.
    """
    im = Image.open(path).convert("L")
    sc = max(w / im.width, h / im.height)
    im = im.resize((int(im.width * sc) + 1, int(im.height * sc) + 1), Image.LANCZOS)
    x, y = (im.width - w) // 2, int((im.height - h) * 0.35)
    im = im.crop((x, y, x + w, y + h))
    inv = Image.eval(im, lambda v: 255 - v)
    if gamma != 1.0:
        inv = inv.point(lambda v: int(255 * (v / 255) ** gamma))
    return Image.composite(Image.new("RGB", (w, h), tint), Image.new("RGB", (w, h), bg), inv)


def base_canvas():
    canvas = Image.new("RGB", (W, H), INK)
    glow = Image.new("RGB", (W, H), INK)
    gd = ImageDraw.Draw(glow)
    gd.ellipse((W * 0.42, -H * 0.3, W * 1.25, H * 1.1), fill=(46, 26, 16))
    glow = glow.filter(ImageFilter.GaussianBlur(190))
    canvas = Image.blend(canvas, glow, 0.55)
    return canvas


def variant_a():
    canvas = base_canvas()
    # kartu arsip di kanan
    card_w, card_h = 424, 532
    photo = glow_engraving(PORTRAIT, card_w - 16, card_h - 108, gamma=0.85)
    card = Image.new("RGB", (card_w, card_h), (18, 20, 24))
    card.paste(photo, (8, 8))
    cd = ImageDraw.Draw(card)
    cd.rectangle((0, 0, card_w - 1, card_h - 1), outline=(78, 84, 92), width=2)
    cd.rectangle((8, card_h - 96, card_w - 8, card_h - 8), fill=(12, 14, 17))
    cd.text((26, card_h - 84), "ADAM WEISHAUPT", font=IN6(26), fill=IVORY)
    cd.text((26, card_h - 50), "profesor hukum · 1776", font=IN5(20), fill=SAGE)
    cd.ellipse((20, 18, 36, 34), fill=ORANGE)
    card = card.rotate(-3.2, expand=True, resample=Image.BICUBIC)

    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rectangle((796, 96, 1266, 678), fill=(0, 0, 0, 190))
    shadow = shadow.filter(ImageFilter.GaussianBlur(38))
    canvas = Image.alpha_composite(canvas.convert("RGBA"), shadow).convert("RGB")

    # ikon mata-segitiga samar di belakang kartu
    icon = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    eye_triangle(ImageDraw.Draw(icon), 1000, 250, 150, ORANGE, width=5, alpha=60)
    canvas = Image.alpha_composite(canvas.convert("RGBA"), icon).convert("RGB")
    canvas.paste(card, (838, 78))

    d = ImageDraw.Draw(canvas, "RGBA")
    tracked(d, (66, 96), "BUKTI ATAU TAFSIR?", IN6(23), ORANGE, track=5)
    d.text((66, 146), "ILLUMINATI", font=SG7(124), fill=IVORY)
    d.text((66, 268), "PERNAH", font=SG7(124), fill=IVORY)
    d.text((66, 390), "ADA?", font=SG7(136), fill=ORANGE)
    d.rectangle((70, 574, 452, 580), fill=ORANGE)
    d.text((70, 594), "1785 dibubarkan  ·  1797 teorinya lahir", font=IN5(24), fill=SAGE)
    d.text((70, 628), "satu pertanyaan, dua jawaban", font=IN5(22), fill=(150, 158, 152))
    d.text((70, 672), "ODDCHAPTER", font=SG7(24), fill=(214, 220, 208))
    canvas = vignette(canvas, 0.45)
    return grain(canvas)


def variant_b():
    canvas = Image.new("RGB", (W, H), INK)
    bg = cover(BG_EYE, W, H, 0.45)
    bg = Image.blend(bg, Image.new("RGB", (W, H), INK), 0.30)
    canvas.paste(bg, (0, 0))

    shade = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shade)
    for i in range(H):
        a = int(60 + 200 * max(0.0, (i - H * 0.35) / (H * 0.65)) ** 1.4)
        sd.line([(0, i), (W, i)], fill=(6, 8, 10, min(238, a)))
    canvas = Image.alpha_composite(canvas.convert("RGBA"), shade).convert("RGB")


    d = ImageDraw.Draw(canvas, "RGBA")
    tracked(d, (64, 96), "1776 · 1785 · 1797", IN6(24), ORANGE, track=6)
    d.text((64, 148), "MEREKA", font=SG7(126), fill=IVORY)
    d.text((64, 288), "BENAR-BENAR", font=SG7(126), fill=IVORY)
    d.text((64, 428), "ADA.", font=SG7(126), fill=ORANGE)
    band = Image.new("RGBA", (W, 92), (8, 10, 12, 216))
    canvas = Image.alpha_composite(canvas.convert("RGBA"), _band(band)).convert("RGB")
    d = ImageDraw.Draw(canvas, "RGBA")
    d.rectangle((0, H - 92, W, H - 88), fill=ORANGE)
    d.text((64, H - 70), "lalu kenapa buktinya berhenti di 1785?", font=IN6(30), fill=IVORY)
    d.text((1096, H - 70), "ODDCHAPTER", font=SG7(26), fill=SAGE)
    canvas = vignette(canvas, 0.35)
    return grain(canvas)


def _band(band):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    layer.paste(band, (0, H - 92))
    return layer


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    a = variant_a()
    b = variant_b()
    targets = [
        ("EP01SB_thumbnail.jpg", b),      # utama: kolase arsip + hook
        ("EP01SB_thumbnail_alt.jpg", a),  # alternatif: potret Weishaupt
    ]
    for name, im in targets:
        im = im.convert("RGB")
        im.save(OUT / name, quality=90, optimize=True, progressive=True)
        print(f"{name}  {im.width}x{im.height}  {(OUT / name).stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    main()
