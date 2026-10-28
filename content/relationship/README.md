# Ruang Antara — slate v2

Tujuh naskah, tujuh wilayah, tujuh struktur. Satu naskah per hari, tiga platform per
naskah. Ini **bukan** kumpulan ide; tiap berkas sudah berisi naskah bertimecode, fact
ledger berlabel, caption yang diadaptasi per platform, outline long-form, dan catatan
visual.

Aturan yang dipakai saat menulis ada di [`docs/05-editorial-bible.md`](../../docs/05-editorial-bible.md).
Identitas & palet ada di [`docs/01-brand/relationship.md`](../../docs/01-brand/relationship.md).

```bash
python3 automation/validate_pieces.py     # QC slate ini
```

---

## 1. Slate

| Hari | Tanggal | Kode | Naskah | Dtk | Wilayah | Struktur | Berkas |
|---|---|---|---|---|---|---|---|
| 1 | Sen 2026-11-09 | RW1 | Orang yang paling bagus menjual biasanya jadi manajer yang paling mahal | 78 | C · kerja | S1 | `pieces/RW1-promosi.md` |
| 2 | Sel 2026-11-10 | IN1 | Satu dari 260 orang yang kamu kenal | 82 | E · institusi | S2 | `pieces/IN1-satu-dari-260.md` |
| 3 | Rab 2026-11-11 | FR1 | Persahabatan jarang berakhir. Ia berhenti. | 76 | B · pertemanan | S3 | `pieces/FR1-teman-yang-berhenti.md` |
| 4 | Kam 2026-11-12 | SO1 | 38 saksi yang tidak pernah ada | 84 | D · masyarakat | S4 | `pieces/SO1-38-saksi.md` |
| 5 | Jum 2026-11-13 | NA1 | Aturan tahun 1517 yang masih dipakai | 80 | F · alam | S5 | `pieces/NA1-aturan-1517.md` |
| 6 | Sab 2026-11-14 | TE1 | Mereka berkabung untuk sebuah fitur yang dimatikan | 86 | G · teknologi | S6 | `pieces/TE1-mereka-berkabung.md` |
| 7 | Min 2026-11-15 | EC1 | Uang yang jaminannya bukan hukum, tapi rasa malu | 80 | I · ekonomi | S7 | `pieces/EC1-jaminannya-kelompok.md` |

Total 566 detik naskah → 21 draf (7 naskah × 3 platform).

---

## 2. Peta wilayah

Spektrum A–I dari brand brief. Yang jadi **wilayah primer**:

```
A  romantis            — (sekunder di TE1)
B  keluarga/pertemanan — FR1
C  kerja & karier      — RW1
D  masyarakat          — SO1
E  politik/institusi   — IN1
F  manusia & alam      — NA1
G  manusia & teknologi — TE1
H  diri sendiri        — (sekunder di FR1, TE1)
I  ekonomi & uang      — EC1
```

Wilayah A sengaja **tidak** dijadikan primer di slate pertama. Bukan karena romansa
tidak penting, tapi karena kanal ini tidak ingin dibaca sebagai akun pacaran dalam
tujuh hari pertama. Romansa masuk sebagai lapisan sekunder (TE1: kontinuitas sebagai
syarat kedekatan), bukan sebagai subjek.

Wilayah H juga belum primer: "diri sendiri" paling mudah jatuh jadi konten motivasi,
dan itu ada di daftar tolak.

---

## 3. Peta struktur

| # | Struktur | Dipakai | Ketegangan yang dipakai |
|---|---|---|---|
| S1 | studi kasus → penjelasan | RW1 | seleksi vs hadiah |
| S2 | pengamatan → konteks → konsekuensi | IN1 | keamanan vs kepercayaan |
| S3 | kontradiksi → data → mekanisme | FR1 | hilang pelan-pelan vs berakhir |
| S4 | mitos → koreksi → bukti lebih baik | SO1 | cerita yang benar vs cerita yang berguna |
| S5 | urutan sejarah → logika aturan | NA1 | hak memakai vs biaya merawat |
| S6 | peristiwa → bukti → apa yang terungkap | TE1 | kontinuitas vs pembaruan |
| S7 | mekanisme → cara bekerja → cara gagal | EC1 | jaminan sosial vs jaminan hukum |

