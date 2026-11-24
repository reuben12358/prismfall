# Pokémon Prismfall — Proposal Bundle: Gen 6–9 Animated B2W2 Sprites, Reborn-Style Postgame Legendaries & Gym 1 Dorian (Meloetta Ace)

**Date:** 2026-11-23  
**Author:** Antigravity Architect (Read-Only Audit & Claude-Ready Blueprint)  
**Target Repo:** `/home/antigravity/reuben12358/prismfall`  
**Engine Snapshot Audited:** `/home/antigravity/pf_engine_run/base` (Pokémon Essentials v21.1 + Unofficial EBDX 1.4.7 + Gen 9 Resource Pack)  
**Status:** Proposal only — zero source files edited; ready for parent review and Claude execution.

---

## Executive Summary

| Mandate | Verified Current State | Headline Action for Claude |
|---|---|---|
| **Part A — Gen 6–9, Regional & Mega Animated B2W2 Sprites** | Gen 1–5 (`#001–#649`) are **100% animated** (649/649 F/B/Shiny). Gen 6 is partial (**55/72 Front, 39/72 Back, 12/72 Shiny**). Gen 7–9 (**0/304**), Regional forms (**0/58** including **Hisuian Zorua `570_1`**), Primals (**0/2**), and half of Megas (**24/48 Front, 14/48 Back**) fall back to static PNGs. Across Prismfall's **795** live PBS species/forms (+23 combat Megas), the live gap is **247 Front / 263 Back** (**248 / 264** once Dorian gets Hisuian Zorua). Also caught **4 engine/asset bugs** (broken `FrontShiny`/`BackShiny` fallback path, 29 uppercase `.PNG` filenames, 141/180 oversized `192–288px` Gen 9 static PNGs, zeroed Gen 7–9 `BattlerAltitude`). | Build repeatable `tools/install_ebdx_animated_sprites.py` pulling strictly 2D Gen 5 B2W2-style horizontal strips from **Open-Source EBDX Renovation Project 4.0** / **Lucidious89 Animated Pokémon System `[SPRITES]`** + **`Ghasty001/Animated_sprites_by_Ghasty001`** + **La Base de Sky** + **Pokémon Showdown `gen5ani`** (GIF→PNG strip converter), fix `Battler Bitmaps.rb` shiny fallback path, lowercase `.PNG` extensions, and normalize strip height. |
| **Part B — Ban Story Legendary Captures → Reborn-Style Postgame Network** | All 8 currently registered story boss files (`101`–`108_Boss_*.rb`) and Festival Arceus (`008_Festival_Data.rb`) already set `:catch => false`, and wild Paradox spawns (`pbs/encounters.txt:2848–2861`) live only on postgame Map `905`. **However, 3 active main-story leaks + 3 unregistered bosses exist:** (1) Ch10 **Type: Null Lv 45/50 gift** (`S180`, Map `699`), (2) Act IV **Kubfu Lv 60 gift** (Ironreach Dojo), (3) Act IV **Regirock Lv 64** (Stonesleep `788`), plus unregistered `:LOYAL_THREE`, `:PECHARUNT_DEEP`, and Ogerpon's Act V/Festival boundary. | Enforce hard story-lock (`!Prismfall::Endings.postgame? && !$game_switches[160]`) inside `004_Bosses_Battle.rb` + move Type: Null, Kubfu, Regirock, and all Legendary/Mythical/UB/Paradox captures into a **3-Tier Reborn-Style Postgame Network** (`S160 POSTGAME`, switches `S270–S295`), opening with **Dorian's Crownhaven Encore (Meloetta)**, **Gloamwood Masks (Loyal Three → Ogerpon)**, and culminating in **18-Plate Convergence (Arceus)**. |
| **Part C — Gym 1 Dorian Pell (`LEADER_DORIAN`) Meloetta Ace Redesign** | Currently 5/6/3 mons (`Aipom, Minccino, Spinda, Jigglypuff, +Hard Whismur, Kecleon` ace). Damage-calc proof shows **stock `:GRAND_STAGE` double-stacks Normal × Sound (`×1.69 / ×2.10 / ×2.25`)**, turning Lv 15 Meloetta's 75 BP `RELICSONG` off 128 SpA into a **253-BP nuke that OHKOs 14/19 Badge-0 Pokémon** (even Bulbasaur/Squirtle/Kricketune). Also verified **Meloetta cannot learn `DISARMINGVOICE`** in v21.1 `PBS/pokemon.txt`, and `validate_trainers.py` flags Sketched moves on `SMEARGLE` unless allowlisted. | Upgrade Dorian to a strictly Normal-type 6-mon Theater Troupe (`Smeargle, Spinda, Jigglypuff, Chatot, Hisuian Zorua [Form=1], Meloetta [Lv 15 Ace]`; Casual 4-mon). Add 1-line `:not_moves => [:RELICSONG]` on `:GRAND_STAGE`'s Sound damage stack + 1-bar `"Matinee Rehearsal"` `register_trainer_boss` (`0.80×` Std / `0.85×` Hard / `0.78×` Cas, zero boss pips, full status vulnerability) so Lv 15 Meloetta sings `RELICSONG`, swaps **Aria ↔ Pirouette**, and stays **cleanly beatable** vs Badge-0 counters! |

---

# PART A — Gen 6–9, Regional Variants & Mega Evolutions Animated B2W2 Battle Sprites Audit & Sourcing Plan

## A.1 Exact Quantitative Audit of `/home/antigravity/pf_engine_run/base/`

Audited against `/home/antigravity/pf_engine_run/base/PBS/pokemon.txt` (**1,025 base species**, `#001 BULBASAUR` through `#1025 PECHARUNT`, including lowercase-letter IDs `NIDORANfE` and `NIDORANmA`) and `PBS/pokemon_forms.txt` (**395 alternate forms**).

### Directory Totals (PNG Dimension Scan: Animated = Horizontal Multi-Frame Strip `W > H`, `W % H == 0`)

| Directory | Flat Files | Animated Strips | Static PNGs | `Female/` Subdir (Anim / Stat) | `Gigantamax/` Subdir (Anim / Stat) | Total PNGs |
|---|---:|---:|---:|---:|---:|---:|
| `Graphics/EBDX/Battlers/Front/` | 821 | 818 | 3 (`172_1`, `483_1`, `999`) | 190 (97 / 93) | 35 (0 / 35) | **1,046** |
| `Graphics/EBDX/Battlers/Back/` | 791 | 789 | 2 | 185 (97 / 88) | 35 (0 / 35) | **1,011** |
| `Graphics/EBDX/Battlers/FrontShiny/` | 755 | 752 | 3 | 189 (96 / 93) | 35 (0 / 35) | **979** |
| `Graphics/EBDX/Battlers/BackShiny/` | 752 | 749 | 3 | 184 (96 / 88) | 35 (0 / 35) | **971** |
| `Graphics/Pokemon/Front/` | 1,541 | **0** | 1,541 | — (flat `_female`) | — | **1,541** |
| `Graphics/Pokemon/Back/` | 1,536 | **0** | 1,536 | — | — | **1,536** |
| `Graphics/Pokemon/Front shiny/` | 1,536 | **0** | 1,536 | — | — | **1,536** |
| `Graphics/Pokemon/Back shiny/` | 1,534 | **0** | 1,534 | — | — | **1,534** |

### Base Species Coverage by Generation (Form `0`, All 1,025 Species)

| Generation (National Dex) | Total | EBDX Front Anim | EBDX Back Anim | EBDX FrontShiny Anim | EBDX BackShiny Anim | Static Fallback (`Graphics/Pokemon/`) |
|---|---:|---:|---:|---:|---:|---:|
| **Gen 1 (`#001–#151`)** | 151 | **151 (100%)** | **151 (100%)** | **151 (100%)** | **151 (100%)** | 0 |
| **Gen 2 (`#152–#251`)** | 100 | **100 (100%)** | **100 (100%)** | **100 (100%)** | **100 (100%)** | 0 |
| **Gen 3 (`#252–#386`)** | 135 | **135 (100%)** | **135 (100%)** | **135 (100%)** | **135 (100%)** | 0 |
| **Gen 4 (`#387–#493`)** | 107 | **107 (100%)** | **107 (100%)** | **107 (100%)** | **107 (100%)** | 0 |
| **Gen 5 (`#494–#649`)** | 156 | **156 (100%)** | **156 (100%)** | **156 (100%)** | **156 (100%)** | 0 |
| **Gen 6 (`#650–#721`)** | 72 | **55 (76.4%)** | **39 (54.2%)** | **12 (16.7%)** | **9 (12.5%)** | 17 Front / 33 Back |
| **Gen 7 (`#722–#809`)** | 88 | **0 (0%)** | **0 (0%)** | **0 (0%)** | **0 (0%)** | 88 |
| **Gen 8 (`#810–#905`)** | 96 | **0 (0%)** | **0 (0%)** | **0 (0%)** | **0 (0%)** | 96 |
| **Gen 9 (`#906–#1025`)** | 120 | **0 (0%)** | **0 (0%)** | **0 (0%)** | **0 (0%)** | 119 (+`999.png` static 96×96) |
| **TOTAL Base Species** | **1,025** | **704 (68.7%)** | **688 (67.1%)** | **661 (64.5%)** | **658 (64.2%)** | **321 Front / 337 Back** |

- **Exact 17 Gen 6 species missing Front animation:** `#685 SLURPUFF`, `#686 INKAY`, `#689 BARBARACLE`, `#691 DRAGALGE`, `#693 CLAWITZER`, `#694 HELIOPTILE`, `#695 HELIOLISK`, `#698 AMAURA`, `#699 AURORUS`, `#701 HAWLUCHA`, `#705 SLIGGOO`, `#706 GOODRA`, `#712 BERGMITE`, `#713 AVALUGG`, `#714 NOIBAT`, `#719 DIANCIE`, `#721 VOLCANION`.
- **Exact 16 additional Gen 6 species with Front animation but missing Back animation (33 total missing Back):** `#676 FURFROU`, `#678 MEOWSTIC`, `#683 AROMATISSE`, `#690 SKRELP`, `#692 CLAUNCHER`, `#696 TYRUNT`, `#702 DEDENNE`, `#703 CARBINK`, `#708 PHANTUMP`, `#710 PUMPKABOO`, `#711 GOURGEIST`, `#715 NOIVERN`, `#716 XERNEAS`, `#717 YVELTAL`, `#718 ZYGARDE` (50%), `#720 HOOPA`.

### Alternate Forms, Regional Variants & Mega Evolutions (`PBS/pokemon_forms.txt`, 395 Entries)

| Form Category | Total in PBS | Front Anim | Back Anim | FrontShiny Anim | BackShiny Anim | Notes |
|---|---:|---:|---:|---:|---:|---|
| **Mega Evolutions** | 48 | **24** | **14** | **4** | **4** | Only `ABSOL_1`, `GARDEVOIR_1`, `LUCARIO_1`, `MEWTWO_1` have Shiny anims. **24 missing Front entirely** (`AERODACTYL_1`, `ALTARIA_1`, `AUDINO_1`, `BLAZIKEN_1`, `CAMERUPT_1`, `DIANCIE_1`, `GALLADE_1`, `HOUNDOOM_1`, `LATIAS_1`, `LATIOS_1`, `LOPUNNY_1`, `MANECTRIC_1`, `MEDICHAM_1`, `METAGROSS_1`, `MEWTWO_2`, `PINSIR_1`, `RAYQUAZA_1`, `SALAMENCE_1`, `SCEPTILE_1`, `SHARPEDO_1`, `SLOWBRO_2`, `STEELIX_1`, `SWAMPERT_1`, `TYRANITAR_1`). **10 more have Front but no Back** (`AGGRON_1`, `BANETTE_1`, `BEEDRILL_1`, `BLASTOISE_1`, `CHARIZARD_2`, `GENGAR_1`, `GYARADOS_1`, `HERACROSS_1`, `KANGASKHAN_1`, `SABLEYE_1`). |
| **Primal Reversions** | 2 | **0** | **0** | **0** | **0** | Both `KYOGRE_1` and `GROUDON_1` are static! (Critical for Ch11/Ch14/Postgame bosses.) |
| **Alolan Forms** | 18 | **0** | **0** | **0** | **0** | 100% static fallback. |
| **Galarian Forms** | 20 | **0** | **0** | **0** | **0** | 100% static fallback. |
| **Hisuian Forms** | 16 | **0** | **0** | **0** | **0** | 100% static fallback + **uppercase `.PNG` hazard** (see §A.3)! |
| **Paldean Forms** | 4 | **0** | **0** | **0** | **0** | 100% static fallback. |
| **Other Forms** | 287 | **90** | **87** | **87** | **87** | Gen 1–5 forms (Unown, Castform, Deoxys, Rotom, Giratina Origin, Shaymin Sky, Deerling/Sawsbuck, Kyurem, Meloetta Pirouette, Genesect) are animated; Gen 6–9 forms (Vivillon/Florges patterns, Oricorio, Silvally memories, Ogerpon masks, Terapagos) are mostly static. |

### Spotlight Check — Creator-Mentioned & Prismfall Key Species

