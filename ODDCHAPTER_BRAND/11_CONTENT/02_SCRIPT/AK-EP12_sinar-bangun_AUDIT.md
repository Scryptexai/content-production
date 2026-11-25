# Audit naskah Short — AK-EP12 · Sinar Bangun 4

**Status:** `PRA-PRODUKSI LENGKAP — copy C final, take VO terukur, scene, dan aset
sudah siap untuk review pra-render; belum ada render, master video, antrean, Drive,
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
| `python3 ODDCHAPTER_BRAND/tools/check_story.py AK-EP12` | **LULUS** — 41,36 detik dari pengukuran VO, echo `kapal`, tanpa kegagalan. |
| `python3 ODDCHAPTER_BRAND/tools/check_research.py AK-EP12 -v` | **LULUS** — hook, seluruh beat, dan loop copy C final memiliki token fakta dari `AK-EP12_sinar-bangun_fakta.md`. |
| `python3 ODDCHAPTER_BRAND/tools/check_info_design.py AK-EP12 -v` | **LULUS 7/7** — kronologi, karantina putusan, celah, tesis–antitesis–sintesis, angka, dan suara penyelidik/ajakan langsung. |
| `python3 ODDCHAPTER_BRAND/tools/check_longform.py LF03_sinar-bangun` | **LULUS** — regresi induk tetap 1.424 kata / sekitar 9,5 menit. |
| `python3 -m py_compile ...` dan JSON gate | Lulus sebelum commit. |

## Catatan mekanis

Pemeriksa riset kini juga mengenali singkatan lembaga huruf kapital, seperti `KNKT`,
sebagai token fakta. Perubahan itu diperlukan karena Short memakai rekomendasi KNKT
dalam satu baris yang tidak membawa angka; sebelumnya tokeniser hanya mengenali nama
dengan huruf awal kapital seperti `Sinar` atau `Bangun`.

Heuristik kata sebelumnya menghitung digit sebagai satu token dan terlalu pendek saat
angka dibaca penuh dalam bahasa Indonesia. `check_story.py` kini menerima
`measured_duration_seconds` tervalidasi sebagai bukti yang lebih kuat daripada
heuristik; tanpa pengukuran field itu tetap memakai estimasi lama. Copy C final,
dibaca natural oleh narator feminin terpilih, mengukur **41,360 detik** (PCM S16LE,
24 kHz, mono) dan lulus target 35–45 detik. Baca sumber 55,080 detik, B tepat 45,800
detik, B cue terpisah 49,160 detik, serta C token-gated 45,080 detik dikarantina tanpa
time-stretch. Detail hash dan jalur aset ada di
`AK-EP12_sinar-bangun_PREPRODUCTION.md` §2a.

Pemeriksa story/info-design juga mengakui pertanyaan langsung dan imperatif mental
seperti `hitung`/`cari` sebagai ajakan penonton, selain `kamu`/`kita`/`anda`; perubahan
ini mempertahankan tuntutan suara penyelidik pada copy ringkas dan regresi EP11 lulus.

## Keputusan visual pra-produksi

Rencana yang diizinkan sekarang hanya memakai scene desain informasi Remotion: meja
posko, titik data, garis rute skematis, timeline, siluet kapal generik, dan kartu
angka. Implementasi source-nya ada di
`10_FILM/remotion/src/scenes/SinarBangunPreprod.tsx`; paket cue, manifest, sumber,
dan hash font ada di `AK-EP12_sinar-bangun_PREPRODUCTION.md`.

Tidak perlu mencari stock footage untuk meloloskan gate visual. Scene tidak mengimpor
foto, video, audio, URL, atau visual generatif; ia memakai SVG/CSS/data motion lokal.
Tidak ada bundel Remotion runtime, render still, `renderMedia`, FFmpeg, atau media
master yang dijalankan/dihasilkan. Esbuild hanya memeriksa source statis; ia tidak
memanggil renderer atau menghasilkan media.

## Gerbang berikutnya

- [x] Pemilik menyetujui Short, kartu angka, dan arah visual **sebatas
      pra-produksi**.
- [x] Cue VO, baseline frame, manifest aset, source mapping, dan batas etik dicatat
      dalam `AK-EP12_sinar-bangun_PREPRODUCTION.md`.
- [x] Pemilik memilih narator feminin Indonesia dan menyetujui Pemadatan B/C; seluruh
      take yang melewati 45 detik dikarantina tanpa time-stretch.
- [x] Copy C final, VO kontigu 41,360 detik, source/visual timing, dan tiga gate
      diperbarui serta lulus; static bundle check tidak memanggil renderer.
- [ ] Persetujuan pre-render/render-master terpisah diterima sebelum bundle/renderer,
      caption, render Remotion, atau QC teknis dijalankan.
- [ ] Review master terpisah sebelum Drive, queue, jadwal, atau unggah.
