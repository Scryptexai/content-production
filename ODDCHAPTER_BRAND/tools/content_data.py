"""
content_data.py — satu sumber kebenaran untuk 21 episode.

Struktur tiap episode mengikuti model narrative nonfiction Jon Franklin
("Writing for Story", dua Pulitzer): satu karakter yang menginginkan sesuatu,
menabrak komplikasi, gagal, lalu mendapat wawasan yang mengubah makna — bukan
rangkaian fakta. Di dalam 60 detik, model itu dipetakan ke lima bagian
(hook 5% · setup 15% · tension 35% · turn 15% · consequence 20%).

Kunci teknisnya: TANAMAN. Satu detail kecil yang ditanam di awal dan berubah
maknanya di turn. Tanpa itu, episode cuma fakta yang dibacakan.

Field:
  protagonis  siapa yang menginginkan sesuatu (nama + satu detail spesifik)
  mau         apa yang dia mau, dalam satu kalimat konkret
  hambatan    apa yang menghalangi
  tanaman     detail yang ditanam di awal dan dibayar di turn
  beats       [(bagian, kalimat VO)] — bagian: setup/tension/turn/consequence
  sumber      status + rujukan
"""

EPISODES = [
    # ─────────────────────────────────────────────── HILANG ──
    dict(
        ep="EP01", voice_legacy=True, day=1, slot="pagi", jam="07.00", series="HILANG", pov="A",
        title="TIGA PENJAGA DAN SATU SET PAKAIAN YANG TERTINGGAL", struktur="klimaks-awal",
        thumb=["TIGA", "PENJAGA"], thumb_text="TIDAK PULANG",
        durasi=56,
        protagonis="Donald McArthur, penjaga pengganti di Eilean Mòr.",
        mau="Menyelesaikan pekerjaan pagi dan menunggu kapal yang datang menjemputnya.",
        hambatan="Desember 1900. Pulau batu tanpa pohon, tanpa jalan, tanpa radio.",
        tanaman="Satu set pakaian tahan air tertinggal di gantungan.",
        hook="15 Desember 1900. Tiga penjaga masuk ke menara. Tidak ada yang melihat mereka keluar.",
        hook_alt="Ada tiga orang di menara itu. Setelah Desember 1900, tidak ada satu pun yang keluar.",
        tanya="Apa yang terjadi di dalam? Bagaimana tiga orang hilang dari pulau batu tanpa satu pun jejak?",
        entitas="tiga penjaga",
        relate="Sebelas hari sebelumnya, di pulau batu Skotlandia. Tiga orang mengunci pintu dari dalam, seperti kamu.",
        diskusi="Kalau kamu di pulau itu, kamu akan naik ke menara atau menunggu kapal?",
        celah="Kenapa satu penjaga keluar tanpa pakaian tahan airnya?",
        gambar_melekat="Tiga orang berdiri di kaki menara, dan tidak satu pun dari mereka terlihat keluar.",
        beats=[
            # 0 · CUT. Klimaks sudah diucapkan; sekarang pertanyaannya, lalu cerita mundur.
            ("tanya", "Apa yang terjadi di dalam? Bagaimana tiga orang hilang dari pulau batu tanpa satu pun jejak?"),
            ("setup", "Sebelas hari sebelumnya, di pulau batu Skotlandia. Tiga orang mengunci pintu dari dalam, seperti kamu."),
            ("tension", "Desember 1900. Sebuah kapal lewat dan mencatat: lampunya mati."),
            ("tension", "Laporan itu sampai ke darat. Tidak ada yang naik selama sebelas hari."),
            ("tension", "26 Desember, kapal tender akhirnya sampai. Pintunya terkunci dari dalam."),
            ("tension", "Jam di menara berhenti. Kerja pagi itu selesai semua."),
            ("turn", "Dia keluar cepat, dalam hujan, tanpa pakaian itu."),
            ("turn", "Kalimat indah yang kita kutip seratus tahun itu tidak ada di arsip."),
            ("consequence", "Tidak satu pun mayat ditemukan. Yang tertinggal hanya pakaian itu."),
        ],
        turn_quote="“Laut tenang. Tuhan di atas semua.”",
        turn_verdict="Sesuatu terjadi setelah kerja selesai. Kalimat dramatisnya ditambahkan kemudian.",
        loop="Pakaian itu masih di gantungan, dan ketiga penjaga itu tidak pernah pulang.",
        cues=["LAMPU MATI", "SEBELAS HARI", "PINTU TERKUNCI", "JAM BERHENTI"],
        visual="Tiga penjaga di kaki menara; ruang jaga kosong; menara di garis horizon; pakaian di gantungan.",
        captions=['', 'Apa yang terjadi?', 'Seperti kamu.', 'Lampunya mati.', 'Tidak ada yang naik.', 'Pintu terkunci dari dalam.', 'Kerja pagi selesai semua.', '', '', 'Tidak satu pun mayat.', ''],
        caption_hi=['', 'terjadi', 'kamu', 'mati', 'Tidak ada', 'terkunci', 'selesai', '', '', 'mayat', ''],
        stamps=[('1900', 0), ('?', 1), ('11', 4), ('0', 9)],
        sfx={'00_hook': 'rustle', '01_tanya': 'gust', '02_setup': 'gust', '03_tension': 'engine', '04_tension': 'gust', '05_tension': 'clunk', '06_tension': 'tick', '07_turn': 'rustle', '08_turn': 'page', '09_consequence': 'boom', '99_loop': 'boom'},
        photos=['00_keepers', '01_empty_room', '02_island', '03_ship', '11_lighthouse_far', '04_door', '12_clock', '07_oilskins', '08_logbook', '13_empty_sea', '07_oilskins'],
        bed="audio/EP01/bed.wav",
        plate="tower",
        sumber="VERIFIED — Northern Lighthouse Board, nlb.org.uk/history/flannan-isles/. Hilang setelah kerja pagi 15 Des 1900; Archtor mencatat lampu mati; laporan diterima 18 Des; Hesperus tiba 26 Des; lampu bersih, minyak penuh; satu set oilskins tertinggal. Buku harian dramatis = tambahan fiktif (Mike Dash, Fortean Times).",
    ),
    dict(
        ep="EP02", voice_legacy=True, day=2, slot="pagi", jam="07.00", series="HILANG", pov="B",
        struktur="klimaks-awal",
        title="MEREKA MEMOTONG TENDA ITU DARI DALAM",
        thumb=["DIPOTONG", "DARI DALAM"], thumb_text="DIPOTONG DARI DALAM",
        durasi=64,
        protagonis="Igor Dyatlov, 23 tahun, pemimpin kelompok pendaki Institut Politeknik Ural.",
        mau="Membawa delapan orang menyeberangi lereng Kholat Syakhl dan pulang.",
        hambatan="Malam 1–2 Februari 1959. Angin kencang, salju, suhu jauh di bawah nol.",
        tanaman="Tenda itu dipotong dari dalam, padahal pintunya cuma satu meter dari situ.",
        hook="1 Februari 1959. Sembilan pendaki memotong tenda dari dalam, lalu keluar tanpa sepatu.",
        hook_alt="Ada sembilan orang di dalam tenda itu. Tidak satu pun keluar lewat pintu.",
        tanya="Kenapa sembilan orang merobek rumah mereka sendiri, lalu berlari ke salju?",
        entitas="sembilan pendaki",
        diskusi="Di posisi mereka, kamu akan memotong tenda atau menunggu sampai pagi?",
        celah="Kenapa mereka memotong tenda sendiri lalu berlari ke salju tanpa sepatu?",
        relate="Kamu pernah tidur di tempat asing, dan dengar bunyi di luar tenda yang tak bisa dijelaskan.",
        gambar_melekat="Kain tenda terpotong dari dalam, menganga ke arah kamera.",
        beats=[
            # 0 · CUT: pertanyaan yang memotong, sebelum cerita dimulai
            ("tanya", "Kenapa sembilan orang merobek rumah mereka sendiri, lalu berlari ke salju?"),
            # 1 · RELATE: penonton masuk lewat pengalaman yang pernah dialaminya
            ("relate", "Kamu pernah tidur di tempat asing, dan dengar bunyi di luar tenda yang tak bisa dijelaskan."),
            ("setup", "Mereka mahasiswa Ural. Berpengalaman semua, dan Igor Dyatlov yang memimpin."),
            ("tension", "Satu mahasiswa pulang karena sakit punggung. Dia satu-satunya yang selamat."),
            ("tension", "Tiga minggu kemudian tenda itu ditemukan masih berdiri. Sepatu dan jaket di dalam."),
            ("tension", "Jejak kaki turun ke hutan: satu setengah kilometer, sebagian hanya berkaus kaki."),
            ("tension", "Dua ditemukan di bawah pohon cedar. Empat di dasar jurang, tulang dada retak."),
            ("turn", "Enam puluh tahun dugaan: pasukan, monster, senjata rahasia."),
            ("turn", "Dua insinyur memodelkan longsoran salju. Hampir semua luka itu cocok."),
            ("consequence", "Tapi tidak ada model yang menjelaskan kenapa mereka tidak kembali ke tenda."),
        ],
        turn_quote="“Mereka dibunuh.”",
        turn_verdict="Luka mereka cocok dengan longsoran lempeng salju. Yang tidak cocok: kenapa mereka tidak kembali.",
        loop="Mereka memotong tenda mereka sendiri. Pertanyaan itu masih di salju, enam puluh tujuh tahun.",
        cues=["1 DARI 9", "3 MINGGU", "1,5 KM", "EMPAT"],
        visual="Sembilan orang berbaris di malam bersalju; kain tenda terpotong dari dalam; jejak kaki turun ke hutan; cedar; jurang.",
        captions=['', 'Kenapa mereka keluar?', 'Pernah tidur di tempat asing?', 'Sembilan mahasiswa.', 'Dia pulang karena sakit punggung.', 'Sepatu masih di dalam.', 'Turun ke hutan, tanpa sepatu.', 'Empat di jurang. Tulang retak.', '', '', 'Tidak kembali ke tenda.', ''],
        caption_hi=['', 'keluar', 'asing', 'Sembilan', 'punggung', 'Sepatu', 'tanpa sepatu', 'jurang', '', '', 'Tidak', ''],
        stamps=[('1959', 0), ('9', 3)],
        sfx={'00_hook': 'boom', '01_tanya': 'gust', '02_relate': 'rustle', '03_setup': 'gust', '04_tension': 'rustle', '05_tension': 'clunk', '06_tension': 'gust', '07_tension': 'page', '08_turn': 'boom', '09_turn': 'rustle', '10_consequence': 'boom', '99_loop': 'boom'},
        photos=['00_hikers', '01_tent_cut', '02_tent_inside', '03_group', '04_train', '05_slope', '06_footprints', '07b_ravine', '08_casefile', '09_avalanche', '10_tent_dark'],
        bed="audio/EP02/bed.wav",
        plate="shelter",
        sumber=("VERIFIED — Night of 1–2 Feb 1959, Kholat Syakhl, northern Urals, nine hikers of the Ural "
                "Polytechnical Institute led by Igor Dyatlov; tent found cut open from the inside with boots, "
                "coats and food still inside; footprints led ~1.5 km downhill toward the treeline, some barefoot; "
                "two bodies under a large cedar with remains of a small fire; four in the ravine with severe chest "
                "and skull injuries; Yuri Yudin turned back early with sciatica and was the only survivor. "
                "Eksekusi resmi 1959: 'a compelling natural force'; 2020 penyelidikan Rusia: longsoran; "
                "Gaume & Puzrin, 'Mechanisms of slab avalanche release and impact in the Dyatlov Pass incident "
                "in 1959', Communications Earth & Environment (2021) — model longsoran lempeng salju. "
                "Ringkasan sekunder: History.com. Paper asli belum dibaca langsung."),
    ),
    dict(
        ep="EP03", voice_legacy=True, day=3, slot="pagi", jam="07.00", series="HILANG", pov="B",
        struktur="klimaks-awal",
        title="KAPAL YANG MASIH BISA BERLAYAR, AWAK YANG MENINGGALKANNYA",
        thumb=["KAPAL", "KOSONG"], thumb_text="KAPAL KOSONG",
        durasi=72,
        protagonis="Benjamin Briggs, kapten Mary Celeste. Istrinya dan anaknya ikut di kapal.",
        mau="Mengantar 1.701 tong alkohol ke Genoa, lalu pulang ke Massachusetts.",
        hambatan="Atlantik Utara, November 1872. Sepuluh orang di satu kapal layar kecil.",
        tanaman="Sekoci hilang, kompas hancur. Kapalnya sendiri masih bisa berlayar.",
        hook="5 Desember 1872. Sepuluh awak Mary Celeste hilang. Kapal dan muatannya masih ada.",
        hook_alt="Ada sepuluh orang di kapal itu. Delapan hari kemudian, tidak satu pun tinggal.",
        tanya="Kenapa sepuluh orang naik sekoci, dan meninggalkan kapal yang masih bisa berlayar?",
        entitas="sepuluh awak",
        diskusi="Kalau kamu di kapal itu, kamu akan naik sekoci atau menunggu kapal lewat?",
        celah="Kenapa awak meninggalkan kapal yang masih bisa berlayar?",
        relate="Kamu pernah meninggalkan rumah yang masih utuh, karena takut pada sesuatu yang belum kamu lihat?",
        gambar_melekat="Sekoci kosong di atas air tenang, talinya terkulai.",
        beats=[
            ("tanya", "Kenapa sepuluh orang naik sekoci, dan meninggalkan kapal yang masih bisa berlayar?"),
            ("relate", "Kamu pernah meninggalkan rumah yang masih utuh, karena takut pada sesuatu yang belum kamu lihat?"),
            ("setup", "Mary Celeste berlayar dari New York ke Genoa, membawa 1.701 tong alkohol industri."),
            ("tension", "Kapten Briggs membawa istri dan anaknya yang berumur dua tahun. Sepuluh orang semuanya."),
            ("tension", "Dei Gratia melihat kapal itu berlayar aneh. Tidak ada satu pun orang di dek."),
            ("tension", "Makanan enam bulan masih di palka. Perahunya hilang, kompasnya hancur."),
            ("tension", "Jurnal kapal berhenti 25 November. Kapal itu mengapung sendiri sembilan hari."),
            ("turn", "Bajak laut tidak menyentuh barang. Badai tidak merusak kapal ini."),
            ("turn", "Yang mereka tinggalkan bukan kapal yang tenggelam. Kapal yang masih bisa berlayar."),
            ("consequence", "Sembilan tong bocor. Tapi tidak ada yang menjelaskan sepuluh orang di sekoci kecil."),
        ],
        turn_quote="“Mereka dibunuh dan kapalnya dijarah.”",
        turn_verdict="Barang berharga utuh, kapal tidak rusak. Mereka pergi dengan sekoci, bukan tenggelam.",
        loop="Sepuluh orang naik sekoci kecil, dan satu kapal berlayar tanpa mereka.",
        cues=["ISTRI & ANAK", "DEI GRATIA", "PERAHU HILANG", "9 HARI"],
        visual="Sepuluh orang di dek kapal layar; dek kosong dengan kemudi tanpa tangan; palka berisi tong; sekoci kosong di laut tenang.",
        captions=['', 'Kenapa mereka naik sekoci?', 'Pernah takut pada yang belum dilihat?', '1.701 tong alkohol.', 'Sepuluh orang semuanya.', 'Tidak ada orang di dek.', 'Makanan masih di palka.', 'Jurnal berhenti 25 November.', '', '', 'Sembilan tong bocor.', ''],
        caption_hi=['', 'sekoci', 'takut', '1.701', 'Sepuluh', 'dek', 'Makanan', 'November', '', '', 'bocor', ''],
        stamps=[('1872', 0), ('1.701', 3), ('10', 4)],
        sfx={'00_hook': 'boom', '01_tanya': 'gust', '02_relate': 'rustle', '03_setup': 'engine', '04_tension': 'engine', '05_tension': 'gust', '06_tension': 'clunk', '07_tension': 'page', '08_turn': 'boom', '09_turn': 'engine', '10_consequence': 'boom', '99_loop': 'gust'},
        photos=['00_crew', '01_empty_deck', '02_cabin', '03_hold', '04_family', '05_ship_far', '06_supplies', '07_logbook', '08_valuables', '05_ship_far', '03_hold', '10_boat'],
        bed="audio/EP03/bed.wav",
        plate="vessel",
        sumber=("VERIFIED — Mary Celeste, brigantine, New York → Genoa, berlayar 7 Nov 1872; kargo 1.701 tong "
                "alkohol industri; di atas kapal: Kapten Benjamin Briggs, istri Sarah, putri Sophia (2 tahun), "
                "dan tujuh awak = sepuluh orang. Ditemukan oleh Dei Gratia 4–5 Des 1872 (sumber berbeda pada "
                "tanggalnya): dek kosong, sekoci hilang, kompas hancur, kronometer dan sekstan hilang, sebagian "
                "besar surat kapal hilang kecuali jurnal; air sekitar 1,1 m di palka; satu pompa dibongkar; "
                "makanan dan air masih ada. Catatan jurnal terakhir 25 Nov, dekat Azores; sembilan tong ditemukan "
                "kosong di Gibraltar, tong-tong itu kayu ek merah yang lebih berpori. Tidak ada tanda kekerasan. "
                "Ringkasan sekunder: maritimeducation.com, theunsolvedrecord.substack.com, skeptic.org.uk. "
                "Laporan Admiralty Gibraltar belum dibaca langsung."),
    ),
    dict(
        ep="EP04", voice_legacy=True, day=4, slot="pagi", jam="07.00", series="HILANG", pov="A",
        struktur="klimaks-awal",
        title="MEREKA BERJALAN MENJAUH DARI PERTOLONGAN",
        thumb=["JALAN", "KE ATAS"], thumb_text="JALAN KE ATAS",
        durasi=55,
        protagonis="Lima pria dari Yuba City, California. Yang kelima, Gary Mathias, tidak pernah ditemukan.",
        mau="Pulang setelah menonton pertandingan basket di Chico.",
        hambatan="Jalan pegunungan Plumas National Forest, Februari 1978, salju setinggi lutut.",
        tanaman="Kunci masih di kontak, tangki masih setengah penuh, mobil tidak rusak.",
        hook="1978. Lima pria berjalan ke atas, meninggalkan mobil yang kuncinya masih di kontak.",
        hook_alt="Di dalam trailer itu ada makanan dan pemanas. Dia tidak memakainya.",
        tanya="Kenapa mereka berjalan ke atas, menjauhi mobil yang masih bisa dipakai?",
        entitas="lima pria",
        diskusi="Kalau kamu di mobil itu, kamu akan menunggu sampai terang atau ikut berjalan ke atas?",
        celah="Kenapa mereka berjalan menjauhi jalan raya dan menjauhi pertolongan?",
        relate="Kamu pernah ikut orang lain ke arah yang salah, karena tidak ada yang bertanya?",
        gambar_melekat="Jejak kaki menanjak ke bukit, menjauhi mobil yang mereka tinggalkan.",
        beats=[
            ("tanya", "Kenapa mereka berjalan ke atas, menjauhi mobil yang masih bisa dipakai?"),
            ("relate", "Kamu pernah ikut orang lain ke arah yang salah, karena tidak ada yang bertanya?"),
            ("setup", "Februari 1978. Lima pria dari Yuba City menonton basket di Chico."),
            ("tension", "Pukul sepuluh malam mereka membeli makanan di toko. Setelah itu hilang."),
            ("tension", "Empat hari kemudian, mobil mereka ditemukan di jalan salju Plumas."),
            ("tension", "Kunci masih di kontak, tangki setengah penuh. Tidak ada kerusakan."),
            ("tension", "Mereka berjalan ke atas, menjauhi jalan, ke tempat yang lebih dingin."),
            ("turn", "Juni 1978. Ted Weiher ditemukan di dalam trailer penjaga hutan."),
            ("turn", "Di dalam ada makanan, selimut, dan pemanas. Hampir tidak ada yang dibuka."),
            ("consequence", "Tiga lainnya ditemukan di luar, membeku di atas salju."),
            ("consequence", "Sepatu Gary Mathias ada di dalam. Tubuhnya tidak pernah ditemukan."),
        ],
        turn_quote="\u201cMereka tersesat.\u201d",
        turn_verdict="Tersesat tidak membuat orang berjalan ke atas, melewati makanan, dan menjauhi jalan.",
        loop="Kuncinya masih di kontak. Dan pria kelima tidak pernah turun dari bukit.",
        cues=["TERAKHIR TERLIHAT", "ARAH SALAH", "TIDAK RUSAK", "LEBIH DINGIN"],
        visual="Mobil tertutup salju dari belakang; kunci di lubang kontak; jejak kaki menanjak; trailer penjaga hutan gelap.",
        captions=[
            "",
            "Kenapa ke atas?",
            "Pernah ikut arah salah?",
            "Basket di Chico, 1978.",
            "Pukul sepuluh malam. Lalu hilang.",
            "Empat hari. Mobil di salju.",
            "Kunci di kontak. Tangki setengah.",
            "Ke atas, menjauhi jalan.",
            "Trailer penjaga hutan. Juni.",
            "Makanan, selimut, pemanas. Tidak dipakai.",
            "Tiga ditemukan di luar, membeku.",
            "Sepatu Mathias ada. Tubuhnya tidak.",
            "",
        ],
        caption_hi=["", "ke atas", "salah", "Chico", "sepuluh", "Empat hari", "setengah", "menjauhi jalan", "Trailer", "Tidak dipakai", "membeku", "Sepatu", ""],
        stamps=[["1978", 0], ["10", 4], ["70", 5]],
        sfx={
            "00_hook": "boom", "01_tanya": "gust", "02_relate": "rustle", "03_setup": "engine",
            "04_tension": "engine", "05_tension": "gust", "06_tension": "clunk", "07_tension": "page",
            "08_turn": "boom", "09_turn": "engine", "10_consequence": "boom", "11_consequence": "gust",
            "99_loop": "gust",
        },
        photos=[
            "00_five_men", "01_car_snow", "02_wrong_road", "03_gym", "04_market_night",
            "05_logging_road", "06_keys_ignition", "07_tracks_up", "08_trailer",
            "09_trailer_inside", "10_snow_hollow", "11_mathias_shoes", "06_keys_ignition",
        ],
        bed="audio/EP04/bed.wav",
        plate="road",
        sumber=(
            "VERIFIED pada butir utama, dengan tiga koreksi dari versi rencana. Lima pria dari Yuba City, "
            "California, malam Jumat 24 Februari 1978 menonton pertandingan basket kampus di Chico (sekitar 50 mil "
            "dari rumah). Terakhir terlihat sekitar pukul 22.00 di toko Behr's Market, Chico, membeli makanan ringan. "
            "Dilaporkan hilang Sabtu 25 Februari. Mobil Jack Madruga, Mercury Montego 1969, ditemukan Selasa "
            "28 Februari (satu ringkasan menyebut 27) di jalan logging bersalju Plumas National Forest dekat Rogers "
            "Cow Camp, sekitar 70 mil ke timur dari jalur pulang mereka. Kondisi mobil: tidak rusak, kunci di lubang "
            "kontak, TANGKI SEKITAR SETENGAH PENUH (bukan penuh), tanpa tanda pembongkaran atau perkelahian. "
            "KORREKSI 1: naskah rencana menulis 'tangki penuh' - semua ringkasan menyebut setengah penuh; angka itu "
            "yang dipakai. KORREKSI 2: 'sembilan mil' dibuang - sumber berbeda antara 11 dan 20 mil untuk jarak trailer "
            "dari mobil, jadi tidak ada angka jarak yang diucapkan. KORREKSI 3: sebab kematian Weiher ditulis sebagai "
            "kelaparan dan kedinginan (kesimpulan pemeriksa); laporan otopsi yang menyebut radang paru dan keracunan "
            "darah akibat kaki membeku belum dibaca langsung. Juni 1978 (4-8 Juni) setelah salju mencair: Ted Weiher "
            "ditemukan di tempat tidur trailer ranger US Forest Service, terbungkus selimut, berat badannya tinggal "
            "separuh; trailer berisi makanan kaleng dan ransum, selimut, pemanas propana, lentera minyak, dan korek - "
            "hampir semuanya tidak dipakai. Jenggotnya menunjukkan dia bertahan 8-13 minggu. Jack Madruga, Bill "
            "Sterling, dan Jackie Huett ditemukan di hutan, di luar. Gary Mathias tidak pernah ditemukan; sepatunya "
            "ada di dalam trailer. Ringkasan sekunder: anomalydesk.com, morbidology.com, icecoldcases.com, "
            "talesfromtheunderworld.com; dokumen primer (laporan insiden Butte County 28 Feb 1978, otopsi Juni-Juli "
            "1978, inventaris trailer) belum dibaca langsung."
        ),
    ),
    dict(
        ep="EP05", voice_legacy=True, day=5, slot="pagi", jam="07.00", series="HILANG", pov="D",
        struktur="klimaks-awal",
        title="MEREKA MENULIS SATU KATA, BUKAN SEBUAH PERINGATAN",
        thumb=["TANPA", "MAYAT"], thumb_text="TANPA MAYAT",
        durasi=56,
        protagonis="Seratus lima belas orang koloni Roanoke, termasuk bayi Virginia Dare yang lahir di sana.",
        mau="Bertahan sampai gubernurnya kembali membawa bahan makanan.",
        hambatan="Gubernurnya berlayar ke Inggris, dan perang menahannya tiga tahun.",
        tanaman="Mereka sepakat: kalau pergi karena terpaksa, ukir salib. Di kayu itu tidak ada salib.",
        hook="1590. Seratus lima belas orang hilang. Rumah mereka dibongkar rapi, bukan dihancurkan.",
        hook_alt="Satu kata terpahat di tiang pagar, dan tidak ada salib di atasnya.",
        tanya="Kenapa mereka membongkar rumah sendiri, lalu meninggalkan satu kata di pagar?",
        entitas="lima belas orang",
        diskusi="Kalau kamu menemukan kata itu tanpa salib, kamu akan mencarinya atau menganggap semuanya sudah mati?",
        celah="Kenapa mereka menulis nama tempat, bukan tanda bahaya yang sudah disepakati?",
        relate="Kamu pernah meninggalkan rumah, dan berharap ada yang mencari?",
        gambar_melekat="Satu kata terpahat di tiang pagar, dan tidak ada salib di atasnya.",
        beats=[
            ("tanya", "Kenapa mereka membongkar rumah sendiri, lalu meninggalkan satu kata di pagar?"),
            ("relate", "Kamu pernah meninggalkan rumah, dan berharap ada yang mencari?"),
            ("setup", "1587. Seratus lima belas orang Inggris mendarat di Roanoke."),
            ("tension", "Gubernurnya berlayar ke Inggris mengambil bahan makanan."),
            ("tension", "Perang dengan Spanyol menahan kapal. Dia kembali tiga tahun kemudian."),
            ("tension", "Agustus 1590. Rumah-rumah sudah dibongkar, bukan runtuh."),
            ("tension", "Di tiang pagar terpahat satu kata: CROATOAN."),
            ("turn", "Mereka sudah sepakat: kalau pergi terpaksa, ukir salib di atas nama itu."),
            ("turn", "Di kayu itu tidak ada salib."),
            ("turn", "Empat ratus tahun kata di kayu itu dibaca sebagai pesan terakhir."),
            ("consequence", "Padahal tidak ada satu pun tulang. Tidak ada kuburan."),
            ("consequence", "Croatoan bukan peringatan. Itu alamat, lima puluh mil ke selatan."),
        ],
        turn_quote="\u201cMereka dibantai.\u201d",
        turn_verdict="Tidak ada tulang, tidak ada kuburan, dan nama itu ditulis tanpa salib. Itu alamat.",
        loop="Rumah itu dibongkar rapi karena mereka pindah, bukan karena dibantai.",
        cues=["JOHN WHITE", "ARMADA SPANYOL", "AGUSTUS 1590", "8 HURUF"],
        captions=[
            "",
            "Kenapa bongkar rumah sendiri?",
            "Pernah pergi tanpa alamat?",
            "Roanoke, 1587.",
            "Dia pergi cari makanan.",
            "Tiga tahun. Perang.",
            "Rumah dibongkar, bukan runtuh.",
            "Satu kata di tiang pagar.",
            "Janji mereka: salib kalau terpaksa.",
            "Tidak ada salib.",
            "Empat ratus tahun salah baca.",
            "Tanpa tulang. Tanpa kuburan.",
            "Itu alamat, lima puluh mil.",
            "",
        ],
        caption_hi=["", "bongkar", "alamat", "Roanoke", "makanan", "Tiga tahun", "dibongkar", "pagar", "salib", "Tidak ada salib", "salah baca", "Tanpa tulang", "alamat", ""],
        stamps=[["115", 0], ["1587", 3], ["400", 10]],
        sfx={
            "00_hook": "boom", "01_tanya": "gust", "02_relate": "rustle", "03_setup": "engine",
            "04_tension": "engine", "05_tension": "gust", "06_tension": "clunk", "07_tension": "page",
            "08_turn": "boom", "09_turn": "engine", "10_turn": "boom",
            "11_consequence": "gust", "12_consequence": "boom", "99_loop": "gust",
        },
        photos=[
            "00_houses", "01_gate", "02_shore_dusk", "03_landing", "04_ship_away",
            "05_storm", "06_dismantled", "07_carved_post", "13_agreement", "09_bare_wood",
            "10_map", "11_empty_ground", "12_island_far", "06_dismantled",
        ],
        bed="audio/EP05/bed.wav",
        plate="ridge",
        sumber=(
            "VERIFIED pada butir utama; satu klaim rencana dilunakkan. 1587: ekspedisi keluarga di bawah "
            "gubernur John White, sekitar 115 orang, mendarat di Roanoke (kini Carolina Utara); Virginia Dare "
            "lahir 18 Agustus 1587, anak Inggris pertama yang lahir di Amerika. White berlayar ke Inggris akhir "
            "1587 untuk bahan makanan; perang dengan Spanyol (Armada 1588) menahan pelayaran; ia kembali dan "
            "mendarat 18 Agustus 1590 - tiga tahun kemudian, pada ulang tahun cucunya. Yang ia temukan: rumah "
            "sudah DIBONGKAR (bukan runtuh atau terbakar), palisade kayu dibangun, tidak ada mayat, tidak ada "
            "kuburan, tidak ada tanda pertempuran; peti yang ia kubur sudah digali, buku/peta/zirah rusak karena "
            "hujan, barang berat (batang besi, timah, senjata) ditinggal. Dua pahatan: 'CRO' di pohon dan "
            "'CROATOAN' di tiang pagar; keduanya TANPA salib. Kesepakatan sebelum ia pergi: nama tempat tujuan "
            "dipahat kalau pindah, salib Malta ditambahkan kalau perpindahan itu karena bahaya. Croatoan = pulau "
            "(kini Hatteras, sekitar 50 mil ke selatan) dan nama orang Algonquian di sana, dengan Manteo sebagai "
            "kepala yang bersahabat. White hendak menyeberang ke Croatoan, tetapi badai dan kerusakan jangkar "
            "menggagalkannya; ia tidak pernah kembali ke Amerika. LUNGGUH: rencana menulis 'mereka pindah dan "
            "bergabung dengan orang di sana' sebagai fakta - itu masih HIPOTESIS. Yang bisa dikatakan: tidak ada "
            "bukti pembantaian di Roanoke, dan kata itu adalah alamat, bukan peringatan. Bukti pendukung "
            "hipotesis asimilasi: temuan abad ke-16 di Hatteras (termasuk endapan kerak besi pandai besi, tim "
            "Mark Horton), 'Site X' di Bertie County (First Colony Foundation, 2015), simbol benteng di bawah "
            "tambalan peta La Virginea Pars (British Museum, 2012), dan laporan John Smith 1607. Ringkasan "
            "sekunder: encyclopediavirginia.org, pagesofhistory.org, scienceinsights.org. Laporan asli White "
            "('The fift voyage of M. John White', Hakluyt) belum dibaca langsung."
        ),
    ),
    dict(
        ep="EP06", day=6, slot="malam", jam="19.30", series="TERSEMBUNYI", pov="B",
        struktur="klimaks-awal",
        title="API DI BAWAH KOTA YANG TIDAK PERNAH DIPADAMKAN",
        thumb=["MASIH", "MENYALA"], thumb_text="MASIH MENYALA",
        durasi=46,
        protagonis="Lima petugas pemadam sukarela dan kota kecil di atas lapisan batu bara.",
        mau="Membersihkan tumpukan sampah sebelum libur Memorial Day.",
        hambatan="Sampahnya dibakar di dalam lubang bekas tambang, tepat di atas batu bara.",
        tanaman="Api masuk lewat celah batu, dan tidak ada yang tahu sampai gasnya naik ke rumah.",
        hook="Pernah membayangkan tinggal di kota yang apinya tidak bisa dimatikan?",
        hook_alt="Bayangkan lantai rumahmu hangat. Kamu tidak tahu kenapa.",
        tanya="Bayangkan lantai rumahmu hangat. Kamu akan pindah, atau pura-pura tidak tahu?",
        entitas="api",
        diskusi="Kalau rumahmu berdiri di atas api, kamu akan pindah atau bertahan?",
        celah="Kenapa mereka memilih memindahkan kota, bukan memadamkan api?",
        relate="Kita pintar mencari alasan untuk tetap tinggal di rumah tua itu.",
        gambar_melekat="Retakan di jalan mengeluarkan uap, dan rumah masih berdiri di atasnya.",
        beats=[
            ("tanya", "Bayangkan lantai rumahmu hangat. Kamu akan pindah, atau pura-pura tidak tahu?"),
            ("relate", "Kita pintar mencari alasan untuk tetap tinggal di rumah tua itu."),
            ("setup", "Lima orang membakar sampah di lubang bekas tambang pada 1962."),
            ("tension", "Mereka cuma ingin bersih-bersih. Apinya masuk ke batu bara, dan tinggal di sana."),
            ("tension", "Sembilan belas tahun kemudian, seorang anak nyaris jatuh ke dalam lubang di halaman."),
            ("turn", "Yang mereka pilih bukan memadamkan api. Mereka memindahkan kotanya."),
            ("consequence", "Lihat peta kota itu. Sejak 1992 semua rumah jadi milik negara."),
            ("consequence", "Sekarang tinggal lima orang. Kamu masih mau tinggal di atas api?"),
        ],
        turn_quote="\u201cApi itu akan padam sendiri, atau dipadamkan.\u201d",
        turn_verdict="Tidak. Yang mereka beli bukan pemadaman, tapi jarak. Apinya masih menyala di bawah jalan yang kosong.",
        loop="Apinya masih menyala. Di bawah jalan yang tidak lagi dilewati siapa pun.",
        cues=["BATU BARA", "UAP PANAS", "TANPA PEMILIK", "MASIH MENYALA"],
        captions=[
            "",
            "Bayangkan lantai hangat.",
            "Kita cari alasan.",
            "Sampah dibakar, 1962.",
            "Api masuk ke batu bara.",
            "19 tahun. Lubang.",
            "Bukan dipadamkan.",
            "Sejak 1992, milik negara.",
            "Lima orang tinggal.",
            "",
        ],
        caption_hi=["", "lantai", "alasan", "1962", "batu bara", "19 tahun", "dipadamkan", "1992", "Lima orang", ""],
        stamps=[["1962", 3], ["5", 8]],
        sfx={
            "00_hook": "boom", "01_tanya": "gust", "02_relate": "rustle", "03_setup": "engine",
            "04_tension": "engine", "05_tension": "clunk", "06_turn": "boom",
            "07_consequence": "engine", "08_consequence": "gust", "99_loop": "gust",
        },
        photos=[
            "00_dumpfire", "01_steam_crack", "02_kitchen", "03_council", "04_seam",
            "06_sinkhole", "10_demolition", "11_route61", "01_steam_crack", "07_vent",
        ],
        bed="audio/EP06/bed.wav",
        plate="plume",
        sumber=(
            "VERIFIED pada butir utama. 27 Mei 1962: dewan Borough Centralia menyewa lima anggota pemadam "
            "sukarela untuk membersihkan/membakar tumpukan sampah di lubang bekas tambang terbuka dekat "
            "Odd Fellows Cemetery, menjelang Memorial Day; api masuk lewat celah terbuka di batuan penutup ke "
            "lapisan antrasit di bawah kota. 9 Agustus 1962 tambang di sekitar Centralia ditutup setelah karbon "
            "monoksida terdeteksi. 1981: Todd Domboski (12 tahun) hampir jatuh ke lubang uap yang terbuka di "
            "halaman rumah neneknya; peristiwa ini yang membawa kasusnya ke media nasional - kedalaman lubang "
            "dilaporkan sekitar 45 meter. 1984: Kongres menyetujui sekitar 42 juta dolar untuk relokasi sukarela. "
            "13 Juli 1992: Gubernur Robert Casey memakai eminent domain atas seluruh properti borough; warga "
            "yang bertahan secara resmi dianggap penghuni tanpa hak, lalu menggugat dan mencapai kesepakatan "
            "boleh tinggal seumur hidup. 2002: kode pos Centralia dihentikan. Populasi: puncak sekitar 2.700 "
            "(1890), sekitar 1.000 (1980), 5 orang (sensus 2020). Api masih membara; DEP Pennsylvania "
            "memperkirakan sekitar 400 acre terbakar, suhu hingga sekitar 540 C pada kedalaman sampai 90 meter, "
            "dan masih bisa terbakar sekitar 250 tahun lagi. Route 61 rusak dan ditutup permanen 1992. "
            "Ringkasan sekunder: pabook.libraries.psu.edu, centraliapa.org, worldatlas.com, discoveryuk.com, "
            "boingboing.net. Buku David DeKok 'Fire Underground' dan laporan DEP belum dibaca langsung."
        ),
    ),
    dict(
        ep="EP07", day=7, slot="malam", jam="19.30", series="TERSEMBUNYI", pov="A",
        struktur="klimaks-awal",
        title="JEJAK KAKI ITU HANYA SATU ARAH",
        thumb=["JEJAK", "SATU ARAH"], thumb_text="JEJAK SATU ARAH",
        durasi=46,
        protagonis="Keluarga Gruber di pertanian terpencil Hinterkaifeck, Bavaria.",
        mau="Melewati musim dingin di pertanian yang jauh dari kampung.",
        hambatan="Ada jejak kaki di salju menuju rumah mereka, dan tidak ada yang kembali.",
        tanaman="Kunci hilang, langkah terdengar di loteng, dan tidak ada pintu yang dibuka paksa.",
        hook="Kalau semua jejak di salju itu mengarah masuk, siapa yang keluar?",
        hook_alt="Semua jejak di salju itu mengarah ke satu pintu.",
        tanya="Kamu akan memeriksa atapnya, atau pura-pura tidak dengar?",
        entitas="jejak",
        diskusi="Kalau rumahmu dikelilingi jejak yang masuk, kamu akan memeriksa loteng?",
        celah="Kenapa tidak ada satu pun jejak yang keluar dari rumah itu?",
        relate="Kita sering mengabaikan bunyi kecil di rumah sendiri.",
        gambar_melekat="Jejak kaki di salju berhenti di depan pintu, dan tidak berlanjut.",
        beats=[
            ("tanya", "Kamu akan memeriksa atapnya, atau pura-pura tidak dengar?"),
            ("relate", "Kita sering mengabaikan bunyi kecil di rumah sendiri."),
            ("setup", "Malam tiga puluh satu Maret 1922, enam orang tidur di pertanian Bavaria itu."),
            ("tension", "Lihat kuncinya: hilang. Andreas naik ke loteng, dan tidak ada siapa pun."),
            ("tension", "Tidak ada pintu yang dirusak. Jadi bagaimana dia bisa masuk?"),
            ("turn", "Dia tidak masuk malam itu. Dia sudah menunggu di dalam rumah."),
            ("consequence", "Empat hari kemudian, tetangga melihat asap dari cerobong."),
            ("consequence", "Dia menyalakan api di dapur. Kamu bisa bayangkan baunya."),
        ],
        turn_quote="\u201cSeseorang masuk malam itu.\u201d",
        turn_verdict="Tidak ada pintu yang dirusak, dan kuncinya sudah hilang berhari-hari sebelumnya. Dia tidak masuk; dia sudah di dalam.",
        loop="Jejak di salju itu berhenti di pintu. Yang membuatnya tidak pernah keluar.",
        cues=["LOTENG", "KUNCI HILANG", "ASAP", "MASIH DI DALAM"],
        captions=[
            "",
            "Kamu akan cek atap?",
            "Kita abaikan bunyi kecil.",
            "31 Maret 1922.",
            "Kunci hilang.",
            "Loteng kosong.",
            "Dia sudah di dalam.",
            "Asap empat hari.",
            "Api di dapur.",
            "",
        ],
        caption_hi=["", "loteng", "bunyi kecil", "1922", "kunci", "Loteng", "di dalam", "Asap", "dapur", ""],
        stamps=[["1922", 3], ["4", 7]],
        sfx={
            "00_hook": "gust", "01_tanya": "gust", "02_relate": "rustle", "03_setup": "engine",
            "04_tension": "clunk", "05_tension": "gust", "06_turn": "boom",
            "07_consequence": "gust", "08_consequence": "rustle", "99_loop": "gust",
        },
        photos=[
            "00_snow_tracks", "01_front_door", "02_window_night", "03_farm_dusk",
            "05_attic", "09_bolted_door", "07_barn_dark", "06_chimney_smoke",
            "08_stove", "00_snow_tracks",
        ],
        bed="audio/EP07/bed.wav",
        plate="ridge",
        sumber=(
            "VERIFIED pada butir utama. Hinterkaifeck: pertanian terpencil di Bavaria, sekitar 70 km utara "
            "Munich. Malam 31 Maret - 1 April 1922 enam orang terbunuh: Andreas Gruber (63), istrinya "
            "Caezilia (72), anak mereka Viktoria Gabriel (35), cucu Caezilia (7) dan Josef (2), serta pembantu "
            "baru Maria Baumgartner (44) yang tiba hari itu juga. Beberapa hari sebelumnya Andreas melaporkan "
            "ke tetangga: jejak kaki di salju dari tepi hutan menuju pertanian tanpa jejak kembali, langkah "
            "kaki di loteng, koran Munich yang tidak dipesan, dan kunci rumah yang hilang. Pembantu sebelumnya "
            "berhenti karena merasa rumah itu tidak tenang. Tidak ada tanda masuk paksa. Jenazah ditemukan "
            "4 April 1922 setelah tetangga curiga: tidak ada aktivitas, tetapi asap masih keluar dari cerobong "
            "dan ternak sudah diberi makan serta diperah. Senjata yang diyakini dipakai adalah cangkul berat "
            "(mattock); alat itu baru ditemukan setahun kemudian saat bangunan dibongkar. Pertanian dibongkar "
            "1923. Tengkorak dikirim ke Munich dan hilang pada masa Perang Dunia II; korban dimakamkan tanpa "
            "tengkorak di Waidhofen. Kasus tidak pernah selesai; tinjauan akademi polisi Jerman 2007 "
            "menyimpulkan bukti yang tersisa tidak cukup. Rincian luka dan dugaan pelaku sengaja TIDAK dipakai. "
            "Ringkasan sekunder: stillunsolvedmysteriesoftheworld, anomalien.com, defrostingcoldcases, "
            "truecrimeatlas, christian-hardinghaus.de, clutchjustice."
        ),
    ),
    dict(
        ep="EP08", day=8, slot="pagi", jam="07\.30", series="TERSEMBUNYI", pov="B",
        struktur="klimaks-awal",
        title="SEMUA LABEL DI PAKAIANNYA DIPOTONG",
        thumb=["SEMBILAN", "NAMA"], thumb_text="SEMBILAN NAMA",
        durasi=38,
        protagonis="Seorang perempuan tanpa nama, ditemukan di lembah Isdalen, Norwegia.",
        mau="Tidak ditemukan.",
        hambatan="Semua yang bisa menyebut namanya sudah dia buang sendiri.",
        tanaman="Label dipotong, tanda di botol dikerok, dan koper berisi delapan nama.",
        hook="Semua label di bajunya dipotong. Sebelum dia hilang.",
        hook_alt="Ada perempuan yang mencopot namanya dari setiap benda yang dia bawa.",
        tanya="Coba lihat delapan nama ini. Yang mana yang kamu pakai pulang?",
        entitas="label",
        diskusi="Menurut kamu, apa yang sebenarnya terjadi di lembah itu?",
        celah="Kenapa dia menghapus namanya lebih rapi daripada kematiannya sendiri?",
        relate="Kita sembunyikan nama di internet. Dia pakai gunting.",
        gambar_melekat="Potongan label di atas pakaian, tanpa satu pun merek yang tersisa.",
        # 9 segmen · 82 kata. Di 142 wpm + jeda 0,22 dtk = 37-38 dtk.
        # Dipangkas 16 Nov 2026 dari 12 segmen/105 kata: di atas 60 dtk penonton
        # hampir tidak pernah memutar ulang, jadi persentase tontonan tidak naik.
        beats=[
            ("tanya", "Coba lihat delapan nama ini. Yang mana yang kamu pakai pulang?"),
            ("relate", "Kita sembunyikan nama di internet. Dia pakai gunting."),
            ("setup", "Tahun 1970, lembah Isdalen, Norwegia. Ada perempuan terbakar di atas batu."),
            ("tension", "Tubuhnya hangus dari depan. Punggungnya utuh."),
            ("tension", "Ada jelaga di paru-parunya. Dia masih hidup waktu api menyala."),
            ("turn", "Orang mau mati tidak memotong label. Tidak mengerok tanda di botol."),
            ("consequence", "Lihat kopernya. Wig, uang asing, delapan nama."),
        ],
        turn_quote="\u201cDia bunuh diri.\u201d",
        turn_verdict="Mungkin. Tapi orang yang mau mati tidak memotong label, dan tidak mengerok tanda di botol.",
        loop="Semua label hilang. Kamu tidak akan tahu namanya. Kenapa?",
        cues=["LABEL DIPOTONG", "JELAGA", "8 NAMA"],
        captions=[
            "",
            "Delapan nama.",
            "Kita sembunyikan nama.",
            "Isdalen, 1970.",
            "Terbakar dari depan.",
            "Jelaga di paru-paru.",
            "Bukan bunuh diri?",
            "Wig, uang, delapan nama.",
            "Kenapa?",
        ],
        caption_hi=["", "Delapan nama", "nama", "1970", "terbakar", "jelaga", "label", "koper", "kenapa"],
        stamps=[["1970", 3], ["8", 1]],
        sfx={
            "00_hook": "rustle",
            "01_tanya": "page",
            "02_relate": "page",
            "03_setup": "gust",
            "04_tension": "boom",
            "05_tension": "gust",
            "06_turn": "boom",
            "07_consequence": "clunk",
            "99_loop": "boom",
        },
        photos=[
            "00_labels", "01_passports", "00_labels", "03_valley", "04_scorch",
            "05_bottles", "00_labels", "06_suitcase", "00_labels",
        ],
        bed="audio/EP08/bed.wav",
        plate="ridge",
        sumber=(
            "VERIFIED pada butir utama. 29 November 1970: jenazah seorang perempuan ditemukan di Isdalen "
            "(lembah di kaki Ulriken, dekat Bergen, Norwegia). Tubuh terbakar hebat di bagian depan; "
            "punggung relatif utuh; jelaga di paru-paru menunjukkan dia masih hidup saat terbakar. Semua "
            "label pada pakaian dipotong dan tanda pada botol dikerok. Dua koper di penitipan barang "
            "Stasiun Bergen: pakaian tanpa label, wig, kacamata tanpa resep, lima lembar 100 Deutsche Mark, "
            "peta, buku catatan berkode. Otopsi: keracunan karbon monoksida dan fenobarbital; 50-70 tablet "
            "Fenemal. Polisi menyimpulkan kemungkinan bunuh diri; banyak pihak meragukannya. Kasus dibuka "
            "kembali 2016; analisis isotop gigi mengarah ke sekitar Nuremberg. Yang TIDAK dipakai: nama "
            "alias yang belum terverifikasi dan teori konspirasi."
        ),
    ),
    dict(
        ep="EP09", day=4, slot="siang", jam="12.30", series="TERSEMBUNYI", pov="D",
        title="DUA KATA YANG MENYEMBUNYIKAN SEORANG TEKNISI LISTRIK",
        thumb=["DUA KATA", "TANPA NAMA"], thumb_text="DUA KATA",
        durasi=37,
        protagonis="Pria tanpa nama di pantai Somerton, Australia Selatan.",
        mau="Dikenali.",
        hambatan="Semua yang menyebut namanya sudah dibuang atau dipotong.",
        tanaman="Secarik kertas di saku: TAMAM SHUD. Tidak ada dompet, tidak ada tanda pengenal.",
        hook="Di sakunya cuma kertas: TAMAM SHUD. Tidak ada dompet, tidak ada nama.",
        hook_alt="Selama tujuh puluh tahun dia disebut mata-mata. Ternyata dia bukan siapa-siapa yang penting.",
        tanya="Coba lihat dua kata ini. Ada yang bisa kamu baca?",
        entitas="kertas",
        diskusi="Kalau kode di kertas itu milikmu, kenapa kamu menulisnya?",
        celah="Siapa pria ini, dan kenapa tidak satu pun orang mengenalnya?",
        relate="Kita tinggalkan nama di setiap benda. Dia mencopot semuanya.",
        gambar_melekat="Secarik kertas dengan dua kata, terlipat di saku jas.",
        beats=[
            ("tanya", "Coba lihat dua kata ini. Ada yang bisa kamu baca?"),
            ("relate", "Kita tinggalkan nama di setiap benda. Dia mencopot semuanya."),
            ("setup", "Desember 1948, pantai Somerton, Australia. Pria rapi, tanpa luka."),
            ("tension", "Lihat pakaiannya. Setiap label dipotong."),
            ("tension", "Kertas itu sobekan dari buku puisi. Sisa halaman penuh huruf acak."),
            ("turn", "Tujuh puluh tahun dia disebut mata-mata. Lalu DNA bilang lain."),
            ("consequence", "Dia teknisi listrik dari Melbourne. Namanya Carl Webb."),
        ],
        turn_quote="\u201cDia mata-mata Perang Dingin.\u201d",
        turn_verdict="Dia teknisi listrik dari Melbourne. Yang tersisa: kenapa dia ada di pantai itu.",
        loop="Kertas itu masih dua kata. Kamu punya tebakan?",
        cues=["TANPA ID", "TAMAM SHUD", "2022: DNA"],
        captions=[
            "",
            "Dua kata.",
            "Dia mencopot semuanya.",
            "Somerton, 1948.",
            "Labelnya dipotong.",
            "Sisa halaman penuh huruf.",
            "Bukan mata-mata.",
            "Carl Webb. Teknisi listrik.",
            "Kenapa di pantai itu?",
        ],
        caption_hi=["", "TAMAM SHUD", "nama", "1948", "label", "huruf", "DNA", "Carl Webb", "kenapa"],
        stamps=[["1948", 3]],
        sfx={
            "00_hook": "page",
            "01_tanya": "page",
            "02_relate": "rustle",
            "03_setup": "gust",
            "04_tension": "rustle",
            "05_tension": "page",
            "06_turn": "boom",
            "07_consequence": "clunk",
            "99_loop": "boom",
        },
        bed="audio/EP09/bed.wav",
        plate="paper",
        sumber=(
            "VERIFIED 2026-11-06 — 1 Desember 1948, pantai Somerton, Adelaide: pria tak dikenal tewas; tanpa dompet atau "
            "tanda pengenal; label pakaian dipotong, termasuk merek 'Keane'. Berbulan kemudian, di fob pocket yang "
            "dijahit di celana, ditemukan gulungan kertas 'Tamám Shud' (Persia: 'sudah berakhir') dari halaman terakhir "
            "Rubaiyat Omar Khayyam, edisi FitzGerald cetakan Whitcombe & Tombs 1941; buku itu lalu ditemukan di mobil tak "
            "terkunci dekat pantai, dengan lima baris huruf kapital di belakangnya (tak pernah dipecahkan secara resmi) "
            "dan satu nomor telepon. Otopsi: organ membengkak, limpa membesar, tanpa racun terdeteksi; pemeriksa yakin "
            "kematian tak wajar; di sidang disebut obat yang sulit dideteksi (kemudian diidentifikasi sebagai digitalis "
            "dan ouabain). Putusan koroner: identitas tak dikenal, kematian tak wajar, kemungkinan racun, bunuh diri "
            "mungkin tapi keadaan tak biasa, pembunuhan tetap mungkin. Mei 2021 jenazah digali untuk DNA; Juli 2022 Derek "
            "Abbott dan Colleen Fitzpatrick mengumumkan identifikasi lewat genealogi genetik dari rambut di topeng gips: "
            "Carl 'Charles' Webb, lahir 16 November 1905 di Footscray, Melbourne, anak termuda dari enam, teknisi "
            "listrik/pembuat instrumen. SAPOL dan Forensic Science SA belum mengonfirmasi resmi (2026: laporan ke koroner "
            "disebut 'segera'). Abbott: tak ada jejak intelijen; kode mungkin catatan taruhan kuda. Sumber: ABC News 26 "
            "Jul 2022; IEEE Spectrum (Abbott, April 2023); StrangeOutdoors."
        ),
    ),
    dict(
        ep="EP10", day=5, slot="malam", jam="18.30", series="TERSEMBUNYI", pov="B",
        title="MEREKA MEMBUAT BAHASA SENDIRI, LALU DIPISAHKAN",
        thumb=["HANYA", "SATU SAMA LAIN"], thumb_text="BAHASA SENDIRI",
        durasi=42,
        protagonis="June Gibbons, satu dari dua kembar identik di Wales.",
        mau="Punya dunia tempat dia bisa bicara.",
        hambatan="Dunia luar hanya punya satu cara untuk menyebut mereka: sakit.",
        tanaman="Mereka menulis novel dan puisi dalam bahasa yang mereka buat sendiri.",
        hook="Mereka menulis buku dalam bahasa yang tidak dimengerti siapa pun.",
        hook_alt="Dua anak membuat bahasa sendiri, lalu menulis novel di dalamnya.",
        tanya="Bayangkan punya bahasa yang cuma kamu dan satu orang tahu. Kenapa itu dianggap penyakit?",
        entitas="bahasa",
        diskusi="Kalau satu-satunya orang yang bisa kamu ajak bicara diambil, kamu masih punya suara?",
        celah="Kenapa memisahkan dua orang yang hanya bicara satu sama lain?",
        relate="Kita pakai bahasa untuk menjelaskan diri. Mereka pakai untuk menghilang.",
        gambar_melekat="Dua buku catatan penuh huruf yang tidak bisa dibaca siapa pun.",
        beats=[
            ("tanya", "Bayangkan punya bahasa yang cuma kamu dan satu orang tahu. Kenapa itu dianggap penyakit?"),
            ("relate", "Kita pakai bahasa untuk menjelaskan diri. Mereka pakai untuk menghilang."),
            ("setup", "Wales, 1963. Dua kembar identik, June dan Jennifer."),
            ("tension", "Mereka berhenti bicara ke siapa pun. Kecuali satu sama lain."),
            ("tension", "Bahasa itu punya aturan, kosakata, dan nama sendiri."),
            ("tension", "Coba lihat buku catatan mereka. Novel, puisi, sandiwara."),
            ("turn", "Rumah sakit jiwa memisahkan mereka. Supaya sembuh."),
            ("consequence", "Sebelas tahun di Broadmoor. Jennifer meninggal 9 Maret 1993."),
        ],
        turn_quote="\u201cMereka harus dipisahkan supaya sembuh.\u201d",
        turn_verdict="Yang mereka bangun bukan penyakit. Dunia itu runtuh justru saat mereka dipisahkan.",
        loop="Bahasa itu hilang saat mereka dipisahkan. Kamu masih punya suara?",
        cues=["1963 WALES", "BAHASA SENDIRI", "NOVEL & PUISI", "DIPISAHKAN"],
        captions=[
            "",
            "Bahasa sendiri.",
            "Mereka pakai untuk menghilang.",
            "Wales, 1963.",
            "Berhenti bicara ke orang lain.",
            "Aturan dan kosakata sendiri.",
            "Novel dan puisi.",
            "Dipisahkan supaya sembuh.",
            "9 Maret 1993.",
            "Masih punya suara?",
        ],
        caption_hi=["", "bahasa", "menghilang", "1963", "berhenti", "kosakata", "novel", "dipisahkan", "1993", "suara"],
        stamps=[["1963", 3], ["2", 2]],
        sfx={
            "00_hook": "page",
            "01_tanya": "page",
            "02_relate": "rustle",
            "03_setup": "door",
            "04_tension": "tick",
            "05_tension": "page",
            "06_tension": "page",
            "07_turn": "clunk",
            "08_consequence": "boom",
            "99_loop": "boom",
        },
        bed="audio/EP10/bed.wav",
        plate="paper",
        sumber=(
            "VERIFIED 2026-11-06 — June-Alison dan Jennifer Gibbons, kembar identik, lahir 11 April 1963 di rumah sakit "
            "militer Aden (orang tua Aubrey dan Gloria, keturunan Barbados), besar di Haverfordwest, Wales; berkomunikasi "
            "hanya satu sama lain; istilah pers: idioglossia/cryptophasia. Menulis fiksi di kamar bersama: June 'The "
            "Pepsi-Cola Addict' (1982), Jennifer 'Discomania'. 1981 tindak pidana remaja; 1982 dijatuhi penahanan tak "
            "tentu di Broadmoor (Mental Health Act), total 11 tahun. Jennifer meninggal 9 Maret 1993, usia 29, saat "
            "dipindahkan ke Caswell Clinic, Bridgend; sebab resmi miokarditis akut, tanpa jejak obat/racun, tanpa kondisi "
            "jantung sebelumnya. June masih hidup (BBC 2023; Wales Barat). KOREKSI: bukan June yang meninggal 1993. Klaim "
            "'bahasa rahasia' dibantah June (2023): mereka bicara Inggris dengan gangguan wicara berat + slang Kreol "
            "Bajan, sehingga tak terdengar seperti bahasa Inggris. Sumber: Wikipedia (en) June and Jennifer Gibbons; BBC "
            "News 26 Des 2023; MIT Press. Buku Marjorie Wallace belum dibaca langsung."
        ),
    ),

    # ─────────────────────────────────────────────── ANEH ──
    dict(
        ep="EP11", day=1, slot="siang", jam="12.30", series="ANEH", pov="B",
        title="TUJUH PULUH DUA DETIK YANG TIDAK PERNAH TERULANG",
        thumb=["72", "DETIK"], thumb_text="72 DETIK",
        durasi=52,
        protagonis="Jerry Ehman, astronom yang membaca hasil cetak teleskop.",
        mau="Menemukan sesuatu di antara derau yang tidak berarti.",
        hambatan="Selama lima puluh tahun, tidak ada yang muncul dua kali.",
        tanaman="Sinyal itu datang tepat di frekuensi hidrogen — frekuensi paling masuk akal untuk mengirim pesan.",
        hook="1977. Sinyal itu datang di frekuensi hidrogen, 72 detik, lalu berhenti selamanya.",
        hook_alt="Satu urutan huruf di kertas printer: 6 E Q U J 5. Itu bukan pesan.",
        tanya="Kalau bukan dari Bumi, dari mana sinyal 72 detik itu datang?",
        entitas="sinyal",
        celah="Kalau itu bukan pesan, kenapa muncul di frekuensi yang paling masuk akal untuk pesan?",
        gambar_melekat="Huruf 6EQUJ5 tercetak di kertas printer, dikelilingi angka.",
        beats=[
            ("setup", "15 Agustus 1977. Teleskop Big Ear di Ohio menyapu langit, seperti biasa."),
            ("setup", "Semalam itu, komputer mencetak satu urutan aneh: 6 E Q U J 5."),
            ("tension", "Itu bukan pesan. Itu kode kekuatan sinyal, naik lalu turun, dalam 72 detik."),
            ("tension", "Sinyalnya datang di frekuensi 1420 MHz."),
            ("tension", "Frekuensi yang sama yang dipancarkan hidrogen di seluruh alam semesta."),
            ("tension", "Frekuensi yang paling masuk akal untuk dipakai mengirim pesan."),
            ("tension", "Ehman menulis satu kata di pinggir kertas itu: Wow."),
            ("turn", "Selama empat puluh tahun, teleskop lain mencari ke titik yang sama."),
            ("turn", "Tidak pernah ada lagi. Dan sinyal itu datang dari arah tanpa bintang."),
            ("consequence", "Dia cukup lama untuk dicatat. Tidak cukup lama untuk dipahami."),
            ("consequence", "Yang tersisa hanya satu kata di pinggir kertas, ditulis oleh orang yang juga tidak tahu."),
        ],
        turn_quote="“Itu pesan dari peradaban lain.”",
        turn_verdict="Sinyal itu tidak pernah terulang, dan datang dari arah tanpa bintang yang diketahui.",
        loop="Tujuh puluh dua detik. Sejak itu, tidak ada apa-apa. Hanya satu kata di pinggir kertas.",
        cues=["15 AGU 1977", "6EQUJ5", "1420 MHz", "72 DETIK", "TIDAK PERNAH LAGI"],
        visual="Kertas printer dengan huruf 6EQUJ5; grafik 72 detik; peta langit kosong.",
        plate="signal",
        sumber=(
            "VERIFIED 2026-11-06 — 15 Agustus 1977, ±22.16 waktu lokal, teleskop Big Ear Ohio State (transit, tak bisa "
            "digerakkan) merekam sinyal pita sempit 72 detik — durasi maksimum satu titik langit melintas di berkas "
            "teleskop — dekat 1420 MHz, garis hidrogen netral (acuan Cocconi–Morrison 1959). Intensitas dicatat skala 0-9 "
            "lalu A-Z; Jerry R. Ehman melihat deret '6EQUJ5', melingkarinya dengan tinta merah, menulis 'Wow!' di margin. "
            "Puncak 'U' ±30 kali derau. Arah Sagitarius, dekat Tau Sagittarii. Muncul hanya di satu dari dua tanduk "
            "penerima (terpisah ±3 menit sapuan) — argumen melawan interferensi lokal; tanpa drift frekuensi selama 72 "
            "detik. Lebih dari 50 pengamatan ulang gagal, termasuk survei Breakthrough Listen 2020. Hipotesis komet "
            "Antonio Paris (2016/2017; 266P/Christensen, P/2008 Y2) ditolak sebagian besar astronom; reanalisis data asli "
            "2024 (kolaborasi 'Arecibo Wow') menyimpulkan sinyal lebih kuat dari perkiraan 1977 sehingga model komet "
            "makin sulit. Sumber: esovitae; decodingtheunknown; monkeyandelf (ringkasan 2026). Makalah asli belum dibaca."
        ),
    ),
    dict(
        ep="EP12", day=2, slot="siang", jam="12.30", series="ANEH", pov="A",
        title="KOTA YANG MENGOBATI MEREKA DENGAN CARA YANG SAMA",
        thumb=["MENARI", "SAMPAI MATI"], thumb_text="SAMPAI MATI",
        durasi=54,
        protagonis="Frau Troffea, perempuan pertama yang menari di jalan Strasbourg.",
        mau="Berhenti menari.",
        hambatan="Tubuhnya tidak mau berhenti, dan kota memberinya satu-satunya obat yang salah.",
        tanaman="Kota itu tidak menghentikan mereka. Dokter menyarankan sebaliknya.",
        hook="1518. Kota itu menyuruh mereka terus menari, sampai ratusan orang tidak bisa berdiri.",
        hook_alt="Ratusan orang menari di jalan selama berhari-hari. Sebagian tidak selamat.",
        tanya="Kenapa mereka terus menari sampai ratusan orang tidak bisa berdiri?",
        entitas="orang",
        celah="Kenapa kota memilih menambah musik, bukan menghentikan mereka?",
        gambar_melekat="Kaki telanjang berlumur darah di atas batu jalan.",
        beats=[
            ("setup", "Juli 1518. Strasbourg, wilayah yang sekarang masuk Prancis."),
            ("setup", "Seorang perempuan bernama Frau Troffea mulai menari di jalan."),
            ("tension", "Dia menari berhari-hari. Tanpa musik. Tanpa berhenti."),
            ("tension", "Dalam sebulan, ratusan orang ikut menari."),
            ("tension", "Kota itu tidak menghentikan mereka."),
            ("tension", "Dokter justru menyarankan: biarkan mereka menari. Bangun panggung. Panggil musisi."),
            ("turn", "Obat itu justru makanan penyakitnya."),
            ("turn", "Mereka menari sampai tubuh mereka tidak bisa berdiri."),
            ("consequence", "Beberapa meninggal karena kelelahan dan serangan panas."),
            ("consequence", "Kota itu kelaparan, dilanda wabah, dan penuh ketakutan. Tarian itu berhenti ketika kotanya berhenti panik."),
        ],
        turn_quote="“Mereka kesurupan.”",
        turn_verdict="Mereka kelaparan, ketakutan, dan tidak punya cara lain untuk mengatakannya. Obatnya justru memperburuk.",
        loop="Mereka berhenti menari. Tapi tidak ada yang tahu bagaimana tarian itu dimulai.",
        cues=["JULI 1518", "STRASBOURG", "400 ORANG", "TANPA MUSIK", "SEBAGIAN MENINGGAL"],
        visual="Kaki di batu jalan; siluet orang menari tanpa wajah; panggung kosong.",
        plate="road",
        sumber=(
            "VERIFIED 2026-11-06 — Strasbourg, Alsace (kota bebas Kekaisaran Romawi Suci; kini Prancis), Juli-September "
            "1518. Kronik: perempuan yang dikenal sebagai Frau Troffea mulai menari 14 Juli di jalan berbatu depan "
            "rumahnya tanpa musik; menari terus, berhenti hanya untuk tidur, lalu mulai lagi; 4-6 hari. Dalam beberapa "
            "hari lebih dari 30 orang ikut; dalam sebulan perkiraan 50-400 (kronik keluarga Imlin: 400). Otoritas kota "
            "mulanya menanggapinya sebagai penyakit, bukan kerasukan: menyewa musisi dan membangun panggung besar — "
            "diduga justru mengundang lebih banyak penari. Troffea diangkut kereta ±30 mil ke Saverne, ke kuil Santo "
            "Vitus; ritual: sepatu merah, salib kecil di tangan, salib minyak suci di sol dan punggung sepatu, dupa dan "
            "mantra Latin. Gelombang berhenti akhir Agustus/September 1518. Angka '15 kematian per hari' hanya dari "
            "catatan yang lebih kemudian (Waller) dan diperdebatkan; dari enam kronik sezaman, empat menyebut Troffea "
            "penari pertama. Penjelasan utama (Waller 2008): psikosis massal akibat stres — panen gagal, kelaparan, "
            "wabah, sifilis, ketidakstabilan politik — di dalam kerangka kepercayaan bahwa Santo Vitus mengutuk orang "
            "dengan menari. Sumber: Wikipedia (en); Public Domain Review (Ned Pennant-Rea); Observatory.wiki; Sherman "
            "Theatre."
        ),
    ),
    dict(
        ep="EP13", day=3, slot="siang", jam="12.30", series="ANEH", pov="B",
        title="MEREKA MENUNGGU SESEORANG YANG TIDAK PERNAH DATANG",
        thumb=["MASKER", "TIMAH"], thumb_text="MASKER TIMAH",
        durasi=53,
        protagonis="Miguel Viana dan Manoel Cruz, dua pria di Bukit Vintém, Rio de Janeiro.",
        mau="Menunggu seseorang di tempat yang disebutkan dalam catatan.",
        hambatan="Waktunya tertulis jelas. Orangnya tidak pernah datang.",
        tanaman="Catatan itu menyuruh mereka menunggu, menelan kapsul, lalu memakai masker.",
        hook="1966. Masker timah di wajah mereka. Di saku: catatan berisi perintah menunggu.",
        hook_alt="Mereka memakai setelan resmi dan masker timah. Tidak ada yang tahu untuk apa.",
        tanya="Kenapa mereka menunggu di dalam, padahal tidak ada yang datang menjemput?",
        entitas="masker timah",
        celah="Siapa yang menulis jadwal itu, dan kenapa dia tidak pernah datang?",
        gambar_melekat="Dua masker timah di atas batu, menghadap langit.",
        beats=[
            ("setup", "20 Agustus 1966. Dua pria ditemukan tewas di sebuah bukit di Rio de Janeiro."),
            ("setup", "Mereka memakai setelan resmi. Di wajah mereka, masker timah buatan sendiri."),
            ("tension", "Tidak ada luka. Tidak ada tanda perkelahian."),
            ("tension", "Di saku salah satunya, ada catatan tulisan tangan."),
            ("tension", "Isinya: jam, tempat, dan instruksi untuk menunggu seseorang."),
            ("tension", "Ada juga instruksi untuk menelan kapsul, lalu memakai masker."),
            ("turn", "Mereka melakukan semuanya. Tepat waktu."),
            ("turn", "Orang yang menulis instruksi itu tidak pernah datang — dan uang yang disebut di catatan itu tidak pernah ditemukan."),
            ("consequence", "Selama enam puluh tahun, teorinya bunuh diri atau ritual."),
            ("consequence", "Tapi catatan itu bukan surat perpisahan. Itu jadwal. Dan jadwal butuh orang kedua."),
        ],
        turn_quote="“Itu bunuh diri.”",
        turn_verdict="Catatan itu jadwal pertemuan, bukan surat perpisahan. Orang kedua tidak pernah datang.",
        loop="Dua pria menunggu di bukit itu. Sampai sekarang tidak ada yang tahu siapa yang mereka tunggu.",
        cues=["20 AGU 1966", "2 PRIA", "MASKER TIMAH", "CATATAN", "UANG HILANG"],
        visual="Bukit dengan dua siluet; catatan tangan tak terbaca; dua masker timah di batu.",
        plate="ridge",
        sumber=(
            "VERIFIED 2026-11-06 — 'Caso das Máscaras de Chumbo', Morro do Vintém, Niterói, Rio. Dua teknisi elektronik "
            "dari Campos dos Goytacazes: Manoel Pereira da Cruz dan Miguel José Viana. 17 Agustus 1966 mereka berangkat "
            "dengan alasan membeli bahan elektronik dan mobil di São Paulo; naik bus ke Niterói, membeli jas hujan, air "
            "mineral, dua handuk kecil; ±15.15 berjalan ke jalur bukit, terlihat ±17.00. Jenazah ditemukan 20 Agustus "
            "1966 oleh remaja yang menerbangkan layang-layang. Di lokasi: dua lempeng timah penutup mata (masker), jas "
            "hujan, botol air kosong, handuk, dan catatan di kantong Miguel berbunyi '16:30 estar no local determinado. "
            "18:30 ingerir cápsulas, após efeito proteger metais aguardar sinal máscara'. Pemeriksaan tulisan tangan 1967 "
            "menyimpulkan catatan ditulis Miguel sendiri. Otopsi: tanpa luka, tanpa tanda kekerasan, tanpa racun "
            "terdeteksi, tanpa kontaminasi radioaktif; tubuh berwarna kemerahan. Sebab kematian tak pernah ditetapkan. "
            "Hipotesis yang pernah dipakai polisi (perwira Idovam Ferreira): keduanya mati saat mencoba eksperimen "
            "parapsikologi dengan kapsul tak diketahui isinya. Klaim saksi soal objek di atas bukit 17 Agustus dan uang "
            "yang hilang TIDAK terverifikasi — jangan dipakai sebagai fakta. Sumber: Mega Curioso; Portal Fenomenum; "
            "clubedeastronomia; strangehappen (tinjauan 2026). Laporan polisi 1966/1967 belum dibaca langsung."
        ),
    ),
    dict(
        ep="EP14", day=4, slot="siang", jam="12.30", series="ANEH", pov="D",
        title="DUA KALI DALAM SATU MALAM, DAN TIDAK ADA YANG TERTANGKAP",
        thumb=["SIAPA", "PUN"], thumb_text="SIAPA PUN",
        durasi=52,
        protagonis="Seorang teknisi siaran di Chicago yang melihat sinyalnya diambil alih.",
        mau="Menjaga siaran tetap di jalurnya.",
        hambatan="Seseorang memotong transmisinya, dan dia tidak bisa menghentikannya.",
        tanaman="Pembajakan terjadi dua kali dalam satu malam, di dua saluran berbeda.",
        hook="1987. Dua siaran dibajak dalam satu malam, di dua saluran. Tidak ada yang tertangkap.",
        hook_alt="Di tengah film, gambarnya hilang. Yang muncul: seseorang dengan kepala palsu dan suara rusak.",
        tanya="Kenapa dua siaran bisa dibajak dalam satu malam, dan tidak ada yang tertangkap?",
        entitas="dua siaran",
        celah="Bagaimana satu orang bisa memotong dua transmisi, lalu hilang?",
        gambar_melekat="Layar TV penuh derau dengan siluet kepala di tengahnya.",
        beats=[
            ("setup", "22 November 1987, Chicago. Pukul sembilan malam, saluran WGN menayangkan film."),
            ("setup", "Gambarnya tiba-tiba hilang."),
            ("tension", "Yang muncul: seseorang memakai topeng kepala, dengan suara yang dirusak."),
            ("tension", "Dia bergerak, bicara, dan menempelkan sesuatu ke layar."),
            ("tension", "Sembilan puluh detik kemudian, siaran kembali normal."),
            ("tension", "Dua jam kemudian, saluran lain dibajak lagi. Kali ini lebih lama."),
            ("turn", "Untuk membajak siaran analog, kamu harus tahu di titik mana sinyal bisa dipotong."),
            ("turn", "Itu bukan lelucon. Itu pengetahuan teknis — dan orangnya tidak pernah tertangkap."),
            ("consequence", "FCC menyelidiki bertahun-tahun. Tidak ada nama. Tidak ada tuntutan."),
            ("consequence", "Tiga puluh delapan tahun kemudian, orang itu masih tidak punya wajah."),
        ],
        turn_quote="“Itu iseng anak-anak.”",
        turn_verdict="Dua pembajakan dalam satu malam butuh pengetahuan teknis. Dan pelakunya tidak pernah tertangkap.",
        loop="Sembilan puluh detik, dua saluran, nol tersangka.",
        cues=["22 NOV 1987", "CHICAGO", "90 DETIK", "2 KALI", "TIDAK TERTANGKAP"],
        visual="Layar TV analog penuh derau; siluet kepala di bingkai 4:3; ruang kontrol gelap.",
        plate="signal",
        sumber=(
            "VERIFIED 2026-11-06 — 22 November 1987, Chicago. 21.14 waktu setempat: segmen olahraga WGN-TV (sembilan "
            "malam) dipotong ±28 detik oleh figur bertopeng Max Headroom, latar logam bergelombang berputar, tanpa audio; "
            "kru WGN masih di studio sehingga sinyal bisa direbut kembali cepat. 23.15: WTTW (afiliasi PBS) sedang "
            "menayangkan serial Doctor Who ('Horror of Fang Rock') dibajak ±90 detik, kali ini dengan audio: kalimat acak "
            "soal 'world newspaper nerds', lalu adegan ditepuk dengan pemukul lalat sambil berteriak. Krunya sudah "
            "pulang, sehingga tidak ada yang menghentikan. Metodenya bukan menyambung kabel: kedua stasiun memakai "
            "studio-to-transmitter link gelombang mikro menuju pemancar di atas gedung tinggi (Sears Tower/John Hancock), "
            "dan penyusup memancarkan sinyal lebih kuat ke penerima ('capture effect'). Kebutuhan: pemancar directional "
            "mahal, titik tinggi dengan garis pandang ke dua pemancar, pengetahuan teknis tingkat insinyur siaran/radio "
            "amatir berlisensi; direktur teknik WTTW saat itu, Al Skierkiewicz, menyebut pelakunya kemungkinan insinyur "
            "siaran atau operator radio amatir. FCC dan FBI menyelidiki bersama; FBI membuat enam cetakan foto dari pita "
            "WTTW; tidak ada sidik jari, tidak ada peralatan, tidak ada nama. Berkas tidak pernah ditutup dengan "
            "tersangka; daluwarsa federal (lima tahun) sudah habis sejak lama, jadi pelaku tak bisa dituntut. Klaim 2010 "
            "di Reddit ('saya kenal mereka') tidak pernah terverifikasi. Sumber: WTTW retrospective 2017; "
            "Vice/Motherboard (laporan teknis FBI); historicmysteries; csintresearch (arsip kasus, cek terakhir Jan "
            "2026)."
        ),
    ),
    dict(
        ep="EP15", day=5, slot="siang", jam="12.30", series="ANEH", pov="D",
        title="TULANG YANG MEMBUKTIKAN KITA TIDAK SENDIRIAN",
        thumb=["60.000", "TAHUN"], thumb_text="BUKAN KITA",
        durasi=57,
        protagonis="Tim penggalian Gua Liang Bua, Flores, 2003.",
        mau="Mencari bukti manusia purba yang bermigrasi lewat Indonesia.",
        hambatan="Yang mereka temukan tidak cocok dengan apa pun di buku teks.",
        tanaman="Tengkoraknya terlalu kecil untuk manusia modern, terlalu tua untuk dianggap kelainan.",
        hook="Enam puluh ribu tahun. Tingginya satu meter, otaknya sepertiga otak kita.",
        hook_alt="Tingginya satu meter. Otaknya sepertiga otak kita. Dan dia hidup saat manusia modern sudah ada.",
        tanya="Bagaimana dia bertahan puluhan ribu tahun dengan otak sepertiga otak kita?",
        entitas="dia",
        celah="Kalau bukan manusia modern yang sakit, lalu apa yang hidup di gua itu?",
        gambar_melekat="Tengkorak kecil di samping alat batu, di lantai gua.",
        beats=[
            ("setup", "2003. Sebuah tim penggalian bekerja di Gua Liang Bua, Flores."),
            ("setup", "Mereka mencari jejak migrasi manusia purba lewat Indonesia."),
            ("tension", "Mereka menemukan kerangka yang tidak sesuai dengan apa pun yang ada di buku."),
            ("tension", "Tingginya sekitar satu meter. Volume otaknya sepertiga otak kita."),
            ("tension", "Di sekitarnya ada alat batu. Ada bukti perburuan."),
            ("tension", "Umurnya direvisi 2016: sekitar 100.000 sampai 60.000 tahun, bukan 18.000."),
            ("turn", "Sebagian ilmuwan bersikeras: ini bukan spesies baru. Ini manusia modern yang sakit."),
            ("turn", "Perdebatan itu berlangsung lebih dari sepuluh tahun."),
            ("consequence", "Analisis gigi dan rahang menyimpulkan: ini bukan kita."),
            ("consequence", "Mereka hidup di pulau itu puluhan ribu tahun. Lalu menghilang, dan ceritanya ikut hilang."),
        ],
        turn_quote="“Itu manusia modern yang sakit.”",
        turn_verdict="Gigi dan rahangnya bukan milik kita. Ini kerabat yang berpisah jauh lebih lama.",
        loop="Satu meter tingginya. Delapan belas ribu tahun. Dan kita baru tahu bahwa kita tidak pernah sendirian.",
        cues=["2003", "LIANG BUA", "1 METER", "60.000 TAHUN", "BUKAN KITA"],
        visual="Penampang gua; siluet satu meter di samping skala manusia modern; alat batu.",
        plate="ridge",
        sumber=(
            "VERIFIED 2026-11-06 — 2 September 2003, Gua Liang Bua, Flores barat, tim gabungan Australia-Indonesia "
            "(Michael Morwood, Peter Brown). Ditemukan LB1: kerangka perempuan dewasa ±30 tahun, tinggi ±1,06 m, volume "
            "otak ±380-420 cc (sebanding simpanse), bukan fosil (belum termineralisasi); plus bagian dari sedikitnya "
            "sebelas individu lain. Diumumkan sebagai spesies baru di Nature, Oktober 2004. ALAT BATU: Oldowan-like "
            "(serpih, chopper, serpih teretouch) dari batu vulkanik dan chert lokal; tanpa teknik prepared-core. Fauna: "
            "Stegodon kerdil (banyak juvenil, sebagian bertanda potong) dan hewan endemik Flores. TANGGAL: angka lama "
            "18.000 tahun (dan 12.000) berasal dari sampel radiokarbon di unit sedimen yang menutupi, bukan dari "
            "tulangnya. Revisi stratigrafi Sutikna dkk., Nature 532 (Maret 2016): semua sisa kerangka H. floresiensis "
            "100.000-60.000 tahun; alat batu 190.000-50.000 tahun. Mata Menge (So'a Basin, ±70 km timur): rahang bawah "
            "dan gigi ±700.000 tahun (van den Bergh dkk., Nature 2016). Alat batu di Wolo Sege ≥1 juta tahun. Penyebab "
            "kepunahan tidak pasti: letusan gunung, perubahan iklim/habitat, atau kedatangan H. sapiens (yang mencapai "
            "kawasan ±50.000 tahun lalu). DNA tidak berhasil diambil karena tropis. Hipotesis 'manusia modern yang sakit' "
            "(microcephaly, Laron, Down syndrome) ditolak sebagian besar spesialis, termasuk tinjauan PLOS One 2016; re- "
            "dating 2016 juga melemahkannya karena sisa itu mendahului bukti H. sapiens di kawasan. Sumber: Australian "
            "Museum; Sutikna dkk. 2016 (Nature 532:366); van den Bergh dkk. 2016 (Nature 534:245); Spoken Past; "
            "homininhistory."
        ),
    ),
    dict(
        ep="EP16", day=6, slot="siang", jam="12.30", series="ANEH", pov="B",
        title="TAWA YANG MENYEBAR SEPERTI WABAH, TANPA SATU PUN VIRUS",
        thumb=["TIDAK BISA", "BERHENTI"], thumb_text="TIDAK BISA BERHENTI",
        durasi=52,
        protagonis="Tiga murid perempuan di sekolah Kashasha, Tanganyika.",
        mau="Menjalani hari sekolah seperti biasa.",
        hambatan="Tubuh mereka mulai tertawa, dan tidak berhenti.",
        tanaman="Tidak ada virus, tidak ada racun, tidak ada penyebab fisik yang ditemukan.",
        hook="1962. Ratusan orang tertawa selama berbulan-bulan. Tidak ada virus yang ditemukan.",
        hook_alt="Tidak ada virus. Yang menyebar hanya tawa — dan tidak ada yang bisa menghentikannya.",
        tanya="Kenapa tertawa bisa menular, padahal tidak ada virus yang ditemukan?",
        entitas="orang",
        celah="Kalau bukan penyakit, apa yang menular di sekolah itu?",
        gambar_melekat="Bangku kelas kosong dengan papan tulis penuh tulisan pudar.",
        beats=[
            ("setup", "Januari 1962. Sebuah sekolah di desa Kashasha, Tanganyika."),
            ("setup", "Tiga murid perempuan mulai tertawa."),
            ("tension", "Tawanya tidak berhenti di jam pelajaran."),
            ("tension", "Dalam beberapa hari, puluhan murid ikut tertawa. Beberapa menangis."),
            ("tension", "Dalam dua bulan, sekolah itu ditutup."),
            ("tension", "Wabahnya pindah ke sekolah lain. Dan sekolah berikutnya."),
            ("tension", "Sebagian murid tertawa selama berhari-hari, bahkan berminggu-minggu."),
            ("turn", "Tidak ada virus yang ditemukan. Tidak ada racun. Tidak ada penyebab fisik."),
            ("turn", "Yang ada: sekolah baru, aturan baru, dan anak-anak yang tidak pernah dimintai pendapat."),
            ("consequence", "Yang menyebar bukan penyakit. Yang menyebar adalah tekanan."),
            ("consequence", "Tawanya berhenti setelah delapan belas bulan. Tekanannya tidak."),
        ],
        turn_quote="“Itu wabah penyakit.”",
        turn_verdict="Tidak ada virus, tidak ada racun. Yang menyebar adalah tekanan, dalam bentuk yang bisa dilihat semua orang.",
        loop="Ratusan orang tertawa karena tidak punya cara lain untuk bicara.",
        cues=["JAN 1962", "KASHASHA", "1.000 ORANG", "18 BULAN", "TANPA VIRUS"],
        visual="Kelas dengan bangku kosong; gelombang abstrak menyebar antar bangku; koridor sekolah.",
        plate="shelter",
        sumber=(
            "VERIFIED 2026-11-06 — 30 Januari 1962, sekolah asrama misi di Kashasha, tepi barat Danau Victoria, "
            "Tanganyika (kini Tanzania): tiga murid perempuan mulai tertawa. Dalam hitungan hari menyebar; 18 Maret 1962 "
            "sekolah ditutup setelah 95 dari 159 murid (usia 12-18) terkena. Gejala: tawa tak terkendali disertai "
            "menangis, pingsan, sesak, ruam, nyeri; episode dari beberapa jam sampai 16 hari (rata-rata ±7 hari); tidak "
            "ada kematian yang tercatat. Sekolah dibuka lagi 21 Mei 1962, 57 murid kembali terkena dalam beberapa minggu, "
            "lalu ditutup lagi akhir Juni. Menyebar ke Nshamba (April-Mei: 217 orang, sebagian besar remaja, dalam 34 "
            "hari), Kanyangereka, dan Ramashenye Girls' Middle School (Juni: 48 murid), lalu desa-desa lain; reda setelah "
            "±18 bulan (pertengahan 1964). Guru dan orang dewasa di posisi otoritas nyaris tidak terkena. Penyelidikan: "
            "A.M. Rankin (Makerere University College) dan P.J. Philip (petugas medis pemerintah Bukoba); sampel darah, "
            "makanan, air diperiksa; tidak ada patogen, racun, atau defisiensi; laporan di Central African Journal of "
            "Medicine, 1963 — kesimpulan: mass psychogenic illness. KONTEKS: Tanganyika merdeka dari Inggris Desember "
            "1961, beberapa minggu sebelumnya; tekanan harapan baru di sekolah misi. CATATAN ANGKA: '1.000 orang di 14 "
            "sekolah' muncul di rangkuman kemudian dan tidak ada di laporan 1963 — naskah memakai angka laporan asli dan "
            "menyebut angka besar sebagai klaim yang diperdebatkan. Sumber: Rankin & Philip 1963 (via rangkuman bygonist, "
            "livelyhistory, boingboing); Pringle 2019; Hempelmann."
        ),
    ),

    # ─────────────────────────────────────────────── BENCANA ──
    dict(
        ep="EP17", day=6, slot="pagi", jam="07.00", series="BENCANA", pov="A",
        title="SUARA YANG TERDENGAR SEJAUH 4.800 KILOMETER",
        thumb=["4.800", "KILOMETER"], thumb_text="4.800 KM",
        durasi=56,
        protagonis="Seorang kapten kapal di Selat Sunda, pagi 27 Agustus 1883.",
        mau="Melewati selat itu dan sampai di pelabuhan berikutnya.",
        hambatan="Gunung di depannya sedang membelah dirinya sendiri.",
        tanaman="Suara itu tidak hanya terdengar. Gelombang tekanannya tercatat di barometer seluruh dunia.",
        hook="1883. Suara itu terdengar 4.800 kilometer jauhnya. Gelombang tekanannya tercatat di seluruh dunia.",
        hook_alt="Itu suara paling keras yang pernah dicatat manusia. Sebagian orang yang mendengarnya tidak pernah mendengar lagi.",
        tanya="Kalau suaranya terdengar 4.800 kilometer jauhnya, apa yang terjadi di dekatnya?",
        entitas="suara itu",
        celah="Seberapa jauh sebuah ledakan merambat, kalau udaranya sendiri yang bergerak?",
        gambar_melekat="Barometer di Eropa mencatat gelombang dari gunung di Selat Sunda.",
        beats=[
            ("setup", "Krakatau. Gunung kecil di Selat Sunda, antara Jawa dan Sumatra."),
            ("setup", "Sejak Mei 1883, gunung itu mengeluarkan asap dan abu."),
            ("tension", "27 Agustus, empat ledakan besar terjadi dalam beberapa jam."),
            ("tension", "Ledakan terbesar terdengar sampai Australia dan Pulau Rodrigues."),
            ("tension", "Itu seperdelapan permukaan bumi."),
            ("tension", "Gelombang tekanannya tercatat di barometer di seluruh dunia."),
            ("turn", "Yang paling mengejutkan bukan ledakannya."),
            ("turn", "Gelombang tekanan itu berputar mengelilingi bumi beberapa kali — udara di atas kita bergerak seperti air."),
            ("consequence", "Tsunaminya mencapai tiga puluh meter. Lebih dari tiga puluh enam ribu orang meninggal."),
            ("consequence", "Bertahun-tahun setelah itu, matahari terbenam di Eropa berwarna merah menyala. Tidak ada yang tahu kenapa."),
        ],
        turn_quote="“Gunungnya meletus.”",
        turn_verdict="Gelombang tekanannya berputar mengelilingi bumi beberapa kali. Udara di atas kita bergerak seperti air.",
        loop="Suara itu tidak berhenti di 4.800 kilometer. Ia berputar mengelilingi dunia, dan langit Eropa berubah.",
        cues=["27 AGU 1883", "KRAKATAU", "4.800 KM", "30 METER", "DUNIA BERUBAH"],
        visual="Kolom abu di garis pantai; peta radius suara; grafik barometer dunia.",
        plate="plume",
        sumber=(
            "VERIFIED 2026-11-06 — Krakatau, Selat Sunda. Aktivitas dimulai Mei 1883 (asap/abu, letusan kecil); puncak "
            "26-27 Agustus 1883. 27 Agustus: empat ledakan besar antara 05.30 dan 10.02; ledakan ketiga pukul 10.02 "
            "dianggap suara terkeras yang tercatat instrumen. Suara terdengar jelas 3.110 km jauhnya di Perth (penduduk "
            "mengira tembakan artileri, mengirim tim mencari kapal dalam kesulitan) dan 4.800 km jauhnya di Pulau "
            "Rodrigues dekat Mauritius (petugas kolonial mencatat 'raungan meriam berat' dan mengira ada pertempuran "
            "laut). Di dekat sumber, tekanan melampaui batas teoretis bunyi di udara (±194 dB), sehingga yang merambat "
            "adalah gelombang tekanan, bukan bunyi dalam arti akustik biasa. Gelombang tekanan terekam barometer/barograf "
            "di London, Paris, Washington, Tokyo, New York; terukur ±5 hari, mengelilingi bumi setidaknya tiga kali penuh "
            "(rangkuman populer: ±3,5-4 kali). Dua pertiga pulau runtuh ke laut; tsunami sampai ±41 m di tempat terdekat; "
            "295 kota/pesisir rusak; korban resmi kolonial Belanda 36.417 (perkiraan lain lebih tinggi); ±90% korban "
            "akibat tsunami, bukan letusan. Debu mencapai stratosfer/mesosfer (±43-80 km menurut berbagai ukuran); suhu "
            "global turun; matahari terbenam merah di Eropa berbulan-bulan. Sumber: Wikipedia (1883 eruption of "
            "Krakatau); volcanodb; geographyworlds; missedhistory; spacedaily."
        ),
    ),
    dict(
        ep="EP18", day=7, slot="pagi", jam="07.00", series="BENCANA", pov="D",
        title="GUNUNG DI SUMBAWA YANG MENCURI SATU MUSIM DARI EROPA",
        thumb=["MUSIM", "HILANG"], thumb_text="MUSIM HILANG",
        durasi=57,
        protagonis="Seorang petani di Eropa, 1816, yang menanam di bulan yang salah.",
        mau="Memanen seperti tahun-tahun sebelumnya.",
        hambatan="Musimnya tidak datang, dan tidak ada yang tahu kenapa.",
        tanaman="Debu dari sebuah gunung di Sumbawa terbang ke stratosfer dan memantulkan sinar matahari.",
        hook="1815. Gunung di Sumbawa meletus. Setahun kemudian, salju turun di bulan Juni.",
        hook_alt="Satu gunung di Sumbawa meledak. Setahun kemudian, orang di Eropa kelaparan.",
        tanya="Kalau gunungnya di Sumbawa, kenapa salju turun di benua lain setahun kemudian?",
        entitas="gunung",
        celah="Bagaimana debu dari satu pulau bisa mencuri satu musim di benua lain?",
        gambar_melekat="Ladang gandum tertutup salju di bulan Juni.",
        beats=[
            ("setup", "April 1815. Gunung Tambora di Sumbawa meletus."),
            ("setup", "Itu letusan terbesar yang tercatat dalam sejarah modern."),
            ("tension", "Abu dan gas sulfurnya naik ke stratosfer."),
            ("tension", "Di sana, sulfur berubah menjadi partikel yang memantulkan sinar matahari."),
            ("tension", "Selama setahun berikutnya, bumi menerima lebih sedikit panas."),
            ("tension", "1816 dikenal sebagai tahun tanpa musim panas."),
            ("tension", "Di Amerika, salju turun di bulan Juni. Tanaman gagal."),
            ("turn", "Kita menyebut letusan itu bencana lokal."),
            ("turn", "Tapi debunya terbang setengah bumi dan mencuri satu musim dari seluruh benua."),
            ("consequence", "Di Eropa, harga roti meledak. Kerusuhan terjadi di banyak kota."),
            ("consequence", "Satu gunung di Sumbawa mengubah harga roti di London, dan tidak ada yang melihat hubungannya saat itu."),
        ],
        turn_quote="“Itu bencana lokal di Indonesia.”",
        turn_verdict="Debunya terbang setengah bumi, mencuri satu musim, dan membuat orang Eropa kelaparan.",
        loop="Satu gunung di Sumbawa. Satu musim yang hilang di benua lain.",
        cues=["APR 1815", "TAMBORA", "1816", "TANPA MUSIM PANAS", "ROTI MAHAL"],
        visual="Lapisan abu di stratosfer; peta aliran sulfur; ladang gagal panen.",
        plate="plume",
        sumber=(
            "VERIFIED 2026-11-06 — Gunung Tambora, Sumbawa (kini Nusa Tenggara Barat). Aktivitas meningkat sejak 1812; "
            "letusan mulai 5 April 1815, puncak 10-15 April 1815. VEI 7 — letusan terbesar dalam sejarah tercatat, ±4-10 "
            "kali energi Krakatau 1883; material terlempar diperkirakan 100-180 km³; tinggi kolom ±43 km; guncangan "
            "terdengar sampai Ternate (±1.400 km) dan abu jatuh ratusan kilometer jauhnya. Letusan berhenti 15 Juli 1815; "
            "aktivitas kecil lagi Agustus 1819. Dampak global: selubung aerosol sulfat di stratosfer → 1816 disebut Tahun "
            "Tanpa Musim Panas. New England/Kanada: 'dry fog' yang tidak hilang oleh angin atau hujan, matahari meredup "
            "sampai bintik matahari terlihat dengan mata telanjang; salju turun 6 Juni 1816 di New York dan Maine; Quebec "
            "hampir 30 cm; es masih ditemukan di danau/rivers sampai Pennsylvania pada Agustus; panen jagung gagal (hanya "
            "±seperempat yang bisa dipakai). Eropa: suhu turun ±1-2 °C; gandum, rye, barley, oat naik tajam sampai 1817; "
            "Irlandia kelaparan; Jerman panen gagal total → demonstrasi di pasar gandum dan toko roti, lalu kerusuhan, "
            "pembakaran, penjarahan di banyak kota; di East Anglia harga gandum naik ±33% antara Maret-Mei 1816 → "
            "kerusuhan 'Bread or Blood', lima orang dieksekusi. Diperkirakan sampai ±71.000 kematian global (kelaparan + "
            "epidemi typhus). Sumber: Wikipedia (Mount Tambora; Year Without a Summer); AAAS Scientia; Historical "
            "Climatology ('Bread or Blood'); markvoganweather."
        ),
    ),
    dict(
        ep="EP19", day=7, slot="siang", jam="12.30", series="BENCANA", pov="B",
        title="LEDAKAN YANG TIDAK MENINGGALKAN APA PUN UNTUK DIPEGANG",
        thumb=["TANPA", "KAWAH"], thumb_text="TANPA KAWAH",
        durasi=54,
        protagonis="Leonid Kulik, ilmuwan yang memimpin ekspedisi pertama ke Siberia, 1927.",
        mau="Menemukan kawah meteorit dan besinya.",
        hambatan="Tidak ada kawah, tidak ada pecahan, tidak ada logam.",
        tanaman="Dua ribu kilometer persegi hutan rebah menjauhi satu titik — dan di titik itu tidak ada apa-apa.",
        hook="1908. Dua ribu kilometer persegi hutan rebah, semuanya menjauhi satu titik.",
        hook_alt="Pohon-pohon rebah serentak, semua menjauhi satu titik. Di tengahnya, kosong.",
        tanya="Kenapa hutan rebah menjauhi satu titik, tapi tidak ada kawah di titik itu?",
        entitas="hutan",
        celah="Kalau ada ledakan sebesar itu, di mana batunya?",
        gambar_melekat="Ribuan pohon rebah radial, dan satu titik kosong di tengahnya.",
        beats=[
            ("setup", "30 Juni 1908. Pagi. Siberia tengah."),
            ("setup", "Saksi melihat langit terbelah. Lalu ada cahaya, dan angin panas."),
            ("tension", "Delapan ratus kilometer jauhnya, orang mendengar ledakan."),
            ("tension", "Gelombang tekanannya tercatat di stasiun cuaca di Inggris."),
            ("tension", "Hutan di bawahnya rebah. Dua ribu kilometer persegi."),
            ("tension", "Semua pohon jatuh menjauhi satu titik pusat."),
            ("tension", "Ekspedisi pertama baru datang sembilan belas tahun kemudian."),
            ("turn", "Kulik mencari kawah. Dia mencari batu. Dia mencari besi."),
            ("turn", "Yang dia temukan justru sebaliknya: benda itu tidak pernah sampai ke tanah."),
            ("consequence", "Ia meledak di udara, beberapa kilometer di atas hutan."),
            ("consequence", "Ledakan sekuat itu, dan tidak meninggalkan apa pun untuk dipegang."),
        ],
        turn_quote="“Ada meteorit yang menabrak bumi.”",
        turn_verdict="Tidak ada kawah dan tidak ada pecahan. Benda itu meledak di udara sebelum menyentuh tanah.",
        loop="Hutan rebah menjauhi satu titik kosong. Sampai sekarang, titik itu tetap kosong.",
        cues=["30 JUN 1908", "TUNGUSKA", "2.000 KM²", "TANPA KAWAH", "MELEDAK DI UDARA"],
        visual="Pola pohon rebah radial dari atas; satu titik kosong di pusatnya; hutan Siberia.",
        plate="ridge",
        sumber="NEEDS-SOURCE — Peristiwa Tunguska 1908; laporan ekspedisi Kulik belum dibaca langsung.",
    ),
    dict(
        ep="EP20", day=7, slot="malam", jam="19.30", series="BENCANA", pov="B",
        title="YANG MEMBUNUH MEREKA ADALAH UDARA YANG TURUN",
        thumb=["DANAU", "BERNAPAS"], thumb_text="DANAU BERNAPAS",
        durasi=58,
        protagonis="Warga desa di lembah Danau Nyos, Kamerun.",
        mau="Tidur seperti malam-malam sebelumnya.",
        hambatan="Malam itu, danau di atas mereka mengeluarkan napas.",
        tanaman="Tidak ada letusan, tidak ada lava, tidak ada api. Tidak ada yang bisa dilihat.",
        hook="1986. Tidak ada letusan, tidak ada lava. Pagi berikutnya 1.700 orang tidak bangun.",
        hook_alt="Tidak ada letusan. Tidak ada lava. Tidak ada api. Hanya udara yang turun ke lembah.",
        tanya="Kalau tidak ada letusan dan tidak ada lava, apa yang membunuh mereka?",
        entitas="1.700 orang",
        celah="Kalau bukan gunung, apa yang membunuh satu lembah dalam satu malam?",
        gambar_melekat="Danau hitam yang tenang, dan lembah di bawahnya yang sunyi.",
        beats=[
            ("setup", "21 Agustus 1986. Danau Nyos, Kamerun."),
            ("setup", "Malam itu, danau mengeluarkan awan gas karbon dioksida."),
            ("tension", "Gas itu tidak berwarna. Tidak berbau. Lebih berat dari udara."),
            ("tension", "Ia turun ke lembah, tempat orang-orang tidur."),
            ("tension", "Pagi berikutnya, 1.700 orang meninggal. Bersama ribuan ternak."),
            ("tension", "Yang selamat bangun dengan luka, tanpa tahu apa yang terjadi."),
            ("turn", "Semua orang pertama mengira gunung meletus."),
            ("turn", "Tidak ada letusan. Gas itu tersimpan di dasar danau selama bertahun-tahun, di bawah tekanan."),
            ("consequence", "Yang membunuh mereka bukan air, bukan api, bukan gunung. Yang membunuh mereka adalah udara."),
            ("consequence", "Danau itu masih menyimpan gasnya. Pipa yang dipasang sekarang satu-satunya alasan ia masih tenang."),
        ],
        turn_quote="“Gunungnya meletus.”",
        turn_verdict="Tidak ada letusan. Gas tersimpan di dasar danau, lalu turun ke lembah saat orang tidur.",
        loop="Sebuah danau bernapas sekali, dan satu lembah tidak pernah bangun.",
        cues=["21 AGU 1986", "DANAU NYOS", "CO₂", "1.700 ORANG", "PIPA DEGASSING"],
        visual="Danau dari atas; lapisan gas turun ke lembah; pipa degassing di permukaan.",
        plate="water",
        sumber="NEEDS-SOURCE — Danau Nyos 1986; program degassing sejak 2001; mekanisme limnik belum dikutip langsung.",
    ),

    # ─────────────────────────────────────────────── HARGA ──
    dict(
        ep="EP21", day=6, slot="malam", jam="19.30", series="HARGA", pov="A",
        title="MEREKA DIAJARI MENJILAT KUAS, SETIAP KALI",
        thumb=["RAHANG", "RONTOK"], thumb_text="RAHANG RONTOK",
        durasi=58,
        protagonis="Seorang pelukis dial jam di pabrik Orange, New Jersey, 1917.",
        mau="Mendapat upah, dan tetap sehat.",
        hambatan="Perusahaannya mengajari dia menjilat kuas berisi radium.",
        tanaman="Dokter perusahaan punya satu diagnosis untuk semua gejala itu: sifilis.",
        hook="1917. Mereka diajari menjilat kuas berisi radium. Dokter perusahaan menyebutnya sifilis.",
        hook_alt="Mereka diberi tahu cat itu aman. Mereka bahkan diberi tahu bahwa cat itu menyehatkan.",
        tanya="Kenapa dokternya menyebut sifilis, padahal dia tahu itu radium?",
        entitas="orang",
        celah="Kenapa perusahaan punya diagnosis sendiri untuk penyakit yang ia sebabkan?",
        gambar_melekat="Kuas kecil di dekat bibir, dan pot cat yang menyala dalam gelap.",
        beats=[
            ("setup", "1917. Sebuah pabrik jam di Orange, New Jersey."),
            ("setup", "Perempuan muda melukis angka di dial jam dengan cat yang menyala dalam gelap."),
            ("tension", "Cat itu mengandung radium."),
            ("tension", "Untuk membuat ujung kuas runcing, mereka diajari menjilatnya."),
            ("tension", "Setiap kali selesai satu angka."),
            ("tension", "Bertahun-tahun kemudian, gigi mereka mulai lepas sendiri."),
            ("tension", "Rahang mereka membusuk. Anemia. Tulang mereka patah tanpa sebab."),
            ("turn", "Dokter perusahaan menyebut penyebabnya: sifilis."),
            ("turn", "Padahal perusahaan sudah mengukur radiasi di tubuh para pekerja itu sejak lama."),
            ("consequence", "Mereka menggugat. Dan menang."),
            ("consequence", "Hukum ketenagakerjaan Amerika berubah karena mereka. Mereka tidak sempat menikmatinya."),
        ],
        turn_quote="“Penyebabnya sifilis.”",
        turn_verdict="Perusahaan sudah mengukur radiasi di tubuh mereka. Diagnosis itu bukan kesalahan — itu tameng.",
        loop="Mereka menjilat kuas itu setiap hari, dan hukumnya berubah hanya setelah mereka mati.",
        cues=["1917", "ORANGE, NJ", "RADIUM", "JILAT KUAS", "HUKUM BERUBAH"],
        visual="Meja kerja dengan kuas kecil; dial jam bercahaya di kegelapan; rahang pada rontgen.",
        plate="dial",
        sumber="NEEDS-SOURCE — Radium Girls 1917–1930an; gugatan 1927 dan preseden hukum belum dikutip langsung.",
    ),
]


