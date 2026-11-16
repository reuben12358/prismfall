# Prismfall Field Effects — DSL & API Reference (v1.0)

Plugin: `plugins/Prismfall Field Effects/` (Essentials v21.1). Core engine = files `001_`–`009_` (009 = Field Notes
encyclopedia: records each field the player battles on in save data `:prismfall_field_notes`; pause-menu entry "Field Notes").
**Each field lives in its own file `1xx_Field_<Name>.rb` that only calls `FieldEffects.register`.**
Never edit the core files to add a field. Validate with `ruby tools/validate_fields.rb` (must print 0 errors).

Implemented reference fields (copy their style): `101_Field_Silkwood.rb` … `111_Field_Bleed.rb`.
File numbers already used: 101–111. Pick a free number ≥ 112 for new fields (gym fields 112–129, story fields 130+).

---------------------------------------------------------------------------------------------------
## 1. Integration contract (LOCKED, from SPINE)

| What | How |
|---|---|
| Set field for next battle | `setBattleRule("field", :VOLCANIC)` (Symbol or String; `"none"` = no field, overrides map default) |
| Default field per map | `FieldEffects::MAP_FIELDS[map_id] = :FIELD_ID` or `[:FIELD_ID, stage]` (plain Hash; add entries from any plugin that loads after this one) |
| Starting stage | `setBattleRule("fieldStage", 3)` (overrides the MAP_FIELDS stage; default 1) |
| Current field in battle | `battle.field_effect` → Symbol, `:NONE` if none |
| Change field mid-battle | `battle.change_field(:NEW_ID, "message")` → true if changed. `message` nil ⇒ new field's `:intro_message` is shown; `""` ⇒ nothing shown |
| Change event | every change calls `FieldEffects.notify_change(battle, old_id, new_id)` → `EventHandlers.trigger(:prismfall_field_changed, battle, old_id, new_id)` |

Event timing: at battle start (after send-out, before the intro text) `:prismfall_field_changed` fires once with
`old_id = :NONE`. `battle.field_effect` is already set from `prepare_battle` onward, so scene-creation code may read it.
A **stage** change (§7) also fires `:prismfall_field_changed` with `old_id == new_id`; read
`FieldEffects.backdrop_for(battle)` for the stage-aware backdrop.
Extra (non-LOCKED) event: `:prismfall_field_overlay_changed (battle, field_id, old_borrowed_ids, new_borrowed_ids)`
fires when a `:borrow` field (e.g. `:BLEED`) rotates the fields it borrows from.

### Other public helpers
```ruby
FieldEffects.register(:ID, {...})          # define a field
FieldEffects.get(:ID) / FieldEffects[:ID]  # frozen definition Hash (or nil)
FieldEffects.exists?(:ID), FieldEffects.ids, FieldEffects.name_of(:ID)
FieldEffects.current(battle)               # same as battle.field_effect but nil-safe
FieldEffects.field_is?(battle, :A, :B)     # current field is one of these
FieldEffects.current_definition(battle)    # definition with the current stage applied
FieldEffects.backdrop_for(battle)          # stage-aware :backdrop of the current field
FieldEffects.stage(battle) / battle.field_stage
battle.set_field_stage(n, "message")       # see §7
FieldEffects.state(battle)                 # scratch Hash for your procs; cleared on field change
FieldEffects.rotate_borrowed(battle)       # force a :borrow rotation now
FieldEffects.borrowed_fields(battle)       # [ids] currently borrowed (:BLEED/:PRISM_ARENA); borrowed_field = first or nil
FieldEffects.prism_state(battle)           # frozen { :field, :type, :plate, :next_field, :next_type, :next_plate,
                                           #   :rounds_left, :rotation, :interval } while PRISM_ARENA is active, else nil
FieldEffects.transition_progress(battle, :id)  # [count, uses] of a transition with that :id
```
Field definitions' messages are plain strings; the engine runs them through `_INTL` with arguments at display time.
**Do not call `_INTL` in field files.**

