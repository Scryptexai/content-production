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

## Status plate (22 dari 22 — semua 1920×1080)

Semua plate di bawah sudah di-upscale ke **1920×1080** dengan
`tools/upscale_plates.py` (Lanczos + grain 5,5% + unsharp halus). Asli 1376×768
disimpan di `plates_src/` (tidak masuk Git).

| plate | berkas | isi | QC |
|---|---|---|---|
| V01 | `V01_steamboat_night.jpg` | kapal uap malam, asap, jendela menyala | ✅ entitas di frame pertama |
| V02 | `V02_deck_crowd.jpg` | dek penuh, tanpa senjata, sebagian bertelanjang kaki | ✅ versi 2 (versi 1 ditolak) |
| V03 | `V03_wharf_line.jpg` | barisan naik ke kapal di dermaga Vicksburg | ✅ tanpa senjata, ada perwira berdaftar |
| V04 | `V04_side_on_photo.jpg` | kapal dari tepi sungai, dua dek penuh orang | ✅ paling mendekati foto Helena 1865 |
| V05 | `V05_hold_barrels.jpg` | palka: tong gula, lentera, lorong sempit | ✅ tanpa orang |
| V06 | `V06_boiler_patch.jpg` | tambalan dipaku di sambungan ketel | ✅ gambar "sebab" |
| V07 | `V07_the_warning.jpg` | tukang ketel menunjuk, kapten bersedekap | ✅ adegan peringatan, tanpa dialog |
| V08 | `V08_river_map.jpg` | peta sungai tangan, kompas kuningan | ✅ tanpa huruf terbaca |
| V09 | `V09_memphis_dock_night.jpg` | dermaga Memphis malam, tong diturunkan | ✅ |
| V10 | `V10_flooded_river.jpg` | sungai banjir dari atas, satu kapal kecil | ✅ litografi tint, bukan foto (1865 tak ada drone) |
| V11 | `V11_listing_deck.jpg` | dek miring, orang berpegangan, asap dari celah | ✅ |
| V12 | `V12_steam_burst.jpg` | uap putih + pecahan kayu, api kecil | ✅ bukan bola api |
| V13 | `V13_hand_on_wreckage.jpg` | tangan memegang papan hangus | ✅ tanpa wajah |
| V14 | `V14_rescue_boat.jpg` | lentera menyisir air, orang ditarik | ✅ |
| V15 | `V15_shore_row.jpg` | barisan berselimut di tepi sungai, dua pria bertopi di tangan | ✅ tanpa wajah, tanpa luka |
| V16 | `V16_newspaper.jpg` | tumpukan koran 1865, tangan menekan | ✅ kolom tak terbaca |
| V19 | `V19_soybean_field.jpg` | galian di ladang kedelai, kayu hangus | ✅ gambar kunci turn |
| V22 | `V22_field_aerial.jpg` | aerial baris kedelai saat matahari rendah | ✅ penutup, kosong |

| V17 | `V17_courtroom.jpg` | ruang sidang militer: tiga perwira, berkas, peta | ✅ kertas tak terbaca |
| V18 | `V18_empty_river.jpg` | sungai kosong setelah bencana, tanpa perahu | ✅ kekosongan sebagai efek |
| V20 | `V20_charred_timber.jpg` | kayu hangus dengan paku besi, tangan menyentuh | ✅ tekstur arang, bukan arang generik |
| V21 | `V21_two_maps.jpg` | dua peta ditumpuk, alur sungai bercabang | ✅ vellum transparan, tanpa huruf |

**Semua plate selesai.** Langkah berikutnya: `timing.json` dari
`tools/build_long_timing.py` (sudah jalan: 8 babak, 578,8 s, 17.364 frame), lalu
komposisi Remotion 16:9 dan narasi per babak.

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

1. ~~Plate V01–V02 dulu~~ — selesai; keduanya dipakai.
2. ~~Sisa plate~~ — selesai, 22/22.
3. **Narasi babak 0–2 lebih dulu**, dengarkan tanpa gambar. Kalau tidak menahan
   sampai menit 3, naskahnya yang salah, bukan gambarnya — dan itu lebih murah
   diperbaiki sebelum render.
4. Komposisi `LongFilm.tsx` 16:9 + `timing.json`, lalu render, lalu QC:
   - durasi ≥ 8 menit, tidak ada babak yang bisa dilewati tanpa kehilangan arti
   - suara: loudnorm `I=-14, TP=-1.5, LRA=11`
   - frame 0 wajib memuat entitas (kapal), bukan langit

## Yang harus diputuskan manusia sebelum render

- **Judul akhir.** Tiga kandidat ada di `SCRIPT.md` §6; pilih satu sebelum thumbnail
  digambar, karena thumbnail dan judul harus menyebut benda yang sama.
- **Apakah angka 1.167 dipakai di thumbnail.** Angka itu yang paling bisa
  dipertanggungjawabkan (Salecker 2022), tetapi bukan angka terbesar.
