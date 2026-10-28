# Chromium, Remotion, dan koreksi saya

Dokumen ini mencatat satu kesalahan teknis yang saya buat, penyebabnya, dan cara memperbaikinya. Ditulis karena kesimpulan "tidak bisa" yang salah lebih berbahaya daripada kegagalan yang jujur.

---

## Ringkas

| | |
|---|---|
| **Klaim awal saya** | "Chromium tidak bisa dijalankan di sandbox ini, jadi video-shotcraft (Remotion) tidak bisa dipakai." |
| **Kenyataan** | **Salah.** Chromium bisa jalan. Remotion bisa render. |
| **Penyebab** | `@sparticuz/chromium` **membawa** `libnspr4.so` + `libnss3.so`, tapi hanya mengekstraknya kalau mendeteksi Amazon Linux. Di Debian, ekstraksi tidak pernah terjadi — jadi Chromium gagal dengan `error while loading shared libraries`. |
| **Perbaikan** | Ekstrak `al2023.tar.br` manual ke `/tmp/al2023/lib`, lalu jalankan dengan `LD_LIBRARY_PATH=/tmp/al2023/lib`. |

---

## 1. Kenapa `npm pack` / paket Sparticuz sebenarnya sudah benar

`@sparticuz/chromium` (v153) bekerja dengan cara:

1. `chromium.br` → binary Chromium (di-inflate ke `/tmp/chromium`)
2. `al2023.tar.br` → **11 pustaka sistem**, termasuk `libnspr4.so` dan `libnss3.so`
3. `swiftshader.tar.br` → `libEGL.so`, `libGLESv2.so`, `libvulkan.so.1` (GPU software)
4. `fonts.tar.br` → font

Pustaka sistem yang selama ini saya cari di apt **ternyata ada di dalam paket npm**:

```
lib/libnspr4.so      lib/libnss3.so      lib/libnssutil3.so
lib/libplc4.so       lib/libplds4.so     lib/libsoftokn3.so
lib/libfreebl3.so    lib/libfreeblpriv3.so   lib/libexpat.so.1
```

Masalahnya ada di `index.js`:

```js
if (isRunningInAmazonLinux2023(nodeMajorVersion)) {
    setupLambdaEnvironment(join(tmpdir(), "al2023", "lib"));
}
```

Fungsi yang menyetel `LD_LIBRARY_PATH` **hanya dipanggil di Amazon Linux 2023**. Di Debian, `.so`-nya diekstrak (atau tidak, tergantung kapan `executablePath()` dipanggil), tapi path-nya tidak pernah didaftarkan.

---

## 2. Perbaikan (5 langkah, terbukti)

```bash
mkdir -p /home/user/render-lab && cd /home/user/render-lab
npm init -y
npm i @sparticuz/chromium puppeteer-core

# ekstrak pustaka sistem yang dibawa paket
python3 - <<'EOF'
import brotli, tarfile, io, os
raw = brotli.decompress(open('node_modules/@sparticuz/chromium/bin/al2023.tar.br','rb').read())
os.makedirs('/tmp/al2023', exist_ok=True)
tarfile.open(fileobj=io.BytesIO(raw)).extractall('/tmp/al2023')
EOF

# verifikasi tidak ada pustaka yang hilang
LD_LIBRARY_PATH=/tmp/al2023/lib ldd /tmp/chromium | grep "not found"   # → kosong
```

Lalu jalankan **selalu** dengan `LD_LIBRARY_PATH`:

```bash
LD_LIBRARY_PATH=/tmp/al2023/lib node script.mjs
LD_LIBRARY_PATH=/tmp/al2023/lib npx remotion render ...
```

**Hasil uji:** `HeadlessChrome/153.0.8010.0` — screenshot 1080×1920 berhasil.

---

## 3. Remotion: jalan, dengan dua jebakan

Setelah Chromium hidup, `npx remotion still` masih gagal dua kali. Keduanya bukan soal Chromium:

| Error | Penyebab | Solusi |
|---|---|---|
| `Maximum for --concurrency is 2` | Remotion membatasi sesuai jumlah *core* (sandbox 2 vCPU) | **wajib** `--concurrency=2` |
| `esbuild: Unexpected ">"` | `registerRoot` tidak boleh menerima Fragment `<>...</>` | daftarkan beberapa `<Composition>` di dalam **satu** komponen Root |

