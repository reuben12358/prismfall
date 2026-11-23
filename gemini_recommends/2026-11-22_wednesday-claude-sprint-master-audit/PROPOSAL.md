# Wednesday Sprint Master Audit — Verified Runtime, Map Softlock, Trial, Economy & UX Brief

- **Date:** 2026-11-22
- **Author:** Gemini (3-Lane Parallel Automated Verification: Battle/Plugins, 117 Built RXDATA Maps & BFS Reachability, PBS/Trials/Economy/UX)
- **Status:** 100% read-only verified & deduplicated against `gemini_recommends/REVIEW.md` and all prior `2026-11-21_*` / `2026-11-22_*` proposals (zero repeated or previously rejected items).

### Baseline Checks (Confirmed Passing)
- `ruby -c` across all `plugins/**/*.rb`: **0 syntax errors.**
- `ruby tools/gen_fields_md.rb --check` & `ruby tools/field_defaults_to_rb.rb --check`: **PASS** (35/35 fields, 0 missing battleback/transition PNGs).
- `pbs/trainers.txt` + `pbs/trainers_trials.txt` (758 trainers) & `pbs/encounters*.txt` (133 base + 78 badge-tier overlays): **0 syntax/duplicate/weight errors.**
- `plugins/Prismfall Trials/` (111 quests, 52 EventMons, 119 TALK keys): **0 broken symbol references.**
- 84/117 built RXDATA maps form a clean connected Prologue→Ch4 graph with 0 out-of-bounds warps and 0 map-connection seam mismatches.

---

## PART A — P0 Hard Crashes, Softlocks & Broken Core Mechanics

### A1. Battle Systems, Bosses, Field Effects & EBDX Bridge (8 P0 Bugs)

1. **Arceus `:prism_turn` Is Silently Dead on Every Bar Break & `:prism_interval` Crashes With `FrozenError`**
   - **Files:** `plugins/Prismfall Bosses/005_Bosses_Effects.rb:298-325`, `plugins/Prismfall Field Effects/004_FieldEffects_Engine.rb:827-835`, `103_Boss_Arceus.rb:92`
   - **Cause:** `Bosses.prism_state` calls `FieldEffects.prism_state(battle)`, which returns a new `.freeze`'d summary hash **without `:turn`**. Result: `Bosses.prism_turn` returns `false` on every Arceus shield break (Plates never rotate, form/moveset never swap), and any boss using `:prism_interval` crashes with `FrozenError` at `005:313`.
   - **Fix (`005_Bosses_Effects.rb:298-303`):** Return the live writable `st[:prism]` hash from `FieldEffects.state(battle)` directly (remove line `300`).

2. **`Pokemon#calc_stats` Arity Mismatch Crashes EBDX 2-Arg Calls (`ArgumentError`)**
   - **File:** `plugins/Prismfall Bosses/002_Bosses_Registry.rb:183-186` (compare `plugins/Prismfall Core/023_Cameos_HPBoost.rb:61-65`)
   - **Cause:** `def calc_stats` takes 0 args while EBDX calls `calc_stats(basestat, boss)`.
   - **Fix:** `def calc_stats(*args)` → `prismfall_bosses_calc_stats(*args)`.

3. **Missing `pbFaint` After Lethal `:on_entry`, `:seed` & `Corrosive Mire` Damage Creates 0-HP Zombie Battlers**
   - **Files:** `plugins/Prismfall Field Effects/004_FieldEffects_Engine.rb:494-495, 524-526`, `107_Field_CorrosiveMire.rb:90-94`
   - **Cause:** `pbTakeEffectDamage` sets `@hp = 0` without calling `pbFaint`. Affects all 6 `:on_entry` hazard fields (`109, 117, 122, 125, 130, 135`), `114_Field_FrozenLake.rb:91` (`ELEMENTALSEED`), and `107_Field_CorrosiveMire.rb:91-94` (marsh-gas Fire blast).
   - **Fix:** Call `battler.pbFaint` when `battler.fainted?` at `004:495`, `004:525`, and `107:94`.

4. **Trainer Boss Bar Depletion on Entry Hazards Stays Unresolved & Absorbs Player's Turn for 0 Damage**
   - **File:** `plugins/Prismfall Bosses/004_Bosses_Battle.rb:224-231`
   - **Cause:** `pbOnBattlerEnteringBattle` never calls `Prismfall::Bosses.process(self)`, leaving `st.pending = :break` stuck until after the player's next attack deals 0 damage.
   - **Fix:** Call `Prismfall::Bosses.process(self)` right after `prismfall_bosses_pbOnBattlerEnteringBattle`.

5. **All Ch19 War Partner & Tag Partner AI Field Plays (`Marisol v19`, `Sigrun v19`, `Juno`, `Kestrel`) Are Dead Code**
   - **File:** `plugins/Prismfall Field Effects/012_FieldEffects_TrainerPlays.rb:153-156`
   - **Cause:** `return nil if !battle.opponent || (battler_index & 1) == 0` excludes player-side AI tag partners at even index `2`!
   - **Fix:** Replace `(battler_index & 1) == 0` with `battle.pbOwnedByPlayer?(battler_index)`.

6. **All Room Flashes (`NEON_GRID`, `STORMFRONT`, `BLEED`, `PRISM_ARENA`, `COLOSSEUM`) Are Invisible Behind HD Battlebacks (`img000`)**
   - **Files:** `plugins/Prismfall EBDX Bridge/003_Bridge_EBDX.rb:446-468`, `002_Bridge_Core.rb:156-160`
   - **Cause:** `prismfall_update_flash` tints only `@sprites["bg"]`, which is completely occluded by `@sprites["img000"]` whenever `*_hd.png` exists (all 6 flash fields have `*_hd.png`).
   - **Fix:** Apply and reset flash `Color` on both `@sprites["bg"]` and `@sprites["img000"]`.

7. **`010_Bridge_VersusIntro.rb`: Non-EBDX Boot Crash, 786 KB Bitmap Leak per Cast Fight & Unprotected State**
   - **File:** `plugins/Prismfall EBDX Bridge/010_Bridge_VersusIntro.rb:132, 307-320, 434-439, 460-569`
   - **Causes & Fixes:** (a) Wrap `L460-569` in `if defined?(EliteBattle) && defined?(DynamicTrainerSprite)` so vanilla fallback doesn't `NameError`; (b) dispose `@s["world"].bitmap` (`snap_screen`, 786 KB) inside `dispose`; (c) wrap `Sequence#play` in `begin ... ensure; dispose; end`; (d) `.dup` `EliteBattle.get_vector(:ENEMY)` on `L486`; (e) reset `PrismfallVS.hold_pose = false` on `:on_end_battle`.

8. **Double-Battle Z-Move Spread→Single Target Loss & Taunt Turn-Waste on `Extreme Evoboost`**
   - **File:** `plugins/Prismfall Z-Power/003_ZPower_Battle.rb:42-45, 78-85, 98-112, 175-188`
   - **Cause:** `pbFightMenu` checks `moves[idxMove].pbTarget` instead of swapped `@choices[idx][2]`, skipping target choice when Z-boosting spread moves (`Surf`, `Earthquake`, `Dazzling Gleam`, etc.) in Doubles; and Taunt allows Physical `Last Resort` → Status `Extreme Evoboost`, wasting the turn.
   - **Fix:** Reject Status Z-moves under Taunt in `zmove_for`/`status_z_exempt?`, and resolve target selection from `@choices[idxBattler][2]` after `pbRegisterMove`.

---

### A2. Built RXDATA Maps, Geometry, Warps & Story Progression Softlocks (8 P0 Bugs)

9. **Map `546` (`Thistledown Manor`): Portrait Gallery Dungeon (`D5`) Walled Off by Furniture (BFS-Verified Softlock)**
   - **Files:** `mapgen/layouts/manor.py:137, 212-213` → `maps_out/Data/Map546.rxdata`
   - **Cause:** `put('mn_clock', 23, 8)` (`(23,9)` solid) + `put('mn_sheet_tall', 22, 9)` (`(22,10)` solid) seal the sole 1-tile doorway `(19..21, 9)` into the West Portrait Gallery — softlocking `D5`, `Map 547` (Attic), and `EL_THISTLEDOWN`.
   - **Fix:** Relocate `mn_clock` (e.g. `(25, 8)`/`(32, 8)`) and `mn_sheet_tall` (e.g. `(35, 9)`).

10. **Map `145` (`Pageant Hall`): Solid Curtain Tiles Seal Both Backstage Wings (Locks Out Cantor Vesper & Eevee Octave!)**
    - **Files:** `mapgen/layouts/saltmere_interiors.py:89, 117-118` → `maps_out/Data/Map145.rxdata`
    - **Cause:** `NM(912)`/`NM(914)` (`passage=15`) cover `x=11, y=4..8` and `x=26, y=4..8`, sealing off the wing openings at `y=7..8` and blocking Vesper, Lyra, Eevee, `S190`, and `CR_OCTAVE`.
    - **Fix:** Skip `y=7..8` when placing `NM(912)`/`NM(914)` (or make both tiles passable overhead).

11. **Map `528` (`Marram Down`): North Dune Stairs Placed on South Beach (`max(y)` Bug — Isolates 10 Events)**
    - **Files:** `mapgen/layouts/routes_craft.py:259, 280-285` → `maps_out/Data/Map528.rxdata`
    - **Cause:** `max(y for y in range(H) if m.ht[y, x] == 1)` hits the south beach foredune (`y=53..56`) instead of the north dune belt (`y=21..26`), leaving Saltmere Beacon, Beacon Keeper heal, Sledge Run, 2 trainers, and 4 items completely unreachable.
    - **Fix:** Restrict `range(H)` → `range(40)` on lines `281` and `285`.

