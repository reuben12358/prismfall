# WORLD_MAP — the geography of Velmora

Owner: world cartographer. SPINE Revisions 9, 13 and 14. Images: **`art/previews/world_map.png`** (painted region map) and
**`graphics/UI/Town Map/prismfall_velmora.png`** (the in-game Town Map, 480×320). Both are drawn by
`python3 -I tools/worldmap/gen_world_map.py` from `tools/worldmap/world_geo.py` (coasts, mountains, rivers) and
`tools/worldmap/world_data.py` (towns, roads, squares). Roads in detail: `design/ROUTES.yaml` and WORLD.md §11. Names:
`design/PLACE_NAMES.md`.

Coordinates below are **town-map squares** (x 0–29 east, y 0–19 south), the same grid as `pbs/town_map.txt`.
One square is roughly six leagues, a long day's walk. The continent is about 26 squares across and 18 from the ice to the
Hallow Strait.

---
## 1. The shape of the land

Velmora is one broad continent shaped like a shield laid on its side, with its boss (the Zenith Plateau) north of centre
and a ring of mountains (the Crownwall) set into its south-east quarter. Ice closes the north, open ocean lies west and
east, and the narrow Hallow Strait in the south is the only way most foreigners ever arrive.

| Sea or coast | Where | Character |
|---|---|---|
| **The Frozen North Sea** | the whole north, x 0–26, y 0–2 | Frozen solid since AF 0 (the Icicle Plate fell into it). It *is* Isenmar: the kingdom's roads, fisheries and a capital-sized harbour (Rimeholt) stand on it. Floes, pressure cracks, the Thane's sled-road along it from Rimeholt to the Rime Isles. Off Underveil the ice gives way to the black water over **drowned Aurelia**. |
| **The Shattered Ice** | north-east, x 26–29, y 1–4 | The strait between Isenmar's **Rime Isles** (Skaldfast) and Ashkaar's **Cinder Cape**. Broken floes, steam where lava meets the sea. The Ashkaar–Isenmar war is fought here and only here: the two kingdoms share no land border. |
| **The Ember Sea** | the east coast, x 27–29 | Warm, dark water under Ashkaar's basalt cliffs; the Dragonback ridge runs along the shore. |
| **The Hallow Strait** | the south, y 18–19 | The ferry sea. The *Dovetail* crosses it in the prologue (the last civilian crossing). The **Shardfall Isles** (postgame) lie in it south of the Gloamwood. Chalk cliffs west of Ferrow's Landing (Lacecliff Walk), dunes and a salt lagoon at Saltmere. |
| **The Western Deep** | the west coast, x 0–2 | Deep cold water. The coast runs from Saltmere's salt flats north through the frost-flats of the Frostflat Causeway, the Rimewood's frozen shore, the sea cliffs of Gullcry and the Ebb estuary to the fjords below Rimeholt. A coast packet links Saltmere and Ebbmouth by sea. |

## 2. Highlands

| Range | Where | What it is |
|---|---|---|
| **The Zenith Plateau** and **the Escarpment** | x 8–17, y 1–6 | A raised tableland, the City Above. Its edge is a cliff all round: the north face drops into the sea at Underveil (the Hanging Stair goes down it), the west face is the frozen falls of the Icefall Locks, the south face sheds the Outfall into Mirefen. Lumen City, Skyreach (airship spire) and Cogsworth (foundries, east rim) stand on it. |
| **The Frostfang Mountains** | x 4–8, y 3–6 | Isenmar's spine between Rimeholt and the Ebb. The Frostfang Pass (Road 10) and the Mast Glacier (Road 11) cross them. |
| **The Crags of Ossaria** and **the Jawbone Ridge** | x 20–26, y 1–6 | Red rock on the north coast; Cragholm's lift-galleries; a toothed ridge running south to Vigil, with the Darkglass Mine in it. |
| **The Cinderhorn** and **the Dragonback** | x 24–27, y 6–13 | Ashkaar's volcano above Cindervault, and the ridge along the east coast. Lava veins, cinder cones, dragon roosts. |
| **The Wyrmspine** | x 21–25, y 16 | The ridge Wyrmrest stands on; Road 18 runs along its crest. |
| **The Crownwall** | a ring around (19.5, 14.5) | A ring of white peaks, unclimbable except at its one gap on the north-east side, where the **Pilgrim Pass** climbs from Ashkaar. Crownhaven sits in the bowl inside. |
| **The Spinners' fells** | x 9–10, y 12 | Sheep hills north of Briarwick (Spinners' Rise, Road 3). |

