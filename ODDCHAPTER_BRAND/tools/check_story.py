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
# ── 00D · PSIKOLOGI AUDIENS ────────────────────────────────────────────────
# Kata pengisi: bisa dihapus tanpa kehilangan makna, jadi ia hanya menambah durasi.
FILLER = {"sangat", "cukup", "benar-benar", "sebenarnya", "ternyata", "sungguh",
          "amat", "banget", "sekali", "agak", "kayaknya", "sepertinya", "rupanya",
          "mungkin", "begitu", "memang", "sangatlah"}

# Kalimat ringkasan: mematikan kail karena tidak menyebut benda dan tidak menyisakan celah.
SUMMARY = ("bertahun-tahun", "selama bertahun", "sampai sekarang", "hingga kini",
           "sampai hari ini", "banyak teori", "para ahli masih", "tidak terpecahkan",
           "di seluruh dunia", "selama berabad", "dianggap misteri", "banyak orang percaya")

# Benda yang bisa dilihat penonton. Satu baris wajib punya salah satunya (atau angka).
CONCRETE = set("""
orang pria perempuan anak ibu ayah istri bayi mahasiswa pendaki penjaga awak kapten penumpang pekerja
dokter ilmuwan insinyur tentara pasukan warga keluarga saudara mayat senjata tubuh tangan kaki kepala mata mulut
gigi tulang dada darah rambut wajah kulit otak jantung
tenda sepatu kaus jaket pakaian topi masker kuas kertas buku jurnal arsip surat peta kunci pintu
jendela kamar rumah meja kursi cangkir lampu lilin jam menara mercusuar kapal sekoci perahu layar
tong mobil jalan jembatan pagar pohon kayu batu gunung lereng jurang salju es air laut danau
sungai hutan api asap gas angin hujan kabut langit bintang tanah lantai atap dinding gantungan
pulau desa kota kampung darat pantai pelabuhan stasiun pabrik tambang terowongan gereja kuburan pos
sinyal radio suara frekuensi sirene nada rekaman film foto kamera label nama angka alamat kamar
karpet botol obat jarum timah nampan piring sendok pisau tali sekop bendera
makanan kompas palka sekstan kronometer jangkar layar kemudi dayung pelampung
""".split())

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


# ── 00E · SUARA NARATOR ─────────────────────────────────────────────────────
# Naskah yang berbunyi seperti laporan gagal bukan karena faktanya salah, tetapi
# karena tidak ada yang diajak bicara. Aturan di bawah menjaga suara itu.
REPORT_WORDS = {
    "diketahui", "dilaporkan", "tercatat", "merupakan", "disebutkan", "berdasarkan",
    "adapun", "tersebut", "sejumlah", "berbagai", "sedangkan", "namun", "sehingga",
    "mengakibatkan", "dilakukan", "terjadi", "yakni", "yaitu", "sementara",
}
LOOK = {"lihat", "lihatlah", "bayangkan", "coba", "ingat", "dengar", "dengarkan",
        "perhatikan", "pikirkan", "bayangkanlah", "ikut"}
SECOND = ("kamu", "kita", "anda")


def sentences(t):
    return [x for x in re.split(r"(?<=[.!?])\s+", t.strip()) if x]


