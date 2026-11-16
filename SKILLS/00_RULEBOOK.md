# 00_RULEBOOK — aturan yang dipakai, bukan yang dikagumi

Ringkasan kerja dari dua belas dokumen root + skill pack TTS. Setiap baris di sini
harus bisa dijawab "ya/tidak" saat memeriksa naskah. Teori lengkapnya ada di
dokumen masing-masing; dokumen ini yang dibaca sambil menulis.

Tanda: **[M]** = diperiksa mesin (`tools/check_story.py`), **[H]** = diperiksa manusia
sebelum rekam.

---

## 1 · Editorial (`EDITORIAL-FONDATION.md`)

- **[H]** Satu episode = satu alasan untuk peduli. Kalau alasannya "ini sedang viral", belum cukup.
- **[H]** Pisahkan empat hal dan jangan campur: **fakta**, **tafsir**, **opini**, **hipotesis**.
- **[M]** Tidak ada kata yang meminta perhatian alih-alih menunjukkan bukti
  (`misteri`, `rahasia`, `mengerikan`, …).
- **[H]** Kritik menyerang tindakan/klaim, bukan membuat tuduhan baru pada orang nyata.
- **[H]** Penonton harus pulang membawa: sudut pandang baru, pemahaman baru, satu pertanyaan
  yang tidak nyaman, atau satu kaitan yang tak terduga.

## 2 · Cerita (`STORYTELLING-FONDAMENTAL.md`)

- **[H]** Informasi menjawab "apa yang terjadi"; cerita menjawab "kenapa itu penting".
- **[M]** Ada satu pertanyaan dramatik yang dipegang sampai turn — bukan tiga.
- **[H]** Progresi: pertanyaan → informasi baru → ketegangan/kontradiksi → sudut pandang baru.
- **[H]** Setiap babak harus mengubah pemahaman penonton, bukan menambah daftar fakta.

## 3 · Hook (`HOOK ENGINEERING.md` + `00E` §6)

- **[M]** Satu pintu per episode: pertanyaan / pernyataan / fakta / harapan / khayalan / adegan / dialog.
- **[M]** Tidak dibuka dengan tahun atau angka.
- **[M]** Hook ≤ 12 kata (batas keras 14), satu tarikan napas.
- **[M]** Kalimat pertama berupa pertanyaan atau fakta yang bisa dicek.
- **[M]** Ada satu entitas konkret yang disebut di hook (benda/orang/tempat yang bisa ditunjuk).
- **[H]** Tidak ada sapaan, perkenalan kanal, ringkasan berita, atau "jangan lupa subscribe" di awal.
- **[H]** Janji hook harus ditepati naskah; kalau tidak, ganti hook, bukan tambah drama.
- **[H]** 0–3 s: pengamatan mengejutkan. 3–6 s: ketegangan. 6–10 s: arah cerita.

Enam kegagalan yang dilarang: pembuka generik ("belakangan ini sedang ramai…"), clickbait
kosong, drama berlebihan tanpa bukti, bahasa filosofis palsu, rentetan pertanyaan tanpa
perkembangan, tuduhan tanpa dasar.

## 4 · Ketegangan & retensi (`NARRATIVE-TENSION-&-AUDIENCE-RETENTION.md`)

- **[H]** Ketegangan berasal dari **kesenjangan**: yang diketahui penonton vs yang diketahui tokoh.
- **[H]** Satu loop utama; loop kecil boleh, tapi harus ditutup atau diwariskan ke episode lain.
- **[H]** Eskalasi: setiap belokan harus membuat posisi tokoh lebih sempit, bukan lebih ramai.
- **[H]** Jangan menahan informasi dengan cara menipu; tahan dengan cara **mengurutkan**.

## 5 · Emosi & pacing (`EMOTIONAL-PACING.md`)

- **[M]** Maksimal 2 kalimat per beat (hook/loop maksimal 3).
- **[H]** Kontras menciptakan ritme: tenang → pukulan pendek → tenang lagi.
- **[H]** Jeda dipakai di tempat yang bermakna (sebelum pembalik, sesudah satu fakta berat),
  bukan setelah setiap kalimat.
- **[M]** Tidak ada kata pengisi (`sangat`, `ternyata`, `sebenarnya`, `mungkin`, …).
- **[H]** Jangan berteriak di setiap baris; baris paling menakutkan biasanya yang paling tenang.

## 6 · Penutup (`MEMORABLE-ENDING.md`)

- **[M]** Loop memanggil kembali kata/benda dari hook (echo), bukan merangkum.
- **[H]** Pilih satu teknik: pergeseran sudut pandang, kesadaran yang tidak nyaman,
  pertanyaan terbuka, kaitan tak terduga, atau kalimat yang bisa diulang.
