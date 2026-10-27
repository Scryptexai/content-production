# Storyboard — Skrip 01 "Shade Paling Gelap"
### 7 adegan · 71,3 detik · 1080×1920 · 30 fps

Setiap adegan di bawah ini punya **file audio sendiri** dan **still sendiri**, siap dimasukkan ke pipeline lipsync (SadTalker / MuseTalk / LatentSync) satu per satu. Aset sudah dipotong — lihat `assets/scene/manifest.json`.

```
foto + audio per scene  →  lipsync (GPU)  →  klip  →  dirangkai pipeline ffmpeg
```

---

## Ringkasan

| # | Adegan | Waktu | Durasi | Shot | Audio | Nada |
|---|---|---|---|---|---|---|
| 01 | **Hook** | 0:00–0:08,7 | 8,7 s | `alya-shot-01-hook.jpg` | `scene-01.mp3` | Rendah, mengaku |
| 02 | **Cerita** | 0:08,7–0:20,1 | 11,4 s | `alya-shot-02-story.jpg` | `scene-02.mp3` | Mengingat, menirukan BA |
| 03 | **Reveal** | 0:20,1–0:26,6 | 6,5 s | `alya-shot-03-reveal.jpg` | `scene-03.mp3` | Berbisik, membocorkan |
| 04 | **Tensi** | 0:26,6–0:39,5 | 12,9 s | `alya-shot-04-tension.jpg` | `scene-04.mp3` | Getir, terkendali |
| 05 | **Turn** | 0:39,5–0:45,5 | 6,0 s | `alya-shot-05-turn.jpg` | `scene-05.mp3` | Paling pelan |
| 06 | **Value** | 0:45,5–1:02,7 | 17,2 s | `alya-shot-06-value.jpg` | `scene-06.mp3` | Instruktif, cepat |
| 07 | **CTA** | 1:02,7–1:11,3 | 8,6 s | `alya-shot-07-cta.jpg` | `scene-07.mp3` | Hangat, mengajak |

---

## Adegan 01 — Hook
**Tujuan:** menghentikan *scroll* dalam 1 detik. Tidak ada pertanyaan, tidak ada janji — hanya pengakuan.

| | |
|---|---|
| **Framing** | *Medium close-up*, dagu sampai dada, mata di sepertiga atas |
| **Latar** | Kamar, rak foundation buram di belakang |
| **Gerak kamera** | Push-in pelan 1,02 → 1,10 |
| **Teks layar** | ⬛ `KARAKTER AI` (pojok kiri atas) · `@kakalya.jujur` (kanan atas) · **"INI UDAH PALING GELAP, KAK"** (2 baris, 0–3,4 s) |
| **Aksi karakter** | Bibir hampir tidak bergerak di 0,5 detik pertama. Tatapan lurus. **Tidak tersenyum.** |
| **Lipsync** | Mulut hampir tertutup di awal — model harus bisa menahan mulut tanpa *jitter*. Ini tes kualitas terbaik. |

---

## Adegan 02 — Cerita
**Tujuan:** membuat audiens melihat dirinya di kursi konter.

| | |
|---|---|
| **Framing** | *Medium shot*, pinggang ke atas — tangan ikut masuk frame |
| **Gerak kamera** | Push-in 1,02 → 1,09 |
| **Teks layar** | `AKU MASIH INGAT…` → `"INI UDAH PALING GELAP, KAK"` (di bagian kutipan) |
| **Aksi karakter** | Satu gestur tangan telapak terbuka di dada (sudah ada di still). Kepala sedikit miring saat menirukan suara BA. |
| **Lipsync** | Bagian terpanjang kedua (11,4 s) — paling rawan *drift* identitas. Pakai `--still` di SadTalker agar latar tidak ikut bergerak. |

---

## Adegan 03 — Reveal
**Tujuan:** satu-satunya bagian "rahasia". Volume turun, penonton merasa diberi akses.

| | |
|---|---|
| **Framing** | *Close-up* rapat, kepala dan bahu |
| **Gerak kamera** | Push-in 1.03 → 1,11, sangat lambat |
| **Teks layar** | `ADA 1 SHADE LAGI DI BELAKANG` |
| **Aksi karakter** | Dagu turun sedikit, mata naik ke kamera. Bibir tertutup di akhir kalimat. |
| **Lipsync** | Banyak konsonan bilabial (p, b, m) di "padahal", "rak belakang" — cek bibir benar-benar menutup. |

