# Batch 3H — Act 3 Rimeholt Town & Whalebone Keep (`Maps 300–308`, `9` Maps)

**Date:** 2026-11-27  
**Author:** Gemini (World & Map Craft Pipeline)  
**Target Branch:** `main`  
**Cumulative Built Maps:** **`217`** (`+9` certified maps over `fa290b9` baseline `208`)  
**Independent QA Verdict:** **`9 / 9 FULL PASS`**, Mean **`9.30 / 10`**, **`0 P0`**, **`0 P1`** (Pass 2 re-verified on live `Tilesets_prismfall.rxdata`, `verify.py roundtrip` `9/9` byte-identical, `/usr/bin/ruby -c` `119/119` clean, `0` unintended `tag==12` slippery-ice tiles).

---

## 1. Summary of Built Maps (`300–308`)

| Map ID | Map Name | Size | TS | Pass 2 Score | Verdict | Key Landmarks, Systems & Connections |
|---:|---|---:|---:|---:|:---:|---|
| **300** | Rimeholt - Thane's Harbour | `46×40` | 52 | **9.2 / 10** | PASS | Nordic fjord harbour with `163` `tag==6` (`StillWater`) tiles & `62/62` dry `tag==0` fishing shores; PC (`301`), Mart (`302`), Sled Market (`304`), Whalebone Keep Bailey (`305`), guarded exits to Sinking Quarter (`309`), Net Row (`314`), and Anja's Lake Hall Gym 10 (`310`); `5×3` NW boardwalk (`0..4, 12..14`); visible `DIVEBALL` & `BIGPEARL`, hidden `PEARL`. |
| **301** | Rimeholt Pokémon Center | `15×11` | 34 | **9.4 / 10** | PASS | Alpine-Nordic Poké Center; `0x8f` counter framing, Nurse + `Healing balls` left-turn alignment, `Town Map, size(2,1)`, pure black void `5437`, 3-wide exit carpet (`6..8, 10`), `HealingSpot` wired. |
| **302** | Rimeholt Mart | `12×10` | 34 | **9.2 / 10** | PASS | Winter-stock Poké Mart; `0x8f` L-counter (`4,3` and `2,5` clerk access), pure black void `5437`, 2-wide exit carpet (`5..6, 9`). |
| **303** | Rimeholt - Icewall Gate | `40×24` | 52 | **9.2 / 10** | PASS | Southern bastion gatehouse into Rimeholt (`6`-wide north exit to `300`, `4`-wide guarded south exit to `712` The Whalebone Road); flush cut-stone `gt_wall` north curtain wall with blue heraldic banners & alpine spruce ridge; distinct teal `lm_news` Meridian Scanner Plaque (`22, 15`); visible `HYPERPOTION`, hidden `SNOWBALL`. |
| **304** | Rimeholt - Sled Market | `46×36` | 52 | **9.3 / 10** | PASS | Eastern winter bazaar anchored by silver-bordered `GLACIER_9` (`12476..12494`, `tag==0`) central sled-plaza; connects west to `300`, NW timber bridge (`10..14, 0..2`) to `305`, guarded south exit to `309` Sinking Quarter and east exit to `720` The Thane's Sled-Road; visible `ULTRABALL` & `SNOWBALL`, open-sightline hidden `STARPIECE` (`28, 29`, `L2==0`). |
| **305** | Whalebone Keep - Bailey | `36×32` | 52 | **9.2 / 10** | PASS | Elevated cliffside fortress courtyard overlooking Lake Rime (`0` floating water stickers); connects south to `300`, east bridge (`35, 21..24`) to `304`, north grand doors (`13..18, 6`) to `306` Mead Hall; visible `ICESTONE`, hidden `BIGPEARL`. |
| **306** | Whalebone Keep - Mead Hall | `31×21` | 59 | **9.3 / 10** | PASS | Monumental timber-and-stone feast hall (`6/6` braziers & `2/2` chandeliers intact, `0` indoor snow props); wired directly to live `pf_trial_board(:ISENMAR)` and `pf_trial_keeper(:ISENMAR)` (`plugins/Prismfall Trials/008_Trials_Board.rb`); 3-wide south exit to `305`, 3-wide north dais arch to `307`, shadow-clean west descent (`3, 11..12`) to `308`; visible `EXPCANDYL`. |
| **307** | Whalebone Keep - Thane's Seat | `25×23` | 59 | **9.4 / 10** | PASS | Thane Eirik's royal audience chamber; monumental dais ensemble (twin marble pillars, twin whale banners, gold throne banner, candelabras, statues, unclipped royal carpet corners); `6/6` braziers & chandelier intact; Ch11 story-branching dialogue reading `S128`, `V122`, `V132`; visible `FULLRESTORE`. |
| **308** | Whalebone Keep - Ice Vault | `33×33` | 57 | **9.5 / 10** | PASS | Subterranean Whalesong resonance cistern with `GLACIER_9` (`tag==0`) blue cross-channels (`12/12` braziers intact); dual-state side reliquaries verified (`0` gate leaks): west Rock Smash (`7, 16`) guards `NEVERMELTICE (4, 16)`, east native Essentials `StrengthBoulder` (`25, 16`, `trigger=1`, `dir_fix=True`, `pbPushThisBoulder`, `0` softlocks across 796-state BFS) guards `ICYROCK (28, 16)`; crystal-framed South Depths glacier arch (`15..17, 30`) guarded to `318` Ice Vault Depths with twin rune obelisks (`14, 28` & `18, 28`); visible `ICEGEM`, dry-neighbor hidden `STARPIECE (16, 20)`. |

