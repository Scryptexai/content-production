"""Konfigurasi kasus AK-EP03 — Dyatlov Pass 1959 (POV tim pencari Slobtsov & Sharavin).

Sumber naskah/shotlist: Drive `naskah.md`, `shotlist.md`, `fakta.md`, `footage_index.md`.
Aturan: tanpa gore, tanpa teori konspirasi, klaim satu-sumber (Slobtsov) selalu
diberi atribusi "kata Slobtsov". Footage hanya stok Mixkit (bukan arsip) —
di layar diberi label FOOTAGE STOK dan dikreditkan di kartu akhir + deskripsi.
"""

SLUG = "dyatlov-pass"
VO_FILE = "vo_dyatlov-pass.mp3"
END = 101.60
OUT_NAME = "AK-EP03_dyatlov-pass_short_v1.mp4"
SRT_NAME = "AK-EP03.id.srt"
BED_BUILDER = "bed_dyatlov.py"
CLIP_BG_BRIGHT = "-0.34"   # latar blur footage: lebih terang dari EP02 supaya tidak terbaca letterbox

IMAGES = {
    "A": ("01_tenda_ditemukan_1959.jpg", 809, 640),      # tenda di lereng, 1959 (PD)
    "B": ("02_foto_anggota_tur_dyatlov.jpg", 1280, 960),  # memorial sembilan foto (PD, D. Nikishin)
    "C": ("03_monumen_dyatlov_mikhailovskoe.jpg", 1280, 960),  # monumen Mikhailovskoe (PD)
    "D": ("04_peta_gunung_dan_tenda.jpg", 1135, 601),    # peta Kholat-Sayakhl (CC BY-SA 4.0), bingkai hitam dipangkas
    "E": ("05_peta_lereng.jpg", 1133, 816),              # peta lereng + titik tenda (CC BY-SA 4.0)
    "F": ("06_peta_sverdlovsk.jpg", 1280, 1492),         # peta Oblast Sverdlovsk (PD)
}

# Footage kasus (work/dyatlov-pass/footage/): (berkas, detik mulai, durasi tersedia)
CLIPS = {
    "SNOW1": ("m_snowpine_3352.mp4", 0.40, 30.0),     # salju turun di hutan pinus (vertikal)
    "SNOW2": ("m_snowpine_3352.mp4", 4.20, 30.0),
    "SNOW3": ("m_snowpine_3352.mp4", 6.60, 30.0),
    "MIST1": ("m_mist_3308.mp4", 0.30, 30.0),         # kabut di kaki gunung bersalju (vertikal)
    "MIST2": ("m_mist_3308.mp4", 4.60, 30.0),
    "FOG1": ("m_fog_4396.mp4", 0.80, 30.0),           # kabut di puncak (16:9)
    "FOG2": ("m_fog_4396.mp4", 9.20, 30.0),
    "SUMMIT1": ("m_summit_3335.mp4", 0.60, 30.0),     # dua sosok berjalan di puncak (16:9)
    "SNOWFOG1": ("m_snowfog_35040.mp4", 1.00, 30.0),  # salju di hutan berkabut (16:9)
    "SNOWFOG2": ("m_snowfog_35040.mp4", 8.00, 30.0),
    "SNOWFOG3": ("m_snowfog_35040.mp4", 14.00, 30.0),
    "FIRE1": ("m_campfire_47311.mp4", 0.70, 30.0),    # api unggun + tenda malam (16:9)
    "FIRE2": ("m_campfire_47311.mp4", 4.60, 30.0),
    "FIRE3": ("m_campfire_47311.mp4", 8.70, 30.0),
    "FIRE4": ("m_campfire_47311.mp4", 11.20, 30.0),
    "MIST3": ("m_mist_3308.mp4", 6.00, 30.0),
    "RADIO1": ("m_radio_48533.mp4", 0.60, 30.0),      # dial radio analog (16:9)
    "MOON1": ("m_moon_3350.mp4", 0.50, 30.0),         # bulan di atas hutan salju (16:9)
    "MOON2": ("m_moon_3350.mp4", 4.50, 30.0),
}

TAG_FOTO = "FOTO ARSIP 1959 · DOMAIN PUBLIK"
TAG_PD = "FOTO: DMITRIY NIKISHIN · DOMAIN PUBLIK"
TAG_PETA = "PETA: WIKIMEDIA COMMONS · CC BY-SA 4.0"
TAG_STOK = "FOOTAGE STOK · MIXKIT FREE LICENSE"

