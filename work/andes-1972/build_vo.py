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
    ("vo_01", ["Bayangkan pesawat kalian jatuh di pegunungan bersalju dan tujuh hari berlalu tanpa makanan sama sekali.",
               "Apa yang akan kalian makan untuk tidak mati kelaparan?"], 0.50),
    ("vo_02", ["Kebanyakan orang akan menjawab bahwa mereka akan bertahan dengan mencari daun atau akar yang bisa dimakan.",
               "Tetapi di pegunungan itu tidak ada satu pun tumbuhan dan tidak ada satu pun hewan.",
               "Yang bisa mereka lihat hanya salju, batu, dan serpihan pesawat."], 0.50),
    ("vo_03", ["Karena itu, para penyintas mengambil keputusan yang tidak pernah masuk rencana siapa pun di antara mereka.",
               "Mereka memutuskan memakan tubuh teman-teman mereka sendiri yang sudah meninggal sejak hari pertama kecelakaan, karena hanya itu satu-satunya makanan yang tersisa di gunung itu."], 0.55),
    ("vo_04", ["Keputusan itu tidak diambil oleh orang-orang kejam, tetapi oleh orang-orang beriman yang harus memilih antara nilai yang mereka pegang dan nyawa mereka sendiri.",
               "Pada hari kesebelas, sebuah radio transistor di antara kursi pesawat menyiarkan bahwa pencarian resmi terhadap mereka sudah dihentikan.",
               "Tidak ada satu pun di dunia yang tahu mereka masih hidup."], 0.60),
    ("vo_05", ["Penerbangan itu berangkat dari Montevideo, Uruguay, pada tiga belas Oktober seribu sembilan ratus tujuh puluh dua, membawa tim rugbi Old Christians Club menuju Santiago di Cile.",
               "Pesawat jatuh di sisi Argentina Pegunungan Andes, dan dua belas orang tewas seketika.",
               "Tiga puluh tiga orang yang selamat bersembunyi di dalam badan pesawat yang berwarna putih, dan warna itu menyatu dengan salju sehingga pesawat pencari tidak melihatnya dari udara."], 0.50),
    ("vo_06", ["Makanan yang mereka bawa, cokelat dan beberapa botol anggur, habis dalam satu minggu.",
               "Mereka menulis kata SOS dengan lipstik di badan pesawat, tetapi tidak ada pesawat yang menoleh.",
               "Pada dua puluh sembilan Oktober, longsor salju menyapu tempat berlindung mereka dan menewaskan delapan orang lagi.",
               "Sebagian besar dari mereka beragama Katolik, dan perdebatan tentang keputusan itu berlangsung lama."], 0.50),
    ("vo_07", ["Akhirnya mereka mengambil sumpah bersama: tidak ada satu pun orang yang akan dibunuh untuk dijadikan makanan.",
               "Yang mereka makan hanya tubuh teman-teman yang sudah meninggal sejak hari pertama.",
               "Keputusan itu diambil bersama setelah setiap orang diberi kesempatan berbicara menentangnya."], 0.55),
    ("vo_08", ["Dua orang akhirnya memutuskan berjalan keluar.",
               "Nando Parrado dan Roberto Canessa berjalan selama sepuluh hari melintasi punggung Pegunungan Andes tanpa peta dan tanpa perlengkapan pendakian.",
               "Mereka menemukan seorang penggembala Chili bernama Sergio Catalán, dan orang itulah yang membawa kabar mereka ke kantor polisi."], 0.50),
    ("vo_09", ["Evakuasi pun dimulai pada dua puluh dua Desember seribu sembilan ratus tujuh puluh dua, tujuh puluh dua hari setelah pesawat jatuh di sebuah lembah sisi Argentina Pegunungan Andes, dekat perbatasan Cile.",
               "Enam belas dari empat puluh lima orang selamat.",
               "Yang membuat mereka bertahan bukan keberuntungan, melainkan keputusan yang mereka ambil bersama pada malam-malam paling gelap di gunung itu."], 0.55),
    ("vo_10", ["Sekarang giliran kalian.",
               "Kalau kalian berada di pesawat itu, dan keputusan itu harus diambil pada malam yang sama juga, kalian ikut, atau kalian menolaknya sampai akhir?",
               "Tulis jawaban kalian di kolom komentar."], 0.70),
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
