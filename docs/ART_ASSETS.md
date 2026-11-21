# Prismfall — Field Battle Art (backdrops, bases, layers)

This lists every graphic the field system can use, per field, with sizes, file names and a short art brief.
You can source or commission it all from this list.
**Nothing here is required to play**: a field without art falls back to a tinted stock EBDX room with its
particle FX (`Plugins/Prismfall EBDX Bridge/001_Bridge_Config.rb`, `:fallback` + `:tone`).
Add art in any order.

## 0. Status (Revision 10): every field and stage has shipped art

All 35 fields and their stages (51 field/stage rooms, plus night variants) have finished backdrops. They live in the kit folder
**`graphics/EBDX/Battlebacks/`** (`battlebg/` rooms, `elements/` animated layers), which `tools/package.sh` copies to
`Graphics/EBDX/Battlebacks/` in the dev kit. Real-engine stills: `docs/battle_captures/backdrops/contact_sheet.png`.

- **Build:** `python3 -I art/battlebacks/build_backdrops.py [FIELD ...]` composes every room from the Rejuvenation /
  Reborn / Desolation battlebacks plus procedural props, and writes the generated bridge file
  `Plugins/Prismfall EBDX Bridge/006_Bridge_Art.rb` and the per-file table in `docs/CREDITS.md`.
- **HD rooms:** each room also ships as `battlebg/<bd>_hd.png`, **864 x 693** (the room at EBDX's 2.25 scale). The
  bridge draws it as a flat EBDX layer at 1/2.25 zoom, so the default camera shows it 1:1 (crisp pixel art). The
  default camera shows HD x 158-670, y 150-534; the foe stands at HD (526, 342), the player at (261, 567).
  `<bd>.png` (384 x 308) is the same picture downscaled (EBDX void colours, fallback).
- **Animated layers:** per field, EBDX's own keys (scrolling strips, bubbles, lights, vacuum rings) under
  `:art_extras`, and bridge layers under `:layers` (pulse / flicker / sway / rotate / bob / drift / sheet frames),
  plus particle emitters (`:fx`, including `:puff` steam and smoke). Keys are documented in `001_Bridge_Config.rb`.
- **Stage keys with art:** `field_flower_garden_2..5`, `field_grand_stage_2/_3`, `field_neon_grid_blackout`,
  `field_desert_bloom`, `field_mindscape_nightmare`, `field_hollow_cathedral_consecrated`, `field_new_moon_abyss`,
  `field_new_moon_lamplight`, `field_dragons_den_wyrmfire`, `field_wildfire_embers`. New fields: `field_wildfire`,
  `field_meadow`, and the Ch19 war fields `field_flooded_dunes` / `field_glass_dunes` (the DESERT room flooded, then
  glassed: same dunes, horizon and platform spots; `art/battlebacks/fields_g.py`). `field_ashen_waste` is now **Cinderglass** (Volcanic's layout quenched to black glass).
  CAVE 2 and COLOSSEUM 2 have bridge-side art (`field_cave_cracked`, `field_colosseum_frenzy`): their field
  definitions carry no stage key, so the bridge profile names it (`:stages => { 2 => { :backdrop => ... } }`).
  Night variants: `field_frozen_lake_night` (aurora), `field_meadow_night`.
- **Sources beyond the three games** (all already on disk in `/home/claude/ref/art/morgebby/`, credited per file in
  `docs/CREDITS.md`): Magiscarf "Fields Backgrounds" (MEADOW); aveontrainer's painted battle backgrounds (DESERT dunes,
  MOUNTAIN highland falls, WASTELAND dead-tree mire); carchagui's cave background (CAVE earth panel, SNOWY_MOUNTAIN
  snow panel); princess-phoenix's arena panel (PRISM_ARENA). Rejuvenation's painted night plaza (NEW_MOON) and
  Darchlight path (INVERSE) replaced their procedural bases.
- **Checked online and not usable:** Eevee Expo 654, 1517, 1668 are Fakemon battler packs (no backgrounds); 40 is a
  tutorial; everblack's itch.io pack is generic-RPG battlebacks (off-style). Judged off-style earlier in
  `art/tilesets/NEW_SOURCES.md`: ORAS/XY EBDX packs, Orre battlebacks.
- **Not made:** vanilla (non-EBDX) `_bg/_base0/_base1/_message` sets.

The sections below are the original brief, kept for anyone repainting a room by hand.

## 1. Formats

### EBDX (primary — this is what players see)
Each field's art lives in `Graphics/EBDX/Battlebacks/` and uses the field definition's `:backdrop` name `<bd>`.

