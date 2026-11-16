# BOSSES — `Prismfall Bosses` plugin (Rejuvenation-style multi-bar bosses)

Plugin folder: `plugins/Prismfall Bosses/` (Essentials v21.1, Ruby 3.1-safe). `meta.txt`: `Requires = Prismfall Core`,
`Optional = Elite Battle: DX,1.4.7`, `Optional = Prismfall Field Effects,1.0.0`. Works with or without EBDX.

| File | Contents |
|---|---|
| `001_Bosses_Config.rb` | tunables: Festival switch, default immunities, messages, pip look/offsets |
| `002_Bosses_Registry.rb` | `register`, difficulty-keyed values, `create_pokemon` / `make_boss` / `strip`, `Pokemon#calc_stats` stat multipliers |
| `003_Bosses_State.rb` | per-battle `BossState` (bars, pending break, immunities, catch rule) |
| `004_Bosses_Battle.rb` | battle-layer hooks: HP, statuses, Poké Balls, AI, entry, end of battle |
| `005_Bosses_Effects.rb` | bar breaks, defeat scripts, on-break effects, summon, PRISM_ARENA follow |
| `006_Bosses_Start.rb` | event helpers, trainer bosses, EBDX intro styling, Festival switch |
| `007_Bosses_UI.rb` | bar pips on the EBDX databox or the vanilla databox |
| `008_Bosses_Debug.rb` | Debug > **Prismfall Bosses...** |
| `101`–`104` | examples: Kyogre (Isenmar), Zekrom (Zenith), Arceus True Finale, Hard Warden aces |

