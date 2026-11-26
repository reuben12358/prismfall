# Pokémon Prismfall — Ruin Route script: the Gilded King (R3, R6, R7)

> The three scenes where **Gilded King Aurelius** (*King Aurelius Aurel*, First Sovereign of drowned Aurelia) speaks.
> Ruin Route only (`story/12_RUIN_ROUTE.md`). Source: Gemini's rework
> (`gemini_recommends/2026-11-23_gilded-king-aurelian-gilgamesh-rework/PROPOSAL.md` §2–§3, creator-locked Path B
> "Aurelius"; internal ids and art renamed to GILDED_AURELIUS / AURELIUS on 2026-11-24), adapted to Path B: the King is **Aurelius**; **Aurelian** is only ever Voss.
>
> **Wiring.** `[portrait: AURELIUS, <expr>]` shows the AURELIUS_* portraits under the name "Gilded King Aurelius"
> (Cutscenes `014_Portraits.rb`). His battle is `[GILDED_AURELIUS,Aurelius]` (v0 / 100 / 200) on `:PRISM_ARENA` running
> Inverse, with the gold VS screen (EBDX Bridge `010_Bridge_VersusIntro.rb`) and his mid-battle barks (Z-Power
> `006_ZPower_TrainerBarks.rb`). Map events named "Aurelius" wear his overworld sprite (`025_CharsetAliases.rb`).
>
> **Voice.** Archer Gilgamesh's *personality* only, grounded in Velmora (Reuben, 2026-11-24): **no** golden portals, **no**
> summoned or floating weapons, no Fate names or romaji. Effortless, lounging amusement; casual, absolute possessiveness;
> never a rant. "Mongrel" is for counterfeits, panicking crowds, and the PC up to Gilt's send-out; it is dropped for good
> once Gilt is cornered, in his LoseText and after the battle. His words: *my treasury, the Chain, counterfeit, know your
> station, my court, the original*. One to three short sentences a box.

---

