#!/usr/bin/env bash
#===============================================================================
# Prismfall REAL-ENGINE battle capture (Linux, headless). Dev tool only.
#
#   bash run_engine_capture.sh build      # build mkxp-z 2.4.2 from source (once, ~2 min)
#   bash run_engine_capture.sh assemble   # contained game copy: base project + kit + autorun
#   bash run_engine_capture.sh run volcanic            # or silkwood,zekrom
#   bash build_captures.sh                # GIFs + key frames -> docs/battle_captures/engine/
#
# Everything happens under $RUN (default /home/claude/run). Nothing in the kit or the
# reference base project is modified. Needs: gcc/g++, cmake, ninja, python3, git (GitHub
# clones only), Xvfb, system libs present on this box (SDL2, GL/Mesa, openal, ogg/vorbis/
# theora, freetype, pixman, libpng, zlib, bz2) and Ruby 3.3 at $RUBY_HOME.
# Transcribed from the session that produced the captures (Nov 2026).
#===============================================================================
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
KIT="$(cd "$HERE/../../.." && pwd)"
RUN="${RUN:-/home/claude/run}"
BASE="${BASE:-/home/claude/ref/ebdx_renovation}"
RUBY_HOME="${RUBY_HOME:-/opt/rbenv/versions/3.3.6}"
B="$RUN/build"; P="$B/prefix"; L=/usr/lib/x86_64-linux-gnu

clone() { [[ -d "$B/$2" ]] || git clone -q --depth 1 ${3:+--branch $3} "https://github.com/$1" "$B/$2"; }

