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
Data lives in `008_Festival_Data.rb` (entrants, default seeding, rule sets, stages) and `015_Festival_Draw.rb`
(choice-driven draw). The roster comes from `design/CAMEOS.md`: Lin is the headline/QF cameo, plus Amaria, Shelly,
Alexandra, Venam, Shiv and Garret. Melia, Titania and Nova are draw-only extras. The bracket Wardens are Nyx, Kaito,
Odessa, Celestine and Sigrun; they're NPC-only, with version 50 reserved. The default seeding is CAMEOS.md's
"Default draw" table. Cameo versions follow CAMEOS.md: 1 = R16/exhibition, 2 = QF, 3 = SF/Final-tier.
`PLAYER_PATH = [:JUNO, :LIN, :KESTREL, :VALEN]` is now only the **fallback**, see 5a. The player's drawn opponents
always win their NPC matches until they meet the player. The other NPC matches use `SCRIPTED_WINNERS[[round, match]]`;
anything left over is simulated from `:rating` with a per-save seed, so results are stable across reloads.

Stages and caps (per-round rule sets): R16 90, QF 92, SF 94, Final 96, Hijack 100, True Finale 100. The QF-to-Final rule
sets set a cap override; the 100 rule set unlocks the finale cap. Every rule set means: no Bag, canLose (retry), heal
before and after, no prize money. Exhibitions are offered for flagged entrants who are no longer alive in the bracket
(Shelly's is a double battle).

### 5a. Choice-driven draw (Revision 3)
`DRAWS[stage_id]` is an ordered list of `{ :opponent, :condition, :version }`. The first candidate whose condition holds
wins; the stage default is always appended last as the fallback. Bracket stages (R16 to Final) are drawn when
`Festival.start` runs. The drawn opponent is seated in the player's block: if it's already seeded it swaps seats with the
default, otherwise it replaces the default, which leaves the bracket. Hijack is drawn live and fixed when its battle starts.
A variant is just another entrant with the same `:person`, e.g. `:KESTREL_FALLEN` = RIVAL_KESTREL with `:rival_battle => 9`,
which loads versions 90/91/92. Validation runs at load (console warning) and on `Festival.start` in debug (raises). It checks
that every candidate exists, every condition parses, every stage has a fallback, and no person is a candidate in two stages,
so a run can never draw anyone twice.
```ruby
DRAWS[:SF] = [
  { :opponent => :KESTREL_FALLEN, :condition => "bond(:KESTREL) <= -4 || choice(:kestrel_truth) == :betrayed" },
  { :opponent => :TITANIA, :condition => "choice(:kestrel_truth) == :told && bond(:KESTREL) >= 6", :version => 3 }
]   # fallback: :KESTREL
```
Sample draw entrants that need trainer data: `LEADER_ROWAN "Rowan" v50`, `CHAMPION_SUCCESSOR "Successor" v0`,
`HOLLOW_MOURNER "Mourner" v0`, Kestrel v90-92, Melia v1, Titania v3, Nova v2. All of these are placeholders until NARRATIVE_KEYS.md arrives.

```
# Reception desk (after Badge 18):
Conditional Branch > Script: Prismfall::Festival.start
# Arena entrance:
Script: Prismfall::Festival.show_bracket
Conditional Branch > Script: Prismfall::Festival.next_match
   (won)  -> cutscene for the stage; branch on Prismfall::Festival.stage_id (:QF, :SF, :FINAL, :HIJACK, :ARCEUS, nil=finished)
   (else) -> "Try again?" loop; the stage doesn't advance
# Exhibition hall NPC:
Script: Prismfall::Festival.exhibition_menu          # or .exhibition(:SHIV)
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
Data tables are in `012_Narrative_Data.rb`. They're SAMPLE keys until `design/NARRATIVE_KEYS.md` exists; then transcribe them there.
State is saved in `Prismfall.state.narrative` (save file, not switches). Unregistered keys still work, with a console warning in debug.
- **Bonds** `BONDS` (default range -10..10, per-character `:start`), tiers `BOND_TIERS` (:hostile, :wary, :neutral, :friendly, :close, :devoted).
- **Standing** `FACTIONS` (:HOLLOW, :MERIDIAN, :ACCORD), tiers `STANDING_TIERS`.
- **Resonance** is one integer from -10 (Ruin) to +10 (Harmony). Bands: :ruin, :ruin_leaning, :balanced, :harmony_leaning, :harmony.
- **Choices** `CHOICES[key] = { :values, :once }`. Every decision is logged with play time and map ID. `:once` choices can't be changed.
```
Script: pf_bond_add(:JUNO, 1)              # quiet
Script: pf_bond_add(:KESTREL, -2, true)    # with "Kestrel will remember that."
Script: pf_standing_add(:HOLLOW, 1)
Script: pf_resonance_add(-1)               # toward Ruin (+ = Harmony)
Script: pf_choose(:mourner_fate, :spare)
Conditional Branch > Script: pf_choice(:mourner_fate) == :spare
Conditional Branch > Script: pf_bond(:JUNO) >= 3
Conditional Branch > Script: pf_cond("bond(:JUNO) >= 3 && standing(:ACCORD) > 0")
```
In Ruby: `Prismfall::Bonds.get/set/add/tier`, `Prismfall::Standing.*`, `Prismfall::Resonance.value/shift/band`,
`Prismfall::Choices.get/make/made?/log`. Every change fires `:prismfall_narrative_changed (kind, id, old, new)`.

## 9. Condition strings (safe subset, no eval)
These are used by draws and ending rules, and are available to any data table through `Prismfall.cond(str)` / `pf_cond(str)`.
Operators: `&& || !` (or `and or not`), `== != >= <= > <`, `+ -`, and parentheses. Literals: integers, `:symbols`,
`"strings"`, `true false nil`. Only these functions exist:
`bond(:ID) bond_tier(:ID) standing(:F) standing_tier(:F) resonance resonance_band choice(:K) made(:K) chose(:K, :V)
badges has_badge(N) difficulty level_cap starter_slot starter_gen password(:ID) gameover_found(:ID) gameovers_found
ending_seen(:ID) ruin_unlocked ruin_route festival_stage eliminated(:ID) switch(N) var(N)` (switches and variables are read-only).
`nil` counts as 0 in arithmetic and `< >` comparisons. Use `Prismfall::Conditions.check(str)` → `[ok, error]` to validate.
To add a function, add a line to `Conditions::FUNCTIONS`.

## 10. Story game overs + checkpoints
`GAME_OVERS[id] = { :title, :epitaph, :hint, :me, :ruin_exempt }` (12 samples).
`Prismfall.game_over(:GO_X)` does the following:
1. Records the ID in the Ledger.
2. Fades BGM/BGS.
3. Shows a code-drawn dark screen: "GAME OVER", the red title, the epitaph and the Ledger progress.
4. Offers **Load last save** (only if a save exists) or **Return to title**.
5. Ends the event and leaves the map through the vanilla return-to-title flag. *Load last save* redirects that one title call to a scene that loads Game.rxdata.

Call it from map or common events, not from inside a battle. `Prismfall.checkpoint` saves like the Save menu, so place it
**before** a risky scene's trigger, not inside an autorun that would re-run on load.
```
Script: Prismfall.checkpoint
...
Text: (the player chooses to follow the Hollow into the pyre)
Script: Prismfall.game_over(:GO_HOLLOW_PYRE)
# Battle-loss game over:
Script: setBattleRule("canLose")
Conditional Branch > Script: !Prismfall.rival_battle(:RIVAL_KESTREL, "Kestrel", 6)
   Script: Prismfall.game_over(:GO_VANES_FALL)
```

## 11. Ledger (cross-save)
The Ledger is a text file next to the save, `Prismfall_Ledger.txt` in `System.data_directory`. It holds the game overs
found and endings seen, and survives new games. **Ruin Route unlocked** = every registered game over (minus `:ruin_exempt`) found.
View it with `Prismfall::Ledger.show` or from the pause-menu "Ledger" entry, which appears once anything is recorded. Unfound
entries show as "???"; set `LEDGER_SHOW_HINTS` to show the `:hint` text instead.
```
Conditional Branch > Script: Prismfall::Ledger.ruin_unlocked?
   Script: Prismfall.start_ruin_route        # sets this save's Ruin Route flag (condition: ruin_route)
```

## 12. Endings
`ENDINGS[id] = { :name, :kind (:good/:bad/:grey/:ruin), :common_event, :credits }`. `ENDING_RULES` is an ordered list of
`[id, condition]` with `DEFAULT_ENDING` as the fallback. There are 7 samples: 1 good, 1 bad, 4 grey, 1 ruin.
`Prismfall.trigger_ending(:END_X)` does the following:
1. With no ID, it uses `Prismfall::Endings.determine`.
2. Records the ending in the Ledger.
3. Sets this save's post-game state (`narrative[:ending]`, `[:endings]`, `[:postgame]`) and unlocks the cap.
4. Fires `:prismfall_ending (id, first_time)` and the optional `Endings::HOOK` proc.
5. Runs the ending's common event, then the credits if `:credits` is set. After the credits the map returns and the calling event continues.
```
Script: pf_choose(:final_decision, :restore)
Script: Prismfall.trigger_ending            # determined from the rules
Script: pbMessage("...epilogue text after the credits...")
Conditional Branch > Script: Prismfall::Endings.postgame?
```

## 13. New-game passwords
`Prismfall::Passwords.prompt` asks "Would you like to enter a password?", then takes passwords until a blank entry. It then
closes, because passwords are new-game only. Put it in the intro right after `Prismfall.choose_difficulty`, or before it:
the Hard Lock password restricts the choice to Hard. The table is `Passwords::TABLE`; add a row to add a password.

| Word | ID | Effect |
|---|---|---|
| `nocap` | :NO_LEVEL_CAPS | caps disabled for the save |
| `fullivs` | :FULL_IVS | player-owned Pokémon calculate stats with 31 in every IV |
| `noexpall` | :EXP_ALL_OFF | `has_exp_all` and the Exp. All item read as off |
| `monotype` | :MONOTYPE | asks for a type; Pokémon without it can't battle (they count as fainted in battle) |
| `hardonly` | :HARD_LOCK | sets Hard; difficulty menus only offer Hard |
| `litemode` | :LITEMODE | overrides: Exp ×2, no disobedience, AI skill ≤ 32 |
Passwords that change tunables do it through `:overrides`, which `Prismfall::Difficulty.setting` checks first.
Conditions can test them with `password(:MONOTYPE)`.

## Open questions (need the user)
1. **Hard mode Bag lock:** this also blocks Poké Balls and items in *trainer* battles only; wild battles stay open. Is that right?
