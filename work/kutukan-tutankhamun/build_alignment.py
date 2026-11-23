#!/usr/bin/env python3
"""Buat timestamp kata konservatif untuk VO internal tanpa output alignment dari TTS.

Setiap klip TTS diketahui durasinya. Kalimat diberi jeda yang terdengar wajar;
sisa waktu dibagi pada kata berdasarkan panjang ejaan. Ini lebih jujur daripada
membuat timestamp seolah datang dari ASR, dan cukup untuk caption per kelompok
pada draft visual. QC akhir dilakukan pada frame/caption master.
"""
import json, re
from pathlib import Path

OUT = Path(__file__).with_name("vo_alignment.json")
DURS = [86.32, 71.64]
CHUNKS = [
"""Lord Carnarvon meninggal kurang dari dua bulan setelah ruang makam Tutankhamun dibuka. Koran lalu memberi nama yang jauh lebih besar dari kematiannya: kutukan Firaun. Kalau itu benar kutukan, kenapa orang yang masuk makam bersamanya hidup puluhan tahun? Sebelumnya, Howard Carter hampir kehabisan waktu. Bertahun-tahun ia mencari makam seorang raja muda di Lembah Para Raja. Lord Carnarvon membiayai satu musim penggalian terakhir. November seribu sembilan ratus dua puluh dua, tim Carter menemukan tangga yang turun ke tanah. Di ujungnya ada pintu bersegel. Lihat detail kecil itu: pintu masih tertutup setelah lebih dari tiga ribu tahun. Ruang makam dibuka bertahap. Pada Februari seribu sembilan ratus dua puluh tiga, Carter dan timnya mulai masuk ke bagian paling penting dari penemuan itu. Lalu, pada lima April, Carnarvon meninggal di Kairo setelah dirawat karena infeksi serius. Dua fakta itu berdiri berurutan. Makam dibuka. Carnarvon meninggal. Koran mengambil jarak pendek di antara keduanya dan mengisinya dengan satu kata: kutukan. Coba perhatikan trik ceritanya. Setelah satu nama masuk daftar kematian, daftar itu terus mencari nama berikutnya. Tapi daftar orang yang selamat jarang ikut dicetak.""",
"""Howard Carter, orang yang memimpin penggalian, hidup sampai seribu sembilan ratus tiga puluh sembilan. Lady Evelyn Herbert, yang hadir pada akses awal makam, meninggal pada seribu sembilan ratus delapan puluh. Dokter Douglas Derry, yang memeriksa muminya, meninggal pada seribu sembilan ratus enam puluh sembilan. Jadi pilihannya bukan antara percaya atau menertawakan kisah kuno. Pertanyaannya lebih tajam: kutukan atau koran, mana yang membangun legenda ini? Makamnya nyata. Kematian Carnarvon juga nyata. Tapi hubungan di antara keduanya tidak pernah terbukti. Infeksi bisa menjelaskan satu kematian; judul besar menjelaskan kenapa kita mengingatnya sebagai kutukan. Kita melakukan hal yang sama sampai sekarang. Kita melihat dua peristiwa berdekatan, lalu merasa sudah menemukan penyebabnya. Padahal kita belum menghitung semua orang yang tidak masuk cerita. Kutukan itu bukan tulisan di dinding makam. Ia adalah daftar kematian yang kehilangan daftar orang yang selamat. Kalau satu kematian setelah satu penemuan terasa seperti bukti, siapa yang kita lupa hitung?""",
]

sent_re = re.compile(r"[^.!?]+[.!?]")
word_re = re.compile(r"[A-Za-zÀ-ÿ0-9]+(?:['’-][A-Za-zÀ-ÿ0-9]+)?[,.?!:]?")
all_words = []
offset = 0.0
for ci, (text, dur) in enumerate(zip(CHUNKS, DURS)):
    sentences = sent_re.findall(text)
    parsed = [[m.group() for m in word_re.finditer(s)] for s in sentences]
    # jeda kalimat: klausa pendek, sedikit lebih panjang sesudah tanda tanya.
    pauses = [0.18 + (0.09 if s.rstrip().endswith('?') else 0.0) for s in sentences]
    pauses[-1] = 0.05
    speak = dur - sum(pauses)
    weights = [sum(max(1, len(re.sub(r"[^A-Za-zÀ-ÿ0-9]", "", w))) for w in ws) + 4
               for ws in parsed]
    total_weight = sum(weights)
    t = offset
    for sent, ws, weight, pause in zip(sentences, parsed, weights, pauses):
        sd = speak * weight / total_weight
        wts = [max(1, len(re.sub(r"[^A-Za-zÀ-ÿ0-9]", "", w))) for w in ws]
        sw = sum(wts)
        for word, wt in zip(ws, wts):
            end = t + sd * wt / sw
            all_words.append({"word": word, "start": round(t, 3), "end": round(end, 3)})
            t = end
        t += pause
    offset += dur

OUT.write_text(json.dumps({
    "source": "VO internal voice-08; timestamp kata proporsional per kalimat dari durasi TTS chunks (draft caption alignment)",
    "words": all_words,
}, ensure_ascii=False, indent=1) + "\n")
print(f"{len(all_words)} words, end {all_words[-1]['end']:.3f} sec")