## R3 — Drowned Aurelia: the Sun Court Below (Map 826, the Mirrorwalk)
*(Replaces 12_RUIN_ROUTE R3 beats 3–4 and the game-over hook. After Gym 16 (Ruin).)*
```
(Under green sea-glass light the drowned throne room stands silent. The Gilded King's throne rises out of coral-crusted marble. Its armrests, open hands on the main route, are clenched golden fists now.)
[portrait: REFLECTION, neutral] (quietly, from your shadow) We've done that one.
[name: Reflection] The hands remember closing.
(Inspect the throne: "Sit on the Gilded King's throne?" Yes: you sit. Nothing closes. Only a faint, amused scrape from the mirror-wall at the throne's back.)
[portrait: AURELIUS, smug] (a dry voice through the glass, calm as poured wine) ...Oh? Already learned not to put your fingers in a king's seat?
[portrait: AURELIUS, happy] Pity. My artificers spent six months on those armrests.
(The mirror-wall is not a reflection of the ruins. It is a window into AF 0: the Sun Court in dry midsummer gold, banners taut in mid-air, Gilders frozen mid-chant, sparks hung like dust, and at its centre King Aurelius Aurel, the blazing Gilded Chain in his hands, mid-command.)
(Nothing behind the glass moves. Not a banner. Not a mote of light.)
(Then his golden eyes slide sideways and lock onto you. Slowly, while his whole court stays frozen in midsummer dust, only King Aurelius lowers the Chain with a bored sigh and strolls down his dais to lean against the inside of the glass.)
[portrait: AURELIUS, smug] Well, now. No tribute, no bowed head.
[name: Gilded King Aurelius] Who gave you leave to wander into my court, mongrel?
[portrait: AURELIUS, neutral] Wait... no colour in your chest. No tint in your step.
[name: Gilded King Aurelius] And standing behind your heel...
(His gaze drops to the Reflection at your shoulder, and his amusement sharpens into real interest.)
[portrait: AURELIUS, happy] Ha! Twenty-three graves, and you wear your own corpse for a shadow.
[name: Gilded King Aurelius] Three centuries of drowned fish, and at last something worth looking at.
(SFX: a hydraulic hiss. The pressure-door shears open; Meridian floodlights cut across the marble. Aurelian Voss steps into the air-pocket, helmet under his arm, and stops dead at the sight of the Sun Court.)
[portrait: VOSS, shocked] [emote: exclaim] ...No.
(His case slips from his fingers and clangs on the marble. For the first time in the game, the calmest man in Velmora drops to both knees.)
[portrait: VOSS, crying] He's alive.
[name: Voss] Three hundred years, behind the glass, he's still alive...
[name: Voss] Your Majesty. House Aurel kept the notebooks.
[name: Voss] I built the Spire on your foundations. I brought back the cradle.
(Behind the glass the King tilts his chin down at the kneeling man in charcoal wool and a pressure-collar. The smile doesn't fade. It turns cold as winter gold.)
[portrait: AURELIUS, deadpan] ...Stand up, whatever you are.
[name: Gilded King Aurelius] You're getting mud on my reflection.
[portrait: AURELIUS, smug] "House Aurel"? In that mourning-coat?
[name: Gilded King Aurelius] You pitched a shopkeeper's tower on my drowned roof, and you expect applause, like a clerk who stole the silverware during a fire.
[portrait: VOSS, shocked] I built the Engine! Eighteen pylons in Crownhaven!
[name: Voss] Better than metal, my lord. It only needs the cradle.
[portrait: AURELIUS, neutral] (two fingers, waved lazily, without looking at him) Then fetch your little brass toy and set the stage, mongrel.
[name: Gilded King Aurelius] Even a stray hound can carry a bone to the right door.
(Voss doesn't hear the contempt, or won't. His salvage team hoists the keystone cradle and retreats to the submarine lock.)
[portrait: VOSS, happy] It will be ready at the Coronation, Your Majesty.
[name: Voss] Every lock. Every light.
(The lock seals. Only you, your Reflection and the King behind the glass remain. He rests one gauntleted palm lightly against the inside of the mirror, opposite your chest.)
[portrait: AURELIUS, smug] Look at him.
[name: Gilded King Aurelius] Three hundred years, and my bloodline prays to a ghost in a pane of glass.
[portrait: AURELIUS, neutral] You, however, did not kneel.
[name: Gilded King Aurelius] You did not even lower your eyes.
(A slow, dangerous grin: a sovereign spotting the first challenger in three centuries who might make him sit up.)
[portrait: AURELIUS, happy] Bring that little tin crown to Crownhaven, hollow thing.
[name: Gilded King Aurelius] Let the merchant finish building my door.
(His fingers close on the Chain. One word, through the glass, like struck gold:)
[portrait: AURELIUS, smug] "Finish."
```

## R6 — Crownhaven, the Night of Masques (Ruin variant)
*(12_RUIN_ROUTE R6 beat 6. The main route's play (39_SCRIPT_CH20) runs until the King's line.)*
```
(Midnight. Fewer lanterns than on the main route; the crowd keeps three paces from the Renegade in the front row. Celestine has just finished Maren's lament from the wings, her eyes on you, when the actor playing the Gilded King sweeps forward in crimson velvet. Behind him, set into the painted Sun Court, stands Dorian's tallest dressing-room mirror, placed to catch the torchlight.)
[name: The Gilded King (actor)] Let priests measure their gratitude in crumbs!
[name: The Gilded King (actor)] If heaven will not kneel, we'll—
(The torches flicker and burn metallic gold. The stage mirror stops reflecting the square: a golden throne room opens inside the frame, and a tall figure in black-and-gold armour strolls up to the glass behind the actor's shoulder.)
(The actor freezes. His painted chain clatters across the boards. In the wings, Dorian goes white.)
[portrait: DORIAN, shocked] [emote: exclaim] ...That isn't a lighting cue.
[name: Dorian] Somebody drop the... drop the curtain!
(The ropes won't move. Inside the mirror the King leans on the gilded frame, one elbow propped, like a patron at a rehearsal.)
[portrait: AURELIUS, smug] Passable velvet, actor.
[name: Gilded King Aurelius] Though you play my laugh far too humbly.
[portrait: AURELIUS, deadpan] And tell whoever stitched that crown that my goldsmiths went off the sea-cliffs for proportions that sloppy.
(Gasps. The Wardguard reach for Poké Balls and freeze: every shield, every lantern pane, every Basilica window shows the same golden gaze looking down at them.)
[portrait: AURELIUS, deadpan] Lower those Poké Balls, mongrels.
[name: Gilded King Aurelius] Did I grant you leave to interrupt my play?
[portrait: AURELIUS, neutral] Ansel Crewe, was it? The playwright they hanged for remembering me?
[portrait: AURELIUS, happy] A decent second act. A cowardly third.
[name: Gilded King Aurelius] He has me weeping as Aurelia sinks. How tedious.
[name: Gilded King Aurelius] When the sky broke over my head, I did not weep. I applauded.
(Celestine steps out of the wings, pale, unable to lie even now.)
[portrait: CELESTINE, shocked] ...You're not a memory.
[name: Celestine] The Glass kept you whole.
[portrait: AURELIUS, smug] A truth-speaker? Charming. Maren's songbirds still keep their feathers.
[name: Gilded King Aurelius] Sing your third verse, little bird, if you have the stomach.
(His eyes pass the stage lights, Dorian, the Wardguard, Voss trembling in the Meridian box, and settle squarely on you.)
[portrait: AURELIUS, happy] Ah. There sits my real audience.
[portrait: AURELIUS, smug] Every Plate in this realm was mine before your grandparents learned to draw breath.
[name: Gilded King Aurelius] Beat the tired old caretaker tomorrow, hollow one, pick up my little silver hoop... and try not to bore me when the curtain rises for real.
(He snaps his fingers inside the glass. Every torch in the square dies. When the lanterns relight, the mirror shows only frightened faces, and one hairline golden crack shaped like a crown.)
[portrait: DORIAN, panic] ...Thirty years in the theatre, darling, and I have never had a review from the title character.
```

