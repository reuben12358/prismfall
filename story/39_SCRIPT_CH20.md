# Script: Chapter 20 — "The Festival of Champions" (Crownhaven, Festival week, Days 0–6)

> **Final playable script** for Chapter 20: seven days in one city.
>
> **Maps:** Crownhaven (480–519), including:
> - the Basilica steps
> - the Meridian Prism Arena (its stands, the floor and the Wardens' box)
> - the Glassfall Memorial Garden (489)
> - the garden court
> - the Basilica square (the Night of Masques)
> - the Sovereign's Sanctum
> - the Concordance Spire (under construction)
> - the festival grounds
>
> None of these maps is built; the list at the end is what to build from.
>
> **Order:** follows `story/38_SCRIPT_CH19.md`. Chapter 21 ("Sovereign") is Day 7.
>
> **Sources:**
> - Act and branch files: 08_ACT_V Ch20 (the day-by-day beats, which this script stages); **14_WAR_AND_BLESSING Part A** (the delegations and seats; it wins on conflicts); **10_CHOICES_ENDINGS §3** and **NARRATIVE_KEYS §6** (the draw rules, R16 → SF candidates, exhibitions; the bracket is theirs, this script only stages it).
> - Characters and lore: 03_CAST; 09_MYSTERIES (#2 Morwen's letter, #11 the Tuning, #17 the Engine); 15_COMEDY Ch20 "The Good Tea"; 13_CUTSCENES (the ceremony, highlights).
> - Design: `design/EEVEE_OCTAVE.md`; `design/CHAPTER_BEATS.md`.
> - Plugins: `Prismfall Core` 008/009/010/015 (the Festival manager: `Prismfall::Festival.next_match`, `.exhibition(id)`, `Draw.set_day(n)`).

## Conventions
As in the earlier scripts. Festival matches go through the manager:
- **The PC's match each day:** `Prismfall::Festival.next_match`. The manager picks the opponent from the draw and its ruleset sets the cap: R16 90, QF 92, SF 94.
- **Exhibitions:** `Prismfall::Festival.exhibition(:id)`.
- **The day:** `Prismfall::Festival::Draw.set_day(n)`, 0–7.
- **Healing:** the manager heals between matches.

**Portrait cast:** every Warden; Valen, Voss, Kestrel, Juno, Ilsa, Larch, Calla, Rowan / Teo (by flag), Okoro, Hollis, Tamsin, Carol and Vesper (Octave), Morwen (echo, conditional); and the PC (one authored line, at the audience).

**Plain:** the Hierophant, the crowd, the Choir, and the Saltmere Players.

**Counter:** V141 **CH20_STEP** (new; design/FLAGS.md). It tracks scenes within the days; the Festival day itself lives in `Prismfall::Festival::Draw.day`.

| V141 | Scene |
|---|---|
| 0 | Day 0: arrival |
| 1 | the draw and `:ch20_colors` |
| 2 | Day 1: the ceremony and the vision (S156) |
| 3 | Day 2: R16 |
| 4 | the garden court |
| 5 | Day 3: exhibitions and Okoro (`:ch20_envoy`) |
| 6 | Day 4: QF |
| 7 | Day 5: Corvin's warning |
| 8 | the Night of Masques (S157) |
| 9 | Calla (`:ch20_calla`) |
| 10 | Valen's audience (`:ch20_audience`; S158) |
| 11 | "Little Owl" |
| 12 | Interlude V |
| 13 | Day 6: SF (K8) |
| 14 | Morwen's letter |
| 15 | the eve of the Final (chapter closed; V102 = 21) |

**State set here:**
- **Switches:** S155 CH20_VEIL_GATE_OPEN stays **OFF** (the Gate stays shut, Revision 4/5), S156 CH20_CEREMONY_DONE, S157 CH20_MASQUES_DONE, S158 CH20_AUDIENCE_DONE.
- **Variables:** V114 KESTREL_STAGE = 5 (K8), V119 INTERLUDE_ACTIVE = 5 then 0.
- **Keys:** `:ch20_colors`, `:ch20_envoy`, `:ch20_calla`, `:ch20_audience`, `:sq_little_owl`.
- **Game over:** `GO_EARLY_CROWN`.
- **Key Item:** MORWEN'S LETTER (Kestrel's, readable after the SF).

## The chapter's key events (design/CHAPTER_BEATS.md)
1. **The Opening Ceremony and the vision.** Eighteen Wardens carry eighteen Plates into the Ring. Valen's glove comes off, and forty thousand people see the crystal arm. The PC's shard answers: *"...Little light. You have carried me far."*
2. **Valen's audience.** He explains rather than defends: "I chose a country over a woman's name. I'd do it again. I hate that I'd do it again." The PC answers (`:ch20_audience`).
3. **K8 and Morwen's letter.** Kestrel either tears off the Gauntlet or keeps it. Ysolde gives him the letter on the arena floor.

## Density (Festival chapter; design/DENSITY_STANDARD.md, adapted)
The Festival's density comes from the bracket, the exhibitions and the grounds, not from route trainers:

| Item | This chapter |
|---|---|
| Story fights (≥4) | **R16**, **QF**, **SF (K8)** (critical, via the manager) · plus exhibitions: the Eevee Octave gauntlet (9 fights), the Pageant Bout, Juno's Garden Match, the Ebb Guild match, Morwen's Echo (conditional) |
| Trainers | The **Festival grounds** hold 12 open challengers (Day 3, the "Grounds Ladder": original characters from every kingdom, Lv 88–90; roster at the end) |
| EventMons (≥3) | **Eevee "Amen"** and the Eevium Z (the Octave) · **Indeedee "Usher"** (gift, an arena usher on Day 1) · **Alcremie "Festival"** (gift, the street-food sweets stall on Day 3) |
| Hangouts | Every Warden in their kingdom's pavilion on Day 3 (one line each; Bonds +1 at most once) |
| Glassfall Slivers | 6: the last of the 100. Hidden in the arena's stands, the Memorial Garden, the Basilica bell, the Spire scaffold, the Sanctum window, and the Glassfall Scar's child-sized space |
| Quests | `:sq_little_owl` (Ilsa) · *The Ninth Verse* (Octave) · "The Good Tea" (running gag) · the Sliver exchange's last tier (100 at Larch's stall) |

