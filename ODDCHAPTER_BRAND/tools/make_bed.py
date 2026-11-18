"""
make_bed.py — bed musik + sfx kartu untuk satu episode, disintesis (bukan stok).

Dipakai build_longform.py: `music` = bed, `sfx` = dentuman kartu.
Semua dari filter ffmpeg, jadi tidak ada urusan lisensi dan tiap episode bisa
punya nada dasar sendiri.

    python3 tools/make_bed.py --ep SB-EP02 --dur 520 --root 62
"""
import argparse
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent


def ff(*cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        raise SystemExit("ffmpeg gagal: " + " ".join(cmd[:8]) + "\n" + r.stderr[-1200:])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ep", required=True)
    ap.add_argument("--dur", type=float, default=520.0)
    ap.add_argument("--root", type=float, default=62.0, help="frekuensi dasar drone (Hz)")
    args = ap.parse_args()

    out = ROOT / "10_FILM" / "remotion" / "public" / "audio" / args.ep
    out.mkdir(parents=True, exist_ok=True)
    bed, sfx = out / "bed.wav", out / "sfx.wav"
    d = f"{args.dur:.1f}"
    f0 = args.root

    # tiga sinus rendah (oktaf + kuint) yang saling mengayun pelan + angin jauh
    graph = (
        f"sine=frequency={f0}:sample_rate=48000:duration={d}[a0];"
        f"sine=frequency={f0 * 1.5:.2f}:sample_rate=48000:duration={d}[a1];"
        f"sine=frequency={f0 * 2.0:.2f}:sample_rate=48000:duration={d}[a2];"
        f"anoisesrc=color=pink:sample_rate=48000:duration={d}:amplitude=0.55,"
        f"lowpass=f=420,highpass=f=60[amb];"
        f"[a0]volume=0.30,tremolo=f=0.10:d=0.55[s0];"
        f"[a1]volume=0.16,tremolo=f=0.13:d=0.60[s1];"
        f"[a2]volume=0.09,tremolo=f=0.17:d=0.50[s2];"
        f"[amb]volume=0.22,tremolo=f=0.11:d=0.35[amb2];"
        f"[s0][s1][s2][amb2]amix=inputs=4,volume=4,"
        f"aformat=channel_layouts=stereo,"
        f"afade=t=in:st=0:d=12,afade=t=out:st={max(0.0, args.dur - 8):.1f}:d=8,"
        f"loudnorm=I=-26:TP=-6:LRA=9[out]"
    )
    ff("ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
       "-filter_complex", graph, "-map", "[out]", "-ar", "48000", "-ac", "2",
       "-c:a", "pcm_s16le", str(bed))

    # dentuman kartu: klik pendek + thump 48 Hz yang cepat mati
    hit = (
        "anoisesrc=color=white:sample_rate=48000:duration=0.9:amplitude=0.9,"
        "highpass=f=1200,afade=t=out:st=0:d=0.9:curve=exp,volume=0.30[air];"
        "sine=frequency=48:sample_rate=48000:duration=0.9,"
        "afade=t=out:st=0:d=0.55:curve=exp,volume=0.95[low];"
        "[air][low]amix=inputs=2,volume=2,"
        "aecho=0.7:0.6:60|130:0.28|0.16,"
        "aformat=channel_layouts=stereo,loudnorm=I=-20:TP=-3:LRA=7[out]"
    )
    ff("ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
       "-filter_complex", hit, "-map", "[out]", "-ar", "48000", "-ac", "2",
       "-c:a", "pcm_s16le", str(sfx))

    for f in (bed, sfx):
        print(f"{f.relative_to(ROOT)}  {f.stat().st_size / 1e6:.1f} MB")


if __name__ == "__main__":
    sys.exit(main())
