# WORLD — Velmora region & level design (World lead)

Binding: `SPINE.md` (incl. **REVISION 2**). Machine-readable map list: **`design/maps.json`** (the Map Builder works from it).
Gym puzzles: `GYM_PUZZLES.md`. Species: `POKEMON_AVAILABILITY.md`. Wild data: `pbs/encounters.txt` (validated by `tools/validate_encounters.py`).
Names that the story team hasn't fixed yet are marked *(prov.)*.

---
## 1. Region layout: seven kingdoms around Crownhaven

**The region map is `art/previews/world_map.png`** (painted) and the in-game Town Map is
`graphics/UI/Town Map/prismfall_velmora.png`; the geography in words is **`design/WORLD_MAP.md`**. Both images and the
town-map squares come from `tools/worldmap/` (Revision 13). Gym numbers below follow Revision 14 (Saltmere 1, Briarwick 2).
```
 Schematic, not to scale (N up). Kingdoms touch ONLY through the borderlands in [brackets]; adjacency is authoritative in §10.
 ~~~~~~~~~~~~ THE FROZEN NORTH SEA (Isenmar's sea-ice; the Thane's sled-road runs on it) ~~~~~~~~~~~  Rime Isles: Skaldfast
 (10)Rimeholt  [B2 Anchorhold]  (11)Skyreach  (16)Underveil, Midstair[L]  (15)Cogsworth   (13)Cragholm  ~Shattered Ice~
   ISENMAR      Frostfang Mts     ZENITH PLATEAU (the City Above)             OSSARIA (the Bone Sands)    Cinder Cape
 (3)Ebbmouth --[B Brassfall]-- (4)LUMEN CITY --[C Copperdune]-- (5)Duneholt   [I Vigil]  [M Glasswake]   (Ashkaar)
   [A2 Snowbriar]   [G Verdigris]    NADIR lowlands: (6)Mirefen  [D Charwell]  [E Scaldwater] -- (7)Cindervault
 [A Rimewood]   (9)Verdance  [H Glassmere] Mirror Mere   (8)Ironreach           ASHKAAR (the Dragonfire Dominion)
   Frostwick       [F Lanternroot]           ( CROWNHAVEN inside the Crownwall )  [K Pilgrim's Rest]
 (2)Briarwick (in the Gossamer Wood)  [F Mothwell]                                   (18)Wyrmrest
 (1)Saltmere ------- (0)Ferrow's Landing      (17)Gloaming --[J Thornwatch]--      [ANTUMBRA, behind the glass:
 ~~~~~~~~~~~~~~~~~~~~ THE HALLOW STRAIT ~~~~~~~~~~~~~ Shardfall Isles ~~~~~~~~~~~~    (12)Lucent, (14)Gravenmoor]
 ANTUMBRA (mirror realm) has three stable gates: A Mirror Mere (Elowen, border H), B the Grave Glass at Vigil and
 C the Obsidian Barrows' east gate (both Ossaria, border I). The map draws it as an inset in the south-east sea.
```

| Kingdom | Where | Wild types (~70%) | Visits (gym #) | What changes on return |
|---|---|---|---|---|
| Elowen | south & south-west forest | Fairy, Grass, Bug, Normal | 1,2 → 9 → 17 | Act III: Verdance's runaway bloom opens Gossamer Heartwood; Act V: forest heart (Gloamwood) at twilight, Bleed visibly spreading from Briarwick |
| Isenmar | west & north coast | Water, Ice | 3 → 10 | Act III: Rimeholt's lake thawing under a Meridian Lattice; Ebbmouth Sea Grotto opens (Surf) |
| Zenith | north-central plateau | Electric, Steel, Flying | 4 → 11 → 15 | Act II: Lowlight Shattered (Bleed); Act III: Mandate checkpoints; Act IV: foundry district under martial law |
| Nadir | beneath Lumen + its runoff marsh | Poison, Dark, Fighting | 6, 8 → 16 | Act IV: the Fault drains the north coast, Underveil opens onto drowned Aurelia |
| Ashkaar | east / south-east volcanic | Fire, Dragon | 7 → 18 | Act V: caldera tap damage, dragon-lords mobilised |
| Ossaria | north-east desert & canyons | Ground, Rock | 5 → 13 | Act IV: Duneholt Undersands (deeper ruins) open |
| Antumbra | mirror realm behind Elowen | Ghost, Psychic, Dark | 12 → 14 | postgame: Distortion Core (Giratina) |
| Crownhaven | centre, on the Crown ring | — | Act V | Festival |

Borderland routes (marked `Borderland (A/B)` in maps.json) mix both kingdoms' types ~50/50.
**Story note:** Aurelia (the drowned capital) sits under Underveil on the **north** coast below Lumen's cliffs. 00_OVERVIEW says "south coast"; story team please reconcile (Revision 2 put the Nadir beneath Lumen).
**Town map:** Velmora must be **region 0** in `town_map.txt`. Essentials' form handlers turn Pikachu/Exeggcute/Cubone Alolan in region 1 and Koffing/Mime Jr. Galarian in region 2.

---
## 2. Map ID scheme (RPG Maker XP, sample maps end at 075)

| IDs | Use |
|---|---|
| **100 + 20·c** (c = 0 Ferrow's Landing, 1 Briarwick, 2 Saltmere, 3 Ebbmouth … 18 Wyrmrest; see the Revision 14 note below) | city block: +0 exterior, +1 Pokémon Center, +2 Mart, +3..+9 houses/landmarks, **+10..+19 gym rooms** (+10 entrance … last = Warden arena) |
| 480–519 | Crownhaven (+10..+19 Festival Arena, Battle Tower) |
| **520 + 20·s** (s = badges held, 0–18) | overworld segment s, the land between gym s and gym s+1: +0..+3 routes, +4..+7 dungeons, **+8..+9 Bleed zone**, +10..+17 rest houses/gates, +18..+19 optional |
| 900–919, 940–949 | postgame (Hallow Strait, Shardfall Isles, Antumbra Distortion Core) |
| 920–939 | Ashkaar–Isenmar war theatre (§9) |
| 950–959 | overflow for big-city districts |
| 960–979 | **Ruin Route only** maps |
| 980–989 | interludes (playable as other characters) · 990–999 dev/test |
| segment +18/+19 | also used for **branch-only** maps (e.g. 698 Hollow Sanctuary, 699 Meridian Black Site, 838 Accord Archive) |

So the map ID tells you the badge count (and therefore the level cap): the validator relies on this.
**Revision 14 exception.** Saltmere (Gym 1) keeps block **140–159** and Briarwick (Gym 2) keeps block **120–139**: built maps are never renumbered. For these two blocks, and for the Act I legs that changed stretch (541–548 are now on the Gym 2 stretch, 520–528 except 524–526 on the Gym 1 stretch), the ID no longer tells the badge count. **`segment` in maps.json is authoritative**, and `validate_encounters.py` reads it before the ID scheme. Gym 1's rooms are 150 (lobby) and 154 (auditorium); Gym 2's are 130 (foyer) and 131 (Weaving Hall). Puzzle switch blocks follow the building, not the number: 305–309 the Loomhouse, 310–314 the Pell Playhouse. Revisit areas that open later (e.g. Gossamer Heartwood, Ebbmouth Sea Grotto) take IDs in the segment where they open, not in their kingdom's first block.

---
## 3. Progression (segment table)

Wild level band ≈ previous cap −3 … next cap −2. Field = default battle field (`FieldEffects::MAP_FIELDS`). `—` = :NONE.

| s | Act | From → to | Maps (ID) and field | Wild Lv |
|---|---|---|---|---|
| 0 | I | Ferrow's → Saltmere (G1 cap 15) — the Strand Road, Ch1–2 | The Ferrymen's Mile 520, Windfall Row 521 (branch) + Hale Farmhouse 523, **Glassed Orchard 522** BLEED (story), Lacecliff Walk 527 BEACH, Marram Down 528 BEACH; Saltmere 140–147 and the Pell Playhouse 150/154 | 3–12 |
| 1 | I | Saltmere → Briarwick (G2 19) — the Weavers' Road, Ch3 | The Grey Saltings 541 BEACH, Brinecut Mine 544/545 CAVE, The Dyers' Ford 552, Thistledown Lea 540, Thistledown Manor 546/547 (haunted house), Gossamer Wood 524 SILKWOOD, Woodward's Hut 526; Briarwick 120–125 and the Loomhouse 130/131 | 12–17 |
| 2 | I | Briarwick → Ebbmouth (G3 23) — the Hoar Road, Ch4 | After Tamsin's badge: Gossamer Deepwood 525 SILKWOOD (Cut), **Cocoonfall Hollow 548** BLEED, the Loomhouse Upper Lofts 132/134 and the Playhouse Backstage 151–153 (optional). **Borderland A (the Rimewood):** Spinners' Rise 566, Frostwick Pass 577, **Frostwick 570** (+571–576), Rimewood Path 578, The Rimewood 562, Rimewood Glade 563 (Cut). Then Isenmar: Gullcry Cliffs 561, Gullcry Caves 564/565 CAVE; K2 on 561. Side road: Frostflat Causeway 560 (Frostwick ↔ Saltmere) with **The Rehearsal 568** BLEED | 16–21 |
| 3 | I | Ebbmouth → Lumen City (G4 27) | The Reedholms 580, the Icefall Locks 581, Voltaic Sluiceworks 584/585 SCRAPYARD (Rotom), **Ebb Hollow 588** BLEED | 18–25 |
| 4 | II | Lumen → Duneholt (G5 31) | The Brass Dunes 600, the Rib Road 601 DESERT, Static Tunnels 604/605 CAVE (Flash), **The Lowlight (Shattered) 608** BLEED (story) | 22–29 |
| 5 | II | Duneholt → Mirefen (G6 35) | R11 620 DESERT, R12 621, Ossuary of Dunes 624/625 CAVE (Strength, Unown ruins), **Sinkfield 628** | 26–33 |
| 6 | II | Mirefen → Cindervault (G7 39) | Leechman's Walk 640, Lake Sallow 641 (Surf), Miasma Caverns 644/645 CORROSIVE_MIRE, **Weeping Fen 648**, Lantern Isle 658 BEACH (opt.) | 30–37 |
| 7 | II | Cindervault → Ironreach (G8 43) | The Ashmarch 660 ASHEN_WASTE, the Ironway 661 MOUNTAIN, the Cinderhorn 664–666 VOLCANIC, **Emberfall 668**; optional/war road: **Cinderglass Barrens 662**, Petrified Ashwood 663, **Glasswake 670** (border M) | 34–41 |
| 8 | III | Ironreach → Verdance (G9 47) | The Rootdeep 680 CAVE + **Lanternroot 690** (border F), Prism Falls 681 RAINBOW, **Royal Chase 682** (Safari-style reserve), Grudgestone Quarry 684/685 CAVE, **Echo Coliseum 688** | 38–45 |
| 9 | III | Verdance → Rimeholt (G10 51) | The Hart's Run 700, the Hoarwood 701 SNOWY_MOUNTAIN, Gossamer Heartwood 703 SILKWOOD (revisit), Frostfang Pass 704/705 SNOWY_MOUNTAIN, **Bride Grove 708** (story) | 42–49 |
| 10 | III | Rimeholt → Skyreach (G11 55) | The Thane's Sled-Road 720, the Mast Glacier 721 SNOWY_MOUNTAIN, Ebbmouth Sea Grotto 723 (revisit), Cloudstair 724–726 MOUNTAIN (Rock Climb), **Stillwater 728** | 46–53 |
| 11 | III | Skyreach → Lucent (G12 59) | Conductors' Causeway 740 STORMFRONT, the Wired Wood 741, Mirror Mere 742, **Antumbra Threshold 743 INVERSE**, Stormwatch Spire 744–746 STORMFRONT, **Shattered Sky 748** | 50–57 |
| 12 | IV | Lucent → Cragholm (G13 63) | The Obsidian Barrows 760 INVERSE (Antumbra), Spinefall Gorge 761 (Waterfall), Geode Hollow 764/765 CRYSTAL_CAVERN, **Dreaming Quarter 768** | 54–61 |
| 13 | IV | Cragholm → Gravenmoor (G14 67) | The Jawbone Ridge 780 MOUNTAIN, Hindmoor 781 (Antumbra moors), Duneholt Undersands 783 DESERT (revisit, Groudon arc), Darkglass Mine 784/785 DARK_CRYSTAL, **Stonesleep 788** (fossils) | 58–65 |
| 14 | IV | Gravenmoor → Cogsworth (G15 71) | The Noonless Road 800, the Slag Mesa 801 WASTELAND, Barrow of the Wardens 804/805 (CAVE/HOLLOW_CATHEDRAL), Giratina's Reverse Depths 806 INVERSE, **The Hush 808** | 62–69 |
| 15 | IV | Cogsworth → Underveil (G16 75) | The Hanging Stair 820 SCRAPYARD, the Drownings 821 WATER_SURFACE, Under the Drownings 822 UNDERWATER (Dive), **Aurelia** 824 UNDERWATER / 825–826 CAVE, **Ironbloom 828** | 66–73 |
| 16 | V | Underveil → Gloaming (G17 80) | The Blindwater 840 CAVE, the Gloamwood Verge 841, Lightless Deep 844 DARK_CRYSTAL / 845 NEW_MOON (Pecharunt arc), **Inverted Ward 848 INVERSE** | 70–78 |
| 17 | V | Gloaming → Wyrmrest (G18 85) | The Gloamwood 860 FAIRY_TALE, the Thornwar Marches 861 MOUNTAIN, Wyrmscar Rift 864 CAVE / 865 DRAGONS_DEN (Reshiram arc), **Rainbow Scar 868 RAINBOW** | 75–83 |
| 18 | V | Wyrmrest → Crownhaven (Festival 90) | R37 880 MOUNTAIN, Sovereign's Ascent 884–886, **Glassfall Scar 888** | 80–88 |
| PG | — | postgame | Hallow Strait 900, Seabed 901, Shardfall Isles 905, Antumbra Distortion Core 910 | 80–95 |

Each kingdom has one legendary arc with a boss battle (see POKEMON_AVAILABILITY §4): Elowen = Ogerpon + Loyal Three, Isenmar = Kyogre, Zenith = Zekrom, Nadir = Pecharunt, Ashkaar = Reshiram, Ossaria = Groudon, Antumbra = Giratina.

---
## 3b. Map states, branches, Ruin Route
- **States** (maps.json `states`): one map, several looks, keyed by Core story state (act, choice keys from `story/10_CHOICES_ENDINGS.md` once it exists, `ruin_route`). Build them as event pages or overlay events on the **same** map. Use a separate map only when `replaced_by` is set (e.g. 181 Lowlight → 608 after the Shatter). Current list: Briarwick 120 (Bleed spread Act III, "heartfall" Act V), Saltmere 140 (Mandate / Hollow-riot branch), Ebbmouth 160 (Imprint failing Act III), Lumen 180 (Mandate → martial law), Lowlight 181, R2 521 and Gossamer Wood 524 (Bleed spread), Glassed Orchard 522 (Ruin Route opening).
- **Encounter versions** (`$PokemonGlobal.encounter_version`, global, falls back to version 0 per map): **0** default · **1** Bleed-spread (set at the start of Act IV; revisited early maps get higher-level, Bleed-touched tables) · **2** Ruin Route · **3** postgame.
- **Branch-only maps** come from faction Standing in Act III/IV: 698 Hollow Sanctuary, 699 Meridian Black Site (Type: Null line), 838 Accord Archive. Each is optional, and the matching branch shows its entrance.
- **Ruin Route** (secret; unlocked by the Ledger): hub 960 The Ledger Hall, reachable from any Bleed Veil, plus 961–963. More are added as the Narrative Systems spec lands.
- **Game-over hooks:** every Bleed zone, Aurelia and the Glassfall Scar has a marked "point of no return" tile (`feat game_over_hook` to be added per spec) so story game overs can fire on-map.

## 4. Field moves across 18 badges

`Settings::FIELD_MOVES_COUNT_BADGES = true` (the badge **count** gates each move). Set these in `001_Settings.rb` (or have Prismfall Core redefine them):

| Move | Item | Got where (after badge) | Constant = value | First required at |
|---|---|---|---|---|
| Headbutt | tutor (Windfall Row farmhouse) | Act I start | none (no gate in v21) | optional trees |
| Cut | HM01 | Briarwick Cutter's House (after **Tamsin's** badge, B2) | `BADGE_FOR_CUT = 2` (Rev 14; was 1) | Gossamer Deepwood (to Cocoonfall Hollow) |
| Rock Smash | TM98 | Brinecut miner, handed over on the Weavers' Road (B1) | `BADGE_FOR_ROCKSMASH = 2` (unchanged: usable from Tamsin's badge) | optional rocks on the Grey Saltings / Brinecut, Lacecliff Walk's third arch, Rimewood Path's frozen silk |
| Flash | TM70 | Rook Calder (B4) | `BADGE_FOR_FLASH = 4` | Static Tunnels (dark) |
| Strength | HM04 | Duneholt excavators (B5) | `BADGE_FOR_STRENGTH = 5` | Ossuary of Dunes |
| Surf | HM03 | Mirefen ferrymen (B6) | `BADGE_FOR_SURF = 6` | Lake Sallow |
| Fly | HM02 | Skyreach courier at the Ironreach Conclave (B8) | `BADGE_FOR_FLY = 8` | Act III criss-crossing |
| Rock Climb | TM100 | Rimeholt ice-climbers (B10) | **no v21 constant/handler**: Core must add `Prismfall::BADGE_FOR_ROCKCLIMB = 10` + a cliff-event helper | Cloudstair |
| Waterfall | HM05 | Skyreach sky-river guides (B11) | `BADGE_FOR_WATERFALL = 11` | Spinefall Gorge |
| Dive | HM06 | Cogsworth bathysphere works (B15) | `BADGE_FOR_DIVE = 15` | Under the Drownings / Aurelia |

