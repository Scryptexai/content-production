# 00E — SUARA NARATOR: MENYAPA, BUKAN MEMBACAKAN LAPORAN

Catatan pemilik, 13 Nov 2026: *“visual udah bagus tapi VO script masih kurang di
storytelling-nya — masih terdengar membaca laporan, bukan berinteraksi dengan
penonton, dan sedang memberi tahu informasi.”*

Itu tepat. Naskah EP01–EP05 disusun sebagai **ringkasan peristiwa**: tanggal,
angka, lalu kesimpulan. Semua kalimatnya benar, tetapi tidak ada satu pun yang
berbicara **kepada** penonton. Tidak ada ajakan melihat, tidak ada pertanyaan yang
ditujukan, tidak ada “kamu”.

Dokumen ini mengunci suara itu supaya tidak kembali.

---

## 1 · TIGA PERBEDAAN YANG MENENTUKAN

| laporan (salah) | bercerita (benar) |
|---|---|
| “Negara memilih memindahkan kota, bukan memadamkan api.” | “Pemerintah tidak memilih memadamkan api. Mereka membayar warga untuk pindah.” |
| “1992. Negara mengambil seluruh kota.” | “Tahun 1992, negara mengambil seluruh kota. Tinggal di sana bukan lagi hakmu.” |
| “Api masih menyala hingga kini.” | “Apinya masih menyala. Di bawah jalan yang sekarang kosong.” |

Yang berubah bukan faktanya. Yang berubah: **siapa yang diajak bicara**, dan
**kapan** kejadiannya (sekarang, di depan mata, bukan “pada tahun itu”).

## 2 · ATURAN SUARA (diperiksa otomatis)

1. **Sapa penonton minimal tiga kali** dengan “kamu”/“kita” — bukan sebagai
   penutup, tetapi di tengah cerita.
2. **Minimal dua ajakan melihat**: *lihat, bayangkan, coba, ingat, dengar,
   perhatikan, pikirkan*. Ajakan ini yang membuat VO terdengar menunjuk layar.
3. **Minimal dua pertanyaan di dalam naskah** (selain hook): pertanyaan membuat
   penonton menjawab di kepala, dan itu terasa seperti percakapan.
4. **Satu ide satu kalimat.** Maksimal dua kalimat per baris VO (hook dan penutup
   boleh tiga). Kalimat panjang selalu terdengar seperti dibacakan.
5. **Dilarang kosakata laporan**: *diketahui, dilaporkan, tercatat, merupakan,
   disebutkan, berdasarkan, adapun, tersebut, sejumlah, berbagai, sedangkan,
   namun, sehingga, mengakibatkan, dilakukan, terjadi*. Kalau salah satu muncul,
   kalimatnya hampir pasti berbunyi seperti berita.
6. **Tanggal diucapkan seperti orang bercerita**: “Tahun 1981, …”, bukan
   “1981: …”. Angka tetap boleh, tetapi tidak boleh menumpuk — satu angka per
   baris, maksimal.
7. **Kata ganti orang, bukan jabatan.** “Mereka” untuk pelaku, “kamu” untuk
   penonton, “dia” untuk satu orang. “Pihak berwenang”, “ pemerintah daerah”,
   “warga setempat” membunuh suara.

## 3 · URUTAN YANG TETAP (dari `00B`)

Klimaks + entitas → cut + pertanyaan → cerita dari awal → turn → consequence →
loop. Suara baru tidak mengubah urutan; ia mengubah **cara mengucapkannya**.

## 4 · CONTOH: EP06 SEBELUM → SESUDAH

| baris | versi laporan (dipakai sampai EP05) | versi bercerita (dipakai EP06 ke atas) |
|---|---|---|
| hook | 1962. Lima petugas membakar sampah di atas tambang. Api itu masih menyala. | 1962. Api ini dinyalakan di bawah sebuah kota. Sekarang lihat rumahnya. |
| cut | Kenapa api sekecil itu tidak bisa dipadamkan selama enam puluh tahun? | Coba bayangkan api itu di bawah rumahmu. Kamu akan pindah ke mana? |
| relate | Kamu pernah tinggal di rumah yang sudah tidak aman, tapi tetap tinggal? | Kita sering bertahan, walau tahu tempatnya tidak aman. |
| turn | Negara memilih memindahkan kota, bukan memadamkan api. | Pemerintah tidak memilih memadamkan api. Mereka membayar warga untuk pindah. |
| penutup | Api yang mereka nyalakan untuk membersihkan sampah masih menyala di bawah kota. | Apinya masih menyala. Di bawah jalan yang sekarang kosong. |

Bedanya bisa diuji: versi kanan **tidak bisa dibacakan dengan nada berita**
tanpa terdengar aneh. Itu tujuannya.

## 5 · GERBANG

