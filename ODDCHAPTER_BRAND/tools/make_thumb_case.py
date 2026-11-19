#!/usr/bin/env python3
"""Thumbnail 16:9 + poster 9:16 generik per kasus (ffmpeg, tanpa AI).

Pemakaian: python3 make_thumb_case.py <slug>   (JOBS dari work/<slug>/thumb_cfg.py)
"""
import os, subprocess, sys
from pathlib import Path

FF = os.environ.get("FFMPEG") or __import__("imageio_ffmpeg").get_ffmpeg_exe()
ROOT = Path(__file__).resolve().parents[2]
SLUG = sys.argv[1]
import importlib.util
CASE = ROOT / "work" / SLUG
_spec = importlib.util.spec_from_file_location(f"thumb_{SLUG}", CASE / "thumb_cfg.py")
_cfg = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_cfg)
IMG = CASE / "img"
FONTS = CASE / "fonts"
OUT = ROOT / "ODDCHAPTER_BRAND" / "11_CONTENT" / "06_UPLOAD" / "thumbs"
OUT.mkdir(parents=True, exist_ok=True)

ANTON = FONTS / "Anton-Regular.ttf"
BARLOW = FONTS / "BarlowCondensed-ExtraBold.ttf"
RED = "0xD82A2A"
IVORY = "0xF0ECE0"
GREY = "0xD0D0D0"

JOBS = _cfg.JOBS


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
    pos = "0:0" if side == "left" else f"0:{oy}"
    fc += f"[v][1:v]overlay={pos}:shortest=1[a];"
    fc += f"[a][2:v]overlay={pos}:shortest=1[b];"

    extra = []
    if side == "left":
        extra.append(f"drawbox=x={pw-6}:y=0:w=6:h={h}:color={RED}@1:t=fill")
    else:
        extra.append(f"drawbox=x=0:y={oy}:w={w}:h=6:color={RED}@1:t=fill")
    fonts = {"ANTON": ANTON, "BARLOW": BARLOW}
    colors = {"RED": RED, "IVORY": IVORY, "GREY": GREY}
    for (text, font, size, color, x, y) in items:
        font = fonts.get(font, font)
        color = colors.get(color, color)
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
