#!/usr/bin/env python3
"""
align_vo.py — potong satu berkas VO jadi sembilan segmen, memakai timestamp per kata
dari ASR (faster-whisper), bukan menebak dari keheningan.

    python3 tools/align_vo.py --audio "VO EP02.mp3" --segments segments.json --out vo_out

Kenapa begini: VO pemilik satu berkas utuh (471 dtk). Diukur di −32 dB hanya ada dua
jeda ≥ 0,60 dtk, sementara laju bacanya 126–177 kata/menit antar segmen. Kalau dipotong
pakai proporsi jumlah kata, batas ke-4 meleset sampai ±8 dtk — potongannya jatuh di
tengah kalimat dan Shorts ikut rusak.

Karena naskahnya diketahui persis, masalah ini bisa diselesaikan dengan pencocokan
urutan (difflib) antara kata naskah dan kata hasil ASR:

  naskah 1.177 kata, urut -> ASR memberi waktu mulai/selesai per kata
  setiap kata naskah dipetakan ke satu waktu; batas segmen = akhir kata terakhir segmen

Angka dibuang dari kedua sisi sebelum pencocokan: naskah mengeja ("dua ribu delapan
belas"), ASR sering menulis "2018". Membuang keduanya lebih aman daripada menebak
ejaan. Kata lain tetap dipakai sebagai jangkar.

Keluaran: vo_out/VO_01.wav … VO_09.wav (48 kHz mono), vo_out/boundaries.json,
vo_out/report.txt. Skrip berhenti dengan kode 1 kalau ada segmen yang laju bacanya
menyimpang > 30% dari median — tanda batasnya salah.
"""

import argparse
import difflib
import json
import pathlib
import re
import statistics
import subprocess
import sys

NUM = re.compile(r"^[\d.,]+$")


def norm_words(text):
    """kata untuk pencocokan: huruf kecil, tanpa tanda baca, angka dibuang"""
    text = text.lower().replace("’", "'").replace("–", " ").replace("—", " ")
    raw = re.findall(r"[a-z']+|\d+[\d.,]*", text)
    return [w.strip("'") for w in raw if not NUM.match(w)]


def script_tokens(segments):
    """daftar (kata, indeks_segmen) untuk seluruh naskah, urut"""
    out = []
    for seg in segments:
        for w in norm_words(seg["text"]):
            out.append((w, seg["id"]))
    return out


def transcribe(audio, language, model_name):
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        sys.exit("::error::faster-whisper belum terpasang (pip install faster-whisper)")

    print(f"ASR: model={model_name} bahasa={language}", flush=True)
    model = WhisperModel(model_name, device="cpu", compute_type="int8")
    segments, info = model.transcribe(
        audio,
        language=language,
        word_timestamps=True,
        vad_filter=True,
        beam_size=5,
        condition_on_previous_text=False,
    )
    words = []
    for s in segments:
        for w in (s.words or []):
            for tok in norm_words(w.word):
                words.append((tok, float(w.start), float(w.end)))
    print(f"ASR: {len(words)} kata, durasi audio {info.duration:.2f} dtk", flush=True)
    if len(words) < 100:
        sys.exit("::error::hasil ASR terlalu pendek — audio atau model bermasalah")
    return words


