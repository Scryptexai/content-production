# EP01 — ILLUMINATI: ORGANISASI ATAU INTERPRETASI?

**Seri baru ODDCHAPTER · long-form 05:18 · 1080×1920 · 30 fps**
Bahan datang dari pemilik (Drive `SERIES BARU — ODDCHAPTER / EP01 — ILLUMINATI PERNAH ADA`):
VO, timestamp/transkrip, musik latar, satu efek suara, dan rekomendasi visual.

| berkas | isi |
|---|---|
| `EP01_ILLUMINATI_VO.mp3` | 05:18,01 · mono 44,1 kHz · −25,2 LUFS (dinormalisasi ke −16 saat mix) |
| `Timestamp-full.txt` | transkrip TurboScribe + batas waktu 17 blok → dipakai sebagai **kontrak** potongan gambar |
| `EP01 — TIMESTAMP & VISUAL RECOMMENDATION` | label bab, catatan visual, larangan ("jangan tampilkan simbol modern sebagai bukti langsung") |
| `EP01_ILLUMINATI_MUSIC_BACKGROUND.mp3` | 05:18,02 · stereo · −13,9 LUFS (di-ducking −18 dB di bawah VO) |
| `EP01_ILLUMINATI_SOUND_EFFECT.mp3` | 1,04 s · dipasang di 4 penanda (0:00 · 1:58 · 4:10 · 5:13) |

## Kenapa timestamp pemilik yang memotong gambar

Short-form memakai `build_timing.py` (durasi tiap baris diukur dari mp3 per
segmen). Long-form tidak bisa begitu: narasinya satu berkas 5 menit. Karena itu
`tools/build_longform.py` membaca batas waktu pemilik dan menolak naskah yang
timpang — kalau ada celah > 0,3 detik antara dua blok, build gagal, karena itu
artinya ada bagian narasi yang berjalan tanpa gambar.

## Struktur (17 blok)

| waktu | bab | plate |
|---|---|---|
| 0:00–0:23 | BUKTI ATAU TAFSIR? | meja arsip, dokumen + segel lilin |
| 0:23–0:52 | MITOS MODERN | kolase mitos (mata, piramida) — sebagai persepsi, bukan bukti |
| 0:52–1:07 | 1776 — BAVARIA | **arsip:** potret Adam Weishaupt; etsa Ingolstadt (Hollar, 1638) |
| 1:07–1:26 | ORGANISASI NYATA | buku aturan; **arsip:** Nachtrag, halaman struktur derajat |
| 1:26–1:44 | REPRESI | meja kerja; segel lilin + lemari arsip ditutup |
| 1:44–1:58 | 1785 — DINYATAKAN ILEGAL | edik; halaman arsip yang hilang |
| 1:58–2:27 | 1797 — TEORI MENYEBAR | dua jalur; **arsip:** sampul Barruel |
| 2:27–2:50 | BUKTI YANG DIPAKAI | papan benang; Nachtrag |
| 2:50–3:08 | INTERPRETASI A | papan benang; buku aturan |
| 3:08–3:22 | BACAAN SKEPTIS | halaman hilang; satu dokumen dua panah |
| 3:22–3:36 | SIMBOL DIPINJAM | kolase mitos; dua panah |
| 3:36–3:50 | GARIS BUKTI TERPUTUS | halaman hilang; dua jalur |
| 3:50–4:10 | CELAH KESINAMBUNGAN | dua jalur; edik |
| 4:10–4:28 | DUA CARA MEMBACA | dua panah; meja arsip |
| 4:28–4:48 | KELEMAHAN KEDUANYA | halaman hilang; meja kerja |
| 4:48–5:13 | PERTANYAAN | meja kerja; meja arsip |
| 5:13–5:18 | ODDCHAPTER | meja arsip |

## Visual: apa yang asli, apa yang ilustrasi

- **Arsip domain publik (4):** potret Weishaupt, etsa Ingolstadt (Wenceslaus
  Hollar 1638), sampul *Memoirs Illustrating the History of Jacobinism*
  (Barruel), halaman *Nachtrag* berisi struktur derajat ordo. Ditandai label
  `ARSIP` di layar.
- **Ilustrasi/rekonstruksi (9):** meja arsip, kolase mitos, buku aturan, meja
  kerja, segel + lemari, dua jalur, papan benang, halaman hilang, dua panah.
  Semuanya gambar situasi, **bukan** dokumen yang diklaim sebagai temuan.
- Tidak ada satu pun simbol modern yang dipakai sebagai bukti Illuminati masih
  aktif — sesuai catatan pemilik dan bunyi naskahnya sendiri.

## Audio

```
VO      loudnorm −16 LUFS  →  −2 dB
musik   −18 dB, di-ducking sidechain (threshold 0,03 · ratio 12 · release 420 ms)
sfx     +12 dB di 0:00 · 1:58 · 4:10 · 5:13
mix     alimiter 0,85 → −1 dB → −16,8 LUFS, peak −1,0 dBFS
master  loudnorm −14 LUFS · TP −1,5
```

## Kalau harus dibangun ulang

```bash
cd ODDCHAPTER_BRAND
python3 tools/build_longform.py EP01 -v        # json + mix
cd 10_FILM/remotion
node scripts/render-longform.mjs still 40 400   # cek tampilan (opsional)
node scripts/render-longform.mjs render         # 9544 frame → master
```

`public/` di-ignore Git: plate dan mp3 tidak ikut commit. VO/musik/sfx asli ada
di Drive pemilik, plate dibuat ulang dari daftar di tabel atas.

## Struktur v2 — berjeda (17 Nov 2026)

Naskah tidak berubah satu kata pun; yang berubah hanya **titik henti**. Narasi
dipotong di keheningan asli VO, lalu tiap potongan diberi pembuka sendiri.

| # | waktu | jeda | isi | yang berbunyi |
|---|---|---|---|---|
| — | 0:00–0:15,8 | — | hook: "BUKTI ATAU TAFSIR?" | VO |
| 0 | 0:15,8–0:18,8 | interstitial 3,0 dtk | ikon mata-segitiga digambar · 1776 ↔ 2026 · "?" + "SATU PERTANYAAN, DUA JAWABAN" | sfx + musik |
| 1 | 0:26,6 | kartu bab 2,6 dtk | TAFSIR MODERN · "mata satu, piramida, bank, perang" | sfx kertas + musik |
| 2 | 1:12,1 | kartu bab | **SIAPA PEMIMPIN ILLUMINATI?** · "pertanyaan yang tidak pernah selesai" | sfx kertas + musik |
| 3 | 1:52,7 | kartu bab | 1785 — DISEGEL, BUKAN DIHAPUS | sfx + musik |
| 4 | 2:38,0 | kartu bab | TEORI LAHIR | sfx + musik |
| 5 | 3:21,3 | kartu bab | BUKTI YANG SAMA | sfx + musik |
| 6 | 4:05,1 | kartu bab | CELAH 200 TAHUN | sfx + musik |
| 7 | 4:46,1 | kartu bab | LEMAH DI DUA SISI | sfx + musik |
| 8 | 5:34,4 | kartu bab | JADI, YANG MANA? | sfx + musik |

VO asli 318,12 dtk → master v2 341,95 dtk (+23,8 dtk jeda). Titik potong
divalidasi ada di keheningan (pusat keheningan terdekat, geser maks 1,4 dtk),
jadi tidak ada kata yang terbelah.
