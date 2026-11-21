# PRISMFALL CHARACTER STYLE GUIDE (v1, 2026-11-20)

For the pixel artists who make our cast: dialogue portraits, battle fronts, overworlds and VS bars. Every rule here can be
checked: a number, a colour, a pixel position or a yes/no test. §9 maps each rule to the reference pieces it came from.
Sources: `art/research/SOURCES.md`. Study boards: `art/research/moodboard_{portraits,characters,pixel}.png`.
Worked example: `art/previews/27_style_test.png` (Juno refresh, Dorian Pell new), recipes in `art/research/scripts/`.

**Our art must be original.** We learn principles from the references. We never trace, copy or recolour a specific piece or
character. Before anyone sees new art, ask: *who does this look like?* (§2.8)

---

## 0. The target in one paragraph

**Clean, bright and big-eyed, like the official Black 2/White 2 VS art, with the design depth of the Rejuvenation cast.**
The anchor is Juno's accepted portrait, pass 3 (`art/out/Graphics/Portraits/JUNO*.png`, SPINE Rev 17). It is 48-px art shown
at 2x, with black outlines, 2–3 flat tones per material, large eyes with one highlight, warm saturated colour and about 30 colours.
The user rejected the more realistic, painterly Rejuvenation/Desolation faces (pass 5), any "choppy" or "muddy" texture
(1-px black strand lines inside hair, Kitbash §12), anything that resembles a known character (the "Burgh in a wig" portraits), and
pixel-by-pixel drawing that wasn't designed first (Rev 11, "god awful"). From Desolation we take only its *format*: a framed
96x96 face beside the message box (Rev 22).

### What the study found (the ten things that make the references work)
1. **Silhouette first, then value, then colour.** honnojis' own ref sheets start from 24 black silhouette thumbnails, narrow
   to 4 greyscale value roughs, and only then go to colour and turnarounds (`juno_ref_portfolio`, `damian_ref_sheet_v3`, `pom_ref_sheet_v3`).
2. **Few colours, flat.** An official B2W2 VS bust uses only **14–15 colours** for a 128x64 bust. Desolation faces use 22–39 colours
   at 48x48, honnojis' 100-px pixel faces 21–22. "Clean" in practice means few tones per material, no blends and no noise.
3. **One accent against a calm base.** Pom is brown, green and black plus pale-blue denim; Damian is black and plum, with the rose as
   his accent; the B2W2 VS bars are each one hue. The accent covers at most about a tenth of the figure.
4. **Hue-shifted shadows, never grey.** honnojis shades skin toward rose and violet and hair toward plum. Desolation's silver
   hair (Face 22) is shaded in blue-greys. Neutral grey shadows are what read as "muddy".
5. **Tinted dark lines inside, darkest lines outside.** honnojis' pixel pieces outline with plum `#2d1e2f`, not black, and draw
   interior lines in each material's darkest tone. B2W2 and Desolation keep the silhouette and the lash line near-black.
6. **Eyes carry the character.** Every reference eye has a heavy upper lash (2 px at 48–100 px, with a flick at the outer corner),
   a two-tone iris, one hard highlight, and a lower lid drawn in skin shadow rather than black.
7. **Hair is 3–6 sculpted clumps** with tapered tips and one highlight arc per clump. It is never a helmet and never strands.
8. **Mouths are shapes, not dots.** A closed mouth is a line whose corners act. An open mouth is an outlined hole with a dark inside,
   a row of teeth under the top lip and a tongue at the bottom (Skyla VS, Pom, Damian, honnojis chibis).
9. **The pose or gesture is the personality.** In VS art a hand in the foreground (pointing, a ball, a prop) does as much as the face
   (Skyla, Lenora, Roxie, Reborn 227's card, NoodlesXL's "VS Alice").
10. **Plates, not scenery.** Portraits sit on a flat plate: honnojis' chibis on a flat colour disc, angeceleste's icons on flat
    colour with a 1-px light rim, Fiorne's portraits in a bordered frame beside the text, Desolation's on the window skin.

---

## 1. Process (every character, in this order)

| Step | Output | Gate |
|---|---|---|
| 1. Concept | a noun phrase that is not the type or the job ("the curtain call that never ended") + 3 traits | `design/CHARACTER_DESIGN_STUDY.md` §3.1 |
| 2. Silhouettes | 6–12 black thumbnails at the real size (80-px front or 48-px bust) | §2.1 test passes for one of them |
| 3. Value rough | the pick in 3–4 greys | the face and the hook are the two brightest/most contrasting areas |
| 4. Colour plan | 3 colours + 1 accent, ramps built per §2.5 | §2.4 counts |
| 5. Pixels | portrait (§3), front (§4), overworld (§5), VS (§6) | the §3.12 checklist, then a review sheet at 1x/2x beside Juno pass 3 |
| 6. Review | an independent critic (Rev 11), then the user | "who does it look like?" (§2.8) asked and answered on the sheet |

