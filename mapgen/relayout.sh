#!/usr/bin/env bash
# relayout.sh - after ANY change to the PF Rejuv sheet (a piece added in rdraw / tdraw / ndraw / gdraw, an image
# resized): rebuild the sheet, then re-run every layout script that writes PF Rejuv tile ids, then build.
# (MAPGEN.md 2n's run order, map builder 12.)  Usage: bash mapgen/relayout.sh [--strict]
set -euo pipefail
cd "$(dirname "$0")"
python3 -I rcustom.py && python3 -I rcompose.py && python3 -I rstamps.py
for s in ferrow_rj briarwick_rj dovetail ebbmouth saltmere_rj saltmere_interiors orchard trial_interiors early_interiors war routes_early rimewood caves; do
  echo "== layouts/$s.py"; python3 -I layouts/$s.py > /tmp/relayout_$s.log 2>&1 || { tail -20 /tmp/relayout_$s.log; exit 1; }
done
python3 -I layouts/reskin.py 525 > /tmp/relayout_reskin.log 2>&1
git checkout -- specs/525_deepwood_cocoonfall.yaml       # reskin rewrites it; 548 is written by deepwood.py 548 alone
python3 -I build.py "$@"
