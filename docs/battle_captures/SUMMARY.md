# Prismfall battle captures - headless logic test

> **These are logic-test outputs, not game screenshots.** The real Pokemon Essentials v21.1 battle code
> (Battle, Battler, Move, AI, abilities, items) ran in plain Ruby with the Prismfall Core, Field Effects and
> Bosses plugins loaded by the real PluginManager, behind a text-logging battle scene. No graphics, audio,
> EBDX or RPG Maker runtime was involved, so nothing here proves how the game *looks*.

Regenerate with `ruby tools/harness/run_all.rb` then `python3 -I tools/harness/render_cards.py`.

**Real-engine footage** (mkxp-z + Elite Battle: DX + these plugins, AI vs AI): see `engine/README.md`.

## What loaded
- Engine: 313 script sections of the base project (Essentials v21.1), in order.
- Plugins, in PluginManager order: v21.1 Hotfixes, Generation 9 Pack, Prismfall Core, Prismfall Field Effects, Prismfall Bosses.
- PBS compiled by the real Compiler: 1420 species, 832 moves, 496 trainers (incl. the kit's trainers/trainer types/seed items); 33 fields registered.
- Not loaded: Elite Battle DX, Prismfall EBDX Bridge, Cutscenes, Debug Tools, maps, encounters.

## Result
- Full AI-vs-AI battles: **33/33 completed without an error** (one per field).
- Scripted probes: boosted move 33/33 fields; transitions 123/124 rules fired; seeds 34/34; end-of-round rules 33/35.
- Boss / arena runs: 5 (see below). Exceptions in the final run: **0**.

## Per field
"Field messages" = distinct messages written in the field's definition that appeared in the full battle.

| # | Field | Full battle vs | Completed? | Result | Turns | Field messages | Boosted move (damage on field / no field) | Transitions fired | Seed | End-of-round |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Silkwood `SILKWOOD` | Gym 1 Warden Tamsin (Lv.15) | yes | player won | 5 | 8 | Bug Buzz 99 / 66 | 2/2 | 1/1 | 1/1 |
| 2 | Grand Stage `GRAND_STAGE` | Gym 2 Warden Dorian (Lv.19) | yes | player lost | 13 | 6 | Swift 58 / 45 | 7/7 | 1/1 | none defined |
| 3 | Water Surface `WATER_SURFACE` | Gym 3 Warden Marisol (Lv.23) | yes | player lost | 21 | 4 | Water Pulse 66 / 45 | 4/4 | 1/1 | 2/2 |
| 4 | Neon Grid `NEON_GRID` | Gym 4 Warden Rook (Lv.27) | yes | player won | 15 | 6 | Thunderbolt 99 / 66 | 5/5 | 1/1 | 2/2 |
| 5 | Desert `DESERT` | Gym 5 Warden Sahar (Lv.31) | yes | player lost | 14 | 7 | Earth Power 79 / 66 | 5/5 | 1/1 | 2/2 |
| 6 | Corrosive Mire `CORROSIVE_MIRE` | Gym 6 Warden Corvin (Lv.35) | yes | player lost | 18 | 8 | Sludge Bomb 99 / 66 | 3/3 | 1/1 | 2/2 |
| 7 | Volcanic Field `VOLCANIC` | Gym 7 Warden Brann (Lv.39) | yes | player won | 6 | 7 | Flamethrower 99 / 66 | 3/3 | 1/1 | 2/3 |
| 8 | Colosseum `COLOSSEUM` | Gym 8 Warden Kaito (Lv.43) | yes | player won | 8 | 7 | Aura Sphere 63 / 53 | 2/3 | 1/1 | none defined |
| 9 | Flower Garden `FLOWER_GARDEN` | Gym 9 Warden Juno (Lv.47) | yes | player lost | 18 | 6 | Energy Ball 73 / 66 | 21/21 | 1/1 | none defined |
| 10 | Frozen Lake `FROZEN_LAKE` | Gym 10 Warden Anja (Lv.51) | yes | player lost | 14 | 7 | Ice Beam 99 / 66 | 3/3 | 1/1 | none defined |
| 11 | Stormfront `STORMFRONT` | Gym 11 Warden Odessa (Lv.55) | yes | player lost | 12 | 5 | Air Slash 66 / 56 | 1/1 | 1/1 | 4/5 |
| 12 | Mindscape `MINDSCAPE` | Gym 12 Warden Ilsa (Lv.59) | yes | player lost | 12 | 3 | Psychic 148 / 99 | 5/5 | 1/1 | 1/1 |
| 13 | Crystal Cavern `CRYSTAL_CAVERN` | Gym 13 Warden Bastian (Lv.63) | yes | player lost | 17 | 6 | Power Gem 113 / 59 | 4/4 | 1/1 | 1/1 |
| 14 | Hollow Cathedral `HOLLOW_CATHEDRAL` | Gym 14 Warden Ysolde (Lv.67) | yes | player lost | 23 | 7 | Shadow Ball 79 / 53 | 4/4 | 1/1 | none defined |
| 15 | Factory `FACTORY` | Gym 15 Warden Magnus (Lv.71) | yes | player lost | 15 | 7 | Flash Cannon 113 / 59 | 2/2 | 1/1 | 1/1 |
| 16 | New Moon `NEW_MOON` | Gym 16 Warden Nyx (Lv.75) | yes | player lost | 19 | 11 | Dark Pulse 105 / 59 | 5/5 | 1/1 | none defined |
| 17 | Fairy Tale `FAIRY_TALE` | Gym 17 Warden Celestine (Lv.80) | yes | player lost | 13 | 6 | Moonblast 104 / 70 | 1/1 | 1/1 | 1/1 |
| 18 | Dragon's Den `DRAGONS_DEN` | Gym 18 Warden Sigrun (Lv.85) | yes | player lost | 14 | 7 | Dragon Pulse 94 / 62 | 3/3 | 1/1 | none defined |
| 19 | Underwater `UNDERWATER` | Fisherman Andrew (Lv.18) | yes | player won | 4 | 2 | Water Pulse 99 / 45 | 2/2 | 1/1 | 1/1 |
| 20 | Cinderglass `ASHEN_WASTE` | Hiker Ford (Lv.19) | yes | player won | 3 | 3 | Power Gem 99 / 59 | 3/3 | 1/1 | 2/2 |
| 21 | Inverse Field `INVERSE` | Echo of the Ghost Warden Morwen (Lv.90) | yes | player lost | 22 | 4 | Shadow Ball 63 / 53 | 1/1 | 1/1 | none defined |
| 22 | The Bleed `BLEED` | Hollow Keeper Thistle (Lv.15) | yes | player won | 9 | 4 | Judgment 113 / 73 | none defined | 2/2 | 1/1 |
| 23 | Dark Crystal Cavern `DARK_CRYSTAL` | Hollow Keeper Teo (Lv.21) | yes | player won | 5 | 5 | Dark Pulse 87 / 59 | 4/4 | 1/1 | none defined |
| 24 | Scrapyard `SCRAPYARD` | Meridian Director Sabine (Lv.97) | yes | player won | 10 | 3 | Flash Cannon 71 / 59 | 2/2 | 1/1 | none defined |
| 25 | Cave `CAVE` | Camper Liam (Lv.11) | yes | player won | 4 | 4 | Power Gem 87 / 59 | 6/6 | 1/1 | none defined |
| 26 | Mountain `MOUNTAIN` | Black Belt Taro (Lv.16) | yes | player won | 5 | 3 | Power Gem 87 / 59 | 3/3 | 1/1 | none defined |
| 27 | Snowy Mountain `SNOWY_MOUNTAIN` | Champion Shelly (Lv.17) | yes | player lost | 16 | 4 | Ice Beam 99 / 66 | 3/3 | 1/1 | 1/1 |
| 28 | Beach `BEACH` | Picnicker Susie (Lv.18) | yes | player won | 2 | 2 | Water Pulse 53 / 45 | 2/2 | 1/1 | 2/2 |
| 29 | Rainbow `RAINBOW` | Gym Leader Amaria (Lv.78) | yes | player lost | 15 | 3 | Swift 66 / 45 | 2/2 | 1/1 | 2/2 |
| 30 | Wasteland `WASTELAND` | Meridian CEO Aurelian (Lv.100) | yes | player lost | 15 | 3 | Sludge Bomb 95 / 66 | 2/2 | 1/1 | 1/1 |
| 31 | Prism Arena `PRISM_ARENA` | Sovereign Valen (Lv.96) | yes | player lost | 18 | 2 | Tri Attack 76 / 59 | none defined | 1/1 | 2/2 |
| 32 | Wildfire `WILDFIRE` | Hiker Ford (Lv.19) | yes | player won | 0 | 3 | Flamethrower 99 / 66 | 9/9 | 1/1 | 1/1 |
| 33 | Meadow `MEADOW` | Hiker Ford (Lv.19) | yes | player won | 2 | 2 | Energy Ball 79 / 66 | 4/4 | 1/1 | 1/1 |

Logs: `logs/NN_<field>.txt` (full battle) and `probes/<field>.txt` (every scripted probe for that field).

## Bosses and PRISM_ARENA
| Run | Result | Turns | Bars broken | Field changes | Log |
|---|---|---|---|---|---|
| BOSS Zekrom (ZEKROM_ENGINE, 3 bars, FACTORY -> SCRAPYARD) vs over-levelled Lv.100 party | player won | 5 | 2 | FACTORY->SCRAPYARD | `logs/boss_zekrom.txt` |
| BOSS Kyogre (KYOGRE_ISENMAR, 3 bars, FROZEN_LAKE -> WATER_SURFACE) vs over-levelled Lv.100 party | player won | 7 | 2 | FROZEN_LAKE->WATER_SURFACE, WATER_SURFACE->FROZEN_LAKE | `logs/boss_kyogre.txt` |
| BOSS Arceus (ARCEUS_FINALE on PRISM_ARENA) vs Lv.100 party | player lost | 8 | 0 | - | `logs/boss_arceus.txt` |
| BOSS Hard-mode Warden Ilsa via Prismfall.gym_battle(12) (ace = 2-bar boss) vs over-levelled Lv.100 party | player won | 12 | 1 | - | `logs/boss_hard_warden_ilsa.txt` |
| PRISM_ARENA rotation: Lv.25 Arceus (Multitype) for 20 rounds, Judgment every 3rd round | fled/forfeit | 20 | 0 | Plate turns: T3 VOLCANIC, T6 WATER_SURFACE, T9 FLOWER_GARDEN, T12 NEON_GRID, T15 FROZEN_LAKE, T18 COLOSSEUM | `logs/prism_arena_rotation.txt` |

## Probe detail
### Silkwood (`SILKWOOD`)
- Boost: Bug Buzz: 99 dmg on field vs 66 without (BUG-type moves x1.5)
- Transition FIRED - stage 1: types FIRE, category damaging, condition proc x3 -> WILDFIRE: fired with Flamethrower, Flamethrower, Flamethrower
- Transition FIRED - stage 1: types FIRE, category damaging x2 -> WILDFIRE: fired with Sunny Day, Flamethrower, Flamethrower
- Seed OK - TELLURICSEED: consumed; "Mew's Telluric Seed spun a silk cocoon around it!"
- End of round OK - rule 1: heal on {:types=>[:BUG]}: Pinsir: "Pinsir sipped nectar from the silk-hung blossoms."

### Grand Stage (`GRAND_STAGE`)
- Boost: Swift: 58 dmg on field vs 45 without (NORMAL-type moves x1.3)
- Transition FIRED - stage 1: flags Dance x2 -> stage +1: fired with Quiver Dance, Quiver Dance
- Transition FIRED - stage 1: flags Sound, category damaging x2 -> stage +1: fired with Overdrive, Overdrive
- Transition FIRED - stage 1: moves CELEBRATE/ENCORE/FAKEOUT... x2 -> stage +1: fired with Celebrate, Celebrate
- Transition FIRED - stage 1: moves PROTECT/DETECT/SUBSTITUTE... -> stage -1: fired with Protect
- Transition FIRED - stage 2: flags Dance x2 -> stage +1: fired with Quiver Dance, Quiver Dance
- Transition FIRED - stage 2: flags Sound, category damaging x2 -> stage +1: fired with Overdrive, Overdrive
- Transition FIRED - stage 2: moves CELEBRATE/ENCORE/FAKEOUT... x2 -> stage +1: fired with Celebrate, Celebrate
- Seed OK - SYNTHETICSEED: consumed; "Mew's Synthetic Seed put it in the spotlight! It's here to perform!"

### Water Surface (`WATER_SURFACE`)
- Boost: Water Pulse: 66 dmg on field vs 45 without (WATER-type moves x1.5)
- Transition FIRED - stage 1: moves DIVE -> UNDERWATER: fired with Dive
- Transition FIRED - stage 1: moves GRAVITY -> UNDERWATER: fired with Gravity
- Transition FIRED - stage 1: moves BLIZZARD/SHEERCOLD/GLACIATE... x3 -> FROZEN_LAKE: fired with Glaciate, Glaciate, Glaciate
- Transition FIRED - stage 1: moves SLUDGEWAVE/TOXIC/ACIDSPRAY x2 -> CORROSIVE_MIRE: fired with Sludge Wave, Sludge Wave
- Seed OK - ELEMENTALSEED: consumed; "Mew's Elemental Seed wrapped it in a veil of seawater!"
- End of round OK - rule 1: cure_status on {:grounded=>true, :status=>[:BURN]}: Florges: "The cool water soothed Florges's burn!"
- End of round OK - rule 2: heal on {:abilities=>[:WATERABSORB]}: Florges: "Florges soaked up the spray."

### Underwater (`UNDERWATER`)
- Boost: Water Pulse: 99 dmg on field vs 45 without (WATER-type moves x1.5)
- Transition FIRED - stage 1: moves DIVE/BOUNCE/FLY... -> WATER_SURFACE: fired with Dive
- Transition FIRED - stage 1: moves SLUDGEWAVE x2 -> CORROSIVE_MIRE: fired with Sludge Wave, Sludge Wave
- Seed OK - ELEMENTALSEED: consumed; "Mew's Elemental Seed released a shimmering bubble of air around it!"
- End of round OK - rule 1: heal on {:abilities=>[:WATERABSORB, :DRYSKIN]}: Florges: "Florges drank in the sea."

### Neon Grid (`NEON_GRID`)
- Boost: Thunderbolt: 99 dmg on field vs 66 without (ELECTRIC-type moves x1.5)
- Transition FIRED - stage 1: moves EARTHQUAKE/MAGNITUDE/BULLDOZE... x2 -> stage 2: fired with Earthquake, Earthquake
- Transition FIRED - stage 1: moves SURF/MUDDYWATER/HYDROPUMP... x2 -> stage 2: fired with Surf, Surf
- Transition FIRED - stage 1: moves MUDSPORT -> stage 2: fired with Mud Sport
- Transition FIRED - stage 2: moves CHARGE/DISCHARGE/PARABOLICCHARGE... x2 -> stage 1: fired with Charge, Charge
- Transition FIRED - stage 2: terrain Electric -> stage 1: fired with Electric Terrain
- Seed OK - SYNTHETICSEED: consumed; "Mew's Synthetic Seed magnetized it above the grid!"
- End of round OK - rule 1: stats on {:abilities=>[:MOTORDRIVE], :grounded=>true}: Florges: "Florges drew current from the grid!"
- End of round OK - rule 2: heal on {:abilities=>[:VOLTABSORB]}: Florges: "Florges drew power from the grid."

### Desert (`DESERT`)
- Boost: Earth Power: 79 dmg on field vs 66 without (GROUND-type moves x1.2)
- Transition FIRED - stage 1: weather Rain/HeavyRain -> stage 2: fired with Rain Dance
- Transition FIRED - stage 1: moves SURF/MUDDYWATER/WATERSPOUT... x3 -> stage 2: fired with Surf, Surf, Surf
- Transition FIRED - stage 1: moves ERUPTION/BLASTBURN/FUSIONFLARE... x2 -> ASHEN_WASTE: fired with Eruption, Eruption
- Transition FIRED - stage 2: weather Sun/HarshSun/Sandstorm -> stage 1: fired with Sunny Day
- Transition FIRED - stage 2: types FIRE, category damaging x2 -> stage 1: fired with Flamethrower, Flamethrower
- Seed OK - TELLURICSEED: consumed; "Mew's Telluric Seed half-buried it in hardened sand!"
- End of round OK - rule 1: heal on {:abilities=>[:EARTHEATER]}: Florges: "Florges ate into the dunes."
- End of round OK - rule 2: damage on {:abilities=>[:DRYSKIN]}: Florges: "Florges's skin dried out in the desert heat."

### Corrosive Mire (`CORROSIVE_MIRE`)
- Boost: Sludge Bomb: 99 dmg on field vs 66 without (POISON-type moves x1.5)
- Transition FIRED - stage 1: terrain Misty -> WATER_SURFACE: fired with Misty Terrain
- Transition FIRED - stage 1: moves PURIFY x2 -> WATER_SURFACE: fired with Purify, Purify
- Transition FIRED - stage 1: types FIRE, category damaging x2 -> WASTELAND: fired with Flamethrower, Flamethrower
- Seed OK - SYNTHETICSEED: consumed; "Mew's Synthetic Seed filled it with corrosive vigor!"
- End of round OK - rule 1: heal on {:types=>[:POISON]}: Muk: "The mire nourished Muk."
- End of round OK - rule 2: proc on {:types=>[:POISON]}: Muk: "The mire nourished Muk."

### Volcanic Field (`VOLCANIC`)
- Boost: Flamethrower: 99 dmg on field vs 66 without (FIRE-type moves x1.5)
- Transition FIRED - stage 1: moves SURF/MUDDYWATER/WATERSPOUT... x2 -> ASHEN_WASTE: fired with Surf, Surf
- Transition FIRED - stage 1: weather Rain/HeavyRain -> ASHEN_WASTE: fired with Rain Dance
- Transition FIRED - stage 1: weather Sandstorm -> ASHEN_WASTE: fired with Sandstorm
- Seed OK - ELEMENTALSEED: consumed; "Mew's Elemental Seed ignited, filling it with volcanic power!"
- End of round OK - rule 1: heal on {:abilities=>[:MAGMAARMOR]}: Florges: "Florges basked in the magma."
- End of round OK - rule 2: cure_status on {:status=>[:FROZEN]}: Florges: "Florges thawed out!"
- End of round NOT OBSERVED - end_of_round hook: hook ran for 7 rounds without visible output

### Cinderglass (`ASHEN_WASTE`)
- Boost: Power Gem: 99 dmg on field vs 59 without (ROCK-type moves x1.3)
- Transition FIRED - stage 1: moves ERUPTION/LAVAPLUME/MAGMASTORM... x3 -> VOLCANIC: fired with Eruption, Eruption, Eruption
- Transition FIRED - stage 1: moves SURF/MUDDYWATER/HYDROPUMP... x3 -> WATER_SURFACE: fired with Surf, Surf, Surf
- Transition FIRED - stage 1: weather HeavyRain -> WATER_SURFACE: fired with Splash
- Seed OK - ELEMENTALSEED: consumed; "Mew's Elemental Seed wrapped it in a cloak of steam!"
- End of round OK - rule 1: stats on {:abilities=>[:STEAMENGINE]}: Florges: "Florges drew power from the steam vents!"
- End of round OK - end_of_round hook: "The ground hisses... the geysers will blow next turn! / Geysers of steam blast up through the glass!"

### Inverse Field (`INVERSE`)
- Boost: Shadow Ball: 63 dmg on field vs 53 without (GHOST-type moves x1.2)
- Transition FIRED - stage 1: moves TOPSYTURVY -> (proc): fired with Growl, Topsy-Turvy
- Seed OK - MAGICALSEED: consumed; "Mew's Magical Seed turned its world upside down!"

### The Bleed (`BLEED`)
- Boost: Judgment: 113 dmg on field vs 73 without (Judgment x1.3)
- Seed OK - MAGICALSEED: consumed; "Mew's Magical Seed drank from the Bleed!"
- Seed OK - SYNTHETICSEED: consumed; "Mew's Synthetic Seed insulated it against the Bleed!"
- End of round OK - rule 1: proc on {}: Florges: "The Bleed warped Florges's power!"

### Colosseum (`COLOSSEUM`)
- Boost: Aura Sphere: 63 dmg on field vs 53 without (FIGHTING-type moves x1.2)
- Transition NOT OBSERVED - stage 1: check proc -> stage 2: did NOT fire with GROWL, SPLASH, SPLASH, SPLASH, SPLASH, SPLASH, SPLASH, SPLASH, SPLASH
- Transition FIRED - stage 1: moves EARTHQUAKE/MAGNITUDE/BULLDOZE... x3 -> CAVE: fired with Earthquake, Earthquake, Earthquake
- Transition FIRED - stage 2: moves PROTECT/DETECT/REST... x2 -> stage 1: fired with Protect, Protect
- Seed OK - SYNTHETICSEED: consumed; "Mew's Synthetic Seed fired it up to the roar of the crowd!"

### Flower Garden (`FLOWER_GARDEN`)
- Boost: Energy Ball: 73 dmg on field vs 66 without (GRASS-type moves x1.1)
- Transition FIRED - stage 1: moves GROWTH/ROTOTILLER/FLOWERSHIELD... -> stage +1: fired with Growth
- Transition FIRED - stage 1: weather Sun/HarshSun/Rain/HeavyRain -> stage +1: fired with Sunny Day
- Transition FIRED - stage 1: terrain Grassy -> stage +1: fired with Grassy Terrain
- Transition FIRED - stage 1: types GRASS, category damaging x2 -> stage +1: fired with Energy Ball, Energy Ball
- Transition FIRED - stage 1: types FIRE, category damaging -> stage -1: fired with Flamethrower
- Transition FIRED - stage 1: moves CUT/FURYCUTTER/SLASH... -> stage -1: fired with Cut
- Transition FIRED - stage 1: weather Hail -> stage -1: fired with Hail
- Transition FIRED - stage 1: moves ACIDSPRAY/SLUDGEWAVE/CORROSIVEGAS... -> stage 1: fired with Acid Spray
- Transition FIRED - stage 2: moves GROWTH/ROTOTILLER/FLOWERSHIELD... -> stage +1: fired with Growth
- Transition FIRED - stage 2: weather Sun/HarshSun/Rain/HeavyRain -> stage +1: fired with Sunny Day
- Transition FIRED - stage 2: terrain Grassy -> stage +1: fired with Grassy Terrain
- Transition FIRED - stage 2: types GRASS, category damaging x2 -> stage +1: fired with Energy Ball, Energy Ball
- Transition FIRED - stage 3: moves GROWTH/ROTOTILLER/FLOWERSHIELD... -> stage +1: fired with Growth
- Transition FIRED - stage 3: weather Sun/HarshSun/Rain/HeavyRain -> stage +1: fired with Sunny Day
- Transition FIRED - stage 3: terrain Grassy -> stage +1: fired with Grassy Terrain
- Transition FIRED - stage 3: types GRASS, category damaging x2 -> stage +1: fired with Energy Ball, Energy Ball
- Transition FIRED - stage 4: moves GROWTH/ROTOTILLER/FLOWERSHIELD... -> stage +1: fired with Growth
- Transition FIRED - stage 4: weather Sun/HarshSun/Rain/HeavyRain -> stage +1: fired with Sunny Day
- Transition FIRED - stage 4: terrain Grassy -> stage +1: fired with Grassy Terrain
- Transition FIRED - stage 4: types GRASS, category damaging x2 -> stage +1: fired with Energy Ball, Energy Ball
- Transition FIRED - stage 5: types FIRE, category damaging x2 -> WILDFIRE: fired with Flamethrower, Flamethrower
- Seed OK - TELLURICSEED: consumed; "Mew's Telluric Seed took root in the garden!"

### Frozen Lake (`FROZEN_LAKE`)
- Boost: Ice Beam: 99 dmg on field vs 66 without (ICE-type moves x1.5)
- Transition FIRED - stage 1: condition proc x3 -> WATER_SURFACE: fired with Flamethrower, Flamethrower, Flamethrower
- Transition FIRED - stage 1: types ICE, category damaging rewinds {:crack=>1}: fired with Flamethrower, Ice Beam
- Transition FIRED - stage 1: weather Sun/HarshSun -> WATER_SURFACE: fired with Sunny Day
- Seed OK - ELEMENTALSEED: consumed; "Mew's Elemental Seed sent it skating at full speed - straight across the jagged ice!"

### Stormfront (`STORMFRONT`)
- Boost: Air Slash: 66 dmg on field vs 56 without (FLYING-type moves x1.2)
- Transition FIRED - stage 1: moves SUNNYDAY x2 -> RAINBOW: fired with Sunny Day, Sunny Day
- Seed OK - ELEMENTALSEED: consumed; "Mew's Elemental Seed crackled with storm energy!"
- End of round OK - rule 1: damage on {:grounded=>false, :in_weather=>[:Rain, :HeavyRain], :not_types=>[:ELECTRIC], :not_abilities=>[:LIGHTNINGROD, :VOLTABSORB, :MOTORDRIVE]}: Tornadus (RAINDANCE): "Lightning arced down at Tornadus!"
- End of round NOT OBSERVED - rule 2: stats on {:grounded=>false, :in_weather=>[:Rain, :HeavyRain], :types=>[:ELECTRIC], :not_abilities=>[:LIGHTNINGROD, :VOLTABSORB, :MOTORDRIVE]}: no end-of-round effect seen (tried Ampharos)
- End of round OK - rule 3: stats on {:abilities=>[:LIGHTNINGROD], :in_weather=>[:Rain, :HeavyRain]}: Florges (RAINDANCE): "Florges drew a lightning bolt!"
- End of round OK - rule 4: stats on {:abilities=>[:MOTORDRIVE], :in_weather=>[:Rain, :HeavyRain]}: Florges (RAINDANCE): "Florges drew a lightning bolt!"
- End of round OK - rule 5: heal on {:abilities=>[:VOLTABSORB], :in_weather=>[:Rain, :HeavyRain]}: Florges (RAINDANCE): "Florges drew a lightning bolt!"

### Mindscape (`MINDSCAPE`)
- Boost: Psychic: 148 dmg on field vs 99 without (PSYCHIC-type moves x1.5)
- Transition FIRED - stage 1: moves DARKVOID/NIGHTMARE/SPITE -> stage 2: fired with Dark Void
- Transition FIRED - stage 1: types DARK, category damaging x3 -> stage 2: fired with Dark Pulse, Dark Pulse, Dark Pulse
- Transition FIRED - stage 1: moves TOPSYTURVY -> INVERSE: fired with Growl, Topsy-Turvy
- Transition FIRED - stage 1: flags Sound, category damaging x3 -> INVERSE: fired with Overdrive, Overdrive, Overdrive
- Transition FIRED - stage 2: moves CALMMIND/AROMATHERAPY/HEALBELL... x2 -> stage 1: fired with Calm Mind, Calm Mind
- Seed OK - MAGICALSEED: consumed; "Mew's Magical Seed flooded its mind with thoughts!"
- End of round OK - rule 1: proc on {:status=>[:SLEEP]}: Florges: "Florges is stirring in its dream..."

### Crystal Cavern (`CRYSTAL_CAVERN`)
- Boost: Power Gem: 113 dmg on field vs 59 without (ROCK-type moves x1.3)
- Transition FIRED - stage 1: moves DARKPULSE/NIGHTDAZE/DARKVOID... -> DARK_CRYSTAL: fired with Dark Pulse
- Transition FIRED - stage 1: weather Sandstorm -> DARK_CRYSTAL: fired with Sandstorm
- Transition FIRED - stage 1: moves EXPLOSION/SELFDESTRUCT/MISTYEXPLOSION -> CAVE: fired with Explosion
- Transition FIRED - stage 1: moves EARTHQUAKE/MAGNITUDE/BULLDOZE... x3 -> CAVE: fired with Earthquake, Earthquake, Earthquake
- Seed OK - MAGICALSEED: consumed; "Mew's Magical Seed refracted the crystals' light around it!"
- End of round OK - end_of_round hook: "The crystals shifted to amethyst! / The crystals flared a fiery red!"

### Dark Crystal Cavern (`DARK_CRYSTAL`)
- Boost: Dark Pulse: 87 dmg on field vs 59 without (DARK-type moves x1.5)
- Transition FIRED - stage 1: moves AURORABEAM/SIGNALBEAM/FLASHCANNON... x2 -> CRYSTAL_CAVERN: fired with Aurora Beam, Aurora Beam
- Transition FIRED - stage 1: weather Sun/HarshSun -> CRYSTAL_CAVERN: fired with Sunny Day
- Transition FIRED - stage 1: moves EXPLOSION/SELFDESTRUCT/MISTYEXPLOSION -> CAVE: fired with Explosion
- Transition FIRED - stage 1: moves EARTHQUAKE/MAGNITUDE/BULLDOZE... x3 -> CAVE: fired with Earthquake, Earthquake, Earthquake
- Seed OK - MAGICALSEED: consumed; "Mew's Magical Seed drank in the darkness!"

### Hollow Cathedral (`HOLLOW_CATHEDRAL`)
- Boost: Shadow Ball: 79 dmg on field vs 53 without (GHOST-type moves x1.5)
- Transition FIRED - stage 1: moves SACREDFIRE/SACREDSWORD/JUDGMENT... x3 -> stage 2: fired with Sacred Fire, Sacred Fire, Sacred Fire
- Transition FIRED - stage 1: moves TOPSYTURVY -> INVERSE: fired with Growl, Topsy-Turvy
- Transition FIRED - stage 1: moves BOOMBURST/SHADOWFORCE/HYPERSPACEFURY... x2 -> INVERSE: fired with Boomburst, Boomburst
- Transition FIRED - stage 2: moves CURSE/SPITE/GRUDGE... x2 -> stage 1: fired with Curse, Curse
- Seed OK - MAGICALSEED: consumed; "Mew's Magical Seed let a wandering spirit possess it!"

### Factory (`FACTORY`)
- Boost: Flash Cannon: 113 dmg on field vs 59 without (STEEL-type moves x1.5)
- Transition FIRED - stage 1: moves EXPLOSION/SELFDESTRUCT/MISTYEXPLOSION... -> SCRAPYARD: fired with Explosion
- Transition FIRED - stage 1: moves EARTHQUAKE/MAGNITUDE/BULLDOZE... x3 -> SCRAPYARD: fired with Earthquake, Earthquake, Earthquake
- Seed OK - SYNTHETICSEED: consumed; "Mew's Synthetic Seed oiled its joints like factory machinery!"
- End of round OK - rule 1: cure_status on {:status=>[:FROZEN]}: Florges: "The crucibles' heat thawed Florges out!"

### Scrapyard (`SCRAPYARD`)
- Boost: Flash Cannon: 71 dmg on field vs 59 without (STEEL-type moves x1.2)
- Transition FIRED - stage 1: moves CHARGE/DISCHARGE/PARABOLICCHARGE... x3 -> FACTORY: fired with Charge, Charge, Charge
- Transition FIRED - stage 1: moves ACIDSPRAY/SLUDGEWAVE/CORROSIVEGAS... x2 -> WASTELAND: fired with Acid Spray, Acid Spray
- Seed OK - SYNTHETICSEED: consumed; "Mew's Synthetic Seed bolted scrap armor onto it!"

### New Moon (`NEW_MOON`)
- Boost: Dark Pulse: 105 dmg on field vs 59 without (DARK-type moves x1.5)
- Transition FIRED - stage 1: moves DARKVOID -> stage 2: fired with Dark Void
- Transition FIRED - stage 1: moves DARKPULSE/NIGHTDAZE/MOONGEISTBEAM... x3 -> stage 2: fired with Moongeist Beam, Moongeist Beam, Moongeist Beam
- Transition FIRED - stage 1: moves FLASH/TAILGLOW/DAZZLINGGLEAM... x3 -> stage 3: fired with Flash, Flash, Flash
- Transition FIRED - stage 2: moves FLASH/TAILGLOW/DAZZLINGGLEAM... x2 -> stage 1: fired with Flash, Flash
- Transition FIRED - stage 3: types DARK, category damaging x3 -> stage 1: fired with Dark Pulse, Dark Pulse, Dark Pulse
- Seed OK - MAGICALSEED: consumed; "Mew's Magical Seed sharpened its night vision!"

### Fairy Tale (`FAIRY_TALE`)
- Boost: Moonblast: 104 dmg on field vs 70 without (FAIRY-type moves x1.5)
- Transition FIRED - stage 1: types DRAGON, category damaging x3 -> DRAGONS_DEN: fired with Dragon Pulse, Dragon Pulse, Dragon Pulse
- Seed OK - MAGICALSEED: consumed; "Mew's Magical Seed granted it a fairy godmother's blessing!"
- End of round OK - rule 1: heal on {:status=>[:SLEEP]}: Florges: "Florges dreams of happily ever after."

### Dragon's Den (`DRAGONS_DEN`)
- Boost: Dragon Pulse: 94 dmg on field vs 62 without (DRAGON-type moves x1.5)
- Transition FIRED - stage 1: types WATER/ICE, category damaging x3 -> CAVE: fired with Water Pulse, Water Pulse, Water Pulse
- Transition FIRED - stage 1: types FAIRY, category damaging x3 -> FAIRY_TALE: fired with Moonblast, Moonblast, Moonblast
- Transition FIRED - stage 1: types DRAGON, category damaging x4 -> stage 2: fired with Dragon Pulse, Dragon Pulse, Dragon Pulse, Dragon Pulse
- Seed OK - ELEMENTALSEED: consumed; "Mew's Elemental Seed kindled dragonfire within it!"

### Cave (`CAVE`)
- Boost: Power Gem: 87 dmg on field vs 59 without (ROCK-type moves x1.5)
- Transition FIRED - stage 1: moves EARTHQUAKE/MAGNITUDE/BULLDOZE... -> stage 2: fired with Earthquake
- Transition FIRED - stage 1: moves POWERGEM/DIAMONDSTORM x2 -> CRYSTAL_CAVERN: fired with Power Gem, Power Gem
- Transition FIRED - stage 1: moves ERUPTION/LAVAPLUME/MAGMASTORM... x2 -> VOLCANIC: fired with Eruption, Eruption
- Transition FIRED - stage 1: moves DRACOMETEOR -> DRAGONS_DEN: fired with Draco Meteor
- Transition FIRED - stage 1: moves DRAGONPULSE/DRAGONENERGY/CLANGINGSCALES x2 -> DRAGONS_DEN: fired with Dragon Pulse, Dragon Pulse
- Transition FIRED - stage 2: moves EARTHQUAKE/MAGNITUDE/BULLDOZE... -> stage 1: fired with Earthquake
- Seed OK - TELLURICSEED: consumed; "Mew's Telluric Seed shook stones loose from the ceiling!"

### Mountain (`MOUNTAIN`)
- Boost: Power Gem: 87 dmg on field vs 59 without (ROCK-type moves x1.5)
- Transition FIRED - stage 1: weather Hail -> SNOWY_MOUNTAIN: fired with Hail
- Transition FIRED - stage 1: moves BLIZZARD/MOUNTAINGALE/SHEERCOLD... x2 -> SNOWY_MOUNTAIN: fired with Blizzard, Blizzard
- Transition FIRED - stage 1: moves ERUPTION/LAVAPLUME/MAGMASTORM... x2 -> VOLCANIC: fired with Eruption, Eruption
- Seed OK - TELLURICSEED: consumed; "Mew's Telluric Seed caught the mountain wind!"

### Snowy Mountain (`SNOWY_MOUNTAIN`)
- Boost: Ice Beam: 99 dmg on field vs 66 without (ICE-type moves x1.5)
- Transition FIRED - stage 1: moves ERUPTION/MAGMASTORM x2 -> VOLCANIC: fired with Eruption, Eruption
- Transition FIRED - stage 1: weather Sun/HarshSun -> MOUNTAIN: fired with Sunny Day
- Transition FIRED - stage 1: moves HEATWAVE/LAVAPLUME/FIREPLEDGE... x2 -> MOUNTAIN: fired with Heat Wave, Heat Wave
- Seed OK - TELLURICSEED: consumed; "Mew's Telluric Seed packed it in a shell of snow!"
- End of round OK - rule 1: cure_status on {:grounded=>true, :status=>[:BURN]}: Florges: "The deep snow soothed Florges's burn!"

### Beach (`BEACH`)
- Boost: Water Pulse: 53 dmg on field vs 45 without (WATER-type moves x1.2)
- Transition FIRED - stage 1: weather HeavyRain -> WATER_SURFACE: fired with Splash
- Transition FIRED - stage 1: moves SURF/MUDDYWATER/WATERSPOUT... x3 -> WATER_SURFACE: fired with Surf, Surf, Surf
- Seed OK - TELLURICSEED: consumed; "Mew's Telluric Seed buried it in cool, wet sand!"
- End of round OK - rule 1: heal on {:abilities=>[:WATERABSORB, :DRYSKIN]}: Florges: "Florges soaked up the sea spray."
- End of round OK - rule 2: cure_status on {:abilities=>[:HYDRATION]}: Florges: "HP Florges (player): 148 -> 130 / 297"

### Rainbow (`RAINBOW`)
- Boost: Swift: 66 dmg on field vs 45 without (NORMAL-type moves x1.5)
- Transition FIRED - stage 1: weather Sandstorm/Hail -> (proc): fired with Sandstorm
- Transition FIRED - stage 1: moves DEFOG -> (proc): fired with Defog
- Seed OK - MAGICALSEED: consumed; "Mew's Magical Seed shimmered in every colour!"
- End of round OK - rule 1: heal on {:status=>[:SLEEP]}: Florges: "Florges is having sweet dreams beneath the rainbow."
- End of round OK - rule 2: proc on {:abilities=>[:CLOUDNINE]}: Florges: "Florges's Defense rose!"

### Wasteland (`WASTELAND`)
- Boost: Sludge Bomb: 95 dmg on field vs 66 without (POISON-type moves x1.2)
- Transition FIRED - stage 1: terrain Grassy -> FLOWER_GARDEN: fired with Grassy Terrain
- Transition FIRED - stage 1: moves PURIFY x2 -> MEADOW: fired with Purify, Purify
- Seed OK - TELLURICSEED: consumed; "Mew's Telluric Seed drew power from the tainted ground!"
- End of round OK - rule 1: heal on {:abilities=>[:POISONHEAL], :status=>[:POISON]}: Florges: "Florges thrived on the toxic wastes."

### Prism Arena (`PRISM_ARENA`)
- Boost: Tri Attack: 76 dmg on field vs 59 without (Tri Attack x1.3)
- Seed OK - MAGICALSEED: consumed; "Mew's Magical Seed refracted the light of the Plates!"
- End of round OK - rule 1: heal on {} +condition: Snorlax (SPLASH): "Snorlax's Plate resonated with the arena!"
- End of round OK - end_of_round hook: "The Flame Plate begins to glow... After the next turn, the arena becomes the Volcanic Field! / The Plates turn! The Flame Plate blazes, and the arena becomes the Volcanic Field!"

### Wildfire (`WILDFIRE`)
- Boost: Flamethrower: 99 dmg on field vs 66 without (FIRE-type moves x1.5)
- Transition FIRED - stage 1: check proc -> stage 2: fired with Splash, Splash, Splash, Splash, Splash, Splash, Splash, Splash
- Transition FIRED - stage 1: moves SURF/MUDDYWATER/HYDROPUMP... x2 -> stage 2: fired with Surf, Surf
- Transition FIRED - stage 1: moves DEFOG/WHIRLWIND/TAILWIND -> stage 2: fired with Defog
- Transition FIRED - stage 1: weather Rain/HeavyRain/Sandstorm -> stage 2: fired with Rain Dance
- Transition FIRED - stage 2: moves ERUPTION/LAVAPLUME/HEATWAVE... x2 -> stage 1: fired with Eruption, Eruption
- Transition FIRED - stage 2: weather Sun/HarshSun -> stage 1: fired with Sunny Day
- Transition FIRED - stage 2: weather Rain/HeavyRain -> MEADOW: fired with Rain Dance
- Transition FIRED - stage 2: terrain Grassy -> MEADOW: fired with Grassy Terrain
- Transition FIRED - stage 2: moves GROWTH/INGRAIN/GRASSPLEDGE... x2 -> MEADOW: fired with Growth, Growth
- Seed OK - ELEMENTALSEED: consumed; "Mew's Elemental Seed caught the blaze inside it!"
- End of round OK - end_of_round hook: "The wildfire is starting to burn itself out... / ## FIELD STAGE: WILDFIRE is now stage 2"

### Meadow (`MEADOW`)
- Boost: Energy Ball: 79 dmg on field vs 66 without (GRASS-type moves x1.2)
- Transition FIRED - stage 1: types FIRE, category damaging, condition proc x2 -> WILDFIRE: fired with Flamethrower, Flamethrower
- Transition FIRED - stage 1: types FIRE, category damaging -> WILDFIRE: fired with Sunny Day, Flamethrower
- Transition FIRED - stage 1: terrain Grassy -> FLOWER_GARDEN: fired with Grassy Terrain
- Transition FIRED - stage 1: moves GROWTH/ROTOTILLER/FLOWERSHIELD... x2 -> FLOWER_GARDEN: fired with Growth, Growth
- Seed OK - TELLURICSEED: consumed; "Mew's Telluric Seed let it vanish into the tall grass!"
- End of round OK - rule 1: heal on {:abilities=>[:SAPSIPPER]}: Florges: "Florges grazed on the meadow."

