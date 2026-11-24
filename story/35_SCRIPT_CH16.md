# Script: Chapter 16 — "Clear Air" (the Slag Road, Cogsworth, Gym 15; Rook's footage; Strade Works: the casting floor, the blueprints, Zekrom; Magnus; Operation Clear Air; Interlude IV)

> **Final playable script** for Chapter 16. Maps: the Slag Road out of the Hush (801 the Slag Mesa and the Slagglass, 811 the Smokestack Parade), Cogsworth (400–402, plus the canteen and the clock-tower as [NEW] interiors), Gym 15 (410–414), Strade Works (403 the Foundry Floor; [NEW] 404 the Casting Floor, 405 the Drafting Vault, 406 the Engine Core Chamber), and Mirefen for **Interlude IV** (220 the stilt-walks, 223 Corvin's Infirmary and the Quiet Ward). The chapter ends on the supply-lift down to Midstair (830). None of these maps is built; the list at the end is what to build from.
> Follows `story/34_SCRIPT_CH15.md`. Chapter 17 ("The Drowned Crown") follows. Sources: 07_ACT_IV Ch16, 03_CAST (Rook, Magnus, Marchetti, Quent, Corvin, Wenlow, Sallow, Brann), 08_ACT_V (the proof: the Arbiter Blueprints; Magnus at the governor; Rook cuts the grid), 09_MYSTERIES (#6 Voss at the dials, #14 UNIMPRINTED-01), NARRATIVE_KEYS (`:ch16_rook`, `:ch16_zekrom`, `:ch16_magnus`, `GO_OVERTIME`, `ROOK_CUTS_GRID`, `MAGNUS_EXPOSED`/`MAGNUS_KEPT_FAITH`, `VOSS_DISCREDITED`), 15_COMEDY Ch16 "Off Camera", GYM_PUZZLES Gym 15, WALKTHROUGH Ch16, the boss `:ZEKROM_ENGINE` (102_Boss_Zekrom.rb), the Trials quests `NA_LIFT_STRIKE` and `AS_FORGE_REMEMBERS`, `design/CHAPTER_BEATS.md`, `design/DENSITY_STANDARD.md`.

## Conventions
As in the earlier scripts. **Portrait cast here:** Rook, Magnus, Marchetti, Quent, Corvin (radio or cell only), **Wenlow** (playable in the Interlude), Sallow (if `:expose`), Brann (the optional forge), and the PC (no authored line this chapter). **Plain:** the Cogsworth workers, the canteen cook, the Unity Rally screens (Voss's voice, `[name: Voss (screen)]`), the Nadir commuters, the Directorate officers, the patients, every trainer.
**Gym 15** is a single battle: `Prismfall.gym_battle(15)`. **The casting floor** is a tag double: `pbRegisterPartner(:LEADER_ROOK, "Rook", 16)`, then `TrainerBattle.start(:MERIDIAN_MARCHETTI, "Helene", 2, :MERIDIAN_QUENT, "Percival", 1)` on `:FACTORY`. The Rook partner team, `[LEADER_ROOK,Rook,16]`, is now in PBS. **Zekrom** is `Prismfall::Bosses.wild_battle(:ZEKROM_ENGINE)` (registered; its bar 2 turns the field to `:SCRAPYARD`).
**Counter:** V137 **CH16_STEP** (new; design/FLAGS.md): 0 on the Slag Mesa · 1 Cogsworth: the Unity Rally · 2 Rook in the canteen (`:ch16_rook`) · 3 Gym 15 won · 4 the casting floor won · 5 the blueprints (S144) · 6 Zekrom freed (S145) · 7 Magnus (`:ch16_magnus`) · 8 Operation Clear Air (S146) · 9 Interlude IV · 10 the supply-lift at dawn (chapter closed; V102 = 17).
**State set here:** S144 CH16_BLUEPRINTS_GOT, S145 CH16_ZEKROM_DONE, S146 CH16_PURGE_BEGUN. Keys: `:ch16_rook`, `:ch16_zekrom` (`:freed`, set after the boss whatever the result), `:ch16_magnus`. Game over: `GO_OVERTIME`. Key Item: **ARBITER BLUEPRINTS**.

## The chapter's key events (design/CHAPTER_BEATS.md)
1. **The Arbiter blueprints and Zekrom freed.** In Strade Works' drafting vault:
   - eighteen locks built *into the new Festival arena*;
   - a keystone cradle "to be recovered from site AURELIA";
   - **"Calibration subject: UNIMPRINTED-01. Retention: indefinite."**

   In the core chamber, the Dark Stone has cracked open around a half-emerged Zekrom bound in golden cable. You free it; you don't beat it.
   - **Build-up:** Ch14's telemetry ("he's tuning you"), Ch15's young Voss at the dials, Larch's "never let them examine you".
   - **Payoff:** you read your own designation in someone else's handwriting.
   - **Consequence:** the Engine's first core is lost (Voss must reroute through Lumen's grid in Ch21), and the blueprints become a third of the Act V proof.
2. **The Sump Purge begins, and Wenlow dies.** "Operation Clear Air" sends the Directorate down into Nadir. Interlude IV is played as Wenlow, and the death **can't be prevented**.
   - **Build-up:** Wenlow since Ch6 (cheerful, clumsy, "I've read the book twice"), Corvin's Quiet Ward, the Fault draining the Sump.
   - **Consequence:** Nadir's anger (Ch17's independence), Corvin's grief, and the act's moral floor.

## Density (design/DENSITY_STANDARD.md; agents build from this section)
| Item | This chapter |
|---|---|
| Story/boss/rival fights (≥4) | **Gym 15 Magnus** · **the casting floor (PC + Rook vs Marchetti + Quent)** · **Zekrom** · **Interlude IV: Wenlow vs two officers** (all critical) · optional: the `NA_LIFT_STRIKE` officer, Brann's forge sparring |
| Route/gym/dungeon trainers (12–20) | 18 (roster at the end): the Slag Mesa 4, the Smokestack Parade 3, Cogsworth 2, Gym 15 6 (GYM_PUZZLES), Strade Works 3 |
| EventMons (≥3) | **Varoom "Lugnut"** (gift, a Nadir mechanic in the canteen) · **Heatmor "Torch"** (static, the Slagglass) · **Galarian Weezing "Clear Air"** (static, the top of the Smokestack Parade) |
| Hangouts (2–4) | Rook in the canteen · *one of* Magnus at the clock-tower (`:conscience`) / Sallow at her airship dock (`:expose`) · Brann's forge (optional quest, any time from 15 badges) |
| Glassfall Slivers (4–6) | 5: the Slagglass, a Smokestack Parade chimney-top, Cogsworth's clock-tower, the canal floor (**Dive**, from the bathysphere works), the drafting vault's waste-bin |
| Trials quests (≥3) | `NA_LIFT_STRIKE` (Midstair, **closes when the Purge begins**, S146) · `AS_FORGE_REMEMBERS` (Brann, from 15 badges) · new **`ZE_LETTERS_DOWN`** (the commuters' letters, delivered in Ch17) · `ZE_RETURN_TO_SENDER` and `EL_DOLL_WHO_WAITED` (Mega quests, from 14 badges) |
| Badge overlay | Badge 15: `encounters_badgetiers.txt` tier for 801, 811 |
**No jokes** from the Operation Clear Air broadcast (V137 7 → 8) to the end of the chapter. "Off Camera" plays in the canteen at V137 1 → 2.

---

# CHAPTER 16 — "Clear Air"

**Chapter start:** V102 = 16, V137 = 0. The Hush's far edge; the sound comes back. Quest log "Eighteen Roads": *North-east to Cogsworth and the Slag Mesa. Gym 15.*

## Map 801 — the Slag Mesa (`:WASTELAND`) and the Slagglass
Zenith's eastern waste: a mesa of slag heaps, black and grey, steaming in the rain, run off from three hundred years of foundries. On the skyline, Cogsworth: smokestacks that never stop, and clock-towers. The **Slagglass** is a field of fused slag that has turned to Bleed-glass. It hums. Wild Pokémon flicker in and out of it.
- **The Slagglass:** **Glassfall Sliver** in a slag bubble. A **Heatmor "Torch"** (static, Lv 67, Flash Fire) at a Durant mound, eating the colony one at a time very politely. Durant cries play from inside the mound.
- A scrap-picker from Nadir: "Day shift's Zenith folk. Night shift's ours. Third shift's anyone who'll take it. I'm all three. You learn to sleep standing up. Like a horse. Like a sad horse."
- A Meridian sign every hundred yards: "REMEDIATION ZONE. UNITY THROUGH INDUSTRY." The sign is rusting.
Trainers (Lv 67–68): a worker (a scrap-picker), a punk, a biker, an engineer (Meridian survey).

## Map 811 — the Smokestack Parade (`:FACTORY`)
A road of chimney-stacks and gantries into Cogsworth. Directorate banners hang from every gantry. On the tallest chimney, reached by a service ladder: **Glassfall Sliver**, and a **Galarian Weezing "Clear Air"** (static, Lv 67, Neutralizing Gas) sitting in the chimney's mouth, breathing smoke in and breathing out clean air. A worker at the foot of the ladder: "Nobody's told it to stop. Nobody's told it to start. It just does it. Best thing in Cogsworth."
Trainers (Lv 68): a worker, a scientist, a Directorate officer on a gantry ("Papers. ...You're the ferry child. The Director said you'd come. The Director says a lot of things.").

## Cogsworth (400–402): **the Unity Rally** (autorun at the main plaza, V137 == 0 → 1)
```
(Cogsworth. Three shifts, and the shift-whistles never quite stop. A clock-tower over every street, all of them chiming the quarter at once.)
(The main plaza: a crowd under a giant screen, Directorate banners down every wall. On the screen, Aurelian Voss, in a white suit, filling the sky.)
[name: Voss (screen)] Order. Light. Unity. For three hundred years the Bleed has eaten our children. Strade Works is building the machine that ends it. Every rivet you set this shift is a child who never turns to glass.
[name: Voss (screen)] Order. Light. Unity.
(The crowd says it back. Not loud. On time.)
[name: Worker] (next to you, quietly, to nobody) Don't know what we're building. Big, whatever it is. Round. Eighteen of something.
V137 = 1.
```
- **Cogsworth (400):** the Center (401), the Mart (402; Badge-15 stock, Metal Coat, Synthetic Seeds), the **bathysphere works** at the canal (Dive suits after Gym 15, as WALKTHROUGH: "Dive from the bathysphere works"). The **canal floor** (Dive) has **Glassfall Sliver**.
- **The clock-tower** [NEW interior]: a stair up through the works of the biggest clock; at the top, **Glassfall Sliver** behind the minute-hand's counterweight. After `:conscience`, it's Magnus's hangout (below).
- Townsfolk: a Nadir commuter with a lunch-tin: "Lift up at five, lift down at nine. My mum says I smell of Zenith now. I say she smells of Nadir. We're both right." A foreman, about Voss: "Man pays on time. You'd be surprised how much you'll forgive a man who pays on time."
- **`NA_LIFT_STRIKE`** (optional; Midstair, via the Cogsworth lift-head; as catalogued). **It closes when the Purge begins (S146)**: the union's last strike. After that the lifts run Directorate traffic only, and the giver's line becomes "They broke it. With the lifts still full."
- **New: `ZE_LETTERS_DOWN`** (optional; rank 1; giver: the commuter with the lunch-tin). Five Nadir commuters on the third shift each have a letter for home. The lift's post-sack is "full, they say", so the PC carries them. Collecting all five before the Purge (S146) is the quest; delivering them happens in Ch17's Nadir. One of them is addressed to "Mum, Underveil, the green door." **Reward:** Odessa's postbag ribbon (a Gale Post standing + 1, a Codex line).

## The canteen: **Rook, off-camera** (touch, a hunched figure at the back table, V137 == 1 → 2)
```
(The workers' canteen. Steam, noise, long tables, soup. At the back, alone, unshaven, in a borrowed work-coat with his holo-jacket balled up under the bench: Rook Calder. No drone. Nobody's recording.)
[portrait: ROOK, neutral] Hey. Hey. Don't — don't say my name. Sit down. Please.
```
**Comedy scene Ch16, "Off Camera"** (15_COMEDY as written). Then:
```
[portrait: ROOK, neutral] (pushing the bowl away) I've been going to the Spire every night since the Lowlight. To see them. Dex. The other eleven. I just stand there. Nobody films that.
[portrait: ROOK, sad] And I've been doing something else. The Spire's security system backs up to the building I'm contracted to. I've got the password. They never changed it. I've been copying the footage.
(He slides a small Lattice-glass slate across the table and taps it. Grey, silent footage: a Spire service corridor, night. A figure in a long coat swipes a keycard at the Plate Vault door. The light goes green. The figure turns, and it's Sable.)
[portrait: ROOK, sad] Sable. With a Meridian keycard. The night of the Lowlight. I've had it for months.
[portrait: ROOK, sad] I was scared. I'm still scared. You're the only person I know who isn't scared of anything.
(You are, actually. He doesn't need to know.)
[portrait: ROOK, neutral] So. Tell me what to do. Put it out now? Or sit on it, smile for the cameras, and wait for the worst possible moment?
```
```
> Leak it now. (leak_now)
  Script: pf_choose(:ch16_rook, :leak_now)
  [portrait: ROOK, neutral] (a long breath) Okay. Okay. Rotom — no. No Rotom. I'll do it myself. Old-fashioned. A post on every channel I've got.
  (He taps the slate. Somewhere above Cogsworth, on every screen, the grey footage plays between the Unity Rally clips.)
  [portrait: ROOK, shocked] (his own slate buzzes forty times in a row) That's Meridian legal. That's Meridian legal. That's — oh, that's my contract. That's my contract being terminated. By message. With an emoji.
  [portrait: ROOK, happy] (laughing, shaky) I'm fired. I'm blacklisted from the Spire. I'm — I think I'm free? Is this what it feels like?
> Hold it for the Festival. (hold)
  Script: pf_choose(:ch16_rook, :hold)
  [portrait: ROOK, neutral] (pocketing the slate) The worst possible moment. Opening ceremony. Forty thousand people and Voss on the dais. I can do that. I'm good at moments. It's the only thing I'm good at.
  [portrait: ROOK, sad] And I keep my keycards. All of them. Including the ones that open Strade Works. (A beat.) Want to see what they're building?
V137 = 2.
```
*(NARRATIVE_KEYS: `:leak_now` MERIDIAN−2 HOLLOW+1; Kroll exposed realm-wide even without Ch13's evidence; Rook can't cut the grid in Ch21 or reach the Zap Plate unless Marchetti turns. `:hold` → `ROOK_CUTS_GRID`. **On `:leak_now`, Rook still has the Strade Works keycards.** Meridian revokes his Spire access, not the contractor cards it forgot it had issued: "Nobody cancels the cards. Nobody ever cancels the cards." The infiltration happens on both branches.)*
- **Gift: Varoom "Lugnut"** (Lv 40, Overcoat), from a Nadir mechanic at the next table who's been listening: "It lives in my lunch-tin. It's outgrown the lunch-tin. You look like someone with a bigger lunch-tin."
- **Hangout, Rook in the canteen** (from V137 >= 2 until S146): *Off Camera*, Rook trying ordinary things for the first time. Laundry. Queuing. Being bad at something with nobody watching. It's the comedy runner's soft side.

## Gym 15 — Strade Works (410–414, `:FACTORY`)
As GYM_PUZZLES Gym 15: 410 Gatehouse (teach: the tick clock), 411 Assembly Line (twist: shared belt groups), 412 Crane Bay (combine: feed the press a crate), 413 the arena, **414 Tolerance Lab** (Mastery, optional). Gym trainers (6): Engineer ×2, Worker ×2, Scientist, Meridian Foreman; Lv 67–70.
*(GYM_PUZZLES 413 mentions "the partner battle with his apprentice comes just before". That's superseded: the partner battle is the casting floor **after** the gym, per 07_ACT_IV and this script.)*
- **Klink foreman at 410:** "The line moves when you move. Mr. Strade likes it that way. Mr. Strade likes everything a particular way."

### 413 — the Warden Arena
```
(A clean white arena in the middle of the foundry. A man in an immaculate grey suit, a prosthetic right hand of polished steel, consulting a pocket watch.)
[portrait: MAGNUS, neutral] Four minutes and twelve seconds through the Crane Bay. Two seconds over tolerance. Acceptable.
[portrait: MAGNUS, neutral] Faith gave us three hundred years of the Bleed. Engineering will give us the next three hundred without it. I'm told that's a slogan now. I wrote it as a sentence.
[portrait: MAGNUS, neutral] Begin when ready. I'm always ready. It saves time.
BATTLE: Prismfall.gym_battle(15)
```
- **Mid-battle (Metagross "Engine" Mega Evolves):** "The foundry hammers its plating home. Tolerances: zero." `[bubble: MAGNUS, neutral, sparkle]`
- **Win:**
```
[portrait: MAGNUS, neutral] (closing the watch) Within tolerance. Yours, not mine.
RECEIVE: the TOLERANCE BADGE (badge 15). RECEIVE: TM91 FLASH CANNON.
[portrait: MAGNUS, neutral] The bathysphere works will fit you for a diving suit. The canals here go down further than people think. Most things do.
RECEIVE: (at the bathysphere works) DIVE.
V137 = 3.
```
*(Badge name, proposed: the **Tolerance Badge**. The VS plate reads ARTIFICER above MAGNUS.)*

## Strade Works, the night shift: **the infiltration** (touch, Rook at the works' side gate, V137 == 3)
```
(Night. The works' side gate. Rook in his borrowed work-coat, with a lanyard of keycards.)
[portrait: ROOK, neutral] Rule one. We go when the whistle goes. No heroics. Rule two. I'm in charge of rule one.
(He swipes. Green. The gate opens onto the night shift: three hundred workers, sparks, a noise like the inside of a bell.)
```
- **The Foundry Floor (403):** a stealth-lite crossing. Night-shift foremen patrol fixed step-routes (Gym 16's guard system, reused). Being seen means a fight (Strade Works trainers ×3, Lv 69–70) instead of a reset: "Papers!" Rook: "We're from Quality." The foreman: "Quality doesn't come at night." Rook: "That's what makes it quality."

### 404 — the Casting Floor: **PC + Rook vs Marchetti + Quent** (touch, critical; V137 == 3 → 4)
```
(The Casting Floor: a hall the size of a cathedral, molten metal running in channels, ladles the size of houses on chains overhead. On a gantry, waiting, Director Marchetti and Doctor Quent.)
[if MARCHETTI_TURNED]
  [portrait: MARCHETTI, neutral] (not quite looking at you) I'm here because he's here. Don't read anything into it. (A pause.) Read something into it.
[else]
  [portrait: MARCHETTI, neutral] The Spire logged a contractor card at the side gate. Forty minutes ago. I didn't think it'd be you, Calder.
[portrait: QUENT, happy] And the young person! You never came for your medical. I'll take that as a "later". Most people mean later.
[portrait: ROOK, angry] (stepping up beside you, voice shaking, standing anyway) Hey. Doctor. Chat says you're creepy. Chat's right for once.
Script: pbRegisterPartner(:LEADER_ROOK, "Rook", 16)
BATTLE: TrainerBattle.start(:MERIDIAN_MARCHETTI, "Helene", 2, :MERIDIAN_QUENT, "Percival", 1) — tag double; `:FACTORY` (Bronzong's Explosion or three quakes → `:SCRAPYARD`).
(LOSE: whiteout to 401; the infiltration restarts at the side gate, with Gym 15 kept.)
(WIN:)
[if MARCHETTI_TURNED]
  [portrait: MARCHETTI, neutral] (to her troopers, flat) They went up the east stair. Go up the east stair. (They go up the east stair. You're on the west one.)
[else]
  [portrait: MARCHETTI, angry] (Houndoom down, breathing hard) Get the doctor out. The floor's going.
[portrait: QUENT, neutral] (being helped away, smiling at you over a shoulder) Such interesting readings. You really should let me look. It would save everybody a great deal of trouble.
V137 = 4.
```
*(Mega Houndoom is the pair's one Mega (WALKTHROUGH). On `MARCHETTI_TURNED` she still fights: "I don't throw fights. I just lose them carefully.")*

### 405 — the Drafting Vault: **the Blueprints** (touch, the central drafting table, V137 == 4 → 5; key event 1)
```
(The Drafting Vault: tall cabinets, drafting lamps, blueprint-paper hung on lines like washing. Silent. At its centre, a table as long as a ship with one blueprint pinned across all of it.)
(A ring. A stadium-sized ring of eighteen locks, built into the bowl of a new arena. The title block: CROWNHAVEN FESTIVAL ARENA (RENOVATION). ARBITER ENGINE — INSTALLED SYSTEM.)
(In the middle of the ring: a cradle. A margin note in neat engineer's hand: "Keystone. To be recovered from site AURELIA.")
(At the bottom of the sheet, a box, the kind every blueprint has, for the load it's built to carry.)
(CALIBRATION SUBJECT: UNIMPRINTED-01. RETENTION: INDEFINITE.)
(You read it twice. It doesn't change.)
[portrait: ROOK, shocked] (reading over your shoulder) "Unimprinted"... that's — that's you. That's what they call you on the screens. "Retention"? What's "retention"?
(The copier at the end of the table is already running; Rook set it going when you came in. Sheet by sheet, the blueprints feed through.)
RECEIVE: ARBITER BLUEPRINTS (Key Item). Switch S144 CH16_BLUEPRINTS_GOT = ON.
V137 = 5.
```
*(Never say what the keystone is (the Legend Plate, Ch17) or what "retention" means beyond the word. Ch17 names the shard; Ch20 says "keep" out loud. In the waste-bin by the copier: **Glassfall Sliver**, wrapped in a spoiled print.)*
- A door at the back: ENGINE CORE — AUTHORISED ENGINEERS ONLY. Rook: "We're engineers. We're engineering this."

### 406 — the Engine Core Chamber: **Boss: Zekrom** (touch, the cage, V137 == 5 → 6)
```
(A round chamber three storeys high. In the middle, a cage of Lattice-glass bars, and in the cage, a great black stone the size of a house, which has split open like an egg.)
(Half out of the stone: a dragon, black as the stone, its tail a turbine of blue light. Bound in golden cable, a hundred strands, every one of them humming.)
[portrait: ROOK, shocked] That's... that's not a stabiliser.
(The dragon opens one eye. It looks at the cables. It looks at you. You understand, without knowing how: it isn't asking you to fight it. It's asking you to help it pull.)
BATTLE: Prismfall::Bosses.wild_battle(:ZEKROM_ENGINE) — Lv 72; bars Casual 2 / Standard 3 / Hard 4; `:FACTORY`, then `:SCRAPYARD` at bar 2.
(LOSE: whiteout to 401; the infiltration restarts from the vault (the blueprints are kept).)
```
*(The boss's own messages: "A containment cable around Zekrom snapped!" at each bar, "The Engine core buckles!" at bar 2, and on defeat "The last cable tore loose! Zekrom broke free of the Engine core and burst through the roof!")*
```
(The last cable goes. Zekrom rises out of the stone, slowly, the turbine of its tail spinning up into a scream. It looks at you once, the long flat look you're starting to know.)
(Then it goes straight up, through three storeys of Strade Works, through the drafting vault's ceiling, through the foundry roof, into the night. Far above Cogsworth, the Stormfront lights up from inside.)
Script: pf_choose(:ch16_zekrom, :freed)
Switch S145 CH16_ZEKROM_DONE = ON. V137 = 6.
```
**☠ `GO_OVERTIME` "Overtime"** (immediately after; a countdown):
```
(A klaxon. Red lights. A voice on a speaker, calm: "CORE BREACH. CONTAINMENT VENT IN THREE.")
(In the control booth by the door, the copier is still running: the calibration annex, forty pages. It's on page thirty-one.)
[portrait: ROOK, panic] (from the door) That's the whistle! That's the whistle! No heroics!
> Finish copying? (3)
  > Stay.  (Page thirty-four.)
  > Go.    — (out)
["CONTAINMENT VENT IN TWO."]
[portrait: ROOK, panic] I said no heroics! I'm not saying it a third time!
> Finish copying? (2)
  > Stay.  (Page thirty-eight.)
  > Go.    — (out)
["CONTAINMENT VENT IN ONE."]
> Finish copying? (1)
  > Stay.  Script: Prismfall.game_over(:GO_OVERTIME)
  > Go.    — (out)
(out:) (You dive through the bulkhead as it slams behind you. Through the porthole: white fire filling the chamber, the copier going with it.)
```
*(NARRATIVE_KEYS §9 epitaph: "You stayed past the whistle. Strade Works issued a statement about an industrial accident." The prompts time out after 3 seconds each as "Go" (the countdown is real). Rook only warns twice.)*

## The ruined vault: **Magnus** (autorun on coming through the bulkhead, V137 == 6 → 7)
```
(The Drafting Vault, wrecked. Zekrom's exit has torn a hole through the ceiling to the night sky. Rain is coming in. Blueprint-paper everywhere, soaking, blowing about. Rook's gone ahead to hold the lift.)
(In the middle of it, picking up a sheet of wet paper with his steel hand, smoothing it on a ruined table: Magnus Strade.)
[portrait: MAGNUS, neutral] (without looking up) Don't run. I haven't called security. I'm not going to.
[portrait: MAGNUS, neutral] I don't build weapons. I build tolerances. When they came to me, I was told it was a Plate stabiliser. Eighteen Plates, one cradle, the Bleed ended for ever. I believed it. It was beautiful.
[portrait: MAGNUS, sad] I learned the truth two years ago. That box at the bottom of the sheet. I kept building. Because the mathematics was beautiful, and the alternative was the Bleed.
(He holds up the sheet: CALIBRATION SUBJECT: UNIMPRINTED-01.)
[portrait: MAGNUS, neutral] I didn't know it was a child until I saw you in the gym. Four minutes twelve through the Crane Bay. I thought, that's a person who would have been very good at my job.
(He winds his pocket watch. Click, click, click.)
[portrait: MAGNUS, neutral] What will you do with me?
```
```
> Expose him. (expose)
  Script: pf_choose(:ch16_magnus, :expose)
  (You take the blueprints to Councillor Renata Sallow, at her house's airship dock on Cogsworth's heights, before dawn.)
  [portrait: SALLOW, neutral] (reading by a gas-lamp, in a dressing-gown, very awake) Oh, Aurelian. Oh, you *fool*. (To you:) The Council sits at nine. He'll lose the board vote. He'll lose half the city. He won't lose the war. (A beat.) And Strade?
  (Magnus is arrested at dawn, in his suit, in the plaza, under the screen with Voss on it. He doesn't resist. He winds his watch as they take him.)
  [portrait: MAGNUS, neutral] (passing you, in irons) Correct. Unpleasant. Correct.
> Appeal to his conscience. (conscience)
  Script: pf_choose(:ch16_magnus, :conscience)
  (You hold up the sheet with your designation on it.)
  (You don't say anything. You don't need to. The question is on the paper.)
  [portrait: MAGNUS, neutral] (he looks at it for a long time) ...Will I let it take a child.
  (He says nothing. He winds his watch. Click, click, click. He puts it away. He picks up the next wet sheet, and the next, and starts to put the vault back in order, by himself, in the rain.)
V137 = 7.
```
*(NARRATIVE_KEYS: `:expose` ACCORD+1 MERIDIAN−2 VOSS−1 → `MAGNUS_EXPOSED`; with Rook's leak, `VOSS_DISCREDITED`. The design leaks publicly, but nobody is left inside. `:conscience` → `MAGNUS_KEPT_FAITH`: in the finale he disables the Engine's safety governor: "No machine I have built will kill a child." The ARBITER BLUEPRINTS stay in the Bag on both branches: Sallow has copies made. They're one of the three proofs (08_ACT_V).)*
- **Hangout (one per path):** `:conscience` → **Magnus at the clock-tower**, winding the city's clocks by hand at night, "to keep my hands busy". He'll talk tolerances, never the Engine. `:expose` → **Sallow at her airship dock**: Council gossip, Voss's board, her house's old airships.

## **Operation Clear Air** (autorun on leaving Strade Works, V137 == 7 → 8; no jokes from here to the end of the chapter)
```
(The plaza, past midnight. Rook waiting at the lift-head with his collar up. The third shift has stopped. Everyone is looking at the screens.)
(On every screen in Cogsworth, a white sunburst on black, and two words: OPERATION CLEAR AIR.)
[name: Voss (screen)] Since the Fault drained the Sump, Nadir's lower districts have fallen into lawlessness. Sweetrot gangs. Hollow terror cells. Tonight the Directorate restores order to the Underveil and the Mirefen.
[name: Voss (screen)] Topside, you have nothing to fear. Go home. Sleep. In the morning the air will be clear.
(On the screen: a column of grey coats marching into a lift. The lift going down.)
(Around you, nobody says anything. A man next to you finishes his soup.)
[name: Worker] (quietly, to nobody) My mum lives down there.
Switch S146 CH16_PURGE_BEGUN = ON. V137 = 8.
(`NA_LIFT_STRIKE` and `ZE_LETTERS_DOWN` collection close here; the letters already carried are delivered in Ch17.)
```

---

# INTERLUDE IV — "Clear Air" (play as Wenlow; V137 == 8 → 9)
**Staging:** fade to black, then the title card "INTERLUDE IV — Clear Air". **Party swap:** V119 INTERLUDE_ACTIVE = 4 (the existing interlude swap, as in Interludes I–III). The PC's party is stored; the player character is **Wenlow** (a new charset); his party is **Corvin's spare Pokémon**: **Amoonguss, Swalot, Gastrodon, Lv 62** (a new loadout). Mirefen at night, rain on the marsh, the stilt-walks lamp-lit. The BGM is the Infirmary theme, then **silence** from the Ward doorway on.

## Map 223 — Corvin's Infirmary (Wenlow's opening)
```
(Corvin's Infirmary in the Mirefen. Night. Rain on the tin roof. Rows of cots. At the back, behind a curtain of hanging glass-beads, the Quiet Ward: forty patients who don't move, dreaming, some of them faintly glass at the edges.)
(A young man of seventeen in a too-big oilcloth coat, the plague-doctor half-mask pushed up on his forehead, carrying three trays at once, about to drop all of them: Wenlow.)
[portrait: WENLOW, happy] (to the room) Right! Evening rounds! Mrs. Pell, water. Old Fisk, the green one, not the brown one, the brown one's for the — yes, that one.
[if CORVIN_FREED]
  [portrait: WENLOW, neutral] (at the radio on the shelf) Infirmary to Cragholm, Infirmary to Cragholm. Doctor? It's me. I'm back with the medicine. Everyone's turned. The glass ones are fine. They're always fine. (A pause.) That's a joke. You never laugh at that one.
[else]
  [portrait: WENLOW, neutral] (to a photo pinned over the desk: Corvin, masked, scowling) I'm back from the seams, Doctor. Sack of medicine, like I promised. Somebody has to turn the glass ones. You'd be furious if nobody turned the glass ones.
(The radio crackles. A voice, not Corvin's: a fisher on the stilt-walks, out of breath.)
[name: Radio] Infirmary? Grey coats at the east walks. Lots. They're going house to house. They've got the Sweetrot list.
(Wenlow puts down the trays. All three. Without dropping any of them.)
[portrait: WENLOW, neutral] ...Okay. Okay. I've read the book twice.
```

## Interlude play (223 and 220, the stilt-walks): three tasks, any order, then the Ward
1. **Move the walking patients**: six patients who can walk, led down the back ladder to the boats (follow-the-leader; each one has a line: "Is it the gangs?" "No, Mrs. Pell. It's the government." "Oh, that's worse.").
2. **Hide the Sweetrot addicts in the Quiet Ward**: four Sweetrot patients, shaking, carried to cots among the glass patients. The mechanic: Wenlow lays a sheet over each one and they go still.
```
[portrait: WENLOW, neutral] (laying the last sheet) They won't search the glass ones. Nobody ever looks at the glass ones.
```
3. **Fight two officers on the stilt-walks**: Directorate officers searching the walk-houses, in single battles on the walk (`:CORROSIVE_MIRE`, Lv 62).
```
BATTLE: TrainerBattle.start(:MERIDIAN_DIRECTORATE, "Officer Grane") — single; Wenlow's party.
BATTLE: TrainerBattle.start(:MERIDIAN_DIRECTORATE, "Officer Tull") — single; Wenlow's party.
(LOSE: back to the Infirmary; the task resets. The Interlude can't be failed, only replayed.)
[name: Officer Tull] (recalling his Pokémon, irritated) Medic. You're obstructing. There's a list. Stand aside, or you're on it.
[portrait: WENLOW, neutral] I'm not on any lists. I'm not important enough for lists.
```

## The Ward doorway (autorun once all three are done)
```
(The Infirmary. Silence: the BGM cuts. Only the rain.)
(The front door opens. A Directorate squad: six grey coats, a lieutenant with a list, lamps.)
[name: Lieutenant] Medical facility. We have reason to believe Sweetrot users are being harboured on these premises.
(Wenlow is standing in the Ward's doorway, in front of the bead curtain. Behind him, forty patients dreaming. Four of them breathing.)
[portrait: WENLOW, neutral] (the mask pushed up, his hands open) This is a hospital.
[portrait: WENLOW, neutral] You have to —
[anim: cut to black, 0 frames]
(A single gunshot SE. Nothing else. No music. Hold black for 120 frames.)
```
*(**This death cannot be prevented**: there is no branch, no prompt, and no stat check. No text after the cut. The shot is the only sound. V119 = 0: restore the PC's party and charset in the black.)*

## Aftermath (on the black, then the fade-in)
```
[if CORVIN_FREED]
  (Cragholm, the deep seams, the hospital. A radio on a pit-prop. Corvin is sitting very still next to it, in his coat, the mask in his hands.)
  [name: Radio] ...Infirmary to Cragholm. Infirmary to — (static) — is anyone — the boy, Doctor. The boy. (static)
  (Corvin doesn't move. Pip, in the doorway, starts to come in, and Bastian, behind her, puts a hand on her shoulder and stops her.)
[else]
  (A Directorate cell. Corvin on a bench, unmasked, his hands bandaged. A young guard at the bars, eating, chatting to nobody.)
  [name: Guard] They did the Mirefen last night. Your place. (chewing) Some kid in the doorway. Wouldn't move.
  (Corvin stands up. He walks to the bars. He doesn't say anything. The guard stops chewing.)
V137 = 9.
```
*(The Quiet Ward's four hidden patients survive, and the forty dreaming ones aren't touched: "Nobody ever looks at the glass ones" is true. This is Wenlow's whole legacy, and Corvin's Quiet Ward testimony in Act V (08_ACT_V's proof: "testimony that the Fixed still dream") rests on it.)*

---

## Cogsworth, dawn: **the supply-lift** (chapter close; autorun at the lift-head, V137 == 9 → 10)
```
(Dawn over Cogsworth. Grey. The shift-whistles haven't started yet. Rook at the supply-lift, holding the cage door, his work-coat buttoned to the neck.)
[portrait: ROOK, sad] I heard on the union band. The Mirefen. The Infirmary. A kid.
(He doesn't say anything else. He holds the door.)
(The cage goes down. Through the grille in the floor, a long way below, Nadir: the stacked districts, the drained Sump, and over the Underveil, smoke, rising straight up in the still morning air.)
(In your Bag: the blueprints. CALIBRATION SUBJECT: UNIMPRINTED-01.)
V137 = 10. Variable V102 STORY_CHAPTER = 17.
QUEST LOG: "Eighteen Roads" — Down into Nadir. The Underveil is burning. Gym 16.
```
*(Ch17 opens on the Hanging Stair down into the Drownings and the Underveil.)*

## Optional: **Brann's forge** (`AS_FORGE_REMEMBERS`; Hearthguild anvil, 244; any time from 15 badges until the Festival)
As written in 07_ACT_IV Ch16 and the Trials plugin (the strings match). Brann knows his ring on your hand. If you told him the Light Stone was the Dominar's, he says so once and won't talk about it after. He gives you the **Cameruptite**, the twin of Kiln's. Most players find him on the way to Wyrmrest (Ch19). It's listed here because it opens at 15 badges.

---

## Map events needed (Chapter 16)

None of this chapter's maps is built. **[NEW]** = an event or map not in maps.json. V137 = **CH16_STEP** (design/FLAGS.md). Maps go through the three-pass workflow (design/MAPGEN.md, top).

**801 The Slag Mesa** (`:WASTELAND`): slag heaps; the Remediation signs; the **Slagglass** (Bleed-glass zone, a humming BGS; **Sliver #1**; **Heatmor "Torch"** static at the Durant mound); the scrap-picker; 4 trainers.
**811 The Smokestack Parade** (`:FACTORY`): chimney-stacks and gantries, Directorate banners; the service ladder to the tallest chimney (**Sliver #2**; **Galarian Weezing "Clear Air"** static); 3 trainers (one Directorate, on a gantry).
**400 Cogsworth / 401 Center / 402 Mart**: clock-towers (the quarter chime: a BGS every 15 minutes in-game); **the plaza screen** (a big picture; the Unity Rally autorun, V137 0 → 1); townsfolk; the bathysphere works (Dive after Gym 15); the **canal** (Dive spot, **Sliver #4**); the lift-head (`NA_LIFT_STRIKE` to 830; the supply-lift close, V137 9 → 10); the `ZE_LETTERS_DOWN` commuters ×5 (gone after S146); 2 trainers. Mart: Badge-15 stock, Metal Coat, Synthetic Seed.
**[NEW] Cogsworth canteen** (interior ~21×15): long tables; Rook at the back (`:ch16_rook`, "Off Camera", his hangout until S146); the Nadir mechanic (**Varoom "Lugnut"** gift).
**[NEW] Cogsworth clock-tower** (interior, 2 floors): the clockwork stair; **Sliver #3**; Magnus's hangout (`:conscience` only).
**[NEW] Sallow's airship dock** (a small exterior on Cogsworth's heights): the `:expose` scene; Sallow's hangout (`:expose` only).
**410–414 Gym 15**: as GYM_PUZZLES (tick clock, belts, presses, crane); 6 trainers; Magnus (413); V137 = 3.
**403 Strade Works, Foundry Floor**: the side gate (Rook; the infiltration start); night-shift patrols (step-driven sight cones; a seen foreman is a battle); 3 trainers.
**[NEW] 404 Casting Floor**: molten channels (impassable animated tiles), hanging ladles; Marchetti and Quent on the gantry; **the tag battle** (V137 3 → 4).
**[NEW] 405 Drafting Vault**: blueprint-washing on lines; the long table (the ARBITER BLUEPRINTS, S144, V137 4 → 5); the copier; the waste-bin (**Sliver #5**); the core-chamber door. **Ruined state** after S145: a roof hole with rain (a weather overlay in the room), wet sheets blowing; **Magnus** (V137 6 → 7, `:ch16_magnus`).
**[NEW] 406 Engine Core Chamber**: the Lattice-glass cage, the split Dark Stone, Zekrom bound (a large event sprite with cable overlays); **Zekrom** (`:ZEKROM_ENGINE`; S145; V137 5 → 6); the control booth with the copier; **`GO_OVERTIME`** (three timed prompts; red-light tone and klaxon BGS); the bulkhead.
**220 Mirefen stilt-walks / 223 Corvin's Infirmary** (Interlude IV): rain at night; the Infirmary cots and the bead-curtained **Quiet Ward** (40 glass-edged patients as decor events; 4 sheet-cover hide events); the back ladder to the boats (6 walking patients, follow-the-leader); the radio; **2 officer battles** on the walks; **the doorway autorun** (BGM cut; cut to black; the gunshot SE; a 120-frame hold); the party and charset swap (V119 = 4 → 0; [NEW] Wenlow charset and loadout: Amoonguss, Swalot, Gastrodon Lv 62).
**Cragholm 363 field hospital** (Aftermath, `CORVIN_FREED`) or **a Directorate cell** (a small [NEW] interior, else): the aftermath vignettes; V137 = 9.

## Trainer roster (Ch16; 18 regular trainers; PBS blocks in 3 versions; ≤ 71 throughout)
| Map | Class (stock type) | Name | Lv | Team idea (field touch) |
|---|---|---|---|---|
| 801 | Worker | Scrap-picker Doyle | 67 | Garbodor, Copperajah, Klefki |
| 801 | Punk *(Guitarist)* | Vex | 67 | Toxtricity, Muk (Alolan), Weezing |
| 801 | Biker | Ratchet | 68 | Revavroom, Krookodile, Scrafty |
| 801 | Engineer *(Scientist)* | Surveyor Hale | 68 | Magnezone, Klinklang, Ferrothorn (Wasteland: Poison and Steel thrive) |
| 811 | Worker | Stoker Maeve | 68 | Coalossal, Torkoal, Camerupt |
| 811 | Scientist | Dr. Ilkley | 68 | Porygon2, Magnezone, Rotom-Fan |
| 811 | Directorate Officer *(MERIDIAN_DIRECTORATE)* | Officer Penrose | 68 | Mightyena, Corviknight, Arcanine |
| 400 | Ace Trainer | Delphine | 69 | Metagross, Gyarados, Volcarona |
| 400 | Gentleman | Mr. Cardew | 69 | Klinklang, Aegislash, Bronzong |
| **Gym 15** | Engineer ×2, Worker ×2, Scientist, Meridian Foreman | (GYM_PUZZLES) | 67–70 | as GYM_PUZZLES |
| 403 | Night Foreman *(Worker)* | Foreman Briggs | 69 | Machamp, Excadrill, Conkeldurr |
| 403 | Night Foreman *(Worker)* | Foreman Oyelaran | 70 | Copperajah, Steelix, Rhyperior |
| 403 | Engineer *(Scientist)* | Engineer Pask | 70 | Magnezone, Rotom-Heat, Klinklang |
**Story fights:** `[LEADER_ROOK,Rook,16]` partner (**added to PBS**); Marchetti v2 + Quent v1 (existing); `:ZEKROM_ENGINE` (existing); Officers Grane and Tull (new `MERIDIAN_DIRECTORATE` blocks, Lv 62: Mightyena / Houndoom / Magnezone and Arcanine / Corviknight / Muk); Wenlow's loadout (new; Amoonguss / Swalot / Gastrodon Lv 62).

**Items owner:** ARBITER BLUEPRINTS (Key Item), the TOLERANCE BADGE (proposed), TM91, DIVE, Glassfall Slivers #1–5 of the Ch16 allotment, Odessa's postbag ribbon (`ZE_LETTERS_DOWN`), Cameruptite (`AS_FORGE_REMEMBERS`, optional). **EventMons:** Varoom "Lugnut" (gift, Lv 40), Heatmor "Torch" (static, Lv 67), Galarian Weezing "Clear Air" (static, Lv 67). **Portrait requests (art, to Gemini):** **WENLOW** (the playable charset as well as the bust: `happy`, `neutral`), **SALLOW** (`neutral`, `smug`), MAGNUS `sad`.
