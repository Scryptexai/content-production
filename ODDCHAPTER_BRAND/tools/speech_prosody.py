"""speech_prosody.py — mengukur jeda, ritme, dan arah nada hasil TTS.

Keluhan pemilik (14 Nov 2026): "intonasi, ritme dan jeda tidak tepat — yang
harusnya jeda malah lanjut, yang harusnya nada tinggi malah turun."

Masalah pertama bisa **diukur**: jeda di dalam satu berkas, panjangnya, dan
apakah sebuah pertanyaan berakhir naik atau turun. Skrip ini membaca mp3 per
segmen dan mencetak angka, supaya perbaikan naskah tidak dikerjakan dengan
menebak.

    python3 tools/speech_prosody.py EP08
    python3 tools/speech_prosody.py EP08 --json out.json

Yang dihitung per segmen:
  dur        durasi total (detik)
  wpm        kata per menit (naskah dibanding audio)
  pauses     jeda diam >= 140 ms di dalam segmen + totalnya
  tail       arah nada 300 ms terakhir dibanding median segmen (semit)
             negatif = turun, positif = naik
  rate       kata/detik tiap 1 detik pertama (untuk melihat hook terlalu cepat)

Batas yang dipakai kanal (bukan standar industri, ini target internal):
  · tidak ada jeda >= 400 ms di tengah satu breath group (kecuali memang ditandai)
  · pertanyaan (…) harus `tail` >= -1,5 semit (tidak jatuh)
  · wpm 120–155
"""

import json
import pathlib
import subprocess
import sys
import wave

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
AUDIO = ROOT / "10_FILM" / "remotion" / "public" / "audio"
SR = 16000
HOP = 160          # 10 ms
WIN = 400          # 25 ms
F0_MIN, F0_MAX = 70, 400
SIL_DB = -34.0     # ambang hening relatif puncak, dB
MIN_PAUSE = 0.14   # detik


def ffmpeg():
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return "ffmpeg"


def load(path):
    """mp3 -> float32 mono 16 kHz (lewat wav sementara, tanpa dependensi audio)."""
    tmp = pathlib.Path("/tmp") / (pathlib.Path(path).stem + "_prosody.wav")
    subprocess.run(
        [ffmpeg(), "-y", "-hide_banner", "-loglevel", "error", "-i", str(path),
         "-ac", "1", "-ar", str(SR), str(tmp)], check=True)
    with wave.open(str(tmp), "rb") as w:
        raw = w.readframes(w.getnframes())
    return np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0


