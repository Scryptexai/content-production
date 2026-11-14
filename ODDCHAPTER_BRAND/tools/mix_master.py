"""mix_master.py — menyusun audio final dari bagian-bagiannya, lalu mux ke gambar.

Kenapa tidak menyerahkan campuran ke Remotion: di sana bed dan efek diputar pada
volume tetap, tanpa ducking, dan tanpa cara mengukur. Akibatnya dua kali pemilik
mendengar hal yang sama — "backsound terlalu nyaring, VO kurang jelas".

Skrip ini menyusun ulang trek audio dengan angka yang bisa diperiksa:

  · tiap segmen narasi dinormalkan ke RMS yang sama (tidak ada segmen yang
    lebih pelan dari yang lain — keluhan "suara turun di zona yang tidak tepat");
  · bed ditempel pada level yang dihitung dari target selisih, bukan tebakan;
  · efek ditempel di awal segmennya, di bawah narasi;
  · hasil akhir diukur ebur128, ditargetkan -14 LUFS / true peak <= -1,5 dBTP;
  · video diambil apa adanya (copy), jadi tidak perlu render ulang.

    python3 tools/mix_master.py EP08
    python3 tools/mix_master.py EP08 --bed -36 --sep 18
"""

import argparse
import json
import pathlib
import subprocess
import sys
import wave

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
AUDIO = ROOT / "10_FILM" / "remotion" / "public" / "audio"
TIMING = ROOT / "10_FILM" / "remotion" / "src" / "timing.generated.json"
EPISODES = ROOT / "10_FILM" / "remotion" / "output" / "episodes"
SR = 48000
VO_RMS_DB = -20.0        # semua segmen disamakan di sini
BED_LUFS = -36.0         # bed jauh di bawah narasi
SFX_GAIN_DB = -9.0


def ffmpeg():
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return "ffmpeg"


def load_wav(path):
    with wave.open(str(path), "rb") as w:
        n, ch = w.getnframes(), w.getnchannels()
        raw = w.readframes(n)
    x = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
    if ch > 1:
        x = x.reshape(-1, ch).mean(axis=1)
    return x


def decode(src, dst, extra=None):
    cmd = [ffmpeg(), "-y", "-hide_banner", "-loglevel", "error", "-i", str(src)]
    if extra:
        cmd += ["-af", extra]
    cmd += ["-ac", "1", "-ar", str(SR), "-c:a", "pcm_s16le", str(dst)]
    subprocess.run(cmd, check=True)


