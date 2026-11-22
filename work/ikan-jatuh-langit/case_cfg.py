"""Konfigurasi OS-EP02 — Ikan jatuh dari langit (Drumherg,1928).

VO = VO PEMILIK apa adanya (vo_owner/vo_ikan-jatuh-langit.mp3,220,19 s; SRT
TurboScribe81 cue (watermark dibuang), alignment = cue → kata proporsional →
vo_alignment.json,488 kata). END = 225,19 s (VO + outro animasi5 dtk).
Format: feed vertikal9:16 durasi bebas (bukan Shorts — VO >3 menit).

Koreksi pemilik22 Nov (00G): pahami section → footage Coverr spesifik per
section (31 klip BARU di footage/os-ep02 — nol reuse lintas episode; QC per
shot: s3_genangan/s8_jalan_hujan_warga/s15_awan_gelap2 GAGAL → diganti
s3_hujan_kaca & s8_hujan_kota, yang gagal tidak dipakai) → foto AI hanya
untuk yang tak mungkin difoto (4 still) → wajib source document (peta OSM —
kredit terbakar di render MapZoom) → tidak ada section yang hanya foto.

Shot peta (koreksi22 Nov): MAP-A zoom Irlandia → Drumherg/Comber (narasi
"tercatat tahun1928 di daerah Drumherg dekat Comber"), MAP-B County Down →
Strangford Lough + garis ±3 km dua titik (narasi "jaraknya sekitar3 km").
Keduanya render terpisah (scripts/render-mapzoom.mjs) → klip mode raw
(tanpa CLIP_POST grade).
"""

SLUG = "ikan-jatuh-langit"
VO_FILE = "vo_owner/vo_ikan-jatuh-langit.mp3"
END = 225.19
OUT_NAME = "OS-EP02_ikan-jatuh-langit_feed.mp4"
SRT_NAME = "OS-EP02.id.srt"

# foto AI + source document: key -> (file, lebar, tinggi)
IMAGES = {
    # foto AI — adegan yang tak mungkin difoto (tanpa orang)
    "IKAN_JALAN": ("hook_ikan_jalan.png", 1408, 768),
    "ATAP":       ("ikan_di_atap.png", 1408, 768),
    "LADANG":     ("ikan_di_ladang.png", 1408, 768),
    "WATERSPOUT": ("waterspout.png", 1408, 768),
    # source document (00G butir4) — peta asli tersaji via MAP-A/MAP-B (klip raw),
    # kredit "© OpenStreetMap contributors" terbakar di render MapZoom.
}

