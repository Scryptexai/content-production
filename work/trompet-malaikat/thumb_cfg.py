"""Thumbnail/poster OS-EP03 — Trompet malaikat (Seneca Guns).

Palet standar ODDCHAPTER. Sumber gambar: foto AI langit badai dengan
siluet trompet (tanpa orang).
"""

JOBS = [
    # ── Thumbnail 16:9 (panel kiri 68%)
    ("OS-EP03_thumbnail_16x9.jpg", 1280, 720, "hook_langit_trompet.png", "left", [
        ("SUARA TROMPET DARI LANGIT", "BARLOW", 54, "IVORY", 40, 80),
        ("TROMPET MALAIKAT", "ANTON", 170, "RED", 40, 170),
        ("SENECA GUNS · DAN SENECA · NEW YORK", "BARLOW", 52, "IVORY", 40, 460),
        ("DIDENGAR SEPANJANG PESISIR TIMUR", "ANTON", 66, "IVORY", 40, 560),
    ]),
    # ── Poster 9:16 (panel bawah 50%)
    ("OS-EP03_poster_9x16.jpg", 1080, 1920, "hook_langit_trompet.png", "bottom", [
        ("SUARA TROMPET DARI LANGIT", "BARLOW", 64, "IVORY", 48, 1030),
        ("TROMPET", "ANTON", 150, "RED", 48, 1140),
        ("MALAIKAT", "ANTON", 150, "RED", 48, 1290),
        ("SENECA GUNS", "BARLOW", 76, "IVORY", 48, 1520),
        ("DAN SENECA · NEW YORK · PESISIR TIMUR", "BARLOW", 46, "GREY", 48, 1660),
    ]),
    # ── Kartu akhir 16:9 (panel bawah 50% → mulai y=360; teks wajib < 720)
    ("OS-EP03_endcard_16x9.jpg", 1280, 720, "hook_langit_trompet.png", "bottom", [
        ("ODDCHAPTER", "ANTON", 110, "IVORY", 48, 395),
        ("FENOMENA NYATA · SENECA GUNS", "BARLOW", 46, "RED", 48, 545),
        ("Footage stok: Coverr · Peta: © Esri · HERE · Garmin · OpenStreetMap contributors",
         "BARLOW", 34, "GREY", 48, 655),
    ]),
]
