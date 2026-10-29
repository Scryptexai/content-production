# Kajian: dua tool yang Anda tunjuk

Dipelajari 30 Okt 2026. Keduanya sangat berbeda — satu tentang **cara render**,
satu tentang **sumber gerak**. Hanya yang pertama yang menjawab masalah kita.

---

## 1. `mg-styles-15` — INI jawabannya

Vincentwei1021, MIT. Lima belas film motion-design 10 detik, semuanya **ditulis
sebagai kode**, tanpa image/video generation.

### Cara kerjanya

```
index.html  →  window.renderAt(t)  →  headless Chrome ambil frame  →  ffmpeg
```

Satu halaman HTML yang bisa menggambar **frame untuk waktu berapa pun**.
`harness/render.mjs` membuka halaman itu di Chrome headless (via
`puppeteer-core`), memanggil `renderAt(t)` untuk tiap frame, menangkap
screenshot, lalu menyambungnya dengan ffmpeg.

Tidak ada React, tidak ada webpack, tidak ada hidrasi. Hanya DOM + SVG +
Canvas yang dipanggil per frame.

### Kenapa ini menyelesaikan masalah kita

Masalah yang Anda sebut: "prosesnya selama itu". Saya ukur di mesin yang sama
(2 core), 300 frame, 1920×1080, scene yang sama:

| Jalur | Waktu | Per frame |
|---|---|---|
| Remotion (React + webpack + bundle) | 23 mnt 31 dtk | 4,70 dtk |
| Halaman + `render.mjs` | **27,3 dtk** | **0,09 dtk** |

**Selisih 51×.** Untuk video 3 menit: 7 jam → 8 menit.

Penyebabnya bukan Chrome-nya (sama-sama Chromium), tapi lapisan di atasnya:
webpack harus membundel ulang tiap render, React harus me-render ulang pohon
komponen, dan `OffthreadVideo` menambah dekode. Halaman biasa melewati semua itu.

### Yang diambil

| Berkas | Isi |
|---|---|
| `film/harness/render.mjs` | renderer dari repo itu, **tidak diubah** selain path Chrome |
| `film/harness/LICENSE-mg-styles-15.txt` | lisensi MIT asli, dibawa apa adanya |
| `film/lib.js` | easing/spring/bezier/parallax yang saya tulis sendiri, gaya sama |
| `film/scenes/climb/index.html` | scene kita, ditulis ulang dalam bentuk `renderAt(t)` |

Kontrak `renderAt` juga berarti render bisa diulang persis dan diparalelkan —
tidak ada state yang bocor antar frame.

---

## 2. `Motion2MixamoRig` — belum bisa dipakai

MaxLiu22, eksperimental. Memetakan gerak orang di video ke karakter 3D
ber-rig Mixamo.

### Yang dibutuhkan sebelum satu frame pun keluar

| Kebutuhan | Ukuran / syarat |
|---|---|
| Bobot GVHMR | **~5 GB**, diunduh saat run pertama |
| Bobot HaMeR (tangan) | **~2,7 GB** (opsional) |
| Model SMPL-X | wajib **registrasi** di smpl-x.is.tue.mpg.de |
| Karakter Mixamo | akun Adobe, unduh FBX |
| Video sumber | **tepat satu orang**, kepala sampai kaki utuh di frame |
| Waktu ekstraksi | 8–15 menit per klip 30 dtk (CPU) |

### Kenapa belum cocok sekarang

1. **Butuh video orang sungguhan.** Kita tidak punya footage, dan aturan kita
   melarang mengambil klip YouTube. Ini tool yang *membutuhkan* input yang
   justru tidak kita punya.
2. **Ujungnya render 3D.** Gerak hasil retarget harus dirender — kembali ke
   Blender, dan Blender di mesin ini 8,4 dtk/frame untuk Cycles CPU. Itu
   masalah yang baru saja kita tinggalkan.
3. **Domainnya berbeda.** Tool ini untuk pengembang game yang butuh `.glb`
   beranimasi, bukan untuk film motion-design 2D.

### Kapan ia berguna

Kalau nanti kita mau bikin karakter 3D realistis yang bergerak seperti manusia
sungguhan — misalnya untuk format "tokoh nyata jadi animasi" — ini jalan yang
benar. Tetapi itu proyek terpisah dengan anggaran unduhan ~8 GB dan pipeline
render Blender/EEVEE yang harus dibereskan lebih dulu.

---

## Putusan

**Pakai `mg-styles-15` sekarang.** Bukan karena gayanya, tapi karena
arsitekturnya: satu halaman, satu fungsi, satu renderer tanpa lapisan.

**Tunda `Motion2MixamoRig`.** Simpan catatannya; ia baru masuk akal ketika
kita punya footage orang dan sudah siap merender 3D.

## Konsekuensi untuk repo

- `remotion/` tetap ada untuk short-form lama, tapi **long-form pindah ke
  `film/`**.
- Figur tetap dari rig Python (`export_figure.py`), jadi validasi pijakan
  0,00 px tidak hilang.
- Perintah render sekarang:

```bash
cd projects/knot-theory/film
export LD_LIBRARY_PATH=/tmp/al2023/lib:$LD_LIBRARY_PATH PATH=/tmp/bin:$PATH
node harness/render.mjs scenes/climb --out scenes/climb/out/v.mp4 --duration 12
```
