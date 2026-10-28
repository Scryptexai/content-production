# Beauty AI Influencer — Character Bible

Empat karakter AI untuk ceruk *beauty* Indonesia. Bukan empat variasi dari wajah yang sama — empat **model bisnis** yang berbeda: beda audiens, beda bahasa, beda cara menghasilkan uang, beda risiko.

> Status: **v1 draft**, siap dipakai untuk produksi konten & pitching brand.
> Yang masih perlu divalidasi sebelum launch: ketersediaan handle, review legal untuk klaim, dan training LoRA (lihat [`playbook/01-produksi-ai.md`](playbook/01-produksi-ai.md)).

---

## Daftar isi

| File | Isi |
|---|---|
| [`characters/01-kirana-adisurya.md`](characters/01-kirana-adisurya.md) | **Kirana** — Sang Peracik. Formulator yang membedah INCI & menghitung harga wajar. |
| [`characters/02-sekar-ayu.md`](characters/02-sekar-ayu.md) | **Sekar** — Sang Kanvas. Wajah sebagai karya seni; *look* yang mustahil ada di dunia nyata. |
| [`characters/03-ratna-kusumawardhani.md`](characters/03-ratna-kusumawardhani.md) | **Ratna** — Musim Kedua. Kulit 40+, melasma, menopause, dan harga diri. |
| [`characters/04-alya-nur-ramadhani.md`](characters/04-alya-nur-ramadhani.md) | **Alya** — Kak Alya. Mantan *beauty advisor* yang sekarang jujur soal komisi. |
| [`playbook/01-produksi-ai.md`](playbook/01-produksi-ai.md) | Master prompt, identity lock, LoRA, QC 12 poin, *voice design*. |
| [`playbook/02-kepatuhan-dan-etika.md`](playbook/02-kepatuhan-dan-etika.md) | Label AI (IG, TikTok, Permendag 19/2026), klaim BPOM, aturan "no fake before-after". |
| [`playbook/03-rencana-90-hari.md`](playbook/03-rencana-90-hari.md) | Kalender launch, KPI, rate card, urutan monetisasi. |
| [`strategy/01-strategi-tercepat.md`](strategy/01-strategi-tercepat.md) | **Keputusan: jalur pendapatan tercepat & paling efisien** + desain fase uji 10 konten. |
| [`playbook/04-tools-video-avatar.md`](playbook/04-tools-video-avatar.md) | **Tool untuk karakter yang benar-benar "hidup"** — perbandingan MuseTalk/LatentSync/SadTalker, lisensi, VRAM, runbook GPU. |
| [`scripts/alya-01-storyboard.md`](scripts/alya-01-storyboard.md) | **Storyboard 7 adegan** Skrip 01 — framing, gerak kamera, aksi, teks, catatan lipsync. |
| [`video/alya-01-shade-paling-gelap.mp4`](video/alya-01-shade-paling-gelap.mp4) | Video 71 detik 1080×1920 — animatic (still + gerak kamera + audio + subtitle). |
| [`scripts/alya-01-10.md`](scripts/alya-01-10.md) | **10 skrip video siap produksi** untuk Alya — hook, intonasi, teks layar, closing. |
| [`scripts/alya-01-preview.html`](scripts/alya-01-preview.html) | **Preview sinkron** skrip 01: audio + subtitle + timeline adegan. |
| [`audio/`](audio/) | Take audio terpilih (Skrip 01, 71 detik). |
| [`assets/frames/`](assets/frames/) | Frame pembuka vertikal 9:16 untuk Skrip 01. |
| [`data/characters.json`](data/characters.json) | Versi mesin dari keempat profil (untuk pipeline konten). |
| [`index.html`](index.html) | Brand book visual — buka di browser. |
| `assets/characters/*.jpg` | Foto referensi tiap karakter (AI-generated, 896×1200). |
| `assets/scene/` | 7 shot *Alya* + audio per adegan + `manifest.json` — input pipeline lipsync. |
| `assets/scene/audio/` | Audio dipotong per adegan (siap untuk SadTalker / MuseTalk). |

---

## Proyek aktif: video narasi tanpa karakter

| File | Isi |
|---|---|
| [`projects/tropical-climate/`](projects/tropical-climate/) | **"Kulit Tropis, Formula Subtropis"** — video 3:11, 10 adegan, narasi saja, tanpa karakter. |
| [`projects/tropical-climate/research.md`](projects/tropical-climate/research.md) | Riset 13 sumber: zona iklim IVb, sains humektan/oklusif, UV, stabilitas panas. |
| [`projects/tropical-climate/shots.md`](projects/tropical-climate/shots.md) | Pemetaan shot dari video-shotcraft + aturan gerak yang diterapkan. |
| [`projects/tropical-climate/out/tropical-subtropis-COMPLETE.mp4`](projects/tropical-climate/out/tropical-subtropis-COMPLETE.mp4) | Film final 3:16 — bumper Remotion + 10 adegan + musik + sound design. |
| [`projects/tropical-climate/chromium-notes.md`](projects/tropical-climate/chromium-notes.md) | Koreksi: Chromium **bisa** jalan; cara render Remotion di sandbox ini. |
| [`projects/tropical-climate/audio_build.py`](projects/tropical-climate/audio_build.py) | Sintesis musik + SFX, ducking, loudnorm -16 LUFS. |

