# Batch 04 — pemeriksaan VO review pertama

**Tanggal ukur:** 6 November 2026
**Status:** `REVIEW ONLY · BUKAN MASTER VO · TIDAK BOLEH MASUK PRODUKSI / QUEUE`

Dokumen ini merekam hasil pengukuran lima MP3 review yang dihasilkan dari draf
skrip dengan suara narasi Indonesia pilihan review (`voice-10`). Ini **bukan**
persetujuan rekaman final, timing caption, render, atau publikasi. File audio
berada di `work/batch-04/vo_review/` dan tetap merupakan bahan kerja yang tidak
di-commit.

## Metode

- Pemeriksaan dilakukan dengan executable `ffprobe` yang dipin oleh proyek
  Remotion: `10_FILM/remotion/node_modules/@ffprobe-installer/linux-x64/ffprobe`.
- Durasi adalah `format.duration`; jumlah kata mengikuti angka perkiraan yang
  tercantum di masing-masing draf skrip, bukan transkrip otomatis.
- Semua berkas yang diperiksa terbaca sebagai MP3, 24 kHz, mono. Itu adalah
  karakteristik file review, **bukan** spesifikasi master akhir.

## Hasil dan rekonsiliasi draf

| Skrip | Kata VO draf | Rentang yang tertulis di skrip | Durasi MP3 review | Laju efektif | Selisih terhadap batas atas | Keputusan review |
|---|---:|---:|---:|---:|---:|---|
| B04-S02 Cottingley Fairies | 115 | 46–55 dtk | 55,296 dtk | 124,8 kpm | +0,296 dtk | Nyaris sesuai; cek ulang satu kali setelah pembacaan/edit final. |
| B04-S06 Clever Hans | 101 | 40–48 dtk | 49,536 dtk | 122,3 kpm | +1,536 dtk | Melewati target; ringkas atau setujui target baru hanya setelah review skrip. |
| B04-S07 Piltdown Man | 95 | 38–46 dtk | 52,248 dtk | 109,1 kpm | +6,248 dtk | Tidak sesuai target; naskah/pacing wajib direkonsiliasi sebelum VO final. |
| B04-S15 Hitler Diaries | 105 | 44–52 dtk | 52,464 dtk | 120,1 kpm | +0,464 dtk | Nyaris sesuai; cek ulang satu kali setelah pembacaan/edit final. |
| B04-S16 Sokal Affair | 109 | 42–50 dtk | 55,944 dtk | 116,9 kpm | +5,944 dtk | Tidak sesuai target; naskah/pacing wajib direkonsiliasi sebelum VO final. |

KPM = kata per menit, dihitung dari kata draf ÷ durasi file. Perbedaan antar
naskah menunjukkan bahwa hitungan kata saja tidak cukup untuk mengunci runtime:
pause, tanda baca, nama, dan pengucapan ikut memengaruhi hasil suara.

## Jejak berkas review yang diukur

| Berkas | Ukuran | SHA-256 |
|---|---:|---|
| `B04-S02_cottingley-fairies_review.mp3` | 221.421 byte | `093831b4eadb827567209cdfa0e33b5215513bbc93359ec3059a340ac135507f` |
| `B04-S06_clever-hans_review.mp3` | 198.381 byte | `2259d0f71a6ebb1b86424b680f708a6b1429868ba2de94131c1601e263f78387` |
| `B04-S07_piltdown-man_review.mp3` | 209.229 byte | `a32d6b281e323a3a2c2da2f25ef03dfa37c24213df0a721a80c3d6929e220890` |
| `B04-S15_hitler-diaries_review.mp3` | 210.093 byte | `7b3277948c7264da1989c1fbe99ebedb5178567c4faae2e78c3c787e0ba9b42a` |
| `B04-S16_sokal-affair_review.mp3` | 224.013 byte | `d5edcf5b12c9d98a042a9f11f1ce47df6f4c5567581f25ed6617069b15e6a25a` |

## Yang masih harus diselesaikan sebelum produksi

1. Reviewer menyetujui atau merevisi masing-masing naskah terhadap ledger klaim
dan sumber yang tertaut; untuk B04-S07 dan B04-S16, target runtime harus
secara eksplisit diputuskan, bukan diasumsikan dari hitungan kata.
2. Setelah naskah terkunci, buat/ukur VO **final** dan lakukan timing caption
berdasarkan file final itu. MP3 review di atas tidak boleh dipakai sebagai
master timing.
3. Verifikasi hak setiap aset dan buat manifest visual per episode. Tidak ada
aset arsip, gambar AI, musik, atau footage yang dinilai/diizinkan oleh dokumen
ini.
4. Baru setelah tiga langkah tersebut, pertimbangkan komposisi/render Remotion,
QC teknis, master Drive, dan persetujuan upload terpisah.

Sampai semua pagar tersebut selesai, seluruh slot Batch 04 tetap
`DO_NOT_QUEUE`; dokumen ini tidak mengubah `BATCH_04_SCHEDULE_DRAFT.json`.
