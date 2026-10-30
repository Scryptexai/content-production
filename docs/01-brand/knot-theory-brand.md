# Knot Theory — brand & aset

Nama kanal: **Knot Theory** · `@knottheory` di TikTok, Instagram, YouTube.
Tagline: **manusia dan ikatannya**.

Aset jadi ada di [`brand/knot-theory/assets/`](../../brand/knot-theory/assets/), semua
dibangkitkan ulang dengan satu perintah:

```bash
cd brand/knot-theory && python3 build_brand.py --sheet
```

---

## 1. Kenapa simpul, dan kenapa simpul ini

Simpul adalah bentuk paling jujur dari sebuah relasi: tidak ada yang diikat kalau tidak
ada dua ujung, dan setiap ikatan punya harga — tali yang menahan juga tali yang
membatasi. Nama "Knot Theory" juga harfiah: teori simpul adalah cabang matematika yang
mempelajari apakah dua simpul bisa dilepas menjadi satu garis lurus. Pertanyaan itu
persis pertanyaan kanal ini tentang hubungan.

Mark-nya adalah **trefoil (2,3)** — simpul paling sederhana yang benar-benar tersimpul,
tiga untaian bertemu di tiga titik. Yang penting: **setiap persilangan punya atas dan
bawah yang benar.** Itu bukan detail dekoratif. Simpul yang salah anyam secara matematis
bukan simpul. Mark ini dibuat dari kurva parametrik dan dihitung z-nya untuk menentukan
untaian mana yang lewat di atas, jadi tidak ada ilusi yang dipalsukan.

Satu hal yang tidak dilakukan: tidak ada satu untaian pun yang bisa dilepas tanpa
memutus yang lain. Itu definisi ketergantungan, dan itu sebabnya mark ini dipakai apa
adanya — bukan sebagai ornamen yang ditempel di teks.

---

## 2. Sistem logo

| Nama | Isi | Berkas |
|---|---|---|
| Logo utama | mark + KNOT THEORY + hairline rose + tagline, transparan | `logo-primary-transparent-2400.png` |
| Mark saja | trefoil, transparan | `logo-mark-transparent-1600.png` |
| Mark vektor | path SVG, stroke round-cap | `logo-mark.svg` |
| Avatar | mark di dalam lingkaran, latar ink | `avatar-1080.jpg` |
| Avatar aksen | satu untaian rose (varian untuk konten, bukan profil) | `avatar-rose-1080.png` |
| Watermark YT | mark putih, 150 px | `yt-watermark-150.png` |

**Aturan pakai**

- Ruang kosong minimum di sekeliling mark = **0,5 × tinggi mark** di semua sisi.
- Ukuran minimum mark: **24 px** (di bawah itu celah persilangan menutup; pakai versi
  yang lebih tebal, jangan diperkecil terus).
- Warna: krem `#EFE7DC` di atas ink. Mark **tidak** boleh diwarnai gradien, diberi
  bayangan, atau diberi outline.
- Varian rose hanya untuk motion/cover; profil resmi memakai versi mono.
- Jangan memutar, memiringkan, atau menambahkan efek 3D. Simpulnya sudah punya ilusi
  kedalaman dari anyaman; efek tambahan merusaknya.

---

## 3. Warna

| Peran | Nama | Hex | Pakai |
|---|---|---|---|
| Latar atas | ink | `#0C1018` | gradien latar |
| Latar bawah | ink-2 | `#151B28` | gradien latar |
| Teks utama | krem | `#EFE7DC` | judul, mark |
| Aksen | rose | `#D98E73` | hairline, label episode, satu untaian |
| Data positif | sage | `#8FA98B` | grafik yang bekerja |
| Batas/ketidakpastian | lilac | `#A79BC8` | label `TIDAK DIKETAHUI` |
| Teks sekunder | muted | `#8A93A3` | metadata, handle |

Rasio kontras krem di atas ink ≈ 13:1 (lolos AAA). Rose di atas ink ≈ 5,4:1 — cukup
untuk teks besar, jangan untuk paragraf.

---

## 4. Tipografi

| Peran | Font | Berkas | Alasan |
|---|---|---|---|
| Judul & wordmark | Instrument Serif | `fonts/InstrumentSerif-Regular.ttf` | serif tegas, murah di layar kecil |
| Tagline & kutipan | Instrument Serif Italic | `fonts/InstrumentSerif-Italic.ttf` | satu keluarga, dua nada |
| Label & data | IBM Plex Mono Medium | `fonts/IBMPlexMono-Medium.ttf` | angka rata, terasa arsip bukan iklan |

