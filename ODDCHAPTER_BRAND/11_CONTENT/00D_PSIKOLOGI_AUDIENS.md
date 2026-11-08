# 00D — PSIKOLOGI AUDIENS, KALIMAT PER KALIMAT

Dokumen ini menjawab satu keluhan yang benar: **banyak aturan, tapi belum tentu
semua diterapkan.** Karena itu aturannya di sini bukan nasihat — sebelas di
antaranya dijaga `tools/check_story.py` dan akan menggagalkan episode.

Tesisnya satu kalimat:

> Penonton tidak menonton cerita kita. Dia menonton **dirinya sendiri** di dalam
> cerita kita. Kalau sebuah kalimat tidak menyentuh dirinya, kalimat itu hanya
> informasi yang lewat.

---

## 1 · TIGA PERTANYAAN UNTUK SETIAP KALIMAT

Sebelum satu kalimat masuk naskah, ia harus lolos tiga pertanyaan. Kalau ada satu
jawaban "tidak", kalimat itu belum selesai ditulis — bukan salah, belum selesai.

| # | pertanyaan | kalau gagal |
|---|---|---|
| 1 | Setelah kalimat ini, apa yang penonton **belum tahu**? | kalimat itu menutup, bukan membuka — matikan |
| 2 | Ini **pernah dialami siapa**? (fisik, sosial, atau intelektual) | penonton tidak punya tempat masuk |
| 3 | Kalau kalimat ini dihapus, **apa yang hilang**? | kalau tidak ada yang hilang, ia hiasan |

Aturan 1 melahirkan **kail**: setiap kalimat meninggalkan satu ujung terbuka.
Aturan 2 melahirkan **relatabilitas**. Aturan 3 melahirkan **ekonomi**.

---

## 2 · KAIL — EMPAT JENIS, TIDAK ADA YANG KELIMA

Kalimat yang "mengundang diskusi" bukan kalimat yang ramai. Ia kalimat yang
membuat otak penonton **menghitung sendiri**. Empat jenis kail yang dipakai:

| kail | bentuk | contoh | yang terjadi di kepala penonton |
|---|---|---|---|
| **angka janggal** | jumlah yang tidak masuk akal | "1.701 tong alkohol utuh. Sepuluh orangnya hilang." | "kok bisa muatannya utuh?" |
| **kontradiksi** | dua fakta yang saling memukul | "Sepatu masih di dalam. Mereka keluar tanpa sepatu." | "berarti bukan karena dingin…" |
| **tindakan tanpa alasan** | ada yang dilakukan, alasannya ditahan | "Sembilan orang merobek tenda sendiri." | "kenapa?" |
| **pengalaman bersama** | penonton pernah ada di situ | "Kamu pernah tidur di tempat asing, dan dengar bunyi yang tak bisa dijelaskan." | "pernah. aku pernah." |

