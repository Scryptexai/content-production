# Audit editorial — LF03 · Sinar Bangun 4

**Status:** `NASKAH PANJANG DISETUJUI — Short turunan sudah diaudit; menunggu
persetujuan terpisah untuk Short sebelum rekaman, aset, atau render.`

**Tanggal audit:** 6 November 2026

## Putusan audit

Naskah boleh masuk **review editorial pemilik**, bukan produksi. Ia mempertahankan
satu pertanyaan: *bagaimana jumlah penumpang baru dapat dihitung sesudah kapal
tenggelam?* Kalimat tandatangannya adalah: **“188 bukan angka kapal. Ia angka
posko.”**

Tesis tidak lagi memakai klaim “izin yang tidak pernah ada” sebagai hook. Klaim
izin/SPB berasal dari pelaporan/penyidikan yang butuh konteks hukum; naskah ini
tidak membutuhkannya untuk menjelaskan persoalan keselamatan yang sudah terbaca
dari kronologi, verifikasi korban, dan rekomendasi KNKT.

## Pemeriksaan fakta per babak

| Babak | Klaim / fungsi | Pasangan sumber | Putusan |
|---|---|---|---|
| 1 | Verifikasi pada pukul 15.00 hari kesembilan: 188 = 21 selamat, 3 meninggal, 164 dilaporkan hilang; jumlah hilang tidak dapat dipastikan | `SOURCES.md` #12, #13, #26, #27 | Pakai; semua label angka wajib tampil lengkap. |
| 2 | Rute, embarkasi, sekitar 150 orang lebih, sekitar 70 motor, penumpang tertinggal, cuaca, pembayaran tunai, kekhawatiran penumpang | #2–#7, #19, #30 | Pakai; tidak membuat klaim bahwa ketiadaan bukti bayar sendiri membuktikan ketiadaan manifest. |
| 3 | 45 adalah kapasitas dalam dokumen yang diringkas rilis KNKT; 188 hasil posko; satu vs tiga geladak | #17–#18 | Pakai hanya dengan atribusi “ringkasan hasil KNKT”. Tidak menyebut 188 sebagai angka manifest. |
| 4 | Kronologi 16.50 → 17.10, gelombang, akses keluar, jaket, dan tiga kapal penolong | #8–#11 | Pakai; tanpa visual orang tenggelam, tanpa wajah atau rekonstruksi korban. |
| 5 | 16 hari pencarian, 450 meter, ROV, keluarga, penghentian operasi | #14–#16, #27, #31 | Pakai; `164` selalu berbunyi “dilaporkan hilang”. |
| 6 | Temuan stabilitas/akses/peralatan dan rekomendasi | #21–#23, #28–#29 | Pakai sebagai ringkasan beratribusi. Laporan keselamatan tidak dijadikan putusan pidana. |
| 7 | Pertanyaan penutup soal kemampuan daftar penumpang menjawab jumlah sebelum kapal bergerak | Sintesis dari #12–#13, #18, #23, #27 | Pakai sebagai pertanyaan editorial, bukan tuduhan bahwa seorang tertentu gagal membuat daftar. |

## Klasifikasi sumber dan batasnya

- **Primer langsung:** laporan final KNKT `KNKT.18.06.21.03`, bagian pengantar,
  sinopsis, kronologi, dan SAR yang tersedia pada pembaca PDF resmi. Ini mendukung
  tulang punggung kronologi dan angka naskah.
- **Ringkasan beratribusi:** rilis hasil KNKT yang dibaca melalui ANTARA Sumut serta
  salinan rekomendasi INSA. Ini dipakai untuk detail 45 vs 188, perbedaan geladak,
  analisis stabilitas, dan butir rekomendasi. Semua kalimat naskah yang bergantung
  pada kelompok ini menyebut `ringkasan hasil KNKT` atau `KNKT meminta`.
- **Tidak dipakai:** sangkaan kepolisian tentang SPB/manifes, kapasitas awal 43,
  identitas korban, putusan pidana, dan klaim apakah rekomendasi kemudian sudah
  diterapkan. Tidak ada yang boleh masuk ke Short tanpa penelitian baru.

## Etika dan visual

- Tidak menyebut individu sebagai pelaku atau mengubah laporan keselamatan menjadi
  kesimpulan hukum.
- Tidak menyamakan `164 dilaporkan hilang` dengan jumlah kematian pasti.
- Tidak memakai kisah keluarga, foto korban, wajah, atau jenazah sebagai alat retensi.
- Plate yang direncanakan adalah desain informasi Remotion: peta rute, kapal
  potongan, timeline, penghitung posko, sonar abstrak, dan kartu rekomendasi.
- Apabila halaman/foto laporan dipakai, tiap aset harus diberi sumber halaman.
  Animasi atau simulasi laut wajib diberi label `REKONSTRUKSI VISUAL`, bukan
  arsip kejadian.

## Gerbang yang sudah dijalankan

| Gerbang | Hasil |
|---|---|
| `python3 ODDCHAPTER_BRAND/tools/score_topic.py --all` | T04 20/24, tier `kontroversi`, `dipakai` |
| Fact table berlabel | Ada di `02_SCRIPT/riset/AK-EP12_sinar-bangun_fakta.md` |
| Sumber → klaim | 32 baris di `SOURCES.md` menurut pemeriksa (termasuk baris header tabel) |
| `python3 ODDCHAPTER_BRAND/tools/check_longform.py LF03_sinar-bangun` | **LULUS** — 1.424 kata, sekitar 9,5 menit, 7 babak, 32 baris klaim |
| Review visual/etik internal | Lulus bersyarat: hanya desain data/dokumen berlisensi |
| `git diff --check` | Lulus pada saat audit |

## Gerbang yang belum boleh dilompati

- [x] Pemilik menyetujui judul, hook, tesis, dan batas etika naskah panjang pada
      6 November 2026.
- [x] Short diturunkan dari naskah ini, dengan pasangan baris asal di
      `02_SCRIPT/AK-EP12_sinar-bangun.md`.
- [x] Metadata episode dan tiga gerbang Short diregistrasikan; audit ada di
      `02_SCRIPT/AK-EP12_sinar-bangun_AUDIT.md`.
- [ ] Persetujuan terpisah atas naskah Short, aset, suara kanal, serta master Remotion.
- [ ] Render, Drive, antrean unggah, atau penerbitan.

**Keputusan berikutnya:** minta persetujuan pemilik untuk Short yang diturunkan.
Sampai persetujuan itu ada, pekerjaan berhenti di dokumen; tidak ada VO, tidak ada
render, dan tidak ada tindakan upload.
