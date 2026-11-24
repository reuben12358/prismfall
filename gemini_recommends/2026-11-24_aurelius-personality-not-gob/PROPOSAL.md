# Proposal: Gilded King Aurelius — Pure Archer Gilgamesh Personality Audit (Zero Gate of Babylon)

- **Date:** 2026-11-24
- **Status:** Ready-to-apply spec for Claude (Wednesday sprint) — **zero edits made to `.rb`, `story/`, or `pbs/`** per freeze discipline.
- **Supersedes (on R7 staging & voice):** `gemini_recommends/2026-11-23_gilded-king-aurelian-gilgamesh-rework/PROPOSAL.md` §3D3–§3D4 and the scrapped Wave 7 Gate-of-Babylon cutscene in `gemini_recommends/2026-11-24_art-drop15-npcs-and-ch17-21-wiring/PROPOSAL.md:301`.

> [!IMPORTANT]
> **CREATOR DIRECTIVE (`2026-11-24`):**
> *"task 3: I told u to give gilgamesh's personality to the gilded king, not have him use gilgamesh's gate of babylon :sob: just his personality (like him using zasshu to refer to mongrels, etc)"*
>
> **Hard Rule Going Forward:** **Archer Gilgamesh's PERSONALITY ONLY** (*Fate/stay night*, *Fate/Grand Order: Babylonia*, *Fate/strange Fake*) — **ZERO** Gate of Babylon golden portals, **ZERO** floating swords/halberds, **ZERO** Enkidu-from-portals choreography, and **ZERO** Fate magic gimmicks. King Aurelius Aurel is 100% grounded in **Pokémon Prismfall's world**: a 300-year-old Velmoran sovereign commanding his six gilded Pokémon (`Sunguard` Golurk, `Regalia` Aegislash, `Deluge` Kyogre, `Sunder` Groudon, `Colossus` Regigigas, `Gilt` Gholdengo) and the Arbiter Engine's eighteen crystal pylons through sheer royal arrogance.

---

## 1. Forensic Repo Audit — Clean vs. Literal Gate of Babylon Bleed

Every file, plugin, PBS entry, art asset, and movie referencing **Aurelius / `THEODRIC` / `GILDED_THEODRIC` / the Gilded King** was audited line-by-line across the repository.

### 1.1 Confirmed Gate of Babylon / Fate-Magic Bleed (MUST PURGE)

| # | File & Location | Exact Current Content | Diagnosis | Required Fix |
|---|---|---|---|---|
| **1** | `Movies/pf_ruin_r7_aurelius_mirror_pierce(_safe).ogv`<br>`art/out/Movies/pf_ruin_r7_aurelius_mirror_pierce(_safe).ogv`<br>`gemini_recommends/2026-11-24_art-drop15-npcs-and-ch17-21-wiring/PROPOSAL.md:301` | Scrapped Wave 7 anime cutscene showing Aurelius summoning literal golden Gate-of-Babylon portals & floating weapons/halberds. | **CRITICAL BLEED (SCRAPPED).** Direct violation of creator directive. Verified **never wired** into `plugins/Prismfall Cutscenes/016_Movies.rb`! | **Confirm scrapped.** Parent is deleting the `.ogv` files; also verify `art/out/Movies/` mirror copies are removed, strike Wave 7 from `2026-11-24_art-drop15` §7.2, and **never** wire into `016_Movies.rb` or `tools/package.sh`. |
| **2** | `story/42_SCRIPT_RUIN_KING.md:134`<br>*(origin: `2026-11-23` proposal line 449)* | `(He steps back onto the centre ring. Eighteen golden portals ripple open behind his cape like mirrored shields; the Prism field inverts: strengths to weaknesses, the sky to inverted gold.)` | **DIRECT BLEED.** Verbatim Gate of Babylon visual choreography (golden ripples fanning behind his cape) leaked from the Nov 23 proposal into Claude's live script! | **PURGE & REPLACE (§3.6 below):** Aurelius raises one gilded Poké Ball in an unhurried palm (matching `GILDED_THEODRIC.png` / `VS/THEODRIC.png`) as the Arbiter Engine's **eighteen physical crystal pylons** around the arena rim flare gold and invert `:PRISM_ARENA`. |

### 1.2 Borderline Echoes & Continuity Polish (RECOMMENDED TIGHTENING)

