# AK-EP12 — paket pra-produksi Remotion / VO / aset

**Status:** `REVIEW MASTER LOKAL LULUS — TIDAK ADA DISTRIBUSI`

Setelah persetujuan pra-produksi, pemilik memberi persetujuan **terpisah dan sempit**
untuk satu render review lokal Remotion beserta QC/provenance lokalnya. Persetujuan
itu menghasilkan satu review master lokal; ia **tidak** mengizinkan transfer Drive,
queue, jadwal, unggahan, publikasi, unlist, penghapusan, atau perubahan episode
kanonik `EP12` (MV Joyita). Tidak ada tindakan distribusi dilakukan oleh pekerjaan ini.

**Induk editorial:** `07_LONGFORM/LF03_sinar-bangun/SCRIPT.md`

**Naskah terkunci untuk pengukuran:** `AK-EP12_sinar-bangun.md` §1

**Lembar fakta:** `riset/AK-EP12_sinar-bangun_fakta.md`

**Implementasi scene:** `10_FILM/remotion/src/scenes/SinarBangunPreprod.tsx`

**Komposisi rencana:** `ODDCHAPTER-AK-EP12-SINAR-BANGUN-PREPROD`

---

## 1 · Kontrak implementasi

| Kunci | Nilai rencana | Batas |
|---|---|---|
| Kanvas | `1080 × 1920` / 9:16 | Tidak ada versi 16:9 atau pengganti EP12 kanonik. |
| Frame rate | `30 fps` | Mengikuti `theme.ts`. |
| Timing bench | `1.260` frame / **42,0 detik visual** | Take C final terukur 41,360 detik; 19 frame (0,640 detik) adalah hold visual penutup. Kontainer review terukur 42,005 detik karena padding AAC; video tetap tepat 1.260 frame / 30 fps. |
| Mesin visual | React + Remotion SVG/CSS/data motion | Seluruh frame review keluar dari `@remotion/renderer`; FFmpeg dipakai sesudah render hanya untuk normalisasi/encode audio, faststart, container, dan QC—stream video disalin tanpa perubahan dan diverifikasi hash-nya. |
| Audio pada komposisi | VO C final lokal, melalui Remotion `Audio` | Skrip review menyalin take terverifikasi ke `public/audio/ak-ep12-sinar-bangun-review.wav` sebelum bundling; audio itu hanya dipakai pada satu review master lokal. |
| Gaya potong | Hard cut dengan masuk/keluar 10–18 frame | Tidak ada dissolves, footage bencana, atau rekonstruksi yang diklaim arsip. |

`SinarBangunPreprod.tsx` memakai bentuk SVG, teks, CSS gradient, dan titik data
deterministik untuk seluruh visualnya. Satu-satunya media adalah `Audio` +
`staticFile` untuk take C final lokal yang disalin oleh skrip review; tidak ada `Img`,
`Video`, API, aset web eksternal, foto kapal, maupun footage tragedi. Karena itu
implementasi tetap dapat ditinjau sebagai desain informasi tanpa menyarukan arsip atau
rekonstruksi sebagai dokumentasi.

---

## 2 · Peta VO yang siap direkam

Teks di bawah identik secara makna dengan naskah Short yang sudah lulus gate. Tanda
waktu adalah **cue editing sementara**. Pembacaan sumber sudah diuji setelah pemilik
memilih narator feminin berbahasa Indonesia; hasilnya dicatat di §2a dan tidak
mengubah naskah terkunci tanpa keputusan editorial berikutnya.

| Cue | Slot plate pasca-ukur | Teks rekam C final yang diverifikasi | Frame / scene | Fakta |
|---|---:|---|---|---|
| V01 | 0,0–5,3 | Angka 188 muncul sembilan hari sesudah kapal tenggelam. | `0–158` · data posko | F04, F05 |
| V02 | 5,3–8,2 | Kenapa 188 muncul belakangan? | `159–245` · rute skematis | F04, F05 |
| V03 | 8,2–11,8 | Kita kira 188 dihitung di dermaga. | `246–353` · titik dermaga | F04 |
| V04 | 11,8–15,9 | 18 Juni 2018, kapal berangkat 16.50. | `354–476` · timeline | F01 |
| V05 | 15,9–20,9 | Dua puluh menit, gelombang 1,5 sampai 2 meter membalikkan kapal. | `477–626` · gelombang abstrak | F02 |
| V06 | 20,9–30,2 | Dokumen 45, posko 188: 21 selamat, 3 meninggal, 164 hilang. | `627–904` · kartu angka | F04, F14 |
| V07 | 30,2–33,7 | KNKT: 188 bukan angka dermaga. | `905–1.009` · kalimat tanda tangan | F04, F05 |
| V08 | 33,7–37,5 | KNKT meminta manifest sebelum berangkat. | `1.010–1.123` · dokumen abstrak | F19 |
| V09 | 37,5–41,36 | Hitung 188 sebelum kapal berangkat, atau cari? | `1.124–1.240` · loop angka | F04, F19 |

