"""Thumbnail/poster AK-EP10 — Wowon Krimo (pengganda uang).

Palet standar ODDCHAPTER, panel gelap86%. Still AI tanpa orang:
amplop_meja (thumbnail16:9), aki_banyu_sea (poster9:16 + endcard).
"""

JOBS = [
    # ── Thumbnail16:9 (panel kiri68%)
    ("AK-EP10_thumbnail_16x9.jpg", 1280, 720, "amplop_meja.jpg", "left", [
        ("JANJI UANG BERLIPAT", "BARLOW", 54, "IVORY", 40, 80),
        ("9 ORANG", "ANTON", 170, "RED", 40, 170),
        ("DALANGNYA: WOWON ERAWAN", "BARLOW", 52, "IVORY", 40, 460),
        ("2023", "ANTON", 72, "IVORY", 40, 560),
    ]),
    # ── Poster9:16 (panel bawah50%)
    ("AK-EP10_poster_9x16.jpg", 1080, 1920, "aki_banyu_sea.jpg", "bottom", [
        ("JANJI UANG BERLIPAT", "BARLOW", 64, "IVORY", 48, 1030),
        ("9 ORANG", "ANTON", 150, "RED", 48, 1140),
        ("2023 · WOWON ERAWAN", "BARLOW", 76, "IVORY", 48, 1520),
        ("VONIS SEUMUR HIDUP", "BARLOW", 54, "GREY", 48, 1660),
    ]),
    # ── Kartu akhir16:9 (panel bawah50%)
    ("AK-EP10_endcard_16x9.jpg", 1280, 720, "aki_banyu_sea.jpg", "bottom", [
        ("ODDCHAPTER", "ANTON", 110, "IVORY", 48, 800),
        ("KASUS NYATA · ARSIP ASLI", "BARLOW", 46, "RED", 48, 960),
        ("Footage stok: Coverr · Sumber: Tempo · BBC Indonesia · detik",
         "BARLOW", 34, "GREY", 48, 1300),
    ]),
]
