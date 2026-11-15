# 15 · Desain informasi ala NERROR — dipelajari, lalu diterapkan ke OODCHAPTER

Dokumen kerja. Yang diambil dari Nessie Judge bukan suaranya, bukan genrenya yang
horor, dan bukan judulnya yang berteriak. Yang diambil satu hal: **cara ia
mengurutkan informasi sampai penonton menyimpulkan sendiri.**

Diperiksa mesin: `python3 tools/check_info_design.py` (tujuh cek A–G).
Naskah juga tetap harus lulus `tools/check_story.py`.

---

## 1 · Kenapa contohnya relevan

NERROR adalah segmen misteri/kasus/konspirasi di kanal Nessie Judge. Genre-nya
sama dengan OODCHAPTER: satu peristiwa nyata, satu hal yang tidak selesai, dan
penonton yang datang untuk tahu "kenapa". Bedanya cuma dua: ia punya 10–30 menit,
kita 35–45 detik; ia boleh main horor, kita tidak boleh mengarang.

Justru karena genre-nya sama, kesalahan kita kelihatan jelas saat dibandingkan.
Dua kajian akademik tentang NERROR menyebut hal yang sama tanpa saling menyalin:

- penjelasannya **selalu mulai dari kronologi**, lalu teori, lalu hasil kasus
  terbaru — penonton yang awalnya tidak paham akhirnya ikut menyimpulkan;
- isinya bergerak **tesa → antitesa → sintesa**: klaim resmi, lawan klaim, lalu
  pembacaan yang menyatukan keduanya;
- sumber ditampilkan, bukan disebut samar ("menurut penelitian") — ada kutipan
  dan potongan berita di layar;
- penonton **diundang memutuskan**; kolom komentar adalah bagian dari formatnya.

Itu bukan bakat, itu arsitektur. Arsitektur itu yang kita tiru.

## 2 · Tujuh mekanisme, dan padanannya di kanal kita

| # | NERROR | OODCHAPTER | Cek mesin |
|---|---|---|---|
| A | mulai dari **kronologi** (tanggal, tempat, satu detail membosankan) | beat `setup` wajib memuat tanggal/bulan + tempat, sebelum ada tafsir | `A` |
| B | **petunjuk dulu, putusan belakangan**; tidak ada "berarti…" di awal | kata putusan (`berarti`, `terbukti`, `jadi jelas`, `seharusnya`) hanya boleh muncul di/di selepas `turn` | `B` |
| C | **kesimpulan dikarantina**: satu, di satu tempat, dan ada yang mengatakannya | kesimpulan hanya di beat `turn`, wajib bertribusi (`bilang`, `menurut`, kutipan) | `C` |
| D | **pertanyaan yang tidak dijawab** tetap dipegang sampai akhir | field `celah` + `loop` berupa pertanyaan; `celah` tidak boleh dijawab di naskah | `D` |
| E | **tesa–antitesa–sintesa**: klaim resmi dilawan bukti, lalu dibacakan | `turn` = klaim + lawan klaim (`bukan … tapi`), `turn_verdict` = sintesa kanal | `E` |
| F | **bukti yang bisa ditunjuk**: angka, jarak, jam, kutipan di layar | ≥3 beat memuat angka/tanggal/jarak; setiap angka di VO muncul juga di `cues`/`stamps` | `F` |
| G | **suara penyelidik**, bukan hakim; penonton diajak | ≥2 sapaan `kamu/kita`; tidak ada tuduhan mutlak (`pelakunya adalah …`) tanpa atribusi | `G` |

## 3 · Bahasa: pola kalimat yang dipinjam

Bukan diksi horornya — pola informasinya. Semua di bawah lolos aturan editorial
kita (tanpa `misteri`/`aneh`/`ternyata`, tanpa kalimat ringkasan).

1. **Pintu kronologi** — "29 Mei 2006, Porong. Air keruh muncul di sawah, lalu ke jalan."
   Tanggal + tempat + satu detail fisik yang membosankan. Itu yang membuat
   kejadian berikutnya terasa nyata.
2. **Paradoks pembuka** — "Tanah keluar dari dalam tanah, dan tidak ada yang bisa menutupnya."
   Benda konkret + satu hal yang tidak masuk akal, tanpa kata sifat.
3. **Jarak sebagai petunjuk** — "Sumur gas itu cuma 150 meter dari titik semburan."
   Angka yang bisa diperiksa lebih kuat daripada kata "dekat".
4. **Pemisah klaim** — "Perusahaan bilang ini bencana alam. Ahli geologi bilang bukan
   getarannya, tapi sumur gas itu." Dua kalimat pendek, dua pihak, tanpa narator
   memihak di kalimat itu.
5. **Sintesa kanal** — `turn_verdict`: "Getarannya terlalu jauh. Yang paling dekat bukan
   patahan, tapi sumur bor." Narator boleh menyimpulkan **setelah** dua klaim berdiri.