BOX = {"box": (1010, 568)}          # jendela 16:9 untuk footage horizontal
NIGHT = {"box": (1010, 568), "bg": "-0.62"}   # klip malam: latar lebih gelap

# (mulai, selesai, gambar/klip, mode, zoom awal, zoom akhir, opsi)
SHOTS = [
    (0.00,   1.20, None, "black", 1.00, 1.00, {}),
    (1.20,   4.60, "A", "canvas", 1.00, 1.08, {"tag": TAG_FOTO, "focusx": 0.56}),
    (4.60,   7.90, "SNOW1", "clipfill", 1.00, 1.00, {"tag": TAG_STOK}),
    (7.90,   9.35, "A", "card", 1.10, 1.00, {"focusx": 0.56}),
    (9.35,  13.30, "MIST1", "clipfill", 1.00, 1.00, {"tag": TAG_STOK}),
    (13.30, 17.40, "FOG1", "clip", 1.00, 1.00, {"tag": TAG_STOK, **BOX}),
    (17.40, 21.30, "D", "canvas", 1.00, 1.10, {"tag": TAG_PETA}),
    (21.30, 25.20, "SUMMIT1", "clip", 1.00, 1.00, {"tag": TAG_STOK, **BOX}),
    (25.20, 28.13, "E", "card", 1.00, 1.08, {"tag": TAG_PETA}),
    (28.13, 32.20, "A", "canvas", 1.32, 1.48, {"tag": TAG_FOTO, "focusx": 0.58}),
    (32.20, 35.63, "SNOWFOG1", "clipfill", 1.00, 1.00, {"tag": TAG_STOK}),
    (35.63, 38.90, "A", "canvas", 1.06, 1.16, {"focusx": 0.58}),
    (38.90, 42.29, "SNOWFOG2", "clip", 1.00, 1.00, {"tag": TAG_STOK, **BOX}),
    (42.29, 45.75, "A", "card", 1.16, 1.02, {"focusx": 0.56}),
    (45.75, 48.90, "FIRE1", "clip", 1.00, 1.00, {"tag": TAG_STOK, **NIGHT}),
    (48.90, 51.67, "SNOW2", "clipfill", 1.00, 1.00, {"tag": TAG_STOK}),
    (51.67, 56.60, "SNOWFOG3", "clip", 1.00, 1.00, {"tag": TAG_STOK, **BOX}),
    (56.60, 59.65, "MIST2", "clipfill", 1.00, 1.00, {"tag": TAG_STOK}),
    (59.65, 63.50, "FIRE2", "clip", 1.00, 1.00, {"tag": TAG_STOK, **NIGHT}),
    (63.50, 68.27, "FIRE3", "clip", 1.00, 1.00, {"tag": TAG_STOK, **NIGHT}),
    (68.27, 71.10, "FIRE4", "clip", 1.00, 1.00, {"tag": TAG_STOK, **NIGHT}),
    (71.10, 75.01, "MIST3", "clipfill", 1.00, 1.00, {"tag": TAG_STOK}),
    (75.01, 78.00, "MOON1", "clip", 1.00, 1.00, {"tag": TAG_STOK, **NIGHT}),
    (78.00, 81.39, "B", "canvas", 1.00, 1.08, {"tag": TAG_PD}),
    (81.39, 85.50, "RADIO1", "clip", 1.00, 1.00, {"tag": TAG_STOK, **BOX}),
    (85.50, 88.70, "SNOW3", "clipfill", 1.00, 1.00, {"tag": TAG_STOK}),
    (88.70, 91.46, "FOG2", "clipfill", 1.00, 1.00, {"tag": TAG_STOK}),
    (91.46, 94.47, "F", "card", 1.00, 1.08, {"tag": "PETA: WIKIMEDIA COMMONS · DOMAIN PUBLIK"}),
    (94.47, 96.90, "MOON2", "clip", 1.00, 1.00, {"tag": TAG_STOK, **NIGHT}),
    (96.90, 99.80, "C", "canvas", 1.00, 1.10, {"tag": "MONUMEN: DMITRIY NIKISHIN · DOMAIN PUBLIK"}),
    (99.80, 100.90, "C", "card", 1.10, 1.00, {}),
    (100.90, 101.60, None, "black", 1.00, 1.00, {}),
]

