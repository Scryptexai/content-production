# AK-EP08 — Ponari: antrean yang tidak berhenti (naskah = VO pemilik)

Sumber ide: Drive `ODDCHAPTER Shortlist Batch 2` (usulan Angker Bot,19 Nov 2026),
**peringkat4** (footage bergerak LEMAH — tidak ada klip bebas; diselesaikan
dengan footage bank atmosferik + AI still, sesuai pola EP05–EP07). Format:
adaptasi ODDCHAPTER8 beat.

**VO = VO PEMILIK, dipakai apa adanya** (Drive `ponari-antrean/vo` →
`vo_owner/vo_ponari-antrean.mp3`, **78,81 s,152 kata**, ElevenLabs "Riri Rida -
Documentary & News", alignment faster-whisper). Naskah = transkrip VO; perubahan
hanya perbaikan caption.

END video **82,90 s (1:23)** — durasi bebas1–3 menit.

## Sudut pandang (dari shortlist — wajib dijaga)

Bukan mengejek keyakinan orang miskin. Inti: **antrean yang tidak berhenti
justru setelah praktiknya ditutup** — pengangguran disebut70%, berobat ke
dokter mahal; pertanyaan penutup membalik: "kalau bukan ke sana, mereka harus
ke mana?" Ponari = **korban eksploitasi lingkungan** (anak-anak saat itu;
Komnas Perlindungan Anak pernah menegur). Nada: hormat pada korban (4+1
meninggal), tanpa menyebut nama korban (sumber tidak sepakat), tanpa nada
mengejek.

## Peta beat → waktu mulai (dari vo_owner/vo_alignment.json)

| Beat | Fungsi | Mulai |
|---|---|---|
| B1 | Dilema — puluhan ribu nomor antrean, segelas air + sebuah batu | 0,00 |
| B2 | Reaksi — Jombang2009, Ponari9 tahun, batu tersambar petir | 6,72 |
| B3 | Pertaruhan — Balongsari penuh sesak, gelas & botol, dua hari menunggu | 21,54 |
| B4 | Tindakan Mengagetkan — kerumunan menelan korban:4 meninggal, polisi tutup | 33,34 |
| B5 | Tekanan — tidak pulang; ribuan tetap menunggu; air sumur & air mandi | 41,00 |
| B6 | Tekanan — Kenapa? pengangguran70%, berobat mahal | 52,64 |
| B7 | Hasil & Fakta — akhir Maret, korban kelima (pemuda19, kelelahan) | 61,86 |
| B8 | Interactive Debate Hook — "mereka harus ke mana?" | 69,14 (selesai78,40) |

## Teks VO (transkrip pemilik — sumber caption)

> Puluhan ribu nomor antrean. Setiap hari. Untuk segelas air yang dicelup
> sebuah batu. Jombang, Jawa Timur, awal dua ribu sembilan. Muhammad Ponari,
> sembilan tahun, konon menemukan sebuah batu setelah tersambar petir. Air
> celupan batu itu, kata orang, bisa menyembuhkan. Dalam hitungan hari, desa
> kecil Balongsari penuh sesak. Orang datang dari berbagai kota membawa gelas
> dan botol. Ada yang menunggu dua hari, tidur di rumah warga. Lalu kerumunan
> itu menelan korban. Empat orang meninggal di tengah desakan. Polisi menutup
> praktiknya. Tapi orang-orang tidak pulang. Ribuan tetap menunggu di luar.
> Ada yang minum air sumur di depan rumah itu. Ada yang menadah air bekas mandi
> sang anak. Kenapa? Di desa itu, pengangguran disebut mencapai tujuh puluh
> persen. Dan berobat ke dokter... mahal. Akhir Maret, korban kelima meninggal.
> Seorang pemuda sembilan belas tahun, yang kelelahan menunggu. Orang bertanya,
> kenapa mereka percaya pada sebuah batu? Mungkin pertanyaan yang lebih
> jujur... kalau bukan ke sana, mereka harus ke mana?

## Perbaikan caption (bukan perubahan ucapan)

- `antrian antrian` (duplikat ASR) → **antrean** — `MERGE`.
- `orang -orang` → **orang-orang** — `MERGE`.
- `Empat` → **4** — `NUM_PHRASES` (2009,9,70,19 sudah digit di alignment).
- `KEYWORDS` merah: PONARI,2009,4,70.

## Aksesori produksi

- `work/ponari-antrean/`: `vo_owner/` (mp3 + alignment + text + settings),
 `vo_alignment.json` salinan, `footage/` → symlink bank.
- **Aturan baru (21 Nov2026)**: semua klip16:9 dirender **cover-crop full
 layar9:16** (default `clip_filter()` — tanpa `window`).
- AI still (tanpa orang): `img/stone_glass.jpg` (batu dalam gelas),
 `img/village_lane.jpg` (gang desa senja), `img/well_water.jpg` (sumur desa).
- Footage bank: kerumunan (crowd×2), hujan malam, koridor gelap, lilin
 (memorial), mata, katedral, koran, surat, kota malam, bayangan jalan,
 koper/menunggu (sb-ep02, tema "datang dari kota"), dermaga (penutup).
- Klip tak-valid bank tidak dipakai; tanpa `footage_risiko/`.

## Sumber fakta (shortlist — sudah diverifikasi Angker Bot)

- ANTARA — kronologi & korban (4 tewas terinjak; korban kelima29 Mar2009)
- Inside Indonesia — "Ponari and the Sorcerer's Stone" (eksploitasi anak,
 tarif, dampak sekolah)
- Liputan6 — antusiasme warga, komentar antropolog Unair (jimat & kesehatan
 mahal)
- Catatan angka: tarif Rp1.000–5.000 (konflik sumber — VO tidak menyebut);
 tanggal sambaran petir konflik (VO hanya "awal2009")

## Pemeriksaan editorial

- Tanpa nama korban; tanpa foto jenazah/TKP; tanpa nada mengejek.
- Ponari diperlakukan sebagai anak yang dieksploitasi, bukan pelaku.
- Footage stok + label di layar + kredit di kartu akhir dan deskripsi.
- VO pemilik dipakai apa adanya.
