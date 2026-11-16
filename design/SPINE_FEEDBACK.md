
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
