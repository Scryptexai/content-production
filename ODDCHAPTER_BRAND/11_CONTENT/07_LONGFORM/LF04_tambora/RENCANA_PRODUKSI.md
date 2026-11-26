# LF04 · rencana produksi — Tambora 1815

**Status:** produksi dan QC final selesai. Master 1920×1080/30 fps lulus dengan tepat
20.231 frame; master tercatat di Drive untuk satu unggahan YouTube baru **unlisted**
yang diotorisasi pemilik. Tidak ada rilis publik atau penjadwalan.

**Kanvas panjang yang dipakai:** 1920×1080, 30 fps. Semua visual frame berasal dari
Remotion / `@remotion/renderer`; FFmpeg dipakai pasca-render hanya untuk duplikasi
frame exact 6→30 fps, satu clone frame terminal hasil pembulatan, koreksi rentang JPEG,
audio/container, dan QC.

## Kontrak editorial

1. Cerita mengikuti rantai bukti, bukan daftar superlatif letusan.
2. Judul “Tahun Tanpa Musim Panas” dibatasi pada konteks anomali 1816 di Eropa dan
   Amerika Utara; globe tidak boleh diberi satu warna seolah seluruh dunia mengalami
   cuaca identik.
3. Bukti arkeologi Doro Bente divisualkan sebagai lapisan, artefak, dan ruang
   ketidakpastian. Tidak ada kota lengkap, keluarga, atau menit terakhir yang direka.
4. Tidak ada angka korban jiwa tunggal di layar/narasi tanpa sumber primer yang
   memadai; angka itu tidak diperlukan untuk hook maupun turn.
5. Tidak ada footage korban/bencana. Semua visual inti dapat berupa desain informasi
   original, peta skematis, arsip berlisensi, dan diagram atmosfer.
6. Setiap angka/klaim yang tampak harus kembali ke `SOURCES.md`.

## Plate / scene yang diperlukan setelah persetujuan

| Babak | Scene Remotion | Gerak utama | Label sumber |
|---|---|---|---|
| 1 | `FiveLayers` | tiga lapisan laut lama lalu lima lapisan piroklastik 1815 tersusun | `BRIN 2024` |
| 2 | `DelayedNews` | halaman koran dan log kapal bergerak lewat peta ke Batavia dengan tanggal Mei 1815 | `BADAN GEOLOGI 2020` |
| 3 | `CalderaEvidence` | potongan kaldera, endapan, dan jalur aliran ke laut; tanpa simulasi korban | `GVP · TAMBORA` |
| 4 | `DoroBente` | grid ekskavasi, fragmen artefak, lalu garis batas “bukti ≠ rekonstruksi” | `BRIN 2024` |
| 5 | `AerosolChain` | SO2 naik → aerosol sulfat → radiasi pendek berkurang; globe menandai wilayah kajian | `SCHURER ET AL. 2019` |
| 6 | `Attribution` | panel dengan/ tanpa forcing; sirkulasi tetap sebagai lapisan ketiga | `SCHURER ET AL. 2019` |
| 7 | `EvidenceChain` | tanah → arsip → atmosfer → model kembali menjadi lima lapisan penutup | `MULTI-SUMBER` |

## Aset yang boleh dipertimbangkan kemudian

| Kelas | Putusan awal | Syarat |
|---|---|---|
| Peta garis Sumbawa/Eropa, kaldera, stratigrafi, diagram aerosol | Buat original | Bentuk/skala harus ditinjau terhadap sumber; bukan peta navigasi presisi. |
| Foto kaldera GVP/NASA | Opsional | Lisensi, kredit, crop, dan label sumber diperiksa sebelum dipakai. Tidak mengambil gambar hanya dari hasil pencarian. |
| Halaman Java Government Gazette atau Bo’ Sangaji Kai | Opsional | Sumber scan primer, hak pakai, halaman, dan transliterasi diverifikasi per aset. |
| Foto artefak / situs Doro Bente | Tidak dibutuhkan baseline | Harus mendapat izin/lisensi eksplisit; tidak memakai foto untuk mengisi cerita personal. |
| Footage letusan, korban, atau AI photorealistic disaster scene | Tidak dipakai | Risiko konteks keliru dan eksploitasi lebih besar daripada nilai informasinya. |
| Musik/SFX | Belum dipilih | Tidak mengalahkan narasi; lisensi dan loudness harus diaudit. |

## Gerbang produksi

- [x] Naskah panjang melewati pemeriksaan mekanis format dan sumber awal.
- [x] Rencana mengunci visual data-led dan batas etik sebelum pencarian aset.
- [x] Pemilik menyetujui naskah panjang final sebelum VO, aset, scene, atau render.
- [x] Setiap aset visual/audio memiliki provenance; baseline memakai diagram SVG
      original tanpa foto/footage/rekonstruksi korban.
- [x] Persetujuan render/master terpisah diterima sebelum bundling atau
      `@remotion/renderer`; QC final media lulus.
- [x] Persetujuan distribusi terpisah diterima untuk Drive dan satu unggahan YouTube
      **unlisted** baru.
- [ ] Jangan menjadwalkan atau merilis publik tanpa persetujuan baru.
