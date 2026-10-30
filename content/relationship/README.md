# Knot Theory — slate v1

Tujuh topik, tujuh wilayah, tujuh struktur. **Satu topik per hari → tiga video**, satu
untuk tiap platform, dengan format dan hook yang berbeda. Total 21 video dalam 7 hari.

Aturan menulis: [`docs/05-editorial-bible.md`](../../docs/05-editorial-bible.md).
Identitas & merek: [`docs/01-brand/relationship.md`](../../docs/01-brand/relationship.md) ·
[`docs/01-brand/knot-theory-brand.md`](../../docs/01-brand/knot-theory-brand.md).
Aset logo/banner: `brand/knot-theory/assets/`.

```bash
python3 automation/validate_pieces.py     # QC slate ini
```

---

## 1. Cara tiga video itu dibuat dari satu topik

Bukan satu video diunggah tiga kali. Satu topik punya **satu set bukti** (fact ledger di
tiap naskah) dan **tiga potongan** yang berbeda bentuk:

| | YouTube | TikTok | Instagram Reels |
|---|---|---|---|
| Panjang | 8–10 menit | 55–75 dtk | 45–60 dtk |
| Isi | argumen utuh: adegan → bukti → batas → pertanyaan | satu temuan + satu mekanisme | satu proposisi, visual dulu |
| Hook | **adegan**: tempat, tahun, atau angka yang spesifik | **ketegangan**: ada yang belum selesai | **proposisi**: satu kalimat yang terbaca tanpa suara |
| Teks | judul + sumber di deskripsi | satu angka besar per adegan | teks layar besar, ≥60% frame |
| Akhir | pertanyaan yang butuh 8 menit untuk dijawab | potong tanpa kesimpulan | satu kalimat yang bisa disimpan |
| Caption | deskripsi panjang + sumber + batas data | 1–3 baris, hashtag topik | cerita 4–6 baris, tanpa hashtag berlebihan |

Uji cepat: **kalau hook TikTok bisa ditempel ke Reels tanpa diubah, berarti belum
diadaptasi.** Tiga hook harus berbeda bentuk, bukan tiga versi kalimat yang sama.

---

## 2. Slate

| Hari | Tanggal | Kode | Topik | Wilayah | Struktur | YT | TikTok | IG |
|---|---|---|---|---|---|---|---|---|
| 1 | Sen 2026-11-09 | RW1 | Orang yang paling bagus menjual jadi manajer termahal | C kerja | S1 | 8:30 | 78 dtk | 52 dtk |
| 2 | Sel 2026-11-10 | IN1 | Satu dari 260 orang yang kamu kenal | E institusi | S2 | 9:00 | 82 dtk | 55 dtk |
| 3 | Rab 2026-11-11 | FR1 | Persahabatan jarang berakhir, ia berhenti | B pertemanan | S3 | 8:00 | 76 dtk | 50 dtk |
| 4 | Kam 2026-11-12 | SO1 | 38 saksi yang tidak pernah ada | D masyarakat | S4 | 8:30 | 84 dtk | 58 dtk |
| 5 | Jum 2026-11-13 | NA1 | Aturan tahun 1517 yang masih dipakai | F alam | S5 | 8:00 | 80 dtk | 55 dtk |
| 6 | Sab 2026-11-14 | TE1 | Mereka berkabung untuk sebuah fitur yang dimatikan | G teknologi | S6 | 9:00 | 86 dtk | 58 dtk |
| 7 | Min 2026-11-15 | EC1 | Uang yang jaminannya bukan hukum, tapi rasa malu | I ekonomi | S7 | 8:00 | 80 dtk | 55 dtk |

Berkas naskah: `pieces/{KODE}-*.md`. Naskah short di dalamnya adalah versi TikTok;
potongan Instagram diambil dari naskah yang sama dengan memotong bagian tengah dan
mengganti hook (lihat §3); outline long-form adalah kerangka YouTube.

---

## 3. Tiga hook per topik

Diambil dari varian yang sudah ada di tiap naskah, tapi ditulis ulang agar bentuknya
berbeda per platform. **Yang dipakai hook A di TikTok belum tentu hook A di Reels.**

