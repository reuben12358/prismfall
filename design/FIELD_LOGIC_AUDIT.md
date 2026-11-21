# Field logic audit (SPINE Revision 24)

The creator (2026-11-21): *"I just want to make sure our field effects make sense and their transitions are relevant"*
and *"I'm also perfectly fine with certain field effects not having any transition effects."*

Every rule of the 35 fields was checked against two questions:

1. **Rules:** could a player guess *why this happens here*? Each needs a physical or lore reason. Rules that were
   arbitrary, contradicted another rule, or were pure number noise were reworked or cut.
2. **Transitions:** is the trigger plausible (fire burns a meadow, a flood fills a desert), is the destination what that
   place would really become, and does it matter in a real fight (does a trainer play it, or is it a fair player
   answer)? Implausible or pointless ones were reworked or cut. Fields with no transitions are fine.

Two fights are locked and were not touched: **Brann's Gym 7** (every Volcanic and Cinderglass rule his fight uses stays
exactly as it is) and the **Gym 1 Grand Stage crowd** rules. Rows are at the grain of the Field Notes bullets: one row
can cover several numbers that share one reason.

## Summary

| Rows in the tables below | Kept | Reworked | Cut | Added |
|---|---|---|---|---|
| Rules | 225 | 6 | 2 | 8 (all Glass Dunes: Mirror Glass, insulation, sound cracks, broken glass) |
| Transitions | 60 | 3 | 4 | 2 (Glass Dunes cooling and reheating) |

**Changed outside the Glass Dunes** (the fights whose fields changed were re-run: `design/BALANCE.md` §9c):

| Field | Change | Why |
|---|---|---|
| Frozen Lake | Sunlight now thaws the lake over **3 rounds of sun** (each damaging Ice move refreezes a round); only the harsh sun of Desolate Land melts it at once | It melted in one sunny turn although the same field says the ice is "far too thick to dig through". Anja's lake (Gym 10) no longer falls to one Sunny Day. |
| Crystal Cavern, Dark Crystal Cavern | Underground like the Cave: **Sun, Rain and Hail can't start**. Cut: "sunlight rekindles the Dark Crystal Cavern" | Cragholm's crystal caverns and the Darkglass Mine are underground; the Cave already says "there's no sky down here". Sandstorms (cave dust) still darken the crystals; two light moves still relight them. |
| Factory | Indoors: **no weather at all** (Sun is blocked too; its +2 turns are gone) | "The foundry roof shuts out the weather" blocked rain, sand and hail but made the sun last longer. The crucibles' heat is the Fire x1.2. |
| Neon Grid | Cut: **Pulse moves x1.5** | Dark Pulse, Dragon Pulse, Water Pulse and Aura Sphere have nothing to do with circuitry. The neon *light* moves keep their x1.3. |
| Wildfire | Cut: **Defog, Whirlwind or Tailwind blow it down to Embers** | The same field says wind *fans* the fire (wind moves x1.2 and also Fire). Water, rain and sand still put it out. |
| Underwater | **Sky Drop** fails and no longer surfaces the battle; cut: **2 Sludge Waves -> Corrosive Mire** | Sky Drop was both "impossible underwater" and a way up. A polluted deep sea doesn't turn into a surface swamp (and no fight used it). Dive, Fly and Bounce still surface. |
| Water Surface | The Corrosive Mire trigger is **Sludge Wave or Acid Spray x2** (Toxic no longer counts) | Toxic poisons one target, not a lake. |
| Wasteland | **Grassy Terrain -> Meadow** (was Flower Garden) | Grass comes back to poisoned slag first; a tended five-stage garden can't spring out of it. Purify x2 still -> Meadow. |
| Flooded Dunes | Cut: **Steam Engine +1 Speed on entry** | There's no steam in cold floodwater (the searing moves make the steam). |

