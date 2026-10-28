#!/usr/bin/env bash
# Render TropicalFilm per potongan.
#
# Kenapa dipecah: satu tab Chromium yang merender ~6.000 frame 1080×1920
# perlahan menghabiskan memori dan akhirnya crash di tengah render. Dengan
# potongan 800 frame, tiap potongan mulai dari browser baru — total waktu hampir
# sama, tapi tidak ada render yang hilang saat crash.
#
# Pemakaian:  ./render-chunks.sh [mulai] [selesai]
set -uo pipefail

cd "$(dirname "$0")"
STEP=${STEP:-800}
TOTAL=${TOTAL:-5909}
START=${1:-0}
END=${2:-$((TOTAL - 1))}
OUT=out/chunks
mkdir -p "$OUT"

export LD_LIBRARY_PATH=/tmp/al2023/lib
FLAGS=(--browser-executable=/tmp/chromium --muted --codec=h264 --crf=20 --x264-preset=medium)

i=0
for ((from = START; from <= END; from += STEP)); do
  to=$((from + STEP - 1))
  ((to > END)) && to=$END
  name=$(printf "%s/chunk-%02d.mp4" "$OUT" "$i")
  i=$((i + 1))
  if [[ -s $name ]]; then
    echo "skip $name"
    continue
  fi
  echo "=== $from-$to → $name"
  if ! npx remotion render src/index.ts TropicalFilm "$name" \
      --frames="$from-$to" --concurrency=2 "${FLAGS[@]}"; then
    echo "    gagal di concurrency=2, ulang dengan 1"
    npx remotion render src/index.ts TropicalFilm "$name" \
      --frames="$from-$to" --concurrency=1 "${FLAGS[@]}" || { echo "GAGAL $name"; exit 1; }
  fi
done
echo "selesai: $i potongan di $OUT"
