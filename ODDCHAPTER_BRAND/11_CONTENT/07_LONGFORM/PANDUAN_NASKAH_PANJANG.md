# CETAK BIRU NASKAH PANJANG
### Format 10–30 menit · 21 episode · arah: misteri

Dokumen ini mengunci bentuk. Setiap naskah panjang di folder ini mengikuti urutan
bab yang sama, dengan alasan yang sama. Kalau satu episode terasa lambat, yang
salah bukan babnya — yang salah adalah isi babnya.

---

## 1. Kenapa bentuknya begini

Analitik kanal (Oktober–November 2026) memberi tiga angka yang menentukan:

| temuan | angka | artinya untuk naskah panjang |
|---|---|---|
| stayed-to-watch rata-rata | 57,9% | penonton pergi di paruh awal. Klimaks harus di depan, bukan di menit 8 |
| durasi yang bertahan | 59–73 dtk | bukan karena penonton tidak suka cerita panjang, tapi karena **short tidak punya ruang misteri** |
| topik yang paling menempel | misteri | episode misteri menahan penonton lebih lama daripada episode bencana |

Kesimpulan operasional: naskah panjang **bukan** short yang diperpanjang. Short
menjawab pertanyaan di detik ke-40. Naskah panjang **menahan** jawabannya, dan
justru itu yang membuatnya bisa 10–30 menit.

Aturan turunannya: satu episode panjang = **satu pertanyaan**, bukan tiga. Kalau
muncul fakta yang tidak membantu pertanyaan itu, fakta itu dipotong walaupun
menarik.

---

## 2. Kerangka tujuh bab

Penanda waktu memakai naskah 12 menit (~1.650 kata). Untuk naskah 20 menit,
kalikan panjang bab, jangan tambah bab.

| # | bab | waktu | isi | fungsi |
|---|---|---|---|---|
| 1 | **PINTU MASUK** | 0:00–0:40 | satu adegan, satu pertanyaan | mengunci penonton sebelum ia sadar ia menonton |
| 2 | **ORANGNYA** | 0:40–3:00 | siapa yang ada di situ, apa yang ia mau, apa yang menghalangi | penonton hanya bertahan kalau ada manusia yang bisa ia bayangkan |
| 3 | **YANG TIDAK COCOK** | 3:00–6:30 | tiga barang bukti, urut dari paling wajar ke paling aneh | setiap barang bukti harus menutup satu dugaan dan membuka dugaan lain |
| 4 | **YANG DITEMUKAN BELAKANGAN** | 6:30–9:00 | penelitian, dokumen, atau penyelidikan modern | ini bagian yang membuat kanal ini bukan sekadar daftar horor |
| 5 | **DUGAAN YANG PALING KUAT** | 9:00–10:30 | satu penjelasan, diuji jujur | kalau kita tidak punya penjelasan, katakan tidak punya |
| 6 | **YANG MASIH TERBUKA** | 10:30–11:30 | satu detail yang tidak diselesaikan penjelasan itu | sisa inilah yang dibawa pulang penonton |
| 7 | **PERTANYAAN PENUTUP** | 11:30–12:00 | satu pertanyaan, bukan kesimpulan | memicu komentar dan tonton-ulang |

**Larangan yang tidak boleh dilanggar:**

· Bab 1 tidak boleh dibuka dengan tahun, angka, atau nama tempat. Buka dengan
  **benda atau orang yang sedang melakukan sesuatu**. Tahun masuk di kalimat ketiga
  atau di bab 2.
· Bab 3 tidak boleh berisi lebih dari tiga barang bukti. Empat membuat penonton
  berhenti menghitung.
· Bab 5 wajib menyebutkan **apa yang tidak dijelaskan** oleh dugaan itu, di bab
  yang sama. Jangan menunda ke bab 6 seolah kejutan.
· Tidak ada kata "tercatat", "terjadi", "diketahui", "menurut data". Ganti dengan
  apa yang dilihat orang.
· Tidak ada rekonstruksi yang tidak ada di `sumber`. Kalau adegan tidak punya
  sumber, adegan itu ditulis sebagai pertanyaan, bukan sebagai peristiwa.

