# SYSTEMS — `Prismfall Core` plugin

Plugin folder: `plugins/Prismfall Core/` (Essentials v21.1, Ruby 3.1-safe). All tunables are in
`001_Config.rb` (gyms, caps, difficulty, starters, trainer card) and `008_Festival_Data.rb` (Festival).
Core state is saved in its own save value (`$prismfall`, `Prismfall::SaveState`), never in switches/variables.

## 0. Load order and hooks
`meta.txt` declares `Optional = v21.1 Hotfixes` and `Optional = Elite Battle: DX`, so Core loads **after**
them. This matters because EBDX redefines `pbLoadTrainer`; Core must wrap EBDX's version.
Every hook is an `alias`-chain with a `unless method_defined?` guard (safe on F12 soft reset), and sits at the
battle or trainer-loading layer (never the battle scene), so it works with or without EBDX:

| Hook | Purpose |
|---|---|
| `pbLoadTrainer` | picks the difficulty variant (+100 Hard / +200 Casual, falls back to base) |
| `:on_trainer_load` handler | rival starter swap (TrainerBattle foes and registered partners) |
| `BattleCreationHelperMethods.prepare_battle` | forced Set style, Bag lock, snapshot of cap/difficulty in `battle.rules` |
| `Game_Temp#add_battle_rule` | new rules `"noBagItems"` / `"allowBagItems"` |
| `Battle#pbItemMenu` | blocks the Bag when the Bag lock is on |
| `Battle#pbGainExpOne` + `GameData::GrowthRate#add_exp` | no Exp at cap, Exp clamped to the cap, difficulty Exp multiplier |
| `Battle::Battler#pbObedienceCheck?` | disobedience above the cap (vanilla badge check runs if caps are off) |
| Rare Candy / EXP Candy item handlers + `pbChangeExp` | blocked at cap, usable quantity limited to the cap |
| `DayCare::DayCareSlot#add_exp` | Day Care stops at the cap |
| `NPCTrainer#skill_level` | AI skill floor per mode |
| `PokemonPauseMenu#pbShowInfo` | pause-menu box: "Level cap: Lv. 23 / Mode: Standard" |
| `PokemonTrainerCard_Scene#pbDrawTrainerCardFront` | 18-badge layout |
| `pbCallTitle` | one-shot redirect to "load last save" after a story game over |
| `Pokemon#calcIV`, `Pokemon#able?` | passwords: Perfect IVs, Monotype (only in battle, only for player-owned Pokémon) |
| `Player#has_exp_all`, `PokemonBag#has?(:EXPALL)` | password: No Exp. All |
| pause menu entry `:prismfall_ledger` | Ledger viewer |
| `Pokemon#calc_stats` | `HP_BOOSTS` max-HP multipliers (Shiv's Ambipom) |
| `Scene_Credits#main` | credits → title for endings with no post-game |
| `:on_trainer_load` `:prismfall_hp_boosts` | applies `HP_BOOSTS` |

Custom events other plugins can listen to (`EventHandlers.add(event, :key, proc)`):
`:prismfall_badge_awarded (n)`, `:prismfall_difficulty_changed (old, new)`, `:prismfall_festival_started`,
`:prismfall_festival_before_battle (stage_id, opponent_id)`, `:prismfall_festival_result (stage_id, won)`,
`:prismfall_festival_boss (pkmn, stage_id)` (non-EBDX boss path), `:prismfall_festival_finished (champion)`,
`:prismfall_festival_drawn (path)`, `:prismfall_narrative_changed (kind, id, old, new)`, `:prismfall_game_over (id, first)`,
`:prismfall_ending (id, first)`, `:prismfall_ruin_route_started`, `:prismfall_password_enabled (id, value)`.

## 1. Gyms and badges
`Prismfall::GYMS` mirrors SPINE: one Hash per gym with `:index, :type, :city, :warden, :trainer_name,
:trainer_type, :field, :cap, :version` (gym 9 also has `:rival_battle => 3`, i.e. Juno's J3 uses versions 30/31/32).

- `$player.badges` grows to 18 entries automatically (padded on load/award). `Prismfall.badge_count` counts badges 1-18.
- Award with `Prismfall.award_badge(n)`, not `$player.badges[n-1] = true`: it also records the badge time,
  fires `:prismfall_badge_awarded` and announces the new cap.
- Field-move requirements (WORLD.md section 4): `FIELD_MOVE_BADGES` sets CUT 1, ROCKSMASH 2, FLASH 4, STRENGTH 5, SURF 6,
  FLY 8, ROCKCLIMB 10, WATERFALL 11, DIVE 15. These are written into `Settings::BADGE_FOR_*` at load.
  `FIELD_MOVES_COUNT_BADGES = true` means "at least N badges"; set it to `false` for "gym N's badge specifically" (written 1-18 in our config).
- **Rock Climb** (v21 has no handler; `022_RockClimb.rb` adds one) uses `Prismfall::BADGE_FOR_ROCKCLIMB` (also `Settings::BADGE_FOR_ROCKCLIMB`) = 10.
  To map a cliff, put an Action-Button event on the bottom tile and one on the top tile, named `RockClimb` or `RockClimb(N)`,
  with `Script: pbRockClimb` (or `pbRockClimb(3)`). The player then moves N tiles in the facing direction with Through on (default 2).
  Using the move from the party menu while facing the event works too. Keep the landing tile passable. Optional SE: `Audio/SE/Rock climb`.

### Trainer Card (18 badges in 2 rows of 9)
Core keeps the vanilla text and suppresses only the vanilla 8-badge row. Layout is set in `TrainerCardLayout`:
32x32 icons, row 1 at y=294 and row 2 at y=332, x = 64 + col*44 (badge strip covers about x 56-456, y 286-372).
Art to draw (none of it is required, there are code fallbacks):

| File | Size | Notes |
|---|---|---|
| `Graphics/UI/Trainer Card/icon_badges_18.png` | 288x64 | 9 columns x 2 rows of 32x32; badge *i* (0-based) at column `i % 9`, row `i / 9`. Fallback: vanilla `icon_badges.png` read 8 per row. |
| `Graphics/UI/Trainer Card/icon_badge_slot.png` | 32x32 | optional empty-slot frame drawn under every slot; fallback is a faint box drawn in code |
| `Graphics/UI/Trainer Card/card.png`, `card_f.png` | 512x384 | redraw the bottom panel as a 2x9 badge strip (area above); the text rows are unchanged from vanilla |

## 2. Level caps
Cap = `:cap` of the **first gym whose badge isn't owned**: 15 before Badge 1, ... , 85 before Badge 18.
With all 18 badges the cap is 90; it becomes 100 after `Prismfall::LevelCap.unlock_finale!`. The Festival
calls that for the finale stages; earlier rounds raise the cap through an override (QF 92, SF 94, Final 96).
- Battle Exp stops at the cap, and a single gain can't push a Pokémon past it. EVs are still gained.
  "X is at the level cap" is shown once per battle per Pokémon.
- Rare Candy and EXP Candy are refused at the cap, and the "how many?" maximum stops at the cap.
  Setting `RARE_CANDY_EVOLVES_AT_CAP = true` lets a Rare Candy trigger a pending level evolution instead.
- Obedience: Pokémon above `cap + :obedience_margin` can disobey (same formula as vanilla, using the cap
  instead of the badge level). Off on Casual. When caps are off, the vanilla badge check runs.
- Day Care growth stops at the cap.
- The cap is shown in the pause menu info box (`SHOW_CAP_IN_PAUSE_MENU`), on the debug status screen, and through `Prismfall::LevelCap.announce`.

```
Script: Prismfall::LevelCap.announce            # "The current level cap is Lv. 23."
Script: Prismfall::LevelCap.set_override(30)    # story-forced cap; .clear_override to undo
Script: Prismfall::LevelCap.unlock_finale!      # post-Badge-18 cap becomes 100
Conditional Branch > Script: Prismfall.level_cap >= 50
```

## 3. Difficulty (Casual / Standard / Hard)
| Tunable | Casual | Standard | Hard |
|---|---|---|---|
| trainer version offset | +200 | 0 | +100 |
| Exp multiplier | 1.5 | 1.0 | 1.0 |
| forced Set style | no | no | **yes** |
| Bag in trainer battles | yes | yes | **no** |
| cap obedience | off | on | on |
| AI skill floor | - | - | 48 (high) |
Also available per mode: `:exp_at_cap`, `:candy_at_cap` (make caps soft), `:cap_bonus`, `:ai_skill_max`,
`:obedience_margin`. The rule for changing modes later is `DIFFICULTY_CHANGE_RULE` (`:any`, `:lower_only` or `:locked`).

Trainer variants (SPINE): any `TrainerBattle`/`pbLoadTrainer` call with version `v < 100` loads `v+offset`
if it exists in trainers.txt, else `v`. Versions >= 100 are explicit and never remapped.
Explicit battle rules always win over the mode: `setBattleRule("switchStyle")`, `setBattleRule("allowBagItems")`, `setBattleRule("noBagItems")`.

```
# Intro event, after the player names themselves:
Script: Prismfall.choose_difficulty            # choice list with descriptions + confirm
# NPC / PC that lets the player change it later:
Script: Prismfall::Difficulty.change_menu
Conditional Branch > Script: Prismfall::Difficulty.hard?
```

## 4. Rival starter system
Starter table `STARTER_LINES`: Gen 1-9 × [Grass, Fire, Water] × 3 stages (all IDs checked against the Gen 9 Pack PBS).
1. Record the starter when the player receives it:
   `Script: Prismfall.record_starter($player.party[0])` (or `:SPRIGATITO`). For an off-table pick, pass the slot and gen explicitly:
   `Prismfall.record_starter(:EEVEE, gen: 1, slot: 2)`. If nothing was recorded, Core falls back to the player's earliest-received starter-line Pokémon.
2. Rival battles: `Prismfall.rival_battle(:RIVAL_KESTREL, "Kestrel", 3)` gives version `3*10 + slot`
   (+ the difficulty offset through `pbLoadTrainer`). Options: `lose_text:`, `can_lose:`, `double:`, `field:`, `outcome_var:`. Returns true on a win.
3. At load, every Gen 1 starter-line Pokémon of `RIVAL_KESTREL`, `RIVAL_JUNO` or `LEADER_JUNO` becomes the same
   slot and stage in the player's generation: the level is kept, level-up moves are regenerated, item/nature/EVs/IVs/shininess/nickname
   are kept, and so is the ability slot (an explicit PBS `Ability` maps to its slot). Mega Stones are remapped to the
   new species' stone if it has one, else replaced with `MEGA_STONE_FALLBACK_ITEM` (Life Orb).
- Cutscene helpers: `Prismfall::Rival.kestrel_slot` / `juno_slot` (Kestrel has the advantage, Juno is weak),
  `Prismfall::Rival.rival_starter_species(:KESTREL, 0)` gives the species ID to name or show.
- Gym 9: `Prismfall.gym_battle(9)` uses LEADER_JUNO version 30/31/32 automatically.

```
Script: Prismfall.rival_battle(:RIVAL_KESTREL, "Kestrel", 1, can_lose: true)
Script: Prismfall.gym_battle(3)          # Marisol, sets :WATER_SURFACE if Field Effects is installed
Script: pbMessage(_INTL("Kestrel picked {1}!", GameData::Species.get(Prismfall::Rival.rival_starter_species(:KESTREL)).name))
```

## 5. Festival of Champions
Data lives in `008_Festival_Data.rb` (entrants, `DELEGATIONS`, rule sets, stages) and `015_Festival_Draw.rb` (draw, `MATCH_RULES`,
exhibitions, Arceus variants). It's transcribed from NARRATIVE_KEYS §6. **SPINE Revisions 5–6** apply: the Festival chooses who
receives Arceus's Blessing. There are 16 seats: the player plus 15 kingdom delegates (two per kingdom, plus Valen for the Accord).
Every entrant is a story-met character. Cameos are sidequest fights (§14).

`Festival.start` runs in this order:
1. **Delegations.** For each seat in `DELEGATIONS`, the first candidate whose condition holds and who isn't seated yet takes it.
   `:FORFEIT` seats (a kingdom that lost the war, or Cragholm after the raid) are lent to the first free name in `FORFEIT_POOL`.
   `BRACKET_SEATS` maps seats to bracket slots. `Festival.seated?(:ID)` and the condition `seated(:ID)` report who got in; before
   the Festival starts they give a live preview.
2. **The draw** (5a) over the seated entrants.
3. **NPC matches.** A drawn path opponent wins until they meet the player. Otherwise the first `MATCH_RULES` row for that pair whose
   condition holds decides it, and failing that the higher `:rating`.

Caps by round: R16 90, QF 92, SF 94, Final 96, Hijack/True Finale 100. Every round: no Bag, canLose (retry), heals.

**Highlights.** After the player wins a round, `show_round_results` announces each NPC result. If the match has `MATCH_RULES` moments
(`[actor, pokemon, event, caption]`), it asks "Watch the highlights?". If `Prismfall::Cutscene.match_highlight` exists, Core calls it as
`match_highlight(a, b, winner, moments)`, where each trainer is `{ :id, :name, :trainer_type }`. Otherwise the captions play as text.
Set `AUTO_ROUND_RESULTS = false` to call `Prismfall::Festival.show_round_results(round)` from an event instead.

### 5a. The draw
`DRAWS[stage]` is an ordered list of `{ :opponent, :condition, :version }`. The first match whose *person* isn't already used wins; the
stage default (`PLAYER_PATH = [:JUNO, :CELESTINE, :KESTREL, :VALEN]`) is the fallback.
- **R16, QF, SF** are drawn at start. A seated opponent **swaps** into the player's block and the displaced entrant plays on as an NPC.
  An unseated one (Rowan, Dask) replaces the default, who **withdraws**; that counts as out.
- **The Final is `:live`**: it's drawn when its battle starts on Day 7. Brann stands in for a collapsed Valen without reseating anyone.
- **The Hijack** is drawn live (Voss, Quent or Theodric).

`Festival.drawn(:STAGE)` and `drawn(:STAGE)` return the locked entrant. `Festival.arceus_variant` returns the matching `ARCEUS_VARIANTS`
entry for Prismfall Bosses. Opponents the player meets go to the Ledger `met` list. Validation covers seats, forfeits, match rules and
draws (persons disjoint across stages), and flags any cameo or Rev-4 outsider entrant.

### 5b. Festival days and exhibitions
Events set the day: `Prismfall::Festival.set_day(3)` or `.next_day!`; conditions can read it with `festival_day`. Exhibitions (`exhibition_menu`,
`exhibition(:ID)`) offer two kinds of opponent:
- entrants flagged `:exhibition` (Marisol), from the day **after** they're knocked out or withdraw;
- `EXHIBITION_EXTRAS` entries (Pageant Bout: Dorian & Rook as a double; Juno's Garden Match; Marisol; Morwen's Echo), each with a
  `:condition` and a `:from_day`.

None are offered on the Ruin Route; its Eevee Octave is run by events. Two-trainer entrants (`:double => true`) start a double battle.

```
# Reception desk (after Badge 18):
Conditional Branch > Script: Prismfall::Festival.start
# Arena entrance:
Script: Prismfall::Festival.show_bracket
Conditional Branch > Script: Prismfall::Festival.next_match
   (won)  -> cutscene for the stage; branch on Prismfall::Festival.stage_id (:QF, :SF, :FINAL, :HIJACK, :ARCEUS, nil=finished)
   (else) -> "Try again?" loop; the stage doesn't advance
# Exhibition hall NPC:
Script: Prismfall::Festival.set_day(3)
Script: Prismfall::Festival.exhibition_menu          # or .exhibition(:PAGEANT_BOUT)
# Custom battle staged by the event (e.g. a scripted double):
Script: Prismfall::Festival.record_result(true)
Conditional Branch > Script: Prismfall::Festival.finished?
```
The bracket scene is drawn entirely in code: names at the edges, gold/grey/blue paths, and a centre Final/Champion box.
An optional background goes in `Graphics/UI/Prismfall/festival_bracket_bg.png` (512x384).

**Why not PWT?** The base project's *Pokemon World Tournament* is a random 8-trainer, 3-round, map-event-driven
tournament with no saved bracket. It can't hold a 16-entrant, story-locked, saved bracket, so the Festival doesn't use it.
PWT stays available for the post-game Battle Tower and Warden rematch gauntlet. It works alongside Core: its `pbLoadTrainer`
and `prepare_battle` aliases chain with ours, so PWT opponents also get difficulty variants. PWT battles set
`internalBattle = false`, so caps and Exp don't apply there.

## 6. Boss battles (Rejuvenation-style) with EBDX
EBDX ships `EliteBattle.bossBattle(species, level, player_side = 2, can_catch = false, options = {})`
(`Plugins/Elite Battle DX/[000] Scripts/Battle Mechanics/Boss Battles.rb`). It provides:
- a 2v1 or 1v1 wild battle with the boss databox (`dataBoxBoss`)
- stat multipliers through `:bossboost`; `:HP => 2.0` doubles max HP
- status immunities (configured by `BOSSBATTLES` `IMMUNITIES` in the EBDX metrics)
- no capture, no running
- `generateWild` options: `:moves, :iv, :ev, :ability, :nature, :item, :form, :shiny`

Core uses it automatically for the Festival Arceus stage when EBDX is present (`STAGES[...][:boss]`). The separate
`Prismfall Bosses` plugin (Rejuvenation-style multi-bar bosses, another agent) is adding its own switch to take that stage over when it's installed. Core leaves the stage as is.

EBDX has **no native multiple HP bars**. To get the Rejuvenation "phases" feel, combine three things:
1. `EliteBattle.bossBattle` with a high `:HP` boost.
2. A battle script, set before the battle with `EliteBattle.set(:nextBattleScript, :MY_BOSS)`, holding a `BattleScripts::MY_BOSS` hash whose keys are
   `"turnStartN"`, `"damageOpp"`, `"lastOpp"` and so on (see `[003] Config/Battle Scripts.rb`). A key's value can be a proc that runs in the scene, e.g.
   `@battlers[1].pbRecoverHP(...)`, `@battlers[1].pbRaiseStatStageBasic(:ATTACK, 1)`, `@battle.change_field(:BLEED, "...")`
   or `@sprites["battlebg"].reconfigure(...)`. That gives a scripted "bar break" at a damage threshold.
3. For trainer villains, the same script through the EBDX trainer PBS `BattleScript` key.

If true multi-bar HP is needed later, it belongs in a small hook on `Battle::Battler#pbReduceHP` (an EBDX Bridge task). Don't rewrite bossBattle.

```
Script: EliteBattle.bossBattle(:GIRATINA, 60, 1, false, { :bossboost => { :HP => 2.5, :ATTACK => 1.2, :DEFENSE => 1.2, :SPECIAL_ATTACK => 1.2, :SPECIAL_DEFENSE => 1.2, :SPEED => 1.0 }, :moves => [:SHADOWFORCE, :DRAGONCLAW, :AURASPHERE, :WILLOWISP] })
```
(Set `setBattleRule("field", :INVERSE)` or `setBattleRule("canLose")` first if needed. EBDX's wild boss path runs `prepare_battle`, so Core's and Field Effects' rules still apply.)

## 7. Debug
Debug menu → **Prismfall Core...** covers:
- status and data check
- set difficulty, set starter
- cap override, finale cap, caps on/off
- Festival tools: start, reset, skip to stage, bracket, next match, exhibitions
- **Narrative tools**: edit bond/standing/resonance, make a choice, test a condition string, show the determined ending, trigger an ending, force the password prompt, redraw the bracket
- **Ledger tools**: view, mark all found, clear, test any game over The separate *Prismfall Debug Tools* plugin covers fields, Wardens and badge count.

## 8. Narrative state (Bonds / Standing / Resonance / Choices)
The data in `012_Narrative_Data.rb` is transcribed from `design/NARRATIVE_KEYS.md` §1–5, 9 and 12. Re-run the transcription when that file
changes. State is saved in `Prismfall.state.narrative`, not in switches.
- **Bonds**: 10 (Juno, Kestrel, Rowan, Voss, Valen, Ilsa, Sigrun, Nyx, Marisol, Ysolde), range −10..10. Tiers: hostile, wary, neutral,
  friendly, close, devoted.
- **Standing**: Hollow, Meridian, Accord. Tiers: enemy, distrusted, neutral, trusted, ally.
- **Resonance**: −10 (Ruin) .. +10 (Harmony), in 5 bands.
- **Choices**: 48 keys, all `:once`. **`pf_choose` applies `CHOICE_EFFECTS` once.** The effect tokens are `ID+n`, with `RES` meaning
  Resonance. The toast "X will remember that." appears only when a Bond changes tier. Events no longer apply deltas by hand.
- **Aliases**: the Map Builder's keys `:PRO_FELLOWSHIP`, `:CH2_TAMSIN`, `:CH3_JUNO_TALK`, `:CH4_KESTREL_MOURNER` and `:CH4_TEO` resolve to
  the canonical lowercase keys. Any UPPERCASE key whose lowercase form is registered also resolves. Those map events still hand-apply their
  own (older) deltas, so effects are **not** auto-applied through a legacy alias (`LEGACY_ALIASES_SKIP_EFFECTS`). To migrate an event, change
  it to the lowercase key and delete its `pf_bond_add` / `pf_standing_add` lines.
- **Derived flags** (`DERIVED_FLAGS`, ~45) such as `TEO_SAVED` and `KESTREL_FALLEN` are computed and never stored. Flags can reference
  other flags; cycles are rejected. **Tallies**: `CONSENT` (the 18 `WARDEN_CONSENT` conditions; ≥12 is needed for the Good ending),
  `ENGINE_BREAKS` and `WARM_BONDS`.
- **The Ashkaar–Isenmar War** (§4.3): six `:war_*` choices with effects, and the `WAR_TRUST` tally. The outcome flags are
  `WAR_STOPPED`, `WAR_BOTH_BROKEN`, `WAR_ASHKAAR_WON` and `WAR_ISENMAR_WON`, plus `WAR_OCCUPATION` and `ISENMAR_EMBITTERED` /
  `ASHKAAR_EMBITTERED`. An embittered kingdom's Wardens withhold Consent (entries 3, 10 / 7, 18), occupation forces the Unfinished
  ending, and the loser of the war gets one Festival seat.
- **Mirror switches**: Core rewrites S221–S228 (TEO_SAVED … KESTREL_REDEEMED) after every narrative change. Events read them; never write them.
```
Script: pf_choose(:ch9_teo_sable, :save_teo)        # applies MARISOL+4 HOLLOW+1 RES+1 once
Conditional Branch > Script: pf_flag(:TEO_SAVED)
Conditional Branch > Script: pf_tally(:CONSENT) >= 12
Conditional Branch > Script: pf_cond("flag(:KESTREL_FALLEN) && choice(:ch21_reach_kestrel) == :let_go")
Script: pf_bond_add(:ILSA, 1)                       # Quiet Hours scenes etc.
```
`Prismfall::NarrativeCheck.run` implements the NARRATIVE_KEYS §15 checklist:
- every choice key and value used in conditions exists;
- every `flag`/`tally`/`bond`/`standing` name used exists;
- no flag cycles;
- effect tokens are valid;
- every alias target exists;
- `ENDING_RULES` covers every `:ch21_final` value;
- `WARDEN_CONSENT` has 18 entries;
- the Festival draw is valid.

It runs at load (console warnings in debug) and from Debug → Prismfall Core → Show Core status.

## 9. Condition strings (safe subset, no eval)
These are used by draws, flags, tallies, ending rules and exhibitions, and are available anywhere via `Prismfall.cond(str)` / `pf_cond(str)`.
Operators: `&& || !` (or `and or not`), `== != >= <= > <`, `+ -`, and parentheses. Literals: integers, `:symbols`, `"strings"`, `true false nil`.
Only these functions exist:
`bond bond_tier standing standing_tier resonance resonance_band choice made chose flag tally badges has_badge difficulty level_cap
starter_slot starter_gen password gameover_found gameovers_found ending_seen ruin_unlocked ruin_route festival_stage festival_day drawn seated
eliminated met cameo_beaten switch var` (switches and variables are read-only).
`nil` counts as 0 in arithmetic and `< >` comparisons. To add a function, add a line to `Conditions::FUNCTIONS`.

## 10. Story game overs + checkpoints
There are 25 entries: 23 canonical, plus 2 Ruin-only marked `:ruin_exempt`. Map-builder aliases resolve to canonical IDs:
`:GO_LAST_FERRY` → `:GO_HOMEWARD`, `:GO_BLEED_TIDE` → `:GO_ORCHARD`. `Prismfall.game_over(:GO_X)` does the following:
1. Records the canonical ID in the Ledger.
2. Shows the dark code-drawn screen.
3. Offers **Load last save** or **Return to title**.

`Prismfall.checkpoint` saves, so place it **before** the trigger page (the NARRATIVE_KEYS §10 table lists each checkpoint). The `nomercy`
password turns checkpoints off.
```
Script: Prismfall.checkpoint
Script: Prismfall.game_over(:GO_CURTAIN_CALL)
# Battle-loss game over (GO_WEATHER: the unwinnable Kyogre):
Script: setBattleRule("canLose")
Conditional Branch > Script: !WildBattle.start(:KYOGRE, 80)
   Script: Prismfall.game_over(:GO_WEATHER)
```

## 11. Ledger (cross-save)
The Ledger is the file `Prismfall_Ledger.txt` next to the save, and it survives new games. It holds:
- game overs found,
- endings seen,
- **cameos beaten**,
- Festival opponents **met** (for the Hall of Reflections),

each with the first-found time. **Ruin Route unlocked** = all 23 canonical game overs found. View it with `Prismfall::Ledger.show`, or
through the pause-menu "Ledger" entry. It has three tabs: Game Overs / Endings / Cameos, with "???" for anything unfound. Hints for unfound
game overs show with the `ledgerhints` password or once any ending has been seen.
```
Conditional Branch > Script: Prismfall::Ledger.ruin_unlocked?       # Ch15 Reverse Depths pane
   Script: pf_choose(:ch15_look_back, :yes)
   Script: Prismfall.start_ruin_route
```

## 12. Endings
There are 10 endings: Homecoming (good), The Gilded Chain (bad), 6 grey, and 2 ruin. `ENDING_RULES` is an ordered list (`DEFAULT_ENDING` =
Unfinished). `Prismfall.trigger_ending` with no ID does the following:
1. Determines the ending from the rules.
2. Records it in the Ledger.
3. Sets `narrative[:postgame]` to the ending ID and writes the **post-game switches S263–S269** from `POSTGAME_SWITCHES`.
4. Fires `:prismfall_ending`.
5. Runs the ending's common event, then the credits.

The Gilded Chain has no post-game, so its credits return to the title. Every other ending returns to the map, and the calling event continues.
```
Script: pf_choose(:ch21_final, :return)
Script: pf_choose(:ch21_boon, :end_reparations)   # the Boon is asked BEFORE the ending fires; this value lifts an occupation
Script: Prismfall.trigger_ending
```

## 13. New-game passwords
`Prismfall::Passwords.prompt` takes passwords at new game only. Put it in the intro, next to `Prismfall.choose_difficulty`.

| Word | Effect |
|---|---|
| `nocap` | no level caps |
| `fullivs` | 31 IVs for player-owned Pokémon |
| `noexpall` | Exp. All off |
| `monotype` | choose a type; Pokémon without it can't battle |
| `hardonly` | Hard, and it can't be lowered |
| `litemode` | Exp ×2, no disobedience, AI ≤ 32 |
| `ledgerhints` | Ledger hints for unfound game overs |
| `nomercy` | `Prismfall.checkpoint` does nothing |
| `openbook` | flag for the Ties page (shows numbers) |
| `colorless` | Resonance swings halved |
| `secondferry` | accepted only once the Ledger has an ending; sets `:SECOND_FERRY` (the NG+ carryover itself is still to do) |

Rows go in `Passwords::TABLE`. Use `:overrides` for difficulty tunables and `:requires`/`:refusal` for gated passwords.

## 14. Sidequest cameo fights + HP boosts
These are Revision 4's optional cameo sidequests:
```
Script: Prismfall.cameo_battle(:FESTIVAL_LIN, "Lin", 9)     # post-game rematch version 9 (BALANCE.md: 0/1/2/3/9)
Script: Prismfall.cameo_battle(:FESTIVAL_SHELLY, "Shelly", 0, double: true)
```
Each is a normal trainer battle with the difficulty variant and canLose, so a loss doesn't black out. It returns true on a win. The first win
against each cameo trainer type is recorded in the Ledger, with a toast; `Narrative::CAMEOS` lists the 10 names. The condition
`cameo_beaten(:FESTIVAL_LIN)` checks it.

`HP_BOOSTS` gives listed trainer Pokémon a max-HP multiplier through an `:on_trainer_load` handler. Damage carries through recalculation.
It's currently used for Shiv's Ambipom at ×2 (BALANCE.md).

## 15. Trials, quests, event Pokémon, badge-tier encounters (separate plugin: `Prismfall Trials`)
Requires Core; stores its state in `Prismfall.state.trials` (no switches). Design: `design/TRIALS.md`, `design/BADGE_TIERS.md`;
data and dialogue: `design/TRIALS_QUESTS.md`, `design/EVENT_POKEMON.md` (generated by `ruby tools/trials_docs.rb`); map events:
`design/TRIAL_EVENTS.yaml`. Event API: `pf_trial_talk(:KEY)`, `pf_trial_board(:TRIAL)`, `pf_trial_keeper(:TRIAL)`,
`pf_quest_*`, `pf_event_battle/gift`, `pf_trial_rumours`. It adds read-only condition functions to
`Prismfall::Conditions::FUNCTIONS` (`quest_state`, `quest_step`, `quest_done`, `quest_flag`, `trial_rank`, `chase`, `deed`,
`event_mon`, `has_item`, `party_has`, `night`, `fields_seen`, `tier`...) and a "Quests" pause-menu entry.
Test: `tools/harness/run_trials.rb`.

## Open questions (need the user)
1. **Hard mode Bag lock:** this also blocks Poké Balls and items in *trainer* battles only; wild battles stay open. Is that right?