KEYWORDS = {"TENDA", "DYATLOV", "SLOBTSOV", "SHARAVIN", "1959"}

MERGE = [
    (["orang", "-orang"], "ORANG-ORANG"),
]

WORD_FIX = {
    "tropong": "teropong",
    "siapapun": "siapa pun",
}

CREDITS = ("Foto: arsip 1959 (PD) · Dmitriy Nikishin (PD) · Wikimedia Commons\\N"
           "Peta: Wikimedia Commons · CC BY-SA 4.0\\N"
           "Footage stok: Mixkit Free License\\N"
           "Sumber: Slobtsov (EX no.46, 2007) · dyatlovpass.com · Wikipedia")

OVL = [
    # ── hook
    (1.30, 4.55, "Kicker", "{\\pos(540,700)\\an5\\fs58\\fad(260,180)}DYATLOV PASS"),
    # ── tanggal penemuan tenda
    (9.55, 12.60, "Stamp", "{\\pos(540,520)\\an5\\fs104\\frz-5\\fad(160,150)}26 · 02 · 1959"),
    (9.90, 12.60, "Kicker", "{\\pos(540,660)\\an5\\fs52\\fad(240,150)}PEGUNUNGAN URAL"),
    # ── tim pencari
    (18.60, 21.20, "Kicker", "{\pos(540,1015)\an5\fs62\fad(220,160)}TIM PENCARI MAHASISWA"),
    (22.40, 25.10, "Kicker", "{\\pos(540,900)\\an5\\fs48\\fad(220,160)}BORIS SLOBTSOV · MIKHAIL SHARAVIN"),
    (25.45, 28.00, "Stamp", "{\\pos(540,520)\\an5\\fs76\\frz-4\\fad(160,140)}SEMBILAN PENDAKI"),
    # ── tenda
    (32.45, 35.45, "Big", "{\\pos(540,620)\\an5\\fs210\\c&H002A2AD8&\\fad(200,160)}TENDA ITU"),
    (40.95, 42.15, "Big", "{\\pos(540,600)\\an5\\fs200\\c&H002A2AD8&\\fad(140,120)}KOSONG"),
    # ── jaket & uang
    (45.95, 48.70, "Kicker", "{\\pos(540,560)\\an5\\fs72\\fad(200,150)}UANGNYA MASIH ADA"),
    # ── parit
    (56.95, 59.50, "Kicker", "{\\pos(540,560)\\an5\\fs60\\fad(220,160)}MEREKA MENGIRA SELAMAT"),
    # ── minum di tenda
    (65.20, 68.10, "Kicker", "{\\pos(540,560)\\an5\\fs62\\fad(220,150)}UNTUK KESEHATAN MEREKA"),
    # ── usul minum untuk arwah
    (72.95, 74.90, "Kicker", "{\\pos(540,900)\\an5\\fs54\\fad(180,140)}MEREKA YAKIN MASIH HIDUP"),
    # ── sebulan kemudian
    (75.35, 77.90, "Stamp", "{\\pos(540,520)\\an5\\fs70\\frz-4\\fad(160,140)}SEBULAN KEMUDIAN"),
    # ── radio
    (83.25, 85.30, "Kicker", "{\\pos(540,560)\\an5\\fs60\\fad(200,140)}RADIO: TENDA DITEMUKAN"),
    # ── semua tim pindah
    (91.65, 94.30, "Kicker", "{\\pos(540,560)\\an5\\fs56\\fad(200,150)}SEMUA TIM PINDAH KE LERENG ITU"),
    # ── penutup
    (97.10, 99.65, "Kicker", "{\\pos(540,860)\\an5\\fs48\\c&H00E0ECF0&\\fad(240,140)}@oddchapter7"),
    (99.30, 101.55, "Big", "{\\pos(540,660)\\an5\\fs110\\fad(260,0)}ODDCHAPTER"),
    (99.60, 101.55, "Kicker", "{\\pos(540,760)\\an5\\fs42\\c&H002A2AD8&\\fad(300,0)}KASUS NYATA · ARSIP ASLI"),
    (99.90, 101.55, "Credit", "{\\pos(540,980)\\an5\\fs26\\c&H00D0D0D0&\\fad(360,0)}" + CREDITS),
]
