# Kenapa video faceless terlihat murah — dan apa yang harus dibenahi

Catatan riset untuk Knot Theory. Ditulis setelah v2, v3, dan v4 ditolak dengan
alasan yang sama: **"teks masih dominan, animasi tidak jelas"**. Dokumen ini
mencatat penyebabnya secara terukur, bukan sebagai selera.

---

## 1. Diagnosis: apa yang salah di v2–v4

Diukur langsung dari kode yang dipakai (`anim2d.py`, `make_anim.py`):

| Ukuran | v4 | Ambang yang terbaca |
|---|---|---|
| Tinggi figur | 93,7 px dari 540 (17,4%) | 35–60% tinggi frame |
| Resolusi render | 960×540, di-upscale ke 1080p | render native 1080p |
| Lapis kedalaman | 1 (datar) | 4–7 lapis dengan parallax |
| Bayangan | tidak ada | bayangan kontak + bayangan antar-lapis |
| Blur kedalaman | tidak ada | per lapis |
| Kabut atmosferik | tidak ada | per lapis |
| Interpolasi gerak | linear | anticipation / overshoot / follow-through |
| Teks di frame | 138–240 px (dominan) | ≤ 56 px (keterangan) |

Satu angka menjelaskan sebagian besar keluhan: **figur 17% tinggi frame**.
Pada ukuran itu siluet manusia tidak terbaca sebagai manusia — yang terlihat
adalah piktogram. Ukuran teks 138 px, delapan kali lebih besar dari kepala
figur. Maka mata menangkap teks, bukan gerak. Itulah "video lirik".

---

## 2. Temuan riset

### 2.1 Yang membuat faceless terlihat mahal

Sumber: analisis produksi faceless (Satura AI, 2026; Subscribr; pixflow;
overseeros sound design guide).

1. **Motion grammar yang itu-itu saja** adalah penyebab utama kesan murah.
   "Every scene moves the same way … that sameness teaches the viewer what the
   next shot will look like before it arrives." Zoom pelan yang sama di setiap
   blok = presentasi slide.
2. **Perceived production value = relevansi gerak × kesesuaian tone ÷ friksi
   edit.** Menambah kata tidak menolong; menambah gerak yang relevan menolong.
3. **Editing transformatif** (bukan sekadar menempel footage) adalah yang
   membedakan dari konten "reused". Ini juga yang dijaga YouTube.
4. **Sound design** disebut berulang sebagai alat retensi termurah: whoosh
   hanya di tempat ada gerakan, ambience untuk tempat dan kontinuitas, dan
   jangan satu efek per potongan.

### 2.2 Kedalaman: 2.5D

Sumber: Moonb 2.5D guide, Pixeldust, Premation.

Teknik yang benar-benar menjual kesan dalam,urut dari yang paling berdampak:

1. **Bayangan** — "shadows are the quickest win I know: drop a soft shadow from
   a flat character onto the ground plane behind them and they stop floating on
   top of the world and start standing in it."
2. **Depth of field** — "the one people forget … it does more for the 'this
   looks expensive' reaction than any amount of extra parallax."
3. **Kabut atmosferik** — lapis jauh lebih pucat dan kontrasnya turun.
4. **Parallax** — jarak antar-lapis kecil; parallax berlebihan = "cardboard
   cutouts in a shoebox".
5. **Kamera yang berhenti** — "constant motion reads as a screensaver; let the
   camera arrive somewhere and stay for a beat."

### 2.3 Gerak: prinsip animasi

Sumber: 12 principles (Shortfilmcentral), secondary motion (Artemisia),
physics for animators (RMCAD), catatan CSC418 Toronto.

Yang paling sering hilang pada animasi prosedural — dan semuanya hilang di v4:

- **Anticipation** — gerakan kecil sebelum gerakan besar. Tanpa ini, aksi
  terasa mendadak. Uji 12-frame anticipation dibaca lebih bertenaga.
- **Follow-through & overlapping** — bagian tubuh selesai bergerak di waktu
  berbeda. "If a shot feels mechanical, check whether anything in frame is
  still settling after the main action ends."
