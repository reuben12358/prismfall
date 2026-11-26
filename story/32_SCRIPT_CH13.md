# Script: Chapter 13 — "Behind the Glass" (the Glass Road, Antumbra, Lucent, Gym 12; the Mindscape; the tribunal; the Fault; end of Act III)

> **Final playable script** for Chapter 13, the last chapter of Act III. It covers the Glass Road (740 Conductors' Causeway, 741 the Wired Wood with 750/751 Verdigris, the Crown Road's 602 Candle Down, 603 the Highwold and 756 Kingsmead, 752 the Looking-Glass Wood with 753/754 Glassmere, 742 Mirror Mere), Antumbra (743 the Threshold, 755 Widdershins Walk, Lucent 340–345, the Athenaeum and its Glass Court [NEW]), Gym 12 (350–356), the Mindscape [NEW], and the optional 748 Shattered Sky. None of these maps is built; the list at the end is what to build from.
> Follows `story/31_SCRIPT_CH12.md`. The Act IV opener (Ch14, "The Deep Seams") follows this. Sources: 06_ACT_III Ch13, 03_CAST (Ilsa, Dask, Rowan, Juno, Kaito, Valen, Kroll/Sable, Marchetti, Wick, Celestine, Ellery, Vesper), 09_MYSTERIES (#1, #6, #9, #10, #12, #13, #16, #17, #25, #27), NARRATIVE_KEYS (`:ch13_remember`, `:ch13_kaito`, `:ch13_rowan_testimony`, `:ch13_fault`, GO_LOOKING_BACK, `KAITO_TESTIFIED`, `ROWAN_ALIVE`, `MARCHETTI_TURNED`, `IRONREACH_EVIDENCE`), 15_COMEDY (Ch13 "Thinking Loudly"), GYM_PUZZLES Gym 12, EEVEE_OCTAVE (Vesper's second meeting, Lento), BALANCE (Ilsa, Kroll Ch13), WALKTHROUGH Ch13, `design/CHAPTER_BEATS.md`.

## Conventions
As in the earlier scripts. **Portrait cast here:** Ilsa, Juno, Rowan, Kaito, Valen, Kroll (Sable unmasked), Marchetti, Wick, Celestine, Dask, Voss (a screen), and **the PC** (the first authored line, in the Mindscape; `\pf[PLAYER,…]`). **Plain:** the child (the PC at five; no portrait, a small sprite), Ines (a voice and a silhouette), Hierophant Ellery and the Accord choristers, Vesper (the Octave's leader, met in the cloister), the Accord clerk of the court, the kings' observers, Verdigris's and Glassmere's townsfolk, every trainer. Gym 12 is a single battle: `Prismfall.gym_battle(pfm_gym(:LEADER_ILSA), double: false)`. Kroll is `TrainerBattle.start(:MERIDIAN_KROLL, "Sabine")` (base version: Ch13, Lv 59, Mega Sharpedo; BALANCE).
**Counter:** V134 **CH13_STEP** (design/FLAGS.md): 0 on the Causeway · 1 Kingsmead and the Glassfall Scar · 2 Mirror Mere: Dask's rule · 3 across the Threshold (S134) · 4 Lucent: Ilsa ("Thinking Loudly"; the gym opens) · 5 Gym 12 won · 6 the Mindscape (S135) · 7 Juno and the Ralts · 8 the tribunal (S136) · 9 the Fault (S137) · 10 dawn: the Secret Articles (Act III closed; V101 = 4, V102 = 14).
**State set here:** S134 CH13_ANTUMBRA_ENTERED, S135 CH13_MINDSCAPE_DONE, S136 CH13_TRIBUNAL_DONE, S137 CH13_FAULT (Act IV's encounter version 1 everywhere), V113 ROWAN_STATUS (by `:ch13_fault`), V101 = 4. Keys: `:ch13_remember`, `:ch13_kaito`, `:ch13_rowan_testimony`, `:ch13_fault`. Key Item: SECRET ARTICLES (sealed). WICK'S LETTER is delivered here if the PC carries it.

## The chapter's key events (design/CHAPTER_BEATS.md)
1. **The Mindscape memory** (`:ch13_remember`). Ilsa opens the memory a Mismagius sealed in the PC: Lower Crownhaven, AF 290, the Choir, the Crown, brass machines with sunburst plates, the crack, a woman in a Ghost Warden's veil over the child. The PC speaks for the first time. Build-up: the NULL scan (P), Larch's journal (Ch1), the badge case's chords, the Glassfall Scar on the road in, the late reflection (Ch12). Payoff: the memory, and Ilsa's "The man in white was my father." Consequence: the Ch15 echo (harder on `:not_yet`), Ilsa's "Little Owl".
2. **The tribunal and the Fault.** Rowan's trial in the Glass Court: Kaito's Marrowgate (`:ch13_kaito`), the PC's testimony (`:ch13_rowan_testimony`), Sable unmasked as Kroll (with the COMM-DEVICE), then the Arbiter's test-fire under Cogsworth: the ground moves, the sea pulls back from the south coast, the court's floor drops into the flooded undercroft, and the PC can reach Rowan or Marchetti (`:ch13_fault`). Build-up: Ch9's unmasking, Juno's speech, Ch12's SPLITTER CASING. Consequence: Act IV's map states (S137), who leads the Lantern Hollow, Marchetti's turn, Rowan's Festival seat.
**Density** (CHAPTER_BEATS: "the densest chapter; keep the gym short"): Gym 12 is three rooms and the arena, no more; the road's optional content (Verdigris, Glassmere, the Still Water) sits before the Threshold. **No jokes** from the court's first gavel to dawn on the steps; "Thinking Loudly" is before the gym. **No side content** opens in Lucent between the Mindscape (V134 == 6) and dawn (V134 == 10) except the cloister scene with Juno and Vesper's optional sparring, which are the evening before the court.

---

# CHAPTER 13 — "Behind the Glass"

**Chapter start:** V101 = 3, V102 = 13, V134 = 0 (the late reflection closed Ch12). The PC is on Conductors' Causeway (740).

## Map 740 — Conductors' Causeway (`:STORMFRONT`) and Map 741 — the Wired Wood (borderland G), 750/751 Verdigris
Road sign (740): "CONDUCTORS' CAUSEWAY. The Glass Road. Lucent by the Crown Road and the Mere."
- The causeway's puddles: the PC's reflection behaves after the first one. A lineman on a pylon ladder: "Don't stare at the water out here. My granddad said the water on the Glass Road shows you what's coming. My grandma said it shows you what you'd rather not. They were both very cheerful people."
- **The Wired Wood**: a borderland forest grown through decommissioned Lattice pylons; copper-green bark, birds nesting in insulators, a hum in the trunks. **Verdigris** (750) is a town of retired linemen. A retired lineman at the Center (751): "Larch? On the screens? I worked her first line. Ferrow's Landing, AF 281. She brought us all cake. Nobody brings linemen cake." *(Ch12's photograph on Voss's desk was the same line.)*
- The Wardens' Circular at 751: Juno: "LUCENT BY THE MERE. TRIBUNAL IN FIVE DAYS. I'VE WRITTEN THE SPEECH ELEVEN TIMES." Kaito replies: "Stop at ten."
Trainers (Lv 55–58): linemen, a pylon-climber, a researcher.

## The Crown Road: 602 Candle Down, 603 the Highwold, 756 Kingsmead — **"The Scar"** (autorun at Kingsmead's old paddock gate, V134 == 0 → 1)
```
(Kingsmead: old royal paddocks at the foot of the Crownwall's north-west face. The wall goes up, white, forever. Halfway up it, a wide patch glitters, as if somebody threw a handful of glass at the stone and it stuck.)
[name: Paddock Keeper] The Glassfall Scar. AF 290.
[name: Paddock Keeper] Forty people were up on the wall-walk when the Crown cracked, watching the Festival from the top.
[name: Paddock Keeper] The light came out over the wall and they're still up there.
[name: Paddock Keeper] In the glitter. You can see a hand, if the sun's right.
(Your chest hurts. Not a lot. The star-shaped scar under your collar, the one with no colour, aches like a bruise somebody pressed.)
[name: Paddock Keeper] [emote: question] You all right? People come over queer sometimes, here.
[name: Paddock Keeper] The Synod says the Glass is thin under the Scar.
[name: Paddock Keeper] Says some folk can hear it.
V134 = 1.
```
*(06_ACT_III "The road": the Scar sets up the Mindscape. 09 #1: the scar is the PC's; the shard aches near anything that broke in AF 290.)*

## Map 752 — the Looking-Glass Wood (borderland H), 753/754 Glassmere, and the Still Water (optional)
The Looking-Glass Wood: silver birches with mirror-bright bark; the path doubles back on itself in reflections.
- **Glassmere** (753): a town that lives half on the shore, half on its reflection in the Mere. A child: "Mum says don't wave at your reflection here, it waves back first sometimes."
- **The Still Water** (`AN_OCTAVE_STILL_WATER`, Lento of the Octave; EEVEE_OCTAVE): open from here, on the frozen Mirror Mere past Glassmere; before the Threshold. (Vesper's sparring and her letter come at the Athenaeum cloister the night before the court.)

## Map 742 — Mirror Mere: **"Behind, Welcome"** (autorun at the Mere's edge, V134 == 1 → 2)
```
(A lake so still it isn't a lake. The sky is in it, the birches are in it, you are in it. Halfway across, the reflection stops matching: in the water, the far shore has a city on it, white colonnades and an upside-down city hanging over them in the sky. On the real far shore there's nothing.)
(On a stone landing, a tall old man in a grey robe with a lantern. One eye brown, one eye white.)
[portrait: DASK, neutral] Welcome, behind. Behind, welcome.
[name: Dask] Archseer Imre Dask, of the Veiled Synod.
[name: Dask] The Provost sent for you.
[name: Dask] Ilsa Marr doesn't send for people. So: here I am, sent.
[name: Dask] The Glass is thin this year. It wasn't thin when I was a boy.
[name: Dask] Something on your side is pulling at it.
[name: Dask] Something on ours is pulling back.
[name: Dask] One rule. Only one.
[name: Dask] Never look back through the Glass once you've crossed.
[name: Dask] Not for a voice. Not for a name. Not for anyone.
[name: Dask] Once you're behind, you're behind.
[name: Dask] [emote: dots] (turning away) Once you're behind, you're behind.
[name: Dask] I said it twice. Remember that I said it twice.
(He walks out onto the water. It holds him. It holds you.)
V134 = 2.
```

## Map 743 — the Antumbra Threshold (`:INVERSE`): **"Don't Look Back"** → GO_LOOKING_BACK (autorun two-thirds of the way across, V134 == 2 → 3)
- The Threshold: rivers run uphill, shadows fall toward lamps, the path's signposts are in mirror-writing. One signpost, legible only in its reflection: "DO NOT LOOK BACK."
- Wild Ghost, Psychic and Dark Pokémon; `:INVERSE` (type matchups flip).
- **In every reflection the PC passes** (puddles, the river's uphill face, a signpost's brass), at the edge: a shadow with six black wings, watching. It's never there when the PC looks straight at the spot. *(09 #25, Giratina.)*
```
(Behind you, very far, from the shore you left, a voice.)
JUNO (off): \PN! \PN, wait! It's me! I came the long way— wait for me! Please!
(It's her voice exactly. The catch in it. The way she says your name like a question.)
[portrait: DASK, neutral] (ahead, not turning) Behind, welcome.
```
```
> Look back.
  > Look back?
    > Yes.
      (You turn.)
      (On the far shore there's no one. In the water at your feet, there's you, facing the other way, already walking back toward the shore you came from. It doesn't look round.)
      (When you try to move, your feet move the wrong way.)
      Script: Prismfall.game_over(:GO_LOOKING_BACK)
    > No.
> Keep walking.
(You keep walking. The voice calls twice more, then stops in the middle of your name.)
(On the far side, the ground is ordinary ground again, and there's a city.)
Switch S134 CH13_ANTUMBRA_ENTERED = ON. V134 = 3.
```
*(GO_LOOKING_BACK: NARRATIVE_KEYS §9, epitaph "You looked back. Now you're the reflection, and something else is wearing your face to the Festival." Foreshadowing: Dask's rule, stated twice, and the mirror-writing sign. Juno is in Lucent already (she came by the Accord's coach); the voice isn't hers.)*

## Map 755 — Widdershins Walk, and Lucent (340–345; Antumbra, `:MINDSCAPE`)
Widdershins Walk: a colonnaded road where everyone walks on the left going one way and the right coming back, and nobody can say why.
```
(Lucent. White colonnades, quiet streets, people who speak softly. And over the city, upside down in the sky, the same city: its towers pointing down, its streets full of tiny people walking on the underside of the clouds.)
[name: Gate Scholar] The Speculum. The Mind Plate's half of us.
[name: Gate Scholar] Don't stare, it's rude. They can see you staring.
```
**Lucent townsfolk (340 Athenaeum Quarter, 341 PC, 342 Mart, 343 Tribunal Ward):** the Tribunal Ward is full: Wardens' coaches, kings' observers, Accord guards, Meridian lawyers, press; a hawker selling "ROWAN: MONSTER OR MARTYR?" pamphlets (both covers, same pamphlet inside); an Accord guard: "Meridian didn't want to give him up. The Sovereign made them. Took a vote. Won by two."

### Map 344 — the Great Reading Hall: comedy scene Ch13, **"Thinking Loudly"** (touch, Ilsa at the reading desk, V134 == 3 → 4)
```
(A hall of books so high the top shelves are in cloud. At a desk in the middle, a woman in high-collared robes with silver-blonde hair pinned up with a pencil, and big padded earmuffs.)
[portrait: ILSA, neutral] You're thinking very loudly. Please stop.
> (Think about nothing)
  [portrait: ILSA, neutral] That's worse. Now it's just a hum.
> (Think about Larch's tea)
  [portrait: ILSA, shocked] [emote: exclaim] Oh, that's vile. Who does that to kelp?
  [portrait: ILSA, angry] No— stop— you're thinking about it *more* now—
> (Think about Kestrel buying four eels)
  [portrait: ILSA, happy] ...Heh.
  [portrait: ILSA, neutral] I didn't laugh. Provosts don't laugh.
  [name: Ilsa] You imagined it, loudly.
[portrait: ILSA, neutral] Ilsa Marr. Provost. Warden of the Mind Plate, which is upstairs, upside down.
[name: Ilsa] My gym's through that door. Do it quickly. I have a trial to host, and you have something in you I'd like to look at afterwards, if you'll let me.
[portrait: ILSA, sad] (quietly, putting her earmuffs straight) Someone sealed a memory in you. A long time ago.
[name: Ilsa] I can hear the seal. It's very well made.
V134 = 4. The gym opens.
```
*(15_COMEDY Ch13 "Thinking Loudly": one option, as written; the three thoughts are the menu. Before the blow.)*

## Maps 350–354 (356) — the Lucent gym (Gym 12; GYM_PUZZLES Gym 12, kept short)
Doors open at V134 >= 4. As GYM_PUZZLES Gym 12 ("your reflection keeps you honest"): 350 the Reading Room (teach), 351 the Mirror Hall (twist), 352 the Swap Atrium (combine), 354 the Warden Arena. **353 is cut from the critical path** (density: CHAPTER_BEATS); 356 the Quiet Room (Mastery) stays optional.
- In 351, the reflection pane: the PC's reflection is the gym's own mechanic here, and for once it is exactly on time. A scholar: "Yours keeps up. Some people's don't, out here."

### 354 — the Warden Arena: Ilsa
```
(A round room with no corners. The walls are mirrors. In every one, the room is slightly different.)
[portrait: ILSA, neutral] The arena reshapes itself to what you remember.
[name: Ilsa] I don't choose what it shows. You do.
[name: Ilsa] The truth is a weapon. I've kept it sheathed for ten years.
[name: Ilsa] Don't mistake that for mercy. Shall we?
BATTLE: Prismfall.gym_battle(pfm_gym(:LEADER_ILSA), double: false) — field `:MINDSCAPE` (Topsy-Turvy → Inverse); Mega Slowbro under Trick Room.
(Mid-battle, when the field turns:) [portrait: ILSA, shocked] (her earmuffs slipping) That's— that's not a place I put there. That's yours. Where is that?
(Her last Pokémon, Hatterene "Hush":) [portrait: ILSA, neutral] Hush. They're loud. Quiet them.
(WIN:)
[portrait: ILSA, neutral] ...Quiet, for once.
[name: Ilsa] Your thoughts were very loud. I liked them.
[name: Ilsa] The CANDOUR BADGE. It means you can't lie to Lucent.
[name: Ilsa] Nobody can; the badge just admits it.
RECEIVE: CANDOUR BADGE. RECEIVE: TM29 PSYCHIC.
[portrait: ILSA, sad] Now. The seal.
[name: Ilsa] Come to the Reading Hall when you're ready. I won't enjoy it.
V134 = 5.
```
*(**Badge name (proposed):** the **Candour Badge**. The mid-battle line uses the Mindscape field's arena change: the place she can't place is Crownhaven's Lower Town (the Mindscape's map), seeded here.)*

## The Mindscape (key event 1; the Reading Hall → the Mindscape [NEW]; touch Ilsa with V134 == 5 → 6)
```
[portrait: ILSA, neutral] Sit. Close your eyes. I'll be there.
[name: Ilsa] You won't see me. You'll feel me, like a hand on the back of a chair.
[portrait: ILSA, sad] It was a Ghost-type that sealed it. I can feel the shape of the curtain.
[name: Ilsa] Whoever asked it to do that loved you very much and was very frightened.
Script: Prismfall.checkpoint
(White.)
```
```
(Bells. A town of narrow streets under a great white wall, hung with Festival banners in eighteen colours. Lower Crownhaven, AF 290. Everything is a little too bright, like a memory of a summer.)
(The people in the streets are blurred, like figures behind frosted glass. Only one thing is sharp: a child of five on the steps of a chapel, in a coat too big for them, holding a Choir ribbon in both hands.)
(The child looks up at you. They have your face. They're not surprised.)
CHILD: Mum's singing. Do you want to see the light?
CHILD: It's going to hurt.
```
```
> "Show me." (show)
  Script: pf_choose(:ch13_remember, :show)
  [portrait: PLAYER, neutral] Show me.
  CHILD: Okay. Hold my hand. Not too tight.
> "I'm scared too." (scared)
  Script: pf_choose(:ch13_remember, :scared)
  [portrait: PLAYER, sad] I'm scared too.
  CHILD: (taking your hand anyway) I know. That's why I waited for you.
> "...Not yet." (not_yet)
  Script: pf_choose(:ch13_remember, :not_yet)
  [portrait: PLAYER, sad] ...Not yet.
  CHILD: (nodding, very seriously) Okay. I'll keep it. It's heavy, though. Don't leave it too long.
  (The child sits back down on the step with the ribbon. The bells go quiet. White.)
```
*(The first authored PC dialogue (06_ACT_III). NARRATIVE_KEYS §4.2: `:show` ILSA+1 RES+1, `:scared` ILSA+2 RES+2, `:not_yet` ILSA+1, and the memory plays in the Ch15 Cathedral echo instead, harder.)*
```
[if :ch13_remember != :not_yet]
  (The chapel. Inside, a choir in white on a high loft, singing one long note in eighteen voices. In the front row a woman with your eyes, singing with her whole body. Ines.)
  (Below the loft, a white-robed man with a crown on his head. The Crown blazes: eighteen colours and one clear stone in the middle. Valen, younger, upright, holding up the sky.)
  (Behind the choir loft, in the shadow, where nobody in the congregation can see: brass machines. Dials, pipes, cables running into the floor. On each machine, a small gold plate: a sunburst.)
  (The note goes higher. The machines hum louder. The child's hand is hot in yours.)
  SE: a crack, like ice on a lake, but inside your head.
  (The clear stone in the Crown splits. Light comes out of it, all at once, white, everywhere.)
  (Something comes out of the light, small and sharp and very fast, and goes into the child's chest.)
  (Pain. Yours. Theirs. The same.)
  (A woman in black, with a Ghost Warden's veil over her face, throws herself over the child, over you, and the light breaks on her back like water on a rock.)
  VOICE (a man's, through the light, very calm): Find the child.
  (Darkness. And in the darkness, the shape of a Mismagius, drawing something closed over all of it, slowly, like a curtain.)
  (White.)
Switch S135 CH13_MINDSCAPE_DONE = ON. V134 = 6.
```
*(09 #9: the brass machines with sunburst plates are Meridian's array (Ch15 echo confirms). #10: the veiled woman is Morwen. #1: the thing that went into the child is the Legend Plate splinter. The calm voice is Valen's.)*
```
(The Reading Hall. You're in the chair. Ilsa is on the floor beside it, her earmuffs off, in her hands. She's white.)
[portrait: ILSA, sad] [emote: dots] (very quietly) The man in white was my father.
[name: Ilsa] I've known for ten years.
[name: Ilsa] I read it out of him at my mother's funeral, the winter after the Glassfall.
[name: Ilsa] I was twenty-one. I never said a word.
[portrait: ILSA, neutral] The truth is a weapon. I've kept it sheathed.
[name: Ilsa] Don't mistake that for mercy.
[name: Ilsa] (putting the earmuffs back on) The trial's in the morning.
[name: Ilsa] He'll be sitting at the top of the court in that white coat, presiding. And I'll be sitting next to him, and I'll be hosting it, and neither of us will say anything at all. That's the family business.
[if :ch13_remember == :not_yet]
  [portrait: ILSA, neutral] You said "not yet". That's allowed.
  [name: Ilsa] Not everybody's ready to be five again.
  [name: Ilsa] I'll keep the door. It'll open by itself one day, somewhere worse.
  [portrait: ILSA, sad] I'm sorry about that.
```
*(09 #17: Ilsa is Valen's daughter; she says it here. This seeds "Little Owl" (Act V).)*

## The Athenaeum cloister garden: **"Veil"** (Juno and the Ralts; autorun on leaving 344 at night, V134 == 6 → 7)
```
(The cloister garden at night. Juno sits on the rim of a reflecting pool with a speech in her lap she isn't reading. Her blossom veil trails in the water. Something in the veil is trembling.)
[portrait: JUNO, sad] Don't. I know. I look like a wedding that got lost.
[name: Juno] He's in a cell under this building.
[name: Juno] Tomorrow I sit in the Wardens' row and listen to them decide what he is.
[name: Juno] I've written this speech eleven times. It says "uncle" in all of them.
(The veil moves. A small white Pokémon with a green bowl of hair peers out of the blossoms: a Ralts, its red horn glowing faintly.)
[portrait: JUNO, shocked] [emote: question] ...Oh. Hello. How long have you been in there?
[portrait: JUNO, happy] Since the Threshold, I think.
[name: Juno] Ilsa says Ralts can feel what you feel. So it's had a horrible week.
[name: Juno] Everyone stares at the veil. Nobody looks inside it.
[name: Juno] That's actually very clever of you.
[portrait: JUNO, neutral] They feel it when you're frightened, and they come closer instead of running away. That's backwards. I like it.
> It's picked you.
  [portrait: JUNO, happy] Has it? ...Then you're Veil.
  [name: Juno] I name things after where they hide. It's a system.
> (Say nothing.)
  [portrait: JUNO, happy] You're right, it's not my decision.
  [name: Juno] ...Veil? Do you want to be Veil?
  [name: Juno] It's nodding. Or shivering. I'm counting it.
[portrait: JUNO, sad] Uncle Rowan's ring still won't talk to me.
[name: Juno] Maybe it's waiting for me to stop being scared.
[name: Juno] Maybe Veil can teach me how.
[if JUNO_ESTRANGED]
  (Juno sees you at the cloister door. She doesn't wave you over. She talks to the Ralts instead, too quietly to hear, and after a while you go.)
V134 = 7.
```
*(06_ACT_III's scene, as written. Gardevoir "Veil" replaces Comfey on Juno's team from J4; Rowan's ring answers her through it at the Festival (MEGA_EVOLUTION §1.2).)*
**Also tonight (optional):** Vesper of the Eevee Octave in the cloister's other walk: the second meeting, an optional sparring double (EEVEE_OCTAVE), the singers' letters, and Lento's silence if The Still Water isn't done. **WICK'S LETTER** (if carried from Ch10's Hollow Sanctuary): the jailer at the undercroft stair takes it. "From Brother Wick? ...I'll see he gets it. I'll read it first. I'm not a monster; I'm a jailer." Rowan's line in the dock tomorrow changes (below).
**Kaito, in the cloister's colonnade** (touch, before sleeping) → **CHOICE `:ch13_kaito`**:
```
[portrait: KAITO, neutral] You. Sit.
[name: Kaito] Tomorrow they'll ask the Wardens if anyone has anything to add.
[name: Kaito] Usually nobody does.
[name: Kaito] [emote: dots] Fifteen years ago I did something on the Sovereign's order.
[name: Kaito] Nobody knows. My Lucario knows. He could feel them.
[name: Kaito] I could say it. In the court. With him sitting there.
[name: Kaito] It would end things. It might end me.
[name: Kaito] You don't owe me an answer. I'm asking anyway. Should I?
> Say it. (encourage)
  Script: pf_choose(:ch13_kaito, :encourage)
  [portrait: KAITO, neutral] ...Right.
  (He stands.)
  [name: Kaito] A fist is a promise. Don't make one you won't keep.
> It isn't yours to carry alone. Not tomorrow. (spare)
  Script: pf_choose(:ch13_kaito, :spare)
  [portrait: KAITO, neutral] (after a long time) ...Maybe. Maybe not tomorrow.
  (He doesn't look relieved. He looks like a man putting something heavy back on his shoulders.)
```
*(NARRATIVE_KEYS §4.2 `:ch13_kaito`: `:encourage` ACCORD−2 VALEN−2 ILSA+2 HOLLOW+1, `KAITO_TESTIFIED`; `:spare` ACCORD+1 VALEN+1. 09 #27: Marrowgate and the Quiet Towns.)*

---

## The Glass Court [NEW; the Athenaeum, off 343]: **the tribunal** (key event 2; autorun on waking at 341 with V134 == 7 → 8)
```
(The Glass Court: a round chamber under a dome of clear glass, with the upside-down city hanging in the sky beyond it. Tiers of benches. At the top, on a white chair, Valen, in his white coat with one glove on. Beside him, lower, Ilsa, earmuffs on, hosting.)
(The Wardens' row: Juno with a Ralts in her veil, Kaito with his wraps on, Celestine smiling at nothing, others. The kings' gallery: two thrones empty, Isenmar's and Ashkaar's, with junior observers at the back rail behind them; the Ossarian's full. Meridian's lawyers. The press. Hierophant Ellery of the Prism Choir, in white and gold, with a row of white-robed Accord choristers behind her.)
(In the dock, in chains, a gaunt man with a grey-shot beard. His right hand is wrapped, and where the wrapping ends the skin is marked with a branching pattern like lightning. Rowan Ashby.)
Variable V113 ROWAN_STATUS = 2.
[name: Clerk of the Court] The Accord's tribunal is in session.
[name: Clerk of the Court] The Sovereign presides. The Provost of Lucent hosts.
[name: Clerk of the Court] Witnesses will swear.
[portrait: CELESTINE, happy] (when the clerk comes to her) I can't lie anyway. It'd be rude to pretend.
[portrait: VALEN, neutral] Rowan Ashby. Warden of the Meadow Plate.
[name: Valen] You stand accused of the masked attacks on the Saltmere Pageant, the Ironreach Conclave and the Accord's peace.
[name: Valen] Have you anything to say?
[portrait: ROWAN, neutral] (standing as far as the chain lets him) I wanted to pull the nails.
[name: Rowan] I was wrong about how.
[name: Rowan] I was not wrong about why.
[if WICK'S LETTER was delivered] [portrait: ROWAN, sad] (to the Wardens' row, quieter) Wick says the faithful are fed. Tell him I read it. Tell him twice.
(Juno doesn't look at him. Her hands are white on the speech in her lap.)
```
### Kaito's testimony (only if `:ch13_kaito == :encourage`)
```
[name: Clerk of the Court] Does any Warden wish to add to the record?
(Silence. Then Kaito stands.)
[portrait: KAITO, neutral] Marrowgate. Fifteen years ago. My orders. My unit.
[name: Kaito] I sealed the gate. They were still knocking.
[name: Kaito] (looking up at the white chair) On the Sovereign's order.
(Nobody speaks. Valen doesn't deny it. He looks at Kaito for a long moment, and then down at his gloved hand.)
(Then the kings' gallery erupts: the Thane's observer on his feet, the Dominar's envoy laughing, the Ossarian writing very fast.)
[name: Clerk of the Court] [emote: exclaim] ORDER—
```
*(`KAITO_TESTIFIED`: the Accord's moral authority cracks; Kaito becomes the Wardens' conscience (Act V).)*
### The PC's testimony → **CHOICE `:ch13_rowan_testimony`**
```
[name: Clerk of the Court] The court calls the Unimprinted witness.
[name: Clerk of the Court] You were at the Saltmere Pageant. At Ironreach, in the Pit.
[name: Clerk of the Court] You saw the mask break. Tell the court what this man is.
(Juno looks at you for the first time today.)
> Condemn him. (condemn)
  Script: pf_choose(:ch13_rowan_testimony, :condemn)
  (You tell them about the Pageant's panic, the Conclave's dead, the glass at Ironreach. All of it true.)
  [portrait: VALEN, neutral] The Pale Gaol. For the rest of his natural life.
  [name: Valen] The court will seal the sentence at the evening session.
  (Juno stands up in the Wardens' row and walks out of the court without a word. The Ralts in her veil looks back at you over her shoulder.)
> Plead for mercy. (mercy)
  Script: pf_choose(:ch13_rowan_testimony, :mercy)
  (You tell them about Phantump at Tidewatch Station, about the mask cracking because he put himself between a child and the glass, about "everything that grows must be allowed to die".)
  [portrait: VALEN, neutral] (after a long pause, and a look at Ilsa, who gives nothing back) House arrest. In Verdance.
  [name: Valen] In the custody of the Warden of the Meadow Plate.
  [name: Valen] To be sealed at the evening session.
  (in the Wardens' row, both hands over her mouth)
> Refuse to testify. (refuse)
  Script: pf_choose(:ch13_rowan_testimony, :refuse)
  (You say you won't. The clerk asks twice. You say it twice.)
  [portrait: VALEN, neutral] The court notes the witness's silence.
  (A pause.)
  [name: Valen] Sentence will be pronounced at the evening session.
  (Juno never asks you why. Not today, not ever.)
```
*(NARRATIVE_KEYS §4.2 `:ch13_rowan_testimony`: `:condemn` ROWAN−4 JUNO−3 ACCORD+2 HOLLOW−2 VALEN+1; `:mercy` ROWAN+3 JUNO+3 HOLLOW+2 ACCORD−1 (the only route to R16 Rowan; he never serves the house arrest because of the Fault); `:refuse` ROWAN−1 ILSA+1.)*
### **Sable unmasked** (with `IRONREACH_EVIDENCE`: the PC holds the COMM-DEVICE)
```
[if IRONREACH_EVIDENCE]
  [name: Clerk of the Court] Has the witness any further evidence for the record?
  (You put the comm-device on the rail. The brass radio-box from the Ironreach Pit, with MERIDIAN SPECIAL ACCOUNTS under its sunburst. Beside it, the Splitter casing from Skyreach.)
  (Ilsa takes her earmuffs off. The whole court goes quiet, the way a room goes quiet when someone opens a window in winter.)
  [portrait: ILSA, neutral] (not loudly; everybody hears it) Someone in this room recognises that box.
  [name: Ilsa] Someone in the public gallery. Third row. Grey hat.
  [portrait: ILSA, angry] Sable is Sabine Kroll. Meridian Special Accounts.
  [name: Ilsa] She cracked Lumen's Plate. She set the Ironreach charges.
  [name: Ilsa] She bombed Skyreach. On orders.
  (Uproar. In the third row of the public gallery, a woman in a grey hat stands up, takes it off, and shakes out her hair. She is smiling.)
  [portrait: KROLL, happy] Light for everyone, right?
  [name: Kroll] ...Oh, never mind. You're no fun any more, Provost.
  (She vaults the rail into the well of the court. Accord guards go for her. A Sharpedo comes out of a ball between them.)
  BATTLE: TrainerBattle.start(:MERIDIAN_KROLL, "Sabine") — single; the Glass Court (`:MINDSCAPE`); her Mega Sharpedo (a Lattice band at her wrist).
  (LOSE: whiteout to 341; the court restarts at the evidence, the testimony kept.)
  (WIN:)
  [portrait: KROLL, smug] (as the guards close in) Inquiry. There'll be an inquiry. You'll see.
  (A smoke pellet. When it clears, there's a broken window high in the dome and a grey hat on the floor.)
[if !IRONREACH_EVIDENCE]
  (You put the Splitter casing on the rail. It's circumstantial. The Meridian lawyers say so, at length.)
  (Later, in a corridor, Ilsa stops you with a hand on your sleeve, her earmuffs off.)
  [portrait: ILSA, neutral] (very low) The woman in the grey hat, third row.
  [name: Ilsa] Sable. Sabine Kroll, Meridian. I read it straight out of her.
  [name: Ilsa] And I can't say it in there, because a Provost's reading isn't evidence without something to hang it on.
  [name: Ilsa] Keep that casing. Somebody will believe it, one day.
```
*(09 #12 and #13. Without the COMM-DEVICE, Kroll stays hidden; the public learns in Act IV through Rook's leak and believes it less. The casing still lets the PC turn Marchetti in Ch14 (`:ch14_marchetti`).)*
### Voss on every screen (the hour after; the Tribunal Ward's screens)
```
SCREEN: [portrait: VOSS, sad] If any Meridian contractor acted outside the law, they acted alone. I am appalled. I've ordered a full inquiry. The Fellowship will cooperate in every way.
SCREEN: (a ticker under him) MERIDIAN APPROVAL +4 · "DIRECTOR'S CANDOUR PRAISED"
Switch S136 CH13_TRIBUNAL_DONE = ON. V134 = 8.
```

## **The Fault** (key event 2, payoff; autorun at the evening session, V134 == 8 → 9)
```
(The evening session. Rowan back in the dock. Valen in the white chair, the seal in his gloved hand, about to speak.)
(The water in the court's carafes shivers. Then the benches. Then the floor.)
(Far away, under everything, something starts. A hum, low and enormous, like eighteen notes played at once by somebody who doesn't know music.)
(Under your collar, the colourless scar burns so hot it hurts, and you put your hand over it.)
SCREEN SHAKE (long).
(The dome's glass cracks, in one long line, then a hundred, and comes down in a slow, glittering rain.)
(The floor of the Glass Court tilts, and the middle of it goes, into the dark undercroft below, and the water comes up through it, black and fast.)
Script: Prismfall.checkpoint
```
*(Under Cogsworth, Meridian test-fires the Arbiter Engine's first core: the Dark Stone, drawing on all eighteen Plates at once (06; 09 #15 "the Fault (test-fire)"). The tremor runs through every Imprint.)*
```
(The undercroft: the court's broken floor in a black pool, rising. Lamps swinging.)
(On one side, the dock, half under water. Rowan, still chained to its rail, the water at his chest, pulling at the chain with his good hand.)
(On the other side, the court's great brass orrery has come down, ring and all. Under the ring, pinned at the waist, Director Marchetti, conscious, grey-faced, her Manectric barking at the brass.)
(Across the water, on the far stair, Brother Wick and three Hollow faithful, shouting for Rowan. Too far.)
(You can reach one. The water's still rising.)
```
```
> Break Rowan's chain. (rowan)
  Script: pf_choose(:ch13_fault, :rowan)
  (Your Pokémon at the chain, all of them, and it gives. Rowan comes up out of the water gasping. Wick's people reach out from the stair and pull him across.)
  (Behind you, Directorate troops in the doorway hauling the brass ring up, together, too slowly. When they get Marchetti out she can't stand. She looks at you once, across the water. Nothing in her face at all.)
  (Rowan, on the far stair, soaked, before Wick's people pull him away into the dark of the undercroft tunnels:)
  [portrait: ROWAN, neutral] Ask the Drowned Crown.
  [name: Rowan] It's awake now. So are you.
  Variable V113 ROWAN_STATUS = 3 (escaped / Lantern Hollow).
> Heave the ring off Marchetti. (marchetti)
  Script: pf_choose(:ch13_fault, :marchetti)
  (You and your Pokémon get under the brass ring, and push, and it lifts a foot, and Marchetti drags herself out from under it on her elbows.)
  (When you turn round, the dock is under water. All of it. The chain is still taut.)
  (Wick's people go in after him. It takes them a long time. When they bring him up the stair, he isn't moving.)
  (Juno comes down the broken steps from the court, and sees, and stops.)
  [portrait: JUNO, crying] (not loudly) Uncle Rowan.
  [portrait: MARCHETTI, neutral] [emote: dots] (on the floor, bleeding, to you, only) I owe you a life.
  Variable V113 ROWAN_STATUS = 6 (drowned in the Fault).
Switch S137 CH13_FAULT = ON. V134 = 9.
```
*(NARRATIVE_KEYS §4.2 `:ch13_fault` (MAJOR): `:rowan` ROWAN+3 JUNO+2 HOLLOW+1, `ROWAN_ALIVE`, Marchetti maimed and unturned; `:marchetti` JUNO−4 HOLLOW−2 MERIDIAN+1, `MARCHETTI_TURNED` (she stands the Directorate down at the hijack). Knock-ons if Rowan drowns (06): Teo leads the Lantern Hollow if `TEO_SAVED`, else Thistle and Wick; "The Gardener" can't be drawn at R16; Juno holds Elin alone in Homecoming. V113: 2 during the tribunal, then 3 (escaped) or 6 (drowned; a value added to FLAGS with this script).)*
**What the Fault did** (shown in the next morning's screens and NPC lines; S137's map states):
- The Bleed leaped forward in every Imprint: from Act IV every early map uses encounter version 1 (Bleed-spread).
- On the south coast, the sea pulled back from Zenith's cliffs overnight. The Sump drained, and the spires of drowned Aurelia stand naked under Underveil for the first time in three hundred years.
- A Lucent scholar on the Athenaeum steps: "Every needle in the seismograph room broke at once. All eighteen. Like something pulled on every Plate in the world at the same moment."
- Vesper of the Octave (if met), shaking: "The Choir says we were born lucky. I don't feel lucky."

## Map 748 — the Shattered Sky (optional; `:BLEED`, from V134 >= 9)
The Speculum, Lucent's upside-down city in the sky, has cracked: pieces of it hang between earth and sky, and a stair of broken colonnade leads up into them. The PC can walk among the fragments (Bleed wilds) and find the first **Zygarde Core** at the top (the Zygarde Cell quest hook). A fragment of the reflected Athenaeum has the Glass Court's dome in it, whole, with tiny figures still sitting in it, upside down, waiting for a verdict.

## The Athenaeum steps: **"Father's Secret Articles"** (Chapter 13 close, END OF ACT III; autorun at dawn on 340, V134 == 9 → 10)
```
(Dawn. The Athenaeum steps, covered in broken glass. The upside-down city in the sky has a crack across it like a broken plate. Somewhere, a bell that isn't ringing for anything.)
(Ilsa comes down the steps with her earmuffs round her neck and her robes torn at the hem. She has an envelope: thick, sealed with the Sovereign's own seal, the wax not yet cracked.)
[portrait: ILSA, neutral] Father's Secret Articles.
[name: Ilsa] The parts of the Concordance the Accord doesn't teach.
[name: Ilsa] I took them out of his desk at four this morning while he was looking at the sky.
[name: Ilsa] Don't read them yet. Go and find Bastian Ore first.
[name: Ilsa] Cragholm, in the Bone Sands. He was *there*. In AF 290.
[name: Ilsa] He'll tell you what the Articles don't.
RECEIVE: SECRET ARTICLES (sealed).
[portrait: ILSA, sad] [emote: dots] (turning back to the doors) I'm going to go and sit with my father now.
[name: Ilsa] Neither of us will say anything at all.
(She goes in. You're alone on the steps.)
(In every broken pane of glass around you, on every step, hundreds of tiny reflections of the morning, and in every one of them, at the edge, six black wings fold, and unfold, and fold.)
TITLE CARD: END OF ACT III.
V134 = 10. Variable V101 STORY_ACT = 4. V102 STORY_CHAPTER = 14.
CHAPTER CARD: Chapter 14, "The Deep Seams" (it names ACT IV · THE DROWNED CROWN; plays when V102 is set; Cutscenes 020).
QUEST LOG: "Eighteen Roads" — Through the Grave Glass at Vigil, north to Cragholm in the Bone Sands. Find Bastian Ore, the oldest Warden. He was there.
```
*(06_ACT_III's cliffhanger and END OF ACT III. 09 #5: the Secret Articles ("One in Keeping") are read in Act IV. #25: the six wings are Giratina (Ch15).)*

---

## Map events needed (Chapter 13)

None of these maps is built. **[NEW]** = an event or map not in maps.json. V134 = **CH13_STEP** (design/FLAGS.md). Maps go through the three-pass workflow (design/MAPGEN.md, top).

**740 Conductors' Causeway** — road sign, the lineman on the pylon ladder, puddles (decor reflections), trainers.
**741 The Wired Wood / 750–751 Verdigris** — pylon-trees (decor), the retired lineman (cake line), the Circular at 751 (Juno's post, Kaito's reply), trainers.
**602 Candle Down · 603 the Highwold · 756 Kingsmead** — the Crown Road; **756 the Scar autorun** at the paddock gate (V134 0 → 1): the paddock keeper; the Crownwall's north-west face with the glittering Scar (a large overlay/panorama), the PC's scar ache (a screen pulse).
**752 Looking-Glass Wood / 753–754 Glassmere** — mirror-bark birches; doubling paths; Glassmere's child; The Still Water's start (Lento; EEVEE_OCTAVE).
**742 Mirror Mere** — the still lake (reflection overlay showing Lucent on the far shore); the stone landing; **Dask** with the lantern (autorun V134 1 → 2); the walk onto the water (passable water tiles from V134 >= 2).
**743 Antumbra Threshold** (`:INVERSE`) — uphill river (animated tiles reversed), shadows toward lamps; the mirror-writing signpost (readable only via its reflection event); six-winged shadow events at reflections (appear only when the PC isn't facing them: a check on player direction); **the voice autorun** two-thirds across (GO_LOOKING_BACK; S134, V134 = 3).
**755 Widdershins Walk** — colonnade, two walking lanes of NPCs (looping move routes, opposite directions).
**340–345 Lucent** — the Speculum overhead (sky panorama, upside-down city; cracked after S137); 340 the Athenaeum Quarter and its steps (the dawn autorun, V134 9 → 10); 341 PC (sleep triggers: tribunal morning V134 == 7; the Circular); 342 Mart; **343 Tribunal Ward** (crowds, coaches, guards, the pamphlet hawker; screens: Voss's statement after V134 >= 8; the Fault's morning headlines after S137); **344 Great Reading Hall** ("Thinking Loudly", V134 3 → 4; the Mindscape trigger at the chair, V134 == 5); 345 Sealed Stacks (flavour); **the cloister garden** (on 344's edge or its own small map): Juno at the reflecting pool ("Veil", V134 6 → 7), Vesper (optional double), Kaito in the colonnade (`:ch13_kaito`), the undercroft jailer (WICK'S LETTER).
**The Glass Court [NEW]** (the Athenaeum's tribunal chamber, ~29×25): the dome, tiers, Valen's white chair and Ilsa's seat, the Wardens' row (Juno + Ralts, Kaito, Celestine, 2 more), the kings' gallery (two empty chairs, the Ossarian, the envoys), Ellery and eight Octave singers, the press, Meridian's lawyers, the public gallery's third row (Kroll in a grey hat); the dock with Rowan; the clerk. The tribunal autorun (V134 7 → 8), the testimony branches, the Kroll battle and her escape (a broken pane high in the dome), **the Fault** (V134 8 → 9): the dome breaking (picture/flash), the floor dropping (a map swap to the undercroft state).
**The Glass Court undercroft [NEW]** (the court's flooded state, ~21×17): the black pool, the dock half-submerged with Rowan chained, the fallen orrery ring with Marchetti under it and her Manectric, Wick and three faithful on the far stair; `:ch13_fault`; V113.
**The Mindscape [NEW]** (Lower Crownhaven, AF 290; ~29×25, `:MINDSCAPE`, an over-bright tint): banners, blurred townsfolk (transparent NPCs), the chapel steps with **the child** (a small PC-alike sprite with a ribbon), the chapel interior (choir loft with Ines and the Choir, Valen with the blazing Crown, **brass machines with sunburst plates** behind the loft, the crack and the light as a picture sequence, the veiled woman, the Mismagius curtain).
**350–352, 354, 356 Lucent gym (Gym 12)** — as GYM_PUZZLES Gym 12; **353 off the critical path** (density); Ilsa (354), single; CANDOUR BADGE, TM29; V134 = 5.
**748 The Shattered Sky** (optional, from V134 >= 9) — floating fragments, the colonnade stair, Bleed wilds, the first Zygarde Core, the upside-down Glass Court fragment (decor).

**Trainer designer:** none new (Ilsa, Kroll Ch13, Vesper's sparring double are in PBS or EEVEE_OCTAVE). **Items owner:** SECRET ARTICLES (sealed Key Item; read in Act IV). **Badge name (proposed):** the **Candour Badge**.
