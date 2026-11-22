"""Konfigurasi OS-EP03 — Trompet malaikat (Seneca Guns).

VO = VO PEMILIK apa adanya (vo_owner/vo_trompet-malaikat.mp3,205,64 s; SRT
ElevenLabs46 cue — teks sudah diperbaiki: sangkakala/malaikat Israfil/ratusan
tahun/Dan Seneca/gempa/seismograf/dst), alignment cue → kata proporsional →
vo_alignment.json,443 kata. END =210,68 s (VO + outro animasi5 dtk) →
>3 menit → master dipecah2 part <3 menit (keputusan pemilik, seperti EP02).
Format: feed vertikal9:16.

Koreksi pemilik22 Nov (00G): footage Coverr spesifik per section (39 klip
BARU di footage/os-ep03 — nol reuse lintas episode, dicek otomatis saat picks)
→ foto AI hanya untuk yang tak mungkin difoto (4 still) → source document =
peta OSM (kredit terbakar di render MapZoom) → tidak ada section yang hanya
foto.

Shot peta (koreksi22 Nov) —3 job, sinkron narasi:
  MAP-A42,94–48,02 zoom AS timur → Dan Seneca, NY ("Seneca Guns… Dan
    Seneca, New York"), headline SENECA GUNS.
  MAP-B48,02–53,39 zona pesisir NC·SC·Virginia ("sepanjang pesisir North
    Carolina, South Carolina, serta Virginia").
  MAP-C77,60–84,00 zoom Charleston, SC ("gempa besar mengguncang
    Charleston"), headline1886. Fakta jarak tidak ada → tanpa garis berlabel.
Klip map mode raw (tanpa CLIP_POST grade).
"""

SLUG = "trompet-malaikat"
VO_FILE = "vo_owner/vo_trompet-malaikat.mp3"
END = 210.68
OUT_NAME = "OS-EP03_trompet-malaikat_feed.mp4"
SRT_NAME = "OS-EP03.id.srt"

# foto AI: key -> (file, lebar, tinggi)
IMAGES = {
    # adegan tak mungkin difoto (tanpa orang)
    "LANGIT":      ("hook_langit_trompet.png", 1408, 768),
    "CHARLESTON":  ("charleston1886.png",      1408, 768),
    "SEISMOGRAF":  ("seismograf.png",          1408, 768),
    "METEOR":      ("meteor_sonik.png",        1408, 768),
    # source document (00G butir4) — peta asli via MAP-A/B/C (klip raw),
    # kredit "© OpenStreetMap contributors" terbakar di render MapZoom.
}

