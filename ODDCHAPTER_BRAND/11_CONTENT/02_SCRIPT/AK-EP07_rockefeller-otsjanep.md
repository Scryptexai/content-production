# AK-EP07 — Michael Rockefeller & Otsjanep (naskah = VO pemilik)

Sumber ide: Drive `ODDCHAPTER Shortlist Batch 2` (usulan Angker Bot,19 Nov 2026),
**peringkat3** (peringkat2 Heaven's Gate tidak punya VO pemilik → dilewati
sesuai aturan "VO pemilik wajib untuk item Drive"). Format: adaptasi ODDCHAPTER
8 beat (`00F_FORMAT_CURIOSITY_LOOP.md` §2).

**VO = VO PEMILIK, dipakai apa adanya** (Drive `rockefeller-otsjanep/vo` →
`vo_owner/vo_rockefeller-otsjanep.mp3`, **103,70 s,186 kata**, ElevenLabs
"Riri Rida - Documentary & News", alignment faster-whisper). Naskah di bawah =
transkrip VO; perubahan hanya perbaikan caption (lihat §Perbaikan caption).

END video **107,80 s (1:48)** — durasi bebas1–3 menit.

## Sudut pandang (dari shortlist — wajib dijaga)

Bukan versi "dimakan kanibal". Inti cerita: **kolonialisme & laporan yang
dikubur** — tahun1958 tentara kolonial menembak5 warga Otsjanep;1961 laporan
misionaris menyebut kematian Rockefeller sebagai balas dendam; laporan itu
dikubur demi citra Belanda. Nada: menghormati semua pihak (keluarga Rockefeller,
warga Otsjanep, korban1958). Tanpa sensasi, tanpa detail kanibalisme, tanpa
foto jenazah.

## Peta beat → waktu mulai (dari vo_owner/vo_alignment.json)

| Beat | Fungsi | Mulai |
|---|---|---|
| B1 | Dilema Ekstrem — tiga titik di laut: dua jeriken, satu kepala | 0,00 |
| B2 | Reaksi Alami — Michael Rockefeller,23, putra Gubernur NY, Nov1961 | 9,64 |
| B3 | Pertaruhan — pencarian besar,10 hari, tak ada jasad, "tenggelam" | 24,78 |
| B4 | Tindakan Mengagetkan — pengakuan warga Otsjanep: ia dibunuh | 43,26 |
| B5 | Tekanan —5 pria Otsjanep ditembak polisi kolonial, dendam lama | 54,32 |
| B6 | Tekanan — laporan ditulis, dikirim, lalu dikubur (Carl Hoffman) | 68,62 |
| B7 | Hasil & Fakta — tanpa bukti; meninggal hukum1964 | 83,06 |
| B8 | Interactive Debate Hook — "siapa yang lebih nyaman dengan jawaban, tenggelam?" | 96,10 (selesai103,26) |

## Teks VO (transkrip pemilik — sumber caption)

> Seorang pemuda Amerika berenang menuju pantai Papua. Rekannya hanya sempat
> melihat tiga titik di permukaan laut... dua jeriken, dan satu kepala. Michael
> Rockefeller, dua puluh tiga tahun, putra Gubernur New York. November seribu
> sembilan ratus enam puluh satu, perahunya terbalik di lepas pantai Asmat.
> Setelah sehari semalam hanyut, ia memutuskan berenang ke daratan. Belanda dan
> Australia mengirim pesawat dan helikopter. Amerika menawarkan armadanya,
> ayahnya terbang ke Merauke. Sekitar sepuluh hari kemudian, pencarian
> dihentikan. Tidak ada jasad. Kabar resminya: tenggelam, atau diserang hewan
> laut. Tapi sebulan kemudian, seorang misionaris Belanda menerima pengakuan
> dari beberapa warga desa Otsjanep. Menurut mereka, Michael tidak tenggelam.
> Ia dibunuh. Alasannya, kata para misionaris, bukan soal Michael. Beberapa
> tahun sebelumnya, polisi kolonial Belanda menembak mati lima pria Otsjanep.
> Dan Michael datang ke desa yang masih menyimpan dendam. Laporan itu ditulis,
> dikirim, dan... tenggelam. Menurut wartawan Carl Hoffman, yang menelusuri
> kasus ini puluhan tahun kemudian, laporan itu dikubur. Belanda tak mau
> citranya di Papua rusak. Tidak ada bukti yang pernah menjawabnya. Keluarga
> Rockefeller tetap meyakini ia tenggelam. Michael dinyatakan meninggal secara
> hukum pada tahun seribu sembilan ratus enam puluh empat. Pertanyaannya bukan
> lagi, apa yang terjadi di laut... Tapi siapa yang lebih nyaman dengan
> jawaban, tenggelam?

## Perbaikan caption (bukan perubahan ucapan)

- `jerikan` → **jeriken** (ASR) — `WORD_FIX`.
- `misyonaris` → **misionaris** (2×) — `WORD_FIX`.
- `Otsjaneb` → **Otsjanep** (2×) — `WORD_FIX`.
- `Karl` → **Carl**, `Hofmann` → **Hoffman** — `WORD_FIX`.
- `sepuluh hari` → **10 hari**, `lima pria` → **5 pria** — `NUM_PHRASES`
 (23,1961,1964 sudah digit di alignment pemilik).
- `KEYWORDS` merah: ROCKEFELLER, OT SJANEP → **OTSJANEP**, 1961,1964.

## Aksesori produksi

- `work/rockefeller-otsjanep/`: `vo_owner/` (mp3 + alignment + text + settings
 pemilik), `vo_alignment.json` (salinan untuk builder), `footage/` → symlink
 bank (root + `sb-ep02/` laut/pantai/kapal/pesawat — tema laut cocok; `sb-ep02`
 dipakai untuk B1–B3, B7–B8).
- AI-generated dipakai untuk thumb/poster (tanpa orang). Klip tak-valid bank
 (nama ≠ isi) tidak dipakai. **Tidak memakai5 mp4 misterius di folder Drive
 (nama = ID YouTube, provenansi/hak tak jelas → masuk kategori footage
 risiko)** — hanya Coverr/bank + AI, sesuai aturan.
- Tanpa `footage_risiko/`.

## Sumber fakta (shortlist + verifikasi)

- Wikipedia — Michael Rockefeller (peristiwa, pencarian, meninggal hukum1964)
- Carl Hoffman, *Savage Harvest* (2014) — laporan misionaris & motivasi Otsjanep
- Stichting Papua Erfgoed — kronologi pencarian (⚠ tanggal: pakai "November
 1961" mengikuti VO pemilik)
- Wikipedia — Otsjanep/Asmat (penembakan1958)

## Pemeriksaan editorial

- Tanpa sensasi kanibalisme; sudut kolonialisme & laporan yang dikubur.
- Angka korban disebut apa adanya dari VO (5 pria Otsjanep,1958).
- Footage stok + label di layar + kredit di kartu akhir dan deskripsi.
- VO pemilik dipakai apa adanya — tidak ada kalimat ditambah/dipotong.
