# 00E — SUARA NARATOR: MENYAPA, BUKAN MEMBACAKAN LAPORAN

Catatan pemilik, 13 Nov 2026: *“visual udah bagus tapi VO script masih kurang di
storytelling-nya — masih terdengar membaca laporan, bukan berinteraksi dengan
penonton, dan sedang memberi tahu informasi.”*

Itu tepat. Naskah EP01–EP05 disusun sebagai **ringkasan peristiwa**: tanggal,
angka, lalu kesimpulan. Semua kalimatnya benar, tetapi tidak ada satu pun yang
berbicara **kepada** penonton. Tidak ada ajakan melihat, tidak ada pertanyaan yang
ditujukan, tidak ada “kamu”.

Dokumen ini mengunci suara itu supaya tidak kembali.

---

## 1 · TIGA PERBEDAAN YANG MENENTUKAN

| laporan (salah) | bercerita (benar) |
|---|---|
| “Negara memilih memindahkan kota, bukan memadamkan api.” | “Pemerintah tidak memilih memadamkan api. Mereka membayar warga untuk pindah.” |
| “1992. Negara mengambil seluruh kota.” | “Tahun 1992, negara mengambil seluruh kota. Tinggal di sana bukan lagi hakmu.” |
| “Api masih menyala hingga kini.” | “Apinya masih menyala. Di bawah jalan yang sekarang kosong.” |

Yang berubah bukan faktanya. Yang berubah: **siapa yang diajak bicara**, dan
**kapan** kejadiannya (sekarang, di depan mata, bukan “pada tahun itu”).

## 2 · ATURAN SUARA (diperiksa otomatis)

1. **Sapa penonton minimal tiga kali** dengan “kamu”/“kita” — bukan sebagai
   penutup, tetapi di tengah cerita.
2. **Minimal dua ajakan melihat**: *lihat, bayangkan, coba, ingat, dengar,
   perhatikan, pikirkan*. Ajakan ini yang membuat VO terdengar menunjuk layar.
3. **Minimal dua pertanyaan di dalam naskah** (selain hook): pertanyaan membuat
   penonton menjawab di kepala, dan itu terasa seperti percakapan.
4. **Satu ide satu kalimat.** Maksimal dua kalimat per baris VO (hook dan penutup
   boleh tiga). Kalimat panjang selalu terdengar seperti dibacakan.
5. **Dilarang kosakata laporan**: *diketahui, dilaporkan, tercatat, merupakan,
   disebutkan, berdasarkan, adapun, tersebut, sejumlah, berbagai, sedangkan,
   namun, sehingga, mengakibatkan, dilakukan, terjadi*. Kalau salah satu muncul,
   kalimatnya hampir pasti berbunyi seperti berita.
6. **Tanggal diucapkan seperti orang bercerita**: “Tahun 1981, …”, bukan
   “1981: …”. Angka tetap boleh, tetapi tidak boleh menumpuk — satu angka per
   baris, maksimal.
7. **Kata ganti orang, bukan jabatan.** “Mereka” untuk pelaku, “kamu” untuk
   penonton, “dia” untuk satu orang. “Pihak berwenang”, “ pemerintah daerah”,
   “warga setempat” membunuh suara.

## 3 · URUTAN YANG TETAP (dari `00B`)

Klimaks + entitas → cut + pertanyaan → cerita dari awal → turn → consequence →
loop. Suara baru tidak mengubah urutan; ia mengubah **cara mengucapkannya**.

## 4 · CONTOH: EP06 SEBELUM → SESUDAH

| baris | versi laporan (dipakai sampai EP05) | versi bercerita (dipakai EP06 ke atas) |
|---|---|---|
| hook | 1962. Lima petugas membakar sampah di atas tambang. Api itu masih menyala. | 1962. Api ini dinyalakan di bawah sebuah kota. Sekarang lihat rumahnya. |
| cut | Kenapa api sekecil itu tidak bisa dipadamkan selama enam puluh tahun? | Coba bayangkan api itu di bawah rumahmu. Kamu akan pindah ke mana? |
| relate | Kamu pernah tinggal di rumah yang sudah tidak aman, tapi tetap tinggal? | Kita sering bertahan, walau tahu tempatnya tidak aman. |
| turn | Negara memilih memindahkan kota, bukan memadamkan api. | Pemerintah tidak memilih memadamkan api. Mereka membayar warga untuk pindah. |
| penutup | Api yang mereka nyalakan untuk membersihkan sampah masih menyala di bawah kota. | Apinya masih menyala. Di bawah jalan yang sekarang kosong. |