- **Busur (arcs)** — hampir semua gerak alami melengkung, bukan garis lurus.
- **Slow in / slow out** — akselerasi dan deselerasi.
- **Secondary motion** — rambut, mantel, ujung kain tertinggal dari badan.
  Tanpa itu, animasi "dilabeli cheap atau belum selesai".

### 2.4 Siluet vs anatomi

Pelajarannya dari percobaan di repo ini: anatomi prosedural (kapsul + elips)
selalu kalah dari anatomi asli di ukuran besar — hasilnya terbaca sebagai
manekin karet. Yang tidak kalah adalah **siluet + cahaya tepi**. Film animasi
2D mahal memakai ini justru karena efektif: siluet dibaca otak sebagai
manusia, dan rim light memberi tahu dari mana cahayanya. Ini juga menyembunyikan
titik lemah model.

### 2.5 Bunyi

Sumber: overseeros, ocularsounds, shortzly, pixflow.

- Voiceover dulu, baru musik, lalu ambience, terakhir efek.
- Whoosh hanya di titik gerakan; jangan di setiap potongan.
- Satu efek per transisi, dua maksimum.
- Efek harus "quiet enough to be subliminal".
- Tanpa desain bunyi, gerakan di layar terasa kosong.

---

## 3. Yang dibangun sebagai jawaban (`cine.py`, `make_proof.py`)

| Kriteria riset | Implementasi |
|---|---|
| Render native 1080p | 1920×1080, lapis karakter supersample 2× |
| Figur terbaca | 40–52% tinggi frame, proporsi ±7 kepala |
| Siluet + cahaya tepi | badan poligon gelap, rim light dari posisi matahari |
| 4–7 lapis kedalaman | 8 lapis: langit, bukit jauh, kota, tebing, tangga+figur, debu, batu depan, bingkai |
| Parallax terkendali | faktor 0,28→1,30 per kedalaman (bukan 0→2) |
| Bayangan antar-lapis | `drop_shadow` per lapis depan |
| Bayangan kontak | `soft_shadow` di bawah kaki, menempel ke permukaan |
| Depth of field per lapis | 0,8–16 px sesuai kedalaman, tanpa di lapis fokus |
| Kabut atmosferik | campuran warna horizon per kedalaman |
| Tekstur kertas | bintik + serat, dikali luminansi |
| Anticipation | fase 0–22% langkah: badan turun sebelum naik |
| Arcs | kaki mengangkat lewat `sin(πq)`, bukan interpolasi lurus |
| Follow-through | mantel tertinggal, badan tertekan setelah menapak |
| Kamera yang berhenti | zoom berhenti 2,5 dtk terakhir |
| Tanpa teks | nol teks di dalam frame |
| Bunyi | `make_sfx.py`: angin, langkah, denyut di puncak |

---

## 4. Checklist sebelum render (dipakai tiap video)

- [ ] Figur ≥ 38% tinggi frame?
- [ ] Ada teks > 60 px? (kalau ya: hapus, bukan dikecilkan)
- [ ] Minimal 4 lapis kedalaman dengan parallax berbeda?
- [ ] Ada bayangan kontak di setiap objek yang menyentuh permukaan?
- [ ] Lapis jauh lebih pucat/kurang kontras?
- [ ] Ada minimal satu anticipation sebelum aksi utama?
- [ ] Kamera berhenti minimal 1 detik di akhir shot?
- [ ] Setiap shot punya ukuran shot berbeda (wide/medium/close)?
- [ ] Ada lapisan bunyi selain musik?
- [ ] Nol frame identik berurutan (uji diff)?

---

## 5. Sumber

- Satura AI — *How to Make Faceless AI Videos Look Cinematic* (2026)
- Subscribr — *AI Stock Footage That Doesn't Look Cheap* (2025)
- Pixflow — *YouTube Video Retention Editing*
- Overseeros — *YouTube Sound Design: VO, Music & SFX*
- Shortzly — *Short-Form Video Sound Design* (2026)
- Moonb — *What Is 2.5D Animation* (2026)
- Pixeldust — *2.5D Animation Tutorial*
- Premation — *2.5D parallax animation*
- Artemisia College — *Secondary Motion in Animation*
- Shortfilmcentral — *12 Principles of Animation* (2026)
- RMCAD — *Physics for Animators*
- CSC418, University of Toronto — *Fundamental Principles of Animation*
