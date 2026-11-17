# WORLD — Velmora region & level design (World lead)

Binding: `SPINE.md` (incl. **REVISION 2**). Machine-readable map list: **`design/maps.json`** (the Map Builder works from it).
Gym puzzles: `GYM_PUZZLES.md`. Species: `POKEMON_AVAILABILITY.md`. Wild data: `pbs/encounters.txt` (validated by `tools/validate_encounters.py`).
Names that the story team hasn't fixed yet are marked *(prov.)*.

---
## 1. Region layout: seven kingdoms around Crownhaven

```
 Schematic, not to scale. Kingdoms touch ONLY through the borderlands in [brackets]; adjacency is authoritative in §10.
                                            N
 ~~~~~~~~~~~~~~~~~~~~~ FROZEN NORTH SEA (Isenmar waters) ~~~~~~~~~~~~~~~~~~~~~~~~  RIME ISLES (Isenmar): Skaldfast
  (10)Rimeholt  ~~~~~~~~~~~ sled-road along the north coast ~~~~~~~~~~~~~~~~~~~~~~~  ~~ SHATTERED ICE strait ~~
     |  \[B2 Mast Glacier: Anchorhold]--(11)Skyreach      (16)Underveil (Nadir, N coast)      Cinder Cape (Ashkaar)
 [A2 N.Rimewood:                          |  ZENITH       [L Hanging Stair: Midstair]               |
   Snowbriar]          (4)LUMEN CITY ---- [C Brass Dunes: Copperdune] ---- (5)Duneholt       [M Cinderglass Barrens:
     |       [B Icefall Locks:   |   (15)Cogsworth --[C' Slag Mesa]--+     OSSARIA            Glasswake]
  ISENMAR      Brassfall]        |   NADIR beneath: (8)Ironreach      |  [D Leach Canyons:      |
 (3)Ebbmouth ---+                |       (6)Mirefen -- Charwell] ------+   (13)Cragholm    ASHKAAR
     |          [G Wired Wood:   |           \[E Sulfur Reach: Scaldwater]-----------(7)Cindervault
 [A Rimewood:    Verdigris]  [F Rootdeep: Lanternroot / Mothwell]  [I Obsidian Barrows: Vigil] |
  Frostwick]          |          |                    ((ANTUMBRA)) (12)Lucent (14)Gravenmoor    |
 (2)Saltmere   ELOWEN  [H Looking-Glass Wood: Glassmere] ((gate))      ( CROWNHAVEN )  (18)Wyrmrest
     |   (9)Verdance              (17)Gloaming --[J Thornwar Marches: Thornwatch]--+   [K Pilgrim Pass:
 (1)Briarwick                                                                          Pilgrim's Rest]
 (0)Ferrow's Landing ~~~~~~~~~~~~~~~~~~~~~~~~~ Hallow Strait (south) ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 ANTUMBRA (mirror realm) has two stable gates: Mirror Mere (Elowen, border H) and the Grave Glass (Ossaria, border I).
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
| **100 + 20·c** (c = 0 Ferrow's Landing, 1 Briarwick … 18 Wyrmrest) | city block: +0 exterior, +1 Pokémon Center, +2 Mart, +3..+9 houses/landmarks, **+10..+19 gym rooms** (+10 entrance … last = Warden arena) |
| 480–519 | Crownhaven (+10..+19 Festival Arena, Battle Tower) |
| **520 + 20·s** (s = badges held, 0–18) | overworld segment s, the land between gym s and gym s+1: +0..+3 routes, +4..+7 dungeons, **+8..+9 Bleed zone**, +10..+17 rest houses/gates, +18..+19 optional |
| 900–919, 940–949 | postgame (Hallow Strait, Shardfall Isles, Antumbra Distortion Core) |
| 920–939 | Ashkaar–Isenmar war theatre (§9) |
| 950–959 | overflow for big-city districts |
| 960–979 | **Ruin Route only** maps |
| 980–989 | interludes (playable as other characters) · 990–999 dev/test |
| segment +18/+19 | also used for **branch-only** maps (e.g. 698 Hollow Sanctuary, 699 Meridian Black Site, 838 Accord Archive) |

So the map ID tells you the badge count (and therefore the level cap): the validator relies on this. Revisit areas that open later (e.g. Gossamer Heartwood, Ebbmouth Sea Grotto) take IDs in the segment where they open, not in their kingdom's first block.

---
## 3. Progression (segment table)

Wild level band ≈ previous cap −3 … next cap −2. Field = default battle field (`FieldEffects::MAP_FIELDS`). `—` = :NONE.

| s | Act | From → to | Maps (ID) and field | Wild Lv |
|---|---|---|---|---|
| 0 | I | Ferrow's → Briarwick (G1 cap 15) | R1 520, R2 521, **Glassed Orchard 522** BLEED (story), Gossamer Wood 524 SILKWOOD | 3–12 |
| 1 | I | Briarwick → Saltmere (G2 19) | Gossamer Deepwood 525 SILKWOOD (Cut), R3 540, R4 541 BEACH, Brinecut Mine 544/545 CAVE, Thistledown Manor 546/547 (haunted house), **Cocoonfall Hollow 548** BLEED | 10–17 |
| 2 | I | Saltmere → Ebbmouth (G3 23) | **Borderland A (the Rimewood):** R5 Frostflat Causeway 560, **Frostwick 570** (+571–576), The Rimewood 562, Rimewood Glade 563 (Cut). Then Isenmar: R6 Gullcry Cliffs 561, Gullcry Caves 564/565 CAVE, **The Rehearsal 568** BLEED (off R5); K2 on R6 | 14–21 |
| 3 | I | Ebbmouth → Lumen City (G4 27) | R7 580, R8 581, Voltaic Sluiceworks 584/585 SCRAPYARD (Rotom), **Ebb Hollow 588** BLEED | 18–25 |
| 4 | II | Lumen → Duneholt (G5 31) | R9 600, R10 601 DESERT, Static Tunnels 604/605 CAVE (Flash), **The Lowlight (Shattered) 608** BLEED (story) | 22–29 |
| 5 | II | Duneholt → Mirefen (G6 35) | R11 620 DESERT, R12 621, Ossuary of Dunes 624/625 CAVE (Strength, Unown ruins), **Sinkfield 628** | 26–33 |
| 6 | II | Mirefen → Cindervault (G7 39) | R13 640, R14 Lake Sallow 641 (Surf), Miasma Caverns 644/645 CORROSIVE_MIRE, **Weeping Fen 648**, Lantern Isle 658 BEACH (opt.) | 30–37 |
| 7 | II | Cindervault → Ironreach (G8 43) | R15 660 ASHEN_WASTE, R16 Ironway 661 MOUNTAIN, Mt. Cinder 664–666 VOLCANIC, **Emberfall 668**; optional/war road: **Cinderglass Barrens 662**, Petrified Ashwood 663, **Glasswake 670** (border M) | 34–41 |
| 8 | III | Ironreach → Verdance (G9 47) | R17 The Rootdeep 680 CAVE + **Lanternroot 690** (border F), R18 Prism Falls 681 RAINBOW, **Royal Chase 682** (Safari-style reserve), Grudgestone Quarry 684/685 CAVE, **Echo Coliseum 688** | 38–45 |
| 9 | III | Verdance → Rimeholt (G10 51) | R19 700, R20 701 SNOWY_MOUNTAIN, Gossamer Heartwood 703 SILKWOOD (revisit), Frostfang Pass 704/705 SNOWY_MOUNTAIN, **Bride Grove 708** (story) | 42–49 |
| 10 | III | Rimeholt → Skyreach (G11 55) | R21 720, R22 721 SNOWY_MOUNTAIN, Ebbmouth Sea Grotto 723 (revisit), Cloudstair 724–726 MOUNTAIN (Rock Climb), **Stillwater 728** | 46–53 |
| 11 | III | Skyreach → Lucent (G12 59) | R23 740 STORMFRONT, R24 741, Mirror Mere 742, **Antumbra Threshold 743 INVERSE**, Stormwatch Spire 744–746 STORMFRONT, **Shattered Sky 748** | 50–57 |
| 12 | IV | Lucent → Cragholm (G13 63) | R25 760 INVERSE (Antumbra), R26 761 (Waterfall), Geode Hollow 764/765 CRYSTAL_CAVERN, **Dreaming Quarter 768** | 54–61 |
| 13 | IV | Cragholm → Gravenmoor (G14 67) | R27 780 MOUNTAIN, R28 781 (Antumbra moors), Duneholt Undersands 783 DESERT (revisit, Groudon arc), Darkglass Mine 784/785 DARK_CRYSTAL, **Stonesleep 788** (fossils) | 58–65 |
| 14 | IV | Gravenmoor → Cogsworth (G15 71) | R29 800, R30 801 WASTELAND, Barrow of the Wardens 804/805 (CAVE/HOLLOW_CATHEDRAL), Giratina's Reverse Depths 806 INVERSE, **The Hush 808** | 62–69 |
| 15 | IV | Cogsworth → Underveil (G16 75) | R31 820 SCRAPYARD, R32 821 WATER_SURFACE, R32 Seabed 822 UNDERWATER (Dive), **Aurelia** 824 UNDERWATER / 825–826 CAVE, **Ironbloom 828** | 66–73 |
| 16 | V | Underveil → Gloaming (G17 80) | R33 840 CAVE, R34 Gloamwood Verge 841, Lightless Deep 844 DARK_CRYSTAL / 845 NEW_MOON (Pecharunt arc), **Inverted Ward 848 INVERSE** | 70–78 |
| 17 | V | Gloaming → Wyrmrest (G18 85) | R35 Gloamwood 860 FAIRY_TALE, R36 861 MOUNTAIN, Wyrmscar Rift 864 CAVE / 865 DRAGONS_DEN (Reshiram arc), **Rainbow Scar 868 RAINBOW** | 75–83 |
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
| Headbutt | tutor (R2 farmhouse) | Act I start | none (no gate in v21) | optional trees |
| Cut | HM01 | Briarwick Cutter's House (B1) | `BADGE_FOR_CUT = 1` | Gossamer Deepwood |
| Rock Smash | TM98 | Brinecut miner (B2) | `BADGE_FOR_ROCKSMASH = 2` | optional rocks R4/Brinecut |
| Flash | TM70 | Rook Calder (B4) | `BADGE_FOR_FLASH = 4` | Static Tunnels (dark) |
| Strength | HM04 | Duneholt excavators (B5) | `BADGE_FOR_STRENGTH = 5` | Ossuary of Dunes |
| Surf | HM03 | Mirefen ferrymen (B6) | `BADGE_FOR_SURF = 6` | R14 Lake Sallow |
| Fly | HM02 | Skyreach courier at the Ironreach Conclave (B8) | `BADGE_FOR_FLY = 8` | Act III criss-crossing |
| Rock Climb | TM100 | Rimeholt ice-climbers (B10) | **no v21 constant/handler**: Core must add `Prismfall::BADGE_FOR_ROCKCLIMB = 10` + a cliff-event helper | Cloudstair |
| Waterfall | HM05 | Skyreach sky-river guides (B11) | `BADGE_FOR_WATERFALL = 11` | R26 |
| Dive | HM06 | Cogsworth bathysphere works (B15) | `BADGE_FOR_DIVE = 15` | R32 Seabed / Aurelia |

Rods: Old Rod at Ferrow's Landing (start), Good Rod at Ebbmouth Anglers' Guild (B3), Super Rod from the Rimeholt ice-fisher (B10). The validator enforces these unlocks: a Water table on an early map is capped at the Surf-era cap, and so on.

## 5. Bleed zones and the Unimprinted protagonist
- Every Bleed zone sits behind a **Bleed Veil**, a shimmer-tile event at its entrance. NPCs and partners stop at it ("my skin's burning, I can't"). The PC walks through alone. This is the gameplay proof of being Unimprinted, taught in the Glassed Orchard (s0, mandatory).
- Inside: field `:BLEED` (except Inverted Ward = `:INVERSE`, Rainbow Scar = `:RAINBOW`), Land encounter rate 25, **Imprinted variants** (regional forms) appear only here and near their Imprint, no Fly out (Escape Rope works), screen tint + Lullaby BGM.
- Each zone holds one **Bleed Shard** (*prov.* key item `BLEEDSHARD`, 19 total). Larch trades rewards for them (Ability Capsule, Bottle-Cap-style IV items, the Legend-Plate lore).
- Mandatory zones: Glassed Orchard (s0), The Lowlight (s4), Bride Grove (s9), Glassfall Scar (s18). The rest are optional, but they hold the best items and TMs.

## 6. Key items / TM highlights
Gym TMs: 1 U-turn TM89 · 2 Facade TM42 · 3 Water Pulse TM03 · 4 Volt Switch TM43 · 5 Bulldoze TM83 · 6 Poison Jab TM84 · 7 Flamethrower TM35 · 8 Brick Break TM31 · 9 Energy Ball TM53 · 10 Ice Beam TM13 · 11 Roost TM51 · 12 Psychic TM29 · 13 Stealth Rock TM76 · 14 Shadow Ball TM30 · 15 Flash Cannon TM91 · 16 Dark Pulse TM79 · 17 Dazzling Gleam TM21 · 18 Dragon Pulse TM59.
Field TMs: Giga Drain TM19 (Gossamer Wood), X-Scissor TM81 (Cocoonfall), Work Up TM10 (Rehearsal), Brine TM55 (Gullcry B1F), Scald TM49 (Ebb Hollow), Thunderbolt TM24 (Lowlight), Earthquake TM26 (Mt. Cinder Caldera), Drain Punch TM60 (Grudgestone), Calm Mind TM04 (Dreaming Quarter), Will-O-Wisp TM61 (The Hush), Trick Room TM92 (Inverted Ward), Dragon Claw TM02 (Wyrmscar Rift), Hyper Beam TM15 (Crownhaven).
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
| 0→1→2 | Ferrow's → Briarwick → Saltmere | inside Elowen |
| 2→3 | Saltmere → Ebbmouth | **A** Rimewood (south): R5, Frostwick, Rimewood |
| 3→4 | Ebbmouth → Lumen | **B** Icefall Locks: R8, Brassfall, Sluiceworks |
| 4→5 | Lumen → Duneholt | **C** Brass Dunes: R9, Copperdune |
| 5→6 | Duneholt → Mirefen | **D** Leach Canyons: R12, Charwell |
| 6→7 | Mirefen → Cindervault | **E** Sulfur Reach: R14 Lake Sallow, Scaldwater |
| 7→8 | Cindervault → Ironreach | **E** again via the Ironway, R16 |
| 8→9 | Ironreach → Verdance | **F** Rootdeep: R17, Lanternroot |
| 9→10 | Verdance → Rimeholt | **A2** northern Rimewood: R20, Snowbriar |
| 10→11 | Rimeholt → Skyreach | **B2** Mast Glacier: R22, Anchorhold, Cloudstair |
| 11→12 | Skyreach → Lucent | **G** Wired Wood (R24, Verdigris), then **H** Mirror Mere (Glassmere) → Antumbra Threshold |
| 12→13 | Lucent → Cragholm | **I** Obsidian Barrows: R25, Vigil |
| 13→14 | Cragholm → Gravenmoor | **I** again: Vigil's Grave Glass → R28 |
| 14→15 | Gravenmoor → Cogsworth | **I** (R29's east gate) then **C'** Slag Mesa R30 |
| 15→16 | Cogsworth → Underveil | **L** Hanging Stair: R31, Midstair, R32 |
| 16→17 | Underveil → Gloaming | **F** again (south): R33 Rootdeep River, Mothwell |
| 17→18 | Gloaming → Wyrmrest | **J** Thornwar Marches: R36, Thornwatch |
| 18→Festival | Wyrmrest → Crownhaven | **K** Pilgrim Pass: R37, Pilgrim's Rest |
| war arc | Cindervault → Cinder Cape | **M** Cinderglass Barrens 662/663, Glasswake (the war itself is across the sea) |

| Code | Borderland | Biome blend and signature landmarks | Wild mix | Town (ID): trade · culture mix · tension · sidequest |
|---|---|---|---|---|
| A | **The Rimewood** (Elowen/Isenmar) | Oldwood frozen in hoar: ice-glazed giant trees, frozen Gossamer silk curtains, salt flats turning to frost-flats. Border Stones, Frost Loom, Silk-fall | Snover, Snom, Cubchoo, Swinub, Bergmite, Vanillite, Deerling, Stantler, Teddiursa, Smoochum, Delibird | **Frostwick 570**: rime-silk, honey and silk for furs, eel and whale oil · Elowen treehouses above Isenmar longhouses · Meridian survey pegs and the sunburst stamped over both seals · "The Two Hearths" |
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

**Ferrow's Landing (100)**, 40×32, Outside. South coast ferry village, Elowen.
```
 TTTTTTTTTTTTTTTTT[N exit to R1]TTTTTTTTT
 T        +--LAB(103)--+                T
 T  PC    |  Larch     |      MART      T
 T (101)  +------------+     (102)      T
 T   ...cobbled main street x18-21...   T
 T INN(104)  CUSTOMS(108)  DOCK(107)  LIGHTHOUSE(105)
 ~~~~~~~~~~~~~~~~|pier|~~~~~~~~~~~~~~~~~~
 ~~~~~~~~~~~~~~~~|BERTH (Dovetail)|~~~~~~
