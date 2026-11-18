#!/usr/bin/env python3
"""Potong master 16:9 SB-EP02 jadi lima Shorts 9:16.

Kenapa bukan crop: caption master ada di kiri bawah 16:9, crop vertikal akan
memotongnya. Klip 16:9 diletakkan utuh di tengah kanvas 1080x1920 dengan latar
versi blur dari gambar yang sama.

Beda dari versi EP01 (yang memakai angka waktu tulis tangan): di sini rentang
ditulis dalam WAKTU VO ASLI lalu dipetakan ke waktu master lewat
longform.generated.json, karena master menyisipkan kartu bab 2,6 dtk. Dengan
begitu Short tidak pernah mulai atau berhenti di dalam kartu, dan satu Short
boleh terdiri dari dua potongan (mis. hook + inti).

    python3 tools/make_shorts_ep02.py --dry-run
    python3 tools/make_shorts_ep02.py
    python3 tools/make_shorts_ep02.py S3
"""
import argparse
import json
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
REPO = ROOT.parent
GEN = ROOT / "10_FILM" / "remotion" / "src" / "longform.generated.json"
MASTER = ROOT / "10_FILM" / "remotion" / "output" / "episodes" / "SB-EP02_MH370_1920x1080_master.mp4"
OUT = REPO / "work" / "shorts"
FONTS = ROOT / ".build" / "fonts"
SG7 = FONTS / "space-grotesk-latin-700-normal.ttf"
IN6 = FONTS / "inter-latin-600-normal.ttf"
FFMPEG = "ffmpeg"

# (id, [(awal, akhir) dalam waktu VO asli], hook 1, hook 2, label, klaim)
SHORTS = [
    ("S1",
     [(0.30, 23.30), (109.20, 131.00)],
     "Pesawat Ini Terlacak Tujuh Kali",
     "dan Kita Tetap Kehilangan Dia",
     "MH370 · 02:25 – 08:19",
     "Tujuh handshake tidak membawa posisi — hanya jarak dan pergeseran frekuensi."),
    ("S2",
     [(135.00, 180.00)],
     "Satu Angka Doppler,",
     "Seluruh Koridor Utara Gugur",
     "MH370 · BTO & BFO",
     "BFO membaca arah gerak; dari situ busur ketujuh jadi dasar pencarian."),
    ("S3",
     [(263.20, 316.60)],
     "Pencarian Termahal di Dunia,",
     "Ditemukan Tukang Bersih Pantai",
     "MH370 · TIGA SERPIHAN",
     "Tiga serpihan dikonfirmasi mengunci arah, bukan titik."),
    ("S4",
     [(221.00, 262.60)],
     "28 Hari, 7.571 km²,",
     "Hasilnya Nol",
     "MH370 · PENCARIAN 2025–26",
     "Fase 2025–26 ditutup 23 Januari 2026; 8 Maret 2026 tanpa bangkai."),
    ("S5",
     [(317.20, 364.00)],
     "Data Sama Persis,",
     "Dua Titik Jatuh Berbeda",
     "MH370 · DUA PEMBACAAN",
     "BTO dan BFO identik; pembedanya kecepatan turun di menit terakhir."),
]


def load_map():
    data = json.loads(GEN.read_text(encoding="utf-8"))
    spans = [(s["origStart"], s["origEnd"], s["start"]) for s in data["segments"]]
    return data, spans


def to_master(t, spans):
    """Waktu VO asli → waktu master (kartu bab ikut menggeser)."""
    for a, b, ms in spans:
        if a - 0.01 <= t <= b + 0.01:
            return ms + (t - a)
    raise SystemExit(f"waktu {t}s di luar semua segmen")


def drawtext(text, size, y, color, font, alpha="1"):
    esc = text.replace("\\", "\\\\").replace("'", "\\'").replace(":", "\\:")
    return (f"drawtext=fontfile={font}:text='{esc}':x=64:y={y}:fontsize={size}:"
            f"fontcolor={color}:alpha={alpha}")


def wrap(text, width=46, max_lines=3):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = f"{cur} {w}".strip()
        if len(t) <= width:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines[:max_lines]


