"""
check_film_assets.py — daftar aset yang masih kurang sebelum satu episode bisa
dirender dengan tampilan yang sama seperti EP01–EP08.

Kenapa ini ada: `Episode.tsx` punya dua jalur gambar.

  PHOTO  foto per segmen (`public/plates/<EP>/*.jpg`) + gerak kamera + scan
  PLATE  plate vektor (`PlateArt`) — jaring pengaman kalau foto belum ada

EP01–EP08 semuanya di jalur PHOTO. EP09–EP21 belum punya satu foto pun, jadi
jatuh ke PLATE. Dulu jalur PLATE hanya di-zoom 4,5 % sepanjang episode: hasilnya
terlihat dari kanal yang berbeda. Geraknya sudah disamakan (Camera.ts), tetapi
BAHAN-nya tetap beda sampai foto per episode dibuat.

Skrip ini tidak mengubah apa pun. Ia menjawab satu pertanyaan: episode mana yang
sudah siap render setara EP01–EP08, dan apa yang kurang.

    python3 tools/check_film_assets.py
    python3 tools/check_film_assets.py EP09
"""

import hashlib
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
from content_data import EPISODES  # noqa: E402

PUBLIC = ROOT / "10_FILM" / "remotion" / "public"
PLATES = PUBLIC / "plates"
AUDIO = PUBLIC / "audio"
THUMBS = PUBLIC / "thumbs"

# EP01–EP08 memakai 9–14 foto per episode; 9 adalah jumlah minimum yang masih
# memberi satu gambar baru di hampir setiap segmen.
MIN_PHOTOS = 9


def _norm(t):
    t = re.sub(r"[\u201c\u201d\"']", "", t or "")
    return re.sub(r"\s+", " ", t).strip().lower()


def narasi(e):
    """Cek narasi: apakah audio yang akan diputar benar-benar berisi naskahnya.

    Ini gerbang yang tidak ada sebelumnya. EP09 pernah dirender dengan audio
    Somerton Man sementara gambar dan caption-nya Danau Kenanga: semuanya
    "lengkap" menurut hitungan berkas, jadi tidak ada yang gagal. Sekarang
    teks di MANIFEST dibandingkan dengan teks naskah, dan VO satu berkas
    diperiksa sha256-nya.
    """
    ep = e["ep"]
    if e.get("vo"):
        want = e["vo"]["file"]
        path = AUDIO / ep / want
        if not path.exists():
            return f"VO {want} tidak ada"
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != e["vo"].get("sha256"):
            return f"VO {want} sha256 tidak cocok dengan yang tercatat (berkas berubah)"
        man = AUDIO / ep / "MANIFEST-VO.json"
        if not man.exists():
            return "MANIFEST-VO.json tidak ada"
        segs = len(e["vo"]["cues"])
        if segs != len(e["beats"]) + 2:
            return f"cue VO {segs} tidak sama dengan jumlah segmen {len(e['beats']) + 2}"
        return ""

    man = AUDIO / ep / "MANIFEST.json"
    if not man.exists():
        return "MANIFEST.json tidak ada (tidak ada bukti isi audio)"
    data = json.loads(man.read_text())
    got = {f["file"].replace(".mp3", ""): _norm(f.get("text", "")) for f in data.get("files", [])
           if f["file"].endswith(".mp3") and not f["file"].startswith("fx/")}
    want = {"00_hook": _norm(e["hook"])}
    for i, (part, txt) in enumerate(e["beats"]):
        want[f"{i + 1:02d}_{part}"] = _norm(txt)
    want["99_loop"] = _norm(e["loop"])
    beda = [k for k, v in want.items() if got.get(k) != v]
    if beda:
        return ("audio tidak cocok dengan naskah: " + ", ".join(beda[:4])
                + ("…" if len(beda) > 4 else ""))
    return ""


def row(e):
    ep = e["ep"]
    segs = len(e["beats"]) + 2
    photos = sorted(PLATES.glob(f"{ep}/*.jpg")) if (PLATES / ep).is_dir() else []
    if e.get("vo"):
        # mode VO milik user: satu berkas utuh untuk seluruh episode
        vo = 1 if (AUDIO / ep / e["vo"]["file"]).exists() else 0
        vo_want = 1
    else:
        vo = len(list(AUDIO.glob(f"{ep}/*.mp3"))) if (AUDIO / ep).is_dir() else 0
        vo_want = segs
    bed = (AUDIO / ep / "bed.wav").exists()
    sfx = (AUDIO / ep / "sfx.wav").exists()
    thumb = (THUMBS / f"{ep}.png").exists() or (THUMBS / f"{ep}.jpg").exists()
    jalur = "PHOTO" if photos else "PLATE"

    kurang = []
    if len(photos) < MIN_PHOTOS:
        kurang.append(f"foto {len(photos)}/{segs} segmen")
    if vo < vo_want:
        kurang.append(f"VO {vo}/{vo_want}")
    narasi_beda = narasi(e)
    if narasi_beda:
        kurang.append(narasi_beda)
    if not bed:
        kurang.append("bed")
    if not sfx:
        kurang.append("sfx")
    if not thumb:
        kurang.append("thumbnail")

    return {
        "ep": ep,
        "jalur": jalur,
        "segs": segs,
        "photos": len(photos),
        "vo": vo,
        "bed": bed,
        "sfx": sfx,
        "thumb": thumb,
        "kurang": kurang,
        "narasi": narasi_beda,
    }


def main():
    want = sys.argv[1:] or [e["ep"] for e in EPISODES]
    rows = [row(e) for e in EPISODES if e["ep"] in want]

    print(f"{'ep':5s} {'jalur':6s} {'foto':>4s} {'VO':>3s} {'bed':>3s} {'sfx':>3s} {'thumb':>5s}  kurang")
    for r in rows:
        print(f"{r['ep']:5s} {r['jalur']:6s} {r['photos']:>4d} {r['vo']:>3d} "
              f"{'ya' if r['bed'] else '—':>3s} {'ya' if r['sfx'] else '—':>3s} "
              f"{'ya' if r['thumb'] else '—':>5s}  {', '.join(r['kurang']) or 'lengkap'}")

    photo = sum(1 for r in rows if r["jalur"] == "PHOTO")
    plate = len(rows) - photo
    print(f"\n{photo} episode di jalur PHOTO (setara EP01–EP08) · {plate} episode masih PLATE")
    if plate:
        print("Yang masih PLATE akan terlihat beda dari EP01–EP08 sampai fotonya dibuat:")
        print("satu gambar 1080×1920 per segmen, disimpan di "
              "10_FILM/remotion/public/plates/<EP>/NN_nama.jpg (NN = urutan segmen).")
    rusak = [r for r in rows if r.get("narasi")]
    if rusak:
        print("\nNARASI TIDAK COCOK — render dibatalkan sampai audio dan naskah sama:")
        for r in rusak:
            print(f"  {r['ep']}: {r['narasi']}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
