# Batch 04 — 16 YouTube Shorts mandiri, source-first

**Status: Rencana produksi dan jadwal draf — BELUM BOLEH DIANTREKAN/DIUNGGAH**
**Keputusan pemilik:** 6 November 2026
**Format disetujui:** 16 Shorts mandiri (bukan 1 long-form + 3 companion per hari)
**Slot disetujui:** 28 November–1 Desember 2026, pukul 07.00 / 12.00 / 18.00 / 21.00 WIB
**Visibilitas target:** harus ditetapkan ulang dalam metadata yang telah disetujui

> Pemilik memilih urutan **sumber → skrip → produksi → jadwalkan**. Karena itu,
> dokumen ini mengunci **niat jadwal**, bukan membuat unggahan atau antrean
> `requested`. Tidak ada master, metadata unggah, file Drive, atau queue publish
> yang boleh dibuat sampai setiap slot lolos gerbang bukti di bawah.

---

## 1. Jadwal yang dikunci

| Hari | Pagi · 07.00 WIB | Siang · 12.00 WIB | Sore · 18.00 WIB | Malam · 21.00 WIB |
|---|---|---|---|---|
| Sabtu, 28 Nov | B04-S01 · Great Moon Hoax | B04-S02 · Cottingley Fairies | B04-S03 · Cardiff Giant | B04-S04 · Foto “Nessie” 1934 |
| Minggu, 29 Nov | B04-S05 · Mary Toft | B04-S06 · Clever Hans | B04-S07 · Piltdown Man | B04-S08 · Mechanical Turk |
| Senin, 30 Nov | B04-S09 · Fox Sisters | B04-S10 · Feejee Mermaid | B04-S11 · Mitos panik *War of the Worlds* | B04-S12 · Princess Caraboo |
| Selasa, 1 Des | B04-S13 · Tjut Zahara Fonna | B04-S14 · Babi Ngepet Depok | B04-S15 · Hitler Diaries | B04-S16 · Sokal Affair |

Konversi teknis ke UTC dan payload Zernio berada di
`BATCH_04_SCHEDULE_DRAFT.json`. Bila suatu slot tidak mencapai status **GO**,
slot itu **kosong**—tidak diganti arsip lama, tidak diisi AI generik, dan tidak
dipaksakan tayang demi memenuhi jadwal.

---

## 2. Gerbang wajib setiap Shorts

Satu slot baru boleh bergerak dari `RISET` ke `GO PRODUKSI` setelah semuanya benar:

1. **Dua sumber dibaca langsung**, termasuk setidaknya satu sumber primer, arsip,
   museum, dokumen institusional, atau riset ilmiah yang menyajikan metode/bahan.
2. **Lembar fakta** menyatakan setiap klaim yang dipakai, sumbernya, batas
   kepastian, dan klaim yang sengaja dibuang.
3. **Naskah ≤ 90 detik** lolos cek etik: tidak mengafirmasi supernatural, tidak
   mengolok agama/komunitas, tidak mengeksploitasi tubuh/korban, dan tidak membuat
   vonis hukum baru.
4. **Visual** punya credit/licence yang dapat dibuktikan. Ilustrasi AI hanya boleh
   menjadi ilustrasi berlabel; tidak boleh menyerupai bukti arsip atau rekonstruksi
   korban.
5. **Master Remotion** sudah ditonton/QC, dengan manifest provenance, SHA-256,
   ukuran byte, thumbnail, dan metadata yang konsisten.
6. **Master berada di Drive** dan dapat diunduh workflow; baru sesudah itu metadata
   dan satu file antrean `approved: true` dibuat untuk satu unggahan.

Tidak satu pun dari baris di bawah telah melewati enam gerbang tersebut.

---

## 3. Daftar 16 konten baru dan jalur pembuktian