Larangan: **ringkasan**. Satu kalimat ringkasan ("selama bertahun-tahun banyak
teori muncul") mematikan tiga kail sekaligus karena tidak menyebut benda, tidak
meninggalkan celah, dan tidak bisa dialami. Dijaga gate butir 3d.

---

## 3 · RELATABILITAS — TIGA TINGKAT, DAN YANG MANA DIPAKAI

Cerita hilang di menara, di gunung, di kapal — semuanya jauh. Yang membuatnya
dekat bukan latarnya, tapi **satu hal yang penonton sudah tahu rasanya**.

| tingkat | yang disentuh | contoh di EP02 |
|---|---|---|
| **fisik** | tubuh | sakit punggung. Satu pendaki pulang karena itu — dan hanya dia yang hidup. |
| **sosial** | kebiasaan orang | "Kamu pernah tidur di tempat asing…" |
| **intelektual** | keyakinan yang pernah dipegang | "Enam puluh tahun kita diberi satu versi." |

Aturan produksi: **minimal satu baris `relate` per episode, diucapkan, memakai
kata "kamu" atau "kita", dan diletakkan sebelum bagian tension** — bukan di akhir
sebagai penutup. Penonton harus masuk ke dalam cerita sebelum cerita menuntut
apa-apa darinya.

Yang saya lakukan di EP01 salah separuh: barisnya memakai "kita", tapi
relatabilitasnya **intelektual** ("kalimat yang kita kutip seratus tahun itu tidak
ada di arsip"). Itu masuk akal, tapi tidak menyentuh tubuh. EP02 memakai yang
fisik: nyeri punggung.

---

## 4 · DISKUSI — PERTANYAAN YANG SENGAJA TIDAK DIJAWAB

Setiap episode punya dua pertanyaan, dan keduanya tidak boleh sama:

- `tanya` — pertanyaan yang **memotong** cerita di detik ke-9, dan **dijawab**
  oleh `turn_verdict`. Kalau tidak dijawab, penonton merasa dibohongi.
- `diskusi` — pertanyaan yang **tidak dijawab episode**, dan memang tidak boleh
  dijawab. Ini yang membuat orang menulis komentar, bukan sekadar menonton.

Syarat `diskusi`: bisa dijawab penonton dalam satu baris, jawabannya berbeda-beda
antar orang, dan bukan pertanyaan yang jawabannya ada di video. Dijaga gate
butir 1f.

Contoh EP02 — `diskusi`: "Di posisi mereka, kamu akan memotong tenda atau
menunggu sampai pagi?" Dua jawaban sama-sama masuk akal. Itu bahan komentar.

---

## 5 · SEPULUH ATURAN KALIMAT (yang dijaga gate)

| # | aturan | gate |
|---|---|---|
| 1 | kalimat pertama = pertanyaan **atau** fakta berangka | 1b |
| 2 | hook ≤ 14 kata, tanpa kata yang meminta (misteri, aneh, menakjubkan) | 1 |
| 3 | entitas disebut di hook, dan foto pembuka bukan lanskap | 0 |
| 4 | setiap baris naskah ≤ 16 kata | 3d |
| 5 | setiap baris memuat **satu benda konkret** yang bisa dilihat | 3d |
| 6 | tidak ada kata pengisi: sangat, cukup, benar-benar, sebenarnya, ternyata | 3d |
| 7 | tidak ada kalimat ringkasan ("bertahun-tahun", "sampai sekarang", "banyak teori") | 3d |
| 8 | ada satu baris `relate` yang menyapa penonton, sebelum tension | 1e |
| 9 | ada satu `diskusi` yang tidak dijawab episode | 1f |
| 10 | kalimat terakhir memanggil satu kata dari hook | 5 |

Sepuluh aturan ini **bukan** tambahan di atas naskah. Ia urutan kerja: tulis
kalimat → jalankan tiga pertanyaan §1 → pilih salah satu kail §2 → pastikan satu
baris relate §3 → tinggalkan satu diskusi §4 → baru gate.

---

## 6 · CONTOH AUDIT — EP02, BARIS PER BARIS

| baris | kail | relate | dibiarkan terbuka |
|---|---|---|---|
| "Sembilan pendaki memotong tenda dari dalam, lalu keluar tanpa sepatu." | tindakan tanpa alasan | — | kenapa memotong, kenapa tanpa sepatu |
| "Kenapa sembilan orang merobek rumah mereka sendiri, lalu berlari ke salju?" | kontradiksi | — | seluruh episode |
| "Kamu pernah tidur di tempat asing, dan dengar bunyi yang tak bisa dijelaskan." | pengalaman bersama | fisik/sosial | bunyi apa |
| "Satu dari mereka pulang lebih awal karena sakit punggung. Dia satu-satunya yang hidup." | angka janggal (1 dari 9) | fisik | apakah punggung menyelamatkannya |
| "Tiga minggu kemudian tenda itu ditemukan masih berdiri. Sepatu dan jaket masih di dalam." | kontradiksi | — | kenapa barang ditinggal |
| "Empat di dasar jurang. Tulang dada mereka retak." | angka janggal | — | gaya apa yang mematahkan dada |
| "Dua insinyur memodelkan longsoran salju. Hampir semua luka itu cocok." | angka janggal | — | kenapa tidak semuanya cocok |
| "Tapi tidak ada model yang menjelaskan kenapa mereka tidak kembali ke tenda." | kontradiksi | — | pertanyaan yang tinggal |

Kalau sebuah baris tidak bisa diisi ketiga kolomnya, baris itu belum layak masuk
render — sebagus apa pun bunyinya saat dibaca.

---

## 7 · YANG BELUM DIKERJAKAN

Jujur, supaya tidak terlihat selesai:

- `relate` + `diskusi` diisi untuk **EP01 dan EP02**. Sembilan belas episode lain
  sudah punya `entitas` + `tanya`, tetapi belum punya dua field ini — gate
  menandainya sebagai catatan untuk setiap episode yang belum diproduksi.
- EP01 sudah diperbaiki: baris setup-nya sekarang berbunyi *"Sebelas hari
  sebelumnya, di pulau batu Skotlandia. Tiga orang mengunci pintu dari dalam,
  seperti kamu."* — relatabilitasnya fisik, bukan lagi hanya intelektual.
  Master-nya dirender ulang sebagai v7.
- Aturan §1 (tiga pertanyaan) tidak bisa diperiksa mesin. Ia tetap kerja manual.
  Yang dijaga mesin hanya bentuk luarnya: panjang, benda konkret, kata pengisi,
  ringkasan, relate, diskusi.
