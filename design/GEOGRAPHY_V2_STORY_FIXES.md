# Geography v2 + SPINE Rev 18: story lines to fix

Written by the cartographer for the story agent. Every line below describes a border crossing, a direction or a
war site that is wrong under **Geography v2** (SPINE Rev 18: Elowen in the middle, Ossaria north, Isenmar west,
Ashkaar east, Zenith/Nadir south) or under the **land war in Ossaria** (Rev 18 war bullet). Line numbers are
from the tree on 2026-11-19. Suggested fixes are only suggestions: wording is yours. The map data
(`tools/worldmap/world_data.py`, `design/maps.json`, `design/ROUTES.yaml`, `design/PLACE_NAMES.md`,
`design/WORLD.md` §1/§9/§10, `design/WORLD_MAP.md`) is already updated, and `art/previews/world_map.png` shows
the new layout and the front.

## 0. Where things are now (quick reference)

| Kingdom | Where | Borders |
|---|---|---|
| **Ossaria** | the north: bone sands along the north coast, the crags (Cragholm, Vigil); the war is fought in its western dunes | Isenmar (the Mast Glacier), Elowen (the Brass Dunes, the Leach Canyons), Ashkaar (the Cinderglass Barrens), Antumbra (gate B, the Grave Glass at Vigil) |
| **Isenmar** | the west and north-west: the frozen sea, Rimeholt on Lake Rime (north-west), Ebbmouth on the west coast south of it | Elowen (the Rimewood, the Hoarwood, the Icefall Locks), Ossaria (the Mast Glacier). **Never Ashkaar, never Zenith/Nadir.** |
| **Ashkaar** | the east: Cindervault and the Cinderhorn, the Wyrmspine and Wyrmrest; Cinder Cape at its north-east tip | Ossaria (the Cinderglass Barrens, Glasswake), Elowen (Lake Sallow / the Sulfur Reach, the Ironway, the Thornwar Marches). **Never Isenmar, never Zenith/Nadir.** |
| **Elowen** | the middle, from the south-west coast (the start: Ferrow's Landing, Saltmere, Briarwick) to the Gloamwood and Gloaming in the south-east | every kingdom. The **Crown Road** rings the Crownwall: Wallshadow Row (W and S), Candle Down (E), the Highwold (N), Kingsmead (NW); Coppice Ride links it west to the Icefall Locks |
| **Zenith** | the south: the plateau of the City Above; Lumen City on its south brink, Skyreach and Cogsworth on its east side | **Elowen only** (the Meridian Mainline, the Arc-Lamp Mile, the Wired Wood, the Slag Mesa) |
| **Nadir** | beneath Zenith, same footprint: Mirefen's marsh at the foot of the north cliff, Ironreach under the west rim, Underveil under the south cliff with **drowned Aurelia on the south coast** | Zenith (vertical: the Hanging Stair, the Drownings), Elowen (the Rootdeep, the Blindwater, the Gutterfall) |
| **Crownhaven** | Elowen's heart, inside the Crownwall | Elowen only; one way in: the Pilgrim Pass, then Sovereign's Ascent |
| **Antumbra** | behind the glass (inset) | gate A at Mirror Mere (Elowen, north-west of Crownhaven), gate B at the Grave Glass (Vigil, Ossaria), gate C at the Slagglass (the Slag Mesa, Zenith/Elowen) |

**The war (Rev 18).** Isenmar's host marches east from Rimeholt along the Thane's Sled-Road, over the Mast
Glacier to **Skaldfast** (now Isenmar's border fortress on Ossaria's west edge, map 921–923) and digs in on
**the Rimed Sands** (920, was "the Rime Narrows"). Ashkaar's legions march from Cindervault's north gate through
the Cinderglass Barrens and Glasswake, then west across the bone sands to the **Ashkaar Siege Camp** (924).
**Cinder Cape Warfort** (927) is Ashkaar's staging fortress on its own north-east coast, behind the lines and
out of sight of the battlefield. **The Steamline** (925) is the steam-glass strip where the two Imprints meet.
The battlefield is **the Glass Dunes** (926, was "the Shattered Ice"): Primal Kyogre drags a flood-sea into the
desert and Reshiram's fire turns the dunes to glass. Map renames: 920 the Rimed Sands, 922 Skaldfast - Rime Keep
(was Harbour Keep), 926 the Glass Dunes, 582 Lumen West Gate (was Lumen South Gate; Lumen is now entered from the
west, off the Arc-Lamp Mile).

Severity: **W** = wrong under v2/Rev 18 and should change; **C** = check (it still works, but the geography
behind it has moved); **N** = naming only.

## 1. story/01_WORLD_LORE.md

| Line | Now says | Sev | Problem and suggested fix |
|---|---|---|---|
| 18 | Aurelia "rose in gold terraces up the **northern** sea-cliffs" | W | Aurelia is under Zenith's **south** cliffs now. "up the southern sea-cliffs". |
| 21 | "woke ... Kyogre off the **northern** coast" | W | Kyogre sleeps in Isenmar's frozen sea in the west. "off the western coast". |
| 33 | "The surge rolled **west** along the coast and woke Kyogre" | C | From the south coast the surge goes west, then north up the west coast. "rolled west and north up the coast" if you want it exact. |
| 34 | Antumbra: "Behind the great forest **of the south**" | W | Elowen is the middle now. "Behind the great forest" (gate A, Mirror Mere, is north-west of Crownhaven). |
| 223 | Elowen: "The great forest **of the south and south-west**" | W | "The great forest at the heart of Velmora, from the south-west coast to the Gloamwood in the south-east, with Crownhaven at its centre. It borders every kingdom." |
| 228 | Gloaming: "**the forest's heart**"; "the dusk is spreading **south** across Elowen" | W | Crownhaven is Elowen's heart; Gloaming is the deep **south-east**. "the forest's oldest corner"; the dusk spreads **west** across Elowen (toward Briarwick). |
| 236 | Isenmar: "The **west and north coast**" | W | The north coast is Ossaria's. "The west and north-west coast". |
| 237 | Ebbmouth: "the **glacier-fed** River Ebb" | C | The Ebb now rises on the Crownland downs west of the Crownwall and runs west past the Icefall Locks to Ebbmouth. "where the River Ebb comes down from the downs to meet the open sea", or keep "glacier-fed" only if you want a glacier tributary (none is drawn). |
| 241 | Zenith: "on the **north-central** plateau" | W | "on the southern plateau". |
| 250 | Underveil: "the Sump **beneath the north cliffs**" | W | "beneath the south cliffs". |
| 253 | Ashkaar: "The **east and south-east** volcanic highlands" | W | The south-east is Elowen's Gloamwood (and the Antumbra inset). "The eastern volcanic highlands, from Cinder Cape on the north-east coast down the Wyrmspine". |
| 254 | "the caldera of **Mount Cinder**" | N | The volcano's place name is **the Cinderhorn** (maps 664–666 in PLACE_NAMES). Same at 05_ACT_II.md:99, :103 and 11_FINALE_LINES.md:65. |
| 258 | Ossaria: "The **north-east** desert and canyon country" | W | "The northern desert and canyon country along the north coast". Worth adding that the war is fought in its western dunes, on neutral ground. |

## 2. story/00_OVERVIEW.md

| Line | Now says | Sev | Problem and suggested fix |
|---|---|---|---|
| 48 | the Fault "pulls the sea back from the **north coast**" | W | "south coast". |
| 112 | Ossaria row (Act IV: Cragholm ...) | C | Add the war: "Act IV–V: two foreign armies dig in on its western dunes". |
| 113 | Ashkaar row: "Act V: Wyrmrest **at the war's edge**" | C | The front is now far away, in Ossaria's west. "Act V: Wyrmrest, its riders gone to the war in the sands". |

## 3. story/04_ACT_I.md (start chain unchanged)

| Line | Now says | Sev | Problem and suggested fix |
|---|---|---|---|
| 192, 194 | Ch5: "The Reedholms → The Icefall Locks → Lumen City" | C | Lumen is now in the south, so Road 4 continues on Elowen ground: the Icecutters' Haul (592), the Icefall Locks (581), **Coppice Ride (595)**, **Wallshadow Row (594, the Crown Road's south-west arc)**, the Arc-Lamp Mile (593), then **Lumen West Gate (582)**. Add the new legs to the Location line. |

