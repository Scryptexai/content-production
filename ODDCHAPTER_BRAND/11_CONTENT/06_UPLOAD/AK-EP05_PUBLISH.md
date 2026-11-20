# AK-EP05 — Andes 1972 (uji format Curiosity Loop)

Status: **DRAFT — BELUM DIIZINKAN TAYANG** (`approved:false` di `queue/AK-EP05.json`).
Dry-run `upload_zernio.py AK-EP05` lolos 20 Nov 2026. Menunggu persetujuan pemilik
setelah format 8 beat terbukti; episode ini di luar daftar ide Drive, jadi izin lama
(EP03/EP04) tidak berlaku.

**VO = TTS internal (voice-05), bukan VO pemilik.** Naskah
`02_SCRIPT/AK-EP05_andes-1972.md` sudah diselaraskan dengan teks TTS yang dipakai
(408 kata, **169,12 s**). Format: 8 beat adaptasi `00F_FORMAT_CURIOSITY_LOOP.md` §2,
durasi 2:53 (keputusan pemilik: bebas 1–3 menit, asal beat benar & kalimat utuh).

Judul: **72 Hari di Andes: 45 Orang Terjebak, 16 Selamat oleh Satu Keputusan**
Hook (awal deskripsi): "Tujuh hari tanpa makanan di punggung Andes — apa yang akan
kalian lakukan?"

## Berkas

| Berkas | Ukuran | Drive ID |
|---|---|---|
| `AK-EP05_andes-1972_short.mp4` (173,0 s, 1080×1920 @30) — rev2 | 49.084.435 B | `1mZxYU9s9X7UexYzYvwDHzIlnxy7BfhSK` |
| `AK-EP05_thumbnail_16x9.jpg` (1280×720) | 84.485 B | `14erM1wGCF-vE_9kXLWDuTfvxh-3oVhQu` |
| `AK-EP05_poster_9x16.jpg` (1080×1920) | 170.240 B | `12AdFMRtY82JZnaQGYt2jC37ITkiZdOBF` |
| `AK-EP05.id.srt` (183 cue) | 8.924 B | `1FU37YtX79m-iv-E3wsvSN2Chfou2rn5v` |

Folder Drive: `1pxGWa4Fdisj7UBzEWC4BPFWSBIlTj71o` (andes-1972), MP4 sudah publik.
sha256 `0bf601e8a5e448fc25d5ef59aa35e66cb1d1c53b62ad2c4266878a6d7b9249fa`
Audio: −15,0 LUFS · true peak −1,4 dBTP · AAC / 44,1 kHz.

## Peta beat (selaras teks TTS final)

| t (s) | Beat | Fungsi |
|---|---|---|
| 0,00 | B1 | Tantangan Logika / Dilema Ekstrem |
| 10,04 | B2 | Reaksi Alami Manusia — opsi normal: buah-buahan |
| 19,77 | B3 | Tindakan Sang Tokoh yang Mengagetkan (tanpa bocor jawaban) |
| 37,79 | B4 | Pertaruhan Nyawa (High Stakes) |
| 56,35 | B5 | Tekanan Situasi — kecelakaan (reveal: Pegunungan Andes) |
| 80,57 | B6 | Tekanan Situasi — kelaparan & longsor |
| 102,03 | B7 | Tekanan Situasi — sumpah bersama |
| 114,70 | B8 | Momen Puncak — berjalan keluar |
| 132,93 | B9 | Hasil Akhir & Fakta Kunci (reveal) |
| 155,46 | B10 | Interactive Debate Hook → 169,12; video 173,03 |

## Revisi rev2 (koreksi pemilik, 20 Nov 2026)

- B2: opsi jawaban normal "daun atau akar" → **buah-buahan / makanan yang biasa
  ada di hutan** (pilihan wajar; twist B3 tetap ekstrem).
- Rujukan "gunung itu" yang menggantung → skema sembunyi–tampil: B1–B3
  "pegunungan bersalju" (disamar), B5 tampil **Pegunungan Andes**, B9 menutup
  "Pegunungan Andes". Overlay: "PASTI KALIAN CARI BUAH-BUAHAN", "HARI DI ANDES".
- vo_02/vo_03/vo_09 diregenerasi; retime penuh `case_cfg.py` + `bed_andes.py`
  (`retime.py`); VO 169,91 → 169,12 s; video 174,00 → 173,03 s.

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