**Not changed, on purpose:** the Volcanic sandstorm quench (the weakest Volcanic rule, a sandstorm smothering lava into
glass, but Brann's fight is locked and it is a player answer there), the Grand Stage, the Bleed and the Prism Arena
(their rules borrow other fields'), and every map default in `FIELD_DEFAULTS.yaml` (the audit found no map whose field
broke a rule; `field_defaults_to_rb.rb --check` is clean).

**Cross-field consistency checked:** sound breaks glass everywhere now (the Glass Dunes crack, the Hollow Cathedral's
stained glass, the Mindscape's dream "glass" over the Reverse World); underground fields have no sky (Cave, Crystal
Cavern, Dark Crystal); indoor fields have no weather (Grand Stage, Factory); burns are soothed by water (Water
Surface, Flooded Dunes, Snowy Mountain's snow) and impossible in it (Underwater); nothing freezes near heat (Volcanic,
Wildfire, Factory, Dragon's Den, Hot Glass).

## The Glass Dunes rework (approved concept)

Real glass forms from sand only at extreme heat (lightning, a blast site's trinitite, a meteor's impact glass), stays
hot a long time, flashes water to steam, bends and reflects light, is brittle (thermal shock, impacts), doesn't
conduct and cools. So the field has two stages:

| Rule / transition | Verdict | Reason |
|---|---|---|
| Hot Glass (stage 1): Fire x1.2, Fire types heal 1/16, Turboblaze x1.2 more, Steam Engine +1 Speed | keep | the white fire's heat stays in the glass |
| Hot Glass: Ice x0.8, nothing freezes | keep | ice hisses on hot glass |
| Hot Glass: Water moves may burn grounded targets (20%), Scald / Steam Eruption x1.3 and burn more | keep | water flashes to steam on it |
| Hot Glass: light moves x1.3 | keep | light bends through the heat haze |
| Hot Glass: no hail, Sun +2 | keep | too hot for hail; the glass holds the sun's heat |
| Mirror Coat x1.25, Reflect and Light Screen +3, Mirror / Prism Armor on entry (were on the hot glass) | rework | moved to Mirror Glass: steam-fogged hot glass isn't a mirror |
| **Cooling:** 4 rounds without a damaging Fire move -> Mirror Glass; sun holds the heat, rain cools it twice as fast | added | glass cools; the Fire side has to keep it hot |
| **Reheating:** a damaging Fire move turns Mirror Glass back into Hot Glass | added | fire heats glass |
| Mirror Glass (stage 2): beams and light moves x1.5 and never miss (the hot-glass list plus Psybeam, Ice Beam, Hyper Beam, Moongeist Beam, Meteor Beam, Lumina Crash) | added | Reborn's Mirror Arena: beams ricochet from mirror to mirror |
| Mirror Glass: Double Team and Minimize +1 evasion more | added | the mirror images multiply |
| Mirror Glass: Flash, Kinesis, Sand Attack, Smokescreen -1 accuracy more | added | the mirrors throw the glare back and forth |
| Mirror Glass: Counter, Mirror Coat, Metal Burst, Comeuppance x1.5 | added | the mirror throws the blow back harder (x1.25 on the old field) |
| Mirror Glass: Reflect, Light Screen, Aurora Veil +3 turns; Aurora Veil without hail; Mirror / Prism Armor on entry; hail can fall | added | barriers caught in the mirror; cool glass |
| Both: Mirror Shot x1.5 and always lowers accuracy | keep | the glare of the glass |
| Both: **Electric x0.8 against grounded targets; Electric Terrain can't form** | added | glass doesn't conduct |
| Both: Dig fails, Sand Tomb is Rock-type glass grit x1.2, no sandstorm, nothing takes root | keep | no loose sand left |
| Cracks: quakes, heavy blows, Rock Smash x2 (both stages), big Ice moves (Hot Glass only) | rework | thermal shock needs hot glass; Explosion and Self-Destruct join the impacts |
| **Damaging sound moves crack it** (both stages; Fire-type sound moves heat it instead) | added | the Choir tunes Glassfall glass by singing to it (`01_WORLD_LORE` "Choir glass", `Z_MOVES.md`); a loud enough voice breaks it |
| Shards hit the user's grounded foes (1/16, Rock-scaled) | keep | flying glass |
| **Broken glass stays on the ground** on that side: a grounded switch-in takes 1/16 Rock-scaled; Heavy-Duty Boots and being airborne avoid it; Rapid Spin, Mortal Spin, Defog, Tidy Up sweep it; Court Change swaps it; gone when the glass breaks or floods | added | shards lie where they fall (half a Stealth Rock, one layer) |
| 3 cracks -> Desert (in rain: Flooded Dunes); each damaging Fire move anneals one crack; cooling doesn't mend them | keep (the count now survives the stage change) | brittle glass falls back to sand; heat anneals glass |
| Heavy rain, 2 Origin Pulses or 3 floods -> Flooded Dunes | keep | the sea comes back over the glass; the war's tug of war (Kyogre, Isenmar) |
| Beam clash x2 -> the Bleed | keep | the story's beam clash over the glassing dunes (WAR-1); both Imprints are in the glass |
| Desert -> Glass Dunes (2 searing moves); Flooded Dunes -> Glass Dunes (Blue / Fusion Flare, or 2 searing moves) | keep | only extreme heat makes glass; Reshiram's white fire |
| Telluric Seed: +2 Def, -1 Sp. Def | keep | a glass carapace that light passes through |

## Per field

### Silkwood
| Rule / transition | Verdict | Reason |
|---|---|---|
| Bug x1.5, Grass x1.2, Fire x1.2; Swarm and Overgrow always on | keep | a bug forest; dry silk burns |
| Electroweb x1.5, never misses, 30% paralysis; Electric x1.2 in rain | keep | current runs along the threads (the creator's own idea); wet silk carries it |
| Bug signature moves x1.5 / x1.3; blades x1.2 | keep | bugs at home in their web; blades cut through silk |
| Bug fliers glide (Flying x1.2), other fliers x0.8 | keep | silk carries bugs and tangles birds |
| Bug contact moves wrap in silk (Speed -1); Bug added effects x2 | keep | silk sticks |
| String Shot, Electroweb, Sticky Web never miss; String Shot / Silk Trap tighter; Defend Order +1 Def | keep | silk moves in a silk forest |
| Grounded non-Bugs step into fresh silk once (Speed -1; boots avoid) | keep | walking into webs |
| Bug types sip nectar (1/16) | keep | the silk-moth groves flower |
| Grassy Terrain +3, Electric Terrain +2 | keep | forest floor; the webs hold charge |
| Telluric Seed: +1 Def / Sp. Def, -1 Speed | keep | a cocoon |
| -> Wildfire: 3 damaging Fire moves (2 in sun) | keep | fire races along the silk; Tamsin's rain answers it (Gym 2) |

### Grand Stage (locked: Gym 1 crowd rules)
| Rule / transition | Verdict | Reason |
|---|---|---|
| Applause stages, Normal and sound / dance boosts, showpieces, Sing, crits at Standing Ovation | keep | an opera house that plays to the crowd (tuned and approved) |
| Dancer, Punk Rock, Liquid Voice on entry; indoors, no weather | keep | stage performers; a roof |
| Synthetic Seed: +1 Speed, Laser Focus, Taunted by the spotlight | keep | the spotlight |
| Saltmere's house sets the opening stage; fans cheer from Encore up | keep | Rev 19 crowd idea, approved |
| Stage up: 2 dances / sound moves / showpieces or a crit; down: stalling | keep | the crowd cheers a show and is bored by stalling |

### Water Surface
| Rule / transition | Verdict | Reason |
|---|---|---|
| Water x1.5; Electric x1.5 and Fire x0.5 against grounded targets | keep | open water: current spreads, flames hiss |
| Torrent, Swift Swim, Hydration, Rain Dish, Dry Skin as if raining | keep | swimmers in their element |
| Whirlpool x2, water moves x1.3 / x1.2 | keep | currents |
| Ground moves and hazards sink | keep | nothing touches the ground |
| Wading x0.75 Speed; Water attacks sweep targets along (Speed -1) | keep | swimming is slow for non-swimmers |
| Burns soothed; Water Absorb sips; Water Compaction / Propeller Tail on entry | keep | cool water |
| Rain +3, Misty +2, no Grassy Terrain | keep | open water |
| Elemental Seed: +1 Speed, Aqua Ring | keep | a veil of seawater |
| -> Underwater: Dive (on the strike turn) | keep | the battle follows you down |
| -> Underwater: Gravity | keep | everything is dragged under (Reborn's rule) |
| -> Frozen Lake: 3 big Ice moves | keep | the water freezes; Anja's refreeze (Gym 10) |
| -> Corrosive Mire: 2 of Sludge Wave, Toxic, Acid Spray | **rework** | Sludge Wave or Acid Spray x2: Toxic poisons one target, not a lake |

### Underwater
| Rule / transition | Verdict | Reason |
|---|---|---|
| Water x1.5; Electric x1.5 never misses; Flying x0.5; sound x1.3 | keep | water conducts and carries sound; no air |
| Ground moves also hit as Water | keep | silt churns into the attack |
| Physical non-Water x0.5 from non-swimmers | keep | water drags at heavy blows |
| Water moves boosted; Whirlpool confuses; Octazooka's ink | keep | the deep belongs to swimmers |
| Fire fizzles; no burns; hazards fail | keep | underwater |
| "Fly, Bounce, Sky Drop fail" | **rework** | only Sky Drop fails; Fly and Bounce are the way up |
| Non-Water half Speed; rain abilities active; no weather or terrain | keep | underwater |
| Elemental Seed: Aqua Ring, becomes pure Water | keep | adapts to the deep |
| -> Water Surface: Dive, Fly, Bounce | keep | surfacing (not a transform strike) |
| -> Water Surface: Sky Drop | **cut** | Sky Drop fails underwater, so it can't also lift the battle |
| -> Corrosive Mire: 2 Sludge Waves | **cut** | a polluted deep sea doesn't become a surface swamp; no fight used it |

### Neon Grid
| Rule / transition | Verdict | Reason |
|---|---|---|
| Electric x1.5, Steel x1.2 | keep | live circuitry; steel conducts |
| Pulse moves x1.5 | **cut** | Dark / Dragon / Water Pulse and Aura Sphere aren't electrical (Rook's team had none) |
| Neon light moves x1.3 | keep | the neon glare |
| Conductors (Gear Grind, Flash Cannon, Surf...) also hit as Electric | keep | metal and water carry current |
| Electric move boosts; Water moves carry 30% paralysis; Zap Cannon 80%, Thunder x1.2 | keep | the grid feeds them (Rook's Camera) |
| Grounded Pokemon can't sleep; Surge Surfer on; Magnet Rise +3 | keep | the buzzing grid underfoot |
| Charge / Magnet Rise / Eerie Impulse bonuses; Plus, Minus, Motor Drive... on entry | keep | charged up |
| Electric Terrain +3 | keep | the grid holds it |
| Blackout stage: cycling surges, Dark / Ghost up, light x1.5 | keep | a shorted grid flickers; shadows (Reborn's Short-Circuit) |
| Synthetic Seed: +1 Sp. Atk, Magnet Rise | keep | floats above the live grid |
| -> Blackout: 2 quakes, 2 floods or Mud Sport | keep | quakes and water short it; the player's answer to Rook |
| Blackout -> back: 2 charging moves or Electric Terrain | keep | reboot; Rook's Charge |

### Desert
| Rule / transition | Verdict | Reason |
|---|---|---|
| Ground x1.2, Fire x1.2; Ice x0.75, Water x0.8 | keep | sun-baked sand drinks water and melts ice |
| Sand abilities without weather; Solar Power free | keep | sand and sun everywhere |
| Ground types burrow (special x0.67) | keep | hiding in the sand |
| Sand Tomb x2, sun / cactus / bone moves boosted | keep | the Bone Sands |
| Physical Ground moves kick sand (20% acc -1); Sand Attack better; Shore Up +1 Def | keep | loose sand |
| Earth Eater heals, Dry Skin dries | keep | the dunes; the heat |
| No hail; Sandstorm +3, Sun +2; no Grassy Terrain | keep | desert climate |
| Superbloom: Grass x1.5, Bug x1.2, petals, Chlorophyll, Leaf Guard, Grass heals | keep | rain wakes the seeds in the sand (real deserts do this) |
| Telluric Seed: +1 Def / Sp. Def, -1 Speed | keep | half-buried |
| -> Superbloom: rain, or 3 floods | keep | Sahar's fight; Isenmar's Drizzle on 920 |
| Superbloom -> dunes: sun, sandstorm, 2 Fire attacks | keep | the bloom withers |
| -> Flooded Dunes: heavy rain, Origin Pulse; from the bloom also 3 floods | keep | Kyogre's sea-storm over the dunes (Ch19) |
| -> Glass Dunes: 2 searing moves | keep | only extreme heat makes glass; Ashkaar's plan on 926 |

### Corrosive Mire
| Rule / transition | Verdict | Reason |
|---|---|---|
| Poison x1.5, added effects x1.5; Poison hits Steel | keep | toxins corrode steel |
| Grass moves also Poison; mud and Muddy Water also Poison | keep | plants and mud drink the toxins |
| Acid / sludge / mud moves boosted; Venoshock always doubled against grounded targets | keep | everything grounded stands in poison |
| Accuracy of poison powders and gases up; Water may poison | keep | toxic water and air |
| Poison types fling mud (30% poison) and heal 1/16 | keep | Poison Pokemon weaponise the mire |
| Toxic Boost on; Merciless / Corrosion / Poison Touch / Toxic Debris on entry | keep | at home in poison |
| Fire x1.3 and scorches grounded foes 1/8 | keep | marsh gas ignites (Corvin's Heat Wave) |
| Synthetic Seed: +1 Atk / Sp. Atk, holder poisoned | keep | power from the toxins |
| -> Water Surface: Misty Terrain, or 2 Purify | keep | cleansed mire becomes clear water; J2 Juno's Misty Terrain |
| -> Wasteland: 2 damaging Fire moves | keep | the gas burns off, leaving poisoned badlands; Corvin's play (Gym 6) |

### Volcanic (locked: Gym 7)
| Rule / transition | Verdict | Reason |
|---|---|---|
| Fire x1.5, Ice x0.5; Blaze, Flare Boost, Flash Fire | keep (locked) | magma |
| Rock moves superheated; wind carries embers | keep (locked) | lava rock; embers on the wind |
| Lava / smog / earth moves boosted; Smack Down onto the crust | keep (locked) | the crust |
| Eruptions primed by quakes and lava moves; lava rains on grounded foes | keep (locked) | Brann's plan |
| Will-O-Wisp, Ground burns, Smokescreen | keep (locked) | heat and smoke |
| Nothing freezes; Magma Armor; no hail; Sun +3; no Grassy / Misty | keep (locked) | heat |
| Elemental Seed: +1 Atk / Sp. Atk / Speed, holder burned | keep (locked) | Camerupt's seed |
| -> Cinderglass: 2 floods / big Ice moves, or rain | keep (locked) | quenched lava sets into obsidian; the intended answer |
| -> Cinderglass: sandstorm | keep (locked) | weakest Volcanic rule (sand smothering lava); a player answer in a locked fight |

### Cinderglass (`:ASHEN_WASTE`)
| Rule / transition | Verdict | Reason |
|---|---|---|
| Rock x1.3, Ground x1.2, Fire x1.2, Ice x0.7 | keep | obsidian over still-hot rock |
| Geysers every 3 rounds; quakes set them off | keep | a quenched volcano vents steam (Brann's Anvil, Steam Engine) |
| Floods flash to steam (accuracy -1) | keep | water on hot rock |
| Scald / Steam Eruption x1.5 | keep | steam |
| Obsidian shards: Stone Edge... x1.3; Stealth Rock doubled | keep | volcanic glass edges |
| Wind whips up glass grit (also Rock, 30% acc -1); glass storms | keep | grit |
| Sand Rush / Sand Veil in grit; Rock Polish +1 Speed; Smokescreen | keep | grit and smoke |
| Steam Engine, Magma Armor on entry; hail melts | keep | steam and heat |
| Elemental Seed: +1 Speed, +1 evasion, -1 accuracy | keep | a cloak of steam |
| -> Volcanic: 3 big Fire moves | keep (locked) | re-melting it; Brann's Lava Plumes |
| -> Water Surface: 3 floods or heavy rain | keep | the caldera fills into a lake |

### Inverse Field
| Rule / transition | Verdict | Reason |
|---|---|---|
| Inverse type chart | keep | the Reverse World |
| Ghost, Psychic, Dark x1.2; reflection moves x1.25; Psychic may confuse | keep | creatures of mind and shadow; reflections |
| Contrary, Magic Bounce, Mirror Armor on entry; rooms and Psychic Terrain longer; Topsy-Turvy +1 Speed | keep | a world inside out |
| Magical Seed: +1 Atk / Sp. Atk, -2 Speed | keep | built for Trick Room |
| -> previous field (or Mindscape): Topsy-Turvy | keep | rights the world; Dask's Malamar |

### The Bleed and the Prism Arena
| Rule / transition | Verdict | Reason |
|---|---|---|
| The Bleed borrows another field every 3 rounds (war pool on 925 / 926); off-type x1.2; type-shifting moves x1.3; stat warp | keep | raw Imprint energy; the story's Bleed |
| The Prism Arena borrows each gym's field in a fixed, announced order | keep | the Festival's Plates |
| No transitions (borrowed fields never transform them) | keep | fine without |

### Colosseum
| Rule / transition | Verdict | Reason |
|---|---|---|
| Fighting x1.2 (x1.5 Frenzy); punches, kicks, throws boosted | keep | a pit-fighting arena |
| Crowd: knockouts +1 Atk / Sp. Atk; underdog x1.2; Psychic mind games booed | keep | the crowd decides |
| Focus moves, No Retreat, Inner Focus / Steadfast crits; No Guard, Justified, armour on entry | keep | fighters' arena |
| Double Team, Minimize, Roar, Whirlwind fail | keep | nowhere to hide, no one leaves the pit |
| Synthetic Seed: +1 Atk, Focus Energy, Taunted | keep | the roar of the crowd |
| Frenzy stage after 2 knockouts; 2 stalling moves calm it | keep | the crowd's mood |
| -> Cave: 3 quakes | keep | Ironreach's Iron Pit is a colosseum in a mined-out cavern (`01_WORLD_LORE`); Sable and Brisk's Ch9 play |

### Flower Garden
| Rule / transition | Verdict | Reason |
|---|---|---|
| 5 growth stages; Grass, Bug, Fire, petals and Cut grow stronger with it | keep | a garden grows; dense dry growth burns better |
| Grows from tending moves, sun or rain, Grassy Terrain, Grass attacks, Flower Veil / Gift | keep | tending |
| Cut back by Fire, blades, hail; acid resets it | keep | pruning and poison |
| Stage 3+: Overgrow, Swarm, Grass Pelt, powders, healing; stage 4+: Chlorophyll, nectar | keep | lush garden |
| Stage 5: overgrowth shields Grass types | keep | Juno's overgrowth |
| Grassy Terrain +3; Telluric Seed grows it | keep | a garden |
| Stage 5 -> Wildfire: 2 Fire attacks | keep | an overgrown garden burns; the counterplay to Juno (Gym 9) |

### Frozen Lake
| Rule / transition | Verdict | Reason |
|---|---|---|
| Ice x1.5; Rock moves freeze into ice boulders | keep | the lake's cold (Reborn's Icy Field) |
| Skating and sliding moves boosted, +1 Speed on priority / rolling moves | keep | slick ice |
| Icy Wind / Glaciate slow more; Slush Rush, Snow Cloak, Ice Body without hail | keep | ice everywhere |
| Quakes splinter the ice into Spikes | keep | broken ice |
| Dig fails (ice too thick); Hail +3; Aurora Veil without hail; no Grassy | keep | thick ice |
| Elemental Seed: +2 Speed, 1/8 HP | keep | skating across jagged ice |
| -> Water Surface: 3 cracks (Fire, quakes, heavy blows); Ice refreezes a crack | keep | the ice gives way; Anja's Body Press / High Horsepower play |
| -> Water Surface: sunlight melts it at once | **rework** | 3 rounds of sun thaw it (Ice moves refreeze a round); harsh sun still melts it at once. One sunny turn can't melt ice "too thick to dig through" |

### Stormfront
| Rule / transition | Verdict | Reason |
|---|---|---|
| Electric x1.3, Flying x1.2, wind moves x1.2 | keep | a storm on an airship deck |
| Smack Down x2 onto the deck; aerial moves boosted; Hurricane / Thunder / Storm moves never miss | keep | wind and lightning |
| Hazards blow off the deck; Tailwind +2 | keep | gale |
| Wind Rider, Wind Power, Big Pecks, Levitate on entry | keep | at home in wind |
| Lightning in rain strikes fliers; Electric types channel it | keep | lightning seeks the highest point |
| No sun; Electric Terrain +3 | keep | the storm swallows the sun |
| Elemental Seed: +1 Speed, Charge | keep | storm-charged |
| -> Rainbow: 2 Sunny Days | keep | sun breaking through a storm makes a rainbow; Odessa's play (Gym 11) |

### Mindscape
| Rule / transition | Verdict | Reason |
|---|---|---|
| Psychic x1.5; Dark and Ghost x1.2; sound x1.2 | keep | thought made real; nightmares lurk |
| Dream / mind moves boosted; disciplined minds resist | keep | a world of thought |
| Sleep is shallow; Meditate / Kinesis better; Forewarn, Anticipation, Telepathy on entry; rooms longer | keep | lucid dreaming |
| Nightmare stage: Dark / Ghost x1.5, Hex, Dream Eater, sleep deep | keep | the dream curdles |
| Magical Seed: +2 Sp. Atk, confused | keep | a flood of thoughts |
| -> Nightmare: Dark Void, Nightmare, Spite or 3 Dark attacks; back with 2 soothing moves | keep | Kroll's Ch13 play; Ilsa's Calm Minds |
| -> Inverse: Topsy-Turvy, or 3 damaging sound moves | keep | noise shatters the dream like glass and shows the Reverse World behind it (Lucent, Antumbra); Ilsa's Psychic Noise, the Octave's Espeon |

### Crystal Cavern
| Rule / transition | Verdict | Reason |
|---|---|---|
| Rock x1.3, Dragon x1.2, sound x1.2 | keep | gems; old wyrms hoarded them; the crystals ring |
| The glow cycles Fire > Water > Grass > Psychic | keep | prismatic crystals (Reborn) |
| Stealth Rock flares with the glow; light moves x1.5 | keep | crystal light |
| Ancient Power, Flash, Rock Polish bonuses | keep | gems |
| Screens +2, Aurora Veil without hail, Prism Armor | keep | mirroring crystals |
| Weather: sun, rain and hail could start | **rework** | underground now: Sun, Rain, Hail can't start (as in the Cave; Cragholm is carved into the canyon wall) |
| Magical Seed: +1 Sp. Atk, Light Screen | keep | crystal barrier |
| -> Dark Crystal: Dark Pulse, Night Daze, Dark Void, Fiery Wrath, or a sandstorm | keep | darkness or dust blots out the light; Bastian's Geode lost Sand Stream for it |
| -> Cave: an explosion, or 3 quakes | keep | the crystals shatter; Bastian's Golem (Gym 13) |

### Dark Crystal Cavern
| Rule / transition | Verdict | Reason |
|---|---|---|
| Dark x1.5, Ghost x1.3, Rock x1.2; Dark / Ghost take x0.83 | keep | hunting in the dark |
| Shadow strikes x1.5; light moves x1.2 | keep | struck from the dark; light pierces it |
| x0.9 accuracy for those who can't see; Dark / Ghost contact crits; Flash; no Solar Beam | keep | darkness |
| Weather: sun, rain and hail could start | **rework** | underground: they can't (Darkglass Mine, Lightless Deep) |
| Magical Seed: +1 Atk / Sp. Atk | keep | |
| -> Crystal Cavern: 2 light moves | keep | light rekindles the crystals; Marchetti Ch14 |
| -> Crystal Cavern: sunlight | **cut** | there's no sky in a cavern |
| -> Cave: an explosion, or 3 quakes | keep | the dead crystals shatter |

### Hollow Cathedral
| Rule / transition | Verdict | Reason |
|---|---|---|
| Ghost x1.5, sound x1.3; Ghost and Normal hit each other | keep | a haunted nave that echoes; the veil is thin |
| Ghostfire (Fire also Ghost); Will-O-Wisp; Ghost moves boosted; spirits around sleepers | keep | candles and spirits |
| Cursed Body / Perish Body / Mummy / Rattled on entry | keep | the haunted |
| Consecrated stage: Ghost / Dark x0.8, Fairy and holy x1.2 / x1.5, Normal smites Ghosts | keep | holy light |
| Magical Seed: +1 Sp. Def, part Ghost | keep | a wandering spirit |
| -> Consecrated: 3 holy acts; back with 2 Ghost rites by a Ghost | keep | Wick's Ch7 play; Ysolde's rites (Gym 14) |
| -> Inverse: Topsy-Turvy, or 2 of Boomburst, Shadow Force, Hyperspace Fury / Hole | keep | they shatter the stained glass, and the Glass between the worlds is thin here; sound breaks glass, as on the Glass Dunes |

### Factory
| Rule / transition | Verdict | Reason |
|---|---|---|
| Steel x1.5, Electric x1.2, Fire x1.2 | keep | machinery, power, crucibles |
| Gears, hammers, rollers boosted; Fire softens plating | keep | a foundry |
| Metal-tuning moves better; Light / Heavy Metal, Download on entry | keep | metal shaped eagerly (the Iron Plate) |
| Nothing freezes; Electric Terrain +2 | keep | crucibles; power |
| "Indoors: no rain, sand or hail; Sun +2 turns" | **rework** | indoors means no weather at all: Sun can't start either |
| Synthetic Seed: +1 Atk, +1 Speed | keep | |
| -> Scrapyard: an explosion, or 3 quakes | keep | wreck the foundry; Magnus's flip (Gym 15), Quent's Explosion (Ch16) |

### Scrapyard
| Rule / transition | Verdict | Reason |
|---|---|---|
| Steel x1.2, Poison x1.2; junk and smog boosted | keep | scrap and leaking chemicals |
| Rust: Water super effective on Steel | keep | wet scrap rusts |
| Oil slicks burn (20%); live cables paralyse Steel targets (20%) | keep | scrapyard hazards |
| Stealth Rock mixed with scrap; scavenger abilities on entry | keep | junk everywhere |
| Shift Gear and Gear Up fail | keep | rusted gears |
| Synthetic Seed: +1 Def / Sp. Def, -1 Speed | keep | bolted-on scrap |
| -> Factory: 3 charging moves | keep | power restarts the machines; Magnus's Mark One |
| -> Wasteland: 2 acid moves | keep | the chemicals leach into poisoned ground |

### New Moon
| Rule / transition | Verdict | Reason |
|---|---|---|
| Dark x1.5, shadow moves x1.2; x0.9 accuracy for the unseeing | keep | a moonless undercity |
| Stars and light pierce it; Moonlight fails, Moonblast dims; no sun | keep | no moon, no sun |
| Abyss stage: total darkness | keep | deeper dark |
| Lamplight stage: lamps lit, Fire / Electric x1.2, thieves | keep | Nadir's gaslamps |
| Magical Seed: accuracy, Focus Energy, draws the shadows in | keep | Nyx's Weavile (Gym 16) |
| -> Abyss: Dark Void or 3 deepening moves; back with 2 light moves | keep | Nyx's play |
| -> Lamplight: 3 light moves; back with 3 Dark attacks | keep | the player's answer to Nyx; her snuffing |

### Fairy Tale
| Rule / transition | Verdict | Reason |
|---|---|---|
| Fairy x1.5, Dragon x1.5, Steel x1.3; Marvel Scale | keep | fairies, dragons and knights |
| Knights' blades; Steel slays Dragons; Cut / Slash become Steel | keep | dragonslayers |
| Dragonfire: Fire also Dragon | keep | the story's dragon |
| Spells boosted; true love's kiss wakes sleepers | keep | fairy tale tropes |
| Shields and Noble Roar better; armour and magic abilities on entry | keep | castle |
| Sleepers dream of happily ever after; Misty +3 | keep | |
| Magical Seed: +1 Sp. Atk / Sp. Def | keep | a fairy godmother |
| -> Dragon's Den: 3 Dragon attacks | keep | rouse the dragon beneath the castle; K7 and Celestine (Gym 17) |

### Dragon's Den
| Rule / transition | Verdict | Reason |
|---|---|---|
| Dragon x1.5, Fire x1.3; Water / Ice x0.7; Dragons x0.83 damage taken | keep | a dragon's lair over magma |
| Hoard moves (Pay Day, Make It Rain); lair moves boosted; Dragon Rage 140 | keep | the hoard; dragon's rage |
| Magma Armor, Multiscale, Flash Fire, Dragon's Maw | keep | lair |
| Amulet Coin holders can't be statused | keep, **and teach it** | the hoard protects its own (Sigrun's Dreamwing). It fails "could a player guess it?" on its own, so the Field Notes say it plainly and a Wyrmrest dragon-tamer hints it: "Bring gold into a dragon's den, and the hoard treats you as its own." (Gemini review 2026-11-21) |
| Nothing freezes; Stealth Rock with embers; no hail; Sun +2; no Grassy | keep | Wyrmrest is an open rift on the peaks, so sun is fine |
| Wyrmfire stage after 4 Dragon attacks | keep | the den awakens |
| Elemental Seed: +1 Atk / Speed, Flash Fire | keep | |
| -> Cave: 3 Water / Ice attacks | keep | cooling the lair leaves a cave; the player's answer to Sigrun |
| -> Fairy Tale: 3 Fairy attacks | keep | fairy magic tames the dragon |

### Cave
| Rule / transition | Verdict | Reason |
|---|---|---|
| Rock x1.5; sound x1.5; drilling moves | keep | echoing stone |
| Low ceiling: non-contact Flying x0.5, Ground hits fliers, Sky Drop fails | keep | no room to fly |
| Sound status moves more accurate; Flash, Howl | keep | echoes |
| Stealth Rock doubled; no sun, rain or hail; Sandstorm +3 | keep | underground |
| Cave-in on the second quake | keep | the ceiling cracks, then falls (Kroll Ch17) |
| Telluric Seed: +1 Def, Stealth Rock on the foes | keep | |
| -> Crystal Cavern: 2 Power Gems / Diamond Storms | keep | gems in the walls catch the light |
| -> Volcanic: 2 eruption moves | keep | magma breaks through |
| -> Dragon's Den: Draco Meteor, or 2 Dragon Pulses | keep | dragon fire relights a lair; Sigrun reopens her den (Gym 18) |

### Mountain
| Rule / transition | Verdict | Reason |
|---|---|---|
| Rock x1.5, Flying x1.2, wind x1.3; Avalanche, throws, Sky Attack, Hyper Voice | keep | boulders, ridge winds, echoes off the peaks |
| Storm moves accurate; Thunder never misses on the peaks | keep | high and exposed |
| Tailwind +2; wind abilities | keep | |
| Sun +3 | keep | thin air, strong sun |
| Telluric Seed: +1 Speed, Tailwind | keep | |
| -> Snowy Mountain: hail, or 2 big Ice moves | keep | snow buries the peak |
| -> Volcanic: 2 eruption moves | keep | magma breaks through the peak |

### Snowy Mountain
| Rule / transition | Verdict | Reason |
|---|---|---|
| Ice x1.5, Rock / Flying x1.2, wind x1.3, Fire x0.75 | keep | blizzard |
| Rock moves come down frozen; snowballs and throws | keep | avalanche |
| Ice types take less from physical attacks | keep | snow armour (as Gen 9 Snow) |
| Snow abilities without hail; Hail +3; Aurora Veil; Tailwind +2 | keep | |
| Deep snow soothes burns | keep | |
| Telluric Seed: +1 Def, Defense Curl | keep | |
| -> Mountain: sun, or 2 big Fire moves | keep | the snow melts off the slopes |
| -> Volcanic: 2 of Eruption / Magma Storm | keep | magma breaks through |

### Beach
| Rule / transition | Verdict | Reason |
|---|---|---|
| Water x1.2, Ground x1.2; mud and sand moves | keep | sand and surf |
| Tide-pool moves; focus moves; focused minds ignore accuracy and evasion stages | keep | the calm of the waves (Reborn) |
| Calm Mind / Meditate / Kinesis / Sand Attack bonuses | keep | |
| Sand abilities; sea breeze kicks sand | keep | |
| Shore Up heals more; spray heals; Hydration cures | keep | |
| No hail; Sun / Sandstorm +2 | keep | balmy sea air |
| Telluric Seed: +1 Def, Aqua Ring | keep | |
| -> Water Surface: heavy rain, or 3 big surf moves | keep | the tide comes in |

### Rainbow
| Rule / transition | Verdict | Reason |
|---|---|---|
| Added effects twice as likely | keep | prismatic light (Reborn) |
| Normal x1.5, Dark x0.75, Marvel Scale | keep | light washes out the dark |
| Colourful moves x1.5 | keep | |
| Sonic Boom 140 | keep | Reborn's Sonic Rainboom nod; harmless, Sonic Boom is otherwise dead |
| Cosmic Power, sweet dreams, Nightmare fails, Cloud Nine | keep | |
| Misty +3; Aurora Veil without hail | keep | |
| Magical Seed: +1 Sp. Atk, Wish | keep | a wish on a rainbow |
| -> previous field (or Meadow): sandstorm, hail or Defog | keep | the storm blots it out |

### Wasteland
| Rule / transition | Verdict | Reason |
|---|---|---|
| Poison x1.2 (x1.5 in acid rain); sludge moves | keep | slag and grime |
| Sludge inflicts random statuses | keep | something nasty in the slag |
| Weeds whip; trapped fumes boost explosions; quakes x0.5 | keep | the slag soaks up quakes (Corvin's Wasteland) |
| Toxic Boost; Poison Heal | keep | |
| Synthesis / Morning Sun / Moonlight fail | keep | the jaundiced sky |
| Hazards splinter into Imprint shards | keep | Bleed-scarred ground |
| Sandstorm +3 | keep | |
| Telluric Seed: +1 Atk / Sp. Atk, badly poisoned | keep | |
| -> Flower Garden: Grassy Terrain | **rework** | -> Meadow: grass comes back first; a tended garden can't spring from slag |
| -> Meadow: 2 Purify | keep | cleansing |

### Wildfire
| Rule / transition | Verdict | Reason |
|---|---|---|
| Fire x1.5, Blaze, Flare Boost, Flash Fire; Ice x0.5; Grass x0.5 against grounded | keep | a blaze |
| Wind moves fan the flames (also Fire); smog, Smack Down, Flame Charge | keep | wind feeds fire |
| Fire spreads (30% sea of fire) | keep | |
| Will-O-Wisp, Smokescreen; nothing freezes | keep | |
| Fuel: burns down to Embers after 4 rounds; Fire feeds it | keep | fires burn out |
| Embers stage: coals, ash, pioneer shoots, smoke wraiths | keep | after a fire |
| Elemental Seed: +1 Atk / Sp. Atk, Flash Fire, burned | keep | |
| -> Embers: 2 douses, rain or a sandstorm | keep | water and sand put fire out |
| -> Embers: Defog, Whirlwind, Tailwind | **cut** | the same field says wind fans the fire |
| Embers -> Wildfire: 2 big Fire moves or sun | keep | re-ignition |
| Embers -> Meadow: rain, Grassy Terrain, 2 growing moves | keep | life returns (Thistle, Juno) |

### Meadow
| Rule / transition | Verdict | Reason |
|---|---|---|
| Grass x1.2, Bug x1.2; Grass Pelt, Leaf Guard | keep | tall grass |
| Grass and Bug types hide in the grass (evasion) | keep | |
| Breeze, blades, stampede, foragers boosted | keep | open country |
| Powders, Grass Whistle, Sweet Scent; Run Away, Sap Sipper | keep | |
| Sun +2, Grassy +3 | keep | |
| Telluric Seed: +1 evasion, Ingrain | keep | vanishes into the grass |
| -> Wildfire: 2 Fire moves (1 in sun) | keep | dry grass burns; J1 Juno's lesson |
| -> Flower Garden: Grassy Terrain or 2 tending moves | keep | tending makes it bloom; J1 Juno's Prankster Grassy Terrain |

### Flooded Dunes
| Rule / transition | Verdict | Reason |
|---|---|---|
| Water x1.3, Ice x1.2, Electric x1.3 against grounded | keep | the Northern Sea over the sand |
| Fire x0.5 against grounded, except searing moves and Turboblaze | keep | water hisses fire down; white fire is too hot |
| Searing moves flash the flood to steam (accuracy -1) | keep | |
| Mud: Ground also Water; mud moves; quicksand | keep | wet sand |
| Surf moves; hazards sink | keep | |
| Wading; rain abilities active | keep | |
| No burns; burns soothed; Water Absorb / Storm Drain; Water Compaction | keep | cold water |
| Steam Engine +1 Speed on entry | **cut** | no steam in cold floodwater |
| Rain +3; no sandstorm | keep | |
| The tide drains into a Superbloom after 5 rounds (rain holds it, Water feeds it, sun drains it) | keep | a flood drains into sand |
| Elemental Seed: +1 Speed, part Water | keep | soaked through |
| -> Glass Dunes: Blue / Fusion Flare, or 2 searing moves, even when snuffed | keep | white fire fuses the wet sand (Reshiram, Ch19) |
| -> Frozen Lake: 3 big Ice moves | keep | the flood freezes; Isenmar's Lapras |
| -> Desert Superbloom: the tide runs out | keep | |
