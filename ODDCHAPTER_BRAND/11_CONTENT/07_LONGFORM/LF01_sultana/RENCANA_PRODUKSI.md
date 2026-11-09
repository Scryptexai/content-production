# LF01 · rencana produksi

**Naskah:** `SCRIPT.md` (1.449 kata ≈ 9:40 pada 150 kata/menit)
**Kanvas:** 1920×1080, 30 fps · **Kode warna:** Ink `#17191D` / Ivory `#F4F0E8` /
Sage `#A7B0A1` / Orange `#F26A3D` (sama dengan Shorts, supaya satu kanal terasa satu).

## Yang belum ada di repo

Remotion sekarang hanya punya komposisi 1080×1920 (`Film.tsx`). Format panjang butuh:

1. `LongFilm.tsx` — 1920×1080, subtitle di `bottom: 120`, margin kiri 140, stamp
   tanggal di kanan atas (`top: 90`), ukuran caption 44 px.
2. `build_long_timing.py` — menghitung durasi per babak dari naskah (kata ÷ 2,5 kata
   per detik + jeda 0,4 s per ganti babak).
3. Audio: satu trek narasi per babak (bukan satu berkas 10 menit) supaya bisa
   diperbaiki per babak tanpa merender ulang semuanya.

## Daftar plate (22 gambar)

Semua `jpg`, 16:9, 2048×1152, tanpa teks di dalam gambar — teks masuk lewat Remotion.
Gaya: arsip abad ke-19 yang diferensial, grain halus, warna tanah.

| plate | isi | catatan |
|---|---|---|
| V01 | kapal uap kayu roda samping di sungai lebar, malam, asap dua cerobong | pembuka; entitas = kapal |
| V02 | geladak penuh pria berdesakan, tidak terlihat lantai | jarak dekat, wajah menghadap kamera |
| V03 | barisan pria kurus di dermaga, seragam lusuh | harus terlihat kurus, bukan rapi |
| V04 | kapal geladak penuh dilihat dari samping, hitam-putih | meniru foto Helena 1865 |
| V05 | palka: tong kayu, lampu minyak, ruang sempit | untuk 100 ton gula |
| V06 | tangan memasang tambalan logam di ketel, paku keling | detail kerja, bukan ilustrasi |
| V07 | dua pria di dekat ketel, satu menunjuk | wajah setengah terang |
| V08 | peta sungai Vicksburg–St. Louis, garis tangan | boleh peta bergaya 1865 |
| V09 | dermaga Memphis malam, gula diturunkan, lampu minyak | kabut tipis |
| V10 | sungai lebar dari ketinggian, arus berputar | drone/udara, 1865 tidak ada drone — pakai gaya lukisan cat air |
| V11 | geladak miring, orang berpegangan, asap dari celah | kemiringan harus terasa |
| V12 | uap putih menyembur dari sisi kapal, pecahan kayu | **bukan** bola api |
| V13 | tangan memegang puing di air gelap | satu tangan, bukan banyak |
| V14 | kapal kecil dengan lampu sorot menyisir sungai | penyelamatan |
| V15 | barisan tubuh di tepi sungai, ditutupi kain | tanpa wajah, tanpa darah |
| V16 | halaman surat kabar 1865, judul Lincoln, kolom kecil | judul harus terbaca “LINCOLN” |
| V17 | ruang sidang militer: meja, kertas, seragam | dingin, banyak kertas |
| V18 | sungai luas tanpa kapal | kekosongan setelah bencana |
| V19 | ladang kedelai datar, satu pria berdiri memandang tanah | kunci turn |
| V20 | potongan kayu hangus di atas tanah, tangan menyentuh | tekstur arang harus jelas |
| V21 | dua peta alur sungai ditumpuk (1865 vs sekarang) | overlay, bukan dua gambar terpisah |
| V22 | ladang kedelai dari udara, matahari rendah, satu jalur tanah | penutup, gambar yang diingat |

## Status plate (batch 1 — 8 dari 22)

| plate | berkas | status | catatan QC |
|---|---|---|---|
| V01 | `plates/V01_steamboat_night.jpg` | ✅ dipakai | entitas jelas di frame pertama; asap, kabut, jendela menyala |
| V02 | `plates/V02_deck_crowd.jpg` | ✅ dipakai (versi 2) | versi 1 **ditolak**: tahanan memegang senapan dan dek bertali-temali — tahanan yang dibebaskan tidak bersenjata |
| V06 | `plates/V06_boiler_patch.jpg` | ✅ dipakai | tambalan tipis + paku keling baru terbaca; ini gambar "sebab" |
| V12 | `plates/V12_steam_burst.jpg` | ✅ dipakai | uap putih, bukan bola api — sesuai fakta ketel |
| V13 | `plates/V13_hand_on_wreckage.jpg` | ✅ dipakai | tanpa wajah, jadi tidak melampaui arsip |
| V16 | `plates/V16_newspaper.jpg` | ✅ dipakai | kolom koran sengaja tidak terbaca (model menghasilkan huruf palsu) |
| V19 | `plates/V19_soybean_field.jpg` | ✅ dipakai | gambar kunci turn: kayu hangus di bawah permukaan ladang |
| V22 | `plates/V22_field_aerial.jpg` | ✅ dipakai | penutup; kosong, tanpa manusia |

Belum dibuat: V03, V04, V05, V07, V08, V09, V10, V11, V14, V15, V17, V18, V20, V21.

### Kunci gaya (supaya plate ke-9 sampai ke-22 tidak melenceng)

1. **Tahanan tidak pernah membawa senjata.** Mereka paroled, kurus, sebagian bertelanjang kaki.
2. **Dek steamboat bukan kapal layar**: tidak ada tiang, tali-temali, atau roda kemudi besar.
3. **Ledakan = uap putih + pecahan kayu**, bukan bola api oranye. Api menyusul, kecil.
4. **Tidak ada huruf yang terbaca** di koran, papan, atau label. Kalau perlu teks, masuk lewat Remotion.
5. **Warna**: sepia/abu dingin untuk 1865; hijau-tanah alami untuk 1982. Dua zaman, dua palet —
   itu yang membuat turn terasa pindah waktu, bukan pindah filter.
6. **Resolusi**: model mengembalikan 1376×768. Semua plate di-upscale ke 1920×1080
   (lanczos) lalu diberi grain halus; tanpa grain, upscale terlihat lunak. Detail
   tidak bertambah — karena itu tidak ada plate yang boleh bergantung pada detail kecil.

## Urutan kerja

1. Plate V01–V02 dulu (dua ini menentukan apakah episode ini layak dilanjutkan:
   kalau kapal dan geladak tidak meyakinkan, seluruh 10 menit jatuh).
2. Narasi babak 0–2 → dengarkan tanpa gambar. Kalau tidak menahan sampai menit 3,
   naskahnya yang salah, bukan gambarnya.
3. Sisa plate, lalu render 16:9, lalu QC:
   - durasi ≥ 8 menit, tidak ada babak yang bisa dilewati tanpa kehilangan arti
   - suara: loudnorm `I=-14, TP=-1.5, LRA=11`
   - frame 0 wajib memuat entitas (kapal), bukan langit

## Yang harus diputuskan manusia sebelum render

- **Judul akhir.** Tiga kandidat ada di `SCRIPT.md` §6; pilih satu sebelum thumbnail
  digambar, karena thumbnail dan judul harus menyebut benda yang sama.
- **Apakah angka 1.167 dipakai di thumbnail.** Angka itu yang paling bisa
  dipertanggungjawabkan (Salecker 2022), tetapi bukan angka terbesar.
