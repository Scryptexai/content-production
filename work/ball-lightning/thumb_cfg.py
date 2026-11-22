"""Thumbnail/poster OS-EP01 — Ball lightning di restoran Plöckenhaus.

Palet standar ODDCHAPTER. Sumber gambar: foto AI bola cahaya (tanpa orang).
"""

JOBS = [
    # ── Thumbnail16:9 (panel kiri68%)
    ("OS-EP01_thumbnail_16x9.jpg", 1280, 720, "ai_ball_restoran.png", "left", [
        ("BOLA CAHAYA DI RESTORAN1963", "BARLOW", 54, "IVORY", 40, 80),
        ("KUGELBLITZ", "ANTON", 170, "RED", 40, 170),
        ("5 SAKSI · SEPT1963 · ALPEN AUSTRIA", "BARLOW", 52, "IVORY", 40, 460),
        ("1963", "ANTON", 72, "IVORY", 40, 560),
    ]),
    # ── Poster9:16 (panel bawah50%)
    ("OS-EP01_poster_9x16.jpg", 1080, 1920, "ai_ball_restoran.png", "bottom", [
        ("BOLA CAHAYA DI RESTORAN", "BARLOW", 64, "IVORY", 48, 1030),
        ("KUGELBLITZ", "ANTON", 150, "RED", 48, 1140),
        ("SEPTEMBER 1963", "BARLOW", 76, "IVORY", 48, 1520),
        ("PLÖCKENHAUS · ALPEN, AUSTRIA", "BARLOW", 54, "GREY", 48, 1660),
    ]),
    # ── Kartu akhir16:9 (panel bawah50%)
    ("OS-EP01_endcard_16x9.jpg", 1280, 720, "ai_ball_restoran.png", "bottom", [
        ("ODDCHAPTER", "ANTON", 110, "IVORY", 48, 800),
        ("FENOMENA NYATA · LAPORAN SAKSI1963", "BARLOW", 46, "RED", 48, 960),
        ("Footage stok: Coverr · Arsip: Wikimedia Commons (PD/CC BY-SA)",
         "BARLOW", 34, "GREY", 48, 1300),
    ]),
]
