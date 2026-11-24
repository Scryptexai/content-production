# AK-EP12 — paket pra-produksi Remotion / VO / aset

**Status:** `PRA-PRODUKSI DIIZINKAN — BUKAN IZIN RENDER ATAU DISTRIBUSI`

Persetujuan pemilik atas Short mengizinkan dua hal saja: perencanaan scene 9:16
Remotion dan penyiapan VO/aset yang dapat diverifikasi. Tidak ada master video,
frame render, transfer Drive, queue, jadwal, unggahan, atau perubahan pada episode
kanonik `EP12` (MV Joyita) yang dibuat atau diizinkan oleh berkas ini.

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
| Timing bench | `1.200` frame / **40,0 detik** | Baseline berada dalam target 35–45 detik; bukan durasi master. VO terukur berhak mengubah batas scene, bukan mengubah fakta/naskah tanpa audit. |
| Mesin visual | React + Remotion SVG/CSS/data motion | Saat master disetujui, seluruh frame harus keluar dari `@remotion/renderer`; FFmpeg, bila kelak dipakai, hanya post-render audio/container/QC. |
| Audio pada komposisi | **Tidak ada** | File scene sengaja silent; belum ada audio yang ditempel, dibundel, atau dirender. |
| Gaya potong | Hard cut dengan masuk/keluar 10–18 frame | Tidak ada dissolves, footage bencana, atau rekonstruksi yang diklaim arsip. |

`SinarBangunPreprod.tsx` memakai hanya bentuk SVG, teks, CSS gradient, dan titik
data deterministik. Tidak ada `Img`, `Video`, `Audio`, `staticFile` media, API,
atau aset web eksternal di scene tersebut. Karena itu implementasi dapat ditinjau
sebagai desain informasi tanpa mencari foto kapal atau footage tragedi.

---

## 2 · Peta VO yang siap direkam

Teks di bawah identik secara makna dengan naskah Short yang sudah lulus gate. Tanda
waktu adalah **cue editing sementara**. Pembacaan sumber sudah diuji setelah pemilik
memilih narator feminin berbahasa Indonesia; hasilnya dicatat di §2a dan tidak
mengubah naskah terkunci tanpa keputusan editorial berikutnya.

| Cue | Waktu rencana | Teks rekam yang diverifikasi | Frame / scene | Fakta |
|---|---:|---|---|---|
| V01 | 0,0–3,5 | Angka 188 baru muncul sembilan hari sesudah kapal tenggelam. | `0–104` · data posko | F04, F05 |
| V02 | 3,5–7,0 | Menurut kamu, kenapa 188 baru ada sesudah kapal tenggelam? | `105–209` · rute skematis | F04, F05 |
| V03 | 7,0–10,5 | Kita kira 188 dihitung di dermaga. | `210–314` · titik dermaga | F04 |
| V04 | 10,5–15,0 | 18 Juni 2018, Sinar Bangun 4 berangkat pukul 16.50. | `315–449` · timeline | F01 |
| V05 | 15,0–20,0 | Dua puluh menit, gelombang 1,5 sampai 2 meter membalikkan kapal. | `450–599` · gelombang abstrak | F02 |
| V06 | 20,0–27,0 | Lihat angka ini: 45 di dokumen; 21 selamat; 3 meninggal; 164 hilang. | `600–809` · kartu angka | F04, F14 |
| V07 | 27,0–32,0 | Coba baca KNKT: 188, tapi bukan angka dermaga. | `810–959` · kalimat tanda tangan | F04, F05 |
| V08 | 32,0–36,0 | KNKT meminta manifest sebelum kapal berangkat. | `960–1.079` · dokumen abstrak | F19 |
| V09 | 36,0–40,0 | Sebelum kapal berangkat, kamu menghitung 188 atau mencarinya? | `1.080–1.199` · loop angka | F04, F19 |

### Aturan pembacaan dan pengukuran