6. **Ekor yang tidak ditutup** — "Tanah itu masih keluar. Kamu pindah?"
   Pertanyaan yang jawabannya bukan di video ini, tapi di kepala penonton.

Yang **tidak** dipinjam: "Shits About to Go Down", campur bahasa Inggris, judul
huruf besar berteriak, suasana mistis, dan penilaian "mengerikan". Semuanya
bertabrakan dengan `EDITORIAL-FONDATION.md` dan dengan pembatasan iklan.

## 4 · Struktur 10 slot (35–45 detik)

Sama seperti `content_data.py` kita, urutannya yang diubah bukan jumlahnya:

| slot | bagian | isi | soal yang dijawab |
|---|---|---|---|
| 0 | `hook` | paradoks/pernyataan + benda konkret | "apa yang tidak masuk akal?" |
| 1 | `tanya` | satu pertanyaan saja | "apa yang mau kita cari?" |
| 2 | `relate` | taruhan penonton (`kamu`, `kita`) | "kenapa saya peduli?" |
| 3 | `setup` | tanggal + tempat + detail fisik | "kapan, di mana?" |
| 4 | `tension` | petunjuk 1: kejanggalan pertama | "kok bisa?" |
| 5 | `tension` | petunjuk 2: angka/jarak yang terukur | "seberapa dekat/jauh?" |
| 6 | `tension` | petunjuk 3: detail yang terlalu pas | "kenapa persis di situ?" |
| 7 | `turn` | klaim resmi vs bukti + bacaan kanal | "siapa yang bilang apa?" |
| 8 | `consequence` | harga yang dibayar, konkret | "lalu kenapa itu penting?" |
| 9 | `loop` | pertanyaan terbuka, memanggil kata dari hook | "kalau kamu, bagaimana?" |

Aturan tambahan yang menempel di struktur ini:

- **Tidak ada fakta baru setelah `turn`.** Kalau muncul angka baru di
  `consequence`, itu twist murah; pindahkan ke salah satu `tension`.
- **Satu celah per episode.** `celah` ditulis sekali, dipakai di `hook`/`loop`,
  dan **tidak dijawab**. Kalau dijawab, episode itu kehilangan fungsinya.
- **Setiap angka di VO punya pasangan di layar** (`cues`, `stamps`, caption).
  Di NERROR ini bentuknya kutipan berita; di kita bentuknya label teks.

## 5 · Evaluasi naskah kanal: 21 episode, 15 Nov 2026

`python3 tools/check_info_design.py` — skor 7 = semua mekanisme ada.

| cek | lulus | artinya kalau gagal |
|---|---|---|
| A kronologi dulu | 12/21 | penonton tidak tahu kapan peristiwanya; cerita kehilangan pijakan |
| B petunjuk dulu | **21/21** | (sudah kuat) kita tidak pernah mendahulukan putusan |
| C karantina kesimpulan | **21/21** | (sudah kuat) satu kesimpulan, bertribusi |
| D pertanyaan tertahan | 16/21 | 5 episode menutup celahnya sendiri |
| E tesa–antitesa–sintesa | **9/21** | klaim resmi disebut, lawannya tidak; penonton tidak diajak menimbang |
| F bukti bisa ditunjuk | **5/21** | episode berjalan dengan kata sifat, bukan angka |
| G suara penyelidik | 17/21 | 4 episode tanpa sapaan atau menuduh mutlak |

Rata-rata 4,81/7; 18 episode belum penuh. Yang lulus 7/7: **EP16, EP20** (dan EP11
sesudah ditulis ulang).

Diagnosis jujur, dalam bahasa produksi:

1. **Kita jago menahan kesimpulan (B, C) tetapi miskin bukti terukur (F).**
   Naskah kita berbunyi seperti penyelidik yang sudah tahu jawabannya dan memilih
   kata-kata yang bagus. NERROR selalu punya satu angka yang bisa dicek penonton.
2. **Kita hampir tidak pernah menghadirkan dua klaim yang bertarung (E).**
   Padahal justru di situ penonton merasa diajak berpikir, bukan diajari.
3. **Tiga perempat episode membuka tanpa tanggal (A).** Hook memang harus tanpa
   tahun, tetapi beat ketiga wajib punya — dan sering tidak ada.
4. **Lima episode menutup celahnya sendiri (D).** Loop yang menjawab pertanyaan
   mematikan komentar, dan komentar adalah satu-satunya sinyal yang menaikkan
   distribusi Shorts kita.

### Contoh nyata: EP02 (2/7) — contoh perbaikan, naskahnya tidak diubah karena sudah tayang

