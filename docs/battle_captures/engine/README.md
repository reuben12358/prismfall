# Real-engine battle captures (EBDX + Prismfall field effects)

**These are real game frames.** The engine is mkxp-z 2.4.2, built from source on Linux. It ran the Elite
Battle: DX base project with the Prismfall kit installed on top. Every frame is unmodified output of the
engine's own `Graphics.screenshot`. The only additions are the caption strip *below* each frame and, in the
GIFs, black "time skip" cards between trimmed segments.

Neither side is player-controlled: the AI picks every move (`battle.controlPlayer = true`), and battles are
started through the kit's normal calls. Rendering used Xvfb with Mesa llvmpipe (software OpenGL). Audio was
off.

These captures are **not** made on Windows, with real art, or with sound (see "Not verified").

> **Easier to follow:** `slow/` has the same three battles re-recorded with in-engine reading pacing
> (slow text, 2.5–3.5 s message holds, 1 s before each turn) as full-battle MP4s plus trimmed GIFs.
> See `slow/README.md`. The files below are the original fast captures.

## Files

| File | What it shows |
|---|---|
| `volcanic_to_ashen.gif` | Gym 7, Warden Brann, started with `Prismfall.gym_battle(7)`. The Volcanic Field intro and harsh sun (Torkoal's Drought), then Surf ×2 quenches the magma: the Bridge flashes steam-grey and the room becomes Ashen Waste. Real speed. |
| `volcanic_to_ashen_key_f00163.png` | Field intro message on the EBDX MAGMA room, with the Bridge's volcanic tone and embers. |
| `volcanic_to_ashen_key_f00247.png` | Transition progress: "Steam hisses… (1 more)". |
| `volcanic_to_ashen_key_f00268.png`, `…f00275.png` | Field-boosted Lava Plume: "The magma roared!" (Fire ×1.5) and "The lava surged!" (move ×1.5). |
| `volcanic_to_ashen_key_f00475.png` | The Bridge's transition flash, `[200,200,200]` from `001_Bridge_Config.rb`. |
| `volcanic_to_ashen_key_f00493.png` | After the change: the Ashen Waste room and the quench message. |
| `silkwood_to_ashen.gif` | Gym 1, Warden Tamsin. Forest room, sticky-web entry, Telluric Seed, Ember boosted on the silk, and the third Fire move burning the Silkwood into Ashen Waste. Two segments. |
| `silkwood_to_ashen_key_f00162/277/384/1385/1397.png` | Intro, seed activation, boosted Ember, transition flash, ash room. |
| `zekrom_boss.gif` | `Prismfall::Bosses.wild_battle(:ZEKROM_ENGINE)`: the EBDX boss databox with our 3 bar pips. Bar 1 breaks (HP refills, pip goes dark); bar 2 breaks and the boss break table changes FACTORY → SCRAPYARD (orange flash). Two segments. |
| `zekrom_boss_key_f00140/267/294/600/613/760.png` | Pips all lit, bar-1 break at 0 HP, refill, flash, Scrapyard message, one pip left. |

GIF details: frames were captured every 3rd engine frame. The GIFs use every 2nd capture at 100 ms, so they
play at real speed. They use a shared 128-colour palette (lossy); the key PNGs are full colour.

## What the engine runs confirmed

- Every Prismfall plugin loads in the real PluginManager alongside Elite Battle: DX, Luka's Scripting
  Utilities, the Gen 9 Pack and Hotfixes. That covers Core, Field Effects, the **EBDX Bridge** (its first ever
  run), Bosses, Maps, Cutscenes and Debug Tools.
- None of our plugins raised an exception in 3 engine battles, and the Bridge echoed no warnings.
- The Bridge picks the room, tone and particle FX at battle start. On every field change it rebuilds the
  room with the configured flash colour. The databox pips from `Prismfall Bosses/007_Bosses_UI.rb` render in
  the EBDX boss databox.

## Issues found (none crash the battle code)

1. **Base project, not ours: EBDX fails to load.** `Plugins/Elite Battle DX/[000] Scripts/Battle UI/UI
   Fixes.rb` line 4 has `class PokemonSprite < SpriteWrapper`. That raises "superclass mismatch" because the
   base scripts define `PokemonSprite < Sprite`, so the game stops at boot. The capture copy drops the
   superclass (`class PokemonSprite`). The same line is in both reference base projects, so check it on Windows.
2. **Kit: a fresh install crashes on New Game** (`tileset_name for nil`). The maps were regenerated on 16 Nov
   and now use tilesets 30/33/34/40 (e.g. map 109, the start map, uses 33). The base project only has tilesets
   1–25. `tools/package.sh` ships the maps but not the tileset records or `maps_out/Graphics`, and
   `mapgen/merge_tilesets.py` isn't packaged. This is in-progress map work; the captures bypass it (see below).
3. **Art: no trainer sprites** for `LEADER_BRANN` or `LEADER_TAMSIN`. EBDX logs a warning and shows no
   trainer.
4. **Config: FACTORY and SCRAPYARD share EBDX's `INDOOR` room.** That transition shows only as the flash plus
   a small tone shift (wall colour `[185,206,220]` → `[206,203,185]`). Real art or a different fallback room
   would make it readable.
5. **Latent, found by reading code (not observed):** on outdoor rooms (`:outdoor => true`, e.g.
   FLOWER_GARDEN), EBDX's `daylightTint` resets room tones whenever the weather changes, which would drop the
   Bridge's field tone until the next room rebuild.

## Capture-copy-only changes (never in the kit)

The capture copy is `/home/claude/run/game`, assembled by the script. It has these changes:

- the EBDX line from issue 1 is patched;
- `mkxp.json` gets `rubyLoadpath`, so Ruby can find `zlib.so`, and vsync is off;
- the dev-only plugin `ZZ Demo Autorun` (`tools/harness/visual/`) is installed. It skips the title, presses
  Use on message boxes (including the first-boot "N new map(s) imported" box), starts on the base project's
  map 1 instead of the kit's start map (issue 2), builds the party, starts the battle and dumps frames;
- audio calls are silenced: there is no audio device, and this engine build's `bgm_play` rejects
  Essentials' float position.

Demo parties are scripted to force the signature interaction (for example the Volcanic lead knows only
Surf). The AI chooses the actual moves.

## Re-running

```bash
cd tools/harness/visual
bash run_engine_capture.sh build        # once: clones deps from GitHub, builds mkxp-z (~2 min)
bash run_engine_capture.sh assemble     # copies the base project + dist overlay + autorun into $RUN/game
bash run_engine_capture.sh run volcanic # or: run silkwood,zekrom   (env DEMO_TURNS=n caps turns)
bash build_captures.sh                  # GIFs + key PNGs into this folder
```

- The first boot of a fresh copy compiles PBS and plugins, which takes a few minutes.
- Frames land in `$RUN/captures_keep/<battle>/`, and the per-turn log in `$RUN/captures_keep/*_demo.log`.
- Battles aren't seeded, so a re-run gives different frame numbers. Update the `--key` indices in
  `build_captures.sh` to match.
- The `assemble` and `run` steps were re-tested from scratch. The `build` step is transcribed from the
  session that produced the binary.

## Not verified

Windows, a real GPU, or how EBDX looks at full speed. Audio. Custom field backdrops (none exist yet: every
field uses a tinted stock EBDX room). Fields other than Volcanic, Silkwood, Ashen Waste, Factory and
Scrapyard. PRISM_ARENA and BLEED visuals. Double battles. Human input.

The mechanics of all 31 fields are covered by the logic harness: see `../SUMMARY.md`.
