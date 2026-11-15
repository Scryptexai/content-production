"""drive_export.py — siapkan naskah untuk Google Drive, satu dokumen per episode.

Alasan: pemilik merender VO sendiri di ElevenLabs, lalu menaruhnya di timeline.
Yang ia butuh bukan JSON: ia butuh (1) teks bersih per segmen, dan (2) kapan
tiap segmen harus mulai, supaya VO dan teks di layar jatuh di tempat yang sama.

Dua jenis berkas yang dihasilkan:
  SHORT/EPxx — JUDUL.md   satu segmen satu baris + tabel timestamp
  LONG/EPxx — JUDUL.md    satu bab satu blok + tabel paragraf

Model waktu (sama dengan build_timing.py):
  lead-in 0,15 s · jeda antar segmen 0,22 s · ekor 0,9 s · pace 145 kata/menit
  Untuk naskah panjang, pace dipakai 130 kata/menit (narasi lambat) dan jeda
  antar bab 0,8 s.

    python3 tools/drive_export.py
"""

import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
from content_data import EPISODES  # noqa: E402

OUT = ROOT / "11_CONTENT" / "09_DRIVE"
SRC_LONG = ROOT / "11_CONTENT" / "07_LONGFORM"

WPM_SHORT = 145.0
WPM_LONG = 130.0
GAP = 0.22
LEAD = 0.15
TAIL = 0.9
CHAP_GAP = 0.8


def mmss(sec):
    m, s = divmod(sec, 60)
    return f"{int(m):02d}:{s:05.2f}"


def durasi(kata, wpm):
    return max(0.8, kata / wpm * 60)


def short_segments(ep):
    segs = [("00_hook", ep["hook"])]
    for i, (part, text) in enumerate(ep["beats"]):
        segs.append((f"{i + 1:02d}_{part}", text))
    segs.append(("99_loop", ep["loop"]))
    return segs


def short_doc(ep):
    segs = short_segments(ep)
    total_kata = sum(len(t.split()) for _, t in segs)
    t = LEAD
    rows = []
    for kunci, teks in segs:
        d = durasi(len(teks.split()), WPM_SHORT)
        rows.append((kunci, t, d, len(teks.split()), teks))
        t += d + GAP
    total = t - GAP + TAIL

    L = [f"# {ep['ep']} — {ep['title']}", "",
         f"**Seri:** {ep['series']}  ·  **Segmen:** {len(segs)}  ·  "
         f"**Kata:** {total_kata}  ·  **Target durasi:** {ep.get('durasi', '-')} dtk  ·  "
         f"**Estimasi model:** {total:.1f} dtk", "",
         "## Setelan ElevenLabs", "",
         "| unsur | nilai |", "|---|---|",
         "| model | `eleven_multilingual_v2` atau `eleven_turbo_v2_5` |",
         "| stability / similarity / style | **0.38** / **0.82** / **0.35**, speaker boost **on** |",
         "| speed | **0.85** (naikkan ke 0.90 kalau hasilnya di bawah 130 kata/menit) |",
         "| format | mp3 44.1 kHz mono |",
         "| nama berkas | pakai kolom **berkas** di tabel bawah |", "",
         "## Tabel timestamp", "",
         "`mulai` dihitung dari model waktu kanal: lead-in 0,15 s, jeda antar segmen 0,22 s, "
         "ekor 0,90 s. Kalau hasil render meleset, ukur ulang durasi tiap berkas lalu geser "
         "kolom `mulai` — urutannya tidak berubah.", "",
         "| berkas | kunci | mulai | durasi | kata | teks |", "|---|---|---|---|---|---|"]
    for kunci, start, d, kata, teks in rows:
        L.append(f"| `{ep['ep']}_{kunci}.mp3` | {kunci} | {mmss(start)} | {d:.1f} s | {kata} | {teks} |")
    L += ["", f"**Total:** {mmss(total)} ({total:.1f} detik)", "",
          "## Teks bersih — tempel satu per satu", "",
          "Jangan digabung. Satu segmen = satu berkas VO.", "", "```"]
    L += [t for _, t in segs]
    L += ["```", "",
          "## Catatan produksi", "",
          "· Pertanyaan harus berakhir naik.",
          "· Satu segmen satu tarikan napas.",
          "· Jangan menambahkan tag atau jeda tertulis di dalam teks.",
          "· Loop: segmen terakhir dipakai lagi di awal (tonton ulang).", ""]
    return "\n".join(L), total_kata, total


def long_chapters(path):
    """Baca berkas panjang, kelompokkan per bab, kumpulkan paragraf narasi."""
    lines = path.read_text(encoding="utf-8").splitlines()
    bab, paras = [], []
    current = None
    for ln in lines:
        s = ln.strip()
        if s.startswith("## BAB"):
            current = {"judul": s.lstrip("# ").strip(), "paras": []}
            bab.append(current)
        elif not s or s.startswith(("#", ">", "---", "`[", "|", "**Seri", "**Pertanyaan")):
            continue
        elif current is not None:
            current["paras"].append(s)
    paras = [p for b in bab for p in b["paras"]]
    return bab, paras


