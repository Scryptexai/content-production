"""Konfigurasi kasus AK-EP05 — Tragedi Andes 1972 (uji format Curiosity Loop 00F).

VO = TTS internal voice-05, 10 klip beat (naskah 02_SCRIPT/AK-EP05_andes-1972.md).
Durasi VO 169,91 s; END 174,00 s (kartu penutup 4,1 s). Waktu kata dari
build_vo.py (perkiraan bobot suku kata per kalimat — batas kalimat diketahui).

Format: 8 beat adaptasi — dilema (B1) → reaksi (B2) → tindakan mengagetkan (B3) →
pertaruhan (B4) → tekanan (B5–B7) → puncak (B8) → reveal (B9) → debat komentar (B10).

Tanpa gore, tanpa kondisi jenazah, tanpa detail prosedur. Footage stok Coverr,
dilabeli di layar + dikreditkan di kartu akhir dan deskripsi.
"""

SLUG = "andes-1972"
VO_FILE = "vo_andes.mp3"
END = 174.00
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
    # ── B2 reaksi alami manusia (10,04–21,23)
    (10.04,  14.60, "HUTAN_DINGIN", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    (14.60,  18.00, "SISA_SALJU", "clipfill", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (18.00,  21.23, "GUNUNG_KABUT", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    # ── B3 tindakan yang mengagetkan (21,23–38,55)
    (21.23,  25.60, "LILIN_GELAP", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **NIGHT}),
    (25.60,  30.10, "HUTAN_SALJU", "clipfill", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (30.10,  34.60, "API_GELAP", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **NIGHT}),
    (34.60,  38.55, "TENDA_DINGIN", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    # ── B4 pertaruhan nyawa (38,55–57,10)
    (38.55,  43.20, "SALIB_GUNUNG", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    (43.20,  47.80, "API_GELAP2", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **NIGHT}),
    (47.80,  52.40, "KORAN", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    (52.40,  57.10, "GUNUNG_KABUT2", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    # ── B5 kecelakaan (57,10–81,33)
    (57.10,  61.60, "PESAWAT_AWAN", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    (61.60,  66.20, "NAIK_PESAWAT", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    (66.20,  70.70, "PESAWAT_GUNUNG", "clipfill", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (70.70,  75.20, "GUNUNG_SALJU", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    (75.20,  78.60, "JENDELA_PESAWAT", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    (78.60,  81.33, "SISA_SALJU2", "clipfill", 1.00, 1.00, {"tag": TAG_STOK_C}),
    # ── B6 kelaparan & longsor (81,33–102,79)
    (81.33,  85.90, "HUTAN_SALJU", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    (85.90,  90.40, "PESAWAT_PENCARI2", "clipfill", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (90.40,  95.00, "GUNUNG_KABUT3", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    (95.00,  99.10, "SALIB_GUNUNG2", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    (99.10, 102.79, "LILIN_GELAP2", "clipfill", 1.00, 1.00, {"tag": TAG_STOK_C}),
    # ── B7 sumpah bersama (102,79–115,46)
    (102.79, 107.00, "GUNUNG_SNOW2", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    (107.00, 111.20, "TENDA_DINGIN2", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    (111.20, 115.46, "HUTAN_DINGIN2", "clipfill", 1.00, 1.00, {"tag": TAG_STOK_C}),
    # ── B8 momen puncak: berjalan keluar (115,46–133,69)
    (115.46, 120.10, "TREK_MOUNTAIN", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    (120.10, 124.70, "PUNCAK_JALAN", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    (124.70, 129.20, "TREK_MOUNTAIN2", "clipfill", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (129.20, 133.69, "LEMBAH_AERIAL", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    # ── B9 hasil & fakta kunci (133,69–156,24)
    (133.69, 138.50, "PESAWAT_PENCARI", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    (138.50, 143.10, "ARGENTINA_VALLEY", "clipfill", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (143.10, 147.70, "LEMBAH", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    (147.70, 152.10, "GUNUNG_SALJU2", "clipfill", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (152.10, 156.24, "ARGENTINA_TIERRA", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    # ── B10 debat komentar (156,24–169,91)
    (156.24, 161.10, "GUNUNG_KABUT4", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    (161.10, 165.60, "API_GELAP3", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **NIGHT}),
    (165.60, 169.91, "GUNUNG_SNOW", "clipfill", 1.00, 1.00, {"tag": TAG_STOK_C}),
    # ── kartu penutup (169,91–174,00)
    (169.91, 174.00, None, "black", 1.00, 1.00, {}),
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
    (10.50, 14.40, "Kicker", "{\\pos(540,1010)\\an5\\fs50\\fad(220,160)}PASTI KALIAN CARI DAUN & AKAR"),
    (18.30, 21.10, "Kicker", "{\\pos(540,700)\\an5\\fs52\\fad(220,160)}TIDAK ADA YANG BISA DIMAKAN"),
    # ── B3 tindakan mengagetkan
    (21.60, 25.40, "Kicker", "{\\pos(540,1010)\\an5\\fs44\\fad(220,160)}KEPUTUSAN YANG TAK PERNAH DIRENCANAKAN"),
    (30.40, 34.40, "Kicker", "{\\pos(540,1010)\\an5\\fs46\\c&H002A2AD8&\\fad(220,160)}SATU-SATUNYA MAKANAN YANG TERSISA"),
    # ── B4 pertaruhan
    (38.90, 43.00, "Kicker", "{\\pos(540,700)\\an5\\fs50\\fad(220,160)}ORANG BERIMAN HARUS MEMILIH"),
    (43.60, 47.60, "Stamp", "{\\pos(540,520)\\an5\\fs80\\frz-4\\fad(160,150)}HARI KE-11"),
    (48.20, 52.20, "Kicker", "{\\pos(540,1010)\\an5\\fs50\\fad(220,160)}PENCARIAN RESMI DIHENTIKAN"),
    (52.80, 56.90, "Kicker", "{\\pos(540,1010)\\an5\\fs44\\fad(220,160)}TAK ADA YANG TAHU MEREKA MASIH HIDUP"),
    # ── B5 kecelakaan
    (57.40, 61.40, "Stamp", "{\\pos(540,520)\\an5\\fs72\\frz-4\\fad(160,150)}13 · 10 · 1972"),
    (61.90, 66.00, "Kicker", "{\\pos(540,1010)\\an5\\fs46\\fad(220,160)}TIM RUGBI OLD CHRISTIANS CLUB"),
    (66.50, 70.50, "Kicker", "{\\pos(540,700)\\an5\\fs52\\fad(220,160)}JATUH DI SISI ARGENTINA"),
    (71.00, 73.20, "Big", "{\\pos(540,620)\\an5\\fs150\\c&H002A2AD8&\\fad(200,150)}12"),
    (73.25, 75.10, "Kicker", "{\\pos(540,860)\\an5\\fs44\\c&H00E0ECF0&\\fad(200,150)}TEWAS SEKETIKA"),
    (75.50, 77.00, "Big", "{\\pos(540,620)\\an5\\fs150\\c&H002A2AD8&\\fad(200,150)}33"),
    (77.05, 78.50, "Kicker", "{\\pos(540,860)\\an5\\fs44\\c&H00E0ECF0&\\fad(200,150)}SELAMAT DI HARI PERTAMA"),
    (78.90, 81.20, "Kicker", "{\\pos(540,1010)\\an5\\fs44\\fad(220,160)}BADAN PESAWAT PUTIH · TAK TERLIHAT"),
    # ── B6 kelaparan & longsor
    (81.60, 85.70, "Kicker", "{\\pos(540,1010)\\an5\\fs48\\fad(220,160)}MAKANAN HABIS DALAM SATU MINGGU"),
    (86.20, 90.20, "Kicker", "{\\pos(540,700)\\an5\\fs52\\fad(220,160)}SOS DENGAN LIPSTIK"),
    (90.70, 92.60, "Big", "{\\pos(540,620)\\an5\\fs150\\c&H002A2AD8&\\fad(200,150)}8"),
    (92.65, 94.80, "Kicker", "{\\pos(540,860)\\an5\\fs42\\c&H00E0ECF0&\\fad(200,150)}TEWAS DALAM LONGSOR · 29 OKT"),
    (95.30, 98.90, "Kicker", "{\\pos(540,1010)\\an5\\fs50\\fad(220,160)}PERDEBATAN YANG PANJANG"),
    # ── B7 sumpah
    (103.10, 106.80, "Stamp", "{\\pos(540,520)\\an5\\fs76\\frz-4\\fad(160,150)}SUMPAH BERSAMA"),
    (107.30, 111.00, "Kicker", "{\\pos(540,1010)\\an5\\fs44\\c&H002A2AD8&\\fad(220,160)}TAK ADA YANG DIBUNUKH UNTUK DIMAKAN"),
    # ── B8 berjalan keluar
    (115.80, 119.90, "Kicker", "{\\pos(540,1010)\\an5\\fs50\\fad(220,160)}DUA ORANG BERJALAN KELUAR"),
    (120.40, 124.50, "Kicker", "{\\pos(540,700)\\an5\\fs52\\fad(220,160)}10 HARI TANPA PETA"),
    (125.00, 129.00, "Kicker", "{\\pos(540,1010)\\an5\\fs48\\fad(220,160)}SERGIO CATALÁN · PENGEMBALA"),
    (129.50, 133.50, "Kicker", "{\\pos(540,1010)\\an5\\fs50\\fad(220,160)}KABAR SAMPAI KANTOR POLISI"),
    # ── B9 reveal
    (134.00, 138.30, "Stamp", "{\\pos(540,520)\\an5\\fs72\\frz-4\\fad(160,150)}22 · 12 · 1972"),
    (138.80, 142.90, "Kicker", "{\\pos(540,1010)\\an5\\fs50\\fad(220,160)}LEMBAH DEKAT PERBATASAN CILE"),
    (143.40, 145.20, "Big", "{\\pos(540,620)\\an5\\fs150\\c&H002A2AD8&\\fad(200,150)}72"),
    (145.25, 147.50, "Kicker", "{\\pos(540,860)\\an5\\fs46\\c&H00E0ECF0&\\fad(200,150)}HARI DI GUNUNG"),
    (148.00, 149.80, "Big", "{\\pos(540,620)\\an5\\fs150\\c&H002A2AD8&\\fad(200,150)}16"),
    (149.85, 151.90, "Kicker", "{\\pos(540,860)\\an5\\fs44\\c&H00E0ECF0&\\fad(200,150)}DARI 45 ORANG SELAMAT"),
    (152.40, 156.00, "Kicker", "{\\pos(540,1010)\\an5\\fs46\\fad(220,160)}KEPUTUSAN, BUKAN KEBERUNTUNGAN"),
    # ── B10 debat
    (156.60, 160.90, "Kicker", "{\\pos(540,700)\\an5\\fs56\\c&H002A2AD8&\\fad(240,170)}GILIRAN KALIAN"),
    (161.40, 165.40, "Kicker", "{\\pos(540,1010)\\an5\\fs54\\fad(220,160)}IKUT, ATAU TOLAK?"),
    (165.90, 169.70, "Kicker", "{\\pos(540,1010)\\an5\\fs46\\fad(220,160)}TULIS JAWABANMU DI KOLOM KOMENTAR"),
    # ── kartu penutup
    (170.30, 174.00, "Big", "{\\pos(540,640)\\an5\\fs110\\fad(260,0)}ODDCHAPTER"),
    (170.60, 174.00, "Kicker", "{\\pos(540,740)\\an5\\fs42\\c&H002A2AD8&\\fad(300,0)}KASUS NYATA · ARSIP ASLI"),
    (170.90, 174.00, "Credit", "{\\pos(540,1000)\\an5\\fs26\\c&H00D0D0D0&\\fad(360,0)}" + CREDITS),
]
