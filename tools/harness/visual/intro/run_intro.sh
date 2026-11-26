#!/usr/bin/env bash
#===============================================================================
# Trainer battle opening in the REAL engine (dev tool): Juno's line with her portrait -> EBDX integrated VS
# -> "You are challenged by Rival Juno!" -> send-outs. Re-run with new art:
#   bash run_intro.sh [--art DIR] [--player A|B]     DIR = a Graphics/ tree (Trainers/, Characters/, Portraits/...)
#   RUN=/home/claude/run_intro (default)  needs /home/claude/run/build (mkxp-z build)
#===============================================================================
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"; VIS="$(cd "$HERE/.." && pwd)"; KIT="$(cd "$VIS/../../.." && pwd)"
ART=""; PLAYER="A"; CAPTURE="$HERE/006_IntroCapture.rb"; PLAN="intro"
while [[ $# -gt 0 ]]; do case "$1" in --art) ART="$2"; shift 2;; --player) PLAYER="$2"; shift 2;; --capture) CAPTURE="$2"; shift 2;; --plan) PLAN="$2"; shift 2;; *) shift;; esac; done
export RUN="${RUN:-/home/claude/run_intro}"
if [[ ! -d "$RUN/game" ]]; then
  mkdir -p "$RUN"; [[ -e "$RUN/build" ]] || ln -s /home/claude/run/build "$RUN/build"
  PACKAGE=0 bash "$VIS/run_engine_capture.sh" assemble
  python3 -I "$KIT/mapgen/merge_tilesets.py" "$RUN/game" | tail -1   # the overworld half needs the Prismfall tilesets
fi
G="$RUN/game"
for d in "$KIT"/plugins/*/; do n="$(basename "$d")"; rm -rf "$G/Plugins/$n"; cp -r "$d" "$G/Plugins/$n"; done
find "$G/Plugins" -name '__pycache__' -prune -exec rm -rf {} +
[[ -d "$KIT/graphics" ]] && cp -r "$KIT/graphics/." "$G/Graphics/"
[[ -d "$KIT/art/out/Graphics" ]] && cp -r "$KIT/art/out/Graphics/." "$G/Graphics/"
[[ -n "$ART" ]] && cp -r "$ART/." "$G/Graphics/"
# current maps and tilesets (the assembled copy may predate them): tileset registry, map data, MapInfos
cp -r "$KIT/maps_out/Graphics/." "$G/Graphics/" 2>/dev/null || true
cp -r "$KIT/maps_out/Plugins/." "$G/Plugins/" 2>/dev/null || true   # map helpers (Prismfall Maps)
python3 -I "$KIT/mapgen/merge_tilesets.py" "$G" --force | tail -1
# ...then Gemini's Gen 5 reskin of those sheets on top, as tools/package.sh ships it (stale sheets are skipped);
# after merge_tilesets, which copies the mapgen sheets in again. PF_NO_GEN5=1 captures the plain mapgen look.
python3 -I "$KIT/tools/overlay_reskin.py" "$G/Graphics" | tail -1
python3 -I "$KIT/mapgen/merge_mapinfos.py" "$G" --force 2>&1 | tail -1
cp "$KIT/pbs/trainer_types.txt" "$G/PBS/trainer_types_prismfall.txt"   # current trainer types (PLAYER_A/B)
rm -f "$G/Data/trainer_types.dat"                                         # a missing .dat makes Essentials recompile PBS
cp "$KIT/pbs/trainers.txt" "$G/PBS/trainers_prismfall.txt"             # current trainers (Ch8 Hammer/Lieutenant)
rm -f "$G/Data/trainers.dat"
cp "$VIS/001_DemoAutorun.rb" "$G/Plugins/ZZ Demo Autorun/"; rm -f "$G/Plugins/ZZ Demo Autorun/"00[6-9]_*.rb; cp "$CAPTURE" "$G/Plugins/ZZ Demo Autorun/"
rm -rf "$G"/Captures/intro_* "$G"/Captures/tap_* "$G"/Captures/ch[0-9]*_*
IC_FOE="${IC_FOE:-}" IC_PLAYER="$PLAYER" DEMO_PLAN="$PLAN" ISOLATE=1 DISPLAY_NUM="${DISPLAY_NUM:-178}" RUN_TIMEOUT="${RUN_TIMEOUT:-900}" \
  bash "$VIS/run_engine_capture.sh" run "$PLAN" | grep -E "intro|tap|command|EXCEPTION|FATAL|Error|player trainer|RESULT" || true
mkdir -p "$RUN/frames"
for d in "$G"/Captures/intro_*/ "$G"/Captures/tap_*/ "$G"/Captures/ch[0-9]*_*/; do [[ -d "$d" ]] || continue; n="$(basename "$d")"; rm -rf "$RUN/frames/$n"; mv "$d" "$RUN/frames/$n"; done
cp "$G/Captures/demo.log" "$RUN/frames/" 2>/dev/null || true
echo "frames: $RUN/frames"
