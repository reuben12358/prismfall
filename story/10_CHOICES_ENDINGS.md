# Story Bible 10: Choices, the Festival Draw, Game Overs, the Ruin Route and the Endings

> Owner: Narrative Systems. Binding: `design/SPINE.md` Revision 3. Implementation contract (every key, value, condition and ID):
> **`design/NARRATIVE_KEYS.md`** — if this file and that one disagree, NARRATIVE_KEYS wins and this file is the bug.
> Built on the story lead's act files 04–08 and the FLAGS.md crosswalk; their key names are kept (lowercased).
> Kingdom names are Revision 3: Elowen, Antumbra, Isenmar, Ashkaar, Ossaria, Zenith, Nadir, and Crownhaven.

## 0. Design pillars

1. **No good/evil buttons.** Every prompt trades something real: a life now against proof later (Teo or Sable's comm-device), the truth
   against the person who'd tell it (expose Magnus, or trust him), honesty against a friend's dignity (expose Anja, or let her confess).
2. **Delayed and visible.** Most choices pay off two or three chapters later, and the game *shows* the debt coming due (§1.4), never the numbers.
3. **The world keeps score, not a meter.** The big outcomes are counts of people: how many Wardens let go of their Plate (Consent),
   how many cracks the PC and their friends put in Voss's machine (Engine breaks). Both are shown on screen before the finale.
4. **Easy in, dark later.** Act I's choices are small and kind-hearted (who to trust, what to say). Act II asks who to save. Acts III–V ask
   who you'll let die, and who you'll become.

---

## 1. Choice architecture

### 1.1 Bonds (10)

Range −10..+10. Tiers: hostile ≤ −5 · wary −4..−2 · neutral −1..1 · friendly 2..4 · close 5..7 · devoted 8+.

| Bond | Start | Why it's tracked | What it changes |
|---|---|---|---|
| **Juno** | +2 | the friend you start with | Consent (≥ 0); estranged Juno (≤ −5) travels apart in Ch11; Garden Match exhibition; Homecoming slide with the PC |
| **Kestrel** | −1 | the rival who can fall | Fallen at ≤ −4 (or ≤ 1 with the pity line, or ≤ 1 while you're Meridian's ally), unless you gave him the ring or answered K6 bluntly; devoted (8+) lets him take the Borrowed Crown; Ghost seat with Ysolde |
| **Rowan** | 0 | the Mourner | radicalized (≤ −2 after being condemned) opens the Hollow Spring; his R16 appearance needs mercy, not affection |
| **Voss** | +1 | the first person who was kind to you | how warmly he offers, how bitterly he takes refusal; Ruin R4 |
| **Valen** | 0 | the father-figure who planned your life | his collapse (≤ −2 with a refusal at the audience); his last words; Zygarde chooses the PC post-game at ≥ 3 |
| **Ilsa** | 0 | the daughter who reads minds | Little Owl (≥ 3 to start, ≥ 4 to reconcile); Consent (≥ 5 or reconciled) |
| **Sigrun** | 0 | the heir who was relieved | war trust (≥ 4); she draws into your QF if you've gone Ruin-leaning or broke Ashkaar; Borrowed Crown bearer (≥ 6) |
| **Nyx** | 0 | the broker | Consent (≥ 4 or the bargain) |
| **Marisol** | 0 | the sister of the boy you may not save | if Teo died: Consent at ≥ 3, otherwise she claims her Right of Grievance in R16 |
| **Ysolde** | 0 | Morwen's partner | Kestrel–Ysolde reconciliation (≥ 4), Kestrel's Ghost seat, Morwen's Echo exhibition |

Other Wardens are **not** Bond tracks. When an act file says "Tamsin's Bond goes up", the choice key itself carries it, and it surfaces in
that Warden's Consent condition (§6.2). That keeps ten relationships deep instead of thirty shallow.

### 1.2 Standing (Hollow / Meridian / Accord)

Range −10..+10 (Meridian and Accord start at +1, the Hollow at 0). "High" = ≥ 4 (the Ch10 Sanctuary / Black Site branches, the Ch17 Archive
branch); "Low" = ≤ −2; "broken" Hollow = below 0. Standing gates **content** (branch maps, who ambushes you, Voss's warmth, Lantern Hollow at the
hijack) far more than endings; the endings read Standing only through the Hollow Spring and Concord options.

### 1.3 Resonance (Harmony ↔ Ruin)

One integer from −10 (Ruin, *none*) to +10 (Harmony, *every*). It moves only when the PC *uses* the shard or chooses how to carry grief:
soothing or silencing the Glass Matriarch (Ch2), venting or forcing the caldera (Ch8), the Ogre (Ch10), "nobody" (Ch10), burning Morwen's
letter (Ch12), the Mindscape line (Ch13), the K6 line (Ch15), the oath (Ch19), Calla (Ch20), burning Kestrel's gauntlet off (Ch21).
Bands: ruin ≤ −6 · ruin-leaning −5..−2 · balanced · harmony-leaning 2..5 · harmony ≥ 6.

### 1.4 How the player sees consequences (no numbers)

- **"X will remember that."** Only when a Bond changes tier, or on a MAJOR choice. Rare on purpose, so it lands.
- **The Ties page** (Trainer Card, page 3): ten portraits with a lantern that is cracked / guttering / lit / bright / blazing / starred,
  plus three faction sigils with one word each (Enemy … Ally). The `openbook` password adds numbers.
- **The scar.** The PC's star-shaped scar in the Bag portrait shifts from pearl-white through colorless to a black-violet that *eats* the
  edges of the icon. Bleed motes drift toward the PC at Harmony and away at Ruin. Wardens comment ("You've gone cold, love.").
- **The Velmora Gazette** in every Pokémon Center: two headlines per chapter picked by rule (e.g. "IRONREACH BOMBER STILL AT LARGE" vs
  "MERIDIAN CONTRACTOR LINKED TO IRONREACH" after Ch13).
- **Tamsin's eighteen banners** (Ch20, the opening ceremony): she weaves one per Warden, in white thread if that Warden will let go and grey if
  not. "Twelve white. I don't know what it means, but it feels like it means something." That is the Consent count, shown.
- **Larch's Engine board** (Ch20, Day 5): a hand-built panel of eleven lamps wired to her readings of the arena. Each lit lamp is a crack in
  the Engine (§6.2). "If that case is still singing to him and Magnus never flinched, three lamps won't be enough. I can't make that sound kinder."
- **The Journal** records every named decision in one line of prose ("You told the Glass Court what you saw in the Lowlight.").

---

## 2. Choice catalog (48 keys)

Format: **key** — situation. Options → immediate effect. *Long-term.* Exact deltas: NARRATIVE_KEYS §4.2. ★ = MAJOR (10).

### Prologue and Act I — "The Last Ferry" (warm; nothing here can ruin you, but everything is remembered)
- **`:pro_fellowship`** — Voss offers a Fellowship card on the *Dovetail*. *accept* (money, Meridian trust) / *decline* (Voss likes you more:
  "Independent. Good.") / *silent* (he leaves it on the rail). *Sets how warmly Meridian treats you in Acts I–II.*
- **`:ch2_matriarch`** *(new)* — The beaten Glass Matriarch thrashes in the silk-moth grove. *soothe* (stay with it all night; half the grove
  crystallizes; Harmony) / *silence* (press your hand to it and the Imprint leaves it like water down a drain; the grove is saved, the
  Matriarch is left hollow; Ruin −2). *The player's first lesson: the efficient choice is the Ruin one.*
- **`:ch2_tamsin`** — Tamsin's secret Lattice contract. *expose* / *help_confess* / *keep_secret*. *Keeping it means the pylon keeps
  draining Briarwick, and in Act V she can't afford to let go of her Plate (Consent).*
- **`:ch3_juno_talk`** — tell Juno about the NULL scan? *told* (she keeps it) / *deflect* / *silent*.
- **`:ch4_kestrel_mourner`** — is the Mourner his mother? *kind* / *blunt* (−2) / *silent*.
- **`:ch4_teo`** — Marisol is tipping off her brother's cell. *report* (Meridian trust; Marisol −4; Teo is hunted) / *keep_secret* / *confront*
  (she breaks down; the strongest Marisol bond). *Seeds who Marisol is if Teo dies.*
- **`:ch5_lowlight_testimony`** — a Directorate officer asks what you saw. *"The Mourner broke the Plate"* (it's what it looked like) /
  *"Someone else was there"* / *"I don't know."* *Telling the official story on record costs Dorian's Consent: "I keep the lie I know until
  someone shows me a better one."*

### Act II — "Imprints" (who do you save?)
- **`:ch6_drillsite`** — the freed Pokémon and the drill-site children. *hollow* / *directorate* (a Mandate Pass that opens checkpoints later) /
  *sanctuary* (Sahar invokes Warden's right). *Directorate costs Sahar's Consent.*
- **`:ch6_kestrel_rumor`** — K3. *encourage* (+2 now, −3 at Ironreach when it isn't her) / *warn* (−1 now, +2 at Ironreach: "I hate that you were
  right") / *silent*. *The kind answer now is the cruel one later.*
- **`:ch7_ledger`** — J2. *name_him* (Juno −3, then +2 at Ironreach: she already knew) / *reassure* (+2, then −2) / *ask_corvin*.
- **`:ch8_caldera`** — the Caldera Crisis. *vent* with Wick (forges cold; Harmony) / *dampers* with Quent (the tap keeps running; Ruin −1) /
  *shutdown* by force (a harder fight; Accord trust; the Dominar's respect).
- **`:ch8_lightstone`** — *hearthguild* / *wyrmrest* (Sigrun +2; the only route to swaying the Dominar) / *dominar* (Brann won't let go of his
  Plate for a man who'd give away his guild's relic).
- ★ **`:ch9_teo_sable`** — the Conclave Shatter. Teo is Fixing under the scaffolding; Sable is running for the service lift with the
  comm-device. **Save Teo** (he lives with glassed fingers; Marisol +4; Sable escapes clean) / **chase Sable** (you tear the device from her belt;
  Teo dies reaching for his sister). *Long-term: Teo leads the Lantern Hollow strikers, or his photo is nailed to the strike banner; only the
  device exposes Kroll publicly at the Ch13 tribunal; Marisol's Consent or her Right of Grievance in R16.*
- **`:ch9_rowan_words`** — Rowan, led away. *why* / *look_after* (+2) / *silent* (+1).

### Act III — "Fault Lines" (who do you let fall?)
- **`:ch10_null`** — Black Site branch only: take the Type: Null. Voss +2. *An unsettling gift: it reacts to you like the badge case.*
- **`:ch10_ogre`** — the Loyal Three or the Ogre (*three* is `GO_LOYAL`). *ogre* (Ogerpon fights with you, later joins Juno) / *hesitate*.
- **`:ch10_succession_stance`** — "Who should own the Plates?" *accord* (Valen +2) / *kingdoms* / *nobody* (the first "nobody"; Harmony).
- **`:ch11_anja`** — her suppressed readings. *expose* (`ANJA_EXPOSED`; Meridian blamed loudly) / *let_confess* (she becomes the Act V swing
  vote). *Exposing her costs her Consent and makes her claim R16: "You threw me to the court. Fine. Ice remembers."*
- **`:ch11_strike`** *(new)* — the Ebbmouth Strike picket when the strikebreakers arrive. *stand* (the optional tag battle with Marisol;
  +2, +3 if Teo died) / *mediate*. *The only Act III way back to Marisol after Teo's death.*
- **`:ch12_letter`** — Morwen's dead letter to "I.". *keep* (you can quote her in the hijack) / *send* (Kestrel +3: "You sent me a *letter*.
  Hers.") / *burn* (Ruin −2; Odessa finds out: "Dead letters are the last thing some people ever said." She won't let go of her Plate.)
- **`:ch13_remember`** — the five-year-old in the Mindscape. *"Show me."* / *"I'm scared too."* (Ilsa +2, Harmony +2) / *"...Not yet."*
- ★ **`:ch13_kaito`** — Kaito asks whether to speak about Marrowgate. **Encourage** (the Accord's moral authority cracks; Valen −2; Ilsa +2;
  Kaito's Consent) / **spare** him the burden (Accord trust; Kaito never lets go). *A man who never confessed can't release anything.*
- ★ **`:ch13_rowan_testimony`** — your testimony at the Glass Court. **Condemn** (Pale Gaol; Juno −3; Rowan −4: if he survives, he radicalizes,
  which opens the Hollow Spring) / **Mercy** (Rowan +3, Juno +3, Hollow +2; with Hollow trust ≥ 4 he comes to the Festival as "the Gardener"
  with Juno's blessing) / **Refuse** (Ilsa, privately: "Coward. Kind of a coward. I understand.").
- ★ **`:ch13_fault`** *(new, who lives)* — the Fault. The Glass Court's undercroft floods with Rowan chained in the dock, and the orrery's
  brass ring comes down on Director Marchetti. Wick's people are on the far side of the water. You can reach one. **Rowan** (he escapes with
  Wick, as written; Marchetti is dragged out by her troops, maimed and unturned) / **Marchetti** (Rowan drowns in the dark under the court, still
  chained; Marchetti owes you her life and stands the Directorate down at the hijack). *Long-term: who leads the Lantern Hollow (Rowan, else Teo,
  else Thistle and Wick); whether Elin wakes into her husband's arms; Juno −4.*
- **`:sq_doctors_cell`** — "The Doctor's Cell" (Ch11–13): free Corvin from the holding barge, or fail. *Corvin's Consent; the Cragholm hospital.*

### The Ashkaar–Isenmar War (Revision 6; chapters placed by the story lead, Act III–IV) — six proposed choices
- **`:war_warning`** — you see the Dominar's legions at Frostfang Pass before anyone. Warn Isenmar / warn Ashkaar they've been seen / warn both
  (the Accord's way; both sides note it) / say nothing.
- **`:war_convoy`** — Marisol asks the one person who can walk the Bleed-front to take a convoy through the Steamline into besieged Skaldfast: *relief* (food) /
  *arms* (harpoon-guns; Marisol +3, Sigrun −2) / *refuse*.
- **`:war_prisoner`** — Ashkaar holds Anja; the Thane holds the Dominar's nephew. *free* one in secret / broker an *exchange* / *leave* them.
- **`:war_legend`** — both sides beg you to bring their legend: *calm Kyogre* / *wake Reshiram* / *neither*. It decides whose beams meet in the climax.
- ★ **`:war_climax`** — the Shattered Ice, both lines charging. **Stand between** them / **back Ashkaar** / **back Isenmar**. Standing between only
  stops the war if both armies have seen you act in good faith four times (war trust: warned both, relief, a prisoner helped, no legend used as a
  weapon, Sigrun ≥ 4, Marisol ≥ 3). Otherwise the beam clash goes off over your head and breaks both armies.
- **`:war_terms`** — if one side won: argue for *mercy*, *reparations* or *occupation* at the armistice table in Skaldfast.
- **`:ch20_colors`** (the story lead's key) — whose colors the challenger wears on Day 0: Elowen's, Zenith's, Nadir's, or none ("the Unsworn", a whisper
  of Harmony). Crowd reactions, one R16 line, one small delta.
- **`:ch21_boon`** (the story lead's key) — the Blessed's one binding decree: end the war's reparations / seat Nadir on every council / dissolve the
  Seat. It is asked before the ending is fixed, so ending reparations can undo an *occupation* you argued for and reopen Homecoming.

*Long-term:* a beaten kingdom forfeits a Festival seat (§3.1); beaten and unforgiven, its Wardens won't release their Plates (Marisol and Anja,
or Brann and Sigrun; both pairs if the clash broke both armies), which can sink Consent below 12 on its own; *occupation* makes Homecoming
impossible (Unfinished at best); the winner's fleets or legions (both, if you stopped it) defend Crownhaven in the hijack; Anja vs Brann in the
bracket is decided by it.

### Act IV — "The Drowned Crown" (who are you willing to become?)
- ★ **`:ch14_telemetry`** — Larch opens the badge case. **Destroy** (Voss knows at once; Directorate pressure in Ch16–17; an Engine crack) /
  **Sabotage** (keep it and feed it lies: two cracks, a tense "did he notice?" beat at every later badge) / **Leave** it (the road to the Bad
  ending, and Bastian's Consent is gone: "You walked a Meridian beacon into my seams.").
- **`:ch14_marchetti`** — after her defeat, show her the Splitter Casing or the comm-device? *show_evidence* (she goes still; turns at the
  hijack) / *none*.
- **`:ch15_kestrel`** — the PC's authored line after K6. *sorry* ("I'd give it back if I could": +1 now, +3 at the SF if he's Redeemed, but
  pity is the one thing a weak bond can't carry) / *she_chose* ("Don't you dare make her choice my crime": −2, and he can never fall) /
  *resolve* ("I'm going to make it worth it": +2, Harmony +2).
- **`:ch15_look_back`** — only with a complete Ledger: the Ruin Route door (§5).
- **`:ch16_zekrom`** — outcome of freeing Zekrom (always, if you win). One Engine crack.
- **`:ch16_rook`** — *leak_now* (Kroll is confirmed realm-wide today; Rook is fired and blacklisted from the Spire) / *hold* (he leaks on Day 1
  of the Festival, and he's still inside on Day 7 to cut Lumen's grid). *Truth now, or a weapon later. Rook can only release a Plate he can reach.*
- ★ **`:ch16_magnus`** — the Arbiter blueprints. **Expose** (Magnus arrested; with Rook's leak and the Night of Masques, Meridian's board throws
  Voss out before Day 7 and **Quent** hijacks the Engine instead) / **Conscience** ("Will you let it take a child?": the governor goes off in the
  finale, an Engine crack, Magnus's Consent). *The honest public act removes the man who could have saved you from inside.*
- **`:ch17_nyx`** — *trade* your secret for the arena schematics (her blackout is precise, an Engine crack, her Consent) / *refuse*
  (she helps anyway, sloppily, and gets hurt).
- ★ **`:ch17_voss_offer`** — the Sun Court. **Refuse** / **Feign** (the hijack opens with Voss's Silvally weakened: "You let me get close.") /
  **Accept** (`VOSS_ACCEPTED`: at the hijack his hand ends the game in Concord Dawn if you take it).

### Act V — "Sovereign" (who carries it?)
- ★ **`:ch18_kestrel_ring`** — after K7, Morwen's Ring. **Give now** (+3: he can never fall) / **Keep** (a bigger moment at the SF if he's
  Redeemed, and the one thing that can reach him in the Engine if he isn't). *The safest choice and the most dramatic choice are different.*
  Then the prompt that is `GO_STAY_OUT`.
- ★ **`:ch19_oath`** — at the Draco brazier, aloud. **Return** / **Keep** (Valen +3; Kaito draws into your QF: "You'd keep them? Marrowgate's still knocking."; Sigrun won't let go of the Draco Plate) / **Open** ("I don't know yet") / **Ruin** (only at Ruin-leaning or lower; Sigrun draws her
  blade and lets you pass). The hidden "Whatever you want to hear." is `GO_LIARS_PYRE`.
- **`:ch19_dominar`** — the petition. *swayed* (needs the Light Stone at Wyrmrest plus proof, or Sigrun ≥ 4) / *failed* (the legions march on Zenith).
- **`:ch20_envoy`** — Envoy Okoro. *proof* (needs two of: Larch Papers, Arbiter Blueprints, testimony that the Fixed still dream, from Teo if he lived ("I could hear everything while my hand was glass") or Corvin's ward records if he's free; no Severance) / *plea*.
- **`:ch20_calla`** *(new, who lives)* — at the Night of Masques Calla Wren finds you, shaking: she can get the arena's power schematics to Larch.
  Only offered if someone inside is already moving (Rook held, or Magnus kept faith). *shelter* her with Edda (partial schematics, one crack) /
  *send_back* for the full set (two cracks, and Kroll finds her in the Spire stairwell; she doesn't come back) / *turn_away*.
- ★ **`:ch20_audience`** — the PC answers Valen's confession. **Return** / **Keep** (he weeps, once) / **Refuse** ("Nobody decides for me."). *If the
  PC refuses with a cold Bond, Ilsa never came, and the telemetry still runs, Voss's pre-ignition drains him: Valen collapses before the Final,
  and his successor fights you.*
- **`:sq_little_owl`** — Ilsa's quest culmination: *reconciled* / *refused*.
- **`:ch21_crown`** — kneel / stand / step back (flavor; stepping back is a whisper of Harmony).
- **`:ch21_hand`** — only with `VOSS_ACCEPTED`: take his hand (Concord Dawn now) / refuse ("You promised.").
- **`:ch21_reach_kestrel`** *(new)* — only if Kestrel fell: he's harnessed into the Engine as Voss's conduit, between Voss's second and third bars.
  *reach* (needs the ring or Morwen's words; he comes back) / *burn* (the shard tears the gauntlet off; he lives, scarred; Ruin −3) /
  *let_go* (he burns out as the Engine fires).
- **`:ch21_spare_voss`** — Judgment strikes the hijacker. *shield* (he lives, crippled, and asks to see the sunrise) / *let_judge*.
- **`:ch21_final`** — the final decision (§6.1).

---

## 3. The Festival draw (Revisions 5–6: kingdom delegations, story-met characters only)

### 3.1 What the Festival is now
The Festival of Champions is the rite by which all Velmora chooses the one person who receives **Arceus's Blessing**. Sixteen stand in the Prism
Arena: the Unimprinted challenger and **fifteen delegates**, two from each of the seven kingdoms and the Accord's Sovereign. Nobody in the bracket
is a stranger: every possible opponent has been met at least twice by Act IV. The four Rev-4 outsiders are gone.

**Who each kingdom sends** (exact rules: NARRATIVE_KEYS §6.1):

| Kingdom | Seat A | Seat B | What decides it |
|---|---|---|---|
| **Elowen** | Juno | Celestine | fixed, but Juno gives her seat to "the Gardener" (Rowan) if you earned it (R16 draw) |
| **Antumbra** | Ysolde | **Kestrel** if Gravenmoor names him (redeemed, and the ring given or Ysolde ≥ 4), else **Ilsa** | whether the name *Vane* is restored or he's disowned |
| **Zenith** | **Rook** if he held the footage and is still Meridian's face, else **Odessa** | **Kestrel** under Meridian's sunburst if Gravenmoor didn't claim him; else **Magnus** unless exposed; else Odessa/Rook | Rook's and Magnus's Ch16 choices; Kestrel's state |
| **Nadir** | Kaito | **Nyx**, or **Corvin** if you freed him and refused Nyx's bargain | who the City Below trusts |
| **Ossaria** | Sahar | **Bastian**, unless the raid came in on your beacon (telemetry left); then the seat is lent out | Ch14 |
| **Isenmar** | Marisol (or Anja, if only one seat is left and she's the one with the open account with you) | Anja, or **forfeit** | the war |
| **Ashkaar** | Sigrun | Brann, or **forfeit** | the war |
| **The Accord** | Valen | — | — |

**The war decides seats.** A kingdom that lost the war (or both, if the clash broke both armies) forfeits its second seat; the Accord lends it to a
Warden with no seat (Dorian first, then Tamsin, Rook, Odessa, Ilsa, Nyx, Corvin). A victor gets terms, never a third delegate.

### 3.2 Stage pools (first matching candidate wins; the last line is the fallback)

| Stage (cap) | Priority | Opponent | Condition | On-screen reason |
|---|---|---|---|---|
| **R16** (90) | 1 | **Marisol** (Grievance) | she holds a seat, Teo died, Bond ≤ 2 | Right of Grievance: "Let's see you run past *me*." |
| | 2 | **Anja** | she holds a seat and you exposed her | "You threw me to the court. Fine. Ice remembers." |
| | 3 | **Rowan, "the Gardener"** | Rowan lived, you pleaded mercy, Hollow trust ≥ 4 | Juno gives him Elowen's seat: "One last garden, child." |
| | fallback | **Juno** (J4) | — | "We started on the same dock." |
| **QF** (92) | 0 | **Archseer Dask** | Ruin Route | "Behind, welcome. Welcome, behind." |
| | 1 | **Sigrun** | Resonance ≤ −3, or you helped Isenmar break her father's legions | "Dragons weigh things. You've gotten heavier." |
| | 2 | **Kaito** | your oath was Keep | "You'd keep them? Marrowgate's still knocking." |
| | 3 | **Ysolde** | Kestrel has fallen | "If I can't reach him, I'll find out what reached you." |
| | 4 | **Odessa** | she holds a seat; five close Bonds; Harmony-leaning | "Everyone keeps telling you what you're *for*. The wind doesn't care. What do *you* want?" |
| | fallback | **Celestine** | — | "I cannot lie, so listen while we fight." |
| **SF** (94) | 1 | **Kestrel (Fallen)** | `KESTREL_FALLEN` | Meridian's banner; he keeps the Gauntlet on |
| | fallback | **Kestrel (Redeemed)**, K8 | — | Gravenmoor's banner or Meridian's; he tears the Gauntlet off |
| **Final** (96), live on Day 7 | 0 | **Valen, the Last Tuning** | Ruin Route | — |
| | 1 | **Brann** | Valen collapsed | "He asked me to. Last thing he asked." |
| | fallback | **Valen** | — | Zygarde |
| **Hijack** (100), live | 0 / 1 / fallback | **Theodric** (Ruin) / **Quent** (Voss discredited) / **Voss** | — | — |
| **True Finale** (100) | — | **Arceus** variant | Judgment > Gilded > War > Miscalibrated > Bound | §6.2 |

**Functions moved off the retired outsiders:** the Return confirmation is **Celestine's**, and it's an oath because she cannot lie ("Give them back.
I've waited forty years to say that to someone who could."). The warning before *His Hand* is **Larch's** ("Don't let him make you a part. He's very
good at parts."). The Concord Dawn closing line is Celestine's, in fairy-tale cadence: "Once upon a time a god was kept in a box. It was quiet. For a
while." "That isn't him fighting" is **Kaito's**, because his Lucario felt it. The Ruin hint is **Ilsa's**: "You're thinking very loudly.
Twenty-three times."

### 3.3 Proof: exactly one opponent per stage, never the same person twice
1. **At least one / at most one.** Every list ends in an unconditional fallback who is *always seated* (Juno, Celestine, Kestrel, Valen; Voss), and the
   resolver stops at the first match.
2. **No duplicates.** Persons per stage are disjoint: R16 {Marisol, Anja, Rowan, Juno}; QF {Dask, Sigrun, Kaito, Ysolde, Odessa, Celestine}; SF
   {Kestrel}; Final {Valen, Brann}; Hijack {Theodric, Quent, Voss}. Core's validator enforces it.
3. **Only seated people are drawn.** Candidates whose seat depends on choices (Marisol, Anja, Odessa) carry `seated()` in their condition; Kaito,
   Ysolde and Sigrun are always seated; Rowan and Dask enter by replacing the default; Brann's stand-in is live and needs no seat.
4. **Fifteen seats always fill.** Each seat ends in an unconditional candidate or a forfeit drawn from a pool of seven for at most three forfeits.
5. **Alive and present.** Rowan needs `ROWAN_ALIVE`; Quent precedes Voss when Voss was removed; Brann only when Valen collapsed.

### 3.4 Companion matches and highlights
NPC matches resolve by rule, and the player can watch any notable one as a pixel-animated highlight (`MATCH_RULES`, NARRATIVE_KEYS §6.5: winner
rule plus 2–4 key moments each). Order: a drawn path opponent wins until they meet the player; then the pair's rule; then rating. Examples:
- **Anja vs Brann**, the war in miniature: Anja wins if Isenmar won or the war was stopped with the prisoners freed, else Brann. Its centre is a
  Blizzard–Flamethrower beam clash where, this time, nobody dies.
- **Kestrel vs Kaito** (Kestrel wins): Lucario flinches from something that isn't the blade.
- **Juno**, when a Grievance displaces her: she beats Ysolde at Bond ≥ 5 ("Your aunt is listening"), and loses to Sigrun with her garden at stage five.
- **Valen vs Sigrun** (Valen): "He beat me with an arm made of glass." **Valen vs Kaito**: Kaito's first Aura Sphere goes a hand's width wide, on purpose.

### 3.5 Sample runs

| Run | R16 | QF | SF | Final | Hijack | Arceus |
|---|---|---|---|---|---|---|
| "The kind one" (Teo saved, mercy, war stopped, five close Bonds) | **Rowan** | **Odessa** | Kestrel, for Gravenmoor | Valen | Voss | Miscalibrated |
| "The honest one" (chased Sable, exposed Anja and Magnus) | **Marisol** | Celestine | Kestrel | Valen | **Quent** | Bound |
| "Isenmar's sword" (backed Isenmar, occupation) | Juno | **Sigrun** | Kestrel | Valen | Voss | Bound → *Unfinished* at best |
| "Meridian's friend" (telemetry left, oath Keep, cold audience) | Juno | **Kaito** | **Kestrel (Fallen)**, for Meridian | **Brann** | Voss | **Gilded** |
| "The Renegade" | Juno | **Dask** | Kestrel | **Valen, Last Tuning** | **Theodric** | **Judgment** |

### 3.6 Displaced defaults, exhibitions, teams
- **Displaced:** Marisol/Anja swap seats with Juno, and the QF Wardens swap with Celestine; the displaced one plays on as an NPC. Rowan takes Juno's
  seat (she gave it), and on the Ruin Route Dask takes Celestine's ("I cannot lie, so I won't pretend this is a game.").
- **Exhibitions** (story-met only): the **Pageant Bout** (Dorian and Rook, a double), **Juno's Garden Match** if she wasn't your R16, the **Ebb Guild
  match** with Marisol (Teo saved, close), **Morwen's Echo** on the Night of Masques, and the **Eevee Octave** (Vesper is met in Ch3 and Ch13). On the
  Ruin Route only the Octave plays.
- **Teams:** NARRATIVE_KEYS §7. **19 new Festival teams** (Marisol 90, Anja 90, Rowan 90, Celestine 92, Sigrun 92, Kaito 92, Ysolde 92, Odessa 92,
  Dask 92, Kestrel Fallen 90–92, Brann 96, Valen 1, Quent 99, Theodric 0, Dorian 90, Rook 90, Morwen 90) plus 4 Arceus configs. Revision 6 adds none:
  the other delegates are NPC-only. Retired: Isaura 2, Drey 1, Mireille 2, Thorne 1, Bastian 90, Sigrun 96, and every cameo `FESTIVAL_*` team.

---

## 4. Game overs: the Ledger

**23 canonical game overs** (the story lead's 22 minus the cut "Encore", plus two new ones) and 2 Ruin-only extras. Titles, epitaphs, hints,
triggers, the foreshadowing that must be on screen first, and checkpoint placement are in NARRATIVE_KEYS §9–10, verbatim. Rules every one of them follows:
- **Fair.** Each is a deliberate player choice, warned at least once on screen in the same chapter, and most need a confirm or a repeated
  prompt. None fires from a cumulative stat on its own (Pull the Nail is *offered* only at high Hollow trust, but you still have to say yes).
- **Cheap to retry.** `Prismfall.checkpoint` sits directly before each trigger, so a curious player loses seconds, not an hour.
- **Recorded.** Each death writes its epitaph to the cross-save Ledger, where it stays across new games.

| Act | # | Game over | Kind | One-line trigger |
|---|---|---|---|---|
| I | 1 | Homeward | joke (tutorial) | go back on the ferry |
| I | 2 | Two in the Orchard | defy a warning | pull Juno through the Veil |
| I | 3 | Curtain Call | darkly funny | join the ghost company "forever" |
| I | 4 | Live Wire | defy | grab the cracked Zap Plate barehanded |
| II | 5 | Sinkfield | defy | step off the bones for the glint |
| II | 6 | Sweet Tooth | darkly funny | take the Sweetrot a third time |
| II | 7 | Let Them Listen | complicity | take the Hammer's detonator |
| II | 8 | Pull the Nail | betrayal (Sable's) | plant her charge where only you can walk |
| III | 9 | Loyal | choice | stand with the Loyal Three |
| III | 10 | **Weather** *(new)* | **battle you were told to flee** | fight Kyogre the moment it wakes instead of running for the towers |
| III | 11 | Thin Ice | failed escape | go back for the data core |
| III | 12 | Read the Fine Print | interlude (as Kestrel), darkly funny | open Voss's drawer |
| III | 13 | Looking Back | defy | look back through the Glass |
| IV | 14 | Willing | capture | let Quent "examine" you |
| IV | 15 | Echo | defy | stay for your mother's echo three times |
| IV | 16 | Overtime | **timed** | keep copying past the klaxon |
| IV | 17 | Into the Line | defy | step between the Directorate and Nadir |
| IV | 18 | The Throne | capture, darkly funny | sit on the Gilded King's throne |
| V | 19 | Fair Bargain | darkly funny | buy an answer without asking the price |
| V | 20 | **Somebody Else's Story** *(new)* | choice-based | agree to stay out of Crownhaven |
| V | 21 | Liar's Pyre | defy | tell the brazier "Whatever you want to hear." |
| V | 22 | Early Crown | betrayal (Valen's) | accept the crown the night before the Final |
| V | 23 | His Hand | betrayal (Voss's) | take his hand at the hijack |
| Ruin | R1 | Welcome, Behind | Ruin-only | accept Archseer Dask's offer to stay behind the Glass |
| Ruin | R2 | Long Live the King | Ruin-only | kneel to Theodric |

**The two new ones.**
- **Weather (Ch11).** At step 4 of the Thaw, "the lake *breathes*". Anja, already running: "That's not a Pokémon, that's *weather*. Towers!" Prompt:
  *Fight it now* / *Get to the towers*. Fighting starts an unwinnable lv 80 Kyogre (one Primal-rain Origin Pulse). *"You tried to fight the sea.
  The sea didn't notice. In spring, Rimeholt carved your name on the ice wall, and the thaw took that too."* Choosing the towers continues to the
  partner battle and the real boss, as written. This is the game's one "battle you were told to flee", and it teaches the Ch21 lesson early.
- **Somebody Else's Story (Ch18).** After K7, Kestrel: "Don't come. I mean it." Prompt: *Stay out of Crownhaven?* → *He's already walking away.
  Let him go?* Everyone who matters has told the PC it must be them (Celestine's "walker", Sigrun's summons, Larch's letter). *"You did what
  everyone had told you since the ferry. The Engine took Kestrel instead. He lasted eleven minutes. Velmora lasted a week."*

**Cut:** "Encore" (Ch20). It needed four conditions to fire and duplicated Into the Line's lesson ("don't make them choose"). Dorian's ad-lib
stays as flavor; the PC simply doesn't go up.

**Hints.** After the first ending is seen (or with the `ledgerhints` password), unfound Ledger slots show a one-line riddle instead of "???".
Hesper Vane's lighthouse mirror has one crack per game over found; at 23 the cracks make a door shape (the only diegetic hint that the Ledger means something).

---

## 5. The Ruin Route: "Every Type and None"

### 5.1 Unlock and branch
- **Unlock:** all 23 canonical game overs in the Ledger (`ruin_unlocked`).
- **In-story trigger:** Ch15, right after the Giratina boss in the Reverse Depths. A pane of black glass shows Juno on the other side, calling
  the PC's name: the exact image of *Looking Back* (GO 13). On a save with a full Ledger, the prompt appears again: **Look back?** Saying yes no
  longer kills you. The reflection steps aside, and the PC walks *through*. (`:ch15_look_back`; `no` keeps the main story and the door never
  reopens on that save.) The branch comes after K6, so Kestrel's state is already set.
- **Why it needs every death:** inside the Glass, the PC finds out that every game over *happened*. Antumbra is the reverse side of the world,
  where things that almost were are kept, and Giratina kept every one of them. You can't walk into the Reverse until it knows your face, and it
  learns your face from your graves.

### 5.2 What the Ruin Route reveals (never stated on the main route)
1. **The Ledger is real.** The Reverse Depths' floor is a field of twenty-three graves, each carved with its epitaph. "You have no Imprint in
   Velmora. In here, you have twenty-three." The PC's **Reflection** stands up from the last grave: the one who remembers dying every time.
2. **Antumbra is an unfinished Judgment.** At AF 0, when the Chain closed, Arceus *began to judge Aurelia*: to unmake it. The Prismfall was
   the god choosing to break itself rather than finish. The half-done unmaking is Antumbra. Rivers run uphill there because that's what a world
   looks like halfway to nothing. Giratina, guardian of reverse places, has held the seam shut for three hundred years so the sentence can't finish.
3. **The verse of none.** Maren carved a third verse of the Hymn of Return on the Reverse side of the Concordance, where only the Glass could
   read it: *"And if the walker comes with no color in their heart, the god will come home to finish what it began."* A whole Arceus, returned
   to a land that chained it, could complete the Judgment of AF 0. Celestine knew: "I cannot lie, so I stopped singing it."
4. **What "I learned that here" means.** In every main-route ending Arceus says "I will not take what is not given. I learned that here." It's
   talking about Judgment. It came within one heartbeat of unmaking a kingdom, and chose to break instead. Homecoming works because the Wardens
   *give*, and the PC carries the shard in Harmony. The Ruin Route is the PC deciding nobody, god or Crown or company, should hold that power again.
5. **The Gilded King is still alive, behind the glass.** Antumbra froze the Sun Court at the instant of the Calling. Theodric's reflection stands
   in it mid-command, the reflected Chain in his hands. Voss has dreamed of him all his life.

### 5.3 Chapter outline (replaces the rest of Ch15 through Ch21)
- **R1 "Twenty-Three Graves"** (Reverse Depths). The graves; the Reflection, who speaks in the PC's own authored lines, reversed. **Mirror battle:
  the Reflection** (your own party, generated at your levels, on `:INVERSE`). Then **Giratina (Origin) tests the Renegade** (multi-bar trial on
  `:INVERSE`). Giratina gives the PC the **none**: Resonance locks at ruin (≤ −6), and the Ledger becomes a Key Item, *the Black Case*.
  New traversal, **Mirrorwalk**: marked mirrors in Zenith, Nadir, Elowen and Ashkaar open onto their Reverse maps.
- **R2 "Built to Break"** (Cogsworth, Gym 15). The PC now *wants* the Engine finished: it's the only machine that can hold all eighteen Plates
  still long enough to unmake them. Zekrom still has to be freed (the core must fail so Voss reroutes everything to Crownhaven). `:ch16_magnus`
  reads differently: *expose* means you ruin him so nobody stops the build; *conscience* means you persuade him to build it "to break right".
  **Gym 15 (Ruin):** Magnus on `:FACTORY`, which becomes `:SCRAPYARD` on turn one: "You came here to break it. So did I, once."
- **R3 "The Sun Court Below"** (Underveil, Gym 16; Aurelia). Nyx sides with the Renegade; her house kept the drowned truth for three hundred years
  and she's tired of it. **Gym 16 (Ruin):** an illusion double battle where `:NEW_MOON` runs with Inverse matchups. In the Sun Court, Theodric's
  reflection fills the mirror-wall. Voss walks in, sees him, and falls to his knees: "He's alive. Behind the glass he's still alive." He leaves
  with the cradle, serving a dead king now.
- **R4 "Midnight in Gloaming"** (Gym 17; Pecharunt; K7). Celestine tells the PC the verse of none, and refuses the badge. **Gym 17 (Ruin):** `:FAIRY_TALE`
  turns `:INVERSE` for her last Pokémon ("Once upon a time, which was the only time"). Xerneas does **not** wake; the dusk stays. K7 plays as
  written, but Kestrel knows: "You're going to *erase* her? Everything she paid for?" `:ch18_kestrel_ring` is still offered.
- **R5 "The Last Gate"** (Wyrmrest, Gym 18). The oath can only be true one way: "I'm going to end it. All of it." Reshiram accepts the truth and
  flies away without a fight. **Gym 18 (Ruin):** Sigrun on `:DRAGONS_DEN`, no Reshiram, every Pokémon a step faster ("Dragons don't let anything
  through they haven't weighed. I've weighed you."). The Dominar can't be swayed; his legions march on Zenith during the Festival.
- **R6 "The Unfestival"** (Festival week). The Accord bars "the Renegade". Archseer Dask claims the PC for the Veiled Synod and walks them in through the Glass; Dorian, who has never
  once let the bowl ruin a story, seeds them anyway. **R16 Juno** ("You'll make sure Verdance never gets an autumn."), **QF Archseer Dask** (his offer to stay behind the Glass is
  `GO_R_WELCOME_BEHIND`), **SF Kestrel** (he tears the Gauntlet off to fight you as himself), **Final Valen, the Last Tuning** ("I'll hold them quiet
  one more time. I'll die doing it. That's still better than you."). No exhibitions. Ilsa, earmuffs off: "You're thinking very loudly. Twenty-three times."
  At the Night of Masques, the actor playing the Gilded King freezes mid-line, because the mirror behind the stage is showing the real one.
- **R7 "Every Type and None"** (the finale). At the Coronation the Engine wakes, but the hand that reaches up through the arena's crystal walls
  isn't only Voss's: **Theodric's reflection** steps through wearing the Chain. Voss kneels (kneel with him: `GO_R_KNEEL`). When Theodric casts him
  aside, `:ruin_voss`: *spare* him or *abandon* him to the Chain. **Hijack: Theodric.** Then Arceus descends, not dragged but *coming*, to finish what
  it began. **True Finale: Arceus (Judgment)**, seven bars, Giratina at the PC's side (player side of two), the last bar on `:INVERSE` as Giratina
  turns the arena inside out. Valen holds the Ring one last time, to keep the crowd alive while god and Renegade fight. Then the Unmaking.

### 5.4 Final boss, endings and cost
- **Final boss:** Arceus (Judgment), `ARCEUS_JUDGMENT` (NARRATIVE_KEYS §6.6).
- **The Unmaking needs a vessel.** The *none* unmakes the Chain, the Plates, Judgment and finally the Glass, and whoever carries it goes with the
  Glass. The Reflection offers to go in the PC's place: "I've done this twenty-three times. Let me do it once on purpose." Then **`:ruin_walk`: who
  walks out of the Glass?**
  - **`:me` → END_UNMAKING "The Unmaking".** The Reflection is unmade with the Glass. Antumbra and Velmora fold into each other. Every Imprint ends at
    once: no fields, no Bleed, no miracles; Rimeholt thaws, Cindervault cools, Verdance gets its first autumn (Juno won't look at the PC while it
    falls). The Fixed wake, *all* of them, even the long-Fixed who had stopped dreaming, and some of them wake as strangers. Arceus, with nothing left
    to judge or be chained by, leaves as a light with no color and never comes back. Giratina, the final witness, closes its eyes. Mirrors are just
    mirrors. The PC is the only person alive who remembers the old world, and twenty-three ways it ended. The scar is still colorless, by choice.
  - **`:reflection` → END_REFLECTION "The One Who Came Back"** (secret). The PC is unmade with the Glass, and the Reflection walks out wearing their
    face, which is GO 13's epitaph come true. The epilogue is the same world as the Unmaking, seen slightly wrong: the Reflection signs its name
    mirrored once and corrects it; Juno, raking the first leaves: "You never used to hum." Last image: Hesper's lighthouse mirror, with nothing behind it.
- **Post-game:** Antumbra's mirrors stay open as ordinary places (the Reverse maps), Giratina is catchable at the Distortion Core, there is no Arceus,
  and the Festival never runs again. On END_REFLECTION the post-game is played as the Reflection (nobody else notices).

### 5.5 Why it's worth playing
It answers the three questions the main route leaves open (what Antumbra is, why the Ledger remembers, what Arceus meant by "I learned that
here"), and once you know them, Homecoming reads differently: it was one consenting Warden away from the end of the world. It adds four
re-fought gyms, a new Festival bracket (Dask, Valen of the Last Tuning, Theodric), the only scenes where the Gilded King speaks, Giratina as an
ally, Mirrorwalk maps, two endings, and two more graves for completionists.

---

## 6. Endings

### 6.1 The final decisions
1. **Ch17, the Sun Court (`:ch17_voss_offer`).** Accepting is a promise you keep or break later.
2. **Ch21, the hijack (`:ch21_hand`, only if you accepted).** Taking Voss's hand ends the game in **Concord Dawn** before Arceus is ever fought.
   Without the promise, the same gesture is `GO_HIS_HAND`.
3. **Ch21, the True Finale.** If the Engine is fully calibrated, the PC fights *for* Arceus and loses the struggle anyway: **The Gilded Chain**.
4. **Ch21, Arceus speaks (`:ch21_final`).** The PC says it aloud:
   - **Return** — "Go home. Take them with you." (always)
   - **Keep** — "I'll keep them. I'll keep everyone safe." (always)
   - **Borrowed** — the PC hesitates, and Kestrel (redeemed and devoted) or Sigrun (Bond ≥ 6) steps forward: "Not you. Let me be nearest."
   - **Concord** — "Stay. Stay and power the world." (if you accepted Voss's offer, or Magnus's governor was never switched off)
   - **Unmake** — "No. No more gods." (main route: Resonance ≤ −6, or Hollow trust ≥ 4 with Rowan radicalized or Kroll never publicly exposed)
5. **Ruin Route, R7 (`:ruin_walk`).** Who walks out of the Glass.

### 6.2 What decides the outcome
- **Wardens' Consent** = how many of the 18 Wardens release their Plate (NARRATIVE_KEYS §5 `WARDEN_CONSENT`, one condition each, in gym order).
  It's on screen twice: Tamsin's white and grey banners (Ch20), and the Arceus fight itself, which is six bars of three locks each. Between bars
  those three Wardens kneel and let go, or refuse. Every refusal makes the next lock **forced** (Arceus gains +1 to every stat stage for that bar).
  Each refusal has a reason the player caused: Tamsin can't afford it (her secret kept), Dorian keeps the lie he knows (you told the official story),
  Rook can't reach his Plate, Corvin is in a cell, Brann won't for a man who gave the Light Stone away, Kaito never confessed, Anja "drowns without
  it", Odessa remembers the burned letter, Bastian remembers the beacon, Ysolde lost Kestrel, Magnus "won't hand my city's future to a god",
  Celestine hears the wrong key, Sigrun meant to wear the Crown.
- **Engine breaks** = eleven lamps on Larch's board: telemetry destroyed or sabotaged (sabotage counts twice), Zekrom freed, Magnus's
  conscience, Rook still inside, Nyx's precise blackout, Calla's schematics (twice if she went back), Marchetti turned, the Lantern Hollow at the
  pylons, Kestrel not lost. **The Engine is calibrated** (Bad ending live) only if the telemetry was left running, Magnus wasn't reached, *and*
  three or fewer lamps are lit.

### 6.3 Conditions matrix (first row that matches wins; exact strings: NARRATIVE_KEYS §12)

| # | Ending | Kind | Condition |
|---|---|---|---|
| 1 | **The One Who Came Back** | Ruin (secret) | Ruin Route and the Reflection walks out |
| 2 | **The Unmaking** | Ruin | Ruin Route |
| 3 | **Concord Dawn** | Grey | took Voss's hand (after accepting in Ch17), or chose Concord |
| 4 | **The Gilded Chain** | **Bad (canon)** | Engine calibrated |
| 5 | **The Hollow Spring** | Grey | chose Unmake (main route) |
| 6 | **The Borrowed Crown** | Grey | let Kestrel or Sigrun take it |
| 7 | **The Long Vigil** | Grey | chose Keep |
| 8 | **Homecoming, Unfinished** | Grey | Return, but Consent < 12 or Resonance < 2 |
| 9 | **The Empty Lighthouse** *(new)* | Grey | Return with Consent and Harmony, but Kestrel burned out in the Engine |
| 10 | **Homecoming** | **Good (canon)** | Return, Consent ≥ 12, Resonance ≥ 2, Kestrel alive |

### 6.4 Epilogue beats
The story lead's scenes in 08_ACT_V stand for Homecoming, the Gilded Chain, the Long Vigil, Unfinished, the Hollow Spring, Concord Dawn and the
Borrowed Crown. This spec adds the conditions that vary them, and three new endings.
- **Homecoming (Good).** As written. The variable slides: Elin wakes in Rowan's arms *or*, if Rowan drowned at the Fault, Juno alone holds her aunt
  and tells her; Teo on the Ebbmouth quay or his photo on the guild wall; Kestrel as Ghost Warden (`KESTREL_ACCEPTED_SEAT`) or a Gale Post wanderer;
  Calla's name on the Spire memorial if she went back; the quarantine lifts now (`ENVOY_PERSUADED`) or a year late; Voss watches the sunrise
  (spared) or is light at the arena's heart; Nadir's first elected seat with Nyx in it.
- **Homecoming, Unfinished (Grey).** One slide per refusing Warden's city, in gym order, each a single image of what the Last Shatter took
  ("Briarwick: the looms went still in one night. Tamsin weaves by hand now."). If Resonance was below Harmony, the PC's scar never takes the land's color.
- **The Empty Lighthouse (Grey, new).** Everything in Homecoming happens, but Kestrel burned out as the Engine's conduit. Hesper climbs the
  lighthouse every night and lights a lamp nobody needs. Ysolde keeps the Ghost seat. The PC reads Morwen's letter aloud at the grave he never
  visited, the letter he never opened. Last slide: Kestrel's Aegislash, sheathed, on the PC's belt.
- **The Long Vigil / The Borrowed Crown (Grey).** As written; the bearer is Kestrel if `KESTREL_BEARS`, else Sigrun. With Sigrun: "Ten years.
  Maybe twelve. I was relieved once. Never again." Juno and the PC swear to find another door either way.
- **The Hollow Spring (Grey).** As written. If Rowan drowned, Thistle plants the first seed in plain soil; if Teo lived, he's the one who won't
  speak to her.
- **Concord Dawn (Grey).** As written, plus: if reached through `:ch21_hand`, the PC never fights Arceus at all, and the last slide is the PC
  reading the arena's power output on a Council screen with Celestine's line over it: "Once upon a time a god was kept in a box. It was quiet. For a while."
- **The Gilded Chain (Bad).** As written. The PC as "the Sovereign Who Sleeps". If Quent hijacked, the mug on the desk is Quent's, not Voss's,
  and Voss is in the crowd of schoolchildren's parents, visiting.
- **The Unmaking / The One Who Came Back (Ruin).** §5.4.

### 6.5 Post-game state
Per NARRATIVE_KEYS §12. In short: **full** post-game (Concordance Spire, Warden's Gauntlet, Distortion Core, legendary rematches) after Homecoming,
Unfinished (refusers are absent from the Gauntlet and their cities keep Bleed scars), Empty Lighthouse, the Long Vigil (the PC is Sovereign; the
Gauntlet is framed as Sovereign's audiences), the Borrowed Crown (the bearer is absent) and both Ruin endings (Mirrorwalk maps stay open).
**Partial** after the Hollow Spring (Spire and Gauntlet only; most legendaries are gone with their Plates) and Concord Dawn (Spire only; the
Wardens are pensioned off; Quent's Concord Zero arc starts). **None** after the Gilded Chain: credits, then the title screen.
Zygarde chooses the PC at Valen's memorial in any ending with a memorial if Valen's Bond is 3 or more, or Ilsa reconciled with him (`ZYGARDE_CHOOSES`).

---

## 7. Other systems

1. **Quiet Hours (relationship scenes).** A bench icon at Pokémon Centers when a Bond first reaches friendly and again at close: 20 short scenes
   (Juno's seed catalogue, Kestrel teaching the PC to throw stones at the lighthouse, Ysolde lighting a lantern for Ines). Each grants +1 and a
   keepsake at close (Juno's seed packet = a Grassy Seed; Marisol's union pin; Nyx's crescent earring, which sells for one Poké Dollar and is
   priceless). *Impl.:* one common event per scene; condition `bond_tier(:X) == :friendly && !made(:qh_x1)`, register `:qh_<bond><n>` choice keys with value `[:seen]`.
2. **Interludes.** The act files already define five (Rowan, Kestrel, Wenlow, Valen…). Add **Interlude VI "The Night Ferry"** as Morwen in AF 290,
   unlocked after any ending: a stealth walk carrying the five-year-old PC to Edda's boat. Its last line is Morwen's echo's line from Ch15.
   *Impl.:* `pbChangePlayer` to the interlude character, stash `$player.party` in Core state, give a preset party, restore on exit; interlude
   choices never touch the PC's Bonds (except where the act file says so).
3. **Field Notes.** Each field gets an entry on first battle; individual effects fill in only once *observed* ("Fire moves hit harder here.").
   `:BLEED` keeps a log of which fields it has borrowed. *Impl.:* listen to `:prismfall_field_changed`; Field Effects marks effect lines as seen
   when they trigger; Core stores a set per field.
4. **The Ledger viewer and Hall of Reflections.** The Ledger also records every Festival opponent variant the player has **met**. Post-game,
   the Distortion Core's **Hall of Reflections** lets them re-fight any variant they've met in *any* playthrough (Kestrel Fallen, the Gardener,
   Brann for Valen, Quent…) at lv 100. It reuses every team the balance team built. *Impl.:* Ledger lines `MET:<ENTRANT>`; the hall's menu reads them.
5. **The Second Ferry (New Game+).** After any ending, the `secondferry` password starts a new game that keeps the Ledger (always), Field Notes,
   Pokédex *seen* flags and one Pokémon of choice from the Hall of Fame as "a passenger". Ines's letter gains a postscript that matches the last
   ending seen. The Journal shows faint "echo" lines under choices made in the previous run. *Impl.:* a carryover file written at the ending,
   read by the password handler.
6. **The Velmora Gazette.** Two headlines per chapter per Pokémon Center, chosen by condition strings from a table (§1.4). *Impl.:*
   `GAZETTE[chapter] = [[condition, headline], …]`, first match per slot, shown by a newspaper event.
7. **Promises.** A Quest Log category for things the PC says they'll do ("I'll come back for a Fizzbolt," to Dex; "I'll look after her," to
   Rowan). Kept promises pay off in epilogue slides; broken ones get one quiet line. *Impl.:* choice keys `:promise_<name>` with
   `[:made, :kept, :broken]`; the Quest Log lists `:made` ones.
8. **Passwords.** Core's table plus `ledgerhints`, `nomercy` (no checkpoints before game overs), `openbook` (numbers on the Ties page),
   `colorless` (halved Resonance swings) and `secondferry` (NARRATIVE_KEYS §14).

---

## 8. Requests for the story lead (reconciliation list)

Edits the act files need so they match this spec. Keys and conditions are in NARRATIVE_KEYS; nothing here changes a LOCKED SPINE item.
1. **All files:** write choice keys as lowercase symbols (`:ch9_teo_sable`); outcome names like `TEO_SAVED` stay as they are (they're derived flags).
2. **Bond mentions for non-Bond characters** (Tamsin, Sahar, Brann, Anja, Rook, Corvin): replace "X's Bond goes up/down" with the choice key; their
   payoff is their Consent condition (NARRATIVE_KEYS §5). Ysolde and Marisol **are** Bonds now.
3. **04 Ch2:** add the Glass Matriarch prompt (`:ch2_matriarch`: soothe / silence) after the boss.
4. **04 Ch5:** add Dorian's refusal line for the Arceus fight if the PC told the Directorate "The Mourner broke the Plate".
5. **06 Ch11:** add the *Fight it now / Get to the towers* prompt at "the lake breathes" (`GO_WEATHER`); make the strike's optional tag battle the
   `:ch11_strike` choice (stand / mediate).
6. **06 Ch13 tribunal:** the Splitter Casing alone is circumstantial. Public exposure of Kroll at the tribunal needs the Ironreach comm-device; the
   casing still lets the PC turn Marchetti in Ch14.
7. **06 Ch13 Fault (new MAJOR):** add `:ch13_fault`. If the PC pulls out Marchetti, Rowan drowns in the flooded undercroft and Wick's people can't
   reach him. Knock-ons: the Lantern Hollow is led by Teo (if saved) or by Thistle and Wick; "the Gardener" can't enter R16; Homecoming's Bride
   Tree scene is Juno alone; the Hollow Spring's seed is Thistle's; Rowan's Act IV–V lines go to whoever leads.
8. **07 Ch15:** after the Giratina boss, the Ruin trigger (only with a full Ledger), §5.1.
9. **07 Ch16 `:ch16_rook`:** *leak_now* gets Rook fired and blacklisted from the Spire, so he can't cut the grid in Ch21; *hold* keeps him inside.
   Update the hijack montage line to fire on `ROOK_CUTS_GRID`.
10. **07 Ch17:** Nyx's refuse branch is fine as written (her blackout happens, but it doesn't count as an Engine break).
11. **08 Ch18:** after K7, add *Stay out of Crownhaven?* (`GO_STAY_OUT`).
12. **08 Ch19:** Liar's Pyre's hidden option is simply always offered (no lie tracking). The *Ruin* oath needs Resonance ≤ −2.
13. **08 Ch20:** add Calla's defection scene at the Night of Masques (`:ch20_calla`); Envoy Okoro's *proof* needs two of the three proofs; cut
    GO-20 Encore; Valen's collapse is `VALEN_COLLAPSED` (no Little Owl, a refusal with a cold Bond, and the telemetry left running).
14. **08 Ch20 Draw:** stage the Right of Grievance (Marisol), Kaito and Odessa yielding their invitations, Juno giving hers to "the Gardener",
    the QF draw lines for Sigrun, Kaito, Ysolde and Odessa, and Celestine's withdrawal on the Ruin Route (§3.2, §3.6). Anja (exposed) replaces the story lead's
    Tamsin variant, which is cut (no Tamsin Bond to read).
15. **08 Ch21:** Fallen Kestrel is not a hijack opponent; he's harnessed as Voss's conduit and `:ch21_reach_kestrel` plays between Voss's second
    and third bars. The tag partner is Juno when he's Fallen.
16. **08 Ch21 Arceus:** six bars of three locks in gym order; write all 18 release lines and all 18 refusal lines (reasons in §6.2).
17. **08 Endings:** add **The Empty Lighthouse**; the Gilded Chain's Quent variant; the two Ruin endings (§5.4) replace the Unmaking sketch, and Archseer Dask
    is the Ruin QF (his offer is `GO_R_WELCOME_BEHIND`).
18. **Ruin Route (new):** chapters R1–R7 (§5.3) need scripting, plus four Mirrorwalk Reverse maps (World lead) and black badge art (art).
19. **Hints to plant on the main route:** Ilsa's "You're thinking very loudly" count line only after any game over is in the Ledger; Hesper's cracked
    mirror; Arceus's "I learned that here"; Celestine phrasing the Hymn as "the verses I sing".
20. **03_CAST** still lists the retired canon cameos and Revision 2 kingdom names in places; update to Revision 4.
21. **Revisions 4–6 (Festival):** no cameos and no outsiders. Rewrite 08_ACT_V's Festival as the Blessing rite with kingdom delegations (§3.1),
    the pools and reassigned lines in §3.2, companion-match highlights (§3.4) and the exhibitions in §3.6. Venam's "I could hear everything" goes to
    Teo if he lived, otherwise Corvin's ward records. CAMEOS.md's default draw is obsolete.
22. **Rev 5 screen-time fixes:** give Anja one Act IV scene and Ysolde one pre-Ch15 scene; introduce Archseer Dask again in Ruin R1 and R4 (done in
    §5.3's intent; script it); the Eevee Octave is cleared (Vesper is met in Ch3 and Ch13).
23. **The war (Rev 6):** build the chapters around the six `:war_*` choices above, with Anja's capture, the siege of Skaldfast, and a climax cutscene
    whose ending frame follows `WAR_STOPPED / WAR_BOTH_BROKEN / WAR_ASHKAAR_WON / WAR_ISENMAR_WON` (NARRATIVE_KEYS §4.3). Ch19's Dominar petition
    must read the war's outcome.
