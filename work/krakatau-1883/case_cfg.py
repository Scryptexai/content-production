"""Konfigurasi kasus AK-EP02 — Krakatau 1883 (Kapten Lindemann & Loudon)."""

SLUG = "krakatau-1883"
VO_FILE = "vo_krakatau-1883.mp3"
END = 106.40
OUT_NAME = "AK-EP02_krakatau-1883_short_v1.mp4"
SRT_NAME = "AK-EP02.id.srt"

IMAGES = {
    "A": ("A_litograf.jpg", 1280, 1628),      # litograf Royal Society 1888
    "B": ("B_afterglow.jpg", 1280, 1842),     # langit pasca-letusan, Royal Society
    "C": ("C_kitlv.jpg", 1280, 1731),         # KITLV 5888
    "D": ("D_karang.jpg", 700, 538),          # karang terlempar, Tropenmuseum
    "E": ("E_telok.jpg", 1280, 816),          # Residentiehuis Telok Betong (ilustrasi)
    "F": ("F_peta.jpg", 1280, 1280),          # peta Krakatau
}


# Footage kasus (work/<slug>/footage/): (berkas, detik mulai, durasi tersedia)
# Isi: rekonstruksi drama BBC "Krakatoa: The Last Days" (2006) — di layar selalu
# diberi label REKONSTRUKSI, bukan arsip. Hanya potongan tanpa wajah aktor.
CLIPS = {
    "F1": ("e0nky4I35xo.mp4", 282.8, 4.40),   # laut surut: kapal kandas di dasar
    "F2": ("e0nky4I35xo.mp4", 515.2, 4.40),   # air keruh menyapu, ranting dan puing
    "F3": ("e0nky4I35xo.mp4", 502.6, 2.80),   # benda mengapung berputar di air gelap
}
LABEL_REKON = "REKONSTRUKSI DRAMA BBC 2006 \u00b7 BUKAN ARSIP"

SHOTS = [
    (0.00,   2.20, "A", "card",   1.00, 1.04, {}),
    (2.20,   6.30, "A", "canvas", 1.00, 1.09, {"tag": "LITOGRAF: ROYAL SOCIETY 1888 · DOMAIN PUBLIK"}),
    (6.30,  10.10, "C", "canvas", 1.09, 1.00, {"tag": "LITOGRAF: KITLV 5888 · DOMAIN PUBLIK"}),
    (10.10, 15.60, "E", "canvas", 1.00, 1.08, {"tag": "ILUSTRASI: TELOK BETONG · KITLV (CC BY 4.0)"}),
    (15.60, 18.90, "A", "card",   1.06, 1.00, {}),
    (18.90, 24.50, "E", "card",   1.00, 1.06, {}),
    (24.50, 28.70, "F1", "clip", 1.0, 1.0, {"tag": "REKONSTRUKSI DRAMA BBC 2006 · BUKAN ARSIP", "box": (1000, 750)}),
    (28.70, 33.20, "B", "canvas", 1.10, 1.00, {}),
    (33.20, 38.50, "F", "card",   1.00, 1.06, {}),
    (38.50, 44.80, "F", "card",   1.08, 1.00, {}),
    (44.80, 47.30, "F3", "clip", 1.0, 1.0, {"tag": "REKONSTRUKSI DRAMA BBC 2006 · BUKAN ARSIP", "box": (1000, 750)}),
    (47.30, 51.00, "C", "card",   1.00, 1.06, {}),
    (51.00, 56.50, "A", "card",   1.06, 1.00, {}),
    (56.50, 62.60, "D", "canvas", 1.10, 1.00, {}),
    (62.60, 68.40, "C", "canvas", 1.00, 1.12, {}),
    (68.40, 72.50, "F2", "clip", 1.0, 1.0, {"tag": "REKONSTRUKSI DRAMA BBC 2006 · BUKAN ARSIP", "box": (1000, 750)}),
    (72.50, 76.00, "E", "canvas", 1.00, 1.10, {}),
    (76.00, 80.30, "D", "canvas", 1.10, 1.02, {}),
    (80.30, 83.30, "B", "card",   1.00, 1.06, {}),
    (83.30, 86.00, "A", "canvas", 1.00, 1.10, {}),
    (86.00, 89.90, "B", "card",   1.06, 1.00, {}),
    (89.90, 92.90, "C", "canvas", 1.10, 1.00, {}),
    (92.90, 96.90, "A", "canvas", 1.10, 1.00, {}),
    (96.90, 100.50, "D", "canvas", 1.00, 1.10, {}),
    (100.50, 102.80, "A", "card", 1.04, 1.00, {}),
    (102.80, 104.40, "F", "canvas", 1.00, 1.08, {}),
    (104.40, 106.40, None, "black", 1.0, 1.0, {}),
]

KEYWORDS = {"KRAKATAU", "TSUNAMI", "LINDEMANN", "LOUDON", "BEROUW", "1883", "36.000", "10.30"}

NUM_PHRASES = [
    (["sepuluh", "tiga", "puluh"], "10.30"),
]

