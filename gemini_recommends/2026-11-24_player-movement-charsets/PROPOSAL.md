# Player A & Player B Full Movement Charsets (`_run`, `_bike`, `_surf`, `_fish_offset`) — Wiring Proposal

- **Date:** 2026-11-24
- **Author:** Gemini (Player Movement Charset Specialist)
- **Status:** All 8 movement charsets authored, visually inspected, QA-verified (`8/8 PASS`), and dual-synced byte-identically on disk in both `graphics/Characters/` and `art/out/Graphics/Characters/`. **No files in `pbs/` or `plugins/` were edited by this drop.**
- **Proof Sheet:** `previews/111_player_movement_charsets_proof.png`
- **Interactive Preview Studio:** `/tmp/prismfall_player_movement_studio.html` (87 KB self-contained offline studio; Playwright verified `0` console errors / `0` page errors)

---

## What

Adds all **8 missing Essentials v21.1 player movement overworld charsets** for both protagonists (`PLAYER_A` and `PLAYER_B`), matching their canonical walk sheets (`graphics/Characters/PLAYER_A.png` and `PLAYER_B.png`) at 100% exact `2×` pixel-locked Gen 5 B2W2 resolution:

- **Run:** `PLAYER_A_run.png`, `PLAYER_B_run.png` (`128×192`, `32×48` cell / `16×24` native) — forward-leaning athletic B2W2 sprint cycle with pumping bent elbows, wide diagonal side-stride, alternate back heel-kick showing soles, and wind-swept hair/ponytail motion.
- **Bike:** `PLAYER_A_bike.png`, `PLAYER_B_bike.png` (`192×192`, `48×48` cell / `24×24` native) — custom touring bicycles (cobalt-silver frame for Player A; burnt-orange & pearl-white frame for Player B), circular `6×6` native wheels with 4-phase rotating spokes, gold headlight, red taillight, chrome handlebars, and alternate pumping pedals/knees.
- **Surf:** `PLAYER_A_surf.png`, `PLAYER_B_surf.png` (`128×192`, `32×48` cell / `16×24` native) — seated/riding posture matching `boy_surf.png`/`girl_surf.png` exact foot/hip Y anchor (`y=21` native on cols 0–1, buoyant `1px` crest lift to `y=20` on cols 2–3 synced with `base_surf.png`'s wave cycle).
- **Fish (`_offset`):** `PLAYER_A_fish_offset.png`, `PLAYER_B_fish_offset.png` (`384×320`, `96×80` cell / `48×40` native) — full Essentials `pbFishingBegin` (`C3→C2→C1→C0`) & `pbFishingEnd` (`C0→C1→C2→C3`) casting and tugging sequence with sleek 2px B2W2 fishing rods, anchored at exact Essentials `_offset` ground origin (`ox=48, oy=64` = `walk + (+32, +16)` native 2×) for **zero teleporting** when starting or ending fishing.

## Why

Currently, `plugins/Prismfall Core/026_PlayerLooks.rb` (lines 6 & 41–46) keeps running on the walk sheet and leaves `CycleCharset`, `SurfCharset`, `DiveCharset`, `FishCharset`, and `SurfFishCharset` falling back to stock Essentials Red/Leaf (`boy_bike`, `boy_surf`, `boy_fish_offset`, `girl_bike`, `girl_surf`, `girl_fish_offset`). Wiring these 8 sheets removes every stock Red/Leaf fallback so both Prismfall protagonists retain 100% consistent visual identity across walking, running, cycling, surfing, diving, and fishing.

## Where It Plugs In

Two drop-in wiring paths are provided below depending on whether Claude maintains player metadata directly in `pbs/metadata.txt` or continues routing through `plugins/Prismfall Core/026_PlayerLooks.rb` (which currently intercepts `GameData::PlayerMetadata` for player IDs `1` & `2` so stock Essentials `PBS/metadata.txt` doesn't need to be forked):

### Option A — Ready-to-Drop `pbs/metadata.txt` `[1]` & `[2]` Player Metadata Block

Verified against Essentials v21.1 stock `PBS/metadata.txt` keys (lines 15–33):

```ini
#-------------------------------
[1]
TrainerType = PLAYER_A
WalkCharset = PLAYER_A
RunCharset = PLAYER_A_run
CycleCharset = PLAYER_A_bike
SurfCharset = PLAYER_A_surf
DiveCharset = PLAYER_A_surf
FishCharset = PLAYER_A_fish_offset
SurfFishCharset = PLAYER_A_fish_offset
#-------------------------------
[2]
TrainerType = PLAYER_B
WalkCharset = PLAYER_B
RunCharset = PLAYER_B_run
CycleCharset = PLAYER_B_bike
SurfCharset = PLAYER_B_surf
DiveCharset = PLAYER_B_surf
FishCharset = PLAYER_B_fish_offset
SurfFishCharset = PLAYER_B_fish_offset
```

*(Note: `trainer_PLAYER_A.png` and `PLAYER_A.png` are byte-identical `128×192` sheets, as are `trainer_PLAYER_B.png` and `PLAYER_B.png`; either `PLAYER_A` or `trainer_PLAYER_A` resolves cleanly for `WalkCharset`.)*

### Option B — Exact Unified Diff for `plugins/Prismfall Core/026_PlayerLooks.rb`

Because `026_PlayerLooks.rb` currently overrides `GameData::PlayerMetadata#trainer_type`, `#walk_charset`, and `#run_charset` at runtime (and `pbs/metadata.txt` is not currently forked in the Prismfall repo), extending `026_PlayerLooks.rb` activates all 8 sheets immediately with safe `pbResolveBitmap` fallback guards:

```diff
--- a/plugins/Prismfall Core/026_PlayerLooks.rb
+++ b/plugins/Prismfall Core/026_PlayerLooks.rb
@@ -4,12 +4,32 @@
 # metadata 1/2 (Red/Leaf). This points those two at Prismfall's own trainer types and
 # overworld sheets when the art and the PBS trainer types are installed; otherwise the stock
-# ones stay. Running uses the walk sheet; cycle/surf/fish sets stay stock until Prismfall versions exist.
+# ones stay. All movement sheets (walk/run/bike/surf/dive/fish) resolve per-slot with safe fallback.
 #===============================================================================
 module Prismfall
   PLAYER_LOOKS = {
-    1 => { :trainer_type => :PLAYER_A, :walk => "trainer_PLAYER_A" },
-    2 => { :trainer_type => :PLAYER_B, :walk => "trainer_PLAYER_B" }
+    1 => {
+      :trainer_type => :PLAYER_A,
+      :walk         => "trainer_PLAYER_A",
+      :run          => "PLAYER_A_run",
+      :cycle        => "PLAYER_A_bike",
+      :surf         => "PLAYER_A_surf",
+      :dive         => "PLAYER_A_surf",
+      :fish         => "PLAYER_A_fish_offset",
+      :surf_fish    => "PLAYER_A_fish_offset"
+    },
+    2 => {
+      :trainer_type => :PLAYER_B,
+      :walk         => "trainer_PLAYER_B",
+      :run          => "PLAYER_B_run",
+      :cycle        => "PLAYER_B_bike",
+      :surf         => "PLAYER_B_surf",
+      :dive         => "PLAYER_B_surf",
+      :fish         => "PLAYER_B_fish_offset",
+      :surf_fish    => "PLAYER_B_fish_offset"
+    }
   }
 
   def self.player_look(id)
@@ -22,6 +42,11 @@ module Prismfall
     end
     return @player_look_ok[id] ? look : nil
   end
+
+  def self.resolve_player_sheet(look, key, fallback)
+    name = look[key]
+    return (name && pbResolveBitmap("Graphics/Characters/#{name}")) ? name : fallback
+  end
 end
 
 module GameData
@@ -38,11 +63,40 @@ module GameData
       return look ? look[:walk] : pf_look_walk_charset
     end
 
-    # no Prismfall running sheet yet: run in the walk sheet rather than switch to stock Red/Leaf
     alias pf_look_run_charset run_charset unless method_defined?(:pf_look_run_charset)
     def run_charset
       look = Prismfall.player_look(@id)
-      return look ? (look[:run] || look[:walk]) : pf_look_run_charset
+      return look ? Prismfall.resolve_player_sheet(look, :run, look[:walk]) : pf_look_run_charset
+    end
+
+    alias pf_look_cycle_charset cycle_charset unless method_defined?(:pf_look_cycle_charset)
+    def cycle_charset
+      look = Prismfall.player_look(@id)
+      return look ? Prismfall.resolve_player_sheet(look, :cycle, pf_look_cycle_charset) : pf_look_cycle_charset
+    end
+
+    alias pf_look_surf_charset surf_charset unless method_defined?(:pf_look_surf_charset)
+    def surf_charset
+      look = Prismfall.player_look(@id)
+      return look ? Prismfall.resolve_player_sheet(look, :surf, pf_look_surf_charset) : pf_look_surf_charset
+    end
+
+    alias pf_look_dive_charset dive_charset unless method_defined?(:pf_look_dive_charset)
+    def dive_charset
+      look = Prismfall.player_look(@id)
+      return look ? Prismfall.resolve_player_sheet(look, :dive, pf_look_dive_charset) : pf_look_dive_charset
+    end
+
+    alias pf_look_fish_charset fish_charset unless method_defined?(:pf_look_fish_charset)
+    def fish_charset
+      look = Prismfall.player_look(@id)
+      return look ? Prismfall.resolve_player_sheet(look, :fish, pf_look_fish_charset) : pf_look_fish_charset
+    end
+
+    alias pf_look_surf_fish_charset surf_fish_charset unless method_defined?(:pf_look_surf_fish_charset)
+    def surf_fish_charset
+      look = Prismfall.player_look(@id)
+      return look ? Prismfall.resolve_player_sheet(look, :surf_fish, pf_look_surf_fish_charset) : pf_look_surf_fish_charset
     end
   end
 end
```

---

## Verified Asset Manifest & QA Audit (Dual-Synced Byte-Identical SHA-256)

Every file below exists byte-identically in both `graphics/Characters/` and `art/out/Graphics/Characters/`:

| File | Sheet Size | Cell (Native 1×) | Anchor `(ox, oy)` | `exact2x` | Semi-Alpha | Orphans | `L≠flip(R)` | Colors | Bytes | SHA-256 |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| `PLAYER_A_run.png` | `128×192` | `32×48` (`16×24`) | `(16, 48)` | `True` | `0` | `0` | `0px` | `11` | `2,647` | `c9945ab86f7107a53252108a00ea9b31167e1c3ba8173a85e03c9a180e1e6f5b` |
| `PLAYER_A_bike.png` | `192×192` | `48×48` (`24×24`) | `(24, 48)` | `True` | `0` | `0` | `0px` | `15` | `3,300` | `7f8480606bc9654e53671bc34ff26de1edc9a929886122179fb51e02be5181d7` |
| `PLAYER_A_surf.png` | `128×192` | `32×48` (`16×24`) | `(16, 48)` | `True` | `0` | `0` | `0px` | `11` | `2,305` | `326c646f8a1a7c02d602a00d09d667d7a30401b965bbac5bf30447f7303a72e3` |
| `PLAYER_A_fish_offset.png` | `384×320` | `96×80` (`48×40`) | `(48, 64)` | `True` | `0` | `0` | `0px` | `12` | `4,817` | `7122a56d30047e34dc4db91b4ee42b2acbf0735dc46e851f12bed7a51864fc07` |
| `PLAYER_B_run.png` | `128×192` | `32×48` (`16×24`) | `(16, 48)` | `True` | `0` | `0` | `0px` | `13` | `2,833` | `02356aff6b6810adb01e8a7d7201ac9ab976e1be55a047cba1304b8c1ade2796` |
| `PLAYER_B_bike.png` | `192×192` | `48×48` (`24×24`) | `(24, 48)` | `True` | `0` | `0` | `0px` | `17` | `3,771` | `54f996995c31d084ec510124c107d214a57c9488b27d90916bd18054fd2c2fc7` |
| `PLAYER_B_surf.png` | `128×192` | `32×48` (`16×24`) | `(16, 48)` | `True` | `0` | `0` | `0px` | `13` | `2,795` | `d79d7caf6af28262956ba13c976e510c050c548c14bb8572f3c0b4148962ae99` |
| `PLAYER_B_fish_offset.png` | `384×320` | `96×80` (`48×40`) | `(48, 64)` | `True` | `0` | `0` | `0px` | `14` | `5,383` | `0340f9232e2a0d84ae0cfec598f329e317d355da18415ae4d416e4f00fa958ba` |

## Sources & Engine References

- Canonical protagonists (locked reference): `graphics/Characters/PLAYER_A.png`, `graphics/Characters/PLAYER_B.png`, `graphics/Portraits/PLAYER_{A,B}.png`, `graphics/Trainers/PLAYER_{A,B}.png`.
- Essentials v21.1 geometry & engine anchor templates verified against `/home/antigravity/pf_engine_run/game/Graphics/Characters/{boy,girl}_{run,bike,surf,fish_offset}.png`, `base_surf.png`, `PBS/metadata.txt`, and `Sprite_Character` / `Sprite_SurfBase` / `pbFishingBegin` (`Data/Scripts.rxdata`).
- Project art contract: `art/HANDOFF_GEMINI.md`.
