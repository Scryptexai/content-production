"""Konfigurasi OS-EP01 — Ball lightning: bola cahaya di restoran Plöckenhaus.

VO = VO PEMILIK apa adanya (vo_owner/vo_ball-lightning.mp3,182,36 s; SRT
ElevenLabs65 cue, alignment = timing cue → vo_alignment.json,373 kata).
END =187,36 s (VO + outro animasi5 dtk). Format: feed vertikal9:16 durasi
bebas (bukan Shorts — VO sudah lewat3 menit).

Koreksi pemilik22 Nov (00G): pahami section → footage Coverr spesifik per
section (18 klip BARU di footage/os-ep01 — nol reuse lintas episode) → foto
AI hanya untuk yang tak mungkin difoto (4 still) → wajib source document
(3: ukiran19c PD, peta CC BY-SA, foto Heidelberg CC BY-SA) → tidak ada
section yang hanya foto.
"""

SLUG = "ball-lightning"
VO_FILE = "vo_owner/vo_ball-lightning.mp3"
END = 187.36
OUT_NAME = "OS-EP01_ball-lightning_feed.mp4"
SRT_NAME = "OS-EP01.id.srt"

# foto AI + source documents (di img/): key -> (file, lebar, tinggi)
IMAGES = {
    # foto AI — adegan yang tak mungkin difoto (tanpa orang)
    "BALLROOM": ("ai_ball_restoran.png", 768, 1376),
    "LANTAI":   ("ai_ball_lantai.png", 768, 1376),
    "MELEDEK":  ("ai_ball_meledek.png", 768, 1376),
    "TENNIS":   ("ai_bola_tennis.png", 768, 1376),
    # source document (00G butir4) — canvas card + kredit per shot
    "UKIRAN":   ("engraving_globe_de_feu_1870s.jpg", 960, 807),
    "HEIDEL":   ("heidelberg_alte_universitaet.jpg", 960, 720),
    "PETA":     ("reliefkarte_ploecken.png", 500, 345),
}

# footage/os-ep01/ (semua klip baru hasil fetch-footage,6,00 s masing-masing)
CLIPS = {
    "RESTORAN":  ("os-ep01/restoran_perapian.mp4",  0.40, 6.00),
    "HUJAN":     ("os-ep01/hujan_jendela.mp4",      0.40, 6.00),
    "BADAI":     ("os-ep01/badai_vilnius.mp4",      0.40, 6.00),
    "ANJING1":   ("os-ep01/anjing_kafe.mp4",        0.40, 6.00),
    "ANJING2":   ("os-ep01/anjing_lihat.mp4",       0.40, 6.00),
    "API":       ("os-ep01/api_gelap.mp4",          0.00, 6.00),
    "GEREJA":    ("os-ep01/gereja_jendela.mp4",     0.40, 6.00),
    "LILIN":     ("os-ep01/lilin_bokeh.mp4",        0.40, 6.00),
    "AWAN":      ("os-ep01/awan_timelapse.mp4",     0.40, 6.00),
    "PASS":      ("os-ep01/jalan_pass_kabut.mp4",   0.40, 6.00),
    "AWAN2":     ("os-ep01/awan_redup.mp4",         0.40, 6.00),
    "WAGNER":    ("os-ep01/wagner_menulis.mp4",     0.40, 6.00),
    "PENSIL":    ("os-ep01/pensil_tajam.mp4",       0.40, 6.00),
    "ALPEN":     ("os-ep01/alpen_kabut.mp4",        0.40, 6.00),
    "BUKU":      ("os-ep01/buku_halaman.mp4",       0.40, 6.00),
    "LAB":       ("os-ep01/eksperimen_lab.mp4",     0.30, 6.00),
    "LISTRIK":   ("os-ep01/menara_listrik.mp4",     0.40, 6.00),
    "GEREJA2":   ("os-ep01/gereja_sejarah.mp4",     0.40, 6.00),
}

TAG_STOK_C = "FOOTAGE STOK · COVERR"
TAG_UKIRAN = "ARSIP · WIKIMEDIA COMMONS · PD ABAD-19"
TAG_PETA = "PETA · TSCHUBBY · CC BY-SA3.0"
TAG_HEIDEL = "FOTO · RIBAX · CC BY-SA4.0"

