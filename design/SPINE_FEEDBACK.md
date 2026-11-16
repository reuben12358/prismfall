
## From: Tech integration lead (EBDX Bridge / docs) — 2026-11-15
1. **"Prismfall EBDX Bridge — Requires EBDX" vs. "fallback when EBDX is absent".** Essentials' PluginManager
   hard-errors when a `Requires` plugin is missing (`sortLoadOrder`: "Plugin '…' requires plugin '…'"), so with
   `Requires = Elite Battle: DX` the bridge's vanilla fallback can never load. Proceeded as written (meta.txt has
   `Requires = Elite Battle: DX,1.4.7` + `Requires = Prismfall Field Effects`); the vanilla code is present and
   guarded. Suggest changing the SPINE line to `Optional = Elite Battle: DX,1.4.7` (loads after EBDX if present,
   no error if absent). SETUP.md §4 documents the one-line switch.
2. **Consider the Open-Source EBDX Renovation Project (ChromeValiant, Eevee Expo res. 1831, v4.0 Oct 2026)** as the
   EBDX baseline: it is a fork of the LOCKED Manurocker95 port with the v21 frame-rate/lag fixes, a 60 FPS cap,
   animated Gen 1–9 sprites, SOS allies and HP-threshold scripting. Unverified: its meta.txt Name and whether
   `BattleSceneRoom#reconfigure` / `Battle::Scene#loadBackdrop` are unchanged (the bridge depends on both).
3. **Boss battles (rev. 2 §4):** EBDX's boss module gives stat boosts/immunities only — no multi-bar HP. Rejuvenation-
   style multi-bar bosses need custom code (Core).

## From: World & level design lead — 2026-11-15
1. **Gym puzzle state needs RMXP switches/variables.** Requesting the block **301–400** (gym n uses 300+5n … 300+5n+4; Gym 1 = 305–309 … Gym 18 = 390–394) for FLAGS.md. It sits outside the story's 101–300 range. (Core's "systems use save data, not switches" rule can't apply to event-built puzzles.)
2. **Aurelia location.** Revision 2 put the Undercity/Nadir beneath Lumen (north-central). WORLD.md therefore places drowned Aurelia under Underveil on the **north** coast below Zenith's cliffs. 00_OVERVIEW says the Fault drains the **south** coast. Story team: please pick one (World is easy to flip).
3. **Rock Climb** has no `Settings::BADGE_FOR_*` constant or field handler in v21. Core needs to add `BADGE_FOR_ROCKCLIMB = 10` plus a cliff-event helper (WORLD.md §4).
4. **Boss battles:** see the Tech lead's note #3. GYM_PUZZLES marks Ilsa/Celestine "multi-bar boss style (Hard)". That needs Core's custom multi-bar code.
- Update (tech lead, 2026-11-15): evaluated the Renovation fork (cloned to /home/claude/ref/ebdx_renovation, commit 452d27ca).
  Plugin Name still `Elite Battle: DX` (v4.0, Essentials 21.1); bridge and Core hooks are API-compatible. SETUP.md now
  recommends it (option A), with Manurocker95's repo as the fallback (option B). Its Gen 9 Pack is 3.3.8 (ours: 3.2.5):
  validators currently target /home/claude/ref/ebdx/PBS; consider re-validating trainers/encounters against
  /home/claude/ref/ebdx_renovation/PBS.