# footage/os-ep02/ (31 klip hasil fetch-footage,6,00 s masing-masing; cs+dur≤6)
CLIPS = {
    "PASAR_INDIA":   ("os-ep02/s1_pasar_ikan_india.mp4",   0.00, 6.00),
    "JALAN_HUJAN":   ("os-ep02/s1_jalan_hujan.mp4",        0.00, 6.00),
    "JALAN_ATAP":    ("os-ep02/s2_jalan_atap.mp4",         0.00, 6.00),
    "AWAN_TIMELAPSE":("os-ep02/s2_awan_timelapse.mp4",     0.00, 6.00),
    "HUJAN_KACA":    ("os-ep02/s3_hujan_kaca.mp4",         0.00, 6.00),
    "JALAN_BERAWAN": ("os-ep02/s4_jalan_berawan.mp4",      0.00, 6.00),
    "AWAN_GELAP":    ("os-ep02/s5_awan_gelap.mp4",         0.00, 6.00),
    "IKAN_DIJUAL":   ("os-ep02/s5_ikan_dijual.mp4",        0.00, 6.00),
    "PERMUKIMAN":    ("os-ep02/s6_permukiman.mp4",         0.00, 6.00),
    "SUNGAI":        ("os-ep02/s7_sungai.mp4",             0.00, 6.00),
    "KOLAM":         ("os-ep02/s7_kolam_ikan.mp4",         0.00, 6.00),
    "JALAN_LADANG":  ("os-ep02/s7_jalan_ladang.mp4",       0.00, 6.00),
    "HUJAN_KOTA":    ("os-ep02/s8_hujan_kota.mp4",         0.00, 6.00),
    "IKAN_MERAH":    ("os-ep02/s9_ikan_merah.mp4",         0.00, 6.00),
    "PASAR_IKAN2":   ("os-ep02/s9_pasar_ikan2.mp4",        0.00, 6.00),
    "DANAU":         ("os-ep02/s10_danau.mp4",             0.00, 6.00),
    "DESA_PESISIR":  ("os-ep02/s10_desa_pesisir.mp4",      0.00, 6.00),
    "GELOMBANG":     ("os-ep02/s11_gelombang_laut.mp4",    0.00, 6.00),
    "TORNADO":       ("os-ep02/s11_tornado.mp4",           0.00, 6.00),
    "AIR_PASANG":    ("os-ep02/s12_air_pasang.mp4",        0.00, 6.00),
    "AWAN_BERPUTAR": ("os-ep02/s12_awan_berputar.mp4",     0.00, 6.00),
    "OMBAK_BATU":    ("os-ep02/s12_ombak_batu.mp4",        0.00, 6.00),
    "KORAN":         ("os-ep02/s13_koran.mp4",             0.00, 6.00),
    "NELAYAN":       ("os-ep02/s13_nelayan.mp4",           0.00, 6.00),
    "JALAN_KOSONG":  ("os-ep02/s14_jalan_kosong.mp4",      0.00, 6.00),
    "SUNGAI_JALAN":  ("os-ep02/s14_sungai_jalan.mp4",      0.00, 6.00),
    "KOTA_GELAP":    ("os-ep02/s15_kota_gelap.mp4",        0.00, 6.00),
    "AQUARIUM":      ("os-ep02/s15_aquarium.mp4",          0.00, 6.00),
    "LADANG_HIJAU":  ("os-ep02/s16_ladang_hijau.mp4",      0.00, 6.00),
    "ALAM":          ("os-ep02/s16_alam.mp4",              0.00, 6.00),
    # shot peta Remotion (render scripts/render-mapzoom.mjs → salin ke sini)
    "MAP_A": ("os-ep02/map_drumherg_1928.mp4",     0.00, 7.30),
    "MAP_B": ("os-ep02/map_strangford_distance.mp4", 0.00, 6.80),
}

TAG_STOK_C = "FOOTAGE STOK · COVERR"

