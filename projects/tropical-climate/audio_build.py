#!/usr/bin/env python3
"""
Musik + sound design untuk "Kulit Tropis, Formula Subtropis".

Semua audio disintesis di sini (tidak ada aset musik pihak ketiga):
  - ambient bed: drone + pad akor per adegan, crossfade equal-power
  - sub pulse: detak pelan tiap 2,4 detik
  - whoosh  : noise band-pass sweep di setiap batas adegan
  - impact  : sub drop + klik di titik reveal data
  - riser   : noise naik 4 detik sebelum dua puncak

Lalu dicampur: narasi + musik (ducking sidechain) + SFX, loudnorm -16 LUFS.
"""
import os
import subprocess

import numpy as np

ROOT = os.path.dirname(os.path.abspath(__file__))
FF = open(os.path.join(ROOT, "..", "..", ".ffmpeg-path")).read().strip()
SR = 48000
BUILD = os.path.join(ROOT, "build")
os.makedirs(BUILD, exist_ok=True)

# lead/tail identik dengan render.py
SCENES = [
    ("vo-01.mp3", 1.60, 0.45),
    ("vo-02.mp3", 0.30, 0.40),
    ("vo-03.mp3", 0.30, 0.45),
    ("vo-04.mp3", 0.30, 0.40),
    ("vo-05.mp3", 0.30, 0.40),
    ("vo-06.mp3", 0.30, 0.40),
    ("vo-07.mp3", 0.30, 0.45),
    ("vo-08.mp3", 0.30, 0.40),
    ("vo-09.mp3", 0.30, 0.40),
    ("vo-10.mp3", 0.30, 1.10),
]

# ---------------------------------------------------------------- helpers
def run(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError(p.stderr[-3000:])


def dur_of(path):
    out = subprocess.run([FF, "-hide_banner", "-i", path], capture_output=True, text=True).stderr
    for line in out.splitlines():
        if "Duration:" in line:
            h, m, s = line.split("Duration:")[1].split(",")[0].strip().split(":")
            return int(h) * 3600 + int(m) * 60 + float(s)
    raise RuntimeError("dur?")


def to_wav(src, dst, extra=None):
    cmd = [FF, "-y", "-loglevel", "error", "-i", src]
    if extra:
        cmd += extra
    cmd += ["-ar", str(SR), "-ac", "2", "-c:a", "pcm_s16le", dst]
    run(cmd)


def note(name):
    """Frekuensi nada, mis. 'A2'."""
    base = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3, "E": 4, "F": 5,
            "F#": 6, "Gb": 6, "G": 7, "G#": 8, "Ab": 8, "A": 9, "A#": 10,
            "Bb": 10, "B": 11}
    n, octv = name[:-1], int(name[-1])
    midi = 12 * (octv + 1) + base[n]
    return 440.0 * 2 ** ((midi - 69) / 12)


def one_pole_lp(x, cutoff_hz):
    """Lowpass satu kutub, cutoff bisa array (per sampel)."""
    a = np.exp(-2 * np.pi * np.asarray(cutoff_hz) / SR)
    y = np.empty_like(x)
    acc = 0.0
    for i in range(len(x)):
        acc = (1 - a[i]) * x[i] + a[i] * acc
        y[i] = acc
    return y


def equal_power(n):
    t = np.linspace(0, 1, n, endpoint=False)
    return np.sin(t * np.pi / 2)


# ---------------------------------------------------------------- 1. VO
print("1/5  menyusun narasi …")
durs = []
for vo, lead, tail in SCENES:
    durs.append(lead + dur_of(os.path.join(ROOT, "audio", vo)) + tail)
starts = np.concatenate([[0.0], np.cumsum(durs)[:-1]])
TOTAL = float(sum(durs))
print(f"      total {TOTAL:.2f}s, {len(SCENES)} adegan")

parts = []
for (vo, lead, tail), d in zip(SCENES, durs):
    parts.append(np.zeros(int(lead * SR)))
    tmp = os.path.join(BUILD, "vo_tmp.wav")
    to_wav(os.path.join(ROOT, "audio", vo), tmp)
    parts.append(tmp)
    parts.append(np.zeros(int(tail * SR)))

# gabung narasi dengan concat demuxer (lebih aman untuk puluhan ribu sampel)
vo_list = os.path.join(BUILD, "vo_list.txt")
tmp_sil = os.path.join(BUILD, "sil.wav")
np_sil = np.zeros(int(max(d for d in durs) * SR))
import wave
with wave.open(tmp_sil, "wb") as w:
    w.setnchannels(2), w.setsampwidth(2), w.setframerate(SR)
    w.writeframes((np.zeros((int(0.001 * SR), 2))).astype(np.int16).tobytes())

