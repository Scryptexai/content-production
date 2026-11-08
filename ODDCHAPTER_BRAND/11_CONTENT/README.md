# 11_CONTENT — sistem konten 21 hari

Tujuh hari, tiga slot per hari, tiga platform per episode. Semua isi di folder ini
dibangun dari satu file data (`../tools/content_data.py`), jadi script, kalender,
dan thumbnail tidak bisa berbeda satu sama lain.

## Isi

| file | apa |
|---|---|
| `00_STRATEGI.md` | keputusan yang mengikat: POV, struktur script, enam tipe hook, jadwal, gate sumber, standar visual |
| `01_IDEA/21_IDEA_CONTENT.md` | 21 ide + kolom "dugaan → kenyataan" + peta hari |
| `01_IDEA/CONTENT_CALENDAR.csv` | 63 baris: 21 episode × 3 platform, lengkap dengan jam WIB |
| `02_SCRIPT/EP01…EP21_*.md` | satu script per episode: hook, beat per detik, titik balik, loop, cue, sumber, hook A/B |
| `02_SCRIPT/ALL_SCRIPTS.md` | semuanya dalam satu dokumen untuk review cepat |
| `03_THUMBNAIL/*.png` | 21 thumbnail 1080×1920 siap upload |
| `03_THUMBNAIL/*.svg` | versi vektor yang bisa diedit |
| `03_THUMBNAIL/CONTACT_SHEET.png` | semua 21 dalam satu grid |
| `00B_KERANGKA_STORYTELLING.md` | kerangka cerita (Franklin) + rujukan |
| `00C_MESIN_5_EFEK.md` | lima efek yang diminta, mekanismenya, dan gerbangnya |
| `05_VISUAL_PLAN.md` | sistem visual yang benar-benar dirender: 10 bentuk plate, tipografi, ritme segmen, render, QA |
| `10_FILM/remotion/` | kode video: `PlateArt.tsx` (10 bentuk), `Episode.tsx` (satu komposisi untuk 21 episode) |

## Cara memperbarui

```bash
cd ODDCHAPTER_BRAND
python3 tools/build_content_kit.py all       # script + kalender + thumbnail
python3 tools/build_content_kit.py scripts   # hanya dokumen
python3 tools/build_content_kit.py thumbs    # hanya gambar
```

Edit `tools/content_data.py`, bukan file hasil generate. Kalau script diubah,
thumbnail ikut berubah (subline-nya diambil dari kalimat pertama hook).

Video punya jalur sendiri, dan tidak ada teks yang ditulis ulang di kode:

```bash
python3 tools/build_episodes_json.py      # content_data -> src/episodes.generated.json
python3 tools/build_timing.py EP01        # durasi audio nyata + caption pendek -> timing.generated.json
python3 tools/build_sfx.py EP01           # efek suara per segmen -> public/audio/EP01/sfx.wav
cd 10_FILM/remotion
node scripts/still-plates.mjs             # QA 10 bentuk dasar
node scripts/still-ep01.mjs 150 760 1560  # QA frame kunci
node scripts/render-episode.mjs EP01      # master 1080x1920 + loudnorm -14 LUFS
```

## Status

- 21 ide: selesai.
- 21 script: selesai, semuanya `NEEDS-SOURCE`.
- 21 thumbnail: selesai, 1080×1920, kontak sheet tersedia.
- Visual plan: selesai.
- Video: **EP01 selesai** — 58,28 s, 1080×1920, 30 fps, narasi terukur, master di
  `10_FILM/remotion/output/episodes/EP01_1080x1920_master.mp4`.
- Video EP02–EP21: menunggu narasi (9–10 klip per episode); bentuk plate-nya sudah ada.

**`NEEDS-SOURCE` adalah gerbang, bukan label.** Tidak ada episode yang boleh
dirender jadi video final sebelum rujukan primernya dibaca dan statusnya diubah
jadi `VERIFIED`. Peristiwa yang dipakai nyata; yang belum ada di sesi ini adalah
verifikasinya.
