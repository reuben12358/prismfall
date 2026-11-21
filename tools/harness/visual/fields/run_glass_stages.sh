#!/usr/bin/env bash
#===============================================================================
# Glass Dunes stage captures in the REAL engine (dev tool): Hot Glass cooling into Mirror Glass, and three Boombursts
# shattering Mirror Glass back into the Desert. Uses its own capture copy and display.
#   RUN=/home/claude/run_flcap bash run_glass_stages.sh [assemble]   # first time (needs /home/claude/run/build)
#   GS_PLANS=cool bash run_glass_stages.sh                           # one plan
#   FE_SRC=<dir with 1xx_Field_*.rb> ...                             # test field files that aren't in the kit yet
# Frames: $RUN/frames/gs_<plan>/f*.bmp (every GS_EVERY-th engine frame). GIFs: make_gif.py (see README).
#===============================================================================
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
VIS="$(cd "$HERE/.." && pwd)"
KIT="$(cd "$VIS/../../.." && pwd)"
export RUN="${RUN:-/home/claude/run_flcap}"
if [[ "${1:-}" == "assemble" || ! -d "$RUN/game" ]]; then
  mkdir -p "$RUN"; [[ -e "$RUN/build" ]] || ln -s /home/claude/run/build "$RUN/build"
  PACKAGE=0 bash "$VIS/run_engine_capture.sh" assemble
fi
G="$RUN/game"
# live kit plugins + field art (the capture copy always runs the current working tree)
for d in "$KIT"/plugins/*/; do n="$(basename "$d")"; rm -rf "$G/Plugins/$n"; cp -r "$d" "$G/Plugins/$n"; done
find "$G/Plugins" -name '__pycache__' -prune -exec rm -rf {} +
[[ -n "${FE_SRC:-}" ]] && cp "$FE_SRC"/1*.rb "$G/Plugins/Prismfall Field Effects/"
[[ -d "$KIT/graphics" ]] && cp -r "$KIT/graphics/." "$G/Graphics/"
cp "$HERE/005_GlassStageCapture.rb" "$G/Plugins/ZZ Demo Autorun/"
rm -rf "$G"/Captures/gs_*
DEMO_PLAN=glassstages ISOLATE=1 DISPLAY_NUM="${DISPLAY_NUM:-177}" RUN_TIMEOUT="${RUN_TIMEOUT:-1500}" \
  bash "$VIS/run_engine_capture.sh" run glassstages | grep -E "turn |msg:|field change|EXCEPTION|FATAL|Error|battle gs_" || true
mkdir -p "$RUN/frames"
for d in "$G"/Captures/gs_*/; do n="$(basename "$d")"; rm -rf "$RUN/frames/$n"; mv "$d" "$RUN/frames/$n"; done
rm -rf "$RUN"/captures_keep/gs_* "$RUN"/captures_keep/glassstages_demo.log
echo "frames: $RUN/frames"
