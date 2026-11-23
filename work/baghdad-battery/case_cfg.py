"""Konfigurasi OS-EP06 — Baghdad Battery.

VO internal perempuan voice-08; 103,52 dtk, diikuti outro 5 dtk.
Sudut bukti: replika elektrokimia dapat bekerja, tetapi fungsi artefak asli
belum terbukti. Diagram sumber ialah skema modern CC BY-SA 2.5, bukan foto.
Subtitle diproyeksikan ke span bicara VAD tanpa caption lead.
"""
SLUG="baghdad-battery"
VO_FILE="vo_internal/vo_baghdad-battery.m4a"
END=108.52
OUT_NAME="OS-EP06_baghdad-battery_feed.mp4"
SRT_NAME="OS-EP06.id.srt"
CAPTION_LEAD=0.0
CAPTION_TAIL=0.12
IMAGES={
 "SOURCE":("baghdad_diagram_source.png",1080,1920),
 "PARTS":("baghdad_parts_card.png",1080,1920),
 "VERDICT":("baghdad_verdict_card.png",1080,1920),
 "EVIDENCE":("baghdad_evidence_card.png",1080,1920),
 "KOENIG":("baghdad_koenig_card.png",1080,1920),
}
CLIPS={
 "MAP_KHUJUT":("map_khujut_rabu.mp4",0.0,6.4),
 "POTTERY":("baghdad_pottery.mp4",0.0,6.0),
 "WRITE":("baghdad_writing_notebook.mp4",0.0,6.0),
 "OLDWRITE":("baghdad_oldman_writing.mp4",0.0,6.0),
 "ELDER":("baghdad_elder_writing.mp4",0.0,6.0),
 "COFFEE":("baghdad_writing_coffee.mp4",0.0,6.0),
}
TAG_STOK_C="FOOTAGE STOK · COVERR · ILUSTRASI"
SHOTS=[
 (0.00,0.24,None,"black",1,1,{}),
 (0.24,5.90,"SOURCE","fill",1,1.05,{}),
 (5.90,10.30,"VERDICT","fill",1,1.03,{}),
 (10.30,15.60,"PARTS","fill",1,1.04,{}),
 (15.60,22.00,"MAP_KHUJUT","clip",1,1,{"raw":True}),
 (22.00,26.60,"SOURCE","fill",1.03,1.08,{}),
 (26.60,31.50,"KOENIG","fill",1,1.03,{}),
 # Semua pull Coverr diseragamkan 6 dtk. Kartu bukti menyerap sisa durasi
 # agar kita tidak mengulang/membekukan frame setelah file sumber berakhir.
 (31.50,37.50,"POTTERY","clip",1,1,{"tag":TAG_STOK_C}),
 (37.50,47.00,"VERDICT","fill",1.03,1.08,{}),
 (47.00,53.00,"WRITE","clip",1,1,{"tag":TAG_STOK_C}),
 (53.00,62.20,"EVIDENCE","fill",1,1.04,{}),
 (62.20,68.20,"OLDWRITE","clip",1,1,{"tag":TAG_STOK_C}),
 (68.20,76.20,"SOURCE","fill",1.05,1.10,{}),
 (76.20,82.20,"ELDER","clip",1,1,{"tag":TAG_STOK_C}),
 (82.20,92.20,"VERDICT","fill",1.05,1.11,{}),
 (92.20,98.00,"COFFEE","clip",1,1,{"tag":TAG_STOK_C}),
 (98.00,103.52,"EVIDENCE","fill",1.04,1.10,{}),
 (103.52,108.52,None,"outro",1,1,{}),
]
KEYWORDS={"BAGHDAD","BATERAI","KABEL","TEMBAGA","BESI","KÖNIG","KHUJUT","RABU","REPLIKA","ARKEOLOGI"}
NUM_PHRASES=[]
MERGE=[]
WORD_FIX={"baghdad":"Baghdad","khujut":"Khujut","rabu":"Rabu","wilhelm":"Wilhelm","könig":"König","tembaga":"Tembaga","arkeologi":"Arkeologi"}
CREDITS=("Skema: Ironie, Pile Bagdad · Wikimedia Commons · CC BY-SA 2.5\\N"
 "Skema modern, bukan foto artefak · Footage stok: Coverr\\N"
 "Peta: © OpenStreetMap contributors · ODbL")
OVL=[
 (0.60,5.60,"Big","{\\pos(540,560)\\an5\\fs76\\fad(160,150)}KABELNYA\\NDI MANA?"),
 (6.20,10.00,"Kicker","{\\pos(540,1040)\\an5\\fs48\\fad(180,150)}REPLIKA BISA ≠ FUNGSI ASLI TERBUKTI"),
 (10.80,15.30,"Stamp","{\\pos(540,510)\\an5\\fs56\\frz-4\\fad(160,150)}KERAMIK · TEMBAGA · BESI"),
 (22.40,26.20,"Kicker","{\\pos(540,1040)\\an5\\fs44\\fad(180,150)}SKEMA MODERN · BUKAN FOTO ARTEFAK"),
 (26.90,31.20,"Stamp","{\\pos(540,510)\\an5\\fs56\\frz-4\\fad(160,150)}1938 · HIPOTESIS KÖNIG"),
 (39.50,46.60,"Kicker","{\\pos(540,1040)\\an5\\fs46\\fad(180,150)}ELEKTROLIT DITAMBAHKAN KE REPLIKA"),
 (54.70,61.80,"Stamp","{\\pos(540,510)\\an5\\fs50\\frz-4\\fad(160,150)}JEJAK PEMAKAIAN?"),
 (69.90,75.80,"Kicker","{\\pos(540,1050)\\an5\\fs44\\fad(180,150)}WADAH GULUNGAN ATAU RITUAL JUGA MUNGKIN"),
 (84.50,91.60,"Kicker","{\\pos(540,1050)\\an5\\fs44\\fad(180,150)}KEMUNGKINAN RANGKAIAN ≠ BUKTI PEMAKAIAN"),
 (98.40,103.20,"Kicker","{\\pos(540,760)\\an5\\fs42\\fad(180,120)}EKSPERIMEN BUKAN MESIN WAKTU."),
 (104.00,108.40,"Big","{\\pos(540,640)\\an5\\fs105\\fad(260,0)}ODDCHAPTER"),
 (104.30,108.40,"Credit","{\\pos(540,1000)\\an5\\fs25\\c&H00D0D0D0&\\fad(360,0)}"+CREDITS),
]
