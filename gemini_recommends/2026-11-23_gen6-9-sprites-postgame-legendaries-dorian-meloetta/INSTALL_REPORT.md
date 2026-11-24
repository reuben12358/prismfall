# Pokémon Prismfall — Gen 6–9, Regional Variants, Primals & Mega Evolutions Animated B2W2 Sprite Pipeline Report

**Date:** 2026-11-24  
**Pipeline Script:** [install_ebdx_animated_sprites.py](file:///home/antigravity/reuben12358/prismfall/gemini_recommends/2026-11-23_gen6-9-sprites-postgame-legendaries-dorian-meloetta/install_ebdx_animated_sprites.py)  
**Credits File:** [SPRITE_CREDITS.md](file:///home/antigravity/reuben12358/prismfall/gemini_recommends/2026-11-23_gen6-9-sprites-postgame-legendaries-dorian-meloetta/SPRITE_CREDITS.md)  
**Staged Verified Pack:** `/home/antigravity/pf_engine_run/ebdx_gen6_9_animated_pack/` (with `manifest.json`)  
**Engine Copy Smoke-Test:** `/home/antigravity/pf_engine_run/sprite_test_out/engine_copy/`  
**Visual Proof Contact Sheet:** [72_gen6_9_mega_animated_sprites.png](file:///home/antigravity/.gemini/jetski/brain/2484663edd3ff4720df7e62906cca222/previews/72_gen6_9_mega_animated_sprites.png)  
**Visual Proof Live Animated GIF:** [72_gen6_9_mega_animated_sprites.gif](file:///home/antigravity/.gemini/jetski/brain/2484663edd3ff4720df7e62906cca222/previews/72_gen6_9_mega_animated_sprites.gif)

---

## 1. Executive Verdict — 100.0% Live Prismfall Gaps Closed (Zero 3D Renders)

Using strictly genuine **2D Gen 5 B2W2 pixel art** (ZERO 3D `ani/` model renders), the repeatable importer closed **100.0% of all Prismfall live gaps** across Front, Back, FrontShiny, and BackShiny:

| Roster Slice | Total Species/Forms | Before Front (Gap) | **After Front (Gap)** | Before Back (Gap) | **After Back (Gap)** | Before Shiny F/B | **After Shiny F/B** |
|---|---:|---:|---:|---:|---:|---:|---:|
| `pbs/trainers.txt` + `trainers_trials.txt` | 365 | 282 (-83) | **365 (-0)** | 276 (-89) | **365 (-0)** | 262 / 260 | **365 / 365** |
| Live Trainer Combat Megas | 23 | 12 (-11) | **23 (-0)** | 8 (-15) | **23 (-0)** | 3 / 3 | **23 / 23** |
| `pbs/encounters.txt` + `encounters_badgetiers.txt` | 713 | 491 (-222) | **713 (-0)** | 480 (-233) | **713 (-0)** | 464 / 462 | **713 / 713** |
| **Combined Live PBS Roster** | **795** | **548 (-247)** | **795 (-0)** | **532 (-263)** | **795 (-0)** | **510 / 508** | **795 / 795** |
| **Live PBS + Dorian Gym 1 `ZORUA,1`** | **796** | **548 (-248)** | **796 (-0)** | **532 (-264)** | **796 (-0)** | **510 / 508** | **796 / 796** |
| **Live + Spotlight Story/Postgame Bosses** | **819** | **550 (-269)** | **819 (-0)** | **534 (-285)** | **819 (-0)** | **512 / 510** | **819 / 819** |

---

## 2. Full Category Breakdown (Before → After Staged `prismfall-plus-forms` Pack)

| Category | Total in PBS | Before Front → **After Front** | Before Back → **After Back** | Before FrontShiny → **After** | Before BackShiny → **After** | Live Prismfall Remaining |
|---|---:|---:|---:|---:|---:|---:|
| **Gen 1–5 Base (`#001–#649`)** | 649 | 649 → **649 (100%)** | 649 → **649 (100%)** | 649 → **649 (100%)** | 649 → **649 (100%)** | **0** |
| **Gen 6 Base (`#650–#721`)** | 72 | 55 → **69** *(51/51 live)* | 39 → **65** *(51/51 live)* | 12 → **54** *(51/51 live)* | 9 → **53** *(51/51 live)* | **0** |
| **Gen 7 Base (`#722–#809`)** | 88 | 0 → **52** *(52/52 live)* | 0 → **52** *(52/52 live)* | 0 → **52** *(52/52 live)* | 0 → **52** *(52/52 live)* | **0** |
| **Gen 8 Base (`#810–#905`)** | 96 | 0 → **70** *(70/70 live)* | 0 → **70** *(70/70 live)* | 0 → **70** *(70/70 live)* | 0 → **70** *(70/70 live)* | **0** |
| **Gen 9 Base (`#906–#1025`)** | 120 | 0 → **89** *(89/89 live)* | 0 → **89** *(89/89 live)* | 0 → **89** *(89/89 live)* | 0 → **89** *(89/89 live)* | **0** |
| **Alolan Forms** | 18 | 0 → **18 (100%)** | 0 → **18 (100%)** | 0 → **18 (100%)** | 0 → **18 (100%)** | **0** |
| **Galarian Forms** | 20 | 0 → **20 (100%)** | 0 → **20 (100%)** | 0 → **20 (100%)** | 0 → **20 (100%)** | **0** |
| **Hisuian Forms** | 16 | 0 → **16 (100%)** | 0 → **16 (100%)** | 0 → **16 (100%)** | 0 → **16 (100%)** | **0** |
| **Paldean Forms** | 4 | 0 → **4 (100%)** | 0 → **4 (100%)** | 0 → **4 (100%)** | 0 → **4 (100%)** | **0** |
| **Primal Reversions (`KYOGRE_1`, `GROUDON_1`)** | 2 | 0 → **2 (100%)** | 0 → **2 (100%)** | 0 → **2 (100%)** | 0 → **2 (100%)** | **0** |
| **Mega Evolutions (All 48)** | 48 | 24 → **48 (100%)** | 14 → **48 (100%)** | 4 → **48 (100%)** | 4 → **48 (100%)** | **0** |
| **Other Alt Forms** *(live + Ogerpon/Terapagos/Urshifu/Zygarde)* | 287 | 90 → **100** *(15/15 live)* | 87 → **97** *(15/15 live)* | 87 → **98** *(15/15 live)* | 87 → **98** *(15/15 live)* | **0** |

*(Note: Running `--scope all` can also fill **1,025/1,025** base species across the full National Dex — only 12 visually-identical internal form slots like Team Star Starmobiles `REVAVROOM_1..5`, Own Tempo `ROCKRUFF_2`, and Authentic/Masterpiece teacups have no separate animated files.)*

---

## 3. Spotlight Cast & All 11 Missing Live Trainer Megas — Verification Table

Every spotlight Pokémon requested for Gym 1, Chapters 10–19, Postgame Tiers 1–3, and Warden/Champion Mega Aces is verified **100% animated** across Front, Back, FrontShiny, and BackShiny:

| Species / Form | EBDX Filename | Role in Prismfall | Front Strip | Back Strip | FrontShiny | BackShiny | Source |
|---|---|---|---|---|---|---|---|
| **Hisuian Zorua (`ZORUA,1`)** | `570_1.png` | **Gym 1 Dorian (Part C)** | `63px / 108f` | `63px / 24f` | `63px / 108f` | `63px / 24f` | EBDX Renovation 4.0 |
| **Hisuian Zoroark (`ZOROARK,1`)** | `571_1.png` | Dorian Encore / Evo | `77px / 24f` | `79px / 24f` | `77px / 24f` | `79px / 24f` | EBDX Renovation 4.0 |
| **Meloetta Aria (`MELOETTA,0`)** | `648.png` | **Gym 1 Dorian Ace** | `63px / 150f` | `58px / 149f` | `63px / 150f` | `58px / 149f` | Stock B2W2 (preserved) |
| **Meloetta Pirouette (`MELOETTA,1`)** | `648_1.png` | **Relic Song Form** | `76px / 76f` | `75px / 76f` | `76px / 76f` | `75px / 76f` | Stock B2W2 (preserved) |
| **Ogerpon Teal (`OGERPON,0`)** | `1017.png` | Ch10 / Act V / Postgame | `76px / 63f` | `69px / 20f` | `76px / 63f` | `69px / 20f` | EBDX Renovation 4.0 |
| **Ogerpon Wellspring (`OGERPON,1`)** | `1017_1.png` | Postgame Mask 2 | `76px / 63f` | `69px / 20f` | `76px / 63f` | `69px / 20f` | EBDX Renovation 4.0 |
| **Ogerpon Hearthflame (`OGERPON,2`)** | `1017_2.png` | Postgame Mask 3 | `77px / 63f` | `69px / 20f` | `77px / 63f` | `69px / 20f` | EBDX Renovation 4.0 |
| **Ogerpon Cornerstone (`OGERPON,3`)** | `1017_3.png` | Postgame Mask 4 | `76px / 63f` | `69px / 20f` | `76px / 63f` | `69px / 20f` | EBDX Renovation 4.0 |
| **Okidogi (`OKIDOGI,0`)** | `1014.png` | Ch10 / PG Loyal Three | `84px / 123f` | `84px / 8f` | `84px / 123f` | `84px / 8f` | EBDX Renovation 4.0 |
| **Munkidori (`MUNKIDORI,0`)** | `1015.png` | Ch10 / PG Loyal Three | `64px / 26f` | `63px / 8f` | `64px / 26f` | `63px / 8f` | EBDX Renovation 4.0 |
| **Fezandipiti (`FEZANDIPITI,0`)** | `1016.png` | Ch10 / PG Loyal Three | `71px / 132f` | `77px / 8f` | `71px / 132f` | `77px / 8f` | EBDX Renovation 4.0 |
| **Pecharunt (`PECHARUNT,0`)** | `1025.png` | Ch18 / PG Mythical | `77px / 137f` | `61px / 8f` | `77px / 137f` | `61px / 8f` | EBDX Renovation 4.0 |
| **Gholdengo (`GHOLDENGO,0`)** | `1000.png` | Gen 9 Live Roster | `119px / 93f` | `76px / 6f` | `119px / 93f` | `76px / 6f` | EBDX Renov4 / Ghasty / Showdown |
| **Annihilape (`ANNIHILAPE,0`)** | `979.png` | Gen 9 Live Roster | `74px / 92f` | `69px / 10f` | `74px / 92f` | `69px / 10f` | EBDX Renov4 / Ghasty001 |
| **Primal Kyogre (`KYOGRE,1`)** | `382_1.png` | Ch11 / Ch19 / PG Boss | `121px / 85f` | `100px / 24f` | `121px / 85f` | `100px / 24f` | EBDX Renov4 / Showdown `gen5ani` |
| **Primal Groudon (`GROUDON,1`)** | `383_1.png` | Ch14 / PG Boss | `96px / 50f` | `88px / 50f` | `96px / 50f` | `88px / 50f` | EBDX Renov4 / Showdown `gen5ani` |
| **Mega Aerodactyl (`AERODACTYL,1`)** | `142_1.png` | Missing Live Trainer Mega #1 | `118px / 60f` | `127px / 60f` | `118px / 60f` | `127px / 60f` | Aronousqui (Renov4) |
| **Mega Camerupt (`CAMERUPT,1`)** | `323_1.png` | Missing Live Trainer Mega #2 | `129px / 72f` | `126px / 72f` | `129px / 72f` | `126px / 72f` | Aronousqui (Renov4) |
| **Mega Gallade (`GALLADE,1`)** | `475_1.png` | Missing Live Trainer Mega #3 | `105px / 78f` | `98px / 78f` | `105px / 78f` | `98px / 78f` | Aronousqui (Renov4) |
| **Mega Houndoom (`HOUNDOOM,1`)** | `229_1.png` | Missing Live Trainer Mega #4 | `89px / 72f` | `87px / 72f` | `89px / 72f` | `87px / 72f` | Aronousqui (Renov4) |
| **Mega Latias (`LATIAS,1`)** | `380_1.png` | Missing Live Trainer Mega #5 | `127px / 73f` | `135px / 73f` | `127px / 73f` | `135px / 73f` | Aronousqui (Renov4) |
| **Mega Lopunny (`LOPUNNY,1`)** | `428_1.png` | Missing Live Trainer Mega #6 | `92px / 69f` | `100px / 69f` | `92px / 69f` | `100px / 69f` | Aronousqui (Renov4) |
| **Mega Manectric (`MANECTRIC,1`)** | `310_1.png` | Missing Live Trainer Mega #7 | `108px / 97f` | `102px / 97f` | `108px / 97f` | `102px / 97f` | mangalos810 (Renov4) |
| **Mega Metagross (`METAGROSS,1`)** | `376_1.png` | Missing Live Trainer Mega #8 | `115px / 71f` | `122px / 71f` | `115px / 71f` | `122px / 71f` | Aronousqui (Renov4) |
| **Mega Salamence (`SALAMENCE,1`)** | `373_1.png` | Missing Live Trainer Mega #9 | `126px / 67f` | `130px / 67f` | `126px / 67f` | `130px / 67f` | Aronousqui (Renov4) |
| **Mega Sharpedo (`SHARPEDO,1`)** | `319_1.png` | Missing Live Trainer Mega #10 | `107px / 76f` | `109px / 76f` | `107px / 76f` | `109px / 76f` | Aronousqui (Renov4) |
| **Mega Slowbro (`SLOWBRO,2`)** | `080_2.png` | Missing Live Trainer Mega #11 | `94px / 79f` | `97px / 79f` | `94px / 79f` | `97px / 79f` | Aronousqui (Renov4) |
| **Mega Banette/Gengar/Gyarados/Sableye** | `354_1`,`094_1`,`130_1`,`302_1` | 4 Back-Only Trainer Megas | Stock preserved | `99/96/145/79px` (`48–72f`) | `48–72f` | `48–72f` | Aronousqui (Renov4) |
| **Mega Altaria (`ALTARIA,1`)** | `334_1.png` | All-48 Megas (Ghasty GIF!) | `112px / 61f` | `141px / 36f` | `112px / 61f` | `141px / 36f` | **Ghasty001 GIF** + Renov4 |

---

## 4. Pack Sizes by Deployment Tier

We measured exact on-disk sizes of the tight union-bbox normalized RGBA PNG strips (stock `#001–#649` format parity):

| Deployment Tier (`--scope`) | Species/Forms Covered | Newly Installed Strips | Total Disk Size | Notes |
|---|---|---:|---:|---|
| `--scope live` | **796** (`795` live PBS + Dorian `ZORUA,1`) | **1,086** (`248 F / 264 B / 286 FS / 288 BS`) | **25.57 MB** | Minimum footprint closing 100% of current live PBS gaps |
| `--scope prismfall` | **819** (796 live + 23 Story/Postgame Bosses) | **1,170** (`269 F / 285 B / 307 FS / 309 BS`) | **27.95 MB** | Adds Ogerpon 0–3, Loyal Three, Pecharunt, Primals, Hisuian Zoroark, Type: Null, Kubfu/Urshifu, Regieleki/Drago, Terapagos |
| **`--scope prismfall-plus-forms`** *(staged now!)* | **881** (819 + **ALL 48 Megas** + **ALL 58 Regionals** + 4 Female) | **1,402** (`320 F / 342 B / 369 FS / 371 BS`) | **40.61 MB** | **Recommended for engine bundle** — zero chance a player Mega-Evolves or evolves a Regional form into a static sprite! |

**Recommendation for Repo Hygiene:** Do NOT commit `40.61 MB` of binary PNGs directly into git history unless desired; instead drop `install_ebdx_animated_sprites.py` into `tools/` and run it during engine assembly (`assemble_game.sh`) or stage `/home/antigravity/pf_engine_run/ebdx_gen6_9_animated_pack/` directly into `/home/antigravity/pf_engine_run/base/Graphics/EBDX/Battlers/`!

---

## 5. Verification & Live Tests Executed

1. **Form-Index Parity Cross-Check (`PBS/pokemon_forms.txt`):** Verified **394 / 395** alternate forms between Prismfall `base/PBS/pokemon_forms.txt` and ChromeValiant's `PBS/pokemon_forms*.txt` match **100% identically** (`0` form-number mismatches — `SLOWBRO_2 = Mega Slowbro`, `DARUMAKA_2 = Galarian`, `MEOWTH_2 = Galarian`, `ZORUA_1 = Hisuian`, `OGERPON_1..3 = Masks`, etc.; the 1 non-matching name `BASCULEGION_1` Female is already mapped accurately).
2. **Staged Pack Strip Verification (`--verify-strips`):**
   - Checked: **`1,402 / 1,402` PASSED (`0` failed)** across `Front` (320), `Back` (342), `FrontShiny` (369), `BackShiny` (371) + `Female/215_1.png` (4).
   - Every single strip confirmed: valid `RGBA` PNG, `W > H`, `W % H == 0`, `frames ∈ [6, 180]` (median `54f`), non-identical frames, frame size `S ∈ [30, 182]` px (median `74px`, matching stock `#001–#649` median `66px` and max `154px`!), `0` semi-transparent halo pixels (`alpha ∈ {0, 255}`), `unique_rgb <= 180` (strictly 2D pixel art!).
   - Union-bbox square normalization guarantees **ZERO frame drift** and **100% preserved hops/bobs** while matching `PrismfallEBDX.grounded_oy` automatically.
3. **Direct Live GIF→PNG Conversion Tests:**
   - **Pokémon Showdown `gen5ani*` (live HTTPS):** `15 / 15` strips passed (`0` failures) — tested `KYOGRE_1` (`85f`, disposal=3 verified `0` pixel diff!), `GROUDON_1` (`50f`), `SALAMENCE_1` (`103f`), `GHOLDENGO` (`93f`), `VULPIX_1` (`10f`), `ZOROARK_1` (`24f`), `WOOPER_1` (`72f`).
   - **Ghasty001 GitHub GIFs:** `26 / 26` strips passed (`0` failures) — tested `ANNIHILAPE` (`92f`), `DRAGAPULT` (`50f`), `ALTARIA_1` (`61f`), `CLAWITZER` (`60f`), `DRAGALGE` (`70f`), `HELIOLISK` (`44f`), `GHOLDENGO` Back (`6f`).
4. **Full Merged Engine Copy Test (`/home/antigravity/pf_engine_run/sprite_test_out/engine_copy/`):**
   - Standalone `--audit` on merged copy confirmed **796/796 Live (0 gaps)** and **819/819 Live+Spotlight (0 gaps)** across all 4 views.
   - Stale static `Front/999.png` (Gimmighoul `96×96`) cleanly replaced with `6649×61` (**109-frame** animated strip!).
   - `--normalize-extensions` cleanly lowercased **116 uppercase `.PNG` files** (`29 × 4` views, including `ZORUA_1.PNG`) under `Graphics/Pokemon/` → **`0` remaining `.PNG` files**.
5. **Visual QA Inspection (`view_file`):**
   - Visually inspected both [72_gen6_9_mega_animated_sprites.png](file:///home/antigravity/.gemini/jetski/brain/2484663edd3ff4720df7e62906cca222/previews/72_gen6_9_mega_animated_sprites.png) and [72_gen6_9_mega_animated_sprites.gif](file:///home/antigravity/.gemini/jetski/brain/2484663edd3ff4720df7e62906cca222/previews/72_gen6_9_mega_animated_sprites.gif) showing **30 spotlight Front + Back pairs (60 live animated sprites)** at uniform 1× native scale — crisp 2D Gen 5 B2W2 pixel art, clean battle-base grounding, zero 3D renders, zero clipping, smooth 32-frame loop!

---

## 6. Claude Handoff Commands (Drop-In Ready)

1. Copy `install_ebdx_animated_sprites.py` to `tools/install_ebdx_animated_sprites.py` and merge `SPRITE_CREDITS.md` into `CREDITS.md`.
2. Overlay the already-verified staged pack into the engine (instant, 0 conversion wait) OR regenerate cleanly from scratch:
   ```bash
   # Option A — Apply pre-verified staged pack directly (40.61 MB, 1,402 strips):
   cp -a /home/antigravity/pf_engine_run/ebdx_gen6_9_animated_pack/{Front,Back,FrontShiny,BackShiny} \
         /home/antigravity/pf_engine_run/base/Graphics/EBDX/Battlers/

   # Option B — Fully repeatable clean run from scratch (any machine):
   python3 tools/install_ebdx_animated_sprites.py \
     --download-sources /home/antigravity/pf_engine_run/sprite_sources \
     --engine /home/antigravity/pf_engine_run/base \
     --prismfall-pbs pbs \
     --source renovation4=/home/antigravity/pf_engine_run/sprite_sources/chromevaliant_ebdx/Graphics/Pokemon \
     --source ghasty=/home/antigravity/pf_engine_run/sprite_sources/ghasty001 \
     --fetch-showdown-gaps \
     --prefer-more-frames \
     --include-female \
     --scope prismfall-plus-forms \
     --install-prismfall \
     --normalize-extensions /home/antigravity/pf_engine_run/base/Graphics/Pokemon \
     --audit \
     --verify-strips
   ```
3. **Companion Ruby/PBS Polish Reminders (from Proposal §A.3 — Claude's engine slice):**
   - Apply the 2-line `subdir2` shiny static fallback fix in `Plugins/Elite Battle DX/[000] Scripts/Battle Core/Battler Bitmaps.rb:199–207, 341–350` (`"Front shiny"` / `"Back shiny"`).
   - Add `BattlerAltitude = 10` (or `PrismfallEBDX::FLOATING` entries) for hovering Gen 7–9 species without `:LEVITATE` (`PECHARUNT`, `GHOLDENGO`, `FLUTTERMANE`, `IRONMOTH`, `IRONJUGULIS`, `DRAGAPULT`, `MINIOR`, Tapus, etc.) so they float cleanly above their shadows.
