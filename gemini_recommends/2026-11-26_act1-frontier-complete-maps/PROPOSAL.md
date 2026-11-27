# Act 1 Frontier Complete — 10 New Built Maps (Batch 1B → `144` Built Maps = ACT 1 100% Complete!)

**Date:** 2026-11-26  
**Scope:** 10 Final Act 1 Frontier Maps (`565, 580, 581, 584, 585, 588, 590, 591, 592, 595`)  
**Verification:**
- **Strict Build:** `/usr/bin/python3 mapgen/build.py --strict --only 565 580 581 584 585 588 590 591 592 595` → **`10 maps; 0 warnings`** (`GATE ok 584 Turbine Blast Shutter`).
- **Roundtrip:** `verify.py roundtrip` → **`10/10 byte-identical`**.
- **Independent Forensic Critic Pass 2:** **`10 / 10 PASS` (Mean `9.05 / 10`, `0 P0`)** — including both Reuben direct visual rebuilds (`591` Brassfall PC symmetrical alpine timber U-counter **`9.4/10`**, `595` Coppice Ride monumental double-tiered white Crownwall **`9.2/10`**), `21/21` exact canonical PBS trainers (`0` duplicates across all `144` specs), `20/20` south-readable `pf_signpost` events on solid base `18112`, `0` missing SEs, `4/4` Lock Road seams + `3/3` outbound arrivals (`160`, `564`, `594`) 4-bit BFS verified, and `6/6` Outdoor Rubric PASS.

---

## 1. Delivered Map Table (All Committed in `mapgen/` & `maps_out/Data/`)

| ID | Map Name | Size / TS | Critic Pass 2 | Connections / Integration Notes |
|---:|---|---|---:|---|
| **565** | Gullcry Caves B1F | `32×30` / TS 57 | **9.1 / 10** | Return warp `(16,1) → 564 (29,6)` (Gullcry Caves); `5` valid PBS items |
| **580** | The Reedholms | `110×90` / TS 52 | **8.9 / 10** | North/East seam to `592` (`7` matched), west warp to `160 (58,36)`, NW dam portal `[18,14] → 584`, 3-tile linked Teo bridge trigger `(55,43..45)`, `5` PBS trainers (`Solveig, Tarjei, Aksel, Sunniva, Jorun`) |
| **581** | The Icefall Locks | `72×120` / TS 52 | **9.2 / 10** | South seam to `590` (`6` matched), East seam to `595` (`6` matched), Ice Elevator Top `(14,17) ↔ 590 (32,10)`, recessed Ice Cave `(21,30)`, Lattice No. 4 fenced north of road, `4` PBS trainers (`Brede, Hartley, Alwin, Ylva`) |
| **584** | Voltaic Sluiceworks | `40×32` / TS 60 | **8.9 / 10** | Dual-breaker puzzle (`pfm?(:sluice_b1) && pfm?(:sluice_b2)`) gating `Turbine Blast Shutter (36,4)` → `585`, `2` PBS trainers (`Elwin, Nix`) |
| **585** | Sluiceworks Turbine Hall | `30×24` / TS 60 | **9.1 / 10** | Boss Rotom dais, `CELLBATTERY (26,4)` powering Brassfall Ice Elevator, solid chasm plinths |
| **588** | Ebb Hollow | `34×30` / TS 60 | **9.0 / 10** | Bleed Shard #4 (`29,25`, SE `'Mining item get'`), White coral + 3rd boundary stone (`10,19`), `TM49 (4,4)`, `Hidden Big Pearl (8,4)` |
| **590** | Brassfall | `40×36` / TS 52 | **9.0 / 10** | West seam `592` (`6`), North seam `581` (`6`), Ice Elevator `(32,9)` (consumes `CELLBATTERY` → `pfm_set(:brassfall_elevator)`), `T590_PC ↔ 591`, on-screen Arrival touch strip `x=16, y=15..24`, `2` PBS trainers (`Ingvild, Corwin`) |
| **591** | Brassfall Pokémon Center | `15×11` / TS 34 | **9.4 / 10** | `HealingSpot [590, 11, 22]`, symmetrical alpine timber U-counter (`x=5..9, y=2..3`, `0x8f`), `NPC 16` Nurse `(8,2)`, Gale Post Clerk `(3,6)` advancing `V125 CH5_STEP (0→1)` + `:ch5_eighteen_roads`, 10-item Mart `(11,6)` |
| **592** | The Icecutters' Haul | `110×70` / TS 52 | **8.8 / 10** | West seam `580` (`7`), East seam `590` (`6`), sealed North & South Sawyer's Cross stone gates, `3` PBS trainers (`Bodil, Torsten, Nils`) |
| **595** | Coppice Ride | `110×72` / TS 60 | **9.2 / 10** | West seam `581` (`6`), East arrival `594 (1,41)` (Wallshadow Row), monumental double-tiered white Crownwall + cascading River Ebb spring + 3-tile Crownwall view trigger `(66..68,21)`, open `MIRACLESEED (87,56)`, `5` PBS trainers (`Hazel, Wat, Perkin, Tansy, Osric`) |

---

## 2. Optional Follow-Up Notes for Claude (`pbs/` / `design/MAP_AUDIO.yaml` / `mapgen/merge_mapinfos.py`)
- All 10 new map IDs (`565, 580, 581, 584, 585, 588, 590, 591, 592, 595`) are ready for `design/MAP_AUDIO.yaml` entries (specs currently carry clean fallback BGMs), `MapInfos.rxdata` merge, and `pbs/connections.txt` seamless edge stitching (`580↔592`, `592↔590`, `590↔581`, `581↔595`, `595↔594`)!
- Zero edits were made to Claude-owned files (`plugins/`, `pbs/`, `story/`, `tools/`, `design/MAP_AUDIO.yaml`, `mapgen/rstamps.yaml`).
