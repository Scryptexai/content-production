"""Konfigurasi kasus AK-EP04 — Kapal Van der Wijck 1936 (POV lima nelayan Brondong).

Sumber: work/van-der-wijck-1936/{fakta.md,naskah.md,shotlist.md}. Tanpa gore, tanpa
teori konspirasi, angka korban yang berbeda antar sumber disajikan sebagai perdebatan
(bukan dipilih diam-diam). Footage hanya stok Coverr/Mixkit — dilabeli di layar dan
dikreditkan di kartu akhir + deskripsi.
"""

SLUG = "van-der-wijck-1936"
VO_FILE = "vo_van-der-wijck.mp3"
END = 95.70
OUT_NAME = "AK-EP04_van-der-wijck-1936_short_v1.mp4"
SRT_NAME = "AK-EP04.id.srt"
BED_BUILDER = "bed_vdw.py"
CLIP_BG_BRIGHT = "-0.46"

IMAGES = {}

# klip di work/van-der-wijck-1936/footage/: (berkas, detik mulai, durasi tersedia)
# semua footage Coverr 6,00 s → durasi shot harus <= 6,00 - mulai
CLIPS = {
    "NIGHT1": ("night_ocean_aerial__coverr-view-of-the-harbor-8599.mp4", 0.20, 6.00),
    "OMBAK1": ("s1_ombak_malam.mp4", 0.30, 6.00),
    "OMBAK2": ("s1_ombak_malam.mp4", 1.50, 6.00),
    "KAPAL1": ("s5_kapal_laut.mp4", 0.30, 6.00),
    "KAPAL2": ("s5_kapal_laut.mp4", 1.70, 6.00),
    "KAPALJAUH": ("s5_kapal_kejauhan.mp4", 0.40, 6.00),
    "KAPALJAUH2": ("s5_kapal_kejauhan.mp4", 1.20, 6.00),
    "DERMAGA": ("s8_dermaga.mp4", 0.30, 6.00),
    "OMBAKBESAR": ("s5_ombak_besar.mp4", 0.20, 6.00),
    "BATU": ("s6_ombak_batu.mp4", 0.40, 6.00),
    "BATULAUT": ("s6_batu_laut.mp4", 0.40, 6.00),
    "LAUTLUAS": ("s9_laut_luas.mp4", 0.15, 6.00),
    "PERAHU1": ("s5_perahu.mp4", 0.30, 6.00),
    "PERAHU2": ("s5_perahu.mp4", 1.50, 6.00),
    "PERAHU3": ("s5_perahu.mp4", 2.40, 6.00),
    "PERAHU4": ("s5_perahu.mp4", 3.00, 6.00),
    "AWAN1": ("s2_awan_dari_kabin.mp4", 0.30, 6.00),
    "AWAN2": ("s2_awan_dari_kabin.mp4", 2.30, 6.00),
    "RADIO1": ("m_radio_48533.mp4", 0.60, 11.00),
    "LAUT2": ("s9_laut_luas.mp4", 0.80, 6.00),
    "LANGIT": ("s2_langit_malam.mp4", 0.30, 6.00),
    "PIHA": ("s6_piha.mp4", 0.40, 6.00),
    "DARAT": ("s9_darat_di_laut.mp4", 0.40, 6.00),
}

TAG_STOK_C = "FOOTAGE STOK · COVERR"
TAG_STOK_M = "FOOTAGE STOK · MIXKIT FREE LICENSE"

BOX = {"box": (1020, 574)}          # jendela 16:9 di atas latar blur
NIGHT = {"box": (1020, 574), "bg": "-0.66"}

