# Content — 35 konten / 7 hari

Sumber tunggal: **`scripts.json`** (35 entri). Semua file lain di folder ini
dibangkitkan, jangan diedit manual.

> **Catatan:** `relationship/` adalah slate terpisah (v2, mulai 2026-11-09) dengan
> standar editorial baru — 7 naskah riset primer, 1/hari. Ia tidak dibangkitkan dari
> `scripts.json` dan tidak mengubah kalender 105 draf di atas.
> Lihat `relationship/README.md` dan `docs/05-editorial-bible.md`.

```bash
python3 automation/build_schedule.py   # scripts.json → day-*.md, calendar-7-days.md, calendar.json, schedule.csv
python3 automation/validate.py         # QC: 35×3 draf, slot, urutan, panjang caption
```

| File | Isi |
|---|---|
| `scripts.json` | 35 skrip: hook, VO per beat, teks layar, visual, caption, hashtag, sumber, alat |
| `day-01.md` … `day-07.md` | versi baca manusia, 5 konten per hari |
| `calendar-7-days.md` | peta 7 hari × 5 slot |
| `../automation/zernio/content/calendar.json` | 105 draf siap di-approve |
| `../automation/zernio/content/schedule.csv` | lembar kerja (buka di Sheets) |

---

## Aturan naskah

1. **Hook 0–3 detik** harus memuat ketegangan, bukan salam. Tanpa "hai guys".
2. **Satu klaim per video.** Kalau ada dua, pecah jadi dua video.
3. **VO 4–6 beat**, tiap beat = satu ide + satu visual.
4. **Penutup = pertanyaan** yang bisa dijawab di komentar (bukan CTA jualan).
5. **Sumber wajib** untuk setiap angka. Tanpa sumber → hapus angkanya.
6. **Tanpa kata:** glowing, bestie, auto, toxic (untuk orang), wajib punya.
7. Panjang 45–75 detik; di atas 60 detik agar memenuhi syarat Creator Rewards
   bila kelak akun memenuhi syarat lain.

## Library hook (dipakai bergiliran, jangan ulang bentuk)

| Bentuk | Contoh |
|---|---|
| Koreksi mitos | "Krim yang kamu puji di Tokyo bisa jadi lengket di Jakarta." |
| Angka mengejutkan | "SPF 50 bukan 50 kali lebih aman dari SPF 1." |
| Pertanyaan pribadi | "Kalau wajahmu lengket jam 10 pagi, ini penyebabnya." |
| Kontradiksi | "Produk ini lulus uji stabilitas. Tapi ujinya di ruangan 25 derajat." |
| Pengakuan pola | "Kamu sudah tahu harus berhenti setahun lalu." |
| Alat langsung | "Empat pertanyaan ini lebih penting daripada besarnya tabungan." |

## Struktur beat yang dipakai

```
BEAT 1  hook          (0–3 dtk)   satu kalimat, tanpa penjelasan
BEAT 2  mekanisme     (3–15)      kenapa ini terjadi
BEAT 3  bukti/angka   (15–35)     satu angka + sumbernya
BEAT 4  konsekuensi   (35–50)     apa artinya untuk penonton
BEAT 5  alat          (50–65)     pertanyaan / tes / kalimat jeda
```

## Pembagian niche

| Niche | Jumlah | Seri |
|---|---|---|
| Beauty | 21 (3/hari) | Iklim & Tekstur · UV & Pigmentasi · Iklim & Stabilitas · Dasar Bahan · Rutin 3 Langkah |
| Relationship | 14 (2/hari) | Beban Tak Terlihat · Uang & Rumah Tangga · Pola dari Keluarga |

Alasan 3:2 — beauty punya jalur afiliasi lebih cepat (produk fisik),
relationship membangun otoritas & komentar (waktu tinggal lebih panjang).