# (mulai, selesai, klip/still, mode, z0, z1, opsi)
# mode "clip" = footage cover-crop FULL LAYAR9:16 (aturan21 Nov2026)
SHOTS = [
    # ── S1 hook: restoran pegunungan, hujan, petir (0,43–11,43)
    (0.00,    0.60, None, "black", 1.00, 1.00, {}),
    (0.60,    5.77, "RESTORAN", "clip", 1.00, 1.04, {"tag": TAG_STOK_C}),
    (5.77,    8.45, "HUJAN", "clip", 1.00, 1.03, {"tag": TAG_STOK_C}),
    (8.45,   11.43, "BADAI", "clip", 1.00, 1.04, {"tag": TAG_STOK_C}),
    # ── S2 bola cahaya masuk, merendah, anjing menjauh (11,43–26,45)
    (11.43,  17.89, "BALLROOM", "fill", 1.00, 1.10, {}),
    (17.89,  20.55, "LANTAI", "fill", 1.02, 1.10, {}),
    (20.55,  23.57, "ANJING1", "clip", 1.00, 1.03, {"tag": TAG_STOK_C}),
    (23.57,  26.45, "ANJING2", "clip", 1.00, 1.03, {"tag": TAG_STOK_C}),
    # ── S3 saksi sama; bola ~2 m meledak; tak ada yang terbakar (26,45–42,37)
    (26.45,  30.13, "UKIRAN", "canvas", 1.00, 1.05, {"tag": TAG_UKIRAN}),
    (30.13,  36.71, "MELEDEK", "fill", 1.00, 1.12, {}),
    (36.71,  42.37, "API", "clip", 1.00, 1.05, {"tag": TAG_STOK_C}),
    # ── S4 kalau di desa: jin, iblis, tanda dunia lain (42,37–50,87)
    (42.37,  46.50, "GEREJA", "clip", 1.00, 1.04, {"tag": TAG_STOK_C}),
    (46.50,  50.87, "LILIN", "clip", 1.00, 1.05, {"tag": TAG_STOK_C}),
    # ── S5 CTA like: cahaya aneh saat badai (50,87–57,03)
    (50.87,  54.00, "AWAN", "clip", 1.00, 1.03, {"tag": TAG_STOK_C}),
    (54.00,  57.03, "HUJAN", "clip", 1.20, 1.24, {"tag": TAG_STOK_C}),
    # ── S6 fakta: Sep1963 pukul11; Plöckenhaus/Plöckenpass/Alpen (57,03–73,49)
    (57.03,  60.03, "PASS", "clip", 1.00, 1.03, {"tag": TAG_STOK_C}),
    (60.03,  65.57, "AWAN2", "clip", 1.00, 1.05, {"tag": TAG_STOK_C}),
    (65.57,  73.49, "PETA", "canvas", 1.04, 1.14, {"tag": TAG_PETA}),
    (73.49,  79.57, "HEIDEL", "canvas", 1.02, 1.10, {"tag": TAG_HEIDEL}),
    # ── S7 saksi: mahasiswa Heidelberg; Günther A. Wagner menulis laporan (79,57–86,57)
    (79.57,  83.00, "WAGNER", "clip", 1.00, 1.03, {"tag": TAG_STOK_C}),
    (83.00,  86.57, "PENSIL", "clip", 1.00, 1.04, {"tag": TAG_STOK_C}),
    # ── S8 deskripsi: sebesar bola tenis; kecepatan seperti berjalan (86,57–96,53)
    (86.57,  90.93, "TENNIS", "fill", 1.00, 1.10, {}),
    (90.93,  96.53, "ALPEN", "clip", 1.00, 1.05, {"tag": TAG_STOK_C}),
    # ── S9 koroborasi:5 saksi, ruangan sebelah, anjing (96,53–115,41)
    (96.53, 101.79, "BUKU", "clip", 1.00, 1.05, {"tag": TAG_STOK_C}),
    (101.79, 105.35, "UKIRAN", "canvas", 1.12, 1.04, {"tag": TAG_UKIRAN}),
    (105.35, 110.61, "API", "clip", 1.50, 1.55, {"tag": TAG_STOK_C}),
    (110.61, 115.41, "ANJING1", "clip", 1.00, 1.05, {"tag": TAG_STOK_C}),
    # ── S10 nama & definisi: kugelblitz / ball lightning (115,41–127,78)
    (115.41, 120.89, "LANTAI", "fill", 1.12, 1.02, {}),
    (120.89, 124.50, "AWAN", "clip", 1.50, 1.54, {"tag": TAG_STOK_C}),
    (124.50, 127.78, "BADAI", "clip", 2.00, 2.04, {"tag": TAG_STOK_C}),
    # ── S11 debate ilmiah: plasma/tanah menguap/medan listrik (127,78–146,37)
    (127.78, 133.39, "LAB", "clip", 1.00, 1.05, {"tag": TAG_STOK_C}),
    (133.39, 137.00, "LISTRIK", "clip", 1.00, 1.04, {"tag": TAG_STOK_C}),
    (137.00, 140.29, "TENNIS", "fill", 1.14, 1.04, {}),
    (140.29, 143.50, "BUKU", "clip", 1.10, 1.14, {"tag": TAG_STOK_C}),
    (143.50, 146.37, "WAGNER", "clip", 2.50, 2.54, {"tag": TAG_STOK_C}),
    # ── S12 iblis? sains? (146,37–159,33)
    (146.37, 149.50, "GEREJA2", "clip", 1.00, 1.04, {"tag": TAG_STOK_C}),
    (149.50, 153.03, "LILIN", "clip", 2.40, 2.45, {"tag": TAG_STOK_C}),
    (153.03, 156.00, "LAB", "clip", 3.00, 3.04, {"tag": TAG_STOK_C}),
    (156.00, 159.33, "PENSIL", "clip", 2.60, 2.65, {"tag": TAG_STOK_C}),
    # ── S13 resolusi: kesaksian nyata, jurnal ilmiah, fenomena alam (159,33–172,25)
    (159.33, 162.67, "HEIDEL", "canvas", 1.16, 1.08, {"tag": TAG_HEIDEL}),
    (162.67, 167.00, "UKIRAN", "canvas", 1.02, 1.10, {"tag": TAG_UKIRAN}),
    (167.00, 172.25, "AWAN2", "clip", 0.40, 0.46, {"tag": TAG_STOK_C}),
    # ── S14 CTA komentar (172,25–182,36)
    (172.25, 176.50, "PASS", "clip", 1.70, 1.75, {"tag": TAG_STOK_C}),
    (176.50, 180.55, "LILIN", "clip", 1.00, 1.06, {"tag": TAG_STOK_C}),
    (180.55, 182.36, "RESTORAN", "clip", 1.50, 1.53, {"tag": TAG_STOK_C}),
    # ── outro animasi brand (182,36–187,36)
    (182.36, 187.36, None, "outro", 1.00, 1.00, {}),
]