| Slot | Judul kerja (bukan metadata final) | Hook/artefak konkret | Payoff manusia/sistem | Jejak sumber awal untuk dibaca | Status & batas keras |
|---|---|---|---|---|---|
| B04-S01 | **1835: Koran Ini Menemukan Makhluk Bersayap di Bulan** | Cetakan 1835 “lunar animals” | Nama astronom, istilah teknis, dan rantai sumber menciptakan otoritas palsu. | Library of Congress print; reprint Smithsonian 1859. Dossier: `RISET_GREAT_MOON_HOAX_1835.md`. | `RISET LANJUT`; jangan klaim semua orang percaya, angka sirkulasi, atau bentuk pengakuan *Sun* sebelum koran primer dibaca. |
| B04-S02 | **5 Foto Peri di 1917. Semua Punya Peniti** | Foto dan kamera Cottingley | Foto yang tidak dimanipulasi gelap kamar tetap bisa merekam panggung kertas. | National Science and Media Museum; Leeds Special Collections. | `RISET`; jangan mengejek dua anak atau menyatakan foto kelima terselesaikan bila sumber menyisakan klaim berbeda. |
| B04-S03 | **1869: Mereka Mengubur Patung agar “Menemukan” Raksasa** | Foto/kliping penggalian Cardiff Giant | Benda, kerumunan, pers, dan otoritas ilmiah dapat diuji lewat bahan patung dan dokumen sezaman. | Massachusetts Historical Society; *Proceedings* MHS 1869. | `RISET`; jangan pakai narasi “seluruh umat/semua warga” atau motif tunggal pencipta tanpa sumber primer. |
| B04-S04 | **1934: Foto Monster Itu Hanya Model Kecil** | Cetakan “Surgeon’s Photograph” | Foto menjadi bukti karena kredit seorang dokter dan koran, bukan karena ukurannya terbukti. | Science Museum Group object 1983-5236/31788; koran 1934/rekaman pengakuan harus dibaca. | `RISET`; tanpa visual animal harm, tanpa menyatakan semua kisah Loch Ness selesai hanya dari satu foto. |
| B04-S05 | **1726: Dokter Menulis 38 Halaman tentang Kelinci** | Buku harian Richard Manningham | Kegagalan/kompetisi otoritas medis dibaca dari arsip, bukan sebagai tontonan tubuh. | Wellcome Collection diary/deposisi Mary Toft. | `RISET ETIK TINGGI`; tanpa tubuh, prosedur, atau pengakuan yang diperlakukan bebas tekanan. |
| B04-S06 | **1904: Kuda Ini Berhenti Menjawab saat Tak Ada yang Tahu** | Tabel eksperimen Pfungst | Kesalahan bukan sulap sadar; peneliti menemukan isyarat manusia yang tak disadari. | Oskar Pfungst, *Clever Hans* (1911), termasuk laporan 1904. | `RISET`; jangan menyebut pemilik sengaja menipu dan jangan menyalin angka eksperimen tanpa halaman. |
| B04-S07 | **1953: Tulang “Manusia Purba” Itu Gagal di Uji Bahan** | Rekam arsip Piltdown dan laporan pengujian | Bukti fisik baru mengalahkan sebuah rekonstruksi yang terasa cocok dengan harapan zamannya. | Natural History Museum/National Archives catalog; laporan 1953. | `RISET`; jangan pakai klaim dalang tunggal atau menyiratkan bidang evolusi runtuh karena satu pemalsuan. |
| B04-S08 | **1828: Mesin Catur Ini Membuka Kotaknya. Manusia Tetap Tersembunyi** | Broadside pertunjukan Maelzel | Penonton melihat roda gigi, tetapi tak melihat siapa yang mengambil keputusan. | Library of Congress broadside 1826/1828; sumber museum tentang mekanismenya. | `RISET`; konteks kostum “Turk” tidak boleh dieksotisasi; bukan analogi simplistis terhadap AI modern. |
| B04-S09 | **1848: Ketukan dari Dinding Menjadi Gerakan Besar** | Pamflet/pengakuan Fox Sisters | Kejadian ruang keluarga berubah menjadi industri keyakinan, pers, dan pertunjukan. | LOC, *The Death-Blow to Spiritualism* (1888); pamflet kesaksian 1848. | `RISET ETIK`; pengakuan 1888 dan penarikan kemudian harus disampaikan sebagai rekam yang diperdebatkan, bukan vonis tunggal atas seluruh penghayat spiritualisme. |
| B04-S10 | **1842: “Putri Duyung” Itu Dijual sebagai Benda Pajangan** | Objek “Mermaid” koleksi Peabody | Sensasi tidak hanya berasal dari objek, tetapi juga kampanye promosi dan asal-usul yang tidak dapat diverifikasi. | Harvard Peabody object 97-39-70/72853; autobiografi Barnum 1855. | `RISET`; jangan menyatakan objek Harvard pasti artefak Barnum asli; hindari visual tubuh hewan yang eksploitif. |
| B04-S11 | **1938: Cerita Kepanikan Radio yang Terlanjur Dipercaya** | Rekaman siaran dan halaman koran | Siaran fiksi nyata; mitos bahwa “seluruh negeri panik” harus diuji kembali lewat data dan liputan. | Library of Congress recording/essay; studi tanggapan kontemporer. | `RISET`; jangan mengganti satu mitos absolut dengan absolut baru—akui sebagian pendengar memang cemas. |
| B04-S12 | **1817: Perempuan Ini Datang dengan Bahasa yang Tidak Ada** | Pamflet 1817/potret Caraboo | Masyarakat elite membaca pakaian, bahasa ciptaan, dan “penerjemah” sebagai bukti status. | John M. Gutch, *Caraboo* (1817); kliping 1817/potret Bristol. | `RISET ETIK`; kritik diarahkan ke sistem kelas/eksotisasi, bukan aksen, etnis, atau latar miskin Mary Baker. |
| B04-S13 | **1970: Suara dari Perut Membuat Orang-Orang Datang** | Kliping koran 1970 tentang pemeriksaan/penangkapan | Klaim luar biasa memperoleh legitimasi sebelum pemeriksaan; fokus pada media dan verifikasi. | NewspaperSG, *Berita Harian* 3 & 7 Nov 1970; laporan kontemporer tambahan. | `RISET ETIK TINGGI`; jangan mengejek bacaan agama atau subjek; mekanisme *tape recorder* hanya dipakai setelah kliping primer dibaca utuh. |
| B04-S14 | **2021: Seekor Babi Dibeli untuk Menjadi “Bukti”** | Pernyataan konferensi pers Polres Depok / jejak video viral | Rumor kehilangan uang, peran sosial, dan skenario visual menciptakan klaim gaib yang dapat diperiksa polisi. | Pernyataan Kapolres dalam laporan TVRI/Tempo/Detik 29 Apr 2021. | `RISET ETIK TINGGI`; tidak ada footage penyembelihan, ejekan ke keyakinan, nama/identitas tak perlu, atau detail prosedur hukum yang belum dipastikan. |
| B04-S15 | **1983: Buku Harian Ini Runtuh ketika Kertasnya Diuji** | Dokumen/press release Bundesarchiv | Sebuah scoop melewati pemeriksaan awal; materi kertas, tinta, dan arsip menghentikannya. | Bundesarchiv 6 Mei 1983; artikel arsip 7 Mei 1983. | `RISET SENSITIF`; fokus pada forensik dokumen dan kegagalan media, tanpa visual propaganda, simbol ekstremis, atau pemutihan kejahatan Nazi. |
| B04-S16 | **1996: Jurnal Ini Mencetak Parodi Fisika sebagai Serius** | Artikel *Social Text* dan pengakuan penulis | Kredensial dan jargon dapat mengalahkan pemeriksaan argumentasi; tidak membuktikan seluruh bidang ilmu “palsu”. | Arsip primer Alan Sokal (artikel, pengungkapan, dan respons editor). | `RISET`; jangan memakainya untuk menyerang akademisi/kelompok politik secara menyeluruh; baca respons editor bersama sumber Sokal. |