```
Prologue: 110 cabin → 109 deck (Voss) → berth (19,28) → Customs (NULL scan) → Lab (starter) → Lighthouse (Kestrel, K1).

**Route 1 (520)**, 26×48 coastal heath going N. One-way ledge row at y24 (a shortcut home). Juno's catching tutorial at the south end. 2 trainers.
**Route 2 (521)**, 60×26 E–W orchards. Hale Farmhouse (523, Headbutt tutor). In the NE corner is a quarantine cordon around the **Glassed Orchard (522)**, the first Bleed Veil scene. The W edge leads into Gossamer Wood.
```
 R2:  [Wood]<==== hedgerow fields ==== FARM ==== orchard trees ==== [cordon|Glassed Orchard]
                                                     ||
                                                  (R1 below)
```
**Gossamer Wood (524)**, 48×48, SILKWOOD. Silk-web walls (decor events) make a trail S→N with two side loops. Woodward's Hut (526) sits in the central clearing. A Cut tree on the E edge leads to **Deepwood (525)**, an optional pond area you return to after Badge 1.
**Briarwick (120)**, 44×40. Six hollow giant trees joined by rope bridges, with the Loomhouse Gym (the biggest tree) at the north. W edge → Route 3. The Cutter's House gives HM01.
**Route 3 (540)**, 64×28 river meadows. River along the south third with a stone bridge. On the N hill is Thistledown Manor (546/547, optional haunted house: furniture that moves, a portrait-order puzzle, Greavard in the attic). In a NW copse is **Cocoonfall Hollow (548)**. The NE cave mouth is the Brinecut Mine shortcut exit.
**Route 4 (541)**, 30×52 S-bound salt marsh to shingle beach (BEACH). Boardwalks over still-water pools. The Brinecut Mine (544) mouth is in the E chalk cliff.
**Saltmere (140)**, 48×40, the Elowen free port. Market square, with the Pell Playhouse (Gym) on its N side, the harbour to the S, and the Pageant Hall (Mourner hijack) to the E. J1 happens in the square. The Eevee gift is here after B2.
**Route 5, Frostflat Causeway (560)**, 64×30. Borderland A starts here. A raised salt road runs W from Saltmere. The crust turns from salt (E) to frost (W), and the first Ice slide tiles appear. The Border Stones carry both kingdoms' arms with a Meridian sunburst bolted across them. A S spur leads to **The Rehearsal (568)**. W edge → Frostwick.
**Frostwick (570)**, 44×40, the borderland village. Elowen treehouses sit in ice-glazed giant trees above Isenmar turf-and-whalebone longhouses. The frozen Hoar Brook (with ice-fishing holes) crosses the square, the Hearth Stone stands in it, and the E gate is a whale-rib palisade wrapped in briar. Buildings: PC 571, The Exchange 572 (mart + barter), The Two Hearths inn 573 (sidequest), Rime-silk Loft 574, Border House 575 (customs: forester, huscarl and a Meridian clerk), Halvard's Smokehouse 576. N edge → the Rimewood.
**The Rimewood (562)**, 48×56. Oldwood frozen in hoar: ice-glazed giant boles and frozen-silk curtains make the walls. Features: a frozen-brook slide shortcut, a fallen giant-tree bridge, the trapper's lean-to (heal), the Frost Loom, and an aurora clearing. 5 trainers. The E Cut sapling leads to **Rimewood Glade (563)** (the Silk-fall, a pond slide puzzle for Never-Melt Ice, the Snowveil Shrine). N edge → Route 6.
**Route 6, Gullcry Cliffs (561)**, 30×60, the first true Isenmar ground: whalebone waymarkers, a cod-skull cairn, stilt fishing huts. A landslide at y28–32 forces the detour through **Gullcry Caves (564)**. K2 waits at the N end, and the N edge leads to Ebbmouth.
```
 140 Saltmere --W--> 560 Route 5 --W--> 570 FROSTWICK --N--> 562 Rimewood --N--> 561 Route 6 --N--> 160 Ebbmouth
                       | S spur                                 | E (Cut)            | W cliff mouths
                      568 Rehearsal                            563 Glade          564 Gullcry 1F -- 565 B1F