| # | File & Location | Exact Current Content | Diagnosis | Required Fix |
|---|---|---|---|---|
| **3** | `story/42_SCRIPT_RUIN_KING.md:95` | `(Two links of the Chain lash out of the crystal like whips, snap the harness straps and throw the chief executive of Meridian twenty feet across the arena into the Chain's burning perimeter.)` | **Minor Enkidu-portal echo.** Chains whipping *"out of the crystal"* visually brushes against Gilgamesh firing Enkidu out of golden portals. | **Tighten (§3.4 below):** Keep it physical & Prismfall-native — Aurelius flicks the physical Gilded Chain already trailing from his own gauntlet (or catches Voss by the collar and flings him effortlessly) into the Engine's golden containment perimeter. |
| **4** | `plugins/Prismfall Z-Power/006_ZPower_TrainerBarks.rb:20–21`<br>`story/42_SCRIPT_RUIN_KING.md:146` | `"A thousand blades were forged after Aurelia sank. Every one a crude copy of mine."` | **Subtle Fate "prototype blade hoard" echo.** Slightly evokes GoB's endless sword vault rather than his actual Aegislash Pokémon. | **Tighten (§4 below):** Ground 100% in Velmoran kingship and Aegislash's royal Pokédex heritage (*"Every petty king since Aurelia sank has worn tin and called it regalia..."*). |
| **5** | `story/12_RUIN_ROUTE.md:79` | `His team is the Gilders' court: Golurk, Aegislash, Gholdengo-gold reflections of Wardens' aces, on :PRISM_ARENA running Inverse.` | **Stale outline note** (no GoB bleed, just out of sync with finalized PBS team). | **Optional 1-line sync:** Update to `Golurk, Aegislash, Kyogre, Groudon, Regigigas and Gholdengo ("Gilt")`. |

### 1.3 Verified 100% Clean Files & Visual Assets (ZERO GoB Bleed)

| Scope | Audited Files & Lines | Verdict | Notes |
|---|---|---|---|
| **PBS & Trainer Gen** | `pbs/trainers.txt:15070–15220` (`v0`, `100`, `200`), `pbs/trainer_types.txt:420–426`, `tools/trainer_gen/gen.py:1155–1177` | **CLEAN** | All 6 Pokémon (`Sunguard` Golurk, `Regalia` Aegislash, `Deluge` Kyogre, `Sunder` Groudon, `Colossus` Regigigas, `Gilt` Gholdengo), moves, items, and 82-char `LoseText` (`"Ha...! Magnificent! Three hundred years, and at last a challenger. Go—end the sky."`) are 100% canonical Pokémon + Velmora lore. Zero Mega Ring (canon per `design/MEGA_EVOLUTION.md:388`). |
| **Trainer Barks Code** | `plugins/Prismfall Z-Power/006_ZPower_TrainerBarks.rb:1–112` | **CLEAN of portals** *(personality upgrade in §4)* | Zero portals, zero Fate names, clean Ruby hooks (`:sendout`, `:round1`, `:ace_low`). Currently only uses `"mongrel"` **once** in the whole fight (`:GOLURK`); §4 dials up unmistakable Gilgamesh arrogance, possessiveness, and booming laughter without touching any hook logic. |
| **Core & Cutscene Plugins** | `008_Festival_Data.rb:61`, `012_Narrative_Data.rb:114,415`, `015_Festival_Draw.rb:47`, `025_CharsetAliases.rb:31–33`, `014_Portraits.rb:96,865`, `016_Movies.rb`, `010_Bridge_VersusIntro.rb:48,69` | **CLEAN** | `:GILDED_THEODRIC => "THEODRIC"` (`:gold` VS screen), `Portrait.register(:THEODRIC, name: "Gilded King Aurelius")`, `GO_R_KNEEL` epitaph, and `016_Movies.rb` (no Wave 7 entry) are all clean. |
| **Story Bible & Main Scripts** | `01_WORLD_LORE.md:17–25,42`, `03_CAST.md:362`, `10_CHOICES_ENDINGS.md:287–422`, `12_RUIN_ROUTE.md:7–93`, `20_SCRIPT_CH0-2.md:1224–1240`, `25_SCRIPT_CH6.md:312–328`, `33_SCRIPT_CH14.md:381–391`, `36_SCRIPT_CH17.md:240–295`, `39_SCRIPT_CH20.md:304–328`, `40_SCRIPT_CH21.md:17,110` | **CLEAN** | Zero Fate portals or weapons anywhere. Lines like Dorian's *"A king who looked up at the sky and decided it was trespassing on his skyline"* and Sahar's *"He isn't praying. He's giving the sun an order"* are pure gold. |
| **Visual Art Assets** *(directly inspected)* | `graphics/Trainers/GILDED_THEODRIC.png`, `graphics/EBDX/VS/THEODRIC.png`, `graphics/Portraits/THEODRIC_{smug,happy,angry,deadpan}.png` | **CLEAN** | Black-and-gold armored sovereign with sunburst crown and golden chain, raising a **gilded Poké Ball** in a relaxed, elevated palm. Zero portals, zero floating weapons. His `smug` and `happy` portraits already radiate effortless Gilgamesh composure! |

