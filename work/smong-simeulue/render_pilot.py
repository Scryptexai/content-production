#!/usr/bin/env python3
"""Render the AK-EP11 Smong Simeulue review/publish master from verified plates."""
from pathlib import Path
import subprocess
import imageio_ffmpeg

CASE = Path(__file__).resolve().parent
FF = imageio_ffmpeg.get_ffmpeg_exe()
FPS = 30
W, H = 1080, 1920
SHOTS = [
    (0.000, 4.329, "01_laut_surut.png", 0.50, 0.60),
    (4.329, 8.372, "02_simeulue_map.png", 0.50, 0.54),
    (8.372, 13.203, "03_urutan_smong.png", 0.50, 0.54),
    (13.203, 17.742, "04_kurang_dari_10_menit.png", 0.50, 0.48),
    (17.742, 20.800, "05_noaa_tsunami.png", 0.50, 0.52),
    (20.800, 24.292, "04_kurang_dari_10_menit.png", 0.52, 0.52),
    (24.292, 28.500, "05_langi_800_selamat.png", 0.50, 0.53),
    (28.500, 32.348, "06_ingat_bertindak.png", 0.50, 0.54),
    (32.348, 35.490, "07_pertanyaan.png", 0.50, 0.48),
]


def run(cmd):
    p = subprocess.run(cmd, text=True, capture_output=True)
    if p.returncode:
        raise RuntimeError(" ".join(map(str, cmd)) + "\n" + p.stderr[-5000:])


def main():
    shots = CASE / "shots"
    out = CASE / "out"
    shots.mkdir(exist_ok=True)
    out.mkdir(exist_ok=True)
    for i, (a, b, name, fx, fy) in enumerate(SHOTS):
        dur = b - a
        frames = round(dur * FPS)
        z = f"1+0.045*on/{max(1,frames-1)}"
        vf = (
            f"scale=2160:3840,setsar=1,zoompan=z='{z}':"
            f"x='(iw-iw/zoom)*{fx}':y='(ih-ih/zoom)*{fy}':"
            f"d={frames}:s={W}x{H}:fps={FPS},"
            f"fade=t=in:st=0:d=0.12,fade=t=out:st={max(0,dur-0.14):.3f}:d=0.14,format=yuv420p"
        )
        target = shots / f"{i:02d}.mp4"
        run([FF, "-y", "-loop", "1", "-framerate", str(FPS), "-i", str(CASE / "img" / name),
             "-filter:v", vf, "-frames:v", str(frames), "-r", str(FPS),
             "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-an", str(target)])
        print(f"shot {i:02d}: {dur:.3f}s {name}")
    listing = CASE / "concat.txt"
    listing.write_text("".join(f"file '{shots / f'{i:02d}.mp4'}'\n" for i in range(len(SHOTS))))
    cat = CASE / "cat.mp4"
    run([FF, "-y", "-f", "concat", "-safe", "0", "-i", str(listing), "-c", "copy", str(cat)])
    # The plates carry their own concise, large on-screen narrative. A separately timed
    # SRT accompanies the upload; this avoids obscuring the verified map/data cards with
    # redundant long subtitles in a 9:16 frame.
    master = out / "AK-EP11_smong-simeulue_feed.mp4"
    run([FF, "-y", "-i", str(cat), "-i", str(CASE / "audio" / "master.wav"),
         "-filter:v", "format=yuv420p",
         "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "medium", "-crf", "22",
         "-maxrate", "5M", "-bufsize", "10M", "-c:a", "aac", "-b:a", "192k", "-ar", "44100",
         "-movflags", "+faststart", "-t", "35.490", "-pix_fmt", "yuv420p", str(master)])
    print(master, master.stat().st_size)

if __name__ == "__main__":
    main()