## R7 — Crownhaven Temple-Arena: the Hijack (Map 491, `:PRISM_ARENA` + Inverse)
*(12_RUIN_ROUTE R7 beats 1–4.)*

### The mirror breach
```
(Valen lies spent on the flagstones. No Warden lifts the Sovereign's Crown; you pick it up off the arena floor yourself. The moment your fingers touch it, the Arbiter Engine's eighteen pylons roar awake: not Meridian blue, but old Aureate gold.)
(Every crystal panel round the arena turns to a mirror. In every pane stands the frozen Sun Court, and then, all at once, every reflection moves.)
(SFX: glass shattering in reverse, like bells chiming upward. A golden boot steps out of the central pylon, trailing eighteen links of humming gold chain. Behind him the sky over Crownhaven splits into inverted gold-and-violet glass.)
[portrait: VOSS, happy] (stumbling onto the floor in his Engine-harness, arms open) Your Majesty! Look at what House Aurel built for you!
[name: Voss] Eighteen locks, calibrated to the splinter. No crude iron: pure current!
[name: Voss] The god will have nowhere left to—
(The King doesn't break stride. He stops three paces from Voss, taps a steel conduit on the harness with the back of a gilded knuckle (a hollow, tinny clink) and laughs once, dry as salt.)
[portrait: AURELIUS, smug] ...That's it?
[portrait: AURELIUS, deadpan] Three hundred years, and this tin-plated parlour trick is what House Aurel calls ambition?
[portrait: VOSS, shocked] My lord? It draws on all eighteen Imprints. I spent thirty years—
[portrait: AURELIUS, angry] You built a shopkeeper's tower on my drowned roof, wired a clerk's harness out of scraps from my sewers, and crawled to my glass on your knees!
[portrait: AURELIUS, smug] And they named you for me. "Aurelian": heir of Aurelius.
[name: Gilded King Aurelius] A copper coin stamped with the sovereign's face.
[portrait: AURELIUS, neutral] Know your place, mongrel.
(With a lazy flick of his gauntlet he catches Voss by the steel collar of the harness, snapping the straps clean, and flings the chief executive of Meridian twenty feet across the flagstones into the Arbiter Engine's burning golden perimeter.)
[portrait: VOSS, panic] No, Your Majesty, I'm your heir—!
[portrait: AURELIUS, deadpan] A king has no heirs while he is standing in the room.
```
*(The Aurelian / Aurelius line is the payoff of 09 #8 on this route; Voss's given name is never spoken by the King before R7.)*

### `GO_R_KNEEL` ("Long Live the King") and `:ruin_voss`
```
(The King turns his back on Voss, already bored, and faces you across the humming keystone cradle. The inverted light of the eighteen Plates moves across his crown.)
[portrait: AURELIUS, smug] Now, then. The clerk is out of the way, and the sky is already listening.
[portrait: AURELIUS, neutral] Every Plate, every crown, every worthy specimen in this land was mine before your grandparents learned to breathe. I am merely collecting interest.
[portrait: AURELIUS, smug] You walked through twenty-three graves to open my door.
[name: Gilded King Aurelius] A finer errand than any servant I left in the salt.
(He holds out one open, gauntleted hand: not Voss's offer of partnership, a monarch granting an audience.)
[name: Gilded King Aurelius] Kneel, mongrel. Set that little hoop at my feet, and I will be generous.
[name: Gilded King Aurelius] I am always generous to things that know their station.
(At your shoulder, Giratina's presence coils cold behind the Black Case: a warning in the glass.)
> Kneel. (GO_R_KNEEL)
  (You drop to one knee and lay the Crown on the gold flagstones. His smile widens, neither cruel nor kind: a collector closing a velvet box.)
  [portrait: AURELIUS, happy] Good.
  [name: Gilded King Aurelius] You see how simple the world is when things return to their rightful owner?
  (Every mirror in Crownhaven breaks inward at once. Golden banners pour out of the glass. Three hundred years of drowned Aurelia step back into the sunlight, and the Chain closes round your ribs like an armrest.)
  Script: Prismfall.game_over(:GO_R_KNEEL)
> Refuse.
  (You don't kneel. You toss the Crown aside onto the flagstones, where it rings once and goes still. Behind you the Black Case hums with colourless emptiness.)
  (For a heartbeat his brows lift. Then he laughs, a bright, terrible sound that shakes the stadium glass.)
  [portrait: AURELIUS, happy] Ha! Look at those eyes.
  [name: Gilded King Aurelius] Not a shred of fear, not a whisper of devotion!
  [portrait: AURELIUS, smug] A moment. Before I crush you: your little benefactor is burning in my Chain.
  (By the southern pylon Voss hangs in the golden links, smoke curling off his sleeves, reaching blindly for the floor.)
  [portrait: VOSS, crying] ...Help... please...
  [name: Voss] it wasn't supposed to be like this...
  > Pull Voss out of the Chain. (spare)
    Script: pf_choose(:ruin_voss, :spare)
    (You step into the golden arcs, your colourless shard eating the burn, and haul him clear. He collapses on the marble, breathing hard, every trace of Meridian's poised chief executive gone.)
    [portrait: AURELIUS, smug] Mercy for a counterfeit? Soft. Or merely tidy.
    [name: Gilded King Aurelius] Still, bare-handed through my Chain without flinching...
    [name: Gilded King Aurelius] you do have nerve.
  > Leave him to the Chain. (abandon)
    Script: pf_choose(:ruin_voss, :abandon)
    (You don't turn your head. The Chain tightens and swallows him into the Engine's glare.)
    [portrait: AURELIUS, happy] Cold as glass.
    [name: Gilded King Aurelius] Not a glance for the man who handed you your badge case on the ferry!
    [name: Gilded King Aurelius] Good. Kings do not trip over broken tools.
```
*(GO_R_KNEEL epitaph, Core `012_Narrative_Data.rb`: "You knelt. The Aureate Kingdom stepped through the Glass, golden and unrepentant, and King Aurelius finished his sentence.")*

### The challenge
```
(He steps back onto the centre ring and lifts a single gilded Poké Ball in a relaxed, raised palm, the Chain's links chiming softly across his breastplate. Round the stadium rim all eighteen crystal pylons of the Arbiter Engine flare Aureate gold together; the Prism field turns inside out: strengths to weaknesses, the Crownhaven sky to cold inverted gold.)
[portrait: AURELIUS, smug] Look up, mongrel.
[name: Gilded King Aurelius] Let us see what three hundred years of mortal mediocrity has produced.
[portrait: AURELIUS, neutral] You mean to unmake the sky?
[name: Gilded King Aurelius] To erase the eighteen Plates I spent a kingdom's blood to claim?
[portrait: AURELIUS, happy] Hahaha! Audacious! Unforgivable! Utterly magnificent!
[portrait: AURELIUS, angry] Stand your ground, insolent mongrel!
[name: Gilded King Aurelius] Face the First Sovereign of Aurelia and prove you have the spine to look heaven in the eye!
BATTLE: Prismfall::Festival.next_match (stage :HIJACK on the Ruin Route) -> [GILDED_AURELIUS,Aurelius] on :PRISM_ARENA, the event layering Inverse. Gold VS screen (AURELIUS). LoseText: "Ha...! Magnificent! Three hundred years, and at last a challenger. Go—end the sky."
```
**His team, the treasury** (`tools/trainer_gen/gen.py`, BALANCE.md): Sunguard (Golurk, the original of Voss's "Gilder"),
Regalia (Aegislash), Deluge (Kyogre) and Sunder (Groudon): the Year of Two Weathers, Colossus (Regigigas), Gilt
(Gholdengo, Lv 100). No Mega Ring: the rings came three centuries after him.

**Barks in battle** (Z-Power `006_ZPower_TrainerBarks.rb`; each once per battle; his Pokémon and his manner, never
portals): Sunguard's send-out ("Witness the original, mongrel."), the end of the first round on the inverted arena ("Look
up, mongrel. Even heaven's own laws bow backward in my court..."), Regalia's ("Every petty king since Aurelia sank has
worn tin and called it regalia..."), the first titan ("...I collared the sea and the earth merely to tend my gardens!"),
Colossus ("I grant you five heartbeats, mongrel..."), Gilt's send-out ("Hahaha! Well played, mongrel!": the last time he
says the word), and Gilt under a third of its HP ("Hahaha! Yes! That cold, unflinching glare...").

### After the battle (right before Arceus descends)
```
(Gilt shatters into a cascade of old Aureate coins that melt into light before they reach the marble. The King staggers half a step, stops himself and straightens. Hairline cracks of white light race across his armour and his crown.)
[portrait: AURELIUS, happy] ...Ha. Haha... hahaha!
(He wipes a fleck of golden glass-dust from his cheek, and looks at you with no bitterness at all: only fierce satisfaction.)
[portrait: AURELIUS, smug] Do you know how long I stood behind that mirror, watching ten generations of sheep polish the bars of my daughter's cage?
[portrait: AURELIUS, neutral] Voss wanted a better furnace. Valen wanted another decade of quiet.
[name: Gilded King Aurelius] Even my Maren only wanted the sky to forgive her.
[portrait: AURELIUS, happy] And then you walk in with nothing in your chest (no prayer, no crown, no pity) and break my court to pieces just to reach the throat of heaven.
(Above the arena the clouds tear open. White Judgment light pours down through the inverted sky: not dragged by the Chain, descending of its own will. The eighteen locks howl.)
(His reflection begins to come apart from the heels up, in flakes of gold leaf. He doesn't flinch. He raises one gauntlet in a brief, mocking, entirely sincere royal salute.)
[portrait: AURELIUS, smug] Your turn, sovereign of nothing.
[portrait: AURELIUS, happy] Do not dare lose after beating me.
[name: Gilded King Aurelius] Make the Original One remember what mortal defiance looks like!
(A last chime of breaking gold, and King Aurelius Aurel disperses back into the Glass, leaving you alone under the descending light of Arceus.)
```
*(Then 12_RUIN_ROUTE R7 beat 5: Arceus descends; Valen holds the Ring one last time.)*

---

## How he sees the others (Gemini §2.3, for future scenes)
- **Voss:** a counterfeit. He inherited the grudge without the sovereignty.
- **The Renegade PC:** R3 curiosity, R6 his real audience, R7 a lazy test, then exhilarated recognition.
- **Arceus:** the only worthy rival. It broke itself rather than wear a collar; he respects that much, "which is why I intend to finish the argument."
- **Dorian and Ansel Crewe's play:** delightful, slightly timid theatre.
- **Valen:** pitying scorn. "Ten generations of clerks polishing the bars of their own cage, and calling the bruise 'duty.'"
- **Princess Maren:** the one mortal he never calls a mongrel. "My daughter was the only soul in Aurelia who dared tell me no without lowering her chin. Pity she built a monastery out of her backbone."
- **Staging guardrail:** personality only, never Fate powers. He never opens golden portals or summons floating swords; his dominance is his bearing, his words, the Arbiter Engine's pylons and Chain, and his six Pokémon.
