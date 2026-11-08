# ODDCHAPTER — STRATEGI KONTEN 21 HARI

> **Revisi.** Bagian §2–§4 di dokumen ini (H·R·R, enam tipe hook, struktur
> 45–60 s) sudah **digantikan** oleh `00B_KERANGKA_STORYTELLING.md`. Alasan:
> H·R·R adalah struktur retensi, bukan struktur cerita. Yang dipakai sekarang
> adalah model narrative nonfiction (komplikasi → gagal → bingung → wawasan →
> resolusi) dengan satu protagonis, satu keinginan, dan satu tanaman per episode.


Dokumen ini adalah aturan mainnya. Semua script, thumbnail, dan visual plan di
folder ini tunduk pada aturan di bawah — bukan sebaliknya.

---

## 1. Apa yang dijual kanal ini

Bukan "cerita horor", bukan "misteri konspirasi". Yang dijual satu hal:

> **Kamu masuk dengan satu dugaan. Kamu keluar dengan dugaan yang lain.**

Itu janji tagline `KISAH NYATA. DI LUAR DUGAAN.` Setiap episode wajib punya satu
titik balik yang membuat penonton berkata "oh, ternyata bukan itu". Kalau tidak ada
titik balik, itu bukan episode ODDCHAPTER — itu artikel.

**Niche:** kisah nyata terdokumentasi yang berakhir jauh dari dugaan.
**Bukan niche:** horor, kerasukan, konspirasi tanpa bukti, teori tanpa sumber.

---

## 2. POV — dan kenapa hanya tiga yang boleh dipakai

POV adalah keputusan paling menentukan retensi. Empat kandidat, tiga dipakai:

| POV | Kalimat khas | Dipakai? | Alasan |
|---|---|---|---|
| **A — "KAMU"** (orang kedua) | "Kamu berdiri di dermaga itu pukul tiga pagi." | **Ya, POV utama** | Menempatkan penonton *di dalam* kejadian. Hook orang kedua menahan scroll lebih lama karena otak memperlakukan "kamu" sebagai instruksi, bukan informasi. |
| **B — "SAKSI"** (orang ketiga + arsip) | "Catatan penjaga berikutnya menyebut satu hal." | **Ya, POV investigasi** | Dipakai saat cerita bersandar pada dokumen, laporan, foto, rekaman. Objektif, tidak mengarang isi kepala orang. |
| **D — "KITA"** (kolektif) | "Kita semua salah membaca foto ini selama 70 tahun." | **Ya, POV koreksi** | Dipakai untuk episode yang intinya "yang kamu tahu selama ini keliru". |
| C — "DIA" (orang pertama tokoh) | "Aku membuka pintu itu." | **TIDAK** | Untuk tokoh nyata, POV-C berarti mengarang isi kepala orang yang pernah hidup. Itu fabrikasi. Dilarang. |

**Aturan POV:**
1. Satu episode = satu POV, konsisten dari hook sampai loop.
2. POV-A hanya boleh memakai detail yang terdokumentasi ("kamu" = posisi, bukan pikiran tokoh).
3. Tidak ada dialog yang dikarang. Kutipan hanya kalau ada di sumber primer.

---

## 3. Struktur script: KLIMAKS DI AWAL → CUT → CERITA

Yang menahan penonton bukan pembuka yang dihias rapi. Yang menahan penonton
adalah **klimaks yang dipotong di tengah**, lalu ceritanya mundur ke awal. Urutan
ini tiga langkah dan tidak boleh ditukar (lengkap: `00B` §0):

```
KLIMAKS + ENTITAS  0–9 s    momen paling ekstrem di episode. Satu fakta bertanggal,
                            dan yang terlihat di layar adalah ORANGNYA, bukan pemandangan.
CUT + PERTANYAAN   9–15 s   cerita dipotong tepat di titik yang membuat orang bertanya:
                            apa yang terjadi? bagaimana bisa? kok bisa begitu?
CERITA DARI AWAL   15–21 s  baru sekarang "Sebelas hari sebelumnya…" — siapa, di mana, mau apa.
BUKTI              21–42 s  fakta berurutan, tiap 3–4 detik satu informasi baru.
TITIK BALIK        42–51 s  dugaan pertama runtuh. Detail yang ditanam di awal berubah makna.
SISA + LOOP        51–63 s  yang masih tidak terjawab, lalu kalimat terakhir memanggil hook.
```

Angka di atas adalah EP01 v6 yang sudah dirender; episode lain boleh 45–63 detik,
tetapi proporsinya sama.

**Yang dilarang di setiap script:**
- "Hai guys", "selamat datang kembali", perkenalan kanal di 5 detik pertama.
- Menjelaskan latar sebelum klimaksnya dipotong (detik pertama = suasana).
- Membuka dengan pemandangan kosong; frame pertama setelah thumbnail wajib entitas.
- Menutup dengan "like dan subscribe" — ganti dengan loop.
- Klaim faktual tanpa status sumber.

---

## 4. Copywriting: enam hook yang boleh dipakai

