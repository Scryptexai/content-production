# LF04 · provenance visual dan timing

**Status:** aset produksi dibuat sebagai diagram SVG original; tidak memakai foto, footage, scan arsip, korban, atau rekonstruksi fotorealistik. Setiap plate merujuk ke keluarga sumber yang sama dengan `SOURCES.md`. Master final lulus QC sebagai H.264 1920×1080/30 fps `yuv420p`, AAC stereo 48 kHz, **20.231 frame**, dan 674,366667 detik; SHA-256 `41044439821a7700d460fbfa978d42be7ab44c3f02402169a99fd19fd93e5b3c`. Satu frame terminal diklon tepat dari visual Remotion untuk menutup perbedaan pembulatan proxy 6 fps tanpa interpolasi.

## Audio

- Narator: `voice-09`, Indonesian feminine, disintesis dalam delapan proses berurutan (pembuka dibagi menjadi dua karena filter penyedia).
- Berkas kontigu: `work/tambora/vo_internal/LF04_Tambora_voice-09_contiguous.wav`
- Durasi suara: **674.360 detik** / **11.24 menit**, tanpa time stretch.
- SHA-256 voice kontigu: `579b22673c6afc9130bcd62e1d925c28a11dc0b9207dd645f1a877f44e5885c4`.
- Dua bagian pembuka memakai parafrasa TTS-minimal yang menjaga arti naskah: “satu kotak ekskavasi” menggantikan “sebuah kotak”, dan struktur kalimat disederhanakan agar lolos filter. Tidak ada klaim, angka, atau batas editorial baru.

## Visual

- Renderer: `@remotion/renderer`; semua visual utama adalah SVG hasil desain internal di `10_FILM/remotion/public/lf04/`.
- Peta/koneksi adalah skema konseptual, bukan peta navigasi dan bukan jalur fisik material.
- Source labels menyatakan **keluarga sumber**, bukan menyamar sebagai halaman arsip primer yang tidak digunakan sebagai aset.
- Tidak ada angka korban tunggal, tidak ada “kota beku”, dan tidak ada visual pengalaman korban.

