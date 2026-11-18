# Prismfall Fields (v1.1, Revision 10 redesign)

Player-facing reference for all 33 battle fields. The per-field sections are generated from the field files
(`plugins/Prismfall Field Effects/1xx_Field_*.rb`: `:description`, `:notes`, transitions, seed), so they match what
the in-game **Field Notes** show. DSL: `FIELD_API.md`. Research behind the redesign: `FIELD_RESEARCH.md`.
Map defaults: `FIELD_DEFAULTS.yaml`. Backdrop keys: `FIELD_BACKDROPS_NEEDED.md`.

## What changed in the redesign

- **Voice.** Pokémon use the place. Messages have the Pokémon as the actor ("rode the updraft", "drank from the
  geyser"). No field describes Pokémon as helpless against the scenery; hazards are things matching types exploit.
- **Depth, in the Reborn style.** Each field has 15–30 interactions: type and move boosts, abilities that are always
  active, status immunities, longer screens and weather, changed secondary effects, a seed with a trade-off, a
  natural type (Camouflage, Mimicry, Terrain Pulse, Nature Power) and a family (elemental, telluric, synthetic, magical).
- **Transform strike.** The move that changes the field hits 1.3× harder.
- **No dead ends.** Every transition leads to a full field. Ashen Waste is now **Cinderglass** (same ID
  `:ASHEN_WASTE`): quenched lava turned to volcanic glass, with geysers every 3 rounds, steam, and obsidian shards.
- **Two new fields:** **Wildfire** (what Silkwood, Meadow and an overgrown Flower Garden burn into; it burns down
  to Embers and regrows into Meadow) and **Meadow** (the open-country default).
- **Stages** on Grand Stage (applause), Neon Grid (Blackout), Desert (Superbloom), Colosseum (Frenzy), Mindscape
  (Nightmare), Hollow Cathedral (Consecrated), New Moon (Abyss, Lamplight), Dragon's Den (Awakened), Cave (cracked
  ceiling), Wildfire (Embers) and Flower Garden (5 growth stages).
- **Every battle has a field**: see the end of this file.

## Transition map

`A → B (trigger)`. "×n" = that many uses. Stage changes inside one field are listed in its section.

