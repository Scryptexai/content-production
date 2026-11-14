# Jadwal tayang 15 Nov 2026 (via Zernio, `scheduledFor` — bukan `publishNow`)

| jam WIB | episode | durasi | judul | post Zernio | status |
|---|---|---|---|---|---|
| 07.30 | EP08 | 38,2 s | Label di Bajunya Dipotong. 1970: Dia Hilang Tanpa Nama. | `6af89b196abb0bb79a196d29` | scheduled |
| 12.30 | EP09 | 39,4 s | Kertas di Sakunya Cuma Dua Kata. 1948: Dia Tak Punya Nama. | `6af8a02b588bc489d6d82eb5` | scheduled |
| 18.30 | EP10 | 44,6 s | Mereka Menulis Buku dalam Bahasa yang Tak Dimengerti Siapa pun. | `6af8a2cdc3753df892a8fc08` | scheduled |

## Yang berubah di ketiga episode ini

1. **Suara kembali ke narator internal kanal** `ojz6ro9PB1xDu44lymdM` (setelan Denas
   dan seluruh `polish`/atempo dihapus). Konsistensi diukur: `voice_consistency.py`
   LULUS di ketiga episode.
2. **Durasi 35–45 detik** (dulu 51–73). EP08 105→81 kata, EP09 125→82, EP10 →91.
3. **Narasi mulai 0,15 dtk** dan cover hanya 0,5 dtk (dulu 1,5 dtk) — 30–57% penonton
   menggeser di 1–2 detik pertama.
4. **Penutup berupa pertanyaan** yang mengundang komentar; pertanyaan komentar juga
   ditulis di deskripsi dan komentar pertama.
5. **Backsound diukur, bukan ditebak**: bed −36/−38 LUFS, selisih ke narasi
   17,1 dB (EP08) dan 17,4 dB (EP09). Semua segmen narasi disamakan RMS-nya.

## Catatan terbuka

- Video EP08 lama yang masih publik dan harus dihapus manual pemilik:
  `F6BGrQhYmaA` (v1) dan `3E2ekjMZPkc` (v2, yang ditolak).
- EP09/EP10 belum punya foto plat (hanya plate + teks). EP01–EP04 juga begitu, jadi
  ini tampilan yang sah, bukan kekurangan teknis.

## Angka hasil ukur ketiga master

| | EP08 | EP09 | EP10 |
|---|---|---|---|
| durasi | 38,2 s | 39,4 s | 44,6 s |
| narasi / jeda | −16,2 / −33,3 dBFS | −17,2 / −34,5 dBFS | −16,2 / −34,6 dBFS |
| selisih VO↔bed | **17,1 dB** | **17,4 dB** | **18,4 dB** |
| loudness | −14,0 LUFS | −13,9 LUFS | −14,0 LUFS |
| true peak | −1,7 dBTP | −1,7 dBTP | −1,7 dBTP |
| VO mulai | 0,15 s | 0,15 s | 0,15 s |
| konsistensi suara | LULUS (9 segmen) | LULUS (9 segmen) | LULUS (10 segmen) |

Semua dijadwalkan lewat `POST /v1/posts` dengan `scheduledFor` + `timezone: Asia/Jakarta`
— **tidak ada `publishNow`**.
