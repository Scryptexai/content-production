"""
check_story.py — gerbang lima efek (lihat 11_CONTENT/00C_MESIN_5_EFEK.md).

Bukan pemeriksa selera. Yang dicek adalah hal-hal yang bisa dibuktikan secara
mekanis dan, kalau gagal, hampir pasti merusak salah satu dari lima efek.

    python3 tools/check_story.py          # semua episode
    python3 tools/check_story.py EP01     # satu episode
"""
import re
import sys
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from content_data import EPISODES  # noqa: E402

# kata yang "meminta" perhatian alih-alih menunjukkan sesuatu
BANNED = {"misteri", "rahasia", "aneh", "menakjubkan", "mengerikan", "terpecahkan", "misterius"}
STOP = {"yang", "dan", "itu", "ini", "dengan", "untuk", "dari", "tidak", "tapi",
        "mereka", "dalam", "pada", "adalah", "lebih", "akan", "sudah", "hanya",
        "masih", "kembali", "sendiri", "begitu", "sekarang", "memang", "tetapi",
        "sampai", "setelah", "sebelum", "karena", "kalau", "harus", "bisa", "orang",
        "tahun", "banyak", "semua", "juga", "atau", "punya", "pernah"}


def words(t):
    return [w for w in re.findall(r"[A-Za-zÀ-ÿ0-9']+", t.lower())]


def echo(a, b):
    """Kata bermakna yang dipakai di hook dan dipanggil lagi di penutup."""
    ka = {w for w in words(a) if len(w) > 4 and w not in STOP}
    kb = {w for w in words(b) if len(w) > 4 and w not in STOP}
    return sorted(ka & kb)


def turn_numbers(e):
    """Angka/nama yang muncul pertama kali di turn = fakta baru = twist murah."""
    before = " ".join(t for part, t in e["beats"] if part != "turn") + " " + e["hook"]
    turn = " ".join(t for part, t in e["beats"] if part == "turn")
    nums_turn = set(re.findall(r"\b\d[\d.,]*\b", turn))
    nums_before = set(re.findall(r"\b\d[\d.,]*\b", before))
    return sorted(nums_turn - nums_before)


def check(e):
    fails, notes = [], []

    # 1 · berhenti scroll
    n_hook = len(e["hook"].split())
    if n_hook > 14:
        fails.append(f"(1) hook {n_hook} kata, batas 14")
    bad = [w for w in words(e["hook"]) if w in BANNED]
    if bad:
        fails.append(f"(1) hook memakai kata yang meminta, bukan menunjukkan: {', '.join(bad)}")
    if not re.search(r"\d|\b(lampu|tenda|jejak|masker|kertas|pintu|kunci|label|salju|kuas|danau|pohon)\b", e["hook"].lower()):
        notes.append("(1) hook tidak menyebut benda konkret — cek manual")

    # 1b · kalimat pertama harus pertanyaan ATAU fakta yang bisa dicek (ada angka)
    first = re.split(r"(?<=[.!?])\s+", e["hook"].strip())[0]
    if not (first.rstrip().endswith("?") or re.search(r"\d", first)):
        fails.append("(1b) kalimat pertama hook bukan pertanyaan dan tidak memuat angka — buka dengan pertanyaan atau fakta")

    # 1c · teks thumbnail 1–3 kata
    tt = (e.get("thumb_text") or "").strip()
    ntt = len(tt.split())
    if not 1 <= ntt <= 3:
        fails.append(f"(1c) teks thumbnail {ntt} kata, harus 1–3: '{tt}'")

    # 2 · ada yang salah, belum paham apa
    celah = e.get("celah", "")
    if not celah:
        fails.append("(2) tidak ada field celah")
    else:
        if len(celah.split()) > 18:
            fails.append(f"(2) celah {len(celah.split())} kata, batas 18")
        if not celah.strip().endswith("?"):
            fails.append("(2) celah harus berupa pertanyaan")

    # 3 · bertahan: celah tidak boleh dijawab sebelum turn
    if not any(part == "turn" for part, _ in e["beats"]):
        fails.append("(3) tidak ada segmen turn")
    tension = [t for part, t in e["beats"] if part == "tension"]
    if any("ternyata" in t.lower() for t in tension):
        fails.append("(3) ada 'ternyata' di tension — jawaban bocor sebelum turn")

    # 4 · kejutan: turn tidak menambah angka baru
    if not e.get("turn_verdict"):
        fails.append("(4) tidak ada turn_verdict")
    if not e.get("turn_quote"):
        fails.append("(4) tidak ada turn_quote (dugaan yang dipatahkan)")
    fresh = turn_numbers(e)
    if fresh:
        fails.append(f"(4) angka baru muncul pertama kali di turn: {', '.join(fresh)}")

    # 5 · diingat
    g = e.get("gambar_melekat", "")
    if not g:
        fails.append("(5) tidak ada gambar_melekat")
    elif len(g.split()) > 14:
        fails.append(f"(5) gambar_melekat {len(g.split())} kata, batas 14")
    sh = echo(e["hook"], e["loop"])
    if not sh:
        fails.append("(5) penutup tidak memanggil satu kata pun dari hook")

    # kelayakan produksi
    total = len(e["hook"].split()) + sum(len(t.split()) for _, t in e["beats"]) + len(e["loop"].split())
    secs = round(total / 2.45)
    if not 42 <= secs <= 62:
        fails.append(f"(produksi) {secs} detik, di luar 42–62")
    if len(e["cues"]) > 5:
        fails.append("(produksi) cue lebih dari 5")
    if not 2 <= len(tension) <= 6:
        notes.append(f"(produksi) {len(tension)} beat tension — 3–4 paling sehat")

    return fails, notes, sh, secs


def main():
    want = sys.argv[1:] or [e["ep"] for e in EPISODES]
    rows, nfail = [], 0
    for e in EPISODES:
        if e["ep"] not in want:
            continue
        fails, notes, sh, secs = check(e)
        nfail += len(fails)
        status = "LULUS" if not fails else "GAGAL"
        print(f"{e['ep']}  {status}  {secs}s  echo=\"{', '.join(sh) or '-'}\"")
        for f in fails:
            print(f"    ✗ {f}")
        for n in notes:
            print(f"    · {n}")
        rows.append((e["ep"], status, len(fails)))
    ok = sum(1 for _, s, _ in rows if s == "LULUS")
    print(f"\n{ok}/{len(rows)} lulus · {nfail} masalah")
    return 0 if nfail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
