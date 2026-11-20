"""Konfigurasi kasus AK-EP05 — "Batas Terakhir Manusia" (Andes 1972, uji format 00F).

VO = TTS internal voice-05, 8 klip beat (naskah 02_SCRIPT/AK-EP05_andes-1972.md —
revisi total sudut pandang: dilema batin penonton, bukan laporan kronologis).
Durasi VO 87,31 s; END 91,40 s (kartu penutup 4,1 s). Waktu kata dari build_vo.py.

Format: 8 beat adaptasi — tantangan langsung (B1) → reaksi alami (B2) → patahan
keyakinan (B3) → pertaruhan nyawa (B4) → tekanan situasi (B5) → perjanjian moral
(B6) → payoff (B7) → debat komentar (B8).

Tanpa gore, tanpa kondisi jenazah, tanpa detail prosedur. Footage stok Coverr,
dilabeli di layar + dikreditkan di kartu akhir dan deskripsi.
"""

SLUG = "andes-1972"
VO_FILE = "vo_andes.mp3"
END = 91.40
OUT_NAME = "AK-EP05_andes-1972_short.mp4"
SRT_NAME = "AK-EP05.id.srt"
BED_BUILDER = "bed_andes.py"
CLIP_BG_BRIGHT = "-0.46"

IMAGES = {}

# work/andes-1972/footage/ (symlink ke footage/andes-1972): (berkas, detik mulai, durasi tersedia 6,00 s)
CLIPS = {
    "GUNUNG_SNOW":   ("gunung_snow.mp4",        0.50, 6.00),
    "GUNUNG_SNOW2":  ("gunung_snow.mp4",        1.20, 6.00),
    "SALJU_HUTAN":   ("salju_hutan.mp4",        0.60, 6.00),
    "HUTAN_DINGIN":  ("hutan_dingin.mp4",       0.50, 6.00),
    "HUTAN_DINGIN2": ("hutan_dingin.mp4",       1.40, 6.00),
    "SISA_SALJU":    ("sisa_salju.mp4",         0.40, 6.00),
    "SISA_SALJU2":   ("sisa_salju.mp4",         2.50, 6.00),
    "GUNUNG_KABUT":  ("gunung_kabut.mp4",       0.30, 6.00),
    "GUNUNG_KABUT2": ("gunung_kabut.mp4",       0.80, 6.00),
    "GUNUNG_KABUT3": ("gunung_kabut.mp4",       1.00, 6.00),
    "GUNUNG_KABUT4": ("gunung_kabut.mp4",       0.60, 6.00),
    "LILIN_GELAP":   ("lilin_gelap.mp4",        0.50, 6.00),
    "LILIN_GELAP2":  ("lilin_gelap.mp4",        1.50, 6.00),
    "API_GELAP":     ("api_gelap.mp4",          1.50, 6.00),
    "API_GELAP2":    ("api_gelap.mp4",          1.20, 6.00),
    "API_GELAP3":    ("api_gelap.mp4",          0.40, 6.00),
    "TENDA_DINGIN":  ("tenda_dingin.mp4",       0.60, 6.00),
    "TENDA_DINGIN2": ("tenda_dingin.mp4",       1.40, 6.00),
    "SALIB_GUNUNG":  ("salib_gunung.mp4",       0.50, 6.00),
    "SALIB_GUNUNG2": ("salib_gunung.mp4",       1.50, 6.00),
    "PESAWAT_AWAN":  ("pesawat_awan.mp4",       0.50, 6.00),
    "NAIK_PESAWAT":  ("naik_pesawat.mp4",       0.50, 6.00),
    "PESAWAT_GUNUNG": ("pesawat_gunung.mp4",    0.60, 6.00),
    "GUNUNG_SALJU":  ("gunung_salju.mp4",       0.50, 6.00),
    "GUNUNG_SALJU2": ("gunung_salju.mp4",       1.30, 6.00),
    "JENDELA_PESAWAT": ("jendela_pesawat.mp4",  0.80, 6.00),
    "JENDELA_PESAWAT2": ("jendela_pesawat.mp4", 1.50, 6.00),
    "HUTAN_SALJU":   ("hutan_salju.mp4",        0.50, 6.00),
    "TREK_MOUNTAIN": ("trek_mountain.mp4",      0.50, 6.00),
    "TREK_MOUNTAIN2": ("trek_mountain.mp4",     1.30, 6.00),
    "PUNCAK_JALAN":  ("puncak_jalan.mp4",       0.60, 6.00),
    "LEMBAH_AERIAL": ("lembah_aerial.mp4",      0.70, 6.00),
    "PESAWAT_PENCARI": ("pesawat_pencari.mp4",  0.60, 6.00),
    "PESAWAT_PENCARI2": ("pesawat_pencari.mp4", 1.50, 6.00),
    "ARGENTINA_VALLEY": ("argentina_valley.mp4", 0.60, 6.00),
    "LEMBAH":        ("lembah.mp4",             0.70, 6.00),
    "ARGENTINA_TIERRA": ("argentina_tierra.mp4", 0.80, 6.00),
    "KORAN":         ("koran.mp4",              0.50, 6.00),
}

