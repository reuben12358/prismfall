# WORLD_MAP — the geography of Velmora

Owner: world cartographer. SPINE Revisions 9, 13, 14 and **18 (Geography v2: Elowen in the middle; the war on land in
Ossaria)**. Images: **`art/previews/world_map.png`** (painted region map) and
**`graphics/UI/Town Map/prismfall_velmora.png`** (the in-game Town Map, 480×320). Both are drawn by
`python3 -I tools/worldmap/gen_world_map.py` from `tools/worldmap/world_geo.py` (coasts, mountains, rivers, the war
front) and `tools/worldmap/world_data.py` (towns, roads, squares, borderlands). Roads in detail: `design/ROUTES.yaml`
and WORLD.md §11. Names: `design/PLACE_NAMES.md`. Story lines that Geography v2 made wrong:
`design/GEOGRAPHY_V2_STORY_FIXES.md`.

Coordinates below are **town-map squares** (x 0–29 east, y 0–19 south), the same grid as `pbs/town_map.txt`.
One square is roughly six leagues, a long day's walk. The continent is about 27 squares across and 19 from the north
coast to the Hallow Strait.

---
## 1. The shape of the land

Velmora is one broad continent. **Elowen's green country fills the middle**, and the **Crownwall**, a ring of white
peaks, stands at its heart (14.5, 9.5) with Crownhaven inside it. The bone sands of **Ossaria** run along the whole
north coast. **Isenmar** holds the west and north-west, where the sea itself is frozen. **Ashkaar's** volcanic
highlands fill the east. In the south rises the **Zenith Plateau**, the City Above, with **Nadir** beneath it and
drowned Aurelia under its south cliff. The narrow Hallow Strait in the south is the only way most foreigners arrive.

| Sea or coast | Where | Character |
|---|---|---|
| **The Northern Sea** | the whole north coast, y 0–1 | Open, grey water off Ossaria's dunes and the Crags. West of x ≈ 9.6 it is frozen: that is Isenmar's sea. No war is fought on it. |
| **The frozen sea** | the west and north-west, x 0–9 | Frozen solid since AF 0 (the Icicle Plate fell into it). It *is* Isenmar: Rimeholt stands on Lake Rime, an inlet of it, and the Thane's sled-road runs along its shore east to the Mast Glacier. |
| **The Western Deep** | the west coast below the ice, x 0–2 | Deep cold water. The coast runs from Saltmere's salt flats north through the frost-flats of the Frostflat Causeway, the Rimewood's frozen shore, the sea cliffs of Gullcry and the Ebb estuary to the fjords below Rimeholt. A coast packet links Saltmere and Ebbmouth by sea. |
| **The Ember Sea** | the east coast, x 27–29 | Warm, dark water under Ashkaar's basalt cliffs; the Dragonback runs along the shore, and Cinder Cape is its north-east tip. |
| **The Hallow Strait** | the south, y 18–19 | The ferry sea. The *Dovetail* crosses it in the prologue (the last civilian crossing). Chalk cliffs west of Ferrow's Landing (Lacecliff Walk), dunes and a salt lagoon at Saltmere. Under Zenith's south cliff the sea covers **drowned Aurelia** (the Fault drains it in Act III). The **Shardfall Isles** (postgame) lie off the Gloamwood, x 20–24. |

## 2. Highlands

