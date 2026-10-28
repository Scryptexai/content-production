#!/usr/bin/env python3
"""
Tropical / Subtropical — narration explainer renderer.

Menerapkan motion grammar dari video-shotcraft (kinetic type, data viz,
diagram, camera moves, hard cuts, breathing holds) dengan renderer native
(Pillow + ffmpeg), karena Chromium tidak tersedia di lingkungan ini.

Output: 10 scene mp4 (video+audio) + concat final.
"""
import math
import os
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.abspath(__file__))
FF = open(os.path.join(ROOT, "..", "..", ".ffmpeg-path")).read().strip()

W, H = 1080, 1920
FPS = 30

BG = (11, 12, 10)
PAPER = (237, 228, 211)
MUTED = (139, 133, 119)
TERRA = (192, 96, 58)
TEAL = (46, 95, 91)
GOLD = (201, 162, 39)
WHITE = (255, 255, 255)

F = "/usr/share/fonts/truetype/dejavu/"
SERIF = F + "DejaVuSerif-Bold.ttf"
SANS_B = F + "DejaVuSans-Bold.ttf"
SANS = F + "DejaVuSans.ttf"
MONO = F + "DejaVuSansMono-Bold.ttf"

_fc = {}


def font(path, size):
    k = (path, size)
    if k not in _fc:
        _fc[k] = ImageFont.truetype(path, size)
    return _fc[k]


# ---------------------------------------------------------------- easing
def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def ease_out(t):
    t = clamp(t)
    return 1 - (1 - t) ** 3


def ease_in_out(t):
    t = clamp(t)
    return 3 * t * t - 2 * t * t * t


def prog(t, t0, dur):
    return clamp((t - t0) / dur) if dur > 0 else 1.0


# ---------------------------------------------------------------- assets
_bgcache = {}


def load_bg(name, zoom=1.12):
    """Muat + crop ke rasio 9:16, sedikit lebih besar untuk Ken Burns."""
    k = (name, zoom)
    if k in _bgcache:
        return _bgcache[k]
    p = os.path.join(ROOT, "assets", name)
    im = Image.open(p).convert("RGB")
    tw, th = int(W * zoom), int(H * zoom)
    s = max(tw / im.width, th / im.height)
    im = im.resize((max(tw, int(im.width * s)), max(th, int(im.height * s))), Image.LANCZOS)
    x = (im.width - tw) // 2
    y = (im.height - th) // 2
    im = im.crop((x, y, x + tw, y + th))
    _bgcache[k] = im
    return im


def bg_frame(name, t, t1, z0=1.0, z1=1.06, dy=0.0):
    """Ken Burns: crop bergerak dari tekstur besar."""
    im = load_bg(name)
    p = ease_in_out(prog(t, 0, max(0.001, t1)))
    z = z0 + (z1 - z0) * p
    cw, ch = int(W / z * (1.12 / 1.12)), int(H / z)
    cw, ch = int(W / z), int(H / z)
    cw, ch = min(cw, im.width), min(ch, im.height)
    cx = im.width / 2
    cy = im.height / 2 + dy * ch * p
    x = clamp(cx - cw / 2, 0, im.width - cw)
    y = clamp(cy - ch / 2, 0, im.height - ch)
    return im.crop((int(x), int(y), int(x + cw), int(y + ch))).resize((W, H), Image.BILINEAR)


_vig = None