1. Rekaman memakai bahasa Indonesia natural: `188` dibaca *seratus delapan puluh
delapan*, `16.50` dibaca *enam belas lima puluh*, dan `1,5–2 meter` dibaca *satu
setengah sampai dua meter*. Tidak ada SSML/markup pada naskah rekam.
2. Gunakan satu suara internal kanal yang **dipilih/disetujui pemilik**; rencana
   produksi induk melarang `voice-06` dan `voice-07`. Pemilik telah memilih kandidat
   **feminin / id-ID** pada audisi. ID penyedia bersifat sesi dan tidak dicatat sebagai
   kredensial/pengganti persetujuan editorial.
3. Pembacaan sumber sembilan cue telah diukur (lihat §2a) dan melampaui 45 detik.
   Karena itu ia dikarantina sebagai bukti timing gagal—bukan take final. Bila total
   melampaui 45 detik, potong kata dengan audit editorial—jangan mempercepat audio
   secara buta.
4. Sebelum render, pemeriksa mengonfirmasi kata `hilang` pada V06 dan bahwa V07
   tidak mengubah `188` menjadi manifest. Tidak ada nama orang, tuduhan, SPB, atau
   angka kematian pasti di VO.

### 2a · Hasil audisi dan uji waktu — belum menjadi VO final

Pemilik memilih kandidat **narator feminin Indonesia** pada audisi. Audio berikut
adalah bahan pra-produksi lokal, bukan media master, dan tidak ditambahkan ke
komposisi, dibundel, dirender, atau dipindah ke Drive.

| Uji | Materi | Hasil ukur `ffprobe` | Putusan |
|---|---|---:|---|
| A · baca naskah sumber | Sembilan cue persis seperti tabel V01–V09; PCM S16LE, 24 kHz, mono | **55,080 detik** tanpa jeda tambahan | **GAGAL** target 35–45 detik. Dikarantina; tidak boleh dipercepat atau dipakai sebagai master. |
| B · tes pemadatan | Satu take kontigu dari teks kandidat di bawah; PCM S16LE, 24 kHz, mono | **41,920 detik** | Lulus durasi sebagai **tes saja**. Teksnya belum menggantikan naskah/gate dan menunggu persetujuan editorial pemilik. |

Take A dipindahkan ke `work/sinar-bangun/vo_internal/rejected-original-read/` agar
tidak tertukar dengan kandidat berikutnya. File uji B berada di
`work/sinar-bangun/vo_internal/AK-EP12_cut-B_duration-test.wav`; SHA-256-nya adalah
`9c759824d9e9f7d46443cd06f7fa6cab28af766f50a92d1286f25acb3135a66f`.
Tidak ada file audio yang dipentaskan sebagai `master`.

**Kandidat pemadatan B — hanya untuk keputusan editorial**

> Angka 188 muncul sembilan hari sesudah kapal tenggelam. Kenapa baru muncul
> sesudahnya? Kita kira dihitung di dermaga. Pada 18 Juni 2018, kapal berangkat pukul
> 16.50. Dua puluh menit kemudian, gelombang 1,5 sampai 2 meter membalikkan kapal.
> Dokumen: 45. Posko: 188. 21 selamat, 3 meninggal, 164 hilang. Di KNKT, 188 bukan
> angka dermaga. KNKT meminta manifest sebelum berangkat. Hitung sebelum berangkat,
> atau cari sesudahnya?

Pemadatan B tidak menambah fakta: F01, F02, F04, F05, F14, dan F19 tetap satu-satunya
landasannya. Namun ia mengubah redaksi hook, pertanyaan, dan setup; karena itu ia
**belum** boleh menggantikan naskah sumber sampai pemilik menyetujuinya dan ketiga
gate Short dijalankan ulang. Jika disetujui, pertanyaan B akan ditulis menjadi
`Kenapa 188 baru muncul sesudahnya?` agar tetap membawa token fakta eksplisit sebelum
pembuatan ulang take terpisah.

---

## 3 · Daftar scene dan jejak sumber

