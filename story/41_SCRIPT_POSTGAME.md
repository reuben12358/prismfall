# Script: Post-Game — "Fallmorn" (the morning after; the Registry; the lighthouse; Zygarde; the Spire and the Gauntlet; the legendary network; the Distortion Core; Concord Zero)

> **The post-game's story script.** It's the frame and the key scenes. The quest mechanics, levels and capture rules come from **Gemini's Part B network** (`gemini_recommends/2026-11-23_gen6-9-sprites-postgame-legendaries-dorian-meloetta`, adopted in REVIEW.md), with the continuity fixes listed at the end. Scope by ending is NS §6.5: **full**, **partial** (Hollow Spring and Concord Dawn: the Spire plus Tier 1 only) or **none** (the Gilded Chain).
> **Follows** the ending (`story/40_SCRIPT_CH21.md`).
> **Sources:**
> - Story: 08_ACT_V POST-GAME HOOKS; 12_RUIN_ROUTE (Ruin aftermath, where Arceus doesn't return); 03_CAST (Hesper, Larch, Dorian, Juno, Kaito, Corvin, Mother Gutter, Quent, Calla, Ysolde, Sahar, Dask, Ilsa).
> - Design: `design/CAMEOS.md` (Lin and the superbosses); `design/POKEMON_AVAILABILITY.md` §4 (every legendary capture happens here); FLAGS S160 and S261–S300.

## Conventions
As in the earlier scripts.

**The capture rule:** every post-game legendary is a `Prismfall::Bosses` fight. Each has 2–3 bars (3–4 on Hard) and `:catch => :last_bar`: the player breaks the shields before Poké Balls work. **Gifts** (Type: Null, Kubfu) are given after a trial.

**Counter:** V143 **PG_STEP** (new; design/FLAGS.md):
- 0: the morning after
- 1: the Registry opens (S270)
- 2: the lighthouse
- 3: Valen's memorial
- 4: the Spire and Gauntlet tour
- 5: Concord Zero begins (S269)

The quest flags follow Gemini's allocation:

| Flags | Meaning |
|---|---|
| S270 | PG_LEGENDS_BOARD_OPEN |
| S271–S278 | Tier 1 clears |
| S279 | PG_TIER2_RIFTS_OPEN |
| S280–S284 | Tier 2 clears |
| S285 | PG_TIER3_APEX_OPEN |
| S286–S293 | Tier 3 clears |
| S294 | PG_ARCEUS_CONVERGENCE_DONE |

These are registered in FLAGS.md with this script.

---

## P0. The morning after (autorun on the first map load after credits; S262 → V143 = 0)
The PC wakes in the room above Pilgrim's Rest, where they slept on the eve of the Final. The world state comes from the ending (S263 Homecoming / S264 Vigil and Borrowed / S265 Ruin).
```
[if S263 PG_HOMECOMING_WORLD]
  (Morning. Through the window, Crownhaven, and above it, for the first time you can remember, a plain blue sky. No ripple. No colour at the edges.)
  (On the windowsill, someone has left a cup of tea. It's the good tea. There's a note under it in Larch's hand: "Registry. Spire lobby. When you've slept. — I.L.")
[if S264 PG_VIGIL_WORLD]
  (Morning. The sky over Crownhaven ripples, very faintly, the way it always has. Quieter than before. The Plates sleep.)
  [if :ch21_final == :keep] (Your hand, on the blanket. Nothing yet. You check it anyway.)
  (A note under a cup: "Registry. Spire lobby. When you've slept. — I.L.")
[if S265 PG_RUIN_WORLD]
  → 12_RUIN_ROUTE's aftermath frame. The Registry opens via the Mirrorwalk Rifts; Arceus never returns (Gemini B.3 "Ending Compatibility").
V143 = 0.
```

## P1. Larch's Postgame Registry (the Concordance Spire lobby; touch, Larch, V143 == 0 → 1)
```
(The Concordance Spire's lobby, finished at last, gold and glass, quieter than the arena. A board on an easel covered in pinned notes, eighteen columns, one per kingdom. Larch in front of it with a mug.)
[portrait: LARCH, happy] There you are. Sit. No, don't sit, look. Every Warden sent me something. Rumours. Sightings. Things that woke up when the sky closed and didn't go back to sleep.
[portrait: LARCH, neutral] The old ones. The legends. They're not bound any more. They're not *anyone's*. Some of them want to be found. Some want to be fought. One or two want to be left alone, and I've marked those in red. Respect the red.
[portrait: LARCH, smug] I'm calling it the Registry. Dorian wanted "The Grand Tour". We compromised: I won.
Switch S270 PG_LEGENDS_BOARD_OPEN = ON. V143 = 1.
```
**The Registry board** (a `Prismfall::Trials` category, `:POSTGAME`; Gemini Part B.3). Each card is a quest. The tiers:
- **Tier 1** (Lv 82–90; open at once): the eight chains below.
- **Tier 2** (Lv 90–95): opens at 4 Tier-1 clears plus S268.
- **Tier 3** (Lv 95–100): opens at the Tier-2 keystones plus S267.

### Tier 1: Regional Trials and Mythical Encores (the story beat for each card; mechanics per Gemini)
| Card | Giver and opening line | Notes |
|---|---|---|
| **T1-1 Crownhaven Encore** (`PG_MELOETTA`, S271) | Dorian's gold playbill: "*She held back in Act One so you could shine, darling. Opening Night is hers.*" | The Encore at the Crownhaven Opera Hall: Dorian's Lv 90 troupe, then Meloetta, 2 bars, on Grand Stage at Standing Ovation. At the end: "Take her on tour, darling. The whole world is a stage now." |
| **T1-2 The Masks of Gloamwood** (`PG_OGERPON`, S272) | Juno at the Bride Tree: "They've been standing at the border stones for three hundred years being ashamed. Somebody should tell them it's over." | The Loyal Three, then Ogerpon across all four masks. It **joins the PC here at last**: the only way it ever becomes party. If `:ch10_ogre == :hesitate`, Juno's reconciliation beat plays first. |
| **T1-3 The Bitter Mochi Seal** (`PG_PECHARUNT`, S273) | **Corvin** (if `CORVIN_FREED`) or **Mother Gutter**: a Sweetrot echo under the Moon Market. *Not Wenlow: Wenlow died in Interlude IV; his notes are the lead.* | Larch's kelp tea (running gag 1) breaks the dormant shell. |
| **T1-4 The Stonesleep Braille** (`PG_REGIS`, S274) | Sahar: "The braille under Stonesleep. I read it the day the sky closed. It's an *invitation*." | The Regi chain across Ossaria, Isenmar and Zenith, ending with Regigigas in the Aurelia Ruin Vault. |
| **T1-5 The Three Mirror Lakes** (`PG_LAKES`, S275) | Dask and Ilsa: "Three ripples. Knowledge, Emotion, Will. Lucent, Rime, Sallow." | Uxie, Mesprit, Azelf. |
| **T1-6 Project NULL, Unmasked** (`PG_TYPENULL`, S276) | Opened by the **NULL CRADLE KEY** (Ch10 `:take`), or by Calla (`CALLA_ALIVE`) on any route: "I know the Black Site's codes. I wrote half of them." | Kestrel helps if he's alive and not `KESTREL_LOST`. Quent's automated security, then **Type: Null** (the gift, finally; it remembers the PC's badge case), the 17 Memories, and Genesect. |
| **T1-7 The Pit-Dojo Scrolls** (`PG_KUBFU`, S277) | Kaito: "Five rounds. No items. You're the Champion; you can afford to lose." | Kubfu plus both scroll towers. |
| **T1-8 Roamers, Guardians and Encores** (`PG_ROAMERS`, S278) | Each Warden's pinned rumour on the board, one legend or mythical tied to their kingdom. | The Birds, Beasts, Lati@s, Heatran, Cresselia and Darkrai, Swords, Forces, and the mythical vignettes (per Gemini's list). |

### Tier 2: Bleed Rifts and Ruin Anomalies (story beats)
| Card | Story beat |
|---|---|
| **T2-1 The Eleven Bleed Rifts** (`PG_UBS`) | Giratina's wound (Ch15) is still open. The rifts are where other worlds leak through. Ysolde: "The Glass is mending. Slowly. Things are getting through while it does." |
| **T2-2 Guardians of the Shardfall** (`PG_TAPUS`) | Shardfall Isles (905): the quarantine's first islands. Edda's ferry runs there now. |
| **T2-3 The Four Cursed Stakes of Aurelius** (`PG_RUIN_QUARTET`) | The Gilded King's four curses, buried in four kingdoms' shrines. Sahar and Celestine. |
| **T2-4 Prism Echoes** (`PG_PARADOX`) | Shardfall's deep crater, where the Bleed made echoes of the past and the future. |
| **T2-5 Crown of the Hoarwood** (`PG_CALYREX`) | Anja and Ysolde's winter legend. |

### Tier 3: Apex Rematches and the Convergence
These are the story legends, rematched and caught (`:catch => :last_bar`). Each giver is the Warden who was there:
- **Kyogre and Groudon:** Anja and Sahar.
- **Zekrom and Reshiram (then Kyurem):** Rook and Sigrun. On Reshiram, Sigrun tests the PC, because it chose her.
- **Giratina:** the Distortion Core (P5).
- **Zygarde:** P3. It's already the PC's if `ZYGARDE_CHOOSES`; the Tier 3 card is its 100% form.
- **Echoes of Distant Worlds:** the box legends.
- **The 18-Plate Convergence** (`PG_ARCEUS`, S294): Arceus, Lv 100, with the Legend Plate, 4 bars, `:catch => :last_bar`. This is **non-Ruin endings only.**

```
(At the Convergence's start, in the arena, on the Ring where Valen held it, the eighteen Wardens kneel at the pylons again, empty-handed this time, because they want to see.)
[name: Arceus] Little light. You came back. I said I would not take what is not given. Will you give me a test?
(At the end, caught or not:)
[name: Arceus] (if caught) Then I will walk with you a while. Not chained. Not bought. Given.
```

## P2. The lighthouse (Ferrow's Landing; touch, Hesper at the lamp, V143 >= 1 → 2)
The PC's first post-game visit to Ferrow's Landing, where the game began.
```
(Ferrow's Landing lighthouse, at the top of the stair. Hesper Vane, seventy-eight, at the lamp, polishing a lens that doesn't need it. She doesn't turn round.)
[portrait: HESPER, neutral] Sprog. Edda said you'd come up eventually. Everyone comes up eventually. It's the only view in town.
[portrait: HESPER, sad] Tell me about her last night. My daughter. Morwen. You were there. You were five. I know you won't remember. Tell me anyway.
```
```
[if S141 CH15_ECHO_DONE]
  (You tell her. The echo. The vestry. Ines at the door. The Mismagius closing your eyes. "I'll carry the name.")
  (She listens to all of it without turning round. When you're done she keeps polishing the lens.)
  [portrait: HESPER, sad] ...I spat on her grave. Did he tell you that? Kestrel. I spat on it. In front of him.
  [portrait: HESPER, neutral] (putting the cloth down) I'm going to go and apologise. It's a long walk to Gravenmoor. I'll take the ferry. They run again now.
[if KESTREL_LOST]
  [portrait: HESPER, sad] And the boy. They told me. I light the lamp for him. Nobody needs it. I light it anyway.
[if !KESTREL_LOST]
  [portrait: HESPER, smug] And the boy. He writes now. Badly. Every week. Complaining about the Gravenmoor damp. [if KESTREL_ACCEPTED_SEAT] The Ghost Warden of Gravenmoor complains about the damp. I've framed one.
V143 = 2.
```
*(The last of 08's post-game hooks: "Hesper Vane, finally, asks the PC to tell her about her daughter's last night".)*

## P3. Valen's memorial: **Zygarde chooses** (Crownhaven, the Basilica garden; `ZYGARDE_CHOOSES` = Valen Bond ≥ 3 or Ilsa reconciled; V143 >= 1 → 3)
```
(Valen's memorial: forged by Brann from the empty Crown's setting, a plain ring of metal on a plinth. No statue. Valen would have hated a statue.)
[if ILSA_RECONCILED] (Ilsa sitting on the plinth's step, earmuffs round her neck, not on.)
(On the plinth, a single green Cell, glowing. It was on Valen's windowsill. Somebody brought it here.)
[if ZYGARDE_CHOOSES]
  (The Cell lifts off the plinth and settles against your hand, the way the Cell on the sill pulsed once, the night before the Final.)
  [if ILSA_RECONCILED]
    [portrait: ILSA, neutral] (not looking up) He asked it if he was wrong. It never answered him. (A beat.) I think that's the answer. It's choosing you instead.
  RECEIVE: ZYGARDE CUBE (the Cell quest completes; the 100% form is Tier 3).
[else]
  (The Cell stays on the plinth. It glows, steadily, at nobody.)
V143 = 3.
```

## P4. The Concordance Spire and **the Warden's Gauntlet** (S266, S267; the Spire lobby; V143 >= 1 → 4)
- **The Spire** (Battle Tower) is open: the facility rules are design-side (the battle-facility team).
- **The Warden's Gauntlet**: all eighteen Wardens back-to-back at Lv 100.
  - In Homecoming their teams use no fields, because the Imprints are fading: a "pure" gauntlet.
  - **PBS (added):** version **98** of every Warden (e.g. `[LEADER_DORIAN,Dorian,98]`, `[LEADER_SIGRUN,Sigrun,98]`; +100 Hard, +200 Casual), Lv 96–100 with the ace at 100; Juno is `[LEADER_JUNO,Juno,60]` / `[LEADER_JUNO,Juno,61]` / `[LEADER_JUNO,Juno,62]` (`Prismfall::Rival.version_for(6)`, her starter follows the player's). Gyms 6–18 are the gym six with the Hard sets promoted; Dorian, Tamsin, Rook and Sahar are rebuilt with the same partners grown up (Bobbin is a Leavanny); Marisol is her Festival six. "No fields" is the event's battle rule.
  - **Refusing Wardens are absent** after Homecoming, Unfinished. Their pedestals stand empty, with a line each from `11_FINALE_LINES.md` §3.
```
[portrait: DORIAN, happy] (in the Gauntlet's antechamber, in his best coat) First on the bill again, darling. Some of us are born to open.
[portrait: SIGRUN, neutral] (at the far end, last) I'll be here. All eighteen of us, in order. No fields, no Plates. Just us and what we taught them.
V143 = 4.
```

## P5. The Distortion Core (Antumbra, 910; S268)
Dask at Vigil's Grave Glass: "The wound in its side. It never closed. It's in the Core, guarding the hole it can't mend. Go and see it. Don't look back on the way in. Habit, now, isn't it."
- The Core: an inverted labyrinth (Gemini T3-3). The rematch is **Giratina Origin**, Lv 98 with the Griseous Core, `:catch => :last_bar`.
- On capture or defeat: *(The wound along its side, at last, starts to close. Behind it the Glass goes quiet. The rifts (T2-1) stop opening, one by one.)*

## P6. **Concord Zero** (Quent's post-game arc; S269; opens after the Gauntlet's first clear, or at once on Concord Dawn)
The seed: **Dr. Quent escaped with an Engine fragment** (08). A three-part post-game arc, outlined here. Its full script comes after the Tier 1 cards are built.
1. **"The Readings"**: Calla (if alive) or Larch finds Meridian accounts still paying a lab that doesn't exist. Trace it through Lumen's dark districts to a sealed Spire sub-basement.
2. **"Zero"**: Quent has built a pocket Engine around the fragment, the size of a room, and fed it the Ch14 telemetry archive. He's growing something to the shape of UNIMPRINTED-01. *(It's not a clone. It's an echo of the PC's readings with nobody inside.)*
3. **"Retention"**: the PC fights it: a boss with the PC's own team's *types* and no Imprint. Then Quent, who giggles until the end: "Indefinite! I wrote *indefinite*! I never thought anyone would *read* it!" Then the arrest (Marchetti, if turned) or the escape (else; a hook for later).

**Opening scene** (P6.1, touch, the Registry board's black card, which appears at S267):
```
(A black card on the Registry board. No Warden's name on it. Larch takes it down and turns it over. On the back, in Quent's neat hand: "Your readings were the most beautiful thing I've ever seen. I kept them. — P.Q.")
[portrait: LARCH, angry] (very quietly) He kept them.
Switch S269 PG_CONCORD_ZERO = ON. V143 = 5.
```

## P7. Cameo superbosses and the rest (pointers)
- **Lin** and the Lv 100 cameo rematches: `design/CAMEOS.md`. Lin's lines change by ending.
- **Garret's Eden rumour** near Marrowgate: a deliberate dead end, and a kindness (CAMEOS).
- **The Shardfall Isles (905) and the Hallow Strait (900/901):** the outer islands where the quarantine began, with the Bleed remnants fading. Edda's ferry runs there; Tier 2 and Tier 3 cards point there.
- **Brann's forge** (`AS_FORGE_REMEMBERS`) stays open if it wasn't done.

---

## Continuity fixes to Gemini's network (applied in this script; the quest builders follow these)
1. **T1-3:** "Corvin & Wenlow" is now **Corvin (if freed) or Mother Gutter**. Wenlow died in Interlude IV (Ch16); his notes are the lead.
2. **T1-6:** Calla only if `CALLA_ALIVE` (`:ch20_calla != :send_back`). Kestrel only if not `KESTREL_LOST`. The NULL CRADLE KEY (Ch10) opens it as well.
3. **T1-2:** Ogerpon joins the party **only here**. In the story it's a partner/follower (Ch10, Ch18), and on Juno's Festival team.
4. **The Convergence (Arceus):** never on the Ruin Route (12_RUIN_ROUTE: Arceus doesn't return), and never after the Gilded Chain (no post-game at all).
5. **The Ch14–19 story bosses** are rematched here, all `:catch => false` in their story fights: Groudon (Undersands), Giratina (the Core), Zekrom, Reshiram (Sigrun tests the PC), Pecharunt (T1-3), Kyogre.

## Map and event needs (post-game)
**Registry and Crownhaven**
- the Concordance Spire lobby: the Registry board, an easel of 18 columns of pinned cards; Larch's hangout
- Valen's memorial in the Basilica garden: the Cell; ZYGARDE CUBE
- the Gauntlet antechamber and 18 pedestals (empty for refusers)
- the Crownhaven Opera Hall (T1-1)

**Elsewhere in Velmora**
- the Ferrow's Landing lighthouse top: Hesper (the map exists from the Prologue)
- the Distortion Core (910)
- the Concord Zero sub-basement: [NEW], in the Lumen Spire

Each Tier card's maps are in Gemini's table.

**Portrait requests (art, to Gemini):** **HESPER** (`neutral`, `sad`, `smug`).
