"""voice_consistency.py — memastikan semua segmen satu episode dibawakan suara yang sama.

Keluhan pemilik (15 Nov 2026): "setiap scene vo-nya beda, tidak sama" — dan dia
benar; itu tidak bisa dilihat dari nama berkas, hanya dari suara. Skrip ini
mengukur ciri akustik tiap segmen lalu membandingkannya dengan median episode.

Ciri yang dipakai (semuanya murah dan cukup untuk menangkap "orang lain"):
  f0      median frekuensi dasar (Hz)      — tinggi/rendah suara
  cent    spectral centroid (Hz)           — terang/gelap timbre
  roll    rolloff 85% (Hz)                 — seberapa banyak energi tinggi
  zcr     zero-crossing rate               — kekasaran konsonan
  tilt    beda energi 0-1 kHz vs 2-6 kHz   — "dada" vs "kepala"

Kalau satu segmen menyimpang jauh dari median yang lain, itu bukan variasi
emosi — itu suara lain. Ambang di bawah dipilih dari data: segmen satu voice
menyimpang <12%, segmen yang beda orang >35%.

    python3 tools/voice_consistency.py EP08
"""

import pathlib
import subprocess
import sys
import wave

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
AUDIO = ROOT / "10_FILM" / "remotion" / "public" / "audio"
SR = 16000
WIN, HOP = 512, 256
F0_MIN, F0_MAX = 60, 450
# Ambang per ciri. ZCR dan rolloff ikut berubah karena isi kalimat (konsonan,
# desis), jadi keduanya tidak dipakai sebagai penentu — hanya dilaporkan.
TOL = {"f0": 0.18, "cent": 0.35, "tilt": 4.0}


def ffmpeg():
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return "ffmpeg"


def load(path):
    tmp = pathlib.Path("/tmp") / (pathlib.Path(path).stem + "_vc.wav")
    subprocess.run([ffmpeg(), "-y", "-hide_banner", "-loglevel", "error",
                    "-i", str(path), "-ac", "1", "-ar", str(SR), str(tmp)], check=True)
    with wave.open(str(tmp), "rb") as w:
        raw = w.readframes(w.getnframes())
    x = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
    x = x / (np.abs(x).max() + 1e-9)
    return x


def features(x):
    n = 1 + max(0, (len(x) - WIN) // HOP)
    idx = np.arange(WIN)[None, :] + HOP * np.arange(n)[:, None]
    fr = x[idx]
    rms = np.sqrt((fr ** 2).mean(axis=1) + 1e-12)
    cen, roll, zcr, f0 = [], [], [], []
    spec = np.abs(np.fft.rfft(fr * np.hanning(WIN), axis=1))
    freqs = np.fft.rfftfreq(WIN, 1 / SR)
    for i in range(n):
        if rms[i] < 0.02:          # lewati hening
            continue
        s = spec[i]
        tot = s.sum() + 1e-9
        cen.append((s * freqs).sum() / tot)
        cs = np.cumsum(s)
        roll.append(freqs[np.searchsorted(cs, 0.85 * cs[-1])])
        zcr.append(np.mean(np.abs(np.diff(np.sign(fr[i]))) > 0) / 2)
        f = fr[i] - fr[i].mean()
        ac = np.correlate(f, f, mode="full")[len(f) - 1:]
        lo, hi = int(SR / F0_MAX), int(SR / F0_MIN)
        seg = ac[lo:hi]
        if len(seg) and ac[0] > 0:
            lag = int(np.argmax(seg)) + lo
            if ac[lag] / ac[0] > 0.3:
                f0.append(SR / lag)
    low = spec[:, (freqs >= 80) & (freqs <= 1000)].sum(axis=1).mean()
    high = spec[:, (freqs >= 2000) & (freqs <= 6000)].sum(axis=1).mean() + 1e-9
    return {
        "f0": float(np.median(f0)) if f0 else 0.0,
        "cent": float(np.median(cen)) if cen else 0.0,
        "roll": float(np.median(roll)) if roll else 0.0,
        "zcr": float(np.median(zcr)) if zcr else 0.0,
        "tilt": float(20 * np.log10(low / high)),
    }


def main():
    ep = sys.argv[1] if len(sys.argv) > 1 else "EP08"
    d = AUDIO / ep
    files = sorted(p for p in d.glob("*.mp3"))
    if not files:
        raise SystemExit(f"tidak ada mp3 di {d}")
    rows = [(f.stem, features(load(f))) for f in files]
    keys = ["f0", "cent", "roll", "zcr", "tilt"]
    judged = ["f0", "cent", "tilt"]
    med = {k: float(np.median([r[k] for _, r in rows])) for k in keys}

    print(f"{ep} · {len(rows)} segmen · median: "
          + "  ".join(f"{k}={med[k]:.1f}" for k in keys))
    bad = []
    for name, r in rows:
        out = []
        for k in judged:
            if k == "tilt":
                d = r[k] - med[k]
                limit = TOL[k]
            else:
                d = (r[k] - med[k]) / (abs(med[k]) + 1e-9) * 100
                limit = TOL[k] * 100
            if abs(d) > limit:
                out.append((k, d, limit))
        flag = "OK" if not out else "BEDA"
        print(f"  {name:16s} f0={r['f0']:6.1f} cent={r['cent']:7.0f} tilt={r['tilt']:6.1f} "
              f"| " + (", ".join(f"{k} {d:+.1f}{'%' if k != 'tilt' else 'dB'}" for k, d, _ in out) or "-")
              + f"  {flag}")
        for k, d, _ in out:
            bad.append((name, k, d))
    if bad:
        print(f"\nTOLAK: {len(bad)} penyimpangan — kemungkinan suara berbeda:")
        for name, k, v in bad:
            unit = "dB" if k == "tilt" else "%"
            print(f"  ✗ {name}: {k} {v:+.1f}{unit}")
        sys.exit(1)
    print("\nLULUS: semua segmen dalam ambang — satu suara.")


if __name__ == "__main__":
    main()
