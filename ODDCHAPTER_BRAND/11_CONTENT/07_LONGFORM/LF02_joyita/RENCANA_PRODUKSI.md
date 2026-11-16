# LF02 · rencana produksi — MV Joyita

**Naskah:** `SCRIPT.md` (1.232 kata · 7 babak). Gate 150 kata/menit → **8:12**;
tempo terukur LF01 135 kata/menit → **9:07**. Rencana di bawah memakai **±9 menit**
supaya tidak ada kejutan saat audio masuk.
**Kanvas:** 1920×1080, 30 fps · warna sama dengan Shorts: Ink `#17191D` /
Ivory `#F4F0E8` / Sage `#A7B0A1` / Orange `#F26A3D`.

Bedanya dengan LF01: naskah ini punya **empat angka yang wajib muncul di layar**
(10.25 · 25 orang · 970 km · 6 dari 25). Angka itu bukan hiasan — itu satu-satunya
bukti yang dipegang penonton saat cerita selesai.

## Yang belum ada di repo

1. `LongFilm.tsx` — 1920×1080, caption `bottom: 120`, margin kiri 140, stamp angka
   di kanan atas (`top: 90`), caption 44 px. Belum dibuat; baru ada `Film.tsx` 9:16.
2. `timing.json` — dibuat dengan `tools/build_long_timing.py` setelah naskah beku.
   Jalankan **setelah** narasi tiap babak punya durasi nyata (`measure_audio.py`).
3. Audio per babak (7 berkas), bukan satu berkas 9 menit — supaya satu babak bisa
   diperbaiki tanpa merender ulang semuanya.

## Daftar plate (22 gambar)

Semua `jpg`, 16:9, 2048×1152, **tanpa huruf terbaca** — teks masuk lewat Remotion.
Gaya: warna film 1955 yang sudah pudar (Ektachrome disimpan di lemari lembap),
abu-hijau laut + kuning kuningan, grain halus, tidak ada efek sinematik modern.

| plate | babak | isi | catatan |
|---|---|---|---|
| V01 | 1 | lambung kapal miring ke kiri, garis air di tengah lambung, laut tenang | frame 0 wajib memuat entitas: kapal, bukan langit |
| V02 | 1 | jam dinding kapal, jarum 10.25, logam berkarat | angka harus terbaca — satu-satunya teks yang boleh tajam |
| V03 | 1 | dek kosong, dua dudukan sekoci kosong dengan tali menjuntai | kekosongan sebagai gambar, bukan ilustrasi |
| V04 | 1 | tas dokter kulit terbuka di atas papan, perban tergulung | **tanpa darah menetes**; satu bercak kecokelatan cukup |
| V05 | 2 | dermaga Apia 1955, barang dimuat, orang di tepi | pakaian 1955, tanpa kendaraan modern |
| V06 | 2 | kapal tahun 30-an dari samping, lambung putih, dua tiang pendek | wajah kapal pesiar, bukan kapal kargo |
| V07 | 2 | ruang mesin: kopling dan poros, satu mesin terbuka | kunci babak 2: sebab keberangkatan tertunda |
| V08 | 2 | tas bedah dan instrumen di atas meja kayu, tangan bersiap | satu tangan, tanpa wajah |
| V09 | 3 | antena radio dan isolator, kabel putus dicat | detail kecil, harus terlihat jelas kenapa |
| V10 | 3 | rumah kemudi dengan tenda kanvas terpasang | kanvas, bukan logam |
| V11 | 3 | kasur digulung menutup mesin di ruang mesin | gambar "perbaikan darurat" |
| V12 | 3 | rakit Carley di dek, drum kosong ditumpuk di dekatnya | drum harus berkarat dan kosong |
| V13 | 4 | peta Pasifik dengan kotak pencarian dan satu tanda silang | garis pensil, bukan grafis digital |
| V14 | 4 | potongan pipa pendingin, korosi di sambungan | makro, satu benda saja |
| V15 | 4 | kerang kecil menempel di pelat lambung di atas garis air | kunci "kemiringan sudah lama" |
| V16 | 4 | pompa bilge tanpa saringan, bilge berair | gelap, lampu satu titik |
| V17 | 5 | dek malam, air setinggi lutut, satu lampu tangan | tanpa wajah, tanpa panik yang teatrikal |
| V18 | 5 | rakit kecil di ombak, dilihat dari jauh dan tinggi | rakit terlihat kecil sekali |
| V19 | 5 | daftar barang hilang di atas kertas bersegel, tangan menunjuk | huruf tidak terbaca |
| V20 | 6 | ruang sidang Apia: meja panjang, berkas tebal, kipas langit-langit | dingin, banyak kertas, tanpa orang menonjol |
| V21 | 6 | enam lembar surat kematian di atas meja, sembilan belas ruang kosong | komposisi angka, bukan grafik |
| V22 | 7 | lambung miring yang sama seperti V01, matahari lebih rendah | penutup: gambar yang diingat |

