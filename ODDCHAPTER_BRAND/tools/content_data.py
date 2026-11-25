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
        photos=[
            "00_hook", "01_tanya", "02_relate", "03_setup",
            "04_tension", "05_tension", "06_turn", "07_consequence", "08_loop",
        ],
        title="TAS DI PUNGGUNGNYA BERISI BATU, DAN DIA DITEMUKAN DI DANAU KAMPUS",
        struktur="klimaks-awal",
        thumb=["TAS BERISI", "BATU"], thumb_text="TAS BERISI BATU",
        durasi=54, plate="water",
        protagonis="Akseyna, mahasiswa biologi UI, 18 tahun, anak seorang perwira TNI.",
        mau="Pulang ke Yogyakarta, atau setidaknya tidak tenggelam di kampusnya sendiri.",
        hambatan="Tempat kejadian dan kamar kosnya sudah dimasuki orang sebelum disegel.",
        tanaman="Secarik surat di kamar kos yang meminta dia tidak dicari.",
        # NARASI = VO BUATAN USER (Drive: 1dD1nKT97JadquxCIf2WiAhnBoXGOtq7U ·
        # VO-EP09.mp3, 52,85 dtk). Teks di bawah ini disalin dari berkas SRT user
        # (EP09.srt, 16 baris); build_timing memakai cue-nya, bukan hitungan kata.
        vo=dict(
            file="vo.mp3",
            srt="vo.srt",
            source="Drive 1dD1nKT97JadquxCIf2WiAhnBoXGOtq7U · VO-EP09.mp3",
            sha256="3a31927d0752f68a23ba7f6bfaed9114e43e74584b5fa08935f626697ddc7135",
            # (part, teks, mulai, selesai) — detik pada berkas user. Batas antar
            # segmen disnap ke jeda hening nyata di berkas itu.
            cues=[
                (None, "Tas di punggungnya berisi batu konblok, dan dia ditemukan di danau kampus.", 0.0, 4.842),
                ("tanya", "Tapi coba pikirkan satu hal. Kalau kamu memang ingin menghilang, kenapa kamu membutuhkan batu?", 4.842, 10.485),
                ("relate", "Kita biasanya mengikat batu pada sesuatu yang ingin kita buang, supaya benda itu tenggelam dan tidak muncul kembali.", 10.485, 17.03),
                ("setup", "Maret 2015, Danau Kenanga, Depok. Seorang mahasiswa biologi berusia 18 tahun ditemukan di sana.", 17.03, 24.502),
                ("tension", "Di kamar kosnya ditemukan sebuah surat. Isinya: \u201cJangan cari aku.\u201d", 24.502, 29.325),
                ("tension", "Tapi ada detail lain yang tidak bisa diabaikan. Memar di punggungnya, dan air di dalam paru-parunya.", 29.325, 35.227),
                ("turn", "Lebih jauh lagi, pemeriksa tulisan tangan menyebutkan bahwa surat tersebut ditulis oleh dua orang yang berbeda.", 35.227, 41.401),
                ("consequence", "Ayahnya datang setiap bulan Maret, dan dia terus menuntut satu nama. Tas itu masih berada di danau yang sama.", 41.401, 48.742),
                (None, "Sekarang pertanyaannya, menurut kamu siapa sebenarnya yang menggendongnya?", 48.742, 52.851),
            ],
        ),
        hook="Tas di punggungnya berisi batu konblok, dan dia ditemukan di danau kampus.",
        hook_alt="Orang yang mau bunuh diri tidak menggendong batu di punggung. Dia menggendongnya.",
        tanya="Kalau kamu memang ingin menghilang, kenapa kamu membutuhkan batu?",
        entitas="tas",
        relate="Kita biasanya mengikat batu pada sesuatu yang ingin kita buang, supaya benda itu tenggelam dan tidak muncul kembali.",
        diskusi="Kalau itu bukan bunuh diri, siapa yang ingin dia hilang?",
        celah="Kenapa batu itu diikat ke punggung, bukan ke tangan atau kaki?",
        gambar_melekat="Ransel berisi batu konblok, dipakai di punggung.",
        beats=[
            ("tanya", "Tapi coba pikirkan satu hal. Kalau kamu memang ingin menghilang, kenapa kamu membutuhkan batu?"),
            ("relate", "Kita biasanya mengikat batu pada sesuatu yang ingin kita buang, supaya benda itu tenggelam dan tidak muncul kembali."),
            ("setup", "Maret 2015, Danau Kenanga, Depok. Seorang mahasiswa biologi berusia 18 tahun ditemukan di sana."),
            ("tension", "Di kamar kosnya ditemukan sebuah surat. Isinya: \u201cJangan cari aku.\u201d"),
            ("tension", "Tapi ada detail lain yang tidak bisa diabaikan. Memar di punggungnya, dan air di dalam paru-parunya."),
            ("turn", "Lebih jauh lagi, pemeriksa tulisan tangan menyebutkan bahwa surat tersebut ditulis oleh dua orang yang berbeda."),
            ("consequence", "Ayahnya datang setiap bulan Maret, dan dia terus menuntut satu nama."),
        ],
        turn_quote="“Dia bunuh diri, dan menulis suratnya sendiri.”",
        turn_verdict="Dua tulisan tangan di surat itu. Statusnya berubah jadi dugaan pembunuhan, tanpa tersangka.",
        loop="Sekarang pertanyaannya, menurut kamu siapa sebenarnya yang menggendongnya?",
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
        photos=[
            "00_hook", "01_setup", "02_tension", "03_tension", "04_relate",
            "05_tension", "06_turn", "07_consequence", "08_loop",
        ],
        # NARASI = VO BUATAN USER (Drive: 1x15AvOEZSd4LhXOd6eId2x8-DxIUfrT6 ·
        # VO EP10.mp3, 59,01 dtk). Teks dari TIMESTAMP EP10.txt (7 blok),
        # dipecah jadi 9 segmen; batas disnap ke jeda hening nyata.
        vo=dict(
            file="vo.mp3",
            timestamp="vo_timestamp.txt",
            source="Drive 1x15AvOEZSd4LhXOd6eId2x8-DxIUfrT6 · VO EP10.mp3",
            sha256="486667240b114ac041916af73fdc4ff3fb2d199cb2d1953054161526f76b2cab",
            cues=[
                (None, "Dua kardus di Trotoar Sudirman 1981.", 0.0, 4.495),
                ("setup", "Isinya potongan tubuh manusia tanpa nama. Dua satpam melihatnya pagi itu.", 5.105, 9.908),
                ("tension", "Tapi mereka tidak berani membuka kardus tersebut.", 10.490, 15.597),
                ("tension", "Ketika dua pemulung akhirnya membukanya, mereka menemukan kepala dan potongan tubuh manusia. Namanya tidak diketahui.", 15.947, 20.998),
                ("relate", "Identitasnya tidak ditemukan. Ratusan orang datang mencari anggota keluarga yang hilang. Tapi tak satu pun cocok.", 21.473, 28.283),
                ("tension", "Anehnya sidik jari korban masih bisa diperiksa. Wajahnya juga masih ada. Tapi identitasnya tetap tidak terungkap.", 28.695, 35.856),
                ("turn", "Pada 27 November 1981, jasad itu dimakamkan di TPU Tegal Alur. Kasus ini dikenal sebagai Setia Budi 13. Empat puluh tahun lebih berlalu.", 36.238, 45.996),
                ("consequence", "Pelakunya belum diketahui. Identitas korbannya pun masih menjadi misteri. Kita masih mengingat kasusnya.", 47.348, 55.486),
                (None, "Tapi siapa yang mengingat namanya?", 56.292, 59.011),
            ],
        ),
        title="DUA KARDUS DI TROTOAR SUDIRMAN, DAN SATU NAMA YANG TIDAK PERNAH ADA",
        struktur="klimaks-awal",
        thumb=["DUA KARDUS", "TANPA NAMA"], thumb_text="DUA KARDUS",
        durasi=59, plate="road",
        protagonis="Mun'im Idris, dokter forensik yang membedah jasad itu.",
        mau="Memberi jasad itu satu nama.",
        hambatan="Sidik jari, wajah, dan ratusan keluarga yang datang \u2014 tidak satu pun cocok.",
        tanaman="Sidik jari korban tidak dihilangkan oleh pelakunya.",
        hook="Dua kardus di Trotoar Sudirman 1981.",
        hook_alt="Pelakunya tidak menghapus sidik jari. Bertahun kemudian, itu pun tidak menolong siapa pun.",
        tanya="Kenapa sidik jari yang masih utuh tidak menemukan satu nama pun?",
        entitas="kardus",
        relate="Identitasnya tidak ditemukan. Ratusan orang datang mencari anggota keluarga yang hilang.",
        diskusi="Menurut kamu, siapa yang paling mungkin mengenalnya?",
        celah="Kenapa sidik jari yang utuh tidak menemukan satu nama pun?",
        gambar_melekat="Dua kardus di trotoar, dan satu nisan tanpa nama.",
        beats=[
            ("setup", "Isinya potongan tubuh manusia tanpa nama. Dua satpam melihatnya pagi itu."),
            ("tension", "Tapi mereka tidak berani membuka kardus tersebut."),
            ("tension", "Ketika dua pemulung akhirnya membukanya, mereka menemukan kepala dan potongan tubuh manusia. Namanya tidak diketahui."),
            ("relate", "Identitasnya tidak ditemukan. Ratusan orang datang mencari anggota keluarga yang hilang. Tapi tak satu pun cocok."),
            ("tension", "Anehnya sidik jari korban masih bisa diperiksa. Wajahnya juga masih ada. Tapi identitasnya tetap tidak terungkap."),
            ("turn", "Pada 27 November 1981, jasad itu dimakamkan di TPU Tegal Alur. Kasus ini dikenal sebagai Setia Budi 13. Empat puluh tahun lebih berlalu."),
            ("consequence", "Pelakunya belum diketahui. Identitas korbannya pun masih menjadi misteri. Kita masih mengingat kasusnya."),
        ],
        turn_quote="\u201cSetia Budi 13.\u201d",
        turn_verdict="Jasad dimakamkan tanpa nama di Tegal Alur. Pelaku dan identitas korban: dua-duanya kosong sampai sekarang.",
        loop="Tapi siapa yang mengingat namanya?",
        cues=["SETIABUDI 13", "TANPA NAMA", "SIDIK JARI"],
        captions=["", "Dua kardus.", "Satpam tak berani.", "Kepala, tanpa nama.",
                  "Ratusan datang. Nol cocok.", "Sidik jari utuh.", "Tegal Alur, 1981.",
                  "Empat puluh tahun.", "Siapa namanya?"],
        caption_hi=["", "kardus", "berani", "nama", "cocok", "sidik jari", "Tegal Alur",
                    "empat puluh", "nama"],
        stamps=[["1981", 6]],
        sfx={"00_hook": "clunk", "01_setup": "gust", "02_tension": "page", "03_tension": "rustle",
             "04_relate": "page", "05_tension": "boom", "06_turn": "boom",
             "07_consequence": "clunk", "99_loop": "boom"},
        sumber=(
            "VERIFIED 2026-11-06 \u2014 Kasus 'Setiabudi 13'. Pagi 23 November 1981, dua satpam PT "
            "Garuda Mataram Motor menemukan dua kardus di trotoar Jalan Jenderal Sudirman, "
            "Setiabudi, Jakarta, seberang Gedung Arthaloka; keduanya berbau anyir dan dikerubungi "
            "lalat, dilaporkan ke polisi yang sedang mengatur lalu lintas, lalu tergeletak sampai "
            "ditemukan dua gelandangan. Kardus pertama berisi kepala dan tiga belas tulang yang "
            "dikerat dari daging; kardus kedua berisi 180 potongan daging termasuk paru-paru, hati, "
            "dan limpa. Anus, kandung kemih, dan pankreas tidak ditemukan. Autopsi \u00b12 jam oleh "
            "Mun'im Idris, yang menyebut jasad dipotong sistematis; perkiraan mutilasi 3\u20134 jam oleh "
            "lebih dari satu orang. Korban pria tanpa identitas, perkiraan usia 18\u201321 tahun, tinggi "
            "165 cm, dibunuh 1\u20132 hari sebelum ditemukan. Sidik jari, telapak tangan, telapak kaki, "
            "dan wajah tidak dihilangkan, tetapi hasil tes sidik jari tidak menemukan pasangan yang "
            "cocok. Ratusan orang datang mengaku kehilangan kerabat; tidak ada yang cocok. Jasad "
            "dikebumikan 27 November 1981 di TPU Tegal Alur, Kalideres, Jakarta Barat. Kasus tidak "
            "pernah terpecahkan. Catatan: detail mutilasi sengaja tidak diucapkan di VO \u2014 naskah "
            "hanya memakai 'kepala, tulang, tanpa identitas' agar tidak kena pembatasan iklan. "
            "Belum dibaca langsung: buku Mun'im Idris (2013) dan liputan Mata Najwa/Kumparan yang "
            "dikutip Wikipedia \u2014 verifikasi sebelum tayang."
        ),
    ),

    # ── EP11 · tanah Porong yang belum berhenti ────────────────────────────
    "EP11": dict(
        title="ENAM MENIT TERAKHIR SEORANG PILOT, LALU SUARA LOGAM",
        struktur="klimaks-awal",
        thumb=["BUKAN", "PESAWAT"], thumb_text="BUKAN PESAWAT",
        durasi=43, plate="signal",
        photos=["01_hook", "02_tanya", "03_relate", "04_setup", "05_tension",
                "06_tension", "07_turn", "08_consequence", "09_loop"],
        protagonis="Frederick Valentich, pilot 20 tahun, Cessna 182 VH-DSJ.",
        mau="Sampai ke King Island dalam 69 menit.",
        hambatan="Ada benda di langit yang tidak bisa dia namai, dan tidak ada yang melihatnya.",
        tanaman="Rekaman radio enam menit; kalimat terakhirnya: itu bukan pesawat.",
        hook="Rekaman itu berhenti di 19.12 dan pilot itu tidak pernah menjawab lagi.",
        hook_alt="Pilot ini melapor ada pesawat besar di bawahnya. Rekamannya berhenti pukul 19.12.",
        tanya="Apa yang dia lihat sebelum rekaman berhenti di 19.12?",
        entitas="rekaman",
        relate="Kita cuma punya suara Valentich. Kamu tidak bisa melihat keluar jendela itu.",
        diskusi="Kamu percaya dia melihat pesawat lain, atau dia kehilangan arah?",
        celah="Apa yang ada di luar jendela itu, yang tidak ikut terekam?",
        gambar_melekat="Jarum jam radio di 19.12 dan mikrofon yang terbuka tujuh belas detik.",
        beats=[
            ("tanya", "Apa yang dia lihat sebelum rekaman berhenti di 19.12?"),
            ("relate", "Kita cuma punya suara Valentich. Kamu tidak bisa melihat keluar jendela itu."),
            ("setup", "21 Oktober 1978, pukul 19.06. Frederick Valentich terbang ke King Island."),
            ("tension", "Coba lihat 19.06: panggilan pertama, ada pesawat besar di bawahnya."),
            ("tension", "Perhatikan jamnya: 19.11, mesinnya mulai tersendat."),
            ("turn", "Laporan resmi 1978: penyebabnya tidak bisa ditentukan. Tapi rekaman berhenti dengan suara logam."),
            ("consequence", "4 hari dicari dari laut dan udara. Tidak ada bagian pesawatnya."),
        ],
        turn_quote="\u201cIt is hovering and it is not an aircraft.\u201d",
        turn_verdict=("Rekaman itu tidak membuktikan benda apa pun. Yang ia buktikan: satu-satunya "
                      "orang yang melihatnya kehilangan kemampuan membaca langit, dan laporan resmi "
                      "memilih tidak memilih di antara dua bacaan itu."),
        loop="Kalau kamu pilot itu: putar balik ke pantai, atau lanjut ke King Island?",
        cues=["21 OKT 1978", "19.06", "19.11", "SUARA 17 DETIK"],
        captions=["", "Apa yang dia lihat?", "Kita cuma punya suara.", "Moorabbin, 1978.",
                  "Empat lampu.", "19.11.", "Penyebab: tidak diketahui.", "4 hari, kosong.",
                  "Putar balik?"],
        caption_hi=["", "lihat", "suara", "1978", "lampu", "19.11", "tidak tentu", "kosong", "balik"],
        visual=("Gulungan pita rekaman; jam dinding 19.12; empat lampu di langit hitam; "
                "mikrofon terbuka; peta Bass Strait dengan garis Moorabbin-King Island."),
        stamps=[["19.11", 5], ["4 HARI", 7]],
        sfx={"00_hook": "gust", "01_tanya": "page", "02_relate": "page", "03_setup": "gust",
             "04_tension": "clunk", "05_tension": "tick", "06_turn": "boom",
             "07_consequence": "gust", "99_loop": "boom"},
        sumber=(
            "TERVERIFIKASI SEBAGIAN 2026-11-16 — Frederick Valentich, 20 tahun, Cessna 182L "
            "VH-DSJ (panggilan Delta Sierra Juliet), hilang 21 Oktober 1978 dalam penerbangan "
            "Moorabbin-King Island (125 mil, normalnya 69 menit). Transkrip Melbourne Flight "
            "Service (berkas Australian Department of Transport V116/783/1047): 19.06.14 panggilan "
            "pertama 'any known traffic below five thousand' dijawab 'no known traffic'; 19.06.44 "
            "'large aircraft below five thousand, four bright like landing lights'; 19.07.31 "
            "'passed over me at least a thousand feet above'; 19.08.48 'playing some sort of game, "
            "two three times at speeds I could not identify', level 4.500 kaki; 19.09.42 'long "
            "shape'; 19.10.19 diam, saling mengorbit, 'green light metallic shiny'; 19.10.46 "
            "'it's just vanished'; 19.11.50 mesin rough-idling, set 23/24, 'coughing'; niat ke King "
            "Island; kalimat terakhir 'it is hovering and it is not an aircraft'; 19.12.28 mikrofon "
            "terbuka 17 detik berisi suara logam, lalu diam. Alarm SAR 19.12, dia tidak tiba 19.33. "
            "Pencarian udara-laut 4 hari dengan P-3 Orion RAAF, berakhir 25 Oktober 1978, tanpa satu "
            "pun bagian pesawat; laporan resmi: penyebab tidak bisa ditentukan. Teori disorientasi "
            "(malam tanpa horizon, pesawat terbalik, lampunya sendiri terpantul) dan teori 'kabur ke "
            "pedalaman' sama-sama dibahas dan tidak terbukti. Sumber dibaca: transkrip yang dikutip "
            "ulang arsip V116/783/1047, AP 22 Oktober 1978, Haines 'Melbourne Episode' 1987. BELUM "
            "dibaca: pindaian penuh berkas ATSB, audio asli transkrip, koran Australia 1978 (Trove). "
            "Catatan riset: 11_CONTENT/02_SCRIPT/riset/EP11_valentich.md"
        ),
    ),
}

