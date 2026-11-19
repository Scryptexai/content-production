# SERI ANGKER — AK-EP01 (Sengkon & Karta) — TAYANG

**Tayang** 19 Nov 2026 14:12 UTC · https://www.youtube.com/watch?v=_n8noXxix3k · post Zernio `6aff03a6858a651f34f13abc` (publik, Entertainment).

Judul: `12 Tahun Dipenjara untuk Pembunuhan yang Tak Pernah Mereka Lakukan.`
Hook (baris pertama deskripsi): `Kalau Genul tak pernah bicara... siapa yang akan menolong mereka?`
Deskripsi: 15 hashtag (#Shorts #oddchapter #sengkonkarta #salahtangkap #salahpidana #sejarahindonesia #kasusnyata #hukumindonesia #peninjauankembali #mahkamahagung #cipinang #bekasi #1974 #truecrime #kisahnyata) + tag YouTube 15 (182 karakter).

## Mengapa EP01 ILLUMINATI tidak dapat distribusi

Empat sebab yang paling mungkin, berurutan menurut dampak:

1. **Topiknya konspirasi.** "Illuminati" masuk wilayah yang paling sering diturunkan jangkauannya
   (misinformasi/konspirasi). Format apa pun akan kena atapnya. Seri angker memakai
   **kasus nyata yang terdokumentasi** — aman dari kategori itu.
2. **Tidak ada alasan menonton sampai habis.** Shorts dinilai dari *retensi*, bukan panjang.
   Video 8 menit dengan pembuka panjang = mayoritas penonton geser di 1–2 detik pertama.
   Pilot ini membuka dengan satu kalimat yang isinya sudah berupa teka-teki (0–2,3 dtk).
3. **Materi terlihat "dibuat ulang".** Footage stok berulang + caption bakar penuh bisa terbaca
   sebagai konten daur ulang. Pilot ini memakai **foto arsip asli 1980** (Kompas, Sinar Harapan,
   Wikimedia) dengan kredit per foto — nol klip YouTube, jadi tidak ada jejak *reused content*.
4. **Tidak ada identitas seri.** Penonton tidak tahu ini bagian dari apa. Seri angker punya
   palet, tipografi, kartu akhir, dan penanda "ODDCHAPTER · KASUS NYATA · ARSIP ASLI".

## Struktur baru (dipakai pilot, ±1:56)

| Waktu | Beat | Isi | Alat |
|---|---|---|---|
| 0:00–0:02 | Hook visual | "PEMBUNUH ASLINYA / SATU PENJARA" di atas kertas koran gelap | kartu + Anton merah |
| 0:02–0:08 | Janji | Kalimat pembuka VO: pembunuh asli satu penjara, hukum tak bisa apa-apa | foto arsip + tag sumber |
| 0:08–0:55 | Kasus | 1974 pembunuhan → ditangkap → pengakuan → vonis **12 th & 7 th** | koran, cap "OKT 1977", angka besar |
| 0:55–1:21 | Balik | Tahanan yang sama membuka rahasia → **GENUL** (drop audio, hening 1,3 dtk) | kartu GENUL + riser |
| 1:21–1:41 | Dinding | Putusan final, cap **INKRACHT**, 4 Nov 1980 keluar | foto arsip nyata |
| 1:41–1:57 | Pamungkas | Tanah habis, Karta 1982, Sengkon 1988 → lahir PK → pertanyaan balik ke penonton | kartu akhir + kredit |

Aturan teknis yang dipegang: potong gambar **0,15 dtk sebelum kata jangkar** (dari `vo_alignment.json`),
caption 1–3 kata di zona aman (margin bawah 672 px), kata kunci merah #D82A2A,
grade dingin (sat 0,30 · kontras 1,18 · gamma 0,85), grain + vignette + kedip halus,
satu *drop* audio per video (−1,5 dBTP, −15 LUFS).

## Berkas

| berkas | ukuran | Drive id |
|---|---|---|
| `AK-EP01_sengkon-karta_short_v1.mp4` | 36.032.330 B · 1:56,60 · 1080×1920 · 30 fps | `1mtyEyBXhWsnPvrNDzG3V_hYhoHddqOiW` |
| `AK-EP01_thumbnail_16x9.jpg` | 131.370 B · 1280×720 | `1v6p1e5qFJXoWPnLteM1zk6Zo3rZmZT63` |
| `AK-EP01_poster_9x16.jpg` | 189.695 B · 1080×1920 | `1X2Sied_7G9-pddORMIiZG9uTV5hf3o60` |
| `AK-EP01.id.srt` | 75 cue | `1wXR2d4H-P8_V453M7bhhjGiTIV09I0P_` |

Folder Drive: **Angker Bot / ODDCHAPTER / sengkon-karta** (`1s1ianisjYVPQXKw9hnUGsOcBOOvb-p2Y`), semua publik.

QA lolos: durasi 116,60 dtk · −15,0 LUFS · TP −1,5 dBFS · yuv420p tv/bt709 ·
`upload_zernio.py` tanpa ✗ (judul 71 karakter, hook pertanyaan, deskripsi 835 karakter, thumbnail < 2 MB).

## Cara membangun ulang

```bash
export FFMPEG=$(python3 -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())")
python3 ODDCHAPTER_BRAND/tools/build_short_angker.py all   # 32 shot → video → bed+mix → mux
python3 ODDCHAPTER_BRAND/tools/make_thumb_angker.py        # thumbnail 16:9 + poster 9:16
python3 ODDCHAPTER_BRAND/tools/build_short_angker.py srt   # SRT dari alignment
```

Aset kerja di `work/sengkon/` (gambar, VO pemilik, alignment, font hasil konversi woff→ttf).

## Menerbitkan

```bash
python3 ODDCHAPTER_BRAND/tools/upload_zernio.py AK-EP01 --send --request ODDCHAPTER_BRAND/11_CONTENT/06_UPLOAD/queue/AK-EP01.json
```

Syarat: `approved` di berkas antrean diubah ke `true` **setelah pemilik menonton**, lalu commit+push.
Setelah tayang, cek "Made for kids" di YouTube Studio (Zernio tidak bisa mengaturnya).

## Kasus berikutnya (sudah siap di Drive, tinggal ganti gambar + shotlist)

`dyatlov-pass` · `krakatau-1883` · `tambora-1815` · `titanic-carpathia` — masing-masing sudah punya
naskah, shotlist, foto arsip, VO (±1:44–2:05), dan `props.json`. Pola yang sama bisa dipakai,
cukup ganti `IMG_FILES`, `SHOT_LIST`, dan overlay di `build_short_angker.py`.