Slot plate mengikuti take kontigu terukur; batas antar-cue adalah rencana editorial
untuk animasi dan caption, bukan klaim word-level timestamp dari penyedia suara. Frame
`1.241–1.259` menahan pertanyaan tanpa audio selama 0,640 detik.

### Aturan pembacaan dan pengukuran

1. Rekaman memakai bahasa Indonesia natural: `188` dibaca *seratus delapan puluh
delapan*, `16.50` dibaca *enam belas lima puluh*, dan `1,5–2 meter` dibaca *satu
setengah sampai dua meter*. Tidak ada SSML/markup pada naskah rekam.
2. Gunakan satu suara internal kanal yang **dipilih/disetujui pemilik**; rencana
   produksi induk melarang `voice-06` dan `voice-07`. Pemilik telah memilih kandidat
   **feminin / id-ID** pada audisi. ID penyedia bersifat sesi dan tidak dicatat sebagai
   kredensial/pengganti persetujuan editorial.
3. Pembacaan sumber dan dua iterasi pemadatan yang melampaui 45 detik dikarantina
   (lihat §2a); take kontigu C final lulus pada 41,360 detik. Bila total melampaui
   45 detik, potong kata dengan audit editorial—jangan mempercepat audio secara buta.
4. Sebelum render, pemeriksa mengonfirmasi kata `hilang` pada V06 dan bahwa V07
   tidak mengubah `188` menjadi manifest. Tidak ada nama orang, tuduhan, SPB, atau
   angka kematian pasti di VO.

### 2a · Hasil audisi dan uji waktu — take C final siap untuk review lokal, bukan master publik

Pemilik memilih kandidat **narator feminin Indonesia** pada audisi dan menyetujui
Pemadatan B lalu C. Take final berikut digunakan hanya pada satu komposisi dan master
**review lokal** yang telah disetujui terpisah; ia bukan master publik dan tidak
dipindah ke Drive, queue, jadwal, atau unggahan.

| Uji | Materi | Hasil ukur `ffprobe` | Putusan |
|---|---|---:|---|
| A · baca naskah sumber | Sembilan cue copy awal; PCM S16LE, 24 kHz, mono | **55,080 detik** tanpa jeda tambahan | **GAGAL**. Dikarantina; tidak dipercepat atau dipakai sebagai master. |
| B · tes awal / copy tepat | Tes kata B 41,920 dtk, lalu copy B tepat kontigu dan cue terpisah | **45,800 / 49,160 detik** | **GAGAL**. Batas file dan kata yang diperlukan tidak boleh diakali dengan time-stretch. |
| C · tes pertama | Copy C sebelum token/gerbang final | **44,160 detik** | Dalam rentang, tetapi perlu pembetulan token fakta/gerbang. |
| C · token-gated | Copy C dengan `188` eksplisit di relate | **45,080 detik** | **GAGAL** 0,080 detik; dikarantina, tidak dipercepat. |
| C · **final** | Copy C final yang ada pada tabel V01–V09 | **41,360 detik** | **LULUS** target 35–45 detik. Dipakai sebagai VO untuk satu review master lokal, bukan master publik. |

Take A dipindahkan ke `work/sinar-bangun/vo_internal/rejected-original-read/` agar
tidak tertukar dengan aset final. Take kontigu yang lolos berada di
`work/sinar-bangun/vo_internal/AK-EP12_cut-C-final-contiguous.wav`:

```text
PCM S16LE · 24.000 Hz · mono · 1.985.358 byte · 41,360 detik · 1.241 frame @30 fps
SHA-256  3a4a5e99d4f2e475c3f1c9b9c931443d5ef79f63bfb7b5703e02a4fd3a4e9ff4
```

Tidak ada file audio yang dipentaskan sebagai `master`. C final mempertahankan F01,
F02, F04, F05, F14, dan F19. Untuk mengunci gate tanpa menambah klaim, `188`
dikembalikan pada relate; kata `pukul`, `kemudian`, dan `sesudahnya` dibuang dari
setup/tension/loop. `164` tetap **HILANG**; `45` tetap beratribusi pada ringkasan
hasil; dan `188` tetap angka posko, bukan manifest.

---

## 3 · Daftar scene dan jejak sumber

