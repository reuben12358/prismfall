# Prismfall Cutscenes: authoring guide (SPINE Rev 6 + 7)

Plugin: `plugins/Prismfall Cutscenes/` (v1.0.0, Essentials 21.1, optional dependency on Prismfall Core).
It provides three things:

1. **Pixel cutscenes** written as data in a small Ruby DSL and played full-screen (`Prismfall::Cutscene.play(:ID)`).
2. **Festival match highlights**, built automatically from two trainers and a list of key moments.
3. **Portraits** for overworld dialogue: the cast's face beside the message box (default), or the rare speech
   bubble (`pf_say`, or a `\pf[...]` / `\pfb[...]` tag in Show Text).

Everything works with zero custom art: backgrounds, beams, particles and emotes are drawn by code, and any missing
sprite or portrait is replaced by a code-drawn placeholder. All sound cues are silent when their file is missing.

| File | Contents |
|---|---|
| `001_Config.rb` | Tunables, effect palettes, audio cue table |
| `002_Util.rb` | Easing, colours, pixel drawing (`Pix`), audio wrapper |
| `003_DSL.rb` | `Cutscene.define / build / play`, the DSL (`Builder`) |
| `004_Actors.rb` | Sprite loading and placeholders (`Gfx`), `Actor` |
| `005_Backdrops.rb` | Procedural and image backgrounds |
| `006_Scene.rb` | The player: camera, layers, timeline, skip, core commands |
| `007_Particles.rb` | Particles, burning/freezing overlays, dome |
| `008_Beams.rb` | Charge-up, beam, impact, **beam clash** |
| `009_Armies.rb` | Crowds, marching, army clash, volleys |
| `010_Text.rb` | Captions, speaker lines, title card, VS card, HP bars |
| `011_Highlights.rb` | `match_highlight` |
| `012_Cinematic.rb` | Dithering, scenery layers (floes, aurora, smoke, hosts), impact frames, slow motion, fracture, rim light, edge glow |
| `012_Cinematic_Techniques.rb` | Techniques from Rejuvenation/Reborn: sheets and flipbooks, `play_sheet`, blend modes, stills, pulses, database animations, on-map mode, camera follow, photosensitive mode (see design/CUTSCENE_RESEARCH.md) |
| `013_Scenes_War.rb` | `:WAR_CLIMAX` (story/13_CUTSCENES.md WAR-1) and `:WAR_CLIMAX_DEMO` |
| `014_Portraits.rb` | Portrait face windows, speech bubbles and the message hook |
| `015_Debug.rb` | Debug menu: "Prismfall Cutscenes..." |
| `selftest/` | Offline test harness (not loaded by the game; see section 9) |

---

## 1. Calling it from events

```
Script: Prismfall::Cutscene.play(:WAR_CLIMAX)
Script: pbCutscene(:MY_SCENE)                         # short form
Script: pbCutscene(:WAR_CLIMAX, variant: :B)          # scene variables
Conditional Branch > Script: pbCutscene(:MY_SCENE)    # true = watched to the end, false = skipped
```

- The scene fades in from black, plays, fades out, and the map fades back. The map BGM is memorised and restored
  if the scene played its own BGM (`restore_bgm: false` on `define` turns that off).
- **Skip:** hold Back (X/Esc) for 0.7 s. `define(:ID, skippable: false)` disables it. For "skippable after the first
  viewing", gate it in the event with a switch and call a non-skippable copy the first time.
- After a scene: `Prismfall::Cutscene.skipped?`, and `Prismfall::Cutscene.result(:clash_winner)` (`:a`, `:b`, `:both`
  or `:fizzle`) when it contained a beam clash.
- A scene that raises an error is logged and ended (returns false) instead of freezing the event. In Debug with
  `$DEBUG` set, the error is raised so you see it.

### Photosensitive mode
`Prismfall::Cutscene.photosensitive = true` (or a `$PokemonSystem.photosensitive` option set to 1, or the Debug menu
toggle) does three things in every cutscene: flashes are capped at a quarter strength with no hold, impact frames are
skipped, and camera shake is cut to 20%. Rejuvenation and Reborn do the same with their own photosensitive setting.
Expose it in the options menu when Core adds one.

## 2. Writing a scene

Put scenes in any plugin script that loads after this one (or in `013_Scenes_War.rb` style files here).

```ruby
Prismfall::Cutscene.define(:MY_SCENE) do
  background :sky, palette: :dusk
  background :sea, palette: :burning
  letterbox true, duration: 0
  actor :kyogre,   species: :KYOGRE,   at: [96, 310], flip: true
  actor :reshiram, species: :RESHIRAM, at: [420, 290]
  emit :embers, rate: 20
  text "The strait burned for three days."
  together do
    charge_up at: :kyogre,   color: :water
    charge_up at: :reshiram, color: :fire
  end
  beam_clash a: { from: :kyogre, color: :water }, b: { from: :reshiram, color: :fire },
             duration: 7, winner: :both
  say "Sigrun", "Father. Enough."
  fade_out
end
```

**Coordinates** are screen pixels in a 512x384 world; the camera starts centred on `[256, 192]`. The world can be
wider than the screen (procedural backgrounds tile sideways), so armies can stand at x = -300 or 800 and the camera
pans to them. Actors are anchored at their feet (bottom centre).

