# Field backdrops after the Revision 10 field redesign

For the backdrop workstream (art/battlebacks, Prismfall EBDX Bridge). The field side keeps one `:backdrop`
key per field and per stage. The bridge builds `Graphics/EBDX/Battlebacks/battlebg/<key>.png` (+ `_hd`) from
these keys. If a stage key has no art, the bridge falls back to the stage-1 art. The field plugin never
edits the bridge config. Everything below is a request or a suggestion.

Status checked 2026-11-17 11:10: **every key below already has art in `graphics/EBDX/Battlebacks/battlebg/`**
(the backdrop pass ran in parallel and picked up the keys from the field files). **Exception, 2026-11-19:** the two war fields
`field_flooded_dunes` and `field_glass_dunes` are new and have no art yet (briefs in the table; bridge suggestions in §4). So the open items are design
changes the current art does not show yet, plus transition colours for the new transitions.

## 1. Keys: fields and stages

| Field ID | In-game name | Stage | Backdrop key | Status / what the art should show |
|---|---|---|---|---|
| WILDFIRE | Wildfire | 1 | `field_wildfire` | **NEW field.** Art exists. A forest or meadow fully alight. The fire is a resource that Fire types ride and feed (fuel counter), not a disaster scene. |
| WILDFIRE | Wildfire | 2 "Embers" | `field_wildfire_embers` | **NEW stage.** Art exists. A burned-down glow: smouldering ground, drifting sparks, the first green shoots. It leads on to MEADOW, so the shoots matter. |
| MEADOW | Meadow | 1 | `field_meadow` | **NEW field.** Art exists. Open grass and wildflowers. It is the default for most routes, so it must look good and not bland: wind in the grass, wildflowers, pollen. |
| ASHEN_WASTE | **Cinderglass** (renamed) | 1 | `field_ashen_waste` (key kept) | **REWORK needed.** The current art is a cooled caldera under falling grey ash. The redesign is *Cinderglass*: lava quenched into a plain of black volcanic glass, with steam geysers that erupt every 3 rounds, glittering glass grit, and obsidian shards that Rock/Ground users throw. Please keep the Volcanic layout so the quench still reads as the same place. Swap the grey ash fall for steam plumes rising from vents (periodic bursts would match the geyser rounds), glints on glass facets, and a violet-black glass sheen with hot orange seams in the cracks. Avoid grey, dusty "dead" art. The user's complaint was that this transition felt like going to "kinda nothing". |
| FLOODED_DUNES | Flooded Dunes | 1 | `field_flooded_dunes` | **NEW field (2026-11-19, the Ch19 war; no art yet).** *Desert dunes under a flood-sea.* Ossaria's bone-white dunes with the Northern Sea poured in over them: grey-green seawater fills the hollows, the dune crests stand out of it as pale sandbars, foam lines and a slow swell run between them, wet dark sand at every waterline, the grey sea on the horizon and a low rain-sky. Keep the Desert layout (the same dunes, now drowned) so DESERT -> FLOODED_DUNES reads as the sea arriving. It is Kyogre's sea and Isenmar's ground: powerful, cold, moving water, not a disaster scene. Spray, rain sheen and drifting foam would fit; a tide line that rises and falls would match the drain mechanic. |
| GLASS_DUNES | Glass Dunes | 1 | `field_glass_dunes` | **NEW field (2026-11-19, the Ch19 war; no art yet).** *Black-green glass dunes with steam.* The same dunes fused by white fire into smooth black-green glass (desert glass / trinitite: deep bottle-green to near-black, with hot amber seams where it is still cooling), a breaking wave of the flood set into glass mid-curl, hollows of boiling water steaming between the glass crests, glints and refraction on the facets, a faint prismatic Bleed shimmer where the two Imprints are locked in. Steam rising in plumes, not grey ash. It must read as beautiful and strange, the place Reshiram made, and later the bone-carters' necropolis: no gore, no glassed bodies in the battle art. Keep the Desert/Flooded Dunes layout so the three backdrops are one place in three states. |
| GLASS_DUNES | Mirror Glass (stage 2, Rev 24) | 2 | `field_glass_dunes_mirror` | **Built 2026-11-21** (`art/battlebacks/fields_g.py` `glass_mirror`). The same glassed dunes after the heat has gone (4 rounds without Fire): clear green glass mirroring a cool blue sky and its cirrus by elevation, still mirror ponds where the pools boiled, clear glass cacti and wave, mirror platforms; facet flashes, a sweeping sheen, the sun and its glint; no steam, no amber seams. Reborn's Mirror Arena in the Glass Dunes. The Hot -> Mirror and Mirror -> Hot stage changes use the stage colour fade. |
| GRAND_STAGE | Grand Stage | 2 "Encore" | `field_grand_stage_2` | Stage. Art exists. Warmer lights, an audience reacting. |
| GRAND_STAGE | Grand Stage | 3 "Standing Ovation" | `field_grand_stage_3` | Stage. Art exists. Full spotlight, confetti. |
| NEON_GRID | Neon Grid | 2 "Blackout" | `field_neon_grid_blackout` | Stage. Art exists. The grid has shorted: dark city, live sparks, Electric power surging in a cycle. A pulsing spark layer would show the surge cycle. |
| DESERT | Desert | 2 "Superbloom" | `field_desert_bloom` | Stage. Art exists. Rain makes the desert bloom. |
| MINDSCAPE | Mindscape | 2 "Nightmare" | `field_mindscape_nightmare` | Stage. Art exists. |
| HOLLOW_CATHEDRAL | Hollow Cathedral | 2 "Consecrated" | `field_hollow_cathedral_consecrated` | Stage. Art exists. The curse is lifted and light pours in. |
| NEW_MOON | New Moon | 2 "Abyss" | `field_new_moon_abyss` | Stage. Art exists. |
| NEW_MOON | New Moon | 3 "Lamplight" | `field_new_moon_lamplight` | Stage. Art exists. Also the town default for Nadir (Ironreach, Underveil, Barons' Stair), so it will be seen a lot. |
| DRAGONS_DEN | Dragon's Den | 2 "Awakened" (Wyrmfire) | `field_dragons_den_wyrmfire` | Stage. Art exists. The hoard-dragons are awake and the den runs with wyrmfire. |
| FLOWER_GARDEN | Flower Garden | 2-5 | `field_flower_garden_2` ... `_5` | Unchanged keys. Art exists. Stage 5 can now catch fire and become WILDFIRE. |
| CAVE | Cave | 2 "Cracked ceiling" | (none: uses `field_cave`) | Optional. Stage 2 is the cave after a quake: the ceiling is cracked and the next quake brings it down. A `field_cave_cracked` key could be added if the art budget allows. Ask and the field will point to it. |
| COLOSSEUM | Colosseum | 2 "Frenzy" | (none: uses `field_colosseum`) | Optional. The crowd in a frenzy after KOs. A `field_colosseum_frenzy` key could be added, same as above. |

Unused art: `field_frozen_lake_night` is not referenced by any field (fine as a scripted `nextBattleBack`).

No field was removed. All 31 roster IDs plus WILDFIRE and MEADOW keep their IDs and `field_<id>` keys.

## 2. Transitions that are new or changed (suggested `TRANSITION_OVERRIDES`)

The bridge has overrides for VOLCANIC->ASHEN_WASTE, FROZEN_LAKE->WATER_SURFACE, WATER_SURFACE<->UNDERWATER,
CRYSTAL_CAVERN->DARK_CRYSTAL, FACTORY->SCRAPYARD, SILKWOOD/FLOWER_GARDEN/MEADOW->WILDFIRE, MEADOW->FLOWER_GARDEN,
ANY->BLEED and BLEED->ANY. `[:WILDFIRE, :ASHEN_WASTE]` is no longer used: Wildfire now burns down to Embers
and then regrows into MEADOW. Suggested colours for the other transitions:

| From -> To | Trigger (short) | Suggested flash |
|---|---|---|
| DESERT -> FLOODED_DUNES | Primordial Sea / Origin Pulse: the flood-sea pours in (also from the Superbloom) | `[150, 210, 255]` sea |
| DESERT / FLOODED_DUNES -> GLASS_DUNES | the hottest Fire moves (Blue Flare) glass the sand | `[235, 255, 240]` white-hot, green-tinged |
| GLASS_DUNES -> FLOODED_DUNES | heavy rain, Origin Pulse ×2, floods ×3: the sea breaks back over the glass | `[150, 210, 255]` sea |
| GLASS_DUNES -> DESERT | 3 shatters: the glass breaks into glittering sand | `[230, 220, 190]` sand-dust |
| FLOODED_DUNES -> DESERT (stage 2) | the tide drains away and the wet sand blooms | `[200, 255, 170]` green |
| FLOODED_DUNES -> FROZEN_LAKE | big Ice moves freeze the flood | `:white` |
| GLASS_DUNES -> BLEED | two beam clashes tear the Imprints open (the WAR-1 dome) | `:distortion` (the existing ANY->BLEED rule covers it) |
| DESERT -> ASHEN_WASTE | **no longer used** (2026-11-19): a glassed desert is now GLASS_DUNES; Cinderglass is only the quenched volcano | — |
| ASHEN_WASTE -> VOLCANIC | eruption moves reopen the vents | `[255, 90, 20]` lava |
| ASHEN_WASTE -> WATER_SURFACE | big Water moves / heavy rain flood the glass basin | `[200, 220, 235]` steam |
| WILDFIRE -> MEADOW (from Embers) | rain, Grassy Terrain, growth moves | `[200, 255, 170]` green |
| CORROSIVE_MIRE -> WATER_SURFACE | Misty Terrain / Purify | `[180, 230, 255]` |
| CORROSIVE_MIRE -> WASTELAND | Fire burns off the bog gas | `[255, 140, 40]` |
| WATER_SURFACE -> FROZEN_LAKE | strong Ice moves | `:white` |
| WATER_SURFACE / UNDERWATER -> CORROSIVE_MIRE | Sludge Wave / Toxic | `[120, 40, 140]` |
| STORMFRONT -> RAINBOW | two Sunny Days break the storm | `[255, 245, 200]` |
| RAINBOW -> (field it came from, else MEADOW) | sand / hail / Defog | `:white` |
| MINDSCAPE / HOLLOW_CATHEDRAL -> INVERSE | Topsy-Turvy, reality-tearing moves | `:distortion` |
| INVERSE -> (field it came from, else MINDSCAPE) | Topsy-Turvy again | `:distortion` |
| SCRAPYARD -> FACTORY | Electric moves reboot the machines | `[255, 240, 120]` |
| SCRAPYARD -> WASTELAND | acid eats the scrap | `[120, 40, 140]` |
| FAIRY_TALE -> DRAGONS_DEN | the dragon wins the story | `[255, 110, 40]` |
| DRAGONS_DEN -> CAVE | Water/Ice cool the hoard cavern | `[200, 220, 235]` steam |
| DRAGONS_DEN -> FAIRY_TALE | Fairy moves turn it into a story | `[255, 210, 240]` |
| CAVE -> CRYSTAL_CAVERN | Power Gem / Diamond Storm | `[200, 240, 255]` |
| CAVE / MOUNTAIN / SNOWY_MOUNTAIN -> VOLCANIC | eruption moves | `[255, 90, 20]` |
| CAVE -> DRAGONS_DEN | Draco Meteor, dragon moves | `[255, 110, 40]` |
| COLOSSEUM / CRYSTAL_CAVERN / DARK_CRYSTAL -> CAVE | quakes, explosions | `[150, 120, 90]` dust |
| DARK_CRYSTAL -> CRYSTAL_CAVERN | light beams | `:white` |
| MOUNTAIN <-> SNOWY_MOUNTAIN | hail or Ice moves / sun or Fire moves | `:white` |
| BEACH -> WATER_SURFACE | tide (big Water moves, heavy rain) | `[150, 210, 255]` |
| WASTELAND -> MEADOW / FLOWER_GARDEN | Purify / Grassy Terrain | `[200, 255, 170]` |

Stage changes inside one field (Grand Stage applause, Neon Grid blackout, Desert bloom...) swap to the stage
key with the bridge's normal stage fade.

## 3. Where players will see each field most (from FIELD_DEFAULTS.yaml)

The number of maps (of 424) that default to each field. Fields that come up often are worth extra polish.
91 maps are NONE: no-battle interiors.

- Very common: CAVE 23, BLEED 21, GRAND_STAGE 21 (all of Crownhaven), HOLLOW_CATHEDRAL 18, SNOWY_MOUNTAIN 17,
  DESERT 17, SILKWOOD 15, STORMFRONT 14, FROZEN_LAKE 14
- Common: INVERSE 12, MINDSCAPE 12, NEON_GRID 11, MOUNTAIN 11, FLOWER_GARDEN 11, WATER_SURFACE 11 (plus every
  surf and fishing battle), VOLCANIC 10, DRAGONS_DEN 10, FAIRY_TALE 10, NEW_MOON 9, CORROSIVE_MIRE 9,
  ASHEN_WASTE 8, FACTORY 8, BEACH 7
- Early game first impressions: BEACH (Ferrow's Landing, Saltmere), MEADOW (Routes 1-3: the first wild battles),
  SILKWOOD (Briarwick, Gossamer Wood, Loomhouse Gym), GRAND_STAGE (Pell Playhouse), WATER_SURFACE (Ebbmouth, Tidelock Gym)
- Mostly reached by transition: WILDFIRE (0 maps), MEADOW (5), RAINBOW (2), PRISM_ARENA (1), UNDERWATER (3, plus diving)

## 4. Bridge profile suggestions for the two war fields (2026-11-19, field workstream)

The bridge config is the bridge owner's; these are suggestions only. Until `field_flooded_dunes` / `field_glass_dunes`
art exists, the bridge's fallback room shows (DEFAULT_PROFILE), so a profile with a good fallback matters.
- **`:FLOODED_DUNES`**: `:fallback => { "backdrop" => "Sand", "sky" => true }`, `:outdoor => true`,
  `:art_extras => { "water" => true }`, `:tone => [-20, 0, 25, 20]` (cold sea light over the sand),
  `:transition => [150, 210, 255]`; fx: a `:drift` of spray (`:dot`, white/pale blue, `:dir => 1`) and a `:twinkle` of
  wave glints low in the room (`:area` on the lower half), like WATER_SURFACE's.
- **`:GLASS_DUNES`**: `:fallback => { "backdrop" => "Sand", "sky" => true }`, `:outdoor => true`,
  `:tone => [-35, 0, -20, 40]` (dark bottle-green glass), `:transition => [235, 255, 240]`; fx: a `:rise` of steam
  (`:puff`, the existing `STEAM` colours, slow, `:layers => [:back, :mid]`) and a `:twinkle` of glass glints
  (`:spark`, white and pale green, `:blend => 1`).
- Layout: the war boss fights (Reshiram / Kyogre) start on DESERT and change twice, so the stage-1 art of all
  three should share one horizon line.

