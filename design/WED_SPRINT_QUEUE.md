# Wednesday sprint queue (agents resume after the Nov 25, 10am PT reset)

Work that review verdicts accepted but held for the agents (or Claude on plan quota). Oldest first; strike through when done.
Source: `gemini_recommends/REVIEW.md`.

## Bosses and battle engine (from the Acts III–V audit, §1.3–1.5)
1. Register the seven missing late-game multi-bar bosses: Ch10 Loyal Three (triple), Ch14 Groudon (Undersands 783), Ch15 Giratina (Altered → Origin), Ruin R1 `GIRATINA_ORIGIN_TRIAL` (ends when the PC holds back for a turn), Ch18 Pecharunt (Lightless Deep), Ch19 Wyrmrest Reshiram on `:DRAGONS_DEN` (when `:war_legend == :neither`), Ch21 Valen's Zygarde (Complete on the final bar), Ch21 Silvally (bar-3 regen unless the Fallen-Kestrel conduit breaks).
2. Arceus: a `:gym_order` rotation for `:PRISM_ARENA`, so each bar cycles its trio's three gym fields while they say their vows (11_FINALE_LINES).
3. Tag battles: allow one Mega per trainer (decision in REVIEW.md). Engine change in the Mega plugin, plus a harness check.
4. Kyogre (`:KYOGRE_ISENMAR`) balance at cap 55 (BALANCE §9d): harness round 4.

## Teams and hooks (§3.2)
5. Partner teams: Redeemed Kestrel for Ch21 (3 mons, Lv 95–97, matching RIVAL_JUNO 70–72); Rook for the Ch16 Casting Floor.
6. Ogerpon into Juno's J4 team (RIVAL_JUNO 40–42) when `OGERPON_TRUSTED`: a party hook at load, like the starter swap.
7. Aurelia (824–826): `:WATER_SURFACE` trainer-field overrides for Amaria and Titania (CAMEOS).
8. Ruin Route Inverse overlays: Ruin Gym 16 Nyx, Ruin Gym 17 Celestine (on the last mon), Ruin R7 Theodric.
9. Ch11 harpooners (ISENMAR_SOLDIER_M/F) at Lv 48–52.

## The Wednesday master audit (gemini_recommends/2026-11-22_wednesday-claude-sprint-master-audit)
11. Work through Parts A–J in order (P0 → P1 → P2), skipping what REVIEW.md marks done (E1.1, A7, A13, A15-255, G2) and what it routes to Gemini (Gemini-owned layouts). Part D (staged transitions) is the transitions agent's; Part C3 follows REVIEW.md's economy decision.
12. Add a post-paint BFS reachability check to `mapgen/build.py`, and gate packaging on `export_tilesets_rxdata.py --check` (stops the A9–A11 and E1.1 classes of bug recurring).

## Maps (pass 2, plan quota only)
10. `mapgen/REFINE_QUEUE.md`, including the stage-direction pass.

## Added 2026-11-22 (Gemini backlog pass)
- **Cutscene agent:** the P0 engine fixes from `gemini_recommends/2026-11-22_rejuv-v14-cutscene-cinematics-spec` (letterbox/bust lifecycle, input lock, fade/tint stacking) come before any new scene. The two-pillar laws are the style rule.
- **Audio agent:** the v4.3 WIRING_SPEC: `design/MAP_AUDIO.yaml` → mapgen BGS, the trainer-type BGMs, the ME/SE hooks, and a selftest-safe `VoiceTicker` (014_Portraits.rb). Then the cutscene audio matrix.
- **Codex/teams agent:** the class line on Codex cards (CODEX_SPEC), post-game rematch tables (STORY_REMATCHES), and gauntlets. G1 goes in the Ch14+ hub, not Ch13.
- **Density (see `design/DENSITY_STANDARD.md`):** Wave 0, the Ch5 rescue (softlocks, the 5 Gala/Lift trainers, 16–18 Lock Road and Circuit trainers). Wave 1: Slivers (`Prismfall::Slivers` counter + exchange), the Trading Chain, the Mystery Egg, and badge overlays 5–9. Then retrofit Ch6–13 trainers to the floor.
