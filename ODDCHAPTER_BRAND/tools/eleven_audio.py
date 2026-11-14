"""eleven_audio.py — narasi, efek suara, dan musik lewat ElevenLabs.

Kenapa skrip ini ada di repo padahal ia butuh internet: sandbox tidak bisa
menjangkau api.elevenlabs.io, runner GitHub Actions bisa. Jadi semua panggilan
nyata terjadi di `.github/workflows/eleven-audio.yml`, dan skrip ini yang
menentukan *apa* yang dibuat — satu sumber kebenaran, dipakai lokal maupun CI.

Identitas suara dikunci di `tools/voice.json`:
    voice_id = ojz6ro9PB1xDu44lymdM   (narator kanal, mulai EP08)

Perintah:

    python3 tools/eleven_audio.py --check
        Uji kunci + voice id: siapa namanya, sisa kuota karakter, dan satu
        contoh 5 detik (ditulis ke /tmp, tidak masuk repo).

    python3 tools/eleven_audio.py --episode EP08 --only voice [--force]
        Sepuluh segmen narasi -> public/audio/EP08/{00_hook,...,99_loop}.mp3
        Nama berkas sama dengan yang dibaca build_timing.py, jadi timing,
        caption, dan Remotion tidak perlu diubah.

    python3 tools/eleven_audio.py --episode EP08 --only sfx [--force]
        Satu efek per nama di ep["sfx"] -> public/audio/EP08/fx/<nama>.mp3

    python3 tools/eleven_audio.py --episode EP08 --only place
        Menempelkan fx ke timeline nyata (timing.generated.json) -> sfx.wav

    python3 tools/eleven_audio.py --episode EP08 --only all
        voice -> build_timing -> sfx -> place -> build_bed, berurutan.

    python3 tools/eleven_audio.py --music "prompt" --out bed_music.mp3 --ms 48000
        Musik latar (hanya kalau memang perlu; bed.wav sudah cukup di banyak
        episode, dan dua lapisan musik bersamaan akan saling menutupi).
"""

import argparse
import json
import os
import pathlib
import subprocess
import sys
import time
import urllib.error
import urllib.request

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

API = "https://api.elevenlabs.io/v1"
AUDIO = ROOT / "10_FILM" / "remotion" / "public" / "audio"
TIMING = ROOT / "10_FILM" / "remotion" / "src" / "timing.generated.json"
VOICE_FILE = HERE / "voice.json"

# Efek -> prompt. Ditulis sebagai bunyi yang terjadi, bukan nama kategori:
# model efek bekerja jauh lebih tepat kalau diberi sumber, ruang, dan jarak.
SFX_PROMPTS = {
    "rustle": "close-miked heavy wool clothing shifting, one short movement, dry room, no music",
    "gust": "cold wind pressing against a wooden house, gust swelling and fading, distant, no music",
    "engine": "distant steam ship engine, low chug, muffled through fog, no music",
    "clunk": "heavy iron door bolt sliding shut, one solid metallic clunk, small stone room",
    "tick": "a clock ticking twice then stopping, close, quiet room, no music",
    "page": "a single page of old paper turned close to the microphone, dry, no music",
    "boom": "deep cinematic sub drop, 40 hertz, long decay, felt more than heard, no music",
    "footstep": "boots stepping on packed snow, three slow steps, cold open air, no music",
    "door": "old wooden door creaking open slowly, close, night interior, no music",
    "fire": "small fire burning in an iron stove, close, dry crackle, no music",
    "water": "slow drip of water in a stone tunnel, echoing, distant, no music",
    "crowd": "muffled distant crowd murmur behind glass, no words, no music",
}


def api_key():
    key = os.environ.get("ELEVENLABS_API_KEY") or os.environ.get("ELEVENLABS_KEY")
    if not key:
        raise SystemExit("ELEVENLABS_API_KEY kosong. Di CI: secrets.ELEVENLABS_API_KEY.")
    return key.strip()


def voice_cfg():
    cfg = json.loads(VOICE_FILE.read_text(encoding="utf-8"))
    cfg["voice_id"] = os.environ.get("ELEVEN_VOICE_ID") or cfg["voice_id"]
    cfg["model_id"] = os.environ.get("ELEVEN_MODEL") or cfg["model_id"]
    return cfg


