# Knot Theory — produksi video

Pipeline video pendek untuk kanal Knot Theory: 1080×1920, 30 fps, tanpa wajah,
latar bergerak, narasi suara + tipografi.

```
shots/<ID>.json ──┐
                  ├─ TTS per beat ──→ public/audio/<ID>-<beat>.mp3
plate bergerak ───┤
musik sintesis ───┘
                  ↓
        build_timing.py  → src/shots.ts (from/to tiap beat dari durasi audio)
                  ↓
        remotion render  → out/<ID>-silent.mp4 (VO sudah di dalamnya)
                  ↓
        ffmpeg: musik + ducking + loudnorm −16 LUFS
                  ↓
        out/<ID>.mp4  → QC durasi/resolusi/loudness
```

---

## Menjalankan

```bash
# sekali per mesin
npm install --prefix remotion
pip install --break-system-packages pillow numpy imageio-ffmpeg

# aset yang dibangkitkan (tidak masuk git)
python3 plates/make_plate.py --ffmpeg "$(python3 -c 'import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())')"
python3 make_music.py --sec 130

# cek timing tanpa render
python3 render.py RW1 --dry

# render satu video
python3 render.py RW1

# render semua naskah yang sudah punya audio
python3 render.py --all
```

Berkas yang dihasilkan: `out/<ID>.mp4`, `out/<ID>-silent.mp4`,
`out/<ID>-props.json`, `remotion/src/shots.ts`.

---

## Struktur berkas

| Berkas | Isi |
|---|---|
| `shots/<ID>.json` | naskah per beat: `kind`, teks VO, teks layar, sumber |
| `remotion/src/Short.tsx` | komposisi `KnotShort` — plate, slide, identitas, progress |
| `remotion/src/fonts.ts` | pemuat font yang menahan render sampai siap |
| `remotion/src/palette.ts` | warna brand |
| `plates/make_plate.py` | plate 12 dtk: simpul berputar + bloom + grain |
| `make_music.py` | musik sintesis (drone + pad + pulse + tekstur), 4 varian |
| `build_timing.py` | JSON + durasi audio → `shots.ts` |
| `render.py` | render, mix, QC |

---

## Tipe beat

| `kind` | Tampilan |
|---|---|
| `hook` | serif besar, satu klaim, boleh ada `screen[0]` kecil |
| `statement` | serif sedang + satu baris layar |
| `number` | **angka raksasa mono** + kalimat penjelas (warna rose) |
| `pair` | dua angka/dua istilah bertumpuk (warna sage) |
| `note` | catatan metodologis, teks layar lilac |
| `close` | pertanyaan penutup, tanpa teks layar |

Aturan dari editorial bible yang ditegakkan di komposisi:

- safe area: 96 px kiri/kanan, 180 px atas, 320 px bawah (UI TikTok)
- satu angka besar per adegan, hold ≥ 1 dtk setelah fade masuk
- easing `bezier(0.22, 1, 0.36, 1)`, fade 14 frame, geser 26 px
- tidak ada wajah, tangan, atau stok foto manusia

---

## Latar bergerak

`make_plate.py` membuat loop 12 dtk dengan tiga lapis gerak:

1. **simpul trefoil raksasa** berputar 24° + melayang (gerak yang terlihat)
2. dua bloom cahaya bernapas dengan fase berbeda
3. grain yang berubah tiap frame

Empat varian warna: `ink`, `rose`, `sage`, `lilac`. Plate disimpan 540×960
lalu di-upscale — memang lembut, dan itu disengaja: latar tidak boleh bersaing
dengan teks. Kontras dijaga ≤ 20% di area teks.

---

## Biaya waktu (terukur di mesin 2 vCPU)

| Tahap | Waktu |
|---|---|
| Render plate (satu varian, 12 dtk) | 25 dtk |
| Musik (4 varian, 130 dtk) | 10 dtk |
| Remotion render 106 dtk video | **±13 mnt** |
| Mix audio + QC | 40 dtk |

Render adalah bottleneck: ±0,2 dtk per frame di 1080×1920. Untuk 21 video
perlu ±5 jam render. Karena itu:

- render dijalankan sebagai proses latar, satu batch per malam
- naskah dipecah per `shots/*.json` supaya bisa lanjut walau satu video gagal
- kalau butuh lebih cepat: turunkan ke 810×1440 lalu upscale (teks sedikit
  lebih lembut), atau potong durasi naskah, jangan turunkan fps

---

## QC otomatis

`render.py` memeriksa tiap video:

- durasi ≥ 40 dtk (short yang lebih pendek dari itu berarti naskahnya terpotong)
- resolusi tepat 1080 × 1920
- loudness −16 LUFS ±1,5 dan true peak ≤ −1,5 dBTP

Yang tidak diperiksa mesin dan tetap harus dilihat manusia: apakah teks
terbaca di layar HP, apakah angka di layar cocok dengan fact ledger, dan apakah
kalimat terakhir benar-benar pertanyaan.

---

## Catatan mesin

Chromium dari `@sparticuz/chromium` perlu pustaka AL2023:

```bash
python3 -c "
import brotli, tarfile, io, pathlib
p = pathlib.Path('remotion/node_modules/@sparticuz/chromium/bin/al2023.tar.br')
tarfile.open(fileobj=io.BytesIO(brotli.decompress(p.read_bytes()))).extractall('/tmp/al2023')"

export LD_LIBRARY_PATH=/tmp/al2023/lib
node -e "require('@sparticuz/chromium').default.executablePath().then(console.log)"  # → /tmp/chromium
```

Tanpa `LD_LIBRARY_PATH`, Chromium gagal start dan Remotion berhenti dengan
"browser executable not found" — bukan masalah Remotion.

## Video panjang (benchmark)

Satu video 3–4 menit 16:9, dipakai sebagai patokan video berikutnya.

```bash
FF=$(python3 -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())")
python3 make_backdrop_assets.py                      # knot-mark, bloom, grain
python3 make_backdrop_loop.py --ffmpeg "$FF"          # backdrop/loop-<tone>.mp4 + -long.mp4
python3 build_long.py RW1-long --ffmpeg "$FF"         # timing dari durasi audio nyata
python3 make_music.py --sec 230 --ffmpeg "$FF"        # bed musik (di-gitignore)

cd remotion
export LD_LIBRARY_PATH=/tmp/al2023/lib
npx remotion render src/index.ts KTL-benchmark out/RW1L-silent.mp4 \
  --browser-executable=/tmp/chromium --concurrency=2 --crf=19 --log=error
cd ..
python3 mix.py --video remotion/out/RW1L-silent.mp4 \
  --music remotion/public/music/ink.mp3 --out out/RW1L.mp4 --ffmpeg "$FF"
```

Catatan teknis (jangan diulang):

- Latar **tidak** digambar sebagai lapisan gambar ber-animasi di Remotion —
  itu 1,6 dtk/frame. Latar dibakar jadi video oleh `make_backdrop_loop.py`
  (0,2–0,4 dtk/frame).
- `<OffthreadVideo loop>` di versi ini **membeku di frame pertama**
  (selisih antar frame 0,000). Karena itu berkasnya diulang jadi
  `loop-<tone>-long.mp4` dan diputar lurus tanpa `loop`.
- Simpul di latar harus kecil dan di kanan. Versi besar-di-tengah membuat teks
  tenggelam dan tidak terbaca di ponsel.
