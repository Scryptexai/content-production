# Niche & sistem produksi — versi 3 (setelah pindah ke video-shotcraft)

## 1. Niche (tidak berubah)

Short-form vertikal yang membahas **kebijakan dan pemerintahan berbasis bukti**:
kritik pemerintah, hubungan antar negara, hubungan pejabat–rakyat.

Empat saringan sebelum satu klaim boleh masuk naskah:

1. **Ada sumber primer** yang bisa ditelusuri (jurnal, buku, data resmi) — bukan
   artikel agregator, bukan utas media sosial.
2. **Angkanya bisa disentuh**: kalau klaimnya "banyak", ia belum layak.
3. **Ada sudut pandang diri sendiri yang bisa diperiksa** (seperti Fowler & Hall
   pada klaim Achen–Bartels di EP01). Klaim yang tidak bisa gagal bukan klaim.
4. **Tidak menyebut partai, nama pejabat, atau negara sebagai sasaran.** Yang
   dikritik adalah mekanisme, bukan orang.

## 2. Sistem produksi sekarang

Satu alat: **video-shotcraft** (Remotion + kartu shot). Semua yang lain dihapus.

```
video/src/lib/     theme · motion · Stage · Table · Photo · Type · Layout · objects
video/src/shots/   enam shot per episode
video/public/      objects/*.png (hasil chroma key) + audio/{sfx,bgm}
video/tools/       key_objects.py (foto hijau → PNG transparan)
```

### Cara aset dibuat (ini yang diminta)

1. Foto objek dibuat dengan **latar hijau murni** (`#00FF00`), satu objek per foto.
2. `tools/key_objects.py` mengubahnya jadi **PNG transparan** dan memotong kotaknya
   rapat ke batas objek.
3. `Photo.tsx` menempatkannya sebagai **benda di dalam ruang**: parallax sendiri,
   bayangan kontak yang melebar saat naik, rim light mengikuti alfa, defokus, dan
   grade warna yang sama untuk semua objek.

Foto **tidak pernah** dipakai sebagai latar. Latar selalu `Stage` (ruangan dengan
lampu, berkas cahaya, debu, vignette, grain) + `Table` (meja berperspektif).

### Lima tipe shot yang dipakai ulang

| Tipe | Fungsi naratif | Kartu acuan | Dipakai |
|---|---|---|---|
| **spotlight** | satu objek harus jadi pusat perhatian | `spotlight-hero-card` | EP01 shot 01 |
| **fall** | banyak benda jatuh, satu per satu, ke satu titik | `deck-deal-flyin` | EP01 shot 02 |
| **scan** | memeriksa banyak titik, satu per satu | `chart-live-moves` | EP01 shot 03 |
| **orbit** | satu benda berubah wujud/perasaan | `space-camera-moves` | EP01 shot 04 |
| **assemble** | banyak benda jadi satu poster | `product-card-progressive-assemble` | EP01 shot 05 |
| **lockup** | merek mengunci, sumber tinggal | `logo-shrink-wordmark-lockup` | EP01 shot 06 |

Aturan pemilihan: **tipe dipilih dari fungsi naratif, bukan selera.** Kalau
kalimatnya memeriksa → scan. Kalau kalimatnya membandingkan → dua objek
berdampingan, bukan dua tipe digabung.

## 3. Struktur 60 detik (terbukti di EP01)

| Detik | Fungsi | Shot |
|---|---|---|
| 0–10 | kail: satu objek + satu peristiwa | spotlight |
| 10–20 | akibat yang terukur (angka) | fall |
| 20–32 | pemeriksaan ulang (titik balik) | scan |
| 32–43 | apa yang sebenarnya tersisa (analisis) | orbit |
| 43–53 | kembali ke penonton (pertanyaan) | assemble |
| 53–60 | merek + sumber | lockup |

Aturan waktu: satu shot 10–12 detik, satu gagasan per shot, angka mendarat
sekitar detik ke-10 dan ke-30.

## 4. Antrean episode

| EP | Klaim | Sumber | Tipe | Status |
|---|---|---|---|---|
| 01 | Yang dihukum bukan yang berwenang | Achen & Bartels 2016 bab 5; Fowler & Hall 2018 | spotlight, fall, scan, orbit, assemble, lockup | **selesai** |
| 02 | Yang dipakai mengukur kursi lama (promosi dari kinerja jabatan sebelumnya) | Benson, Li & Shue, *QJE* 134(4) 2019 | fall, scan, assemble | berikutnya |
| 03 | Bencana mengubah suara — hanya kalau bantuannya tidak datang | Healy & Malhotra, *APSR* 103(3) 2009 | scan, fall | rencana |
| 04 | Apa yang sebenarnya dihitung saat pemerintah mengumumkan "berhasil" | **belum dipilih** | — | **terkunci** |

EP04 tidak boleh dikerjakan sebelum sumbernya dipilih.

## 5. Yang masih kurang

- **VO belum direkam** untuk episode mana pun. Naskah siap.
- **Aset objek masih enam.** EP02 butuh minimal dua objek baru (mis. kursi, tangga)
  supaya tidak terasa mengulang EP01.
- **Belum ada episode yang memakai data instansi Indonesia.** Dua episode pertama
  memakai data Amerika dan menyebutnya di layar; itu jujur, tetapi belum menjawab
  "bagaimana di Indonesia".
- **Render 26 menit per 60 detik** di mesin 2 core. Bukan masalah untuk satu
  episode; akan jadi masalah untuk 3 video/hari. Pilihan: mesin lebih besar, atau
  durasi 30–45 detik untuk sebagian slot.
