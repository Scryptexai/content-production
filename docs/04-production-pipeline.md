# 04 — Pipeline produksi (Remotion + Blender + FFmpeg)

Satu video pendek = satu berkas JSON. Semua visual dibangkitkan dari data itu,
jadi 35 konten tidak dikerjakan manual satu per satu.

```
content/scripts.json ─┐
                      ├─→ TTS per beat ─┐
asset manifest ───────┘                 ├─→ Remotion (Short.tsx) ─→ MP4 senyap
plate Blender (ops) ────────────────────┘                              │
                                                                       ↓
musik/SFX (python) ──────────────→ FFmpeg loudnorm + mux ─→ assets/video/B01.mp4
```

---

## 1. Struktur data per konten

`content/scripts.json` sudah memuat semuanya. Tambahan yang dibuat saat produksi
(`content/media/B01.json`):

```json
{
  "id": "B01",
  "niche": "beauty",
  "beats": [
    {"vo": "audio/B01-01.mp3", "in": 1.2, "out": 5.4, "text": "Krim yang sama, dua kota, dua hasil."},
    {"vo": "audio/B01-02.mp3", "in": 5.4, "out": 11.0, "text": "Seoul: 55% RH"}
  ],
  "plates": {"bg": "plates/window-cold-loop.mp4", "fg": "images/B01-window.png"},
  "palette": "beauty",
  "poster": 3.4
}
```

`in`/`out` dihitung dari durasi tiap file TTS (ffprobe) + jeda 0,25 s.

---

## 2. Remotion: komposisi `Short`

`projects/tropical-climate/remotion/` dipakai sebagai basis. Tambah:

```tsx
// src/short/Short.tsx  — satu komposisi untuk semua konten
export const Short: React.FC<{data: ShortData}> = ({data}) => (
  <AbsoluteFill style={{backgroundColor: palette(data.palette).bg}}>
    <Plate src={data.plates.bg} />            {/* loop 6 dtk + parallax */}
    <Parallax src={data.plates.fg} depth={0.35} />
    {data.beats.map((b, i) => (
      <Sequence key={i} from={sec(b.in)} durationInFrames={sec(b.out - b.in)}>
        <Beat text={b.text} audio={b.vo} palette={data.palette} index={i} />
      </Sequence>
    ))}
    <Audio src={staticFile(`music/${data.id}.wav`)} volume={0.22} />
  </AbsoluteFill>
);
```

Aturan yang diwarisi dari M1 (jangan diubah):

| Aturan | Nilai |
|---|---|
| fps | 30 |
| ukuran | 1080×1920 |
| easing | `bezier(0.22, 1, 0.36, 1)` |
| hold | ≥ 1 dtk di klaim utama |
| zoom maksimum | 1,15 |
| durasi | 45–75 dtk |
| safe area | 96 px kiri/kanan, 220 px bawah (UI TikTok), 180 px atas |

Render:

```bash
LD_LIBRARY_PATH=/tmp/al2023/lib npx remotion render src/index.ts Short \
  out/B01.mp4 --props=content/media/B01.json --browser-executable=/tmp/chromium \
  --concurrency=2 --muted --crf=20
```

> Kalau render > 900 frame, pecah per 800 frame (`render-chunks.sh`). Dua jebakan
> Chromium/font sudah didokumentasikan di `projects/tropical-climate/chromium-notes.md`.

---

## 3. Blender: plate latar bergerak

Satu scene → 8 varian warna/tema. Resep minimum:

| Plate | Isi | Simulasi | Waktu render |
|---|---|---|---|
| `macro-skin` | tekstur kulit makro + cahaya bergerak | noise + area light | 1–2 mnt |
| `window-cold` | kaca berembun, cahaya dingin | partikel embun | 2–3 mnt |
| `window-tropical` | kaca + daun + cahaya hangat | cloth ringan (daun) | 3–4 mnt |
| `drop` | tetes cairan memantul | fluid (Mantaflow, resolusi rendah) | 15–25 mnt |
| `wax` | petrolatum meleleh | fluid + subsurf | 20–40 mnt |
| `heat` | gelombang panas di kabin | noise displacement | 1–2 mnt |
| `sun` | debu di sorotan cahaya | volumetrik + partikel | 2–3 mnt |
| `bottle` | kaca + pantulan bergerak | HDRI berputar | 2–3 mnt |

```bash
blender -b plates/macro-skin.blend -E BLENDER_EEVEE_NEXT \
  -o /tmp/p_#### -F PNG -x 1 -a
ffmpeg -y -framerate 30 -i /tmp/p_%04d.png -t 6 \
  -vf "scale=1080:1920:flags=lanczos,gblur=sigma=1.2" \
  -c:v libx264 -crf 18 -pix_fmt yuv420p assets/plates/macro-skin-loop.mp4
```

