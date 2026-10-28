# Tropical / Subtropical
### Film narasi tanpa karakter · niche beauty · POV formulasi × iklim

> **Tesis:** produk yang kamu pakai pagi ini kemungkinan dibuat untuk kulit yang hidup di 12 °C. Kamu tinggal di 30 °C dengan kelembapan 80%.

**Film final:** `out/tropical-remotion-COMPLETE.mp4` — dirender penuh oleh **Remotion** (`remotion/`), 3 menit 16 detik · 1080×1920 · 30 fps · −16 LUFS · audio stereo.

> File MP4 berukuran besar **tidak disimpan di git**. Hasil render ada di Drive:
> [`tropical-subtropis-remotion-3m17-1080x1920.mp4`](https://drive.google.com/file/d/1yNZTvviCyy7mDI6M_s2iat_IuLraLlMw/view)
> (folder `movie/tropical-climate`, 38,7 MB). Repo ini hanya berisi kode, aset kecil, dan dokumen.
> Versi Pillow sebelumnya (`out/tropical-subtropis-COMPLETE.mp4`) tetap ada di riwayat commit sebagai arsip.

---

## Kenapa POV ini

Konten kecantikan lokal hampir seluruhnya menjawab **"produk mana"**. Film ini menjawab **"kenapa formulanya bisa salah tempat"** — persinggungan formulasi kosmetik dan klimatologi. Sudut yang jarang diambil karena butuh dua bidang sekaligus: kimia bahan + data iklim.

Tanpa review, tanpa merek, tanpa afiliasi — aman untuk fase uji, tetap punya gigi karena berbasis angka.

Riset lengkap + 13 sumber: [`research.md`](research.md).

---

## Struktur

| Bagian | Isi | Durasi |
|---|---|---|
| **Bumper** | **Remotion** — kartu judul editorial, reskin palet film | 0:05 |
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

### Satu renderer: Remotion

| Bagian | Renderer | Alasan |
|---|---|---|
| **Bumper + 10 adegan (3:17)** | **Remotion 4.0** + Chromium (`remotion/`) | semua teks & diagram vektor/DOM, presisi frame, satu timeline |
| Audio | `audio_build.py` (numpy + ffmpeg) | musik & SFX disintesis sendiri, lalu dimux setelah render |

Versi lama memakai Pillow (`render.py`) untuk 10 adegan — rasterisasi per frame.
Pillow mewarnai teks setelah resize, jadi huruf kehilangan ketajaman. Remotion
menggambar DOM pada ukuran akhir: tidak ada teks yang diskalakan sebagai gambar,
dan karena itu tidak ada lagi kompromi "huruf harus digambar ulang". `render.py`
masih disimpan sebagai acuan copy/layout.

### Chromium: koreksi penting

Sebelumnya saya menyimpulkan Chromium tidak bisa jalan di sandbox ini. **Itu salah.** `@sparticuz/chromium` membawa `libnspr4.so` dan `libnss3.so` di dalam paketnya, tapi hanya mengekstraknya bila mendeteksi Amazon Linux. Di Debian, ekstraksi tidak pernah terjadi.

Perbaikannya: ekstrak `al2023.tar.br` manual → `LD_LIBRARY_PATH=/tmp/al2023/lib`. Setelah itu **Remotion render normal** (150 frame dalam 12,6 detik).

Detail lengkap, termasuk dua jebakan Remotion lain (`--concurrency=2` wajib di 2 vCPU, dan `registerRoot` tidak boleh menerima Fragment): [`chromium-notes.md`](chromium-notes.md).

### Pipeline lengkap

```
riset 13 sumber → narasi 10 segmen → TTS per segmen (durasi presisi)
        ↓
8 gambar AI 9:16 → Remotion (bumper + 10 adegan, DOM/SVG) → MP4 senyap
        ↓                                    ↓
   audio_build.py (musik + SFX + ducking)  ─┘ → mux → MP4 final
```

### Jalankan ulang

```bash
npm --prefix remotion install
# Chromium: lihat remotion/README.md §2 (ekstrak al2023.tar.br)
LD_LIBRARY_PATH=/tmp/al2023/lib npx --prefix remotion remotion render \
  remotion/src/index.ts TropicalFilm remotion/out/film-silent.mp4 \
  --browser-executable=/tmp/chromium --concurrency=2 --muted --crf=20

python3 audio_build.py       # → build/mix.wav (musik + narasi + SFX)
# mux: lihat remotion/README.md §5
```

Detail perintah, tabel durasi per adegan, dan catatan jebakan Remotion:
[`remotion/README.md`](remotion/README.md).

---

## Struktur file

```
projects/tropical-climate/
├── research.md          # 13 sumber: WHO TRS 953, ICH Q1A(R2), iklim Jakarta, sains humektan
├── shots.md             # pemetaan shot + aturan shotcraft yang dipakai
├── chromium-notes.md    # koreksi Chromium + cara render Remotion
├── remotion/            # renderer aktif: src/film/{Bumper,scenes,Film,atoms,fonts}
├── render.py            # arsip renderer Pillow (acuan copy & layout)
├── audio_build.py       # sintesis musik + SFX + mix
├── assets/              # 8 gambar AI 9:16
├── audio/               # 10 narasi
└── out/                 # film final (di-.gitignore, ada di Drive)
```

---

## Kepatuhan

Tanpa merek, tanpa afiliasi, tanpa klaim khasiat. Tidak ada "menyembuhkan/menghilangkan/memutihkan", tidak ada anjuran obat keras. Label AI tetap wajib saat unggah — lihat [playbook kepatuhan](../../playbook/02-kepatuhan-dan-etika.md).

---

## Yang bisa ditingkatkan berikutnya

1. **Subtitle burned-in** — mayoritas penonton menonton tanpa suara.
2. **Potong 3 klip pendek** 30–45 detik untuk feed.
3. **Versi 16:9** untuk YouTube (cukup tambah composition di `remotion/src/Root.tsx`).
4. **VO bahasa Inggris** + timing yang sama untuk pasar ekspat.
