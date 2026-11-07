# 05 — VISUAL PLAN

**Status: dibangun ulang dari yang benar-benar dirender.** Versi sebelumnya adalah
rencana; dokumen ini adalah deskripsi sistem yang sudah jalan. Kalau keduanya
berbeda, yang ini yang benar — karena EP01 sudah dirender jadi master 1080×1920
dengan audio nyata, dan setiap angka di bawah ini diambil dari kode dan dari file
hasil render, bukan dari perkiraan.

Koreksi kedua, dan ini yang paling penting: **versi pertama EP01 ternyata
cuma teks di atas latar statis.** Secara naskah ia lulus, secara tontonan ia mati
— tidak ada yang bergerak, tidak ada yang berubah, tidak ada alasan untuk tinggal.
Rencana ini sekarang dibangun di atas satu aturan: **setiap 1,5–2,5 detik harus
ada perubahan yang bisa dilihat**, dan tidak pernah ada frame yang diam.

| keputusan | status | alasan |
|---|---|---|
| plate vektor saja, teks di atas latar statis | **dibatalkan** | itulah keluhan penonton pertama: "pasif". Naskah yang bagus tidak menahan siapa pun di layar yang tidak berubah |
| foto generasi sebagai gambar penuh, tanpa gerak | **dibatalkan** | gambar yang diam tetap diam, sekalipun fotonya bagus |
| foto generasi + gerak kamera + grade + tipografi di atasnya | **dipakai** | foto memberi tempat, gerak memberi hidup, tipografi memberi arti. Satu foto tidak pernah tampil lebih dari 6 detik tanpa perubahan |
| rencana lama: `CountUp`, `MapDiagram`, `CrossSection`, 9 komponen | dibatalkan | sembilan gaya berbeda = tidak ada gaya. Diganti 2 komponen: `Photo` dan teks |
| footage stok | tidak dipakai | egress sandbox diblokir; semua gambar dibuat di mesin ini |

---

## 1 · EMPAT LAPIS: FOTO, GERAK, TEKS, ATMOSFER

| lapis | isi | dibuat oleh | catatan |
|---|---|---|---|
| **FOTO** | satu gambar per segmen: ruang, benda, laut, langit | `generate_image`, 768×1376, disimpan di `public/plates/EPxx/` | selalu bergerak; tidak pernah tampil diam |
| **GERAK** | push-in / tarik-out / geser kiri / geser kanan, goyang handheld, flicker exposure, garis sapuan | `src/scenes/PhotoScene.tsx` | dipilih bergiliran supaya dua segmen berurutan tidak bergerak ke arah yang sama |
| **TEKS** | hook, cue, caption, kutipan, pembalik, loop, nomor segmen, progres | `src/scenes/Episode.tsx` | satu pesan per frame |
| **ATMOSFER** | grade dingin, grain, vignette, kedip potongan | `Photo` + `CutFlash` | yang membuat potongan terasa, bukan patah |

Kalau sebuah episode belum punya foto, ia jatuh ke plate vektor (`PlateArt.tsx`,
10 bentuk) — tidak pernah layar kosong, tapi juga belum boleh disebut selesai.

Aturan gerak, dan ini yang menentukan penonton tinggal atau tidak:

| aturan | angka | kenapa |
|---|---|---|
| kamera tidak pernah diam | skala bergerak 0.11–0.13 sepanjang segmen | mata menangkap gerak sebelum menangkap isi |
| arah gerak berganti tiap segmen | 4 mode bergiliran | dua push-in berturut-turut terasa seperti berhenti |
| potongan | 10 potongan dalam 58 s (rata-rata 5,8 s) | cukup lama untuk dibaca, cukup pendek untuk tidak bosan |
| kedip potongan | 4 frame gelap (0.13 s), 34 % saat titik balik | membuat cut terasa disengaja |
| teks bergerak | per kata, 2 frame per kata | teks yang muncul sekaligus terasa seperti slide |
| progres terlihat | garis oranye di bawah, mengisi sepanjang durasi | penonton tahu "hampir selesai" — itu yang menahan mereka |

Kalau sebuah frame bisa dibingkai jadi poster tanpa kehilangan apa pun, frame itu
gagal — karena berarti tidak ada yang bergerak di dalamnya.

---

## 2 · FOTO PER SEGMEN (EP01)

Sepuluh segmen, sepuluh gambar, satu gambar per segmen — tidak ada yang dipakai
dua kali kecuali kalau maknanya berubah. Semua dalam satu resep: gelap, hampir
monokrom arang–tulang, satu aksen hangat, tanpa wajah, tanpa teks, ruang kosong
di sepertiga atas.