| Scene | Frame / detik pasca-ukur | Gerak yang diimplementasikan | Teks layar utama | Sumber / batas |
|---|---:|---|---|---|
| S01 | `0–158` / 0,0–5,3 | Grid data dan titik bergerak mengunci ke `188`; bukan gambar manusia. | `VERIFIKASI HARI KE-9 · BUKAN MANIFEST` | F04–F05 · KNKT I.2.2. |
| S02 | `159–245` / 5,3–8,2 | Garis rute skematis dan ikon perahu generik bergerak Simanindo → Tigaras. | `KAPAN ANGKA INI ADA?` | F01 · KNKT I.1. Bukan peta presisi/GIS. |
| S03 | `246–353` / 8,2–11,8 | Lingkaran data, bukan wajah/penumpang, bergerak di bidang dermaga. | `KITA KIRA 188 DIHITUNG DI DERMAGA.` | F04 · klaim persepsi editorial, bukan fakta bahwa manifest tersedia. |
| S04 | `354–476` / 11,8–15,9 | Timeline aktif dari `16.50` menuju `17.10`; rute normal `30 MENIT` muncul sebagai konteks. | `18 JUNI 2018 · DUA PULUH MENIT` | F01–F02, F11 · KNKT I.1. |
| S05 | `477–626` / 15,9–20,9 | Gelombang abstrak dari kiri memiringkan siluet kapal generik. | `1,5–2 M` dan `BUKAN ARSIP KEJADIAN` | F02 · diagram, bukan rekonstruksi/footage kejadian. |
| S06 | `627–904` / 20,9–30,2 | Kontras `45` dan `188`, lalu kartu bergerak `21 / 3 / 164`. | `164 HILANG` | F04, F14. `45` selalu beratribusi “ringkasan hasil KNKT”; `164` tidak boleh menjadi “meninggal”. |
| S07 | `905–1.009` / 30,2–33,7 | `188` kembali ke label posko/hari ke-9. | `BUKAN ANGKA KAPAL. IA ANGKA POSKO.` | F04–F05 · KNKT I.2.2. |
| S08 | `1.010–1.123` / 33,7–37,5 | Lembar rekomendasi abstrak membuka “MANIFEST / SEBELUM / BERANGKAT”. | `REKOMENDASI KESELAMATAN` | F19 · sumber ringkasan/rekomendasi beratribusi, bukan bukti implementasi sesudah 2018. |
| S09 | `1.124–1.259` / 37,5–42,0 | Angka dan pertanyaan kembali; 19 frame terakhir diam sesudah VO. | `HITUNG 188 ATAU CARI?` | Sintesis editorial dari F04 dan F19. |

Setiap footer sumber yang terlihat di komposisi mengikuti tingkat bukti di atas.
Label `KNKT I.2.2 · REKOMENDASI KNKT` di scene penutup sengaja menggabungkan dua
sumber berbeda hanya untuk menandai dua bagian kalimat; itu **bukan** klaim bahwa
rekomendasi manifest muncul pada halaman I.2.2 laporan primer.

---

## 4 · Manifest aset dan provenance

### A. Aset visual scene — diverifikasi

| ID | Aset | Lokasi / pembuat | Lisensi / provenance | Verifikasi | Putusan |
|---|---|---|---|---|---|
| A01 | Grid, titik data, kartu angka, garis timeline, rute, kapal dan gelombang abstrak | Didefinisikan langsung di `SinarBangunPreprod.tsx` sebagai React/SVG/CSS | Kode original repository; tidak menyalin foto/footage | Inspeksi statis: tidak ada import media atau URL di scene | Pakai. |
| A02 | Space Grotesk 300/500/700 | `public/fonts/space-grotesk-latin-*-normal.ttf`, dimuat `src/fonts.ts` | SIL Open Font License 1.1 menurut loader proyek | SHA-256 tercatat di bawah | Pakai; file lokal existing, tidak dipindahkan/distribusikan ulang oleh pekerjaan ini. |
| A03 | Inter 500/600 | `public/fonts/inter-latin-*-normal.ttf`, dimuat `src/fonts.ts` | SIL Open Font License 1.1 menurut loader proyek | SHA-256 tercatat di bawah | Pakai. Browser dapat mensintesis weight 700/800 untuk label; tidak menambah file font baru. |
| A04 | Warna dan ukuran brand | `src/brand.json`, `src/theme.ts` | Aset brand repository | Nilai runtime dibaca lokal: ink/ivory/orange/sage, `1080×1920`, `30 fps` | Pakai. |

**Hash file font yang diperiksa pada pra-produksi**

