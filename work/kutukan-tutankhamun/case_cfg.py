"""Konfigurasi OS-EP04 — Kutukan Makam Tutankhamun.

VO internal perempuan voice-08, disetujui pemilik sebagai suara internal yang
mendekati karakter Riri. Sumber: vo_internal/vo_kutukan-tutankhamun.m4a
(157,96 dtk); END = 162,63 dtk dengan outro brand 4,67 dtk. Caption memakai
anchor jeda audio/VAD per frasa lalu distribusi proporsional di dalam frasa;
bukan dipresentasikan sebagai forced alignment ASR.

Sudut bukti: makam KV62 dan kematian Carnarvon adalah fakta; klaim hubungan
sebab-akibat supernatural tidak terbukti. Kartu tanggal + kartu tiga penyintas
adalah bukti visual turn. Sumber lokasi nyata: peta OpenStreetMap berlisensi
ODbL, dianimasikan sebagai MAP-ZOOM ke KV62 dan diberi kredit pada shot.

00G: footage Coverr baru di footage/os-ep04 (nol reuse lintas episode), foto
AI hanya untuk adegan historis yang tak dapat direkam, dokumen sumber nyata,
dan peta asli. Semua klip Coverr diberi label di layar.
"""

SLUG = "kutukan-tutankhamun"
VO_FILE = "vo_internal/vo_kutukan-tutankhamun.m4a"
END = 162.63
OUT_NAME = "OS-EP04_kutukan-tutankhamun_feed.mp4"
SRT_NAME = "OS-EP04.id.srt"
# Anchor VAD sudah berada di awal suara kata; jangan mendahului ucapan lagi.
CAPTION_LEAD = 0.0
CAPTION_TAIL = 0.14

IMAGES = {
    "DOOR": ("tomb_sealed_door.png", 768, 1376),
    "VALLEY": ("valley_excavation_empty.png", 768, 1376),
    "PRESS": ("newspaper_press_empty.png", 768, 1376),
    "TIMELINE": ("timeline_1922_1923.png", 1080, 1920),
    "SURVIVORS": ("survivors_counterevidence.png", 1080, 1920),
    "VERDICT": ("verdict_two_facts.png", 1080, 1920),
}

# Semua klip normalisasi 6s oleh fetch-footage. MAP raw sudah 6,4s.
CLIPS = {
    "S1_DESERT": ("os-ep04/s1_desert_view.mp4", 0.0, 6.0),
    "S1_HALL": ("os-ep04/s1_hallway.mp4", 0.0, 6.0),
    "S2_BOOK": ("os-ep04/s2_old_book.mp4", 0.0, 6.0),
    "S2_PAGES": ("os-ep04/s2_pages.mp4", 0.0, 6.0),
    "S2_WRITE": ("os-ep04/s2_writing_fire.mp4", 0.0, 6.0),
    "S3_ROCKS": ("os-ep04/s3_desert_rocks.mp4", 0.0, 6.0),
    "S3_CAPPA": ("os-ep04/s3_cappadocia.mp4", 0.0, 6.0),
    "S3_RUINS": ("os-ep04/s3_ruins.mp4", 0.0, 6.0),
    "S3_STONE": ("os-ep04/s3_stone_sculpture.mp4", 0.0, 6.0),
    "S3_STONE_MOUNTS": ("os-ep04/s3_stone_mountains.mp4", 0.0, 6.0),
    "S4_ARCH": ("os-ep04/s4_arch.mp4", 0.0, 6.0),
    "S4_CANDLE": ("os-ep04/s4_candle.mp4", 0.0, 6.0),
    "S5_DIARY": ("os-ep04/s5_diary.mp4", 0.0, 6.0),
    "S5_NOTES": ("os-ep04/s5_notes.mp4", 0.0, 6.0),
    "S5_WATCH": ("os-ep04/s5_watch.mp4", 0.0, 6.0),
    "S6_DESERT": ("os-ep04/s6_empty_desert.mp4", 0.0, 6.0),
    "S6_LOUVRE": ("os-ep04/s6_louvre.mp4", 0.0, 6.0),
    "S6_TUILERIES": ("os-ep04/s6_louvre_tuileries.mp4", 0.0, 6.0),
    "S7_DOOR": ("os-ep04/s7_old_door.mp4", 0.0, 6.0),
    "S7_ROAD": ("os-ep04/s7_road_california.mp4", 0.0, 6.0),
    "MAP_KV62": ("os-ep04/map_valley_of_kings_kv62.mp4", 0.0, 6.4),
}

TAG_STOK_C = "FOOTAGE STOK · COVERR"

