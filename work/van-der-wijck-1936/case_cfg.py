"""Konfigurasi kasus AK-EP04 — Kapal Van der Wijck 1936 (POV nelayan Brondong).

Narasi memakai VO PEMILIK dari Drive (folder van-der-wijck/vo, 108,30 s), bukan TTS
lokal: teks, jeda, dan penekanannya milik pemilik. Timestamp kata dari
`vo_owner/vo_alignment.json` (faster-whisper). Karena itu ada MERGE/WORD_FIX untuk
salah dengar ASR (mis. "di nihari" → dini hari, "Waik" → Wijck).

Tanpa gore, tanpa teori konspirasi. Footage stok Coverr/Mixkit, dilabeli di layar dan
dikreditkan di kartu akhir + deskripsi.
"""

SLUG = "van-der-wijck-1936"
VO_FILE = "vo_van-der-wijck.mp3"
END = 110.90
OUT_NAME = "AK-EP04_van-der-wijck-1936_short_v2.mp4"
SRT_NAME = "AK-EP04.id.srt"
BED_BUILDER = "bed_vdw.py"
CLIP_BG_BRIGHT = "-0.46"

IMAGES = {}

# work/van-der-wijck-1936/footage/: (berkas, detik mulai, durasi tersedia 6,00 s kecuali radio)
CLIPS = {
    "NIGHT1": ("night_ocean_aerial__coverr-view-of-the-harbor-8599.mp4", 0.20, 6.00),
    "OMBAK1": ("s1_ombak_malam.mp4", 0.30, 6.00),
    "OMBAK2": ("s1_ombak_malam.mp4", 1.50, 6.00),
    "KAPAL1": ("s5_kapal_laut.mp4", 0.30, 6.00),
    "KAPALJAUH": ("s5_kapal_kejauhan.mp4", 0.40, 6.00),
    "DERMAGA": ("s8_dermaga.mp4", 0.30, 6.00),
    "RADIO1": ("m_radio_48533.mp4", 0.60, 11.00),
    "BATU": ("s6_ombak_batu.mp4", 0.40, 6.00),
    "OMBAKBESAR": ("s5_ombak_besar.mp4", 0.20, 6.00),
    "BATULAUT": ("s6_batu_laut.mp4", 0.40, 6.00),
    "AWAN1": ("s2_awan_dari_kabin.mp4", 0.30, 6.00),
    "AWAN2": ("s2_awan_dari_kabin.mp4", 1.60, 6.00),
    "PERAHU1": ("s5_perahu.mp4", 0.30, 6.00),
    "PERAHU2": ("s5_perahu.mp4", 1.50, 6.00),
    "PERAHU3": ("s5_perahu.mp4", 2.20, 6.00),
    "DARAT": ("s9_darat_di_laut.mp4", 0.40, 6.00),
    "LAUT2": ("s9_laut_luas.mp4", 0.60, 6.00),
    "LAUT2B": ("s9_laut_luas.mp4", 2.40, 6.00),
    "LANGIT": ("s2_langit_malam.mp4", 0.30, 6.00),
    "TULIS": ("hand_writing_letter__coverr-writing-a-note-4875.mp4", 1.00, 6.00),
    "KORAN": ("newspaper_printing__coverr-local-dutch-newspapers-8257.mp4", 0.50, 6.00),
    "PIHA": ("s6_piha.mp4", 0.40, 6.00),
    "MERC1": ("s5_mercusuar_badai.mp4", 1.90, 6.00),   # dalam rumah lampu
    "MERC2": ("s5_mercusuar_badai.mp4", 1.70, 6.00),
    "MERC3": ("s5_mercusuar_badai.mp4", 1.40, 6.00),
    "MERC4": ("s5_mercusuar_badai.mp4", 2.20, 6.00),
    "MERC_EXT": ("s5_mercusuar_badai.mp4", 0.05, 6.00),  # mercusuar di tebing (0–1,5 s)
    "BUKU": ("old_book_pages__coverr-flicking-through-bible-pages-3558.mp4", 0.50, 6.00),
}