```text
36b35f64ab48fbb9af3b3a608d0732629c65a1283499b11354a32c563326c3d0  space-grotesk-latin-300-normal.ttf
95873a0793b21b4d461f0eca3e32f7a875ba560ddd7e9678bb18824679c706b9  space-grotesk-latin-500-normal.ttf
174b4d6efdc0b2c8324577c8e1663957bf47a7d7435fd339b5be238659438bf5  space-grotesk-latin-700-normal.ttf
aa9045eb0c6e0f64d5803d15cb131bd049c854007f3f44ed88dcc41065f5fac8  inter-latin-500-normal.ttf
23ba116d0a2b428dd563e90e1bc5575a206eeb907310f66f7e1409fa7f8f3f9a  inter-latin-600-normal.ttf
```

### B. Aset yang sengaja tidak dicari/dipakai

| Kelas | Putusan | Alasan |
|---|---|---|
| Foto kapal, korban, keluarga, jenazah | Tidak dipakai | Tidak perlu untuk tesis; risiko salah konteks, lisensi, dan eksploitasi korban. |
| Footage banjir/gelombang dari lokasi lain | Tidak dipakai | Tidak boleh menyarukan rekaman lain sebagai kejadian Sinar Bangun 4. |
| Gambar generatif/foto-realistik kapal | Tidak dipakai | Bentuk data sudah menjelaskan konsep; gambar berisiko terbaca sebagai arsip atau rekonstruksi faktual. |
| Scan halaman laporan KNKT | Tidak dipakai pada baseline | Bila kelak dipakai, setiap halaman perlu URL, nomor halaman, crop, dan label `DOKUMEN KNKT · 2018` tersendiri. |
| Musik/SFX | Belum dipilih | Tidak esensial untuk proof; tidak ada file audio yang disalin atau dihasilkan sekarang. |

---

## 5 · QA pra-render yang sudah dan belum dilakukan

### Sudah dilakukan pada tahap ini

- Komposisi terdaftar di `src/Root.tsx` dengan ID eksplisit dan kontrak `1080×1920`
  / 30 fps / 1.260 frame (42,0 detik visual; termasuk hold 0,640 detik).
- Scene dibaca secara statis terhadap naskah dan lembar fakta: label `188`, `45`,
  `21`, `3`, dan `164 HILANG` mempertahankan batas sumbernya.
- Setelah persetujuan render terpisah, `scripts/render-ak-ep12-sinar-bangun-review.mjs`
  membundel komposisi dan menghasilkan raw video melalui `@remotion/renderer`.
  Sepuluh still QC mencakup semua sembilan scene serta hold akhir.
- Review master lokal melewati QC: H.264 `1080×1920`, `30/1 fps`, `yuv420p`, 1.260
  frame; audio AAC stereo 48 kHz; 42,005 detik kontainer; `−15 LUFS`, `−2,96 dBTP`.
  Hash elementary video raw/final identik (`1628a773…fe69191`), sehingga FFmpeg hanya
  mengubah audio/container dan tidak merender ulang visual.
- Manifest provenance review lokal berada di
  `11_CONTENT/06_UPLOAD/provenance/AK-EP12-sinar-bangun-remotion-review.json`; sumber
  visualnya native React/SVG/CSS/data motion, tanpa footage/foto eksternal.
- Tidak ada Drive, Zernio, queue, jadwal, unggahan, unlist, penghapusan, atau tindakan
  distribusi/publikasi yang dijalankan untuk AK-EP12.

### Gate render review lokal — selesai dengan persetujuan terpisah

- [x] Pemilik memilih narator feminin Indonesia; pembacaan sumber dan tes pemadatan
  diukur tanpa percepatan audio.
- [x] Pemilik menyetujui Pemadatan B dan C; take yang melampaui 45 detik tetap
  dikarantina tanpa time-stretch.
- [x] Copy C final, metadata, dan layout scene diselaraskan dengan take kontigu
  41,360 detik; `check_story.py`, `check_research.py`, dan `check_info_design.py`
  dijalankan ulang dengan hasil lulus.
- [x] Editor memeriksa ulang batas fakta/etik C: `164 HILANG`, 45 beratribusi,
  188 bukan manifest, tanpa nama/tuduhan/SPB/izin.
- [x] Persetujuan terpisah untuk satu render review lokal dicatat; preflight browser,
  bundle, renderer Remotion, frame QC, loudness, dan provenance lokal telah lulus.
- [x] Master review lokal dan raw visual Remotion tetap di `work/sinar-bangun/`; tidak
  ada transfer atau tindakan distribusi.
- [ ] Persetujuan distribusi/master publik yang eksplisit diperlukan **sebelum** Drive,
  queue, jadwal, upload, unlist, penghapusan, atau publikasi apa pun. Persetujuan itu
  belum diberikan.

**Batas berikutnya:** review master sudah tersedia secara lokal untuk peninjauan
pemilik. Tidak ada tindakan lebih lanjut terhadap distribusi atau kalender episode
kanonik sampai ada persetujuan eksplisit yang baru.
