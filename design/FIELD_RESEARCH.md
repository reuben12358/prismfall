# Field effects in Reborn, Rejuvenation and Desolation — research notes

Written for SPINE Revision 10 (deeper fields). Sources: the three games' scripts (plain Ruby, read only, never run),
`Data/fields.dat` and `Data/fieldnotes.dat` (decoded with `mapgen/rmarshal.py` under `python3 -I`; nothing was
`Marshal.load`ed), and the `Graphics/Battlebacks` folder names. Everything below is a summary in our own words;
quotes are a few words at most. "Rebornverse" = the shared engine all three games use.

Numbers at a glance (from the decoded data):

| Game | Fields (incl. stage variants) | Avg. per-move entries per field | Fields that can transform | Field Notes lines |
|---|---|---|---|---|
| Reborn | 41 | 19 | 31 | 817 |
| Rejuvenation | 56 | 28 | 43 | 1449 |
| Desolation | 43 | 21 | 31 | 807 |

Per-move entries are only the data half: each game also has hundreds of hard-coded `@battle.FE == :X` checks in
the battle, battler, move, ability and AI code (Colosseum, Electric Terrain, Fairy Tale and Glitch each appear
40–90 times). A typical "great" field ends up with 20–40 player-visible rules (its Field Notes line count).

---------------------------------------------------------------------------------------------------
## 1. How they structure a field