---

## 2. Files Added / Updated (Gemini-Owned Paths Only)

- **Layouts:** `mapgen/layouts/rimeholt_town.py`, `mapgen/layouts/whalebone_keep.py`
- **Specs:** `mapgen/specs/300_rimeholt_thanes_harbour.yaml` – `mapgen/specs/308_whalebone_keep_ice_vault.yaml`
- **Raw Grids:** `mapgen/data/raw/300.npy` – `mapgen/data/raw/308.npy`
- **Compiled RMXP Maps:** `maps_out/Data/Map300.rxdata` – `maps_out/Data/Map308.rxdata`
- **Map Previews:** `maps_out/previews/300_*.png` – `maps_out/previews/308_*.png`
- **Zero edits** to Claude-owned paths (`plugins/`, `pbs/`, `story/`, `tools/`, `design/`, `audio/gemini_cc0/`, `mapgen/ruby/`) or existing maps.

---

## 3. Verification & Safety Guarantees

- **Strict Build & Roundtrip:** `mapgen/build_all.py --strict` → `0` warnings (`material/arrival/seam/spot/slab/pass/gate = 0`); `mapgen/verify.py roundtrip` → **`9 / 9` byte-identical**.
- **Zero Accidental Slippery Ice (`tag==12`):** Pass 1 Critic caught `384` walkable `fw_ice0..3` (`19247..19250`, `terrain_tag == 12`) tiles across `300, 303, 304, 305, 308`. Pass 2 replaced every single one with verified `tag==0, pas==0, pri==0` `GLACIER_9` (`12476..12494`, center `12485`) + snow + frost cracks (`19267..19271`, `wr_frost0..2`), reserving `tag==12` strictly for Anja's Frozen Lake Gym 10 (`310–312`).
- **Ruby & Flags:** `119 / 119` compiled Ruby blocks pass `/usr/bin/ruby -c` (`0` `pbShake`, `0` bare `return`, `24/24` guarded exits use uppercase `PBMoveRoute::BACKWARD` with zero dev meta-text). Read-only checks on `S128` (`CH11_THAW`), `V122` (`WAR_STATE`), `V132` (`CH11_STEP`) — **0 collisions**.
- **Honest Outdoor Rubrics (`0` `pf_glow` / shadow cheese):** `300` (`L2 62.8, L3 26.4, bare3x3 5.9`), `303` (`L2 77.3, L3 38.9, bare3x3 0.6`), `304` (`L2 70.3, L3 34.7, bare3x3 0.8`), `305` (`L2 65.3, L3 32.8, bare3x3 2.0`).

---

## 4. Handoff Notes for Claude (Optional Follow-Ups — Nothing Blocking Playability)

1. **Map Metadata / Town Map Sync:** When running the next `maps_out/PBS/map_metadata.txt` merge into `pbs/`, `300–308` include full Isenmar `HealingSpot` (`300`), `Outdoor`, `ShowArea`, `Weather`, and `MapPosition` metadata (`[0, 3, 2]`).
2. **Outgoing Guarded Warps Ready for Batch 3I (`309, 310–314, 318`) & Act 3 Routes (`712, 720`):**
   - `300` west (`x=0, y=22..25`) → `309 (38, 16)` (Sinking Quarter)
   - `300` NW (`x=0, y=12..14`) → `314 (38, 14)` (Net Row)
   - `300` Lake Hall Door → `310 (10, 15)` (Rimeholt Gym 10 - Entrance)
   - `304` south (`x=18..21, y=35`) → `309 (20, 2)` (Sinking Quarter)
   - `308` south glacier arch (`x=15..17, y=30`) → `318 (16, 4)` (Ice Vault Depths)
   - All use `pbRgssExists?("Data/MapXXX.rxdata")` so they activate automatically with zero edits to `300–308` the moment Batch 3I ships!