Nothing else in Act I moves: Ferrow's Landing, the Strand Road, Saltmere, the Weavers' Road, Briarwick and the
Hoar Road → Rimewood/Frostwick → Ebbmouth keep their positions and directions.

## 4. story/05_ACT_II.md

| Line | Now says | Sev | Problem and suggested fix |
|---|---|---|---|
| 14 | Ch6 title: "The Brass Dunes → Static Tunnels → The Rib Road → Duneholt" | C | Lumen to Ossaria now crosses Elowen: the Meridian Mainline (612) north off the plateau, **Candle Down (602)** and **the Highwold (603)** round the Crownwall, then the Brass Dunes. |
| 16 | Ch6 Location: "**R9**, Static Tunnels, **R10**, Duneholt, **R11** ..." | N | Old route labels. R9 = the Brass Dunes (600), R10 = the Rib Road (601), R11 = the Marrow Road (620). Add the Mainline (612), Candle Down (602), the Highwold (603); Sunbleach Flats (613) lies past Duneholt. |
| 18 | "**Zenith's plateau gives way to Ossaria**" | W | Zenith and Ossaria no longer touch. "North of the Crownwall the Highwold's chalk downs give way to the Brass Dunes, and then to **Ossaria, the Bone Sands**." (The Brass Dunes are the Elowen/Ossaria borderland; Copperdune is its town.) |
| 57, 59 | Ch7: "The Leach Canyons → Mirefen" | C | The road now goes the Marrow Road (620) → the Kneeling Stones (632) → the Leach Canyons (621, Ossaria/Elowen) → **Wormwood Lea (634, Elowen)** → **the Gutterfall (633, Nadir)** → Mirefen. Add Wormwood Lea and the Gutterfall. |
| 62 | "The PC descends a rattling lift-cage **from the plateau's edge**" | W | The PC now arrives from Elowen at ground level, not from the plateau top. "The PC rides a rattling lift-cage down the Gutterfall, where Zenith's runoff pours off the plateau's north cliff. Under the overhang the sky disappears ..." (the rest of the paragraph stands). |
| 99 | "**Mount Cinder**" | N | the Cinderhorn (see 01:254). Also line 103. |
| 101 | "the land climbs **out of Nadir's runoff into Ashkaar**" | W | Nadir and Ashkaar never touch. Lake Sallow is the Elowen/Ashkaar borderland (the Sulfur Reach). "Past Lake Sallow's sulfur shallows, still Elowen ground, the land climbs into **Ashkaar** ..." |
| 135, 137 | Ch9: "The Ashmarch → The Ironway → Ironreach" | C | Between the Ironway (Elowen/Ashkaar border) and Ironreach the road now runs **Candle Down (602)** on the Crown Road, then **the Long Drop (672)** down under Zenith's west rim. Add both. |

