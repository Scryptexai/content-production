# Niche, naskah, dan templat scene — cara kerja yang bisa diulang 3× sehari

Dokumen ini menjawab satu pertanyaan yang menentukan: **bagaimana 3 video/hari
bisa dibuat tanpa menulis scene baru setiap kali.**

Jawabannya bukan "lebih cepat mengetik". Jawabannya: **lima tipe scene yang
dipakai ulang**, dan naskah yang dipaksa cocok dengan tipe itu — bukan
sebaliknya.

---

## 1. Niche yang dipilih

**Kritik pemerintah & hubungan pejabat–rakyat, berbasis bukti, tidak partisan.**

Ini bukan pilihan selera. Ini pilihan yang lolos empat saringan:

| Saringan | Kenapa lolos |
|---|---|
| Ada literatur akademik yang bisa dikutip | ilmu politik & ekonomi politik punya puluhan tahun data tentang perilaku memilih, akuntabilitas, birokrasi |
| Tidak butuh footage atau wajah | semuanya bisa digambar: diagram, angka, simpul, tangga |
| Bisa dikritik tanpa jadi kampanye | kritik diarahkan ke **mekanisme** ("bagaimana kita menilai"), bukan ke tokoh |
| Tidak melanggar aturan kanal | tidak ada diagnosis, tidak ada kutipan fiktif, tidak ada klaim motif |

**Yang dilarang di niche ini** (sudah dicatat juga di `SCRIPT-EP01.md`):

- menyebut partai, nama pejabat, atau negara tertentu sebagai sasaran
- "rakyat itu bodoh" — itu penghinaan, bukan analisis
- klaim tanpa angka yang bisa dilacak
- menyembunyikan hasil yang menolak klaim kita sendiri

---

## 2. Aturan naskah (checklist, wajib lulus semua)

Naskah yang tidak lulus salah satu poin di bawah **tidak masuk produksi**.

1. **Satu klaim utama per episode.** Kalau ada dua, pecah jadi dua episode.
2. **Klaim utama bisa dinyatakan dalam satu kalimat tanpa angka.** Angka
   datang setelah kalimat itu, bukan sebagai gantinya.
3. **Ada satu titik balik.** Episode tanpa titik balik adalah ceramah.
   Titik balik yang paling kuat: **temuan yang menolak klaim kita sendiri.**
4. **Setiap angka punya sumber primer**, dan sumbernya ditulis di frame.
5. **Fakta, tafsiran, dan spekulasi ditandai beda.** "Penelitian menemukan X"
   ≠ "artinya Y".
6. **Tidak ada kalimat yang hanya mengulang gambar.** Teks menjelaskan apa yang
   tidak bisa digambar; gambar menunjukkan apa yang tidak perlu dijelaskan.
7. **60 detik = 150–170 kata.** Lebih dari itu, VO akan bertabrakan dengan
   teks di layar.
8. **Kalimat terakhir harus pertanyaan yang berlaku untuk penonton**, bukan
   kesimpulan yang mengulang.

### Struktur 60 detik yang dipakai EP01

| Detik | Fungsi | Isi |
|---|---|---|
| 0–6 | **kail** | satu pernyataan yang membuat orang berhenti menggulir |
| 6–18 | **kasus** | satu peristiwa konkret + angka pertama |
| 18–34 | **mekanisme** | apa yang sebenarnya diukur; ini inti episodenya |
| 34–47 | **titik balik** | bukti yang menolak kasus tadi |
| 47–60 | **kembali ke penonton** | apa yang tersisa setelah angkanya runtuh |

Blok **mekanisme** adalah yang membedakan kanal ini dari konten "fakta unik".
Tanpa blok itu, video hanya jadi trivia.

---

## 3. Lima tipe scene

Semua ada di `film/kit/kit.js` dan dipakai di `film/scenes/`.

| Tipe | Fungsi naratif | Kode | Dipakai di |
|---|---|---|---|
| **climb** | perpindahan, perjalanan, "naik" | `stairs()` | belum dipakai di episode jadi |
| **count** | angka yang perlu **penyebut** (3 dari 100) | `dotPct()` | EP01 (3,2 dari 100) · EP02 (4 dari 100) |
| **split** | dua hal dibandingkan, berubah bentuk | `barPair()` | EP01 (−10 vs −0,5) · EP02 (0 vs +30 %) |
| **board** | banyak entitas + satu yang bergerak di antaranya | `board()` | EP02 (satu orang naik lima jenjang) |
| **knot** | sesuatu yang diikat / mengendor / lepas | `trefoil()` + `thread()` | EP01 (temuan yang mengendor) |

Aturan pemakaian:

- **Satu scene = satu tipe.** Jangan gabung dua tipe dalam satu frame; mata
  kehilangan fokus dan teks jadi satu-satunya penjelas.