for _e in EPISODES:
    if _e["ep"] in _INDONESIA:
        _e.update(_INDONESIA[_e["ep"]])


# ══════════════════════════════════════════════════════════════════════════
# BATCH 2 · 6 NOV 2026 — EP12–EP14, sengaja di luar Jawa
#
# EP12 Kelimutu (NTT) · EP13 Trunyan (Bali) · EP14 Orang Pendek (Kerinci, Sumatera)
# Semua memakai aturan yang sama: satu tanaman, dibayar di turn, tanpa fakta baru.
# Klaim yang belum diuji (bau Trunyan, keberadaan orang pendek) ditulis sebagai
# klaim, bukan sebagai fakta — lihat field `sumber`.
# ══════════════════════════════════════════════════════════════════════════

_INDONESIA_BATCH2 = {
    # ── EP12 · kapal yang tidak bisa tenggelam ─────────────────────────────
    # Topik T01 dari gerbang topik (11_CONTENT/01_IDEA/topik_kandidat.json):
    # MV Joyita, 1955. Menggantikan Kelimutu (tier `umum`) yang ditahan.
    # Ladder: fokus L2 — setiap angka di VO punya label di layar.
    # Sumber dibaca 15 Nov 2026: Samoa Observer (17 Mei 2025), The Fiji Times,
    # RNZ/PMN News (10 Jun 2022), Explorersweb, Popular Mechanics.
    # Catatan riset: 11_CONTENT/02_SCRIPT/riset/EP12_mv-joyita.md
    "EP12": dict(
        title="KAPAL YANG TIDAK BISA TENGGELAM, DAN 25 ORANG YANG MENINGGALKANNYA",
        struktur="klimaks-awal",
        thumb=["KAPAL", "KOSONG"], thumb_text="KAPAL KOSONG",
        durasi=43, plate="vessel",
        protagonis="Kapten Thomas Miller dan 24 orang yang naik ke kapal yang tidak bisa tenggelam.",
        mau="Sampai ke Tokelau dengan satu mesin.",
        hambatan="Air masuk pelan-pelan dari pipa yang tidak dilihat siapa pun.",
        tanaman="Sekoci dan tiga rakit Carley hilang; kapalnya tetap terapung.",
        hook="Kapal itu tidak bisa tenggelam. Dua puluh lima orang meninggalkannya.",
        hook_alt="Dua puluh lima orang naik ke kapal yang tidak bisa tenggelam. Tidak ada yang tersisa.",
        tanya="Kenapa mereka pergi dari kapal yang terapung?",
        entitas="kapal",
        relate="Kita percaya kapal yang tidak bisa tenggelam. Kamu juga.",
        diskusi="Kalau kamu di kapal itu, kamu ikut turun ke sekoci?",
        celah="Kenapa mereka meninggalkan kapal yang tidak bisa tenggelam?",
        gambar_melekat="Sekoci kosong di sisi kapal yang masih terapung.",
        # Potongan klimaks dari 07_LONGFORM/LF02_joyita/SCRIPT.md (babak 1, 4, 5, 6, 7).
        # Kalimat di sini adalah kalimat yang sama dengan naskah panjang, dipendekkan —
        # bukan naskah baru. Ubah naskah panjang dulu, baru potong.
        beats=[
            ("tanya", "Kenapa mereka pergi dari kapal yang terapung?"),
            ("relate", "Kita percaya kapal yang tidak bisa tenggelam. Kamu juga."),
            ("setup", "3 Oktober 1955, Apia. Joyita berlayar dengan satu mesin."),
            ("tension", "Malam kedua, air masuk lewat pipa yang terkorosi."),
            ("tension", "Mereka menurunkan sekoci. Ditemukan lima minggu kemudian, 970 kilometer jauhnya."),
            ("tension", "Coba lihat jamnya: berhenti di 10.25. Kamu bisa bayangkan gelapnya?"),
            ("turn", "Penyelidikan bilang itu tidak bisa dijelaskan. Tapi mereka tidak salah membaca air; mereka salah membaca kapal."),
            ("consequence", "Enam dari dua puluh lima orang baru dinyatakan mati pada 2022."),
        ],
        turn_quote="“Nasib mereka tidak bisa dijelaskan dari bukti yang diajukan.”",
        turn_verdict=("Kebocoran itu nyata; yang keliru bukan pembacaan mereka atas air, melainkan "
                      "pembacaan atas kapal. Kapal yang tidak bisa tenggelam tidak membuat orang "
                      "di dalamnya aman."),
        loop="Kapal itu masih mengapung. Apakah itu berarti kamu selamat?",
        cues=["APIA 1955", "970 KM", "10.25", "PIPA BOCOR"],
        captions=["", "Kenapa pergi?", "Kita percaya kapal.", "Apia, 1955.", "Pipa bocor.",
                  "Sekoci turun.", "10.25.", "Salah baca kapal.", "6 dari 25.", "Kamu selamat?"],
        caption_hi=["", "pergi", "kapal", "1955", "pipa", "sekoci", "10.25", "kapal", "mati", "selamat"],
        visual=("Lambung miring 45 derajat dengan garis air yang basah; jam dinding kapal di 10.25; "
                "sekoci kosong di atas dek; peta jalur Apia–Tokelau dan titik penemuan di utara Fiji."),
        stamps=[["10.25", 6], ["970 KM", 5]],
        sfx={"00_hook": "gust", "01_tanya": "page", "02_relate": "page", "03_setup": "gust",
             "04_tension": "clunk", "05_tension": "gust", "06_tension": "tick",
             "07_turn": "boom", "08_consequence": "clunk", "99_loop": "boom"},
        sumber=(
            "TERVERIFIKASI SEBAGIAN 2026-11-15 — MV Joyita, kapal kayu 69 kaki, dibangun 1931 di "
            "Wilmington Boat Works, Los Angeles, untuk sutradara Roland West. Berlayar dari Apia, "
            "Samoa, 3 Oktober 1955 menuju Tokelau; 25 orang (16 awak, 9 penumpang, termasuk dua anak "
            "berusia 6 dan 11 tahun). Keberangkatan tertunda sehari karena kopling mesin kiri rusak; "
            "berlayar dengan satu mesin. Ditemukan 10 November 1955 oleh kapal Tuvalu (Kapten Gerald "
            "Douglas) di utara Vanua Levu, Fiji, miring ±45 derajat dan ±970 kilometer dari jalur; "
            "sekoci dan tiga rakit Carley hilang, logbook dan alat navigasi hilang, radio tersetel "
            "2182 kHz (kanal darurat) dengan kabel antena putus sehingga jangkauan ±2 mil, jam listrik "
            "berhenti di 10.25, lampu navigasi menyala, tas dokter berisi perban berdarah di geladak, "
            "mesin kanan tertutup kasur. Sidang di Apia Februari 1956: lambung sehat; air masuk lewat "
            "pipa pendingin yang terkorosi; pompa bilge tanpa saringan dan tersumbat; kapal tidak dalam "
            "bahaya tenggelam karena lapisan gabus dan 80 drum kosong; kesimpulan resmi menyebut nasib "
            "25 orang 'inexplicable on the evidence submitted at the inquiry', dan kapten dinilai lalai "
            "berlayar dengan satu mesin. Hanya 6 dari 25 orang dinyatakan meninggal (PMN News, 10 Juni "
            "2022). Sumber dibaca: Samoa Observer 17 Mei 2025, The Fiji Times, PMN News/RNZ 10 Juni "
            "2022, Explorersweb, Popular Mechanics. BELUM dibaca: transkrip sidang Apia 1956 dan koran "
            "Samoa 1955-56. Angka 970 km adalah pembulatan dari '600 mil' pada sumber; naskah memakai "
            "satu angka saja supaya tidak bertentangan."
        ),
    ),

    # ── EP13 · mayat yang tidak dikubur ─────────────────────────────────────
    "EP13": dict(
        title="DI DESA INI MAYAT TIDAK DIKUBUR, DAN TIDAK ADA YANG BISA MENJELASKAN BAUNYA",
        struktur="klimaks-awal",
        thumb=["TANPA KUBUR", "TANPA BAU"], thumb_text="TANPA KUBUR",
        durasi=43, plate="ridge",
        protagonis="Warga Bali Aga di Trunyan yang menjaga leluhurnya di atas tanah.",
        mau="Tetap dekat dengan yang sudah meninggal.",
        hambatan="Adat hanya mengizinkan cara ini, dan belum ada yang mengukur bau itu.",
        tanaman="Pohon Taru Menyan di tengah area pemakaman.",
        hook="Tubuh mereka tidak dikubur, dan di bawah pohon itu tidak tercium bau.",
        hook_alt="Di Trunyan tidak ada liang kubur dan tidak ada kremasi. Ada satu pohon, dan puluhan tengkorak.",
        tanya="Kalau mayat dibiarkan terbuka di bawah pohon, kenapa kamu tidak mencium apa pun?",
        entitas="tubuh",
        relate="Kita mengubur orang supaya tanah menutup bau dan hewan.",
        diskusi="Kalau keluargamu memilih cara ini, kamu setuju?",
        celah="Kenapa tidak ada bau, padahal tubuhnya dibiarkan terbuka?",
        gambar_melekat="Tengkorak tersusun di altar batu, di bawah satu pohon besar.",
        beats=[
            ("tanya", "Kalau mayat dibiarkan terbuka di bawah pohon, kenapa kamu tidak mencium apa pun?"),
            ("relate", "Kita mengubur orang supaya tanah menutup bau dan hewan."),
            ("setup", "Trunyan, Bali. Mayat ditaruh di bawah pohon Taru Menyan."),
            ("tension", "Coba lihat. Puluhan tengkorak tersusun di altar batu, tanpa liang."),
            ("tension", "Orang wajar, orang kecelakaan, orang belum menikah: tiga tempat."),
            ("tension", "Pohon Taru Menyan, kata warga, yang menyerap baunya."),
            ("turn", "Bau itu belum pernah diukur. Yang terukur: keluarganya masih datang."),
            ("consequence", "Mereka menaruh sesajen, dan menyapa yang sudah mati dengan nama."),
        ],
        turn_quote="“Mereka dibiarkan begitu saja.”",
        turn_verdict="Mereka tidak dibiarkan. Yang belum pernah diuji cuma baunya; yang jelas, mayat itu masih punya alamat.",
        loop="Pohon itu masih berdiri. Kamu akan menyebutnya kuburan atau rumah?",
        cues=["TRUNYAN", "MEPASAH", "TANPA LIANG"],
        captions=["", "Kenapa tidak bau?", "Kita menutup dengan tanah.", "Trunyan, Bali.",
                  "Tengkorak di batu.", "Tiga tempat.", "Pohon Taru Menyan.", "Belum diukur.",
                  "Kuburan atau rumah?"],
        caption_hi=["", "bau", "tanah", "Trunyan", "tengkorak", "tiga", "pohon", "diukur", "rumah"],
        stamps=[["TRUNYAN", 3]],
        sfx={"00_hook": "gust", "01_tanya": "page", "02_relate": "page", "03_setup": "rustle",
             "04_tension": "boom", "05_tension": "page", "06_tension": "rustle",
             "07_turn": "boom", "08_consequence": "page", "99_loop": "boom"},
        sumber=(
            "VERIFIED 2026-11-06 — Desa Trunyan, Kecamatan Kintamani, Kabupaten Bangli, Bali (masyarakat "
            "Bali Aga). Tradisi pemakaman disebut mepasah atau 'kubur angin': jenazah tidak dikubur dan "
            "tidak dikremasi, melainkan diletakkan di area pemakaman di bawah pohon Taru Menyan, sebagian "
            "ditutup anyaman bambu berbentuk kerucut untuk menghindari hewan; setelah membusuk, "
            "tulang dan tengkoraknya diletakkan di altar di bawah pohon. Ada tiga area terpisah: Seme "
            "Wajah (meninggal wajar), Seme Bantah (meninggal tidak wajar/kecelakaan), Seme Muda (bayi, "
            "anak, dan yang belum menikah). Klaim bahwa area itu tidak berbau dan penyebabnya pohon Taru "
            "Menyan adalah keyakinan warga dan laporan pengunjung — TIDAK ada penelitian yang mengukur "
            "konsentrasi gas/aroma di lokasi, sehingga di naskah klaim itu ditulis sebagai 'kata warga' "
            "dan turn menyatakan bahwa bau itu belum pernah diukur. Rujukan yang dibaca: National "
            "Geographic Indonesia (23 Oktober 2018) dan Majalah Outsiders (9 Mei 2026). Belum dibaca "
            "langsung: kajian antropologi Bali Aga dan data Balai Arkeologi Bali — verifikasi sebelum "
            "tayang."
        ),
    ),

    # ── EP14 · primata yang tidak pernah terpotret ──────────────────────────
    "EP14": dict(
        title="SERATUS TAHUN ORANG MELIHATNYA, DAN TIDAK ADA SATU FOTONYA",
        struktur="klimaks-awal",
        thumb=["TANPA FOTO", "SERATUS TAHUN"], thumb_text="TANPA FOTO",
        durasi=43, plate="signal",
        protagonis="Debbie Martyr, peneliti yang menghabiskan bertahun-tahun di Kerinci.",
        mau="Satu foto yang tidak bisa dibantah.",
        hambatan="Kamera yang menangkap harimau tidak pernah menangkapnya.",
        tanaman="Sampel rambut yang dikirim ke laboratorium.",
        hook="Orang pendek sudah muncul seratus tahun di cerita, dan belum ada foto.",
        hook_alt="Saksi melihatnya berkali-kali. Kameranya tidak sekali pun.",
        tanya="Kalau kamu pasang seratus kamera, apa yang akan kamu tunggu?",
        entitas="orang pendek",
        relate="Kita percaya pada foto, dan penasaran pada yang tidak pernah difoto.",
        diskusi="Kalau kamu yang menemukannya, kamu akan memotret atau lari?",
        celah="Kenapa saksi melihatnya, tapi kamera tidak pernah?",
        gambar_melekat="Cetakan kaki pendek dan lebar, tanpa hewan pembanding.",
        beats=[
            ("tanya", "Kalau kamu pasang seratus kamera, apa yang akan kamu tunggu?"),
            ("relate", "Kita percaya pada foto, dan penasaran pada yang tidak pernah difoto."),
            ("setup", "Kerinci, Sumatera. Tingginya 85 sentimeter, kata saksi."),
            ("tension", "Coba lihat cetakan kakinya. Pendek, lebar, tanpa hewan pembanding."),
            ("tension", "Sampel rambut dikirim ke laboratorium, dan hasilnya tidak pernah keluar."),
            ("turn", "Rambut itu bukan primata baru. Itu rambut manusia."),
            ("consequence", "Kamera masih dipasang, dan yang muncul tetap hewan yang kita kenal."),
        ],
        turn_quote="“Ada primata baru di hutan Sumatera.”",
        turn_verdict="Rambutnya manusia. Yang tersisa cuma cerita, dan cerita tidak bisa dipotret.",
        loop="Cerita itu masih ada, dan fotonya belum. Kamu percaya yang mana?",
        cues=["KERINCI", "85 CM", "TANPA FOTO"],
        captions=["", "Seratus kamera?", "Kita percaya yang difoto.", "Kerinci, 85 cm.",
                  "Cetakan kaki.", "Sampel rambut.", "Rambut manusia.", "Kamera tetap kosong.",
                  "Apa yang mereka lihat?"],
        caption_hi=["", "kamera", "difoto", "Kerinci", "kaki", "rambut", "manusia", "kosong", "lihat"],
        stamps=[["1990", 3]],
        sfx={"00_hook": "page", "01_tanya": "page", "02_relate": "page", "03_setup": "gust",
             "04_tension": "clunk", "05_tension": "rustle", "06_turn": "boom",
             "07_consequence": "page", "99_loop": "boom"},
        sumber=(
            "VERIFIED 2026-11-06 — Orang pendek (uhang pandak), makhluk mirip primata bipedal yang "
            "diklaim menghuni hutan Sumatera, terutama di Kabupaten Kerinci dan Taman Nasional Kerinci "
            "Seblat. Deskripsi saksi: tinggi 80–150 cm (Debbie Martyr: biasanya 85–90 cm, kadang sampai "
            "120 cm), berbulu pendek gelap, bahu lebar. Laporan tertulis sejak awal abad ke-20, antara "
            "lain catatan Mr. van Heerwarden (1923) semasa survei lahan; cerita serupa hidup di "
            "masyarakat Suku Anak Dalam (Bukit Duabelas) sebagai 'hantu pendek'. Penelitian paling "
            "serius: Debbie Martyr (1990-an, pernah didukung Fauna & Flora International) dan fotografer "
            "Jeremy Holden yang memasang camera trap di TNKS — banyak harimau dan beruang madu terekam, "
            "orang pendek tidak; keduanya mengaku pernah melihatnya sendiri. Cetakan kaki (cast) "
            "dikumpulkan, beberapa sampel rambut dianalisis dan hasil DNA-nya dilaporkan manusia "
            "(ekspedisi Adam Davies & Andrew Sanderson). Tidak ada spesimen, tulang, atau foto jelas. "
            "Rujukan: Kompas.com (4 Mei 2012), Skeptoid #77, Wikipedia ID. Ini klaim yang belum "
            "terbukti — naskah tidak menyatakan orang pendek ada; turn justru mematahkan bukti "
            "rambutnya. Belum dibaca langsung: laporan ekspedisi FFI dan hasil laboratorium asli — "
            "verifikasi sebelum tayang."
        ),
    ),
}

