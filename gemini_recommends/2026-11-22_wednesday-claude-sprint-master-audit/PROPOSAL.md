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

