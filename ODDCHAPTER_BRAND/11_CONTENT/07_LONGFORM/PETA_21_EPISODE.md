# PETA 21 EPISODE — NASKAH PANJANG
### Satu pertanyaan per episode. Arah: misteri.

Aturan dari analitik kanal: penonton bertahan pada **misteri**, bukan pada bencana.
Karena itu setiap episode panjang dibingkai sebagai pertanyaan yang tidak selesai,
walaupun topiknya letusan, wabah, atau kecelakaan industri.

Kolom **status** menentukan apakah episode boleh ditulis penuh:
`VERIFIED` = fakta di `tools/content_data.py → sumber` sudah dicek;
`PERLU CEK` = naskah panjang **belum** ditulis sampai sumbernya dibaca langsung,
supaya tidak ada detail baru yang dikarang.

| ep | seri | pertanyaan panjang (misterinya) | yang dibongkar di bab 5 | status |
|---|---|---|---|---|
| 01 | HILANG | kenapa tiga penjaga keluar tanpa pakaian tahan air & pintu terkunci dari dalam | gelombang di sisi pulau — tidak menjelaskan pakaian yang tertinggal | **VERIFIED** |
| 02 | HILANG | kenapa sembilan orang memotong tenda sendiri lalu lari tanpa sepatu | longsoran lempeng salju (Gaume & Puzrin 2021) — tidak menjelaskan kenapa tak ada yang kembali | **VERIFIED** |
| 03 | HILANG | kenapa sepuluh orang naik sekoci dari kapal yang masih bisa berlayar | uap alkohol di palka — tidak menjelaskan pompa yang dibongkar | **VERIFIED** |
| 04 | HILANG | kenapa lima pria berjalan ke atas, menjauhi mobil & pertolongan | tersesat — tidak menjelaskan kenapa tak satu pun berbalik | **VERIFIED** |
| 05 | HILANG | kenapa rumah dibongkar rapi lalu hanya satu kata dipahat, tanpa salib | pindah & berbaur (Site X, Hatteras, peta La Virginea Pars) — tidak menjelaskan kapan mereka berhenti jadi koloni | **VERIFIED** |
| 06 | TERSEMBUNYI | kenapa api satu sore masih menyala 60+ tahun kemudian | api bawah tanah tak bisa dipadamkan (DEP: ±400 acre, ±540 °C) — tidak menjelaskan 19 tahun pembiaran | **VERIFIED** |
| 07 | TERSEMBUNYI | kenapa jejak kaki hanya satu arah, dan ternak tetap dirawat | pelaku orang lokal — tidak menjelaskan kenapa ia tinggal 4 hari | **VERIFIED** |
| 08 | TERSEMBUNYI | kenapa semua label dipotong tapi buku kode disimpan | agen / pelarian pribadi — tidak menjelaskan kode yang sengaja dibuat bertahan | **VERIFIED** |
| 09 | TERSEMBUNYI | kenapa pria tanpa identitas membawa sobekan puisi, dan apa dua kata itu | identifikasi DNA 2022 (Carl Webb); kode TAMAM SHUD belum terpecahkan | **VERIFIED** |
| 10 | TERSEMBUNYI | kenapa dua kembar membangun bahasa yang hanya mereka bisa pakai | idioglossia & pemisahan institusi (Broadmoor) — batas antara bahasa & perlindungan diri | **VERIFIED** |
| 11 | ANEH | kenapa sinyal 72 detik itu tidak pernah terulang, di frekuensi paling masuk akal | 1420 MHz = garis hidrogen; arah tanpa bintang; 40 tahun pencarian kosong | **VERIFIED** |
| 12 | ANEH | kenapa kota memilih menari sampai ratusan orang sakit, bukan menghentikannya | 1518 Strasbourg: wabah tari & cara otoritas menanganinya | **VERIFIED** |
| 13 | ANEH | kenapa ratusan orang menunggu sesuatu di Morro do Vintém sampai mereka sendiri jadi bukti | 1966, saksi & catatan terjemahan | **VERIFIED** |
| 14 | ANEH | kenapa dua siaran bajakan terjadi dalam satu malam dan pelakunya tak pernah tertangkap | Max Headroom 1987, laporan FCC | PERLU CEK |
| 15 | ANEH | kenapa kerangka satu meter itu membuat kita menulis ulang garis waktu manusia | Homo floresiensis, Liang Bua; revisi stratigrafi 2016 | PERLU CEK |
| 16 | ANEH | kenapa tawa bisa menyebar tanpa virus, dan kenapa ia berhenti | epidemi tawa Tanganyika 1962, laporan jurnal medis | PERLU CEK |
| 17 | BENCANA | kenapa suara letusan terdengar 4.800 km jauhnya tapi banyak yang tak mendengar apa pun | Krakatau 1883, catatan barometer global | PERLU CEK |
| 18 | BENCANA | kenapa setahun setelah Tambora, salju turun di bulan Juni | tahun tanpa musim panas 1816, hubungan letusan–harga roti | PERLU CEK |
| 19 | BENCANA | kenapa ledakan terbesar yang tercatat tidak meninggalkan kawah, dan butuh 19 tahun untuk ditemukan | Tunguska 1908, ekspedisi Kulik | PERLU CEK |
| 20 | BENCANA | kenapa 1.700 orang mati oleh udara yang turun dari danau | Nyos 1986, mekanisme limnik & degassing sejak 2001 | PERLU CEK |
| 21 | HARGA | kenapa perusahaan tahu, dan hukum baru berubah setelah mereka mati | Radium Girls 1917–1930an, gugatan 1927 & presedennya | PERLU CEK |

