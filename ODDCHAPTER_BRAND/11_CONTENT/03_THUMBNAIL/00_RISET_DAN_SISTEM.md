# RISET & SISTEM THUMBNAIL — EP01–EP08
### 16:9 · 1280×720 (render 1920×1080) · siluet tanpa wajah · palet kanal

Dokumen ini mencatat apa yang **dibaca dan diuji** sebelum satu gambar pun dibuat,
lalu mengunci sistem desain yang dipakai untuk 8 thumbnail. Tujuannya: delapan
gambar ini harus terlihat seperti satu keluarga, bukan delapan poster berbeda.

---

## 1. Yang dibaca (dan apa yang diambil)

| sumber | temuan yang dipakai | yang dibuang |
|---|---|---|
| Backlinko/tubeanalytics, ringkasan CTR 2026 | thumbnail kustom ±35% lebih baik dari otomatis; CTR niche true crime/misteri 6–12%; judul & thumbnail bekerja sebagai satu sistem | "wajah manusia selalu menang" — untuk kanal ini wajah AI justru melemahkan kredibilitas |
| ampifire, panduan thumbnail 2026 | **0–3 kata** outperform teks panjang; 12 karakter ke bawah paling kuat; >3 elemen visual turunkan CTR ±23% | angka absolut yang tidak bisa diverifikasi |
| 1of10, 9 tips komposisi | subjek di titik rule-of-thirds; 30–40% ruang negatif; kontras minimum 4.5:1; outline teks 4–8 px; teks 60–80 pt di kanvas 1280 | — |
| henrydavidphotography, panduan 2026 | subjek mengisi ≥60% frame; komposisi diagonal lebih hidup; teks di paruh atas; hindari sudut bawah (tertutup UI YouTube) | — |
| key-g, panduan 2025 | batasi 2–3 hue; satu aksen warna; stroke 3–6 px; cek "squint test" di 120 px | teks hingga 6 kata (terlalu panjang untuk kanal ini) |
| formula pemilik (dokumen 7 bagian) | urutan: attention → awareness → curiosity; thumbnail menyampaikan **apa yang salah**, judul menjelaskan kenapa | clickbait palsu, banyak panah/lingkaran/tanda seru |

**Kesimpulan yang paling menentukan:** pada ukuran ponsel, thumbnail ini dibaca
sebagai **satu bentuk + dua sampai tiga kata**. Karena itu setiap gambar dibuat
dari satu subjek besar (siluet), satu sumber cahaya, dan satu baris teks.

---

## 2. Kenapa siluet, bukan wajah

Pemilik memilih **siluet/punggung saja**. Itu keputusan yang tepat untuk kanal ini,
dan alasannya bukan selera:

· Kasus di kanal ini tentang **orang yang hilang** atau **orang yang sudah meninggal**.
  Wajah AI yang jelas akan menjadi klaim visual palsu — penonton merasa dibohongi
  saat video menyebut tidak ada foto korban.
· Siluet dari belakang memaksa penonton **mengisi wajahnya sendiri**. Itu curiosity
  gap yang jauh lebih kuat daripada ekspresi ketakutan yang generik.
· Secara produksi, siluet bisa diulang delapan kali tanpa terlihat seperti template
  yang sama, karena yang berubah adalah tempat dan benda.

---

## 3. Palet (dikunci, tidak boleh digeser per episode)

| peran | kode | pemakaian |
|---|---|---|
| Ink | `#17191D` | bayangan, stroke teks, langit malam, scrim |
| Ivory | `#F4F0E8` | teks utama, kabut, salju, lampu |
| Sage | `#A7B0A1` | midtone, lumut, pakaian, batu |
| Orange | `#F26A3D` | **satu** sumber cahaya hangat per gambar + aksen garis teks |

Aturan: **maksimal satu area orange per gambar.** Orange adalah tanda tangan kanal;
kalau dipakai dua kali, mata tidak tahu harus melihat yang mana.

---

## 4. Grid yang dipakai semua episode

```
┌───────────────────────────────────────────────┐
│  EP 0X        ▁▁▁▁▁  (garis orange 8 px)      │
│                                               │
│  KATA         ┌───────────────┐               │
│  KATA         │   SILUET      │  ← 55–65%     │
│  KATA         │   (punggung)  │    tinggi frame│
│               └───────────────┘               │
│         (ruang negatif 38–42% kiri)           │
│                                               │
│  ── 15% bawah dikosongkan (durasi YouTube) ── │
└───────────────────────────────────────────────┘
```

