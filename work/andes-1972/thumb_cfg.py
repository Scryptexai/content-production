"""JOBS thumbnail 16:9 + poster 9:16 untuk AK-EP05 (Andes 1972, uji format 00F).

Sudut bicara mengikuti hook B1: tujuh hari tanpa makanan — angka 72 hari baru
disebut di subline, jawaban besar (keputusan) tidak dibocorkan di thumbnail.
Gambar dasar: img/thumb_andes.jpg & img/poster_andes.jpg (AI, tanpa orang, tanpa gore).
"""

JOBS = [
    ("AK-EP05_thumbnail_16x9.jpg", 1280, 720, "thumb_andes.jpg", "left", [
        ("ANDES · 13 OKTOBER 1972", "BARLOW", 28, "GREY", 56, 58),
        ("TUJUH HARI TANPA", "ANTON", 92, "IVORY", 56, 112),
        ("MAKANAN", "ANTON", 118, "RED", 56, 206),
        ("45 ORANG TERJEBAK DI ANDES", "BARLOW", 48, "IVORY", 58, 380),
        ("16 SELAMAT SETELAH 72 HARI", "BARLOW", 36, "GREY", 58, 442),
        ("ODDCHAPTER", "BARLOW", 30, "GREY", 58, 640),
    ]),
    ("AK-EP05_poster_9x16.jpg", 1080, 1920, "poster_andes.jpg", "bottom", [
        ("ANDES · 13 OKTOBER 1972", "BARLOW", 42, "GREY", 68, 998),
        ("TUJUH HARI TANPA", "ANTON", 92, "IVORY", 64, 1058),
        ("MAKANAN", "ANTON", 150, "RED", 64, 1156),
        ("45 ORANG TERJEBAK DI ANDES", "BARLOW", 52, "IVORY", 68, 1348),
        ("16 SELAMAT SETELAH 72 HARI", "BARLOW", 38, "GREY", 68, 1424),
        ("ODDCHAPTER", "BARLOW", 34, "GREY", 68, 1790),
    ]),
]