# (mulai, selesai, asset, mode, z0, z1, extra)
SHOTS = [
    (0.00,   0.25, None,        "black", 1.0, 1.0, {}),
    # S1 — cold open: payoff/kontra-bukti dari klimaks disalin ke depan.
    # Sesudah itu cerita kembali ke awal pencarian Carter (18,67 dtk).
    (0.25,   5.00, "DOOR",      "fill",  1.0, 1.09,
     {"tag": "ILUSTRASI AI · BUKAN FOTO KV62"}),
    (5.00,   9.65, "VERDICT",   "fill",  1.0, 1.03, {}),
    (9.65,  14.40, "SURVIVORS", "fill",  1.0, 1.02, {}),
    (14.40, 18.67, "S1_HALL",   "clip",  1.0, 1.0, {"tag": TAG_STOK_C}),
    # S2 — Carter dan Lembah Para Raja
    (18.67, 23.50, "VALLEY",    "fill",  1.0, 1.07, {}),
    (23.50, 29.90, "MAP_KV62",  "clip",  1.0, 1.0, {"raw": True}),
    (29.90, 34.50, "S2_BOOK",   "clip",  1.0, 1.0, {"tag": TAG_STOK_C}),
    (34.50, 39.00, "S2_PAGES",  "clip",  1.0, 1.0, {"tag": TAG_STOK_C}),
    (39.00, 43.80, "S2_WRITE",  "clip",  1.0, 1.0, {"tag": TAG_STOK_C}),
    (43.80, 47.90, "S3_RUINS", "clip", 1.0, 1.0,
     {"tag": "FOOTAGE STOK · COVERR · ILUSTRASI"}),
    # S3 — pembukaan bertahap; sakit dan kematian Carnarvon
    (47.90, 52.80, "TIMELINE",  "fill",  1.0, 1.02, {}),
    (52.80, 57.20, "S4_ARCH",   "clip",  1.0, 1.0, {"tag": TAG_STOK_C}),
    (57.20, 61.80, "TIMELINE",  "fill",  1.08, 1.12, {"focusy": 0.65}),
    (61.80, 66.10, "S4_CANDLE", "clip",  1.0, 1.0, {"tag": TAG_STOK_C}),
    # S4 — koran mengisi jarak dua fakta
    (66.10, 70.40, "PRESS",     "fill",  1.0, 1.08, {}),
    (70.40, 74.70, "S5_DIARY",  "clip",  1.0, 1.0, {"tag": TAG_STOK_C}),
    (74.70, 80.00, "S5_WATCH",  "clip",  1.0, 1.0, {"tag": TAG_STOK_C}),
    (80.00, 86.32, "S5_NOTES",  "clip",  1.0, 1.0, {"tag": TAG_STOK_C}),
    # S5 — turn: daftar penyintas
    (86.32, 92.80, "SURVIVORS", "fill",  1.0, 1.02, {}),
    (92.80, 99.00, "SURVIVORS", "fill",  1.07, 1.11, {"focusy": 0.58}),
    (99.00,104.00, "S6_LOUVRE", "clip",  1.0, 1.0, {"tag": TAG_STOK_C}),
    (104.00,110.00,"S6_TUILERIES","clip",1.0, 1.0, {"tag": TAG_STOK_C}),
    # S6 — pertanyaan utama + hubungan yang tidak terbukti
    (110.00,115.20,"VERDICT",   "fill",  1.0, 1.03, {}),
    (115.20,120.80,"S6_DESERT", "clip",  1.0, 1.0, {"tag": TAG_STOK_C}),
    (120.80,126.20,"S3_STONE",  "clip",  1.0, 1.0, {"tag": TAG_STOK_C}),
    (126.20,131.60,"S7_DOOR",   "clip",  1.0, 1.0, {"tag": TAG_STOK_C}),
    (131.60,137.20,"VERDICT",   "fill",  1.04, 1.10, {"focusy": 0.62}),
    # S7 — bias sebab-akibat; kalimat tanda tangan
    (137.20,142.00,"S7_ROAD",   "clip",  1.0, 1.0, {"tag": TAG_STOK_C}),
    (142.00,146.50,"SURVIVORS", "fill",  1.12, 1.17, {"focusy": 0.78}),
    (146.50,151.00,"S3_ROCKS",  "clip",  1.0, 1.0, {"tag": TAG_STOK_C}),
    (151.00,157.98,"DOOR",      "fill",  1.08, 1.16, {}),
    (157.98,162.63,None,         "outro", 1.0, 1.0, {}),
]

