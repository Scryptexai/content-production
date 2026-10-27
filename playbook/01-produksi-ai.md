# 01 — Produksi AI: dari prompt ke konten

Dokumen ini menjawab satu pertanyaan: **bagaimana menjaga wajah yang sama selama 200 konten.**

Karakter AI gagal bukan karena prompt pertama jelek — tapi karena *drift* di konten ke-40. Wajahnya melebar, hidungnya berubah, warna kulitnya naik tiga tingkat, dan audiens diam-diam berhenti percaya.

---

## 0. Prinsip dasar

1. **Satu wajah = satu model, bukan satu prompt.** Prompt hanya untuk *look*; identitas dikunci dengan LoRA.
2. **Referensi lebih kuat daripada deskripsi.** Selalu mulai dengan foto referensi (`assets/characters/*.jpg`), bukan teks saja.
3. **Konsistensi mengalahkan keindahan.** Render yang sedikit "kurang cantik" tapi identik lebih bernilai daripada render sempurna yang bukan karakter itu.
4. **Tidak ada retouching wajah.** Yang boleh: warna, kontras, debu sensor, *grain*. Yang tidak boleh: *liquify*, *skin smoothing*, *eye enlargement*.

---

## 1. Alur produksi (7 langkah)

```
[1] Referensi      →  aset dasar karakter (sudah ada di assets/characters/)
[2] Dataset        →  25–40 gambar turunan, variasi angle & cahaya
[3] Training LoRA  →  identity lock (FLUX / SDXL, rank 16–32)
[4] Master prompt  →  template tetap per karakter (di bawah)
[5] Render batch   →  20–40 gambar per sesi
[6] QC 12 poin     →  lihat §5 — INI YANG TIDAK BOLEH DILEWATI
[7] Edit & tayang  →  warna, teks, subtitle; simpan metadata
```

**Waktu realistis:** 1,5–2 hari kerja untuk setup LoRA, lalu ~4–6 jam per batch 10 konten. Ini pekerjaan penuh waktu, bukan sampingan.

---

## 2. Dataset & training (ringkas, praktis)

**Komposisi dataset (30 gambar):**

| Jenis | Jumlah | Catatan |
|---|---|---|
| *Close-up* wajah frontal | 8 | 3 ekspresi: netral, bicara, tersenyum tipis |
| *Close-up* 3/4 & profil | 6 | Kiri dan kanan |
| *Medium shot* dada ke atas | 8 | Termasuk set & pakaian khas |
| *Full/half body* | 4 | Untuk konten *lifestyle* |
| Detail tanda khas | 4 | Tahi lalat, kacamata, anting, tato, melasma |

**Aturan dataset:**
- Variasi cahaya: siang jendela, cincin lampu, *flash* keras, sore keemasan.
- Variasi latar: minimal 3 latar per karakter.
- **Jangan** masukkan gambar yang sudah di-*retouch* ke dataset — model akan belajar kulit yang salah.
- Beri *caption* yang menyebut tanda khas secara eksplisit (`mole under left eye`, `freckles`, `melasma on both cheeks`), supaya model mengikatkannya ke token karakter, bukan menganggapnya noise.

**Pengaturan awal yang aman:** rank 16–24, learning rate 1e-4, 1.500–2.500 langkah, *trigger token* unik per karakter (`krna_wmn`, `skr_ayu`, `rtn_ksm`, `aly_nr`).

---

## 3. Master prompt per karakter

> Ganti `{token}` dengan token LoRA. Semua prompt ditulis untuk model fotorealistik; jangan menambahkan "masterpiece, best quality" — itu sisa kebiasaan model lama dan tidak membantu.

### Kirana — `krna_wmn`