| Range | Where | What it is |
|---|---|---|
| **The Zenith Plateau** and **the Escarpment** | x 15–21, y 14–18 | A raised tableland, the City Above. Its edge is a cliff all round: the north face sheds the Outfall into Mirefen's marsh, Ironreach and the Long Drop sit under its north-west rim, the west face (the Escarpment) looks over the Gossamer, and the south face drops into the sea at Underveil (the Hanging Stair goes down it). Lumen City stands on its south brink, Skyreach (airship spire) on the north-east, Cogsworth (foundries) on the east rim, and the Slag Mesa spills off its east side. |
| **The Crownwall** | a ring around (14.5, 9.5), about three squares across | White peaks, unclimbable except at the one gap on the east side, where Sovereign's Ascent climbs in from the Pilgrim Pass. The Crown Road circles it outside. |
| **The Frostfang Mountains** | x 4–8, y 3–6 | Isenmar's spine between the Ebb and Rimeholt. The Frostfang Pass and the Whalebone Road (Road 10) cross them; the Mast Glacier spills off their north-east end. |
| **The Crags of Ossaria** and **the Jawbone Ridge** | x 19–23, y 1–3 | Red rock on the north coast; Cragholm's lift-galleries; a toothed ridge running south to Vigil, with the Darkglass Mine in it. |
| **The Kneeling Stones** | x 18–19, y 4–5 | A low ridge of fossil vertebrae where the River Leach rises. |
| **The Cinderhorn** and **the Dragonback** | the Cinderhorn (25.7, 10.3); the Dragonback x 26–27, y 5–8 | Ashkaar's volcano south-east of Cindervault, and the ridge along the east coast. Lava veins, cinder cones, dragon roosts. |
| **The Wyrmspine** | x 23–25, y 13–15 | The ridge Wyrmrest stands on; Road 18 climbs it from the Thornwar Marches. |
| **The Spinners' fells** | x 9–10, y 12 | Sheep hills north of Briarwick (Spinners' Rise, Road 3). |

## 3. Rivers and lakes

| Water | Course |
|---|---|
| **River Ebb** | Rises on the Crownland downs west of the Crownwall (11, 8), runs west over the frozen falls of **the Icefall Locks**, through Brassfall and the Reedholms delta to **Ebbmouth**. Its current runs both ways (the Splash Plate). |
| **River Selvedge** | Rises in the Gossamer Wood, runs south-west past Thistledown Lea and through the Dyers' Ford (red, blue and yellow below the dye-works) to the **Saltmere Lagoon**. The Weavers' Road (Road 2) follows it. |
| **The Prism** | From Mirror Mere south past the Crownwall's west side over **Prism Falls** (the rainbow that never stops) into the Gossamer, where it joins the Selvedge. |
| **River Leach** | From the Kneeling Stones south through the Leach Canyons and Wormwood Lea, clean until it reaches the plateau, then over **the Gutterfall** into Mirefen's marsh, where Nadir's runoff turns it blue. |
| **The Outfall** | Zenith's waste water, down the plateau's north face into Mirefen. |
| **Spinefall** | From the Crags south over the fossil spine of Spinefall Gorge into the desert sinks near Vigil. |
| **Gloam Water** and **the Thornrun** | South through the Gloamwood and the Thornwar Marches to the Hallow Strait. |
| **The Blindwater** | Underground. It leaves the sea at Underveil through **the Throat**, runs east beneath the plateau's south cliff (Mothwell's lamps light it) and comes back into the light at the **Gloamwood Verge**. Road 17 is a boat journey along it. Drawn dotted. |
| **Lake Rime** | The frozen inlet Rimeholt is built on; the Ice Vault (Kyogre) lies beneath. |
| **Lake Sallow** | One great sulfur hot spring on the Elowen/Ashkaar border, north-east of Mirefen; Lantern Isle steams in the middle. Road 7 crosses it (Surf). |
| **Mirror Mere** | A small silver lake in the Looking-Glass Wood, north-west of the Crownwall: gate A into Antumbra. |
| **Saltmere Lagoon** | The salt lake behind Saltmere's sandbar, fed by the Selvedge; the Grey Saltings' pans line it. |

## 4. The kingdoms

