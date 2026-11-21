# Proposal: Close Multi-Bar Boss Shield Cheese, Wire Missing Finale Hooks & Expand SPINE Rev 16 Gates to Wardens 5-18

- **What:** Harden `Prismfall Bosses` against volatile/HP-setting cheese, wire four unfinished finale/boss hooks promised in `BALANCE.md`/`015_Festival_Draw.rb`, and expand `design/warden_gates.json` from Wardens 1-4 to all 18 Wardens.
- **Why:** Verified still live on commit `3a520c6`:
  1. **Multi-bar boss shield cheese & 1-HP drain bug (`plugins/Prismfall Bosses/004_Bosses_Battle.rb:16, 37-55, 169-206`):**
     - `status_immunity` only blocks primary status, Yawn, Confusion, and Attract — **Ghost Curse (25%/turn), Leech Seed (12.5%/turn), Perish Song, Destiny Bond, Endeavor, and Pain Split all bypass it**, and `:cure_status => true` on bar break only calls `pbCureStatus` (so Curse/Leech Seed persist across every bar, and 1-HP Endeavor strips an entire shield bar in one move).
     - When a boss is already at 1 HP before the bar-breaking hit, `lost = 0` overwrites `ds.hpLost = 0` (L16, L37-45), making Drain moves / Shell Bell heal 0 HP and Counter / Mirror Coat / Metal Burst deal 0 damage.
     - `104_Boss_HardWardens.rb:18` (`:versions => [0, 100]`) misses Ruin Route Hard Celestine (`version 101`, `pbs/trainers.txt:15447`).
  2. **Four unwired story/finale battle hooks:**
     - **Arceus choice-driven variants:** `015_Festival_Draw.rb:117-128` defines 5 variants (`:ARCEUS_JUDGMENT`, `:ARCEUS_GILDED`, `:ARCEUS_WAR`, `:ARCEUS_MISCALIBRATED`, `:ARCEUS_BOUND`), but `007_Bosses_Integrations.rb:9` hardcodes `FESTIVAL_BOSSES = { :ARCEUS => :ARCEUS_FINALE }` and never calls `Prismfall::Festival.arceus_variant`.
     - **Project NULL Silvally Memory re-indexing:** `design/BALANCE.md:169-172` specifies Voss/Quent's Silvally `"NULL"` switching Memory to match each `:PRISM_ARENA` Plate turn, but `136_Field_PrismArena.rb` only attunes `:MULTITYPE` (`:RKSSYSTEM` unimplemented).
     - **Ruin R1 Reflection party mirror:** `pbs/trainers.txt:15678` & `BALANCE.md:191` rely on a Core `:on_trainer_load` hook mirroring `$player.party` for `[REFLECTION,???]`, which doesn't exist yet.
     - **Missing `:MOURNER_TREVENANT` boss registration** (`pbs/trainers.txt:10092`) and **Kestrel Ch21 post-SF Morwen's Ring partner branch** (`MEGA_EVOLUTION.md:56` vs `012_Narrative_Data.rb:101`).
  3. **SPINE Rev 16 validation stops at Warden 4 (`design/warden_gates.json:32-45`):** Wardens 1-4 pass cleanly, but Wardens 5-18 are completely unvalidated. Five Ch5+ EventMons in `plugins/Prismfall Trials/131_EventMons_Later.rb` currently violate Rev 16's 2-gym counter horizon (R4):
     - `OS_STUNFISK` (Galarian Ground/Steel, Ch7, L58) -> Poison-immune + SE vs Gym 6 Corvin
     - `OS_TRAPINCH` (Ground, Ch6, L55) -> SE vs Gym 6 Corvin
     - `AS_NOIBAT` (Flying/Dragon, Ch8, L40) -> SE vs Gym 8 Kaito & Gym 9 Juno
     - `AS_HOUNDOUR` (Fire/Dark, Ch8, L43) -> SE vs Gym 9 Juno
     - `IS_CETODDLE` (Ice, Ch11, L78) -> SE vs Gym 11 Odessa
     *(Also keep an eye on `524` `HeadbuttHigh` giving 500-BST Heracross/Pinsir at 1 badge and `528` `SANDYGAST` being Normal-immune against Dorian's Minccino/Spinda.)*
  4. **Fresh EBDX Renovation boot fix (`plugins/~Prismfall Base Fixes/meta.txt`):** Because `~` sorts alphabetically last, double-check load order against EBDX `UI Fixes.rb` line 4 (`class PokemonSprite < SpriteWrapper`) or ship an explicit installer patch helper (currently `run_engine_capture.sh:101` patches `UI Fixes.rb` with `sed -i`).
- **Where it plugs in:** `plugins/Prismfall Bosses/{004_Bosses_Battle.rb,007_Bosses_Integrations.rb,104_Boss_HardWardens.rb}`, `plugins/Prismfall Field Effects/136_Field_PrismArena.rb`, `plugins/Prismfall Core/012_Narrative_Data.rb`, `design/warden_gates.json`, `plugins/Prismfall Trials/131_EventMons_Later.rb`.
- **Sources:** Direct code audit of commit `3a520c6` against `design/SPINE.md` Rev 16/21/23, `design/BALANCE.md`, `design/BOSSES.md`, and `design/MEGA_EVOLUTION.md`.
