"""Thumbnail/poster OS-EP02 — Ikan jatuh dari langit (Drumherg,1928).

Palet standar ODDCHAPTER. Sumber gambar: foto AI ikan berserakan di jalan
desa (tanpa orang).
"""

JOBS = [
    # ── Thumbnail16:9 (panel kiri68%)
    ("OS-EP02_thumbnail_16x9.jpg", 1280, 720, "hook_ikan_jalan.png", "left", [
        ("DI DESA INI, IKAN JATUH DARI LANGIT", "BARLOW", 54, "IVORY", 40, 80),
        ("HUJAN IKAN", "ANTON", 170, "RED", 40, 170),
        ("1928 · DRUMHERG · IRLANDIA UTARA", "BARLOW", 52, "IVORY", 40, 460),
        ("±3 KM DARI STRANGFORD LOUGH", "ANTON", 66, "IVORY", 40, 560),
    ]),
    # ── Poster9:16 (panel bawah50%)
    ("OS-EP02_poster_9x16.jpg", 1080, 1920, "hook_ikan_jalan.png", "bottom", [
        ("IKAN JATUH DARI LANGIT", "BARLOW", 64, "IVORY", 48, 1030),
        ("HUJAN IKAN", "ANTON", 150, "RED", 48, 1140),
        ("TAHUN 1928", "BARLOW", 76, "IVORY", 48, 1520),
        ("DRUMHERG · DEKAT COMBER · IRLANDIA UTARA", "BARLOW", 46, "GREY", 48, 1660),
    ]),
    # ── Kartu akhir16:9 (panel bawah50% → mulai y=360; teks wajib < 720)
    ("OS-EP02_endcard_16x9.jpg", 1280, 720, "hook_ikan_jalan.png", "bottom", [
        ("ODDCHAPTER", "ANTON", 110, "IVORY", 48, 395),
        ("FENOMENA NYATA · IRLANDIA UTARA1928", "BARLOW", 46, "RED", 48, 545),
        ("Footage stok: Coverr · Peta: © OpenStreetMap contributors",
         "BARLOW", 34, "GREY", 48, 655),
    ]),
]