---

## 2. Sharpening His Pure Archer Gilgamesh Personality

### 2.1 Localization Note: *Zasshu* → Natural English `"mongrel"`
- In English-language Pokémon Prismfall (crisp, literary UK-English prose: *colour, centre, armour, parlour*), **never** insert romaji `"Zasshu!"` — that breaks Velmora's tone into parody.
- Instead, deliver the exact *zasshu* rhythm through **natural, surgical English `"mongrel"`**:
  - `"Who gave you leave to raise your eyes to me, mongrel?"`
  - `"Lower those Poké Balls, mongrels."`
  - `"Know your place, mongrel."`
  - `"Look up, mongrel."`
  - `"Hahaha—well played, mongrel!"` *(the final time he ever uses the word — right before genuine respect replaces it!)*

### 2.2 Four Pillars of Aurelius's Voice (Personality Audit Gaps Fixed Below)

1. **Present From Scene 1 (Fixing the R3 Gap):** In the current `story/42_SCRIPT_RUIN_KING.md`, Aurelius never uses `"mongrel"` once during his entire R3 debut or R6 theatre review, and only uses it once in the entire 6-Pokémon R7 battle. Introducing it sharply in **R3** (toward both the trespassing PC and kneeling Voss) and **R6** (dismissing the panicking Wardguard) locks in his unmistakable cadence immediately.
2. **Casual, Absolute Possessiveness (*"Everything Worth Having Was Already Mine"*):** Archer Gilgamesh treats every crown, treasure, and extraordinary creature in the world as property on loan from his vault. In Velmora, that means framing the **eighteen Plates, the Sovereign's Crown, Crownhaven itself, and legendary Pokémon** as Aurelia's overdue assets — *"Every Plate, every crown, every worthy specimen in this land was mine before your grandparents learned to draw breath. I am merely collecting interest."*
3. **Lounging, Perceptive Theatrical Wit (*Fate/strange Fake* Energy):** He is never frantic, never shouts to feel intimidating, and reads people's souls in two seconds beneath a relaxed smile. While the entire Sun Court stands frozen behind Antumbra's Glass, *only* Aurelius lazily uncrosses his stance and strolls down to lean against the mirror like a patron at a play. His anger flashes **only** at cheap counterfeits pretending to his majesty (Voss).
4. **Earned Booming Laughter (`"Hahaha—well played, mongrel!"` → `"challenger"`):** Contempt flips into genuine, roaring joy **only** when the Renegade PC breaks through his court and titans without flinching. Once `Gilt` enters and gets pushed below a third of its HP (`:ace_low`), `"mongrel"` **disappears permanently** — replaced by `"challenger"` and `"sovereign of nothing"`, culminating in his unbothered, sincere royal salute before Arceus descends.

### 2.3 Exact `"mongrel"` Progression Arc (Synced Across Script & Barks)

| Beat | How Aurelius Addresses the PC / Others | Tone |
|---|---|---|
| **R3 — Sun Court Mirror** | PC: `"mongrel"` → `"hollow thing"` · Voss: `"clerk"`, `"mongrel"` | Divine boredom broken by mild curiosity; freezing scorn for his kneeling descendant. |
| **R6 — Night of Masques** | Wardguard: `"mongrels"` · PC: `"my real audience"`, `"hollow one"` | Relaxed, razor-witted royal patron reviewing his own banned play. |
| **R7 — Mirror Breach & Offer** | Voss: `"mongrel"` · PC: `"mongrel"` (`"Kneel, mongrel."`) | Imperious contempt for a counterfeit; lazy test of an audacious mortal. |
| **R7 Battle — Opening (`Sunguard` → `Colossus`)** | PC: `"mongrel"` (`Sunguard`, `:round1`, `Regalia`, `Colossus`) | Effortless aristocratic superiority commanding his gilded Pokémon court & ancient titans. |
| **R7 Battle — Pivot (`Gilt` Send-Out)** | **`"Hahaha—well played, mongrel!"`** *(final use!)* | Sudden, booming Gilgamesh delight — scorn cracks open into exhilarating recognition. |
| **R7 Battle — Cornered (`:ace_low`), `LoseText`, Post-Battle** | **ZERO `"mongrel"`** → `"challenger"`, `"sovereign of nothing"` | Pure earned respect for mortal willpower that dares stare down heaven itself. |

