# Milestones

## M1 — Film panjang "Kulit Tropis, Formula Subtropis" ✅

**Tanggal:** 2026-10-28 · **Commit:** `2b9274d` · **Tag:** `milestone-1`

| Item | Nilai |
|---|---|
| Durasi | 3:16,97 (5.909 frame @30 fps) |
| Resolusi | 1080×1920, h264 yuv420p BT.709 + AAC 192k |
| Ukuran | 38,7 MB (versi Pillow sebelumnya 69 MB) |
| Audio | −15,9 LUFS, true peak −0,8 dBFS, LRA 2,2 |
| Renderer | Remotion 4 + Chromium (@sparticuz/chromium + lib AL2023) |

**Yang terbukti:** pipeline narasi TTS → asset AI → motion graphics DOM/SVG → musik
sintesis → mux. Semua satu timeline, presisi frame.

**Catatan review (dari pemilik):**
> "Motion-nya sudah sangat baik — pertahankan gayanya. Yang perlu dikembangkan:
> background jangan statis, harus bergerak, supaya tidak monoton."

→ ditindaklanjuti di M3 (`docs/00-roadmap.md` §4).

**Artefak:** `projects/tropical-climate/` (kode + dokumentasi), MP4 di Drive
(`movie/tropical-climate`).

---

## M2 — Fondasi studio dua niche 🚧

Definisi selesai:

- [x] Repo bersih: seluruh setup karakter/dokumen lama dihapus
- [x] Dua identitas niche (nama, suara, palet, format, hashtag)
- [x] Kit akun YT/TikTok/IG: nama, handle, bio SEO, pinned, checklist verifikasi
- [x] Riset monetisasi: jalur tercepat + produk + rate card
- [x] 35 draf skrip (5/hari × 7 hari) dengan sumber & caption
- [x] Kalender 105 post (35 video × 3 platform) siap di-approve di Zernio
- [x] Panduan setup MCP Zernio di mesin lokal

---

## M3 — Variasi visual & siklus uji 🚧 rencana

- [ ] Plate latar bergerak (Blender) untuk 8 tema latar
- [ ] 3 varian hook per konten (A/B) + pencatatan hasil
- [ ] Otomasi QC (durasi, loudness, safe-area teks)
- [ ] Dashboard ringkas: CTR, retensi 3 detik, simpan, follow/1000 views
