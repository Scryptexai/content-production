#!/usr/bin/env python3
"""
Build video vertikal 9:16 untuk Skrip 01 "Shade Paling Gelap" (Alya).

Yang dilakukan:
  1. Render 12 segmen dari 7 still (gerakan kamera Ken Burns via zoompan)
  2. Gabung dengan hard cut (gaya jump-cut TikTok, sesuai naskah)
  3. Vignette + grain halus
  4. Overlay kartu teks (dibuat dengan Pillow, bukan drawtext)
  5. Mux audio + loudnorm -16 LUFS

Jalankan:  python3 playbook/build_video.py
Output:    video/alya-01-shade-paling-gelap.mp4
"""
import os
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FF = open(os.path.join(ROOT, ".ffmpeg-path")).read().strip()

W, H = 1080, 1920
FPS = 30
AUDIO = os.path.join(ROOT, "audio/alya-01-shade-paling-gelap.mp3")
DURATION = 71.3

SCENE = os.path.join(ROOT, "assets/scene")
BUILD = os.path.join(ROOT, "build")
CARDS = os.path.join(BUILD, "cards")
OUTDIR = os.path.join(ROOT, "video")
for d in (BUILD, CARDS, OUTDIR):
    os.makedirs(d, exist_ok=True)

SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"

PAPER = (239, 231, 218, 255)
GOLD = (255, 233, 168, 255)
ACCENT = (201, 139, 139, 255)

# ---------------------------------------------------------------- timeline
# (mulai, selesai, gambar, zoom_mulai, zoom_akhir, drift_y)
SEGMENTS = [
    (0.0, 4.2, "alya-shot-01-hook.jpg", 1.02, 1.10, -14),
    (4.2, 8.7, "alya-shot-05-turn.jpg", 1.13, 1.03, 8),
    (8.7, 14.0, "alya-shot-02-story.jpg", 1.02, 1.09, -10),
    (14.0, 20.1, "alya-shot-02-story.jpg", 1.16, 1.06, 12),
    (20.1, 26.6, "alya-shot-03-reveal.jpg", 1.03, 1.11, -8),
    (26.6, 33.0, "alya-shot-04-tension.jpg", 1.04, 1.12, -6),
    (33.0, 39.5, "alya-shot-04-tension.jpg", 1.17, 1.07, 10),
    (39.5, 45.5, "alya-shot-05-turn.jpg", 1.02, 1.09, -6),
    (45.5, 54.0, "alya-shot-06-value.jpg", 1.03, 1.10, -8),
    (54.0, 62.7, "alya-shot-06-value.jpg", 1.16, 1.06, 10),
    (62.7, 67.0, "alya-shot-07-cta.jpg", 1.02, 1.08, -6),
    (67.0, 71.3, "alya-shot-07-cta.jpg", 1.13, 1.04, 8),
]

# (mulai, selesai, teks) — maks 12 kata per kartu
LINES = [
    (0.0, 4.2, "Enam tahun aku jualan foundation."),
    (4.2, 8.7, "Dan selama itu, aku nggak pernah pakai shade yang cocok buat kulitku sendiri."),
    (8.7, 14.0, "Aku masih ingat. Ada mbak-mbak datang ke konter, kulitnya sawo matang."),
    (14.0, 20.1, "Dia minta shade paling gelap. Aku bilang: \u201cKak, ini udah paling gelap.\u201d"),
    (20.1, 26.6, "Padahal di rak belakang, masih ada satu shade lagi."),
    (26.6, 33.0, "Kenapa? Karena shade gelap dianggap nggak laku."),
    (33.0, 39.5, "Jadi kamu disuruh pakai yang lebih terang, biar katanya kelihatan cerah."),
    (39.5, 45.5, "Itu bukan kulit kamu yang salah. Itu stoknya yang nggak pernah dibuat untuk kamu."),
    (45.5, 52.0, "Satu: tes di rahang, bukan di tangan."),
    (52.0, 58.0, "Dua: tunggu dua puluh menit. Foundation berubah setelah kena minyak kulit."),
    (58.0, 62.7, "Tiga: cek di cahaya matahari, bukan di lampu konter."),
    (62.7, 67.0, "Kamu pernah nggak dibilang \u201cini udah paling gelap, Kak\u201d?"),
    (67.0, 71.3, "Tulis di komentar. Aku pengen tahu, ada berapa banyak dari kita."),
]