KEYWORDS = {"TUTANKHAMUN", "CARNARVON", "HOWARD", "CARTER", "KV62", "FIRAUN", "KUTUKAN"}
NUM_PHRASES = [
    (["seribu", "sembilan", "ratus", "dua", "puluh", "dua"], "1922"),
    (["seribu", "sembilan", "ratus", "dua", "puluh", "tiga"], "1923"),
    (["seribu", "sembilan", "ratus", "tiga", "puluh", "sembilan"], "1939"),
    (["seribu", "sembilan", "ratus", "delapan", "puluh"], "1980"),
    (["seribu", "sembilan", "ratus", "enam", "puluh", "sembilan"], "1969"),
    (["tiga", "ribu"], "3.000"),
]
MERGE = []
WORD_FIX = {"tutankhamun": "Tutankhamun", "carnarvon": "Carnarvon", "howard": "Howard", "carter": "Carter", "evelyn": "Evelyn", "herbert": "Herbert", "douglas": "Douglas", "derry": "Derry", "firaun": "Firaun"}

CREDITS = ("Footage stok: Coverr\\N"
           "Peta lokasi: © OpenStreetMap contributors · ODbL\\N"
           "Visual AI tanpa orang · Mengandung media sintetis")

OVL = [
    (0.60,  4.85, "Big",    "{\\pos(540,620)\\an5\\fs78\\fad(160,150)}KUTUKAN FIRAUN?\\NPEMBODOHAN PUBLIK."),
    (19.10,23.20, "Stamp",  "{\\pos(540,520)\\an5\\fs54\\frz-4\\fad(160,140)}HOWARD CARTER"),
    # MAP memiliki title dan credit sendiri
    (30.30,34.30, "Kicker", "{\\pos(540,1010)\\an5\\fs46\\fad(220,160)}NOVEMBER 1922 · TANGGA DITEMUKAN"),
    (40.00,43.60, "Kicker", "{\\pos(540,700)\\an5\\fs46\\fad(200,140)}PINTU BERSEGEL · 3.000 TAHUN"),
    (48.30,52.50, "Stamp",  "{\\pos(540,510)\\an5\\fs54\\frz-4\\fad(160,150)}FEBRUARI 1923"),
    (57.80,61.50, "Kicker", "{\\pos(540,1010)\\an5\\fs46\\fad(220,160)}5 APRIL · INFEKSI SERIUS"),
    (66.60,70.10, "Stamp",  "{\\pos(540,520)\\an5\\fs56\\frz-4\\fad(160,150)}DUA FAKTA BERURUTAN"),
    (75.10,79.70, "Kicker", "{\\pos(540,1010)\\an5\\fs46\\fad(220,160)}KORAN MENGISI JARAKNYA: KUTUKAN"),
    (80.30,86.00, "Kicker", "{\\pos(540,700)\\an5\\fs46\\fad(220,160)}DAFTAR KEMATIAN TERUS MENCARI NAMA"),
    (99.30,103.70,"Stamp",  "{\\pos(540,520)\\an5\\fs54\\frz-4\\fad(160,150)}KUTUKAN ATAU KORAN?"),
    (110.40,114.90,"Kicker", "{\\pos(540,1010)\\an5\\fs46\\fad(220,160)}HUBUNGANNYA TIDAK PERNAH TERBUKTI"),
    (121.20,126.00,"Kicker", "{\\pos(540,700)\\an5\\fs44\\fad(220,160)}SATU KEMATIAN BISA DIJELASKAN INFEKSI"),
    (132.10,137.00,"Stamp",  "{\\pos(540,520)\\an5\\fs50\\frz-4\\fad(160,150)}URUTAN BUKAN SEBAB-AKIBAT"),
    (143.00,146.20,"Kicker", "{\\pos(540,1010)\\an5\\fs46\\fad(220,160)}KITA SERING LUPA MENGHITUNG PENYINTAS"),
    (151.60,157.60,"Kicker", "{\\pos(540,700)\\an5\\fs44\\fad(220,120)}SIAPA YANG KITA LUPA HITUNG?"),
    (158.50,162.90,"Big",    "{\\pos(540,640)\\an5\\fs110\\fad(260,0)}ODDCHAPTER"),
    (158.80,162.90,"Kicker", "{\\pos(540,740)\\an5\\fs42\\c&H002A2AD8&\\fad(300,0)}ODDCHAPTER SURPRISE · OS-EP04"),
    (159.10,162.90,"Credit", "{\\pos(540,1000)\\an5\\fs26\\c&H00D0D0D0&\\fad(360,0)}" + CREDITS),
]