`python3 tools/check_story.py EPxx` sekarang punya dua lapis:

- lima efek (hook, celah, turn, echo) — tidak berubah;
- **suara narator** (§2 di atas) — baru, dan gagal kalau naskah kembali ke gaya
  laporan.

Naskah lama (EP01–EP05) sengaja dibiarkan: videonya sudah tayang, dan mengubah
naskahnya tidak mengubah apa pun di layar. Yang wajib memakai aturan ini adalah
setiap episode yang belum dirender, mulai EP06.

---

## 6 · HOOK: TUJUH PINTU MASUK, SATU LARANGAN

Keluhan kedua pemilik (13 Nov 2026): *“kalimat awalnya masih tidak punya hook…
gaya bahasanya masih terdengar orang yang baca koran, bukan yang sedang ngajak
ngobrol.”*

Penyebabnya bukan kata pembukanya, tetapi **kebiasaan membuka dengan tanggal**:
`1962. Api ini dinyalakan…` Itu kalimat pembuka berita. Tanggal adalah fakta yang
paling tidak menarik untuk didengar pertama, dan menaruhnya di depan memaksa
narator berhenti, mengambil napas, lalu membacakan. Penonton mendengarnya sebagai
pembaca, bukan sebagai teman ngobrol.

**Larangan:** hook tidak boleh diawali tahun/angka. Tanggal masuk nanti — sebagai
kejutan (“Sembilan belas tahun kemudian…”), bukan sebagai pintu.

### Tujuh pintu yang boleh dipakai

| pintu | bentuk | contoh untuk kasus nyata |
|---|---|---|
| **Pertanyaan** | pertanyaan yang penonton jawab di kepala | “Kamu pernah tinggal di rumah yang lantainya hangat, padahal di luar musim dingin?” |
| **Pernyataan** | kalimat datar yang isinya tidak masuk akal | “Ada kota di Pennsylvania yang menyala dari bawah.” |
| **Fakta** | satu angka yang mengejutkan, bukan tanggal | “Sebuah api sudah menyala di bawah kota ini lebih lama dari usia kamu.” |
| **Harapan** | keinginan sederhana yang lalu dilawan | “Mereka cuma ingin kotanya bersih sebelum libur panjang.” |
| **Khayalan** | ajakan membayangkan diri sendiri di sana | “Bayangkan lantai rumahmu hangat, dan kamu tidak tahu kenapa.” |
| **Adegan** | satu gambar yang bergerak | “Lima orang berdiri di tepi lubang tambang, membawa korek api.” |
| **Dialog** | kalimat yang pernah diucapkan | “‘Apinya tidak akan sampai ke rumah.’ Kalimat itu diucapkan tahun 1962.” |

Aturan memilih: **satu pintu saja per episode.** Dua pintu di kalimat pertama
terdengar seperti iklan. Sesudah pintu, langsung beri satu detail yang bisa
dilihat (benda, bagian tubuh, cuaca), bukan penjelasan.

### Ritme dan intonasi (yang membuatnya terdengar ngobrol)

1. **Panjang-pendek bergantian.** Kalimat pembuka boleh 10–14 kata; kalimat
   sesudahnya dipotong jadi 3–6 kata. Contoh: *“Ada kota di Pennsylvania yang
   menyala dari bawah. Api itu belum pernah mati.”*
2. **Satu kata yang ditekan per baris.** Bukan kapital di layar — pilih kata yang
   paling mengejutkan dan letakkan di akhir kalimat.
3. **Jeda = titik, bukan koma.** Di VO, koma hilang. Kalau butuh jeda, potong
   kalimatnya.
4. **Tanpa kata sambung pembuka.** “Sementara itu”, “Selain itu”, “Kemudian”
   adalah tanda orang membaca. Mulai langsung dari subjek.
5. **Ucapkan seperti memberi tahu teman di meja sebelah**, bukan mengumumkan di
   panggung: tidak ada “perlu diketahui”, tidak ada “menurut catatan”.
6. **Satu baris = satu tarikan napas.** Kalau satu baris tidak muat diucapkan
   dalam satu napas, baris itu terlalu panjang.

### Gerbang otomatis

`check_story.py` sekarang menolak hook yang diawali angka/tahun, dan mencatat
kalau hook lebih dari 12 kata.

---

## 7 · IDENTITAS SUARA (dikunci 14 Nov 2026)

Pemilik menetapkan satu suara untuk seluruh kanal mulai EP08 — bukan lagi
memilih suara per episode.

| unsur | nilai |
|---|---|
| penyedia | ElevenLabs |
| **voice_id** | **`ojz6ro9PB1xDu44lymdM`** — narator internal kanal (dipakai EP01–EP07; **dikembalikan pemilik 16 Nov 2026**) |
| model | `eleven_turbo_v2_5` · **speed 0.85** (diganti 14 Nov 2026, lihat catatan di bawah) |
| format | `mp3_44100_192` |
| settings | stability 0.38 · similarity 0.82 · style 0.35 · speaker boost aktif · speed 1.00 |
| kecepatan target | 138 kata/menit, dikoreksi per segmen dengan `atempo` |