## 1. How it works
- A boss is a Pokémon tagged with a boss ID (`pkmn.prismfall_boss_id`, a Symbol, so it's save-safe). Bar state lives on
  the battle, keyed by the Pokémon object, so a trainer's ace keeps its bars across switching.
- **Bar break.** `Battle::Battler#pbReduceHP` is alias-chained. When HP loss would take a boss with bars left to 0, HP
  stops at 1 and the bar is marked *pending*. The excess is discarded, so **overflow never carries**, and further damage
  (extra hits of a multi-hit move, a partner's hit in the same move) is absorbed. The move's `damageState.hpLost` is
  trimmed so animations and drain stay correct. The break resolves at the next safe point: after `pbUseMove`, after
  `pbTakeEffectDamage` (poison, weather, recoil, hazards...), at the end of the round, or before `pbJudge`. Resolving
  shows `"{1}'s shield shattered!"`, refills HP to full (or `:refill`) and runs the on-break script.
- **Last bar.** Damage works normally and the boss faints, unless an `:on_defeat` effect has `:end_battle`/`:survive`
  and its condition holds. Then it stays at 1 HP, the script runs and the battle ends with that decision
  (Kyogre "calms", Zekrom "breaks free").
- **Statuses.** While bars remain, `pbCanInflictStatus?`, `pbCanSynchronizeStatus?`, `pbCanSleepYawn?`,
  `pbCanConfuse?` and `pbCanAttract?` refuse the listed statuses ("{1}'s shield repelled the effect!"). Self-inflicted
  ones (Rest, Flame Orb) still work. EBDX's own boss immunity flag is switched off for our bosses so only this config applies.
- **AI.** Wild bosses get trainer skill 100 (best-skill v21 AI, `:ai_skill` to change). Trainer bosses use their trainer's
  skill (Core's difficulty floor applies). `:ai_script` forces moves per bar, turn by turn.
- **Capture.** By default bosses can't be caught: Poké Balls are disabled (no ball is used up), and a thrown ball is deflected as a fallback.
  `:catch => :last_bar` re-enables balls on the last bar. `:catch => true` always allows them.
  A caught boss loses its tag and stat multipliers before it's stored.
- **Cleanup.** At the end of battle every Pokémon is untagged and its stats are recalculated.

### EBDX and the Renovation fork
- Wild bosses use EBDX's boss databox: `:nextUI` is set like `EliteBattle.bossBattle` does, and so is `:setBoss`, which in the
  Renovation fork also gives the red name outline, hides the level and adds the S/M intro styling. `:ebdx => { :databox => false }` turns this off.
- **Pips.** In EBDX, an extra sprite in the databox's `@sprites` follows EBDX's own move/fade/dispose loops. It sits at
  `EBDX_PIP_OFFSET` from the HP bar. Without EBDX, pips are drawn on the vanilla databox bitmap at `VANILLA_PIP_POS`.
  Optional art: `Graphics/UI/Prismfall/boss_pips.png` (2 frames side by side: full, empty). Without it, the pips are drawn in code.
- **Renovation's HP-threshold scripting** (`:damageCap` / `EliteBattle.defineBoss`) runs in the scene layer, inside
  the HP-bar animation (`pbHitAndHPLossAnimation`/`pbHPChanged`). It clamps HP at a % but never refills, fires only
  `"HPCap<pct>"` battle-script speech, and needs the EBDX scene. So the mechanic lives at the battle layer and clears
  `:damageCap` for our bosses. The plugin still builds on Renovation's battle-script system: every break calls
  `pbTrainerBattleSpeech("bossBreak<n>")`, so an EBDX `BattleScripts` hash (`:ebdx => { :script => :MY_SCRIPT }`) can
  add `"bossBreak1"` dialogue or procs. `:speech => "key"` fires any key. Renovation's SOS helper
  (`pbGenerateAllyBattler`) is used for `:summon` when it's present.
- `EliteBattle.bossBattle` itself is not used. Its `:bossboost` equivalent is `:stat_mults`.

## 2. Definition reference — `Prismfall::Bosses.register(:ID, { ... })`
Any value marked *D* may be a difficulty Hash `{ :CASUAL => x, :STANDARD => y, :HARD => z, :default => w }` or a proc.

| Key | Meaning |
|---|---|
| `:species`, `:level` *D* | required for wild bosses. Trainer bosses keep the PBS Pokémon |
| `:form` *D*, `:nickname`, `:shiny`, `:gender` | |
| `:moves` *D* | up to 4 move IDs (replaces the moveset) |
| `:ability`, `:ability_index`, `:item`, `:nature`, `:ivs` (Integer = all, or Hash), `:evs` (Hash) | |
| `:bars` *D* | number of HP bars (default 2) |
| `:stat_mults` *D* | `{ :HP => 1.0, :ATTACK => 1.25, ... }` multiplies stats (`:HP` raises max HP) |
| `:status_immunity` *D* | `true` (default) = `DEFAULT_IMMUNITIES` (5 majors + Yawn), `:all` (+ confusion, attract), `false`, or a list |
| `:immunity_last_bar` *D* | keep immunities on the last bar (default false) |
| `:catch` *D* / `:catch_rate` | `false` (default), `true`, `:last_bar` / override catch rate |
| `:can_run` *D* | wild boss battles are `cannotRun` unless true. `:can_lose` adds `canLose` |
| `:size` *D* | battle size rule, e.g. `"2v1"` (EBDX bossBattle style) |
| `:field`, `:weather`, `:terrain` *D* | battle-start rules (`:field` needs Field Effects). Rules an event already set win |
| `:music` *D* | battle BGM (`$PokemonGlobal.nextBattleBGM`) |
| `:intro` *D* | message(s) when the boss first enters |
| `:break_message` | replaces `BREAK_MESSAGE` (`""` = none) |
| `:on_break` | effects run on **every** break (Hash or list of Hashes) |
| `:breaks` | `{ n => effects }`: when bar *n* is depleted (1 = first bar) |
| `:on_defeat` | effects when the last bar is depleted. Those with `:end_battle`/`:survive` prevent the faint; the others run just before the faint |
| `:ai_skill` *D*, `:ai_script` *D*, `:ai_script_loop` | `:ai_script => { 1 => [:CALMMIND, nil, :JUDGMENT] }` (bar => one move per turn; `nil` = AI picks). It ends after its last entry unless looped |
| `:follow_prism` | `{ :form => true, :form_message, :movesets => { :FIRE => [...], :default => [...] } }`: follows PRISM_ARENA's ascendant Plate |
| `:prism_interval` *D* | sets the arena's writable `:interval` (rounds per turn) |
| `:ebdx` | `{ :databox => true/false, :script => :BattleScriptName }` |

### Effect keys (inside `:on_break` / `:breaks` / `:on_defeat`)
They're applied in this order. `{1}` in messages is the boss (`"The wild Kyogre"`). Every effect may have
`:condition => proc { |battle, battler, state| bool }`.

`:message`/`:messages` · `:animation` (common anim) · `:speech` (EBDX battle-script key) · `:cure_status` (`:all` also
cures confusion) · `:reset_stats` (`true` or `:negative`) · `:form` (Integer or `:match_type`) + `:form_message` ·
`:types` · `:ability` · `:item` · `:moves` (replace) · `:learn` (`{ slot => :MOVE }` or list) · `:stats` (`{ :SPEED => 1 }`) ·
`:field` + `:field_message` (`battle.change_field`) · `:prism_turn` (PRISM_ARENA's announced `:turn`) · `:weather`
(+ `:weather_permanent`) · `:terrain` (+ `:terrain_permanent`) · `:clear_hazards` (`true` = boss's side, `:foe`, `:both`) ·
`:clear_screens` (`true` = player's side) · `:heal_allies` (fraction) · `:summon` (`{ :species, :level, :moves, :item,
:ability, :boss, :message }`) · `:music` (phase BGM) · `:primal` (gives the orb and runs Primal Reversion) ·
`:proc` (`|battle, battler, state|`) · `:result` (Symbol stored in `last_result`) · `:end_battle` (`true`/1 = win, or a
decision) · `:refill` (next bar's HP fraction, default 1.0, break only).

## 3. Event usage
```
# Wild boss (cannotRun, field/weather from the definition):
Conditional Branch > Script: Prismfall::Bosses.wild_battle(:KYOGRE_ISENMAR)
   Conditional Branch > Script: Prismfall::Bosses.last_result[:result] == :calmed
Script: Prismfall::Bosses.wild_battle(:ZEKROM_ENGINE, can_lose: true, field: :NONE)
# Trainer whose ace is a boss (:MOURNER_TREVENANT is a hypothetical definition):
Script: Prismfall::Bosses.trainer_battle(:HOLLOW_MOURNER, "Mourner", 0, boss: :MOURNER_TREVENANT, species: :TREVENANT)
# Wrap another helper (one-shot, consumed by the next trainer load):
Script: Prismfall::Bosses.mark_next_trainer(:WARDEN_ACE_2BAR)
Script: Prismfall.gym_battle(12)
# Standing rule (e.g. Hard mode):
Prismfall::Bosses.register_trainer_boss(:KEY, { :trainer_type => :LEADER_NYX, :versions => [0, 100],
  :condition => proc { |tr| Prismfall::Difficulty.hard? }, :slot => :ace, :boss => :WARDEN_ACE_2BAR })
# Custom battles: Prismfall::Bosses.create_pokemon(:ID) / make_boss(pkmn, :ID), then start the battle yourself.
```
`last_result` → `{ :id, :bars, :bars_left, :breaks, :defeated, :result, :decision, :all => [...] }` (after any boss battle).
Events other plugins can listen to: `:prismfall_boss_starting (id, pkmn)`, `:prismfall_boss_entered (battle, battler, id)`,
`:prismfall_boss_bar_broken (battle, battler, id, n, bars_left)`, `:prismfall_boss_defeated (battle, battler, id, result)`,
`:prismfall_boss_battle_ended (battle, last_result)`.

## 4. Shipped examples
| ID | Bars (C/S/H) | Notes |
|---|---|---|
| `:KYOGRE_ISENMAR` | 2/3/3 | Lv 55 on `:FROZEN_LAKE`. Break 1: lake cracks to `:WATER_SURFACE`, learns Water Spout, SpA +1. Break 2: Primal Reversion, Origin Pulse set, the shard hums. Last bar on a **Harmony lean** (Resonance band) → "calmed" (no faint, result `:calmed`); otherwise it faints (`:defeated`). |
| `:ZEKROM_ENGINE` | 2/3/4 | Lv 72 on `:FACTORY`. Each break "snaps a containment cable", Atk +1. Break 2: `:FACTORY → :SCRAPYARD`, learns Bolt Strike. Opens with Hone Claws (`:ai_script`). Last bar → breaks free (result `:freed`). |
| `:ARCEUS_FINALE` | 3/3/4 | Lv 100 on `:PRISM_ARENA`, BALANCE.md §7 stats/EVs, stat ×1.1/1.25/1.3, immunities on every bar. Every break: "The Plates answer their god!", then a **forced Plate turn through the arena's own `:turn`** (so the arena's announcements stay consistent; Multitype re-types), negative stages reset, status cured. Then Arceus swaps form/sprite + BALANCE moveset to the new type. The arena's regular turns are followed the same way. `ARCEUS_LEGEND_PHASE = true` enables BALANCE's Legend-Plate last bar (??? form, field by Resonance). |
| `:WARDEN_ACE_2BAR` | 2 | template. Rules `:HARD_ILSA` / `:HARD_CELESTINE` make the **last** Pokémon of Ilsa's/Celestine's gym team a 2-bar boss on Hard (versions 0/100 only, never Festival v50). Break: cure, reset drops, Def/SpDef +1. |

### Festival switch (Core)
`Prismfall::Festival.boss_battle` is alias-chained. A stage runs this plugin's boss if `stage[:prismfall_boss]` names
one, or else `FESTIVAL_BOSSES[stage[:id]]` does (`:ARCEUS => :ARCEUS_FINALE`). `:prismfall_boss => false`,
`USE_FOR_FESTIVAL = false` or the debug toggle falls back to Core's EBDX `bossBattle` path. `next_match` still applies the stage's rule set,
field (`:PRISM_ARENA`), `cannotRun`/`disablePokeBalls`, cap and heals, and `:prismfall_festival_boss (pkmn, :ARCEUS)` still
fires with the boss Pokémon. No Core edits are needed. Optionally, Core can add `:prismfall_boss => :ARCEUS_FINALE` to the stage to make the link explicit.

## 5. Debug
Debug > **Prismfall Bosses...**: start any registered wild boss (with canLose, then shows the result), Arceus True Finale,
Hard Warden ace (Ilsa/Celestine Hard team, 2-bar ace), and toggle the Festival switch.

## 6. Verification
`ruby -c` passes on every file. A stub harness (`/tmp/bosses_test/test.rb` + `test_ebdx.rb`, 59 checks, all passing)
loads the plugin against minimal Essentials stubs that use v21's real `pbReduceHP`/`pbRecoverHP` logic. It covers:
- breaks from move damage (3-hit move: first hit trimmed to hp-1, later hits absorbed, exact full refill) and from effect damage
- every on-break effect used by the examples, statuses and immunity drop, the calm/free/faint defeat paths, and ball deflection
- difficulty-keyed bars and stat multipliers, the scripted AI move and wild AI skill 100
- the PRISM_ARENA turn on a break plus natural-turn follow (form and moveset)
- trainer rules (Hard only, ace slot, v50 untouched), the Festival switch on/off, vanilla and EBDX pips, EBDX setup and the SOS summon
All move, ability, item, species and type IDs were checked against the base project PBS.

## 7. Limitations
- Not run in the real engine yet. The pip offsets (`EBDX_PIP_OFFSET`, `VANILLA_PIP_POS`) and the boss-databox look need an in-game check.
- `:summon` without the Renovation SOS helper only fills an existing **fainted** slot on the boss's side, so start the
  battle as `1v2`/`2v2` for that. In trainer battles it shows "...but no help came!".
- One-hit KO moves, Destiny Bond, Perish Song, Explosion and similar effects break one bar, not the whole boss. Sturdy and Focus Sash work on every bar, since each bar refills to full.
- Bars are per Pokémon. Exp is only awarded when the boss finally faints, so a calmed or freed boss gives no Exp.
- A `:pending_trainer` mark that's never consumed (the battle was skipped) applies to the next trainer load.
- `:breaks` keys can't be difficulty Hashes. Use effect `:condition`s instead.
- The Hard Warden rule checks `Prismfall::Difficulty.hard?`. A Hard player always gets the boss ace, even if a team
  has no v+100 variant.
