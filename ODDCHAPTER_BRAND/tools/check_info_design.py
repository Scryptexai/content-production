"""
check_info_design.py — desain informasi ala NERROR, diperiksa mesin.

Lihat SKILLS/15_NERROR_INFO_DESIGN.md. Yang diperiksa bukan selera, melainkan
tujuh hal yang bisa dibuktikan dari teks naskah:

  A  kronologi dulu        — waktu/tempat konkret muncul di tiga beat pertama
  B  petunjuk dulu         — tidak ada kata kesimpulan sebelum beat "turn"
  C  karantina kesimpulan  — kesimpulan hanya di "turn", dan ada yang mengatakannya
  D  pertanyaan tertahan   — hook bertanya / loop bertanya, celah tidak dijawab
  E  tesis–antitesis–sintesis — turn memuat klaim, lawan klaim, dan pembacaan
  F  bukti bisa ditunjuk   — ≥3 beat memuat angka/tanggal/jarak/nominal
  G  suara penyelidik      — ≥2 sapaan, dan tidak ada tuduhan mutlak pada nama

    python3 tools/check_info_design.py             # tabel semua episode
    python3 tools/check_info_design.py EP11 -v     # satu episode, rincian
    python3 tools/check_info_design.py --strict    # keluar 1 kalau ada yang gagal
"""
import re
import sys
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from content_data import EPISODES  # noqa: E402

BULAN = r"(januari|februari|maret|april|mei|juni|juli|agustus|september|oktober|november|desember)"
KRONOLOGI = re.compile(rf"\b(1[89]|20)\d\d\b|\b{BULAN}\b", re.I)

# Kata yang mengubah laporan menjadi putusan. Kalau muncul sebelum turn,
# penonton menerima kesimpulan sebelum buktinya — persis yang dihindari NERROR.
PUTUSAN = re.compile(
    r"\b(berarti|terbukti|jelas\s+bahwa|kesimpulannya|itu\s+sebabnya|jadi\s+jelas|"
    r"sudah\s+pasti|tentu\s+saja|seharusnya|membuktikan)\b", re.I)

# Penanda ada yang bicara: atribusi. Kesimpulan tanpa atribusi = opini narator.
ATRIBUSI = re.compile(
    r"\b(bilang|kata|menurut|mengaku|menyebut|menulis|melaporkan|memutuskan|"
    r"surat|laporan|putusan|kesaksian|pengakuan)\b|[\u201c\u201d\"]", re.I)

# Penanda lawan klaim: tesis dan antitesis harus bertemu di satu beat.
LAWAN = re.compile(r"\b(tapi|tetapi|padahal|bukan|sementara|namun|sebaliknya)\b", re.I)

BUKTI = re.compile(r"\b\d[\d.,]*\b|\bRp\s?\d", re.I)

TUDUHAN = re.compile(
    r"\b(pelaku(nya)?\s+adalah|yang\s+membunuh\s+adalah|didalang(i|kan)\s+oleh|"
    r"tersangka\s+adalah)\b", re.I)

SAPA = re.compile(r"\b(kamu|kita|anda)\b", re.I)

NAMA_CEK = ("A", "B", "C", "D", "E", "F", "G")


def beats(e):
    return list(e["beats"])


def parts(e):
    return [p for p, _ in e["beats"]]


def scripts(e):
    return [e["hook"]] + [t for _, t in e["beats"]] + [e["loop"]]


def check_a(e):
    """Kronologi dulu: tiga beat pertama memuat tahun/bulan."""
    head = [t for _, t in e["beats"][:3]]
    hit = [t for t in head if KRONOLOGI.search(t)]
    if hit:
        return True, f"anchor di beat {[i + 1 for i, (_, t) in enumerate(e['beats'][:3]) if KRONOLOGI.search(t)]}"
    return False, "tiga beat pertama tanpa tahun/bulan — penonton belum tahu kapan"


def check_b(e):
    """Petunjuk dulu: tidak ada kata putusan sebelum turn."""
    bad = []
    for i, (part, t) in enumerate(e["beats"]):
        if part == "turn":
            break
        if PUTUSAN.search(t):
            bad.append(i + 1)
    if bad:
        return False, f"kata putusan di beat {bad} sebelum turn"
    return True, "tidak ada putusan sebelum turn"