def map_times(toks, asr):
    """petakan setiap kata naskah ke (mulai, selesai) di audio"""
    a = [t[0] for t in toks]
    b = [w[0] for w in asr]
    times = [None] * len(a)
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            for k in range(i2 - i1):
                times[i1 + k] = (asr[j1 + k][1], asr[j1 + k][2])
        elif tag == "replace":
            # kata naskah dipetakan merata ke rentang waktu blok ASR penggantinya
            t0 = asr[j1][1]
            t1 = asr[j2 - 1][2]
            n = i2 - i1
            step = (t1 - t0) / max(n, 1)
            for k in range(n):
                times[i1 + k] = (t0 + k * step, t0 + (k + 1) * step)
        # delete: kata naskah tidak ada di ASR -> diisi belakangan
        # insert: kata ASR tanpa padanan -> diabaikan

    # isi lubang dengan interpolasi antara tetangga yang sudah punya waktu
    for i, t in enumerate(times):
        if t is not None:
            continue
        prev = next((times[j][1] for j in range(i - 1, -1, -1) if times[j]), 0.0)
        nxt = next((times[j][0] for j in range(i + 1, len(times)) if times[j]), None)
        times[i] = (prev, prev if nxt is None else max(prev, prev))
    return times


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--audio", required=True)
    ap.add_argument("--segments", required=True)
    ap.add_argument("--out", default="vo_out")
    ap.add_argument("--model", default="small")
    ap.add_argument("--pad", type=float, default=0.35,
                    help="tambahan jeda di akhir tiap segmen (dtk)")
    args = ap.parse_args()

    spec = json.loads(pathlib.Path(args.segments).read_text(encoding="utf-8"))
    segs = spec["segments"]
    lang = spec.get("language", "id")
    audio = args.audio

    probe = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                            "-of", "csv=p=0", audio], capture_output=True, text=True)
    total = float(probe.stdout.strip() or 0)
    if total <= 0:
        sys.exit(f"::error::tidak bisa membaca durasi {audio}")

    asr = transcribe(audio, lang, args.model)
    toks = script_tokens(segs)
    times = map_times(toks, asr)

    # batas segmen = akhir kata terakhir tiap segmen (kecuali segmen terakhir = durasi audio)
    bounds, seen = [], set()
    for i, (w, sid) in enumerate(toks):
        if sid in seen:
            continue
        seen.add(sid)
        last = max(j for j, (_, s) in enumerate(toks) if s == sid)
        end = min(total, times[last][1] + args.pad)
        bounds.append((sid, end))

    cuts = [(1, 0.0, bounds[0][1])]
    for k in range(1, len(bounds)):
        cuts.append((bounds[k][0], round(cuts[-1][2], 3), round(bounds[k][1], 3)))
    cuts[-1] = (cuts[-1][0], cuts[-1][1], round(total, 3))

    out = pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    rows, durs = [], []
    for sid, start, end in cuts:
        dst = out / f"VO_{sid:02d}.wav"
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                        "-ss", f"{start:.3f}", "-to", f"{end:.3f}", "-i", audio,
                        "-af", "silenceremove=start_periods=0:stop_periods=0",  # no-op, jaga filter graph
                        "-ar", "48000", "-ac", "1", "-c:a", "pcm_s16le", str(dst)], check=True)
        dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                    "-of", "csv=p=0", str(dst)], capture_output=True,
                                   text=True).stdout.strip() or 0)
        words = len(segs[sid - 1]["text"].split())
        durs.append(dur)
        rows.append({"id": sid, "start": round(start, 3), "end": round(end, 3),
                     "duration": round(dur, 3), "words": words,
                     "wpm": round(words / dur * 60, 1) if dur else 0,
                     "file": dst.name})

    wpm = [r["wpm"] for r in rows]
    med = statistics.median(wpm)
    bad = [r for r in rows if abs(r["wpm"] - med) / med > 0.30]

    lines = ["seg  mulai   akhir   durasi  kata   wpm", "-" * 44]
    for r in rows:
        lines.append(f"{r['id']:>3} {r['start']:7.2f} {r['end']:7.2f} {r['duration']:7.2f} "
                     f"{r['words']:>5} {r['wpm']:6.1f}")
    lines.append(f"\nmedian {med:.1f} wpm · total {sum(durs):.2f} dtk · audio {total:.2f} dtk")
    lines.append("BATAS MENCURIGAKAN: " + (", ".join(f"SEG {r['id']}" for r in bad) if bad else "tidak ada"))
    report = "\n".join(lines)
    print(report, flush=True)

    (out / "boundaries.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1) + "\n",
                                         encoding="utf-8")
    (out / "report.txt").write_text(report + "\n", encoding="utf-8")

    if bad:
        print("::warning::ada segmen dengan laju di luar ±30% median — periksa batasnya", flush=True)
        sys.exit(1)
    print("OK: sembilan segmen dipotong, semua laju dalam ±30% median", flush=True)


if __name__ == "__main__":
    main()
