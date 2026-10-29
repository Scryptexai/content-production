import type { LongProps } from "./LongForm";

export const LONG: LongProps = {
  "id": "RW1L",
  "tone": "ink",
  "chapter": "01 / KERJA",
  "source": "Benson, Li & Shue — Promotions and the Peter Principle, QJE 134(4), 2019",
  "preview": true,
  "blocks": [
    {
      "key": "b1",
      "scene": "adegan",
      "kicker": "2019 · DATA PERUSAHAAN",
      "headline": "Tiga ekonom. 131 perusahaan.",
      "stats": [
        {
          "value": "131",
          "label": "perusahaan"
        },
        {
          "value": "38.843",
          "label": "tenaga penjualan"
        },
        {
          "value": "1.553",
          "label": "promosi jadi manajer"
        }
      ],
      "anim": "s1_hall",
      "vo": "RW1L-b1.mp3",
      "from": 24,
      "to": 504
    },
    {
      "key": "b2",
      "scene": "metode",
      "kicker": "CARA MENGUKUR",
      "headline": "Yang dihitung bukan kesan, tapi selisih.",
      "before": {
        "t": "sebelum ia menjabat",
        "v": "penjualan tim"
      },
      "after": {
        "t": "sesudah ia menjabat",
        "v": "penjualan tim"
      },
      "note": "selisihnya = nilai tambah manajer",
      "anim": "s2_measure",
      "vo": "RW1L-b2.mp3",
      "from": 518,
      "to": 1090
    },
    {
      "key": "b3",
      "scene": "bar",
      "kicker": "APA YANG MEMBUAT DIPROMOSIKAN",
      "headline": "Penjualan berlipat dua.",
      "bars": [
        {
          "label": "peluang promosi",
          "value": 14.3,
          "display": "+14%",
          "accent": "sage"
        }
      ],
      "footnote": "relatif terhadap laju dasar promosi",
      "anim": "s3_sales",
      "vo": "RW1L-b3.mp3",
      "from": 1103,
      "to": 1667
    },
    {
      "key": "b4",
      "scene": "kurva",
      "kicker": "SETELAH PROMOSI",
      "headline": "Yang terbaik saat menjual, terburuk saat memimpin tim.",
      "labelA": "penjualan sebelum promosi",
      "labelB": "penjualan tim sesudahnya",
      "value": "−7,5%",
      "anim": "s4_team_drop",
      "vo": "RW1L-b4.mp3",
      "from": 1680,
      "to": 2266
    },
    {
      "key": "b5",
      "scene": "prediktor",
      "kicker": "YANG SEBENARNYA MEMPREDIKSI",
      "headline": "Bukan bakat. Pernah melihat pekerjaan orang lain dari dekat.",
      "rows": [
        {
          "label": "penjualan sebelum promosi",
          "value": "−7,5%",
          "tone": "rose"
        },
        {
          "label": "pengalaman lintas tim",
          "value": "+15,8%",
          "tone": "sage"
        }
      ],
      "anim": "s5_cross_team",
      "vo": "RW1L-b5.mp3",
      "from": 2280,
      "to": 2830
    },
    {
      "key": "b6",
      "scene": "kontrafaktual",
      "kicker": "SATU SKENARIO YANG DIHITUNG PENULIS",
      "headline": "Kalau memilih dengan benar.",
      "value": "+30%",
      "note": "bukan lebih banyak promosi — kualitas manajernya",
      "anim": "s6_towers",
      "vo": "RW1L-b6.mp3",
      "from": 2844,
      "to": 3430
    },
    {
      "key": "b7",
      "scene": "mekanisme",
      "kicker": "KENAPA PERUSAHAAN TETAP MELAKUKANNYA",
      "headline": "Promosi mengerjakan dua hal sekaligus.",
      "left": {
        "t": "seleksi",
        "d": "siapa yang akan jadi manajer bagus"
      },
      "right": {
        "t": "hadiah",
        "d": "siapa yang layak diberi imbalan"
      },
      "note": "dua tujuan ini menginginkan orang yang berbeda",
      "anim": "s7_reward",
      "vo": "RW1L-b7.mp3",
      "from": 3443,
      "to": 4259
    },
    {
      "key": "b8",
      "scene": "kutipan",
      "kicker": "BUKAN GAGASAN BARU",
      "quote": "Setiap karyawan cenderung naik ke tingkat ketidakmampuannya.",
      "attrib": "Laurence J. Peter, 1969 — ditulis sebagai satire",
      "anim": "s8_peter",
      "vo": "RW1L-b8.mp3",
      "from": 4272,
      "to": 4880
    },
    {
      "key": "b9",
      "scene": "batas",
      "kicker": "BATAS DATA",
      "headline": "Yang tidak bisa dijawab data ini.",
      "chips": [
        "tenaga penjualan",
        "perusahaan Amerika",
        "kinerja terukur"
      ],
      "unknown": "apakah memilih dengan tepat membuat perusahaan lebih untung — itu tidak diuji",
      "anim": "s9_bounds",
      "vo": "RW1L-b9.mp3",
      "from": 4894,
      "to": 5604
    },
    {
      "key": "b10",
      "scene": "tanya",
      "kicker": "PENUTUP",
      "question": "Kalau promosi di tempatmu ternyata bekerja sebagai hadiah — siapa yang sebenarnya sedang dipilih?",
      "anim": "s10_question",
      "vo": "RW1L-b10.mp3",
      "from": 5618,
      "to": 6106
    }
  ],
  "beats": [
    {
      "span": 1,
      "kind": "stat",
      "plate": "grid",
      "accent": "cream",
      "kicker": "2019 · DATA PERUSAHAAN",
      "big": "131",
      "mid": "perusahaan Amerika",
      "key": "b1-1",
      "block": "b1",
      "from": 24,
      "to": 143,
      "plateFrom": 0
    },
    {
      "span": 1,
      "kind": "pair",
      "plate": "columns",
      "accent": "rose",
      "kicker": "ISI DATANYA",
      "pairs": [
        [
          "38.843",
          "tenaga penjualan"
        ],
        [
          "1.553",
          "promosi jadi manajer"
        ]
      ],
      "key": "b1-2",
      "block": "b1",
      "from": 143,
      "to": 335,
      "plateFrom": 97
    },
    {
      "span": 1,
      "kind": "line",
      "plate": "grid",
      "accent": "cream",
      "big": "Bukan sampel kecil.",
      "sub": [
        "berlaku di hampir semua perusahaan itu"
      ],
      "key": "b1-3",
      "block": "b1",
      "from": 335,
      "to": 518,
      "plateFrom": 194
    },
    {
      "span": 1,
      "kind": "line",
      "plate": "columns",
      "accent": "sage",
      "kicker": "CARA MENGUKUR",
      "big": "Caranya sederhana.",
      "sub": [
        "tapi hampir tidak pernah dilakukan"
      ],
      "key": "b2-1",
      "block": "b2",
      "from": 518,
      "to": 605,
      "plateFrom": 0
    },
    {
      "span": 1,
      "kind": "line",
      "plate": "tunnel",
      "accent": "rose",
      "big": "Bukan kesan.",
      "sub": [
        "bukan wawancara atasan"
      ],
      "key": "b2-2",
      "block": "b2",
      "from": 605,
      "to": 740,
      "plateFrom": 97
    },
    {
      "span": 0.55,
      "kind": "split",
      "plate": "columns",
      "accent": "sage",
      "kicker": "YANG DIHITUNG",
      "before": "penjualan tim",
      "after": "penjualan tim",
      "labelBefore": "sebelum ia menjabat",
      "labelAfter": "sesudah ia menjabat",
      "key": "b2-3",
      "block": "b2",
      "from": 740,
      "to": 932,
      "plateFrom": 194
    },
    {
      "span": 0.45,
      "kind": "line",
      "plate": "tunnel",
      "accent": "sage",
      "big": "Selisihnya,",
      "sub": [
        "nilai tambah manajer"
      ],
      "key": "b2-4",
      "block": "b2",
      "from": 932,
      "to": 1103,
      "plateFrom": 291
    },
    {
      "span": 1,
      "kind": "line",
      "plate": "columns",
      "accent": "cream",
      "kicker": "PERTANYAANNYA",
      "big": "Apa yang membuat seseorang dipromosikan?",
      "key": "b3-1",
      "block": "b3",
      "from": 1103,
      "to": 1224,
      "plateFrom": 0
    },
    {
      "span": 1,
      "kind": "word",
      "plate": "tunnel",
      "accent": "rose",
      "big": "Penjualan.",
      "key": "b3-2",
      "block": "b3",
      "from": 1224,
      "to": 1267,
      "plateFrom": 97
    },
    {
      "span": 1,
      "kind": "bars",
      "plate": "columns",
      "accent": "sage",
      "kicker": "PENJUALAN BERLIPAT DUA",
      "bars": [
        [
          "peluang promosi",
          14,
          "+14%",
          "sage"
        ]
      ],
      "sub": [
        "relatif terhadap laju dasar"
      ],
      "key": "b3-3",
      "block": "b3",
      "from": 1267,
      "to": 1461,
      "plateFrom": 194
    },
    {
      "span": 1,
      "kind": "line",
      "plate": "tunnel",
      "accent": "cream",
      "big": "Yang dinilai: pekerjaan lama.",
      "sub": [
        "bukan kemampuan di pekerjaan baru"
      ],
      "key": "b3-4",
      "block": "b3",
      "from": 1461,
      "to": 1680,
      "plateFrom": 291
    },
    {
      "span": 1,
      "kind": "line",
      "plate": "wire",
      "accent": "cream",
      "kicker": "SESUDAH PROMOSI",
      "big": "Dan hal aneh terjadi.",
      "key": "b4-1",
      "block": "b4",
      "from": 1680,
      "to": 1767,
      "plateFrom": 0
    },
    {
      "span": 1,
      "kind": "line",
      "plate": "tunnel",
      "accent": "rose",
      "big": "Penjual terbaik, pemimpin terburuk.",
      "sub": [
        "saat memimpin tim"
      ],
      "key": "b4-2",
      "block": "b4",
      "from": 1767,
      "to": 1880,
      "plateFrom": 97
    },
    {
      "span": 0.6,
      "kind": "stat",
      "plate": "wire",
      "accent": "rose",
      "kicker": "PENJUALAN PRA-PROMOSI BERLIPAT DUA",
      "big": "−7,5%",
      "mid": "penjualan rata-rata anak buahnya",
      "key": "b4-3",
      "block": "b4",
      "from": 1880,
      "to": 2026,
      "plateFrom": 194
    },
    {
      "span": 0.4,
      "kind": "line",
      "plate": "tunnel",
      "accent": "rose",
      "big": "Makin hebat menjual,",
      "sub": [
        "makin besar penurunan timnya"
      ],
      "key": "b4-4",
      "block": "b4",
      "from": 2026,
      "to": 2123,
      "plateFrom": 291
    },
    {
      "span": 1,
      "kind": "line",
      "plate": "wire",
      "accent": "cream",
      "big": "Semakin hebat ia menjual,",
      "sub": [
        "semakin besar penurunan yang ia bawa"
      ],
      "key": "b4-5",
      "block": "b4",
      "from": 2123,
      "to": 2280,
      "plateFrom": 388
    },
    {
      "span": 1,
      "kind": "line",
      "plate": "columns",
      "accent": "sage",
      "kicker": "YANG SEBENARNYA MEMPREDIKSI",
      "big": "Ternyata hal lain.",
      "key": "b5-1",
      "block": "b5",
      "from": 2280,
      "to": 2456,
      "plateFrom": 0
    },
    {
      "span": 1,
      "kind": "stat",
      "plate": "tunnel",
      "accent": "sage",
      "kicker": "PENGALAMAN LINTAS TIM BERLIPAT DUA",
      "big": "+15,8%",
      "mid": "nilai tambah manajer",
      "key": "b5-2",
      "block": "b5",
      "from": 2456,
      "to": 2587,
      "plateFrom": 97
    },
    {
      "span": 1,
      "kind": "word",
      "plate": "columns",
      "accent": "cream",
      "big": "Bukan bakat mistis.",
      "key": "b5-3",
      "block": "b5",
      "from": 2587,
      "to": 2634,
      "plateFrom": 194
    },
    {
      "span": 1,
      "kind": "line",
      "plate": "tunnel",
      "accent": "cream",
      "big": "Pernah melihat pekerjaan orang lain dari dekat.",
      "sub": [
        "dan tahu bagian mana yang gampang rusak"
      ],
      "key": "b5-4",
      "block": "b5",
      "from": 2634,
      "to": 2844,
      "plateFrom": 291
    },
    {
      "span": 1,
      "kind": "line",
      "plate": "wire",
      "accent": "cream",
      "kicker": "SATU SKENARIO DIHITUNG",
      "big": "Kalau memilih dengan benar.",
      "key": "b6-1",
      "block": "b6",
      "from": 2844,
      "to": 2931,
      "plateFrom": 0
    },
    {
      "span": 0.5,
      "kind": "grid30",
      "plate": "grid",
      "accent": "sage",
      "big": "+30%",
      "mid": "kualitas manajer",
      "key": "b6-2",
      "block": "b6",
      "from": 2931,
      "to": 3095,
      "plateFrom": 97
    },
    {
      "span": 0.5,
      "kind": "line",
      "plate": "wire",
      "accent": "sage",
      "big": "Dipilih dari potensi manajerial.",
      "sub": [
        "bukan dari penjualan"
      ],
      "key": "b6-3",
      "block": "b6",
      "from": 3095,
      "to": 3258,
      "plateFrom": 194
    },
    {
      "span": 1,
      "kind": "line",
      "plate": "grid",
      "accent": "rose",
      "big": "Bukan 30% lebih banyak promosi.",
      "key": "b6-4",
      "block": "b6",
      "from": 3258,
      "to": 3373,
      "plateFrom": 291
    },
    {
      "span": 1,
      "kind": "word",
      "plate": "wire",
      "accent": "cream",
      "big": "Kualitas orangnya.",
      "key": "b6-5",
      "block": "b6",
      "from": 3373,
      "to": 3443,
      "plateFrom": 388
    },
    {
      "span": 1,
      "kind": "line",
      "plate": "tunnel",
      "accent": "rose",
      "kicker": "KESIMPULAN TERMUDAH",
      "big": "Justru gagal di sini.",
      "key": "b7-1",
      "block": "b7",
      "from": 3443,
      "to": 3560,
      "plateFrom": 0
    },
    {
      "span": 1,
      "kind": "word",
      "plate": "wire",
      "accent": "cream",
      "big": "Perusahaan tidak bodoh.",
      "key": "b7-2",
      "block": "b7",
      "from": 3560,
      "to": 3667,
      "plateFrom": 97
    },
    {
      "span": 0.5,
      "kind": "list",
      "plate": "tunnel",
      "accent": "sage",
      "kicker": "BOBOT PENJUALAN DITURUNKAN SAAT",
      "items": [
        "jabatan manajerialnya lebih berat"
      ],
      "key": "b7-3",
      "block": "b7",
      "from": 3667,
      "to": 3826,
      "plateFrom": 194
    },
    {
      "span": 0.5,
      "kind": "list",
      "plate": "wire",
      "accent": "sage",
      "kicker": "BOBOT PENJUALAN DITURUNKAN SAAT",
      "items": [
        "jabatan manajerialnya lebih berat",
        "gaji anak buah bergantung pada performa"
      ],
      "key": "b7-4",
      "block": "b7",
      "from": 3826,
      "to": 3984,
      "plateFrom": 291
    },
    {
      "span": 1,
      "kind": "line",
      "plate": "tunnel",
      "accent": "cream",
      "big": "Promosi bukan cuma alat memilih.",
      "key": "b7-5",
      "block": "b7",
      "from": 3984,
      "to": 4079,
      "plateFrom": 388
    },
    {
      "span": 1,
      "kind": "line",
      "plate": "wire",
      "accent": "rose",
      "big": "Promosi juga hadiah.",
      "sub": [
        "bagi yang masih di lapangan dan sedang menonton"
      ],
      "key": "b7-6",
      "block": "b7",
      "from": 4079,
      "to": 4272,
      "plateFrom": 65
    },
    {
      "span": 1,
      "kind": "line",
      "plate": "grid",
      "accent": "cream",
      "kicker": "BUKAN GAGASAN BARU",
      "big": "Ditulis pada 1969.",
      "key": "b8-1",
      "block": "b8",
      "from": 4272,
      "to": 4316,
      "plateFrom": 0
    },
    {
      "span": 1,
      "kind": "quote",
      "plate": "wire",
      "accent": "cream",
      "big": "Setiap karyawan cenderung naik ke tingkat ketidakmampuannya.",
      "who": "Laurence J. Peter, 1969 — ditulis sebagai satir",
      "key": "b8-2",
      "block": "b8",
      "from": 4316,
      "to": 4599,
      "plateFrom": 97
    },
    {
      "span": 1,
      "kind": "line",
      "plate": "grid",
      "accent": "cream",
      "big": "Lima puluh tahun: cuma sindiran.",
      "sub": [
        "tentang birokrasi"
      ],
      "key": "b8-3",
      "block": "b8",
      "from": 4599,
      "to": 4743,
      "plateFrom": 194
    },
    {
      "span": 1,
      "kind": "line",
      "plate": "wire",
      "accent": "sage",
      "big": "Datanya mengubah itu.",
      "key": "b8-4",
      "block": "b8",
      "from": 4743,
      "to": 4894,
      "plateFrom": 291
    },
    {
      "span": 1,
      "kind": "line",
      "plate": "grid",
      "accent": "rose",
      "kicker": "BATAS DATA",
      "big": "Batasnya harus disebut.",
      "key": "b9-1",
      "block": "b9",
      "from": 4894,
      "to": 4950,
      "plateFrom": 0
    },
    {
      "span": 1,
      "kind": "chips",
      "plate": "columns",
      "accent": "cream",
      "chips": [
        "tenaga penjualan",
        "perusahaan Amerika",
        "kinerja terukur"
      ],
      "key": "b9-2",
      "block": "b9",
      "from": 4950,
      "to": 5201,
      "plateFrom": 97
    },
    {
      "span": 1,
      "kind": "line",
      "plate": "grid",
      "accent": "cream",
      "big": "Guru, perawat, perancang.",
      "sub": [
        "efek ini belum diuji di sana"
      ],
      "key": "b9-3",
      "block": "b9",
      "from": 5201,
      "to": 5414,
      "plateFrom": 194
    },
    {
      "span": 1,
      "kind": "line",
      "plate": "columns",
      "accent": "rose",
      "big": "Apakah lebih untung?",
      "sub": [
        "itu tidak diuji"
      ],
      "key": "b9-4",
      "block": "b9",
      "from": 5414,
      "to": 5618,
      "plateFrom": 291
    },
    {
      "span": 1,
      "kind": "line",
      "plate": "wire",
      "accent": "cream",
      "kicker": "PENUTUP",
      "big": "Seleksi dan hadiah menginginkan orang yang berbeda.",
      "key": "b10-1",
      "block": "b10",
      "from": 5618,
      "to": 5753,
      "plateFrom": 0
    },
    {
      "span": 1,
      "kind": "word",
      "plate": "grid",
      "accent": "cream",
      "big": "Bukan soal adil.",
      "key": "b10-2",
      "block": "b10",
      "from": 5753,
      "to": 5852,
      "plateFrom": 97
    },
    {
      "span": 1,
      "kind": "question",
      "plate": "wire",
      "accent": "rose",
      "big": "Siapa yang sebenarnya sedang dipilih?",
      "key": "b10-3",
      "block": "b10",
      "from": 5852,
      "to": 6154,
      "plateFrom": 194
    }
  ]
} as unknown as LongProps;
