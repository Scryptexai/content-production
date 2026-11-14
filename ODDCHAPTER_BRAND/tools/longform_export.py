"""longform_export.py — bersihkan naskah panjang jadi teks siap tempel.

Ambil setiap `EPxx_PANJANG.md` di 11_CONTENT/07_LONGFORM, buang semua baris
produksi (judul, kotak 🎬, penanda waktu, garis pemisah), sisakan narasi saja.
Satu paragraf = satu baris di berkas `.txt`, supaya bisa ditempel bertahap ke
ElevenLabs dan jeda diatur di timeline, bukan oleh model.

    python3 tools/longform_export.py
"""

import pathlib
import re

HERE = pathlib.Path(__file__).resolve().parent
SRC = HERE.parent / "11_CONTENT" / "07_LONGFORM"


def is_production(line: str) -> bool:
    s = line.strip()
    if not s:
        return True
    if s.startswith(("#", ">", "---", "`[", "**Seri", "**Pertanyaan", "|")):
        return True
    return False


def main():
    for md in sorted(SRC.glob("EP*_PANJANG.md")):
        body = md.read_text(encoding="utf-8").splitlines()
        paras = [re.sub(r"^[-·]\s*", "", ln.strip()) for ln in body if not is_production(ln)]
        txt = md.with_suffix(".txt")
        txt.write_text("\n".join(paras) + "\n", encoding="utf-8")
        words = sum(len(p.split()) for p in paras)
        print(f"{md.stem:22s} {len(paras):3d} paragraf · {words:5d} kata · ±{words / 150:.1f} mnt")


if __name__ == "__main__":
    main()
