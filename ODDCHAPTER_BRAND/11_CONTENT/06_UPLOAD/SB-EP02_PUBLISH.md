# SB-EP02 — MH370: SATU BUSUR SATELIT · rencana tayang

Status per 18 Nov 2026. Semua angka di bawah ini bisa diperiksa ulang dari berkas
yang disebut, bukan dari ingatan.

| bagian | keadaan | bukti |
|---|---|---|
| VO 9 segmen | terpotong & terverifikasi | `02_SCRIPT/VO/SB-EP02/VO_BOUNDARIES.md`, `words.json` |
| Naskah | v2, gerbang `00E §7` lulus | `02_SCRIPT/SB-EP02_mh370_satu-busur-satelit.md` |
| Footage | 43 klip Coverr 1080p30 | `footage/sb-ep02/`, `footage-report-sb-ep02.json` |
| Plate diagram | 7 gambar (AI) | `10_FILM/assets/SB-EP02/` |
| Master 16:9 | 8:12 (491,97 dtk), 1920×1080 30 fps, −13,9 LUFS, TP −1,5 dBTP | `output/episodes/SB-EP02_MH370_1920x1080_master.mp4` |
| Caption | 194 cue SRT + caption bakar per kata | `10_FILM/captions/SB-EP02.id.srt` |
| Thumbnail | 1× 16:9 + 5× 9:16 dari frame master | `06_UPLOAD/thumbs/SB-EP02*` |
| Shorts | 5× 9:16, 42–53 dtk, potong dari master | `work/shorts/SB-EP02_S*.mp4` |

## Berkas di Drive (folder `1EuT_BfTVx25yN-EvvH7n1PhQo2Oap4BC`, semua publik)

| berkas | id | ukuran |
|---|---|---|
| `SB-EP02_MH370_1920x1080_master.mp4` | `1W51gewNOAARZ5vdOpELK49a8gQ-wPHSx` | 90.109.036 B |
| `SB-EP02_S1.mp4` | `1CsCGDYJAZKE-1vwLVnnw6pNyrSO2ASyL` | 4.572.835 B |
| `SB-EP02_S2.mp4` | `1FCkmINh1JiMl2cr51wFl4JAdLdQd0XQJ` | 2.292.474 B |
| `SB-EP02_S3.mp4` | `1oD13xfVazPGXAwkc-yU1iIRWnTcescR4` | 8.585.129 B |
| `SB-EP02_S4.mp4` | `1qt2FTe3wz4lXUCdaM_3I25qQWWb3XFks` | 6.501.580 B |
| `SB-EP02_S5.mp4` | `13byEYciV_wnvFmNV-aFl0HFjvxHF5-_k` | 2.443.839 B |

QC teks sudah lewat `upload_zernio.py` (dry-run): judul 70 karakter, hook berangka,
deskripsi dibuka hook yang sama, thumbnail <2 MB. Metadata: `06_UPLOAD/SB-EP02*.json`.

## Urutan tayang (sesuai keputusan pemilik: Shorts dulu)

1. `SB-EP02_S1` … `SB-EP02_S5` — satu per satu, jeda minimal 6 jam, judul & thumbnail
   masing-masing sudah disiapkan di `06_UPLOAD/SB-EP02_S*.json`.
2. Master panjang setelah Short terakhir. Deskripsi master menautkan playlist/shorts,
   dan Short menautkan master begitu master tayang.

## Yang perlu persetujuan pemilik

- Unggah ke YouTube **belum** dilakukan. Berkas antrean `queue/SB-EP02.json` sengaja
  ditulis dengan `"approved": false`; selama nilainya bukan `true`, workflow
  `youtube-upload.yml` hanya memberi peringatan dan tidak mengunggah apa pun.
- Master harus ada di Drive dan **dibagikan publik** dulu (`§23`); `drive_file_id` di
  `06_UPLOAD/SB-EP02.json` harus diisi dari hasil unggah itu.
- Thumbnail 16:9 wajib ditinjau dari frame master (bukan dari Short), sesuai aturan lama.

## Cara menerbitkan (kalau sudah disetujui)

```bash
# 1 · isi drive_file_id hasil unggah, lalu
python3 ODDCHAPTER_BRAND/tools/build_meta_sbep02.py --drive <FILE_ID>
# 2 · ubah "approved": false → true pada queue yang dituju
# 3 · push — satu berkas antrean = satu unggahan, dan published.json mencatatnya
```
