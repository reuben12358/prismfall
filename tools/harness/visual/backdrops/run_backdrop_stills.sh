#!/usr/bin/env bash
#===============================================================================
# Backdrop stills in the REAL engine (dev tool). One wild battle per field, shot on
# the first command phase.  Uses its own capture copy and display.
#   RUN=/home/claude/run_backdrops bash run_backdrop_stills.sh [assemble]   # first time
#   BD_FIELDS=VOLCANIC,FLOWER_GARDEN:3 bash run_backdrop_stills.sh           # some fields
#   BD_TIME=night BD_VECTORS=1 bash run_backdrop_stills.sh
# Shots land in $RUN/captures_keep/backdrops/.  Contact sheet: make_contact_sheet.py.
#===============================================================================
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
VIS="$(cd "$HERE/.." && pwd)"
KIT="$(cd "$VIS/../../.." && pwd)"
export RUN="${RUN:-/home/claude/run_backdrops}"
if [[ "${1:-}" == "assemble" || ! -d "$RUN/game" ]]; then
  mkdir -p "$RUN"; [[ -e "$RUN/build" ]] || ln -s /home/claude/run/build "$RUN/build"
  PACKAGE=0 bash "$VIS/run_engine_capture.sh" assemble
fi
G="$RUN/game"
# live kit plugins + field art (the capture copy always runs the current working tree)
for d in "$KIT"/plugins/*/; do n="$(basename "$d")"; rm -rf "$G/Plugins/$n"; cp -r "$d" "$G/Plugins/$n"; done
find "$G/Plugins" -name '__pycache__' -prune -exec rm -rf {} +
[[ -d "$KIT/graphics" ]] && cp -r "$KIT/graphics/." "$G/Graphics/"
cp "$HERE/002_BackdropStills.rb" "$G/Plugins/ZZ Demo Autorun/"
rm -rf "$G/Captures/backdrops"
DEMO_PLAN=backdrops ISOLATE=1 DISPLAY_NUM="${DISPLAY_NUM:-141}" RUN_TIMEOUT="${RUN_TIMEOUT:-2400}" \
  bash "$VIS/run_engine_capture.sh" run backdrops | grep -E "backdrop still|EXCEPTION|FATAL|Error" || true
mkdir -p "$RUN/captures_keep/backdrops"
cp "$G"/Captures/backdrops/*.png "$RUN/captures_keep/backdrops/" 2>/dev/null || true
grep -h "Prismfall EBDX Bridge" "$G"/Data/debuglog.txt 2>/dev/null | tail -20 || true
echo "shots: $RUN/captures_keep/backdrops"
