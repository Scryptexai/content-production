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

import pathlib
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


def row(e):
    ep = e["ep"]
    segs = len(e["beats"]) + 2
    photos = sorted(PLATES.glob(f"{ep}/*.jpg")) if (PLATES / ep).is_dir() else []
    vo = len(list(AUDIO.glob(f"{ep}/*.mp3"))) if (AUDIO / ep).is_dir() else 0
    bed = (AUDIO / ep / "bed.wav").exists()
    sfx = (AUDIO / ep / "sfx.wav").exists()
    thumb = (THUMBS / f"{ep}.png").exists() or (THUMBS / f"{ep}.jpg").exists()
    jalur = "PHOTO" if photos else "PLATE"

    kurang = []
    if len(photos) < MIN_PHOTOS:
        kurang.append(f"foto {len(photos)}/{segs} segmen")
    if vo < segs:
        kurang.append(f"VO {vo}/{segs}")
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
    return 0


if __name__ == "__main__":
    sys.exit(main())
