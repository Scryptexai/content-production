# Kajian: `lcy362/agnes-video-generator`

Dipelajari 29 Okt 2026. Commit yang diperiksa: `HEAD` saat kloning (depth 1).
Repo 125 MB, **52.540 baris Python**, MIT, 7 pipeline video.

---

## 1. Apa ini sebenarnya

Bukan generator. Ini **orkestrator** — 52 ribu baris kode yang membungkus API
video milik Agnes AI (`apihub.agnes-ai.com`). Semua render terjadi di cloud
mereka (ComfyUI di belakang gateway new-api). Laptop cuma menjalankan FastAPI.

Yang dikerjakan repo ini, dan itu bagian yang sulit:

| Lapisan | Isi |
|---|---|
| Prompt | `core/screenwriter/` — 2.125 baris prompt LLM untuk cerita → adegan → shot |
| API | `core/api/` — multi-key, rate limiter, retry 2 rel, error collector |
| Pipeline | 7 jenis: creative, manuscript, anchor, poetry, simple, ... |
| Audio | `edge_tts` (Azure, gratis tanpa key) + tashkeel Arab + estimasi kecepatan |
| Subtitle | `srt` + moviepy TextClip, bidi untuk Arab |
| Compositing | moviepy: concat, audio overlay, watermark, freeze frame |

## 2. Batas keras — ini yang menentukan

| Hal | Nilai | Konsekuensi untuk kita |
|---|---|---|
| Butuh API key | Ya, dari `platform.agnes-ai.com` | Tidak bisa dipakai tanpa akun |
| Model gratis | `agnes-video-2.5-flash`, **720P tetap** | Kurang untuk YouTube 1080p |
| Durasi per klip | **4–12 dtk** | 3 menit = 15–18 klip |
| Model bayar | 2.5: 720P $0.025/s · 960P $0.040/s · 2K $0.055/s | 2K 3 menit ≈ $9,9/video |
| Batas inferensi | ~15 menit per task, lalu gagal | Sebagian task hangus |
| **Jaringan dari sandbox ini** | **TLS diblokir** | **Tidak bisa dijalankan di sini** |

Bukti blokir (bukan asumsi):

```
$ curl -sv https://apihub.agnes-ai.com/v1/models
* Connected to apihub.agnes-ai.com (104.18.19.62) port 443
* TLSv1.3 (OUT), TLS handshake, Client hello (1):
* OpenSSL SSL_connect: SSL_ERROR_SYSCALL
HTTP=000
```

TCP tembus, TLS dihentikan proxy. Artinya: kode bisa saya baca, tapi **tidak
bisa saya render satu frame pun** lewat tool ini.

## 3. Tiga teknik yang layak dicolong

### 3.1 Rantai keyframe — ini yang paling berharga

Inti `core/pipelines/creative/steps_video.py`:

> **frame terakhir scene N dijadikan frame pertama scene N+1**

```python
current_first_frame = end_frame_path   # dipakai sebagai input scene berikutnya
```

Efeknya: tiap potongan menyambung secara visual, dan boleh dipotong **di tengah
gerakan**. Ini menyelesaikan masalah yang saya catat di v4: "kamera per blok
tidak sinambung, ada potongan halus di batas blok". Solusinya bukan kamera yang
lebih halus, tapi **keyframe yang dibagi antar-shot**.

### 3.2 Keyframe statis, gerak terpisah

`design_shots_for_scene()` memaksa model mengisi lima medan terpisah:

| Medan | Aturan |
|---|---|
| `ff_desc` | frame pertama — **dilarang pakai kata gerak** |
| `lf_desc` | frame terakhir — **dilarang pakai kata gerak** |
| `motion_desc` | gerak antar-dua-frame itu saja |
| `visual_desc` | deskripsi keseluruhan |
| `variation_type` | `large` / `medium` / `small` |

Pemisahan ini memaksa penulis memikirkan **dua pose konkret** dan apa yang
terjadi di antaranya. Itu pose-to-pose, prinsip animasi nomor 4, dan persis
yang hilang dari renderer saya: saya menggerakkan fungsi sinus terus-menerus,
bukan menuju pose yang ditentukan.

### 3.3 `variation_type` = aturan seleksi shot

Tiga tingkat perubahan: `large` (ganti tempat), `medium` (elemen baru masuk),
`small` (gerak kecil). Ini memberi alasan eksplisit untuk **tidak memotong
dengan cara yang sama dua kali** — kritik "motion grammar yang itu-itu saja"
dari riset v5.

## 4. Putusan

**Untuk produksi kita sekarang: tidak dipakai.** Tiga alasan, berurutan:

1. **Tidak bisa jalan di sini** — TLS diblokir. Butuh mesin Anda + key.
2. **720P gratis** terlalu rendah untuk long-form YouTube. Naik ke 960P/2K
   berarti bayar per detik, dan itu biaya yang tumbuh linear dengan target
   3 video/hari.
3. **Konsistensi karakter** masih jadi masalah terbuka di model i2v. Untuk
   seri yang butuh tokoh sama di 20 video, rantai keyframe menahan *kontinuitas
   antar-shot*, bukan *identitas antar-video*.

**Yang saya ambil sekarang:** §3.1, §3.2, §3.3 — ketiganya bisa diterapkan ke
renderer sendiri tanpa API, tanpa biaya, dan tanpa kehilangan 1080p.

**Kapan tool ini masuk akal:** kalau kita mau pivot ke stock-footage AI-generated
(realistis, bukan papercut), atau untuk short-form TikTok/IG yang 720p sudah
cukup. Itu keputusan terpisah, dan butuh key Anda.

## 5. Kalau Anda mau mencobanya

Di mesin Anda, bukan sandbox:

```bash
git clone https://github.com/lcy362/agnes-video-generator.git
cd agnes-video-generator
cp .env.example .env        # isi AGNES_API_KEY dari platform.agnes-ai.com
./start.sh                  # → http://localhost:8765
```

Pilih pipeline **Manuscript** (tempel naskah) atau **Creative** (dari ide).
Model: `agnes-video-2.5-flash` (gratis, 720P, 4–12 dtk/klip).

Saran saya: coba satu blok 30 detik dulu, lalu nilainya dibandingkan dengan
renderer kita di resolusi sama. Jangan langsung 3 menit.