## 3. Rivers and lakes

| Water | Course |
|---|---|
| **River Ebb** | Off the Escarpment at the Icefall Locks, west through Brassfall and the Reedholms delta to **Ebbmouth**. Its current runs both ways (the Splash Plate). |
| **River Selvedge** | Rises in the Gossamer Wood, runs south-west past Thistledown Lea and through the Dyers' Ford (red, blue and yellow below the dye-works) to the **Saltmere Lagoon**. The Weavers' Road (Road 2) follows it. |
| **The Prism** | From Mirror Mere west over **Prism Falls** (the rainbow that never stops) and south into the Gossamer, where it joins the Selvedge. |
| **River Leach** | From the Kneeling Stones west through the Leach Canyons, glowing blue with Nadir's runoff, over the **Gutterfall** into Mirefen marsh. |
| **The Outfall** | Zenith's waste water, down the south face of the Escarpment into Mirefen. |
| **Spinefall** | From the Crags south over the fossil spine of Spinefall Gorge into the desert sinks near Vigil. |
| **Gloam Water** and **the Thornrun** | South through the Gloamwood and the Thornwar Marches to the Hallow Strait. |
| **The Blindwater** | Underground. It leaves the sea at Underveil through **the Throat**, runs south beneath the plateau and the Rootdeep (Mothwell's lamps light it) and comes back into the light at the **Gloamwood Verge**. Road 17 is a boat journey along it. Drawn dotted. |
| **Lake Rime** | The frozen inlet Rimeholt is built on; the Ice Vault (Kyogre) lies beneath. |
| **Lake Sallow** | One great sulfur hot spring between Mirefen and Cindervault; Lantern Isle steams in the middle. Road 7 crosses it (Surf). |
| **Mirror Mere** | A small silver lake in the Looking-Glass Wood: gate A into Antumbra. |
| **Saltmere Lagoon** | The salt lake behind Saltmere's sandbar, fed by the Selvedge; the Grey Saltings' pans line it. |

## 4. The kingdoms

| Kingdom | Where | Land | Seat and gym towns (gym #, Revision 14) |
|---|---|---|---|
| **Elowen, the Evergreen Crown** | the south-west and south, from the west coast to the Gloamwood | Oldwood, orchards, river meadows, chalk coast. The Gossamer Wood (silk) in the middle; the Gloamwood (permanent dusk) at its heart in the south-east. | **Verdance** (seat, 9) · Saltmere (1, free port) · Briarwick (2) · Gloaming (17) · Ferrow's Landing (start) |
| **Isenmar, the Frozen Sea** | the north-west coast, the frozen north sea, the Rime Isles | Snowfields, pine, fjords and sea-ice. | **Rimeholt** (seat, 10) · Ebbmouth (3) · Skaldfast (Rime Isles, war) |
| **Zenith, the City Above** | the plateau, north-centre | Brass, white stone, rail and pylons; airships. | **Lumen City** (seat, 4) · Skyreach (11) · Cogsworth (15) |
| **Nadir, the City Below** | below the plateau: the north-coast undercity and the southern lowlands | Marsh, slag, mine shafts, a sea-drowned city. | **Underveil** (seat, 16, in drowned Aurelia's towers) · Mirefen (6) · Ironreach (8) |
| **Ossaria, the Bone Sands** | the north-east desert and crags | Sand, canyons, fossil beds, tombs. | **Duneholt** (seat, 5) · Cragholm (13) |
| **Ashkaar, the Dragonfire Dominion** | the east and south-east | Basalt, ash plains, the Cinderhorn, dragon ridges. Reaches north along the coast to Cinder Cape. | **Cindervault** (seat, 7) · Wyrmrest (18) · Cinder Cape Warfort (war) |
| **Antumbra, the Kingdom Behind the Glass** | nowhere on the real map: the inset in the south-east sea | The mirror realm: inverted desert hanging in the sky, shadows falling toward the light. | **Lucent** (seat, 12) · Gravenmoor (14) |
| **Crownhaven** | inside the Crownwall, south-east of centre | The Accord's capital and the Festival grounds. | **Crownhaven** (the Festival) |

## 5. Borders and borderlands

Kingdoms touch **only** through borderlands (Revision 9), each with a town where the two peoples live together. On the
map the borderlands are the mottled ground where both kingdoms' colours mix; the dashed red line marks kingdom edges.

| Code | Borderland | Between | Where (squares) | Town |
|---|---|---|---|---|
| A | The Rimewood | Elowen / Isenmar | west coast, x 3–7, y 9–14 | Frostwick (6, 12) |
| A2 | The Rimewood (north), the Hoarwood | Elowen / Isenmar | x 5–7, y 8–9 | Snowbriar (5, 8) |
| B | The Icefall Locks | Isenmar / Zenith | the west Escarpment, x 6–9, y 6–7 | Brassfall (8, 7) |
| B2 | The Mast Glacier | Isenmar / Zenith | x 6–7, y 1–2 | Anchorhold (7, 2) |
| C, C' | The Brass Dunes, the Slag Mesa | Zenith / Ossaria | the plateau's east foot, x 15–18, y 3–5 | Copperdune (17, 4) |
| D | The Leach Canyons | Ossaria / Nadir | x 18–20, y 8 | Charwell (19, 8) |
| E | The Sulfur Reach | Nadir / Ashkaar | Lake Sallow and the Ironway, x 19–21, y 10–11 | Scaldwater (21, 10) |
| F | The Rootdeep | Nadir / Elowen | x 13–15, y 12–15 (and the Blindwater below) | Lanternroot (13, 12), Mothwell (15, 15) |
| G | The Wired Wood | Zenith / Elowen | the plateau's south-west foot, x 10–11, y 7–9 | Verdigris (11, 9) |
| H | The Looking-Glass Wood | Elowen / Antumbra | x 12–14, y 9–10 | Glassmere (13, 10) |
| I | The Obsidian Barrows | Antumbra / Ossaria | x 22–23, y 7–8 | Vigil (23, 7) |
| J | The Thornwar Marches | Elowen / Ashkaar | the south coast, x 19–21, y 16–17 | Thornwatch (21, 17) |
| K | The Pilgrim Pass | Ashkaar / Crownhaven | the Crownwall's north-east gap, x 21–23, y 13–15 | Pilgrim's Rest (22, 13) |
| L | The Hanging Stair | Zenith / Nadir | the plateau's north cliff, x 14–15, y 1–2 | Midstair (14, 1) |
| M | The Cinderglass Barrens | Ashkaar / Ossaria | x 24–25, y 7–9 | Glasswake (25, 7) |

**Fire and ice never border.** Isenmar's land is the north-west; Ashkaar's is the east. Between them lie Zenith, Nadir and
Ossaria on land, and the only place they meet is the sea: the **Shattered Ice** strait between Skaldfast and Cinder Cape
(war theatre, maps 920–927). Ashkaar reaches it overland through the Cinderglass Barrens and the Wyrmtongue spit;
Isenmar by the Thane's sled-road across the frozen sea.

Not adjacent (by design): Isenmar–Ashkaar, Isenmar–Ossaria, Isenmar–Nadir, Elowen–Ossaria, Antumbra with anything but
Elowen and Ossaria, Crownhaven with anything but Ashkaar.

## 6. Roads, sea lanes and air lanes

- **The Eighteen Roads** join the gym towns in badge order; **the Pilgrim Road** (Road 19) climbs from Wyrmrest into the
  Crown. Each road is two to five named maps (WORLD.md §11). On both maps a numbered shield marks each road.
  The early chain (Revision 14): Ferrow's Landing → **the Strand Road** west along the chalk coast → **Saltmere** →
  **the Weavers' Road** inland up the Selvedge → Gossamer Wood → **Briarwick** → **the Hoar Road** north over the fells,
  through Frostwick and the Rimewood, down Gullcry Cliffs → **Ebbmouth**. The Frostflat Causeway along the coast closes
  the loop from Frostwick back to Saltmere.
- **Side roads:** Windfall Row (orchards, Chapter 1), the Frostflat Causeway, the war road north from Cindervault
  (the Cinderglass Barrens, Glasswake, the Wyrmtongue to Cinder Cape).
- **Sea lanes:** the Last Ferry (the *Dovetail*, into Ferrow's Landing), the coast packet (Saltmere ↔ Ebbmouth), the
  Strait ferry to the Shardfall Isles (postgame). **On the ice:** the Thane's sled-road from Rimeholt along the frozen
  north sea to the Rime Isles. **The war crossing:** Cinder Cape ↔ Skaldfast across the Shattered Ice.
- **Air lanes** (Act III, Skyreach airships): Skyreach ↔ Anchorhold, Skyreach ↔ Lumen.
- **Underground:** the Blindwater (Road 17).

## 7. Crownhaven and the Festival grounds

Crownhaven sits in the bowl of the Crownwall, a ring of white peaks about three squares across, south-east of the
continent's centre. Every kingdom can see the ring; only Ashkaar can walk into it, by the **Pilgrim Pass** through the
ring's one gap on the north-east side (eighteen shrines, Dominar's Toll below it, Pilgrim's Rest at its foot,
Sovereign's Ascent through the wall, and the Coronation Road down into the city). Everyone else comes by air or as
Ashkaar's guest, which is the politics of the Festival in one fact.
Inside the ring: Lower Crownhaven (the Eighteen Gates face the Imprints, the Market Ring, the Pilgrims' Quarter), Upper
Crownhaven (the Basilica, the Accord Palace, the Concordance Spire) and the **Festival grounds** on the bowl's east
side, nearest the pass: the Processional Plaza, the **Temple-Arena of the Blessing** (Hall of Eighteen Doors, Altar
Stage) and the Court of Eight Pavilions. The Glassfall Scar lies on the inner slope of the north-west wall.

## 8. Antumbra

Antumbra has no place on the real map. Both images draw it as an **inset framed like a mirror** in the south-east sea.
Its three gates are marked A, B and C on the mainland and in the inset:
- **A, Mirror Mere** (Elowen, the Looking-Glass Wood) → the Antumbra Threshold → Widdershins Walk → **Lucent**.
- **B, the Grave Glass** at Vigil (Ossaria) ↔ Yesterday's Road (from Lucent) and Hindmoor → Downflame Road → **Gravenmoor**.
- **C, the Obsidian Barrows' east gate** ↔ the Noonless Road from Gravenmoor (the Barrow of the Wardens stands at it).

## 9. The in-game Town Map

`pbs/town_map.txt` (shipped as `PBS/town_map_prismfall.txt`) defines **region 0, Velmora**, with
`Filename = prismfall_velmora.png`. Every settlement, every road square and every named dungeon has a `Point`; dungeons
and districts show as the point of interest of their square. Every map has a `MapPosition` (`mapgen/data/town_map_positions.json`,
applied by `build.py`; maps.json `metadata.town_map_pos`). Fly spots exist for the six built towns (their PC
HealingSpots). `Prismfall Maps/009_TownMap.rb` compiles our file instead of the stock one, whose Essen region 0 it
replaces. The UI draws the 480×320 graphic over `Graphics/UI/Town Map/bg.png`.

| Settlement | Square | | Settlement | Square |
|---|---|---|---|---|
| Ferrow's Landing | 12, 18 | | Rimeholt | 3, 2 |
| Saltmere | 6, 18 | | Skyreach | 10, 3 |
| Briarwick | 11, 13 | | Lucent (inset) | 28, 16 |
| Ebbmouth | 3, 7 | | Cragholm | 24, 2 |
| Lumen City | 12, 5 | | Gravenmoor (inset) | 27, 18 |
| Duneholt | 22, 4 | | Cogsworth | 16, 2 |
| Mirefen | 16, 9 | | Underveil | 12, 1 |
| Cindervault | 24, 10 | | Gloaming | 16, 17 |
| Ironreach | 17, 11 | | Wyrmrest | 24, 15 |
| Verdance | 9, 10 | | Crownhaven | 19, 14 |

Borderland towns, roads and dungeons: `design/PLACE_NAMES.md` (Square column) and `pbs/town_map.txt`.

## 10. Updating

1. Edit `tools/worldmap/world_data.py` (names, roads, squares) or `world_geo.py` (coast, mountains, rivers).
2. `python3 -I tools/worldmap/gen_docs.py` → PLACE_NAMES.md, ROUTES.yaml, WORLD.md §11, town_map.txt, positions, maps.json.
3. `python3 -I tools/worldmap/gen_world_map.py` → both images (about a minute).
4. If names changed: `python3 -I tools/rename_places.py` (dry run, read `tools/worldmap/last_rename.diff`), then `--apply`.
5. `ruby tools/field_defaults_to_rb.rb`, then the map builder's `build.py`.
