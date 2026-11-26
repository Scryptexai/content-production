#!/usr/bin/env python3
"""Build the sealed LF04 Tambora visual/timing document for Remotion.

The production deliberately uses original SVG information design rather than
stock disaster footage, archival scans with unverified reuse rights, or a
photorealistic reconstruction. Every on-screen figure remains paired with the
same named source family that supports it in LF04_tambora/SOURCES.md.

Inputs are the voice-09 WAV timing manifest and the approved LF04 manuscript
extract. Outputs are tracked SVG plates plus the LF04-specific Remotion input.
The WAV itself stays in the ignored working/public-audio location.
"""
from __future__ import annotations

import html
import json
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
BRAND = HERE.parent
REPO = BRAND.parent
WORK = REPO / "work" / "tambora" / "vo_internal"
TIMING = WORK / "LF04_Tambora_voice-09_timing.json"
OUT_JSON = BRAND / "10_FILM" / "remotion" / "src" / "longform.lf04.generated.json"
OUT_SVG = BRAND / "10_FILM" / "remotion" / "public" / "lf04"
OUT_AUDIO = BRAND / "10_FILM" / "remotion" / "public" / "audio" / "LF04" / "lf04_tambora_voice-09.wav"
VISUAL_MANIFEST = BRAND / "11_CONTENT" / "07_LONGFORM" / "LF04_tambora" / "VISUAL_PROVENANCE.md"

FPS = 30

# This is the exact TTS-safe wording used for the first two takes. It only
# adjusts wording that the speech provider refused; its fact boundaries match
# the owner-approved opening in SCRIPT.md.
OPENING = (
    "Di Doro Bente di Semenanjung Tambora, satu kotak ekskavasi memperlihatkan lima "
    "lapisan material vulkanik dari tahun 1815. Di bawahnya ada tiga lapisan lebih tua, "
    "terbentuk ketika tempat itu masih berupa laut dangkal. Di atasnya tanah berubah, "
    "bukan hanya oleh cerita lisan, melainkan oleh material yang dapat dibaca lapis demi lapis. "
    "Setahun sesudah tanggal pada lapisan itu, Eropa mencatat musim panas yang gagal datang. "
    "Dua tempat ini dipisahkan laut, bahasa, dan ribuan kilometer. Namun keduanya masuk ke satu rantai bukti. "
    "Rantai itu tidak berupa satu gambar tunggal. Tanah menyimpan urutan material. Arsip menyimpan kabar yang tidak tiba serentak. "
    "Catatan iklim menyimpan suhu dan hujan dari wilayah tertentu. Setiap bagian menjawab pertanyaan berbeda: "
    "apa yang menutup lanskap, kapan kabar dapat dipastikan, dan bagaimana perubahan iklim diuji. "
    "Cerita Tambora sering diringkas sebagai gunung di Sumbawa yang membuat dunia mendingin. "
    "Arah kalimat itu benar, tetapi terlalu pendek untuk menjelaskan dampak awal, perjalanan kabar, dan ukuran ilmiahnya. "
    "Karena itu cerita ini dimulai dari lima lapisan di Sumbawa, bukan dari langit Eropa. "
    "Apa yang dapat dibuktikan oleh lima lapisan itu, dan bagian mana yang tidak boleh diisi dengan dugaan?"
)