# ══════════════════════════════════════════════════════════════════════════
# PENULISAN ULANG 16 NOV 2026 — naskah pendek 35–45 detik (EP11–EP21)
#
# Kenapa ditulis ulang: data performa Shorts kanal berhenti di ~1.000 tayangan,
# stayed-to-watch 57,9%, dan durasi 59–73 detik. Episode 11–21 masih memakai
# pola lama (10 beat, 110–130 kata) sehingga tidak mungkin masuk 35–45 detik.
#
# Pemisahan ini disengaja: naskah ditimpa di sini, bukan di badan data aslinya,
# supaya fakta dan `sumber` tetap apa adanya dan mudah dibandingkan.
# ══════════════════════════════════════════════════════════════════════════

_SHORT_2026 = {
    "EP11": dict(
        durasi=38,
        hook="Teleskop itu menangkap sinyal selama 72 detik. Lalu tidak pernah lagi.",
        tanya="Coba lihat cetakan komputer ini: 6EQUJ5. Kamu bisa membacanya?",
        relate="Kita memindai langit setiap malam, berharap ada yang menjawab.",
        beats=[
            ("tanya", "Coba lihat cetakan komputer ini: 6EQUJ5. Kamu bisa membacanya?"),
            ("relate", "Kita memindai langit setiap malam, berharap ada yang menjawab."),
            ("setup", "Agustus 1977, Ohio. Teleskop Big Ear menyapu langit seperti biasa."),
            ("tension", "Sinyalnya datang di 1.420 megahertz. Frekuensi yang dipancarkan hidrogen."),
            ("tension", "Frekuensi paling masuk akal kalau ada yang mau mengirim pesan."),
            ("turn", "Empat puluh tahun teleskop lain mencari ke titik yang sama. Kosong."),
            ("consequence", "Lihat arahnya. Tidak menunjuk ke bintang mana pun."),
        ],
        loop="72 detik. Kamu pikir itu pesan, atau kebetulan?",
        cues=["72 DETIK", "1420 MHz", "0 BINTANG"],
        captions=["", "6EQUJ5.", "Kita memindai langit.", "Ohio, 1977.", "1.420 MHz.",
                  "Frekuensi hidrogen.", "Kosong.", "Tanpa bintang.", "Pesan atau kebetulan?"],
        caption_hi=["", "6EQUJ5", "langit", "1977", "1420", "hidrogen", "kosong", "bintang", "kebetulan"],
        stamps=[["72", 0]],
        sfx={"00_hook": "tick", "01_tanya": "page", "02_relate": "gust", "03_setup": "gust",
             "04_tension": "boom", "05_tension": "tick", "06_turn": "boom", "07_consequence": "gust",
             "99_loop": "boom"},
    ),
    "EP12": dict(
        durasi=40,
        hook="Ratusan orang menari di jalan sampai tidak bisa berdiri. Tanpa musik.",
        tanya="Coba bayangkan kota yang menyuruh warganya menari. Kamu akan ikut?",
        relate="Kita menari untuk lupa. Mereka menari sampai lupa cara berhenti.",
        beats=[
            ("tanya", "Coba bayangkan kota yang menyuruh warganya menari. Kamu akan ikut?"),
            ("relate", "Kita menari untuk lupa. Mereka menari sampai lupa cara berhenti."),
            ("setup", "Juli 1518, Strasbourg. Seorang perempuan mulai menari di jalan."),
            ("tension", "Berhari-hari. Tanpa musik, tanpa tidur."),
            ("tension", "Lihat: dalam sebulan, ratusan orang ikut. Kota tidak menghentikannya."),
            ("turn", "Dokter justru menyarankan panggung dan musisi. Obatnya jadi bensinnya."),
            ("consequence", "Beberapa meninggal kelelahan. Tarian berhenti saat paniknya berhenti."),
        ],
        loop="Mereka berhenti menari. Kamu tahu apa yang memulainya?",
        cues=["1518", "TANPA MUSIK", "PANGGUNG & MUSISI"],
        captions=["", "Tanpa musik.", "Kita menari untuk lupa.", "Strasbourg, 1518.", "Berhari-hari.",
                  "Ratusan ikut.", "Panggung dan musisi.", "Kelelahan.", "Apa yang memulainya?"],
        caption_hi=["", "musik", "lupa", "1518", "berhari-hari", "ratusan", "panggung", "kelelahan", "memulainya"],
        stamps=[["1518", 3]],
        sfx={"00_hook": "tick", "01_tanya": "page", "02_relate": "page", "03_setup": "crowd",
             "04_tension": "tick", "05_tension": "crowd", "06_turn": "boom", "07_consequence": "boom",
             "99_loop": "boom"},
    ),
    "EP13": dict(
        durasi=41,
        hook="Dua pria memakai masker timah di wajah. Di saku: catatan berisi perintah.",
        tanya="Coba baca catatan itu. Kenapa kamu akan menunggu orang yang belum pernah kamu lihat?",
        relate="Kita menunggu jemputan yang tidak datang, lalu pulang sendiri. Mereka tidak pulang.",
        beats=[
            ("tanya", "Coba baca catatan itu. Kenapa kamu akan menunggu orang yang belum pernah kamu lihat?"),
            ("relate", "Kita menunggu jemputan yang tidak datang, lalu pulang sendiri. Mereka tidak pulang."),
            ("setup", "Agustus 1966, bukit di Rio de Janeiro. Dua pria, setelan resmi."),
            ("tension", "Tidak ada luka. Uang di catatan itu tidak pernah ditemukan."),
            ("tension", "Catatan itu memuat jam, tempat, dan perintah menelan kapsul."),
            ("turn", "Mereka datang tepat waktu. Orang yang menulis jadwal itu tidak datang."),
            ("consequence", "Enam puluh tahun disebut bunuh diri. Tapi surat perpisahan tidak punya jam."),
        ],
        loop="Masker timah itu masih di bukit. Menurut kamu, siapa yang mereka tunggu?",
        cues=["1966", "MASKER TIMAH", "CATATAN"],
        captions=["", "Catatan di saku.", "Kita menunggu jemputan.", "Rio, 1966.", "Tanpa luka.",
                  "Jam dan tempat.", "Tepat waktu.", "Bukan perpisahan.", "Siapa yang ditunggu?"],
        caption_hi=["", "catatan", "menunggu", "1966", "luka", "jam", "tepat waktu", "perpisahan", "ditunggu"],
        stamps=[["1966", 3]],
        sfx={"00_hook": "page", "01_tanya": "page", "02_relate": "gust", "03_setup": "gust",
             "04_tension": "tick", "05_tension": "page", "06_turn": "boom", "07_consequence": "boom",
             "99_loop": "boom"},
    ),
    "EP14": dict(
        durasi=40,
        hook="Dua siaran dibajak dalam satu malam. Tidak ada yang tertangkap.",
        tanya="Coba bayangkan wajah orang di balik topeng itu. Kamu akan mencari siapa?",
        relate="Kita pernah kehilangan sinyal sebentar, lalu kesal. Kota ini kehilangan dua siaran.",
        beats=[
            ("tanya", "Coba bayangkan wajah orang di balik topeng itu. Kamu akan mencari siapa?"),
            ("relate", "Kita pernah kehilangan sinyal sebentar, lalu kesal. Kota ini kehilangan dua siaran."),
            ("setup", "November 1987, Chicago. Film di saluran WGN tiba-tiba hilang."),
            ("tension", "Yang muncul: orang bertopeng kepala, suaranya dirusak."),
            ("tension", "Sembilan puluh detik. Lalu dua jam kemudian, saluran kedua."),
            ("turn", "Membajak sinyal analog butuh tahu di titik mana kabelnya bisa dipotong."),
            ("consequence", "Itu bukan lelucon. Itu pengetahuan teknis, dan orangnya tidak pernah ada."),
        ],
        loop="Dua siaran dibajak, nol tersangka. Kamu akan mulai dari mana?",
        cues=["1987", "90 DETIK", "2 SALURAN"],
        captions=["", "Dua saluran.", "Sinyal hilang.", "Chicago, 1987.", "Topeng kepala.",
                  "90 detik.", "Titik potong.", "Nol tersangka.", "Mulai dari mana?"],
        caption_hi=["", "saluran", "sinyal", "1987", "topeng", "90 detik", "kabel", "tersangka", "mana"],
        stamps=[["1987", 3], ["2", 1]],
        sfx={"00_hook": "tick", "01_tanya": "page", "02_relate": "gust", "03_setup": "clunk",
             "04_tension": "boom", "05_tension": "tick", "06_turn": "clunk", "07_consequence": "boom",
             "99_loop": "boom"},
    ),
    "EP15": dict(
        durasi=42,
        hook="Tingginya satu meter, otaknya sepertiga otak kita, dan dia hidup.",
        tanya="Coba lihat tengkorak itu. Kalau bukan kita, lalu siapa yang hidup di gua Flores?",
        relate="Kita selalu yakin hanya ada satu jenis manusia. Gua itu membantahnya.",
        beats=[
            ("tanya", "Coba lihat tengkorak itu. Kalau bukan kita, lalu siapa yang hidup di gua Flores?"),
            ("relate", "Kita selalu yakin hanya ada satu jenis manusia. Gua itu membantahnya."),
            ("setup", "2003, Gua Liang Bua, Flores. Tim menggali mencari jejak migrasi."),
            ("tension", "Yang keluar: kerangka satu meter, otak sepertiga otak kita."),
            ("tension", "Di sekitarnya ada alat batu, dan bukti perburuan."),
            ("turn", "Sebagian ilmuwan bersikeras: ini manusia modern yang sakit."),
            ("consequence", "Gigi dan rahangnya bilang lain. Ini bukan kita."),
        ],
        loop="Satu meter, enam puluh ribu tahun. Menurut kamu, siapa yang menghabiskan mereka?",
        cues=["1 METER", "60.000 TAHUN", "BUKAN KITA"],
        captions=["", "Satu meter.", "Hanya satu jenis?", "Flores, 2003.", "Otak sepertiga.",
                  "Alat batu.", "Manusia sakit?", "Bukan kita.", "Siapa yang menghabiskan?"],
        caption_hi=["", "satu meter", "jenis", "2003", "otak", "alat batu", "sakit", "bukan kita", "menghabiskan"],
        stamps=[["60.000", 0]],
        sfx={"00_hook": "boom", "01_tanya": "page", "02_relate": "gust", "03_setup": "water",
             "04_tension": "boom", "05_tension": "tick", "06_turn": "page", "07_consequence": "boom",
             "99_loop": "boom"},
    ),
    "EP16": dict(
        durasi=39,
        hook="Ratusan orang tertawa selama berbulan-bulan. Tidak ada virus yang ditemukan.",
        tanya="Coba bayangkan sekolah yang tidak bisa berhenti tertawa. Kamu akan pulang?",
        relate="Kita tertawa kalau lelah. Di sekolah itu, tertawa jadi satu-satunya cara bicara.",
        beats=[
            ("tanya", "Coba bayangkan sekolah yang tidak bisa berhenti tertawa. Kamu akan pulang?"),
            ("relate", "Kita tertawa kalau lelah. Di sekolah itu, tertawa jadi satu-satunya cara bicara."),
            ("setup", "Januari 1962, desa Kashasha, Tanganyika. Tiga murid mulai tertawa."),
            ("tension", "Tawanya tidak berhenti di jam pelajaran. Puluhan ikut, beberapa menangis."),
            ("tension", "Dua bulan kemudian sekolah ditutup. Wabahnya pindah ke sekolah lain."),
            ("turn", "Tidak ada virus, tidak ada racun. Yang ada aturan baru, dan anak yang tidak ditanya."),
            ("consequence", "Yang menular bukan penyakit. Yang menular tekanan."),
        ],
        loop="Tawanya berhenti setelah delapan belas bulan. Tekanannya, menurut kamu, berhenti?",
        cues=["1962", "TANPA VIRUS", "18 BULAN"],
        captions=["", "Ratusan orang.", "Tertawa kalau lelah.", "Kashasha, 1962.", "Puluhan ikut.",
                  "Sekolah ditutup.", "Bukan virus.", "Yang menular tekanan.", "Berhenti?"],
        caption_hi=["", "seribu", "tertawa", "1962", "puluhan", "ditutup", "virus", "tekanan", "berhenti"],
        stamps=[["1962", 3]],
        sfx={"00_hook": "crowd", "01_tanya": "page", "02_relate": "page", "03_setup": "crowd",
             "04_tension": "tick", "05_tension": "crowd", "06_turn": "boom", "07_consequence": "boom",
             "99_loop": "boom"},
    ),
    "EP17": dict(
        durasi=41,
        hook="Suara itu terdengar 4.800 kilometer jauhnya. Barometer di Eropa ikut bergerak.",
        tanya="Coba bayangkan suara yang bisa memutari bumi. Kamu mau berdiri di mana?",
        relate="Kita kenal guntur yang membuat kaca bergetar. Ini bukan guntur.",
        beats=[
            ("tanya", "Coba bayangkan suara yang bisa memutari bumi. Kamu mau berdiri di mana?"),
            ("relate", "Kita kenal guntur yang membuat kaca bergetar. Ini bukan guntur."),
            ("setup", "Krakatau, Selat Sunda. Sejak Mei 1883, asapnya tidak berhenti."),
            ("tension", "27 Agustus, empat ledakan dalam beberapa jam."),
            ("tension", "Barometer di seluruh dunia ikut bergerak."),
            ("turn", "Yang mengejutkan bukan ledakannya. Gelombang itu berputar mengelilingi bumi."),
            ("consequence", "Setelah itu, matahari terbenam di Eropa merah menyala."),
        ],
        loop="Suara itu berhenti, langitnya tidak. Menurut kamu, apa yang naik ke sana?",
        cues=["1883", "4.800 KM", "BAROMETER"],
        captions=["", "4.800 kilometer.", "Bukan guntur.", "Selat Sunda, 1883.", "Empat ledakan.",
                  "Barometer dunia.", "Memutari bumi.", "Langit merah.", "Apa yang naik?"],
        caption_hi=["", "4800 km", "guntur", "1883", "ledakan", "barometer", "memutari bumi", "merah", "naik"],
        stamps=[["1883", 3], ["4.800", 1]],
        sfx={"00_hook": "boom", "01_tanya": "page", "02_relate": "gust", "03_setup": "gust",
             "04_tension": "boom", "05_tension": "tick", "06_turn": "boom", "07_consequence": "gust",
             "99_loop": "boom"},
    ),
    "EP18": dict(
        durasi=42,
        hook="Gunung Tambora meledak. Setahun kemudian, salju turun di bulan Juni.",
        tanya="Coba lihat kalender 1816. Kenapa musim panas hilang dari Eropa?",
        relate="Kita mengira cuaca di sini ditentukan langit di sini. Ternyata tidak.",
        beats=[
            ("tanya", "Coba lihat kalender 1816. Kenapa musim panas hilang dari Eropa?"),
            ("relate", "Kita mengira cuaca di sini ditentukan langit di sini. Ternyata tidak."),
            ("setup", "April 1815, Gunung Tambora, Sumbawa. Letusan terbesar yang pernah dilihat orang."),
            ("tension", "Abu dan sulfur naik ke stratosfer, lalu memantulkan sinar matahari."),
            ("tension", "Selama setahun, bumi menerima lebih sedikit panas. Kamu bisa bayangkan dinginnya?"),
            ("turn", "Di Amerika, salju turun bulan Juni. Tanaman gagal."),
            ("consequence", "Di Eropa harga roti meledak, dan kota-kota mulai rusuh."),
        ],
        loop="Satu gunung di Sumbawa mengubah harga roti di London. Kamu lihat hubungannya?",
        cues=["1815", "TANPA MUSIM PANAS", "HARGA ROTI"],
        captions=["", "Salju di bulan Juni.", "Langit di sini.", "Tambora, 1815.", "Sulfur ke stratosfer.",
                  "Lebih sedikit panas.", "Panen gagal.", "Harga roti.", "Hubungannya?"],
        caption_hi=["", "juni", "langit", "1815", "stratosfer", "panas", "gagal", "roti", "hubungannya"],
        stamps=[["1815", 3], ["1816", 4]],
        sfx={"00_hook": "boom", "01_tanya": "page", "02_relate": "gust", "03_setup": "boom",
             "04_tension": "gust", "05_tension": "tick", "06_turn": "gust", "07_consequence": "crowd",
             "99_loop": "boom"},
    ),
    "EP19": dict(
        durasi=39,
        hook="Dua ribu kilometer persegi hutan rebah, semuanya menjauhi satu titik.",
        tanya="Coba lihat titik kosong itu. Kalau ada ledakan sebesar itu, di mana batunya?",
        relate="Kita mengharapkan ledakan meninggalkan lubang. Yang ini tidak meninggalkan apa pun.",
        beats=[
            ("tanya", "Coba lihat titik kosong itu. Kalau ada ledakan sebesar itu, di mana batunya?"),
            ("relate", "Kita mengharapkan ledakan meninggalkan lubang. Yang ini tidak meninggalkan apa pun."),
            ("setup", "Juni 1908, Siberia tengah. Langit terbelah, lalu angin panas."),
            ("tension", "Delapan ratus kilometer jauhnya, orang mendengar ledakannya. Kamu juga akan dengar."),
            ("tension", "Hutan rebah menjauhi satu titik pusat. Dua ribu kilometer persegi."),
            ("turn", "Ekspedisi pertama datang sembilan belas tahun kemudian. Mencari kawah."),
            ("consequence", "Tidak ada kawah. Benda itu meledak di udara, dan tidak meninggalkan batu."),
        ],
        loop="Hutan itu rebah ke arah luar. Menurut kamu, apa yang meledak di atas sana?",
        cues=["1908", "2.000 KM²", "TANPA KAWAH"],
        captions=["", "Menjauhi satu titik.", "Lubang?", "Siberia, 1908.", "800 kilometer.",
                  "Dua ribu km persegi.", "Mencari kawah.", "Tidak ada kawah.", "Apa yang meledak?"],
        caption_hi=["", "titik", "lubang", "1908", "800 km", "2000 km2", "kawah", "tanpa kawah", "meledak"],
        stamps=[["1908", 3]],
        sfx={"00_hook": "boom", "01_tanya": "page", "02_relate": "gust", "03_setup": "boom",
             "04_tension": "boom", "05_tension": "gust", "06_turn": "page", "07_consequence": "boom",
             "99_loop": "boom"},
    ),
    "EP20": dict(
        durasi=41,
        hook="Tidak ada letusan, tidak ada lava. Pagi berikutnya, 1.700 orang tidak bangun.",
        tanya="Coba bayangkan udara yang turun ke lembah. Kamu akan lari ke mana?",
        relate="Kita takut pada api yang terlihat. Yang ini tidak berwarna dan tidak berbau.",
        beats=[
            ("tanya", "Coba bayangkan udara yang turun ke lembah. Kamu akan lari ke mana?"),
            ("relate", "Kita takut pada api yang terlihat. Yang ini tidak berwarna dan tidak berbau."),
            ("setup", "Agustus 1986, Danau Nyos, Kamerun. Malam itu danau mengeluarkan awan gas."),
            ("tension", "Gas itu lebih berat dari udara, jadi turun ke lembah tempat orang tidur."),
            ("tension", "Pagi berikutnya, 1.700 orang dan ribuan ternak tidak bangun."),
            ("turn", "Semua orang pertama mengira gunung meletus. Tidak ada letusan."),
            ("consequence", "Gas itu tersimpan di dasar danau bertahun-tahun, di bawah tekanan."),
        ],
        loop="1.700 orang tidak bangun. Menurut kamu, apa yang menahannya sekarang?",
        cues=["1986", "TANPA LETUSAN", "CO₂"],
        captions=["", "Tanpa lava.", "Api yang terlihat.", "Nyos, 1986.", "Lebih berat dari udara.",
                  "1.700 orang.", "Bukan letusan.", "Gas di dasar danau.", "Apa yang menahannya?"],
        caption_hi=["", "lava", "terlihat", "1986", "udara", "1700 orang", "letusan", "gas", "menahannya"],
        stamps=[["1986", 3], ["1.700", 5]],
        sfx={"00_hook": "boom", "01_tanya": "page", "02_relate": "gust", "03_setup": "water",
             "04_tension": "water", "05_tension": "boom", "06_turn": "page", "07_consequence": "boom",
             "99_loop": "boom"},
    ),
    "EP21": dict(
        durasi=40,
        entitas="kuas",
        hook="Mereka diajari menjilat kuas berisi radium. Setiap kali selesai satu angka.",
        tanya="Coba bayangkan tangan yang melukis angka menyala. Kamu akan menjilat kuasnya?",
        relate="Kita percaya pada label di dinding pabrik. Mereka juga.",
        beats=[
            ("tanya", "Coba bayangkan tangan yang melukis angka menyala. Kamu akan menjilat kuasnya?"),
            ("relate", "Kita percaya pada label di dinding pabrik. Mereka juga."),
            ("setup", "1917, pabrik jam di Orange, New Jersey. Perempuan muda melukis angka dial."),
            ("tension", "Catnya radium. Supaya ujung kuas runcing, mereka diajari menjilatnya."),
            ("tension", "Bertahun-tahun kemudian, gigi mereka lepas sendiri. Rahang membusuk."),
            ("turn", "Dokter perusahaan menyebut penyebabnya sifilis. Perusahaan sudah tahu."),
            ("consequence", "Mereka menggugat dan menang. Hukum berubah karena mereka."),
        ],
        loop="Mereka menjilat kuas itu tiap hari. Menurut kamu, siapa yang seharusnya diperiksa?",
        cues=["1917", "RADIUM", "GUGATAN"],
        captions=["", "Radium.", "Percaya pada label.", "Orange, 1917.", "Ujung kuas.",
                  "Gigi lepas.", "Sifilis?", "Mereka menang.", "Siapa yang diperiksa?"],
        caption_hi=["", "radium", "label", "1917", "kuas", "gigi", "sifilis", "menang", "diperiksa"],
        stamps=[["1917", 3]],
        sfx={"00_hook": "tick", "01_tanya": "page", "02_relate": "page", "03_setup": "clunk",
             "04_tension": "tick", "05_tension": "boom", "06_turn": "page", "07_consequence": "boom",
             "99_loop": "boom"},
    ),
}