Aturan: **tidak ada struktur yang dipakai dua kali** dalam satu slate, dan tidak boleh
sama dua kali berturut-turut lintas slate. Slate berikutnya mulai dari S1 lagi.

---

## 4. Peta hook

| Kode | Bentuk | Baris pertama |
|---|---|---|
| RW1 | temuan | "Data dari 131 perusahaan menunjukkan pola yang sulit diterima…" |
| IN1 | angka turunan | "Satu dari 260 orang yang kamu kenal…" |
| FR1 | kontradiksi | "Persahabatan jarang berakhir dengan pertengkaran." |
| SO1 | koreksi mitos | "38 orang melihat, tidak ada yang menolong. Cerita itu salah…" |
| NA1 | tanggal | "Ada aturan tertulis dari tahun 1517 yang masih dipakai…" |
| TE1 | peristiwa | "Pada Februari 2023, sebuah perusahaan mematikan satu fitur…" |
| EC1 | paradoks | "Jaminannya bukan kontrak. Jaminannya rasa malu." |

Tiap berkas punya tiga varian hook (A/B/C) untuk uji. Varian B/C boleh berbeda bentuk
dari varian A — itu tujuannya.

---

## 5. Jadwal tayang (WIB)

Satu naskah per hari, tiga platform, tiga jam berbeda:

| Platform | Jam | Alasan |
|---|---|---|
| TikTok | 11:45 | konsumsi cepat di jam makan siang |
| Instagram | 20:00 | prime time, simpan & share |
| YouTube | 21:30 | penonton siap menonton lebih lama |

Jam berbeda juga memastikan **caption tidak terposting serentak** — kalau identik,
berarti tidak ada adaptasi (lihat editorial bible §8).

Naskah dibaca sebagai satu paket: b-roll dan plate yang dipakai short bisa dipakai
ulang di long-form minggu yang sama, tapi naskahnya bukan potongan naskah yang sama.

---

## 6. Status QC

`automation/validate_pieces.py` memeriksa:

- 7 naskah, id unik, tanggal berurutan dari `startDate`
- struktur tidak berulang (dan tidak berurutan sama), bentuk hook unik, wilayah primer unik
- tiap berkas: durasi cocok dengan indeks, ada "Kenapa ini layak", fact ledger,
  minimal satu `FAKTA`, minimal satu baris `TIDAK-DIKETAHUI`, sumber yang bisa dicek
- tiga varian hook A/B/C
- caption TikTok ≠ Instagram, panjang caption wajar, judul YouTube ≤ 60
- daftar frasa terlarang (editorial bible §4) tidak muncul

Perintah: `python3 automation/validate_pieces.py` → `✓ 7 naskah · 566 dtk …`

Yang **tidak** diperiksa mesin, dan tetap harus dibaca manusia:

1. Apakah angka di naskah cocok dengan sumber aslinya (validator tidak membuka paper).
2. Apakah kalimat terakhir benar-benar pertanyaan, bukan kesimpulan yang menyamar.
3. Apakah ada satu kalimat yang bisa dipindah ke naskah lain tanpa berubah — kalau ada, potong.

---

## 7. Hubungan dengan slate lama

`content/scripts.json` (35 konten, 105 draf, mulai 2026-11-02) adalah slate M2 yang
sudah ter-commit dan terjadwal. Slate itu ditulis dengan standar lama: 2 konten
relationship/hari, salah satunya masih berbau psikologi pasangan.

Slate v2 ini **menggantikan bagian relationship** mulai 2026-11-09 dengan laju 1/hari.
Tiga konsekuensi yang perlu diputuskan pemilik kanal:

1. **Minggu 1 (2–8 Nov)** masih memakai 14 naskah relationship lama. Kalau standar baru
   berlaku surut, slot relationship minggu itu perlu dikosongkan atau diganti.
2. Laju turun dari 2/hari jadi 1/hari. Itu disengaja: naskah dengan bukti primer butuh
   riset per topik, dan 2/hari akan memaksa kembali ke pola "10 fakta".
3. Slot 21:30 yang tadinya beauty dipakai YouTube relationship. Beauty tidak kehilangan
   slot; ia berbagi hari.

Kalau keputusannya mempertahankan dua kanal berjalan paralel, `content/relationship/`
tetap bisa divalidasi sendiri tanpa menyentuh kalender beauty.
