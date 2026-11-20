# AK-EP04 — Kapal Van der Wijck 1936 (POV nelayan Brondong)

Status: **TAYANG** — https://www.youtube.com/watch?v=sv_PEpSINFI (20 Nov 2026 08:48 UTC,
post Zernio `6b00093e4f1a4b87dbcf9d8c`, publik). Disetujui pemilik lewat balasan "lanjut"
atas rev2.

**Rev2 memakai VO PEMILIK**, bukan TTS lokal. VO dan teksnya diambil dari Drive
`van-der-wijck/vo` (`vo_van-der-wijck.mp3`, `vo_text.txt`, `vo_alignment.json`,
`vo_settings.json`) — ElevenLabs "Dhawa – Storytelling, Calm & Cinematic",
`eleven_multilingual_v2`, speed 0,95, **108,30 s**. Kata-katanya bukan milik saya:
hook "Semua orang kenal kapalnya…", SOS tanpa posisi, kapten enam jam terapung,
buruh pribumi yang tidak tercatat, sembilan perahu baru, dan pelat besi di mercusuar
Brondong. Rev1 (VO TTS internal, 95,7 s) dibuang dan berkasnya di Drive sudah di-trash.

Judul: **140 Orang Ditarik dari Laut Malam Itu. Tak Ada yang Tahu Siapa Mereka.**

## Berkas

| Berkas | Ukuran | Drive ID |
|---|---|---|
| `AK-EP04_van-der-wijck-1936_short_v2.mp4` (110,9 s, 1080×1920 @30) | 36.233.598 B | `1Z0PMJveNoddHwpt2w3JEp-1TkjFtzapn` |
| `AK-EP04_thumbnail_16x9.jpg` (1280×720) | 70.735 B | `1nCwbYddGA4ph4ffDOiRlmzho85va23zJ` |
| `AK-EP04_poster_9x16.jpg` (1080×1920) | 101.126 B | `1hmjax8eATZ5-nf8f1piWM55_z7PqUMAC` |
| `AK-EP04.id.srt` (89 cue) | 4.225 B | `1iSCrKTku0wVg0OAPxhYdC8WvSo-_7Brc` |

Folder Drive: `118AuYkyfDc3YvicyHanZzlU1WCj8mjRq` (van-der-wijck).
sha256 `88dcbfd6c0e4d6bb5a0929ad40262d61ef65b2ae887b41ab2a98f8e9b36399f1`
Audio: −15,0 LUFS · true peak −1,4 dBTP · AAC / 44,1 kHz.

## Peta beat (selaras `vo_alignment.json` milik pemilik)

| t (s) | Ucapan | Visual |
|---|---|---|
| 0,0 | "Semua orang kenal kapalnya…" | pelabuhan malam → ombak |
| 10,1 | "Dini hari, 20 Oktober 1936…" | kapal di laut + stamp `20 · 10 · 1936` |
| 21,5 | "Menjelang pukul satu… SOS…" | dial radio + batu laut (`SINYAL TERAKHIR`, `TANPA POSISI`) |
| 29,6 | "Menurut kesaksian pertama… oleng…" | ombak besar, batu laut (`SEKOCI TAK SEMPAT TURUN`) |
| 39,8 | "Pesawat Dornier baru berangkat saat fajar…" | awan dari kabin (`HANYA SATU SEKOCI`) |
| 47,7 | "Tapi di pesisir Brondong, Lamongan…" | perahu nelayan (`BRONDONG · LAMONGAN`, `TANPA ATURAN RESMI`) |
| 60,6 | "…menarik sekitar 140 orang dari air" | angka `140` di atas pantai |
| 62,6 | "Termasuk sang kapten… enam jam terapung" | laut gelap (`KAPTEN · 6 JAM TERAPUNG`) |
| 68,5 | "Sekitar lima puluh orang tak pernah ditemukan…" | langit malam (`50 ORANG TAK PERNAH DITEMUKAN`) |
| 71,5 | "…buruh pribumi tidak tercatat namanya" | tangan menulis + koran Belanda |
| 78,3 | "Setahun kemudian, sembilan perahu baru…" | tebing laut (`SETAHUN KEMUDIAN · 9 PERAHU`) |
| 82,2 | "…dibangun sebuah mercusuar kecil di Brondong" | rumah lampu mercusuar (3 shot) |
| 94,2 | pelat besi: "Tanda peringatan kepada penolong-penolong" | kartu hitam + tulisan pelat |
| 96,8 | "Hari ini orang menyebutnya monumen, padahal itu mercusuar" | mercusuar di tebing (`MERKUSUAR`, `BUKAN MONUMEN`) |
| 98,1 | "Kapal itu punya novel dan film" | halaman buku (`NOVEL · FILM`) |
| 104,8 | "Para penolongnya… hanya punya sebuah pelat besi" | laut gelap → kartu akhir |

## Yang berubah dari rev1

- VO: TTS internal → **VO pemilik** (108,30 s). Semua timing, caption, dan shot
  dihitung ulang dari `vo_alignment.json` milik pemilik (faster-whisper).
- Salah dengar ASR dibereskan di `case_cfg.py` lewat MERGE/WORD_FIX:
  "di nihari" → DINI HARI, "Waik" → Wijck, "monument" → monumen,
  "penulung-penulung" → PENOLONG-PENOLONG, "tiba -tiba" → TIBA-TIBA.
- Shot baru: mercusuar di tebing + rumah lampu (Coverr `s5_mercusuar_badai`),
  koran Belanda (`newspaper_printing`), tangan menulis (`hand_writing_letter`),
  halaman buku (`old_book_pages`).
- Durasi 95,7 → 110,9 s; SRT 83 → 89 cue.

## Aturan editorial yang dipatuhi

- Tanpa gore, tanpa kondisi jenazah, tanpa teori konspirasi.
- Angka: narasi memakai versi pemilik (260 di kapal, ±140 ditarik, ±50 tak ditemukan).
  Deskripsi menyebut angka sumber lain (42 hilang · 55 · 58 tewas · 75 hilang) sebagai
  perdebatan, bukan memilih diam-diam.
- Footage stok **Coverr + Mixkit Free License**, tag di layar, kredit di kartu akhir
  dan di deskripsi. Tidak ada footage_risiko.

## Setelah tayang

1. `published.json` sudah mencatat AK-EP04 (post `6b00093e4f1a4b87dbcf9d8c`).
2. `queue/AK-EP04.json` sudah `"status": "done"`.
3. MP4 di Drive dibiarkan publik seperti EP01–EP03 supaya bisa ditonton langsung.

## Kalau perlu render ulang

```
cp <footage Coverr/Mixkit> work/van-der-wijck-1936/footage/
python3 ODDCHAPTER_BRAND/tools/build_short_case.py van-der-wijck-1936 shots|video|audio|mux|srt
python3 ODDCHAPTER_BRAND/tools/make_thumb_case.py van-der-wijck-1936
```

VO pemilik tersimpan di `work/van-der-wijck-1936/vo_owner/` (mp3 + alignment asli)
dan disalin ke `vo_van-der-wijck.mp3` + `vo_alignment.json` yang dibaca builder.
Semua footage Coverr 6,00 s: durasi shot + titik mulai sumber harus ≤ 6,00 s.
