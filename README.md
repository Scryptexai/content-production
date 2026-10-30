# content-production

Studio konten pendek (9:16) untuk dua niche: **beauty-formulasi** dan **relationship**.
Semua video tanpa karakter manusia: narasi suara + motion graphics vektor (Remotion),
latar gambar AI + (nanti) plate Blender untuk latar bergerak.

Target distribusi: **YouTube Shorts · TikTok · Instagram Reels**, dijadwalkan semi-otomatis
lewat Zernio (approve manual per post).

---

## Status

| Milestone | Isi | Status |
|---|---|---|
| **M1** | Film 3:17 "Kulit Tropis, Formula Subtropis" — 10 adegan, Remotion + musik/SFX | ✅ selesai, `projects/tropical-climate/` |
| **M2** | Fondasi studio: 2 identitas niche, 35 draf konten (7 hari), riset monetisasi, jadwal Zernio | ✅ selesai, `ddcd6fb` |
| **M2.5** | Repositioning editorial relationship: spektrum relasi A–I, editorial bible, 7 naskah riset primer | 🚧 `content/relationship/` |
| **M3** | Latar bergerak (Blender + FFmpeg), A/B hook, siklus uji 30 hari | ⬜ rencana |

Lihat [`MILESTONES.md`](MILESTONES.md) untuk definisi "selesai" tiap milestone.

---

## Peta repo

```
brand/knot-theory/           aset merek Knot Theory (logo, banner, avatar) + renderer
docs/
  00-roadmap.md              roadmap teknis + rencana variasi visual
  01-brand/beauty.md         identitas niche beauty
  01-brand/relationship.md   identitas niche relationship
  01-brand/accounts.md       nama, handle, bio SEO per platform
  01-brand/knot-theory-brand.md  logo, warna, tipografi, ukuran & safe area per platform
  02-monetization.md         jalur pendapatan tercepat + produk yang cocok
  03-publishing-zernio.md    setup MCP Zernio + jadwal 7 hari
  04-production-pipeline.md  Remotion + Blender + FFmpeg
  05-editorial-bible.md      aturan operasional: label fakta, 7 struktur, frasa terlarang
content/
  calendar-7-days.md         35 konten: peta + aturan produksi
  day-01.md … day-07.md      5 skrip per hari (3 beauty + 2 relationship, slate M2)
  relationship/              slate v2: 7 naskah riset primer, 7 wilayah, 7 struktur
automation/zernio/           kanal, kalender 105 post, runner lokal
automation/validate_pieces.py  QC slate v2 (struktur, label fakta, frasa terlarang)
playbook/kepatuhan.md        label AI, klaim, disclosure affiliate
projects/tropical-climate/   M1: pipeline film panjang (Remotion), acuan gaya
```

---

## Aturan main

1. **Tidak ada karakter manusia.** Tidak ada wajah, tidak ada lipsync. Suara + gerak grafis.
2. **Satu video = satu klaim yang bisa dibela.** Sumber dicatat di `content/day-*.md`
   dan, untuk slate v2, di fact ledger tiap naskah. Klaim diberi label
   `FAKTA / ANGKA-TURUNAN / TAFSIRAN-PENULIS / HIPOTESIS / TIDAK-DIKETAHUI`.
3. **Latar tidak boleh statis.** Setiap adegan minimal punya satu gerak lambat
   (Ken Burns, parallax, atau plate bergerak). Aturan ada di `docs/00-roadmap.md` §4.
4. **Hasil render besar tidak masuk git.** MP4 → Drive; repo hanya kode, aset <5 MB, dokumen.
5. **Tidak ada kredensial di repo.** API key hanya di `.env` (gitignored) di mesin yang publish.
