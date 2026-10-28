#!/usr/bin/env python3
"""Render aset brand Knot Theory.

    python3 build_brand.py          # tulis semua aset ke assets/
    python3 build_brand.py --sheet  # + preview-sheet.png

Butuh Pillow. Font di fonts/ (SIL OFL), geometri mark di knot_geometry.py.
Semua koordinat layout dihitung dari ukuran kanvas, jadi proporsinya tetap
walaupun ukuran kanvas diubah.
"""
import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

import knot_geometry as K

ROOT = Path(__file__).parent
OUT = ROOT / "assets"
OUT.mkdir(exist_ok=True)
FONTS = ROOT / "fonts"

INK_TOP = (12, 16, 24)
INK_BOTTOM = (21, 27, 40)
CREAM = (239, 231, 220)
ROSE = (217, 142, 115)
MUTED = (138, 147, 163)

SERIF = "InstrumentSerif-Regular.ttf"
SERIF_IT = "InstrumentSerif-Italic.ttf"
MONO = "IBMPlexMono-Regular.ttf"
MONO_MED = "IBMPlexMono-Medium.ttf"


# ------------------------------------------------------------------ dasar
def _lerp(a, b, t):
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))


def background(w, h, glow=0.55, at=(0.5, 0.42), grain=4.0):
    grad = Image.new("RGB", (1, 256))
    d = ImageDraw.Draw(grad)
    for y in range(256):
        d.point((0, y), _lerp(INK_TOP, INK_BOTTOM, (y / 255) ** 0.8))
    im = grad.resize((w, h), Image.BICUBIC)

    s = 128
    mask = Image.new("L", (s, s), 0)
    px = mask.load()
    cx, cy, rad = at[0] * s, at[1] * s, s * 0.8
    for y in range(s):
        for x in range(s):
            v = max(0.0, 1.0 - math.hypot((x - cx) / rad, (y - cy) / rad))
            px[x, y] = int(255 * (v ** 2.2) * glow)
    mask = mask.resize((w, h), Image.BICUBIC).filter(
        ImageFilter.GaussianBlur(max(2, w * 0.03)))
    im = Image.composite(Image.new("RGB", (w, h), (34, 44, 64)), im, mask)

    if grain:
        n = Image.effect_noise((max(1, w // 2), max(1, h // 2)), 90)
        n = n.resize((w, h), Image.BILINEAR)
        im = Image.blend(im, Image.merge("RGB", (n, n, n)), grain / 100)
    return im


def draw_mark(im, size, center, stroke_ratio=0.085, color=CREAM, inset=0.055):
    """Trefoil dengan over/under benar. Distempel lingkaran rapat (bukan line())."""
    d = ImageDraw.Draw(im)
    stroke = size * stroke_ratio
    r = stroke / 2
    subs, _ = K.build(size, center[0], center[1], stroke, inset=inset)
    for sp in subs:
        last = None
        for p in sp:
            if last is None or math.dist(p, last) >= stroke * 0.10:
                d.ellipse([p[0] - r, p[1] - r, p[0] + r, p[1] + r], fill=color)
                last = p
        for p in (sp[0], sp[-1]):
            d.ellipse([p[0] - r, p[1] - r, p[0] + r, p[1] + r], fill=color)


def font(name, px):
    return ImageFont.truetype(str(FONTS / name), max(6, int(px)))


def tracked(d, s, f, tracking, fill, center=None, left=None, top=None):
    """Teks dengan letter-spacing. center=(x, y) memusatkan kotak tinta."""
    widths = [d.textlength(c, font=f) for c in s]
    total = sum(widths) + tracking * max(0, len(s) - 1)
    if center:
        x = center[0] - total / 2
        bb = d.textbbox((0, 0), s, font=f)
        y = center[1] - (bb[1] + bb[3]) / 2
    else:
        x = left if left is not None else 0
        y = top if top is not None else 0
    for c, w in zip(s, widths):
        d.text((x, y), c, font=f, fill=fill, anchor="la")
        x += w + tracking
    return total


def rule(d, cx, y, width, color, thickness):
    d.rounded_rectangle([cx - width / 2, y - thickness / 2,
                         cx + width / 2, y + thickness / 2],
                        radius=thickness / 2, fill=color)


# ------------------------------------------------------------------ lockup
def lockup(im, cx, cy, width, mark_ratio=0.135, word_ratio=0.062,
           tag_ratio=0.024, show_tag=True, with_bg=False):
    """Mark + wordmark + garis + tagline, ditumpuk, dipusatkan di (cx, cy)."""
    d = ImageDraw.Draw(im)
    mark = width * mark_ratio
    gap1 = width * 0.018
    f_word = font(SERIF, width * word_ratio)
    track = f_word.size * 0.20
    gap2 = width * 0.022
    rule_w = width * 0.16
    rule_t = max(2, width * 0.0016)
    gap3 = width * 0.016
    f_tag = font(SERIF_IT, width * tag_ratio)

    total = mark + gap1 + f_word.size + gap2 + rule_t
    if show_tag:
        total += gap3 + f_tag.size

    y = cy - total / 2
    draw_mark(im, mark, (cx, y + mark / 2), stroke_ratio=0.088, color=CREAM)
    y += mark + gap1
    tracked(d, "KNOT THEORY", f_word, track, CREAM,
            center=(cx, y + f_word.size / 2))
    y += f_word.size + gap2
    rule(d, cx, y + rule_t / 2, rule_w, ROSE, rule_t)
    y += rule_t
    if show_tag:
        y += gap3
        tracked(d, "manusia dan ikatannya", f_tag, f_tag.size * 0.02, CREAM,
                center=(cx, y + f_tag.size / 2))


# ------------------------------------------------------------------ aset
def logo_transparent(size=1600, ratio=0.72, stroke=0.085):
    ss = 2
    S = size * ss
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    draw_mark(im, S * ratio, (S / 2, S / 2), stroke_ratio=stroke,
              color=CREAM + (255,))
    im = im.resize((size, size), Image.LANCZOS)
    im.save(OUT / f"logo-mark-transparent-{size}.png")
    return im


def lockup_transparent(w=2400, h=1400):
    ss = 2
    im = Image.new("RGBA", (w * ss, h * ss), (0, 0, 0, 0))
    lockup(im, w * ss / 2, h * ss / 2, w * ss * 0.78)
    im = im.resize((w, h), Image.LANCZOS)
    im.save(OUT / f"logo-primary-transparent-{w}.png")
    return im


def avatar(size=1080, ratio=0.58, stroke=0.098, accent=False):
    """Avatar untuk tiga platform: semuanya dipotong bulat, jadi mark dijaga
    tetap di dalam lingkaran 86% (circumradius kurva 3.727/5.472 dari bbox)."""
    ss = 2
    S = size * ss
    im = background(S, S, glow=0.45, at=(0.5, 0.46))
    draw_mark_accent(im, S * ratio, (S / 2, S / 2), stroke, accent)
    im = im.resize((size, size), Image.LANCZOS)
    name = "avatar-rose-" if accent else "avatar-"
    im.save(OUT / f"{name}{size}.png")
    # pratinjau potongan bulat seperti di aplikasi
    mask = Image.new("L", (size * 2, size * 2), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, size * 2 - 1, size * 2 - 1], fill=255)
    mask = mask.resize((size, size), Image.LANCZOS)
    prev = Image.new("RGB", (size, size), (8, 11, 17))
    prev.paste(im, (0, 0), mask)
    prev.save(OUT / f"{name}{size}-circular-preview.png")
    return im


def draw_mark_accent(im, size, center, stroke_ratio=0.098, accent=False):
    """Varian: satu untaian (yang paling bawah) diberi rose — 'satu untaian
    yang bisa kamu ikuti'. Dipakai di motion & cover, bukan di logo utama."""
    if not accent:
        return draw_mark(im, size, center, stroke_ratio=stroke_ratio)
    d = ImageDraw.Draw(im)
    stroke = size * stroke_ratio
    r = stroke / 2
    subs, _ = K.build(size, center[0], center[1], stroke, inset=0.055)
    for i, sp in enumerate(subs):
        col = ROSE if i == 2 else CREAM
        last = None
        for p in sp:
            if last is None or math.dist(p, last) >= stroke * 0.10:
                d.ellipse([p[0] - r, p[1] - r, p[0] + r, p[1] + r], fill=col)
                last = p
        for p in (sp[0], sp[-1]):
            d.ellipse([p[0] - r, p[1] - r, p[0] + r, p[1] + r], fill=col)


def mark_svg(size=512, stroke=0.085):
    """Mark vektor (stroke, round caps) untuk dipakai di Remotion/Blender/cetak."""
    subs, _ = K.build(size, size / 2, size / 2, size * stroke, inset=0.055)
    parts = []
    for sp in subs:
        sp = K.simplify(sp, tol=size * 0.0016)
        d = "M " + " L ".join(f"{x:.2f} {y:.2f}" for x, y in sp)
        parts.append(f'    <path d="{d}" />')
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" '
        f'width="{size}" height="{size}">\n'
        f'  <g fill="none" stroke="#EFE7DC" '
        f'stroke-width="{size * stroke:.2f}" '
        f'stroke-linecap="round" stroke-linejoin="round">\n'
        + "\n".join(parts) +
        "\n  </g>\n</svg>\n"
    )
    (OUT / "logo-mark.svg").write_text(svg, encoding="utf-8")
    return svg


def yt_watermark(px=150):
    ss = 4
    S = px * ss
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    draw_mark(im, S * 0.92, (S / 2, S / 2), stroke_ratio=0.11,
              color=CREAM + (235,), inset=0.03)
    im = im.resize((px, px), Image.LANCZOS)
    im.save(OUT / f"yt-watermark-{px}.png")
    return im


def youtube_banner(w=2560, h=1440):
    ss = 2
    W, H = w * ss, h * ss
    im = background(W, H, glow=0.5, at=(0.5, 0.5))

    # knot raksasa samar di dua sisi, di luar area aman
    ghost = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw_mark(ghost, H * 0.98, (W * 0.085, H * 0.50), stroke_ratio=0.045,
              color=(60, 74, 102, 255), inset=0.0)
    draw_mark(ghost, H * 0.98, (W * 0.915, H * 0.50), stroke_ratio=0.045,
              color=(60, 74, 102, 255), inset=0.0)
    ghost.putalpha(ghost.getchannel("A").point(lambda a: int(a * 0.5)))
    im = Image.alpha_composite(im.convert("RGBA"), ghost).convert("RGB")

    safe_w = 1546 / 2560 * W
    lockup(im, W / 2, H / 2, safe_w * 0.90, with_bg=True)
    im = im.resize((w, h), Image.LANCZOS)
    im.save(OUT / "yt-banner-2560x1440.jpg", quality=93, subsampling=1)

    x0, y0 = (w - 1546) // 2, (h - 423) // 2
    im.crop((x0, y0, x0 + 1546, y0 + 423)).save(
        OUT / "yt-banner-safe-1546x423.jpg", quality=93, subsampling=1)
    return im


def tt_cover(title, ep, w=1080, h=1920):
    ss = 2
    W, H = w * ss, h * ss
    im = background(W, H, glow=0.5, at=(0.5, 0.38))
    d = ImageDraw.Draw(im)
    m = W * 0.085

    # blok atas: mark + nama kanal
    draw_mark(im, W * 0.17, (W / 2, H * 0.105), stroke_ratio=0.10)
    f_brand = font(MONO_MED, W * 0.024)
    tracked(d, "KNOT THEORY", f_brand, f_brand.size * 0.34, CREAM,
            center=(W / 2, H * 0.183))

    # label episode
    f_ep = font(MONO_MED, W * 0.023)
    tracked(d, ep, f_ep, f_ep.size * 0.20, ROSE, left=m, top=H * 0.335)

    # judul
    f_t = font(SERIF, W * 0.082)
    lines = wrap(d, title, f_t, W - 2 * m)
    y = H * 0.378
    for ln in lines:
        d.text((m, y), ln, font=f_t, fill=CREAM, anchor="la")
        y += f_t.size * 1.12

    # garis + tagline di bawah judul
    rule(d, W / 2, y + H * 0.022, W * 0.20, ROSE, max(2, W * 0.003))
    f_tag = font(SERIF_IT, W * 0.030)
    tracked(d, "manusia dan ikatannya", f_tag, f_tag.size * 0.02, CREAM,
            center=(W / 2, y + H * 0.062))

    im = im.resize((w, h), Image.LANCZOS)
    im.save(OUT / f"tt-cover-{w}x{h}.jpg", quality=93, subsampling=1)
    return im


def pack(d, items, f, max_w, tracking=0.0):
    """Bagi daftar item ke baris tanpa memutus item (pemisah ' · ')."""
    lines, cur = [], []
    for it in items:
        trial = cur + [it]
        w = sum(d.textlength(x, font=f) for x in trial) + \
            tracking * (len(trial) - 1) + d.textlength("  ·  ", font=f) * (len(trial) - 1)
        if cur and w > max_w:
            lines.append(cur)
            cur = [it]
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines


def wrap(d, text, f, max_w):
    words, lines, cur = text.split(), [], ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if d.textlength(t, font=f) <= max_w:
            cur = t
        else:
            lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def yt_thumb(w=1280, h=720, title="JUDUL EPISODE"):
    ss = 2
    W, H = w * ss, h * ss
    im = background(W, H, glow=0.5, at=(0.42, 0.45))
    d = ImageDraw.Draw(im)
    m = W * 0.055
    draw_mark(im, H * 0.20, (m + H * 0.10, m + H * 0.10), stroke_ratio=0.10)
    f_b = font(MONO_MED, W * 0.0145)
    tracked(d, "KNOT THEORY", f_b, f_b.size * 0.30, CREAM,
            left=m + H * 0.20 + W * 0.014, top=m + H * 0.10 - f_b.size * 0.55)

    f_t = font(SERIF, W * 0.072)
    lines = wrap(d, title, f_t, W * 0.46)
    y = H * 0.42
    for ln in lines:
        d.text((m, y), ln, font=f_t, fill=CREAM, anchor="la")
        y += f_t.size * 1.10
    rule(d, m + W * 0.06, y + H * 0.035, W * 0.12, ROSE, max(2, W * 0.0026))

    # knot besar di kanan, sebagian keluar kanvas
    big = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw_mark(big, H * 0.86, (W * 0.855, H * 0.52), stroke_ratio=0.075,
              color=(239, 231, 220, 46), inset=0.02)
    im = Image.alpha_composite(im.convert("RGBA"), big).convert("RGB")
    im = im.resize((w, h), Image.LANCZOS)
    im.save(OUT / f"yt-thumb-template-{w}x{h}.jpg", quality=93, subsampling=1)
    return im


def ig_pinned(w=1080, h=1350):
    ss = 2
    W, H = w * ss, h * ss
    im = background(W, H, glow=0.5, at=(0.5, 0.36))
    d = ImageDraw.Draw(im)
    m = W * 0.085

    draw_mark(im, W * 0.20, (W / 2, H * 0.20), stroke_ratio=0.10)
    f_brand = font(SERIF, W * 0.085)
    tracked(d, "KNOT THEORY", f_brand, f_brand.size * 0.18, CREAM,
            center=(W / 2, H * 0.315))
    rule(d, W / 2, H * 0.365, W * 0.17, ROSE, max(2, W * 0.0035))

    f_lead = font(SERIF_IT, W * 0.052)
    lead = "Kanal tentang ikatan yang tidak bisa dilepas sebelah pihak."
    y = H * 0.415
    for ln in wrap(d, lead, f_lead, W - 2 * m):
        tracked(d, ln, f_lead, 0, CREAM, center=(W / 2, y))
        y += f_lead.size * 1.25

    f_list = font(MONO, W * 0.024)
    items = ["KERJA", "INSTITUSI", "MASYARAKAT", "ALAM", "TEKNOLOGI",
             "EKONOMI", "PERTEMANAN"]
    lines = pack(d, items, f_list, W * 0.78, f_list.size * 0.18)
    yy = H * 0.615
    for ln in lines:
        tracked(d, "  ·  ".join(ln), f_list, f_list.size * 0.18, MUTED,
                center=(W / 2, yy))
        yy += f_list.size * 1.9

    f_hand = font(MONO_MED, W * 0.026)
    tracked(d, "@knottheory", f_hand, f_hand.size * 0.14, CREAM,
            center=(W / 2, H * 0.88))
    im = im.resize((w, h), Image.LANCZOS)
    im.save(OUT / "ig-pinned-1080x1350.jpg", quality=93, subsampling=1)
    return im


def ig_highlight(label, w=1080, h=1920):
    ss = 2
    W, H = w * ss, h * ss
    im = background(W, H, glow=0.45, at=(0.5, 0.5))
    d = ImageDraw.Draw(im)
    # tampil sebagai lingkaran 1:1 di tengah -> semua isi di dalam kotak tengah
    side = min(W, H)
    top = (H - side) / 2
    draw_mark(im, side * 0.42, (W / 2, top + side * 0.44), stroke_ratio=0.105)
    f = font(MONO_MED, side * 0.052)
    tracked(d, label, f, f.size * 0.22, CREAM,
            center=(W / 2, top + side * 0.70))
    im = im.resize((w, h), Image.LANCZOS)
    im.save(OUT / f"ig-highlight-{label.lower()}-{w}x{h}.jpg",
            quality=93, subsampling=1)
    return im


# ------------------------------------------------------------------ sheet
def preview_sheet():
    W, H = 2400, 1700
    im = Image.new("RGB", (W, H), (8, 11, 17))
    d = ImageDraw.Draw(im)
    f_h = font(MONO_MED, 34)
    f_c = font(MONO, 24)

    def paste(path, box, label, panel=None):
        x, y, w, h = box
        a = Image.open(OUT / path)
        a.thumbnail((w, h), Image.LANCZOS)
        if panel:
            d.rectangle([x - 10, y - 10, x + a.size[0] + 10, y + a.size[1] + 10],
                        fill=panel)
        im.paste(a, (x, y), a if a.mode == "RGBA" else None)
        d.text((x, y + a.size[1] + 14), label, font=f_c, fill=(150, 158, 175))
        d.rectangle([x, y, x + a.size[0], y + a.size[1]], outline=(38, 46, 62))

    d.text((60, 54), "KNOT THEORY — brand kit", font=f_h, fill=CREAM)
    d.text((60, 104), "logo, avatar, banner tiga platform (ukuran final)",
           font=f_c, fill=(150, 158, 175))

    paste("logo-primary-transparent-2400.png", (60, 170, 760, 420),
          "logo utama (transparan) — ditaruh di atas ink", panel=(14, 18, 27))
    paste("yt-thumb-template-1280x720.jpg", (1480, 170, 560, 315),
          "YT thumbnail 1280×720")
    paste("avatar-1080.png", (880, 170, 260, 260), "avatar 1080×1080")
    paste("yt-watermark-150.png", (1180, 170, 150, 150), "watermark 150×150")
    paste("tt-cover-1080x1920.jpg", (60, 700, 300, 534), "TikTok cover 1080×1920")
    paste("ig-pinned-1080x1350.jpg", (400, 700, 300, 375), "IG pinned 1080×1350")
    paste("ig-highlight-sumber-1080x1920.jpg", (740, 700, 250, 444),
          "IG highlight 1080×1920")
    paste("yt-banner-2560x1440.jpg", (1040, 700, 1300, 731),
          "YouTube banner 2560×1440")
    paste("yt-banner-safe-1546x423.jpg", (1040, 1470, 600, 164),
          "safe area 1546×423 (yang terlihat di mobile)")
    im.save(OUT / "preview-sheet.png")
    return im


if __name__ == "__main__":
    logo_transparent()
    lockup_transparent()
    avatar()
    avatar(accent=True)
    mark_svg()
    yt_watermark()
    yt_thumb(title="Aturan tahun 1517 yang masih dipakai")
    youtube_banner()
    tt_cover("Aturan tahun 1517 yang masih dipakai", "EP. 05 · S5 · ALAM")
    ig_pinned()
    for lab in ("EPISODE", "SUMBER", "TANYA"):
        ig_highlight(lab)
    if "--sheet" in sys.argv:
        preview_sheet()
    print("selesai ->", OUT)
    total = 0
    for p in sorted(OUT.iterdir()):
        kb = p.stat().st_size / 1024
        total += kb
        print(f"  {p.name:40s} {kb:7.0f} KB")
    print(f"  {'TOTAL':40s} {total:7.0f} KB")