def vignette():
    global _vig
    if _vig is None:
        v = Image.new("L", (W // 4, H // 4), 0)
        d = ImageDraw.Draw(v)
        d.ellipse([-W // 8, -H // 8, W // 4 + W // 8, H // 4 + H // 8], fill=255)
        v = v.resize((W, H), Image.BILINEAR).filter(ImageFilter.GaussianBlur(60))
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ov.putalpha(Image.eval(v, lambda x: int((255 - x) * 0.62)))
        _vig = ov
    return _vig


_scrims = {}


def scrim(img, top=0.0, bottom=0.0, mid=0.0):
    """Gradien gelap untuk keterbacaan teks di atas foto terang."""
    k = (round(top, 2), round(bottom, 2), round(mid, 2))
    if k not in _scrims:
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        if top > 0:
            for i in range(500):
                d.rectangle([0, i, W, i + 1], fill=(8, 9, 7, int(255 * top * (1 - i / 500) ** 2)))
        if bottom > 0:
            for i in range(700):
                d.rectangle([0, H - i - 1, W, H - i], fill=(8, 9, 7, int(255 * bottom * (1 - i / 700) ** 1.6)))
        if mid > 0:
            band = int(H * 0.34)
            y0 = (H - band) // 2
            for i in range(band):
                a = mid * (1 - abs(i - band / 2) / (band / 2)) ** 1.5
                d.rectangle([0, y0 + i, W, y0 + i + 1], fill=(8, 9, 7, int(255 * a)))
        _scrims[k] = ov
    out = Image.alpha_composite(img.convert("RGBA"), _scrims[k])
    img.paste(out.convert("RGB"), (0, 0))


_bands = {}


def band(img, y0, y1, strength=0.62):
    """Pita gelap lembut di belakang blok teks (lower-third)."""
    k = (y0, y1, round(strength, 2))
    if k not in _bands:
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        pad = 150
        a0, a1 = max(0, y0 - pad), min(H, y1 + pad)
        for y in range(a0, a1):
            if y < y0:
                f = 1 - (y0 - y) / pad
            elif y > y1:
                f = 1 - (y - y1) / pad
            else:
                f = 1.0
            d.rectangle([0, y, W, y + 1], fill=(8, 9, 7, int(255 * strength * (f ** 1.5))))
        _bands[k] = ov
    out = Image.alpha_composite(img.convert("RGBA"), _bands[k])
    img.paste(out.convert("RGB"), (0, 0))


_grain = []


def grain(i):
    if not _grain:
        import random
        rnd = random.Random(7)
        for _ in range(6):
            g = Image.new("L", (W // 3, H // 3))
            px = g.load()
            for yy in range(0, H // 3, 2):
                for xx in range(0, W // 3, 2):
                    n = rnd.randint(0, 255)
                    px[xx, yy] = n
                    if xx + 1 < W // 3:
                        px[xx + 1, yy] = n
                    if yy + 1 < H // 3:
                        px[xx, yy + 1] = n
                        if xx + 1 < W // 3:
                            px[xx + 1, yy + 1] = n
            _grain.append(g.resize((W, H), Image.NEAREST))
    return _grain[i % 6]


# ---------------------------------------------------------------- text
def tw(d, s, f):
    b = d.textbbox((0, 0), s, font=f)
    return b[2] - b[0]


def wrap(d, s, f, maxw):
    out, cur = [], ""
    for w in s.split():
        trial = (cur + " " + w).strip()
        if tw(d, trial, f) <= maxw or not cur:
            cur = trial
        else:
            out.append(cur)
            cur = w
    if cur:
        out.append(cur)
    return out


def text_center(img, s, f, y, fill, alpha=255, tracking=0):
    d = ImageDraw.Draw(img)
    if tracking == 0:
        x = (W - tw(d, s, f)) / 2
        d.text((x, y), s, font=f, fill=fill + (alpha,))
    else:
        total = sum(tw(d, c, f) + tracking for c in s) - tracking
        x = (W - total) / 2
        for c in s:
            d.text((x, y), c, font=f, fill=fill + (alpha,))
            x += tw(d, c, f) + tracking


def words_reveal(img, s, f, y, fill, t, t0, per=0.085, alpha=255, maxw=None, line_gap=1.18):
    """Kata muncul satu per satu (opacity ramp), rata tengah."""
    d = ImageDraw.Draw(img)
    lines = wrap(d, s, f, maxw) if maxw else [s]
    n = 0
    for row in lines:
        x0 = (W - tw(d, row, f)) / 2
        for w in row.split(" "):
            a = clamp((t - (t0 + n * per)) / 0.18) * alpha
            if a > 3:
                d.text((x0, y), w, font=f, fill=fill + (int(a),))
            x0 += tw(d, w + " ", f)
            n += 1
        y += int(f.size * line_gap)
    return y


def rule(img, y, t, t0, w_max=760, color=GOLD, dur=0.7):
    p = ease_out(prog(t, t0, dur))
    if p <= 0:
        return
    d = ImageDraw.Draw(img)
    w = int(w_max * p)
    d.rectangle([(W - w) // 2, y, (W + w) // 2, y + 2], fill=color + (255,))


def label(img, s, y, color=MUTED, size=27, alpha=255, t=None, t0=0):
    f = font(SANS_B, size)
    if t is not None:
        alpha = int(clamp((t - t0) / 0.3) * alpha)
    if alpha > 2:
        text_center(img, s, f, y, color, alpha, tracking=6)


def big_number(img, s, y, color=PAPER, size=200, alpha=255):
    f = font(MONO, size)
    text_center(img, s, f, y, color, alpha)


# ---------------------------------------------------------------- drawing kit
def arrow_down(d, x, y0, y1, color, prog_=1.0, width=6):
    if prog_ <= 0:
        return
    y_end = y0 + (y1 - y0) * prog_
    d.line([x, y0, x, y_end - 14 * prog_], fill=color + (255,), width=width)
    if prog_ > 0.85:
        s = 16
        d.polygon([(x, y_end), (x - s, y_end - s), (x + s, y_end - s)], fill=color + (255,))


def arrow_up(d, x, y0, y1, color, prog_=1.0, width=6):
    if prog_ <= 0:
        return
    y_end = y0 - (y0 - y1) * prog_
    d.line([x, y0, x, y_end + 14 * prog_], fill=color + (255,), width=width)
    if prog_ > 0.85:
        s = 16
        d.polygon([(x, y_end), (x - s, y_end + s), (x + s, y_end + s)], fill=color + (255,))


def panel(d, box, fill=None, outline=MUTED, a=40, width=2, radius=18):
    d.rounded_rectangle(box, radius=radius, fill=(fill + (a,)) if fill else None,
                        outline=outline + (110,), width=width)


# ---------------------------------------------------------------- scenes
def scene1(t, dur, img):
    """Cold open: 12°C / 50% lalu potong ke Jakarta."""
    cut = 8.0
    if t < cut:
        base = bg_frame("02-cold-window.jpg", t, cut, 1.04, 1.10, 0.02)
    else:
        base = bg_frame("03-tropical-window.jpg", t - cut, dur - cut, 1.10, 1.02, -0.02)
    img.paste(base, (0, 0))
    scrim(img, top=0.35, bottom=0.55)

    if t < cut:
        a1 = int(255 * clamp((t - 0.5) / 0.5))
        if a1 > 2:
            text_center(img, "12°C", font(MONO, 200), 520, PAPER, a1)
            label(img, "SUHU RATA-RATA   ·   EROPA", 760, MUTED, 25, a1)
    else:
        a1 = int(255 * clamp((t - cut - 0.1) / 0.4))
        if a1 > 2:
            band(img, 1060, 1350, 0.68)
            label(img, "KOTA INI", 1080, GOLD, 26, a1)
            text_center(img, "JAKARTA", font(SERIF, 132), 1130, PAPER, a1)
            label(img, "27–30°C   ·   KELEMBAPAN 74–84%", 1310, PAPER, 26, a1)


def scene2(t, dur, img):
    """Data: tiga statistik kota tropis."""
    img.paste(bg_frame("03-tropical-window.jpg", t, dur, 1.06, 1.0, 0.01), (0, 0))
    ov = Image.new("RGBA", (W, H), (11, 12, 10, 150))
    img.alpha_composite(ov) if img.mode == "RGBA" else img.paste(Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB"), (0, 0))

    label(img, "JAKARTA  ·  DATA IKLIM", 250, GOLD, 26, t=t, t0=0.2)
    rule(img, 310, t, 0.4, 700, GOLD)

    rows = [("SUHU", "27–30", "°C", 0.9), ("KELEMBAPAN", "74–84", "%", 2.4), ("INDEKS UV", "11", "EXTREME", 4.4)]
    y = 470
    for name, num, unit, t0 in rows:
        a = int(255 * clamp((t - t0) / 0.35))
        if a <= 2:
            y += 330
            continue
        d = ImageDraw.Draw(img)
        d.text((120, y), name, font=font(SANS_B, 30), fill=MUTED + (a,))
        d.text((120, y + 60), num, font=font(MONO, 150), fill=PAPER + (a,))
        d.text((120 + tw(d, num, font(MONO, 150)) + 18, y + 132), unit, font=font(SANS_B, 40), fill=TERRA + (a,))
        d.rectangle([120, y + 262, 960, y + 263], fill=(255, 255, 255, 26))
        y += 330

    label(img, "SUMBER: BMKG / WEATHER2TRAVEL / BRITANNICA", 1700, MUTED, 21, t=t, t0=5.4)


def scene3(t, dur, img):
    """Frame: bukan detail kecil."""
    img.paste(bg_frame("01-skin-macro.jpg", t, dur, 1.08, 1.02, 0.01), (0, 0))
    ov = Image.new("RGBA", (W, H), (11, 12, 10, 120))
    base = img.convert("RGBA")
    img.paste(Image.alpha_composite(base, ov).convert("RGB"), (0, 0))

    band(img, 580, 1080, 0.66)
    words_reveal(img, "BUKAN", font(SERIF, 130), 620, PAPER, t, 0.25, maxw=900)
    words_reveal(img, "DETAIL KECIL.", font(SERIF, 130), 760, TERRA, t, 0.75, maxw=900)
    rule(img, 950, t, 1.5, 620, GOLD)
    words_reveal(img, "dua lingkungan. dua kimia.", font(SANS, 46), 1010, PAPER, t, 2.0, maxw=820)


def scene4(t, dur, img):
    """Humektan: definisi + pertanyaan."""
    img.paste(bg_frame("04-glycerin-drop.jpg", t, dur, 1.10, 1.02, -0.01), (0, 0))
    band(img, 280, 1000, 0.62)
    label(img, "BAHAN 01", 300, GOLD, 28, t=t, t0=0.2)
    words_reveal(img, "HUMEKTAN", font(SERIF, 142), 380, PAPER, t, 0.5, maxw=980)
    rule(img, 570, t, 1.1, 640, TERRA)
    words_reveal(img, "gliserin  ·  asam hialuronat", font(SANS, 44), 630, PAPER, t, 1.4, maxw=900)
    words_reveal(img, "menarik air", font(SANS_B, 62), 760, TEAL, t, 2.6, maxw=900)

    a = int(255 * clamp((t - 7.2) / 0.5))
    if a > 2:
        text_center(img, "dari mana?", font(SERIF, 96), 900, GOLD, a)


def scene5(t, dur, img):
    """Diagram humektan: lembap vs kering."""
    img.paste(bg_frame("01-skin-macro.jpg", t, dur, 1.05, 1.0, 0.0), (0, 0))
    ov = Image.new("RGBA", (W, H), (11, 12, 10, 210))
    img.paste(Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB"), (0, 0))
    d = ImageDraw.Draw(img)
    label(img, "HUMEKTAN  ·  DUA KONDISI", 200, GOLD, 25, t=t, t0=0.2)

    def panels(x0, x1, acc, title, rh, t0, up, lines, verdict):
        p = ease_out(prog(t, t0, 0.8))
        if p <= 0:
            return
        y0, y1 = 470, 1290
        d.rounded_rectangle([x0, y0, x1, y1], radius=20,
                            fill=(17, 19, 16, int(215 * p)),
                            outline=acc + (int(230 * p),), width=3)
        d.rectangle([x0, y0 + 24, x0 + 8, y0 + 96], fill=acc + (int(255 * p),))
        d.text((x0 + 34, y0 + 34), title, font=font(SANS_B, 30), fill=acc + (int(255 * p),))
        d.text((x0 + 34, y0 + 84), rh, font=font(MONO, 56), fill=PAPER + (int(255 * p),))

        # garis kulit
        ys = 1120
        d.line([x0 + 30, ys, x1 - 30, ys], fill=PAPER + (int(150 * p),), width=3)
        d.text((x0 + 30, ys + 16), "permukaan kulit", font=font(SANS, 24), fill=MUTED + (int(220 * p),))

        # panah
        for i, ax in enumerate([x0 + 105, x0 + 205, x0 + 305]):
            a2 = ease_out(prog(t, t0 + 0.5 + i * 0.22, 0.65))
            if up:
                arrow_up(d, ax, ys - 20, 820 - i * 18, acc, a2, 7)
            else:
                arrow_down(d, ax, 820 + i * 18, ys - 20, acc, a2, 7)
        d.text((x0 + 34, 780), "air dari kulit" if up else "air dari udara",
               font=font(SANS, 28), fill=PAPER + (int(220 * p),))

        yy = ys + 76
        for txt, col in lines:
            d.text((x0 + 30, yy), txt, font=font(SANS_B if col is not PAPER else SANS, 30),
                   fill=col + (int(255 * p),))
            yy += 46

    panels(70, 510, TEAL, "LEMBAP", "80% RH", 1.0, False,
           [("→ lengket,", TERRA), ("  tidak menguap", PAPER)], "x")
    panels(570, 1010, TERRA, "KERING", "40% RH", 7.6, True,
           [("→ makin kering", TERRA), ("  di ruang ber-AC", PAPER)], "x")

    a = int(255 * clamp((t - 16.6) / 0.6))
    if a > 2:
        text_center(img, "bahan yang sama. dua hasil.", font(SERIF, 60), 1450, PAPER, a)


def scene6(t, dur, img):
    """Oklusif: rumah kaca."""
    img.paste(bg_frame("05-petrolatum.jpg", t, dur, 1.02, 1.10, -0.01), (0, 0))
    band(img, 240, 640, 0.58)
    label(img, "BAHAN 02", 260, GOLD, 28, t=t, t0=0.2)
    words_reveal(img, "OKLUSIF", font(SERIF, 150), 330, PAPER, t, 0.5, maxw=980)
    words_reveal(img, "petrolatum · minyak mineral · lilin", font(SANS, 40), 520, PAPER, t, 1.3, maxw=920)
    rule(img, 600, t, 2.0, 620, TERRA)

    # diagram: layer + panas terperangkap (muncul di detik 10)
    p = ease_out(prog(t, 10.0, 0.9))
    if p > 0:
        d = ImageDraw.Draw(img)
        ytop = 760
        # lapisan oklusif
        d.rounded_rectangle([90, ytop, 990, ytop + 46], radius=8, fill=TERRA + (int(230 * p),))
        d.text((110, ytop - 46), "LAPISAN OKLUSIF", font=font(SANS_B, 24), fill=TERRA + (int(255 * p),))
        # kulit
        d.rectangle([90, ytop + 46, 990, ytop + 300], fill=(30, 26, 22, int(220 * p)))
        d.text((110, ytop + 250), "kulit", font=font(SANS, 26), fill=MUTED + (200,))
        # panah keringat terperangkap
        for i, ax in enumerate([230, 420, 610, 800]):
            a2 = ease_out(prog(t, 10.6 + i * 0.15, 0.6))
            arrow_up(d, ax, ytop + 240, ytop + 90, GOLD, a2, 5)
        d.text((110, ytop + 316), "keringat tidak bisa keluar · panas terperangkap",
               font=font(SANS, 28), fill=PAPER + (int(235 * p),))

    a = int(255 * clamp((t - 17.5) / 0.6))
    if a > 2:
        words_reveal(img, "kamu menyebutnya breakout.", font(SERIF, 64), 1250, PAPER, t, 17.5, maxw=940)
        words_reveal(img, "padahal itu cuaca.", font(SERIF, 64), 1340, TERRA, t, 19.0, maxw=940)


def scene7(t, dur, img):
    """Panas: Arrhenius + zona iklim."""
    img.paste(bg_frame("06-heat-car.jpg", t, dur, 1.10, 1.0, 0.005), (0, 0))
    ov = Image.new("RGBA", (W, H), (11, 12, 10, 170))
    img.paste(Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB"), (0, 0))

    label(img, "PANAS  ·  KIMIA", 230, GOLD, 26, t=t, t0=0.2)
    words_reveal(img, "×2", font(MONO, 250), 290, TERRA, t, 0.6, maxw=900)
    words_reveal(img, "setiap +10°C, laju reaksi berlipat dua",
                 font(SANS, 40), 640, PAPER, t, 1.6, maxw=900)

    # grafik eksponensial
    p = ease_out(prog(t, 8.5, 1.8))
    if p > 0:
        d = ImageDraw.Draw(img)
        gx0, gy0, gx1, gy1 = 140, 1250, 940, 780
        d.line([gx0, gy0, gx1, gy0], fill=PAPER + (120,), width=2)
        d.line([gx0, gy0, gx0, gy1], fill=PAPER + (120,), width=2)
        d.text((gx1 - 290, gy0 + 46), "suhu penyimpanan", font=font(SANS, 24), fill=MUTED + (200,))
        d.text((gx0 - 10, gy1 - 40), "laju", font=font(SANS, 24), fill=MUTED + (200,))
        pts = []
        n = int(120 * p)
        for i in range(n):
            u = i / 119
            x = gx0 + u * (gx1 - gx0)
            y = gy0 - (math.exp(2.0 * u) - 1) / (math.exp(2.0) - 1) * (gy0 - gy1)
            pts.append((x, y))
        if len(pts) > 1:
            d.line(pts, fill=GOLD + (255,), width=6, joint="curve")
        for xx, lab_ in [(gx0 + 0.0 * (gx1 - gx0), "25°"), (gx0 + 0.55 * (gx1 - gx0), "30°"),
                         (gx0 + 0.85 * (gx1 - gx0), "40°")]:
            if p > 0.5:
                d.line([xx, gy0, xx, gy0 - 12], fill=PAPER + (120,), width=2)
                d.text((xx - 18, gy0 + 14), lab_, font=font(MONO, 26), fill=PAPER + (230,))

    # zona iklim
    p2 = ease_out(prog(t, 14.0, 1.0))
    if p2 > 0:
        d = ImageDraw.Draw(img)
        y = 1400
        d.text((120, y), "ZONA UJI STABILITAS", font=font(SANS_B, 24), fill=MUTED + (255,))
        # II
        d.text((120, y + 50), "II  EROPA", font=font(SANS_B, 28), fill=PAPER + (int(255 * p2),))
        d.text((520, y + 44), "25°C / 60%", font=font(MONO, 34), fill=MUTED + (int(255 * p2),))
        # IVb
        d.text((120, y + 150), "IVb  INDONESIA", font=font(SANS_B, 28), fill=GOLD + (int(255 * p2),))
        d.text((520, y + 144), "30°C / 75%", font=font(MONO, 34), fill=PAPER + (int(255 * p2),))
        d.rectangle([120, y + 112, 120 + int(760 * p2), y + 116], fill=(255, 255, 255, 30))
        d.rectangle([120, y + 212, 120 + int(960 * p2), y + 216], fill=GOLD + (170,))

    a = int(255 * clamp((t - 24.5) / 0.6))
    if a > 2:
        text_center(img, "di dalam mobil: 40°C+", font(SANS_B, 52), 1690, TERRA, a)


def scene8(t, dur, img):
    """UV."""
    img.paste(bg_frame("07-uv-sun.jpg", t, dur, 1.04, 1.12, 0.01), (0, 0))
    label(img, "ULTRAVIOLET", 250, GOLD, 26, t=t, t0=0.2)

    # gauge UV
    p = ease_out(prog(t, 1.2, 2.2))
    d = ImageDraw.Draw(img)
    cx, cy, r = W // 2, 830, 250
    d.arc([cx - r, cy - r, cx + r, cy + r], 180, 360, fill=(255, 255, 255, 40), width=14)
    if p > 0:
        end = 180 + 180 * p
        col = TEAL if p < 0.55 else (GOLD if p < 0.8 else TERRA)
        d.arc([cx - r, cy - r, cx + r, cy + r], 180, end, fill=col + (255,), width=14)
    a = int(255 * clamp((t - 2.6) / 0.5))
    if a > 2:
        text_center(img, "11", font(MONO, 210), 620, PAPER, a)
        text_center(img, "EXTREME", font(SANS_B, 40), 880, TERRA, a)

    words_reveal(img, "SPF mengukur UVB.", font(SANS_B, 58), 1010, PAPER, t, 5.2, maxw=900)
    words_reveal(img, "UVA yang membuat menua dan bercak.", font(SANS, 44), 1100, PAPER, t, 9.0, maxw=920)
    words_reveal(img, "dan UVA tidak berubah sepanjang tahun.", font(SANS, 40), 1170, MUTED, t, 12.5, maxw=920)

    p3 = ease_out(prog(t, 15.6, 0.7))
    if p3 > 0:
        d = ImageDraw.Draw(img)
        box = [120, 1300, 960, 1500]
        d.rounded_rectangle(box, radius=14, outline=GOLD + (int(230 * p3),), width=3)
        text_center(img, "PA++++", font(MONO, 96), 1330, GOLD, int(255 * p3))
        text_center(img, "BUKAN KEMEWAHAN — SYARAT MINIMUM", font(SANS_B, 28), 1480, PAPER, int(240 * p3))


def scene9(t, dur, img):
    """Solusi: tiga perubahan."""
    img.paste(bg_frame("08-serum-bottle.jpg", t, dur, 1.02, 1.10, 0.0), (0, 0))
    ov = Image.new("RGBA", (W, H), (11, 12, 10, 150))
    img.paste(Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB"), (0, 0))
    label(img, "YANG BERUBAH", 230, GOLD, 26, t=t, t0=0.2)

    items = [
        ("01", "TEKSTUR", "gel · essence · water-break\nbukan krim tebal", 1.2),
        ("02", "URUTAN", "humektan di kulit lembap\nlalu emolien ringan", 11.0),
        ("03", "PENYIMPANAN", "lemari, bukan kamar mandi\nvitamin C: botol gelap, tertutup", 21.0),
    ]
    y = 330
    for num, head, body, t0 in items:
        a = int(255 * clamp((t - t0) / 0.45))
        if a > 2:
            d = ImageDraw.Draw(img)
            d.text((100, y), num, font=font(MONO, 62), fill=GOLD + (a,))
            d.text((210, y + 8), head, font=font(SANS_B, 46), fill=PAPER + (a,))
            yy = y + 78
            for ln in body.split("\n"):
                d.text((210, yy), ln, font=font(SANS, 34), fill=MUTED + (a,))
                yy += 46
            d.rectangle([100, y + 200, 100 + int(860 * ease_out(prog(t, t0, 0.8))), y + 202],
                        fill=(255, 255, 255, 30))
        y += 330

    a = int(255 * clamp((t - 27.5) / 0.8))
    if a > 2:
        words_reveal(img, "oksigen, bukan matahari,", font(SERIF, 52), 1400, PAPER, t, 27.5, maxw=920)
        words_reveal(img, "yang membunuh vitamin C.", font(SERIF, 52), 1470, TERRA, t, 28.4, maxw=920)


def scene10(t, dur, img):
    """Penutup + pertanyaan."""
    img.paste(bg_frame("03-tropical-window.jpg", t, dur, 1.06, 1.00, 0.0), (0, 0))
    ov = Image.new("RGBA", (W, H), (11, 12, 10, 165))
    img.paste(Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB"), (0, 0))

    band(img, 520, 1010, 0.70)
    words_reveal(img, "KULIT TROPIS.", font(SERIF, 96), 560, PAPER, t, 0.3, maxw=940)
    words_reveal(img, "FORMULA TROPIS.", font(SERIF, 96), 680, TERRA, t, 1.2, maxw=940)
    rule(img, 900, t, 2.4, 620, GOLD)

    a = int(255 * clamp((t - 4.6) / 0.6))
    if a > 2:
        text_center(img, "kotamu mana?", font(SANS_B, 64), 960, GOLD, a)

    a2 = int(255 * clamp((t - 6.4) / 0.7))
    if a2 > 2:
        d = ImageDraw.Draw(img)
        f = font(SANS, 30)
        for i, ln in enumerate(["Sumber: WHO TRS 953 · ASEAN Stability Guideline",
                                "ICH Q1A(R2) zona iklim · data iklim Jakarta 2026"]):
            x = (W - tw(d, ln, f)) / 2
            d.text((x, 1620 + i * 42), ln, font=f, fill=MUTED + (a2,))


SCENES = [
    ("01", "vo-01.mp3", 1.6, 0.45, scene1),
    ("02", "vo-02.mp3", 0.30, 0.40, scene2),
    ("03", "vo-03.mp3", 0.30, 0.45, scene3),
    ("04", "vo-04.mp3", 0.30, 0.40, scene4),
    ("05", "vo-05.mp3", 0.30, 0.40, scene5),
    ("06", "vo-06.mp3", 0.30, 0.40, scene6),
    ("07", "vo-07.mp3", 0.30, 0.45, scene7),
    ("08", "vo-08.mp3", 0.30, 0.40, scene8),
    ("09", "vo-09.mp3", 0.30, 0.40, scene9),
    ("10", "vo-10.mp3", 0.30, 1.10, scene10),
]


def audio_dur(p):
    out = subprocess.run([FF, "-hide_banner", "-i", p], capture_output=True, text=True).stderr
    for line in out.splitlines():
        if "Duration:" in line:
            h, m, s = line.split("Duration:")[1].split(",")[0].strip().split(":")
            return int(h) * 3600 + int(m) * 60 + float(s)
    raise RuntimeError("no duration " + p)


def build_scene(idx):
    sid, vo, lead, tail, fn = SCENES[idx]
    vp = os.path.join(ROOT, "audio", vo)
    ad = audio_dur(vp)
    dur = lead + ad + tail
    nfr = int(round(dur * FPS))
    outdir = os.path.join(ROOT, "build")
    os.makedirs(outdir, exist_ok=True)
    tmp = os.path.join(outdir, f"s{sid}.mp4")

    cmd = [FF, "-y", "-loglevel", "error",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-pix_fmt", "yuv420p",
           "-r", str(FPS), tmp]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)

    for i in range(nfr):
        t = i / FPS
        img = Image.new("RGB", (W, H), BG)
        fn(t, dur, img)
        img = img.convert("RGBA")
        img.alpha_composite(vignette())
        g = grain(i)
        base = img.convert("RGB")
        reg = Image.blend(base, Image.merge("RGB", (g, g, g)), 0.035)
        # fade in/out per scene
        fade = 1.0
        if t < 0.28:
            fade = t / 0.28
        elif t > dur - 0.34:
            fade = max(0.0, (dur - t) / 0.34)
        if fade < 1.0:
            reg = Image.blend(Image.new("RGB", (W, H), BG), reg, fade)
        proc.stdin.write(reg.tobytes())

    proc.stdin.close()
    proc.wait()
    if proc.returncode != 0:
        print(proc.stderr.read().decode()[-2000:])
        sys.exit(1)

    # mux audio chunk: lead silences + vo + tail
    chunk = os.path.join(outdir, f"s{sid}-a.wav")
    subprocess.run([
        FF, "-y", "-loglevel", "error",
        "-f", "lavfi", "-t", f"{lead:.3f}", "-i", "anullsrc=r=48000:cl=stereo",
        "-i", vp,
        "-f", "lavfi", "-t", f"{tail:.3f}", "-i", "anullsrc=r=48000:cl=stereo",
        "-filter_complex", "[1:a]aformat=sample_rates=48000:channel_layouts=stereo[a1];"
                           "[0:a][a1][2:a]concat=n=3:v=0:a=1[out]",
        "-map", "[out]", "-c:a", "pcm_s16le", chunk,
    ], check=True)

    final = os.path.join(outdir, f"final{sid}.mp4")
    subprocess.run([
        FF, "-y", "-loglevel", "error", "-i", tmp, "-i", chunk,
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
        "-shortest", "-movflags", "+faststart", final,
    ], check=True)
    os.remove(tmp)
    os.remove(chunk)
    print(f"scene {sid}: {dur:.2f}s, {nfr} frames -> {final}")
    return final


if __name__ == "__main__":
    which = sys.argv[1:] or [str(i) for i in range(len(SCENES))]
    for a in which:
        build_scene(int(a))
