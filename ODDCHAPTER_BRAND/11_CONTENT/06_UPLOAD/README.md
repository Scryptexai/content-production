# 06_UPLOAD — dari master jadi YouTube, tanpa upload otomatis

Folder ini bukan video. Ini **instruksi unggah**: judul, hook, deskripsi, tag,
komentar pertama, dan id file Drive untuk tiap episode. Yang mengeksekusi adalah
GitHub Actions (`.github/workflows/youtube-upload.yml`) lewat API Zernio.

```
11_CONTENT/06_UPLOAD/
├── EP01.json            metadata unggah (judul, hook, deskripsi, tags, first_comment,
│   EP02.json             categoryId, drive_file_id, size_bytes, sha256, video, thumbnail)
├── EP03.json
├── thumbs/EP0n_thumbnail.jpg    yang benar-benar dikirim ke YouTube (±0,3 MB, ikut repo)
└── README.md
```

Master MP4 **tidak** ada di Git (17–22 MB per episode). Master tinggal di Drive
folder `video ready`; workflow mengunduhnya sendiri dari `drive_file_id`
(dicoba lewat `gdown`, lalu unduhan langsung `drive.usercontent.google.com` —
karena itu file master harus tetap **anyone with the link → Viewer**).

---

## Kenapa tidak ada yang bisa terunggah sendiri

Unggahan ke kanal orang lain tidak bisa dibatalkan dengan `Ctrl+Z`. Karena itu tiga
lapis:

1. Workflow hanya punya pemicu `workflow_dispatch` — tidak ada `push`, tidak ada
   jadwal. Tidak ada yang berjalan tanpa satu orang menekan **Run workflow**.
2. Job terikat ke environment `production` yang punya **required reviewers**.
   Tanpa klik *Approve*, langkah unduh pun tidak mulai.
3. Default input `dry_run: true`. Dry-run menyusun payload penuh dan mencetaknya,
   lalu berhenti — nol request ke Zernio.

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

### 3. Jalankan percobaan kering

Actions → **Upload episode to YouTube (Zernio)** → **Run workflow**:

- episode: `EP01`
- visibility: `public`
- dry_run: **`true`**

Setelah approve, langkah *Cek metadata* mencetak payload lengkap: judul, deskripsi,
tag, judul playlist, dan `mediaItems`. **Baca judulnya di situ.** Kalau ada yang
salah, perbaiki `EP0n.json` dan ulangi dry-run — bukan mengunggah lalu mengedit
di YouTube.

### 4. Unggah sungguhan

Ulangi dengan `dry_run: false`. Hasilnya:

- ringkasan di halaman run (tabel episode/status/tautan),
- log JSON di artifact `upload-log-*` (90 hari),
- tautan video di `post.platforms[].platformPostUrl`.

Mulai dengan `visibility: unlisted` untuk episode pertama, tonton di YouTube asli,
lalu ubah ke publik dari YouTube Studio. Video yang belum siap lebih murah
di-unlisted-kan daripada dihapus setelah ditonton.

---

## Unggah dari laptop (kalau tidak mau lewat Actions)

```bash
cd ODDCHAPTER_BRAND
export ZERNIO_API_KEY=...  ZERNIO_YOUTUBE_ACCOUNT_ID=...

python3 tools/upload_zernio.py EP01                         # dry-run, baca payload
python3 tools/upload_zernio.py EP01 --send --visibility unlisted
python3 tools/upload_zernio.py --all --send                 # EP01–EP03 berurutan
```

`tools/upload_zernio.py` hanya memakai pustaka standar Python — tidak perlu
`pip install` apa pun. `--media-dir` menunjuk folder berisi
`EP0n_1080x1920_master.mp4` + `EP0n_thumbnail.jpg`; tanpa flag itu, ia mencari di
`10_FILM/remotion/output/episodes/` (butuh thumbnail di folder yang sama, lihat
`10_FILM/upload/`).

---

## Isi judul dan hook saat ini

| EP | Judul (≤100 kar.) | Panjang | Hook (baris pertama deskripsi) |
|---|---|---|---|
| 01 | Tiga Penjaga Masuk ke Menara Itu. Tidak Ada yang Melihat Mereka Keluar. | 71 | Tiga penjaga masuk ke menara itu pada 15 Desember 1900. Tidak ada yang melihat mereka keluar. |
| 02 | Mereka Memotong Tenda Itu dari Dalam, Lalu Berlari ke Salju Tanpa Sepatu | 72 | 1 Februari 1959. Sembilan pendaki memotong tenda mereka sendiri dari dalam, lalu keluar tanpa sepatu. |
| 03 | Kapal Itu Masih Bisa Berlayar. Sepuluh Awaknya Naik Sekoci dan Hilang. | 70 | 5 Desember 1872. Sepuluh awak Mary Celeste hilang. Kapal dan muatannya masih ada. |

Aturan judul yang dipakai: satu kalimat pernyataan yang memuat satu hal mustahil,
tanpa kata "misteri", tanpa emoji, tanpa huruf kapital semua. Tiap JSON juga
menyimpan `title_alternatives` (3 varian) — kalau judul utama tidak dapat klik,
ganti dan uji lagi; jangan mengubah judul video yang sudah berumur lebih dari
seminggu, karena itu memutus rekomendasi yang sedang berjalan.

Komentar pertama tiap episode adalah pertanyaan, bukan ajakan like. Yang dibeli
adalah balasan, bukan tayangan.

---

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