> **Koreksi penting:** saya sempat menyimpulkan Chromium tidak bisa jalan di sini. **Itu salah.** `@sparticuz/chromium` membawa `libnspr4.so`/`libnss3.so` di dalam paketnya, hanya saja tidak diekstrak di Debian. Setelah diekstrak manual + `LD_LIBRARY_PATH`, **Remotion render normal** — bumper film ini dibuat dengan komponen asli `PaperTitleCard` dari video-shotcraft. Detail: [`chromium-notes.md`](projects/tropical-climate/chromium-notes.md).

---

## Matriks pembeda

Ini bagian terpenting. Empat karakter ini dirancang supaya **tidak saling memakan audiens**.

| | **Kirana** | **Sekar** | **Ratna** | **Alya** |
|---|---|---|---|---|
| **Arketipe** | The Sage | The Creator | The Caregiver | The Confidante |
| **Usia** | 27 | 24 | 52 | 29 |
| **Kota** | Bandung | Yogyakarta | Surabaya | Jakarta (tinggal Depok) |
| **Latar** | Sarjana farmasi, 3 tahun di pabrik maklon | Putus studi DKV, asisten MUA pengantin | 24 tahun di bank, pensiun dini | 6 tahun *beauty advisor*, supervisor counter |
| **Wajah** | Bulat, kantung mata dibiarkan, bob pendek, kacamata | Buzz cut platinum-lilac, kulit cokelat tua, freckles, tato bintang | Rahang lembut, garis tawa, melasma tidak di-retouch, rambut perak | Wajah bulat, lesung pipi, hijab dusty rose, plus-size |
| **Nada bicara** | Datar, angka, memotong | Puitis, pendek, *lowercase* | Lambat, hangat, "Ning" | Ceplas-ceplos Jakarta, "jujurly" |
| **Sub-niche** | Formulasi & harga | Art makeup & AR | Kulit matang 40+ | Shade match & modest beauty |
| **Audiens inti** | 20–34, skeptis, campur pria | 16–26, seni & drag | 42–60 (+ anak yang beli untuk ibu) | 22–38, Muslim, budget-conscious |
| **Platform utama** | TikTok → YouTube | Instagram + Pinterest | Instagram + Facebook + YouTube | TikTok Shop + IG Live |
| **Format andalan** | Bedah INCI 60 detik | Satu Wajah, Lima Gerakan | 5 Menit untuk Kulit 50+ | Tes 12 Jam |
| **USP** | Menghitung harga formula, bukan memuji tekstur | Wajah yang mustahil ada — dan bisa disewa | Tidak menjual kerinduan pada usia 20 | Dulu dibayar untuk menjual, sekarang dibayar untuk jujur |
| **Pendapatan** | Audit formula B2B, kursus | Kampanye visual, AR, drops | Komunitas berbayar, AOV tinggi | Affiliate + live shopping |
| **Kecepatan cuan** | Lambat (3–6 bln) | Sedang (2–4 bln) | Sedang (2–3 bln) | Cepat (30–60 hari) |
| **Pertahanan (moat)** | Tinggi — butuh keahlian nyata | Tinggi — butuh *craft* visual | Sedang — kompetisi rendah | Sedang — mudah ditiru |
| **Risiko utama** | Terlalu teknis, reach kecil | Konversi rendah, isu AI vs MUA | Dianggap "tidak seksi" | Konflik dengan brand |

---

## Cara memilih (pendapat, bukan menu)

Kalau harus memulai dengan **satu** karakter:

1. **Butuh pendapatan dalam 60 hari** → **Alya**. Affiliate TikTok Shop paling cepat menghasilkan, dan cerita "mantan BA yang buka suara" langsung dipahami audiens.
2. **Ingin aset yang sulit ditiru** → **Kirana**. Setiap video butuh pengetahuan formulasi nyata; pesaing tidak bisa menyalin dengan ganti prompt.
3. **Ingin kompetisi paling sepi** → **Ratna**. Segmen 45+ di Indonesia besar, daya beli tinggi, dan hampir tidak ada creator yang konsisten menggarapnya.
4. **Ingin kampanye brand & jangkauan global** → **Sekar**. Paling "AI-native": hanya AI yang bisa melakukan ini, jadi tidak ada isu authenticity.

**Jangan jalankan empat-empatnya sekaligus.** Satu karakter butuh ~15 jam/minggu untuk riset, render, edit, dan komunitas. Rekomendasi: pilih satu sebagai *flagship*, satu sebagai *cadangan* yang diuji dengan 6 konten, lalu hentikan yang kalah.

---

## Prinsip yang berlaku untuk keempatnya

1. **Tidak pernah menyamar sebagai manusia.** Bio dan label platform menyatakan AI. Ini bukan sekadar etika — sejak 31 Agustus 2026 Instagram memotong reach profil AI yang tidak berlabel. Detail di [`playbook/02`](playbook/02-kepatuhan-dan-etika.md).
2. **Tidak ada before-after khasiat skincare.** AI bisa memfabrikasi hasil; karena itu *before-after* hanya dipakai untuk makeup (hasil yang bisa diverifikasi dalam satu duduk), tidak pernah untuk klaim khasiat.
3. **Tidak ada klaim medis.** Kosmetik bukan obat. Tretinoin, hidrokuinon, dan sejenisnya hanya disebut sebagai "harus lewat dokter".
4. **Manusia tetap di dalam loop.** Setiap naskah yang menyebut bahan aktif, angka, atau klaim di-review manusia sebelum tayang.