Semua SIL Open Font License. Wordmark memakai tracking +0,20 em; jangan dirapatkan.
Teks judul maksimum **2 baris** di cover; kalau lebih, judulnya kurang tajam.

---

## 5. Aset per platform (dan apa yang sebenarnya ada)

Ini bagian yang sering salah: **TikTok dan Instagram tidak punya banner.** Yang ada di
sana adalah avatar, cover video, dan (di IG) grid + sorotan. Jadi "banner" di dua
platform itu dikerjakan oleh tiga aset lain, bukan satu gambar lebar.

| Platform | Slot | Ukuran final | Berkas | Catatan |
|---|---|---|---|---|
| YouTube | Banner channel | **2560 × 1440** (maks 6 MB) | `yt-banner-2560x1440.jpg` | **satu file**; isi di dalam 1546 × 423 |
| YouTube | Banner (opsi TV) | 2560 × 1440 | `yt-banner-tv-2560x1440.jpg` | atmosfer tambahan di atas/bawah; aman untuk mobile juga |
| YouTube | Safe area | 1546 × 423 | `yt-banner-safe-1546x423.jpg` | yang terlihat di HP |
| YouTube | Pratinjau Desktop | 2560 × 423 | `yt-preview-desktop-2560x423.jpg` | cek sebelum upload |
| YouTube | Pratinjau Tablet | 1855 × 423 | `yt-preview-tablet-1855x423.jpg` | |
| YouTube | Pratinjau Mobile | 1546 × 423 | `yt-preview-mobile-1546x423.jpg` | |
| YouTube | Pratinjau TV | 2560 × 1440 | `yt-preview-tv-2560x1440.jpg` | |
| YouTube | Lembar spek | 1800 × 2578 | `yt-banner-spec-sheet.png` | banner + peta zona + 3 potongan |
| YouTube | Avatar | 800 × 800 (render 1080) | `avatar-1080.jpg` | dipotong bulat |
| YouTube | Watermark | 150 × 150 | `yt-watermark-150.png` | muncul di pojok player |
| YouTube | Thumbnail | 1280 × 720 | `yt-thumb-template-1280x720.jpg` | judul kiri, mark kanan |
| TikTok | Foto profil | 200 × 200 (render 1080) | `avatar-1080.jpg` | dipotong bulat |
| TikTok | Cover video | **1080 × 1920** | `tt-cover-1080x1920.jpg` | aman: 90 px kiri/kanan, 220 atas, 420 bawah |
| TikTok | Banner profil | — | — | tidak ada slot ini di TikTok |
| Instagram | Foto profil | 320 × 320 (render 1080) | `avatar-1080.jpg` | dipotong bulat |
| Instagram | Post pinned | **1080 × 1350** (4:5) | `ig-pinned-1080x1350.jpg` | tampil paling besar di grid |
| Instagram | Sorotan | **1080 × 1920** | `ig-highlight-*-1080x1920.jpg` | hanya lingkaran tengah terlihat |
| Instagram | Banner profil | — | — | tidak ada slot ini di IG |

### Banner YouTube: satu file, empat potongan

Yang penting dipahami: **YouTube hanya menyimpan satu file banner.** Tab Desktop,
Tablet, Mobile, dan TV di YouTube Studio bukan empat slot upload — itu pratinjau
potongan dari file yang sama. Jadi tidak ada "banner versi mobile" yang diunggah
terpisah; yang bisa dilakukan adalah menaruh isi di area yang **tidak terpotong di
potongan mana pun**.

| Pratinjau | Potongan (px) | Lolos kalau isi ada di |
|---|---|---|
| TV | 2560 × 1440 | seluruh kanvas |
| Desktop | 2560 × 423 | 1546 × 423 tengah |
| Tablet | 1855 × 423 | 1546 × 423 tengah |
| Mobile | **1546 × 423** | 1546 × 423 tengah |

Karena mobile adalah yang paling sempit, **1546 × 423 adalah patokan**:
semua teks, logo, dan tagline harus di dalamnya. Di luar kotak itu hanya boleh
tekstur — ornamen sayap kiri/kanan, gradien, grain.

