# 05 — VISUAL PLAN

**Status: dibangun ulang dari yang benar-benar dirender.** Versi sebelumnya adalah
rencana; dokumen ini adalah deskripsi sistem yang sudah jalan. Kalau keduanya
berbeda, yang ini yang benar — karena EP01 sudah dirender jadi master 1080×1920
dengan audio nyata, dan setiap angka di bawah ini diambil dari kode dan dari file
hasil render, bukan dari perkiraan.

Yang dibatalkan dari rencana lama, dan alasannya:

| rencana lama | status | alasan |
|---|---|---|
| plate gambar generasi (`GEN`) sebagai lapis utama tiap episode | **dibatalkan** | gambar generasi tidak akurat secara faktual; kalau ia penuh layar, penonton melihat "gambar AI", dan efek yang kita kejar (percaya → terasa ada yang salah) langsung hilang |
| peta/grafik `ARC` dari GeoJSON | **dibatalkan** untuk 21 episode ini | menambah waktu render dan satu lapis kesalahan fakta (skala, proyeksi) yang tidak sepadan dengan durasi 58 detik |
| 8 komponen baru (`HairGrid`, `CountUp`, `MapDiagram`, `CrossSection`, `Radial`, `Dial`, `Keyword`, `LoopBack`) | **diganti** oleh 1 komponen plate + 4 komponen teks | sembilan komponen = sembilan gaya. Satu bahasa visual lebih kuat dan lebih murah dirawat |
| footage stok | tetap tidak dipakai | egress sandbox diblokir; rencana ini tidak bergantung padanya |

Yang dipertahankan: satu master vertikal per episode, 30 fps, 1080×1920, semua
teks dibakar, tidak ada dissolve — potongan keras.

---

## 1 · TIGA LAPIS, DAN TIDAK ADA YANG PENUH LAYAR

| lapis | isi | dibuat oleh | catatan |
|---|---|---|---|
| **PLATE** | satu bentuk dasar: menara, kapal, tenda, jalan, kertas, sinyal, gunung, air, dial, bukit | `src/scenes/PlateArt.tsx` — SVG, 10 bentuk | napas skala 1.000 → 1.045 sepanjang episode, 1 warna aksen |
| **TEKS** | hook, cue, caption narasi, kartu titik balik, loop | `src/scenes/Episode.tsx` | satu pesan per frame, tidak pernah dua blok bersaing |
| **ATMOSFER** | grain 44 baris, vignette bawah, gradien radial di garis horizon | `Grain` + dua `AbsoluteFill` | membuat SVG datar terasa seperti film, bukan slide |

Aturannya: **tidak ada satu pun frame yang berupa satu gambar besar**. Plate
selalu garis dan bidang tipis di atas latar gelap; teks selalu punya ruang
kosong di sekitarnya. Kalau sebuah frame bisa dibingkai jadi poster tanpa
kehilangan apa pun, frame itu gagal.

---

## 2 · SEPULUH BENTUK DASAR

Semua episode memakai aturan gambar yang sama: latar `#17191D`, garis rambut
`sage` 1–1.6 px, siluet `ivory` 2–2.4 px dengan opasitas 0.16–0.62, dan **satu**
aksen `orange` yang mewakili satu benda penting di episode itu.

| # | bentuk | apa yang digambar | dipakai | aksen oranye = |
|---|---|---|---|---|
| 01 | `tower` | badan menara trapesium, galeri, lentera, dua celah jendela | EP01 | lampu yang masih menyala |
| 02 | `vessel` | lambung, dua tiang, tali, lentera tiang depan | EP03 | lentera yang tidak dijaga |
| 03 | `shelter` | tenda dengan tali pasak, pintu terlipat, satu sisi disobek | EP02, EP07, EP16 | kain yang terbuka dari dalam |
| 04 | `road` | jalur menyempit ke satu titik di ufuk, garis tengah putus | EP04, EP06, EP12 | titik tujuan yang tidak masuk akal |
| 05 | `paper` | lembar miring, 12 garis tulis, satu garis digarisbawahi | EP08, EP09, EP10 | kata yang tidak bisa dijelaskan |
| 06 | `signal` | enam busur konsentris + satu garis datar di bawah | EP11, EP14 | sumber sinyal |
| 07 | `plume` | kerucut gunung, kawah, kolom abu vertikal | EP17, EP18 | pijar di kawah |
| 08 | `water` | permukaan bergaris, dua tebing, refleksi terbalik | EP20 | garis pijar di permukaan |
| 09 | `dial` | 60 takik, dua jarum, satu angka berbahaya | EP21 | angka tempat jarum berhenti |
| 10 | `ridge` | tiga lapis punggung bukit, satu tiang berdiri | EP05, EP13, EP15, EP19 | ujung tiang |

