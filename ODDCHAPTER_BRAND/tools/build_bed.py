"""
build_bed.py — ambience + drone + dentuman, satu file per episode.

Sebelumnya bed EP01 dibuat dengan perintah ffmpeg sekali pakai, jadi setiap kali
timing berubah (narasi direkam ulang), dentumannya jatuh di tempat yang salah.
Skrip ini membaca `timing.generated.json` — bukan angka yang ditulis tangan —
supaya dentuman selalu mendarat di titik balik yang sebenarnya.

    python3 tools/build_bed.py EP01

Tiga lapisan:
  amb    angin jauh (pink noise, lowpass) — mean sekitar -31 dB, tidak pernah dominan
  drone  dua sinus rendah yang naik pelan — memberi "ruang", bukan melodi
  hit    dentuman 42 Hz — hanya di tempat yang memang patah:
         hook (klimaks), cut ke pertanyaan, turn pertama, consequence, loop

Output: public/audio/<EP>/{amb,bed}.wav
"""

import json
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
AUDIO = ROOT / "10_FILM" / "remotion" / "public" / "audio"
TIMING = ROOT / "10_FILM" / "remotion" / "src" / "timing.generated.json"


def ffmpeg():
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def build(ep_id):
    tm = json.loads(TIMING.read_text())[ep_id]
    total = tm["total"] + 2.0
    segs = tm["segments"]
    by_part = {}
    for s in segs:
        by_part.setdefault(s.get("part") or s["kind"], []).append(s)

    # titik dentuman: klimaks (hook), cut ke pertanyaan, turn, consequence, loop
    hits = [segs[0]["start"] + 0.3]
    for name in ("tanya",):
        if name in by_part:
            hits.append(by_part[name][0]["start"])
    if "turn" in by_part:
        hits.append(by_part["turn"][0]["start"])
    if "consequence" in by_part:
        hits.append(by_part["consequence"][0]["start"])
    hits.append(by_part["loop"][0]["start"])
    hits = [round(h, 2) for h in sorted(set(hits))]

    outdir = AUDIO / ep_id
    outdir.mkdir(parents=True, exist_ok=True)

    # 1 · angin
    amb = outdir / "amb.wav"
    subprocess.run([
        ffmpeg(), "-y", "-v", "error",
        "-f", "lavfi", "-i",
        f"anoisesrc=d={total}:c=pink:a=0.5",
        "-af", (f"lowpass=f=480,highpass=f=45,tremolo=f=0.11:d=0.35,"
                f"afade=t=in:st=0:d=2.0,afade=t=out:st={total - 2.5}:d=2.4,volume=0.5"),
        "-ar", "48000", "-ac", "2", str(amb),
    ], check=True)

    # 2 · drone + dentuman
    inputs = ["-i", str(amb)]
    filters = []
    labels = ["0:a"]
    idx = 1

    drone_len = total
    for freq, vol in ((55, 0.10), (82.5, 0.055)):
        inputs += ["-f", "lavfi", "-i", f"sine=f={freq}:d={drone_len}"]
        filters.append(f"[{idx}:a]afade=t=in:st=0:d=3.0,afade=t=out:st={drone_len - 3}:d=3.0,"
                       f"volume={vol}[d{idx}]")
        labels.append(f"d{idx}")
        idx += 1

    for i, h in enumerate(hits):
        inputs += ["-f", "lavfi", "-i", f"sine=f=42:d=2.4"]
        filters.append(
            f"[{idx}:a]afade=t=out:st=0.25:d=2.0,volume=0.55,"
            f"adelay={int(h * 1000)}|{int(h * 1000)}[h{idx}]")
        labels.append(f"h{idx}")
        idx += 1

    mix = "".join(f"[{l}]" for l in labels)
    filters.append(f"{mix}amix=inputs={len(labels)}:normalize=0:duration=first,"
                   f"volume=2.2,alimiter=limit=0.9,afade=t=out:st={total - 2.0}:d=2.0[out]")

    bed = outdir / "bed.wav"
    subprocess.run([ffmpeg(), "-y", "-v", "error", *inputs,
                    "-filter_complex", ";".join(filters), "-map", "[out]",
                    "-ar", "48000", "-ac", "2", str(bed)], check=True)

    print(f"{ep_id}: amb {amb.stat().st_size // 1024} kB · bed {bed.stat().st_size // 1024} kB "
          f"· {total:.1f}s · hit di {', '.join(str(h) + 's' for h in hits)}")


if __name__ == "__main__":
    for ep in (sys.argv[1:] or ["EP01"]):
        build(ep)