def call(path, payload=None, *, accept="audio/mpeg", timeout=240, retries=3):
    """Satu panggilan HTTP. Kembalikan bytes; JSON kalau accept=application/json."""
    url = path if path.startswith("http") else API + path
    body = json.dumps(payload).encode() if payload is not None else None
    last = None
    for attempt in range(retries):
        req = urllib.request.Request(url, data=body, method="POST" if body else "GET")
        req.add_header("xi-api-key", api_key())
        req.add_header("accept", accept)
        if body:
            req.add_header("content-type", "application/json")
        try:
            with urllib.request.urlopen(req, timeout=timeout) as res:
                data = res.read()
                return json.loads(data) if accept == "application/json" else data
        except urllib.error.HTTPError as exc:
            detail = exc.read()[:600].decode("utf-8", "replace")
            last = f"{exc.code} {detail}"
            # 401/422 tidak akan berubah kalau diulang; 429/5xx layak ditunggu.
            if exc.code in (400, 401, 403, 404, 422):
                break
            time.sleep(4 * (attempt + 1))
        except Exception as exc:  # noqa: BLE001 — jaringan sandbox sering menolak
            last = repr(exc)
            time.sleep(3 * (attempt + 1))
    raise SystemExit(f"GAGAL {path}: {last}")



def _ff():
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return "ffmpeg"


def polish(path, cfg, words):
    """Rapikan satu segmen: tempo ke target, ratakan keras, jaga konsistensi.

    Kenapa bukan hanya mengandalkan parameter `speed`: tidak semua model
    menghormatinya (multilingual_v2 mengabaikannya, dan turbo pun tidak selalu
    mencapai target). Jadi tempo diukur dari hasil nyata lalu dikoreksi dengan
    `atempo` — perubahan tempo tanpa mengubah pitch.

    Kenapa dikompres: pemilik mendengar "suara turun 1-2 kata di zona yang tidak
    tepat". Itu dinamika model. Kompresor ringan (3:1) menaikkan kata yang
    tertekan tanpa membuat kalimat datar, lalu RMS tiap segmen disamakan supaya
    tidak ada segmen yang lebih pelan dari yang lain.
    """
    target_wpm = cfg.get("pace_wpm", 138)
    tol = cfg.get("tempo_tolerance", 0.10)
    dur = _probe_duration(path)
    if not dur or not words:
        return None
    wpm = words / dur * 60
    tempo = 1.0
    if abs(wpm - target_wpm) / target_wpm > tol:
        tempo = min(1.30, max(0.72, wpm / target_wpm))
    chain = ["highpass=f=70", "lowpass=f=12000"]
    if tempo != 1.0:
        chain.append(f"atempo={tempo:.3f}")
    if cfg.get("polish", True):
        chain.append("acompressor=threshold=-22dB:ratio=3:attack=6:release=140:makeup=2")
        chain.append("alimiter=limit=0.95")
    tmp = path.with_name(path.stem + "_polish" + path.suffix)
    subprocess.run([_ff(), "-y", "-hide_banner", "-loglevel", "error", "-i", str(path),
                    "-af", ",".join(chain), "-ar", "48000", "-ac", "1",
                    "-c:a", "libmp3lame", "-b:a", "192k", str(tmp)], check=True)
    tmp.replace(path)
    return {"wpm_before": round(wpm, 1), "tempo": round(tempo, 3),
            "dur_after": _probe_duration(path)}


def _probe_duration(path):
    try:
        out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                              "-of", "csv=p=0", str(path)], capture_output=True, text=True)
        return float(out.stdout.strip())
    except Exception:
        r = subprocess.run([_ff(), "-i", str(path)], capture_output=True, text=True)
        for line in r.stderr.splitlines():
            if "Duration:" in line:
                hms = line.split("Duration:")[1].split(",")[0].strip()
                h, m, sec = hms.split(":")
                return int(h) * 3600 + int(m) * 60 + float(sec)
    return None


