"""
export_srt.py — caption + metadata turunan dari longform.generated.json.

Caption yang dibakar di video dipotong 8 kata (nyaman dibaca sekilas). Untuk
unggahan, potongan yang sama dipecah lagi jadi baris 40–42 karakter dan dibatasi
±7 dtk per cue, lalu ditulis sebagai SRT. Karena sumbernya timestamp kata
(words.json), cue-nya jatuh di kata, bukan di pembagian durasi.

    python3 tools/export_srt.py SB-EP02
"""
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
GEN = ROOT / "10_FILM" / "remotion" / "src" / "longform.generated.json"
CAP = ROOT / "10_FILM" / "captions"
MAX_CHARS = 42
MAX_CUE = 7.0


def wrap(text, width=MAX_CHARS, max_lines=2):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = f"{cur} {w}".strip()
        if len(t) <= width or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    if len(lines) <= max_lines:
        return lines
    # terlalu panjang: bagi rata, jangan melebihi dua baris kalau bisa
    out, per = [], -(-len(words) // max_lines)
    for i in range(0, len(words), per):
        out.append(" ".join(words[i:i + per]))
    return out[:max_lines]


def ts(t):
    h, rem = divmod(max(0.0, t), 3600)
    m, s = divmod(rem, 60)
    ms = int(round((s - int(s)) * 1000))
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{ms:03d}"


def main():
    ep = sys.argv[1] if len(sys.argv) > 1 else "SB-EP02"
    data = json.loads(GEN.read_text(encoding="utf-8"))
    caps = [(c["t0"], c["t1"], c["text"]) for s in data["segments"] for c in s["captions"]]
    caps.sort()
    CAP.mkdir(parents=True, exist_ok=True)
    out = CAP / f"{ep}.id.srt"
    n = 0
    with out.open("w", encoding="utf-8") as f:
        for t0, t1, text in caps:
            if t1 - t0 > MAX_CUE:            # potongan terlalu panjang → pecah dua
                mid = (t0 + t1) / 2
                parts = [text.split(" ")[: len(text.split(" ")) // 2],
                         text.split(" ")[len(text.split(" ")) // 2:]]
                spans = [(t0, mid), (mid, t1)]
            else:
                parts, spans = [text.split(" ")], [(t0, t1)]
            for words, (a, b) in zip(parts, spans):
                body = wrap(" ".join(words))
                if not body or not body[0]:
                    continue
                n += 1
                f.write(f"{n}\n{ts(a)} --> {ts(b)}\n" + "\n".join(body) + "\n\n")
    print(f"{out.relative_to(ROOT)}  {n} cue · {len(caps)} potongan caption")

    # bab untuk deskripsi YouTube (timestamp dari kartu yang sebenarnya)
    lines = [f"{int(c['start']) // 60:02d}:{int(c['start']) % 60:02d}  {c['title'].title()}"
             for c in data["cards"]]
    print("\n".join(lines))


if __name__ == "__main__":
    main()
