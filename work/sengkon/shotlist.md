# SHOT LIST – Sengkon & Karta (ODDCHAPTER Short, ±85 s, 1080×1920)
Dibuat 19 Nov 2026. Ini paket aset/brief untuk agent builder (Angker Bot tidak lagi membangun video). VO belum direkam (voice: Riri Rida `tCKeP99grYL9wZRg6sQ9`, model `eleven_multilingual_v2`; kredit ±50, top-up diperlukan untuk re-take). Naskah: `naskah.md` (hook B). Foto asli: folder `foto/` + `foto/sources.md`.
**Aturan:** tanpa AI-generated photo/gambar orang; foto orang hanya dari arsip asli. Visual simbolis (pintu besi, lorong, malam desa) dari stok berlisensi atau bank footage. Tidak menampilkan jenazah/kekerasan. Crop wajah anak-anak dari montase Sinar Harapan.
**YouTube diblokir dari IP box**, sehingga semua unduhan YouTube dilakukan nanti di laptop Kahfi (pop-os, `~/.local/bin/yt-dlp`, ffmpeg). Lihat bagian "Unduhan YouTube".

## A. Tabel beat (waktu perkiraan, tempo VO pelan)

| # | Waktu | VO (anchor) | Visual utama | Sumber aset | Teks layar |
|---|---|---|---|---|---|
| 1 | 0:00–0:07 | HOOK "Pembunuh sebenarnya mendekam…" | Hitam; bunyi besi/kunci; foto Kompas 5 Nov 1980 muncul redup, zoom sangat pelan | `foto/kompas_halaman1_5nov1980_sengkon_karta_bebas.jpg` (grade gelap, vignette) | "SATU PENJARA" |
| 2 | 0:07–0:19 | "November 1974, Bojongsari… dua petani miskin" | Malam desa, rumah bambu/kayu, kabut; jalan tanah sepi | Stok (lihat query D1) atau bank: G__6fYuJ684 jalan desa @10:00–15:00 (tanpa tebu, di-grade gelap) | "BOJONGSARI, BEKASI — 1974" |
| 3 | 0:19–0:31 | "Mereka menyangkal… menandatangani… hakim lebih percaya polisi" | Tangan menulis/menandatangani kertas, bayangan jendela (close-up simbolis, tanpa wajah) | Stok (D2) | "MENURUT MEREKA: DISIKSA" |
| 4 | 0:31–0:43 | "Oktober 1977… dua belas tahun… tujuh tahun… Cipinang… tanah dijual" | Palu hakim / ruang sidang gelap + lambang Garuda; pintu besi penjara | Bank: R852jnm95ME @38:58 ruang sidang Garuda (inset, Dukun AS 1998 – ilustrasi saja, BUKAN sidang ini) atau stok (D3) | "OKT 1977 — SENGKON 12 TH · KARTA 7 TH" |
| 5 | 0:43–0:53 | "Lalu, di balik tembok yang sama… Genul… pembunuh" | Lorong penjara, jeruji, cahaya dingin; jeda 1 detik sebelum "Genul" | Bank: R852jnm95ME @15:38 ilustrasi pria di balik jeruji (inset) atau stok (D4) | "GENUL — keponakan Sengkon" |
| 6 | 0:53–1:06 | "Genul diadili… pintu sel tetap terkunci… putusan final" | Pintu besi menutup; stempel "INKRACHT"; foto Oemar Seno Adji (inset kecil, grade gelap) | Stok pintu (D4) + `foto/wiki_oemar_seno_adji_menteri_kehakiman.jpg`; teks stempel dibuat sendiri | "PUTUSAN SUDAH FINAL" |
| 7 | 1:06–1:16 | "Empat November 1980… ambulans… TBC… tanah habis… 1982… 1988" | Foto arsip nyata: Sengkon di RSU Bekasi; Karta dipeluk keluarga; urut cepat 2–3 s/foto, Ken Burns pelan | `foto/kompas_sengkon_rsu_bekasi_1980.jpg`, `foto/kompas_karta_dipeluk_keluarga_4nov1980.jpg`, `foto/historia_sinarharapan_5nov1980.jpg` (crop panel Sengkon kiri-atas; tanpa panel anak) | "4 NOV 1980" lalu "1982" · "1988" |
| 8 | 1:16–1:25 | "Dari luka mereka lahir Peninjauan Kembali… siapa yang akan menolong mereka?" | Halaman Kompas 5 Nov 1980 zoom-out perlahan → fade ke hitam; langkah menjauh | `foto/kompas_halaman1_5nov1980_sengkon_karta_bebas.jpg`; opsional `foto/wiki_gedung_mahkamah_agung_ri.jpg` (grade gelap) | "Peninjauan Kembali (PK)" lalu "Sumber: Kompas, Tempo, Detik, Tirto" · "Foto: Arsip Kompas/Kartono Ryadi · Sinar Harapan/Perpusnas RI" |

