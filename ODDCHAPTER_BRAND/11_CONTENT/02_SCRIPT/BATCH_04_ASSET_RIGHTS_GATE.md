# Batch 04 — gerbang hak aset dan manifest visual awal

**Tanggal pemeriksaan:** 6 November 2026
**Ruang lingkup:** B04-S02, B04-S06, B04-S07, B04-S15, B04-S16
**Status keseluruhan:** `0 ASET CLEARED · JANGAN RENDER · JANGAN BUAT THUMBNAIL / MASTER / QUEUE`

Dokumen ini menerjemahkan hasil review sumber menjadi pagar aset. Ia **bukan**
manifest aset final dan tidak mengizinkan unduhan, screenshot, crop, AI-image,
footage, musik, atau penggunaan ulang. Status `SOURCE READ` selalu berbeda dari
status hak pakai visual.

## Aturan yang berlaku untuk kelima episode

1. Satu aset tidak boleh masuk render hanya karena halaman sumber dapat dibuka.
   Hak penggunaan, credit, dan cara atribusi harus dibuktikan per file.
2. Setiap dokumen/foto arsip harus diperiksa pada halaman hak atau perjanjian
   izin yang berlaku. “Ada di internet”, “edisi tua”, atau “koleksi museum”
   bukan lisensi.
3. Jika visual sintetis kelak disetujui, ia wajib memakai label `ILUSTRASI AI`,
   tidak menyerupai artefak/screenshot sumber, dan tidak menjadi bukti sejarah.
4. Stok/footage masih perlu lisensi dan audit reuse lintas episode; belum ada
   kandidat atau file yang dipilih untuk Batch 04.
5. Tidak ada sumber musik, SFX, thumbnail, peta, footage, scan, atau foto yang
   dinilai cleared dalam dokumen ini.

## Matriks hak menurut episode

| ID | Material sumber yang mungkin menggoda untuk dipakai | Status hak saat ini | Batas visual yang boleh direncanakan saja | Bukti yang masih wajib sebelum aset dibuat/dipakai |
|---|---|---|---|---|
| B04-S02 Cottingley Fairies | Foto peri, kamera, surat Elsie, sketsa dari koleksi Science Museum Group. | **TIDAK CLEARED.** Halaman museum mencantumkan credit © Elsie Wright & Frances Griffiths / Science Museum Group dan © Science Museum Group. | Tipografi orisinal, diagram kamera/pelat generik, dan bentuk cutout abstrak yang tidak meniru foto/anak asli. | Halaman lisensi per objek atau izin tertulis; object ID, credit line, syarat crop/animasi, dan atribusi final. |
| B04-S06 Clever Hans | Foto Hans, von Osten, laporan/ilustrasi buku, atau scan halaman Pfungst. | **TIDAK CLEARED.** Teks primer dipakai sebagai sumber fakta, bukan persetujuan memakai scan/ilustrasi. | Diagram kondisi eksperimen dan siluet kuda non-identifiable buatan orisinal, tanpa menyamarkan sebagai dokumentasi 1904. | Sumber visual berlisensi jelas; bila memakai reproduksi buku, cek status edisi/terjemahan/file spesifik serta hak di negara distribusi. |
| B04-S07 Piltdown Man | Foto tengkorak/rahang, rekonstruksi, plate publikasi 1953, atau objek NHM. | **TIDAK CLEARED.** Halaman NHM/BHL membuktikan klaim, tidak memberi lisensi aset yang dicatat di sini. | Diagram material non-fotorealistik: fragmen dipisahkan, uji bahan, garis bukti. Tidak ada rekonstruksi manusia purba sebagai “bukti”. | Lisensi/credit per objek atau public-domain proof untuk file yang benar-benar dipilih; object ID dan ketentuan BHL/NHM. |
| B04-S15 Hitler Diaries | Scan diary, konferensi pers, logo/simbol/arsip yang mengandung Nazi imagery. | **DILARANG / TIDAK CLEARED.** Bundesarchiv menyatakan reproduksi gambar hanya dengan izin tertulis; batas editorial juga melarang ikonografi Nazi. | Diagram orisinal tentang tiga jalur pemeriksaan, serat kertas generik, dan perbandingan teks abstrak tanpa simbol/quote/scan. | Tidak ada pengecualian visual arsip tanpa izin tertulis dan review etik tambahan. Izin hak tidak menghapus larangan ikonografi. |
| B04-S16 Sokal Affair | Scan artikel *Social Text*, cover jurnal, halaman *Lingua Franca*, atau screenshot situs NYU. | **TIDAK CLEARED.** Halaman web dan artikel adalah sumber fakta; tidak ada hak tampilan/rekaman yang dikonfirmasi. | Tipografi orisinal dan diagram proses submit → baca → respons; tidak boleh terlihat seperti halaman jurnal/arsip asli. | Lisensi tertulis atau ketentuan reuse yang menyebut file spesifik; cek hak penerbit untuk cover/scan dan hak situs untuk screenshot. |