# (mulai, selesai, klip/still, mode, z0, z1, opsi)
# mode "clip" = footage cover-crop FULL LAYAR9:16 (aturan21 Nov2026)
SHOTS = [
    (0.00,    0.31, None, "black", 1.00, 1.00, {}),
    # ── S1 hook: ikan berserakan di jalan (0,31–12,41)
    (0.31,    4.93, "IKAN_JALAN", "fill", 1.00, 1.10, {}),
    (4.93,    7.61, "PASAR_INDIA", "clip", 1.00, 1.03, {"tag": TAG_STOK_C}),
    (7.61,    9.51, "JALAN_LADANG", "clip", 1.00, 1.03, {"tag": TAG_STOK_C}),
    (9.51,   12.41, "JALAN_HUJAN", "clip", 1.00, 1.04, {"tag": TAG_STOK_C}),
    # ── S2 dari mana? di atas atap rumah (12,41–24,11)
    (12.41,  17.03, "AWAN_TIMELAPSE", "clip", 1.00, 1.04, {"tag": TAG_STOK_C}),
    (17.03,  21.60, "ATAP", "fill", 1.00, 1.10, {}),
    (21.60,  24.11, "JALAN_ATAP", "clip", 1.00, 1.03, {"tag": TAG_STOK_C}),
    # ── S3 CTA like (24,11–34,53)
    (24.11,  29.05, "HUJAN_KACA", "clip", 1.00, 1.04, {"tag": TAG_STOK_C}),
    (29.05,  34.53, "AWAN_GELAP", "clip", 1.00, 1.05, {"tag": TAG_STOK_C}),
    # ── S4 fakta: bukan fiksi →1928 Drumherg dekat Comber (34,53–44,15)
    (34.53,  36.93, "JALAN_BERAWAN", "clip", 1.00, 1.03, {"tag": TAG_STOK_C}),
    (36.93,  44.15, "MAP_A", "clip", 1.00, 1.00, {"raw": True}),
    # ── S5 badai petir + ikan kemerahan di lahan (44,15–53,39)
    (44.15,  48.03, "AWAN_GELAP", "clip", 1.15, 1.19, {"tag": TAG_STOK_C}),
    (48.03,  51.47, "LADANG", "fill", 1.00, 1.10, {}),
    (51.47,  53.39, "IKAN_DIJUAL", "clip", 1.00, 1.03, {"tag": TAG_STOK_C}),
    # ── S6 di tanah + di atas atap bungalow (53,39–58,77)
    (53.39,  54.81, "PASAR_IKAN2", "clip", 1.00, 1.02, {"tag": TAG_STOK_C}),
    (54.81,  58.77, "JALAN_ATAP", "clip", 1.20, 1.24, {"tag": TAG_STOK_C}),
    # ── S7 negasi: sungai / kolam / kendaraan (58,77–67,95)
    (58.77,  61.31, "SUNGAI", "clip", 1.00, 1.03, {"tag": TAG_STOK_C}),
    (61.31,  63.81, "KOLAM", "clip", 1.00, 1.03, {"tag": TAG_STOK_C}),
    (63.81,  67.95, "JALAN_LADANG", "clip", 1.25, 1.29, {"tag": TAG_STOK_C}),
    # ── S8 kesimpulan warga: turun bersama hujan (67,95–75,79)
    (67.95,  72.79, "HUJAN_KOTA", "clip", 1.00, 1.05, {"tag": TAG_STOK_C}),
    (72.79,  75.79, "HUJAN_KACA", "clip", 1.30, 1.34, {"tag": TAG_STOK_C}),
    # ── S9 tak ada yang melihat; hasil akhirnya saja (75,79–96,65)
    (75.79,  81.15, "PASAR_IKAN2", "clip", 0.50, 0.55, {"tag": TAG_STOK_C}),
    (81.15,  86.51, "IKAN_MERAH", "clip", 1.00, 1.05, {"tag": TAG_STOK_C}),
    (86.51,  91.90, "PERMUKIMAN", "clip", 1.00, 1.05, {"tag": TAG_STOK_C}),
    (91.90,  96.65, "AWAN_TIMELAPSE", "clip", 1.20, 1.25, {"tag": TAG_STOK_C}),
    # ── S10 Strangford Lough ±3 km (96,65–114,91)
    (96.65, 100.23, "DANAU", "clip", 1.00, 1.03, {"tag": TAG_STOK_C}),
    (100.23, 106.95, "MAP_B", "clip", 1.00, 1.00, {"raw": True}),
    (106.95, 110.60, "DESA_PESISIR", "clip", 1.00, 1.04, {"tag": TAG_STOK_C}),
    (110.60, 114.91, "GELOMBANG", "clip", 1.00, 1.05, {"tag": TAG_STOK_C}),
    # ── S11 waterspout: definisi (114,91–132,29)
    (114.91, 118.17, "WATERSPOUT", "fill", 1.00, 1.08, {}),
    (118.17, 121.83, "TORNADO", "clip", 1.00, 1.04, {"tag": TAG_STOK_C}),
    (121.83, 125.75, "AIR_PASANG", "clip", 1.00, 1.04, {"tag": TAG_STOK_C}),
    (125.75, 129.00, "OMBAK_BATU", "clip", 1.00, 1.03, {"tag": TAG_STOK_C}),
    (129.00, 132.29, "DESA_PESISIR", "clip", 1.30, 1.34, {"tag": TAG_STOK_C}),
    # ── S12 mekanisme: angkat → jatuh (132,29–151,69)
    (132.29, 136.31, "AWAN_BERPUTAR", "clip", 1.00, 1.04, {"tag": TAG_STOK_C}),
    (136.31, 141.83, "GELOMBANG", "clip", 0.40, 0.46, {"tag": TAG_STOK_C}),
    (141.83, 146.31, "NELAYAN", "clip", 1.00, 1.05, {"tag": TAG_STOK_C}),
    (146.31, 151.69, "SUNGAI_JALAN", "clip", 1.00, 1.06, {"tag": TAG_STOK_C}),
    # ── S13 hujan ikan dilaporkan global (151,69–158,27)
    (151.69, 155.27, "KORAN", "clip", 1.00, 1.04, {"tag": TAG_STOK_C}),
    (155.27, 158.27, "PASAR_INDIA", "clip", 1.30, 1.34, {"tag": TAG_STOK_C}),
    # ── S14 kasus Drumherg: masuk akal, bukan bukti final (158,27–174,09)
    (158.27, 163.75, "JALAN_KOSONG", "clip", 1.00, 1.05, {"tag": TAG_STOK_C}),
    (163.75, 169.31, "JALAN_BERAWAN", "clip", 0.40, 0.46, {"tag": TAG_STOK_C}),
    (169.31, 174.09, "IKAN_DIJUAL", "clip", 1.20, 1.25, {"tag": TAG_STOK_C}),
    # ── S15 ringkasan: yang tahu / yang tidak tahu (174,09–198,57)
    (174.09, 177.50, "IKAN_MERAH", "clip", 1.30, 1.34, {"tag": TAG_STOK_C}),
    (177.50, 181.65, "PASAR_INDIA", "clip", 1.80, 1.85, {"tag": TAG_STOK_C}),
    (181.65, 185.29, "ATAP", "fill", 1.12, 1.04, {}),
    (185.29, 189.89, "SUNGAI", "clip", 1.30, 1.35, {"tag": TAG_STOK_C}),
    (189.89, 193.45, "AIR_PASANG", "clip", 1.30, 1.35, {"tag": TAG_STOK_C}),
    (193.45, 198.57, "JALAN_KOSONG", "clip", 0.40, 0.46, {"tag": TAG_STOK_C}),
    # ── S16 kutukan vs sains (198,57–210,71)
    (198.57, 203.11, "KOTA_GELAP", "clip", 1.00, 1.05, {"tag": TAG_STOK_C}),
    (203.11, 207.63, "AQUARIUM", "clip", 1.00, 1.05, {"tag": TAG_STOK_C}),
    (207.63, 210.71, "LADANG_HIJAU", "clip", 1.00, 1.03, {"tag": TAG_STOK_C}),
    # ── S17 CTA komentar (210,71–220,19)
    (210.71, 215.19, "ALAM", "clip", 1.00, 1.04, {"tag": TAG_STOK_C}),
    (215.19, 220.19, "DANAU", "clip", 0.90, 0.95, {"tag": TAG_STOK_C}),
    # ── outro animasi brand (220,19–225,19)
    (220.19, 225.19, None, "outro", 1.00, 1.00, {}),
]