Setiap episode memakai **satu** dari enam pola ini, dan ditulis ulang tiga kali
sebelum dipilih. Hook final ada di file script; dua alternatifnya disimpan di
`HOOK_BANK.md` untuk A/B test.

| # | Pola | Contoh |
|---|---|---|
| 1 | Detail spesifik yang tidak masuk akal | "Meja makan di rumah itu sudah disiapkan. Untuk empat orang. Tidak ada yang pulang." |
| 2 | Angka yang terlalu aneh untuk bohong | "Tiga pria menghilang dari menara. Jam di dinding masih berdetak. Makan malam mereka masih hangat." |
| 3 | Kontradiksi | "Kapal itu ditemukan kosong. Barang bawaannya utuh. Perahunya hilang." |
| 4 | Perintah langsung | "Jangan cari nama orang ini di internet sebelum kamu tahu satu hal." |
| 5 | Pengakuan salah | "Selama 70 tahun kita diberi tahu satu versi. Bukti fisiknya bilang lain." |
| 6 | Adegan menengah-aksi | "Di tengah kalimatnya, suaranya berhenti. Rekaman masih berjalan 40 menit." |

**Aturan urutan di atas semua pola:** hook bukan ringkasan cerita, melainkan
klimaksnya — diucapkan seperti sudah terjadi, dengan entitas yang bisa ditunjuk.
Pertanyaannya (`tanya` di `content_data.py`) harus pertanyaan yang nanti dijawab
`turn_verdict`; pertanyaan yang tidak pernah dijawab adalah klik yang dibohongi.

**Aturan kalimat:** maksimal 14 kata (16 untuk baris naskah), satu benda
konkret per baris, tanpa kata pengisi, tanpa kalimat ringkasan. Aturan lengkap
dan gerbangnya: `00D_PSIKOLOGI_AUDIENS.md`. Kata kerja aktif. Tanpa "sangat", "cukup",
"banyak sekali". Satu kalimat = satu langkah cerita.

---

## 5. Rencana posting: 3 post/hari × 7 hari

Satu episode = satu video vertikal 1080×1920 → dipublikasikan ke **tiga platform
sekaligus** (YouTube Shorts, Facebook Reels, TikTok). Tiga slot per hari:

| Slot | Jam (WIB) | Karakter slot | Kategori yang cocok |
|---|---|---|---|
| **PAGI** 07.00 | bangun–berangkat kerja | pendek, 40–45 s, hook keras | HILANG (kriminal/misteri) |
| **SIANG** 12.30 | istirahat makan | penjelasan, 50–60 s, rasa ingin tahu | ANEH (sains & anomali) |
| **MALAM** 19.30 | santai sebelum tidur | atmosferik, 55–60 s, gelap | TERSEMBUNYI |

21 episode = 7 hari × 3 slot. Urutan sengaja dibuat: episode terkuat di hari 1,
kategori dicampur supaya feed tidak monoton.

---

## 6. Aturan sumber (tidak bisa dinegosiasi)

Setiap script punya baris `SUMBER:` dengan salah satu status:

- `VERIFIED` — ada rujukan primer/ilmiah yang sudah dicek di sesi ini.
- `NEEDS-SOURCE` — peristiwa nyata dan terdokumentasi luas, tetapi rujukan belum
  diverifikasi di sesi ini. **Tidak boleh naik tayang sebelum baris ini diisi.**
- `LEGEND` — cerita rakyat/legenda. Wajib disebut "legenda" di narasi.

Gerbang ini sudah ada di `tools/episode.py check` — gate `evidence` akan gagal
kalau baris sumber kosong.

---

## 7. Standar visual (ringkas)

- Palet: Ink `#17191D` · Ivory `#F4F0E8` · Sage `#A7B0A1` · Signal Orange `#F26A3D`
  (orange = aksen, maksimal satu per frame).
- Tipografi: Space Grotesk (display) + Inter (teks). Tanpa font lain.
- Timpa-aman 1080×1920: teks di dalam x 96–984, y 300–1500.
- Caption terbakar wajib (mayoritas orang menonton tanpa suara).
- Audio: −14 LUFS, true peak −1.5 dBTP, narasi satu suara konsisten.

Rencana visual per episode ada di `05_VISUAL_PLAN.md`, ditulis **setelah** script
dan thumbnail disetujui — sesuai urutan kerja yang diminta.

---

## 8. Status dokumen ini

Rencana di atas sudah dieksekusi menjadi artefak konkret:

| bagian strategi | artefak |
|---|---|
| 21 ide + jadwal 7×3 | `01_IDEA/21_IDEA_CONTENT.md`, `01_IDEA/CONTENT_CALENDAR.csv` |
| struktur script 45–60 s | `02_SCRIPT/EP01…EP21_*.md` |
| headline per episode | judul tiap script = headline; dipakai di thumbnail dan caption |
| visual (setelah thumbnail) | `03_THUMBNAIL/` lalu `05_VISUAL_PLAN.md` |

Semua 21 episode masih berstatus `NEEDS-SOURCE`. Itu disengaja: kerangka cerita,
POV, dan hook-nya selesai, tetapi verifikasi rujukan belum. Gate `evidence` akan
tetap menolak semuanya sampai baris sumbernya diubah.
