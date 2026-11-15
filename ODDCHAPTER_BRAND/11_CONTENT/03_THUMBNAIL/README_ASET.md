# ASET THUMBNAIL — EP01–EP08 (LONG + SHORT)

Delapan episode, dua berkas per episode. Semua sudah diunggah ke Drive:
`ODDCHAPTER / thumbnail / 16x9 LONG (1280x720)` dan `9x16 SHORT (1080x1920)`.

## Cara pakai di YouTube Studio

| Keperluan | Berkas | Ukuran | Syarat YouTube |
|---|---|---|---|
| Thumbnail video panjang | `16x9/EPxx_16x9_1280x720.jpg` | 1280×720, 146–243 KB | ≤2 MB, 16:9 ✓ |
| Cover Short/Reels | `9x16/EPxx_9x16_1080x1920.jpg` | 1080×1920, 380–559 KB | 9:16 ✓ |

Langkah: Studio → **Konten** → pilih video → **Detail** → *Thumbnail* → **Unggah file** →
pilih berkas 16:9. Untuk Shorts, cover vertikal dipasang di editor Shorts (potong/cover),
bukan di kolom thumbnail biasa.

Kalau tidak ada `EP07`/`EP08` 16:9 di Drive, artinya unggahan belum lengkap — cek folder
`16x9 LONG (1280x720)`, harus berisi delapan berkas.

## Daftar berkas & headline

| Episode | Headline 16:9 | Headline 9:16 | Isi visual (tanpa wajah) |
|---|---|---|---|
| EP01 | PAKAIAN / TERTINGGAL | sama | menara api + pakaian di tiang, dua siluet membelakangi kamera |
| EP02 | DIPOTONG / DARI DALAM | sama | tenda disobek dari dalam, siluet berjalan ke salju, lantern orange |
| EP03 | KAPAL / KOSONG | sama | dek kosong, kemudi tanpa tangan, layar menganggur |
| EP04 | JALAN / KE ATAS | sama | mobil terkubur salju, jejak kaki naik bukit |
| EP05 | TANPA / MAYAT | sama | rumah dibongkar, tiang pagar berpahat, siluet berbadan tebal |
| EP06 | API TAK / PADAM | sama | aspal retak, uap, pendar orange dari bawah tanah |
| EP07 | JEJAK / SATU ARAH | sama | jejak kaki satu arah menuju kabin, tidak ada jejak balik |
| EP08 | TANPA / NAMA | sama | lereng berbatu berkabut, bara api kecil, siluet di punggung |

Headline 2–3 kata, sengaja **tidak** mengulang judul video
(judul EP01 mis. "TIGA PENJAGA DAN SATU SET PAKAIAN YANG TERTINGGAL").

## Sistem yang dipakai (tidak berubah antar episode)

- Palet: Ink `#17191D` · Ivory `#F4F0E8` · Sage `#A7B0A1` · Orange `#F26A3D` (satu area saja).
- Headline **Anton**, huruf besar semua, 2 baris, stroke Ink, rata kiri.
- Label `EP 0X` **Archivo Black** warna Sage + garis aksen orange di atas headline.
- Wordmark `ODDCHAPTER` kecil di kiri bawah.
- 16:9: subjek di kanan, teks di kiri, 15% bawah dibiarkan kosong (UI YouTube menimpa di sana).
- 9:16: teks di atas, subjek di bawah, 20% bawah dibiarkan kosong (UI Shorts).
- Scrim gradien + butir film + vignette supaya teks selalu kontras di atas latar apa pun.
- Tanpa wajah manusia — hanya siluet dari belakang.

## Berkas kerja

- `plates/` — gambar dasar tanpa teks (`EPxx_plate.png` 16:9, `EPxx_9x16.png` 9:16).
- `final/16x9/`, `final/9x16/` — hasil akhir bertulisan.
- `final/_KONTAK_SHEET.jpg` — semua 16 berkas dalam satu lembar untuk meninjau konsistensi.
- `assets/fonts/` — `Anton-Regular.ttf`, `ArchivoBlack-Regular.ttf`.
- `00_RISET_DAN_SISTEM.md` — riset, palet, grid, delapan konsep, checklist audit.

## Regenerasi

```bash
cd ODDCHAPTER_BRAND
python3 tools/thumbnail_render.py                 # pasang teks ke semua plate
python3 tools/thumbnail_contact_sheet.py          # lembar tinjau 16 berkas
python3 tools/thumbnail_render_169_from_916.py    # cadangan 16:9 dari plate 9:16
```

Ganti headline cukup di `HEADLINE` dalam `tools/thumbnail_render.py`, lalu jalankan ulang.

## Catatan jujur

`plates/EP07_plate.png` dan `plates/EP08_plate.png` (16:9) belum berhasil dibuat karena
batas 10 gambar per sesi generator. Sementara itu `16x9/EP07` dan `16x9/EP08` dipotong dari
plate 9:16 lewat `tools/thumbnail_render_169_from_916.py` — komposisinya sudah benar
(teks kiri, subjek kanan) tetapi ketajamannya di bawah enam episode lain. Ganti dengan plate
16:9 asli begitu generator bisa dipakai lagi: buat plate, jalankan
`python3 tools/thumbnail_render.py`, unggah ulang dua berkas itu.
