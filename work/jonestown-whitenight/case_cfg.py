"""Konfigurasi kasus AK-EP06 — Jonestown / "White Night" (Shortlist Batch 2 #1).

VO = VO PEMILIK apa adanya (vo_owner/vo_jonestown-whitenight.mp3,101,15 s,176 kata;
alignment faster-whisper). Tanpa TTS. END105,24 s (kartu penutup4,1 s).

Format: 8 beat adaptasi Curiosity Loop — dilema (B1) → komune & janji (B2) →
White Night (B3) → antre gelas merah (B4) → tes kesetiaan (B5) → sumpah
Leighton (B6) → fakta918/909 (B7) → "berhenti di mana?" (B8).

Aturan episode (CATATAN batch2): tanpa gore, tanpa metode rinci, tanpa foto
jenazah/TKP; angka korban hanya918/909; nada menghormati korban; footage stok
Coverr + label layar + kredit.
"""

SLUG = "jonestown-whitenight"
VO_FILE = "vo_owner/vo_jonestown-whitenight.mp3"
END = 105.24
OUT_NAME = "AK-EP06_jonestown-whitenight_short.mp4"
SRT_NAME = "AK-EP06.id.srt"
BED_BUILDER = "bed_jonestown.py"
CLIP_BG_BRIGHT = "-0.46"

IMAGES = {}

# work/jonestown-whitenight/footage/ → symlink bank footage/:
# (berkas, detik mulai, durasi tersedia)
CLIPS = {
    "CANDLE_A":       ("candle_dark__coverr-blurred-candles-in-the-dark-5231.mp4",   0.50, 8.00),
    "JUNGAL":         ("fog_forest_mountain__coverr-mountains-in-fanal-madeira-island-6802.mp4", 1.00, 8.00),
    "KATEDRAL_INT":   ("cathedral_interior__coverr-positano-cathedral-7425.mp4",      0.80, 8.00),
    "PATUNG_LIBERTY": ("statue_sculpture__coverr-the-statue-of-liberty-401.mp4",      0.60, 8.00),
    "BULAN":          ("moon_night_sky__user-ai-generation-0b4ZdNtmzT9q.mp4",        0.40, 6.00),
    "BAYANGAN":       ("shadow_walking__coverr-pov-walking-down-the-street-1894.mp4", 0.50, 6.00),
    "KORIDOR":        ("dark_corridor__coverr-scary-hallway-7141.mp4",               0.50, 6.00),
    "ASAP":           ("smoke_black_background__user-ai-generation-iaAaX0rR2kx7.mp4", 0.50, 6.00),
    "ANTRE":          ("crowd_slow_motion__coverr-crowded-bridge-8424.mp4",           1.00, 8.00),
    "LILIN_GELAP2":   ("candle_dark__coverr-candles-in-the-dark-4381.mp4",           1.00, 8.00),
    "MATA":           ("close_up_eye__coverr-ai-generated-close-up-of-a-pale-horses-eye.mp4", 0.50, 6.00),
    "JEMAAH":         ("crowd_slow_motion__coverr-live-music-concert-5249.mp4",       2.00, 8.00),
    "HUJAN":          ("rain_on_window_night__user-ai-generation-BCHZqmfTpSvX.mp4",   0.50, 6.00),
    "KATEDRAL_DOME":  ("cathedral_dome__coverr-a-view-of-the-domes-and-towers-of-the-jeronimos-monastery-1873.mp4", 0.50, 6.00),
    "JON_PORTRAIT":   ("portrait_painting__coverr-old-man-painting-a-portrait-8242.mp4", 0.50, 6.00),
    "TULIS_SURAT":    ("hand_writing_letter__coverr-handwriting-a-note-8044.mp4",     1.00, 8.00),
    "DIARY":          ("letters_paper__coverr-writing-in-a-diary-2746.mp4",           0.50, 6.00),
    "KORAN":          ("newspaper_printing__coverr-local-dutch-newspapers-8257.mp4",  0.50, 6.00),
    "BUKU":           ("stack_of_books__coverr-placing-books-on-a-desk-2325.mp4",     0.50, 8.00),
    "LILIN_GEREJA":   ("candle_flame__coverr-burning-church-candles-4154.mp4",        0.50, 6.00),
    "LILIN_HATI":     ("candle_flame__coverr-candles-in-a-heart-shape-1.mp4",         0.50, 6.00),
    "ANTRE2":         ("crowd_slow_motion__coverr-crowded-bridge-8424.mp4",           3.20, 8.00),
    "KORIDOR2":       ("dark_corridor__coverr-scary-hallway-7141.mp4",               2.00, 6.00),
}

