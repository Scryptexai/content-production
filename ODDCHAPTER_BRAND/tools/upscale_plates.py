#!/usr/bin/env python3
"""
upscale_plates.py — naikkan plate ke 1920×1080 (16:9) dengan upscale + grain.

Model gambar mengembalikan 1376×768. Untuk video 1080p, plate harus 1920×1080.
Upscale Lanczos saja terlihat lunak; grain halus menyembunyikan kelunakan itu dan
sekaligus menyatukan plate yang dibuat di sesi berbeda.

    python3 tools/upscale_plates.py 11_CONTENT/07_LONGFORM/LF01_sultana/plates
    python3 tools/upscale_plates.py <folder> --width 1920 --height 1080 --grain 0.055

Asli disimpan di `plates_src/` (masuk .gitignore) supaya tidak pernah hilang:
grain tidak bisa dibatalkan.
"""
import argparse
import pathlib
import shutil
import sys

from PIL import Image, ImageFilter


def cover(img, width, height):
    """Isi seluruh kanvas lalu potong tengah — tanpa distorsi rasio."""
    scale = max(width / img.width, height / img.height)
    size = (round(img.width * scale), round(img.height * scale))
    resized = img.resize(size, Image.LANCZOS)
    left = (resized.width - width) // 2
    top = (resized.height - height) // 2
    return resized.crop((left, top, left + width, top + height))


def grain(img, amount):
    if amount <= 0:
        return img
    noise = Image.effect_noise(img.size, 26).convert("L")
    noise_rgb = Image.merge("RGB", (noise, noise, noise))
    return Image.blend(img, noise_rgb, amount)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("folder")
    ap.add_argument("--width", type=int, default=1920)
    ap.add_argument("--height", type=int, default=1080)
    ap.add_argument("--grain", type=float, default=0.055)
    ap.add_argument("--quality", type=int, default=92)
    args = ap.parse_args()

    folder = pathlib.Path(args.folder)
    if not folder.is_dir():
        sys.exit(f"folder tidak ada: {folder}")
    src_dir = folder.parent / "plates_src"
    src_dir.mkdir(exist_ok=True)

    plates = sorted(p for p in folder.glob("*.jpg"))
    if not plates:
        sys.exit(f"tidak ada .jpg di {folder}")

    for path in plates:
        backup = src_dir / path.name
        if not backup.exists():
            shutil.copy2(path, backup)
        source = backup if backup.stat().st_size <= path.stat().st_size else path
        with Image.open(source) as img:
            img = img.convert("RGB")
            before = img.size
            out = cover(img, args.width, args.height)
            out = grain(out, args.grain)
            out = out.filter(ImageFilter.UnsharpMask(radius=2, percent=55, threshold=3))
            out.save(path, "JPEG", quality=args.quality, optimize=True, progressive=True)
        print(f"{path.name:34s} {before[0]}×{before[1]} → {args.width}×{args.height}  "
              f"{path.stat().st_size / 1024:.0f} KB")

    print(f"\n{len(plates)} plate · asli di {src_dir.relative_to(folder.parent.parent.parent)}")


if __name__ == "__main__":
    main()