· **Teks di kiri, subjek di kanan** — konsisten di 8 episode, supaya feed kanal
  terlihat rapi saat di-scroll.
· Headline: Anton, uppercase, **2–3 kata**, tinggi huruf 96 px (kanvas 1280),
  warna Ivory, stroke Ink 6 px, jarak baris 0,92.
· Label episode: Archivo Black 26 px, Sage, di kiri atas.
· Garis aksen: 8 × 220 px, Orange, di atas headline.
· Tidak ada panah, lingkaran, tanda seru, emoji, atau bayangan ganda.

---

## 5. Delapan konsep (satu konflik per gambar)

| ep | judul video | headline (2–3 kata) | pemicu | visual |
|---|---|---|---|---|
| 01 | Tiga penjaga dan satu set pakaian yang tertinggal | **PAKAIAN TERTINGGAL** | pattern violation | siluet pria di kaki menara, punggung menghadap; pakaian tahan air tergantung di tiang; lampu menara orange |
| 02 | Mereka memotong tenda itu dari dalam | **DIPOTONG DARI DALAM** | threat | kain tenda menganga, dilihat dari dalam; siluet berjalan menjauh ke salju |
| 03 | Kapal yang masih bisa berlayar, awak yang meninggalkannya | **KAPAL KOSONG** | curiosity gap | dek kosong, kemudi tanpa tangan; siluet berdiri di pagar, punggung menghadap |
| 04 | Mereka berjalan menjauhi pertolongan | **JALAN KE ATAS** | unresolved | mobil tertutup salju ditinggal; jejak kaki menanjak; siluet kecil di punggung bukit |
| 05 | Mereka menulis satu kata, bukan peringatan | **TANPA MAYAT** | pattern violation | tiang pagar kayu terpahat, rumah dibongkar, siluet berdiri di tanah kosong |
| 06 | Api di bawah kota yang tidak pernah dipadamkan | **API TAK PADAM** | hidden danger | jalan retak mengeluarkan uap; celah tanah berpendar orange; siluet di tepi jurang aspal |
| 07 | Jejak kaki itu hanya satu arah | **JEJAK SATU ARAH** | threat | rumah pertanian gelap; satu baris jejak menuju pintu, tanpa jejak kembali |
| 08 | Semua label di pakaiannya dipotong | **TANPA NAMA** | mystery | lereng berbatu; siluet perempuan menjauh; sisa api orange di tanah |

Judul dan headline **tidak mengulang**: headline menunjukkan apa yang salah,
judul menjawab kenapa itu penting.

---

## 6. Checklist sebelum unggah

1. Subjek dikenali dalam 1 detik? (squint test 120 px)
2. Teks terbaca di ponsel, 2–3 kata, tidak menabrak UI?
3. Ada satu kejanggalan spesifik, bukan sekadar suasana gelap?
4. Palet tetap empat warna? Hanya satu area orange?
5. Subjek tidak membocorkan jawaban video?
6. Janji headline benar-benar ada di dalam video?
7. Terlihat satu keluarga dengan tujuh thumbnail lain?

---

## 7. Cara menguji nanti

Unggah dua versi hanya kalau ada data: pakai fitur **Test & Compare** YouTube
pada video yang sama, ukur CTR **per sumber traffic** (browse vs suggested),
lalu bandingkan juga retensi 30 detik pertama. CTR naik tapi retensi turun =
thumbnail menjanjikan hal yang tidak diberikan video.

---

## Status produksi (final)

Sistem di atas sudah dieksekusi: **16 berkas** (8 episode × 16:9 + 9:16) ada di
`final/16x9/EPxx_16x9_1280x720.jpg` dan `final/9x16/EPxx_9x16_1080x1920.jpg`,
sudah diunggah ke Drive `ODDCHAPTER / thumbnail / 16x9 LONG (1280x720)` dan
`9x16 SHORT (1080x1920)`. Rincian berkas, headline, dan cara pasang di Studio:
`README_ASET.md`.

Yang perlu diketahui saat audit ulang:
- Headline final dipendekkan menjadi **dua baris** agar aman di kartu kecil; isi pesannya sama.
- `EP06` memakai `API TAK PADAM` (bukan `MASIH MENYALA`) karena lebih memicu ancaman laten.
- `EP08` memakai `TANPA NAMA` (judul aslinya menyebut sembilan nama) — sengaja menyembunyikan
  angka supaya penonton harus membuka video.
- 16:9 `EP07` & `EP08` masih hasil potong dari plate 9:16; ganti dengan plate 16:9 asli
  begitu generator gambar tersedia lagi.