| File | Size | Required? | Notes |
|---|---|---|---|
| `battlebg/<bd>.png` | **384 × 308** | yes (else the fallback room is used) | The whole "room": sky/walls **and** floor with both battle platforms painted in. EBDX scales it ×2.25 (`ROOM_SCALE`) and pans/zooms it with the camera, so paint at native pixel size, Gen 5 style. Keep important detail away from the outer ~40 px. |
| `battlebg/<bd>_night.png` | 384 × 308 | optional | Used at night, outdoor fields only (marked 🌙 below). |
| `base/<bd>.png` | **384 × 182** | optional | Ground overlay stamped onto the bottom of the room (EBDX `"base"`). Use it to vary the floor without repainting the room. |
| `elements/<bd>_fog.png` | ~708 × 120 (tileable horizontally) | optional | Scrolling semi-transparent front layer (mist, heat haze, spores). It's drawn in front of the Pokémon, so keep it faint and in the top half. |

**Platform placement:** battlers stand at room coordinates (x, y) from `PBS/EBDX/metrics.txt`.

| Battle type | Player side | Foe side |
|---|---|---|
| Single | ~(116, 244) in Prismfall rooms (EBDX's 116,252 raised by the Bridge) | ~(234, 152) |
| Double | (92, 240) and (192, 262) | (256, 164) and (198, 152) |

Paint platforms or clearings around those points: centre them there. The Bridge puts every battler's feet on
the point (`007_Bridge_Placement.rb`; floating species hover 20 px above it), so an off-centre base shows.
Size the player base 1.5x the foe base (`bblib.PLAYER_SCALE`; HD foe 116x25 radii -> player 174x37.5): the send-out
pull-back shows it whole.
Every field also gets **particle FX** drawn by the bridge. It generates the shapes itself, so no art is needed.
Battle weather (rain, sun, sand, hail, fog) comes from EBDX's own weather layers.

**Format:** PNG, RGBA or indexed. Avoid alpha in the room image's corners: EBDX samples pixels (0,0) and (0,307)
to fill the void around the room.

### Vanilla Essentials (only if you run without EBDX)
Files go in `Graphics/Battlebacks/`, sized like the stock `field_*` set:

| File | Size |
|---|---|
| `<bd>_bg.png` | **512 × 288** |
| `<bd>_base0.png` (player platform) | **512 × 64** |
| `<bd>_base1.png` (foe platform) | **256 × 128** |
| `<bd>_message.png` (message bar) | **512 × 96** |

Optional `_eve` / `_night` variants work as in vanilla.

## 2. File names

The names below are the definitions' `:backdrop` values. The ones marked ✓ are already registered in
`Plugins/Prismfall Field Effects/1NN_Field_*.rb`. The rest follow the team convention `field_<snake_id>`
(FIELD_API §11); check the definition when it lands.

**FLOWER_GARDEN** has 5 stages. Each stage may declare its own `:backdrop`, e.g. `field_flower_garden_2`…`_5`;
check the definition for the exact names. A stage without its own art reuses the stage-1 art.

## 3. Per-field list and art direction

Legend: 🌙 = outdoor field, so `_night` variants are worth making. FX = what the bridge animates on top, so don't paint it.

### Gym fields

| # | Field | `<bd>` | Fallback until art exists | Art direction |
|---|---|---|---|---|
| 1 | SILKWOOD | `field_silkwood` ✓ | Forest, mossy tint | Old-growth Briarwick forest hung with silk curtains between trunks. Dew-beaded webs catch the light. Silk-wrapped stump platforms. Soft green-gold canopy light. *FX: drifting silk threads, spores.* |
| 2 | GRAND_STAGE | `field_grand_stage` ✓ | EBDX "Stage" | Saltmere's opera house from the stage: red velvet, gilt boxes, footlights, a painted backdrop flat. The player stands on the boards, the foe under a spotlight. *FX: confetti; EBDX spin/stage lights.* |
| 3 | WATER_SURFACE | `field_water_surface` ✓ 🌙 | EBDX "Water" | Ebbmouth's flooded harbour at high tide: open water to the horizon, drowned pilings, floating buoy platforms. Northern-coast palette (cold teal, white spray). *FX: sun glints; EBDX water shimmer.* |
| 4 | NEON_GRID | `field_neon_grid` ✓ | EBDX "Net", blue tint | Lumen City arena floor, a glowing cyan circuit grid; holo-billboards and an airship silhouette behind. Clean Piltover-style chrome. *FX: rising sparks, neon flickers, faint flashes.* |
| 5 | DESERT | `field_desert` ✓ 🌙 | EBDX "Sand", warm tint | Duneholt dunes under a white-hot sky, canyon walls in the distance, half-buried ruins. Flat sandstone slabs as platforms. *FX: blowing sand.* |
| 6 | CORROSIVE_MIRE | `field_corrosive_mire` ✓ | Forest, purple tint | Mirefen runoff marsh below the Undercity: violet-green sludge, rusted drain pipes, dead reeds, a sickly lamp glow. *FX: rising toxic bubbles.* |
| 7 | VOLCANIC | `field_volcanic` ✓ | EBDX "Magma" | Cindervault caldera: basalt shelves over a lava river, a glowing magma crust, dragon-lord banners on obsidian pillars. *FX: embers, ash.* |
| 8 | COLOSSEUM | `field_colosseum` | EBDX "Net" crowd, warm tint | Ironreach pit-fighting ring in an old mine shaft: a chain-link fence, a packed crowd on scaffolding, hanging work lamps, a sand floor. *FX: dust motes.* |
| 9 | FLOWER_GARDEN (×5) | stage 1 `field_flower_garden` 🌙, stages 2–5 per the definition | Outdoor field + tall grass | Verdance's terraced garden. Stage 1: bare beds with buds. 2: sprouts. 3: blooms. 4: full flowering with arches. 5: an overgrown riot of colour with a giant bloom behind the foe. Keep the composition identical across stages so the swap reads as growth. *FX: petals and pollen that increase each stage.* |
| 10 | FROZEN_LAKE | `field_frozen_lake` 🌙 | EBDX "Snow", cool tint | Rimeholt's frozen lake: thick blue ice with cracks, pines and fjord cliffs, the aurora at night. Ice-floe platforms. *FX: snowfall, ice glints.* |
| 11 | STORMFRONT | `field_stormfront` 🌙 | EBDX "Sky", dark grey | Skyreach airship spire deck above the clouds in a storm: anvil clouds, rigging, a wind-torn pennant. Platforms are deck plates. *FX: rain and wind streaks, lightning flashes.* |
| 12 | MINDSCAPE | `field_mindscape` | EBDX "Dimension", violet | Lucent's psychic dreamscape (Umbra): a floating library, mirrored stairs, impossible geometry, a pastel-violet void. *FX: thought-motes; EBDX vacuum rings.* |
| 13 | CRYSTAL_CAVERN | `field_crystal_cavern` | EBDX "Cave", teal tint | Cragholm geode cavern with huge prismatic crystal clusters, lit from inside. Crystal-ringed platforms. *FX: crystal glints.* |
| 14 | HOLLOW_CATHEDRAL | `field_hollow_cathedral` | EBDX "Champion" pillars, dark purple | Gravenmoor's ruined cathedral: broken stained glass, pews, a candle-lit altar behind the foe, moonlight shafts. *FX: will-o'-wisps, dust in the light shafts.* |
| 15 | FACTORY | `field_factory` | EBDX "IndoorA", grey | Cogsworth foundry: conveyor lines, crucibles pouring molten steel, giant gears, catwalks. Steel-plate platforms. *FX: steam, falling sparks.* |
| 16 | NEW_MOON | `field_new_moon` | EBDX "Darkness" | Underveil's heart: a black sky with a dark moon and starfield over undercity rooftops, faint violet rim light. *FX: stars, shadow motes; EBDX dark rings.* |
| 17 | FAIRY_TALE | `field_fairy_tale` | Forest, pink tint | Gloaming: a storybook castle glade in the forest heart, giant mushrooms, a fairy-ring stone circle, warm twilight. *FX: sparkles.* |
| 18 | DRAGONS_DEN | `field_dragons_den` | EBDX "Magma", purple | Wyrmrest lair: dragon bones and a treasure hoard on a magma-lit cavern floor, carved wyrm statues. *FX: violet-orange embers, gold glints.* |

### Story / route fields

| Field | `<bd>` | Fallback | Art direction |
|---|---|---|---|
| CAVE | `field_cave` | EBDX "Cave" | Generic Velmoran cave: damp stone, stalactites, a lantern-lit path. *FX: dust.* |
| MOUNTAIN | `field_mountain` 🌙 | EBDX "Mountain" | Highland ridge: wind-bent pines, distant peaks, rocky ledges. *FX: wind streaks.* |
| SNOWY_MOUNTAIN | `field_snowy_mountain` 🌙 | EBDX "Snow" | Glaciem summit in a blizzard, cornices, prayer flags. *FX: heavy snow.* |
| BEACH | `field_beach` 🌙 | Sand + water | Southern coast (Ferrow's Landing): sand, tide pools, a ferry pier on the horizon. *FX: sun glints; EBDX water.* |
| UNDERWATER | `field_underwater` ✓ | EBDX "Underwater" | Kelp-forest sea floor with ruins, god rays from above. *FX: plankton; EBDX bubbles, light shafts.* |
| RAINBOW | `field_rainbow` 🌙 | EBDX "Sky", bright | A cloud field under a full double rainbow, prismatic mist. *FX: prismatic sparkles.* |
| WASTELAND | `field_wasteland` 🌙 | Sand, sick grey | Bleed-scarred dump: barrels, slag, dead trees, a jaundiced sky. *FX: toxic bubbles, ash.* |
| ASHEN_WASTE | `field_ashen_waste` ✓ | Cave, grey | VOLCANIC after quenching: cooled black rock, steam vents, falling ash. **Same layout as VOLCANIC** so the transition reads as the same place. *FX: heavy ash, steam.* |
| DARK_CRYSTAL | `field_dark_crystal` | Dark cave | CRYSTAL_CAVERN darkened: **same layout**, crystals gone obsidian-violet, light dead. *FX: violet glints; EBDX vacuum.* |
| SCRAPYARD | `field_scrapyard` | IndoorA, rust | FACTORY wrecked: **same layout**, collapsed gantry, fires out, scrap piles. *FX: smoke, sparks.* |
| INVERSE | `field_inverse` ✓ | Dimension, greyscale | Umbra's mirrored realm (Distortion World cue): upside-down terrain, floating islands, inverted colours (paint it as a negative image, since EBDX can't invert at runtime). *FX: upward "snow".* |
| BLEED | `field_bleed` ✓ | EBDX "Darkness", red | The corruption: torn reality, red-cyan chromatic aberration, shards of other fields bleeding through. *FX: glitch shards, distortion transition, flashes. Borrowed fields' FX appear on top as BLEED rotates them.* |
| PRISM_ARENA | `field_prism_arena` | EBDX "Champion" | Crownhaven Festival finale: a colossal arena with the 18 Plates hung in a ring overhead, prismatic floor sigil. *FX: prismatic sparkles; borrowed gym FX appear as it cycles.* |

**Transitions to keep visually consistent** (same camera framing and platform positions):
VOLCANIC↔ASHEN_WASTE, FROZEN_LAKE→WATER_SURFACE, WATER_SURFACE↔UNDERWATER, CRYSTAL_CAVERN→DARK_CRYSTAL,
FACTORY→SCRAPYARD, and FLOWER_GARDEN stages 1–5.

## 4. Optional EBDX extras per field

- Any EBDX room key can be added to a field's `:art_extras` in the bridge config:
  - `"sky" => true` animated sky with clouds, sun and stars. It is drawn **over** the top ~105 px of the room, so keep your horizon and skyline below that line.
  - `"lightsA"` / `"lightsB"` / `"lightsC"` stage, disco or ambient light shafts.
  - `"water" => true` water shimmer.
  - `"vacuum"` dark rings.
  - `"imgNNN" => { :bitmap => ..., :scrolling/:sheet/:rainbow/:effect => ... }` your own animated layers from `elements/`
    (see the [EBDX environment docs](https://luka-sj.com/essentials/resources/EBDX/docs?page=24)).
    Prismfall adds `:parallax => [px, py]` (the layer follows the camera by that fraction, for far sky layers).
- **Clouds and other sky layers go behind the scenery.** An `img` strip only sits above or below the *whole* room
  bitmap, so a cloud strip over the room crosses every tree and mast painted into it. Split the room instead
  (`art/battlebacks/skies.py`): room at z 0, the scrolling sky strip at z 0 (drawn after it), and a sky-less
  cut-out of the room (`pf_<field>_front`) at z 1 above both. MEADOW and STORMFRONT work this way.
- **Don't mirror scenery above the horizon.** The top margin of an extended room is on screen whenever EBDX's camera
  pulls back (intro, send-out). Continue the sky there (`skies.extend_with_sky`) or paint what belongs above the
  frame (MEADOW: the oak's crown), never an upside-down copy of the source. For a new panel, add a plan to
  `art/battlebacks/fields_i.py` (keyed by the md5 of the panel's pixels): it paints the top margin and the side
  margins' upper rows from the panel's own pixels (`margins.py`: patch quilting with a material layout, patches
  copied, never flipped), or repeats a built structure upright, or continues a gradient sky. The opening close-up
  (ENEMY camera) also shows ~45 px past the panel's right edge; the send-out pull-back shows HD x 4..668, y 23..633.
- **Layers over the room bitmap cross everything painted in it.** A full-width scrolling strip (foam, mist) that
  should stay behind a painted object needs a cut-out of that object above it (MOUNTAIN: `pf_mountain_crags`
  over the foam strip).
- With a `*_night` room, any `:art_extras` or `:layers` element that has a `<bitmap>_night.png` uses it.
- Trainer intro backgrounds are a separate EBDX feature (`Graphics/EBDX/Transitions/`). They aren't needed for fields.

## 5. Asset checklist

- [ ] Gym fields: 18 rooms (plus FLOWER_GARDEN stages 2–5, 4 more rooms)
- [ ] Route/story fields: 13 rooms
- [ ] 🌙 night variants: 10 optional
- [ ] Vanilla `_bg/_base0/_base1/_message` sets: only if you ship without EBDX
