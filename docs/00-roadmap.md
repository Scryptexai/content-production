# 00 — Roadmap

Empat lapis pekerjaan. M1 selesai; M2 = 35 draf kalender; M2.5 = repositioning editorial
relationship (7 naskah riset primer); M3 = variasi visual.

```
L1  NASKAH        hook → klaim → bukti → konsekuensi → pertanyaan
L2  PRODUKSI      TTS · aset gambar · Remotion · musik
L3  VARIASI       latar bergerak (Blender/FFmpeg), varian hook, format silang
L4  DISTRIBUSI    YT + TikTok + IG via Zernio, approve manual, ukur, ulang
```

---

## 1. Prinsip yang tidak berubah

1. **Narasi dulu, visual mengikuti.** Setiap kalimat VO punya satu tugas visual.
2. **Satu video, satu ide.** Kalau butuh dua, itu dua video.
3. **Angka harus punya sumber.** Tanpa sumber → bukan klaim, tapi opini; tulis sebagai opini.
4. **Tanpa karakter.** Tidak ada wajah, lipsync, atau "AI influencer". Suara + grafis.
5. **Gaya M1 dipertahankan:** gelap, tenang, tipografi serif besar, satu aksen warna,
   gerak easing lambat (bezier 0.22,1,0.36,1), hold ≥1 detik.

---

## 2. Masalah yang harus dibereskan di M3: latar statis

Keluhan tepat: 10 adegan M1 memakai 8 still dengan Ken Burns 1,02→1,10. Itu gerak,
tapi **teksturnya tidak berubah** — mata menangkap "foto diperbesar", bukan "dunia bergerak".

Tiga tingkat solusi, dari murah ke mahal:

| Tkt | Teknik | Alat | Efek | Biaya render |
|---|---|---|---|---|
| 1 | **Parallax berlapis** — pisahkan subjek/latar, geser beda kecepatan | Remotion (`<Img>` + transform) | kedalaman nyata, bukan zoom | gratis |
| 2 | **Plate bergerak** — 6–10 dtk video loop latar (asap, air, kain, cahaya) | **Blender** (EEVEE) → FFmpeg loop | latar benar-benar hidup | 1–3 menit/plate |
| 3 | **Simulasi ringan** — cairan, serbuk, uap, kain tertiup | Blender (Mantaflow/cloth) → FFmpeg | sinematik, tidak bisa dipalsukan still | 10–40 menit/plate |

Rencana M3: 8 plate (satu per tema: kulit makro, jendela dingin, jendela tropis,
tetes gliserin, petrolatum, panas mobil, UV, botol serum) × 2 lapis parallax.
Plate dibuat sekali, dipakai berulang → biaya turun per video.

### Resep Blender → plate (target: 6 detik, 1080×1920, 30 fps, loopable)

```bash
# render EEVEE, tanpa audio, PNG seq → FFmpeg jadi mp4 loop
blender -b scene.blend -E BLENDER_EEVEE_NEXT -o /tmp/plate_#### -F PNG -x 1 -a
ffmpeg -y -framerate 30 -i /tmp/plate_%04d.png -vf "scale=1080:1920:flags=lanczos" \
  -c:v libx264 -crf 18 -pix_fmt yuv420p -movflags +faststart plate-06s.mp4
# loop mulus: potong 2 frame terakhir, crossfade 12 frame diRemotion (<Loop>)
```

Aturan plate: **tanpa objek tajam** (blur 2–6 px), **tanpa teks**, kontras rendah,
supaya teks di atasnya tetap juara. Semua plate masuk `assets/plates/` (<5 MB/file).

---

## 3. Variasi: supaya 35 video tidak terasa satu video

Tiga sumbu variasi yang murah dan terbukti:

| Sumbu | Nilai | Dipakai untuk |
|---|---|---|
| **Format grafis** | kinetic type · diagram · angka besar · kartu data · grafik waktu | rotasi per konten |
| **Warna aksen** | terra (bahaya/panas) · teal (aman/sejuk) · gold (angka) | makna, bukan dekorasi |
| **Irama** | 3 potongan (hook cepat) · 6 potongan (cerita) · 1 take (kontemplatif) | sesuai topik |

Ditambah: **3 varian hook** untuk 5 konten teratas tiap minggu (A/B di TikTok;
YT pakai "Test & Compare" thumbnail/judul). Catat di `content/experiments.md`.

---

## 4. Aturan latar bergerak (mulai berlaku sejak konten #1)

1. Setiap adegan punya ≥1 gerak: plate, parallax, atau pan.
2. Tidak ada dua adegan berurutan dengan gerak searah — selang-seling.
3. Latar bergerak ≤ 20% kontras teks; kalau ganggu, turunkan opacity plate.
4. Gerak berhenti (hold) minimal 1 detik di setiap klaim utama.
5. Tidak ada zoom > 1,15 — di layar HP terasa "gelisah".

---

## 5. Siklus uji 30 hari (M3)

```
Minggu 1–2 : 35 konten, 5/hari, jadwal tetap (lihat §6)
Minggu 3   : gandakan format yang menang; matikan yang <50% median retensi 3 dtk
Minggu 4   : 3 seri baru dari pemenang + 1 eksperimen liar (format asing)
```

Metrik yang dipakai (bukan vanity): **retensi 3 detik**, **watch-through %**,
**simpan per 1.000 tayangan**, **follow per 1.000 tayangan**. Likes tidak dipakai
sebagai keputusan.

---

## 6. Jam posting (WIB) — 5 slot

| Slot | Jam | Isi | Alasan |
|---|---|---|---|
| 1 | 06:30 | beauty — pagi, rutin | orang buka HP sebelum aktivitas |
| 2 | 11:45 | relationship — jam makan siang | konsumsi "pikiran" lebih tinggi |
| 3 | 16:30 | beauty — sore | pulang kerja/sekolah |
| 4 | 20:00 | relationship — prime time | waktu tenang, komentar panjang |
| 5 | 21:30 | beauty — malam | ritual malam, simpan tinggi |

Semua jadwal disimpan sebagai UTC di `automation/zernio/content/calendar.json`
(WIB = UTC+7).

---

## 7. Slate v2 — relationship (mulai 2026-11-09)

Bagian relationship tidak lagi ditulis dengan standar "2 konten/hari, sudut psikologi
pasangan". Sejak 9 November, laju turun jadi **1 naskah/hari, 3 platform/jam berbeda**,
dengan syarat: sumber primer, fact ledger berlabel, minimal satu baris `TIDAK-DIKETAHUI`,
dan struktur naratif yang tidak berulang.

| Bergeser dari | Menjadi |
|---|---|
| 2 konten relationship/hari | 1 naskah/hari, riset per topik |
| sudut psikologi pasangan | spektrum A–I: kerja, institusi, masyarakat, alam, teknologi, ekonomi |
| "5 tanda…" | mekanisme + bukti + batas data |
| penutup berisi pelajaran | penutup berupa pertanyaan terbuka |
| caption sama di 3 platform | caption diadaptasi per platform, jam tayang berbeda |

Aturan tulis: `docs/05-editorial-bible.md`. Indeks & jadwal: `content/relationship/README.md`.
QC: `python3 automation/validate_pieces.py`.

**Keputusan terbuka:** 14 naskah relationship lama di minggu 1 (2–8 Nov) masih memakai
standar lama. Pilihannya mengosongkan slot itu, atau menjalankannya sebagai arsip dengan
catatan bahwa standar baru berlaku mulai 9 Nov.