```

**Ebbmouth (160)**, 46×42, Isenmar's warm southern port. The River Ebb runs through it (x30–35), and its **current tiles flip with day/night** (two event pages), which is the Imprint's signature. Canals and stilt houses. The Tidelock Gym is the lock-house on the river (E). The Reyes House cellar (166) holds the Hollow cell. The Anglers' Guild gives the Good Rod after B3.
**Route 7 (580)**, 52×42 delta reed-beds: a mesh of still-water channels crossed by boardwalks, rain. The NW dam leads to the **Voltaic Sluiceworks (584/585**, optional, static Rotom Lv25). The W bank leads to **Ebb Hollow (588)**.
**Route 8, Icefall Locks (581)**, 32×52 switchbacks up the frozen falls of the Lumen escarpment (borderland B; town Brassfall 590). The fenced Meridian Extraction Lattice #4 is a story landmark. Lumen South Gate (582) is at the top.
**Lumen City (180 Concourse 64×52, 181 Lowlight 40×30)**. A white-stone grid with a central Prism fountain plaza, Meridian Spire in its own Spire District (195; interiors 185/186, Act I gala and Shatter), the Circuit Gym to the W, and the Dept. Store (183/184) and Fossil Lab (188) to the S. The Lowlight district steps down to the SE. After the Shatter (end of Act I), a story switch swaps 181 for the Bleed map **608**. The Static Tunnels entrance (Act II, needs Flash) is at the NE rail tunnel.