with open(vo_list, "w") as f:
    for (vo, lead, tail) in SCENES:
        # silence dibuat per segmen
        for amt, tag in ((lead, "lead"), (tail, "tail")):
            p = os.path.join(BUILD, f"sil_{tag}_{amt:.2f}.wav")
            if not os.path.exists(p):
                n = int(amt * SR)
                with wave.open(p, "wb") as w:
                    w.setnchannels(2), w.setsampwidth(2), w.setframerate(SR)
                    w.writeframes(np.zeros((n, 2), dtype=np.int16).tobytes())
            f.write(f"file '{p}'\n")
        wv = os.path.join(BUILD, os.path.basename(vo).replace(".mp3", ".wav"))
        if not os.path.exists(wv):
            to_wav(os.path.join(ROOT, "audio", vo), wv)
        f.write(f"file '{wv}'\n")

vo_full = os.path.join(BUILD, "vo_full.wav")
run([FF, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", vo_list,
     "-ar", str(SR), "-ac", "2", "-c:a", "pcm_s16le", vo_full])
VO_DUR = dur_of(vo_full)
print(f"      vo_full: {VO_DUR:.2f}s")
TOTAL = VO_DUR
N = int(TOTAL * SR)
t = np.arange(N) / SR

# ---------------------------------------------------------------- 2. musik
print("2/5  musik …")
# akor per adegan (resolusi akhir di A minor)
CHORDS = [
    ["A2", "E3", "A3", "C4"],
    ["A2", "E3", "A3", "C4", "E4"],
    ["F2", "C3", "A3", "C4"],
    ["F2", "C3", "A3", "F4"],
    ["D3", "A3", "D4", "F4"],
    ["E2", "B2", "E3", "G3"],
    ["F2", "Ab3", "C4", "F4"],          # tensi
    ["G2", "D3", "Bb3", "D4"],
    ["A2", "E3", "A3", "C4", "E4"],
    ["A2", "E3", "A3", "C4"],
]

bed = np.zeros(N)
XF = 1.4  # detik crossfade
for i, chord in enumerate(CHORDS):
    s = starts[i]
    e = s + durs[i]
    a, b = int(max(0, (s - XF / 2)) * SR), int(min(TOTAL, e + XF / 2) * SR)
    seg_n = b - a
    if seg_n <= 0:
        continue
    tt = np.arange(seg_n) / SR
    # envelope equal-power per segmen
    env = np.ones(seg_n)
    fade = int(XF * SR)
    if fade * 2 < seg_n:
        env[:fade] = equal_power(fade)
        env[-fade:] = equal_power(fade)[::-1]
    sig = np.zeros(seg_n)
    for j, nm in enumerate(chord):
        f = note(nm)
        amp = 0.20 / (1 + 0.45 * j)
        # dua osilator detune + sub
        sig += amp * np.sin(2 * np.pi * f * tt)
        sig += amp * 0.7 * np.sin(2 * np.pi * f * 1.0015 * tt + 0.6)
        if j < 2:
            sig += amp * 0.35 * np.sin(2 * np.pi * f * 0.5 * tt)
    # tremolo sangat lambat
    sig *= 1.0 + 0.10 * np.sin(2 * np.pi * 0.06 * tt)
    bed[a:b] += sig * env

# air / ruang: noise lowpass + LFO
rng = np.random.default_rng(3)
air = rng.standard_normal(N) * 0.5
air = one_pole_lp(air, np.full(N, 850.0))
air *= 0.020 * (0.7 + 0.3 * np.sin(2 * np.pi * 0.045 * t))
bed += air

# sub pulse tiap 2,4 s
pulse = np.zeros(N)
period = 2.4
for k in range(int(TOTAL / period) + 1):
    s = int(k * period * SR)
    ln = int(0.7 * SR)
    if s + ln >= N:
        break
    tt = np.arange(ln) / SR
    pulse[s:s + ln] += 0.045 * np.sin(2 * np.pi * 55 * tt) * np.exp(-tt * 6)

bed += pulse

# normalisasi + fade global
bed /= max(1e-9, np.max(np.abs(bed)))
fade_in = int(2.0 * SR)
bed[:fade_in] *= equal_power(fade_in)
fade_out = int(3.5 * SR)
bed[-fade_out:] *= equal_power(fade_out)[::-1]
bed *= 0.55