| Scene | Frame / detik baseline | Gerak yang diimplementasikan | Teks layar utama | Sumber / batas |
|---|---:|---|---|---|
| S01 | `0–104` / 0,0–3,5 | Grid data dan titik bergerak mengunci ke `188`; bukan gambar manusia. | `VERIFIKASI HARI KE-9 · BUKAN MANIFEST` | F04–F05 · KNKT I.2.2. |
| S02 | `105–209` / 3,5–7,0 | Garis rute skematis dan ikon perahu generik bergerak Simanindo → Tigaras. | `KAPAN ANGKA INI ADA?` | F01 · KNKT I.1. Bukan peta presisi/GIS. |
| S03 | `210–314` / 7,0–10,5 | Lingkaran data, bukan wajah/penumpang, bergerak di bidang dermaga. | `KITA KIRA 188 DIHITUNG DI DERMAGA.` | F04 · klaim persepsi editorial, bukan fakta bahwa manifest tersedia. |
| S04 | `315–449` / 10,5–15,0 | Timeline aktif dari `16.50` menuju `17.10`; rute normal `30 MENIT` muncul sebagai konteks. | `18 JUNI 2018 · DUA PULUH MENIT` | F01–F02, F11 · KNKT I.1. |
| S05 | `450–599` / 15,0–20,0 | Gelombang abstrak dari kiri memiringkan siluet kapal generik. | `1,5–2 M` dan `BUKAN ARSIP KEJADIAN` | F02 · diagram, bukan rekonstruksi/footage kejadian. |
| S06 | `600–809` / 20,0–27,0 | Kontras `45` dan `188`, lalu kartu bergerak `21 / 3 / 164`. | `164 HILANG` | F04, F14. `45` selalu beratribusi “ringkasan hasil KNKT”; `164` tidak boleh menjadi “meninggal”. |
| S07 | `810–959` / 27,0–32,0 | `188` kembali ke label posko/hari ke-9. | `BUKAN ANGKA KAPAL. IA ANGKA POSKO.` | F04–F05 · KNKT I.2.2. |
| S08 | `960–1.079` / 32,0–36,0 | Lembar rekomendasi abstrak membuka “MANIFEST / SEBELUM / BERANGKAT”. | `REKOMENDASI KESELAMATAN` | F19 · sumber ringkasan/rekomendasi beratribusi, bukan bukti implementasi sesudah 2018. |
| S09 | `1.080–1.199` / 36,0–40,0 | Angka dan pertanyaan kembali; tidak ada CTA/upload card. | `HITUNG 188 ATAU CARI SESUDAHNYA?` | Sintesis editorial dari F04 dan F19. |

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

- Komposisi didaftarkan di `src/Root.tsx` dengan ID eksplisit dan kontrak `1080×1920`
  / 30 fps / 1.200 frame.
- Scene dibaca secara statis terhadap naskah dan lembar fakta: label `188`, `45`,
  `21`, `3`, dan `164 HILANG` mempertahankan batas sumbernya.
- Tidak ada aset visual eksternal, master, screenshot, bundel Remotion runtime,
  render still, `renderMedia`, FFmpeg, Drive, Zernio, queue, jadwal, atau upload yang
  dijalankan untuk AK-EP12. Satu-satunya media baru adalah test VO lokal yang diukur
  dan dikarantina di §2a.

### Wajib selesai **sebelum meminta** persetujuan pra-render/master yang terpisah

- [x] Pemilik memilih narator feminin Indonesia; pembacaan sumber dan tes pemadatan
  diukur tanpa percepatan audio.
- [ ] Pemilik menyetujui/menolak Kandidat Pemadatan B. Jika disetujui, editor
  memperbarui naskah/metadata, menjalankan tiga gate, lalu membuat ulang sembilan cue
  final yang terpisah dan mengukur ulang totalnya.
- [ ] Editor menandatangani perubahan cue/frame yang mungkin dibutuhkan oleh VO
  terukur dan melakukan pembacaan ulang etik/fakta.
- [ ] Bundle/renderer preflight, render review/master Remotion, caption, loudness,
  QC frame, serta provenance dijalankan **hanya** dengan persetujuan terpisah.
- [ ] Persetujuan master diberikan sebelum tindakan Drive, queue, jadwal, upload,
  unlist, penghapusan, atau publikasi apa pun.

**Permintaan keputusan berikutnya:** pilih apakah Kandidat Pemadatan B boleh
menggantikan copy VO sumber. Sesudah itu barulah sembilan cue final dan timing scene
dapat dikunci. Persetujuan pra-render/master harus disebut terpisah dan tidak tersirat
dari persetujuan ini.