for _e in EPISODES:
    if _e["ep"] in _INDONESIA_BATCH2:
        _e.update(_INDONESIA_BATCH2[_e["ep"]])


# ══════════════════════════════════════════════════════════════════════════
# BATCH 3 · 6 NOV 2026 — EP15–EP17: Sulawesi, Kalimantan, Sumatera
#
# EP15 likuefaksi Palu · EP16 lukisan gua Sangkulirang · EP17 Sinabung.
# Semua memakai disiplin yang sama: satu tanaman, dibayar di turn, tanpa angka
# baru di turn (check_story akan menolak kalau dilanggar).
# ══════════════════════════════════════════════════════════════════════════

_INDONESIA_BATCH3 = {
    # ── EP15 · tanah yang berhenti jadi padat ──────────────────────────────
    "EP15": dict(
        title="TANAH DI PETOBO BERUBAH JADI LUMPUR, DAN RUMAHNYA IKUT BERGERAK",
        struktur="klimaks-awal",
        thumb=["TANAH", "MENGALIR"], thumb_text="TANAH MENGALIR",
        durasi=43, plate="ridge",
        protagonis="Warga Petobo yang rumahnya bergerak bersama tanah.",
        mau="Menyelamatkan diri dari tanah yang tidak lagi diam.",
        hambatan="Tanahnya bergerak lebih cepat dari orang yang berlari.",
        tanaman="Kata Kaili untuk peristiwa ini: nalodo, amblas.",
        hook="Tanah di Petobo berubah jadi lumpur, dan rumah-rumah ikut bergerak.",
        hook_alt="Rumah di Petobo tidak roboh. Rumah itu ikut berjalan bersama tanahnya.",
        tanya="Kalau tanah padat bisa mengalir, apa yang kamu pijak sekarang?",
        entitas="tanah",
        relate="Kita menaruh rumah di atas tanah karena percaya tanah diam.",
        diskusi="Kalau rumahmu berdiri di atas tanah itu, kamu pindah?",
        celah="Kenapa tanah yang padat bisa mengalir seperti air?",
        gambar_melekat="Rumah dan pohon bergeser puluhan meter dari tempatnya.",
        beats=[
            ("tanya", "Kalau tanah padat bisa mengalir, apa yang kamu pijak sekarang?"),
            ("relate", "Kita menaruh rumah di atas tanah karena percaya tanah diam."),
            ("setup", "28 September 2018, Palu. Getaran 7,5 dari sesar Palu-Koro."),
            ("tension", "Coba lihat Petobo. Rumah, jalan, pohon, bergerak satu arah."),
            ("tension", "Warga Kaili menyebutnya nalodo: tanah yang amblas, terhisap."),
            ("turn", "Tanahnya tidak menelan apa pun. Air di dalamnya yang membuat tanah berhenti jadi padat."),
            ("consequence", "Di Balaroa, 678 orang meninggal, dan 199 tidak pernah ditemukan."),
        ],
        turn_quote="“Tanahnya menelan mereka.”",
        turn_verdict="Tidak ada yang menelan. Air di dalam tanah membuatnya berhenti jadi padat, lalu bergerak.",
        loop="Tanah itu masih di sana, cuma tidak bisa dipijak. Kamu akan tinggal di atasnya?",
        cues=["PETOBO", "2018", "NALODO"],
        captions=["", "Apa yang kamu pijak?", "Kita percaya tanah diam.", "Palu, 2018.",
                  "Semua bergerak.", "Nalodo.", "Bukan ditelan.", "678 nama.",
                  "Kamu akan tinggal?"],
        caption_hi=["", "tanah", "tanah", "2018", "bergerak", "nalodo", "air", "678", "tinggal"],
        stamps=[["2018", 3]],
        sfx={"00_hook": "boom", "01_tanya": "page", "02_relate": "page", "03_setup": "gust",
             "04_tension": "boom", "05_tension": "page", "06_turn": "boom",
             "07_consequence": "clunk", "99_loop": "boom"},
        sumber=(
            "VERIFIED 2026-11-06 — Gempa 28 September 2018 (Mw 7,5) di sesar Palu-Koro memicu "
            "likuefaksi dan aliran lumpur di Balaroa dan Petobo (Kota Palu) serta Jono Oge (Kabupaten "
            "Sigi), Sulawesi Tengah. Rangkaian gempa susulan M6,4; 6,2; 6,1 terjadi sekitar 25 menit "
            "setelah gempa utama dan ikut memicu likuefaksi. Studi geoteknik (microtremor/MASW, "
            "semi-empiris) menyimpulkan likuefaksi terjadi hingga kedalaman ±16 meter karena sedimen "
            "lunak, muka air tanah dangkal, dan ground shear strain tinggi. Masyarakat Kaili menyebut "
            "peristiwa ini 'nalodo' (amblas/terhisap lumpur). Data BAPPENAS per 15 Februari 2019 untuk "
            "Kelurahan Balaroa: 678 meninggal, 199 hilang, 1.087 rumah rusak berat, 1.461 rumah hilang; "
            "area likuefaksi Balaroa ±40 Ha dari 238 Ha. Rujukan dibaca: Tempo (29 Sep 2023), Journal of "
            "Engineering and Technological Sciences 56(3) 2024, Springer Geo-environmental Disasters "
            "(2021), jurnal JRPP 7(4) 2024. Catatan: angka korban total Palu-Sigi-Donggala berbeda-beda "
            "antar sumber; naskah hanya memakai angka Balaroa dari BAPPENAS di atas. Belum dibaca "
            "langsung: laporan BNPB/BAPPENAS asli dan paper Bradley dkk. (2019) — verifikasi sebelum "
            "tayang."
        ),
    ),

    # ── EP16 · lukisan yang umurnya dihitung dari batu di atasnya ──────────
    "EP16": dict(
        title="LUKISAN TERTUA DI DUNIA ADA DI GUA KALIMANTAN, DAN PEMBUATNYA TIDAK DIKENAL",
        struktur="klimaks-awal",
        thumb=["BANTENG", "40.000 TAHUN"], thumb_text="BANTENG 40.000",
        durasi=43, plate="shelter",
        protagonis="Pindi Setiawan, arkeolog ITB yang ikut meneliti gua itu.",
        mau="Tahu siapa yang melukis, dan kapan.",
        hambatan="Yang tersisa cuma cat dan kapur; tidak ada tulang, tidak ada nama.",
        tanaman="Umur lukisan dihitung dari kerak kapur di atas cat.",
        hook="Di dinding gua Kalimantan ada banteng, dan umurnya 40.000 tahun.",
        hook_alt="Gambar banteng ini lebih tua dari piramida, dan tidak ada yang tahu siapa pembuatnya.",
        tanya="Kalau catnya sudah hilang, dari mana kamu tahu umur dinding itu?",
        entitas="banteng",
        relate="Kita menghitung umur dari batu kapur yang tumbuh di atasnya.",
        diskusi="Kalau lukisan itu bisa lebih tua lagi, apa artinya?",
        celah="Kenapa umur lukisan dihitung dari batu di atasnya?",
        gambar_melekat="Banteng merah di dinding kapur, dengan cap tangan di sebelahnya.",
        beats=[
            ("tanya", "Kalau catnya sudah hilang, dari mana kamu tahu umur dinding itu?"),
            ("relate", "Kita menghitung umur dari batu kapur yang tumbuh di atasnya."),
            ("setup", "Kutai Timur, 1994. Penjelajah Prancis menemukan gua ini."),
            ("tension", "Coba lihat cap tangannya. Satu berumur 51.800 tahun."),
            ("tension", "Di sebelahnya, gambar perahu dan orang, umurnya 20.000 tahun."),
            ("turn", "Yang diuji bukan catnya, tapi batu kapur yang menutupinya. Jadi angkanya batas minimum."),
            ("consequence", "Lukisan itu bisa lebih tua, dan tangan pembuatnya belum dikenal."),
        ],
        turn_quote="“Lukisan ini berumur 40.000 tahun.”",
        turn_verdict="Angka itu batas minimum: yang diuji kerak di atasnya, bukan catnya. Bisa jauh lebih tua.",
        loop="Banteng itu masih di dinding yang sama. Menurut kamu, siapa yang melukisnya?",
        cues=["SANGKULIRANG", "40.000 TH", "TANPA NAMA"],
        captions=["", "Dari mana tahu umurnya?", "Umur dari batu di atasnya.", "Kutai Timur, 1994.",
                  "Cap tangan 51.800.", "Perahu, 20.000.", "Batas minimum.", "Pembuatnya hilang.",
                  "Siapa yang melukis?"],
        caption_hi=["", "umur", "batu", "1994", "tangan", "perahu", "minimum", "nama", "melukis"],
        stamps=[["1994", 3]],
        sfx={"00_hook": "clunk", "01_tanya": "page", "02_relate": "page", "03_setup": "gust",
             "04_tension": "page", "05_tension": "page", "06_turn": "boom",
             "07_consequence": "rustle", "99_loop": "boom"},
        sumber=(
            "VERIFIED 2026-11-06 — Lubang Jeriji Saléh, kawasan karst Sangkulirang–Mangkalihat, "
            "Kabupaten Kutai Timur, Kalimantan Timur. Lukisan ditemukan penjelajah Prancis Luc-Henri "
            "Fage pada 1994. Penanggalan uranium-thorium terhadap kerak kalsit yang menutupi lukisan "
            "(bukan terhadap pigmennya) oleh tim Maxime Aubert (Griffith University) bersama Pindi "
            "Setiawan (ITB) dkk., terbit di Nature 2018: gambar hewan mirip banteng minimum 40.000 "
            "tahun — saat itu lukisan figuratif tertua yang diketahui; cap tangan oranye salah satunya "
            "berusia maksimum 51.800 tahun dan dua lainnya minimum 37.200 tahun; cap tangan warna "
            "murbei gelap serta gambar manusia, perahu, dan bentuk geometris berumur ±20.000–21.000 "
            "tahun. Karena metode ini menghitung umur kerak di atas cat, angka tersebut adalah umur "
            "minimum — lukisannya sendiri bisa lebih tua. Pindi Setiawan menyebut siapa senimannya dan "
            "apa yang terjadi pada mereka masih misteri. Rujukan dibaca: Kompas Sains (8 Nov 2018), "
            "Intisari/Grid (9 Nov 2018), abstrak Nature 'Palaeolithic cave art in Borneo'. Belum dibaca "
            "langsung: naskah penuh Nature 2018 (Aubert dkk.) dan laporan Balai Arkeologi — verifikasi "
            "sebelum tayang."
        ),
    ),

    # ── EP17 · gunung yang dianggap mati ───────────────────────────────────
    "EP17": dict(
        title="TIDAK MELETUS SEJAK 1600, LALU SATU PAGI GUNUNG INI KELUAR LAVA",
        struktur="klimaks-awal",
        thumb=["GUNUNG", "BANGUN"], thumb_text="GUNUNG BANGUN",
        durasi=43, plate="plume",
        protagonis="Warga Karo di lereng Sinabung yang mengungsi malam itu.",
        mau="Pulang ke rumah yang tidak lagi di zona aman.",
        hambatan="Tidak ada catatan letusan, jadi tidak ada yang siap.",
        tanaman="Catatan letusan terakhir: 1600.",
        hook="Gunung ini tidak pernah meletus sejak 1600, lalu satu pagi keluar lava.",
        hook_alt="Empat abad catatannya kosong. Lalu pada 2010 gunung ini bangun di tengah malam.",
        tanya="Kalau tidak ada catatan, bagaimana kamu tahu gunung itu masih hidup?",
        entitas="gunung",
        relate="Kita percaya catatan lebih dari gunungnya sendiri.",
        diskusi="Kalau kamu tinggal di lerengnya, kamu pindah sebelum atau sesudah?",
        celah="Kenapa gunung yang diam seribu tahun bisa bangun tanpa peringatan?",
        gambar_melekat="Asap tipis di puncak, dari gunung yang dianggap mati.",
        beats=[
            ("tanya", "Kalau tidak ada catatan, bagaimana kamu tahu gunung itu masih hidup?"),
            ("relate", "Kita percaya catatan lebih dari gunungnya sendiri."),
            ("setup", "Karo, 2.451 meter. Catatan terakhir 1600, lalu diam."),
            ("tension", "Coba lihat puncaknya. Ada kawah, dan asap tipis yang tidak pernah jadi berita."),
            ("tension", "Perkiraan letusan terakhir: tahun 800. Artinya seribu dua ratus tahun diam."),
            ("turn", "Diam bukan mati. Tekanan tetap menumpuk di bawah gunung."),
            ("consequence", "29 Agustus 2010, 12.000 orang mengungsi, dan satu tidak sampai."),
        ],
        turn_quote="“Gunungnya sudah mati.”",
        turn_verdict="Diam bukan mati. Catatan yang kosong cuma berarti tidak ada yang menulis.",
        loop="Gunung itu sekarang berasap tiap hari. Kamu masih akan tinggal di lerengnya?",
        cues=["SINABUNG", "2010", "1.200 TAHUN"],
        captions=["", "Masih hidup?", "Kita percaya catatan.", "Karo, 2.451 m.",
                  "Asap tanpa berita.", "Diam 1.200 tahun.", "Diam bukan mati.", "12.000 mengungsi.",
                  "Kamu masih tinggal?"],
        caption_hi=["", "hidup", "catatan", "Karo", "asap", "1.200", "tekanan", "12.000", "tinggal"],
        stamps=[["2010", 3]],
        sfx={"00_hook": "gust", "01_tanya": "page", "02_relate": "page", "03_setup": "clunk",
             "04_tension": "gust", "05_tension": "page", "06_turn": "boom",
             "07_consequence": "boom", "99_loop": "gust"},
        sumber=(
            "VERIFIED 2026-11-06 — Gunung Sinabung (Deleng Sinabung), Dataran Tinggi Karo, Kabupaten "
            "Karo, Sumatera Utara; stratovolcano 2.451 m. Tidak pernah tercatat meletus sejak 1600, "
            "dengan perkiraan letusan terakhir sekitar tahun 800 — artinya masa diamnya lebih dari "
            "seribu tahun, bukan empat abad. Aktif kembali: 27 Agustus 2010 mengeluarkan asap dan abu; "
            "29 Agustus 2010 dini hari sekitar 00.15 WIB mengeluarkan lava; status naik menjadi Awas; "
            "12.000 warga dievakuasi ke 8 lokasi; satu orang meninggal karena gangguan pernapasan saat "
            "mengungsi; abu terbawa sampai sebagian Kota Medan. Rujukan dibaca: Wikipedia Indonesia "
            "'Gunung Sinabung' (dengan rujukan Kompas, Detik, Liputan6, USGS) — status VERIFIED untuk "
            "tanggal dan angka evakuasi. Catatan: halaman itu juga mencantumkan letusan 31 Agustus 2026; "
            "belum dipakai di naskah karena belum ada rujukan berita yang dibaca. Belum dibaca langsung: "
            "siaran pers PVMBG/Badan Geologi 2010 dan kronologi resmi — verifikasi sebelum tayang."
        ),
    ),
}

