# WORKFLOW.md — urutan produksi dan serah-terima antar tahap

Versi asli (generik) dari pemilik: `WORKFLOW_upstream.md`. Dokumen ini adalah
versi yang mengikat untuk repo ini: nama berkas, nama alat, dan gerbangnya nyata.

## 1 · Alur satu episode

```
brief → premis → karakter/entitas → beat kausal → naskah (suara kanal)
      → audit naskah → plate gambar → thumbnail → rekam narasi → efek & bed
      → timing → render → loudnorm → Drive → antrean unggah → tayang → catat
```

| # | tahap | dikerjakan dengan | keluaran | gerbang |
|---|---|---|---|---|
| 1 | brief | pilihan topik + seri (HILANG/TERSEMBUNYI/ANEh/…) | satu kalimat janji episode | topik belum pernah dipakai |
| 2 | premis | `STORYTELLING-FONDAMENTAL.md` | pertanyaan dramatik tunggal | ada satu pertanyaan, bukan tiga |
| 3 | entitas | `HOOK ENGINEERING.md` §3 + `00B` | `entitas`, `protagonis`, `mau`, `hambatan` | entitas disebut di hook |
| 4 | beat | `00B` + `NARRATIVE-TENSION…` | 8 beat + hook + loop | `check_story.py` (lima efek) |
| 5 | naskah | `00E` + `NATURAL-INDONESIAN…` | kalimat yang diucapkan | `check_story.py` (suara + TTS) |
| 6 | audit | `EDITORIAL-FONDATION.md` §5 + tabel audit `AGENTS.md` §3 | catatan revisi | tidak ada klaim tanpa sumber |
| 7 | gambar | `VISUAL-STORYTELLING.md` + `IMAGE-GENERATION.md` | 9–10 plate 9:16 | satu gambar melekat, tanpa wajah karangan |
| 8 | thumbnail | `03_THUMBNAIL` + aturan 1–3 kata | jpg 1080×1920 | teks ≤3 kata, terbaca di layar kecil |
| 9 | suara | `elevenlabs-tts-2026/SKILL.md` + `voice.json` | mp3 per segmen | markup bersih, `MANIFEST.json` ada, **prosodi terukur** (`speech_prosody.py`) |
| 10 | efek & bed | `eleven_audio.py --only sfx/place`, `build_bed.py` | `sfx.wav`, `bed.wav` | efek tidak menutupi kata |
| 11 | timing | `build_timing.py` | `timing.generated.json` | semua segmen `measured: true` |
| 12 | render | `render-episode.mjs` | mp4 1080×1920 | masih + frame cek visual |
| 13 | loudnorm | ffmpeg `loudnorm` + `ebur128` | master | −14 LUFS ±0,5 · ≤ −1,5 dBTP |
| 14 | Drive | `upload_file` + `make_public` | `drive_file_id` | bisa diunduh publik |
| 15 | antrean | `06_UPLOAD/EPxx.json` + `queue/EPxx.json` | push | `publishNow: true` |
| 16 | tayang | `youtube-upload.yml` | URL + `post_id` | tercatat di `published.json` |

## 2 · Serah-terima (handoff)

Setiap tahap menyerahkan **data**, bukan narasi panjang. Bentuk minimal:

```json
{
  "episode": "EP09",
  "revision": 1,
  "series": "TERSEMBUNYI",
  "pov": "A",
  "entitas": "…",
  "hook_door": "pertanyaan|pernyataan|fakta|harapan|khayalan|adegan|dialog",
  "beats": [{"part": "tanya", "text": "…"}],
  "gambar_melekat": "…",
  "sumber": ["…"],
  "gates": {"check_story": "LULUS", "tts": "bersih", "loudness": "-14.7 LUFS"},
  "status": "draft|audited|recorded|rendered|queued|published"
}
```

Aturan serah-terima:

- Tahap berikutnya **tidak boleh** mengubah fakta yang sudah ditetapkan tahap sebelumnya
  tanpa mencatat perubahan dan menjalankan ulang gerbang yang terdampak.
- Kalau gerbang gagal, alur **berhenti** di tahap itu. Tidak ada "nanti diperbaiki saat render".
- Revisi naskah setelah rekaman = rekam ulang segmen yang berubah saja, lalu `build_timing.py`
  wajib dijalankan lagi (caption mengikuti audio nyata, bukan perkiraan).

## 3 · Peran yang dipisah (satu agen boleh memerankan semua, tapi tidak sekaligus)

1. **Direktur** — menjaga janji episode, memutuskan pintu hook.
2. **Penulis** — beat kausal, kalimat yang diucapkan.
3. **Editor** — memotong yang tidak perlu, menjaga integritas fakta.
4. **Sutradara visual** — plate, urutan, gambar melekat.
5. **Sutradara suara** — arah VO, tanda baca, jeda, campuran.
6. **QC** — menjalankan gerbang, menulis catatan, menolak yang belum layak.

Praktiknya di sesi ini: satu agen, tetapi **urutannya tidak boleh dilompati** —
terutama QC sebelum rekam, karena rekaman yang salah membakar kuota dan waktu render.

## 4 · Kalau ada yang gagal

| gejala | langkah pertama |
|---|---|
| `check_story.py` gagal | perbaiki naskah, jangan turunkan gerbang |
| narasi terasa datar | `PUNCTUATION.md`: pecah kalimat, tambah satu jeda bermakna |
| narasi terasa teater | buang tag, kurangi elipsis, kembali ke baseline tanda baca |
| render > 25 menit / crash | cek `node_modules`, font, `chromium`; ulangi sekali, lalu lapor |
| unggahan gagal | baca annotation run; jangan ubah metadata untuk "mencoba lagi" |
| loudness meleset | ulangi encode; jangan menormalkan audio di editor lain |