| sekarang | masalah | perbaikan |
|---|---|---|
| hook: "1 Februari 1959. Sembilan pendaki memotong tenda dari dalam…" | dibuka dengan tanggal (aturan hook), dan tidak ada satu angka pun di beat | hook: "Sembilan orang memotong tenda dari dalam, lalu keluar tanpa sepatu." |
| beat `tension`: "Jejak kaki turun ke hutan…" | jarak tanpa angka | "Jejak kaki turun 1,5 kilometer ke hutan. Sebagian hanya berkaus kaki." |
| `turn`: "Enam puluh tahun dugaan: pasukan, monster, senjata rahasia." | daftar tuduhan, bukan dua klaim yang bertarung | "Penyelidik Soviet bilang pasukan. Dua insinyur salju bilang longsoran. Hampir semua luka itu cocok." |
| tanpa sapaan | penonton tidak diajak | `relate`: "Kamu pernah tidur di tempat asing, dan dengar bunyi di luar tenda?" |

### Contoh nyata: EP11 (Porong) — sudah ditulis ulang, 6/7 → 7/7

| sebelum | sesudah | mekanisme |
|---|---|---|
| "Tanah di Porong mengeluarkan lumpur, dan 20 tahun kemudian masih keluar." | "Tanah keluar dari dalam tanah, dan tidak ada yang bisa menutupnya." | hook paradoks, tanpa tahun |
| "Mei 2006, Porong, Sidoarjo. Awalnya cuma air keruh di sawah." | "29 Mei 2006, Porong. Air keruh muncul di sawah, lalu ke jalan." | kronologi (A) |
| "Dua hari sebelumnya, tanah di Yogyakarta berguncang." | "Dua hari sebelumnya, 27 Mei, tanah di Yogyakarta berguncang." | angka (F) |
| "Ahli geologi bilang getaran itu terlalu jauh. Yang paling dekat bukan sesar, tapi sumur gas." | "Perusahaan bilang ini bencana alam. Ahli geologi bilang bukan getarannya, tapi sumur gas itu." | tesa–antitesa (E) |
| "Tanah itu masih mengeluarkan lumpur. Kamu akan tinggal di sana?" | "Tanah itu masih keluar. Kamu pindah?" | celah tetap terbuka (D) |

Sekalian diperbaiki: field `visual` EP11 masih berisi kertas printer 6EQUJ5 (sisa
naskah Wow! signal yang menimpa data Porong), dan override mati `_SHORT_2026`
untuk EP11 dihapus supaya tidak ada lagi data nyasar.

## 6 · Episode dengan VO pemilik (EP09, EP10, dan seterusnya)

Episode yang narasinya direkam pemilik **tidak boleh diubah teksnya**
(`00_RULEBOOK` §13). Untuk episode itu, desain informasi dipindahkan ke bagian
yang masih milik kanal:

- **`cues` dan `stamps`** memikul mekanisme F: setiap angka di VO diberi label
  yang muncul di layar (`1981`, `150 METER`, `27 NOVEMBER`).
- **`turn_verdict`** memikul E: klaim resmi dan lawannya ditulis sebagai teks
  layar saat turn, bukan diucapkan ulang.
- **`celah` + `loop` + caption TikTok** memikul D: pertanyaan yang diucapkan VO
  diulang di caption, dan komentar diminta di sana.
- **`description`** memikul A: kronologi lengkap dengan tanggal ditulis di tiga
  baris pertama deskripsi, karena VO tidak menyebutnya.

Artinya: mekanisme A–G tetap berlaku, tetapi dieksekusi di lapisan teks-layar,
bukan di lapisan suara. Jangan menilai episode VO dengan skor naskahnya saja.

## 7 · Yang tidak ditiru

| jangan | kenapa |
|---|---|
| suasana horor, "mengerikan", klaim mistis | `EDITORIAL-FONDATION.md`: kanal ini kasus nyata, bukan horor. Ada korban yang keluarganya masih hidup |
| campur bahasa Inggris sebagai gaya | menambah kata tanpa menambah informasi; TTS juga salah melafalkan |
| judul berteriak + huruf besar semua | kita sudah punya aturan hook ≤12 kata, tanpa tahun di depan |
| spekulasi tanpa atribusi | NERROR menampilkan sumber; kita wajib menulis `sumber` dan memisahkan fakta/tafsir |
| durasi panjang, banyak babak | Shorts 35–45 detik; satu celah, satu putaran |

## 8 · Cara memakai dokumen ini

```bash
python3 tools/check_info_design.py            # tabel 21 episode
python3 tools/check_info_design.py EP11 -v    # rincian per cek
python3 tools/check_info_design.py --strict   # gerbang: keluar 1 kalau ada yang gagal
python3 tools/check_story.py EP11            # gerbang lama tetap wajib
```

Urutan menulis yang dipakai mulai EP11:

1. Tulis **kronologi** dulu (tanggal, tempat, satu detail fisik).
2. Daftar **tiga petunjuk** yang bisa ditunjuk — kalau tidak ada angka, cari.
3. Tulis **klaim resmi** dan **lawan klaimnya** dalam satu beat `turn`.
4. Tulis **sintesa** kanal di `turn_verdict`, bukan di VO.
5. Tulis **celah** yang tidak akan dijawab. Lalu hook, baru terakhir loop.
6. Jalankan dua gerbang. Kalau E atau F merah, jangan menulis ulang seluruh
   naskah — tambahkan satu angka dan satu lawan klaim.
