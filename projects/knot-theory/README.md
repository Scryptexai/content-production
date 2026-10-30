# Knot Theory — proyek produksi

Kanal short-form vertikal (9:16, 30 fps, < 3 menit) yang membahas **kebijakan dan
pemerintahan berbasis bukti**: satu angka, satu sumber, tanpa menyebut partai atau
nama pejabat.

## Produksi video

Seluruh video dibuat dengan **video-shotcraft** (Remotion + kartu shot motion).
Tidak ada lagi pipeline lain di folder ini — harness SVG lama, rig karakter,
plate Blender, dan SFX prosedural sudah dihapus.

- Kode film: [`video/`](video/) — lihat [`video/README.md`](video/README.md)
- Aset objek: foto berlatar hijau → chroma key → PNG transparan
  (`video/tools/key_objects.py`), dipakai sebagai **benda di dalam ruang**,
  bukan sebagai latar.

## Episode yang sudah jadi

| EP | Judul | Durasi | Sumber utama | Berkas |
|---|---|---|---|---|
| 01 | Yang menghukum bukan yang berwenang | 60 dtk | Achen & Bartels, *Democracy for Realists* (2016) bab 5; Fowler & Hall (2018) | `video/out/knot-theory-ep01.mp4` |

## Dokumen

- `docs/` — brand, niche, naskah, pipeline
- `content/` — kalender dan draf naskah per hari
