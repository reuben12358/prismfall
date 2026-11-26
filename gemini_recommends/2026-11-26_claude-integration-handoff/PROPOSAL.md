# Proposal: Claude Integration Hand-Off — Cutscene Card Ribbon Fix, Map Second Pass (244/249/593 + 0 Warnings), & Complete Art-Owed Wiring

Date: 2026-11-26
From: Gemini (Visual QA / Art / Mapgen)
For: Claude (Integration into Claude-owned `plugins/`, `pbs/`, `story/`, `tools/`)

---

## 1. URGENT P0 UI Fix — Chapter Opening Card Ribbon Strike-Through (`plugins/Prismfall Cutscenes/020_ChapterOpeningCards.rb`)

Independent `visual_critic` audit of the live `020_ChapterOpeningCards.rb` render caught a systemic layout bug affecting **all 24 chapter cards**:

- **Root cause:** `RIBBON_H = 96` (L39) draws the bottom gold rule at `y = RIBBON_H - 2 = 94` (L943). Meanwhile `text_sprite(:loc, ..., @ribbon_y + 74, 53)` (L916) builds a `42px` bitmap and calls `bmp.draw_text(0, 0, @w, 40, text, 1)` (L962), which vertically centers the `:loc` subtitle at `y = @ribbon_y + 74 + 20 = @ribbon_y + 94`. Result: **the bottom gold horizontal rule cuts straight through the middle of the Location subtitle on every single chapter card.**
- **Suggested 5-line fix in `plugins/Prismfall Cutscenes/020_ChapterOpeningCards.rb`:**
  1. Line 39: `RIBBON_H = 110` (up from `96`), and on line 897 nudge `@ribbon_y` up by `7px` (`- 7`) so vertical framing stays balanced.
  2. Lines 913–916: adjust the 4 text sprite `y` anchors to sit cleanly centered inside the `110px` ribbon (remembering `draw_text(..., 40, ...)` centers at `y + 20`):
     - `:act` -> `@ribbon_y - 2` (center `+18`)
     - `:num` -> `@ribbon_y + 15` (center `+35`)
     - `:title` -> `@ribbon_y + 38` (center `+58`)
     - `:loc` -> `@ribbon_y + 66` (center `+86`, leaving `22px` clear above the bottom rule at `y = 108`).

### 1b. Guard `set_pose` Row Detection (`plugins/Prismfall Cutscenes/017_AdvancedAnimations.rb`)
- At L202–207, `set_pose(sheet, pose_idx)` currently hard-codes `load_sheet(sheet, [4, 1], false)`. Since 61+ cast `pose_*.png` sheets use the `128x192` `4x4` layout (4 poses × 4 frames, matching `018_ExpressiveDialogue.rb`), auto-detecting `rows = (bmp.height >= 160 ? 4 : 1)` prevents `set_pose` from ever stretching or mis-slicing a 4×4 pose sheet.

---

## 2. Map Second Pass — `120 maps; 0 warnings` + 3 New Built Maps (`249`, `244`, `593`)

### 2a. `mapgen/build.py` Improvements (already landed)
- **`walk_airborne` spec key** (regex on event names): skips mid-throw trampoline events (`^Web ` on Map 131 Loomhouse Canopy) in both `check_reach` and `walk_check` (their landings are already mathematically proved by `mapgen/puzzles/canopy.py`).
- **Inert empty rest-page skip** in `walk_check`: parallel/autorun events whose only non-empty pages are trigger 3/4 (with an empty `cond: {self: A}` rest page, e.g. Map 548 Atmosphere/Escort setup) are no longer falsely flagged as walk-to events.
- **`walk_speckle` filter** (`default: 4` tiles): unreachable scenery-edge pockets of `<= 4` tiles (passable rock/icicle tops, ravine-rim autotile corners on Map 548) are ignored for the `% stranded` count while events inside them are still flagged.
- **Result:** Full strict build (`mapgen/build.py --strict`) passes with **`120 maps; 0 warnings`**, all 12 `GATE` checks shut, all 7 puzzle checks OK, and **0 unbuilt transfer targets** across all 120 maps.

