"""tts_export.py — naskah siap tempel ke ElevenLabs, satu segmen satu baris.

Kenapa ada: pemilik memilih merender suara sendiri di ElevenLabs (16 Nov 2026).
Yang ia butuh bukan JSON, bukan timing, bukan mp3 — teks bersih yang bisa
ditempel, dengan urutan yang sama seperti yang dibaca `build_timing.py`.

Aturan keluaran:
  · satu berkas .txt per episode, satu segmen per baris, tanpa penomoran,
    tanpa markdown, tanpa tag — persis yang lolos `check_story.tts_safe`;
  · satu berkas .md per episode: kunci segmen, jumlah kata, perkiraan durasi,
    dan setelan suara yang disarankan;
  · indeks `00_INDEKS.md` berisi semua episode + total kata.

    python3 tools/tts_export.py            # semua episode
    python3 tools/tts_export.py EP09 EP10
"""

import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
from content_data import EPISODES  # noqa: E402

OUT = ROOT / "11_CONTENT" / "02_SCRIPT" / "TTS"
WPM = 145.0          # pace narasi yang dipakai kanal (terukur 138–146 wpm)
GAP = 0.22


def segments(ep):
    """(kunci, teks) — sama persis dengan yang dipakai build_timing."""
    out = [("00_hook", ep["hook"])]
    for i, (part, text) in enumerate(ep["beats"]):
        out.append((f"{i + 1:02d}_{part}", text))
    out.append(("99_loop", ep["loop"]))
    return out


def render(ep):
    segs = segments(ep)
    words = sum(len(t.split()) for _, t in segs)
    speak = words / WPM * 60
    total = speak + GAP * (len(segs) - 1) + 0.15 + 0.9
    return segs, words, total


def main():
    wanted = sys.argv[1:] or [e["ep"] for e in EPISODES]
    OUT.mkdir(parents=True, exist_ok=True)
    index = ["# Indeks naskah TTS", "",
             "Satu segmen = satu baris. Tempel baris demi baris, **jangan** digabung:",
             "jeda antar segmen diatur di timeline (0,22 dtk), bukan oleh model.", "",
             "| episode | segmen | kata | perkiraan durasi |", "|---|---|---|---|"]

    for e in EPISODES:
        if e["ep"] not in wanted:
            continue
        segs, words, total = render(e)
        txt = OUT / f"{e['ep']}.txt"
        txt.write_text("\n".join(t for _, t in segs) + "\n", encoding="utf-8")

        md = [f"# {e['ep']} — {e['title']}", "",
              f"**Seri:** {e['series']} · **POV:** {e.get('pov', '-')} · "
              f"**{len(segs)} segmen · {words} kata · ±{total:.0f} detik**", "",
              "## Setelan ElevenLabs", "",
              "| unsur | nilai |", "|---|---|",
              "| model | `eleven_multilingual_v2` atau `eleven_turbo_v2_5` |",
              "| setelan | stability **0.38** · similarity **0.82** · style **0.35** · speaker boost **on** |",
              "| kecepatan | **0.85** (kalau hasilnya <130 kata/menit, naikkan ke 0.90) |",
              "| format | mp3 44.1 kHz, mono |",
              "| nama berkas | sama dengan kolom kunci di bawah |", "",
              "## Segmen", "",
              "| kunci | kata | perkiraan | teks |", "|---|---|---|---|"]
        for key, text in segs:
            md.append(f"| `{key}` | {len(text.split())} | "
                      f"{len(text.split()) / WPM * 60:.1f} s | {text} |")
        md += ["", "## Catatan produksi", "",
               "· Pertanyaan harus berakhir naik. Kalau turun, ulangi segmen itu saja.",
               "· Satu segmen satu tarikan napas. Kalau terasa sesak, kalimatnya yang salah, "
               "bukan kecepatannya.",
               "· Berkas `.txt` sudah bersih dari markup; jangan menambahkan tag.",
               "· Sesudah semua segmen jadi, jalankan `python3 tools/build_timing.py "
               f"{e['ep']}` sebelum render.", ""]
        (OUT / f"{e['ep']}.md").write_text("\n".join(md), encoding="utf-8")

        index.append(f"| [{e['ep']}]({e['ep']}.md) | {len(segs)} | {words} | ±{total:.0f} s |")
        print(f"{e['ep']}  {len(segs)} segmen · {words} kata · ±{total:.0f} s")

    (OUT / "00_INDEKS.md").write_text("\n".join(index) + "\n", encoding="utf-8")
    print(f"\ntulis: {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