Aturan plate: **blur 1–3 px**, tanpa objek tajam, tanpa teks, kontras rendah
(≤ 20% di area teks). Simpan ≤ 5 MB/file; `assets/plates/*.mp4` boleh masuk git
kalau totalnya < 40 MB, kalau lebih → Drive.

---

## 4. Audio

Musik: pakai `projects/tropical-climate/audio_build.py` sebagai basis (akor per
seri, sub pulse, whoosh di transisi). Untuk 35 video pendek:

```bash
# 1. narasi per beat (TTS) → audio/B01-01.mp3 …
# 2. gabung + musik + ducking, target -16 LUFS / -1.5 dBTP
ffmpeg -y -i voice.wav -i music.wav -filter_complex \
 "[1:a]volume=0.6,highpass=f=55,lowpass=f=9000[m];\
  [m][0:a]sidechaincompress=threshold=0.045:ratio=7:attack=18:release=340[duck];\
  [0:a][duck]amix=inputs=2:duration=first:normalize=0,\
  loudnorm=I=-16:TP=-1.5:LRA=11[a]" -map "[a]" -ar 48000 -ac 2 mix.wav
# 3. mux
ffmpeg -y -i out/B01.mp4 -i mix.wav -map 0:v -map 1:a \
  -c:v libx264 -crf 19 -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 \
  -color_trc bt709 -color_range tv -c:a aac -b:a 192k -shortest \
  -movflags +faststart assets/video/B01.mp4
```

Target akhir: **−16 LUFS, true peak ≤ −1,5 dBFS**, audio 48 kHz stereo.

---

## 5. QC sebelum tayang (checklist 8 poin)

- [ ] durasi 45–75 dtk, 1080×1920, 30 fps
- [ ] teks tidak masuk area UI platform (safe area di §2)
- [ ] loudness −16 ±1 LUFS, tidak clipping
- [ ] klaim di VO ada di `source` pada `scripts.json`
- [ ] caption platform tidak terpotong (TikTok ≤ 2.200, IG ≤ 2.200)
- [ ] poster dipilih dari frame dengan teks terbanyak
- [ ] label AI & disclosure ada di deskripsi
- [ ] nama file `B01.mp4` sesuai `calendar.json`

---

## 6. Kapasitas & waktu

| Tahap | Per video | 35 video |
|---|---|---|
| Naskah | sudah selesai (M2) | — |
| TTS (5 beat) | 40 dtk | 25 mnt |
| Aset/plate | 0 (pakai ulang 8 plate) | — |
| Render Remotion | 60–120 dtk | 45–70 mnt |
| Audio + mux | 30 dtk | 20 mnt |
| **Total** | **±3 mnt** | **±1,5–2 jam** |

Dengan 2 vCPU, 35 video ≈ 2 jam render + 1 jam QC. Itu sebabnya produksi
dilakukan **batch per hari** (5 video), bukan menunggu semua selesai.

---

## 7. Pipeline nyata yang dipakai: Knot Theory (`projects/knot-theory/`)

Bagian 1–6 di atas adalah rencana M2. Yang benar-benar dijalankan untuk kanal
Knot Theory ada di `projects/knot-theory/` dan berbeda di beberapa titik penting:

| Rencana §1–6 | Yang dipakai | Alasan |
|---|---|---|
| plate Blender | `plates/make_plate.py` (numpy + ffmpeg) | Blender tidak tersedia di mesin render; plate tetap bergerak 3 lapis |
| aset gambar AI | tidak dipakai | aturan kanal: tanpa wajah, tanpa stok foto |
| TTS per beat | TTS per beat (sama) | — |
| musik dari `audio_build.py` | `make_music.py` (4 varian, disintesis) | tidak butuh file sampel, bebas lisensi |
| `Short.tsx` generik | `remotion/src/Short.tsx` — komposisi `KnotShort` | tipe beat: hook/statement/number/pair/note/close |
| ffprobe | `ffmpeg -i` + regex | ffprobe tidak tersedia di image ini |

### Angka terukur (2 vCPU, 1080×1920, 30 fps)

| Tahap | Waktu |
|---|---|
| plate 12 dtk, satu varian | 25 dtk |
| musik 4 varian × 130 dtk | 10 dtk |
| Remotion render 106 dtk | **±13 mnt** (±0,2 dtk/frame) |
| mix + loudnorm + QC | 40 dtk |

Konsekuensi: 21 video (7 topik × 3 platform) ≈ 5 jam render. Render dijalankan
sebagai proses latar, bukan di dalam satu perintah tunggal.

### QC yang dijalankan `render.py`

durasi ≥ 40 dtk · resolusi tepat 1080×1920 · loudness −16 LUFS ±1,5 ·
true peak ≤ −1,5 dBTP

Panduan lengkap: `projects/knot-theory/README.md`.