12. **Chapter 5 (`Lumen City`) — 3 Interlocking Softlocks + 5 Missing PBS Trainers**
    - **Files:** `mapgen/layouts/story_ch5.py:188-208`, `mapgen/layouts/lumen_interiors.py:121, 167, 239, 265, 269, 309, 332-340`
    - **Bugs:**
      1. Nothing ever sets `V125 = 10`, permanently blocking `Map608 Ev17 ('Testimony')` (`:ch5_lowlight_testimony`, `S115 CH5_MANDATE`, `V125 = 11`). Set `V125 = 10` at end of `Map608 Ev13` or `Ev15`.
      2. All 3 routes back into `Map 952` (`Plate Vault`) lock at `V125 >= 9` and `Map608` has no return warp at `(48,4)`, permanently blocking Larch's 3 a.m. scene (`V125 = 11 → 12`). *(Nothing sets `V125 = 13` either.)*
      3. `Map952 Ev2` calls undefined `pfm_cutscene(:SH1)` (silently swallowed by `rescue nil`).
      4. All 5 Ch5 Gala/Service-Lift trainers (`RIVAL_JUNO,13`, `HOLLOW_THISTLE,1`, `HOLLOW_GRUNT_M,5`, `HOLLOW_GRUNT_F,5`, `HOLLOW_GRUNT_M,6`) are missing from `pbs/trainers*.txt`, silently skipping all 3 fights (`012_Lumen.rb:26-44`).

13. **Map `255` (`Cindervault - Tap Chamber`, Ch8): Off-by-One Gate, Wipe-Softlock & Premature `:once` Lock**
    - **File:** `mapgen/layouts/cindervault.py:80, 89, 99, 112, 129` (`255_cindervault_tap.yaml:36..138`)
    - **Cause:** (a) Autorun requires `CH8_STEP >= 6` instead of `>= 5` (`6` is set at the end!); (b) `Self:A = ON` runs outside both battle checks so wiping permanently bricks Ch8; (c) `pf_choose(:ch8_caldera, ...)` (`:once => true`) fires *before* the branch fight.

14. **Unchecked `{'boss': ...}` & Wild Battles Allow Wiping/Fleeing to Skip Multi-Bar Bosses**
    - **Files:** `mapgen/rpg.py:214-221`, `deepwood.py:258-274` (`548` `:GLASS_MATRIARCH`), `lumen_interiors.py:320-329` (`952` `:OVERCHARGED`), `story_ch5.py:168-170` (`181` `Rotom` junction boxes)
    - **Cause:** `rpg.py` compiles `{'boss': ...}` as a bare `355` script command rather than an `if` branch checking `wild_battle`'s return value — wiping still runs post-boss story flags/awards before blackout transfer.

15. **2 Unguarded Live Warps to Unbuilt Maps (`Errno::ENOENT` Crash on Step)**
    - **Files:** `mapgen/specs/582_lumen_west_gate.yaml:15-17` (`Ev2 → Map 593`) and `mapgen/specs/255_cindervault_tap.yaml:18-20` (`Ev1 → Map 249`). Guard both with `pbRgssExists?`.

16. **`G4_SPLICE` Switch ID Split-Brain (`S325` vs `S422`) Stomps Gym 5's Reserved Block**
    - **File:** `mapgen/puzzles/circuit.py:28` hardcodes `S_SPLICE = 325` (Gym 5 block `325..329`) instead of `mapgen/flags.yaml:61`'s `G4_SPLICE = 422`.

---

### A3. Economy, Trials, Cameos, Encounters & Core Unlocks (7 P0 Bugs)

17. **Bicycle Is 100% Unobtainable (`GALAINVITATION` Bag-Check Mismatch)**
    - **Files:** `mapgen/layouts/lumen_interiors.py:85, 379` (`187_glide_cycles.yaml:19`)
    - **Cause:** `pfm_item(:GALAINVITATION, ...)` stores non-PBS items in `PrismfallMaps.flags[:story_items]`, while Glide Cycles checks `$bag.has?(:GALAINVITATION)`.
    - **Fix:** Use `pfm_has?(:GALAINVITATION)` (and/or define Prismfall story Key Items in `pbs/items_prismfall.txt`).

18. **Trial-Board Softlock Bug: 2 Instant Softlocks + 14 Cancel-Softlocks (Bricks 5 Eevee Octave Singers / `EEVIUMZ` & 7 Mega Stones!)**
    - **Files:** `plugins/Prismfall Trials/150_Trials_Talk.rb:141, 151-154`, `008_Trials_Board.rb:66-67`
    - **Cause:** (a) Hardcoded `scene == :offer` immediately softlocks board-accepted `EL_LAST_PLANK` (scene `:berth`) and `NA_BEDSIDE_MANNER` (scene `:corvin_offer`, Audinite); (b) `set_flag(qid, :from_board, false)` runs **before** `Script.run_scene`, so pressing Cancel/"No" at the giver permanently bricks 14 quests (`EL_OCTAVE_MOSS`, `ZE_OCTAVE_OFF_BEAT`, `OS_OCTAVE_NOON_BELL`, `AS_OCTAVE_TOO_LOUD`, `AN_OCTAVE_STILL_WATER`, `EL_LAMP_LENS`, `EL_DOLL_WHO_WAITED`, `EL_OLD_PINCER`, `ZE_RETURN_TO_SENDER`, `AS_OLD_CINDER`, `NA_MOON_MARKET_DOGS`, `NA_BEDSIDE_MANNER`, `ZE_FORM_7B`, `IS_SKALDS_SAGA`).
    - **Fix:** Set `:from_board` for all board quests, match `cond.include?("quest_state(:SELF) == :available")`, and clear `:from_board` **only after** `run_scene` advances the quest step/state.

19. **Losing to Shelly (`Map 525`) Permanently Bricks `EL_SHELLY`, Ledger Cameo & Leaves Party Fainted**
    - **Files:** `mapgen/specs/525_gossamer_deepwood.yaml:69-76, 106-113`, `plugins/Prismfall Core/023_Cameos_HPBoost.rb:19-34`, `541_grey_saltings.yaml:221-227`
    - **Cause:** `cameo_battle` sets `canLose` without healing on loss, and `525` ignores the return value and unconditionally sets `selfswitch A = true` (deleting Shelly forever without firing `:prismfall_cameo_beaten`). Same unchecked flee/loss issue on Glassed Masquerain (`525:106-113`) and Crabrawler Ring (`541:221-227`).

20. **Zero `HeadbuttTree` / `pbHeadbutt` Events Exist — 5 Entire Wild Lines Unobtainable (+ Dead `541` RockSmash Table)**
    - **Files:** `pbs/encounters.txt:86-96, 197-207, 392-395`, `mapgen/build.py:250-282`, `521_windfall_row.yaml:167`
    - **Impact:** Coll teaches Headbutt, yet zero headbutt trees exist anywhere — making **`AIPOM`, `BURMY`, `CHERUBI`, `KARRABLAST`, `SHELMET`** (and Badge-2 `SHUCKLE`) 100% unobtainable. Map `541` also defines a `RockSmash` table with zero breakable rocks.

21. **All 12 Passwords Unreachable Outside Debug & `Difficulty.change_menu` Unexposed**
    - **Files:** `mapgen/specs/109_dovetail.yaml:46`, `plugins/Prismfall Core/020_Passwords.rb:4`, `001_Config.rb:105`
    - **Fix:** Call `Prismfall::Passwords.prompt` after `Prismfall.choose_difficulty` on `109`, and expose `Prismfall::Difficulty.change_menu` via PC / Options.

22. **Lumen City Missing Fly Destination (`pbs/town_map.txt:182`)**
    - **Fix:** Add `,,180,25,46` to `Point = 16,16,Lumen City`, and add a `MapMetadata` `HealingSpot` fallback in `maps_out/Plugins/Prismfall Maps/009_TownMap.rb:52-56` so every future town auto-enables Fly.

23. **4 Built-Map Mega/Trial Events Unplaced + 3 Duplicate Reusable TMs + Live Dev-Text Leaks**
    - **Unplaced on built maps (`trial_overlay.py`):** `HERACRONITE` (`524`), `EL_ENCORE` Lopunnite+Normalium Z (`154`), `IS_CAUSEWAY_MATRIARCH` Kangaskhanite (`560`), `WOODWARD_PINCER` giver half (`526`).
    - **Duplicate reusable TMs (Rank 3 vs sidequests):** `TM20` (`EL_ROOTWARD_WAKE`), `TM28` (`OS_UNOWN_MURALS`), `TM48` (`AN_ECHO_HALL`).
    - **Live dev-text leaks:** `113_Quests_Octave.rb:290` (`"(new map 606, off Sunbleach Flats 613; 215 is the Gym 5 Mastery)"` prints inside the Trial Board UI!); `522_glassed_orchard.yaml:1079` (`"[item data missing: GLASSAPPLE]"`); literal `[TODO story]` on `101, 146, 147, 161, 280, 281, 285-287, 295`; `:KELPTEABAG` (`121:822`) vs `:KELPTEA` (`182:21`).

---

## PART B — P1 Mechanics, Evolution/Mart Availability & Wiring Mismatches

