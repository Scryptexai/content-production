# AK-EP02 — Krakatau 1883 (Kapten Lindemann & Loudon)

Status: **`approved: false`** — belum diunggah ke YouTube. Semua artefak sudah di Drive.

## Berkas

| Berkas | Ukuran | Drive ID |
|---|---|---|
| `AK-EP02_krakatau-1883_short_v1.mp4` (106,4 s, 1080×1920 @30) | 29.976.769 B | `1DNV01RC39NLFSeNHUehvu0fMrwiSM6u_` |
| `AK-EP02_thumbnail_16x9.jpg` | 172.897 B | `1iusJx_bVvnYo3dlimb5pfGL-KoWGWHEc` |
| `AK-EP02_poster_9x16.jpg` | 473.206 B | `1Iz87YdHVDIJU9XK_BpZ-K1JhT9OLiL8_` |
| `AK-EP02.id.srt` (85 cue) | 4.109 B | `1c5JENSvqkTL9VR3H7roRH4FsUIOXTi2a` |

Folder Drive: `krakatau-1883/` → `1xofrSnxqA26kVOlpgfP7INLRpgCeiqbJ` (keempatnya sudah publik: anyone/reader).

Lokal: `work/krakatau-1883/out/AK-EP02_krakatau-1883_short_v1.mp4`
sha256 `1c4f63f5f72047d42b2141894622ecbafe534a2e2d318998c117c2772c9c15d6`

Audio: −15,12 LUFS · true peak −1,52 dBTP · AAC 192 k · 44,1 kHz.
VO milik pemilik: `vo_krakatau-1883.mp3` (105,465 s, 184 kata, suara "Dhawa", eleven_multilingual_v2, speed 0,95) — tidak di-TTS ulang.

## Judul & hook

- Judul (74 char): `Tsunami Krakatau Datang. Kapten Ini Malah Membelokkan Kapalnya ke Arahnya.`
- Hook (dipakai juga sebagai kalimat pembuka deskripsi): `Kalau semua orang berlari ke darat, kenapa kapten ini justru membawa kapalnya ke tengah gelombang?`
- Tags 11, kategori YouTube 24 (Entertainment), `madeForKids: false`.
- `containsSyntheticMedia: true` — narasi VO sintetis (ElevenLabs); seluruh foto/ilustrasi = arsip asli, bukan AI.

## Peta beat (align ke `vo_alignment.json`)

| t (s) | Beat | Perlakuan visual |
|---|---|---|
| 0,0 | Hook "Saat tsunami Krakatau datang…" | kartu: Kicker + Big merah "MENGHADAPI TSUNAMI" |
| 10,9 | Telok Betong, Lampung | canvas Residentiehuis (tag KITLV CC BY 4.0) |
| 15,6 | 26 Agustus 1883 | kartu + Stamp merah "26 AGUSTUS 1883" |
| 18,9 | Loudon, Kapten Lindemann | kartu papan nama: KAPAL UAP POS & WISATA / **LOUDON** / KAPTEN J. T. H. LINDEMANN |
| 25,2 | Laut berputar, tak ada perahu | litograf Royal Society (canvas) |
| 31,4 | Pukul satu pagi, mualim kembali | kartu + Stamp "01.00" |
| 38,5 | Berouw kandas | kartu + Big merah "BEROUW" |
| 44,8 | ±07.00, dinding air | canvas KITLV 5888 |
| 47,3 | Laut jadi dinding | kartu + Stamp "07.00" |
| 51,0 | Kapal pos & wisata, bukan perang | kartu + Stamp "KAPAL POS · BUKAN PERANG" |
| 57,5 | Kemudi diputar, menghadap gelombang | karang terlempar (Tropenmuseum CC BY-SA 3.0) |
| 63,6 | Naik ke puncak, meluncur turun | litograf KITLV |
| 72,5 | Telok Betong disapu | Residentiehuis (canvas) |
| 76,0 | Berouw terlempar ke pohon kelapa | karang terlempar (canvas) |
| 80,3 | Tiga jam kemudian: batu apung & abu | kartu + Kicker "TIGA JAM KEMUDIAN" |
| 86,0 | 10.30 gelap total | kartu + Big merah "10.30" + "SEPERTI TENGAH MALAM" |
| 97,8 | 36.000 tewas | kartu + Big "36.000" + "ANGKA RESMI 36.417" |
| 104,4 | "Satu kapal pulang membawa cerita" | kartu akhir: ODDCHAPTER · kredit foto + sumber + @oddchapter7 |

Tag sumber selalu muncul di setiap shot ber-foto; kredit lengkap + CTA ada di kartu akhir.

## QA yang sudah lewat

- 27 shot (10 kartu desain + 1 kartu hitam), 85 caption (≤3 kata / ≤18 karakter, kata kunci merah saja), 21 overlay teks.
- Overlay hanya di kartu desain → tidak pernah menabrak judul/foto; tag sumber di y=300, overlay ≥ y=430, caption di y≈1100.
- Caption panjang (mis. "GOUVERNEUR-GENERAAL LOUDON") otomatis dikecilkan agar tetap di dalam margin 60 px.
- `loudnorm` −15,12 LUFS / TP −1,52 dB, stream `h264 High, yuv420p(tv, bt709), 1080×1920, 30 fps`.
- Attribute wajib: karang terlempar = Woodbury & Page (CC BY-SA 3.0); Residentiehuis = ilustrasi suasana (CC BY 4.0), bukan foto kejadian; dinyatakan di tag + kredit.
- Klaim yang sengaja **tidak** dipakai: nomor klaim #5/#7/#9 di `fakta.md`, jam pasti gelombang (VO memakai "sekitar pukul tujuh").

## Cara build ulang

```bash
cd ODDCHAPTER_BRAND/tools
python3 build_short_case.py krakatau-1883 shots    # 27 shot (10 kartu di-cache)
python3 build_short_case.py krakatau-1883 video    # subs.ass + concat + burn
python3 build_short_case.py krakatau-1883 audio    # bed numpy + loudnorm
python3 build_short_case.py krakatau-1883 mux
python3 build_short_case.py krakatau-1883 srt      # → 06_UPLOAD/AK-EP02.id.srt
python3 make_thumb_case.py krakatau-1883           # thumb 16:9 + poster 9:16
```

Konfigurasi kasus: `work/krakatau-1883/case_cfg.py` (IMAGES, SHOTS, OVL, KEYWORDS, NUM_PHRASES, MERGE, WORD_FIX) dan `thumb_cfg.py`.

## Cara terbit (setelah pemilik menonton)

1. Ubah `approved` → `true` di `06_UPLOAD/AK-EP02.json` **dan** `06_UPLOAD/queue/AK-EP02.json`.
2. `python3 tools/upload_zernio.py AK-EP02 --media-dir work/krakatau-1883/out` (dry-run dulu, cek hook/judul).
3. Kirim ke Zernio: tambahkan `--send`. Jangan pernah `--send` tanpa izin eksplisit pemilik.