Plate dipilih lewat field `plate` di `tools/content_data.py` dan divalidasi oleh
`tools/build_episodes_json.py` (nama plate yang tidak ada langsung gagal).

Cara memeriksa kesepuluhnya dalam satu menit:

```
node scripts/still-plates.mjs      # -> output/plates/plate_00..09.png
```

`PLATE-GALLERY` adalah komposisi 10 frame di `Root.tsx`; frame ke-n = bentuk ke-n.
Kalau salah satu bentuk tidak lagi terlihat satu keluarga dengan yang lain, itu
terlihat di sini sebelum 21 episode dirender.

---

## 3 · TIPOGRAFI

Space Grotesk 700 untuk pernyataan, Inter 600 untuk keterangan. Tidak ada font
ketiga, tidak ada italic, tidak ada drop shadow selain scrim caption.

| elemen | font | ukuran | letak | catatan |
|---|---|---|---|---|
| hook (judul episode) | Space Grotesk 700 | 92 px, turun ke 84/72/62 untuk teks panjang | atas, `top: H×0.22` | muncul per kata, 2 frame per kata, keluar dengan `clipPath` |
| loop (penutup) | Space Grotesk 700 | 74 px, sama, `fit()` | `top: H×0.24` | kalimat yang mengembalikan penonton ke hook |
| kutipan titik balik | Space Grotesk 700 | 96 px | tengah vertikal | satu coretan oranye 9 px menimpa kutipan |
| kalimat pembalik | Inter 600 | 44 px, orange | bawah kutipan, +56 px | satu baris, tidak pernah lebih |
| label "yang selama ini dikutip" | Inter 600 | 25 px, tracking 0.32em, sage | atas kutipan | satu-satunya label yang boleh mendahului kutipan |
| cue | Inter 600 | 24 px, tracking 0.28em, sage | `top: 300`, kiri | mis. `SEBELAS HARI` |
| caption narasi | Inter 600 | 52 px, line-height 1.32 | `bottom: 520` | durasi = durasi audio segmen itu |
| nomor segmen | Space Grotesk 700 | 30 px, tracking 0.34em | `top: 300`, kiri | `04 / 10` — memberi penonton rasa "hampir selesai" |
| footer | Space Grotesk 700 + Inter 600 | 30 / 22 px | `top: 1470` | `ODDCHAPTER` kiri, `HILANG · EP 01` kanan |

**Aturan yang lahir dari kegagalan nyata:** setiap teks yang panjangnya tidak
diketahui saat menulis kode wajib melewati `fit()` (auto-downscale 4 tingkat).
Tanpa itu, satu kata panjang (`…dua puluh delapan…`) melewati tepi kanan dan
terpotong di master — sudah terjadi, sudah diperbaiki, jangan diulang.

Zona aman: **x 96–984, y 300–1500.** Footer di 1470 masih di dalam; caption
tidak pernah turun di bawah 520 karena area 0–1500 dipakai plate.

Warna caption tidak pernah orange. Orange hanya untuk satu hal penting per frame.

---

## 4 · RITME: SEGMEN, BUKAN DURASI

Satu episode = 9–10 segmen, dan setiap segmen adalah satu file audio. Yang
menentukan kapan sebuah teks muncul bukan perkiraan, tapi durasi file itu.

```
hook → setup → tension ×4 → turn ×2 → consequence → loop
```

| bagian | jumlah | fungsi efek | durasi khas |
|---|---|---|---|
| hook | 1 | berhenti menggulir | 5–7 s |
| setup | 1 | dunia terbentuk, satu benda konkret | 6–8 s |
| tension | 4 | sesuatu salah, tidak dijelaskan | 4–9 s masing-masing |
| turn | 2 | kutipan yang selama ini dipercaya, lalu dibalik | 4–5 s + 4–5 s |
| consequence | 1 | apa artinya kalau pembalikan itu benar | 4–5 s |
| loop | 1 | kembali ke benda di hook, dengan makna baru | 5–6 s |

