#!/usr/bin/env bash
# Menyiapkan seluruh toolchain video di sandbox (tanpa root).
# Sandbox bisa ter-reset kapan saja; jalankan ini lagi kalau node_modules atau
# Chromium hilang.
#
#   bash setup_sandbox.sh
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
cd "$here"

echo "[1/4] python"
python3 -c "import numpy, PIL, imageio_ffmpeg" 2>/dev/null \
  || pip install --break-system-packages -q numpy pillow imageio-ffmpeg

echo "[2/4] node modules"
if [ ! -d remotion/node_modules ]; then
  (cd remotion && npm ci --no-audit --no-fund >/dev/null 2>&1)
fi

echo "[3/4] Chromium + pustaka AL2023"
if [ ! -x /tmp/chromium ] || [ ! -d /tmp/al2023/lib ]; then
  (cd remotion && node -e "
const fs=require('fs'), zlib=require('zlib'), c=require('@sparticuz/chromium').default||require('@sparticuz/chromium');
const bin='node_modules/@sparticuz/chromium/bin/';
fs.writeFileSync('/tmp/al2023.tar', zlib.brotliDecompressSync(fs.readFileSync(bin+'al2023.tar.br')));
fs.writeFileSync('/tmp/chromium.br', fs.readFileSync(bin+'chromium.br'));
c.executablePath().then(()=>console.log('chromium ok'));
")
  mkdir -p /tmp/al2023 && tar -xf /tmp/al2023.tar -C /tmp/al2023
fi

cat > /tmp/video-env.sh <<'EOF'
export LD_LIBRARY_PATH=/tmp/al2023/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}
export FF=$(python3 -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())")
EOF

echo "[4/4] selesai"
echo "Pakai dengan:  source /tmp/video-env.sh"
