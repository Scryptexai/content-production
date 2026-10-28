# Tropical / Subtropical
### Video narasi tanpa karakter · niche beauty · POV formulasi × iklim

> **Tesis:** produk yang kamu pakai pagi ini kemungkinan dibuat untuk kulit yang hidup di 12 °C. Kamu tinggal di 30 °C dengan kelembapan 80%.

**Output:** [`out/tropical-subtropis-web.mp4`](out/tropical-subtropis-web.mp4) — 3 menit 11 detik, 1080×1920, 30 fps, narasi Indonesia, 10 adegan.

---

## Kenapa POV ini

Konten kecantikan lokal hampir seluruhnya menjawab **"produk mana"**. Video ini menjawab **"kenapa formulanya bisa salah tempat"** — persinggungan formulasi kosmetik dan klimatologi. Sudut yang jarang diambil karena butuh dua bidang sekaligus: kimia bahan dan data iklim.

Konsekuensinya: tidak ada review, tidak ada merek, tidak ada afiliasi. Aman untuk fase uji, dan tetap punya gigi karena berbasis angka.

Riset lengkap + 13 sumber: [`research.md`](research.md).

---

## Struktur 10 adegan

| # | Adegan | Isi | Durasi |
|---|---|---|---|
| 01 | Cold open | 12 °C Eropa → *hard cut* Jakarta | 0:15 |
| 02 | Data | 27–30 °C · 74–84% RH · UV 11 | 0:14 |
| 03 | Frame | "Bukan detail kecil. Dua lingkungan, dua kimia." | 0:11 |
| 04 | Bahan 01 | Humektan: gliserin, HA — "menarik air, dari mana?" | 0:13 |
| 05 | Diagram | Lembap 80% vs kering 40%: arah air berlawanan | 0:20 |
| 06 | Bahan 02 | Oklusif: selimut → rumah kaca, keringat terperangkap | 0:25 |
| 07 | Panas | ×2 laju reaksi per +10 °C; zona II vs IVb | 0:30 |
| 08 | UV | Gauge indeks 11; SPF≠UVA; PA++++ syarat minimum | 0:21 |
| 09 | Solusi | 3 perubahan: tekstur, urutan, penyimpanan | 0:31 |
| 10 | Penutup | "Kulit tropis. Formula tropis." + CTA + sumber | 0:12 |

---

## Cara kerja teknis (dan batasnya)

Tool yang diminta: **[video-shotcraft](https://github.com/Vincentwei1021/video-shotcraft)**. Repo itu adalah *skill* Claude Code/Codex yang mengajari agen memilih **124 kartu resep gerak / 150 shot**, lalu menulis komponen React dan merender dengan **Remotion** — yang butuh Chromium.

**Chromium tidak bisa dijalankan di lingkungan ini.** Sudah diuji dan gagal dengan bukti:
`@sparticuz/chromium` → `libnspr4.so: cannot open shared object file`; Debian tanpa `libnss3`/`libnspr4`; `apt` diblokir; tidak ada root; tidak ada paket npm yang menyediakan pustaka sistem tersebut; Remotion juga mengunduh Chrome dari `storage.googleapis.com` yang diblokir.

**Yang saya ambil dari tool itu: tata bahasa geraknya.** Aturan yang diterapkan (dari `references/aesthetic-rules.md`):

- **R1** — info penting ditahan ≥1 detik sebelum cut (kartu "12 °C" ditahan 3 detik)
- **R2** — kecepatan dari akselerasi, bukan linear (semua easing, bukan lerp)
- **R3** — ritme lebih baik lambat; tidak ada gerakan <0,3 detik
- **Q-class** — teks digambar **setelah** crop-resize, di resolusi penuh, jadi tidak ikut kabur saat zoom
- **P-class** — QC per shot: tiap adegan di-render, diambil 3–4 frame, diperiksa, lalu diperbaiki

Detail pemetaan shot per shot: [`shots.md`](shots.md).

---

## Pipeline

```
riset (13 sumber)  →  narasi 10 segmen  →  TTS per segmen (durasi presisi)
        ↓
10 gambar AI 9:16  →  render.py (Pillow, motion graphics)  →  10 klip + audio
        ↓
ffmpeg concat  →  encode final (3 Mbps, faststart)  →  MP4
```

`render.py` menghasilkan tiap frame dengan Pillow, lalu menyambung audio per segmen dengan *silence* pengisi supaya narasi tidak bertabrakan di batas adegan. Waktu render: ~40 detik per adegan di 2 vCPU.

**Jalankan ulang:**
```bash
python3 -m pip install --break-system-packages imageio-ffmpeg pillow
python3 render.py          # semua 10 adegan
python3 render.py 4 6      # adegan tertentu saja
```

---

## Struktur file

```
projects/tropical-climate/
├── research.md          # 13 sumber: WHO TRS 953, ICH Q1A(R2), iklim Jakarta, sains humektan
├── shots.md             # pemetaan shot + aturan shotcraft yang dipakai
├── render.py            # renderer 10 adegan (Pillow → ffmpeg)
├── assets/              # 8 gambar AI 9:16
├── audio/               # 10 narasi (vo-01..vo-10)
└── out/                 # film final
```

---

## Batas kepatuhan

- Tanpa merek, tanpa afiliasi, tanpa klaim khasiat.
- Tidak ada klaim "menyembuhkan/menghilangkan/memutihkan".
- Tidak ada anjuran obat keras — selalu "konsultasi dokter".
- Tetap perlu label AI pada saat unggah, sesuai [playbook kepatuhan](../../playbook/02-kepatuhan-dan-etika.md).

---

## Yang masih bisa ditingkatkan

1. **Musik latar** — film ini tanpa BGM; sengaja, supaya narasi diuji dulu. Tambahkan setelah struktur disetujui.
2. **Bumper 3 detik** untuk pembuka feed & *hook* versi 15 detik.
3. **Subtitle burned-in** untuk penonton yang menonton tanpa suara (mayoritas di TikTok).
4. **Versi 16:9** — layout sudah aman untuk reframe, tapi perlu komposisi ulang.
5. **Render Remotion asli** — kalau Anda punya Chromium, `shots.md` bisa langsung dipakai sebagai spesifikasi.
