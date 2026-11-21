"""Thumbnail/poster AK-EP07 — Rockefeller/Otsjanep.

Palet standar ODDCHAPTER (RED / IVORY / GREY), panel gelap86%, garis merah.
Gambar AI tanpa orang: sea_vast.jpg (16:9 + endcard), report_dark.jpg (poster9:16).
"""

JOBS = [
    # ── Thumbnail16:9 (panel kiri68%)
    ("AK-EP07_thumbnail_16x9.jpg", 1280, 720, "sea_vast.jpg", "left", [
        ("DUA JERIKEN — DAN SATU KEPALA", "BARLOW", 50, "IVORY", 40, 80),
        ("1961", "ANTON", 180, "RED", 40, 170),
        ("LAPORAN YANG DIKUBUR", "BARLOW", 56, "IVORY", 40, 460),
        ("OTSJANEP", "ANTON", 72, "IVORY", 40, 560),
    ]),
    # ── Poster9:16 (panel bawah50%)
    ("AK-EP07_poster_9x16.jpg", 1080, 1920, "report_dark.jpg", "bottom", [
        ("TIGA TITIK DI LAUT", "BARLOW", 64, "IVORY", 48, 1030),
        ("1961", "ANTON", 240, "RED", 48, 1120),
        ("LAPORAN YANG DIKUBUR", "BARLOW", 76, "IVORY", 48, 1500),
        ("MICHAEL ROCKEFELLER · OT SJANEP", "BARLOW", 54, "GREY", 48, 1660),
    ]),
    # ── Kartu akhir16:9 (panel bawah50%)
    ("AK-EP07_endcard_16x9.jpg", 1280, 720, "sea_vast.jpg", "bottom", [
        ("ODDCHAPTER", "ANTON", 110, "IVORY", 48, 800),
        ("KASUS NYATA · ARSIP ASLI", "BARLOW", 46, "RED", 48, 960),
        ("Footage stok: Coverr · Sumber: Wikipedia · Savage Harvest (2014)",
         "BARLOW", 34, "GREY", 48, 1300),
    ]),
]