```
{token}, 27-year-old Indonesian woman, skincare formulator, round wide face,
warm medium skin with visible pores and faint acne marks on chin,
undereye dark circles left untouched, small mole under left eye, small mole on right neck,
short blunt black bob with slightly darker roots, round tortoiseshell glasses pushed up on head,
oversized cream linen shirt with sleeves rolled up, thin silver necklace,
sitting at a warm wooden table in a small home lab, beakers, cheap digital scale,
printed INCI ingredient sheets pinned to a corkboard behind her,
warm 4300K window light from the left, 50mm f/2, subtle film grain, Fujifilm Pro 400H palette,
unretouched real skin texture, deadpan expression, mid-gesture holding tweezers
--no beauty filter, smooth skin, glam makeup, studio background, jewelry stack
```

### Sekar — `skr_ayu`

```
{token}, 24-year-old Indonesian woman, editorial art makeup muse,
deep warm brown skin with visible pores and editorial sheen, sharp cheekbones,
light freckles across nose, short platinum-lilac buzz cut with 1cm dark roots,
small chrome star tattoo under right eye, geometric silver ear cuff on left ear,
bare shoulders, sculptural graphic eye makeup with one intense color accent,
one patch of skin deliberately left bare, saturated seamless backdrop,
hard direct flash with colored gel, sharp defined shadow, 85mm, high contrast,
magazine cover lighting, skin texture fully visible
--no skin smoothing, lightened skin, blue eyes, soft focus, beauty filter
```

**Catatan Sekar:** *look* makeup berubah tiap konten, jadi deskripsikan makeup di prompt per sesi, **tapi jangan pernah** ubah: warna kulit, *buzz cut*, freckles, tato, *ear cuff*. Masking/inpainting area makeup adalah cara paling aman untuk menjaga identitas.

### Ratna — `rtn_ksm`

```
{token}, 52-year-old Indonesian woman, mature beauty creator,
soft square face, laughter lines around eyes and mouth, deep forehead lines,
visible pores, soft brown melasma patches across both cheeks left unretouched,
warm tan skin, silver-grey streaks at temples and front hairline,
shoulder-length dark hair swept back, thin natural brows, no eyeliner,
ivory silk shirt, small gold earrings, gold bracelet on right wrist,
seated in a rattan chair by a large window in a Surabaya home,
tropical plants, wooden window frame, golden late-afternoon light, gentle leaf shadows,
85mm f/1.8, subtle film grain, editorial documentary style, calm dignified expression
--no retouching, no airbrushing, no filtered skin, no hair dye, no contouring
```

**Peringatan:** model *default* akan menghaluskan kulit perempuan 50+ secara agresif. Tambahkan `visible pores, deep wrinkles preserved` dan periksa manual setiap render (§5 poin 6).

### Alya — `aly_nr`

```
{token}, 29-year-old Indonesian plus-size woman, modest beauty creator,
round face with deep dimple on right cheek, medium warm sawo matang skin,
thick natural brows, bold black winged eyeliner, nude-rose lip cream,
dusty rose pashmina hijab draped neatly with one pin, large gold hoop earrings worn over hijab,
oversized olive blazer, gold bracelet on right wrist, natural plus-size body fully visible,
sitting cross-legged on a bed in a small Jakarta apartment, ring light,
shelves of 40 foundation shades arranged behind her, warm domestic lighting,
50mm f/1.8, shallow depth of field, real skin texture, friendly conspiratorial smile
--no body slimming, no jaw narrowing, no skin lightening, no missing hijab
```

---

## 4. Voice design

Suara adalah 50% identitas dan paling sering diabaikan.

| Karakter | Pitch | Tempo | Aksen | Catatan |
|---|---|---|---|---|
| Kirana | Rendah–sedang | Sedang, staccato | Bandung netral, sedikit Sunda | Jeda menggantikan emosi |
| Sekar | Rendah | Lambat | Yogya halus | Hampir bisikan, tidak *asmr* |
| Ratna | Sedang–rendah | Lambat, jelas | Surabaya baku | Artikulasi konsonan akhir |
| Alya | Sedang–tinggi | Cepat | Jakarta | Naik turun, partikel "sih/deh" |

