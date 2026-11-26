# Audit editorial — LF04 · Tambora 1815

**Status:** `DRAF LONG-FORM BERBASIS SUMBER — MENUNGGU REVIEW EDITORIAL PEMILIK`

## Mandat dan pilihan topik

Pemilik meminta cerita baru yang **wajib format panjang**, setelah 32 video pendek
belum memperlihatkan kenaikan view yang diharapkan. Pemilihan ini tidak menyimpulkan
bahwa niche gagal; ia mengubah unit nilai dari satu klaim singkat menjadi satu rantai
pembuktian yang dapat diikuti dalam sekitar 10 menit.

Topik yang dipilih untuk riset dan draf ini adalah **Tambora 1815**. Ia lebih kuat dari
angle “gunung paling besar” saja karena memiliki empat jalur bukti yang saling menguji:

1. **Lanskap dan endapan** — kaldera, tefra, aliran piroklastik, dan lima lapisan 1815.
2. **Arsip Nusantara** — berita Java Government Gazette, log kapal, dan rekaman Bima
   yang ditelusuri Badan Geologi.
3. **Arkeologi** — penelitian Doro Bente dengan artefak dan stratigrafi, tanpa membuat
   ulang kehidupan yang tidak terdokumentasi.
4. **Atribusi iklim** — studi peer-reviewed yang membedakan forcing Tambora dari
   variabilitas sirkulasi untuk menjelaskan anomali Eropa 1816.

Dengan begitu video tidak menjual satu fakta viral “musim panas hilang”, tetapi membuka
bagaimana bukti lokal, arsip, dan model iklim saling membatasi satu sama lain.

## Putusan naskah

**Judul kerja:** *Tambora 1815: Lima Lapisan Abu dan Tahun Tanpa Musim Panas*.

**Pertanyaan yang dibayar:** bagaimana letusan di Sumbawa dapat dibuktikan sebagai
rantai lokal → atmosfer → iklim lintas benua tanpa menyederhanakan sebabnya?

**Kalimat tesis:** Tambora bukan sekadar judul tentang “musim panas yang hilang”.
Lima lapisan di Sumbawa, catatan berita yang terlambat tiba, dan model iklim modern
menunjukkan rantai peristiwa yang dapat diuji serta batas dari setiap bagiannya.

**Turn:** bukan “Tambora tidak menyebabkan 1816”, melainkan koreksi yang lebih kuat:
forcings Tambora membuat anomali dingin Eropa jauh lebih mungkin, sementara pola
sirkulasi tetap penting untuk membaca presipitasi dan sebaran dampak regional.

## Pemeriksaan fakta per babak

| Babak | Fungsi / klaim | Pasangan sumber | Putusan |
|---|---|---|---|
| 1 | Lima lapisan piroklastik 1815 di Doro Bente sebagai hook bukti | `SOURCES.md` #18 | Pakai; tidak memperlakukan satu situs sebagai seluruh Sumbawa. |
| 2 | Laporan 1815 bergerak lewat koran, kapal, surat, dan arsip | #9–#12 | Pakai sebagai rekonstruksi beratribusi Badan Geologi, bukan jam kejadian universal. |
| 3 | VEI 7, kaldera, endapan, dan arah aliran | #2–#8, #14–#15 | Pakai; angka menjadi ukuran bukti, bukan kompetisi skala. |
| 4 | Kerajaan di sekitar Tambora dan riset Doro Bente | #13, #16–#18 | Pakai dengan batas ketat: artefak/stratigrafi tidak menjadi rekonstruksi tokoh atau kota lengkap. |
| 5 | SO2, aerosol sulfat, radiasi, dan konteks 1816 | #19–#20 | Pakai sebagai mekanisme serta konteks wilayah yang spesifik. |
| 6 | Model atribusi 2019: dingin, presipitasi, serta peran sirkulasi | #21–#25 | Pakai sebagai pembalik; jangan menyebut sebab tunggal. |
| 7 | Sintesis empat jenis bukti dan echo lima lapisan | #1–#25 | Pakai sebagai kesimpulan editorial, bukan prediksi bencana berikutnya. |

## Batas etika, ilmiah, dan visual

- Tidak ada angka korban jiwa tunggal. Angkanya bervariasi lintas sumber dan bukan
  diperlukan untuk tesis.
- Tidak ada tubuh, wajah korban, kisah duka yang diambil tanpa sumber, atau suara
  teror yang direka.
- Tidak ada label “Pompeii dari Timur”, “kota beku”, atau klaim bahwa suatu situs
  menjaga kehidupan manusia pada menit tertentu.
- “Tahun Tanpa Musim Panas” dilokalkan pada konteks Eropa/Amerika Utara pada 1816,
  bukan seluruh bumi dan bukan ramalan iklim masa kini.
- Seluruh grafik wajib memberi label sumber: `GVP`, `BADAN GEOLOGI 2020`, `BRIN
  2024`, atau `SCHURER ET AL. 2019`.
- Jika kelak memakai gambar arsip atau halaman dokumen, sumber, lisensi, dan nomor
  halaman harus diverifikasi satu per satu. Baseline visual dapat sepenuhnya memakai
  peta/diagram/stratigrafi original agar tidak bergantung pada gambar kejadian.

## Gerbang yang sudah dijalankan

| Gerbang | Hasil |
|---|---|
| Pemetaan klaim → sumber | 25 klaim substantif, 5 sumber dibaca langsung di `SOURCES.md` |
| `python3 ODDCHAPTER_BRAND/tools/check_longform.py LF04_tambora` | **LULUS** — 1.450 kata, sekitar 9,7 menit, 7 babak, 26 baris klaim tabel |
| Struktur cerita | Hook lima lapisan → berita terlambat → bukti fisik → batas arkeologi → mekanisme → atribusi → echo; satu pertanyaan per babak dan satu turn |
| Audit batas | Lulus untuk draf: tidak ada angka korban pasti, tuduhan, rekonstruksi korban, atau sebab iklim tunggal |

## Gerbang yang belum boleh dilompati

- [x] Riset sumber, peta klaim, dan draf long-form diselesaikan.
- [x] Format panjang dipertahankan; **tidak ada Short turunan** dibuat atau
      dijadwalkan oleh pekerjaan ini.
- [ ] Pemilik mereview dan menyetujui judul, tesis, struktur, serta batas ilmiah
      sebelum naskah dianggap final.
- [ ] Asset audit, VO, scene/plate, bundling Remotion, render, QC media, Drive,
      antrean, jadwal, upload, atau publikasi memerlukan persetujuan terpisah.

**Catatan kalender:** ide lama EP18 tentang Tambora adalah proposal Short berstatus
`NEEDS-SOURCE`. LF04 ini adalah episode panjang yang berdiri sendiri; ia tidak
mengubah episode kalender, tidak mengambil nomor EP12 kanonik, dan tidak mengizinkan
aksi distribusi apa pun.
