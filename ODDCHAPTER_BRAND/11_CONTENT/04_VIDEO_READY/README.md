# video ready — isi folder ini

Master siap upload ke TikTok / YouTube Shorts / Facebook Reels.
1080×1920 · H.264 (yuv420p, tv range) · 30 fps · AAC 48 kHz stereo · −14 LUFS (EP05: −14,8 LUFS, −1,2 dBTP).

File binernya **tidak** disimpan di Git (folder `10_FILM/remotion/output/` di-ignore,
supaya repo tidak membengkak 20 MB per episode). Yang tersimpan: sumber, naskah,
dan indeks ini. Salinan yang bisa ditonton ada di Drive → folder `video ready`.

## Daftar master

| episode | judul | durasi | ukuran | Drive file id | file lokal |
|---|---|---|---|---|---|
| EP01 v7 | TIGA PENJAGA DAN SATU SET PAKAIAN YANG TERTINGGAL | 64,85 s | 17,9 MB | `18u4GwSOAMVIsCtnPIGBAjvc-Axy-Nrur` | `10_FILM/remotion/output/episodes/EP01_1080x1920_master.mp4` |
| EP02 | MEREKA MEMOTONG TENDA ITU DARI DALAM | 72,32 s | 21,1 MB | `1WF4yQQkg02pctkJ8QsX-xls37gQCvoyJ` | `10_FILM/remotion/output/episodes/EP02_1080x1920_master.mp4` |
| EP03 | KAPAL YANG MASIH BISA BERLAYAR, AWAK YANG MENINGGALKANNYA | 71,80 s | 21,9 MB | `1chsdzAkdplfm3JdmBHOefj5MQP_khUiZ` | `10_FILM/remotion/output/episodes/EP03_1080x1920_master.mp4` |
| EP04 | MEREKA BERJALAN MENJAUH DARI PERTOLONGAN (JALAN KE ATAS) | 70,81 s | 17,3 MB | `1O2onobslZxZo5miA83s6d5cEHcfK1OGL` | `10_FILM/remotion/output/episodes/EP04_1080x1920_master.mp4` |
| EP05 | MEREKA MENULIS SATU KATA, BUKAN SEBUAH PERINGATAN (ROANOKE) | 68,84 s | 17,6 MB | `1ls-1EVOdp-2L81QvNpyi6QjzqmNHDdJY` | `10_FILM/remotion/output/episodes/EP05_1080x1920_master.mp4` |
| EP06 | API DI BAWAH KOTA YANG TIDAK PERNAH DIPADAMKAN (CENTRALIA) | 57,92 s | 16,7 MB | `1NHnFpmKd2YsTPEhzuORBkQj4b4xAn-n4` | `10_FILM/remotion/output/episodes/EP06_1080x1920_master.mp4` |

Buka Drive: `https://drive.google.com/file/d/<file id>/view`
Unduh langsung: `https://drive.google.com/uc?id=<file id>&export=download`

Master lama (v3–v6) sudah di-trash supaya tidak ada dua file dengan nama sama.

## Cara membuat ulang satu master

```
cd ODDCHAPTER_BRAND
python3 tools/build_timing.py EP03      # durasi nyata tiap segmen
python3 tools/build_bed.py EP03         # angin + drone + dentuman di titik balik
python3 tools/build_sfx.py EP03         # efek per segmen
python3 tools/build_episodes_json.py    # teks + daftar foto ke Remotion
cd 10_FILM/remotion
node scripts/still-episode.mjs EP03     # QA frame sebelum encode
node scripts/render-episode.mjs EP03    # render + loudnorm → *_master.mp4
```

Encode akhir (kalau mau dari `_raw.mp4` dengan CRF sendiri):

```
ffmpeg -i EP03_raw.mp4 \
  -vf "scale=in_range=full:out_range=tv,format=yuv420p" \
  -af "loudnorm=I=-14:TP=-1.5:LRA=11" \
  -c:v libx264 -preset slow -crf 21 -maxrate 6M -bufsize 12M \
  -pix_fmt yuv420p -c:a aac -b:a 160k -ar 48000 -movflags +faststart \
  EP03_1080x1920_master.mp4
```

## Isi lain di folder ini

`REFERENSI_standar_visual_ODDCHAPTER_PILOT_001_captions_1080x1920.mp4` — pilot fase
sebelumnya. Bukan salah satu dari 21 episode; patokan mutu minimum (gerak,
tipografi, caption, warna).

## Konvensi nama

```
EP01_1080x1920_master.mp4        ← satu file per episode, selalu nama ini
EP01_raw.mp4                     ← render mentah 8 Mbps, bahan encode ulang
```

Satu nama per episode, tanpa nomor versi di nama file: versi dicatat di tabel di
atas dan di commit Git, supaya Drive tidak pernah punya dua "EP01".

## Catatan EP04 — aset kerja yang sempat masuk Git

Plate (12 JPEG) dan potongan narasi (13 MP3) EP04 di-commit sementara ke repo
saat produksi, lalu dicabut lagi setelah master jadi. Alasannya teknis, bukan
perubahan konvensi: di sandbox tempat EP04 dibuat, berkas yang masuk
`.gitignore` tidak bertahan antar-sesi, sementara kuota generator gambar dan
suara (10 per giliran) tidak cukup untuk menghasilkan ulang 12 gambar + 13 klip
setiap sesi. Setelah `EP04_1080x1920_master.mp4` ada di Drive, keduanya tidak
lagi dibutuhkan di Git — `.gitignore` berlaku seperti sebelumnya.

Yang tetap tersimpan di repo: naskah, data episode (`tools/content_data.py`),
thumbnail 1080x1920, metadata unggah, dan indeks ini. Master ada di Drive.