**Timing model.** A time cursor runs through the block.

| Kind | Commands | Cursor |
|---|---|---|
| Showpieces | `text say title vs_card charge_up beam beam_clash volley clash_armies lunge faint fade_out fade_in` | The next command starts when they end |
| Tweens | `move scale rotate fade tint hop tremble hit hp_bar pan zoom shake flash tone letterbox march rout overlay dome army_tint army_fall impact ring clash_mod` | Start at the cursor and do not move it |
| Instant | `background actor remove camera cut flip face emit stop_emit burst army bgm bgs se me cry call` | No time |

- `wait: true` makes a tween block; `wait: false` runs a showpiece in the background.
- `wait 1.5` moves the cursor. `together { ... }` starts everything inside at the same time and continues when the
  longest ends (`wait` inside it staggers). `sequence { ... }` is a normal run nested inside `together`.
  `at(12.0) { ... }` places commands at an absolute time; `now` is the cursor.
- The scene's length is the end of its last command. Timing is real seconds and does not depend on frame rate.

**Variables and variants.** `var(:name, default)` reads a variable passed to `play`/`build`. Ordinary Ruby (`if`,
`case`, loops, local variables) works inside the block. `define(:ID, vars: proc { {...} })` supplies defaults at play
time (the war climax reads Core's flags this way). `include_scene(:OTHER, key: value)` inlines another scene.

**Mistakes are caught when the game loads:** using an actor or army before declaring it raises `ArgumentError`
naming the scene, and a misspelt command raises `NoMethodError`.

## 3. Command reference

Common options on tweens: `duration:` (seconds), `ease:` (`:linear :in :out :in_out :in_cubic :out_cubic :sine
:out_back :out_bounce :steps`).
A **point** is `[x, y]`, an actor id (its mouth), an army id (a random soldier), `[x, y, w, h]` (random inside), or
`{ actor: :id, part: :feet | :center | :top | :mouth, offset: [dx, dy] }`.

### Backgrounds (each call adds layers, back to front)
| Command | Options |
|---|---|
| `background :sky` | `palette: :day :dawn :dusk :night :burning :storm :snow`, `clouds: false/count`, `stars:`, `sun: [x, y]` |
| `background :sea` | `palette: :day :night :burning :storm :black`, `horizon: 200` (animated glints) |
| `background :ice` | `palette: :day :dawn :ember :night :glass`, `plates: true` (black-water channels), `cracks:` |
| `background :battlefield` | `palette: :grass :scorched :snow :sand :stone`, `craters:` |
| `background :mountains` | `color:`, `y:` (base line), `height:`, `snow: true` (parallax 0.3) |
| `background :arena` | `colors: [left, right]` crowd tints, `tint:` floor tint |
| `background :fleet` / `:fortress` | `x:`, `y:` (ground line), `width:`, `color:`, `count:` / `towers:`, `glow:` |
| `background :gradient` | `colors: [[r,g,b], ...]`, `y:`, `height:` |
| `background :color` / `background image: "Graphics/..."` | `color:` / `tile:`, `px:` (zoom), `x:`, `y:` |

All take `parallax:` (0 = fixed to the screen, 1 = moves with the camera), `scroll:` (px/s), `opacity:`, `seed:`.
`clear_backgrounds` removes them.

### Actors
`actor :id, <source>, at: [x, y], scale: 1, flip: false, opacity: 255, z:, mouth: [dx, dy]`

| Source | Notes |
|---|---|
| `species: :KYOGRE` | Battler sprite; `back: true`, `shiny: true`, `form:`, `gender:`. EBDX strips animate |
| `trainer: :LEADER_ANJA` | Trainer front sprite |
| `charset: "NPC 01"` or `charset: :LEADER_ANJA` | Overworld charset; `dir: :down/:left/:right/:up`, `walk: true`, `color:` for the placeholder |
| `player: true` | The player's current charset |
| `icon: :EEVEE` | Pokémon icon |
| `image: "Graphics/Pictures/x"` | Any picture |
| `prop: :ship / :banner / :stone / :tripod` | Small code-drawn props, `color:` |

`silhouette: true` (or a colour) fills the sprite with one colour; `tint: [r, g, b, amount]` blends towards one.
Declaring an id again replaces that actor. Sprites up to 128 px tall are treated as native-resolution and shown at 2x.

| Command | Options |
|---|---|
| `move :id` | `to:` point or actor / `by: [dx, dy]`, `arc:` (hop height), `walk: true` |
| `scale` / `rotate` / `fade` | `to:` (rotate also `by:` degrees; fade 0–255) |
| `tint :id` | `color:`, `amount:` 0–255 (255 = silhouette) |
| `flip :id` / `face :id, :left` | |
| `hop` / `tremble` | `height:`, `times:` / `power:` |
| `lunge :id` | `toward:`, `distance:`, `hit: false` (miss), `color:` (attack, hits the target at the far point) |
| `hit :id` / `faint :id` | White flash + knock-back (`dir:`, `power:`) / sink and fade |
| `hp_bar :id` | `value:` 0–1, `show: false` |
| `remove :id` / `clear_actors` | |

### Camera and screen
| Command | Options |
|---|---|
| `camera` | `at:`, `zoom:` (instant) |
| `cut` | Same, behind a two-frame black blink (a hard cut) |
| `pan` | `to:` / `by:`, `zoom:` |
| `zoom` | `to:` (keep it >= 1; zooming out shows layer edges) |
| `shake` | `power:` px, `decay: false` |
| `flash` | `color:`, `power:` 0–255, `hold:` seconds at full strength |
| `tone` | `to: [r, g, b, gray]` (tints the world, not text) |
| `fade_out` / `fade_in` | To and from black |
| `letterbox true/false` | `height: 32` |

### Particles and overlays
- `emit :embers / :snow / :rain / :debris / :sparks / :smoke / :steam / :ice_shards / :lift / :petals / :motes`, with
  `at:` / `from:` / `area:` (none of them = whole-screen weather), `rate:`, `duration:`, `color:`, `id:`,
  `layer: :back`, `speed:`, `angle:`, `spread:`. `stop_emit :id` (or all with no id).
- `burst kind, at:, count:, color:`
- `overlay :burning, level: 0..1` (flames from the bottom edge) / `overlay :freezing, level: 0..1` (frost from the edges)
- `dome at:, radius:, duration:` grows a scanline dome; `dome hole_at: :actor, hole: 54` opens a clear circle;
  `dome off: true`.

### Beams
| Command | Options |
|---|---|
| `charge_up` | `at:`, `color:`, `size:` |
| `beam` | `from:`, `to:`, `color:`, `width: 14` (full thickness in art pixels; 1 art pixel = 2 screen pixels), `travel:`, `impact: false`, `hit: false`, `shake:` |
| `impact` / `ring` | `at:`, `color:`, `size:` / `radius:`, `squash:`, `layer: :front` |
| `beam_clash` | see below |

`color:` is a palette name (`:fireclash :seaclash :fire :blueflare :water :ice :dragon :electric :grass :psychic :dark :ghost :fairy
:steel :poison :ground :rock :fighting :bug :flying :light :white :bleed :steam :smoke`) or one `[r, g, b]` (a
four-colour ramp is derived).

```ruby
beam_clash a: { from: :kyogre, color: :water, width: 10 },   # or just a: :kyogre
           b: { from: :reshiram, color: :fire },
           duration: 7, winner: :a,        # :a, :b, :both (detonation), :fizzle (gutters out), :mash
           curve: :a_rallies,              # or [[0, 0.5], [0.5, 0.3], [1, 0.6]]
           mash: true, player: :a,         # button mashing pushes the clash point
           launch: 0.6, resolve: 1.6, ball: 20, ground: 306, shake: 4, strobe: true, id: :clash
```
- Each beam is drawn as a dark pixel outline, a coloured edge and body, a hot inner band and a white core, with
  dithered fringes between the bands. `width:` per side defaults to 22; the war climax uses 32 (64 screen pixels, a
  sixth of the screen height). The clash sphere (`ball:` radius, default 0.9 x width) swirls both colours round a
  white core. Each keyframe of `curve:` is a surge: flash, shake, rings and a spray of sparks and ice.
  `ground: y` sets where rubble lifts from. With `winner: :a/:b` the winning beam swells, swallows the other and
  washes the screen white. Previews: `docs/cutscene_previews/beam_clash_*.png`.
- The clash position runs from 0 (at `a`) to 1 (at `b`); high means `a` is winning. `curve:` is the scripted
  struggle (time 0–1 over the struggle phase). Presets: `:even :a_rallies :b_rallies :a_dominates :b_dominates
  :left_right_hold`.
- With `mash: true` each press of Use pushes the point for `player:`; with `winner: :mash` the side ahead when the
  struggle ends wins. Read it with `Prismfall::Cutscene.result(:clash_winner)`.
- Run a long clash under several shots with `wait: false`, and change it with `clash_mod :clash, white: 1.0,
  intensity: 0.4, shake: 2, strobe: false, duration: 2` (`white` bleaches both beams).

### Armies
| Command | Options |
|---|---|
| `army :id` | `icons: [species]` / `charset:` (file or trainer type) / `color:` (code-drawn soldiers), `count:`, `rows:`, `area: [x, y, w, h]`, `facing: :left/:right`, `scale:` |
| `march :id` | `by: [dx, dy]` |
| `clash_armies :a, :b` | `casualties: 0.3`, `gap:` |
| `volley` | `from:`, `to:`, `kind: :fire :ice :water :arrow :rock :dragon :electric`, `count:`, `arc:`, `casualties:` |
| `rout :id` / `army_fall :id` / `army_tint :id` | `by:` / `fraction:` / `color:`, `amount:` |

### Sheets, flipbooks and other Rejuvenation/Reborn techniques
These come from how those games actually build their scenes (design/CUTSCENE_RESEARCH.md).

| Command | Options |
|---|---|
| `actor :id, sheet: "Graphics/Characters/X", grid: [4, 4], frame: 0` | Any grid sheet (charset format is 4×4). `px:` zoom (default 1), `blend: :add / :sub` |
| `pose :id, frame: n` / `pose :id, row:, col:` | Show one cell (also works on charset and icon actors) |
| `flipbook :id, frames: 0..7, hold: 0.1` | Step through cells. `holds: [..]` per frame, `loops:`, `se: { 3 => "Anim/Explosion" }`, `end_frame:`. A tween: add `wait: true` to block |
| `play_sheet "Graphics/Animations/X", grid: [5, 2], frames: 0..4, at: point, hold: 0.05` | One-shot effect that removes itself (`blend: :add` default). Chain several with `at(t) { ... }` along a path for travelling bursts |
| `still "Graphics/Pictures/X", duration: 3, fade: 0.3, steps: 5, dim: 120` | Full-screen CG or storyboard over the scene (blocking) |
| `pulse tone: [-68, -102, -102, 120], duration: 0.15, times: 2` | Tone heartbeat for impacts |
| `anim 16, at: point` | Plays database animation #16 from `Data/Animations.rxdata` |
| `follow :id, smooth: 0.15` / `follow off: true` | Camera keeps tracking an actor; `cut`, `pan`, `camera` end it |
| `fade_in steps: 5`, `fade_out steps: 5`, `fade :id, to: 0, steps: 5`, `ease: :step3`..`:step8` | Stepped (pixel-art) fades |

| `fx_sheet "Graphics/Animations/X", grid: [5, 4], frames: 0..3, at: point, hold: 0.08, loops: true, id: :fire1` | Looping or held effect cell (`blend:`, `scale:`, `z:`); end it with `stop_fx :fire1` |
| `fx_sheet` extras | `origin: [ox, oy]`, `squash:` (flatten a ground decal), `grow: [from, to, seconds]`, `stay: seconds / :forever` (hold the last frame), `fade:` / `fade_in:` seconds, `drift: [vx, vy]` + `gravity:` (thrown pieces) |
| `shadow :id, size: 30, ground: 420` | Dithered ground shadow under a flying actor |
| `submerge :id, to: 0.6, duration: 1` | Sink an actor into the water line |
| `idle :id, frames: [0, 1], hold: 0.3` | Background loop that a `flipbook`/`pose` interrupts |
| `beam_clash style: :sheet, a: { sheet:, flare: {..} }, b: {..}, core: [..], burst: {..}, steam: {..}` | Beams built from tileable sheet segments and effect cells instead of code-drawn beams. All other `beam_clash` options still apply; `rings: true` re-enables code rings |

**On-map scenes:** `define(:ID, on_map: true) { ... }` plays over the live map. There is no black curtain, the map
keeps updating underneath and no background is needed. Actors can follow map events with `actor :x, ..., event: 12`
(or `event: :player`), plus `offset: [dx, dy]`.

**Porting event timings:** one RMXP "Wait 1" in those games is `TICK` = 0.05 s.

### Text and audio
- `text "Caption"` (`position: :bottom/:top/:center`, `duration:`), `say "Name", "Line"` (typed out),
  `title "BIG", sub: "small"`. Text is timed (default from its length) and never waits for a button.
- `bgm "name"`, `bgs`, `se`, `me`, `cry :SPECIES`, `bgm_fade 1.0`, `bgs_fade`. A symbol looks the cue up in
  `AUDIO` in `001_Config.rb`, which lists the design/AUDIO.md name first and stock stand-ins after it:
  `:beam_charge :beam_fire :beam_clash :beam_break :crowd_cheer :crowd_gasp :bgm_war_field :bgm_war_clash
  :bgm_war_after :bgs_war :bgs_rain :bgm_highlight :me_hl_start :me_hl_hit :me_hl_result`.
- `call { |scene| ... }` runs Ruby against the live scene (`always: true` also runs it when the scene is skipped,
  e.g. to set a switch).

## 4. The war climax

`:WAR_CLIMAX` "The Beam Clash on the Glass Dunes" follows story/13_CUTSCENES.md WAR-1 shot by shot (about 72 s,
including a slow-motion beat; the storyboard's 95 s was a suggestion). Since SPINE Rev 18 the war is fought on land,
on the Glass Dunes (map 926) in Ossaria's western desert: Isenmar's host from Skaldfast on the left (west), Ashkaar's
legions from the Siege Camp on the right (east), the grey Northern Sea along the top.

| Variable | Values | Default source |
|---|---|---|
| `variant:` | `:A` WAR_STOPPED, `:A2` WAR_BOTH_BROKEN, `:B` WAR_ASHKAAR_WON, `:C` WAR_ISENMAR_WON | `Prismfall::Narrative.flag(...)`; `:A` without Core |
| `legends:` | `false` = the Wardens' aces fight instead, and there is no flood | false when `choice(:war_legend) == :neither` |
| `water_legend:` / `fire_legend:` | placeholder species (`:KYOGRE` / `:RESHIRAM`) | story team can swap |
| `water_mon:` / `fire_mon:` | aces when `legends: false`: on-map `:GYARADOS` (Marisol's, out of the trench-lines' meltwater) / `:SALAMENCE`; procedural `:MAMOSWINE` / `:SALAMENCE` | |
| `starter_charset:` | charset for the starter in shot 9A | `"Followers/EEVEE"` |
| `overpower:` | `true` with `:B`/`:C`: the winning kingdom's beam swallows the other and whites out the screen instead of the clash falling silent. Not in the storyboard, so off by default | `false` |

Event: `Script: pbCutscene(:WAR_CLIMAX)`. `:WAR_CLIMAX_DEMO` is the same scene fixed to variant `:A2`.
Audio follows design/AUDIO.md: `War - Battlefield` → 0.5 s fade → `War - Beam Clash` on the clash frame → silence
at the break → `War - Aftermath`.

Differences from the storyboard, all because of engine limits:
- Shot 4's split screen is two cuts (there is no split-screen primitive).
- "Heat-haze shader" and per-half screen tints are a whole-screen tone.
- No-legend variant: there is no overworld Mamoswine sheet in the reference games, so the on-map version uses
  Marisol's Gyarados (the storyboard's alternative); it rises at Kyogre's spot rather than in a trench-line.
- **Confirmed by the story team (2026-11-19):** "`:war_legend` kept the legendaries away" means `:neither`, and only `:neither` (14_WAR_AND_BLESSING Part B).

### On-map staging (current `:WAR_CLIMAX`)
`013_Scenes_War_OnMap.rb` stages the scene the way Rejuvenation/Reborn do: an overworld map, overworld-scale
legendaries acting through sheet frames, armies as charset blocks under banners, effect sheets along the beam path.
- Art lives in the plugin overlay `Plugins/Prismfall Cutscenes/Graphics/{Characters,Animations,Pictures}/pfw_*`.
  The loader looks there after the game's own `Graphics/`, so nothing needs copying. Rebuild it with
  `python3 -I tools/build_war_assets.py` (characters, beams, clash cells; it also runs `tools/build_desert.py` for
  the stage, flood, glass and bone-carters). It reads /home/claude/ref/games; origins are in docs/CREDITS.md.
- **The stage** is a picture, `Graphics/Pictures/pfw_glass_dunes.png` (64×24 tiles): Reborn's Twilight Desert dune
  layer recoloured bone-white, the Northern Sea from Rejuvenation's Zor Coast autotile (greyed), Skaldfast from
  Rejuvenation's Castle Weiss wall (rime-tinted) under a Kristiline ice cliff, the Rimed Sands' white trench-lines,
  the Siege Camp (Badlands tents and stake palisade on an earthwork) and a sandstone mesa (Zorrialyn Desert) for
  Meridian. `pfw_glass_dunes.json` records the boxes. When map 926 exists, export it to that file name, or change
  `WAR_STAGE` and the coordinates at the top of the scene (`water_at`, `fire_at`, `clash_c`, `ground`, `gate`,
  `crest`, `mesa`, `flood_at`).
- **The flood-sea** is `pfw_fx_flood` (6 cells of 768×576, 3×2): the sea pouring south over the dunes into the
  hollow round Kyogre. It is an actor (`:flood`, z 455, under every figure) flipbooked 0→5 in shot 2 and 5→0 in shot
  12 as Kyogre sinks.
- **The glass:** `pfw_fx_glass_patch` (Blue Flare's trail, seven patches laid as the beam runs out), `pfw_fx_glass_ring`
  (the wet sand glassing round the clash, hot to cool, replaces the ice fracture), `pfw_fx_glass_wave` (a flood wave
  curling, then setting into glass; it stays to the end), and the bone-carters' banner tinted to glass in shot 8.
  All of them `stay: :forever`, so shots 13 and 15 stand on the glass plain.
- Kyogre: `pfw_kyogre_rise` (emerge/sink flipbooks) and `pfw_kyogre_primal` (front-facing, markings glow), then
  `pfw_kyogre_side` for the beam (a kitbash of Reborn's overworld Kyogre in the Primal palette). Reshiram:
  `pfw_reshiram` charset, descends walking left. No battle sprites are used.
- The clash point is `pfw_fx_clash_core` (blue | white-hot | orange) with chunks and steam thrown out (`spray:`);
  the dome is `pfw_fx_dome`; each army is two drilled blocks under banners (`army ..., blocks: 2, gap: 56`).
- People and props: `pfw_bone_carter` (the bone-carters, who flee when the flood comes and walk back out in shot 15
  to raise a new white banner), `pfw_banner_carters`, `pfw_sled` (Isenmar's ice-sledges; Eirik stands on the lead
  one; in 9C it is Marisol's sled-boat riding the flood), `pfw_gyarados`.
- 13B/C: the losing host breaks and the winner's banners go up over Skaldfast (B) or over the Siege Camp (C).
- If the stage picture is missing, `:WAR_CLIMAX` plays `:WAR_CLIMAX_PROCEDURAL` (`013_Scenes_War.rb`, code-drawn:
  `background :dunes` with a flood pool, the same shots and lines).
- **Real-engine capture:** `bash tools/engine_capture/capture.sh assemble`, then
  `CUT_VARS=variant=A CUT_EVERY=3 bash tools/engine_capture/capture.sh run WAR_CLIMAX`. It reuses the mkxp-z binary
  built by tools/harness/visual, works in its own copy (`/tmp/pfcut_run`), locks game time to 1/60 s per frame and
  writes PNG frames plus `frames.tsv`. Works for any scene id.
- Previews (real engine): docs/cutscene_previews/war_climax_dunes_engine_sheet.png, war_climax_dunes_engine_full.mp4,
  war_climax_dunes_engine_slow.mp4 (flood and clash at half speed), war_climax_dunes_engine_flood.gif,
  war_climax_dunes_engine_clash.gif. The `war_climax_engine_*` / `war_climax_onmap_*` files are the superseded
  sea-ice build.

### Legendary acting sheets (procedural version)
If `Graphics/Characters/pkmn_kyogre_war.png` / `pkmn_reshiram_war.png` exist (named after the species in use), the war
climax uses them instead of battle sprites. The spec:
- 4×4 cells of about 140×100 px each, shown at 2×.
- Overworld scale and 3/4 overworld perspective, dark outline, 24–32 colours.
- Rows: 0 rise/enter, 1 charge, 2 fire loop, 3 recoil/exit.
- The default is 4×4; pass a different `water_sheet:` / `fire_sheet:` to use another file.

Reborn's Zygarde scene (`pkmn_zygarde5.png`) is the model.

## 5. Festival highlights

```ruby
Prismfall::Cutscene.match_highlight(a, b, winner, moments)
```
This is exactly what Core calls (`015_Festival_Draw.rb`, `Festival.play_highlight`, after its own "Watch the
highlights?" prompt): `a`, `b`, `winner` are `{ :id, :name, :trainer_type }` and `moments` is the `MATCH_RULES` list
of `[actor_id, species, event, caption]`. **No Core change is needed.** It never raises `ArgumentError`; on any
internal error it logs and returns false.

| Event | What plays |
|---|---|
| `:send_out` | The Pokémon appears with its cry; its trainer hops |
| `:attack` | Lunge and hit, HP drops |
| `:beam` | Charge-up and beam in the Pokémon's type colour |
| `:beam_clash` | Both charge, beams lock, the row's actor wins the clash |
| `:dodge` | The foe lunges and misses |
| `:faint` | The row's Pokémon is hit and faints |
| `:switch` | Recall and send out the named species |
| `:field_shift` | Rings, tone shift and motes in the type colour |
| `:taunt` | Trainer hops, the foe trembles |
| `:forfeit` | The Pokémon is recalled |
| `:finish` | Charged beam, the foe faints |

Other accepted forms:
```ruby
match_highlight(a, b, winner: :a, moments: [:opening, :super_effective, :final_blow, :walk_off])
match_highlight([:LEADER_TAMSIN, "Tamsin", 0], { name: "Rook", team: [:ROTOM, :TOXTRICITY] }, winner: :b)
```
- `a`/`b`: the hash (optional `:team`, `:version`, `:pbs_name`), a Festival entrant id, or `[type, name, version]`.
- Template moments: `:opening :super_effective :clutch :beam_clash :final_blow :walk_off`; `nil` picks four.
- `tint:` tints the arena floor (the active field); `play: false` returns the scene without playing it.
- Result: VS card (trainer sprites, names, team icons), 2–4 moments, result card. Length is always 15–30 s
  (extra moments are dropped, a short reel holds the result card longer).
- Teams come from trainers PBS, through Core's `Festival.entrant`/`resolve_trainer` when Core is loaded; species
  named in the moments are added. An unknown trainer just gets the moments' species.
- `offer_festival_highlight(a, b, winner, moments)` asks first; use it only from events, Core already asks.
- The four fully storyboarded highlights (FH-1 to FH-4) currently play through this generic renderer using their
  `MATCH_RULES` rows. Their bespoke shots (Gauntlet glow, crowd reactions, illusion break) are not hand-authored yet.

## 6. Portraits: face windows and speech bubbles (Rev 22; the bubble is Rev 7's)

A line of dialogue can look three ways (SPINE Rev 22; the writing rules are in story/13_CUTSCENES.md, "Portrait use"):

| Mode | When | Looks |
|---|---|---|
| **Face** (default) | A `\pf[...]` / `[portrait: ...]` line or `pf_say` by someone in `Portrait::CAST` who has portrait art | A framed 96x96 face on the message box's left edge, above the box (below it when the box is at the top), as in Desolation |
| **Bubble** (opt-in) | A `\pfb[...]` / `[bubble: ...]` line or `pf_say(..., bubble: true)` by someone in `CAST` | The round portrait with a speech tail pointing at the speaker on the map, plus emotes |
| **Plain** | Not in `CAST`, or no art yet (and no bubble asked for) | The normal message box; the tag is removed and the "Name: " label stays |

```
Script:     pf_say(:JUNO, :happy, "You walked through the Bleed like it was fog.")            face
            pf_say(:LARCH, :angry, "IT LIVES IN A TREE.", bubble: true, emote: :anger)       bubble
Show Text:  \pf[JUNO,happy]Juno: You walked through the Bleed like it was fog.                face
            \pfb[LARCH,angry,anger]Larch: IT LIVES IN A TREE.                                bubble
            \pfb[MARTIN,shocked,sweat+exclaim,12]Martin: WHAT.   (3rd field: emotes, 4th: event id or name)
Story tags: [portrait: JUNO, happy] ...   [bubble: LARCH, angry, anger] ...   (same effect)
Trials:     [:JUNO, :happy, "text"]   [:LARCH, :angry, "text", :bubble]
            [:LARCH, :angry, "text", { :bubble => true, :emote => [:anger], :event => "Professor Larch" }]
```
- The tag is removed and the rest goes to the normal message box, so every other control code still works. It is
  handled by an alias around `pbMessageDisplay`, so it works in Show Text, `pbMessage` and choices.
- `pf_say` adds "Name: " for you (`name: false` to drop it, `name: "???"` to override). `emote:` (one or a list) and
  `event:` only matter with `bubble: true`; in face mode the tag's emote and event fields are ignored.
- **Carry-over:** within one conversation (until the main map interpreter starts a new event), a cast member's untagged
  `Name: ...` line keeps the face of their last tagged line, expression included. So scripts tag only a speaker's first
  line and expression changes, and map events keep their `Name: ...` lines.

### Face mode
- The art file is picked by the expression: `Graphics/Portraits/ID_expression.png`, else `ID.png`; any expression name
  works. `:PLAYER` uses `PLAYER_A` / `PLAYER_B` by `$player.character_ID` (the look picked with `pbChangePlayer(1/2)`);
  `register(:ID, art: :OTHER)` borrows another id's files. No file = the plain box (no sprite crop, no silhouette).
- The frame (128x128 around the 96x96 face) is cut from the message box's own windowskin, so it follows the speech frame
  picked in Options: the skin's left corners and edge, mirrored for the right side, around a panel of the skin's body
  colour. RPG Maker XP/VX skins work too; with no skin at all, a code-drawn frame stands in. Faces with transparent
  backgrounds show that panel.
- Placement follows Essentials' `pbPositionNearMsgWindow(face, msgwindow, :left)`: the box's x, above the box, or below
  it when there is no room above. It follows `\wu` / `\wm` / `\wd` and the box's slide-in.
- Entry: a new speaker rises 8 px out of the box and fades in (0.16 s); the same speaker with a new face file gets a 2 px
  nudge (0.1 s); the same face on the next line does not move. No bounce.

### Bubble mode
- **Who the tail points at:** the event given in the tag; else an event on the map whose name is the id
  (or the one registered); `PLAYER` is the player; else the event running the text. If the speaker is off-screen,
  the bubble sits at the left above the box with the tail pointing at the box.
- The bubble pops in with a bounce, follows the speaker, stays above (or below) the message box, and closes with it.

| Expressions | `neutral happy smug angry crying shocked deadpan panic sad blush` |
|---|---|
| Emotes | `sweat shock anger sparkle gloom question exclaim tears blush dots` |

Each expression has a backdrop colour, default emotes and (for angry/crying/panic) a shake. Face overlays (tears,
gloom lines, blush marks) are only drawn when there is no art for that expression, so they do not double up on a
drawn crying face. Other expression names fall back to `neutral`'s look (the file is still looked up by name).

Optional per-character setup, anywhere after the plugin loads:
```ruby
Prismfall::Portrait.register(:MARTIN, name: "Martin", trainer: :LEADER_MARTIN, event: "Martin",
                             color: [200, 60, 60], crop: [40, 6, 48], cast: true)
```

### Portrait art spec
- Folder `Graphics/Portraits/`. Files `NAME_expression.png` (e.g. `JUNO_happy.png`), plus `NAME.png` as the
  fallback for expressions without their own file. `NAME` is the id in capitals (`PLAYER_A`, `PLAYER_B` for the player).
  The project's art lives in `art/out/Graphics/Portraits/` (Juno, Larch, both player looks); copy it into the game's
  `Graphics/` (design/CHARACTER_ART.md). `tools/package.sh` does not ship it yet.
- **96x96 px**, drawn as pixel art at 2x (48x48 art pixels doubled), Desolation's face-file format. The face window shows
  the whole square at 1:1. A 48x48 file also works and is doubled; other square sizes are scaled to 96.
- The bubble masks the same file to a circle of diameter 96: keep the face inside the centre ~80 px. Transparent
  backgrounds show the frame's panel (face) or the expression's backdrop colour (bubble).
- Do not draw sweat drops, shock lines and so on into the file; the bubble animates them outside the ring.
- Bubble load order: `NAME_expression.png` → `NAME.png` → round crop of the trainer front sprite's head (trainer type
  from `register`, else `NAME`, `LEADER_NAME`, `RIVAL_NAME`, `CHAMPION_NAME`) → silhouette with the initial.

### Real-engine shots
`plugins/Prismfall Cutscenes/tools/engine_capture/capture.sh portraits` (mkxp-z under Xvfb, a lean hard-linked copy of
the base project: `assemble`, then `portraits`, then `clean`) installs the maps on a first boot and on the second stages
Ferrow's Landing with stand-in Juno/Larch/dockhand events: `docs/playtest/portraits_*.png` (Juno happy, sad and a
carried name-only line; Larch; a dockhand's plain box; Larch's bubble; a choice; the box at the top; the player's face).

### Stand-in sprites
Prismfall trainer types have no art yet, so `STAND_INS` in `001_Config.rb` maps them to stock sprites
(`ASHKAAR_SOLDIER` → Black Belt, `ISENMAR_SOLDIER` → Sailor, `LEADER_ANJA` → Lorelei, `MERIDIAN_QUENT` → Professor,
and so on). The mapping is my guess at a look, not a casting decision; edit it freely. Own art
(`Graphics/Trainers/TYPE.png`, `Graphics/Characters/trainer_TYPE.png`) always wins, and a type with neither gets
the code-drawn figure.

## 7. Limitations

- Not run in the real engine yet (no mkxp-z here). It is tested against strict fakes and a software renderer
  (section 9). First thing to check in game: beam-clash frame rate. The thick clash issues roughly 800–2,000
  `fill_rect` calls per FX frame; if that is slow, set `BEAM_DITHER = false`, lower `FX_FPS` or raise `BEAM_CHUNK`
  in `001_Config.rb`.
- Pixel-grid rules: FX are drawn at half resolution and shown at 2x, in four colours per effect, at 30 FX frames per
  second. Sprites snap to even pixels at zoom 1. Camera zoom other than 1 or 2 and `rotate` break the grid by nature.
- No split screen, no shaders, no per-region tints. Sprite rotation is used only for fallen soldiers.
- Zooming out below 1 shows layer edges. Shakes above about 16 px can show the bottom edge of ground layers.
- Text is timed, with no button prompt, so that scenes keep a fixed length. Captions are not routed through the
  message system, so `\c[]`-style codes do not work inside cutscene text.
- Battler mouths are guessed (58% of the sprite height). Set `mouth: [dx, dy]` per actor for beams that must leave
  from the right spot (dx is for the unflipped sprite).
- Highlights pick beam colours from the Pokémon's first type, not from the move named in the caption.
- Portraits: one face or bubble at a time; a bubble needs the speaker's event for its tail.
- The scene does not update the map underneath (it is covered).

## 8. Optional art that would improve it

| Art | Where | Gain |
|---|---|---|
| Legendary acting sheets | `Graphics/Characters/pkmn_<species>_war.png` (see section 4) | The war climax's biggest missing piece: staged battle sprites read wrong at this scale |
| Effect sheets | `Graphics/Animations/*.png` (192 px cells) or any grid | Sparse, 4-colour impacts and beam segments for `play_sheet ... blend: :add`, the way Reborn builds its set pieces |
| Portraits | `Graphics/Portraits/NAME_expression.png` | Every cast member without art talks in the plain box until theirs lands; see the spec above |
| Soldier charsets | `Graphics/Characters/trainer_ASHKAAR_SOLDIER.png`, `trainer_ISENMAR_SOLDIER.png`, `..._OFFICER` | Replaces the block-figure armies and rulers |
| Character charsets | `trainer_LEADER_SIGRUN`, `trainer_LEADER_ANJA`, `trainer_MERIDIAN_QUENT`, `trainer_MERIDIAN_AGENT` | Shots 13–14 |
| Trainer front sprites | `Graphics/Trainers/LEADER_*.png` etc. | VS cards and highlight trainers |
| War backdrops | 512x384 (or wider) pictures: the Glass Dunes at dawn (dry, flooded, glassed), Skaldfast's walls on the sand, the Siege Camp's earthwork, the observers' mesa | `background image:` instead of procedural layers |
| Temple-Arena backdrop | 512x384 picture | Highlights (`background image:` in `Highlight.build`) |
| Ice-sledge, sled-boat, bone-carters' banner, war banner, Light Stone, tripod sprites | any PNG, used with `actor :x, image:` | Replaces the code-drawn props |
| Audio | names in design/AUDIO.md (`Beam charge`, `Beam clash`, `Beam break`, `Crowd cheer`, `Crowd gasp`, `War - *`, `Festival highlight *`) | Until then stock/EBDX stand-ins play, or silence |

## 9. Self-test

```
ruby "plugins/Prismfall Cutscenes/selftest/harness.ruby_stub"
ruby "plugins/Prismfall Cutscenes/selftest/harness.ruby_stub" --render WAR_CLIMAX --at 19,25,36 --out /tmp/frames --assets variant=A
```
The files are named without `.rb` on purpose: PluginManager loads every file whose path contains `.rb`.
The harness fakes Sprite/Bitmap/Viewport/Graphics/Input strictly (integer pixel coordinates, no use after dispose,
no leaked sprites or viewports), reads teams from `pbs/trainers.txt` and Core's real `MATCH_RULES`, and with
`--render` composites frames to PNG (needs ImageMagick; `--assets` uses the EBDX base project's sprites, path in
`PF_ASSETS`). The suite covers both example scenes at 20/40/60/144 FPS and with jitter and lag spikes, all war
variants, every DSL command, skipping, mash clashes, Core's `match_highlight` call for all 12 rules, the portrait
tag forms and the three modes (face with the project's real art from `art/out`, opt-in bubble, plain fallback), face
placement, entry and carry-over, the frame's windowskin cut, Trials talk rows (`:bubble` and option hashes), every
bubble expression and emote, the art fallback chain, the Debug menu entries, and the
Rejuvenation/Reborn techniques: flipbooks, `play_sheet` chains, blend modes, stills, pulses, database animations
(through a stand-in `RPG::Sprite`), on-map mode with event-following actors, camera follow, legend sheets in the war
climax, and photosensitive mode.