---

## 3. Exact Drop-In Upgrades for `story/42_SCRIPT_RUIN_KING.md`

> Matches Claude's existing UK spelling (`colour`, `centre`, `armour`, `parlour`), `[portrait: THEODRIC, <expr>]` tags, and 1–3 short sentences per Essentials message box. Every beat not listed below (including R7's Voss roast lines 89–97, `:spare`/`:abandon` reactions lines 124/128, and the R7 Post-Battle salute lines 154–165) is **already 10/10 and stays verbatim**.

### 3.1 Header Voice Note (Replaces lines 13–15)
```markdown
> **Voice.** Pure Archer Gilgamesh *personality* grounded 100% in Velmora — **zero** Gate of Babylon portals, **zero**
> summoned weapons, **zero** Fate names or romaji. Effortless, lounging amusement; casual supreme possessiveness; never
> a rant. Natural English "mongrel" is for counterfeits, panicking crowds, and the PC up through Gilt's send-out —
> dropped permanently once Gilt is cornered (`:ace_low`), in `LoseText`, and post-battle. His words: *my treasury, the
> Chain, counterfeit, know your station, my court, the original*. One to three short sentences a box.
```

### 3.2 R3 — Drowned Aurelia: The Sun Court Below (Replaces lines 28–52)
*Upgrades: adds his lounging unfreeze behind the glass, his first breezy `"mongrel"` appraisal of the trespassing PC, and sharper possessive contempt toward kneeling Voss.*

```text
(Nothing behind the glass moves. Not a banner. Not a mote of light.)
(Then his golden eyes slide sideways and lock onto you. Slowly—while his entire court remains frozen in midsummer dust—only King Aurelius lowers the Chain with a bored sigh and strolls down his dais to lean casually against the inside of the glass.)
[portrait: THEODRIC, smug] Well, now. No tribute, no bowed head—who gave you leave to wander into my court, mongrel?
[portrait: THEODRIC, neutral] Wait... no colour in your chest. No tint in your step. And standing behind your heel...
(His gaze drops to the Reflection at your shoulder, and his amusement sharpens into genuine intrigue.)
[portrait: THEODRIC, happy] Ha! Twenty-three graves, and you wear your own corpse for a shadow. Three centuries of drowned fish, and at last something worth looking at.
(SFX: a hydraulic hiss. The pressure-door shears open; Meridian floodlights cut across the marble. Aurelian Voss steps into the air-pocket, helmet under his arm, and stops dead at the sight of the Sun Court.)
[portrait: VOSS, shocked] ...No.
(His case slips from his fingers and clangs on the marble. For the first time in the game, the calmest man in Velmora drops to both knees.)
[portrait: VOSS, crying] He's alive. Three hundred years, behind the glass, he's still alive...
[portrait: VOSS, neutral] Your Majesty. House Aurel kept the notebooks. I built the Spire on your foundations. I brought back the cradle.
(Behind the glass the King tilts his chin down at the kneeling man in charcoal wool and a pressure-collar. The smile doesn't fade. It turns cold as winter gold.)
[portrait: THEODRIC, deadpan] ...Stand up, whatever you are. You're getting mud on my reflection.
[portrait: THEODRIC, smug] "House Aurel"? In that mourning-coat? You pitched a shopkeeper's tower on my drowned roof and expect applause like a clerk who stole the silverware during a fire.
[portrait: VOSS, shocked] I built the Engine! Eighteen pylons in Crownhaven! Better than metal, my lord. It only needs the cradle.
[portrait: THEODRIC, neutral] (two fingers, waved lazily, without looking at him) Then fetch your little brass toy and set the stage, mongrel. Even a stray hound can carry a bone to the right door.
(Voss doesn't hear the contempt, or won't. His salvage team hoists the keystone cradle and retreats to the submarine lock.)
[portrait: VOSS, happy] It will be ready at the Coronation, Your Majesty. Every lock. Every light.
(The lock seals. Only you, your Reflection and the King behind the glass remain. He rests one gauntleted palm lightly against the inside of the mirror, opposite your chest.)
[portrait: THEODRIC, smug] Look at him. Three hundred years, and my bloodline prays to a ghost in a pane of glass.
[portrait: THEODRIC, neutral] You, however, did not kneel. You did not even lower your eyes.
(A slow, dangerous grin: a sovereign spotting the first challenger in three centuries who might actually make him sit up.)
[portrait: THEODRIC, happy] Bring that little tin crown to Crownhaven, hollow thing. Let the merchant finish building my door.
(His fingers close on the Chain. One word, through the glass, like struck gold:)
[portrait: THEODRIC, smug] "Finish."
```

