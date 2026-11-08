#!/usr/bin/env bash
# Fetches official OFL font files (Space Grotesk, Inter) from the npm registry
# (@fontsource packages) and converts WOFF2 -> TTF into .build/fonts.
# Fonts are NOT committed to this repository; run this script to rebuild.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
BUILD="$HERE/../.build"
mkdir -p "$BUILD/pkg" "$BUILD/fonts"
cd "$BUILD/pkg"
[ -f package.json ] || npm init -y >/dev/null 2>&1
npm install --silent @fontsource/space-grotesk @fontsource/inter
python3 - "$BUILD" <<'PY'
import sys, pathlib
from fontTools.ttLib import TTFont
build = pathlib.Path(sys.argv[1]); out = build/"fonts"
want = {
 "space-grotesk": ["space-grotesk-latin-300-normal","space-grotesk-latin-400-normal","space-grotesk-latin-500-normal","space-grotesk-latin-600-normal","space-grotesk-latin-700-normal"],
 "inter": ["inter-latin-400-normal","inter-latin-500-normal","inter-latin-600-normal","inter-latin-700-normal"],
}
for pkg, files in want.items():
    for f in files:
        src = build/"pkg"/"node_modules"/(f"@fontsource/{pkg}")/"files"/(f+".woff2")
        if not src.exists(): print("MISSING", src); continue
        font = TTFont(str(src)); font.flavor = None
        dst = out/(f+".ttf"); font.save(str(dst)); print("ok", dst.name)
PY
