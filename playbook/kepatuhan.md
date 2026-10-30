# Kepatuhan & etika

Dokumen operasional, bukan nasihat hukum. Ditinjau ulang setiap kuartal.

> **Konteks baru:** tidak ada karakter manusia, tidak ada wajah AI, tidak ada
> lipsync. Yang ada: narasi suara sintetis + motion graphics + gambar AI.
> Ini **menurunkan** risiko (tidak ada persona palsu), tapi tidak menghapus
> kewajiban disclosure dan tidak menghapus aturan klaim.

---

## 1. Label & disclosure

| Platform | Kewajiban | Cara |
|---|---|---|
| **YouTube** | *Altered content*: wajib bila ada suara/visual sintetis yang realistis | toggle saat upload → "Altered content → Yes" |
| **TikTok** | Label konten AI untuk visual realistis hasil AI | toggle "AI-generated content" + caption `dibuat dengan bantuan AI` |
| **Instagram/Meta** | Label untuk konten AI; profil AI wajib label | aktifkan label AI pada post; bio memuat `narasi AI` |
| **Caption/deskripsi** | Transparansi kita sendiri | satu baris tetap: `Bukan saran medis · narasi & grafik dibuat dengan bantuan AI · tidak ada afiliasi tersembunyi` |

Aturan internal: **lebih baik menyebut AI dua kali daripada sekali** — kepercayaan
audiens lebih murah daripada krisis "ketahuan".

---

## 2. Klaim kesehatan & kecantikan (beauty)

| Dilarang | Contoh | Ganti dengan |
|---|---|---|
| Klaim menyembuhkan | "menyembuhkan jerawat" | "membantu mengurangi tampilan jerawat" (dan hanya bila ada sumber) |
| Klaim absolut | "pasti memutihkan" | "beberapa studi menunjukkan..." |
| Angka tanpa sumber | "97% pengguna puas" | sertakan sumber & ukuran sampel, atau hapus |
| Before-after palsu | foto "hasil 3 hari" | tidak dipakai sama sekali |
| Menyerang merek | "produk X berbahaya" | jelaskan mekanisme bahan, tanpa menyebut merek |

Tambahan: produk dengan klaim obat (acne treatment, whitening dengan hidrokuinon)
**tidak boleh diulas** tanpa registrasi BPOM yang jelas.

---

## 3. Klaim psikologis (relationship)

1. **Bukan terapi.** Cantumkan di bio & deskripsi channel.
2. **Tidak mendiagnosis.** Tulis "pola", bukan "dia narsis/borderline".
3. **Kekerasan domestik:** hentikan analisis, arahkan ke layanan profesional
   (LISA 129, psikolog klinis, Puskesmas). Jangan pernah menyarankan "coba hadapi dulu".
4. **Riset** disebut dengan penulis + tahun; jangan mengarang angka.
5. **Tidak ada generalisasi gender** ("semua pria...", "wanita selalu...").

---

## 4. Afiliasi & iklan

- Setiap video berisi produk afiliasi: tulis `#afiliasi` di caption **dan** sebut
  di VO ("ini tautan afiliasi").
- Tidak ada afiliasi untuk produk yang belum diuji tim.
- Brand deal: tulis `#kerjasama` + nama brand di 2 baris pertama deskripsi.
- Hadiah produk gratis tetap dianggap kerja sama.

---

## 5. Hak cipta & musik

- Semua musik/SFX **disintesis sendiri** (`audio_build.py`), tidak memakai track
  platform. Ini menghindari takedown dan masalah lisensi di monetisasi.
- Gambar AI: simpan prompt & model di `content/media/<ID>.json` untuk bukti orisinalitas.
- Tidak memakai klip milik orang lain, termasuk "reaction" yang memuat video utuh.

---

## 6. Data penonton & komentar

- Tidak menyimpan data pribadi pengikut di repo.
- Cerita pengikut hanya dipakai dengan izin tertulis + anonimisasi.
- Komentar yang menyebut kekerasan/krisis dijawab dengan arahan layanan, bukan analisis.

---

## 7. Hal yang harus ditinjau ulang tiap kuartal

- [ ] Perubahan kebijakan label AI (Meta, TikTok, YouTube)
- [ ] Perubahan aturan afiliasi (TikTok Shop, Shopee)
- [ ] Permendag 19/2026 & aturan PMSE terkait konten AI
- [ ] Regulasi BPOM untuk produk yang diulas
