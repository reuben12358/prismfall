# Proposal — Batch 1A Unbuilt Act 1 Maps: Lumen Upper Wards, Meridian Spire Upper Floors & Reyes Cellar (`9` Brand-New Maps → `134` Built Maps!)

**Status:** **9 / 9 Independent Visual Critic PASS (Pass 2 Mean `9.12 / 10`, `0 P0` defects)** · `134 maps; 0 warnings` (`mapgen/build.py --strict`) · `9 / 9` byte-identical `verify.py roundtrip` · `100%` 4-bit directional BFS reachability · `0` edits to existing built maps or Claude-owned paths.

> Note: Map `133` (Loomhouse Spindle) was intentionally skipped because it is retired in SPINE Rev 14 (`design/GYM_PUZZLES.md:394`).

## 1. Delivered Maps & Independent Critic Scores (`9 / 9 PASS`, Mean `9.12 / 10`)

| Map | Canonical Name | Size & TS | Layout Module & Spec | Pass 2 Critic Score |
|---:|---|---|---|---:|
| **166** | Reyes Cellar (Hollow cell) | `17×13` TS 34 | `mapgen/layouts/act1_upper_interiors.py` → `mapgen/specs/166_reyes_cellar.yaml` | **9.2 / 10 PASS** |
| **184** | Lumen Arcade Dept. Store 2F | `21×15` TS 34 | `mapgen/layouts/act1_upper_interiors.py` → `mapgen/specs/184_lumen_arcade_2f.yaml` | **9.2 / 10 PASS** |
| **194** | Lumen City – Council Ward | `48×40` TS 60 | `mapgen/layouts/lumen_upper_wards.py` → `mapgen/specs/194_lumen_council_ward.yaml` | **9.3 / 10 PASS** |
| **195** | Lumen City – Spire District | `44×48` TS 60 | `mapgen/layouts/lumen_upper_wards.py` → `mapgen/specs/195_lumen_spire_district.yaml` | **9.3 / 10 PASS** |
| **196** | Lumen City – Skyport Terrace | `40×36` TS 60 | `mapgen/layouts/lumen_upper_wards.py` → `mapgen/specs/196_lumen_skyport_terrace.yaml` | **9.0 / 10 PASS** |
| **197** | Zenith Council Hall – Council Chamber | `31×23` TS 60 | `mapgen/layouts/lumen_upper_wards.py` → `mapgen/specs/197_zenith_council_chamber.yaml` | **9.1 / 10 PASS** |
| **198** | Meridian Spire – Executive Gallery | `31×19` TS 60 | `mapgen/layouts/lumen_upper_wards.py` → `mapgen/specs/198_meridian_executive_gallery.yaml` | **9.0 / 10 PASS** |
| **199** | Meridian Spire – Dark Stone Core | `25×25` TS 60 | `mapgen/layouts/lumen_upper_wards.py` → `mapgen/specs/199_meridian_dark_stone_core.yaml` | **9.1 / 10 PASS** |
| **959** | Skyport Customs | `17×11` TS 34 | `mapgen/layouts/lumen_upper_wards.py` → `mapgen/specs/959_skyport_customs.yaml` | **8.9 / 10 PASS** |

---

## 2. Exact 1-Line Incoming Warp Hookups (on Existing Built Maps)

All **outbound return warps** on the 9 new maps are already wired to verified walkable & BFS-reachable coordinates on `164`, `180`, `183`, and `185`, and all internal Batch 1A bi-directional links (`194↔197`, `196↔959`, `198↔199`) are already wired and verified.

### A. Map `164` — Reyes House → `166` Reyes Cellar (Hollow cell)
- On `Map164.rxdata`, `[3, 6]` is the verified walkable cell directly east of the cellar hatch `[1, 6]`; `166 [13, 3]` returns cleanly to `164 [3, 6] down`.
- Incoming hookup on `164` (when cellar hatch unlocks in Ch4):
  ```yaml
  - {type: warp, name: 'Cellar door', at: [1, 6], to: {map: 166, x: 13, y: 4, dir: down}, se: 'Door enter'}
  ```

### B. Map `183` — Lumen Arcade 1F → `184` Lumen Arcade Dept. Store 2F
- `184 [19, 2]` (`Escalator to 1F`) returns cleanly to verified walkable `183 [16, 6] left`.
- Incoming hookup on `183` (place silver escalator stamp `7431/7439` at `(17, 5..6)`):
  ```yaml
  - {type: warp, name: 'Escalator to 2F', at: [17, 6], to: {map: 184, x: 18, y: 2, dir: left}, se: 'Door enter'}
  ```

