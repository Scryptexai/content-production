# 06_UPLOAD — dari master jadi YouTube, otomatis lewat antrean

Folder ini bukan video. Ini **instruksi unggah**: judul, hook, deskripsi, tag,
komentar pertama, dan id file Drive untuk tiap episode. Yang mengeksekusi adalah
GitHub Actions (`.github/workflows/youtube-upload.yml`) lewat API Zernio.

```
11_CONTENT/06_UPLOAD/
├── EP01.json            metadata unggah (judul, hook, deskripsi, tags, first_comment,
│   EP02.json             categoryId, drive_file_id, size_bytes, sha256, video, thumbnail)
├── EP03.json
├── thumbs/EP0n_thumbnail.jpg    yang benar-benar dikirim ke YouTube (±0,3 MB, ikut repo)
├── queue/EP0n.json      antrean: push berkas berstatus "requested" = unggah episode itu
├── published.json       buku besar: episode yang sudah tayang, ditulis balik oleh job
└── README.md
```

Master MP4 **tidak** ada di Git (17–22 MB per episode). Master tinggal di Drive
folder `video ready`; workflow mengunduhnya sendiri dari `drive_file_id`
(dicoba lewat `gdown`, lalu unduhan langsung `drive.usercontent.google.com` —
karena itu file master harus tetap **anyone with the link → Viewer**).

---

## Status: sudah tayang

| EP | Judul | YouTube |
|---|---|---|
| 01 | 3 Penjaga Masuk Menara di Pulau Flannan. Lampunya Mati, Tak Seorang Pun Keluar. | https://www.youtube.com/watch?v=l-_uCXDQo0g |
| 02 | 9 Pendaki Merobek Tenda dari Dalam, Lalu Lari ke Salju Tanpa Sepatu. | https://www.youtube.com/watch?v=X-OyOWaac_M |
| 03 | 10 Awak Naik Sekoci dari Kapal yang Masih Utuh. Tak Satu Pun Kembali. | https://www.youtube.com/watch?v=C3Bc7HSwyXY |

Diunggah 2026-11-08 oleh workflow, publik, kanal ODDCHAPTER (@oddchapter7).
Ketiganya tercatat di `published.json`. Berkas di `queue/` sekarang berstatus
`published`; kalau ditambah episode baru, buat berkas baru berstatus `requested`.

---

## Kenapa unggahan ini aman walau otomatis

Unggahan ke kanal orang lain tidak bisa dibatalkan dengan `Ctrl+Z`. Karena itu tiga
lapis:

1. **Antrean berkas.** Tidak ada yang diunggah sampai ada berkas di
   `06_UPLOAD/queue/` berstatus `requested`. Berkas itu yang menjadi izin.
2. **Buku besar.** Episode yang sudah tayang tercatat di `published.json`;
   push berikutnya melewatinya. Satu episode, satu unggahan.
3. **Hash master.** sha256 dan ukuran file dicocokkan dengan metadata sebelum
   satu byte pun dikirim. File yang bukan yang disetujui tidak akan diunggah.

Dan sebelum `--send` menyentuh jaringan, `upload_zernio.py` memeriksa: ukuran file
sama dengan `size_bytes`, sha256 sama dengan `sha256`, judul ≤ 100 karakter, hook
ada di baris pertama deskripsi, deskripsi ≤ 5.000 karakter, tag ≤ 500 karakter
gabungan, thumbnail JPEG ≤ 2 MB. Satu saja gagal, unggahan dibatalkan.

---

## Pemasangan sekali jalan

### 1. Pasang tiga secret

Settings → Secrets and variables → Actions → **New repository secret**:

| Nama | Isi | Wajib |
|---|---|---|
| `ZERNIO_API_KEY` | API key dari dashboard Zernio (Settings → API keys) | ya |
| `ZERNIO_YOUTUBE_ACCOUNT_ID` | `accountId` kanal YouTube di Zernio | ya |
| `ZERNIO_PLAYLIST_ID` | id playlist tujuan, kalau mau semua episode masuk satu playlist | tidak |

Cara mengambil `accountId`: di Zernio, hubungkan kanal YouTube dulu
(Accounts → Connect → YouTube), lalu buka `GET /v1/profiles` dengan API key yang
sama:

```bash
curl -s -H "Authorization: Bearer $ZERNIO_API_KEY" \
  https://zernio.com/api/v1/profiles | python3 -m json.tool | grep -i -A3 youtube
```

Yang dicari: `platforms[].platform == "youtube"` → `accountId`. Salin ke secret.
Kalau kanal pernah dilepas dan disambung ulang, `accountId` bisa berubah — perbarui
secret-nya, kalau tidak unggahan akan ditolak Zernio.

