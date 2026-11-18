#!/usr/bin/env python3
"""build_short_meta.py — metadata 06_UPLOAD/EP01SB_S{n}.json untuk Shorts hasil potong.

Sumber: work/shorts/EP01SB_S{n}.mp4 (hasil tools/make_shorts.py) + thumbnail
thumbs/EP01SB_S{n}_thumb.jpg (hasil tools/make_short_thumbs.py, diganti nama jadi
…_thumbnail.jpg karena fetch_masters.py mencari nama itu).

Kenapa metadata ditulis oleh skrip, bukan tangan: size_bytes + sha256 harus
persis sama dengan file yang benar-benar diunggah ke Drive. Kalau beda satu byte,
upload_zernio.py berhenti sebelum mengirim apa pun.
"""
import hashlib
import json
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
META_DIR = ROOT / "11_CONTENT" / "06_UPLOAD"
THUMBS = META_DIR / "thumbs"
SHORTS = ROOT.parent / "work" / "shorts"
LONG = "https://www.youtube.com/watch?v=mhI-Q3uVy1g"

ITEMS = [
    {
        "id": "S1",
        "drive": "1kzRloG9qbr2zxYCewKWvVq-E3iSBs3Ji",
        "title": "1797: Teori Illuminati Lahir dari Buku, Bukan dari Bukti",
        "hook": "Buku 1797 itu yang melahirkan teori, bukan bukti.",
        "alt": ["1797: Dua Buku yang Melahirkan Teori Illuminati",
                "Teori Illuminati Tidak Berasal dari Bukti, Tapi dari Buku"],
        "body": ("Pada 1797, Augustin Barruel di Prancis dan John Robison di Skotlandia "
                 "menerbitkan buku yang menghubungkan Illuminati dengan revolusi dan kekuasaan gelap.\n\n"
                 "Organisasinya sendiri sudah dibubarkan pemerintah Bavaria pada 1785. "
                 "Tapi bukunya dibaca jauh lebih luas daripada dokumen aslinya: diterjemahkan, "
                 "dikutip, lalu diulang selama dua abad.\n\n"
                 "Itu sebabnya teorinya bertahan lebih lama daripada organisasinya."),
        "tags": ["illuminati", "sejarah", "barruel 1797", "robison 1797",
                 "teori konspirasi", "oddchapter"],
    },
    {
        "id": "S2",
        "drive": "1zIhUl5yY685cIqzjWt3rIb3y-M0ADRsk",
        "title": "1776: Mata Satu dan Piramida Sudah Ada Sebelum Illuminati",
        "hook": "Kalau mata satu dan piramida sudah ada lebih dulu, siapa yang meminjam?",
        "alt": ["Simbol Illuminati Itu Dipinjam, Bukan Diciptakan",
                "Mata Satu Bukan Simbol Illuminati — Itu Simbol yang Dipinjam"],
        "body": ("Mata satu di atas piramida bukan ciptaan Illuminati. Lambang itu sudah dipakai "
                 "ordo dan negara jauh sebelumnya; segel resmi Amerika dicetak 1782.\n\n"
                 "Yang baru adalah maknanya. Setelah teori 1797 menyebar, lambang lama itu "
                 "ditempeli cerita baru, lalu dianggap bukti kesinambungan.\n\n"
                 "Simbol bisa dipinjam siapa saja. Simbol bukan bukti."),
        "tags": ["illuminati", "simbol", "mata satu", "piramida", "segel dollar", "oddchapter"],
    },
    {
        "id": "S3",
        "drive": "1a3WS80nl_cxa2fi_zUWzolVNcnzQmUJP",
        "title": "1785: Dokumen yang Sama, Dua Kesimpulan yang Berlawanan",
        "hook": "Dua kesimpulan dari satu dokumen 1785. Mana yang benar?",
        "alt": ["Tidak Ada Bukti Setelah 1800 — Bubar atau Bersembunyi?",
                "Dua Cara Membaca Bukti Illuminati yang Sama"],
        "body": ("Satu pihak membaca: organisasi bubar 1785, dan semua yang datang setelahnya "
                 "hanya meminjam namanya.\n\n"
                 "Pihak lain membaca: tidak adanya dokumen setelah 1800 justru bukti "
                 "bahwa mereka berhasil menghilang.\n\n"
                 "Dua-duanya bersandar pada ketiadaan yang sama, dan dua-duanya punya celah: "
                 "yang pertama tidak bisa menjelaskan kenapa ceritanya bertahan, "
                 "yang kedua tidak punya satu dokumen pun untuk mendukungnya."),
        "tags": ["illuminati", "bukti sejarah", "1785", "edikt bayern", "sejarah", "oddchapter"],
    },
]


def main():
    for it in ITEMS:
        video = SHORTS / f"EP01SB_{it['id']}.mp4"
        data = video.read_bytes()
        duration = float(subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "csv=p=0", str(video)],
            capture_output=True, text=True, check=True).stdout.strip())

        thumb_name = f"EP01SB_{it['id']}_thumbnail.jpg"
        target = THUMBS / thumb_name
        if not target.exists():
            src = THUMBS / f"EP01SB_{it['id']}_thumb.jpg"
            src.replace(target)

        desc = (it["hook"] + "\n\n" + it["body"] +
                "\n\nEpisode penuh (5:42): " + LONG +
                "\n\nODDCHAPTER — sejarah yang dicek ulang, bukan dikutip ulang.\n"
                "#shorts #illuminati #sejarah #oddchapter")

        meta = {
            "episode": f"EP01SB_{it['id']}",
            "series": "SB-EP01",
            "kind": "short",
            "video": video.name,
            "thumbnail": thumb_name,
            "title": it["title"],
            "title_alt": it["alt"],
            "hook": it["hook"],
            "description": desc,
            "tags": it["tags"],
            "first_comment": "Setelah lihat potongan ini, masih yakin simbol sama dengan bukti?",
            "categoryId": "27",
            "madeForKids": False,
            "containsSyntheticMedia": True,
            "visibility": "public",
            "drive_file_id": it["drive"],
            "duration_seconds": round(duration, 3),
            "size_bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
            "cut_from": {"master_drive_file_id": "1jSDnEw70IfrqpCn1UVahqB75Tc6hhvJG"},
        }
        out = META_DIR / f"EP01SB_{it['id']}.json"
        out.write_text(json.dumps(meta, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(f"{meta['episode']}  {len(it['title'])} char judul  {len(desc)} char desc  "
              f"{duration:.1f} dtk  {len(data)} byte  {meta['sha256'][:12]}…")


if __name__ == "__main__":
    main()
