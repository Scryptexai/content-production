"""
score_topic.py — gerbang topik: apakah cerita ini layak dibahas sekarang?

Lihat SKILLS/16_TOPIK_DAN_KURIKULUM.md. Skor 0–2 untuk 12 indikator (maks 24),
lalu tiga gerbang keras:

  1. skor ≥ 17
  2. ada kejanggalan ATAU dua pihak yang bertarung
  3. dokumen primer ≥ 1  — kalau tidak ada yang bisa dibaca, kita akan mengarang
  4. kelangkaan ≥ 1      — kalau semua orang sudah membahasnya, kita hanya jadi yang ke-98

Plus aturan tahap: selama kemampuan POV belum L4 (lihat kurikulum), hanya
tier `misteri` dan `kontroversi` yang boleh masuk. Tier `peristiwa` dan `umum`
ditahan — bukan karena jelek, tapi karena belum bisa kita bawakan dengan baik.

    python3 tools/score_topic.py
    python3 tools/score_topic.py --all        # tampilkan yang ditolak juga
    python3 tools/score_topic.py --strict     # keluar 1 kalau ada kandidat < 17
    python3 tools/score_topic.py -f jalur/lain.json
"""
import json
import sys
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
DEFAULT = ROOT / "11_CONTENT" / "01_IDEA" / "topik_kandidat.json"

BOBOT = {
    "kejanggalan": "ada satu hal yang tidak masuk akal dalam satu kalimat",
    "dua_pihak": "ada klaim resmi dan lawan klaimnya (bukan cuma 'belum terpecahkan')",
    "dokumen_primer": "ada arsip/laporan/putusan/transkrip yang bisa dibaca langsung",
    "bukti_visual": "ada objek, foto, rekaman, atau peta yang bisa ditunjuk",
    "taruhan": "ada manusia yang kehilangan sesuatu, bukan sekadar keanehan",
    "kelangkaan": "belum dibahas besar di YouTube Indonesia (2 = nyaris belum ada)",
    "celah": "pertanyaannya tidak selesai, bukan sekadar belum ditemukan",
    "pov_langka": "bisa dirumuskan satu kalimat sudut pandang yang jarang dipakai",
    "aktualitas": "masih hangat, atau ada dokumen baru yang dirilis",
    "etika": "aman: tidak menuduh tanpa putusan, tidak mengeksploitasi korban",
    "satu_pertanyaan": "bisa dipadatkan jadi satu pertanyaan 35–45 detik",
    "bahan_visual": "cukup bahan untuk 9 foto tanpa mengarang wajah korban",
}

TIER_BOLEH = {"misteri", "kontroversi"}
MIN_SKOR = 17


def muat(path):
    return json.loads(pathlib.Path(path).read_text())


def nilai(k):
    ind = k.get("indikator") or {}
    kurang = [n for n in BOBOT if n not in ind]
    salah = [n for n, v in ind.items() if not isinstance(v, int) or not 0 <= v <= 2]
    return ind, kurang, salah


def gerbang(k, ind):
    gagal = []
    total = sum(ind.values())
    if total < MIN_SKOR:
        gagal.append(f"skor {total} < {MIN_SKOR}")
    if ind.get("kejanggalan", 0) < 1 and ind.get("dua_pihak", 0) < 1:
        gagal.append("tidak ada kejanggalan dan tidak ada pihak yang bertarung")
    if ind.get("dokumen_primer", 0) < 1:
        gagal.append("tidak ada dokumen primer — naskah akan jadi karangan")
    if ind.get("kelangkaan", 0) < 1:
        gagal.append("topik sudah padat di YouTube Indonesia")
    tier = (k.get("tier") or "").strip().lower()
    if tier not in TIER_BOLEH:
        gagal.append(f"tier '{tier or '?'}' ditahan sampai kemampuan POV L4 "
                     f"(sekarang hanya {', '.join(sorted(TIER_BOLEH))})")
    if ind.get("etika", 0) < 1:
        gagal.append("etika: berisiko menuduh / mengeksploitasi")
    if ind.get("satu_pertanyaan", 0) < 1:
        gagal.append("tidak bisa dipadatkan jadi satu pertanyaan")
    if not k.get("pov"):
        gagal.append("belum ada kalimat POV")
    if not k.get("dokumen"):
        gagal.append("daftar dokumen kosong")
    return total, gagal


def main():
    argv = sys.argv[1:]
    path = DEFAULT
    if "-f" in argv:
        path = pathlib.Path(argv[argv.index("-f") + 1])
    tampil_semua = "--all" in argv
    strict = "--strict" in argv

    data = muat(path)
    kartu = data.get("kandidat", [])

    print(f"gerbang topik · {path.relative_to(ROOT) if str(path).startswith(str(ROOT)) else path}")
    print(f"{'id':5s} {'skor':6s} {'tier':12s} {'status':17s} kandidat")
    lolos, gagal_total = [], 0
    for k in kartu:
        ind, kurang, salah = nilai(k)
        if kurang or salah:
            print(f"{k.get('id','?'):5s}  !! indikator tidak lengkap: kurang {kurang} salah {salah}")
            continue
        total, alasan = gerbang(k, ind)
        status = "LOLOS" if not alasan else "TOLAK"
        # kartu yang memang ditandai "ditolak" adalah contoh, bukan kandidat:
        # ia tidak menghitung sebagai kegagalan gerbang.
        contoh = (k.get("status") or "") == "ditolak"
        if status == "TOLAK":
            if not contoh:
                gagal_total += 1
        else:
            lolos.append(k)
        if status == "TOLAK" and not tampil_semua and contoh:
            continue
        print(f"{k.get('id','?'):5s} {total:2d}/24  {k.get('tier','?'):12s} "
              f"{(k.get('status') or '-'):17s} {k.get('judul_kerja','')[:52]}")
        for a in alasan:
            print(f"        ✗ {a}")
        if not alasan and k.get("dokumen"):
            print(f"        dokumen: {', '.join(k['dokumen'][:3])}")
    print(f"\n{len(lolos)} kandidat lolos · {gagal_total} ditolak")

    if strict and gagal_total:
        print("::error::ada kandidat yang tidak lolos gerbang topik")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