### 2. Pasang gerbang persetujuan

Settings → Environments → **New environment** → nama `production` →
centang **Required reviewers** → pilih akun sendiri. Tanpa langkah ini workflow
tetap jalan, tapi tidak ada yang menghentikannya di tengah.

### 3. Unggah otomatis lewat antrean

Tidak ada tombol yang perlu ditekan. Antreannya adalah berkas JSON di
`queue/`; menambah satu berkas berstatus `requested` lalu push = episode itu
diunggah.

```json
{ "episode": "EP01", "status": "requested", "visibility": "public" }
```

Push berkas itu memicu `.github/workflows/youtube-upload.yml` (jalur
`06_UPLOAD/queue/*.json`). Urutan job:

1. **Cek kredensial** — `GET /v1/accounts` + `/v1/profiles`; akun YouTube dicari
   otomatis. Kalau secret `ZERNIO_YOUTUBE_ACCOUNT_ID` kosong atau tidak cocok,
   akun pertama yang ditemukan dipakai, jadi unggahan tetap jalan.
2. **Unduh master dari Drive** memakai `drive_file_id`, lalu **sha256 + ukuran
   dicocokkan** dengan metadata. Bedanya satu byte → berhenti.
3. **Presign + PUT + `POST /v1/posts`** dengan `Idempotency-Key` dari sha256 +
   judul (berlaku 24 jam, jadi timeout yang diulang tidak membuat video kedua;
   409/429/5xx diulang otomatis).
4. **`published.json`** dicatat dan di-commit balik oleh job. Push berikutnya
   melewati episode yang sudah ada di situ — satu episode tidak mungkin tayang
   dua kali. Push oleh `GITHUB_TOKEN` tidak memicu workflow lain, jadi tidak ada
   lingkaran.

Satu berkas antrean per push. `visibility` boleh `public`, `unlisted`, atau
`private`.

### Idempotensi: mengapa mengulang tidak membuat video kedua

Uji 2026-11-09: EP01 diambil ulang dari Drive (`sha256` cocok), diunggah ke
storage Zernio, lalu `POST /v1/posts` dijalankan lagi dengan `"force": true`.
Hasilnya **post yang sama**, `post_id 6af0954333e414fd437af3ca`,
`https://www.youtube.com/watch?v=l-_uCXDQo0g` — bukan video baru.

Sebabnya `Idempotency-Key` yang diturunkan dari sha256 master + judul: selama
24 jam, request dengan kunci sama mengembalikan post yang sudah ada (HTTP 200).
Ini yang membuat "jalankan ulang karena timeout" aman. Kalau memang ingin video
persis sama terbit dua kali, tunggu lebih dari 24 jam — dan itu hampir selalu
bukan yang diinginkan.

### 4. Menjalankan manual (opsional)

Actions → **Upload episode to YouTube (Zernio)** → **Run workflow** →
**Use workflow from**: `arena/66ec29bf-content-production`. Isi `dry_run: true`
untuk melihat payload lengkap tanpa mengunggah, lalu `false` untuk mengunggah.

Setiap `POST /v1/posts` tetap membawa `Idempotency-Key`, jadi menjalankan ulang
episode yang sama dalam 24 jam mengembalikan post yang sama, bukan video kedua.

Hasil unggahan:

- tabel episode/status/tautan di halaman run,
- log JSON di artifact `upload-log-*` (90 hari),
- `published.json` di repo: post id, status, tautan YouTube, judul.

## Unggah dari laptop (kalau tidak mau lewat Actions)

```bash
cd ODDCHAPTER_BRAND
export ZERNIO_API_KEY=...  ZERNIO_YOUTUBE_ACCOUNT_ID=...

python3 tools/upload_zernio.py EP01                         # dry-run, baca payload
python3 tools/upload_zernio.py --all --text-only            # cek judul/hook/tag saja,
                                                            # tanpa master di mesin ini
python3 tools/upload_zernio.py EP01 --send --visibility unlisted
python3 tools/upload_zernio.py --all --send                 # EP01–EP03 berurutan
```

`tools/upload_zernio.py` hanya memakai pustaka standar Python — tidak perlu
`pip install` apa pun. `--media-dir` menunjuk folder berisi
`EP0n_1080x1920_master.mp4` + `EP0n_thumbnail.jpg`; tanpa flag itu, ia mencari di
`10_FILM/remotion/output/episodes/` (butuh thumbnail di folder yang sama, lihat
`10_FILM/upload/`).

---

## Judul dan hook

