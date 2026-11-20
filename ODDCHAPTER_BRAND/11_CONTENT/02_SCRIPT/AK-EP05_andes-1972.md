# AK-EP05 — Batas Terakhir Manusia (Andes 1972, naskah TTS final rev3)

Format: adaptasi ODDCHAPTER 8 beat (`00F_FORMAT_CURIOSITY_LOOP.md` §2).
**REV3 — revisi total sudut pandang (koreksi pemilik):** naskah tidak lagi
"laporan kronologis" (angka kering, urutan peristiwa), melainkan **dilema batin
penonton** — penonton dibawa ke posisi sang tokoh: akal sehat vs naluri bertahan
hidup, format kuis/laporan → konflik psikologis langsung, dan penutup memaksa
sikap ("kamu ikut makan atau mati mempertahankan prinsip?").

VO: TTS internal voice-05, **8 klip** → `build_vo.py` → **87,31 s (180 kata);
END video 91,40 s (1:31)**. Kode waktu 00:00–00:60 pada naskah kreatif pemilik
adalah penanda beat; durasi final mengikuti keputusan pemilik (bebas 1–3 menit)
agar **setiap kalimat utuh, tidak dipersingkat**.

## Peta beat → klip (waktu mulai final dari vo_alignment)

| Beat | Fungsi | Klip | Mulai |
|---|---|---|---|
| B1 | Question Hook — tantangan langsung | vo_01 | 0,00 |
| B2 | Expected Answer — reaksi alami | vo_02 | 4,65 |
| B3 | Expectation Break — patahan keyakinan (radio) | vo_03 | 10,75 |
| B4 | Open Loop — pertaruhan nyawa | vo_04 | 15,72 |
| B5 | The Journey — tekanan situasi nyata | vo_05 | 25,38 |
| B6 | Progressive Reveal — momen perjanjian moral | vo_06 | 51,30 |
| B7 | Final Reveal & Payoff — hasil pengorbanan | vo_07 | 64,71 |
| B8 | Interactive Debate Hook — pancingan komentar | vo_08 | 74,68 (selesai 87,31) |

## Teks VO per klip (sumber TTS — sama persis dengan SEGS build_vo.py)

**vo_01 — Question Hook (0,00)**
> Berapa hari kamu sanggup menahan lapar sebelum melanggar prinsip moral terbesarmu?

**vo_02 — Expected Answer (4,65)**
> Kamu pasti merasa lebih memilih mati daripada harus menyentuh jasad sahabatmu sendiri.

**vo_03 — Expectation Break (10,75)**
> Tapi keyakinan itu runtuh begitu kamu mendengar satu siaran radio ini.

**vo_04 — Open Loop (15,72)**
> Di titik itu, mereka tahu tidak ada pahlawan yang datang.
> Pilihannya cuma menyerah, atau melakukan hal yang tak terbayangkan.

**vo_05 — The Journey / Conflict (25,38)**
> Suhu minus tiga puluh derajat.
> Tubuh mulai memakan lemaknya sendiri, otot melemah, dan halusinasi datang.
> Di luar bangkai pesawat, jasad rekan-rekan mereka terawetkan sempurna oleh es.
> Malam itu, di dalam kegelapan kabin yang membeku, perdebatan paling sunyi terjadi.
> Sebagian menangis menolak karena takut dosa.
> Sebagian sadar: menolak makan berarti bunuh diri perlahan.

**vo_06 — Progressive Reveal / Janji (51,30)**
> Bukan paksaan yang mengubah segalanya, melainkan sebuah janji.
> Mereka saling berikrar: jika tubuhku mati malam ini, pakailah ragaku agar kalian bisa pulang menemui keluarga.

**vo_07 — Final Reveal & Payoff (64,71)**
> Pengorbanan kelam itu memberi mereka tenaga.
> Setelah tujuh puluh dua hari dan berjalan kaki menembus dinding es Andes, enam belas orang berhasil pulang hidup-hidup.

