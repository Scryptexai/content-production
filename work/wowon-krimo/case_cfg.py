"""Konfigurasi kasus AK-EP10 — Wowon Krimo: pengganda uang (Shortlist Batch 2 cadangan B1).

VO = VO PEMILIK apa adanya (vo_owner/vo_wowon-krimo.mp3,85,31 s,159 kata;
ElevenLabs Riri Rida, alignment faster-whisper). Tanpa TTS. END89,40 s (kartu
penutup4,44 s).

Sudut: janji uang berlipat vs korban yang menagih. Sensitivitas: pelaku HIDUP
→ bahasa "terdakwa/divonis"; tanpa gore/metode/foto jenazah; tanpa nama korban.
ATURAN21 Nov2026: semua klip16:9 cover-crop FULL LAYAR9:16 (default
clip_filter; tanpa "window").
"""

SLUG = "wowon-krimo"
VO_FILE = "vo_owner/vo_wowon-krimo.mp3"
END = 89.40
OUT_NAME = "AK-EP10_wowon-krimo_short.mp4"
SRT_NAME = "AK-EP10.id.srt"
BED_BUILDER = "bed_wowon.py"

# still AI (tanpa orang): key -> (file, lebar, tinggi)
IMAGES = {
    "AMPLOP": ("amplop_meja.jpg", 768, 1376),
    "TELEPON": ("phone_dark.jpg", 768, 1376),
    "LAUT": ("aki_banyu_sea.jpg", 768, 1376),
}

# work/wowon-krimo/footage/ → symlink bank/:
# (berkas, detik mulai, durasi tersedia)
CLIPS = {
    "CATAT":     ("letters_paper__coverr-scheduling-a-meeting-in-a-diary-8878.mp4", 0.40, 6.00),
    "BAYANGAN":  ("shadow_walking__coverr-pov-walking-down-the-street-1894.mp4", 0.40, 6.00),
    "LAUTMALAM": ("sb-ep02/night_ocean_aerial__coverr-marina-de-lagos-689.mp4",   0.40, 6.00),
    "MATA":      ("close_up_eye__coverr-ai-generated-close-up-of-a-pale-horses-eye.mp4", 0.40, 6.00),
    "KORIDOR":   ("dark_corridor__coverr-scary-hallway-7141.mp4",                 0.40, 6.00),
    "ASAP":      ("smoke_black_background__user-ai-generation-iaAaX0rR2kx7.mp4", 0.40, 6.00),
    "MIGRAN1":   ("sb-ep02/s3_naik_pesawat.mp4",                                  0.40, 6.00),
    "MIGRAN2":   ("sb-ep02/s3_checkin.mp4",                                       0.40, 6.00),
    "TULIS1":    ("hand_writing_letter__coverr-handwriting-a-note-8044.mp4",      0.60, 8.00),
    "HUJAN":     ("rain_on_window_night__user-ai-generation-BCHZqmfTpSvX.mp4",    0.40, 6.00),
    "KORIDOR2":  ("dark_corridor__coverr-scary-hallway-7141.mp4",                 1.50, 6.00),
    "KABUT":     ("fog_forest_mountain__coverr-mountains-in-fanal-madeira-island-6802.mp4", 0.80, 8.00),
    "KORAN":     ("newspaper_printing__coverr-local-dutch-newspapers-8257.mp4",   0.40, 6.00),
    "BUKU":      ("stack_of_books__coverr-placing-books-on-a-desk-2325.mp4",      0.50, 8.00),
    "KRIMINOLOG":("portrait_painting__coverr-old-man-painting-a-portrait-8242.mp4", 0.50, 6.00),
    "ARSIP":     ("old_book_pages__coverr-flicking-through-bible-pages-3558.mp4", 0.50, 8.00),
    "KAPALJAUH": ("sb-ep02/s5_kapal_kejauhan.mp4",                                0.30, 6.00),
    "LAUTLUAS":  ("sb-ep02/s9_laut_luas.mp4",                                     0.30, 6.00),
}

TAG_STOK_C = "FOOTAGE STOK · COVERR"