---

## Adegan 04 — Tensi
**Tujuan:** konflik. Ini adegan yang membuat orang berkomentar.

| | |
|---|---|
| **Framing** | Dua potongan: 0–33,0 s *close-up* ketat; 33,0–39,5 s lebih lebar |
| **Gerak kamera** | 1,04 → 1,12 (masuk), lalu 1,17 → 1,07 (menjauh) |
| **Teks layar** | `BUKAN KULITMU. STOKNYA.` |
| **Aksi karakter** | Alis turun, bibir terkatup. **Jangan dibuat marah** — kendali, bukan ledakan. |
| **Lipsync** | Nada getir berarti rahang bergerak minimal. Kalau model membuat mulut terlalu aktif, hasilnya jadi kehilangan wibawa. |

---

## Adegan 05 — Turn
**Tujuan:** inti emosional seluruh video.

| | |
|---|---|
| **Framing** | *Close-up*, wajah memenuhi frame, latar nyaris hilang |
| **Gerak kamera** | Push-in 1,02 → 1,09 — **paling pelan di seluruh video** |
| **Teks layar** | `BUKAN SALAH KULITMU` |
| **Aksi karakter** | Hampir diam. Hanya mata. Ini adegan dengan gerakan paling sedikit dan dampak paling besar. |
| **Lipsync** | Risiko utama: artefak di tepi hijab. Kalau meleleh, turunkan resolusi area wajah atau ganti ke LatentSync. |

---

## Adegan 06 — Value
**Tujuan:** memberi sesuatu yang bisa disimpan. Titik *save rate* tertinggi.

| | |
|---|---|
| **Framing** | Dua potongan: 45,5–54,0 s *medium*; 54,0–62,7 s lebih dekat |
| **Gerak kamera** | 1,03 → 1,10 lalu 1,16 → 1,06 |
| **Teks layar** | `1 RAHANG` → `2 TUNGGU 20 MENIT` → `3 CAHAYA MATAHARI` (muncul satu per satu, jangan sekaligus) |
| **Aksi karakter** | Telunjuk menyentuh rahang di poin pertama (sudah ada di still). Angka diucapkan dengan ketukan. |
| **Lipsync** | 17,2 detik paling panjang — pecah jadi 3 potongan agar model tidak kelelahan. Setiap potongan ±5–6 detik. |

---

## Adegan 07 — CTA
**Tujuan:** mengundang cerita, bukan emoji. Komentar panjang = distribusi.

| | |
|---|---|
| **Framing** | Dua potongan: 62,7–67,0 s *medium*; 67,0–71,3 s lebih dekat |
| **Gerak kamera** | 1,02 → 1,08 lalu 1,13 → 1,04 |
| **Teks layar** | `KAMU PERNAH DIBILANG INI?` → `TULIS DI KOMENTAR` |
| **Aksi karakter** | Tangan di dagu, lesung pipi muncul, alis naik satu. **Berhenti bicara 1,5 detik terakhir**, hanya menatap. |
| **Lipsync** | Kalimat tanya harus naik di akhir. Model lipsync hanya mengikuti audio — pastikan audionya sendiri yang membawa intonasi. |

---

## Catatan teknis untuk pipeline lipsync

| Parameter | Nilai | Alasan |
|---|---|---|
| Resolusi kerja | 1080×1920, wajah ≥ 480 px | Di bawah itu, artefak mulut terlihat |
| FPS | 30 | Cukup untuk sosmed, hemat GPU |
| Potongan maksimum per inference | **6 detik** | Di atas itu, identitas mulai bergeser |
| Audio | MP3 48 kHz mono → konversi ke WAV 16 kHz untuk model | Sebagian model hanya menerima WAV |
| Enhancer wajah | GFPGAN/CodeFormer **off** untuk karakter AI | Enhancer justru memuluskan kulit dan menghapus tekstur jujur |
| Latar | Bekukan (`--still`) | Latar yang ikut bergerak = terlihat palsu |

**Aturan besi:** hasil lipsync yang belum lolos QC 7 poin (lihat [`04-tools-video-avatar.md`](../playbook/04-tools-video-avatar.md) §6) **tidak boleh tayang**, sekalipun terlihat bagus di layar ponsel.
