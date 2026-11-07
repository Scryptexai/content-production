# 05 — VISUAL PLAN

Dokumen ini dibuat **setelah** 21 script (`02_SCRIPT/`) dan 21 thumbnail
(`03_THUMBNAIL/`) selesai, sesuai urutan kerja yang diminta. Isinya bukan mood
board: ini instruksi produksi — setiap bidikan punya waktu, subjek, dan cara
membuatnya dengan tool yang benar-benar ada di mesin ini.

Batas nyata yang membentuk seluruh rencana ini: **sandbox tidak bisa mengunduh
dari internet terbuka** (hanya GitHub/npm/PyPI + jalur `footage.yml`). Karena itu
visual dibangun dari tiga bahan yang pasti tersedia — vektor, tipografi, dan
gambar yang dibuat sendiri — bukan dari footage stok.

---

## 1 · TIGA LAPIS, TIDAK PERNAH SATU GAMBAR PENUH

Setiap frame adalah komposisi dari tiga lapis. Tidak ada satu pun bidikan yang
berupa "satu foto besar yang mengisi layar".

| lapis | isi | sumber | catatan |
|---|---|---|---|
| **PLATE** | bentuk dasar: langit, air, dinding, salju, asap | vektor/SVG + gradien yang digambar di Remotion | selalu bergerak pelan (skala 1.00→1.06 dalam 8 s) |
| **OBJEK** | benda yang dibicarakan: menara, tenda, pintu, danau | `generate_image` (potongan), atau SVG presisi | dipotong `sharp`, tidak pernah full-frame |
| **TEKS** | angka, tanggal, label, caption | Space Grotesk / Inter, dibakar | satu pesan per frame |

Alasan aturannya sekeras ini: gambar hasil generasi tidak pernah akurat secara
faktual. Kalau ia jadi seluruh layar, penonton melihat "gambar AI". Kalau ia jadi
satu lapis di balik angka dan garis presisi, ia jadi tekstur.

---

## 2 · SISTEM PER SERI

Lima seri, lima cara memandang. Penonton harus bisa menebak seri hanya dari
warna gerak dan ritme potong.

| seri | warna dominan | tekstur | kamera | ritme potong | suara |
|---|---|---|---|---|---|
| **HILANG** | Ink + Sage, satu aksen Orange | garis horizon, kabut tipis, butir halus | statis, hanya napas skala | 2,5–3 s | angin rendah, tanpa musik |
| **TERSEMBUNYI** | Ink hampir hitam, Ivory dingin | vignette kuat, cincin konsentris | dorong pelan ke dalam (push-in) | 3–4 s | drone rendah, satu nada |
| **ANEH** | Ink + Orange | garis-garis teknis, grid, osiloskop | geser horizontal (tracks) | 1,5–2 s | pulsa synth, klik |
| **BENCANA** | Ink + Sage, Orange hanya di inti | gradien vertikal, partikel | tarikan ke belakang (pull-out) | 2–2,5 s | sub-bass, gemuruh |
| **HARGA** | Ivory di atas Ink, Orange sebagai luka | garis halus, satu garis putus | statis, teks yang bergerak | 3 s | senyap, satu ketukan |

Aturan aksen: **satu Orange per frame, maksimal.** Orange selalu berarti "ini
bagian yang penting" — kalau ada dua, tidak ada yang penting.

---

## 3 · TIMELINE UNIVERSAL

Semua episode memakai kerangka waktu yang sama. Yang berubah hanya isinya.

```
0 ─ 3 s    HOOK        satu plate, satu objek, teks hook muncul 1 frame per kata
3 ─ 7 s    STAKE       plate berganti, angka/tanggal masuk, kamera mulai bergerak
7 ─ 20 s   BUKTI       potongan tercepat di episode ini: 3–4 bidikan
20 ─ 35 s  TITIK BALIK plate berhenti bergerak; semua elemen lain menghilang
35 ─ 50 s   SISA        satu bidikan panjang, tidak ada potongan
50 ─ 60 s  LOOP        kembali ke plate pertama, teks hook terakhir
```

Titik balik adalah satu-satunya momen di mana **tidak ada gerakan**. Itu jeda
yang membuat penonton mendengar kalimatnya.

---

## 4 · SHOT LIST PER EPISODE

Empat plate per episode. Kolom "cara" menyebut bahan yang dipakai: `VEC` = vektor
presisi di Remotion, `GEN` = potongan gambar generasi, `TTL` = tipografi besar,
`ARC` = arsip/berkas yang boleh ditampilkan (peta, grafik, surat).