TAG_STOK_C = "FOOTAGE STOK · COVERR"

BOX = {"box": (1020, 574)}
NIGHT = {"box": (1020, 574), "bg": "-0.66"}

# (mulai, selesai, klip, mode, z0, z1, opsi)
SHOTS = [
    # ── B1 tantangan langsung (0,00–4,65)
    (0.00,    0.80, None, "black", 1.00, 1.00, {}),
    (0.80,    4.65, "GUNUNG_SNOW", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    # ── B2 reaksi alami (4,65–10,75)
    (4.65,    7.70, "NAIK_PESAWAT", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    (7.70,   10.75, "JENDELA_PESAWAT", "clipfill", 1.00, 1.00, {"tag": TAG_STOK_C}),
    # ── B3 patahan keyakinan: radio (10,75–15,72)
    (10.75,  13.20, "KORAN", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    (13.20,  15.72, "PESAWAT_PENCARI", "clipfill", 1.00, 1.00, {"tag": TAG_STOK_C}),
    # ── B4 pertaruhan nyawa (15,72–25,38)
    (15.72,  20.50, "LILIN_GELAP", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **NIGHT}),
    (20.50,  25.38, "GUNUNG_KABUT", "clipfill", 1.00, 1.00, {"tag": TAG_STOK_C}),
    # ── B5 tekanan situasi (25,38–51,30)
    (25.38,  29.60, "HUTAN_DINGIN", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    (29.60,  33.90, "SISA_SALJU", "clipfill", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (33.90,  38.30, "API_GELAP", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **NIGHT}),
    (38.30,  42.50, "TENDA_DINGIN", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    (42.50,  46.80, "GUNUNG_KABUT2", "clipfill", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (46.80,  51.30, "LILIN_GELAP2", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **NIGHT}),
    # ── B6 perjanjian moral (51,30–64,71)
    (51.30,  55.90, "SALIB_GUNUNG", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    (55.90,  60.30, "JENDELA_PESAWAT2", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    (60.30,  64.71, "SALIB_GUNUNG2", "clipfill", 1.00, 1.00, {"tag": TAG_STOK_C}),
    # ── B7 payoff: berjalan keluar & pulang (64,71–74,68)
    (64.71,  68.10, "TREK_MOUNTAIN", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    (68.10,  71.40, "PUNCAK_JALAN", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    (71.40,  74.68, "PESAWAT_PENCARI2", "clipfill", 1.00, 1.00, {"tag": TAG_STOK_C}),
    # ── B8 debat komentar (74,68–87,31)
    (74.68,  79.00, "GUNUNG_KABUT4", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    (79.00,  83.20, "API_GELAP3", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **NIGHT}),
    (83.20,  87.31, "GUNUNG_SNOW2", "clipfill", 1.00, 1.00, {"tag": TAG_STOK_C}),
    # ── kartu penutup (87,31–91,40)
    (87.31,  91.40, None, "black", 1.00, 1.00, {}),
]

KEYWORDS = {"ANDES", "72", "16", "30"}

# angka dieja di VO -> digit di caption; urutan frasa panjang dulu untuk potongan tumpang tindih
NUM_PHRASES = [
    (["seribu", "sembilan", "ratus", "tujuh", "puluh", "dua"], "1972"),
    (["tiga", "puluh", "tiga"], "33"),
    (["dua", "puluh", "sembilan"], "29"),
    (["dua", "puluh", "dua"], "22"),
    (["empat", "puluh", "lima"], "45"),
    (["tujuh", "puluh", "dua"], "72"),
    (["tiga", "puluh"], "30"),
    (["enam", "belas"], "16"),
    (["kesebelas"], "KE-11"),
]

MERGE = []
WORD_FIX = {}

CREDITS = ("Footage stok: Coverr\\N"
           "Sumber: Wikipedia · Britannica\\N"
           "Piers Paul Read, Alive (1974) · Nando Parrado\\N"
           "Pablo Vierci, La Sociedad de la Nieve\\N"
           "@oddchapter7 · KASUS NYATA · ARSIP ASLI")

OVL = [
    # ── B1 tantangan langsung
    (1.20,    4.50, "Kicker", "{\\pos(540,700)\\an5\\fs56\\fad(240,170)}KAPAN NURANI MANUSIA MENYERAH?"),
    # ── B2 reaksi alami
    (5.00,    7.60, "Kicker", "{\\pos(540,1010)\\an5\\fs46\\fad(220,160)}MEMILIH MATI DARIPADA MENYENTUH SAHABAT"),
    # ── B3 patahan keyakinan
    (11.00,  15.50, "Stamp", "{\\pos(540,500)\\an5\\fs60\\frz-4\\fad(160,150)}HARI KE-11:\\NOPERASI SAR RESMI DIHENTIKAN"),
    # ── B4 pertaruhan nyawa
    (16.10,  20.30, "Kicker", "{\\pos(540,1010)\\an5\\fs48\\fad(220,160)}TIDAK ADA PAHLAWAN YANG DATANG"),
    (21.00,  25.20, "Kicker", "{\\pos(540,1010)\\an5\\fs46\\fad(220,160)}MENYERAH, ATAU YANG TAK TERBAYANGKAN"),
    # ── B5 tekanan situasi
    (25.80,  29.40, "Stamp", "{\\pos(540,520)\\an5\\fs64\\frz-4\\fad(160,150)}SUHU MINUS 30°"),
    (30.00,  33.70, "Kicker", "{\\pos(540,1010)\\an5\\fs46\\fad(220,160)}TUBUH MEMAKAN LEMAKNYA SENDIRI"),
    (34.30,  38.10, "Kicker", "{\\pos(540,1010)\\an5\\fs46\\fad(220,160)}TERAWETKAN SEMPURNA OLEH ES"),
    (38.80,  42.30, "Kicker", "{\\pos(540,700)\\an5\\fs48\\fad(220,160)}PERDEBATAN PALING SUNYI"),
    (43.00,  46.60, "Kicker", "{\\pos(540,1010)\\an5\\fs46\\fad(220,160)}SEBAGIAN MENOLAK · TAKUT DOSA"),
    (47.10,  51.10, "Kicker", "{\\pos(540,1010)\\an5\\fs44\\c&H002A2AD8&\\fad(220,160)}MENOLAK MAKAN = BUNUH DIRI PERLAHAN"),
    # ── B6 perjanjian moral
    (51.70,  55.70, "Stamp", "{\\pos(540,520)\\an5\\fs64\\frz-4\\fad(160,150)}PAKTA DI TENGAH ES"),
    (56.30,  60.10, "Kicker", "{\\pos(540,1010)\\an5\\fs46\\fad(220,160)}JIKA AKU MATI, PAKAILAH RAGAKU"),
    (60.60,  64.50, "Kicker", "{\\pos(540,1010)\\an5\\fs46\\fad(220,160)}PULANG MENEMUI KELUARGA"),
    # ── B7 payoff
    (65.10,  67.90, "Kicker", "{\\pos(540,1010)\\an5\\fs48\\fad(220,160)}DUA ORANG BERJALAN KELUAR"),
    (68.20,  71.20, "Kicker", "{\\pos(540,1010)\\an5\\fs44\\fad(220,160)}MENEMBUS DINDING ES ANDES · 72 HARI"),
    (71.50,  74.50, "Kicker", "{\\pos(540,700)\\an5\\fs48\\c&H002A2AD8&\\fad(220,160)}16 ORANG PULANG HIDUP-HIDUP"),
    # ── B8 debat komentar
    (75.10,  78.90, "Kicker", "{\\pos(540,700)\\an5\\fs56\\c&H002A2AD8&\\fad(240,170)}MAKAN DEMI PULANG?"),
    (79.30,  83.10, "Kicker", "{\\pos(540,700)\\an5\\fs56\\fad(240,170)}MATI DEMI PRINSIP?"),
    (83.50,  87.10, "Kicker", "{\\pos(540,1010)\\an5\\fs48\\fad(220,160)}TULIS PILIHANMU DI KOMENTAR"),
    # ── kartu penutup
    (87.70,   91.40, "Big", "{\\pos(540,640)\\an5\\fs110\\fad(260,0)}ODDCHAPTER"),
    (88.00,   91.40, "Kicker", "{\\pos(540,740)\\an5\\fs42\\c&H002A2AD8&\\fad(300,0)}KASUS NYATA · ARSIP ASLI"),
    (88.30,   91.40, "Credit", "{\\pos(540,1000)\\an5\\fs26\\c&H00D0D0D0&\\fad(360,0)}" + CREDITS),
]
