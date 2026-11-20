"""Konfigurasi kasus AK-EP05 — Tragedi Andes 1972 (uji format Curiosity Loop 00F).

VO = TTS internal voice-05, 10 klip beat (naskah 02_SCRIPT/AK-EP05_andes-1972.md).
Durasi VO 169,12 s; END 173,21 s (kartu penutup 4,1 s). Waktu kata dari
build_vo.py (perkiraan bobot suku kata per kalimat — batas kalimat diketahui).

Format: 8 beat adaptasi — dilema (B1) → reaksi (B2) → tindakan mengagetkan (B3) →
pertaruhan (B4) → tekanan (B5–B7) → puncak (B8) → reveal (B9) → debat komentar (B10).

Tanpa gore, tanpa kondisi jenazah, tanpa detail prosedur. Footage stok Coverr,
dilabeli di layar + dikreditkan di kartu akhir dan deskripsi.
"""

SLUG = "andes-1972"
VO_FILE = "vo_andes.mp3"
END = 173.21
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
    "SENJA_SALJU":   ("senja_salju.mp4",        0.40, 6.00),
    "SENJA_SALJU2":  ("senja_salju.mp4",        1.10, 6.00),
    "SENJA_SALJU3":  ("senja_salju.mp4",        0.30, 6.00),
    "SENJA_SALJU4":  ("senja_salju.mp4",        1.40, 6.00),
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
    "KORAN":          ("koran.mp4",             0.50, 6.00),
}

TAG_STOK_C = "FOOTAGE STOK · COVERR"

BOX = {"box": (1020, 574)}
NIGHT = {"box": (1020, 574), "bg": "-0.66"}