| Kode | TikTok (ketegangan) | Instagram (proposisi) | YouTube (adegan) |
|---|---|---|---|
| RW1 | "Perusahaan ini tahu penjual terbaiknya jadi manajer buruk. Mereka tetap melakukannya." | "Naik jabatan dan menjadi atasan itu dua pekerjaan berbeda. Yang satu dipakai untuk memilih yang lain." | "131 perusahaan, 38.843 tenaga penjualan, 1.553 promosi. Yang dipromosikan adalah yang penjualannya tertinggi — dan timnya kemudian menjual lebih sedikit." |
| IN1 | "Satu dari 260 orang yang kamu kenal mungkin sedang mencatat apa yang kamu bilang." | "Pengawasannya berakhir. Ketidakpercayaannya tidak." | "Di Jerman Timur pada 1980-an, 0,38 persen penduduk tercatat sebagai informan resmi. Tiga dekade setelah negaranya bubar, tetangganya masih tidak saling percaya." |
| FR1 | "Persahabatanmu tidak berakhir. Ia berhenti — dan tidak ada yang memutuskan." | "Tidak ada pertengkaran. Hanya dua orang yang berhenti punya alasan untuk bertemu." | "1990: tiga persen orang Amerika menjawab mereka tidak punya teman dekat. 2021: dua belas persen. Tidak ada yang memutuskan apa pun di antara kedua angka itu." |
| SO1 | "38 orang melihat dan tidak ada yang menolong. Itu tidak pernah terjadi." | "Cerita yang salah bisa bertahan enam puluh tahun kalau ia berguna." | "Pada 13 Maret 1964, New York Times menulis satu artikel tentang pembunuhan di depan 38 saksi. Enam dekade kemudian, hampir setiap detailnya sudah direvisi." |
| NA1 | "Ada aturan tertulis dari tahun 1517 yang masih dipakai hari ini. Isinya satu kalimat." | "Hak memakai diikat ke kewajiban merawat. Di satu desa, ikatan itu bertahan lima abad." | "Di Valais, Swiss, sekitar 600 orang mengelola padang dan hutan bersama. Aturan tertulisnya lebih tua daripada negara Swiss." |
| TE1 | "Mereka berkabung untuk sebuah fitur yang dimatikan." | "Yang berakhir bukan aplikasinya. Yang berakhir adalah orang yang mereka kenal." | "3 Februari 2023: otoritas Italia memerintahkan penghentian pemrosesan data. Dalam hitungan jam, pengguna di seluruh dunia kehilangan sesuatu yang bukan fitur." |
| EC1 | "Bunga nol persen. Tanpa kontrak. Tanpa agunan. Dan tetap jalan puluhan tahun." | "Jaminannya bukan hukum. Jaminannya adalah kamu akan bertemu orang itu lagi bulan depan." | "Sekitar 29 persen orang dalam sampel survei rumah tangga Indonesia ikut setidaknya satu arisan. Tidak ada bunga, tidak ada kontrak, tidak ada agunan." |

Aturan tambahan untuk hook YouTube: **jangan buka dengan tesis.** Buka dengan tempat,
tahun, atau angka — biarkan penonton menunggu 40 detik pertama untuk tahu mengapa itu
penting.

---

## 4. Jadwal tayang (WIB)

| Platform | Jam | Alasan |
|---|---|---|
| TikTok | 11:45 | konsumsi cepat di jam makan siang |
| Instagram | 20:00 | prime time, simpan & share |
| YouTube | 21:30 | penonton siap menonton 8 menit |

Jamnya sengaja tidak sama supaya caption tidak pernah terposting serentak, dan supaya
komentar di satu platform bisa dipakai memperbaiki hook di platform berikutnya di hari
yang sama.

---

## 5. Beban produksi — baca ini sebelum mulai

3 video/hari = **21 video/7 hari**, dengan 7 di antaranya video 8–10 menit yang
masing-masing butuh 1 sumber primer baru. Itu bukan beban yang sama dengan 21 short.

Urutan yang realistis:

| Minggu | Output | Catatan |
|---|---|---|
| 1 | 7 TikTok + 7 Reels (short), **3 YouTube** | long-form dibuat untuk topik terkuat dulu; 4 sisanya ditunda, bukan dipaksa |
| 2 | +4 YouTube dari topik sisa | short sudah tayang, komentarnya dipakai memperbaiki naskah panjang |
| 3 | siklus penuh 3/hari | hanya kalau batch pertama lolos QC tanpa revisi besar |

Kalau pemilik kanal ingin 3 video/hari di **setiap** platform sejak hari pertama
(9 video/hari), itu butuh penulis/riset tambahan — bukan penambahan jam kerja. Naskah
dengan bukti primer tidak bisa dipercepat dengan cara itu.

---

## 6. QC

`automation/validate_pieces.py` memeriksa:

- 7 naskah, id unik, tanggal berurutan dari `startDate`
- struktur tidak berulang, bentuk hook unik, wilayah primer unik
- tiap berkas: durasi cocok dengan indeks, "Kenapa ini layak", fact ledger, ≥1 `FAKTA`,
  ≥1 baris `TIDAK-DIKETAHUI`, sumber yang bisa dicek
- tiga varian hook A/B/C
- caption TikTok ≠ Instagram, judul YouTube ≤ 60 karakter
- frasa terlarang (editorial bible §4) tidak muncul

Yang tetap harus dibaca manusia:

1. Angka di naskah cocok dengan sumber aslinya.
2. Kalimat terakhir pertanyaan asli, bukan kesimpulan yang menyamar.
3. Tidak ada kalimat yang bisa dipindah ke naskah lain tanpa berubah.
4. Tiga hook satu topik benar-benar berbeda bentuk (validator hanya cek varian, bukan bentuk).

---

## 7. Hubungan dengan slate M2

`content/scripts.json` (35 konten, 105 draf, mulai 2026-11-02) adalah slate M2 yang
sudah ter-commit. Hashtag relationship-nya sudah diganti `#knottheory`, kalender
diregenerasi dan lolos `validate.py`. Isi naskahnya **tidak** diubah — 14 naskah lama
itu tetap memakai standar M2, bukan standar editorial bible.

Konsekuensi yang perlu diputuskan: minggu 1 (2–8 Nov) masih memakai 14 naskah tersebut,
sementara standar baru mulai 9 Nov. Pilihannya: kosongkan slot relationship minggu itu,
atau jalankan sebagai arsip dengan catatan standar baru berlaku 9 Nov.
