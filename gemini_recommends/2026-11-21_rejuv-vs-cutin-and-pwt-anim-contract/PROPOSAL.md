# Art & Engine Contract: Rejuvenation-Style VS Battle Cut-In + B2W2 PWT Trainer Intro Poses

- **Status:** **ART IN PROGRESS** (none of the new `vsTrainer_*` / `vsBar_*` / `vs_emblem` files or updated PWT pose strips are pushed yet — this proposal locks the exact shared asset contract before we push so Gemini and Claude build to the exact same spec!).
- **Scope:** Art-to-engine alignment for two creator visual directives shared with both agents on 2026-11-21:
  1. Replace EBDX's diagonal Pokéball split + single-trainer `integratedVS` splash with a **Pokémon Rejuvenation-style split VS cut-in** (`Player [Left] VS Opponent [Right]`, modeled after Rejuvenation's *Maël vs Eizen*).
  2. Support **Pokémon B2W2 PWT-style animated trainer intro poses** (like Lance in B2W2 PWT sweeping his cape open at battle start, then settling into a living idle loop).

---

## 1. Rejuvenation-Style Split VS Cut-In — Exact Art Contract

Gemini is producing genuine pixel-art `Graphics/Transitions/` assets (pure `2x2` uniform blocks, `semi=0`, `orphans=[]`, mirrored in `graphics/Transitions/` and `art/out/Graphics/Transitions/`) matching Essentials v21.1 & Rejuvenation conventions:

| Asset Path | Native 1x | Shipped 2x | Facing / Composition |
|---|---|---|---|
| `Graphics/Transitions/vsTrainer_PLAYER_A.png` | `128x64` | **`256x128`** | Transparent bg, chest-up dynamic battle pose gripping Poké Ball, **facing RIGHT** (left half of screen) |
| `Graphics/Transitions/vsTrainer_PLAYER_B.png` | `128x64` | **`256x128`** | Transparent bg, chest-up dynamic battle pose gripping Poké Ball, **facing RIGHT** (left half of screen) |
| `Graphics/Transitions/vsTrainer_<TRAINERTYPE>.png` | `128x64` | **`256x128`** | Transparent bg, chest-up dramatic signature pose + foreground hand/prop, **facing LEFT** (right half of screen) |
| `Graphics/Transitions/vsBar_PLAYER_A.png` / `vsBar_PLAYER_B.png` | `128x64` | **`256x128`** | Opaque horizontal speed-line energy banner (left half) |
| `Graphics/Transitions/vsBar_<TRAINERTYPE>.png` | `128x64` | **`256x128`** | Opaque horizontal speed-line energy banner in trainer's signature palette (right half) |
| `Graphics/Transitions/vs_emblem.png` | `64x64` | **`128x128`** | Transparent bg, bold slanted stylized `VS` mark centered over the seam |

### Initial Cast Wave Being Produced Now (Batch 1 — 8 Sets)
- Players: `PLAYER_A`, `PLAYER_B`
- Opponents: `RIVAL_JUNO`, `LEADER_JUNO`, `RIVAL_KESTREL`, `LARCH`, `LEADER_DORIAN`, `LEADER_TAMSIN`
- *(Subsequent major cast waves — Marisol, Voss, Rowan/Mourner, Thistle, Teo, Vesper, etc. — will drop into the exact same naming convention automatically.)*

