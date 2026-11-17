# MASTER UPLOAD — daftar serah-terima video jadi

**Aturan (berlaku sejak 15 Nov 2026, atas permintaan pemilik):**
setiap video yang **selesai di-build wajib langsung diunggah ke Drive**, di sesi
yang sama dengan render-nya. Render yang belum ada di Drive dianggap belum jadi.

- Folder Drive: **`video ready`** — `1fVoOvZgiYB3V7S2C5LfMrCpo-c4Xxzo2`
- Nama berkas: `EPxx_1080x1920_master.mp4` (satu nama per episode; versi dicatat di sini)
- Render yang digantikan **diganti nama**, bukan dihapus: `..._v1-<alasan>.mp4`
- Setiap baris di tabel ini harus punya id Drive yang benar-benar ada.

Periksa kapan saja:

```
python3 tools/check_master_upload.py
```

Skrip itu membandingkan `10_FILM/remotion/output/episodes/*.mp4` dengan tabel ini
dan berhenti dengan status ≠ 0 kalau ada master lokal yang belum tercatat.

---

## Master aktif

| ep | versi | durasi | ukuran | diunggah | Drive file id |
|---|---|---|---|---|---|
| EP01 | v7 | 64,85 s | 17,9 MB | 8 Nov 2026 | `18u4GwSOAMVIsCtnPIGBAjvc-Axy-Nrur` |
| EP02 | v1 | 72,32 s | 21,1 MB | 8 Nov 2026 | `1WF4yQQkg02pctkJ8QsX-xls37gQCvoyJ` |
| EP03 | v1 | 71,80 s | 21,9 MB | 8 Nov 2026 | `1chsdzAkdplfm3JdmBHOefj5MQP_khUiZ` |
| EP04 | v1 | 70,81 s | 17,3 MB | 11 Nov 2026 | `1O2onobslZxZo5miA83s6d5cEHcfK1OGL` |
| EP05 | v1 | 68,84 s | 17,6 MB | 13 Nov 2026 | `1ls-1EVOdp-2L81QvNpyi6QjzqmNHDdJY` |
| EP06 | v2 | 54,38 s | 16,0 MB | 14 Nov 2026 | `1O4HvhK22QLjxXuLkhOzngAH-WS_jGLtH` |
| EP07 | v1 | 48,28 s | 14,1 MB | 14 Nov 2026 | `1OrIaFbZKj_yufo-HOSpVCYxnhmUHYKc8` |
| EP08 | v2 | 53,50 s | 15,3 MB | 14 Nov 2026 | `131CrG69yCLrczrTygjYbTV5Hs-TxIDRl` |
| EP09 | **v4 — VO buatan user + cover benar** | 53,78 s | 32,9 MB | 16 Nov 2026 | `1leWLFt4QuLEgXMSmnemYAXRWlMr9vUCT` |
| EP10 | **v1 — VO buatan user, 9 foto segmen** | 59,90 s | 60,0 MB | 15 Nov 2026 | `1YfNXyS4qKM39zybT7LLpMkpq3JS7ibdX` |
| EP11 | **v4 — topik diganti ke Valentich (T02), naskah ditulis dari tabel fakta riset; `voice-04`** | 53,33 s | 13,2 MB | 16 Nov 2026 | `1sOzdlwY34aI1beOz4UqnRl8SYMtKX6dz` |

### Seri baru — long-form (VO + timestamp + musik dari pemilik)

| ep | versi | durasi | ukuran | diunggah | Drive file id |
|---|---|---|---|---|---|
| SB-EP01 | **v1 — ILLUMINATI: ORGANISASI ATAU INTERPRETASI?** (17 blok timestamp pemilik, 4 plate arsip domain publik) | 318,14 s | 81,6 MB | 17 Nov 2026 | `1eNMpdk-cvMFIG-LI5nEW2_caVXO0D6qd` |

## Arsip (digantikan, tetap ada di Drive)

| ep | nama berkas | alasan | Drive file id |
|---|---|---|---|
| EP09 | `EP09_1080x1920_master_v3-intro-lama.mp4` | VO user sudah benar, tetapi 0,5 dtk pertama masih cover Somerton Man | `1ZMikYIar_HDYmS8wY5-wGbBDdM9DTnOL` |
| EP09 | `EP09_1080x1920_master_v2-vo-lama.mp4` | render 15 Nov: audio dari naskah lama (Somerton Man), bukan VO user | `1SmFv67IVaoCxC7Ow1SCid4Pk6wtbkLBl` |
| EP09 | `EP09_1080x1920_master_v1-plate.mp4` | render lama, seluruh episode cuma satu plate vektor statis (bukan foto per segmen) | `1hfB9nq-fScY1dJtA5_NCMYjoUH4r7lsi` |
| EP08 | `EP08_1080x1920_master.mp4` | versi sebelum v2 | `10rTpHzuEnQkfXNiC8dWuVAU23TQv-oD6` |
| EP08 | `EP08_1080x1920_master_v4.mp4` | percobaan v4 | `1_aFdKTXtaT1ycHe2IbCHhOawUNoS3CQx` |
| EP08 | `EP08_1080x1920_master_v5_internal.mp4` | uji internal | `1UrKOv6JgRJOzh1D5LOjuJ58mAHp1MJtm` |
| EP06 | `EP06_1080x1920_master.mp4` | versi sebelum v2 | `1NHnFpmKd2YsTPEhzuORBkQj4b4xAn-n4` |
| EP11 | `EP11_1080x1920_master_v1-ambigu.mp4` | naskah v1: 8 dari 10 kalimat ambigu ("tanah keluar dari dalam tanah", "tanah berguncang") | `1nU4-Ce_g7555Dau1KOKXZ9P-CLiroFzv` |
| EP11 | `EP11_1080x1920_master_v2-porong.mp4` | topik Porong ditolak pemilik ("topik nya kurang menarik itu masalah nya"); naskahnya sudah bersih dari kalimat ambigu, tetapi ditayangkan sebagai pengganti sementara | `1zZ5imWXaZWqGFigD2VzQyN28VqBf-kW-` |

