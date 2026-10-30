# EP01 — "Yang menghukum bukan yang berwenang"

60 dtk · 1080×1920 · 30 fps · 1800 frame

- Kode film: `video/src/shots/index.tsx` (shot 01–06), `video/src/Main.tsx` (rangkaian + bunyi)
- Keluaran: `video/out/film-raw.mp4` → `video/out/knot-theory-ep01.mp4` (loudnorm −14 LUFS)
- Kartu shot yang dipakai: `references/shots/` (spotlight-hero-card, deck-deal-flyin,
  chart-live-moves, space-camera-moves, product-card-progressive-assemble,
  logo-shrink-wordmark-lockup)

---

## 1. Bukti

| Klaim di layar | Angka | Sumber |
|---|---|---|
| "Empat orang tewas diserang hiu" (1916, pesisir New Jersey) | 4 korban, 1–12 Juli 1916 | Achen & Bartels, *Democracy for Realists* (Princeton UP, 2016), bab 5 |
| "Suara turun 3–13 poin di kota pantai" | −12,8 pp (beach boroughs, SE 4,4); −3,2 pp regresi utama; ringkasan penulis "sekitar 10 pp" | sama, bab 5 "Blind Retrospection" |
| "Setiap angka diperiksa lagi… hampir nol" | uji ulang 1872–2012: −0,5 pp, tidak signifikan; 10 spesifikasi, 1 signifikan sekitar 1/20 yang diharapkan karena kebetulan | Fowler & Hall (2018) |
| "Sepuluh cara menguji, satu tampak berarti" | sama | sama |

**Rentang "3–13" dipakai, bukan angka tunggal**, karena sumbernya memang rentang
(3,2 sampai 13,3 tergantung spesifikasi). Ini keputusan jujur, bukan penyederhanaan.

**Yang tidak diklaim:** bukan data Indonesia, bukan data instansi pemerintah. Ini
pemilu kota di Amerika 1916.

---

## 2. Naskah dua lapis (teks di layar = ringkas, VO = penuh, VO belum direkam)

### Shot 01 · 0–10 dtk — kliping
- Kicker: `Knot Theory · Episode 01`
- Judul: **1916** · Sub: *Pesisir New Jersey*
- Badan: "Empat orang tewas diserang hiu."
- Sumber: "Serangan hiu, 1–12 Juli 1916"

Gerak: lampu teater menyapu dari kiri (f76–164) lalu mengunci kliping; kliping
naik dari meja (lift 0,24→0,38) dan berkilau sekali (sheen f180–232). Sirip di
lapisan jauh bergerak lebih lambat dan hampir larut ke kabut (dim 0,6 · blur 8).

### Shot 02 · 10–20,5 dtk — kotak suara
- Kicker: `Pemilu · 7 November 1916`
- Judul: **Suara turun** · Angka: **3–13** (rose)
- Badan: "poin di kota pantai, dibanding kabupaten lain"
- Aksen: *Bukan karena kebijakannya.*

Gerak: lima surat suara jatuh satu per satu (f104–192) ke celah kotak. Kertas
digambar **di belakang kotak** (`behind`), jadi saat badannya melewati garis
siluet tutup, kotak yang menutupinya — terbaca masuk ke celah, bukan menguap.
Kotak sudah ada di frame pertama; shot tidak pernah dibuka dengan layar kosong.

### Shot 03 · 20,5–32,5 dtk — kaca pembesar
- Kicker: `2018 · uji ulang 1872–2012`
- Judul: **Setiap angka diperiksa lagi.** · Sub (serif miring): *hampir nol*
- Badan: "Sepuluh cara menguji, satu tampak berarti."
- Aksen: *Itu pun bisa kebetulan.*

Gerak: kaca pembesar menyapu bidang 100 titik uji dalam empat perhentian; titik di
bawah kaca menyala sesuai jarak (near = 1 − jarak/240). Pada f246–282 sepuluh
titik uji yang redup padam, menyisakan satu titik rose di tengah.

### Shot 04 · 32,5–43,5 dtk — simpul
- Kicker: `Yang tersisa`
- Judul: **Bukan angkanya.**
- Aksen: *Tapi cara kita menilai.*

Gerak: simpul berputar pelan (ry = frame × 0,1), mengendor 9 % (f152–252),
cahaya di belakangnya menguat lalu melemah. Kamera mengelilingi simpul
(zoom 1,0 → 1,1 → 1,02 → 1,14).

### Shot 05 · 43,5–53,5 dtk — poster
- Kicker: `Yang diukur`
- Badan: "Kalau yang menghukum tak bisa dikendalikan,"
- Aksen: *apa yang sebenarnya kita nilai?*

Gerak: enam benda tersusun sebagai satu poster; yang bergerak hanya simpul
(rotasi lambat + napas) dan kamera (zoom 1,1 → 0,97).

### Shot 06 · 53,5–60 dtk — merek
- Wordmark **Knot Theory** · tagline `satu angka · satu sumber`
- Sumber: "Achen & Bartels 2016 · Fowler & Hall 2018"
- "episode berikutnya · siapa yang naik"

---

## 3. Peta bunyi (`src/Main.tsx`)

| Frame | Bunyi | Volume | Untuk |
|---|---|---|---|
| 14 | transition-soft | 0,26 | lampu teater menyala |
| 32 | click-camera | 0,20 | kliping masuk |
| 166 | whoosh-fast | 0,30 | lampu mengunci |
| 232 | transition-soft | 0,22 | kilau kliping |
| 334 / 360 | transition-snap / impact-cine | 0,30 / 0,30 | kotak mendarat |
| 418–546 | swoosh-quick ×5 | 0,18–0,22 | lima surat suara |
| 648–788 | click-camera ×3 | 0,20–0,22 | kaca berhenti |
| 856 / 868 | whoosh-fast / transition-soft | 0,32 / 0,24 | grid runtuh |
| 986 / 1002 | transition-soft / click-camera | 0,24 / 0,16 | simpul muncul |
| 1128 | impact-cine | 0,30 | simpul mengendor |
| 1302 / 1352 / 1420 | whoosh / snap / impact | 0,30 / 0,20 / 0,32 | poster + pertanyaan |
| 1602 / 1628 / 1658 | snap / impact / soft | 0,24 / 0,30 / 0,20 | wordmark |

BGM: satu lapis rendah (`public/audio/bgm/bed.mp3`, turunan `cat-walk.mp3` yang
sudah di-lowpass 240 Hz), 0,30, otomatis turun 45 % selama 26 frame di setiap
impact supaya SFX terbaca.

---

## 4. Yang masih kurang (jujur)

- **VO belum ada.** Naskah di atas siap dibaca; belum direkam.
- **Audio masih pelan.** Campuran mentah terukur −28,9 LUFS; wajib lolos
  loudnorm sebelum tayang (perintahnya ada di `video/README.md`).
- **Data Amerika, bukan Indonesia.** Ditulis di layar, tidak disembunyikan.
- **Tidak ada satu pun karakter manusia di film.** Ini keputusan, bukan kelalaian:
  wajah buatan adalah hal pertama yang membuat video seperti ini terasa murah.
