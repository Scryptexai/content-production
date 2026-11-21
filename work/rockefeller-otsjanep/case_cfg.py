"""Konfigurasi kasus AK-EP07 — Michael Rockefeller & Otsjanep (Shortlist Batch 2 #3).

VO = VO PEMILIK apa adanya (vo_owner/vo_rockefeller-otsjanep.mp3,103,70 s,186 kata;
ElevenLabs Riri Rida, alignment faster-whisper). Tanpa TTS. END107,80 s (kartu
penutup4,54 s).

Sudut: kolonialisme & laporan yang dikubur — BUKAN sensasi kanibalisme. Aturan
episode (CATATAN shortlist): tanpa foto jenazah, nada hormat, angka dari VO
(5 pria Otsjanep1958; meninggal hukum1964). Footage: bank root + sb-ep02
(laut/kapal/pesawat); TIDAK memakai5 mp4 Drive ber-ID YouTube (provenansi tak
jelas = footage risiko).
"""

SLUG = "rockefeller-otsjanep"
VO_FILE = "vo_owner/vo_rockefeller-otsjanep.mp3"
END = 107.80
OUT_NAME = "AK-EP07_rockefeller-otsjanep_short.mp4"
SRT_NAME = "AK-EP07.id.srt"
BED_BUILDER = "bed_rockefeller.py"
CLIP_BG_BRIGHT = "-0.46"

IMAGES = {}

# work/rockefeller-otsjanep/footage/ → symlink bank/:
# (berkas, detik mulai, durasi tersedia)
CLIPS = {
    "LAUT_LUAS":    ("sb-ep02/s9_laut_luas.mp4",                     0.30, 6.00),
    "PERAHU":       ("sb-ep02/s5_perahu.mp4",                        0.40, 6.00),
    "STATUE":       ("statue_sculpture__coverr-the-statue-of-liberty-401.mp4", 0.60, 8.00),
    "KAPAL":        ("sb-ep02/s5_kapal_laut.mp4",                    0.30, 6.00),
    "OMBAK_KARANG": ("sb-ep02/s5_ombak_karang.mp4",                  0.15, 6.00),
    "PESAWAT":      ("sb-ep02/s3_pesawat_di_apron.mp4",              0.40, 6.00),
    "KABIN":        ("sb-ep02/s2_awan_dari_kabin.mp4",               0.30, 6.00),
    "MENUNGGU":     ("sb-ep02/s3_menunggu.mp4",                      0.40, 6.00),
    "MALAM_LAUT":   ("sb-ep02/s1_ombak_malam.mp4",                   0.40, 6.00),
    "BADAI":        ("sb-ep02/storm_waves_sea__coverr-large-waves-crashing-on-the-rocky-shore-8765.mp4", 0.40, 6.00),
    "SURAT1":       ("hand_writing_letter__coverr-handwriting-a-note-8044.mp4", 0.80, 8.00),
    "ALKITAB":      ("old_book_pages__coverr-reading-the-bible-5396.mp4", 0.50, 6.00),
    "BATU_LAUT":    ("sb-ep02/s6_batu_laut.mp4",                     0.30, 6.00),
    "MERCUSUAR":    ("sb-ep02/s5_mercusuar_badai.mp4",               0.40, 6.00),
    "KORIDOR":      ("dark_corridor__coverr-scary-hallway-7141.mp4", 0.50, 6.00),
    "MATA":         ("close_up_eye__coverr-ai-generated-close-up-of-a-pale-horses-eye.mp4", 0.50, 6.00),
    "OMBAK_BATU":   ("sb-ep02/s6_ombak_batu.mp4",                    0.30, 6.00),
    "SURAT2":       ("hand_writing_letter__coverr-writing-a-note-4875.mp4", 0.50, 8.00),
    "KORAN":        ("newspaper_printing__coverr-local-dutch-newspapers-8257.mp4", 0.50, 6.00),
    "HALAMAN":      ("old_book_pages__coverr-flicking-through-bible-pages-3558.mp4", 0.50, 8.00),
    "BAYANGAN":     ("shadow_walking__coverr-pov-walking-down-the-street-1894.mp4", 0.50, 6.00),
    "KAPAL_JAUH":   ("sb-ep02/s5_kapal_kejauhan.mp4",                0.30, 6.00),
    "DERMAKA":      ("sb-ep02/s8_dermaga.mp4",                       0.40, 6.00),
    "BULAN":        ("moon_night_sky__user-ai-generation-0b4ZdNtmzT9q.mp4", 0.40, 6.00),
    "DARAT_LAUT":   ("sb-ep02/s9_darat_di_laut.mp4",                 0.30, 6.00),
    "OMBAK_BESAR":  ("sb-ep02/s5_ombak_besar.mp4",                   0.30, 6.00),
}