| Species / Form | Dex `#` | EBDX Front | EBDX Back | EBDX Shiny | `Graphics/Pokemon/` Static Fallback | Verdict |
|---|---:|---|---|---|---|---|
| **Meloetta Aria (`MELOETTA,0`)** | `#648` | `648.png` (`9450×63`, **150f ANIM**) | `648.png` (`8642×58`, **149f ANIM**) | **ANIM** | `96×96` / `96×96` | **READY NOW** |
| **Meloetta Pirouette (`MELOETTA,1`)** | `#648` | `648_1.png` (`5776×76`, **76f ANIM**) | `648_1.png` (`5700×75`, **76f ANIM**) | **ANIM** | `96×96` / `96×96` | **READY NOW** |
| **Dorian's Core Gen 1–5 Troupe** (`SMEARGLE`, `SPINDA`, `JIGGLYPUFF`, `CHATOT`) | `#235,#327,#039,#441` | **ALL 4 ANIM** (48–80f) | **ALL 4 ANIM** (47–80f) | **ALL 4 ANIM** | `96×96` | **READY NOW** |
| **Hisuian Zorua (`ZORUA,1`)** | `#570` | **MISSING** | **MISSING** | **MISSING** | `ZORUA_1.PNG` (**UPPERCASE `.PNG`!** `96×96`) | **PRIORITY 1 GAP** (Gym 1!) |
| **Hisuian Zoroark (`ZOROARK,1`)** | `#571` | **MISSING** | **MISSING** | **MISSING** | `ZOROARK_1.PNG` (uppercase `.PNG`) | GAP |
| **Ogerpon (`OGERPON,0..3`)** | `#1017` | **MISSING** | **MISSING** | **MISSING** | **`192×192` Front / `288×288` Back** (2×/3× giant!) | **PRIORITY 1 GAP** (Ch10/Act V/PG) |
| **Loyal Three (`OKIDOGI`, `MUNKIDORI`, `FEZANDIPITI`)** | `#1014–1016` | **MISSING** | **MISSING** | **MISSING** | **`192×192` Front / `288×288` Back** | **PRIORITY 1 GAP** (Ch10/PG) |
| **Pecharunt (`PECHARUNT,0`)** | `#1025` | **MISSING** | **MISSING** | **MISSING** | **`192×192` Front / `288×288` Back** | **PRIORITY 1 GAP** (Ch18/PG) |
| **Gholdengo (`GHOLDENGO,0`)** | `#1000` | **MISSING** | **MISSING** | **MISSING** | `96×96` / `96×96` | GAP (in Ghasty001 + Showdown `gen5ani`!) |
| **Annihilape (`ANNIHILAPE,0`)** | `#979` | **MISSING** | **MISSING** | **MISSING** | `96×96` / `96×96` | GAP (in Ghasty001!) |
| **Mega Lucario (`LUCARIO,1`)** | `#448` | `448_1.png` (`6912×96`, **72f ANIM**) | `448_1.png` (**72f ANIM**) | **ANIM** | `96×96` | READY NOW |
| **Mega Gardevoir (`GARDEVOIR,1`)** | `#282` | `282_1.png` (`2976×96`, **31f ANIM**) | `282_1.png` (**31f ANIM**) | **ANIM** | `96×96` | READY NOW |
| **Mega Gallade / Metagross / Salamence / Camerupt / Aerodactyl / Slowbro / Lopunny** | various | **ALL MISSING** | **ALL MISSING** | **MISSING** | `96×96` | **PRIORITY 1 GAP** (Warden/Champion Aces!) |
| **Primal Kyogre (`KYOGRE,1`) / Primal Groudon (`GROUDON,1`)** | `#382,#383` | **MISSING** | **MISSING** | **MISSING** | `96×96` | **PRIORITY 1 GAP** (Ch11/Ch14/PG!) |
| **Giratina Origin (`GIRATINA,1`)** | `#487` | `487_1.png` (`1183×91`, **13f ANIM**) | `487_1.png` (**13f ANIM**) | **ANIM** | `96×96` | READY NOW |
| **Zygarde Complete (`ZYGARDE,2`)** | `#718` | `718_2.png` (`960×96`, **10f ANIM**) | `718_2.png` (**10f ANIM**) | MISSING | `96×96` | Front/Back ready; Shiny gap |

---

## A.2 Cross-Reference Against Prismfall's Live PBS Roster

Auditing every `(species, form)` actually referenced in `pbs/trainers.txt`, `pbs/trainers_trials.txt`, `pbs/encounters.txt`, `pbs/encounters_badgetiers.txt`, plus all **23** combat Mega Evolutions triggered by trainer Mega Stones (excluding `EVIOLITE`):

| Live Roster Slice | Unique `(Species, Form)` | Front Animated | **Front GAP** | Back Animated | **Back GAP** | Shiny Anim (F / B) |
|---|---:|---:|---:|---:|---:|---:|
| `pbs/trainers.txt` + `trainers_trials.txt` | 365 | 282 | **83** | 276 | **89** | 262 / 260 |
| Trainer Combat Mega Evolutions | 23 | 12 | **11** | 8 | **15** | 3 / 3 |
| `pbs/encounters.txt` + `encounters_badgetiers.txt` | 713 | 491 | **222** | 480 | **233** | 464 / 462 |
| **Combined Live Prismfall Roster** | **795** | **548 (68.9%)** | **247** | **532 (66.9%)** | **263** | **510 / 508** |
| *+ New Dorian `ZORUA,1` (Part C)* | **796** | **548** | **248** | **532** | **264** | **510 / 508** |

**Exact breakdown of the 247 current live Front-animation gaps (+1 Hisuian Zorua = 248):**
- **Gen 9 Base:** `83`
- **Gen 8 Base:** `66`
- **Gen 7 Base:** `50`
- **Gen 6 Base:** `14` (`AURORUS`, `AVALUGG`, `BARBARACLE`, `BERGMITE`, `CLAWITZER`, `DRAGALGE`, `GOODRA`, `HAWLUCHA`, `HELIOLISK`, `HELIOPTILE`, `INKAY`, `NOIBAT`, `SLIGGOO`, `SLURPUFF`) — plus `12` more Gen 6 live species missing Back animation (`26` Back gaps total)!
- **Trainer Mega Forms:** `11` Front (`AERODACTYL_1`, `CAMERUPT_1`, `GALLADE_1`, `HOUNDOOM_1`, `LATIAS_1`, `LOPUNNY_1`, `MANECTRIC_1`, `METAGROSS_1`, `SALAMENCE_1`, `SHARPEDO_1`, `SLOWBRO_2`) + `4` Back-only (`BANETTE_1`, `GENGAR_1`, `GYARADOS_1`, `SABLEYE_1`) = `15` Back gaps.
- **Alolan Forms:** `10` (`DIGLETT_1`, `EXEGGUTOR_1`, `GOLEM_1`, `GRIMER_1`, `MAROWAK_1`, `MUK_1`, `NINETALES_1`, `SANDSHREW_1`, `SANDSLASH_1`, `VULPIX_1`).
- **Galarian Forms:** `9` (`CORSOLA_1`, `DARUMAKA_2`, `FARFETCHD_1`, `LINOONE_1`, `MEOWTH_2`, `MRMIME_1`, `SLOWPOKE_1`, `STUNFISK_1`, `WEEZING_1`).
- **Hisuian Forms:** `0` currently in PBS → **`+1` (`ZORUA_1`)** immediately with Part C! (Plus evolutions like `URSALUNA`, `KLEAVOR`, `SNEASLER`, `OVERQWIL`, `WYRDEER`, `BASCULEGION`.)
- **Other Alt Forms:** `4` (`FLOETTE_4`, `FLORGES_4`, `ORICORIO_1`, `SILVALLY_8`).

---

## A.3 How Prismfall's EBDX Resolves Animated Sprites (+ 4 Real Bugs Discovered)

Verified directly in `/home/antigravity/pf_engine_run/base/Plugins/Elite Battle DX/`:

1. **Resolution Order (`[000] Scripts/Battle Core/Battler Bitmaps.rb:172–335`, `Config.rb:73–75`):**
   - `PRIORITIZE_ANIMATED_SPRITES = true` and `PRIORITIZE_REGULAR_SPRITES = true`.
   - `EliteBattle.GetSpeciesIndex(species)` (`EBDX Module.rb:52,74–95`) indexes `@full_species = [:NONE] + all GameData::Species` → 1-based National Dex index (`BULBASAUR = 1`, `ZORUA = 570`, `MELOETTA = 648`, `PECHARUNT = 1025`).
   - `EliteBattle.GetSpeciesID(species)` returns the internal Symbol (`:ZORUA`, `:OGERPON`, etc.).
   - For each `(species, form, back, shiny, female, shadow)`:
     1. Probes `Graphics/EBDX/Battlers/<subdir>[/Female]/%03d[_form][_shadow].png` (e.g. `570_1.png`, `648_1.png`, `1017_1.png` — note `%03d` prints 4 digits cleanly for `>= 1000`, e.g. `1017.png`).
     2. Probes `Graphics/EBDX/Battlers/<subdir>[/Female]/%s[_form][_shadow].png` (e.g. `ZORUA_1.png`, `OGERPON_1.png`).
     3. Falls back to `Graphics/Pokemon/<subdir>/...` (static PNGs).
   - **Recommended Canonical Naming for New Animated Strips:** **Internal Symbol (`ZORUA_1.png`, `OGERPON.png`, `METAGROSS_1.png`)** OR **Zero-Padded Dex Number (`570_1.png`, `1017.png`, `376_1.png`)**. Using **symbolic names** (`SPECIES.png` / `SPECIES_form.png`) matches Essentials v21.1 + Renovation 4.0 + Lucidious89 APS natively, avoids any Dex-index drift if species order ever changes, and is checked immediately after numeric lookup (zero collision with existing Gen 1–5 `001..649.png` files; and for Gen 6/Mega upgrades we overwrite/replace the numeric file OR remove stale static numeric files like `999.png`!).
2. **Frame-Strip Format (`[000] Scripts/Battle Core/EBDX Wrapper.rb:5–158`):**
   - `BitmapEBDX` **explicitly rejects `.gif`** (`line 16`: `"BitmapEBDX does not support GIF files."`).
   - Expects a **horizontal PNG strip** of `N` square frames of size `H × H`, so total dimensions are **`(N * H) × H`**.
   - At load time (`lines 135–144`), EBDX slices `ceil(width / height)` square frames of `H × H` and scales each by `FRONT_SPRITE_SCALE = 2` / `BACK_SPRITE_SCALE = 2` (`Config.rb:16–19`), unless overridden in `PBS/EBDX/pokemon.txt` via `SpriteScaleEnemy` / `SpriteScalePlayer`.
   - Native Gen 1–5 B2W2 strips have frame height `H = 48–104 px` (rendered at `96–208 px` after `×2`).
3. **Auto-Grounding Placement (`plugins/Prismfall EBDX Bridge/007_Bridge_Placement.rb:16–154`):**
   - **Great news:** Prismfall's own `PrismfallEBDX.grounded_oy` automatically scans the lowest opaque pixel row across up to 12 sampled frames of every loaded bitmap and plants the sprite's feet cleanly on the battle base — **no manual `BattlerEnemyY`/`BattlerPlayerY` hand-positioning needed for grounded species!**
   - `PBS/EBDX/pokemon.txt` already contains all **1,430 sections** through `PECHARUNT`, **but** Gen 7–9 & Regional entries all have `BattlerAltitude = 0`. Floating/hovering Gen 7–9 species without `:LEVITATE` (e.g., `PECHARUNT`, `FLUTTERMANE`, `IRONMOTH`, `IRONJUGULIS`, `GHOLDENGO`, `NOIBAT`, `DRAGAPULT`, `MINIOR`, `TAPUKOKO..FINI`, `COSMOG`, `SOLGALEO`, `LUNALA`, `NECROZMA`, `NIHILEGO`, `XURKITREE`, `CELESTEELA`, `KARTANA`, `MIRAIDON`, `CHIYU`) need `BattlerAltitude = 10` in `PBS/EBDX/pokemon.txt` (or an entry in `PrismfallEBDX::FLOATING`) so they hover over their shadows properly.

### 4 Real Engine/Asset Bugs Caught During This Audit

1. **BUG 1 — Broken Shiny Static Fallback Path (`Battler Bitmaps.rb:199–207` & `341–350`):**
   - EBDX computes `subdir = "FrontShiny"` / `"BackShiny"` and sets `folder2 = "Graphics/Pokemon/" + subdir`.
   - Essentials v21.1's actual folders are **`Graphics/Pokemon/Front shiny`** and **`Graphics/Pokemon/Back shiny`** (lowercase `s` with a space)!
   - **Impact:** Any shiny Gen 6–9, Regional, or Mega Pokémon missing from `Graphics/EBDX/Battlers/{FrontShiny,BackShiny}` fails the `folder2` lookup completely and degrades to non-shiny or `000.png`!
   - **2-Line Fix:** Map `subdir2 = (tshiny && back) ? "Back shiny" : tshiny ? "Front shiny" : back ? "Back" : "Front"` for `folder2 = "Graphics/Pokemon/" + subdir2`.
