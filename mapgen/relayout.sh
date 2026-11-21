#!/usr/bin/env bash
# relayout.sh - after ANY change to the PF Rejuv sheet (a piece added in rdraw / tdraw / ndraw / gdraw, an image
# resized): rebuild the sheet, then re-run every layout script that writes PF Rejuv tile ids, then build.
# (MAPGEN.md 2n's run order, map builder 12.)  Usage: bash mapgen/relayout.sh [--strict]
set -euo pipefail
cd "$(dirname "$0")"
python3 -I rcustom.py && python3 -I rcompose.py && python3 -I rstamps.py
for s in ferrow_rj briarwick_rj dovetail ebbmouth saltmere_rj saltmere_interiors orchard trial_interiors early_interiors war routes_early rimewood caves tidelock manor circuit_gym lumen lumen_interiors; do
  echo "== layouts/$s.py"; python3 -I layouts/$s.py > /tmp/relayout_$s.log 2>&1 || { tail -20 /tmp/relayout_$s.log; exit 1; }
done
# 525 is built by routes_early (routes_craft.build_525, map builder 16): no reskin, no spec restore any more
python3 -I build.py "$@"