| From | To |
|---|---|
| Silkwood | Wildfire (Fire moves ×3, ×2 in sun) |
| Meadow | Wildfire (Fire ×2, ×1 in sun); Flower Garden (Grassy Terrain, growth moves ×2) |
| Flower Garden (stage 5) | Wildfire (Fire ×2) |
| Wildfire | Embers stage (burns out after 4 rounds unless fed; water, wind, rain); Embers → Meadow (rain, Grassy Terrain, growth moves ×2) or back to Wildfire (big Fire moves ×2, sun) |
| Volcanic | Cinderglass (big Water or Ice moves ×2, rain, sandstorm) |
| Cinderglass | Volcanic (eruption moves ×3); Water Surface (big Water moves ×3, heavy rain) |
| Desert | Superbloom stage (rain, Water moves ×3); Cinderglass (hottest Fire moves ×2) |
| Cave | Crystal Cavern (Power Gem, Diamond Storm ×2); Volcanic (eruption moves ×2); Dragon's Den (Draco Meteor, dragon moves ×2) |
| Mountain | Snowy Mountain (hail, blizzard moves ×2); Volcanic (eruption moves ×2) |
| Snowy Mountain | Mountain (sun, big Fire moves ×2); Volcanic (Eruption, Magma Storm ×2) |
| Beach | Water Surface (tide: big Water moves ×3, heavy rain) |
| Water Surface | Underwater (Dive, Gravity); Frozen Lake (big Ice moves ×3); Corrosive Mire (Sludge Wave, Toxic, Acid Spray ×2) |
| Underwater | Water Surface (Dive, Fly, Bounce, Sky Drop); Corrosive Mire (Sludge Wave ×2) |
| Frozen Lake | Water Surface (Fire or quake hits ×3, sun; Ice moves refreeze) |
| Corrosive Mire | Water Surface (Misty Terrain, Purify ×2); Wasteland (Fire ×2) |
| Wasteland | Meadow (Purify ×2); Flower Garden (Grassy Terrain) |
| Stormfront | Rainbow (Sunny Day ×2) |
| Rainbow | the field it came from, else Meadow (sandstorm, hail, Defog) |
| Crystal Cavern | Dark Crystal (Dark Pulse-style moves, sandstorm); Cave (explosions, quakes ×3) |
| Dark Crystal | Crystal Cavern (light moves ×2, sun); Cave (explosions, quakes ×3) |
| Factory | Scrapyard (explosions, quakes ×3) |
| Scrapyard | Factory (Electric charging moves ×3); Wasteland (acid moves ×2) |
| Colosseum | Frenzy stage (knockouts); Cave (quakes ×3: the arena floor gives way) |
| Fairy Tale | Dragon's Den (Dragon moves ×3) |
| Dragon's Den | Awakened stage (Dragon ×4); Cave (Water/Ice ×3); Fairy Tale (Fairy ×3) |
| Mindscape | Nightmare stage; Inverse (Topsy-Turvy, damaging sound moves ×3 crack the dream) |
| Hollow Cathedral | Consecrated stage (holy moves ×3); Inverse (Topsy-Turvy, Boomburst/Shadow Force ×2) |
| Inverse | the field it came from, else Mindscape (Topsy-Turvy) |
| The Bleed, Prism Arena | none (they borrow other fields' effects in rotation) |
| Grand Stage, Neon Grid, New Moon, Stormfront* | stage changes only (*Stormfront also → Rainbow) |

## Silkwood (`:SILKWOOD`)

*Telluric field. Backdrop `field_silkwood`. Nature Power: BUGBUZZ. Natural type: BUG.*

> Giant webs glisten between the ancient trees...

Bugs ride the silk, the threads carry current, blades cut paths and fire races along the webs.

- Bug x1.5, Grass x1.2, Fire x1.2. Swarm and Overgrow are always active.
- Electroweb x1.5 and never misses: the current runs along the threads (30% paralysis). In rain every Electric move rides the wet silk (x1.2).
- Attack Order, Struggle Bug, Silver Wind x1.5; Lunge, Leech Life, Pounce, Fell Stinger, First Impression x1.3.
- Blades (Cut, X-Scissor, Leaf Blade...) x1.2. Bug-type fliers glide on the silk (Flying x1.2); other fliers weave through it (x0.8).
- Bug contact moves may wrap the target in silk (Speed -1). Bug moves' own added effects are twice as likely.
- String Shot, Electroweb, Sticky Web never miss; String Shot and Silk Trap bind tighter; Defend Order +1 Def more.
- Grounded non-Bug Pokemon step into fresh silk the first time they enter (Speed -1; Heavy-Duty Boots avoid it).
- Bug types sip nectar each turn (1/16 HP). Grassy Terrain +3 turns, Electric Terrain +2 (the webs hold the charge).
- Fire races along the silk: 3 damaging Fire moves (2 in sunlight) set it ablaze -> Wildfire.
- Telluric Seed: +1 Defense, +1 Sp. Def, but the cocoon slows it (-1 Speed).

**Changes:**
- FIRE-type moves x3 → **Wildfire**
- FIRE-type moves, in Sun/HarshSun x2 → **Wildfire**

**Seed (TELLURICSEED):** DEFENSE +1, SPECIAL_DEFENSE +1, SPEED -1.

## Grand Stage (`:GRAND_STAGE`)

*Synthetic field. Backdrop `field_grand_stage`. Nature Power: HYPERVOICE. Natural type: NORMAL.*

> The curtain rises! The spotlight blazes over the stage!

An opera house that plays to the crowd: songs, dances and showpieces build applause in three stages; stalling bores it.

- Applause has 3 stages: Opening Night, Encore, Standing Ovation. Starts at 1.
- Up a stage: 2 dances, 2 damaging sound moves, 2 showpieces (Fake Out, Acrobatics, Pay Day, Celebrate, Encore...), or any critical hit.
- Down a stage: stalling - Protect, Detect, Substitute, Recover, Rest, Yawn, Roost, Splash...
- Normal x1.3 / x1.5 / x1.5. Damaging sound and dance moves x1.3 / x1.4 / x1.5 (Punk Rock, Liquid Voice x1.2 more).
- Pay Day x2; Acrobatics, Drum Beating, Fake Out x1.5; Last Resort x1.3. Sound moves may dazzle (10% confusion).
- Status dances also give +1 Speed; Celebrate raises every stat; Charm-style moves also lower Sp. Atk. Encore lasts 2 turns longer.
- Standing Ovation: every attack +1 critical-hit stage, Sing never misses, Normal types and Dancers bask in applause (1/16 HP).
- Dancer +1 Speed, Punk Rock / Liquid Voice +1 Sp. Atk on entry. Indoors: no weather.
- Synthetic Seed: +1 Speed and Laser Focus, but the spotlight Taunts the holder.

**Changes:**
- Dance moves x2 → stage +1
- Sound moves x2 → stage +1
- CELEBRATE, ENCORE, FAKEOUT, ACROBATICS, LASTRESORT +6 more x2 → stage +1
- PROTECT, DETECT, SUBSTITUTE, REST, RECOVER +9 more → stage -1
- *Stage 2* (`field_grand_stage_2`): 
  - Dance moves x2 → stage +1
  - Sound moves x2 → stage +1
  - CELEBRATE, ENCORE, FAKEOUT, ACROBATICS, LASTRESORT +6 more x2 → stage +1
  - PROTECT, DETECT, SUBSTITUTE, REST, RECOVER +9 more → stage -1
- *Stage 3* (`field_grand_stage_3`): 
  - PROTECT, DETECT, SUBSTITUTE, REST, RECOVER +9 more → stage -1

**Seed (SYNTHETICSEED):** SPEED +1; effects: laser_focus, taunt.

## Water Surface (`:WATER_SURFACE`)

*Elemental field. Backdrop `field_water_surface`. Nature Power: WHIRLPOOL. Natural type: WATER.*

> The battle is taking place on the open water!

Swimmers ride the currents, electricity races across the surface and flames hiss into steam. Nothing touches the ground.

- Water x1.5. Electric x1.5 against grounded targets. Fire x0.5 against grounded targets (it hisses into steam).
- Torrent, Swift Swim, Hydration, Rain Dish and Dry Skin act as if it were raining.
- Whirlpool x2 (and more accurate); Water Pledge x1.5; Dive, Wave Crash, Brine, Aqua Step, Flip Turn, Anchor Shot x1.3; Muddy Water, Surging Strikes x1.2.
- Ground moves and hazards sink: Earthquake, Magnitude, Bulldoze, Dig, Fissure, Stomping Tantrum, Spikes, Toxic Spikes, Stealth Rock fail.
- Grounded non-Water Pokemon wade at x0.75 Speed. Water attacks may sweep grounded non-Water targets along (Speed -1).
- The cool water soothes grounded Pokemon's burns. Water Absorb sips 1/16 HP a turn. Water Compaction +1 Def, Propeller Tail +1 Speed on entry.
- Rain lasts 3 turns longer, Misty Terrain 2 turns longer. Grassy Terrain can't take root.
- Dive or Gravity -> Underwater. 3 big ice moves -> Frozen Lake. 2 Sludge Waves (or Toxic + Sludge Wave) -> Corrosive Mire.
- Elemental Seed: +1 Speed and Aqua Ring.

**Changes:**
- DIVE → **Underwater**
- GRAVITY → **Underwater**
- BLIZZARD, SHEERCOLD, GLACIATE, ICEBEAM, FREEZEDRY x3 → **Frozen Lake**
- SLUDGEWAVE, TOXIC, ACIDSPRAY x2 → **Corrosive Mire**

**Seed (ELEMENTALSEED):** SPEED +1; effects: aqua_ring.

## Underwater (`:UNDERWATER`)

*Elemental field. Backdrop `field_underwater`. Nature Power: WATERPULSE. Natural type: WATER.*

> Blue silence presses in from every side... The battle is underwater!

The deep belongs to swimmers: Water and Electric surge, sound carries, silt joins ground attacks. Fire can't burn and heavy blows drag.

- Water x1.5. Electric x1.5 and never misses. Flying x0.5 (no air to catch). Sound moves x1.3.
- Ground attacks churn up the seabed and also hit as Water.
- Physical non-Water attacks from non-Water Pokemon x0.5 (Swift Swim and Steelworker swimmers are exempt).
- Anchor Shot x2; Dive, Water Pulse, Whirlpool, Jet Punch x1.5; Octazooka x1.3 (its ink always clouds); Crabhammer, Liquidation x1.2. Whirlpool may spin the target into confusion.
- Fire moves fizzle. Fly, Bounce, Sky Drop and every entry hazard fail. Nothing can be burned; burns wash away on entry.
- Non-Water Pokemon move at half Speed. Torrent, Swift Swim (x2 Speed) and Hydration act as if it were raining.
- No weather or terrain reaches the depths. Water Absorb and Dry Skin drink in the sea (1/16 HP).
- Dive, Bounce, Fly or Sky Drop -> back to the Water Surface. 2 Sludge Waves -> Corrosive Mire.
- Elemental Seed: +1 Speed and Aqua Ring, and the holder adapts to the deep (becomes pure Water type).

**Changes:**
- DIVE, BOUNCE, FLY, SKYDROP → **Water Surface**
- SLUDGEWAVE x2 → **Corrosive Mire**

**Seed (ELEMENTALSEED):** SPEED +1; effects: aqua_ring; special effect.

## Neon Grid (`:NEON_GRID`)

*Synthetic field. Backdrop `field_neon_grid`. Nature Power: DISCHARGE. Natural type: ELECTRIC.*

> Neon circuitry hums beneath your feet!

Electric Pokemon draw power from live circuitry; water and steel conduct; nobody can doze off. Quakes, mud or floods black it out.

- Electric x1.5, Steel x1.2. Pulse moves x1.5; neon light moves (Dazzling Gleam, Flash Cannon, Luster Purge...) x1.3.
- Conductors: Gear Grind, Magnet Bomb, Gyro Ball, Flash Cannon, Steel Beam, Surf and Muddy Water also hit as Electric.
- Rising Voltage, Magnet Bomb x1.5; Discharge, Parabolic Charge, Zing Zap, Plasma Fists, Electro Drift, Overdrive x1.3.
- Damaging Water moves carry the grid's current (30% paralysis). Zap Cannon has 80% accuracy; Thunder x1.2.
- Grounded Pokemon can't fall asleep. Surge Surfer is always active. Magnet Rise lasts 3 turns longer.
- Charge also +1 Sp. Atk; Magnet Rise +1 Speed; Eerie Impulse lowers Sp. Atk one stage more.
- Plus / Minus +1 Sp. Atk on entry; Motor Drive, Lightning Rod, Volt Absorb, Electromorphosis start charged. Each turn Motor Drive gains Speed and Volt Absorb heals.
- Electric Terrain lasts 3 turns longer.
- Blackout: 2 quakes, 2 floods (Surf, Muddy Water, Hydro Pump...) or Mud Sport short the grid -> stage 2.
- Blackout: Electric damage surges in a fixed cycle (x0.5, x1.5, x0.8, x2, x1.2, repeat). Dark x1.3, Ghost x1.2; light moves x1.5 and Flash blinds more. 2 charging moves (or Electric Terrain) reboot the grid.
- Synthetic Seed: +1 Sp. Atk and Magnet Rise (it floats above the live grid).

**Changes:**
- EARTHQUAKE, MAGNITUDE, BULLDOZE, FISSURE, PRECIPICEBLADES +2 more x2 → stage 2
- SURF, MUDDYWATER, HYDROPUMP, WATERSPOUT, WAVECRASH x2 → stage 2
- MUDSPORT → stage 2
- *Stage 2* (`field_neon_grid_blackout`): Blackout: Electric damage surges in a fixed cycle, shadows grow strong and light dazzles. Charge it back up to reboot.
  - CHARGE, DISCHARGE, PARABOLICCHARGE, WILDCHARGE, CHARGEBEAM +7 more x2 → stage 1
  - terrain Electric → stage 1

**Seed (SYNTHETICSEED):** SPECIAL_ATTACK +1; effects: magnet_rise.

## Desert (`:DESERT`)

*Telluric field. Backdrop `field_desert`. Nature Power: SANDTOMB. Natural type: GROUND.*

> Heat shimmers over the endless dunes...

Sand-dwellers own the dunes: sand abilities always work, Ground types hide in the sand, and the bones of Ossaria make weapons. Rain wakes a superbloom; searing heat makes glass.

- Ground x1.2, Fire x1.2. Ice x0.75 and Water x0.8 (the dunes drink them).
- Sand Rush, Sand Force, Sand Veil and Solar Power work without weather (Solar Power costs no HP here).
- Ground-type Pokemon burrow into the sand: special attacks against them deal x0.67.
- Sand Tomb x2; Scorching Sands, Solar Beam, Solar Blade, Needle Arm, Dig x1.5; Sandsear Storm, Thousand Waves, Heat Wave, Pin Missile and bone moves x1.3.
- Physical Ground moves may kick sand in the eyes (20%, accuracy -1). Sand Attack never misses and drops accuracy one stage more; Shore Up also gives +1 Def.
- Earth Eater draws on the dunes (1/16 HP a turn). Dry Skin dries out in the heat (1/8).
- Hail can't form; Sandstorm +3 turns, Sun +2. Grassy Terrain can't take root.
- Rain, or 3 floods (Surf, Muddy Water, Hydro Pump...) -> Superbloom (stage 2). 2 searing moves (Eruption, Blast Burn, Fusion Flare, Blue Flare...) -> Cinderglass.
- Superbloom: Grass x1.5, Bug x1.2, petal and seed moves x1.5, Chlorophyll and Leaf Guard active, Grass types drink 1/16 HP a turn. Sun, sandstorm or 2 fire attacks bake it back to dunes.
- Telluric Seed: +1 Defense, +1 Sp. Def, but it's half-buried (-1 Speed).

**Changes:**
- weather Rain/HeavyRain → stage 2
- SURF, MUDDYWATER, WATERSPOUT, HYDROPUMP, WATERPLEDGE +2 more x3 → stage 2
- ERUPTION, BLASTBURN, FUSIONFLARE, BLUEFLARE, MAGMASTORM +3 more x2 → **Cinderglass**
- *Stage 2* (`field_desert_bloom`): Superbloom: the rain woke the seeds in the sand. Grass, Bug and petal moves surge while it lasts.
  - weather Sun/HarshSun/Sandstorm → stage 1
  - FIRE-type moves x2 → stage 1

**Seed (TELLURICSEED):** DEFENSE +1, SPECIAL_DEFENSE +1, SPEED -1.

## Corrosive Mire (`:CORROSIVE_MIRE`)

*Synthetic field. Backdrop `field_corrosive_mire`. Nature Power: ACIDSPRAY. Natural type: POISON.*

> Toxic sludge bubbles underfoot... the air reeks of corrosion.

Poison Pokemon weaponise the mire: venom laces mud and water, toxins eat through steel, and fire turns the marsh gas into a weapon.

- Poison x1.5; Poison moves' own added effects x1.5 as likely. Poison moves hit Steel types (neutral).
- Grass drinks the toxins: Grass moves also hit as Poison. Mud moves and Muddy Water also hit as Poison.
- Acid, Acid Spray, Smog x2; Clear Smog, Sludge, mud moves, Barb Barrage x1.5; Sludge Wave, Mortal Spin x1.3; Gunk Shot x1.2.
- Venoshock and Barb Barrage hit grounded targets as if they were already poisoned (x2).
- Gunk Shot x1.25 accuracy; Smog and Poison Gas x1.4; Poison Powder, Stun Spore, Sleep Powder x1.25. Damaging Water moves may poison (20%).
- Each turn, every Poison type may fling toxic mud at a grounded foe (30%: poisons). Poison types are nourished (1/16 HP).
- Toxic Boost is always active. Merciless, Corrosion, Poison Touch +1 Attack on entry; Toxic Debris +1 Defense.
- Fire ignites the marsh gas: Fire x1.3 and every damaging Fire move scorches the user's grounded, non-Fire foes for 1/8 HP.
- Misty Terrain, or 2 Purify, cleanse it -> Water Surface. 2 damaging Fire moves burn the gas off -> Wasteland.
- Synthetic Seed: +1 Attack, +1 Sp. Atk, but the holder is poisoned (Guts, Poison Heal and Toxic Boost love it).

**Changes:**
- terrain Misty → **Water Surface**
- PURIFY x2 → **Water Surface**
- FIRE-type moves x2 → **Wasteland**

**Seed (SYNTHETICSEED):** ATTACK +1, SPECIAL_ATTACK +1; status: POISON.

## Volcanic Field (`:VOLCANIC`)

*Elemental field. Backdrop `field_volcanic`. Nature Power: LAVAPLUME. Natural type: FIRE.*

> Magma churns across the battlefield!

Fire Pokemon draw on the magma; winds carry embers; quakes prime eruptions. Water, ice, rain or sand quench it into black glass.

- Fire x1.5, Ice x0.5. Blaze and Flare Boost are always active; Flash Fire starts lit.
- Rock moves come out superheated (also Fire). Wind moves carry embers (also Fire, x1.2).
- Lava Plume, Flame Burst, Fire Spin, Smog, Clear Smog x1.5; Magma Storm, Earth Power, Heat Crash, Torch Song, Scald, Steam Eruption x1.3; Eruption x1.2.
- Smack Down and Thousand Arrows slam the foe onto the glowing crust (x1.5, also Fire). Grass moves wither against grounded targets (x0.5).
- Eruptions: Eruption, Lava Plume, Magma Storm, Earth Power and quakes prime the volcano; at the end of that round it erupts.
- An eruption: Fire types and Flash Fire / Flare Boost users ride it (+1 Atk or Sp. Atk), Magma Armor +1 Def/Sp. Def; lava rains on other grounded Pokemon (1/8, Fire-scaled; Heatproof, Water Veil, Flame Body, Aqua Ring... protect); sleepers wake; all hazards are blown away.
- Will-O-Wisp never misses; damaging Ground moves may burn grounded targets (20%); Smokescreen drops accuracy one stage more.
- Nothing can be frozen. Magma Armor +1 Def on entry and basks in the magma (1/16 HP a turn).
- Hail can't form; Sun +3 turns. Grassy and Misty Terrain burn away.
- Quenching: 2 floods or big ice moves (Surf, Hydro Pump, Water Spout, Muddy Water, Blizzard...), rain or a sandstorm -> Cinderglass.
- Elemental Seed: +1 Attack, +1 Sp. Atk, +1 Speed, but the holder is burned.

**Changes:**
- SURF, MUDDYWATER, WATERSPOUT, HYDROPUMP, WATERPLEDGE +7 more x2 → **Cinderglass**
- weather Rain/HeavyRain → **Cinderglass**
- weather Sandstorm → **Cinderglass**

**Seed (ELEMENTALSEED):** ATTACK +1, SPECIAL_ATTACK +1, SPEED +1; status: BURN.

## Cinderglass (`:ASHEN_WASTE`)

*Elemental field. Backdrop `field_ashen_waste`. Nature Power: SCORCHINGSANDS. Natural type: ROCK.*

> The magma has set into black glass... and steam roars from every crack!

A quenched volcano of obsidian, steam and geysers. Swimmers and fire Pokemon ride the steam; water flashes into blinding clouds; obsidian sharpens every rock.

- Rock x1.3, Ground x1.2, Fire x1.2 (heat still glows under the glass). Ice x0.7.
- Geysers blow every 3 rounds (a quake or Dig sets them off that round): Water and Fire types and Steam Engine ride the steam (+1 Speed); other grounded Pokemon take a 1/8 blast (Water-scaled; Water Veil, Heatproof, Magma Armor, Water Absorb... are safe).
- Water floods (Surf, Hydro Pump, Muddy Water...) flash into steam: every Pokemon that isn't Water or Fire type loses 1 accuracy.
- Scald, Steam Eruption, Hydro Steam x1.5 and burn more often (x1.5).
- Obsidian shards: Stone Edge, Stone Axe, Rock Slide, Rock Throw, Power Gem, Diamond Storm, Rock Wrecker x1.3. Stealth Rock cuts twice as deep (Heavy-Duty Boots protect).
- Wind moves whip up glass grit: they also hit as Rock and may lower accuracy (30%). Sandstorms become glass storms (+3 turns).
- Sand Rush and Sand Veil work in the glass-grit. Rock Polish also +1 Speed (it polishes on the obsidian); Smokescreen drops accuracy one stage more.
- Steam Engine +1 Speed on entry and every turn. Magma Armor +1 Def on entry. Hail melts in the steam.
- 3 big fire moves (Eruption, Lava Plume, Magma Storm, Blast Burn...) re-melt it -> Volcanic Field. 3 floods (even ones that miss) or heavy rain fill the caldera -> Water Surface.
- Elemental Seed: +1 Speed, +1 evasion (a cloak of steam), but -1 accuracy (it can't see out either).

**Changes:**
- ERUPTION, LAVAPLUME, MAGMASTORM, FIREPLEDGE, INFERNO +4 more x3 → **Volcanic Field**
- SURF, MUDDYWATER, HYDROPUMP, WATERSPOUT, SPARKLINGARIA +3 more x3 → **Water Surface**
- weather HeavyRain → **Water Surface**

**Seed (ELEMENTALSEED):** SPEED +1, EVASION +1, ACCURACY -1.

## Inverse Field (`:INVERSE`)

*Magical field. Backdrop `field_inverse`. Nature Power: TRIATTACK. Natural type: GHOST.*

> The world turns inside out... Type matchups are reversed!

The Reverse World: the type chart is inverted, reflections strike back harder, and creatures of mind and shadow move freely.

- Inverse type chart: immunities and resistances become weaknesses (x2); weaknesses become resistances (x0.5). Airborne Pokemon still dodge Ground moves.
- Ghost, Psychic and Dark x1.2. Shadow Force, Mirror Shot x1.5; Phantom Force, Foul Play x1.3; Psyshock x1.2.
- Reflections strike back harder: Counter, Mirror Coat, Metal Burst and Comeuppance deal x1.25. Mirror Shot always lowers accuracy.
- Psychic attacks may turn the target's thoughts inside out (10% confusion). Confuse Ray, Hypnosis, Dark Void x1.2 accuracy.
- Contrary Pokemon feel at home (+1 Speed on entry). Magic Bounce and Mirror Armor +1 Sp. Def / Def on entry.
- Trick Room, Magic Room and Wonder Room last 3 turns longer; Psychic Terrain 3 turns longer. Topsy-Turvy also gives +1 Speed.
- Topsy-Turvy rights the world -> the field it came from (or the Mindscape).
- Magical Seed: +1 Attack, +1 Sp. Atk, but -2 Speed (perfect under Trick Room).

**Changes:**
- TOPSYTURVY → returns to the previous field (else Mindscape)

**Seed (MAGICALSEED):** SPEED -2, ATTACK +1, SPECIAL_ATTACK +1.

## The Bleed (`:BLEED`)

*Magical field. Backdrop `field_bleed`. Nature Power: TRIATTACK. Natural type: PSYCHIC.*

> Reality frays at the edges... The Bleed is spreading!

Every 3 rounds it borrows another field's effects. Raw Imprint energy rewards coverage, shapeshifters and type-shifting moves.

- Every 3 rounds (and at once) it borrows the full effects of another field at random. Borrowed fields never transform the Bleed and their seeds don't react.
- Attacks that don't match the user's type x1.2 (raw Imprint energy rewards coverage).
- Type-shifting moves drink the raw Imprints: Judgment, Multi-Attack, Techno Blast, Revelation Dance, Weather Ball, Terrain Pulse, Hidden Power x1.3.
- Protean, Libero and Color Change Pokemon adapt fast (+1 Speed on entry). Mimicry takes the Bleed's natural type (Psychic).
- End of turn: each Pokemon has a 20% chance to have its power warped - one stat +1, another -1.
- Magical Seed: a random stat +2. Synthetic Seed: +1 Defense and +1 Sp. Def (insulated against the warp).

**Seed (MAGICALSEED):** special effect.

**Seed (SYNTHETICSEED):** DEFENSE +1, SPECIAL_DEFENSE +1.

## Colosseum (`:COLOSSEUM`)

*Synthetic field. Backdrop `field_colosseum`. Nature Power: BRICKBREAK. Natural type: FIGHTING.*

> The crowd roars as the fighters enter the pit!

The crowd decides: punches, kicks and throws land harder, knockouts are rewarded, underdogs are cheered and mind games booed. No hiding, no running.

- Fighting x1.2 (x1.5 in a Frenzy). Punching moves and kicks x1.2 (x1.3 in a Frenzy); throws into the cage (Circle Throw, Storm Throw, Vital Throw, Dragon Tail, Submission, Seismic Toss) x1.5.
- Focus Punch x1.5; Revenge, Payback, Retaliate, Avalanche, Lash Out, Reversal x1.3; Beat Up, Fell Stinger, Pay Day x2 (the crowd throws coins).
- The crowd: knocking out a foe gives +1 Attack (physical finisher) or Sp. Atk (special). An underdog at 1/3 HP or less deals x1.2 (x1.3 in a Frenzy). Special Psychic mind games are booed (x0.8).
- Inner Focus and Steadfast: +1 critical-hit stage. Focus Blast x1.2 accuracy. Focus Energy also +1 Attack; No Retreat also +1 Speed; Sand Attack drops accuracy one stage more.
- No Guard and Justified +1 Attack, Battle Armor and Shell Armor +1 Defense on entry.
- Double Team and Minimize fail (nowhere to hide); Roar and Whirlwind fail (no one leaves the pit).
- Frenzy (stage 2): after 2 knockouts. Every attack +1 critical-hit stage. 2 stalling moves (Protect, Recover, Rest, Substitute...) calm the crowd again.
- 3 quakes bring the old mine shaft down -> Cave.
- Synthetic Seed: +1 Attack and Focus Energy, but the crowd's roar Taunts the holder.

**Changes:**
- a field condition (see notes) → stage 2
- EARTHQUAKE, MAGNITUDE, BULLDOZE, FISSURE, HEADLONGRUSH x3 → **Cave**
- *Stage 2* (`field_colosseum`): Frenzy: the crowd is wild - every attack is likelier to crit and the fighters hit harder.
  - PROTECT, DETECT, REST, RECOVER, SLACKOFF +3 more x2 → stage 1
  - EARTHQUAKE, MAGNITUDE, BULLDOZE, FISSURE, HEADLONGRUSH x3 → **Cave**

**Seed (SYNTHETICSEED):** ATTACK +1; effects: focus_energy, taunt.

## Flower Garden (`:FLOWER_GARDEN`)

*Telluric field. Backdrop `field_flower_garden`. Nature Power: MAGICALLEAF. Natural type: GRASS.*

> Tiny buds dot the garden beds.

Grows in 5 stages from tending, sun, rain and Grass attacks; Grass, Bug and (later) Fire grow stronger. Fire, blades, frost and acid cut it back.

- 5 growth stages; the gym's starting stage depends on the puzzle.
- Grows +1: Growth, Rototiller, Flower Shield, Ingrain, Water Sport, Aromatherapy, Floral Healing, Life Dew, Leech Seed, the Pledges (they count even if they fail); sun or rain starting; Grassy Terrain starting; every 2 Grass attacks; a Flower Veil or Flower Gift Pokemon entering.
- Cut back -1: Fire attacks (stages 1-4), non-Grass blades (Slash, X-Scissor, Air Slash...), hail. Acid (Acid Spray, Sludge Wave, Corrosive Gas) burns it back to stage 1.
- Grass x1.1 / 1.2 / 1.3 / 1.5 / 2.0. Bug - / 1.1 / 1.2 / 1.3 / 1.5. Fire - / - / 1.1 / 1.3 / 1.5. Petal moves - / 1.2 / 1.3 / 1.5 / 1.5. Cut x1.5 at every stage.
- Stage 3+: Overgrow, Swarm and Grass Pelt always active; Sweet Scent also lowers Def and Sp. Def; Growth and Rototiller give +1 Atk and Sp. Atk more; powder moves x1.2 accuracy; grounded Grass types drink 1/16 HP a turn.
- Stage 4+: Chlorophyll and Flower Gift active; Bug types feast on nectar (1/16 HP).
- Stage 5: the overgrowth shields Grass types (their weaknesses become neutral) - but 2 Fire attacks set it ablaze -> Wildfire.
- Grassy Terrain lasts 3 turns longer at every stage.
- Telluric Seed: +1 Sp. Def and Ingrain, and the garden grows one stage.

**Changes:**
- GROWTH, ROTOTILLER, FLOWERSHIELD, INGRAIN, WATERSPORT +6 more → stage +1
- weather Sun/HarshSun/Rain/HeavyRain → stage +1
- terrain Grassy → stage +1
- GRASS-type moves x2 → stage +1
- FIRE-type moves → stage -1
- CUT, FURYCUTTER, SLASH, NIGHTSLASH, XSCISSOR +13 more → stage -1
- weather Hail → stage -1
- ACIDSPRAY, SLUDGEWAVE, CORROSIVEGAS, ACID → stage 1
- *Stage 2* (`field_flower_garden_2`): 
  - GROWTH, ROTOTILLER, FLOWERSHIELD, INGRAIN, WATERSPORT +6 more → stage +1
  - weather Sun/HarshSun/Rain/HeavyRain → stage +1
  - terrain Grassy → stage +1
  - GRASS-type moves x2 → stage +1
  - FIRE-type moves → stage -1
  - CUT, FURYCUTTER, SLASH, NIGHTSLASH, XSCISSOR +13 more → stage -1
  - weather Hail → stage -1
  - ACIDSPRAY, SLUDGEWAVE, CORROSIVEGAS, ACID → stage 1
- *Stage 3* (`field_flower_garden_3`): 
  - GROWTH, ROTOTILLER, FLOWERSHIELD, INGRAIN, WATERSPORT +6 more → stage +1
  - weather Sun/HarshSun/Rain/HeavyRain → stage +1
  - terrain Grassy → stage +1
  - GRASS-type moves x2 → stage +1
  - FIRE-type moves → stage -1
  - CUT, FURYCUTTER, SLASH, NIGHTSLASH, XSCISSOR +13 more → stage -1
  - weather Hail → stage -1
  - ACIDSPRAY, SLUDGEWAVE, CORROSIVEGAS, ACID → stage 1
- *Stage 4* (`field_flower_garden_4`): 
  - GROWTH, ROTOTILLER, FLOWERSHIELD, INGRAIN, WATERSPORT +6 more → stage +1
  - weather Sun/HarshSun/Rain/HeavyRain → stage +1
  - terrain Grassy → stage +1
  - GRASS-type moves x2 → stage +1
  - FIRE-type moves → stage -1
  - CUT, FURYCUTTER, SLASH, NIGHTSLASH, XSCISSOR +13 more → stage -1
  - weather Hail → stage -1
  - ACIDSPRAY, SLUDGEWAVE, CORROSIVEGAS, ACID → stage 1
- *Stage 5* (`field_flower_garden_5`): 
  - FIRE-type moves x2 → **Wildfire**
  - CUT, FURYCUTTER, SLASH, NIGHTSLASH, XSCISSOR +13 more → stage -1
  - weather Hail → stage -1
  - ACIDSPRAY, SLUDGEWAVE, CORROSIVEGAS, ACID → stage 1

**Seed (TELLURICSEED):** SPECIAL_DEFENSE +1; effects: ingrain; special effect.

## Frozen Lake (`:FROZEN_LAKE`)

*Elemental field. Backdrop `field_frozen_lake`. Nature Power: ICEBEAM. Natural type: ICE.*

> The battle is taking place on a frozen lake!

Skaters glide and build speed, boulders freeze, quakes splinter the ice into spikes. Fire, quakes and heavy blows crack it; ice attacks refreeze it; sunlight melts it.

- Ice x1.5. Rock moves freeze into ice boulders (also Ice).
- Skating: Rapid Spin, Rollout, Ice Ball x1.5; Triple Axel, Ice Spinner, Spin Out, Aqua Step, Chilling Water x1.3.
- Sliding: grounded users of priority strikes, Ice Shard, Rollout, Ice Ball, Steamroller, Spin Out, Ice Spinner, Lunge or Defense Curl gain +1 Speed.
- Icy Wind and Glaciate drop Speed one stage more. Slush Rush, Snow Cloak and Ice Body work without hail; Ice Scales and Thick Fat +1 Def on entry.
- Quakes splinter the ice: Earthquake, Magnitude, Bulldoze, Fissure and Stomping Tantrum lay a layer of Spikes on both sides.
- Dig fails (the ice is far too thick). Hail lasts 3 turns longer; Aurora Veil works without hail. Grassy Terrain can't take root.
- Cracking: 3 hits from any mix of damaging Fire moves, quakes and heavy blows (High Horsepower, Heavy Slam, Body Press, Headlong Rush, Heat Crash) -> Water Surface. Each damaging Ice move refreezes one crack. Sunlight melts it at once.
- Elemental Seed: +2 Speed - but the holder skates straight across the jagged ice (1/8 HP).

**Changes:**
- a field-specific move condition (see notes) x3 → **Water Surface**
- ICE-type moves → rewinds progress
- weather Sun/HarshSun → **Water Surface**

**Seed (ELEMENTALSEED):** SPEED +2.

## Stormfront (`:STORMFRONT`)

*Elemental field. Backdrop `field_stormfront`. Nature Power: HURRICANE. Natural type: FLYING.*

> Gale-force winds howl across the airship deck!

Fliers ride the gale, wind and Electric moves surge, Tailwind lingers and hazards blow off the deck. In rain, lightning strikes the highest flier - or an Electric Pokemon channels it.

- Electric x1.3, Flying x1.2. Wind moves (Gust, Twister, Hurricane, Air Cutter, Icy Wind, Heat Wave, Silver Wind, the four Storm moves...) x1.2.
- Smack Down x2 and Thousand Arrows x1.5 (slammed onto the deck); Fly, Bounce, Sky Drop, Sky Attack, Dragon Ascent x1.3.
- Hurricane, Thunder and the Storm moves never miss.
- Spikes, Toxic Spikes and Sticky Web blow off the deck (they fail). Tailwind lasts 2 turns longer.
- On entry: Wind Rider +1 Attack, Wind Power charged, Big Pecks +1 Defense, Levitate +1 Speed.
- Lightning (rain only): each turn every airborne Pokemon may be struck (15%, 1/8 HP, Electric-scaled). Airborne Electric types channel it instead (+1 Sp. Atk); Lightning Rod (+1 Sp. Atk), Motor Drive (+1 Speed) and Volt Absorb (heals 1/8) draw the bolts.
- The storm swallows the sun: Sun can't start. Electric Terrain lasts 3 turns longer.
- 2 Sunny Days (they count even though the sun can't break through) tear the storm open -> Rainbow.
- Elemental Seed: +1 Speed and Charge.

**Changes:**
- SUNNYDAY x2 → **Rainbow**

**Seed (ELEMENTALSEED):** SPEED +1; effects: charge.

## Mindscape (`:MINDSCAPE`)

*Magical field. Backdrop `field_mindscape`. Nature Power: PSYCHIC. Natural type: PSYCHIC.*

> The world dissolves into a sea of drifting thoughts...

Thought is made real: Psychic surges, nightmares take shape, rooms fold longer, dreams are shallow. Dark moves curdle it into a Nightmare; noise or Topsy-Turvy shatter it.

- Dream (stage 1): Psychic x1.5; Dark and Ghost x1.2 (nightmares lurk). Damaging sound moves x1.2.
- Dream Eater, Mirror Shot, Psybeam x1.5; Expanding Force, Mystical Fire, Extrasensory, Future Sight, Esper Wing, Lumina Crash x1.3; Psyshock, Stored Power x1.2.
- A disciplined mind resists: Psychic moves deal x0.75 to Inner Focus, Own Tempo and Oblivious Pokemon.
- Dream-sleep is shallow: sleepers wake twice as fast. Meditate and Kinesis work one stage better.
- Forewarn and Anticipation +1 Sp. Def on entry; Telepathy +1 Speed. Trick Room, Magic Room, Wonder Room +2 turns; Psychic Terrain +3.
- Dark Void, Nightmare or Spite (or 3 Dark attacks) curdle the dream -> Nightmare (stage 2).
- Nightmare: Dark and Ghost x1.5, Psychic x1.2, Fairy x0.8. Hex x1.5, Dream Eater x2; Hypnosis and Dark Void more accurate; Dark and Ghost types feed on the dread (1/16 HP a turn); sleep is no longer shallow. 2 soothing moves (Calm Mind, Heal Bell, Aromatherapy, Sweet Kiss, Wish...) calm it back to a dream.
- Topsy-Turvy, or 3 damaging sound moves, crack the dream -> Inverse Field.
- Magical Seed: +2 Sp. Atk, but the flood of thoughts confuses the holder.

**Changes:**
- DARKVOID, NIGHTMARE, SPITE → stage 2
- DARK-type moves x3 → stage 2
- TOPSYTURVY → **Inverse Field**
- Sound moves x3 → **Inverse Field**
- *Stage 2* (`field_mindscape_nightmare`): Nightmare: shadows feed on dread and grow strong; light falters. Soothing moves calm it back into a dream.
  - CALMMIND, AROMATHERAPY, HEALBELL, SWEETKISS, LUNARBLESSING +2 more x2 → stage 1
  - TOPSYTURVY → **Inverse Field**
  - Sound moves x3 → **Inverse Field**

**Seed (MAGICALSEED):** SPECIAL_ATTACK +2.

## Crystal Cavern (`:CRYSTAL_CAVERN`)

*Magical field. Backdrop `field_crystal_cavern`. Nature Power: POWERGEM. Natural type: ROCK.*

> Prismatic crystals glitter all around!

The crystals' glow cycles Fire > Water > Grass > Psychic each round: Rock moves (and Stealth Rock) take that type, and that type shines. Light refracts, barriers mirror. Darkness or sand blots out the light.

- Rock x1.3, Dragon x1.2 (old wyrms hoarded these crystals). Damaging sound moves x1.2 (the crystals ring).
- The glow cycles each round: red (Fire) > blue (Water) > green (Grass) > amethyst (Psychic), starting at random. Rock moves also hit as the glow's type; moves OF the glow's type are x1.2.
- Stealth Rock flares with the glow: an extra 1/16 hit of that type on entry.
- Light moves refract into dazzling beams (x1.5): Power Gem, Diamond Storm, Flash Cannon, Dazzling Gleam, Aurora Beam, Luster Purge, Mist Ball, Moongeist Beam, Prismatic Laser, Meteor Beam, Lumina Crash, Ancient Power...
- Ancient Power's stat boost is twice as likely. Flash drops accuracy one stage more; Rock Polish also +1 Sp. Atk.
- Reflect, Light Screen and Aurora Veil last 2 turns longer; Aurora Veil works without hail. Prism Armor Pokemon take x0.75 from every hit.
- Dark Pulse, Night Daze, Dark Void, Fiery Wrath or a sandstorm -> Dark Crystal Cavern. An explosion, or 3 quakes -> Cave (the crystals shatter).
- Magical Seed: +1 Sp. Atk and a Light Screen for its side.

**Changes:**
- DARKPULSE, NIGHTDAZE, DARKVOID, FIERYWRATH → **Dark Crystal Cavern**
- weather Sandstorm → **Dark Crystal Cavern**
- EXPLOSION, SELFDESTRUCT, MISTYEXPLOSION → **Cave**
- EARTHQUAKE, MAGNITUDE, BULLDOZE, FISSURE x3 → **Cave**

**Seed (MAGICALSEED):** SPECIAL_ATTACK +1; effects: light_screen.

## Dark Crystal Cavern (`:DARK_CRYSTAL`)

*Magical field. Backdrop `field_dark_crystal`. Nature Power: DARKPULSE. Natural type: DARK.*

> Darkness fills the cavern. The crystals have gone black...

Creatures of the dark hunt by feel and hide in it; obsidian edges cut. Most Pokemon struggle to aim. Light pierces the dark and can rekindle the crystals.

- Dark x1.5, Ghost x1.3, Rock x1.2 (obsidian). Dark and Ghost Pokemon melt into the dark: x0.83 damage taken.
- Shadow Sneak, Sucker Punch, Shadow Claw, Night Slash x1.5 (struck from the dark); Stone Edge, Stone Axe x1.2.
- Light moves (Power Gem, Flash Cannon, Dazzling Gleam, Luster Purge, Meteor Beam...) x1.2 - they pierce the dark.
- Damaging moves from Pokemon that aren't Dark, Ghost or Rock are x0.9 accurate (Keen Eye, Illuminate, Mind's Eye, No Guard see fine). Illuminate +1 accuracy on entry.
- Dark and Ghost contact moves: +1 critical-hit stage. Flash drops accuracy one stage more. Solar Beam and Solar Blade fail (no light to gather).
- Prism Armor Pokemon take x0.75 from every hit.
- 2 light moves (Flash, Tail Glow and Light of Ruin count too), or sunlight -> Crystal Cavern. An explosion or 3 quakes -> Cave.
- Magical Seed: +1 Attack, +1 Sp. Atk.

**Changes:**
- AURORABEAM, SIGNALBEAM, FLASHCANNON, LUSTERPURGE, MISTBALL +15 more x2 → **Crystal Cavern**
- weather Sun/HarshSun → **Crystal Cavern**
- EXPLOSION, SELFDESTRUCT, MISTYEXPLOSION → **Cave**
- EARTHQUAKE, MAGNITUDE, BULLDOZE, FISSURE x3 → **Cave**

**Seed (MAGICALSEED):** ATTACK +1, SPECIAL_ATTACK +1.

## Hollow Cathedral (`:HOLLOW_CATHEDRAL`)

*Magical field. Backdrop `field_hollow_cathedral`. Nature Power: SHADOWBALL. Natural type: GHOST.*

> Candles gutter in the ruined nave... Restless spirits stir in the gloom.

Ghosts gather in the gloom and the veil is thin (Ghost and Normal hit each other). Hymns echo, candles burn with ghostfire. Holy light consecrates it.

- Haunted (stage 1): Ghost x1.5; Ghost moves' own added effects x1.5 as likely. Damaging sound moves x1.3 (the nave echoes).
- The veil is thin: Ghost moves hit Normal types and Normal moves hit Ghost types (neutral).
- Ghostfire: Fire moves also hit as Ghost. Will-O-Wisp never misses.
- Astonish x2; Ominous Wind x1.5 (its boost twice as likely); Poltergeist, Spirit Shackle, Mystical Fire, Infernal Parade and the ossuary's bone moves x1.3. Night Shade x1.5. Lick always paralyzes.
- The spirits crowd around sleepers: Ghost attacks against a sleeping target x1.3. Scary Face also lowers Attack.
- Cursed Body, Perish Body, Wandering Spirit, Mummy +1 Sp. Def on entry; Rattled Pokemon jump at shadows (+1 Speed).
- 3 holy acts (Sacred Fire, Sacred Sword, Judgment, Dazzling Gleam, Light of Ruin, Purify, Heal Bell; they count even if they fail) -> Consecrated (stage 2).
- Consecrated: Ghost and Dark x0.8, Fairy x1.2, holy moves x1.5, hymns (sound) x1.3. Normal moves strike Ghost types super effectively. Curses are lifted each turn; Justified +1 Attack on entry. 2 Ghost rites (Curse, Spite, Grudge, Nightmare, Last Respects, Destiny Bond) by a Ghost type bring the spirits back.
- Topsy-Turvy, or 2 dimension-rending moves (Boomburst, Shadow Force, Hyperspace Fury/Hole), shatter the glass -> Inverse Field.
- Magical Seed: +1 Sp. Def, and a wandering spirit makes the holder part Ghost type.

**Changes:**
- SACREDFIRE, SACREDSWORD, JUDGMENT, DAZZLINGGLEAM, LIGHTOFRUIN +2 more x3 → stage 2
- TOPSYTURVY → **Inverse Field**
- BOOMBURST, SHADOWFORCE, HYPERSPACEFURY, HYPERSPACEHOLE x2 → **Inverse Field**
- *Stage 2* (`field_hollow_cathedral_consecrated`): Consecrated: Ghost and Dark weakened, Fairy, hymns and holy moves strengthened, Normal moves smite Ghosts. Ghost rites can undo it.
  - CURSE, SPITE, GRUDGE, NIGHTMARE, LASTRESPECTS +1 more x2 → stage 1
  - TOPSYTURVY → **Inverse Field**
  - BOOMBURST, SHADOWFORCE, HYPERSPACEFURY, HYPERSPACEHOLE x2 → **Inverse Field**

**Seed (MAGICALSEED):** SPECIAL_DEFENSE +1; adds GHOST type.

## Factory (`:FACTORY`)

*Synthetic field. Backdrop `field_factory`. Nature Power: GEARGRIND. Natural type: STEEL.*

> Gears grind and molten steel pours... The foundry roars to life!

Steel Pokemon mesh with the machinery: gears, hammers and rollers ring out, metal-tuning moves work better, the crucibles' heat softens rival plating. Explosions or quakes wreck it.

- Steel x1.5, Electric x1.2, Fire x1.2 (the crucibles). Steelworker and Steely Spirit users' Steel moves x1.2 more.
- Gear Grind x2; Magnet Bomb, Steel Roller, Steamroller, Gyro Ball, Techno Blast x1.5; Double Iron Bash, Flash Cannon, Steam Eruption, Spin Out, Explosion, Self-Destruct, Misty Explosion x1.3; hammers (Hammer Arm, Ice/Wood/Crab/Dragon/Gigaton Hammer) x1.3.
- Damaging Fire moves may soften a Steel target's plating (30%, Defense -1). Metal Sound and Screech never miss.
- Shift Gear also +1 Defense; Autotomize, Iron Defense and Metal Sound work one stage better; Magnet Rise +1 Speed and lasts 3 turns longer.
- On entry: Light Metal +1 Speed, Heavy Metal +1 Defense, Download +1 Speed (it syncs with the line).
- Nothing can be frozen near the crucibles. Indoors: Rain, Sandstorm and Hail can't start. Sun +2 turns, Electric Terrain +2.
- An explosion (Explosion, Self-Destruct, Misty Explosion, Mind Blown) wrecks it at once; 3 quakes bring the catwalks down. Either leaves a Scrapyard.
- Synthetic Seed: +1 Attack and +1 Speed.

**Changes:**
- EXPLOSION, SELFDESTRUCT, MISTYEXPLOSION, MINDBLOWN → **Scrapyard**
- EARTHQUAKE, MAGNITUDE, BULLDOZE, FISSURE, HEADLONGRUSH +2 more x3 → **Scrapyard**

**Seed (SYNTHETICSEED):** ATTACK +1, SPEED +1.

## Scrapyard (`:SCRAPYARD`)

*Synthetic field. Backdrop `field_scrapyard`. Nature Power: GUNKSHOT. Natural type: STEEL.*

> Jagged scrap and leaking chemicals litter the ground...

Scavengers thrive: junk is ammunition, oil burns, cables spark and rust leaves Steel weak to Water. Recharge the machines to restart the line.

- Steel x1.2, Poison x1.2 (leaking chemicals). Fling x2; Smog x1.5; Gunk Shot, Clear Smog, Magnet Bomb, Metal Claw, Explosion, Self-Destruct x1.3.
- Rust: Water moves are super effective against Steel types.
- Oil slicks: damaging Fire moves may splash burning oil (20% burn). Live cables: Electric attacks may paralyze Steel targets (20%).
- Stealth Rock is mixed with scrap: an extra 1/16 Steel-scaled hit on entry (Heavy-Duty Boots protect). Smokescreen drops accuracy one stage more.
- Scavengers: Pickup +1 Speed, Scrappy +1 Attack, Magnet Pull +1 Defense (it pulls scrap armor onto itself) on entry.
- Shift Gear and Gear Up fail (the gears have rusted). Gunk Shot x1.25 accuracy.
- 3 charging moves (Charge, Discharge, Wild Charge, Magnet Rise, Electric Terrain...; they count even if they fail) restart the machines -> Factory. 2 acid moves (Acid Spray, Sludge Wave, Corrosive Gas, Acid Armor...) leach the chemicals out -> Wasteland.
- Synthetic Seed: +1 Defense, +1 Sp. Def, but the bolted-on scrap is heavy (-1 Speed).

**Changes:**
- CHARGE, DISCHARGE, PARABOLICCHARGE, WILDCHARGE, CHARGEBEAM +6 more x3 → **Factory**
- ACIDSPRAY, SLUDGEWAVE, CORROSIVEGAS, ACIDARMOR, ACID x2 → **Wasteland**

**Seed (SYNTHETICSEED):** DEFENSE +1, SPECIAL_DEFENSE +1, SPEED -1.

## New Moon (`:NEW_MOON`)

*Magical field. Backdrop `field_new_moon`. Nature Power: DARKPULSE. Natural type: DARK.*

> The moon has gone dark over Underveil... Something moves in the shadows.

A darkness ladder. Creatures of the dark hide and strike from it; stars and true light pierce it. Dark moves deepen it into an Abyss; enough light relights Nadir's lamps.

- New Moon (stage 1): Dark x1.5; shadow moves (Dark Pulse, Night Slash, Shadow Ball, Shadow Claw, Sucker Punch, Phantom Force...) x1.2.
- Moves from Pokemon that aren't Dark or Ghost are x0.9 accurate (Keen Eye, Illuminate, Mind's Eye, Compound Eyes, No Guard see fine). Night Daze never misses. Illuminate +1 accuracy on entry.
- Stars and light pierce the dark: Swift x1.5; Meteor Mash, Meteor Beam x1.3; light moves (Dazzling Gleam, Flash Cannon, Photon Geyser...) x1.3. Flash blinds one stage more; Cosmic Power also +1 Sp. Atk.
- Feint Attack and Thief x1.5. Moonlight fails and Moonblast loses its glow (x0.75). The sun can't rise here.
- Dark Void, or 3 deepening moves (Dark Pulse, Night Daze, Moongeist Beam, Ominous Wind, Night Shade...) -> Abyss (stage 2).
- Abyss: Dark x1.5, Ghost x1.3, shadow moves x1.4; light moves x0.75; accuracy x0.8 for those who can't see; Solar Beam and Solar Blade fail. 2 light moves push it back to stage 1.
- 3 light moves on the New Moon relight Nadir's gaslamps -> Lamplight (stage 3): Dark x1.2, Fire and Electric x1.2 (the lamps), light moves x1.3, thieves x1.5, normal accuracy; Pickpocket and Frisk +1 Speed on entry. 3 Dark attacks snuff the lamps (stage 1).
- Magical Seed: +1 accuracy and Focus Energy - and it draws the shadows in (New Moon -> Abyss; Lamplight -> New Moon).

**Changes:**
- DARKVOID → stage 2
- DARKPULSE, NIGHTDAZE, MOONGEISTBEAM, OMINOUSWIND, ASTRALBARRAGE +1 more x3 → stage 2
- FLASH, TAILGLOW, DAZZLINGGLEAM, LIGHTOFRUIN, PHOTONGEYSER +7 more x3 → stage 3
- *Stage 2* (`field_new_moon_abyss`): Abyss: the darkness is total. Shadows strike hard, light barely carries, the blind can hardly aim.
  - FLASH, TAILGLOW, DAZZLINGGLEAM, LIGHTOFRUIN, PHOTONGEYSER +7 more x2 → stage 1
- *Stage 3* (`field_new_moon_lamplight`): Lamplight: the undercity's lamps are lit. Lamplighters' fire and current flare, thieves work the shadows between the lamps.
  - DARK-type moves x3 → stage 1

**Seed (MAGICALSEED):** ACCURACY +1; effects: focus_energy; special effect.

## Fairy Tale (`:FAIRY_TALE`)

*Magical field. Backdrop `field_fairy_tale`. Nature Power: SECRETSWORD. Natural type: FAIRY.*

> Once upon a time, in a castle deep in the forest... the story begins!

Fairies cast spells, knights draw gleaming blades and dragons breathe dragonfire. Armour and magic shine; true love's kiss wakes any sleeper. Rouse the dragon to change the story.

- Fairy x1.5, Dragon x1.5, Steel x1.3. Marvel Scale is always active.
- Knights: blade moves x1.3, and x1.2 more against Dragons; Steel moves strike Dragons like a dragonslayer (x1.5). Cut and Slash become gleaming Steel blades.
- Dragonfire: Fire moves also hit as Dragon.
- Spells: Draining Kiss x2; Magical Leaf, Fairy Wind, Mystical Fire, Ancient Power, Relic Song, Sparkling Aria, Fleur Cannon x1.5; Moongeist Beam, Behemoth Bash x1.3.
- True love's kiss: Draining Kiss and Sweet Kiss wake a sleeping target. Sweet Kiss never misses.
- King's Shield +1 Def, Crafty Shield +1 Sp. Def, Flower Shield +1 Def and Sp. Def; Noble Roar lowers Atk and Sp. Atk one stage more.
- On entry: Battle Armor, Shell Armor +1 Def; Magic Guard, Magic Bounce, Mirror Armor, Pastel Veil +1 Sp. Def; Magician +1 Sp. Atk.
- Sleepers dream of happily ever after (1/16 HP a turn). Misty Terrain lasts 3 turns longer.
- 3 Dragon attacks rouse the dragon beneath the castle -> Dragon's Den.
- Magical Seed: +1 Sp. Atk and +1 Sp. Def (a fairy godmother's blessing).

**Changes:**
- DRAGON-type moves x3 → **Dragon's Den**

**Seed (MAGICALSEED):** SPECIAL_ATTACK +1, SPECIAL_DEFENSE +1.

## Dragon's Den (`:DRAGONS_DEN`)

*Elemental field. Backdrop `field_dragons_den`. Nature Power: DRAGONPULSE. Natural type: DRAGON.*

> Magma glows beneath a dragon's hoard... Ancient wyrms watch from the stone.

Dragons are armoured by their lair, fire runs in the floor and the hoard pays out. Dragon attacks awaken the den; Water and Ice cool it; Fairy magic tames it.

- Dragon x1.5, Fire x1.3. Water and Ice x0.7 (the lair's heat). Dragon types are armoured by their lair (x0.83 damage taken).
- Pay Day x2; Make It Rain, Dragon Breath x1.5 (Dragon Breath also hits as Fire); Smack Down and Thousand Arrows x2 (onto the magma, also Fire); bone moves, Lava Plume, Magma Storm, Earth Power, Power Gem, Diamond Storm x1.3.
- Dragon Rage deals 140 HP (200 in Wyrmfire). Dragon Rush x1.25 accuracy.
- Magma Armor: immune to Fire, +1 Def and Sp. Def on entry. Multiscale: Dragon weaknesses become neutral. Flash Fire starts lit; Dragon's Maw +1 Attack.
- Dragon Dance also +1 Speed; Noble Roar lowers Atk and Sp. Atk one stage more.
- The hoard protects its own: a Pokemon holding an Amulet Coin can't be given a status condition. Nothing can be frozen.
- Stealth Rock picks up embers: an extra 1/16 Fire-scaled hit on entry.
- Hail can't form; Sun +2 turns. Grassy Terrain burns away.
- 4 Dragon attacks awaken the den -> Wyrmfire (stage 2): Dragon x2, Fire x1.5, Water and Ice x0.5; Dragon attacks may burn (20%); Dragons bask in the wyrmfire (1/16 HP a turn).
- 3 Water or Ice attacks -> Cave. 3 Fairy attacks tame the dragon -> Fairy Tale.
- Elemental Seed: +1 Attack, +1 Speed and Flash Fire.

**Changes:**
- WATER/ICE-type moves x3 → **Cave**
- FAIRY-type moves x3 → **Fairy Tale**
- DRAGON-type moves x4 → stage 2
- *Stage 2* (`field_dragons_den_wyrmfire`): Awakened: Dragon x2, Fire x1.5, Ice halved. Dragon attacks spit wyrmfire; dragons bask in it.
  - WATER/ICE-type moves x3 → **Cave**
  - FAIRY-type moves x3 → **Fairy Tale**

**Seed (ELEMENTALSEED):** ATTACK +1, SPEED +1; effects: flash_fire.

## Cave (`:CAVE`)

*Telluric field. Backdrop `field_cave`. Nature Power: ROCKTOMB. Natural type: ROCK.*

> The cave walls loom close... every sound echoes.

Rock Pokemon own the walls and every sound echoes; the low ceiling grounds fliers. Quakes crack the ceiling - twice, and it caves in. Gems, magma or dragons can open it into somewhere else.

- Rock x1.5. Damaging sound moves x1.5 (they echo). Rock Climb, Rock Tomb, Drill Run, Hyper Drill, Drum Beating, Dig x1.5.
- The ceiling is low: Flying moves that don't make contact x0.5; Ground moves hit Flying types; Sky Drop fails.
- Sound-based status moves (Sing, Supersonic, Screech, Metal Sound...) x1.3 accuracy. Flash drops accuracy one stage more; Howl also +1 Attack.
- Stealth Rock hits twice as hard (Heavy-Duty Boots protect).
- Underground: Sun, Rain and Hail can't start. Sandstorm lasts 3 turns longer.
- Cave-in: a quake (Earthquake, Magnitude, Bulldoze, Fissure, Land's Wrath, Precipice Blades, Thousand Waves, Headlong Rush) cracks the ceiling. The next quake brings it down: everyone takes 1/8 HP of Rock-type damage (Rock Head, Bulletproof, Overcoat are safe), and the dust settles.
- 2 Power Gems / Diamond Storms -> Crystal Cavern. 2 of Eruption, Lava Plume, Magma Storm, Fire Pledge, Blast Burn -> Volcanic Field. Draco Meteor, or 2 Dragon Pulses -> Dragon's Den.
- Telluric Seed: +1 Defense and scatters Stealth Rock on the opposing side.

**Changes:**
- EARTHQUAKE, MAGNITUDE, BULLDOZE, FISSURE, LANDSWRATH +3 more → stage 2
- POWERGEM, DIAMONDSTORM x2 → **Crystal Cavern**
- ERUPTION, LAVAPLUME, MAGMASTORM, FIREPLEDGE, BLASTBURN x2 → **Volcanic Field**
- DRACOMETEOR → **Dragon's Den**
- DRAGONPULSE, DRAGONENERGY, CLANGINGSCALES x2 → **Dragon's Den**
- *Stage 2* (`field_cave`): The ceiling is cracked: the next quake move brings it down on every Pokemon.
  - EARTHQUAKE, MAGNITUDE, BULLDOZE, FISSURE, LANDSWRATH +3 more → stage 1
  - POWERGEM, DIAMONDSTORM x2 → **Crystal Cavern**
  - ERUPTION, LAVAPLUME, MAGMASTORM, FIREPLEDGE, BLASTBURN x2 → **Volcanic Field**
  - DRACOMETEOR → **Dragon's Den**
  - DRAGONPULSE, DRAGONENERGY, CLANGINGSCALES x2 → **Dragon's Den**

**Seed (TELLURICSEED):** DEFENSE +1; effects: stealth_rock.

## Mountain (`:MOUNTAIN`)

*Telluric field. Backdrop `field_mountain`. Nature Power: ROCKSLIDE. Natural type: ROCK.*

> The wind howls across the mountain ridge!

High, rocky and windswept: boulders tumble, fliers ride the ridge winds, throws send foes down the slope and Tailwind lingers. Ice buries it in snow; magma can break through the peak.

- Rock x1.5, Flying x1.2. Wind moves x1.3. Avalanche x1.5; throws (Vital Throw, Circle Throw, Storm Throw) x1.5; Sky Attack, Hyper Voice x1.2. Seismic Toss x1.25.
- Hurricane and the Storm moves x1.2 accuracy; Thunder never misses on the peaks.
- Tailwind lasts 2 turns longer. Wind Rider +1 Attack and Wind Power charged on entry (and when the field appears).
- Sunlight lasts 3 turns longer in the thin air.
- Hail, or 2 big ice moves (Blizzard, Mountain Gale, Sheer Cold, Glaciate) -> Snowy Mountain. 2 of Eruption, Lava Plume, Magma Storm, Fire Pledge -> Volcanic Field.
- Telluric Seed: +1 Speed and a Tailwind for the holder's side.

**Changes:**
- weather Hail → **Snowy Mountain**
- BLIZZARD, MOUNTAINGALE, SHEERCOLD, GLACIATE x2 → **Snowy Mountain**
- ERUPTION, LAVAPLUME, MAGMASTORM, FIREPLEDGE x2 → **Volcanic Field**

**Seed (TELLURICSEED):** SPEED +1; effects: tailwind.

## Snowy Mountain (`:SNOWY_MOUNTAIN`)

*Telluric field. Backdrop `field_snowy_mountain`. Nature Power: AVALANCHE. Natural type: ICE.*

> A blizzard rages over the snowbound peak!

Ice Pokemon ride the blizzard: snow abilities always work, boulders freeze, snowballs grow as they roll, Ice types shrug off blows. Big fire or sunlight melts it back to bare rock.

- Ice x1.5, Rock and Flying x1.2, wind moves x1.3. Fire x0.75 (the cold dulls it).
- Rock moves come down frozen (also Ice).
- Powder Snow x2; Icy Wind, Avalanche, Ice Ball, Rollout and throws (Vital/Circle/Storm Throw) x1.5; Glaciate, Mountain Gale, Bitter Malice x1.3.
- Ice types take less from physical attacks (x0.67). Blizzard and Thunder never miss.
- Slush Rush, Snow Cloak and Ice Body work without hail. Hail lasts 3 turns longer; Aurora Veil works without hail. Tailwind lasts 2 turns longer.
- On entry: Wind Rider +1 Attack, Wind Power charged. The deep snow soothes grounded Pokemon's burns each turn.
- Sun, or 2 big fire moves (Heat Wave, Lava Plume, Blast Burn, Inferno, Overheat, Blue Flare, Fusion Flare...) -> Mountain. 2 of Eruption or Magma Storm -> Volcanic Field.
- Telluric Seed: +1 Defense and Defense Curl (pair it with Ice Ball or Rollout).

**Changes:**
- ERUPTION, MAGMASTORM x2 → **Volcanic Field**
- weather Sun/HarshSun → **Mountain**
- HEATWAVE, LAVAPLUME, FIREPLEDGE, BLASTBURN, INFERNO +7 more x2 → **Mountain**

**Seed (TELLURICSEED):** DEFENSE +1; effects: defense_curl.

## Beach (`:BEACH`)

*Telluric field. Backdrop `field_beach`. Nature Power: MUDDYWATER. Natural type: GROUND.*

> Waves lap at the sandy shore...

Sand and surf: shore-dwellers dig and splash, the calm sea air rewards focus, and the breeze kicks sand into everyone's eyes. A rising tide floods the beach.

- Water x1.2, Ground x1.2. Mud-Slap, Mud Shot, Mud Bomb x2; Muddy Water, Sand Tomb x1.5; Scorching Sands x1.3 (50% burn).
- Tide pools: Crabhammer, Razor Shell, Shell Side Arm, Shell Trap, Brine x1.3. Focus: Aura Sphere, Focus Blast, Zen Headbutt, Stored Power x1.3; Focus Blast x1.1 accuracy.
- Focused minds (Inner Focus, Own Tempo, Pure Power, Steadfast, Sand Veil) ignore every accuracy and evasion stage.
- The sound of the waves: Calm Mind also +1 Sp. Atk, Meditate +1 Attack; Kinesis and Sand Attack drop accuracy one stage more (Sand Attack never misses).
- Sand Rush, Sand Force and Sand Veil work in the beach sand. Water Compaction +1 Def and Sp. Def on entry.
- Sea breeze: wind moves (and Fire Spin, Whirlpool, Leaf Tornado) kick up sand - every other Pokemon loses 1 accuracy.
- Shore Up heals 1/6 HP more. Water Absorb and Dry Skin soak up the spray (1/16); Hydration cures status each turn.
- Hail can't form. Sun and Sandstorm last 2 turns longer.
- Heavy rain, or 3 big surf moves (Surf, Muddy Water, Water Spout, Origin Pulse, Water Pledge, Wave Crash) -> Water Surface (the tide comes in).
- Telluric Seed: +1 Defense and Aqua Ring.

**Changes:**
- weather HeavyRain → **Water Surface**
- SURF, MUDDYWATER, WATERSPOUT, ORIGINPULSE, WATERPLEDGE +1 more x3 → **Water Surface**

**Seed (TELLURICSEED):** DEFENSE +1; effects: aqua_ring.

## Rainbow (`:RAINBOW`)

*Magical field. Backdrop `field_rainbow`. Nature Power: AURORABEAM. Natural type: FAIRY.*

> A brilliant rainbow arcs over the battlefield!

Prismatic light everywhere: added effects are twice as likely, colourful moves blaze, Normal moves surge and darkness falters.

- Every move's own added effect is twice as likely (stacks with Serene Grace).
- Normal x1.5. Dark x0.75 (the light washes it out). Marvel Scale is always active.
- Colours x1.5: Aurora Beam, Signal Beam, Dazzling Gleam, Mist Ball, Luster Purge, Sparkling Aria, Silver Wind, Heart Stamp, Sacred Fire, Tri Attack, Mystical Fire, Judgment, Multi-Attack, Weather Ball, Hidden Power, Relic Song and the Pledges. Prismatic Laser, Photon Geyser, Fleur Cannon x1.3.
- Sonic Boom deals 140 HP. Cosmic Power also +1 Sp. Def. Nightmare fails.
- Sleeping Pokemon have sweet dreams (1/16 HP a turn). Cloud Nine Pokemon float on the clouds (a random stat +1 each turn).
- Misty Terrain lasts 3 turns longer; Aurora Veil works without hail.
- Sandstorm, hail or Defog blot out the rainbow -> the field it replaced (or a Meadow).
- Magical Seed: +1 Sp. Atk, and a wish is made for the holder.

**Changes:**
- weather Sandstorm/Hail → returns to the previous field (else Meadow)
- DEFOG → returns to the previous field (else Meadow)

**Seed (MAGICALSEED):** SPECIAL_ATTACK +1; effects: wish.

## Wasteland (`:WASTELAND`)

*Telluric field. Backdrop `field_wasteland`. Nature Power: GUNKSHOT. Natural type: POISON.*

> Poisoned slag and dead trees stretch to a jaundiced horizon...

Bleed-scarred badlands where grime-dwellers thrive: sludge carries strange afflictions, hazards splinter into Imprint shards, acid rain stings, and tough weeds whip through the slag.

- Poison x1.2 (x1.5 in acid rain). Sludge, Octazooka, Mud Bomb x1.5; Gunk Shot, Belch x1.3; Sludge Bomb, Sludge Wave x1.2; Spit Up x2.
- The slag carries something nasty: Sludge, Sludge Bomb, Sludge Wave, Gunk Shot and Octazooka may inflict a random status (20%).
- Weeds of the waste: Vine Whip and Power Whip x1.5. Explosion-type moves x1.3 (trapped fumes). Quakes x0.5 (the slag soaks them up).
- Toxic Boost is always active. Poison Heal draws 1/16 HP more from the waste each turn while poisoned.
- Synthesis, Morning Sun and Moonlight fail under the jaundiced sky.
- Hazards splinter: Stealth Rock adds an Imprint shard of a random type (1/16, scaled by that type); Toxic Spikes also eat into grounded Pokemon (1/16 Poison-scaled). Heavy-Duty Boots protect.
- Sandstorm lasts 3 turns longer.
- Grassy Terrain -> Flower Garden (life returns). 2 Purify (they count even if they fail) -> Meadow.
- Telluric Seed: +1 Attack and +1 Sp. Atk, but the holder is badly poisoned (great on Poison types and Poison Heal).

**Changes:**
- terrain Grassy → **Flower Garden**
- PURIFY x2 → **Meadow**

**Seed (TELLURICSEED):** ATTACK +1, SPECIAL_ATTACK +1; status: TOXIC.

## Prism Arena (`:PRISM_ARENA`)

*Magical field. Backdrop `field_prism_arena`. Nature Power: JUDGMENT. Natural type: NORMAL.*

> The eighteen Plates blaze in a ring above Crownhaven's arena!

The Festival finale. Every 3 turns the Plates turn and the arena takes on the next gym field, in a fixed order announced a turn ahead.

- Opening: the Plates rest for 3 turns. Then every 3 turns they turn, and the arena takes on a gym field's effects.
- Each turn is announced one turn ahead. Fixed order: Fire, Water, Grass, Electric, Ice, Fighting, Ground, Poison, Flying, Psychic, Bug, Rock, Ghost, Dark, Fairy, Steel, Dragon, Normal.
- Multitype Pokémon take the ascendant Plate's type; Judgment and Nature Power strike with it.
- Super-effective hits on Pokémon of the ascendant type x1.2. Holding the ascendant Plate heals 1/16 HP a turn.
- Tri Attack x1.3, Prismatic Laser x1.2. Borrowed fields never transform the arena.

**Seed (MAGICALSEED):** SPECIAL_ATTACK +1, SPECIAL_DEFENSE +1.

## Wildfire (`:WILDFIRE`)

*Elemental field. Backdrop `field_wildfire`. Nature Power: FLAMETHROWER. Natural type: FIRE.*

> The battlefield is ablaze! Flames leap from tree to tree!

Fire Pokemon draw the blaze into their attacks, winds fan it and every fire attack can spread it around the foes. It burns down to embers unless it's fed.

- Wildfire (stage 1): Fire x1.5; Blaze and Flare Boost always active; Flash Fire starts lit. Ice x0.5; Grass moves x0.5 against grounded targets.
- Damaging wind moves fan the flames (also Fire, x1.2). Smog, Clear Smog x1.5 (also Fire); Smack Down, Thousand Arrows x2 (into the burning undergrowth, also Fire); Flame Charge, Fire Spin x1.5.
- Spreading: a damaging Fire attack may spread the fire around the user's foes (30%: a 3-turn sea of fire on their side).
- Will-O-Wisp never misses; Smokescreen drops accuracy one stage more. Nothing can be frozen.
- Fuel: it burns down to Embers after 4 rounds; each damaging Fire attack feeds it a round (max 5).
- Put out sooner: 2 douses (Surf, Muddy Water, Hydro Pump, Water Spout, Sand Tomb, Water/Mud Sport...), Defog, Whirlwind or Tailwind, rain or a sandstorm -> Embers.
- Embers (stage 2): Fire, Ground, Grass and Ghost x1.2 (coals, ash, pioneer shoots, smoke wraiths); Flare Boost active; wind moves whirl ash (30% accuracy -1); Grass types take root in the fertile ash (1/16 HP a turn); Growth also +1 Sp. Atk.
- Embers: 2 big fire moves or sunlight -> Wildfire again. Rain, Grassy Terrain, or 2 growing moves (Growth, Ingrain, Grass Pledge, Rototiller...) -> Meadow (life returns).
- Elemental Seed: +1 Attack, +1 Sp. Atk and Flash Fire, but the holder is burned.

**Changes:**
- a field condition (see notes) → stage 2
- SURF, MUDDYWATER, HYDROPUMP, WATERSPOUT, WATERPLEDGE +5 more x2 → stage 2
- DEFOG, WHIRLWIND, TAILWIND → stage 2
- weather Rain/HeavyRain/Sandstorm → stage 2
- *Stage 2* (`field_wildfire_embers`): Embers: smouldering coals and fertile ash. Fire still flares, ghosts thicken in the smoke and pioneer plants take root. Fire can re-ignite it; rain and growth bring the land back.
  - ERUPTION, LAVAPLUME, HEATWAVE, FIREBLAST, INFERNO +8 more x2 → stage 1
  - weather Sun/HarshSun → stage 1
  - weather Rain/HeavyRain → **Meadow**
  - terrain Grassy → **Meadow**
  - GROWTH, INGRAIN, GRASSPLEDGE, FLORALHEALING, ROTOTILLER +1 more x2 → **Meadow**

**Seed (ELEMENTALSEED):** ATTACK +1, SPECIAL_ATTACK +1; effects: flash_fire; status: BURN.

## Meadow (`:MEADOW`)

*Telluric field. Backdrop `field_meadow`. Nature Power: ENERGYBALL. Natural type: GRASS.*

> Tall grass ripples in the breeze across the meadow.

Elowen's open countryside: grazers stampede, bugs and birds work the wildflowers, the breeze carries seed and petal, and the tall grass hides whoever lives in it. Fire races through it; tending makes it bloom.

- Grass x1.2 and Bug x1.2. Grass Pelt and Leaf Guard are always active (the tall grass).
- Grounded Grass and Bug Pokemon melt into the tall grass (x1.1 evasion).
- The breeze carries them: Fairy Wind, Silver Wind, Magical Leaf, Razor Leaf, Leafage, Pollen Puff x1.5; wind moves x1.2. Cut x2 (and blades send grass clippings flying: Cut, Slash, Air Slash, Air Cutter, Fury Cutter, Psycho Cut, X-Scissor also hit as Grass).
- Stampede: Stomp, Take Down, Double-Edge, Body Slam, Headbutt, Horn Attack, Wild Charge, Head Charge, Raging Bull, High Horsepower, Stomping Tantrum x1.2. Foragers: Bug Bite, Pounce, Lunge, Struggle Bug, Pluck x1.3.
- Powder moves x1.25 accuracy; Grass Whistle x1.3. Sweet Scent lowers evasion one stage more.
- On entry: Run Away +1 Speed (it darts into the grass), Sap Sipper +1 Attack. Sap Sipper grazes each turn (1/16 HP).
- Sun lasts 2 turns longer; Grassy Terrain 3 turns longer.
- 2 damaging Fire moves (1 in sunlight) set the dry grass alight -> Wildfire. Grassy Terrain, or 2 tending moves (Growth, Rototiller, Flower Shield, Floral Healing, Aromatherapy, Grass Pledge, Ingrain) -> Flower Garden.
- Telluric Seed: +1 evasion (it vanishes into the tall grass) and Ingrain.

**Changes:**
- FIRE-type moves x2 → **Wildfire**
- FIRE-type moves, in Sun/HarshSun → **Wildfire**
- terrain Grassy → **Flower Garden**
- GROWTH, ROTOTILLER, FLOWERSHIELD, FLORALHEALING, AROMATHERAPY +2 more x2 → **Flower Garden**

**Seed (TELLURICSEED):** EVASION +1; effects: ingrain.
## Every battle has a field

Data: `FIELD_DEFAULTS.yaml`. The engine picks, in order: the event's `setBattleRule("field", …)` → diving
(Underwater) → trainer exceptions → wild encounter type (surfing and fishing → Water Surface unless the map is
already watery; contests → Meadow) → the map's wild field → cave encounters on field-less maps (Cave) → surfing →
the map's field → the battle environment (grass → Meadow, forest → Silkwood, cave → Cave, sand → Beach, snow →
Snowy Mountain, …).

- All 424 maps in `maps.json` have an entry (the 79 built story maps are hand-reviewed; map 990 is the test arena).
  333 have a field; 91 are `NONE`: Poké Centers, Marts, houses, offices and other rooms with no battles.
- Kingdom flavour for maps the world spec left open: Elowen Meadow/Silkwood, Isenmar Beach/Snowy Mountain/Cave,
  Zenith Neon Grid/Mountain/Factory, Nadir New Moon (Lamplight)/Corrosive Mire/Scrapyard, Ashkaar
  Cinderglass/Mountain/Volcanic, Ossaria Desert/Cave, Antumbra Mindscape/Inverse, Crownhaven Grand Stage.
  Borderlands blend their two kingdoms.
- **Exceptions:** the tutorial battle (Kestrel K1 at Ferrow's Landing) has no field; gyms, bosses and set pieces set
  their own field in the event; Safari-style battles (Royal Chase) have no moves and so no field; Festival bracket
  rounds use the Temple-Arena's Grand Stage.