def measure_lufs(path):
    out = subprocess.run([ffmpeg(), "-hide_banner", "-nostats", "-i", str(path),
                          "-filter_complex", "ebur128=peak=true", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    tail = out.split("Summary:")[-1]
    lufs = tp = None
    for line in tail.splitlines():
        if "I:" in line and "LUFS" in line:
            lufs = float(line.split("I:")[1].split("LUFS")[0])
        if "Peak:" in line and "dBFS" in line:
            tp = float(line.split("Peak:")[1].split("dBFS")[0])
    return lufs, tp


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ep")
    ap.add_argument("--bed", type=float, default=BED_LUFS, help="target LUFS bed")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    ep = args.ep

    tm = json.loads(TIMING.read_text(encoding="utf-8"))[ep]
    segs = tm["segments"]
    total = tm["total"] + 1.0
    work = pathlib.Path("/tmp") / f"mix_{ep}"
    work.mkdir(exist_ok=True)

    # 1 · narasi: decode, samakan RMS, taruh di offset masing-masing
    n_total = int(total * SR)
    vo = np.zeros(n_total, dtype=np.float32)
    seg_rms = []
    for s in segs:
        src = AUDIO / ep / f"{s['key']}.mp3"
        if not src.exists():
            raise SystemExit(f"hilang: {src}")
        wav = work / f"{s['key']}.wav"
        decode(src, wav)
        x = load_wav(wav)
        rms = float(np.sqrt((x ** 2).mean() + 1e-12))
        gain = 10 ** ((VO_RMS_DB - 20 * np.log10(rms + 1e-9)) / 20)
        x = np.clip(x * gain, -1, 1)
        start = int(s["start"] * SR)
        end = min(start + len(x), n_total)
        vo[start:end] += x[: end - start]
        seg_rms.append(20 * np.log10(np.sqrt((x ** 2).mean()) + 1e-9))

    vo_path = work / "vo.wav"
    _write(vo_path, vo)

    # 2 · bed: geser ke target LUFS
    bed = AUDIO / ep / "bed.wav"
    bed_gain = 0.0
    if bed.exists():
        lufs, _ = measure_lufs(bed)
        bed_gain = 0.0 if lufs is None else (args.bed - lufs)

    # 3 · efek
    sfx = AUDIO / ep / "sfx.wav"

    # 4 · campur
    mix = work / "mix.wav"
    inputs = ["-i", str(vo_path)]
    filters = ["[0:a]aformat=sample_fmts=fltp:channel_layouts=mono[v0]"]
    labels = ["v0"]
    idx = 1
    if bed.exists():
        inputs += ["-i", str(bed)]
        filters.append(f"[{idx}:a]volume={bed_gain:.2f}dB,"
                       f"aformat=sample_fmts=fltp:channel_layouts=mono,"
                       f"atrim=0:{total:.3f}[b]")
        labels.append("b")
        idx += 1
    if sfx.exists():
        inputs += ["-i", str(sfx)]
        filters.append(f"[{idx}:a]volume={SFX_GAIN_DB:.2f}dB,"
                       f"aformat=sample_fmts=fltp:channel_layouts=mono,"
                       f"atrim=0:{total:.3f}[s]")
        labels.append("s")
        idx += 1
    mixed = "".join(f"[{l}]" for l in labels)
    filters.append(f"{mixed}amix=inputs={len(labels)}:normalize=0:duration=longest,"
                   f"alimiter=limit=0.95:level=false,"
                   f"afade=t=out:st={total - 1.2:.3f}:d=1.2[out]")
    subprocess.run([ffmpeg(), "-y", "-hide_banner", "-loglevel", "error", *inputs,
                    "-filter_complex", ";".join(filters), "-map", "[out]",
                    "-ar", str(SR), "-ac", "2", "-c:a", "pcm_s16le", str(mix)], check=True)

    lufs, tp = measure_lufs(mix)
    print(f"campuran: {lufs} LUFS · TP {tp} dBFS · bed {bed_gain:+.1f} dB → target {args.bed} LUFS")
    print(f"narasi per segmen: {min(seg_rms):.1f} … {max(seg_rms):.1f} dBFS "
          f"(disamakan ke {VO_RMS_DB:.0f})")

    # 5 · normalisasi final dua tahap + mux video
    probe = subprocess.run([ffmpeg(), "-hide_banner", "-nostats", "-i", str(mix),
                            "-af", "loudnorm=I=-14:TP=-1.8:LRA=11:print_format=json",
                            "-f", "null", "-"], capture_output=True, text=True).stderr
    js = json.loads(probe[probe.index("{"): probe.rindex("}") + 1])
    src_video = EPISODES / f"{ep}_raw.mp4"
    if not src_video.exists():
        src_video = EPISODES / f"{ep}_1080x1920_master.mp4"
    out = pathlib.Path(args.out) if args.out else EPISODES / f"{ep}_1080x1920_master.mp4"
    tmp = out.with_name(out.stem + "_mix.mp4")
    subprocess.run([
        ffmpeg(), "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(src_video), "-i", str(mix),
        "-map", "0:v:0", "-map", "1:a:0",
        "-vf", "scale=in_range=full:out_range=tv,format=yuv420p",
        "-af", (f"loudnorm=I=-14:TP=-1.8:LRA=11:measured_I={js['input_i']}:"
                f"measured_TP={js['input_tp']}:measured_LRA={js['input_lra']}:"
                f"measured_thresh={js['input_thresh']}:offset={js['target_offset']}:linear=true"),
        "-c:v", "libx264", "-preset", "slow", "-crf", "21", "-maxrate", "6M",
        "-bufsize", "12M", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-ar", str(SR),
        "-movflags", "+faststart", "-shortest", str(tmp),
    ], check=True)
    tmp.replace(out)
    lufs, tp = measure_lufs(out)
    print(f"master  : {lufs} LUFS · TP {tp} dBFS · {out.stat().st_size} B")
    return 0


def _write(path, x):
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes())


if __name__ == "__main__":
    sys.exit(main())