### 3.3 R6 — Night of Masques: Ruin Variant (Replaces lines 66–75)
*Upgrades: adds a razor-sharp Gilgamesh dismissal of the panicking Wardguard (`"Lower those Poké Balls, mongrels"`) and casual possessiveness over Velmora's Plates while preserving Ansel Crewe's critique, Celestine's beat, and Dorian's iconic closing line verbatim.*

```text
(Gasps. The Wardguard reach for Poké Balls and freeze: every shield, every lantern pane, every Basilica window shows the same golden gaze looking down at them.)
[portrait: THEODRIC, deadpan] Lower those Poké Balls, mongrels. Did I grant you leave to interrupt my play?
[portrait: THEODRIC, neutral] Ansel Crewe, was it? The playwright they hanged for remembering me?
[portrait: THEODRIC, happy] A decent second act. A cowardly third. He has me weeping as Aurelia sinks. How tedious. When the sky broke over my head, I did not weep. I applauded.
(Celestine steps out of the wings, pale, unable to lie even now.)
[portrait: CELESTINE, shocked] ...You're not a memory. The Glass kept you whole.
[portrait: THEODRIC, smug] A truth-speaker? Charming. Maren's songbirds still keep their feathers. Sing your third verse, little bird, if you have the stomach.
(His eyes pass the stage lights, Dorian, the Wardguard, Voss trembling in the Meridian box, and settle squarely on you.)
[portrait: THEODRIC, happy] Ah. There sits my real audience.
[portrait: THEODRIC, smug] Every Plate in this realm was mine before your grandparents learned to draw breath. Beat the tired old caretaker tomorrow, pick up my little silver hoop... and try not to bore me when the curtain rises for real.
(He snaps his fingers inside the glass. Every torch in the square dies. When the lanterns relight, the mirror shows only frightened faces, and one hairline golden crack shaped like a crown.)
```

### 3.4 R7 — The Mirror Breach: Physical Voss Toss (Replaces line 95 ONLY)
*Purges the subtle Enkidu-from-crystal-portal visual (`"Two links of the Chain lash out of the crystal like whips"`), grounding the beat purely in Aurelius's physical arrogance and the Arbiter Engine's perimeter.*

**BEFORE (line 95):**
```text
(Two links of the Chain lash out of the crystal like whips, snap the harness straps and throw the chief executive of Meridian twenty feet across the arena into the Chain's burning perimeter.)
```

**AFTER (line 95):**
```text
(With a lazy flick of his gauntlet, Aurelius catches Voss by the steel collar of his harness—snapping the straps cleanly—and flings the chief executive of Meridian twenty feet across the flagstones into the Arbiter Engine's burning golden perimeter.)
```

### 3.5 R7 — `GO_R_KNEEL` Lead-In: Sovereign Possessiveness (Replaces lines 104–107)
*Adds Aurelius's signature Gilgamesh possessiveness right before his royal offer to kneel.*

```text
[portrait: THEODRIC, smug] Now, then. The clerk is out of the way, and the sky is already listening.
[portrait: THEODRIC, neutral] Every Plate, every crown, every worthy specimen in this land was mine before your grandparents learned to breathe. I am merely collecting interest.
[portrait: THEODRIC, smug] You walked through twenty-three graves to open my door—a finer errand than any servant I left in the salt.
(He holds out one open, gauntleted hand: not Voss's offer of partnership, a monarch granting an audience.)
[portrait: THEODRIC, smug] Kneel, mongrel. Set that little hoop at my feet, and I will be generous. I am always generous to things that know their station.
```

### 3.6 R7 — The Challenge: FULL GATE OF BABYLON PURGE (Replaces lines 132–140)
*🚨 **CRITICAL FIX:** Completely purges line 134's `"Eighteen golden portals ripple open behind his cape like mirrored shields"`. Replaces it with 100% Pokémon Prismfall staging matching `graphics/Trainers/GILDED_THEODRIC.png` & `graphics/EBDX/VS/THEODRIC.png` (Aurelius casually lifting a gilded Poké Ball while the Arbiter Engine's 18 stadium pylons invert `:PRISM_ARENA`).*

