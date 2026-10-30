# Remotion — Kulit Tropis, Formula Subtropis

Migrasi renderer dari Pillow/`render.py` ke **Remotion 4**. Semua visual sekarang
digambar sebagai DOM/SVG di Chromium (vektor, teks digambar ulang sesuai ukuran
akhir), bukan lagi rasterisasi Pillow yang lalu di-crop.

Hasil akhir: `1080 × 1920`, 30 fps, **5.906 frame (3:16,97)**, h264 + AAC 192 kbps.

---

## Struktur

```
src/
  index.ts              registerRoot(RemotionRoot)
  Root.tsx              TropicalFilm · TropicalScenes · S01…S10 (QA per adegan)
  film/
    fonts.ts            @remotion/fonts → DM Serif Display, Inter, IBM Plex Mono
    atoms.tsx           palet, easing, Bg (Ken Burns), Scrim, Band, Words, Num, Rule, Kicker
    scenes.tsx          S01…S10 + kit diagram (Arrow, Panel, curve, gauge)
    Bumper.tsx          kartu judul 152 frame (5,07 dtk)
    Film.tsx            timeline: bumper + 10 adegan, <Audio> VO per adegan
public/
  images/01…08-*.jpg    8 still latar (sama dengan versi Pillow)
  audio/vo-01…10.mp3    narasi
  fonts/*.woff2         7 file latin
```

Urutan adegan & durasi (frame @30 fps) — **identik** dengan `render.py` supaya
`build/mix.wav` tetap sinkron:

| # | Adegan | Frame | Detik |
|---|--------|------:|------:|
| — | Bumper | 152 | 5,07 |
| 01 | cold open 12 °C → Jakarta | 463 | 15,43 |
| 02 | tiga statistik iklim | 431 | 14,37 |
| 03 | "bukan detail kecil" | 323 | 10,77 |
| 04 | humektan | 386 | 12,87 |
| 05 | lembap vs kering | 602 | 20,07 |
| 06 | oklusif | 751 | 25,03 |
| 07 | panas ×2 + zona IVb | 895 | 29,83 |
| 08 | UV gauge | 616 | 20,53 |
| 09 | tiga perubahan | 933 | 31,10 |
| 10 | penutup | 357 | 11,90 |

---

## Menjalankan

### 1. Dependensi

```bash
npm install
```

### 2. Chromium (lingkungan tanpa browser sistem)

Chromium diambil dari paket `@sparticuz/chromium` (bukan download Playwright).
Butuh `brotli` untuk membuka arsip AL2023:

```bash
python3 -c "
import brotli
d=brotli.decompress(open('node_modules/@sparticuz/chromium/bin/al2023.tar.br','rb').read())
open('/tmp/al2023.tar','wb').write(d)"
mkdir -p /tmp/al2023 && tar -xf /tmp/al2023.tar -C /tmp/al2023
python3 -c "
import brotli
d=brotli.decompress(open('node_modules/@sparticuz/chromium/bin/chromium.br','rb').read())
open('/tmp/chromium','wb').write(d)"
chmod +x /tmp/chromium && LD_LIBRARY_PATH=/tmp/al2023/lib /tmp/chromium --version
```

### 3. Studio (pratinjau interaktif)

```bash
LD_LIBRARY_PATH=/tmp/al2023/lib npx remotion studio src/index.ts --browser-executable=/tmp/chromium
```

### 4. Render

```bash
LD_LIBRARY_PATH=/tmp/al2023/lib npx remotion render src/index.ts TropicalFilm \
  out/film-silent.mp4 --browser-executable=/tmp/chromium --concurrency=2 \
  --muted --codec=h264 --crf=20 --x264-preset=medium
```

`--concurrency` **maksimal 2** di mesin 2 vCPU; lebih dari itu Chromium kehabisan
memori. `--muted` dipakai karena audio final dicampur di langkah berikut.

### 5. Audio + mux

Musik dan SFX tetap disintesis oleh `../audio_build.py` (tidak ada aset
pihak ketiga), lalu dicampur dengan narasi + ducking + `loudnorm I=-16`.

```bash
python3 ../audio_build.py            # → ../build/mix.wav (191,39 s = 10 adegan)

# geser 5,067 dtk agar audio mulai setelah bumper
ffmpeg -y -i ../build/mix.wav -af "adelay=5067|5067,apad" -t 196.97 \
  -ar 48000 -ac 2 -c:a aac -b:a 192k out/audio-final.m4a

ffmpeg -y -i out/film-silent.mp4 -i out/audio-final.m4a \
  -map 0:v -map 1:a -c:v copy -c:a copy -shortest \
  -movflags +faststart out/tropical-remotion-COMPLETE.mp4
```

---

## Catatan teknis

- **Semua `<Composition>` di satu `Root`.** `registerRoot` tidak boleh menerima
  Fragment — bundling esbuild akan gagal dengan `Unexpected ">"`.
- Font dimuat lewat `@remotion/fonts` sehingga Remotion menahan frame sampai
  glyph siap (tidak ada FOUT di frame 0).
- `Bg` memakai `Img` + `transform: scale/translate` linear per frame — gerakan
  Ken Burns halus, bukan potongan crop per frame seperti Pillow.
- Teks tidak pernah diperkecil sebagai gambar: `Words` menggambar per kata
  dengan easing `bezier(0.22, 1, 0.36, 1)`.
- Durasi dihitung dari `lead + VO + tail`, dibulatkan ke frame. Kalau salah satu
  VO diganti, `SCENE_FRAMES` di `src/film/Film.tsx` dan `SCENES` di
  `audio_build.py` harus diperbarui bersamaan.
- `out/` di-`.gitignore`: hasil render besar diunggah ke Drive, bukan ke git.
