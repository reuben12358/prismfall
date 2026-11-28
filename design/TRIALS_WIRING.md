# TRIALS_WIRING - which Trial quests and event Pokemon are really on the maps

> **Generated** by `python3 -I tools/trials_wiring.py` from the plugin data (`ruby tools/trials_docs.rb --json`), `design/TRIAL_EVENTS.yaml`, the built maps (`maps_out/Data`), the map specs (`mapgen/specs`) and `mapgen/trial_overlay.py`. Re-run it after a map build.
> **Status:** *in maps* = every map event the quest needs is in a built map; *next build* = the events are in the specs or `trial_overlay.py` and the next `build.py` run lays them; *needs maps* = a map it needs is not built yet (its events are in `mapgen/REQUESTS.md`); *designed* = a `:stub`, no scenes yet. *not placed* = its map is built or specced but no event calls it. **Tier** = the badges its unlock needs. Maps: *built* / *spec* (spec, not built) / *planned* (maps.json only).

## Chapters 0-5 at a glance

| Ch | Quests | Designed only | In maps (before) | In maps now | Next build | Needs maps |
|---|---|---|---|---|---|---|
| 0 | 1 | 0 | 0 | 1 | 0 | 0 |
| 1 | 5 | 0 | 5 | 5 | 0 | 0 |
| 2 | 9 | 0 | 5 | 8 | 0 | 1 |
| 3 | 6 | 0 | 3 | 6 | 0 | 0 |
| 4 | 9 | 0 | 7 | 9 | 0 | 0 |
| 5 | 6 | 1 | 1 | 5 | 0 | 0 |

## Every quest

