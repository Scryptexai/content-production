"""Konfigurasi kasus AK-EP09 — Gerhana 1983: negara menyuruh masuk rumah (Batch 2 #5).

VO = VO PEMILIK apa adanya (vo_owner/vo_gerhana-1983.mp3,89,12 s,151 kata;
ElevenLabs Riri Rida, alignment faster-whisper). Tanpa TTS. END93,20 s (kartu
penutup4,56 s).

Sudut: ketaatan massal vs edukasi — perintah masuk rumah, TVRI/RRI, aparat,
kritik ilmuwan LIPI. Nada ganjil-bukan-kriminal, tanpa teori konspirasi.
ATURAN21 Nov2026: semua klip16:9 cover-crop FULL LAYAR9:16 (default
clip_filter; tanpa "window").
"""

SLUG = "gerhana-1983"
VO_FILE = "vo_owner/vo_gerhana-1983.mp3"
END = 93.20
OUT_NAME = "AK-EP09_gerhana-1983_short.mp4"
SRT_NAME = "AK-EP09.id.srt"
BED_BUILDER = "bed_gerhana.py"

# still AI (tanpa orang): key -> (file, lebar, tinggi)
IMAGES = {
    "ECLIPSE":  ("eclipse.jpg", 768, 1376),
    "SHUTTER":  ("window_shutters.jpg", 768, 1376),
    "TV":       ("old_tv.jpg", 768, 1376),
}

# work/gerhana-1983/footage/ → symlink bank/:
# (berkas, detik mulai, durasi tersedia)
CLIPS = {
    "LANGIT":     ("sb-ep02/s2_langit_malam.mp4",                     0.30, 6.00),
    "KOTA_MALAM": ("night_city_aerial__coverr-city-at-night-4382.mp4", 0.60, 8.00),
    "KORAN":      ("newspaper_printing__coverr-local-dutch-newspapers-8257.mp4", 0.40, 6.00),
    "TULIS1":     ("hand_writing_letter__coverr-handwriting-a-note-8044.mp4", 0.60, 8.00),
    "MATA":       ("close_up_eye__coverr-ai-generated-close-up-of-a-pale-horses-eye.mp4", 0.40, 6.00),
    "HUJAN":      ("rain_on_window_night__user-ai-generation-BCHZqmfTpSvX.mp4", 0.40, 6.00),
    "JENDELA":    ("sb-ep02/s2_jendela_senja.mp4",                     0.40, 6.00),
    "KORIDOR":    ("dark_corridor__coverr-scary-hallway-7141.mp4",     0.40, 6.00),
    "BAYANGAN":   ("shadow_walking__coverr-pov-walking-down-the-street-1894.mp4", 0.40, 6.00),
    "ANTRE":      ("crowd_slow_motion__coverr-crowded-bridge-8424.mp4", 0.60, 8.00),
    "AWAN":       ("sb-ep02/s2_awan_dari_kabin.mp4",                   0.30, 6.00),
    "KOTA2":      ("sb-ep02/s7_kota_malam.mp4",                        0.40, 6.00),
    "MATA2":      ("close_up_eye__coverr-ai-generated-close-up-of-a-pale-horses-eye.mp4", 1.50, 6.00),
    "BULAN":      ("moon_night_sky__user-ai-generation-0b4ZdNtmzT9q.mp4", 0.40, 6.00),
    "ASAP":       ("smoke_black_background__user-ai-generation-iaAaX0rR2kx7.mp4", 0.40, 6.00),
    "JEMAAH":     ("crowd_slow_motion__coverr-live-music-concert-5249.mp4", 0.60, 8.00),
    "BUKU":       ("stack_of_books__coverr-placing-books-on-a-desk-2325.mp4", 0.50, 8.00),
    "TULIS2":     ("hand_writing_letter__coverr-writing-a-note-4875.mp4", 0.50, 8.00),
    "KORAN2":     ("newspaper_printing__coverr-local-dutch-newspapers-8257.mp4", 1.50, 6.00),
}

TAG_STOK_C = "FOOTAGE STOK · COVERR"