Bedanya bisa diuji: versi kanan **tidak bisa dibacakan dengan nada berita**
tanpa terdengar aneh. Itu tujuannya.

## 5 · GERBANG

`python3 tools/check_story.py EPxx` sekarang punya dua lapis:

- lima efek (hook, celah, turn, echo) — tidak berubah;
- **suara narator** (§2 di atas) — baru, dan gagal kalau naskah kembali ke gaya
  laporan.

Naskah lama (EP01–EP05) sengaja dibiarkan: videonya sudah tayang, dan mengubah
naskahnya tidak mengubah apa pun di layar. Yang wajib memakai aturan ini adalah
setiap episode yang belum dirender, mulai EP06.

---

## 6 · HOOK: TUJUH PINTU MASUK, SATU LARANGAN

Keluhan kedua pemilik (13 Nov 2026): *“kalimat awalnya masih tidak punya hook…
gaya bahasanya masih terdengar orang yang baca koran, bukan yang sedang ngajak
ngobrol.”*

Penyebabnya bukan kata pembukanya, tetapi **kebiasaan membuka dengan tanggal**:
`1962. Api ini dinyalakan…` Itu kalimat pembuka berita. Tanggal adalah fakta yang
paling tidak menarik untuk didengar pertama, dan menaruhnya di depan memaksa
narator berhenti, mengambil napas, lalu membacakan. Penonton mendengarnya sebagai
pembaca, bukan sebagai teman ngobrol.

**Larangan:** hook tidak boleh diawali tahun/angka. Tanggal masuk nanti — sebagai
kejutan (“Sembilan belas tahun kemudian…”), bukan sebagai pintu.

### Tujuh pintu yang boleh dipakai

| pintu | bentuk | contoh untuk kasus nyata |
|---|---|---|
| **Pertanyaan** | pertanyaan yang penonton jawab di kepala | “Kamu pernah tinggal di rumah yang lantainya hangat, padahal di luar musim dingin?” |
| **Pernyataan** | kalimat datar yang isinya tidak masuk akal | “Ada kota di Pennsylvania yang menyala dari bawah.” |
| **Fakta** | satu angka yang mengejutkan, bukan tanggal | “Sebuah api sudah menyala di bawah kota ini lebih lama dari usia kamu.” |
| **Harapan** | keinginan sederhana yang lalu dilawan | “Mereka cuma ingin kotanya bersih sebelum libur panjang.” |
| **Khayalan** | ajakan membayangkan diri sendiri di sana | “Bayangkan lantai rumahmu hangat, dan kamu tidak tahu kenapa.” |
| **Adegan** | satu gambar yang bergerak | “Lima orang berdiri di tepi lubang tambang, membawa korek api.” |
| **Dialog** | kalimat yang pernah diucapkan | “‘Apinya tidak akan sampai ke rumah.’ Kalimat itu diucapkan tahun 1962.” |

Aturan memilih: **satu pintu saja per episode.** Dua pintu di kalimat pertama
terdengar seperti iklan. Sesudah pintu, langsung beri satu detail yang bisa
dilihat (benda, bagian tubuh, cuaca), bukan penjelasan.

### Ritme dan intonasi (yang membuatnya terdengar ngobrol)

1. **Panjang-pendek bergantian.** Kalimat pembuka boleh 10–14 kata; kalimat
   sesudahnya dipotong jadi 3–6 kata. Contoh: *“Ada kota di Pennsylvania yang
   menyala dari bawah. Api itu belum pernah mati.”*
2. **Satu kata yang ditekan per baris.** Bukan kapital di layar — pilih kata yang
   paling mengejutkan dan letakkan di akhir kalimat.
3. **Jeda = titik, bukan koma.** Di VO, koma hilang. Kalau butuh jeda, potong
   kalimatnya.
4. **Tanpa kata sambung pembuka.** “Sementara itu”, “Selain itu”, “Kemudian”
   adalah tanda orang membaca. Mulai langsung dari subjek.
5. **Ucapkan seperti memberi tahu teman di meja sebelah**, bukan mengumumkan di
   panggung: tidak ada “perlu diketahui”, tidak ada “menurut catatan”.
6. **Satu baris = satu tarikan napas.** Kalau satu baris tidak muat diucapkan
   dalam satu napas, baris itu terlalu panjang.

### Gerbang otomatis

`check_story.py` sekarang menolak hook yang diawali angka/tahun, dan mencatat
kalau hook lebih dari 12 kata.
