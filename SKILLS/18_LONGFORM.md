# 18 · Long-form: VO pemilik + timestamp pemilik

Dibuat 16–17 Nov 2026 untuk seri baru ("SERIES BARU — ODDCHAPTER", EP01
Illuminati, 05:18). Pemilik mengirim satu berkas VO, transkrip bertimestamp,
musik latar, dan satu efek suara. Tidak ada TTS di jalur ini.

## Kontrak

| pihak | memberi | tidak boleh |
|---|---|---|
| pemilik | VO final, timestamp, musik, sfx, rekomendasi visual | — |
| produksi | potongan gambar, caption, campuran audio, master 9:16 | menulis ulang narasi, menggeser timestamp, menambah kalimat |

Naskah **tidak** ditulis ulang. Kalau transkrip bilang "lo/gue", layar juga
"lo/gue". Kalau ada kalimat yang salah, itu keputusan pemilik — bukan editor.

## Tiga berkas, satu alur

```
02_SCRIPT/LONGFORM/EPxx_*.json     naskah + batas waktu + plate + bab
        │  tools/build_longform.py
        ├─→ src/longform.generated.json       (dibaca LongForm.tsx)
        └─→ public/audio/EPxxLF/mix.wav       (VO + musik ducked + sfx)
                    │  scripts/render-longform.mjs
                    └─→ output/episodes/EPxx_*_1080x1920_master.mp4
```

`build_longform.py` gagal keras kalau: segmen tidak mulai di 0 · ada celah
> 0,3 dtk antar segmen · segmen terakhir tidak berakhir di durasi VO · ada
segmen tanpa plate atau tanpa caption.

## Campuran audio (urutan prioritas: VO → efek → musik)

```
VO     loudnorm I=-16 TP=-1.5 → −2 dB
musik  −18 dB + sidechaincompress (threshold 0,03 · ratio 12 · release 420 ms)
sfx    +12 dB di penanda pemilik saja (bukan tiap potongan)
mix    alimiter 0,85 → −1 dB      (hasil EP01: −16,8 LUFS · peak −1,0)
master loudnorm I=-14 TP=-1.5
```

VO pemilik sering jauh lebih pelan dari musiknya (EP01: VO −25,2 LUFS vs musik
−13,9 LUFS). Jangan menaikkan VO dengan `volume` mentah — pakai `loudnorm`,
lalu ducking musik. Tanpa dua langkah itu, musik menang.

## Tampilan

- **Plate `cover`**: foto penuh layar, zoom 1,03→1,11 sepanjang potongan.
- **Plate `contain`**: engraving/peta/sampul buku sebagai "kartu arsip" dengan
  label `ARSIP` — jangan dipotong paksa jadi 9:16, hasilnya merusak gambar.
- Bab masuk di awal segmen (2,6 dtk), caption = potongan transkrip (≤ 9 kata),
  waktu dibagi menurut panjang karakter di dalam segmen.
- Kedip 3 frame tiap ganti plate; grain PNG 256px digeser, **bukan** gradient
  yang diraster ulang (itu yang menjatuhkan laju render ke 0,04x).

## Pelajaran render (mahal, jangan diulang)

| salah | akibat | benar |
|---|---|---|
| `imageFormat: "png"` | 3,5 MB/menit ≈ 2 jam untuk 5 menit video | `jpeg` q92 ≈ 2x lebih cepat |
| `concurrency: 4` | Remotion menolak: mesin ini 2 core | `concurrency: 2` |
| `repeat-conic-gradient` grain | raster ulang tiap frame | tile PNG + `transform` |
| `boxShadow: inset 240px` | blur besar per frame | `radial-gradient` statis |
| `filter: saturate/contrast` di `<Img>` | filter per frame | grade plate di Python |
| JPEG tanpa koreksi range | warna keluar `yuvj420p` (full-range) | encode ulang `scale=in_range=full:out_range=tv,format=yuv420p` |

Laju akhir: ±3,5 frame/detik (2 core) → 5 menit video ≈ 45 menit render +
±10 menit encode akhir.

## Daftar periksa sebelum unggah

1. `ffprobe` master: 1080×1920 · 30 fps · `yuv420p` · durasi = durasi VO.
2. `ebur128`: I ≈ −14 LUFS · TP ≤ −1,0 dBFS.
3. Tiga stillframe: hook, satu kartu arsip, satu segmen tengah — caption tidak
   menabrak plate, tidak ada kotak putih, tidak ada teks terpotong.
4. Unggah ke Drive `video ready` hari itu juga, catat di `MASTER_UPLOAD.md`.
