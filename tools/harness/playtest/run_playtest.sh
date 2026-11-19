#!/usr/bin/env bash
#===============================================================================
# Prismfall REAL-ENGINE playtest (Linux, headless). Dev tool only.
# A fresh copy of the base project gets the packaged kit exactly as README.md says
# (unzip dist/Prismfall_DevKit.zip, copy Plugins/ PBS/ Data/ Graphics/ in), then the
# dev-only "ZZ Playtest Bot" plugin plays it (see 001_PlaytestBot.rb).
#
#   bash run_playtest.sh assemble   # package, fresh copy, apply the kit, add the bot
#   bash run_playtest.sh install    # 1st Debug boot (compiles), New Game -> install offer -> quit
#   bash run_playtest.sh play       # restart, New Game, Debug > Files > Install (no-op), prologue
#   bash run_playtest.sh route1     # dev shortcut: start on Route 1 after K1, walk into its trainers
#   bash run_playtest.sh ch1        # resume at Route 1 (state as after K1) and play Chapter 1 to Briarwick
#   bash run_playtest.sh checks     # dev shortcut: glyph lines + quest log + every trainer added 2026-11-17
#   python3 make_playtest_media.py  # shots + GIF -> docs/playtest/
#
# Needs the mkxp-z build from tools/harness/visual/run_engine_capture.sh (build step).
# Test-copy-only changes: the bot plugin, mkxp.json (Ruby stdlib path, no vsync, own
# save folder "Prismfall Playtest") and the Linux engine binary. Nothing else is patched.
# The engine runs with a TZ whose local time is about 13:00 (override: PLAY_TZ) so Essentials' day/night tint
# shows the maps by day,
# on its own Xvfb display :147 (override: PLAY_DISPLAY) so it never collides with other engine runs.
#===============================================================================
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
KIT="$(cd "$HERE/../../.." && pwd)"
RUN="${RUN:-/home/claude/run}"
BASE="${BASE:-/home/claude/ref/ebdx_renovation}"
RUBY_HOME="${RUBY_HOME:-/opt/rbenv/versions/3.3.6}"
GAME="$RUN/playtest_game"
SAVE_DIR="$HOME/.local/share/Prismfall Playtest"

assemble() {
  (cd "$KIT" && bash tools/package.sh)
  rm -rf "$GAME" "$RUN/playtest_kit"; mkdir -p "$GAME" "$RUN/playtest_kit"
  (cd "$BASE" && tar cf - --exclude=.git .) | (cd "$GAME" && tar xf -)
  (cd "$RUN/playtest_kit" && unzip -q "$KIT/dist/Prismfall_DevKit.zip")
  K="$RUN/playtest_kit/Prismfall_DevKit"
  for d in Plugins PBS Data Graphics; do cp -r "$K/$d/." "$GAME/$d/"; done   # README step 2 (merge folders)
  mkdir -p "$GAME/Plugins/ZZ Playtest Bot"
  cp "$HERE/meta.txt" "$HERE/001_PlaytestBot.rb" "$GAME/Plugins/ZZ Playtest Bot/"
  python3 - "$GAME/mkxp.json" "$RUBY_HOME" <<'PY'
import sys
p, r = sys.argv[1], sys.argv[2]; s = open(p, encoding='utf-8').read(); i = s.index('"windowTitle"')
s = s[:i] + ('"rubyLoadpath": ["%s/lib/ruby/3.3.0/x86_64-linux", "%s/lib/ruby/3.3.0"],\n    "vsync": false, '
             '"frameSkip": false, "dataPathApp": "Prismfall Playtest",\n    ' % (r, r)) + s[i:]
open(p, 'w', encoding='utf-8').write(s)
PY
  cp "$RUN/build/mkxp-z/b/mkxp-z.x86_64" "$GAME/"
  echo "assembled $GAME"
}

# POSIX TZ whose local time is about 13:00 now (POSIX signs are inverted: PLAY5 = UTC-5)
midday_tz() {
  local off=$(( (13 - 10#$(date -u +%H) + 36) % 24 - 12 ))
  echo "PLAY$(( -off ))"
}

session() {
  [[ "$1" == install ]] && rm -rf "$SAVE_DIR"          # a fresh machine: no saves, no logs
  export PLAYBOT_STATE="$RUN/playtest_resume_state.txt"
  if [[ "$1" != resume ]]; then                          # resume: Continue from the bot's autosave, keep the output
    rm -f "$SAVE_DIR"/Game*.rxdata "$PLAYBOT_STATE"      # New Game must be the first load-screen entry
    rm -rf "$GAME/Playtest"
  fi
  mkdir -p "$RUN/playtest_out"
  (cd "$GAME" && PLAYBOT_SESSION="$1" TZ="${PLAY_TZ:-$(midday_tz)}" ALSOFT_DRIVERS=null timeout "${TIMEOUT:-2400}" \
     xvfb-run -n "${PLAY_DISPLAY:-147}" -s "-screen 0 1024x768x24" ./mkxp-z.x86_64 debug > "$RUN/playtest_$1_stdout.txt" 2>&1) || true
  o="$1"; [[ "$1" == resume ]] && o=play; rm -rf "$RUN/playtest_out/$o"; cp -r "$GAME/Playtest" "$RUN/playtest_out/$o" 2>/dev/null || true
  [[ -f "$SAVE_DIR/errorlog.txt" ]] && cp "$SAVE_DIR/errorlog.txt" "$RUN/playtest_out/$1/" || true
  grep -E "FATAL|STUCK|bot error|installer|plan done|finished" "$RUN/playtest_out/$1/bot.log" || true
}

# Stop only this test copy's engine (other engine runs may share the machine)
stop() {
  for p in $(pgrep -f mkxp-z.x86_64 || true); do
    [[ "$(readlink "/proc/$p/cwd" 2>/dev/null)" == "$GAME" ]] && kill "$p" && echo "stopped $p"
  done; true
}

case "${1:-}" in
  assemble) assemble ;;
  stop) stop ;;
  install|play|route1|checks|ch1|resume) session "$1" ;;
  *) echo "usage: $0 assemble | install | play | route1 | checks | ch1 | stop"; exit 1 ;;
esac
