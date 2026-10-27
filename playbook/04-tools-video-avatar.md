# 04 — Tool untuk karakter yang benar-benar "hidup"

Dokumen ini menjawab satu pertanyaan: **tool apa yang dipakai supaya Alya benar-benar berbicara di depan kamera, bukan sekadar still yang di-zoom.**

Jawaban singkat: **tidak ada tool di lingkungan kerja ini yang bisa melakukannya.** Bukan karena kurang mencari — ada tiga tembok keras, dan sudah saya uji. Sisanya adalah jalur yang bisa Anda jalankan sendiri hari ini.

---

## 1. Bukti: kenapa tidak bisa di sini

Hasil pengujian langsung di sandbox ini:

| Yang dibutuhkan | Hasil uji | Konsekuensi |
|---|---|---|
| GPU CUDA | `nvidia-smi` tidak ada, `/dev/nvidia*` kosong | Semua model di bawah butuh 4–18 GB VRAM |
| CPU / RAM | **2 vCPU, 3 GB RAM** | Inference difusi akan OOM sebelum frame pertama |
| Model weights (HuggingFace) | `huggingface.co` → **000 (diblokir)** | MuseTalk, LatentSync, LivePortrait, SadTalker semua ambil bobot dari sini |
| `raw.githubusercontent.com` | **000 (diblokir)** | Tidak bisa ambil skrip instalasi |
| GitHub release assets | `objects.githubusercontent.com` → **000** | Checkpoint `.pth/.safetensors` tidak bisa diunduh |

Yang **bisa** diakses: `pypi.org`, `files.pythonhosted.org`, `github.com` (halaman web & API saja). Artinya: paket Python bisa dipasang, **tapi bobot modelnya tidak bisa diambil.** Tanpa bobot, MuseTalk hanyalah kode kosong.

Jadi video 71 detik yang ada sekarang dibuat dengan **animasi kamera + still** (Ken Burns, *jump cut*, *vignette*, *grain*, subtitle, audio). Itu disebut **animatic** — bukan talking-head. Saya sebut apa adanya daripada menamainya "karakter hidup".

---

## 2. Peta tool (per Oktober 2026)

Ada dua kelas yang sering tertukar. Kesalahan paling umum: memilih MuseTalk untuk foto, padahal MuseTalk butuh **video yang sudah ada**.

**Kelas A — butuh video input.** Ambil video yang sudah ada, ganti gerakan mulut sesuai audio baru.
**Kelas B — butuh satu foto.** Ubah still jadi video bergerak.

| Tool | Kelas | Lisensi komersial | Kualitas | Kecepatan | VRAM | Catatan |
|---|---|---|---|---|---|---|
| **LatentSync 1.6** (ByteDance) | A | ✅ Apache-2.0 | ★★★★★ — gigi, lidah, bibir paling detail | Lambat | ~18 GB | Paling bagus untuk *close-up* hero shot |
| **LatentSync 1.5** | A | ✅ Apache-2.0 | ★★★★ | Sedang | ~8 GB | Versi realistis untuk GPU konsumen |
| **MuseTalk 1.5** (Tencent) | A | ✅ MIT (bobot boleh komersial) | ★★★★ | **Real-time 30fps+** | ~4 GB min | Pilihan untuk volume & *live* |
| **SadTalker** | **B** | ✅ Apache-2.0 | ★★★ | Sedang | ~6 GB | Satu foto + audio → kepala bergerak. Paling praktis untuk kasus kita |
| **LivePortrait** (Kuaishou) | **B** | ✅ MIT | ★★★★ ekspresif | Real-time | ~6 GB | Digerakkan video *driving*, bukan audio langsung |
| **Wav2Lip** | A | ❌ **non-komersial** | ★★ | Cepat | ~2 GB | **Jangan dipakai** untuk merek komersial |
| **Sonic / KeySync / InfiniteTalk / LTX LipDub** | A/B | campur | ★★★★ | Berat | 16 GB+ | Gelombang baru; ekosistem belum stabil |
| **Duix-Avatar** | B | ✅ open source | ★★★ | Sedang | 12 GB | Ada GUI, cocok kalau tidak nyaman CLI |

Untuk kebutuhan Alya — yang **hanya punya still** — jalurnya:

```
foto (LoRA, sudah ada)
   → SadTalker            : still + audio → video kepala bergerak
   → LatentSync 1.5       : refine area mulut 512px
   → pipeline ffmpeg      : subtitle, teks, grade, mux   ← sudah jadi di repo ini
```

---

## 3. Trik yang mengubah biaya: base video sekali, lipsync berkali-kali

Ini bagian yang paling berdampak dan paling sering dilewatkan.

Jangan render ulang karakter dari nol untuk setiap konten. Buat **satu base video per shot** (5–8 detik, gerakan mikro: bernapas, kedip, sedikit bergeser), lalu pakai tool Kelas A untuk mengganti mulut pada setiap naskah baru. Hasilnya:

| Pendekatan | Waktu GPU per konten 60 dtk | Biaya sewa (A10G) |
|---|---|---|
| Render penuh dari still tiap konten | 40–80 menit | ~$0,20–0,40 |
| Base video + lipsync saja | 6–12 menit | ~$0,05–0,08 |

Untuk 10 konten pertama, bedanya sekitar **$2 vs $0,60** — kecil. Tapi pada konten ke-100, bedanya adalah 40 jam kerja GPU. Karena itu **investasikan sekali di base video yang bagus.**

---

## 4. Runbook: GPU sewa (jalur yang saya rekomendasikan)

Sewa per jam, bukan beli GPU. Harga pasar Oktober 2026: **A10G 24 GB ≈ $0,30–0,72/jam**, T4 16 GB ≈ $0,16–0,30/jam.

