#!/usr/bin/env bash
# Menyiapkan Blender (bpy) di sandbox tanpa root, tanpa OpenGL.
#
# Kenapa perlu skrip: bpy butuh 8 pustaka X11 dan 2 simbol GL yang tidak ada
# di image ini, dan libxkbcommon dituntut dengan versi simbol V_0.5.0.
# Render memakai Cycles CPU, jadi permukaan GL tidak pernah benar-benar dipakai
# dan aman dipalsukan.
#
#   bash setup_blender.sh && source /tmp/blender-env.sh
set -euo pipefail

STUB=/tmp/glstub
mkdir -p "$STUB"

echo "[1/3] bpy 4.2.0 (519 MB)"
python3 -c "import bpy" 2>/dev/null || pip install --break-system-packages -q bpy==4.2.0

echo "[2/3] stub X11/GL"
python3 - "$STUB" <<'PY'
import glob, re, subprocess, sys, pathlib

stub = pathlib.Path(sys.argv[1])
libs = (glob.glob('/usr/local/lib/python3.11/dist-packages/bpy/lib/*.so*')
        + glob.glob('/usr/local/lib/python3.11/dist-packages/bpy/*.so'))
pat = re.compile(r'^(X\w+|XFixes\w*|XRender\w*|Xkb\w*|gl[A-Z]\w*|glX\w*|egl\w*|wl_\w+)$')
syms = set()
for lb in libs:
    out = subprocess.run(['nm', '-D', '--undefined-only', lb],
                         capture_output=True, text=True).stdout
    for line in out.splitlines():
        p = line.split()
        if p and pat.match(p[-1]):
            syms.add(p[-1])
syms |= {'XauGetBestAuthByAddr', 'XauDisposeAuth', 'XauReadAuth', 'XFixesShowCursor',
         '_XiGetDevicePresenceNotifyEvent', '_XiGetDevicePresenceNotifyEvent2'}
(stub / 'stub.c').write_text(
    "/* stub X11/GL: Cycles CPU tidak menyentuh permukaan GL */\n"
    + "\n".join(f'void *{s}(void) {{ return 0; }}' for s in sorted(syms)) + "\n")
print(f"    {len(syms)} simbol")
PY
gcc -shared -fPIC -o "$STUB/libGL.so.1" "$STUB/stub.c"
for f in libGL.so libGLX.so.0 libEGL.so.1 libGLESv2.so.2 libXrender.so.1 libXfixes.so.3 \
         libXi.so.6 libXxf86vm.so.1 libSM.so.6 libICE.so.6 libXext.so.6 libXau.so.6; do
  cp "$STUB/libGL.so.1" "$STUB/$f"
done

# libxkbcommon harus mengekspor simbol di versi V_0.5.0 — ini yang bikin gagal
# kalau hanya memakai pustaka stub biasa.
echo "[3/3] libxkbcommon ber-versi V_0.5.0"
python3 - "$STUB" <<'PY'
import pathlib, subprocess, sys
stub = pathlib.Path(sys.argv[1])
out = subprocess.run(
    ['objdump', '-T', '/usr/local/lib/python3.11/dist-packages/bpy/__init__.so'],
    capture_output=True, text=True).stdout
syms = sorted({p for line in out.splitlines() for p in line.split() if p.startswith('xkb_')})
syms = [s.rstrip(',') for s in syms]
(stub / 'xkb.c').write_text(
    "\n".join(f'void *{s}(void) {{ return 0; }}' for s in syms) + "\n")
(stub / 'xkb.map').write_text(
    "V_0.5.0 {\n  global:\n" + "".join(f"    {s};\n" for s in syms) + "  local: *;\n};\n")
print(f"    {len(syms)} simbol")
PY
gcc -shared -fPIC -Wl,--version-script="$STUB/xkb.map" -o "$STUB/libxkbcommon.so.0" "$STUB/xkb.c"

cat > /tmp/blender-env.sh <<'EOF'
export LD_LIBRARY_PATH=/tmp/glstub${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}
EOF

LD_LIBRARY_PATH="$STUB" python3 -c "import bpy; print('Blender siap:', bpy.app.version_string)"
echo
echo "Pakai dengan:  source /tmp/blender-env.sh"