# (mulai, selesai, klip, mode, z0, z1, opsi)
SHOTS = [
    # ── B1 dilema ekstrem (0,00–10,04)
    (0.00,    1.00, None, "black", 1.00, 1.00, {}),
    (1.00,    5.40, "GUNUNG_SNOW", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    (5.40,   10.04, "SALJU_HUTAN", "clipfill", 1.00, 1.00, {"tag": TAG_STOK_C}),
    # ── B2 reaksi alami manusia (10,04–19,77)
    (10.04,  14.01, "HUTAN_DINGIN", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    (14.01,  16.96, "SISA_SALJU", "clipfill", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (16.96,  19.77, "GUNUNG_KABUT", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    # ── B3 tindakan yang mengagetkan (19,77–37,79)
    (19.77,  24.32, "LILIN_GELAP", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **NIGHT}),
    (24.32,  29.00, "HUTAN_SALJU", "clipfill", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (29.00,  33.68, "API_GELAP", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **NIGHT}),
    (33.68,  37.79, "TENDA_DINGIN", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    # ── B4 pertaruhan nyawa (37,79–56,35)
    (37.79,  42.44, "SALIB_GUNUNG", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    (42.44,  47.04, "API_GELAP2", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **NIGHT}),
    (47.04,  51.65, "KORAN", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    (51.65,  56.35, "GUNUNG_KABUT2", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    # ── B5 kecelakaan (56,35–80,57)
    (56.35,  60.85, "PESAWAT_AWAN", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    (60.85,  65.45, "NAIK_PESAWAT", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    (65.45,  69.94, "PESAWAT_GUNUNG", "clipfill", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (69.94,  74.44, "GUNUNG_SALJU", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    (74.44,  77.84, "JENDELA_PESAWAT", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    (77.84,  80.57, "SISA_SALJU2", "clipfill", 1.00, 1.00, {"tag": TAG_STOK_C}),
    # ── B6 kelaparan & longsor (80,57–102,03)
    (80.57,  85.14, "HUTAN_SALJU", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    (85.14,  89.64, "PESAWAT_PENCARI2", "clipfill", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (89.64,  94.24, "GUNUNG_KABUT3", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    (94.24,  98.34, "SALIB_GUNUNG2", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    (98.34, 102.03, "LILIN_GELAP2", "clipfill", 1.00, 1.00, {"tag": TAG_STOK_C}),
    # ── B7 sumpah bersama (102,03–114,70)
    (102.03, 106.24, "GUNUNG_SNOW2", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    (106.24, 110.44, "TENDA_DINGIN2", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    (110.44, 114.70, "HUTAN_DINGIN2", "clipfill", 1.00, 1.00, {"tag": TAG_STOK_C}),
    # ── B8 momen puncak: berjalan keluar (114,70–132,93)
    (114.70, 119.34, "TREK_MOUNTAIN", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    (119.34, 123.94, "PUNCAK_JALAN", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    (123.94, 128.44, "TREK_MOUNTAIN2", "clipfill", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (128.44, 132.93, "LEMBAH_AERIAL", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    # ── B9 hasil & fakta kunci (132,93–155,46)
    (132.93, 137.74, "PESAWAT_PENCARI", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    (137.74, 142.33, "ARGENTINA_VALLEY", "clipfill", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (142.33, 146.93, "LEMBAH", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    (146.93, 151.32, "GUNUNG_SALJU2", "clipfill", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (151.32, 155.46, "ARGENTINA_TIERRA", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    # ── B10 debat komentar (155,46–169,12)
    (155.46, 160.32, "GUNUNG_KABUT4", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    (160.32, 164.81, "API_GELAP3", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **NIGHT}),
    (164.81, 169.12, "GUNUNG_SNOW", "clipfill", 1.00, 1.00, {"tag": TAG_STOK_C}),
    # ── kartu penutup (169,12–173,21)
    (169.12, 173.21, None, "black", 1.00, 1.00, {}),
]

KEYWORDS = {"ANDES", "SOS", "1972", "16"}

# angka dieja di VO -> digit di caption; urutan frasa panjang dulu untuk potongan tumpang tindih
NUM_PHRASES = [
    (["seribu", "sembilan", "ratus", "tujuh", "puluh", "dua"], "1972"),
    (["tiga", "belas"], "13"),
    (["dua", "belas"], "12"),
    (["tiga", "puluh", "tiga"], "33"),
    (["dua", "puluh", "sembilan"], "29"),
    (["dua", "puluh", "dua"], "22"),
    (["tujuh", "puluh", "dua"], "72"),
    (["enam", "belas"], "16"),
    (["empat", "puluh", "lima"], "45"),
    (["kesebelas"], "KE-11"),
    (["sepuluh"], "10"),
    (["delapan"], "8"),
]

MERGE = []
WORD_FIX = {}

CREDITS = ("Footage stok: Coverr\\N"
           "Sumber: Wikipedia · Britannica\\N"
           "Piers Paul Read, Alive (1974) · Nando Parrado\\N"
           "Pablo Vierci, La Sociedad de la Nieve\\N"
           "@oddchapter7 · KASUS NYATA · ARSIP ASLI")

OVL = [
    # ── B1 dilema
    (1.60,   5.20, "Kicker", "{\\pos(540,700)\\an5\\fs48\\fad(240,170)}BAYANGKAN PESAWAT KALIAN JATUH"),
    (5.80,   9.90, "Kicker", "{\\pos(540,1010)\\an5\\fs50\\fad(220,160)}TUJUH HARI TANPA MAKANAN"),
    # ── B2 reaksi
    (10.44, 13.83, "Kicker", "{\\pos(540,1010)\\an5\\fs50\\fad(220,160)}PASTI KALIAN CARI BUAH-BUAHAN"),
    (17.22, 19.66, "Kicker", "{\\pos(540,700)\\an5\\fs52\\fad(220,160)}TIDAK ADA YANG BISA DIMAKAN"),
    # ── B3 tindakan mengagetkan
    (20.15, 24.11, "Kicker", "{\\pos(540,1010)\\an5\\fs44\\fad(220,160)}KEPUTUSAN YANG TAK PERNAH DIRENCANAKAN"),
    (29.31, 33.47, "Kicker", "{\\pos(540,1010)\\an5\\fs46\\c&H002A2AD8&\\fad(220,160)}SATU-SATUNYA MAKANAN YANG TERSISA"),
    # ── B4 pertaruhan
    (38.14, 42.24, "Kicker", "{\\pos(540,700)\\an5\\fs50\\fad(220,160)}ORANG BERIMAN HARUS MEMILIH"),
    (42.84, 46.84, "Stamp", "{\\pos(540,520)\\an5\\fs80\\frz-4\\fad(160,150)}HARI KE-11"),
    (47.45, 51.45, "Kicker", "{\\pos(540,1010)\\an5\\fs50\\fad(220,160)}PENCARIAN RESMI DIHENTIKAN"),
    (52.05, 56.15, "Kicker", "{\\pos(540,1010)\\an5\\fs44\\fad(220,160)}TAK ADA YANG TAHU MEREKA MASIH HIDUP"),
    # ── B5 kecelakaan
    (56.65, 60.65, "Stamp", "{\\pos(540,520)\\an5\\fs72\\frz-4\\fad(160,150)}13 · 10 · 1972"),
    (61.15, 65.25, "Kicker", "{\\pos(540,1010)\\an5\\fs46\\fad(220,160)}TIM RUGBI OLD CHRISTIANS CLUB"),
    (65.75, 69.74, "Kicker", "{\\pos(540,700)\\an5\\fs52\\fad(220,160)}JATUH DI SISI ARGENTINA"),
    (70.24, 72.44, "Big", "{\\pos(540,620)\\an5\\fs150\\c&H002A2AD8&\\fad(200,150)}12"),
    (72.49, 74.34, "Kicker", "{\\pos(540,860)\\an5\\fs44\\c&H00E0ECF0&\\fad(200,150)}TEWAS SEKETIKA"),
    (74.74, 76.24, "Big", "{\\pos(540,620)\\an5\\fs150\\c&H002A2AD8&\\fad(200,150)}33"),
    (76.29, 77.74, "Kicker", "{\\pos(540,860)\\an5\\fs44\\c&H00E0ECF0&\\fad(200,150)}SELAMAT DI HARI PERTAMA"),
    (78.14, 80.44, "Kicker", "{\\pos(540,1010)\\an5\\fs44\\fad(220,160)}BADAN PESAWAT PUTIH · TAK TERLIHAT"),
    # ── B6 kelaparan & longsor
    (80.84, 84.94, "Kicker", "{\\pos(540,1010)\\an5\\fs48\\fad(220,160)}MAKANAN HABIS DALAM SATU MINGGU"),
    (85.44, 89.44, "Kicker", "{\\pos(540,700)\\an5\\fs52\\fad(220,160)}SOS DENGAN LIPSTIK"),
    (89.94, 91.84, "Big", "{\\pos(540,620)\\an5\\fs150\\c&H002A2AD8&\\fad(200,150)}8"),
    (91.89, 94.04, "Kicker", "{\\pos(540,860)\\an5\\fs42\\c&H00E0ECF0&\\fad(200,150)}TEWAS DALAM LONGSOR · 29 OKT"),
    (94.54, 98.14, "Kicker", "{\\pos(540,1010)\\an5\\fs50\\fad(220,160)}PERDEBATAN YANG PANJANG"),
    # ── B7 sumpah
    (102.34, 106.04, "Stamp", "{\\pos(540,520)\\an5\\fs76\\frz-4\\fad(160,150)}SUMPAH BERSAMA"),
    (106.54, 110.24, "Kicker", "{\\pos(540,1010)\\an5\\fs44\\c&H002A2AD8&\\fad(220,160)}TAK ADA YANG DIBUNUKH UNTUK DIMAKAN"),
    # ── B8 berjalan keluar
    (115.04, 119.14, "Kicker", "{\\pos(540,1010)\\an5\\fs50\\fad(220,160)}DUA ORANG BERJALAN KELUAR"),
    (119.64, 123.74, "Kicker", "{\\pos(540,700)\\an5\\fs52\\fad(220,160)}10 HARI TANPA PETA"),
    (124.24, 128.24, "Kicker", "{\\pos(540,1010)\\an5\\fs48\\fad(220,160)}SERGIO CATALÁN · PENGEMBALA"),
    (128.74, 132.74, "Kicker", "{\\pos(540,1010)\\an5\\fs50\\fad(220,160)}KABAR SAMPAI KANTOR POLISI"),
    # ── B9 reveal
    (133.24, 137.54, "Stamp", "{\\pos(540,520)\\an5\\fs72\\frz-4\\fad(160,150)}22 · 12 · 1972"),
    (138.04, 142.13, "Kicker", "{\\pos(540,1010)\\an5\\fs50\\fad(220,160)}LEMBAH DEKAT PERBATASAN CILE"),
    (142.63, 144.43, "Big", "{\\pos(540,620)\\an5\\fs150\\c&H002A2AD8&\\fad(200,150)}72"),
    (144.48, 146.73, "Kicker", "{\\pos(540,860)\\an5\\fs46\\c&H00E0ECF0&\\fad(200,150)}HARI DI ANDES"),
    (147.23, 149.03, "Big", "{\\pos(540,620)\\an5\\fs150\\c&H002A2AD8&\\fad(200,150)}16"),
    (149.08, 151.12, "Kicker", "{\\pos(540,860)\\an5\\fs44\\c&H00E0ECF0&\\fad(200,150)}DARI 45 ORANG SELAMAT"),
    (151.62, 155.22, "Kicker", "{\\pos(540,1010)\\an5\\fs46\\fad(220,160)}KEPUTUSAN, BUKAN KEBERUNTUNGAN"),
    # ── B10 debat
    (155.82, 160.12, "Kicker", "{\\pos(540,700)\\an5\\fs56\\c&H002A2AD8&\\fad(240,170)}GILIRAN KALIAN"),
    (160.62, 164.61, "Kicker", "{\\pos(540,1010)\\an5\\fs54\\fad(220,160)}IKUT, ATAU TOLAK?"),
    (165.11, 168.91, "Kicker", "{\\pos(540,1010)\\an5\\fs46\\fad(220,160)}TULIS JAWABANMU DI KOLOM KOMENTAR"),
    # ── kartu penutup
    (169.51, 173.21, "Big", "{\\pos(540,640)\\an5\\fs110\\fad(260,0)}ODDCHAPTER"),
    (169.81, 173.21, "Kicker", "{\\pos(540,740)\\an5\\fs42\\c&H002A2AD8&\\fad(300,0)}KASUS NYATA · ARSIP ASLI"),
    (170.11, 173.21, "Credit", "{\\pos(540,1000)\\an5\\fs26\\c&H00D0D0D0&\\fad(360,0)}" + CREDITS),
]