- **[H]** Dilarang menutup dengan ringkasan ("begitulah kisahnya", "sampai sekarang masih misteri").
- **[M]** Frasa ringkasan dilarang (`sampai hari ini`, `hingga kini`, `banyak teori`, …).

## 7 · Bahasa Indonesia manusia (`NATURAL-INDONESIAN-WRITING-HUMAN-VOICE.md`)

- **[M]** Minimal tiga kalimat menyapa penonton (`kamu`/`kita`).
- **[M]** Minimal dua ajakan melihat (`lihat`, `bayangkan`, `coba`, `ingat`).
- **[M]** Minimal dua pertanyaan di seluruh naskah.
- **[M]** Tanpa kosakata laporan (`tersebut`, `adapun`, `sebagaimana`, `diketahui bahwa`, …).
- **[H]** Baca keras. Kalau lidah tersandung, kalimatnya belum selesai.
- **[H]** Satu ide per klausa; koma untuk mengelompokkan, titik untuk menutup.

## 8 · Suara & TTS (`AUDIO PRODUCTION.md` + `elevenlabs-tts-2026/`)

Naskah → suara, aturan yang mengikat:

- **[M]** Teks yang diucapkan bersih dari markup: tanpa `<tag>`, tanpa `[tag]`, tanpa `**`,
  tanpa penomoran daftar, tanpa emoji.
- **[M]** Tidak ada SSML. Model v3/v4 memakai tag kurung siku; kita **tidak memakai tag sama
  sekali** — naskah kanal ini mengandalkan tanda baca dan urutan kalimat.
- **[M]** Singkatan ditulis lengkap; angka dipastikan terbaca benar (uji dengan satu kalimat).
- **[H]** Baseline selalu "tanda baca saja"; tag/penekanan hanya kalau terbukti perlu setelah
  perbandingan A/B pada voice yang sama.
- **[H]** Jeda presisi (mis. 1 detik) dibuat di timeline editor, bukan dikarang dari koma.
- **[H]** Satu suara untuk seluruh kanal (`tools/voice.json`), settings tidak diubah tanpa uji A/B.
- **[H]** Mix: VO paling jelas → efek penting → musik → ambience. Tidak ada musik yang bersaing
  dengan frekuensi suara.

### Catatan lapangan (bukan dari dokumen, dari produksi kanal ini)

- **Suara kanal: Denas — High class catchy storyteller (`arwfiAiEfIHHZCwcYYx2`).** Konsistensi
  suara dibuktikan dengan `tools/voice_consistency.py`; segmen yang menyimpang >18% F0 ditolak.
- **Model kanal: `eleven_turbo_v2_5`, speed 0.85.** Bukan pilihan selera: `eleven_multilingual_v2`
  terbukti mengambil 203–219 kata/menit pada kalimat 12 kata dan **mengabaikan `speed`**
  (berkas byte-identik pada dua nilai speed berbeda). Turbo v2.5 @0.85 = 142 wpm dan
  pertanyaan berakhir naik. Diukur dengan `tools/speech_prosody.py`, 14 Nov 2026.
- **Jeda di dalam satu berkas bukan milik kita.** Model yang menaruhnya. Karena itu jeda
  dikendalikan dengan memecah naskah menjadi satu breath group per segmen, lalu mengatur
  `GAP` di timeline — bukan dengan menambah koma atau elipsis.
- **Tempo dikoreksi setelah rekam.** Target 138 wpm; kalau menyimpang >10%, diterapkan
  `atempo` per segmen (pitch tetap). Model tidak bisa dipercaya untuk soal tempo.
- **Bed −32 LUFS, volume 0.85.** Backsound yang menutupi kata adalah kesalahan produksi,
  bukan selera.
- **Tidak ada unggahan tanpa persetujuan pemilik** (`"approved": true` pada berkas antrean).
- **Setiap rekaman diukur, bukan dikira.** `python3 tools/speech_prosody.py EPxx` mencetak
  wpm, jeda ≥140 ms, dan arah nada 300 ms terakhir. Target: 120–160 wpm, tanpa jeda
  ≥400 ms di tengah frasa, pertanyaan tidak jatuh di bawah −1,5 semit.
- Kunci API kanal hanya berizin `text_to_speech`; metadata voice tidak terbaca. Jangan
  membangun alur yang bergantung pada `/voices` atau `/user`.
- `speed` 1.00 menghasilkan ±140 kata/menit pada naskah kanal (target 135). Kalau perlu lebih
  tenang, ubah `settings.speed` ke 0.96 dulu — jangan mengubah tempo dengan menambah kata.