TAG_STOK_C = "FOOTAGE STOK · COVERR"

BOX = {"box": (1020, 574)}
NIGHT = {"box": (1020, 574), "bg": "-0.66"}

# (mulai, selesai, klip, mode, z0, z1, opsi)
SHOTS = [
    # ── B1 tiga titik di laut (0,00–9,64)
    (0.00,    0.80, None, "black", 1.00, 1.00, {}),
    (0.80,    5.10, "LAUT_LUAS", "clipfill", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (5.10,    9.64, "PERAHU", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    # ── B2 Michael Rockefeller (9,64–24,78)
    (9.64,   14.20, "STATUE", "clipfill", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (14.20,  19.00, "KAPAL", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    (19.00,  24.78, "OMBAK_KARANG", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **NIGHT}),
    # ── B3 pencarian besar (24,78–43,26)
    (24.78,  29.10, "PESAWAT", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    (29.10,  33.40, "KABIN", "clipfill", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (33.40,  37.60, "MENUNGGU", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    (37.60,  40.50, "MALAM_LAUT", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **NIGHT}),
    (40.50,  43.26, "BADAI", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **NIGHT}),
    # ── B4 pengakuan Otsjanep (43,26–54,32)
    (43.26,  48.00, "SURAT1", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    (48.00,  51.60, "ALKITAB", "clipfill", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (51.60,  54.32, "BATU_LAUT", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    # ── B5 dendam lama (54,32–68,62)
    (54.32,  58.90, "MERCUSUAR", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **NIGHT}),
    (58.90,  63.10, "KORIDOR", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **NIGHT}),
    (63.10,  66.00, "MATA", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **NIGHT}),
    (66.00,  68.62, "OMBAK_BATU", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    # ── B6 laporan dikubur (68,62–83,06)
    (68.62,  73.20, "SURAT2", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    (73.20,  77.60, "KORAN", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    (77.60,  80.60, "HALAMAN", "clipfill", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (80.60,  83.06, "BAYANGAN", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    # ── B7 tanpa bukti,1964 (83,06–96,10)
    (83.06,  87.80, "KAPAL_JAUH", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **BOX}),
    (87.80,  92.00, "DERMAKA", "clipfill", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (92.00,  96.10, "BULAN", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **NIGHT}),
    # ── B8 debate hook (96,10–103,26)
    (96.10, 100.00, "DARAT_LAUT", "clipfill", 1.00, 1.00, {"tag": TAG_STOK_C}),
    (100.00, 103.26, "OMBAK_BESAR", "clip", 1.00, 1.00, {"tag": TAG_STOK_C, **NIGHT}),
    # ── kartu penutup (103,26–107,80)
    (103.26, 107.80, None, "black", 1.00, 1.00, {}),
]

KEYWORDS = {"ROCKEFELLER", "OTSJANEP", "1961", "1964"}

# angka dieja di VO -> digit di caption; frasa panjang dulu
NUM_PHRASES = [
    (["sepuluh", "hari"], "10 hari"),
    (["lima", "pria"], "5 pria"),
]

# potongan kata ASR yang harus disatukan (kosong bila tak ada)
MERGE = []

# ejaan nama yang dirapikan (ASR: jerikan/misyonaris/Otsjaneb/Karl Hofmann)
WORD_FIX = {
    "jerikan": "jeriken",
    "misyonaris": "misionaris",
    "otsjaneb": "Otsjanep",
    "karl": "Carl",
    "hofmann": "Hoffman",
}

CREDITS = ("Footage stok: Coverr\\N"
           "Sumber: Wikipedia · Carl Hoffman, Savage Harvest (2014)\\N"
           "Stichting Papua Erfgoed · KITLV\\N"
           "@oddchapter7 · KASUS NYATA · ARSIP ASLI")

OVL = [
    # ── B1 tiga titik di laut
    (1.10,    4.90, "Stamp", "{\\pos(540,520)\\an5\\fs64\\frz-4\\fad(160,150)}TIGA TITIK DI LAUT"),
    (5.40,    9.40, "Kicker", "{\\pos(540,700)\\an5\\fs52\\fad(240,170)}DUA JERIKEN — DAN SATU KEPALA"),
    # ── B2 Michael Rockefeller
    (10.10,  14.00, "Kicker", "{\\pos(540,1010)\\an5\\fs48\\fad(220,160)}MICHAEL ROCKEFELLER, 23"),
    (14.60,  18.80, "Kicker", "{\\pos(540,700)\\an5\\fs50\\fad(220,160)}PUTRA GUBERNUR NEW YORK"),
    (19.40,  24.50, "Stamp", "{\\pos(540,520)\\an5\\fs68\\frz-4\\fad(160,150)}NOVEMBER 1961"),
    # ── B3 pencarian besar
    (25.20,  28.90, "Kicker", "{\\pos(540,1010)\\an5\\fs46\\fad(220,160)}PENCARIAN: PESAWAT & HELIKOPTER"),
    (29.50,  33.20, "Kicker", "{\\pos(540,1010)\\an5\\fs46\\fad(220,160)}AMERIKA MENAWARKAN ARMADANYA"),
    (33.80,  37.40, "Kicker", "{\\pos(540,700)\\an5\\fs48\\fad(220,160)}SEPULUH HARI — LALU DIHENTIKAN"),
    (38.00,  40.30, "Kicker", "{\\pos(540,1010)\\an5\\fs46\\c&H002A2AD8&\\fad(220,160)}TIDAK ADA JASAD"),
    (40.60,  43.10, "Kicker", "{\\pos(540,1010)\\an5\\fs46\\fad(220,160)}TENGGELAM — ATAU HEWAN LAUT"),
    # ── B4 pengakuan Otsjanep
    (43.70,  47.80, "Kicker", "{\\pos(540,1010)\\an5\\fs46\\fad(220,160)}SEBULAN KEMUDIAN — PENGAKUAN"),
    (48.30,  51.40, "Stamp", "{\\pos(540,520)\\an5\\fs72\\frz-4\\fad(160,150)}IA DIBUNUH"),
    (51.80,  54.20, "Kicker", "{\\pos(540,700)\\an5\\fs48\\fad(220,160)}DESA OT SJANEP"),
    # ── B5 dendam lama
    (54.80,  58.70, "Kicker", "{\\pos(540,1010)\\an5\\fs46\\fad(220,160)}BUNUHANNYA BUKAN SOAL MICHAEL"),
    (59.30,  62.90, "Stamp", "{\\pos(540,520)\\an5\\fs68\\frz-4\\fad(160,150)}5 PRIA OT SJANEP"),
    (63.40,  65.80, "Kicker", "{\\pos(540,700)\\an5\\fs48\\c&H002A2AD8&\\fad(220,160)}DENDAM LAMA"),
    (66.20,  68.50, "Kicker", "{\\pos(540,1010)\\an5\\fs46\\fad(220,160)}IA DATANG KE DESA ITU"),
    # ── B6 laporan dikubur
    (69.10,  73.00, "Kicker", "{\\pos(540,1010)\\an5\\fs46\\fad(220,160)}LAPORAN ITU DITULIS, DIKIRIM..."),
    (73.60,  77.40, "Stamp", "{\\pos(540,520)\\an5\\fs68\\frz-4\\fad(160,150)}LALU DIKUBUR"),
    (78.00,  80.40, "Kicker", "{\\pos(540,700)\\an5\\fs48\\fad(220,160)}MENURUT CARL HOFFMAN"),
    (80.70,  82.90, "Kicker", "{\\pos(540,1010)\\an5\\fs46\\fad(220,160)}BELANDA TAK MAU CITRANYA RUSAK"),
    # ── B7 tanpa bukti,1964
    (83.50,  87.60, "Kicker", "{\\pos(540,1010)\\an5\\fs46\\fad(220,160)}TIDAK ADA BUKTI YANG MENJAWAB"),
    (88.20,  91.80, "Kicker", "{\\pos(540,700)\\an5\\fs44\\fad(220,160)}KELUARGA MEYAKINI IA TENGGELAM"),
    (92.30,  95.90, "Stamp", "{\\pos(540,520)\\an5\\fs72\\frz-4\\fad(160,150)}MENINGGAL HUKUM 1964"),
    # ── B8 debate hook
    (96.60,  99.80, "Kicker", "{\\pos(540,1010)\\an5\\fs46\\fad(220,160)}APA YANG TERJADI DI LAUT?"),
    (100.10, 103.10, "Kicker", "{\\pos(540,700)\\an5\\fs56\\c&H002A2AD8&\\fad(240,170)}SIAPA YANG LEBIH NYAMAN?"),
    # ── kartu penutup
    (103.70, 107.80, "Big", "{\\pos(540,640)\\an5\\fs110\\fad(260,0)}ODDCHAPTER"),
    (104.00, 107.80, "Kicker", "{\\pos(540,740)\\an5\\fs42\\c&H002A2AD8&\\fad(300,0)}KASUS NYATA · ARSIP ASLI"),
    (104.30, 107.80, "Credit", "{\\pos(540,1000)\\an5\\fs26\\c&H00D0D0D0&\\fad(360,0)}" + CREDITS),
]