Audio bed: gunakan `/workspace/dukun-as/work/mix.py` (drone, sub-bass, detak jam, angin; layer dapat diatur; gratis kredit). Tambah: gema logam sel (beat 5–6), satu stinger tipis saat "Genul" (beat 5) dan saat "4 November 1980" (beat 7). Target LUFS −15 sama seperti Dukun AS v2.
Sinkron: cut = onset kata − 0.15 s (metode v2 Dukun AS; jalankan faster-whisper pada VO final lalu re-time).

## B. Pemakaian foto asli (ringkas)
Lihat `foto/sources.md` untuk kredit. Tidak ada foto Genul dan lokasi era 1970-an (celah). Jangan buat ilustrasi wajah Genul atau komplotan.

## C. Bank footage lama (/workspace/dukun-as/footage_index.md) – bisa dipakai ulang?
Bank dibuat untuk Dukun AS (Sumatra Utara, ladang tebu). Relevansi rendah; hanya untuk atmosfer simbolis dan HARUS dilabeli "ilustrasi". Jangan dipakai sebagai bukti.
| Aset bank | Waktu | Pemakaian untuk Sengkon-Karta |
|---|---|---|
| R852jnm95ME (Dateline 2016) | 0:00–0:04 awan badai gelap | Transisi/hook (beat 1) ✔ |
| R852jnm95ME | 38:55–39:10 ruang sidang 1998 + Garuda (inset, hindari wajah hakim/terdakwa) | Beat 4 (ilustrasi ruang sidang) ✔ terbatas |
| R852jnm95ME | 15:30–15:38 ilustrasi pria di balik jeruji; 15:30–16:00 siluet berjalan kabut | Beat 5 ✔ (ilustrasi bergaya, aman) |
| R852jnm95ME | 12:20–12:30 jalan setapak hutan gelap | Beat 2 opsional |
| G__6fYuJ684 (Dolan Medan) | 10:00–15:00 jalan desa sepi, pohon besar | Beat 2 (grade gelap; Medan ≠ Bekasi) opsional |
| 7BFEpTTfYCM (Tinta Waktu) | ilustrasi 10:08–10:32 (tabib/rahasia) | ✘ terlalu spesifik Dukun AS |
| Semua klip ladang tebu, kliping koran "Dukun AS", dramatisasi tebu, makam, wawancara, SCTV 2008 | – | ✘ jangan dipakai |
Hindari: apa pun yang menampilkan wajah/jenazah/penggalian. Ingat bank = hak cipta pihak ketiga; jangan hapus/ubah file sumber.

## D. Kueri pencarian footage (untuk stok/CC/YT; unduh di laptop)
Stok berlisensi bebas (Pexels/Pixabay/Mixkit/Videvo/Wikimedia Commons; cek lisensi):
- D1 "village night fog bamboo house", "rural Indonesia night dark path", "kampung malam gelap rumah bambu"
- D2 "hand signing document dark close up", "pen writing paper shadow window", "interrogation room shadow" (tanpa wajah)
- D3 "judge gavel dark courtroom", "courtroom empty dark", "Garuda emblem court Indonesia"
- D4 "prison corridor dark bars", "iron door closing prison", "jail cell shadow", "heavy metal door lock close"
- D5 (atmosfer) "clock ticking dark", "rain window night", "old newspaper close up"
Arsip/penerbit YouTube (pencarian di laptop, cuplikan atmosfer/arsip, bukan klaim fakta):
- "Sengkon Karta dokumenter", "Sengkon dan Karta kisah nyata", "sejarah peninjauan kembali Sengkon Karta", "Sengkon Karta Kompas TV", "Albert Hasibuan Sengkon Karta wawancara", "LP Cipinang 1980 arsip", "peradilan sesat Indonesia sejarah hukum", "Oemar Seno Adji Mahkamah Agung peninjauan kembali"
- Gunakan hanya potongan tanpa wajah orang yang masih hidup/wawancara; kredit sumber.