# Scene card labels are short and source-scoped. They are not a second script:
# the narration retains the whole claim and qualification.
SCENES = [
    # act, scene title, kicker, style, [(label, sub, source, kind), ...]
    ("LIMA LAPISAN", "Kotak B28U18", "STRATIGRAFI · BRIN 2024", "cards", [
        ("TIGA LAPISAN", "lingkungan laut lebih tua", "BRIN 2024", "layers-old"),
        ("LIMA LAPISAN", "material piroklastik · 1815", "BRIN 2024", "layers-new"),
        ("DORO BENTE", "satu situs · bukti khusus", "BRIN 2024", "grid"),
    ]),
    ("LIMA LAPISAN", "Satu rantai, tiga arsip", "CARA MEMBACA BUKTI", "cards", [
        ("TANAH", "urutan material", "BRIN 2024", "layers-new"),
        ("ARSIP", "kabar tidak serentak", "BADAN GEOLOGI 2020", "archive"),
        ("IKLIM", "suhu dan hujan setempat", "SCHURER ET AL. 2019", "chart"),
    ]),
    ("LIMA LAPISAN", "Batas kesimpulan", "PERTANYAAN PEMBUKA", "cards", [
        ("APA YANG TERTUTUP?", "lapisan dapat dibaca", "BRIN 2024", "scope"),
        ("KAPAN KABAR TIBA?", "tanggal terbit ≠ waktu bahaya", "BADAN GEOLOGI 2020", "calendar"),
        ("BAGAIMANA DIUJI?", "peluang, bukan cuaca seragam", "SCHURER ET AL. 2019", "scope"),
    ]),
    ("KABAR YANG TIBA TERLAMBAT", "April sampai Mei 1815", "REKONSTRUKSI ARSIP · BADAN GEOLOGI 2020", "timeline", [
        ("APRIL 1815", "fase letusan · VEI 7", "GVP TAMBORA", "calendar"),
        ("11 MEI", "Benares tiba di Batavia", "BADAN GEOLOGI 2020", "route"),
        ("6 · 13 · 20 · 27 MEI", "edisi Gazette bertahap", "BADAN GEOLOGI 2020", "calendar"),
    ]),
    ("KABAR YANG TIBA TERLAMBAT", "Rute informasi", "KAPAL · SURAT · SALINAN LAPORAN", "cards", [
        ("BENARES", "Makassar → Batavia", "BADAN GEOLOGI 2020", "route"),
        ("DISPATCH", "dentuman malam 11 April", "BADAN GEOLOGI 2020", "archive"),
        ("BO’ SANGAJI KAI", "rekaman Bima yang disebut", "BADAN GEOLOGI 2020", "archive"),
    ]),
    ("KABAR YANG TIBA TERLAMBAT", "Dua urutan berbeda", "JANGAN DISAMAKAN", "cards", [
        ("KEJADIAN", "bahaya di tempat tertentu", "BATAS EDITORIAL", "arrows"),
        ("LAPORAN", "kabar bergerak bertahap", "BADAN GEOLOGI 2020", "route"),
        ("TANGGAL TERBIT", "waktu pembaca menerima kabar", "BATAS EDITORIAL", "calendar"),
    ]),
    ("BENTUK YANG TERTINGGAL", "Kaldera sebagai jejak", "GVP · TAMBORA", "cards", [
        ("SEKITAR 6 KM", "lebar kaldera", "GVP TAMBORA", "caldera"),
        ("SEKITAR 1.250 M", "rim di atas lantai", "GVP TAMBORA", "caldera"),
        ("BENTUK BERUBAH", "jejak geologi, bukan drama", "GVP TAMBORA", "scope"),
    ]),
    ("BENTUK YANG TERTINGGAL", "Urutan endapan", "GVP · SUTAWIDJAJA ET AL. 2006", "cards", [
        ("SEKITAR 200 M", "unit 1815 di satu dinding", "GVP TAMBORA", "column"),
        ("≥ 4 JATUHAN TEFRA", "sebelum aliran dan surge", "SUTAWIDJAJA ET AL. 2006", "column"),
        ("URUTAN", "endapan memberi waktu & jangkauan", "GVP TAMBORA", "layers-new"),
    ]),
    ("BENTUK YANG TERTINGGAL", "Arah material", "DESKRIPSI ENDAPAN · GVP", "cards", [
        ("LERENG", "material mengikuti permukaan", "GVP TAMBORA", "arrows"),
        ("PANTAI & LAUT", "mencapai sisi Sanggar", "GVP TAMBORA", "arrows"),
        ("UDARA", "jalur bukti lain", "GVP TAMBORA", "atmosphere"),
    ]),
    ("SITUS, BUKAN KOTA REKAAN", "Nama dalam studi", "SUTAWIDJAJA ET AL. 2006", "cards", [
        ("SANGGAR", "keterangan masyarakat", "SUTAWIDJAJA ET AL. 2006", "names"),
        ("TAMBORA", "keterangan masyarakat", "SUTAWIDJAJA ET AL. 2006", "names"),
        ("PEKAT", "keterangan masyarakat", "SUTAWIDJAJA ET AL. 2006", "names"),
    ]),
    ("SITUS, BUKAN KOTA REKAAN", "Kerja lapangan", "PENELITIAN ARKEOLOGI · BRIN 2024", "timeline", [
        ("2006", "penelitian dimulai", "BRIN 2024", "calendar"),
        ("2008 → 2021", "penelitian diteruskan", "BRIN 2024", "research"),
        ("DORO BENTE", "lokasi dengan temuan khusus", "BRIN 2024", "grid"),
    ]),
    ("SITUS, BUKAN KOTA REKAAN", "Yang ditemukan", "DORO BENTE · BRIN 2024", "cards", [
        ("FRAGMEN KERAMIK", "artefak yang dilaporkan", "BRIN 2024", "artifact"),
        ("GERABAH", "artefak yang dilaporkan", "BRIN 2024", "artifact"),
        ("TULANG & CANGKANG", "material yang dilaporkan", "BRIN 2024", "artifact"),
    ]),
    ("SITUS, BUKAN KOTA REKAAN", "Kekuatan batas", "BUKTI ≠ REKONSTRUKSI", "cards", [
        ("SATU KOTAK", "bukan seluruh Sumbawa", "BRIN 2024", "boundary"),
        ("AKTIVITAS MANUSIA", "bukan kota utuh dari imajinasi", "BRIN 2024", "boundary"),
        ("TIDAK DIREKONSTRUKSI", "wajah, rute, menit terakhir", "BATAS EDITORIAL", "scope"),
    ]),
    ("JALAN KE STRATOSFER", "Mekanisme atmosfer", "SCHURER ET AL. 2019", "cards", [
        ("SO₂", "masuk ke stratosfer", "SCHURER ET AL. 2019", "atmosphere"),
        ("AEROSOL SULFAT", "terbentuk di stratosfer", "SCHURER ET AL. 2019", "particles"),
        ("RADIASI PENDEK ↓", "energi bersih ke permukaan", "SCHURER ET AL. 2019", "arrows"),
    ]),
    ("JALAN KE STRATOSFER", "Mekanisme bukan cuaca seragam", "SISTEM IKLIM", "cards", [
        ("PROSES FISIKA", "dapat bekerja lintas atmosfer", "SCHURER ET AL. 2019", "atmosphere"),
        ("SIRKULASI", "ikut menentukan pola setempat", "SCHURER ET AL. 2019", "globe"),
        ("DAMPAK TERCATAT", "tempat · musim · masyarakat", "BATAS EDITORIAL", "scope"),
    ]),
    ("JALAN KE STRATOSFER", "Konteks 1816", "WILAYAH KAJIAN · SCHURER ET AL. 2019", "cards", [
        ("EROPA TENGAH & BARAT", "musim panas 1816", "SCHURER ET AL. 2019", "globe"),
        ("DINGIN & BASAH", "anomali regional yang diuji", "SCHURER ET AL. 2019", "chart"),
        ("BUKAN LABEL GLOBAL", "tidak semua benua seragam", "BATAS EDITORIAL", "scope"),
    ]),
    ("PEMBALIKAN: BUKAN SATU TOMBOL CUACA", "Cara menguji 1816", "SCHURER ET AL. 2019", "cards", [
        ("DATA INSTRUMENTAL AWAL", "merekam anomali", "SCHURER ET AL. 2019", "research"),
        ("DUA MODEL IKLIM", "simulasi pembanding", "SCHURER ET AL. 2019", "model"),
        ("FORCING vs SIRKULASI", "dua peran dipisahkan", "SCHURER ET AL. 2019", "comparison"),
    ]),
    ("PEMBALIKAN: BUKAN SATU TOMBOL CUACA", "Apa yang bisa dijelaskan", "HASIL ATRIBUSI · SCHURER ET AL. 2019", "cards", [
        ("PRESIPITASI", "sirkulasi dapat mereproduksi pola", "SCHURER ET AL. 2019", "chart"),
        ("SEKITAR ¼", "anomali dingin yang dijelaskan", "SCHURER ET AL. 2019", "chart"),
        ("SISA PERTANYAAN", "bukan satu sebab tunggal", "SCHURER ET AL. 2019", "comparison"),
    ]),
    ("PEMBALIKAN: BUKAN SATU TOMBOL CUACA", "Peluang berubah", "HASIL ATRIBUSI · SCHURER ET AL. 2019", "cards", [
        ("HINGGA 100×", "dingin Eropa lebih mungkin", "SCHURER ET AL. 2019", "likelihood-cold"),
        ("1,5 → 3×", "kondisi basah lebih mungkin", "SCHURER ET AL. 2019", "likelihood-wet"),
        ("FORCING BESAR", "mengubah peluang dalam sistem", "SCHURER ET AL. 2019", "comparison"),
    ]),
    ("KEMBALI KE LIMA LAPISAN", "Empat mata rantai", "BUKTI YANG SALING MENGUJI", "cards", [
        ("TANAH", "lapisan 1815 di Doro Bente", "BRIN 2024", "layers-new"),
        ("ARSIP", "kabar kapal dan surat", "BADAN GEOLOGI 2020", "archive"),
        ("ATMOSFER", "mekanisme aerosol sulfat", "SCHURER ET AL. 2019", "atmosphere"),
        ("MODEL", "peluang dingin diuji", "SCHURER ET AL. 2019", "model"),
    ]),
    ("KEMBALI KE LIMA LAPISAN", "Batas di setiap mata rantai", "TIDAK MELONCAT", "cards", [
        ("SITUS", "bukti khusus, bukan seluruh pulau", "BRIN 2024", "boundary"),
        ("ARSIP", "jeda kabar, bukan jam bahaya", "BADAN GEOLOGI 2020", "calendar"),
        ("IKLIM", "peluang regional, bukan seragam", "SCHURER ET AL. 2019", "scope"),
    ]),
    ("KEMBALI KE LIMA LAPISAN", "Membaca tanpa mengisi dugaan", "PERTANYAAN PENUTUP", "cards", [
        ("LIMA LAPISAN", "titik awal yang dapat diperiksa", "BRIN 2024", "layers-new"),
        ("RANTAI BUKTI", "tanah → arsip → atmosfer → model", "MULTI-SUMBER", "chain"),
        ("APA YANG DIRINGKAS?", "bukti apa yang perlu dibaca lagi?", "ODDCHAPTER", "question"),
    ]),
]

