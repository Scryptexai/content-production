#!/usr/bin/env python3
"""Potong klimaks master 16:9 jadi Shorts 9:16.

Kenapa bukan crop: master punya caption bakar di bawah-kiri; crop 9:16 akan
memotongnya. Jadi klip 16:9 diletakkan utuh di tengah kanvas 1080x1920, dengan
latar versi blur dari gambar yang sama — format Shorts yang lazim, dan caption
tetap terbaca.

Titik potong diambil dari batas segmen master (setelah kartu bab), jadi tidak
ada kata yang terbelah: setiap segmen dimulai dan diakhiri di jeda VO.
"""
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT.parent / "google_drive" / "EP01_ILLUMINATI_1920x1080_master_v3.mp4"
OUT = ROOT.parent / "work" / "shorts"
FONTS = ROOT / ".build" / "fonts"
SG7 = FONTS / "space-grotesk-latin-700-normal.ttf"
IN6 = FONTS / "inter-latin-600-normal.ttf"

FFMPEG = "ffmpeg"

# (id, start, end, baris hook 1, baris hook 2, label kecil)
SHORTS = [
    ("S1", 115.30, 158.00,
     "Teori Illuminati Lahir", "dari Buku, Bukan Bukti",
     "1797 · BARRUEL & ROBISON",
     "Dua penulis menerbitkan buku 1797. Teorinya menyebar lebih cepat daripada faktanya."),
    ("S2", 218.00, 245.10,
     "Simbolnya Dipinjam,", "Bukan Diciptakan",
     "MATA SATU · PIRAMIDA · DOLLAR",
     "Mata satu, piramida, segel di uang dollar: lambang lama yang diberi makna baru."),
    ("S3", 268.60, 309.20,
     "Dokumen Sama,", "Kesimpulan Berlawanan",
     "DUA CARA MEMBACA BUKTI",
     "Ketiadaan bukti bisa dibaca dua arah. Keduanya punya celah."),
]


def drawtext(text, size, y, color, font, alpha="1", spacing=0):
    esc = text.replace("'", "\\'").replace(":", "\\:")
    return (
        f"drawtext=fontfile={font}:text='{esc}':x=(w-text_w)/2:y={y}:"
        f"fontsize={size}:fontcolor={color}@{alpha}"
        + (f":borderw=0" if not spacing else "")
    )


def wrap_lines(text, max_chars=52):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if len(t) <= max_chars:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines[:2]


def build(sid, start, end, l1, l2, label, claim):
    dur = end - start
    fade_out = max(0.0, dur - 0.6)
    hook_alpha = "if(lt(t,0.4),t/0.4,if(lt(t,5.5),1,max(0,(6.2-t)/0.7)))"
    esc = lambda t: t.replace("'", "\\'")
    cl = wrap_lines(claim, 46)
    cl1 = cl[0] if cl else ""
    cl2 = cl[1] if len(cl) > 1 else ""

    chain = [
        f"[0:v]trim=start={start}:end={end},setpts=PTS-STARTPTS,setsar=1[src]",
        "[src]split=2[bg][fg]",
        "[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
        "gblur=sigma=26,eq=brightness=-0.12:saturation=0.55[bgz]",
        "[fg]scale=1080:-2[fgz]",
        "[bgz][fgz]overlay=0:468[v1]",
        "[v1]drawbox=x=0:y=464:w=1080:h=3:color=0xC6602A@0.85:t=fill[v2]",
        "[v2]drawbox=x=0:y=1081:w=1080:h=3:color=0xC6602A@0.35:t=fill[v3]",
        f"[v3]drawtext=fontfile={IN6}:text='{esc(label)}':x=64:y=196:fontsize=28:"
        "fontcolor=0xC6602A:alpha=0.95[v4]",
        f"[v4]drawtext=fontfile={SG7}:text='{esc(l1)}':x=64:y=248:fontsize=66:"
        f"fontcolor=0xF0ECE0:alpha='{hook_alpha}'[v5]",
        f"[v5]drawtext=fontfile={SG7}:text='{esc(l2)}':x=64:y=330:fontsize=66:"
        f"fontcolor=0xF0ECE0:alpha='{hook_alpha}'[v6]",
        "[v6]drawbox=x=0:y=1092:w=1080:h=520:color=0x06080A@0.80:t=fill[v6a]",
        "[v6a]drawbox=x=64:y=1178:w=220:h=3:color=0xC6602A@0.95:t=fill[v6b]",
        f"[v6b]drawtext=fontfile={IN6}:text='{esc(cl1)}':x=64:y=1214:fontsize=36:"
        "fontcolor=0xF0ECE0:alpha=0.96[v6c]",
        f"[v6c]drawtext=fontfile={IN6}:text='{esc(cl2)}':x=64:y=1268:fontsize=36:"
        "fontcolor=0xF0ECE0:alpha=0.96[v6d]",
        f"[v6d]drawtext=fontfile={SG7}:text='ODDCHAPTER':x=64:y=1768:fontsize=34:"
        "fontcolor=0xF0ECE0:alpha=0.92[v7]",
        f"[v7]drawtext=fontfile={IN6}:text='ILLUMINATI · BUKTI ATAU TAFSIR?':x=64:y=1820:"
        "fontsize=26:fontcolor=0xC6CEBE:alpha=0.85[v8]",
        f"[v8]drawbox=x=0:y=1912:w='1080*t/{dur:.3f}':h=6:color=0xC6602A@0.9:t=fill[vout]",
    ]
    af = (
        f"atrim=start={start}:end={end},asetpts=PTS-STARTPTS,"
        f"afade=t=in:st=0:d=0.35,afade=t=out:st={fade_out:.3f}:d=0.6"
    )
    out = OUT / f"EP01SB_{sid}.mp4"
    cmd = [
        FFMPEG, "-hide_banner", "-loglevel", "error", "-y", "-i", str(SRC),
        "-filter_complex", ";".join(chain), "-map", "[vout]", "-map", "0:a",
        "-af", af, "-t", f"{dur:.3f}",
        "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-profile:v", "high",
        "-pix_fmt", "yuv420p", "-r", "30",
        "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-ac", "2",
        "-movflags", "+faststart", str(out),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-1500:])
        sys.exit(f"gagal {sid}")
    print(f"{out.name}  {dur:.1f}s  {out.stat().st_size/1048576:.1f} MB")
    return {"id": sid, "file": out.name, "start": start, "end": end,
            "hook": f"{l1} {l2}", "duration": round(dur, 2)}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    only = sys.argv[1] if len(sys.argv) > 1 else None
    rows = []
    for s in SHORTS:
        if only and s[0] != only:
            continue
        rows.append(build(*s))
    (OUT / "shorts.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