KEYWORDS = {"DRUMHERG", "COMBER", "STRANGFORD", "WATERSPOUT",
            "TORNADO", "1928", "KUTUKAN"}

NUM_PHRASES = []

MERGE = []

WORD_FIX = {
    "low": "Lough",   # TTS membaca "Lough" sebagai "Low" — ejaan benar di caption
}

CREDITS = ("Footage stok: Coverr\\N"
           "Peta: \\Nc OpenStreetMap contributors\\N"
           "@oddchapter7 · FENOMENA NYATA · IRLANDIA UTARA1928")

OVL = [
    # ── S1 hook
    (1.10,    5.60, "Stamp", "{\\pos(540,520)\\an5\\fs56\\frz-4\\fad(160,150)}IKAN JATUH DARI LANGIT"),
    # ── S2 dari mana
    (12.90,  17.00, "Kicker", "{\\pos(540,1010)\\an5\\fs46\\fad(220,160)}DARI MANA ASALNYA?"),
    # ── S3 CTA like
    (24.50,  28.90, "Kicker", "{\\pos(540,1010)\\an5\\fs44\\fad(220,160)}KLIK LIKE — KEJADIAN ANEH YANG BISA DIJELASKAN"),
    # ── S4 fakta
    (35.00,  36.60, "Stamp", "{\\pos(540,520)\\an5\\fs54\\frz-4\\fad(160,150)}BUKAN CERITA FIKSI"),
    # ── S5 badai (map A sudah punya headline sendiri)
    (44.60,  47.90, "Stamp", "{\\pos(540,520)\\an5\\fs56\\frz-4\\fad(160,150)}BADAI PETIR YANG SANGAT KUAT"),
    (48.40,  51.30, "Kicker", "{\\pos(540,1010)\\an5\\fs46\\c&H002A2AD8&\\fad(220,160)}PULUHAN IKAN KECIL MERAH DI LAHAN"),
    # ── S7 negasi
    (59.20,  63.70, "Kicker", "{\\pos(540,1010)\\an5\\fs44\\fad(220,160)}TIDAK ADA SUNGAI · TIDAK ADA KOLAM JEBOL"),
    (64.20,  67.80, "Kicker", "{\\pos(540,700)\\an5\\fs44\\fad(220,160)}TIDAK ADA KENDARAAN PEMBAWA IKAN"),
    # ── S8 kesimpulan
    (73.10,  75.60, "Stamp", "{\\pos(540,520)\\an5\\fs58\\frz-4\\fad(160,150)}TURUN BERSAMA HUJAN?"),
    # ── S9 bukti
    (76.40,  80.90, "Kicker", "{\\pos(540,1010)\\an5\\fs46\\fad(220,160)}TIDAK ADA YANG MELIHATNYA JATUH"),
    (88.00,  91.70, "Kicker", "{\\pos(540,700)\\an5\\fs44\\fad(220,160)}KESAKSIAN CUKUP UNTUK BUKTIKAN?"),
    # ── S10 setelah map B
    (107.40, 110.40, "Kicker", "{\\pos(540,1010)\\an5\\fs46\\fad(220,160)}JARAK TERLALU JAUH UNTUK DIJELASKAN"),
    # ── S11 waterspout
    (115.30, 118.00, "Stamp", "{\\pos(540,520)\\an5\\fs72\\frz-4\\fad(160,150)}WATERSPOUT"),
    (122.20, 125.60, "Kicker", "{\\pos(540,1010)\\an5\\fs46\\c&H002A2AD8&\\fad(220,160)}PUSARAN ANGIN DI ATAS PERMUKAAN AIR"),
    # ── S12 mekanisme
    (132.70, 136.20, "Kicker", "{\\pos(540,1010)\\an5\\fs46\\fad(220,160)}AIR + IKAN TERANGKAT KE UDARA"),
    (146.80, 151.50, "Kicker", "{\\pos(540,700)\\an5\\fs46\\fad(220,160)}JATUH KEMBALI — KADANG JAUH DARI ASAL"),
    # ── S13 global
    (152.10, 155.10, "Kicker", "{\\pos(540,1010)\\an5\\fs46\\fad(220,160)}PERNAH DILAPORKAN DI BERBAGAI TEMPAT"),
    # ── S14 kasus
    (158.70, 163.60, "Stamp", "{\\pos(540,520)\\an5\\fs54\\frz-4\\fad(160,150)}MASUK AKAL — BUKAN BUKTI FINAL"),
    (165.50, 169.20, "Kicker", "{\\pos(540,1010)\\an5\\fs44\\fad(220,160)}TIDAK ADA REKAMAN · TIDAK ADA SAKSI"),
    # ── S15 ringkasan
    (177.00, 181.50, "Kicker", "{\\pos(540,1010)\\an5\\fs44\\fad(220,160)}YANG KITA TAHU: SETELAH BADAI · BANYAK · DI ATAP"),
    (190.40, 197.90, "Kicker", "{\\pos(540,700)\\an5\\fs44\\c&H002A2AD8&\\fad(220,160)}YANG KITA TIDAK TAHU: BAGAIMANA JATUHNYA"),
    # ── S16 kutukan vs sains
    (199.10, 203.00, "Stamp", "{\\pos(540,520)\\an5\\fs64\\frz-4\\fad(160,150)}KUTUKAN ATAU SAINS?"),
    (203.60, 210.10, "Kicker", "{\\pos(540,1010)\\an5\\fs46\\fad(220,160)}BADAI MENGANGKAT · MENJATUHKAN DI TEMPAT SALAH"),
    # ── S17 CTA komentar
    (211.20, 216.40, "Stamp", "{\\pos(540,520)\\an5\\fs60\\frz-4\\fad(160,150)}MENURUT LO, CUKUP?"),
    (216.90, 219.70, "Kicker", "{\\pos(540,1010)\\an5\\fs48\\fad(220,160)}TULIS PENDAPAT LO DI KOMENTAR"),
    # ── outro
    (220.70, 225.19, "Big", "{\\pos(540,640)\\an5\\fs110\\fad(260,0)}ODDCHAPTER"),
    (221.00, 225.19, "Kicker", "{\\pos(540,740)\\an5\\fs42\\c&H002A2AD8&\\fad(300,0)}ODDCHAPTER SURPRISE · OS-EP02"),
    (221.30, 225.19, "Credit", "{\\pos(540,1000)\\an5\\fs26\\c&H00D0D0D0&\\fad(360,0)}" + CREDITS),
]
