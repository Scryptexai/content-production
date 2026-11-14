# 07_LONGFORM — format panjang (8–12 menit)

Shorts di `02_SCRIPT/` menjawab satu pertanyaan dalam 60 detik. Format panjang
tidak boleh jadi Shorts yang diperpanjang: ia harus punya **argumen** — satu hal
yang berubah di kepala penonton setelah menonton, bukan hanya fakta yang
bertambah.

| Unsur | Aturan |
|---|---|
| Kanvas | 1920×1080 (16:9), 30 fps. Bukan 9:16 — YouTube menilai video dari durasi, bukan rasio, tapi 16:9 adalah bentuk yang ditonton orang di TV dan laptop. |
| Durasi | 8–12 menit. Di bawah 8 menit, lebih baik jadi Shorts. Di atas 12, butuh dua sub-argumen, bukan satu. |
| Narasi | 140–155 kata/menit. 1.400–1.700 kata untuk 10 menit. Satu napas = satu kalimat. |
| POV | Satu POV untuk seluruh episode, dipilih sebelum menulis (lihat `00_STRATEGI.md` §2). Untuk format panjang, **D (“kita”)** hampir selalu lebih tepat: cerita panjang butuh tesis, dan tesis butuh suara yang bisa mengoreksi. |
| Jumlah bab | 5–8 chapter YouTube, masing-masing ≥ 30 detik, diberi nama dengan kata benda — bukan “Pendahuluan”/“Kesimpulan”. |
| Pertanyaan | Setiap bab wajib menyisakan satu pertanyaan yang belum dijawab bab itu. Bab yang menutup semua pertanyaannya adalah bab yang membuat orang berhenti. |
| Sumber | Setiap angka dan peristiwa punya baris di `SOURCES.md`. Angka yang diperdebatkan ditulis sebagai rentang, dengan penyebut nama penyusunnya. |
| Gerbang | `python3 tools/check_longform.py LF01` harus lulus sebelum masuk produksi. |

## Struktur tujuh babak

Berbeda dari Shorts (klimaks → pertanyaan → cerita), format panjang memakai
klimaks **dan** tesis di depan, lalu membuktikannya:

| # | babak | fungsi | porsi |
|---|---|---|---|
| 0 | KLIMAKS + TESIS | kejadian paling ekstrem, lalu satu kalimat yang menyatakan apa yang akan dibantah episode ini | 0–40 s |
| 1 | ORANG | siapa yang ada di dalamnya, dan apa yang mereka inginkan | 10–15% |
| 2 | SEBAB | keputusan kecil yang membuat bencana itu mungkin | 10–15% |
| 3 | MALAM | peristiwa itu sendiri, dengan waktu dan tempat yang konkret | 15–20% |
| 4 | HARGA | berapa yang dibayar, dan oleh siapa | 15% |
| 5 | DIAM | kenapa dunia tidak membicarakannya | 15% |
| 6 | TURN | fakta yang mengubah arti seluruh cerita — tidak menambah fakta baru | 10% |
| 7 | ECHO | pertanyaan yang dibawa pulang penonton | 5% |

## Penamaan & tata letak

```
07_LONGFORM/
├── README.md
└── LF01_<slug>/
    ├── SCRIPT.md              narasi + isyarat visual + chapter
    ├── SOURCES.md             klaim → sumber → tingkat keyakinan
    └── RENCANA_PRODUKSI.md    plate, urutan kerja, yang harus diputuskan manusia
```
