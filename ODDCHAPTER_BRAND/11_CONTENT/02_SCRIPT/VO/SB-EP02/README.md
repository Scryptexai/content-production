# SB-EP02 — VO siap tempel ke ElevenLabs

Naskah di folder ini **khusus VO**. Sudah dibersihkan untuk mesin baca: tanpa tanda waktu,
tanpa keterangan kamera, angka ditulis dengan huruf, singkatan diberi spasi (B T O, B F O,
G P S) supaya dibaca sebagai huruf, bukan satu kata.

## Kenapa dipecah sembilan berkas

Total naskah **7.714 karakter** — di atas batas 5.000 karakter per permintaan ElevenLabs.
Karena itu VO dibuat **per segmen** (`VO_01.txt` … `VO_09.txt`), masing-masing 367–1.285
karakter. Ini juga yang membuat Shorts bisa dipotong tanpa memotong kata: setiap berkas
adalah satu segmen utuh di naskah.

| berkas | kata | karakter | ± durasi | fungsi di episode |
|---|---|---|---|---|
| `VO_01.txt` | 56 | 367 | 22 dtk | kail (salah sangka) |
| `VO_02.txt` | 63 | 393 | 25 dtk | batas + kenapa ini tentang penonton |
| `VO_03.txt` | 162 | 1.053 | 65 dtk | malam 8 Maret, detik demi detik |
| `VO_04.txt` | 199 | 1.285 | 80 dtk | tujuh handshake, B T O / B F O |
| `VO_05.txt` | 188 | 1.205 | 75 dtk | tiga gelombang pencarian |
| `VO_06.txt` | 124 | 861 | 50 dtk | tiga serpihan, bagian "kesal" |
| `VO_07.txt` | 144 | 964 | 58 dtk | dua pembacaan + pertanyaan biner |
| `VO_08.txt` | 104 | 695 | 42 dtk | perpanjangan 2026 |
| `VO_09.txt` | 137 | 883 | 55 dtk | penutup + loop ke penonton |

Total ± 7,8–8,7 menit VO; dengan kartu, jeda, dan footage utuh, episode jadi 9–11 menit.
`SB-EP02_VO_FULL.txt` = sembilan segmen digabung untuk pembacaan utuh (jangan dipakai
generate sekaligus — melebihi batas karakter).

## Setelan yang dipakai

- Model: **Eleven Multilingual v2** (v3 hanya kalau suaranya memang dilatih untuk v3).
- Stability 0,45–0,55 · Similarity 0,75 · Style 0 · Speed 0,95–1,0.
- Output **MP3 320 kbps** atau **WAV 48 kHz**; mono lebih aman untuk di-mix ulang.
- Satu segmen = satu generate. **Jangan gabung** dua segmen dalam satu permintaan: batas
  potong Shorts ada di batas segmen.

## Setelah selesai

1. Beri nama hasilnya persis `VO_01.mp3` … `VO_09.mp3` (kalau memakai WAV: `VO_01.wav`).
2. Unggah kembali ke folder Drive ini. Render mengambil VO dari Drive, bukan dari TTS —
   jadi yang masuk video adalah rekaman yang Anda setujui.
3. Kalau ada segmen yang di-generate ulang, **nama berkasnya harus sama**; kalau berubah,
   batas potong Shorts dan penyelarasan kartu ikut bergeser.

## Catatan baca

- Baris kosong = jeda. Jangan dihapus; itu pemisah beat, bukan hiasan.
- Angka sudah ditulis dengan huruf (contoh "dua ribu dua puluh enam") supaya tidak dibaca
  sebagai angka ribuan atau tanggal gaya Amerika.
- Tiga frasa sengaja dibiarkan berbahasa Inggris: `Good night Malaysian three seven zero`
  (kutipan asli kokpit), `no find, no fee` (nama skema kontrak), `Ocean Infinity` (nama
  perusahaan). Jangan diterjemahkan.
- Nada: seperti orang menjelaskan ke teman, bukan pembaca berita. Kalimat pendek memang
  pendek — biarkan tempo jatuh di titik, bukan dinaikkan.