> **Plugin scope warning.** Essentials evals every plugin file into the same `TOPLEVEL_BINDING`, so a top-level
> local variable (`blades = [...]`) or `def` in a field file is visible to — and can collide with — every later file.
> Put helpers inside the call: `FieldEffects.register(:ID, (lambda do; helpers...; { ...definition... }; end).call)`
> (see `113_Field_FlowerGarden.rb`, `130_Field_Cave.rb`). Never define top-level locals, methods or constants.

---------------------------------------------------------------------------------------------------
## 2. Minimal field

```ruby
FieldEffects.register(:CAVE, {
  :name          => "Cave",
  :backdrop      => "field_cave",          # base name of Graphics/Battlebacks/<backdrop>_bg etc.
  :intro_message => "The cave walls loom close.",
  :description   => "Echoing chamber. Sound moves and Rock moves are stronger.",  # optional, docs/debug
  :type_mods     => { :ROCK => 1.5, :FLYING => 0.5 },
  :type_messages => { :ROCK => "The cavern rumbled!" },
  :damage_mods   => [{ :flags => ["Sound"], :mult => 1.5, :message => "{2} echoed through the cave!" }]
})
```
Required keys: `:name`, `:backdrop`, `:intro_message`. Everything else is optional.

### Conventions
* IDs are Symbols exactly as in PBS: types `:FIRE`, moves `:SURF`, abilities `:FLASHFIRE`, items `:CHARCOAL`,
  stats `:ATTACK :DEFENSE :SPECIAL_ATTACK :SPECIAL_DEFENSE :SPEED :ACCURACY :EVASION`.
* Statuses: `:SLEEP :POISON :TOXIC :BURN :PARALYSIS :FROZEN` (`:TOXIC` = badly poisoned; `:NONE` only in matchers).
* Weather IDs: `:Sun :Rain :Sandstorm :Hail :HarshSun :HeavyRain :StrongWinds :ShadowSky`.
  Terrain IDs: `:Electric :Grassy :Misty :Psychic`.
* Move flags (base project PBS, Gen 9 Pack): `Contact CanProtect CanMirrorMove ThawsUser HighCriticalHitRate Biting
  Punching Sound Powder Pulse Bomb Dance CannotMetronome TramplesMinimize Slicing Wind`. Only a handful of moves carry
  `Slicing`/`Wind` — for wind/cutting themes also list the classic moves explicitly with `:moves`.
* IDs are validated against `/home/claude/ref/ebdx/PBS` (Essentials 21.1 + Gen 9 Pack: Gen 1–9 moves/abilities/items).
* Fractions of max HP: use Rationals or Floats — `1/8r` or `0.125`. **Never `1/8`** (Integer division = 0;
  the validator flags it).
* Any single-element list may be written without brackets (`:types => :FIRE`).
* Message placeholders: see each key. `{1}` is almost always the acting battler's name (`pbThis`), `{2}` the move name.

---------------------------------------------------------------------------------------------------
## 3. Matchers (shared grammar)

### 3.1 Move matcher — usable in every rule list marked **[M]**
All keys present must match (AND); list values match if ANY element matches (OR).

| Key | Value | Matches when |
|---|---|---|
| `:moves` | [move IDs] | move ID is in list |
| `:not_moves` | [move IDs] | move ID is NOT in list |
| `:types` | [type IDs] | move's type **this use** (after field type changes, Ion Deluge…) is in list |
| `:not_types` | [type IDs] | move's type is not in list |
| `:flags` | ["Sound", …] | move has any listed flag (`"Contact"` respects Long Reach) |
| `:category` | `:physical` `:special` `:status` `:damaging` (or list) | |
| `:function_codes` | ["FunctionCode", …] | move's PBS FunctionCode is in list |
| `:user` | battler matcher (§3.2) | the move's user matches |
| `:target` | battler matcher | the (current) target matches. Rules evaluated without a target (type changes, priority, move fails) never match a rule containing `:target` |
| `:condition` | `proc { \|battle, user, target, move, type\| bool }` | escape hatch; `target` may be nil |