| EP | 0–7 s | 7–20 s | 20–35 s | 35–60 s |
|---|---|---|---|---|
| **01** | VEC menara + horizon, kabut | VEC denah pulau 3 titik | TTL "PINTU TERKUNCI" di atas plate gelap | VEC menara padam, satu titik Orange |
| **02** | GEN kain tenda sobek, makro | VEC peta jalur 9 titik | VEC potongan tenda dari dalam (garis putus) | GEN salju kosong, jejak kaki |
| **03** | GEN lambung kapal di kabut | ARC peta Atlantik 1872 | VEC daftar muatan (1.701 tong) | VEC sekoci kosong, laut |
| **04** | GEN mobil tertutup salju | VEC profil elevasi (naik, bukan turun) | TTL "MEREKA MENDAKI" | GEN pos jaga hutan, satu pintu |
| **05** | GEN pagar kayu, satu kata | VEC peta Roanoke–Croatoan | ARC ukiran "CROATOAN" | GEN kampung pesisir kosong |
| **06** | GEN retakan aspal berasap | VEC penampang tanah + lapisan bara | VEC peta kota yang menyusut | GEN jalan kosong, lampu jalan |
| **07** | GEN atap bersalju, satu jalur jejak | VEC denah rumah, loteng disorot | TTL "6 ORANG · 1 JEJAK" | GEN perapian dingin |
| **08** | GEN koper terbuka di lantai | VEC sembilan label nama | ARC halaman kode angka | GEN lembah berbatu, kabut |
| **09** | GEN pantai fajar, satu sosok | VEC buku terbuka, huruf acak | TTL "TAMAM SHUD" | ARC peta Adelaide 1948 |
| **10** | GEN dua sosok membelakangi | VEC dua lingkaran yang bertumpuk | VEC dua lingkaran terpisah | GEN kamar tidur, dua tempat tidur |
| **11** | VEC kertas printer "6EQUJ5" | VEC grafik 72 detik | ARC peta langit kosong | VEC satu garis datar |
| **12** | GEN kaki di batu jalan | VEC gelombang orang (siluet berulang) | ARC peta Strasbourg 1518 | GEN jalan kosong |
| **13** | GEN dua sosok di bukit | VEC kertas catatan, tulisan tak terbaca | TTL "MASKER TIMAH" | GEN bukit berkabut |
| **14** | VEC layar TV analog, derau | VEC tiga titik transmisi | TTL "90 DETIK" | GEN ruang kontrol gelap |
| **15** | VEC siluet 1 m vs 1,7 m | VEC penampang gua Liang Bua | ARC skala tengkorak | VEC satu siluet kecil memudar |
| **16** | VEC 12 bangku kelas | VEC gelombang tawa menyebar | TTL "18 BULAN" | GEN kelas kosong |
| **17** | GEN kolom abu di garis pantai | ARC peta radius suara 4.800 km | VEC barometer dunia (gelombang) | VEC matahari terbenam merah |
| **18** | VEC lapisan stratosfer | ARC peta aliran sulfur | VEC grafik suhu global 1816 | GEN ladang gagal panen |
| **19** | VEC pola pohon rebah, radial | VEC satu titik kosong di pusat | TTL "TANPA KAWAH" | GEN hutan Siberia |
| **20** | VEC danau dari atas | VEC penampang danau + lapisan CO₂ | VEC gas turun ke lembah | GEN lembah fajar, diam |
| **21** | GEN meja kerja, kuas, pot cat | VEC dial jam bercahaya | TTL "JILAT KUAS" | VEC satu dial padam |

`ARC` bukan gambar stok: itu peta/grafik yang saya gambar ulang sebagai SVG di
Remotion, supaya garis, label, dan skalanya bisa dipertanggungjawabkan.

---

## 5 · ASET YANG HARUS DIBUAT

### 5.1 Gambar generasi (dipotong, bukan full-frame)

Enam belas plate `GEN`. Semua dibuat dengan satu instruksi gaya yang sama supaya
terlihat satu keluarga:

> "Cinematic plate, 16:9, very low contrast, near-monochrome charcoal and bone
> palette, one small warm accent, heavy atmosphere, no people's faces, no text,
> shallow depth of field, film grain, underexposed, negative space in the upper
> third."

Daftar plate: kain tenda sobek · salju kosong + jejak · lambung kapal di kabut ·
mobil bersalju · pagar kayu · retakan aspal berasap · atap bersalju · koper di
lantai · pantai fajar · dua sosok membelakangi · kaki di batu jalan · sosok di
bukit · ruang kontrol · kelas kosong · ladang gagal panen · meja kerja kuas.