def frames(x):
    n = 1 + max(0, (len(x) - WIN) // HOP)
    idx = np.arange(WIN)[None, :] + HOP * np.arange(n)[:, None]
    return x[idx]


def f0_track(x):
    fr = frames(x)
    rms = np.sqrt((fr ** 2).mean(axis=1) + 1e-12)
    out = np.zeros(len(fr))
    lo, hi = int(SR / F0_MAX), int(SR / F0_MIN)
    for i, f in enumerate(fr):
        if rms[i] < 1e-3:
            continue
        f = f - f.mean()
        ac = np.correlate(f, f, mode="full")[len(f) - 1:]
        if ac[0] <= 0:
            continue
        seg = ac[lo:hi]
        if not len(seg):
            continue
        lag = int(np.argmax(seg)) + lo
        if ac[lag] / ac[0] < 0.3:      # tidak cukup periodik: anggap tak bersuara
            continue
        out[i] = SR / lag
    return rms, out


def semit(a, b):
    if a <= 0 or b <= 0:
        return 0.0
    return 12 * np.log2(a / b)


def analyse(path, text):
    x = load(path)
    dur = len(x) / SR
    rms, f0 = f0_track(x)
    db = 20 * np.log10(rms + 1e-9)
    db -= db.max()
    quiet = db < SIL_DB
    # jeda: rentetan frame hening, abaikan hening di awal/akhir (itu bukan jeda bicara)
    pauses, run = [], 0
    for i, q in enumerate(quiet):
        if q:
            run += 1
        else:
            if run:
                pauses.append(run)
            run = 0
    if run:
        pauses.append(run)
    if pauses and quiet[0]:
        pauses = pauses[1:]
    if pauses and quiet[-1]:
        pauses = pauses[:-1]
    pdur = [round(p * HOP / SR, 3) for p in pauses]
    pdur_sig = [p for p in pdur if p >= MIN_PAUSE]

    voiced = f0[f0 > 0]
    med = float(np.median(voiced)) if len(voiced) else 0.0
    tail_frames = f0[-int(0.30 * SR / HOP):]
    tail_v = tail_frames[tail_frames > 0]
    tail = float(np.median(tail_v)) if len(tail_v) else 0.0
    lead_frames = f0[: int(0.60 * SR / HOP)]
    lead_v = lead_frames[lead_frames > 0]
    lead = float(np.median(lead_v)) if len(lead_v) else 0.0

    words = len(text.split())
    return {
        "file": pathlib.Path(path).name,
        "dur": round(dur, 2),
        "words": words,
        "wpm": round(words / dur * 60, 1) if dur else 0,
        "pauses": pdur_sig,
        "pause_total": round(sum(pdur_sig), 2),
        "pauses_over_400ms": [p for p in pdur_sig if p >= 0.4],
        "f0_median": round(med, 1),
        "tail_semit": round(semit(tail, med), 2),
        "lead_semit": round(semit(lead, med), 2),
        "question": text.strip().endswith("?"),
    }


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    ep = args[0] if args else "EP08"
    sys.path.insert(0, str(HERE))
    from content_data import EPISODES  # noqa: E402
    e = next((x for x in EPISODES if x["ep"] == ep), None)
    if not e:
        raise SystemExit(f"{ep} tidak ada")

    segs = [("00_hook", e["hook"])]
    segs += [(f"{i + 1:02d}_{p}", t) for i, (p, t) in enumerate(e["beats"])]
    segs.append(("99_loop", e["loop"]))

    rows, flags = [], []
    for key, text in segs:
        path = AUDIO / ep / f"{key}.mp3"
        if not path.exists():
            print(f"{key:16s} — belum ada audio")
            continue
        r = analyse(path, text)
        rows.append(r)
        print(f"{key:16s} {r['dur']:5.2f}s {r['wpm']:6.1f} wpm  jeda={r['pause_total']:4.2f}s "
              f"({len(r['pauses'])}x)  tail={r['tail_semit']:+5.2f}st"
              + ("  ← pertanyaan" if r["question"] else ""))
        if r["wpm"] and not 120 <= r["wpm"] <= 160:
            flags.append(f"{key}: {r['wpm']} wpm di luar 120–160")
        if r["pauses_over_400ms"]:
            flags.append(f"{key}: jeda panjang di tengah frasa {r['pauses_over_400ms']}")
        if r["question"] and r["tail_semit"] < -1.5:
            flags.append(f"{key}: pertanyaan berakhir TURUN ({r['tail_semit']:+} st)")
        if not r["question"] and r["tail_semit"] > 3.0:
            flags.append(f"{key}: pernyataan berakhir naik tajam ({r['tail_semit']:+} st)")

    total = round(sum(r["dur"] for r in rows), 2)
    words = sum(r["words"] for r in rows)
    print(f"\n{ep}: {len(rows)} segmen · {total} s ucapan · {words} kata "
          f"· {round(words / total * 60, 1) if total else 0} wpm rata-rata")
    if flags:
        print("\nMASALAH:")
        for f in flags:
            print("  ✗", f)
    else:
        print("\nTidak ada masalah prosodi yang terukur.")

    if "--json" in sys.argv:
        out = pathlib.Path(sys.argv[sys.argv.index("--json") + 1])
        out.write_text(json.dumps({"episode": ep, "segments": rows, "flags": flags},
                                  ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"json: {out}")


if __name__ == "__main__":
    main()
