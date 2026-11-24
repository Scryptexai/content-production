# SKILLS — apa yang dibaca sebelum menulis episode

Direktori ini adalah **kitab kerja** kanal. Isinya dua sumber:

1. Dua belas dokumen pengetahuan di root repo (`HOOK ENGINEERING.md`, `AUDIO PRODUCTION.md`,
   `STORYTELLING-FONDAMENTAL.md`, dst.) — dari pemilik, tidak diubah isinya.
2. `elevenlabs-tts-2026/` — skill pack TTS (v4) yang di-commit 14 Nov 2026.

Ditambah tiga berkas ringkas yang mengikat keduanya ke pipeline yang benar-benar
jalan di repo ini: `AGENTS.md`, `WORKFLOW.md`, `00_RULEBOOK.md`.

## Urutan baca (jangan dibalik)

| # | berkas | gunanya |
|---|---|---|
| 1 | `SKILLS/AGENTS.md` | kontrak: apa yang boleh dan tidak boleh dilakukan |
| 2 | `SKILLS/WORKFLOW.md` | urutan kerja + serah-terima antar tahap |
| 3 | `SKILLS/00_RULEBOOK.md` | aturan yang **diperiksa mesin** dan yang diperiksa manusia |
| 4 | dokumen root sesuai kebutuhan tahap (tabel di bawah) | teori & contoh |
| 5 | `SKILLS/elevenlabs-tts-2026/SKILL.md` + `PUNCTUATION.md` + `QA_RUBRIC.md` | sebelum narasi direkam |
| 6 | `ODDCHAPTER_BRAND/11_CONTENT/00B`, `00C`, `00E` | aturan internal kanal (sudah lebih tua & lebih ketat) |
| 7 | `SKILLS/15_NERROR_INFO_DESIGN.md` + `tools/check_info_design.py` | desain informasi: kronologi → petunjuk → klaim vs bukti → celah terbuka |
| 8 | `SKILLS/16_TOPIK_DAN_KURIKULUM.md` + `tools/score_topic.py` | gerbang topik (12 indikator), uji POV, tangga kualitas L1–L8 |

Kalau dokumen root bertabrakan dengan `00B`/`00C`/`00E`, **yang menang adalah
`00B`/`00C`/`00E`**, karena di situlah gerbang otomatis (`tools/check_story.py`)
dipasang. Dokumen root adalah bahan pemikiran; 00B/00C/00E adalah undang-undang.

## Peta dokumen root → tahap produksi

| tahap | dokumen | yang diambil |
|---|---|---|
| pilih & Tajamkan ide | `EDITORIAL-FONDATION.md` | identitas editorial, standar kemanusiaan, integritas fakta/opini |
| susun cerita | `STORYTELLING-FONDAMENTAL.md` | informasi vs cerita, progresi pemahaman |
| buka | `HOOK ENGINEERING.md` | 7 arketipe hook, 10 detik pertama, 6 kegagalan umum |
| tahan | `NARRATIVE-TENSION-&-AUDIENCE-RETENTION.md` | loop, janji, eskalasi |
| atur napas | `EMOTIONAL-PACING.md` | tingkat intensitas, kontras, jeda, kegagalan pacing |
| tutup | `MEMORABLE-ENDING.md` | 5 teknik penutup, punchline, kegagalan penutup |
| tulis kalimatnya | `NATURAL-INDONESIAN-WRITING-HUMAN-VOICE.md` | bahasa ngobrol, ritme, anti-bahasa koran |
| gambar | `VISUAL-STORYTELLING.md` | bahasa visual, komposisi, urutan gambar |
| aset gambar | `IMAGE-GENERATION.md` | art direction, prompt produksi, konsistensi |
| gerak | `ANIMATION&MOTION.md` | makna gerak, kamera, lapisan |
| sunting | `VIDEO_&_EDITING.md` | potongan, ritme, transisi |
| suara | `AUDIO PRODUCTION.md` | arah VO, konsistensi suara, hierarki mix |
| alat & QC | `TOOL-ORCHESTRATION.md` | urutan alat, kegagalan, audit akhir |
| naskah → TTS | `elevenlabs-tts-2026/` | tanda baca dulu, tag minimal, tanpa SSML, QA dengar |

## Yang tidak ada di kitab ini, dan tetap wajib

- `ODDCHAPTER_BRAND/11_CONTENT/00E_SUARA_NARATOR.md` §1–§7 — suara kanal, tujuh pintu hook,
  dan identitas suara `ojz6ro9PB1xDu44lymdM`.
- `ODDCHAPTER_BRAND/tools/voice.json` — satu-satunya tempat id suara disimpan.
- `ODDCHAPTER_BRAND/tools/check_story.py` — gerbang lima efek + gerbang TTS.
- `ODDCHAPTER_BRAND/11_CONTENT/00C_MESIN_5_EFEK.md` — lima efek yang harus terasa.

## Referensi skill eksternal (opsional, selalu terakhir)

`SKILLS/EXTERNAL_VIDEO_SKILLS.md` dan `.agents/skills/` berisi referensi eksternal
yang telah diaudit dan dipin terbatas. Keduanya **hanya** dibaca setelah urutan di
atas dan tidak boleh mengubah gerbang kanal. Lihat dokumen tersebut untuk izin,
lisensi, commit sumber, serta larangan API/dependensi/renderer eksternal.

## Aturan pemeliharaan

- Dokumen root tidak disunting tanpa perintah pemilik; kalau ada yang bertentangan
  dengan praktik, catat di `00_RULEBOOK.md` §9 (catatan penyimpangan), bukan di file aslinya.
- `elevenlabs-tts-2026/` juga tidak disunting. Pengalaman lapangan (mis. "v2 lebih stabil
  untuk Bahasa Indonesia pada voice ini") masuk ke `00_RULEBOOK.md` §8.
- Setiap episode baru: baca `AGENTS.md` → `00_RULEBOOK.md` → tulis → `check_story.py` → baru rekam.
