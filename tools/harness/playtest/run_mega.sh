#!/usr/bin/env bash
#===============================================================================
# Prismfall REAL-ENGINE Mega Evolution capture (Linux, headless). Dev tool only.
# Its own lean game copy ($RUN/mega_game: Audio and the big unchanged Graphics folders are HARD LINKS to the read-only
# base, so they take no disk space; mkxp-z's PhysFS won't follow symlinks), save folder ("Prismfall Mega") and Xvfb display (PLAY_DISPLAY, default 211), so it never collides with the
# other runners. The kit is copied straight from the working tree (the folders tools/package.sh ships), then the
# dev-only bot (001_PlaytestBot.rb + 002_PuzzleBot.rb + 004_MegaBot.rb) plays.
#
#   bash run_mega.sh assemble    # lean base copy + Plugins/PBS/Data/Graphics + bot
#   bash run_mega.sh install     # first Debug boot (compiles), New Game -> install offer -> quit
#   bash run_mega.sh mega        # the player's Fight menu: Mega button -> Mega Charizard X; the AI's Mega Camerupt
#   bash run_mega.sh gif         # slow GIF of the Mega Evolution from the recorded frames, then deletes the frames
#   bash run_mega.sh stop        # stops only this copy's engine
#   bash run_mega.sh clean       # removes the game copy and the save folder
#===============================================================================
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
KIT="$(cd "$HERE/../../.." && pwd)"
RUN="${RUN:-/home/claude/work/mega/engine}"
BASE="${BASE:-/home/claude/ref/ebdx_renovation}"
ENGINE="${ENGINE:-/home/claude/run/build/mkxp-z/b/mkxp-z.x86_64}"
RUBY_HOME="${RUBY_HOME:-/opt/rbenv/versions/3.3.6}"
GAME="$RUN/mega_game"
SAVE_DIR="$HOME/.local/share/Prismfall Mega"
# Graphics folders the kit writes into are copied; everything else is hard-linked from the base (same filesystem;
# the engine never writes into Graphics or Audio, and "clean" only removes the links).
COPY_GFX="Characters EBDX UI Tilesets Autotiles Fogs Battlebacks Pictures"

assemble() {
  rm -rf "$GAME"; mkdir -p "$GAME/Graphics"
  (cd "$BASE" && tar cf - --exclude=.git --exclude=./Graphics --exclude=./Audio .) | (cd "$GAME" && tar xf -)
  cp -al "$BASE/Audio" "$GAME/Audio"
  for d in "$BASE"/Graphics/*/; do
    n="$(basename "$d")"
    if [[ " $COPY_GFX " == *" $n "* ]]; then cp -r "$d" "$GAME/Graphics/$n"; else cp -al "$BASE/Graphics/$n" "$GAME/Graphics/$n"; fi
  done
  cp -r "$KIT/plugins/." "$GAME/Plugins/"; cp -r "$KIT/maps_out/Plugins/." "$GAME/Plugins/"
  find "$GAME/Plugins" -name '__pycache__' -prune -exec rm -rf {} +
  declare -A PBS_MAP=([trainer_types.txt]=trainer_types_prismfall.txt [trainers.txt]=trainers_prismfall.txt
                      [items_fields.txt]=items_prismfall.txt [encounters.txt]=encounters_prismfall.txt
                      [town_map.txt]=town_map_prismfall.txt)
  for f in "$KIT"/pbs/*.txt; do b="$(basename "$f")"; cp "$f" "$GAME/PBS/${PBS_MAP[$b]:-$b}"; done
  cp "$KIT"/maps_out/PBS/*.txt "$GAME/PBS/"
  cp "$KIT"/maps_out/Data/Map*.rxdata "$KIT/maps_out/Data/mapinfos_prismfall.txt" "$KIT/maps_out/Data/Tilesets_prismfall.rxdata" \
     "$KIT/maps_out/Data/system_prismfall.txt" "$GAME/Data/"
  for sub in Tilesets Autotiles Fogs; do mkdir -p "$GAME/Graphics/$sub"; cp "$KIT/maps_out/Graphics/$sub/"*.png "$GAME/Graphics/$sub/"; done
  [[ -d "$KIT/graphics" ]] && cp -r "$KIT/graphics/." "$GAME/Graphics/"
  mkdir -p "$GAME/Plugins/ZZ Playtest Bot"
  cp "$HERE/meta.txt" "$HERE/001_PlaytestBot.rb" "$HERE/002_PuzzleBot.rb" "$HERE/004_MegaBot.rb" "$GAME/Plugins/ZZ Playtest Bot/"
  python3 - "$GAME/mkxp.json" "$RUBY_HOME" <<'PY'
import sys
p, r = sys.argv[1], sys.argv[2]; s = open(p, encoding='utf-8').read(); i = s.index('"windowTitle"')
s = s[:i] + ('"rubyLoadpath": ["%s/lib/ruby/3.3.0/x86_64-linux", "%s/lib/ruby/3.3.0"],\n    "vsync": false, '
             '"frameSkip": false, "dataPathApp": "Prismfall Mega",\n    ' % (r, r)) + s[i:]
open(p, 'w', encoding='utf-8').write(s)
PY
  cp "$ENGINE" "$GAME/"
  du -sh "$GAME" | sed 's/^/assembled (lean): /'
}

midday_tz() { local off=$(( (13 - 10#$(date -u +%H) + 36) % 24 - 12 )); echo "PLAY$(( -off ))"; }

session() {
  [[ "$1" == install ]] && rm -rf "$SAVE_DIR"
  rm -f "$SAVE_DIR"/Game*.rxdata
  rm -rf "$GAME/Playtest"; mkdir -p "$RUN/mega_out"
  (cd "$GAME" && PLAYBOT_SESSION="$1" PLAYBOT_REC_EVERY="${REC_EVERY:-2}" TZ="${PLAY_TZ:-$(midday_tz)}" ALSOFT_DRIVERS=null timeout "${TIMEOUT:-1500}" \
     xvfb-run -n "${PLAY_DISPLAY:-211}" -s "-screen 0 1024x768x24" ./mkxp-z.x86_64 debug > "$RUN/mega_$1_stdout.txt" 2>&1) || true
  rm -rf "$RUN/mega_out/$1"; mv "$GAME/Playtest" "$RUN/mega_out/$1" 2>/dev/null || true
  [[ -f "$SAVE_DIR/errorlog.txt" ]] && cp "$SAVE_DIR/errorlog.txt" "$RUN/mega_out/$1/" || true
  grep -E "FATAL|STUCK|bot error|installer|plan done|finished|MG" "$RUN/mega_out/$1/bot.log" || true
}

gif() {
  python3 -I "$HERE/make_mega_gif.py" "$RUN/mega_out/mega" "${OUT:-$KIT/docs/battle_captures/mega}"
  rm -rf "$RUN/mega_out/mega/frames"
}

stop() {
  for p in $(pgrep -f mkxp-z.x86_64 || true); do
    [[ "$(readlink "/proc/$p/cwd" 2>/dev/null)" == "$GAME" ]] && kill "$p" && echo "stopped $p"
  done; true
}

case "${1:-}" in
  assemble) assemble ;;
  stop) stop ;;
  install|mega) session "$1" ;;
  gif) gif ;;
  clean) rm -rf "$GAME" "$SAVE_DIR"; echo "removed $GAME and $SAVE_DIR" ;;
  *) echo "usage: $0 assemble | install | mega | gif | stop | clean"; exit 1 ;;
esac