def run(cmd, desc=""):
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        print(f"[ffmpeg gagal] {desc}\n{cmd}\n{p.stderr[-3000:]}")
        sys.exit(1)


# ---------------------------------------------------------------- 1. segmen
print("1/5  render segmen …")
seg_files = []
for i, (s, e, img, z0, z1, dy) in enumerate(SEGMENTS):
    dur = e - s
    frames = max(2, int(dur * FPS))
    # zoompan: zoom bergerak linear dari z0 ke z1, sedikit drift vertikal
    expr = f"{z0}+({z1}-{z0})*on/{frames}"
    drift = f"ih/2-(ih/zoom/2)+{dy}*on/{frames}"
    vf = (
        "scale=1620:2880:force_original_aspect_ratio=increase,"
        "crop=1620:2880,"
        f"zoompan=z='{expr}':x='iw/2-(iw/zoom/2)':y='{drift}':d=1:s={W}x{H}:fps={FPS},"
        "format=yuv420p"
    )
    out = os.path.join(BUILD, f"seg{i:02d}.mp4")
    run([
        FF, "-y", "-loglevel", "error",
        "-loop", "1", "-framerate", str(FPS), "-i", os.path.join(SCENE, img),
        "-t", f"{dur:.3f}", "-vf", vf,
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-r", str(FPS),
        out,
    ], f"segmen {i}")
    seg_files.append(out)

# ---------------------------------------------------------------- 2. concat
print("2/5  gabung …")
lst = os.path.join(BUILD, "list.txt")
with open(lst, "w") as f:
    for p in seg_files:
        f.write(f"file '{p}'\n")
joined = os.path.join(BUILD, "joined.mp4")
run([FF, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst,
     "-c", "copy", joined], "concat")

# ---------------------------------------------------------------- 3. look
print("3/5  vignette + grain …")
graded = os.path.join(BUILD, "graded.mp4")
run([
    FF, "-y", "-loglevel", "error", "-i", joined,
    "-vf", "vignette=PI/4.6,noise=alls=5:allf=t+u,eq=contrast=1.03:saturation=1.02,format=yuv420p",
    "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-r", str(FPS),
    graded,
], "grade")