# Mapping the narrator chunks to the same factual wording. JSON chunks 02–08
# were made straight from SCRIPT.md; only act 1 uses the content-filter-safe take.
def narration_by_act() -> dict[str, str]:
    source = json.loads((WORK / "LF04_tambora_voice_chunks.json").read_text(encoding="utf-8"))
    grouped: dict[str, list[str]] = {}
    for row in source:
        grouped.setdefault(row["act"], []).append(row["text"])
    grouped["LIMA LAPISAN"] = [OPENING]
    return {name: " ".join(parts) for name, parts in grouped.items()}


def text_parts(text: str, maximum_words: int = 8) -> list[str]:
    """Caption-sized phrases, in source order, without inventing wording."""
    words = text.replace("\n", " ").split()
    parts, current = [], []
    for word in words:
        current.append(word)
        if len(current) >= maximum_words or word.endswith((".", "?", "!", ";", ":")):
            parts.append(" ".join(current))
            current = []
    if current:
        parts.append(" ".join(current))
    return parts


def captions(text: str, start: float, end: float) -> list[dict]:
    parts = text_parts(text)
    weights = [max(1, len(p.replace(" ", ""))) for p in parts]
    total = sum(weights)
    cursor = start
    result = []
    for part, weight in zip(parts, weights):
        duration = (end - start) * weight / total
        result.append({"t0": round(cursor, 3), "t1": round(cursor + duration, 3), "text": part})
        cursor += duration
    if result:
        result[-1]["t1"] = round(end, 3)
    return result


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def svg_text(value: str, x: int, y: int, size: int, color: str = "#EDE7D6", weight: int = 700, anchor: str = "start") -> str:
    return f'<text x="{x}" y="{y}" fill="{color}" font-family="Inter,Arial,sans-serif" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">{esc(value)}</text>'