### 3.2 Battler matcher — used by `:user`, `:target`, `:battlers`
| Key | Value | Matches when |
|---|---|---|
| `:types` / `:not_types` | [types] | battler has any / none of these types |
| `:abilities` / `:not_abilities` | [abilities] | battler has (active) any / none of these abilities |
| `:items` / `:not_items` | [items] | battler holds (active) any / none of these items |
| `:grounded` | true / false | `true` = not airborne (Flying, Levitate, Air Balloon, Magnet Rise… are airborne) |
| `:status` | [statuses] | battler's status is listed (`:TOXIC` also matches poison) |
| `:condition` | `proc { \|battle, battler\| bool }` | escape hatch |

Example: `:user => { :types => [:BUG], :grounded => true }`.

---------------------------------------------------------------------------------------------------
## 4. Effect keys

### 4.1 Identity
| Key | Type | Notes |
|---|---|---|
| `:name` | String | **required** |
| `:backdrop` | String | **required**. Also used as vanilla battleback if `Graphics/Battlebacks/<backdrop>_bg` exists |
| `:intro_message` | String | **required**. Shown at battle start and after a change with no message |
| `:description` | String | optional one-liner (shown in Field Notes, the in-game field encyclopedia) |
| `:notes` | [String] | optional Field Notes bullet lines; if omitted they are generated from the definition |
| `:nature_power` | move ID | Nature Power becomes this move (a built-in terrain still takes precedence) |
| `:camouflage` | type ID | Camouflage makes the user this type |
| `:secret_power` | Integer | Secret Power's effect code: 0/1 paralyze, 2 sleep, 3 Sp.Atk−1, 4/6/12 Speed−1, 5 Atk−1, 7/11/13 flinch, 8 Acc−1, 9 freeze, 10 burn, 14 Def−1 |

### 4.2 Damage
| Key | Format | Effect |
|---|---|---|
| `:type_mods` | `{ TYPE => mult }` | base power × mult for moves of that type this use |
| `:type_messages` | `{ TYPE => "text" }` | shown (once per move use) when that `:type_mods` entry applies. `{1}` user, `{2}` move |
| `:move_mods` | `{ MOVE => mult }` | base power × mult for that move (stacks with `:type_mods`) |
| `:move_messages` | `{ MOVE => "text" }` | shown when that `:move_mods` entry applies |
| `:damage_mods` **[M]** | list of rules | each matching rule applies: `:mult` (base power), `:attack_mult`, `:defense_mult`, `:final_mult` (final damage), optional `:message` (`{1}` user, `{2}` move) |

All damage modifiers multiply into Essentials' normal `multipliers` hash, after weather/terrain/abilities, so they stack.
Messages appear once per move use (not per target/hit), just before the attack animation.

```ruby
:damage_mods => [
  { :moves => [:SCALD, :STEAMERUPTION], :mult => 1.3, :message => "The heat super-charged the steam!" },
  { :types => [:FIRE], :target => { :grounded => true }, :final_mult => 1.2 },
  { :category => :physical, :user => { :abilities => [:SANDFORCE] }, :attack_mult => 1.2 },
  { :types => [:WATER], :target => { :types => [:FIRE] }, :mult => 0.5 }  # defensive nerf example
]
```

### 4.3 Type & effectiveness
| Key | Format | Effect |
|---|---|---|
| `:type_changes` **[M]** | rules with `:to => TYPE`, optional `:message` | move's type becomes `:to` (first matching rule per field wins). Feeds STAB, effectiveness, the AI. `:target` keys never match here |
| `:extra_types` **[M]** | rules with `:add => TYPE`, optional `:message` | move additionally deals `:add`-type effectiveness (Flying Press style). An added type the target is immune to counts as neutral |
| `:effectiveness_mods` | rules `{ :attack => [types], :defend => [types], :moves => [opt], :set => 1.0 / :mult => 2.0 }` | per single matchup (one defending type). Omit `:attack`/`:defend` to mean "any" |
| `:inverse` | `true` | Inverse chart: immune/resisted ⇒ 2×, super effective ⇒ 0.5× (airborne still dodges Ground) |