Rods: Old Rod at Ferrow's Landing (start), Good Rod at Ebbmouth Anglers' Guild (B3), Super Rod from the Rimeholt ice-fisher (B10). The validator enforces these unlocks: a Water table on an early map is capped at the Surf-era cap, and so on.

## 5. Bleed zones and the Unimprinted protagonist
- Every Bleed zone sits behind a **Bleed Veil**, a shimmer-tile event at its entrance. NPCs and partners stop at it ("my skin's burning, I can't"). The PC walks through alone. This is the gameplay proof of being Unimprinted, taught in the Glassed Orchard (s0, mandatory).
- Inside: field `:BLEED` (except Inverted Ward = `:INVERSE`, Rainbow Scar = `:RAINBOW`), Land encounter rate 25, **Imprinted variants** (regional forms) appear only here and near their Imprint, no Fly out (Escape Rope works), screen tint + Lullaby BGM.
- Each zone holds one **Bleed Shard** (*prov.* key item `BLEEDSHARD`, 19 total). Larch trades rewards for them (Ability Capsule, Bottle-Cap-style IV items, the Legend-Plate lore).
- Mandatory zones: Glassed Orchard (s0), The Lowlight (s4), Bride Grove (s9), Glassfall Scar (s18). The rest are optional, but they hold the best items and TMs.

## 6. Key items / TM highlights
Gym TMs: 1 Facade TM42 (Dorian) · 2 U-turn TM89 (Tamsin) · 3 Water Pulse TM03 · 4 Volt Switch TM43 · 5 Bulldoze TM83 · 6 Poison Jab TM84 · 7 Flamethrower TM35 · 8 Brick Break TM31 · 9 Energy Ball TM53 · 10 Ice Beam TM13 · 11 Roost TM51 · 12 Psychic TM29 · 13 Stealth Rock TM76 · 14 Shadow Ball TM30 · 15 Flash Cannon TM91 · 16 Dark Pulse TM79 · 17 Dazzling Gleam TM21 · 18 Dragon Pulse TM59.
Field TMs: Giga Drain TM19 (Gossamer Wood), X-Scissor TM81 (Cocoonfall), Work Up TM10 (Rehearsal), Brine TM55 (Gullcry B1F), Scald TM49 (Ebb Hollow), Thunderbolt TM24 (Lowlight), Earthquake TM26 (The Cinderhorn Caldera), Drain Punch TM60 (Grudgestone), Calm Mind TM04 (Dreaming Quarter), Will-O-Wisp TM61 (The Hush), Trick Room TM92 (Inverted Ward), Dragon Claw TM02 (Wyrmscar Rift), Hyper Beam TM15 (Crownhaven).
Key items: Badge case (Voss, prologue; records the shard, story), Bicycle (Lumen Glide shop, s3), Linking Cord (sold in the Lumen Dept. Store 2F; trade evolutions), Dowsing Machine (Duneholt, s5), Odd Keystone (Ossuary, s5), Fossil revival at Lumen Fossil Lab (Act II) and Cragholm (Act IV), Imprint Lens (*prov.*, Larch, Act II: shows hidden Bleed paths).

---
## 8. Scale, seats, borders and look (Revisions 5–6)
**Look:** the target is Pokémon Rejuvenation's overworld (tall timber buildings, layered foliage, textured paths, weather and lighting overlays). No Gen 3 look. In maps.json, `tileset` is only the stock placeholder used for prototypes. `tileset_kit` names a **role** (e.g. `G45_CASTLE_CITY`, `G4_SNOW_FORTRESS`, `G5_METROPOLIS`, `G4_DISTORTION`) that the Map Builder maps onto Rejuvenation/Reborn/Desolation tilesets (credit the artists in CREDITS.md).
**Borders:** every map has a `border` field saying what forms its edge (sea, cliffs, curtain walls, facades, canyon walls, frozen sea, oldwood canopy with giant trunks). Generic tree-row walls are banned.
**Visual briefs:** 20 major places carry `visual_brief` (landmarks, silhouette, materials, palette, 3 set pieces).

