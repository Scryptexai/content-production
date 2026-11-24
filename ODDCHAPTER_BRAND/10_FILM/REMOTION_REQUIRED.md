# REMOTION REQUIRED — gate produksi dan publikasi

**Berlaku untuk setiap video baru tanpa pengecualian.**

Semua publish master ODDCHAPTER—Shorts, episode panjang, versi revisi, potongan,
atau eksperimen—wajib memiliki **visual yang dirender oleh Remotion** menggunakan
`@remotion/renderer`. Tidak ada jalur FFmpeg-only, slideshow, Pillow→FFmpeg,
atau renderer pengganti untuk master yang akan diunggah.

## Batas yang diperbolehkan

FFmpeg boleh dipakai **setelah** render visual Remotion hanya untuk:

- mux audio;
- normalisasi loudness dan encode audio;
- faststart/container final;
- pemeriksaan teknis (durasi, hash, codec, silence, loudness);
- pembuatan thumbnail atau aset pendukung.

FFmpeg tidak boleh menjadi pembuat frame visual publish master. Visual harus
berasal dari composition Remotion yang tercatat.

## Bukti wajib sebelum unggah

Setiap metadata `11_CONTENT/06_UPLOAD/<EPISODE>.json` wajib menyertakan:

```json
"render_provenance": {
  "engine": "remotion",
  "engine_version": "4.0.541",
  "renderer": "@remotion/renderer",
  "composition": "<composition-id>",
  "entrypoint": "ODDCHAPTER_BRAND/10_FILM/remotion/src/index.ts",
  "manifest": "ODDCHAPTER_BRAND/11_CONTENT/06_UPLOAD/provenance/<EPISODE>.json"
}
```

Manifest yang di-commit wajib menyebut `episode`, `composition`, `entrypoint`,
`engine`, `renderer`, dan `master_sha256` yang sama dengan metadata. Validator
`tools/upload_zernio.py` menolak unggahan sebelum menghubungi Zernio bila bukti
ini tidak ada atau tidak cocok.

## Ketentuan untuk video yang sudah telanjur tayang

Video lama tidak dapat diganti file-nya di YouTube. Jika perlu koreksi visual,
buat ulang dengan Remotion, QA, lalu unggah sebagai video baru hanya setelah
pemilik menentukan penanganan video lama (tetap, unlist, atau hapus). Tidak ada
unpublish, delete, atau unggah duplikat otomatis.
