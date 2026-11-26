# Script: Chapter 15 — "The Hollow Cathedral" (the War Convoy; the Jawbone Ridge, Vigil, Hindmoor, Gravenmoor, Gym 14; Vane Hall; the Cathedral echo; K6; Morwen's Ring; the prisoner; Giratina)

> **Final playable script** for Chapter 15. It covers Duneholt's bazaar (201–203) and the built war maps (930 the bone-carters' camp, 926 the Glass Dunes, 925 the Steamline, 920 the Rimed Sands; 924/928 the Ashkaar Siege Camp and Command Pavilion), then the Jawbone Ridge (780), Vigil (770/771), Hindmoor (781), the Downflame Road (790), Gravenmoor (380–395: the town, Vane Hall 383, the Lantern Hospice 384 and its barrows, Gym 14 390–395), and on the way out the Noonless Road (800), the Barrow of the Wardens (804/805), Giratina's Reverse Depths (806) and the Hush (808). Built so far: 920, 924–926, 928, 930. The list at the end is what to build from.
> Follows `story/33_SCRIPT_CH14.md`. Chapter 16 ("Clear Air") follows. Sources: 07_ACT_IV Ch15, 03_CAST (Ysolde, Kestrel, Morwen, Edda, Dask, Odessa, Marisol, Teo, Anja, Eirik, Hrothgar, Ines), 09_MYSTERIES (#1 the shard, #2 Morwen's crime, #3 the night ferry, #6 Voss at the dials, #18 the Ledger), 10_CHOICES_ENDINGS (K-arc, Ruin unlock), 12_RUIN_ROUTE R1, 14_WAR_AND_BLESSING (War 2 `:war_convoy`, War 3 `:war_prisoner`, the Ch15 row), NARRATIVE_KEYS (`:ch15_kestrel`, `:ch15_look_back`, `:war_convoy`, `:war_prisoner`, `GO_ECHO`, `KESTREL_FALLEN`/`REDEEMED`), 15_COMEDY Ch15 "The Dead Are Bad at This", GYM_PUZZLES Gym 14, WALKTHROUGH Ch15, `design/CHAPTER_BEATS.md` (Ch14 density note: the convoy opens this chapter), `design/DENSITY_STANDARD.md`.

## Conventions
As in the earlier scripts. **Portrait cast here:** Ysolde, Kestrel, Dask, Odessa, Marisol (letter only; no portrait here), Teo (if `TEO_SAVED`), Anja, Juno (Circular only), Morwen (**the echo**: `MORWEN`, translucent, `neutral`/`sad` only), Edda, Sahar (one line), and the PC (two authored lines; `\pf[PLAYER,…]`). **Plain:** the caravan-mother, the sled-runners, Dominar Hrothgar (no portrait yet; `[name: Dominar]`), the Ashkaar patrol, the Gale Post courier, the lantern-priests, the echoes (Aldous, the sweeping woman, the children, Vane Hall's servant), Ines's echo (singing only; she never speaks in this chapter), every trainer.
**Gym 14** is a **double**: `Prismfall.gym_battle(pfm_gym(:LEADER_YSOLDE), double: true)` (GYM_PUZZLES; Core's gym table gets the double rule). **K6** is `Prismfall.rival_battle(:RIVAL_KESTREL, "Kestrel", 6, field: :HOLLOW_CATHEDRAL)` (versions 60–62 by starter slot), on `:HOLLOW_CATHEDRAL` (the MapDefaults rows exist). **Giratina** is the new boss key `:GIRATINA_DEPTHS` (`plugins/Prismfall Bosses/108_Boss_Giratina.rb`).
**Counter:** V136 **CH15_STEP** (new; design/FLAGS.md): 0 Duneholt: Marisol's sledges · 1 the convoy through · 2 Vigil: the Siege news · 3 Gravenmoor: Dask and Ysolde · 4 Vane Hall walked · 5 Gym 14 won · 6 the Cathedral echo (S141) · 7 K6 (S142; V114 = 3) · 8 Morwen's Ring · 9 the prisoner · 10 the Barrow of the Wardens · 11 Giratina (S143) · 12 the Hush (chapter closed; V102 = 16).
**State set here:** S141 CH15_ECHO_DONE, S142 CH15_K6_DONE, S143 CH15_GIRATINA_DONE, V114 KESTREL_STAGE = 3. Keys: `:war_convoy`, `:ch15_kestrel`, `:war_prisoner`, `:ch15_look_back`. Game over: `GO_ECHO`. Key Items: **MORWEN'S RING** (Edda), and the **TALLY-STICKS** ×3 handed in (`OS_CARTERS_DEAD`).

## The chapter's key events (design/CHAPTER_BEATS.md)
1. **The Cathedral echo.** Kestrel's Gauntlet forces the Spooky Plate to replay AF 290 through **Morwen's eyes**. It shows the brass and the dials, a young Voss, the splinter of colourless light going into a five-year-old's chest, Morwen over the child while forty people turn to glass, Valen's "Find the child", and Edda's night ferry. Then her echo turns and looks at you. This is **the central revelation of the game**. Build-up: the Pale Child (Prologue, the Mourner), Ch12's dead letter to "I.", Ch13's Mindscape, Bastian's account (Ch14). Payoff: the player knows what they are before any NPC says it aloud (Ch17 names it). Consequence: Kestrel's arc, the shard dialogue swaps, Morwen's Ring.
2. **K6.** Kestrel finds out his mother ruined her own name for the PC (`:ch15_kestrel`). Then **Giratina** in the Reverse Depths, and the Ruin Route's door. Build-up: K1–K5, "the Glassfall boy", the grandmother. Consequence: KESTREL_FALLEN / REDEEMED (the K8 path), the Festival semifinal letter, and the Ruin Route for a full Ledger.

## Density (design/DENSITY_STANDARD.md; agents build from this section)
| Item | This chapter |
|---|---|
| Story, boss and rival fights (≥4) | **The Steamline patrol** (the convoy) · **Gym 14 Ysolde** (double) · **K6** · **Giratina** (all critical) · by choice: **the cage guard** (`:war_prisoner` `:free`) |
| Route, gym and dungeon trainers (12–20) | 17 (roster at the end): Jawbone Ridge 3, Hindmoor 3, Downflame Road 2, Gym 14 6 (GYM_PUZZLES), the Noonless Road and the Barrow 3 |
| EventMons (≥3) | **Frigibax "Sledge"** (gift, the sled-runners) · **Sinistea, Antique form** (static, Vane Hall's music room) · **Bronzong "Six O'Clock"** (static, the Barrow Sanctum) |
| Hangouts (2–4) | Ysolde at the Lantern Hospice · Edda at the Hindmoor staithe · Odessa at her skiff |
| Glassfall Slivers (4–6) | 5: the Jawbone Ridge cairn, a Hindmoor standing pool, Vane Hall's nursery window, the Noonless Road milestone, the Hush |
| Trials quests (≥3) | `OS_CARTERS_DEAD` (completes in the Steamline) · `AN_GIMMIGHOUL_COINS` (Gravenmoor) · new **`AN_ALDOUS_DOOR`** (the comedy echo) · `AN_BEHIND_THE_GLASS` opens after S143 |
| Badge overlay | Badge 14: `encounters_badgetiers.txt` tier for 780, 781, 800, 804 |
**No jokes** from the Cathedral echo (V136 5 → 6) to the end of the chapter, except Edda's one dry line at the grave, which isn't a joke. "The Dead Are Bad at This" plays before the gym. **No side content** opens between the Cathedral and the end of K6.

---

# CHAPTER 15 — "The Hollow Cathedral"

**Chapter start:** V102 = 15, V136 = 0. First light in Duneholt. The quest log "Eighteen Roads": *North to Gravenmoor. (First: Marisol's sledges.)*

## Duneholt, the bazaar at first light: **War 2, the War Convoy** (touch, the green awnings, V136 == 0)
```
(The Terrace Bazaar before the stalls open. Under green awnings: twelve sledges on sand-runners, roped and tarped. Ebb Guild sled-runners in Isenmar oilskins, too hot, not complaining. At the head of the line, an old caravan-mother on a camel, veiled, holding a lantern that's already out.)
[name: Caravan-mother] The Unimprinted. Good.
[name: Caravan-mother] My house leads you to the glass. Past the glass, the glass is yours.
[name: Sled-runner] (a letter, handed over) Captain Reyes says read it before you decide.
[name: Sled-runner] Then decide quick. Siege closes tonight.
(The letter, in Marisol's square hand.)
"Two cargoes in the bazaar. I bought both. Under the left tarps, food: grain, salt-fish, milk powder for the Skaldfast creche. Under the right, harpoon-guns from the Ebb yards. Skaldfast's walls hold three days on either. Not both: the sledges won't take both through the steam.
 Whichever you walk in, I'll stand behind. Whichever you leave, my people sell back to the bazaar, and the caravan-mothers give it to the refugees here.
 Nobody shoots the Unimprinted. Prove it. — M."
```
```
> Walk the food in. (relief)
  Script: pf_choose(:war_convoy, :relief)
  [name: Sled-runner] (uncovering the left tarps) Milk powder. Fifty sacks of it.
  [name: Sled-runner] The Thane'll hate it. The creche won't.
> Walk the guns in. (arms)
  Script: pf_choose(:war_convoy, :arms)
  [name: Sled-runner] (quietly) Right. Harpoons. Skaldfast'll hold.
  (A beat.)
  [name: Sled-runner] Somebody on the other side won't.
> I won't walk a war. (refuse)
  Script: pf_choose(:war_convoy, :refuse)
  [name: Caravan-mother] Then the bazaar eats today. That's not nothing, child.
  (She turns the camel.)
  [name: Caravan-mother] Marisol will be angry. Marisol is often angry.
  [name: Caravan-mother] The bazaar is often hungry.
  (Skip to "Odessa's skiff" below; the Steamline still opens for `OS_CARTERS_DEAD`.)
V136 = 1 on :relief/:arms after the walk below; V136 = 1 immediately on :refuse.
```
*(NARRATIVE_KEYS: `:relief` MARISOL+2 RES+1; `:arms` MARISOL+3 SIGRUN−2 RES−1; `:refuse` MARISOL−2. `:relief` is one of the Blessing's war conditions.)*

### The walk (on `:relief`/`:arms`: 930 → 926 → 925; a follow sequence)
The caravan-mother leads the line west across the Dry Tide and the Glass Dunes (926) to the **Convoy marker** at the Steamline's edge (925). There she stops and turns her camel round: "Past the glass, the glass is yours."
- **Stage direction:** the PC walks point into the steam. The sledges follow the PC's footprints exactly (a recorded-path follower: the same echo mechanic as Gym 14's crypt, built once and used twice). Where the PC steps, the steam thins and the Bleed's flicker stops for a tile around them. Step off the line and the sledge behind stops and creaks.
- The Steamline's built events play as written (the frozen flood, the ice-locked whaleboat, the sentries). **`OS_CARTERS_DEAD`**: the three remains markers are on this map. Each is a body in the glass with a tally-stick on a cord. The PC breaks each one free (an interact plus a short flash). They're all different: an Isenmar boy in oilskins, an Ashkaar legionary with a dragon-scale amulet, and a third with no uniform at all. That last one is a well-woman from Duneholt, which nobody had counted.
- **The patrol (critical on `:relief`/`:arms`).** Halfway across, an Ashkaar dragon patrol drops out of the steam.
```
(Wingbeats. A Dragonite lands across the path, steam boiling off its wings. Two riders in dragonhide.)
[name: Ashkaar Rider] Halt! Sledges into Skaldfast. Under whose banner?
[if :relief]
  [name: Ashkaar Rider] Food, the runners say. Everyone says food.
  [name: Ashkaar Rider] Show me, or show me your Pokémon.
[if :arms]
  [name: Ashkaar Rider] Food, the runners say.
  (He lifts a tarp with his spear. Harpoon-steel.)
  [name: Ashkaar Rider] ...Food. Draw.
BATTLE: TrainerBattle.start(:ASHKAAR_OFFICER, "Rider Torvald", :ASHKAAR_SOLDIER, "Rider Esk") — double; `:BLEED` (the Steamline's own field); Lv 64–65.
(LOSE: whiteout to 201; the convoy waits at the marker.)
[if :relief]
  [name: Ashkaar Rider] (looking at the milk powder) ...Go on.
  [name: Ashkaar Rider] Dominar's orders are "no arms past the glass".
  [name: Ashkaar Rider] He never said anything about milk.
[if :arms]
  [name: Ashkaar Rider] (bleeding, furious) The Dominar will hear the Unimprinted carry harpoons now.
  [name: Ashkaar Rider] Remember who you used to be.
  (They go up into the steam.)
```
- **The Rimed Sands (920), Isenmar's lines.** The sledges come out of the steam into the trenches. Sled-runners cheer, very quietly, because there are snipers.
  - `[if TEO_SAVED]` **Teo** is at the trench-head with a clipboard and a scarf over his face, organizing the handover: "Marisol said you'd come. She said it like a threat. Get the sledges into the ditch, I'll get them over the glacier tonight." A beat. "...Thanks. For the Fault, too. If that was you. Somebody said it was you."
  - **Gift: Frigibax "Sledge"** (Lv 35, Thermal Exchange), from a sled-runner: "Ashkaar's got dragons. Isenmar's got one. It hates the cold, and it hates dragons, and it pulled a sledge all the way here out of spite. Take it. It likes you, and I'm not sure it likes anybody."
```
V136 = 1.
```

### Odessa's skiff (autorun at the Rimed Sands lookout, V136 == 1; on `:refuse`, at Duneholt's Gale Post)
```
(A Gale Post skiff comes down out of the white sky on a long rope, rocking, and Odessa leans over the gunwale in flying goggles.)
[portrait: ODESSA, happy] Mail's mail! Get in.
[name: Odessa] You're overdue at a graveyard, and I've a sack for Vigil that won't deliver itself.
[portrait: ODESSA, neutral] (as the skiff lifts, looking west at the smoke) I fly both sides' mail now.
[name: Odessa] Same sack. I read nothing. I know everything.
[name: Odessa] You'd be amazed what a war says in its letters home.
[name: Odessa] (as the Jawbone Ridge comes up under you) If they take somebody worth fetching, I'll come back for you.
[name: Odessa] Don't make that face. They will.
```
**Hangout, Odessa at the skiff** (from V136 >= 2; at Vigil's Gale Post mooring, later Gravenmoor's): *Mail Call*, a postbag of letters from the war, read in her voice, one per visit. It also offers fast travel back to Duneholt and the Rimed Sands.

## Map 780 — the Jawbone Ridge (`:MOUNTAIN`)
A ridge of white rock like the jaw of something huge, with teeth. To the west, the war's smoke stands on the sky in a long brown wall. To the north, Antumbra's fog. The Darkglass Mine's headframe (784) stands on the crest, boarded up since the raid, with a Directorate notice nailed to it and a Lantern Hollow lantern hung on the notice.
- At the cairn on the highest tooth: **Glassfall Sliver**.
- A hiker with a telescope: "That's Skaldfast under the smoke. You can see the dragons go round it, very small, like flies round a lamp. I can't stop watching. I've tried."
Trainers (Lv 63–64): a hiker, an Ace Trainer, a dragon tamer (an Ashkaar deserter, out of uniform: "I'm not deserting. I'm *going home the long way.*").

## Vigil: **the Siege news** (autorun at Vigil's Center, V136 == 1 → 2)
```
(Vigil's Center. A Gale Post courier, white with road dust, is pinning a sheet to the board while a crowd reads over his shoulders.)
[name: Courier] THE SIEGE OF SKALDFAST.
[name: Courier] Ashkaar's dragons have ringed the fortress and burned the sled-road on the Mast Glacier. The Ebb Guild is running sleds over the glacier from Anchorhold by night.
[name: Courier] A sortie on the Rimed Sands, repulsed. Taken by Ashkaar...
(He reads the list. The crowd goes quiet at one name.)
[name: Courier] ...Warden Anja Sorrel of Rimeholt.
[name: Courier] (to you, lower) Gale Post says you knew her. I'm sorry.
[name: Courier] She went west from the seams, didn't she. With a list.
QUEST LOG: "The Taken" — Anja is held in the Ashkaar Siege Camp. Odessa says she'll come back for you.
V136 = 2.
```
*(`:war_prisoner` is decided after Edda's grave (step 9), when Odessa comes back. It's on the critical path, because Anja's pre-Festival scene depends on it.)*
- The Wardens' Circular at Vigil's board: Sahar: "Duneholt's well is at four feet and rising. I'm not crying, it's the dust." Kaito: "Congratulations." Sahar: "I said it's the dust."

## Map 781 — Hindmoor (`:INVERSE`) and Map 790 — the Downflame Road
Hindmoor: heather and fog, the border stones where Pip turned back, and **standing pools** that show what's behind you, not above you. Looking into one shows the road you came by, and in the deepest one, a ferry at night. (On examining that pool: *"(A ferry, small and far off, going out over black water. Somebody at the rail is holding a child.)"* The PC can't look away for a second. Then it's just a pool.)
- **Glassfall Sliver** at the bottom of the shallowest pool (Dive is not needed; the pool is only ankle-deep, it just *looks* bottomless).
- **Hangout, Edda at the Hindmoor staithe** opens after the grave (V136 >= 8): the *Dovetail* is tied up where the moor river meets the sea-lochs. She has been running smuggled mail and medicine in and out of Antumbra since the quarantine. See "The grave" below.
- The Downflame Road (790): a road that runs **downhill in both directions**, an Inverse joke the land is making. Lantern-posts with real flames burning **downwards**.
Trainers: Hindmoor (Lv 64–65): a hex maniac, a black-belt pilgrim, a punk; the Downflame Road (Lv 65): a gentleman, a psychic.

## Gravenmoor: **"Louder"** (autorun at the town gate, V136 == 2 → 3)
```
(Gravenmoor. A town of grey slate and lanterns, built among barrows. Fog in the streets thick enough to lose your feet in. Everywhere, faint and grey, the echoes: a woman sweeping a step that isn't there; two children playing a game, the same three moves over and over; a man waving at a wall.)
(At the gate, waiting, an old man in a veil of mirror-chips: Archseer Dask.)
[portrait: DASK, neutral] You came by the road. Good.
[name: Dask] Roads are honest. Mirrors are not.
[portrait: DASK, sad] The echoes are louder. Louder, the echoes.
[name: Dask] Since the Fault, since the boy came with his brass glove.
[name: Dask] Something behind the Glass is listening back.
[portrait: DASK, neutral] (looking at you, which he never does) You still haven't looked back.
[name: Dask] Good. Keep not doing it.
[name: Dask] One day you'll have to decide whether that's a rule or a habit.
(He walks off into the fog, and the fog doesn't seem to notice him go.)
```
*(Dask's second encounter. 12_RUIN_ROUTE R1 calls back "you looked; I told you never to look", so this scene must play.)*
```
(Further in, under a lit lantern on a pole, a pale woman in layered black lace, veiled, the lantern held up as if she's been holding it for a long time.)
[portrait: YSOLDE, neutral] You're the ferry child. I've been waiting for you. And for him. He's come in on the white ship. He went straight up the hill.
[portrait: YSOLDE, sad] Vane Hall. His home.
[name: Ysolde] Nobody's lived there since AF 290 except the dust and the... well. You'll see.
[portrait: YSOLDE, neutral] The dead aren't gone here.
[name: Ysolde] They're just very bad at conversation.
V136 = 3.
```
- **Comedy scene Ch15, "The Dead Are Bad at This"** (touch, Ysolde by the waving man; available V136 3–5; 15_COMEDY as written). After "Hello, Aldous", **`AN_ALDOUS_DOOR`** opens (new; see Optional).
- **Gravenmoor (380–382):** the Center (381), the Mart (382; Badge-14 stock plus Spell Tag and Reaper Cloth), the Synod lantern-priests ("Since the Fault they've started *noticing* us. A child echo asked me the time yesterday. I told her. She said 'thank you'. In two hundred years she's never said thank you."), and `AN_GIMMIGHOUL_COINS` (a lantern-priest at the collection plate).
- **The Lantern Hospice (384)**: where Antumbra sends the dying to be near the Glass. **Hangout, Ysolde at the Hospice** (from V136 >= 3): she reads to patients who can't hear her. Late at night they're echoes, and they can.

## Vane Hall (383, `:HAUNTED`-style interior with the `:HOLLOW_CATHEDRAL` field; touch at the gate, V136 == 3 → 4)
The sad haunted house. Dust-sheets, a hall clock **stopped at 11:40**, and the echoes of *his family*. The puzzle path (World/puzzle team): five rooms, each replaying the night of AF 290 from the household's side. The doors open in the order the night happened. The **clock hands** in each room show which room comes next (11:00, 11:10, 11:25, 11:35, 11:40).
```
(Vane Hall. Kestrel is standing in the entrance hall in his sponsor jacket, the Gauntlet on his left arm, looking at the stairs. He doesn't turn round.)
[portrait: KESTREL, neutral] Go away.
(He doesn't move. Neither do you.)
[portrait: KESTREL, angry] Fine. Don't touch anything.
```
Rooms (each an echo, then a door):
1. **The parlour, 11:00.** A grandmother, younger, laughing at a card game. Kestrel: "...She laughed. I forgot she did that."
2. **The nursery, 11:10.** Morwen in a chair, reading to a boy of six in a nightshirt: a story about a ferryman. Kestrel stops in the doorway. "That's my room. That's — don't touch that." *(A model ferry on the windowsill. Behind it: **Glassfall Sliver**, which the PC can take only after Kestrel has left the room.)*
3. **The study, 11:25.** Morwen at a desk, writing a letter, crying without making a sound. She seals it. She writes on the front: *Kestrel, when he's ready.* Kestrel takes a step towards the desk and the echo is gone.
4. **The servants' stair, 11:35.** A maid's echo at the window: "The Warden's not back yet. Ma'am, the Warden's not back yet." The old woman's voice from offstage: "Then lock the doors."
5. **The hall, 11:40.** The front door bangs open. Nobody comes through it. The clock stops. Kestrel, very quietly: "She never came back. They said she was at the Festival. They said she did a terrible thing. Then they sold the horses."
- **The music room** (optional; off the parlour): a tea service on a dust-sheeted piano. One cup is warm. **Sinistea (Antique form)** (static, Lv 64, Cursed Body; the authenticity mark under the cup: "*V.H. AF 211*").
```
(Back in the hall. Kestrel, at the door, without looking at you.)
[portrait: KESTREL, neutral] Voss says it's all in the Cathedral. The whole night. Recorded.
[name: Kestrel] And I've got a glove that can play it back.
[portrait: KESTREL, angry] Go and get your badge. I'll be waiting at the altar.
[name: Kestrel] You're going to watch it with me.
V136 = 4.
```

## Gym 14 — the Hollow Cathedral (390–395, `:HOLLOW_CATHEDRAL`)
As GYM_PUZZLES Gym 14: 390 Narthex (teach: the bell-rope worlds), 391/392 the Living and Dead Naves (twist: pews bridge crypts), 393 Requiem Crypt (combine: **Morwen's echo** replays your last 12 steps and holds a plate), 394 the arena, **395 Morwen's Chapel** (Mastery, optional). Gym trainers (6): Channeler ×3, Gentleman (revenant), Lady, Mourner-acolyte; they're in 392 only; Lv 63–66.
- **Ysolde at 390:** "Whatever you move among the living, the dead must walk around. Mind the candles. Some of them are people."
- **393, the first time the echo walks:** *(The grey figure that follows your steps is a woman in a Warden's coat. She has no face you can see. She stops on the plate and stays, patiently, as if she's done this before.)*
- **Mastery (395), resolved against 07_ACT_IV:** the chapel's reward is Magical Seed ×2 and a Spell Tag, plus the chapel's **lectern text** (Morwen's prayer, below). **Morwen's sealed letter is not given to the PC**: it's kept in the chapel, and Ysolde takes it from there after K6 to offer to Kestrel. (GYM_PUZZLES listed the letter as a Mastery reward; this script supersedes that, so the letter returns at the Festival semifinal as designed.) Lectern: *"Keep him. Keep the other one. Keep the ferryman's lamp lit. I will carry the name. — M."*

### 394 — the Warden Arena (double)
```
[portrait: YSOLDE, neutral] Morwen taught me in this room. She'd stand there, where you are.
[name: Ysolde] She said the dead fight beside the living here, so you'd better be worth fighting beside.
[portrait: YSOLDE, sad] I'm going to fight you, and then he's going to do something I can't stop.
[name: Ysolde] I want you to know I tried. Win, please. It'll be easier for you after.
BATTLE: Prismfall.gym_battle(pfm_gym(:LEADER_YSOLDE), double: true)
```
- **Mid-battle (Sableye Mega Evolves):** "She'd have liked you. She liked anyone who wouldn't stay down." `[bubble: YSOLDE, sad, sparkle]`
- **Win:**
```
[portrait: YSOLDE, neutral] There. Morwen's room has a new name in it.
RECEIVE: the KNELL BADGE (badge 14). RECEIVE: TM30 SHADOW BALL.
(Up in the nave, very faint, a Choir is tuning. Ysolde's lantern flickers.)
[portrait: YSOLDE, panic] [emote: exclaim] He's started. Come on.
V136 = 5.
```
*(Badge name, proposed: the **Knell Badge**. The VS plate reads LANTERN PRIEST above YSOLDE.)*

## The Hollow Cathedral: **The Echo** (autorun in the Living Nave, V136 == 5 → 6; key event 1; no jokes from here to the end of the chapter)
**Cutscene: `CE-1` "AF 290, Through Her Eyes"** (new; 13_CUTSCENES). It needs the letterbox, the grey-sepia tone, the echo tint and the bell SE. Stage directions in brackets are animations, per the `[anim]` rule (design/MAPGEN.md): emotes, move routes, tone and flash, never text the player reads.
```
(The nave. Candles. Kestrel at the altar, the Gauntlet on his raised left arm, its lattice of glass glowing white. The Spooky Plate's niche behind the altar glows back at it.)
[portrait: YSOLDE, sad] Kestrel. Not like this.
[name: Ysolde] She made me swear — when you were ready —
[portrait: KESTREL, angry] Ten years, Ysolde. "When he's ready."
[name: Kestrel] I'm ready. Watch me be ready.
(He closes his fist. The Gauntlet screams like a tuning fork. Every candle in the Cathedral leans towards the altar.)
[anim: screen tone → grey-sepia; letterbox in; the nave's walls dissolve into an arena]
```
*(The echo. Every line here is the echo's: the world speaks in short, plain story text. The PC sees it whatever they chose in Ch13. If `choice(:ch13_remember) == :not_yet`, a single extra line plays first: "(You said 'not yet'. The Cathedral doesn't ask.)")*
```
(Crownhaven's arena, ten years ago, from high in the stands, through someone's eyes. Bells. The Choir in white, eighteen of them, and in the front row a young woman with her hair pinned up, singing: Ines.)
(The eyes we're seeing through turn: behind the Choir loft, half-hidden, big brass machines with dials. Little gold sunburst plates. Men in white coats.)
(One of them is young and eager and leans in to read a dial, and pushes his hair out of his eyes: Aurelian Voss.)
(The Crown on Valen's head, eighteen Plates around it, begins to glow. The Choir's note rises. The dials climb.)
[anim: white flash; bell-crack SE]
(A sound like a bell breaking.)
(A splinter of colourless light flies out of the Crown, very fast, across the whole arena, and goes into the chest of a child of five in the front of the Choir. A little thing in a Choir ribbon. The child doesn't even fall down. The child just stands there, glowing.)
[anim: the Glassfall: a white wave rolls down the lower stands from left to right; people stop, mid-movement, and turn to glass]
(The eyes run. Down the stairs, against the crowd. The Glassfall sweeps the lower stands and forty people turn to glass, one after another, so close you could touch them.)
(The eyes reach the child and the world goes dark: she's thrown herself over the child, a Warden's coat over both of them, and the light goes over.)
(Through the light, on the dais, Valen, on his knees, the Crown cracked on his head:)
[name: Valen] Find the child. Whatever it costs. Find the child.
[anim: cut; tone darker; a small stone room]
(A vestry. A woman in a Warden's coat kneeling by the child, who is asleep now and still faintly glowing. Ines at the door, shaking.)
[portrait: MORWEN, neutral] Take them. Edda's boat is at the Landing at midnight.
[name: Morwen] I'll carry the name. Go.
[name: Ines] (a sound, not a word)
[portrait: MORWEN, sad] Go.
(A Mismagius rises out of the dark, gently, and lays a hand over the sleeping child's eyes, the way you'd close a curtain.)
(Ines takes the child. The door closes.)
(Morwen alone in the vestry, kneeling, to no one:)
[name: Morwen] Kestrel. I'm sorry.
[anim: silence, 60 frames; then the echo stays and the tone half-returns]
(And then, impossibly, the echo turns her head. Across the nave. Across ten years. She looks straight at you.)
[portrait: MORWEN, neutral] [emote: dots] Little one. You came back.
[name: Morwen] I told her not to let you.
[anim: the echo fades; letterbox out; tone back]
Switch S141 CH15_ECHO_DONE = ON. V136 = 6.
```
*(09 #1/#2/#3/#6. Never name the shard, the reset or the Legend Plate (Ch17). "Little one" is Morwen's, and only Morwen's, name for the PC. The Mismagius closing the child's eyes explains the amnesia, and the first thing the PC remembers is the ferry (Prologue).)*

### ☠ **`GO_ECHO` "Echo"** (Choir loft, available only between the echo and K6)
After the echo, before Kestrel turns: a faint singing from the loft. **Ines's echo**, singing the Choir's note, alone.
```
(An echo is still singing in the Choir loft. A young woman with her hair pinned up. She's singing the note from before it broke.)
> Stay and listen?
  > Stay. (1st)
    (You stay. It's the most beautiful thing you've ever heard, and you've heard it before.)
  > Go.  — (on to K6)
> Stay and listen? (2nd; only after the 1st)
  [portrait: YSOLDE, panic] (from very far off) Echoes are a door that only opens one way —
  (Your hand on the loft rail is translucent. You can see the rail through it.)
  > Stay. (2nd)   > Go.
> Stay and listen? (3rd)
  > Stay.  Script: Prismfall.game_over(:GO_ECHO)
  > Go.
```
*(NARRATIVE_KEYS §9: epitaph "You stayed for the song. Gravenmoor has one more echo now. It sings harmony." The translucent hand is a tone/opacity change on the player sprite.)*

## **K6** (autorun when the PC leaves the loft or the altar step, V136 == 6 → 7)
```
(Kestrel is standing where the echo was. The Gauntlet is smoking. He's looking at you like he's never seen you before, which, in a way, he hasn't.)
[if choice(:ch12_letter) == :send]
  [portrait: KESTREL, angry] You sent me her *letter*. Her letter to that woman.
  [name: Kestrel] And you still came here.
[portrait: KESTREL, angry] My whole life for you.
[name: Kestrel] Do you know what they called me in school? The Glassfall boy.
[name: Kestrel] My grandmother spat on her grave. Spat on it. I watched.
[name: Kestrel] And she was saving YOU.
(The Gauntlet flares. The nave's candles gutter all at once.)
BATTLE: Prismfall.rival_battle(:RIVAL_KESTREL, "Kestrel", 6, field: :HOLLOW_CATHEDRAL) — `:HOLLOW_CATHEDRAL`; the Gauntlet overloads once (below).
(LOSE: the rival rule: the story continues, and Kestrel's line below swaps to "Stay down. Stay down. She'd have wanted you to stay down.")
```
- **Mid-battle (on the turn his 4th Pokémon enters), the overload:** "Kestrel's Gauntlet is overloading!" The field flickers to `:BLEED` for one turn, then back to `:HOLLOW_CATHEDRAL` (`battle.change_field(:BLEED)` for 1 turn via a battle-script hook; the MapDefaults rows already note it). `[bubble: KESTREL, angry, shock]`
- **On his ace (Aegislash "Morwen"):** "It was your mother's blade's child. That's what Grandmother said. She lied about everything else. Did she lie about that too?" `[bubble: KESTREL, sad]`

**After K6: the PC speaks (`:ch15_kestrel`, the PC's third authored line in the game)**
```
(He's on his knees on the altar step, recalling Aegislash. He doesn't look up.)
> "I'm sorry. I didn't know. I'd give it back if I could." (sorry)
  Script: pf_choose(:ch15_kestrel, :sorry)
  \pf[PLAYER,sad] I'm sorry. I didn't know. I'd give it back if I could.
  [portrait: KESTREL, sad] (a long time) ...You can't.
  [name: Kestrel] That's the whole problem. You can't.
> "I was five. She chose. Don't you dare make her choice my crime." (she_chose)
  Script: pf_choose(:ch15_kestrel, :she_chose)
  \pf[PLAYER,angry] I was five. She chose. Don't you dare make her choice my crime.
  [portrait: KESTREL, angry] (he looks up, and for a second, something in his face is almost relief) ...There you are.
  [name: Kestrel] I wondered if there was anybody in there.
> "...Your mother saved my life. I'm going to make it worth it." (resolve)
  Script: pf_choose(:ch15_kestrel, :resolve)
  \pf[PLAYER,neutral] ...Your mother saved my life. I'm going to make it worth it.
  [portrait: KESTREL, neutral] (he stands up) Then you'd better. You'd better.
(He walks out of the Cathedral without another word. The door doesn't bang. That's worse.)
Switch S142 CH15_K6_DONE = ON. Variable V114 KESTREL_STAGE = 3. V136 = 7.
```
*(NARRATIVE_KEYS: `:sorry` KESTREL+1 YSOLDE+1, and +3 at the semifinal if not Fallen; `:she_chose` KESTREL−2, which unlocks the Redeemed path at K8 because he respects being fought back; `:resolve` KESTREL+2 YSOLDE+2 RES+2. See KESTREL_FALLEN for the full gate.)*

### The moor's edge (autorun outside, the PC watching from the Cathedral steps)
```
(Down the hill, at the edge of the moor, in the fog: Kestrel walking fast. Ysolde catching him up with her lantern. You can't hear them. You can see them.)
(She holds out a Poké Ball. He looks at it. He takes it. Inside, for a second, a shape in a witch's hat.)
(She holds out a sealed letter. He looks at it for a long time. He doesn't take it. He walks on into the fog.)
(Ysolde stands there with the letter. Then she puts it inside her coat, very carefully, like something that could still break.)
[portrait: YSOLDE, sad] (later, on the steps, to you) She made me swear. "When he's ready."
[name: Ysolde] I don't think anyone is ever ready. I'm sorry I waited.
(A pause.)
[name: Ysolde] I'll keep it. I'm good at keeping things.
[name: Ysolde] It's the only thing I'm good at.
```
*(Morwen's Mismagius goes to Kestrel (his team from K7). The sealed letter returns at the Festival semifinal.)*

## The barrows below the Lantern Hospice: **Morwen's Grave** (touch, a kneeling figure, V136 == 7 → 8)
```
(The barrows under the Hospice. Rows of stones. One is plain and small and cut with two letters: M.V.)
(A squat old woman in a sea-coat is kneeling at it, laying kelp-flowers, wet and green, on the stone. A gold tooth. A Lapras inked on her forearm.)
[portrait: EDDA, neutral] Sprog.
[name: Edda] (not getting up) I took you out on the night ferry. Brought you back on the last one.
[name: Edda] Tide's got a sense of humour.
(A beat.)
[name: Edda] She paid me in her Warden's ring. Hers. Off her own hand.
[name: Edda] I never sold it. Twenty different times I nearly did. Couldn't.
(She holds it out: a heavy ring of black glass and silver. In the black glass, very faint, the same colourless chip as yours.)
[portrait: EDDA, sad] Her boy should have it. I'm a coward about boys.
[name: Edda] You give it to him. When you think he'll not throw it in the sea.
RECEIVE: MORWEN'S RING (Key Item).
[portrait: EDDA, neutral] (getting up, knees cracking) The Dovetail's at the Hindmoor staithe.
[name: Edda] Smuggling, these days, since they took my licence.
[name: Edda] Mail, medicine, the odd Warden. Come and see me.
[name: Edda] Don't tell anyone. Tell everyone.
V136 = 8.
```
*(Morwen's Ring is for Kestrel in Ch18 (`:ch18_kestrel_ring`); it's the only way his Scizor Mega Evolves, at K8. "Sprog" is what she called the PC in the Prologue.)*

## **War 3, The Taken** (`:war_prisoner`; Odessa's skiff at Gravenmoor's mooring, V136 == 8 → 9)
```
[portrait: ODESSA, neutral] Told you. Somebody worth fetching. Get in.
[name: Odessa] We'll fly over the lines; from the drop it's a short walk across the sands.
[name: Odessa] I don't land in camps. Camps shoot at things that land.
```
The skiff drops the PC on the Glass Dunes (926). A short walk to the **Ashkaar Siege Camp** (924, built), then the **Command Pavilion** (928, built).
```
(The Command Pavilion. A lacquer map table. The oath-brazier, white at the heart. An empty stand of black glass, dusty, where something round and heavy sat until recently. In an iron hawk-cage made larger: Anja, in her furs, sitting very straight.)
[name: Dominar] Speak plainly. The brazier is lit.
[name: Dominar] In this tent a lie is a death sentence, and I have signed eleven.
[name: Dominar] The Unimprinted. My daughter's friend, they tell me, and the Thane's sister's.
[name: Dominar] Everyone's friend. Have you come to buy a Warden?
[portrait: ANJA, neutral] (from the cage, without turning) Tell my brother I'd have signed for the heaters again.
[name: Anja] Tell him that first. Then whatever this is.
```
```
> Free her. (free)
  Script: pf_choose(:war_prisoner, :free)
  (Night. The camp asleep, apart from the guard at the cage, who isn't.)
  BATTLE: TrainerBattle.start(:ASHKAAR_OFFICER, "Cage-Warden Hesk") — single; `:BLEED`; Lv 67.
  (LOSE: whiteout to 381; Odessa will fly you back.)
  (You walk her out through the Steamline the way you walked the sledges, in your own footsteps, with the Bleed quiet round you both.)
  [portrait: ANJA, neutral] (at the Isenmar lines, not looking back) Every time someone saves me, I owe them a count I can't pay.
  (A beat.)
  [name: Anja] I'll start a new ledger. Yours is the first line.
> Broker an exchange. (exchange)
  Script: pf_choose(:war_prisoner, :exchange)
  (Dawn, a caravan well between the lines. The bone-carters' white banner over it. Elder Ossa and Zainab Darzi at the well-head. Isenmar riders on one side with a young Ashkaar noble in chains; Ashkaar riders on the other with Anja.)
  [name: Zainab] No blood at a well. That's the oldest law in the sand, older than both your crowns. Walk them across. Slowly.
  [name: Zainab] I'm writing this down.
  (The Dominar's nephew walks east. Anja walks west. They pass each other at the well. Neither of them looks at the other. Both of them look at the water.)
  [portrait: ANJA, neutral] (passing you) That's the first time those two crowns have agreed on anything since AF 290.
  [name: Anja] Write that down too.
> Leave it. (leave)
  Script: pf_choose(:war_prisoner, :leave)
  [name: Dominar] Wise. Or cold.
  [name: Dominar] The brazier can't tell the difference. Neither can I.
  [portrait: ANJA, sad] (as you go, very quietly) Count it. Somebody should.
V136 = 9.
```
*(NARRATIVE_KEYS: `:free` RES+1 ACCORD−1; `:exchange` ACCORD+2; `:leave` RES−1. `:war_prisoner != :leave` is a Blessing war condition. The empty stand is something the Dominar had brought out of Cindervault, whatever was on it (09; Act V). Don't explain it here.)*
- Odessa's skiff, back to Gravenmoor: "Mail's mail. People are mail too, if you squint."

## Optional around Gravenmoor (from V136 >= 3; shut between the echo and the end of K6)
- **`AN_ALDOUS_DOOR`** (new; rank 2, 3 pts; giver: Ysolde, after "Hello, Aldous"): Aldous waves at where his door *used to be*. The town plan of AF 211 is in the Hospice archive. The PC finds the old door's position (a barrow-stone now) and leans the old door, found in Vane Hall's cellar, against it. At six o'clock Aldous waves at the door, and it **opens**, and he goes through. *(It's the only echo in the game that leaves.)* Ysolde: "Oh. Oh, he's gone. That's — I'll miss him. Isn't that ridiculous. Nobody's ever left before." Reward: Reaper Cloth, Cleanse Tag ×2. *(This plays before the Cathedral. It's not a joke, so the no-jokes rule doesn't bar it after.)*
- **`AN_GIMMIGHOUL_COINS`** (stub as catalogued; Gravenmoor 380).
- **Hangout, Edda at the Hindmoor staithe** (V136 >= 8): *The Dovetail's Hold*, smuggled cargo with a story each visit (the medicine for the Hospice; a crate of Isenmar letters; "the odd Warden" turns out to be Juno's Circular in a bottle). It also sells Deep Sea items.

## Map 800 — the Noonless Road (`:INVERSE`) and the Barrow of the Wardens (804/805)
The road north-east out of Gravenmoor, towards Cogsworth. It's never noon on it: the sun stands at a quarter to all day. A milestone reads "NOON, 1 MILE", and always will. Behind it: **Glassfall Sliver**.
Trainers (Lv 67–68): a medium, a hex maniac, and a revenant gentleman (in the Barrow).

### The Barrow of the Wardens (804; touch at the barrow-door, V136 == 9 → 10)
A long barrow under the moor where generations of Wardens are buried, each with a **replica of their Plate** on their breast in grey glass. Eighteen alcoves on each side, centuries of them.
- Reading the replicas (optional, 18 inscriptions) tells three hundred years of Warden history in single lines. ("Warden of Ebbmouth, elected. She was voted out the year she died, and won the recount posthumously.")
- **The Barrow Sanctum (805), the Bell of AF 211**: a bronze bell hung from the barrow roof. At six o'clock it rings itself once. Ring it at six and it opens its eyes: **Bronzong "Six O'Clock"** (static, Lv 66, Heavy Metal). *(Callback: Aldous, AF 211, "every evening at six". In the Barrow, a gravestone: "ALDOUS — who said hello.")*
- **The barrow-door into the sky:**
```
(At the end of the barrow, a stone door in the floor. You open it. It opens downward. On the other side, below your feet, is sky: grey, upside-down, going down forever.)
(And somewhere in that sky, something enormous is moving.)
V136 = 10.
```

## Map 806 — Giratina's Reverse Depths (`:INVERSE`): **Boss: Giratina** (touch at the torn pane, V136 == 10 → 11)
The Depths: floating islands of black rock in an upside-down sky, waterfalls going up, trees growing down. Wild Pokémon at Lv 66–70 (WALKTHROUGH). At the centre, a tear in the air like a crack in a mirror, bleeding grey light.
```
(The tear is open. Through it you can see the Cathedral nave, the candles, an altar step. The tear is getting wider. Something pulls it wider from the other side.)
(A shape like a shadow with a crown of ribs drags itself halfway through the tear and turns its red eyes on you. It's furious. It's hurt. Along its side, a long grey wound like glass.)
BATTLE: Prismfall::Bosses.wild_battle(:GIRATINA_DEPTHS) — 3 bars (Casual 2), Lv 70; Altered, then Origin on the last bar; `:INVERSE`.
(LOSE: whiteout to 381; the boss restarts at bar 1.)
```
```
(It doesn't flee.)
(It looks at you: the way the sea-beast in Isenmar looked at you, and the red one under the sand. A long, flat look. It knows what you carry. It has been guarding the hole your god left for three hundred years.)
(It turns its back on you, takes the edges of the tear in its claws, and pulls them shut, slowly, like a sailor mending a net. The grey light goes out.)
(The wound along its side doesn't close. It goes back into the dark with it still open.)
Switch S143 CH15_GIRATINA_DONE = ON. V136 = 11.
```
*(The wound is why other-world visitors keep slipping into Velmora: the cameo quests, design/CAMEOS.md. Post-game: the Distortion Core. S143 opens `AN_BEHIND_THE_GLASS` in Lucent.)*

### **`:ch15_look_back`** (only if `ruin_unlocked`; touch, a black pane at the Depths' far edge)
```
(At the far edge of the Depths, a pane of black glass stands on its own, like a door with no wall.)
(In it, Juno. On the other side of the glass, calling your name. Waving. Laughing. Exactly the way she was in Lucent, on the stair, when Dask said never to look back.)
(You know this picture. You've died in it.)
> Look back? (yes)
  Script: pf_choose(:ch15_look_back, :yes)
  (You look.)
  (Nothing happens to you.)
  (The reflection lowers her hand. Steps aside. It isn't Juno.)
  Script: Prismfall::Ledger.start_ruin_route
  → story/12_RUIN_ROUTE.md R1, "Twenty-Three Graves".
> Don't. (no)
  Script: pf_choose(:ch15_look_back, :no)
  (You walk past. Behind you the glass goes on calling. When you've walked far enough, it stops. It never starts again, on this save.)
```
*(Without `ruin_unlocked`, the pane isn't there. Dask's line at Gravenmoor's gate set up "rule or habit".)*

## Map 808 — the Hush (`:BLEED`): **chapter close** (autorun at the far edge, V136 == 11 → 12)
A Bleed zone where sound doesn't exist. **BGM and BGS stop; SEs are muted** for the map. The PC's footsteps show as **ripples** on the ground (an animation on each step). Wild Pokémon move, and their cries show as rings with no sound. **Glassfall Sliver** in a ripple that doesn't fade. No dialogue boxes at all on this map until its far edge.
```
(At the far edge of the Hush, where the sound starts again, you stop and listen to it come back: wind, then a bird, then far off, something industrial: hammers. A lot of hammers. Cogsworth.)
(In your pocket, Morwen's Ring is cold. Under your collar, the scar is warm.)
V136 = 12. Variable V102 STORY_CHAPTER = 16.
QUEST LOG: "Eighteen Roads" — North-east to Cogsworth and the Slag Mesa. Gym 15. Somebody in the Strade Works has been building something with Voss's name on the blueprints.
```
*(Ch16 opens on the Noonless Road → the Slag Mesa → Cogsworth.)*

---

## Map events needed (Chapter 15)

Built so far: **920, 924, 925, 926, 928, 930**. **[NEW]** = an event or map not in maps.json. V136 = **CH15_STEP** (design/FLAGS.md). Maps go through the three-pass workflow (design/MAPGEN.md, top).

**201–203 Duneholt bazaar**: the green awnings and 12 sledges (decor events); the caravan-mother; the sled-runner with Marisol's letter; **`:war_convoy`** (V136 0 → 1 on `:refuse`).
**930 bone-carters' camp**: the convoy line passes; `OS_CARTERS_DEAD` turn-ins (3 tally-sticks to Elder Ossa, the Tally-wall).
**926 Glass Dunes / 925 Steamline** (built): the caravan-mother turns back at the **Convoy marker**; **the path-follower convoy** [NEW helper: `pf_echo_follow` records the PC's steps and moves N sledge events along them; shared with Gym 14's crypt echo]; 3 **remains markers** [NEW] (`OS_CARTERS_DEAD`); **the patrol** double (Torvald, Esk); the dragon landing (a Dragonite event drops in: jump plus a shadow).
**920 Rimed Sands** (built): trench-head handover; Teo (`TEO_SAVED`); the sled-runner gift (**Frigibax "Sledge"**); V136 = 1; **Odessa's skiff** autorun at the lookout (a large rope-and-skiff picture descending; fade to 780).
**780 Jawbone Ridge** (`:MOUNTAIN`): the white jaw-ridge; the smoke-wall panorama to the west; the boarded headframe (784) with the notice and lantern; **Sliver #1** at the cairn; the telescope hiker; 3 trainers.
**770/771 Vigil**: the Center board autorun (**the Siege news**, V136 1 → 2); the Circular; Odessa's mooring (her hangout).
**781 Hindmoor** (`:INVERSE`): standing pools [NEW reflection events: an interact shows the road behind; the deep pool shows the ferry vignette]; **Sliver #2**; the **staithe** with the *Dovetail* (Edda's hangout from V136 >= 8); 3 trainers.
**790 Downflame Road** (`:INVERSE`): downhill-both-ways slopes; lantern-posts with downward flames (animated tiles); 2 trainers.
**380 Gravenmoor / 381 Center / 382 Mart**: fog; the **echo NPCs** (the sweeping woman, the three-move children, **Aldous** at the wall) as translucent looping events; **the gate autorun** (Dask, then Ysolde, V136 2 → 3); "The Dead Are Bad at This" (V136 3–5); `AN_GIMMIGHOUL_COINS`; Mart: Badge-14 stock, Spell Tag, Reaper Cloth; Odessa's mooring.
**383 Vane Hall** [interior set, ~5 rooms]: the clock at 11:40 (hall); the five rooms' echo vignettes in order (the clock-hand door logic); Kestrel following as an NPC through the rooms (move routes); **Sliver #3** in the nursery (after Kestrel leaves the room); the music room's **Sinistea (Antique)** static; the hall exit scene (V136 3 → 4).
**384 Lantern Hospice** + **the barrows**: Ysolde's hangout; the archive (AF 211 town plan for `AN_ALDOUS_DOOR`); **Morwen's grave** (M.V. stone, Edda kneeling; V136 7 → 8; MORWEN'S RING).
**390–395 Gym 14**: as GYM_PUZZLES (twin naves, pews, the crypt echo, Morwen's chapel with the lectern text); 6 trainers; Ysolde double (394); V136 = 5. **The nave cutscene `CE-1`** (V136 5 → 6) needs: letterbox, the sepia tone, an arena panorama, the Glassfall wave (a picture sweep), the vestry set, the Morwen echo sprite, Ines's echo; **the loft** (`GO_ECHO`, three prompts, a translucent player); **K6** at the altar step (V136 6 → 7; the overload hook); the moor's-edge vignette.
**924 Siege Camp / 928 Command Pavilion** (built): reached via Odessa (926 drop). Add to 928: the Dominar's lines (above), Anja's cage dialogue, **`:war_prisoner`**; the night cage-guard fight (`:free`); the **caravan well** for `:exchange` [NEW small map ~21×17 between the lines, or staged on 926]; V136 8 → 9.
**800 Noonless Road** (`:INVERSE`): the NOON 1 MILE milestone + **Sliver #4**; 2 trainers.
**804 Barrow of the Wardens / 805 Sanctum**: 18 replica-Plate alcoves (inscriptions); the Bell of AF 211 (**Bronzong "Six O'Clock"**, at 6 pm only); Aldous's gravestone; **the barrow-door into the sky** (V136 9 → 10); 1 trainer.
**806 Giratina's Reverse Depths** (`:INVERSE`): floating islands, up-falls; the tear (a picture overlay showing the nave); **Giratina** (`:GIRATINA_DEPTHS`; S143; V136 10 → 11); the black pane (only `ruin_unlocked`; `:ch15_look_back`).
**808 The Hush** (`:BLEED`): **map-level audio mute** [NEW: a map flag in MAP_AUDIO.yaml; `pbBGMStop`/`pbBGSStop` + SE mute on entry]; footstep ripples; silent cries; **Sliver #5**; the far-edge close (V136 11 → 12; V102 = 16).

## Trainer roster (Ch15; 17 regular trainers; PBS blocks in 3 versions; ≤ 67 before Badge 14, ≤ 71 after)
| Map | Class (stock type) | Name | Lv | Team idea (field touch) |
|---|---|---|---|---|
| 780 | Hiker | Gunnar | 63 | Steelix, Garganacl, Lycanroc (Mountain: wind-boosted Flying is bad news for him) |
| 780 | Ace Trainer | Rosalind | 64 | Lucario, Kingdra, Mamoswine |
| 780 | Dragon Tamer | Deserter Brask | 64 | Flygon, Salamence (no uniform; "going home the long way") |
| 781 | Hex Maniac | Morag | 64 | Mismagius, Gourgeist, Trevenant |
| 781 | Black Belt | Pilgrim Ansel | 65 | Lucario, Hitmontop, Medicham |
| 781 | Punk *(Guitarist)* | Cassidy | 65 | Toxtricity, Skuntank, Houndoom (Inverse: Poison loves it) |
| 790 | Gentleman | Mr. Ashby | 65 | Polteageist, Aegislash, Mr. Rime |
| 790 | Psychic | Seren | 65 | Gardevoir, Bronzong, Indeedee |
| **Gym 14** | Channeler ×3, Gentleman (revenant), Lady, Mourner-acolyte | (GYM_PUZZLES) | 63–66 | as GYM_PUZZLES; in 392 only |
| 800 | Medium *(Channeler)* | Wenna | 67 | Banette, Dusknoir, Froslass |
| 800 | Hex Maniac | Ilse | 68 | Gengar, Hatterene, Mimikyu |
| 804 | Gentleman | Revenant Lord Faraday | 68 | Aegislash, Doublade, Golurk (Barrow, `:CAVE`) |
**Story fights (new PBS):** `ASHKAAR_OFFICER` "Rider Torvald" + `ASHKAAR_SOLDIER` "Rider Esk" (double, Lv 64–65: Dragonite, Garchomp / Salamence, Haxorus); `ASHKAAR_OFFICER` "Cage-Warden Hesk" (Lv 67: Hydreigon, Kommo-o, Arcanine, Tyranitar). **K6**: existing `RIVAL_KESTREL` 60–62 and 160/260 versions. **Gym 14**: existing `LEADER_YSOLDE`. **Boss:** `:GIRATINA_DEPTHS` (108_Boss_Giratina.rb).

**Items owner:** MORWEN'S RING (Key Item), the KNELL BADGE (proposed), TM30, Glassfall Slivers #1–5 of the Ch15 allotment, Magical Seed ×2 + Spell Tag (Mastery), Reaper Cloth + Cleanse Tag ×2 (`AN_ALDOUS_DOOR`), Relic Gold (`AN_GIMMIGHOUL_COINS`), the carters' Spell Tag (`OS_CARTERS_DEAD`, completing). **EventMons:** Frigibax "Sledge" (gift, Lv 35), Sinistea Antique (static, Lv 64), Bronzong "Six O'Clock" (static, Lv 66). **Portrait requests (art, to Gemini):** **MORWEN** (echo: translucent grey-blue, Warden's coat; `neutral`, `sad`), **EDDA** (`neutral`, `sad`), Dominar Hrothgar (`neutral`, `angry`), Ines (echo, singing; a sprite is enough).
