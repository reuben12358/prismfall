# Art Drop 13 + Wave 3A/3B Pure-Gemini Battlebacks — Engine Wiring Handoff

- **Date:** 2026-11-22
- **Author:** Gemini (Art Director)
- **Live on `origin/main`:** `9ed3d49`, `fb4380a`, `7ebdcd6`, `070327d`, `a9cfd80`, `3707e8a` (**260 dual-synced PNGs**, 100% SHA-256 byte-identical across `graphics/` and `art/out/Graphics/`)

---

## 1. What Shipped & Passed QA (All Live on `origin/main`)

### A. Art Drop 13 — 6 Complete Pure-Gemini Boss & Cantor Character Packs (192 Dual-Synced PNGs)
Every character pack passes `exact2x=True`, `semi=0`, `orphans=0`, `bottom_y=156` across all 16 PWT frames, flush-bottom `256x136` VS bust facing left, `128x192` 4×4 overworld + `trainer_<TTYPE>.png` mirror, and 12 locked-framing `96x96` portraits (`<ID>.png` == `<ID>_neutral.png` + 11 expressions):
- **`OCTAVE_VESPER` / `VESPER`** (Cantor Vesper Lindqvist — 32 PNGs)
- **`HOLLOW_THISTLE` / `THISTLE`** (Hollow Pallbearer Mara "Thistle" — 32 PNGs)
- **`MERIDIAN_MARCHETTI` / `MARCHETTI`** (Director Helene Marchetti — 32 PNGs)
- **`MERIDIAN_QUENT` / `QUENT`** (Dr. Percival Quent — 32 PNGs)
- **`MERIDIAN_KROLL` / `KROLL`** + **`HOLLOW_SABLE` / `SABLE`** (Sabine Kroll / "Sable" Dual-Identity Double Pack — 64 PNGs sharing the exact same locked face/bob/eyes across her Meridian coat and undercover Hollow cloak!)

*(Prismfall now has **31 complete pure-Gemini cast identities** live on disk!)*

### B. Wave 3A + 3B Pure-Gemini Battlebacks (17 / 19 Tier-1 Arenas = 68 Dual-Synced PNGs)
All 17 arenas shipped in BOTH `field_<key>.png` (`384x308`) and `field_<key>_hd.png` (`864x693`), EBDX anchor-locked (`FOE=(526.5,342)` / `PLAYER=(261,567)`), bringing Prismfall to **40 / 54 pure-Gemini HD battleback variants (26 / 36 fields)**:
- **Wave 3A (`7ebdcd6`):** Shared-geometry `GRAND_STAGE` (`1`, `2`, `3`), `SILKWOOD`, `BEACH`, pixel-locked `NEON_GRID` + `NEON_GRID_BLACKOUT`, and `NEW_MOON` Stage 1 *(Stages 2–3 `_lamplight` & `_abyss` queued for next image-quota reset)*.
- **Wave 3B (`9ed3d49`):** Shared-horizon Ossaria Ch19 War 5-pack (`DESERT`, `DESERT_BLOOM`, `FLOODED_DUNES`, bottle-green trinitite `GLASS_DUNES`, `GLASS_DUNES_MIRROR`), shared-layout Ashkaar pair (`VOLCANIC` + Rev 10 Cinderglass `ASHEN_WASTE`), `INVERSE`, and dark-storybook `FAIRY_TALE`.

*(Battlebacks are already live in `graphics/EBDX/Battlebacks/battlebg/` — zero code changes required!)*

---

## 2. Exact Engine Wiring Changes Needed (2 Small Ruby Edits)

### A. `plugins/Prismfall EBDX Bridge/010_Bridge_VersusIntro.rb`
1. **Un-spoil Sable & map PBS first-names in `VS_IDS` (`L28–42`):**
   - Change line `36` from `:HOLLOW_SABLE => "KROLL"` to **`:HOLLOW_SABLE => "SABLE"`** now that her dedicated undercover Hollow cloak bust (`EBDX/VS/SABLE.png`) is live (prevents spoiling Sabine Kroll's Meridian suit before Ch13!).
   - Add the remaining 5 Drop 13 mappings (critical for `MARCHETTI` [`"Helene"`], `QUENT` [`"Percival"`], and `KROLL` [`"Sabine"`], whose PBS trainer names are first names):
```ruby
    :HOLLOW_SABLE       => "SABLE",      # dedicated undercover Hollow cloak bust (replaces KROLL alias)
    :MERIDIAN_KROLL     => "KROLL",      # PBS name "Sabine"
    :MERIDIAN_MARCHETTI => "MARCHETTI",  # PBS name "Helene"
    :MERIDIAN_QUENT     => "QUENT",      # PBS name "Percival"
    :HOLLOW_THISTLE     => "THISTLE",
    :OCTAVE_VESPER      => "VESPER",
```
2. **Add `THEMES` entries (`L43–53`):** (`"KROLL" => :red` and `"MARCHETTI" => :red` are already present; optionally `"MARCHETTI" => :grey` also fits her Meridian Directorate uniform cleanly):
```ruby
    # Art Drop 13 (Bosses & Cantor Vesper)
    "VESPER" => :gold, "THISTLE" => :green, "QUENT" => :teal, "SABLE" => :teal
```

### B. `plugins/Prismfall Core/025_CharsetAliases.rb`
Add Drop 13 event names to `NAME_ALIASES` (`L20–27`, audited against `mapgen/layouts/` & `mapgen/specs/`):
```ruby
    "Vesper" => "VESPER", "Thistle" => "THISTLE",
    "Marchetti" => "MARCHETTI", "Helene" => "MARCHETTI",
    "Quent" => "QUENT", "Percival" => "QUENT",
    "Kroll" => "KROLL", "Sabine" => "KROLL", "Sable" => "SABLE"
```

### C. Already Auto-Wired (Zero Changes Needed)
- `plugins/Prismfall Cutscenes/014_Portraits.rb` already lists `VESPER`, `THISTLE`, `SABLE`, `KROLL`, `QUENT`, and `MARCHETTI` in `CAST`.
- `plugins/Prismfall Cutscenes/004_Actors.rb` resolves `Graphics/Trainers/<TTYPE>.png` and `Graphics/Characters/trainer_<TTYPE>.png` directly.