| segmen | gambar | isi | gerak kamera |
|---|---|---|---|
| hook | `01_hook` | pakaian tahan air di gantungan, boots kosong, lampu minyak | push-in |
| setup | `02_island` | pulau batu di laut luas, satu menara | tarik-out |
| tension 1 | `03_ship` | dek kapal uap, menara di balik kabut | geser kiri |
| tension 2 | `04_door` | pintu besi menara, tertutup, ombak | geser kanan |
| tension 3 | `06_lamp` | lensa fresnel bersih, minyak penuh, tak ada yang menjaga — sebelas hari | push-in |
| tension 4 | `05_table` | meja makan ditinggal, tiga kursi mundur — kerja pagi selesai | tarik-out |
| turn 1 | `08_logbook` | buku harian terbuka, jam berhenti | geser kiri |
| turn 2 | `07_oilskins` | pakaian itu, dari dekat | push-in |
| consequence | `09_sea_night` | laut malam, menara tanpa cahaya | geser kanan |
| loop | `10_loop` | lemari museum, pakaian yang sama, 126 tahun kemudian | push-in |

Aturan pemilihan gambar, bukan selera: **satu segmen = satu benda atau satu
ruang yang bisa disebut dalam satu kata.** Kalau sebuah gambar butuh dijelaskan,
ia salah untuk frame 2 detik.

Sepuluh bentuk vektor (`tower`, `vessel`, `shelter`, `road`, `paper`, `signal`,
`plume`, `water`, `dial`, `ridge`) tetap ada sebagai cadangan dan sebagai bahasa
grafis untuk episode yang fotonya belum dibuat.

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
| caption | Inter 600 | 54 px, line-height 1.30 | `bottom: 520` | **bukan transkrip**: satu kalimat ≤ 9 kata, muncul per kata (1,6 frame/kata), satu kata kunci oranye |
| angka besar (`Stamp`) | Space Grotesk 700 | 200–260 px, opasitas 0,14 | kanan atas, `top: 236` | angka dari beat itu menghantam masuk lalu menggeser 26 px; gerak grafis tanpa menambah teks |
| nomor segmen | Space Grotesk 700 | 30 px, tracking 0.34em | `top: 300`, kiri | `04 / 10` — memberi penonton rasa "hampir selesai" |
| footer | Space Grotesk 700 + Inter 600 | 30 / 22 px | `top: 1470` | `ODDCHAPTER` kiri, `HILANG · EP 01` kanan |

Tiga aturan teks, semuanya karena versi pertama terlalu banyak bicara di layar:

1. **Narasi panjang, caption pendek.** Yang didengar 14 kata; yang dibaca 7. Kalau
   keduanya sama, penonton membaca dan berhenti mendengar.
2. **Satu kata kunci oranye per caption.** Bukan untuk hiasan — itu yang tersisa
   di ingatan setelah scroll.
3. **Angka tidak ditulis dua kali.** Kalau ada `Stamp` besar (1900, 11, 26), cue
   tidak mengulanginya. Cue hanya label: `LAMPU MATI`, `SEBELAS HARI`.

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
| hook | 1 | berhenti menggulir | 5–7 s (foto sudah bergerak sejak frame 1) |
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

**Bed sudah ada di master EP01** dan dibuat di mesin ini, bukan diunduh:
angin pink-noise yang disaring (45–380 Hz), dua drone 48/121 Hz, dan empat
dentuman sub di titik-titik balik (hook 1,5 s · kutipan 36,4 s · pembalik 45,6 s ·
loop 50,7 s). Level bed mean −31 dB, puncak −10 dB — cukup terasa di speaker
kecil, tidak menutupi narasi.

**Efek per benda** dibuat oleh `tools/build_sfx.py` — disintesis dari osilator
dan noise ffmpeg, bukan sampel unduhan, lalu ditempatkan di frame segmennya
memakai timing nyata (mean −34,6 dB, puncak −12,9 dB):

| efek | resep | dipakai di EP01 |
|---|---|---|
| `rustle` | noise putih, band 600–3,2 kHz, tremolo 7 Hz | hook, pembalik (pakaian) |
| `gust` | pink noise, lowpass 520 Hz, swell 2,4 s | setup, sebelas hari |
| `engine` | dua sine 58/87 Hz + noise rendah | dek kapal |
| `clunk` | sine 120 Hz turun cepat + noise burst | pintu terkunci |
| `tick` | dua tick 2,6 kHz lalu hening | jam berhenti |
| `page` | noise band 2–6 kHz, 0,22 s | buku harian |
| `boom` | sine 42 Hz, decay 2,4 s | consequence, loop |

Menambah efek = menambah satu baris di `sfx` (`content_data.py`), lalu jalankan
`python3 tools/build_sfx.py EPxx`. Tidak ada file yang diunduh.

Yang belum ada: musik tonal. Di 58 detik, musik tonal cepat jadi "stok video";
angin + sub + efek benda sudah cukup memberi ruang.

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
7. **Uji gerak:** ambil dua frame berjarak 2 detik di tengah setiap segmen; kalau
   keduanya identik, segmen itu statis dan tidak boleh lolos.

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