def icon(kind: str) -> str:
    orange, sage, ivory, blue = "#C46A34", "#AAB7A1", "#EDE7D6", "#607D95"
    line = 'stroke-width="12" stroke-linecap="round" stroke-linejoin="round" fill="none"'
    sage_line = f'stroke="{sage}" {line}'
    if kind.startswith("layers"):
        colors = ["#4A6471", "#5A7783", "#6B8992"] if kind == "layers-old" else ["#4E443A", "#8F5E3C", "#C46A34", "#DEC08B", "#B16D46"]
        y = 180
        rows = []
        for c in colors:
            rows.append(f'<path d="M94 {y} C230 {y-22} 470 {y+24} 665 {y-5} L665 {y+52} C460 {y+76} 230 {y+36} 94 {y+58}Z" fill="{c}" opacity="0.94"/>')
            y += 66
        return "".join(rows) + f'<line x1="94" y1="160" x2="665" y2="160" {sage_line} opacity=".38"/>'
    if kind in {"chain", "arrows"}:
        return (f'<path d="M120 326 H602" {line} stroke="{orange}"/> '
                f'<path d="M562 274 L624 326 L562 378" {line} stroke="{orange}"/> '
                + "".join(f'<circle cx="{x}" cy="326" r="48" fill="#172126" stroke="{ivory}" stroke-width="5"/>' for x in (150, 360, 570)))
    if kind in {"scope", "boundary"}:
        return (f'<rect x="115" y="178" width="530" height="300" rx="20" fill="#101619" stroke="{sage}" stroke-width="6"/> '
                f'<rect x="210" y="238" width="340" height="180" rx="12" fill="#1D2D31" stroke="{orange}" stroke-width="8"/> '
                f'<path d="M164 436 L595 210" {line} stroke="{orange}" opacity=".75"/>')
    if kind == "calendar":
        return (f'<rect x="150" y="154" width="460" height="352" rx="22" fill="#E6DDC9"/> '
                f'<rect x="150" y="154" width="460" height="85" rx="22" fill="{orange}"/> '
                + "".join(f'<line x1="{x}" y1="270" x2="{x}" y2="452" stroke="#8E806A" stroke-width="4" opacity=".7"/>' for x in (266, 382, 498))
                + "".join(f'<line x1="182" y1="{y}" x2="578" y2="{y}" stroke="#8E806A" stroke-width="4" opacity=".7"/>' for y in (315, 360, 405, 450))
                + f'<circle cx="440" cy="338" r="32" fill="none" stroke="{orange}" stroke-width="12"/>')
    if kind in {"route", "archive"}:
        return (f'<path d="M105 410 C185 242 254 476 349 310 S523 270 652 174" {line} stroke="{orange}"/> '
                + "".join(f'<circle cx="{x}" cy="{y}" r="22" fill="{orange}"/>' for x, y in ((115, 405), (354, 309), (650, 175)))
                + f'<rect x="106" y="154" width="184" height="114" rx="12" fill="#D9CBAF" transform="rotate(-8 106 154)"/> '
                + f'<line x1="130" y1="190" x2="254" y2="190" stroke="#6A5840" stroke-width="8"/>'
                + f'<line x1="130" y1="222" x2="234" y2="222" stroke="#6A5840" stroke-width="8"/>')
    if kind == "caldera":
        return (f'<ellipse cx="380" cy="318" rx="242" ry="130" fill="#1D2D31" stroke="{ivory}" stroke-width="9"/> '
                f'<ellipse cx="380" cy="318" rx="142" ry="68" fill="#071012" stroke="{orange}" stroke-width="8"/> '
                f'<path d="M104 440 H656 M154 474 H606" {sage_line} opacity=".52"/> '
                f'<path d="M132 200 L226 116 M628 200 L534 116" {line} stroke="{orange}" opacity=".8"/>')
    if kind == "column":
        colors = ["#8A6B4A", "#BF8555", "#D6B97D", "#C46A34", "#E0D3B8"]
        return "".join(f'<rect x="252" y="{150+i*66}" width="256" height="62" fill="{c}" stroke="#101619" stroke-width="5"/>' for i, c in enumerate(colors)) + f'<path d="M180 474 H570" {line} stroke="{orange}"/>'
    if kind in {"names", "research", "grid"}:
        return (f'<path d="M115 212 H645 M115 320 H645 M115 428 H645" {sage_line} opacity=".45"/> '
                f'<path d="M206 152 V488 M380 152 V488 M554 152 V488" {sage_line} opacity=".45"/> '
                f'<rect x="210" y="216" width="164" height="100" fill="#284149" stroke="{orange}" stroke-width="8"/>')
    if kind == "artifact":
        return (f'<path d="M140 442 C148 252 262 150 330 232 C402 92 574 210 608 430 Z" fill="#B68658" stroke="{ivory}" stroke-width="8"/> '
                f'<path d="M203 358 C300 298 407 388 536 286" {line} stroke="#5C412B"/> '
                f'<circle cx="426" cy="274" r="33" fill="#D6C6A5" stroke="#5C412B" stroke-width="8"/>')
    if kind in {"atmosphere", "particles"}:
        dots = "".join(f'<circle cx="{160+(i%5)*108}" cy="{226+(i//5)*66}" r="{9+(i%3)*5}" fill="{ivory}" opacity=".{4+i%5}"/>' for i in range(15))
        return (f'<path d="M330 482 C330 388 355 328 380 198" {line} stroke="{orange}"/> '
                f'<path d="M326 236 L380 160 L432 236" {line} stroke="{orange}"/> {dots} '
                f'<path d="M105 480 H655" {sage_line} opacity=".5"/>')
    if kind == "globe":
        return (f'<circle cx="380" cy="326" r="178" fill="#19313B" stroke="{ivory}" stroke-width="8"/> '
                f'<ellipse cx="380" cy="326" rx="88" ry="178" {sage_line} opacity=".7"/> '
                f'<path d="M204 326 H556 M240 258 H520 M240 394 H520" {sage_line} opacity=".7"/> '
                f'<path d="M276 228 Q380 180 480 252" {line} stroke="{orange}"/>')
    if kind in {"chart", "likelihood-cold", "likelihood-wet"}:
        vals = [110, 196, 292] if kind == "likelihood-cold" else ([120, 178, 238] if kind == "likelihood-wet" else [150, 260, 202])
        return (f'<path d="M130 470 H650 M130 470 V156" {sage_line} opacity=".65"/> '
                + "".join(f'<rect x="{178+i*148}" y="{470-v}" width="86" height="{v}" rx="8" fill="{orange if i == 2 else sage}" opacity="{.9 if i == 2 else .65}"/>' for i, v in enumerate(vals)))
    if kind in {"model", "comparison"}:
        return (f'<rect x="114" y="156" width="532" height="330" rx="16" fill="#0F171B" stroke="{sage}" stroke-width="6"/> '
                f'<path d="M156 418 L244 346 L338 382 L432 250 L548 300 L610 202" {line} stroke="{orange}"/> '
                f'<path d="M156 348 L244 308 L338 328 L432 334 L548 270 L610 292" {line} stroke="{ivory}" opacity=".75"/>')
    if kind == "question":
        return (f'<circle cx="380" cy="302" r="160" fill="#1D2D31" stroke="{orange}" stroke-width="10"/> '
                f'<path d="M322 272 C322 214 434 202 434 280 C434 326 380 334 380 382" {line} stroke="{ivory}"/> '
                f'<circle cx="380" cy="435" r="12" fill="{ivory}"/>')
    return f'<path d="M105 410 C210 180 500 520 650 190" {line} stroke="{orange}"/>'