## 5. story/06_ACT_III.md

| Line | Now says | Sev | Problem and suggested fix |
|---|---|---|---|
| 17 | "The Rootdeep Lift Road (the great freight-lift **from Nadir up to the plateau**)" | W | The Rootdeep is the Nadir/Elowen borderland; Verdance is in Elowen. "the great freight-lift from Nadir's mines up to Elowen's downs, west of the plateau". The road is the Tailings (692) → the Rootdeep (680) → Prism Falls (681) → the Briarway (693) → Verdance. |
| 102 | "Transit (segment 10) ... The Thane's Sled-Road/The Mast Glacier ... **pass back through Ebbmouth**" | W | The Sled-Road and the Mast Glacier now run **east** from Rimeholt to Anchorhold on the Ossaria border, away from Ebbmouth. Either make the Ebbmouth Strike a detour south from Rimeholt down the Whalebone Road (Ebbmouth is a short walk south of the Hoarwood), or move the strike to Anchorhold's moorings. |
| 112 | Ch11 cliffhanger: "**Cloudstair** (Rock Climb) and **Stillwater** (728)" | W | Stillwater is by Rimeholt; the Cloudstair is in Zenith, at the other end of Velmora. Isenmar and Zenith share no border, so Road 11 has an **air leg**: Sled-Road (720) → Mast Glacier (721) → **Anchorhold (730)**, where the airships moor → by Gale Post airship over Ossaria and Elowen → **the Tetherline (732)** → Cloudstair (724) → Skyreach. Suggest: Stillwater on the Sled-Road; the Gale Post airship (with its banner) picks the PC up at Anchorhold. |
| 116 | Ch12 title: "Cloudstair → Skyreach" | C | Add the airship from Anchorhold and the Tetherline (see 112). |
| 161, 164 | Ch13: "Conductors' Causeway → The Wired Wood → **Mirror Mere**" | C | Between the Wired Wood and Mirror Mere the road now crosses Verdigris, **Candle Down (602)**, **the Highwold (603)** and **Kingsmead (756)** round the Crownwall's north, then the Looking-Glass Wood (752). Add them. |
| 217 | "On the **north coast**, the sea pulls back from Zenith's cliffs" | W | "south coast". |