# footage/os-ep03/ (39 klip hasil fetch-footage,6,00 s masing-masing; cs+dur≤6)
CLIPS = {
    "S1_CLOUDS_ROAD":   ("os-ep03/s1_clouds_road.mp4",        0.00, 6.00),
    "S1_TIMELAPSE_NT":  ("os-ep03/s1_timelapse_night.mp4",    0.00, 6.00),
    "S1_CLOUDS_PLANE":  ("os-ep03/s1_clouds_plane.mp4",       0.00, 6.00),
    "S1_MARINA":        ("os-ep03/s1_marina.mp4",             0.00, 6.00),
    "S2_MIC_SWING":     ("os-ep03/s2_mic_swing.mp4",          0.00, 6.00),
    "S2_CAR_LIGHTS":    ("os-ep03/s2_car_lights.mp4",         0.00, 6.00),
    "S3_USA_FLAG":      ("os-ep03/s3_usa_flag.mp4",           0.00, 6.00),
    "S3_NY_TRAFFIC":    ("os-ep03/s3_ny_traffic.mp4",         0.00, 6.00),
    "S5_CURTAIN":       ("os-ep03/s5_curtain.mp4",            0.00, 6.00),
    "S5_HOUSE_LAKE":    ("os-ep03/s5_house_lake.mp4",         0.00, 6.00),
    "S6_WAVES_CALM":    ("os-ep03/s6_waves_calm.mp4",         0.00, 6.00),
    "S6_YACHTS":        ("os-ep03/s6_yachts.mp4",             0.00, 6.00),
    "S6_SEA_BRIDGE":    ("os-ep03/s6_sea_bridge.mp4",         0.00, 6.00),
    "S7_BCN_STREETS":   ("os-ep03/s7_bcn_streets.mp4",        0.00, 6.00),
    "S7_RUINS":         ("os-ep03/s7_ruins.mp4",              0.00, 6.00),
    "S7_WINDOW_BRANCH": ("os-ep03/s7_window_branch.mp4",      0.00, 6.00),
    "S8_NEWSPAPER_Q":   ("os-ep03/s8_newspaper_queue.mp4",    0.00, 6.00),
    "S8_NEWS_SCROLL":   ("os-ep03/s8_news_scroll.mp4",        0.00, 6.00),
    "S8_CLOCK":         ("os-ep03/s8_grand_central_clock.mp4",0.00, 6.00),
    "S9_DARAGA":        ("os-ep03/s9_daraga_church.mp4",      0.00, 6.00),
    "S9_JERONIMOS":     ("os-ep03/s9_jeronimos.mp4",          0.00, 6.00),
    "S9_JERONIMOS_ARCH":("os-ep03/s9_jeronimos_arch.mp4",     0.00, 6.00),
    "S10_GUITAR":       ("os-ep03/s10_guitar_strings.mp4",    0.00, 6.00),
    "S10_RECORD":       ("os-ep03/s10_record_player.mp4",     0.00, 6.00),
    "S10_MIC_DROP":     ("os-ep03/s10_mic_drop.mp4",          0.00, 6.00),
    "S11_AIRPLANE":     ("os-ep03/s11_airplane.mp4",          0.00, 6.00),
    "S11_ROCKET":       ("os-ep03/s11_rocket.mp4",            0.00, 6.00),
    "S11_SNOW":         ("os-ep03/s11_snow_branch.mp4",       0.00, 6.00),
    "S12_HORIZON":      ("os-ep03/s12_horizon.mp4",           0.00, 6.00),
    "S12_PARK_TL":      ("os-ep03/s12_park_tl.mp4",           0.00, 6.00),
    "S13_NEWS_MAN":     ("os-ep03/s13_newspaper_man.mp4",     0.00, 6.00),
    "S13_OLDMAN_PARK":  ("os-ep03/s13_oldman_park.mp4",       0.00, 6.00),
    "S13_OLDMAN_WRITE": ("os-ep03/s13_oldman_writing.mp4",    0.00, 6.00),
    "S14_FOG_WOODS":    ("os-ep03/s14_fog_woods.mp4",         0.00, 6.00),
    "S15_CITY_NIGHT":   ("os-ep03/s15_city_night.mp4",        0.00, 6.00),
    "S15_EVENING":      ("os-ep03/s15_evening_city.mp4",      0.00, 6.00),
    "S16_STREETS_SS":   ("os-ep03/s16_streets_sunset.mp4",    0.00, 6.00),
    "S16_TREES_WIND":   ("os-ep03/s16_trees_wind.mp4",        0.00, 6.00),
    "S16_SUN_COAST":    ("os-ep03/s16_sun_coast.mp4",         0.00, 6.00),
    # shot peta Remotion (render scripts/render-mapzoom.mjs → salin ke sini)
    "MAP_A": ("os-ep03/map_seneca_ny.mp4",        0.00, 5.08),
    "MAP_B": ("os-ep03/map_carolina_coast.mp4",   0.00, 5.37),
    "MAP_C": ("os-ep03/map_charleston_1886.mp4",  0.00, 6.40),
}

TAG_STOK_C = "FOOTAGE STOK · COVERR"

