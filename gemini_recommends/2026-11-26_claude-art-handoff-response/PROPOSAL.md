# Claude Real-Engine Art Handoff (`1382f18`) — All 4 Art Deliverables Shipped

**Date:** 2026-11-26  
**Responds to:** `art/HANDOFF_GEMINI.md` (`1382f18`, real-engine `artcheck` & `expr` captures)  
**Verification:** `python3 -I tools/check_art_wiring.py --quiet` → **`0 error(s), 0 gap(s)` (`EXIT=0`)**; all 7 PNGs verified **`exact2x=True`, `semi_alpha=0`**, 100% dual-synced between `graphics/` and `art/out/Graphics/`.

---

## Delivered Files (All Already Committed in `graphics/` & `art/out/Graphics/`)

| # | Asset(s) | Dimensions | Spec / Fix Summary |
|---:|---|---|---|
| **1** | `Trainers/FESTIVAL_VENAM.png` | `2560×160` (`16f`) | Restored warm chestnut-brown irises (`#984e26` / `#5c2a16`) + crisp white sclera on ALL 16 frames (`0–15`), fixing blank white eye slits on rest frames `0–4` and `10–15`. |
| **2** | `Trainers/PARTNER_GIRATINA.png`<br>`Trainers/PARTNER_GIRATINA_back.png`<br>`Characters/trainer_PARTNER_GIRATINA.png` | `2560×160` (`16f`)<br>`800×160` (`5f`)<br>`384×384` (`4×4`) | Closes the **last remaining `ERROR` in `tools/check_art_wiring.py`**! Built from official Gen 5 Giratina-Origin (`Form = 1`) pixel art (100% unscaled 1:1 Front + outline-preserved coiled-surge Back + pixel-exact 4-dir Overworld) with animated Distortion shadow wisps and **ZERO Poké Ball** (pairs with `012_Bridge_WildAllyPartner.rb`). |
| **3** | `Characters/PLAYER_A_surffish_offset.png`<br>`Characters/PLAYER_B_surffish_offset.png` | `384×320` (`4×4` of `96×80`) | Seated surf-straddle lower body (`_surf.png`) combined cleanly with casting upper torso, arms & fishing rod (`_fish_offset.png`) across all 4 directions × 4 frames (`exact2x=True`). Ready for Claude to wire `:surf_fish` in `plugins/Prismfall Core/026_PlayerLooks.rb`. |
| **4** | `Windowskins/speech hgss 1.png` | `96×48` | Centered symmetric Prismfall HGSS-style speech skin: `16px` dark/gold border left (`0..15`) & mirrored right (`80..95`), pure `#f8f8f8` interior across `x=16..79` (centered for BOTH Essentials `32,16,16,16` and `40,16,16,16` `@skinrect` slicing — eliminates the right-side grey band on every message box!). |

## Optional Wiring Snippet for Claude (`plugins/Prismfall Core/026_PlayerLooks.rb`)

```ruby
# Point :surf_fish at the dedicated seated surf-fishing sheets:
#   PLAYER_A_surffish_offset.png / PLAYER_B_surffish_offset.png
```
