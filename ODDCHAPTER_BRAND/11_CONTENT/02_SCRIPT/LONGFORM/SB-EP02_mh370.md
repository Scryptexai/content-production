# SB-EP02 — SATU BUSUR SATELIT (long-form 16:9)

Bangunan data untuk `build_longform.py`. Sembilan blok = sembilan segmen VO pemilik;
batas blok hanya di batas segmen yang sudah diverifikasi (`VO_BOUNDARIES.md`).

| blok | VO (dtk) | tata letak | isi |
|---|---|---|---|
| 1 | 0 → 23,59 | footage | hook salah sangka · tiga pelacakan |
| 2 | 23,59 → 46,02 | footage | kerangka: bukti terkuat = sisa hitungan |
| 3 | 46,02 → 109,04 | footage | kronologi 8 Maret 2014, satu lewat satu |
| 4 | 109,04 → 191,40 | **diagram** | tujuh handshake · BTO · BFO · busur ketujuh |
| 5 | 191,40 → 262,92 | footage | tiga gelombang pencarian |
| 6 | 262,92 → 316,84 | footage | tiga serpihan, tukang bersih pantai |
| 7 | 316,84 → 375,42 | **diagram** | dua pembacaan: kosong atau terkendali |
| 8 | 375,42 → 416,70 | footage | perpanjangan 1 Jul 2026 – 30 Jun 2027 |
| 9 | 416,70 → 471,17 | footage | satu pencarian lagi |

Delapan kartu bab menambah 20,8 dtk jeda → master **491,97 dtk (8:12)**, 14.759 frame @30 fps.

## Berkas yang dipakai

- VO utuh: `work/vo/SB-EP02/SB-EP02_full.wav` — gabungan `VO_01`…`VO_09` (mp3 asli hanya di
  Drive: `1yzfE90efvYUJYMEu6iHof_do7aM8ZlLp`). Tidak di Git.
- Caption: `.../VO/SB-EP02/words.json` (1.185 kata, `seg_t` = segmen menurut waktu nyata).
- Bed musik + sfx kartu: `tools/make_bed.py --ep SB-EP02 --dur 520 --root 58` (disintesis
  ffmpeg; tiga sinus rendah + angin pink noise, −26 LUFS; dentuman kartu 48 Hz).
- Footage: `footage/sb-ep02/*.mp4` (43 klip, Coverr), disalin ke `public/footage/` lalu
  di-grade ke `public/footage_graded/` oleh `tools/bake_overlay.py`.
- Plate diagram: `10_FILM/assets/SB-EP02/*.jpg` (7 gambar, dibuat untuk episode ini).

## Membangun ulang

```bash
export PATH=/home/user/bin:$PATH                      # ffmpeg/ffprobe dari npm installer
bash ODDCHAPTER_BRAND/tools/fetch_fonts.sh            # @fontsource → .build/fonts
python3 ODDCHAPTER_BRAND/tools/fix_font_names.py
cp ODDCHAPTER_BRAND/.build/fonts/*.ttf ODDCHAPTER_BRAND/10_FILM/remotion/public/fonts/
python3 ODDCHAPTER_BRAND/tools/make_bed.py --ep SB-EP02 --dur 520 --root 58
python3 ODDCHAPTER_BRAND/tools/build_longform.py SB-EP02 -v
python3 ODDCHAPTER_BRAND/tools/bake_overlay.py SB-EP02   # grade + scrim + sweep
python3 ODDCHAPTER_BRAND/tools/build_longform.py SB-EP02 -v   # ambil jalur footage_graded
cd ODDCHAPTER_BRAND/10_FILM/remotion
LF_NAME=SB-EP02_MH370 node scripts/render-longform.mjs still 60 4800 11200
LF_NAME=SB-EP02_MH370 node scripts/render-longform.mjs render
python3 ../tools/export_srt.py SB-EP02
python3 ../tools/make_shorts_ep02.py
```