def long_doc(ep, path):
    bab, paras = long_chapters(path)
    kata_total = sum(len(p.split()) for p in paras)
    t = 0.0
    rows_bab, rows_par, no = [], [], 0
    for b in bab:
        mulai_bab = t
        for p in b["paras"]:
            d = durasi(len(p.split()), WPM_LONG)
            no += 1
            rows_par.append((no, mmss(t), d, len(p.split()), p))
            t += d
        rows_bab.append((b["judul"], mmss(mulai_bab), t - mulai_bab,
                         sum(len(p.split()) for p in b["paras"])))
        t += CHAP_GAP
    total = t - CHAP_GAP

    L = [f"# {ep['ep']} — {ep['title']}", "",
         f"**Seri:** {ep['series']}  ·  **Kata:** {kata_total}  ·  "
         f"**Estimasi durasi:** {total / 60:.1f} menit "
         f"(pace {int(WPM_LONG)} kata/menit)", "",
         "## Setelan ElevenLabs", "",
         "| unsur | nilai |", "|---|---|",
         "| model | `eleven_multilingual_v2` |",
         "| stability / similarity / style | **0.38** / **0.82** / **0.35**, speaker boost **on** |",
         "| speed | **0.88** — pace narasi panjang, jangan dinaikkan |",
         "| format | mp3 44.1 kHz mono |", "",
         "## Timestamp per bab", "",
         "| bab | mulai | durasi | kata |", "|---|---|---|---|"]
    for judul, mulai, d, kata in rows_bab:
        L.append(f"| {judul} | {mulai} | {d / 60:.1f} mnt | {kata} |")
    L += ["", f"**Total:** {total / 60:.1f} menit", "",
          "## Timestamp per paragraf", "",
          "Satu paragraf = satu berkas VO. Kolom `teks` memuat 10 kata pertama, "
          "supaya kamu bisa mencocokkan berkas dengan barisnya.", "",
          "| # | mulai | durasi | kata | 10 kata pertama |", "|---|---|---|---|---|"]
    for no_, mulai, d, kata, p in rows_par:
        awal = " ".join(p.split()[:10]) + ("…" if kata > 10 else "")
        L.append(f"| {no_} | {mulai} | {d:.1f} s | {kata} | {awal} |")

    L += ["", "## Naskah", ""]
    for b in bab:
        L += [f"### {b['judul']}", ""]
        for p in b["paras"]:
            L.append(p)
            L.append("")
    L += ["## Catatan produksi", "",
          "· Kotak 🎬 di berkas kerja (07_LONGFORM) tidak ikut ke sini — itu catatan visual.",
          "· Jangan berganti suara di tengah naskah.",
          "· Bab 6 harus tetap terasa terbuka; jangan menambahkan kesimpulan saat merekam.", ""]
    return "\n".join(L), kata_total, total


def main():
    (OUT / "SHORT").mkdir(parents=True, exist_ok=True)
    (OUT / "LONG").mkdir(parents=True, exist_ok=True)

    indeks = ["# INDEKS NASKAH ODDCHAPTER", "",
              "Satu dokumen per episode. Kolom **mulai** dipakai untuk menaruh berkas VO "
              "di timeline; kolom **berkas** dipakai sebagai nama berkas suara.", ""]

    indeks += ["## SHORT (35–45 detik)", "",
               "| episode | judul | seri | segmen | kata | estimasi |", "|---|---|---|---|---|---|"]
    for e in EPISODES:
        doc, kata, total = short_doc(e)
        nama = f"{e['ep']} — {e['title']}.md"
        (OUT / "SHORT" / nama).write_text(doc, encoding="utf-8")
        indeks.append(f"| {e['ep']} | {e['title']} | {e['series']} | 9 | {kata} | {total:.0f} dtk |")

    indeks += ["", "## LONG (naskah panjang)", "",
               "| episode | judul | seri | kata | estimasi |", "|---|---|---|---|---|"]
    for path in sorted(SRC_LONG.glob("EP*_PANJANG.md")):
        kode = path.stem.split("_")[0]
        e = next(x for x in EPISODES if x["ep"] == kode)
        doc, kata, total = long_doc(e, path)
        nama = f"{kode} — {e['title']}.md"
        (OUT / "LONG" / nama).write_text(doc, encoding="utf-8")
        indeks.append(f"| {kode} | {e['title']} | {e['series']} | {kata:,} | {total / 60:.1f} mnt |"
                      .replace(",", "."))

    (OUT / "00_INDEKS.md").write_text("\n".join(indeks) + "\n", encoding="utf-8")
    print("SHORT:", len(list((OUT / 'SHORT').glob('*.md'))), "berkas")
    print("LONG :", len(list((OUT / 'LONG').glob('*.md'))), "berkas")


if __name__ == "__main__":
    main()
