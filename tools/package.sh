#!/usr/bin/env bash
# Builds dist/Prismfall_DevKit.zip — an overlay you copy into an Essentials v21.1 project.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$ROOT/dist/Prismfall_DevKit"
rm -rf "$ROOT/dist" && mkdir -p "$OUT/Plugins" "$OUT/PBS" "$OUT/Design" "$OUT/Story" "$OUT/Docs" "$OUT/Tools"

# Plugins (folder names are the plugin names)
cp -r "$ROOT/plugins/." "$OUT/Plugins/"

# PBS: shipped as suffixed files so stock PBS stays untouched (v21.1 merges PBS/<base>_<suffix>.txt)
declare -A PBS_MAP=(
  [trainer_types.txt]=trainer_types_prismfall.txt
  [trainers.txt]=trainers_prismfall.txt
  [items_fields.txt]=items_prismfall.txt
  [encounters.txt]=encounters_prismfall.txt
)
for src in "${!PBS_MAP[@]}"; do
  [[ -f "$ROOT/pbs/$src" ]] && cp "$ROOT/pbs/$src" "$OUT/PBS/${PBS_MAP[$src]}"
done
# Any other PBS additions keep their names
for f in "$ROOT"/pbs/*.txt; do
  b="$(basename "$f")"; [[ -n "${PBS_MAP[$b]:-}" ]] && continue; cp "$f" "$OUT/PBS/$b"
done

cp "$ROOT"/design/*.md "$OUT/Design/" 2>/dev/null || true
cp "$ROOT"/story/*.md  "$OUT/Story/"  2>/dev/null || true
cp "$ROOT"/docs/*.md   "$OUT/Docs/"   2>/dev/null || true
find "$ROOT/tools" -maxdepth 1 -type f ! -name package.sh -exec cp {} "$OUT/Tools/" \;
[[ -f "$ROOT/README.md" ]] && cp "$ROOT/README.md" "$OUT/README.md"

# Strip editor/OS junk, then zip
find "$OUT" -name '.DS_Store' -delete
(cd "$ROOT/dist" && zip -qr Prismfall_DevKit.zip Prismfall_DevKit)
echo "Built $ROOT/dist/Prismfall_DevKit.zip"
(cd "$ROOT/dist" && unzip -l Prismfall_DevKit.zip | tail -1)
