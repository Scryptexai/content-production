"""Thumbnail/poster AK-EP06 — Jonestown / White Night.

Palet standar ODDCHAPTER (RED 0xD82A2A / IVORY / GREY), panel gelap 86%,
garis merah pemisah. Gambar: jungle_night.jpg (16:9, endcard), candles_dark.jpg
poster3x4 — keduanya AI tanpa orang.
"""

JOBS = [
    # ── Thumbnail16:9 (panel kiri68%)
    ("AK-EP06_thumbnail_16x9.jpg", 1280, 720, "jungle_night.jpg", "left", [
        ("MEREKA DISURUH MINUM RACUN", "BARLOW", 54, "IVORY", 40, 80),
        ("918", "ANTON", 180, "RED", 40, 170),
        ("MENINGGAL DI JONESTOWN", "BARLOW", 56, "IVORY", 40, 460),
        ("WHITE NIGHT", "ANTON", 72, "IVORY", 40, 560),
    ]),
    # ── Poster9:16 (panel bawah50%)
    ("AK-EP06_poster_9x16.jpg", 1080, 1920, "candles_dark.jpg", "bottom", [
        ("MEREKA DISURUH MINUM RACUN", "BARLOW", 64, "IVORY", 48, 1030),
        ("918", "ANTON", 260, "RED", 48, 1120),
        ("MENINGGAL DI JONESTOWN", "BARLOW", 76, "IVORY", 48, 1500),
        ("WHITE NIGHT · 18 NOVEMBER 1978", "BARLOW", 56, "GREY", 48, 1660),
    ]),
    # ── Kartu akhir16:9 (panel bawah50%)
    ("AK-EP06_endcard_16x9.jpg", 1280, 720, "jungle_night.jpg", "bottom", [
        ("ODDCHAPTER", "ANTON", 110, "IVORY", 48, 800),
        ("KASUS NYATA · ARSIP ASLI", "BARLOW", 46, "RED", 48, 960),
        ("Footage stok: Coverr · Sumber: Wikipedia · Jonestown Institute",
         "BARLOW", 34, "GREY", 48, 1300),
    ]),
]
