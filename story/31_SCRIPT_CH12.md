# Script: Chapter 12 — "Dead Letters" (the Tetherline, the Cloudstair, Skyreach, Gym 11; the Larch Papers; the raid; K5; Interlude III)

> **Final playable script** for Chapter 12, the third chapter of Act III. It covers the mail-ship's arrival and the Tetherline (732), the Cloudstair (724–726, Rock Climb), Skyreach (320–326: the Mast Ward, the Center and Mart, the Lower Gantries, the Skybridge Ward, the Gale Post Hall, the Smugglers' Gantry), the Gale Post gym (Gym 11, 330–334), Stormwatch Spire (744–746), Interlude III in Meridian Spire (Voss's office, Lumen), and the road out onto Conductors' Causeway (740). None of these maps is built; the list at the end is what to build from.
> Follows `story/30_SCRIPT_CH11.md`; `story/32_SCRIPT_CH13.md` follows this. Sources: 06_ACT_III Ch12 and Interlude III, 03_CAST (Odessa, Larch, Kestrel, Marchetti, Kroll, Voss, Calla, Morwen), 09_MYSTERIES (#8 the pin, #10 and #16 and #28 the letter to "I.", #12 Sable is Kroll, #14 the badge case, #15 the arena model, #23 the Stormfront Wyrm, #25 the reflection), NARRATIVE_KEYS (`:ch12_letter`, GO_FINE_PRINT, Odessa's Consent), 14_WAR_AND_BLESSING (the Ch12 insert), 15_COMEDY (Ch12 "Flight Safety"; the first mirror gag; the Wardens' Circular), GYM_PUZZLES Gym 11, MEGA_EVOLUTION §1.2 (Meridian's keystones), BALANCE (K5, Marchetti Ch12, Odessa), WALKTHROUGH Ch12, `design/CHAPTER_BEATS.md`.

## Conventions
As in the earlier scripts. **Portrait cast here:** Larch, Odessa, Kestrel, Voss, Calla, Marchetti. Juno appears only by Circular. Sable/Kroll does not appear: she is exposed in Ch13, and nothing here may name Kroll on screen. **Plain:** Kit (the Gale Post courier boy, the gym's hint giver), the mail-ship's loader and captain's mate, the sky-river guides, the Directorate officers, the Mart clerk, the newsreader and the Meridian spokesman, every townsperson and trainer. Odessa's gym battle is a **double**: `Prismfall.gym_battle(pfm_gym(:LEADER_ODESSA), double: true)`. K5 is `Prismfall.rival_battle(:RIVAL_KESTREL, "Kestrel", 5, field: :STORMFRONT)`. Marchetti is `TrainerBattle.start(:MERIDIAN_MARCHETTI, "Helene")` (base version; her Ch12 team, Mega Manectric).
**Counter:** V133 **CH12_STEP** (design/FLAGS.md): 0 aboard the mail-ship · 1 moored on the Tetherline · 2 up the Cloudstair into the Mast Ward (the curfew) · 3 the Gale Post Hall: Larch and Odessa · 4 "Flight Safety" (the skiff drill; the gym opens) · 5 Gym 11 won · 6 the Larch Papers broadcast (S131) · 7 the raid: the bomb, Marchetti, Larch away by skiff, the Fellowship SUSPENDED (S132) · 8 K5 and `:ch12_letter` (S133, V114 = 2) · 9 Interlude III done (V119 3 → 0) · 10 Conductors' Causeway, the late reflection (chapter closed; V102 = 13).
**State set here:** S131 CH12_LARCH_PAPERS, S132 CH12_GALE_RAID, S133 CH12_K5_DONE, V114 KESTREL_STAGE = 2, V119 INTERLUDE_ACTIVE = 3 then 0. Key: `:ch12_letter`. Key Items: SPLITTER CASING; MORWEN'S LETTER (if `:keep`). The Mandate arch at every Pokémon Center reads SUSPENDED from V133 >= 7 (28_SCRIPT_CH10, the Act III opener).

## The chapter's key events (design/CHAPTER_BEATS.md)
1. **The Larch Papers.** At midnight Larch reads her own AF 292 report to every screen in Velmora: Lattice extraction accelerates the Bleed. "I designed the Lattice. I was wrong." Within the hour a bomb kills the broadcast mid-sentence, and by dawn Meridian's news has her as the bomber. Build-up: Larch's Ch4 confession ("It's my design"), her Ch8 goodbye, Rimeholt's ice, Cindervault's caldera, Lumen's cracked Plate, the "Larch works for Meridian" red herring (resolved here). Payoff: the broadcast, the realm *hearing* it, the bomb. Consequence: Larch a fugitive in Cragholm (Ch14), the SPLITTER CASING (Ch13's tribunal, Kroll), Odessa's Consent, the Fellowship SUSPENDED.
2. **K5 and the dead letters.** Kestrel, in Meridian's sponsor jacket with a Resonance Gauntlet, robs Odessa's dead-letter archive for Voss in exchange for "the full AF 290 file". One letter falls: Morwen's, to "I.". `:ch12_letter`. Build-up: the envelope at the Lift (Ch10), K3's rumour (Ch6), K4's anger (Ch9). Payoff: the letter's text, the first time the PC reads Morwen's own words. Consequence: Interlude III, K6's opening line, Odessa's and Ysolde's lines, `:ch21_reach_kestrel`.
**No jokes** from the first red line on Stormwatch's board (V133 == 5, at night) to Larch's skiff clearing the storm wall, and none in Interlude III after Voss steps out. "Flight Safety" plays in the afternoon, before (15_COMEDY §1: a joke before a blow). **No side content** opens between Gym 11 (V133 == 5) and the archive (V133 == 8).

---

# CHAPTER 12 — "Dead Letters"

**Chapter start:** V101 = 3, V102 = 12, V133 = 0 (Anchorhold closed Ch11). The PC is aboard the Gale Post mail-ship over the Crownwall.

## The mail-ship (a short deck map or cutscene; autorun, V133 == 0 → 1)
```
(The mail-ship's deck in the late afternoon. Sacks lashed everywhere. A Pelipper asleep on every rail. Ahead, out of the plain south of the Crownwall, a thing like a needle: a spire of masts and gantries a mile high, going straight up into a wall of cloud that never moves. Lightning walks along the inside of the cloud like veins.)
[name: Captain's Mate] Skyreach. And the Stormfront on top of it, the Sky Plate's own weather.
[name: Captain's Mate] Been there since before the Accord. Never rained a drop on the city.
[name: Captain's Mate] Just sits there and thinks.
[name: Captain's Mate] We'll not moor at the top. Directorate's searching every sack at the upper docks since the Thaw.
[name: Captain's Mate] Everything from Isenmar gets opened.
[name: Captain's Mate] Captain says we go in low, on the Tetherline, and you climb.
(Something moves in the storm wall. Very big, very dark, along the lightning, and gone.)
[name: Captain's Mate] (not looking) Don't. Crews have a word for that.
[name: Captain's Mate] The Stormfront Wyrm.
[name: Captain's Mate] You see it, you don't say you saw it, and you buy the next round.
SE: the mooring horn. The ship drops into the shadow of the spire.
V133 = 1.
```
*(09 #23: the Wyrm is Zekrom, the Spire's Dark Stone, wired into Stormwatch's core; Larch's line in the Gale Post Hall is the seed's second half. Freed in Ch16.)*

## Map 732 — The Tetherline (`:STORMFRONT`)
```
(A walkway of iron grating slung under Skyreach's mooring cables, a hundred feet above the plain, swaying. The cables go up into the dark of the spire overhead, thick as trees.)
[name: Loader] (handing your bag down) Up the Cloudstair. It's the porters' way.
[name: Loader] Nobody official's climbed it in years. They'll be looking at the lifts.
```
Road sign: "THE TETHERLINE. Cable crews only. Do not lean."
Trainers (Lv 52–54): cable-crew riggers, a Gale Post courier on a break. The Tetherline's far end is the Cloudstair's foot.

## Maps 724–726 — the Cloudstair (`:MOUNTAIN`; Rock Climb)
The porters' stair up the outside of the spire's rock core: climbing walls (Rock Climb, from Rimeholt), wind-scoured ledges, a cave section (725) through the core, and the summit (726) at the Mast Ward's back door.
- A porter resting with a sack of mail on his back: "Lifts are for people with nothing to hide. That's nobody, these days."
- At the summit, a Directorate searchlight sweeps the ledge every few seconds (a timed event; walking into the beam isn't a fail, it sends you back to the last ledge with "A searchlight finds you. You duck back down.").
Trainers (Lv 52–55): climbers, a birdkeeper, a porter.

## Skyreach (320–326; Zenith's airship spire, `:STORMFRONT`)

### Map 320 — the Mast Ward: arrival (autorun at the Cloudstair's top gate, V133 == 1 → 2)
```
(Skyreach. A city built up the outside of a needle: platforms bolted to the masts, skybridges strung between them, airships nosed into docking cradles like bees into a comb. Everything creaks. Everything is lit.)
(At dusk, from the highest mast, a searchlight comes on. Then another. Then a dozen, sweeping the bridges.)
SE: a bell, nine strokes.
SCREEN (on every mast): ◆ MANDATE CURFEW IN EFFECT 21:00–06:00 ◆ Remain indoors. The Directorate thanks you for your patience.
(On the nearest bridge, two Directorate officers walk past. Each has a steel band on the wrist, with a bead of cloudy glass set in it.)
V133 = 2. QUEST LOG: "Eighteen Roads" — Find the Gale Post Hall. Odessa Gale's gym is the Post itself.
```
**Townsfolk (320, 321 PC, 322 Mart, 323 Lower Gantries, 324 Skybridge Ward):**
- A dock-hand: "Gale Post flies war mail for both sides now. Isenmar's letters and Ashkaar's, same sack. Captain says mail's mail." *(14_WAR_AND_BLESSING, the Ch12 insert.)*
- A Directorate clerk at the lift: "Prism munitions crates for the front? The Post refused them. Refused! The Warden said she doesn't carry things that go bang. We'll see about that."
- A child on the Skybridge Ward, pointing up at the storm: "My dad says there's a dragon in it. My mum says there's a dragon in everything if you're drunk enough."
- **The Center (321)**, the Mandate arch: SCREEN: ◆ PRIORITY GUEST ◆ Welcome to Skyreach, \PN. Curfew begins at 21:00. *(From V133 >= 7: ◆ FELLOWSHIP STATUS: SUSPENDED ◆ Please present yourself to a Directorate officer.)*
- **The Wardens' Circular** at 321: Juno's post, from the Elowen border: "THORNGUARD COUNTED FOUR THOUSAND AND TWELVE. THEY COUNTED THE BABIES TWICE. I MADE THEM. — J.H., WARDEN OF VERDANCE." Dorian replies: "*(Applause.)*" Anja doesn't reply. *(If `:ch11_anja == :let_confess`, Anja replies: "Twice is right. They're heavy.")*

### Map 325 — the Gale Post Hall: **"Guest of the Post"** (autorun on entering, V133 == 2 → 3)
```
(A hangar-sized sorting hall inside the spire. Pigeonholes up to the roof, rope ladders, letter sacks sliding on overhead rails, Pelipper and Corvisquire coming and going through round doors in the walls like a dovecote. It smells of paper, rain and engine oil.)
(At a sorting table at the far end, in a borrowed Gale Post coat with the sleeves rolled up, a grey-haired woman is sorting letters very fast and very badly.)
[portrait: LARCH, happy] \PN! You found it. Of course you found it.
[name: Larch] Did you come up the Cloudstair? Don't tell me. I know you did.
[name: Larch] You've got that look. The rock-dust look.
(A young woman drops down a rope from a pigeonhole twenty feet up and lands on the table. Goggles, a scarf that goes round three times, a scar through one eyebrow.)
[portrait: ODESSA, happy] So this is the famous one. No colour on the scanners.
[name: Odessa] You'd make a great smuggler.
[portrait: ODESSA, smug] Odessa Gale. I run the Post and the Post runs me.
[name: Odessa] Skyreach's got one law: the wind doesn't care.
[name: Odessa] Everything else is negotiable.
[portrait: LARCH, neutral] Odessa's been kind enough to hide me. In plain sight.
[name: Larch] Nobody looks at a woman sorting mail.
[portrait: ODESSA, neutral] She's terrible at it.
[name: Odessa] Three letters to Lumen in the Isenmar hole this morning.
```
```
[portrait: LARCH, neutral] (lower) Did you see the officers on the bridges? The bands on their wrists?
[name: Larch] Lattice-glass. Meridian can't buy a Warden's ring off the Hearthguild, so it grows its own keystones.
[name: Larch] A Warden's ring asks a heartstone to open. Theirs pry it open.
[portrait: LARCH, sad] If they come for me tonight and Marchetti's dog changes shape on you, don't stand there gawping.
[portrait: LARCH, neutral] And the dragon. The crews' dragon in the storm.
[name: Larch] I've seen the drawings they make of it.
[portrait: LARCH, shocked] [emote: dots] (very softly) That's impossible. That's the shape of the Spire's core.
[name: Larch] I signed off on that core. It was a battery.
```
```
[portrait: LARCH, neutral] I'm going to say something tonight, \PN. On every screen.
[name: Larch] Odessa's relays reach every Center in Velmora, and every Center has a screen now, thanks to the Mandate.
[name: Larch] Meridian built me an audience.
[portrait: LARCH, sad] Everything I wrote in AF 292. The report they buried.
[name: Larch] Rimeholt's in it. Cindervault's in it. The Ebb's in it. Lumen's Plate.
[name: Larch] I predicted all of it, and then I took their money and I let them bury it.
[portrait: LARCH, neutral] And a Lattice technician in Rimeholt sent me something on the ship you came in on.
[name: Larch] The last hour of Tower Three. Signed "Tage".
[name: Larch] I don't know who Tage is. I'd like to buy him a drink.
[portrait: ODESSA, neutral] Midnight. Stormwatch Spire. The relay crown's at the top of the storm.
[name: Odessa] Get your badge first.
[name: Odessa] If tonight goes how I think it'll go, there won't be a gym tomorrow.
V133 = 3.
```
*(The Ch4 red herring ("Larch works for Meridian") is resolved here: she did, and she's about to say so. Tage's cache is the Ch11 GO_THIN_ICE beat's consequence.)*

### Map 326 — the Smugglers' Gantry: comedy scene Ch12, **"Flight Safety"** (touch, the skiff on the gantry, V133 == 3 → 4)
```
(A narrow gantry sticking out of the spire into empty air. Moored to it, a Gale Post skiff: a wing, a basket and a rope.)
(Odessa is in the basket. Larch is on the gantry, holding the rope with both hands.)
[portrait: ODESSA, happy] Drill! If it goes wrong tonight, this is your door.
[name: Odessa] Safety briefing! There's one rope. Hold it.
[portrait: LARCH, panic] [emote: question] Where is the rest of the briefing?
[portrait: ODESSA, smug] That was the long version.
[portrait: LARCH, angry] I have a DOCTORATE in things that should not be airborne and this is all of them!
[portrait: ODESSA, happy] Professor, you invented the thing that's eating the country.
[name: Odessa] You don't get to be scared of a kite.
[portrait: LARCH, deadpan] ...That's fair. I hate that that's fair.
> (Let go of the rope)
[portrait: LARCH, panic] [emote: exclaim] LECTURE FOURTEEN STARTS NOW—
(The skiff drops six feet on its tether, bobs, and comes back up. Larch is still holding on. Odessa is laughing so hard she has to sit down in the basket.)
[portrait: ODESSA, happy] Six feet! She did six feet!
[name: Odessa] (to you) You heard her. Lecture fourteen. Don't let me forget.
V133 = 4. The Gale Post gym opens.
```
*(15_COMEDY Ch12 "Flight Safety", staged as a drill so the real escape at midnight lands: the joke goes before the blow. The "(Let go of the rope)" option is the PC's only line; it's always offered, and always taken.)*
*Also here: **the first mirror gag** (15_COMEDY): on the way back in, a puddle on the gantry. The PC's reflection is caught mid-yawn and snaps to attention. Kit, the courier boy, sees it: "Do it again!" (It won't.) (15_COMEDY gives the line to Juno; she's at the Elowen border this chapter, so Kit has it.)*

## Maps 330–334 — the Gale Post gym (Gym 11; GYM_PUZZLES Gym 11)
Doors open at V133 >= 4. Built as GYM_PUZZLES Gym 11 ("the wind doesn't care"): 330 the Hangar (teach), 331 the Gust Deck (twist, coupled vanes), 332 the Mail Chute (combine, sacks ride the wind), 333 the Captain's Deck (arena), 334 the Dead-Letter Archive (Mastery, optional; and the stage of K5).
- **Gym sign:** "THE GALE POST. Warden: ODESSA GALE. 'Hold onto something.'"
- **Kit** (the hint courier in 331/332): "Every vane works two fans. Look up, the rods show which." On the third hint: "Captain says I'm not allowed to just tell you. (He tells you.)"
- **334 the Dead-Letter Archive** is open as Mastery before the raid. Its undeliverable "Abroad — closed by quarantine" hole is visibly stuffed with a bundle tied in black ribbon. Kit: "Don't touch that one. Captain says those are the saddest letters in the world. Nobody knows who 'I.' is."

### 333 — the Captain's Deck: Odessa (double)
```
(An open deck on the outside of the spire, in the wind, with the storm wall close enough overhead to hear it hum. Odessa on the far rail with her goggles down.)
[portrait: ODESSA, happy] Hold onto something. No, really.
[portrait: ODESSA, neutral] I've flown letters through three storms and a Bleed.
[name: Odessa] People write things in letters they'd never say.
[name: Odessa] Love. Sorry. Goodbye.
[name: Odessa] I carry them. I don't read them. I don't hand them to a clerk because he said please.
[portrait: ODESSA, smug] Let's see if you can keep your feet.
BATTLE: Prismfall.gym_battle(pfm_gym(:LEADER_ODESSA), double: true) — field `:STORMFRONT` (Tailwind and Hurricane; Mega Pidgeot "Post").
(Mega Pidgeot:) [portrait: ODESSA, happy] Post! Special delivery!
(Her last Pokémon, Corviknight "Taxi":) [portrait: ODESSA, neutral] Taxi. Take us home.
(WIN:)
[portrait: ODESSA, happy] You kept your feet! Nobody keeps their feet.
[portrait: ODESSA, neutral] The POSTMARK BADGE. Every letter that goes through Skyreach gets one.
[name: Odessa] Means it got here. Means somebody carried it.
RECEIVE: POSTMARK BADGE. RECEIVE: TM51 ROOST.
[name: Odessa] (looking up at the storm, quieter) Get some sleep. Not too much. Midnight.
V133 = 5.
```
*(**Badge name (proposed):** the **Postmark Badge**; not in PBS or BADGE_TIERS. The sky-river guides' Waterfall (HM05) and the Mastery reward wait until the morning after: no side content between V133 == 5 and 8.)*

---

## Maps 744–746 — Stormwatch Spire: **the Larch Papers** (key event 1)

### Map 321 → 744: **"Midnight"** (autorun on sleeping at 321 with V133 == 5; night)
```
(Night. A knock at the Center's window, not the door. Odessa, hanging upside down from the gutter.)
[portrait: ODESSA, neutral] Curfew's on, so we're going over the roofs. Keep low.
[name: Odessa] Don't look at the searchlights; they're slower than they look and faster than you think.
Script: Prismfall.checkpoint
(Fade. Rooftops, skybridges, a ladder up the outside of a mast with the city falling away underneath.)
```
### 744/745 — the climb (Stormwatch's maintenance stair inside the relay mast; wild Electric and Steel Pokémon, two Directorate guards who don't look up)
- A maintenance board on 745: "RELAY CROWN: ALL CHANNELS. CORE: DO NOT OPEN." Underneath, chalked: "IT HUMS WHEN THE STORM DOES."
- The core's housing on 745: a steel cylinder as big as a house, rivets and warning stripes. When the PC passes, the shard goes warm, and something inside the cylinder **moves**, once, heavy, like a sleeper turning over. *(Zekrom. Ch16.)*

### Map 746 — the Roof: **the broadcast** (autorun at the relay crown, V133 == 5 → 6)
```
(The top of the spire. A ring of relay dishes round a little glass booth, and above it, close enough to touch, the underside of the storm: slow, purple, full of light.)
(Inside the booth, Larch at a microphone, in her own coat again, with a stack of paper and her reading glasses on a cord. Odessa at the switchboard.)
[portrait: ODESSA, neutral] Every Center. Every mast. Every screen in Velmora.
[name: Odessa] You're live in three. Two.
(She points.)
SCREEN (every screen in the realm; shown here on the booth's monitor and, in quick cuts, on screens the player has seen: the Ebbmouth quay, Rimeholt's Keep gate, Ironreach's Pit, the Verdance Heartgarden where Juno is sleeping on a bench under it, Cindervault's forge hall):
[portrait: LARCH, neutral] Good evening. My name is Imelda Larch.
[name: Larch] Most of you have never heard of me, and every one of you has a light on because of me.
[name: Larch] Twenty-one years ago I designed the Prism Lattice. Eleven cities.
[name: Larch] I was very proud. In AF 292 I wrote a report for the Fellowship's board.
[name: Larch] This is it.
(She holds it up. It has a stamp across the front: SUPPRESSED.)
[name: Larch] Page four. Lattice extraction accelerates the Bleed.
[name: Larch] Every Plate we draw on thins the world around it.
[name: Larch] I gave them the rate. I gave them the cities that would go first.
[portrait: LARCH, sad] Ebbmouth's river. Lumen's Plate. Cindervault's caldera. Rimeholt's lake.
[name: Larch] In that order. It's in my handwriting.
[name: Larch] I was right about all of it, and nobody stopped, and I took the money and I let them put this in a drawer.
[portrait: LARCH, neutral] (a smaller sheet) This came to me on a mail-ship today, from a technician named Tage. It's the last hour of Rimeholt's Tower Three. The draw at a hundred and fifty-five percent.
[name: Larch] An override signed in Lumen, not in Rimeholt.
[name: Larch] (another) And these are the heat contracts. Isenmar's and Ashkaar's.
[name: Larch] Side by side. Same price per—
[portrait: LARCH, sad] (she stops herself, looks into the camera) No. You won't read that page.
[name: Larch] Nobody will. Here's the only line that matters.
[portrait: LARCH, neutral] I designed the Lattice. I was wrong.
[name: Larch] I'm telling you now because nobody else will.
Switch S131 CH12_LARCH_PAPERS = ON. V133 = 6.
(On the monitor, the quick cuts again: on the Ebbmouth quay, Marisol standing up. In Rimeholt's Keep, Anja putting down her pipe. In Verdance, Juno awake on her bench with her hands over her mouth.)
```
*(06_ACT_III: the broadcast is electric; the realm hears it. The heat-contract page is 14_WAR_AND_BLESSING's "nobody reads that page": Larch herself skips it, which is the point. Larch's given name, Imelda, is said on screen here for the first time since Ines's letter in the prologue (03_CAST).)*
```
[portrait: LARCH, neutral] Section two. The Unimprinted. In AF 290, at Crownhaven, during the—
(A sound under the floor. Not loud. A cough of the building.)
(Then the relay mast below the booth bends like a reed, and the dishes on the north side go up in white light.)
SCREEN SHAKE. FLASH. SE: the explosion, then a long scream of steel.
(The monitor shows: ◆ SIGNAL LOST ◆)
(Smoke. Larch on the floor of the booth with her papers everywhere. Odessa already up, dragging her by the coat.)
[portrait: ODESSA, angry] [emote: exclaim] Up. UP. That wasn't the storm.
```
### **The raid** (autorun, the stair down 746 → 745 → 325)
```
(Down the stair in the smoke. Below, on every landing, boots. Torches. Directorate grey, coming up.)
(At the 745 landing, in the wreckage of the relay mast's base, something glints in the debris by your foot: a curved shard of dark casing with a blinking dead light on it.)
RECEIVE: SPLITTER CASING. "A fragment of a Splitter's housing. The same make as the one at Lumen's Shatter."
[portrait: LARCH, shocked] That's— that's what cracked Lumen's Plate.
[name: Larch] That's the Hammer's. That's Sable's—
[portrait: ODESSA, neutral] Then it's the same hand that did Lumen. Pocket it. Run.
```
*(09 #12: the casing matches Lumen's because the same hand set both: Sable, who is Sabine Kroll of Meridian's Special Accounts. Tonight it makes the bombing look like the Hollow's. At the Ch13 tribunal, with the COMM-DEVICE (`IRONREACH_EVIDENCE`), it does the opposite. Key Item for Ch13 and Ch14.)*
```
(The Gale Post Hall, 325. Sacks spilled across the floor, Pelipper screaming in the rafters, couriers with their hands up. Directorate officers everywhere. On the sorting-hall catwalk above, a woman in a long grey coat with a steel band at her wrist and a Manectric at her heel.)
[portrait: MARCHETTI, neutral] Professor Larch. Warden Gale. And our Fellowship guest.
[name: Marchetti] Good. Everyone I wanted, in one room.
[name: Marchetti] Nobody is under arrest. You're all under protection.
[name: Marchetti] A Hollow bomb has just destroyed public infrastructure, and the Directorate's first duty is your safety.
[portrait: LARCH, angry] A Hollow— You did that. Your people did that.
[portrait: MARCHETTI, neutral] Professor. You'll want to be careful what you say in front of witnesses.
[name: Marchetti] It's all being written down.
[portrait: ODESSA, neutral] (to the PC, not moving her lips) Skiff. Gantry. Two minutes.
[name: Odessa] Keep her busy.
[portrait: MARCHETTI, neutral] (coming down the catwalk stair) You're not under arrest.
[name: Marchetti] You're under protection.
[name: Marchetti] Learn the difference before it's taught to you.
BATTLE: TrainerBattle.start(:MERIDIAN_MARCHETTI, "Helene") — single, field `:STORMFRONT`; the catwalks. Her Mega Manectric is the first Meridian Mega (Larch's warning pays off).
(Mega Evolution:) (The band on Marchetti's wrist flares, and the bead of glass in it goes bright and ugly, like a lamp too close to a face. It doesn't sing the way a stone should. It screams.)
(LOSE: whiteout to 321 under "protection"; the raid restarts at 325 from the checkpoint, Larch still in the hall.)
(WIN:)
[portrait: MARCHETTI, neutral] (recalling Manectric, not hurried) Fine.
[name: Marchetti] I'll note that you resisted protection.
(Behind her, through the hall's round doors, a skiff drops off the Smugglers' Gantry into the dark: a wing, a basket, a rope, two figures.)
(Larch's voice comes back on the wind, very faint.)
LARCH (off): —LECTURE FOURTEEN—
(The skiff goes up into the storm wall, into the lightning, and doesn't come out.)
[portrait: MARCHETTI, angry] (for the first time) Get me an airship. Any airship.
(An officer, apologetic.) Director, nothing flies into the Stormfront. Only the Post.
Switch S132 CH12_GALE_RAID = ON. V133 = 7.
```
*(Odessa gets Larch out through the Stormfront to Cragholm ("I've got friends who live underground"; 06). Odessa herself comes back for her Post before dawn, by the Smugglers' Gantry.)*
### Map 322 — the Skyreach Mart: **"Status"** (touch at the counter, any time after V133 == 7)
```
[name: Mart Clerk] (apologetic, turning the terminal round) I'm so sorry.
[name: Mart Clerk] It just came through. I didn't do it.
TERMINAL: Fellowship status: SUSPENDED. Priority services withdrawn. Please present yourself to a Directorate officer at your earliest convenience.
[name: Mart Clerk] I can still sell you things. Cash.
[name: Mart Clerk] I'm not supposed to. I'm going to.
```
*(`:pro_fellowship` keeps its value; Meridian has withdrawn the privilege. The PC's Center screens read SUSPENDED from here on.)*

### The dawn news (Center screens; first time the PC passes one after V133 == 7)
```
SCREEN: (Meridian blue.) "—Hollow sympathiser Imelda Larch, who last night bombed Skyreach's Stormwatch relay in an attempt to—"
SCREEN: (A Meridian spokesman at a podium with the sunburst behind him.) "We are cooperating fully with the Directorate. Professor Larch's state of mind has been a concern to her former colleagues for some time."
SCREEN: ◆ LARCH: WANTED FOR QUESTIONING ◆
```

## Map 334 — the Dead-Letter Archive: **K5** (key event 2; autorun on entering 325 after V133 == 7, a sound from the archive door)
```
(The archive. Pigeonholes floor to ceiling, by kingdom, ten years of letters nobody could deliver. Somebody has been through the shelves in a hurry: sacks slit open, letters ankle-deep.)
(At the far end, by the hole marked ABROAD — CLOSED BY QUARANTINE, a boy in a beautiful new jacket, cream and gold, with the Meridian sunburst on the shoulder. On his left hand, a gauntlet of steel and cloudy glass that hums.)
(He has the bundle in the black ribbon in his right hand.)
[portrait: KESTREL, neutral] You. Of course you.
[name: Kestrel] Don't. I know what you're going to say. "That's not yours."
[name: Kestrel] It is. It's hers. It's the only thing of hers left in the world that isn't a lie somebody else told.
[portrait: KESTREL, angry] He's going to give me the file. All of it. AF 290.
[name: Kestrel] What really happened to her.
[name: Kestrel] All I had to do was walk in here while the Directorate made a noise.
[name: Kestrel] (lifting the gauntlet) And he gave me this, so nobody stops me.
[name: Kestrel] Want to see what it does?
BATTLE: Prismfall.rival_battle(:RIVAL_KESTREL, "Kestrel", 5, field: :STORMFRONT) — single; K5. The Gauntlet: the field surges (a visual tell, the field's overlay flaring) whenever Kestrel's Pokémon attack. Aegislash "Morwen" is his ace.
(Mid-battle, Aegislash "Morwen":) [portrait: KESTREL, neutral] I named her after the only person who never lied to me.
(LOSE: whiteout to 321; K5 restarts at the archive door.)
(WIN:)
[portrait: KESTREL, panic] (stepping back, the gauntlet sparking) No— no, that's— it's supposed to—
(He doesn't stay to finish. He turns and goes up the archive's ladder to the roof door, two rungs at a time, with the bundle inside his jacket. At the top a letter slips out of the ribbon, flutters, and comes down, slowly, through the dust, at your feet.)
(He doesn't come back for it. He doesn't see.)
Switch S133 CH12_K5_DONE = ON. Variable V114 KESTREL_STAGE = 2.
```
*(K5, BALANCE: Lv 54, Staraptor, Krookodile, Scizor, Zweilous, his starter, Aegislash "Morwen"; Hard AbilityIndex 2. The Gauntlet's surge is a visual tell only. Kestrel's sprite wears the sponsor jacket from here; the gold envelope corner (Ch10) is gone.)*
```
(The envelope is old. The postmark is from Crownhaven, AF 290, and stamped over it: UNDELIVERABLE — QUARANTINE. Addressed to "I.", and under that a street the rain got to long ago, in a country across the sea.)
(The letter inside is one page. The handwriting is fast and slants hard to the right, like someone writing into the wind.)
LETTER: "I. — You must not let the child come back. Not for my sake, not for anything. If Valen learns what lodged in that little chest, he will put a crown on it."
LETTER: "Keep wilting, love. Keep them small and safe and far. I'll carry the name. — M."
(Under the M, a tiny drawing: a sprig of something, three leaves.)
```
```
> Keep the letter. (keep)
  Script: pf_choose(:ch12_letter, :keep)
  (You fold it along its old folds and put it in your bag, next to the badge case. The case hums, once, as if it noticed.)
  RECEIVE: MORWEN'S LETTER.
> Send it to Kestrel by Gale Post. (send)
  Script: pf_choose(:ch12_letter, :send)
  (Kit, at the archive door with his eyes very wide, takes it from you in both hands.)
  [name: Kit] Kestrel Vane, Meridian Spire, Lumen.
  [name: Kit] That's easy. That's a real address.
  (He looks at it.)
  [name: Kit] It's been undeliverable for ten years. Not any more.
  (He puts a Postmark on it himself, carefully, in the corner, and runs.)
> Burn it. (burn)
  > It's the last thing someone wrote. Burn it?
    > Burn it.
      Script: pf_choose(:ch12_letter, :burn)
      (There's a lamp on the archive desk. The paper takes quickly, the way old paper does. The little drawing of three leaves goes last.)
      (Behind you, at the door, Odessa, back from the storm, wet through, with her goggles round her neck. She looks at the ashes.)
      [portrait: ODESSA, sad] Dead letters are the last thing some people ever said.
      (She doesn't say anything else. She doesn't need to.)
    > No.
V133 = 8.
```
*(NARRATIVE_KEYS §4.2 `:ch12_letter`: `:send` KESTREL+3 YSOLDE+1, and K6 opens "You sent me a *letter*. Hers."; `:burn` RES−2 YSOLDE−2, Ysolde's "So you chose not to know. That's a choice too.", and Odessa won't release the Sky Plate in Act V (WARDEN_CONSENT entry 11); `:keep` leverage or a gift in Ch15. `:ch21_reach_kestrel` checks `!= :burn`. 09 #10, #16, #28: "I." is Ines, the PC's mother; "the child" is the PC; "keep wilting" means stay abroad and sicken rather than come home. The PC isn't told: a player who remembers Ines's letter from the prologue ("I wanted one of us to have an ordinary life") can put it together. The Ch15 echo confirms it.)*
```
[if :ch12_letter != :burn]
  (Odessa comes in from the roof door, back from the storm, wet through, with her goggles round her neck.)
  [portrait: ODESSA, neutral] She's out. Cragholm by now, under a mountain with a lot of miners who owe me favours.
  [name: Odessa] She was sick twice over the Mast Glacier and lectured me the whole way.
  [name: Odessa] Lecture fourteen. It's about wind shear. It's actually very good.
[portrait: ODESSA, neutral] They'll shut the Post, you know. Not today. Some day soon. "Pending review."
[portrait: ODESSA, smug] Let them. The wind doesn't care.
```
**Side content opens now** (V133 >= 8): the sky-river guides (Waterfall, HM05; 323); the Mastery room 334 (its Morwen hole is empty now; Odessa: "Some letters you keep.", the Mastery completes without the bundle); trainers on the Skybridge Ward.

---

## INTERLUDE III — "Dead Letters" (playable as Kestrel; autorun on sleeping at 321 with V133 == 8)
**Party swap:** V119 INTERLUDE_ACTIVE = 3; the PC's party is stored and Kestrel's K5 team (healed) is loaded; the player character is Kestrel (`trainer_RIVAL_KESTREL` charset, the sponsor jacket). Map: **Meridian Spire, Voss's office** (Lumen; a single interior map, [NEW]), small hours.
```
(A tall office at the top of a tower. One wall is glass, and the whole of Lumen is under it, lit up: eleven million lights. Rain on the glass.)
(Behind a long desk, a silver-haired man in shirtsleeves is making tea. He has a kettle on a hot-plate, a tin of tea and two mugs. One of them is chipped.)
(Calla Wren is by the door with a clipboard. She doesn't look up.)
[portrait: VOSS, happy] Kestrel. Come in. Sit, sit.
[name: Voss] You look like you've been rained on. Have you been rained on?
[portrait: KESTREL, neutral] (putting the bundle on the desk) I brought them.
[portrait: VOSS, neutral] (not touching the bundle) In a minute. Tea first. Milk?
[name: Voss] You take milk. You took milk when you were five and you came to the Lumen Gala with your mother and stole every sugar cube in the hall. I remember.
(He gives Kestrel the chipped mug. He keeps the good one.)
```
**The office (walkable; the player examines things before talking to Voss again):**
- **A framed photograph:** a young man in a linesman's overalls on top of a pylon, grinning, with a sunburst armband. "AF 281. First Lattice line, Ferrow's Landing. — V."
- **A model under glass:** a circular arena with a crown-shaped roof and eighteen pillars. The plaque: "THE PRISM ARENA. Crownhaven. Festival of Champions." Kestrel: "...It looks like a lock."
- **The desk:** the gold sunburst pin, set apart on a velvet square. Looked at closely, the rays are uneven, like teeth. Kestrel: "Like a key." *(09 #8 and #14: the pin is the Gilded King's sun shaped like a lock; the badge case is the key.)*
- **The private drawer** (the desk's left side; it's not locked). See GO_FINE_PRINT below.
```
[portrait: VOSS, neutral] (handing Kestrel a thick folder, string-tied, stamped AF 290 · CROWNHAVEN · SOVEREIGN'S EYES ONLY) As promised. All of it.
(Kestrel unties it. Inside: transcripts. A Sovereign's order in Valen's hand: "Warden Vane to be held responsible. Her name to be struck." A press release written before the event it describes.)
[portrait: KESTREL, shocked] [emote: dots] He wrote it. Before.
[name: Kestrel] He wrote it before it happened.
[portrait: VOSS, sad] Your mother was destroyed by a man who thinks he's holding up the sky.
[name: Voss] I'd like to help you take the sky off him.
[portrait: VOSS, neutral] The Festival's in the spring. Valen will be in the arena, in front of the whole realm.
[name: Voss] Meridian would be honoured to sponsor an entrant who has something to say to him.
(A contract on the desk. A pen beside it. Gold nib.)
[name: Voss] I have to take a call. Five minutes. Read it properly. Read all of it.
[name: Voss] I'd hate you to think I'd hidden anything.
(He goes out. Calla stays by the door. As Voss passes her, she glances, once, at the left side of the desk. Then at Kestrel. Then back at her clipboard.)
```
*(The folder is real, mostly: it proves Valen scapegoated Morwen, and it leaves out Meridian's array at Crownhaven entirely (06; 09 #1). Calla's glance is the warning: she has had her own doubts since Ch5.)*
```
> Sign the contract.
  (Kestrel reads it. All of it. It's eleven pages and it's fair, and it's kind, and there's nothing in it.)
  (He signs. The gold nib scratches.)
  (Voss comes back in with a fresh pot of tea and sees the signature and smiles like a father at a school prize-giving.)
  [portrait: VOSS, happy] Welcome to the family.
  (Out of Voss's sight, Calla writes something on her clipboard, and then crosses it out so hard the pen goes through the paper.)
> Open the left-hand drawer.
  > Calla looked at it. Open it anyway?
    > Open it.
      (The drawer slides out without a sound. One file. Very thin.)
      FILE: UNIMPRINTED-01: KEYSTONE.
      (A photograph clipped to the front. A fifteen-year-old on the deck of a ferry in the rain, looking at the camera without smiling. You, on the Dovetail, the day you landed.)
      (The door opens.)
      [portrait: VOSS, neutral] Ah.
      (He doesn't sound angry. He sounds disappointed, the way a teacher is disappointed. He closes the door behind him, very gently.)
      Script: Prismfall.game_over(:GO_FINE_PRINT)
    > No.
```
*(GO_FINE_PRINT: Interlude-only, Kestrel's game over; epitaph "Kestrel Vane was reported missing the next morning. Meridian offered a reward." The photograph is the PC on the Dovetail (the prologue), from the ferry's own camera: Voss has had them on file since the NULL scan.)*
```
(After the signing. Kestrel at the glass wall with the chipped mug, looking down at the city. Lumen's eleven million lights.)
[portrait: KESTREL, neutral] (to his reflection) I'm going to make him say it.
[name: Kestrel] In front of everyone. Her name.
(Behind him, on the desk, the bundle of letters. Voss hasn't untied it. He never does, in front of Kestrel.)
[if :ch12_letter == :send]
  (A Gale Post courier at the office door, out of breath, with one letter and a Postmark in the corner. Calla takes it and, without a word, puts it in Kestrel's hand on his way out.)
  (He reads it in the lift. The lift goes down forty floors. He doesn't move the whole way.)
Variable V119 INTERLUDE_ACTIVE = 0. The PC's party is restored. V133 = 9.
```
*(Kestrel signs the Festival sponsorship contract in every branch except the game over (06 Interlude III). V114 = 2 already, from K5.)*

---

## Map 740 — Conductors' Causeway: Chapter 12 close, **"Half a Second"** (autorun on the causeway's first puddle, V133 == 9 → 10)
```
(Morning. The Glass Road north out of Zenith: a causeway of pylons and wire over a grey marsh, the Lattice lines humming overhead. It has rained in the night. The causeway is full of puddles.)
(You stop at the edge of one. Your reflection looks up at you: the same coat, the same bag, the badge case at your hip.)
(You turn your head.)
(Your reflection turns its head.)
(Half a second later.)
(You stay very still. So does it. Then the wind moves the water, and it's just a puddle again.)
V133 = 10. V102 STORY_CHAPTER = 13.
QUEST LOG: "Eighteen Roads" — North on the Glass Road to Lucent and the Athenaeum. Gym 12. Rowan's tribunal is there.
```
*(06_ACT_III's cliffhanger and 09 #25: Antumbra's mirror world, reached in Ch13 at Mirror Mere. The comedy mirror gag earlier this chapter (the yawn) is the same thing played light; this is the first time it's wrong.)*

---

## Map events needed (Chapter 12)

None of these maps is built. **[NEW]** = an event or map not in maps.json. V133 = **CH12_STEP** (design/FLAGS.md). Maps go through the three-pass workflow (design/MAPGEN.md, top): Claude's first pass, Claude's refinement on quota only, then Gemini.

**The mail-ship** [NEW] — a deck map (or a cutscene with a fixed panorama of the spire and the storm wall; the Wyrm's silhouette as a timed fog/picture flash); the captain's mate; the arrival autorun (V133 0 → 1).
**732 The Tetherline** — iron grating under the cables (bridge tiles over a sky panorama), the loader at the gangway, road sign, trainers; the far end to 724.
**724–726 The Cloudstair** — Rock Climb walls, ledges, the cave section through the core (725), the porter, trainers; **726 the searchlight** (a timed sweeping event; a touch on its beam tiles sends the PC to the last ledge), the back gate to 320.
**320 Mast Ward** — the arrival autorun (V133 1 → 2): the curfew bell, the searchlights (looping light events, night tint from 21:00 in-game or always at V133 2–7), the officers with wrist-bands; the screens (curfew text; from V133 >= 7 the dawn news); townsfolk as written.
**321 PC · 322 Mart · 323 Lower Gantries · 324 Skybridge Ward** — the Mandate arch (PRIORITY GUEST, SUSPENDED from V133 >= 7); 321's Circular (Juno's post; Dorian; Anja's reply only if `:let_confess`); the sleep trigger for "Midnight" (V133 == 5) and for Interlude III (V133 == 8); 322's clerk and terminal (V133 >= 7); 323 the sky-river guides (Waterfall, from V133 >= 8); the child, the dock-hand, the clerk at the lift.
**325 Gale Post Hall** — pigeonhole walls, overhead sack rails (decor animation), Pelipper/Corvisquire doors; "Guest of the Post" autorun (V133 2 → 3): Larch at the sorting table, Odessa on the rope; **the raid** state (V133 == 6 → 7): sacks spilled, couriers with hands up, 6 officers, Marchetti on the catwalk with Manectric, the battle; the round doors showing the skiff drop (a scripted move route on 326 seen through the doors, or a short cut to 326). From V133 >= 7: the archive noise trigger to 334.
**326 Smugglers' Gantry** — the skiff (event sprite: wing, basket, rope), "Flight Safety" (touch, V133 3 → 4), the puddle and Kit (mirror gag, once); the skiff's empty mooring from V133 >= 7.
**330–333 Gale Post gym (Gym 11)** — doors open at V133 >= 4; as GYM_PUZZLES Gym 11; Kit's hints; **Odessa (333), double**, her three mid-battle lines, POSTMARK BADGE, TM51; V133 = 5.
**334 Dead-Letter Archive** — as GYM_PUZZLES Mastery; the ABROAD hole with the black-ribbon bundle (V133 < 7), then empty; **K5** (V133 == 7 → 8): letters ankle-deep (floor decor), Kestrel at the ABROAD hole with the gauntlet, the battle, the ladder exit (move route), the falling letter (a small animated event), `:ch12_letter` (the lamp on the desk; Kit at the door; Odessa's entrance).
**744–746 Stormwatch Spire** — the "Midnight" route over the roofs (a short cutscene or a rooftop map; the checkpoint), 744/745 the maintenance stair with wild encounters and two guards, the board, **the core housing** (a big event on 745; it shifts once when the PC passes, and the shard line); **746 the Roof**: relay dishes, the glass booth, the storm overhead (fog), the broadcast autorun (V133 5 → 6, S131), the screen cuts (pictures of five earlier places), the bomb (flash, shake, the north dishes to a wrecked state), the stair down; the **SPLITTER CASING** pickup on 745.
**Meridian Spire, Voss's office** [NEW; Lumen] — glass wall over Lumen at night (panorama), the desk with the kettle and two mugs, the photograph, the arena model, the pin, the left drawer (GO_FINE_PRINT), Calla by the door, the contract; Interlude III's party swap and V119 (3 → 0).
**740 Conductors' Causeway** — pylons, wires, a marsh; the first puddle (the reflection autorun, V133 9 → 10, V102 = 13): the PC's reflection as a mirrored event that turns its head on a half-second delay (a move route with a wait of 15 frames).

**Trainer designer:** none new (Odessa, Marchetti Ch12 and K5 are in `pbs/trainers.txt`). **Items owner:** SPLITTER CASING (Key Item, for Ch13/Ch14), MORWEN'S LETTER (Key Item, `:keep`; for Ch15). **Badge name (proposed):** the **Postmark Badge**.
