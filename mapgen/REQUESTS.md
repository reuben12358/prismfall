# mapgen/REQUESTS.md — tooling requests to the owner of shared mapgen code and palettes

## From builder 3 (routes / forest / Cocoonfall / Gym 1), 2026-11-16
Nothing here blocks me; each item has a workaround in place that touches no shared file.

1. **Tileset IDs 40 and 41 are claimed** (please do not register other sheets there).
   - 40 "Prismfall Wilds" = Tectonic Outside with ids unchanged (so every `tectonic`/`city` painter, learned table and
     stamp still works), then Rejuvenation `Route 2_new` and `Goldenleaf Forrest`, a Bleed recolour of the Tectonic part,
     and a custom strip (silk, giant trees). Built by my own `mapgen/compose_wilds.py`; palette `palettes/wilds.yaml`.
   - 41 "Prismfall Loomhouse" (Gym 1 and the two small interiors); `compose_wilds.py` as well; palette `palettes/loom.yaml`.
   - I did not touch `compose_tileset.py` or tileset 33. If you would rather have one composite, fold these parts into 33
     and I will remap by offset (`data/compose_wilds_offsets.json`).
2. **Art Director's "Forest & nature" sheet** (art/tilesets/, Ekat fairy/haunted woods): when it lands, please append it to
   the composite, or tell me and I append it to tileset 40 the same way.
3. **Fog in build.py.** Rubric 10 asks for fog pictures; build.py has `tone:` but no `fog:`. Request: spec key
   `fog: {name, opacity, blend, zoom, sx, sy}` emitted next to MAP_TONES. Workaround now: a parallel event on each map
   runs RMXP command 204 (change fog) once.
4. **Stamps.** `Ctx` loads only stamps.json / stamps_t.json / stamps_w.json. Request: also load `data/stamps_*.json`.
   Workaround now: my layout kit expands its own stamps into `tiles:` entries.
5. **Preview.** `render.py` does not show tone or fog, so mood cannot be judged from previews. Request: `--mood` flag.