**BEFORE (lines 132–140):**
```text
### The challenge
```
(He steps back onto the centre ring. Eighteen golden portals ripple open behind his cape like mirrored shields; the Prism field inverts: strengths to weaknesses, the sky to inverted gold.)
[portrait: THEODRIC, neutral] Let us see what three hundred years of mortal mediocrity has produced.
[portrait: THEODRIC, smug] You mean to unmake the sky? To erase the Plates I spent a kingdom's blood to collar?
[portrait: THEODRIC, happy] Audacious! Unforgivable! Utterly magnificent!
[portrait: THEODRIC, angry] Come, then, mongrel. Stand before the First Sovereign of Aurelia and show me whether you deserve to look heaven in the eye!
BATTLE: Prismfall::Festival.next_match (stage :HIJACK on the Ruin Route) -> [GILDED_THEODRIC,Aurelius] on :PRISM_ARENA, the event layering Inverse. Gold VS screen (THEODRIC). LoseText: "Ha...! Magnificent! Three hundred years, and at last a challenger. Go—end the sky."
```
```

**AFTER (lines 132–140):**
```text
### The challenge
```
(He steps back onto the centre ring and lifts a single gilded Poké Ball in a relaxed, elevated palm, golden chain-links chiming softly across his breastplate. Around the stadium rim, all eighteen crystal pylons of the Arbiter Engine flare Aureate gold in unison; the Prism field flips inside out—strengths twisting into weaknesses, the Crownhaven sky inverting to cold gold.)
[portrait: THEODRIC, smug] Look up, mongrel. Let us see what three hundred years of mortal mediocrity has produced.
[portrait: THEODRIC, neutral] You mean to unmake the sky? To erase the eighteen Plates I spent a kingdom's blood to claim?
[portrait: THEODRIC, happy] Hahaha—audacious! Unforgivable! Utterly magnificent!
[portrait: THEODRIC, angry] Stand your ground, insolent mongrel! Face the First Sovereign of Aurelia and prove you have the spine to look heaven in the eye!
BATTLE: Prismfall::Festival.next_match (stage :HIJACK on the Ruin Route) -> [GILDED_THEODRIC,Aurelius] on :PRISM_ARENA, the event layering Inverse. Gold VS screen (THEODRIC). LoseText: "Ha...! Magnificent! Three hundred years, and at last a challenger. Go—end the sky."
```
```

### 3.7 R7 — Barks Summary Sync (Replaces lines 145–150) & Guardrail (Appends after line 176)
```markdown
**Barks in battle** (Z-Power `006_ZPower_TrainerBarks.rb`; each once per battle, pure Pokémon treasury & Gilgamesh
personality—zero portals): Sunguard's send-out ("Witness the original, mongrel..."), end of round 1 on the inverted
arena ("Look up, mongrel. Even heaven's own laws bow backward in my court..."), Regalia's ("Every petty king since
Aurelia sank has worn tin and called it regalia..."), the first titan ("...I collared the sea and the earth merely to
tend my gardens!"), Colossus ("I grant you five heartbeats, mongrel..."), Gilt's send-out ("Hahaha—well played,
mongrel!..." — final use of the word), and Gilt under a third of its HP ("Hahaha! Yes! That cold, unflinching glare..."
— "mongrel" permanently dropped).
```

Add one closing bullet under `## How he sees the others` (after line 176):
```markdown
- **Staging Guardrail:** **Personality ONLY — never Fate powers.** Aurelius never opens golden weapon portals or summons floating swords/halberds; his dominance comes strictly from his bearing, his words, the Arbiter Engine's physical pylons/Chain, and his six Pokémon.
```

---

## 4. Exact Drop-In Upgrades for `plugins/Prismfall Z-Power/006_ZPower_TrainerBarks.rb`

### 4.1 Side-by-Side Personality & GoB-Purge Comparison