2. **BUG 2 — 29 Uppercase `.PNG` Files in `Graphics/Pokemon/{Front,Back}/`:**
   - All 29 Hisuian/PLA static sprites (`ZORUA_1.PNG`, `ZOROARK_1.PNG`, `ARCANINE_1.PNG`, `TYPHLOSION_1.PNG`, `SAMUROTT_1.PNG`, `DECIDUEYE_1.PNG`, `KLEAVOR.PNG`, `URSALUNA.PNG`, `SNEASLER.PNG`, `OVERQWIL.PNG`, `BASCULEGION.PNG`, `ENAMORUS.PNG`, `DIALGA_1.PNG`, `PALKIA_1.PNG`, `PAWMOT.PNG`, etc.) have uppercase `.PNG` extensions.
   - **Impact:** Case-sensitive Linux/mkxp-z builds can fail `pbResolveBitmap` if only `.png` is probed! Normalize all `.PNG` → `.png` across `Graphics/Pokemon/` and `Graphics/EBDX/`.
3. **BUG 3 — 141 Oversized Front (`160–192px`) & 180 Oversized Back (`160–288px`) Static Gen 9 DLC Sprites:**
   - Kitakami/Indigo Disk sprites (`OGERPON`, `OKIDOGI`, `MUNKIDORI`, `FEZANDIPITI`, `PECHARUNT`, `ARCHALUDON`, `HYDRAPPLE`, `TERAPAGOS`, etc.) in `Graphics/Pokemon/` are `192×192` Front and `288×288` Back. Because EBDX multiplies every sprite by `SCALE = 2`, they render at a **giant `384×384` / `576×576`**!
   - **Fix:** Replace with 1× Gen 5 animated strips (`H ≈ 64–112 px`), and for any remaining static fallback, either nearest-neighbor downsample `2×`/`3×` pixel-art sprites back to 1× (`96×96`) OR set `SpriteScaleEnemy = 1` / `SpriteScalePlayer = 1` in `PBS/EBDX/pokemon.txt`.
4. **BUG 4 — Stale Static Files Blocking Fallback (`EBDX/Battlers/Front/{172_1,483_1,999}.png`):**
   - `999.png` (`96×96`, Gimmighoul), `172_1.png` (`160×160`), and `483_1.png` (`88×88`) are single-frame static files sitting inside the animated folder. Replace with real animated strips or purge.

---

## A.4 Verified Active Open-Source Gen 5 B2W2-Style Animated Sprite Packs (Gens 6–9, Regionals, Megas)

**Strict Aesthetic Policy:** Keep Prismfall **100% 2D Gen 5 B2W2 pixel art**. **NEVER** import Pokémon Showdown's `ani/` (3D XY/SM/SwSh models) — only 2D sprite packs below!

