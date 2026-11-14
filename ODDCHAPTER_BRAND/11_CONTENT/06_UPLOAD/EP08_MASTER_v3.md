# EP08 — Isdal Woman · master v3 (suara Denas)

**Berkas:** `EP08_1080x1920_master_v3.mp4` · 51,0 s · 14.734.683 B · 1080×1920
**sha256:** `7fd50bf44c2429b673079cc94a39026e1ad440f15da213d9a2ef4b495ba56cce`
**Status:** menunggu persetujuan pemilik. **Belum diunggah ke YouTube** — gerbang unggah menolak antrean tanpa `"approved": true`.

## Angka hasil ukur (bukan klaim)

| Pemeriksaan | Alat | Hasil |
|---|---|---|
| Satu suara di semua segmen | `tools/voice_consistency.py` | **LULUS** — 12/12 segmen Denas `arwfiAiEfIHHZCwcYYx2` |
| Naskah diucapkan seluruhnya | banding naskah vs 12 berkas segmen | 12/12 segmen, 105 kata, tidak ada segmen berisi teks lain |
| Ritme | wpm per segmen | rata **138,4 wpm**, rentang **126–147** (sebelumnya ada 202 wpm) |
| Backsound tidak menutupi VO | RMS narasi vs RMS jeda | narasi −16,3 dBFS · jeda −32,2 dBFS → **selisih 15,9 dB** |
| Tidak ada VO turun 1–2 kata | RMS tiap segmen | semua segmen disamakan **−20,0 dBFS** |
| Loudness master | `ebur128=peak=true` | **−14,0 LUFS** · true peak **−1,7 dBTP** |

## Kenapa beda dari v2

Campuran audio sekarang disusun oleh `tools/mix_master.py`: tiap segmen narasi dinormalkan dulu ke RMS yang sama, bed digeser tepat ke target (−36 LUFS) dengan gain yang dihitung dari hasil ukur, lalu hasil campuran diukur dan dinormalisasi ke −14 LUFS. Di v2 campuran diserahkan ke volume tetap di Remotion tanpa pengukuran, dan itu penyebab "VO kurang jelas" yang Anda dengar dua kali.

## Catatan yang masih terbuka

1. Tiga segmen punya lompatan nada akhir kalimat: `07_turn` +21,19 st, `09_consequence` +20,99 st, `99_loop` +21,81 st. Bisa jadi artefak pengukuran sesudah kompresor, bisa jadi intonasi. Kalau setelah didengar terasa aneh, sebut nomor segmennya — perbaikan hanya perlu rekam ulang segmen itu dan remix, tidak render ulang.
2. Dua video EP08 masih publik di @oddchapter7 dan harus dihapus manual oleh pemilik: `F6BGrQhYmaA` (v1) dan `3E2ekjMZPkc` (v2).