# (mulai, selesai, klip/still, mode, z0, z1, opsi)
# mode "clip" = footage cover-crop FULL LAYAR9:16 (aturan21 Nov2026)
SHOTS = [
    # ── B1 Rp1.000 → Rp5.000,9 nyawa (0,00–8,44)
    (0.00,    0.80, None, "black", 1.00, 1.00, {}),
    (0.80,    4.60, "AMPLOP", "fill", 1.00, 1.09, {}),
    (4.60,    8.44, "CATAT", "clip", 1.00, 1.00, {"tag": TAG_STOK_C}),
    # ── B2 Wowon, tokoh Aki Banyu (8,44–16,14)
    (8.44,   12.00, "BAYANGAN", "clip", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (12.00,  16.14, "LAUT", "fill", 1.00, 1.10, {}),
    # ── B3 lewat telepon; ternyata Wowon sendiri (16,14–36,24)
    (16.14,  20.10, "TELEPON", "fill", 1.04, 1.12, {}),
    (20.10,  24.60, "LAUTMALAM", "clip", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (24.60,  28.60, "MATA", "clip", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (28.60,  32.40, "KORIDOR", "clip", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (32.40,  36.24, "ASAP", "clip", 1.00, 1.00, {"tag": TAG_STOK_C}),
    # ── B411 pekerja migran (36,24–51,58)
    (36.24,  40.30, "MIGRAN1", "clip", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (40.30,  44.40, "MIGRAN2", "clip", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (44.40,  48.00, "TULIS1", "clip", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (48.00,  51.58, "HUJAN", "clip", 1.00, 1.00, {"tag": TAG_STOK_C}),
    # ── B5 penagih dihabisi (51,58–60,26)
    (51.58,  55.60, "KORIDOR2", "clip", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (55.60,  60.26, "KABUT", "clip", 1.00, 1.00, {"tag": TAG_STOK_C}),
    # ── B6 vonis November2023 (60,26–68,62)
    (60.26,  64.40, "KORAN", "clip", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (64.40,  68.62, "BUKU", "clip", 1.00, 1.00, {"tag": TAG_STOK_C}),
    # ── B7 kriminolog >9 (68,62–74,26)
    (68.62,  71.60, "KRIMINOLOG", "clip", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (71.60,  74.26, "ARSIP", "clip", 1.00, 1.00, {"tag": TAG_STOK_C}),
    # ── B8 debate hook (74,26–84,96)
    (74.26,  78.60, "LAUT", "fill", 1.12, 1.02, {}),
    (78.60,  81.80, "KAPALJAUH", "clip", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (81.80,  84.96, "LAUTLUAS", "clip", 1.00, 1.00, {"tag": TAG_STOK_C}),
    # ── kartu penutup (84,96–89,40)
    (84.96,  89.40, None, "black", 1.00, 1.00, {}),
]

KEYWORDS = {"WOWON", "BANYU", "9", "11"}

NUM_PHRASES = [
    (["rp", "1", "000"], "Rp1.000"),
    (["rp", "5", "000"], "Rp5.000"),
]

MERGE = [
    (["di", "ancam"], "diancam"),
    (["bertahun", "-tahun"], "bertahun-tahun"),
]

WORD_FIX = {
    "wawon": "Wowon",
    "menguara": "mengubah suara",
    "akibanyu": "Aki Banyu",
    "akibatnya": "Aki Banyu",
    "pelakunyanya": "pelakunya",
    "difonis": "divonis",
}

CREDITS = ("Footage stok: Coverr\\N"
           "Sumber: Tempo · BBC Indonesia · detik\\N"
           "@oddchapter7 · KASUS NYATA · ARSIP ASLI")

OVL = [
    # ── B1 amplop
    (1.10,    4.40, "Stamp", "{\\pos(540,520)\\an5\\fs56\\frz-4\\fad(160,150)}RP1.000 JADI RP5.000"),
    (4.90,    8.30, "Stamp", "{\\pos(540,520)\\an5\\fs54\\frz-4\\c&H002A2AD8&\\fad(160,150)}9 ORANG KEHILANGAN NYAWA"),
    # ── B2 Wowon & Aki Banyu
    (8.90,   11.80, "Kicker", "{\\pos(540,1010)\\an5\\fs48\\fad(220,160)}WOWON ERAWAN — DALANGNYA"),
    (12.40,  16.00, "Stamp", "{\\pos(540,520)\\an5\\fs76\\frz-4\\fad(160,150)}AKI BANYU"),
    # ── B3 lewat telepon, ternyata Wowon
    (16.60,  19.90, "Kicker", "{\\pos(540,1010)\\an5\\fs46\\fad(220,160)}HANYA BICARA LEWAT TELEPON"),
    (20.50,  24.40, "Stamp", "{\\pos(540,520)\\an5\\fs58\\frz-4\\fad(160,150)}AKI BANYU ADALAH WOWON"),
    (25.00,  30.80, "Kicker", "{\\pos(540,1010)\\an5\\fs42\\fad(220,160)}DUA REKANNYA BARU TAHU SETELAH DITANGKAP"),
    (31.40,  36.10, "Kicker", "{\\pos(540,700)\\an5\\fs44\\fad(220,160)}TOKOH YANG TIDAK PERNAH MENUNJUKKAN DIRI"),
    # ── B411 pekerja migran
    (36.80,  40.10, "Stamp", "{\\pos(540,520)\\an5\\fs64\\frz-4\\fad(160,150)}11 PEKERJA MIGRAN"),
    (40.70,  44.20, "Kicker", "{\\pos(540,1010)\\an5\\fs46\\fad(220,160)}MENYETOR TIAP BULAN — BERTAHUN-TAHUN"),
    (44.80,  47.80, "Kicker", "{\\pos(540,700)\\an5\\fs48\\fad(220,160)}TAK SATU PUN MENERIMA UNTUNG"),
    (48.40,  51.40, "Kicker", "{\\pos(540,1010)\\an5\\fs50\\c&H002A2AD8&\\fad(220,160)}YANG BERTANYA: KAMU AKAN CELAKA"),
    # ── B5 penagih dihabisi
    (52.10,  55.40, "Kicker", "{\\pos(540,1010)\\an5\\fs48\\fad(220,160)}PENAGIH JANJI DIHABISI"),
    (56.00,  60.10, "Kicker", "{\\pos(540,700)\\an5\\fs46\\fad(220,160)}BEGITU PULA ANGGOTA KELUARGA"),
    # ── B6 vonis
    (60.80,  64.20, "Stamp", "{\\pos(540,520)\\an5\\fs72\\frz-4\\fad(160,150)}NOVEMBER 2023"),
    (64.70,  68.50, "Kicker", "{\\pos(540,700)\\an5\\fs50\\fad(220,160)}VONIS: PENJARA SEUMUR HIDUP"),
    # ── B7 kriminolog
    (69.10,  71.40, "Kicker", "{\\pos(540,1010)\\an5\\fs48\\fad(220,160)}KRIMINOLOG: LEBIH DARI 9?"),
    (71.80,  74.10, "Kicker", "{\\pos(540,700)\\an5\\fs50\\c&H002A2AD8&\\fad(220,160)}TAK ADA YANG TAHU PASTI"),
    # ── B8 debate hook
    (74.80,  78.40, "Stamp", "{\\pos(540,520)\\an5\\fs56\\frz-4\\fad(160,150)}AKI BANYU TIDAK PERNAH ADA"),
    (79.00,  84.70, "Kicker", "{\\pos(540,700)\\an5\\fs48\\c&H002A2AD8&\\fad(240,170)}PERCAYA JANJI YANG TIDAK BISA DICEK?"),
    # ── kartu penutup
    (85.40,  89.40, "Big", "{\\pos(540,640)\\an5\\fs110\\fad(260,0)}ODDCHAPTER"),
    (85.70,  89.40, "Kicker", "{\\pos(540,740)\\an5\\fs42\\c&H002A2AD8&\\fad(300,0)}KASUS NYATA · ARSIP ASLI"),
    (86.00,  89.40, "Credit", "{\\pos(540,1000)\\an5\\fs26\\c&H00D0D0D0&\\fad(360,0)}" + CREDITS),
]
