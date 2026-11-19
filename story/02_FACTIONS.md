# Story Bible 02: Factions

> Faction **Standing** (Hollow / Meridian / Accord) is a Core-tracked value (SPINE Rev. 3). Choice keys and thresholds belong to `story/10_CHOICES_ENDINGS.md`. This file covers who the factions are and how they change. Trainer type IDs per SPINE: `HOLLOW_*`, `MERIDIAN_*`.

## Who wants the PC, and for what

| Power | What they think the PC is | What they want | When they learn it |
|---|---|---|---|
| **Meridian / Voss** | The keystone | To bring the PC, shard attuned by eighteen badges, into the Arbiter Engine | Prologue (the dock scanner reads NULL) |
| **The Accord / Valen** | The vessel | To crown the PC so the Crown is whole and the PC holds the Plates for a century | Ch9 (sees the PC unharmed in the Ironreach Bleed burst) |
| **The Hollow / Rowan** | The walker | To have the PC carry the Plates home (Rowan), or break them (Sable's faction) | Ch5 (the Mourner sees the PC walk into the Lowlight Shatter) |
| **The kingdoms** | A political asset | Elowen and Ashkaar each want the PC as *their* Velmoran champion at the Festival | Act III onward |

The game's spine is the PC learning they're wanted. Its climax is the PC deciding what they're *for*.

---

## THE HOLLOW

**"Let the land grieve."** Eco-zealots who believe the Plates are nails driven into Velmora's body and must be pulled out. They are partially right: the Plates *must* leave. They are wrong about how: breaking a Plate Shatters it.

### Iconography and culture
- Grey cowls. **Carved bark masks modeled on the Gossamer Ogre** of Elowen folklore, the misunderstood guardian. The sigil is **the Hollow Ring**, an empty circle "for the space the Plates should leave".
- Members call the Plates "the Nails". Rank-and-file call themselves **the Bereaved**, and almost every one of them has lost someone to the Bleed. Admins are **Pallbearers**. The leader is **the Mourner**.
- Rituals: they leave **bare soil** at every site they hit, "so something can finally rot". They sing dirges at Lattice pylons.
- Recruiting ground: **Nadir**, above all Mirefen and Ironreach, where Bleed-sickness and Zenith's runoff hit hardest. Sump Barons quietly fund them because anything that hurts Meridian hurts Zenith.
- Battle style: Grass, Ghost, Dark and Poison. Bereaved grunts field "mourning" teams of Pokémon rescued from Bleed zones, some visibly glassed (a palette swap only, no mechanic).

### Structure

| Role | Member | ID | Notes |
|---|---|---|---|
| The Mourner | **Rowan Ashby** | `HOLLOW_MOURNER` | Grass Warden of Verdance. See 03_CAST. |
| Pallbearer (theology) | **Brother Wick** | `HOLLOW_WICK` | Co-founder and author of the Return doctrine. Psychic/Ghost team (Bronzong, Chimecho, Musharna, Dusknoir). |
| Pallbearer (field) | **Mara "Thistle" Thistlewood** | `HOLLOW_THISTLE` | Ex-Briarwick weaver whose village Lowmarsh is a Quiet Town. Bug/Poison team (Ariados, Scolipede, Vespiquen, Dustox). Cuts the Lantern Theatre's curtain ropes at the Saltmere hijack (Ch2); the PC's first admin fight, at Briarwick's pylon (Ch3). |
| Pallbearer (cells) | **Teo Reyes** | `HOLLOW_TEO` | Ebbmouth cell leader, Marisol's brother, 19. Water/Grass team (Ludicolo, Quagsire, Lombre, Toxicroak). |
| Pallbearer ("the Hammer") | **Sable** | `HOLLOW_SABLE` → `MERIDIAN_KROLL` | Actually **Sabine Kroll** of Meridian Special Accounts. Dark/Poison team (Drapion, Honchkrow, Skuntank, Toxicroak). Carries Meridian **Splitters**, the Plate-breaking charges. |
| Cells | ~12, each 5–30 Bereaved | `HOLLOW_GRUNT` | Strongest in Nadir, Ebbmouth, Briarwick and Mirefen. |

### Why Rowan Ashby is the Mourner (justification)
1. **Theme.** The man who loves the land most is the one who sees the Imprint as a sickness. Rowan has spent 24 years in a garden that never stops blooming over soil that never gets to rest. "The flowers never die here. Do you know what that means? Nothing rots. Nothing returns."
2. **Motive.** His grief is literal and visible. His wife Elin *is* the Bride Tree, and he waters her every dawn. Every Hollow speech is a eulogy for her.
3. **Access.** He is a Warden. He has attended three Tunings, knows the ceremony is more than a lightshow, and was told by Valen to "tend his garden". He knows where Plates are kept and how Wardens think.
4. **Structure.** SPINE locks Juno's succession to the Grass seat in Act III. Rowan's unmasking at the end of Act II is the cleanest, most painful reason the seat falls vacant. It also turns the *friendly* rival's story into the emotional engine of Act III.
5. **A fair twist.** Clues are planted from Ch1 (see 09). Misdirection points elsewhere: the realm-wide rumor that the Mourner is Kestrel's dead mother, and Kestrel's own obsessive belief in it.
6. **Sympathy.** He never wanted deaths. The Lowlight Shatter (Sable's doing) horrifies him and drives him from "pull the nails" toward Wick's "carry them home". That pivot is the Hollow's arc in miniature.

### How the Hollow changes across the acts
- **Act I: theater and sabotage.** They hijack Saltmere's pageant (the Mourner's first appearance, and the question "Ask your Warden"), cut Meridian survey lines in Briarwick (the first sabotage, and Thistle's answer to that question) and spike Ebbmouth's tidal Lattice. The tone is romantic outlaws. At the **Lumen Gala**, the Mourner tries to *steal* the Zap Plate from Meridian's vault to stop the Lattice drain. Sable detonates a Splitter on it, the Lowlight Shatters, and the realm blames the Hollow. The Mourner's hand is burned catching the cracked Plate.
- **Act II: the split.** Rowan pulls back and starts hunting for "the other way" (the Legend Plate, the Hymn). Sable gathers the angriest Bereaved into **the Hammer**, a faction that wants more Shatters "until they listen". At Cindervault they compete openly: Wick's people try to vent the caldera safely while the Hammer tries to blow it. At **the Ironreach Conclave** the Hammer tries to Shatter the Fist Plate under the Wardens' feet. The Mourner shields the crowd and is unmasked and arrested.
- **Act III: leaderless and framed.**
  - The Hammer carries out a string of "Hollow atrocities". Some are real. Most are Meridian false flags, including the Skyreach relay bombing blamed on Larch.
  - Wick holds the faithful together in hiding: the **Hollow Sanctuary** (branch map 698), open to a PC with high Hollow Standing.
  - At Rowan's tribunal in Lucent, **Sable is exposed as Sabine Kroll**. With the Ironreach evidence (key `IRONREACH_EVIDENCE`) the exposure is public and immediate. Without it, only the PC and Ilsa learn the truth, and the public believes it later and less.
  - The Fault hits and Rowan escapes.
- **Act IV: the Lantern Hollow.** Rowan reforms the movement as **the Lantern Hollow**: no masks, no Splitters, and one goal, to carry the Plates home. They become uneasy allies who shelter refugees in Cragholm, guide the PC through Gravenmoor's barrows and fight beside Nadir during the Sump Purge. A die-hard Hammer remnant under a freed or escaped Kroll stays loyal to Meridian's money.
- **Act V: in the crowd.** Rowan, Wick, Thistle and (if alive) Teo come to the Festival disguised as Choir porters. During the hijack they guard the Concordance Ring pylons. The **Hollow Spring** grey ending is the dark version of everything they wanted, reached if the PC follows their original creed all the way.

### Hollow Standing: what it unlocks (story side)
- **High:** the Hollow Sanctuary branch; Wick teaches the Hymn's missing verse early; Bereaved grunts stand down instead of fighting (fewer grunt battles in Nadir); Thistle's defection in Ch14 happens earlier and warmer.
- **Low:** Hollow cells attack the PC as "Meridian's pet" in Act III, and the Hollow Spring ending is locked.

---

## MERIDIAN CONCORD

**"Light for everyone."** Velmora's energy company. It harvests Imprints with Lattices, stores the power in Prism Cells, sells it to every kingdom (and, under a quarantine exemption, abroad), and since Act II it polices the realm under **the Mandate**. It is the nicest-looking villain in the game: clean uniforms, real jobs, real light.

### Structure

| Division | Head | ID | What it does |
|---|---|---|---|
| Chair & CEO | **Aurelian Voss** | `MERIDIAN_VOSS` | Also chairs the Zenith Council. |
| Executive office | **Calla Wren** (aide) | — | Schedules, scanners, secrets. Quiet defector. |
| Grid Division | (board) | `MERIDIAN_GRUNT` "Linesman" | Builds and runs Lattices. Rank-and-file linesmen are decent working people, often from Nadir. |
| Security Directorate | **Director Helene Marchetti** | `MERIDIAN_MARCHETTI` | The Mandate's enforcers ("Directorate officers"). Steel/Electric team (Magnezone, Klefki, Bisharp, Electivire, Corviknight). |
| Research & Special Projects | **Dr. Percival Quent** | `MERIDIAN_QUENT` | Runs the **Arbiter Project** (the Engine) and **Project NULL** (the Type: Null → Silvally line at the **Meridian Black Site**, branch map 699). Psychic/Steel team (Metang, Porygon2, Bronzong, Reuniclus, Klinklang). |
| Special Accounts | **Sabine Kroll ("Sable")** | `MERIDIAN_KROLL` | Covert operations. False flags. |
| Public Relations | the "Light for Everyone" campaign | — | Rook Calder is its face. |

**Assets:**
- Meridian Spire in Lumen City, with its Dark Stone core (Zekrom).
- The Lattice network across fourteen cities by Act III.
- An airship fleet, the *Gilded Hours* class. The name is a family joke nobody gets.
- The Strade Works contracts in Cogsworth.
- The newly rebuilt **Meridian Prism Arena** in Crownhaven. Meridian paid for the Festival's new venue, and the Engine is inside it.

### The Arbiter Engine (Voss's plan, in plain terms)
1. **Eighteen Plates in convergence.** The Festival's opening ceremony provides them.
2. **A keystone.** The Legend Plate: the Crown's shard plus the PC's splinter. The keystone cradle is salvaged from drowned Aurelia in Ch17.
3. **Calibration.** Resonance data from Plate-attuned battles. Every badge the PC earns is recorded by the **Meridian badge case** Voss gave them on the ferry. Every Festival match on the Prism Arena is a calibration run.
4. **Power.** Originally the Dark Stone (Zekrom) in a Cogsworth core. After the PC frees Zekrom in Ch16, Voss reroutes to **Lumen's whole grid** fed into the arena, which is why Rook cutting the grid in the finale matters.
5. **The result.** An artificial Judgment that pulls Arceus down into a new Gilded Chain, made permanent. Voss calls it "**the last utility**".

**Weak points** (each tied to a player choice; triggers in 10_CHOICES_ENDINGS):
- Telemetry sabotage (Ch14): false calibration data.
- Zekrom freed (Ch16): the original core is lost.
- Magnus's governor (Ch16/21).
- Rook's grid cut (Ch21).
- Nyx's comms blackout (Ch21).
- Calla's schematics (Ch20).

The more of these the PC has in place, the more the Voss and Arceus fights tilt toward Harmony, and the more ending options open. If none are in place, the **Gilded Chain** Bad ending is live.

### How Meridian changes across the acts
- **Act I: patron.** Voss is kind on the ferry. The Fellowship card pays for the PC's Potions. Linesmen give directions. Meridian sponsors the gyms (Rook is literally on its billboards). At the Gala, after the Shatter, Meridian *restores the light* and Voss is the hero. The Accord grants the Mandate. The darkness is visible only in the margins: Tamsin's contract, the stuttering Ebb, Larch's frown.
- **Act II: protector.** Mandate checkpoints go up, first in Nadir. Directorate officers "escort" the PC "for their safety". Quent turns up at Cindervault running the geothermal tap that nearly blows the caldera, and his battle there is the PC's first Meridian admin fight. After Ironreach, Meridian takes Rowan into its own custody, not the Accord's. That is the first moment players should feel a chill.
- **Act III: the velvet fist.**
  - Mandate curfews in Skyreach. The Larch Papers are answered with a smear campaign, then a frame-up (the Skyreach relay bombing).
  - The Gale Post raid, where the PC battles Marchetti.
  - Voss's public charm stays perfect. When Kroll is exposed at Lucent, he publicly disowns her as a "rogue contractor", announces an inquiry, and gains in the polls.
  - Meridian test-fires the Engine in Cogsworth at the end of the act, which causes **the Fault**.
- **Act IV: exposed and unbothered.**
  - The PC learns everything: the telemetry (Ch14), the Engine (Ch16) and the lineage (Ch17).
  - **The Sump Purge** (Ch16): after the Fault exposes Aurelia, Meridian's Directorate "secures" Underveil and Nadir's lower districts, blaming Sweetrot gangs and the Hollow. Dozens die, Wenlow among them. Topside watches it on the news as "Operation Clear Air".
  - Nadir declares independence (Ch17). Councillor Sallow starts working against Voss from inside the Council.
- **Act V: host.** Meridian runs Festival security under a Council vote that Anja's swing vote can't stop. It sponsors the arena, the broadcast, even the confetti. At the coronation, Voss hijacks the ceremony.

### Meridian Standing: what it unlocks (story side)
- **High:** the Meridian Black Site branch, where the PC can obtain the Type: Null line. Voss's deal in Ch17 is offered warmly, and Concord Dawn is available. Directorate patrols wave the PC through. **Danger:** high Standing plus untouched telemetry is the road to the Bad ending.
- **Low:** Directorate ambush battles in Act III–IV, and the Fellowship card is cancelled in Ch12, which the PC hears about from a Mart clerk.

---

## THE ACCORD

**"Eighteen in Concord, One in Keeping."** The three-hundred-year-old treaty government: the Sovereign, the eighteen Wardens, the Chancellor's bureaucracy, the Wardguard and the Prism Choir. It is the realm's legitimacy and its oldest lie.

### Structure
- **The Sovereign:** Valen Corrigan, since AF 270. He holds the Crown and performs the Tuning.
- **The Accord Council:** the Sovereign and eighteen Wardens, with **Chancellor Ambrose Hollis** as administrator. Hollis is quietly on Meridian's payroll and passes the Mandate in Act II.
- **The Wardguard:** the Accord's soldiers, who guard Plates against kings. Since Kaito Ren left, they are mostly ceremonial, apart from their worst job: sealing Quiet Towns.
- **The Prism Choir:** clergy who sing the Tuning liturgy, led by Hierophant Maud Ellery. The PC's mother was a cantor.
- **The Keepers:** the hidden circle who know the secret articles. Valen, **Brann** ("the Sovereign's Hand"), the Underveil Wardens (Nyx's line), Gloaming's Warden (Celestine) and, unofficially, Ilsa, who read it out of her father's mind.
- **The Accord Archive** (branch map 838) is open to a PC with high Accord Standing. It holds the Concordance's Secret Articles in Maren's handwriting.

### The Accord's lies (in order of discovery)
1. That the Bleed is new and manageable. It has been worsening for a century, and the **Quiet Towns** were removed from maps.
2. That the Tuning is a symbolic lightshow. It is the only thing holding the Plates quiet, and it kills Sovereigns.
3. That Morwen Vane caused the Glassfall. Valen scapegoated her to keep the Tuning secret.
4. That the Prismfall was a gift. It was a god escaping a chain.
5. That the Plates are Velmora's forever. The founders swore they were *borrowed*, and Odo Prell erased the promise in AF 140.

### How the Accord changes across the acts
- **Act I: distant majesty.** Festival posters, the counting rhyme, Valen's broadcast ("every ten years, Velmora *endures*"). Valen appears in person after the Lowlight Shatter. He grants the Mandate because he believes a Hollow at war with Meridian is a bigger threat than Meridian.
- **Act II: the Conclave.** The Accord convenes in Ironreach to vote on extending the Mandate. The Hollow attack hands Hollis the votes. Valen sees the PC in the Bleed burst and recognizes what they are.
- **Act III: fault lines.**
  - The Council splits into blocs (see 01_WORLD_LORE §9).
  - The kingdoms test the Accord: Elowen claims the Meadow Plate, Isenmar declares martial law, the Dominar threatens war.
  - Valen backs Juno's succession and personally presides at Rowan's tribunal, where Kaito's Marrowgate testimony cracks the Accord's moral authority if the PC encouraged it.
- **Act IV: the lie exposed.** Bastian, the Gravenmoor echo and Brann reveal the truth about the Fracture and the Tuning. Valen does not deny it. He says only: "Win your last two badges. Then come to me, and I'll tell you everything."
- **Act V: confession and sacrifice.** Valen confesses (Ch20), fights the PC in the Final, and dies holding the Concordance Ring during the Arceus battle. What becomes of the Accord afterward depends on the ending: dissolved, reformed into a council of equals, or continued under a new Crown.

### Accord Standing: what it unlocks (story side)
- **High:** the Accord Archive branch, early access to Brann's confession in Act IV, and Valen's audience in Ch20 is longer and gentler. Sigrun's trial is shorter.
- **Low:** the Wardguard won't escort the PC to Crownhaven, so the PC must take the smugglers' route over the Glassfall Scar. Valen's audience is colder. The Borrowed Crown ending is harder to reach.

---

## THE KINGDOMS AS PLAYERS (act-by-act moves)

| Kingdom | Act I | Act II | Act III | Act IV | Act V |
|---|---|---|---|---|---|
| **Elowen** (Queen Maelis, Prince Caedmon) | Coins, banners, the Royal Chase closed | Tax-barges turned back at Saltmere | **Claims the Meadow Plate** after Rowan's arrest, and the Thornguard occupies the Heartgarden. Opens the Royal Chase as a PR gesture | Signs the **Forest Compact** with Meridian (Caedmon's doing). The Lantern Theatre stays shut | Thornguard checkpoints at Gloaming. Maelis, sidelined by her son, quietly helps the PC (optional scene) |
| **Isenmar** (Thane Eirik) | Ebbmouth strike brewing over Thane taxes and Meridian layoffs | — | **The Thaw.** Martial law, refugees south. Anja breaks with Meridian | Refugees in Cragholm and Briarwick | Eirik attends the Festival begging for debt relief |
| **Zenith** (Voss's Council) | The Gala | Mandate checkpoints | Curfews. The Larch smear | The Sump Purge. Sallow's quiet opposition | Hosts the Festival, then the hijack |
| **Nadir** (Sump Barons, Nyx) | — | Pits, Sweetrot, Hollow recruiting. The Conclave attack | Mandate raids | **The Sump Purge. Nadir declares independence** | Its fighters come up the lifts to Crownhaven |
| **Ashkaar** (Dominar Hrothgar) | Rumors | **Caldera crisis.** Demands the Light Stone and threatens war on Zenith | Legions muster | Raids on Meridian convoys | Legions at Wyrmrest. Either march on Zenith or fly for Crownhaven (`DOMINAR_SWAYED`) |
| **Ossaria** (Prince-Elector Kassan) | — | Sells drilling rights, and the Duneholt aquifer collapses | — | Sells Cragholm's seams. Meridian raid. Groudon wakes | Kassan arrested in the epilogue (Good ending) or knighted by Meridian (Bad) |
| **Antumbra** (Veiled Synod) | — | — | The PC crosses the Glass. Dask warns of the thinning | Giratina wakes in the Reverse Depths | Keeps the Veil Gate sealed ("a wall that's falling down"). The Glass leaks anyway (cameo sidequests). Ruin Route: Dask claims the Renegade |