### B1. Field Effects & Z-Power Mechanics Gaps (`design/FIELDS.md` Parity)
- **`Aurora Veil` (`:weather_as => :Hail`) fails under Rain/Sun/Sandstorm (`006_FieldEffects_BattleHooks.rb:46`):** Breaks Rainbow's signature mechanic (Rainbow is literally started by Rain+Sun!). Return `@fe_weather_as` unconditionally when set inside `with_weather_as`.
- **4 `"never misses"` fields code `:set => 100` instead of `:always_hit => true`:** `120_HollowCathedral:66` (`WILLOWISP`), `121_Factory:43` (`METALSOUND/SCREECH`), `123_NewMoon:59,96` (`NIGHTDAZE` — even nerfed to 80–90% by New Moon's own blind proc!), `124_FairyTale:56` (`SWEETKISS`).
- **Wildfire early-douse stale fuel (`137_Field_Wildfire.rb:85-101, 134-137`):** Dousing Stage 1 early doesn't reset `st[:fuel] = 4`, so re-igniting burns out in 1 turn.
- **Stale Mirror Glass evasion text (`140_Field_GlassDunes.rb:40-41, 209, 285`):** Still promises removed Double Team/Flash amplification in `:notes` & `design/FIELDS.md:1014,1032`.
- **Backwards Cave collapse text & post-flood Cinderglass steam leak:** `130_Field_Cave.rb:15-24, 91-92` prints *"dust settles"* before *"ceiling gave way"*; `109_Field_AshenWaste.rb:102-115` missing `next if FieldEffects.lingering?(battle)`.
- **Quick 1-line mechanics fixes:** `004:235,272` use `move.pbCalcType(user)` for `-ate`/`Normalize`; `120:31,67` prevent `OMINOUSWIND` stacking to 3.0×; `003_Mega_Fields.rb:76-82` rewind Frozen Lake `:thaw` too; `106_Desert:13` add `:VCREATE`; `010_FieldEffects_Extensions.rb:317` hook `pbCanSleepYawn?` for Neon Grid; `008_Bridge_Transitions.rb:106,242` preserve `@pftr_zoff` during defocused refresh; `002_ZPower_Moves.rb:34` add Gen 7 BP overrides for variable-power `Power = 1` moves (`Grass Knot`, `Low Kick`, `Gyro Ball`, `Heavy Slam`, `Return`, `Eruption`, etc.).

### B2. Evolution, Mart & Pokédex Availability Gaps
- **Zero `LINKINGCORD`, zero `DUSKSTONE`/`DAWNSTONE`, zero Stone Shop until Badge 18 postgame:** Traps Dorian's Badge-1 gift Eevee, `Ralts → Gallade` (`GALLADITE`), `Misdreavus`, `Murkrow`, `Honedge`, `Litwick`, plus **30+ zero-source evo items** including already-wired EventMon evos (`UPGRADE`/`DUBIOUSDISC` for `ZE_PORYGON`, `AUSPICIOUSARMOR`/`MALICIOUSARMOR` for `AS_CHARCADET`, `CRACKEDPOT`/`UNREMARKABLETEACUP` for `Sinistea`/`Poltchageist`, Apples, Sweets, `RAZORCLAW`/`FANG`, `PRISMSCALE`, `METALALLOY`, and single-player `FINIZEN → PALAFIN`).
- **Missing promised Ch1–5 Pokédex gifts & Fossil Lab revival:** `ABRA` gift missing from `150–154` (makes `ALAKAZITE` unusable); `PANSEAR/PANPOUR/PANSAGE` missing from `552`; Lumen Fossil Lab (`188`) has no revival script despite `OLDAMBER` placed on `545` and required by `OS_AMBER_AGAIN` (Aerodactylite).
- **Zero Field Seeds sold anywhere** (all 7 built Marts are bare stock `template: mart`, contradicting Ferrow clerk's *"The Seeds are new"* at `101:1469`), **zero `EXPALL`** (despite `"noexpall"` password), **zero Move Relearner/Deleter/Name Rater**, and `RARE_CANDY_EVOLVES_AT_CAP = false` (`001_Config.rb:82`) trapping friendship/move evolutions at cap.
- **Badges 5–7 encounter overlay gap** (`pbs/encounters_badgetiers.txt` has 0 entries for Badges 5–7, plus stale comment at `L309-311`).

### B3. Map Audio, Sprites, Portraits & Metadata Wiring
- **Unlock `:surprised` in `014_Portraits.rb:59-70` (all 31 live cast already have `*_surprised.png` on disk!):** Instantly fixes 4 Saltmere `:surprised` tags (`saltmere_rj.py:486, 536, 553, 557`). Also add `COLL`, `SHELLY` (cameos), and `ACCORD_GUARD` to `CAST` (`L86-96`).
- **Spark the Pichu invisible (`story_ch5.py:134, 209`):** Uses `'Followers'` instead of `'Followers/PICHU'`.
- **Dead-silence map BGMs & missing `'Anim/'` SE prefixes:** `Map 126` (`bgm: Briarwick`) and `Map 168` (`bgm: Ebbmouth`) point to nonexistent files; `Map 186` (Ch5 Gala climax!) has `bgm: ''`; `522:1031` (`Ice 1` → `Anim/Ice1`) and `circuit.py:370,416` (`Thunder1`/`Paralyze1` → `Anim/...`).
- **Sync `FIELD_DEFAULTS.yaml` / `011_FieldEffects_MapDefaults.rb` / `design/maps.json` / `system_prismfall.txt`:** Add built maps `134, 255, 951, 952` (and `126, 148, 168, 990`); re-run `export_tilesets_rxdata.py` so `system_prismfall.txt` includes `V124–V134`, `S221–S232`, `S320–S324`, `S521–S524`.
- **10 more isolated outdoor maps missing `SnapEdges = true`:** `146, 147, 280, 285, 525, 563, 568, 579, 608, 929`.
- **Event placement fixes:** `Map 548 @(4,15)` Juno overlaps `Veil 2` (`deepwood.py:184,230`); `Map 167 @(37,28)` Ch4 Super Potion stranded on water-locked cell (`ebbmouth.py:252`); `Map 255` post-Ch8 actors lack vanish page; `gen_playhouse.py:259` `${1}` → `₽{1}`.

---

## PART C — P2 High-ROI Wednesday Polish & Quality Upgrades

1. **In-Battle Field Manual Hotkey (`009_FieldEffects_FieldNotes.rb`):** Bind a 1-key in-battle Field Notes overlay (`AUX1`/`SPECIAL`) showing active field, current stage, seed effect, boosts/nerfs & transitions + register `:FIELDNOTES` as a usable Key Item.
2. **Lumen Arcade 1F (`183`) Tactical Specialty Mart + Ferrow Mart Seeds (`102`):** 4 badge-gated clerks (Standard Mart, Stones + `LINKINGCORD` + Evo Items, Field Seeds, Nature Mints / EV Power Items / EV Berries / Exp Candies) + single-player `FINIZEN` evo rule.
3. **Zero-Friction Team Building:** Grant `:EXPALL` in Ch1 Tidewatch (`103`), flip `RARE_CANDY_EVOLVES_AT_CAP = true` (+ check level-up evos after cap battles), add gold `CAP` indicator & IV/EV readout on Party/Summary, add Party "Relearn Move" / Move Deleter + free HM forget, and add a repeatable Exp-Candy sparring NPC in Pokémon Centers.
4. **Smarter Gym & Boss Battle AI:**
   - **Quent Turn-2 Trick Room fix (`012_FieldEffects_TrainerPlays.rb:88`):** Add `:no_trick_room` so Quent doesn't cancel his own Trick Room on Turn 2; switch Nyx/Celestine `:FAKEOUT` (`L83-84`) from `:first_turns` to `:first_turn_out`.
   - **Smart Z-Move AI (`003_ZPower_Battle.rb:114-137`):** Don't burn once-per-battle Z-Moves into immunities, Disguise, or 1-HP foes already KO'd by the base move.
   - **Boss Multi-Bar AI awareness (`004_Bosses_Battle.rb`):** Suppress low-HP withdrawal & pointless `Recover` spam when `bars_left > 1`.
   - **Wire `AIField.battler_affinity` (`007_FieldEffects_AI.rb:194-215`) into switch-in scoring** + fix `:even_if_failed` ordering (`007:126`), Frozen Lake `:thaw` detection (`012:125`), and Inverse EOR calculation (`007:100`).
5. **Quest Log & Z-Move Confirm UX:** Show `q[:where]`, `q[:rec_level]`, reward preview, and "X pts to next rank" in `009_Trials_QuestLog.rb` (and expand clipped 72px detail box); show computed BP & category in Z-Move confirm (`003_ZPower_Battle.rb:106`).
6. **Clean Polish & Automated Regression Guards:**
   - Skip the 1.6s `POSE_SECONDS` input freeze on 1-frame generic trainers (`010_Bridge_VersusIntro.rb:540-546`); remove Arceus's duplicate Plate-shift message (`103_Boss_Arceus.rb:98`, `:form_message => ""`); clean 7 `ruby -wc` unused locals (`125:11`, `139:22`, `140:40-41`, `010:161`, `012_Sheet_Effects:270,353`).
   - **Add a post-paint within-map BFS reachability check to `mapgen/build.py`** (automatically prevents future `546`/`145`/`528`-class softlocks in <1s).
   - **Add 5 harness tests** (`tools/harness/run_all.rb` + `validate_fields.rb`): Arceus bar-break `:prism_turn` + `:prism_interval`, `calc_stats(nil, true)`, lethal `:on_entry`/seed/`Corrosive Mire` fainting, tag-partner slot-2 AI field plays, and `"never misses"` vs `:set => 100` lint.

---

## PART D — Universal 65-Edge Staged Field Transitions & Signposting (Creator-Requested)

**Problem Verified (`001_Bridge_Config.rb:61-128`, `008_Bridge_Transitions.rb`, `art/battlebacks/transitions.py`):**
- Prismfall has **65 total mid-battle transitions** (**46** `Field → Field` + **19** `Stage → Stage`), yet currently **only 1** (`:glass_quench`, `DESERT`/`FLOODED_DUNES` → `GLASS_DUNES`) uses `008_Bridge_Transitions.rb`'s in-room staged wave-front — AND its pre-sliced `rv00..rv15` PNGs were cut from the old procedural `fields_g` desert glass (causing a visual pop onto our new pure-Gemini `field_glass_dunes_hd.png` at `t = 1.5s`!).
- All other 64 transitions (including `MEADOW`/`SILKWOOD`/`FLOWER_GARDEN` → `WILDFIRE`, `WILDFIRE` → `MEADOW`, `VOLCANIC` → `ASHEN_WASTE`, etc.) currently fall back to a flat 8-frame solid-color flash with zero pre-break visual warning on multi-hit counters (`uses >= 2`).

### 1. Generalize `008_Bridge_Transitions.rb` to 8 Reusable Elemental Presets (Covers 65 / 65 Edges!)
Instead of storing 65 separate pre-sliced `rv00..rv15` PNG folders, generate **reusable directional alpha-mask strips** (or mask the live target `field_<dst>_hd.png` `Bitmap` in memory at swap start using 4 geometric wave archetypes: radial ground-first spread, jagged fracture web, sweeping flood crest, prismatic distortion wipe). That keeps total disk footprint tiny (~4 MB) **and guarantees zero stale-art mismatch whenever any `_hd.png` backdrop is updated by Gemini**!

| Preset | Visual Wave-Front Signature | Exact Edges Covered (All 46 Field→Field + 19 Stage→Stage) |
|---|---|---|
| **`:wildfire_sweep`** | Fiery orange-amber combustion front (`#FF781E → #B43C14`), ember rim, rising smoke/sparks | `MEADOW`/`SILKWOOD`/`FLOWER_GARDEN` → `WILDFIRE`, `WILDFIRE` S2→S1, `ASHEN_WASTE`/`CAVE`/`MOUNTAIN`/`SNOWY_MOUNTAIN` → `VOLCANIC`, `DRAGONS_DEN` S1→S2 (Wyrmfire), `CAVE`/`FAIRY_TALE` → `DRAGONS_DEN` |
| **`:glass_quench`** | White-hot leading rim (`#FFFCEC`), amber cooling body, jagged glass veins, steam bursts *(re-read live `field_glass_dunes_hd.png`!)* | `DESERT`/`FLOODED_DUNES` → `GLASS_DUNES`, `GLASS_DUNES` S1⇄S2 (Mirror) |
| **`:flood_surge`** | Foaming sapphire/teal crest wave (`#4CC8FF → #1A6CA8`), white spray/steam puffs | `DESERT`/`GLASS_DUNES` → `FLOODED_DUNES`, `BEACH`/`ASHEN_WASTE`/`CORROSIVE_MIRE`/`FROZEN_LAKE`/`UNDERWATER` → `WATER_SURFACE`, `WATER_SURFACE` → `UNDERWATER`, `WILDFIRE` S1→S2 (Embers), `VOLCANIC` → `ASHEN_WASTE` (heavy white steam quench) |
| **`:frost_creep`** | Geometric ice-blue frost veins (`#D8F6FF → #6BC8FF`) spiderwebbing outward, frost motes | `WATER_SURFACE`/`FLOODED_DUNES` → `FROZEN_LAKE`, `MOUNTAIN` ⇄ `SNOWY_MOUNTAIN` |
| **`:bloom_wave`** | Emerald-gold / rose-petal wave (`#C8FFAA` / `#FFE6F0`), drifting petals & sunbeams | `MEADOW` → `FLOWER_GARDEN`, `WILDFIRE`/`WASTELAND` → `MEADOW`, `DESERT` S1→S2 (Superbloom), `FLOWER_GARDEN` S1..S5, `STORMFRONT` → `RAINBOW`, `DRAGONS_DEN` → `FAIRY_TALE`, `HOLLOW_CATHEDRAL` S1→S2 (Consecrated) |
| **`:quake_shatter`** | Jagged stone/earth fissures (`#D4B07A` / `#FF9628`), debris puffs, brief micro-shake | `FACTORY` ⇄ `SCRAPYARD`, `COLOSSEUM`/`CRYSTAL_CAVERN`/`DARK_CRYSTAL`/`DRAGONS_DEN` → `CAVE`, `CAVE` S1⇄S2, `COLOSSEUM` S1⇄S2, `GLASS_DUNES` → `ROCK`, `FAIRY_TALE` → `STEEL` |
| **`:blight_miasma`** | Oozing toxic violet-chartreuse ripple (`#A855F7 → #4ADE80`) + rising acid-mist bubbles | `WATER_SURFACE` → `CORROSIVE_MIRE`, `CORROSIVE_MIRE`/`SCRAPYARD` → `WASTELAND`, `DESERT` S2→S1 |
| **`:rift_eclipse`** | Prismatic crimson/violet/cyan glass-shard fracture wave + dim-out pulse | `GLASS_DUNES` → `BLEED`, `MINDSCAPE`/`HOLLOW_CATHEDRAL` → `INVERSE`, `MINDSCAPE` S1⇄S2, `CRYSTAL_CAVERN` ⇄ `DARK_CRYSTAL`, `NEON_GRID` S1⇄S2, `NEW_MOON` S1⇄S2⇄S3, `HOLLOW_CATHEDRAL` S2→S1 |

### 2. Two High-Clarity In-Battle Visual Signposting Additions
1. **Multi-Hit Pre-Break Warning Emitter (`uses - 1` hits reached):** Across the 36 multi-use transitions (`uses >= 2`), whenever a counter reaches **1 hit remaining** (e.g., `MEADOW` Hit 1 `"Sparks are catching... (1 more)"`, `FROZEN_LAKE` crack `"1 more"`, `CAVE` tremor `"1 more"`, `FACTORY` overload `"1 more"`), attach a lightweight temporary warning particle emitter matching the impending preset (drifting sparks, spreading frost motes, falling pebbles, rising steam, glitch shards) until the transition fires or resets.
2. **Brief Field-Transform Toast Banner + CC0 SE:** Right as the staged reveal completes, slide a clean 1.2s non-blocking top banner (e.g. `"FIELD → WILDFIRE (Blaze)"` / `"STAGE 2 → CINDERGLASS"` with preset accent stripe) paired with the matching `Audio/SE/` effect (`Glass Quench`, `Field Shatter`, `Prism Arena Swell`).

### 3. Paired Gemini Art Queue (Next Image-Quota Reset ~11:13 PM PST)
Gemini will pair this with matching pure-Gemini battlebacks so every major cross-field transition stays visually locked:
- **`WILDFIRE` + `WILDFIRE_EMBERS`** built directly from `field_meadow_hd.png`'s exact rolling Elowen horizon (seamless `MEADOW → WILDFIRE → EMBERS → MEADOW` cycle!).
- **Creator-requested Art Studio reworks:** Bone-free Pokémon-world **Ossaria Desert 5-pack** (carved Relic/sandstone ruins & mesas, locked horizon) + fully rethought symmetrical vaulted **Hollow Cathedral 2-pack** (removing floating wood planks & stubby back arches) + remaining **`NEW_MOON_LAMPLIGHT` / `NEW_MOON_ABYSS`**.

---

## PART E — Core, Cutscenes, Puzzles, Tileset RXDATA & Save-Migration Audit (Verified Deduplicated Pass)

### E1. Additional P0 Crashes, Softlocks & Cross-Save State Leaks
1. **`Tilesets_prismfall.rxdata` Missing Tilesets `59`, `60`, `61` → Instant `NoMethodError` Crash Entering ALL 18 Builder 14–16 Maps (`Map 546/547`, `Map 180/181/185–193`, `Map 582`, `Map 608`, `Map 951/952`, `Map 255`):**
   - Verified via Ruby `Marshal.load`: `maps_out/Data/Tilesets_prismfall.rxdata` only contains keys `[30, 33, 34, 40, 50..58]`, omitting `59` (Manor), `60` (Lumen/Gym 4), and `61` (Ch8 Cindervault Tap) defined in `maps_out/tilesets_prismfall.json`. Also missing `S325`, `S423`, `S424` and `V125`, `V129`, `V521` in `system_prismfall.txt` (permanently locking Gym 4 & Lumen blackout).
   - **Fix:** Re-run `python3 -I mapgen/export_tilesets_rxdata.py` and gate packaging with `--check`.
2. **Brinecut Mine 1F (`Map 544`): `pfm_cart_ride` Never Enables `$game_player.through = true` → 100% Progression Softlock (`011_Caves.rb:58-77`):**
   - `"Ride cart"` has `through = true`, but `$game_player` has `through = false`, so the player stalls on the south side of the impassable row `y=21` chasm while the cart parks across the gap (blocking B1F ladder & Thistledown Lea exit). Branch `"D"` (`L76`) also skips `wait_moves(pl)` and Juno follower isn't resynced.
   - **Fix:** Wrap `pfm_cart_ride` in `was = pl.through; begin; pl.through = true; ... ensure; pl.through = was; pl.opacity = 255; $game_temp.followers.put_followers_on_player if $game_temp.respond_to?(:followers); end`.
3. **Tidelock Basin (`Map 171/172/173`, `:g3_basin`): Reset Teleports Player Into Solid Wall `(14, 21)` + Broken Cross-Map Reset/Skip (`007_PuzzleRooms.rb:160-168`):**
   - On `Map 171`, `(14, 21)` is impassable tile `505` (`0x0f`), permanently trapping the player on `"Reset this room"`. Also resetting on `172/173` doesn't swap back to `171`, and `"Skip this room"` doesn't move the player to `173` / north pier.
   - **Fix:** Change `:start => [14, 22, 8]` (passable on all 3 maps) and add map-swap `:proc` hooks to `:reset` (→ `171`) and `:solved` (→ `173`).
4. **Rock Climb (`022_RockClimb.rb:30-42`) Never Sets `$game_player.through = true`:**
   - Comment promises `"ignoring passability"` and `L40` resets `through = false`, yet `through = true` is never set before `pbMoveRoute($game_player, [FORWARD]*steps)` → fails in place or hangs `while $game_player.move_route_forcing` on every cliff. Wrap with `begin/ensure` + follower resync.
5. **`monotype` Password Crashes Battle Start When Party Has 0 Matching-Type Mons (`020_Passwords.rb:173-178, 209-214`):**
   - `monotype_blocks?` stays `false` out of battle, then marks the entire starter party `able? == false` once `in_battle = true`, crashing `pbStartBattleCore` on 15/18 types. Guard against emptying the entire party.
6. **Cutscene `slowmo(0.0)` Permanently Deadlocks Cutscene & Skip (`012_Cinematic.rb:544-550`, `006_Scene.rb:201-204, 235-248`):**
   - `dt *= @timescale` freezes `@time` forever on `0.0` (blocking Skip too), and skipping during `slowmo(0.2)` stretches fade 5×. Clamp `scale = [a[:scale].to_f, 0.01].max` (or track slowmo on wall-clock `dt`) and reset `@timescale = 1.0` in `begin_ending`.
7. **Thistledown Manor (`Map 546`): `:d5_dining` Reset Permanently Loses Dropped Armchairs + Stale `PFManor.@zone` Across Save/Load (`007_PuzzleRooms.rb:177-184, 217-218, 255-258`):**
   - Reset clears `S521/S522` but not self-switch `"A"` on `"Armchair d1"/"d2"` and omits `:proc => proc { PFManor.reset_room("d") }`. Clear `@zone` on save load / new game.
8. **Circuit Gym (`Map 190–192`): `PFCircuit.power` Unconditional Recursion on `:alarm` (`SystemStackError`) + Stale Skip State (`007_PuzzleRooms.rb:386-390, 458-460`):**
   - Only recurse when `!quiet`, and attach `:solved[:proc] = proc { PFCircuit.power(mid, true) }` to `:g4_190..192`.
9. **Module-Level State Leaks Across Save/Title (`005_MapAtmosphere.rb:133-141`, `005_Puzzles_Hooks.rb:28-46`) + `Ledger.write` Silent `ENOENT` Before First Save (`016_Ledger.rb:61-65`):**
   - Reset `@last_tone_map`/`@tone_was_set` (also in `pfm_dusk`/`pfm_day`) and `@prev_pos`/`@prev_map`/`@last_step` on save load/new game; `mkdir_p(File.dirname(path))` in `Ledger.write` before opening `.tmp`.

### E2. Additional P1 Runtime & Edge-Case Fixes
- **Partner Difficulty Remap Backward (`004_Difficulty.rb:126-137, 172-176`):** `pbLoadTrainer` remaps `pbRegisterPartner` (`MERIDIAN_QUENT` on `Map 255`, `RIVAL_JUNO` in Ch11), **buffing** your ally on Hard (`+100`) and **nerfing** your ally on Casual (`+200`). Wrap `pbRegisterPartner` with a `Difficulty.without_remap` guard.
- **`Difficulty.apply_battle_rules` Bypasses Passwords (`004_Difficulty.rb:140-152`):** Use `setting(:trainer_bag_items)` / `setting(:force_set_style)` instead of `mode[...]`.
- **`Festival.over_limit` Blocks `nocap` Players (`009_Festival.rb:266-269`):** Add `return [] if !Prismfall::LevelCap.enabled?`.
- **`LevelCap.unlock_finale!` Leaves Cap Stuck at `96` (`005_LevelCap.rb:80-85`):** Clear `Prismfall.state.level_cap_override = nil`.
- **Exp/Rare Candy Max Coerces `0` to `1` on Lv 100 / Eggs (`005_LevelCap.rb:192-215`):** Add `next 0 if ret <= 0` before clamping.
- **`Endings.trigger` Doesn't End Active Interpreter Before `Scene_Credits` (`018_Endings.rb:64-70`):** Call `pbMapInterpreter.command_end if pbMapInterpreterRunning?` in the `if roll` branch too.
- **`Map 181` Lowlight Junction Boxes (`Ev 41–44`) Clear on Flee/Loss:** Gate `pfm_lumen_box(i)` & Self-Switch `"A"` on `WildBattle.start` win/capture.
- **`020_Passwords.rb` Unwired `:OPEN_BOOK`/`:SECOND_FERRY` + Traded Mons Bypass `:MONOTYPE` / Miss `:FULL_IVS` (`L43-54, 168-171`).**
- **`014_Portraits.rb:174-206` Colored Speaker Prefix Drops Carry Face + `@scene_faces`/`@last_face` Leak Across Saves:** Allow trailing color codes after `:` in `label_of`, and reset both ivars on save load/title.
- **`006_RivalStarters.rb:190-203` `swap_species` Wipes All 45 Hand-Crafted Rival Starter Movesets & Doesn't Reset `pkmn.ability = nil`.**
- **P2 Disposal & F12 Guard Cleanup:** Guard unguarded aliases in `012_Cinematic_Techniques.rb:62,80,112`, `012_Sheet_Effects.rb:34,129,379`, `010_JunoFollower.rb:142,253`; wrap `Scene.fade_back`, `FaceBox#initialize`, `Bubble#initialize`, `003_Puzzles_Movement.rb` (`ride`/`shift`), and `PrismfallLumen.tag` in `ensure`; resync followers in `web_fall` & `pfm_tide_surge`; ignore erased events in `004_Puzzles_Tracers.rb:46`.

---

## PART F — Act I–II Script Continuity & Exhaustive Tag-Ally Roster Audit

### F1. Act I–II Map / PBS / Script Contradictions to Clean Up
1. **Circuit Gym (`Map 190–192`) Builds With ZERO Gym Trainers (`mapgen/layouts/circuit_gym.py:57-61, 151, 182, 226`):** `trainer_if` silently skips all 6 Gym 4 trainers because they have not been added to `pbs/trainers.txt` yet — add the 6 Circuit Gym trainers to `pbs/trainers.txt` and rebuild.
2. **Ch5 Lowlight Veil (`story_ch5.py:197-206`, `Map 608`):** Drops Valen's crystal-hand reveal and uses a generic `Directorate Officer` instead of Director Marchetti's full scripted debut (`story/24_SCRIPT_CH5.md`) for two of the three testimony choices.
3. **Ch4 Maps (`570..174`) Still Pre-Script Stubs** compared to the finalized `story/23_SCRIPT_CH4.md` — sync Ch4 dialogue/events when updating Builder 13/14.
4. **`HOLLOW_TEO` v0 LoseText Spoils Unmasking Early (`pbs/trainers.txt:10139`):** `"Tell my sister— no. Don't tell her anything."` plays in Ch1 before Teo's identity twist; move/soften the v0 line.
5. **Lore/Timeline Text Fixes:**
   - **Meridian Spire Age 3-Way Contradiction (`story/24_SCRIPT_CH5.md`):** Line `344` (`"Ten years that Spire's been up there"`), Line `354` (`"Forty years I've fed the birds in the Spire's shadow"`), and Line `454` (`"Raised AF 271"` = 29 years ago) all conflict — pick ONE date (e.g. built AF 271 / 29 years ago, first Lattice switched on 10 years ago) and align `344`/`354`.
   - **Morwen Exile Cause (`story/25_SCRIPT_CH6.md:371`):** Says Morwen died `"Of the wilting"` — align with canon (`01_WORLD_LORE` / `03_CAST` Hollow/Bleed fate).
   - **Ch12 Juno Line Leak (`story/15_COMEDY.md:214`):** Gives Juno a puddle-reflection line in Ch12 when Juno is absent from Ch12's cast; reassign or shift to Ch11/Ch14.
   - **Route 1 Double-Backslash Portrait Leak:** Fix `'\\pf[...]'` literal markup in Ferryman's Mile (`520`) script source, plus Saltmere harbour wilting phrasing & Ch7 Festival season wording.

### F2. Exhaustive Tag-Battle Ally & Playable Roster (Art + Engine Wiring Sync)
- **Protagonists (2):** `PLAYER_A`, `PLAYER_B` → Gemini upgrading to **16f animated fronts** + **LEFT-HAND B2W2 5f back-throws**.
- **Core 7 Human Tag Allies (all 7 already have 16f fronts; Gemini building LEFT-HAND 5f `*_back.png`):** `RIVAL_JUNO` (+ `LEADER_JUNO`), `RIVAL_KESTREL`, `MERIDIAN_QUENT`, `LEADER_ANJA`, `LEADER_MARISOL`, `LEADER_ROOK`, `LEADER_SIGRUN`.
- **Cameo / Interlude (+2):** `FESTIVAL_VENAM` (Ch7 tag — needs 16f front + LEFT-HAND back-throw) and `WENLOW` (Ch16 Interlude IV playable — needs LEFT-HAND back-throw); also `LEADER_ROWAN.png` missing front for Festival `v90/190/290`.
- **Non-Human Tag Allies (2 — Engine Hook Needed):** `PARTNER_OGRE` (Ch10 Ogerpon — missing from `pbs/trainers.txt`, needs non-human partner sprite/trainer hook) and **Giratina** (Ruin Route R7).

---

## PART G — Field Effects (47 Files), Mega, Z-Power & EBDX Bridge Audit (100% Plugin Coverage Complete)

### G1. Additional P0 Gameplay / Mechanics Bugs
1. **`Gorilla Tactics` Z-Move Struggle Softlock (`plugins/Prismfall Z-Power/003_ZPower_Battle.rb:146-157`):**
   - `on_unleash` rewrites `@lastMoveUsed`/`@movesUsed` to `base.id`, but never updates `user.effects[PBEffects::ChoiceBand]`. A `Gorilla Tactics` Pokémon holding a Z-Crystal gets permanently Choice-locked onto `z.id` (not in its moveset), forcing Struggle until switch-out.
   - **Fix (`L156`):** `user.effects[PBEffects::ChoiceBand] = base.id if user.effects[PBEffects::ChoiceBand] == z.id`.
2. **`Dancer` Copied Moves Silently Dropped by ALL Field Transitions (`004_FieldEffects_Engine.rb:756-771`, `006_FieldEffects_BattleHooks.rb:11-25, 88-92`):**
   - `Oricorio`'s `Dancer` triggers via `pbUseMoveSimple` (bypassing `pbUseMove`), so `move_landed` sees the triggering move's `ctx[:landed] == true` and aborts — breaking `GRAND_STAGE` applause and all Dance field transitions (8 trainers in PBS!).
   - **Fix (`006`):** Wrap `pbUseMoveSimple` with `FieldEffects.push_move_use` / `ensure pop_move_use`.
3. **Two-Turn Moves Double-Count `uses >= 2` Field Transitions (`004_FieldEffects_Engine.rb:659`):**
   - `next if rule[:strike_turn] && user.effects[PBEffects::TwoTurnAttack]` only guards `:DIVE` (`WATER_SURFACE`/`UNDERWATER`), allowing `Meteor Beam`, `Shadow Force`, `Solar Beam`, `Solar Blade`, and `Freeze Shock` to count BOTH charge turn and strike turn (1-turning 2-hit transitions on `DARK_CRYSTAL`, `HOLLOW_CATHEDRAL`, `FLOWER_GARDEN`, `DRAGONS_DEN`).
   - **Fix (`004:659`):** `next if user.effects[PBEffects::TwoTurnAttack] && !rule[:on_charge]`.
4. **`Seismic Toss` on `COLOSSEUM` Silently Gets 1.0× Instead of Documented 1.5× (`112_Field_Colosseum.rb:11, 30, 42`):**
   - `FixedDamageMove` bypasses `pbCalcDamageMultipliers` (`:damage_mods`). Move `:SEISMICTOSS` out of `throws` into `:fixed_damage_mods => [{ :moves => [:SEISMICTOSS], :mult => 1.5, ... }]`.

### G2. Additional P1 Balance, Asset & EBDX Fixes
- **EBDX VS Intro `V` / `S.` Letters Park & Linger on Screen Edges (`010_Bridge_VersusIntro.rb:421-430` — Creator-Caught!):** At `t = HOLD_END + 0.22` (`x = 1.0`), `@v_home[0] - 220 ≈ +6 px` and `@s_home[0] + 220 ≈ 504 px` stop both letters *inside* the `512px` frame while opacity is tied to late vortex `k = ease_in(prog(t, +0.14, +0.46))` (`k = 0.0625` → **94% opacity!**), leaving `V` & `S.` parked on the left/right edges for `0.24s`. **Fix (`L425-429`):** Increase travel `220` → `360` and fade opacity on `x` (`@s["V"].opacity = @s["S"].opacity = (255 * (1 - x)).round`) so both shoot cleanly off-screen while fading out.
- **EBDX Double-Opponent Trainer Sprites Mis-Indexed (`007_Bridge_Placement.rb:67, 215-221`):** Iterates battler indices `1, 3` against `"trainer_#{i}"` instead of trainer indices `0, 1` (`each_with_index` fixes `"trainer_0"` never moving and `"trainer_1"` landing on slot 0!).
- **Missing `dbl_field_glass_dunes_mirror_{ally,foe}.png` (`007_Bridge_Placement.rb:115-122, 208`):** Only 2 missing double-base PNGs out of 108 — causes battlers to snap off-base when `GLASS_DUNES` shifts to Stage 2 in doubles; regenerate via `art/battlebacks/doubles.py` (+ Stage-1 fallback).
- **Casual K8 Kestrel (`v280–282`) Never Gets Morwen's Ring / Mega Scizor (`001_Mega_Config.rb:45`):** Casual K8 Scizor is Lv 85, below `:min_level => 90` → lower to `:min_level => 82`.
- **Field Logic Edge Cases:**
  - `112_Field_Colosseum.rb:20`: Gate `st[:kos]` accumulation on `FieldEffects.stage(battle) == 1` so Stage 2 KOs don't immediately re-trigger Frenzy on the turn it calms.
  - `113_Field_FlowerGarden.rb:35`: Exclude `:FIRE` from Stage-5 `blades` cut-back so `Bitter Blade` can actually ignite `WILDFIRE`.
  - `114_Field_FrozenLake.rb:64`: Add `|| FieldEffects.lingering?(battle)` so the shattering 3rd quake doesn't scatter Ice Spikes onto `WATER_SURFACE`.
  - `107_Field_CorrosiveMire.rb:47-49`: Split `:BARBBARRAGE` (`!b.pbHasAnyStatus?`) from `:VENOSHOCK` (`!b.poisoned?`) to stop 4× (540 BP) double-dipping vs burn/para/sleep/freeze.
  - `004_FieldEffects_Engine.rb:516-527`: Don't consume Field Seeds when `apply_battler_effect` returns `false`; `004:892`: honor Gen 9 `:COVERTCLOAK` on `:added_effects`.
  - `010_FieldEffects_Extensions.rb:100-112`: Let activated `Flower Gift` (`FLOWER_GARDEN` S4–5) boost allies in Doubles too.
  - `001_Prismfall_DebugMenu.rb:88`: Allow `field == :NONE` to actually pass `setBattleRule("field", :NONE)` instead of falling back to map default.
- **P2 Cleanup & Leak Fixes:** Cache `:bitmap` particles in `002_Bridge_Core.rb:235-238` and dispose `puffbmp` in `008_Bridge_Transitions.rb:260`; guard remaining 3 unguarded `alias` sites (`009_FieldEffects_FieldNotes.rb:114`, `012_FieldEffects_TrainerPlays.rb:182,196`); fix duplicate status-cure text (`004:434`, `pbCureStatus(!msg)`); use `ab = check_ability || @ability_id` in `006:114`; gate `137_Field_Wildfire.rb:35` `burn_down` on `FieldEffects.current(battle) == :WILDFIRE`; wrap `004_Bridge_Vanilla.rb:80-111` `fade` sprite in `ensure`.

---

## PART H — Exhaustive PBS Data Integrity, RXDATA Encounter Tiles & Scaling Audit (758 Trainers / 117 Maps Verified)

### H1. Additional P0 Dead Map Encounters & Unregistered Consumable/Story Items
1. **Two Built Maps Have 100% Dead Wild/Fishing Tables (0 Matching Terrain Tiles in `Map*.rxdata`):**
   - **`Map 608` (`The Lowlight (Shattered)`, `pbs/encounters.txt:966-979`):** Uses `Land,25` (12 species, sole base-table `LITWICK`/`DRIFLOON`/`PIKACHU`/`LUXIO`/`FLAAFFY`), but `Map608.rxdata` has **0 Grass/TallGrass terrain tiles** → change to `Cave,25` (step-anywhere ruin encounters) or paint Grass tiles.
   - **`Map 570` (`Frostwick`, `pbs/encounters.txt:656-670`, `encounters_badgetiers.txt:233-238`):** Defines 5 fishing tables (incl. early `FEEBAS` & `VELUZA` explicitly advertised by `140_BadgeTier_Rumours.rb:68-69`), yet `Map570.rxdata` has **0 Water terrain tiles** (Ice-only) → paint open-channel Water (`tag 7`) tiles or relocate rod tables + rumours.
2. **17 Custom Prismfall Items Missing From `pbs/items*.txt`:**
   - `:FIZZBOLT` (`story_ch5.py:128`) deducts **₽60** for 2 unusable drinks that never enter `$bag`; `:OLDCHOWDER` (`story_early.py:218`, "Restores 20 HP") & `:BRAMBLETART` (`L371`, "Restores 30 HP") never enter `$bag`; `:MOTHERLOOMSSHUTTLE` (`gen_loomhouse.py:160-161`) isn't even recorded in `flags[:story_items]` on Gym win; plus 10 more story Key Items (`APPLEWOODLOG`, `BADGECASE`, `BARKMASK`, `BLEEDSHARD`, `DUSKPETAL`, `FELLOWSHIPCARD`, `LAMPTAPER`, `LEDGERKEY`, `PROMPTERSSCRIPT`, `SANDSHOVEL`).
   - **Fix:** Add all healing foods (`Pocket = 2`, `FieldUse/BattleUse = OnPokemon`) and story Key Items (`Pocket = 8`, `Flags = KeyItem`) to `pbs/items_fields.txt` (or `pbs/items_story.txt`), and wire `gen_loomhouse.py:160-161` to `pfm_item`.

### H2. Additional P1 Trainer Scaling Regressions, Dead Seeds & Self-Sabotaging Moves
- **Hard-Mode Juno J1/J2 Starters Downgraded Below Standard (`tools/trainer_gen/gen.py:660-673`):** `starter_mon` overrides `ms` (Standard) without updating `mh` (Hard), downgrading 4 Hard Juno teams (`v110/111/112/122` — e.g. Lv 35 Hard Charmeleon loses `FLAMETHROWER`/`SLASH` for `SCRATCH`/`SMOKESCREEN`). Add `hard_moves=` (defaulting to `moves`) and regenerate `pbs/trainers.txt`.
- **8 Festival Warden Teams Hold Dead Field Seeds on `:PRISM_ARENA` (`pbs/trainers.txt`):** `:PRISM_ARENA` accepts **only `:MAGICALSEED`**, yet `LEADER_ODESSA` (`92/192/292` Oricorio) and `LEADER_BRANN` (`96/196/296` Magmortar) hold `ELEMENTALSEED`, and `LEADER_KAITO` (`92/192` `UNBURDEN` Hawlucha) holds `SYNTHETICSEED` (breaking Unburden!). Swap to `MAGICALSEED` or `WHITEHERB`/`LIFEORB`/`HEAVYDUTYBOOTS`.
- **12 Singles Sets Carry Doubles-Only Moves (Including Boss Healing Player!):**
  - `HOLLOW_WICK` (`0/100`, `pbs/trainers.txt:10237,10275`) Gardevoir runs **`HEALPULSE`** in a 1v1 Singles battle (healing the player +50% HP!) → swap to `WISH`/`WILLOWISP`/`SHADOWBALL`.
  - Singles Festival QF `LEADER_ODESSA` (`92/192/292`: `WIDEGUARD` Pelipper, `HELPINGHAND` Oricorio), `LEADER_CELESTINE` (`92/192`: `FOLLOWME` Togekiss), `ARCHSEER_DASK` (`92/292`: `QUASH` Sableye), and Gym 1 `JUGGLER,Florian` (`0/100/200`: `HELPINGHAND` Minccino).
- **Dead `LEADER_TAMSIN` AI Support Rule (`012_FieldEffects_TrainerPlays.rb:80`):** Targets removed `:SILKTRAP` instead of Hard Vivillon's `:RAGEPOWDER`.
- **Metadata Fixes (`maps_out/PBS/map_metadata_prismfall.txt`):** Add `BattleBack = city` on `180/181/608`, `Outdoor = true` on open-air Bleed zones `522/548`, and `MapPosition` on `990`.
- **P2 Polish:** Add Hard/Casual (`v150/250`) to all 4 `pbs/trainers_trials.txt` trainers; fix `MAGICALSEED` description (`pbs/items_fields.txt:20`: move `"theatrical"` to `SYNTHETICSEED`); fix `-Atk` natures on physical `CHANNELER,Mireille` (`TIMID` Gastly) & `FESTIVAL_TITANIA` (`BOLD` Play Rough Klefki); clean 3 `pbs/town_map.txt` redundant POIs (`L181,202,205`), stale `design/maps.json` segments (`255`, `920/924/925/926`), and decorative encounter-grass tag `2` on town maps `120/147/180`.

---

## PART I — End-to-End Playtest, `512×384` UI Ergonomics, Save/Game-Over & Reborn/Rejuv QoL Audit

### I1. Additional P0 Save/Reload Bugs, Softlocks & Severe `512×384` UI Collisions
1. **"Load last save" After ALL 25 Story Game Overs Fails to Reload State (`017_GameOver.rb:44-47, 162-176`):**
   - `GameOver.trigger` and `PrismfallReloadScene#main` call `Game.load(save_data)` / `$game_temp.title_screen_calling = true` without calling **`SaveData.mark_values_as_unloaded`** — so Essentials v21.1 skips reloading already-loaded `SaveData::Value`s (leaving switches, vars, choices, party & position dirty in RAM!). Add `SaveData.mark_values_as_unloaded` at `L45` and `L171`.
2. **Festival Level Cap Never Raises Between Rounds (`009_Festival.rb:350-352, 389-392`):**
   - `record_result(true)` advances `state[:stage] += 1` without calling `unlock_cap_for(ruleset(nxt[:ruleset]))`, pinning the player at Lv 90/92/94/96 until they enter the next round underleveled and deliberately lose to raise the cap!
3. **2 Autorun `Prismfall.checkpoint` Traps Softlock Saves Inside Locked Boss Rooms (`Map 952`, `Map 255`):**
   - `952_meridian_plate_vault.yaml:24-75` and `255_cindervault_tap.yaml:35-127` call `Prismfall.checkpoint` as Command #1 inside `trigger: autorun` (directly violating `017_GameOver.rb:56-57`), trapping battered/underleveled saves in an inescapable zero-heal boss loop! Move checkpoints outside the autorun + add pre-boss heals.
4. **`Endings.trigger` Never Saves Postgame State Before Credits + Marks `:END_GILDED_CHAIN` as `postgame? == true` (`018_Endings.rb:47-72`):**
   - Call `Game.save if !no_postgame`, set `n[:postgame] = no_postgame ? false : id`, and add `SaveData.mark_values_as_unloaded` on the `elsif no_postgame` title return.
5. **8 Built-Map Choices Map Cancel (`X`/`Esc`) to the Affirmative Option (`cancel: 1` Off-by-One):**
   - `552_dyers_ford.yaml:230` (barge), `528_marram_down.yaml:28` (one-way sledge), `541_grey_saltings.yaml:218` (ring fight), `566_spinners_rise.yaml:70` (Ram Race), `525_deepwood_cocoonfall.yaml:812,833,854` (anchors), `143_saltmere_rooms.yaml:1907` → change `cancel: 1` → `cancel: 2` (1-indexed!).
6. **4 Custom `512×384` UI Screens Clip or Overlap Text:**
   - `009_FieldEffects_FieldNotes.rb:132,150,191-209`: `LIST_WIDTH=200` clips `"Dark Crystal Cavern"`, `"Battled here: N"` collides 50–85px into field title on `y=40`, Line 10 collides into page counter at `y=354`, and lacks `LEFT`/`RIGHT` page navigation.
   - `019_LedgerScene.rb:96-114`: 6 long epitaphs clip past `h=72px` box into footer `y=358` (fix: `ROWS=6`, `box_y=234`, `h=114`).
   - `017_GameOver.rb:100-107`: 4-line epitaphs (`GO_STAY_OUT`/`GO_WEATHER`) collide into Ledger count at `y=262` (use `pbSetSmallFont` + `lineheight=24`).
   - `008_Trials_Board.rb:24-32` & `009_Trials_QuestLog.rb:21,96-97`: 45-char board items clip >512px & 27-char institution names overlap quest titles (use short `[:kingdom]` label).
7. **Ruin Route Bugs (`012_Narrative_Data.rb:406-411`, `016_Ledger.rb:140-145`):**
   - Register missing `:GO_R_SWEET_DREAMS` (`:ruin_exempt => true`); clamp `Resonance` to `<= -6` in `start_ruin_route` & `Resonance.set` so Harmony `+6` buff doesn't stay active on Ruin Route; add point-of-no-return confirmation + pre-branch checkpoint for `:ch15_look_back`.

### I2. High-Impact Reborn/Rejuv QoL Upgrades & P1 Fixes
- **Bag-HM / Field Tool QoL (`028_FieldMove_QoL.rb`) + Coast Packet:** Allow owning Badge + HM/TM (or Golden Tool) to use all 10 field moves (`Cut`, `Rock Smash`, `Flash`, `Strength`, `Surf`, `Fly`, `Rock Climb`, `Waterfall`, `Dive`, `Headbutt`) without wasting party moveslots; wire the documented Saltmere (`146`) ↔ Ebbmouth (`160`) ↔ Ferrow's (`100`) coast packet NPC (closing the 25-hour pre-Badge-8 Fly bottleneck).
- **Player Options Menu (`027_Options_QoL.rb`):** Expose already-coded **Photosensitive Mode** (`$PokemonSystem.photosensitive`, also gating `003_Bridge_EBDX.rb:446` & `010_Bridge_VersusIntro.rb` strobes!), **Speed-Up / Turbo (`1×/2×/3×`)**, **Difficulty change**, **Exp. All toggle**, and **Autosave toggle**.
- **Missing "Ties" Pause-Menu Screen + Menu Order Collision:** Add `PrismfallTiesScene` (Bonds / Factions / Resonance + exact numbers when `:OPEN_BOOK` is active — integrates cleanly with `Prismfall::Codex`!), and fix `Ledger` vs `Field Notes` both claiming `"order" => 45` (assign `43 Codex/Ties, 44 Quests, 45 Field Notes, 46 Ledger`).
- **4 Live Dev-Text Leaks in Festival Highlights (`015_Festival_Draw.rb:84, 87, 104, 112`):** Replace raw `"(ISENMAR_EMBITTERED)"`, `":VOLCANIC cools to :ASHEN_WASTE"`, `"Marisol swears for a full caption box"`, and `"If KAITO_TESTIFIED"` with diegetic prose; collapse 7 sequential R16 popups into 1 summary + highlight picker.
- **Trial Board Rank-4 Badge-Gate Spam (`005_Trials_Quests.rb:264-282`):** Track paid ranks per-rank so Badge-8 Elowen Rank 4 doesn't spam a popup on every board open for 6 gyms AND block Rank 5 rewards behind `break`.
- **Missing Gauntlet & War-Theatre Heals:** Add `$player.heal_party` before Bout 1 in `Octave.run_gauntlet` & `Trials.gauntlet`, repeatable healers on `528`/`540`, a Bone-Carters' Camp (`930`) medic + post-Partner heal on `926`, a pre-K2 camp heal on `561`, and Gym Lobby heal/PC attendants (`130/150/170/190`).
- **Other High-ROI UI/UX Fixes:**
  - `010_Festival_BracketScene.rb:163-203`: Show live `fe.drawn(:FINAL)` (`Brann` if `VALEN_COLLAPSED`), widen `CENTER_W = 168`, fix dead border fill `L184-185`, add message on empty `exhibition_menu`.
  - `019_LedgerScene.rb:126` & `009_Trials_QuestLog.rb:116`: Cache `@rows` outside the 60fps `loop`, add fade-in/out & `ensure` disposal, separate `:ruin_exempt` count (`23/23 (+0/2 Ruin)`).
  - `109_dovetail.yaml:19-27`: Show visual sprite previews (`PLAYER_A.png`/`PLAYER_B.png`) during Style A/B pick instead of pitch-black screen; fix `litemode`+`Hard` hybrid in `020_Passwords.rb:35-37`.
  - **Meridian Fellowship Card Mart Discount:** Wire the promised 10% `PokemonMartAdapter#getPrice` discount & global `:fellowship_off` activation.
  - **Visual Polish:** Draw dark 2-row tray behind 18 badges on `007_TrainerCard.rb`; adjust `007_Bosses_UI.rb:101` EBDX pip offset for regular Hard-Warden databoxes; add `QUENT/VESPER/MARCHETTI/KROLL/SABLE/THISTLE` + `"NPC "` prefix support to `025_CharsetAliases.rb:36`; prevent player sprite reverting to Gen 3 Red/Leaf while fishing/cycling/surfing (`026_PlayerLooks.rb:41-46`); add `'·'` to `002_Font_Glyphs.rb`; fix `Map 522` double-Juno window (`010_JunoFollower.rb:27`); wire `secondferry` NG+ carryover (`018_Endings.rb` + `020_Passwords.rb`).

---

## PART J — Overworld Map Atmosphere & Battle Cinematography Spectacle Pack (Zero New Image Art!)

### J1. Overworld Map Atmosphere & Lighting Bugs (All 117 Built RXDATA Maps Audited)
1. **P0 — 72 Animated Doors Wipe `MAP_TONES` Back to `(0,0,0,0)` (`mapgen/rpg.py:265-269`):**
   - `door_pages` emits `Tone(0,0,0,0)` *after* `Transfer Player` (and after `:on_enter_map` sets `MAP_TONES[dest]`), clobbering destination color grading on every building entry (plus 6 mid-map resets in `131, 181, 523, 545, 578, 924, 952`).
   - **Fix:** Add `PrismfallMaps.restore_tone(frames = 6)` in `005_MapAtmosphere.rb` and replace trailing `Tone(0,0,0,0)` in `rpg.py:269`.
2. **P0 — Water Reflections Silently Killed Across All Elowen Rivers & Lumen City (`mapgen/rcompose.py:316`):**
   - `AUTO_TAG['Still water'] = 6` (`StillWater` reflection tag) is skipped whenever the source tile has `x == 7` → `0` water reflections on `TS 53` (`521/524/525/540/552/566`) and `TS 60` (`180/181/608`). Prioritize `AUTO_TAG[name]` before source `x` and paint `tag=16` (`Puddle`) on `541 Grey Saltings`.
3. **P1 — Fog Never Clears Across Connections + Vanishing `prismfall_glass.png` + Night-Tone Crush (`005_MapAtmosphere.rb:126-146`):**
   - Reset `$game_map.fog_name = ""; $game_map.fog_opacity = 0` when `!f`; hook `:on_map_or_spriteset_change` for save-loads; attenuate negative outdoor `MAP_TONES` by `0.45×` at night; move `522`/`548` off one-shot `fog_event` into `MAP_FOGS` (`prismfall_glass`) and add `prismfall_glass` to `568/608/925/926`; swap `TS 61` static 1-frame `PF Magma` (`Map 255`) to animated 4-frame `Lava.png` already on disk; color-grade the 23 flat `(0,0,0,0)` maps (esp. `150–154` Pell Playhouse & `185–186` Spire Lobby/Gala Hall).
4. **P1 — Zero-Placement Automatic Tile-Scanned Lighting (`mapgen/ruby/013_OverworldLighting.rb`):**
   - **600+ light & Bleed tiles are already painted in `Map*.rxdata`** (`54` `gl_lamp`, `61` `lm_arclamp`, `58` hanging lanterns/garlands, `70` braziers/campfires, `67` tall interior windows & footlights, `433` Bleed glass shards). Scan `$game_map.data` once per map load to anchor cached additive radial glow halos (`blend_type = 1`, dusk/night scaling, `S424` Lowlight blackout reactivity, `154` Playhouse spotlight cones, interior window light shafts, Bleed prism shimmer, and lightweight ambient embers/fireflies/prism dust) + 3 new 256×256 fog PNGs (`prismfall_sunbeams`, `prismfall_shadow`, `prismfall_embers`) + strolling overworld `Followers/*` Pokémon & townsfolk on quiet hub maps!

### J2. Battle Cinematography, Multi-Bar Boss Drama & Z-Move/Mega Polish (`0` New Art Needed)
1. **P0 — Multi-Bar Boss Shield-Break Spectacle (`005_Bosses_Effects.rb:43-64, 96-133`, `007_Bosses_UI.rb:13, 113-114`):**
   - Currently **0/10** bosses wire `:music`, `:animation`, `:speech`, or break FX; `007_Bosses_UI.rb:13` erases the pip *before* `break_bar` runs; `pbBGMPlay(e[:music])` (`L128`) & `primal` (`L129`) run *last* after everything already happened.
   - **Fix:** Add `Prismfall::Bosses::FX.on_bar_break`: `0.10s` hitstop + camera zoom `:ENEMY` + `"Boss Shield Break"` SE + boss cry + 14f shake + themed room flash + 18-particle shard burst + pip shatter spark before redraw; move `e[:music]` (auto-fallback `"Battle - Boss Final Bar"` on last bar) & `primal` to fire *first*; add wild-boss title ribbon intros + `:defeat_fx` (`:calm_dissolve`, `:cable_break_launch`, `:steam_ascend`, `:shatter_collapse`).
2. **P0 — Enable Mid-Battle Portraits & Voice Blips (`014_Portraits.rb:812-834`):**
   - Hook `Battle::Scene#pbDisplayMessage`, `#pbDisplayPausedMessage`, `#pbShowCommands` to run `Portrait.extract(msg)` + optional `,right` side anchor (`x = 384`, clear of player databox) + `pbSEPlay("Voice - #{aid}")`! Immediately upgrades Mourner (`105:16`), Rook (`bosses.yaml:62`), Hard Wardens (`104`), and Groudon/Sahar (`107_Boss_Act3to5.rb`).
3. **P1 — Z-Move Ultimate Animations & 8-Eeveelution Prismatic Convergence (`001..005_ZPower`):**
   - Replace `002_ZPower_Moves.rb:54` replaying Level-5 base animations (`Tackle`/`Ember`) with `Z_SIGNATURE_ANIMS` (`:GIGAIMPACT`, `:BLASTBURN`, `:HYDROCANNON`, `:VOLTTACKLE`, `:DRACOMETEOR`, `:DARKVOID`, `:MOONBLAST`, etc.); replace `EXTREMEEVOBOOST`'s `:WORKUP` (`001:86`) with an 8-color spiraling orb convergence + `"Prism Arena Swell"` SE; add Z-unleash camera zoom + room dim + type-colored `1.05s` `:eye_strip` cut-in; expand `PrismfallSpeech::LINES` (`005_ZPower_TrainerSpeech.rb:21-27`) from `1` entry to all Wardens/Rivals/Directors (`:ace`, `:mega`, `:zmove`) + auto `"Battle - Warden Last"` BGM switch on a Gym Warden's final mon!
4. **P1 — Mega Cut-Ins, VS Polish & Dynamic Weather/State Field Fusion (`002..004_Mega`, `010_Bridge_VersusIntro.rb`, `002..003_Bridge`):**
   - Pre-Mega `1.0s` `:eye_strip` cut-in (crimson-glass glitch treatment for Meridian Lattice-band Megas!) + SFX/flash on all 8 Mega field showpieces (`003_Mega_Fields.rb:53-108`).
   - In `010_Bridge_VersusIntro.rb`: add missing `THEMES` (`QUENT/SABLE/THISTLE/VESPER`), mirrored desaturated `:REFLECTION` PC VS screen (0 new art!), 2-opponent dual-bust VS support (`L96`), `"VS Cutin Lightning"` + `Voice - <ID>` on lock, and small-font rank kicker above trainer name.
   - In `002..003_Bridge`: wire `:prismfall_weather_changed` visual fusion (atmospheric `Tone` + Stormfront lightning rain, Ashen Waste glass sandstorm, Wasteland acid rain, Silkwood electric dew), live `:prismfall_field_visual_state` sync (`CRYSTAL_CAVERN` 4-hue glow, `PRISM_ARENA` 18-Plate sigil/beams, `VOLCANIC` primed, `ASHEN_WASTE` geyser, `NEON_GRID` S2 surge), direction-aware `transition_for(old_id, old_stage, new_id, new_stage)`, `pfl*` parallax, outdoor night fallback tone (`11/13` fields), and `:animation` hooks on field hazards across `101..140`!






