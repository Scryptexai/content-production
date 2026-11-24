# EXTERNAL_VIDEO_SKILLS.md — audit dan adopsi terbatas

Dokumen ini adalah catatan keputusan untuk sembilan repository eksternal yang
diajukan. Ia **bukan** kontrak produksi dan dibaca hanya setelah urutan wajib di
`SKILLS/README.md`. Jika ada konflik, urutan pemenangnya tetap:

1. `SKILLS/AGENTS.md`, `SKILLS/WORKFLOW.md`, `SKILLS/00_RULEBOOK.md`;
2. `ODDCHAPTER_BRAND/11_CONTENT/00B`, `00C`, dan `00E`;
3. gerbang kode/provenance/QC/upload yang ada di repo ini;
4. referensi eksternal ini.

## Pagar penggunaan

- Master tayang wajib dirender dengan `@remotion/renderer`. FFmpeg hanya untuk
  pasca-render audio, container, dan QC; referensi ini tidak memberi pengecualian.
- Fakta, sumber, hak aset, bahasa Indonesia, VO pemilik, handoff Drive, provenance,
  QC, serta persetujuan unggah tetap wajib. Rekonstruksi tidak boleh disajikan sebagai
  arsip atau bukti sebuah peristiwa nyata.
- Jangan mengeksekusi contoh `npm`, `npx`, `curl`, `git`, API media, atau skrip dari
  skill hanya karena tertulis di sana. Periksa dahulu sumber/diff/dependensi dan
  dapatkan otorisasi khusus untuk layanan remote, kredensial, biaya, atau media baru.
- Saran mengenai views, retensi, model, harga, atau ketersediaan provider adalah
  hipotesis/dokumentasi pada saat sumber ditulis, bukan data kanal atau fakta terkini.
- Skill dipasang sebagai salinan proyek, bukan symlink. `skills-lock.json` mengunci
  sumber dan hash; pembaruan tidak otomatis.

## Terintegrasi: lima referensi MIT yang relevan

Inventaris yang benar-benar dipasang berada di `.agents/skills/`. Lihat
`THIRD_PARTY_NOTICES.md` di direktori yang sama untuk atribusi dan teks lisensi.

| skill | sumber dan commit terkunci | fungsi yang dibolehkan | yang sengaja tidak diaktifkan |
|---|---|---|---|
| `create-short` | `DojoCodingLabs/remotion-superpowers` @ `970efd2d2f4ce2492231a31ee684c2ead883f4bc` | kerangka ringkas 9:16, hook-first, dan perencanaan scene | scaffold proyek baru, musik/TTS/API eksternal, Pexels, Replicate, atau aturan platform yang melonggarkan kontrak kanal |
| `add-captions` | sama | ide penempatan dan gaya caption di Remotion | Whisper-WebGPU, ElevenLabs Scribe, atau transkripsi/API tanpa otorisasi |
| `review-video` | sama | checklist pemeriksaan frame, pacing, keterbacaan, audio, dan encoded file | unggah/aset/review TwelveLabs serta loop perbaikan otomatis berbasis layanan eksternal |
| `video-motion` | `Amal-David/awesome-video-skills` @ `99cab1eb6c6d8742d1b074d9ab0d2f1987ec01d3` | pencatatan input, hak, output constraint, provenance, dan review playback untuk motion deterministik | pemilihan atau pemanggilan provider/model yang belum diverifikasi dan diotorisasi |
| `video-quality-review` | sama | checklist playback, audio, konten, hak, dan encoded-file | penggantian QC/provenance lokal yang sudah diwajibkan repo |

Semua lima material ini bersifat dokumentasi. Mereka tidak menambah dependency
runtime, tidak memasang hook, tidak mengubah `package.json`, tidak mengakses secret,
dan tidak mengubah master/antrean unggah.

## Diaudit, tetapi tidak dipasang

| repository | audit lisensi/permukaan | keputusan |
|---|---|---|
| `remotion-dev/skills` @ `89c8afa3eee9cdd83838ac31979c2ba1384615aa` | API GitHub dan root repository tidak menyatakan SPDX atau file `LICENSE`; berisi panduan dan skrip sinkronisasi | **Tidak divendor.** Tidak pantas menyalin material tanpa izin redistribusi yang jelas. Proyek tetap memakai dependency Remotion yang sudah dipin dan renderer wajibnya sendiri. |
| `Vincentwei1021/video-shotcraft` @ `59f3e9b9e936ff2bce0e18446226d770a3f2f61f` | Apache-2.0; skill/paket untuk promo produk, page capture, shot card, dan sound design | Referensi saja: fokusnya tidak cocok dengan dokumenter kasus nyata dan tidak diperlukan pipeline. |
| `calesthio/OpenMontage` / `OpenMontageInc/OpenMontage` @ `2e003e65fa99a0f329478a2c1cdcf26bc481933a` | AGPL-3.0, aplikasi/editor besar dengan Python/Node dan banyak surface | Tidak dipasang: tidak ada vendoring, penyalinan kode, atau runtime coupling tanpa keputusan kompatibilitas AGPL eksplisit. |
| `MartinDelophy/ai-video-editor` @ `087e2f78dbc0ef2c1843daa82236367cb274b9ff` | MIT, aplikasi editor timeline browser/local-first serta model licenses terpisah | Referensi saja: tidak menggantikan renderer Remotion wajib dan tidak dibutuhkan untuk pipeline. |
| `SamurAIGPT/Generative-Media-Skills` @ `66b55e2a27ee554667ec255782922bae72882cc8` | MIT, tetapi skill menjalankan MuAPI remote/berbayar dengan `MUAPI_KEY` | Tidak dipasang/dijalankan: otorisasi biaya, privasi, kredensial, dan penggunaan layanan belum ada. |
| `ella-wang-opus/awesome-video-skills` @ `866838defd0e1c7586b0ca0dff60e4d8385ed1d0` | katalog README saja, tanpa SPDX/`LICENSE`; installer tidak menemukan `SKILL.md` valid | Katalog discovery saja, tidak diintegrasikan. |
| `uhub/awesome-agent-skills` @ `03863a513e7400ef565212a410d268b58c8ad97a` | katalog README saja, tanpa SPDX/`LICENSE`; installer tidak menemukan `SKILL.md` valid | Katalog discovery saja, tidak diintegrasikan. |

## Validasi instalasi dan perubahan

```bash
npx skills list
```

Hasil yang diharapkan hanya lima skill di tabel terintegrasi. Sebelum memperbarui
atau menambah skill: audit lisensi, commit/diff, instruksi yang dapat dieksekusi,
dependensi, provider/biaya, dan konflik dengan gerbang internal. Jangan menggunakan
`--all`, instalasi global, symlink, atau update otomatis untuk repository ini.