### 2b. Visual Map Craft Polish Landed (Critic Pass 3 Certified — 0 P0!)
- **Gen 5 Reskin (`mapgen/gen5_reskin.py`):**
  - **Map 545 Brinecut Salt Lake (9.0 PASS):** restored two-tone Chargestone rose-white salt highlights on `shade_cave_strata(mode="salt")`, luminous pale rose-salt crust shoreline ring (`#F0E2E8`/`#D6BAC8`/`#A8879B`), and brine-mint water (`#0C4F5A`..`#6CC8C0`). See `2026-11-26_bgs-drip-nadir-loop-fix/PROPOSAL.md` for full breakdown.
  - **Dirt-path halo fix:** softened pale-mint grass rim highlight (`(168,216,160)`) on `RJ DirtDark` / `RJ Dirt` / `PF Gravel Spring` autotiles into warm B2W2 sunlit olive (`w_rim`).
- **Systemic Winter S1 Mega-Fix & Alpine Route Overhaul (`167`, `522`, `548`, `560`, `561`, `577`, `578`, `579`):** replaced purple-bordered `CERULEAN_3X3`/`PERI_3X3` rectangles on white snow with native seamless `sn_g0..sn_g3` drift variation; cleared `561`'s ~150-boulder snowball block into one diagonal rockslide ridge (`GATE ok`); staggered full-width cliffs & eroded rectangular tall-grass grids into organic glades (`560`/`577`/`578`); carved 6 organic forest clearings & fixed hut tree-clipping on `579`; added organic green-to-snow transition + full-box non-overlapping frosted pines on `522`.
- **Major Urban, War & Landmark Map Upgrades:**
  - `105` & `106` Ferrow Lighthouse: fixed off-by-1-row `SLATE` void tiles; replaced `106`'s grey statue with a 3×3 octagonal crystal/stone Fresnel beacon housing + roaring golden flame on a sunlit dais.
  - `181` Lumen Lowlight & `608` Lowlight Shattered: softened sidewalks to warm weathered grey flagstones, broke S8 facade repetition with market nooks & varied storefronts, added continuous right-edge parapet, and **demolished 3 entire tenement blocks in `608`** into rubble craters, exposed foundations & radiating obsidian/amethyst shatter fissures.
  - `285` Briar Hall Upper Court: cleared colliding barrel/lamp so the twin-lantern garden arch at `(53,40)` stands unbroken.
  - `552` The Dyers' Ford: eliminated all opaque flat-color MS-Paint river dye squares, restoring sparkling animated river water framed by bankside dye vats, timber sluices, hanging cloth drying racks & staggered bunting.
  - `926` The Glass Dunes & `930` Bone-Carters' Camp: replaced `926`'s desert ocean-wave stamp with vitrified obsidian & sea-glass crystal ridges, organic rounded blast craters, smooth western flood channel & feathered desert trails (`GATE ok`); fused `930`'s gapped north cliffs into continuous stepped canyon walls & replaced glowing cyan troughs with wooden barrels/crates/bones.
  - `573` The Two Hearths + **8 S6/S7 Thematic Interior Upgrades (`571`, `572`, `574`, `575`, `576`, `148`, `126`, `168`):** symmetric blazing carved-marble fireplaces + dressed tavern dining tables on `573`; bespoke thematic craft across all 8 interiors (nets/rigging/cork-floats on `168`, twin looms/silk-cutting bench/dye vats on `574`, hanging fish/butcher table on `576`, rustic timber exchange on `572`, warden's lodge on `575`, distinct coastal vs. woodland lantern workshops on `148`/`126`, dressed lodge lounge on `571`, max 1 subtle indoor lamp per room).

### 2c. Story / Quest / PBS Hand-Off for New Maps `249`, `244`, `593`
All three maps (`mapgen/layouts/cindervault_town.py` -> `249`, `244`; `mapgen/layouts/arc_lamp_mile.py` -> `593`) are built, byte-identical roundtrip verified, Critic Pass 3 certified (`244` 9.2, `249` 8.9, `593` 9.2), and warp-matched to `255` and `582` (exact coordinates verified walkable: `255 -> 249 (20,12) up`, `255 -> 244 (10,8) up`, `582 -> 593 (108,40) left`; unbuilt neighbors `240`, `243`, `594` guarded with `pbRgssExists?`). Static canon flavor NPCs/signs are placed; Claude-owned dynamic story/quest/PBS hooks remaining:
1. **Map 244 (`Hearthguild Hall`):**
   - `V129 == 4` ("My Father"): Envoy Haskar in Warden Chair `(7,10)`, two oath-guards, Brann confrontation, Sigrun entering Yard Door `(10,15)`, four bells opening Gym 7.
   - `V129 == 6` ("Whose Is It", arriving from `255` at `(10,8)` facing Light Stone Grille `(10,4)`): `:ch8_lightstone` three-way choice (`:hearthguild` / `:wyrmrest` / `:dominar`), advancing `V129 -> 7`.
   - `V129 == 7` ("Chestnuts"): late-night forge scene by Chestnut Pan `(13,4)` & Cider Cask `(17,10)` (`V129 -> 8`).
   - Ch17 Quest `AS_FORGE_REMEMBERS`: Brann Holloway post-`OS_RING_DAY` (`badges >= 15`, reward `CAMERUPTITE`).
2. **Map 249 (`Cindervault - Slag Ward`):**
   - Dynamic Ch8 states (`V129 == 6` Five Bells dusk/evacuation pacing; `V110 CINDERVAULT_STATE == 1` `:vent` vs `2` `:dampers`).
   - Optional `design/MAP_AUDIO.yaml` entries for `249` & `244` (specs carry `map_audio:` blocks).
3. **Map 593 (`The Arc-Lamp Mile`):**
   - Add `[593]` wild encounter table to `pbs/encounters.txt` (`WORLD.md` pool: Yamper, Shinx, Pawmi, Rookidee, Klink, Magnemite, Bounsweet; Night: Joltik, Voltorb).
   - All 4 confirmed PBS trainers are placed (`[ROCKER, Jax]`, `[JUGGLER, Fitch]`, `[BEAUTY, Coralie]`, `[SCIENTIST, Morley]`). If a 5th trainer per `WORLD.md` is wanted, define in `pbs/trainers.txt`.
   - Optional Juno follower dialogue hooks for Clockwork Pickers & Lamp 47 Glassfall secret + `design/MAP_AUDIO.yaml` entry.

---

## 3. Complete Art-Owed & Critic-Certified Delivery (`tools/check_art_wiring.py` -> 0 Errors, 0 Gaps)

All **154** new/repaired art files are Critic Pass 3 certified (`100% PASS, 0 P0`) and dual-synced byte-identically (`0` MD5 mismatches) across `graphics/` and `art/out/Graphics/` (with **Garret, Nova & Shiv** preserved 100% untouched per Reuben):
1. **Remove all 17 stand-in rows from `plugins/Prismfall Core/032_TrainerArtStandIns.rb`:**
   - 12 Grounds Ladder front strips (`2560x160`, 16f, `9.0–9.4 PASS`): `WEAVER`, `HARPOONER`, `STREAMER`, `FOREMAN`, `MOON_BROKER`, `WYRM_RIDER`, `LAMP_RUNNER`, `WELL_KEEPER`, `LANTERN_ACOLYTE`, `EMBALMER`, `WARDGUARD`, `CANTOR`.
   - 5 War/Border front strips (`2560x160`, 16f, anchor-locked `9.2–9.4 PASS`): `ASHKAAR_SOLDIER`, `THORNWATCH`, `ISENMAR_TRENCHER`, `ISENMAR_HIRDMAN`, `ASHKAAR_EMBER_RIDER`.
2. **Wire Dominar Hrothgar (`Trainers/HROTHGAR.png` [9.5 PASS] + `EBDX/VS/HROTHGAR.png` [9.5 PASS]):**
   - Currently the only 2 `UNWIRED` files in `check_art_wiring.py` because no `[HROTHGAR]` PBS trainer type or `VS_IDS[:HROTHGAR]` entry exists yet; ready to register whenever his Ch19/Ch11 boss encounter is wired.
3. **Interlude Backs & Wenlow VS Bust (live automatically via existing engine paths):**
   - `Trainers/CHAMPION_VALEN_back.png` (9.4), `Trainers/LEADER_ROWAN_back.png` (9.4), `Trainers/SUMP_BARON_back.png` (9.3), `EBDX/VS/WENLOW.png` (9.2).
4. **Overworld Sheets, Full Portrait Expression Sets, Acting Poses, Props & 90° Apex Plates:**
   - All **24** missing `Characters/trainer_<TYPE>.png` sheets (12 Grounds Ladder + 12 core/war/boss classes, `0` cell clips, `8.6–9.3 PASS`) -> `TYPE_CHARSETS` stand-ins for `ASHKAAR_SOLDIER_M` & `ISENMAR_SOLDIER_M` can also be retired.
   - `Portraits/REFLECTION_{surprised,smug,panic,blush,crying}.png` (9.2) + full **11-expression** canonical sets (`55` PNGs, 9.1) for `ASHKAAR_OFFICER`, `ISENMAR_OFFICER`, `MERIDIAN_ADMIN`, `MERIDIAN_ASHE` (base alias synced), `OCTAVE_SINGER` -> **0 single-face portrait notes left**.
   - **6** missing `Characters/pose_*.png` acting sheets (`REFLECTION`, `MERIDIAN_ASHE`, `ASHKAAR_OFFICER`, `ISENMAR_OFFICER`, `MERIDIAN_ADMIN`, `OCTAVE_SINGER`, `8.5–9.0 PASS`, `0` border clips) -> `\pfp[...]` calls work natively in `018_ExpressiveDialogue.rb`.
   - **4** shadow-fixed overworld props (`pf_armchair`, `pf_cave_rock_E/L/S`, `semi_alpha=0`, `exact2x=True`, 9.0).
   - **3** museum-grade `512×384` `90°` cutscene apex plates: new `Pictures/cut_ch2_pageant_tear_90deg.png` (**9.6**, wired in `:CH2_PAGEANT`) + upgraded `cut_ch17_voss_breach_90deg.png` (**9.6**) & `cut_ch19_war1_90deg.png` (**9.4**).
   - **29** Critic P0/P1 battle, OW & action fixes (Squad 1 `PLAYER_A/B`, `PUNK_ZARA` canon mohawk, `PARTNER_OGRE` + `_back`, `SUMP_BARON`, `GILDER_AUTOMATON`, `HOLLOW_ADMIN`, `THORNGUARD`; Squad 2 `FESTIVAL_LIN` crown unclip, `FESTIVAL_TITANIA_back` wavy crimson hair, `QUENT`/`GUTTER` OWs+poses, `PLAYER_A/B_surf` & `_run`, and all 8 `u=9` -> `u=6` smoothed Officer/Agent strips).

---

## 4. Remaining Minor Repo Cleanups (Claude-Owned)
- **Audition HTMLs committed:** `prismfall_anime_ost_audition.html` copied into `gemini_recommends/2026-11-23_anime-ost-situational-bgm/` and `cc0_bgs_v5_audition.html` copied into `gemini_recommends/2026-11-24_cc0-bgs-v5-field-audio-upgrade/` per `REVIEW.md` L167 & L206.
- **Delete 3 unused legacy unsuffixed types** (`HOLLOW_GRUNT`, `MERIDIAN_AGENT`, `ISENMAR_SOLDIER` — 0 trainer blocks each) from `pbs/trainer_types.txt` & `032_TrainerArtStandIns.rb` if no longer needed.
- **Pending future wiring (when maps are built):** war maps `920–926` re-wire to the Ch19 script; two-trainer cameo call for Amaria + Titania on their venue map.
