# AK-EP04 — Kapal Van der Wijck 1936 (POV lima nelayan Brondong)

Status: **DRAF SELESAI, BELUM TAYANG.** Menunggu izin pemilik sebelum masuk antrean
(`queue/AK-EP04.json` masih `"status": "draft"`, `"approved": false`).

Judul: **Kapal Itu Tenggelam dalam 6 Menit. 145 Orang Diselamatkan Lima Nelayan.**

Sumber ide: spreadsheet Drive "ODDCHAPTER – Daftar Ide Konten (19 Nov 2026)", peringkat 2
(skor 20) — bukan ide hasil riset baru.

## Berkas

| Berkas | Ukuran | Lokasi |
|---|---|---|
| `AK-EP04_van-der-wijck-1936_short_v1.mp4` (95,7 s, 1080×1920 @30) | 34.596.271 B | `work/van-der-wijck-1936/out/` (belum ke Drive) |
| `AK-EP04_thumbnail_16x9.jpg` (1280×720) | 74.930 B | `06_UPLOAD/thumbs/` |
| `AK-EP04_poster_9x16.jpg` (1080×1920) | 100.159 B | `06_UPLOAD/thumbs/` |
| `AK-EP04.id.srt` (83 cue) | 4.003 B | `06_UPLOAD/` |

sha256 `fe548f93da2a0da33c388457228b95b6e8cc5fca010270e3e4682e9c87efabc8`
Audio: −15,0 LUFS · true peak −1,3 dBTP · AAC 198 k / 44,1 kHz.

VO: internal TTS (voice-05), 11 beat, 208 kata / 1.373 karakter, 93,33 s. Rangkaian
klip TTS → `build_vo.py` → `vo_van-der-wijck.mp3` + `vo_alignment.json`.
Enam klip pertama gagal digabung jadi satu, jadi VO dirakit dari 10 klip (kalimat
4+5 dijadikan satu klip) — batas kalimat tetap pasti, jadi waktu kata tidak melenceng.

## Peta beat (selaras `vo_alignment.json`)

| t (s) | Beat VO | Visual |
|---|---|---|
| 0,0 | hook | hitam → pelabuhan malam |
| 1,3 | "Pada 19 Oktober 1936…" | stamp `19 OKTOBER 1936` + ombak malam |
| 9,7 | "Namanya Van der Wijck" | kapal di laut + stamp `VAN DER WIJCK · KPM` |
| 18,0 | "berlayar dari Surabaya menuju Semarang" | dermaga malam (SURABAYA → SEMARANG) |
| 24,9 | "dua belas mil dari Pantai Brondong" | ombak besar + stamp `12 MIL` |
| 32,4 | "Menurut laporan surat kabar…" | batu laut + **6 MENIT** (merah) |
| 39,8 | "Tidak ada kapal besar di dekat situ" | laut luas (bed diturunkan) |
| 44,8 | "Lima nelayan Brondong… 145 orang" | perahu + `5 NELAYAN · 145 ORANG` + daftar nama |
| 56,9 | "Delapan pesawat amfibi Dornier" | jendela kabin + awan |
| 63,2 | "Sang nakhoda selamat" | dial radio (Mixkit) |
| 67,2 | "plakat di Brondong masih menyebut namanya" | pantai + kapal di kejauhan |
| 72,0 | "Jumlah korban tidak pernah bulat" | langit malam + **42 · 58 · 75** |
| 81,4 | "bangkainya ditemukan… 28 meter" | tebing laut + stamp `28 METER` |
| 90,4 | "perahu kayu yang datang lebih dulu" | perahu senja penuh layar → kartu akhir |

## Aturan editorial yang dipatuhi

- **Tanpa gore**, tanpa kondisi jenazah, tanpa penyebab kematian eksplisit.
- **Tanpa teori konspirasi.** Penyebab tenggelam dibatasi pada yang tertulis di sumber
  (air masuk, pompa kewalahan, laporan "enam menit").
- **Angka korban tidak dipilih diam-diam**: 42 hilang (de Telegraaf 22 Okt 1936),
  58 tewas (detikJatim), 75 hilang, 70 (validnews), 55 (merdeka) — di layar dan di
  deskripsi disebut sebagai perdebatan.
- Klaim satu-sumber selalu diatribusikan: "menurut laporan surat kabar saat itu",
  "tercatat" untuk daftar 145 orang.
- Footage stok **Coverr + Mixkit Free License**, tag di layar (`FOOTAGE STOK · …`),
  kredit di kartu akhir dan di deskripsi. Tidak ada footage_risiko.

## Sebelum tayang (urutannya)

1. Minta izin pemilik. Kalau setuju → ubah `queue/AK-EP04.json` jadi
   `"status": "requested"`, `"approved": true`, `requested_at` diisi.
2. Unggah master MP4, thumbnail, poster, SRT ke folder Drive kasus ini →
   isi `drive_file_id` di `AK-EP04.json` (workflow mengunduh master dari Drive,
   bukan dari Git).
3. Push **satu** berkas antrean saja (workflow menolak >1 permintaan per push).
4. Setelah tayang: catat di `published.json`, ubah status antrean jadi `done`,
   lalu isi `_PUBLISH.md` ini dengan tautan.

## Kalau perlu render ulang

```
cp <footage Coverr/Mixkit> work/van-der-wijck-1936/footage/
python3 ODDCHAPTER_BRAND/tools/build_short_case.py van-der-wijck-1936 shots|video|audio|mux|srt
python3 ODDCHAPTER_BRAND/tools/make_thumb_case.py van-der-wijck-1936
```

Semua footage Coverr berdurasi tepat 6,00 s — durasi tiap shot + titik mulai sumber
harus ≤ 6,00 s, kalau tidak shot memendek dan total video bergeser.
