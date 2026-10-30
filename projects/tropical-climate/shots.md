# Pemetaan shot — dari video-shotcraft ke film ini

Tool yang dipakai: **[video-shotcraft](https://github.com/Vincentwei1021/video-shotcraft)** (Apache-2.0) — 124 kartu resep gerak / 150 shot, dibangun untuk Remotion.

## Apa yang bisa dan tidak bisa saya ambil

Repo itu adalah **skill** untuk Claude Code / Codex: ia mengajari agen memilih *shot recipe* lalu menulis komponen React, merender dengan **Remotion** (butuh Chromium).

Di lingkungan ini Chromium **tidak bisa dijalankan** — sudah diuji: `@sparticuz/chromium` gagal dengan `libnspr4.so: cannot open shared object file`; Debian tanpa `libnss3`/`libnspr4`, `apt` diblokir, tidak ada root, dan tidak ada paket npm yang menyediakan pustaka sistem itu. Remotion juga mengunduh Chrome dari `storage.googleapis.com` yang diblokir.

**Yang saya ambil: tata bahasa geraknya**, lalu saya implementasikan ulang dengan renderer yang terbukti jalan (Pillow + ffmpeg). Jadi hasilnya bukan render Remotion, tapi mengikuti aturan gerak dan ritme tool tersebut.

---

## Aturan shotcraft yang diterapkan

| Aturan (dari `references/aesthetic-rules.md`) | Penerapan di film ini |
|---|---|
| **R1** — info penting harus "bernapas" ≥1 detik sebelum cut | Setiap angka/kartu ditahan; scene 01 menahan "12°C" 3 detik penuh |
| **R2** — kecepatan dari akselerasi, bukan linear | Ken Burns pakai `ease_in_out`; kartu masuk pakai `ease_out` |
| **R3** — ritme lebih baik lambat; aksi utama ≥3 detik | Tidak ada gerakan <0,3 detik; diagram muncul 0,7–0,9 detik |
| **Q-class** — tidak ada zoom yang membuat teks tajam jadi kabur | Teks digambar **setelah** crop-resize, di resolusi penuh 1080×1920 |
| **P-class** — QC tiap shot, bukan di akhir | Setiap scene di-render lalu diambil 3–4 frame untuk diperiksa |

---

## Peta shot

| # | Adegan | Shot grammar | Motion | Durasi |
|---|---|---|---|---|
| 01 | Hook dingin | *cold open* + *hard cut* | Ken Burns dua arah, cut di 8,0 s (tepat setelah "kamu tinggal di Jakarta") | 15,4 s |
| 02 | Data iklim | **data viz** / *stat stack* | Tiga baris angka masuk berurutan, aturan tipografi 30 px | 14,4 s |
| 03 | Frame | *text-as-mask* versi tipografi | Kata muncul satu per satu, *rule* tumbuh dari tengah | 10,8 s |
| 04 | Humektan | *specimen card* | Label → judul → sub → kunci, masing-masing dengan jeda | 12,9 s |
| 05 | Diagram humektan | **diagram / split panel** | Dua panel tumbuh, panah bergerak naik & turun | 20,1 s |
| 06 | Oklusif | *layer stack* | Lapisan menutup, panah keringat naik tapi tertahan | 25,0 s |
| 07 | Panas | **chart reveal** (eksponensial) + bar komparasi | Kurva digambar per titik, bar zona II vs IVb | 30,2 s |
| 08 | UV | **gauge / arc meter** | Jarum busur 180→360°, angka "11" menahan | 20,5 s |
| 09 | Solusi | *numbered list* | 3 blok masuk, garis bawah tumbuh per blok | 31,0 s |
| 10 | Penutup | *end card* + kredit sumber | Dua baris judul, CTA, sumber | 11,6 s |

Total ≈ **192 detik (3:12)**.

---

## Perbedaan penting dari tool aslinya

| | video-shotcraft | Film ini |
|---|---|---|
| Renderer | Remotion + Chromium | Pillow (raster) + ffmpeg |
| Sumber visual | screenshot halaman web nyata | foto AI-generated 9:16 |
| Gerak | 2.5D camera, shader, 3D | Ken Burns 2D + motion graphic 2D |
| Kelebihan | presisi vektor, teks tetap tajam saat zoom | bisa jalan tanpa Chromium, cepat (~40 s/scene) |
| Kekurangan | butuh browser + Node | tidak ada 3D/parallax nyata |

**Kalau Anda ingin hasil Remotion asli** (teks vektor, parallax 2.5D, kamera 3D): jalankan di mesin yang punya Chromium — `cd video-shotcraft/template && npm i && npx remotion render`. Aset dan storyboard di project ini bisa langsung dipakai sebagai bahan.
