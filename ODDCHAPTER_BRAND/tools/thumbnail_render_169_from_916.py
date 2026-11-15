"""thumbnail_render_169_from_916.py — cadangan sementara.

Plate 16:9 EP07 & EP08 belum ada (kena batas 10 gambar/turn). Skrip ini
memotong sabuk 16:9 dari plate 9:16 memakai renderer yang sama, supaya dua
episode itu tetap punya pasangan long. Ganti begitu plate 16:9 asli tersedia.
"""

import sys

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))

import pathlib

from PIL import Image

from PIL import ImageOps

import thumbnail_render as tr

# titik atas jendela 16:9 pada plate 1376 px + perlu cermin? (subjek ke kanan)
CROP = {"EP07": (640, True), "EP08": (800, False)}


def main():
    for ep, (top, mirror) in CROP.items():
        src = Image.open(tr.PLATES / f"{ep}_9x16.png").convert("RGB")
        h = int(src.width * 9 / 16)
        box = (0, top, src.width, min(top + h, src.height))
        if box[3] - box[1] < h:
            box = (0, src.height - h, src.width, src.height)
        band = src.crop(box).resize((tr.SPEC["16x9"]["w"], tr.SPEC["16x9"]["h"]), Image.LANCZOS)
        if mirror:
            band = ImageOps.mirror(band)
        img = tr.scrim(band, "16x9")
        img = tr.draw_text(img, ep, "16x9")
        img = tr.brand(img, "16x9")
        img = tr.grain(img)
        img = tr.vignette(img)
        img = img.resize(tr.SPEC["16x9"]["out"], Image.LANCZOS)
        out = tr.OUT / "16x9" / f"{ep}_16x9_1280x720.jpg"
        img.save(out, "JPEG", quality=93, subsampling=1, optimize=True)
        print(f"  {out.relative_to(tr.ROOT)}  {out.stat().st_size // 1024} KB  (crop dari 9x16)")


if __name__ == "__main__":
    main()
