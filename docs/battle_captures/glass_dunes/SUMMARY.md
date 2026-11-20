# The Glass Dunes field sequence - headless logic test

> Logic-test output (real Essentials v21.1 battle code + Prismfall Core, Field Effects and Bosses, text scene).
> Not game footage. Regenerate: `PRISM_RUN_DIR=<private run dir> PRISM_OUT=<dir> ruby tools/harness/run_glass_dunes.rb`.

War pool (MAP_BORROW_POOLS[925/926]): VOLCANIC, ASHEN_WASTE, FROZEN_LAKE, SNOWY_MOUNTAIN, DESERT, FLOODED_DUNES, GLASS_DUNES

| Scenario | Result | Turns | Fields | Checks |
|---|---|---|---|---|
| A. Glass Dunes walk (map 926 default, no field rule): Kyogre vs Reshiram, both scripted | fled/forfeit | 10 | DESERT > FLOODED_DUNES > GLASS_DUNES > BLEED | starts_on_desert ok; desert_flood_glass ok; beam_clash_to_bleed ok; transform_strike ok; steam_on_flood ok; clash_progress ok; bleed_echoes_war_only ok |
| B. Primal Kyogre (Primordial Sea) vs Reshiram on 926: flood at send-out, glass under the heavy rain | fled/forfeit | 5 | DESERT > FLOODED_DUNES > GLASS_DUNES > FLOODED_DUNES > GLASS_DUNES | flood_before_turn_1 ok; snuffed_flare_glasses ok; origin_pulse_refloods ok; fusion_flare_reglass ok |
| C. AI vs AI: Reshiram boss (3 bars, break 1 = the flood-sea) vs Kyogre, Garchomp, Lapras on 926 | player lost | 6 | DESERT > DESERT st2 > FLOODED_DUNES > GLASS_DUNES | starts_on_desert ok; reaches_flood ok; reaches_glass ok; no_exceptions ok |
| D. AI vs AI: Primal Kyogre boss (2 bars) vs Reshiram, Charizard, Garchomp on 926 | player lost | 2 | DESERT > FLOODED_DUNES | flooded_at_start ok; no_exceptions ok |
| E. Tide: Flooded Dunes, the player's Sunny Day drains the flood (sun: 2 a round) | fled/forfeit | 4 | FLOODED_DUNES > DESERT > DESERT st2 | drains_to_desert_bloom ok; warned ok |
| E2. AI vs AI on the Flooded Dunes: Kyogre vs a Drought Ninetales (sun drains the tide) | player lost | 4 | FLOODED_DUNES > DESERT > DESERT st2 | no_exceptions ok; warned ok |
| F. The Steamline (map 925 default, no field rule): 15 quiet rounds of Bleed rotation | fled/forfeit | 15 | BLEED | default_is_bleed ok; rotated ok; war_pool_only ok |
| F2. Control: the Bleed on a map without a pool (990) borrows from every field | fled/forfeit | 15 | BLEED | borrows_outside_war_pool ok |
| G1. AI vs AI on 926: ISENMAR_OFFICER Captain v1 vs Lv.85 challenger | player won | 12 | DESERT > DESERT st2 > DESERT st1 | no_exceptions ok; starts_on_desert ok |
| G2. AI vs AI on 926: ASHKAAR_OFFICER Captain v1 vs Lv.85 challenger | player lost | 9 | DESERT | no_exceptions ok; starts_on_desert ok |
| G3. AI vs AI on 926: ISENMAR_SOLDIER_F Soldier v1 vs Lv.85 challenger | player won | 7 | DESERT > DESERT st2 | no_exceptions ok; starts_on_desert ok |
| G4. AI vs AI on 926: ASHKAAR_SOLDIER_F Soldier v1 vs Lv.85 challenger | player lost | 7 | DESERT | no_exceptions ok; starts_on_desert ok |
| G'1. AI vs AI on 926 with the suggested WANTS: ISENMAR_OFFICER Captain v1 vs Lv.85 challenger | player won | 12 | DESERT > DESERT st2 > DESERT st1 | no_exceptions ok |
| G'2. AI vs AI on 926 with the suggested WANTS: ASHKAAR_OFFICER Captain v1 vs Lv.85 challenger | player won | 7 | DESERT | no_exceptions ok |
