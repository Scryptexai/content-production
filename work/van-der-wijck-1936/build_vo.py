#!/usr/bin/env python3
"""Rangkai 10 klip TTS jadi satu VO + vo_alignment.json (waktu kata diperkirakan).

Tiap klip = satu kalimat (kecuali vo_04 = dua kalimat). Karena batas kalimat
diketahui pasti, waktu kata di dalam satu kalimat dibagi menurut bobot suku kata —
kesalahan tidak menumpuk lintas kalimat.
"""
import json, re, subprocess, wave
from pathlib import Path
import numpy as np
import imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe()
CASE = Path(__file__).resolve().parent
SR = 44100

SEGS = [
    ("vo_01", ["Pada 19 Oktober 1936, sebuah kapal mewah berhenti di tengah Laut Jawa.",
               "Enam menit kemudian, kapal itu sudah tidak ada."], 0.55),
    ("vo_02", ["Namanya Van der Wijck.", "Kapal uap milik perusahaan Belanda, KPM, dijuluki burung camar karena bodinya yang putih dan tenang."], 0.40),
    ("vo_03", ["Malam itu kapal berlayar dari Surabaya menuju Semarang, membawa ratusan penumpang dan seratus lima puluh ton besi."], 0.40),
    ("vo_04", ["Sekitar dua belas mil dari Pantai Brondong, kapal miring.",
               "Air masuk lebih cepat daripada pompa yang bisa membuangnya.",
               "Menurut laporan surat kabar saat itu, seluruh badan kapal hilang di bawah air hanya dalam enam menit."], 0.45),
    ("vo_05", ["Tidak ada kapal besar di dekat situ.", "Yang ada hanya perahu-perahu nelayan dari pantai."], 0.45),
    ("vo_06", ["Lima nelayan Brondong tercatat menyelamatkan seratus empat puluh lima orang:",
               "Kaslibin lima puluh tiga, Modwie tiga puluh dua, Troenoredjo dua puluh dua, Sratit dua puluh satu, Mardjiki tujuh belas."], 0.50),
    ("vo_07", ["Delapan pesawat amfibi Dornier dikirim dari Surabaya, dan sekitar dua puluh orang dievakuasi lewat udara."], 0.40),
    ("vo_08", ["Sang nakhoda selamat.", "Operator radionya, Uytermerk, tidak meninggalkan posnya.",
               "Sebuah plakat di Brondong masih menyebut namanya."], 0.60),
    ("vo_09", ["Jumlah korban tidak pernah bulat: satu koran menulis empat puluh dua hilang, sumber lain lima puluh delapan tewas, sampai tujuh puluh lima hilang."], 0.40),
    ("vo_10", ["Pada 2021, bangkainya ditemukan di kedalaman dua puluh delapan meter.",
               "Yang tidak pernah diperdebatkan: perahu kayu yang datang lebih dulu."], 0.90),
]

VOWELS = "aeiouy"


def load(path):
    p = subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-i", str(path),
                        "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"], capture_output=True)
    a = np.frombuffer(p.stdout, dtype="<i2").astype(np.float32) / 32768
    # buang keheningan di ujung (5 ms frame)
    fr = int(0.005 * SR)
    n = len(a) // fr
    e = np.array([np.sqrt((a[i * fr:(i + 1) * fr] ** 2).mean()) for i in range(n)])
    idx = np.where(e > max(0.004, e.max() * 0.02))[0]
    if len(idx):
        a = a[max(0, idx[0] - 4) * fr: min(n, idx[-1] + 6) * fr]
    return a


def syllables(word):
    w = re.sub(r"[^a-z]", "", word.lower())
    if not w:
        return 1
    n = sum(1 for ch in w if ch in VOWELS)
    n -= len(re.findall(r"[aeiouy]{2,}", w))
    return max(1, n + 1)


def main():
    parts, words, t = [], [], 0.0
    for key, sentences, gap_after in SEGS:
        a = load(CASE / "audio" / f"{key}.mp3")
        dur = len(a) / SR
        # bobot per kalimat -> batas kalimat di dalam klip
        wt = [sum(syllables(w) + 1 for w in s.split()) for s in sentences]
        total_w = sum(wt)
        bounds, acc = [], 0
        for w in wt[:-1]:
            acc += w
            bounds.append(t + dur * acc / total_w)
        bounds.append(t + dur)
        start = t
        for si, sent in enumerate(sentences):
            s0 = start if si == 0 else bounds[si - 1]
            s1 = bounds[si]
            toks = sent.split()
            wts = [syllables(w) + 1 for w in toks]
            tw = sum(wts)
            cursor = s0
            for tok, ww in zip(toks, wts):
                d = (s1 - s0) * ww / tw
                words.append({"word": tok, "start": round(cursor, 3), "end": round(cursor + d, 3)})
                cursor += d
        parts.append(a)
        parts.append(np.zeros(int(gap_after * SR), dtype=np.float32))
        t += dur + gap_after
    audio = np.concatenate(parts)
    # normalisasi ringan
    audio = audio / (np.max(np.abs(audio)) + 1e-9) * 0.92
    wav = CASE / "vo_van-der-wijck.wav"
    with wave.open(str(wav), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(audio, -1, 1) * 32767).astype("<i2").tobytes())
    subprocess.run([FF, "-y", "-hide_banner", "-loglevel", "error", "-i", str(wav),
                    "-b:a", "192k", str(CASE / "vo_van-der-wijck.mp3")], check=True)
    words = [w for w in words if w["word"].strip()]
    text = " ".join(w["word"] for w in words)
    json.dump({"source": "tts-internal voice-05", "duration": round(len(audio) / SR, 3),
               "text": text, "words": words},
              open(CASE / "vo_alignment.json", "w"), ensure_ascii=False, indent=1)
    print("durasi total", round(len(audio) / SR, 2), "s |", len(words), "kata")
    for k, s, g in [(a, b, c) for a, b, c in SEGS]:
        pass
    # ringkas batas segmen untuk case_cfg
    prev = 0.0
    for key, sentences, gap in SEGS:
        first = next(w for w in words if w["start"] >= prev - 1e-6)
        print(f"{key}: mulai {first['start']:.2f}")
        prev = first["start"] + 0.01


if __name__ == "__main__":
    main()
