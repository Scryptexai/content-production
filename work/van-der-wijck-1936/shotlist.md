# SHOTLIST — AK-EP04 (11 beat, ±103 s)

Footage: stok yang sudah ada di repo (Coverr + Mixkit) — laut, kapal, pelabuhan malam, radio, asap, fajar.
Tidak ada foto arsip (foto Commons tidak bisa diunduh dari sandbox). Kalau pemilik mengunggah foto
Van der Wijck / monumen Brondong ke Drive, saya sisipkan di beat 9.

| # | Beat | Visual | Aset |
|---|---|---|---|
| 1 | hook 6 menit | laut malam gelap, horizon | `night_ocean_aerial` |
| 2 | kapal mewah "de meeuw" | kapal di laut siang, lambung putih | `s5_kapal_laut` |
| 3 | Surabaya → Semarang, 150 ton besi | pelabuhan, derek, barang | `s3_koper`/`harbor` |
| 4 | 12 mil dari Brondong, miring | ombak menerpa lambung, miring | `storm_waves_sea` |
| 5 | 6 menit | air gelap menelan, gelembung | `s6_ombak_batu` |
| 6 | tak ada kapal besar | laut kosong luas | `s9_laut_luas` |
| 7 | lima nelayan, 145 orang | perahu kecil di laut | `s5_perahu` |
| 8 | 8 pesawat Dornier | langit, awan rendah | `s2_awan_dari_kabin` |
| 9 | nakhoda selamat, operator tetap | dial radio menyala, lalu gelap | `mixkit_48533` |
| 10 | angka korban | asap/kabut, teks angka | `smoke_black_background` |
| 11 | 2021, 28 meter | bawah laut/cahaya biru, fajar | `s6_piha`/`coastline_aerial` |

Kartu teks: "19 OKTOBER 1936", "VAN DER WIJCK · KPM", "12 MIL DARI BRONDONG", "6 MENIT", "TIDAK ADA KAPAL BESAR", "5 NELAYAN · 145 ORANG", "8 PESAWAT DORNIER", "NAKHODA SELAMAT", "42 · 58 · 75", "28 METER", "@oddchapter7".

## Realisasi (final render, 95,7 s)

Shotlist di atas adalah rencana; hasil render memakai 25 shot. Yang berubah setelah QC frame:

| Rencana | Final | Alasan |
|---|---|---|
| `storm_waves_sea` (beat 4) | `s5_ombak_besar` + `s6_ombak_batu` | klip badai tidak ada di repo; ombak karang lebih dekat |
| asap/kabut untuk angka korban (beat 10) | `s2_langit_malam` (langit berbintang) | berkas `black_smoke_*` ternyata halaman batu + pohon, bukan asap |
| kabut Mixkit (beat 9) | pantai + kapal di kejauhan | `m_fog_4396` ternyata puncak gunung bersalju — salah musim untuk Laut Jawa |
| `s6_piha`/`coastline_aerial` (beat 11) | `s6_piha` (tebing) lalu `s9_darat_di_laut` (pantai) | tebing untuk "28 meter", pantai terang untuk penutup |
| `s3_koper` (beat 3) | `s8_dermaga` + `s5_kapal_laut` | koper bandara terlalu modern |

Semua footage Coverr 6,00 s; tidak ada shot yang melebihi jendela sumbernya (diperiksa
otomatis sebelum render). Klip yang dipakai: `s1_ombak_malam`, `s2_awan_dari_kabin`,
`s2_langit_malam`, `s5_kapal_laut`, `s5_kapal_kejauhan`, `s5_ombak_besar`, `s5_perahu`,
`s6_ombak_batu`, `s6_batu_laut`, `s6_piha`, `s8_dermaga`, `s9_laut_luas`,
`s9_darat_di_laut`, `night_ocean_aerial`, plus `m_radio_48533` (Mixkit).