## Proses visual yang boleh disiapkan tanpa memproduksi aset

Setiap visual plan pada lima file skrip hanya boleh diperlakukan sebagai
**brief konseptual**. Sebelum membuat satu file gambar atau meminta footage,
editor harus mengisi dan menyetujui baris manifest berikut untuk tiap kandidat:

| Field manifest | Isi minimum |
|---|---|
| `episodeId` / `assetId` | ID B04 dan ID unik; tidak boleh berbagi ID lintas episode. |
| `beat` / `claimLedgerRef` | Rentang VO dan baris ledger yang dijelaskan; satu aset tidak menambah klaim. |
| `kind` | `original-diagram`, `licensed-archive`, `licensed-stock`, `map`, atau `ai-illustration`. |
| `sourceUrl` / `objectId` | URL dan object ID/file asal yang benar-benar dipakai, bukan homepage koleksi. |
| `rightsStatus` | `PENDING`, `CLEARED`, atau `REJECTED`; tidak ada status implisit. |
| `licenseOrPermission` | Tautan lisensi/izin tertulis, cakupan platform/territory/durasi, dan batas transformasi. |
| `credit` | Baris credit persis seperti yang diminta pemegang hak. |
| `reuseCheck` | Episode/asset set terdahulu yang dibandingkan dan hasilnya. |
| `aiDisclosure` | Jika sintetis: teks label, posisi, dan alasan visual tidak menjadi bukti. |
| `reviewer` / `reviewedAt` | Nama penyetuju dan tanggal; tanpa ini status tetap `PENDING`. |

## Visual-source-document gate

Kebijakan visual merekomendasikan sedikitnya satu dokumen sumber yang sah per
episode. Saat ini **tidak ada** lima episode ini yang memiliki dokumen sumber
berhak pakai. Diagram orisinal berlabel sumber dapat membantu menjelaskan klaim,
tetapi tidak boleh ditandai sebagai dokumen arsip atau dipakai untuk melewati
gerbang source document. Bila tidak ada dokumen berlisensi jelas, episode tetap
tertahan sampai pemilik/editor memberi keputusan yang kompatibel dengan kebijakan
visual dan hak.

## Kriteria keluar dari gerbang

Semua syarat berikut wajib dipenuhi per episode, bukan sekali untuk batch:

- setidaknya satu manifest aset telah direview dengan `rightsStatus: CLEARED`;
- tidak ada aset yang melanggar batas etika/representasi dalam file skrip;
- klaim pada layar dapat dilacak ke ledger dan tidak lebih spesifik dari VO;
- audit reuse menunjukkan tidak memakai footage/still episode lama;
- untuk peta, sumber dan lisensi peta spesifik juga dicatat terpisah;
- VO final, caption timing, dan persetujuan naskah tetap merupakan gerbang
  sendiri setelah hak aset.

Sampai kondisi itu terpenuhi, tidak boleh ada komposisi Remotion Batch 04,
render, master, thumbnail, Drive verification, metadata unggah, atau request
queue. Semua slot Batch 04 tetap `DO_NOT_QUEUE`.
