# Batch 04 — gerbang skrip pertama

**Tanggal pemeriksaan:** 6 November 2026
**Prinsip:** sumber → skrip → produksi → jadwal
**Ini bukan persetujuan upload.** Tidak ada baris di bawah yang dapat membuat
metadata unggah, queue Zernio, atau jadwal YouTube sebelum master dan QC lengkap.

## Kandidat yang boleh masuk draf skrip

| Slot | ID draf | Topik | Alasan lolos ke draf | Status sesudah skrip |
|---|---|---|---|---|
| B04-S02 | `B04-S02` | Cottingley Fairies | Museum pemegang objek menyajikan foto, kamera, surat Elsie 1983, dan batas sengketa foto kelima. | Draf skrip; VO review ada, durasi belum direkonsiliasi; aset belum ada. |
| B04-S06 | `B04-S06` | Clever Hans | Buku Pfungst 1907/1911 dan telaah ilmiah modern sama-sama membatasi kesimpulan pada isyarat manusia tak disengaja. | Draf skrip; VO review ada, durasi belum direkonsiliasi; aset belum ada. |
| B04-S07 | `B04-S07` | Piltdown Man | Koleksi Natural History Museum dan publikasi/rekam 1953 mengunci jalur bukti material, tanpa perlu berspekulasi pelaku. | Draf skrip; VO review ada, durasi belum direkonsiliasi; aset belum ada. |
| B04-S15 | `B04-S15` | Hitler Diaries | Bundesarchiv memegang dokumentasi pemeriksaan dan kronologi pengungkapan; skrip membahas verifikasi dokumen, bukan tokoh Nazi. | Draf skrip; VO review ada, durasi belum direkonsiliasi; aset belum ada. |
| B04-S16 | `B04-S16` | Sokal Affair | Artikel asli, pengungkapan Sokal, serta respons editor tersedia dan memungkinkan konteks dua sisi. | Draf skrip; VO review ada, durasi belum direkonsiliasi; aset belum ada. |

## Kandidat yang tetap tertahan di riset

`B04-S01`, `B04-S03`, `B04-S04`, `B04-S05`, `B04-S08`, `B04-S09`, `B04-S10`,
`B04-S11`, `B04-S12`, `B04-S13`, dan `B04-S14` **tidak** memperoleh naskah
sampai catatan pagar dalam `BATCH_04_SOURCE_REGISTER.md` ditutup. Secara khusus,
B04-S14 tetap membutuhkan status perkara resmi dan review harm-minimization;
B04-S05/B04-S09/B04-S12/B04-S13 membutuhkan review martabat subjek sebelum
format hiburan dipertimbangkan.

## Gerbang sesudah draf skrip

Draf skrip hanya dapat pindah ke produksi bila:

1. naskah dicek ulang terhadap sumber yang dirujuk di file skrip;
2. daftar aset menyebut sumber, lisensi, dan pernyataan AI bila berlaku;
3. VO final disetujui dan diukur; teks layar tidak menambah klaim;
4. render Remotion memiliki manifest, QC teknis, thumbnail, dan caption;
5. master final terverifikasi di Drive dengan hash/ukuran;
6. hanya setelah semua itu, satu request queue `approved: true` dapat dibuat
   untuk satu unggahan per push.
