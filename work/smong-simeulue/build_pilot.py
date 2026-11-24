#!/usr/bin/env python3
"""Build visual plates and timed ASS captions for AK-EP11 Smong Simeulue.

Every visual is either first-party information design or one of the two licensed
sources recorded in sources.md. No generic tsunami footage or generated people.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import json, math, random

CASE = Path(__file__).resolve().parent
IMG = CASE / "img"
W, H = 1080, 1920
NAVY = (5, 22, 34)
DEEP = (3, 14, 24)
IVORY = (239, 238, 230)
MUTED = (177, 194, 198)
RED = (216, 42, 42)
SEA = (14, 73, 98)

FONT = CASE / "fonts" / "BarlowCondensed-ExtraBold.ttf"
FONT_B = CASE / "fonts" / "BarlowCondensed-Bold.ttf"
FONT_A = CASE / "fonts" / "Anton-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(str(path), size)


def cover_bg(seed):
    random.seed(seed)
    im = Image.new("RGB", (W, H), NAVY)
    px = im.load()
    # Gentle deterministic texture, so data cards are not flat black.
    for y in range(H):
        base = int(13 * (1 - y / H))
        for x in range(W):
            n = random.randrange(-4, 5)
            px[x, y] = (max(0, 5 + base + n), max(0, 22 + base + n), max(0, 34 + base + n))
    d = ImageDraw.Draw(im, "RGBA")
    for i in range(28):
        y = 150 + i * 58 + (i % 3) * 7
        phase = i * 0.48
        pts = [(0, y)]
        for x in range(0, W + 32, 32):
            pts.append((x, y + int(math.sin(x / 92 + phase) * (7 + i % 3))))
        d.line(pts, fill=(86, 155, 171, 20), width=2)
    d.ellipse((-330, 860, 780, 1970), fill=(6, 57, 74, 95))
    d.ellipse((360, -520, 1550, 700), fill=(31, 72, 85, 42))
    return im


def title(d, kicker, headline, y=155, small=False):
    d.text((72, y), kicker, font=font(FONT_B, 34), fill=RED, spacing=2)
    size = 124 if not small else 96
    # Headline supports manual newlines.
    d.multiline_text((68, y + 52), headline, font=font(FONT_A, size), fill=IVORY,
                     spacing=4, stroke_width=0)


def footer(d, source):
    d.rectangle((60, 1772, 1020, 1840), fill=(0, 0, 0, 135))
    d.text((84, 1792), source, font=font(FONT_B, 26), fill=(202, 213, 214))
    d.text((84, 1846), "ODDCHAPTER  ·  KASUS NYATA", font=font(FONT_B, 24), fill=(119, 146, 153))


def save(im, name):
    im.save(IMG / name, quality=95)


def plate_sea():
    im = cover_bg(1)
    d = ImageDraw.Draw(im, "RGBA")
    # concentric water ripples; intentionally symbolic and not claimed as event footage
    for r in range(90, 1300, 92):
        box=(W//2-r, 1030-r//3, W//2+r, 1030+r//3)
        d.ellipse(box, outline=(72, 160, 179, max(12, 70-r//22)), width=4)
    d.rectangle((0, 1080, W, H), fill=(1, 18, 29, 42))
    title(d, "SIMEULUE · ACEH", "SAAT LAUT\nSURUT", y=188)
    d.text((72, 565), "warga tidak menunggu", font=font(FONT_B, 56), fill=MUTED)
    d.text((72, 630), "peringatan resmi", font=font(FONT_B, 56), fill=MUTED)
    d.rounded_rectangle((72, 748, 580, 836), radius=18, fill=RED)
    d.text((100, 770), "JANGAN TUNGGU", font=font(FONT_B, 38), fill=IVORY)
    footer(d, "ILUSTRASI DATA · BUKAN REKAMAN KEJADIAN")
    save(im, "01_laut_surut.png")


def map_card(highlight=False, label="SIMEULUE · ACEH", source="PETA: SADALMELIK · CC BY-SA 3.0"):
    im = cover_bg(2 if not highlight else 5)
    d = ImageDraw.Draw(im, "RGBA")
    title(d, "PULAU DI BARAT ACEH", label, y=120, small=True)
    raw = Image.open(IMG / "simeulue_topography_cc-by-sa-3.png").convert("RGB")
    # Preserve all map context; rest on an ivory card.
    card = Image.new("RGB", (930, 827), IVORY)
    m = raw.resize((850, 755), Image.Resampling.LANCZOS)
    card.paste(m, (40, 36))
    im.paste(card, (75, 468))
    d.rounded_rectangle((75,468,1005,1295),radius=22,outline=(239,238,230,255),width=5)
    if highlight:
        # Langi coordinates: 2.808°N, 95.772°E. Map plotting frame approx x=33…327, y=0…278.
        x_raw = 33 + (95.772 - 95.5) * 294
        y_raw = (3.0 - 2.808) * 278
        x, y = 75 + 40 + int(x_raw / 330 * 850), 468 + 36 + int(y_raw / 293 * 755)
        # Correct for input bounds and resized map: deliberate approximate locator only.
        d.ellipse((x-30,y-30,x+30,y+30), fill=RED, outline=IVORY, width=5)
        d.line((x+24,y-20,x+165,y-97), fill=RED, width=7)
        d.rounded_rectangle((x+150,y-137,x+396,y-66), radius=14, fill=RED)
        d.text((x+173,y-124), "LANGI", font=font(FONT_B, 43), fill=IVORY)
    footer(d, source)
    return im


def plate_map():
    save(map_card(), "02_simeulue_map.png")


def plate_rule():
    im = cover_bg(3)
    d = ImageDraw.Draw(im, "RGBA")
    title(d, "SMONG", "SATU URUTAN\nYANG DIINGAT", y=152, small=True)
    steps=[("1", "GEMPA KUAT"), ("2", "LAUT SURUT"), ("3", "KE BUKIT")]
    y=590
    for n, text in steps:
        d.rounded_rectangle((78,y,1002,y+190),radius=28,fill=(17,51,64,232),outline=(83,138,150,100),width=3)
        d.ellipse((112,y+38,226,y+152),fill=RED)
        d.text((149,y+52),n,font=font(FONT_A,56),fill=IVORY)
        d.text((272,y+54),text,font=font(FONT_A,72),fill=IVORY)
        if n != "3":
            d.polygon([(517,y+213),(564,y+213),(540,y+264)], fill=RED)
        y += 284
    footer(d, "PENGETAHUAN TURUN-TEMURUN · UNESCO 2026")
    save(im, "03_urutan_smong.png")


def plate_noaa():
    im = cover_bg(8).convert("RGBA")
    d = ImageDraw.Draw(im, "RGBA")
    title(d, "26 DESEMBER 2004", "GELOMBANG\nMENYEBAR", y=132, small=True)
    gif = Image.open(IMG / "noaa_2004_tsunami_pd.gif").convert("RGBA")
    gif.thumbnail((720, 760), Image.Resampling.LANCZOS)
    card = Image.new("RGBA", (820, 910), (239, 238, 230, 255))
    card.alpha_composite(gif, ((820 - gif.width) // 2, 75))
    ImageDraw.Draw(card, "RGBA").rectangle((0, 780, 820, 910), fill=(4, 22, 34, 255))
    ImageDraw.Draw(card).text((44, 810), "SIMULASI GELOMBANG · SUMATRA", font=font(FONT_B, 36), fill=IVORY)
    im.alpha_composite(card, (130, 500))
    d = ImageDraw.Draw(im, "RGBA")
    d.text((132, 1470), "LANGI: < 10 MENIT SETELAH GUNCANGAN BERHENTI", font=font(FONT_B, 40), fill=IVORY)
    footer(d, "ANIMASI: NOAA CENTER FOR TSUNAMI RESEARCH · PUBLIC DOMAIN")
    save(im.convert("RGB"), "05_noaa_tsunami.png")


def plate_time():
    im = cover_bg(4)
    d = ImageDraw.Draw(im, "RGBA")
    title(d, "26 DESEMBER 2004", "WAKTUNYA\nKURANG DARI", y=160, small=True)
    d.text((70, 550), "10", font=font(FONT_A,390), fill=RED)
    d.text((560, 728), "MENIT", font=font(FONT_A,118), fill=IVORY)
    d.line((82,1045,998,1045),fill=(126,177,186,120),width=4)
    d.text((76,1100), "guncangan berhenti",font=font(FONT_B,54),fill=MUTED)
    d.text((76,1170), "gelombang mencapai Langi",font=font(FONT_B,54),fill=IVORY)
    d.text((76,1288), "< 10 menit",font=font(FONT_A,102),fill=IVORY)
    footer(d, "DATA LANGI · MCADOO DKK., 2006 / NOAA PMEL")
    save(im,"04_kurang_dari_10_menit.png")


def plate_langi():
    im = map_card(highlight=True, label="LANGI · UTARA SIMEULUE", source="PETA: SADALMELIK · CC BY-SA 3.0 · DATA: MCADOO DKK. 2006")
    d=ImageDraw.Draw(im,"RGBA")
    d.rounded_rectangle((73,1325,1007,1640),radius=28,fill=(4,18,28,238),outline=(216,42,42,190),width=3)
    d.text((108,1370),"DESANYA HANCUR.",font=font(FONT_B,56),fill=MUTED)
    d.text((106,1442),"SEKITAR",font=font(FONT_B,46),fill=IVORY)
    d.text((105,1480),"800",font=font(FONT_A,152),fill=RED)
    d.text((490,1522),"WARGA\nSELAMAT",font=font(FONT_A,84),fill=IVORY,spacing=-6)
    save(im,"05_langi_800_selamat.png")


def plate_memory():
    im=cover_bg(6)
    d=ImageDraw.Draw(im,"RGBA")
    title(d,"BUKAN MENEBak LAUT", "MEREKA\nMENGINGAT", y=160,small=True)
    d.rounded_rectangle((70,640,1010,1190),radius=38,fill=(9,47,60,206),outline=(105,165,174,110),width=4)
    d.text((155,700),"CERITA",font=font(FONT_A,108),fill=IVORY)
    d.text((155,840),"→",font=font(FONT_A,135),fill=RED)
    d.text((360,850),"TINDAKAN",font=font(FONT_A,90),fill=IVORY)
    d.text((155,1030),"SMONG",font=font(FONT_A,112),fill=RED)
    footer(d,"SMONG · CERITA DAN SYAIR ANTARGENERASI")
    save(im,"06_ingat_bertindak.png")


def plate_question():
    im=cover_bg(7)
    d=ImageDraw.Draw(im,"RGBA")
    # a rising ridge graphic, symbolic only
    d.polygon([(0,1520),(0,1420),(180,1320),(350,1390),(530,1190),(760,1280),(1080,1060),(1080,1920),(0,1920)],fill=(9,62,68,250))
    title(d,"PERTANYAAN TERAKHIR", "SIAPA YANG\nMENGAJARKAN\nTANDA BAHAYA?", y=190,small=True)
    d.text((76,1370),"TULIS DI KOMENTAR",font=font(FONT_B,42),fill=RED)
    d.text((76,1430),"pengetahuan yang kita ingat bisa jadi tindakan.",font=font(FONT_B,42),fill=IVORY)
    footer(d,"SUMBER: NOAA PMEL · UNESCO · BMKG")
    save(im,"07_pertanyaan.png")


def write_ass():
    # timings represent exact outputs of separately synthesized voice segments,
    # joined with 100 ms gaps. Captions are sentence-level—not projected word timing.
    timings = [
        (0.000,4.229,"SAAT LAUT SURUT, WARGA PULAU INI TIDAK MENUNGGU PERINGATAN RESMI."),
        (4.329,8.272,"DI SIMEULUE, MEREKA MEWARISI SATU KATA: SMONG."),
        (8.372,13.103,"PESAN ITU HIDUP DALAM CERITA DAN SYAIR, DARI GENERASI KE GENERASI."),
        (13.203,17.642,"ARTINYA: SETELAH GEMPA KUAT DAN LAUT SURUT, LARI KE TEMPAT TINGGI."),
        (17.742,24.192,"PADA 26 DESEMBER 2004, GELOMBANG MENCAPAI LANGI KURANG DARI SEPULUH MENIT SETELAH GUNCANGAN BERHENTI."),
        (24.292,28.400,"DESANYA HANCUR. TAPI SEKITAR DELAPAN RATUS WARGANYA SELAMAT."),
        (28.500,32.248,"MEREKA TIDAK MENEBAK LAUT. MEREKA MENGINGAT CERITA LELUHUR."),
        (32.348,35.490,"DI RUMAHMU, SIAPA YANG MENGAJARKAN TANDA BAHAYA?"),
    ]
    def t(s):
        m, sec = divmod(s, 60)
        return f"0:{int(m):02d}:{sec:05.2f}"
    head="""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Sub,Barlow Condensed ExtraBold,78,&H00FFFFFF,&H00FFFFFF,&H00131C21,&H9A131C21,0,0,0,0,100,100,2,0,1,8,3,2,54,54,398,1

