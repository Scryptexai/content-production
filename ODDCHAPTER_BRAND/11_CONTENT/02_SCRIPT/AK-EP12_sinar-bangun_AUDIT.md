# Audit naskah Short — AK-EP12 · Sinar Bangun 4

**Status:** `PRA-PRODUKSI DISETUJUI — naskah/gate tetap LULUS; perencanaan Remotion
dan paket VO/aset dapat disiapkan. Belum ada take VO, render, master, antrean, Drive,
atau unggahan.`

**Persetujuan pemilik:** Short disetujui untuk **pra-produksi saja** setelah review
naskah, kartu angka, dan arah visual. Persetujuan ini tidak mencakup render, transfer,
queue, penjadwalan, upload, publikasi, atau perubahan episode kanonik `EP12`.

## Hubungan dengan naskah panjang

- Induk: `11_CONTENT/07_LONGFORM/LF03_sinar-bangun/SCRIPT.md`.
- Persetujuan pemilik untuk naskah panjang diterima pada 6 November 2026.
- Short tidak menambah peristiwa, tersangka, kapasitas baru, atau angka baru. Tabel
  pemotongan di `AK-EP12_sinar-bangun.md` memetakan setiap segmen ke BABAK 1, 2,
  3, 4, 6, atau 7 pada induk dan ke fakta F01, F02, F04, F05, F14, F19.

## Putusan fakta dan bahasa

| Item | Putusan |
|---|---|
| `188` | Selalu disebut sebagai angka posko/hari kesembilan, bukan manifest keberangkatan. |
| `164` | Tampil sebagai `HILANG`; tidak pernah diperlakukan sebagai angka kematian. |
| `45` | Berlabel `di dokumen` / ringkasan hasil KNKT; tidak disebut kapasitas pasti tanpa atribusi. |
| Penyebab | VO menyebut gelombang yang membalikkan kapal, lalu merebut kembali konteks lewat angka dan rekomendasi; tidak menuduh orang. |
| Izin/SPB | Tidak masuk naskah, visual, judul, atau metadata. |
| Korban | Tidak ada nama, foto, wajah, jenazah, keluarga, atau rekonstruksi manusia. |

## Gerbang yang dijalankan

| Perintah | Hasil |
|---|---|
| `python3 ODDCHAPTER_BRAND/tools/check_story.py AK-EP12` | **LULUS** — 35 detik, echo `kapal`, tanpa kegagalan. |
| `python3 ODDCHAPTER_BRAND/tools/check_research.py AK-EP12 -v` | **LULUS** — hook, seluruh beat, dan loop memiliki token fakta dari `AK-EP12_sinar-bangun_fakta.md`. |
| `python3 ODDCHAPTER_BRAND/tools/check_info_design.py AK-EP12 -v` | **LULUS 7/7** — kronologi, karantina putusan, celah, tesis–antitesis–sintesis, angka, dan suara penyelidik. |
| `python3 ODDCHAPTER_BRAND/tools/check_longform.py LF03_sinar-bangun` | **LULUS** — regresi induk tetap 1.424 kata / sekitar 9,5 menit. |
| `python3 -m py_compile ...` dan JSON gate | Lulus sebelum commit. |

## Catatan mekanis

Pemeriksa riset kini juga mengenali singkatan lembaga huruf kapital, seperti `KNKT`,
sebagai token fakta. Perubahan itu diperlukan karena Short memakai rekomendasi KNKT
dalam satu baris yang tidak membawa angka; sebelumnya tokeniser hanya mengenali nama
dengan huruf awal kapital seperti `Sinar` atau `Bangun`.

Pemeriksa Short membaca digit sebagai satu token dan menghitung rancangan ini sebagai
35 detik. Rekaman final **wajib** tetap mengukur tempo Indonesia sebenarnya, sebab
angka akan dibaca sebagai kata. Jika hasil nyata melewati 45 detik, penulis memotong
kata dari naskah; audio tidak boleh dipercepat secara buta.

## Keputusan visual pra-produksi

Rencana yang diizinkan sekarang hanya memakai scene desain informasi Remotion: meja
posko, titik data, garis rute skematis, timeline, siluet kapal generik, dan kartu
angka. Implementasi source-nya ada di
`10_FILM/remotion/src/scenes/SinarBangunPreprod.tsx`; paket cue, manifest, sumber,
dan hash font ada di `AK-EP12_sinar-bangun_PREPRODUCTION.md`.

Tidak perlu mencari stock footage untuk meloloskan gate visual. Scene tidak mengimpor
foto, video, audio, URL, atau visual generatif; ia memakai SVG/CSS/data motion lokal.
Tidak ada bundel, render still, `renderMedia`, FFmpeg, atau media master yang
dijalankan/dihasilkan ketika pra-produksi ini disiapkan.

## Gerbang berikutnya

- [x] Pemilik menyetujui Short, kartu angka, dan arah visual **sebatas
      pra-produksi**.
- [x] Cue VO, baseline frame, manifest aset, source mapping, dan batas etik dicatat
      dalam `AK-EP12_sinar-bangun_PREPRODUCTION.md`.
- [ ] Pemilik memilih satu suara internal kanal; teks rekam berangka diuji/dibaca dan
      durasi nyata setiap cue dicatat.
- [ ] Persetujuan pre-render/render-master terpisah diterima sebelum bundle/renderer,
      caption, render Remotion, atau QC teknis dijalankan.
- [ ] Review master terpisah sebelum Drive, queue, jadwal, atau unggah.
