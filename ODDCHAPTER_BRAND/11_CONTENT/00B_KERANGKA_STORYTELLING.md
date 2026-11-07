# 00B — KERANGKA STORYTELLING (menggantikan §2–§4 di `00_STRATEGI.md`)

Dokumen ini ada karena versi pertama script saya disusun dari perasaan, bukan dari
ilmu. Struktur "Hook–Retain–Reward" memang berguna untuk menahan penonton, tetapi
itu **struktur retensi, bukan struktur cerita**. Yang membuat orang bertahan sampai
detik ke-50 bukan hook-nya — melainkan satu orang yang menginginkan sesuatu.

Kerangka di bawah ini diambil dari praktik narrative nonfiction, bukan dari blog
tips. Rujukannya disebut di akhir.

---

## 1. MODEL DASAR — Jon Franklin

Jon Franklin (dua Pulitzer, *Writing for Story*) merumuskan cerita bukan sebagai
rangkaian fakta, tetapi sebagai:

> "a sequence of actions that occur when a sympathetic character encounters a
> complicating situation that he confronts and solves."

Lima bagiannya:

| # | bagian | isi | di video 60 detik |
|---|---|---|---|
| 1 | **Komplikasi** | satu masalah yang menimpa satu orang | 0–3 s (hook) + 3–12 s (setup) |
| 2 | **Perkembangan 1 — gagal** | dia mencoba, dan gagal | 12–20 s |
| 3 | **Perkembangan 2 — bingung** | dia punya semua kepingan, tidak tahu artinya | 20–32 s |
| 4 | **Perkembangan 3 — wawasan** | sesuatu berubah makna | 32–47 s (turn) |
| 5 | **Resolusi** | perubahan pada orang atau situasinya | 47–60 s |

Franklin menolak menulis sebelum kelima bagian itu bisa dinyatakan dalam **lima
baris tiga kata**. Contoh untuk EP01:

```
Lampu padam.        (komplikasi)
Tiga pria turun.    (gagal)
Jejak hilang.       (bingung)
Catatan dipalsukan. (wawasan)
Laut menyimpan.     (resolusi)
```

Kalau lima baris itu tidak bisa ditulis, ceritanya belum ada — dan tidak ada
jumlah hook yang bisa menutupi itu.

---

## 2. TIGA HAL YANG WAJIB ADA DI SETIAP EPISODE

### a. Satu protagonis, satu keinginan

Bukan "kasus", bukan "peristiwa". Satu orang yang menginginkan sesuatu yang
konkret. Di `tools/content_data.py` ini field `protagonis` dan `mau`.

Tanpa keinginan, penonton tidak punya alasan menunggu hasilnya — dan tanpa itu,
semua trik retensi hanya menunda kebosanan.

### b. Satu tanaman (planted detail)

Detail kecil yang ditanam di 10 detik pertama, lalu **berubah makna** di turn.
Bukan detail baru di akhir — turn yang menambah fakta adalah plot twist murahan.
Turn yang mengubah makna detail lama adalah cerita.

Contoh yang dipakai:

| episode | tanaman | berubah jadi |
|---|---|---|
| EP01 | satu set pakaian tahan air tertinggal | bukti bahwa satu orang keluar tanpa persiapan — bukan badai yang menyapu semua |
| EP04 | pintu mobil tidak dikunci, tangki penuh | mereka tidak terjebak; mereka memilih menjauh dari pertolongan |
| EP07 | jejak kaki hanya satu arah | pembunuh bukan datang malam itu; dia sudah di dalam rumah |
| EP12 | kota menyarankan mereka terus menari | obatnya adalah penyakitnya |
| EP19 | pohon rebah menjauhi satu titik | tidak ada kawah, karena bendanya tidak pernah menyentuh tanah |

### c. Satu resolusi yang mengubah sesuatu

Franklin: resolusi adalah "any change in the character or situation". Kalau di
akhir tidak ada yang berubah — tidak pada tokohnya, tidak pada pemahaman
penonton — itu bukan cerita, itu informasi.

---

## 3. PETUNJUK TEKNIS YANG DIPAKAI

- **Scene, bukan ringkasan.** Setiap beat adalah satu tempat dan satu waktu.
  "Desember 1900, sebuah kapal lewat" adalah scene. "Selama bertahun-tahun
  banyak teori muncul" adalah ringkasan — dan ringkasan membunuh tegangan.