## Kunci gaya (supaya plate ke-10 sampai ke-22 tidak melenceng)

1. **Tidak ada wajah korban.** Semua orang dari belakang, dari jauh, atau tangan saja.
2. **Tidak ada darah.** Satu bercak pudar di perban, tidak lebih.
3. **1955, bukan 2025.** Tidak ada jaket pelampung modern, radio VHF, atau kapal fiber.
4. **Tidak ada huruf terbaca** kecuali dua: jam 10.25 dan angka 25 di plate penutup.
5. **Laut tidak dramatis.** Tidak ada ombak setinggi rumah. Yang menakutkan di cerita
   ini adalah air yang biasa, di tempat yang salah.
6. **Satu palet untuk semua plate**: abu-hijau laut, kuningan, ivory. Orange hanya
   dipakai Remotion untuk angka, tidak pernah masuk gambar.

## Urutan kerja

1. ~~Naskah + SOURCES~~ — selesai; `check_longform.py LF02_joyita` **LULUS** (8.2 menit, 42 baris klaim).
2. **Narasi babak 1–2 lebih dulu**, VO pemilik (bukan TTS), dengarkan tanpa gambar.
   Kalau dua menit pertama tidak menahan, naskahnya yang salah — bukan gambarnya.
3. `timing.json` → `LongFilm.tsx` → render uji 60 detik (babak 1 saja) untuk cek
   tipografi 16:9 pada layar ponsel.
4. Plate 22 gambar, urut babak; jangan menunggu semua selesai untuk mulai menaruh
   V01–V04 di timeline.
5. Render penuh → QC: durasi ≥ 8 menit, loudnorm `I=-14, TP=-1.5, LRA=11`, frame 0
   memuat kapal, tidak ada babak yang bisa dilewati tanpa kehilangan arti.
6. **Setelah LF02 lulus, baru** potong short EP12 dari klimaksnya (babak 4–5), bukan
   sebaliknya.

## Yang harus diputuskan manusia sebelum render

- **Judul akhir.** Naskah memakai "KAPAL YANG TIDAK BISA TENGGELAM". Kandidat kedua:
  "DUA PULUH LIMA ORANG, ENAM SURAT KEMATIAN". Pilih sebelum thumbnail, karena
  thumbnail dan judul harus menyebut benda yang sama.
- **Apakah angka 10.25 dipakai di thumbnail.** Jam berhenti adalah detail paling
  spesifik yang dimiliki cerita ini, dan satu-satunya yang bisa dipakai tanpa wajah.
- **Apakah empat dokumen primer di `SOURCES.md` dikejar dulu.** Kalau ya, episode
  naik dari "terverifikasi sebagian" ke "lengkap"; kalau tidak, naskah tetap boleh
  tayang dengan angka yang sudah dikunci di tabel.
