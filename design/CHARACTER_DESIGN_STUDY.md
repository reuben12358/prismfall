# CHARACTER DESIGN STUDY: what makes a sprite character remarkable at a glance

Owner: Character Designer. Written 2026-11-17 for SPINE Revision 10, item 5.
Trigger: the user called Juno v4 "soulless" and "a recolor gender swap of Sword/Shield's grass gym leader [Milo]". He said,
"I need something that makes me excited when I see Juno." The problem is **design and personality, not pixel technique**.
Technique stays in `design/PIXEL_ART_NOTES.md`. This file is about what to draw, not how to place pixels.

Concept sheet for Juno (Phase 2): **`art/previews/08_juno_concepts.png`**. It is waiting for the user to choose a direction (see §8).

---

## 0. TL;DR

1. Every memorable sprite here starts from a **specific concept** (a maid haunted by flame, a cook who fights with a pot lid, a
   strict instructor, a museum worker), not from a **role** ("grass girl", "gardener"). A role produces a uniform, and a uniform
   produces an NPC.
2. The concept has to survive at 1× as **one big shape**. If the black silhouette alone doesn't name the character, the design
   fails, however clean the pixels are.
3. The shape needs **one bold, unexpected element**: something nobody else in the cast or the genre would carry or wear.
4. **The pose is the personality.** "Stand, smile, hold the ball up" is the default for NPC trainer classes. Almost nobody
   memorable uses it.
5. **The face thinks something.** Memorable faces are asymmetric: one brow up, a one-sided grin, gritted teeth, a hand thrust at the
   camera. A centred, symmetric, mildly smiling face reads as "pleasant" and is forgotten at once.
6. **Colour carries personality, not type.** Dressing a Grass character in green makes them a type mascot. The best use the type
   colour as an accent and give the costume a colour that says who they are.
7. Juno v1–v4 failed on all six counts at once (§2), and we then spent nine rounds polishing pixels on a design nobody had
   questioned.

---

## 1. The library (what was studied)

Everything is read-only reference. Downloads are in `/home/claude/ref/charrefs/<source>/`; the study sheets I made are in
`art/work/study/`, made with `art/tools/study/{pack,plate,sil,ttypes}.py`.

| Source | What | Count looked at |
|---|---|---|
| Rejuvenation (`Graphics/Characters/trainer*.png`, `Transitions/vsTrainer*`, `Faces`) | battle fronts (90-native small set + 180-native large set), VS busts, faces | 291 fronts, 132 VS, 13 faces |
| Reborn (same folders) | battle fronts (80 native), VS busts | 297 fronts, 98 VS |
| Desolation (same + `Faces`) | battle fronts, VS busts, speech portraits | 167 fronts, 56 VS, 90 faces. The local `Gameovers/` folder is **empty**, so there was nothing to study there. |
| Official, via Pokémon Showdown's sprite index (Gen 4/5 sprites, plus later-gen characters redrawn in Gen 5 style) | every Gen 4 and Gen 5 leader, E4 member, champion and rival, HGSS Johto leaders, and XY-to-SV leaders in Gen 5 style | 157 |
| Other pixel casts | Chrono Trigger (7 character strips + team palettes), FF6 (battle screenshot), Sea of Stars (press kit screenshots and art), Eastward (official site character art), Deltarune (key art, screenshots), Celeste (screenshots and portraits), Hyper Light Drifter (key art), Octopath (1 screenshot only) | ~50 images |
| Design writing | Ohmura and Sugimori on designing the Gen 5 cast (Nintendo Dream interview, translated by Lava Cut Content); Valve's *Illustrative Rendering in TF2* (character read order) | 2 |

To be precise about what was studied, sprite IDs were mapped to their characters by decoding each game's `ttypes.dat` with the safe
pure-Python marshal reader (`art/work/study/ttypes_<game>.txt`). That gives, for example, Rejuvenation 139 = Angie, 141 = Amber,
143/144 = Flora/Florin (Grass), and Reborn 96 = Florinia (Grass), 93 = Julia, 101 = Shelly.

