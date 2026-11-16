# [ARSIP 16 Nov 2026] Topik ini tidak dipakai.
#
# Alasan pemilik: "topik nya kurang menarik itu masalah nya". Naskahnya sendiri
# sudah dibersihkan dari kalimat ambigu (v2, 49 dtk, master di Drive
# 1zZ5imWXaZWqGFigD2VzQyN28VqBf-kW-), tetapi topiknya tetap dinilai lemah:
# Porong terlalu sering muncul di media Indonesia, dan tidak ada dokumen primer
# yang bisa dibuka penonton.
# Pengganti: T02 Valentich (EP11_enam-menit-terakhir-delta-sierra-juliet.md).

# EP11 — LUMPUR PANAS KELUAR DARI SAWAH DI PORONG SEJAK 2006, DAN BELUM BERHENTI

**Seri:** ANEH · **Slot:** SIANG 12.30 WIB · **POV:** B
**Narasi:** 93 kata · 10 segmen · target **35–45 detik**
**Suara:** narator internal kanal `ojz6ro9PB1xDu44lymdM` — sesi ini memakai
`voice-04` (VO internal yang sama dengan EP06–EP07), sesuai perintah pemilik 16 Nov 2026.

---

## 0 · KERANGKA

| unsur | isi |
|---|---|
| **Protagonis** | Warga Porong yang rumahnya tenggelam pelan-pelan. |
| **Mau** | Tinggal di tanah yang sama, sedekat mungkin dengan rumahnya. |
| **Hambatan** | Lumpurnya keluar dari dalam tanah, dan tidak ada yang berhasil menutupnya. |
| **Tanaman** | Titik semburan hanya 150 meter dari sumur gas. |
| **Celah** | Kenapa titik semburan muncul 150 meter dari sumur, bukan di sumurnya? |
| **Gambar melekat** | Rumah yang hanya kelihatan atapnya di tengah lumpur. |

## 1 · HOOK (mulai 0,15 dtk)

> Lumpur panas naik dari dalam tanah di Porong dan menelan rumah warga.

Alternatif: Sejak 2006, lumpur keluar dari dalam tanah di Porong. Sampai sekarang
belum berhenti.

## 2 · BEAT

| bagian | VO |
|---|---|
| TANYA | Dari mana lumpur di rumah warga itu datang? |
| RELATE | Kita mengira tanah di bawah rumah kita tidak bergerak. Kamu juga. |
| SETUP | 29 Mei 2006. Lumpur dan gas keluar dari sawah di Porong. |
| TENSION | Dua hari sebelumnya, 27 Mei, gempa mengguncang Yogyakarta. |
| TENSION | Sumur gas Banjar Panji satu cuma 150 meter dari semburan. |
| TENSION | Coba lihat: dua menit jalan kaki. |
| TURN | Lapindo bilang ini bencana alam. Tapi ahli geologi bilang sumbernya sumur gas Lapindo. |
| CONSEQUENCE | Dua puluh tahun kemudian, lumpur masih menutup jalan tol Porong. |

## 3 · TURN

Kutipan: **“Ini bencana alam. Gempa yang menyebabkan.”**

Pembalik: gempa Yogyakarta terlalu jauh untuk jadi penyebab. Yang 150 meter dari
titik semburan adalah sumur gas Lapindo — dan jarak itu sudah disebut sebelum turn,
jadi penonton bisa menghitung sendiri.

## 4 · ECHO + AJAKAN KOMENTAR

> Lumpur itu masih keluar. Kalau rumahmu di Porong, kamu pindah?

Pertanyaan komentar (tidak diucapkan di VO): **Kalau kamu tinggal di Porong, kamu pindah atau bertahan?**

## 4b · KONTRAK LIMA EFEK

| # | efek | perangkat |
|---|---|---|
| 1 | berhenti scroll | lumpur yang menelan rumah warga, dan belum berhenti |
| 2 | ada yang salah | tanah dianggap diam; di Porong ia keluar dari bawah rumah |
| 3 | bertahan | jarak 150 meter ditanam di tension, dibayar di turn |
| 4 | kejutan | tanaman dibaca ulang: penyebabnya bukan gempa, tapi sumur |
| 5 | diingat | atap rumah yang masih kelihatan di tengah lumpur |