# (mulai, selesai, klip/still, mode, z0, z1, opsi)
# mode "clip" = footage cover-crop FULL LAYAR9:16 (aturan21 Nov2026)
SHOTS = [
    (0.00,    0.31, None, "black", 1.00, 1.00, {}),
    # ── S1 hook: suara trompet dari langit (0,31–26,77)
    (0.31,    4.60, "LANGIT", "fill", 1.00, 1.10, {}),
    (4.60,    9.60, "S1_CLOUDS_ROAD", "clip", 1.00, 1.04, {"tag": TAG_STOK_C}),
    (9.60,   14.60, "S1_TIMELAPSE_NT", "clip", 1.00, 1.05, {"tag": TAG_STOK_C}),
    (14.60,  19.60, "S1_CLOUDS_PLANE", "clip", 1.00, 1.04, {"tag": TAG_STOK_C}),
    (19.60,  24.00, "S1_MARINA", "clip", 1.00, 1.03, {"tag": TAG_STOK_C}),
    (24.00,  26.77, "S1_CLOUDS_PLANE", "clip", 1.20, 1.23, {"tag": TAG_STOK_C}),
    # ── S2 CTA like (26,77–33,83)
    (26.77,  31.00, "S2_MIC_SWING", "clip", 1.00, 1.04, {"tag": TAG_STOK_C}),
    (31.00,  33.83, "S2_CAR_LIGHTS", "clip", 1.00, 1.03, {"tag": TAG_STOK_C}),
    # ── S3 bukan fiksi + Seneca Guns (33,83–42,94)
    (33.83,  38.40, "S3_USA_FLAG", "clip", 1.00, 1.04, {"tag": TAG_STOK_C}),
    (38.40,  42.94, "S3_NY_TRAFFIC", "clip", 1.00, 1.05, {"tag": TAG_STOK_C}),
    # ── S4 lokasi: Dan Seneca NY + pesisir (42,94–53,39) — MAP-A/B
    (42.94,  48.02, "MAP_A", "clip", 1.00, 1.00, {"raw": True}),
    (48.02,  53.39, "MAP_B", "clip", 1.00, 1.00, {"raw": True}),
    # ── S5 deskripsi suara: meriam jauh / rumah bergetar (53,39–62,55)
    (53.39,  58.00, "S5_CURTAIN", "clip", 1.00, 1.04, {"tag": TAG_STOK_C}),
    (58.00,  62.55, "S5_HOUSE_LAKE", "clip", 1.00, 1.05, {"tag": TAG_STOK_C}),
    # ── S6 negasi: perang/kapal/runtuh/badai (62,55–73,82)
    (62.55,  67.00, "S6_WAVES_CALM", "clip", 1.00, 1.04, {"tag": TAG_STOK_C}),
    (67.00,  70.40, "S6_YACHTS", "clip", 1.00, 1.03, {"tag": TAG_STOK_C}),
    (70.40,  73.82, "S6_SEA_BRIDGE", "clip", 1.00, 1.03, {"tag": TAG_STOK_C}),
    # ── S7 Charleston1886 (73,82–92,18) — foto + MAP-C
    (73.82,  77.60, "CHARLESTON", "fill", 1.00, 1.10, {}),
    (77.60,  84.00, "MAP_C", "clip", 1.00, 1.00, {"raw": True}),
    (84.00,  88.40, "S7_RUINS", "clip", 1.00, 1.04, {"tag": TAG_STOK_C}),
    (88.40,  92.18, "S7_WINDOW_BRANCH", "clip", 1.00, 1.03, {"tag": TAG_STOK_C}),
    # ── S8 masa itu: tanpa seismograf/radar (92,18–110,55)
    (92.18,  96.80, "S7_BCN_STREETS", "clip", 1.00, 1.04, {"tag": TAG_STOK_C}),
    (96.80, 101.40, "S8_NEWSPAPER_Q", "clip", 1.00, 1.04, {"tag": TAG_STOK_C}),
    (101.40, 106.00, "S8_CLOCK", "clip", 1.00, 1.03, {"tag": TAG_STOK_C}),
    (106.00, 110.55, "S8_NEWS_SCROLL", "clip", 1.00, 1.05, {"tag": TAG_STOK_C}),
    # ── S9 jadi pertanda: suara malaikat (110,55–121,36)
    (110.55, 114.00, "S9_DARAGA", "clip", 1.00, 1.03, {"tag": TAG_STOK_C}),
    (114.00, 118.00, "S9_JERONIMOS", "clip", 1.00, 1.04, {"tag": TAG_STOK_C}),
    (118.00, 121.36, "S9_JERONIMOS_ARCH", "clip", 1.00, 1.03, {"tag": TAG_STOK_C}),
    # ── S10 gempa dangkal + frekuensi (121,36–138,99) — foto seismograf
    (121.36, 126.00, "SEISMOGRAF", "fill", 1.00, 1.10, {}),
    (126.00, 131.00, "S10_GUITAR", "clip", 1.00, 1.05, {"tag": TAG_STOK_C}),
    (131.00, 135.20, "S10_RECORD", "clip", 1.00, 1.04, {"tag": TAG_STOK_C}),
    (135.20, 138.99, "S10_MIC_DROP", "clip", 1.00, 1.03, {"tag": TAG_STOK_C}),
    # ── S11 penyebab lain (138,99–149,95) — foto meteor
    (138.99, 143.00, "METEOR", "fill", 1.00, 1.10, {}),
    (143.00, 145.70, "S11_ROCKET", "clip", 1.00, 1.03, {"tag": TAG_STOK_C}),
    (145.70, 147.90, "S11_AIRPLANE", "clip", 1.00, 1.02, {"tag": TAG_STOK_C}),
    (147.90, 149.95, "S11_SNOW", "clip", 1.00, 1.02, {"tag": TAG_STOK_C}),
    # ── S12 ragu + bagian menarik (149,95–160,19)
    (149.95, 154.90, "S12_HORIZON", "clip", 1.00, 1.04, {"tag": TAG_STOK_C}),
    (154.90, 160.19, "S12_PARK_TL", "clip", 1.00, 1.05, {"tag": TAG_STOK_C}),
    # ── S13 tafsir vs laporan asli (160,19–178,35)
    (160.19, 164.80, "S13_NEWS_MAN", "clip", 1.00, 1.04, {"tag": TAG_STOK_C}),
    (164.80, 169.40, "S13_OLDMAN_PARK", "clip", 1.00, 1.04, {"tag": TAG_STOK_C}),
    (169.40, 174.00, "S13_OLDMAN_WRITE", "clip", 1.00, 1.04, {"tag": TAG_STOK_C}),
    (174.00, 178.35, "S7_BCN_STREETS", "clip", 1.30, 1.34, {"tag": TAG_STOK_C}),
    # ── S14 batas klaim (178,35–182,84)
    (178.35, 182.84, "S14_FOG_WOODS", "clip", 1.00, 1.04, {"tag": TAG_STOK_C}),
    # ── S15 yang tahu (182,84–193,30)
    (182.84, 187.60, "S15_CITY_NIGHT", "clip", 1.00, 1.04, {"tag": TAG_STOK_C}),
    (187.60, 193.30, "S15_EVENING", "clip", 1.00, 1.05, {"tag": TAG_STOK_C}),
    # ── S16 CTA komentar (193,30–205,68)
    (193.30, 197.90, "S16_STREETS_SS", "clip", 1.00, 1.04, {"tag": TAG_STOK_C}),
    (197.90, 201.80, "S16_TREES_WIND", "clip", 1.00, 1.04, {"tag": TAG_STOK_C}),
    (201.80, 205.68, "S16_SUN_COAST", "clip", 1.00, 1.03, {"tag": TAG_STOK_C}),
    # ── outro animasi brand (205,68–210,68)
    (205.68, 210.68, None, "outro", 1.00, 1.00, {}),
]

