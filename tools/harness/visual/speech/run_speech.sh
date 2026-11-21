#!/usr/bin/env bash
#===============================================================================
# Trainer speech capture in the REAL engine (dev tool). See 004_SpeechCapture.rb.
#   RUN=/home/claude/run_place SP_CASES="celestine,ebdx_demo" bash run_speech.sh
# Needs an assembled capture copy at $RUN/game. PP_PLUGINS=<dir>: Prismfall plugins from there instead of the
# working tree. Frames + speech.tsv: $RUN/speech/ (replaced on every run).
#===============================================================================
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
VIS="$(cd "$HERE/.." && pwd)"
KIT="$(cd "$VIS/../../.." && pwd)"
export RUN="${RUN:-/home/claude/run_place}"
G="$RUN/game"
[[ -d "$G" ]] || { echo "no capture copy at $G"; exit 1; }
PL="${PP_PLUGINS:-$KIT/plugins}"
for d in "$PL"/*/; do n="$(basename "$d")"; rm -rf "$G/Plugins/$n"; cp -r "$d" "$G/Plugins/$n"; done
find "$G/Plugins" -name '__pycache__' -prune -exec rm -rf {} +
[[ -d "$KIT/graphics" ]] && cp -r "$KIT/graphics/." "$G/Graphics/"
rm -f "$G/Plugins/ZZ Demo Autorun/002_BackdropStills.rb" "$G/Plugins/ZZ Demo Autorun/003_PlacementProbe.rb"
cp "$VIS/001_DemoAutorun.rb" "$VIS/meta.txt" "$G/Plugins/ZZ Demo Autorun/"
cp "$HERE/004_SpeechCapture.rb" "$G/Plugins/ZZ Demo Autorun/"
DEMO_PLAN=speech ISOLATE=1 DISPLAY_NUM="${DISPLAY_NUM:-175}" RUN_TIMEOUT="${RUN_TIMEOUT:-900}" \
  bash "$VIS/run_engine_capture.sh" run speech | grep -E "speech |EXCEPTION|FATAL|Error" || true
rm -rf "$RUN/speech"; mkdir -p "$RUN/speech"
cp "$G"/Captures/speech/* "$RUN/speech/" 2>/dev/null || true
for d in "$G"/Captures/sp_*/; do [[ -n "$(ls -A "$d" 2>/dev/null)" ]] && cp -r "$d" "$RUN/speech/"; done
rm -rf "$RUN/captures_keep"
echo "frames: $RUN/speech"
