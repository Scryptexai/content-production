# Tropical / Subtropical
### Film narasi tanpa karakter · niche beauty · POV formulasi × iklim

> **Tesis:** produk yang kamu pakai pagi ini kemungkinan dibuat untuk kulit yang hidup di 12 °C. Kamu tinggal di 30 °C dengan kelembapan 80%.

**Film final:** [`out/tropical-subtropis-COMPLETE.mp4`](out/tropical-subtropis-COMPLETE.mp4)
**Durasi:** 3 menit 16 detik · 1080×1920 · 30 fps · -16 LUFS · audio stereo

---

## Kenapa POV ini

Konten kecantikan lokal hampir seluruhnya menjawab **"produk mana"**. Film ini menjawab **"kenapa formulanya bisa salah tempat"** — persinggungan formulasi kosmetik dan klimatologi. Sudut yang jarang diambil karena butuh dua bidang sekaligus: kimia bahan + data iklim.

Tanpa review, tanpa merek, tanpa afiliasi — aman untuk fase uji, tetap punya gigi karena berbasis angka.

Riset lengkap + 13 sumber: [`research.md`](research.md).

---

## Struktur

| Bagian | Isi | Durasi |
|---|---|---|
| **Bumper** | **Remotion** — `PaperTitleCard` dari video-shotcraft, di-reskin | 0:05 |
| 01 Cold open | 12 °C Eropa → *hard cut* Jakarta | 0:15 |
| 02 Data | 27–30 °C · 74–84% RH · UV 11 | 0:14 |
| 03 Frame | "Bukan detail kecil. Dua lingkungan, dua kimia." | 0:11 |
| 04 Bahan 01 | Humektan: gliserin, HA — "menarik air, dari mana?" | 0:13 |
| 05 Diagram | Lembap 80% vs kering 40%: arah air berlawanan | 0:20 |
| 06 Bahan 02 | Oklusif: selimut → rumah kaca, keringat terperangkap | 0:25 |
| 07 Panas | ×2 laju reaksi per +10 °C; zona II vs IVb | 0:30 |
| 08 UV | Gauge indeks 11; SPF≠UVA; PA++++ syarat minimum | 0:21 |
| 09 Solusi | 3 perubahan: tekstur, urutan, penyimpanan | 0:31 |
| 10 Penutup | "Kulit tropis. Formula tropis." + CTA + sumber | 0:12 |

---

## Audio

Musik dan sound design **disintesis sendiri** (`audio_build.py`) — tidak ada aset pihak ketiga, jadi aman untuk komersial:

- **Ambient bed** — drone + pad akor per adegan (A minor, resolusi akhir ke tonik), crossfade equal-power 1,4 detik
- **Sub pulse** — detak 55 Hz tiap 2,4 detik
- **Whoosh** — noise band-pass sweep di setiap batas adegan
- **Impact** — sub drop + klik di 4 titik reveal
- **Riser** — noise naik 4 detik sebelum dua puncak

Mix: narasi di atas, musik **ducking** via `sidechaincompress` (threshold 0.045, ratio 7), lalu `loudnorm` ke **-16 LUFS / -1,5 dBTP** — standar TikTok/IG/YouTube.

Hasil ukur: **-16.0 LUFS, true peak -1.4 dBTP, LRA 2.2 LU**.

---

## Teknis

### Dua renderer, satu film

| Bagian | Renderer | Alasan |
|---|---|---|
| **Bumper (5 detik)** | **Remotion 4.0** + Chromium — komponen asli video-shotcraft | teks vektor, letterpress animation, presisi frame |
| **10 adegan (3:11)** | **Pillow + ffmpeg** (`render.py`) | motion graphics 2D + data viz; 40–90 detik per adegan |

### Chromium: koreksi penting

Sebelumnya saya menyimpulkan Chromium tidak bisa jalan di sandbox ini. **Itu salah.** `@sparticuz/chromium` membawa `libnspr4.so` dan `libnss3.so` di dalam paketnya, tapi hanya mengekstraknya bila mendeteksi Amazon Linux. Di Debian, ekstraksi tidak pernah terjadi.

Perbaikannya: ekstrak `al2023.tar.br` manual → `LD_LIBRARY_PATH=/tmp/al2023/lib`. Setelah itu **Remotion render normal** (150 frame dalam 12,6 detik).

Detail lengkap, termasuk dua jebakan Remotion lain (`--concurrency=2` wajib di 2 vCPU, dan `registerRoot` tidak boleh menerima Fragment): [`chromium-notes.md`](chromium-notes.md).

### Pipeline lengkap

```
riset 13 sumber → narasi 10 segmen → TTS per segmen (durasi presisi)
        ↓
8 gambar AI 9:16 → render.py (Pillow motion graphics) → 10 klip
        ↓                                    ↓
   audio_build.py (musik + SFX + ducking)  ─┘
        ↓
   Remotion (bumper) → concat → encode 3 Mbps → MP4
```

### Jalankan ulang

```bash
python3 -m pip install --break-system-packages numpy pillow imageio-ffmpeg
python3 render.py            # 10 adegan
python3 audio_build.py       # musik + mix
# bumper: lihat chromium-notes.md §3
```

---

## Struktur file

```
projects/tropical-climate/
├── research.md          # 13 sumber: WHO TRS 953, ICH Q1A(R2), iklim Jakarta, sains humektan
├── shots.md             # pemetaan shot + aturan shotcraft yang dipakai
├── chromium-notes.md    # koreksi Chromium + cara render Remotion
├── render.py            # 10 adegan (Pillow → ffmpeg)
├── audio_build.py       # sintesis musik + SFX + mix
├── assets/              # 8 gambar AI 9:16
├── audio/               # 10 narasi
└── out/                 # film final
```

---

## Kepatuhan

Tanpa merek, tanpa afiliasi, tanpa klaim khasiat. Tidak ada "menyembuhkan/menghilangkan/memutihkan", tidak ada anjuran obat keras. Label AI tetap wajib saat unggah — lihat [playbook kepatuhan](../../playbook/02-kepatuhan-dan-etika.md).

---

## Yang bisa ditingkatkan berikutnya

1. **Migrasikan 10 adegan ke Remotion** — satu pipeline, dan semua motion graphics jadi vektor (tajam di semua ukuran). Chromium sudah terbukti jalan.
2. **Subtitle burned-in** — mayoritas penonton menonton tanpa suara.
3. **Potong 3 klip pendek** 30–45 detik untuk feed.
4. **Versi 16:9** untuk YouTube.
