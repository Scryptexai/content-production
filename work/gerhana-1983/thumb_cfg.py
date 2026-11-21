"""Thumbnail/poster AK-EP09 — Gerhana 1983.

Palet standar ODDCHAPTER, panel gelap86%. Still AI dari workdir episode
(tanpa orang): eclipse (16:9 + endcard), window_shutters (poster9:16).
"""

JOBS = [
    # ── Thumbnail16:9 (panel kiri68%)
    ("AK-EP09_thumbnail_16x9.jpg", 1280, 720, "eclipse.jpg", "left", [
        ("TENGAH HARI JADI MALAM", "BARLOW", 54, "IVORY", 40, 80),
        ("1983", "ANTON", 170, "RED", 40, 170),
        ("SEMUA DIPERINTAH MASUK RUMAH", "BARLOW", 52, "IVORY", 40, 460),
        ("11 JUNI", "ANTON", 72, "IVORY", 40, 560),
    ]),
    # ── Poster9:16 (panel bawah50%)
    ("AK-EP09_poster_9x16.jpg", 1080, 1920, "window_shutters.jpg", "bottom", [
        ("TENGAH HARI JADI MALAM", "BARLOW", 64, "IVORY", 48, 1030),
        ("MASUK RUMAH", "ANTON", 150, "RED", 48, 1140),
        ("11 JUNI 1983 · PULAU JAWA", "BARLOW", 76, "IVORY", 48, 1520),
        ("PERINGATAN TVRI & RRI", "BARLOW", 54, "GREY", 48, 1660),
    ]),
    # ── Kartu akhir16:9 (panel bawah50%)
    ("AK-EP09_endcard_16x9.jpg", 1280, 720, "eclipse.jpg", "bottom", [
        ("ODDCHAPTER", "ANTON", 110, "IVORY", 48, 800),
        ("KASUS NYATA · ARSIP ASLI", "BARLOW", 46, "RED", 48, 960),
        ("Footage stok: Coverr · Sumber: CNN Indonesia · Tirto (Kompas 1983)",
         "BARLOW", 34, "GREY", 48, 1300),
    ]),
]
