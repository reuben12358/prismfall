# Claude Integration Handoff — Unbuilt World Maps Batch 2 (`240–243` Cindervault Core & `594` Wallshadow Row)

All **5 brand-new canonical world maps** (`240`, `241`, `242`, `243`, `594`) are built, independently audited by `visual_critic` (**5/5 PASS: `9.0–9.2/10`, `0 P0`, `0` `NB2AUTO` mismatches, `0` passguard hits, `100%` directional BFS event reachability across all 124 events & `9/9` cross-map warp contracts**), and committed directly under `mapgen/` and `maps_out/`.

This proposal provides ready-to-wire Claude-owned items (`pbs/encounters.txt`, `design/MAP_AUDIO.yaml` alignment, and Ch5 / Ch8 story & side-quest script hook coordinates). Zero Claude-owned files were directly edited.

---

## 1. Critic-Certified Map Summary & Active Warp Matrix

| Map | Name | Size / TS | Critic Pass 2 | Active Warps / Doors | Guarded Future Exits (`pbRgssExists?`) |
|---:|---|---:|:---:|---|---|
| **240** | Cindervault – Forge Terraces | `46×42` / `61` | **9.0/10 PASS** | `(20,27)` → `249 (4,3) down` *(arrives from `249` at `(20,26) up`)*; PC door `(7,20)` `CV_PC` → `241 (7,10) up`; Mart door `(13,20)` `CV_MART` → `242 (5,9) up`; SE stair `(28..30,40)` → `243 (34,6) down` | `(20..22,2)` → `250` The Foundry Gym 7; `(5..7,2)` → `245` Pyre Keep Rampart; `(37..39,2)` → `248` Dragon Roosts; `(1,23..25)` → `660` The Ashmarch |
| **241** | Cindervault Pokémon Center | `15×11` / `34` | **9.1/10 PASS** | Exit `(7,10)` `CV_PC` → `240` PC doorstep `(7,21) down`; `HealingSpot: [240, 7, 21]` | — |
| **242** | Cindervault Mart | `12×10` / `34` | **9.0/10 PASS** | Exit `(5,9)` `CV_MART` → `240` Mart doorstep `(13,21) down` | — |
| **243** | Cindervault – Caldera Gate | `40×24` / `61` | **9.2/10 PASS** | North path `(19..21,3)` → `249 (21,31) up` *(arrives from `249` at `(20,4) down`)*; NE stair `(33..35,5)` → `240 (29,37) up` *(arrives from `240` at `(34,6) down`)* | South portcullis `(18..21,22)` → `652` The Pyre Road; West pass `(1,13..15)` → `660` The Ashmarch |
| **594** | Wallshadow Row | `150×80` / `60` | **9.0/10 PASS** | East Crown Road `(149,38..42)` → `593 (1,20) right` *(arrives from `593` at `(148,40) left`)* | West `(0,39..43)` → `595` Coppice Ride; NW bluff `(0,21..24)` → `681` Prism Falls; North pass `(42..45,1)` → `756` Kingsmead; SE lift `(121..123,71)` → `672` The Long Drop; NE spur `(149,21..24)` → `602` Candle Down |

---

## 2. Story & Side-Quest Integration Hooks (Exact Verified Tile Coords)

All placed NPCs and signs are static with **zero invented switches/variables**:

### Chapter 8 — Cindervault (`story/29_SCRIPT_CH8.md` & `design/TRIALS_QUESTS.md`)
- **Map `243` (Caldera Gate):**
  - **"The Hug"** (`V129 == 3 → 4`): Trigger autorun stepping north through the `gt_gate6` south portcullis archway `(18..21, 19..20)`. Brann descends the central stone staircase `(18..21, 8..10)`; Gate Smith is staged at `(15, 12)` right beside the warning bell-post `(13, 11)`.
  - **Departure beat (`V129 == 9 → 10`):** Swap Gate Smith `(15, 12)` dialogue on `S121 CH8_WAR_DRUMS` + add `:ch8_lightstone` reaction NPC near NE terrace stair `(33, 11)`.
