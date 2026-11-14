NATURAL INDONESIAN WRITING — HUMAN VOICE

Knowledge Base — Script Intelligence

Berkas ini sebelumnya kosong. Isinya disusun dari praktik kanal ini
(`ODDCHAPTER_BRAND/11_CONTENT/00E_SUARA_NARATOR.md`), dari aturan editorial
(`EDITORIAL-FONDATION.md`), dan dari heuristik tanda baca pada
`SKILLS/elevenlabs-tts-2026/PUNCTUATION.md`.

1. PURPOSE

Mengubah naskah yang benar menjadi naskah yang terdengar seperti orang berbicara.

Kebenaran fakta tidak menyelamatkan kalimat yang dibaca seperti pengumuman.
Penonton Shorts memutuskan dalam tiga detik: ini orang yang sedang memberi tahu
saya sesuatu, atau ini orang yang sedang membacakan sesuatu untuk saya.

2. THE DIFFERENCE

LAPORAN:
"Fenomena tersebut menunjukkan adanya kecenderungan masyarakat dalam membentuk
penilaian berdasarkan informasi yang tidak utuh."

MANUSIA:
"Kita menilai orang dari satu potong video. Padahal kita tahu, potongan itu
dibuat supaya kita menilai."

Yang berubah bukan datanya. Yang berubah: siapa yang diajak bicara, dan kapan
kejadiannya (di depan mata, bukan "pada tahun itu").

3. TIGA KEPUTUSAN SEBELUM MENULIS

A. SIAPA YANG BICARA
Satu orang, satu suara, satu pendengar. Bukan "para penonton", bukan "audiens".
Yang diajak: kamu. Yang ikut: kita.

B. KAPAN
Sekarang. Bukan "pada 1922", tapi "malam itu, di rumah itu". Tahun boleh muncul
setelah penonton sudah berdiri di tempat kejadian.

C. APA YANG DITINGGALKAN
Satu pertanyaan yang belum dijawab. Kalau semua sudah dijelaskan di paragraf
pertama, tidak ada alasan untuk tinggal.

4. KALIMAT

- Satu ide per klausa. Koma untuk mengelompokkan, titik untuk menutup.
- Panjang bervariasi: kalimat menengah untuk menyiapkan, kalimat pendek untuk memukul,
  kalimat panjang hanya kalau memang ada napas untuk itu.
- Kata kerja aktif. "Api itu masuk ke batu bara" bukan "api tersebut merambat ke dalam lapisan".
- Benda konkret, bukan kategori. "kunci", "label", "salju", "botol" — bukan "barang bukti",
  bukan "peristiwa tragis".
- Angka dipakai kalau mengejutkan; kalau hanya melengkapi, buang.
- Tidak ada kata pengisi: sangat, cukup, benar-benar, sebenarnya, ternyata, mungkin, memang.

5. YANG DILARANG

- Pembuka berita: "Belakangan ini sedang ramai diperbincangkan…"
- Sapaan & perkenalan: "Halo semuanya, kembali lagi di channel…"
- Kesimpulan kosong: "Begitulah kisahnya, semoga bermanfaat."
- Frasa ringkasan: "sampai hari ini masih menjadi misteri", "banyak teori yang beredar".
- Drama tanpa bukti: "Indonesia berada di ambang kehancuran."
- Bahasa filsafat palsu: "Di balik setiap realitas tersimpan paradoks kehidupan."
- Empat pertanyaan beruntun tanpa satu pun dijawab.
- Penjelasan yang menjelaskan: "Dia panik, yang artinya dia takut."

6. RITME (yang membuatnya terdengar mengobrol)

1. Buka dengan satu kalimat pendek yang menunjuk benda atau kejadian.
2. Beri satu kalimat kedua yang memperbesar jarak: "Tapi ada yang aneh."
3. Sesudah tiga kalimat informasi, sisipkan satu kalimat yang menyapa penonton.
4. Sebelum pembalik, berhenti. Kalimat terpendek di seluruh naskah ada di situ.
5. Sesudah pembalik, jangan menambah fakta baru. Ubah makna yang sudah dilihat.
6. Tutup dengan gambar yang sama seperti pembuka, dengan arti yang berbeda.

7. TANDA BACA SEBAGAI ARAHAN SUARA

Koma mengelompokkan. Titik menutup. Tanda tanya hanya untuk pertanyaan yang benar-benar
ditanyakan. Elipsis (…) untuk menahan satu kata yang belum ingin disebut — maksimal
dua kali per naskah. Em dash (—) untuk patah mendadak. Tanda seru hampir tidak pernah.

Tidak ada markup di teks yang diucapkan: tanpa `<break>`, tanpa `[pause]`, tanpa bintang
penebal. Mesin suara membacanya sebagai kata, atau prosodinya rusak.

8. UJI BACA KERAS

Bacakan naskahnya. Tandai setiap tempat lidah tersandung. Tiga penyebab tersering:

- klausa terlalu panjang → pecah di koma;
- dua kata benda berdempet ("proses pemindahan kota") → ganti dengan kalimat;
- kata abstrak yang tidak punya gambar ("fenomena", "dinamika", "peristiwa") → ganti benda.

Kalau satu paragraf tidak bisa dibaca dalam satu napas, itu bukan paragraf untuk audio.

9. CONTOH: SEBELUM → SESUDAH

SEBELUM
"Pada tahun 1970, seorang perempuan ditemukan tewas di lembah Isdalen, Norwegia.
Seluruh label pada pakaiannya telah dihilangkan sehingga identitasnya tidak dapat
diidentifikasi."

SESUDAH
"Kenapa seseorang memotong semua label dari pakaiannya sendiri, lalu menghilang?
November 1970. Sebuah lembah di Norwegia. Tubuhnya terbakar dari depan,
punggungnya utuh, dan api itu tidak menyebar."

Yang berubah: pertanyaan di depan, tahun tidak memimpin, kalimat pendek,
benda konkret (label, punggung, api).

10. HUBUNGAN DENGAN GERBANG OTOMATIS

`tools/check_story.py` memeriksa bagian yang bisa dibuktikan mesin pada dokumen ini:
kata pengisi, kosakata laporan, jumlah sapaan, jumlah ajakan melihat, jumlah pertanyaan,
panjang hook, dan kebersihan markup untuk TTS.

Sisanya — apakah kalimat ini terasa seperti manusia — tidak bisa diperiksa mesin.
Itu tugas uji baca keras di §8, dan itu tidak boleh dilewati.
