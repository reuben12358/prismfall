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
| **Kestrel** | −1 | the rival who can fall | Fallen at ≤ −4 (or ≤ 1 with the pity line); devoted (8+) lets him take the Borrowed Crown; Ghost seat with Ysolde |
| **Rowan** | 0 | the Mourner | radicalized (≤ −2 after being condemned) opens the Hollow Spring; his R16 appearance needs mercy, not affection |
| **Voss** | +1 | the first person who was kind to you | how warmly he offers, how bitterly he takes refusal; Ruin R4 |
| **Valen** | 0 | the father-figure who planned your life | his collapse (≤ −2 with a refusal at the audience); his last words; Zygarde chooses the PC post-game at ≥ 3 |
| **Ilsa** | 0 | the daughter who reads minds | Little Owl (≥ 3 to start, ≥ 4 to reconcile); Consent (≥ 5 or reconciled) |
| **Sigrun** | 0 | the heir who was relieved | Final stand-in (≥ 5); Borrowed Crown bearer (≥ 6) |
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
  the Engine (§6.2). "Fewer than four, and it holds. I can't make that sound kinder."
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
- ★ **`:ch19_oath`** — at the Draco brazier, aloud. **Return** / **Keep** (Valen +3; Alexandra comes to the QF to ask whether the Fixed will
  ever wake; Sigrun won't let go of the Draco Plate) / **Open** ("I don't know yet") / **Ruin** (only at Ruin-leaning or lower; Sigrun draws her
  blade and lets you pass). The hidden "Whatever you want to hear." is `GO_LIARS_PYRE`.