# (mulai, selesai, klip/still, mode, z0, z1, opsi)
# mode "clip" = footage cover-crop FULL LAYAR9:16 (aturan21 Nov2026)
SHOTS = [
    # ── B1 tengah hari jadi malam (0,00–11,54)
    (0.00,    0.80, None, "black", 1.00, 1.00, {}),
    (0.80,    5.20, "ECLIPSE", "fill", 1.00, 1.09, {}),
    (5.20,    8.40, "LANGIT", "clip", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (8.40,   11.54, "KOTA_MALAM", "clip", 1.00, 1.00, {"tag": TAG_STOK_C}),
    # ── B2 peringatan TVRI/RRI (11,54–24,34)
    (11.54,  15.60, "TV", "fill", 1.00, 1.08, {}),
    (15.60,  19.40, "KORAN", "clip", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (19.40,  21.90, "TULIS1", "clip", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (21.90,  24.34, "MATA", "clip", 1.00, 1.00, {"tag": TAG_STOK_C}),
    # ── B3 rakyat patuh (24,34–39,48)
    (24.34,  28.40, "HUJAN", "clip", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (28.40,  32.00, "SHUTTER", "fill", 1.04, 1.12, {}),
    (32.00,  35.20, "JENDELA", "clip", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (35.20,  39.48, "KORIDOR", "clip", 1.00, 1.00, {"tag": TAG_STOK_C}),
    # ── B4 aparat &20 teropong (39,48–46,88)
    (39.48,  43.00, "BAYANGAN", "clip", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (43.00,  46.88, "ANTRE", "clip", 1.00, 1.00, {"tag": TAG_STOK_C}),
    # ── B5 astronom datang, rakyat hanya TVRI (46,88–58,90)
    (46.88,  50.60, "AWAN", "clip", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (50.60,  54.40, "TV", "fill", 1.15, 1.05, {}),
    (54.40,  58.90, "KOTA2", "clip", 1.00, 1.00, {"tag": TAG_STOK_C}),
    # ── B6 ayah Semarang (58,90–67,06)
    (58.90,  62.40, "MATA2", "clip", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (62.40,  64.80, "BULAN", "clip", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (64.80,  67.06, "ASAP", "clip", 1.00, 1.00, {"tag": TAG_STOK_C}),
    # ── B7 Yogyakarta446/14, LIPI (67,06–79,68)
    (67.06,  71.00, "JEMAAH", "clip", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (71.00,  74.40, "BUKU", "clip", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (74.40,  77.00, "TULIS2", "clip", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (77.00,  79.68, "KORAN2", "clip", 1.00, 1.00, {"tag": TAG_STOK_C}),
    # ── B8 debate hook (79,68–88,64)
    (79.68,  84.00, "SHUTTER", "fill", 1.14, 1.04, {}),
    (84.00,  88.64, "ECLIPSE", "fill", 1.10, 1.00, {}),
    # ── kartu penutup (88,64–93,20)
    (88.64,  93.20, None, "black", 1.00, 1.00, {}),
]

KEYWORDS = {"GERHANA", "1983", "446"}

NUM_PHRASES = [
    (["satu", "jam"], "1 jam"),
]

MERGE = [
    (["satu", "-satunya"], "satu-satunya"),
    (["di", "perintah"], "diperintah"),
]

WORD_FIX = {
    "tropong": "teropong",
}

CREDITS = ("Footage stok: Coverr\\N"
           "Sumber: CNN Indonesia · Tirto (Kompas1983)\\N"
           "@oddchapter7 · KASUS NYATA · ARSIP ASLI")

OVL = [
    # ── B1 tengah hari jadi malam
    (1.10,    5.00, "Stamp", "{\\pos(540,520)\\an5\\fs64\\frz-4\\fad(160,150)}11 JUNI 1983"),
    (5.50,    8.20, "Kicker", "{\\pos(540,700)\\an5\\fs52\\fad(240,170)}TENGAH HARI JADI MALAM"),
    (8.60,   11.40, "Stamp", "{\\pos(540,520)\\an5\\fs72\\frz-4\\fad(160,150)}MASUK RUMAH"),
    # ── B2 peringatan TVRI/RRI
    (12.00,  15.40, "Kicker", "{\\pos(540,1010)\\an5\\fs46\\fad(220,160)}PERINGATAN LEWAT TVRI & RRI"),
    (15.90,  19.20, "Stamp", "{\\pos(540,520)\\an5\\fs76\\frz-4\\c&H002A2AD8&\\fad(160,150)}JANGAN MENATAP"),
    (19.60,  21.70, "Kicker", "{\\pos(540,700)\\an5\\fs52\\fad(220,160)}KAMU BISA BUTA"),
    (22.10,  24.20, "Kicker", "{\\pos(540,1010)\\an5\\fs48\\fad(220,160)}PRESIDEN SOEHARTO → MENPEN"),
    # ── B3 rakyat patuh
    (24.80,  28.20, "Kicker", "{\\pos(540,1010)\\an5\\fs50\\fad(220,160)}RAKYAT PATUH"),
    (28.80,  31.80, "Kicker", "{\\pos(540,700)\\an5\\fs46\\fad(220,160)}JENDELA RAPAT — LUBANG ANGIN DISUMBAT"),
    (32.30,  35.00, "Kicker", "{\\pos(540,1010)\\an5\\fs46\\fad(220,160)}MATA SAPI DITUTUP KAIN"),
    (35.50,  39.30, "Kicker", "{\\pos(540,1010)\\an5\\fs44\\fad(220,160)}HAMIL DISURUH SEMBUNYI DI KOLONG"),
    # ── B4 aparat
    (39.90,  42.80, "Kicker", "{\\pos(540,700)\\an5\\fs48\\fad(220,160)}APARAT: MASUK LAGI!"),
    (43.30,  46.70, "Stamp", "{\\pos(540,520)\\an5\\fs72\\frz-4\\fad(160,150)}20 TEROPONG DISITA"),
    # ── B5 astronom vs rakyat
    (47.30,  50.40, "Kicker", "{\\pos(540,1010)\\an5\\fs46\\fad(220,160)}ASTRONOM JUSTRU DATANG"),
    (50.90,  54.20, "Kicker", "{\\pos(540,700)\\an5\\fs50\\fad(220,160)}RAKYAT HANYA LEWAT TVRI"),
    (54.80,  58.70, "Kicker", "{\\pos(540,1010)\\an5\\fs46\\fad(220,160)}SATU-SATUNYA TELEVISI SAAT ITU"),
    # ── B6 ayah Semarang
    (59.30,  62.20, "Kicker", "{\\pos(540,1010)\\an5\\fs48\\fad(220,160)}AYAH DI SEMARANG MENATAP LANGSUNG"),
    (62.70,  64.60, "Stamp", "{\\pos(540,520)\\an5\\fs72\\frz-4\\c&H002A2AD8&\\fad(160,150)}1 JAM"),
    (65.00,  66.90, "Kicker", "{\\pos(540,700)\\an5\\fs48\\fad(220,160)}PENGLIHATAN TAK KEMBALI"),
    # ── B7 Yogyakarta, LIPI
    (67.50,  70.80, "Kicker", "{\\pos(540,1010)\\an5\\fs46\\fad(220,160)}YOGYAKARTA:446 PERIKSA MATA"),
    (71.40,  74.20, "Kicker", "{\\pos(540,700)\\an5\\fs50\\c&H002A2AD8&\\fad(220,160)}14 MENGALAMI PERADANGAN"),
    (74.80,  76.80, "Kicker", "{\\pos(540,1010)\\an5\\fs48\\fad(220,160)}ILMUWAN LIPI BICARA"),
    (77.20,  79.50, "Stamp", "{\\pos(540,520)\\an5\\fs56\\frz-4\\fad(160,150)}LARANGAN TANPA PENJELASAN"),
    # ── B8 debate hook
    (80.10,  83.80, "Kicker", "{\\pos(540,1010)\\an5\\fs46\\fad(220,160)}DIPERINTAH BERSEMBUNYI..."),
    (84.30,  88.50, "Kicker", "{\\pos(540,700)\\an5\\fs54\\c&H002A2AD8&\\fad(240,170)}BUKAN DIAJARI CARA MELIHATNYA?"),
    # ── kartu penutup
    (89.10,  93.20, "Big", "{\\pos(540,640)\\an5\\fs110\\fad(260,0)}ODDCHAPTER"),
    (89.40,  93.20, "Kicker", "{\\pos(540,740)\\an5\\fs42\\c&H002A2AD8&\\fad(300,0)}KASUS NYATA · ARSIP ASLI"),
    (89.70,  93.20, "Credit", "{\\pos(540,1000)\\an5\\fs26\\c&H00D0D0D0&\\fad(360,0)}" + CREDITS),
]
