#!/usr/bin/env bash
#===============================================================================
# Battler placement probe in the REAL engine (dev tool). See 003_PlacementProbe.rb.
#   RUN=/home/claude/run_place PP_CASES="MEADOW:TAUROS/LUCARIO;VOLCANIC:TORKOAL/SNORLAX" PP_VECTORS=1 \
#     bash run_placement.sh
#   PP_GROUND=0 PP_GRAPHICS=/tmp/old_art  ... "before" shots (EBDX's own metrics, older room art)
# Needs an assembled capture copy at $RUN/game (run_engine_capture.sh assemble, or a copy of one).
# The copy always runs the current working tree's plugins and graphics.
# Shots + probe.tsv: $RUN/placement/ (replaced on every run).
#===============================================================================
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
VIS="$(cd "$HERE/.." && pwd)"
KIT="$(cd "$VIS/../../.." && pwd)"
export RUN="${RUN:-/home/claude/run_place}"
G="$RUN/game"
[[ -d "$G" ]] || { echo "no capture copy at $G"; exit 1; }
for d in "$KIT"/plugins/*/; do n="$(basename "$d")"; rm -rf "$G/Plugins/$n"; cp -r "$d" "$G/Plugins/$n"; done
find "$G/Plugins" -name '__pycache__' -prune -exec rm -rf {} +
[[ -d "$KIT/graphics" ]] && cp -r "$KIT/graphics/." "$G/Graphics/"
# PP_GRAPHICS=<dir>: laid over Graphics/ after the kit (e.g. old room art for "before" shots)
[[ -n "${PP_GRAPHICS:-}" ]] && cp -r "$PP_GRAPHICS/." "$G/Graphics/"
rm -f "$G/Plugins/ZZ Demo Autorun/002_BackdropStills.rb"
cp "$VIS/001_DemoAutorun.rb" "$VIS/meta.txt" "$G/Plugins/ZZ Demo Autorun/"
cp "$HERE/003_PlacementProbe.rb" "$G/Plugins/ZZ Demo Autorun/"
DEMO_PLAN=placement ISOLATE=1 DISPLAY_NUM="${DISPLAY_NUM:-173}" RUN_TIMEOUT="${RUN_TIMEOUT:-1800}" \
  bash "$VIS/run_engine_capture.sh" run placement | grep -E "placement |EXCEPTION|FATAL|Error" || true
rm -rf "$RUN/placement"; mkdir -p "$RUN/placement"
cp "$G"/Captures/placement/* "$RUN/placement/" 2>/dev/null || true
for d in "$G"/Captures/pp_*/; do [[ -n "$(ls -A "$d" 2>/dev/null)" ]] && cp -r "$d" "$RUN/placement/"; done
rm -rf "$RUN/captures_keep"
echo "shots: $RUN/placement"
