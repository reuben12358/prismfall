# WORLD — Velmora region & level design (World lead)

Binding: `SPINE.md` (incl. **REVISION 2**). Machine-readable map list: **`design/maps.json`** (the Map Builder works from it).
Gym puzzles: `GYM_PUZZLES.md`. Species: `POKEMON_AVAILABILITY.md`. Wild data: `pbs/encounters.txt` (validated by `tools/validate_encounters.py`).
Names that the story team hasn't fixed yet are marked *(prov.)*.

---
## 1. Region layout: seven kingdoms around Crownhaven

```
                                   N
 +-----------------------------------------------------------------------------+
 | ~~ ISENMAR (frozen north coast) ~~ |        ZENITH (plateau, airship masts)   |
 |  [10 RIMEHOLT]==R21==R22==Cloudstair==[11 SKYREACH]   Stormwatch Spire       |
 |   Lake Rime  Stillwater*      |         |  R23 skybridges                    |
 |      | Frostfang Pass         |   [4 LUMEN CITY]===R9===+   [15 COGSWORTH]   |
 |     R20  (tundra edge)        |  /  Static Tunnels      |    R31  R32 drowned|
 |      |                    R8 /  ::::: NADIR (beneath Lumen) :::::  coast |
 | [3 EBBMOUTH]==R7==Sluiceworks   [8 IRONREACH]   [16 UNDERVEIL]~Aurelia       |
 |   |  Ebb Hollow*                  |  R16 Ironway   [6 MIREFEN]  R12   OSSARIA|
 |  R6 Gullcry Caves   R17 Lift Road |        \       |  R13       [5 DUNEHOLT]   |
 |   |                   |           |         \    R14 Lake Sallow  R11  R10    |
 |  R5 salt flats      R18 Prism Falls         \     |      [13 CRAGHOLM] R27  |
 | [2 SALTMERE]          |       +-------------+   [7 CINDERVAULT]  R26 Geode   |
 |   |  R4 Brinecut Mine |       | CROWNHAVEN  |   R15  Mt. Cinder               |
 |  R3 Thistledown Mnr.  |       |  (neutral)  |==R36== ASHKAAR          |
 |   |                [9 VERDANCE] +---R37------+   [18 WYRMREST] Wyrmscar Rift  |
 | [1 BRIARWICK]  R19 ->R20  Royal Chase   [17 GLOAMING] R35 Gloamwood            |
 |   | Gossamer Wood        ELOWEN   R34 Gloamwood Verge <- R33 (river)    |
 |  R2 -- R1     Mirror Mere ==> (gate to ANTUMBRA)                                |
 | [0 FERROW'S LANDING] ~~~~~~~~~~~~~~~ Hallow Strait (south) ~~~~~~~~~~~~~~~~~~ |
 +-----------------------------------------------------------------------------+
  ANTUMBRA, the Reverse Kingdom (behind the Elowen forest, entered through mirror gates):
    Mirror Mere -> Antumbra Threshold -> [12 LUCENT] -> R25 (exits via a mirror into the Ossaria, R26)
    Grave Glass (R27) -> R28 fog moors -> [14 GRAVENMOOR] -> R29 barrows -> R30 (exits into Lumen's wasteland)
  * = Bleed zone.   ==  = road/edge link.   ~ = sea.
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
| 900–949 | postgame (Hallow Strait, Shardfall Isles, Antumbra Distortion Core) |
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
| 2 | I | Saltmere → Ebbmouth (G3 23) | R5 560 (salt flats), R6 561, Gullcry Caves 564/565 CAVE, **The Rehearsal 568** BLEED; K2 on R6 | 14–21 |
| 3 | I | Ebbmouth → Lumen City (G4 27) | R7 580, R8 581, Voltaic Sluiceworks 584/585 SCRAPYARD (Rotom), **Ebb Hollow 588** BLEED | 18–25 |
| 4 | II | Lumen → Duneholt (G5 31) | R9 600, R10 601 DESERT, Static Tunnels 604/605 CAVE (Flash), **The Lowlight (Shattered) 608** BLEED (story) | 22–29 |
| 5 | II | Duneholt → Mirefen (G6 35) | R11 620 DESERT, R12 621, Ossuary of Dunes 624/625 CAVE (Strength, Unown ruins), **Sinkfield 628** | 26–33 |
| 6 | II | Mirefen → Cindervault (G7 39) | R13 640, R14 Lake Sallow 641 (Surf), Miasma Caverns 644/645 CORROSIVE_MIRE, **Weeping Fen 648**, Lantern Isle 658 BEACH (opt.) | 30–37 |
| 7 | II | Cindervault → Ironreach (G8 43) | R15 660 ASHEN_WASTE, R16 Ironway 661 MOUNTAIN, Mt. Cinder 664–666 VOLCANIC, **Ashkaarfall 668** | 34–41 |
| 8 | III | Ironreach → Verdance (G9 47) | R17 Lift Road 680, R18 Prism Falls 681 RAINBOW, **Royal Chase 682** (Safari-style reserve), Grudgestone Quarry 684/685 CAVE, **Echo Coliseum 688** | 38–45 |
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
**Route 5 (560)**, 64×28 salt flats (Sand terrain), Elowen/Isenmar borderland. A wrecked pier village S is **The Rehearsal (568)**.
**Route 6 (561)**, 30×60 sea cliffs N to Ebbmouth, light rain. A landslide at y28–32 forces a detour through **Gullcry Caves (564)**, which has two mouths on the W cliff. K2 waits at the N end.
```
 R6:  N exit (Ebbmouth)        Gullcry 1F
        K2 ●                   +-------------+
        |  <-------mouth N-----| tide pools  |
      ######## landslide ##     |      v B1F  |
        |  <-------mouth S-----|             |
        |                      +-------------+
      E edge -> Route 5
```
**Ebbmouth (160)**, 46×42, Isenmar's warm southern port. The River Ebb runs through it (x30–35), and its **current tiles flip with day/night** (two event pages), which is the Imprint's signature. Canals and stilt houses. The Tidelock Gym is the lock-house on the river (E). The Reyes House cellar (166) holds the Hollow cell. The Anglers' Guild gives the Good Rod after B3.
**Route 7 (580)**, 52×42 delta reed-beds: a mesh of still-water channels crossed by boardwalks, rain. The NW dam leads to the **Voltaic Sluiceworks (584/585**, optional, static Rotom Lv25). The W bank leads to **Ebb Hollow (588)**.
**Route 8 (581)**, 32×52 switchbacks up the Lumen escarpment, Isenmar/Zenith borderland. The fenced Meridian Extraction Lattice #4 is a story landmark. Lumen South Gate (582) is at the top.
**Lumen City (180 Concourse 64×52, 181 Lowlight 40×30)**. A white-stone grid with a central Prism fountain plaza, Meridian Tower to the E (185/186, Act I gala and Shatter), the Circuit Gym to the W, and the Dept. Store (183/184) and Fossil Lab (188) to the S. The Lowlight district steps down to the SE. After the Shatter (end of Act I), a story switch swaps 181 for the Bleed map **608**. The Static Tunnels entrance (Act II, needs Flash) is at the NE rail tunnel.