- **Tipe dipilih dari fungsi naratif, bukan dari selera.** Kalau kalimatnya
  membandingkan dua angka → `split`. Kalau menyebut proporsi → `count`.
  Kalau menyebut proses yang bisa dibatalkan → `knot`.
- **Teks tidak pernah jadi tipe scene.** Di riset sendiri: teks di atas 56 px
  (16:9) / 46 px (9:16) membuat penonton membaca, bukan menonton.
- **Grafik selesai sebelum 940 px layar.** Versi pertama EP02 melanggar ini:
  grid 10×10 dengan jarak 50 px menembus kepala karakter.
- **Setiap objek yang seolah dipegang karakter wajib punya penghubung ke
  tangan** (`thread()`). Tanpa itu penonton membacanya sebagai logo melayang.
- **`dotPct.update()` menerima JUMLAH titik, bukan pecahan.** `0.04` tidak
  menyalakan 4 titik — itu menyalakan nol koma nol empat titik. Untuk "4 dari
  100" tulis `4`. Kesalahan ini sempat terjadi di EP02.

---

## 4. Peta waktu standar

Setiap episode 60 detik punya **empat stasiun** dan **tiga perjalanan**.
Karakter berjalan di antara stasiun; kamera mengikuti pinggul, jadi kaki
menapak di tempat dan tidak ada foot-slide.

```
 0 ──── 6         18 ──── 22,6     34 ──── 38,6        60
 │ jalan │ stasiun 1 │ jalan │ stasiun 2 │ jalan │ stasiun 3 │
 │       │  6–18     │       │  22,6–34  │       │  38,6–60  │
```

Angka ini bukan hiasan: 6 dtk cukup untuk membaca satu kalimat + melihat satu
grafik tumbuh, dan 11 dtk di stasiun terakhir cukup untuk dua putaran teks.

---

## 5. Alur produksi satu episode (target: 45 menit)

| Langkah | Waktu | Alat |
|---|---|---|
| 1. Pilih klaim + cari sumber primer | 10 mnt | pencarian web; simpan DOI |
| 2. Tulis naskah 8 poin + cek checklist §2 | 10 mnt | `docs/SCRIPT-EP01.md` sebagai contoh |
| 3. Petakan ke 5 tipe scene | 5 mnt | tabel seperti §4 |
| 4. Salin `scenes/ep01`, ganti angka & teks | 10 mnt | jangan sentuh `kit.js` |
| 5. Render masih + cek 3 hal | 3 mnt | `--stills 9,31,48` |
| 6. Render penuh + mux bunyi | 5 mnt | 1800 frame ≈ 6 mnt di mesin 2-core |

Langkah 6 adalah satu-satunya yang tidak bisa dipercepat dengan mengetik lebih
cepat — dan itu sudah 20× lebih cepat dari pipeline Remotion lama.

---

## 6. Antrean episode (klaim sudah dipilih, sumber sudah dicatat)

| EP | Klaim | Sumber | Tipe dominan |
|---|---|---|---|
| 01 | Yang dihukum bukan yang berwenang (serangan hiu 1916) | Achen & Bartels 2016 bab 5; Fowler & Hall 2018 | count, split, knot |
| 02 | Promosi berdasarkan kinerja lama, bukan kinerja jabatan baru | Benson, Li & Shue, *QJE* 134(4) 2019 | board, split |
| 03 | Bencana alam mengubah suara — tapi hanya kalau bantuannya tidak datang | Healy & Malhotra, *APSR* 103(3) 2009 | count, split |
| 04 | Apa yang sebenarnya dihitung ketika pemerintah mengumumkan "berhasil" | perlu sumber primer — **belum dipilih** | count |

**EP04 belum boleh dikerjakan** sampai sumbernya dipilih. Aturan §2 poin 4
mengikat: tidak ada angka tanpa sumber primer.

---

## 7. Yang masih kurang (jujur)

- **VO belum ada.** Naskah siap dibaca, tapi belum direkam. Tanpa VO, video ini
  masih "video bergerak dengan teks", bukan narasi.
- **Dua episode jadi (EP01, EP02).** EP03–04 masih rencana.
- **`board` vertikal sudah ada** (ditulis untuk EP02), tapi baru diuji sampai
  6 jenjang × 8 kolom. Di atas itu jarak antar titik jatuh di bawah 40 px dan
  board berhenti terbaca di 9:16.
- **Karakter belum bisa memegang objek.** Semua interaksi masih berupa
  benang; butuh klip `grip` kalau scene berikutnya butuh pegangan.
- **Belum ada episode yang memakai instansi pemerintah sebagai data.** EP01
  dan EP02 sama-sama meminjam data dari Amerika (pemilu kota, penjualan
  perusahaan) dan menyebutnya di layar. Ini jujur, tapi belum menjawab
  pertanyaan "bagaimana di Indonesia".
