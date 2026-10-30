#!/usr/bin/env bash
# setup.sh — memasang toolchain KHUSUS pipeline film (mg-styles-15).
#
# Berbeda dari ../setup_sandbox.sh (yang juga memasang Remotion penuh), skrip ini
# hanya memasang yang dibutuhkan jalur cepat:
#   * Chromium headless (dari @sparticuz/chromium, tanpa root)
#   * pustaka AL2023 yang dibutuhkan Chromium (libnspr4, libnss3, dst)
#   * puppeteer-core
#   * ffmpeg (lewat imageio-ffmpeg — tidak ada apt/root di sandbox)
#
# Sandbox bisa ter-reset kapan saja. Jalankan ulang skrip ini, lalu:
#   source /tmp/video-env.sh
#
#   bash setup.sh
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
cd "$here"

echo "[1/4] python: numpy, pillow, imageio-ffmpeg"
python3 -c "import numpy, PIL, imageio_ffmpeg" 2>/dev/null \
  || pip install --break-system-packages -q numpy pillow imageio-ffmpeg

echo "[2/4] node: puppeteer-core + @sparticuz/chromium"
[ -d node_modules/puppeteer-core ] || npm install --no-audit --no-fund --silent
[ -d node_modules/@sparticuz/chromium ] || npm install --no-audit --no-fund --silent --save @sparticuz/chromium

echo "[3/4] Chromium + pustaka AL2023"
if [ ! -x /tmp/chromium ] || [ ! -d /tmp/al2023/lib ]; then
  node -e "
const fs=require('fs'), zlib=require('zlib');
const c=require('@sparticuz/chromium').default||require('@sparticuz/chromium');
const bin='node_modules/@sparticuz/chromium/bin/';
if (fs.existsSync(bin+'al2023.tar.br')) {
  fs.writeFileSync('/tmp/al2023.tar', zlib.brotliDecompressSync(fs.readFileSync(bin+'al2023.tar.br')));
  fs.writeFileSync('/tmp/chromium.br', fs.readFileSync(bin+'chromium.br'));
}
c.executablePath().then(()=>{}).catch(e=>{console.error(e.message)});
"
  mkdir -p /tmp/al2023 && tar -xf /tmp/al2023.tar -C /tmp/al2023
fi

echo "[4/4] ffmpeg + env"
mkdir -p /tmp/bin
ln -sf "$(python3 -c 'import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())')" /tmp/bin/ffmpeg
cat > /tmp/video-env.sh <<'EOF'
export LD_LIBRARY_PATH=/tmp/al2023/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}
export PATH=/tmp/bin:$PATH
EOF

echo "selesai.  source /tmp/video-env.sh  lalu:"
echo "  node harness/render.mjs scenes/ident --out scenes/ident/out/v.mp4"