---

## Urutan penulisan berikutnya

1. **Selesai:** EP01–EP13 (sumber diverifikasi 6 Nov 2026, naskah panjang sudah ada).
2. **Selanjutnya:** EP14–EP21. Sebelum menulis, baca sumber tiap kasus (bukan
   ringkasan), lalu ubah kolom `sumber` di `content_data.py` dari `NEEDS-SOURCE`
   menjadi `VERIFIED` dengan tanggal + dokumen yang dibaca.
3. Episode yang sumbernya tetap `PERLU CEK` **tidak** ditulis panjang. Lebih baik
   tidak ada naskah daripada naskah yang mengarang.

### Koreksi fakta yang sudah dilakukan (6 Nov 2026)

· **EP10:** versi lama menyebut "June meninggal 1993, Jennifer setahun kemudian".
  Yang benar: **Jennifer** meninggal 9 Maret 1993 (usia 29); June masih hidup
  (wawancara BBC 2023). Short EP10 sudah diperbaiki.
· **EP10:** "bahasa rahasia" dibantah June sendiri: yang dipakai adalah bahasa
  Inggris dengan gangguan wicara berat + slang Kreol Bajan. Ini dipakai sebagai
  tikungan di bab 5 naskah panjang.
· **EP09:** label "Keane" ternyata bukan nama samaran — pakaian itu milik
  keponakan Webb yang gugur di PD II. Identifikasi Carl Webb (Juli 2022) belum
  dikonfirmasi resmi oleh koroner.
· **EP13:** klaim saksi soal objek di langit dan uang yang hilang **tidak** dipakai
  sebagai fakta; hanya disebut sebagai klaim tak terverifikasi.

## Kalau butuh 20–30 menit

Kerangka tujuh bab menghasilkan ±10 menit. Untuk melewati 20 menit, jangan
menambah bab baru di tengah — tambahkan **lapisan** di dalam bab yang sudah ada:

· **BAB 2 +** riwayat tempat & orang sebelum hari kejadian (dari sumber yang sama).
· **BAB 3 +** barang bukti keempat dan kelima, yang masing-masing **menutup** satu
  dugaan. Ini yang membuat penonton bertahan: setiap barang bukti harus menghapus
  satu kemungkinan.
· **BAB 4 +** dokumen: kutipan laporan, angka resmi, nama penyidik.
· **BAB 6 +** dua penjelasan yang saling bertentangan, disajikan bergantian tanpa
  memilih pemenang.

Aturan tetap: satu episode satu pertanyaan. Menambah panjang tanpa menambah
ketegangan hanya menambah waktu keluar penonton.