**Kingdom seats** are castle cities built from several linked district maps (`districts` on the main map), with walls and a gatehouse, a keep or palace on high ground, slums, and grand interiors. Each has a **royal court** map (`royal_court`) where the kingdom names its Festival delegation.
| Kingdom | Seat (main ID) | Districts / interiors | Court |
|---|---|---|---|
| Elowen | **Verdance** 280 | Glasshouse Ward 283, Kingsgate Barbican 284, Briar Hall Upper Court 285, Great Hall 286, Royal Gallery 288, Thorn Crypts 289, Heartgarden 294 (Gym 9), Cathedral of the Evergreen 295, Rootward slums 296 | Thorn Throne 287 |
| Isenmar | **Rimeholt** 300 (fortress-port on the frozen sea) | Icewall Gate 303, Sled Market 304, Whalebone Keep Bailey 305, Mead Hall 306, Ice Vault 308 (Kyogre sleeps below), Sinking Quarter 309, Net Row 314 | Thane's Seat 307 |
| Ashkaar | **Cindervault** 240 (*prov.* seat: Pyre Keep on the caldera rim) | Caldera Gate 243, Hearthguild Hall 244, Pyre Keep Rampart 245, Hall of Oaths 247, Dragon Roosts 248, Slag Ward 249, Ancestor Crypts 254 | Ember Throne 246 |
| Ossaria | **Duneholt** 200 (canyon city) | Sandgate 203, Aquifer Quarter 204, Elector's Palace Courtyard 205, Mural Gallery 207, Necropolis of the Electors 208, Dig Lab 209, Sinkwells 214 | Hall of Audience 206 |
| Zenith | **Lumen City** 180 (metropolis, 5 districts) | Lowlight 181, Council Ward 194, Spire District 195 (Meridian Spire 185/186/198/199), Skyport Terrace 196 | Council Chamber 197 |
| Nadir | **Underveil** 420 (vertical undercity in drowned Aurelia's towers) | Moon Market 423, Sump Docks 424, Barons' Stair 425, Bell Tower 426, Drowned Cathedral 429; Sun Court = 826 | Nyx's Hall of Whispers 427 |
| Antumbra | **Lucent** 340 + its inverted reflection | Tribunal Ward 343, Athenaeum 344/345, The Speculum 346, Palace of Glass 347/348/355 (*prov.* names) | Veiled Throne 349 |
| Crownhaven | Lower Crownhaven 480 | Eighteen Gates 482, Basilica Close 483, Basilica 484/485, Accord Palace 486/488/492, Memorial Garden 489, Market Ring 496, Pilgrims' Quarter 497, Concordance Spire 493/494/498 | Sovereign's Throne Room 487 |

**Festival grounds:** the **Temple-Arena of the Blessing** (the rebuilt Meridian Prism Arena) is a colosseum fused with a cathedral: Processional Plaza 495, Hall of Eighteen Doors 490, Altar Stage 491 (`:PRISM_ARENA`). Next to it is the Court of Eight Pavilions 499, one pavilion per delegation.
**Other cities at their own scale:** Saltmere gains Harbour & Breakwater 146 and Old Town 147. Ebbmouth gains Mill Quay 167. Skyreach is vertical (323–326). Ferrow's Landing and Briarwick stay villages. Story landmarks added: Corvin's Infirmary 223, the Iron Pit 263, Vane Hall 383, Lantern Hospice 384, Strade Works 403, Cragholm Lift Galleries 363, Great Tree Roots 443.

## 9. The Ashkaar–Isenmar war (Revision 6)
Ashkaar and Isenmar share **no land border** (Revision 9). The war is fought across the **Shattered Ice strait** in the north-east sea. On one side are Isenmar's **Rime Isles** (Skaldfast), at the far end of its frozen north sea. On the other is Ashkaar's **Cinder Cape**, the north-eastern tip of the Dominion, reached overland through the Cinderglass Barrens (border M). War-theatre maps are **920–939** (all *prov.* names; the story team sets the act):
| ID | Map | Role |
|---|---|---|
| 920 | The Rime Narrows | front line on the ice: trenches, burnt sled-forts |
| 921–923 | **Skaldfast**: Outer Walls, Harbour Keep, Great Hall | the besieged Isenmar fortress-port |
| 924 | Ashkaar Siege Camp | legion tents, dragon pickets, the Dominar's war-tent |
| 925 | The Steamline | no-man's-land where lava meets sea ice |
| 926 | **The Shattered Ice** | frozen-sea battlefield for the climax cutscene (beam clash; FROZEN_LAKE → WATER_SURFACE) |
| 927 | Cinder Cape Warfort | Ashkaar's staging fortress |
Access: the Isenmar side is the sled-road from Rimeholt across the frozen north sea. The Ashkaar side is the north road Cindervault → Cinderglass Barrens 662 → Glasswake 670 → Cinder Cape 927. 925/926 are sea, not borderland. A `war` state is defined on Rimeholt 300/304, Cindervault 240, Ebbmouth 160, Routes 21/22/15/16 and Wyrmrest 460.

---
## 10. Borderlands (Revision 9)
Kingdoms touch **only** through borderlands. Each borderland blends both biomes, cultures and wild types (≈50/50; the validator skips the kingdom-share check on `Borderland (A/B)` maps) and has at least one intermediate town. maps.json carries the full records under the top-level `borderlands` key; every member map has `borderland`.

**Adjacency graph** (13 edges): Elowen–Isenmar (A) · Isenmar–Zenith (B) · Zenith–Ossaria (C) · Ossaria–Nadir (D) · Nadir–Ashkaar (E) · Nadir–Elowen (F) · Zenith–Elowen (G) · Elowen–Antumbra (H, Mirror Mere) · Antumbra–Ossaria (I, Grave Glass) · Elowen–Ashkaar (J) · Ashkaar–Crownhaven (K, the only overland way into the Crown) · Zenith–Nadir (L, vertical) · Ashkaar–Ossaria (M).
**Not adjacent:** Isenmar–Ashkaar (sea war only), Isenmar–Ossaria, Isenmar–Nadir, Elowen–Ossaria, Antumbra–anything but Elowen/Ossaria, Crownhaven–anything but Ashkaar. Long jumps are optional only: Skyreach airships (Act III+), Fly (B8).

**Walking the gym order** (crossings in order):
| Leg | From → to | Crossing(s) |
|---|---|---|
| 0→1→2 | Ferrow's → Saltmere → Briarwick | inside Elowen: the Strand Road along the coast, then the Weavers' Road inland (the direct forest road is corded off until the Glass Matriarch falls) |
| 2→3 | Briarwick → Ebbmouth | **A** Rimewood (south): Spinners' Rise, Frostwick Pass, Frostwick, Rimewood Path, the Rimewood; side road Frostflat Causeway back to Saltmere |
| 3→4 | Ebbmouth → Lumen | **B** Icefall Locks: The Icefall Locks, Brassfall, Sluiceworks |
| 4→5 | Lumen → Duneholt | **C** Brass Dunes: The Brass Dunes, Copperdune |
| 5→6 | Duneholt → Mirefen | **D** Leach Canyons: The Leach Canyons, Charwell |
| 6→7 | Mirefen → Cindervault | **E** Sulfur Reach: Lake Sallow, Scaldwater |
| 7→8 | Cindervault → Ironreach | **E** again via the Ironway |
| 8→9 | Ironreach → Verdance | **F** Rootdeep: The Rootdeep, Lanternroot |
| 9→10 | Verdance → Rimeholt | **A2** northern Rimewood: The Hoarwood, Snowbriar |
| 10→11 | Rimeholt → Skyreach | **B2** Mast Glacier: The Mast Glacier, Anchorhold, Cloudstair |
| 11→12 | Skyreach → Lucent | **G** Wired Wood (Verdigris), then **H** Mirror Mere (Glassmere) → Antumbra Threshold |
| 12→13 | Lucent → Cragholm | **I** Obsidian Barrows: The Obsidian Barrows, Vigil |
| 13→14 | Cragholm → Gravenmoor | **I** again: Vigil's Grave Glass → Hindmoor |
| 14→15 | Gravenmoor → Cogsworth | **I** (The Noonless Road's east gate) then **C'** Slag Mesa |
| 15→16 | Cogsworth → Underveil | **L** Hanging Stair: The Hanging Stair, Midstair, the Drownings |
| 16→17 | Underveil → Gloaming | **F** again (south): The Blindwater, Mothwell |
| 17→18 | Gloaming → Wyrmrest | **J** Thornwar Marches: The Thornwar Marches, Thornwatch |
| 18→Festival | Wyrmrest → Crownhaven | **K** Pilgrim Pass: R37, Pilgrim's Rest |
| war arc | Cindervault → Cinder Cape | **M** Cinderglass Barrens 662/663, Glasswake (the war itself is across the sea) |

| Code | Borderland | Biome blend and signature landmarks | Wild mix | Town (ID): trade · culture mix · tension · sidequest |
|---|---|---|---|---|
| A | **The Rimewood** (Elowen/Isenmar) | The Gossamer's oldwood frozen in hoar: ice-glazed giant trees, frozen silk curtains, fells turning to frost north of Briarwick, and salt flats turning to frost-flats along the coast road to Saltmere. Handfast Arch, Border Stones, Frost Loom, Silk-fall | Snover, Snom, Cubchoo, Swinub, Bergmite, Vanillite, Deerling, Stantler, Teddiursa, Smoochum, Delibird | **Frostwick 570**: rime-silk, honey and silk for furs, eel and whale oil · Elowen treehouses above Isenmar longhouses · Meridian survey pegs and the sunburst stamped over both seals · "The Two Hearths" |
| A2 | Northern Rimewood | deep snow-forest of royal hunting lodges | as A + Abomasnow, Sawsbuck, Ursaring | **Snowbriar 710**: furs, venison · lodges + trappers · game laws vs clan rights · "The White Stag" |
| B | **The Icefall Locks** (Isenmar/Zenith) | Frozen falls off the escarpment harnessed by brass sluices, turbines and an ice-lift. Lattice pylons frozen into the ice | Magnemite, Pawmi, Wattrel, Tadbulb, Snover, Bergmite, Plusle/Minun | **Brassfall 590**: cut ice for batteries and scrip · ice-cutters' union + lock engineers · scrip vs pay; the Lattice drains the Ebb · "The Ice Elevator" |
| B2 | The Mast Glacier | airships ice-anchored to a glacier tongue | Ice × Flying/Steel | **Anchorhold 730**: mooring rights · anchor-smiths + pilots · smugglers vs embargo · "Cut Loose" |
| C / C' | **The Brass Dunes** (Zenith/Ossaria) | Dune-buried locomotives, sand-scoured brass, a broken viaduct; slag mesas near Cogsworth | Sandshrew, Silicobra, Hippopotas, Phanpy, Rufflet, Electrike, Orthworm | **Copperdune 610**: fossils for coal and rails · caravanserai + freight depot · Meridian drill crews, tomb-robbers · "Tomb Freight" |
| D | **The Leach Canyons** (Ossaria/Nadir) | Blue-glowing toxic canals through sandstone, poisoned fossil beds, mine adits | Ekans, Gulpin, Shroodle, Maschiff, Skorupi, Krokorok, Glimmet | **Charwell 630**: Ossarian bone-char filters clean Nadir's poison · char-burners + sump-folk · who owns clean water · "Clean Water" |
| E | **The Sulfur Reach** (Nadir/Ashkaar) | Acid hot springs, sulfur flats, boiling yellow pools; Lake Sallow as a vast hot spring; the Ironway pass | Salandit, Charcadet, Numel, Scraggy, Houndour, Capsakid, Cyclizar | **Scaldwater 650**: sulfur, spa rights, mercenary contracts · the Truce of the Baths · Ashkaar recruiting Nadir youths for the war · "Truce of the Waters" (comic brawl) |
| M | **The Cinderglass Barrens** (Ashkaar/Ossaria) | Obsidian dunes, a petrified ash forest, lava tubes, glass-storms | Carkol, Magcargo, Torkoal, Vibrava, Gible, Sudowoodo, Onix, Rhyhorn, Golett | **Glasswake 670**: glass, lenses, black mirrors (the source of the Grave Glass) · furnace-masters + sand-merchants · conscripted glassblowers, Elector tariffs · "The Glassblower's Apprentice" |
| F | **The Rootdeep** (Nadir/Elowen) | Giant roots through mine shafts, glowing fungus, root-cathedrals, overgrown carts | Foongus, Parasect, Shiinotic, Breloom, Toedscruel, Bramblin, Machoke, Scraggy | **Lanternroot 690**: lamp-moss and mushroom ale for ore · fungus-growers + miners · sacred roots vs seams · "The Root That Bleeds". South hamlet **Mothwell 850** |
| G | **The Wired Wood** (Zenith/Elowen) | Vine-wrapped Lattice pylons, clockwork orchards, greenhouse-factories, Glasswood crystals along the cables | Luxray, Boltund, Klang, Floette, Granbull, Tinkatuff | **Verdigris 750**: fruit and silk for tools · Meridian managers + orchard workers · the crystal creep · "Clockwork Bees" |
| H | **The Looking-Glass Wood** (Elowen/Antumbra) | Reflections that disagree, rivers running uphill near Mirror Mere | Kirlia, Flittle, Rabsca, Ribombee | **Glassmere 753**: mirror-readings for bread · fisherfolk + "reflections" · people coming back reversed · "Your Other Half" |
| I | **The Obsidian Barrows** (Antumbra/Ossaria) | A necropolis of obsidian tomb-mirrors that became gates; shadows fall upward; the inverted desert hangs in the sky | Palossand, Golurk, Claydol, Runerigus, Inkay, Absol, Houndstone | **Vigil 770**: embalming, consulting echoes · embalmers + mediums · tomb-law vs the Synod's claim on the dead · "The Unquiet Elector" |
| L | **The Hanging Stair** (Zenith/Nadir) | The cliff beneath Zenith: cable lifts, outflow falls, shanty scaffolds, the drowned coast | Magneton, Klang, Bisharp, Skuntank, Muk, Scrafty | **Midstair 830**: tolls on everything going up or down · servants + workers · Meridian curfews · "The Lift Strike" |
| J | **The Thornwar Marches** (Elowen/Ashkaar) | Ash-grey giants with ember leaves that burn without dying, charcoal clearings, Thornwar forts, fire-lily meadows | Scovillain, Centiskorch, Volcarona, Talonflame, Leavanny, Flygon | **Thornwatch 870**: charcoal for tools · burners + smiths · Thornwar memory, the Dominar's legions · "The Truce Bell" |
| K | **The Pilgrim Pass** (Ashkaar/Crownhaven) | Eighteen roadside shrines, pilgrim camps, Ashkaar toll-forts | mixed high level | **Pilgrim's Rest 890**: lodging, relics · every kingdom's pilgrims · tolls on a sacred road · "Eighteen Shrines" |
Full Act I spec (Rimewood stretch) is in maps.json (560, 562, 563, 570–576, 561, 564, 565, 568) and §7. The rest are outlines.

---
## 7. Act I map layouts (detail; exact data in maps.json)

> **Revision 13-14 note (cartographer):** the town descriptions below still hold. The *road* maps are superseded by
> §11 and `design/ROUTES.yaml`: new names, the Saltmere-first order, target sizes 2-4x these, and new legs
> (527, 528, 552, 566, 577, 578). Where a road paragraph here disagrees with §11, §11 wins.

**Ferrow's Landing (100)**, 40×32, Outside. South coast ferry village, Elowen.
```
 TTTTTTTTTTTTTTTTT[N exit to the Ferrymen's Mile]TTTTTTTTT
 T        +--LAB(103)--+                T
 T  PC    |  Larch     |      MART      T
 T (101)  +------------+     (102)      T
 T   ...cobbled main street x18-21...   T
 T INN(104)  CUSTOMS(108)  DOCK(107)  LIGHTHOUSE(105)
 ~~~~~~~~~~~~~~~~|pier|~~~~~~~~~~~~~~~~~~
 ~~~~~~~~~~~~~~~~|BERTH (Dovetail)|~~~~~~
```
Prologue: 110 cabin → 109 deck (Voss) → berth (19,28) → Customs (NULL scan) → Lab (starter) → Lighthouse (Kestrel, K1).

**Revision 14 chain (Act I).** 100 → **520** (N: **521** Windfall Row branch: Hale Farmhouse 523, Glassed Orchard 522; its W forest road to 524 is corded off until the Glass Matriarch falls) → W at the Hale Bell: **527** Lacecliff Walk → **528** Marram Down → **140 Saltmere** (East Gate; Gym 1 in the Old Town 147) → North Gate (opens after the Pageant, S108): **541** the Grey Saltings (Brinecut 544/545) → **552** the Dyers' Ford → **540** Thistledown Lea (Thistledown Manor 546/547) → **524** Gossamer Wood (W edge) → **120 Briarwick** (Gym 2) → North Gate: **566** Spinners' Rise → **577** Frostwick Pass → **570** Frostwick → **578** Rimewood Path → **562** the Rimewood → **561** Gullcry Cliffs → **160 Ebbmouth**. Side road: **560** Frostflat Causeway, Frostwick (S) ↔ Saltmere (West Gate), chained at the Border Stones until the PC reaches Frostwick. Cocoonfall Hollow (548) is entered only through the Gossamer Deepwood (525), after Tamsin's badge. Names and leg detail: §11 and `tools/worldmap/world_data.py`. The paragraphs below describe the maps as built; where a connection changed, the new one is given.

**The Ferrymen's Mile (520)**, 26×48 coastal heath going N. One-way ledge row at y24 (a shortcut home). Juno's catching tutorial at the south end. 2 trainers.
**Windfall Row / Windfall Row (521)**, 60×26 E–W orchards. Hale Farmhouse (523, Headbutt tutor). In the NE corner is a quarantine cordon around the **Glassed Orchard (522)**, the first Bleed Veil scene. The W edge leads into Gossamer Wood, but the Accord has corded that forest road off (the Glasswood is across it); it opens from the wood's side after the Matriarch (V105 ≥ 1) as the shortcut home.
```
 Windfall Row:  [Wood]<==== hedgerow fields ==== FARM ==== orchard trees ==== [cordon|Glassed Orchard]
                                                     ||
                                                  (The Ferrymen's Mile below)
```
**Gossamer Wood (524)**, 48×48, SILKWOOD. Silk-web walls (decor events) make a trail S→N with two side loops. Woodward's Hut (526) sits in the central clearing. A Cut tree on the E edge leads to **Deepwood (525)**, an optional pond area you return to after Tamsin's badge (Cut). Rev 14: the main entrance is now the W edge from Thistledown Lea; the S warp to Windfall Row is the corded forest road.
**Briarwick (120)**, 44×40. Six hollow giant trees joined by rope bridges, with the Loomhouse Gym (Gym 2, the biggest tree) at the north. Rev 14: reached from Gossamer Wood; the North Gate leads to Spinners' Rise (566). The old W edge → Thistledown Lea is no longer on the main road. The Cutter's House gives HM01 after Tamsin's badge.
**Thistledown Lea (540)**, 64×28 river meadows. River along the south third with a stone bridge. On the N hill is Thistledown Manor (546/547, optional haunted house: furniture that moves, a portrait-order puzzle, Greavard in the attic). Rev 14: the Lea is now the third leg of the Weavers' Road (W: the Dyers' Ford, E: Gossamer Wood), and the manor is a Ch3 detour. The NW copse warp to **Cocoonfall Hollow (548)** is retired: the Hollow is entered through the Deepwood. The cave mouth is the Brinecut Mine shortcut back to the Saltings.
**The Grey Saltings / the Grey Saltings (541)**, 30×52 salt marsh to shingle beach (BEACH). Boardwalks over still-water pools. The Brinecut Mine (544) mouth is in the E chalk cliff. Rev 14: the first leg of the Weavers' Road: S edge → Saltmere's North Gate, N edge → the Dyers' Ford (552).
**Saltmere (140)**, 48×40, the Elowen free port and **Gym 1**. Market square, the harbour and breakwater (146) to the S, the Old Town (147) with the Pell Playhouse (gym), and the Lantern Theatre (145, the Pageant and the Mourner's hijack). J1 happens on the promenade green. The Eevee gift comes with Badge 1. Rev 14 gates: East Gate ← Marram Down (528); North Gate → the Grey Saltings (opens after S108); West Gate → Frostflat Causeway (side road, chained until Frostwick).
**Frostflat Causeway (560)**, 64×30. Rev 14: a **side road**, the quick coast road from Frostwick back to Saltmere's West Gate, chained at the Border Stones until the PC first reaches Frostwick by the Pass. A raised salt road; the crust turns from salt (Saltmere end) to frost (Frostwick end), and the first Ice slide tiles appear. The Border Stones carry both kingdoms' arms with a Meridian sunburst bolted across them. A spur leads to **The Rehearsal (568)**. The main Act I border crossing is now Frostwick Pass (577), at the Handfast Arch.
**Frostwick (570)**, 44×40, the borderland village. Elowen treehouses sit in ice-glazed giant trees above Isenmar turf-and-whalebone longhouses. The frozen Hoar Brook (with ice-fishing holes) crosses the square, the Hearth Stone stands in it, and the E gate is a whale-rib palisade wrapped in briar (Rev 14: the arrival gate, from Frostwick Pass; the S gate leads to the Frostflat Causeway). Buildings: PC 571, The Exchange 572 (mart + barter), The Two Hearths inn 573 (sidequest), Rime-silk Loft 574, Border House 575 (customs: forester, huscarl and a Meridian clerk), Halvard's Smokehouse 576. N edge → Rimewood Path (578) → the Rimewood.
**The Rimewood (562)**, 48×56. Oldwood frozen in hoar: ice-glazed giant boles and frozen-silk curtains make the walls. Features: a frozen-brook slide shortcut, a fallen giant-tree bridge, the trapper's lean-to (heal), the Frost Loom, and an aurora clearing. 5 trainers. The E Cut sapling leads to **Rimewood Glade (563)** (the Silk-fall, a pond slide puzzle for Never-Melt Ice, the Snowveil Shrine). N edge → Gullcry Cliffs.
**Gullcry Cliffs (561)**, 30×60, the first true Isenmar ground: whalebone waymarkers, a cod-skull cairn, stilt fishing huts. A landslide at y28–32 forces the detour through **Gullcry Caves (564)**. K2 waits at the N end, and the N edge leads to Ebbmouth.
```
 120 Briarwick --N--> 566 Spinners' Rise --> 577 Frostwick Pass --> 570 FROSTWICK --N--> 578 Rimewood Path --> 562 Rimewood --N--> 561 Gullcry --N--> 160 Ebbmouth
                                                                   | S gate                                 | E (Cut)             | W cliff mouths
             140 Saltmere (W Gate) <-- 560 Frostflat Causeway (side road) --+                           563 Glade           564 Gullcry 1F -- 565 B1F
                                              | spur: 568 Rehearsal
```

**Ebbmouth (160)**, 46×42, Isenmar's warm southern port. The River Ebb runs through it (x30–35), and its **current tiles flip with day/night** (two event pages), which is the Imprint's signature. Canals and stilt houses. The Tidelock Gym is the lock-house on the river (E). The Reyes House cellar (166) holds the Hollow cell. The Anglers' Guild gives the Good Rod after B3.
**The Reedholms (580)**, 52×42 delta reed-beds: a mesh of still-water channels crossed by boardwalks, rain. The NW dam leads to the **Voltaic Sluiceworks (584/585**, optional, static Rotom Lv25). The W bank leads to **Ebb Hollow (588)**.
**The Icefall Locks (581)**, 32×52 switchbacks up the frozen falls of the Lumen escarpment (borderland B; town Brassfall 590). The fenced Meridian Extraction Lattice #4 is a story landmark. Lumen South Gate (582) is at the top.
**Lumen City (180 Concourse 64×52, 181 Lowlight 40×30)**. A white-stone grid with a central Prism fountain plaza, Meridian Spire in its own Spire District (195; interiors 185/186, Act I gala and Shatter), the Circuit Gym to the W, and the Dept. Store (183/184) and Fossil Lab (188) to the S. The Lowlight district steps down to the SE. After the Shatter (end of Act I), a story switch swaps 181 for the Bleed map **608**. The Static Tunnels entrance (Act II, needs Flash) is at the NE rail tunnel.

---
<!-- ROUTES:BEGIN (generated by tools/worldmap/gen_docs.py) -->
## 11. The Eighteen Roads (SPINE Revisions 13-14)

No place is called "Route N" any more. Each **road** joins two gym towns and has a name; each road is **two or more large maps** (legs), each with its own name, landmark, wild flavour, field and at least one secret or side path. Machine-readable plan: **`design/ROUTES.yaml`** (the map builder's input). Every map's old and new name: **`design/PLACE_NAMES.md`**. Geography and the region map: **`design/WORLD_MAP.md`**, `art/previews/world_map.png`. Source of all three: `tools/worldmap/world_data.py`.

**Size means density.** Early legs grow to 64-140 tiles on their long side (2-4x the old maps). Size is never empty: every leg lists what fills it (`fill`), roughly one feature per 400 tiles, plus 4-6 trainers, a heal point on long legs, a Road Stone (the collectible milestone, one per road), shortcuts that open from the far end, and grass in separate patches with sight lines broken by the landform. Rule of thumb for the builder: no straight empty corridor longer than 12 tiles, and every dead end pays (item, view, NPC or secret).

**Revision 14 chain.** Ferrow's Landing -> the Strand Road (coast) -> **Saltmere, Gym 1** -> the Weavers' Road (inland, up the Selvedge) -> Gossamer Wood -> **Briarwick, Gym 2** -> the Hoar Road (north over the fells into the Rimewood) -> Frostwick -> **Ebbmouth, Gym 3**. Map IDs do not change; `segment` in maps.json does.

| Road | Name | From -> to | Legs (target size, tiles) | Chapter |
|---|---|---|---|---|
| 1 | **The Strand Road** | Ferrow's Landing -> Saltmere | The Ferrymen's Mile 520 64x110 -> Windfall Row 521 120x70 (branch) -> Lacecliff Walk 527 140x64 -> Marram Down 528 110x80 | Ch 1-2 |
| 2 | **The Weavers' Road** | Saltmere -> Briarwick | The Grey Saltings 541 70x110 -> The Dyers' Ford 552 80x72 -> Thistledown Lea 540 130x64 -> Gossamer Wood 524 90x110 | Ch 3 |
| 3 | **The Hoar Road** | Briarwick -> Ebbmouth | Spinners' Rise 566 80x120 -> Frostwick Pass 577 72x96 -> Rimewood Path 578 80x88 -> The Rimewood 562 96x110 -> Gullcry Cliffs 561 64x130 -> Frostflat Causeway 560 140x64 (side) | Ch 4 |
| 4 | **The Lock Road** | Ebbmouth -> Lumen City | The Reedholms 580 110x90 -> The Icecutters' Haul 592 110x70 -> The Icefall Locks 581 72x120 -> The Arc-Lamp Mile 593 110x64 | Ch 5 |
| 5 | **The Brass Road** | Lumen City -> Duneholt | The Meridian Mainline 612 130x64 -> The Brass Dunes 600 130x72 -> The Rib Road 601 72x120 -> Sunbleach Flats 613 110x64 | Act II |
| 6 | **The Leach Road** | Duneholt -> Mirefen | The Marrow Road 620 130x70 -> The Kneeling Stones 632 90x80 -> The Leach Canyons 621 100x100 -> The Gutterfall 633 80x96 | Act II |
| 7 | **The Sulfur Road** | Mirefen -> Cindervault | Leechman's Walk 640 120x72 -> Lake Sallow 641 120x100 -> The Pyre Road 652 130x70 | Act II |
| 8 | **The Iron Road** | Cindervault -> Ironreach | The Ashmarch 660 120x72 -> The Ironway 661 150x70 -> The Long Drop 672 64x130 -> The Cinderglass Barrens 662 130x90 (side) -> The Wyrmtongue 673 64x120 (side) | Act II |
| 9 | **The Root Road** | Ironreach -> Verdance | The Tailings 692 100x70 -> The Rootdeep 680 72x130 -> Prism Falls 681 130x80 -> The Briarway 693 72x120 | Act III |
| 10 | **The Hart Road** | Verdance -> Rimeholt | The Hart's Run 700 140x70 -> The Hoarwood 701 80x130 -> The Whalebone Road 712 72x120 | Act III |
| 11 | **The Mast Road** | Rimeholt -> Skyreach | The Thane's Sled-Road 720 140x72 -> The Mast Glacier 721 72x130 -> The Tetherline 732 130x64 | Act III |
| 12 | **The Glass Road** | Skyreach -> Lucent | Conductors' Causeway 740 72x130 -> The Wired Wood 741 80x130 -> The Looking-Glass Wood 752 100x90 -> Widdershins Walk 755 100x80 | Act III |
| 13 | **The Grave Road** | Lucent -> Cragholm | Yesterday's Road 772 110x64 -> The Obsidian Barrows 760 130x80 -> Spinefall Gorge 761 72x130 -> The Vertebrae 773 64x120 | Act IV |
| 14 | **The Moor Road** | Cragholm -> Gravenmoor | The Jawbone Ridge 780 150x72 -> Hindmoor 781 80x130 -> Downflame Road 790 110x70 | Act IV |
| 15 | **The Slag Road** | Gravenmoor -> Cogsworth | The Noonless Road 800 140x70 -> The Dry Tide 810 140x72 -> The Slag Mesa 801 80x130 -> The Smokestack Parade 811 120x64 | Act IV |
| 16 | **The Drowned Road** | Cogsworth -> Underveil | The Brink 832 130x60 -> The Hanging Stair 820 72x150 -> The Drownings 821 120x120 | Act IV |
| 17 | **The Blind Road** | Underveil -> Gloaming | The Throat 852 64x110 -> The Blindwater 840 150x80 -> The Gloamwood Verge 841 72x130 | Act V |
| 18 | **The Truce Road** | Gloaming -> Wyrmrest | The Gloamwood 860 140x80 -> The Thornwar Marches 861 80x130 -> The Wyrmspine 872 150x72 | Act V |
| 19 | **The Pilgrim Road** | Wyrmrest -> Crownhaven | Dominar's Toll 892 110x70 -> The Pilgrim Pass 880 80x140 -> The Coronation Road 893 150x64 | Act V |

### Road 1: The Strand Road (Ferrow's Landing -> Saltmere, Ch 1-2)

Ferrow's Landing west along the chalk coast to the free port. Chapter 1 lives on its first leg and the orchard branch; Chapter 2 arrives in Saltmere for Gym 1. Wild Lv 3-12 (Gym 1 cap 15).

**The Ferrymen's Mile (520)**, Elowen, `:MEADOW`, target **64x110** (was 44x68). 
*Name:* The mile the ferrymen walked each dusk to ring the Hale bell once the last boat was in.
- **Landmark:** The Hale Bell on its post above the sea cliff, and the stile where Larch sees you off.
- **Exits:** S: Ferrow's Landing. N: Windfall Row. W (new, at the Hale Bell): Lacecliff Walk, behind the quarantine roadblock (Accord guards, moved here from Windfall Row; lifts on S105).
- **Wild:** Lillipup, Wooloo, Skwovet, Fletchling, Rookidee, Lechonk, Rolycoly. Night: Hoothoot, Nickit, Tarountula.
- **Fill:** sea-cliff walk on the south-west side with Wingull posts and a view down to the moored Dovetail; Hale's Bramble: six berry terraces and a picking shed (Wenna's cousin sells tarts); the Minding Hedges: a three-turn hedge maze with a hidden Potion (the sign's joke made real); one-way ledge row (the shortcut home); Juno's catching clearing (fenced tutorial grass); sheepfold: herd three stray Wooloo back (the first small Trial-style errand); the old ferry-toll booth with its fare board (lore); Road Stone I: the first of the eighteen milestones (one per Road; take a rubbing of each); 4 trainers: Youngster Pim, Lass Dory, a shepherd, a bell-ringer's apprentice; gorse banks, drystone walls, a duck pond, two farm carts, a scarecrow.
- **Secret:** The Smuggler's Stair: behind the toll booth a bramble (Cut, after Briarwick) hides steps to the Ferryman's Rest, a sea cave with a rowboat, a Glass Apple and a night-only Nickit den.

**Windfall Row (521)**, Elowen, `:MEADOW`, target **120x70** (was 62x48). *Branch road.* 
*Name:* Orchard law: a traveller may keep any fruit that has already fallen, and nothing else.
- **Landmark:** The Cider Press yard, and the Accord's quarantine cordon across the lane to the Glassed Orchard.
- **Exits:** S: the Ferrymen's Mile. NE: the Glassed Orchard (Bleed Veil, Chapter 1). W: the corded forest road to Gossamer Wood (never opens from this side; opens from the wood once V105 >= 1, after the Matriarch). Door: Hale Farmhouse.
- **Wild:** Smoliv, Fidough, Bounsweet, Nidoran, Shinx, Litleo, Zigzagoon. Night: Oddish, Nymble, Spinarak. Headbutt: Combee, Cherubi, Heracross.
- **Fill:** six named orchards in rows (apple, pear, plum, cherry, quince, medlar); every tree a Headbutt tree; the Cider Press yard: press, barrels, a trade NPC, a cellar door; the Nidoran chase: a wild Nidoran runs between three orchards before it can be battled (Rev 13); beehive wall and a honey errand (Combee); scarecrow field: a Twins double battle; Accord cordon camp: two tents, wardens, the barrier events; windmill on a rise, duck pond, a farm stand selling berries; drystone lanes with carts, ladders against the trees, windfall-fruit items on the ground; 5 trainers: Bug Catcher Wim, Picnicker Ada, the Twins, a cider-maker, an orchard hand.
- **Secret:** The Thirteenth Row: the plum orchard has twelve rows on the sign and thirteen on the ground. The gap behind the thirteenth leads to a walled garden with a sleeping Applin (event Pokemon) and a Miracle Seed.

**Lacecliff Walk (527)**, Elowen, `:BEACH`, target **140x64** (new map). 
*Name:* The sea has worn the chalk into arches as fine as Briarwick lace; the weavers copy the cliffs, not the other way round.
- **Landmark:** The Lace Arches: a run of sea-cut chalk arches with the path going through three of them.
- **Exits:** E: the Ferrymen's Mile. W: Marram Down.
- **Wild:** Wingull, Pikipek, Skwovet, Buneary, Shellos, Krabby. Night: Hoothoot, Noibat. Tide pools: Corphish, Wiglett.
- **Fill:** cliff-top path weaving through three chalk arches (the third collapses into a ledge shortcut after Rock Smash); cliff stairs down to two coves: shingle, rock pools (Old Rod), a beached rowboat; the Wrecker's Lamp: a false light on a pole that a hermit swears he keeps for the gulls; Wingull rookery on a sea stack and a birder with binoculars (trade); gorse heath with a hidden field of sea-pinks (Flabebe swarms on clear mornings); the Lacemakers' Bench: a carved stone seat where Juno makes you rest (comedy beat); smugglers' signal pole that answers Ferrow lighthouse (lore for Kestrel's sidequest); Road Stone I-b; 5 trainers: a fisher, a hiker, a beachcomber, a Lass, a painter at an easel.
- **Secret:** The Lost Thread: under the second arch, a cave only reachable at low tide (night) holds a weaver's drowned sample-book (Briarwick lore) and a Shell Bell.

**Marram Down (528)**, Elowen, `:BEACH`, target **110x80** (new map). 
*Name:* Dune-down held together by marram grass. Saltmere fines anyone who pulls it up, which is why it is still here.
- **Landmark:** The Saltmere Beacon on the highest dune, and the first view of the port and its salt lake.
- **Exits:** E: Lacecliff Walk. W: Saltmere (East Gate).
- **Wild:** Sandygast, Silicobra, Nacli, Bunnelby, Dwebble, Tandemaus, Wingull. Night: Spinarak, Volbeat.
- **Fill:** rolling dunes with marram tall grass in pockets (dune crests block sight lines, so trainers ambush); the Beacon dune and its keeper's hut (heal once); a sand-sledge run from the Beacon down to the shore (one-way, fun shortcut); Saltmere's outer pageant camp: wagons of travelling players rehearsing (hints at Gym 1's stage); a shipwrecked theatre barge half buried in the sand (props, costumes, a hidden TM); bird-hide over a brackish pool (Old Rod); the toll-free stile into Saltmere and a Free Port charter stone; 5 trainers: two actors in costume (double), a kite flier, a sand-sculptor, a dune guard.
- **Secret:** The Prompter's Box: a sunken box in the theatre barge, dug up with a sand-shovel from the camp, holds the Prompter's Script (Gym 1 hint) and a Normal Gem.

### Road 2: The Weavers' Road (Saltmere -> Briarwick, Ch 3)

Inland from the port up the River Selvedge to the silk forest: the road Briarwick's cloth comes down. Salt marsh, then the dyers' river, then the manor meadows, then the Gossamer Wood. Wild Lv 12-17 (Gym 2 cap 19).

**The Grey Saltings (541)**, Elowen, `:BEACH`, target **70x110** (was 30x52). 
*Name:* Saltmere's salt comes from this marsh. 'Grey' is the salt before it is washed, and the weather.
- **Landmark:** The salt pans and the smoke of the boiling-house, with the chalk cliff of Brinecut behind.
- **Exits:** S: Saltmere (North Gate). N: the Dyers' Ford. E cliff: Brinecut Mine. Door: the Brinewife's Rest.
- **Wild:** Nacli, Bunnelby, Crabrawler, Dwebble, Sandygast, Tandemaus, Minccino. Water: Shellos, Wingull, Tentacool. Rock Smash: Binacle.
- **Fill:** boardwalk maze over tidal pools; planks that are only laid at low water (night); salt pans with rakers, white salt stacks, the boiling-house; wreck of a salt barge in the mud (item, later Rock Smash); bird hide (a Squawkabilly watcher who trades); samphire pickers, and a mudflat of Sandygast 'castles' built by children; the Crabrawler ring: a comic boxing errand; a Nacli herd that crosses the path on a timer; the Brinewife's Rest (rest house); 5 trainers; Road Stone II.
- **Secret:** The Drowned Lane: at night the tide uncovers an old cart road to a tidal islet with a wreckers' cache (and a locked chest that needs the Harbour Office key from Saltmere).

**The Dyers' Ford (552)**, Elowen, `:MEADOW`, target **80x72** (new map). 
*Name:* Briarwick's dyers wash their cloth here, so the river runs red, blue and yellow in three bands.
- **Landmark:** The Three Waters: the Selvedge in three coloured bands below the dye-works, crossed by stepping stones.
- **Exits:** S: the Grey Saltings. N: Thistledown Lea.
- **Wild:** Smeargle, Mareep, Flabebe (red, blue or yellow by bank), Cottonee, Marill. Night: Volbeat, Illumise, Oddish. Fishing: Goldeen, Basculin (red-striped in the red band, blue-striped in the blue).
- **Fill:** dye-works: three vat sheds and drying lines you walk under like corridors; madder, woad and weld fields: three colours of tall grass, each with its own encounter slice; the stepping-stone ford (run and you slip into the shallows); vat-yard sluice puzzle: step the three colours in the order the foreman hums; fulling mill with hammers (works as a moving obstacle); cloth barge at a jetty: after the foreman's errand it carries you back to Saltmere; the Smeargle that paints your lead Pokemon's mark on a boundary stone; sheep-wash pool and shearers; 5 dyer trainers with colour-themed teams; shrine of the Fourth Colour (a white ribbon nobody will dye).
- **Secret:** The white water: one thin band of the river is not dyed at all. Follow it upstream through a culvert to the Bleachfield, a small Bleed-touched meadow of white flowers with a TM and one Imprinted encounter.

**Thistledown Lea (540)**, Elowen, `:MEADOW`, target **130x64** (was 64x28). 
*Name:* The river meadows held by House Thistledown until the house died out. Nobody has mown them since.
- **Landmark:** Thistledown Manor on its hill, and the old stone bridge over the Selvedge.
- **Exits:** S: the Dyers' Ford (replaces the old Grey Saltings edge, on the same south side). E: Gossamer Wood (the wood's west eaves). N hill: Thistledown Manor. Cave: Brinecut Mine (the shortcut back to the Saltings). No warp to Cocoonfall Hollow any more: it is entered through the Deepwood.
- **Wild:** Ponyta, Blitzle, Flabebe, Cottonee, Sentret, Doduo, Pancham, Mankey. Night: Morelull, Snubbull, Stunky. Water: Marill, Buizel, Psyduck.
- **Fill:** wildflower meadow in bands of colour, tall grass in four separate fields; the River Selvedge along the south third with two islets (Surf later); stone bridge with a fisherman and a toll that nobody collects; the manor's ruined wall, gateposts and overgrown topiary garden; Ponyta paddock and a drover who races you along the fence; broken mill and mill-race (Old Rod); mowers' camp with hay-ricks and a cook-fire (heal once); bamboo stand with Pancham; 6 trainers including a double battle; Road Stone II-b.
- **Secret:** The Ha-ha: a sunken wall runs round the manor hill. Its ditch is a hidden path to the back garden and a cellar door into the manor's crypt (a second way in, with a Greavard digging there).

**Gossamer Wood (524)**, Elowen, `:SILKWOOD`, target **90x110** (was 50x58). 
*Name:* Kept name: the silk forest that gives Briarwick its trade.
- **Landmark:** The Weft Bridge, a rope of spun silk as thick as a road, and Woodward's Hut in the middle clearing.
- **Exits:** W: Thistledown Lea (new edge). N: Briarwick. S: the corded forest road to Windfall Row (opens from this side when V105 >= 1, after the Matriarch). E (Cut, after Badge 2): Gossamer Deepwood, and Cocoonfall Hollow beyond it.
- **Wild:** Sewaddle, Scatterbug, Blipbug, Cutiefly, Petilil, Shroomish, Sizzlipede. Night: Morelull, Phantump, Venonat. Headbutt: Pineco, Heracross, Pinsir.
- **Fill:** silk-curtain trail west to north with two side loops; canopy walkways on an upper level (rope bridges between giant trunks); cocoon grove, silk-harvest racks and three weavers at work; Woodward's Hut (heal) in the central clearing; fallen giant trunk used as a tunnel; mushroom ring that glows at night; thread-line shortcuts that open from the far side; 6 trainers including Twins Mo & Jo (re-levelled for segment 1); TM Giga Drain grove.
- **Secret:** The Unpicked Seam: one silk wall opens only at night. Behind it a Heracross and a Pinsir are fighting over a sap tree; whichever you help leaves, and the other can be caught.

### Road 3: The Hoar Road (Briarwick -> Ebbmouth, Ch 4)

North out of the Gossamer, over the hoar downs into borderland A (the Rimewood) and down Isenmar's cliffs to Ebbmouth. Frostflat Causeway becomes the coast road back to Saltmere. Wild Lv 16-21 (Gym 3 cap 23).

**Spinners' Rise (566)**, Elowen, `:MEADOW`, target **80x120** (new map). 
*Name:* The drove road up out of the Gossamer where Briarwick's spinners met the hill shepherds to buy fleece.
- **Landmark:** The Fleece Cross: a market cross on the ridge where the old wool fairs were held, hung with prayer-yarn.
- **Exits:** S: Briarwick (North Gate). N: Frostwick Pass.
- **Wild:** Mareep, Wooloo, Skiddo, Deerling, Swablu, Tauros, Nincada. Night: Hoothoot, Noctowl, Spinarak. Higher up: Swinub, Snom.
- **Fill:** switchback drove road from forest edge to open fell (the trees thin out as you climb); sheepfolds and a shepherd's hamlet of three cottages (one becomes a fast-travel rest); the Fleece Cross and its yarn-tied prayer ribbons (a Ribbon errand); a hill fort ring on the summit with a view back over the Gossamer to the sea; the Ram Race: a Skiddo-riding shepherd boy challenges you up the hill (Rev 13 event Pokemon); stone sheep-wash and a cold spring (Old Rod); first snow patches near the top, then the hoar line; 5 trainers: shepherd, hiker, two spinners (double), a wool merchant; Road Stone III.
- **Secret:** The Shearing Cave: behind a waterfall in the sheep-wash, a cave where the shepherds hide the best fleece from the tax-man holds a Soft Sand and a sleeping Dubwool's lost lamb (a Wooloo that joins you).

**Frostwick Pass (577)**, Borderland (Elowen/Isenmar), `:SNOWY_MOUNTAIN`, target **72x96** (new map). 
*Name:* The low pass over the hoar downs into Frostwick. Both kingdoms claim it and neither keeps the toll hut.
- **Landmark:** The Handfast Arch: half whale-jaw, half living briar, raised when the border was last agreed, with a brass Meridian sunburst newly bolted across its keystone (the Chapter 4 border beat).
- **Exits:** S: Spinners' Rise (the drove road comes up from the south). W: Frostwick (East Gate, the whale-rib palisade).
- **Wild:** Snom, Swinub, Snorunt, Stantler, Deerling, Cubchoo, Delibird. Night: Sneasel, Smoochum.
- **Fill:** the climb through hoar-crusted downs; the wind gap: gust tiles that push you back unless you move between gusts; the empty toll hut with two ledgers, one per kingdom, that disagree; a frozen tarn with an ice-fishing hole (Old Rod); avalanche fences and a snow-buried signpost in two scripts; shepherd's bothy (rest and a hot drink); trappers' drying racks; a row of snowmen built by Frostwick children; one is a Snorunt; 4 trainers: a huscarl, a forester, two sledgers; Road Stone III-b.
- **Secret:** Behind the frozen waterfall at the tarn is the Hollow of the Handfast: love-carvings of a forester and a huscarl and a Soothe Bell. It feeds Frostwick's sidequest 'The Two Hearths'.

**Rimewood Path (578)**, Borderland (Elowen/Isenmar), `:SILKWOOD`, target **80x88** (new map). 
*Name:* The trappers' blazed path into the frozen forest: a red axe-mark every twenty paces, and you do not leave them.
- **Landmark:** The Blaze-Trees, and the Lantern Birch where trappers leave a light for whoever is late.
- **Exits:** S: Frostwick (North Gate). N: the Rimewood.
- **Wild:** Snover, Cubchoo, Teddiursa, Deerling, Buneary, Swinub, Vanillite. Night: Sneasel, Snorunt, Morelull.
- **Fill:** hoar-birch outskirts thickening into ice-glazed giants; a frozen brook with a slide shortcut; charcoal burners' clearing with a kiln; trapper's lean-to (heal); the snare line: free a caught Teddiursa (it remembers you in the Rimewood); frozen silk curtains, brittle enough to break with Rock Smash; honey-stump hives; Frostwick woodcutters and a sledge of logs; 5 trainers; the Lantern Birch (relight it at night for a reward).
- **Secret:** The Unblazed: at the one tree with a blue blaze, leave the path. The wood repeats until you follow the Stantler tracks, which lead to a clearing with the herd and one Stantler that will fight.

**The Rimewood (562)**, Borderland (Elowen/Isenmar), `:SILKWOOD`, target **96x110** (was 48x56). 
*Name:* Kept name: the Elowen oldwood that froze when the sea did.
- **Landmark:** The Frost Loom and the aurora clearing.
- **Exits:** S: Rimewood Path. N: Gullcry Cliffs. E (Cut): Rimewood Glade.
- **Wild:** Snover, Bergmite, Cubchoo, Stantler, Teddiursa, Vanillite, Delibird. Night: Sneasel, Snorunt.
- **Fill:** ice-glazed giant boles and frozen-silk curtain walls; fallen giant-tree bridge; frozen-brook slide shortcut; trapper's lean-to (heal); the Frost Loom; aurora clearing; 5 trainers; the Teddiursa from the snare line, if freed, digs up an item here.
- **Secret:** Rimewood Glade (563) behind the Cut sapling: the Silk-fall, the pond slide puzzle for Never-Melt Ice, the Snowveil Shrine.

**Gullcry Cliffs (561)**, Isenmar, `:MOUNTAIN`, target **64x130** (was 30x60). 
*Name:* First true Isenmar ground. Named for the noise, which never stops.
- **Landmark:** Whalebone waymarkers along the cliff and the cod-skull cairn.
- **Exits:** S: the Rimewood. N: Ebbmouth. W cliff mouths: Gullcry Caves.
- **Wild:** Wingull, Ducklett, Cramorant, Taillow, Chatot, Bergmite, Wooper. Water: Swanna, Tentacool.
- **Fill:** cliff-top path with whalebone waymarkers; cod-skull cairn; stilt fishing huts and drying racks; the landslide that forces the detour through Gullcry Caves; sea-stack views with nesting birds; rope-and-plank cliff stairs; a signal-fire platform; Kestrel's battle ground at the north end (K2); 5 trainers; Road Stone III-c above Ebbmouth.
- **Secret:** The Gannet Stair: a rope stair down the cliff face to a rookery ledge, where a Cramorant has swallowed something that is not a fish.

**Frostflat Causeway (560)**, Borderland (Elowen/Isenmar), `:SNOWY_MOUNTAIN`, target **140x64** (was 64x30). *Side road.* 
*Name:* The raised salt road up the coast from Saltmere. Halfway along, the white underfoot stops being salt.
- **Landmark:** The Border Stones: Elowen's briar crown and Isenmar's whale and axe, with a Meridian sunburst bolted over both.
- **Exits:** E (the south end): Saltmere (West Gate). N: Frostwick (South Gate). Spur: the Rehearsal (Bleed Veil). Closed at the Border Stones by an Isenmar customs chain until you arrive in Frostwick by the Pass; then it is the quick road back to Saltmere.
- **Wild:** Spheal, Cetoddle, Snom, Swinub, Wiglett, Skitty, Miltank, Tauros, Dunsparce. Night: Smoochum, Snorunt.
- **Fill:** raised causeway with wind-fences and marker poles; salt-to-frost gradient along the whole map (the tiles change, then the weather); the Border Stones and a Meridian survey camp with pegs and a theodolite; drovers with a Miltank and Tauros herd blocking and unblocking the road; stranded salt wagon (errand: find the wheel pin); first ice-slide tiles on frozen brine pools; children sledging on the frost-flat; brine pools with Wiglett; 5 trainers: Lass Tilde, Sailor Haakon, Bird Keeper Ailsa and two more; Road Stone III-d.
- **Secret:** The Old Causeway: the first road lies under the ice beside the new one. An ice-slide run along it ends at a cairn with an Icy Rock and the name of whoever built it scratched out.

### Road 4: The Lock Road (Ebbmouth -> Lumen City, Ch 5)

Borderland B, the Icefall Locks: up the River Ebb to the foot of Zenith's escarpment and up the frozen falls.

**The Reedholms (580)**, Isenmar, `:SNOWY_MOUNTAIN`, target **110x90** (was 52x42). 
*Name:* The islets ('holms') of the Ebb delta, joined by boardwalks that are re-laid every spring.
- **Landmark:** The eel-weirs, and the north dam of the Voltaic Sluiceworks.
- **Exits:** W: Ebbmouth. E: the Icecutters' Haul. N dam: Voltaic Sluiceworks. S bank: Ebb Hollow.
- **Wild:** Wooper, Lotad, Tympole, Buizel, Goomy, Croagunk, Stunfisk, Azurill.
- **Fill:** a mesh of still channels and boardwalks in rain; eel-weirs and smoke huts; reed-cutters' punts (short ferry hops); a current that flips with day and night on two channels; heron islet; 6 trainers.
- **Secret:** A punt left untied at night drifts to the Sunk Holm, an islet off the boardwalks.

**The Icecutters' Haul (592)**, Borderland (Isenmar/Zenith), `:SNOWY_MOUNTAIN`, target **110x70** (new map). 
*Name:* The sled road the ice-cutters' union drags its blocks down, from the falls to the Ebbmouth boats.
- **Landmark:** Sawyer's Cross: where the Haul meets the forest track from Snowbriar to the Frostfang Pass (gated until Act III).
- **Exits:** W: the Reedholms. E: Brassfall. S gate: Snowbriar (Act III). N gate: Frostfang Pass (Act III).
- **Wild:** Bergmite, Snover, Mudbray, Pawmi, Magnemite, Wattrel.
- **Fill:** ice-sled ruts and block stacks; a union picket hut; haul-teams of Mudsdale; the crossroads gates; 5 trainers.
- **Secret:** A dropped ice block has something frozen inside it; thaw it in Brassfall.

**The Icefall Locks (581)**, Borderland (Isenmar/Zenith), `:SNOWY_MOUNTAIN`, target **72x120** (was 32x52). 
*Name:* The frozen falls of the escarpment, cut into steps and locks by Zenith's engineers.
- **Landmark:** The Ice Elevator and the fenced Meridian Extraction Lattice No. 4.
- **Exits:** W: Brassfall. N: the Arc-Lamp Mile.
- **Wild:** Magnemite, Pawmi, Wattrel, Tadbulb, Bergmite, Snover, Plusle, Minun, Togedemaru.
- **Fill:** switchbacks up the frozen falls; brass sluices and frozen turbine wheels; the cable lift; Lattice pylons; 6 trainers.
- **Secret:** Behind the third lock gate, an ice cave with a maintenance ledger.

**The Arc-Lamp Mile (593)**, Zenith, `:NEON_GRID`, target **110x64** (new map). 
*Name:* The first road in Velmora lit by electric arc lamps. Zenith counts its age from the night they were switched on.
- **Landmark:** One hundred numbered arc lamps, and Lumen's South Gate at the end of them.
- **Exits:** SW: the Icefall Locks. NE: Lumen South Gate.
- **Wild:** Yamper, Shinx, Pawmi, Rookidee, Klink, Magnemite. Night: Joltik, Voltorb.
- **Fill:** paved boulevard with lamp numbers; a tram stop without a tram; advertising hoardings; the lamplighters' depot; 5 trainers.
- **Secret:** Lamp 47 has been dark for ten years; the reason is under its base plate.

### Roads 5-19 (outline)

Each leg: name, target size, landmark, secret. Fill lists follow when the act is detailed.

**Road 5, The Brass Road** (Lumen City -> Duneholt, Act II). Borderland C, the Brass Dunes: the railway east off the plateau and into the sand that buried it.
- **The Meridian Mainline** (612, Zenith, `:MOUNTAIN`, 130x64): Zenith's first railway. You walk the service road beside the track. *Landmark:* The signal gantries and the mouth of the Static Tunnels. *Secret:* A signal box whose levers reroute a handcar to a siding.
- **The Brass Dunes** (600, Borderland (Zenith/Ossaria), `:DESERT`, 130x72): Kept name: dunes the colour of the locomotives buried in them. *Landmark:* The broken viaduct and the half-buried engine 'Progress'. *Secret:* A carriage door under the sand opens into a buried dining car.
- **The Rib Road** (601, Ossaria, `:DESERT`, 72x120): Waymarked by the ribs of a leviathan, one every hundred paces, set there before the Electors. *Landmark:* The Rib Gate: the two largest ribs, meeting overhead. *Secret:* Count the ribs: one is missing, and its socket is a stair.
- **Sunbleach Flats** (613, Ossaria, `:DESERT`, 110x64): The flats before Duneholt, where bones and cloth alike go white in a season. *Landmark:* The bleaching frames of the linen-makers and Duneholt's Sandgate on the horizon. *Secret:* A mirage well that is real at noon only.

**Road 6, The Leach Road** (Duneholt -> Mirefen, Act II). Borderland D, the Leach Canyons: down the poisoned river to Nadir's marsh.
- **The Marrow Road** (620, Ossaria, `:DESERT`, 130x70): It runs through the fossil beds where the rock is the colour of marrow. *Landmark:* The dig terraces and the mouth of the Ossuary of Dunes. *Secret:* An unlabelled dig pit with a complete skeleton nobody has reported.
- **The Kneeling Stones** (632, Ossaria, `:DESERT`, 90x80): Wind-cut pillars that look like bowed pilgrims. The crossroads of Ossaria. *Landmark:* The stones themselves, and the crossroads post: Duneholt, Charwell, Vigil. *Secret:* At dusk the stones' shadows point at one buried door.
- **The Leach Canyons** (621, Borderland (Ossaria/Nadir), `:WASTELAND`, 100x100): Kept name: the canyons the River Leach cut, glowing blue with what Nadir puts in it. *Landmark:* The blue canals and the bone-char filter towers. *Secret:* A dry side canyon with a clean spring that neither side knows about.
- **The Gutterfall** (633, Nadir, `:CORROSIVE_MIRE`, 80x96): Where the Leach drops off the canyon lip into the marsh. Nadir named it. *Landmark:* The blue waterfall and the ladder-town clinging beside it. *Secret:* A ledge behind the fall where the sump-folk leave their dead's lanterns.

**Road 7, The Sulfur Road** (Mirefen -> Cindervault, Act II). Borderland E, the Sulfur Reach: marsh causeways, the hot lake, then the Dominion's first road.
- **Leechman's Walk** (640, Nadir, `:CORROSIVE_MIRE`, 120x72): The plank causeway the leech-gatherers keep up. You pay them or you swim. *Landmark:* The leech-gatherers' stilts and the mouth of the Miasma Caverns. *Secret:* A sunk plank path that only shows when the marsh gas burns off.
- **Lake Sallow** (641, Borderland (Nadir/Ashkaar), `:ASHEN_WASTE`, 120x100): Named for its colour. The whole lake is one hot spring. *Landmark:* The yellow lake, its geysers, and Lantern Isle steaming in the middle. *Secret:* A geyser that lifts a surfer onto the cliff shelf above the lake.
- **The Pyre Road** (652, Ashkaar, `:ASHEN_WASTE`, 130x70): Lined with oath-pyres that are never let go out. Every legionary lights one before first posting. *Landmark:* The avenue of pyres and Cindervault's Caldera Gate. *Secret:* One pyre is cold. Lighting it calls the person it was lit for.

**Road 8, The Iron Road** (Cindervault -> Ironreach, Act II). West again over the higher pass. The war road north (the Cinderglass Barrens) leaves from the same gate.
- **The Ashmarch** (660, Ashkaar, `:ASHEN_WASTE`, 120x72): The legions' marching road. Ash falls on it every day and is swept every night. *Landmark:* The mile-forts and the Cinderhorn smoking to the east. *Secret:* A sweepers' tunnel under the road that the legion uses to move unseen.
- **The Ironway** (661, Borderland (Ashkaar/Nadir), `:MOUNTAIN`, 150x70): Kept name: the pass the ore came down, on rails laid by Nadir and paid for by Ashkaar. *Landmark:* The ore-cart incline and the Truce Posts. *Secret:* A runaway ore cart you can ride down a closed spur.
- **The Long Drop** (672, Nadir, `:SCRAPYARD`, 64x130): Ironreach's front door: a shaft road that goes down for an hour. Named by people who carried things up it. *Landmark:* The winding-tower and the cage lift. *Secret:* A side adit sealed with a pit-fighter's handprint in iron.
- **The Cinderglass Barrens** (662, Borderland (Ashkaar/Ossaria), `:ASHEN_WASTE`, 130x90, side road): Kept name: obsidian dunes where sand met fire. *Landmark:* Black glass dunes and lava tubes. *Secret:* A lava tube that comes out inside the Petrified Ashwood.
- **The Wyrmtongue** (673, Ashkaar, `:VOLCANIC`, 64x120, side road): The spit of black lava that runs out to the Cape, forked at the end like a tongue. *Landmark:* The forked spit and the Warfort's beacon. *Secret:* At the fork's left tip, a sea cave that looks across at the Rime Isles.

**Road 9, The Root Road** (Ironreach -> Verdance, Act III). Borderland F, the Rootdeep: out of the mines through the roots and up into Elowen's royal country.
- **The Tailings** (692, Nadir, `:SCRAPYARD`, 100x70): The mine-waste hills outside Ironreach. Kids sled down them on shovels. *Landmark:* Grey waste cones and the entrance to Grudgestone Quarry. *Secret:* A tailings slide that drops into a buried engine house.
- **The Rootdeep** (680, Borderland (Nadir/Elowen), `:CAVE`, 72x130): Kept name: where Elowen's roots come through the roof of Nadir's mines. *Landmark:* Root-cathedrals and overgrown ore carts. *Secret:* A root that bleeds when cut: the start of Lanternroot's sidequest.
- **Prism Falls** (681, Elowen, `:RAINBOW`, 130x80): Kept name: the falls throw a rainbow all day, every day. It is the Imprint. *Landmark:* The falls and the Rainbow Stair beside them. *Secret:* Behind the falls, a cave where the rainbow is the wrong way round.
- **The Briarway** (693, Elowen, `:FAIRY_TALE`, 72x120): The royal road to Verdance, hedged with briar on both sides by the first monarch and clipped ever since. *Landmark:* The clipped briar walls, the royal milestones, the Kingsgate ahead. *Secret:* A gardeners' door in the hedge to the Royal Chase's back fence.

**Road 10, The Hart Road** (Verdance -> Rimeholt, Act III). Borderland A again, in the north: royal hunting country, the snow-forest, over the Frostfang Pass to the frozen sea.
- **The Hart's Run** (700, Elowen, `:MEADOW`, 140x70): The line the royal hunt rides. No one else may gallop on it, and everyone does. *Landmark:* Hunting towers and the white hart carved into the chalk. *Secret:* The carved hart's eye is a trapdoor.
- **The Hoarwood** (701, Borderland (Elowen/Isenmar), `:SNOWY_MOUNTAIN`, 80x130): What Isenmar calls the northern Rimewood: older, deeper, and white all year. *Landmark:* Royal hunting lodges and frozen Bride-briar hedges. *Secret:* A lodge with one room that is still warm.
- **The Whalebone Road** (712, Isenmar, `:SNOWY_MOUNTAIN`, 72x120): Arched with whale ribs from the pass down to Rimeholt's Icewall Gate, one arch per thane. *Landmark:* The rib arches, each carved with a thane's name; the last is blank. *Secret:* The blank arch has a name on the inside.

**Road 11, The Mast Road** (Rimeholt -> Skyreach, Act III). Borderland B again, in the north: along the frozen sea, across the Mast Glacier and up the Cloudstair.
- **The Thane's Sled-Road** (720, Isenmar, `:SNOWY_MOUNTAIN`, 140x72): The coast road on the sea ice, kept open by the thane's own teams. *Landmark:* Sled posts, ice-fishing camps, the frozen sea to the north. *Secret:* A sled team that will run you out to a wreck locked in the ice.
- **The Mast Glacier** (721, Borderland (Isenmar/Zenith), `:SNOWY_MOUNTAIN`, 72x130): Kept name: airships are ice-anchored along the glacier tongue, and their masts look like a winter forest. *Landmark:* The anchored airships. *Secret:* A crevasse with an airship that never left.
- **The Tetherline** (732, Zenith, `:STORMFRONT`, 130x64): The walkway strung under Skyreach's mooring cables. Zenith calls it safe. *Landmark:* Cable gantries over a long drop. *Secret:* A maintenance cradle that crosses to a mast nobody uses.

**Road 12, The Glass Road** (Skyreach -> Lucent, Act III). South across the plateau, through borderlands G and H, and through the Mere into the kingdom behind the glass.
- **Conductors' Causeway** (740, Zenith, `:STORMFRONT`, 72x130): The road between the lightning rods ('conductors') that feed the Lattice. It hums. *Landmark:* Rows of conductors and Stormwatch Spire. *Secret:* One conductor is grounded, and something lives in the quiet.
- **The Wired Wood** (741, Borderland (Zenith/Elowen), `:SILKWOOD`, 80x130): Kept name: forest grown up Zenith's pylons, or pylons planted in Elowen's forest, depending who you ask. *Landmark:* Vine-wrapped pylons and clockwork orchards. *Secret:* A greenhouse-factory whose clockwork bees have gone wild.
- **The Looking-Glass Wood** (752, Borderland (Elowen/Antumbra), `:MINDSCAPE`, 100x90): Borderland H. The reflections in its pools do not always agree with what is standing over them. *Landmark:* Pools that reflect the wrong sky, and a stream that runs uphill. *Secret:* Walk a path backwards and it goes somewhere else.
- **Widdershins Walk** (755, Antumbra, `:INVERSE`, 100x80): The first road in Antumbra. It can only be walked against the sun, and here the sun agrees. *Landmark:* A colonnade whose shadows fall toward the light. *Secret:* Turn sunwise three times and the road is not there.

**Road 13, The Grave Road** (Lucent -> Cragholm, Act IV). Borderland I, the Obsidian Barrows: out of Antumbra through the tomb-mirrors into Ossaria's high crags.
- **Yesterday's Road** (772, Antumbra, `:INVERSE`, 110x64): Travellers arrive at the far end before they set out. The Synod taxes both ends. *Landmark:* Milestones that count down, then up. *Secret:* A traveller on the road who is you, a little earlier.
- **The Obsidian Barrows** (760, Borderland (Antumbra/Ossaria), `:INVERSE`, 130x80): Kept name: a necropolis of obsidian tomb-mirrors that became gates. *Landmark:* The tomb-mirrors and the desert hanging in the sky. *Secret:* A mirror with no tomb behind it.
- **Spinefall Gorge** (761, Ossaria, `:DESERT`, 72x130): The river comes down over the backbone of something that was a mile long. *Landmark:* The waterfall over fossil vertebrae. *Secret:* A dry cave behind the fall with a nest of something revived.
- **The Vertebrae** (773, Ossaria, `:MOUNTAIN`, 64x120): A stair of round stone drums up to Cragholm, each one a step and a bone. *Landmark:* The drum-stair and Cragholm's lift towers above. *Secret:* One drum is hollow.

**Road 14, The Moor Road** (Cragholm -> Gravenmoor, Act IV). Along the ridge back to Vigil, through the Grave Glass, and across Antumbra's moors.
- **The Jawbone Ridge** (780, Ossaria, `:MOUNTAIN`, 150x72): A ridge with a toothed skyline. Cragholm says the teeth were cut; Vigil says they grew. *Landmark:* The teeth, and the Darkglass Mine headframe. *Secret:* A cave in the largest tooth.
- **Hindmoor** (781, Antumbra, `:INVERSE`, 80x130): The moor that is only seen properly over your shoulder. Look straight at it and it is somewhere else. *Landmark:* Standing pools that show what is behind you. *Secret:* Walk it backwards and you find the cottage.
- **Downflame Road** (790, Antumbra, `:INVERSE`, 110x70): Lit by candles whose flames hang below the wick. Gravenmoor makes them. *Landmark:* The candle-posts and the lantern hospice on the hill. *Secret:* Blow one candle out and a door-shaped piece of dark stays lit.

**Road 15, The Slag Road** (Gravenmoor -> Cogsworth, Act IV). Out of Antumbra by the Barrows' east gate, over Ossaria's dry seabed to the crossroads, then borderland C' to the foundries.
- **The Noonless Road** (800, Antumbra, `:INVERSE`, 140x70): Antumbra has no noon. On this road your shadow never shortens. *Landmark:* Sundials with no shortest mark; the Barrow of the Wardens. *Secret:* A sundial that does work, for one minute.
- **The Dry Tide** (810, Ossaria, `:DESERT`, 140x72): An old seabed, rippled like a beach the sea left one evening and never came back to. *Landmark:* Shell pavements and a stranded ship's ribs. *Secret:* At night you can hear the tide. Follow it.
- **The Slag Mesa** (801, Borderland (Ossaria/Zenith), `:WASTELAND`, 80x130): Kept name: a mesa that is half rock and half what Cogsworth poured on it. *Landmark:* Slag falls, still warm. *Secret:* A cooled slag flow shaped round something large.
- **The Smokestack Parade** (811, Zenith, `:FACTORY`, 120x64): Cogsworth's ceremonial avenue: one chimney per founding patent. *Landmark:* The numbered stacks and three shift-clocks. *Secret:* Stack 9 has no furnace under it.

**Road 16, The Drowned Road** (Cogsworth -> Underveil, Act IV). Borderland L, the Hanging Stair: off the edge of Zenith and down the cliff to the drowned coast.
- **The Brink** (832, Zenith, `:STORMFRONT`, 130x60): Where Zenith stops. A promenade with a brass rail and a very long view. *Landmark:* The rail, the lift-heads, the telescopes. *Secret:* One telescope is fixed on a window in Underveil.
- **The Hanging Stair** (820, Borderland (Zenith/Nadir), `:SCRAPYARD`, 72x150): Kept name: scaffolds, cable lifts and outflow falls down the cliff beneath Zenith. *Landmark:* Cable lifts and shanty scaffolds. *Secret:* A lift cage that stops between floors on purpose.
- **The Drownings** (821, Borderland (Zenith/Nadir), `:WATER_SURFACE`, 120x120): Nadir's name for the coast that went under with Aurelia. *Landmark:* Tower-tops standing out of the sea. *Secret:* Dive below: Under the Drownings (822) and Aurelia.

**Road 17, The Blind Road** (Underveil -> Gloaming, Act V). Borderland F again, underground: the river that runs south beneath half the realm and surfaces in Elowen's twilight.
- **The Throat** (852, Nadir, `:NEW_MOON`, 64x110): The tunnel that swallows the river at Underveil. Boats go in. *Landmark:* The river mouth, in reverse. *Secret:* An air pocket with a smugglers' chapel.
- **The Blindwater** (840, Borderland (Nadir/Elowen), `:CAVE`, 150x80): The underground river. Nothing in it has eyes, and the boatmen sing so the walls know where they are. *Landmark:* Root-arches over black water and the lamps of Mothwell. *Secret:* A side channel that loops under Crownhaven.
- **The Gloamwood Verge** (841, Elowen, `:SILKWOOD`, 72x130): Kept name: the edge of the twilight wood, where the river comes back into the light. *Landmark:* The river's rising and the first lantern-flowers. *Secret:* A clearing that is always one hour later than the rest.

**Road 18, The Truce Road** (Gloaming -> Wyrmrest, Act V). Borderland J, the Thornwar Marches: twilight forest, burning forest, then the dragon ridge.
- **The Gloamwood** (860, Elowen, `:FAIRY_TALE`, 140x80): Kept name: Elowen's heart, where it has been dusk for three hundred years. *Landmark:* The Great Tree on the skyline and paths that move. *Secret:* A path that only exists while you are not on it.
- **The Thornwar Marches** (861, Borderland (Elowen/Ashkaar), `:MOUNTAIN`, 80x130): Kept name: where Elowen and Ashkaar fought the Thornwar. The trees still burn without dying. *Landmark:* Ember-leaved giants and Thornwar forts. *Secret:* A fort whose garrison never got the order to stand down.
- **The Wyrmspine** (872, Ashkaar, `:DRAGONS_DEN`, 150x72): The ridge road to Wyrmrest, along a spine of rock that Ashkaar says is exactly that. *Landmark:* The vertebral crags and the dragon roost-poles. *Secret:* A rib-cave with a clutch of eggs and a very calm mother.

**Road 19, The Pilgrim Road** (Wyrmrest -> Crownhaven, Act V). Borderland K: the only way overland into the Crown.
- **Dominar's Toll** (892, Ashkaar, `:MOUNTAIN`, 110x70): The Dominion taxes a holy road here, and has for three hundred years. *Landmark:* The toll-fort across the whole valley. *Secret:* The toll-keeper's ledger lists one pilgrim who has paid every year since AF 0.
- **The Pilgrim Pass** (880, Borderland (Ashkaar/Crownhaven), `:MOUNTAIN`, 80x140): Kept name: eighteen shrines, one per Plate, up the Crownwall. *Landmark:* The eighteen shrines. *Secret:* A nineteenth shrine, unfinished.
- **The Coronation Road** (893, Crownhaven, `:GRAND_STAGE`, 150x64): Walked once by each Sovereign, on foot, from the Ascent to the Eighteen Gates. *Landmark:* Statues of every Sovereign; the last plinth is empty. *Secret:* The empty plinth already has a name cut on the back.

### What the map builder rebuilds

Listed in `mapgen/REQUESTS.md` (cartographer entry): the Revision 14 relinks of the early maps, the new maps 527, 528, 552, 566, 577, 578, the growth of built maps to their target sizes, and the renamed names and signs in specs and layouts (already changed in the sources by `tools/rename_places.py`).

<!-- ROUTES:END -->
