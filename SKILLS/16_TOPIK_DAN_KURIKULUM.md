# 16 · Topik & kurikulum — yang dibahas, dan urutan menaikinya

Dokumen ini menjawab satu keluhan pemilik (16 Nov 2026): **topiknya** yang kurang,
bukan bahasanya. Isinya tiga hal: gerbang topik (indikator + skor), uji POV, dan
tangga kualitas per episode.

Diperiksa mesin: `python3 tools/score_topic.py` (kartu topik di
`11_CONTENT/01_IDEA/topik_kandidat.json`) dan `tools/check_info_design.py` (A–G).

---

## 1 · Prinsip yang dipakai

1. **Topik tidak pernah menarik atau membosankan sendirian.** Yang menarik adalah
   sudut pandang: satu kalimat yang membuat penonton melihat hal biasa dari tempat
   yang belum pernah ia berdiri.
2. **Tetapi POV mahal.** POV tajam butuh kemampuan menyusun kronologi, memilih
   bukti, dan menahan kesimpulan. Selama itu belum ada, topik umum akan tenggelam —
   bukan karena topiknya, karena kita belum bisa mengangkatnya.
3. **Karena itu urutannya dibalik.** Di awal, ambil topik yang **sudah** punya
   kejanggalan dan dua pihak yang bertarung: misteri dan kontroversi. Keduanya
   memberi tenaga tanpa menuntut POV yang belum kita punya. Topik umum ditahan
   sampai kemampuan POV lulus.
4. **Setiap episode menaikkan satu keterampilan, dan menutup satu kelemahan
   episode sebelumnya.** Tidak ada episode yang hanya "mengulang yang sudah bisa".
5. **Tidak ada naskah sebelum dokumennya dibaca.** Kalau topik tidak punya arsip,
   laporan, putusan, atau transkrip, ia bukan misteri — ia desas-desus.

## 2 · Dua belas indikator (skor 0–2, maksimum 24)

| indikator | yang diukur | kenapa penting untuk Shorts |
|---|---|---|
| `kejanggalan` | ada satu hal yang tidak masuk akal dalam satu kalimat | kalau tidak bisa ditulis dalam satu kalimat, hook-nya tidak akan ada |
| `dua_pihak` | ada klaim resmi dan lawan klaimnya | ini yang membuat penonton berhenti dan ikut menimbang |
| `dokumen_primer` | arsip/laporan/putusan/transkrip yang bisa dibaca | membedakan investigasi dari cerita ulang |
| `bukti_visual` | objek, foto, rekaman, peta | 9 foto per episode harus punya dasar |
| `taruhan` | ada manusia yang kehilangan sesuatu | tanpa ini, penonton menonton, bukan ikut |
| `kelangkaan` | belum dibahas besar di YouTube Indonesia | topik ke-98 tidak bisa menang dari topik pertama |
| `celah` | pertanyaan tidak selesai, bukan sekadar belum ditemukan | celah = komentar = distribusi |
| `pov_langka` | bisa dirumuskan satu kalimat POV yang jarang | satu-satunya pembeda jangka panjang |
| `aktualitas` | masih hangat, atau ada dokumen baru | bukan syarat, tapi menambah tenaga |
| `etika` | tidak menuduh tanpa putusan; tidak mengeksploitasi korban | satu episode tidak etis bisa mematikan kanal |
| `satu_pertanyaan` | bisa dipadatkan jadi satu pertanyaan 35–45 dtk | Shorts tidak punya ruang untuk tiga pertanyaan |
| `bahan_visual` | cukup bahan untuk 9 foto tanpa mengarang wajah | menghindari rekonstruksi palsu |

**Gerbang (keras, bukan saran):**

- skor total **≥ 17/24**
- `kejanggalan ≥ 1` **atau** `dua_pihak ≥ 1`
- `dokumen_primer ≥ 1` — tanpa dokumen, naskah akan mengarang
- `kelangkaan ≥ 1` — kalau semua orang sudah membahasnya, kita tidak punya alasan
- `etika ≥ 1`, `satu_pertanyaan ≥ 1`, `pov` dan `dokumen` terisi

