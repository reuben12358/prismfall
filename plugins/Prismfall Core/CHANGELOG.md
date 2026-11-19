# Prismfall Core - changelog

Notes between workstreams. Newest first. Not loaded by the PluginManager (only .rb files are).

## 2026-11-19 (later still) - story editor: narrative data for the Gym 1 / Gym 2 swap (SPINE Revision 14)
- `012_Narrative_Data.rb` `WARDEN_CONSENT`: rows 1-2 swapped (Dorian `choice(:ch5_lowlight_testimony) != :mourner`, then
  Tamsin `choice(:ch2_tamsin) != :keep_secret`) so the list follows `GYMS` order again. Choice descriptions now say Ch2 for
  `:ch3_juno_talk` and Ch3 for `:ch2_tamsin` / `:ch2_matriarch`. **No key renamed.** `ruby -c` OK.
- Still to do in Core (design/SWAP_GYM1_GYM2.md §7): `FIELD_MOVE_BADGES[:CUT]` 1 -> 2 (Cut is given after Tamsin's badge).

## 2026-11-19 (later) - trainer workstream: Gym 1 / Gym 2 swap (SPINE Revision 14)
- `001_Config.rb` `GYMS`: index 1 is now **Dorian, Saltmere, Normal, :GRAND_STAGE, cap 15, `double: false`**; index 2 is
  **Tamsin, Briarwick, Bug, :SILKWOOD, cap 19, `double: true`**. Trainer IDs are unchanged (`[LEADER_DORIAN,Dorian,0]`,
  `[LEADER_TAMSIN,Tamsin,0]`), so PBS references keep working; badge 1 is now Dorian's, badge 2 Tamsin's.
- `003_Badges_Gyms.rb` `gym_battle`: `GYMS[:double]` is now authoritative: `true` sets "double", `false` sets "single"
  (so an old event that still calls `setBattleRule("double")` before Gym 1 gets the single battle the story wants); no
  key leaves the event's rule. The `double:` argument still overrides.
- **Map events must swap numbers** (logged in `mapgen/REQUESTS.md`): the Loomhouse (130) calls `gym_battle(1)` and must call
  `gym_battle(2)`; the Pell Playhouse (150) calls `gym_battle(2)` and must call `gym_battle(1)` and can drop its
  `setBattleRule("double")`. Until then each gym starts the other Warden.
- Anything else keyed on gym *number* for these two (Field Notes order, badge names, HM badge counts in
  `FIELD_MOVE_BADGES`: Cut was badge 1 from Briarwick's Cutter's House) needs the story / systems owner's check.

## 2026-11-19 - trainer workstream: gym double battles
- `001_Config.rb`: `GYMS` entries for Gyms **2, 6, 11, 16, 17** carry `double: true` (the story has all five as double
  battles; the teams in `pbs/trainers.txt` are tuned for it, see `design/TRAINER_FIELD_PLAYBOOK.md`).
- `003_Badges_Gyms.rb`: `Prismfall.gym_battle(n, ..., double: nil)`. With the default `nil` it sets the `"double"` battle
  rule for those gyms; `double: true` / `double: false` force it for any gym.
- **Backward compatible.** Existing calls need no change. An event that already called `setBattleRule("double")` (or set
  any size rule) before `gym_battle` keeps its own rule. Gym 2's event used to rely on that; it may drop the rule now.
- A player with a single able Pokemon: Essentials shrinks a double to 1v2 on its own, as before.
- Checked in the headless harness (`tools/harness/run_trainers.rb`): Gyms 2, 6, 11, 16, 17 start 2v2, the others 1v1.