**Minggu 1 — sekali saja (2–3 jam, ~$2):**

```bash
# 1. environment
git clone https://github.com/OpenTalker/SadTalker && cd SadTalker
pip install -r requirements.txt

# 2. bobot (di mesin Anda, bukan di sandbox ini)
bash scripts/download_models.sh

# 3. tes satu scene
python inference.py \
  --driven_audio ../assets/scene/audio/scene-01.mp3 \
  --source_image ../assets/scene/alya-shot-01-hook.jpg \
  --result_dir ../out/scene-01 \
  --still --preprocess full --enhancer gfpgan

# 4. refine mulut (opsional, kualitas tertinggi)
#    LatentSync 1.5: butuh 8 GB VRAM
python -m scripts.inference --inference_config configs/latentsync_15.yaml \
  --video_path ../out/scene-01.mp4 \
  --audio_path ../assets/scene/audio/scene-01.mp3
```

**Yang penting:** semua audio per scene **sudah dipotong** di repo ini (`assets/scene/audio/scene-0*.mp3`) dan manifest-nya ada di `assets/scene/manifest.json`. Anda tidak perlu memotong manual.

**Minggu 1 juga — uji kualitas:** bandingkan SadTalker vs MuseTalk pada satu scene yang sama. Kalau MuseTalk menang di wajah Alya (hijab + kulit sawo matang sering jadi kasus sulit), pakai MuseTalk untuk volume.

---

## 5. Kalau tidak mau menyentuh terminal

| Opsi | Biaya | Kelebihan | Kekurangan |
|---|---|---|---|
| **Hugging Face Spaces** (MuseTalk, LatentSync demo) | Gratis / ~$0,60/jam GPU | Tanpa setup, jalan di browser | Antrean, batas durasi, jangan unggah aset komersial ke space publik |
| **Hedra / sync.so / HeyGen** | $20–100/bln | Hasil paling rapi, cepat | Per-menit mahal, kontrol terbatas, data keluar |
| **Google Colab** | Gratis–$10/bln | Notebook siap pakai untuk SadTalker | Sesi putus, GPU tidak dijamin |

**Untuk validasi 10 konten pertama:** Colab + SadTalker gratis sudah cukup untuk menguji apakah wajah Alya "hidup" dengan baik. Jangan bayar apa pun sebelum itu terbukti.

---

## 6. QC khusus lipsync (7 poin)

Berbeda dari QC still. Tambahkan ini ke [`01-produksi-ai.md`](01-produksi-ai.md) §5:

1. **Konsistensi gigi** — gigi tidak boleh berubah jumlah/bentuk antar frame (ciri khas artefak difusi).
2. **Jitter rahang** — rahang tidak boleh bergetar di frame diam.
3. **Artefak tepi hijab** — kain di sekitar dagu sering "meleleh" saat inpainting.
4. **Blink rate** — 15–20 kali/menit. Model sering lupa berkedip; mata kering = tidak manusia.
5. **Kontak mata** — pupil tidak boleh melayang atau berubah ukuran.
6. **Sinkron konsonan bilabial** — m, b, p harus menutup bibir. Ini tes paling cepat untuk lipsync palsu.
7. **Konsistensi warna kulit** — area mulut tidak boleh lebih terang dari pipi.

**Ambang lulus:** dari 71 detik, maksimal 3 detik mengandung artefak yang terlihat. Kalau lebih, turunkan resolusi area wajah atau pakai LatentSync alih-alih MuseTalk.

---

## 7. Rekomendasi akhir

| Kebutuhan Anda | Tool | Alasan |
|---|---|---|
| Validasi cepat, gratis | **SadTalker di Colab** | Satu foto + audio jadi video; cukup untuk membuktikan konsep |
| Produksi rutin 3 video/minggu | **MuseTalk** | 4 GB VRAM, cepat, lisensi MIT komersial |
| Hero shot / konten kampanye | **LatentSync 1.6** | Kualitas mulut tertinggi, 18 GB VRAM |
| Gerakan tubuh & gestur | **LivePortrait** + video *driving* | Satu-satunya yang memberi gestur ekspresif |
| **Jangan** | Wav2Lip | Lisensi non-komersial, kualitas rendah |
| Perakitan akhir | **pipeline ffmpeg repo ini** | Subtitle, grade, teks, mux — sudah teruji |

**Urutan kerja yang saya sarankan:** jangan kejar tool tercanggih dulu. Buktikan dengan SadTalker gratis apakah wajah Alya bisa "hidup" tanpa kehilangan identitasnya. Kalau bisa, baru naik ke MuseTalk untuk volume dan LatentSync untuk konten yang dibayar.

---

### Sumber
- Perbandingan kepraktisan & VRAM MuseTalk/LatentSync/Wav2Lip/SadTalker: [tomodahinata.com](https://tomodahinata.com/en/blog/ai-lip-sync-talking-head-model-selection-guide-2026), [pixazo.ai](https://www.pixazo.ai/blog/best-open-source-ai-lip-sync-models)
- Kebutuhan VRAM LatentSync 1.5 (8 GB) vs 1.6 (18 GB): [github.com/bytedance/LatentSync](https://github.com/bytedance/LatentSync), [sync.so](https://sync.so/blog/what-is-latentsync)
- MuseTalk 4 GB VRAM, 8 detik ≈ 5 menit di laptop: [github.com/TMElyralab/MuseTalk](https://github.com/TMElyralab/MuseTalk)
- Harga sewa GPU: [spheron.network](https://www.spheron.network/blog/self-host-ai-avatar-generator-heygen-alternative-2026)