Still correct: line 74 (Rimeholt on Lake Rime, part of the frozen sea), 99 (refugees "south into Elowen": the
Hoarwood is south of Rimeholt), 72/75 ("northern Wardens", "southern idealists").

## 6. story/07_ACT_IV.md

| Line | Now says | Sev | Problem and suggested fix |
|---|---|---|---|
| 11 | "News screens show the **north coast**: the sea pulled back from Zenith's cliffs" | W | "south coast". |
| 186 | "the Drownings (... the drained **north coast**)" | W | "the drained south coast". |

Still correct: line 20 (Spinefall Gorge as a mirror exit into Ossaria), line 136 (the Slag Mesa as Zenith's
eastern waste: gate C, the Slagglass, is there, so "Noonless Road → Slag Mesa" is right).

## 7. story/08_ACT_V.md

| Line | Now says | Sev | Problem and suggested fix |
|---|---|---|---|
| 32 | "Gloaming's twilight has crept **south** across half the forest, and Briarwick's looms ..." | W | Gloaming is in the south-east, Briarwick in the west. "crept west across half the forest". |
| 74 | "Dominar Hrothgar is at the front ... (the Ashkaar Siege Camp)"; "means to march on Zenith" | C | The Siege Camp is now in Ossaria's western dunes, the length of Ashkaar and half of Ossaria from Wyrmrest. A march on Zenith now has to cross Elowen (Ashkaar and Zenith share no border). Fine as an intent; just don't call Zenith "across the pass". |
| 78 | "petitions the Dominar in his command pavilion at the Siege Camp, after the battle" | C | Fine, but the PC is now far from Wyrmrest: Sigrun flies them (14_WAR:72 already says so). |
| 324 | "Marisol's fishing fleet evacuates Lower Crownhaven across the caldera lake" | ok | The caldera lake is inside the Crownwall; no change. |
| 409 | "Rimeholt rebuilding on the southern shore" | ok | Lake Rime's southern shore; no change. |

## 8. story/14_WAR_AND_BLESSING.md (Part B: the war)

| Line | Now says | Sev | Problem and suggested fix |
|---|---|---|---|
| 49 | "the River Ebb **rises in Ashkaar's highlands** ... Isenmar's **ice-fleet** and Ashkaar's riders have skirmished there" | W | The Ebb is a western river now, and the two kingdoms share no border. New grievance on the ground they do share: "the bone sands between them. Isenmar's sled-caravans and Ashkaar's riders both cross Ossaria's western dunes to the salt and glass markets, each claims the old caravan road and its wells, and they have skirmished there for a century (Ossaria signed neither treaty)." |
| 58 | Ch4 seed: "an Ashkaar rider burned an Isenmar **ice-barge at the headwaters**" | W | "an Ashkaar rider burned an Isenmar sled-caravan on the dune road". |
| 61 | "Kyogre's rain rolls east and floods Ashkaar's **lowland forts**" | C | Direction is right, but the rain crosses Ossaria first, which is a good set-up for the flood-sea in the dunes. "rolls east across the bone sands and floods Ashkaar's forts in the Cinderglass Barrens". |
| 64 | Ch14: "The Steamline ... steam-glass **along the north-east coast**" | W | "steam-glass across Ossaria's western dunes, a few days' march west of Cragholm". (Cragholm is now the nearest gym city to the front, which suits the refugees line.) |
| 65 | Ch15: "Ashkaar's dragons ring the **fortress-port**. Marisol's Ebb Guild runs the blockade **through the Rime Narrows** by night. If Teo lived, he's organizing **boats**." | W | No sea. "Ashkaar's dragons ring the border fortress. Marisol's Ebb Guild runs sled-convoys over the Mast Glacier from Anchorhold by night. If Teo lived, he's organizing the sleds." |
| 68 | Ch19: "Isenmar's host, which has come **up the frozen Ebb** with Kyogre before it" | W | "which has come east over the Mast Glacier and out of Skaldfast into the dunes, with Kyogre's flood-sea before it". |
| 71 | "### The Battle of **the Shattered Ice** (Ch19)" | N | "the Glass Dunes". |
| 72 | Setup: "The front is on the **north-east coast** ... fortress-port Skaldfast ... Cinder Cape Warfort guards Ashkaar's shore, the **Rime Narrows** between them are choked with the **ice-fleet** ... Kyogre ... is walking the **Narrows** like a tide ... fought on **the Shattered Ice**, the broken sea between the two hosts." | W | Suggested rewrite: "The front is in Ossaria's western dunes (WORLD.md §9). Isenmar holds **Skaldfast**, its border fortress on Ossaria's west edge, and has dug white trench-lines across **the Rimed Sands** east of it; Ashkaar's legions hold the **Ashkaar Siege Camp** in the bone sands further east, supplied from the **Cinder Cape Warfort** on Ashkaar's north-east coast through the Cinderglass Barrens. The Bleed strip of steam-glass where the Imprints meet is **the Steamline**. Sigrun's trial and oath (08, Ch19) happen first, at Wyrmrest. Then word comes that Kyogre has risen from the Ice Vault and is dragging a flood-sea across the desert, and that her father has carried the Light Stone to the front. Sigrun flies the PC there overnight. The climax is fought on **the Glass Dunes** between the two hosts, where the flood meets Reshiram's fire and the sand turns to glass." |
| 75 | `:war_warning`: "Climbing Frostfang Pass, the PC sees the Dominar's legions massing" | C | Frostfang is in Isenmar's west; the legions now mass far to the east in the dunes. "sees the smoke of the Dominar's legions massing on the sands beyond the Mast Glacier". |
| 76 | `:war_convoy`: "Marisol's **blockade-runners** ... through the Steamline into besieged Skaldfast" | C | Geography works (from Cragholm, west across the dunes, through the Steamline into Skaldfast). "blockade-runners" → "siege-runners". |
| 79 | `:war_climax`: "On **the Shattered Ice**" | N | "On the Glass Dunes". |
| 89 | WAR-1 "The Beam Clash on **the Shattered Ice**" ... "over the Shattered Ice" | N | "on the Glass Dunes" / "over the flooded dunes". |
| 97 | "Isenmar's **ice-fleet** hold the sky and the lake together" | W | Isenmar has no fleet in this war. "Isenmar's sled-host" (or "ice-riders"). |