| Quest | Trial | Ch | Tier | Maps | Keys | Before | Now | Notes |
|---|---|---|---|---|---|---|---|---|
| **Two Unlisted** `EL_STOWAWAYS` | Elowen | 0 | 0 | 100 built, 108 built, 109 built | `CRATE_WOMAN` `STOWAWAY_MICE` | new | in maps |  |
| **The First Lesson** `EL_FIRST_LESSON` | Elowen | 1 | 0 | 100 built | `DEED_KELP` `DEED_ROPE` `DEED_SAILOR` `DEED_WASHING` `TEASEL` | in maps | in maps |  |
| **Master of Nothing** `EL_MASTER_OF_NOTHING` | Elowen | 1 | 0 | 107 built, 109 built, 160 built | `DOCKMASTER` `DOVETAIL_NEST` `EBB_MAST` | in maps | in maps |  |
| **The Scarecrow Walks** `EL_SCARECROW` | Elowen | 1 | 0 | 100 built, 521 built, 523 built | `COLL` `SCARECROW` `WENNA` | in maps | in maps |  |
| **The Tart Thief** `EL_TART_THIEF` | Elowen | 1 | 0 | 100 built, 103 built | `LOFT_NICKIT` `NICKIT_SIGHTING` `TART_STALL` `WENNA` | in maps | in maps |  |
| **Form 7-B** `ZE_FORM_7B` | Zenith | 1 | 0 | 103 built, 106 built, 107 built, 108 built | `CUSTOMS_OFFICER` `DOCKMASTER` `HESPER` `KIOSK_PENNY` `LARCH` | in maps | in maps |  |
| **The Eevee Octave** `CR_OCTAVE` | Crownhaven | 2 | 0 | 145 built, 340 planned, 489 planned | `VESPER_GARDEN` `VESPER_LUCENT` `VESPER_SALTMERE` | partly | partly, needs maps | waits on map 340, 489 |
| **The Orchard Sings** `EL_GLASS_FOAL` | Elowen | 2 | 1 | 100 built, 522 built | `GLASS_FOAL` `ORCHARD_HOOFPRINT` `TEASEL` | in maps | in maps |  |
| **The Borrowed Lanterns** `EL_LANTERNS` | Elowen | 2 | 0 | 140 built, 145 built, 146 built, 147 built, 148 built | `BOAT_LANTERN` `CARAMEL_SELLER` `HOLLIN` `PROP_LANTERN` `ROPEWALK_LANTERN` `STAGEHAND` | in maps | in maps |  |
| **The Last Plank** `EL_LAST_PLANK` | Elowen | 2 | 1 | 100 built | `BERTH_TIMBURR` `BOATYARD_PLANK` | not in maps | in maps |  |
| **A Hole in the Sky** `EL_PAINT_LOFT` | Elowen | 2 | 1 | 145 built | `FANE` | in maps | in maps |  |
| **The Crown in the Sand** `EL_SAND_CROWN` | Elowen | 2 | 1 | 528 built | `SAND_CROWN` `SCULPTOR` | new | in maps |  |
| **The Sound of Saltmere** `EL_SOUND_OF_SALTMERE` | Elowen | 2 | 1 | 140 built, 145 built, 146 built, 147 built, 148 built | `BREAKWATER_END` `CARAMEL_SELLER` `HOLLIN` `SILENCE_ROPEWALK` `SILENCE_STAGE` | in maps | in maps |  |
| **The Tide-Pool Feud** `EL_TIDE_POOL_FEUD` | Elowen | 2 | 1 | 527 built | `DOBBS` `TIDE_POOL` | partly | in maps |  |
| **Field Survey: Coastal** `ZE_FIELD_SURVEY` | Zenith | 2 | 0 | 108 built, 143 built, 160 built | `KIOSK_PENNY` `KIOSK_PENNY_EBB` `KIOSK_PENNY_SALTMERE` | in maps | in maps |  |
| **The Horn and the Pincer** `EL_HORN_AND_PINCER` | Elowen | 3 | 2 | 524 built | `SAP_TREE` | in maps | in maps |  |
| **The Note Under the Glass** `EL_MATRIARCH_HUM` | Elowen | 3 | 0 | 126 built, 548 built | `ALDRETH` `GLASS_COCOON` | new | in maps |  |
| **The Moss Hymn** `EL_OCTAVE_MOSS` | Elowen | 3 | 1 | 120 built, 524 built | `MOSS_STONE` `OCTAVE_LYRA` | not in maps | in maps |  |
| **Someone Apologising to Bugs** `EL_SHELLY` | Elowen | 3 | 2 | 120 built, 126 built | `ALDRETH` | designed | in maps |  |
| **The Silkthief** `EL_SILKTHIEF` | Elowen | 3 | 2 | 123 built, 525 built | `HETT` `MOTH_NESTS` | in maps | in maps |  |
| **Three Loyal, Three Knots** `EL_THREE_KNOTS` | Elowen | 3 | 1 | 120 built, 126 built, 524 built, 552 built | `ALDRETH` `SHRINE_FORD` `SHRINE_SQUARE` `SHRINE_WOOD` | in maps | in maps |  |
| **The Little Crucible** `AS_LITTLE_CRUCIBLE` | Ashkaar | 4 | 2 | 146 built | `BRAKKA` | in maps | in maps |  |
| **Bracken Comes In** `EL_DROVERS_BELL` | Elowen | 4 | 2 | 579 built | `DROVER` `WOLF_DEN` | new | in maps |  |
| **The Rehearsal** `EL_REHEARSAL` | Elowen | 4 | 2 | 568 built, 573 built | `MAELON` `REHEARSAL_GIRL` `REHEARSAL_LOOP` | in maps | in maps |  |
| **The Egg Thief of Gullcry** `IS_EGG_THIEF` | Isenmar | 4 | 3 | 561 built | `ASTA` `EGG_LEDGE` | in maps | in maps |  |
| **The Oathbound Parcel** `IS_OATH_PARCEL` | Isenmar | 4 | 2 | 168 built, 561 built, 573 built | `BERSI` `INGRITH` `PARCEL_RATTLE` | in maps | in maps |  |
| **The Drowned Note** `IS_OCTAVE_DROWNED_NOTE` | Isenmar | 4 | 2 | 160 built, 167 built | `EBB_NOTE` `MILL_WHEEL` `OCTAVE_ARIA` | partly | in maps |  |
| **A Deed for the Skald** `IS_SKALDS_SAGA` | Isenmar | 4 | 2 | 160 built, 168 built | `BERSI` `GORM` | in maps | in maps |  |
| **Two Hearths, One Pot** `IS_TWO_HEARTHS` | Isenmar | 4 | 2 | 562 built, 573 built, 576 built | `BRENNA_SIGVALD` `HALVARD` `RIMEWOOD_HIVE` | in maps | in maps |  |
| **The Lattice Hums Wrong** `ZE_LATTICE_HUM` | Zenith | 4 | 2 | 160 built, 167 built | `KIOSK_PENNY_EBB` `WHEEL_GUILD` `WHEEL_QUAY` `WHEEL_UPPER` | in maps | in maps |  |
| **The Humming Lamp** `EL_LAMP_LENS` | Elowen | 5 | 3 | 106 built | `HESPER` | in maps | in maps |  |
| **The Names in Holmsby** `IS_EBB_HOLLOW` | Isenmar | 5 | 3 | 580 built, 588 built | `HOLLOW_CORAL` `HOLLOW_STONE` `VEIL_FISHER` | needs maps | in maps |  |
| **Customer Support** `ZE_CUSTOMER_SUPPORT` | Zenith | 5 | 3 | 185 built | `DESK_APPROVALS` `DESK_COMPLIANCE` `DESK_RECORDS` `HELPDESK_ROTOM` | needs maps | in maps |  |
| **The Machine Wants Compliments** `ZE_FIZZBOLT` | Zenith | 5 | 3 | 180 built | `FIZZBOLT_MACHINE` | needs maps | in maps |  |
| **Off the Beat** `ZE_OCTAVE_OFF_BEAT` | Zenith | 5 | 3 | 180 built, 181 built | `LATTICE_JUNCTION` `OCTAVE_CADENCE` | needs maps | in maps |  |
| **Product Recall** `ZE_ROTOM_RECALL` | Zenith | 5 | 3 | 183 built |  | designed | designed |  |
| **Kevin** `OS_KEVIN` | Ossaria | 6 | 4 | 209 built |  | designed | designed |  |
| **The Noon Bell** `OS_OCTAVE_NOON_BELL` | Ossaria | 6 | 4 | 606 built | `OCTAVE_SONA` `SUN_DRIFT` | needs maps | in maps |  |
| **The Riddle Trader** `OS_RIDDLE_CARAVAN` | Ossaria | 6 | 4 | 610 built |  | designed | designed |  |
| **Tomb Freight** `OS_TOMB_FREIGHT` | Ossaria | 6 | 4 | 610 built |  | designed | designed |  |
| **The Mural Gallery's Missing Letter** `OS_UNOWN_MURALS` | Ossaria | 6 | 0 | 207 built |  | designed | designed |  |
| **Ten Years of Light** `ZE_LOWLIGHT_LAMPS` | Zenith | 6 | 0 | 608 built |  | designed | designed |  |
| **Clean Water** `NA_CLEAN_WATER` | Nadir | 7 | 5 | 630 planned |  | designed | designed |  |
| **A Five Out of Ten** `NA_NOODLE_SCORE` | Nadir | 7 | 5 | 220 built |  | designed | designed |  |
| **Lamps Out** `NA_OCTAVE_LAMPS_OUT` | Nadir | 7 | 5 | 220 built | `FERRYMAN_MIREFEN` `FERRY_LAMP` `OCTAVE_NOCT` | needs maps | in maps |  |
| **Sewer Royalty** `NA_VENAM` | Nadir | 7 | 6 | 644 planned |  | designed | designed |  |
| **Something in the Sinkholes** `OS_SINKFIELD` | Ossaria | 7 | 5 | 628 built |  | designed | designed |  |
| **Adequate Swords** `AS_ADEQUATE_SWORDS` | Ashkaar | 8 | 6 | 240 built, 247 built | `ADEQUATE_OWNER` `ADEQUATE_SIGN` `EXCELLENT_SMITH` `HONEST_COURT` | designed | in maps |  |
| **Afraid of Heights** `AS_AFRAID_OF_HEIGHTS` | Ashkaar | 8 | 6 | 248 built | `TAMM` | designed | in maps |  |
| **Ashes Home** `AS_ASHES` | Ashkaar | 8 | 6 | 650 planned |  | designed | designed |  |
| **The Lava-Tube Terror** `AS_DRUDDIGON` | Ashkaar | 8 | 6 | 664 planned |  | designed | designed |  |
| **Too Loud for the Choir** `AS_OCTAVE_TOO_LOUD` | Ashkaar | 8 | 6 | 240 built | `CRUCIBLE_LEGATE` `OCTAVE_FORTE` | needs maps | in maps |  |
| **Seven Bouts** `AS_SEVEN_BOUTS` | Ashkaar | 8 | 6 | 240 built | `CRUCIBLE_LEGATE` | designed | in maps |  |
| **The Trial of Truth** `AS_TRIAL_OF_TRUTH` | Ashkaar | 8 | 6 | 247 built | `HALDEN` `HERALD_PYKE` | designed | in maps |  |
| **The Egg Run** `AS_EGG_RUN` | Ashkaar | 9 | 7 | 248 built |  | designed | designed |  |
| **Two Lucarios** `NA_GARRET` | Nadir | 9 | 0 | 263 built |  | designed | designed |  |
| **Lamplighter Kids** `NA_LAMPLIGHTER_KIDS` | Nadir | 9 | 7 | 260 built |  | designed | designed |  |
| **Pit Ringer** `NA_PIT_RINGER` | Nadir | 9 | 7 | 263 built |  | designed | designed |  |
| **What the Bride Tree Hears** `EL_EVER_BLOOM` | Elowen | 10 | 8 | 294 built |  | designed | designed |  |
| **Gerald** `EL_GERALD` | Elowen | 10 | 8 | 682 planned |  | designed | designed |  |
| **The Rootward Wake** `EL_ROOTWARD_WAKE` | Elowen | 10 | 8 | 296 built |  | designed | designed |  |
| **The Bride Tree's Heart** `EL_BRIDE_TREE_HEART` | Elowen | 11 | 9 | 294 built | `JUNO_BRIDE_TREE` | needs maps | in maps |  |
| **Crystal Sleep** `IS_ALEXANDRA` | Isenmar | 11 | 10 | 309 planned |  | designed | designed |  |
| **Eleven Years at One Hole** `IS_ELEVEN_YEARS` | Isenmar | 11 | 9 | 300 built |  | designed | designed |  |
| **The Harpoon Rite** `IS_HARPOON_RITE` | Isenmar | 11 | 9 | 306 built |  | designed | designed |  |
| **The Sinking Quarter** `IS_SINKING_QUARTER` | Isenmar | 11 | 0 | 309 planned |  | designed | designed |  |
| **The White Stag** `IS_WHITE_STAG` | Isenmar | 11 | 9 | 710 planned |  | designed | designed |  |
| **Cut Loose** `ZE_COURIER` | Zenith | 12 | 10 | 730 planned |  | designed | designed |  |
| **The Echo That Answers First** `AN_ECHO_HALL` | Antumbra | 13 | 12 | 346 planned |  | designed | designed |  |
| **The Still Water** `AN_OCTAVE_STILL_WATER` | Antumbra | 13 | 11 | 742 planned | `MERE_CRACK` `OCTAVE_LENTO` | not in maps | needs maps | waits on map 742 |
| **Your Other Half** `AN_OTHER_HALF` | Antumbra | 13 | 11 | 753 planned |  | designed | designed |  |
| **Shadows Fall Upward** `AN_SHADOWS_UP` | Antumbra | 13 | 12 | 760 planned |  | designed | designed |  |
| **Better Marks** `AN_STUDENT` | Antumbra | 13 | 11 | 344 planned |  | designed | designed |  |
| **It Keeps the Rain In** `AN_UMBRELLA` | Antumbra | 13 | 11 | 743 planned |  | designed | designed |  |
| **The Old Pincer** `EL_OLD_PINCER` | Elowen | 14 | 12 | 526 built, 703 planned | `OLD_PINCER` `WOODWARD_PINCER` | not in maps | not placed | waits on map 703 |
| **Amber, Again** `OS_AMBER_AGAIN` | Ossaria | 14 | 12 | 209 built | `SAHAR_DIGLAB` | needs maps | in maps |  |
| **The Bonewright's Rite** `OS_BONEWRIGHT` | Ossaria | 14 | 13 | 360 planned |  | designed | designed |  |
| **The Ring-Day** `OS_RING_DAY` | Ossaria | 14 | 13 | 363 planned | `BASTIAN_LAMPROOM` | not in maps | needs maps | waits on map 363 |
| **Where the Well Went** `OS_UNDERSANDS` | Ossaria | 14 | 12 | 783 planned |  | designed | designed |  |
| **The Unquiet Elector** `OS_UNQUIET_ELECTOR` | Ossaria | 14 | 12 | 770 planned |  | designed | designed |  |
| **Behind the Glass** `AN_BEHIND_THE_GLASS` | Antumbra | 15 | 14 | 347 planned |  | designed | designed |  |
| **Nine Hundred and Ninety-Nine** `AN_GIMMIGHOUL_COINS` | Antumbra | 15 | 13 | 380 planned |  | designed | designed |  |
| **The Smile Behind the Glass** `AN_SMILE_BEHIND_GLASS` | Antumbra | 15 | 13 | 346 planned | `SAFFI_SPECULUM` `THIRD_PANE` | not in maps | needs maps | waits on map 346 |
| **The Saga of the Glass Dunes** `IS_SAGA_OF_THE_ICE` | Isenmar | 15 | 13 | 921 planned |  | designed | designed |  |
| **The Doll Who Waited** `EL_DOLL_WHO_WAITED` | Elowen | 16 | 14 | 546 built, 547 built | `ATTIC_DOLL` `DOLL_BUTTON` | in maps | in maps |  |
| **The Lift Strike** `NA_LIFT_STRIKE` | Nadir | 16 | 14 | 830 planned |  | designed | designed |  |
| **The Laureate's Prize** `ZE_LAUREATE` | Zenith | 16 | 14 | 194 built |  | designed | designed |  |
| **Return to Sender** `ZE_RETURN_TO_SENDER` | Zenith | 16 | 14 | 320 planned, 323 planned, 324 planned, 325 planned | `DEAD_LETTER_DOOR` `GALE_POSTMASTER` | not in maps | needs maps | waits on map 320, 323, 324, 325 |
| **The Brazier Writ** `AS_BRAZIER_WRIT` | Ashkaar | 17 | 15 | 240 built | `CRUCIBLE_LEGATE` | needs maps | in maps |  |
| **The Forge Remembers** `AS_FORGE_REMEMBERS` | Ashkaar | 17 | 15 | 244 built | `BRANN_HEARTHGUILD` | needs maps | in maps |  |
| **Old Cinder** `AS_OLD_CINDER` | Ashkaar | 17 | 15 | 248 built | `OLD_CINDER` `ROOST_KEEPER` | needs maps | in maps |  |
| **Mother Gutter's Ledger** `NA_GUTTER_DEBTS` | Nadir | 17 | 15 | 423 planned |  | designed | designed |  |
| **Dogs of the Moon Market** `NA_MOON_MARKET_DOGS` | Nadir | 17 | 15 | 423 planned | `KENNEL_CAGE` `OTTOLINE_MOON_MARKET` | not in maps | needs maps | waits on map 423 |
| **The Tyrant's Heart** `OS_TYRANT_HEART` | Ossaria | 17 | 15 | 360 planned, 773 planned | `NASRIN_CRAGHOLM` `THIRD_VERTEBRA` | not in maps | needs maps | waits on map 360, 773 |
| **Dreamwalker** `AN_SHIV` | Antumbra | 18 | 17 | 440 planned |  | designed | designed |  |
| **Encore** `EL_ENCORE` | Elowen | 18 | 16 | 154 built | `DORIAN_ENCORE` | not placed | in maps |  |
| **The Twilight Cloister** `EL_TWILIGHT_CLOISTER` | Elowen | 18 | 16 | 440 planned |  | designed | designed |  |
| **The Causeway Matriarch** `IS_CAUSEWAY_MATRIARCH` | Isenmar | 18 | 16 | 560 built | `CAUSEWAY_MATRIARCH` | not placed | in maps |  |
| **Sweetrot** `NA_SWEETROT` | Nadir | 18 | 0 | 423 planned |  | designed | designed |  |
| **Dragonsworn** `AS_DRAGONSWORN` | Ashkaar | 19 | 17 | 460 planned |  | designed | designed |  |
| **The Memory Kata** `NA_MEMORY_KATA` | Nadir | 19 | 17 | 260 built | `OTTOLINE_LAST_RUNG` | needs maps | in maps |  |
| **The Pavilion Line** `CR_DELEGATION_DISPUTE` | Crownhaven | 20 | 0 | 499 planned |  | designed | designed |  |
| **Eighteen Shrines** `CR_EIGHTEEN_SHRINES` | Crownhaven | 20 | 18 | 890 planned |  | designed | designed |  |
| **The Chancellor's Other Ledger** `CR_HOLLIS_LEDGER` | Crownhaven | 20 | 0 | 486 planned |  | designed | designed |  |
| **Lost Property** `CR_LOST_PROPERTY` | Crownhaven | 20 | 0 | 499 planned |  | designed | designed |  |
| **Invitations to the Masque** `CR_MASQUE_INVITES` | Crownhaven | 20 | 0 | 483 planned |  | designed | designed |  |
| **The Ninth Verse** `CR_OCTAVE_NINTH_VERSE` | Crownhaven | 20 | 0 | 489 planned | `OCTAVE_CAROL` | not in maps | needs maps | waits on map 489 |
| **An Old Man's Errand** `CR_VALENS_ERRAND` | Crownhaven | 20 | 0 | 489 planned |  | designed | designed |  |
| **Hand of the Accord** `CR_ACCORD_CHAMPIONS` | Crownhaven | 21 | 0 | 496 planned |  | designed | designed |  |
| **Bedside Manner** `NA_BEDSIDE_MANNER` | Nadir | 21 | 18 | 223 built | `CORVIN_INFIRMARY` `WARD_BED` `WENLOW_INFIRMARY` | needs maps | in maps |  |
| **The Meteor Champion** `CR_LIN` | Crownhaven | 22 | 0 | 105 built |  | designed | designed |  |