---

## 2. Character design rules

### 2.1 Silhouette first
- [ ] Fill the sprite black on a light plate at **1x** and at 2x. A stranger must be able to tell the main cast apart from the black shapes alone.
- [ ] Each main-cast member owns **one shape nobody else in the cast uses**: Juno's tilted wreath and veil train, Dorian's
      swept-back mane with its forward crest, Kestrel's oversized coat collar, the Mourner's antler crown. Write it on the sheet.
- [ ] The silhouette must have **at least 3 breaks**: tips, notches, a prop or a gap between arm and body. A smooth oval head or a
      "helmet" of hair has none and fails (faces_v1 Dorian, sheet 26).
- [ ] Shape language: round reads warm and soft, triangles and diagonals read as energy and threat, verticals read as rigour.
      Pick the dominant one from the personality (Dorian: diagonals for showman energy; Juno: rounds and a flowing train).
- [ ] Avoid known reads: a long mane, a high stand-up collar and plum together read "vampire" (sheet 27 silhouette E; the
      rejected Juggler body); a spiky crest with a red scarf reads "shonen hero".

### 2.2 Concept, not role
Follow `design/CHARACTER_DESIGN_STUDY.md` §3. In short: the costume answers *who* the character is, not *what type* they are.
The type colour is never the uniform (the Milo trap). One unexpected element, an asymmetric pose and a face that is thinking something.

### 2.3 Distinct faces: the face-shape kit (48-px portrait grid)
No two main-cast faces may share the same **jaw + eye + brow** combination. Pick one row from each table; record the picks on the review sheet.

| Jaw template | Face width at the eye line | Chin | Jaw turn | Use for |
|---|---|---|---|---|
| J1 round | 24–26 px | 5–6 px wide, round | starts 6 rows under the eye line, smooth curve | children, warm teens (Juno) |
| J2 sharp V | 22–24 px | 2–3 px, pointed | straight diagonals from the cheekbone, a 1-px notch under it | sharp teens (Kestrel), sly adults |
| J3 square | 24–27 px | 6–7 px, flat bottom, optional 1-px cleft | turns at the mouth row, 2–3 px corner | adult men (Dorian), soldiers (Valen) |
| J4 long | 22–24 px | 4–5 px | late turn, 2 rows below the mouth | lean or old men (Voss, Rowan) |
| J5 broad | 27–30 px | 7+ px, heavy | wide cheeks, short neck | Edda, big laughing types |

| Eye template | Opening (rows) | Width | Iris | Lid |
|---|---|---|---|---|
| E1 big round | 6–8 | 6–7 | 3–4 wide, 4–6 tall | 2-row lash, no crease (Juno) |
| E2 almond sharp | 3–4 | 6–7 | 2–3 wide | lash angled, outer corner 1 row higher (Kestrel) |
| E3 hooded | 3 | 5–7 | 2 wide x 3 | lid crease 1 row above the lash in skin shadow (Dorian, Larch) |
| E4 narrow | 2 | 5–6 | 2x2 | heavy lash, crow's-foot pixel (Voss, Valen) |

