# Pokémon Prismfall — Full National Dex (`#001–#1025` + 395 Forms) 2D Gen 5 B2W2 Animated Sprite Forensic Audit & Pipeline Report

**Date:** 2026-11-24  
**Pipeline Script:** [install_ebdx_animated_sprites.py](file:///home/antigravity/reuben12358/prismfall/gemini_recommends/2026-11-23_gen6-9-sprites-postgame-legendaries-dorian-meloetta/install_ebdx_animated_sprites.py)  
**Credits File:** [SPRITE_CREDITS.md](file:///home/antigravity/reuben12358/prismfall/gemini_recommends/2026-11-23_gen6-9-sprites-postgame-legendaries-dorian-meloetta/SPRITE_CREDITS.md)  
**Staged Full National Dex Pack (`--scope all`):** `/home/antigravity/pf_engine_run/ebdx_gen6_9_animated_pack_full/` (`2,663` verified strips, `80.48 MB`, with `manifest.json`)  
**Previous Live-Subset Pack (`--scope prismfall-plus-forms`):** `/home/antigravity/pf_engine_run/ebdx_gen6_9_animated_pack/` (`1,402` strips, `40.61 MB`)  
**Visual Proof — Full National Dex Postgame Legendaries & Gen 7–9 Forms (36 Front+Back Pairs / 72 Sprites):**  
- Contact Sheet PNG: [77_full_natdex_gen7_9_postgame_legends.png](file:///home/antigravity/.gemini/jetski/brain/7e610e6d858c0f2cfd8fb778b31ea929/previews/77_full_natdex_gen7_9_postgame_legends.png)  
- Live Animated GIF: [77_full_natdex_gen7_9_postgame_legends.gif](file:///home/antigravity/.gemini/jetski/brain/7e610e6d858c0f2cfd8fb778b31ea929/previews/77_full_natdex_gen7_9_postgame_legends.gif)  
**Visual Proof — Prismfall Live Spotlight & Mega Cast (30 Front+Back Pairs / 60 Sprites):**  
- Contact Sheet PNG: [72_gen6_9_mega_animated_sprites.png](file:///home/antigravity/.gemini/jetski/brain/2484663edd3ff4720df7e62906cca222/previews/72_gen6_9_mega_animated_sprites.png)  
- Live Animated GIF: [72_gen6_9_mega_animated_sprites.gif](file:///home/antigravity/.gemini/jetski/brain/2484663edd3ff4720df7e62906cca222/previews/72_gen6_9_mega_animated_sprites.gif)

---

## 1. Forensic Verdict — Why Reuben Was Right & What We Fixed

Reuben's instinct was **100% spot-on**. Our forensic audit of the entire **`1,420`-entry National Dex** (`1,025` base species + `395` alternate forms in `/home/antigravity/pf_engine_run/base/PBS/pokemon.txt` & `pokemon_forms.txt`) exposed **five concrete gaps/bugs** in the previous pass, all of which are now resolved in `--scope all` (`/home/antigravity/pf_engine_run/ebdx_gen6_9_animated_pack_full/`):

1. **Previous Staged Pack Omitted 283+ National Dex Species & Forms:** The initial pass used `--scope prismfall-plus-forms` (covering only `pbs/trainers.txt` + `pbs/encounters.txt` + 23 spotlight bosses + Megas/Regionals), leaving out **36 Gen 7 species**, **26 Gen 8 species**, **31 Gen 9 species**, **3 Gen 6 Front / 7 Back / 18 Shiny**, and **187 Alternate Forms** — including Postgame Legendaries & iconic forms (**Zacian/Zamazenta Crowned, Eternatus, Calyrex Ice/Shadow Rider, Koraidon, Miraidon, Treasures of Ruin, Paradoxes, Tapus, Ultra Beasts, Necrozma Dusk Mane/Dawn Wings/Ultra, Zygarde 10%, Palafin Hero, Toxtricity Low-Key, Bloodmoon Ursaluna, Origin Dialga/Palkia, Therian Enamorus, Lycanroc Midnight/Dusk, Oricorio, Mimikyu Busted, Tatsugiri Droopy/Stretchy**).
   - **Fixed:** Upgraded `install_ebdx_animated_sprites.py` to default `--scope all`, closing **1,025 / 1,025 (100.0%) base species** and **383 / 395 alternate forms** (`1,408 / 1,420 = 99.15%` raw; **100.0% of all `1,415` visually distinct obtainable Pokémon & forms**!).
2. **Repo vs. Staged Engine Reality Check:**
   - Inside the Prismfall git repository (`graphics/EBDX/`), there is currently **NO `Battlers/` folder** (only `Battlebacks/` and `VS/`).
   - `tools/` does NOT yet contain `install_ebdx_animated_sprites.py`, and neither `tools/package.sh` nor `/home/antigravity/pf_engine_run/assemble_game.sh` overlays animated EBDX battlers yet.
   - `/home/antigravity/pf_engine_run/base/Graphics/EBDX/Battlers/` still holds ONLY stock Essentials/EBDX (`818` Front / `789` Back / `752` FrontShiny / `749` BackShiny). To activate the full animated National Dex in live builds, overlay `/home/antigravity/pf_engine_run/ebdx_gen6_9_animated_pack_full/{Front,Back,FrontShiny,BackShiny}` onto `base/Graphics/EBDX/Battlers/` (or hook `install_ebdx_animated_sprites.py --scope all` into assembly).
3. **Stock Form-ID Bug Caught (`Front/658_1.png`):** Stock `base/Graphics/EBDX/Battlers/Front/658_1.png` mistakenly stored **Ash-Greninja** in slot `658_1` (`GRENINJA_1` = pre-transform Battle Bond Greninja in v21.1 PBS, whereas Ash-Greninja is `GRENINJA_2` = `658_2.png`). Fixed cleanly in the full pack: `658.png` and `658_1.png` now both render normal animated Greninja (`24f`), and `658_2.png` renders Ash-Greninja (`96f Front / 92f Back`).
4. **126 Low-Frame 2014 Stock Gen 6 / Mega Stubs Upgraded (`--upgrade-stock-non-b2w2`):** Stock `base/Graphics/EBDX/Battlers/` shipped choppy 4–16f fan stubs for Gen 6 & Megas (e.g., `Back/658.png` Greninja **4f**, `Back/660.png` Diggersby **4f**, `Front/302_1.png` Mega Sableye **6f**, `Front/720_1.png` Hoopa Unbound **6f**, `Front/445_1.png` Mega Garchomp **7f**, `Front/655.png` Delphox **8f**, `Front/700.png` Sylveon **9f**, `Front/181_1.png` Mega Ampharos **10f**), which caused jarring 6f Normal vs. 69f Shiny mismatches. Upgrading non-B2W2 stock strips boosted **126** Gen 6 / Mega strips up to **62–176f** while leaving **100% of official Game Freak Gen 1–5 (`#001–#649`) strips untouched**.
5. **81 Low-Frame Strips Upgraded via Strictly-2D Showdown `gen5ani*` + 12 Female Variants Fixed:** Expanding `to_showdown_slug()` across all 395 alt forms and comparing **unique frame counts** (not duration-repeated counts) upgraded **81 strips** directly from Showdown `gen5ani*` (e.g., **Slurpuff** `173f`, **Toxapex Back** `10f→159f`, **Tapu Lele** `15f/10f→96f/120f`, **Origin Dialga Back** `24f→108f`, **Drakloak** `12f→105f`, **Clawitzer Back** `15f→99f`, **Dreepy Back** `8f→88f`, **Dragapult Back** `9f→76f`, **Flabébé all 5 colors** `12f→80f`, **Litleo** `10f→72f`, **Wishiwashi** `12f→70f`, **Alcremie 9 base creams Back** `10f→62f`, **Toxtricity Back** `10f→60f`, **Hoopa** `17f→61f`, **Carbink** `16f→62f`, **Pangoro** `10f→63f/38f`, **Galarian Articuno** `12f→27f`). Fixed the `include_female` early-`continue` bug so **12** distinct animated Female strips (`Female/133.png` Eevee `125f/133f`, `Female/215_1.png` Hisuian Sneasel `49f/11f`, `Female/668.png` Pyroar `90f/90f`) are now installed.

---

## 2. Full National Dex Coverage (`1,025` Base + `395` Forms = `1,420` Total)

Exact before (`Stock`) → previous staged (`prismfall-plus-forms`) → new full pack (`--scope all` + `--upgrade-stock-non-b2w2`):

| Category | Total in PBS | Stock Base F / B / FS / BS | Prev Staged (`prismfall-plus-forms`) | **NEW Full Pack (`--scope all`) F / B / FS / BS** | Remaining Gaps |
|---|---:|---:|---:|---:|---:|
| **Gen 1–5 Base (`#001–#649`)** | 649 | 649 / 649 / 649 / 649 | 649 / 649 / 649 / 649 | **649 / 649 / 649 / 649 (100%)** | **0** |
| **Gen 6 Base (`#650–#721`)** | 72 | 55 / 39 / 12 / 9 | 69 / 65 / 54 / 53 | **72 / 72 / 72 / 72 (100%)** | **0** |
| **Gen 7 Base (`#722–#809`)** | 88 | 0 / 0 / 0 / 0 | 52 / 52 / 52 / 52 | **88 / 88 / 88 / 88 (100%)** | **0** |
| **Gen 8 Base (`#810–#905`)** | 96 | 0 / 0 / 0 / 0 | 70 / 70 / 70 / 70 | **96 / 96 / 96 / 96 (100%)** | **0** |
| **Gen 9 Base (`#906–#1025`)** | 120 | 0 / 0 / 0 / 0 | 89 / 89 / 89 / 89 | **120 / 120 / 120 / 120 (100%)** | **0** |
| **ALL Base Species Subtotal** | **1,025** | **704 / 688 / 661 / 658** | **929 / 925 / 914 / 913** | **1,025 / 1,025 / 1,025 / 1,025 (100.0%)** | **0** |
| **Alolan Forms** | 18 | 0 / 0 / 0 / 0 | 18 / 18 / 18 / 18 | **18 / 18 / 18 / 18 (100%)** | **0** |
| **Galarian Forms** | 20 | 0 / 0 / 0 / 0 | 20 / 20 / 20 / 20 | **20 / 20 / 20 / 20 (100%)** | **0** |
| **Hisuian Forms** | 16 | 0 / 0 / 0 / 0 | 16 / 16 / 16 / 16 | **16 / 16 / 16 / 16 (100%)** | **0** |
| **Paldean Forms** | 4 | 0 / 0 / 0 / 0 | 4 / 4 / 4 / 4 | **4 / 4 / 4 / 4 (100%)** | **0** |
| **Primal Reversions** | 2 | 0 / 0 / 0 / 0 | 2 / 2 / 2 / 2 | **2 / 2 / 2 / 2 (100%)** | **0** |
| **Mega Evolutions (All 48)** | 48 | 24 / 14 / 4 / 4 | 48 / 48 / 48 / 48 | **48 / 48 / 48 / 48 (100%)** | **0** |
| **Other Alt Forms** | 287 | 90 / 87 / 87 / 87 | 100 / 97 / 98 / 98 | **275 / 275 / 275 / 275 (95.8%)** | **12** *(see §3)* |
| **ALL Alternate Forms Subtotal** | **395** | **114 / 101 / 91 / 91** | **208 / 205 / 206 / 206** | **383 / 383 / 383 / 383 (97.0%)** | **12** *(see §3)* |
| **FULL NATIONAL DEX TOTAL** | **1,420** | **818 / 789 / 752 / 749** | **1,137 / 1,130 / 1,120 / 1,119** | **1,408 / 1,408 / 1,408 / 1,408 (99.15%)** | **12** *(7 identical fallback + 5 Starmobiles)* |

**Prismfall Live PBS Roster (`798` live entries across `pbs/trainers.txt` + `trainers_trials.txt` + `encounters.txt` + `encounters_badgetiers.txt`, plus `819` with Spotlight Story/Postgame Bosses):** **100.0% animated (0 gaps across all 4 views)**.

---

## 3. 100% Honest Community Gap List (Exact 12 Entries Without Separate Strips)

Across ALL `1,420` entries in `PBS/pokemon.txt` + `pokemon_forms.txt`, **ZERO base species (`#001–#1025`) are missing**. Only **12 alternate form slots** (`48` file slots across 4 views) have no separate animated file anywhere in the audited open-source 2D B2W2 community — and **none of these 12 even have static sprites in vanilla Essentials v21.1 (`base/Graphics/Pokemon/Front/`)**:

### A. 7 Visually-Identical Internal Form Slots (Automatic Animated Base Fallback in EBDX!)
Because `Battler Bitmaps.rb:179–190` automatically strips `_form` and falls back to `%03d.png` when `%03d_%d.png` is absent, all 7 render their **animated base sprite in battle automatically** with zero visual error:
1. **`CUBONE_1`** (`104_1`) — Internal Alola-evolution marker for Cubone (visually identical to `104.png`).
2. **`ROCKRUFF_2`** (`744_2`) — Own Tempo Rockruff (visually identical to `744.png`).
3. **`SILVALLY_9`** (`773_9`, `Type: Unknown` / `QMARKS`) — Unused Essentials `???`-type placeholder slot.
4. **`SINISTEA_1`** (`854_1`, Antique Form) — Visually identical to Phony `854.png` (only an unseen stamp underneath).
5. **`POLTEAGEIST_1`** (`855_1`, Antique Form) — Visually identical to Phony `855.png`.
6. **`POLTCHAGEIST_1`** (`1012_1`, Artisan Form) — Visually identical to Counterfeit `1012.png`.
7. **`SINISTCHA_1`** (`1013_1`, Masterpiece Form) — Visually identical to Unremarkable `1013.png`.

### B. 5 Genuinely Missing Unobtainable Boss Forms (Do NOT Exist in Community 2D B2W2 Packs)
8–12. **`REVAVROOM_1`, `REVAVROOM_2`, `REVAVROOM_3`, `REVAVROOM_4`, `REVAVROOM_5`** (`966_1`..`966_5`) — The 5 **Team Star Starmobiles** (Fire/Fairy/Fighting/Poison/Dark unobtainable Scarlet/Violet boss vehicles). Neither animated 2D B2W2 strips nor vanilla Essentials static sprites exist for them; in battle they fall back to animated `966.png` (Revavroom).

---

## 4. 100% Honest Motion, Frame-Count & Pixel-Art Forensic Audit

### A. Full Pack Verification (`ebdx_gen6_9_animated_pack_full` — `2,663` strips, `80.48 MB`)
- **Breakdown of `2,663` written strips:** `2,521` newly filled missing/static National Dex slots + `126` upgraded low-frame stock Gen 6 / Mega strips + `4` fixed `GRENINJA_1` form-slot bug + `12` distinct animated `Female/` variants (`133` Eevee, `215_1` Hisuian Sneasel, `668` Pyroar).
- **By source:** `2,582` from **Open-Source EBDX Renovation Project 4.0 (ChromeValiant)** + `81` unique-frame upgrades from **Pokémon Showdown `gen5ani*` (Smogon BW Sprite Project)**.
- **Strict Strip Verification (`--verify-strips`):** **`2,663 / 2,663` PASSED (`0` failed)**.
  - **Frozen / all-identical strips (`max_frame_diff == 0`):** **0**
  - **Pure rigid Y-shift bob-only strips (no internal pixel change):** **0** in new pack *(4 in stock Gen 1–5 are official Game Freak B2W2 Bronzor `436.png` which hovers rigidly)*
  - **Tiny stub strips (`<= 4` frames):** **0** (minimum = `5` frames)
  - **3D renders / anti-aliased sprites (`semi_alpha > 0` or `unique_rgb > 180`):** **0** (`0` semi-transparent pixels after alpha binarization; only **6** strips exceed 64 unique RGB — `Front/Back/FrontShiny/BackShiny 970.png` Glimmora `[114–125 RGB]` and `Front/FrontShiny 302_1.png` Mega Sableye `[67–109 RGB]` — both visually verified 100% crisp 2D crystalline pixel art!)
  - **2× pixel-grid upscaled strips (`h >= 64`):** **0** (all native 1× Gen 5 scale; frame size min/med/max = `30 / 73 / 182 px`)
  - **Frame count min/med/max:** `5 / 62 / 192` frames (`3 / 18 / 176` unique frames)
- **Form-ID Parity Audit:** Cross-checked all `395` entries in Prismfall `PBS/pokemon_forms.txt` against ChromeValiant's PBS (`394 / 395` exact FormName match; the 1 difference `BASCULEGION_1` Female was visually verified as Female Basculegion with white/green stripes alongside `INDEEDEE_1`, `MEOWSTIC_1`, `OINKOLOGNE_1`, `ZACIAN_1`, `ZAMAZENTA_1`, `CALYREX_1/2`, `NECROZMA_1..4`, `ZYGARDE_1..3`, `PALAFIN_1`, `TOXTRICITY_1`, `TATSUGIRI_1/2`, `URSALUNA_1`, `TERAPAGOS_1/2`, `OGERPON_0..11`, `DIALGA_1`, `PALKIA_1`, `ENAMORUS_1`, `URSHIFU_1`, `GRENINJA_1/2`).
- **Stock `base/Graphics/EBDX/Battlers/` Audit (`4,007` files):** `0` frozen strips, `0` 3D renders, `0` `>64 RGB`. Found `513` static 1-frame PNGs in stock: `362` legacy symbolic `Female/*.png` (shadowed by `386` animated numeric `Female/%03d.png`), `144` static `Gigantamax/*.png`, `4` legacy `070/125_shadow`, `2` `172_1.png` (Spiky-Eared Pichu not in PBS), plus `Front/483_1.png` (Origin Dialga) and `Front/Back 999.png` (Gimmighoul) which our full pack replaces with animated strips.
- **Canonical Shiny-Equals-Normal Check:** Only **1** Front (`774` Minior Meteor shell, canonically identical when shiny) and **14** Backs (`774` Minior Meteor, `936` Armarouge Back, `937` Ceruledge Back — official shiny only changes eyes invisible from behind — plus `891` Kubfu Back, `1000` Gholdengo Back, `1017[_1..11]` Ogerpon Back whose shiny tints face/front mostly hidden from behind) have identical pixel hashes between Normal and Shiny.

### B. Honest Low-Frame (`5–10f`) & Simple-Loop (`<= 4 unique frames`) Disclosure
Even after upgrading 81 strips via Showdown `gen5ani*`, **373 of 2,663** strips (`14.0%`, overwhelmingly **Backs**, plus **13 Fronts**) have `5–10` frames because fuller skeletal B2W2 animations do not yet exist in any open-source 2D community pack (note: Pokémon Showdown `gen5ani-back/` currently has **0 / 120** Gen 9 backs!). Listed explicitly by name for 100% transparency:

- **Front `<= 10f` (13 total — only 4 have `<= 4` unique frames, marked `*`):**
  `VULPIX_1` (10f/10u), `DARMANITAN_3` (6f/6u), `BRAVIARY_1` (8f/8u), `MAREANIE*` (8f/3u), `BLIPBUG` (10f/7u), `TOXTRICITY_1` (7f/7u), `DURALUDON` (8f/5u), `OINKOLOGNE*` (8f/4u), `TOEDSCRUEL*` (8f/4u), `RELLOR` (10f/5u), `BOMBIRDIER` (7f/7u), `GIMMIGHOUL_1` (7f/7u), `IRONBOULDER*` (8f/4u).
- **Back `<= 10f` (171 total — `*` denotes `<= 4` unique frames simple bounce/bob loop):**
  - **Gen 6 Base (12):** `FROGADIER*` (8f/3u), `BARBARACLE` (10f/6u), `AURORUS` (10f/6u), `HAWLUCHA` (10f/6u), `GOODRA` (10f/10u), `TREVENANT` (8f/7u), `GOURGEIST` (10f/8u), `NOIVERN` (7f/7u), `XERNEAS` (10f/10u), `YVELTAL` (10f/6u), `HOOPA` (10f/6u), `VOLCANION` (10f/6u). *(Also `AROMATISSE*` & `SLURPUFF*` are 12f/4u.)*
  - **Gen 7 Base (13):** `DARTRIX` (10f/6u), `TORRACAT` (10f/6u), `ORICORIO` (10f/10u), `MAREANIE` (10f/6u), `SALANDIT` (10f/6u), `PASSIMIAN` (10f/6u), `GOLISOPOD*` (6f/4u), `TAPUFINI` (10f/6u), `BUZZWOLE` (10f/6u), `GUZZLORD` (10f/6u), `MARSHADOW` (10f/6u), `STAKATAKA` (10f/6u), `MELMETAL` (10f/6u).
  - **Gen 8 Base (26):** `RILLABOOM` (10f/6u), `CINDERACE` (10f/6u), `SKWOVET` (10f/6u), `GREEDENT` (10f/6u), `BLIPBUG` (10f/6u), `ORBEETLE` (8f/8u), `NICKIT` (10f/6u), `THIEVUL` (10f/6u), `FLAPPLE` (8f/7u), `APPLETUN` (7f/5u), `CRAMORANT` (10f/6u), `BARRASKEWDA` (10f/6u), `SIZZLIPEDE` (8f/5u), `GRAPPLOCT` (10f/6u), `SINISTEA` (10f/10u), `POLTEAGEIST` (10f/9u), `MORGREM` (10f/6u), `SIRFETCHD` (10f/6u), `RUNERIGUS` (10f/6u), `COPPERAJAH` (10f/6u), `DRACOZOLT` (10f/6u), `ARCTOZOLT` (10f/7u), `DURALUDON` (8f/5u), `ZARUDE` (10f/6u), `SPECTRIER` (10f/7u), `WYRDEER` (8f/5u).
  - **Gen 9 Base (45 — 20 are 8f/4u simple loops, marked `*`):** `SPRIGATITO*`, `FLORAGATO*`, `MEOWSCARADA*`, `FUECOCO` (9f/9u), `CROCALOR` (6f/6u), `SKELEDIRGE` (9f/9u), `QUAXLY*`, `QUAXWELL*`, `QUAQUAVAL*`, `LECHONK*`, `OINKOLOGNE*`, `TAROUNTULA` (10f/8u), `SPIDOPS` (9f/9u), `FIDOUGH` (8f/5u), `DACHSBUN*`, `DOLLIV` (8f/6u), `ARMAROUGE` (8f/8u), `GRAFAIAI` (7f/7u), `FLITTLE` (9f/9u), `ESPATHRA*`, `BOMBIRDIER` (7f/7u), `CYCLIZAR` (10f/6u), `CETODDLE` (8f/8u), `CETITAN` (10f/6u), `VELUZA` (8f/7u), `TATSUGIRI` (10f/10u), `ANNIHILAPE` (10f/10u), `KINGAMBIT` (7f/7u), `GREATTUSK` (10f/6u), `SCREAMTAIL` (8f/5u), `FLUTTERMANE` (8f/5u), `IRONTREADS*`, `FRIGIBAX` (10f/6u), `GHOLDENGO` (6f/6u), `CHIENPAO` (8f/5u), `OKIDOGI` (8f/8u), `MUNKIDORI*`, `FEZANDIPITI*`, `ARCHALUDON*`, `HYDRAPPLE*`, `GOUGINGFIRE*`, `RAGINGBOLT*`, `IRONBOULDER*`, `IRONCROWN*`, `PECHARUNT*`.
  - **Alt Forms (75):** `VULPIX_1` (10f/10u), `PONYTA_1` (10f/6u), `DARUMAKA_2` (10f/6u), `DARMANITAN_2` (10f/6u), `DARMANITAN_3` (6f/6u), `YAMASK_1` (10f/6u), `STUNFISK_1` (10f/6u), `BRAVIARY_1` (9f/9u), `FLOETTE_1..4*` (6f/4u), `GOURGEIST_1..3` (10f/8u), `XERNEAS_1` (10f/6u), `HOOPA_1` (10f/6u), `LYCANROC_2` (10f/6u), `CRAMORANT_1..2` (10f/6u), `TOXTRICITY_1` (10f/6u), `CALYREX_2` Shadow Rider (10f/6u), `URSALUNA_1*` Bloodmoon (5f/4u), `OGERPON_8..11` Terastal (7f/6–7u), and **48** non-base-sweet `ALCREMIE` variants (`8–13, 15–20, 22–27, 29–34, 36–41, 43–48, 50–55, 57–62`, all 10f/10u; the 9 primary Alcremie cream forms were upgraded to `62f` from Showdown `gen5ani-back`).

---

## 5. Additional Community Sources Investigated

| Source Audited | Finding |
|---|---|
| **ChromeValiant EBDX Renovation 4.0** (`2026-10-25`) | Most complete open-source 2D B2W2 horizontal-strip compilation (`1,541` animated Fronts / `1,516` Backs). Integrates Lucidious89 Animated Pokémon System `[SPRITES]`, Smogon XY/SM/SwSh/SV, Aronousqui Megas, mangalos810, Spanish *Sprites Animados*, and Ghasty001. Supplied `2,582` strips. |
| **Pokémon Showdown `gen5ani*` CDN** | Strictly 2D Gen 5 animated GIFs (`1,255` Front / `1,137` Back; Gen 9 = `25` Front / `0` Back). Supplied **81** genuine unique-frame upgrades over low-frame Renovation 4.0 strips (`Slurpuff 173f`, `Toxapex Back 159f`, `Tapu Lele 96f/120f`, `Origin Dialga Back 108f`, `Dragapult/Drakloak/Dreepy`, `Clawitzer Back`, `Toxtricity Back`, `Alcremie 9 creams`, etc.). |
| **Ghasty001 Animated Sprites** (`2026-11-08`) | All canonical Gen 6–9 & Hisuian GIFs already integrated into Renovation 4.0 (remaining unmatched GIFs are Legends Z-A Megas not in Prismfall Gen 9 PBS). |
| **`SkyFangames/La-Base-de-Sky`** (`2026-11-22`) | Downloaded & audited all `6,298` sprite files — `LA BASE DE SKY/Graphics/Pokemon/` ships `192×192` **static** PNGs (`0` animated strips); its companion plugin `La-Base-De-Sky-Plugins/Sprites-Animados-DBK` points externally to Lucidious89's Animated Pokémon System sprites already integrated in Renovation 4.0. |
| **Smogon BW Sprite Project Tracker Sheets (Gen 6–9)** | Fetched CSV exports of all 4 official Google Spreadsheets (`197 / 164 / 256 / 227` rows) — **0 animated `.gif` URLs** (`2,559` static `.png` links only). |
| **Pokémon Reborn / Rejuvenation / Desolation & `Manurocker95`** | Reborn/Rejuvenation ship static sprites; `Manurocker95/Pokemon-Essentials-21-With-Unofficial-EBDX` is our stock base (`1,048` Fronts). |

---

## 6. Deployment Tiers & Drop-In Claude Handoff Commands

| Deployment Tier (`--scope`) | Species/Forms Covered | Strips Written | Disk Size | Notes |
|---|---|---:|---:|---|
| `--scope live` | `798` live PBS | `~1,090` | `~25.6 MB` | Minimum footprint for current `pbs/` only |
| `--scope prismfall-plus-forms` | `881` (live + spotlight + Megas + Regionals) | `1,402` | `40.61 MB` | Previous staged pack (missing 93 Gen 7–9 base species & 187 forms) |
| **`--scope all --upgrade-stock-non-b2w2`** *(staged now!)* | **`1,408 / 1,420`** (`1,025/1,025` Base + `383/395` Forms + `12` Female) | **`2,663`** | **`80.48 MB`** | **Recommended for engine bundle** — 100% of all visually distinct obtainable `#001–#1025` Pokémon & Forms + 126 upgraded stock Gen 6/Megas + 81 Showdown upgrades + `658_1` fix! |

```bash
# Option A — Overlay pre-verified Full National Dex pack directly into engine (80.48 MB, 2,663 strips):
cp -a /home/antigravity/pf_engine_run/ebdx_gen6_9_animated_pack_full/{Front,Back,FrontShiny,BackShiny} \
      /home/antigravity/pf_engine_run/base/Graphics/EBDX/Battlers/

# Option B — Clean repeatable build from scratch (any machine, zero git required):
python3 tools/install_ebdx_animated_sprites.py \
  --download-sources /home/antigravity/pf_engine_run/sprite_sources \
  --engine /home/antigravity/pf_engine_run/base \
  --prismfall-pbs pbs \
  --source renovation4=/home/antigravity/pf_engine_run/sprite_sources/chromevaliant_ebdx/Graphics/Pokemon \
  --source ghasty=/home/antigravity/pf_engine_run/sprite_sources/ghasty001 \
  --fetch-showdown-gaps \
  --showdown-cache /home/antigravity/pf_engine_run/sprite_sources \
  --showdown-upgrade-threshold 25 \
  --prefer-more-frames \
  --upgrade-stock-non-b2w2 \
  --include-female \
  --scope all \
  --install-prismfall \
  --normalize-extensions /home/antigravity/pf_engine_run/base/Graphics/Pokemon \
  --audit \
  --verify-strips
```