**Aturan:** jangan pakai TTS *default* tanpa penyesuaian. Buat 20 sampel, pilih satu, lalu **kunci**. Ganti suara = ganti identitas; audiens akan merasakannya sebagai *recording*.

**Alternatif yang lebih aman:** untuk karakter yang butuh kredibilitas tinggi (Kirana, Ratna), pertimbangkan **suara manusia asli yang dikontrak** dan tidak pernah tampil di kamera. Ini menghilangkan risiko "suara AI aneh" dan memberi Anda talent yang bisa diwawancarai media.

---

## 5. QC 12 poin (wajib sebelum tayang)

Setiap gambar/video harus lolos semua. Satu kegagalan = *re-render*.

| # | Cek | Gagal jika |
|---|---|---|
| 1 | **Identitas wajah** | Bentuk wajah berbeda dari referensi >10% |
| 2 | **Tanda khas** | Tahi lalat/tato/freckles/melasma hilang atau pindah sisi |
| 3 | **Warna kulit** | Lebih terang dari referensi |
| 4 | **Tangan** | Jumlah jari, panjang jari, atau cengkeraman tidak wajar |
| 5 | **Mata** | Pupil tidak bulat, *catchlight* tidak searah |
| 6 | **Tekstur kulit** | Terlalu mulus untuk usia karakter (Ratna khususnya) |
| 7 | **Teks & label** | Tulisan di kemasan/papan tidak *gibberish* |
| 8 | **Produk** | Logo atau bentuk kemasan nyata yang bisa dikira brand asli |
| 9 | **Anatomi tubuh** | Proporsi tidak konsisten (khusus Alya: tubuh tidak boleh dirampingkan) |
| 10 | **Konteks** | Latar tidak sesuai set karakter (mis. Kirana di studio polos) |
| 11 | **Kepatuhan** | Ada klaim khasiat, *before-after* khasiat, atau produk tanpa nomor izin terlihat |
| 12 | **Metadata** | C2PA/tanda AI hilang (lihat [`02-kepatuhan`](02-kepatuhan-dan-etika.md)) |

**Alat bantu:** buat *contact sheet* 4 kolom wajah sebelah-menyebelah dengan referensi. Mata manusia jauh lebih baik mendeteksi *drift* saat gambar bersebelahan.

---

## 6. Tooling (2026, pilihan praktis)

| Kebutuhan | Opsi |
|---|---|
| Image generation | FLUX.1 (Dev/Pro), SDXL + LoRA, Google Imagen, Midjourney v7 (kurang cocok untuk identity lock) |
| LoRA training | Kohya_ss, Replicate, Fal.ai |
| Video/lipsync | Runway, Kling, HeyGen, Veo — **wajib** cek label AI otomatis di platform |
| Voice | ElevenLabs *voice design* + *voice cloning* (dengan izin talent), atau talent manusia |
| QC batch | Contact sheet + checklist manual; jangan andalkan detektor otomatis |
| Manajemen aset | Folder per sesi + `characters.json` sebagai sumber kebenaran |

**Catatan model:** setiap model punya "bias kecantikan". Model cenderung memutihkan kulit, menghaluskan pori, dan melangsingkan tubuh. Prompt negatif saja **tidak cukup** — QC manual adalah pertahanan utamanya.

---

## 7. Folder & penamaan

```
assets/
  characters/
    kirana.jpg          # referensi utama (sudah ada)
    sekar.jpg
    ratna.jpg
    alya.jpg
  raw/
    2026-11-04_kirana_inci-batch/   # YYYY-MM-DD_karakter_topik
  final/
    2026-11-04_kirana_inci-01.jpg
```

**Aturan:** simpan *prompt* + *seed* + versi LoRA di file `.txt` di sebelah gambar final. Enam bulan kemudian Anda akan bersyukur.
