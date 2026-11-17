#!/usr/bin/env bash
# Builds dist/Prismfall_DevKit.zip — an overlay you copy into an Essentials v21.1 + EBDX project.
# Layout mirrors a project root: Plugins/, PBS/, Data/, Graphics/ can be copied straight in (nothing overwrites stock files).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$ROOT/dist/Prismfall_DevKit"
rm -rf "$ROOT/dist" && mkdir -p "$OUT"/{Plugins,PBS,Data,Design,Story,Docs,Tools/mapgen}

# Plugins: ours + the generated maps runtime/installer plugin(s)
cp -r "$ROOT/plugins/." "$OUT/Plugins/"
[[ -d "$ROOT/maps_out/Plugins" ]] && cp -r "$ROOT/maps_out/Plugins/." "$OUT/Plugins/"
find "$OUT/Plugins" -name '__pycache__' -prune -exec rm -rf {} +

# PBS: suffixed files so stock PBS stays untouched (v21.1 merges PBS/<base>_<suffix>.txt)
declare -A PBS_MAP=(
  [trainer_types.txt]=trainer_types_prismfall.txt
  [trainers.txt]=trainers_prismfall.txt
  [items_fields.txt]=items_prismfall.txt
  [encounters.txt]=encounters_prismfall.txt
)
for src in "${!PBS_MAP[@]}"; do
  [[ -f "$ROOT/pbs/$src" ]] && cp "$ROOT/pbs/$src" "$OUT/PBS/${PBS_MAP[$src]}"
done
for f in "$ROOT"/pbs/*.txt; do
  b="$(basename "$f")"; [[ -n "${PBS_MAP[$b]:-}" ]] && continue; cp "$f" "$OUT/PBS/$b"
done
[[ -d "$ROOT/maps_out/PBS" ]] && cp "$ROOT"/maps_out/PBS/*.txt "$OUT/PBS/"

# Data: generated maps + the MapInfos entry list + our RPG::Tileset entries + our switch/variable names (merged
# in-game by Debug > Files > Install Prismfall maps; we never ship MapInfos, Tilesets or System.rxdata)
cp "$ROOT"/maps_out/Data/Map*.rxdata "$OUT/Data/" 2>/dev/null || true
[[ -f "$ROOT/maps_out/Data/mapinfos_prismfall.txt" ]] && cp "$ROOT/maps_out/Data/mapinfos_prismfall.txt" "$OUT/Data/"
if [[ -f "$ROOT/maps_out/tilesets_prismfall.json" ]]; then
  python3 -I "$ROOT/mapgen/export_tilesets_rxdata.py"     # refresh from the registry (needs numpy here only)
  cp "$ROOT/maps_out/Data/Tilesets_prismfall.rxdata" "$ROOT/maps_out/Data/system_prismfall.txt" "$OUT/Data/"
fi

# Graphics the maps need: our tileset sheets, autotiles and fog pictures (new file names only)
for sub in Tilesets Autotiles Fogs; do
  [[ -d "$ROOT/maps_out/Graphics/$sub" ]] || continue
  mkdir -p "$OUT/Graphics/$sub" && cp "$ROOT/maps_out/Graphics/$sub/"*.png "$OUT/Graphics/$sub/"
done

# Docs
cp "$ROOT"/design/*.md "$OUT/Design/" 2>/dev/null || true
cp "$ROOT"/design/*.json "$OUT/Design/" 2>/dev/null || true
cp "$ROOT"/story/*.md  "$OUT/Story/"  2>/dev/null || true
cp "$ROOT"/docs/*.md   "$OUT/Docs/"   2>/dev/null || true
[[ -d "$ROOT/docs/playtest" ]] && cp -r "$ROOT/docs/playtest" "$OUT/Docs/"   # real-engine playtest shots + GIF
mkdir -p "$OUT/Docs/map_previews" && cp "$ROOT"/maps_out/previews/*.png "$OUT/Docs/map_previews/" 2>/dev/null || true
[[ -f "$ROOT/README.md" ]] && cp "$ROOT/README.md" "$OUT/README.md"

# Tools: validators + standalone map tooling (merge tool needs rmarshal.py + rpg.py beside it)
find "$ROOT/tools" -maxdepth 1 -type f ! -name package.sh -exec cp {} "$OUT/Tools/" \;
for f in merge_mapinfos.py rmarshal.py rpg.py build.py; do
  [[ -f "$ROOT/mapgen/$f" ]] && cp "$ROOT/mapgen/$f" "$OUT/Tools/mapgen/"
done
[[ -d "$ROOT/mapgen/specs" ]] && cp -r "$ROOT/mapgen/specs" "$OUT/Tools/mapgen/"

find "$OUT" \( -name '.DS_Store' -o -name '*.pyc' \) -delete
(cd "$ROOT/dist" && zip -qr Prismfall_DevKit.zip Prismfall_DevKit)
echo "Built $ROOT/dist/Prismfall_DevKit.zip"
(cd "$ROOT/dist" && unzip -l Prismfall_DevKit.zip | tail -1)
