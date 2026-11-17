# PIXEL ART NOTES: trainer-front checklist (v4)

Owner: Character Artist. Written 2026-11-16 from (a) tutorials: Slynyrd Pixelblog 1 (palettes), 5 (basics/clusters), 6 (light),
22 (character sprites), 29 (anime faces/hair); Saint11 "Outlines", "Shading", "Portraits"; Pixel Grimoire #2 (clusters, jaggies);
Dragonfly Cave spriting guide; Tun's trainer-sprite tutorial (pokecharms); and (b) pixel-by-pixel dumps of the local references
(`art/tools/v4/dump.py`): Rejuvenation `trainer002` (girl in dungarees, 90×90), Reborn `trainer007` (green dress, 80×80) and
`trainer010` (80×80), stock EBDX `POKEMONTRAINER_May` (64×64), a Rejuvenation charset (`Aelita`, 48×48 frames).
AdamCYounis: no transcript or written notes were reachable, so nothing here is attributed to him.

## 1. Format and proportions (measured)

| Set | Native canvas (stored ×2) | Figure height | Head (crown to chin) | Colours |
|---|---|---|---|---|
| Stock EBDX / Gen 3-4 | 64×64 | 53–60 px | ~13 px | 13–15 |
| Reborn | 80×80 | 71–76 px | ~16–18 px | 18–23 |
| Rejuvenation (small set) | 90×90 | 59–79 px | ~16 px | 18–39 |
| Rejuvenation (new large set) | 180×180 native | 130–146 px | — | 21–35 |

- [ ] Target **80×80 native, stored doubled (160×160)**, the Reborn size. Figure 70–76 px tall, feet 2–3 px above the bottom edge.
- [ ] Teen = about **4.5–5 heads** tall (the head is big; hair volume makes it read bigger). Shoulders ≈ 1.2–1.4 head widths.
- [ ] Legs ≈ 45 % of the height. Hands are about as big as the eye-to-chin span (Pokémon hands are chunky). Boots/shoes chunky.
- [ ] 3/4 view: the far side of the body is 30–40 % narrower than the near side; the far shoulder is a little higher or hidden.

## 2. Face at small size (from the dumps)

- [ ] Face skin ≈ 11–13 px wide, 10–11 px tall. Eyes sit at about the **middle of the head height** (crown to chin), mouth ~4 px below the eyes.
- [ ] **Eye = 2 px wide × 2–3 px tall**: a dark lash line on top (black or very dark hair colour, can extend 1 px outward), a dark
      iris/pupil block, **one white catchlight pixel**. Gap between the eyes ≈ 3–4 px. Both eyes on the same row.
- [ ] Brows usually hidden by bangs; if shown, 2–3 px of the hair's dark colour.
- [ ] **Nose: none**, or a single shadow pixel. **Mouth: 1–2 px** of deep skin shadow; an open smile is 2–3 px (dark + 1 tongue/teeth pixel).
- [ ] Skin ramp (Reborn): `#ffd5bd` base, `#de987b` shadow (hue shifts red), `#a25e4c` deep/outline. The shadow sits **under the bangs
      (a 1-px band along the hairline)**, down the far cheek/jaw, and under the chin onto the neck. No other shading on the face.
- [ ] The far jaw line uses the deep skin colour as its outline (selective), not black.
- [ ] Freckles, blush: 1–2 px of the skin shadow colour, symmetric, never noisy.

## 3. Hair

- [ ] Hair is a **mass first**: one silhouette, then 3–4 big clumps, then strands. Flow lines start at the crown/parting.
- [ ] 4 tones + an outline: dark (outline/shade, hue-shifted cooler), shadow, base, highlight (**hue-shifted ~20° toward yellow**).
- [ ] Shading as **long strand-shaped clusters** that run with the hair direction (vertical or curved bands such as `jjiijj`), never blobs.
- [ ] Highlight = a narrow **arc band** on the lit upper side (the anime "halo"), made of short dashes, 5–12 px total. Not a ring.
- [ ] Clump tips end in 1-px points, stepped cleanly (2-1-1 or 3-2-1), not wobbly.
- [ ] Reborn outlines hair in its darkest hair colour (dark brown `#371c11`), with black only where it meets the background on the shadow side.

