# LF03 · rencana produksi — Sinar Bangun 4

**Status:** pra-produksi editorial. Naskah panjang harus disetujui pemilik dan
short harus diturunkan darinya sebelum rekam/render.

**Tesis:** Angin memukul kapal, tetapi daftar keselamatan sudah gagal sebelum
keberangkatan: kapasitas 45, verifikasi 188, dan nama korban yang baru dikumpulkan
setelah kapal tenggelam.

**Kanvas panjang:** 1920×1080, 30 fps. **Turunan Short:** 1080×1920, 30 fps,
35–45 detik. Semua frame visual wajib dirender oleh Remotion / `@remotion/renderer`.

## Kontrak visual dan etika

1. Tidak ada rekonstruksi yang disajikan sebagai rekaman 18 Juni 2018.
2. Tidak ada wajah korban, jenazah, keluarga berduka, atau foto anak sebagai alat hook.
3. Visual utama adalah desain informasi: garis rute, deck kapal terukur, kartu angka,
   pembagian ruang, timeline 16.50 → 17.10, dan peta kedalaman 450 meter.
4. Jika memakai still atau potongan halaman laporan KNKT, tampilkan sebagai
   `DOKUMEN KNKT · 2018`, bukan sebagai visual kejadian.
5. Jika memakai footage generatif/rekonstruksi laut atau kapal, labelkan
   `REKONSTRUKSI VISUAL` dan jangan pakai sebagai bukti bahwa detailnya terjadi tepat
   seperti itu.
6. Semua angka di layar harus kembali ke `SOURCES.md` dan research sheet.

## Plate / scene yang diperlukan

| Babak | Scene Remotion | Isi yang bergerak | Label sumber |
|---|---|---|---|
| 1 | `CountGap` | 45 kursi bergeser menjadi 188 titik; titik tambahan melampaui lambung kapal | `DATA KNKT · 2018` |
| 2 | `RouteAndBoarding` | peta Simanindo → Tigaras, rute 3 NM; motor dan titik penumpang masuk satu per satu | `KNKT I.1` |
| 3 | `DeckMismatch` | sertifikat satu geladak bertransisi ke siluet tiga geladak; kartu 45 vs 188 | `RINGKASAN KNKT` |
| 4 | `TwentyMinutes` | garis waktu 16.50 → 17.10, gelombang abstrak dari kiri, jalur keluar menyempit | `KNKT I.1` |
| 5 | `SearchDepth` | sonar sweep turun ke 450 meter; kartu `21 SELAMAT / 3 MENINGGAL / 164 DILAPORKAN HILANG` | `KNKT I.2` |
| 6 | `NotOneWave` | tiga lapisan: beban, geladak, akses keluar; gelombang masuk terakhir, bukan satu-satunya kartu | `KESIMPULAN KNKT` |
| 7 | `Manifest` | daftar kosong berubah menjadi tiga pertanyaan penumpang: jumlah, pelampung, jalur keluar | `REKOMENDASI KNKT` |

## Elemen motion yang wajib terasa

- **Hitungan ruang:** titik penumpang tidak muncul sebagai angka statis; mereka
  mengisi siluet kapal sampai garis stabilitas turun.
- **Dua dek yang terjebak:** diagram potongan kapal memperlihatkan perbedaan antara
  akses keluar dan orang, tanpa menampilkan manusia tenggelam.
- **Kedalaman:** kamera data turun dari permukaan ke 450 meter sambil angka berubah
  dari data penumpang menjadi pencarian. Tidak boleh berupa kartu data diam.
- **Pembalik:** gelombang tidak dihilangkan, tetapi masuk setelah tiga sistem sudah
  terlihat gagal. Ini membuat tesis dapat dilihat, bukan hanya diceramahkan.

## Gerbang sebelum rekam/render

- [ ] `python3 ODDCHAPTER_BRAND/tools/check_longform.py LF03_sinar-bangun` lulus.
- [ ] Pemilik menyetujui tesis, kalimat hook, dan batas etika naskah panjang.
- [ ] Short diturunkan kata-per-kata dari babak 1, 4, 6, dan 7; tabel pasangan baris
      disertakan di berkas Short.
- [ ] Script Short lulus `check_story.py` / `check_research.py` jika entry data
      terdaftar, atau audit setara dicatat khusus format AK.
- [ ] Satu suara kanal yang telah disetujui dipakai konsisten; tidak memakai
      voice-06 atau voice-07.
- [ ] Setiap aset visual memiliki sumber/lisensi/provenance; render mencatat
      `@remotion/renderer`.
- [ ] Tidak ada upload, antrean `requested`, jadwal, atau publikasi sebelum persetujuan
      eksplisit untuk master yang telah direview.