for _e in EPISODES:
    if _e["ep"] in _INDONESIA_BATCH3:
        _e.update(_INDONESIA_BATCH3[_e["ep"]])

# ══════════════════════════════════════════════════════════════════════════
# BATCH 4 · EP18–EP20 · Maluku / Papua / Aceh
# ══════════════════════════════════════════════════════════════════════════

_INDONESIA_BATCH4 = {
    # ── EP18 · tanah yang naik dari laut dalam semalam ─────────────────────
    "EP18": dict(
        title="SETELAH GEMPA, PULAU BARU MUNCUL DI DEPAN KAMPUNG, DAN WARGA MENGUNGSI",
        struktur="klimaks-awal",
        thumb=["PULAU", "BARU"], thumb_text="PULAU BARU",
        durasi=43, plate="water",
        protagonis="Kepala Desa Teinaman yang memutuskan warganya mengungsi malam itu.",
        mau="Menyelamatkan warganya dari sesuatu yang naik dari laut.",
        hambatan="Tidak ada yang bisa menjelaskan apa yang muncul di depan pantai.",
        tanaman="Gempa 7,5 pukul 00.47 WIB.",
        hook="Setelah gempa, air di depan kampung ini naik dan jadi pulau.",
        hook_alt="Sebelum subuh, tanah naik dari laut di depan kampung ini.",
        tanya="Kalau pulau bisa muncul semalam, apa lagi yang bergerak di bawah kita?",
        entitas="pulau",
        relate="Kita cuma lihat permukaan, dan laut menyimpan sisanya.",
        diskusi="Kalau laut di depan rumahmu naik begini, kamu tunggu penjelasan atau langsung pergi?",
        celah="Kenapa gempa bisa memunculkan daratan baru dari laut?",
        gambar_melekat="Tumpukan lumpur gelap di depan pantai, tempat laut tadi.",
        beats=[
            ("tanya", "Kalau pulau bisa muncul semalam, apa lagi yang bergerak di bawah kita?"),
            ("relate", "Kita cuma lihat permukaan, dan laut menyimpan sisanya."),
            ("setup", "Tanimbar, 10 Januari 2023. Gempa 7,5 dari Laut Banda."),
            ("tension", "Coba lihat Desa Teinaman. Tanah naik di depan pantai."),
            ("tension", "Kepala desanya menyebut ini kejadian aneh, lalu mengungsi ke gunung."),
            ("turn", "Yang naik bukan pulau. Lumpur dari bawah menembus rekahan, lalu hilang."),
            ("consequence", "BMKG bilang gunung lumpur itu akan turun sendiri."),
        ],
        turn_quote="“Itu pulau baru.”",
        turn_verdict=("BMKG menyebutnya gunung lumpur: cairan dan gas terkurung di lapisan sedimen, "
                      "lalu mencari jalan keluar lewat rekahan setelah diguncang gempa. Peneliti BRIN "
                      "menyebut dasar laut dangkal yang terangkat. Dua-duanya bukan pulau yang bertahan."),
        loop="Pulau itu bisa hilang sebelum kamu sempat melihatnya. Kamu masih percaya pada yang terlihat di laut?",
        cues=["TEINAMAN", "2023", "M 7,5"],
        captions=["", "Apa lagi yang bergerak?", "Kita lihat permukaan.", "Tanimbar, 2023.",
                  "Tanah naik di pantai.", "Kepala desa mengungsi.", "Bukan pulau baru.",
                  "Akan turun sendiri.", "Kamu masih percaya?"],
        caption_hi=["", "bergerak", "permukaan", "2023", "tanah", "mengungsi", "lumpur", "turun", "percaya"],
        stamps=[["2023", 3]],
        sfx={"00_hook": "gust", "01_tanya": "page", "02_relate": "water", "03_setup": "gust",
             "04_tension": "water", "05_tension": "page", "06_turn": "boom",
             "07_consequence": "page", "99_loop": "water"},
        visual="Garis pantai Teinaman sebelum dan sesudah; potongan lapisan sedimen; peta Laut Banda.",
        sumber=(
            "VERIFIED 2026-11-06 — Gempa tektonik 10 Januari 2023 pukul 00.47.34 WIB, parameter "
            "akhir M7,5 (parameter awal M7,9), episenter 7,37 LS 130,23 BT, 136 km barat laut "
            "Kabupaten Kepulauan Tanimbar, kedalaman 130 km, subduksi Laut Banda, mekanisme naik "
            "(thrust fault). Setelah gempa, warga Desa Teinaman/Teinem (Kecamatan Wuarlabobar, "
            "Tanimbar Utara) melihat tumpukan material muncul di depan pantai dan mengungsi ke "
            "dataran tinggi; Kepala Desa Bony Kelmaskossu meminta warga mengungsi sementara. "
            "Kepala Bidang Mitigasi Gempa Bumi dan Tsunami BMKG, Daryono, menyebut fenomena itu "
            "gunung lumpur (mud volcano): cairan dan gas terkurung dalam sedimen menjadi "
            "overpressure lalu keluar lewat rekahan akibat guncangan gempa, dan umumnya akan "
            "hilang sendiri. Peneliti Pusat Riset Geoteknologi BRIN, Eko Yulianto, menjelaskan "
            "versi lain: pengangkatan daratan dangkal akibat siklus gempa (koseismik). Naskah "
            "memakai dua penjelasan itu tanpa memilih salah satu. Rujukan dibaca: detik.com "
            "10-11 Januari 2023 (kutipan BMKG), MalukuTerkini 11 Januari 2023 (parameter gempa), "
            "kicknews/Antara 11 Januari 2023 (kutipan BRIN), Suara Merdeka 11 Januari 2023. "
            "Belum dibaca langsung: rilis resmi BMKG dan laporan BNPB — verifikasi sebelum tayang."
        ),
    ),

    # ── EP19 · es yang dianggap abadi ternyata cuma menunggu suhu ──────────
    "EP19": dict(
        title="SALJU ABADI DI PUNCAK INI TINGGAL DUA PERSEN, DAN TAHUN INI BISA HABIS",
        struktur="klimaks-awal",
        thumb=["SALJU", "HABIS"], thumb_text="SALJU HABIS",
        durasi=42, plate="ridge",
        protagonis="Peneliti BMKG yang mengukur tebal es di Puncak Jaya.",
        mau="Mencatat es terakhir sebelum hilang.",
        hambatan="Esnya mencair lebih cepat dari jadwal pemantauan.",
        tanaman="Luas es 1988: 4,3 kilometer persegi.",
        hook="Salju abadi di puncak ini tinggal dua persen.",
        hook_alt="Di negara tropis ini ada salju yang bertahan ribuan tahun, dan tahun ini bisa jadi yang terakhir.",
        tanya="Di negara tropis, bagaimana ada es yang bertahan ribuan tahun?",
        entitas="salju",
        relate="Kita menyebutnya abadi, padahal es itu cuma menunggu suhu naik.",
        diskusi="Kalau es terakhir Indonesia hilang tahun ini, itu penting buat kamu?",
        celah="Kenapa es di puncak tertinggi Indonesia bisa habis secepat ini?",
        gambar_melekat="Batu gelap di puncak, bekas tempat es menempel.",
        beats=[
            ("tanya", "Di negara tropis, bagaimana ada es yang bertahan ribuan tahun?"),
            ("relate", "Kita menyebutnya abadi, padahal es itu cuma menunggu suhu naik."),
            ("setup", "Puncak Jaya, 4.884 meter, empat derajat di selatan khatulistiwa."),
            ("tension", "Coba lihat angka 1988. Esnya 4,3 kilometer persegi."),
            ("tension", "Sekarang tinggal 0,09 kilometer persegi. Tebalnya dari 32 meter jadi 4 meter."),
            ("turn", "Abadi itu cuma nama. Es bertahan selama suhunya di bawah beku."),
            ("consequence", "BMKG memperkirakan es itu habis akhir 2026 atau awal 2027."),
        ],
        turn_quote="“Saljunya abadi.”",
        turn_verdict=("Tidak ada yang abadi di 4.884 meter. Es bertahan selama udara di atasnya di bawah "
                      "titik beku; begitu suhu naik, tidak ada yang menahannya. Titik pemantauan terakhir "
                      "bahkan sudah kehilangan seluruh esnya — angka 2 persen itu sisa dari luas 1988."),
        loop="Kamu masih bisa lihat salju ini tahun ini. Kamu akan bilang apa ke anakmu nanti?",
        cues=["PUNCAK JAYA", "4.884 M", "2 PERSEN"],
        captions=["", "Kenapa bisa ada es?", "Kita sebut abadi.", "Puncak Jaya, 4.884 m.",
                  "1988: 4,3 kilometer.", "2025: 0,09 kilometer.", "Abadi cuma nama.",
                  "Habis 2027.", "Kamu akan bilang apa?"],
        caption_hi=["", "es", "abadi", "4.884", "4,3", "0,09", "suhu", "2027", "anak"],
        stamps=[["2026", 7]],
        sfx={"00_hook": "gust", "01_tanya": "page", "02_relate": "page", "03_setup": "gust",
             "04_tension": "tick", "05_tension": "page", "06_turn": "boom",
             "07_consequence": "clunk", "99_loop": "gust"},
        visual="Foto es Puncak Jaya 2010 dan 2024; grafik luas 1988-2025; peta Pegunungan Sudirman.",
        sumber=(
            "VERIFIED 2026-11-06 — Gletser tropis Puncak Jaya (4.884 m, Pegunungan Sudirman/"
            "Jayawijaya, Papua), satu-satunya es abadi di Indonesia, berada sekitar 4 derajat di "
            "selatan khatulistiwa. Luas tutupan es 1988 sekitar 4,3 km2; per September 2025 tinggal "
            "sekitar 0,09 km2 (sekitar 2 persen). Ketebalan 32 meter pada 2010 menjadi sekitar 4 "
            "meter pada 2023, dan titik pemantauan terakhir dilaporkan sudah kehilangan seluruh "
            "lapisan es. Laju pencairan sejak 2016 sekitar 2-2,5 meter per tahun. BMKG "
            "memperkirakan es itu hilang sepenuhnya pada akhir 2026 atau awal 2027, dipicu "
            "pemanasan global dan dipercepat El Nino; pemantauan BMKG November 2024 mencatat luas "
            "0,11-0,16 km2 dari 0,23 km2 pada 2022. BMKG menyebut es ini punya makna budaya dan "
            "spiritual bagi masyarakat adat Papua. Seluruh angka di naskah berasal dari pernyataan "
            "BMKG; tidak ada angka yang dihitung sendiri. Rujukan dibaca: detik.com 3 Juli 2026 dan "
            "6 Juli 2026 (kutipan rilis BMKG), RRI 4 Juli 2026, Kompas.id 12 April 2026 (hasil "
            "survei BMKG 11-15 November 2024). Belum dibaca langsung: laporan lengkap BMKG/BRIN dan "
            "paper Donaldi dkk. — verifikasi sebelum tayang. Catatan: angka 2 persen adalah luas "
            "terakhir yang dipublikasikan (September 2025), bukan pengukuran November 2026."
        ),
    ),

    # ── EP20 · peringatan bencana yang disimpan sebagai lagu tidur ─────────
    "EP20": dict(
        title="DI PULAU INI YANG MENYELAMATKAN ORANG BUKAN SIRENE, TAPI LAGU PENGANTAR TIDUR",
        struktur="klimaks-awal",
        thumb=["LAGU", "SELAMAT"], thumb_text="LAGU PENYELAMAT",
        durasi=44, plate="signal",
        protagonis="Warga Simeulue yang lari ke bukit mengikuti syair neneknya.",
        mau="Naik ke tempat tinggi sebelum gelombang datang.",
        hambatan="Tidak ada sirene, dan gelombang datang delapan menit setelah gempa.",
        tanaman="Kata smong dalam bahasa Devayan berarti tsunami.",
        hook="Di pulau ini, yang menyelamatkan orang bukan sirene, tapi lagu pengantar tidur.",
        hook_alt="Tidak ada sirene di pulau ini. Yang ada cuma lagu yang diajarkan nenek.",
        tanya="Kalau tidak ada sirene, apa yang membuat orang lari ke bukit?",
        entitas="lagu",
        relate="Kita menaruh peringatan di nyanyian pengantar tidur anak.",
        diskusi="Di tempatmu, peringatan bencana diajarkan lewat apa?",
        celah="Kenapa lagu bisa menyelamatkan lebih banyak orang daripada alat?",
        gambar_melekat="Anak-anak tidur sambil mendengar syair soal gelombang.",
        beats=[
            ("tanya", "Kalau tidak ada sirene, apa yang membuat orang lari ke bukit?"),
            ("relate", "Kita menaruh peringatan di nyanyian pengantar tidur anak."),
            ("setup", "Simeulue, 26 Desember 2004. Gempa 9,1, dan laut surut."),
            ("tension", "Coba ingat syairnya: gempa, air surut, lari ke tempat tinggi."),
            ("tension", "Dari 78.000 orang di pulau itu, tujuh yang meninggal. Kita jarang dengar angka sekecil itu."),
            ("turn", "Syair itu bukan hiburan. Ia lagu pengantar tidur anak, supaya diingat saat panik."),
            ("consequence", "Desa Langi rata dengan tanah, dan 800 orangnya selamat."),
        ],
        turn_quote="“Orang desa tidak mungkin tahu tanda tsunami.”",
        turn_verdict=("Mereka tahu, karena syairnya menyebut urutannya: gempa kuat, air laut surut, lalu cari "
                      "tempat lebih tinggi. Yang tidak ada di pulau itu justru sirene — dan syair itu "
                      "diajarkan sebagai nandong, lagu pengantar tidur, sejak tsunami 1907."),
        loop="Sekarang sirene ada di mana-mana. Tapi kamu masih ingat lagu yang diajarkan ibumu?",
        cues=["SIMEULUE", "2004", "SMONG"],
        captions=["", "Apa yang bikin lari?", "Kita simpan di lagu.", "Simeulue, 2004.",
                  "Gempa, surut, naik.", "Tujuh orang.", "Bukan hiburan.",
                  "Langi rata, 800 selamat.", "Kamu ingat lagunya?"],
        caption_hi=["", "sirene", "lagu", "2004", "surut", "tujuh", "syair", "800", "ingat"],
        stamps=[["2004", 3]],
        sfx={"00_hook": "tick", "01_tanya": "page", "02_relate": "page", "03_setup": "gust",
             "04_tension": "water", "05_tension": "page", "06_turn": "boom",
             "07_consequence": "boom", "99_loop": "page"},
        visual="Peta Simeulue dan jarak Desa Langi ke episenter; teks nandong smong; garis waktu 1907-2004.",
        sumber=(
            "VERIFIED 2026-11-06 — Gempa 26 Desember 2004 (Mw 9,1-9,2) memicu tsunami; di Pulau "
            "Simeulue, Aceh, jumlah korban jauh lebih kecil daripada wilayah lain. McAdoo dkk. "
            "(Earthquake Spectra, 2006) mencatat warga Desa Langi, sekitar 40 km dari episenter, "
            "langsung lari ke dataran tinggi hanya dengan waktu sekitar 8 menit; desa itu rata "
            "dengan tanah tetapi sekitar 800 warganya selamat. Rahman, Sakurai & Munadi (2017) "
            "menuliskan 7 korban meninggal dari populasi sekitar 78.000 (sensus 2000); sumber lain, "
            "termasuk kutipan PBB 2024, menyebut 6 korban — naskah memakai angka 7 dari Rahman dkk. "
            "Pengetahuan itu bernama smong (bahasa Devayan: tsunami), diwariskan lewat nandong, "
            "syair/lagu pengantar tidur, yang isinya antara lain: gempa kuat ('unen ne alek linon') "
            "diikuti air laut surut ('uwek suruik sahuli'), lalu segera cari tempat lebih tinggi "
            "('fano me singa tenggi'). Tradisi ini berakar pada tsunami 1907 yang menurut legenda "
            "menewaskan sekitar 70 persen penduduk pulau. Rujukan dibaca: NALAR/National Archaeology "
            "Indonesia (teks nandong beserta terjemahan, mengutip McAdoo dkk. 2006), Suara.com "
            "26 Oktober 2026 (kutipan jurnal Societies 2026 dan angka PBB 2024), abstrak Rahman dkk. "
            "2017 (ScienceDirect), abstrak penelitian Smong 2024. Belum dibaca langsung: naskah "
            "penuh McAdoo dkk. 2006 dan Rahman dkk. 2017 — verifikasi sebelum tayang. Angka korban "
            "1907 adalah legenda, bukan statistik resmi."
        ),
    ),
}

