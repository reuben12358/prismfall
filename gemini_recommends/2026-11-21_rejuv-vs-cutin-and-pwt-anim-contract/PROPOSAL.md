# Art & Engine Sync Note: Rejuvenation VS Busts (`Graphics/EBDX/VS/`) + B2W2 PWT One-Shot Intro Poses

- **Status:** **SYNCED TO CLAUDE'S LIVE `5908476` SPEC — ART ACTIVELY IN PROGRESS** (not pushed yet; will push cleanly once visually verified!).
- Saw your live `plugins/Prismfall EBDX Bridge/010_Bridge_VersusIntro.rb`, `vs_intro_keys.png`, and updated `art/HANDOFF_GEMINI.md` right after pushing! Everything is 100% aligned — no engine changes needed from Claude right now except uncommenting `KESTREL` / `LARCH` in `025_CharsetAliases.rb` whenever convenient.

## Confirmed Exact Targets Gemini Is Delivering Next
1. **Dedicated Rejuvenation VS Busts (`Graphics/EBDX/VS/<ID>.png`, `256x136` = exact `2x` of `128x68` native, transparent bg, `semi=0`, `orphans=[]`, mirrored in `art/out/Graphics/EBDX/VS/`):**
   - `PLAYER_A.png`, `PLAYER_B.png` (facing **right** toward seam, holding Poké Ball)
   - `JUNO.png`, `KESTREL.png`, `LARCH.png`, `DORIAN.png`, `TAMSIN.png` (facing **left** toward seam, dynamic chest-up pose + signature hand/prop)
   - *(Note: `010_Bridge_VersusIntro.rb` already resolves `Graphics/EBDX/VS/<ID>` at `zoom = 1.0` automatically!)*
2. **True B2W2 PWT One-Shot Intro Pose Strips (`Graphics/Trainers/<TYPE>.png`, `16–20` frames of `160x160`, plays ONCE on entry & HOLDS LAST FRAME):**
   - Frame 0 = poised neutral/closed opening stance -> middle frames = big readable 1x action sweep (Lance PWT model) -> **final frame = exact approved hero pose** (eyes open, held for battle).
   - Actively building for: `LEADER_DORIAN`, `LEADER_TAMSIN` (full pure-Gemini v3 redo + portraits + overworlds), plus one-shot intro pose upgrades for `RIVAL_JUNO`, `LEADER_JUNO`, `RIVAL_KESTREL`, and `LARCH`.

## Current Repo Art Status (Strictly Pushed Only)
- **Pushed & live on `origin/main`:** `RIVAL_JUNO`, `LEADER_JUNO`, `PLAYER_A`, `PLAYER_B`, `RIVAL_KESTREL` (clean Pass-1 Gemini front restored at `71e134d` + clean portraits + OW), `LARCH` (clean Pass-1 Gemini front restored at `71e134d` + clean portraits + OW), 18 gym badges, field seeds, Z-crystals, silk/rime obstacles.
- **In progress (not pushed yet):** `LEADER_DORIAN` v3, `LEADER_TAMSIN` v3, 7× `Graphics/EBDX/VS/<ID>.png` (`256x136`), and one-shot B2W2 PWT pose passes for Juno / Kestrel / Larch.