def make_svg(label: str, sub: str, source: str, kind: str) -> str:
    # Ensure source-family attribution remains inside every independent visual
    # asset; the renderer may show a plate alone in future edits.
    lines = []
    words = label.split()
    first, second = " ".join(words[:3]), " ".join(words[3:])
    # Diagram cards are portrait in the default layout and use object-fit cover.
    # Keep important SVG text inside a 110px safe inset so it is not cropped
    # before the card's own label/source overlay appears.
    lines.append(svg_text(source.upper(), 112, 54, 17, "#C46A34", 700))
    lines.append(svg_text(first, 112, 105, 32, "#EDE7D6", 700))
    if second:
        lines.append(svg_text(second, 112, 145, 28, "#EDE7D6", 700))
    lines.append(icon(kind))
    # Credit/boundary is intentionally a source family (not an invented archival
    # locator) because specific unverified scans are not used as visual evidence.
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 640" role="img" aria-label="{esc(label)}">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#10181C"/><stop offset="1" stop-color="#071012"/></linearGradient>
    <pattern id="grid" width="42" height="42" patternUnits="userSpaceOnUse"><path d="M42 0H0V42" fill="none" stroke="#AAB7A1" stroke-opacity=".12" stroke-width="1"/></pattern>
  </defs>
  <rect width="760" height="640" fill="url(#bg)"/>
  <rect width="760" height="640" fill="url(#grid)"/>
  <path d="M0 584 C160 540 292 628 460 574 S660 540 760 570 V640 H0Z" fill="#0B0F12" opacity=".75"/>
  {''.join(lines)}
  <rect x="48" y="554" width="664" height="1" fill="#AAB7A1" opacity=".35"/>
  {svg_text(sub, 112, 594, 20, "#C9D1C2", 500)}
