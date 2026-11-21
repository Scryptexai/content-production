# AK-EP06 — Jonestown / "White Night" (naskah = VO pemilik)

Sumber ide: Drive `ODDCHAPTER Shortlist Batch 2` (usulan Angker Bot, 19 Nov 2026),
**peringkat 1**. Format: adaptasi ODDCHAPTER 8 beat (`00F_FORMAT_CURIOSITY_LOOP.md` §2)
— sudah terbukti di AK-EP05 (uji format tayang 20 Nov 2026).

**VO = VO PEMILIK, dipakai apa adanya** (Drive `jonestown-whitenight/vo` →
`vo_owner/vo_jonestown-whitenight.mp3`, **101,15 s, 176 kata**, alignment
faster-whisper). Tidak ada TTS. Naskah di bawah = transkrip VO; perubahan hanya
perbaikan caption (lihat §Perbaikan caption), bukan perubahan ucapan.

END video **105,24 s (1:45)** — durasi bebas 1–3 menit.

## Peta beat → waktu mulai (dari vo_alignment)

| Beat | Fungsi | Mulai |
|---|---|---|
| B1 | Tantangan Logika / Dilema Ekstrem — "Sebelum 918 orang…" | 0,00 |
| B2 | Reaksi Alami Manusia — komune, Jim Jones, janji surga tropis | 11,38 |
| B3 | Tindakan Mengagetkan — sirene tengah malam, White Night | 21,90 |
| B4 | Pertaruhan Nyawa — antre, gelas cairan merah,45 menit | 37,84 |
| B5 | Tekanan Situasi —45 menit berlalu, tes kesetiaan | 55,26 |
| B6 | Tekanan Situasi — sumpah Deborah Leighton, menuju18 Nov | 67,98 |
| B7 | Hasil Akhir & Fakta Kunci —918 /909, menguji patuh | 84,18 |
| B8 | Interactive Debate Hook — "kamu akan berhenti di mana?" | 97,72 (selesai 101,15) |

## Teks VO (transkrip pemilik — sumber caption)

> Sebelum918 orang meninggal di Guyana, mereka sudah pernah disuruh minum racun,
> dan semuanya meminumnya, namanya Jonestown. Komune di tengah hutan, dipimpin
> pendeta Jim Jones. Hampir seribu orang Amerika pindah ke sana, dijanjikan surga
> tropis jauh dari dunia luar. Tapi ada satu kebiasaan, menurut mantan anggota,
> hampir setiap minggu, sirene meraung tengah malam. seluruh warga dibangunkan.
> Penjaga bersenjata berjaga di sekeliling. Jones menyebutnya White Night. Pada
> satu malam, semua orang, termasuk anak-anak, disuruh antre. Masing-masing
> menerima segelas kecil cairan merah. Katanya, itu racun dan mereka akan mati
> dalam45 menit. Mereka meminumnya, lalu menunggu. Empat puluh lima menit
> berlalu, tak seorang pun jatuh. Jones berkata, itu bukan racun, itu tes
> kesetiaan, dan waktunya, katanya, sudah dekat. Kisah ini tertulis dalam
> pernyataan di bawah sumpah Deborah Leighton, mantan anggota yang kabur. Pada
> Juni1978, lima bulan kemudian,18 November, tidak ada lagi latihan.918 orang
> meninggal hari itu.909 diantaranya di Jonestown. Latihan itu tidak menguji
> racunnya, tapi menguji sampai di mana mereka akan patuh. Kalau kamu ada di
> sana, kamu akan berhenti di mana?

## Perbaikan caption (bukan perubahan ucapan)

- `Johnstown` → **Jonestown** (ASR salah dengar;2 kemunculan) — `WORD_FIX`.
- `seluruh` (setelah titik) → `Seluruh` — `WORD_FIX`.
- `anak -anak` → `anak-anak`, `Masing -masing` → `Masing-masing` — `MERGE`.
- `Empat puluh lima` → `45` — `NUM_PHRASES` (angka sudah digit di tempat lain:
 918,909,45,18,1978).
- `KEYWORDS` merah: JONESTOWN, WHITE, NIGHT, 918,909,45.

## Aksesori produksi

- `work/jonestown-whitenight/`: `vo_owner/` (mp3 + alignment pemilik),
 `vo_alignment.json` (salinan untuk builder), `footage/` → symlink bank
 `footage/` (42 klip; yang dipakai hanya klip tematik: lilin, katedral, hutan
 kabut, kerumunan, koridor gelap, bulan malam, hujan jendela, surat/tulisan,
 koran, buku, patung Liberty, mata, asap, kota malam, jalan bayangan).
- Klip yang TIDAK dipakai: berkas dengan nama tidak cocok isinya
 (gavel/seal_wax/printing_press/wooden_table/stack-boots), ikonografi tak
 relevan (koin, tangga, fountain), modern (press conference), dan salju
 (`remnants-of-snow` — Guyana hutan tropis).
- Tanpa `footage_risiko/` (direktori tidak ada). Hanya Coverr Free License +
 AI-generated yang sudah berada di bank.

## Sumber fakta

- Wikipedia — Peoples Temple / Jonestown (918 total;909 di Jonestown;18 Nov 1978)
- Deborah Layton, *Seductive Poison* (1998) — pernyataan di bawah sumpah
 (affidavit Juni1978)
- Jonestown Institute (jonestowninstitute.org) — arsip
- California Historical Society — arsip CHS (disebut CATATAN batch2)

## Pemeriksaan editorial (aturan episode ini — dari CATATAN batch2)

- **Tanpa gore, tanpa metode rinci, tanpa foto jenazah/TKP.** Angka korban
 hanya918 /909 (disebut apa adanya dari VO pemilik).
- Nada menghormati korban; latihan "White Night" sebagai inti cerita, bukan
 sensasi. Tanpa teori konspirasi.
- Footage stok + label di layar + kredit di kartu akhir dan deskripsi.
- VO pemilik dipakai apa adanya — tidak ada kalimat yang ditambah/dipotong.
