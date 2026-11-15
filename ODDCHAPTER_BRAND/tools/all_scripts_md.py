"""all_scripts_md.py — gabungkan naskah per episode jadi satu dokumen review.

Sumber kebenarannya adalah berkas `02_SCRIPT/EPxx_*.md` yang ditulis tangan,
bukan `content_data.py` (isi keduanya sengaja tidak identik: yang di repo sudah
melalui penyuntingan, yang di data dipakai mesin untuk timing dan TTS).

    python3 tools/all_scripts_md.py
"""

import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
from content_data import EPISODES  # noqa: E402

SCRIPTS = ROOT / "11_CONTENT" / "02_SCRIPT"

HEAD = """# ODDCHAPTER — 21 SCRIPT, 7 HARI

Satu episode = satu hari-slot = tiga platform. Semua script di bawah memakai
struktur yang sama (HOOK 0–3 · BEAT · TITIK BALIK · LOOP) dan semuanya masih
berstatus `NEEDS-SOURCE` sampai rujukannya dibaca.

| # | Hari | Slot | Seri | Headline | POV | Detik |
|---|---|---|---|---|---|---|"""


def file_for(ep):
    hits = sorted(SCRIPTS.glob(f"{ep['ep']}_*.md"))
    if not hits:
        return None
    return hits[0]


def main():
    rows, body, missing = [], [], []
    for e in EPISODES:
        rows.append(f"| {int(e['ep'][2:])} | H{e['day']} | {e['slot']} | {e['series']} | "
                    f"{e['title']} | {e['pov']} | {e['durasi']} |")
        f = file_for(e)
        if not f:
            missing.append(e["ep"])
            continue
        md = f.read_text().rstrip()
        body += ["", "---", "", md.replace("# ", "## ", 1)]

    out = "\n".join([HEAD] + rows + body) + "\n"
    (SCRIPTS / "ALL_SCRIPTS.md").write_text(out)
    print(f"ALL_SCRIPTS.md: {len(EPISODES) - len(missing)} naskah digabung"
          + (f" · belum ada berkas: {', '.join(missing)}" if missing else ""))


if __name__ == "__main__":
    main()