- **`:ch19_dominar`** — the petition. *swayed* (needs the Light Stone at Wyrmrest plus proof, or Sigrun ≥ 4) / *failed* (the legions march on Zenith).
- **`:ch20_envoy`** — Envoy Okoro. *proof* (needs two of: Larch Papers, Arbiter Blueprints, Venam's testimony; no Severance) / *plea*.
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

## 3. The Festival draw

### 3.1 In-world: the lots are honest, the bowl isn't
The Hierophant draws lots from the crystal bowl on the Basilica steps (08_ACT_V). The draw *looks* random. It isn't, and Velmorans half-know it:
the Accord's old customs let certain people choose their opponent. The **Right of Grievance** lets a Warden claim a first-round match against a
challenger who wronged their city. A **Warden's invitation** can be given away. A Sovereign who can't stand is replaced by a stand-in. And
Dorian, the Accord's Pageant-Master, has never once let the bowl ruin a good story. Every rule below has one of those reasons on screen.

### 3.2 Stage pools (first matching candidate wins; the last line is the fallback)

| Stage (cap) | Priority | Opponent | Condition (plain words; exact strings in NARRATIVE_KEYS §6.2) | On-screen reason |
|---|---|---|---|---|
| **R16** (90) "someone from your past" | 1 | **Marisol** (Grievance) | Teo died and Marisol is below close-friendly (≤ 2) | Right of Grievance: "Let's see you run past *me*." Kaito yields his invitation to her |
| | 2 | **Anja** | you exposed her to the Thane's court | "You threw me to the court. Fine. Ice remembers." Odessa gives Anja her place |
| | 3 | **Rowan, "the Gardener"** | Rowan lived, you pleaded mercy, and the Hollow trusts you (≥ 4) | Juno gives her uncle her own invitation: "One last garden, child." |
| | fallback | **Juno** (J4) | — | "We started on the same dock." |
| **QF** (92) "the stranger" | 0 | **Nova** | Ruin Route | Shiv walks her through the dream in his place |
| | 1 | **Titania** | Resonance ≤ −3 | "I came to guard someone. Now I think I'm guarding everyone from you." Amaria withdraws |
| | 2 | **Alexandra** | your oath was Keep | her mother sleeps in crystal: "If you keep them, do yours ever wake?" |
| | 3 | **Garret** | Kestrel has fallen | "Somebody's driving your rival. I want to see who's driving you." |
| | 4 | **Melia** | five or more Bonds at close (≥ 5) and Harmony-leaning | "Everyone keeps telling you what you're *for*. Have you decided yet?" Venam hands her the invitation |
| | fallback | **Lin** | — | the headline: "your god's in pieces and your champion's made of glass. cute region." |
| **SF** (94) "the mirror" | 1 | **Kestrel (Fallen)** | `KESTREL_FALLEN` | he keeps the Gauntlet on and fights like someone drowning |
| | fallback | **Kestrel (Redeemed)**, K8 | — (Ruin Route: same team, Ruin dialogue) | he tears the Gauntlet off: "If I beat you, I beat *you*." |
| **Final** (96) "the crown", drawn live on Day 7 | 0 | **Valen, the Last Tuning** | Ruin Route | he fights to hold the Plates quiet one more time, and to stop you |
| | 1 | **Sigrun**, Sovereign-designate | Valen collapsed, and Sigrun is close (≥ 5) | "He beat me with an arm made of glass. Now he can't stand. So it's me." |
| | 2 | **Brann** | Valen collapsed | "He asked me to. Last thing he asked." |
| | fallback | **Valen** | — | Zygarde, Complete on its last bar |
| **Hijack** (100), drawn live | 0 | **Theodric, the Gilded Reflection** | Ruin Route | the Gilded King steps out of the arena's crystal walls |
| | 1 | **Dr. Quent** | Voss discredited (Magnus exposed + Rook's leak + the Night of Masques) | the board removed Voss; Quent giggles in the harness; Voss watches, appalled |
| | fallback | **Voss** | — | "You carried my key through eighteen doors." |
| **True Finale** (100) | — | **Arceus** variant | Judgment (Ruin) > Gilded (Engine calibrated) > War (Resonance ≤ −6) > Miscalibrated (telemetry sabotaged) > Bound | §6.2 |

### 3.3 Proof: exactly one opponent per stage, never the same person twice

1. **At least one.** Every stage's list ends with an unconditional fallback (Juno, Lin, Kestrel, Valen, Voss; Arceus's last variant has no
   condition). Core's resolver returns the first entry whose condition holds and whose *person* isn't used yet, so it always reaches a match.
2. **At most one.** The resolver stops at the first match.
3. **No duplicates.** Each person appears in exactly one stage's list: R16 {Marisol, Anja, Rowan, Juno}; QF {Nova, Titania, Alexandra, Garret,
   Melia, Lin}; SF {Kestrel}; Final {Valen, Sigrun, Brann}; Hijack {Theodric, Quent, Voss}. The sets are disjoint (Core's validator enforces it),
   so the "person already used" check can never skip a candidate and no playthrough fights anyone twice. Variants (Kestrel Fallen, Valen of the
   Last Tuning) share a person with the default *of the same stage only*.
4. **Everyone drawn is alive and present.** Rowan's entry requires `ROWAN_ALIVE`. Quent precedes Voss whenever Voss was removed. Sigrun and
   Brann are only drawn when Valen collapsed. No other drawable person can die before the Festival.
5. **Vacated seeds never collide.** The five entrants who give up a seed (Kaito, Odessa, Amaria, Venam, Shiv) are on no stage list, and each is
   vacated by exactly one candidate; R16 candidates are mutually exclusive by priority, and so are QF candidates.
6. **Fallen Kestrel is not a hijack opponent.** The story lead's "Kestrel (Fallen) hijacker" would fight him twice; instead he's the Engine's
   harnessed conduit inside the Voss fight (`:ch21_reach_kestrel`).

### 3.4 Five sample runs

| Run | Key choices | R16 | QF | SF | Final | Hijack | Arceus |
|---|---|---|---|---|---|---|---|
| "The kind one" | saved Teo, mercy for Rowan, Hollow trust 5, five close Bonds, ring given, telemetry sabotaged | **Rowan** | **Melia** | Kestrel (Redeemed) | Valen | Voss | Miscalibrated |
| "The honest one" | chased Sable, exposed Anja and Magnus, oath Open | **Marisol** (Grievance beats Anja's priority) | Lin | Kestrel | Valen | **Quent** | Bound |
| "Meridian's friend" | Fellowship, dampers, telemetry left, Kestrel cold, oath Keep, cold refusal at the audience | Juno | **Alexandra** | **Kestrel (Fallen)** | **Sigrun** (Valen collapsed) | Voss | **Gilded** (Bad) |
| "The angry one" | burned the letter, silenced the Matriarch, Resonance −7, condemned Rowan | Juno | **Titania** | Kestrel (Fallen via low Bond) | Valen | Voss | **War** |
| "The Renegade" | Ruin Route | Juno (Ruin dialogue) | **Nova** | Kestrel (Ruin dialogue) | **Valen, Last Tuning** | **Theodric** | **Judgment** |

### 3.5 Where the displaced go
When an unseeded candidate replaces a default, the default isn't simply deleted (NARRATIVE_KEYS §6.3–6.4):
Juno moves into Kaito's seed (Marisol drawn) or Odessa's (Anja drawn) and loses her first match, which opens her "Garden Match" exhibition. When
Rowan is drawn, Juno is absent by design: she gave him her invitation. Lin moves into Amaria's, Venam's or Shiv's seed (Titania, Melia, Nova).
Alexandra and Garret are already seeded, so they just swap with Lin. If Core doesn't build `:vacates`, the fallback is that the default yields
their own place, with the same lines.

### 3.6 Exhibitions that vary
Always: the Eevee Octave and every eliminated cameo (CAMEOS.md). Conditional (NARRATIVE_KEYS §6.5): **Juno's Garden Match** (if she wasn't
your R16), the **Ebb Guild match** with Marisol while Teo heckles from the stands (Teo saved and Marisol close), **Lin** (if she wasn't your QF),
**Melia** / **Titania** (if not drawn), and **Morwen's Echo** on the Night of Masques: Ysolde lights the Cathedral lantern in Crownhaven and
Kestrel's mother fights the PC once, gently, "to see what I bought" (Kestrel and Ysolde reconciled, and the K6 line was Resolve).
On the Ruin Route only the Eevee Octave plays: the champions won't fight the Renegade for sport.

### 3.7 Teams the balance team must build
The full table, with `[TYPE, Name, Version]` for every entry, is NARRATIVE_KEYS §7: **15 new Festival teams** (Marisol 90, Anja 90, Rowan 90,
Alexandra 2, Garret 2, Titania 2, Melia 2, Nova 2, Kestrel Fallen 90–92, Sigrun 96, Brann 96, Valen 1, Quent 99, Theodric 0, Morwen 90),
**4 new Arceus boss configs**, and the non-Festival extras (Juno partner 70–72, Ch21 tag foes v21, four Ruin gym teams v1, the Reflection).