def segments(ep):
    """(key, text) — urutan dan nama sama persis dengan build_timing.py."""
    out = [("00_hook", ep["hook"])]
    for i, (part, txt) in enumerate(ep["beats"]):
        out.append((f"{i + 1:02d}_{part}", txt))
    out.append(("99_loop", ep["loop"]))
    return out


def _spoken_guard(text):
    """Tolak markup sebelum teks dikirim ke mesin suara.

    Aturan dari SKILLS/elevenlabs-tts-2026: yang diucapkan hanya kalimat.
    Tag seperti [pause] atau <break> akan terbaca sebagai kata atau merusak
    prosodi, dan tidak ada di format keluaran kita (mp3 per segmen).
    """
    import re as _re
    for rx, label in (
        (_re.compile(r"<[^>]{1,40}>"), "markup sudut"),
        (_re.compile(r"\[[^\]]{1,40}\]"), "tag kurung siku"),
        (_re.compile(r"\*\*|__|`"), "penanda markdown"),
    ):
        if rx.search(text):
            raise SystemExit(f"teks narasi memuat {label}: {text[:60]!r} — bersihkan dulu")


def tts(text, out_path, cfg):
    _spoken_guard(text)
    payload = {
        "text": text,
        "model_id": cfg["model_id"],
        "voice_settings": cfg["settings"],
    }
    data = call(f"/text-to-speech/{cfg['voice_id']}", payload)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(data)
    return len(data)


def _probe(label, fn, *, fatal=False):
    """Satu pemeriksaan; kegagalan yang tidak fatal dicetak, bukan mematikan."""
    try:
        return fn()
    except SystemExit as exc:  # call() melempar SystemExit saat HTTP gagal
        print(f"{label}: GAGAL — {exc}")
        if fatal:
            raise
        return None


def cmd_check(_args):
    """Uji kunci, voice id, dan satu kalimat TTS.

    /user butuh izin 'user_read' dan sering tidak ada di kunci terbatas — itu
    bukan alasan gagal. Yang wajib lolos hanya voice id + satu kalimat TTS.
    """
    cfg = voice_cfg()
    print(f"voice_id  : {cfg['voice_id']}")
    print(f"model     : {cfg['model_id']}")
    print(f"settings  : {json.dumps(cfg['settings'], ensure_ascii=False)}")

    user = _probe("kuota", lambda: call("/user", accept="application/json"))
    if user:
        sub = user.get("subscription") or {}
        print(f"  akun    : {user.get('first_name', '?')} · tier {sub.get('tier', '?')}")
        print(f"  karakter: {sub.get('character_count', '? ')} / {sub.get('character_limit', '?')}")

    # Kunci ber-scope sempit biasanya hanya punya text_to_speech, tanpa voices_read.
    # Itu bukan masalah: yang menentukan suara bisa dipakai adalah satu kalimat TTS
    # di bawah, bukan metadata voice-nya.
    voice = _probe("metadata voice", lambda: call(f"/voices/{cfg['voice_id']}", accept="application/json"))
    if voice:
        print(f"  nama    : {voice.get('name', '?')} · kategori {voice.get('category', '?')}")
        labels = voice.get("labels") or {}
        if labels:
            print("  label   : " + ", ".join(f"{k}={v}" for k, v in labels.items()))
        if voice.get("description"):
            print(f"  deskripsi: {voice['description'][:160]}")

    out = ROOT / "10_FILM" / "remotion" / "public" / "audio" / "_voicecheck.mp3"
    size = _probe(
        "uji tts",
        lambda: tts("Suara ini yang akan bercerita di setiap episode.", out, cfg),
        fatal=True,
    )
    if size:
        print(f"  hasil   : {size} bytes -> {out}")
        print(f"  durasi  : {audio_duration(out)}")
    print("KONEKSI OK — voice id bisa dipakai.")
    print("catatan: metadata/kuota boleh gagal (kunci hanya berizin text_to_speech).")


def audio_duration(path):
    try:
        import subprocess as sp
        r = sp.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                    "-of", "csv=p=0", str(path)], capture_output=True, text=True)
        return round(float(r.stdout.strip()), 2)
    except Exception:
        return "?"



