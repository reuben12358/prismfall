
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

## From: World & level design lead — 2026-11-16 (Rev 5–6 pass)
1. **Ashkaar's seat** is not named in the lore. WORLD.md §8 provisionally makes it **Pyre Keep on Cindervault's caldera rim** (Wyrmrest stays the pass fortress). Story team: confirm or move it.
2. **Antumbra's seat** is provisionally the **Palace of Glass in the Speculum** (Lucent's inverted reflection), with the Veiled Synod's court there.
3. **War geography** (§9): Ashkaar and Isenmar don't share a land border on the map, so the front is the north-east coast (Rime Narrows / Cinder Cape), with besieged **Skaldfast** and the **Shattered Ice** climax field. All names are provisional.

## From: World & level design lead — 2026-11-16 (Rev 9 borderlands)
Story impacts (full detail in WORLD.md §10, data in maps.json `borderlands`):
1. **Ch4 (Saltmere → Ebbmouth)** now passes R5 Frostflat Causeway → **Frostwick (570, new borderland village)** → The Rimewood (562) → R6 Gullcry Cliffs. 04_ACT_I's border marker ("both arms + Meridian sunburst") is the Border Stones on R5, and the Border House in Frostwick stamps the sunburst over both seals. New NPCs for the story team to voice: Brannagh and Halvard (sidequest "The Two Hearths"), the Meridian clerk, the Frostwick huscarl/forester. **Map Builder:** `mapgen/specs/560_route5_route6.yaml` still joins 560 W → 561. It must now be 560 W → 570, 570 N → 562, 562 N → 561 S. 561 no longer has an E edge.
2. **Act II:** Lumen → Duneholt goes through Copperdune, Duneholt → Mirefen through Charwell, and Mirefen → Cindervault through Scaldwater (whose mercenary recruiting is a war seed). Cindervault → Ironreach uses the Ironway. R17 "Lift Road" is now **The Rootdeep** (Nadir/Elowen cave route) with the town Lanternroot.
3. **Antumbra** has a second stable gate besides Mirror Mere: the **Grave Glass** in the Obsidian Barrows (Ossaria), with the town Vigil. Act IV legs 12→13, 13→14 and 14→15 walk through it. Story team: confirm, or I'll swap in an airship jump.
4. **War:** no Ashkaar–Isenmar land border. The war is across the Shattered Ice strait between Isenmar's Rime Isles (Skaldfast) and Ashkaar's Cinder Cape. Ashkaar's road to the front runs through the Cinderglass Barrens and Glasswake (border M). The previous "NE coast / Rime Narrows" wording is replaced.
5. **Crownhaven** is entered only via the Pilgrim Pass (K) from Wyrmrest, with the pilgrim town Pilgrim's Rest. This matches the lore that Wyrmrest guards "the only overland pass".
All 15 new borderland town names are provisional.
