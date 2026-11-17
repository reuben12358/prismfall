#!/usr/bin/env bash
# Builds docs/battle_captures/engine/slow/ from DEMO_SLOW=1 engine captures.
#   bash build_slow.sh [captures_keep_dir] [spec ...]     (default: all specs in slow_specs/)
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
KEEP="${1:-/home/claude/capture_slow/captures_keep}"; shift || true
OUT="$(cd "$HERE/../../.." && pwd)/docs/battle_captures/engine/slow"
mkdir -p "$OUT"
specs=("$@"); [[ ${#specs[@]} -eq 0 ]] && specs=("$HERE"/slow_specs/*.json)
for s in "${specs[@]}"; do
  tmp="$(mktemp)"; sed -e "s#@KEEP@#$KEEP#g" -e "s#@OUT@#$OUT#g" "$s" > "$tmp"
  python3 -I "$HERE/make_slow.py" "$tmp" 2>&1 | grep -v DeprecationWarning || true
  rm -f "$tmp"
done