VARIANTS = [
    # (nama, model, override settings, ubah teks)
    # Speed hanya berpengaruh pada model yang mendukungnya (v2.5 ke atas).
    # multilingual_v2 mengabaikan speed sepenuhnya — dulu sempat mengira ini
    # penyebab suara terlalu cepat, ternyata bukan: model itu memang mengambil
    # tempo sendiri, dan satu-satunya kendali kita adalah memecah kalimat.
    ("v2_asis", None, {}, None),
    ("v2_ellipsis", None, {}, "ellipsis"),
    ("turbo25_s085", "eleven_turbo_v2_5", {"speed": 0.85}, None),
    ("turbo25_s090", "eleven_turbo_v2_5", {"speed": 0.90}, None),
    ("turbo25_s085_ell", "eleven_turbo_v2_5", {"speed": 0.85}, "ellipsis"),
    ("v4_asis", "eleven_v4", {}, None),
    ("v4_ellipsis", "eleven_v4", {}, "ellipsis"),
]


def _transform(text, how):
    if how == "ellipsis":
        return text.replace(", ", "\u2026 ")
    return text


def cmd_probe(args):
    """Render satu kalimat dalam beberapa varian, untuk dibandingkan dengan ukur.

    Dipakai saat prosodi bermasalah: lebih murah membandingkan 7 varian satu
    kalimat daripada me-render satu episode lalu kecewa.
    """
    cfg = voice_cfg()
    outdir = AUDIO / "_probe"
    outdir.mkdir(parents=True, exist_ok=True)
    for old in outdir.glob("*.mp3"):
        old.unlink()
    used = 0
    for name, model, override, how in VARIANTS:
        c = json.loads(json.dumps(cfg))
        if model:
            c["model_id"] = model
        c["settings"].update(override)
        text = _transform(args.probe, how)
        out = outdir / f"probe_{name}.mp3"
        try:
            size = tts(text, out, c)
        except SystemExit as exc:
            print(f"  ! {name}: {exc}")
            continue
        used += 1
        print(f"  + {out.name} {size} B · {c['model_id']} · {json.dumps(c['settings'], ensure_ascii=False)}")
    print(f"selesai: {used} varian di {outdir}")


def cmd_voice(args, ep):
    cfg = voice_cfg()
    total = 0
    keep = {k for k, _ in segments(ep)}
    # Segmen yang tidak ada lagi di naskah harus dibuang, bukan ditinggal: kalau
    # tertinggal, build_timing tidak membacanya tetapi git menyimpannya selamanya
    # dan suatu hari ada yang salah memakainya.
    for stray in (AUDIO / ep["ep"]).glob("*.mp3"):
        if stray.stem not in keep:
            stray.unlink()
            print(f"  - {stray.name} (tidak dipakai naskah, dihapus)")
    for key, text in segments(ep):
        out = AUDIO / ep["ep"] / f"{key}.mp3"
        if out.exists() and not args.force:
            print(f"  = {key} (sudah ada, {out.stat().st_size} B) — pakai --force untuk menimpa")
            continue
        size = tts(text, out, cfg)
        info = polish(out, cfg, len(text.split()))
        total += len(text)
        extra = ""
        if info:
            extra = (f" · {info['wpm_before']} wpm → tempo {info['tempo']}"
                     f" · {info['dur_after']:.2f}s")
        print(f"  + {key}.mp3 {size} B · {len(text.split())} kata{extra}")
        time.sleep(0.4)
    print(f"narasi {ep['ep']}: {total} karakter terpakai")


def cmd_sfx(args, ep):
    cfg = voice_cfg()
    names = []
    for name in (ep.get("sfx") or {}).values():
        if name not in names:
            names.append(name)
    for name in names:
        prompt = SFX_PROMPTS.get(name)
        if not prompt:
            print(f"  ! {name}: belum ada prompt di SFX_PROMPTS — dilewati")
            continue
        out = AUDIO / ep["ep"] / "fx" / f"{name}.mp3"
        if out.exists() and not args.force:
            print(f"  = fx/{name}.mp3 (sudah ada)")
            continue
        payload = {"text": prompt, "duration_seconds": 2.5, "prompt_influence": 0.6}
        data = call("/sound-generation?output_format=mp3_44100_128", payload)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(data)
        print(f"  + fx/{name}.mp3 {len(data)} B")