### 4.4 Accuracy, priority, crits, secondary-effect chance
| Key | Rule keys | Effect |
|---|---|---|
| `:accuracy_mods` **[M]** | `:mult` (accuracy ×), `:evasion_mult` (target evasion ×), `:set` (base accuracy), `:always_hit => true` | |
| `:priority_mods` **[M]** | `:add => Integer` | priority bracket change (target-less rule) |
| `:crit_mods` **[M]** | `:add => Integer` (crit stages), `:always => true` | Battle Armor/Lucky Chant still apply |
| `:effect_chance_mods` **[M]** | `:set => Integer` or `:mult => Float` | changes the chance of the move's OWN secondary effect (e.g. Scald burn 30→50). Moves without one are unaffected |
| `:fixed_damage_mods` **[M]** | `:set => Integer` (HP) or `:mult => Float`, optional `:message` | fixed-damage moves (Dragon Rage, Sonic Boom, Seismic Toss, Night Shade, Super Fang, Counter, Endeavor, OHKO…) ignore every other damage key; use this. e.g. `{ :moves => [:DRAGONRAGE], :set => 140 }`. AI-aware |
| `:weather_as` **[M]** | `:as => WEATHER` | the matching move's user sees that weather (only while no real weather is up) for the whole move use, e.g. `{ :moves => [:AURORAVEIL], :as => :Hail }`. Affects the user's own weather checks only (the move's failure check, its user-side effects); the AI knows |

### 4.5 Added effects & stat boosts on use
`:added_effects` **[M]** — extra secondary effects rolled **per hit per target** after damage
(skipped by Sheer Force, Shield Dust, Substitute; Serene Grace doubles chance):

| Rule key | Meaning |
|---|---|
| `:chance` | Integer 1–100 (default 100) |
| `:apply_to` | `:target` (default) or `:user` |
| `:status` | status to inflict (normal immunities apply) |
| `:confuse` / `:flinch` | `true` |
| `:stats` | `{ STAT => ±n }` |
| `:message` | replaces the default status text / shown before stat change. `{1}` affected battler, `{2}` move |
| `:proc` | `proc { \|battle, user, target, move\| }` |

```ruby
:added_effects => [{ :types => [:FIRE], :category => :damaging, :chance => 10, :status => :BURN,
                     :target => { :grounded => true }, :message => "{1} was scorched by the magma!" }]
```

`:move_stat_boosts` **[M]** — after a move is used successfully (not on a two-turn charging turn):
`:user_stats => { STAT => n }`, `:target_stats => { STAT => n }` (applied to each affected target),
`:message` (`{1}` user, `{2}` move; shown once if anything changes).
```ruby
:move_stat_boosts => [{ :moves => [:GROWTH], :user_stats => { :ATTACK => 1, :SPECIAL_ATTACK => 1 },
                        :message => "The fertile ground fed {1}'s growth!" }]
```

`:move_fails` **[M]** — the move fails on this field: "X used Y!" + `:message` (`{1}` user, `{2}` move;
default "But it failed!"). PP is consumed. The AI knows (won't pick it).

### 4.6 Battler effects: `:end_of_round`, `:on_entry`
Both are lists of **battler-effect rules**, each applied to every battler matching `:battlers`.
* `:end_of_round` — each round, after terrain countdown, before EOR abilities/items (Speed Boost etc.).
* `:on_entry` — when a battler enters (start of battle included), right after entry hazards, before its switch-in
  ability. Add `:also_on_change => true` to also apply to active battlers when the field starts mid-battle.

| Rule key | Meaning |
|---|---|
| `:battlers` | battler matcher (omit = everyone) |
| `:chance` | Integer % per battler |
| `:damage` | fraction of max HP (`1/8r`); respects Magic Guard |
| `:damage_type` | scales `:damage` by that type's effectiveness vs. the battler (Stealth Rock style; immune ⇒ no damage) |
| `:heal` | fraction of max HP (Heal Block respected) |
| `:cure_status` | `true` |
| `:status` | inflict status (immunities apply) — `:message` replaces the default "was burned" text |
| `:confuse` | `true` |
| `:stats` | `{ STAT => ±n }` (drops respect Mist / Clear Body) |
| `:effects` | named effects: `:ingrain :aqua_ring :magnet_rise :focus_energy :laser_focus :charge :defense_curl :minimize :smack_down :telekinesis :flash_fire :stockpile` |
| `:message` | `{1}` = battler. Shown once if anything happens (with damage: after the HP drop) |
| `:animation` | common animation name (e.g. `"Burn"`, `"Poison"`, `"HealthUp"`) |
| `:proc` | `proc { \|battle, battler\| truthy-if-did-something }` |

```ruby
:end_of_round => [
  { :battlers => { :grounded => true, :not_types => [:FIRE] }, :damage => 1/16r,
    :message => "{1} was singed by the magma!" },
  { :battlers => { :abilities => [:WATERABSORB] }, :heal => 1/16r, :message => "{1} soaked up the mist." }
],
:on_entry => [{ :battlers => { :abilities => [:FLASHFIRE] }, :effects => [:flash_fire] }]
```

### 4.7 Speed & abilities
| Key | Format | Effect |
|---|---|---|
| `:speed_mods` | rules `{ :battlers => matcher, :mult => Float }` | Speed × mult (turn order + AI) |
| `:negated_abilities` | [ability IDs] | these abilities don't work on this field (unstoppable ones like Multitype excepted) |

"Ability X is buffed" = a normal rule with an ability matcher, e.g.
`{ :types => [:FIRE], :user => { :abilities => [:BLAZE] }, :mult => 1.5 }` (Blaze always active),
`:speed_mods => [{ :battlers => { :abilities => [:SANDRUSH] }, :mult => 2.0 }]` (Sand Rush without sand),
`:accuracy_mods => [{ :target => { :abilities => [:SANDVEIL] }, :evasion_mult => 1.25 }]`.

### 4.8 Weather & terrain interaction
Built-in terrains **overlay** fields by default: both apply. A field can restrict them:
```ruby
:weather => { :block => [:Hail], :block_message => "The heat melted the hail before it formed!",
              :transform => { :Rain => :Sun }, :extend => { :Sun => 3 } },
:terrain => { :block => [:Grassy, :Misty], :block_message => "...", :extend => { :Electric => 3 } }
```
* `:block` — the weather/terrain can't start (move "fails" with the message; ability splash is closed). If it is
  already active when the field starts, it ends; overworld weather is silently dropped at battle start.
* `:transform` — starting X starts Y instead (Y is then checked against `:block`).
* `:extend` — extra turns when it starts with a fixed duration.
* Starting a weather/terrain can also trigger a **transition** (§5). Nature Power/Camouflage/Secret Power use
  the terrain if one is up, else the field's `:nature_power`/`:camouflage`/`:secret_power`.

---------------------------------------------------------------------------------------------------
## 5. Transitions `:transitions`
List of rules; each has a **trigger**, a **target**, and optionally `:message` and `:uses`.

| Trigger | Keys | Fires when |
|---|---|---|
| move | any move matcher keys **[M]** (target matcher = first target) | a matching move is used and doesn't fail (`:even_if_failed => true` also counts failures — including moves that fail before hitting, e.g. "But it failed!" or a field's `:move_fails`; two-turn moves count on the charging turn) |
| weather | `:weather => [ids]` | that weather starts |
| terrain | `:terrain => [ids]` | that terrain starts |
| timer | `:turns => n` | at end of round once the field has lasted n rounds |
| check | `:check => proc { \|battle\| bool }` | evaluated at end of each round |

| Target | Meaning |
|---|---|
| `:to => :FIELD_ID` | `battle.change_field(:FIELD_ID, message)`. `:to => :NONE` clears the field. May be a `proc { \|battle\| id }` |
| `:stage => n` / `:stage_delta => ±n` | change the current field's stage (§7) instead |

`:uses => n` — needs n triggers (counted per transition, reset when the field/stage changes).
`:id => :sym` + `:rewind => :sym | [:a, :b] | { :sym => n }` — a rule with `:rewind` lowers the named transitions'
progress (min 0) when it triggers. A rule with `:rewind` and no `:to`/`:stage` only rewinds; its `:message` shows when
progress actually went down. e.g. Frozen Lake: `{ :id => :crack, :types => [:FIRE], :uses => 3, :to => :WATER_SURFACE }`,
`{ :types => [:ICE], :category => :damaging, :rewind => :crack, :message => "The ice refroze!" }`.
`:progress_message` — shown on triggers that don't complete it; `{1}` = remaining uses.
`:message` — shown on change (`nil` ⇒ the new field's intro); **no placeholders** in transition messages.
Only the first completed transition per event fires.

```ruby
:transitions => [
  { :moves => [:SURF, :MUDDYWATER, :WATERSPOUT], :to => :ASHEN_WASTE, :uses => 2,
    :progress_message => "Steam hisses from the magma... ({1} more)",
    :message => "The water quenched the magma! Ash settles over the battlefield." },
  { :weather => [:Rain, :HeavyRain], :to => :ASHEN_WASTE, :message => "The rain cooled the magma to ash!" },
  { :moves => [:DIVE], :to => :UNDERWATER, :message => "The battle plunged beneath the waves!" }
]
```
A field change never chains into another change during the same change.

---------------------------------------------------------------------------------------------------
## 6. Seeds `:seed`
One rule or a list. Each = battler-effect rule (§4.6 keys) + `:item => :ELEMENTALSEED | :MAGICALSEED |
:TELLURICSEED | :SYNTHETICSEED`. A held seed activates (and is consumed) when its holder enters battle on this field,
or when this field starts while it's in battle. `{1}` = holder, `{2}` = seed name; default message
"{1}'s {2} reacted to the field!". Seeds only read the **current** field (never borrowed ones). A field may define
effects for several seeds; seeds without an entry do nothing on that field.
```ruby
:seed => { :item => :TELLURICSEED, :stats => { :DEFENSE => 1 }, :effects => [:ingrain],
           :message => "{1}'s {2} rooted it into the silk!" }
```

---------------------------------------------------------------------------------------------------
## 7. Stages `:stages` (multi-stage fields, e.g. FLOWER_GARDEN)
`:stages => { 2 => { overrides }, 3 => { … } }` — the base definition is stage 1; each stage Hash
**replaces** the listed top-level keys (shallow merge: a stage's `:type_mods` replaces the base `:type_mods` entirely).
A stage may override any key except `:stages`/`:borrow` (e.g. its own `:backdrop`, `:transitions`, `:intro_message`).
Change stage via a transition (`:stage`/`:stage_delta`) or `battle.set_field_stage(n, msg)`.
`battle.field_stage` / `FieldEffects.stage(battle)` read it; `battle.field_effect` stays the same ID.
```ruby
FieldEffects.register(:FLOWER_GARDEN, {
  :name => "Flower Garden", :backdrop => "field_garden1", :intro_message => "Buds dot the field.",
  :type_mods => { :GRASS => 1.1 },
  :transitions => [{ :moves => [:GROWTH, :SUNNYDAY], :stage_delta => 1, :message => "The garden grew!" }],
  :stages => {
    2 => { :backdrop => "field_garden2", :type_mods => { :GRASS => 1.3 } },
    5 => { :backdrop => "field_garden5", :type_mods => { :GRASS => 2.0, :FIRE => 1.5 },
           :transitions => [{ :types => [:FIRE], :to => :ASHEN_WASTE, :message => "The garden burned!" }] }
  }
})
```

---------------------------------------------------------------------------------------------------
## 8. Borrowing `:borrow` (overlay effects from other fields — :BLEED, :PRISM_ARENA)
```ruby
:borrow => { :pool => :all,            # or [:VOLCANIC, :DESERT, ...]
             :exclude => [:INVERSE],   # never borrowed
             :interval => 3,           # rotate every 3 end-of-rounds
             :count => 1,              # fields borrowed at once
             :order => :random,        # or :sequential (cycles :pool in order — use for PRISM_ARENA)
             :start_immediately => true,
             :message => "The Bleed shudders... echoes of {1} seep in!" }   # {1} = borrowed names
```
Borrowed fields contribute their **effect** keys only: type/move/damage/effectiveness/inverse/type changes/extra types/
accuracy/priority/crit/added effects/effect chances/fixed damage/weather_as/stat boosts/move fails/end_of_round/on_entry/speed/negated
abilities/weather/terrain and hooks except `on_start`/`on_end`. **Not** borrowed: identity, transitions, seed, stages,
borrow. Fields that themselves have `:borrow` are never borrowed. Pool `:all` automatically includes fields added
later. Borrowed `on_entry` rules with `:also_on_change` hit active battlers when borrowed.

---------------------------------------------------------------------------------------------------
## 9. Hooks `:hooks` (escape hatches)
All procs are wrapped: an exception is logged (and re-raised only in Debug mode).

| Hook | Signature | Return / use |
|---|---|---|
| `:on_start` | `\|battle, old_field_id\|` | field became active (battle start: old = `:NONE`) |
| `:on_end` | `\|battle, new_field_id\|` | field is about to be replaced |
| `:on_entry` | `\|battle, battler\|` | after the declarative `:on_entry` rules |
| `:end_of_round` | `\|battle\|` | after declarative EOR rules, before timed transitions |
| `:base_type` | `\|battle, user, move, type\|` | return a type Symbol to change the move's type (nil = keep) |
| `:damage` | `\|battle, user, target, move, type, mults, ai\|` | edit `mults[:power_multiplier/:attack_multiplier/:defense_multiplier/:final_damage_multiplier]`. **Called by the AI too (`ai == true`): no messages/side effects when ai** |
| `:effectiveness` | `\|battle, move, move_type, def_type, user, target, eff\|` | return new Float for one matchup (move may be nil) |
| `:accuracy` | `\|battle, user, target, move, type, mods\|` | edit `mods[:base_accuracy/:accuracy_multiplier/:evasion_multiplier/...]` |
| `:after_move` | `\|battle, user, targets, move, num_hits\|` | after a move's hits, before transitions |
| `:block_move` | `\|battle, user, move\|` | return String (fail message) or true to make the move fail |
| `:speed` | `\|battle, battler, mult\|` | return new multiplier (**don't call `battler.pbSpeed` inside**) |
| `:ai_score` | `\|score, aimove, aiuser, ai, battle\|` | return adjusted AI move score |

Use `FieldEffects.state(battle)` to keep per-field counters between hook calls; `battle.pbRandom(n)` for randomness
(keeps recorded battles in sync).

---------------------------------------------------------------------------------------------------
## 10. AI awareness (automatic)
The v21.1 AI sees: field type changes & priority (through `pbCalcType`/`pbPriority`), damage multipliers
(`rough_damage` × field multiplier), effectiveness changes/extra types/inverse, accuracy & crit changes, moves the
field makes fail and weather/terrain the field blocks, field end-of-round damage/healing, and a small score bonus for
moves with `:move_stat_boosts`. Use `:ai_score` for anything else.

---------------------------------------------------------------------------------------------------
## 11. Checklist for a new field file
1. `1NN_Field_<Name>.rb`, only `FieldEffects.register(:ID, {...})` (ID from the SPINE roster).
2. `:name`, `:backdrop` (`"field_<snake_name>"`), `:intro_message`, `:description`.
3. 10–25 interactions; thematic transitions listed in SPINE; a `:seed` entry; `:nature_power`, `:camouflage`.
4. Messages: short, evocative, one sentence. Only on notable boosts (not every 1.2× tweak).
5. `ruby -c` the file, then `ruby tools/validate_fields.rb` → 0 errors.
6. Add a section to `design/FIELDS.md` (player-facing: boosts, nerfs, transitions, seed).