| Brow | Rows | Use |
|---|---|---|
| B1 soft | 1 row, 4–5 px, hair-dark tone | Juno, gentle people |
| B2 strong | 2 rows, 6–7 px, thick at the inner end | Dorian, Kestrel, Valen |
| B3 arched | 2–3 rows, a peak 1–2 rows above the ends | the vain or knowing one (Dorian's far brow) |

Also vary the **nose** (none / 1-px shadow / a bridge line + dark underside for adults) and **age marks** (none / under-eye line /
crow's foot / nasolabial line, each 1 px of skin shadow, never black).

### 2.4 Three colours + one accent
- [ ] **Three costume colours** (main ~60% of the costume, second ~30%, third ~10%) **plus one accent** (≤ 5% of the figure: a rose, a
      gem, an eye colour, a lining). Skin, eye whites and the outline do not count.
- [ ] The accent is the most saturated colour on the character and appears **1–2 times**, never more (Damian's rose and gem; Pom's
      green against brown and black).
- [ ] The type or kingdom colour appears as the second colour, third colour or accent, **not as the main one**.
- [ ] Each colour has a ramp of 3–4 tones (§2.5). A 48-px portrait has **≤ 32 colours**, an 80-px front **≤ 36**.

### 2.5 Ramps: how to build each tone
Light comes from the **upper left** for the whole cast, everywhere.
- **Base:** the local colour.
- **Shadow:** hue rotated 8–20° toward red or violet (toward blue-violet for cool or white materials), saturation +5–15%, value −15–25%.
- **Deep or line tone:** a further step of the same kind (value −35–50% from base). It is used for creases and interior lines.
- **Highlight:** hue rotated toward yellow (warm materials) or cyan (cool), saturation −10%, value +10–15%. Use it sparingly, as single arcs.
- **White, silver or grey materials** get lavender or blue-violet shadows (Dorian `cdc8e6 → a29bc6 → 6e6698 → 4a4274`), never neutral
  grey. Black materials are dark plum or navy, with the lightest tone used as the sheen.
- [ ] No two ramps may share a mid tone; that is how a mouth ends up purple (Kitbash §4). Region-based recolours only.

### 2.6 Kingdom motifs (costume, not architecture)
Cloth colours match `design/ART_DIRECTION.md` §4. Use the kingdom colour as the second colour, third colour or accent.

| Kingdom (types) | Signature colours | Materials and motifs | Silhouette cues | Avoid |
|---|---|---|---|---|
| **Elowen** (Grass, Fairy, Bug, Normal) | leaf `#2F8A4A`, cream linen, berry pink; lantern-gold thread | embroidery borders, leaf-cut hems, petals, thorns, silk | hoods, short capes with scalloped or leaf-cut hems, wreaths | an all-green uniform |
| **Ossaria** (Ground, Rock) | sand `#C8963A`, terracotta, bone white; turquoise accent | wraps, goggles, fossil and ammonite jewellery, bone toggles, sun discs | layered wraps, trailing scarves, goggles pushed up | "desert costume" clichés: carry the fossil and bone theme |
| **Isenmar** (Water, Ice) | slate/ice blue `#3A7AB8`, whalebone white, sea-teal; ember-orange accent (the hearth) | furs, bone toggles, knotwork, rope, wave curls | bulky fur collars, mitts, hoods: broad, low shapes | horned helmets |
| **Ashkaar** (Fire, Dragon) | lacquer red `#B02A20`, basalt black, bronze/gold; ember or jade accent | lacquered scale, horn and claw points, oath cords | sharp pauldrons, tall collars, triangular hems | flame prints everywhere: use scale and horn |
| **Zenith** (Electric, Steel, Flying) | clean white, brass, glass teal `#2A9A9A`; signal-yellow accent | brass trim, lenses, rivets, piping, pressed seams | crisp verticals, high collars, goggles or monocles | glued-on gears (steampunk clutter) |
| **Nadir** (Poison, Dark, Fighting) | soot grey, leather brown, chem green `#4A8A20`; magenta-neon or lantern-orange accent | patches, visible stitches, straps, rebreather filters, Hollow-grey | asymmetric layers, hoods, one bulky glove | generic punk spikes |
| **Crownhaven** (all; the Accord) | pale-gold stone, royal blue `#2A3A9A`, white; a prism edge as the accent (thin lines only) | bells, the crown ring, eight-pointed stars, faceted prisms | long vertical robes and stoles | rainbow everything |
| **Antumbra** (Ghost, Psychic, Dark) | ink violet `#5A3A8A`, mirror silver; pale-gold candle accent | veils, mirror-silver, **mismatched gloves** (left for the living, right for the dead) | veils, split or mirrored halves | the "grim reaper" robe |

**Type motifs.** Each type is one *idea*, filtered through the character's concept and shown in the accent or one prop: Normal
is the everyday made into theatre (Dorian), Grass is growth or bloom (Juno's blossoms), Bug is thread and silk (Tamsin), Water is a
current or tide, Fire is forge or oath, Ice is glaze or rime, Electric is a signal or spark, Ground is strata, Rock is a facet or
gem, Flying is a feather or the wind in the cloth, Psychic is an eye or a mirror, Ghost is a lantern or an echo, Steel is a tool
or a joint, Dark is the moon or a mask, Fairy is ribbon or dusk, Dragon is horn or scale, Poison is a stain or a filter, Fighting
is wraps or knuckles.

### 2.7 Costume construction
- [ ] **Three layers** that read at 1x: base (shirt or dress), mid (vest, sash or wrap), outer (coat, cape or veil). Each layer gets
      its own value step, so the layers separate in the greyscale rough.
- [ ] **One hero prop** that tells a story (Dorian's cane he doesn't need, Juno's bouquet, Kestrel's oversized coat). Props come from
      the character, never from the type chart.
- [ ] **A motif repeats 2–3 times at most** (Damian's rose: brooch, hair stripes, sleeve). Stamps repeated more than twice read as
      stamps (Kitbash §5).
- [ ] **Asymmetry:** one-sided drape, collar, glove or hair lock. A fully symmetric design reads as an NPC.

### 2.8 Originality check (must appear on every review sheet)
- [ ] "Who does this look like?" Check against the official characters in the same role, against the donors, and against the
      Rejuvenation, Reborn and Desolation casts. Write the names you checked on the sheet (sheet 27 does).
- [ ] No piece of a reference image is traced, painted over or recoloured. Kitbash donors follow `design/KITBASH_PIPELINE.md` and
      are not used for main-cast portraits (§3.11).
- [ ] A recolour of a recognisable head is a fail, however good (Rev 13: "Burgh wore a wig").

---

## 3. Dialogue portrait spec (96x96, main cast only, SPINE Rev 22)

### 3.1 Format
- `Graphics/Portraits/<NAME>_<expr>.png`, **96x96 RGBA, 48x48 art doubled** (every art pixel is a 2x2 block). Alpha is 0 or 255 only.
- Shown in Essentials' face window: a 128x128 box, left-aligned above the message box (Desolation's layout; mock in sheet 27).
- Required expressions: `neutral, happy, sad, angry, surprised` + 1–2 signature ones (Juno `wink`; Dorian `laugh`). The user removed
  Juno's separate shocked face: `shocked`/`panic` point at `surprised`.

### 3.2 Framing on the 48-px grid
| Feature | Rows (y) | Columns (x) |
|---|---|---|
| top of the hair silhouette | 0–3 (the outline closes inside the frame unless the hair deliberately breaks the top) | |
| brow line | 17–21 | |
| eye line (iris centre) | **22–27** (Juno 27, Dorian 23) | face centre at x 22–28 |
| nose tip | 28–32 | |
| mouth | 33–37 | |
| chin | **40–44** (Juno 43, Dorian 42) | |
| shoulders and collar | 40–47, reaching the frame's left and right edges | |
| face width at the eye line | 22–30 px (§2.3) | |

- [ ] **Facing:** frontal, or 3/4 turned **toward screen right**, toward the text. Eyes look at the viewer or to the right, never to the left.
- [ ] **Whole head in frame.** Unlike Desolation, which crops into the hair, our heads fit (Juno pass 3): the hair silhouette is
      the hook and must be visible. A hat or crest may touch row 0.
- [ ] One head size for the cast: heads differ in shape, not in scale (face height brow-to-chin 20–24 rows).

### 3.3 Outlines and lines
- [ ] **Silhouette outline:** 1 px, near-black, luminance below 10% (`#000000` for Juno pass 3; new art may use a tinted near-black
      such as `#1a1220`). Never 2 px at 48-px scale.
- [ ] **Feature lines** (upper lash, inner corner, brow underside, mouth line on open mouths) are the outline colour.
- [ ] **Material boundaries:** black where hair meets skin and where clothes meet skin or a different garment. The same material folding
      onto itself (a hair clump over a clump, a cloth fold, the jaw over the neck) uses that material's **darkest tone, not black**.
- [ ] No black inside a hair mass except the boundary lines above. 1-px black strand stripes read as "choppy" (Kitbash §12).
      Exception: Juno's accepted portrait keeps its legacy pass-3 lines below the eye line. Leave them alone.
- [ ] The far jaw and cheek take the skin's deep tone inside the black silhouette line (selective outlining, Reborn and Desolation).

### 3.4 Tones and colours
| Material | Tones | Notes |
|---|---|---|
| skin | base, shadow, deep (+ 1 highlight, optional) | shadow: a 1-px band under the hairline, down the far side (2 px), under the nose and lower lip, the neck under the jaw |
| hair | highlight, light, mid, shadow + crease | §3.7 |
| each cloth | 3–4 | velvet: a lighter sheen on the lit shoulder |
| eyes | white, iris dark, iris light, highlight | the highlight is pure white, 1 px (2 on large eyes) |
| total | **22–32** | count with `tools/kitbash/lint.py` |

- [ ] No dithering, no anti-aliasing against transparency, no semi-transparent pixels.
- [ ] **No orphans:** a pixel with fewer than 2 figure neighbours is deleted, except eye highlights, freckles and the nostril.
- [ ] Clusters are at least 2 px, except deliberate features. Noise reads as "muddy".

### 3.5 Eyes (stamp patterns at 48-px art, not anyone's exact pixels; K = outline, E = white, a/A = iris dark/light, W = highlight, s = skin shadow)
```
E1 big round (Juno, 7x7)   E3 hooded, adult (Dorian)    E3 far eye (3/4)     happy shut (laugh)   surprised
  KKKKKKK                    ssssss                       ssss                  KKKK               KKKKKKKK
 KK EEEE K                  KKKKKKKK                     KKKKKKK               K    K              KEEaaWEK
 KEEaaWEK                   KEEEaWEs                      EEaWK               K      K             KEEAAAE
 KEaaaaEK                    EEEAAE                       EEAAK                ssssss               EEAAaE
 KEAAAAEK                     EEAas                        EAa                                       EEEE
  EEAAEE                      sssss                        sss                                       ssss
   ssss
```
- [ ] Upper lash 1–2 rows with an outer flick of 1 px. The lower lid is skin shadow, 3–5 px, never a closed black ring.
- [ ] The iris is two-tone, darker at the top under the lid. One highlight, top-right of the iris (the light is upper left, the
      eye is a sphere), the same place on both eyes and in every expression.
- [ ] Both irises point the same way. The far eye in 3/4 is 1–2 px narrower, never smaller in height.
- [ ] Expressions change the brows, lids and mouth; the eye *stamp* moves as a whole. Redrawing a few pixels inside an accepted eye
      fails (Juno shocked fix, Kitbash §12).

### 3.6 Mouths that read as mouths at 96x96
The sheet 26 problem: surprised and angry mouths drawn as a red blob read as lipstick. Rules:
- [ ] **Closed mouth = a line, 5–9 px wide**, in a dark warm tone (`#8e3a40` family), not black and not red. The **corners carry the
      expression**: up 1 row (smile), one corner up (smirk/knowing), down 1 row (sad), pinched flat (angry).
- [ ] **The lower lip is a skin-shadow dash** 2–4 px wide, 1–2 rows under the line. There is no red lip fill on anyone who isn't
      wearing lipstick as a design choice.
- [ ] **An open mouth is an outlined hole**, at least **4x3 px of interior**: outline colour around it, a dark interior (`#4a1424`
      family), a **row of teeth under the top lip** (laugh, angry), a **tongue tone in the bottom third** (laugh, shout).
      Its shape tells the emotion: D-shape (laugh), upright oval (surprised), wide rectangle with both teeth rows (angry/gritted),
      downturned trapezoid (crying or shouting in grief).
- [ ] Facial hair goes **above** the mouth with a clear 1-row skin gap. When the mouth opens, the moustache rides up 1 row rather than
      touching the lip line (Dorian laugh).
```
closed smile        knowing (far corner up)    laugh (D-shape)       surprised (oval)    angry (gritted)
 R      R           s          R               s.KKKKKKKKKK           .KKK.               KKKKKKK
  RRRRRR            s.R       R                s.KTTTTTTTTK           KoooK               KTTTTTK
   sss              ...RRRRRRR                 ...KooooooK            KotoK               KoooooK
                    .....sss                   ....KottoK             .KKK.               KTTTTTK
                                               .....KKKK              .sss.               .KKKKK.
```
(R = mouth line, s = skin shadow, K = outline, o = dark interior, T = teeth, t = tongue)

### 3.7 Hair: shaped clumps and highlights
- [ ] **Design the mass, then 3–6 clumps.** Each clump is a curved, tapering shape at least 3 px thick, ending in a tip of
      2–3 px (not a 1-px spike). Tips point *with the flow*: back and down for swept hair, down for hanging hair.
- [ ] **Build it as one silhouette first** (no holes), then lay clumps on top. A crease appears only where a clump tucks under the
      next one, on the tucked-under side, in the darkest hair tone (`dorian_portrait.py`: `hair0` silhouette, then clumps back to front).
- [ ] **Per clump:** base (light) + a 2-px shadow band on the edge away from the light + an occlusion pixel run where it meets the
      crease below + **one highlight arc**: 3–7 px, contiguous (1:1 or 2:1 steps), a third of the way into the clump from its lit edge,
      following the flow, broken where the clump turns. No highlights at the tips. No isolated highlight pixels (they read as sparkles).
- [ ] Highlights, light and mid tones carry the colour. On silver or white hair, mid and shadow are lavender or blue, the
      highlight is near-white and the crease is a deep violet (Dorian). On dark hair the highlight is a desaturated blue or violet,
      never pure white.
- [ ] **Helmet test:** if the hair silhouette is a smooth dome with fewer than 3 tips or notches, or 70% of the hair is one tone,
      redesign it.
- [ ] Hairline shadow: a 1-px skin-shadow band under the hairline. The forehead's lit corner may take 3–4 px of skin highlight.

### 3.8 Translucent layers (veils, glass, smoke)
- [ ] Translucency is a fixed 50% blend of the layer with what is behind it, reduced to **one tone per zone** (veil over background,
      veil over hair). Then add one pleat or edge line. No speckle, and no grey pixels in a warm veil (the pass-3 veil specks, fixed in sheet 27).
- [ ] The inner edge of a translucent layer is a lighter hem line, not a hard dark vertical.

### 3.9 Expressions and how to make them
- [ ] **Change only** brows, eyes, mouth and marks (tear, sweat drop, blush hatch: 2–3 diagonal 1-px lines). The head, hair and
      clothes stay pixel-identical; check with a diff that lists changed pixels by region.
- [ ] Brows lift 1 row for happy, 2 rows for surprised, drop and angle at the inner end for angry, and rise at the inner end for sad.
- [ ] Every expression has to read at true size in the window mock, not only at 5x.

### 3.10 Background treatment
- [ ] Portrait files are **transparent**. The face window draws the plate: the window skin (dark slate `#34384a` in the mocks).
- [ ] Optional per-character plate: one flat colour, the muted signature hue (its VS-bar hue at about 35% saturation and 85% value).
      No gradients, scenery or patterns.
- [ ] The figure never touches the frame on the side the face looks toward. There is always at least 2 px of air at the right.

### 3.11 Construction method for portraits
**Original construction is the default for main-cast portraits** (coordinator's direction, 2026-11-20; both faces_v1 sets, built on
official VS faces, read as generic). Build them as `art/research/scripts/dorian_portrait.py` does:
1. **Shapes:** polygons for the hair silhouette, the clumps, the face (from the §2.3 jaw template), ear, neck, coat, lapels and accessories.
2. **Materials and light:** each material gets its ramp; light comes from the upper left; 1–2-px bands of highlight and shadow on the edges.
3. **Lines:** black silhouette and material boundaries; creases in the darkest tone; drop lone pixels.
4. **Hand passes:** hair arcs, occlusion, hairline shadow, skin planes (forehead light, cheekbone shadow, neck shadow).
5. **Feature stamps:** brows, eyes, nose, mouth, facial hair and marks from the §3.5 and §3.6 stamps, one stamp set per expression.

Kitbashing official busts is no longer used for portraits. Battle fronts and overworlds keep the Rev 11 kitbash pipeline, with this guide's design rules.

### 3.12 Portrait checklist (put it on the review sheet)
- [ ] 96x96, 2x2 blocks, alpha 0/255, ≤ 32 colours, no orphans.
- [ ] Eye line 22–27, chin 40–44, whole head in frame, facing right or front.
- [ ] Silhouette has ≥ 3 breaks; the hook from §2.1 is visible.
- [ ] Jaw, eye and brow templates recorded, and different from every other main-cast face.
- [ ] Hair: ≥ 3 clumps, one arc each, creases in the darkest hair tone, no black strands.
- [ ] Mouths: closed = line + corners; open = outlined hole + dark interior + teeth/tongue rows.
- [ ] 3 colours + 1 accent; shadows hue-shifted; no neutral grey.
- [ ] True-size window mock on a real map preview, beside Juno pass 3.
- [ ] "Who does it look like?" answered in writing.

---

## 4. Trainer battle sprite spec (front)

- **Format:** 80x80 art, exported 160x160 (`<NAME>.png`) plus `<NAME>_native80.png`; EBDX anchors bottom-centre at `TRAINER_SPRITE_SCALE = 1`
  (Kitbash §1, §7). Feet sit 2–3 px above the bottom edge.
- **Proportions** (`design/PIXEL_ART_NOTES.md` §1): figure 70–76 px; teens 4.5–5 heads tall, adults 5.5–6.5; legs about 45% of the height;
  chunky hands.
- [ ] **Pose = personality.** Weight on one leg, an asymmetric arm, a prop held with intent (the kyledove performer, Rejuvenation 240's
      lunge, Dorian's hat aloft). "Stand and hold the ball up" is for NPC classes only.
- [ ] Silhouette reads at **1x on the battle field** beside the other cast fronts (line-up strip on every sheet).
- [ ] Outline black 1 px; interior lines in material deep tones; 3–4 tones per material; **≤ 36 colours** (Reborn fronts 33,
      Rejuvenation 25; our Juno P3 at 45 is over and should be reduced when next touched).
- [ ] The face at front scale: eyes 2 px wide x 2–3 tall with one catchlight; mouth 1–3 px (`PIXEL_ART_NOTES` §2).
- [ ] **Same design as the portrait:** hairline, hook shape, the 3+1 colours and the accent placement must match. The portrait's palette
      ramps are the master; the front uses a subset.
- [ ] The prop is in the character's palette, and organic props come from battlers at the same density (Kitbash §13).

## 5. Overworld spec

- **Format:** 128x192 sheet, 4 frames x 4 directions, 32x48 frames = **16x24 art doubled** (Kitbash §8; the installed `JUNO.png`).
- [ ] Head (with hair) 10–12 rows of the 24; body 12–14. Eyes are 1x2 px dark blocks (no whites) on the front view.
- [ ] Black outline on the silhouette; 2–3 tones per material; ≤ 24 colours on the sheet.
- [ ] The §2.1 hook must survive at 16 px (Juno's wreath is 7 px and the train a sheer strip; Dorian's mane is the back-swept shape on
      all four facings). Exaggerate it by 1–2 px rather than lose it.
- [ ] The accent shows from **all four directions**: if it's on the front (Dorian's rose), add a second accent pixel at the back (his
      cape's silver lining edge).
- [ ] Grey hair reads as elderly at 16 px (Kitbash §14). Give silver hair a lavender mid tone and a white highlight row so it reads as styled.

## 6. VS and battle-intro art direction

- **Format:** `vsTrainer<ID>.png` + `vsBar<ID>.png`, **256x128 = 128x64 art doubled**, the B2W2 VS standard used by Reborn, Rejuvenation
  and Desolation (`Graphics/Transitions`).
- [ ] **Bar:** the character's signature hue as a 5–7-band horizontal ramp, dark at the top and bottom edges, light through the middle, plus
      2–4 white or light streaks (Bianca green, Skyla blue, Elesa gold). Dorian's is footlight gold to amber, so his plum reads hot
      against it; Juno's is spring green, her accent made big.
- [ ] **Bust:** right of centre, facing left or front. The head is 28–36 px tall in art and **breaks the top edge** (hair or hat clipped at row 0).
      A **gesture hand in the foreground** (pointing, a ball, the prop) overlaps the bar (Skyla, Lenora, Roxie's guitar, Reborn 227's card).
- [ ] The battle expression is more intense than the portrait's neutral: Juno's determined grin, Dorian's laugh mid-bow, Kestrel's
      scowl. The face design and palette match the portrait exactly.
- [ ] **14–24 colours**, black outline, 2 tones per material plus a highlight. This is the cleanest art in the game (B2W2 busts use 14–15).
- [ ] An optional 1-px light rim separates a dark bust from a dark bar (NoodlesXL's "VS Alice").
- **Key art and chapter cards** (the illustration tier, honnojis' V14 cover and the Rejuvenation illustrations): one warm key light and a
  cool fill, hard-edged two-tone cel shadows, glow only on light sources, diagonal compositions, the cast's signature colours as shards or
  bands. Use this for title and act cards, not for in-game sprites.

---

## 7. Do and don't (with image examples)

| Do | Example |
|---|---|
| Thumbnail silhouettes before any colour | `moodboard_characters.png` tile 1 (honnojis: 24 silhouettes, then 4 value roughs); sheet 27 rows 1 |
| A swept mane in clumps with one highlight arc each | sheet 27, Dorian 5x |
| Open mouths as outlined holes with teeth and tongue | sheet 27, Dorian laugh; `moodboard_portraits.png` B2W2 Skyla crop |
| Surprised as a dark upright oval | sheet 27, Dorian surprised |
| Shade silver and white with lavender/blue | sheet 27 Dorian; `moodboard_portraits.png` Desolation Faces/22 |
| Draw interior lines in each material's darkest tone | `moodboard_portraits.png` honnojis momo/okarun pixel |
| 3 colours + 1 accent, with a palette strip on the sheet | `moodboard_characters.png` Pom and Damian ref sheets; sheet 27 swatches |
| Put a flat plate behind portraits | `moodboard_portraits.png` honnojis chibi (disc), angeceleste icons (flat colour) |
| Use a gesture hand in VS art | `moodboard_pixel.png` B2W2 Skyla/Lenora, NoodlesXL VS banner |
| Keep accepted art and change it in small, diffed steps | sheet 27 Juno refresh (67 px, all in the veil) |

| Don't | Example of the failure |
|---|---|
| Helmet hair: a smooth dome, one tone | sheet 26 Dorian (faces_v1): "a generic old man with a helmet of hair" |
| A red blob for an open mouth | sheet 26 surprised and angry faces |
| A muddy moustache (2 blended tones, touching the lip) | sheet 26 Dorian; fix: 1 crisp line + 1-row gap (sheet 27) |
| 1-px black strands inside hair | `art/previews/16_juno_hair_fix.png`, top row ("choppy": Rosa's hat lines and Hilda's strand lines) |
| Grey specks in a translucent layer | sheet 27, the pass-3 veil (left) vs the refresh |
| A recoloured recognisable head | sheets 13–14, the Burgh-based Juno ("Burgh wore a wig") |
| Realistic, painterly shading in portraits | sheet 15, pass 5 (rejected for pass 3) |
| The type colour as the uniform | `design/CHARACTER_DESIGN_STUDY.md` Plate A (v4 Juno = Milo) |
| Long mane + plum + high collar | sheet 27 silhouette E; sheet 18 notes (the Juggler body read as a vampire) |
| Drawing pixels before the design is settled | Rev 11: five from-scratch rounds, "god awful" |

---

## 8. Review sheet layout (every character)
1. Silhouettes (black, 1x and 2x) with the pick marked and a one-line reason per rejected option.
2. The chosen design with its 3+1 palette strip and the kingdom/type motif noted.
3. The portrait at 5x and at true size on the window plate and on cream; expressions in a row.
4. A true-size window mock on one of our map previews (`maps_out/previews/`).
5. The comparison: Juno pass 3 and the previous version of this character.
6. The checklist (§3.12) and the "who does it look like?" line.

---

## 9. Where each rule came from

| Rule | Reference pieces (see `art/research/SOURCES.md`) |
|---|---|
| §1 process; §2.1 silhouette first | honnojis `juno_ref_portfolio` (24 silhouettes → 4 value roughs → turnaround), `damian_ref_sheet_v3`, `pom_ref_sheet_v3`; Valve's read order (CHARACTER_DESIGN_STUDY §3) |
| §2.1 ≥ 3 breaks, helmet ban | faces_v1 Dorian (sheet 26, coordinator critique); Desolation Faces/22, 18 (clumped silhouettes) |
| §2.3 face-shape kit | Desolation Faces 10a, 13, 22, 26 (adult vs young jaws); B2W2 VS Grimsley/Drayden/Alder vs Bianca/Rosa crops; honnojis Pom vs Damian heads |
| §2.4 3+1 colours, accent ≤ 5% | honnojis Pom and Damian palette strips; `key_art_2021` (cast read by colour block); B2W2 VS single-hue bars |
| §2.5 hue-shifted ramps; silver = lavender | honnojis `momo_pixel`, `okarun_pixel` (rose and plum shadows); Desolation Faces/22; `rejuv_illust` (warm key, teal fill) |
| §2.6 kingdom motifs | `story/01_WORLD_LORE.md` fashion tells; `design/ART_DIRECTION.md` §4 cloth colours; Nifast Greentail and Princeloppy Pokémon-style pieces (type motif worked into hair and costume) |
| §2.7 layers, one prop, motif ≤ 3 | honnojis Damian (rose ×3), Pom (hoodie/jacket/denim); Rejuvenation front 021 (cane); Kitbash §5 (stamps) |
| §2.8 originality | SPINE Rev 13, 17; Kitbash §11 |
| §3.1–3.2 format and framing | Desolation `Graphics/Faces` (48 → 96, 22–39 colours, face window on the left); Juno pass 3 (eye line 27, chin 43); Fiorne dialogue frames; Mossgrover 64x64 talkers |
| §3.3 lines | B2W2 VS (outline `#101010`–`#282028`); Desolation faces (`#000000`); honnojis pixel pieces (`#2d1e2f` outline, coloured interior lines) |
| §3.4 tone counts, no dithering | B2W2 VS 14–15 colours; honnojis pixel 21–22, no dithering, clusters ≥ 2 px; Desolation 22–39 |
| §3.5 eyes | Desolation 08a, 13 (2-px lash, outer flick); angeceleste icons (heavy lash wing); B2W2 Bianca (two-tone iris, one highlight); Juno pass 3 |
| §3.6 mouths | B2W2 Skyla (teeth row + tongue); honnojis Damian and Pom expression heads; honnojis VGen chibis; sheet 26 failures |
| §3.7 hair clumps and arcs | Desolation Faces 22, 08a; honnojis `okarun_pixel` (lock divisions in the hair's dark tone); Kitbash §12 (Juno hair lessons); `PIXEL_ART_NOTES` §3 |
| §3.8 translucency | Kitbash §6; the pass-3 veil (sheet 27) |
| §3.9 expressions | honnojis Damian and Pom expression sheets; Desolation expression sets (01/01b, 08a–g) |
| §3.10 plates | honnojis VGen chibis (flat disc), angeceleste icons (flat colour + 1-px rim), Fiorne (framed), NoodlesXL FoM portrait |
| §3.11 original construction | coordinator 2026-11-20; sheet 27 Dorian vs sheet 26 |
| §4 fronts | Reborn 193, Rejuvenation 021/240, kyledove MUSICIAN/DANCER; `PIXEL_ART_NOTES.md`; Kitbash §1, §13 |
| §5 overworlds | Rejuvenation `Aelita`, our `JUNO.png` charset, VanillaSunshine Gen 4 sheets; Kitbash §8, §14 |
| §6 VS bars and busts | B2W2 VS Bianca/Skyla/Roxie/Lenora; Rejuvenation VS 192/79; Desolation VS 124; Reborn VS 227; NoodlesXL VS banner and trainer + VS sheet |
| §6 key art | honnojis `v14_cover_art`, `rejuv_illust`, `rejuv_illust_bsky`, `aelita_wallpaper` |
