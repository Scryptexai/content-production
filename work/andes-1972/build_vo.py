#!/usr/bin/env python3
"""Rangkai 10 klip TTS jadi satu VO + vo_alignment.json (waktu kata diperkirakan).

Uji format Curiosity Loop (AK-EP05 Andes 1972). Pola identik dengan EP04 rev1:
tiap klip = satu beat naskah; batas kalimat diketahui pasti, jadi waktu kata di
dalam satu kalimat dibagi menurut bobot suku kata — kesalahan tidak menumpuk
lintas kalimat.
"""
import json, re, subprocess, wave
from pathlib import Path
import numpy as np
import imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe()
CASE = Path(__file__).resolve().parent
SR = 44100

SEGS = [
    ("vo_01", ["Berapa hari kamu sanggup menahan lapar sebelum melanggar prinsip moral terbesarmu?"], 0.50),
    ("vo_02", ["Kamu pasti merasa lebih memilih mati daripada harus menyentuh jasad sahabatmu sendiri."], 0.50),
    ("vo_03", ["Tapi keyakinan itu runtuh begitu kamu mendengar satu siaran radio ini."], 0.50),
    ("vo_04", ["Di titik itu, mereka tahu tidak ada pahlawan yang datang.",
               "Pilihannya cuma menyerah, atau melakukan hal yang tak terbayangkan."], 0.50),
    ("vo_05", ["Suhu minus tiga puluh derajat.",
               "Tubuh mulai memakan lemaknya sendiri, otot melemah, dan halusinasi datang.",
               "Di luar bangkai pesawat, jasad rekan-rekan mereka terawetkan sempurna oleh es.",
               "Malam itu, di dalam kegelapan kabin yang membeku, perdebatan paling sunyi terjadi.",
               "Sebagian menangis menolak karena takut dosa.",
               "Sebagian sadar: menolak makan berarti bunuh diri perlahan."], 0.50),
    ("vo_06", ["Bukan paksaan yang mengubah segalanya, melainkan sebuah janji.",
               "Mereka saling berikrar: jika tubuhku mati malam ini, pakailah ragaku agar kalian bisa pulang menemui keluarga."], 0.50),
    ("vo_07", ["Pengorbanan kelam itu memberi mereka tenaga.",
               "Setelah tujuh puluh dua hari dan berjalan kaki menembus dinding es Andes, enam belas orang berhasil pulang hidup-hidup."], 0.50),
    ("vo_08", ["Jika kamu berada di kabin beku itu pada hari kesebelas, apakah kamu akan ikut makan demi pulang, atau memilih mati mempertahankan prinsipmu?",
               "Tulis pilihan jujurmu di komentar."], 0.60),
]

VOWELS = "aeiouy"


def load(path):
    p = subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-i", str(path),
                        "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"], capture_output=True)
    a = np.frombuffer(p.stdout, dtype="<i2").astype(np.float32) / 32768
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
    parts, words, starts = [], [], []
    t = 0.0
    for key, sentences, gap_after in SEGS:
        a = load(CASE / "audio" / f"{key}.mp3")
        dur = len(a) / SR
        starts.append(t)
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
    audio = audio / (np.max(np.abs(audio)) + 1e-9) * 0.92
    wav = CASE / "vo_andes.wav"
    with wave.open(str(wav), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(audio, -1, 1) * 32767).astype("<i2").tobytes())
    subprocess.run([FF, "-y", "-hide_banner", "-loglevel", "error", "-i", str(wav),
                    "-b:a", "192k", str(CASE / "vo_andes.mp3")], check=True)
    words = [w for w in words if w["word"].strip()]
    text = " ".join(w["word"] for w in words)
    json.dump({"source": "tts-internal voice-05", "duration": round(len(audio) / SR, 3),
               "text": text, "words": words},
              open(CASE / "vo_alignment.json", "w"), ensure_ascii=False, indent=1)
    print("durasi total", round(len(audio) / SR, 2), "s |", len(words), "kata")
    for (key, _, _), s in zip(SEGS, starts):
        print(f"{key}: mulai {s:.2f}")


if __name__ == "__main__":
    main()