- **Map `240` (Forge Terraces):**
  - **"Five Bells" (`V129 == 5 → 6`)**: Trigger on exiting `250` Foundry `(20..22, 3)`. Hearthguild Bell-Ringer stands on the projecting Bell-Tower balcony at `(21, 15)` overlooking Caldera Square `(18..28, 21..26)`.
  - **"The Herald" (`V129 == 8 → 9`)**: Caldera Square `(18..28, 21..26)` is kept wide open for the red-lacquer column + Rapidash herald; Bell-Tower balcony `(20..22, 15)` overlooks the square for Sigrun's silent cameo above.
  - **`:ashkaar_watched` escort**: Spawn polite Oath-Guard follower near Caldera Square when `pfm_get(:ashkaar_watched)`.
  - **Ashen state (`V110 == 1`, `:vent`)**: Optional fog/tone swap or sweeping-smith dialogue swap on `V110 == 1`.
  - **Side Quests (`design/TRIALS_QUESTS.md`):**
    - `AS_OCTAVE_TOO_LOUD` (Forte, Octave 6/8): Forte at `(34, 24)` outside The Crucible gate; Legate Varra Kosk at `(37, 21)` inside the east rim sand ring `(33..41, 21..26)`.
    - `AS_SEVEN_BOUTS` & `AS_BRAZIER_WRIT`: Legate Varra Kosk `(37, 21)` + Crucible Plaque `(34, 21)`.
    - `AS_ADEQUATE_SWORDS`: Adequate Swords Owner at `(8, 38)` outside `"ADEQUATE SWORDS."` `(9, 37)`, directly across the lane from `"EXCELLENT SWORDS."` `(14, 37)` (`SE Door Plate` at `(39, 37)` verified reachable via 2-wide paved lane `(35..40, 38..39)`).

### Chapter 5 — Wallshadow Row (`story/24_SCRIPT_CH5.md:213-282`)
- **Map `594` (Wallshadow Row):**
  - **"Juno at the Four Ways" (`V125 <= 1 → 2`)**: Stage Juno on the Four Ways Inn mounting block `pf_stonebench` at `(15, 39)` outside `sp_inn` `(11, 31)` (door `(13, 38)`) and Four Ways Innkeeper `(14, 39)`.
  - **Juno follower commentary hooks:** Royal Forester `(7, 22)` on NW Prism Falls bluff (`"I came DOWN it. It only works one way."`); Southgate Chapel Window `(111, 55)` on Southgate Shrine (`wh_e` `(105, 48)`, Prayer Board `(107, 56)`, Shrine-keeper `(109, 57)`).
  - **Roadblock unlocks:** Lift Guard `(120, 70)` → `672` Long Drop; Road-mender `(143, 23)` → `602` Candle Down; Tithe-reeve `(44, 7)` → `756` Kingsmead; Royal Forester `(7, 22)` → `681` Prism Falls.
  - **5 PBS Trainers Placed (`pbs/trainers.txt` verified):** `AROMALADY, Linnet` `(64, 32)`, `YOUNGSTER, Hodge` `(51, 46)`, `LASS, Marigold` `(31, 46)`, `TAMER, Hob` `(88, 37)`, `TWINS, Meg & Peg` `(129, 44)` (double battle).
  - **4 Items Placed:** `SUPERPOTION` `(22, 65)`, `GREATBALL` `(76, 70)`, `MIRACLESEED` `(117, 19)`, hidden `REVIVE` `(76, 18)` beside the loose bricks of the Secret Bricked-Up Accord Cave embedded flush in the chalk Crownwall `(73..75, 14..16)` (sign `(74, 16)`).

---

## 3. Recommended `pbs/encounters.txt` Entry for Map `594` (Wallshadow Row)

Canon wild list from `design/WORLD.md:494` (`:MEADOW`, Ch5 Lock Road levels 18–22 matching adjacent `593`):

```ini
#-------------------------------
[594] # Wallshadow Row
Land,21
    20,LILLIPUP,18,21
    20,WOOLOO,18,21
    15,SMOLIV,18,21
    15,FIDOUGH,18,21
    15,FLABEBE,19,21
    15,MAREEP,19,22
LandNight,21
    25,HOOTHOOT,18,21
    20,SPINARAK,18,21
    20,MORELULL,19,22
    15,WOOLOO,18,21
    10,LILLIPUP,18,21
    10,MAREEP,19,22
Water,4
    50,MARILL,18,21
    30,LOTAD,18,21
    20,SURSKIT,18,20
```

---

## 4. `design/MAP_AUDIO.yaml` Alignment

Maps `240`, `243`, and `594` already embed their `map_audio:` blocks directly in their YAML specs (auto-compiled into `013_MapAudio.rb` by `build.py`), while `241` & `242` use built-in Essentials `Poke Center` / `Poke Mart`:

```yaml
240: {bgm: "Town - Ashkaar", bgs: "Lava - Ashkaar", bgs_volume: 55, rain: false}
241: {bgm: "Poke Center", bgs: "", rain: false}
242: {bgm: "Poke Mart", bgs: "", rain: false}
243: {bgm: "Town - Ashkaar", bgs: "Lava - Ashkaar", bgs_volume: 55, rain: false}
594: {bgm: "Route - Elowen", bgs: "", rain: true}
```