Setiap plate masuk `sharp` → di-resize ke 1440 px, di-desaturasi ke ~12 % saturasi,
di-blur 0,6 px di tepi, lalu disimpan sebagai WebP. Plate tidak pernah dipakai
lebih dari 8 detik berturut-turut.

### 5.2 Komponen Remotion yang harus dibangun

| komponen | dipakai di | isi |
|---|---|---|
| `Plate` | semua | gambar/vektor + napas skala + grain, satu API |
| `HairGrid` | ANEH, BENCANA | grid tipis yang bergerak satu piksel per detik |
| `CountUp` | semua | angka naik dari 0 ke nilai nyata, easing `spring` |
| `MapDiagram` | 01,02,05,06,14,17,18 | SVG dari GeoJSON `d3-geo`, proyeksi tetap |
| `CrossSection` | 06,15,18,20 | potongan vertikal berlapis, label di kiri |
| `Radial` | 19 | pola pohon rebah + satu titik kosong |
| `Dial` | 21 | dial jam bercahaya, jarum berhenti di satu detik |
| `Keyword` | semua | teks cue: masuk per kata, keluar dengan `clipPath` |
| `LoopBack` | semua | mengembalikan frame ke plate hook di 2 detik terakhir |

Semua deterministik: `useCurrentFrame()` + `interpolate` + `spring`. Tidak ada
`Math.random()`, `Date.now()`, atau fetch di dalam komposisi.

### 5.3 Komposisi Remotion

Satu komposisi parameterized, bukan 21 komposisi:

```
ODDCHAPTER-EP          props: { ep, series, shots[], cues[], audio }
```

Nama tanpa garis bawah (Remotion menolaknya). 1080×1920, 30 fps, durasi mengikuti
`durasi` di `content_data.py`.

---

## 6 · TIPOGRAFI & CAPTION

- Headline di layar: **Space Grotesk 700**, 96–120 px, tracking −2, maksimal 3 baris.
- Angka besar: **Space Grotesk 700**, 200–260 px, tabular.
- Cue teks: **Inter 600**, 44 px, huruf kapital, tracking +2, muncul 1 frame per kata.
- Caption bicara: **Inter 600**, 54 px, dasar bawah y = 1420, dua baris maksimal,
  kata aktif Ivory, kata lain Sage 45 %.
- Zona aman: x 96–984, y 300–1500. Tidak ada teks di luar itu, titik.

Warna caption tidak pernah Orange — Orange hanya untuk satu hal penting per frame.

---

## 7 · SUARA

Satu narator untuk semua 21 episode: perempuan, Indonesia netral, tempo 4,4
suku kata/detik. Kalau TTS Indonesia tidak tersedia, `edge-tts`
`id-ID-GadisNeural` adalah fallback yang tercatat.

Per seri: satu bed musik 60 detik yang di-loop (bukan 21 lagu), ditambah tiga SFX
lapis — angin, klik, sub-bass. Mix: voice −16 LUFS, bed −28 LUFS, master −14 LUFS
/ −1,5 dBTP. Caption dibangun dari timing audio nyata, bukan dari perkiraan.

---

## 8 · YANG BELUM BISA DIKERJAKAN

| kebutuhan | status | jalan keluar |
|---|---|---|
| footage stok (Pexels/Pixabay) | **tidak bisa** — egress diblokir | tidak dipakai sama sekali; rencana ini tidak bergantung padanya |
| footage domain publik (Commons/Archive) | **tidak bisa** dari sandbox | `footage.yml` dijalankan manual olehmu → `FOOTAGE/` |
| arsip foto asli peristiwa | **tidak bisa** diverifikasi | digambar ulang sebagai `ARC` vektor |
| peta GeoJSON | bisa dari npm (`world-atlas`) | dipakai untuk `MapDiagram` |

Artinya: 21 episode ini **tidak menunggu** footage apa pun. Kalau nanti footage
asli datang, ia masuk sebagai lapis PLATE tambahan — struktur bidikan tidak berubah.

---

## 9 · URUTAN PRODUKSI (per episode)

1. Animasikan satu frame statis → `npx remotion still`
2. Lihat frame itu. Kalau buruk di satu frame, buruk di 1.800 frame.
3. Animasikan satu shot (hook) → render 3 detik
4. Tambah satu transisi → render 8 detik
5. Tambah audio hook → render 8 detik dengan suara
6. Rakit penuh → render 1080×1920
7. `ffprobe` validasi + cek LUFS

Satu episode diperkirakan 25–40 menit render di sandbox ini (≈25 fps). 21 episode
tidak dirender sekaligus; tiga per hari, sesuai jadwal tayang.
