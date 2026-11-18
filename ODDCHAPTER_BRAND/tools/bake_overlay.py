"""
bake_overlay.py — pindahkan kerja piksel dari render ke berkas.

Chromium di sandbox ini jalan dengan rasterisasi software (swangle), jadi tiap
lapisan penuh layar yang dihitung ulang tiap frame (filter CSS grade footage,
dua gradient scrim, sapuan cahaya) menghabiskan hampir seluruh waktu render:
terukur 0,94 fps untuk 1920×1080.

Yang dikerjakan skrip ini:
  · grade Coverr (saturate 0.62 / contrast 1.12 / brightness 0.66) dibakar ke
    klip baru di public/footage_graded/ — tampilan sama, tanpa filter runtime
  · scrim dua gradient dibakar jadi public/overlay/scrim.png (satu Img statis)
  · sapuan cahaya dibakar jadi public/overlay/sweep.png (satu Img yang digeser)

    python3 tools/bake_overlay.py SB-EP02
"""
import json
import os
import pathlib
import subprocess
import sys

from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
REM = ROOT / "10_FILM" / "remotion"
PUB = REM / "public"
GEN = REM / "src" / "longform.generated.json"
FFMPEG = "ffmpeg"
W, H = 1920, 1080


def strip(stops, n=2048):
    """Strip 1×n RGBA: stops = [(pos, (r,g,b,a)), ...] dengan pos 0..1."""
    img = Image.new("RGBA", (n, 1))
    px = img.load()
    for i in range(n):
        t = i / (n - 1)
        rgba = stops[-1][1] if t >= stops[-1][0] else stops[0][1]
        for k in range(len(stops) - 1):
            p0, c0 = stops[k]
            p1, c1 = stops[k + 1]
            if p0 <= t <= p1:
                f = (t - p0) / max(1e-6, p1 - p0)
                rgba = tuple(int(round(c0[j] + (c1[j] - c0[j]) * f)) for j in range(4))
                break
        px[i, 0] = rgba
    return img


def main():
    ep = sys.argv[1] if len(sys.argv) > 1 else "SB-EP02"
    data = json.loads(GEN.read_text(encoding="utf-8"))
    clips = sorted({c["clip"].split("/", 1)[1] for s in data["segments"] for c in s.get("footage", [])})
    src_dir, out_dir = PUB / "footage", PUB / "footage_graded"
    out_dir.mkdir(parents=True, exist_ok=True)

    # Padanan filter CSS lama: saturate(0.62) contrast(1.12) brightness(0.66).
    # PENTING: brightness di ffmpeg eq BERSIFAT TAMBAH, bukan kali — filter CSS
    # brightness() mengalikan. Memakai eq=brightness=0.66 membuat seluruh klip
    # nyaris putih (master pertama harus dibuang karena ini). Perkalian dilakukan
    # colorlevels romax/gomax/bomax (romax = batas OUTPUT; rimax justru
    # menaikkan kontras dan membuat gambar makin putih).
    vf = ("eq=saturation=0.62:contrast=1.12,"
          "colorlevels=romax=0.66:gomax=0.66:bomax=0.66")
    force = os.environ.get("FORCE") == "1"
    for name in clips:
        src, dst = src_dir / name, out_dir / name
        if not force and dst.exists() and dst.stat().st_mtime >= src.stat().st_mtime:
            print("  ada :", name)
            continue
        r = subprocess.run([FFMPEG, "-hide_banner", "-loglevel", "error", "-y", "-i", str(src),
                            "-vf", vf, "-an", "-c:v", "libx264", "-crf", "18",
                            "-preset", "veryfast", "-pix_fmt", "yuv420p",
                            "-movflags", "+faststart", str(dst)], capture_output=True, text=True)
        print(("  ok  : " if r.returncode == 0 else "  GAGAL: ") + name + (r.stderr[-200:] if r.returncode else ""))

    # scrim = dua gradient yang dulu ditumpuk di komponen Scrim
    ov = PUB / "overlay"
    ov.mkdir(parents=True, exist_ok=True)
    v = strip([(0.00, (8, 10, 12, 209)), (0.18, (8, 10, 12, 56)), (0.40, (8, 10, 12, 0)),
               (0.68, (8, 10, 12, 107)), (1.00, (8, 10, 12, 240))]).resize((1, H), Image.NEAREST) \
        .resize((W, H), Image.BILINEAR)
    hgrad = strip([(0.00, (6, 8, 10, 219)), (0.38, (6, 8, 10, 115)),
                   (0.70, (6, 8, 10, 0)), (1.00, (6, 8, 10, 0))]).resize((W, 1), Image.NEAREST) \
        .resize((W, H), Image.BILINEAR)
    Image.alpha_composite(v, hgrad).save(ov / "scrim.png")
    print("scrim:", (ov / "scrim.png").stat().st_size // 1024, "KB")

    # sapuan cahaya: pita vertikal lembut, digeser komponen
    sw_w = 900
    sweep = Image.new("RGBA", (sw_w, H), (0, 0, 0, 0))
    px = sweep.load()
    for x in range(sw_w):
        t = x / (sw_w - 1)
        a = int(round(23 * max(0.0, 1 - abs(t - 0.5) * 2) ** 1.5))
        for y in range(0, H):
            px[x, y] = (255, 246, 226, a)
    sweep.save(ov / "sweep.png")
    print("sweep:", (ov / "sweep.png").stat().st_size // 1024, "KB")


if __name__ == "__main__":
    sys.exit(main())
