# EP05 — MEREKA MENULIS SATU KATA, BUKAN SEBUAH PERINGATAN

**Seri:** HILANG · **Slot:** PAGI 07.00 WIB · **Hari:** H5  
**POV:** D — “KITA” (kolektif; yang dibicarakan adalah asumsi bersama)  
**Durasi:** 123 kata ≈ 50 detik (target 55 s)

---

## 0 · KERANGKA (isi dulu, baru ditulis)

| unsur | isi |
|---|---|
| **Protagonis** | Seratus lima belas orang koloni Roanoke, termasuk seorang bayi bernama Virginia Dare. |
| **Mau** | Bertahan sampai gubernurnya kembali dengan bahan makanan. |
| **Hambatan** | Gubernurnya pergi ke Inggris dan baru bisa kembali tiga tahun kemudian. |
| **Tanaman** (detail yang berubah makna di turn) | Mereka sepakat: kalau pergi karena terpaksa, ukir salib. Di pagar hanya ada satu kata. |
| **Celah** (pertanyaan yang dipegang penonton) | Kenapa mereka menulis nama tempat, bukan tanda bahaya yang sudah disepakati? |
| **Gambar melekat** (satu-satunya yang harus diingat) | Satu kata terpahat di tiang pagar, dan tidak ada salib di atasnya. |

Model ini dari Jon Franklin, *Writing for Story*: komplikasi → gagal → bingung →
wawasan → resolusi. Satu karakter, satu keinginan, satu halangan. Bukan rangkaian fakta.

## 1 · HOOK (0–3 s)

> Rumah dibongkar rapi, bukan dihancurkan. Di pagar: CROATOAN. Tidak ada salib.

Visual: satu objek, tanpa gerak kamera. Teks hook di layar memotong, tidak mengulang VO.

## 2 · BEAT

| bagian | VO |
|---|---|
| SETUP | 1587. Seratus lima belas orang Inggris mendarat di Carolina Utara. |
| SETUP | Gubernurnya berlayar ke Inggris mengambil bahan makanan. |
| TENSION | Perang membuat dia baru bisa kembali tiga tahun kemudian. |
| TENSION | Yang ia temukan bukan koloni. Rumah-rumah sudah dibongkar, bukan dihancurkan. |
| TENSION | Di pagar, terpahat satu kata: CROATOAN. |
| TENSION | Mereka sudah sepakat sebelumnya: kalau pergi karena terpaksa, ukir salib. |
| TURN | Tidak ada salib. |
| TURN | Selama empat ratus tahun kita membaca kata itu sebagai pesan terakhir. |
| TURN | Padahal tidak ada tulang, tidak ada kuburan, tidak ada sisa perkelahian. |
| CONSEQUENCE | Croatoan bukan pesan terakhir. Itu alamat. |
| CONSEQUENCE | Croatoan bukan peringatan. Itu alamat: sebuah pulau lima puluh mil ke selatan. |

## 3 · TURN

Dugaan yang dipatahkan: **“Mereka dibantai.”**

Pembalik: Tidak ada satu pun tulang. Yang ada: nama tempat. Itu alamat, bukan peringatan.

Turn tidak boleh menambah fakta baru. Ia harus mengubah makna sesuatu yang sudah
dilihat penonton sejak detik pertama.

## 4 · ECHO

> Rumah-rumah itu dibongkar rapi karena mereka memang pindah. Seratus lima belas orang berjalan ke selatan.

Kalimat terakhir memanggil kembali detail yang ditanam di hook.

## 4b · KONTRAK LIMA EFEK

| # | efek | perangkat di episode ini |
|---|---|---|
| 1 | berhenti scroll | 11 kata, satu benda konkret, tanpa kata yang meminta |
| 2 | ada yang salah | celah spesifik: _Kenapa mereka menulis nama tempat, bukan tanda bahaya yang sudah disepakati?_ |
| 3 | bertahan | satu loop, ditutup hanya di turn |
| 4 | kejutan | tanaman dibaca ulang, tanpa fakta baru |
| 5 | diingat | gambar melekat + echo kata di penutup |

Gerbang otomatis: `python3 ../tools/check_story.py EP05` (lihat `00C_MESIN_5_EFEK.md`).

## 5 · TEKS DI LAYAR

1. `1587`
2. `115 ORANG`
3. `CROATOAN`
4. `TANPA SALIB`
5. `TANPA KUBURAN`

Maksimal lima cue, 1,5–2 detik masing-masing, huruf kapital, Inter 600.

## 6 · VISUAL SIGNATURE

Pagar kayu dengan satu kata; rumah yang dibongkar rapi; pesisir kosong.

## 7 · DISTRIBUSI

| platform | format |
|---|---|
| TikTok | vertikal 1080x1920, caption <=150 karakter, 3–5 hashtag |
| YouTube Shorts | judul <=60 karakter, deskripsi 2 baris + sumber |
| Facebook Reels | caption 1 kalimat hook + 1 kalimat loop, tanpa link |

Satu episode, tiga platform, satu file master vertikal.

## 8 · SUMBER

`SRC: NEEDS-SOURCE` — Koloni Roanoke 1587–1590; teori asimilasi Croatoan/Lumbee masih hipotesis.

Status `NEEDS-SOURCE` berarti script ini belum boleh tayang sampai rujukan
primernya dibaca dan baris ini diubah jadi `VERIFIED` (lihat `00_STRATEGI.md` §6).

## 9 · HOOK ALTERNATIF (A/B 3 detik pertama)

- Mereka meninggalkan satu kata sebelum pergi. Butuh empat ratus tahun untuk membacanya benar.
---

## Koreksi setelah sumber diperiksa (fase produksi EP05)

Rencana menutup episode ini dengan kalimat "mereka pindah dan bergabung dengan orang
yang sudah ada di sana". Itu **tidak** dikatakan sumber sebagai fakta — ia hipotesis
asimilasi, dan yang bisa dipertanggungjawabkan cuma sampai titik ini:

| yang ditulis rencana | yang bisa dikatakan dari sumber | yang dipakai |
|---|---|---|
| "mereka bergabung dengan penduduk setempat" | hipotesis; bukti pendukung ada (artefak abad ke-16 di Hatteras, Site X di Bertie County 2015), tetapi tidak ada catatan yang menyambung | tidak diucapkan; diganti "itu alamat, lima puluh mil ke selatan" |
| "tidak ada mayat" | benar untuk Roanoke 1590: tidak ada tubuh, tidak ada kuburan, tidak ada tanda pertempuran | dipakai |

Detail yang bertahan dan bisa dicek: 115 orang, John White gubernur, Virginia Dare lahir
18 Agustus 1587, White mendarat kembali 18 Agustus 1590, rumah **dibongkar** bukan runtuh,
palisade baru dibangun, peti yang dikubur sudah digali, barang berat ditinggal,
"CRO" di pohon dan "CROATOAN" di tiang pagar, keduanya **tanpa salib** padahal salib
sudah disepakati sebagai tanda bahaya.

Batasnya: laporan asli White ("The fift voyage of M. John White", Hakluyt) belum dibaca
langsung; semua di atas berasal dari ringkasan sekunder yang saling cocok
(encyclopediavirginia.org, pagesofhistory.org, scienceinsights.org).