### Suggested Runtime Behavior for Claude's Ruby VS Transition
- Trigger automatically for any trainer whose `Graphics/Transitions/vsTrainer_<TRAINERTYPE>.png` exists (falling back gracefully to standard transition for generic route trainers without VS art).
- Screen layout on `512x384` viewport (matching Rejuvenation's *Maël vs Eizen* framing):
  - Black cinema letterbox bars top & bottom (`y = 0..104` and `y = 280..384`, or semi-darkened arena behind the center band).
  - Horizontal center strip (`y = 128..256`, height `128px`):
    - Left (`x = 0..256`): `vsBar_PLAYER_<A|B>` scrolling subtly right-to-left + `vsTrainer_PLAYER_<A|B>` sliding in from left.
    - Right (`x = 256..512`): `vsBar_<OPPONENT>` scrolling subtly left-to-right + `vsTrainer_<OPPONENT>` sliding in from right.
    - Center (`x = 192..320, y = 128..256`): `vs_emblem.png` slamming in on impact with a brief white flash + subtle screen shake.
  - Below strip (`y ~ 268`): Player name centered at `x = 128`, Opponent display name centered at `x = 384`.
- **Feedback requested from Claude:** If your VS transition plugin expects a different width/height (e.g. `256x112` vs `256x128`), a different filename (e.g. `vsTrainer_<TYPE>_bar.png` or `Graphics/EBDX/Transitions/`), or `vsPlayer` vs `vsTrainer_PLAYER_A`, drop a 3-line note in `gemini_recommends/REVIEW.md` and we will match it 1:1 on install!

---

## 2. B2W2 PWT-Style Trainer Animated Intro Pose — Exact Strip Playback Contract

All major opponent battle fronts remain **`2560x160`** (`16` square frames of `160x160` = exact `2x` of `80x80` native, feet locked to native `y = 77` on every frame).

To support true **Pokémon B2W2 PWT-style animated intro poses** (like Lance sweeping open his cape at battle entry and holding his commanding dragon-master pose) without snapping back awkwardly to Frame 0:

| Frame Range | Role | Visual Content |
|---|---|---|
| **`F00..F07`** (8 frames) | **One-Shot Intro Action Pose** | Opening poised stance (`F00–F02`) -> dramatic signature flourish/cape-sweep/hat-tip/shawl-reveal (`F03–F06`) -> settle into hero pose (`F07`) |
| **`F08..F15`** (8 frames) | **Heroic Held Pose + Seamless Loop (`F15 -> F08`)** | Exact hero pose held steady with living cloth/ribbon/tassel/steam breeze, subtle glint, and natural blink |

### Suggested 5-Line EBDX Playback Hook for Claude
- When an opponent trainer enters battle with a 16-frame (`2560x160`) strip:
  - Play frames `0 -> 1 -> ... -> 7` **once** during the `"You are challenged by ..."` intro beat (at ~8–10 fps so the dramatic pose reads crisply!).
  - Once frame `8` is reached, **loop frames `8..15`** (`frame = 8 + ((frame - 8 + 1) % 8)`) until the trainer slides off-screen for send-out!
- **Compatibility note:** Existing strips already pushed (`RIVAL_JUNO`, `LEADER_JUNO`, restored Pass-1 `RIVAL_KESTREL`, restored Pass-1 `LARCH`) work cleanly with EITHER full `0..15` looping OR `0..7` -> `8..15` tail looping. As soon as our upgraded B2W2 PWT intro pose strips (`RIVAL_JUNO`, `LEADER_JUNO`, `RIVAL_KESTREL`, `LARCH`, `LEADER_DORIAN`, `LEADER_TAMSIN`) pass visual QC and are pushed, they will immediately shine under `0..7` intro -> `8..15` loop!
- **Portrait/UI safety note:** If any UI (like `014_Portraits.rb` fallback) crops frame `0` vs frame `8` of a trainer strip, note that `F08` is the canonical settled hero pose (and `F00` is the clean poised opening stance). All major cast members have dedicated `96x96` `Graphics/Portraits/` files already.

---

## 3. Current Repo Art Status (Strictly Verified Pushed vs In Progress)

- **Pushed & live on `origin/main` right now:**
  - `RIVAL_JUNO`, `LEADER_JUNO`, `PLAYER_A`, `PLAYER_B` (full packs, verified live in `j1_intro_gemini_art.gif`)
  - `RIVAL_KESTREL`, `LARCH` (full packs — **clean Pass-1 Gemini battle fronts restored at `71e134d`** + pure `generate_image` portraits + matching overworlds; ready to uncomment in `025_CharsetAliases.rb`!)
  - Badges (`icon_badges_18.png`), Field Seeds, Z-Crystals, Silk/Rime obstacles
- **Actively in progress (NOT pushed yet — will be pushed once visually approved):**
  - `LEADER_DORIAN` & `LEADER_TAMSIN` v3 (pure `generate_image` redo + B2W2 PWT intro poses + 24 portraits + overworlds)
  - B2W2 PWT intro-pose upgrades for `RIVAL_JUNO`, `LEADER_JUNO`, `RIVAL_KESTREL`, `LARCH`
  - Rejuvenation-style VS cut-in sets (`vsTrainer_*`, `vsBar_*`, `vs_emblem.png`) for all 8 core cast members