### 1.1 Data format
One big Ruby hash, `FIELDEFFECTS = { :ID => { ... } }` (`Scripts/Reborn/fieldtext.rb`,
`Scripts/Rejuv/Definitions/fieldtext.rb`, Desolation's `fieldtxt.rb`), compiled into `fields.dat` as `FEData`
objects. Per field:

* **Identity**: `:name`, `:fieldMessage` (intro line), `:graphic` (a list of battleback names — the game picks the
  field from the map's battleback, so *the backdrop is the field key*), `:naturePower`, `:secretPower`, `:mimicry`
  (the field's "natural type", also used by Camouflage, Terrain Pulse and Rejuvenation's Shelter).
* **Per-move table** (`fieldmovedata`): for each move a power multiplier (`0` = the move fails), an accuracy
  override (`0` = never misses), an index into the field's message list, an added type, a field-change target,
  a counter increase towards a multi-step change, and code strings run after the move.
* **Per-type table** (`fieldtypedata`): type multipliers with an optional condition string (e.g. "attacker is
  grounded"), an added type for every move of a type (Volcanic: Rock moves also hit as Fire), type effects run
  after the move.
* **Change rules**: `:fieldChange { NEWFIELD => [moves] }`, change conditions (code strings), change messages,
  `:dontChangeBackup` (the change is temporary / layered), `:changeEffects` (side effects of the change itself,
  e.g. the Corrosive Mist explosion).
* **Seed**: exactly one seed type per field, plus a battler effect, its duration, stat changes, message, animation.
* **UI lists**: `statusMods` / `statusBuffs` / `statusNerfs` — status moves the field changes, so the move menu can
  highlight them; `fieldAppSwitch` — the story switch that unlocks the field's notes in the Field App.
* Rejuvenation adds `overlaymovedata`/`overlaytypedata`: what a terrain does when it sits *on top of* a field.

### 1.2 Engine hooks
* `PokeBattle_Field` holds the current field plus a **layer stack** (`layer`, `backup`). A change can push a field
  on top (temporary, remembers what was underneath) or replace the top. Rejuvenation's terrains and pledge fields
  are **timed overlays** (`duration`, `overlay`) that pop back to the field below.
* Four general-purpose **counters** per field drive multi-step changes ("two quakes collapse the cave").
* `fieldEffectAfterMove` runs after every move: type effects, move effects, counter increases, then the change.
* **The transforming move hits harder**: a move that changes or destroys the field gets ×1.3 (the Field Notes'
  general page says so for every field). It makes field changes something you aim for, not a side effect.
* `setField` re-runs on-field ability triggers, the **seed check** for every active battler, and the weather
  check (`noWeather`): fields veto or end weather (Underwater, New World, Volcanic melts hail).
* Pledge combos create 4-turn fields anywhere (Fire+Grass = Burning, Water+Grass = Swamp, Fire+Water = Rainbow).
* Difficulty scales everything: easy mode halves every field multiplier's distance from ×1; the "Field Frenzy"
  password doubles it.

---------------------------------------------------------------------------------------------------
## 2. What makes their best fields great

The fields people remember (Forest, Volcanic Top, Cave, Crystal Cavern, Flower Garden, Fairy Tale, Water Surface,
Wasteland, Concert, Darkness) share six traits:

1. **The place has verbs.** Each rule reads as something the place *does with* a move: Surf over magma makes
   steam that blinds everyone; a quake in a cave cracks the ceiling and the second one brings it down; Rock moves
   in a crystal cave take on whatever colour the crystals glow this turn; Electroweb and Attack Order run through
   the forest. Players learn the field by thinking about the place, not by memorising a table.
2. **Fewer flat type boosts, more specific moves.** A great field has 1–3 type boosts and 20–60 *named* moves:
   the wind moves, the mud moves, the bone moves, the light beams. Odd picks are the fun ones (Pay Day in the
   dragon hoard, Rock Smash "SMASH'D!" on the Rocky field, Sing perfect on the Big Top).
3. **Abilities and items wake up.** Almost every field "activates" abilities whose normal trigger is weather,
   terrain or low HP (Blaze, Swarm, Sand Rush, Surge Surfer, Grass Pelt, Marvel Scale…) and gives on-entry boosts to
   thematically fitting ones (Magma Armor hardens, Battle Armor gleams on the Fairy Tale field). Items get small
   twists (Amulet Coin in the hoard, Float Stone in Deep Earth). This is where team-building depth comes from.
4. **Every field is a node in a web.** Most fields can become 2–5 others, and the result is usually *as
   interesting* (Grassy → Burning → (water) the fire goes out; Cave → Crystal Cavern / Dragon's Den / Volcanic /
   Icy / Corrupted; Icy → Water Surface *or* Cave depending on what lies under the ice). Changes come from a
   deliberate move (often needing 2–3 uses, with a progress message) or weather, rarely by accident.
5. **Multi-stage fields create a tug of war.** Flower Garden (5 stages: tending grows it, blades and fire cut it),
   Concert (4 hype stages: crits and showy moves raise hype, misses and stalling lower it; damage rolls go max at
   full hype), Darkness (3 stages: dark moves deepen it, light pushes it back), Crystal Cavern's colour cycle,
   Short-Circuit's repeating damage-roll pattern. Both sides fight over the stage.
6. **Signature events.** Volcanic Top's eruption (primed by quake/eruption moves, erupts at end of turn: fire
   damage to the unprotected, wakes sleepers, clears hazards, rewards Flare Boost/Magma Armor), the cave collapse,
   the Corrosive Mist explosion, the Mirror Arena shatter, Wasteland "eating" hazards and spitting them back with
   new effects. One memorable set piece per field.

Where they are weaker (things to avoid): some fields are walls of near-identical ×1.5 lists; a few mechanics are
pure punishment (Corrosive Mist poisons everyone every turn; Murkwater KOs on change); passive end-of-turn chip
damage to "everyone not type X" is common and reads as the place hurting the creatures. Their message voice is
punchy but often generic ("The field strengthened the attack!").

---------------------------------------------------------------------------------------------------
## 3. Topic by topic

### 3.1 Per-move interactions and type changes
* Move power by name (×1.2–×2), by type (often conditional: grounded attacker/target, special only, physical only),
  and `0` = fails ("But there is no solid ground!").
* **Added types** are the strongest tool: Volcanic gives Rock moves Fire; Electric Terrain makes Surf, Muddy Water,
  Hurricane and Explosion also Electric; Forest makes cutting moves Grass; Corrosive makes Grass moves Poison;
  Crystal Cavern cycles Rock moves through Fire/Water/Grass/Psychic.
* **Full type changes** for a few moves (Fairy Tale: Cut, Sacred Sword become Steel; Dragon's Den: Strength
  becomes Rock/Fire).
* Accuracy overrides (Will-O-Wisp never misses in fire, Sing perfect on stage, Thunder perfect on mountains).
* Status-move upgrades (+1 extra stage, extra stats: Rototiller raises both attacks, Sweet Scent lowers defences in
  a blooming garden) and recovery changes (Shore Up full on the beach, Synthesis weak in the dark).
* Durations: Tailwind 6–8 turns on mountains/sky, rooms 8 turns in psychic/starlight fields, weather 8 turns where
  it belongs, Magnet Rise 8 turns on electric fields.
* Two-turn moves lose their charge turn where the place helps (Dig in the desert, Electro Shot on Electric
  Terrain, Solar Beam in the rainbow).

### 3.2 Abilities and items
* "Activates": the ability works as if its condition were met (Blaze/Overgrow/Torrent/Swarm, Sand Rush/Sand Force/
  Sand Veil in the desert and beach, Surge Surfer, Grass Pelt, Leaf Guard, Marvel Scale, Toxic Boost on corrosion).
* On-entry boosts: Magma Armor, Light/Heavy Metal in the factory, Big Pecks in the sky, Frisk steals in the alley,
  Rattled gains Speed in scary places, Illuminate lights up the dark.
* Each-turn triggers: Motor Drive/Volt Absorb charge from the field, Steam Engine/Coal Furnace in volcanic fields,
  Ice Body, Dry Skin (heal or hurt), Natural Cure every turn in the Bewitched Woods.
* Abilities that grant immunities (Magma Armor = Fire immunity in Volcanic Top / Dragon's Den / Infernal; Ice
  Scales and Multiscale remove weaknesses).
* Negations (Frozen Dimension shuts off fire abilities).
* Items: Amulet Coin (status immunity in the hoard), Float Stone, Iron Ball and Magnet in Deep Earth, Nevermelt Ice,
  Soul Dew, Black Sludge; Heavy-Duty Boots and Air Balloon protect from ground effects everywhere.

### 3.3 Terrain, weather and field layering
* Reborn: terrains *are* fields and replace the current one; they remember the field below and return to it.
* Rejuvenation: terrains are 5-turn **overlays** on any field; boosts stack except two type boosts of the same
  type, where the larger applies (bumped to ×1.5). Overlay rules have their own notes.
* Fields veto, end or extend weather: no weather underwater or in space; volcanic fields melt hail; deserts keep
  sun and sand for 8 turns; Starlight's boosts switch off while any weather is up; the Dimensional field randomises
  weather duration.
* Weather triggers changes (rain cools volcanic fields, hail snows over a mountain, sun relights the dark crystals).

### 3.4 Field-changing moves and multi-stage fields
* Single trigger (Dive → Underwater), counted (Muddy Water ×2 → Swamp), conditional on what is underneath (Icy
  melts into Water Surface or Cave), with a `changeEffect` set piece (explosion, shatter, cave collapse).
* Progress messages make counters readable ("The crystals are starting to crack…").
* Stage ladders (Flower Garden, Concert, Darkness) use stage-specific multipliers and stage-scaled ability
  effects (Swarm ×1.8/×2 at stages 3/5; Ingrain ×2/×4).
* The transforming move gets ×1.3; the AI values the change (below).

### 3.5 Seeds
* Four seeds that double as **field families**: Elemental, Telluric, Synthetic, Magical. Each field reacts to
  exactly one; the Field Notes menu even sorts fields by family.
* A seed is a **trade-off**: a stat boost plus a field-flavoured effect, often with a cost — Volcanic: +Atk/SpA/Spe
  but trapped in Fire Spin; Icy: +2 Speed but hurt by ice spikes; Corrosive Mist: +Atk/SpA but badly poisoned;
  Cave: +2 Def but takes Stealth Rock damage; Swamp: +Def and the ability becomes Clear Body; Darkness: the seed
  *deepens the field a stage*; Flower Garden: grows the garden.

### 3.6 Field Notes
* A per-field list of short lines with icons ("[Fire] attacks ↑ ×1.5 when…") plus an elaboration line (move
  lists, conditions). Rejuvenation has 20–48 lines per field, a general page (×1.3 transform rule, natural type,
  overlays), sorting by number/name/family, and overlay notes. Notes are viewable in battle.
* Fields unlock as you meet them (seen fields; Reborn's Field App switch per field).

### 3.7 AI awareness
* Damage, type changes, accuracy and failing moves go through the same calculations the AI uses.
* `getFieldDisruptScore`: for any field, a favourability number for the AI (×1.3–×1.8 per relevant type on each
  side, its party's types, roles, key abilities and moves). A move that would change the field has its score
  multiplied by √(current score / new score) — the AI changes fields it dislikes and protects fields it likes.
* Dozens of field-specific special cases (prefer Defog to clear a field, avoid Fire on a Corrosive Mist unless the
  explosion wins the game, value seeds).

### 3.8 Message tone
Short, punchy, the place as the actor: "The attack rode the current!", "Jet-streamed!", "ECHO-Echo-echo!",
"The lava's heat boosted the flame!", playful asides ("Yodelayheehoo~", "SMASH'D!", "Spooky scary skeletons!"),
crowd voices on the Crowd and Concert fields. Some lines cast Pokémon as victims ("knocked into the lava",
"suffocating smog"); that is the part we drop.

---------------------------------------------------------------------------------------------------
## 4. Their whole roster

Legend for the last column: **→ X** = we take this idea into our field X; **kingdom** = fits a kingdom's identity;
— = not used.

### 4.1 Core roster (Reborn; also in Desolation, most also in Rejuvenation)
| Field | One line | Fit for Prismfall |
|---|---|---|
| Electric Terrain | Grounded Electric ×1.5, no sleep; conductive water and wind moves gain Electric; Mud Sport shorts it | → NEON_GRID (conduction, no sleep for the grounded, Surge Surfer) |
| Grassy Terrain | Grounded Grass ×1.5, fire spreads into a Burning field, quakes softened, 1/16 heal | → MEADOW, FLOWER_GARDEN |
| Misty Terrain | Fairy ×1.5, Dragon ×0.5, status immunity, explosions fail; winds disperse it; smog corrupts it | → FAIRY_TALE / RAINBOW details |
| Dark Crystal Cavern | Dark/Ghost and light beams ×1.5, Dark/Ghost defences ×1.5; sun relights; quakes → Cave | → DARK_CRYSTAL (kept, deepened) |
| Chess Board | Pokémon become chess pieces by stats/slot with role buffs; "chess attacks" deal Rock damage | idea → GRAND_STAGE (stage roles) — not copied |
| Big Top Arena | Physical "striker" moves roll ×0.5–×3; sound, dance, acrobatics boosted; Sing perfect | → GRAND_STAGE (applause ladder, showpiece moves) |
| Burning Field | Grounded Fire ×1.5, Grass/Ice weak, put out by water, wind or sand | → **WILDFIRE** (new) |
| Swamp | Grounded Speed drops each turn, mud ×1.5, quakes ×0.25, explosions fail | → CORROSIVE_MIRE (mud, damp), Nadir |
| Rainbow | Secondary effects ×2, special Normal gains a random type, sleepers heal; sand/hail end it | → RAINBOW (kept, deepened) |
| Corrosive Field | Grounded poison hazard, Grass hits as Poison, acid ×2; Seed Flare / Purify cleanse | → CORROSIVE_MIRE, WASTELAND |
| Corrosive Mist | Poisons everyone each turn; fire triggers a field-wide explosion; wind disperses it | explosion idea → CORROSIVE_MIRE (fume ignition, harnessed) |
| Desert | Ground SpDef ×1.5, sand abilities active, sun hurts Water/Grass, Dig in one turn | → DESERT (Ossaria) |
| Icy Field | Contact priority and rolling moves build Speed, Rock gains Ice, melts into what lies below, quakes make ice spikes | → FROZEN_LAKE (Isenmar) |
| Rocky Field | Rocks give cover (Bulletproof), missed contact moves crash for recoil, Stealth Rock ×2 | → CAVE, MOUNTAIN details |
| Forest | Grass ×1.5, special Bug ×1.5, cutting moves gain Grass, Sticky Web doubled | → SILKWOOD, MEADOW (Elowen) |
| Super-Heated | Mild Fire up, water turns to blinding steam, big fire ignites it | → **STEAM_CALDERA** (new) |
| Factory | Electric ×1.2, gear/steel moves ×2, Download/Motor Drive amplified; overloads short it | → FACTORY (Zenith) |
| Short-Circuit | Electric damage rolls cycle ×0.5–×2; shadows ×1.3 in the gloom; recharging restores the Factory | → NEON_GRID stage 2 "Blackout" |
| Wasteland | Hazards are eaten and return with special effects; sludge inflicts random status | → WASTELAND (Nadir/Bleed) |
| Ashen Beach | Focus: Inner Focus etc. ignore accuracy/evasion; Calm Mind/Kinesis/Sand Attack boosted; ash-stirring winds lower everyone's accuracy | → BEACH (focus), **ASHEN_WASTE** (stirred ash) |
| Water Surface | Non-Water Speed ×0.75, Ground moves fail, hazards sink, Electric ×1.5 vs grounded; Dive → Underwater | → WATER_SURFACE (Isenmar) |
| Underwater | Non-Water Speed ×0.5, Fire fails, no weather, Electric ×2 and never misses | → UNDERWATER |
| Cave | Ground hits airborne, second quake collapses the ceiling, Stealth Rock ×2; becomes many fields | → CAVE (collapse kept, more exits) |
| Glitch | Gen 3 physical/special split by type, altered chart | idea → BLEED flavour only |
| Crystal Cavern | Rock/Dragon ×1.5, Rock moves gain a cycling type, light beams ×1.3; darkness → Dark Crystal | → CRYSTAL_CAVERN (Ossaria) |
| Murkwater Surface | Toxic water: poison damage, Water moves gain Poison; Purify/Whirlpool cleanse | → CORROSIVE_MIRE / WATER_SURFACE pollution link |
| Mountain | Winds and throws ×1.5, Tailwind long + strong winds, Thunder never misses; hail → Snowy, eruption → Volcanic Top | → MOUNTAIN |
| Snowy Mountain | Mountain plus Ice; Rock gains Ice; Fire ×0.5 | → SNOWY_MOUNTAIN (Isenmar) |
| Holy Field | Normal hits Ghost/Dark super effectively; legendary signature moves boosted; curses lifted | → HOLLOW_CATHEDRAL stage 2 (Consecrated) |
| Mirror Arena | Accuracy/evasion games; reflected beams ×2 vs evasive targets; shattering hurts everyone | → INVERSE / MINDSCAPE mirror details |
| Fairy Tale | Fairy/Steel/slicing ×1.5, Dragon ×2, Steel ×2 vs dragons, Fire gains Dragon, armour raises defences | → FAIRY_TALE (Elowen's Gloaming) |
| Dragon's Den | Dragon/Fire ×1.5, Water/Ice ×0.5, Dragon defences ×1.3, Stealth Rock becomes Fire, Magma Armor immune to Fire | → DRAGONS_DEN (Ashkaar) |
| Flower Garden 1–5 | Grows by tending, cut by blades/fire; Grass/Bug/Swarm/Overgrow scale per stage | → FLOWER_GARDEN (kept, deepened) |
| Starlight Arena | Psychic/Dark ×1.5, cosmic moves ×2; any weather switches the boosts off | → NEW_MOON (stars), PRISM_ARENA |
| New World | No weather or field creation, space moves ×2, Doom Desire ×4 | → PRISM_ARENA finale flavour |
| Inverse Field | Inverse type chart | → INVERSE (Antumbra) |
| Psychic Terrain | Priority fails vs grounded, Psychic ×1.5, mind moves +1 stage, rooms 8 turns | → MINDSCAPE |

### 4.2 Rejuvenation additions
| Field | One line | Fit |
|---|---|---|
| Volcanic Field | Rejuvenation's Burning field: molten floor, Fire ×1.5; rain, sand or wind cool it into a Cave | → VOLCANIC |
| Volcanic Top | Eruption mechanic, winds gain Fire, steam lowers accuracy; Blizzard → Mountain, Fly → Sky | → VOLCANIC (eruptions), STEAM_CALDERA (steam), Ashkaar |
| Deep Earth | Permanent Gravity, weight doubled, slow moves strong, fast moves weak | idea → CAVE deep levels — not now |
| Dimensional | Dark dimension: random durations, Dark/Ghost/Shadow ×1.5, anger abilities buffed | → BLEED / INVERSE flavour |
| Frozen Dimensional | Rooms and terrain frozen in place, hate made cold | — |
| Haunted | Ghost hits Normal, sleepers drained, will-o'-wisps join fire moves | → HOLLOW_CATHEDRAL (ghostfire) |
| Corrupted Cave | Grounded Pokémon poisoned each turn; fire combusts it into a Volcanic field | → CAVE ↔ CORROSIVE links |
| Bewitched Woods | Fairy hits Steel, fairy/dark magic, Natural Cure every turn | → FAIRY_TALE, Elowen deep woods |
| Sky Field | Flying ×1.5, hazards (except rocks) fall away, quakes fail; Gravity grounds it into a Mountain | → STORMFRONT (Zenith) |
| Colosseum | KOs grant the highest stat of the fallen, no forced switches, switch in speed order | → COLOSSEUM (Nadir) |
| Infernal | Hellfire: Fire ×2 vs Ghost, Dark/Fire ×1.5, Torment and Heal Block deal damage | — (tone) |
| Concert Venue 1–4 | Hype ladder; damage rolls min/max at the extremes; sleepers woken by noise | → GRAND_STAGE applause stages |
| Back Alley | Healing −33%, item thieves doubled, Frisk steals | → NEW_MOON stage 3 / Nadir streets |
| City | Physical Normal ×1.5, Bug/Poison/Steel ×1.3, street-smart abilities | idea for Zenith streets (NEON_GRID default) |
| Deux Finalis | Story finale fusing dimensions | → PRISM_ARENA / BLEED |

### 4.3 Desolation additions
| Field | One line | Fit |
|---|---|---|
| Cloud Field | Ground moves and hazards fall through the clouds, Flying ×1.3, Rock ×0.75 | → STORMFRONT (deck above the clouds) |
| Crowd Field | The crowd cheers brawling physical moves and boos special Psychic "tricks" | → COLOSSEUM (crowd verdicts) |
| Darkness 1–3 | Shadow moves ×1.1/1.2/1.4, light weaker; dark moves deepen it, light pushes it back; seed deepens it | → NEW_MOON (three-stage darkness ladder) |
| Dance Floor | Dances ×1.4, music ×1.2, Psychic ×1.3; seed grants Dancer | → GRAND_STAGE (dance numbers) |

Battleback names confirm the roster and add map-specific variants of the same field (Rejuvenation: Volcano/
Volcano2, Voltop/Voltop_1, Haunted 1–3, Ruin 1–4, the Gearen districts for City) — one field, several looks.

---------------------------------------------------------------------------------------------------
## 5. What we take, mapped to our engine

| Idea | Prismfall implementation (FIELD_API §) |
|---|---|
| Ability activation | new `:activate_abilities` key: listed abilities behave as if their trigger were met (§4.7) |
| Transforming move ×1.3 | engine-wide: a damaging move that completes a field change gets ×1.3 (opt out per rule with `:boost => false`) (§5) |
| Immunities from the place | new `:status_immunity` rules (Electric-Terrain-style "can't fall asleep") (§4.9) |
| Ability-granted type immunities | `:effectiveness_mods` now take `:user`/`:target` battler matchers (§4.3) |
| Durations (Tailwind, rooms, screens) | new `:effect_durations` key (§4.10) |
| Natural type | Mimicry and Terrain Pulse use the field's `:camouflage` type when no terrain is up (§4.1) |
| Field families / one seed per field | new `:family` key; every field reacts to its family's seed with a trade-off (§6) |
| Seeds that do things | new named effects (tailwind, wish, taunt, screens, hazards on the foe) and `:add_type` (§4.6) |
| Stage ladders | NEW_MOON (Darkness ladder), GRAND_STAGE (applause), NEON_GRID (Blackout), MINDSCAPE (Nightmare), DESERT (Superbloom), COLOSSEUM (Frenzy) |
| Signature events | VOLCANIC eruptions, STEAM_CALDERA geysers, CAVE collapse, CORROSIVE_MIRE fume flare, STORMFRONT lightning, WILDFIRE spreading flames |
| Field web | every transition now leads to a real field; no transition ends at "no field" (FIELDS.md transition map) |
| AI field disruption score | AI scores moves that would complete a transition by how much better/worse the new field is for its side (§10) |
| Map battleback = field | `design/FIELD_DEFAULTS.yaml` (every built map) + engine fallbacks by encounter type and battle environment (§1) |
| Field Notes | every field ships hand-written `:notes`; the menu shows the family (§4.1) |

Not taken: Chess pieces, Glitch's split, Deep Earth weight rules, Frozen Dimension (none fits a kingdom yet);
difficulty scaling of multipliers (worth doing later through Prismfall Core's difficulty modes); timed
pledge overlays (the Essentials pledge side effects already exist).

### Tone rule we adopted
The place is an ally or an instrument, never a torturer. Messages describe Pokémon *using* the place ("{1} rode the
silk currents!", "{1} drew fire up from the magma!", "The ghosts thickened in the dark around {1}!"). Hazards are
events Pokémon cause (eruptions, cave-ins, lightning drawn by a high flier), not chip damage for existing.