**vo_08 — Interactive Debate Hook (74,68)**
> Jika kamu berada di kabin beku itu pada hari kesebelas, apakah kamu akan ikut makan demi pulang, atau memilih mati mempertahankan prinsipmu?
> Tulis pilihan jujurmu di komentar.

## Penyesuaian wajib terhadap naskah kreatif pemilik

- **"Hari ke-10" → hari kesebelas.** Fakta Britannica/Wikipedia: operasi
  pencarian resmi dihentikan 23 Oktober 1972 = hari ke-11 setelah jatuh (13 Okt).
  Berlaku untuk stamp layar B3 dan hook B8.
- **Visual B2 "foto wajah-wajah penumpang" →** `NAIK_PESAWAT` + jendela pesawat
  (tanpa wajah orang — aturan materi AI/stok).
- **Visual B3 "radio kecil di atas salju" →** `KORAN` + pesawat pencari + stamp
  dua baris "HARI KE-11: OPERASI SAR RESMI DIHENTIKAN" (stok Coverr tak punya
  klip radio; koran = metafora siaran/kabar).
- **Visual B7 "helikopter penyelamat" →** pesawat pencari + trek/puncak
  (stok yang tersedia; evakuasi tetap disebut di deskripsi).
- Data kering dihapus dari VO (tak ada nama pesawat, tipe tim, ketinggian
  meter) — fakta teknis tetap di deskripsi & kartu sumber untuk penemuan.

## Catatan produksi

- 8 klip TTS lolos moderasi (voice-05, `language=id`); trim senyap otomatis
  `build_vo.py`; gap antar-beat 0,50 s (B8 0,60 s).
- `NUM_PHRASES`: tiga puluh→30, tujuh puluh dua→72, enam belas→16,
  kesebelas→KE-11. `KEYWORDS` merah: ANDES, 72, 16, 30.
- 24 shot + 23 overlay; `bed_andes.py` hit per beat (B3/B4/B5/B6/B7/B8),
  riser menuju B5, dip kartu penutup. Render ulang penuh 20 Nov (rev3).
- Overlay kunci: KAPAN NURANI MANUSIA MENYERAH? · MEMILIH MATI DARIPADA
  MENYENTUH SAHABAT · HARI KE-11: OPERASI SAR RESMI DIHENTIKAN · TIDAK ADA
  PAHLAWAN YANG DATANG · SUHU MINUS 30° · PERDEBATAN PALING SUNYI ·
  PAKTA DI TENGAH ES · 16 ORANG PULANG HIDUP-HIDUP · MAKAN DEMI PULANG? /
  MATI DEMI PRINSIP? · TULIS PILIHANMU DI KOMENTAR.

## Sumber fakta (untuk kartu sumber & deskripsi)

- Britannica — https://www.britannica.com/event/Uruguayan-Air-Force-flight-571
- Wikipedia — https://en.wikipedia.org/wiki/Uruguayan_Air_Force_Flight_571
- Piers Paul Read, *Alive: The Story of the Andes Survivors* (1974)
- Nando Parrado, *Miracle in the Andes* (2006)
- Pablo Vierci, *La Sociedad de la Nieve* (2008) — dasar film *Society of the Snow* (2023)

## Pemeriksaan editorial

- Tanpa gore, tanpa kondisi jenazah, tanpa detail prosedur, tanpa cara
  kematian eksplisit; "jasad terawetkan es" = fakta, bukan gambaran.
- Angka VO hanya yang disepakati Britannica/Wikipedia (72 hari, 16 selamat,
  hari ke-11, minus 30° lazim dikutip); angka beda sumber tidak dipaksakan.
- "Pencarian dihentikan" = fakta resmi, bukan teori; tanpa teori konspirasi.
- Akhir = dilema sikap penonton (aturan beat8, kunci komentar), bukan penutup
  fakta.
- Footage stok **Coverr Free License** saja, label di layar + kredit di kartu
  akhir dan deskripsi; tidak ada `footage_risiko/`.
