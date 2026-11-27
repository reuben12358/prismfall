# Act 2 Maps Batch 3A — Duneholt Core (`200–209, 214` · Ossaria Canyon Capital!)

**Status:** Independent `visual_critic` Pass 3 Certified — **`11 / 11 PASS`**, Mean **`9.19 / 10`**, **`0 P0`**, **`11 maps; 0 warnings`**, **`11 / 11` byte-identical roundtrip**, **`5 / 5` Outdoor Rubric PASS**, **`4 / 4` seamless stitched outdoor seams**.

## Summary of Added Maps (`153 → 164` Built Maps on `main`)

| Map | Name | Size | TS | Field | Critic Final | Highlights |
|---:|---|---:|---:|---|---:|---|
| **200** | Duneholt - Terrace Bazaar | `48×44` | 56 | `DESERT` | **9.1/10** | 3-tiered Ossaria canyon bazaar, crimson Palace mosaic avenue, travertine South Spine matching `203`, stone-coped central cistern, rock-cut `pf_minemouth` Necropolis entry, guarded `210` Gym & `810` Dry Tide warps |
| **201** | Duneholt Pokémon Center | `15×11` | 34 | — | **9.4/10** | Gold-standard symmetrical 5-wide `0x8f` warm-timber U-counter centered on Pokéball medallion, `HealingSpot: [200, 9, 22]`, Gale Post desk (Larch Ch6 note + `:KELPTEABAG`), twin `HOTEL_WINDOW`s |
| **202** | Duneholt Mart | `12×10` | 34 | — | **9.2/10** | Flush 5-tile `0x8f` L-counter, framed Ossaria wall map, clean terracotta interior, 10 canonical Ch6 PBS items |
| **203** | Duneholt - Sandgate | `40×24` | 56 | `DESERT` | **9.1/10** | Carved sandstone canyon gate bastions crowned with twin blazing `pf_beacon` braziers & Ossaria banners, continuous travertine road, caravan camp, guarded south `613` Sunbleach Flats exit |
| **204** | Duneholt - Aquifer Quarter | `44×36` | 56 | `DESERT` | **9.0/10** | Cohesive connected Great Well + twin feeder canals framed in sandstone coping, twin waterwheels, dry travertine causeway bridges, charcoal-slate Meridian Deep-Works terrace, symmetrical oasis bamboo, all 3 upper-terrace door plaques 100% BFS reachable |
| **205** | Elector's Palace - Courtyard | `40×34` | 56 | `DESERT` | **9.2/10** | Palatial limestone facade, twin sandstone-coped reflecting pools flanking the radiant desert sunburst medallion, symmetrical guardian statues & olive trees |
| **206** | Elector's Palace - Hall of Audience | `29×25` | 59 | — | **9.2/10** | Symmetrical royal chamber with `3/3` intact chandeliers (`18/18` tiles), triple banners framing Prince-Elector Kassan's elevated dais, unobstructed West/East crimson portal runners into recessed gallery alcoves |
| **207** | Elector's Palace - Mural Gallery | `41×15` | 59 | — | **9.2/10** | Grand colonnaded hall with `4/4` intact chandeliers (`24/24` tiles), 4 deepened Ossaria history mural alcoves, strictly `W0` return warps `(39,8..9)` |
| **208** | Necropolis of the Electors | `44×40` | 57 | `CAVE` | **9.3/10** | Subterranean canyon-stone crypt with `15/15` intact burning braziers, sunken pool, recessed NW Royal Crypt stair alcove, walkable East Marrow Tunnel Opening (`620` guarded), `[CHANNELER, Zenobia]` & `[RUINMANIAC, Lucan]` (`4/4` clear sightlines, `0` duplicates) |
| **209** | Sahar's Dig Lab | `21×15` | 34 | — | **9.3/10** | Complete 3×4 fossil revival `labtank` (live 11-fossil revival), complete 3×3 closed bookcase, `pf_trial_board(:OSSARIA)`, `pf_trial_talk(:SAHAR_DIGLAB)`, `OS_KEVIN` hook, seamless crimson runner |
| **214** | Duneholt - Sinkwells | `40×30` | 56 | `DESERT` | **9.1/10** | Stepped canyon drawdown basin, stone-coped sinkwell cistern, recessed west shaft plinth, worker camp & Mason/Well-Keeper lore |

## Notes for Claude
- **Zero edits to existing maps, `rstamps.yaml`, `MAP_AUDIO.yaml`, `flags.yaml`, `plugins/`, `pbs/`, `story/`, or `tools/`.**
- **Canonical PBS Trainers (`0` duplicates across all built specs):** `[CHANNELER, Zenobia]` & `[RUINMANIAC, Lucan]` (`208`).
- **Live Engine Integration:** All 11 `.rxdata` files verified against live `Tilesets_prismfall.rxdata` (`void_L0=0, oob=0, bad_auto=0, passguard=0, green_borders=0, meta_strings=0`), synced into `/home/antigravity/pf_engine_run/game/Data/`, and captured live in `mkxp-z`.
- **Guarded Exits Ready for Batch 3D+ (`pbRgssExists?`, 0 warnings):** `200 → 210` (Duneholt Gym 5), `200 → 810` (Dry Tide), `203 → 613` (Sunbleach Flats), `208 → 620` (The Marrow Road).
