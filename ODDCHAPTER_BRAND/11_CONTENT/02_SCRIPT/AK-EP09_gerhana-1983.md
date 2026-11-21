# AK-EP09 — Gerhana 1983: negara menyuruh semua masuk rumah (naskah = VO pemilik)

Sumber ide: Drive `ODDCHAPTER Shortlist Batch 2` (usulan Angker Bot,19 Nov2026),
**peringkat5** — pilihan terakhir dari5 besar; sensitivitas **Rendah** (nada
ganjil, bukan kriminal). Format: adaptasi ODDCHAPTER8 beat.

**VO = VO PEMILIK, dipakai apa adanya** (Drive `gerhana-1983/vo` →
`vo_owner/vo_gerhana-1983.mp3`, **89,12 s,151 kata**, ElevenLabs "Riri Rida -
Documentary & News", alignment faster-whisper). Naskah = transkrip VO;
perubahan hanya perbaikan caption.

END video **93,20 s (1:33)** — durasi bebas1–3 menit.

## Sudut pandang (dari shortlist — wajib dijaga)

Bukan fenomena astronominya, melainkan **ketaatan massal**: perintah Presiden →
TVRI/RRI → aparat desa mengusir warga yang keluar. Ilmuwan LIPI sendiri bilang
"larangan tanpa penjelasan hanya menyesatkan". Akhir: pertanyaan soal
dibandingkan **diperintah bersembunyi vs diajari cara melihatnya**. Nada: ganjil
& membingungkan, bukan menuduh; tanpa teori konspirasi.

## Peta beat → waktu mulai (dari vo_owner/vo_alignment.json)

| Beat | Fungsi | Mulai |
|---|---|---|
| B1 | Dilema —11 Juni1983, tengah hari jadi malam, semua masuk rumah | 0,00 |
| B2 | Reaksi — peringatan Soeharto/Menpen lewat TVRI & RRI: jangan menatap, bisa buta | 11,54 |
| B3 | Tindakan Mengagetkan — rakyat patuh: jendela, lubang angin, mata sapi, perkutut, hamil kolong | 24,34 |
| B4 | Pertaruhan — aparat menyuruh masuk lagi;20 teropong disita | 39,48 |
| B5 | Tekanan — astronom justru datang menyaksikan; rakyat hanya TVRI | 46,88 |
| B6 | Tekanan — ayah Semarang menatap langsung, penglihatan hilang1 jam | 58,90 |
| B7 | Hasil & Fakta — Yogyakarta:446 periksa mata,14 peradangan; kritik LIPI | 67,06 |
| B8 | Interactive Debate Hook — "diperintah bersembunyi… bukan diajari cara melihatnya?" | 79,68 (selesai88,64) |

## Teks VO (transkrip pemilik — sumber caption)

> Sebelas Juni, seribu sembilan ratus delapan puluh tiga. Tengah hari di Jawa
> mendadak menjadi malam. Dan semua orang sudah diperintahkan... masuk rumah.
> Sebulan sebelumnya, Presiden Soeharto memerintahkan Menteri Penerangan
> menyiapkan peringatan lewat TVRI dan RRI. Isinya satu: jangan menatap
> gerhana. Kamu bisa buta. Rakyat patuh. Jendela ditutup rapat. Lubang angin
> disumbat. Mata sapi ditutup kain. Burung perkutut disembunyikan. Di sejumlah
> daerah, perempuan hamil disuruh bersembunyi di kolong tempat tidur. Aparat
> bahkan menyuruh masuk lagi mereka yang berani keluar. Di Jawa Timur, polisi
> menyita dua puluh teropong. Sementara itu, para astronom dari berbagai negara
> datang, justru untuk menyaksikannya. Rakyat hanya boleh menonton lewat
> TVRI... satu-satunya televisi saat itu. Seorang ayah di Semarang ingin
> membuktikan sendiri. Ia menatap langsung. Penglihatannya tak kembali selama
> satu jam. Di Yogyakarta, empat ratus empat puluh enam orang memeriksakan
> mata. Empat belas mengalami peradangan. Ilmuwan LIPI berkata: larangan tanpa
> penjelasan, hanya menyesatkan. Pertanyaannya bukan apakah gerhana berbahaya.
> Tapi kenapa rakyat hanya diperintah bersembunyi... bukan diajari cara
> melihatnya?

## Perbaikan caption (bukan perubahan ucapan)

- `tropong` → **teropong** (ASR; "20" sudah digit) — `WORD_FIX`.
- `satu -satunya` → **satu-satunya** — `MERGE`.
- `di perintah` → **diperintah** — `MERGE`.
- `satu jam` → **1 jam** — `NUM_PHRASES` (11,1983,20,446,14 sudah digit di
 alignment pemilik).
- `KEYWORDS` merah: GERHANA,1983,446.

## Aksesori produksi

- `work/gerhana-1983/`: `vo_owner/` (mp3 + alignment + text + settings),
 `vo_alignment.json` salinan, `footage/` → symlink bank.
- **Aturan21 Nov2026**: semua klip16:9 **cover-crop full layar9:16** (default
 `clip_filter()`, tanpa `window`).
- AI still (tanpa orang): `img/eclipse.jpg` (gerhana total),
 `img/window_shutters.jpg` (jendela kayu tertutup), `img/old_tv.jpg` (TV80-an
 menyala tanpa teks).
- Footage bank: langit malam, kota malam, koran, surat, mata, hujan-jendela,
 jendela senja (sb-ep02), koridor, bayangan, kerumunan, awan (sb-ep02), buku,
 asap, kabut. Klip tak-valid tidak dipakai; tanpa `footage_risiko/`.

## Sumber fakta (shortlist — diverifikasi Angker Bot)

- CNN Indonesia (8 Mar2016) — totalitas ~7 menit, hanya di Jawa, perintah
 masuk rumah, kegiatan berhenti
- Kompas15 Mei1983 (via Tirto10 Jun2022) — Soeharto perintahkan Menpen
 Harmoko siapkan TVRI/RRI
- CNN Indonesia — aparat usir warga keluar (Cepu, Blora); Moedji Raharto:
 "Warga semua patuh"
- ⚠ Angka/istilah: "446 &14" (Yogyakarta) & "20 teropong" (Jatim) dari VO
 pemilik — jangan tambah angka lain di luar VO

## Pemeriksaan editorial

- Tanpa teori konspirasi; kritik dikutip dari ilmuwan LIPI (bukan klaim kita).
- Nada ganjil-bukan-kriminal; tidak menyalahkan rakyat maupun pemimpin secara
 personal berlebihan — fakta perintah disebut apa adanya.
- Footage stok + label di layar + kredit di kartu akhir dan deskripsi.
- VO pemilik dipakai apa adanya.