- Durasi nyata per segmen menentukan caption; selalu jalankan `build_timing.py` sesudah rekam.

## 9 · Gambar, gerak, sunting

- **[H]** `VISUAL-STORYTELLING.md`: gambar menjelaskan posisi, bukan menghias. Satu plate = satu
  informasi baru.
- **[H]** `IMAGE-GENERATION.md`: art direction ditulis sebelum prompt (gaya, palet, cahaya,
  komposisi, rasio); prompt produksi menyebut lensa/ruang/jarak, bukan kata sifat.
- **[H]** Tidak ada wajah korban yang dikarang. Rekonstruksi memakai benda, ruang, jejak.
- **[H]** `ANIMATION&MOTION.md`: setiap gerak harus menjawab "apa yang berubah dan apa yang
  harus penonton lihat".
- **[H]** `VIDEO_&_EDITING.md`: potongan mengikuti beat audio nyata, bukan feeling; caption
  selesai dibaca dalam ±1,5 detik.

## 10 · Alat & QC (`TOOL-ORCHESTRATION.md`)

- **[H]** Urutan alat tidak boleh dibalik: teks → gerbang → gambar → suara → timing → render → tayang.
- **[H]** Setiap alat punya satu keluaran yang bisa diperiksa; kalau gagal, berhenti dan baca
  pesannya, jangan mengulang perintah yang sama.
- **[M]** Sebelum render: `check_story.py` LULUS, semua segmen `measured`, `sfx.wav`/`bed.wav` ada.
- **[M]** Sebelum tayang: master −14 LUFS ±0,5 dan true peak ≤ −1,5 dBTP, sha256 tercatat.

## 11 · Catatan penyimpangan

Tempat mencatat kalau praktik berbeda dari dokumen, supaya tidak jadi kebiasaan diam-diam:

| tanggal | dokumen | penyimpangan | alasan |
|---|---|---|---|
| 2026-11-14 | `elevenlabs-tts-2026` (v4) | memakai `eleven_turbo_v2_5` @ speed 0.85, bukan v4 | v4 tidak mendukung `speed`; tempo 187 wpm terlalu cepat. Turbo v2.5 memberi kendali tempo yang dibutuhkan |
| 2026-11-14 | `AUDIO PRODUCTION.md` §5 (marker `[PAUSE]`) | tidak memakai marker | bagian dari aturan "tanpa tag": jeda dibuat dengan memecah segmen |
| 2026-11-14 | `AUDIO PRODUCTION.md` §5 (marker `[PAUSE]`) | tidak memakai marker | tag tidak deterministik & terbaca sebagai kata pada sebagian model |


## Aturan performa Shorts (16 Nov 2026)

Data kanal: berhenti di ~1.000 tayangan, *stayed to watch* 57,9%, durasi 59–73 dtk,
shares 0. Kesimpulan yang mengikat produksi:

1. **35–45 detik.** Di atas 60 dtk hampir tidak diputar ulang; persentase tontonan
   tidak akan melewati 100%.
2. **Hook di frame nol.** Narasi mulai ≤0,15 dtk; cover 0,5 dtk; tidak ada jeda
   pembuka, tidak ada teks yang muncul pelan.
3. **Pernyataan boleh jadi hook** asal menyebut benda konkret di kalimat pertama.
4. **Penutup = pertanyaan terbuka** supaya komentar muncul; itu satu-satunya sinyal
   yang bisa mendorong video keluar dari fase uji.
5. **Jeda 0,22 dtk**, tempo bicara dijaga cepat; kalau satu segmen >170 wpm, pecah
   kalimatnya.
6. **Suara kanal = narator internal `ojz6ro9PB1xDu44lymdM`** (dikembalikan 16 Nov 2026).
   Setelan Denas, `polish`, dan atempo dihapus. Konsistensi tetap wajib diukur.

## 12 · Serah-terima master (WAJIB, 15 Nov 2026)

Permintaan pemilik, sudah diulang berkali-kali: **setiap video yang selesai
di-build wajib diunggah ke Drive di sesi yang sama.** Render lokal yang belum ada
di Drive bukan hasil kerja — belum jadi.

- **[H]** Unggah ke folder **`video ready`** — id folder `1fVoOvZgiYB3V7S2C5LfMrCpo-c4Xxzo2`.
- **[H]** Nama berkas `EPxx_1080x1920_master.mp4`, satu nama per episode.
- **[H]** Render yang digantikan diganti nama (`..._v1-plate.mp4`), tidak dihapus.
- **[H]** Catat id Drive di `11_CONTENT/04_VIDEO_READY/MASTER_UPLOAD.md`.
- **[M]** `python3 tools/check_master_upload.py` harus keluar dengan status 0
  sebelum sesi ditutup.