TAG_STOK_C = "FOOTAGE STOK · COVERR"
TAG_STOK_M = "FOOTAGE STOK · MIXKIT FREE LICENSE"

BOX = {"box": (1020, 574)}
NIGHT = {"box": (1020, 574), "bg": "-0.66"}

# (mulai, selesai, klip, mode, z0, z1, opsi)
SHOTS = [
    (0.00,   1.30, None, "black", 1.00, 1.00, {}),
    (1.30,   5.30, "NIGHT1", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **NIGHT}),
    (5.30,  10.00, "OMBAK1", "clipfill", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (10.00, 13.80, "KAPAL1", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    (13.80, 17.80, "KAPALJAUH", "clipfill", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (17.80, 21.36, "DERMAGA", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    (21.36, 25.20, "RADIO1", "clip", 1.00, 1.00, {"tag": TAG_STOK_M, **NIGHT}),
    (25.20, 29.48, "BATU", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **NIGHT}),
    (29.48, 33.10, "OMBAKBESAR", "clipfill", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (33.10, 36.60, "BATULAUT", "clipfill", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (36.60, 39.68, "OMBAK2", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **NIGHT}),
    (39.68, 43.30, "AWAN1", "clipfill", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (43.30, 47.58, "AWAN2", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    (47.58, 51.40, "PERAHU1", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    (51.40, 55.20, "PERAHU2", "clipfill", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (55.20, 58.80, "PERAHU3", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    (58.80, 62.50, "DARAT", "clipfill", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (62.50, 67.80, "LAUT2", "clipfill", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (67.80, 71.50, "LANGIT", "clipfill", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (71.50, 74.80, "TULIS", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    (74.80, 78.18, "KORAN", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    (78.18, 82.20, "PIHA", "clipfill", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (82.20, 85.80, "MERC4", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **NIGHT}),
    (85.80, 90.02, "MERC2", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    (90.02, 94.20, "MERC3", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    (94.20, 96.64, None, "black", 1.00, 1.00, {}),
    (96.64, 98.10, "MERC_EXT", "clipfill", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (98.10, 101.90, "BUKU", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    (101.90, 104.80, "MERC1", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    (104.80, 108.30, "LAUT2B", "clipfill", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (108.30, 110.90, None, "black", 1.00, 1.00, {}),
]

KEYWORDS = {"1936", "SOS", "BRONDONG", "MERKUSUAR"}

NUM_PHRASES = [
    (["seratus", "empat", "puluh"], "140"),
    (["dua", "ratus", "enam", "puluh"], "260"),
    (["lima", "puluh"], "50"),
]

MERGE = [
    (["tiba", "-tiba"], "TIBA-TIBA"),
    (["di", "nihari"], "DINI HARI"),
    (["penulung", "-penulung"], "PENOLONG-PENOLONG"),
]

WORD_FIX = {
    "waik": "Wijck",
    "monument": "monumen",
    "kapten.": "kapten.",
}

CREDITS = ("Footage stok: Coverr · Mixkit Free License\\N"
           "Sumber: Wikipedia ID · detikJatim · merdeka · validnews\\N"
           "de Telegraaf 22 Okt 1936 · monumen Brondong\\N"
           "@oddchapter7 · KASUS NYATA · ARSIP ASLI")

OVL = [
    # ── hook
    (1.60, 5.10, "Kicker", "{\\pos(540,700)\\an5\\fs48\\fad(240,170)}YANG MENARIK MEREKA DARI LAUT"),
    # ── tanggal
    (10.30, 13.60, "Stamp", "{\\pos(540,520)\\an5\\fs80\\frz-4\\fad(160,150)}20 · 10 · 1936"),
    (18.00, 21.20, "Kicker", "{\\pos(540,1010)\\an5\\fs50\\fad(220,160)}SEKITAR 260 ORANG"),
    # ── SOS
    (22.40, 25.00, "Kicker", "{\\pos(540,700)\\an5\\fs52\\fad(200,150)}SINYAL TERAKHIR"),
    (25.30, 29.30, "Kicker", "{\\pos(540,1010)\\an5\\fs54\\c&H002A2AD8&\\fad(220,160)}TANPA POSISI"),
    # ── oleng + sekoci
    (33.30, 36.40, "Kicker", "{\\pos(540,1010)\\an5\\fs46\\fad(220,160)}SEKOCI TAK SEMPAT TURUN"),
    (40.00, 43.10, "Kicker", "{\\pos(540,1010)\\an5\\fs46\\fad(220,160)}DORNIER BERANGKAT SAAT FAJAR"),
    (44.10, 47.40, "Kicker", "{\\pos(540,1010)\\an5\\fs50\\fad(220,160)}HANYA SATU SEKOCI"),
    # ── nelayan
    (47.90, 51.20, "Kicker", "{\\pos(540,700)\\an5\\fs54\\fad(220,160)}BRONDONG · LAMONGAN"),
    (51.60, 55.00, "Kicker", "{\\pos(540,1010)\\an5\\fs46\\fad(220,160)}TANPA ATURAN RESMI"),
    (58.00, 60.30, "Big", "{\\pos(540,620)\\an5\\fs150\\c&H002A2AD8&\\fad(200,150)}140"),
    (60.35, 62.40, "Kicker", "{\\pos(540,860)\\an5\\fs44\\c&H00E0ECF0&\\fad(200,150)}ORANG DITARIK DARI AIR"),
    # ── kapten
    (62.90, 67.60, "Kicker", "{\\pos(540,1010)\\an5\\fs46\\fad(220,160)}KAPTEN · 6 JAM TERAPUNG"),
    # ── yang tak ditemukan
    (68.70, 71.40, "Kicker", "{\\pos(540,1010)\\an5\\fs44\\fad(220,160)}50 ORANG TAK PERNAH DITEMUKAN"),
    (75.00, 78.00, "Kicker", "{\\pos(540,1010)\\an5\\fs46\\fad(220,160)}BURUH PRIBUMI TANPA NAMA"),
    # ── perahu baru + mercusuar
    (78.50, 82.00, "Kicker", "{\\pos(540,1010)\\an5\\fs44\\fad(220,160)}SETAHUN KEMUDIAN · 9 PERAHU"),
    (90.30, 94.00, "Kicker", "{\\pos(540,1010)\\an5\\fs46\\fad(220,160)}PELAT BESI DI DINDINGNYA"),
    # ── tulisan di pelat
    (94.40, 96.55, "Kicker", "{\\pos(540,860)\\an5\\fs52\\c&H00E0ECF0&\\fad(240,120)}TANDA PERINGATAN\\NKEPADA PENOLONG-PENOLONG"),
    # ── penutup
    (96.85, 98.05, "Stamp", "{\\pos(540,520)\\an5\\fs64\\frz-4\\fad(140,120)}MERKUSUAR"),
    (98.25, 101.70, "Kicker", "{\\pos(540,1010)\\an5\\fs46\\fad(220,150)}BUKAN MONUMEN"),
    (102.20, 104.70, "Kicker", "{\\pos(540,1010)\\an5\\fs50\\fad(220,150)}NOVEL · FILM"),
    (105.10, 108.20, "Kicker", "{\\pos(540,900)\\an5\\fs44\\c&H00E0ECF0&\\fad(240,150)}@oddchapter7"),
    (108.60, 110.85, "Big", "{\\pos(540,640)\\an5\\fs110\\fad(260,0)}ODDCHAPTER"),
    (108.90, 110.85, "Kicker", "{\\pos(540,740)\\an5\\fs42\\c&H002A2AD8&\\fad(300,0)}KASUS NYATA · ARSIP ASLI"),
    (109.20, 110.85, "Credit", "{\\pos(540,1000)\\an5\\fs26\\c&H00D0D0D0&\\fad(360,0)}" + CREDITS),
]
