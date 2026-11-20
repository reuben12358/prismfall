# PLACE_NAMES - every map of Velmora, old name -> new name

> Owner: world cartographer. **Source of truth:** `tools/worldmap/world_data.py` (regenerate this file with
> `python3 -I tools/worldmap/gen_docs.py`). `tools/rename_places.py` reads the table below and renames every
> reference in the project (dry run by default). SPINE Revisions 13 and 14. Map IDs never change: Saltmere stays
> 140 and Briarwick 120 after the Gym 1/2 swap; `segment` in maps.json carries the badge count.

## Naming voices

No place is called "Route N". Roads are named the way Westeros names them (the Kingsroad, the Neck, Blackwater
Rush): from geography, history, lords, trades and legends, in each kingdom's own voice. A road between two towns
has one road name (the Strand Road, the Hoar Road) and every map along it has its own name.

- **Elowen.** Fairy-forest English: soft, old and a little courtly. Names come from cloth and thread (the weavers), from thorn, briar and fruit, and from small country laws. Endings: -wick, -lea, -down, -row, -wold, hollow. Examples: The Ferrymen's Mile, Windfall Row, Thistledown Lea, The Dyers' Ford, The Briarway.
- **Isenmar.** Nordic sea-ice: short hard words and kennings. Names come from whale, rime, floe, thane and skald, and from the work that keeps people alive on ice. Endings: -holm, -ness, -garth, -fast, -road. Examples: The Reedholms, The Icecutters' Haul, The Whalebone Road, The Thane's Sled-Road, Gullcry Cliffs.
- **Ashkaar.** Martial fire and dragon: every road is a march, an oath or a part of the wyrm. Names are blunt and possessive (the Dominar's, the Legion's). Words: ash, pyre, oath, march, toll, spine, tongue, horn. Examples: The Ashmarch, The Pyre Road, The Wyrmspine, The Wyrmtongue, Dominar's Toll.
- **Ossaria.** Bone sands: the land is a buried skeleton and is named like one. Roads are bones, flats are bleached, and the Electors put their title on anything that pays tax. Words: rib, marrow, jaw, spine, vertebrae, sun. Examples: The Rib Road, The Marrow Road, The Kneeling Stones, Spinefall Gorge, The Vertebrae.
- **Zenith.** Brass and progress: civic, patented and proud. Roads are Mainlines, Parades and Causeways, named for what they carry or which invention lit them. Words: arc-lamp, conductor, tether, mainline, parade, brink. Examples: The Arc-Lamp Mile, The Meridian Mainline, Conductors' Causeway, The Tetherline, The Smokestack Parade.
- **Nadir.** Undercity slang: short, rude and accurate. People name a place for what it does to you. Words: drop, throat, gutter, tailings, sump, leech, knuckle. Examples: The Long Drop, The Gutterfall, The Tailings, Leechman's Walk, The Throat.
- **Antumbra.** Mirrored and uncanny: names that are true the wrong way round. Time and direction are swapped (yesterday, hindward, widdershins), and light behaves badly (noonless, downflame). Examples: Widdershins Walk, Yesterday's Road, Hindmoor, Downflame Road, The Noonless Road.
- **Crownhaven.** Royal and ceremonial: named by decree and counted. Everything is the Sovereign's, the Accord's or one of eighteen. Examples: The Coronation Road, The Pilgrim Pass, Sovereign's Ascent, The Eighteen Gates, The Crownwall.
- **Borderlands** blend both voices (Frostwick Pass: an Elowen word for an Isenmar pass; the Icecutters' Haul: Isenmar work on a Zenith road).

## The Eighteen Roads (plus the Pilgrim Road)

| Road | Name | From -> to | Maps in order |
|---|---|---|---|
| 1 | The Strand Road | Ferrow's Landing -> Saltmere | The Ferrymen's Mile (520), Windfall Row (521) [branch], Lacecliff Walk (527), Marram Down (528) |
| 2 | The Weavers' Road | Saltmere -> Briarwick | The Grey Saltings (541), The Dyers' Ford (552), Thistledown Lea (540), Gossamer Wood (524) |
| 3 | The Hoar Road | Briarwick -> Ebbmouth | Spinners' Rise (566), Frostwick Pass (577), Rimewood Path (578), The Rimewood (562), Gullcry Cliffs (561), Frostflat Causeway (560) [side] |
| 4 | The Lock Road | Ebbmouth -> Lumen City | The Reedholms (580), The Icecutters' Haul (592), The Icefall Locks (581), The Arc-Lamp Mile (593) |
| 5 | The Brass Road | Lumen City -> Duneholt | The Meridian Mainline (612), The Brass Dunes (600), The Rib Road (601), Sunbleach Flats (613) |
| 6 | The Leach Road | Duneholt -> Mirefen | The Marrow Road (620), The Kneeling Stones (632), The Leach Canyons (621), The Gutterfall (633) |
| 7 | The Sulfur Road | Mirefen -> Cindervault | Leechman's Walk (640), Lake Sallow (641), The Pyre Road (652) |
| 8 | The Iron Road | Cindervault -> Ironreach | The Ashmarch (660), The Ironway (661), The Long Drop (672), The Cinderglass Barrens (662) [side], The Wyrmtongue (673) [side] |
| 9 | The Root Road | Ironreach -> Verdance | The Tailings (692), The Rootdeep (680), Prism Falls (681), The Briarway (693) |
| 10 | The Hart Road | Verdance -> Rimeholt | The Hart's Run (700), The Hoarwood (701), The Whalebone Road (712) |
| 11 | The Mast Road | Rimeholt -> Skyreach | The Thane's Sled-Road (720), The Mast Glacier (721), The Tetherline (732) |
| 12 | The Glass Road | Skyreach -> Lucent | Conductors' Causeway (740), The Wired Wood (741), The Looking-Glass Wood (752), Widdershins Walk (755) |
| 13 | The Grave Road | Lucent -> Cragholm | Yesterday's Road (772), The Obsidian Barrows (760), Spinefall Gorge (761), The Vertebrae (773) |
| 14 | The Moor Road | Cragholm -> Gravenmoor | The Jawbone Ridge (780), Hindmoor (781), Downflame Road (790) |
| 15 | The Slag Road | Gravenmoor -> Cogsworth | The Noonless Road (800), The Dry Tide (810), The Slag Mesa (801), The Smokestack Parade (811) |
| 16 | The Drowned Road | Cogsworth -> Underveil | The Brink (832), The Hanging Stair (820), The Drownings (821) |
| 17 | The Blind Road | Underveil -> Gloaming | The Throat (852), The Blindwater (840), The Gloamwood Verge (841) |
| 18 | The Truce Road | Gloaming -> Wyrmrest | The Gloamwood (860), The Thornwar Marches (861), The Wyrmspine (872) |
| 19 | The Pilgrim Road | Wyrmrest -> Crownhaven | Dominar's Toll (892), The Pilgrim Pass (880), The Coronation Road (893) |

## Every map

`Status`: renamed / new / kept. `Square` = town-map square (x, y) on region 0 (Velmora). The rename script
uses rows whose Old and New differ.

| ID | Old name | New name | Status | Kingdom | Square | Origin |
|---|---|---|---|---|---|---|
| 100 | Ferrow's Landing | Ferrow's Landing | kept | Elowen | 12, 18 | The ferry lands here and nowhere else; Old Ferrow ran the first boat across the Hallow Strait. |
| 101 | Ferrow's Landing Pokémon Center | Ferrow's Landing Pokémon Center | kept | Elowen | 12, 18 |  |
| 102 | Ferrow's Landing Mart | Ferrow's Landing Mart | kept | Elowen | 12, 18 |  |
| 103 | Larch Research Station | Larch Research Station | kept | Elowen | 12, 18 |  |
| 104 | Tidewater Inn | Tidewater Inn | kept | Elowen | 12, 18 |  |
| 105 | Ferrow Lighthouse 1F | Ferrow Lighthouse 1F | kept | Elowen | 12, 18 |  |
| 106 | Ferrow Lighthouse Lamp Room | Ferrow Lighthouse Lamp Room | kept | Elowen | 12, 18 |  |
| 107 | Dockmaster's House | Dockmaster's House | kept | Elowen | 12, 18 |  |
| 108 | Quarantine Customs Hall | Quarantine Customs Hall | kept | Elowen | 12, 18 |  |
| 109 | The Dovetail - Deck | The Dovetail - Deck | kept | Elowen | 12, 19 |  |
| 110 | The Dovetail - Cabin | The Dovetail - Cabin | kept | Elowen | 12, 19 |  |
| 120 | Briarwick | Briarwick | kept | Elowen | 11, 13 | Briar-wick, the dairy-farm in the briars, before the weavers came and the farm became a loom-town. |
| 121 | Briarwick Pokémon Center | Briarwick Pokémon Center | kept | Elowen | 11, 13 |  |
| 122 | Briarwick Mart | Briarwick Mart | kept | Elowen | 11, 13 |  |
| 123 | Weavers' Guildhall | Weavers' Guildhall | kept | Elowen | 11, 13 |  |
| 124 | Treetop House | Treetop House | kept | Elowen | 11, 13 |  |
| 125 | Cutter's House | Cutter's House | kept | Elowen | 11, 13 |  |
| 130 | Loomhouse Gym - Foyer | Loomhouse Gym - Foyer | kept | Elowen | 11, 13 |  |
| 131 | Loomhouse Gym - Weaving Hall | Loomhouse Gym - Weaving Hall | kept | Elowen | 11, 13 |  |
| 132 | Loomhouse Gym - Canopy Lofts | Loomhouse Gym - Canopy Lofts | kept | Elowen | 11, 13 |  |
| 133 | Loomhouse Gym - The Spindle | Loomhouse Gym - The Spindle | kept | Elowen | 11, 13 |  |
| 134 | Loomhouse Upper Lofts - Granny's Knot | Loomhouse Upper Lofts - Granny's Knot | kept | Elowen | 11, 13 |  |
| 140 | Saltmere - Promenade & Market | Saltmere - Promenade & Market | kept | Elowen | 6, 18 | A salt lake behind a sandbar: the town's wealth and its name. Elowen's chartered free port. |
| 141 | Saltmere Pokémon Center | Saltmere Pokémon Center | kept | Elowen | 6, 18 |  |
| 142 | Saltmere Mart | Saltmere Mart | kept | Elowen | 6, 18 |  |
| 143 | Saltmere Harbour Office | Saltmere Harbour Office | kept | Elowen | 6, 18 |  |
| 144 | Saltwife's House | Saltwife's House | kept | Elowen | 6, 18 |  |
| 145 | Lantern Theatre | Lantern Theatre | kept | Elowen | 6, 18 |  |
| 146 | Saltmere - Harbour & Breakwater | Saltmere - Harbour & Breakwater | kept | Elowen | 6, 18 |  |
| 147 | Saltmere - Old Town | Saltmere - Old Town | kept | Elowen | 6, 18 |  |
| 150 | Pell Playhouse - Foyer | Pell Playhouse - Foyer | kept | Elowen | 6, 18 |  |
| 151 | Pell Playhouse - Revolving Stage | Pell Playhouse - Revolving Stage | kept | Elowen | 6, 18 |  |
| 152 | Pell Playhouse - Fly Loft | Pell Playhouse - Fly Loft | kept | Elowen | 6, 18 |  |
| 153 | Pell Playhouse - Dressing Rooms | Pell Playhouse - Dressing Rooms | kept | Elowen | 6, 18 |  |
| 154 | Pell Playhouse - The Grand Stage | Pell Playhouse - The Grand Stage | kept | Elowen | 6, 18 |  |
| 160 | Ebbmouth | Ebbmouth | kept | Isenmar | 3, 7 | Where the River Ebb meets the sea, and where the Ebb runs both ways. |
| 161 | Ebbmouth Pokémon Center | Ebbmouth Pokémon Center | kept | Isenmar | 3, 7 |  |
| 162 | Ebbmouth Mart | Ebbmouth Mart | kept | Isenmar | 3, 7 |  |
| 163 | Anglers' Guild | Anglers' Guild | kept | Isenmar | 3, 7 |  |
| 164 | Reyes House | Reyes House | kept | Isenmar | 3, 7 |  |
| 165 | Net-mender's House | Net-mender's House | kept | Isenmar | 3, 7 |  |
| 166 | Reyes Cellar (Hollow cell) | Reyes Cellar (Hollow cell) | kept | Isenmar | 3, 7 |  |
| 167 | Ebbmouth - Mill Quay | Ebbmouth - Mill Quay | kept | Isenmar | 3, 7 |  |
| 170 | Tidelock Gym - Lock Hall | Tidelock Gym - Lock Hall | kept | Isenmar | 3, 7 |  |
| 171 | Tidelock Gym - Basins (Low Water) | Tidelock Gym - Basins (Low Water) | kept | Isenmar | 3, 7 |  |
| 172 | Tidelock Gym - Basins (Mid Water) | Tidelock Gym - Basins (Mid Water) | kept | Isenmar | 3, 7 |  |
| 173 | Tidelock Gym - Basins (High Water) | Tidelock Gym - Basins (High Water) | kept | Isenmar | 3, 7 |  |
| 174 | Tidelock Gym - Warden's Pool | Tidelock Gym - Warden's Pool | kept | Isenmar | 3, 7 |  |
| 180 | Lumen City - Concourse | Lumen City - Concourse | kept | Zenith | 12, 5 | The first city lit all night; Zenith named it for the light and has not let anyone forget. |
| 181 | Lumen City - Lowlight | Lumen City - Lowlight | kept | Zenith | 12, 5 |  |
| 182 | Lumen City Pokémon Center | Lumen City Pokémon Center | kept | Zenith | 12, 5 |  |
| 183 | Lumen Arcade Dept. Store 1F | Lumen Arcade Dept. Store 1F | kept | Zenith | 12, 5 |  |
| 184 | Lumen Arcade Dept. Store 2F | Lumen Arcade Dept. Store 2F | kept | Zenith | 12, 5 |  |
| 185 | Meridian Spire - Lobby | Meridian Spire - Lobby | kept | Zenith | 12, 5 |  |
| 186 | Meridian Spire - Gala Hall | Meridian Spire - Gala Hall | kept | Zenith | 12, 5 |  |
| 187 | Glide Cycle Shop | Glide Cycle Shop | kept | Zenith | 12, 5 |  |
| 188 | Lumen Fossil Lab | Lumen Fossil Lab | kept | Zenith | 12, 5 |  |
| 189 | Lumen Apartment | Lumen Apartment | kept | Zenith | 12, 5 |  |
| 190 | Circuit Gym - Switchroom | Circuit Gym - Switchroom | kept | Zenith | 12, 5 |  |
| 191 | Circuit Gym - Breadboard Hall | Circuit Gym - Breadboard Hall | kept | Zenith | 12, 5 |  |
| 192 | Circuit Gym - Blackout Grid | Circuit Gym - Blackout Grid | kept | Zenith | 12, 5 |  |
| 193 | Circuit Gym - Core | Circuit Gym - Core | kept | Zenith | 12, 5 |  |
| 194 | Lumen City - Council Ward | Lumen City - Council Ward | kept | Zenith | 12, 5 |  |
| 195 | Lumen City - Spire District | Lumen City - Spire District | kept | Zenith | 12, 5 |  |
| 196 | Lumen City - Skyport Terrace | Lumen City - Skyport Terrace | kept | Zenith | 12, 5 |  |
| 197 | Zenith Council Hall - Council Chamber | Zenith Council Hall - Council Chamber | kept | Zenith | 12, 5 |  |
| 198 | Meridian Spire - Executive Gallery | Meridian Spire - Executive Gallery | kept | Zenith | 12, 5 |  |
| 199 | Meridian Spire - Dark Stone Core | Meridian Spire - Dark Stone Core | kept | Zenith | 12, 5 |  |
| 200 | Duneholt - Terrace Bazaar | Duneholt - Terrace Bazaar | kept | Ossaria | 22, 4 | Dune-holt: the hold among the dunes, carved into canyon walls by the first Electors. |
| 201 | Duneholt Pokémon Center | Duneholt Pokémon Center | kept | Ossaria | 22, 4 |  |
| 202 | Duneholt Mart | Duneholt Mart | kept | Ossaria | 22, 4 |  |
| 203 | Duneholt - Sandgate | Duneholt - Sandgate | kept | Ossaria | 22, 4 |  |
| 204 | Duneholt - Aquifer Quarter | Duneholt - Aquifer Quarter | kept | Ossaria | 22, 4 |  |
| 205 | Elector's Palace - Courtyard | Elector's Palace - Courtyard | kept | Ossaria | 22, 4 |  |
| 206 | Elector's Palace - Hall of Audience | Elector's Palace - Hall of Audience | kept | Ossaria | 22, 4 |  |
| 207 | Elector's Palace - Mural Gallery | Elector's Palace - Mural Gallery | kept | Ossaria | 22, 4 |  |
| 208 | Necropolis of the Electors | Necropolis of the Electors | kept | Ossaria | 22, 4 |  |
| 209 | Sahar's Dig Lab | Sahar's Dig Lab | kept | Ossaria | 22, 4 |  |
| 210 | Duneholt Gym - Entrance | Duneholt Gym - Entrance | kept | Ossaria | 22, 4 |  |
| 211 | Duneholt Gym - Puzzle Room 1 | Duneholt Gym - Puzzle Room 1 | kept | Ossaria | 22, 4 |  |
| 212 | Duneholt Gym - Puzzle Room 2 | Duneholt Gym - Puzzle Room 2 | kept | Ossaria | 22, 4 |  |
| 213 | Duneholt Gym - Warden Arena | Duneholt Gym - Warden Arena | kept | Ossaria | 22, 4 |  |
| 214 | Duneholt - Sinkwells | Duneholt - Sinkwells | kept | Ossaria | 22, 4 |  |
| 220 | Mirefen | Mirefen | kept | Nadir | 16, 9 | The mire-fen at the foot of Zenith's outfall; the name is a description, not a boast. |
| 221 | Mirefen Pokémon Center | Mirefen Pokémon Center | kept | Nadir | 16, 9 |  |
| 222 | Mirefen Mart | Mirefen Mart | kept | Nadir | 16, 9 |  |
| 223 | Corvin Mott's Infirmary | Corvin Mott's Infirmary | kept | Nadir | 16, 9 |  |
| 230 | Mirefen Gym - Entrance | Mirefen Gym - Entrance | kept | Nadir | 16, 9 |  |
| 231 | Mirefen Gym - Puzzle Room 1 | Mirefen Gym - Puzzle Room 1 | kept | Nadir | 16, 9 |  |
| 232 | Mirefen Gym - Puzzle Room 2 | Mirefen Gym - Puzzle Room 2 | kept | Nadir | 16, 9 |  |
| 233 | Mirefen Gym - Warden Arena | Mirefen Gym - Warden Arena | kept | Nadir | 16, 9 |  |
| 240 | Cindervault - Forge Terraces | Cindervault - Forge Terraces | kept | Ashkaar | 24, 10 | The vault of cinders: the Dominion's seat in the caldera rim, built on the ash of the old one. |
| 241 | Cindervault Pokémon Center | Cindervault Pokémon Center | kept | Ashkaar | 24, 10 |  |
| 242 | Cindervault Mart | Cindervault Mart | kept | Ashkaar | 24, 10 |  |
| 243 | Cindervault - Caldera Gate | Cindervault - Caldera Gate | kept | Ashkaar | 24, 10 |  |
| 244 | Hearthguild Hall | Hearthguild Hall | kept | Ashkaar | 24, 10 |  |
| 245 | Pyre Keep - Rampart | Pyre Keep - Rampart | kept | Ashkaar | 24, 10 |  |
| 246 | Pyre Keep - Ember Throne | Pyre Keep - Ember Throne | kept | Ashkaar | 24, 10 |  |
| 247 | Pyre Keep - Hall of Oaths | Pyre Keep - Hall of Oaths | kept | Ashkaar | 24, 10 |  |
| 248 | Pyre Keep - Dragon Roosts | Pyre Keep - Dragon Roosts | kept | Ashkaar | 24, 10 |  |
| 249 | Cindervault - Slag Ward | Cindervault - Slag Ward | kept | Ashkaar | 24, 10 |  |
| 250 | Cindervault Gym - Entrance | Cindervault Gym - Entrance | kept | Ashkaar | 24, 10 |  |
| 251 | Cindervault Gym - Puzzle Room 1 | Cindervault Gym - Puzzle Room 1 | kept | Ashkaar | 24, 10 |  |
| 252 | Cindervault Gym - Puzzle Room 2 | Cindervault Gym - Puzzle Room 2 | kept | Ashkaar | 24, 10 |  |
| 253 | Cindervault Gym - Warden Arena | Cindervault Gym - Warden Arena | kept | Ashkaar | 24, 10 |  |
| 254 | Pyre Keep - Ancestor Crypts | Pyre Keep - Ancestor Crypts | kept | Ashkaar | 24, 10 |  |
| 260 | Ironreach | Ironreach | kept | Nadir | 17, 11 | Iron-reach: as far down as the iron goes, and then the pit-fighters went further. |
| 261 | Ironreach Pokémon Center | Ironreach Pokémon Center | kept | Nadir | 17, 11 |  |
| 262 | Ironreach Mart | Ironreach Mart | kept | Nadir | 17, 11 |  |
| 263 | The Iron Pit | The Iron Pit | kept | Nadir | 17, 11 |  |
| 270 | Ironreach Gym - Entrance | Ironreach Gym - Entrance | kept | Nadir | 17, 11 |  |
| 271 | Ironreach Gym - Puzzle Room 1 | Ironreach Gym - Puzzle Room 1 | kept | Nadir | 17, 11 |  |
| 272 | Ironreach Gym - Puzzle Room 2 | Ironreach Gym - Puzzle Room 2 | kept | Nadir | 17, 11 |  |
| 273 | Ironreach Gym - Puzzle Room 3 | Ironreach Gym - Puzzle Room 3 | kept | Nadir | 17, 11 |  |
| 274 | Ironreach Gym - Warden Arena | Ironreach Gym - Warden Arena | kept | Nadir | 17, 11 |  |
| 280 | Verdance - Market Terraces | Verdance - Market Terraces | kept | Elowen | 9, 10 | Green-ance: the Evergreen Crown's seat, where nothing has wilted in three hundred years. |
| 281 | Verdance Pokémon Center | Verdance Pokémon Center | kept | Elowen | 9, 10 |  |
| 282 | Verdance Mart | Verdance Mart | kept | Elowen | 9, 10 |  |
| 283 | Verdance - Glasshouse Ward | Verdance - Glasshouse Ward | kept | Elowen | 9, 10 |  |
| 284 | Verdance - Kingsgate Barbican | Verdance - Kingsgate Barbican | kept | Elowen | 9, 10 |  |
| 285 | Briar Hall - Upper Court | Briar Hall - Upper Court | kept | Elowen | 9, 10 |  |
| 286 | Briar Hall - Great Hall | Briar Hall - Great Hall | kept | Elowen | 9, 10 |  |
| 287 | Briar Hall - Throne Room | Briar Hall - Throne Room | kept | Elowen | 9, 10 |  |
| 288 | Briar Hall - Royal Gallery | Briar Hall - Royal Gallery | kept | Elowen | 9, 10 |  |
| 289 | Briar Hall - Thorn Crypts | Briar Hall - Thorn Crypts | kept | Elowen | 9, 10 |  |
| 290 | Verdance Gym - Entrance | Verdance Gym - Entrance | kept | Elowen | 9, 10 |  |
| 291 | Verdance Gym - Puzzle Room 1 | Verdance Gym - Puzzle Room 1 | kept | Elowen | 9, 10 |  |
| 292 | Verdance Gym - Puzzle Room 2 | Verdance Gym - Puzzle Room 2 | kept | Elowen | 9, 10 |  |
| 293 | Verdance Gym - Warden Arena | Verdance Gym - Warden Arena | kept | Elowen | 9, 10 |  |
| 294 | The Heartgarden | The Heartgarden | kept | Elowen | 9, 10 |  |
| 295 | Cathedral of the Evergreen | Cathedral of the Evergreen | kept | Elowen | 9, 10 |  |
| 296 | Verdance - Rootward | Verdance - Rootward | kept | Elowen | 9, 10 |  |
| 300 | Rimeholt - Thane's Harbour | Rimeholt - Thane's Harbour | kept | Isenmar | 3, 2 | Rime-holt: the hold on the rime, a fortress-port standing on Lake Rime's ice. |
| 301 | Rimeholt Pokémon Center | Rimeholt Pokémon Center | kept | Isenmar | 3, 2 |  |
| 302 | Rimeholt Mart | Rimeholt Mart | kept | Isenmar | 3, 2 |  |
| 303 | Rimeholt - Icewall Gate | Rimeholt - Icewall Gate | kept | Isenmar | 3, 2 |  |
| 304 | Rimeholt - Sled Market | Rimeholt - Sled Market | kept | Isenmar | 3, 2 |  |
| 305 | Whalebone Keep - Bailey | Whalebone Keep - Bailey | kept | Isenmar | 3, 2 |  |
| 306 | Whalebone Keep - Mead Hall | Whalebone Keep - Mead Hall | kept | Isenmar | 3, 2 |  |
| 307 | Whalebone Keep - Thane's Seat | Whalebone Keep - Thane's Seat | kept | Isenmar | 3, 2 |  |
| 308 | Whalebone Keep - Ice Vault | Whalebone Keep - Ice Vault | kept | Isenmar | 3, 2 |  |
| 309 | Rimeholt - Sinking Quarter | Rimeholt - Sinking Quarter | kept | Isenmar | 3, 2 |  |
| 310 | Rimeholt Gym - Entrance | Rimeholt Gym - Entrance | kept | Isenmar | 3, 2 |  |
| 311 | Rimeholt Gym - Puzzle Room 1 | Rimeholt Gym - Puzzle Room 1 | kept | Isenmar | 3, 2 |  |
| 312 | Rimeholt Gym - Puzzle Room 2 | Rimeholt Gym - Puzzle Room 2 | kept | Isenmar | 3, 2 |  |
| 313 | Rimeholt Gym - Warden Arena | Rimeholt Gym - Warden Arena | kept | Isenmar | 3, 2 |  |
| 314 | Rimeholt - Net Row | Rimeholt - Net Row | kept | Isenmar | 3, 2 |  |
| 320 | Skyreach - Mast Ward | Skyreach - Mast Ward | kept | Zenith | 10, 3 | The spire that reaches the sky-roads; Zenith's airship port. |
| 321 | Skyreach Pokémon Center | Skyreach Pokémon Center | kept | Zenith | 10, 3 |  |
| 322 | Skyreach Mart | Skyreach Mart | kept | Zenith | 10, 3 |  |
| 323 | Skyreach - Lower Gantries | Skyreach - Lower Gantries | kept | Zenith | 10, 3 |  |
| 324 | Skyreach - Skybridge Ward | Skyreach - Skybridge Ward | kept | Zenith | 10, 3 |  |
| 325 | Gale Post Hall | Gale Post Hall | kept | Zenith | 10, 3 |  |
| 326 | Skyreach - Smugglers' Gantry | Skyreach - Smugglers' Gantry | kept | Zenith | 10, 3 |  |
| 330 | Skyreach Gym - Entrance | Skyreach Gym - Entrance | kept | Zenith | 10, 3 |  |
| 331 | Skyreach Gym - Puzzle Room 1 | Skyreach Gym - Puzzle Room 1 | kept | Zenith | 10, 3 |  |
| 332 | Skyreach Gym - Puzzle Room 2 | Skyreach Gym - Puzzle Room 2 | kept | Zenith | 10, 3 |  |
| 333 | Skyreach Gym - Warden Arena | Skyreach Gym - Warden Arena | kept | Zenith | 10, 3 |  |
| 340 | Lucent - Athenaeum Quarter | Lucent - Athenaeum Quarter | kept | Antumbra | 28, 16 | The light that comes from nowhere in the kingdom behind the glass. |
| 341 | Lucent Pokémon Center | Lucent Pokémon Center | kept | Antumbra | 28, 16 |  |
| 342 | Lucent Mart | Lucent Mart | kept | Antumbra | 28, 16 |  |
| 343 | Lucent - Tribunal Ward | Lucent - Tribunal Ward | kept | Antumbra | 28, 16 |  |
| 344 | Lucent Athenaeum - Great Reading Hall | Lucent Athenaeum - Great Reading Hall | kept | Antumbra | 28, 16 |  |
| 345 | Lucent Athenaeum - Sealed Stacks | Lucent Athenaeum - Sealed Stacks | kept | Antumbra | 28, 16 |  |
| 346 | The Speculum - Mirror City | The Speculum - Mirror City | kept | Antumbra | 28, 16 |  |
| 347 | Palace of Glass - Gate of Veils | Palace of Glass - Gate of Veils | kept | Antumbra | 28, 16 |  |
| 348 | Palace of Glass - Hall of Mirrors | Palace of Glass - Hall of Mirrors | kept | Antumbra | 28, 16 |  |
| 349 | Palace of Glass - Veiled Throne | Palace of Glass - Veiled Throne | kept | Antumbra | 28, 16 |  |
| 350 | Lucent Gym - Entrance | Lucent Gym - Entrance | kept | Antumbra | 28, 16 |  |
| 351 | Lucent Gym - Puzzle Room 1 | Lucent Gym - Puzzle Room 1 | kept | Antumbra | 28, 16 |  |
| 352 | Lucent Gym - Puzzle Room 2 | Lucent Gym - Puzzle Room 2 | kept | Antumbra | 28, 16 |  |
| 353 | Lucent Gym - Puzzle Room 3 | Lucent Gym - Puzzle Room 3 | kept | Antumbra | 28, 16 |  |
| 354 | Lucent Gym - Warden Arena | Lucent Gym - Warden Arena | kept | Antumbra | 28, 16 |  |
| 355 | Palace of Glass - Undercroft of Echoes | Palace of Glass - Undercroft of Echoes | kept | Antumbra | 28, 16 |  |
| 360 | Cragholm | Cragholm | kept | Ossaria | 24, 2 | Crag-holm: the island of rock in the crags, where Ossaria cut its lift-galleries. |
| 361 | Cragholm Pokémon Center | Cragholm Pokémon Center | kept | Ossaria | 24, 2 |  |
| 362 | Cragholm Mart | Cragholm Mart | kept | Ossaria | 24, 2 |  |
| 363 | Cragholm - Lift Galleries | Cragholm - Lift Galleries | kept | Ossaria | 24, 2 |  |
| 370 | Cragholm Gym - Entrance | Cragholm Gym - Entrance | kept | Ossaria | 24, 2 |  |
| 371 | Cragholm Gym - Puzzle Room 1 | Cragholm Gym - Puzzle Room 1 | kept | Ossaria | 24, 2 |  |
| 372 | Cragholm Gym - Puzzle Room 2 | Cragholm Gym - Puzzle Room 2 | kept | Ossaria | 24, 2 |  |
| 373 | Cragholm Gym - Warden Arena | Cragholm Gym - Warden Arena | kept | Ossaria | 24, 2 |  |
| 380 | Gravenmoor | Gravenmoor | kept | Antumbra | 27, 18 | The grave-moor: Antumbra buries above ground and walks below it. |
| 381 | Gravenmoor Pokémon Center | Gravenmoor Pokémon Center | kept | Antumbra | 27, 18 |  |
| 382 | Gravenmoor Mart | Gravenmoor Mart | kept | Antumbra | 27, 18 |  |
| 383 | Vane Hall | Vane Hall | kept | Antumbra | 27, 18 |  |
| 384 | Lantern Hospice | Lantern Hospice | kept | Antumbra | 27, 18 |  |
| 390 | Gravenmoor Gym - Entrance | Gravenmoor Gym - Entrance | kept | Antumbra | 27, 18 |  |
| 391 | Gravenmoor Gym - Puzzle Room 1 | Gravenmoor Gym - Puzzle Room 1 | kept | Antumbra | 27, 18 |  |
| 392 | Gravenmoor Gym - Puzzle Room 2 | Gravenmoor Gym - Puzzle Room 2 | kept | Antumbra | 27, 18 |  |
| 393 | Gravenmoor Gym - Puzzle Room 3 | Gravenmoor Gym - Puzzle Room 3 | kept | Antumbra | 27, 18 |  |
| 394 | Gravenmoor Gym - Warden Arena | Gravenmoor Gym - Warden Arena | kept | Antumbra | 27, 18 |  |
| 400 | Cogsworth | Cogsworth | kept | Zenith | 16, 2 | Named for the cog-works of its founding patent and the worth of what it makes. |
| 401 | Cogsworth Pokémon Center | Cogsworth Pokémon Center | kept | Zenith | 16, 2 |  |
| 402 | Cogsworth Mart | Cogsworth Mart | kept | Zenith | 16, 2 |  |
| 403 | Strade Works - Foundry Floor | Strade Works - Foundry Floor | kept | Zenith | 16, 2 |  |
| 410 | Cogsworth Gym - Entrance | Cogsworth Gym - Entrance | kept | Zenith | 16, 2 |  |
| 411 | Cogsworth Gym - Puzzle Room 1 | Cogsworth Gym - Puzzle Room 1 | kept | Zenith | 16, 2 |  |
| 412 | Cogsworth Gym - Puzzle Room 2 | Cogsworth Gym - Puzzle Room 2 | kept | Zenith | 16, 2 |  |
| 413 | Cogsworth Gym - Warden Arena | Cogsworth Gym - Warden Arena | kept | Zenith | 16, 2 |  |
| 420 | Underveil - Lantern Tiers | Underveil - Lantern Tiers | kept | Nadir | 12, 1 | Under the veil of the sea, in the upper towers of drowned Aurelia. |
| 421 | Underveil Pokémon Center | Underveil Pokémon Center | kept | Nadir | 12, 1 |  |
| 422 | Underveil Mart | Underveil Mart | kept | Nadir | 12, 1 |  |
| 423 | Underveil - Moon Market | Underveil - Moon Market | kept | Nadir | 12, 1 |  |
| 424 | Underveil - Sump Docks | Underveil - Sump Docks | kept | Nadir | 12, 1 |  |
| 425 | Underveil - Barons' Stair | Underveil - Barons' Stair | kept | Nadir | 12, 1 |  |
| 426 | Underveil - Bell Tower of Aurel | Underveil - Bell Tower of Aurel | kept | Nadir | 12, 1 |  |
| 427 | Nyx's Hall of Whispers | Nyx's Hall of Whispers | kept | Nadir | 12, 1 |  |
| 429 | Drowned Cathedral of Aurel | Drowned Cathedral of Aurel | kept | Nadir | 12, 1 |  |
| 430 | Underveil Gym - Entrance | Underveil Gym - Entrance | kept | Nadir | 12, 1 |  |
| 431 | Underveil Gym - Puzzle Room 1 | Underveil Gym - Puzzle Room 1 | kept | Nadir | 12, 1 |  |
| 432 | Underveil Gym - Puzzle Room 2 | Underveil Gym - Puzzle Room 2 | kept | Nadir | 12, 1 |  |
| 433 | Underveil Gym - Warden Arena | Underveil Gym - Warden Arena | kept | Nadir | 12, 1 |  |
| 440 | Gloaming | Gloaming | kept | Elowen | 16, 17 | The town at Elowen's heart, where it has been dusk for three hundred years. |
| 441 | Gloaming Pokémon Center | Gloaming Pokémon Center | kept | Elowen | 16, 17 |  |
| 442 | Gloaming Mart | Gloaming Mart | kept | Elowen | 16, 17 |  |
| 443 | Great Tree Roots | Great Tree Roots | kept | Elowen | 16, 17 |  |
| 450 | Gloaming Gym - Entrance | Gloaming Gym - Entrance | kept | Elowen | 16, 17 |  |
| 451 | Gloaming Gym - Puzzle Room 1 | Gloaming Gym - Puzzle Room 1 | kept | Elowen | 16, 17 |  |
| 452 | Gloaming Gym - Puzzle Room 2 | Gloaming Gym - Puzzle Room 2 | kept | Elowen | 16, 17 |  |
| 453 | Gloaming Gym - Puzzle Room 3 | Gloaming Gym - Puzzle Room 3 | kept | Elowen | 16, 17 |  |
| 454 | Gloaming Gym - Warden Arena | Gloaming Gym - Warden Arena | kept | Elowen | 16, 17 |  |
| 460 | Wyrmrest | Wyrmrest | kept | Ashkaar | 24, 15 | Where the wyrms rest: the roost-citadel on the Wyrmspine. |
| 461 | Wyrmrest Pokémon Center | Wyrmrest Pokémon Center | kept | Ashkaar | 24, 15 |  |
| 462 | Wyrmrest Mart | Wyrmrest Mart | kept | Ashkaar | 24, 15 |  |
| 470 | Wyrmrest Gym - Entrance | Wyrmrest Gym - Entrance | kept | Ashkaar | 24, 15 |  |
| 471 | Wyrmrest Gym - Puzzle Room 1 | Wyrmrest Gym - Puzzle Room 1 | kept | Ashkaar | 24, 15 |  |
| 472 | Wyrmrest Gym - Puzzle Room 2 | Wyrmrest Gym - Puzzle Room 2 | kept | Ashkaar | 24, 15 |  |
| 473 | Wyrmrest Gym - Puzzle Room 3 | Wyrmrest Gym - Puzzle Room 3 | kept | Ashkaar | 24, 15 |  |
| 474 | Wyrmrest Gym - Warden Arena | Wyrmrest Gym - Warden Arena | kept | Ashkaar | 24, 15 |  |
| 480 | Lower Crownhaven | Lower Crownhaven | kept | Crownhaven | 19, 14 | The haven of the Crown: the Accord's capital, the only city all seven kingdoms agreed to. |
| 481 | Crownhaven Pokémon Center | Crownhaven Pokémon Center | kept | Crownhaven | 19, 14 |  |
| 482 | Crownhaven - The Eighteen Gates | Crownhaven - The Eighteen Gates | kept | Crownhaven | 19, 14 |  |
| 483 | Upper Crownhaven - Basilica Close | Upper Crownhaven - Basilica Close | kept | Crownhaven | 19, 14 |  |
| 484 | Basilica of First Light | Basilica of First Light | kept | Crownhaven | 19, 14 |  |
| 485 | Basilica Crypts | Basilica Crypts | kept | Crownhaven | 19, 14 |  |
| 486 | Accord Palace - Court of Wardens | Accord Palace - Court of Wardens | kept | Crownhaven | 19, 14 |  |
| 487 | Accord Palace - Sovereign's Throne Room | Accord Palace - Sovereign's Throne Room | kept | Crownhaven | 19, 14 |  |
| 488 | Accord Palace - Gallery of Plates | Accord Palace - Gallery of Plates | kept | Crownhaven | 19, 14 |  |
| 489 | Glassfall Memorial Garden | Glassfall Memorial Garden | kept | Crownhaven | 19, 14 |  |
| 490 | Temple-Arena of the Blessing - Hall of Eighteen Doors | Temple-Arena of the Blessing - Hall of Eighteen Doors | kept | Crownhaven | 19, 14 |  |
| 491 | Temple-Arena of the Blessing - Altar Stage | Temple-Arena of the Blessing - Altar Stage | kept | Crownhaven | 19, 14 |  |
| 492 | Accord Palace - Entrance Hall | Accord Palace - Entrance Hall | kept | Crownhaven | 19, 14 |  |
| 493 | Concordance Spire - Lobby (Battle Tower) | Concordance Spire - Lobby (Battle Tower) | kept | Crownhaven | 19, 14 |  |
| 494 | Concordance Spire - Arena | Concordance Spire - Arena | kept | Crownhaven | 19, 14 |  |
| 495 | Temple-Arena of the Blessing - Processional Plaza | Temple-Arena of the Blessing - Processional Plaza | kept | Crownhaven | 19, 14 |  |
| 496 | Lower Crownhaven - Market Ring | Lower Crownhaven - Market Ring | kept | Crownhaven | 19, 14 |  |
| 497 | Lower Crownhaven - Pilgrims' Quarter | Lower Crownhaven - Pilgrims' Quarter | kept | Crownhaven | 19, 14 |  |
| 498 | Concordance Spire - Exterior | Concordance Spire - Exterior | kept | Crownhaven | 19, 14 |  |
| 499 | Festival Grounds - Court of Eight Pavilions | Festival Grounds - Court of Eight Pavilions | kept | Crownhaven | 19, 14 |  |
| 520 | Route 1 | The Ferrymen's Mile | renamed | Elowen | 12, 17 | The mile the ferrymen walked each dusk to ring the Hale bell once the last boat was in. |
| 521 | Route 2 | Windfall Row | renamed | Elowen | 12, 16 | Orchard law: a traveller may keep any fruit that has already fallen, and nothing else. |
| 522 | The Glassed Orchard | The Glassed Orchard | kept | Elowen | 14, 16 |  |
| 523 | Hale Farmhouse | Hale Farmhouse | kept | Elowen | 12, 16 |  |
| 524 | Gossamer Wood | Gossamer Wood | kept | Elowen | 11, 15 | Kept name: the silk forest that gives Briarwick its trade. |
| 525 | Gossamer Deepwood | Gossamer Deepwood | kept | Elowen | 12, 14 |  |
| 526 | Woodward's Hut | Woodward's Hut | kept | Elowen | 11, 14 |  |
| 527 | - | Lacecliff Walk | new | Elowen | 11, 18 | The sea has worn the chalk into arches as fine as Briarwick lace; the weavers copy the cliffs, not the other way round. |
| 528 | - | Marram Down | new | Elowen | 8, 18 | Dune-down held together by marram grass. Saltmere fines anyone who pulls it up, which is why it is still here. |
| 540 | Route 3 | Thistledown Lea | renamed | Elowen | 9, 15 | The river meadows held by House Thistledown until the house died out. Nobody has mown them since. |
| 541 | Route 4 | The Grey Saltings | renamed | Elowen | 6, 17 | Saltmere's salt comes from this marsh. 'Grey' is the salt before it is washed, and the weather. |
| 542 | Marsh Rest House | The Brinewife's Rest | renamed | Elowen | 6, 17 | A salt-boiler's widow keeps a bed for anyone the marsh has soaked. |
| 544 | Brinecut Mine 1F | Brinecut Mine 1F | kept | Borderland (Elowen/Ossaria) | 8, 16 |  |
| 545 | Brinecut Mine B1F | Brinecut Mine B1F | kept | Borderland (Elowen/Ossaria) | 8, 16 |  |
| 546 | Thistledown Manor | Thistledown Manor | kept | Elowen | 9, 14 |  |
| 547 | Thistledown Manor - Attic | Thistledown Manor - Attic | kept | Elowen | 9, 14 |  |
| 548 | Cocoonfall Hollow | Cocoonfall Hollow | kept | Elowen | 10, 14 |  |
| 552 | - | The Dyers' Ford | new | Elowen | 8, 15 | Briarwick's dyers wash their cloth here, so the river runs red, blue and yellow in three bands. |
| 560 | Route 5 - Frostflat Causeway | Frostflat Causeway | renamed | Borderland (Elowen/Isenmar) | 5, 17 | The raised salt road up the coast from Saltmere. Halfway along, the white underfoot stops being salt. |
| 561 | Route 6 - Gullcry Cliffs | Gullcry Cliffs | renamed | Isenmar | 3, 9 | First true Isenmar ground. Named for the noise, which never stops. |
| 562 | The Rimewood | The Rimewood | kept | Borderland (Elowen/Isenmar) | 5, 10 | Kept name: the Elowen oldwood that froze when the sea did. |
| 563 | Rimewood Glade | Rimewood Glade | kept | Borderland (Elowen/Isenmar) | 6, 10 |  |
| 564 | Gullcry Caves 1F | Gullcry Caves 1F | kept | Isenmar | 2, 8 |  |
| 565 | Gullcry Caves B1F | Gullcry Caves B1F | kept | Isenmar | 2, 8 |  |
| 566 | - | Spinners' Rise | new | Elowen | 10, 12 | The drove road up out of the Gossamer where Briarwick's spinners met the hill shepherds to buy fleece. |
| 568 | The Rehearsal | The Rehearsal | kept | Elowen | 4, 15 |  |
| 570 | Frostwick | Frostwick | kept | Borderland (Elowen/Isenmar) | 6, 12 | Frost-wick, the frost farm: Elowen named it for the cold and Isenmar for the farm. |
| 571 | Frostwick Pokémon Center | Frostwick Pokémon Center | kept | Borderland (Elowen/Isenmar) | 6, 12 |  |
| 572 | The Exchange | The Exchange | kept | Borderland (Elowen/Isenmar) | 6, 12 |  |
| 573 | The Two Hearths | The Two Hearths | kept | Borderland (Elowen/Isenmar) | 6, 12 |  |
| 574 | Rime-silk Loft | Rime-silk Loft | kept | Borderland (Elowen/Isenmar) | 6, 12 |  |
| 575 | Border House | Border House | kept | Borderland (Elowen/Isenmar) | 6, 12 |  |
| 576 | Halvard's Smokehouse | Halvard's Smokehouse | kept | Borderland (Elowen/Isenmar) | 6, 12 |  |
| 577 | - | Frostwick Pass | new | Borderland (Elowen/Isenmar) | 8, 12 | The low pass over the hoar downs into Frostwick. Both kingdoms claim it and neither keeps the toll hut. |
| 578 | - | Rimewood Path | new | Borderland (Elowen/Isenmar) | 6, 11 | The trappers' blazed path into the frozen forest: a red axe-mark every twenty paces, and you do not leave them. |
| 580 | Route 7 | The Reedholms | renamed | Isenmar | 4, 7 | The islets ('holms') of the Ebb delta, joined by boardwalks that are re-laid every spring. |
| 581 | Route 8 - Icefall Locks | The Icefall Locks | renamed | Borderland (Isenmar/Zenith) | 9, 7 | The frozen falls of the escarpment, cut into steps and locks by Zenith's engineers. |
| 582 | Lumen South Gate | Lumen South Gate | kept | Zenith | 10, 6 |  |
| 584 | Voltaic Sluiceworks | Voltaic Sluiceworks | kept | Borderland (Isenmar/Zenith) | 4, 6 |  |
| 585 | Sluiceworks Turbine Hall | Sluiceworks Turbine Hall | kept | Borderland (Isenmar/Zenith) | 4, 6 |  |
| 588 | Ebb Hollow | Ebb Hollow | kept | Isenmar | 4, 8 |  |
| 590 | Brassfall | Brassfall | kept | Borderland (Isenmar/Zenith) | 8, 7 | Where the brass meets the falls: the Icefall Locks' company town. |
| 591 | Brassfall Pokémon Center | Brassfall Pokémon Center | kept | Borderland (Isenmar/Zenith) | 8, 7 |  |
| 592 | - | The Icecutters' Haul | new | Borderland (Isenmar/Zenith) | 6, 7 | The sled road the ice-cutters' union drags its blocks down, from the falls to the Ebbmouth boats. |
| 593 | - | The Arc-Lamp Mile | new | Zenith | 10, 6 | The first road in Velmora lit by electric arc lamps. Zenith counts its age from the night they were switched on. |
| 600 | Route 9 - The Brass Dunes | The Brass Dunes | renamed | Borderland (Zenith/Ossaria) | 15, 5 | Kept name: dunes the colour of the locomotives buried in them. |
| 601 | Route 10 | The Rib Road | renamed | Ossaria | 18, 4 | Waymarked by the ribs of a leviathan, one every hundred paces, set there before the Electors. |
| 604 | Static Tunnels | Static Tunnels | kept | Zenith | 14, 6 |  |
| 605 | Static Tunnels Depths | Static Tunnels Depths | kept | Zenith | 14, 6 |  |
| 608 | The Lowlight (Shattered) | The Lowlight (Shattered) | kept | Zenith | 12, 5 |  |
| 610 | Copperdune | Copperdune | kept | Borderland (Zenith/Ossaria) | 17, 4 | Copper in the dunes: the railway's caravanserai where the line went under the sand. |
| 611 | Copperdune Pokémon Center | Copperdune Pokémon Center | kept | Borderland (Zenith/Ossaria) | 17, 4 |  |
| 612 | - | The Meridian Mainline | new | Zenith | 13, 5 | Zenith's first railway. You walk the service road beside the track. |
| 613 | - | Sunbleach Flats | new | Ossaria | 20, 4 | The flats before Duneholt, where bones and cloth alike go white in a season. |
| 620 | Route 11 | The Marrow Road | renamed | Ossaria | 22, 5 | It runs through the fossil beds where the rock is the colour of marrow. |
| 621 | Route 12 - The Leach Canyons | The Leach Canyons | renamed | Borderland (Ossaria/Nadir) | 20, 8 | Kept name: the canyons the River Leach cut, glowing blue with what Nadir puts in it. |
| 624 | Ossuary of Dunes | Ossuary of Dunes | kept | Ossaria | 23, 6 |  |
| 625 | Ossuary of Dunes - Script Vault | Ossuary of Dunes - Script Vault | kept | Ossaria | 23, 6 |  |
| 628 | Sinkfield | Sinkfield | kept | Ossaria | 21, 5 |  |
| 630 | Charwell | Charwell | kept | Borderland (Ossaria/Nadir) | 19, 8 | Char-well: the well that bone-char keeps clean. |
| 631 | Charwell Pokémon Center | Charwell Pokémon Center | kept | Borderland (Ossaria/Nadir) | 19, 8 |  |
| 632 | - | The Kneeling Stones | new | Ossaria | 21, 6 | Wind-cut pillars that look like bowed pilgrims. The crossroads of Ossaria. |
| 633 | - | The Gutterfall | new | Nadir | 18, 8 | Where the Leach drops off the canyon lip into the marsh. Nadir named it. |
| 640 | Route 13 | Leechman's Walk | renamed | Nadir | 17, 10 | The plank causeway the leech-gatherers keep up. You pay them or you swim. |
| 641 | Route 14 - Sulfur Reach (Lake Sallow) | Lake Sallow | renamed | Borderland (Nadir/Ashkaar) | 19, 10 | Named for its colour. The whole lake is one hot spring. |
| 644 | Miasma Caverns | Miasma Caverns | kept | Nadir | 16, 10 |  |
| 645 | Miasma Caverns B1F | Miasma Caverns B1F | kept | Nadir | 16, 10 |  |
| 648 | The Weeping Fen | The Weeping Fen | kept | Nadir | 15, 9 |  |
| 650 | Scaldwater | Scaldwater | kept | Borderland (Nadir/Ashkaar) | 21, 10 | Scald-water: the hot springs of the Sulfur Reach, and their temper. |
| 651 | Scaldwater Pokémon Center | Scaldwater Pokémon Center | kept | Borderland (Nadir/Ashkaar) | 21, 10 |  |
| 652 | - | The Pyre Road | new | Ashkaar | 22, 10 | Lined with oath-pyres that are never let go out. Every legionary lights one before first posting. |
| 658 | Lantern Isle | Lantern Isle | kept | Borderland (islands) | 20, 9 |  |
| 660 | Route 15 | The Ashmarch | renamed | Ashkaar | 23, 11 | The legions' marching road. Ash falls on it every day and is swept every night. |
| 661 | Route 16 - The Ironway | The Ironway | renamed | Borderland (Ashkaar/Nadir) | 21, 11 | Kept name: the pass the ore came down, on rails laid by Nadir and paid for by Ashkaar. |
| 662 | Route 15b - The Cinderglass Barrens | The Cinderglass Barrens | renamed | Borderland (Ashkaar/Ossaria) | 25, 9 | Kept name: obsidian dunes where sand met fire. |
| 663 | The Petrified Ashwood | The Petrified Ashwood | kept | Borderland (Ashkaar/Ossaria) | 24, 8 |  |
| 664 | Mt. Cinder 1F | The Cinderhorn 1F | renamed | Ashkaar | 25, 11 | The volcano above Cindervault, named for its shape: a horn, still smoking. |
| 665 | Mt. Cinder 2F | The Cinderhorn 2F | renamed | Ashkaar | 25, 11 | As 664. |
| 666 | Mt. Cinder Caldera | The Cinderhorn Caldera | renamed | Ashkaar | 25, 11 | As 664. |
| 668 | Emberfall | Emberfall | kept | Ashkaar | 25, 10 |  |
| 670 | Glasswake | Glasswake | kept | Borderland (Ashkaar/Ossaria) | 25, 7 | The glass-wake: the black glass a lava flow leaves behind it, and the furnace town that sells it. |
| 671 | Glasswake Pokémon Center | Glasswake Pokémon Center | kept | Borderland (Ashkaar/Ossaria) | 25, 7 |  |
| 672 | - | The Long Drop | new | Nadir | 18, 11 | Ironreach's front door: a shaft road that goes down for an hour. Named by people who carried things up it. |
| 673 | - | The Wyrmtongue | new | Ashkaar | 26, 5 | The spit of black lava that runs out to the Cape, forked at the end like a tongue. |
| 680 | Route 17 - The Rootdeep | The Rootdeep | renamed | Borderland (Nadir/Elowen) | 15, 12 | Kept name: where Elowen's roots come through the roof of Nadir's mines. |
| 681 | Route 18 - Prism Falls | Prism Falls | renamed | Elowen | 12, 11 | Kept name: the falls throw a rainbow all day, every day. It is the Imprint. |
| 682 | The Royal Chase | The Royal Chase | kept | Elowen | 8, 11 |  |
| 684 | Grudgestone Quarry | Grudgestone Quarry | kept | Nadir | 16, 13 |  |
| 685 | Grudgestone Quarry B1F | Grudgestone Quarry B1F | kept | Nadir | 16, 13 |  |
| 688 | Echo Coliseum | Echo Coliseum | kept | Nadir | 17, 12 |  |
| 690 | Lanternroot | Lanternroot | kept | Borderland (Nadir/Elowen) | 13, 12 | Lantern-root: the glowing roots the miners read their way by. |
| 691 | Lanternroot Pokémon Center | Lanternroot Pokémon Center | kept | Borderland (Nadir/Elowen) | 13, 12 |  |
| 692 | - | The Tailings | new | Nadir | 16, 12 | The mine-waste hills outside Ironreach. Kids sled down them on shovels. |
| 693 | - | The Briarway | new | Elowen | 10, 11 | The royal road to Verdance, hedged with briar on both sides by the first monarch and clipped ever since. |
| 698 | Hollow Sanctuary | Hollow Sanctuary | kept | Elowen | 10, 13 |  |
| 699 | Meridian Black Site | Meridian Black Site | kept | Nadir | 15, 10 |  |
| 700 | Route 19 | The Hart's Run | renamed | Elowen | 8, 9 | The line the royal hunt rides. No one else may gallop on it, and everyone does. |
| 701 | Route 20 - Northern Rimewood | The Hoarwood | renamed | Borderland (Elowen/Isenmar) | 6, 9 | What Isenmar calls the northern Rimewood: older, deeper, and white all year. |
| 703 | Gossamer Heartwood | Gossamer Heartwood | kept | Elowen | 12, 13 |  |
| 704 | Frostfang Pass | Frostfang Pass | kept | Isenmar | 5, 5 |  |
| 705 | Frostfang Pass 2F | Frostfang Pass 2F | kept | Isenmar | 5, 5 |  |
| 708 | The Bride Grove | The Bride Grove | kept | Elowen | 8, 10 |  |
| 710 | Snowbriar | Snowbriar | kept | Borderland (Elowen/Isenmar) | 5, 8 | Snow-briar: the royal lodge in the frozen bride-briar hedges. |
| 711 | Snowbriar Pokémon Center | Snowbriar Pokémon Center | kept | Borderland (Elowen/Isenmar) | 5, 8 |  |
| 712 | - | The Whalebone Road | new | Isenmar | 4, 4 | Arched with whale ribs from the pass down to Rimeholt's Icewall Gate, one arch per thane. |
| 720 | Route 21 | The Thane's Sled-Road | renamed | Isenmar | 4, 1 | The coast road on the sea ice, kept open by the thane's own teams. |
| 721 | Route 22 - Mast Glacier | The Mast Glacier | renamed | Borderland (Isenmar/Zenith) | 6, 1 | Kept name: airships are ice-anchored along the glacier tongue, and their masts look like a winter forest. |
| 723 | Ebbmouth Sea Grotto | Ebbmouth Sea Grotto | kept | Isenmar | 2, 6 |  |
| 724 | Cloudstair - Lower | Cloudstair - Lower | kept | Zenith | 8, 2 |  |
| 725 | Cloudstair - Inner | Cloudstair - Inner | kept | Zenith | 8, 2 |  |
| 726 | Cloudstair - Summit | Cloudstair - Summit | kept | Zenith | 8, 2 |  |
| 728 | Stillwater | Stillwater | kept | Isenmar | 2, 3 |  |
| 730 | Anchorhold | Anchorhold | kept | Borderland (Isenmar/Zenith) | 7, 2 | Anchor-hold: where the airships are anchored to the glacier. |
| 731 | Anchorhold Pokémon Center | Anchorhold Pokémon Center | kept | Borderland (Isenmar/Zenith) | 7, 2 |  |
| 732 | - | The Tetherline | new | Zenith | 8, 3 | The walkway strung under Skyreach's mooring cables. Zenith calls it safe. |
| 740 | Route 23 | Conductors' Causeway | renamed | Zenith | 10, 4 | The road between the lightning rods ('conductors') that feed the Lattice. It hums. |
| 741 | Route 24 - The Wired Wood | The Wired Wood | renamed | Borderland (Zenith/Elowen) | 10, 7 | Kept name: forest grown up Zenith's pylons, or pylons planted in Elowen's forest, depending who you ask. |
| 742 | Mirror Mere | Mirror Mere | kept | Borderland (Elowen/Antumbra) | 14, 10 |  |
| 743 | Antumbra Threshold | Antumbra Threshold | kept | Antumbra | 25, 16 |  |
| 744 | Stormwatch Spire 1F | Stormwatch Spire 1F | kept | Zenith | 11, 3 |  |
| 745 | Stormwatch Spire 2F | Stormwatch Spire 2F | kept | Zenith | 11, 3 |  |
| 746 | Stormwatch Spire Roof | Stormwatch Spire Roof | kept | Zenith | 11, 3 |  |
| 748 | The Shattered Sky | The Shattered Sky | kept | Zenith | 9, 4 |  |
| 750 | Verdigris | Verdigris | kept | Borderland (Zenith/Elowen) | 11, 9 | Verdigris: the green that copper turns in the rain, and the town that is both. |
| 751 | Verdigris Pokémon Center | Verdigris Pokémon Center | kept | Borderland (Zenith/Elowen) | 11, 9 |  |
| 752 | - | The Looking-Glass Wood | new | Borderland (Elowen/Antumbra) | 12, 9 | Borderland H. The reflections in its pools do not always agree with what is standing over them. |
| 753 | Glassmere | Glassmere | kept | Borderland (Elowen/Antumbra) | 13, 10 | Glass-mere: the lake that shows you the wrong sky. |
| 754 | Glassmere Pokémon Center | Glassmere Pokémon Center | kept | Borderland (Elowen/Antumbra) | 13, 10 |  |
| 755 | - | Widdershins Walk | new | Antumbra | 26, 16 | The first road in Antumbra. It can only be walked against the sun, and here the sun agrees. |
| 760 | Route 25 - The Obsidian Barrows | The Obsidian Barrows | renamed | Borderland (Antumbra/Ossaria) | 22, 8 | Kept name: a necropolis of obsidian tomb-mirrors that became gates. |
| 761 | Route 26 | Spinefall Gorge | renamed | Ossaria | 24, 6 | The river comes down over the backbone of something that was a mile long. |
| 764 | Geode Hollow | Geode Hollow | kept | Ossaria | 25, 5 |  |
| 765 | Geode Hollow B1F | Geode Hollow B1F | kept | Ossaria | 25, 5 |  |
| 768 | The Dreaming Quarter | The Dreaming Quarter | kept | Antumbra | 29, 16 |  |
| 770 | Vigil | Vigil | kept | Borderland (Antumbra/Ossaria) | 23, 7 | The watch kept over the dead, and the town that keeps it. |
| 771 | Vigil Pokémon Center | Vigil Pokémon Center | kept | Borderland (Antumbra/Ossaria) | 23, 7 |  |
| 772 | - | Yesterday's Road | new | Antumbra | 28, 17 | Travellers arrive at the far end before they set out. The Synod taxes both ends. |
| 773 | - | The Vertebrae | new | Ossaria | 24, 4 | A stair of round stone drums up to Cragholm, each one a step and a bone. |
| 780 | Route 27 | The Jawbone Ridge | renamed | Ossaria | 23, 3 | A ridge with a toothed skyline. Cragholm says the teeth were cut; Vigil says they grew. |
| 781 | Route 28 | Hindmoor | renamed | Antumbra | 25, 17 | The moor that is only seen properly over your shoulder. Look straight at it and it is somewhere else. |
| 783 | Duneholt Undersands | Duneholt Undersands | kept | Ossaria | 22, 3 |  |
| 784 | Darkglass Mine | Darkglass Mine | kept | Ossaria | 21, 3 |  |
| 785 | Darkglass Mine B1F | Darkglass Mine B1F | kept | Ossaria | 21, 3 |  |
| 788 | Stonesleep | Stonesleep | kept | Ossaria | 21, 2 |  |
| 790 | - | Downflame Road | new | Antumbra | 26, 18 | Lit by candles whose flames hang below the wick. Gravenmoor makes them. |
| 800 | Route 29 | The Noonless Road | renamed | Antumbra | 28, 18 | Antumbra has no noon. On this road your shadow never shortens. |
| 801 | Route 30 - Slag Mesa | The Slag Mesa | renamed | Borderland (Ossaria/Zenith) | 18, 3 | Kept name: a mesa that is half rock and half what Cogsworth poured on it. |
| 804 | Barrow of the Wardens | Barrow of the Wardens | kept | Antumbra | 29, 17 |  |
| 805 | Barrow Sanctum | Barrow Sanctum | kept | Antumbra | 29, 17 |  |
| 806 | Giratina's Reverse Depths | Giratina's Reverse Depths | kept | Antumbra | 29, 19 |  |
| 808 | The Hush | The Hush | kept | Antumbra | 26, 19 |  |
| 810 | - | The Dry Tide | new | Ossaria | 20, 6 | An old seabed, rippled like a beach the sea left one evening and never came back to. |
| 811 | - | The Smokestack Parade | new | Zenith | 17, 2 | Cogsworth's ceremonial avenue: one chimney per founding patent. |
| 820 | Route 31 - The Hanging Stair | The Hanging Stair | renamed | Borderland (Zenith/Nadir) | 15, 1 | Kept name: scaffolds, cable lifts and outflow falls down the cliff beneath Zenith. |
| 821 | Route 32 | The Drownings | renamed | Borderland (Zenith/Nadir) | 13, 1 | Nadir's name for the coast that went under with Aurelia. |
| 822 | Route 32 Seabed | Under the Drownings | renamed | Borderland (Zenith/Nadir) | 13, 0 | The seabed below the Drownings: streets, with fish in them. |
| 824 | Aurelia - Drowned Spires | Aurelia - Drowned Spires | kept | Nadir | 12, 0 |  |
| 825 | Aurelia - Air Halls | Aurelia - Air Halls | kept | Nadir | 12, 0 |  |
| 826 | Aurelia - Gilded Throne Vault | Aurelia - Gilded Throne Vault | kept | Nadir | 12, 0 |  |
| 828 | Ironbloom | Ironbloom | kept | Zenith | 16, 1 |  |
| 830 | Midstair | Midstair | kept | Borderland (Zenith/Nadir) | 14, 1 | Midway up the Hanging Stair. |
| 831 | Midstair Pokémon Center | Midstair Pokémon Center | kept | Borderland (Zenith/Nadir) | 14, 1 |  |
| 832 | - | The Brink | new | Zenith | 15, 2 | Where Zenith stops. A promenade with a brass rail and a very long view. |
| 838 | Accord Archive | Accord Archive | kept | Crownhaven | 19, 15 |  |
| 840 | Route 33 - Rootdeep River | The Blindwater | renamed | Borderland (Nadir/Elowen) | 14, 13 | The underground river. Nothing in it has eyes, and the boatmen sing so the walls know where they are. |
| 841 | Route 34 - Gloamwood Verge | The Gloamwood Verge | renamed | Elowen | 15, 16 | Kept name: the edge of the twilight wood, where the river comes back into the light. |
| 844 | Lightless Deep | Lightless Deep | kept | Nadir | 13, 14 |  |
| 845 | Lightless Deep B1F | Lightless Deep B1F | kept | Nadir | 13, 14 |  |
| 848 | The Inverted Ward | The Inverted Ward | kept | Nadir | 13, 13 |  |
| 850 | Mothwell | Mothwell | kept | Borderland (Nadir/Elowen) | 15, 15 | The moths that come to the lamps of the underground river. |
| 851 | Mothwell Pokémon Center | Mothwell Pokémon Center | kept | Borderland (Nadir/Elowen) | 15, 15 |  |
| 852 | - | The Throat | new | Nadir | 11, 1 | The tunnel that swallows the river at Underveil. Boats go in. |
| 860 | Route 35 - Gloamwood | The Gloamwood | renamed | Elowen | 17, 17 | Kept name: Elowen's heart, where it has been dusk for three hundred years. |
| 861 | Route 36 - Thornwar Marches | The Thornwar Marches | renamed | Borderland (Elowen/Ashkaar) | 19, 17 | Kept name: where Elowen and Ashkaar fought the Thornwar. The trees still burn without dying. |
| 864 | Wyrmscar Rift | Wyrmscar Rift | kept | Ashkaar | 24, 16 |  |
| 865 | Wyrmscar Depths | Wyrmscar Depths | kept | Ashkaar | 24, 16 |  |
| 868 | The Rainbow Scar | The Rainbow Scar | kept | Elowen | 16, 18 |  |
| 870 | Thornwatch | Thornwatch | kept | Borderland (Elowen/Ashkaar) | 21, 17 | Thorn-watch: the watchtower of the Thornwar, still manned. |
| 871 | Thornwatch Pokémon Center | Thornwatch Pokémon Center | kept | Borderland (Elowen/Ashkaar) | 21, 17 |  |
| 872 | - | The Wyrmspine | new | Ashkaar | 22, 16 | The ridge road to Wyrmrest, along a spine of rock that Ashkaar says is exactly that. |
| 880 | Route 37 - Pilgrim Pass | The Pilgrim Pass | renamed | Borderland (Ashkaar/Crownhaven) | 22, 14 | Kept name: eighteen shrines, one per Plate, up the Crownwall. |
| 884 | Sovereign's Ascent 1F | Sovereign's Ascent 1F | kept | Crownhaven | 21, 13 |  |
| 885 | Sovereign's Ascent 2F | Sovereign's Ascent 2F | kept | Crownhaven | 21, 13 |  |
| 886 | Sovereign's Ascent Summit | Sovereign's Ascent Summit | kept | Crownhaven | 21, 13 |  |
| 888 | The Glassfall Scar | The Glassfall Scar | kept | Crownhaven | 18, 13 |  |
| 890 | Pilgrim's Rest | Pilgrim's Rest | kept | Borderland (Ashkaar/Crownhaven) | 22, 13 | The last rest before the Crownwall, where every kingdom's pilgrims sleep in the same hall. |
| 891 | Pilgrim's Rest Pokémon Center | Pilgrim's Rest Pokémon Center | kept | Borderland (Ashkaar/Crownhaven) | 22, 13 |  |
| 892 | - | Dominar's Toll | new | Ashkaar | 23, 15 | The Dominion taxes a holy road here, and has for three hundred years. |
| 893 | - | The Coronation Road | new | Crownhaven | 20, 13 | Walked once by each Sovereign, on foot, from the Ascent to the Eighteen Gates. |
| 900 | Hallow Strait | Hallow Strait | kept | Borderland (sea) | 13, 19 |  |
| 901 | Hallow Strait Seabed | Hallow Strait Seabed | kept | Borderland (sea) | 13, 19 |  |
| 905 | Shardfall Isles | Shardfall Isles | kept | Borderland (islands) | 19, 19 |  |
| 910 | Antumbra - Distortion Core | Antumbra - Distortion Core | kept | Antumbra | 28, 19 |  |
| 920 | The Rime Narrows | The Rime Narrows | kept | Isenmar | 28, 1 |  |
| 921 | Skaldfast - Outer Walls | Skaldfast - Outer Walls | kept | Isenmar | 28, 0 | Skald-fast: the skalds' fastness, the oldest fort on the Rime Isles. |
| 922 | Skaldfast - Harbour Keep | Skaldfast - Harbour Keep | kept | Isenmar | 28, 0 |  |
| 923 | Skaldfast - Great Hall | Skaldfast - Great Hall | kept | Isenmar | 28, 0 |  |
| 924 | Ashkaar Siege Camp | Ashkaar Siege Camp | kept | Ashkaar | 28, 2 |  |
| 925 | The Steamline | The Steamline | kept | Sea - the Shattered Ice strait (contested) | 27, 3 |  |
| 926 | The Shattered Ice | The Shattered Ice | kept | Sea - the Shattered Ice strait (contested) | 27, 2 |  |
| 927 | Cinder Cape Warfort | Cinder Cape Warfort | kept | Ashkaar | 26, 3 | The Dominion's warfort on the Cape of Cinders, facing the Rime Isles across the Shattered Ice. |
| 959 | Skyport Customs | Skyport Customs | kept | Zenith | 10, 3 |  |
| 960 | The Ledger Hall | The Ledger Hall | kept | Ruin Route | 19, 15 |  |
| 961 | Glassed Orchard - Ruin | Glassed Orchard - Ruin | kept | Ruin Route | 14, 16 |  |
| 962 | Aurelia - Gilded Chain Foundry | Aurelia - Gilded Chain Foundry | kept | Ruin Route | 12, 0 |  |
| 963 | Crownhaven - Ruined Crown | Crownhaven - Ruined Crown | kept | Ruin Route | 19, 14 |  |

## Prose forms

Besides the map names above, the rename script also rewrites these phrases:

| Old | New |
|---|---|
| Mt. Cinder | the Cinderhorn |