Laporan ke pemilik tanpa tautan Drive = belum selesai.

## 13 · Narasi milik user (WAJIB, 16 Nov 2026)

Pemilik membuat VO sendiri untuk sebuah episode, malam-malam, lalu menemukan
render-nya memakai suara lain. Itu kesalahan produksi, bukan selera: **VO yang
sudah dibuat pemilik adalah sumber kebenaran, dan tidak boleh digantikan.**

- **[H]** Kalau episode punya VO dari pemilik, **jangan membuat TTS untuk episode
  itu**, jangan memecah berkasnya, jangan menyusun ulang kalimatnya. Yang dipakai
  hanya berkas itu.
- **[H]** Penyimpanan: `10_FILM/remotion/public/audio/<EP>/vo.mp3` + `vo.srt`
  (SRT pemilik, apa adanya) + `MANIFEST-VO.json` (sumber, byte, detik, sha256,
  peta cue → segmen). sha256 wajib dicatat; kalau berkas berubah, catatannya
  diperbarui, bukan dibiarkan.
- **[H]** Timing diambil dari cue SRT pemilik, bukan dari hitungan kata:
  `content_data.py` menyimpan `vo=dict(file=..., srt=..., cues=[(part, teks,
  mulai, selesai)])`. Batas antar segmen **disnap ke jeda hening nyata** di berkas
  (silencedetect), supaya caption tidak meleset. Tidak ada lead-in dan tidak ada
  jeda 0,22 dtk buatan — durasi episode = durasi berkas + ekor 0,9 dtk.
- **[H]** `Episode.tsx` memutar satu trek (`tm.vo`) dari frame 0. Jangan
  mengembalikannya ke satu-potong-per-segmen untuk episode bermode VO.
- **[H]** Audio lama yang topiknya sudah diganti **dipindahkan** ke
  `public/audio/_arsip/<EP>_<topik>/`, tidak dibiarkan di folder episode. Kalau
  tidak, render berikutnya bisa memakai audio dari cerita yang salah.
- **[H]** Gerbang sebelum render: `python3 tools/check_film_assets.py <EP>` harus
  keluar 0. Skrip itu membandingkan teks di `MANIFEST.json`/`MANIFEST-VO.json`
  dengan naskah, dan memeriksa sha256 VO. Kasus EP09 (audio Somerton Man di
  episode Danau Kenanga) lolos dari semua hitungan berkas; sekarang tidak bisa
  lolos lagi.

### Mengambil berkas dari Drive

Sandbox kerja tidak bisa menghubungi `drive.google.com`; `api.github.com` bisa.
Jalur yang dipakai (dan harus dipakai lagi):

1. Taruh `drive-requests/<nama>.json` → `{"file_id": "...", "name": "VO-EPxx.mp3"}`.
2. Push. Workflow `drive-fetch.yml` (push-triggered) mengunduh berkas lalu
   meng-commit ke branch `drive/inbox`.
3. `git fetch origin +refs/heads/drive/inbox:refs/remotes/origin/drive/inbox` lalu
   `git show origin/drive/inbox:drive-inbox/<nama> > <tujuan>`.
4. Berkas Drive harus "siapa saja yang punya tautan" selama job berjalan; izin
   itu dicabut lagi setelah berkas diambil (`make_private`).

`workflow_dispatch` tidak bisa dipakai dari sesi ini (token tanpa izin Actions
write, ditolak 403). Karena itu jalurnya lewat push.

## 14 · TikTok lewat Zernio (16 Nov 2026)

Akun TikTok kanal sudah tersambung di Zernio, jadi TikTok tidak lagi menunggu
Buffer atau klik manual:

- **[H]** Posting TikTok: antrean `06_UPLOAD/queue/<EP>-tiktok.json` dengan
  `"tiktok_only": true`, `"approved": true`, status `requested` → push.
  Runner menjalankan `upload_zernio.py --tiktok-only`.
- **[H]** Caption TikTok diambil dari `tiktok_caption` di `06_UPLOAD/<EP>.json`
  (≤150 karakter + 3–5 hashtag, aturan `02_SCRIPT` untuk TikTok).
- **[H]** Video dan cover yang dipakai **sama** dengan master YouTube; jangan
  membuat render khusus TikTok.
- **[H]** Setelah tayang, catat `tiktok_url` di `published.json` dan di
  `06_UPLOAD/<EP>_tiktok.md`.