- **Kata kerja, bukan kata sifat.** Franklin: "verbs are everything". Kalimat
  kita dibatasi 14 kata dan harus punya subjek yang melakukan sesuatu.
- **Spesifik, bukan dramatis.** "Empat puluh tujuh tahun" lebih kuat daripada
  "sudah lama sekali". "1.701 tong" lebih kuat daripada "banyak muatan".
  Kekhususan adalah cara penonton percaya.
- **Show, don't tell — tapi telling sesekali boleh.** Satu paragraf orientasi
  ("ini tahun 1959, di Ural") memang perlu. Yang dilarang: telling yang
  menggantikan adegan.
- **Truth, not reality.** Franklin: pembaca tidak mau realitas, mereka mau
  kebenaran. Urutan fakta yang akurat tapi tanpa makna tetap terasa bohong.
- **Satu turn per episode.** Dua turn = tidak ada turn.
- **Echo di akhir.** Kalimat terakhir memanggil kembali detail dari hook, supaya
  penonton merasa lingkaran tertutup — dan ingin memutar ulang.

---

## 4. PEMETAAN KE 60 DETIK

Dua sumber produksi singkat sepakat pada pembagian yang hampir sama: satu hook
pendek, satu setup, satu tegangan panjang, satu turn, satu konsekuensi.

| bagian | porsi | detik (60 s) | isi di script kita |
|---|---|---|---|
| hook | 5 % | 0–3 | satu detail tanaman, diucapkan seperti fakta |
| setup | 15 % | 3–12 | siapa, di mana, ingin apa |
| tension | 35 % | 12–32 | tiga sampai empat percobaan/bukti, semuanya gagal |
| turn | 15 % | 32–47 | detail lama berubah makna |
| consequence | 20 % | 47–60 | apa yang berubah, dan echo ke hook |

Aturan tambahan yang dipakai: **satu open loop**, dibuka sebelum detik ke-12 dan
ditutup setelah detik ke-45. Tidak lebih.

---

## 5. KESALAHAN YANG SUDAH SAYA BUAT (dan tidak diulang)

1. **Menulis dampak, bukan adegan.** Versi pertama EP02 dimulai dengan "sembilan
   orang hilang" — informasi. Versi sekarang dimulai dengan kain tenda yang
   disobek dari dalam — gambar.
2. **Turn yang menambah fakta.** EP01 versi pertama memakai "ternyata cuacanya
   tenang" — itu fakta baru, dan ternyata salah. Versi sekarang memakai detail
   yang sudah ada di hook (pakaian yang tertinggal) dan membalik artinya.
3. **Tanpa protagonis.** "Sebuah kota", "sebuah sinyal", "sebuah ledakan" bukan
   protagonis. Setiap episode sekarang punya satu orang.
4. **Hook yang menjanjikan hal yang tidak dibayar.** Semua hook sekarang berasal
   dari tanaman yang benar-benar dibayar di turn.

---

## 6. RUJUKAN

- Jon Franklin, *Writing for Story: Craft Secrets of Dramatic Nonfiction* —
  model komplikasi/perkembangan/resolusi; lima baris tiga kata.
  Ringkasan praktik: https://www.chipswritinglessons.com/2019/12/25/writing-for-story-a-look-back-at-jon-franklins-masterpiece/
- Wawancara Jon Franklin, Nieman Storyboard —
  https://niemanstoryboard.org/2004/11/18/an-interview-with-jon-franklin/
- Analisis "Mrs. Kelly's Monster" (Writer's Digest) — scene-based writing,
  sensory detail, "truth not reality":
  https://www.writersdigest.com/write-better-fiction/using-literary-techniques-in-narrative-journalism-a-study-of-jon-franklins-mrs-kellys-monster
- Struktur 60 detik (hook 5 % / setup 15 % / tension 35 % / turn 15 % /
  payoff 20 %, satu open loop): https://www.usevyra.com/how-to/structure-a-storytelling-video
- Struktur lima beat untuk drama vertikal 60 detik, termasuk syarat bahwa turn
  harus mengubah makna informasi sebelumnya:
  https://dramapilot.com/blog/structure-a-60-second-ai-short-drama
- Kekhususan sebagai alat empati, dan bukaan dengan micro-conflict:
  https://digitals.live/emotional-storytelling-what-sundance-s-emotional-premiere-te
- Thumbnail tanpa wajah harus membawa informasi naratif ("apa yang aneh di sini?")
  dalam di bawah satu detik: https://www.gofaceless.ai/en/blog/crafting-engagement-with-narrated-story-forms