**Aturan tahap:** selama kemampuan POV belum mencapai **L4**, hanya tier
`misteri` dan `kontroversi` yang boleh masuk. Tier `peristiwa` masuk satu per satu
sebagai latihan, tier `umum` **ditahan**.

## 3 · Delapan tanda topik akan jatuh membosankan

Dipakai untuk menolak sebelum menulis, bukan sesudah render.

1. Bisa diringkas tanpa satu pun angka atau tanggal.
2. Tidak ada pihak yang membantah apa pun (semua sepakat → tidak ada ketegangan).
3. Klaimnya hanya "belum terpecahkan" — bukan "ada dua jawaban yang sama kuat".
4. Bahannya hanya dari video lain, bukan arsip.
5. Tokoh utamanya benda atau angka tanpa manusia yang menanggung akibatnya.
6. Sudut pandangnya sudah jadi standar di semua channel lain ("dari sudut pandang
   korban", "dari sudut pandang pelaku").
7. Tidak bisa dibuat hook tanpa kata sifat (`mengerikan`, `misterius`, `aneh`).
8. Kalau dibahas 40 detik, tidak ada satu pun hal yang penonton bisa cek sendiri.

Empat dari delapan = tolak.

## 4 · Uji POV (empat langkah, lima menit)

1. **Kalimat POV.** Tulis: *"Ini bukan cerita tentang X, tapi tentang Y."*
   X = peristiwa, Y = apa yang sebenarnya dipertaruhkan.
2. **Uji "sudah tahu".** Kalau Y bisa ditebak dari judul, POV-nya belum ada.
3. **Uji lihat.** Apa satu hal yang penonton akan **melihat** dan belum pernah
   dilihat di channel lain? (benda, ruang, dokumen, angka)
4. **Uji 35 detik.** Bisakah Y dijawab **sebagian** dalam 35–45 detik, dan sisanya
   jadi pertanyaan? Kalau butuh 3 menit untuk menjelaskan Y, topik belum siap.

Contoh nyata:

| topik | POV lemah (menghasilkan boring) | POV yang dipakai |
|---|---|---|
| Kelimutu | "danau tiga warna yang katanya berubah sendiri" | belum ada POV → **ditahan** |
| Porong | "bencana lumpur Lapindo" | "perusahaan bilang gempa; ahli bilang sumurnya — dua kalimat, satu kesimpulan" |
| Radium | "kasus Radium Girls" | "dokter perusahaan punya diagnosis; perusahaannya sudah punya alat ukurnya sendiri" |
| Setiabudi 13 | "misteri jasad tanpa identitas" | "sidik jari masih utuh, wajah masih ada, dan tetap nol nama" |

## 5 · Audit 21 naskah (15 Nov 2026)

Tier: `misteri` (satu kejanggalan), `kontroversi` (dua pihak + dokumen),
`peristiwa` (kronologi bencana), `umum` (fakta alam/budaya — butuh POV mahir).
Skor = `check_info_design.py` (A–G).

| ep | topik | tier | putusan | skor |
|---|---|---|---|---|
| EP01 | Tiga penjaga dan satu set pakaian yang tertinggal | misteri | arsip | 4/7 (D,E,F) |
| EP02 | Mereka memotong tenda itu dari dalam | misteri | arsip | 3/7 (D,E,F,G) |
| EP03 | Kapal yang masih bisa berlayar, awak yang meninggalkannya | misteri | arsip | 5/7 (D,F) |
| EP04 | Mereka berjalan menjauh dari pertolongan | misteri | arsip | 3/7 (D,E,F,G) |
| EP05 | Mereka menulis satu kata, bukan sebuah peringatan | misteri | arsip | 2/7 (A,D,E,F,G) |
| EP06 | Api di bawah kota yang tidak pernah dipadamkan | peristiwa | arsip | 6/7 (F) |
| EP07 | Jejak kaki itu hanya satu arah | misteri | arsip | 5/7 (E,F) |
| EP08 | Semua label di pakaiannya dipotong | misteri | arsip | 5/7 (E,F) |
| EP09 | Tas di punggungnya berisi batu | misteri | pakai | 5/7 (E,F) |
| EP10 | Dua kardus di trotoar Sudirman | misteri | pakai | 4/7 (E,F,G) |
| EP11 | Tanah di Porong mengeluarkan lumpur | kontroversi | **pakai** | **7/7** |
| EP12 | Tiga danau di satu puncak | umum | **ganti** | 5/7 (A,F) |
| EP13 | Di desa ini mayat tidak dikubur | umum | tunda | 4/7 (A,E,F) |
| EP14 | Seratus tahun orang melihatnya | umum | **ganti** | 5/7 (A,F) |
| EP15 | Tanah di Petobo berubah jadi lumpur | peristiwa | pakai | 5/7 (E,F) |
| EP16 | Lukisan tertua di dunia | umum | **ganti** | 7/7 (—) |
| EP17 | Tidak meletus sejak 1600 | peristiwa | pakai | 6/7 (A) |
| EP18 | Setelah gempa, pulau baru muncul | umum | **ganti** | 6/7 (F) |
| EP19 | Salju abadi tinggal dua persen | umum | **ganti** | 5/7 (A,E) |
| EP20 | Yang menyelamatkan bukan sirene | peristiwa | tunda | 7/7 (—) |
| EP21 | Mereka diajari menjilat kuas | kontroversi | pakai | 5/7 (E,F) |

Diagnosis, dalam bahasa keputusan:

- **EP01–EP08 adalah daftar topik paling padat di YouTube** (Flannan, Dyatlov, Mary
  Celeste, Yuba, Roanoke, Isdal Woman). Semuanya misteri kelas dunia — kejanggalannya
  kuat, tetapi `kelangkaan` hampir nol. Kanalku jadi yang kesekian, dan itu tidak bisa
  ditambal dengan bahasa.
- **EP09–EP11 adalah tiga episode terbaik yang kita punya**, karena misteri Indonesia
  yang belum padat + dokumen yang bisa dibaca.
- **EP12, EP14, EP16, EP18, EP19 adalah `umum`**: menarik sebagai fakta, tetapi
  bergantung sepenuhnya pada POV — dan POV kita belum di level itu. Ini yang harus
  diganti, bukan diperbaiki bahasanya.
- **EP13 dan EP20** ditahan: materinya ada, tetapi dua-duanya mudah jatuh jadi
  "kearifan lokal" yang sudah dibahas ratusan kali.

## 6 · Rencana: 6 slot yang diganti

Slot EP12, EP14, EP16, EP18, EP19 (+EP13/EP20 ditahan) diisi dari kartu topik
`11_CONTENT/01_IDEA/topik_kandidat.json`. Yang sudah lolos gerbang:

| id | topik | tier | skor | status |
|---|---|---|---|---|
| T01 | MV Joyita — 25 orang meninggalkan kapal yang masih terapung (1955) | misteri | 23/24 | **boleh dipakai** |
| T03 | Boeing 727 hilang di Luanda (2003) | misteri | 20/24 | **boleh dipakai** |
| T02 | Valentich — enam menit rekaman terakhir (1978) | misteri | 20/24 | perlu verifikasi |
| T04 | KM Sinar Bangun — izin yang tidak pernah ada (2018) | kontroversi | 20/24 | perlu verifikasi |
| T05 | Marsinah — satu nama yang tidak masuk putusan (1993) | kontroversi | 18/24 | perlu verifikasi + keputusan pemilik |

Dan satu contoh yang sengaja ditolak, supaya jelas bedanya: **Ourang Medan**
(9/24) — semua orang pernah dengar, tidak ada satu arsip pun. Itulah bentuk
"misteri yang membosankan".

Catatan: T05 menyentuh perkara yang masih hidup secara politik. Kalau dipakai,
naskahnya hanya boleh memakai isi putusan dan mengatribusikan setiap klaim —
tidak ada nama baru yang disebut sebagai pelaku.

## 7 · Tangga kualitas (satu keterampilan per episode)

Delapan tingkat. Setiap episode **wajib** punya dua field di `content_data.py`:
`fokus` (keterampilan yang dinaikkan) dan `perbaikan` (kelemahan episode
sebelumnya yang ditutup).

| tingkat | keterampilan | lulus kalau |
|---|---|---|
| L1 | kronologi | beat ke-3 memuat tanggal + tempat + satu detail fisik (cek A) |
| L2 | bukti terukur | ≥3 beat berisi angka, dan setiap angka muncul di layar (cek F) |
| L3 | dua klaim | `turn` memuat klaim resmi + lawan klaim + sintesa (cek E) |
| L4 | POV langka | kalimat POV ada, dan tidak bisa ditebak dari judul |
| L5 | dokumen di layar | minimal satu kutipan primer tampil saat klaim diucapkan |
| L6 | kontroversi berimbang | dua pihak dapat porsi setara; tidak ada tuduhan tanpa putusan |
| L7 | subjek manusia | ada manusia yang menanggung akibat, tanpa eksploitasi |
| L8 | topik umum dengan POV tajam | tier `umum` baru dibuka setelah **8 episode berturut** lulus semua gerbang |

Tangga yang berjalan sekarang (dari `_LADDER` di `content_data.py`):

| ep | fokus | perbaikan dari episode sebelumnya |
|---|---|---|
| EP09 | L7 subjek manusia | EP08 topik luar negeri, kedekatan nol |
| EP10 | L4 POV: identitas sebagai objek | EP09 bukti terukur lemah |
| EP11 | L3 dua klaim bertarung | EP10 tanpa lawan klaim |
| EP12 | L2 angka punya label di layar | EP11 belum semua angka tampil |
| EP13 | L5 dokumen di layar | EP12 tanpa dokumen |
| EP14 | L5 lanjutan, tanpa mengarang bukti | EP13 klaim tidak berimbang |
| EP15 | L6 kontroversi berimbang | EP14 bukti visual lemah |
| EP16 | L4 POV: siapa yang menghitung | EP15 kronologi terlalu padat |
| EP17 | L6 warga vs zona merah | EP16 taruhan manusia tipis |
| EP18 | L2 bukti terukur (peta/citra) | EP17 angka tanpa pasangan visual |
| EP19 | L5 dokumen ilmiah | EP18 sumber masih berita |
| EP20 | L7 manusia | EP19 tanpa manusia |
| EP21 | L3 dua klaim | EP20 klaim tunggal |

Bila sebuah episode tidak menutup kelemahan sebelumnya, episode itu **tidak
dibangun** — diperbaiki dulu naskahnya, baru dirender. Ini yang membuat kualitas
naik tanpa harus menunggu 20 episode.

## 8 · Cara kerja harian

```bash
# 1. tambah kandidat ke 11_CONTENT/01_IDEA/topik_kandidat.json (12 indikator 0-2)
python3 tools/score_topic.py --all
python3 tools/score_topic.py --strict     # gerbang: gagal = jangan tulis naskah

# 2. setelah kandidat lolos: baca dokumen primer, isi field `sumber` di content_data.py
#    (sampai di sini, `dokumen_primer` hanya janji; sesudah dibaca, ia jadi fakta)

# 3. tulis naskah dengan tingkat L yang sedang dilatih, isi `fokus` + `perbaikan`
python3 tools/check_info_design.py EPxx -v
python3 tools/check_story.py EPxx
```

Aturan penutup: **satu episode satu keterampilan.** Kalau sebuah episode mencoba
menaikkan dua tingkat sekaligus, yang terjadi biasanya tidak ada yang naik.
