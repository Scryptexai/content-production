# 17 · Nilai konten, bukan durasi (16 Nov 2026)

Dokumen ini lahir dari satu kalimat pemilik kanal:

> "kalau cuma durasi yg dipersingkat tapi struktur bahasa nya tidak, 5 detik pun
> akan tetap sama hasilnya"

Artinya: keluhan "kalimatnya kurang menarik" **bukan** masalah durasi, tempo, atau
jumlah kata. Memotong 60 detik menjadi 45 tidak menambah satu pun alasan untuk
menonton. Yang kurang adalah **isi**: klaim yang punya lawan, bukti yang bisa
ditunjuk, dan satu orang yang menyelidiki.

Aturan turunannya mengikat semua episode setelah EP12.

---

## 1 · Apa yang disebut nilai konten

Nilai konten = jumlah hal yang penonton **dapat** dan tidak bisa ia dapat dari
judul berita. Empat hal, dan keempatnya harus ada:

| # | isi | kalau tidak ada |
|---|---|---|
| 1 | **Tesis** — satu kalimat yang menyalahkan bacaan umum | penonton merasa sudah tahu, lalu berhenti |
| 2 | **Rantai bukti** — tiga benda/angka yang menopang tesis | cerita jadi suasana, bukan argumen |
| 3 | **Lawan** — pihak yang mengatakan sebaliknya, dikutip | tesis jadi opini narator |
| 4 | **Konsekuensi** — apa yang masih berlanjut sampai sekarang | video selesai tanpa meninggalkan apa pun |

Naskah yang punya empat hal ini **tidak bisa** dideskripsikan sebagai "kurang
menarik", sependek apa pun durasinya. Naskah yang tidak punya empat hal ini tidak
akan tertolong oleh durasi apa pun.

## 2 · Tujuh uji sebelum menulis satu kata pun

1. **Uji satu kalimat.** Bisa tidak tesisnya diucapkan dalam satu kalimat tanpa
   kata "misteri"? Kalau tidak, topiknya belum dipahami — bukan naskahnya yang salah.
2. **Uji lawan.** Siapa yang membantah? Kalau tidak ada, ini bukan investigasi,
   ini dongeng.
3. **Uji benda.** Apa benda yang bisa difoto di tengah cerita? Minimal tiga.
4. **Uji angka.** Apa angka yang bisa ditunjuk di layar? Minimal tiga, dan semua
   harus ada di `SOURCES.md`.
5. **Uji "lalu kenapa".** Setiap paragraf harus menjawab "lalu kenapa?" Kalau
   jawabannya "supaya lengkap", paragraf itu dibuang.
6. **Uji baca ulang.** Baca dengan suara keras. Kalau ada satu kalimat yang tidak
   bisa diucapkan dalam satu tarikan napas, kalimat itu belum selesai.
7. **Uji hapus.** Hapus satu paragraf. Kalau ceritanya tetap utuh, paragraf itu
   tidak punya nilai konten.

## 3 · Yang memperbaiki "kalimat kurang menarik" (dan yang tidak)

**Memperbaiki:**

- **Ganti kata kerja jadi peristiwa.** "Kapal itu mengalami kerusakan" →
  "Kopling mesin kiri gagal, dan mereka tetap berlayar."
- **Satu kalimat, satu ide.** Kalimat kedua yang menempel hanya menambah kata.
- **Angka menggantikan kata sifat.** "sangat jauh" → "970 kilometer".
- **Benda menggantikan perasaan.** "mereka panik" → "kasur diturunkan menutup mesin".
- **Pertanyaan yang tidak dijawab** di akhir setiap babak.
- **Kutipan pihak lain**, bukan ringkasan narator.
- **Kata ganti yang jelas.** POV "kita" untuk investigasi; "aku" hanya kalau
  memang kanal yang menyelidiki sendiri.

**Tidak memperbaiki (jangan diulang):**

- memotong durasi;
- menambah musik dramatis;
- menambah efek transisi;
- memecah kalimat jadi potongan 3 kata supaya "cepat";
- mengganti narator;
- menaikkan tempo bicara.

Semua itu mengubah **penyajian**, bukan **isi**. Penonton yang berhenti karena isi
tidak akan kembali karena tempo.

## 4 · Urutan produksi yang mengikat

```
topik (gerbang 16) → dokumen primer dibaca → NASKAH PANJANG (8–12 menit)
   → gate check_longform.py LULUS → tunjukkan ke pemilik
   → baru short: potong klimaksnya → gate check_story + check_info_design
   → render → Drive
```

**Short tidak pernah ditulis lebih dulu.** Kalau naskah panjang belum ada, short
tidak diproduksi. Alasannya bukan durasi, tetapi karena short hanya bekerja sebagai
*pintu*: ia menjanjikan ruang yang benar-benar ada di versi panjang. Short tanpa
induk adalah janji kosong — penonton yang ingin mengulik tidak punya tempat pergi.

### Apa yang dipotong ke short

| bagian naskah panjang | masuk short? |
|---|---|
| kalimat pembuka babak 1 | ya, sebagai hook |
| pertanyaan babak 1 | ya, sebagai `tanya` |
| babak 2–3 (orang, latar, hal yang tidak cocok) | **tidak**, kecuali satu fakta yang jadi `setup` |
| babak 4–5 (temuan, dugaan, tesis) | **inti short** — turn diambil dari sini |
| babak 6 (konsekuensi) | ya, satu kalimat |
| babak 7 (pertanyaan penutup) | ya, kata per kata, sebagai `loop` |

Setiap baris short harus punya **baris pasangan** di naskah panjang, dicatat di
bagian "potongan dari naskah panjang" pada berkas short. Baris tanpa pasangan
ditulis ulang, bukan dipertahankan.

## 5 · Papan skor (dipakai saat meninjau, bukan saat menulis)

| # | pertanyaan | 0 | 1 | 2 |
|---|---|---|---|---|
| 1 | tesis satu kalimat, menyalahkan bacaan umum | tidak ada | samar | jelas |
| 2 | lawan dikutip langsung | tidak ada | disebut | dikutip |
| 3 | benda konkret | <3 | 3 | ≥5 |
| 4 | angka tertunjuk & ada di SOURCES | <3 | 3 | ≥5 |
| 5 | konsekuensi masih berjalan | tidak | disebut | dijelaskan sebabnya |
| 6 | pertanyaan yang dibiarkan terbuka | tidak | ada | ada, dan tidak dijawab sampai akhir |
| 7 | short punya pasangan baris di naskah panjang | tidak | sebagian | semua |

**≥11 dari 14** = layak produksi. Di bawah itu, yang diperbaiki naskahnya —
bukan durasinya.

## 6 · Bukti bahwa aturan ini jalan (EP12 / LF02)

- Naskah panjang LF02: 1.232 kata, 7 babak, `check_longform.py` **LULUS**.
- Short EP12: 101 kata, 43 dtk, `check_story.py` **LULUS**, `check_info_design.py`
  **7/7** — dan setiap barisnya punya baris pasangan di LF02 (lihat §6 pada berkas
  short).
- Turn short berubah dari "air masuk lewat pipa bocor" (temuan) menjadi "mereka
  tidak salah membaca air; mereka salah membaca kapal" (tesis). Jumlah kata turun
  3, nilai kontennya yang naik — persis arah yang diminta pemilik.