| Priority | Source Pack | Verified URL | Coverage | Format | License / Credit Terms |
|---:|---|---|---|---|---|
| **1 (Primary All-in-One)** | **Open-Source EBDX Renovation Project 4.0** (ChromeValiant, Oct 2026) | `https://eeveeexpo.com/resources/1831/` | **Gens 1–9 + Regional Variants + ALL Mega Evolutions** (including revamps of Mewtwo X/Y, Rayquaza, all Megas by Aronousqui & Mangalos810, plus Ghasty_001 & La Base de Sky & Lucidious89 sprites) | Essentials v21.1 horizontal PNG strips (`Graphics/Pokemon/...`, ready for EBDX `BitmapEBDX`!) | Free for non-commercial fan games **with full credits** (copy credits block from Eevee Expo resource page / `README.md` into Prismfall's `CREDITS.md`). |
| **2 (Primary Standalone `[SPRITES]`)** | **Animated Pokémon System [DBK Add-On] [v21.1] — `[SPRITES]` pack** (Lucidious89, v1.1.3 Aug 2026) | `https://eeveeexpo.com/resources/1544/` | **Gens 1–9 DLC + Regional Forms + Megas** (sprites shipped separately from DBK scripts, so no DBK conflict with EBDX!) | Horizontal PNG strips (`Front`, `Back`, `Front shiny`, `Back shiny`) | Free for non-commercial Essentials fan games **with credits** to Lucidious89, Luka S.J., Golisopod User, Smogon XY/SM/SwSh/SV Sprite Projects, and the Spanish *Sprites Animados* contributors. |
| **3 (Direct GitHub — High-Polish Gen 6–9 & Hisuian/Mega)** | **`Ghasty001/Animated_sprites_by_Ghasty001`** | `https://github.com/Ghasty001/Animated_sprites_by_Ghasty001` | Direct GitHub `FRONT/`, `BACK/`, `FRONT_SHINY/`, `BACK_SHINY/` for **Gholdengo**, **Annihilape**, **Nacli–Garganacl**, **Smoliv–Arboliva**, **Fidough–Dachsbun**, **Tarountula–Spidops**, **Armarouge/Ceruledge**, **Kingambit**, **Clodsire**, **Dreepy–Dragapult**, **Clauncher/Skrelp/Heliolisk/Trevenant**, **Hisuian Braviary/Qwilfish/Voltorb/Electrode/Sliggoo/Avalugg/Sneasel/Sneasler**, **Wyrdeer**, **Mega Altaria/Ampharos/Beedrill** | Ready-to-use horizontal PNG strips (git-clonable directly!) | Explicitly *"free to use for other projects with credit"* (Ghasty_001 + base spriters listed in repo `README.md`). |
| **4 (Direct GitHub/GitLab Base)** | **`La Base de Sky`** (Skyflyer & DPertierra, v1.1.2 May 2026) | `https://gitlab.com/la-base-de-sky/La-Base-de-Sky` (mirror: `https://github.com/SkyFangames/La-Base-de-Sky`) | Essentials v21.1 Spanish community animated Gen 5–9 + Hisui + Paldea battler strips | Horizontal PNG strips | Free non-commercial use with credit to *La Base de Sky* / *Sprites Animados* team. |
| **5 (Direct CDN Gap-Filler — GIF→PNG)** | **Pokémon Showdown `gen5ani` Buckets** (Smogon BW Sprite Project, updated July 2026) | `https://play.pokemonshowdown.com/sprites/gen5ani/`, `gen5ani-back/`, `gen5ani-shiny/`, `gen5ani-back-shiny/` | Live community-contributed Gen 5-style animated **GIFs** for Gen 1–9, Megas (`-mega`, `-megax`, `-megay`), Primals (`-primal`), and Regional variants (`-alola`, `-galar`, `-hisui`, `-paldea`), including `gholdengo.gif`, `abomasnow-mega.gif`, `alakazam-mega.gif`, etc. | Animated `.gif` → converted losslessly via Pillow to `N*H × H` PNG strips | Smogon BW Sprite Project terms: free non-commercial fan-game use with credit to Smogon X/Y, S/M, SwSh, S/V Sprite Project contributors (`https://www.smogon.com/forums/threads/smogon-sprite-project.3647722/`). |

---

## A.5 Repeatable Importer Blueprint: `tools/install_ebdx_animated_sprites.py`

Claude should implement `tools/install_ebdx_animated_sprites.py` (pure Python 3 + Pillow `PIL.Image`, zero destructive overwrites of Gen 1–5 unless `--force`) with the following exact architecture:

### CLI Contract
```bash
# 1. Audit current gaps vs live Prismfall PBS (read-only)
python3 tools/install_ebdx_animated_sprites.py --engine /home/antigravity/pf_engine_run/base --audit

# 2. Import from local downloaded pack(s) in priority order (e.g., Renovation 4.0 / Lucidious [SPRITES] / Ghasty001)
python3 tools/install_ebdx_animated_sprites.py \
  --engine /home/antigravity/pf_engine_run/base \
  --source renovation4=/path/to/EBDX_Renovation_4/Graphics/Pokemon \
  --source ghasty=/path/to/Animated_sprites_by_Ghasty001 \
  --fetch-showdown-gaps \
  --normalize-extensions \
  --write-credits docs/CREDITS_SPRITES.md

# 3. Smoke-test specific priority species (Dorian troupe, Megas, Gen 9 bosses)
python3 tools/install_ebdx_animated_sprites.py --engine /home/antigravity/pf_engine_run/base --verify ZORUA_1 MELOETTA MELOETTA_1 OGERPON PECHARUNT METAGROSS_1 SALAMENCE_1 GALLADE_1
```

### Core Pipeline Steps
1. **PBS Index Loader:** Parse `PBS/pokemon.txt` (`[A-Za-z0-9_]+` — MUST allow lowercase `f`/`m` for `NIDORANfE`/`NIDORANmA`!) and `PBS/pokemon_forms.txt` to map every canonical `(SPECIES, form)` ↔ `(dex_num, EBDX filename, Showdown slug)`.
   - Showdown slug mapping table:
     - `ZORUA,1` → `zorua-hisui`, `ZOROARK,1` → `zoroark-hisui`
     - `VULPIX,1` → `vulpix-alola`, `WEEZING,1` → `weezing-galar`, `WOOPER,1` → `wooper-paldea`
     - `CHARIZARD,1` → `charizard-megax`, `CHARIZARD,2` → `charizard-megay`, `SLOWBRO,2` → `slowbro-mega`, `KYOGRE,1` → `kyogre-primal`, `GROUDON,1` → `groudon-primal`
     - `OGERPON,1..3` → `ogerpon-wellspring`, `ogerpon-hearthflame`, `ogerpon-cornerstone`
     - `MELOETTA,1` → `meloetta-pirouette`
2. **Preserve Official Gen 1–5 B2W2 Strips:** Never overwrite existing animated Gen 1–5 strips (`001.png`–`649.png` where `W > H && W % H == 0`) unless `--overwrite-gen1-5` is explicitly passed.
3. **Multi-Source Cascade (Front, Back, FrontShiny, BackShiny, Female):**
   - For every missing/static `(species, form, view)`:
     - Check local `--source` directories in order (accepts both `Front`/`Back`/`FrontShiny`/`BackShiny` and `Front`/`Back`/`Front shiny`/`Back shiny` and `FRONT`/`BACK`/`FRONT_SHINY`/`BACK_SHINY` layouts).
     - Validate that the source PNG is genuinely animated (`W > H`, square frames `W % H == 0`, frame count `>= 2`).
     - If `--fetch-showdown-gaps` is enabled and still missing, fetch from `https://play.pokemonshowdown.com/sprites/gen5ani{,-back,-shiny,-back-shiny}/{slug}.gif` (strictly `gen5ani*`, NEVER `ani*`) and run **GIF → EBDX Horizontal Strip Conversion**:
       - Composite every GIF frame onto an RGBA canvas (handling GIF disposal modes `2`/`3` cleanly!).
       - Determine square cell side `S = max(max_frame_w, max_frame_h)` (typically `96` or `max(w,h)`), bottom-center each frame inside its `S × S` cell so `PrismfallEBDX.grounded_oy` reads a steady foot line.
       - Normalize frame rate: expand long-delay frames by `round(duration_ms / 50)` (capped at 4× duplicate frames so strips stay compact, matching EBDX's ~20fps tick at `speed=1`).
       - Stitch horizontally into `(N * S) × S` RGBA PNG (`optimize=True`).
4. **Scale Guard (Prevent Giant 384px/576px Sprites):**
   - Check frame height `H`: if a source strip is pre-upscaled 2× (`H >= 160` with pixel blocks of 2×2, e.g., Lucidious/Gen 9 192px sheets), detect exact 2× pixel-grid scaling and nearest-neighbor downsample by `0.5×` to native Gen 5 1× (`H = 80–96 px`), OR emit `SpriteScaleEnemy = 1` / `SpriteScalePlayer = 1` into `PBS/EBDX/pokemon.txt`.
5. **Hygiene & Companion Fixes:**
   - Rename all 29 uppercase `*.PNG` files in `Graphics/Pokemon/` to lowercase `*.png`.
   - Remove stale static placeholders inside `Graphics/EBDX/Battlers/` (`999.png`, etc.) once replaced.
   - Patch `Battler Bitmaps.rb:199–207` and `341–350` so `folder2` maps shiny fallbacks to `"Front shiny"` / `"Back shiny"`.
   - Update `BattlerAltitude = 10` in `PBS/EBDX/pokemon.txt` for hovering Gen 7–9 species (Pecharunt, Flutter Mane, Iron Moth, Gholdengo, Tapus, etc.).
   - Emit `docs/CREDITS_SPRITES.md` with per-source attribution automatically populated from every sprite actually installed!
6. **Testing in `/home/antigravity/pf_engine_run/`:**
   - Run `tools/install_ebdx_animated_sprites.py --audit` before/after to prove live gap drops from **248 / 264 → ~0** (or exact single-digit remaining community gaps).
   - Boot a headless battle capture against Dorian (`ZORUA,1` + `MELOETTA` Aria/Pirouette), Ogerpon, Pecharunt, and Mega Metagross via `tools/harness/` to verify zero `BitmapEBDX` load errors, valid `grounded_oy` foot lines, and clean frame counts.

---

# PART B — Ban All Main-Story Legendary Captures → Reborn-Style Tiered Postgame Legendary Quest Network

## B.1 Exhaustive Audit of Every Legendary, Mythical, Sub-Legendary, Ultra Beast & Paradox Reference

Audited across `design/POKEMON_AVAILABILITY.md`, `design/EVENT_POKEMON.md`, `design/BOSSES.md`, `design/FLAGS.md`, `design/NARRATIVE_KEYS.md`, `design/WALKTHROUGH.md`, `design/TRIALS_QUESTS.md`, `design/TRIAL_EVENTS.yaml`, `pbs/encounters.txt`, `pbs/encounters_badgetiers.txt`, `plugins/Prismfall Bosses/*.rb`, `plugins/Prismfall Core/008_Festival_Data.rb`, `plugins/Prismfall Trials/*.rb`, and `story/00–34*.md`.

### Complete Violation & Status Matrix (Chapters 0–21 + Festival)

| # | Species / Group | Category | Current Story Slot | Exact Repo Files & Lines | Current Catch/Gift Status | Required Action |
|---:|---|---|---|---|---|---|
| **1** | **Type: Null** (Lv 45/50) | Legendary | **Ch10** (Act III, Meridian Black Site, Map `699`) | `story/28_SCRIPT_CH10.md:98–112`, `story/06_ACT_III.md:24`, `design/POKEMON_AVAILABILITY.md:31`, `design/FLAGS.md:124` (`S180 TYPE_NULL_GIFT`), `design/NARRATIVE_KEYS.md:154,186` (`:ch10_null`), `design/WALKTHROUGH.md:1862` | **LEAK — GIFTED IN ACT III!** (`Received: TYPE: NULL, Lv 45` on `:ch10_null == :take`) | **BLOCK GIFT IN CH10.** Keep the Black Site scene & `:ch10_null` choice intact (`VOSS+2 MERIDIAN+1`), but change `:take` so Quent's cradle locks down / Calla slips you the **Null Cradle Key** (Key Item) instead of handing over the Pokémon ("Meridian won't let an uncalibrated prototype off-site before the Festival"). Move Type: Null reception to **Postgame Tier 1 (Meridian Vault — Project NULL)** gated on `S160 POSTGAME`! |
| **2** | **Kubfu** (Lv 60) | Legendary | **Act IV** (Ironreach Dojo, Map `263`) | `design/POKEMON_AVAILABILITY.md:32` | **LEAK — GIFTED IN ACT IV!** ("Act IV \| Ironreach dojo (any branch) \| Kubfu Lv 60") | **MOVE TO POSTGAME TIER 1.** In Act IV the Ironreach Pit-Dojo awards a **Dark/Water Scroll Seal** (Key Item) or non-legendary `Falinks` (`NA_FALINKS`, already in `EVENT_POKEMON.md:46`); Kubfu joins only after `S160 POSTGAME` in **Ironreach Pit-Dojo Mastery**! |
| **3** | **Regirock** (Lv 64) | Sub-Legendary | **Act IV** (Stonesleep Braille, Map `788`) | `design/POKEMON_AVAILABILITY.md:58` (`Groudon + Regirock (Stonesleep braille) \| Act IV \| 64`); `story/07_ACT_IV.md:96` & `design/WALKTHROUGH.md:2311` (currently fossils only) | **DESIGN LEAK — LISTED IN ACT IV!** | **LOCK BEHIND `S160 POSTGAME`.** During Act IV, Stonesleep (`788`) holds fossil beds and a sealed braille monolith that hums *"Return when the Eighteen are weighed."* Move Regirock into **Postgame Tier 1 (Stonesleep Braille)** alongside the full Regi chain! |
| **4** | **Loyal Three** (`Okidogi`, `Munkidori`, `Fezandipiti`, Lv 46) | Sub-Legendary | **Ch10** (Act III, Bride Grove, Map `708`) | `story/28_SCRIPT_CH10.md:346–388`, `story/06_ACT_III.md:45`, `design/POKEMON_AVAILABILITY.md:53`, `design/WALKTHROUGH.md:1867,1917` | **UNREGISTERED BOSS** (`:LOYAL_THREE [NEW]`) — story script has them flee (`S127`), no capture | **REGISTER WITH `:catch => false`** in `109_Boss_LoyalThree.rb` (`disablePokeBalls = true`, 3-boss multi-bar sequence). Catchable ONLY in **Postgame Tier 1 (Gloamwood Masks)**! |
| **5** | **Ogerpon** (Lv 48 ally / Lv 78 arc) | Legendary | **Ch10** (partner), **Ch18** (Gloamwood), **Festival** (Juno's J4 team) | `story/28_SCRIPT_CH10.md:324–403`, `story/06_ACT_III.md:44–49`, `story/08_ACT_V.md:28,174,473`, `design/POKEMON_AVAILABILITY.md:53`, `design/FLAGS.md:135` (`S223 OGERPON_TRUSTED`) | Narrative partner only (`PARTNER_OGRE` AI ally in Ch10; walks to Gloaming in Ch18; Juno's partner at Festival) — **must never enter PC's box pre-postgame** | **KEEP NARRATIVE BOND, ZERO STORY CAPTURE/GIFT.** Update `POKEMON_AVAILABILITY.md:53` to clarify Ogerpon is **not catchable in Act V**; joins/catchable ONLY in **Postgame Tier 1 (Gloamwood Masks)** after reconciling the Loyal Three! |
| **6** | **Pecharunt** (Lv 78) | Mythical | **Ch18** (Act V, Lightless Deep B1F) | `story/08_ACT_V.md:21–28,473`, `design/POKEMON_AVAILABILITY.md:56`, `design/FLAGS.md:89` (`S150`), `design/WALKTHROUGH.md:2788,2861` | **UNREGISTERED BOSS** — story frees thralls (`S150`), no capture | **REGISTER WITH `:catch => false`** in `110_Boss_Pecharunt.rb`. Catchable ONLY in **Postgame Tier 1 (Lightless Deep Seal)**! |
| **7** | **Kyogre** (Lv 55 / 80 / 85) | Legendary | **Ch11** (`:KYOGRE_ISENMAR`, `:KYOGRE_WEATHER`) & **Ch19** (`:KYOGRE_GLASS_DUNES`) | `plugins/Prismfall Bosses/101_Boss_Kyogre.rb:20,57`, `106_Boss_WarLegends.rb:96`, `design/POKEMON_AVAILABILITY.md:54` | **ALREADY SAFE** (`:catch => false` on all 3 configs!) | Keep `:catch => false`. Rematch & catch (`:catch => :last_bar`) in **Postgame Tier 3 (Whalebone Keep Ice Vault `308`)**. |
| **8** | **Groudon** (Lv 66) | Legendary | **Ch14** (`:GROUDON_UNDERSANDS`, Map `783`) | `plugins/Prismfall Bosses/107_Boss_Groudon.rb:22`, `design/POKEMON_AVAILABILITY.md:58` | **ALREADY SAFE** (`:catch => false`!) | Keep `:catch => false`. Rematch & catch in **Postgame Tier 3 (Duneholt Undersands `783`)**. |
| **9** | **Giratina** (Lv 70) | Legendary | **Ch15** (`:GIRATINA_DEPTHS`, Map `806`) & **R1** (Ruin trial) | `plugins/Prismfall Bosses/108_Boss_Giratina.rb:23`, `story/12_RUIN_ROUTE.md:18,87`, `design/POKEMON_AVAILABILITY.md:59` | **ALREADY SAFE** (`:catch => false`!) | Keep `:catch => false` (including Ruin Route R1 trial!). Rematch & catch in **Postgame Tier 3 (Distortion Core `910`)**. |
| **10** | **Zekrom** (Lv 72) | Legendary | **Ch16** (`:ZEKROM_ENGINE`, Cogsworth) | `plugins/Prismfall Bosses/102_Boss_Zekrom.rb:20`, `design/POKEMON_AVAILABILITY.md:55` | **ALREADY SAFE** (`:catch => false`!) | Keep `:catch => false`. Rematch & catch in **Postgame Tier 3 (Stormwatch Spire Roof)**. |
| **11** | **Reshiram** (Lv 85) | Legendary | **Ch19** (`:RESHIRAM_GLASS_DUNES`, Map `926`) | `plugins/Prismfall Bosses/106_Boss_WarLegends.rb:62`, `design/POKEMON_AVAILABILITY.md:57` | **ALREADY SAFE** (`:catch => false`!) | Keep `:catch => false`. Rematch & catch in **Postgame Tier 3 (Wyrmscar Depths)** (even if Reshiram flew with Sigrun — Sigrun tests you in postgame to earn its respect!). |
| **12** | **Zygarde** (Cells / Core) | Legendary | **Ch13** (`748` Core) → **Postgame** (`ZYGARDE_CHOOSES`) | `story/06_ACT_III.md:251`, `story/08_ACT_V.md:471`, `design/FLAGS.md:33` (`V121 ZYGARDE_CELLS_STORY`), `design/NARRATIVE_KEYS.md:332` | **SAFE IF ENFORCED** — Cells/Core are collectible story items, Assembly is postgame | Explicitly lock Zygarde Cube assembly until `S160 POSTGAME` (Valen's Memorial, **Postgame Tier 3**). |
| **13** | **Arceus** (Lv 100) | Mythical | **Ch21** (`:ARCEUS_FINALE`, Festival True Finale) | `plugins/Prismfall Bosses/103_Boss_Arceus.rb:85`, `plugins/Prismfall Core/008_Festival_Data.rb:150,154`, `design/POKEMON_AVAILABILITY.md:60` | **ALREADY SAFE** (`:catch => false`, `"disablePokeBalls"`) | Keep `:catch => false` in Ch21. Catchable ONLY in **Postgame Tier 3 Capstone (18-Plate Convergence)**! |
| **14** | **Paradox Pokémon (14 species)** | Paradox | **Postgame Map `905`** (Shardfall Isles) | `pbs/encounters.txt:2848–2861`, `design/POKEMON_AVAILABILITY.md:15,84` | **ALREADY SAFE** (Map `905` is postgame-only) | Verify Map `905` warp is hard-gated on `$game_switches[160]` (`POSTGAME`). Move 6 Legendary Paradoxes (Walking Wake/Gouging Fire/Raging Bolt, Iron Leaves/Iron Boulder/Iron Crown) into **Postgame Tier 2**! |
| **15** | **All Event Mons & Wild Tables** | Check | Ch0–21 (`EVENT_POKEMON.md` 1–52, `encounters.txt` 132 maps) | `plugins/Prismfall Trials/130–133_EventMons_*.rb`, `pbs/encounters*.txt` | **VERIFIED CLEAN** — 0 Legendaries/Mythicals/UBs in `encounters.txt` (outside Map `905`) or `EventMons`! | Preserve zero-legendary rule in `tools/harness/run_trials.rb` & `validate_encounters.py`. |

*(Note: Enemy trainers — Kestrel v90 Genesect, Valen Zygarde, Voss/Quent Silvally, Theodric Kyogre/Groudon/Regigigas, Alexandra Latias, and Gym 1 Dorian Meloetta — are uncatchable trainer battles and remain 100% intact!)*

---

## B.2 Hard Engine Safety Net (Code Change Blueprint)

To guarantee **zero main-story legendary captures can ever slip through** (even from future chapter scripts or debug mistakes), add a single authoritative gate in `plugins/Prismfall Core/` + `plugins/Prismfall Bosses/004_Bosses_Battle.rb`:

```ruby
# In Prismfall Core (e.g. 018_Endings.rb):
module Prismfall
  # Flags from Essentials v21.1 / Gen 9 Pack PBS: Legendary, Mythical, SubLegendary, UltraBeast, Paradox
  LEGENDARY_FLAGS = %w[Legendary Mythical SubLegendary UltraBeast Paradox].freeze
  EXTRA_LOCKED_SPECIES = %i[TYPENULL SILVALLY KUBFU URSHIFU].freeze

  def self.postgame_unlocked?
    return true if Prismfall::Endings.postgame?
    return ($game_switches && $game_switches[160]) ? true : false
  end

  def self.story_legendary_locked?(pkmn)
    return false if !pkmn || postgame_unlocked?
    sp = GameData::Species.try_get(pkmn.species)
    return false if !sp
    return true if EXTRA_LOCKED_SPECIES.include?(sp.species)
    flags = sp.flags || []
    return LEGENDARY_FLAGS.any? { |f| flags.include?(f) }
  end
end
```

And hook **`Battle#pbThrowPokeBall`** (in `004_Bosses_Battle.rb:247`) + **`Prismfall::Bosses::BossState#catchable?`** (`003_Bosses_State.rb:56`):
- If `Prismfall.story_legendary_locked?(target.pokemon)` is true, **always force `disablePokeBalls = true` / deflect the ball** with:
  `"Its power refuses to be bound while Velmora's Plates remain unsettled!"`
- Zero effect once `S160 POSTGAME` / `Prismfall::Endings.postgame?` turns ON!

---

## B.3 Pokémon Reborn-Style 3-Tier Postgame Legendary Quest Network

Inspired directly by *Pokémon Reborn*'s beloved postgame quest board (tiered anomaly dossiers, interconnected puzzle dungeons, character callbacks, multi-bar boss rematches with `:catch => :last_bar`, and a finale convergence):

### Unlock & Hub Architecture
- **Master Gate:** `$game_switches[160]` (`POSTGAME`, set upon completing Main Story + Festival + Epilogue; see `design/FLAGS.md:99` and `018_Endings.rb:55`).
- **Hub NPC & Board:** **Professor Larch's Postgame Registry** at the **Crownhaven Accord Hall / Concordance Spire Lobby** (`S266 PG_SPIRE_OPEN`), integrated directly into `Prismfall::Trials` as a new `:POSTGAME` quest category (`115_Quests_PostgameLegends.rb`) with tracked progress in the Quest Log (`009_Trials_QuestLog.rb`)!
- **Reserved Switch Allocation (`design/FLAGS.md:156`, currently `S270–S300` reserved):**
  - `S270`: `PG_LEGENDS_BOARD_OPEN` (Tier 1 unlocked immediately on `S160`)
  - `S271–S278`: Tier 1 Quest Clear Flags (8 major regional/mythical chains)
  - `S279`: `PG_TIER2_RIFTS_OPEN` (unlocks automatically when `>= 4` Tier-1 chains cleared + `S268 PG_DISTORTION_OPEN`)
  - `S280–S284`: Tier 2 Rift/Anomaly Clear Flags (5 major anomaly chains)
  - `S285`: `PG_TIER3_APEX_OPEN` (unlocks when Tier 2 keystones cleared + `S267 PG_GAUNTLET_OPEN`)
  - `S286–S293`: Tier 3 Apex Rematch Capture Flags (Kyogre, Groudon, Zekrom, Reshiram, Giratina, Zygarde, Cosmic, Capstone)
  - `S294`: `PG_ARCEUS_CONVERGENCE_DONE`
- **Ending Compatibility (No Unfair Lockouts!):**
  - Full 3-tier access on `END_HOMECOMING`, `END_UNFINISHED`, `END_EMPTY_LIGHTHOUSE`, `END_LONG_VIGIL`, `END_BORROWED_CROWN` (dialogue adjusts via `S263`/`S264`).
  - On `END_UNMAKING` / `END_REFLECTION` (`S265 PG_RUIN_WORLD`), Tiers 1–2 and Giratina/Apex rematches open through **Mirrorwalk Rifts**, while **Arceus does not return** (honoring `story/12_RUIN_ROUTE.md:87`).
  - On `END_HOLLOW_SPRING` / `END_CONCORD_DAWN`, Tier 1 Regional/Mythical quests still open via Larch's Registry (so players aren't punished with an empty postgame), while `END_GILDED_CHAIN` remains the sole `NO_POSTGAME_ENDINGS` bad ending (`012_Narrative_Data.rb:470`).
- **Capture Mechanic Standard:** Every postgame legendary boss uses `Prismfall::Bosses` with **2–3 bars** (3–4 on Hard) and **`:catch => :last_bar`** (`003_Bosses_State.rb:59`), so the player MUST earn the fight by breaking its shields before Poké Balls unlock on the final bar — classic Reborn/Rejuvenation prestige!

---

### TIER 1 — Regional Trials & Mythical Encores (Lv 82–90 | Unlocked immediately on `S160 POSTGAME`)

| # | Quest Name (`Trials` ID) | Switch | Location (Map ID) | Field | Legendaries / Mythicals | Reborn-Style Quest Structure & Story Callback |
|---:|---|---|---|---|---|---|
| **T1-1** | **Crownhaven Encore** (`PG_MELOETTA`) | `S271` | Pell Playhouse (`154`) → Crownhaven Opera Hall | `:GRAND_STAGE` (Stage 3!) | **Meloetta** (Lv 85, full 600-BST, `:catch => :last_bar`) | **Direct Gym 1 callback!** Dorian sends a gold playbill: his Prima Donna muse held back in Act One so you could shine, and now she wants an *Opening Night* duet with the Champion. Perform a 3-bout Encore showcase (vs Dorian's Lv 90 troupe, then a 2-bar wild boss battle vs Meloetta Aria ↔ Pirouette at full power on Standing Ovation!). On defeat/capture, Dorian bows: *"Take her on tour, darling. The whole world is a stage now."* |
| **T1-2** | **The Masks of Gloamwood** (`PG_OGERPON`) | `S272` | Bride Grove (`708`) & Gloamwood Shrine | `:FLOWER_GARDEN` / `:FAIRY_TALE` | **Okidogi, Munkidori, Fezandipiti** (Lv 84) → **Ogerpon** (Lv 88, + **Wellspring / Hearthflame / Cornerstone Masks**) | Juno invites you back to the Bride Tree. Free of Pecharunt's poison, the **Loyal Three** haunt Elowen's three ancient border stones in shame — defeat & catch each (`:catch => :last_bar`) to lay the false pageant to rest. Then **Ogerpon** challenges you across all 4 masks (changing mask on each bar break!) before choosing to join your team. (Unlocks even if `:ch10_ogre == :hesitate`, via an extra reconciliation beat with Juno!) |
| **T1-3** | **The Bitter Mochi Seal** (`PG_PECHARUNT`) | `S273` | Lightless Deep B1F (Nadir) | `:CORROSIVE_MIRE` → `:NEW_MOON` | **Pecharunt** (Lv 86, 2-bar, `:catch => :last_bar`) | Corvin & Wenlow detect a lingering Sweetrot echo beneath the Moon Market (`423`). Brew Larch's neutralizing Kelp Tea (callback to Running Gag #1!) to break Pecharunt's dormant shell, battle it through Toxic Chain phases, and seal/catch it. |
| **T1-4** | **The Stonesleep Braille** (`PG_REGIS`) | `S274` | Stonesleep (`788`), Whalebone Vault (`308`), Cogsworth Core, Static Tunnels, Wyrmscar | `:CAVE` / `:FROZEN_LAKE` / `:FACTORY` | **Regirock, Regice, Registeel** (Lv 84) → **Regieleki & Regidrago** (Lv 86) → **Regigigas** (Lv 90) | Sahar deciphers the full Stonesleep braille monolith (`788`, formerly locked in Act IV). Classic Reborn-style multi-kingdom braille puzzle: awaken the 3 elemental Regis across Ossaria, Isenmar, and Zenith; bring all 3 to open the twin Electromagnet/Dragon-fang chambers (`Regieleki`, `Regidrago`); bring all 5 to wake **Regigigas** in the Aurelia Ruin Vault! |
| **T1-5** | **The Three Mirror Lakes** (`PG_LAKES`) | `S275` | Mirror Mere (Lucent), Lake Rime (`300`), Lake Sallow (`650`) | `:MINDSCAPE` / `:WATER_SURFACE` | **Uxie, Mesprit, Azelf** (Lv 84) | Archseer Dask & Ilsa sense three psychic ripples across Velmora's three great lakes (Knowledge in Lucent's Mirror Mere, Emotion in Lake Rime, Willpower in Lake Sallow). Each requires a short riddle/reflection puzzle before a 2-bar capture trial. |
| **T1-6** | **Project NULL — Unmasked** (`PG_TYPENULL`) | `S276` | Meridian Black Site (`699`) → Concord Zero Vault (`S269`) | `:FACTORY` → `:PRISM_ARENA` | **Type: Null** (Lv 82 gift/catch) + **all 17 Memories** + **Genesect** (Lv 88, + 4 Drives) | **Direct Ch10 payoff!** Replaces the banned Act III gift. Calla Wren & Kestrel (if alive) help you raid Quent's sealed Black Site cradle (`699`). Defeat Quent's automated security protocols to free **Type: Null** (`S180 TYPE_NULL_GIFT`, now strictly postgame!), unlock the 17 Memory cache across the Bleed zones, and uncover Meridian's archived **Genesect** prototype (tied to Kestrel's Festival ace!). |
| **T1-7** | **The Pit-Dojo Scrolls** (`PG_KUBFU`) | `S277` | Ironreach Dojo (`263`) → Ebbmouth Cliffs & Underveil Spire | `:COLOSSEUM` | **Kubfu** (Lv 80 gift) + **Scroll of Darkness & Scroll of Waters** (`Urshifu`) | **Replaces banned Act IV gift!** Kaito invites the Champion to a 5-round Iron Pit mastery gauntlet (no Bag items). Winning earns **Kubfu**, and visiting the two ancient shrines (Ebbmouth Tide Tower / Underveil Shadow Tower) unlocks BOTH evolution scrolls. |
| **T1-8** | **Velmora Roamers, Guardians & Mythical Vignettes** (`PG_ROAMERS`) | `S278` | Kingdom Sanctuaries & Weather Peaks | Kingdom native fields | **Birds (Kanto + Galar)**, **Beasts (`Raikou/Entei/Suicune`)**, **Latias/Latios**, **Heatran**, **Cresselia/Darkrai**, **Swords of Justice (`Cobalion/Terrakion/Virizion/Keldeo`)**, **Forces of Nature (`Tornadus/Thundurus/Landorus/Enamorus`)**, plus **Mythical Side-Encores** (`Mew`, `Celebi`, `Jirachi`, `Manaphy/Phione`, `Shaymin`, `Victini`, `Diancie`, `Magearna`, `Marshadow`, `Zeraora`, `Zarude`, `Meltan/Melmetal`, `Hoopa`, `Volcanion`, `Deoxys`) | Each Warden posts one postgame rumour on Larch's board tying a legendary to their kingdom's biome (e.g., Brann → **Heatran** in Cinderhorn Caldera `664`; Ysolde → **Darkrai/Cresselia** in Vane Hall & Dreaming Quarter `768`; Odessa → **Articuno/Zapdos/Moltres** + Galar variants on Stormfront/Hoarwood/Cinderhorn; Marisol → **Manaphy/Latias/Latios** in Hallow Strait `900–901`; Celestine → **Diancie/Shaymin/Celebi** in Gloamwood; Bastian → **Deoxys** meteor in Crystal Cavern). |

---

### TIER 2 — Glassfall Bleed Rifts & Ruin Anomalies (Lv 90–95 | Unlocks at `>= 4` Tier-1 clears + `S268 PG_DISTORTION_OPEN`)

| # | Quest Name (`Trials` ID) | Switch | Location (Map ID) | Field | Species | Reborn-Style Quest Structure |
|---:|---|---|---|---|---|---|
| **T2-1** | **The Eleven Bleed Rifts** (`PG_UBS`) | `S280` | 7 Kingdom Bleed Zones + Hallow Strait (`900`) | `:BLEED` / `:INVERSE` | **All 11 Ultra Beasts** (`Nihilego`, `Buzzwole`, `Pheromosa`, `Xurkitree`, `Celesteela`, `Kartana`, `Guzzlord`, `Stakataka`, `Blacephalon`, `Poipole → Naganadel`) | **Reborn Anomaly-style rift hunt!** With the Glass still leaking (`story/07_ACT_IV.md:161`), Larch distributes **Beast Balls** at Tidewatch/Spire. Close 10 kingdom-matched Bleed Rifts (e.g., `Xurkitree` in Lumen Static Tunnels, `Nihilego` in Gossamer Glasswood, `Guzzlord` in Nadir Sump, `Kartana` in Briarwick Looms, `Stakataka` in Stonesleep, `Blacephalon` in Saltmere Backstage!). Closing all 10 rewards a **Poipole** from the final rift! |
| **T2-2** | **Guardians of the Shardfall** (`PG_TAPUS`) | `S281` | Shardfall Isles (`905`) — 4 Cardinal Ruins | `:NEON_GRID` / `:MINDSCAPE` / `:FLOWER_GARDEN` / `:WATER_SURFACE` | **Tapu Koko, Tapu Lele, Tapu Bulu, Tapu Fini** (Lv 92) | Explore the four compass ruins of the postgame **Shardfall Isles (`905`)** where Velmora's quarantine began; each Tapu guards an elemental monolith and transforms the terrain on bar breaks (`:catch => :last_bar`). |
| **T2-3** | **The Four Cursed Stakes of Theodric** (`PG_RUIN_QUARTET`) | `S282` | 4 Shrines (Elowen, Isenmar, Ossaria, Ashkaar) | `:WASTELAND` / `:FROZEN_LAKE` / `:DESERT` / `:VOLCANIC` | **Wo-Chien, Chien-Pao, Ting-Lu, Chi-Yu** (Lv 93) | **Direct Velmora lore tie-in!** Centuries before AF 0, King Theodric's court sealed four relics of ruin (tablet, sword, vessel, beads) under 4 × 4 = 16 glowing stakes across the kingdoms. Pull each color's 4 stakes (tracked in Quest Log!) to unseal its shrine and battle/catch each Treasure of Ruin! |
| **T2-4** | **Prism Echoes — Paradox Sovereigns** (`PG_PARADOX`) | `S283` | Shardfall Isles (`905`) Deep Crater | `:PRISM_ARENA` / `:CRYSTAL_CAVERN` | **Wild 14 Paradoxes** (`pbs/encounters.txt:2848`) + **Walking Wake, Gouging Fire, Raging Bolt, Iron Leaves, Iron Boulder, Iron Crown** (Lv 94) | Wild Paradox spawns roam `905` surface; inside the deep Prism Crater, two 3-mon Paradox anomalies (Past Trio / Future Trio) spawn as 2-bar bosses (`:catch => :last_bar`) once you bring the matching Beast/Sword trio! |
| **T2-5** | **Crown of the Hoarwood** (`PG_CALYREX`) | `S284` | Northern Rimewood (`701`) & Gravenmoor Barrows (`760`) | `:FROZEN_LAKE` / `:HOLLOW_CATHEDRAL` | **Glastrier, Spectrier, Calyrex** (+ **Reins of Unity**) (Lv 93) | Follow Anja & Ysolde's winter legend across the Hoarwood and Obsidian Barrows to tame both steeds and unite the Harvest King. |

---

### TIER 3 — Apex Rematches & 18-Plate Convergence (Lv 95–100 | Unlocks after Tier 2 Keystones + `S267 PG_GAUNTLET_OPEN`)

| # | Quest Name (`Trials` ID) | Switch | Location (Map ID) | Field | Boss / Capture (`:catch => :last_bar`) | Multi-Bar Rematch & Lore Climax |
|---:|---|---|---|---|---|---|
| **T3-1** | **The Thawed Sea & Deep Seams** (`PG_WEATHER_TRIO`) | `S286` | Whalebone Keep Ice Vault (`308`), Duneholt Undersands (`783`), Skyreach Summit | `:WATER_SURFACE` / `:DESERT` / `:STORMFRONT` | **Kyogre** (Lv 95 + Blue Orb), **Groudon** (Lv 95 + Red Orb) → **Rayquaza** (Lv 98) | 3-bar Apex Rematches (`:KYOGRE_PG_CATCH`, `:GROUDON_PG_CATCH`) with Primal Reversion on Bar 2 and `:catch => :last_bar` on Bar 3. Bringing both to Skyreach Summit parts the Stormfront for **Rayquaza** (learns Dragon Ascent)! |
| **T3-2** | **Ideals, Truth & The Husk** (`PG_TAO_TRIO`) | `S287` | Stormwatch Spire Roof, Wyrmscar Depths, Frostfang Core | `:STORMFRONT` / `:DRAGONS_DEN` / `:FROZEN_LAKE` | **Zekrom** (Lv 95), **Reshiram** (Lv 95) → **Kyurem** (Lv 98 + DNA Splicers) | Rematch Zekrom over Zenith (`:ZEKROM_PG_CATCH`); spar Sigrun at Wyrmscar to earn Reshiram's duel (`:RESHIRAM_PG_CATCH`). Bringing both to Frostfang Core awakens **Kyurem** + unlocks DNA Splicers! |
| **T3-3** | **The Distortion Core** (`PG_GIRATINA`) | `S288` | Antumbra Distortion Core (`910`, `S268`) | `:INVERSE` | **Giratina (Origin)** (Lv 98 + Griseous Core) | Direct payoff of `story/08_ACT_V.md:472` & `story/12_RUIN_ROUTE.md:87`. Navigate the inverted Mirrorwalk labyrinth of `910`, mend the final Glass wound, and capture **Giratina** on Bar 3 (`:catch => :last_bar`). |
| **T3-4** | **Valen's Order — 100% Zygarde** (`PG_ZYGARDE`) | `S289` | Valen's Memorial (Crownhaven) | `:PRISM_ARENA` | **Zygarde (Complete / Power Construct)** (Lv 98) | Direct payoff of `V121 ZYGARDE_CELLS_STORY` and `ZYGARDE_CHOOSES` (`story/08_ACT_V.md:471`). Complete the Zygarde Cell hunt (cells scattered across all 7 kingdoms) and face Zygarde Complete at Valen's memorial (`:catch => :last_bar`). |
| **T3-5** | **Echoes of Distant Worlds** (`PG_BOX_LEGENDS`) | `S290–S292` | Hallow Strait Seabed (`901`), Distortion Rifts (`910`), Meridian Spire Summit, Prism Depths | Matching fields | **Mewtwo** (Meridian Lab), **Lugia & Ho-Oh** (Hallow Strait), **Dialga & Palkia** (Distortion Core), **Xerneas & Yveltal** (Bride Grove / Hollow Cathedral), **Cosmog → Solgaleo/Lunala & Necrozma** (Shattered Sky `748`), **Zacian, Zamazenta & Eternatus** (Crownhaven Ramparts / Spire), **Koraidon, Miraidon & Terapagos** (Shardfall Deep Crater `905`) | Unlocked cleanly in 3 themed Reborn-style anomaly sets (`Creation/Life`, `Light/Crown`, `Tera/Apex`), each tied to a cameo or Warden guide (e.g., Alexandra guides Dialga/Palkia; Celestine/Ysolde guide Xerneas/Yveltal; Quent's Concord Zero finale unlocks Mewtwo + Necrozma). |
| **T3-6** | **Capstone — The 18-Plate Convergence** (`PG_ARCEUS`) | `S294` | Crownhaven Prism Arena | `:PRISM_ARENA` → `:RAINBOW` | **Arceus** (Lv 100 + **Legend Plate**, 4-bar, `:catch => :last_bar`) | **Ultimate Postgame Finale** (non-Ruin endings). Requires: Warden's Gauntlet cleared (`S267`), all 18 Plates collected/resonated, and the Velmora Apex Quartet (`Kyogre`, `Groudon`, `Zekrom/Reshiram`, `Giratina`, `Zygarde`) registered. Ascend Crownhaven's Prism Arena for a 4-bar rematch (`:ARCEUS_PG_CATCH`, `ARCEUS_LEGEND_PHASE = true` on Bar 4!) where Arceus willingly lets you catch it on its final bar! |

---

# PART C — Gym Leader 1 Dorian Pell (`LEADER_DORIAN`, `:GRAND_STAGE`, Cap `15`) Team Redesign with Meloetta Ace

## C.1 Design Audit & Why the 2 Chosen Performers Are **Spinda** + **Jigglypuff**

Reuben's locked 4 Pokémon for Standard & Hard:
1. **`SMEARGLE`** (Normal — *The Set Painter / Curtain Raiser*)
2. **`CHATOT`** (Normal/Flying — *The Diva Songbird*)
3. **`ZORUA` (`Form = 1`, Hisuian)** (Normal/Ghost — *The Phantom Understudy*, disguised behind Meloetta via `ILLUSION`!)
4. **`MELOETTA`** (Normal/Psychic ↔ Normal/Fighting — *The Prima Donna Ace*, Singer ↔ Dancer via `RELICSONG`!)

**Selection of Slots 2 & 3 (Completing a 100% Normal-Type 6-Mon Theater Troupe):**

| Candidate | Types | BST | Role Overlap / Harness Risk | Verdict |
|---|---|---:|---|---|
| **Spinda** | Normal | 360 | **Zero overlap!** Owns the **Dance** mechanic (`TEETERDANCE` = Dance move → `+1 Speed` + applause step + confusion, `OWNTEMPO` prevents self-confusion; `COPYCAT` = stage improv!). Already on Dorian's team. | **PICK #1 (Slot 2 — Slapstick Stage Dancer)** |
| **Jigglypuff** | Normal/Fairy | 270 | **Zero overlap!** Owns the **Soprano / Crowd `SING` mechanic** that is explicitly wired into the **Saltmere Full House reward** (`design/BALANCE.md:420` & `102_Field_GrandStage.rb:145–146` — full house disables guaranteed-hit `Sing`!). Paper 20 Base Def ensures Badge-0 physical attackers punish it cleanly; Hard `COMPETITIVE` punishes stat drops. | **PICK #2 (Slot 3 — Chorus Soprano)** |
| *Minccino* | Normal | 300 | Redundant with Chatot (`ECHOEDVOICE`/`ROUND`/`ENCORE`) and Smeargle (`ENCORE`/`BABYDOLLEYES`). | Cut (role absorbed by Smeargle + Chatot) |
| *Whismur* | Normal | 240 | Redundant sound-spammer; less iconic than Spinda's Dance + Jigglypuff's Soprano. | Cut |
| *Furfrou* | Normal | 472 | **Explicitly banned by harness (`gen.py:203`)**: *"Furfrou's Fur Coat + Headbutt swept prepared teams at Lv 13–14."* | Rejected (overtuned) |
| *Igglybuff* | Normal/Fairy | 210 | Strictly weaker/less iconic version of Jigglypuff (15 Def / 20 SpD). | Rejected |

**Troupe Archetype Cast (Zero Role Duplication!):**
1. **Smeargle** — *Set Painter / Stagehand* (opens with `FAKEOUT` showpiece + `PAYDAY` coin-rain showpiece + `ENCORE` + `BABYDOLLEYES` / Hard `PARTINGSHOT` "Exit, stage left!")
2. **Spinda** — *Comic Dancer / Improv* (`TEETERDANCE` dance escalation + `COPYCAT`)
3. **Jigglypuff** — *Chorus Soprano* (`SING` + `DISARMINGVOICE` + `POUND`/`ROUND`, ties into Saltmere Crowd mechanic)
4. **Chatot** — *Diva Songbird* (`ECHOEDVOICE` / Hard `ROUND` + `PECK` + `ENCORE` — **strictly NO `CHATTER`, `BOOMBURST`, or `HYPERVOICE`**; `gen.py:203` explicitly noted Chatter swept prepared teams!)
5. **Hisuian Zorua (`Form = 1`)** — *Phantom Understudy* (Normal/Ghost, enters disguised as **Meloetta** via `ILLUSION`! Fragile 35/40/40 bulk gets OHKO'd by Badge-0 Dark `Bite`/`Thief`, while `SHADOWSNEAK`/`SWIFT` punishes careless Normal/Fighting-expectant plays — **strictly NO `BITTERMALICE` or `SHADOWBALL`**!)
6. **Meloetta** — *Prima Donna Ace* (Lv 15, Aria ↔ Pirouette via `RELICSONG` — **NOT catchable**, loyal theatrical muse holding back to Act One standards!)

---

## C.2 Concrete Damage-Calc Balance Proof (Badge 0 Pool vs Lv 15 Meloetta, H-Zorua & Chatot)

### Critical Math Discovery on `:GRAND_STAGE` + Meloetta Lv 15

Verified directly against `plugins/Prismfall Field Effects/004_FieldEffects_Engine.rb:167–186` and `102_Field_GrandStage.rb:72–79,104–144`:
- `RELICSONG` is **Normal-type** (`type_mods: ×1.3 / ×1.5 / ×1.5`) **AND Sound-flagged** (`damage_mods: ×1.3 / ×1.4 / ×1.5`).
- In `004_FieldEffects_Engine.rb`, those multiply together to **`×1.69` (Stage 1) / `×2.10` (Stage 2) / `×2.25` (Stage 3)** — plus `1.5×` STAB = **`×2.535 / ×3.15 / ×3.375` (effective 190–253 Base Power)** off **128 Base SpA**!
- **Result WITHOUT tuning (Stock `:GRAND_STAGE`, Lv 15 Meloetta IV=12 Hardy):** `RELICSONG` deals **113–141% OHKO** to Lv 15 Starters, **112–139% OHKO** to Kricketune, **200–247% OHKO** to Poochyena, and **80–102% OHKO** even to resisted Rock types (`Nacli`, `Dwebble`) — **14–16 of 19 Badge-0 Pokémon OHKO'd from full HP**, plus 20% Serene Grace Sleep + 10% Grand Stage Confusion!

### The Clean 2-Part Engineering Fix (Lore-Integrated + Zero Hack)

1. **1-Line Field Cap (`plugins/Prismfall Field Effects/102_Field_GrandStage.rb:76`):**
   `FieldEffects.move_matches?` (`004_FieldEffects_Engine.rb:20`) **already supports `:not_moves` natively!**
   ```ruby
   # Prevent Relic Song from double-stacking Normal x Sound into x2.10-2.25;
   # it STILL gets Normal x1.3/1.5/1.5, counts as a Sound move for applause + 10% confusion, and swaps Aria <-> Pirouette!
   { :flags => ["Sound"], :category => :damaging, :not_moves => [:RELICSONG], :mult => show, :message => "{2} rang through the opera house!" },
   ```
2. **10-Line `"Act One Matinee"` Stat Scale (`plugins/Prismfall Bosses/104_Boss_HardWardens.rb` or `109_Boss_DorianMatinee.rb`):**
   Uses Prismfall's **already-built** `Prismfall::Bosses.register_trainer_boss` (`006_Bosses_Start.rb:95–135`):
   - `:bars => 1` → `007_Bosses_UI.rb:19` draws **ZERO boss pips**; `006_Bosses_Start.rb:58` uses normal trainer databox!
   - `:status_immunity => false` → behaves 100% like a normal Gym Ace (can be paralyzed, confused, poisoned, stat-dropped)!
   - `:versions => [0, 100, 200]` → applies **ONLY to Gym 1**, NEVER to Festival v50 or Pageant Bout v90 or Postgame Tier 1!
   - `:stat_mults` → `0.80×` Standard (`~440 effective BST`, matching old Kecleon's 440 BST!), `0.85×` Hard, `0.78×` Casual — and because `Pokemon#calc_stats` (`002_Bosses_Registry.rb:183`) re-applies `stat_mults` on form change, **both Aria AND Pirouette stay cleanly scaled mid-battle!**
   - `:intro => ["Dorian: \"Easy now, my dear — this is Act One, not Opening Night!\"", "Meloetta softens her tempo to match a challenger's first stage!"]`

### Verified Lv 15 Damage Table (Badge-0 Player Pool, Lv 15, IV=15, EV=22, Neutral Nature)

#### Table 1 — **Standard Meloetta Lv 15** (`IV=0, EV=0, Hardy`, `0.80×` Matinee + Single-Boosted `RELICSONG` `×1.30 / ×1.50`)
*Effective Stats — Aria: `HP 44, Atk 22, Def 22, Spe 26, SpA 34, SpD 34` | Pirouette: `HP 44, Atk 34, Def 26, Spe 34, SpA 22, SpD 22`*

| Badge-0 Player Pokémon (Lv 15) | HP / Spe | Meloetta `RELICSONG` (S1 / S2) | Pirouette `QUICKATTACK` (S2) | Player Hit vs Aria (Normal/Psychic) | Player Hit vs Pirouette (Normal/Fighting) | Tactical Takeaway |
|---|---:|---|---|---|---|---|
| **Bulbasaur** | 41 / 21 | 27–32 (**66–78%**) / 31–37 (**76–90%**) | 19–24 (46–59%) | `Vine Whip`: 10–13 (23–30%) | `Vine Whip`: 9–12 (20–27%) | Survives Relic Song even at Stage 2; Leech Seed/Sleep Powder punishes! |
| **Charmander** | 39 / 27 | 31–36 (**79–92%**) / 36–42 (92–108%) | 22–27 (56–69%) | `Ember`: 7–9 (16–20%) | `Ember`: 10–13 (23–30%) | **Outspeeds Aria (27 > 26)**; Smokescreen/Ember chips cleanly! |
| **Squirtle** | 41 / 20 | 27–32 (**66–78%**) / 31–37 (**76–90%**) | 18–22 (44–54%) | `Bite` (2×): 18–22 (**41–50%**) | `Water Pulse`: 15–18 (34–41%) | Tanks Relic Song + **2HKOs Aria with `Bite`**! |
| **Poochyena** | 38 / 18 | 42–50 (111–132%) | 24–31 (63–82%) | `Bite` (STAB 2×): 30–36 (**68–82%**) | *(switches out on Pirouette)* | **OHKOs H-Zorua (133%)**, chunks Aria for **82%**, immune to `Confusion`! |
| **Nickit** (`EL_NICKIT`) | 40 / 22 | 31–36 (78–90%) | 27–33 (68–82%) | `Snarl` (STAB 2×): 20–24 (45–55%, **-1 SpA!**) | `Quick Attack`: 7–9 | Immune to `Confusion`; **`Snarl` neuters Relic Song by -33%!** |
| **Kricketune** (ev. Lv 10) | 51 / 27 | 31–36 (**61–71%**) / 36–42 (**71–82%**) | 19–24 (37–47%) | `Bug Bite` (STAB 2×): 38–48 (**86–109% OHKO!**) | *(resists Fighting)* | **Outspeeds Aria (27 > 26) & OHKOs Aria + steals Oran Berry!** |
| **Dwebble** | 43 / 24 | 19–23 (**44–53%**) / 22–27 (**51–63%**) | 6–9 (**14–21%**) | `Bug Bite` (STAB 2×): 32–38 (**73–86%**) | `Smack Down`: 6–7 | **Premier Badge-0 counter**: resists Normal, shreds Aria for 86%! |
| **Nacli** | 44 / 15 | 19–23 (**43–52%**) / 22–27 (**50–61%**) | 7–9 (**16–20%**) | `Rock Throw`: 12–15 (27–34%) | Walls `Quick Attack` (20%) | Resists Normal; cleanly stalls out Pirouette on Standard! |
| **Sandygast** (Marram 3%) | 44 / 12 | **0 (IMMUNE!)** | **0 (IMMUNE!)** | `Mega Drain` / `Astonish` (immune) | **IMMUNE to Normal + Fighting!** | Forces Meloetta onto unboosted `Confusion` (~40%)! |
| **Kecleon** (`EL_KECLEON`) | 46 / 19 | 16–20 (**35–43%**) / 19–24 (**41–52%**) | 15–19 (**33–41%**) | `Thief` (Protean 2×): 42–50 (**95–114% OHKO!**) | `Fury Swipes`: 20–24 (45–55%) | **Quest reward MVP**: tanks Relic Song cleanly & **OHKOs Aria**! |
| **Munchlax** | 68 / 9 | 20–27 (**29–40%**) / 24–31 (**35–46%**) | 22–27 (32–40%) | `Bite` (2×): 26–32 (**59–73%**) | `Tackle`: 12–15 (27–34%) | Facetanks 2–3 hits and cleanly **2HKOs Aria**! |
| **Fidough** | 39 / 27 | 31–36 (**79–92%**) | 15–19 (38–49%) | `Bite` (2×): 20–24 (**45–55%**) | Resists Fighting (`ROCKSMASH` on Hard) | **Outspeeds Aria (27 > 26)** & 2HKOs with `Bite`! |
| **Rookidee / Fletchling** | 39 / 25–26 | 39–46 (fragile vs Aria) | 24–31 (62–79%) | Switch in **after Pirouette!** | `Pluck` (STAB 2×): 24–30 (**55–68%** + steals Berry!) | **Premier Pirouette counter**: swap in once she dances, punish Fighting typing! |
| **Cutiefly** | 40 / 33 | 31–36 (78–90%) | 22–27 (55–68%) | `Struggle Bug` (-1 SpA!): 20–24 (45–55%) | `Fairy Wind` (STAB 2×): 22–27 (**50–61%**) | **Outspeeds Aria & threatens BOTH formes** (4× resists Fighting)! |

#### Table 2 — Supporting Trio Verification (Lv 10–13 vs Lv 15 Starter `HP 46, Def 25, SpD 25`)
- **Smeargle Lv 10** (`HP 31, Atk 11, Def 14, Spe 22, SpA 11`): `FAKEOUT` deals **4–6 (9–13%)**, `PAYDAY` deals **6–8 (13–17%)** — zero sweep threat; pure stage-setter raising applause by 1 stage before fainting in 2 hits!
- **Chatot Lv 12** (`HP 41, Def 17, SpA 28, Spe 28`): `ECHOEDVOICE` (Turn 1) deals **15–18 (33–39%)**, Hard `ROUND` deals **21–27 (46–59%)** — scary if ignored, blown up by Badge-0 `Nacli` `Rock Throw` (**88%**) or `Shinx` `Spark` (**122% OHKO**)!
- **Hisuian Zorua Lv 13** (`HP 33, Atk 22, Def 16, SpA 28, Spe 24`): `SHADOWSNEAK` deals **7–9 (15–20%)**, `SWIFT` deals **19–22 (41–48%)** — disguised as Meloetta via `ILLUSION`, shattered cleanly by any Dark `Bite`/`Thief` (**112–142% OHKO**) or 2 neutral STAB hits (**55% each**)!

#### Pure-PBS Fallback Note (If Zero `.rb` Edits Are Desired)
If Reuben prefers **zero `.rb` changes** (no `102_Field_GrandStage.rb` cap and no `Matinee` stat scale), then Standard Meloetta (`Lv 15, IV=0, EV=0, Impish`) **cannot safely carry `RELICSONG`** on stock `:GRAND_STAGE` (14/19 OHKO!) and would have to run `ECHOEDVOICE,QUICKATTACK,CONFUSION,SING` (2/19 OHKO S1, 6/19 S2 — playable, but loses the Aria ↔ Pirouette dance transformation!). **Therefore the 2-part fix (1-line `:not_moves => [:RELICSONG]` + 10-line `:DORIAN_MELOETTA_MATINEE`) is STRONGLY RECOMMENDED** because it preserves the iconic **Aria ↔ Pirouette `RELICSONG` transformation** at Cap 15 while hitting the exact 45–73% Standard / 33–62% Hard win-rate band!

---

## C.3 Drop-In Validated PBS Blocks (`pbs/trainers.txt` Lines 10–114)

Verified field-by-field against `tools/validate_trainers.py` and `/home/antigravity/pf_engine_run/base/PBS/` (`pokemon.txt`, `pokemon_forms.txt`, `moves.txt`, `abilities.txt`, `items.txt` + `pbs/items_fields.txt`):
- Exact Essentials v21.1 syntax for Hisuian Zorua: `Pokemon = ZORUA,13` + `Form = 1` (verified `ZORUA_1` in `PBS/pokemon_forms.txt`: Types `NORMAL,GHOST`, Ability `ILLUSION`).
- Exact Essentials v21.1 syntax for Meloetta: `Pokemon = MELOETTA,15` + `Moves = RELICSONG,...` (starts in Aria Forme `Form = 0`; `RELICSONG` transforms to Pirouette `Form = 1` automatically in battle).
- **Zero errors, zero warnings on Standard and Casual** (once the `BALANCE.md` allowlist rows in §C.5 are added for Smeargle's Sketched moves!).

```ini
# Gym 1 - Dorian - field :GRAND_STAGE - cap 15
#-------------------------------
[LEADER_DORIAN,Dorian]
Items = POTION
LoseText = Bravo! Bravissimo! The audience is yours tonight!
Pokemon = SMEARGLE,10
    Moves = FAKEOUT,PAYDAY,ENCORE,BABYDOLLEYES
    Ability = OWNTEMPO
    Item = ORANBERRY
    Nature = JOLLY
    IV = 12
Pokemon = SPINDA,10
    Moves = TEETERDANCE,COPYCAT,TACKLE,DEFENSECURL
    Ability = OWNTEMPO
    Item = ORANBERRY
    Nature = ADAMANT
    IV = 12
Pokemon = JIGGLYPUFF,11
    Moves = SING,DISARMINGVOICE,POUND,DEFENSECURL
    Ability = CUTECHARM
    Item = ORANBERRY
    Nature = MODEST
    IV = 12
Pokemon = CHATOT,12
    Moves = ECHOEDVOICE,PECK,ENCORE,GROWL
    Ability = TANGLEDFEET
    Item = ORANBERRY
    Nature = TIMID
    IV = 12
Pokemon = ZORUA,13
    Form = 1
    Moves = SHADOWSNEAK,SWIFT,TORMENT,LEER
    Ability = ILLUSION
    Item = ORANBERRY
    Nature = TIMID
    IV = 12
Pokemon = MELOETTA,15
    Moves = RELICSONG,QUICKATTACK,CONFUSION,SING
    Ability = SERENEGRACE
    Item = ORANBERRY
    Nature = HARDY
    IV = 0
    EV = 0
#-------------------------------
[LEADER_DORIAN,Dorian,100]
Items = SUPERPOTION
LoseText = Bravo! Bravissimo! The audience is yours tonight!
Pokemon = SMEARGLE,10
    Moves = FAKEOUT,PAYDAY,ENCORE,PARTINGSHOT
    Ability = OWNTEMPO
    Item = FOCUSSASH
    Nature = JOLLY
    IV = 20
    EV = 60,0,4,60,0,0
Pokemon = SPINDA,11
    Moves = TEETERDANCE,PSYBEAM,COPYCAT,ENCORE
    Ability = OWNTEMPO
    Item = SITRUSBERRY
    Nature = TIMID
    IV = 20
    EV = 4,0,0,66,66,0
Pokemon = JIGGLYPUFF,11
    Moves = SING,DISARMINGVOICE,ROUND,DEFENSECURL
    Ability = COMPETITIVE
    Item = SITRUSBERRY
    Nature = MODEST
    IV = 20
    EV = 66,0,4,0,66,0
Pokemon = CHATOT,12
    Moves = ROUND,ECHOEDVOICE,PECK,ENCORE
    Ability = TANGLEDFEET
    Item = ORANBERRY
    Nature = TIMID
    IV = 20
    EV = 4,0,0,72,72,0
Pokemon = ZORUA,13
    Form = 1
    Moves = SHADOWSNEAK,SWIFT,HONECLAWS,SPITE
    Ability = ILLUSION
    Item = SYNTHETICSEED
    Nature = NAIVE
    IV = 20
    EV = 0,40,0,78,40,0
Pokemon = MELOETTA,15
    Moves = RELICSONG,QUICKATTACK,CONFUSION,ROCKSMASH
    Ability = SERENEGRACE
    Item = ORANBERRY
    Nature = HARDY
    IV = 12
    EV = 0
#-------------------------------
[LEADER_DORIAN,Dorian,200]
LoseText = Bravo! Bravissimo! The audience is yours tonight!
Pokemon = SMEARGLE,8
    Moves = PAYDAY,BABYDOLLEYES,TACKLE
    Ability = OWNTEMPO
    Item = ORANBERRY
    Nature = JOLLY
    IV = 4
    EV = 0
Pokemon = CHATOT,10
    Moves = ECHOEDVOICE,PECK,GROWL
    Ability = KEENEYE
    Item = ORANBERRY
    Nature = HARDY
    IV = 4
    EV = 0
Pokemon = ZORUA,11
    Form = 1
    Moves = SCRATCH,SPITE,TORMENT,LEER
    Ability = ILLUSION
    Item = ORANBERRY
    Nature = HARDY
    IV = 4
    EV = 0
Pokemon = MELOETTA,13
    Moves = RELICSONG,QUICKATTACK,CONFUSION,CONFIDE
    Ability = SERENEGRACE
    Item = ORANBERRY
    Nature = IMPISH
    IV = 0
    EV = 0
```

*(Note on Hard `SPINDA,11`: `PSYBEAM` is a L14 level-up move, matching the existing Hard Spinda in `pbs/trainers.txt:64` and `BALANCE.md:29`'s intentional Hard early-move policy. Swap to `FAKETEARS` if strict 0-warning even on Hard is desired. Note on `ZORUA,1`: placed in Slot 5 immediately before Slot 6 `MELOETTA` so `ILLUSION` consistently disguises Hisuian Zorua as Meloetta — a dramatic mid-fight "Phantom Understudy" fakeout!)*

---

## C.4 Matching `tools/trainer_gen/gen.py` Update & `109_Boss_DorianMatinee.rb` Snippet

Because `pbs/trainers.txt` is generated from `tools/trainer_gen/gen.py` (lines 175–215), Claude MUST update `gen.py` (adding optional per-mon `iv=` / `ev_override=` override support in `render()` so Meloetta emits `IV = 0` / `EV = 0` on Standard & Casual and `IV = 12` / `EV = 0` on Hard):

```python
warden(1, "LEADER_DORIAN", "Dorian", 15, "GRAND_STAGE", "Bravo! Bravissimo! The audience is yours tonight!", [
    # 1. Set painter / curtain raiser (Fake Out + Pay Day showpieces build applause without hitting hard).
    P("SMEARGLE", 10, "OWNTEMPO", "ORANBERRY", "JOLLY", "FAKEOUT,PAYDAY,ENCORE,BABYDOLLEYES", "PD",
      casual={"moves": "PAYDAY,BABYDOLLEYES,TACKLE"},
      hard={"item": "FOCUSSASH", "moves": "FAKEOUT,PAYDAY,ENCORE,PARTINGSHOT"}),
    # 2. Slapstick dancer (Teeter Dance raises applause + Speed; Copycat improvs).
    P("SPINDA", 10, "OWNTEMPO", "ORANBERRY", "ADAMANT", "TEETERDANCE,COPYCAT,TACKLE,DEFENSECURL", "S",
      only="nocasual", hard={"lv": 11, "nat": "TIMID", "item": "SITRUSBERRY", "moves": "TEETERDANCE,PSYBEAM,COPYCAT,ENCORE"}),
    # 3. Chorus soprano (ties into Saltmere Full House Sing rule; Hard Competitive punishes stat drops).
    P("JIGGLYPUFF", 11, "CUTECHARM", "ORANBERRY", "MODEST", "SING,DISARMINGVOICE,POUND,DEFENSECURL", "BS",
      only="nocasual", hard={"ab": "COMPETITIVE", "item": "SITRUSBERRY", "moves": "SING,DISARMINGVOICE,ROUND,DEFENSECURL"}),
    # 4. Diva songbird (NO Chatter/Boomburst at Lv 12; Echoed Voice/Round + Encore).
    P("CHATOT", 12, "TANGLEDFEET", "ORANBERRY", "TIMID", "ECHOEDVOICE,PECK,ENCORE,GROWL", "S",
      casual={"ab": "KEENEYE", "nat": "HARDY", "moves": "ECHOEDVOICE,PECK,GROWL"},
      hard={"moves": "ROUND,ECHOEDVOICE,PECK,ENCORE"}),
    # 5. Phantom understudy (Hisuian Zorua Form 1; Illusion disguises it as Meloetta in Slot 6!).
    P("ZORUA", 13, "ILLUSION", "ORANBERRY", "TIMID", "SHADOWSNEAK,SWIFT,TORMENT,LEER", "MX", form=1,
      casual={"nat": "HARDY", "moves": "SCRATCH,SPITE,TORMENT,LEER"},
      hard={"item": "SYNTHETICSEED", "nat": "NAIVE", "moves": "SHADOWSNEAK,SWIFT,HONECLAWS,SPITE"}),
    # 6. Prima Donna ace (Meloetta Aria <-> Pirouette via Relic Song; scaled to Act One via :DORIAN_MELOETTA_MATINEE).
    P("MELOETTA", 15, "SERENEGRACE", "ORANBERRY", "HARDY", "RELICSONG,QUICKATTACK,CONFUSION,SING", "MX",
      iv_override=0, ev_override="0",
      casual={"nat": "IMPISH", "moves": "RELICSONG,QUICKATTACK,CONFUSION,CONFIDE", "iv_override": 0, "ev_override": "0"},
      hard={"moves": "RELICSONG,QUICKATTACK,CONFUSION,ROCKSMASH", "iv_override": 12, "ev_override": "0"}),
])
```

And the 15-line companion file `plugins/Prismfall Bosses/109_Boss_DorianMatinee.rb`:
```ruby
# Gym 1 Dorian's Meloetta holds back to Act One / Badge-1 standards (1 bar = no boss pips, no status immunity).
# Full 600-BST power is unleashed in Postgame Tier 1 ("Crownhaven Encore") and Pageant Bout v90!
Prismfall::Bosses.register(:DORIAN_MELOETTA_MATINEE, {
  :bars            => 1,
  :status_immunity => false,
  :ebdx            => { :databox => false },
  :stat_mults      => {
    :CASUAL   => { :HP => 0.78, :ATTACK => 0.78, :DEFENSE => 0.78, :SPECIAL_ATTACK => 0.78, :SPECIAL_DEFENSE => 0.78, :SPEED => 0.78 },
    :STANDARD => { :HP => 0.80, :ATTACK => 0.80, :DEFENSE => 0.80, :SPECIAL_ATTACK => 0.80, :SPECIAL_DEFENSE => 0.80, :SPEED => 0.80 },
    :HARD     => { :HP => 0.85, :ATTACK => 0.85, :DEFENSE => 0.85, :SPECIAL_ATTACK => 0.85, :SPECIAL_DEFENSE => 0.85, :SPEED => 0.85 }
  },
  :intro => ["Dorian: \"Easy now, my dear — this is Act One, not Opening Night!\"",
             "Meloetta softens her tempo to match a challenger's first stage!"]
})

Prismfall::Bosses.register_trainer_boss(:DORIAN_GYM1_MELOETTA, {
  :trainer_type => :LEADER_DORIAN, :name => "Dorian",
  :versions     => [0, 100, 200], # Gym 1 only — NEVER Festival v50 or Pageant Bout v90!
  :species      => :MELOETTA,
  :boss         => :DORIAN_MELOETTA_MATINEE
})
```

---

## C.5 `design/BALANCE.md` Allowlist & `tools/validate_trainers.py` Notes

Because `SMEARGLE` only lists `SKETCH` in `PBS/pokemon.txt`, `validate_trainers.py` will error on Sketched moves unless Claude adds **either** (recommended: **both**):
1. **Allowlist rows in `design/BALANCE.md` under `## Intentional non-learnable moves (validator allowlist)`:**
   ```markdown
   | LEADER_DORIAN,Dorian,* | SMEARGLE | FAKEOUT | Sketched move (Smeargle). |
   | LEADER_DORIAN,Dorian,* | SMEARGLE | PAYDAY | Sketched move (Smeargle). |
   | LEADER_DORIAN,Dorian,* | SMEARGLE | ENCORE | Sketched move (Smeargle). |
   | LEADER_DORIAN,Dorian,* | SMEARGLE | BABYDOLLEYES | Sketched move (Smeargle). |
   | LEADER_DORIAN,Dorian,100 | SMEARGLE | PARTINGSHOT | Sketched move (Smeargle, Hard). |
   | LEADER_DORIAN,Dorian,200 | SMEARGLE | TACKLE | Sketched move (Smeargle, Casual). |
   ```
2. **Optional 2-line native Sketch rule in `tools/validate_trainers.py:505`:**
   ```python
   # Smeargle can legally learn any move via Sketch (except Chatter / Struggle / CannotSketch moves).
   if mon.species == "SMEARGLE" and m not in ("CHATTER", "STRUGGLE"):
       continue
   ```
   *(If adding the native rule, omit the Smeargle allowlist rows from `BALANCE.md` so `validate_trainers.py:747` doesn't warn about unused allowlist entries!)*

---

## C.6 Story, Dialogue & Lore Hooks for Claude to Update

**Lore Rationale (Why Dorian Has a Mythical Meloetta in Gym 1 — and Why She Isn't Catchable or Broken):**
- Saltmere is *"the only city in Velmora where nothing is a miracle — so we built our own, every night at eight"* (`story/20_SCRIPT_CH0-2.md:886`). Years ago, a wandering **Meloetta** — drawn to the Pell Playhouse's songs — quietly joined Dorian's company as his Prima Donna muse. Neither the Accord nor Queen Maelis knows what she truly is; Dorian calls her his *"first violinist who refuses a salary."*
- Because she is a seasoned stage performer testing a brand-new Badge-0 challenger, she **holds back to Matinee / Act One tempo** (`0.80×`), giving the challenger a thrilling taste of song-and-dance form-shifting (`Aria ↔ Pirouette`) without flattening them — and she is Dorian's partner (trainer battle = uncatchable), saving her **full 600-BST Opening Night battle & capture** as the triumphant opening quest of **Postgame Tier 1 (`PG_MELOETTA`: Crownhaven Encore)**!

### Exact Files Mentioning Dorian's Old Kecleon Ace to Update

| File & Line | Current Text | Recommended Claude Update |
|---|---|---|
| `story/20_SCRIPT_CH0-2.md:1070` | `(Mid-battle, when his ace enters:) [portrait: DORIAN, smug] Costume change!` | Update to: `[portrait: DORIAN, happy] Places, everyone — our Prima Donna! Aria, then Pirouette — keep up, darling!` (And optionally add a brief beat when Hisuian Zorua's Illusion breaks: `"Ah! You spotted the understudy!"`) |
| `story/03_CAST.md:156` | `- **Ace:** **Kecleon** (the quick-change artist; Color Change is a costume change); also **Ambipom**, **Chatot** (the voice), **Furfrou**, and later **Exploud**.` | Update to: `- **Ace:** **Meloetta** (the Prima Donna — Aria the singer, Pirouette the dancer; holds back to Act One tempo in Gym 1, full power in Postgame Encore); also **Smeargle** (set painter), **Chatot** (diva), **Hisuian Zorua** (phantom understudy), **Spinda**, **Jigglypuff**, and later **Mega Lopunny** / **Exploud**.` |
| `story/04_ACT_I.md:91` | `His ace is **Kecleon**, which changes "costume" with each type.` | Update to: `His ace is **Meloetta**, his Playhouse's wandering musical muse — singing in Aria Forme and leaping into Pirouette Forme mid-curtain-call (holding back to Act One standards for a first-badge challenger).` |
| `plugins/Prismfall Trials/130_EventMons_Early.rb:45` & `design/EVENT_POKEMON.md:15` | `"A search-puzzle find before Gym 1: Protean (every move gets STAB), Dorian's own ace species."` | Keep `EL_KECLEON` intact (it is a fantastic Badge-0 Dark/Thief counter to Dorian's Meloetta & Hisuian Zorua!), and simply change `"Dorian's own ace species"` → `"the Lantern Theatre's quick-change prop-master"`! |
| `design/BALANCE.md:139` & `design/TRAINER_FIELD_PLAYBOOK.md:77–84` | Old 5-mon `Aipom, Minccino, Spinda, Jigglypuff, Kecleon` table row & notes | Update to new 6-mon troupe (`Smeargle, Spinda, Jigglypuff, Chatot, Hisuian Zorua, Meloetta`) + document the `:RELICSONG` non-double-stack and `:DORIAN_MELOETTA_MATINEE` rule + re-run `tools/harness/run_winrates.rb PRISM_FIGHTS=G1` to record updated Sparse/Good/Full House win rates! |
| `tools/trainer_gen/gen.py:1083–1091` & `pbs/trainers.txt:14744–14820` (`LEADER_DORIAN,Dorian,90/190/290`) | Pageant Bout exhibition currently uses `Lopunny (Mega), Exploud, Kecleon "Encore"` | Recommend upgrading Slot 3 (`Kecleon "Encore"`) to **Lv 90 `MELOETTA`** (full 600-BST, `RELICSONG,PSYCHIC,CLOSECOMBAT,HYPERVOICE` @ `THROATSPRAY` or `LIFEORB`) so Dorian's Festival Pageant Bout pays off his Gym 1 Prima Donna at full Opening Night glory! |

---

## Verification Checklist for Claude After Execution
1. Run `python3 tools/install_ebdx_animated_sprites.py --engine /home/antigravity/pf_engine_run/base --audit` → verify live Prismfall gaps drop from **248 Front / 264 Back** to near-zero (especially `ZORUA_1`, `OGERPON`, `PECHARUNT`, `OKIDOGI`, `MUNKIDORI`, `FEZANDIPITI`, `GHOLDENGO`, `ANNIHILAPE`, Primal Kyogre/Groudon, and all 11 missing Trainer Megas).
2. Run `python3 -I tools/validate_trainers.py --ref /home/antigravity/pf_engine_run/base/PBS --strict` (or standard mode) → verify **0 errors** and **0 Standard/Casual warnings** on `[LEADER_DORIAN,Dorian]` / `100` / `200`.
3. Run `PRISM_FIGHTS=G1 PRISM_MODES=CASUAL,STANDARD,HARD ruby tools/harness/run_winrates.rb` → verify Standard Sparse/Good/Full House sits in **~40–75%**, Hard Prepared in **~30–60%**, Casual in **~95–100%** (adjust `:DORIAN_MELOETTA_MATINEE` multiplier `0.78–0.85` by ±0.03 if needed).
4. Run `ruby -c` on all edited/added Ruby files (`004_Bosses_Battle.rb`, `102_Field_GrandStage.rb`, `109_Boss_DorianMatinee.rb`, `109/110` Loyal Three/Pecharunt bosses) and verify `Prismfall.story_legendary_locked?` blocks Poké Balls on all Legendaries/Mythicals/UBs/Paradoxes before `S160 POSTGAME` and unlocks cleanly once `S160 POSTGAME = true`.