def _ffmpeg():
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return "ffmpeg"


def cmd_place(args, ep):
    """Tempel fx ke timeline audio nyata -> public/audio/<EP>/sfx.wav."""
    tm = json.loads(TIMING.read_text(encoding="utf-8"))[ep["ep"]]
    mapping = ep.get("sfx") or {}
    fx_dir = AUDIO / ep["ep"] / "fx"
    pieces = []
    for seg in tm["segments"]:
        name = mapping.get(seg["key"])
        path = fx_dir / f"{name}.mp3"
        if not name or not path.exists():
            continue
        pieces.append((path, seg["start"], 0.9 if name != "gust" else 0.7))
    if not pieces:
        print("tidak ada fx untuk ditempel")
        return
    total = tm["total"] + 2.0
    cmd = [_ffmpeg(), "-y", "-hide_banner", "-loglevel", "error"]
    for path, _, _ in pieces:
        cmd += ["-i", str(path)]
    chains, labels = [], []
    for i, (_, start, vol) in enumerate(pieces):
        ms = max(0, int(start * 1000))
        chains.append(f"[{i}:a]volume={vol},adelay={ms}|{ms}[a{i}]")
        labels.append(f"[a{i}]")
    chains.append(
        "".join(labels) + f"amix=inputs={len(labels)}:normalize=0,"
        f"apad,atrim=0:{total:.3f},asetpts=N/SR/TB[out]"
    )
    out = AUDIO / ep["ep"] / "sfx.wav"
    cmd += ["-filter_complex", ";".join(chains), "-map", "[out]",
            "-ar", "48000", "-ac", "1", str(out)]
    subprocess.run(cmd, check=True)
    print(f"sfx.wav: {out} ({out.stat().st_size} B, {len(pieces)} efek)")


def cmd_build(args, ep):
    env = dict(os.environ)
    for script in ("build_timing.py", "build_bed.py"):
        print(f"--- {script} {ep['ep']}")
        subprocess.run([sys.executable, str(HERE / script), ep["ep"]], check=True, env=env)


def cmd_music(args):
    payload = {
        "prompt": args.music,
        "music_length_ms": args.ms,
        "model_id": os.environ.get("ELEVEN_MUSIC_MODEL", "music_v1"),
    }
    data = call("/music?output_format=mp3_44100_192", payload)
    out = pathlib.Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(data)
    print(f"musik: {out} ({len(data)} B)")


def main():
    ap = argparse.ArgumentParser(description="ElevenLabs: narasi, efek, musik.")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--episode", help="EP08")
    ap.add_argument("--only", default="all", choices=["voice", "sfx", "place", "all", "build"])
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--probe", help="satu kalimat untuk dibandingkan antar varian model/settings")
    ap.add_argument("--music")
    ap.add_argument("--ms", type=int, default=48000)
    ap.add_argument("--out", default="music.mp3")
    args = ap.parse_args()

    if args.check:
        cmd_check(args)
        return
    if args.probe:
        cmd_probe(args)
        return
    if args.music:
        cmd_music(args)
        return
    if not args.episode:
        ap.error("butuh --episode, --check, atau --music")

    from content_data import EPISODES  # noqa: E402
    ep = next((e for e in EPISODES if e["ep"] == args.episode), None)
    if not ep:
        raise SystemExit(f"{args.episode} tidak ada di content_data.py")

    if args.only in ("voice", "all"):
        print(f"=== narasi {ep['ep']}")
        cmd_voice(args, ep)
    if args.only in ("sfx", "all"):
        print(f"=== efek {ep['ep']}")
        cmd_sfx(args, ep)
    if args.only in ("all", "build"):
        print(f"=== timing + bed")
        cmd_build(args, ep)
    if args.only in ("place", "all"):
        print(f"=== tempel efek")
        cmd_place(args, ep)


if __name__ == "__main__":
    main()
