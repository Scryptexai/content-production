# Buku VO — SB-EP02 (MH370)

## Yang sudah masuk Drive

| berkas | id Drive | ukuran | teknis | diunggah |
|---|---|---|---|---|
| `VO EP02.mp3` | `1yzfE90efvYUJYMEu6iHof_do7aM8ZlLp` | 7.555.666 B | MP3 · 471,17 dtk (7:51) · mono 44,1 kHz · 128 kbps | 2026-11-18 04:45 UTC |

Disalin ke `google_drive/VO EP02.mp3` (folder ter-gitignore; sumbernya Drive).
Folder Drive: **SB-EP02_MH370_VO** `1EYxZupigSz0HbGtmiHOARQnZgSY0Ris7`.

**Satu berkas utuh**, bukan sembilan. Teks sumber: `SB-EP02_VO_FULL.txt`
(1.177 kata, 7.715 karakter). Rata-rata baca **150 kata/menit** — sesuai perkiraan
naskah (episode 9–11 menit setelah kartu dan jeda).

## Yang perlu diketahui sebelum memotong

Diukur di −32 dB, ambang 0,30 dtk: **121 jeda**. Yang ≥ 0,60 dtk hanya **dua**:

| rentang | panjang | posisi di naskah |
|---|---|---|
| 45,49–46,54 dtk | 1,04 dtk | akhir SEG 02 ("…sistem yang sama") |
| 106,99–107,62 dtk | 0,64 dtk | akhir SEG 03 ("…dua lewat dua puluh lima") |

Sisanya 0,30–0,50 dtk, hampir seragam. Jadi **jeda saja tidak cukup** untuk menemukan
sembilan batas segmen. Kalau dipotong pakai proporsi jumlah kata/karakter, dua batas
awal cocok (46,0 dan 107,3 dtk), tetapi batas berikutnya meleset sampai ±8 dtk karena
laju baca tiap segmen tidak seragam (126–177 kata/menit).

Kesimpulan: **jangan potong dengan silencedetect + proporsi.** Pada segmen 4 ke atas
hasilnya memotong di tengah kalimat, dan Shorts ikut rusak.

## Sudah dipotong (18 Nov 2026)

Opsi 2 dikerjakan: `faster-whisper` di Actions (run 44260878650, success) memberi timestamp
per kata, lalu batas tiap segmen digeser ke tengah jeda terdekat. Hasil: `VO_01.wav` …
`VO_09.wav`, 48 kHz mono, total 471,17 dtk. Tabel batas + id Drive: `VO_BOUNDARIES.md`.

## Tiga cara memotong (arsip keputusan)

| cara | hasil | catatan |
|---|---|---|
| **A. generate per segmen** | 9 berkas bersih `VO_01`…`VO_09` | paling akurat; teksnya sudah ada di `VO_01.txt`…`VO_09.txt`, tinggal 9 kali generate |
| **B. alignment ASR di Actions** | 9 berkas dipotong dari satu MP3 | CI punya internet: `faster-whisper` memberi timestamp per kata; batas diambil di kata terakhir tiap segmen, hasilnya artifact |
| **C. potong manual** | 9 berkas | 46,0 dtk dan 107,3 dtk sudah pasti; sisanya perlu didengar |

Kalau tidak ada yang dipilih, render masih bisa jalan dengan satu berkas VO, tetapi
kartu angka dan 5 Short harus diselaraskan manual di Remotion — lebih rawan daripada
memotong VO sekali di awal.

## Catatan produksi

- Audio mono 44,1 kHz; master video 48 kHz. Resample saat mix, bukan saat potong.
- Target campuran SB-EP01: −14,1 LUFS, TP −1,3; musik −14 dB + ducking rasio 5.
- Nama berkas hasil potong **wajib** `VO_01`…`VO_09` — nama itu yang mengunci batas
  potong Shorts.