KEYWORDS = {"SENECA", "GUNS", "CHARLESTON", "1886", "KIAMAT", "ISRAFIL",
            "SONIK", "SEISMOGRAF", "SANGKAKALA"}

NUM_PHRASES = []

MERGE = []

# teks sumber sudah diperbaiki di vo_elevenlabs.srt sebelum alignment
WORD_FIX = {}

CREDITS = ("Footage stok: Coverr\\N"
           "Peta: \\Nc OpenStreetMap contributors\\N"
           "@oddchapter7 · FENOMENA NYATA · SENECA GUNS 1886")

OVL = [
    # ── S1 hook
    (1.10,    5.60, "Stamp", "{\\pos(540,520)\\an5\\fs56\\frz-4\\fad(160,150)}SUARA TROMPET DARI LANGIT"),
    (12.90,  17.00, "Kicker", "{\\pos(540,1010)\\an5\\fs46\\fad(220,160)}TIDAK ADA PESAWAT · TIDAK ADA MERIAM"),
    (20.00,  24.00, "Kicker", "{\\pos(540,700)\\an5\\fs44\\fad(220,160)}TANDA KIAMAT ATAU SUARA MALAIKAT?"),
    # ── S2 CTA like
    (27.20,  33.60, "Kicker", "{\\pos(540,1010)\\an5\\fs44\\fad(220,160)}PERNAH DENGAR SUARA ANEH DARI LANGIT?"),
    # ── S3 fakta
    (34.30,  38.30, "Stamp", "{\\pos(540,520)\\an5\\fs54\\frz-4\\fad(160,150)}BUKAN REKAMAN FIKSI"),
    (39.00,  42.80, "Kicker", "{\\pos(540,1010)\\an5\\fs46\\fad(220,160)}LAPORAN RATUSAN TAHUN · SENECA GUNS"),
    # ── S4: MAP-A/B punya headline sendiri
    # ── S5 deskripsi
    (54.00,  58.00, "Kicker", "{\\pos(540,1010)\\an5\\fs44\\fad(220,160)}SUARA MERIAM JAUH · GEMURUH PANJANG"),
    (59.00,  62.40, "Stamp", "{\\pos(540,520)\\an5\\fs58\\frz-4\\fad(160,150)}RUMAH BERGETAR"),
    # ── S6 negasi
    (63.00,  67.20, "Kicker", "{\\pos(540,1010)\\an5\\fs44\\fad(220,160)}TANPA PERANG · TANPA KAPAL MELEDAK"),
    (68.00,  73.70, "Kicker", "{\\pos(540,700)\\an5\\fs44\\fad(220,160)}TANPA BANGUNAN RUNTUH · TANPA BADAI"),
    # ── S7 Charleston1886
    (74.30,  77.40, "Stamp", "{\\pos(540,520)\\an5\\fs60\\frz-4\\fad(160,150)}TAHUN 1886"),
    (84.40,  88.20, "Kicker", "{\\pos(540,1010)\\an5\\fs44\\fad(220,160)}GEMURUH + DENTUMAN BERSAMA GEMPA"),
    (88.60,  92.00, "Kicker", "{\\pos(540,700)\\an5\\fs44\\fad(220,160)}GEMPA SUSULAN JUGA BERSUARA"),
    # ── S8 masa tanpa alat
    (93.00,  97.00, "Stamp", "{\\pos(540,520)\\an5\\fs52\\frz-4\\fad(160,150)}TANPA SEISMOGRAF · TANPA RADAR"),
    (102.00, 106.00, "Kicker", "{\\pos(540,1010)\\an5\\fs44\\fad(220,160)}TAK BISA BEDAKAN UDARA / BATUAN"),
    (107.00, 110.40, "Kicker", "{\\pos(540,700)\\an5\\fs46\\fad(220,160)}SUARA JADI PERTANDA"),
    # ── S9 pertanda
    (111.00, 115.30, "Stamp", "{\\pos(540,520)\\an5\\fs56\\frz-4\\fad(160,150)}SUARA MALAIKAT?"),
    (116.00, 121.20, "Kicker", "{\\pos(540,1010)\\an5\\fs46\\fad(220,160)}PERINGATAN DARI DUNIA LAIN"),
    # ── S10 gempa dangkal
    (121.80, 125.80, "Stamp", "{\\pos(540,520)\\an5\\fs56\\frz-4\\fad(160,150)}SEISMOGRAF"),
    (126.50, 131.00, "Kicker", "{\\pos(540,1010)\\an5\\fs46\\fad(220,160)}GETARAN FREKUENSI TINGGI"),
    (132.00, 135.10, "Kicker", "{\\pos(540,700)\\an5\\fs44\\fad(220,160)}GUNCANGAN HAMPIR TAK TERSA"),
    # ── S11 penyebab lain
    (139.40, 142.90, "Stamp", "{\\pos(540,520)\\an5\\fs54\\frz-4\\fad(160,150)}PENYEBAB LAIN?"),
    (143.40, 147.80, "Kicker", "{\\pos(540,1010)\\an5\\fs44\\fad(220,160)}PETIR · BADAI · METEORI · SONIK BOOM"),
    (148.10, 149.90, "Kicker", "{\\pos(540,700)\\an5\\fs44\\fad(220,160)}TANAH RETAK BEKU"),
    # ── S12 ragu
    (150.50, 154.70, "Stamp", "{\\pos(540,520)\\an5\\fs52\\frz-4\\fad(160,150)}BELUM TENTU SATU JAWABAN"),
    (155.40, 159.90, "Kicker", "{\\pos(540,1010)\\an5\\fs46\\fad(220,160)}BAGIAN PALING MENARIKNYA"),
    # ── S13 tafsir vs laporan
    (160.80, 165.00, "Stamp", "{\\pos(540,520)\\an5\\fs56\\frz-4\\fad(160,150)}TAFSIR MANUSIA"),
    (165.40, 169.30, "Kicker", "{\\pos(540,1010)\\an5\\fs44\\fad(220,160)}YANG TERCATAT: SUARA, WAKTU, LOKASI"),
    (170.00, 174.00, "Kicker", "{\\pos(540,700)\\an5\\fs44\\fad(220,160)}REAKSI ORANG YANG MENDENGARNYA"),
    # ── S14 batas
    (178.70, 182.60, "Stamp", "{\\pos(540,520)\\an5\\fs50\\frz-4\\fad(160,150)}TANPA BUKTI · TANPA SATU JAWABAN"),
    # ── S15 yang tahu
    (183.40, 187.40, "Kicker", "{\\pos(540,1010)\\an5\\fs46\\fad(220,160)}SUARA ANEH ITU PERNAH DIDENGAR"),
    (188.20, 193.10, "Kicker", "{\\pos(540,700)\\an5\\fs42\\fad(220,160)}SEBAGIAN TERJELASKAN · SEBAGIAN MENUNGGU DATA"),
    # ── S16 CTA komentar
    (194.00, 198.00, "Stamp", "{\\pos(540,520)\\an5\\fs52\\frz-4\\fad(160,150)}PERTANDA KIAMAT ATAU ALAM?"),
    (201.90, 205.50, "Kicker", "{\\pos(540,1010)\\an5\\fs48\\fad(220,160)}TULIS PENDAPAT LO DI KOMENTAR"),
    # ── outro
    (206.20, 210.68, "Big", "{\\pos(540,640)\\an5\\fs110\\fad(260,0)}ODDCHAPTER"),
    (206.50, 210.68, "Kicker", "{\\pos(540,740)\\an5\\fs42\\c&H002A2AD8&\\fad(300,0)}ODDCHAPTER SURPRISE · OS-EP03"),
    (206.80, 210.68, "Credit", "{\\pos(540,1000)\\an5\\fs26\\c&H00D0D0D0&\\fad(360,0)}" + CREDITS),
]
