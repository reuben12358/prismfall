# Act 2 Maps Batch 3B — Cindervault Gym 7 & Pyre Keep (`245–248, 250–254` · `16/16` Cindervault Complete!)

**Status:** Independent `visual_critic` Pass 2 Certified — **`9 / 9 PASS`**, Mean **`9.31 / 10`**, **`0 P0`**, **`0 P1`**, **`9 maps; 0 warnings`**, **`9 / 9` byte-identical roundtrip**, **`418`-state exhaustive Gym 7 solver `0` softlocks / `0` leaks**.

## Summary of Added Maps (`144 → 153` Built Maps on `main`)

| Map | Name | Size | TS | Field | Critic Pass 2 | Highlights |
|---:|---|---:|---:|---|---:|---|
| **245** | Pyre Keep - Rampart | `33×25` | 61 | `DRAGONS_DEN` | **9.1/10** | Twin Ashkaar gatehouse aligned to `gt_gate6`, Patrol Arcanine & Rapidash, Officer Corvus, `DRAGONFANG`, exact `Map 240` arrival `(16,22)` |
| **246** | Pyre Keep - Ember Throne | `27×27` | 61 | `DRAGONS_DEN` | **9.4/10** | Panoramic living volcanic caldera magma window, cut-basalt lintel, obsidian columns, solid `y=5` golden-iron parapet, sweeping crimson runner, Lord-Steward Vaelen, `FIRESTONE` |
| **247** | Pyre Keep - Hall of Oaths | `33×23` | 61 | `DRAGONS_DEN` | **9.3/10** | Ceremonial gallery, 4 Oath Plinths, **Herald Pyke** (`AS_TRIAL_OF_TRUTH` + `pf_trial_board(:ASHKAAR)`), framed West Crypt portal (`cv_gate_open`), `FIREGEM` |
| **248** | Pyre Keep - Dragon Roosts | `36×24` | 61 | `DRAGONS_DEN` | **9.2/10** | 3-tier volcanic dragon perches, **Roost-Keeper Tarn** (`pf_trial_talk(:ROOST_KEEPER)`), **Old Cinder** (`pf_trial_talk(:OLD_CINDER)`), Ashkaar `wr_tent_r` harness pavilion, Salamence/Flygon/Axew/Trapinch/Noibat/Bagon, `DRAGONGEM`, `MAXPOTION`, exact `Map 240` arrival `(12,20)` |
| **250** | Cindervault Gym - Entrance | `25×24` | 61 | `VOLCANIC` | **9.3/10** | Gym Guide, Foundry Medic (full heal), Camper Flint, 1-channel Pour/Quench TEACH trough with solid iron abutment piers & recessed slag trough bed (`V339`), exact `Map 240` arrival `(12,22)` |
| **251** | Cindervault Gym - Puzzle Room 1 | `29×27` | 61 | `VOLCANIC` | **9.4/10** | Pour Floor (`K1–K3` aimable crucibles, shared quench cistern `V338`, `touch`+confirm `C1/C2` steel chute hatches `25938` vs wooden ladders `23876`, zero-softlock Apprentice Hessa reset, `[ENGINEER, Garran]` & `[BLACKBELT, Ivar]`) |
| **252** | Cindervault Gym - Puzzle Room 2 | `29×27` | 61 | `VOLCANIC` | **9.2/10** | Mould Floor (`M1–M3` cross-floor cast decks, airtight Mastery Vault bulkhead + `S339` vault rewarding `2× ELEMENTALSEED` + `CHARCOAL`, Mould-Runner reset, `[ENGINEER, Oda]` & `[COOLTRAINER_M, Dain]`) |
| **253** | Cindervault Gym - Warden Arena | `21×19` | 61 | `VOLCANIC` | **9.5/10** | Warden Brann caldera arena (`Prismfall.gym_battle(pfm_gym(:LEADER_BRANN), double: false)`, `award_badge`, `:TM35`, `CH8_STEP >= 5`, `S339` Mastery recognition) + framed `lm_sdoor` Fast-Exit Lift to `250` |
| **254** | Pyre Keep - Ancestor Crypts | `33×29` | 61 | `HOLLOW_CATHEDRAL` | **9.4/10** | Cruciform basalt crypt, First Dominar obsidian monolith & sarcophagus altar, south stone ascent stairs, Crypt Litwick, `[CHANNELER, Thessaly]`, `SPELLTAG`, `STARPIECE` |

## Notes for Claude
- **Zero edits to `240_cindervault_forge.yaml`, `255_cindervault_tap.yaml`, `flags.yaml`, `plugins/`, `pbs/`, `story/`, or `tools/`.**
- **Gym 7 Switch / Variable Block (`0` collisions across repo):** `V335–V339, S335–S339, V435–V437, S435–S437` — recommend registering these IDs in `mapgen/flags.yaml` during routine housekeeping.
- **Canonical PBS Trainers (`0` duplicates across all built specs):** `CAMPER,Flint` (`250`), `ENGINEER,Garran` & `BLACKBELT,Ivar` (`251`), `ENGINEER,Oda` & `COOLTRAINER_M,Dain` (`252`), `LEADER_BRANN` (`253`), `CHANNELER,Thessaly` (`254`).
- **Live Engine Integration:** All 9 `.rxdata` files verified against live `Tilesets_prismfall.rxdata` (`void_L0=0, oob=0, bad_auto=0, passguard=0, over_trigger_bad=0, pbShake=0`), synced into `/home/antigravity/pf_engine_run/game/Data/`, and captured live in `mkxp-z`.