Still correct: 59 (the eastern passes), 77 (`:war_prisoner`, a short trip to the Siege Camp: from Cragholm it
is a westward trip across the sands), 80 (the armistice table in Skaldfast's great hall), 93 (Kyogre back to
the sea).

## 9. story/13_CUTSCENES.md (WAR-1)

| Line | Now says | Sev | Problem and suggested fix |
|---|---|---|---|
| 8 | "WAR-1 — The Beam Clash on **the Shattered Ice**" | N | "on the Glass Dunes". |
| 10 | Backdrop: "the Shattered Ice (**broken sea-ice plates, black water between**; Skaldfast's walls left, **Cinder Cape Warfort right**; dawn)" | W | "the Glass Dunes (bone-white dunes under a low sky; Skaldfast's walls far left (west), the Siege Camp's palisade and banners right (east); dawn)". Cinder Cape is out of sight, behind the Ashkaar lines. |
| 14 | Shot 1: "Isenmar: **sled-ships** ... Thane Eirik on the **lead prow** ... the Dominar on the **Warfort wall**" | W | "ice-sledges on frozen sand ... Thane Eirik on the lead sledge ... the Dominar on the Siege Camp's earthwork". |
| 15 | Shot 2: "low angle on the **black water**. The water bulges. Kyogre rises" | W | "low angle on the sand: Kyogre's flood-sea pours in over the dunes, the water bulges, Kyogre rises". Eirik's line could become "Isenmar! The sea has come to the sand!" |
| 16 | Shot 3: "Cut: **the Warfort wall**" | W | "the Siege Camp earthwork". |
| 18 | Shot 5: the beams "cross the **ice**" | W | "cross the flooded dunes". |
| 19 | Shot 6: "**ice plates crack** outward in a ring" | W | "wet sand glasses outward in a ring". |
| 20 | Shot 7: "Cut: **ice surface** ... **Ice** turns to steam-glass" | W | "Cut: the dune surface ... sand and flood-water turn to steam-glass". |
| 23 | Shot 9C: "stands on Marisol's **prow**" | C | Works if Marisol's boat is on Kyogre's flood-sea: say so in the shot ("on the flood"). |
| 28 | 13B/C: "banners go up over Skaldfast (B) or **Cinder Cape (C)**" | W | Cinder Cape is far away. "over Skaldfast (B) or over the Siege Camp (C)". |
| 89 | "adopted as given: ... **Rime Narrows**, Skaldfast, ... **the Shattered Ice** ..." | N | Replace with "the Rimed Sands" and "the Glass Dunes". |

