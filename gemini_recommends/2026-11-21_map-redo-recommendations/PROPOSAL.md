# Map Redo & Visual Level-Design Recommendations (Post–Map Builder 16 Audit)

- **What:** A visual audit of 31 currently built Prismfall maps (current through commits `72519ac..10f3477`, including Map Builder 15's Lumen City / Circuit Gym and Map Builder 16's `525`, `562/563`, `546/547`, and `579` rebuilds), paired with **7 prioritized map redo blueprints**, **2 cross-map stamp-bug fixes**, and **5 side-by-side Before-vs-Target pixel-art concept mockups** (`mockups/`) so Claude and the creator can decide which maps to elevate next.
- **Why:** Recent rebuilds (`546/547` Thistledown Manor, `570` Frostwick, `562/563` Rimewood, `525` Gossamer Deepwood, `544/564` Caves, `171/172` Tidelock Gym) already meet or exceed the Pokémon Rejuvenation visual bar (`design/ART_DIRECTION.md` §0–3). However, **7 high-visibility maps**—spanning Act I routes/cities (`552`, `140/146/147`, `522/548`, `120`), the brand-new Chapter 5 Lumen City & Circuit Gym (`180/181/608`, `190–193`), and the War Theatre climax (`926/925`)—still exhibit ruler-straight horizon stripes, unbordered texture cutouts, flat clip-art landmarks, legacy Tectonic tileset mismatches, or extracted stamp glitches that break immersion next to Claude's strongest work.
- **Where it plugs in:**
  - Routes & Act I towns: `mapgen/layouts/routes_craft.py` (`build_552`, `build_540`, `build_528`), `mapgen/layouts/saltmere_rj.py` (`build_140`, `build_146`, `build_147`), `mapgen/layouts/orchard.py` (`522`), `mapgen/layouts/deepwood.py` (`548`), `mapgen/layouts/briarwick_rj.py` (`120`).
  - Chapter 5 Lumen & Gym 4: `mapgen/layouts/lumen.py` (`build_180`, `build_lowlight`), `mapgen/layouts/circuit_gym.py` (`build_190`–`build_193`), `mapgen/ldraw.py`.
  - War Theatre: `mapgen/layouts/war.py` (`build_926`, `build_925`), `mapgen/gdraw.py` (`wave_curl`, `cliff_kit`).
  - Shared stamps: `mapgen/rstamps.yaml` (`sh_big` line 14, `ak_rock2` line 39).
  - Visual targets & comparisons: `gemini_recommends/2026-11-21_map-redo-recommendations/mockups/`.
- **Sources:**
  - `design/ART_DIRECTION.md` (§0 Hard Requirements, §3 Map Quality Rubric, §4 Per-Kingdom Identity)
  - `design/MAPGEN.md` (§2h–2s recent map-builder tooling, `PF Rejuv` tilesets 50–60, `gates:` proofs)
  - Current rendered map previews in `maps_out/previews/` and `maps_out/previews/lumen/lumen_overview.jpg` (inspected post-commit `10f3477`).

---

## 1. Current Map Quality Scorecard (31 Inspected Maps)

> **Important:** Every grade below reflects the **latest built PNGs** in `maps_out/previews/` after Map Builders 13–16. Maps graded **A- to A+** should **NOT** be redone—they represent the visual benchmark for the rest of the game.

### Keep & Celebrate — Already Rejuvenation-Tier (Do NOT Redo)