build() {
  mkdir -p "$B" "$P/include/SDL2" "$P/lib/pkgconfig" "$P/bin"
  clone mesonbuild/meson meson 1.4.0;            clone mkxp-z/mkxp-z mkxp-z v2.4.2
  clone libsdl-org/SDL SDL release-2.30.0;       clone libsdl-org/SDL_image SDL_image release-2.8.2
  clone libsdl-org/SDL_ttf SDL_ttf release-2.22.0; clone icculus/SDL_sound SDL_sound v2.0.2
  clone icculus/physfs physfs release-3.2.0;     clone kcat/openal-soft openal 1.23.1
  clone xiph/ogg ogg v1.3.5; clone xiph/vorbis vorbis v1.3.7; clone xiph/theora theora v1.1.1
  clone BYVoid/uchardet uchardet
  # xxd (not installed): tiny Python stand-in for `xxd -i`
  cat > "$P/bin/xxd" <<'PY'
#!/usr/bin/env python3
import sys, re
path = sys.argv[-1]; data = open(path, 'rb').read()
name = re.sub(r'[^A-Za-z0-9]', '_', path)
name = '__' + name if name[0].isdigit() else name
rows = ['  ' + ', '.join('0x%02x' % b for b in data[i:i + 12]) for i in range(0, len(data), 12)]
sys.stdout.write('unsigned char %s[] = {\n%s\n};\nunsigned int %s_len = %d;\n' % (name, ',\n'.join(rows), name, len(data)))
PY
  chmod +x "$P/bin/xxd"
  # Headers from the clones + the system's runtime .so files (no -dev packages installed)
  cp "$B"/SDL/include/*.h "$P/include/SDL2/"; ln -sf $L/libSDL2-2.0.so.0 "$P/lib/libSDL2.so"
  cp -r "$B/openal/include/AL" "$P/include/"; ln -sf $L/libopenal.so.1 "$P/lib/libopenal.so"
  mkdir -p "$P/include/ogg" "$P/include/vorbis" "$P/include/theora"
  cp "$B"/ogg/include/ogg/*.h "$P/include/ogg/"; cp "$B"/vorbis/include/vorbis/*.h "$P/include/vorbis/"
  cp "$B"/theora/include/theora/*.h "$P/include/theora/"
  printf '#ifndef __CONFIG_TYPES_H__\n#define __CONFIG_TYPES_H__\n#include <stdint.h>\ntypedef int16_t ogg_int16_t; typedef uint16_t ogg_uint16_t; typedef int32_t ogg_int32_t;\ntypedef uint32_t ogg_uint32_t; typedef int64_t ogg_int64_t; typedef uint64_t ogg_uint64_t;\n#endif\n' > "$P/include/ogg/config_types.h"
  ln -sf $L/libogg.so.0 "$P/lib/libogg.so"; ln -sf $L/libvorbis.so.0 "$P/lib/libvorbis.so"
  ln -sf $L/libvorbisfile.so.3 "$P/lib/libvorbisfile.so"; ln -sf $L/libtheora.so.0 "$P/lib/libtheora.so"
  ln -sf $L/libtheoradec.so.1 "$P/lib/libtheoradec.so"; ln -sf $L/libGL.so.1 "$P/lib/libGL.so"
  pc() { printf 'prefix=%s\nName: %s\nDescription: %s\nVersion: %s\nLibs: -L${prefix}/lib %s\nCflags: -I${prefix}/include %s\n' "$P" "$1" "$1" "$2" "$3" "$4" > "$P/lib/pkgconfig/$1.pc"; }
  pc sdl2 2.30.0 "-lSDL2" "-I$P/include/SDL2 -D_REENTRANT"; cp "$P/lib/pkgconfig/sdl2.pc" "$P/lib/pkgconfig/SDL2.pc"
  pc openal 1.23.1 "-lopenal" "-I$P/include/AL"; pc ogg 1.3.5 "-logg" ""; pc vorbis 1.3.7 "-lvorbis" ""
  pc vorbisfile 1.3.7 "-lvorbisfile" ""; pc theora 1.1.1 "-ltheora -ltheoradec" ""; pc gl 1.2 "-lGL" ""
  pc SDL2_image 2.8.2 "-lSDL2_image" "-I$P/include/SDL2"; pc SDL2_ttf 2.22.0 "-lSDL2_ttf -lfreetype" "-I$P/include/SDL2"
  # Small static libs from source
  CF="-O2 -fPIC -I$P/include/SDL2 -D_REENTRANT"
  (cd "$B/SDL_image/src" && gcc $CF -DUSE_STBIMAGE -DLOAD_PNG -DLOAD_JPG -DLOAD_BMP -DLOAD_GIF -DLOAD_TGA -DLOAD_QOI \
     -I. -I../include -c *.c && ar rcs "$P/lib/libSDL2_image.a" *.o && cp ../include/SDL_image.h "$P/include/SDL2/")
  (cd "$B/SDL_ttf" && gcc $CF $(pkg-config --cflags freetype2) -c SDL_ttf.c && ar rcs "$P/lib/libSDL2_ttf.a" SDL_ttf.o \
     && cp SDL_ttf.h "$P/include/SDL2/")
  (cd "$B/SDL_sound/src" && rm -f SDL_sound_skeleton.c && gcc $CF -I. -c *.c libmodplug/*.c timidity/*.c; \
     rm -f SDL_sound_coreaudio.o; ar rcs "$P/lib/libSDL2_sound.a" *.o && cp SDL_sound.h "$P/include/" "$P/include/SDL2/")
  for d in physfs uchardet; do
    mkdir -p "$B/$d/b" && (cd "$B/$d/b" && cmake .. -DCMAKE_INSTALL_PREFIX="$P" -DCMAKE_INSTALL_LIBDIR=lib \
      -DPHYSFS_BUILD_SHARED=OFF -DPHYSFS_BUILD_TEST=OFF -DPHYSFS_BUILD_DOCS=OFF -DBUILD_SHARED_LIBS=OFF -DBUILD_BINARY=OFF \
      -DCMAKE_POSITION_INDEPENDENT_CODE=ON -DCMAKE_POLICY_VERSION_MINIMUM=3.5 >/dev/null && make -j"$(nproc)" install >/dev/null)
  done
  # mkxp-z: no libjpeg/iconv dev files here; glibc provides iconv; build without fluidsynth/https
  python3 - "$B/mkxp-z/src/meson.build" <<'PY'
import sys
p = sys.argv[1]; s = open(p).read()
s = s.replace("jpeg = dependency('libjpeg', static: build_static)\n", "")
s = s.replace("    iconv = compilers['cpp'].find_library('iconv')\n    global_dependencies += compilers['cpp'].find_library('charset')\n", "    iconv = []\n")
s = s.replace("png, jpeg, iconv, uchardet]", "png, iconv, uchardet]")
open(p, 'w').write(s)
PY
  export PATH="$P/bin:$PATH" PKG_CONFIG_PATH="$P/lib/pkgconfig" LIBRARY_PATH="$P/lib"
  R="$RUBY_HOME"
  (cd "$B/mkxp-z" && rm -rf b && python3 ../meson/meson.py setup b -Dshared_fluid=false -Denable-https=false \
     -Dworkdir_current=true -Dstatic_executable=false -Dmri_includes="$R/include/ruby-3.3.0" -Dmri_libpath="$R/lib" \
     -Dmri_library=ruby -Dcpp_args="-I$R/include/ruby-3.3.0/x86_64-linux -I$P/include -I$P/include/AL -include string.h -include stdlib.h -include stdio.h -include math.h -include strings.h -fpermissive -w" \
     -Dcpp_link_args="-L$P/lib -Wl,-rpath,$R/lib -ldl -lpthread" && ninja -C b)
  echo "built $B/mkxp-z/b/mkxp-z.x86_64"
}

assemble() {
  # PACKAGE=0 reuses the existing dist/ (don't rebuild it while another tool may be reading it)
  [[ "${PACKAGE:-1}" == "1" ]] && (cd "$KIT" && bash tools/package.sh)
  rm -rf "$RUN/game"; cp -r "$BASE" "$RUN/game"
  D="$KIT/dist/Prismfall_DevKit"
  cp -r "$D/Plugins/." "$RUN/game/Plugins/"; cp "$D"/PBS/*.txt "$RUN/game/PBS/"; cp "$D"/Data/* "$RUN/game/Data/"
  mkdir -p "$RUN/game/Plugins/ZZ Demo Autorun"
  cp "$HERE/meta.txt" "$HERE/001_DemoAutorun.rb" "$RUN/game/Plugins/ZZ Demo Autorun/"
  # Base-project fix needed to boot at all (see docs/battle_captures/engine/README.md):
  sed -i '4s/^class PokemonSprite < SpriteWrapper/class PokemonSprite   # capture-copy patch: superclass mismatch/' \
    "$RUN/game/Plugins/Elite Battle DX/[000] Scripts/Battle UI/UI Fixes.rb"
  # Engine config: find Ruby's stdlib (zlib.so), no vsync wait under Xvfb
  # Own save/error-log directory per capture copy (dataPathApp), so copies never share one.
  python3 - "$RUN/game/mkxp.json" "$RUBY_HOME" "PrismfallCapture-$(basename "$RUN")" <<'PY'
import sys
p, r, app = sys.argv[1], sys.argv[2], sys.argv[3]; s = open(p, encoding='utf-8').read(); i = s.index('"windowTitle"')
s = s[:i] + ('"rubyLoadpath": ["%s/lib/ruby/3.3.0/x86_64-linux", "%s/lib/ruby/3.3.0"],\n    "vsync": false, "frameSkip": false,\n'
             '    "dataPathApp": "%s",\n    ') % (r, r, app) + s[i:]
open(p, 'w', encoding='utf-8').write(s)
PY
  cp "$B/mkxp-z/b/mkxp-z.x86_64" "$RUN/game/"
  echo "assembled $RUN/game"
}

run_plan() {
  plan="${1:-volcanic}"
  rm -rf "$RUN/game/Captures"; mkdir -p "$RUN/game/Captures" "$RUN/captures_keep"
  if [[ "${ISOLATE:-0}" == "1" ]]; then
    # Own display + renamed process names, so other tools' `pkill Xvfb` / `pkill mkxp` can't hit this run.
    mkdir -p "$RUN/bin"; cp /usr/bin/Xvfb "$RUN/bin/pfcap-display"; cp "$RUN/game/mkxp-z.x86_64" "$RUN/game/pfcap-engine"
    dn="${DISPLAY_NUM:-87}"
    "$RUN/bin/pfcap-display" ":$dn" -screen 0 1024x768x24 -nolisten tcp > "$RUN/display.log" 2>&1 &
    dpid=$!; sleep 2
    (cd "$RUN/game" && DISPLAY=":$dn" DEMO_PLAN="$plan" ALSOFT_DRIVERS=null timeout "${RUN_TIMEOUT:-1500}" \
       ./pfcap-engine debug > "$RUN/engine_stdout.txt" 2>&1) || true
    kill "$dpid" 2>/dev/null || true
  else
    (cd "$RUN/game" && DEMO_PLAN="$plan" ALSOFT_DRIVERS=null timeout "${RUN_TIMEOUT:-1500}" \
       xvfb-run -a -s "-screen 0 1024x768x24" ./mkxp-z.x86_64 debug > "$RUN/engine_stdout.txt" 2>&1) || true
  fi
  cat "$RUN/game/Captures/demo.log"
  for d in "$RUN"/game/Captures/*/; do n="$(basename "$d")"; rm -rf "$RUN/captures_keep/$n"; cp -r "$d" "$RUN/captures_keep/$n"; done
  cp "$RUN/game/Captures/demo.log" "$RUN/captures_keep/${plan//,/_}_demo.log"
}

case "${1:-}" in
  build) build ;;
  assemble) assemble ;;
  run) run_plan "${2:-volcanic}" ;;
  *) echo "usage: $0 build | assemble | run <volcanic|silkwood|zekrom,...>"; exit 1 ;;
esac