### C. Map `180` — Lumen City: The Concourse → `194`, `195`, `196`
All three return arrivals on `Map180.rxdata` (`[47, 8]`, `[84, 14]`, `[74, 6]`) sit directly beside existing ward guards & signs (`[57]`, `[58]`, `[59]`):
```yaml
- {type: warp, name: 'To Council Ward',    at: [47, 6],  to: {map: 194, x: 24, y: 38, dir: up}}
- {type: warp, name: 'To Spire District',  at: [85, 14], to: {map: 195, x: 1,  y: 35, dir: right}}
- {type: warp, name: 'To Skyport Terrace', at: [74, 4],  to: {map: 196, x: 20, y: 34, dir: up}}
```
*(Note: `195 [22, 12]` Meridian Spire door links directly to `185 [12, 15] up` via explicit `to:` with zero duplicate `LC_TOWER` link conflict.)*

### D. Map `185` — Meridian Spire Lobby → `198` Meridian Spire: Executive Gallery
- `198 [15, 18]` returns cleanly to `185 [12, 6] down`.
- Incoming hookup on `185` (Executive Lift trigger in north lobby wing):
  ```yaml
  - {type: warp, name: 'Executive Lift', at: [22, 6], to: {map: 198, x: 15, y: 17, dir: up}, se: 'Door enter'}
  ```

---

## 3. Suggested `design/MAP_AUDIO.yaml` Entries (9 Maps)

```yaml
  166: {bgm: "Dungeon - Cave", bgs: "Drip - Nadir", bgs_volume: 40, rain: false}            # Reyes Cellar (Hollow cell)
  184: {bgs: ""}                                                                             # Lumen Arcade Dept. Store 2F (keeps Poke Mart BGM)
  194: {bgm: "Town - Zenith", bgs: "Machinery - Zenith", bgs_volume: 45}                     # Lumen City - Council Ward
  195: {bgm: "Theme - Meridian", bgs: "Machinery - Zenith", bgs_volume: 55}                  # Lumen City - Spire District
  196: {bgm: "Town - Zenith", bgs: "Wind - Isenmar", bgs_volume: 50}                         # Lumen City - Skyport Terrace
  197: {bgm: "Theme - Accord", bgs: ""}                                                      # Zenith Council Hall - Council Chamber
  198: {bgm: "Theme - Meridian", bgs: "Machinery - Zenith", bgs_volume: 35, rain: false}     # Meridian Spire - Executive Gallery
  199: {bgm: "Mood - Tension", bgs: "Glassfall Bleed", bgs_volume: 65, rain: false}          # Meridian Spire - Dark Stone Core
  959: {bgm: "Town - Zenith", bgs: ""}                                                       # Skyport Customs
```

---

## 4. Verified Events, Shops, Pickups & Canon Lore Notes

All 9 maps use **zero invented switches/variables**, **zero Nurse Joy (`NPC 16`) sprites**, **zero fourth-wall meta-dialogue (`Act I / Act III`)**, and verified canon dates (`AF 118` Zenith Charter, `AF 241` Meridian Spire HQ, non-spoiler `House Halcyon`):
- **`166` Reyes Cellar (`story/23_SCRIPT_CH4.md`):** Cipher chalkboard `[8,2]`, tidal chart `[10,2]`, framed photo `[6,3]`, dispatch table `[9,7]`, Hollow grunts `[6,8]`/`[11,9]`, pickup `NETBALL` at `[3,9]` *(note: `story/23_SCRIPT_CH4.md:486` uses `NET BALL ×2` if upgraded in Ch4 script)*.
- **`184` Lumen Arcade Dept. Store 2F:** Enclosed `0x80` TM & Evo counter (`NPC 22` at `[4,3]`: `TM17`, `TM73`, `TM10`, Evo Stones, `LINKINGCORD`) + Vitamin counter (`NPC 17` at `[15,3]`: `HPUP`, `PROTEIN`, `IRON`, `CALCIUM`, `ZINC`, `CARBOS`) + Plush Collector, Barista & Battle Shopper.
- **`194` Council Ward / `197` Council Chamber:** `FULLHEAL` at `194 [43,35]`; AF 118 Founders' Orrery & Charter/Delegation marble statue plaques (`197 [11,12]`, `[19,12]`).
- **`195` Spire District / `198` Executive Gallery / `199` Dark Stone Core:** `XSPEED` at `195 [4,44]`; AF 241 Spire Foundation plaque; Aurelian Artifact Case, Gilded King Mural & Lattice Telemetry Console (`198 [22,6]`); `199 [12,12]` Dark Stone Core pedestal (`lm_cradle_cracked`) + 3 real hardware consoles ready for Act IV climax.
- **`196` Skyport Terrace / `959` Skyport Customs:** `HYPERPOTION` at `196 [4,29]`; solid Static Tunnels Headhouse steel door `[35,30]`; `959` enclosed brass-mahogany Airship Purser booth (`NPC 12` at `[8,3]`), public Airship Route Map `[13,2]`, and spacious waiting lounge.