Sumber kebenaran: `tools/voice.json`. Naskah tidak menyimpan id suara; skrip
`tools/eleven_audio.py` membacanya dari sana, jadi mengganti suara hanya boleh
dilakukan di satu berkas itu dan atas perintah pemilik.

**Kenapa dijalankan di GitHub Actions:** `api.elevenlabs.io` tidak terjangkau dari
sandbox. Antrean `11_CONTENT/06_UPLOAD/audio-queue/EPxx.json` dengan
`"status": "requested"` memicu `.github/workflows/eleven-audio.yml`; hasilnya
mp3 per segmen (nama sama dengan yang dibaca `build_timing.py`), efek suara per
nama di `ep["sfx"]`, lalu `timing.generated.json` dan `bed.wav`.

**Efek suara & musik:** efek dibuat dari deskripsi bunyi (bukan nama kategori) di
`SFX_PROMPTS` dalam `tools/eleven_audio.py`; musik hanya dipakai kalau memang
perlu, karena `bed.wav` sudah mengisi ruang.

---

## 8 · RUJUKAN KITAB KERJA (14 Nov 2026)

Pemilik menambahkan dua set dokumen yang kini menjadi skill tetap kanal:

- **Dua belas dokumen root** (`HOOK ENGINEERING.md`, `AUDIO PRODUCTION.md`,
  `STORYTELLING-FONDAMENTAL.md`, `EMOTIONAL-PACING.md`, `MEMORABLE-ENDING.md`,
  `VISUAL-STORYTELLING.md`, `IMAGE-GENERATION.md`, `ANIMATION&MOTION.md`,
  `VIDEO_&_EDITING.md`, `NARRATIVE-TENSION-&-AUDIENCE-RETENTION.md`,
  `TOOL-ORCHESTRATION.md`, `EDITORIAL-FONDATION.md`), ditambah
  `NATURAL-INDONESIAN-WRITING-HUMAN-VOICE.md` yang sebelumnya kosong dan kini terisi.
- **`SKILLS/elevenlabs-tts-2026/`** — skill pack TTS (v4): tanda baca dulu, tag minimal,
  tanpa SSML, QA dengar A/B.

Indeks dan aturan kerjanya ada di **`SKILLS/README.md`**, **`SKILLS/AGENTS.md`**,
**`SKILLS/WORKFLOW.md`**, dan **`SKILLS/00_RULEBOOK.md`**.

Yang mengikat tetap dokumen ini dan `00B`/`00C`: kalau dokumen baru bertentangan,
`00B`/`00C`/`00E` yang menang, karena di situlah gerbang otomatis dipasang.

Aturan tambahan yang kini diperiksa mesin (lihat `tools/check_story.py` fungsi
`tts_safe`): teks yang diucapkan harus bersih dari `<tag>`, `[tag]`, `**`, penomoran
daftar, dan emoji. Singkatan ditulis lengkap; angka dipastikan terbaca benar.

**Kenapa model diganti (14 Nov 2026).** VO EP08 pertama terdengar terlalu cepat,
jedanya salah tempat, dan pertanyaan berakhir turun. Setelah diukur
(`tools/speech_prosody.py`): `eleven_multilingual_v2` mengambil tempo 203–219
kata/menit pada kalimat 12 kata **dan mengabaikan parameter `speed` sepenuhnya**
(dua berkas dengan speed berbeda byte-identik). `eleven_turbo_v2_5` pada kalimat
yang sama dengan speed 0.85: 142 wpm, dan pertanyaan berakhir naik (+0,97 semit).
Karena itu model kanal sekarang `eleven_turbo_v2_5`, speed 0.85.

**Aturan naskah yang lahir dari kejadian itu:**

1. Satu **breath group** per segmen. Kalau satu segmen memuat dua gagasan besar,
   jeda akan jatuh di tempat yang salah — dan kita tidak bisa memindahkannya,
   karena jeda di dalam berkas ditentukan model, bukan kita.
2. Jeda antar kalimat dikendalikan di timeline (`GAP` di `build_timing.py`),
   bukan dikarang lewat koma.
3. Pertanyaan harus berakhir naik. Ini diukur, bukan dirasa: `tail_semit` ≥ −1,5.
4. Kalau satu segmen >160 wpm, pecah kalimatnya — jangan menaikkan `speed`.

## 9 · ATURAN 15 NOV 2026 — DAN PEMBATALANNYA 16 NOV 2026