**No jokes** in these stretches:
- the ceremony's vision (V141 1 → 2);
- from Corvin's warning to the end of Interlude V (V141 6 → 12);
- from Morwen's letter to the end of the chapter.

"The Good Tea" (15_COMEDY) plays on Day 5 before Corvin.

---

# CHAPTER 20 — "The Festival of Champions"

**Chapter start:** V102 = 20, V141 = 0. Crownhaven's gate.
- `Script: Prismfall::Festival.start`
- `Script: Prismfall::Festival::Draw.set_day(0)`

## Day 0: Arrival (V141 == 0 → 1)
```
(Crownhaven: white stone and bells in a caldera above the clouds. Upper Crownhaven hung with eighteen banners, one per kingdom's Plate, woven, every thread, since Ch10, by one weaver.)
(And where the old grounds were, the Meridian Prism Arena: eighteen-sided, gold and glass, too new. It shines like something that doesn't know what it's for yet. You know.)
[portrait: TAMSIN, happy] (under the banners, with a mouthful of pins) You came! Look at them. Look. Eighteen. I finished the Dread one last night. My fingers are bleeding. Don't look at my fingers.
[portrait: TAMSIN, neutral] (lower) Look at the colours tomorrow, though. Some of them will change. I wove them that way. You'll see.
```
- **The Consent display** (from Day 1): each Warden's banner hangs **white** (they'd let go) or **grey** (they won't), by the Consent conditions (NS §6.2). Tamsin's private reading of her colleagues; the player can walk the row and read it. *(An interact on each banner gives one line per Warden, from NARRATIVE_KEYS' consent list.)*
- **Every faction is here** (ambient NPCs across the city):
  - Meridian security in white.
  - Lantern Hollow disguised as Choir porters (`standing(:HOLLOW) >= 2`: one winks).
  - The kings in the observers' gallery: Caedmon, Eirik, the Dominar's herald, Kassan, Dask.
  - **Envoy Delphine Okoro** of the Concert, in a grey coat, taking notes on everything.
- **The Veil Gate stays shut.** Chancellor Hollis to Archseer Dask, overheard on the Basilica steps: "For prestige, Archseer. One night." Dask: "The Glass is leaking already. I won't open a door in a wall that's falling down." *(S155 stays OFF. No foreign champions come: every entrant is someone the PC met on the road.)*
- **The Eevee Octave:** **Carol** in the Glassfall Memorial Garden (489). *The Ninth Verse* opens once all seven road singers are helped (EEVEE_OCTAVE.md).

### **The draw** (autorun at the Basilica steps at dusk, V141 == 0 → 1)
```
(The Basilica steps. The Hierophant in white with a crystal bowl. The sixteen standing in a crescent below. Your name among them, read out third: "The Unimprinted. Of —" and a pause, because the bowl wants a kingdom.)
[portrait: MAELIS, neutral] (from the gallery) Elowen's colours. The forest would be pleased.
[name: Councillor] (Zenith, in white) The Council offers its colours. Meridian sponsors so many fine young people.
[portrait: NYX, smug] (from a pillar, not in the gallery) Nadir's. We're independent now. It means nothing. Wear it anyway.
[portrait: LARCH, neutral] (from the crowd, not loudly) Or none. There's an old clause. "The Unsworn." Nobody's used it in sixty years. It's still in the book. I checked.
> Elowen. (elowen)   > Zenith. (zenith)   > Nadir. (nadir)   > The Unsworn. (unsworn)
  Script: pf_choose(:ch20_colors, <choice>)
(The Hierophant writes it. The bowl is honest. The lots are drawn.)
Script: Prismfall::Festival::Draw.resolve_delegations   # 14 Part A: the war decides Isenmar's and Ashkaar's seats
V141 = 1.
```
*(NARRATIVE_KEYS: elowen ACCORD−1 · zenith MERIDIAN+1 · nadir HOLLOW+1 · unsworn RES+1.)*

*(The bowl is honest. The bracket isn't. The Accord's old customs bend it on screen: the Right of Grievance, yielded invitations, a Warden asking for a challenger's quarter, and Dorian, who has never once let the bowl ruin a good story. Each bend is a one-line Hierophant reading (NS §3.1).)*

## Day 1: The Opening Ceremony (autorun at dusk in the arena, V141 == 1 → 2; key event 1)
`Script: Prismfall::Festival::Draw.set_day(1)`
```
(Dusk. The Prism Arena, forty thousand people. The Choir in white in the loft, eighteen of them. You've seen this before, through someone else's eyes.)
(Down the Sovereign's Stair, one by one, in gym order, to the Choir's counting rhyme: eighteen Wardens, each carrying a Plate in a reliquary.)
```
**The procession** (each Warden steps into frame and sets their Plate into a pylon of the **Concordance Ring**; one line of staging each):
| Warden | Plate | Staging |
|---|---|---|
| Dorian | Blank | bowing to all four sides |
| Tamsin | Insect | pins still in her sleeve |
| Marisol | Splash | |
| Rook | Zap (still cracked, in a cradle) | If Rook was fired (`:ch16_rook == :leak_now`), a Meridian officer carries it, and Rook watches from the crowd with his collar up. |
| Sahar | Earth | |
| Corvin | Toxic | Carried by a Choir porter in his mask, unless `CORVIN_FREED`. |
| Brann | Flame | |
| Kaito | Fist | |
| Juno | Meadow | |
| Anja | Icicle | |
| Odessa | Sky | |
| Ilsa | Mind | |
| Bastian | Stone | leaning on Pip |
| Ysolde | Spooky | |
| Magnus | Iron | under guard if `MAGNUS_EXPOSED` |
| Nyx | Dread | |
| Celestine | Pixie | |
| Sigrun | Draco | |

```
(Valen in white at the Ring's centre, the Crown on his brow. He takes off the grey glove.)
(His arm is glass. Crystal, to the shoulder, catching eighteen colours. A sound goes through forty thousand people that isn't a word.)
(The Choir sings the half-Hymn. The Ring lights in eighteen colours. The sky over Crownhaven ripples like water.)
[anim: the PC's sprite glows; screen to white over 60 frames; hold]
(The world goes white.)
(In the white: a vast shape of light. A wheel. Eighteen places in the wheel, all empty. One eye, opening.)
[name: ???] ...Little light. You have carried me far.
[anim: white to black; then the stands, the PC's view from the floor]
(You're on the floor of the stands. People around you. Someone's hand under your head: Juno's, or Pip's, or a stranger's.)
(Down on the Ring, Valen is looking straight up at you. Across the arena, in the Warden ranks, Ilsa has taken her earmuffs off, and flinches at what she hears in her father.)
Switch S156 CH20_CEREMONY_DONE = ON. V141 = 2.
```
- **Rook's leak** (if `:ch16_rook == :hold`; straight after the ceremony):
  ```
  (Every screen in the arena flickers. The Spire footage: a corridor, a keycard, a figure turning: Sable. Sabine Kroll. Rook's Rotom has the feed.)
  (The crowd turns, row by row, towards the Meridian box.)
  [portrait: VOSS, neutral] (not blinking) Rogue contractor. The inquiry continues.
  (Okoro writes something down. She underlines it.)
  ```
- **Gift: Indeedee "Usher"** (Lv 60, Psychic Surge), from an arena usher who carried you out of the stands: "She found you first. She's been looking at you since. I think she's decided you're hers to look after. Usher's like that."

## Day 2: Round of 16 (V141 == 2 → 3)
`Script: Prismfall::Festival::Draw.set_day(2)`
**The PC's R16:** `Script: Prismfall::Festival.next_match`. The candidate comes from NS §3.2: "someone from your past". The staging lines per candidate:

| Candidate | Condition | Opening line |
|---|---|---|
| **Marisol**, by Right of Grievance | Isenmar seat, Teo died, `bond(:MARISOL) <= 2` | The Hierophant reads the right out. Marisol: "Let's see you run past *me*." (She and Juno swap seeds.) |
| **Anja**, by Right of Grievance | Isenmar seat, `ANJA_EXPOSED` | "You threw me to the court. Fine. Ice remembers." |
| **Rowan, "the Gardener"** | `ROWAN_ALIVE`, mercy pleaded, `standing(:HOLLOW) >= 4` | Masked, under a false name, on Juno's yielded invitation. "One last garden, child. Then I'm done with masks." |
| **Juno (J4, fallback)** | otherwise | "We started on the same dock. Let's see who's grown more." `:PRISM_ARENA` field cycling. **Her first Festival fight: Gardevoir "Veil" Mega Evolves**: "...Oh. There you are." Her ace is Tsareena; Ogerpon fights for her if `OGERPON_TRUSTED` (on *her* team: a Warden's partner, not the PC's). |

*(LOSE: the manager's retry rule.)*

**The other R16 results** are one-line highlights (13_CUTSCENES; watchable from the Wardens' box):
- **Kestrel** advances over Zenith's first delegate (Rook or Odessa), Gauntlet blazing.
- **Valen** advances.
- **Sigrun** advances.

```
V141 = 3.
```

### **The garden court** (touch, the arena's garden court, after the R16, V141 == 3 → 4)
```
[if ROWAN_ALIVE]
  (Juno and Rowan on the same bench, sitting apart. The space between them is exactly one person wide.)
  [if TEO_SAVED]
    [portrait: TEO, neutral] (holding up his glassed fingers) I could hear everything while it had me. Everyone who sat with me. (To Rowan.) You sat with me. Every night. I heard you.
    (Rowan sits down on the grass, and cries. Juno takes his good hand. It's the first time they've touched since Ironreach.)
  [elif has VENAM'S TESTIMONY]
    (You play Venam's Testimony. Rowan listens to it twice. Then he sits down on the grass. Juno takes his good hand.)
  [else]
    [portrait: JUNO, sad] Corvin says they dream. I'm going to believe him. (She takes his hand herself, slowly, as if he might break, or she might.)
[else]
  (Juno alone on the bench, holding a pressed lily from the Bride Tree. She doesn't say anything. She makes room on the bench.)
V141 = 4.
```

## Day 3: Exhibitions and the Festival grounds (V141 == 4 → 5)
`Script: Prismfall::Festival::Draw.set_day(3)`. It's an open day; the exhibition menu is at the arena desk (`Prismfall::Festival.exhibition_menu`).

**The Eevee Octave, *The Ninth Verse*** (EEVEE_OCTAVE.md; the Memorial Garden, 489):
- Opens once all eight singers have been helped (Carol plus the road seven).
- **Vesper** waits with all eight:
  ```
  [portrait: VESPER, neutral] We all lost everything the year the Crown broke. The Choir calls us the lucky ones. I think we're just... what was left.
  ```
- **The gauntlet:** the eight singers in the order the PC helped them, back to back with no healing. Each has one Eeveelution on its home field using its type's Z-move. Then **Vesper's Eevee "Amen"** with Extreme Evoboost on the Grand Stage.
- **Reward:** an **Eevee** and the **Eevium Z** (there's no ring: the PC's Warden's ring wakes it).
  ```
  [portrait: VESPER, happy] Its chip is off the Crown's stone, and our glass came out of the night the Crown broke. They know each other.
  ```
  *(If Understudy is still an Eevee, the crystal works for it too; if it evolved, Vesper notes which Imprint "claimed" it.)*

**The other exhibitions** (NS §3.6, original characters only):
- **The Pageant Bout:** Dorian and Rook in a double, staged as "a duet for the cameras", with Rook's Rotom filming it.
- **Juno's Garden Match**, if she wasn't the PC's R16.
- **The Ebb Guild match** with Marisol while Teo heckles from the stands (`TEO_SAVED` and close).

**The Festival grounds:**
- **The Concordance Spire** (Battle Tower) under construction, as a teaser. On its scaffold: a **Glassfall Sliver**.
- Street food from every kingdom. **Gift: Alcremie "Festival"** (Lv 60, Sweet Veil), from the sweets stall, as a "thank you for not being glass".
- Dorian rehearsing in secret with Celestine: one overheard line, "No, darling, you can't *lie*, so *phrase* it like a threat."
- **The Grounds Ladder:** 12 open challengers in the kingdom pavilions (roster at the end).
- **Warden hangouts:** every Warden in their pavilion, one line each.
- **Larch's stall: the Sliver exchange's last tier** (100).

### **Envoy Okoro** (touch, the Concert's tent, V141 == 4 → 5)
```
[portrait: OKORO, neutral] The Concert sent me to decide one thing: whether to cut Velmora off from the world. Severance. Quarantine for ever. The Bleed is a contagion, they say. Convince me it isn't, or don't.
```
**Proof** needs **two of three**:
- the LARCH PAPERS;
- the ARBITER BLUEPRINTS;
- **testimony that the Fixed still dream**: Teo's (`TEO_SAVED`), Corvin's Quiet Ward records (`CORVIN_FREED`), or Venam's Testimony.

*(The LANCE MANIFESTS (Ch14) can stand in for either document.)*
```
[if two of three]
  > Lay it out for her. (proof)
    Script: pf_choose(:ch20_envoy, :proof)
    [portrait: OKORO, neutral] (reading for a long time) ...Caused. Not caught. Caused, and so curable. (She closes the folder.) I'll recommend against Severance. They may not listen. But I'll have said it in writing, and that's what the Concert reads.
[always]
  > Plead with her. (plea)
    Script: pf_choose(:ch20_envoy, :plea)
    [portrait: OKORO, sad] I believe you. I'm drafting it anyway. With regret. The Concert doesn't read regret.
V141 = 5.
```

## Day 4: Quarterfinal ("the honest view") (V141 == 5 → 6)
`Script: Prismfall::Festival::Draw.set_day(4)`, then `Script: Prismfall::Festival.next_match` at cap 92.

| Candidate | Condition | Lines |
|---|---|---|
| **Celestine (fallback)** | default | "I cannot lie, so listen while we fight." **After the match:** "Give them back. I've waited forty years to say that to someone who could." |
| **Sigrun** | `resonance <= -3`, or the PC helped Isenmar break her father's legions | "Dragons weigh things. You've gotten heavier." |
| **Kaito** | the oath was `:keep` | "You'd keep them? Marrowgate's still knocking." |
| **Ysolde** | `KESTREL_FALLEN` | "If I can't reach him, I'll find out what reached you." |
| **Odessa** | Odessa holds a seat; five close Bonds; Harmony-leaning | "Everyone keeps telling you what you're *for*. The wind doesn't care. What do *you* want?" |
| *(Ruin Route: Archseer Dask; 12_RUIN_ROUTE.)* | | |

**The other QF (highlights):**
- **Kestrel** beats **Kaito**. Kaito's Lucario felt it: "That isn't him fighting."
- **Valen** advances.
- **Sigrun** advances, unless she was the PC's QF; then Celestine plays on in Ashkaar's seed.

```
V141 = 6.
```

## Day 5: The Good Tea, Corvin, the Masques, the audience, Little Owl (V141 == 6 → 12)
`Script: Prismfall::Festival::Draw.set_day(5)`

- **Comedy scene Ch20, "The Good Tea"** (15_COMEDY as written; running gag 1 pays off), in the morning. It's the last joke of the chapter.

### Corvin (touch, at the Sanctum colonnade, V141 == 6 → 7; no jokes from here to the end of Interlude V)
```
[if CORVIN_FREED]
  [portrait: CORVIN, neutral] (coming out of the Sanctum, mask down, washing his hands in a basin as if he'll never get them clean) I've been treating Valen. Privately. Don't tell the Accord, they think he's resting.
[else]
  (A Sanctum physician, not Corvin. Corvin isn't here. He's in a cell, and has been since Ch16. The physician says the same words, worse.)
[speaker] He has weeks. Maybe. He's holding the Plates quiet *right now*, with his body, every hour since the ceremony. He'll fight you tomorrow on what's left.
V141 = 7.
```

### **The Night of Masques: "The Gilded King"** (autorun, the Basilica square at night, V141 == 7 → 8)
```
(The Basilica square. A stage of planks and lanterns. The Saltmere Players, in the Hollow's ogre masks, as the chorus. A sign: THE GILDED KING. A PLAY BY ANSEL CREWE. FIRST PERFORMANCE IN 248 YEARS.)
[portrait: DORIAN, happy] (stepping out before the curtain) Ladies, gentlemen, the Accord, the Concert, assorted kings, and one Chancellor who has sent the Wardguard to stop us: welcome. Tonight we tell the truth. It's a novelty. Do try to enjoy it.
```
The play, as a staged cutscene on the planks (actors as events; Celestine voices Maren from the wings):
- the Blight;
- the chain;
- the god breaking itself;
- the city drowning;
- the daughter's penance.
```
[portrait: CELESTINE, sad] (as Maren, from the wings, a voice that can't lie) I broke my father's chain and drowned my father's city. Both of those are true. I'd do the first again.
(The Wardguard arrives at the square's edge, Hollis behind them.)
(In the way: Kaito, arms folded, his Lucario beside him. [if TEO_SAVED] Teo's strikers, in their work-coats, linking arms.)
[portrait: KAITO, neutral] It's a play, Chancellor. Sit down. You might learn something.
(The Wardguard doesn't push.)
(On the planks, the actor playing the Gilded King, in crimson-lined velvet and a jagged pasteboard crown, steps to the apron and raises a prop chain of painted wood to the real sky.)
[name: The Gilded King (actor)] You ask why I do not bow before the eighteen lights, my daughter? Look down at Aurelia! Look at our aqueducts, our towers, our bread!
[name: The Gilded King (actor)] The sky hung its splendour above MY kingdom without asking leave, and when the blight came, heaven kept its hands folded!
[name: The Gilded King (actor)] Let priests measure their gratitude in crumbs. A king does not beg for what stands beneath his sun. If heaven will not kneel, we'll build a chain.
(Every head in the square turns to the Meridian box.)
(In the box, Aurelian Voss stands up. He applauds. Alone. Warmly. For a long time.)
[portrait: VOSS, happy] Bravo. They finally cast the king correctly.
Switch S157 CH20_MASQUES_DONE = ON. V141 = 8.
```

### **Calla** (`:ch20_calla`; only if `:ch16_rook == :hold` or `MAGNUS_KEPT_FAITH`; touch, a figure in the crowd, V141 == 8 → 9)
```
(In the crowd after the play: a young woman still in a Meridian lanyard, shaking: Calla Wren, who scanned you on the dock at the very beginning.)
[portrait: CALLA, sad] I scanned you on the dock. I photographed the screen. I've been sending him your life for six months. Let me do one thing that isn't that.
[portrait: CALLA, neutral] I can get the arena's power schematics to Larch. I have some. I can go back for the rest.
> Shelter her (Edda's boat). (shelter)
  Script: pf_choose(:ch20_calla, :shelter)
  (Edda takes her by the elbow without a word and walks her down to the Pilgrim's Rest staithe. The partial schematics go to Larch: one crack in the Engine. She lives.)
> Send her back for the full set. (send_back)
  Script: pf_choose(:ch20_calla, :send_back)
  [portrait: CALLA, neutral] (a breath) Okay. Okay. I can do that. (She goes back towards the Spire.)
  (At dawn a Gale Post envelope arrives for Larch: the full set, two cracks in the Engine. There's a smear of blood on the envelope. Calla doesn't come back.)
> Turn her away. (turn_away)
  Script: pf_choose(:ch20_calla, :turn_away)
  [portrait: CALLA, sad] Then I'll just — go home, I suppose. (She leaves. Nobody sees her again.)
V141 = 9.
```
*(NARRATIVE_KEYS: `:shelter` RES+1 · `:send_back` RES−2 (Kroll finds her on the Spire stairwell) · `:turn_away` MERIDIAN+1.)*

### **Valen's audience** (touch, the Sanctum door, V141 == 9 → 10; key event 2)
```
(The Sovereign's Sanctum. Candlelight. A camp bed, not a throne. Valen sitting on the edge of it with his crystal arm resting on a cushion beside him, like something borrowed that he has to give back.)
[portrait: VALEN, neutral] Sit. I'm not going to defend myself. I'm going to explain. It's different. Slightly.
[portrait: VALEN, neutral] Every ten years I bring the Plates home to Crownhaven, and every ten years Velmora *endures*. You noticed I never said "thrives". Nobody ever notices.
[portrait: VALEN, sad] Morwen didn't cause the Glassfall. I let them say she did, because if the world knew the ceremony could fail, the kings would tear the Plates out of the ground and we'd all drown. I chose a country over a woman's name.
[portrait: VALEN, sad] I'd do it again. I hate that I'd do it again.
[portrait: VALEN, neutral] When you beat me tomorrow — and you will — I'll put the Crown on you. The splinter in your heart will make it whole. You'll hold the Plates quiet for a hundred years, and you won't age as fast as I did.
[portrait: VALEN, sad] You'll be... very lonely. I'm sorry. I have no other door.
```
**`:ch20_audience`** (the PC's authored line):
```
> "There's another door. The Hymn. We give them back." (return)
  Script: pf_choose(:ch20_audience, :return)
  \pf[PLAYER,neutral] There's another door. The Hymn. We give them back.
  [portrait: VALEN, angry] And let eighteen cities go dark? Rimeholt drowns. Cindervault freezes. Verdance's fields fail in a year —
  [if has THE HYMN OF RETURN (complete)]
    \pf[PLAYER,neutral] "Not chained, not broken, not bought, not crowned: given back, as a gift is found."
    [portrait: VALEN, shocked] (very quietly) ...Maren wrote that. I thought it was a poem.
> "Then I'll wear it. Somebody has to." (keep)
  Script: pf_choose(:ch20_audience, :keep)
  \pf[PLAYER,neutral] Then I'll wear it. Somebody has to.
  (Valen weeps. Once. He doesn't hide it, and he doesn't do it again.)
> "You don't get to decide that for me. Nobody does." (refuse)
  Script: pf_choose(:ch20_audience, :refuse)
  \pf[PLAYER,angry] You don't get to decide that for me. Nobody does.
  [portrait: VALEN, happy] (and it's the first time you've seen it) Good. Then decide it yourself, tomorrow. That's all I ever wanted, and I never had the courage to want it out loud.
Switch S158 CH20_AUDIENCE_DONE = ON. V141 = 10.
```
*(NARRATIVE_KEYS: `:return` VALEN+2 RES+1 · `:keep` VALEN+3 · `:refuse` VALEN+1. `VALEN_COLLAPSED` = `:refuse` with a cold Bond, no Ilsa, and live telemetry: Voss's pre-ignition drains him overnight.)*

### ☠ **`GO_EARLY_CROWN` "Early Crown"** (at the audience's end)
```
[portrait: VALEN, panic] (standing too fast, the crystal arm knocking the cushion to the floor) Wait. Tonight. I could do it tonight. Here. Skip the Final. So I don't have to hurt you first.
(He's lifting the Crown off his own head with his good hand. It's shaking.)
> Let him.
  [if made ILSA's warning]
    (Ilsa's voice, from the colonnade this afternoon: "Don't let him hand you anything tonight. He's not thinking, he's drowning.")
  > Let him.  Script: Prismfall.game_over(:GO_EARLY_CROWN)
  > Don't.
> Don't.
  [portrait: VALEN, sad] (lowering it) ...No. No. You're right. Tomorrow. Properly. Go and sleep. One of us should.
```
*(NARRATIVE_KEYS §9 epitaph: "The Crown was whole for one second. Then it was Meridian's." Voss has the cradle, so the half-Tuning Fixes the PC in the Sanctum.)*

### **"Little Owl"** (`:sq_little_owl`; autorun outside the Sanctum, V141 == 10 → 11)
```
[if Ilsa's quest steps done]
  (Ilsa at the Sanctum door, earmuffs in her hands, not on.)
  [portrait: ILSA, neutral] (to you) Stay. Please. I need someone to have heard it.
  (She goes in. You stand in the door.)
  [portrait: ILSA, neutral] You chose a country over a daughter. Fine. Then save the country, Father. Don't make a child pay for it.
  [portrait: VALEN, sad] (a long time) ...Little owl.
  (She sits down on the camp bed beside him. She stays the night.)
  Script: pf_choose(:sq_little_owl, :reconciled)
[else]
  (Across the colonnade: Ilsa, watching the Sanctum door, earmuffs on. She doesn't go in.)
  Script: pf_choose(:sq_little_owl, :refused)
V141 = 11.
```
*("Little owl" is the name the player heard in the Mindscape in Ch13.)*

### Conditional: **Morwen's Echo** (exhibition; `KESTREL_YSOLDE_RECONCILED` and `:ch15_kestrel == :resolve`; after midnight, a Crownhaven chapel)
```
(Ysolde lights the Hollow Cathedral's lantern in a small Crownhaven chapel. The echo comes through it, in her Warden's coat, translucent, almost smiling.)
[portrait: MORWEN, neutral] Little one. Let me see what I bought.
BATTLE: Prismfall::Festival.exhibition(:ECHO_MORWEN) — gentle, once.
[portrait: MORWEN, happy] (fading) Good value. Tell him I said so.
```

### **INTERLUDE V, "The Last Night"** (play as Valen; V119 = 5; the Sanctum before dawn; V141 == 11 → 12)
```
(Before dawn. The Sanctum. The player is Valen: slow, one arm, the crystal one held against his chest.)
```
**Three letters at the desk** (an interact each; the player writes them by choosing):
1. **To Ilsa.** If `ILSA_RECONCILED`: "(He looks at Ilsa, asleep on the camp bed under his coat. He tears the letter up. He doesn't need it.)" Otherwise he seals it.
2. **To Morwen's son.** "Kestrel. I'm not asking you to forgive me. I'm asking you to be better at this than I was. It won't be hard." Sealed.
3. **To "whoever wears it next".** "It's heavier on the second day. Nobody tells you that. I'm telling you." Sealed.

**The window** (a Zygarde Cell glowing on the sill):
```
[portrait: VALEN, neutral] (to the Cell) Order, not justice. I chose order. Was I wrong?
(The Cell pulses, once.)
(The player decides what that means. There's no menu. Valen looks at it for as long as the player lets him, and then the dawn comes up.)
V119 = 0. V141 = 12.
```

## Day 6: Semifinal: Kestrel (K8) (V141 == 12 → 13; key event 3)
`Script: Prismfall::Festival::Draw.set_day(6)`, then `Script: Prismfall::Festival.next_match` at cap 94. The manager resolves Kestrel's version (Redeemed or Fallen) from `KESTREL_FALLEN`.

**Kestrel (Redeemed)** (fallback):
- He fights with the Gauntlet at first. At the first field-cycle, he looks at the Gauntlet's light, **tears it off** and throws it across the arena floor:
  ```
  [portrait: KESTREL, angry] No. Not like this. If I beat you, I beat *you*.
  ```
  (The battle hook ends the Gauntlet's field control.) He finishes with Morwen's Mismagius and his Aegislash.
- **If he wears Morwen's Ring** (`:ch18_kestrel_ring == :give_now`): his **Scizor Mega Evolves** (`PrismfallMega::MORWEN_RING`, automatic at battle start when it's sent out).
  ```
  [portrait: KESTREL, sad] Mum. Just this once. Answer me.
  (it does)
  [portrait: KESTREL, neutral] ...She'd have hated the Gauntlet.
  ```
- **If the PC kept the ring:** no Mega (SPINE Rev 21: no borrowed rings).

**Kestrel (Fallen):** the Gauntlet stays on. His Pokémon glow with stolen Imprint, and the field cycles under his command. There's no Mega (a Fallen Kestrel can't have the ring). After the loss, the Gauntlet overloads and burns his hand, and Voss's men carry him off "for medical attention". He reappears in the hijack, harnessed into the Engine (Ch21).

```
Variable V114 KESTREL_STAGE = 5. V141 = 13.
```

### **Morwen's letter** (autorun on the arena floor after the SF, V141 == 13 → 14; no jokes from here)
```
(Ysolde walks out onto the arena floor. Forty thousand people watch her do it. She holds out a sealed letter.)
[if !KESTREL_FALLEN]
  (Kestrel takes it. He opens it there, in front of everyone. The arena screens cut away, tactfully, to the sky.)
```
The letter (Key Item, readable later):
> *"Kestrel. If you're reading this, you're ready, or Ysolde's given up waiting. Both are fine. I didn't fail. I chose. There was a child in the light and I was nearest, and I'd have wanted someone to choose you. They'll call me a disgrace. Let them. Be a Vane anyway — be the kind that's nearest when it matters. I love you more than my seat, more than my name, more than my Plate. That's the whole letter. — Mum."*
```
[if !KESTREL_FALLEN]
  (Kestrel sits down on the arena floor.)
  [if PC still has MORWEN'S RING]
    > Give him the ring.
      (You hold it out. He takes it without looking at you. He puts it on.)
  [portrait: KESTREL, sad] ...Then you take him. Take him for both of us.
  [if KESTREL_YSOLDE_RECONCILED] (He moves over, a little, on the arena floor. Ysolde sits down beside him.)
[if KESTREL_FALLEN]
  (He's already gone, carried off between Meridian medics, his hand wrapped in white. Ysolde stands on the arena floor with the letter, unread, for a long time. Then she puts it back inside her coat.)
  [if :ch12_letter == :keep] (You have Morwen's other letter, the dead one, to "I." You'll be able to quote her to him in the Engine.)
V141 = 14.
```
**The other SF** (a one-line result if Sigrun was the PC's QF): **Valen beats Sigrun.** She entered to win the Crown herself and spare the PC, and he beat her *to protect her*. She leaves the arena without a word.
```
(The Basilica roof, at dusk. Sigrun, sitting on the ridge with her knees up, dragonhide coat around her.)
[portrait: SIGRUN, angry] He beat me with an arm made of glass. I've never been so angry in my life.
[portrait: SIGRUN, sad] (a long pause) He did it so I wouldn't wear it. Didn't he.
```

## The eve of the Final (chapter close; autorun at the PC's room in Pilgrim's Rest, V141 == 14 → 15)
```
(Night. A room above the inn at Pilgrim's Rest. Through the window, the Prism Arena, lit, eighteen colours on its glass, humming faintly. You can feel it humming in your chest.)
(On the bed: your badge case, eighteen badges. Your mother's letter. The Hymn. The blueprints, folded small. [if MORWEN'S RING still held] Morwen's ring.)
(Somebody knocks. Edda, with two cups.)
[portrait: EDDA, neutral] Couldn't sleep either. (She sits on the windowsill.) Told you I had a bet on.
[portrait: EDDA, neutral] I bet on you walking out of that arena on your own feet. Long odds. Long odds are the only ones worth taking.
V141 = 15. Variable V102 STORY_CHAPTER = 21.
QUEST LOG: "The Festival of Champions" — The Final. Valen. Tomorrow.
```
*(Ch21, "Sovereign", is Day 7.)*

---

## Map events needed (Chapter 20)
Crownhaven (480–519) isn't built. **[NEW]** = an event or map not in maps.json. V141 = **CH20_STEP** (design/FLAGS.md). Maps go through the three-pass workflow (design/MAPGEN.md, top).

**Crownhaven upper city:**
- the eighteen banners (interact = consent line; white or grey by NS §6.2)
- Tamsin
- the faction ambients (Meridian security, disguised Hollow porters, the observers' gallery)
- Okoro's tent (`:ch20_envoy`, V141 4 → 5)
- the Basilica steps: **the draw** (V141 0 → 1; `:ch20_colors`; the Hierophant's bowl)

**The Prism Arena:**
- **the ceremony**: the procession of 18 Warden events down the stair, plate-setting animation; Valen's glove; the white vision; the stands; S156; V141 1 → 2
- Rook's leak (screen picture)
- the floor for each match (the manager), highlights from the Wardens' box
- the exhibition desk
- **the SF** and **Morwen's letter** on the floor (V141 12 → 14)
- **Sliver** in the stands

**489 Glassfall Memorial Garden:** Carol, then Vesper and the eight (the Octave gauntlet); a **Sliver**.

**The garden court:** the bench (Juno, Rowan and Teo by flag; V141 3 → 4).

**The festival grounds:**
- kingdom pavilions (Warden hangouts; the Grounds Ladder, 12 trainers)
- street food (**Alcremie "Festival"**)
- the Concordance Spire scaffold (a **Sliver**)
- Larch's stall (Sliver exchange, tier 100)

**The Basilica square:**
- **the Night of Masques** (stage, Players as events, Celestine's voice from the wings, the Wardguard line, Kaito and Teo's strikers, Voss's box applause; S157; V141 7 → 8)
- **Calla** (V141 8 → 9)
- the Basilica bell (a **Sliver**)

**The Sovereign's Sanctum:**
- Corvin (V141 6 → 7)
- **the audience** (V141 9 → 10; `GO_EARLY_CROWN`; S158)
- **Little Owl** (V141 10 → 11)
- **Interlude V** (Valen playable: the desk letters, the window Cell; V119 5 → 0; V141 11 → 12)
- the window (a **Sliver**, after the Interlude)

**A Crownhaven chapel:** Morwen's Echo (conditional).

**The Basilica roof:** Sigrun (after the SF).

**Pilgrim's Rest room:** the eve (V141 14 → 15; V102 = 21).

**888 Glassfall Scar:** the child-sized space (the last **Sliver**: #100, for players who came by the Ascent).

## Rosters (Ch20)
- **Bracket and exhibitions:** existing PBS via the Festival manager (`008_Festival_Data.rb`); the draw rules are NS §3.
- **The Grounds Ladder** (new; 12 open challengers, Lv 88–90; original characters, one or two per kingdom, two Pokémon each, with the kingdom's field in their pavilion):

| Kingdom | Challenger(s) |
|---|---|
| Elowen | a Briarwick weaver |
| Isenmar | a Rimeholt harpooner |
| Zenith | a Lumen streamer; a Cogsworth foreman |
| Nadir | a Moon Market broker |
| Ashkaar | a Wyrmrest rider |
| Ossaria | a Cragholm lamp-runner (Pip's rival); a Duneholt well-keeper |
| Antumbra | a Gravenmoor lantern-priest; a Vigil embalmer |
| Crownhaven | a Wardguard; a Choir cantor |

**EventMons:** Eevee "Amen" + Eevium Z (the Octave), Indeedee "Usher" (gift, Lv 60), Alcremie "Festival" (gift, Lv 60).

**Key Item:** MORWEN'S LETTER (Kestrel's).

**Portrait requests (art, to Gemini):** **OKORO** (`neutral`, `sad`), **HOLLIS**, **VALEN** without the glove (crystal arm; `neutral`, `sad`, `panic`, `happy`), **CALLA** `sad`, **CAROL** and **VESPER** (Octave), the Hierophant (plain is fine).
