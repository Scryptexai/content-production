#!/usr/bin/env python3
"""Kartu bukti/editorial untuk OS-EP05 Piri Reis dan OS-EP06 Baghdad Battery.

Tidak menghasilkan gambar AI. Kartu Piri memakai scan dokumen asli PD; kartu
Baghdad memakai diagram modern CC BY-SA 2.5 dengan atribusi terbakar. Semua teks
ringkasan sengaja diberi label editorial agar tidak menyamar sebagai facsimile.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
W, H = 1080, 1920
INK = "#080A0C"; IVORY = "#F0ECE0"; ORANGE = "#C6602A"; SAGE = "#C6CEBE"; MUTED = "#9BA49A"
FONT_DIR = ROOT / "work" / "kutukan-tutankhamun" / "fonts"
ANTON = str(FONT_DIR / "Anton-Regular.ttf")
BARLOW = str(FONT_DIR / "BarlowCondensed-ExtraBold.ttf")


def f(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, font, width):
    out, line = [], ""
    for w in text.split():
        cand = (line + " " + w).strip()
        if draw.textbbox((0,0), cand, font=font)[2] <= width:
            line = cand
        else:
            if line: out.append(line)
            line = w
    if line: out.append(line)
    return out


def base():
    im = Image.new("RGB", (W,H), INK)
    d = ImageDraw.Draw(im)
    # panel/grain-like horizontal rules
    d.rectangle((0,0,W,14), fill=ORANGE)
    for y in range(170, H, 128):
        d.line((60,y,W-60,y), fill="#151B1C", width=1)
    d.text((70,75), "ODDCHAPTER SURPRISE", font=f(BARLOW,34), fill=ORANGE)
    return im, d


def title(d, text, y=195, size=112, fill=IVORY, maxw=920, gap=0):
    font=f(ANTON,size); lines=wrap(d,text,font,maxw)
    for line in lines:
        d.text((70,y),line,font=font,fill=fill,stroke_width=1,stroke_fill=INK)
        y += size + 6 + gap
    return y


def kicker(d, text, y):
    d.text((70,y), text, font=f(BARLOW,42), fill=ORANGE)
    return y + 60


def bullet(d, text, y, color=IVORY):
    font=f(BARLOW,50)
    lines=wrap(d,text,font,860)
    d.rectangle((72,y+17,88,y+33), fill=ORANGE)
    x=116
    for line in lines:
        d.text((x,y),line,font=font,fill=color)
        y += 56
    return y+22


def footer(d, text):
    font=f(BARLOW,29)
    lines=wrap(d,text,font,920)
    y=H-72-len(lines)*34
    d.rectangle((0,y-26,W,H), fill="#111719")
    for line in lines:
        d.text((70,y),line,font=font,fill=MUTED)
        y += 34


def source_card(src, dest, label, header, footer_text):
    im,d=base(); y=kicker(d,label,190); y=title(d,header,y,70,maxw=920)
    image=Image.open(src).convert("RGB")
    # neutral panel and real source image — no rewriting/retouching of document
    panel=Image.new("RGB",(940,1200),"#D4C5A2")
    scale=min(900/image.width,1140/image.height)
    image=image.resize((round(image.width*scale),round(image.height*scale)),Image.Resampling.LANCZOS)
    panel.paste(image,((940-image.width)//2,(1200-image.height)//2))
    im.paste(panel,(70,520))
    d=ImageDraw.Draw(im)
    d.rectangle((70,520,1010,1720),outline=ORANGE,width=4)
    footer(d,footer_text)
    im.save(dest,quality=96)


def piri_cards():
    out=ROOT/'work/piri-reis/img'; out.mkdir(parents=True,exist_ok=True)
    source_card(out/'piri_reis_map_source_pd.jpg',out/'piri_source_document.png',
                'DOKUMEN ASLI · 1513','PETA PIRI REIS',
                'Piri Reis World Map, 1513 · Topkapı Palace Museum Library H 1824 · via Wikimedia Commons · Public Domain')
    im,d=base(); y=kicker(d,'CATATAN DI PETA',210); y=title(d,'PETA INI DISUSUN DARI SUMBER LAIN',y,88)
    y=bullet(d,'Kira-kira dua puluh peta dan bagan',y+45)
    y=bullet(d,'Sumber Portugis dan Arab',y)
    y=bullet(d,'Satu peta Columbus disebut, tetapi sudah hilang',y)
    d.text((70,1430),'RINGKASAN EDITORIAL',font=f(BARLOW,32),fill=MUTED)
    d.text((70,1475),'DARI INSKRIPSI PADA DOKUMEN',font=f(BARLOW,32),fill=MUTED)
    footer(d,'Sumber: inskripsi Piri Reis, 1513 · Topkapı H 1824 · bukan facsimile teks')
    im.save(out/'piri_sources_card.png')
    im,d=base(); y=kicker(d,'UJI KLAIM VIRAL',210); y=title(d,'ANTARTIKA TANPA ES?',y,110); y=title(d,'TIDAK DIDUKUNG',y+28,112,ORANGE)
    y=bullet(d,'Garis selatan menyambung ke Amerika Selatan',y+70)
    y=bullet(d,'Bentuknya dipengaruhi kompilasi dan ruang kulit',y)
    y=bullet(d,'Kajian kartografi tidak mengidentifikasinya sebagai pantai Antartika',y)
    footer(d,'Verdict editorial berbasis McIntosh (2000) dan catatan sumber pada peta')
    im.save(out/'piri_verdict_card.png')
    im,d=base(); y=kicker(d,'BUKAN LOMPATAN TEKNOLOGI',210); y=title(d,'1513',y,210,ORANGE); d.text((70,y+10),'PETA PIRI REIS',font=f(BARLOW,56),fill=IVORY)
    d.line((70,y+150,1010,y+150),fill=IVORY,width=6); d.polygon([(990,y+132),(1030,y+150),(990,y+168)],fill=ORANGE)
    d.text((70,y+245),'1820',font=f(ANTON,210),fill=IVORY)
    d.text((70,y+455),'ANTARTIKA MASUK CATATAN',font=f(BARLOW,54),fill=IVORY)
    d.text((70,y+514),'PELAYARAN MODERN',font=f(BARLOW,54),fill=IVORY)
    footer(d,'Tanggal pembanding: catatan pelayaran modern · bukan klaim bahwa Piri “gagal”')
    im.save(out/'piri_timeline_card.png')


def baghdad_cards():
    out=ROOT/'work/baghdad-battery/img'; out.mkdir(parents=True,exist_ok=True)
    source_card(out/'baghdad_diagram_source_cc_by_sa.jpg',out/'baghdad_diagram_source.png',
                'SKEMA MODERN · BUKAN FOTO ARTEFAK','KENDI BAGHDAD',
                'Ironie, “Pile Bagdad” · Wikimedia Commons · CC BY-SA 2.5 · skema modern, bukan foto artefak')
    im,d=base(); y=kicker(d,'BAGIAN YANG BENAR-BENAR ADA',210); y=title(d,'EMPAT BAHAN',y,110)
    for a,b in [('KERAMIK','kendi'),('TEMBAGA','tabung'),('BESI','batang'),('ASPAL','sumbat')]:
        d.text((85,y),a,font=f(ANTON,92),fill=ORANGE); d.text((500,y+22),b.upper(),font=f(BARLOW,54),fill=IVORY); y+=150
    footer(d,'Berdasarkan deskripsi material artefak; diagram sumber dikreditkan pada shot lain')
    im.save(out/'baghdad_parts_card.png')
    im,d=base(); y=kicker(d,'BEDAKAN DUA KALIMAT',210); y=title(d,'REPLIKA BISA MEMBERI VOLTASE KECIL',y,90)
    y=title(d,'TIDAK SAMA DENGAN',y+100,76,MUTED); y=title(d,'FUNGSI ASLI TERBUKTI',y+10,98,ORANGE)
    y=bullet(d,'Replika membutuhkan elektrolit yang ditambahkan',y+100)
    y=bullet(d,'Uji kimia menunjukkan kemungkinan, bukan niat pembuatnya',y)
    footer(d,'Kartu inferensi editorial · bukan penyangkalan bahwa reaksi elektrokimia mungkin terjadi')
    im.save(out/'baghdad_verdict_card.png')
    im,d=base(); y=kicker(d,'KALAU INI BENAR-BENAR BATEREI',210); y=title(d,'JEJAK YANG KITA HARAPKAN',y,86)
    y=bullet(d,'Kabel atau penghubung',y+70)
    y=bullet(d,'Rangkaian beberapa kendi',y)
    y=bullet(d,'Artefak sezaman yang terbukti berlapis listrik',y)
    d.rectangle((70,1410,1010,1580),fill=ORANGE); d.text((112,1440),'BUKTI ITU BELUM ADA',font=f(ANTON,66),fill=INK)
    footer(d,'Batas bukti arkeologi · bukan verdict tentang semua kemungkinan fungsi benda')
    im.save(out/'baghdad_evidence_card.png')
    im,d=base(); y=kicker(d,'DOKUMEN HIPOTESIS',210); y=title(d,'1938',y,220,ORANGE)
    y=title(d,'WILHELM KÖNIG',y+35,92)
    d.text((70,y+75),'“EIN GALVANISCHES ELEMENT',font=f(BARLOW,48),fill=IVORY)
    d.text((70,y+130),'AUS DER PARTHERZEIT?”',font=f(BARLOW,48),fill=IVORY)
    d.text((70,y+220),'TANDA TANYA ITU PENTING:',font=f(BARLOW,42),fill=MUTED)
    y=bullet(d,'Ini hipotesis fungsi, bukan putusan fungsi',y+300)
    footer(d,'Forschungen und Fortschritte 14 (1938), 8–9 · kartu bibliografi editorial, bukan scan publikasi')
    im.save(out/'baghdad_koenig_card.png')


if __name__=='__main__':
    piri_cards(); baghdad_cards()
    print('cards written')
