# AK-EP03 — Dyatlov Pass 1959 (POV tim pencari: Slobtsov & Sharavin)

Status: **`approved: false`** — belum diunggah ke YouTube. Menunggu pemilik menonton
`work/dyatlov-pass/out/AK-EP03_dyatlov-pass_short_v1.mp4`.

Judul: **Orang Pertama yang Menemukan Tenda Dyatlov Pass #Shorts**

## Berkas

| Berkas | Ukuran | Drive ID |
|---|---|---|
| `AK-EP03_dyatlov-pass_short_v1.mp4` (101,6 s, 1080×1920 @30) | 33.629.684 B | `1X0yLGOr8L2G-2tNTpg0_UdaNQRgoMUdO` (publik) |
| `AK-EP03_thumbnail_16x9.jpg` (1280×720) | 70.498 B | `1xpt-mwB5NzvlZWky8uH7G5Xvf4HlhOD6` |
| `AK-EP03_poster_9x16.jpg` (1080×1920) | 132.794 B | `1UlQc9gifN3OfGROrXN_j5z5ejip5Awrc` |
| `AK-EP03.id.srt` (86 cue) | 4.104 B | `12P9xZi81dxjdlYgcdYO_4fPEs95EtGeq` |

Semua diunggah ke folder kasus Dyatlov `1wGbbQRtgyBEQrsZ2tfAz8bF8PBsB4Buo`
(mp4 sudah dibuat publik untuk ditonton). Lokal: `work/dyatlov-pass/out/`,
`ODDCHAPTER_BRAND/11_CONTENT/06_UPLOAD/` (+ `thumbs/`).

sha256 `fa71c1a1d9a15ad09d3992871285e5790a06e582d5dbc391b1a5e124dce4ca1a`
Audio: −15,0 LUFS · true peak −1,6 dBTP · AAC 192 k / 44,1 kHz.
VO pemilik: `vo_dyatlov-pass.mp3` (101,38 s, 178 kata) — dipakai apa adanya, tidak di-TTS ulang.

## Yang berubah dari kerangka EP02

- **Builder** (`ODDCHAPTER_BRAND/tools/build_short_case.py`) dapat dua mode footage baru:
  `clipfill` (footage penuh layar 9:16 untuk klip vertikal/tekstur salju) dan opsi per-shot
  `bg` untuk mengatur terang latar blur (klip malam tetap gelap).
- **Bed audio** kini bisa diganti per kasus lewat `CFG.BED_BUILDER`; Dyatlov memakai
  `work/dyatlov-pass/bed_dyatlov.py` — angin, derak salju, drone 43 Hz, tanpa musik dramatis,
  dengan dua penurunan bed: setelah "tak ada seorang pun" dan sepanjang adegan minum.
- Footage **tidak** diberi label REKONSTRUKSI (bukan drama TV), tapi selalu bertag
  `FOOTAGE STOK · MIXKIT FREE LICENSE` + kredit Mixkit di kartu akhir dan deskripsi.

## Peta beat (selaras `vo_alignment.json`)

