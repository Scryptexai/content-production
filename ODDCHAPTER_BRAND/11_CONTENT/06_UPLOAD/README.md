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

Actions → **Upload episode to YouTube (Zernio)** → **Run workflow**. Di dropdown
**Use workflow from**, pilih branch `arena/66ec29bf-content-production` — branch
default (`main`) masih memakai skrip dan judul yang lama. Workflow bisa dijalankan
dari branch mana pun yang memuat file ini.

Langkah pertama job adalah **Cek kredensial**: `GET /v1/profiles` dicetak, akun
YouTube-nya ditandai, dan `ZERNIO_YOUTUBE_ACCOUNT_ID` dicocokkan. Kalau secret
salah, job berhenti di sini — sebelum 20 MB video diunggah. Bisa diuji manual:

```bash
python3 tools/upload_zernio.py --check
```

- episode: `EP01`
- visibility: `public`
- dry_run: **`true`**

Setelah approve, langkah *Cek metadata* mencetak payload lengkap: judul, deskripsi,
tag, judul playlist, dan `mediaItems`. **Baca judulnya di situ.** Kalau ada yang
salah, perbaiki `EP0n.json` dan ulangi dry-run — bukan mengunggah lalu mengedit
di YouTube.

### 4. Unggah sungguhan

Ulangi dengan `dry_run: false`. Setiap `POST /v1/posts` membawa header
**`Idempotency-Key`** yang diturunkan dari sha256 master + judul: kalau job
timeout lalu dijalankan ulang dalam 24 jam, Zernio mengembalikan post yang sama
(HTTP 200), bukan membuat video kedua. Render baru = hash baru = video baru.
Kegagalan 409/429/5xx diulang otomatis dengan kunci yang sama.

Hasilnya:

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
