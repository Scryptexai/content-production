# EP02 — "Yang dipakai mengukur kursi lama"

60 detik · 1080×1920 · 30 fps · satu pengambilan tanpa potongan
Berkas: `film/scenes/ep02/index.html` · bunyi `make_sfx.py --preset ep02`

---

## 1. Aturan yang mengikat episode ini

Sama seperti EP01, ditambah tiga aturan baru hasil revisi EP01:

1. **Objek yang seolah dipegang wajib punya penghubung ke tangan.** Tanpa
   benang, simpul EP01 terbaca sebagai logo yang melayang. Di EP02 tidak ada
   objek yang dipegang, jadi aturan ini tidak dipakai — tetapi tetap berlaku
   untuk episode berikutnya.
2. **Tidak boleh ada dua teks dengan jendela waktu bertumpuk di pita yang
   sama.** Diperiksa per pita, bukan per episode.
3. **Grafik selesai di bawah 940 px layar.** Versi pertama EP02 memakai grid
   10×10 dengan jarak 50 px; baris terakhirnya menembus kepala karakter.
   Sekarang jarak 42 px dan grid digeser ke atas (`cy = Y_CHART − 34`).

Aturan naskah (dari `NICHE-AND-TEMPLATES.md`): bedakan fakta / tafsiran /
analisis, sebut sumber, tanpa nama pejabat, tanpa partai, tanpa negara sebagai
sasaran.

---

## 2. Bukti dan cara memakainya

Satu sumber utama, satu sumber pendahulu.

| Klaim | Angka | Sumber |
|---|---|---|
| Ukuran sampel | 131 perusahaan, 38.843 penjual, 1.553 dipromosikan, 2005–2011 | Benson, Li & Shue, "Promotions and the Peter Principle", *QJE* 134(4) 2019, 2085–2134, doi:10.1093/qje/qjz022 (Bagian III, Tabel I) |
| Peluang promosi | 4,00 % di dalam sampel (hazard bulanan 0,23 %) | sama, Tabel I |
| Penjualan → promosi | penjualan dua kali lipat → peluang promosi **+14,3 %** dari dasar | sama, Tabel IV kolom 4 |
| Penjualan → mutu manajer | penjualan dua kali lipat sebelum promosi → penjualan **tiap bawahan −7,5 %** | sama, Tabel V kolom 2 |
| Kontrafaktual | memilih calon manajer terbaik (bukan penjual terbaik) → mutu manajemen **+30 %** | sama, Bagian V; penulis menyebutnya **batas bawah** |
| Asal gagasan | "setiap orang naik sampai batas ketidakmampuannya" | Peter & Hull, *The Peter Principle*, 1969 |

Dua hal yang **tidak** diklaim:

- Ini **bukan** data instansi pemerintah. Sampelnya penjual di perusahaan
  Amerika. Kalimat itu muncul di layar pada 53,0–60 dtk, bukan dihapus.
- +30 % adalah hasil hitungan kontrafaktual, bukan hasil percobaan. Kalimat
  di layar menyebutnya "hitungan kontrafaktual" di pita sumber.

---

## 3. Naskah di layar (60 detik)

Semua baris ini yang benar-benar dirender; urutannya mengikuti pita.

**0–6,4 · masuk, satu pengambilan**
- Setiap naik satu jenjang,
- yang dinilai kerja di jenjang sebelumnya.

**6,4–18 · stasiun 1 — hitung (`dotPct`)**
- pita atas: 2005–2011 · 131 PERUSAHAAN
- 38.843 penjual. 1.553 di antaranya naik.
- **4 dari 100** (58 px, rose)
- naik jadi manajer dalam satu tahun.
- sumber: Benson, Li & Shue, QJE 2019

Gerak: 100 titik muncul, 4 menyala satu per satu (9,2 / 10,4 / 11,6 / 12,7).

**18–22,6 · jalan**

**22,6–34 · stasiun 2 — board**
- pita atas: YANG DIPAKAI MENILAI: PENJUALAN
- Penjualan dua kali lipat / menaikkan peluang promosi 14,3 %.
- **−7,5 %** (58 px, rose)
- penjualan tiap bawahan, sesudah dia jadi manajer.
- makin tinggi penjualannya, makin turun timnya.

Gerak: 48 titik di enam jenjang. Satu titik (kolom 4) naik dari jenjang
terbawah ke teratas dalam 2,8 dtk, melewati lima jenjang; setiap jenjang yang
dilewatinya meredup sampai 0,95 — tangga yang ia naiki sekaligus menjadi
orang-orang yang sekarang diukur dengan ukurannya.

**34–38,6 · jalan**

**38,6–60 · stasiun 3 — split + sumbu**
- pita atas: BILA YANG DIPILIH BUKAN PENJUAL TERBAIK
- Kualitas manajemen 30 % lebih tinggi / bila yang dipilih adalah calon
  manajer terbaik.
- Batang: SEKARANG = 0 · PILIH CALON MANAJER = +30 %
- Sumbu 0–10–20–30–40 poin persentase. Tanpa sumbu, tinggi batang hanya gambar.

**Penutup (48,6–60)**
- Yang salah bukan orang yang naik.
- **Yang salah ukuran yang dipakai menaikkan.**
- Ini data penjualan perusahaan Amerika, bukan instansi pemerintah.
- sumber: Benson, Li & Shue, QJE 2019 · Peter & Hull, 1969

---

## 4. Peta bunyi (`--preset ep02`)

| Waktu | Bunyi | Alasan |
|---|---|---|
| 0–6,4 / 18–22,6 / 34–38,6 | 12 langkah, lantai keras (320–3800 Hz, 58 Hz dengung ruangan) | interior, bukan pesisir seperti EP01 |
| 9,2 · 10,4 · 11,6 · 12,7 | 4 klik tipis (2400–8200 Hz) | tiap titik menyala |
| 12,9 | nada 98 Hz | angka "4 dari 100" mendarat |
| 26,2–29,1 | glide 196 → 392 Hz + 5 ketukan 0,56 dtk | satu orang naik lima jenjang |
| 29,0 | thud 72 Hz | baris di bawahnya meredup |
| 39,7–42,3 | gesekan pita (500–3200 Hz) | dua batang tumbuh |
| 41,0 | 261,6 + 392 Hz | "+30 %" muncul |
| 48,6 · 49,9 | 146,8 Hz · 110 Hz | dua baris penutup |
| 54,8 | akor 73,4 / 110 / 146,8 Hz, reverb 0,30 | menutup, tidak menggelembung |

Puncak 0,74; fade masuk 0,6 dtk; fade keluar 1,2 dtk. Sama dengan EP01 supaya
dua episode bisa diputar berurutan tanpa lompatan volume.

---

## 5. Yang masih kurang

- **Belum ada data instansi pemerintah.** Itu bukan kelalaian episode, itu
  batas bukti yang ada; disebut di layar. Kalau nanti ada studi promosi PNS
  dengan angka yang bisa ditelusuri, episode ini harus dibuat ulang.
- **Board 48 titik tidak mewakili 38.843 orang.** Ia mewakili *struktur* enam
  jenjang; angka sebenarnya ada di pita teks. Jangan pernah menyebut 48 titik
  sebagai sampel.
- **Karakter selalu berdiri di kiri grafik.** Kontinuitas bagus, tapi tiga
  episode dengan komposisi identik akan terasa seperti templat. Episode
  berikutnya perlu satu scene dengan karakter di kanan atau membelakangi
  kamera.
