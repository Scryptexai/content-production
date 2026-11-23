"""Konfigurasi OS-EP05 — Peta Piri Reis.

VO internal perempuan voice-08; 106,88 dtk, diikuti outro 5 dtk.
Sudut bukti: dokumen 1513 nyata dan penting; klaim Antartika tanpa es tidak
menang atas inskripsi sumber dan pembacaan kartografi. Subtitle diproyeksikan
ke span bicara VAD tanpa caption lead (bukan ASR forced alignment).
"""
SLUG="piri-reis"
VO_FILE="vo_internal/vo_piri-reis.m4a"
END=111.88
OUT_NAME="OS-EP05_peta-piri-reis_feed.mp4"
SRT_NAME="OS-EP05.id.srt"
CAPTION_LEAD=0.0
CAPTION_TAIL=0.12
IMAGES={
 "SOURCE":("piri_source_document.png",1080,1920),
 "SOURCES":("piri_sources_card.png",1080,1920),
 "VERDICT":("piri_verdict_card.png",1080,1920),
 "TIMELINE":("piri_timeline_card.png",1080,1920),
}
CLIPS={
 "MAP_TOPKAPI":("map_istanbul_topkapi.mp4",0.0,6.4),
 "BOATS":("piri_boats_sailing.mp4",0.0,6.0),
 "SEA":("piri_sea_sao_vicente.mp4",0.0,6.0),
 "SUNSET":("piri_atlantic_sunset.mp4",0.0,6.0),
 "PAGES":("piri_pages_notebook.mp4",0.0,6.0),
 "READ":("piri_reading_night.mp4",0.0,6.0),
}
TAG_STOK_C="FOOTAGE STOK · COVERR · ILUSTRASI"
SHOTS=[
 (0.00,0.25,None,"black",1,1,{}),
 (0.25,5.50,"SOURCE","fill",1.00,1.06,{}),
 (5.50,10.80,"VERDICT","fill",1,1.03,{}),
 (10.80,15.40,"SOURCE","fill",1.03,1.08,{}),
 (15.40,21.80,"MAP_TOPKAPI","clip",1,1,{"raw":True}),
 (21.80,29.20,"SOURCES","fill",1,1.03,{}),
 (29.20,35.00,"PAGES","clip",1,1,{"tag":TAG_STOK_C}),
 (35.00,42.80,"SOURCE","fill",1.08,1.14,{}),
 (42.80,48.80,"BOATS","clip",1,1,{"tag":TAG_STOK_C}),
 (48.80,55.50,"VERDICT","fill",1.03,1.07,{}),
 (55.50,62.00,"SOURCE","fill",1.10,1.16,{"focusy":0.64}),
 (62.00,68.50,"TIMELINE","fill",1,1.03,{}),
 # Hasil fetch Coverr dinormalisasi tepat 6 dtk: jangan meminta frame melewati
 # sumber. Tiga klip 6 dtk berturut memberi gerak tanpa freeze/black tail.
 (68.50,74.50,"SUNSET","clip",1,1,{"tag":TAG_STOK_C}),
 (74.50,80.50,"READ","clip",1,1,{"tag":TAG_STOK_C}),
 (80.50,86.50,"SEA","clip",1,1,{"tag":TAG_STOK_C}),
 (86.50,92.00,"SOURCES","fill",1.04,1.10,{}),
 (92.00,101.20,"VERDICT","fill",1.06,1.12,{}),
 (101.20,106.88,"SOURCE","fill",1.10,1.16,{}),
 (106.88,111.88,None,"outro",1,1,{}),
]
KEYWORDS={"PIRI","REIS","ANTARTIKA","COLUMBUS","TOPKAPI","ISTANBUL","AMERIKA","SELATAN","PETA"}
NUM_PHRASES=[]
MERGE=[]
WORD_FIX={"piri":"Piri","reis":"Reis","antartika":"Antartika","columbus":"Columbus","topkapı":"Topkapı","istanbul":"Istanbul","portugis":"Portugis"}
CREDITS=("Dokumen: Piri Reis World Map, 1513 · Topkapı H 1824\\N"
 "via Wikimedia Commons · Public Domain\\N"
 "Footage stok: Coverr · Peta: © OpenStreetMap contributors · ODbL")
OVL=[
 (0.60,5.20,"Big","{\\pos(540,560)\\an5\\fs76\\fad(160,150)}BUKAN BUKTI\\NANTARTIKA."),
 (5.90,10.50,"Kicker","{\\pos(540,1030)\\an5\\fs48\\fad(180,150)}KLAIM VIRAL ≠ BACA DOKUMEN"),
 (22.30,28.80,"Kicker","{\\pos(540,1060)\\an5\\fs46\\fad(180,150)}CATATAN PIRI: KOMPILASI SUMBER"),
 (35.50,42.20,"Stamp","{\\pos(540,510)\\an5\\fs56\\frz-4\\fad(160,150)}BAGIAN YANG SERING DIPOTONG"),
 (49.50,55.00,"Kicker","{\\pos(540,1040)\\an5\\fs46\\fad(180,150)}GARIS SELATAN MENYAMBUNG AMERIKA SELATAN"),
 (62.50,68.10,"Stamp","{\\pos(540,510)\\an5\\fs58\\frz-4\\fad(160,150)}1513 ≠ SATELIT"),
 (84.50,91.50,"Kicker","{\\pos(540,1050)\\an5\\fs46\\fad(180,150)}PETA KOMPLILASI ATAU RAHASIA?"),
 (101.80,106.60,"Kicker","{\\pos(540,760)\\an5\\fs44\\fad(180,120)}PERIKSA CATATAN DI PINGGIRNYA."),
 (107.40,111.80,"Big","{\\pos(540,640)\\an5\\fs105\\fad(260,0)}ODDCHAPTER"),
 (107.70,111.80,"Credit","{\\pos(540,1000)\\an5\\fs25\\c&H00D0D0D0&\\fad(360,0)}"+CREDITS),
]