MERGE = [
    (["guvernur", "general", "lowdon"], "GOUVERNEUR-GENERAAL LOUDON"),
    (["36", "000"], "36.000"),
    (["baling", "-baling"], "BALING-BALING"),
]

WORD_FIX = {
    "berau": "Berouw",
    "lindeman": "Lindemann",
    "uapos": "uap pos",
    "krakatoa": "Krakatau",
}

CREDITS = ("Foto: Royal Society 1888 (PD) · KITLV 5888 (PD)\\N"
           "Tropenmuseum / Woodbury & Page (CC BY-SA 3.0) · Wikimedia Commons\\N"
           "Sumber: laporan Kapten Lindemann · Wikipedia · Live Science\\N@oddchapter7 · KASUS BARU TIAP MINGGU")

OVL = [
    # ── hook (kartu)
    (0.30, 2.20, "Kicker", "{\\pos(540,700)\\an5\\fs76\\c&H00E0ECF0&\\fad(240,0)}SEORANG KAPTEN"),
    (0.70, 2.20, "Big", "{\\pos(540,860)\\an5\\fs104\\c&H002A2AD8&\\fad(200,0)\\t(0,2400,\\fscx104\\fscy104)}MENGHADAPI\\NTSUNAMI"),
    # ── tanggal
    (15.85, 18.80, "Stamp", "{\\pos(540,520)\\an5\\fs100\\frz-5\\fad(160,0)}26 AGUSTUS 1883"),
    # ── papan nama kapal
    (19.10, 24.40, "Kicker", "{\\pos(540,520)\\an5\\fs54\\fad(200,160)}KAPAL UAP POS & WISATA"),
    (19.40, 24.40, "Big", "{\\pos(540,670)\\an5\\fs150\\c&H002A2AD8&\\fad(200,160)}LOUDON"),
    (20.60, 24.40, "Kicker", "{\\pos(540,800)\\an5\\fs52\\c&H002A2AD8&\\fad(240,160)}KAPTEN J. T. H. LINDEMANN"),
    # ── pukul satu pagi
    (33.35, 38.40, "Stamp", "{\\pos(540,520)\\an5\\fs116\\frz-6\\fad(160,150)}01.00"),
    (33.75, 38.40, "Kicker", "{\\pos(540,670)\\an5\\fs56\\fad(240,150)}MUALIM KEMBALI DARI PANTAI"),
    # ── berouw kandas
    (38.70, 44.70, "Big", "{\\pos(540,540)\\an5\\fs180\\c&H002A2AD8&\\fad(180,150)}BEROUW"),
    (39.10, 44.70, "Kicker", "{\\pos(540,700)\\an5\\fs54\\fad(240,150)}KAPAL PEMERINTAH · KANDAS DI DERMAGA"),
    # ── 07.00
    (47.45, 50.90, "Stamp", "{\\pos(540,520)\\an5\\fs136\\frz-6\\fad(140,160)}07.00"),
    (47.90, 50.90, "Kicker", "{\\pos(540,680)\\an5\\fs54\\fad(240,160)}LAUT JADI DINDING"),
    # ── kapal pos bukan perang
    (51.15, 56.40, "Stamp", "{\\pos(540,520)\\an5\\fs78\\frz-4\\fad(160,150)}KAPAL POS · BUKAN PERANG"),
    # ── tiga jam kemudian
    (80.45, 83.20, "Kicker", "{\\pos(540,900)\\an5\\fs62\\fad(180,160)}TIGA JAM KEMUDIAN"),
    # ── 10.30 gelap total
    (86.15, 89.80, "Big", "{\\pos(540,620)\\an5\\fs240\\c&H002A2AD8&\\fad(180,150)}10.30"),
    (86.60, 89.80, "Kicker", "{\\pos(540,800)\\an5\\fs64\\fad(240,150)}SEPERTI TENGAH MALAM"),
    # ── korban
    (100.65, 102.70, "Big", "{\\pos(540,600)\\an5\\fs210\\c&H002A2AD8&\\fad(160,120)}36.000"),
    (101.00, 102.70, "Kicker", "{\\pos(540,780)\\an5\\fs48\\fad(220,120)}KORBAN JIWA · ANGKA RESMI 36.417"),
    # ── kartu akhir
    (104.50, 106.35, "Big", "{\\pos(540,700)\\an5\\fs104\\fad(280,0)}ODDCHAPTER"),
    (104.75, 106.35, "Kicker", "{\\pos(540,830)\\an5\\fs44\\c&H002A2AD8&\\fad(360,0)}KASUS NYATA · ARSIP ASLI"),
    (105.05, 106.35, "Credit", "{\\pos(540,960)\\an5\\fs27\\c&H00D0D0D0&\\fad(420,0)}Foto: Royal Society 1888 (PD) · KITLV 5888 (PD)\\NTropenmuseum / Woodbury & Page (CC BY-SA 3.0) · Wikimedia Commons\\NSumber: laporan Kapten Lindemann · Wikipedia · Live Science\\N@oddchapter7 · KASUS BARU TIAP MINGGU"),
]