## E. Unduhan YouTube (dijalankan LATER di laptop; box IP diblokir)
Hasil pencarian untuk kasus ini menunjukkan: **tidak ada video arsip TVRI/1980 yang terindeks online** dan tidak ditemukan dokumenter YouTube resmi yang jelas. URL kandidat yang ditemukan (belum ditonton, tanpa timestamp pasti karena box tidak bisa memutar/mengunduh YouTube):

| Kandidat | URL | Isi (menurut hasil pencarian) | Pemakaian | Timestamp |
|---|---|---|---|---|
| Puisi "Mata Luka Sengkon Karta" (Peri Sandi Huizache, TIM 1 Juni 2017, kanal Fadli Zon) | https://www.youtube.com/watch?v=MLTOdvXz3Vg | Pembacaan puisi (bukan dokumenter; ada unsur G30S yang tidak terkait) | ✘ jangan dipakai sebagai footage fakta; hanya referensi budaya | – |
| Kompas TV – Yasonna menyinggung Sengkon-Karta (13 Jun 2024) | https://www.kompas.tv/video/514957/menkumham-yasonna-buka-suara-kasus-vina-singgung-kasus-salah-tangkap-petani-sengkon-dan-karta | Berita; tidak relevan visual | ✘ | – |
| Vidio.com Shorts "Kisah Tragis Petani Miskin Sengkon dan Karta…" | https://www.vidio.com/watch/7597495-kisah-tragis-petani-miskin-sengkon-dan-karta-dalam-sejarah-peradilan-indonesia | Shorts; kemungkinan kompilasi ilustrasi | Referensi pembanding gaya; cek lisensi | tonton dulu |
| Dokumenter TV "Mata Luka Sengkon Karta" (Bryan J. T. Halawa, STMM Yogyakarta, 2020) | belum ditemukan di YouTube (hanya katalog skripsi: https://siper.mmtc.ac.id/index.php?id=10155&keywords=&p=show_detail) | Dokumenter mahasiswa | Opsional bila diunggah | – |

**Langkah untuk laptop** (agent builder/Kahfi): 
1. `yt-dlp "ytsearch15:<kueri>" --flat-playlist --print "%(id)s | %(title)s | %(duration_string)s | %(channel)s"` untuk tiap kueri YouTube di D (bagian "Arsip/penerbit").
2. Pilih ≤3 video (hindari wajah wawancara; cari lorong penjara/ruang sidang/arsip koran), tonton cepat, catat timestamp ke `footage_index.md` baru (`~/sengkon-karta-footage`).
3. Unduh segmen saja: `yt-dlp --download-sections "*MM:SS-MM:SS" -f "bv*[height<=1080]+ba/b" -o "~/sengkon-karta-footage/%(id)s_%(section_start)s.%(ext)s" <URL>`.
4. Jangan menghapus bank `~/dukun-as-footage`. Simpan sheet kontak (ffmpeg tile) seperti proses Dukun AS.
Karena belum ada URL+timestamp yang terverifikasi, rencana aman: bangun Short dari **foto arsip (`foto/`) + stok simbolis + bank footage (bagian C)**, bukan dari video YouTube.

## F. Sumber gambar/arsip tambahan (butuh akun/laptop)
- Perpusnas RI – Layanan Surat Kabar Langka (SKALA): cari "Sinar Harapan 5 November 1980", "Kompas 22 Oktober 1980", "Sinar Harapan Oktober 1980 Albert Hasibuan Ketua MA".
- Kompas.id / Arsip Kompas (Kartono Ryadi): foto 3–5 Nov 1980, kunjungan Albert Hasibuan ke Cipinang.
- Majalah Tempo arsip (data.tempo.co / majalah.tempo.co): 13 Des 1980 "Jalan Hukum Sengkon & Karta", 13 Feb 1982 "Meninggal Dunia" (Karta), 29 Sep 1984 "Akhir Legenda Sengkon-Karta", 19 Mar 1988 "Meninggal dunia" (Sengkon).
- Wikimedia Commons: foto modern LP/PN bila perlu (hindari foto individu napi).
- ANRI / Perpusnas film-foto: belum diverifikasi apakah ada koleksi 1974–1981.