## 10. story/10_CHOICES_ENDINGS.md, 12_RUIN_ROUTE.md, 02_FACTIONS.md, 03_CAST.md

| File:line | Now says | Sev | Suggested fix |
|---|---|---|---|
| 10_CHOICES_ENDINGS.md:140 | `:war_climax` "— **the Shattered Ice**, both lines charging" | N | "the Glass Dunes". |
| 10_CHOICES_ENDINGS.md:151 | "the winner's **fleets** or legions" | W | "the winner's host or legions". |
| 10_CHOICES_ENDINGS.md:181, :391 | "the legions march on Zenith" | C | Now a march across Elowen; fine as an outcome. |
| 12_RUIN_ROUTE.md:52 | "R5 — ... (Wyrmrest, Gym 18; **the Shattered Ice**; Nova)" | N | "the Glass Dunes". |
| 12_RUIN_ROUTE.md:56 | "The Battle of **the Shattered Ice**" | N | "the Glass Dunes". |
| 02_FACTIONS.md:168 | Ashkaar: "Either march on Zenith or fly for Crownhaven" | C | As 10:181. |
| 03_CAST.md:319 | Sigrun: "legions are poised to march on Zenith" | C | As 10:181. |

Still correct: 03_CAST.md:169 and :345, 02_FACTIONS.md:165 (Ebbmouth as Isenmar's southern port; refugees
south into Elowen; refugees in Cragholm and Briarwick).

## 11. Not story: design docs, data and code that still use the sea-war names

For their owners; the cartographer has not edited these. Names: the Rime Narrows → **the Rimed Sands** (920),
Skaldfast - Harbour Keep → **Skaldfast - Rime Keep** (922), the Shattered Ice → **the Glass Dunes** (926).

| File:line | What | Owner |
|---|---|---|
| design/SPINE.md:23 | Rev 18 layout bullet "Fire and ice meet only across the northern sea (the war front)" contradicts the war bullet at :26 | coordinator |
| design/SPINE.md:88, :140 | "war is fought across the sea (the Shattered Ice strait)"; "Isenmar (frozen sea fortress-ports)" | coordinator |
| design/FLAGS.md:174 | V122 WAR_STATE "4 = Battle of the Shattered Ice fought" | flags |
| design/NARRATIVE_KEYS.md:228, :231; plugins/Prismfall Core/012_Narrative_Data.rb:289 | `:war_convoy` "Marisol's fleet"; `:war_climax` "the beam clash on the Shattered Ice" (description strings) | narrative keys |
| design/CUTSCENES.md:441 | war backdrops "Shattered Ice at dawn, Skaldfast walls, Cinder Cape Warfort, the ridge" | cutscenes |
| plugins/Prismfall Cutscenes/013_Scenes_War.rb:4, :69; 013_Scenes_War_OnMap.rb:4; 015_Debug.rb:15 | WAR-1 title and the "Shattered Ice before dawn" backdrop; sled-ship props in 004_Actors.rb:207 and 005_Backdrops.rb:301 can stay as land sledges | cutscenes |
| design/TRIALS.md:97; design/TRIALS_QUESTS.md:60; plugins/Prismfall Trials/120_Quests_Catalogue.rb:102, :105 | quest "The Saga of the Shattered Ice" (`IS_SAGA_OF_THE_ICE`; the key can stay) | trials |
| tools/trainer_gen/gen.py:1315–1336 → pbs/trainers.txt comments | "Skaldfast harbour (map 922, Frozen Lake)", "The Shattered Ice (map 926, Frozen Lake)", "Isenmar ice-fleet officer"; 926's default field is now DESERT | trainers |
| design/ART_DIRECTION.md:245 | Isenmar "fortress-ports: sea walls, ice-locked harbour ..." | art (Rimeholt and Ebbmouth still fit; Skaldfast is now a land fortress) |
| design/SPINE_FEEDBACK.md:30, :37; design/CUTSCENE_RESEARCH.md:169 | historical notes on the sea war | none (superseded) |

Already synced by the cartographer: design/FIELD_DEFAULTS.yaml names for 582/920/922/926 and the spec fields
for 920 and 926 (DESERT), regenerated into plugins/Prismfall Field Effects/011_FieldEffects_MapDefaults.rb with
tools/field_defaults_to_rb.rb. The Glass Dunes' mid-battle field change (flood, then glass) is the fields
team's call.
