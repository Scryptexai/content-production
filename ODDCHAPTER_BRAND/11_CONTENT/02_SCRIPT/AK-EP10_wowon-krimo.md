# AK-EP10 — Wowon Krimo: pengganda uang yang menelan9 nyawa (naskah = VO pemilik)

Sumber ide: Drive `ODDCHAPTER Shortlist Batch 2` (usulan Angker Bot,19 Nov2026),
**cadangan B1** — dipilih setelah5 besar tayang; paling dekat dengan formula
Dukun AS (dukun + kepercayaan + banyak korban). Format: adaptasi ODDCHAPTER8
beat.

**VO = VO PEMILIK, dipakai apa adanya** (Drive `wowon-krimo/vo` →
`vo_owner/vo_wowon-krimo.mp3`, **85,31 s,159 kata**, ElevenLabs "Riri Rida -
Documentary & News", alignment faster-whisper). Naskah = transkrip VO;
perubahan hanya perbaikan caption.

END video **89,40 s (1:29)** — durasi bebas1–3 menit.

## Sudut pandang & sensitivitas (wajib dijaga)

Sudut: **jarak antara janji "uang berlipat" dan korban yang menagih** — bukan
kengerian metode. Aturan episode (shortlist B1):
- **Pelaku masih hidup → gunakan bahasa "terdakwa / divonis"** (VO sudah:
 "tiga pelaku divonis penjara seumur hidup" ✓).
- **Rawan gore**: tanpa detail metode, tanpa foto jenazah/TKP, tanpa menyebut
 lokasi kuburan/korban per korban.
- Tanpa nama korban. Nada hormat pada korban (termasuk11 pekerja migran yang
 menyetor bertahun-tahun — mereka korban penipuan, bukan "terlalu percaya").
- Vonis: **1 Nov2023 — Wowon Erawan, Solihin (Duloh), Dede Solehudin divonis
 seumur hidup, lolos dari tuntutan mati** (Tempo) ✓ konsisten dengan VO.

## Peta beat → waktu mulai (dari vo_owner/vo_alignment.json)

| Beat | Fungsi | Mulai |
|---|---|---|
| B1 | Dilema — Rp1.000 jadi Rp5.000;9 orang kehilangan nyawa | 0,00 |
| B2 | Reaksi — Wowon Erawan, dalang suara; tokoh Aki Banyu | 8,44 |
| B3 | Tindakan Mengagetkan — Aki Banyu hanya lewat telepon; ternyata Wowon sendiri | 16,14 |
| B4 | Pertaruhan —11 pekerja migran perempuan menyetor bertahun-tahun; diancam | 36,24 |
| B5 | Tekanan — penagih "dihabisi"; keluarga yang mengganggu | 51,58 |
| B6 | Hasil — November2023, vonis seumur hidup (jaksa tuntut mati) | 60,26 |
| B7 | Fakta — kriminolog: korban lebih dari9; tak pasti | 68,62 |
| B8 | Interactive Debate Hook — "percaya janji yang tidak bisa kamu cek?" | 74,26 (selesai84,96) |

## Teks VO (transkrip pemilik — sumber caption)

> Seribu rupiah masuk amplop. Dibuka, jadi lima ribu. Dari trik murahan
> inilah, sembilan orang kehilangan nyawa. Pelakunya, Wowon Erawan, seorang
> dalang yang pandai mengubah suara. Ia menciptakan satu tokoh: Aki Banyu.
> Sosok sakti penghuni dasar laut, yang menjanjikan siapa pun yang menurut
> akan sukses dan kaya. Aki Banyu tidak pernah menunjukkan diri. Ia hanya
> bicara lewat telepon. Dan ternyata... Aki Banyu adalah Wowon sendiri. Dua
> rekannya baru tahu setelah ditangkap. Korbannya, sebelas pekerja migran
> perempuan. Mereka menyetor uang setiap bulan, bertahun-tahun, dari luar
> negeri. Tak satu pun menerima untung. Yang bertanya, diancam: kamu akan
> celaka. Menurut polisi, korban yang menagih janji itu dihabisi. Begitu pula
> anggota keluarga sendiri yang dianggap mengganggu. November dua ribu dua
> puluh tiga, tiga pelaku divonis penjara seumur hidup. Jaksa menuntut hukuman
> mati. Seorang kriminolog menduga korbannya lebih dari sembilan. Tak ada yang
> tahu pasti. Aki Banyu tidak pernah ada. Yang ada hanya orang-orang yang
> butuh percaya. Kapan terakhir kali kamu percaya pada janji... yang tidak
> bisa kamu cek?

## Perbaikan caption (bukan perubahan ucapan)

- `Wawon` → **Wowon** (2×) — `WORD_FIX`.
- `menguara` → **mengubah suara** — `WORD_FIX`.
- `akibanyu` → **Aki Banyu**; `Akibatnya` (salah dengar di P8) → **Aki Banyu**
 — `WORD_FIX`.
- `Pelakunyanya` → **pelakunya**; `difonis` → **divonis** — `WORD_FIX`.
- `di ancam` → **diancam**; `bertahun -tahun` → **bertahun-tahun** — `MERGE`.
- `Rp. 1 .000` → **Rp1.000**; `Rp. 5 .000` → **Rp5.000** — `NUM_PHRASES`
 (9,11,2023 sudah digit di alignment).
- `KEYWORDS` merah: WOWON, BANYU,9,11.

## Aksesori produksi

- `work/wowon-krimo/`: `vo_owner/` (mp3 + alignment + text + settings),
 `vo_alignment.json` salinan, `footage/` → symlink bank.
- **Aturan21 Nov2026**: semua klip16:9 **cover-crop full layar9:16**.
- AI still (tanpa orang): `img/amplop_meja.jpg` (amplop & uang di meja),
 `img/phone_dark.jpg` (telepon kabel gelap), `img/aki_banyu_sea.jpg` (laut
 malam berkabut — motif Aki Banyu).
- Footage bank: bayangan, huruf/catatan, mata, koridor, asap, hujan malam,
 kabut hutan, koran, buku, potret, kota malam; `sb-ep02` (bandara/naik
 pesawat = pekerja migran; laut & kapal = motif janji menjauh).
- Klip tak-valid tidak dipakai; tanpa `footage_risiko/`; **tanpa footage
 berita TV** (berhak cipta).

## Sumber fakta (shortlist B1 — diverifikasi Angker Bot)

- Tempo — "Tiga terdakwa kasus Wowon … divonis penjara seumur hidup"
 (1 Nov2023, lolos tuntutan mati)
- BBC Indonesia — laporan kasus
- detik — daftar9 korban (Bekasi3, Cianjur5, Garut1)
- ⚠ Angka: VO menyebut9 (kehilangan nyawa),11 (pekerja migran menyetor),
 "lebih dari9" (kriminolog) — ketiganya punya dasar; jangan tambah angka lain.

## Pemeriksaan editorial

- Bahasa "terdakwa/divonis"; pelaku hidup; tanpa spekulasi vonis lain.
- Tanpa detail metode pembunuhan, tanpa foto jenazah, tanpa lokasi kuburan.
- Tanpa nama korban. Footage stok + label di layar + kredit di deskripsi.
- VO pemilik dipakai apa adanya.