| plate | label | sublabel | keluarga sumber | provenance |
|---|---|---|---|---|
| `01-01.svg` | TIGA LAPISAN | lingkungan laut lebih tua | BRIN 2024 | original SVG · layers-old |
| `01-02.svg` | LIMA LAPISAN | material piroklastik · 1815 | BRIN 2024 | original SVG · layers-new |
| `01-03.svg` | DORO BENTE | satu situs · bukti khusus | BRIN 2024 | original SVG · grid |
| `02-01.svg` | TANAH | urutan material | BRIN 2024 | original SVG · layers-new |
| `02-02.svg` | ARSIP | kabar tidak serentak | BADAN GEOLOGI 2020 | original SVG · archive |
| `02-03.svg` | IKLIM | suhu dan hujan setempat | SCHURER ET AL. 2019 | original SVG · chart |
| `03-01.svg` | APA YANG TERTUTUP? | lapisan dapat dibaca | BRIN 2024 | original SVG · scope |
| `03-02.svg` | KAPAN KABAR TIBA? | tanggal terbit ≠ waktu bahaya | BADAN GEOLOGI 2020 | original SVG · calendar |
| `03-03.svg` | BAGAIMANA DIUJI? | peluang, bukan cuaca seragam | SCHURER ET AL. 2019 | original SVG · scope |
| `04-01.svg` | APRIL 1815 | fase letusan · VEI 7 | GVP TAMBORA | original SVG · calendar |
| `04-02.svg` | 11 MEI | Benares tiba di Batavia | BADAN GEOLOGI 2020 | original SVG · route |
| `04-03.svg` | 6 · 13 · 20 · 27 MEI | edisi Gazette bertahap | BADAN GEOLOGI 2020 | original SVG · calendar |
| `05-01.svg` | BENARES | Makassar → Batavia | BADAN GEOLOGI 2020 | original SVG · route |
| `05-02.svg` | DISPATCH | dentuman malam 11 April | BADAN GEOLOGI 2020 | original SVG · archive |
| `05-03.svg` | BO’ SANGAJI KAI | rekaman Bima yang disebut | BADAN GEOLOGI 2020 | original SVG · archive |
| `06-01.svg` | KEJADIAN | bahaya di tempat tertentu | BATAS EDITORIAL | original SVG · arrows |
| `06-02.svg` | LAPORAN | kabar bergerak bertahap | BADAN GEOLOGI 2020 | original SVG · route |
| `06-03.svg` | TANGGAL TERBIT | waktu pembaca menerima kabar | BATAS EDITORIAL | original SVG · calendar |
| `07-01.svg` | SEKITAR 6 KM | lebar kaldera | GVP TAMBORA | original SVG · caldera |
| `07-02.svg` | SEKITAR 1.250 M | rim di atas lantai | GVP TAMBORA | original SVG · caldera |
| `07-03.svg` | BENTUK BERUBAH | jejak geologi, bukan drama | GVP TAMBORA | original SVG · scope |
| `08-01.svg` | SEKITAR 200 M | unit 1815 di satu dinding | GVP TAMBORA | original SVG · column |
| `08-02.svg` | ≥ 4 JATUHAN TEFRA | sebelum aliran dan surge | SUTAWIDJAJA ET AL. 2006 | original SVG · column |
| `08-03.svg` | URUTAN | endapan memberi waktu & jangkauan | GVP TAMBORA | original SVG · layers-new |
| `09-01.svg` | LERENG | material mengikuti permukaan | GVP TAMBORA | original SVG · arrows |
| `09-02.svg` | PANTAI & LAUT | mencapai sisi Sanggar | GVP TAMBORA | original SVG · arrows |
| `09-03.svg` | UDARA | jalur bukti lain | GVP TAMBORA | original SVG · atmosphere |
| `10-01.svg` | SANGGAR | keterangan masyarakat | SUTAWIDJAJA ET AL. 2006 | original SVG · names |
| `10-02.svg` | TAMBORA | keterangan masyarakat | SUTAWIDJAJA ET AL. 2006 | original SVG · names |
| `10-03.svg` | PEKAT | keterangan masyarakat | SUTAWIDJAJA ET AL. 2006 | original SVG · names |
| `11-01.svg` | 2006 | penelitian dimulai | BRIN 2024 | original SVG · calendar |
| `11-02.svg` | 2008 → 2021 | penelitian diteruskan | BRIN 2024 | original SVG · research |
| `11-03.svg` | DORO BENTE | lokasi dengan temuan khusus | BRIN 2024 | original SVG · grid |
| `12-01.svg` | FRAGMEN KERAMIK | artefak yang dilaporkan | BRIN 2024 | original SVG · artifact |
| `12-02.svg` | GERABAH | artefak yang dilaporkan | BRIN 2024 | original SVG · artifact |
| `12-03.svg` | TULANG & CANGKANG | material yang dilaporkan | BRIN 2024 | original SVG · artifact |
| `13-01.svg` | SATU KOTAK | bukan seluruh Sumbawa | BRIN 2024 | original SVG · boundary |
| `13-02.svg` | AKTIVITAS MANUSIA | bukan kota utuh dari imajinasi | BRIN 2024 | original SVG · boundary |
| `13-03.svg` | TIDAK DIREKONSTRUKSI | wajah, rute, menit terakhir | BATAS EDITORIAL | original SVG · scope |
| `14-01.svg` | SO₂ | masuk ke stratosfer | SCHURER ET AL. 2019 | original SVG · atmosphere |
| `14-02.svg` | AEROSOL SULFAT | terbentuk di stratosfer | SCHURER ET AL. 2019 | original SVG · particles |
| `14-03.svg` | RADIASI PENDEK ↓ | energi bersih ke permukaan | SCHURER ET AL. 2019 | original SVG · arrows |
| `15-01.svg` | PROSES FISIKA | dapat bekerja lintas atmosfer | SCHURER ET AL. 2019 | original SVG · atmosphere |
| `15-02.svg` | SIRKULASI | ikut menentukan pola setempat | SCHURER ET AL. 2019 | original SVG · globe |
| `15-03.svg` | DAMPAK TERCATAT | tempat · musim · masyarakat | BATAS EDITORIAL | original SVG · scope |
| `16-01.svg` | EROPA TENGAH & BARAT | musim panas 1816 | SCHURER ET AL. 2019 | original SVG · globe |
| `16-02.svg` | DINGIN & BASAH | anomali regional yang diuji | SCHURER ET AL. 2019 | original SVG · chart |
| `16-03.svg` | BUKAN LABEL GLOBAL | tidak semua benua seragam | BATAS EDITORIAL | original SVG · scope |
| `17-01.svg` | DATA INSTRUMENTAL AWAL | merekam anomali | SCHURER ET AL. 2019 | original SVG · research |
| `17-02.svg` | DUA MODEL IKLIM | simulasi pembanding | SCHURER ET AL. 2019 | original SVG · model |
| `17-03.svg` | FORCING vs SIRKULASI | dua peran dipisahkan | SCHURER ET AL. 2019 | original SVG · comparison |
| `18-01.svg` | PRESIPITASI | sirkulasi dapat mereproduksi pola | SCHURER ET AL. 2019 | original SVG · chart |
| `18-02.svg` | SEKITAR ¼ | anomali dingin yang dijelaskan | SCHURER ET AL. 2019 | original SVG · chart |
| `18-03.svg` | SISA PERTANYAAN | bukan satu sebab tunggal | SCHURER ET AL. 2019 | original SVG · comparison |
| `19-01.svg` | HINGGA 100× | dingin Eropa lebih mungkin | SCHURER ET AL. 2019 | original SVG · likelihood-cold |
| `19-02.svg` | 1,5 → 3× | kondisi basah lebih mungkin | SCHURER ET AL. 2019 | original SVG · likelihood-wet |
| `19-03.svg` | FORCING BESAR | mengubah peluang dalam sistem | SCHURER ET AL. 2019 | original SVG · comparison |
| `20-01.svg` | TANAH | lapisan 1815 di Doro Bente | BRIN 2024 | original SVG · layers-new |
| `20-02.svg` | ARSIP | kabar kapal dan surat | BADAN GEOLOGI 2020 | original SVG · archive |
| `20-03.svg` | ATMOSFER | mekanisme aerosol sulfat | SCHURER ET AL. 2019 | original SVG · atmosphere |
| `20-04.svg` | MODEL | peluang dingin diuji | SCHURER ET AL. 2019 | original SVG · model |
| `21-01.svg` | SITUS | bukti khusus, bukan seluruh pulau | BRIN 2024 | original SVG · boundary |
| `21-02.svg` | ARSIP | jeda kabar, bukan jam bahaya | BADAN GEOLOGI 2020 | original SVG · calendar |
| `21-03.svg` | IKLIM | peluang regional, bukan seragam | SCHURER ET AL. 2019 | original SVG · scope |
| `22-01.svg` | LIMA LAPISAN | titik awal yang dapat diperiksa | BRIN 2024 | original SVG · layers-new |
| `22-02.svg` | RANTAI BUKTI | tanah → arsip → atmosfer → model | MULTI-SUMBER | original SVG · chain |
| `22-03.svg` | APA YANG DIRINGKAS? | bukti apa yang perlu dibaca lagi? | ODDCHAPTER | original SVG · question |

## Dokumen render

- Input komposisi: `10_FILM/remotion/src/longform.lf04.generated.json`
- ID komposisi: `ODDCHAPTER-LONGFORM-LF04-TAMBORA`
- Pengaturan: 1920×1080, 30 fps; 22 scene diagram; caption bersumber dari teks yang disintesis.