**Could not reach:** The Spriters Resource, Bulbapedia/Bulbagarden Archives, every Fandom wiki, Reddit and PokéCommunity all
return 403. The Reborn forum disallows robots. Octopath's official sites are JavaScript-only. Octopath is therefore covered by a
single screenshot and is not used as evidence below.

**Study plates** (the annotated evidence for §3). Each one is a single image with a caption under every example:
- `art/work/study/plates/A_concept_not_role.png`: grass and gardener *role* designs vs. *concept* designs.
- `.../B_pose_is_personality.png`: twelve poses that are personalities.
- `.../C_silhouette_bold_element.png`: colour vs. pure-black silhouettes, with counter-examples (Rejuvenation's Flora, our v4).
- `.../D_face_with_attitude.png`: VS and portrait faces vs. our v4 head.
- `.../E_other_pixel_casts.png`: Deltarune, Chrono Trigger, FF6, Eastward, Sea of Stars, HLD, Celeste.
- Overview pages: `rejuv_0*.png`, `reborn_0*.png`, `deso_0*.png`, `vs_*.png`, `off_g4/g5/g6p_00.png`, `grass_4x_00.png`,
  `rivals_4x_00.png`, `ext_*.png`.

---

## 2. Why our attempts felt generic (the honest diagnosis)

Put v4 next to Milo, the Gardener trainer class, Ramos and Mallow (Plate A). It is the same costume:

| v4 element | Where it comes from | What it says |
|---|---|---|
| green dungarees, cream rolled shirt | Milo's palette (green + cream + tan), Mallow's overalls | "grass type" |
| kerchief/hat band over the head, satchel, gloves | the Gardener class, Ramos | "gardener" |
| standing, ball held up beside the face | May's stance; stock trainer classes | "a trainer" |
| centred face, mild closed smile | default | nothing |
| hair cloud | the one bold shape, but it's a blob. Eastward's Sam owns "tiny girl, giant hair cloud", and Sam's hair contrasts (white on black) where ours doesn't (auburn on orange-brown). | — |

**Role + type-colour costume + default pose + neutral face = a trainer class, an NPC.** Every v4 element answers "what is she?"
(a grass girl, a gardener). None answers "**who** is she?" (an earnest, chaotic, talkative 15-year-old who adopts things and hides
her fear under plant facts). The design sheet in `CHARACTER_ART.md` §8 encoded the role ("green dungarees with patched knees,
oversized gardening gloves, satchel spilling seed packets"). We then executed that sheet very well: nine rounds of hand edits,
selective outlines, hue-shifted ramps. Polish can't rescue a concept that is a costume.

Specific failures, checked against the principles in §3:
- **Concept:** none beyond the role.
- **Silhouette:** at 1× (Plate C) v4 is "hair blob on a standing figure". The details that were meant to carry her (kerchief knot,
  seed packets, satchel) disappear in the black silhouette, and nearly disappear in colour.
- **Bold element:** the hair cloud, which is the right instinct, but it's the *only* idea, and it isn't unexpected.
- **Asymmetry:** the pose is nearly symmetric and the face fully symmetric.
- **Props:** a satchel and gloves are what every gardener carries. They tell no story of hers.
- **Colour:** green, the type colour, as the uniform. That is the Milo comparison exactly.
- **Pose:** the stock "present the ball" stance. Juno talks constantly, runs everywhere and hugs people; the sprite does none of it.
- **Face:** pleasant, centred, closed-mouthed. Nothing she is thinking.

**Process lesson:** v1 to v4 iterated on *technique* (parametric → frankensprite → hand-drawn → pixel-by-pixel). The design itself
was never put to the user as options. From now on the order is: concept options → user picks → silhouette/pose block-in →
polish.

---

## 3. What makes a character remarkable at a glance (with evidence)

Valve's TF2 art team describes a read order: **silhouette first, then the internal value and colour pattern, then detail.** At 80 px
in a battle scene the player gets about two of those three reads. Everything below serves the first two.

### 3.1 A specific concept, not a role (Plate A)
- **Erika** (Grass) is *ikebana / a tea ceremony*: a kimono with autumn leaves, serene. **Cilan** (Grass) is *a waiter*; his
  broccoli hair is his only grass cue. **Brassius** (Grass) is *an avant-garde sculptor* caught mid-flourish. **Reborn's
  Florinia** (Grass) is *a strict head instructor*: ramrod-straight full bodysuit, glasses, ball held out like a pointer. Four
  Grass leaders, four concepts, and not one is a gardener.
- **Lenora:** the designers' first apron "made her look like an average mom", so they reframed it as a museum *work* apron
  (Ohmura/Sugimori interview). The prop was kept and the concept fixed. That is exactly our problem.
- **Garl** (Sea of Stars) and **John** (Eastward) are *cooks* who fight with a pot lid and a frying pan. The job is the kit, and
  the kit is the joke and the warmth at once.
- Counter-examples: **Milo, the Gardener class, Mallow, Rejuvenation's own Flora and Florin.** Flora, Rejuvenation's Grass
  leader, is one of that game's least memorable designs: green hair, a flower clip, a green dress, standing. The best fangame
  shares our trap.

**Rule:** write the concept as a noun phrase that is *not* the type or the job: "a girl who carries her world under glass", "a
maid haunted by flame", "a tycoon too busy to sit down" (Clay's phone and briefcase). Then filter the type through it.

### 3.2 Strong shape language (Plate C, Plate E)
- **Deltarune's key art** shows three pure black silhouettes against a cyan fire, and you can still name Susie (mane), Kris
  (fringe) and Ralsei (hat).
- **Chrono Trigger** and **FF6** at roughly 16×24 px: Crono's spikes, Marle's side ponytail, Lucca's helmet, Frog (a frog);
  Terra's green ponytail, Locke's bandana, Mog's pom-pom. Each has one head shape and one colour pair.
- **Fantina** is a bell: three hair balls and a ball gown. **Clay** is short, stout and hatted, deliberately: the interview says
  his body was chosen "to vary the Gym Leaders' body types". **Crasher Wake** is round, wide and flexing.
- Shape language carries meaning: round = warm and soft (Garl, Wulfric), triangles/diagonals = energy and danger (Amber's guitar
  hook, Lance's cape), verticals = rigour (Florinia, Voss).
- **Test:** fill the sprite black. If it could be anyone, redesign. (`art/tools/study/sil.py` writes these pairs.)

### 3.3 One bold, unexpected element
- **Rejuvenation's Angie** (`trainer139`) is a *maid* whose hair is a red ghost-flame bigger than her body. A mundane role plus one
  supernatural shape: the flame is the silhouette.
- **Valerie's** kimono sleeves are cut as butterfly wings. **Iono's** magnet hair and sleeves are three times her arm size.
  **Olympia's** cape is a starfield.
- **Reborn's Sandy** (`trainer129`) holds a placard reading MAKE LOVE NOT WAR. A prop that is a joke and a biography.
- **Eastward's Sam** is a tiny girl with a white hair cloud bigger than her body.
- The element should be *unexpected for the role*: a flame on a maid, stars on a psychic's cape, a protest sign on a trainer. The
  type-expected element (a flower on a grass girl) doesn't count.

### 3.4 Asymmetry
- **Rejuvenation's Amber** (`141`): the hook of her hair repeats the flying-V guitar, one diagonal rhythm across the body.
- **VS faces** (Plate D): one brow up and a one-sided smirk (Rejuvenation `vsTrainer192`), one eye hidden behind hair (Angie,
  Desolation 14e).
- **Our own cast already does this:** Kestrel's coat is a size too big, with the sleeves past his hands. Asymmetry reads as a life
  lived: something worn, carried, broken, chosen.

### 3.5 Props that tell a story
- **Clay:** a phone and a briefcase, "a busy man who does tasks himself" (interview). **Desolation's Backpacker** (`trainer044`)
  scratches his head under a pack bigger than he is. **Desolation's Channeler** (`012`) holds two lit candles mid-incantation.
  **Rejuvenation's Diabolical Genius** (`229`) juggles Poké Balls.
- A prop should answer a story question: what does she do all day, what is she afraid of, what does she love. A satchel answers
  nothing.

### 3.6 Colour that carries personality
- **Hyper Light Drifter** has no face at all: a magenta cape and a cyan blade *are* the character. **Celeste**: Madeline's hair
  colour is game state (red = dash ready, blue = spent), so colour means something.
- **Angie:** red flame against cyan hair and a black-and-white maid uniform. The colour contrast is the drama.
- **Chrono Trigger's** team palettes: one dominant colour pair per hero, never shared.
- **Type colour as accent, not uniform:** Erika is ochre and orange (autumn), Cilan is black and white (waiter), Florinia's green is
  a severe bodysuit, not leaves. Dress a Grass character head to toe in green and you get Milo.

### 3.7 A pose that IS the personality (Plate B)
- **Reborn's Serra** (Beauty Queen) *reclines on the floor*. **Alder** (Champion) *sits cross-legged*. **Burgh** is *mid-jump*,
  arms flung wide. **Bianca** *kicks one heel up*, leaning, the ball hugged to her chest: "a pure-hearted girl who dances to the beat
  of her own drum". **Penny** *hides inside an oversized Eevee hoodie*: anxiety as costume. **Elesa** sprawls like a model.
  **Rejuvenation's Puppet Master** cocks a hand as if working strings, and its **Dance Prodigy** strikes a disco point. **Reborn's
  Shelly** is small and turned in.
- If the personality is "talks constantly and runs everywhere", the sprite must be talking and running.

### 3.8 A face with attitude (Plate D)
- Gritted-teeth grins, open-mouthed shouts, a hand thrust at the lens bigger than the head (Rejuvenation `vsTrainer210`,
  `240`, `131`). Desolation's portraits tilt the head and crop through the crown. Celeste's "I can't breathe" portrait is anxiety on
  a tiny face.
- At 80 px a face is about 12 px wide. Attitude comes from **brows (2–3 px), mouth shape (open/teeth/one-sided) and head tilt**,
  not from detail.

### 3.9 Contrast with the cast
- **Eastward** pairs huge silent bearded John with tiny loud Sam. Sugimori chose Clay's body to vary the gym. Kestrel and Juno
  are a comic pair ("The Committee", `15_COMEDY.md`). Their silhouettes must differ as much as their temperaments: he is a sharp
  black V, so she should be round, warm, cluttered and moving.

---

## 4. Notes by source (what each taught)

- **Rejuvenation:** its best designs (Angie, Amber, Puppet Master, Diabolical Genius, Dance Prodigy, Narcissa the actress
  in a sweeping gown) each have one outrageous shape and a performance pose. Its VS busts are the gold standard for attitude:
  every one has a gesture into the camera. Its weak designs are its "nice" ones (Flora, Florin, generic grunts).
- **Reborn:** more grounded and smaller (80 px), so personality lives in posture. Florinia's rigidity, Serra lying down, Shelly
  shrinking, Julia's cheer kick with pom-poms, Radomus's top hat and cane, El's huge parson's robe, Sandy's placard. Reborn proves
  that the pose can carry a design when the costume is plain.
- **Desolation:** strong props and absurdity (Channeler's candles, Backpacker's giant pack, Jarred's lunging speedo pose, the
  biker on a motorcycle). Its portraits use 3/4 tilt, crown crops and per-frame expressions.
- **Official Gen 4/5:** nearly every leader has a costume concept (wrestler, model, painter, tycoon, pilot, museum mother) and a
  unique pose. The NPC classes use the stock stand. Our v4 used the class pose for a leader.
- **Later leaders in Gen 5 style:** Valerie, Olympia and Iono show how far a silhouette can be pushed in this format and still
  read.
- **Chrono Trigger / FF6:** identity at 16 px = head shape + colour pair. Idle animations carry personality (Marle bounces,
  Magus broods).
- **Sea of Stars / Eastward:** the warm characters are round, carry their trade, and are funny through body language.
- **Deltarune / HLD / Celeste:** silhouette alone (Deltarune), colour alone (HLD), colour as meaning (Celeste).

---

## 5. Cliché list (avoid unless deliberately subverted)

| Role | Cliché kit | Seen in |
|---|---|---|
| Gardener / Grass | dungarees or overalls, straw or bucket hat, gardening gloves, watering can, shears, all-green outfit, flower hair clip | Milo, Gardener, Ramos, Mallow, Rejuvenation's Flora/Florin, **our v3/v4** |
| Bug | wide straw hat + butterfly net, shorts | Bugsy, Desolation and Rejuvenation bug catchers |
| Fire | flame-shaped red hair, headband, open jacket | Flint, Chili, countless |
| Water | swimsuit or sailor collar, blue hair, ponytail | — |
| Ice | white fur trim, snowflake clip, blue scarf | Candice-alikes |
| Electric | lightning-bolt motif, yellow + black, rocker look | Volkner, Elesa-alikes |
| Ghost | black lace, veil, purple, pale skin | — |
| Psychic | floating, closed eyes, spoon | Sabrina-alikes |
| Scientist / professor | lab coat, glasses, clipboard | Colress, Juniper, every scientist |
| Rival (friendly) | "same as the player but in another colour", backpack, peace sign | — |
| Rival (aggressive) | spiky hair, red/black, jacket, hand in pocket | Silver-alikes (watch Kestrel here) |
| Any | **stand straight, ball held up beside the face, closed smile** | stock trainer classes, **our v4** |
| Any | type colour head to toe | Milo, Flora |
| Any | a "signature" made of small details that vanish at 1× (packets, pins, freckles as the main hook) | **our v3/v4** |

Using a cliché element is fine if *one* bold idea dominates and the cliché is subverted. Lenora's apron became a work apron; Angie
is a maid, but a maid on fire.

---

## 6. The excitement checklist (answer before any block-in)

1. **Concept:** a noun phrase that is not her type or job. Would a stranger *want to know more*?
2. **Silhouette:** draw it black at 1×. Does it name her? Is it different from every other cast silhouette (CHARACTER_ART §8)?
3. **Bold element:** the one thing nobody else would carry or wear. Is it the biggest shape?
4. **Story:** does the bold element encode her *personality and her fear*, and can it change with her arc?
5. **Pose:** what is she *doing*? It must not be "standing, presenting a ball".
6. **Face:** what is she *thinking*? Brows, mouth and tilt. Asymmetric?
7. **Colour:** a pair that says who she is, with the type colour as an accent only. Is it unused in the cast?
8. **Comedy:** does the design make a gag possible (15_COMEDY: "a line is funny because of who says it"; the same goes for
   shapes)?
9. **Scales:** does it survive the 16–20 px overworld and the 96 px portrait?
10. **Cliché scan:** nothing from §5 unless subverted.

---

## 7. Who Juno is (the brief the drawings answer)

From `story/03_CAST.md` and `story/15_COMEDY.md`:
- 15, freckled, frizzy auburn hair. Larch's assistant. Hale's Bramble berry farm. Spent childhood summers in Verdance with "Uncle
  Rowan", her hero.
- **Earnest chaos** (Comedy B, "The Committee"): narrates plant facts at dramatic moments, adopts things, named the trio "Team
  Compost" ("we break things down and make them better!"), hugs Kestrel without warning, waters a plant with Larch's tea and kills
  it.
- Picks the underdog starter: "somebody should give the underdog a chance. Also it was looking at me." Braver than she knows.
- **What she is secretly afraid of:** losing the people she loves to things that won't let go. Aunt Elin "went away" when Juno was
  three: she was Fixed into the Bride Tree, which never stops blooming. Then Rowan, her hero, turns out to be the Mourner. Her
  "anxiety hides under a constant stream of plant facts". Under the seat she inherits: "I didn't want this seat. I wanted *him* in
  it." Her thesis line is about larches: they drop their needles "so they don't snap". Her arc ends with letting go: "Verdance has
  never had an autumn. I'd like to see one."
- Team: the underdog starter; **Bounsweet → Steenee → Tsareena** (grown from a seed-pod in Act I; ace), Whimsicott, Lilligant,
  Comfey, Shiinotic.

---

## 8. Phase 2: four Juno concepts

Sheet: **`art/previews/08_juno_concepts.png`** (1× on two backgrounds, 4×, beside Bianca (official BW) and Rejuvenation's Angie,
with v4 shown small as "before"). The favourite's portrait is on the same sheet. Sources: `art/tools/concepts/c1_greenhouse.py`,
`c2_compost.py`, `c3_seedbomb.py`, `c4_everbloom.py`, `c1_portrait.py`, `sheet.py`. Outputs and `.spr` files are in
`art/work/concepts/`. The thumbnails are deliberately quick block-ins (flat colour, an automatic cel shade, a dark outline), **not
polished**.

### Concept 1: UNDER GLASS (the walking greenhouse)
- **Pitch:** a girl who carries her whole world under glass, a walking greenhouse of rescued plants (and the seed-pod that becomes
  Tsareena), because she can't bear to lose one more thing.
- **Silhouette:** a small running figure with a tall, peaked glass house on her back, taller than her head. A roof vent and a sprout
  break the outline. Nothing else in Pokémon looks like this.
- **Signature element:** the greenhouse pack: brass frame, glinting panes, a tangle of plants, Bounsweet peeking out of the roof
  vent, paper labels in tiny handwriting, and **one cracked pane**.
- **Pose:** mid-run toward you, leaning in, one arm flung out offering the ball like a hug, back heel kicked up, mismatched socks.
- **Face:** brows up, green eyes wide, mouth open mid-plant-fact.
- **Colour:** blackberry-purple knit (Hale's Bramble) + brass and glass. Green lives *inside the glass* only. This pair is not used
  in the cast; Thistle's purple is an accent on ash.
- **Story:** she adopts everything, and here she carries it all. Her ace grows in it from Act I. The fear is the design: she keeps
  what she loves sealed and safe, which is exactly what Verdance's Imprint does to her aunt. The pane cracks when Rowan is unmasked.
  As Warden (J3) the glass comes out and the frame becomes an open trellis, with flowers spilling over. In the finale she opens it:
  "I'd like to see an autumn."
- **Comedy:** it clinks when she runs. She has to set it down very carefully before every battle. Kestrel gets made to carry it
  ("I'm not in the team." "You're holding our greenhouse."). Larch's tea goes in the watering slot.
- **Risks:** a big pack crowds a battle front (handle by placement), and the overworld version needs a 6–8 px peaked box (doable).
  `03_CAST`'s look line (kerchief, satchel of seed packets) would change: the packets become labels, the kerchief a pencil-stabbed
  hair puff.

### Concept 2: ROT & BLOOM (the compost forager)
- **Pitch:** Verdance is the city where nothing ever rots; Juno is the girl who thinks rot is the most beautiful thing in the world.
  A gleeful little toadstool of a forager.
- **Silhouette:** she *is* a toadstool: a huge tilted cap over a squat, coat-pooled mound, knees out.
- **Signature element:** a violet toadstool rain hat with cream spots and baby mushrooms growing on it, a glowing mushroom in her
  fist, a jar of worms on her belt.
- **Pose:** squatting low and thrusting the glowing mushroom at your face. Toothy grin, eyes lit from below: "LOOK at it."
- **Colour:** loam umber + spore-violet glow.
- **Story:** Team Compost taken as a creed. It is Rowan's lesson made flesh ("Everything that grows must be allowed to die... That's
  what makes room") and the Mourner's charge ("Ask your Warden why nothing in Verdance ever rots"). Her Shiinotic. The cheerful
  decomposer in a city that can't decay. Her fear is the never-dying tree.
- **Comedy:** offers everyone mushrooms, names her worms, and is the only person delighted by the Weeping Fen.
- **Risks:** a mushroom cap can read as Mario's Toad or Morelull cosplay. It is fungal rather than floral (her ace is Tsareena).
  The squat hides her body, so it's less athletic.

### Concept 3: SEED BOMBER (the guerrilla gardener)
- **Pitch:** earnest chaos, literally: a guerrilla gardener who lobs seed bombs at every bare patch of ground, and at most of her
  problems. She backs every underdog, weeds included.
- **Silhouette:** a pitcher's windup, a hard diagonal from the cocked fist to the planted foot, with the frizzy ponytail streaming
  the other way.
- **Signature element:** a bandolier of clay seed bombs (one of them is her Poké Ball), a slingshot in her back pocket, a terracotta
  sweatband.
- **Pose:** the windup: front knee high, one arm pointing at the target, tongue out, one eye squeezed shut to aim.
- **Colour:** dandelion yellow + clay terracotta.
- **Story:** the underdog-picker. Weeds are the ultimate underdog. Her high knee prefigures Tsareena's kicks. Seed bombs heal
  Bleed-scarred ground. The irony is that the seed bomber inherits a city "drowning in flowers". Her fear is hidden by never
  standing still.
- **Comedy:** "It's not vandalism, it's reforestation." She has seed-bombed Kestrel, and that is a numbered lecture.
- **Risks:** the closest to a stock "sporty girl" (Whitney, Candice), the yellow sits near Larch's mustard, and the face reads
  least of the four.

### Concept 4: EVER-BLOOM (the flower girl of a wedding that never ended)
- **Pitch:** she was three when her aunt became a tree in permanent bloom. She has worn its never-wilting blossoms every day since.
- **Silhouette:** a tilted wreath and a long cascade of blossoms falling behind her to the ground like a bridal train.
- **Signature element:** the Bride Tree's blossoms (Imprinted, so they never die), with tiny prism glints on the petals. An
  outgrown flower-girl pinafore with the hem let down.
- **Pose:** still and shy, toes turned in, ball held like a bouquet, smiling with eyes a little too bright.
- **Colour:** blossom white + pink, with the auburn hair.
- **Story:** grief worn openly. She bonds to the Meadow Plate at the Bride Tree's roots. In the finale autumn comes, the wreath
  finally wilts, and Elin wakes.
- **Comedy:** the weakest of the four. The joke would have to be the contrast between the angelic look and the plant-fact
  firehose.
- **Risks:** it reads as "flower girl / bride", close to the clichés (Flora, Mallow), and it is the least "earnest chaos". It is
  strongest in portraits and cutscenes and weakest at 1×.

### Recommendation: **1, UNDER GLASS**
It is the only concept whose bold element is all of these at once:
- **the silhouette:** a glass house on a running girl reads at 1× and on the overworld;
- **the personality:** she adopts and carries everything;
- **the joke:** it clinks, it's absurd, and Kestrel has to carry it;
- **the fear:** she keeps what she loves under glass, as Verdance keeps Elin;
- **the arc:** a cracked pane, then an open trellis, then letting go for autumn.

No Pokémon Grass leader has anything like it, and it uses none of the §5 clichés: no hat, no dungarees, no green clothes. Concept 2's
compost humour can live inside it (mushrooms in the greenhouse, worm labels) if wanted.

Portrait for the favourite: `art/work/concepts/c1_portrait.png` (96×96 native, "happy / mid plant-fact", finger raised). It is
shown on the concept sheet at 1×, at 3× and in a speech-bubble circle.

**Next step (after the user chooses):** a clean silhouette and pose block-in at 80×80, then the CHARACTER_ART §8 sheet row is
rewritten from the chosen concept (not the role), and only then the PIXEL_ART_NOTES polish pass. Apply the §6 checklist to Kestrel
and the rest of the cast before drawing them.

---

## Sources (web)
- Ohmura and Sugimori on Gen 5 character design (Nintendo Dream, translated): https://lavacutcontent.com/ken-sugimori-nintendo-dream-4/
- Mitchell, Francke and Eng, *Illustrative Rendering in Team Fortress 2* (Valve): https://www.cs.princeton.edu/courses/archive/fall07/cos597B/papers/mitchell-team-fortress.pdf
- Official trainer sprites (Gen 4/5 and Gen 5-style redraws): https://play.pokemonshowdown.com/sprites/trainers/
- Sea of Stars press kit: https://sabotagestudio.com/presskits/sea-of-stars/
- Eastward character art: https://www.eastwardgame.com/
- Deltarune: https://deltarune.com/ · Celeste: https://www.celestegame.com/ · Hyper Light Drifter: https://heartmachine.com/
- Chrono Trigger sprite strips: https://scalar.usc.edu/works/chronicles/ and https://www.chronocompendium.com/Term/Official_Art.html
- FF6, Octopath and HLD screenshots: Wikipedia (upload.wikimedia.org)