> **16 Nov 2026, perintah pemilik:** *"back to vo internal saja yg dipakai content ep
> sebelumnya, hapus set up vo terbaru ini."* Suara **Denas dihapus seluruhnya** dari
> kanal, termasuk `atempo`/kompresor otomatis (`polish`) yang dibuat khusus untuk
> menambalnya. `tools/voice.json` sekarang menunjuk `ojz6ro9PB1xDu44lymdM`, model
> `eleven_turbo_v2_5`, speed 0.85, tanpa koreksi tempo paksa.
>
> Yang TETAP berlaku dari pengalaman itu: (a) suara harus identik di semua segmen dan
> dibuktikan dengan `voice_consistency.py`; (b) level antar segmen tidak diserahkan ke
> model — `mix_master.py` menyamakan RMS; (c) bed diukur, bukan ditebak.
> Yang DIBATALKAN: identitas Denas, `polish`/atempo, dan target 138 wpm paksa.

Catatan asli 15 Nov (disimpan sebagai jejak):

Yang dilaporkan: "setiap scene vo-nya beda", "tidak menuruti skill", "backsound terlalu
nyaring", "suara turun 1–2 kata di zona yang tidak tepat", "jangan unggah sebelum saya setujui".

**a · Satu suara, dibuktikan dengan ukuran.** `voice_id` lama (`ojz6ro9PB1xDu44lymdM`)
menghasilkan F0 144 Hz pada satu segmen sementara median episode 110 Hz — itu suara lain,
bukan variasi emosi. Sekarang dipakai **Denas** dan setiap episode wajib lulus
`python3 tools/voice_consistency.py EPxx` (F0 median ±18%, spectral centroid ±35%,
tilt ±4 dB). Gagal = jangan render.

**b · Tempo dikoreksi, bukan diharapkan.** Parameter `speed` tidak konsisten dihormati
model. Sesudah TTS, setiap segmen diukur; kalau menyimpang >10% dari 138 wpm, diterapkan
`atempo` (ubah tempo tanpa ubah pitch). Hasil EP08: semua 12 segmen 126–147 wpm
(rata-rata 138,4), dari sebelumnya 202 wpm di satu segmen.

**c · Dinamika diratakan ringan.** Kompresor 3:1 (threshold −22 dB, attack 6 ms,
release 140 ms) + limiter, supaya satu-dua kata yang tiba-tiba pelan tidak tenggelam —
tanpa membuat kalimat datar.

**d · Bed tidak boleh bersaing.** `build_bed.py` sekarang mengukur hasilnya dan menggeser
ke **−32 LUFS** (≈18 dB di bawah narasi). Di Remotion, bed 0.85 dan efek 0.9. Hierarki:
VO → efek → musik → ambience.

**e · Tidak ada unggahan tanpa persetujuan.** `youtube-upload.yml` menolak berkas antrean
yang tidak memuat `"approved": true`. Master dibuat, diukur, ditunjukkan ke pemilik,
baru diunggah setelah pemilik menyatakan setuju.


## 10 · ATURAN PERFORMA SHORTS (16 NOV 2026)

Data kanal: Shorts berhenti di ~1.000 tayangan. Rata-rata rasio *tetap menonton*
57,9% (42–69%), durasi 59–73 detik, likes <1,5%, **shares 0**, komentar hampir tidak
ada. Artinya: hook kalah di 1–2 detik pertama, dan durasi terlalu panjang untuk
diputar ulang. Aturan baru untuk EP08 ke atas — diperiksa mesin, bukan diingat:

| # | aturan | di mana dijaga |
|---|---|---|
| a | **Durasi 35–45 detik**, bukan 50–73 | `check_story.py` (estimasi) + `build_timing.py` (hasil ukur) |
| b | **Narasi mulai ≤0,15 dtk**, bukan 0,6 | `LEAD` di `build_timing.py` |
| c | **Cover hanya 0,5 dtk** (15 frame), dulu 1,5 dtk | `INTRO` di `Episode.tsx` |
| d | **Jeda antar segmen 0,22 dtk**, dulu 0,30 | `GAP` di `build_timing.py` |
| e | **Hook boleh pernyataan** asal menyebut benda konkret — bukan hanya pertanyaan/angka | `check_story.py` butir (1b) |
| f | **Penutup wajib pertanyaan terbuka** yang mengundang komentar | `loop` + `diskusi` |
| g | **Prioritas share**: satu kalimat di akhir yang layak dikirim ke orang lain ("kalau kamu dipisahkan dari satu-satunya orang yang bisa kamu ajak bicara…") | naskah, dinilai manual |

Yang **tidak** boleh dikorbankan demi durasi: satu ide satu kalimat, entitas konkret di
hook, dan penutup yang memanggil kata dari hook (echo). Kalau memangkas naskah membuat
salah satunya hilang, potong beat `consequence`, bukan hook.
