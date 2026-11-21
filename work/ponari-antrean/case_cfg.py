"""Konfigurasi kasus AK-EP08 — Ponari: antrean yang tidak berhenti (Batch 2 #4).

VO = VO PEMILIK apa adanya (vo_owner/vo_ponari-antrean.mp3,78,81 s,152 kata;
ElevenLabs Riri Rida, alignment faster-whisper). Tanpa TTS. END82,90 s (kartu
penutup4,50 s).

Sudut: kemiskinan & akses kesehatan — antrean justru TIDAK berhenti setelah
praktik ditutup; Ponari korban eksploitasi. Nada hormat, tanpa nama korban,
tanpa mengejek keyakinan. ATURAN BARU21 Nov2026: semua klip16:9 render
cover-crop FULL LAYAR9:16 (default clip_filter; tanpa "window").
"""

SLUG = "ponari-antrean"
VO_FILE = "vo_owner/vo_ponari-antrean.mp3"
END = 82.90
OUT_NAME = "AK-EP08_ponari-antrean_short.mp4"
SRT_NAME = "AK-EP08.id.srt"
BED_BUILDER = "bed_ponari.py"

# still AI (tanpa orang): key -> (file, lebar, tinggi)
IMAGES = {
    "BATU":  ("stone_glass.jpg", 768, 1376),
    "DESA":  ("village_lane.jpg", 768, 1376),
    "SUMUR": ("well_water.jpg", 768, 1376),
}

# work/ponari-antrean/footage/ → symlink bank/:
# (berkas, detik mulai, durasi tersedia)
CLIPS = {
    "ANTRE1":       ("crowd_slow_motion__coverr-crowded-bridge-8424.mp4",   0.60, 8.00),
    "BAYANGAN":     ("shadow_walking__coverr-pov-walking-down-the-street-1894.mp4", 0.50, 6.00),
    "HUJAN":        ("rain_on_window_night__user-ai-generation-BCHZqmfTpSvX.mp4", 0.40, 6.00),
    "KATEDRAL":     ("cathedral_interior__coverr-positano-cathedral-7425.mp4", 0.80, 8.00),
    "JEMAAH":       ("crowd_slow_motion__coverr-live-music-concert-5249.mp4", 1.00, 8.00),
    "KOPER":        ("sb-ep02/s3_koper.mp4",                               0.40, 6.00),
    "MENUNGGU":     ("sb-ep02/s3_menunggu.mp4",                            0.50, 6.00),
    "ANTRE2":       ("crowd_slow_motion__coverr-crowded-bridge-8424.mp4",   3.20, 8.00),
    "LILIN1":       ("candle_dark__coverr-candles-in-the-dark-4381.mp4",    1.00, 8.00),
    "KORIDOR":      ("dark_corridor__coverr-scary-hallway-7141.mp4",        0.50, 6.00),
    "JEMAAH2":      ("crowd_slow_motion__coverr-live-music-concert-5249.mp4", 3.10, 8.00),
    "MATA":         ("close_up_eye__coverr-ai-generated-close-up-of-a-pale-horses-eye.mp4", 0.50, 6.00),
    "KORAN":        ("newspaper_printing__coverr-local-dutch-newspapers-8257.mp4", 0.40, 6.00),
    "TULIS":        ("hand_writing_letter__coverr-writing-a-note-4875.mp4", 0.50, 8.00),
    "WAJA_WARGA":   ("portrait_painting__coverr-old-man-painting-a-portrait-8242.mp4", 0.50, 6.00),
    "LILIN_GEREJA": ("candle_flame__coverr-burning-church-candles-4154.mp4", 0.40, 6.00),
    "HUJAN2":       ("rain_on_window_night__user-ai-generation-BCHZqmfTpSvX.mp4", 1.50, 6.00),
    "BULAN":        ("moon_night_sky__user-ai-generation-0b4ZdNtmzT9q.mp4", 0.40, 6.00),
    "KUPOLA":       ("cathedral_dome__coverr-a-view-of-the-domes-and-towers-of-the-jeronimos-monastery-1873.mp4", 0.40, 6.00),
    "DERMAKA":      ("sb-ep02/s8_dermaga.mp4",                             0.30, 6.00),
}

