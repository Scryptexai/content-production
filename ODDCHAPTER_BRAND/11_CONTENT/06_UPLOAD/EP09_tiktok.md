# EP09 — tayang YouTube + TikTok

| kanal | status | tautan | post Zernio |
|---|---|---|---|
| YouTube (@oddchapter7) | tayang 15 Nov 2026 13:02 UTC | https://www.youtube.com/watch?v=xyK0qZFEAtE | `6af9ad63febdc55cc7b5e9bc` |
| TikTok (@oddchapter7) | tayang 15 Nov 2026 13:11 UTC | https://www.tiktok.com/@oddchapter7/video/7708384803367734546 | `6af9af0d1ce3b59aa97bc8da` |

Master yang dipakai keduanya: Drive `1leWLFt4QuLEgXMSmnemYAXRWlMr9vUCT`
(`EP09_1080x1920_master.mp4`, 53,78 dtk, 32,9 MB, VO buatan pemilik).
Cover: `11_CONTENT/06_UPLOAD/thumbs/EP09_thumbnail.jpg` (`TAS BERISI BATU`).

## Jalur TikTok (baru, 16 Nov 2026)

Zernio ternyata sudah punya akun TikTok kanal yang tersambung
(`6aeddf6a0b5ec69b89139f4e` / `oddchapter7`, izin `video.publish`).
Dulu tool-nya hanya menulis `platform: youtube`; sekarang:

- `upload_zernio.py --tiktok-only` → satu post khusus TikTok,
  `platformSpecificData: {title, privacyLevel}`, caption dari `tiktok_caption` di
  `06_UPLOAD/EPxx.json`, idempotency key dibedakan (`-tiktok`) supaya tidak
  bertabrakan dengan post YouTube.
- Antrean: berkas di `06_UPLOAD/queue/` dengan `"tiktok_only": true`.
- Akun TikTok dicari otomatis dari `GET /v1/accounts`; hasilnya dicatat di
  `published.json` sebagai `tiktok_post_id` / `tiktok_url`.
- `--lookup` sekarang menyertakan status tiap platform (`zernio-posts.json`)
  dan daftar platform tersambung (`zernio-accounts.json`).

## Caption TikTok yang dipakai (137 karakter, 4 hashtag)

```
Tasnya berisi batu, bukan alasan untuk hilang. Mahasiswa itu ditemukan di danau kampus.
#misteri #truecrime #kasustakterpecahkan #oddchapter
```