Jarak antar segmen 0.30 s, ekor 1.2 s. Diukur oleh `tools/build_timing.py`, yang
membaca durasi audio nyata lewat `ffprobe` (fallback: stderr `ffmpeg`), lalu
menulis `timing.generated.json` — satu-satunya sumber waktu untuk video.

EP01, terukur: 1748 frame = **58,2 detik**, 10 segmen.
`hook 18 · setup 238 · tension 442/628/777/957 · turn 1092/1222 · consequence 1368 · loop 1520`.

Konsekuensi desain: durasi episode **tidak boleh** ditetapkan lebih dulu. Narasi
yang menentukan; `durasi` di content_data hanya perkiraan untuk kalender.

---

## 5 · SUARA

Satu narator untuk 21 episode (`voice-01`, Indonesia netral), tempo dinaikkan
`atempo=1.12` setelah pengukuran — TTS keluar terlalu lambat untuk format 1 menit.

| tahap | perintah | hasil |
|---|---|---|
| sintesis | 9–10 klip per episode, satu per segmen | 4.5–8 s per klip |
| kecepatan | `ffmpeg -filter:a "atempo=1.12" -c:a libmp3lame -q:a 4` | asli disimpan di `audio/EPxx/raw/` |
| ukur | `ffprobe` → `timing.generated.json` | `audioMeasured: true` |
| master | `scale=in_range=full:out_range=tv,format=yuv420p` + `loudnorm=I=-14:TP=-1.5:LRA=11` + `crf 18` + `+faststart` | mean −17.3 dB, max −1.5 dB (terukur di EP01) |

Belum ada musik dan belum ada SFX di master EP01. Itu keputusan, bukan
keterlambatan: di 58 detik dengan satu suara, musik hanya menambah lapisan yang
harus diadili sendiri. Kalau nanti ditambahkan, bed masuk di −28 LUFS.

---

## 6 · RENDER

```
node scripts/still-plates.mjs            # 10 bentuk dasar
node scripts/still-ep01.mjs 24 150 760   # frame kunci EP01
node scripts/render-episode.mjs EP01     # master
```

`render-episode.mjs` melakukan: bundle → pilih komposisi `ODDCHAPTER-EPxx` →
render h264 + aac → `loudnorm` → `+faststart` → `ffprobe` → tulis
`output/episodes/EPxx.report.json`.

Angka nyata EP01 (Chromium `@sparticuz/chromium` 153, `gl: swangle`, concurrency 2):

| | |
|---|---|
| resolusi / fps | 1080×1920 / 30 |
| durasi | 58.28 s |
| video | h264 High, yuv420p (konversi full→tv range saat normalisasi) |
| audio | aac 48 kHz stereo 192k |
| ukuran master | 3,1 MB (CRF 18; konten gelap-statistik terkompresi sangat efisien) |
| waktu render | ≈13–15 menit per episode di sandbox ini |

Catatan operasional: dengan concurrency default, browser sempat mati di frame 378
(`target closed`). Concurrency 2 + `imageFormat: jpeg` stabil. Kalau render gagal,
ulangi — jangan turunkan resolusi.

---

## 7 · QA SEBELUM SEBUAH EPISODE DISEBUT SELESAI

1. `python3 tools/check_story.py EPxx` → 0 masalah (gerbang lima efek).
2. Tiga still dari master (hook, titik balik, loop) dilihat dengan mata:
   tidak ada teks yang menyentuh tepi, tidak ada teks menabrak footer.
3. `ffprobe` master: 1080×1920, 30 fps, ada stream audio, durasi ±1 s dari rencana.
4. `volumedetect`: max ≤ −1.0 dB, mean antara −20 dan −14 dB.
5. `audioMeasured: true` di `timing.generated.json`.
6. Judul di layar = judul di script (`build_episodes_json.py` sudah dijalankan).

Poin 6 punya sejarah: `episodes.generated.json` dulu tidak punya generator,
sehingga EP01 sempat dirender dengan judul lama sementara script-nya sudah
berubah. Sekarang file itu dihasilkan, bukan ditulis tangan.

---

## 8 · STATUS PER EPISODE

| plate | siap | timing + audio | master |
|---|---|---|---|
| EP01 `tower` | ya | ya (terukur) | **ya** — 58.28 s |
| EP02–EP21 | ya (bentuk sudah ada) | belum — butuh 9–10 klip narasi | belum |

Bentuk untuk 21 episode sudah ada semua; yang belum ada hanya suara. Urutan
produksi per episode karena itu: narasi → ukur → still → master → QA.