## Catatan aset kerja EP09

Foto per segmen EP09 (`public/plates/EP09/`) tidak disimpan di Git — folder
`public/` di-ignore. Master final ada di Drive (`1leWLFt4QuLEgXMSmnemYAXRWlMr9vUCT`),
jadi tidak ada yang hilang dari hasil tayang. Kalau EP09 perlu dirender ulang,
9 foto per segmen harus dibuat lagi dulu; suara, timing, bed, sfx, dan cover
sudah ada di repo.

## Catatan aset kerja EP10

Master EP10 (`1YfNXyS4qKM39zybT7LLpMkpq3JS7ibdX`, 59.953.240 B, sha256
`d04f269e…c8d2d`) memakai VO buatan pemilik (`1x15AvOEZSd4LhXOd6eId2x8-DxIUfrT6`,
59,01 dtk, satu trek) dan 9 foto AI segmen baru (`public/plates/EP10/`, tidak di Git
karena `public/` di-ignore). Timing: `TIMESTAMP EP10.txt` → 9 cue, batas disnap ke
jeda hening nyata. 1797 frame, −14,7 LUFS, TP −1,4 dB. Tayang 15 Nov 2026
14:43 UTC (YouTube) dan 14:46 UTC (TikTok).

## Belum di-build (belum ada master)

EP11–EP21. Untuk tiap episode: VO pemilik dari Drive dulu (bukan TTS), lalu
`content_data.py` (cue 9 segmen), foto 9 segmen, cover, render, unggah Drive,
antrean YouTube + TikTok. Pola EP09 dan EP10 bisa dipakai apa adanya.

## Catatan aset kerja EP11

Master EP11 v4 (`1sOzdlwY34aI1beOz4UqnRl8SYMtKX6dz`, 13.221.601 B, sha256
`0a66e113…0f6136eb`, 53,333 s, -14,1 LUFS, TP -1,5) dibangun 16 Nov 2026 di
sandbox: **topik diganti** dari Porong ke hilangnya Frederick Valentich (kartu
T02), naskah ditulis ulang dari tabel fakta `02_SCRIPT/riset/EP11_valentich.md`
(setiap baris VO memuat minimal satu fakta berlabel F##), VO internal
`voice-04` (perintah pemilik: pakai VO EP05/EP06 — VO pemilik belum turun),
9 segmen mp3 di `public/audio/EP11/`, bed + sfx dari `build_bed.py`/
`build_sfx.py`, 9 foto segmen di `public/plates/EP11/`. Folder `public/`
di-ignore, jadi foto dan mp3 **tidak** masuk Git — kalau harus dirender ulang,
VO bisa dibuat lagi dengan `voice-04` dari `content_data.py` (teks identik),
foto harus dibuat lagi.

Status tayang: **menunggu persetujuan pemilik** (naskah ditunjukkan dulu).
Master v2 Porong tetap yang terakhir disetujui untuk tayang sampai v4 disetujui.


## Catatan aset kerja SB-EP01 (long-form Illuminati)

Master `1eNMpdk-cvMFIG-LI5nEW2_caVXO0D6qd` (81.584.277 B, 318,144 s, −13,9 LUFS,
TP −1,4, sha256 `42c1816f…edcc0411d`) dibangun 17 Nov 2026 dari bahan pemilik di
Drive `SERIES BARU — ODDCHAPTER / EP01 — ILLUMINATI PERNAH ADA`:
VO 05:18, `Timestamp-full.txt` (17 blok), musik latar, satu sfx, dan dokumen
rekomendasi visual. Naskah **tidak** ditulis ulang — potongan gambar mengikuti
timestamp pemilik (`tools/build_longform.py`), caption adalah potongan transkrip.
Audio: VO loudnorm −16, musik −18 dB + ducking sidechain, sfx di 0:00 · 1:58 ·
4:10 · 5:13, master −14 LUFS. Plate: 9 ilustrasi (generate) + 4 arsip domain
publik (Weishaupt, Ingolstadt/Hollar 1638, Barruel, Nachtrag) bertanda `ARSIP`.

Cara membangun ulang ada di `SKILLS/18_LONGFORM.md` dan
`02_SCRIPT/LONGFORM/EP01_illuminati.md`. `public/` di-ignore Git: plate, mix, dan
VO tidak masuk repo; VO/musik/sfx asli tetap di Drive pemilik.

Catatan yang belum ditutup di v1: label bab di atas layar memakai sage 75% tanpa
scrim atas, jadi di plate yang ramai (kolase mitos) kontrasnya tipis. Perbaikan
v2: satu gradient atas 180 px, tanpa perlu mengubah apa pun yang lain.