Perintah yang akhirnya bekerja:

```bash
LD_LIBRARY_PATH=/tmp/al2023/lib npx remotion render src/index.ts TropicalBumper \
  out/bumper.mp4 \
  --browser-executable=/tmp/chromium \
  --concurrency=2 \
  --crf=18
```

**Hasil:** 150 frame, 5,06 detik, 1080×1920, 344 KB, selesai dalam **12,6 detik** (≈12 fps render).

---

## 4. Bumper yang dipakai

Saya tidak menulis ulang komponen: bumper memakai **`PaperTitleCard` asli** dari repo video-shotcraft (`src/aifl/PaperTitleCard.tsx`), di-*reskin* ke palet film:

```tsx
<PaperTitleCard
  duration={150}
  words={[{ text: 'KULIT' }, { text: 'TROPIS.', accent: true }]}
  sub="formula subtropis"
  fontSize={132}
  ink="#EDE4D3" accent="#C0603A" muted="#8B8577" paper="#0B0C0A"
/>
```

Efek yang diwarisi dari komponen itu: *letterpress word-by-word*, aksen amber italik, garis bawah yang tumbuh dengan easing bezier `(0.3, 0, 0.2, 1)`, dan *hold* penuh 1 detik sebelum fade — persis aturan **R1** di `aesthetics-rules.md`.

---

## 5. Yang masih belum ideal

| Batasan | Dampak | Jalan keluar |
|---|---|---|
| Chromium **shell** (tanpa GPU) | render lambat, 12 fps | pakai `--concurrency` lebih tinggi di mesin >2 core |
| 2 vCPU / 4 GB RAM | ~10 menit untuk 3 menit video | naikkan core |
| `/tmp` tidak persis | lib harus diekstrak ulang tiap sesi | taruh ekstraksi di skrip build |
| ~~Renderer dua lapis~~ | **sudah beres** — 10 adegan kini Remotion | — |
| `delayRender` font menggantung di tab kedua | render mati di frame ~400 (pesan menyesatkan: "loadFont requires url") | jangan pakai `@remotion/fonts`; tanam woff2 sebagai data URI + gate yang selalu `continueRender` |
| Satu tab merender 6.000 frame | tab makin berat, render panjang rawan mati | pecah jadi chunk 800 frame (`remotion/render-chunks.sh`), gabung `-c copy` |
| Frame JPEG keluar `yuvj420p` | player bisa salah baca range → warna pudar/pekat | re-encode final `-pix_fmt yuv420p -colorspace bt709 -color_range tv` |

## 5b. Dua jebakan yang baru ketemu saat migrasi penuh

**1. `@remotion/fonts` + `--concurrency=2` = render mati di tengah.**
Gejalanya: `A delayRender() "Loading font …" was called but not cleared after 28000ms`,
selalu sekitar frame 395–405 (tab kedua mulai dari frame itu). Pesan errornya
menyesatkan — seolah `url` kosong, padahal masalahnya `font.load()` tidak pernah
resolve. Gantinya: woff2 ditanam sebagai data URI (`scripts/embed-fonts.mjs` →
`src/film/fontData.ts`) dan sebuah `FontGate` yang melepas handle di `finally`
plus timeout pengaman 8 detik. Setelah itu 800 frame selesai tanpa gagal.

**2. `remotion render` penuh (5.909 frame) tidak stabil di 2 vCPU/4 GB.**
Solusi: render per 800 frame lewat `render-chunks.sh` (tiap potongan mulai dari
browser baru), lalu `ffmpeg -f concat -c copy`. Waktu total ~10 menit.

---

## 6. Pelajaran

Saya menyimpulkan "tidak bisa" dari **satu** percobaan yang gagal, tanpa membaca kode paketnya. Padahal jawabannya ada di 12 baris pertama `index.js`.

Aturan yang saya ambil dari sini: sebelum menyatakan sebuah tool tidak mungkin dipakai, baca dulu kode yang menentukan kondisinya — terutama pengecekan lingkungan yang khas satu platform.