</svg>\n'''


def main() -> None:
    timing = json.loads(TIMING.read_text(encoding="utf-8"))
    by_act: dict[str, list[dict]] = {}
    for item in timing["chunks"]:
        by_act.setdefault(item["act"], []).append(item)
    ranges = {act: (rows[0]["start_seconds"], rows[-1]["end_seconds"]) for act, rows in by_act.items()}
    narration = narration_by_act()

    expected_acts = []
    for act, *_ in SCENES:
        if act not in expected_acts:
            expected_acts.append(act)
    missing = [act for act in expected_acts if act not in ranges or act not in narration]
    if missing:
        raise SystemExit(f"missing timing/narration for: {missing}")

    OUT_SVG.mkdir(parents=True, exist_ok=True)
    scene_counts: dict[str, int] = {}
    numbered = []
    for scene in SCENES:
        act = scene[0]
        scene_counts[act] = scene_counts.get(act, 0) + 1
        numbered.append((scene_counts[act], scene))
    totals = {act: n for act, n in scene_counts.items()}

    segments = []
    SVG_ROWS = []
    visual_number = 0
    for within_act, (act, title, kicker, style, cards) in numbered:
        visual_number += 1
        start_act, end_act = ranges[act]
        share = (end_act - start_act) / totals[act]
        start = start_act + (within_act - 1) * share
        end = end_act if within_act == totals[act] else start_act + within_act * share
        card_rows = []
        for card_no, (label, sub, source, kind) in enumerate(cards, 1):
            file_name = f"{visual_number:02d}-{card_no:02d}.svg"
            (OUT_SVG / file_name).write_text(make_svg(label, sub, source, kind), encoding="utf-8")
            card_rows.append({"plate": f"lf04/{file_name}", "label": label, "sub": sub, "num": card_no})
            SVG_ROWS.append((file_name, label, sub, source, kind))
        # Caption timing is allocated over the whole spoken act once, then
        # clipped into its visual segment. Repeating the full act in every
        # scene would make captions race and no longer match voice-09.
        full_caps = captions(narration[act], start_act, end_act)
        scene_caps = []
        for cap in full_caps:
            midpoint = (cap["t0"] + cap["t1"]) / 2
            if not (start <= midpoint < end):
                continue
            clipped_start, clipped_end = max(start, cap["t0"]), min(end, cap["t1"])
            if clipped_end - clipped_start >= 0.24:
                scene_caps.append({"t0": round(clipped_start, 3), "t1": round(clipped_end, 3), "text": cap["text"]})
        segments.append({
            "i": visual_number - 1,
            "chapter": f"BABAK {expected_acts.index(act) + 1} · {act}",
            "start": round(start, 3), "end": round(end, 3),
            "startFrame": round(start * FPS), "endFrame": round(end * FPS),
            "layout": "diagram",
            "captions": scene_caps,
            "diagram": {"style": style, "title": title, "kicker": kicker, "cards": card_rows},
        })

    total = timing["total_duration_seconds"]
    payload = {
        "id": "LF04-TAMBORA-1815",
        "series": "KASUS NYATA",
        "title": "Tambora 1815: Lima Lapisan Abu dan Tahun Tanpa Musim Panas",
        "vo": "audio/LF04/lf04_tambora_voice-09.wav",
        "fps": FPS,
        "duration": total,
        "totalFrames": round(total * FPS),
        "width": 1920,
        "height": 1080,
        "cards": [],
        "segments": segments,
        "source_boundary": "Original diagrams only; no disaster reconstruction, victim imagery, or unlicensed archival/photographic asset.",
    }
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # Audio is a run-time production input and intentionally ignored by Git.
    source_audio = WORK / "LF04_Tambora_voice-09_contiguous.wav"
    OUT_AUDIO.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source_audio, OUT_AUDIO)

    table = "\n".join(f"| `{file}` | {label} | {sub} | {source} | original SVG · {kind} |" for file, label, sub, source, kind in SVG_ROWS)
    VISUAL_MANIFEST.write_text(
        "# LF04 · provenance visual dan timing\n\n"
        "**Status:** aset produksi dibuat sebagai diagram SVG original; tidak memakai foto, footage, scan arsip, korban, atau rekonstruksi fotorealistik. "
        "Setiap plate merujuk ke keluarga sumber yang sama dengan `SOURCES.md`.\n\n"
        "## Audio\n\n"
        f"- Narator: `voice-09`, Indonesian feminine, disintesis dalam delapan proses berurutan (pembuka dibagi menjadi dua karena filter penyedia).\n"
        f"- Berkas kontigu: `work/tambora/vo_internal/LF04_Tambora_voice-09_contiguous.wav`\n"
        f"- Durasi suara: **{total:.3f} detik** / **{total / 60:.2f} menit**, tanpa time stretch.\n"
        f"- SHA-256 voice kontigu: `{timing['sha256']}`.\n"
        "- Dua bagian pembuka memakai parafrasa TTS-minimal yang menjaga arti naskah: “satu kotak ekskavasi” menggantikan “sebuah kotak”, dan struktur kalimat disederhanakan agar lolos filter. Tidak ada klaim, angka, atau batas editorial baru.\n\n"
        "## Visual\n\n"
        "- Renderer: `@remotion/renderer`; semua visual utama adalah SVG hasil desain internal di `10_FILM/remotion/public/lf04/`.\n"
        "- Peta/koneksi adalah skema konseptual, bukan peta navigasi dan bukan jalur fisik material.\n"
        "- Source labels menyatakan **keluarga sumber**, bukan menyamar sebagai halaman arsip primer yang tidak digunakan sebagai aset.\n"
        "- Tidak ada angka korban tunggal, tidak ada “kota beku”, dan tidak ada visual pengalaman korban.\n\n"
        "| plate | label | sublabel | keluarga sumber | provenance |\n"
        "|---|---|---|---|---|\n" + table + "\n\n"
        "## Dokumen render\n\n"
        "- Input komposisi: `10_FILM/remotion/src/longform.lf04.generated.json`\n"
        "- ID komposisi: `ODDCHAPTER-LONGFORM-LF04-TAMBORA`\n"
        "- Pengaturan: 1920×1080, 30 fps; 22 scene diagram; caption bersumber dari teks yang disintesis.\n",
        encoding="utf-8",
    )
    print(f"wrote {OUT_JSON.relative_to(REPO)}")
    print(f"wrote {len(SVG_ROWS)} original SVG plates in {OUT_SVG.relative_to(REPO)}")
    print(f"copied runtime audio to {OUT_AUDIO.relative_to(REPO)}")
    print(f"duration: {total:.3f}s / {round(total * FPS)} frames")


if __name__ == "__main__":
    main()
