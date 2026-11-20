# AK-EP05 — Andes 1972 (uji format Curiosity Loop, naskah TTS final)

Format: adaptasi ODDCHAPTER 8 beat (`00F_FORMAT_CURIOSITY_LOOP.md` §2).
VO: TTS internal voice-05, 10 klip → `build_vo.py` → **169,91 s** (405 kata);
END video **174,00 s (2:54)** — batas 3 menit terpenuhi. Setiap kalimat utuh,
tidak dipersingkat, tidak ambigu.

## Peta beat → klip (waktu mulai final dari vo_alignment)

| Beat | Fungsi | Klip | Mulai |
|---|---|---|---|
| B1 | Tantangan Logika / Dilema Ekstrem | vo_01 | 0,00 |
| B2 | Reaksi Alami Manusia | vo_02 | 10,04 |
| B3 | Tindakan Sang Tokoh yang Mengagetkan | vo_03 | 21,23 |
| B4 | Pertaruhan Nyawa (High Stakes) | vo_04 | 38,55 |
| B5 | Tekanan Situasi — kecelakaan | vo_05 | 57,10 |
| B6 | Tekanan Situasi — kelaparan & longsor | vo_06 | 81,33 |
| B7 | Tekanan Situasi — sumpah bersama | vo_07 | 102,79 |
| B8 | Momen Puncak — berjalan keluar | vo_08 | 115,46 |
| B9 | Hasil Akhir & Fakta Kunci (reveal) | vo_09 | 133,69 |
| B10 | Interactive Debate Hook | vo_10 | 156,24 (selesai 169,91) |

## Teks VO per klip (sumber TTS — sama persis dengan SEGS build_vo.py)

**vo_01 — Dilema ekstrem**
> Bayangkan pesawat kalian jatuh di pegunungan bersalju dan tujuh hari berlalu tanpa makanan sama sekali. Apa yang akan kalian makan untuk tidak mati kelaparan?

**vo_02 — Reaksi alami manusia**
> Kebanyakan orang akan menjawab bahwa mereka akan bertahan dengan mencari daun atau akar yang bisa dimakan. Tetapi di pegunungan itu tidak ada satu pun tumbuhan dan tidak ada satu pun hewan.

**vo_03 — Tindakan yang mengagetkan**
> Karena itu, para penyintas mengambil keputusan yang tidak pernah masuk rencana siapa pun di antara mereka. Mereka memutuskan memakan tubuh teman-teman mereka sendiri yang sudah meninggal sejak hari pertama kecelakaan, karena hanya itu satu-satunya makanan yang tersisa di gunung itu.

**vo_04 — Pertaruhan nyawa**
> Keputusan itu tidak diambil oleh orang-orang kejam, tetapi oleh orang-orang beriman yang harus memilih antara nilai dan nyawa mereka sendiri. Pada hari kesebelas, sebuah radio transistor di antara kursi pesawat menyiarkan bahwa pencarian resmi terhadap mereka sudah dihentikan. Tidak ada yang tahu mereka masih hidup.

**vo_05 — Kecelakaan**
> Penerbangan itu berangkat dari Montevideo pada tiga belas Oktober seribu sembilan ratus tujuh puluh dua, membawa tim rugbi Old Christians Club menuju Santiago. Pesawat jatuh di sisi Argentina Pegunungan Andes, dan dua belas orang tewas seketika. Tiga puluh tiga orang yang selamat bersembunyi di dalam badan pesawat yang putih, warnanya menyatu dengan salju sehingga pesawat pencari tidak melihatnya dari udara.

**vo_06 — Kelaparan, pencarian, longsor**
> Makanan yang mereka bawa habis dalam satu minggu. Mereka menulis kata SOS dengan lipstik di badan pesawat, tetapi tidak ada pesawat yang menoleh. Pada dua puluh sembilan Oktober, longsor salju menyapu tempat berlindung mereka dan menewaskan delapan orang lagi. Sebagian besar dari mereka beragama Katolik, dan perdebatan tentang keputusan itu berlangsung lama.

**vo_07 — Sumpah bersama**
> Akhirnya mereka mengambil sumpah bersama: tidak ada satu pun orang yang akan dibunuh untuk dijadikan makanan. Keputusan itu diambil bersama setelah setiap orang diberi kesempatan berbicara menentangnya.

**vo_08 — Momen puncak: berjalan keluar**
> Dua orang memutuskan berjalan keluar. Nando Parrado dan Roberto Canessa berjalan selama sepuluh hari melintasi Pegunungan Andes tanpa peta dan tanpa perlengkapan pendakian. Mereka menemukan seorang penggembala bernama Sergio Catalán, yang membawa kabar mereka ke kantor polisi.

**vo_09 — Hasil & fakta kunci**
> Evakuasi dimulai pada dua puluh dua Desember seribu sembilan ratus tujuh puluh dua, tujuh puluh dua hari setelah pesawat jatuh di sebuah lembah sisi Argentina Pegunungan Andes, dekat perbatasan Cile. Enam belas dari empat puluh lima orang selamat. Yang membuat mereka bertahan bukan keberuntungan, melainkan keputusan yang mereka ambil bersama pada malam-malam paling gelap di gunung itu.

**vo_10 — Debat komentar**
> Sekarang giliran kalian. Kalau kalian berada di pesawat itu, dan keputusan itu harus diambil pada malam yang sama juga, kalian ikut, atau kalian menolaknya sampai akhir? Tulis jawaban kalian di kolom komentar.

## Catatan produksi

- Trim 20 Nov: vo_02/04/05/06/07/08/09 diregenerasi lebih ringkas (452 → 405 kata,
  196,63 → 169,91 s). vo_03 memakai klip generasi pertama — frasa inti lolos moderasi
  TTS pada percobaan pertama; percobaan kedua kena blokir, jadi klip lama dipertahankan
  (isinya identik dengan naskah).
- Caption: `NUM_PHRASES` mengubah angka dieja → digit (13/12/33/29/22/72/16/45/8/10,
  "kesebelas" → KE-11, "seribu sembilan ratus tujuh puluh dua" → 1972).
  KEYWORDS merah: ANDES, SOS, 1972, 16.
- Shot QC: klip kota senja_salju diganti (shot 7 → hutan salju, 12 → koran,
  21 → pesawat pencari, 39 → gunung sinematik); shot 8 geser start agar api terlihat.

## Sumber fakta (untuk kartu sumber & deskripsi)

- Britannica — https://www.britannica.com/event/Uruguayan-Air-Force-flight-571
- Wikipedia — https://en.wikipedia.org/wiki/Uruguayan_Air_Force_Flight_571
- Piers Paul Read, *Alive: The Story of the Andes Survivors* (1974)
- Nando Parrado, *Miracle in the Andes* (2006)
- Pablo Vierci, *La Sociedad de la Nieve* (2008) — dasar film *Society of the Snow* (2023)

## Pemeriksaan editorial

- Tanpa gore, tanpa kondisi jenazah, tanpa detail prosedur, tanpa cara kematian eksplisit.
- Angka VO hanya yang disepakati Britannica/Wikipedia (45/12/33/8/16/72; tanggal
  13 Okt 1972, longsor 29 Okt, evakuasi 22 Des). Angka beda sumber tidak dipaksakan.
- "Pencarian dihentikan" = fakta resmi (kisah Roy Harley via Read/Wikipedia), bukan teori.
- Akhir = dilema opini penonton (aturan 55–60 detik versi 1–3 menit), bukan penutup fakta.