---

## 4. Audit kebaruan yang sudah dilakukan

Istilah spesifik enam belas topik di atas dipindai terhadap teks editorial di
`11_CONTENT`, `07_LONGFORM`, skrip, kalender, kandidat, dan riset—dengan dua
dokumen pivot riset baru dikecualikan dari pencarian. Tidak ada hit untuk setiap
istilah kandidat. Ini berarti mereka **belum terlihat sebagai konsep yang sudah
dikembangkan** di arsip kerja saat audit dilakukan.

Audit ini bukan bukti bahwa subjek tidak pernah dibahas di seluruh internet; ia
hanya mencegah duplikasi dengan materi ODDCHAPTER yang tersedia di repositori.
Audit akan diulang sebelum metadata unggah dibuat.

---

## 5. Urutan kerja dan aturan jadwal publik

1. Bangun **16 lembar fakta** dan baca sumber yang ditautkan langsung.
2. Hanya slot berstatus `GO PRODUKSI` yang memperoleh naskah, VO, visual, dan
   master Remotion.
3. QC setiap master + unggah ke Drive + `drive_file_id`, ukuran, hash, thumbnail,
   dan provenance dimasukkan ke metadata upload.
4. Buat dan validasi **dry-run** Zernio untuk satu slot pada satu waktu.
5. Baru buat satu queue file `approved: true` dengan `scheduledFor` yang telah
   dikunci. Workflow kanal memaksa satu unggahan per push dan memverifikasi hash.

**Larangan:** tidak ada placeholder, unggah massal, master tanpa hash, queue
`requested` sebelum QC, atau penggantian video/kalender lama.
