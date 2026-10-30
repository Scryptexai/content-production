# Knot Theory — produksi video (video-shotcraft)

Semua produksi video di `projects/knot-theory/` sekarang dijalankan **hanya** dengan
[`video-shotcraft`](https://github.com/Vincentwei1021/video-shotcraft) (Remotion + kartu shot).
Setup lama sudah dihapus seluruhnya: harness `film/`, rig karakter PNG, plate Blender,
`cine.py`, `motion.py`, dan SFX prosedural sudah tidak ada di repo.

## Isi folder

```
video/
├── src/
│   ├── index.ts · Root.tsx · Main.tsx   rangkaian film + peta bunyi
│   ├── lib/
│   │   ├── theme.ts     satu sumber warna/huruf/ukuran (font dibundel lokal)
│   │   ├── motion.ts    bezier, ramp, kamera multiplane (camAt/project), seeded
│   │   ├── Stage.tsx    ruangan: lampu, berkas cahaya, debu, vignette, grain
│   │   ├── Table.tsx    meja berperspektif, penerima bayangan kontak
│   │   ├── Photo.tsx    objek foto sebagai elemen 3D (parallax, rim, bayangan)
│   │   ├── Type.tsx     tipografi (reveal per kata, roll angka, kicker, sumber)
│   │   ├── Layout.tsx   pita teks tetap + zona benda
│   │   └── objects.ts   ukuran benda dihitung dari tinggi zona (bukan dikira)
│   └── shots/index.tsx  enam shot 60 detik
├── tools/key_objects.py  chroma key foto → PNG transparan + potong rapat
└── public/
    ├── objects/          PNG objek (hasil key) + raw/ (foto hijau asli)
    └── audio/{sfx,bgm}
```

## Aset objek (yang diminta: foto jadi elemen, bukan latar)

Foto dibuat dengan latar hijau murni, lalu di-chroma-key menjadi PNG transparan
dan dipotong rapat ke batas objek. Hasilnya dipakai sebagai **benda di dalam
ruang** yang punya parallax, bayangan kontak, rim light, dan defokus sendiri.

| Objek | Dipakai di | Peran naratif |
|---|---|---|
| `newspaper` | 01, 02, 05 | kliping peristiwa 1916 |
| `fin` | 01, 05 | ancaman yang datang dari luar kendali |
| `ballot-box` | 02, 05 | kotak suara, tempat akibat diukur |
| `ballot-sheet` | 02, 05 | satu surat suara bertanda X — jatuh satu per satu ke celah kotak |
| `magnifier` | 03, 05 | memeriksa ulang angka |
| `thread-knot` | 04, 05, 06 | simpul: sesuatu yang diikat dan dikendorkan |

Buat ulang PNG dari foto mentah:

```bash
python3 tools/key_objects.py     # butuh pillow + numpy
```

Algoritma key ada di docstring `tools/key_objects.py`; intinya alfa diturunkan dari
selisih hijau, ambang 44/92, lalu despill membatasi kanal hijau ke `max(r,b)×1,06`.

## Render

Mesin di sandbox ini 2 core tanpa GPU. Konfigurasi yang terbukti jalan:

```bash
# 1. unduh ffmpeg + chromium headless (sekali saja, di luar repo)
cd /tmp/tools && npm i @ffmpeg-installer/linux-x64 @ffprobe-installer/linux-x64 @sparticuz/chromium
cp node_modules/@ffmpeg-installer/linux-x64/ffmpeg /tmp/bin/
cp node_modules/@ffprobe-installer/linux-x64/ffprobe /tmp/bin/
# lib Chromium (AL2023) dibongkar ke /tmp/al2023, lalu:
export LD_LIBRARY_PATH=/tmp/al2023/lib
export PATH=/tmp/bin:$PATH

# 2. render
npm install
npx tsc --noEmit -p tsconfig.json          # cek tipe dulu, selalu
npx remotion still src/index.ts KnotTheory out/qa/f150.png --frame=150 \
  --concurrency=1 --browser-executable=/tmp/chromium --chrome-mode=chrome-for-testing
npx remotion render src/index.ts KnotTheory out/film-raw.mp4 \
  --concurrency=1 --browser-executable=/tmp/chromium --chrome-mode=chrome-for-testing --crf=18
```

Waktu terukur: **26 menit 30 detik** untuk 1800 frame (0,88 dtk/frame) termasuk
bundling. Still satu frame ≈ 7 detik.

## Normalisasi audio

Render Remotion menghasilkan campuran yang masih pelan (terukur −28,9 LUFS,
puncak −7,4 dB). Selalu loloskan hasilnya ke ffmpeg sebelum dipublikasikan:

```bash
/tmp/bin/ffmpeg -i out/film-raw.mp4 -c:v copy \
  -af "loudnorm=I=-14:TP=-1.5:LRA=9,alimiter=limit=0.94" \
  -c:a aac -b:a 320k -ar 48000 -movflags +faststart out/knot-theory-ep01.mp4
```

## Aturan yang tidak boleh dilanggar lagi

Empat kesalahan nyata di percobaan pertama, semuanya sudah ditutup di kode:

1. **Ukuran benda tidak boleh ditulis manual.** Tinggi benda dipilih, lebar
   dihitung lewat `lib/objects.ts`; kalau tidak, kliping 880 px menabrak pita teks.
2. **Tidak ada frame kosong di awal shot.** Shot 2–6 sudah terisi benda dan teks
   di frame pertama; hanya shot 1 yang boleh fade-in (fade film).
3. **Tidak ada dua elemen teks di pita yang sama** dan **benda tidak boleh masuk
   pita teks** (batas: layar y 1452 untuk pita isi).
4. **Grade warna disamakan.** Semua objek lewat `saturate(0,74) sepia(0,34)
   hue-rotate(-9°)` supaya enam foto berbeda terbaca satu keluarga.
5. **Kertas kecil tidak boleh diputar 3D.** `ballots.png` (kipas kertas) menjadi
   gumpalan tanpa bentuk saat diberi `rx` 40° dan `blur`. Diganti `ballot-sheet`
   (satu lembar, tepi sobek, tanda X) — benda kecil butuh siluet yang jelas.
6. **Benda yang harus "masuk" digambar `behind`.** Dengan zIndex di bawah kotak,
   bagian yang melewati siluet tertutup sendiri; jangan mengandalkan fade.

## Yang belum ada

- **VO belum direkam.** Naskah ada; suara belum.
- Sumber yang dipakai dua episode ini adalah data Amerika (pemilu kota 1916,
  penjualan perusahaan) dan disebut di layar — belum ada data instansi Indonesia.