def voice(e):
    """(6) suara narator — menyapa penonton, bukan membacakan laporan (00E)."""
    fails = []
    script = " ".join([e["hook"]] + [t for _, t in e["beats"]] + [e["loop"]])
    low = script.lower()

    bad = sorted({w for w in words(script) if w in REPORT_WORDS})
    if bad:
        fails.append(f"(6) kosakata laporan: {', '.join(bad)} — ganti dengan kalimat orang")

    looks = sorted({w for w in words(script) if w in LOOK})
    if len(looks) < 2:
        fails.append(f"(6) ajakan melihat cuma {len(looks)} — minimal 2 (lihat/bayangkan/coba/ingat)")

    second = [s for s in sentences(script) if re.search(r"\b(kamu|kita|anda)\b", s.lower())]
    if len(second) < 3:
        fails.append(f"(6) kalimat yang menyapa penonton cuma {len(second)} — minimal 3")

    nq = script.count("?")
    if nq < 2:
        fails.append(f"(6) pertanyaan di naskah cuma {nq} — minimal 2, penonton harus menjawab di kepala")

    for name, ln in [("hook", e["hook"])] + [(f"beat {i + 1}", t) for i, (_, t) in enumerate(e["beats"])] + [("loop", e["loop"])]:
        limit = 3 if name in ("hook", "loop") else 2
        n = len(sentences(ln))
        if n > limit:
            fails.append(f"(6) {name}: {n} kalimat dalam satu tarikan napas (maks {limit})")

    return fails


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

    # 1d · URUTAN PEMBUKA: klimaks + entitas → cut + pertanyaan → cerita (00B §0)
    ent = (e.get("entitas") or "").strip()
    if not ent:
        fails.append("(0) tidak ada field entitas — pembuka wajib menunjuk satu entitas, bukan lanskap")
    elif ent.lower() not in e["hook"].lower():
        fails.append(f"(0) entitas '{ent}' tidak disebut di hook — penonton harus bisa menunjuknya")

    tanya = (e.get("tanya") or "").strip()
    if not tanya:
        fails.append("(0) tidak ada field tanya — cut-nya tidak punya pertanyaan")
    else:
        if not tanya.endswith("?"):
            fails.append("(0) tanya bukan pertanyaan")
        if len(tanya.split()) > 18:
            fails.append(f"(0) tanya {len(tanya.split())} kata, batas 18")
        if tanya and e["hook"].strip() and tanya.lower() == e["hook"].lower():
            fails.append("(0) tanya sama dengan hook — cut-nya tidak menambah apa pun")

    if e.get("struktur") == "klimaks-awal":
        if not e["beats"] or e["beats"][0][0] != "tanya":
            fails.append("(0) struktur klimaks-awal: beat pertama harus 'tanya' (cut), bukan "
                         f"'{e['beats'][0][0] if e['beats'] else '-'}'")
        elif e["beats"][0][1].strip() != tanya:
            fails.append("(0) beat tanya tidak sama dengan field tanya — audio dan naskah akan berbeda")
    else:
        notes.append("(0) alur belum distruktur klimaks-di-awal (00B §0) — dibereskan saat episode diproduksi")

    # 1e · RELATE: satu baris yang menyapa penonton, sebelum tension (00D §3)
    script_text = " ".join([e["hook"]] + [t for _, t in e["beats"]] + [e["loop"]])
    rel = (e.get("relate") or "").strip()
    header = e.get("struktur") == "klimaks-awal"
    if header:
        if not rel:
            fails.append("(1e) tidak ada baris relate — penonton tidak punya tempat masuk")
        else:
            if rel not in script_text:
                fails.append("(1e) relate tidak ada di naskah — harus persis salah satu kalimat yang diucapkan")
            if not re.search(r"\b(kamu|kita|anda)\b", rel.lower()):
                fails.append("(1e) relate tidak menyapa penonton — pakai 'kamu' atau 'kita'")
            idx_rel = next((i for i, (_, t) in enumerate(e["beats"]) if t.strip() == rel), None)
            idx_ten = next((i for i, (p, _) in enumerate(e["beats"]) if p == "tension"), None)
            if idx_rel is not None and idx_ten is not None and idx_rel >= idx_ten:
                fails.append("(1e) relate diletakkan setelah tension — penonton harus masuk lebih dulu")
    else:
        notes.append("(1e) relate belum diisi (00D §3)")

    # 1f · DISKUSI: pertanyaan yang sengaja tidak dijawab episode (00D §4)
    dis = (e.get("diskusi") or "").strip()
    if header:
        if not dis:
            fails.append("(1f) tidak ada diskusi — tidak ada yang membuat orang berkomentar")
        else:
            if not dis.endswith("?"):
                fails.append("(1f) diskusi bukan pertanyaan")
            if len(dis.split()) > 18:
                fails.append(f"(1f) diskusi {len(dis.split())} kata, batas 18")
            if tanya and dis.lower() == tanya.lower():
                fails.append("(1f) diskusi sama dengan tanya — tanya harus dijawab, diskusi harus dibiarkan")
            if dis.rstrip("?") and dis.rstrip("?").lower() in script_text.lower():
                fails.append("(1f) diskusi diucapkan di naskah — pertanyaan komentar tidak boleh masuk VO")
    else:
        notes.append("(1f) diskusi belum diisi (00D §4)")

    # 3d · AUDIT KALIMAT: ≤16 kata, ada benda konkret, tanpa pengisi, tanpa ringkasan
    lines = [("hook", e["hook"])] + [(f"beat {i + 1}", t) for i, (_, t) in enumerate(e["beats"])] + [("loop", e["loop"])]
    line_bad = []
    for name, ln in lines:
        if len(ln.split()) > 16:
            line_bad.append(f"{name}: {len(ln.split())} kata — '{ln[:44]}…'")
        fill = [w for w in words(ln) if w in FILLER]
        if fill:
            line_bad.append(f"{name}: kata pengisi {', '.join(fill)}")
        for ph in SUMMARY:
            if ph in ln.lower():
                line_bad.append(f"{name}: kalimat ringkasan '{ph}'")
        def concrete(w):
            return w in CONCRETE or re.sub(r"(nya|ku|mu)$", "", w) in CONCRETE
        if not (re.search(r"\d", ln) or any(concrete(w) for w in words(ln))):
            line_bad.append(f"{name}: tidak ada benda konkret — '{ln[:44]}…'")
    if line_bad:
        if header:
            fails += [f"(3d) {b}" for b in line_bad[:6]]
        else:
            notes.append(f"(3d) {len(line_bad)} baris belum lolos audit kalimat (00D §5)")

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
    ph = e.get("photos") or []
    if ph and e.get("entitas") and any(w in ph[0] for w in ("island", "sea", "sky", "horizon")):
        fails.append(f"(produksi) foto pembuka '{ph[0]}' lanskap, bukan entitas — pembuka harus menunjuk orang/benda")
    if len(e["cues"]) > 5:
        fails.append("(produksi) cue lebih dari 5")
    if not 2 <= len(tension) <= 6:
        notes.append(f"(produksi) {len(tension)} beat tension — 3–4 paling sehat")

    # 6 · suara narator (00E)
    if e.get("voice_legacy"):
        notes.append("(6) suara laporan — episode ini tayang sebelum 00E; bukan contoh")
    else:
        fails += voice(e)

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