def check_c(e):
    """Karantina kesimpulan: turn ada, bertribusi, dan hanya di situ kesimpulan."""
    ps = parts(e)
    if "turn" not in ps:
        return False, "tidak ada beat turn"
    turn = [t for p, t in e["beats"] if p == "turn"]
    if not ATRIBUSI.search(" ".join(turn) + " " + str(e.get("turn_quote", ""))):
        return False, "turn menyimpulkan tanpa atribusi (siapa yang bilang?)"
    after = e["beats"][ps.index("turn") + 1:]
    if any(PUTUSAN.search(t) for _, t in after):
        return False, "ada putusan baru setelah turn — kesimpulan jadi dua"
    return True, "satu kesimpulan, bertribusi, di turn"


def check_d(e):
    """Pertanyaan tertahan: hook/loop bertanya, dan celah tetap terbuka."""
    q_hook = "?" in e["hook"]
    q_loop = "?" in e["loop"]
    if not (q_hook or q_loop):
        return False, "hook dan loop sama-sama bukan pertanyaan — tidak ada kail"
    if e.get("celah"):
        return True, f"celah dipegang: {e['celah'][:48]}…"
    return True, "pertanyaan ada, tetapi field `celah` kosong"


def check_e(e):
    """Tesis–antitesis–sintesis di dalam turn."""
    turn = " ".join(t for p, t in e["beats"] if p == "turn")
    if not turn:
        return False, "turn kosong"
    if not ATRIBUSI.search(turn + " " + str(e.get("turn_quote", ""))):
        return False, "tidak ada klaim resmi (tesis) yang disebut"
    if not LAWAN.search(turn):
        return False, "tidak ada lawan klaim (antitesis) di turn"
    if not e.get("turn_verdict"):
        return False, "tidak ada pembacaan kanal (sintesis) di `turn_verdict`"
    return True, "tesis + antitesis + sintesis ada"


def check_f(e):
    """Bukti bisa ditunjuk: ≥3 beat dengan angka/tanggal/jarak/nominal."""
    hit = [i + 1 for i, (_, t) in enumerate(e["beats"]) if BUKTI.search(t)]
    if len(hit) >= 3:
        return True, f"angka di beat {hit}"
    return False, f"angka hanya di beat {hit} — kurang dari tiga"


def check_g(e):
    """Suara penyelidik, bukan hakim."""
    n = sum(len(SAPA.findall(t)) for t in scripts(e))
    if n < 2:
        return False, f"sapaan hanya {n} — penonton tidak diajak"
    bad = [t for t in scripts(e) if TUDUHAN.search(t)]
    if bad:
        return False, f"tuduhan mutlak: {bad[0][:60]}…"
    return True, f"{n} sapaan, tanpa tuduhan mutlak"


CHECKS = [check_a, check_b, check_c, check_d, check_e, check_f, check_g]


def evaluate(e):
    out = []
    for name, fn in zip(NAMA_CEK, CHECKS):
        ok, why = fn(e)
        out.append((name, ok, why))
    return out


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    verbose = "-v" in sys.argv or "--verbose" in sys.argv
    strict = "--strict" in sys.argv
    want = args[0] if args else None
    rows, failed = [], 0

    for e in EPISODES if not want else [x for x in EPISODES if x["ep"] == want]:
        res = evaluate(e)
        score = sum(1 for _, ok, _ in res if ok)
        failed += score < len(res)
        rows.append((e["ep"], score, res, e["title"]))
        if verbose:
            print(f"\n{e['ep']} · {e['title']}  {score}/{len(res)}")
            for name, ok, why in res:
                print(f"  {'✓' if ok else '✗'} {name}  {why}")

    if not verbose:
        print(f"{'ep':5s} {'skor':5s} {'gagal':28s} judul")
        for ep, score, res, title in rows:
            bad = ",".join(n for n, ok, _ in res if not ok) or "—"
            print(f"{ep:5s} {score}/{len(res)}   {bad:28s} {title[:52]}")
        total = sum(s for _, s, _, _ in rows)
        print(f"\n{len(rows)} episode · rata-rata {total / len(rows):.2f}/7 · "
              f"{failed} episode belum memenuhi semua")

    if strict and failed:
        print(f"\n::error::{failed} episode belum memenuhi desain informasi NERROR")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