## 5 · TEKS DI LAYAR

Cue: PORONG · 2006 · SUMBER: SUMUR
Caption: —, Dari mana?, Tanah yang diam., Porong, 2006., 27 Mei, Yogya.,
150 meter., 2 menit kaki., Bukan gempa., 20 tahun., Kamu pindah?
Stamp: `150 METER` (segmen 5), `2006` (segmen 3)

## 5b · AUDIT KALIMAT AMBIGU (16 Nov 2026)

Keluhan pemilik atas v1: "banyak kalimat ambigu". Yang diperbaiki, satu per satu:

| v1 | masalahnya | v2 |
|---|---|---|
| "Tanah keluar dari dalam tanah" | benda keluar dari dirinya sendiri; penonton tidak bisa membayangkan | "Lumpur panas naik dari dalam tanah" |
| "Dari mana semua tanah itu datang" | "tanah itu" tidak menunjuk benda apa pun | "Dari mana lumpur di rumah warga itu datang?" |
| "Kita lihat tanah sebagai benda yang diam. Duduk di rumah kita." | kalimat kedua tanpa subjek: siapa yang duduk? | "Kita mengira tanah di bawah rumah kita tidak bergerak. Kamu juga." |
| "tanah di Yogyakarta berguncang" | "tanah berguncang" bisa berarti longsor; penyebabnya gempa | "gempa mengguncang Yogyakarta" |
| "Sumur gas itu cuma 150 meter dari titik semburan" | "itu" tanpa anteseden; sumur mana? | "Sumur gas Banjar Panji satu cuma 150 meter dari semburan" |
| "Ahli geologi bilang getaran itu terlalu jauh" | "getaran itu" kabur; dan tidak ada pihak lawan yang disebut | "Lapindo bilang ini bencana alam. Tapi ahli geologi bilang sumbernya sumur gas Lapindo." |
| "lumpur itu masih menutup jalan dan rumah" | "menutup rumah" ambigu (menutup atap? menutup pintu?) | "masih menutup jalan tol Porong" |
| "Tanah itu masih keluar. Kamu pindah?" | "tanah itu" tanpa anteseden | "Lumpur itu masih keluar. Kalau rumahmu di Porong, kamu pindah?" |

Aturan yang sekarang diperiksa mesin (`check_story.py` §3e):
benda tidak boleh keluar dari dirinya sendiri, kalimat tidak boleh dibuka
"Itu/Ini" tanpa anteseden, dan kata berulang dalam satu beat dicatat untuk
diperiksa manusia.

## 6 · SUMBER

VERIFIED — Semburan lumpur panas Porong, Sidoarjo, Jawa Timur, mulai 29 Mei 2006;
gunung lumpur terbesar di dunia dan masih aktif. Pusat semburan berjarak ±150 meter
dari sumur eksplorasi gas Banjar Panji-1 milik Lapindo Brantas Inc. (operator blok
Brantas), yang mulai dibor awal Maret 2006. Gempa Yogyakarta 27 Mei 2006 — dua hari
sebelumnya — dipakai perusahaan sebagai penjelasan alternatif; sebagian besar
literatur menyimpulkan blow-out pengeboran. Semburan menenggelamkan permukiman dan
memutus jalur tol Surabaya–Gempol, jalan raya Surabaya–Malang, serta jalur kereta
lintas timur.

Catatan verifikasi: artikel Wikipedia Indonesia untuk topik ini bertanda “tanpa
rujukan”, jadi angka kerugian (Rp45 triliun) dan korban (≥20 orang) **belum** boleh
dipakai di VO sampai dicek ke dokumen BPLS/BPK. Naskah hanya memakai fakta yang juga
muncul di sumber berita arus utama: tanggal, lokasi, jarak 150 meter, dan status
masih aktif. Belum dibaca langsung: laporan BPLS, berkas perkara, dan paper penyebab
(Davies dkk. vs Mazzini dkk.) — verifikasi sebelum tayang.