- **[M]** Kalau `published.json` sudah memuat `tiktok_post_id` untuk episode itu,
  tool melewati unggahan berikutnya (pakai `force` hanya untuk salinan uji).

Buffer (`publish.yml`) tetap ada untuk Facebook Reels, tetapi tidak dipakai
untuk YouTube/TikTok lagi.

## 15 · Desain informasi (NERROR, 16 Nov 2026)

Dipelajari dari Nessie Judge/NERROR lalu diterjemahkan ke Shorts: detail di
`SKILLS/15_NERROR_INFO_DESIGN.md`, diperiksa `tools/check_info_design.py` (cek A–G).

- **[M]** `A` Beat ketiga memuat tanggal/bulan + tempat. Hook tetap tanpa tahun.
- **[M]** `B` Kata putusan (`berarti`, `terbukti`, `jadi jelas`, `seharusnya`,
  `sudah pasti`) tidak boleh muncul sebelum beat `turn`.
- **[M]** `C` Kesimpulan hanya di `turn`, dan ada yang mengatakannya
  (`bilang`/`menurut`/kutipan). Tidak ada putusan baru setelah `turn`.
- **[M]** `D` Ada `celah`, dan `celah` **tidak dijawab** di naskah. `loop` berupa
  pertanyaan; caption TikTok memuat pertanyaan yang sama.
- **[M]** `E` `turn` memuat klaim resmi **dan** lawan klaimnya (`bukan … tapi`);
  sintesa kanal ditulis di `turn_verdict`, bukan diucapkan dua kali.
- **[M]** `F` Minimal tiga beat berisi angka/tanggal/jarak/nominal, dan setiap
  angka di VO punya pasangan di `cues`, `stamps`, atau caption.
- **[M]** `G` Minimal dua sapaan `kamu/kita`; dilarang menuduh mutlak
  (`pelakunya adalah …`) tanpa atribusi.
- **[H]** Tidak ada fakta baru setelah `turn`. Kalau ada, pindahkan ke `tension`.
- **[H]** Episode dengan VO pemilik: teks tidak diubah. Mekanisme A–G dieksekusi
  di `cues`, `stamps`, `turn_verdict`, caption, dan deskripsi (lihat §13).
- **[H]** Yang tidak ditiru: horor/mistis, campur bahasa Inggris, judul berteriak,
  spekulasi tanpa sumber. Genre boleh sama; register tidak.

Skor 15 Nov 2026: rata-rata 4,95/7 dari 21 naskah. Yang paling sering gagal: `E`
(9/21) dan `F` (5/21) — klaim tanpa lawan, dan episode tanpa angka.

## 16 · Gerbang topik & tangga kualitas (16 Nov 2026)

Keluhan pemilik: yang salah bukan bahasanya, tetapi **topiknya**. Aturan yang
mengikat mulai sekarang — detail di `SKILLS/16_TOPIK_DAN_KURIKULUM.md`.

- **[M]** Setiap kandidat topik ditulis sebagai kartu di
  `11_CONTENT/01_IDEA/topik_kandidat.json` dengan 12 indikator (0–2). Wajib lulus
  `python3 tools/score_topic.py --strict` (skor ≥17, ada kejanggalan/dua pihak,
  `dokumen_primer` ≥1, `kelangkaan` ≥1, etika aman).
- **[H]** Selama kemampuan POV belum L4, **hanya tier `misteri` dan `kontroversi`**
  yang boleh masuk. Tier `umum` (fakta alam, budaya, wisata) ditahan; tier
  `peristiwa` satu per satu sebagai latihan.
- **[H]** Empat dari delapan tanda "akan membosankan" (daftar di dokumen §3) = tolak
  sebelum menulis, bukan sesudah render.
- **[H]** Setiap episode wajib punya field `tier`, `fokus`, dan `perbaikan` di
  `content_data.py`. `perbaikan` = kelemahan episode sebelumnya yang ditutup.
  Tanpa itu, episode tidak dibangun.
- **[H]** Satu episode satu keterampilan (L1–L8). Dua sekaligus = tidak ada yang naik.
- **[H]** Tidak ada naskah sebelum dokumen primer dibaca. `dokumen_primer` di kartu
  topik hanya janji; `sumber` di `content_data.py` adalah bukti bahwa ia dibaca.
- **[H]** Topik yang sudah padat di YouTube (Flannan, Dyatlov, Mary Celeste, Roanoke,
  Isdal Woman) **tidak diulang**. Yang sudah tayang tetap jadi arsip, bukan contoh.

Status 15 Nov 2026: 6 slot diganti (EP12, EP14, EP16, EP18, EP19), 2 ditahan
(EP13, EP20), 5 kandidat lolos gerbang (T01–T05).

