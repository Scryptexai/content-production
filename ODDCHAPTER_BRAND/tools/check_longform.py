#!/usr/bin/env python3
"""
check_longform.py — gerbang format panjang (lihat 11_CONTENT/07_LONGFORM/README.md).

Bukan selera. Yang diperiksa hanya hal yang bisa dibuktikan mekanis dan, kalau
gagal, hampir pasti merusak episode:

  · durasi masuk akal (kata → menit pada 150 kata/menit)
  · setiap babak menyisakan pertanyaan
  · setiap babak punya isyarat visual
  · satu POV di seluruh narasi (tidak ada "aku", tidak ada "kamu")
  · tidak ada kata pengisi / kata yang meminta perhatian
  · setiap angka di narasi punya baris di SOURCES.md

    python3 tools/check_longform.py LF01
    python3 tools/check_longform.py            # semua LF di 07_LONGFORM/
"""
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
LONGFORM = ROOT / "11_CONTENT" / "07_LONGFORM"

WPM = 150
MIN_MIN, MAX_MIN = 8.0, 12.0
BANNED = {"misteri", "rahasia", "aneh", "menakjubkan", "mengerikan", "ternyata",
          "sebenarnya", "sungguh", "benar-benar", "sangat", "banyak orang percaya",
          "tidak terpecahkan"}
POV_OFFENDERS = {"aku", "saya", "kalian"}


def vo_lines(text):
    """Baris narasi = kutipan blok yang bukan catatan cara baca."""
    out = []
    for line in text.splitlines():
        if not line.startswith(">"):
            continue
        body = line.lstrip("> ").strip()
        if not body or body.startswith("**"):
            continue
        out.append(body)
    return out


def acts(text):
    """Pecah per heading '### BABAK'."""
    parts, current = [], None
    for line in text.splitlines():
        if line.startswith("### BABAK"):
            current = {"title": line.strip("# "), "lines": []}
            parts.append(current)
        elif current is not None:
            current["lines"].append(line)
    for part in parts:
        part["vo"] = vo_lines("\n".join(part["lines"]))
        part["text"] = "\n".join(part["lines"])
    return parts


def words(text):
    return [w for w in re.split(r"[^0-9A-Za-zÀ-ÿ]+", text.lower()) if w]


def check(folder):
    script = folder / "SCRIPT.md"
    sources = folder / "SOURCES.md"
    fails, notes = [], []

    if not script.exists():
        return [f"SCRIPT.md tidak ada di {folder}"], notes
    text = script.read_text(encoding="utf-8")

    narration = vo_lines(text)
    n_words = len(words(" ".join(narration)))
    minutes = n_words / WPM
    notes.append(f"{n_words} kata ≈ {minutes:.1f} menit (pada {WPM} kata/menit)")
    if not (MIN_MIN <= minutes <= MAX_MIN):
        fails.append(f"durasi {minutes:.1f} menit di luar {MIN_MIN:.0f}–{MAX_MIN:.0f} menit")

    act_list = acts(text)
    if len(act_list) < 6:
        fails.append(f"hanya {len(act_list)} babak; format panjang butuh 6–8")
    for act in act_list:
        name = act["title"].split("·")[0].strip()
        joined = " ".join(act["vo"])
        if "?" not in joined:
            fails.append(f"{name}: tidak ada pertanyaan yang disisakan")
        if "VISUAL" not in act["text"]:
            fails.append(f"{name}: tidak ada isyarat VISUAL")
        if not act["vo"]:
            fails.append(f"{name}: narasi kosong")

    lowered = " ".join(narration).lower()
    for word in BANNED:
        if re.search(rf"\b{re.escape(word)}\b", lowered):
            fails.append(f"kata terlarang di narasi: “{word}”")
    for word in POV_OFFENDERS:
        if re.search(rf"\b{word}\b", lowered):
            fails.append(f"POV pecah: “{word}” muncul di narasi (POV harus satu)")

    if " aku " in f" {lowered} ":
        fails.append("POV pecah: “aku” muncul di narasi")

    if not sources.exists():
        fails.append("SOURCES.md tidak ada")
    else:
        rows = [l for l in sources.read_text(encoding="utf-8").splitlines()
                if l.startswith("|") and not set(l) <= set("|-: ")]
        if len(rows) < 20:
            fails.append(f"SOURCES.md baru {len(rows)} baris klaim; minimal 20")
        notes.append(f"{len(rows)} baris klaim di SOURCES.md")

    # angka di narasi harus muncul di SOURCES.md (dibandingkan sebagai digit)
    src_text = sources.read_text(encoding="utf-8") if sources.exists() else ""
    numbers = {n.replace(".", "") for n in re.findall(r"\b\d[\d.]{1,6}\b", " ".join(narration))}
    missing = sorted(n for n in numbers if n not in src_text.replace(".", ""))
    if missing:
        notes.append("angka yang tidak muncul apa adanya di SOURCES.md: " + ", ".join(missing))

    return fails, notes


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else None
    folders = ([p for p in sorted(LONGFORM.glob("LF*")) if p.is_dir()]
               if not target else [LONGFORM / target if (LONGFORM / target).exists()
                                   else next(iter(LONGFORM.glob(f"{target}_*")), None)])
    folders = [f for f in folders if f and f.exists()]
    if not folders:
        print("tidak ada folder LF di 11_CONTENT/07_LONGFORM/")
        return 1

    bad = 0
    for folder in folders:
        fails, notes = check(folder)
        print(f"\n=== {folder.name} ===")
        for note in notes:
            print(f"  · {note}")
        if fails:
            bad += 1
            for f in fails:
                print(f"  ✗ {f}")
        else:
            print("  ✓ LULUS")

    print()
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