TAG_STOK_C = "FOOTAGE STOK · COVERR"

# (mulai, selesai, klip/still, mode, z0, z1, opsi)
# mode "clip" = footage cover-crop FULL LAYAR9:16 (aturan baru21 Nov2026)
SHOTS = [
    # ── B1 puluhan ribu nomor antrean (0,00–6,72)
    (0.00,    0.80, None, "black", 1.00, 1.00, {}),
    (0.80,    3.90, "ANTRE1", "clip", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (3.90,    6.72, "BATU", "fill", 1.04, 1.12, {}),
    # ── B2 Jombang2009, Ponari9 tahun (6,72–21,54)
    (6.72,   11.00, "DESA", "fill", 1.00, 1.08, {}),
    (11.00,  15.30, "BAYANGAN", "clip", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (15.30,  18.60, "HUJAN", "clip", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (18.60,  21.54, "KATEDRAL", "clip", 1.00, 1.00, {"tag": TAG_STOK_C}),
    # ── B3 Balongsari penuh sesak (21,54–33,34)
    (21.54,  25.60, "JEMAAH", "clip", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (25.60,  29.10, "KOPER", "clip", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (29.10,  33.34, "MENUNGGU", "clip", 1.00, 1.00, {"tag": TAG_STOK_C}),
    # ── B4 kerumunan menelan korban (33,34–41,00)
    (33.34,  36.10, "ANTRE2", "clip", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (36.10,  38.90, "LILIN1", "clip", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (38.90,  41.00, "KORIDOR", "clip", 1.00, 1.00, {"tag": TAG_STOK_C}),
    # ── B5 tidak pulang (41,00–52,64)
    (41.00,  45.80, "JEMAAH2", "clip", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (45.80,  49.00, "SUMUR", "fill", 1.04, 1.12, {}),
    (49.00,  52.64, "MATA", "clip", 1.00, 1.00, {"tag": TAG_STOK_C}),
    # ── B6 Kenapa? pengangguran70% (52,64–61,86)
    (52.64,  56.60, "KORAN", "clip", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (56.60,  59.40, "TULIS", "clip", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (59.40,  61.86, "WAJA_WARGA", "clip", 1.00, 1.00, {"tag": TAG_STOK_C}),
    # ── B7 korban kelima (61,86–69,14)
    (61.86,  64.90, "LILIN_GEREJA", "clip", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (64.90,  67.30, "HUJAN2", "clip", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (67.30,  69.14, "BULAN", "clip", 1.00, 1.00, {"tag": TAG_STOK_C}),
    # ── B8 debate hook (69,14–78,40)
    (69.14,  73.30, "KUPOLA", "clip", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (73.30,  78.40, "DERMAKA", "clip", 1.00, 1.00, {"tag": TAG_STOK_C}),
    # ── kartu penutup (78,40–82,90)
    (78.40,  82.90, None, "black", 1.00, 1.00, {}),
]

KEYWORDS = {"PONARI", "2009", "4", "70"}

NUM_PHRASES = [
    (["empat"], "4"),
]

MERGE = [
    (["antrian", "antrian"], "antrean"),
    (["orang", "-orang"], "orang-orang"),
]

WORD_FIX = {}

CREDITS = ("Footage stok: Coverr\\N"
           "Sumber: ANTARA · Inside Indonesia · Liputan6\\N"
           "@oddchapter7 · KASUS NYATA · ARSIP ASLI")

OVL = [
    # ── B1 antrean
    (1.10,    3.70, "Stamp", "{\\pos(540,520)\\an5\\fs56\\frz-4\\fad(160,150)}PULUHAN RIBU NOMOR ANTREAN"),
    (4.10,    6.50, "Kicker", "{\\pos(540,700)\\an5\\fs52\\fad(240,170)}SEGELAS AIR — SEBUAH BATU"),
    # ── B2 Jombang2009
    (7.20,   10.80, "Stamp", "{\\pos(540,520)\\an5\\fs72\\frz-4\\fad(160,150)}JOMBANG 2009"),
    (11.40,  15.10, "Kicker", "{\\pos(540,1010)\\an5\\fs48\\fad(220,160)}MUHAMMAD PONARI, 9 TAHUN"),
    (15.60,  18.40, "Kicker", "{\\pos(540,700)\\an5\\fs48\\fad(220,160)}BATU SETELAH TERSAMBAR PETIR"),
    (18.90,  21.40, "Kicker", "{\\pos(540,1010)\\an5\\fs44\\fad(220,160)}AIR CELUPAN BATU — BISA MENYEMBUHKAN"),
    # ── B3 Balongsari penuh sesak
    (22.00,  25.40, "Kicker", "{\\pos(540,1010)\\an5\\fs46\\fad(220,160)}DESA BALONGSARI PENUH SESAK"),
    (26.00,  28.90, "Kicker", "{\\pos(540,700)\\an5\\fs48\\fad(220,160)}DATANG DARI BERBAGAI KOTA"),
    (29.50,  33.20, "Kicker", "{\\pos(540,1010)\\an5\\fs42\\fad(220,160)}MENUNGGU DUA HARI — TIDUR DI RUMAH WARGA"),
    # ── B4 kerumunan menelan korban
    (33.80,  36.00, "Stamp", "{\\pos(540,520)\\an5\\fs56\\frz-4\\fad(160,150)}KERUMUNAN MENELAN KORBAN"),
    (36.30,  38.80, "Stamp", "{\\pos(540,520)\\an5\\fs80\\frz-4\\c&H002A2AD8&\\fad(160,150)}4 ORANG MENINGGAL"),
    (39.10,  40.90, "Kicker", "{\\pos(540,1010)\\an5\\fs48\\fad(220,160)}POLISI MENUTUP PRAKTIKNYA"),
    # ── B5 tidak pulang
    (41.50,  45.60, "Kicker", "{\\pos(540,700)\\an5\\fs48\\fad(220,160)}TAPI MEREKA TIDAK PULANG"),
    (46.10,  48.80, "Kicker", "{\\pos(540,1010)\\an5\\fs46\\fad(220,160)}RIBUAN TETAP MENUNGGU DI LUAR"),
    (49.40,  52.50, "Kicker", "{\\pos(540,1010)\\an5\\fs42\\fad(220,160)}MINUM AIR SUMUR — MENADAH AIR MANDI"),
    # ── B6 Kenapa?
    (53.00,  56.40, "Stamp", "{\\pos(540,520)\\an5\\fs76\\frz-4\\fad(160,150)}KENAPA?"),
    (56.90,  59.20, "Kicker", "{\\pos(540,700)\\an5\\fs54\\c&H002A2AD8&\\fad(220,160)}PENGANGGURAN 70 PERSEN"),
    (59.60,  61.70, "Kicker", "{\\pos(540,1010)\\an5\\fs50\\fad(220,160)}BEROBAT KE DOKTER... MAHAL"),
    # ── B7 korban kelima
    (62.30,  64.80, "Kicker", "{\\pos(540,1010)\\an5\\fs48\\fad(220,160)}AKHIR MARET — KORBAN KELIMA"),
    (65.20,  67.20, "Kicker", "{\\pos(540,700)\\an5\\fs48\\fad(220,160)}PEMUDA 19 TAHUN — KELELAHAN"),
    # ── B8 debate hook
    (69.60,  73.20, "Kicker", "{\\pos(540,1010)\\an5\\fs46\\fad(220,160)}KENAPA MEREKA PERCAYA SEBUAH BATU?"),
    (73.80,  78.30, "Kicker", "{\\pos(540,700)\\an5\\fs56\\c&H002A2AD8&\\fad(240,170)}MEREKA HARUS KE MANA?"),
    # ── kartu penutup
    (78.80,  82.90, "Big", "{\\pos(540,640)\\an5\\fs110\\fad(260,0)}ODDCHAPTER"),
    (79.10,  82.90, "Kicker", "{\\pos(540,740)\\an5\\fs42\\c&H002A2AD8&\\fad(300,0)}KASUS NYATA · ARSIP ASLI"),
    (79.40,  82.90, "Credit", "{\\pos(540,1000)\\an5\\fs26\\c&H00D0D0D0&\\fad(360,0)}" + CREDITS),
]