| Kingdom | Where | Land | Seat and gym towns (gym #, Revision 14) |
|---|---|---|---|
| **Elowen, the Evergreen Crown** | the middle, from the south-west coast to the Gloamwood in the south-east; borders every kingdom | Oldwood, orchards, river meadows, chalk coast and the Crownland downs round the Crownwall. The Gossamer Wood (silk) in the south-west; the Gloamwood (permanent dusk) in the south-east. | **Verdance** (seat, 9) · Saltmere (1, free port) · Briarwick (2) · Gloaming (17) · Ferrow's Landing (start) |
| **Isenmar, the Frozen Sea** | the west and north-west | Snowfields, pine, fjords and sea-ice. | **Rimeholt** (seat, 10) · Ebbmouth (3) · Skaldfast (border fortress on Ossaria's west edge, war) |
| **Ossaria, the Bone Sands** | the north, along the whole north coast | Sand, canyons, fossil beds, tombs, the Crags. Neutral ground: the war is fought in its western dunes. | **Duneholt** (seat, 5) · Cragholm (13) |
| **Ashkaar, the Dragonfire Dominion** | the east | Basalt, ash plains, the Cinderhorn, dragon ridges, from Cinder Cape in the north-east down the Wyrmspine. | **Cindervault** (seat, 7) · Wyrmrest (18) · Cinder Cape Warfort (war) |
| **Zenith, the City Above** | the plateau in the south | Brass, white stone, rail and pylons; airships. | **Lumen City** (seat, 4) · Skyreach (11) · Cogsworth (15) |
| **Nadir, the City Below** | beneath the plateau, same footprint: the marsh and mines at its foot and the undercity under its south cliff | Marsh, slag, mine shafts, a sea-drowned city. | **Underveil** (seat, 16, in drowned Aurelia's towers) · Mirefen (6) · Ironreach (8) |
| **Antumbra, the Kingdom Behind the Glass** | nowhere on the real map: the inset in the south-east sea | The mirror realm: inverted desert hanging in the sky, shadows falling toward the light. | **Lucent** (seat, 12) · Gravenmoor (14) |
| **Crownhaven** | inside the Crownwall at Velmora's centre, on Elowen ground | The Accord's capital and the Festival grounds. | **Crownhaven** (the Festival) |

## 5. Borders and borderlands

Kingdoms touch **only** through borderlands (Revision 9), each with a town where the two peoples live together. On the
map the borderlands are the mottled ground where both kingdoms' colours mix; the dashed red line marks kingdom edges.
The records (biome, landmarks, wild mix, member maps) are `BORDERLANDS` in `world_data.py`, copied into maps.json and
WORLD.md §10.

| Code | Borderland | Between | Where (squares) | Town |
|---|---|---|---|---|
| A | The Rimewood | Elowen / Isenmar | the west coast between Briarwick and Ebbmouth, x 5–8, y 10–14 (the Frostflat Causeway runs on down the coast to Saltmere) | Frostwick (6, 12) |
| A2 | The Hoarwood | Elowen / Isenmar | x 5–6, y 8–9 | Snowbriar (5, 8) |
| B | The Icefall Locks | Isenmar / Elowen | the Ebb's frozen falls, x 4–8, y 6–7 | Brassfall (7, 7) |
| B2 | The Mast Glacier | Isenmar / Ossaria | tundra and permafrost dunes, x 6–8, y 2–3 | Anchorhold (8, 3) |
| C | The Brass Dunes | Elowen / Ossaria | north of the Crownwall, x 14–15, y 4–5 | Copperdune (15, 5) |
| D | The Leach Canyons | Ossaria / Elowen | x 19, y 5–6 | Charwell (19, 6) |
| E | The Sulfur Reach | Elowen / Ashkaar | Lake Sallow and the Ironway, x 20–23, y 7–10 | Scaldwater (23, 9) |
| F | The Rootdeep | Nadir / Elowen | the plateau's foot: the Rootdeep (x 13–14, y 12–13), the Gutterfall (20, 12), the Long Drop (16, 12), the Blindwater (x 18–19, y 18) | Lanternroot (12, 12), Mothwell (21, 18) |
| G | The Wired Wood | Zenith / Elowen | the plateau's north and west foot: the Wired Wood (18, 12), the Meridian Mainline (17, 13–15), the Arc-Lamp Mile (x 14–15, y 14–15), the Slag Mesa (21, 14) | Verdigris (17, 11) |
| H | The Looking-Glass Wood | Elowen / Antumbra | round Mirror Mere, x 10–11, y 6–7 | Glassmere (11, 6) |
| I | The Obsidian Barrows | Antumbra / Ossaria | x 20, y 3–4 | Vigil (20, 3) |
| J | The Thornwar Marches | Elowen / Ashkaar | x 23, y 15–16 | Thornwatch (23, 15) |
| K | The Pilgrim Pass | Elowen / Crownhaven | from the Dominion's toll-fort west to the Crownwall's gap, x 18–22, y 10–12 | Pilgrim's Rest (18, 10) |
| L | The Hanging Stair | Zenith / Nadir | the plateau's south cliff, x 18–19, y 16–19 | Midstair (19, 17) |
| M | The Cinderglass Barrens | Ashkaar / Ossaria | volcanic ash desert, x 23–24, y 4–6 | Glasswake (23, 4) |

**Fire and ice never border.** Isenmar's land is the west; Ashkaar's is the east. Between them lie Elowen and Ossaria,
and the two meet only as armies, on Ossaria's sands (§7). Zenith and Nadir border Elowen only (Nadir also touches
Zenith, vertically).

Not adjacent (by design): Isenmar–Ashkaar, Isenmar–Zenith/Nadir, Ossaria–Zenith/Nadir, Ashkaar–Zenith/Nadir,
Crownhaven with anything but Elowen. Antumbra touches the mainland only at its three gates.

## 6. Roads, sea lanes and air lanes

- **The Eighteen Roads** join the gym towns in badge order; **the Pilgrim Road** (Road 19) goes in to the Crown. Each
  road is two to six named maps (WORLD.md §11). On both maps a numbered shield marks each road.
  The early chain (Revision 14, unchanged by v2): Ferrow's Landing → **the Strand Road** west along the chalk coast →
  **Saltmere** → **the Weavers' Road** inland up the Selvedge → Gossamer Wood → **Briarwick** → **the Hoar Road** north
  over the fells, through Frostwick and the Rimewood, down Gullcry Cliffs → **Ebbmouth**. The Frostflat Causeway along
  the coast closes the loop from Frostwick back to Saltmere.
- **The Crown Road** circles the Crownwall on Elowen ground: Wallshadow Row (west and south), Candle Down (east), the
  Highwold (north), Kingsmead (north-west), with Coppice Ride linking it west to the Icefall Locks. Every road in
  Velmora ends on it; Roads 4, 5, 8 and 12 run along part of it, and only Road 19 goes in. It is how the gym order
  crosses Elowen between kingdoms that do not touch (WORLD.md §10, "Elowen in between").
- **Side roads:** Windfall Row (orchards, Chapter 1), the Frostflat Causeway, the war road north from Cindervault
  (the Cinderglass Barrens, Glasswake, the Wyrmtongue to Cinder Cape).
- **Sea lanes:** the Last Ferry (the *Dovetail*, into Ferrow's Landing), the coast packet (Saltmere ↔ Ebbmouth), the
  Strait ferry to the Shardfall Isles (postgame). **On the ice:** the Thane's sled-road from Rimeholt east along the
  frozen coast to the Mast Glacier.
- **Air lanes** (Act III, Skyreach airships): Anchorhold ↔ Skyreach (Road 11's air leg, drawn as an outlined dashed
  line: Isenmar and Zenith share no border), Skyreach ↔ Lumen.
- **Underground:** the Blindwater (Road 17).

## 7. The war in the sands (Revision 18)

The Ashkaar–Isenmar war is fought **on land, in Ossaria's western dunes**, neutral ground that both armies march into.
- **Isenmar's host** comes from the west: Rimeholt → the Thane's Sled-Road → over the Mast Glacier → **Skaldfast**
  (9, 2), Isenmar's border fortress on Ossaria's west edge → the white trench-lines of **the Rimed Sands** (11, 2).
- **Ashkaar's legions** come from the east: Cindervault's north gate → the Cinderglass Barrens → Glasswake → west
  across the bone sands → **the Ashkaar Siege Camp** (15, 2). **Cinder Cape Warfort** (26, 3) is their staging fortress
  on Ashkaar's own north-east coast, behind the lines.
- **The Steamline** (12, 1) is the steam-glass strip where the two Imprints meet: ice on one side, fire on the other.
- **The Glass Dunes** (13, 2) are the battlefield. In the climax Primal Kyogre drags a flood-sea into the desert and
  Reshiram's fire turns the dunes to glass.
- On the world map: blue march arrows (Isenmar) and red march arrows (Ashkaar) converge on a glowing jagged front line
  at x ≈ 13, crossed swords mark the Glass Dunes, and the camps are flagged. The Town Map shows the same front in pixels,
  and each war site has its own named point.
- Maps 920–927 (WORLD.md §9). Cragholm (Gym 13) is the nearest gym city to the front.

## 8. Crownhaven and the Festival grounds

Crownhaven sits in the bowl of the Crownwall at the centre of Velmora, on Elowen ground. Every kingdom's road ends on
the Crown Road outside the wall, but there is **one way in**: the **Pilgrim Pass**, which runs west from Dominar's
Toll at the Ashkaar border across Elowen ground (eighteen shrines, Pilgrim's Rest at its end), then **Sovereign's
Ascent** through the wall's one gap on the east side, and the Coronation Road down into the city. The Dominar still
holds the toll at the start of the only road in, which is the politics of the Festival in one fact.
Inside the ring: Lower Crownhaven (the Eighteen Gates face the Imprints, the Market Ring, the Pilgrims' Quarter), Upper
Crownhaven (the Basilica, the Accord Palace, the Concordance Spire) and the **Festival grounds** on the bowl's east
side, nearest the pass: the Processional Plaza, the **Temple-Arena of the Blessing** (Hall of Eighteen Doors, Altar
Stage) and the Court of Eight Pavilions. The Glassfall Scar lies on the inner slope of the north-west wall.

## 9. Antumbra

Antumbra has no place on the real map. Both images draw it as an **inset framed like a mirror** in the south-east sea.
Its three gates are marked A, B and C on the mainland and in the inset:
- **A, Mirror Mere** (Elowen, the Looking-Glass Wood, north-west of the Crownwall) → the Antumbra Threshold →
  Widdershins Walk → **Lucent**.
- **B, the Grave Glass** at Vigil (Ossaria) ↔ Yesterday's Road (from Lucent) and Hindmoor → Downflame Road →
  **Gravenmoor**.
- **C, the Slagglass** at the Slag Mesa (Zenith/Elowen, east of the plateau) ↔ the Noonless Road from Gravenmoor.

## 10. The in-game Town Map

`pbs/town_map.txt` (shipped as `PBS/town_map_prismfall.txt`) defines **region 0, Velmora**, with
`Filename = prismfall_velmora.png`. Every settlement, every road square, every named dungeon and every war site has a
`Point`; dungeons and districts show as the point of interest of their square. Every map has a `MapPosition`
(`mapgen/data/town_map_positions.json`, applied by `build.py`; maps.json `metadata.town_map_pos`). Fly spots exist for
the six built towns (their PC HealingSpots). `Prismfall Maps/009_TownMap.rb` compiles our file instead of the stock
one, whose Essen region 0 it replaces, and makes Fly read the live `HealingSpot` from map metadata. The UI draws the
480×320 graphic over `Graphics/UI/Town Map/bg.png`.

| Settlement | Square | | Settlement | Square |
|---|---|---|---|---|
| Ferrow's Landing | 12, 18 | | Verdance | 9, 10 |
| Saltmere | 6, 18 | | Rimeholt | 3, 2 |
| Briarwick | 11, 13 | | Skyreach | 19, 14 |
| Ebbmouth | 3, 7 | | Lucent (inset) | 28, 16 |
| Lumen City | 16, 16 | | Cragholm | 21, 2 |
| Duneholt | 17, 3 | | Gravenmoor (inset) | 27, 18 |
| Mirefen | 20, 13 | | Cogsworth | 20, 15 |
| Cindervault | 24, 8 | | Underveil | 16, 18 |
| Ironreach | 16, 13 | | Gloaming | 22, 17 |
| Crownhaven | 14, 9 | | Wyrmrest | 25, 13 |

Borderland towns, roads, dungeons and war sites: `design/PLACE_NAMES.md` (Square column) and `pbs/town_map.txt`.

## 11. Updating

1. Edit `tools/worldmap/world_data.py` (names, roads, squares, borderlands, the war) or `world_geo.py` (coast,
   mountains, rivers, the front's drawing).
2. `python3 -I tools/worldmap/gen_docs.py` → PLACE_NAMES.md, ROUTES.yaml, WORLD.md §11, town_map.txt, positions,
   maps.json, FIELD_DEFAULTS.yaml (new maps, renamed maps, spec fields). It is idempotent: a second run changes nothing.
3. `python3 -I tools/worldmap/gen_world_map.py` → both images (about half a minute).
4. If names changed: `python3 -I tools/rename_places.py` (dry run, read `tools/worldmap/last_rename.diff`), then
   `--apply` (it checks every .py and .rb afterwards and rolls back if anything broke).
5. `ruby tools/field_defaults_to_rb.rb`, then the map builder's `build.py`.