## 4. Cloth

- [ ] **Big flat base areas.** Most of a garment is one colour. Reborn's dress is ~70 % base.
- [ ] 3–4 tones per material: highlight (sparse), base, shadow, deep (also its inner outline).
- [ ] **Folds are lines and wedges, not blobs:** 1-px dark lines or 2-px tapering wedges that radiate from stress points (crotch, knees,
      elbows, where a strap pulls, under the bust/bib) and follow gravity on loose cloth. Each fold gets a 1-px highlight on its lit side only
      where it matters.
- [ ] Shadows sit under overhangs: under the collar, under the bib, under the arm on the torso, inside the trouser leg behind the knee.
- [ ] **White/cream cloth shadows are cool** (lavender-blue on white in Rejuvenation: `#c9cceb`, `#7379b3`); cream goes to a warm grey-tan.
- [ ] Patches, seams and pockets: 1-px seam lines in the shadow colour; a patch is a differently-tinted rectangle with a 1-px darker border.

## 5. Outlines

- [ ] 1 px everywhere, no doubled corners, no "L" kinks on curves (step lengths grow/shrink monotonically).
- [ ] Reborn = **selective outline**: each material is outlined with its own darkest tone; black only on the shadow side (bottom/right) and
      at important separations (arm over body, face against hair). Rejuvenation 90-px set = mostly black. Pick one per sprite.
- [ ] Interior lines (arm over torso, strap edges) use the darker of the two materials, not black, unless separating overlapping limbs.
- [ ] No outer anti-aliasing (it halos on battle backgrounds). Inner AA only at a few high-contrast curve steps, 1 px.

## 6. Light and colour

- [ ] Light from the **upper left, slightly in front**. Lit: left/top planes, top of the hair, left cheek. Shade: right side, under the
      chin, under the hair, inner legs.
- [ ] **Hue shift**: shadows move toward blue/purple (cloth, hair) or toward red (skin); highlights toward yellow. Shadow steps raise
      saturation and drop value 15–20 %. No grey/black-mixed shadows.
- [ ] Ramps measured: green dress `#6dc567 → #449056 → #3a643b → #254126` (shadow goes bluer); blue denim `#6c89f4 → #506bd0 →
      #3f4cad → #363c88 → #20234e` (toward violet); pink hair `#f581bb → #d7639d → #ba4b82 → #6d2252` (toward purple); brown hair
      `#9a6a3c → #74423d → #512a27` (highlight toward gold).
- [ ] **18–24 colours total** (Reborn's budget). Every colour must be used in ≥ 3 places, except eye catchlights.
- [ ] Two-colour identity from the design sheet must dominate at 1×.

## 7. Clusters and noise

- [ ] No orphan pixels (a pixel with no same-colour 8-neighbour) except catchlights, buttons, freckles, sparkle.
- [ ] No pillow shading (shade that follows the outline all the way round). Shade comes from one side.
- [ ] No banding (two tone edges running parallel at 1-px distance along a contour).
- [ ] Clusters have clear shapes (wedges, bands, arcs) and point in the direction of form or flow.

## 8. Pose

- [ ] A readable **action line** (head → hips → weight foot) with a slight S or C curve. Hips and shoulders tilt opposite ways (contrapposto).
- [ ] One hand presents a Poké Ball or makes the character's signature gesture; the arms make a clear negative space against the body.
- [ ] Feet apart, toes out; the silhouette must read as a person at 1× with every interior detail removed.
- [ ] The character's one exaggerated feature (design sheet) is the biggest shape in the silhouette.

## 9. Overworld and portrait notes (brief)

- Rejuvenation charsets: 48×48 frames, the head is about half the figure, a black 1-px outline, 2–3 tones per material, hair with a single
  highlight line. Rejuvenation bubble portraits are 96×96, painterly with dark outlines and strong rim light; they are drawn per expression.

## 10. Per-round review procedure

Render 1× and 4× beside two references on a mid-grey battle background. Check: silhouette at 1× (squint), face readable at 1×,
colour count, orphan count (`lint` in `art/tools/v4/px4.py`), outline breaks, pillow shading, banding, fold logic. Fix the single biggest
problem, then re-render.
