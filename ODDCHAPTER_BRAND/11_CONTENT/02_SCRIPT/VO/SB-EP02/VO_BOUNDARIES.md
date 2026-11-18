# Batas potong VO — SB-EP02 (18 Nov 2026)

VO pemilik satu berkas (`VO EP02.mp3`, 471,17 dtk). Dipotong jadi sembilan segmen dengan
alignment ASR (`faster-whisper` model `small`, bahasa `id`) + pencocokan urutan kata naskah,
lalu **setiap batas digeser ke tengah jeda terdekat** supaya tidak ada kata yang terbelah.

| seg | mulai | akhir | durasi | kata | wpm | jeda tempat potong | jeda awal | jeda akhir | puncak |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.00 | 23.59 | 23.59 dtk | 56 | 142.4 | 23,38–23,80 (0,42 dtk) | 0,08 dtk | 0,21 dtk | −4,6 dB |
| 2 | 23.59 | 46.02 | 22.42 dtk | 63 | 168.6 | 45,49–46,54 (1,04 dtk) | 0,21 dtk | 0,52 dtk | −5,5 dB |
| 3 | 46.02 | 109.04 | 63.03 dtk | 162 | 154.2 | 108,88–109,21 (0,33 dtk) | 0,52 dtk | 0,17 dtk | −5,3 dB |
| 4 | 109.04 | 191.40 | 82.35 dtk | 199 | 145.0 | 191,16–191,64 (0,48 dtk) | 0,17 dtk | 0,24 dtk | −3,7 dB |
| 5 | 191.40 | 262.92 | 71.52 dtk | 188 | 157.7 | 262,77–263,07 (0,29 dtk) | 0,24 dtk | 0,15 dtk | −2,4 dB |
| 6 | 262.92 | 316.84 | 53.92 dtk | 124 | 138.0 | 316,59–317,09 (0,50 dtk) | 0,15 dtk | 0,25 dtk | −3,5 dB |
| 7 | 316.84 | 375.42 | 58.58 dtk | 144 | 147.5 | 375,21–375,63 (0,42 dtk) | 0,25 dtk | 0,21 dtk | −4,3 dB |
| 8 | 375.42 | 416.70 | 41.28 dtk | 104 | 151.1 | 416,55–416,86 (0,31 dtk) | 0,21 dtk | 0,15 dtk | −5,6 dB |
| 9 | 416.70 | 471.17 | 54.47 dtk | 137 | 150.9 | — | 0,16 dtk | 0,25 dtk | −5,3 dB |

Median laju 150,9 kata/menit; tidak ada segmen di luar ±30% median.
Total 471,17 dtk = durasi audio asli, tidak ada bagian yang hilang atau tertinggal.

## Verifikasi

- **Jeda awal setiap berkas 0,08–0,52 dtk, jeda akhir 0,15–0,52 dtk** — tidak ada berkas yang
  mulai atau berakhir tepat di tengah bunyi, jadi tidak ada kata terpotong.
- Puncak −2,4 sampai −5,6 dBFS — tidak ada clipping.
- Format 48 kHz mono PCM 16-bit, siap masuk mix (musik −14 dB, ducking rasio 5).

## Di Drive (folder SB-EP02_MH370_VO)

| berkas | id Drive |
|---|---|
| `VO_01.wav` | `18pwfpJtX6MMB514PUl3vffQAFn4t7ASf` |
| `VO_02.wav` | `1T46VaV9rcUEkdciVAEBUxrgwayyW_YUo` |
| `VO_03.wav` | `1fnl4nTHwZ58PpmygZ_oKi3_s1lSwOyFF` |
| `VO_04.wav` | `1Jvk3jrGGkr7AMecAphCpuk8a_-nVxJs0` |
| `VO_05.wav` | `1l1zc6in5YFpJp5dTeDZjEBjq5CeooJFj` |
| `VO_06.wav` | `1CvGIthggUWf7o25NDEwrwue9mOIIIYOZ` |
| `VO_07.wav` | `174UL0IJjjVsd76tKgtIrYSXy3naVhqxV` |
| `VO_08.wav` | `1a8upfi10LhE5FBuWrsYJ4cPhntN7Bh4T` |
| `VO_09.wav` | `1VGWS2YDXoXz3b1nJJ-xmXBthdONvi5Eo` |

## Catatan alat

- `tools/align_vo.py` — ASR + difflib + snap ke jeda. Bisa juga dipakai tanpa ASR:
  `--snap-only --cuts "24.05,45.77,..."` untuk memakai batas yang sudah diketahui.
- Penjaga `guard` (0,35 dtk): jeda yang selesai **sebelum** akhir kata terakhir tidak dipakai,
  karena itu jeda di tengah frasa terakhir, bukan di ujungnya. Tanpa penjaga ini, batas
  segmen 3 tertarik ke 107,31 — di tengah frasa "dua puluh lima".
- `.github/workflows/vo-split.yml` menjalankan hal yang sama di CI dan menulis
  `SPLIT_RESULT.md` ke repo (log Actions tidak terbaca dari sandbox).

## Timestamp per kata (`words.json`)

Run `44315522833` (percobaan 5) memakai `cuts_final` — delapan batas di tabel di atas
diberikan apa adanya, bukan hasil snap baru — lalu menulis `words.json`:

- 1.185 kata, `start`/`end` per kata dari ASR (faster-whisper `small`).
- Tiap entri punya `seg` (segmen naskah) dan `seg_t` (segmen menurut waktu nyata).
  Hanya **6 kata** yang berbeda, semuanya kata angka yang dilewati pencocokan ASR
  ("Delapan", "Dua lewat dua puluh lima") — waktunya diwarisi tetangga lalu diregangkan
  oleh `build_longform.py` sebelum dipakai caption.
- Caption master ditempel ke kata ini, bukan dibagi rata per durasi blok. Contoh: cue
  pertama master "Lo yakin pesawat MH370 hilang tanpa jejak?" 00:00,000–00:03,440.

Berkas: `words.json` (di repo), `boundaries.json`, `report.txt` — semuanya 48 kHz mono
diukur ulang dari VO penuh 471,17 dtk yang dibentuk dari sembilan WAV itu
(`work/vo/SB-EP02/SB-EP02_full.wav`, tidak di Git).