| Hook Key | Current Line (`006_ZPower_TrainerBarks.rb`) | Upgraded Line (Pure Archer Gilgamesh × Pokémon) | Why It's Stronger |
|---|---|---|---|
| `:GOLURK` (*Sunguard*) | `"Witness the original, mongrel. That corroded toy Voss dredged from the silt was my doorstep's dust."` | `["Witness the original, mongrel.", "That corroded toy Voss dredged from the silt was merely dust on my doorstep."]` | Splits into two punchy EBDX beats so `"Witness the original, mongrel."` lands like a gavel drop before roasting Voss's `Gilder`. |
| `:round1` (Inverted Arena) | `"Even heaven's own laws twist backward beneath my heels! Adapt, or shatter!"` | `"Look up, mongrel. Even heaven's own laws bow backward in my court—try not to trip on your own shadow."` | Swaps generic RPG-boss yelling for effortless, lounging Gilgamesh amusement at the Inverted chart! |
| `:AEGISLASH` (*Regalia*) | `["A thousand blades were forged after Aurelia sank. Every one a crude copy of mine.", "Regalia. Show them royal steel."]` | `["Every petty king since Aurelia sank has worn tin and called it regalia. Counterfeits, the lot of them.", "Regalia—remind this mongrel what royal steel looks like."]` | Removes the subtle Fate "thousand blades" vault bleed; grounds 100% in Velmoran kingship & Aegislash's Pokédex lore while keeping Gilgamesh's contempt for fakes! |
| `[:KYOGRE, :GROUDON]` (*Deluge* / *Sunder*) | `["Before I forged a chain for heaven, I leashed the sea and the earth to plow my gardens!", "Let us see if you survive the Year of Two Weathers."]` | `["Before I chained the sky, I collared the sea and the earth merely to tend my gardens!", "Entertain me, mongrel—let us see if you survive the Year of Two Weathers."]` | Adds classic Gilgamesh casual arrogance (`"merely to tend my gardens!"` + `"Entertain me, mongrel"`). |
| `:REGIGIGAS` (*Colossus*) | `"Even a sleeping titan stands when its king commands. Survive five heartbeats, and earn being crushed."` | `["Even a sleeping titan rises when I snap my fingers.", "I grant you five heartbeats, mongrel—amuse me before Colossus wakes."]` | Restores `"mongrel"` (dropped in prior edit) and turns `Slow Start` into an unforgettable aristocratic handicap! |
| `:GHOLDENGO` (*Gilt* — Lv 100 Ace) | `["Hmph...! You tore through my court and my titans alike? Splendid!", "Then drown in the whole treasury of Aurelia. Gilt, make it rain!"]` | `["Hahaha—well played, mongrel! You tore through my court and my titans without lowering your chin!", "Then you have earned the full weight of Aurelia's vault. Gilt—Make It Rain!"]` | Replaces grumpy `"Hmph...!"` with iconic booming Gilgamesh laughter (`"Hahaha—well played, mongrel!"` — his final `"mongrel"`!) + capitalizes Gholdengo's actual canon Pokémon move (`Make It Rain`). |
| `:ace_low` (*Gilt* < 1/3 HP) | `["Hahaha! Yes! That cold, unflinching glare: neither kneeling nor begging!", "Strike harder, challenger! Show me the fang that dares bite a god!"]` | `["Hahaha! Yes! That cold, unflinching glare—neither kneeling nor begging!", "Strike harder, challenger! Show me the willpower that dares look a god in the eye!"]` | Keeps the 10/10 earned-respect euphoria (`"mongrel"` permanently dropped!), aligning cleanly with R7's pre-battle challenge (`"look heaven in the eye"`). |

### 4.2 Ready-to-Apply Drop-In Ruby Block (Replaces `006_ZPower_TrainerBarks.rb` lines 15–31)

*Uses the exact existing keys and `PrismfallSpeech` hooks — zero engine risk, zero new dependencies.*

```ruby
    # Ruin Route R7, the Hijack: Gilded King Aurelius (story/42_SCRIPT_RUIN_KING.md; 2026-11-24 personality-only audit).
    # Pure Archer Gilgamesh personality (no Gate of Babylon portals/weapons): "mongrel" pivots to delighted respect on
    # Gilt's send-out, then disappears permanently once Gilt is cornered (:ace_low), in LoseText, and post-battle.
    [:GILDED_THEODRIC, "Aurelius"] => {
      :sendout => {
        :GOLURK    => ["Witness the original, mongrel.",
                       "That corroded toy Voss dredged from the silt was merely dust on my doorstep."],
        :AEGISLASH => ["Every petty king since Aurelia sank has worn tin and called it regalia. Counterfeits, the lot of them.",
                       "Regalia—remind this mongrel what royal steel looks like."],
        [:KYOGRE, :GROUDON] => ["Before I chained the sky, I collared the sea and the earth merely to tend my gardens!",
                                "Entertain me, mongrel—let us see if you survive the Year of Two Weathers."],
        :REGIGIGAS => ["Even a sleeping titan rises when I snap my fingers.",
                       "I grant you five heartbeats, mongrel—amuse me before Colossus wakes."],
        :GHOLDENGO => ["Hahaha—well played, mongrel! You tore through my court and my titans without lowering your chin!",
                       "Then you have earned the full weight of Aurelia's vault. Gilt—Make It Rain!"]
      },
      :round1  => "Look up, mongrel. Even heaven's own laws bow backward in my court—try not to trip on your own shadow.",
      :ace_low => ["Hahaha! Yes! That cold, unflinching glare—neither kneeling nor begging!",
                   "Strike harder, challenger! Show me the willpower that dares look a god in the eye!"]
    }
```