---

## 3. Cara memakai naskah ini

Setiap berkas `EPxx_PANJANG.md` punya dua lapis:

· **teks narasi** — inilah yang dibaca. Satu paragraf = satu tarikan napas.
· **kotak `🎬`** — catatan visual dan jeda. **Jangan ditempel** ke ElevenLabs.

Berkas `.txt` di sebelahnya sudah bersih: hanya narasi, satu paragraf per baris,
siap ditempel.

Setelan ElevenLabs yang dipakai kanal:

| unsur | nilai |
|---|---|
| stability | 0.38 |
| similarity | 0.82 |
| style | 0.35 |
| speaker boost | on |
| speed | 0.88 (naikkan ke 0.92 kalau hasilnya di bawah 140 kata/menit) |

Satu suara untuk seluruh episode. Jangan berganti suara di tengah naskah panjang —
penonton kehilangan satu-satunya jangkar yang ia punya.

---

## 4. Pemeriksaan sebelum render

1. Baca bab 1 dengan suara keras. Kalau kalimat pertama terdengar seperti berita,
   tulis ulang.
2. Hitung: apakah pertanyaan utama muncul sebelum detik ke-30? Kalau tidak, potong.
3. Periksa setiap fakta di bab 3 dan 4 terhadap `tools/content_data.py` → kunci
   `sumber`. Tidak ada angka baru yang tidak ada di sana.
4. Baca bab 6. Kalau di situ sudah ada jawaban lengkap, hapus satu paragraf —
   naskah panjang butuh satu pintu yang dibiarkan terbuka.
5. Baca bab 7. Kalau pertanyaannya bisa dijawab "ya" atau "tidak", ganti.

---

## 5. Status pengerjaan

Delapan episode pertama sudah selesai. Kata dihitung dari berkas `.txt`
(bukan dari `.md` yang memuat catatan 🎬).

| berkas | episode | paragraf | kata | 150 kpm | setelan 0,88 (≈130 kpm) |
|---|---|---|---|---|---|
| `EP01_PANJANG.md` | Tiga penjaga dan satu set pakaian | 52 | 1.328 | 8,9 mnt | ±10,2 mnt |
| `EP02_PANJANG.md` | Tenda yang dipotong dari dalam | 52 | 1.280 | 8,5 mnt | ±9,8 mnt |
| `EP03_PANJANG.md` | Kapal yang masih bisa berlayar | 57 | 1.314 | 8,8 mnt | ±10,1 mnt |
| `EP04_PANJANG.md` | Mereka berjalan menjauhi pertolongan | 64 | 1.252 | 8,3 mnt | ±9,6 mnt |
| `EP05_PANJANG.md` | Satu kata, bukan peringatan | 58 | 1.293 | 8,6 mnt | ±9,9 mnt |
| `EP06_PANJANG.md` | Api di bawah kota | 48 | 1.225 | 8,2 mnt | ±9,4 mnt |
| `EP07_PANJANG.md` | Jejak kaki itu hanya satu arah | 53 | 1.255 | 8,4 mnt | ±9,7 mnt |
| `EP08_PANJANG.md` | Semua label di pakaiannya dipotong | 54 | 1.239 | 8,3 mnt | ±9,5 mnt |

Durasi bergantung pada pace render. Pada setelan yang dipakai kanal (speed 0,88),
pace-nya jatuh di sekitar 128–132 kata/menit, jadi semua berkas di atas berada di
**9,4–10,2 menit**. Naikkan ke speed 0,92 kalau ingin lebih pendek, atau pakai
"lapisan" di `PETA_21_EPISODE.md` untuk versi 20–30 menit.

EP09–EP21: kerangka, pertanyaan, dan urutan babnya sudah dikunci di
`PETA_21_EPISODE.md`, tetapi naskahnya **belum ditulis** karena fakta episode itu
masih berstatus `NEEDS-SOURCE` di `tools/content_data.py`. Menulis naskah panjang
dari sumber yang belum dibaca sama dengan mengarang.
