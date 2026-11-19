#!/usr/bin/env python3
"""Thumbnail 16:9 + poster 9:16 untuk Short seri angker (ffmpeg, tanpa AI)."""
import os, subprocess, sys
from pathlib import Path

FF = os.environ.get("FFMPEG") or __import__("imageio_ffmpeg").get_ffmpeg_exe()
ROOT = Path(__file__).resolve().parents[2]
CASE = ROOT / "work" / "sengkon"
IMG = CASE / "img"
FONTS = CASE / "fonts"
OUT = ROOT / "ODDCHAPTER_BRAND" / "11_CONTENT" / "06_UPLOAD" / "thumbs"
OUT.mkdir(parents=True, exist_ok=True)

ANTON = FONTS / "Anton-Regular.ttf"
BARLOW = FONTS / "BarlowCondensed-ExtraBold.ttf"
RED = "0xD82A2A"
IVORY = "0xF0ECE0"
GREY = "0xD0D0D0"

JOBS = [
    ("AK-EP01_thumbnail_16x9.jpg", 1280, 720, "A_kompas_halaman1.jpg", "left", [
        ("SALAH TANGKAP  ·  BEKASI 1974", BARLOW, 34, GREY, 64, 66),
        ("PEMBUNUHNYA", ANTON, 92, IVORY, 62, 128),
        ("SATU PENJARA", ANTON, 96, RED, 62, 228),
        ("12 TAHUN & 7 TAHUN", BARLOW, 48, IVORY, 64, 372),
        ("UNTUK PEMBUNUHAN YANG TAK", BARLOW, 32, GREY, 64, 434),
        ("MEREKA LAKUKAN", BARLOW, 32, GREY, 64, 472),
        ("ODDCHAPTER", BARLOW, 30, GREY, 64, 634),
    ]),
    ("AK-EP01_poster_9x16.jpg", 1080, 1920, "A_kompas_halaman1.jpg", "bottom", [
        ("SALAH TANGKAP  ·  BEKASI 1974", BARLOW, 40, GREY, 68, 1030),
        ("PEMBUNUHNYA", ANTON, 122, IVORY, 64, 1096),
        ("SATU PENJARA", ANTON, 134, RED, 64, 1224),
        ("12 TAHUN & 7 TAHUN", BARLOW, 60, IVORY, 68, 1400),
        ("UNTUK PEMBUNUHAN", BARLOW, 40, GREY, 68, 1478),
        ("YANG TAK MEREKA LAKUKAN", BARLOW, 40, GREY, 68, 1528),
        ("ODDCHAPTER", BARLOW, 34, GREY, 68, 1790),
    ]),
]


def build(name, w, h, src, side, items):
    if side == "left":
        pw, ph, ox, oy = int(w * 0.68), h, 0, 0
    else:
        pw, ph, ox, oy = w, int(h * 0.50), 0, int(h * 0.50)

    chain = [
        f"scale={w}:{h}:force_original_aspect_ratio=increase",
        f"crop={w}:{h}",
        "eq=saturation=0.22:contrast=1.18:brightness=-0.06:gamma=0.9",
        "colorbalance=bs=0.07:rs=-0.04",
        "vignette=angle=PI/4.4",
        "noise=alls=6:allf=t",
        "format=rgba",
    ]
    fc = "[0:v]" + ",".join(chain) + "[v];"
    fc += "[v][1:v]overlay=0:0:shortest=1[a];"
    fc += "[a][2:v]overlay=0:0:shortest=1[b];"

    extra = []
    if side == "left":
        extra.append(f"drawbox=x={pw-6}:y=0:w=6:h={h}:color={RED}@1:t=fill")
    else:
        extra.append(f"drawbox=x=0:y={oy}:w={w}:h=6:color={RED}@1:t=fill")
    for (text, font, size, color, x, y) in items:
        txt = text.replace(":", r"\:").replace("'", r"\'")
        extra.append(
            f"drawtext=fontfile={font}:text='{txt}':fontsize={size}:fontcolor={color}"
            f":x={x}:y={y}:shadowcolor=black@0.9:shadowx=3:shadowy=3"
        )
    fc += "[b]" + ",".join(extra) + ",format=yuv420p[out]"

    out = OUT / name
    cmd = [FF, "-y", "-loop", "1", "-i", str(IMG / src),
           "-f", "lavfi", "-i", f"color=c=black@0.86:s={pw}x{ph},format=rgba",
           "-f", "lavfi", "-i", f"color=c=black@0.86:s={pw}x{ph},format=rgba",
           "-filter_complex", fc, "-map", "[out]", "-frames:v", "1", "-q:v", "3", str(out)]
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        sys.stderr.write(p.stderr[-2500:])
        raise SystemExit(1)
    print(out.name, out.stat().st_size)


if __name__ == "__main__":
    for name, w, h, src, side, items in JOBS:
        build(name, w, h, src, side, items)