### 4.3 `pbs/trainers.txt` Verification (`LoseText` & Team)
- **No edit required to `pbs/trainers.txt` or `tools/trainer_gen/gen.py`!**
- Current `LoseText` (`82 chars`, safely under the `85-char` PBS limit):
  > `Ha...! Magnificent! Three hundred years, and at last a challenger. Go—end the sky.`
- Already 100% clean of Gate of Babylon bleed, drops `"mongrel"` cleanly, and transitions directly into Aurelius's booming post-battle laugh and Arceus's descent.
- *(Optional louder-laugh alt if Reuben prefers — exact `83 chars`: `Hahaha! Magnificent! Three hundred years, and at last a challenger. Go—end the sky.`)*

---

## 5. Scrapped Wave 7 Cutscene Confirmation & Wednesday Cleanup Checklist

Per Creator Reuben's directive (`2026-11-24`), **Wave 7 (`pf_ruin_r7_aurelius_mirror_pierce(_safe).ogv`) is SCRAPPED** because it gave Aurelius literal Gate of Babylon golden portals and floating weapons/halberds.

### 5.1 Cleanup & Wiring Checklist for Claude (Wednesday)
1. **`.ogv` deletion ALREADY COMPLETED (`91207fb`):** All 14 scrapped AI-slideshow `.ogv` files (Waves 1–7, including `Movies/pf_ruin_r7_aurelius_mirror_pierce(_safe).ogv` and `art/out/Movies/` mirrors) have been deleted from the repo. All cutscenes are pivoting to **Rejuvenation V14–style in-engine `AdvancedAnimations`** (`gemini_recommends/2026-11-24_rejuv-advanced-animations-engine/PROPOSAL.md`).
2. **Do NOT wire any scrapped `.ogv` movies** into `plugins/Prismfall Cutscenes/016_Movies.rb` or `tools/package.sh`.
3. **Supersede `gemini_recommends/2026-11-24_art-drop15-npcs-and-ch17-21-wiring/PROPOSAL.md` §7.2:** All 7 AI-slideshow `.ogv` waves are retired/scrapped.
4. **Apply §3 patches** to `story/42_SCRIPT_RUIN_KING.md` (especially purging line 134's `"Eighteen golden portals ripple open behind his cape"`!).
5. **Apply §4 drop-in block** to `plugins/Prismfall Z-Power/006_ZPower_TrainerBarks.rb` (lines 15–31).
6. **Optional 1-line sync:** Update `story/12_RUIN_ROUTE.md:79` roster summary (`Golurk, Aegislash, Kyogre, Groudon, Regigigas, Gholdengo`) and `mapgen/REQUESTS.md:1118` (`Theodric` → `Aurelius`).

### 5.2 How R7 Hijack Should Stage Without Wave 7 (100% Pokémon Prismfall)
Instead of a Fate-portal movie, R7 plays using Prismfall's **already-built native presentation** — cleaner, tighter, and 100% loyal to the game's world:
1. **On-Map Mirror Breach (`Map 491`):** Reverse-glass chime SFX + gold screen flash → Aurelius (`THEODRIC` overworld sprite via `025_CharsetAliases.rb`) steps smoothly out of the central crystal pylon.
2. **Voss Confrontation, `GO_R_KNEEL`, and `:ruin_voss`:** Crisp portrait dialogue (`[portrait: THEODRIC, smug/deadpan/angry/happy]` via `014_Portraits.rb`).
3. **Challenge & Battle Entry:** All 18 stadium pylons flare gold (`:PRISM_ARENA` + Inverse) → hard-cut straight into his **B2W2 `:gold` VS Cut-In** (`Graphics/EBDX/VS/THEODRIC.png` via `010_Bridge_VersusIntro.rb`, showing him calmly holding a gilded Poké Ball!) → animated battle strip (`Graphics/Trainers/GILDED_THEODRIC.png`) + §4 pure-Gilgamesh mid-battle barks (`006_ZPower_TrainerBarks.rb`).