# (mulai, selesai, klip, mode, z0, z1, opsi)
SHOTS = [
    (0.00,   1.30, None, "black", 1.00, 1.00, {}),
    (1.30,   5.35, "NIGHT1", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **NIGHT}),
    (5.35,   9.60, "OMBAK1", "clipfill", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (9.60,  13.60, "KAPAL1", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    (13.60, 17.85, "KAPALJAUH", "clipfill", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (17.85, 21.55, "DERMAGA", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    (21.55, 24.80, "KAPAL2", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **NIGHT}),
    (24.80, 28.90, "OMBAKBESAR", "clipfill", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (28.90, 32.20, "BATU", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **NIGHT}),
    (32.20, 36.40, "OMBAK2", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **NIGHT}),
    (36.40, 39.70, "BATULAUT", "clipfill", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (39.70, 44.70, "LAUTLUAS", "clipfill", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (44.70, 49.10, "PERAHU1", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    (49.10, 53.30, "PERAHU2", "clipfill", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (53.30, 56.70, "PERAHU3", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    (56.70, 60.30, "AWAN1", "clipfill", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (60.30, 63.10, "AWAN2", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    (63.10, 67.20, "RADIO1", "clip", 1.00, 1.00, {"tag": TAG_STOK_M, **NIGHT}),
    (67.20, 71.85, "KAPALJAUH2", "clipfill", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (71.85, 76.20, "LANGIT", "clipfill", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (76.20, 81.30, "LAUT2", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    (81.30, 85.90, "PIHA", "clipfill", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (85.90, 90.40, "DARAT", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    (90.40, 93.33, "PERAHU4", "clipfill", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (93.33, 95.70, None, "black", 1.00, 1.00, {}),
]

KEYWORDS = {"1936", "BRONDONG", "WIJCK", "UYTERMERK", "KASLIBIN"}

NUM_PHRASES = [
    (["seratus", "lima", "puluh"], "150"),
    (["seratus", "empat", "puluh", "lima"], "145"),
    (["lima", "puluh", "tiga"], "53"),
    (["tiga", "puluh", "dua"], "32"),
    (["dua", "puluh", "dua"], "22"),
    (["dua", "puluh", "satu"], "21"),
    (["tujuh", "belas"], "17"),
    (["dua", "belas"], "12"),
    (["empat", "puluh", "dua"], "42"),
    (["lima", "puluh", "delapan"], "58"),
    (["tujuh", "puluh", "lima"], "75"),
    (["dua", "puluh", "delapan"], "28"),
]

MERGE = [
    (["perahu", "-perahu"], "PERAHU-PERAHU"),
]

WORD_FIX = {
    "uytermerk,": "Uytermerk,",
}

CREDITS = ("Footage stok: Coverr · Mixkit Free License\\N"
           "Sumber: Wikipedia ID · detikJatim · merdeka.com · validnews\\N"
           "Angka korban: de Telegraaf 22 Okt 1936 & sumber lain berbeda\\N"
           "@oddchapter7 · KASUS NYATA · ARSIP ASLI")

OVL = [
    # ── hook
    (1.55, 4.30, "Kicker", "{\\pos(540,700)\\an5\\fs56\\fad(240,170)}19 OKTOBER 1936"),
    (5.50, 9.30, "Kicker", "{\\pos(540,1010)\\an5\\fs50\\fad(220,160)}LAUT JAWA"),
    # ── nama kapal
    (9.90, 13.30, "Stamp", "{\\pos(540,520)\\an5\\fs78\\frz-4\\fad(160,150)}VAN DER WIJCK"),
    (10.20, 13.30, "Kicker", "{\\pos(540,650)\\an5\\fs46\\fad(240,150)}KPM · \"DE MEEUW\""),
    # ── pelayaran
    (18.05, 21.30, "Kicker", "{\\pos(540,1010)\\an5\\fs52\\fad(220,160)}SURABAYA → SEMARANG"),
    # ── 12 mil
    (25.10, 28.70, "Stamp", "{\\pos(540,520)\\an5\\fs96\\frz-5\\fad(160,150)}12 MIL"),
    (25.40, 28.70, "Kicker", "{\\pos(540,650)\\an5\\fs46\\fad(240,150)}DARI BRONDONG"),
    # ── enam menit
    (32.55, 36.20, "Big", "{\\pos(540,620)\\an5\\fs210\\c&H002A2AD8&\\fad(200,160)}6 MENIT"),
    (33.00, 36.20, "Kicker", "{\\pos(540,830)\\an5\\fs44\\c&H00E0ECF0&\\fad(240,160)}MENURUT KORAN 1936"),
    # ── tak ada kapal besar
    (39.95, 44.50, "Kicker", "{\\pos(540,1010)\\an5\\fs50\\fad(240,170)}TIDAK ADA KAPAL BESAR"),
    # ── lima nelayan
    (45.05, 49.00, "Kicker", "{\\pos(540,560)\\an5\\fs60\\fad(220,160)}5 NELAYAN · 145 ORANG"),
    (49.35, 53.10, "Kicker", "{\\pos(540,1010)\\an5\\fs30\\fad(240,160)}KASLIBIN · MODWIE · TROENOREDJO · SRATIT · MARDJIKI"),
    # ── pesawat
    (56.95, 60.10, "Kicker", "{\\pos(540,1010)\\an5\\fs52\\fad(220,160)}8 PESAWAT DORNIER"),
    # ── nakhoda & operator radio
    (63.40, 67.00, "Kicker", "{\\pos(540,1010)\\an5\\fs52\\fad(220,160)}NAKHODA SELAMAT"),
    (67.45, 71.60, "Kicker", "{\\pos(540,1010)\\an5\\fs44\\fad(220,160)}UYTERMERK · OPERATOR RADIO"),
    # ── angka yang tidak bulat
    (72.25, 76.00, "Big", "{\\pos(540,600)\\an5\\fs130\\fad(200,160)}42 · 58 · 75"),
    (72.60, 76.00, "Kicker", "{\\pos(540,780)\\an5\\fs40\\fad(240,160)}HILANG · TEWAS · HILANG"),
    # ── 2021
    (81.65, 85.70, "Stamp", "{\\pos(540,520)\\an5\\fs88\\frz-4\\fad(160,150)}28 METER"),
    (81.95, 85.70, "Kicker", "{\\pos(540,650)\\an5\\fs42\\fad(240,150)}BANGKAI DITEMUKAN 2021"),
    (86.10, 90.20, "Kicker", "{\\pos(540,900)\\an5\\fs48\\fad(220,160)}PERAHU KAYU DATANG LEBIH DULU"),
    # ── penutup
    (90.60, 93.25, "Kicker", "{\\pos(540,1010)\\an5\\fs46\\c&H00E0ECF0&\\fad(220,150)}@oddchapter7"),
    (93.55, 95.60, "Big", "{\\pos(540,640)\\an5\\fs110\\fad(260,0)}ODDCHAPTER"),
    (93.85, 95.60, "Kicker", "{\\pos(540,740)\\an5\\fs42\\c&H002A2AD8&\\fad(300,0)}KASUS NYATA · ARSIP ASLI"),
    (94.15, 95.60, "Credit", "{\\pos(540,1000)\\an5\\fs26\\c&H00D0D0D0&\\fad(360,0)}" + CREDITS),
]