## Event and quest-reward Pokemon

| Pokemon | Kind | Ch | Badges | Map | Quest | Quest now |
|---|---|---|---|---|---|---|
| `EL_NICKIT` Nickit | battle | 1 | 0 | 103 built | `EL_TART_THIEF` | in maps |
| `EL_SCARECROW_SPAR` Sudowoodo | battle | 1 | 0 | 521 built | `EL_SCARECROW` | in maps |
| `EL_TANDEMAUS` Tandemaus | gift | 1 | 0 | 100 built | `EL_STOWAWAYS` | in maps |
| `EL_GLASS_PONYTA` Ponyta (form 1) | battle | 2 | 1 | 522 built | `EL_GLASS_FOAL` | in maps |
| `EL_KECLEON` Kecleon | battle | 2 | 0 | 145 built | `EL_LANTERNS` | in maps |
| `EL_RALTS` Ralts | gift | 2 | 1 | 146 built | `EL_SOUND_OF_SALTMERE` | in maps |
| `EL_SANDYGAST` Sandygast | boss | 2 | 1 | 528 built | `EL_SAND_CROWN` | in maps |
| `EL_SMEARGLE` Smeargle | gift | 2 | 1 | 145 built | `EL_PAINT_LOFT` | in maps |
| `EL_TIDE_CLOBBOPUS` Clobbopus | battle | 2 | 1 | 527 built | `EL_TIDE_POOL_FEUD` | in maps |
| `EL_TIDE_CRABRAWLER` Crabrawler | battle | 2 | 1 | 527 built | `EL_TIDE_POOL_FEUD` | in maps |
| `EL_TIMBURR` Timburr | gift | 2 | 1 | 100 built | `EL_LAST_PLANK` | in maps |
| `EL_HERACROSS` Heracross | battle | 3 | 2 | 524 built | `EL_HORN_AND_PINCER` | in maps |
| `EL_JOLTIK` Joltik | gift | 3 | 3 | 548 built | `EL_MATRIARCH_HUM` | in maps |
| `EL_PINSIR` Pinsir | battle | 3 | 2 | 524 built | `EL_HORN_AND_PINCER` | in maps |
| `EL_SPIDOPS` Spidops | boss | 3 | 2 | 525 built | `EL_SILKTHIEF` | in maps |
| `AS_LITLEO` Litleo | boss | 4 | 2 | 146 built | `AS_LITTLE_CRUCIBLE` | in maps |
| `EL_DITTO` Ditto | battle | 4 | 2 | 568 built | `EL_REHEARSAL` | in maps |
| `EL_GREAVARD` Greavard | battle | 4 | 2 | 579 built | `EL_DROVERS_BELL` | in maps |
| `EL_SUDOWOODO` Sudowoodo | battle | 4 | 2 | 521 built | `EL_SCARECROW` | in maps |
| `EL_WATTREL` Wattrel | gift | 4 | 3 | 160 built | `EL_MASTER_OF_NOTHING` | in maps |
| `IS_BOMBIRDIER` Bombirdier | boss | 4 | 3 | 561 built | `IS_EGG_THIEF` | in maps |
| `IS_SNOM` Snom | gift | 4 | 2 | 160 built | `IS_OATH_PARCEL` | in maps |
| `ZE_CHARCADET` Charcadet | gift | 4 | 2 | 106 built | `ZE_FORM_7B` | in maps |
| `IS_CORSOLA` Corsola (form 1) | battle | 5 | 3 | 588 built | `IS_EBB_HOLLOW` | in maps |
| `ZE_PORYGON` Porygon | gift | 5 | 3 | 185 built | `ZE_CUSTOMER_SUPPORT` | in maps |
| `OS_CARBINK` Carbink | gift | 6 |  | 209 built | `OS_KEVIN` | designed |
| `OS_TRAPINCH` Trapinch | gift | 6 |  | 610 built | `OS_RIDDLE_CARAVAN` | designed |
| `ZE_DEX_PICHU` Pichu | gift | 6 |  | 608 built | `ZE_LOWLIGHT_LAMPS` | designed |
| `NA_GRIMER` Grimer (form 1) | gift | 7 |  | 220 built | `NA_NOODLE_SCORE` | designed |
| `OS_STUNFISK` Stunfisk (form 1) | boss | 7 |  | 628 built | `OS_SINKFIELD` | designed |
| `AS_DRUDDIGON` Druddigon | boss | 8 |  | 664 planned | `AS_DRUDDIGON` | designed |
| `AS_HOUNDOUR` Houndour | gift | 8 |  | 650 planned | `AS_ASHES` | designed |
| `AS_NOIBAT` Noibat | gift | 8 |  | 248 built | `AS_AFRAID_OF_HEIGHTS` | in maps |
| `AS_RANK_DEINO` Deino | egg | 8 |  | (rank reward) |  | rank reward |
| `AS_AXEW_EGG` Axew | egg | 9 |  | 248 built | `AS_EGG_RUN` | designed |
| `NA_FALINKS` Falinks | boss | 9 |  | 263 built | `NA_PIT_RINGER` | designed |
| `EL_EVER_BLOOM` Floette (form 4) | gift | 10 |  | 294 built | `EL_EVER_BLOOM` | designed |
| `EL_GERALD` Scatterbug | gift | 10 |  | 682 planned | `EL_GERALD` | designed |
| `EL_RANK_COMFEY` Comfey | gift | 10 |  | (rank reward) |  | rank reward |
| `IS_CETODDLE` Cetoddle | gift | 11 |  | 300 built | `IS_HARPOON_RITE` | designed |
| `IS_RANK_LAPRAS` Lapras | gift | 11 |  | (rank reward) |  | rank reward |
| `IS_TATSUGIRI` Tatsugiri (form 1) | gift | 11 |  | 300 built | `IS_ELEVEN_YEARS` | designed |
| `IS_WHITE_STAG` Sawsbuck (form 3) | battle | 11 |  | 701 planned | `IS_WHITE_STAG` | designed |
| `ZE_KLEFKI` Klefki | gift | 12 |  | 730 planned | `ZE_COURIER` | designed |
| `AN_HATENNA` Hatenna | gift | 13 |  | 743 planned | `AN_UMBRELLA` | designed |
| `AN_INDEEDEE` Indeedee (form 1) | gift | 13 |  | 753 planned | `AN_OTHER_HALF` | designed |
| `EL_OLD_PINCER` Pinsir | boss | 14 | 12 | 703 planned | `EL_OLD_PINCER` | not placed |
| `OS_YAMASK` Yamask (form 1) | gift | 14 |  | 770 planned | `OS_UNQUIET_ELECTOR` | designed |
| `AS_OLD_CINDER` Charizard | boss | 17 | 15 | 248 built | `AS_OLD_CINDER` | in maps |
| `IS_CAUSEWAY_MATRIARCH` Kangaskhan | boss | 18 | 16 | 560 built | `IS_CAUSEWAY_MATRIARCH` | in maps |
| `NA_POLTCHAGEIST` Poltchageist | gift | 18 |  | 423 planned | `NA_SWEETROT` | designed |
| `CR_OCTAVE_EEVEE` Eevee | gift | 20 |  | 489 planned | `CR_OCTAVE` | partly, needs maps |
