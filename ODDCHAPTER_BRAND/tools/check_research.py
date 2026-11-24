"""
check_research.py — memastikan naskah benar-benar memakai hasil riset.

Keluhan pemilik 16 Nov 2026: "hampir 90% mungkin tidak ada knowledge dari hasil
research yg di masukan … semua nya hanya sampai diskusi tapi tidak di pakai pada
produksi naskah".

Gerbang ini menjawabnya secara mekanis:

  1. SETIAP baris VO (hook, tiap beat, loop) wajib memuat minimal satu **token
     fakta** yang ada di `02_SCRIPT/riset/EPxx_*.md` — angka, tanggal, nama
     diri, atau kutipan dari dokumen. Baris yang hanya berisi perasaan atau
     rangkuman tidak dihitung.
  2. PERTANYAAN PENUTUP wajib punya **dua pilihan** ("… atau …"), bukan
     pertanyaan kabur seperti "kamu pindah?". Penonton harus tahu apa yang
     bisa ia jawab.
  3. KALIMAT GENERIK dilarang: frasa yang bisa dipakai di episode mana pun
     tanpa membaca satu dokumen pun.

Jalankan:
    python3 tools/check_research.py            # episode yang sudah terdaftar
    python3 tools/check_research.py EP11 -v
"""
import json
import re
import sys
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
from content_data import AK_EPISODES, EPISODES  # noqa: E402

RISET = ROOT / "11_CONTENT" / "02_SCRIPT" / "riset"
GATE = RISET / "_GATE.json"

# frasa yang bisa dipakai di episode apa pun: tanda naskah belum membaca dokumen
GENERIK = [
    "coba bayangkan", "kita mengira", "kita percaya", "sampai hari ini",
    "di seluruh dunia", "tidak ada yang bisa", "yang paling mengejutkan",
    "dan itu yang membuat", "banyak orang percaya", "hingga kini",
    "sampai sekarang", "sampai detik ini", "tidak seorang pun tahu",
    "masih menjadi misteri", "belum ada jawaban",
]

# kata yang muncul di awal kalimat dan bukan nama diri
BUKAN_NAMA = {
    "sejak", "setelah", "sebelum", "tetapi", "tapi", "lalu", "kalau", "ketika",
    "dari", "pada", "dalam", "untuk", "dengan", "yang", "ini", "itu", "dia",
    "kita", "kamu", "mereka", "cuma", "hanya", "semua", "empat", "lima",
    "dua", "tiga", "satu", "enam", "tujuh", "delapan", "sembilan", "sepuluh",
    "perhatikan", "panggilan", "laporan", "rekaman", "pilot", "pesawat",
    "jam", "hari", "tidak", "ada", "jadi", "dan", "atau", "bukan",
}

NUM = re.compile(r"\b\d[\d.,]*\b")
# Nama diri dan singkatan lembaga (misalnya KNKT) sama-sama dapat menjadi token
# fakta. Tanpa kelompok huruf kapital, baris yang sah tentang lembaga sumber akan
# salah terbaca sebagai generik.
NAMA = re.compile(r"\b([A-Z]{2,}|[A-Z][a-zA-Z'’\-]{2,})\b")


def facts(ep_id):
    """Token fakta dari berkas riset: angka dan nama diri."""
    files = sorted(RISET.glob(f"{ep_id}_*.md"))
    if not files:
        return None, []
    text = "\n".join(f.read_text() for f in files)
    nums = set(m.group(0) for m in NUM.finditer(text))
    nama = set()
    for m in NAMA.finditer(text):
        w = m.group(1)
        if w.lower() in BUKAN_NAMA:
            continue
        nama.add(w.lower())
    return files, sorted(nums), sorted(nama)


def lines_of(e):
    out = [("hook", e["hook"])]
    for i, (part, txt) in enumerate(e["beats"]):
        out.append((f"beat {i + 1} ({part})", txt))
    out.append(("loop", e["loop"]))
    return out


def check(e, verbose=False):
    files, nums, nama = facts(e["ep"])
    if files is None:
        return None  # tidak ada riset: dilewati, bukan lulus
    fails, notes, rows = [], [], []
    for name, txt in lines_of(e):
        low = txt.lower()
        hit_num = [n for n in nums if n in txt]
        hit_nama = [w for w in nama if w in low]
        ok = bool(hit_num or hit_nama)
        rows.append((name, ok, (hit_num + hit_nama)[:3], txt))
        if not ok:
            fails.append(f"(riset) {name}: tidak ada satu pun fakta dari {files[0].name} — "
                         f"'{txt[:56]}…'")

    for name, txt in lines_of(e):
        for g in GENERIK:
            if g in txt.lower():
                fails.append(f"(generik) {name}: frasa '{g}' bisa dipakai di episode apa pun")

    loop = e["loop"].strip()
    if loop.endswith("?"):
        if " atau " not in loop.lower():
            fails.append("(tanya) loop berupa pertanyaan tanpa dua pilihan — "
                         f"'{loop}' — pakai '… atau …' / '… gak?' supaya penonton tahu harus menjawab apa")
    else:
        fails.append("(tanya) loop bukan pertanyaan — tidak ada yang bisa dikomentari")

    if verbose:
        print(f"  riset: {files[0].name} · {len(nums)} angka · {len(nama)} nama")
        for name, ok, hit, txt in rows:
            print(f"   {'✓' if ok else '✗'} {name:22s} {','.join(hit) or '—':24s} {txt[:52]}")
    return fails, notes


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    verbose = "-v" in sys.argv or "--verbose" in sys.argv
    gate = json.loads(GATE.read_text()) if GATE.exists() else {}
    want = args or [k for k, v in gate.items() if v]
    nfail, nskip, rows = 0, 0, []
    for e in EPISODES + AK_EPISODES:
        if e["ep"] not in want:
            continue
        res = check(e, verbose)
        if res is None:
            nskip += 1
            print(f"{e['ep']}  LEWAT  (tidak ada berkas riset)")
            continue
        fails, _ = res
        nfail += len(fails)
        status = "LULUS" if not fails else "GAGAL"
        rows.append((e["ep"], status, len(fails)))
        if not verbose:
            print(f"{e['ep']}  {status}  {e['title'][:48]}")
        for f in fails:
            print(f"    ✗ {f}")
    print(f"\n{len(rows)} episode diperiksa · {nfail} masalah")
    return 0 if nfail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
