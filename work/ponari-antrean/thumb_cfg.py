"""Thumbnail/poster AK-EP08 — Ponari/antrean.

Palet standar ODDCHAPTER, panel gelap86%. Still AI dari workdir episode
(tanpa orang): stone_glass (16:9), village_lane (poster9:16 + endcard).
"""

JOBS = [
    # ── Thumbnail16:9 (panel kiri68%)
    ("AK-EP08_thumbnail_16x9.jpg", 1280, 720, "stone_glass.jpg", "left", [
        ("PULUHAN RIBU NOMOR ANTREAN", "BARLOW", 54, "IVORY", 40, 80),
        ("2009", "ANTON", 180, "RED", 40, 170),
        ("SEGELAS AIR — SEBUAH BATU", "BARLOW", 56, "IVORY", 40, 460),
        ("BALONGSARI", "ANTON", 72, "IVORY", 40, 560),
    ]),
    # ── Poster9:16 (panel bawah50%)
    ("AK-EP08_poster_9x16.jpg", 1080, 1920, "village_lane.jpg", "bottom", [
        ("ANTREAN YANG TIDAK BERHENTI", "BARLOW", 64, "IVORY", 48, 1030),
        ("2009", "ANTON", 240, "RED", 48, 1120),
        ("4 MENINGGAL — POLISI MENUTUP", "BARLOW", 68, "IVORY", 48, 1500),
        ("MUHAMMAD PONARI · JOMBANG", "BARLOW", 54, "GREY", 48, 1660),
    ]),
    # ── Kartu akhir16:9 (panel bawah50%)
    ("AK-EP08_endcard_16x9.jpg", 1280, 720, "village_lane.jpg", "bottom", [
        ("ODDCHAPTER", "ANTON", 110, "IVORY", 48, 800),
        ("KASUS NYATA · ARSIP ASLI", "BARLOW", 46, "RED", 48, 960),
        ("Footage stok: Coverr · Sumber: ANTARA · Inside Indonesia · Liputan6",
         "BARLOW", 34, "GREY", 48, 1300),
    ]),
]