for _e in EPISODES:
    if _e["ep"] in _SHORT_2026:
        _e.update(_SHORT_2026[_e["ep"]])


# ══════════════════════════════════════════════════════════════════════════
# PENGGANTIAN 6 NOV 2026 — EP09–EP11 jadi kasus INDONESIA
#
# Arahan pemilik: mulai EP09 isinya misteri / kejadian janggal di Indonesia,
# bukan lagi kasus luar negeri. Naskah lama (Somerton Man, kembar Gibbons,
# Wow! signal) dikeluarkan dari peta; datanya masih ada di badan file ini
# sebagai catatan sejarah, tetapi tidak lagi dipakai EPISODES.
#
# Fakta tiap episode ada di field `sumber` dengan status VERIFIED dan
# rujukan yang dibaca. Angka yang belum terbaca langsung ditandai.
# ══════════════════════════════════════════════════════════════════════════

_INDONESIA = {
    # ── EP09 · tas berisi batu di Danau Kenanga ────────────────────────────
    "EP09": dict(
        title="TAS DI PUNGGUNGNYA BERISI BATU, DAN DIA DITEMUKAN DI DANAU KAMPUS",
        struktur="klimaks-awal",
        thumb=["TAS BERISI", "BATU"], thumb_text="TAS BERISI BATU",
        durasi=41, plate="water",
        protagonis="Akseyna, mahasiswa biologi UI, 18 tahun, anak seorang perwira TNI.",
        mau="Pulang ke Yogyakarta, atau setidaknya tidak tenggelam di kampusnya sendiri.",
        hambatan="Tempat kejadian dan kamar kosnya sudah dimasuki orang sebelum disegel.",
        tanaman="Secarik surat di kamar kos yang meminta dia tidak dicari.",
        hook="Tas di punggungnya berisi batu konblok, dan dia ditemukan di danau kampus.",
        hook_alt="Orang yang mau bunuh diri tidak menggendong batu di punggung. Dia menggendongnya.",
        tanya="Kalau kamu mau hilang, kenapa kamu butuh batu?",
        entitas="tas",
        relate="Kita mengikat batu ke barang yang mau kita buang.",
        diskusi="Kalau itu bukan bunuh diri, siapa yang ingin dia hilang?",
        celah="Kenapa batu itu diikat ke punggung, bukan ke tangan atau kaki?",
        gambar_melekat="Ransel berisi batu konblok, dipakai di punggung.",
        beats=[
            ("tanya", "Kalau kamu mau hilang, kenapa kamu butuh batu?"),
            ("relate", "Kita mengikat batu ke barang yang mau kita buang."),
            ("setup", "Maret 2015, Danau Kenanga, Depok. Mahasiswa biologi, umur 18."),
            ("tension", "Di kamar kosnya ada surat: jangan cari aku."),
            ("tension", "Coba lihat. Memar di punggungnya, dan air di paru-parunya."),
            ("turn", "Pemeriksa tulisan bilang surat itu ditulis dua orang berbeda."),
            ("consequence", "Bapaknya datang tiap Maret, menuntut satu nama."),
        ],
        turn_quote="“Dia bunuh diri, dan menulis suratnya sendiri.”",
        turn_verdict="Dua tulisan tangan di surat itu. Statusnya berubah jadi dugaan pembunuhan, tanpa tersangka.",
        loop="Tas itu masih di danau yang sama. Menurut kamu, siapa yang menggendongnya?",
        cues=["DANAU KENANGA", "2015", "DUA TULISAN"],
        captions=["", "Butuh batu?", "Kita buang dengan batu.", "Depok, 2015.",
                  "Jangan cari aku.", "Air di paru-paru.", "Dua tulisan.", "Satu nama.",
                  "Siapa yang menggendongnya?"],
        caption_hi=["", "batu", "batu", "2015", "surat", "paru-paru", "tulisan", "nama", "siapa"],
        stamps=[["2015", 3]],
        sfx={"00_hook": "boom", "01_tanya": "page", "02_relate": "page", "03_setup": "gust",
             "04_tension": "page", "05_tension": "boom", "06_turn": "boom",
             "07_consequence": "clunk", "99_loop": "boom"},
        sumber=(
            "VERIFIED 2026-11-06 — Akseyna Ahad Dori (lahir 2 Juni 1996, Yogyakarta) mahasiswa "
            "Biologi FMIPA UI angkatan 2013; jasadnya ditemukan mengambang di Danau Kenanga, "
            "Kampus UI Depok, Kamis 26 Maret 2015 oleh petugas kebersihan, memakai pakaian lengkap "
            "dan ransel berisi batu konblok serta kerikil. Tanpa dokumen pengenal; identitas baru "
            "dipastikan 30 Maret 2015 setelah keluarga datang ke RS Polri Kramat Jati. Di kamar "
            "kosnya ditemukan pesan 'Will not return, please don't search, my apologies for "
            "everything'. Polres Metro Depok mula-mula menyimpulkan bunuh diri; setelah autopsi, "
            "status berubah menjadi dugaan pembunuhan karena: memar akibat benda tumpul pada wajah "
            "dan tubuh; pasir serta air di paru-paru (masih bernapas saat masuk air); analisis "
            "grafologi menyimpulkan tanda tangan/tulisan tidak cocok (kemungkinan dua penulis atau "
            "dipalsukan); posisi ransel di punggung dinilai tidak lazim untuk tenggelam sukarela; "
            "robekan pada bagian belakang sepatu. Puluhan saksi diperiksa; tidak ada tersangka; TKP "
            "dan kamar kos sempat dimasuki orang sebelum sterilisasi. Ayahnya, Mardoto, bersama "
            "Aliansi Mahasiswa UI menuntut pengungkapan setiap tahun. Belum dibaca langsung: berkas "
            "autopsi RS Polri, hasil grafologi, dan berkas penyidikan Polres Metro Depok — "
            "verifikasi sebelum tayang."
        ),
    ),

    # ── EP10 · dua kardus di trotoar Sudirman ──────────────────────────────
    "EP10": dict(
        title="DUA KARDUS DI TROTOAR SUDIRMAN, DAN SATU NAMA YANG TIDAK PERNAH ADA",
        struktur="klimaks-awal",
        thumb=["DUA KARDUS", "TANPA NAMA"], thumb_text="DUA KARDUS",
        durasi=42, plate="road",
        protagonis="Mun'im Idris, dokter forensik yang membedah jasad itu.",
        mau="Memberi jasad itu satu nama.",
        hambatan="Sidik jari, wajah, dan ratusan keluarga yang datang — tidak satu pun cocok.",
        tanaman="Sidik jari korban tidak dihilangkan oleh pelakunya.",
        hook="Dua kardus di trotoar Sudirman, 1981. Isinya mayat tanpa nama.",
        hook_alt="Pelakunya tidak menghapus sidik jari. Bertahun kemudian, itu pun tidak menolong siapa pun.",
        tanya="Kalau kamu membunuh orang, kenapa sidik jari di kardus itu dibiarkan?",
        entitas="kardus",
        relate="Kita semua punya nama di satu dokumen, dan dia tidak.",
        diskusi="Menurut kamu, siapa yang paling mungkin mengenalnya?",
        celah="Kenapa sidik jari yang utuh tidak menemukan satu nama pun?",
        gambar_melekat="Dua kardus di trotoar, dan satu nisan tanpa nama.",
        beats=[
            ("tanya", "Kalau kamu membunuh orang, kenapa sidik jari di kardus itu dibiarkan?"),
            ("relate", "Kita semua punya nama di satu dokumen, dan dia tidak."),
            ("setup", "Pagi 23 November 1981, dua satpam melihat dua kardus itu."),
            ("tension", "Coba lihat isinya. Kepala, tulang, dan tidak ada satu lembar identitas."),
            ("tension", "Ratusan orang datang mengaku kehilangan saudara. Tidak ada yang cocok."),
            ("turn", "Sidik jarinya masih utuh, dan tetap tidak ada orang yang cocok."),
            ("consequence", "Dia dikubur 27 November 1981 di Tegal Alur, tanpa nama di nisan."),
        ],
        turn_quote="“Dia pasti dicari keluarganya.”",
        turn_verdict="Tidak ada yang mencari. Jasad itu dikubur tanpa nama, dan berkasnya berhenti di situ.",
        loop="Kardus itu sudah tidak ada. Nama itu masih kosong. Kamu punya tebakan?",
        cues=["SETIABUDI", "1981", "TANPA NAMA"],
        captions=["", "Kenapa dibiarkan?", "Semua punya nama.", "Sudirman, 1981.",
                  "Tanpa identitas.", "Tak ada yang cocok.", "Sidik jari utuh.",
                  "Tegal Alur.", "Kamu punya tebakan?"],
        caption_hi=["", "sidik jari", "nama", "1981", "identitas", "keluarga", "sidik jari",
                    "Tegal Alur", "tebakan"],
        stamps=[["1981", 3]],
        sfx={"00_hook": "clunk", "01_tanya": "page", "02_relate": "page", "03_setup": "gust",
             "04_tension": "rustle", "05_tension": "page", "06_turn": "boom",
             "07_consequence": "clunk", "99_loop": "boom"},
        sumber=(
            "VERIFIED 2026-11-06 — Kasus 'Setiabudi 13'. Pagi 23 November 1981, dua satpam PT "
            "Garuda Mataram Motor menemukan dua kardus di trotoar Jalan Jenderal Sudirman, "
            "Setiabudi, Jakarta, seberang Gedung Arthaloka; keduanya berbau anyir dan dikerubungi "
            "lalat, dilaporkan ke polisi yang sedang mengatur lalu lintas, lalu tergeletak sampai "
            "ditemukan dua gelandangan. Kardus pertama berisi kepala dan tiga belas tulang yang "
            "dikerat dari daging; kardus kedua berisi 180 potongan daging termasuk paru-paru, hati, "
            "dan limpa. Anus, kandung kemih, dan pankreas tidak ditemukan. Autopsi ±2 jam oleh "
            "Mun'im Idris, yang menyebut jasad dipotong sistematis; perkiraan mutilasi 3–4 jam oleh "
            "lebih dari satu orang. Korban pria tanpa identitas, perkiraan usia 18–21 tahun, tinggi "
            "165 cm, dibunuh 1–2 hari sebelum ditemukan. Sidik jari, telapak tangan, telapak kaki, "
            "dan wajah tidak dihilangkan, tetapi hasil tes sidik jari tidak menemukan pasangan yang "
            "cocok. Ratusan orang datang mengaku kehilangan kerabat; tidak ada yang cocok. Jasad "
            "dikebumikan 27 November 1981 di TPU Tegal Alur, Kalideres, Jakarta Barat. Kasus tidak "
            "pernah terpecahkan. Catatan: detail mutilasi sengaja tidak diucapkan di VO — naskah "
            "hanya memakai 'kepala, tulang, tanpa identitas' agar tidak kena pembatasan iklan. "
            "Belum dibaca langsung: buku Mun'im Idris (2013) dan liputan Mata Najwa/Kumparan yang "
            "dikutip Wikipedia — verifikasi sebelum tayang."
        ),
    ),

    # ── EP11 · tanah Porong yang belum berhenti ────────────────────────────
    "EP11": dict(
        title="TANAH DI PORONG MENGELUARKAN LUMPUR SEJAK 2006, DAN BELUM BERHENTI",
        struktur="klimaks-awal",
        thumb=["LUMPUR", "TAK BERHENTI"], thumb_text="LUMPUR TAK BERHENTI",
        durasi=43, plate="plume",
        protagonis="Warga Porong yang rumahnya tenggelam pelan-pelan.",
        mau="Tinggal di tanah yang sama, sedekat mungkin dengan rumahnya.",
        hambatan="Lumpurnya keluar dari dalam tanah, dan tidak ada yang berhasil menutupnya.",
        tanaman="Titik semburan hanya 150 meter dari sumur gas.",
        hook="Tanah di Porong mengeluarkan lumpur, dan 20 tahun kemudian masih keluar.",
        hook_alt="Ada gunung baru di Sidoarjo. Bukan gunung api, dan tidak bisa ditutup.",
        tanya="Dari mana semua tanah itu datang, dan siapa yang kamu salahkan?",
        entitas="tanah",
        relate="Kita lihat tanah sebagai benda yang diam.",
        diskusi="Kalau kamu tinggal di Porong, kamu pindah atau bertahan?",
        celah="Kenapa titik semburan muncul 150 meter dari sumur, bukan di sumurnya?",
        gambar_melekat="Rumah yang hanya kelihatan atapnya di tengah lumpur.",
        beats=[
            ("tanya", "Dari mana semua tanah itu datang, dan siapa yang kamu salahkan?"),
            ("relate", "Kita lihat tanah sebagai benda yang diam."),
            ("setup", "Mei 2006, Porong, Sidoarjo. Awalnya cuma air keruh di sawah."),
            ("tension", "Coba bayangkan rumahmu tenggelam dari lantai, bukan dari atap."),
            ("tension", "Dua hari sebelumnya, tanah di Yogyakarta berguncang."),
            ("tension", "Sumur gas itu cuma 150 meter dari titik semburan."),
            ("turn", "Ahli geologi bilang getaran itu terlalu jauh. Yang paling dekat bukan sesar, tapi sumur gas."),
            ("consequence", "Dua puluh tahun kemudian, lumpur itu masih menutup jalan dan rumah."),
        ],
        turn_quote="“Ini bencana alam. Gempa yang menyebabkan.”",
        turn_verdict="Getarannya terlalu jauh. Yang paling dekat bukan patahan, tapi sumur bor.",
        loop="Tanah itu masih mengeluarkan lumpur. Kamu akan tinggal di sana?",
        cues=["PORONG", "2006", "SUMBER: SUMUR"],
        captions=["", "Dari mana?", "Tanah yang diam.", "Porong, 2006.",
                  "Tenggelam dari lantai.", "Gempa Yogya.", "150 meter.",
                  "Bukan sesar.", "Masih keluar.", "Kamu pindah?"],
        caption_hi=["", "lumpur", "tanah", "2006", "rumah", "gempa", "150", "sumur",
                    "masih", "pindah"],
        stamps=[["2006", 3]],
        sfx={"00_hook": "gust", "01_tanya": "page", "02_relate": "page", "03_setup": "gust",
             "04_tension": "boom", "05_tension": "gust", "06_tension": "clunk",
             "07_turn": "boom", "08_consequence": "gust", "99_loop": "boom"},
        sumber=(
            "VERIFIED 2026-11-06 — Semburan lumpur panas Porong, Sidoarjo, Jawa Timur, mulai 29 Mei "
            "2006; gunung lumpur terbesar di dunia dan masih aktif. Pusat semburan berjarak ±150 "
            "meter dari sumur eksplorasi gas Banjar Panji-1 milik Lapindo Brantas Inc. (operator "
            "blok Brantas), yang mulai dibor awal Maret 2006. Gempa Yogyakarta terjadi 27 Mei 2006, "
            "dua hari sebelumnya — pihak perusahaan memakai itu sebagai penjelasan alternatif; "
            "sebagian besar literatur menyimpulkan blow-out pengeboran. Kerugian harta benda "
            "diperkirakan Rp45 triliun; korban tewas tidak langsung ≥20 orang (angka resmi "
            "bervariasi). Semburan menenggelamkan permukiman dan memutus jalur tol "
            "Surabaya–Gempol, jalan raya Surabaya–Malang, serta jalur kereta lintas timur. Catatan: "
            "artikel Wikipedia Indonesia untuk topik ini bertanda 'tanpa rujukan', sehingga angka "
            "kerugian dan korban harus dicek ke dokumen BPLS/BPK sebelum tayang; naskah hanya "
            "memakai fakta yang juga muncul di sumber berita arus utama (tanggal, lokasi, jarak 150 "
            "meter, masih aktif). Belum dibaca langsung: laporan BPLS, putusan/berkas perkara, dan "
            "paper penyebab (Davies dkk. vs. Mazzini dkk.) — verifikasi sebelum tayang."
        ),
    ),
}

for _e in EPISODES:
    if _e["ep"] in _INDONESIA:
        _e.update(_INDONESIA[_e["ep"]])
