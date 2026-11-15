"""thumbnail_render.py — pasang headline ke plate, hasilkan 2 rasio per episode.

Plate (gambar tanpa teks) dibuat oleh generate_image; skrip ini yang menaruh
tipografi, scrim, garis aksen, butir film, dan vignette — supaya delapan episode
punya sistem yang sama, bukan delapan selera.

Keluaran:
  16x9/EPxx_16x9_1280x720.jpg    untuk thumbnail video YouTube (long)
  9x16/EPxx_9x16_1080x1920.jpg   untuk cover Shorts/Reels

    python3 tools/thumbnail_render.py            # semua plate yang ada
"""

import pathlib
import random

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
PLATES = ROOT / "11_CONTENT" / "03_THUMBNAIL" / "plates"
OUT = ROOT / "11_CONTENT" / "03_THUMBNAIL" / "final"
FONTS = ROOT / "11_CONTENT" / "03_THUMBNAIL" / "assets" / "fonts"

INK = (23, 25, 29)
IVORY = (244, 240, 232)
SAGE = (167, 176, 161)
ORANGE = (242, 106, 61)

HEADLINE = {
    "EP01": ["PAKAIAN", "TERTINGGAL"],
    "EP02": ["DIPOTONG", "DARI DALAM"],
    "EP03": ["KAPAL", "KOSONG"],
    "EP04": ["JALAN", "KE ATAS"],
    "EP05": ["TANPA", "MAYAT"],
    "EP06": ["API TAK", "PADAM"],
    "EP07": ["JEJAK", "SATU ARAH"],
    "EP08": ["TANPA", "NAMA"],
    "EP09": ["TAS BERISI", "BATU"],
    "EP10": ["DUA KARDUS", "TANPA NAMA"],
}

SPEC = {
    "16x9": dict(w=1920, h=1080, out=(1280, 720), size=118, stroke=9,
                 margin=96, top=250, label=42, rule=(236, 9)),
    "9x16": dict(w=1080, h=1920, out=(1080, 1920), size=132, stroke=10,
                 margin=72, top=250, label=46, rule=(200, 10)),
}


def cover(img, w, h):
    """Isi kanvas tanpa distorsi (crop center)."""
    r = max(w / img.width, h / img.height)
    img = img.resize((round(img.width * r), round(img.height * r)), Image.LANCZOS)
    x = (img.width - w) // 2
    y = (img.height - h) // 2
    return img.crop((x, y, x + w, y + h))


def scrim(img, mode):
    """Gradien ink supaya teks selalu punya kontras 4.5:1."""
    w, h = img.size
    grad = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(grad)
    if mode == "16x9":
        for x in range(w):
            a = int(232 * max(0.0, 1 - x / (w * 0.62)) ** 1.35)
            d.line([(x, 0), (x, h)], fill=a)
        for y in range(h):
            a = int(120 * max(0.0, y / h - 0.62) / 0.38) if y > h * 0.62 else 0
            if a:
                d.line([(0, y), (w, y)], fill=max(a, grad.getpixel((0, y))))
    else:
        for y in range(h):
            a = int(238 * max(0.0, 1 - y / (h * 0.52)) ** 1.25)
            d.line([(0, y), (w, y)], fill=a)
        for y in range(int(h * 0.72), h):
            a = int(110 * (y - h * 0.72) / (h * 0.28))
            d.line([(0, y), (w, y)], fill=max(a, grad.getpixel((0, y))))
    grad = grad.filter(ImageFilter.GaussianBlur(24))
    layer = Image.new("RGB", (w, h), INK)
    return Image.composite(layer, img, grad)


def grain(img, strength=9):
    noise = Image.effect_noise(img.size, 26).convert("L")
    noise = noise.point(lambda v: 128 + (v - 128) * 0.7)
    return Image.blend(img, Image.merge("RGB", (noise, noise, noise)), strength / 100)


def vignette(img, power=0.55):
    w, h = img.size
    mask = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(mask)
    d.ellipse([-w * 0.25, -h * 0.35, w * 1.25, h * 1.35], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(min(w, h) * 0.18))
    dark = Image.new("RGB", (w, h), INK)
    return Image.composite(img, dark, mask.point(lambda v: 255 - int((255 - v) * power)))


def fit_font(text, size, stroke, max_w, font_path):
    while size > 40:
        f = ImageFont.truetype(str(font_path), size)
        if f.getlength(text) + stroke * 2 <= max_w:
            return f
        size -= 4
    return ImageFont.truetype(str(font_path), 40)


def draw_text(img, ep, mode):
    spec = SPEC[mode]
    w, h = img.size
    d = ImageDraw.Draw(img)
    margin, top = spec["margin"], int(spec["top"] * h / 1080)

    # label episode
    lab = ImageFont.truetype(str(FONTS / "ArchivoBlack-Regular.ttf"), spec["label"])
    d.text((margin, top - spec["label"] * 1.9), f"EP {ep[2:]}", font=lab, fill=SAGE + (255,))

    # garis aksen
    ry = top - spec["rule"][1] - 26
    d.rectangle([margin, ry, margin + spec["rule"][0], ry + spec["rule"][1]], fill=ORANGE)

    # headline
    y = top
    for line in HEADLINE[ep]:
        f = fit_font(line, spec["size"], spec["stroke"], w - margin * 2, FONTS / "Anton-Regular.ttf")
        d.text((margin, y), line, font=f, fill=IVORY, stroke_width=spec["stroke"], stroke_fill=INK)
        y += int(f.size * 0.94)
    return img


def brand(img, mode):
    w, h = img.size
    d = ImageDraw.Draw(img)
    f = ImageFont.truetype(str(FONTS / "ArchivoBlack-Regular.ttf"), 24 if mode == "16x9" else 30)
    y = h - (96 if mode == "16x9" else 150)
    d.text((SPEC[mode]["margin"], y), "ODDCHAPTER", font=f, fill=SAGE + (190,))
    return img


def render(ep, mode):
    plate = PLATES / (f"{ep}_{'plate' if mode == '16x9' else '9x16'}.png")
    if not plate.exists():
        return None
    spec = SPEC[mode]
    img = cover(Image.open(plate).convert("RGB"), spec["w"], spec["h"])
    img = scrim(img, mode)
    img = draw_text(img, ep, mode)
    img = brand(img, mode)
    img = grain(img)
    img = vignette(img)
    img = img.resize(spec["out"], Image.LANCZOS)

    folder = OUT / ("16x9" if mode == "16x9" else "9x16")
    folder.mkdir(parents=True, exist_ok=True)
    w, h = spec["out"]
    path = folder / f"{ep}_{mode.replace('x', 'x')}_{w}x{h}.jpg"
    img.save(path, "JPEG", quality=93, subsampling=1, optimize=True)
    return path


def main():
    n = 0
    for ep in HEADLINE:
        for mode in ("16x9", "9x16"):
            p = render(ep, mode)
            if p:
                n += 1
                print(f"  {p.relative_to(ROOT)}  {p.stat().st_size // 1024} KB")
    print(f"\n{n} berkas")


if __name__ == "__main__":
    main()
