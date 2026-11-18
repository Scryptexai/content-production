#!/usr/bin/env python3
"""Metadata unggah SB-EP02 (master 8:12) + lima Shorts.

size_bytes dan sha256 dibaca dari berkas yang benar-benar ada, karena
upload_zernio.py menolak mengunggah kalau angka di metadata tidak sama dengan
berkas di Drive.

    python3 tools/build_meta_sbep02.py --master <path.mp4> --drive <file_id>
    python3 tools/build_meta_sbep02.py --shorts          # setelah Shorts dirender
"""
import argparse
import hashlib
import json
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
REPO = ROOT.parent
UPL = ROOT / "11_CONTENT" / "06_UPLOAD"
QUEUE = UPL / "queue"
THUMBS = UPL / "thumbs"
SHORTS = REPO / "work" / "shorts"

MASTER = ROOT / "10_FILM" / "remotion" / "output" / "episodes" / "SB-EP02_MH370_1920x1080_master.mp4"

TITLE = "MH370 Terlacak 7 Kali Setelah Transponder Mati. 12 Tahun, Nol Bangkai."
TITLE_ALT = [
    "7 Kali Terlacak pada 2014, Nol Bangkai pada 2026: MH370 Masih di Mana?",
    "MH370: 7 Handshake, 140.000 km², 3 Serpihan. Nol Badan Pesawat.",
]
HOOK = ("Pesawat itu terlacak 7 kali setelah transpondernya dimatikan. Kenapa 12 tahun "
        "kemudian kita masih tidak punya titiknya?")

DESC = HOOK + """

Pesawat MH370 tidak hilang tanpa jejak. Ia terlacak tujuh kali — 02:25 sampai 08:19 pagi, satu per jam — setelah transponder dan pengirim data otomatisnya mati.

Masalahnya, tujuh pelacakan itu tidak membawa posisi. Tidak ada GPS, tidak ada ketinggian, tidak ada arah. Yang tersisa dua angka: BTO (selisih waktu sinyal pergi-pulang, jadi jarak ke satelit) dan BFO (pergeseran frekuensi karena gerak). Tujuh BTO memberi tujuh lingkaran. BFO memilih utara atau selatan.

Seluruh 12 tahun pencarian berdiri di atas itu.

BAB
""" + """00:23  Apa yang bisa dibuktikan
00:48  Satu lewat satu: 8 Maret 2014
01:54  Tujuh handshake tanpa posisi
03:19  Tiga gelombang pencarian
04:33  Tiga potong yang dikonfirmasi
05:29  Masih dipegang orang, atau sudah kosong?
06:31  Perpanjangan sampai 30 Juni 2027
07:14  Yang tidak bisa dipisahkan data

ANGKA YANG DIPAKAI
• 239 orang: 227 penumpang, 12 awak
• 01:19 "Good night Malaysian three seven zero"
• 01:21 transponder mati di sekitar IGARI
• 02:22 kontak radar militer terakhir di MEKAR
• 02:25–08:19 tujuh handshake Inmarsat
• 120.000 km² (2014–17) · 112.000 km² (2018) · 15.000 km² target 2025–26
• 28 hari, ±7.571 km² pada fase 2025–26
• 151 hari di laut dan >140.000 km² dipetakan (Ocean Infinity)
• 3 serpihan dikonfirmasi: flaperon Réunion, flap Mauritius, flap kanan Pemba

SUMBER
• Laporan AAIB Malaysia (2018) dan pengumuman 8 Maret 2026
• Dokumen Inmarsat: tujuh handshake Inmarsat-3 F1, 64,5° E
• Pernyataan Ocean Infinity dan Kementerian Transportasi Malaysia (2025–2026)
• Catatan debris: Réunion (29 Jul 2015), Mauritius (10 Mei 2016), Pemba (20 Jun 2016)

Kalau semua yang menjawab sinyal itu diam, pesawat lo ada di mana?

#mh370 #malaysiaairlines #penerbangan #oddchapter #documentary"""

TAGS = ["mh370", "malaysia airlines", "mh370 terbaru 2026", "ocean infinity",
        "inmarsat bto bfo", "penerbangan", "sejarah penerbangan", "oddchapter",
        "documentary indonesia", "pesawat hilang"]