KEYWORDS = {"KUGELBLITZ", "BALL LIGHTNING", "1963", "WAGNER",
            "PLÖCKENHAUS", "HEIDELBERG"}

NUM_PHRASES = [
    (["lima", "orang"], "5 orang"),
]

MERGE = [
    (["ball", "lightning"], "ball lightning"),
    (["tahun", "1963"], "tahun 1963"),
    (["pukul", "11"], "pukul 11"),
]

WORD_FIX = {
    "gunther": "Günther",
    "sain": "Sains",
    "pukul11": "pukul 11",
    "tahun1963": "tahun 1963",
    "sekitar2": "sekitar 2",
}

CREDITS = ("Footage stok: Coverr\\N"
           "Arsip: Wikimedia Commons — ukiran PD · peta CC BY-SA · foto Ribax CC BY-SA\\N"
           "@oddchapter7 · FENOMENA NYATA · LAPORAN SAKSI1963")

OVL = [
    # ── S1 hook
    (1.10,    5.60, "Stamp", "{\\pos(540,520)\\an5\\fs56\\frz-4\\fad(160,150)}BOLA CAHAYA DI RESTORAN"),
    (12.00,  17.60, "Kicker", "{\\pos(540,1010)\\an5\\fs46\\fad(220,160)}MASUK LEWAT PINTU YANG TERBUKA"),
    # ── S3 meledak
    (30.60,  36.40, "Stamp", "{\\pos(540,520)\\an5\\fs60\\frz-4\\fad(160,150)}MELEDAK SEPERTI TEMBAKAN"),
    (37.00,  41.60, "Kicker", "{\\pos(540,700)\\an5\\fs46\\c&H002A2AD8&\\fad(220,160)}TIDAK ADA YANG TERBAKAR"),
    # ── S4 desa
    (43.00,  49.80, "Kicker", "{\\pos(540,1010)\\an5\\fs44\\fad(220,160)}DISEBUT JIN, IBLIS, ATAU TANDA DUNIA LAIN"),
    # ── S6 fakta
    (60.60,  65.30, "Stamp", "{\\pos(540,520)\\an5\\fs64\\frz-4\\fad(160,150)}SEPTEMBER 1963 · PUKUL 11"),
    (66.20,  72.40, "Kicker", "{\\pos(540,1010)\\an5\\fs44\\fad(220,160)}PLÖCKENHAUS · PLÖCKENPASS · ALPEN, AUSTRIA"),
    # ── S7 saksi
    (74.00,  79.30, "Kicker", "{\\pos(540,1010)\\an5\\fs46\\fad(220,160)}MAHASISWA GEOLOGI — UNIVERSITÄT HEIDELBERG"),
    (80.00,  85.90, "Stamp", "{\\pos(540,520)\\an5\\fs56\\frz-4\\fad(160,150)}LAPORAN SAKSI: GÜNTHER A. WAGNER"),
    # ── S8 deskripsi
    (87.00,  90.70, "Stamp", "{\\pos(540,520)\\an5\\fs64\\frz-4\\fad(160,150)}SEBESAR BOLA TENIS"),
    (91.20,  95.60, "Kicker", "{\\pos(540,1010)\\an5\\fs46\\fad(220,160)}KECEPATANNYA SEPERTI ORANG BERJALAN"),
    # ── S9 saksi
    (97.00, 101.50, "Kicker", "{\\pos(540,700)\\an5\\fs48\\fad(220,160)}SULIT DIANGGAP ILUSI — JUMLAH SAKSI"),
    (102.00, 105.20, "Stamp", "{\\pos(540,520)\\an5\\fs68\\frz-4\\fad(160,150)}5 ORANG MELIHAT LANGSUNG"),
    (105.80, 110.40, "Kicker", "{\\pos(540,1010)\\an5\\fs46\\fad(220,160)}RUANGAN SEBELAH MENDENGAR LEDAKAN"),
    (111.00, 115.20, "Kicker", "{\\pos(540,700)\\an5\\fs48\\fad(220,160)}ANJING BEREAKSI TERHADAP BENDA ITU"),
    # ── S10 nama
    (115.90, 120.60, "Stamp", "{\\pos(540,520)\\an5\\fs80\\frz-4\\fad(160,150)}KUGELBLITZ"),
    (121.20, 127.00, "Kicker", "{\\pos(540,1010)\\an5\\fs46\\c&H002A2AD8&\\fad(220,160)}BALL LIGHTNING — FENOMENA BADAI PETIR"),
    # ── S11 teori
    (128.20, 133.20, "Kicker", "{\\pos(540,1010)\\an5\\fs46\\fad(220,160)}ILMUWAN BELUM PUNYA SATU PENJELASAN"),
    (133.80, 140.00, "Kicker", "{\\pos(540,700)\\an5\\fs44\\fad(220,160)}TEORI: PLASMA · TANAH MENGUAP · MEDAN LISTRIK"),
    (140.60, 145.70, "Kicker", "{\\pos(540,1010)\\an5\\fs46\\fad(220,160)}MASIH MODEL ILMIAH — BUKAN JAWABAN FINAL"),
    # ── S12 iblis/sains
    (146.80, 152.80, "Stamp", "{\\pos(540,520)\\an5\\fs66\\frz-4\\fad(160,150)}IBLIS ATAU SAINS?"),
    (153.40, 158.80, "Kicker", "{\\pos(540,700)\\an5\\fs50\\c&H002A2AD8&\\fad(240,170)}JAWABANNYA: BELUM"),
    # ── S13 resolusi
    (159.60, 162.50, "Kicker", "{\\pos(540,1010)\\an5\\fs50\\fad(220,160)}SATU KESAKSIAN NYATA"),
    (163.00, 166.80, "Stamp", "{\\pos(540,520)\\an5\\fs54\\frz-4\\fad(160,150)}TERCATAT DALAM JURNAL ILMIAH"),
    # ── S14 CTA komentar
    (172.80, 180.30, "Stamp", "{\\pos(540,520)\\an5\\fs60\\frz-4\\fad(160,150)}FENOMENA ALAM — ATAU LAIN?"),
    # ── outro
    (182.90, 187.36, "Big", "{\\pos(540,640)\\an5\\fs110\\fad(260,0)}ODDCHAPTER"),
    (183.20, 187.36, "Kicker", "{\\pos(540,740)\\an5\\fs42\\c&H002A2AD8&\\fad(300,0)}ODDCHAPTER SURPRISE · OS-EP01"),
    (183.50, 187.36, "Credit", "{\\pos(540,1000)\\an5\\fs26\\c&H00D0D0D0&\\fad(360,0)}" + CREDITS),
]
