#!/usr/bin/env bash
#===============================================================================
# Prismfall REAL-ENGINE Z-Power / Eevee Octave proof (Linux, headless). Dev tool only.
# Its own contained game copy ($RUN/zpower_game), save folder ("Prismfall ZPower") and Xvfb display (first free from :193), so
# it never collides with run_playtest.sh, run_puzzles.sh or the battle captures. Use your own RUN folder
# (RUN=/path; it needs build/mkxp-z/b/mkxp-z.x86_64). The kit is copied straight from the working tree (same folders
# tools/package.sh ships), then the dev-only bot (001_PlaytestBot.rb + 002_PuzzleBot.rb + 003_ZPowerBot.rb) plays.
#
#   bash run_zpower.sh assemble    # fresh base copy + Plugins/PBS/Data/Graphics + bot
#   bash run_zpower.sh install     # first Debug boot (compiles), New Game -> install offer -> quit
#   bash run_zpower.sh zpower      # the player's own Fight menu: Scald -> "Unleash ... Z-Power?" -> Yes -> Hydro Vortex
#   bash run_zpower.sh zgauntlet   # Vesper's event script: the 9-bout gauntlet in a set help order (AI plays the player)
#   bash run_zpower.sh stop        # stops only this copy's engine
#===============================================================================
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
KIT="$(cd "$HERE/../../.." && pwd)"
RUN="${RUN:-/home/claude/run}"
BASE="${BASE:-/home/claude/ref/ebdx_renovation}"
RUBY_HOME="${RUBY_HOME:-/opt/rbenv/versions/3.3.6}"
GAME="$RUN/zpower_game"
SAVE_DIR="$HOME/.local/share/Prismfall ZPower"

assemble() {
  rm -rf "$GAME"; mkdir -p "$GAME"
  (cd "$BASE" && tar cf - --exclude=.git .) | (cd "$GAME" && tar xf -)
  cp -r "$KIT/plugins/." "$GAME/Plugins/"; cp -r "$KIT/maps_out/Plugins/." "$GAME/Plugins/"
  find "$GAME/Plugins" -name '__pycache__' -prune -exec rm -rf {} +
  declare -A PBS_MAP=([trainer_types.txt]=trainer_types_prismfall.txt [trainers.txt]=trainers_prismfall.txt
                      [items_fields.txt]=items_prismfall.txt [encounters.txt]=encounters_prismfall.txt)
  for f in "$KIT"/pbs/*.txt; do b="$(basename "$f")"; cp "$f" "$GAME/PBS/${PBS_MAP[$b]:-$b}"; done
  cp "$KIT"/maps_out/PBS/*.txt "$GAME/PBS/"
  # maps_out/Data/Tilesets_prismfall.rxdata is the map builder's (mapgen/export_tilesets_rxdata.py): copied as it is, not rebuilt here
  cp "$KIT"/maps_out/Data/Map*.rxdata "$KIT/maps_out/Data/mapinfos_prismfall.txt" "$KIT/maps_out/Data/Tilesets_prismfall.rxdata" \
     "$KIT/maps_out/Data/system_prismfall.txt" "$GAME/Data/"
  for sub in Tilesets Autotiles Fogs; do mkdir -p "$GAME/Graphics/$sub"; cp "$KIT/maps_out/Graphics/$sub/"*.png "$GAME/Graphics/$sub/"; done
  [[ -d "$KIT/graphics" ]] && cp -r "$KIT/graphics/." "$GAME/Graphics/"
  mkdir -p "$GAME/Plugins/ZZ Playtest Bot"
  cp "$HERE/meta.txt" "$HERE/001_PlaytestBot.rb" "$HERE/002_PuzzleBot.rb" "$HERE/003_ZPowerBot.rb" "$GAME/Plugins/ZZ Playtest Bot/"
  python3 - "$GAME/mkxp.json" "$RUBY_HOME" <<'PY'
import sys
p, r = sys.argv[1], sys.argv[2]; s = open(p, encoding='utf-8').read(); i = s.index('"windowTitle"')
s = s[:i] + ('"rubyLoadpath": ["%s/lib/ruby/3.3.0/x86_64-linux", "%s/lib/ruby/3.3.0"],\n    "vsync": false, '
             '"frameSkip": false, "dataPathApp": "Prismfall ZPower",\n    ' % (r, r)) + s[i:]
open(p, 'w', encoding='utf-8').write(s)
PY
  cp "$RUN/build/mkxp-z/b/mkxp-z.x86_64" "$GAME/"
  echo "assembled $GAME"
}

midday_tz() { local off=$(( (13 - 10#$(date -u +%H) + 36) % 24 - 12 )); echo "PLAY$(( -off ))"; }

session() {
  [[ "$1" == install ]] && rm -rf "$SAVE_DIR"
  rm -f "$SAVE_DIR"/Game*.rxdata
  rm -rf "$GAME/Playtest"; mkdir -p "$RUN/zpower_out"
  (cd "$GAME" && PLAYBOT_SESSION="$1" PLAYBOT_REC_EVERY="${REC_EVERY:-4}" TZ="${PLAY_TZ:-$(midday_tz)}" ALSOFT_DRIVERS=null timeout "${TIMEOUT:-1800}" \
     xvfb-run -a -n "${PLAY_DISPLAY:-193}" -s "-screen 0 1024x768x24" ./mkxp-z.x86_64 debug > "$RUN/zpower_$1_stdout.txt" 2>&1) || true
  rm -rf "$RUN/zpower_out/$1"; cp -r "$GAME/Playtest" "$RUN/zpower_out/$1" 2>/dev/null || true
  [[ -f "$SAVE_DIR/errorlog.txt" ]] && cp "$SAVE_DIR/errorlog.txt" "$RUN/zpower_out/$1/" || true
  grep -E "FATAL|STUCK|bot error|installer|plan done|finished|ZP" "$RUN/zpower_out/$1/bot.log" || true
}

stop() {
  for p in $(pgrep -f mkxp-z.x86_64 || true); do
    [[ "$(readlink "/proc/$p/cwd" 2>/dev/null)" == "$GAME" ]] && kill "$p" && echo "stopped $p"
  done; true
}

case "${1:-}" in
  assemble) assemble ;;
  stop) stop ;;
  install|zpower|zgauntlet) session "$1" ;;
  *) echo "usage: $0 assemble | install | zpower | zgauntlet | stop"; exit 1 ;;
esac