for _e in EPISODES:
    if _e["ep"] in _INDONESIA_BATCH4:
        _e.update(_INDONESIA_BATCH4[_e["ep"]])


# ══════════════════════════════════════════════════════════════════════════
# TANGGA KUALITAS · 15 Nov 2026 — tier topik + fokus + perbaikan per episode
#
# Aturan pemilik: setiap episode harus menaikkan satu keterampilan, dan
# sekaligus menutup satu kelemahan episode sebelumnya. Isi `fokus` = yang
# dilatih, `perbaikan` = kelemahan episode sebelumnya yang ditutup.
# `tier` dipakai gerbang topik (tools/score_topic.py): selama kemampuan POV
# belum L4, hanya `misteri` dan `kontroversi` yang boleh masuk.
# `topik_status`: pakai / ganti / tunda.
# Lihat SKILLS/16_TOPIK_DAN_KURIKULUM.md.
# ══════════════════════════════════════════════════════════════════════════

_LADDER = {
    "EP01": dict(tier="misteri", topik_status="arsip",
                 fokus="L1 kronologi: tanggal, tempat, satu detail fisik",
                 perbaikan="— (episode pertama; belum ada yang bisa diperbaiki)"),
    "EP02": dict(tier="misteri", topik_status="arsip",
                 fokus="L2 petunjuk: urutan kejanggalan tanpa putusan",
                 perbaikan="EP01 kurang investigasi — EP02 menambah tiga petunjuk berurut"),
    "EP03": dict(tier="misteri", topik_status="arsip",
                 fokus="L1 kronologi yang lebih ketat (rute, kargo, tanggal)",
                 perbaikan="EP02 tidak punya angka terukur — EP03 memakai kargo dan tanggal"),
    "EP04": dict(tier="misteri", topik_status="arsip",
                 fokus="L2 petunjuk dari benda (kunci, tangki, sepatu)",
                 perbaikan="EP03 kronologi kuat, taruhan manusia lemah — EP04 memakai lima keluarga"),
    "EP05": dict(tier="misteri", topik_status="arsip",
                 fokus="L1 kronologi tiga tahun + satu kata",
                 perbaikan="EP04 bukti bertumpuk tanpa arah — EP05 memusatkan satu kata sebagai bukti"),
    "EP06": dict(tier="peristiwa", topik_status="arsip",
                 fokus="L3 sebab-akibat: satu keputusan kecil yang berjalan 60 tahun",
                 perbaikan="EP05 dua pihak tidak ada — EP06 menambah versi dewan kota vs warga"),
    "EP07": dict(tier="misteri", topik_status="arsip",
                 fokus="L2 petunjuk fisik (jejak, loteng, kandang)",
                 perbaikan="EP06 taruhan manusia abstrak — EP07 memakai enam korban bernama"),
    "EP08": dict(tier="misteri", topik_status="arsip",
                 fokus="L4 POV: benda sebagai satu-satunya saksi (label yang dipotong)",
                 perbaikan="EP07 kronologi berlapis tapi tidak ada satu pun dokumen ditunjuk — EP08 memakai isi koper"),
    "EP09": dict(tier="misteri", topik_status="pakai",
                 fokus="L7 subjek manusia: keluarga yang menuntut satu nama",
                 perbaikan="EP08 topik luar negeri, kedekatan nol — EP09 memakai kasus Indonesia yang masih terbuka"),
    "EP10": dict(tier="misteri", topik_status="pakai",
                 fokus="L4 POV: identitas sebagai objek yang hilang, bukan pelaku",
                 perbaikan="EP09 taruhan keluarga kuat tapi bukti terukur lemah — EP10 memakai sidik jari, 27 Nov 1981, TPU Tegal Alur"),
    "EP11": dict(tier="kontroversi", topik_status="pakai",
                 fokus="L3 dua klaim bertarung: perusahaan vs ahli geologi, sintesa di turn",
                 perbaikan="EP10 menutup dengan pertanyaan tapi tanpa lawan klaim — EP11 memperbaiki E (tesa-antitesa)"),
    "EP12": dict(tier="misteri", topik_status="pakai",
                 fokus="L2 bukti terukur: setiap angka di VO punya label di layar",
                 perbaikan="EP11 angka sudah ada di VO tapi belum semua tampil di layar"),
    "EP13": dict(tier="umum", topik_status="tunda",
                 fokus="L5 dokumen di layar: kutipan sumber saat klaim diucapkan",
                 perbaikan="EP12 tidak ada dokumen — EP13 belajar menampilkan kutipan"),
    "EP14": dict(tier="umum", topik_status="ganti",
                 fokus="L5 dokumen di layar (lanjutan), tanpa mengarang bukti",
                 perbaikan="EP13 klaim budaya vs sains tidak berimbang — EP14 belajar menimbang dua klaim"),
    "EP15": dict(tier="peristiwa", topik_status="pakai",
                 fokus="L6 kontroversi berimbang: peta zona merah vs warga yang kembali",
                 perbaikan="EP14 bukti visual lemah — EP15 memakai rekaman dan peta likuefaksi"),
    "EP16": dict(tier="umum", topik_status="ganti",
                 fokus="L4 POV: siapa yang menghitung umur, dan dengan alat apa",
                 perbaikan="EP15 kronologi bencana terlalu padat — EP16 belajar memilih satu detail saja"),
    "EP17": dict(tier="peristiwa", topik_status="pakai",
                 fokus="L6 kontroversi berimbang: warga yang menolak pindah dari zona merah",
                 perbaikan="EP16 taruhan manusia tipis — EP17 memakai orang yang tinggal di lereng"),
    "EP18": dict(tier="umum", topik_status="ganti",
                 fokus="L2 bukti terukur (peta, citra, pengukuran)",
                 perbaikan="EP17 angka letusan belum punya pasangan visual"),
    "EP19": dict(tier="umum", topik_status="ganti",
                 fokus="L5 dokumen ilmiah di layar",
                 perbaikan="EP18 sumber masih berita, bukan dokumen"),
    "EP20": dict(tier="peristiwa", topik_status="tunda",
                 fokus="L7 subjek manusia: yang selamat karena cerita, bukan karena alat",
                 perbaikan="EP19 tidak ada manusia — EP20 mengembalikan taruhan manusia"),
    "EP21": dict(tier="kontroversi", topik_status="pakai",
                 fokus="L3 dua klaim bertarung: dokter perusahaan vs pengukuran radiasi sendiri",
                 perbaikan="EP20 klaim tunggal — EP21 memakai dokumen perusahaan yang berlawanan dengan kesaksiannya"),
}

