#!/usr/bin/env python3
"""Bangun timestamp caption OS-EP04 dari anchor jeda suara (VAD), bukan tebakan.

Versi awal membagi durasi dua klip TTS secara proporsional per kalimat. Pada
narasi ini voice-08 memberi jeda dramatis di tengah beberapa kalimat, sehingga
caption dapat muncul 1–3 detik sebelum kata diucapkan. Anchor di bawah diambil
dari jeda audio yang terukur; kata di dalam satu frasa lalu dibagi menurut panjang
ucapan. Ini bukan ASR dan sengaja didokumentasikan demikian.
"""
import json
import re
from pathlib import Path

OUT = Path(__file__).with_name("vo_alignment.json")
WORD_RE = re.compile(r"[A-Za-zÀ-ÿ0-9]+(?:['’-][A-Za-zÀ-ÿ0-9]+)?[,.?!:]?")

# (teks yang benar-benar diucapkan, mulai kata pertama, akhir kata terakhir)
# Hook v2 berakhir di 17,400. Isi vo_01 lama dipotong mulai 17,832 lalu dipadatkan
# 0,432 dtk di akhir chunk agar batas vo_02 tetap 86,320; karena itu anchor isi
# lama bergeser -0,432 dtk. Semua batas berasal dari silence/VAD -40 dB.
UNITS = [
    ("Kutukan Firaun itu bukan bukti sejarah.", 0.306, 3.381),
    ("Itu pembodohan publik: satu kematian dijual sebagai kutukan,", 3.724, 8.100),
    ("sementara orang-orang yang hidup puluhan tahun dihilangkan dari cerita.", 8.419, 12.525),
    ("Kalau kamu percaya, lihat dulu daftar yang sengaja tidak dicetak.", 13.142, 16.995),
    ("Sebelumnya, Howard Carter hampir kehabisan waktu.", 18.792, 21.674),
    ("Bertahun-tahun ia mencari makam seorang raja muda di Lembah Para Raja.", 22.325, 26.525),
    ("Lord Carnarvon membiayai satu musim penggalian terakhir.", 27.433, 30.673),
    ("November seribu sembilan ratus dua puluh dua, tim Carter menemukan tangga yang turun ke tanah.", 31.551, 36.817),
    ("Di ujungnya ada pintu bersegel.", 37.584, 39.513),
    ("Lihat detail kecil itu: pintu masih tertutup setelah lebih dari tiga ribu tahun.", 40.330, 45.809),
    ("Ruang makam dibuka bertahap.", 46.971, 48.453),
    ("Pada Februari seribu sembilan ratus dua puluh tiga, Carter dan timnya mulai masuk ke bagian paling penting dari penemuan itu.", 49.210, 55.948),
    ("Lalu, pada lima April, Carnarvon meninggal di Kairo setelah dirawat karena infeksi serius.", 56.880, 62.373),
    ("Dua fakta itu berdiri berurutan.", 63.293, 65.115),
    ("Makam dibuka.", 65.744, 66.631),
    ("Carnarvon meninggal.", 67.033, 68.079),
    ("Koran mengambil jarak pendek di antara keduanya dan mengisinya dengan satu kata: kutukan.", 68.913, 73.015),
    ("Coba perhatikan trik ceritanya.", 73.551, 76.611),
    ("Setelah satu nama masuk daftar kematian, daftar itu terus mencari nama berikutnya.", 77.379, 82.009),
    ("Tapi daftar orang yang selamat jarang ikut dicetak.", 82.759, 85.417),
    ("Howard Carter, orang yang memimpin penggalian, hidup sampai seribu sembilan ratus tiga puluh sembilan.", 86.553, 94.691),
    ("Lady Evelyn Herbert, yang hadir pada akses awal makam, meninggal pada seribu sembilan ratus delapan puluh.", 94.969, 100.180),
    ("Dokter Douglas Derry, yang memeriksa muminya, meninggal pada seribu sembilan ratus enam puluh sembilan.", 100.556, 106.762),
    ("Jadi pilihannya bukan antara percaya atau menertawakan kisah kuno.", 107.147, 111.805),
    ("Pertanyaannya lebih tajam: kutukan atau koran, mana yang membangun legenda ini?", 112.177, 117.784),
    ("Makamnya nyata.", 118.656, 119.595),
    ("Kematian Carnarvon juga nyata.", 120.086, 122.061),
    ("Tapi hubungan di antara keduanya tidak pernah terbukti.", 122.496, 125.280),
    ("Infeksi bisa menjelaskan satu kematian; judul besar menjelaskan kenapa kita mengingatnya sebagai kutukan.", 126.112, 132.388),
    ("Kita melakukan hal yang sama sampai sekarang.", 133.158, 135.310),
    ("Kita melihat dua peristiwa berdekatan, lalu merasa sudah menemukan penyebabnya.", 135.868, 140.273),
    ("Padahal kita belum menghitung semua orang yang tidak masuk cerita.", 140.990, 144.209),
    ("Kutukan itu bukan tulisan di dinding makam.", 145.152, 147.287),
    ("Ia adalah daftar kematian yang kehilangan daftar orang yang selamat.", 147.877, 151.447),
    ("Kalau satu kematian setelah satu penemuan terasa seperti bukti, siapa yang kita lupa hitung?", 152.187, 157.527),
]

words = []
for text, t0, t1 in UNITS:
    tokens = [m.group() for m in WORD_RE.finditer(text)]
    if not tokens:
        raise ValueError(f"Tidak ada kata pada unit: {text!r}")
    weights = [max(1, len(re.sub(r"[^A-Za-zÀ-ÿ0-9]", "", tok))) for tok in tokens]
    total = sum(weights)
    now = t0
    for token, weight in zip(tokens, weights):
        end = now + (t1 - t0) * weight / total
        words.append({"word": token, "start": round(now, 3), "end": round(end, 3)})
        now = end

OUT.write_text(json.dumps({
    "source": "VO internal voice-08; timing kata proporsional di dalam frasa yang di-anchor ke jeda audio/VAD (bukan ASR)",
    "words": words,
}, ensure_ascii=False, indent=1) + "\n")
print(f"{len(words)} words, end {words[-1]['end']:.3f} sec")