| t (s) | Beat VO | Visual |
|---|---|---|
| 0,0 | "Mereka menemukan tenda itu…" | hitam + angin |
| 1,2 | "…lalu duduk di dalamnya" | foto tenda 1959 (canvas, tag PD) |
| 4,6 | "minum untuk kesehatan sembilan orang" | salju di hutan pinus (clipfill) |
| 9,35 | "Pegunungan Ural, 26 Februari 1959" | kabut kaki gunung + stamp `26 · 02 · 1959` |
| 13,3 | "Setelah keluarga mendesak pencarian" | kabut puncak (jendela 16:9) |
| 17,4 | "relawan mahasiswa dikirim" | peta Kholat-Sayakhl (CC BY-SA 4.0) |
| 21,3 | "Boris Slobtsov dan Mikhail Sharavin" | dua sosok berjalan di puncak |
| 25,2 | "sembilan pendaki dari kampus mereka" | peta lereng (CC BY-SA 4.0) + stamp SEMBILAN PENDAKI |
| 28,1 | "Lewat teropong… sesuatu di lereng" | foto tenda, zoom rapat (POV) |
| 32,2 | "Tenda yang ambruk" | salju hutan berkabut + **TENDA ITU** |
| 35,6 | "bagian tengahnya sobek" | foto tenda (canvas) |
| 38,9 | "Tak ada seorang pun" | salju turun (jendela) + **KOSONG** |
| 42,3 | "di pintu tergantung jaket Dyatlov" | foto tenda (kartu) |
| 45,8 | "Di sakunya masih ada uang" | tenda + api malam (UANGNYA MASIH ADA) |
| 48,9 | "membuat mereka sedikit lega" | salju pinus (clipfill) |
| 51,7 | "Mereka menggali parit…" | salju hutan berkabut |
| 56,6 | "Kami sangat senang, kenangnya" | kabut (clipfill, bed diturunkan) |
| 59,7 | "Lalu mereka duduk di dalam tenda" | tenda + api malam |
| 63,5 | "membuka botol alkohol…" | api malam (jendela) |
| 68,3 | "Orang-orang lokal… minum untuk arwah" | tenda + api malam (jendela lain) |
| 71,1 | "Slobtsov nyaris memukulnya" | kabut dingin (clipfill) |
| 75,0 | "Sebulan telah lewat" | bulan di hutan salju + stamp SEBULAN KEMUDIAN |
| 78,0 | "imajinasi mereka tak sampai ke sana" | memorial sembilan foto (PD) |
| 81,4 | "Hari itu mereka melapor lewat radio" | dial radio analog (RADIO: TENDA DITEMUKAN) |
| 85,5 | "pencarian berubah…" | salju pinus |
| 88,7 | "jauh lebih sunyi" | kabut puncak (clipfill) |
| 91,5 | "Semua tim lain dipindahkan ke lereng itu" | peta Oblast Sverdlovsk (PD) |
| 94,5 | "Lebih dari 60 tahun kemudian…" | bulan + monumen Mikhailovskoe |
| 96,9 | "masih diperdebatkan" | monumen (canvas) |
| 100,9 | — | kartu akhir: ODDCHAPTER + kredit + @oddchapter7 |

## Footage stok yang dipakai (Mixkit Free License)

| Klip | Dipakai di | Perlakuan |
|---|---|---|
| `mixkit_3308` kabut kaki gunung (vertikal) | 9,4 / 56,6 / 71,1 | full-bleed |
| `mixkit_3352` salju di hutan pinus (vertikal) | 4,6 / 48,9 / 85,5 | full-bleed |
| `mixkit_4396` kabut puncak | 13,3 / 88,7 | jendela 16:9 / full-bleed |
| `mixkit_3335` dua orang di puncak | 21,3 | jendela 16:9 |
| `mixkit_35040` salju hutan berkabut | 32,2 / 38,9 / 51,7 | full-bleed / jendela |
| `mixkit_47311` api unggun + tenda malam | 45,8 / 59,7 / 63,5 / 68,3 | jendela 16:9, latar digelapkan |
| `mixkit_48533` dial radio analog | 81,4 | jendela 16:9 |
| `mixkit_3350` bulan di hutan salju | 75,0 / 94,5 | jendela 16:9 |
| `mixkit_43144` orang di dalam tenda (siang) | **tidak dipakai** | tenda modern siang hari, salah zaman/suasana |

Klip berhak cipta di `footage_risiko/` **tidak** dipakai sama sekali.

## Kepatuhan aturan

- Tanpa gore, tanpa deskripsi jenazah, tanpa teori konspirasi; penyebab kematian tidak dinyatakan.
- Klaim satu sumber selalu diberi atribusi di VO ("kata Slobtsov", "kenangnya", "katanya").
- Semua foto/klip berlisensi jelas; peta CC BY-SA 4.0 dikreditkan di layar + deskripsi.
- Sumber fakta: Wikipedia, dyatlovpass.com (The Search in 1959; Slobtsov, EX no.46/2007),
  wawancara Sharavin.
