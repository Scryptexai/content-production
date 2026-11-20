# AK-EP05 — Andes 1972 (uji format Curiosity Loop)

Status: **DRAFT — BELUM DIIZINKAN TAYANG** (`approved:false` di `queue/AK-EP05.json`).
Dry-run `upload_zernio.py AK-EP05` lolos 20 Nov 2026. Menunggu persetujuan pemilik
setelah format 8 beat terbukti; episode ini di luar daftar ide Drive, jadi izin lama
(EP03/EP04) tidak berlaku.

**VO = TTS internal (voice-05), bukan VO pemilik.** Naskah
`02_SCRIPT/AK-EP05_andes-1972.md` sudah diselaraskan dengan teks TTS yang dipakai
(405 kata, **169,91 s**). Format: 8 beat adaptasi `00F_FORMAT_CURIOSITY_LOOP.md` §2,
durasi 2:54 (keputusan pemilik: bebas 1–3 menit, asal beat benar & kalimat utuh).

Judul: **72 Hari di Andes: 45 Orang Terjebak, 16 Selamat oleh Satu Keputusan**
Hook (awal deskripsi): "Tujuh hari tanpa makanan di punggung Andes — apa yang akan
kalian lakukan?"

## Berkas

| Berkas | Ukuran | Drive ID |
|---|---|---|
| `AK-EP05_andes-1972_short.mp4` (174,0 s, 1080×1920 @30) | 49.867.830 B | `1vlE4Ljyua_t9ZO_YJULjGWNHzkmWPMpr` |
| `AK-EP05_thumbnail_16x9.jpg` (1280×720) | 84.485 B | `14erM1wGCF-vE_9kXLWDuTfvxh-3oVhQu` |
| `AK-EP05_poster_9x16.jpg` (1080×1920) | 170.240 B | `12AdFMRtY82JZnaQGYt2jC37ITkiZdOBF` |
| `AK-EP05.id.srt` (181 cue) | 8.818 B | `15hu9Sy3__fbFFqwCKnZ5dcQdJDQaLVZU` |

Folder Drive: `1pxGWa4Fdisj7UBzEWC4BPFWSBIlTj71o` (andes-1972), MP4 sudah publik.
sha256 `1f2edeffc814d688930906e40461b9927f89ba659861a85b699d3d1db41b8401`
Audio: −15,0 LUFS · true peak −1,4 dBTP · AAC / 44,1 kHz.

## Peta beat (selaras teks TTS final)

| t (s) | Beat | Fungsi |
|---|---|---|
| 0,00 | B1 | Tantangan Logika / Dilema Ekstrem |
| 10,04 | B2 | Reaksi Alami Manusia |
| 21,23 | B3 | Tindakan Sang Tokoh yang Mengagetkan (tanpa bocor jawaban) |
| 38,55 | B4 | Pertaruhan Nyawa (High Stakes) |
| 57,10 | B5 | Tekanan Situasi — kecelakaan |
| 81,33 | B6 | Tekanan Situasi — kelaparan & longsor |
| 102,79 | B7 | Tekanan Situasi — sumpah bersama |
| 115,46 | B8 | Momen Puncak — berjalan keluar |
| 133,69 | B9 | Hasil Akhir & Fakta Kunci (reveal) |
| 156,24 | B10 | Interactive Debate Hook → 169,91; video 174,00 |

## Fakta & sumber

- 13 Okt 1972, Fairchild FH-227D, 45 orang (Old Christians Club, Uruguay → Santiago),
  12 tewas seketika; longsor 29 Okt (+8); pencarian dihentikan hari ke-11; Parrado &
  Canessa trek ±10 hari → Sergio Catalán; 16 selamat; evakuasi 22–23 Des 1972 (72 hari).
- Angka yang berbeda (12 vs 13 tewas tabrakan; evakuasi 20 vs 22 Des) disebut sebagai
  perdebatan di deskripsi — tidak dipilih diam-diam.
- Sumber: Britannica; Wikipedia `Uruguayan_Air_Force_Flight_571`; Read (1974),
  Parrado (2006), Vierci (2008).

## Aturan editorial yang dipatuhi

- Tanpa gore, tanpa jenazah, tanpa penyebab kematian eksplisit, tanpa teori konspirasi.
- Tidak memakai `footage_risiko/`; hanya Coverr Free License (24 klip, kredit di
  deskripsi + kartu akhir + label layar).
- Tanpa orang di frame; thumb/poster AI tanpa manusia; label `KASUS NYATA · ARSIP ASLI`.
- Durasi bebas 1–3 menit (keputusan pemilik); kalimat VO utuh, tidak dipersingkat.

## Langkah berikut (setelah pemilik setujui)

1. `python3 ODDCHAPTER_BRAND/tools/upload_zernio.py AK-EP05 --media-dir work/andes-1972/out`
   (dry-run, sudah lolos) → tambah `--send` untuk tayang.
2. Setelah tayang: catat di `published.json`, ubah `queue/AK-EP05.json` →
   `"status": "done"`, isi `link` + `hasil`.
3. Evaluasi uji format di `00F_FORMAT_CURIOSITY_LOOP.md` §7 sebelum episode berikutnya
   (Jonestown masih ditahan sampai format terbukti).

## Kalau perlu render ulang

```
python3 ODDCHAPTER_BRAND/tools/build_short_case.py andes-1972 shots|video|audio|mux|srt
python3 ODDCHAPTER_BRAND/tools/make_thumb_case.py andes-1972
```

VO TTS tersimpan di `work/andes-1972/vo_andes.mp3` + `audio/vo_01..10.mp3` +
`vo_alignment.json` + `build_vo.py` (SEGS final). Footage di `footage/andes-1972/`
(symlink), picks aktif `tools/footage_picks/ANDES-1972-picks.json`. Semua klip 6,00 s.
