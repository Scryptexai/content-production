"""
build_sfx.py — efek suara per segmen, dibuat di mesin ini (tidak ada unduhan).

    python3 tools/build_sfx.py EP01

Kenapa tidak pakai file sampel: sandbox ini tidak bisa mengambil audio dari
internet, dan sampel berlisensi tidak bisa diverifikasi. Semua efek di sini
disintesis dari osilator dan noise ffmpeg, lalu ditempatkan tepat di frame
segmennya memakai timing nyata.

Resep (semua deterministik):
  rustle  kain bergerak          noise putih, band 600-3.2k, tremolo 7 Hz
  gust    angin menekan          pink noise, lowpass 520, swell 2.4 s
  engine  mesin kapal uap        dua sine 58/87 Hz + noise rendah, swell
  clunk   pintu besi terkunci    sine 120 Hz turun cepat + noise burst
  tick    jam berhenti           dua tick metal, lalu hening
  page    halaman dibalik        noise band 2-6 kHz, 0.22 s
  boom    kejadian besar         sine 42 Hz, decay 2.2 s + noise rendah

Output: public/audio/<EP>/sfx.wav
"""

import json
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
from content_data import EPISODES  # noqa: E402

AUDIO = ROOT / "10_FILM" / "remotion" / "public" / "audio"
TIMING = ROOT / "10_FILM" / "remotion" / "src" / "timing.generated.json"


def ffmpeg():
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


# id -> list of (lavfi source, filter chain). chain sudah termasuk volume + fade.
def recipe(name, vol=1.0):
    v = vol
    if name == "rustle":
        return [
            ("anoisesrc=d=0.55:c=white:a=0.6",
             f"bandpass=f=1400:width_type=q:w=1.4,tremolo=f=7:d=0.8,"
             f"afade=t=in:st=0:d=0.06,afade=t=out:st=0.18:d=0.36,volume={0.5 * v}"),
        ]
    if name == "gust":
        return [
            ("anoisesrc=d=2.6:c=pink:a=0.7",
             f"lowpass=f=520,highpass=f=60,afade=t=in:st=0:d=1.1,"
             f"afade=t=out:st=1.2:d=1.4,volume={0.42 * v}"),
        ]
    if name == "engine":
        return [
            ("sine=f=58:d=2.4", f"afade=t=in:st=0:d=0.5,afade=t=out:st=1.4:d=1.0,volume={0.30 * v}"),
            ("sine=f=87:d=2.4", f"afade=t=in:st=0:d=0.5,afade=t=out:st=1.4:d=1.0,volume={0.14 * v}"),
            ("anoisesrc=d=2.4:c=pink:a=0.5", f"lowpass=f=240,afade=t=in:st=0:d=0.6,afade=t=out:st=1.5:d=0.9,volume={0.16 * v}"),
        ]
    if name == "clunk":
        return [
            ("sine=f=120:d=0.45", f"afade=t=in:st=0:d=0.004,afade=t=out:st=0.02:d=0.43,volume={0.85 * v}"),
            ("sine=f=310:d=0.16", f"afade=t=out:st=0.01:d=0.15,volume={0.22 * v}"),
            ("anoisesrc=d=0.10:c=white:a=0.7", f"bandpass=f=2200:width_type=q:w=1.2,afade=t=out:st=0.01:d=0.09,volume={0.28 * v}"),
        ]
    if name == "tick":
        return [
            ("sine=f=2600:d=0.035", f"afade=t=out:st=0.005:d=0.03,volume={0.35 * v}"),
            ("sine=f=2600:d=0.035", f"adelay=420|420,afade=t=out:st=0.005:d=0.03,volume={0.30 * v}"),
            ("sine=f=140:d=0.5", f"afade=t=out:st=0.05:d=0.45,volume={0.18 * v}"),
        ]
    if name == "page":
        return [
            ("anoisesrc=d=0.30:c=white:a=0.8", f"bandpass=f=3600:width_type=q:w=1.0,"
             f"afade=t=in:st=0:d=0.03,afade=t=out:st=0.05:d=0.25,volume={0.34 * v}"),
        ]
    if name == "boom":
        return [
            ("sine=f=42:d=2.4", f"afade=t=in:st=0:d=0.01,afade=t=out:st=0.05:d=2.35,volume={1.0 * v}"),
            ("anoisesrc=d=0.5:c=pink:a=0.6", f"lowpass=f=180,afade=t=out:st=0.04:d=0.46,volume={0.30 * v}"),
        ]
    raise SystemExit(f"resep suara tidak dikenal: {name}")


def build(ep):
    ep_id = ep["ep"]
    timing = json.loads(TIMING.read_text())[ep_id]
    plan = ep.get("sfx") or {}
    events = []
    for seg in timing["segments"]:
        name = plan.get(seg["key"])
        if name:
            events.append((seg["start"], name))
    events.sort()
    if not events:
        print(f"{ep_id}: tidak ada sfx")
        return

    args = [ffmpeg(), "-hide_banner", "-loglevel", "error", "-y"]
    chains = []
    labels = []
    idx = 0
    for start, name in events:
        for src, chain in recipe(name):
            args += ["-f", "lavfi", "-i", src]
            out = f"s{idx}"
            pre = f"[{idx}:a]{chain}"
            # adelay harus di ujung supaya fade tetap relatif ke awal efek
            chains.append(pre + f",adelay={int(round(start * 1000))}|{int(round(start * 1000))}[{out}]")
            labels.append(f"[{out}]")
            idx += 1
    graph = ";".join(chains) + ";" + "".join(labels) + f"amix=inputs={len(labels)}:normalize=0,atrim=0:{timing['total']},alimiter=limit=0.7[out]"
    dest = AUDIO / ep_id / "sfx.wav"
    dest.parent.mkdir(parents=True, exist_ok=True)
    args += ["-filter_complex", graph, "-map", "[out]", "-ac", "2", "-ar", "48000", "-c:a", "pcm_s16le", str(dest)]
    subprocess.run(args, check=True)
    print(f"{ep_id}: {len(events)} efek -> {dest.relative_to(ROOT)}  ({timing['total']}s)")


if __name__ == "__main__":
    ids = sys.argv[1:] or [e["ep"] for e in EPISODES]
    for ep in EPISODES:
        if ep["ep"] in ids and ep.get("sfx"):
            build(ep)
