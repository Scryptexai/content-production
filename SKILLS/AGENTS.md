# AGENTS.md — kontrak kerja untuk agen yang mengerjakan kanal ini

Ini bukan generator teks. Ini sistem produksi episode: satu episode = satu klaim
kebenaran + satu pengalaman menonton yang utuh, siap tayang di YouTube Shorts.

Dokumen ini adalah versi yang mengikat untuk repo ini. Versi asli dari pemilik
ada di `AGENTS_upstream.md` (jangan disunting); perbedaannya hanya pada hal-hal
teknis: nama alat, gerbang otomatis, dan bahasa keluaran.

## 0 · Batasan yang tidak bisa dinegosiasikan

1. **Bahasa deliverable: Indonesia.** Naskah, caption, judul, deskripsi, komentar pertama.
2. **Bukti, bukan janji.** Setiap episode harus punya URL tayang + `post_id`. Tidak ada
   laporan "sudah diunggah" tanpa dua hal itu.
3. **Jangan mengarang.** Fakta, kutipan, angka, dan tanggal harus bisa ditunjuk
   sumbernya (ditulis di field `sumber` pada `tools/content_data.py`). Yang belum pasti
   ditulis sebagai laporan, bukan kepastian.
4. **Jangan ganti suara.** `voice_id` hanya dari `tools/voice.json`
   (`ojz6ro9PB1xDu44lymdM`). Mengganti suara = keputusan pemilik.
5. **Tanpa PR, tanpa merge.** Kerja berhenti di commit + push branch sesi.
6. **Tayang langsung.** Antrean unggah memakai `publishNow: true`, bukan jadwal.

## 1 · Urutan kerja (ringkas)

1. Tetapkan brief: topik, genre (seri), durasi target, platform, sumbu cerita.
2. Tegakkan premis: satu pertanyaan dramatik yang harus dijawab episode ini.
3. Tetapkan protagonis/entitas: mau apa, terhalang apa, apa yang dipertaruhkan.
4. Susun beat kausal (00B) — `check_story.py` hanya menerima yang koheren.
5. Tulis dengan suara kanal (00E): menyapa penonton, bukan melaporkan.
6. Terjemahkan ke gambar: 9–10 plate, satu gambar melekat.
7. Audit naskah otomatis + manual (§3), baru rekam.
8. Rekam, ukur, render, tayangkan, catat.

## 2 · Aturan keras

- **Tidak ada kebetulan yang menyelesaikan konflik.** Kebetulan boleh memulai, tidak boleh menutup.
- **Setiap belokan lahir dari keputusan, tanaman sebelumnya, atau tekanan eksternal yang masuk akal.**
- **Karakter tidak menjelaskan hal yang sudah dia ketahui** hanya demi penonton.
- **Jangan memakai templat universal.** Panjang dan genre menentukan bentuk.
- **Jangan mengklaim retensi/views** tanpa data analitik.
- **Konsistensi dijaga lewat `content_data.py`** sebagai story bible: nama, tempat, angka, tanggal.
- **Jangan menandai konten sebagai fiksi** kalau ia nyata — dan sebaliknya: kasus nyata
  ditulis sebagai rekonstruksi ("yang dilaporkan", "menurut arsip"), bukan sebagai adegan saksi.
- **Hook satu pintu.** Satu episode memakai satu jenis pembuka (pertanyaan / pernyataan /
  fakta / harapan / khayalan / adegan / dialog), bukan campuran.
- **Tidak ada tanggal atau tahun di kata pertama hook.**

## 3 · Gerbang yang harus lulus sebelum rekam

```bash
python3 ODDCHAPTER_BRAND/tools/check_story.py EPxx
```

Lulus berarti: lima efek terpenuhi, hook satu pintu, ada entitas konkret, ada ajakan
melihat, penonton disapa minimal tiga kali, dan naskah **aman dibaca mesin suara**
(tanpa markup, tanpa tag, tanpa penomoran).

Audit manusia sesudahnya (tidak bisa diotomatiskan):

| pertanyaan | kalau "tidak" |
|---|---|
| Apakah kalimat pertama membuat orang berhenti karena penasaran, bukan karena jijik? | ganti pintu hook |
| Apakah ada satu benda yang bisa ditunjuk penonton di 3 detik pertama? | tambahkan benda |
| Apakah setiap klaim bisa ditunjuk sumbernya? | turunkan jadi laporan atau buang |
| Apakah ada satu kalimat yang akan diulang orang? | tulis ulang penutup |
| Apakah narasi terdengar seperti orang mengobrol, bukan membaca? | baca keras, potong koma & kata pengisi |

## 4 · Keluaran setiap episode

| berkas | isi |
|---|---|
| `tools/content_data.py` (satu entri) | naskah, beat, cue, stamp, sumber |
| `11_CONTENT/02_SCRIPT/EPxx_*.md` | naskah lengkap untuk dibaca manusia |
| `10_FILM/remotion/public/audio/EPxx/*.mp3` | narasi per segmen (voice kanal) |
| `output/episodes/EPxx_1080x1920_master.mp4` | master siap tayang (−14 LUFS) |
| `11_CONTENT/06_UPLOAD/EPxx.json` + `queue/EPxx.json` | metadata unggah + antrean |
| `published.json` | bukti tayang: URL + `post_id` |

## 5 · Yang paling sering salah (dan sudah pernah terjadi di kanal ini)

1. **Naskah terdengar seperti pembaca berita.** Obatnya ada di `00E` §1 dan
   `NATURAL-INDONESIAN-WRITING-HUMAN-VOICE.md`.
2. **Hook dibuka dengan tahun.** Terlihat rapi, langsung kehilangan rasa mengobrol.
3. **Empat pertanyaan beruntun tanpa jawaban.** Penonton merasa ditanya-tanyai, bukan diajak.
4. **Turn yang menambah fakta baru.** Turn harus mengubah makna yang sudah dilihat,
   bukan menambah informasi.
5. **Penutup berupa ringkasan.** Penutup harus memanggil kembali gambar dari hook.
6. **Visual indah, cerita kosong.** Visual tidak pernah menyelamatkan beat yang lemah.

## 6 · Rujukan

- `SKILLS/WORKFLOW.md` — urutan & serah-terima antar tahap.
- `SKILLS/00_RULEBOOK.md` — ringkasan aturan per dokumen + catatan lapangan.
- `ODDCHAPTER_BRAND/11_CONTENT/00B_STRUKTUR.md`, `00C_MESIN_5_EFEK.md`, `00E_SUARA_NARATOR.md`.
- `SKILLS/elevenlabs-tts-2026/SKILL.md` — naskah → suara.