def build(sid, parts, l1, l2, label, claim, spans, dry=False):
    spans_m = [(to_master(a, spans), to_master(b, spans)) for a, b in parts]
    dur = sum(b - a for a, b in spans_m)
    chain, alabels, vl = [], [], []
    for i, (a, b) in enumerate(spans_m):
        chain.append(f"[0:v]trim=start={a:.3f}:end={b:.3f},setpts=PTS-STARTPTS[v{i}]")
        chain.append(f"[0:a]atrim=start={a:.3f}:end={b:.3f},asetpts=PTS-STARTPTS[a{i}]")
        vl.append(f"[v{i}]")
        alabels.append(f"[a{i}]")
    if len(spans_m) > 1:
        chain.append("".join(vl) + f"concat=n={len(vl)}:v=1:a=0[src]")
        chain.append("".join(alabels) + f"concat=n={len(alabels)}:v=0:a=1[aud]")
    else:
        chain.append("[v0]null[src]")
        chain.append("[a0]anull[aud]")

    cl = wrap(claim)
    cl1 = cl[0] if cl else ""
    cl2 = cl[1] if len(cl) > 1 else ""
    cl3 = cl[2] if len(cl) > 2 else ""
    hook_alpha = (f"if(lt(t,0.4),t/0.4,if(lt(t,{dur - 2.6:.2f}),1,"
                  f"max(0,({dur - 2.0:.2f}-t)/0.6)))")
    chain += [
        "[src]split=2[bg][fg]",
        "[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
        "gblur=sigma=26,eq=brightness=-0.12:saturation=0.55[bgz]",
        "[fg]scale=1080:-2[fgz]",
        "[bgz][fgz]overlay=0:468[v1]",
        "[v1]drawbox=x=0:y=464:w=1080:h=3:color=0xC6602A@0.85:t=fill[v2]",
        "[v2]drawbox=x=0:y=1081:w=1080:h=3:color=0xC6602A@0.35:t=fill[v3]",
        "[v3]" + drawtext(label, 28, 196, "0xC6602A", IN6, "0.95") + "[v4]",
        f"[v4]" + drawtext(l1, 66, 248, "0xF0ECE0", SG7, f"'{hook_alpha}'") + "[v5]",
        f"[v5]" + drawtext(l2, 66, 330, "0xF0ECE0", SG7, f"'{hook_alpha}'") + "[v6]",
        "[v6]drawbox=x=0:y=1092:w=1080:h=828:color=0x06080A@0.86:t=fill[v6a]",
        "[v6a]drawbox=x=64:y=1178:w=220:h=3:color=0xC6602A@0.95:t=fill[v6b]",
        f"[v6b]" + drawtext(cl1, 34, 1206, "0xF0ECE0", IN6, "0.96") + "[v6c]",
        f"[v6c]" + drawtext(cl2, 34, 1258, "0xF0ECE0", IN6, "0.96") + "[v6d]",
        f"[v6d]" + drawtext(cl3, 34, 1310, "0xF0ECE0", IN6, "0.96") + "[v6e]",
        f"[v6e]drawtext=fontfile={SG7}:text='ODDCHAPTER':x=64:y=1768:fontsize=34:"
        "fontcolor=0xF0ECE0:alpha=0.92[v7]",
        f"[v7]drawtext=fontfile={IN6}:text='MH370 · SATU BUSUR SATELIT':x=64:y=1820:"
        "fontsize=26:fontcolor=0xC6CEBE:alpha=0.85[v8]",
        f"[v8]drawbox=x=0:y=1912:w='1080*t/{dur:.3f}':h=6:color=0xC6602A@0.9:t=fill[vout]",
        f"[aud]afade=t=in:st=0:d=0.35,afade=t=out:st={max(0.0, dur - 0.6):.3f}:d=0.6[aout]",
    ]
    out = OUT / f"SB-EP02_{sid}.mp4"
    if dry:
        print(f"{sid}  {dur:5.1f}s  master {['%.2f–%.2f' % s for s in spans_m]}")
        return {"id": sid, "duration": round(dur, 2), "parts": spans_m}
    cmd = [FFMPEG, "-hide_banner", "-loglevel", "error", "-y", "-i", str(MASTER),
           "-filter_complex", ";".join(chain), "-map", "[vout]", "-map", "[aout]",
           "-t", f"{dur:.3f}", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
           "-profile:v", "high", "-pix_fmt", "yuv420p", "-r", "30",
           "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-ac", "2",
           "-movflags", "+faststart", str(out)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-1500:])
        raise SystemExit(f"gagal {sid}")
    print(f"{out.name}  {dur:5.1f}s  {out.stat().st_size / 1048576:.1f} MB")
    return {"id": sid, "file": out.name, "duration": round(dur, 2), "parts": spans_m,
            "hook": f"{l1} {l2}", "claim": claim}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("only", nargs="?", default=None)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    data, spans = load_map()
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    for s in SHORTS:
        if args.only and s[0] != args.only:
            continue
        rows.append(build(*s, spans, dry=args.dry_run))
    if not args.dry_run:
        (OUT / "shorts_sb-ep02.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1))
        total = sum(r["duration"] for r in rows)
        print(f"{len(rows)} Short · {total:.0f} dtk")


if __name__ == "__main__":
    sys.exit(main())
