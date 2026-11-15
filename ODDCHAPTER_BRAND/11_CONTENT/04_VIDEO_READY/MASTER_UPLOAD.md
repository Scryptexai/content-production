# MASTER UPLOAD — daftar serah-terima video jadi

**Aturan (berlaku sejak 15 Nov 2026, atas permintaan pemilik):**
setiap video yang **selesai di-build wajib langsung diunggah ke Drive**, di sesi
yang sama dengan render-nya. Render yang belum ada di Drive dianggap belum jadi.

- Folder Drive: **`video ready`** — `1fVoOvZgiYB3V7S2C5LfMrCpo-c4Xxzo2`
- Nama berkas: `EPxx_1080x1920_master.mp4` (satu nama per episode; versi dicatat di sini)
- Render yang digantikan **diganti nama**, bukan dihapus: `..._v1-<alasan>.mp4`
- Setiap baris di tabel ini harus punya id Drive yang benar-benar ada.

Periksa kapan saja:

```
python3 tools/check_master_upload.py
```

Skrip itu membandingkan `10_FILM/remotion/output/episodes/*.mp4` dengan tabel ini
dan berhenti dengan status ≠ 0 kalau ada master lokal yang belum tercatat.

---

## Master aktif

| ep | versi | durasi | ukuran | diunggah | Drive file id |
|---|---|---|---|---|---|
| EP01 | v7 | 64,85 s | 17,9 MB | 8 Nov 2026 | `18u4GwSOAMVIsCtnPIGBAjvc-Axy-Nrur` |
| EP02 | v1 | 72,32 s | 21,1 MB | 8 Nov 2026 | `1WF4yQQkg02pctkJ8QsX-xls37gQCvoyJ` |
| EP03 | v1 | 71,80 s | 21,9 MB | 8 Nov 2026 | `1chsdzAkdplfm3JdmBHOefj5MQP_khUiZ` |
| EP04 | v1 | 70,81 s | 17,3 MB | 11 Nov 2026 | `1O2onobslZxZo5miA83s6d5cEHcfK1OGL` |
| EP05 | v1 | 68,84 s | 17,6 MB | 13 Nov 2026 | `1ls-1EVOdp-2L81QvNpyi6QjzqmNHDdJY` |
| EP06 | v2 | 54,38 s | 16,0 MB | 14 Nov 2026 | `1O4HvhK22QLjxXuLkhOzngAH-WS_jGLtH` |
| EP07 | v1 | 48,28 s | 14,1 MB | 14 Nov 2026 | `1OrIaFbZKj_yufo-HOSpVCYxnhmUHYKc8` |
| EP08 | v2 | 53,50 s | 15,3 MB | 14 Nov 2026 | `131CrG69yCLrczrTygjYbTV5Hs-TxIDRl` |
| EP09 | **v4 — VO buatan user + cover benar** | 53,78 s | 32,9 MB | 16 Nov 2026 | `1leWLFt4QuLEgXMSmnemYAXRWlMr9vUCT` |

## Arsip (digantikan, tetap ada di Drive)

| ep | nama berkas | alasan | Drive file id |
|---|---|---|---|
| EP09 | `EP09_1080x1920_master_v3-intro-lama.mp4` | VO user sudah benar, tetapi 0,5 dtk pertama masih cover Somerton Man | `1ZMikYIar_HDYmS8wY5-wGbBDdM9DTnOL` |
| EP09 | `EP09_1080x1920_master_v2-vo-lama.mp4` | render 15 Nov: audio dari naskah lama (Somerton Man), bukan VO user | `1SmFv67IVaoCxC7Ow1SCid4Pk6wtbkLBl` |
| EP09 | `EP09_1080x1920_master_v1-plate.mp4` | render lama, seluruh episode cuma satu plate vektor statis (bukan foto per segmen) | `1hfB9nq-fScY1dJtA5_NCMYjoUH4r7lsi` |
| EP08 | `EP08_1080x1920_master.mp4` | versi sebelum v2 | `10rTpHzuEnQkfXNiC8dWuVAU23TQv-oD6` |
| EP08 | `EP08_1080x1920_master_v4.mp4` | percobaan v4 | `1_aFdKTXtaT1ycHe2IbCHhOawUNoS3CQx` |
| EP08 | `EP08_1080x1920_master_v5_internal.mp4` | uji internal | `1UrKOv6JgRJOzh1D5LOjuJ58mAHp1MJtm` |
| EP06 | `EP06_1080x1920_master.mp4` | versi sebelum v2 | `1NHnFpmKd2YsTPEhzuORBkQj4b4xAn-n4` |

## Catatan aset kerja EP09

Foto per segmen EP09 (`public/plates/EP09/`) tidak disimpan di Git — folder
`public/` di-ignore. Master final ada di Drive (`1leWLFt4QuLEgXMSmnemYAXRWlMr9vUCT`),
jadi tidak ada yang hilang dari hasil tayang. Kalau EP09 perlu dirender ulang,
9 foto per segmen harus dibuat lagi dulu; suara, timing, bed, sfx, dan cover
sudah ada di repo.

## Belum di-build (belum ada master)

EP10–EP21. EP10 punya VO + draft plate di Drive
(`1j8ofLkaXcDvBFtDDfNWdHuyDZY5gSqnY`) — itu **bukan** master: belum ada foto per
segmen, jadi belum memenuhi standar EP01–EP09. Begitu fotonya dibuat, render →
unggah → baris baru di tabel ini.
