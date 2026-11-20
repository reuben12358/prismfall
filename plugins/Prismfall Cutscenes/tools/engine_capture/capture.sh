#!/usr/bin/env bash
#===============================================================================
# Real-engine cutscene capture (dev tool). Reuses the mkxp-z binary built by
# tools/harness/visual/run_engine_capture.sh; everything else happens in its own
# copy under $RUN so other capture/playtest runs are never touched.
#   bash capture.sh assemble            # base project + kit plugins + this plugin + autorun
#   bash capture.sh sync                # re-copy only the Cutscenes plugin (after edits)
#   CUT_VARS=variant=A bash capture.sh run WAR_CLIMAX
#   bash capture.sh portraits           # 1st boot installs the maps, 2nd takes the face/bubble shots
#   bash capture.sh clean               # delete the run copy (disk is limited)
# Frames: $RUN/game/Captures/frames/f*.png (+ frames.tsv with scene times), log: cut.log
# Portrait shots: $RUN/game/Captures/shots/portraits_*.png (copy the keepers to docs/playtest/)
# The copy is lean: the base project's files are hard links, except Data/, PBS/, Plugins/ and
# mkxp.json (the engine and the installer write those); kit and art files replace links, never write
# through them. The project's own art (art/out/Graphics: portraits, charsets) is copied in too.
#===============================================================================
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
PLUGIN="$(cd "$HERE/../.." && pwd)"
KIT="$(cd "$PLUGIN/../.." && pwd)"
RUN="${RUN:-/tmp/pfcut_run}"
BASE="${BASE:-/home/claude/ref/ebdx_renovation}"
ENGINE="${ENGINE:-/home/claude/run/build/mkxp-z/b/mkxp-z.x86_64}"
RUBY_HOME="${RUBY_HOME:-/opt/rbenv/versions/3.3.6}"

sync_plugin() {
  rm -rf "$RUN/game/Plugins/Prismfall Cutscenes"
  cp -r "$PLUGIN" "$RUN/game/Plugins/Prismfall Cutscenes"
  rm -rf "$RUN/game/Plugins/Prismfall Cutscenes/selftest" "$RUN/game/Plugins/Prismfall Cutscenes/tools"
  mkdir -p "$RUN/game/Plugins/ZZ Cutscene Autorun"
  cp "$HERE/autorun.ruby_stub" "$RUN/game/Plugins/ZZ Cutscene Autorun/001_Autorun.rb"
  printf 'Name       = ZZ Cutscene Autorun\nVersion    = 1.0.0\nEssentials = 21.1\nRequires   = Prismfall Cutscenes\nCredits    = dev-only capture tool\n' \
    > "$RUN/game/Plugins/ZZ Cutscene Autorun/meta.txt"
  rm -f "$RUN/game/Data/PluginScripts.rxdata"
}

assemble() {
  mkdir -p "$RUN"; rm -rf "$RUN/game"; cp -al "$BASE" "$RUN/game"
  for d in Data PBS Plugins; do rm -rf "$RUN/game/$d"; cp -r "$BASE/$d" "$RUN/game/$d"; done
  rm -f "$RUN/game/mkxp.json"; cp "$BASE/mkxp.json" "$RUN/game/mkxp.json"
  D="$KIT/dist/Prismfall_DevKit"
  cp -r "$D/Plugins/." "$RUN/game/Plugins/"; cp "$D"/PBS/*.txt "$RUN/game/PBS/"; cp "$D"/Data/* "$RUN/game/Data/"
  [[ -d "$D/Graphics" ]] && cp -r --remove-destination "$D/Graphics/." "$RUN/game/Graphics/"
  [[ -d "$KIT/art/out/Graphics" ]] && cp -r --remove-destination "$KIT/art/out/Graphics/." "$RUN/game/Graphics/"
  sed -i '4s/^class PokemonSprite < SpriteWrapper/class PokemonSprite   # capture-copy patch: superclass mismatch/' \
    "$RUN/game/Plugins/Elite Battle DX/[000] Scripts/Battle UI/UI Fixes.rb"
  python3 - "$RUN/game/mkxp.json" "$RUBY_HOME" "PrismfallCutCapture" <<'PY'
import sys
p, r, app = sys.argv[1], sys.argv[2], sys.argv[3]; s = open(p, encoding='utf-8').read(); i = s.index('"windowTitle"')
s = s[:i] + ('"rubyLoadpath": ["%s/lib/ruby/3.3.0/x86_64-linux", "%s/lib/ruby/3.3.0"],\n    "vsync": false, "frameSkip": false,\n'
             '    "dataPathApp": "%s",\n    ') % (r, r, app) + s[i:]
open(p, 'w', encoding='utf-8').write(s)
PY
  cp "$ENGINE" "$RUN/game/pfcut-engine"
  sync_plugin
  echo "assembled $RUN/game"
}

# POSIX TZ whose local time is about 13:00 now, so Essentials' day/night tint shows maps by day
midday_tz() {
  local off=$(( (13 - 10#$(date -u +%H) + 36) % 24 - 12 ))
  echo "PFCUT$(( -off ))"
}

run_cut() {
  rm -rf "$RUN/game/Captures"; mkdir -p "$RUN/game/Captures/frames" "$RUN/bin"
  cp /usr/bin/Xvfb "$RUN/bin/pfcut-display"
  dn="${DISPLAY_NUM:-163}"
  "$RUN/bin/pfcut-display" ":$dn" -screen 0 1024x768x24 -nolisten tcp > "$RUN/display.log" 2>&1 &
  dpid=$!; sleep 2
  (cd "$RUN/game" && DISPLAY=":$dn" CUT_ID="${1:-WAR_CLIMAX}" TZ="${CUT_TZ:-$(midday_tz)}" ALSOFT_DRIVERS=null timeout "${RUN_TIMEOUT:-1500}" \
     ./pfcut-engine debug > "$RUN/engine_stdout.txt" 2>&1) || true
  kill "$dpid" 2>/dev/null || true
  cat "$RUN/game/Captures/cut.log" 2>/dev/null || tail -30 "$RUN/engine_stdout.txt"
}

case "${1:-}" in
  assemble) assemble ;;
  sync) sync_plugin ;;
  run) run_cut "${2:-WAR_CLIMAX}" ;;
  portraits) run_cut PF_INSTALL; run_cut PORTRAITS; ls "$RUN/game/Captures/shots/" ;;
  clean) rm -rf "$RUN" ;;
  *) echo "usage: $0 assemble | sync | run <SCENE_ID> | portraits | clean"; exit 1 ;;
esac