for _e in EPISODES:
    _e.update(_LADDER.get(_e["ep"], {}))

# ══════════════════════════════════════════════════════════════════════════
# EPISODE PILOT TERPISAH — tidak masuk generator kalender 21 episode.
#
# AK-EP12 hanya dipakai oleh pemeriksa naskah. Ia sengaja berada di koleksi
# terpisah agar generator program 21 episode tidak menciptakan aset/tayangan
# otomatis untuk pilot yang tetap memerlukan persetujuan render/master dan publikasi terpisah.
# ══════════════════════════════════════════════════════════════════════════

AK_EPISODES = [
    dict(
        ep="AK-EP12", voice_legacy=False, day=0, slot="review", jam="—",
        series="KASUS NYATA", pov="D", tier="kontroversi", topik_status="draf-short",
        fokus="L2 bukti terukur: 45, 188, 21, 3, dan 164 muncul bersama label konteks.",
        perbaikan=("Tidak mengulang narasi 100+ detik: satu pertanyaan, sembilan segmen, "
                   "dan nomor korban tidak disamakan dengan kematian pasti."),
        short_parent="11_CONTENT/07_LONGFORM/LF03_sinar-bangun/SCRIPT.md",
        title="188 NAMA YANG DIHITUNG SESUDAH KAPAL TENGGELAM",
        struktur="klimaks-awal", thumb=["188", "NAMA"], thumb_text="188 NAMA",
        durasi=42, plate="vessel", photos=[],
        measured_duration_seconds=41.36,
        protagonis="Angka 188 yang baru disusun di posko sembilan hari setelah kapal tenggelam.",
        mau="Menjawab siapa yang perlu dicari sebelum daftar dapat dipastikan.",
        hambatan="Jumlah penumpang baru diverifikasi setelah kecelakaan.",
        tanaman="Angka 188: hasil posko hari kesembilan, bukan angka keberangkatan.",
        hook="Angka 188 muncul sembilan hari sesudah kapal tenggelam.",
        hook_alt="Kapal berangkat. Angka 188 muncul sembilan hari kemudian.",
        tanya="Kenapa 188 muncul belakangan?",
        entitas="angka",
        relate="Kita kira 188 dihitung di dermaga.",
        diskusi="Apakah jumlah penumpang harus diumumkan sebelum kapal berangkat?",
        celah="Mengapa 188 baru muncul sesudah kapal tenggelam?",
        gambar_melekat="Angka 188 muncul di posko sembilan hari setelah kapal hilang.",
        beats=[
            ("tanya", "Kenapa 188 muncul belakangan?"),
            ("relate", "Kita kira 188 dihitung di dermaga."),
            ("setup", "18 Juni 2018, kapal berangkat 16.50."),
            ("tension", "Dua puluh menit, gelombang 1,5 sampai 2 meter membalikkan kapal."),
            ("tension", "Dokumen 45, posko 188: 21 selamat, 3 meninggal, 164 hilang."),
            ("turn", "KNKT: 188 bukan angka dermaga."),
            ("consequence", "KNKT meminta manifest sebelum berangkat."),
        ],
        turn_quote="“188 adalah angka keberangkatan.”",
        turn_verdict=("Laporan KNKT menjelaskan 188 berasal dari verifikasi posko hari "
                      "kesembilan, bukan manifest keberangkatan."),
        loop="Hitung 188 sebelum kapal berangkat, atau cari?",
        cues=["HARI KE-9", "188", "45 KE 188", "16.50 KE 17.10"],
        captions=["", "Kenapa 188?", "188 di dermaga?", "18 Juni 2018.",
                  "Dua puluh menit.", "45. 21. 3. 164.", "Bukan angka dermaga.",
                  "Manifest.", "Hitung atau cari?"],
        caption_hi=["", "188", "188", "2018", "dua puluh", "164", "188", "manifest", "188"],
        stamps=[["188", 0], ["45", 5]],
        sfx={},
        visual=("Penghitung posko 188, peta Simanindo–Tigaras, timeline 16.50–17.10, "
                "dan diagram dokumen 45 versus posko 188. Semua frame final Remotion."),
        sumber=(
            "TERVERIFIKASI 2026-11-06 — KNKT.18.06.21.03, bagian sinopsis, kronologi, "
            "dan SAR dibaca langsung; ringkasan rilis hasil KNKT ANTARA Sumut serta rekomendasi "
            "KNKT melalui INSA dipakai dengan atribusi. 188 adalah verifikasi posko hari kesembilan: "
            "21 selamat, 3 meninggal, 164 hilang. Tidak memakai klaim SPB/izin atau tuduhan pidana. "
            "Fakta: 11_CONTENT/02_SCRIPT/riset/AK-EP12_sinar-bangun_fakta.md. Induk: "
            "11_CONTENT/07_LONGFORM/LF03_sinar-bangun/SCRIPT.md."
        ),
    ),
]