music_st = np.stack([bed, np.roll(bed, 240)], axis=1)  # sedikit lebar stereo
music_path = os.path.join(BUILD, "music.wav")
with wave.open(music_path, "wb") as w:
    w.setnchannels(2), w.setsampwidth(2), w.setframerate(SR)
    w.writeframes((np.clip(music_st, -1, 1) * 32767).astype(np.int16).tobytes())

# ---------------------------------------------------------------- 3. SFX
print("3/5  sound design …")
sfx = np.zeros((N, 2))
rng = np.random.default_rng(11)


def place(sig, at, gain=1.0, pan=0.0):
    s = int(at * SR)
    n = len(sig)
    if s < 0 or s >= N:
        return
    n = min(n, N - s)
    l = gain * (1 - max(0, pan))
    r = gain * (1 + min(0, pan))
    sfx[s:s + n, 0] += sig[:n] * l
    sfx[s:s + n, 1] += sig[:n] * r


def whoosh(dur=0.62):
    n = int(dur * SR)
    tt = np.arange(n) / SR
    noise = rng.standard_normal(n)
    env = np.sin(np.pi * tt / dur) ** 2.2
    cut = 300 + 2600 * (tt / dur) ** 0.8
    y = one_pole_lp(noise, cut)
    return y * env


def impact(dur=1.4):
    n = int(dur * SR)
    tt = np.arange(n) / SR
    sub = np.sin(2 * np.pi * 52 * tt) * np.exp(-tt * 3.2)
    click = rng.standard_normal(n) * np.exp(-tt * 55) * 0.5
    return (sub * 0.9 + click)


def riser(dur=4.0):
    n = int(dur * SR)
    tt = np.arange(n) / SR
    noise = rng.standard_normal(n)
    cut = 200 + 5200 * (tt / dur) ** 2
    y = one_pole_lp(noise, cut)
    env = (tt / dur) ** 2.4
    return y * env


# whoosh di setiap batas adegan
for st in starts[1:]:
    place(whoosh(0.62), st - 0.30, 0.30, pan=-0.15)

# impact di titik reveal
for st, off, g in [(starts[1], 0.85, 0.42), (starts[6], 0.55, 0.55),
                   (starts[7], 1.10, 0.38), (starts[9], 0.30, 0.30)]:
    place(impact(1.5), st + off, g)

# riser sebelum dua puncak
place(riser(4.2), starts[6] - 4.2, 0.26)
place(riser(3.0), starts[9] - 3.0, 0.20)

sfx_path = os.path.join(BUILD, "sfx.wav")
with wave.open(sfx_path, "wb") as w:
    w.setnchannels(2), w.setsampwidth(2), w.setframerate(SR)
    w.writeframes((np.clip(sfx, -1, 1) * 32767).astype(np.int16).tobytes())

# ---------------------------------------------------------------- 4. mix
print("4/5  mixing (ducking musik di bawah narasi) …")
mix = os.path.join(BUILD, "mix.wav")
run([
    FF, "-y", "-loglevel", "error",
    "-i", vo_full, "-i", music_path, "-i", sfx_path,
    "-filter_complex",
    # musik: sedikit dipotong low-end, ducking oleh narasi
    "[1:a]volume=0.62,highpass=f=55,lowpass=f=9000[m0];"
    "[m0][0:a]sidechaincompress=threshold=0.045:ratio=7:attack=18:release=340:makeup=1.0[mduck];"
    "[2:a]volume=0.85[sx];"
    "[mduck][sx]amix=inputs=2:duration=first:normalize=0[room];"
    # narasi di atas
    "[0:a][room]amix=inputs=2:duration=first:normalize=0[pre];"
    "[pre]loudnorm=I=-16:TP=-1.5:LRA=11[aout]",
    "-map", "[aout]", "-c:a", "pcm_s16le", mix,
])
print(f"      mix: {dur_of(mix):.2f}s")

# ---------------------------------------------------------------- 5. mux
print("5/5  muxing ke video …")
src = os.path.join(ROOT, "out", "tropical-subtropis-web.mp4")
final = os.path.join(ROOT, "out", "tropical-subtropis-final.mp4")
run([
    FF, "-y", "-loglevel", "error",
    "-i", src, "-i", mix,
    "-map", "0:v", "-map", "1:a",
    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
    "-shortest", "-movflags", "+faststart", final,
])
print(f"selesai → {final} ({os.path.getsize(final)/1e6:.1f} MB)")