TAG_STOK_C = "FOOTAGE STOK · COVERR"

BOX = {"box": (1020, 574)}
NIGHT = {"box": (1020, 574), "bg": "-0.66"}

# (mulai, selesai, klip, mode, z0, z1, opsi)
SHOTS = [
    # ── B1 dilema ekstrem (0,00–11,38)
    (0.00,    0.80, None, "black", 1.00, 1.00, {}),
    (0.80,    5.60, "CANDLE_A", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **NIGHT}),
    (5.60,   11.38, "JUNGAL", "clipfill", 1.00, 1.00, {"tag": TAG_STOK_C}),
    # ── B2 komune & janji (11,38–21,90)
    (11.38,  16.40, "KATEDRAL_INT", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    (16.40,  21.90, "PATUNG_LIBERTY", "clipfill", 1.00, 1.00, {"tag": TAG_STOK_C}),
    # ── B3 White Night (21,90–37,84)
    (21.90,  26.50, "BULAN", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **NIGHT}),
    (26.50,  31.00, "BAYANGAN", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    (31.00,  34.50, "KORIDOR", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **NIGHT}),
    (34.50,  37.84, "ASAP", "clipfill", 1.00, 1.00, {"tag": TAG_STOK_C}),
    # ── B4 antre gelas merah (37,84–55,26)
    (37.84,  42.40, "ANTRE", "clipfill", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (42.40,  46.90, "LILIN_GELAP2", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **NIGHT}),
    (46.90,  51.30, "MATA", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **NIGHT}),
    (51.30,  55.26, "JEMAAH", "clipfill", 1.00, 1.00, {"tag": TAG_STOK_C}),
    # ── B5 tes kesetiaan (55,26–67,98)
    (55.26,  59.60, "HUJAN", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **NIGHT}),
    (59.60,  63.90, "KATEDRAL_DOME", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    (63.90,  67.98, "JON_PORTRAIT", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    # ── B6 sumpah Leighton →18 November (67,98–84,18)
    (67.98,  72.60, "TULIS_SURAT", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    (72.60,  77.10, "DIARY", "clipfill", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (77.10,  81.00, "KORAN", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    (81.00,  84.18, "BUKU", "clipfill", 1.00, 1.00, {"tag": TAG_STOK_C}),
    # ── B7 fakta918/909 (84,18–97,72)
    (84.18,  88.80, "LILIN_GEREJA", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **NIGHT}),
    (88.80,  93.10, "LILIN_HATI", "clipfill", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (93.10,  97.72, "ANTRE2", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    # ── B8 debate hook (97,72–101,15)
    (97.72, 101.15, "KORIDOR2", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **NIGHT}),
    # ── kartu penutup (101,15–105,24)
    (101.15, 105.24, None, "black", 1.00, 1.00, {}),
]

KEYWORDS = {"JONESTOWN", "WHITE", "NIGHT", "918", "909", "45"}

# angka dieja di VO -> digit di caption; urutan frasa panjang dulu
NUM_PHRASES = [
    (["empat", "puluh", "lima"], "45"),
]

# potongan kata ASR yang harus disatukan
MERGE = [
    (["anak", "-anak"], "anak-anak"),
    (["masing", "-masing"], "Masing-masing"),
]

# ejaan nama yang dirapikan (ASR: "Johnstown")
WORD_FIX = {
    "johnstown": "Jonestown",
    "seluruh": "Seluruh",
}

CREDITS = ("Footage stok: Coverr\\N"
           "Sumber: Wikipedia · Jonestown Institute\\N"
           "Deborah Layton, Seductive Poison (1998)\\N"
           "@oddchapter7 · KASUS NYATA · ARSIP ASLI")

OVL = [
    # ── B1 dilema
    (1.20,    5.40, "Kicker", "{\\pos(540,700)\\an5\\fs52\\fad(240,170)}MEREKA DISURUH MINUM RACUN"),
    (6.00,   11.20, "Stamp", "{\\pos(540,520)\\an5\\fs76\\frz-4\\fad(160,150)}NAMANYA: JONESTOWN"),
    # ── B2 komune & janji
    (11.80,  16.20, "Kicker", "{\\pos(540,1010)\\an5\\fs48\\fad(220,160)}KOMUNE DI TENGAH HUTAN"),
    (16.80,  21.70, "Kicker", "{\\pos(540,700)\\an5\\fs50\\fad(220,160)}DIJANJIKAN SURGA TROPIS"),
    # ── B3 White Night
    (22.30,  26.30, "Stamp", "{\\pos(540,520)\\an5\\fs64\\frz-4\\fad(160,150)}SIRENE TENGAH MALAM"),
    (27.00,  30.80, "Kicker", "{\\pos(540,1010)\\an5\\fs46\\fad(220,160)}SELURUH WARGA DIBANGUNKAN"),
    (31.40,  34.30, "Kicker", "{\\pos(540,1010)\\an5\\fs46\\fad(220,160)}PENJAGA BERSENJATA DI SEKELILING"),
    (34.90,  37.70, "Stamp", "{\\pos(540,520)\\an5\\fs88\\frz-4\\fad(160,150)}WHITE NIGHT"),
    # ── B4 antre gelas merah
    (38.30,  42.20, "Kicker", "{\\pos(540,1010)\\an5\\fs46\\fad(220,160)}SEMUA ORANG DISURUH ANTRE"),
    (42.90,  46.70, "Kicker", "{\\pos(540,700)\\an5\\fs50\\c&H002A2AD8&\\fad(220,160)}SEGELAS CAIRAN MERAH"),
    (47.40,  51.10, "Kicker", "{\\pos(540,1010)\\an5\\fs46\\fad(220,160)}RACUN — MATI DALAM 45 MENIT"),
    (51.80,  55.10, "Kicker", "{\\pos(540,1010)\\an5\\fs44\\fad(220,160)}MEREKA MEMINUMNYA, LALU MENUNGGU"),
    # ── B5 tes kesetiaan
    (55.70,  59.40, "Stamp", "{\\pos(540,520)\\an5\\fs64\\frz-4\\fad(160,150)}45 MENIT BERLALU"),
    (60.10,  63.70, "Kicker", "{\\pos(540,1010)\\an5\\fs44\\fad(220,160)}ITU BUKAN RACUN — ITU TES KESETIAAN"),
    (64.30,  67.80, "Kicker", "{\\pos(540,700)\\an5\\fs50\\c&H002A2AD8&\\fad(220,160)}WAKTUNYA SUDAH DEKAT"),
    # ── B6 sumpah Leighton
    (68.40,  72.40, "Kicker", "{\\pos(540,1010)\\an5\\fs46\\fad(220,160)}PERNYATAAN DI BAWAH SUMPAH"),
    (73.00,  76.90, "Kicker", "{\\pos(540,1010)\\an5\\fs44\\fad(220,160)}DEBORAH LEIGHTON · MANTAN ANGGOTA"),
    (77.60,  80.80, "Stamp", "{\\pos(540,520)\\an5\\fs72\\frz-4\\fad(160,150)}18 NOVEMBER 1978"),
    (81.40,  84.00, "Kicker", "{\\pos(540,1010)\\an5\\fs48\\fad(220,160)}TIDAK ADA LAGI LATIHAN"),
    # ── B7 fakta918/909
    (84.70,  88.60, "Big", "{\\pos(540,620)\\an5\\fs150\\c&H002A2AD8&\\fad(200,150)}918"),
    (88.80,  92.80, "Kicker", "{\\pos(540,860)\\an5\\fs46\\c&H00E0ECF0&\\fad(200,150)}ORANG MENINGGAL HARI ITU"),
    (93.00,  97.60, "Kicker", "{\\pos(540,1010)\\an5\\fs44\\fad(220,160)}MENGUJI SAMPAI DI MANA MEREKA PATUH"),
    # ── B8 debate hook
    (98.00, 101.00, "Kicker", "{\\pos(540,700)\\an5\\fs56\\c&H002A2AD8&\\fad(240,170)}BERHENTI DI MANA?"),
    # ── kartu penutup
    (101.55, 105.24, "Big", "{\\pos(540,640)\\an5\\fs110\\fad(260,0)}ODDCHAPTER"),
    (101.85, 105.24, "Kicker", "{\\pos(540,740)\\an5\\fs42\\c&H002A2AD8&\\fad(300,0)}KASUS NYATA · ARSIP ASLI"),
    (102.15, 105.24, "Credit", "{\\pos(540,1000)\\an5\\fs26\\c&H00D0D0D0&\\fad(360,0)}" + CREDITS),
]
