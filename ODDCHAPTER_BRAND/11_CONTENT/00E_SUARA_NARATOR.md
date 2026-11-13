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
