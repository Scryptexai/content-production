# EP10 — tayang YouTube + TikTok (15 Nov 2026)

**Judul:** Dua Kardus di Trotoar Sudirman. Isinya Tubuh Tanpa Nama.
**Topik:** kasus "Setia Budi 13" — dua kardus di trotoar Jalan Jenderal Sudirman,
Setiabudi, Jakarta, 23 November 1981; jasad pria tanpa identitas, dimakamkan
27 November 1981 di TPU Tegal Alur.

| platform | tautan | post id | jam (UTC) |
|---|---|---|---|
| YouTube | https://www.youtube.com/watch?v=KQR0s52rbCE | `6af9c511615d6b707b81a203` | 15 Nov 2026 14:43 |
| TikTok | https://www.tiktok.com/@oddchapter7/video/7708409619067997441 | `6af9c5a14cb7b88c916124d8` | 15 Nov 2026 14:46 |

## Master

- Drive: `1YfNXyS4qKM39zybT7LLpMkpq3JS7ibdX` (`EP10_1080x1920_master.mp4`)
- 59.953.240 B · 59,90 s · 1797 frame · h264 1080×1920 30 fps · aac 48 kHz
- −14,7 LUFS · true peak −1,4 dBFS · sha256 `d04f269e…c8d2d`
- Folder Drive: `video ready` `1fVoOvZgiYB3V7S2C5LfMrCpo-c4Xxzo2`

## Suara dan timing

- VO **buatan pemilik**, bukan TTS: Drive `1x15AvOEZSd4LhXOd6eId2x8-DxIUfrT6`
  (`VO EP10.mp3`, 961.106 B, 59,01 dtk, satu trek — tidak dipecah, tidak di-TTS ulang).
- `TIMESTAMP EP10.txt` → 7 blok; dipecah jadi 9 segmen, batas disnap ke jeda hening
  nyata (`silencedetect -35 dB`, 0,25 dtk). Lompatan 49→50 di timestamp user = jeda
  46,0–47,3 dtk. Detail di `10_FILM/remotion/public/audio/EP10/MANIFEST-VO.json`.
- Aset TTS lama (June & Jennifer Gibbons, "Mereka Menulis Buku dalam Bahasa yang Tak
  Dimengerti Siapa pun") dipindah ke `public/audio/_arsip/EP10_june-gibbons/` —
  tidak dipakai, dan jadwal lamanya (`6af8a2cdc3753df892a8fc08`) dibatalkan sebelum
  tayang sehingga tidak pernah muncul di kanal.

## Visual

9 foto per segmen (768×1376) dibuat baru di `public/plates/EP10/` dengan palet dan
gaya yang sama seperti EP01–EP08 (Ink `#17191D`, Ivory `#F4F0E8`, Sage `#A7B0A1`,
Orange `#F26A3D`). Cover: `DUA KARDUS` / `TANPA NAMA` (plate kardus di trotoar basah,
1080×1920). Tidak ada adegan tubuh; semua penggambaran implisit.

## Caption

YouTube (baris pertama = hook): *Dua kardus di Trotoar Sudirman 1981. Isinya
potongan tubuh manusia tanpa nama.*

TikTok (115 karakter + 4 tag):
`Dua kardus di trotoar Sudirman, 1981. Isinya tubuh tanpa nama.`
`#misteri #truecrime #kasustakterpecahkan #oddchapter`

## Cara kerja (pola baku berikutnya)

1. VO pemilik + timestamp di Drive → `drive-requests/EP10-vo.json` → run
   `drive-fetch.yml` → `git show origin/drive/inbox:drive-inbox/VO-EP10.mp3`.
2. `content_data.py`: blok `vo.cues` 9 segmen (teks + detik), caption, cue teks.
3. Foto 9 segmen + cover → `thumbnail_render.py render('EP10','9x16')`.
4. `build_timing.py` → `build_bed.py` → `build_sfx.py` → `build_episodes_json.py`
   → `node scripts/render-episode.mjs EP10`.
5. `upload_file` master ke folder `video ready`, `create_permission anyone/reader`.
6. `queue/EP10.json` (status `requested`, `approved`) → push → YouTube tayang;
   `queue/EP10-tiktok.json` (`tiktok_only: true`) → push → TikTok tayang;
   `queue/EP10-platforms.json` (lookup) → ambil URL platform.

Catatan: buku besar `published.json` harus **bersih** dari jadwal lama sebelum
mengunggah — selama `EP10` masih tercatat (jadwal TTS), `upload_zernio.py` melewati
episode itu (tercatat = "sudah tayang") dan job berakhir gagal.