| Map ID & Name | Grade | Why It Already Works (Keep Doing More of This!) |
|---|---|---|
| **546 / 547 Thistledown Manor & Attic** | **A+** | Best interior craft in the repo (`mdraw.py`). Distinct per-room wall/floor palettes (sage foyer, crimson portrait gallery, rose parlour, glass conservatory, teal dining room), rich custom furniture, moonlight oculus + footlight stage in `547`. |
| **570 Frostwick** | **A** | Textbook cultural storytelling: frozen Elowen treehouses on NW cliff terrace linked by rope bridges, frozen waterfall feeding a curved ice brook, Hearth Elder centerpiece beside Isenmar whalebone longhouses, briar-rib gate, organic ice lagoon. |
| **154 Pell Playhouse — Auditorium** | **A** | Lush proscenium stage, gold columns, velvet curtain, orchestra pit with grand piano, royal boxes, deep red aisle carpet & chandelier. |
| **562 The Rimewood & 563 Rimewood Glade** | **A / A-** | Huge leap in commit `fcc79e8`. Frost-teal & snow-white mixed canopy, curved Hoar Pond ice slide puzzle, fallen giant log bridge, cozy chalet, frozen Silk-fall waterfall + Stantler upper shelf. |
| **100 Ferrow's Landing** | **A-** | Strong multi-tier coastal bluff (two h=2 terraces), winding gravel streets, harbor overlook with anchor monument, custom moored *Dovetail*, and west headland lighthouse. *(Tiny polish only: two brown cliff boulders sitting on white harbor beach sand look slightly pasted-on.)* |
| **160 Ebbmouth** | **A-** | Atmospheric river-split Isenmar port with dark open river, bridges, lock pylons, waterwheels, whalebone longhouses, dock cranes, and frozen SE cove. |
| **525 Gossamer Deepwood** | **A-** | Great commit `7e58c35` rebuild: upper waterfall, stepping stones, weavers' camp under the elder tree, moth tree, and purple/cyan crystal transition at the east mouth. *(Minor polish: D2 puzzle white arrow tiles in the NE could use softer mossy/webbed tones.)* |
| **544 Brinecut Mine 1F & 564 Gullcry Caves** | **A-** | Night-and-day upgrade over old stock caves (`cdraw.py`). Bedded rose-salt walls + chasm minecart trestles (`544`) and wet slate sea caves with blowhole light shafts (`564`). |
| **171 / 172 Tidelock Gym — Basins** | **A- / B+** | Clean timber lock-hall framing, weathered grey-blue quay stone, muddy algae-flecked low-water bed vs flooded deep basin, union banners & red sluice wheels. |
| **579 The Wolfsrime** | **A-** | Restored in `b4ea0ac`. Dense, enveloping snow-forest canopy with winding snow trail, pocket clearings, frozen brook, and frosted giants—genuinely atmospheric. |
| **566 Spinners' Rise, 578 Rimewood Path, 561 Gullcry Cliffs** | **B+** | Solid Map Builder 12 recrafts with real elevation, waterfalls, sea coves, frozen slides, and drystone folds. *(Light future polish only: soften long straight horizontal cliff segments on `578`/`561` and break up bare upper-center snow on `577` Frostwick Pass.)* |
| **520, 524, 528, 540, 541, 560** *(Act I Crafted Routes)* | **B / B+** | Cohesive `PF Rejuv` routes with strong route mechanics. *(Two surgical stamp bugs to patch in passing: `528` shares the hollow `ak_rock2` sea rock bug; `540` has the stray pine tree baked onto `sh_big`'s roof—see §3.)* |
| **131 Loomhouse Gym — The Canopy** | **B** | Good vertical climb mood & clear web trampolines. *(Optional polish: stagger the full-width straight horizontal wooden bridges into cantilevered branch platforms.)* |

### Needs Redo / Major Visual Elevation — Ranked by Player Impact

| Priority | Map ID & Name | Grade | Core Visual Flaw Observed | Mockup Included? |
|---|---|---|---|---|
| **#1** | **552 The Dyers' Ford** | **C-** | Ruler-straight red/blue/yellow horizontal "national flag" river stripes + giant `+` crosshair road/cliff grid + MS-Paint primary squares. | Yes (`01_552_*`) |
| **#2** | **140 Saltmere** *(+ 146/147 polish)* | **C+** | 88-tile flat wall of ~22 identical High Town houses, Excel-grid salt pans, harsh W/E edge seams, duplicate ships (`146`), 3 horizontal wall strips (`147`). | Yes (`02_140_*`) |
| **#3** | **522 Glassed Orchard** *(+ 548)* | **D+** | Still on legacy Tectonic `bleed` tileset 40 (clashes with all `PF Rejuv` neighbors), SW Veil border glitch, mid-tree white tear, egg-trees don't read as an orchard. | Yes (`03_522_*`) |
| **#4** | **926 Glass Dunes** *(+ 925 polish)* | **C+** | Flat clip-art sky-blue wave silhouette (`gd_wave`), twin dead-vertical crest walls + 25-tile straight horizontal ledge, harsh sawtooth white-spike map border. | Yes (`04_926_*`) |
| **#5** | **181 & 608 Lumen — The Lowlight** | **C+** | Unbordered blinding-white marble square cut into dark brick, roof-vs-street brown value collapse (`lm_roofT`), `608` Shatter reads as mild confetti instead of cataclysm. | Yes (`05_608_*`) |
| **#6** | **180 Lumen Concourse & 190–193 Circuit Gym** | **B- / C+** | Concourse is a flat 5-strip horizontal grid with Meridian Spire wedged in NE corner; Circuit Gym `193` Core has bare floor, random cyan "Z" decals, and bright yellow picket-fence barrier (`lm_bars_*`). | Blueprint |
| **#7** | **120 Briarwick** *(+ global `sh_big` fix)* | **B- / C+** | Bugged `sh_big` stamp has a pine tree growing out of its roof; roofless beige-checker Sheridan roofs clash with Elowen hollow trees; rigid vertical west stream & harsh pale decks. | Blueprint |

---

## 2. Top 7 Detailed Map Redo Proposals

### Priority #1 — `552` The Dyers' Ford (`C-` → Target `A`)

- **Files:** `mapgen/layouts/routes_craft.py` (`build_552`, lines 664–838), `mapgen/specs/552_dyers_ford.yaml`, `mapgen/tdraw.py` (`dye_red/blue/yellow`), `mapgen/ndraw.py` (`dl_cloth_*`, `df_sluice`).
- **Mockups:**
  - Before vs. Target: [`mockups/compare_01_552_dyers_ford.png`](mockups/compare_01_552_dyers_ford.png)
  - Clean Target Concept: [`mockups/01_552_dyers_ford_target.png`](mockups/01_552_dyers_ford_target.png)
- **Observed Flaws:**
  1. **Ruler-straight "national flag" river:** `cy = 35 ± 2` (line 680) plus `band < 0.3 / 0.58 / 0.86` (line 827) paints three rigid horizontal bars of red, blue, and yellow spanning all 80 tiles edge-to-edge—visually reading as a tricolour flag rather than a living river fed by dye-works.
  2. **Crosshair `+` layout:** A dead-vertical central road (`x=38..40`, lines 687–691) intersects a straight horizontal north cliff (`y~20`, line 676) and the horizontal river (`y~35`), slicing the route into four rectangular quadrants.
  3. **Flat primary-color UI squares & boxy crop patches:** Sluice stones `(49/51/53, 18)` appear as three tiny flat MS-Paint squares dropped on bare grass; south madder/woad/weld fields (`dyemask`) read as pixelated colored rectangles; the fulling mill (`gl_flat2`, line 791) sits isolated far from any mill-race or waterwheel.
- **Concrete Redesign Blueprint:**
  - **Organic S-Curve River Selvedge:** Enter at WNW (`y~24`), bend gracefully SE around a lush central bluff (`y~42`), and curve NE (`y~30`) where the clear northeast waterfall (the Fourth Colour) meets the river beside the cloth-barge jetty. Include **two mossy willow/reed river islets** splitting the current.
  - **Staggered Dye-Mill Cascades & Tapering Plumes:** Build three staggered dark-timber dye sheds (stepping down along the north cliff lip from NW to center-north, each with a side waterwheel & stone spillway chute) discharging narrow **madder crimson, woad indigo, and weld ochre runnels**. Replace flat full-width color bands with **curving, tapered dye ribbons** (using 2-row feathered edge tiles + swirl accents) that braid gently around the central islet and dissipate into clear water past the ford.
  - **Diagonal Shoal Stepping-Stone Ford & Overhead Cloth Corridors:** Curve the main weavers' road diagonally from the north stair to a wide pale-gravel river shoal crossed by staggered natural river boulders (varying 1–2 tile widths, not a 2-column vertical dot ladder). String the drying-cloth lines (`dl_cloth_*`) across the winding road at staggered angles between rustic timber posts.
  - **Sluice Monoliths & Grounded Fulling Mill:** Replace the three flat colored floor squares with carved mossy **stone dye-basins / runnel valves** visually linked by a narrow stone channel toward the waterfall culvert grate. Seat the stone fulling mill right on the south-east river bend with an active wooden waterwheel dipping into the current.
  - **Atmosphere & Seams:** Keep `field: MEADOW`, add warm golden-afternoon tone `[10, 6, -6, 0]` + faint drifting pollen/mist fog (`opacity: 28`), and preserve exact N (`offset: 39 -> 540`) and S (`offset: 38 -> 541`) `seal_against` spans.

---

### Priority #2 — `140` Saltmere Upper Town (+ `146` Harbour & `147` Old Town Polish) (`C+` → Target `A`)

- **Files:** `mapgen/layouts/saltmere_rj.py` (`build_140` lines 631–802, `build_146` lines 806–907, `build_147` lines 911–1025), `mapgen/specs/140_saltmere.yaml`, `mapgen/specs/146_saltmere_harbour.yaml`, `mapgen/specs/147_saltmere_oldtown.yaml`, `mapgen/rstamps.yaml` (`ak_rock2` line 39).
- **Mockups:**
  - Before vs. Target: [`mockups/compare_02_140_saltmere.png`](mockups/compare_02_140_saltmere.png)
  - Clean Target Concept: [`mockups/02_140_saltmere_target.png`](mockups/02_140_saltmere_target.png)
- **Observed Flaws:**
  1. **88-tile wall of ~22 flat-row townhouses (`140` High Town):** `m.ht[:12, :] = 2` (line 637) plus `block(m, 0, 39, 0, 7)` / `block(m, 52, 87, 0, 7)` (lines 684–685) creates a ruler-straight horizontal retaining wall topped by an unbroken barrack row of identical-depth houses from `x=0` to `x=87`.
  2. **Excel-spreadsheet salt pans (`140` south):** `LAKE = 59` draws a straight 88-tile sea wall dropping into stark white rectangles subdivided into rigid horizontal/vertical pastel cells (`salt_works`, lines 782–783), split by two rigid rectangular causeways.
  3. **Harsh West/East edge seams (`140` lines 700–703):** A narrow 4-tile vertical strip of white salt (`x=0..3`) runs flush against vertical townhouse gables on the west (`560` Frostflat Causeway seam), while a narrow 4-tile green strip (`x=84..87`) butts flush against eastern blocks (`528` Marram Down seam).
  4. **`146` Harbour & `147` Old Town issues:** `146` places **two 100% identical Dovetail ship stamps** side-by-side (`ship(m, 21, -11); ship(m, -6, -11)`, line 889) in a rigid rectangular `[ ]` stone basin; `147` stacks **three ruler-straight 88-tile horizontal walls** (`m.ht[:19,:]=3; m.ht[19:39,:]=2`, line 920); and `ak_rock2` (lines 892 & 1018) renders with a **square blue-water hole in the middle of every boulder**.
- **Concrete Redesign Blueprint:**
  - **Asymmetric Two-Bluff High Town (`140`):** Break `m.ht[:12, :] = 2` into an **asymmetric NW Citadel/Bell-Tower Bluff** (`y=0..16, x=0..34`, topped by a prominent vertical Salt Bell clock tower breaking the skyline) stepping down via diagonal/offset staircases toward an **elevated NE Lantern Theatre Terrace** (`y=0..14, x=54..84`), with the arched North Gate recessed slightly into a stone barbican pocket (`x=40..48`). Replace unbroken 22-house rows with staggered courtyard clusters (varying setbacks of 1–3 tiles, mixed gable heights, narrow cobbled steps and arched passages).
  - **Curved Promenade & Organic Salt Evaporation Lagoon (`140` south):** Replace straight `LAKE = 59` with a **gently curved/stepped crescent stone sea wall** (`y` arching from `55` at the flanks to `60` in the center, punctuated by two projecting semicircular stone outlook bastions). Beneath it, shape the tidal salt flats as **organic rounded/chamfered earthen bund basins** stepping gently in color (rose-pink halophile → pearl crystallizing → pale turquoise → golden brine), linked by rustic winding timber raking catwalks, conical salt heaps, tubs, and moored rowboats.
  - **Natural Gate Transitions (`SnapEdges` / `seal_against`):** Give the West Gate (`140` W ↔ `560`) a weathered stone customs wall & curving sandy/salt-marsh bluff sloping naturally out of town; give the East Gate (`140` E ↔ `528`) a terraced green coastal headland with clustered pines/cherries and a proper freestanding stone gatehouse instead of a 4-tile flat verge strip.
  - **Surgical Upgrades for `146` & `147`:**
    - In `146`, keep one large merchant carrack and replace the duplicate second ship with a distinct **smaller trawler / open salt-barge + cargo crane pier**, and angle/step the breakwater mole so the harbour feels carved by the coast instead of `[ ]` brackets.
    - In `147`, break the 3 horizontal terrace walls with jutting stone balconies, recessed pocket gardens, and staggered stair flights framing Pell Playhouse asymmetrically.
    - Fix `ak_rock2` in `mapgen/rstamps.yaml` (see §3).

---

### Priority #3 — `522` The Glassed Orchard (+ `548` Cocoonfall Hollow) (`D+` → Target `A`)

- **Files:** `mapgen/layouts/orchard.py` (whole file — still on legacy `wildkit` / `palette: bleed` tileset 40!), `mapgen/specs/522_glassed_orchard.yaml`, `mapgen/layouts/deepwood.py` (`548`), `mapgen/specs/525_deepwood_cocoonfall.yaml`.
- **Mockups:**
  - Before vs. Target: [`mockups/compare_03_522_glassed_orchard.png`](mockups/compare_03_522_glassed_orchard.png)
  - Clean Target Concept: [`mockups/03_522_glassed_orchard_target.png`](mockups/03_522_glassed_orchard_target.png)
- **Observed Flaws:**
  1. **Last Act I outdoor maps stranded on old Tectonic tileset 40:** Every adjacent route (`520`, `521`, `524`, `525`) is now on `PF Rejuv`. Walking from `521` Windfall Row into `522` (the player's **first Bleed zone & Lecture One emotional climax!**) drops the art style back to smooth pastel Tectonic egg-trees (`crystal_tree_2x3`).
  2. **Visible tile & border glitches on `522`:** Broken transparent/void seam along the SW Veil exit (`x=0..4, y=35..39`); a **1-tile horizontal white tear slicing across a mid-map purple tree** (`x~21, y~16` where `CU['strand_h']` overlaps `crystal_tree`); an outdated flat beige slab staircase (`stairs_stone@40`) with a cyan crystal obstructing its bottom step; and a weird chopped black half-stump (`gstump_dark`) floating in the NW.
  3. **Missing "Orchard" visual identity:** Uniformly spaced purple oval blobs on flat pale-lilac turf don't read as *the Pruetts' apple orchard flash-frozen in one winter night*. (`548` Cocoonfall Hollow shares the same legacy Tectonic palette clash and harsh floating horizontal white thread lines.)
- **Concrete Redesign Blueprint:**
  - **Port `522` & `548` to `PF Rejuv` (new vitrified/Bleed slice in `rcustom.py` / `gdraw.py`):** Recolor Rejuvenation's crisp Sheridan cliffs (`sh`), stone stairs (`st_stair_*`), and Goldenleaf timber cottage (`gl_cot`) into translucent ice-lavender/pale-slate crystal glass. Draw **gnarled crystalline apple trees** (translucent ice-blue/violet boughs hung with tiny gleaming ruby-red glass apples + matching shattered glass-apple ground clusters) to replace the egg-shaped Tectonic trees!
  - **Unforgettable "Living-to-Glass" Veil Split at Entrance:** Make the SW entry pocket (`x=0..8, y=30..39`, before the Veil) **living lush Sheridan green grass, green apple trees, and mossy stone orchard gateposts**—then slice diagonally/vertically across it with a glowing iridescent prism Veil curtain so the player visually witnesses the exact boundary where the living world turned to crystal!
  - **Curved Terraced Orchard & Storytelling Props:** Step two curved ash-and-stone orchard terraces northeast up to the glass-encased Pruett Farmhouse on the high knoll (`x~31, y~4`). Plant legible **broken orchard rows** (interrupted by snapped crystal boughs, an overturned wooden cider press, spilled baskets of glass apples, and a mirror-still violet reflecting pond with sunken branches). Wrap all four borders cleanly in dense multi-row dark-violet crystal canopy (`CK.woods` + `CK.infill`) so zero void/edge leaks exist.
  - **Atmosphere:** Cool twilight glass tone `[-16, -20, 22, 48]` + wire the already-commented `fog: prismfall_glass` (`opacity: 60`, slow drift) instead of leaving it as a comment on line 882 of `522_glassed_orchard.yaml`!

---

### Priority #4 — `926` The Glass Dunes (+ `925` The Steamline Polish) (`C+` → Target `A`)

- **Files:** `mapgen/layouts/war.py` (`build_926` lines 636–840; `build_925` lines 420–530), `mapgen/gdraw.py` (`wave_curl` line 597, `cliff_kit('gdc')`), `mapgen/specs/926_glass_dunes.yaml`, `mapgen/specs/925_steamline.yaml`.
- **Mockups:**
  - Before vs. Target: [`mockups/compare_04_926_glass_dunes.png`](mockups/compare_04_926_glass_dunes.png)
  - Clean Target Concept: [`mockups/04_926_glass_dunes_target.png`](mockups/04_926_glass_dunes_target.png)
- **Observed Flaws:**
  1. **Flat clip-art "Frozen Wave" (`gd_wave` at `(1, 6)`):** `wave_curl()` renders as a flat, matte sky-blue 2D silhouette pasted directly onto warm tan sand—zero icy facets, zero translucent depth, zero frost/rubble base anchoring it into the ground.
  2. **Ruler-straight vertical crest canyon & 25-tile horizontal ledge:** Lines 660–683 build two straight vertical block walls (`x=13..17` and `x=43..47`), sealed along the bottom by a **dead-straight 25-tile horizontal ledge (`y=14, x=18..42`, line 751)**, while a straight vertical ribbon of dark glass runs dead-center straight down the south half (`x~29..32`), producing a rigid T-square grid. (Same vertical dead-center glass bar bisects `925` The Steamline!)
  3. **Sawtooth white-spike map border & harsh sand-to-glass edge:** `m.SEAL` rings the entire north and east edges in a 1-tile fence of bright white crystal spikes that looks like saw-teeth, and raw 1-tile stair-stepping between pale tan sand and dark black-green obsidian reads noisy without a transitional scorched-sand fringe.
- **Concrete Redesign Blueprint:**
  - **Rebuild `gd_wave` (`8×6` Glacial Crystal Monument):** Faceted glacial teal-to-emerald-to-ice-white pixel art with crisp dark teal outlines, frothy jagged ice-crystal crest spray, frost-rim snow/ice rubble anchoring its base into the sand, and a tiny silver glint inside the curl (matching the Feebas flavor text on line 708!).
  - **Sculpt the North Crest into a Crescent Impact Caldera:** Replace the twin vertical walls and 25-tile straight horizontal bar with a **sweeping crescent-shaped obsidian blast rim** stepping down in staggered curved tiers with glowing orange-amber heat fissures radiating from the legendary clash point (`(30, 2)`). *(To keep `gates:` leak-proof on stepped one-way ledges, place solid obsidian spire buttresses `gd_spire` / `gdc` corner rocks at every 1-tile elevation step so no diagonal leak exists!)*
  - **Diagonal Obsidian Flows + Scorched-Ash Fringe:** Angle the fused-glass tongues **diagonally NE → SW** off the crater (mirroring the beam blast trajectory rather than a vertical strip), add a **1-tile scorched-ash/fused-sand transition rim** in `gdraw.py` so obsidian melts believably into golden rippled sand, and braid the western turquoise flood channels with soft layered rising steam plumes (`gd_steam*`).
  - **Natural Canyon Framing:** Replace the bright white crystal-tooth perimeter (`m.SEAL`) with weathered **Ossaria sandstone canyon outcrops (`sdc` cliff rims) and sandbagged siege trenches**, framing the battlefield inside an authentic desert basin. *(Apply the same diagonal/curved flow + sandstone border treatment to `925` The Steamline's dead-vertical center stripe!)*

---

### Priority #5 — `181` & `608` Lumen City: The Lowlight (Normal & Shattered) (`C+` → Target `A`)

- **Files:** `mapgen/layouts/lumen.py` (`build_lowlight` lines 292–379), `mapgen/ldraw.py` (`lm_roofT*`, `lm_bleed*`), `mapgen/specs/181_lumen_lowlight.yaml`, `mapgen/specs/608_lumen_lowlight_shattered.yaml`.
- **Mockups:**
  - Before vs. Target: [`mockups/compare_05_608_lowlight_shattered.png`](mockups/compare_05_608_lowlight_shattered.png)
  - Clean Target Concept: [`mockups/05_608_lowlight_shattered_target.png`](mockups/05_608_lowlight_shattered_target.png)
- **Observed Flaws (Brand-New Commit `5ca4139`!):**
  1. **Unbordered blinding-white marble square (`181` & `608` center):** `m.rect(22, 14, 14, 10, 'q')` (line 307) drops a razor-sharp bright-cream rectangle directly into dark soot-brown brick with zero curb, step, or weathering transition—reading like an accidental missing-texture cutout! Same issue on the bare 8×8 white marble corner at `(0, 3)` (line 301).
  2. **Severe Roof-vs-Street Value Collapse (violates `ART_DIRECTION.md` §3.9 Readability):** Solid dark-brown flat tenement roofs (`lm_roofT`, rows 14–18 and 27–31) have nearly the exact same hue and brightness as the walkable dark-brown brick streets below, punctuated only by tiny repeating red chimney pipes in uniform grids.
  3. **Understated `608` Shatter Transformation:** On `608`, 12% scattered 1-tile purple confetti specks (`lm_bleed0-2`, line 365) and small crystal figures leave the tenements and blinding-white square looking virtually untouched—it doesn't deliver the visceral gut-punch of a city-shattering Plate Vault catastrophe!
- **Concrete Redesign Blueprint:**
  - **High-Contrast Tenement Silhouettes (`ldraw.py` `lm_roofT`):** Recolor/redraw Lowlight rooftops as **cool dark charcoal-slate pitched roofs** (blue-grey slate tiles, cast-shadow eaves along south edges, skylights, wooden rooftop water tanks, and overhead metal pipe bridges spanning the alleys) contrasting cleanly against **warm lamp-lit reddish-brown cobblestone alleys** below. Break the rigid 3-row block grid with a crooked stepped alley ("Pidove Steps") and corner recesses.
  - **Grounded Sunken Film-Set Plaza & Stepped Entry Landing:** Border Rook's central square with a **1-tile dark-slate raised kerb + cracked transitional flagstones**, toning its floor down to weathered warm grey-ochre stone so it blends organically into the district; frame the NW Concourse entry landing with a brass balustrade + stone steps descending onto the brick street.
  - **Cataclysmic Vault Shockwave on `608`:** Carve a **dramatic jagged glowing violet-obsidian fissure** radiating diagonally southwest straight out of the blown-open Plate Vault steel door `(48, 4)` across the sunken plaza, with large translucent purple crystal clusters erupting out of cracked tenement walls, shattered pavement rims, broken dark streetlamps, and swirling violet Bleed fog (`prismfall_glass`, opacity 55) over Nadir's glowing night abyss below.

---

### Priority #6 — `180` Lumen City: The Concourse & `190–193` Circuit Gym (`B- / C+` → Target `A-`)

- **Files:** `mapgen/layouts/lumen.py` (`build_180` lines 125–278), `mapgen/layouts/circuit_gym.py` (`build_190`–`build_193`, lines 126–319), `mapgen/ldraw.py` (`lm_bars_*`, floor decals), `mapgen/specs/180_lumen_concourse.yaml`, `mapgen/specs/190_circuit_gym.yaml`–`193_circuit_gym_193.yaml`.
- **Observed Flaws (Brand-New Commit `5ca4139`!):**
  1. **Concourse (`180`) is a flat 5-band horizontal grid:** Five straight horizontal building strips sit on a single uniform `ht=2` plane (only the small SE Lowlight stair drops to `ht=1`), repeating the same verdigris fish-scale mansard block 5–6× side-by-side.
  2. **Un-kerbed rectangular green grass strips & dead-end tram:** Prism Plaza's four `6×3` green lawns (line 183) and the 84-tile south grass strip (line 140) cut sharp 90° raw grass rectangles straight into cream marble with no stone kerb; the tram track (`x=0..83`, line 139) stops abruptly in flat sidewalk on the right with no station/turnaround; and **Meridian Spire** is squeezed into a narrow top-right corner (`x=77, y=0`) instead of commanding the skyline!
  3. **Circuit Gym (`190–193`) floor clutter & "yellow picket fence" boss room:** Every puzzle room scatters disconnected little cyan "Z" floor decals at random across a flat black grid; and in **`193` The Core**, `lm_bars_m/l` (line 247 & 309) reads like a **bright yellow wooden garden picket fence with blue dots** cutting straight across a bare dark room—with Rook standing on plain flat tiles flanked by two tiny potted ferns and no broadcast stage!
- **Concrete Redesign Blueprint:**
  - **Concourse (`180`) Elevation & Landmarks:**
    - Raise the north Council Ward & **Meridian Spire Acropolis (`y=0..16`) to `ht=3`** with twin grand marble staircases, brass balustrades, and flanking reflective pools so Meridian Spire visually towers over Prism Plaza!
    - Redesign Prism Plaza with a **stepped octagonal reflecting basin** around the Prism Fountain, **stone-kerbed circular/chamfered planters** (replacing raw green grass rectangles), a richer ring of festival kiosks/bunting, and varied skyline roofs across Market Street (alternating brass domes, recessed rooftop glass gardens, and taller terraced civic blocks).
    - Terminate the east end of the Tram Boulevard (`x=76..84`) in a glass-vaulted **Concourse Tram Terminal / arched tunnel portal**.
  - **Circuit Gym (`190–193`) Studio Polish:**
    - Replace random floating cyan "Z" squiggles with **structured recessed floor conduit channels** framing the puzzle boards and glowing directional power tracks leading from generator to exit door.
    - Add a sleek dark-steel & cyan **holographic glass barrier (`lm_holorail_*`)** in `ldraw.py` to replace the yellow picket-fence look of `lm_bars_*` inside `193`.
    - Elevate Rook's battle arena in `193` onto a **raised glowing Neon Grid broadcast stage** (central illuminated circuit emblem floor, warm spotlight cones, boom-camera tracks, and an elevated glass VIP gallery balcony on the right where Juno & Larch watch).

---

### Priority #7 — `120` Briarwick (+ Global `sh_big` Roof-Tree Bug) (`B- / C+` → Target `A-`)

- **Files:** `mapgen/layouts/briarwick_rj.py` (lines 60–233), `mapgen/rstamps.yaml` (`sh_big` line 14, `sh_inn` line 16, `sh_ell` line 19), `mapgen/specs/120_briarwick.yaml`, `mapgen/layouts/routes_craft.py` (`build_540` Manor exterior).
- **Observed Flaws:**
  1. **Critical Stamp Extraction Bug (`sh_big`):** `rstamps.yaml` line 14 extracts `sh_big` from Rejuvenation Map 423 (`rect: [14, 5, 12, 13]`) with `rows` that capture a **stray green pine tree growing directly out of the upper-right roof**! This glitch is visibly stamped on BOTH `120` Briarwick's Chapel (`(55, 34)`) AND `540` Thistledown Lea's Manor exterior!
  2. **Flat beige-checker roofs clash with Elowen's deep forest:** `sh_inn` (PC), `sh_big` (Chapel), and `sh_ell` (SW house) have bright pale-tan flat veranda checker roofs (intended for Sheridan's sunny plaza) that read as **roofless beige grids** sitting next to Briarwick's mossy dark-canopy hollow giant trees (`pf_g_*`).
  3. **Rigid vertical west stream & bright floating decks:** The west stream runs nearly straight down `x=8..10`; the weavers' deck (`(22, 23)`) and SE lantern decks (`(51, 52)`/`(59, 52)`) use un-shaded bright Goldenleaf porch planks (`PALE = 3402`) that pop harshly against dark forest ground; and the south entrance opens through an abrupt straight tree cut.
- **Concrete Redesign Blueprint:**
  - **Retire flat-beige Sheridan roofs from Elowen woods:** Swap `sh_inn`, `sh_big`, and `sh_ell` in `120` Briarwick for **steep dark-shingle/moss-tinted Goldenleaf timber buildings (`gl_hall`/`gl_cot`/`gl_ell` with mossy-green roof remap)** or custom hollow-tree structures (`pf_g_*`), so every building harmonizes with the Gathering Tree and Elder Tree Loomhouse!
  - **Organic Stream Bend & Warm Timber Decks:** Meander the west stream gently eastward (`x=8 → 14 → 10`) around a mossy boulder dye-mill pool feeding the dye vats; re-plank the raised weavers' & lantern decks in warm weathered dark timber (`DECK` planks + subtle ground drop-shadow along their stilts) integrated directly against giant tree boles; and curve a low mossy forest ledge around the southern approach from Gossamer Wood.

---

## 3. Two Zero-Effort Cross-Map Stamp Bug Fixes (Immediate Wins!)

Even before scheduling full map redos, fixing these **two single-line stamp extraction bugs** in `mapgen/rstamps.yaml` immediately cleans up **5 shipped maps**:

1. **`sh_big` Stray Pine Tree on Roof (`mapgen/rstamps.yaml:14`)** — *Affects `120` Briarwick & `540` Thistledown Lea*
   - **Cause:** `rect: [14, 5, 12, 13]` includes a Sheridan pine tree overlapping the building's upper-right veranda tiles.
   - **Fix:** Add `clear:` coordinates over the stray pine tiles (or exclude the Sheridan tree row range in `deny:`)—and even better, replace `540` Thistledown Lea's Manor exterior with a proper steep-roofed gothic timber manor facade matching the gorgeous new `546` Thistledown Manor interior!
2. **`ak_rock2` / `dk_rock_big` Hollow Blue-Water Hole (`mapgen/rstamps.yaml:39`)** — *Affects `146` Saltmere Harbour, `147` Saltmere Old Town, `528` Marram Down*
   - **Cause:** The extracted 4×4 Akuwa offshore sea rock stamp has an empty transparent center cell, showing a sharp square pixel hole of blue ocean right through the middle of the boulder.
   - **Fix:** Fill the interior tile of `ak_rock2` (and verify `nt_rock_big` / `dk_rock_big`) with the matching solid rock-cap tile in `rstamps.py` / `rcustom.py` so offshore sea stacks read as solid weathered stone.

---

## 4. Attached Visual Mockups Index (`mockups/`)

| File | Description |
|---|---|
| [`mockups/compare_01_552_dyers_ford.png`](mockups/compare_01_552_dyers_ford.png) | Side-by-side Current vs. Target Concept for **552 The Dyers' Ford** |
| [`mockups/compare_02_140_saltmere.png`](mockups/compare_02_140_saltmere.png) | Side-by-side Current vs. Target Concept for **140 Saltmere** |
| [`mockups/compare_03_522_glassed_orchard.png`](mockups/compare_03_522_glassed_orchard.png) | Side-by-side Current vs. Target Concept for **522 The Glassed Orchard** |
| [`mockups/compare_04_926_glass_dunes.png`](mockups/compare_04_926_glass_dunes.png) | Side-by-side Current vs. Target Concept for **926 The Glass Dunes** |
| [`mockups/compare_05_608_lowlight_shattered.png`](mockups/compare_05_608_lowlight_shattered.png) | Side-by-side Current vs. Target Concept for **608 Lumen — The Lowlight (Shattered)** |
| `mockups/01_552_dyers_ford_target.png` … `05_608_lowlight_shattered_target.png` | Standalone high-resolution target visual concept plates for direct art/layout reference |
