# 00G — KEBIJAKAN VISUAL: PAHAMI SECTION, CARI YANG COCOK, CAMPUR SUMBER

Koreksi pemilik, 22 Nov 2026:

> "masalah footage yg sama digunakan beberapa video — harus cari footage lain;
> banyak juga footage yang tidak sesuai narasinya; pahami setiap section-nya
> lalu cari di Coverr; jika tidak ada generate foto saja, tapi jangan sampai
> semuanya foto — cari juga visual source document."

Dokumen ini mengunci cara memilih visual untuk setiap episode (AK, OS, dan
berikutnya). Mengganti aturan lama yang memakai ulang klip bank antar episode.

## 1 · Urutan kerja per section (wajib)

1. **Pahami section VO dulu.** Baca narasi section (hook/CTA/fakta/…): apa yang
   benar-benar disebut — benda, tempat, tindakan, suasana. Catat kata kunci
   visualnya. Jangan memilih klip sebelum section dipahami.
2. **Cari footage Coverr yang cocok** (bukan yang paling mudah ada):
   - tulis spec `tools/footage_specs/OS-EPxx-discover.json` (kueri per section),
     set `tools/footage_specs/ACTIVE`, push, lalu `gh workflow run fetch-footage.yml`
   - baca `footage-candidates-*.json` (judul kandidat), pilih manual →
     `tools/footage_picks/OS-EPxx.json` → jalankan fetch-footage lagi (mode picks)
   - klip diunduh ke `footage/<slug>/` — **6 s,1920x1080, tanpa audio**
3. **Kalau Coverr tidak punya** → **generate foto AI** (`generate_image`,
   still tanpa orang, palet episode). Ini cadangan, bukan pilihan pertama.
4. **Jangan semua foto** — setiap episode wajib memuat **visual source
   document**: dokumen/foto arsip yang nyata (peta, koran, halaman jurnal,
   cetakan, foto bersejarah) dari sumber bebas lisensi (Wikimedia Commons,
   arsip publik/PD). Kredit sumber + lisensi di deskripsi/kartu akhir.
5. **Larangan reuse lintas episode**: klip/still yang sudah tayang di episode
   lain **tidak dipakai lagi** di episode baru (kecuali pemilik minta eksplisit).
   Tiap episode punya set visualnya sendiri — cek dengan membandingkan
   `work/<slug>/case_cfg.py` CLIPS terhadap episode sebelumnya.
6. **Kesesuaian > ketersediaan**: kalau section tidak dapat visual yang jujur
   cocok, lebih baik foto AI spesifik daripada klip yang maksa (klip yang tidak
   sesuai narasi merusak kepercayaan penonton).

## 1b · Peta lokasi kejadian — WAJIB Remotion, bukan kartu statis

(Koreksi pemilik,22 Nov2026 — berlaku untuk semua episode berikutnya.)

Peta tempat kejadian **jangan** ditampilkan sebagai kartu diam. Bangun shot
peta dengan **Remotion** dari **peta asli** (Wikimedia/OSM berlisensi — bukan
peta karangan AI):

- komposisi `MAP-ZOOM` di `ODDCHAPTER_BRAND/10_FILM/remotion` → render lewat
  `scripts/render-mapzoom.mjs`;
- choreography: **zoom-in** dari luas wilayah → tepat ke titik kejadian,
  dengan **animasi zona** (lingkaran highlight berdenyut) dan **titik
  kejadian** (pin + label nama tempat);
- **sinkronisasi wajib**: shot mulai tepat saat narasi mulai menyebut
  lokasi, dan zona/titik muncul tepat saat nama tempat diucapkan — "saat
  narasi masuk ke tempat kejadian, visual harus menyunting tepat ke
  tempatnya";
- untuk fakta jarak (mis. sumber air ±3 km), animasi **dua titik + garis
  jarak berlabel**;
- kredit sumber peta tetap wajib (label per shot + kartu akhir).

## 2 · Perimbangan sumber (target per episode)

| sumber | peran | catatan |
|---|---|---|
| Footage Coverr (baru) | gerak utama, suasana, aksi | wajib label `FOOTAGE STOK · COVERR` |
| Dokumen arsip (source document) | bukti, tempat, waktu, otoritas | kredit sumber+lisensi; scan/kutipan boleh di-zoom |
| Foto AI | adegan yang tidak mungkin difoto (bola cahaya, momen1963, dll.) | tanpa orang; bukan pengganti bukti |

Rasio fleksibel, tetapi **tidak boleh dua kategori hilang** — minimal ada
footage bergerak, minimal satu source document, foto AI hanya untuk yang tak
tersedia di dua lainnya.

## 3 · Gerbang QC visual

Sebelum render, cek per shot: (a) apakah visualnya benar-benar menggambarkan
section VO-nya? (b) apakah klip ini sudah dipakai di episode lain? (c) apakah
episode punya minimal satu source document? Gagal salah satu → ganti, jangan
lanjut render.
