import type { LongProps } from "./LongForm";

export const LONG: LongProps = {
  "id": "RW1L",
  "tone": "ink",
  "chapter": "01 / KERJA",
  "source": "Benson, Li & Shue — Promotions and the Peter Principle, QJE 134(4), 2019",
  "preview": false,
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
      "vo": "RW1L-b1.mp3",
      "from": 24,
      "to": 668
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
      "vo": "RW1L-b2.mp3",
      "from": 682,
      "to": 1201
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
      "vo": "RW1L-b3.mp3",
      "from": 1215,
      "to": 1811
    },
    {
      "key": "b4",
      "scene": "kurva",
      "kicker": "SETELAH PROMOSI",
      "headline": "Yang terbaik saat menjual, terburuk saat memimpin tim.",
      "labelA": "penjualan sebelum promosi",
      "labelB": "penjualan tim sesudahnya",
      "value": "−7,5%",
      "vo": "RW1L-b4.mp3",
      "from": 1825,
      "to": 2363
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
      "vo": "RW1L-b5.mp3",
      "from": 2377,
      "to": 2915
    },
    {
      "key": "b6",
      "scene": "kontrafaktual",
      "kicker": "SATU SKENARIO YANG DIHITUNG PENULIS",
      "headline": "Kalau memilih dengan benar.",
      "value": "+30%",
      "note": "bukan lebih banyak promosi — kualitas manajernya",
      "vo": "RW1L-b6.mp3",
      "from": 2929,
      "to": 3487
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
      "vo": "RW1L-b7.mp3",
      "from": 3500,
      "to": 4240
    },
    {
      "key": "b8",
      "scene": "kutipan",
      "kicker": "BUKAN GAGASAN BARU",
      "quote": "Setiap karyawan cenderung naik ke tingkat ketidakmampuannya.",
      "attrib": "Laurence J. Peter, 1969 — ditulis sebagai satire",
      "vo": "RW1L-b8.mp3",
      "from": 4253,
      "to": 4916
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
      "vo": "RW1L-b9.mp3",
      "from": 4930,
      "to": 5612
    },
    {
      "key": "b10",
      "scene": "tanya",
      "kicker": "PENUTUP",
      "question": "Kalau promosi di tempatmu ternyata bekerja sebagai hadiah — siapa yang sebenarnya sedang dipilih?",
      "vo": "RW1L-b10.mp3",
      "from": 5626,
      "to": 6097
    }
  ]
} as unknown as LongProps;
