# Prismfall Core - changelog

Notes between workstreams. Newest first. Not loaded by the PluginManager (only .rb files are).

## 2026-11-19 - trainer workstream: gym double battles
- `001_Config.rb`: `GYMS` entries for Gyms **2, 6, 11, 16, 17** carry `double: true` (the story has all five as double
  battles; the teams in `pbs/trainers.txt` are tuned for it, see `design/TRAINER_FIELD_PLAYBOOK.md`).
- `003_Badges_Gyms.rb`: `Prismfall.gym_battle(n, ..., double: nil)`. With the default `nil` it sets the `"double"` battle
  rule for those gyms; `double: true` / `double: false` force it for any gym.
- **Backward compatible.** Existing calls need no change. An event that already called `setBattleRule("double")` (or set
  any size rule) before `gym_battle` keeps its own rule. Gym 2's event used to rely on that; it may drop the rule now.
- A player with a single able Pokemon: Essentials shrinks a double to 1v2 on its own, as before.
- Checked in the headless harness (`tools/harness/run_trainers.rb`): Gyms 2, 6, 11, 16, 17 start 2v2, the others 1v1.
