# 00C — MESIN LIMA EFEK

Lima hal yang kamu minta bukan lima trik. Masing-masing punya penyebab yang
sudah diteliti, dan masing-masing bisa gagal dengan cara yang berbeda. Dokumen
ini memetakan efek → mekanisme → perangkat → cara memeriksanya.

Kalau satu episode tidak memenuhi kelima baris di bawah, episode itu belum jadi —
berapa pun bagusnya kalimatnya.

---

## 1 · Berhenti scroll dalam 1–3 detik

**Mekanisme:** pola terganggu. Otak berhenti pada hal yang *hampir* normal.
Bukan kejutan besar — kejutan besar justru dicap iklan.

**Perangkat:** kalimat pertama menyebut satu fakta biasa, lalu satu hal yang
tidak masuk akal, tanpa konteks dan tanpa penjelasan. Maksimal 14 kata.

| gagal | berhasil |
|---|---|
| "Ada misteri yang belum terpecahkan di Skotlandia." | "Lampu sudah dibersihkan, minyak penuh. Tiga orangnya hilang." |

Yang pertama meminta perhatian. Yang kedua **membuat penonton menghitung sendiri**
bahwa ada yang tidak beres.

**Periksa:** ≤ 14 kata · mengandung satu benda konkret · tidak mengandung kata
"misteri", "rahasia", "aneh", "menakjubkan" (kata-kata itu meminta, bukan menunjukkan).

---

## 2 · Merasa ada yang salah, belum paham apa

**Mekanisme:** information gap (Loewenstein, 1994). Rasa penasaran bukan minat —
ia rasa tidak nyaman karena tahu ada yang hilang. Tiga temuan yang menentukan:

1. Gap harus **spesifik**, bukan samar. Hook kabur ("ini akan mengubah caramu
   melihat segalanya") tidak menciptakan gap karena penonton tidak punya titik
   pembanding. Tanpa titik pembanding, tidak ada yang bisa merasa "hampir tahu".
2. Intensitas tertinggi saat penonton **hampir tahu** — "ujung lidah". Bukan saat
   mereka tidak tahu apa-apa; total ignorance menghasilkan ketidakpedulian.
3. Gap yang terlalu besar membuat orang menyerah, bukan bertahan.

**Perangkat:** sebut hampir seluruh gambar, tahan **satu keping**, dan biarkan
penonton bisa menyebutkan keping yang hilang itu dalam kepalanya sendiri.

| gagal (samar) | berhasil (spesifik, satu keping hilang) |
|---|---|
| "Sembilan pendaki hilang secara misterius." | "Tenda itu disobek dari dalam, dengan pisau. Sembilan orang keluar tanpa alas kaki." |

Yang berhasil menyebut pelaku arah (dari dalam), alat (pisau), dan korban (sembilan
orang tanpa alas kaki). Yang hilang cuma satu: **kenapa keluar**. Itu satu keping,
dan penonton bisa menamainya.

**Periksa:** ada field `celah` — satu pertanyaan yang harus dipegang penonton, ≤ 18
kata, dan pertanyaan itu **dijawab di turn**, bukan dibiarkan menggantung.

---

## 3 · Bertahan karena ingin tahu jawabannya

**Mekanisme:** open loop + Zeigarnik. Tugas yang belum selesai diingat jauh lebih
kuat daripada yang selesai (Zeigarnik, 1927: sekitar 90 % lebih sering diingat).
Dua detail penting:

- Efeknya **paling kuat kalau interrupt terjadi dekat penyelesaian** — 80 % lebih
  kuat daripada 20 %. Artinya: jangan menutup gap di tengah. Tahan sampai 3/4 akhir.
- Kalau penonton dibuat **punya rencana** untuk menyelesaikannya, ketegangannya
  turun. Karena itu jangan pernah memberi "nanti aku jelaskan di akhir" — itu
  membereskan rasa penasaran sebelum waktunya.

**Perangkat:** setiap beat menutup satu pertanyaan kecil dan membuka satu yang
lebih besar. Satu episode, satu loop. Kalau ada dua loop, keduanya melemah.

**Periksa:** `celah` hanya boleh muncul di 3 detik pertama dan baru dijawab di
segmen `turn` (detik 32–47). Tidak boleh ada jawaban di bagian tension.

---

## 4 · Kejutan yang mengubah pemahaman

**Mekanisme:** rekognisi, bukan informasi baru. Kejutan yang benar terasa
**tidak terduga saat itu, tapi tak terhindarkan sedetik kemudian**. Kalau turn
menambah fakta baru, itu plot twist — penonton merasa ditipu, bukan dibalik.

**Perangkat:** satu `tanaman` yang ditanam di hook. Turn tidak menambah apa pun;
turn **membaca ulang** tanaman itu.

| episode | tanaman | dibaca ulang sebagai |
|---|---|---|
| EP01 | satu set pakaian tahan air tertinggal | pekerjaan sudah selesai; mereka keluar sesudahnya — dan kalimat dramatis di buku harian itu ditambahkan puluhan tahun kemudian |
| EP04 | pintu tidak dikunci, tangki penuh | mereka tidak terjebak; mereka memilih menjauh dari pertolongan |
| EP19 | pohon rebah menjauhi satu titik | tidak ada kawah karena bendanya tidak pernah menyentuh tanah |

**Periksa:** `turn` tidak boleh memuat angka, nama, atau benda yang belum muncul
sebelum detik ke-30. Kalau ada, itu fakta baru → gagal.

---

## 5 · Mengingat ceritanya setelah selesai

**Mekanisme:** dua hal yang saling melengkapi.

- **Peak-end rule:** ingatan atas sebuah pengalaman ditentukan oleh momen paling
  kuat dan oleh akhirnya — bukan oleh rata-ratanya. Maka: puncak emosi harus
  berada tepat di turn, dan 13 detik terakhir tidak boleh datar.
- **Efek isolasi (von Restorff):** yang berbeda dari sekelilingnya yang diingat.
  Satu gambar yang tidak mirip apa pun di video itu akan bertahan; lima gambar
  yang mirip akan saling menghapus.

**Perangkat:** satu `gambar_melekat` — satu benda, satu frame, bisa digambarkan
dalam satu kalimat — dan kalimat penutup yang **memanggil kembali kata dari hook**.
Penutup yang tidak memanggil apa pun adalah penutup yang bisa dipotong tanpa ada
yang sadar.

**Periksa:** `gambar_melekat` ≤ 14 kata · kalimat `loop` berbagi minimal satu kata
bermakna dengan hook (dicek otomatis oleh `tools/check_story.py`).

---

## Ringkasan yang dipakai sebagai gerbang

| # | efek | perangkat | field | diperiksa oleh |
|---|---|---|---|---|
| 1 | berhenti scroll | pola terganggu, ≤14 kata, tanpa kata minta | `hook` | check_story: panjang + kata terlarang |
| 2 | ada yang salah | gap spesifik, satu keping hilang | `celah` | check_story: ada + ≤18 kata |
| 3 | bertahan | satu loop, ditutup di turn | `celah` + `beats` | check_story: tidak dijawab sebelum turn |
| 4 | kejutan | tanaman dibaca ulang, tanpa fakta baru | `tanaman` + `turn` | check_story: larangan angka/nama baru |
| 5 | diingat | satu gambar + echo | `gambar_melekat` + `loop` | check_story: echo kata |

---

## Kesalahan yang paling sering terjadi (dan sudah saya lakukan)

1. **Mengira samar = misterius.** Justru sebaliknya: hook samar tidak menciptakan
   gap. Yang menciptakan gap adalah hook yang hampir lengkap.
2. **Menutup gap terlalu cepat.** Kalau jawaban datang di detik ke-25, 35 detik
   sisanya jadi penutup yang membosankan.
3. **Turn yang menambah fakta.** Terasa seperti twist murah dan memutus kontrak
   dengan penonton.
4. **Penutup yang menjelaskan makna.** "Jadi, intinya adalah…" membunuh efek
   ingat. Penutup harus memanggil gambar, bukan menyimpulkan pelajaran.
5. **Lima gambar yang setara.** Tanpa satu gambar yang berbeda, tidak ada yang
   diingat.

---

## Rujukan

- George Loewenstein, "The Psychology of Curiosity: A Review and Reinterpretation",
  *Psychological Bulletin*, 1994 — gap spesifik, "hampir tahu", gap terlalu besar
  membuat orang menyerah.
  Ringkasan: https://chunks.app/blog/the-curiosity-gap-explained ·
  https://uidcaption.com/blog/psychology-of-a-good-hook/
- Bluma Zeigarnik, "On Finished and Unfinished Tasks", 1927 — tugas terputus
  diingat ~90 % lebih sering; efek terkuat saat interrupt dekat penyelesaian.
  https://whennotesfly.com/concepts/psychology-behavior/zeigarnik-effect-explained
- Peak-end rule dan efek isolasi (von Restorff) sebagai dasar ingatan atas
  pengalaman: https://www.cognifit.com/peak-end-rule ·
  https://monsoonfish.com/cognilense/zeigarnik-effect/
- Kerangka cerita (komplikasi → wawasan → resolusi): lihat `00B_KERANGKA_STORYTELLING.md`.
