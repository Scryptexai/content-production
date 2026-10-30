# 03 — Publishing semi-otomatis dengan Zernio

Tujuan: **35 video × 3 platform = 105 post dalam 7 hari**, tanpa pernah "asal upload".
Otomatis sampai batas aman, **satu klik persetujuan per post**.

```
repo (draf + jadwal)  →  runner lokal (approve per post)  →  Zernio (jadwal & publish)
        ↑                        ↑                                  ↑
   git pull               mesin kamu + API key              token platform tetap di Zernio
```

---

## 1. Kenapa dua lapis (dan bukan satu)

| Lapis | Jalan di mana | Butuh rahasia? | Isi |
|---|---|---|---|
| **Kalender draf** (`automation/zernio/content/calendar.json`) | mana saja, termasuk sandbox/CI | tidak | 105 draf, judul, caption, jadwal |
| **Runner push** (`automation/zernio/runner/zernio.mjs`) | **mesin kamu** | ya (`ZERNIO_API_KEY`) | upload media, approve, kirim ke Zernio |
| **MCP hosted Zernio** (opsional) | klien MCP kamu | ya (OAuth/API key) | 280+ tool: inbox, analitik, ads |

Sandbox ini hanya bisa menghubungi GitHub + registry paket. **`zernio.com` dan
`mcp.zernio.com` tidak bisa dijangkau dari sini** — jadi semua langkah push harus
kamu jalankan di lokal. Itu juga alasan desainnya: tidak ada autoPublish.

Fakta REST yang dipakai runner (base `https://zernio.com/api/v1`, Bearer key):

```
GET  /v1/accounts?profileId=…            daftar akun terhubung
GET  /v1/connect/{platform}?profileId=…  url approve di browser
POST /v1/media/presign → PUT bytes       upload media, dapat publicUrl
POST /v1/posts                           jadwalkan (scheduledFor + platforms[])
GET  /v1/posts?status=scheduled          antrean
```

---

## 2. Setup di mesin lokal (sekali, ±15 menit)

```bash
# 1. repo
git clone https://github.com/Scryptexai/content-production.git
cd content-production

# 2. isi .env (JANGAN commit)
cp automation/zernio/.env.example automation/zernio/.env
#   ZERNIO_API_KEY   → https://zernio.com/dashboard/api-keys
#   ZERNIO_PROFILE_ID→ terlihat di dashboard / dipakai di semua endpoint

# 3. cek koneksi
node automation/zernio/runner/zernio.mjs accounts
```

`accounts` mencetak akun yang sudah terhubung dan **menulis pemetaan channel →
account id** ke `automation/zernio/.zernio-mapping.json` (gitignored).

### Menghubungkan 6 akun

```bash
node automation/zernio/runner/zernio.mjs connect
```

Perintah ini mencetak satu URL per platform (YouTube, TikTok, Instagram).
Buka URL-nya di browser, setujui akun **beauty** dulu, ulangi untuk akun
**relationship**. Setelah semua muncul di `accounts`, pemetaan 6 channel
tersimpan otomatis.

> Kalau ada dua akun di platform yang sama (mis. 2× TikTok), `accounts` akan
> memilih yang pertama. Betulkan manual di `.zernio-mapping.json`.

### Daftarkan MCP (opsional, untuk agen)

`automation/zernio/mcp.config.example.json` berisi dua entri:
`zernio-drafts` (lokal, tanpa token) dan `zernio` (hosted, butuh key).
Salin ke config klien MCP kamu (`claude_desktop_config.json` / `.mcp.json`).

---

## 3. Alur per minggu (yang sebenarnya kamu lakukan)

```bash
# Senin pagi
git pull                                   # draf & jadwal terbaru
python3 automation/build_schedule.py       # regenerasi 105 draf (opsional)
python3 automation/validate.py             # QC: 35×3, slot, urutan, panjang caption

# tinjau isi
cat content/calendar-7-days.md
cat content/day-01.md

# uji payload tanpa mengirim apa pun
node automation/zernio/runner/zernio.mjs push --dry-run --day 1

# kirim hari 1 saja, approve per draf (y/N)
node automation/zernio/runner/zernio.mjs push --day 1
```

Setiap `y` = satu post terjadwal di Zernio pada jam yang sudah ditentukan
(UTC, dari `publishAt`). Setiap `N` = draf tetap `DRAFT` dan bisa dikirim nanti.

```bash
node automation/zernio/runner/zernio.mjs status   # antrean di Zernio
node automation/zernio/runner/zernio.mjs sync     # tarik status PUBLISHED/FAILED
```

**Ritme yang disarankan:** kirim 1 hari (15 post) setiap malam untuk hari
berikutnya. Total waktu approval ±5 menit/hari.

---

## 4. Media

Runner mengunggah video lewat presign:

```
POST /v1/media/presign {fileName, contentType, size} → {uploadUrl, publicUrl}
PUT  uploadUrl (bytes)
POST /v1/posts { mediaItems: [{type:'video', url: publicUrl}] }
```

File yang diharapkan (dibuat oleh pipeline produksi, lihat `04-production-pipeline.md`):

```
assets/video/B01.mp4   1080×1920, 30 fps, h264 + AAC, ≤ 60 MB
assets/video/B01.jpg   poster (frame dengan teks terbanyak)
```

`assets/video/*.mp4` **tidak masuk git** (lihat `.gitignore`); simpan di Drive
sampai saat push, lalu taruh di folder itu secara lokal.

---

## 5. Jadwal yang sudah dibuat

| | |
|---|---|
| Mulai | **Senin, 2 November 2026** (07 hari) |
| Slot WIB | 06:30 · 11:45 · 16:30 · 20:00 · 21:30 |
| Per hari | 3 beauty + 2 relationship |
| Total | 35 konten → **105 post** |
| Timezone API | UTC (`publishAt`), tampilan WIB (`publishAtWib`) |

Peta lengkap: [`content/calendar-7-days.md`](../content/calendar-7-days.md).
Lembar kerja CSV: `automation/zernio/content/schedule.csv`.

---

## 6. Kalau ada yang gagal

| Gejala | Sebab biasanya | Tindakan |
|---|---|---|
| `401` | API key salah/kedaluwarsa | buat key baru di dashboard |
| `account id belum ada` | `accounts` belum dijalankan | jalankan `accounts`, cek `.zernio-mapping.json` |
| upload media gagal | nama file / ukuran / tipe | cek `assets/video/<ID>.mp4` ada & < 100 MB |
| post `FAILED` | platform menolak (durasi, rasio, klaim) | baca alasan di dashboard, perbaiki, kirim ulang manual |
| jadwal meleset | zona waktu | `publishAt` harus UTC; WIB = UTC+7 |

---

## 7. Keamanan (tidak bisa dinegosiasikan)

1. **Tidak ada token di repo.** `.env`, `.zernio-mapping.json` di-.gitignore.
2. **Tidak ada autopublish.** `autoPublish: false` di semua channel; runner
   menolak `--yes` tanpa `--dry-run`.
3. **Setiap post punya `reviewNote`** berisi siapa yang menyetujui dan post id Zernio.
4. **Revoke** = hapus API key di dashboard Zernio; tidak ada salinan di repo.
5. **Media** diunggah lewat presign, tidak pernah lewat git.