[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
"""
    lines=[]
    for a,b,tx in timings:
        clean=tx.replace("\\N"," ")
        lines.append(f"Dialogue: 5,{t(a)},{t(b)},Sub,,0,0,0,,{{\\fscx112\\fscy112\\t(0,90,\\fscx100\\fscy100)}}{clean}")
    (CASE/"subs.ass").write_text(head+"\n".join(lines)+"\n")
    srt=[]
    for i,(a,b,tx) in enumerate(timings,1):
        def ts(x):
            h=int(x//3600); m=int(x%3600//60); sec=x%60
            return f"{h:02d}:{m:02d}:{sec:06.3f}".replace('.',',')
        srt.append(f"{i}\n{ts(a)} --> {ts(b)}\n{tx}\n")
    (CASE/"AK-EP11.id.srt").write_text("\n".join(srt))
    (CASE/"caption_timing.json").write_text(json.dumps([{"start":a,"end":b,"text":x} for a,b,x in timings],ensure_ascii=False,indent=2)+"\n")


def main():
    (CASE/"fonts").mkdir(exist_ok=True)
    plate_sea(); plate_map(); plate_rule(); plate_noaa(); plate_time(); plate_langi(); plate_memory(); plate_question(); write_ass()

if __name__ == "__main__":
    main()