# ---------------------------------------------------------------- 4. kartu
def wrap(draw, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=font) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def line_card(idx, text):
    """Kartu subtitle transparan 1080x1920."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype(SANS_B, 54)
    max_w = W - 150
    rows = wrap(d, text, font, max_w)

    # kalau kepanjangan, kecilkan font
    size = 54
    while len(rows) > 3 and size > 40:
        size -= 3
        font = ImageFont.truetype(SANS_B, size)
        rows = wrap(d, text, font, max_w)

    line_h = int(size * 1.34)
    block_h = line_h * len(rows)
    y0 = int(H * 0.695) - block_h // 2
    for r, row in enumerate(rows):
        y = y0 + r * line_h
        # deteksi kutipan -> warna emas
        for seg_text, color in split_quotes(row, font, d):
            x = (W - d.textlength(row, font=font)) / 2
            for sub, col in seg_text:
                d.text((x, y), sub, font=font, fill=col,
                       stroke_width=7, stroke_fill=(0, 0, 0, 235))
                x += d.textlength(sub, font=font)
    img.save(os.path.join(CARDS, f"sub{idx:02d}.png"))


def split_quotes(row, font, d):
    """Pecah baris jadi run berwarna: dalam tanda kutip = emas."""
    runs, buf, in_q = [], "", False
    for ch in row:
        if ch == "\u201c":
            if buf:
                runs.append((buf, PAPER))
            buf, in_q = ch, True
        elif ch == "\u201d":
            buf += ch
            runs.append((buf, GOLD))
            buf, in_q = "", False
        elif in_q:
            buf += ch
        else:
            buf += ch
    if buf:
        runs.append((buf, PAPER))
    return [(runs, None)]


print("4/5  kartu teks …")
for i, (s, e, txt) in enumerate(LINES):
    line_card(i, txt)

# hook card + identitas
hook = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(hook)
f_small = ImageFont.truetype(SANS_B, 26)
f_hook = ImageFont.truetype(SERIF_B, 86)
d.text((72, 196), "6 TAHUN JADI BEAUTY ADVISOR", font=f_small, fill=GOLD)
hook_rows = ["\u201cINI UDAH PALING", "GELAP, KAK\u201d"]
for r, row in enumerate(hook_rows):
    d.text((70, 240 + r * 98), row, font=f_hook, fill=PAPER,
           stroke_width=6, stroke_fill=(0, 0, 0, 200))
hook.save(os.path.join(CARDS, "hook.png"))

badge = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(badge)
f_b = ImageFont.truetype(SANS_B, 24)
label = "KARAKTER AI"
tw = d.textlength(label, font=f_b)
d.rounded_rectangle([60, 96, 60 + tw + 66, 152], radius=28, fill=(0, 0, 0, 120),
                    outline=(255, 255, 255, 60), width=1)
d.ellipse([78, 118, 90, 130], fill=GOLD)
d.text((104, 111), label, font=f_b, fill=(255, 255, 255, 225))
f_h = ImageFont.truetype(SANS_B, 26)
d.text((W - 70 - d.textlength("@kakalya.jujur", font=f_h), 112), "@kakalya.jujur",
       font=f_h, fill=(255, 255, 255, 170))
badge.save(os.path.join(CARDS, "badge.png"))

# ---------------------------------------------------------------- 5. overlay
print("5/5  overlay + audio …")
inputs = ["-i", graded, "-i", os.path.join(CARDS, "badge.png"),
          "-i", os.path.join(CARDS, "hook.png")]
fc = []
prev = "0:v"
idx = 3
# overlay butuh 2 input: aliran video + kartu PNG
for slot, (png, cond) in enumerate([
    ("badge.png", "gte(t,0)"),
    ("hook.png", "between(t,0,3.4)"),
], start=1):
    tag = f"v{slot}"
    fc.append(f"[{prev}][{slot}:v]overlay=0:0:enable='{cond}'[{tag}]")
    prev = tag
for i, (s, e, _) in enumerate(LINES):
    fc.append(f"[{prev}][{idx}:v]overlay=0:0:enable='between(t,{s},{e})'[v{idx}]")
    prev = f"v{idx}"
    inputs += ["-i", os.path.join(CARDS, f"sub{i:02d}.png")]
    idx += 1

# fade out kecil di akhir
fc.append(f"[{prev}]fade=t=out:st={DURATION-0.55:.2f}:d=0.55[vout]")

final = os.path.join(OUTDIR, "alya-01-shade-paling-gelap.mp4")
cmd = [FF, "-y", "-loglevel", "error"] + inputs + [
    "-i", AUDIO,
    "-filter_complex", ";".join(fc),
    "-map", "[vout]", "-map", f"{idx}:a",
    "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
    "-c:v", "libx264", "-preset", "slow", "-crf", "20", "-pix_fmt", "yuv420p",
    "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
    "-t", f"{DURATION}",
    "-movflags", "+faststart",
    final,
]
run(cmd, "overlay")
print(f"\nselesai → {final}")
print(f"ukuran  → {os.path.getsize(final)/1e6:.1f} MB")