Banner saat ini punya margin terukur di potongan tersempit:

```
isi terang bounding box pada 1546 × 423:
  kiri 494 px · kanan 493 px · atas 36 px · bawah 37 px
```

Artinya walaupun YouTube memotong ke tablet (1855) atau desktop (2560), tidak ada
satu huruf pun yang hilang; yang bertambah hanya latar di kiri-kanan.

**Opsi TV.** `yt-banner-tv-2560x1440.jpg` menambahkan gradien gelap halus di 26% atas
dan bawah kanvas — hanya terlihat di TV, dan tetap tidak menyentuh area aman. Ini
opsional: kalau ragu, pakai `yt-banner-2560x1440.jpg`.

### Kenapa ukuran lain begitu

- **TikTok cover 1080×1920** karena UI TikTok menutup 220 px atas (tombol) dan
  ~420 px bawah (username, caption, musik). Judul ditempatkan di 33–52% tinggi layar.
- **IG pinned 1080×1350** karena 4:5 memakan area grid terbesar; 1:1 menyisakan ruang
  kosong, 9:16 terpotong.
- **IG sorotan 1080×1920** karena yang tampil hanya lingkaran tengah — isi diletakkan
  di kotak tengah 1080×1080.
- **Avatar 1080** lalu dipotong bulat; mark dijaga di dalam 58% kanvas karena
  circumradius trefoil 3,727 dari bbox 5,472.

## 6. Proporsi (angka yang dipakai di semua aset)

Supaya tujuh aset terlihat satu keluarga, bukan tujuh desain:

| Hubungan | Nilai |
|---|---|
| Mark : lebar blok | 0,13–0,16 |
| Wordmark : lebar blok | 0,062 |
| Tagline : wordmark | 0,39 |
| Hairline : lebar blok | 0,16 (banner) · 0,17 (pinned) · 0,20 (cover) |
| Mark : judul cover | 1 : 2,1 |
| Margin luar | 8,5% lebar kanvas |
| Tebal stroke mark : ukuran mark | 0,085 (logo) · 0,098 (avatar) · 0,10 (cover) |

Kalau salah satu aset diubah, ubah angkanya di `build_brand.py` — jangan menggeser
manual di editor gambar, karena rasio antar-aset akan pecah.

---

## 7. Yang tidak boleh

- Menaruh teks di luar safe area (YouTube 1546×423, TikTok 220/420, IG lingkaran).
- Mengunggah cover TikTok (1080×1920) ke slot banner YouTube. Itu rasio 9:16;
  YouTube akan memotongnya jadi 16:9 dan judul akan terbelah. Banner punya file sendiri.
- Memakai trefoil sebagai pola berulang di latar video (jadi motif batik, bukan logo).
- Menambahkan tagline lain di aset yang sudah ada tagline.
- Menjual tampilan "AI" sebagai bagian dari identitas — label AI ada di caption, bukan
  di logo.
- Mengganti font ke font sistem "karena lebih cepat". Wordmark yang berubah font bukan
  wordmark.

---

## 8. Berkas kerja

```
brand/knot-theory/
  build_brand.py       renderer semua aset (Pillow)
  knot_geometry.py     kurva trefoil + pemotongan persilangan + simplify SVG
  fonts/               Instrument Serif, IBM Plex Mono (OFL)
  assets/              hasil render siap upload
```

Regenerasi semuanya:

```bash
pip install --break-system-packages pillow
cd brand/knot-theory && python3 build_brand.py --sheet
```

Cek cepat setelah render — margin isi di potongan tersempit:

```bash
cd brand/knot-theory/assets
python3 - <<'EOF'
from PIL import Image
import numpy as np
for f in ["yt-preview-mobile-1546x423.jpg", "yt-preview-tablet-1855x423.jpg"]:
    a = np.asarray(Image.open(f).convert("RGB")).astype(int)
    ys, xs = np.where((a[:,:,0] > 200) & (a[:,:,1] > 190) & (a[:,:,2] > 155))
    H, W = a.shape[:2]
    print(f, "kiri", xs.min(), "kanan", W-1-xs.max(), "atas", ys.min(), "bawah", H-1-ys.max())
EOF
```

Kalau salah satu margin < 24 px, isi terlalu mepet — kurangi skala lockup,
jangan menggeser posisi.