| EP | Judul (≤100 kar.) | Kar. | Hook — baris pertama deskripsi |
|---|---|---|---|
| 01 | 3 Penjaga Masuk Menara di Pulau Flannan. Lampunya Mati, Tak Seorang Pun Keluar. | 79 | 15 Desember 1900. Lampu menara Flannan Isles tidak dinyalakan, dan 3 penjaganya tidak pernah keluar dari menara itu. |
| 02 | 9 Pendaki Merobek Tenda dari Dalam, Lalu Lari ke Salju Tanpa Sepatu. | 68 | 1 Februari 1959. 9 pendaki merobek tenda mereka dari dalam, lalu berlari ke salju tanpa sepatu. |
| 03 | 10 Awak Naik Sekoci dari Kapal yang Masih Utuh. Tak Satu Pun Kembali. | 69 | 5 Desember 1872. Kapal Mary Celeste ditemukan berlayar tanpa awak. Sekocinya hilang, muatannya masih di palka. |

### Rumusnya, bukan selera

1. **Angka di lima kata pertama.** "3", "9", "10" — bukan "tiga", "sembilan".
   Di feed Shorts judul terpotong sekitar 40 karakter, jadi angka yang harus
   bertahan harus berdiri di depan, bukan di tengah kalimat.
2. **Satu detail mustahil, bukan satu premis.** "Lampunya mati, tak seorang pun
   keluar" lebih kuat daripada "menara misterius". Yang menjual adalah benda
   konkret yang tidak seharusnya begitu.
3. **Dua kalimat pendek, titik di tengah.** Kalimat pertama memasang perangkap,
   kalimat kedua menutupnya. Titik memaksa berhenti sejenak — koma membuat
   pembaca meluncur lewat.
4. **Tanpa "misteri", "ternyata", "fakta mengejutkan", emoji, atau kapital semua.**
   Kata-kata itu sudah dipakai semua kanal, jadi tidak lagi memilih siapa pun.
   `upload_zernio.py` sekarang menegur ketiganya (`::warning::`) saat dry-run.
5. **Hook = kalimat pertama deskripsi, dan harus memuat tanggal atau angka.**
   Yang dibaca orang di bawah judul bukan "Hai semuanya" — dia membaca satu
   kalimat yang membuatnya menekan *more*. Hook yang sama dibuka di detik 0,6
   video, jadi tiga tempat (judul, deskripsi, frame pertama) mengatakan hal yang
   sama dengan kata yang sama.
6. **Pertanyaan disimpan untuk komentar pertama.** Judul memancing dengan fakta,
   kolom komentar dibuka dengan pertanyaan yang benar-benar bisa dijawab orang
   biasa: "kamu akan naik ke menara atau menunggu kapal?" Yang dibeli balasan,
   bukan tayangan.

### Varian cadangan (A/B)

Tiap JSON menyimpan `title_alt` berisi tiga varian: satu bentuk pertanyaan
("Kenapa ...?"), satu bentuk kronologi bertanggal, satu bentuk detail fisik.
Aturan pemakaiannya:

- Video **baru** (< 7 hari): boleh ditukar. Beri satu judul minimal 48 jam agar
  datanya cukup untuk dibandingkan — CTR 24 jam pertama masih terlalu berisik.
- Video **lama**: jangan disentuh. Mengganti judul memutus rekomendasi yang
  sedang berjalan; yang lebih baik adalah memakai varian itu untuk episode baru.
- Yang dibandingkan **CTR impresi**, bukan jumlah tayangan. Tayangan bisa naik
  karena satu komentar viral, bukan karena judulnya.

## Kalau unggahan gagal

| Gejala | Penyebab yang paling sering | Tindakan |
|---|---|---|
| `HTTP 401` di `/media/presign` | `ZERNIO_API_KEY` salah atau sudah dicabut | buat key baru, perbarui secret |
| `HTTP 400 ... accountId` | kanal YouTube belum tersambung / id berubah | cek `GET /v1/profiles`, perbarui secret |
| `ukuran … byte, metadata bilang …` | master di Drive di-render ulang, metadata belum diperbarui | perbarui `size_bytes` + `sha256` di JSON |
| `sha256 … tidak cocok` | unduhan Drive terpotong / file lain | hapus `media/`, jalankan ulang |
| `Drive mengembalikan HTML` | master tidak lagi publik | Drive → klik kanan file → Share → *Anyone with the link* → Viewer |
| `file thumbnail tidak ada` | `thumbs/EP0n_thumbnail.jpg` hilang | salin dari `11_CONTENT/03_THUMBNAIL/EP0n.jpg` |
| `judul … karakter, batas YouTube 100` | judul diedit melewati batas | potong, uji ulang dry-run |
| Video jadi, thumbnail tidak | thumbnail > 2 MB | kompres JPEG; `thumbs/` saat ini ±0,1–0,3 MB |