COMMENT = ("Menurut lo: di menit terakhir pesawatnya masih dipegang orang, atau sudah "
           "kosong? Dua-duanya memakai data yang sama persis.")


def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration,size",
                          "-of", "json", str(path)], capture_output=True, text=True).stdout
    return json.loads(out)["format"]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--drive", default="")
    ap.add_argument("--shorts", action="store_true")
    args = ap.parse_args()
    QUEUE.mkdir(parents=True, exist_ok=True)

    if not args.shorts:
        if not MASTER.exists():
            raise SystemExit(f"master belum ada: {MASTER}")
        f = probe(MASTER)
        size = int(f["size"])
        meta = {
            "episode": "SB-EP02",
            "video": MASTER.name,
            "thumbnail": "SB-EP02_thumbnail.jpg",
            "title": TITLE,
            "title_alt": TITLE_ALT,
            "hook": HOOK,
            "description": DESC,
            "tags": TAGS,
            "first_comment": COMMENT,
            "categoryId": "27",
            "madeForKids": False,
            "containsSyntheticMedia": True,
            "visibility": "public",
            "drive_file_id": args.drive,
            "duration_seconds": round(float(f["duration"]), 3),
            "size_bytes": size,
            "sha256": sha256(MASTER),
        }
        (UPL / "SB-EP02.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1) + "\n")
        print(f"06_UPLOAD/SB-EP02.json  {size / 1e6:.1f} MB  {meta['duration_seconds']}s  "
              f"judul {len(TITLE)} char")
        print(f"judul  : {TITLE}")
        print(f"hook   : {HOOK}")
        return 0

    # Shorts: metadata per Short, ukuran dan sha dari hasil render
    spec = json.loads((SHORTS / "shorts_sb-ep02.json").read_text())
    titles = {
        "S1": ("MH370 Terlacak 7 Kali Setelah Transponder Mati — dan Tetap Tak Ada Titiknya",
               "Pesawat ini terlacak 7 kali setelah transpondernya mati. Kenapa tetap tak ada titiknya?"),
        "S2": ("Satu Angka Doppler Membuang Seluruh Koridor Utara MH370",
               "Satu angka Doppler membuang seluruh koridor utara. Busurnya jadi dasar pencarian."),
        "S3": ("Pencarian Termahal Dunia, Serpihan Pertamanya Ditemukan Tukang Bersih Pantai",
               "Pencarian termahal dalam sejarah penerbangan. Serpihan pertamanya ditemukan tukang bersih pantai."),
        "S4": ("MH370: 28 Hari, 7.571 km², Hasilnya Nol",
               "28 hari, 7.571 kilometer persegi. Hasilnya nol bangkai."),
        "S5": ("Data MH370 Sama Persis, Dua Titik Jatuh Berbeda",
               "Data sama persis, dua titik jatuh berbeda. Pembedanya cuma kecepatan turun."),
    }
    for row in spec:
        sid = row["id"]
        path = SHORTS / row["file"]
        f = probe(path)
        title, hook = titles[sid]
        meta = {
            "episode": f"SB-EP02_{sid}",
            "video": path.name,
            "thumbnail": f"SB-EP02_{sid}_thumbnail.jpg",
            "title": title,
            "hook": hook,
            "description": f"{hook}\n\nPotongan dari episode panjang MH370: SATU BUSUR SATELIT.\n\n"
                           f"#mh370 #shorts #oddchapter",
            "tags": ["mh370", "shorts", "penerbangan", "oddchapter", "ocean infinity"],
            "categoryId": "27",
            "madeForKids": False,
            "containsSyntheticMedia": True,
            "visibility": "public",
            "drive_file_id": "",
            "duration_seconds": round(float(f["duration"]), 3),
            "size_bytes": int(f["size"]),
            "sha256": sha256(path),
        }
        (UPL / f"SB-EP02_{sid}.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1) + "\n")
        print(f"06_UPLOAD/SB-EP02_{sid}.json  {meta['size_bytes'] / 1e6:.1f} MB  {title}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
