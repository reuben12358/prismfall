# Script: Chapter 21 — "Sovereign" (Day 7: the Final, the Coronation, the Hijack, Voss, Arceus, the final decision, the endings)

> **Final playable script** for Chapter 21, the last chapter. Day 7 of the Festival.
> - **Maps:** the Prism Arena (the floor, the Concordance Ring, the stands, the machine-gallery, the Meridian box) and the caldera around it. The ending scenes play across the realm, using maps from every earlier chapter.
> - **Order:** follows `story/39_SCRIPT_CH20.md`. After it come the endings (below) and the post-game.
> - **Sources:**
>   - Story: 08_ACT_V Ch21 and THE ENDINGS (scene text this script stages); **`story/11_FINALE_LINES.md`** (all 36 release and refusal lines, and the Unfinished slides: authoritative, not repeated here); `story/12_RUIN_ROUTE.md` R7 (the Ruin variant); 03_CAST; 09_MYSTERIES (every remaining payoff); 13_CUTSCENES (the hijack and Arceus); 15_COMEDY (none: Ch21 has **no jokes**).
>   - Mechanics: NARRATIVE_KEYS (`:ch21_crown`, `:ch21_hand`, `:ch21_reach_kestrel`, `:ch21_spare_voss`, `:ch21_final`, `GO_HIS_HAND`, §6 the endings matrix and consent, ENGINE_BREAKS, `ENGINE_CALIBRATED`, `KESTREL_LOST`/`BEARS`, `PC_SPARED_VOSS`, `LANTERN_HOLDS`); `Prismfall Core` 008/009 (Festival stages FINAL, HIJACK, ARCEUS) and 018 (endings); `Prismfall Bosses` 103 (`:ARCEUS_FINALE` variants).

## Conventions
As in the earlier scripts. The whole cast is on screen. **There are no jokes anywhere in this chapter**, including the endings' slides, except Edda's last line in Homecoming, which isn't a joke.

**Battles, all through the Festival manager:**
| Battle | How it runs |
|---|---|
| The Final | `Prismfall::Festival.next_match` (stage `:FINAL`, cap 96). Valen, or his successor if `VALEN_COLLAPSED`. |
| The Hijack | `Prismfall::Festival.next_match` (stage `:HIJACK`, cap 100). Voss, Quent if `VOSS_DISCREDITED`, or Theodric on the Ruin Route. |
| The True Finale | `Prismfall::Festival.next_match` (stage `:ARCEUS`, cap 100). The variant comes from `Prismfall::Festival::Draw.arceus_variant`. |
| The tag battle | Outside the stages: `pbRegisterPartner` + `TrainerBattle.start` at the "Ch21 tag foes v21" versions. |

**Counter:** V142 **CH21_STEP** (new; design/FLAGS.md):
| Value | Step |
|---|---|
| 0 | dawn |
| 1 | the Final won |
| 2 | the Coronation (`:ch21_crown`) |
| 3 | the Hijack (`:ch21_hand`) |
| 4 | the allies move |
| 5 | the tag battle |
| 6 | the hijacker beaten (`:ch21_reach_kestrel` between bars) |
| 7 | Arceus descends (`:ch21_spare_voss`) |
| 8 | Valen holds the Ring |
| 9 | the True Finale won (S159) |
| 10 | Valen's death |
| 11 | Arceus speaks (`:ch21_final`) |
| 12 | the ending runs |

**State set here:** S159 CH21_FINALE_DONE; the ending, via `Prismfall.trigger_ending` (018, from `Prismfall::Endings.determine`); and S160 POSTGAME where the ending allows it (018 `apply_postgame_switches`).

## The chapter's key events (design/CHAPTER_BEATS.md)
1. **The Hijack.** The Prism Arena *is* the Arbiter Engine. The cradle rises, the Ring grows golden locks, and Voss descends. "You carried my key through eighteen doors. Let me show you what it opens."
2. **The release.** In the True Finale, eighteen Wardens choose, between bars, whether to let their Plate go. Valen holds the Ring and dies into light. Then the PC speaks the last authored line of the game (`:ch21_final`).

---

# CHAPTER 21 — "Sovereign"

**Chapter start:** V102 = 21, V142 = 0. `Script: Prismfall::Festival::Draw.set_day(7)`

## Dawn (autorun, the PC's room → the arena, V142 == 0)
```
(Dawn. The arena. Every seat full, and everyone you've ever met is in it somewhere: Wardens in the Wardens' box, the kings in the gallery, Pip on Bastian's knee, Tamsin under her banners, Edda at the rail with a betting slip.)
[portrait: LARCH, neutral] (at the players' tunnel, her board of eleven lamps under her arm, all dark) One thing. Don't let him make you a part. He's very good at parts.
[portrait: LARCH, sad] (a beat) And win. I'd like to see you win. I've never seen anyone I love win anything.
```
*(Larch's warning foreshadows `GO_HIS_HAND`.)*

## The Final (V142 == 0 → 1)
```
[if !VALEN_COLLAPSED]
  (Valen, in the arena's centre. No glove at all now. The crystal has reached his collarbone.)
  [portrait: VALEN, neutral] Come on, then. Show me there's another door.
[if VALEN_COLLAPSED && bond(:SIGRUN) >= 5]
  (Valen on a stretcher at the Ring's edge. In the centre, in dragonhide: Sigrun.)
  [portrait: SIGRUN, neutral] He beat me with an arm made of glass. Now he can't stand. So it's me.
[if VALEN_COLLAPSED && else]
  (Valen on a stretcher at the Ring's edge. In the centre, a big man, crying openly, with a Camerupt: Brann.)
  [portrait: BRANN, sad] He asked me to. Last thing he asked.
Script: Prismfall::Festival.next_match   # :FINAL, :PRISM_ARENA cycling, cap 96
```
- **Each time the field cycles** (a battle hook, Valen only): his crystal visibly spreads from shoulder to throat, shown as a sprite overlay plus a line: "The crystal climbs Valen's throat..."
- **Zygarde on its last bar** (Complete Forme): "Order, not justice. I chose order." `[bubble: VALEN, sad]`

*(The Zygarde Complete bar is in TODO_QUOTA §2. Until it lands, Zygarde fights as a normal ace.)*
```
(WIN:)
[portrait: VALEN, happy] (on one knee, smiling, breathing hard) Velmora has a new champion.
V142 = 1.
```

## The Coronation (autorun, V142 == 1 → 2)
```
(Valen lifts the Crown from his head. It's cracked; you can see light through the crack. He walks to you at the arena's heart, inside the Concordance Ring. The Choir sings. Forty thousand people on their feet.)
[portrait: VALEN, neutral] (very quietly, for you) I'm sorry. Hold still.
> Kneel. (kneel)
  Script: pf_choose(:ch21_crown, :kneel)
> Stand. (stand)
  Script: pf_choose(:ch21_crown, :stand)
> Step back. (step_back)
  Script: pf_choose(:ch21_crown, :step_back)
(He raises the Crown over your head.)
(The eighteen Plates in the Ring *scream*.)
V142 = 2.
```

## The Hijack (autorun, V142 == 2 → 3; key event 1)
**Cutscene: the hijack** (13_CUTSCENES). Stage directions are animations, per the `[anim]` rule.
```
[anim: the arena's eighteen-sided rings ignite gold, ring after ring, from the rim inward; the floor at the Ring's centre splits]
(The arena wakes. Its rings blaze gold. Out of the floor at the Ring's centre, a golden hand rises, open, palm up, the size of a door: the cradle from Aurelia.)
(The Ring's pylons sprout golden locks. Eighteen. The Gilded Chain.)
(The Crown is torn out of Valen's hand and slams into the cradle's palm. You're pulled after it by your own chest, the shard dragging you to your knees at the golden hand.)
(Down from the Meridian box, in an Engine-harness of brass and Lattice-glass, a gold sunburst pin on his lapel, calm, almost apologetic:)
[if !VOSS_DISCREDITED && !ruin_route]
  [portrait: VOSS, neutral] You carried my key through eighteen doors. Let me show you what it opens.
[if VOSS_DISCREDITED]
  (Not Voss. Doctor Quent, in Voss's harness, giggling. In the gallery, Voss on his feet, white-faced, watching his own machine in someone else's hands.)
  [portrait: QUENT, happy] Oh, the *readings*. Oh, he never let me drive.
[if ruin_route]
  → 12_RUIN_ROUTE R7 (Theodric, the Gilded Reflection).
```
**His hand:**
```
[portrait: VOSS, neutral] (holding out his hand) Stand up. Stand with me. It doesn't have to hurt.
[if VOSS_ACCEPTED]
  > Take it. (take)
    Script: pf_choose(:ch21_hand, :take)
    (You take it. He helps you up. Behind him, the Engine's light steadies, and turns warm.)
    → Concord Dawn. Arceus is never fought. Script: Prismfall.trigger_ending(:END_CONCORD_DAWN)
  > Refuse. (refuse)
    Script: pf_choose(:ch21_hand, :refuse)
    [portrait: VOSS, sad] (genuinely hurt) You promised.
[else]
  > Take it.
    Script: Prismfall.game_over(:GO_HIS_HAND)
  > Don't.
V142 = 3.
```
*(NARRATIVE_KEYS §9 epitaph for `GO_HIS_HAND`: "It didn't hurt. That was the cruelest part." Foreshadowing: Kestrel's K7 speech and Celestine's "not chained, not bought".)*

## The allies move (montage, V142 == 3 → 4)
These are Larch's eleven lamps (NS §6.2). Each beat fires only if its condition holds. It plays as a fast montage, one line each; on Larch's board, a lamp lights for each Engine break.

| Condition | Beat |
|---|---|
| `ROOK_CUTS_GRID` | **Rook**, in the broadcast gantry: "First time Lumen's been dark in ten years. Kinda pretty." The Engine flickers. *(lamp)* |
| `NYX_PRECISE` | **Nyx**: a single switch, and Meridian's comms go dead, surgically. *(lamp)* |
| else | **Nyx** goes in with knives and her people. It works, and it's bloody, and she's hurt. *(no lamp)* |
| `MAGNUS_KEPT_FAITH` | **Magnus** in the machine-gallery, a spanner in his steel hand: "No machine I have built will kill a child. Governor's off. Go." *(lamp)* |
| `MARCHETTI_TURNED` | **Marchetti**, on the Directorate channel: "All units, stand down. Not for this. Never for this." *(lamp)* |
| `TELEMETRY_SABOTAGED` | **Larch**: "It's miscalibrated! It's reaching for a shard that isn't where it thinks!" *(lamp)* |
| `:ch20_calla` (shelter / send_back) | **Calla's schematics**: one lamp, or two if she went back. Larch touches the second lamp and says nothing. |
| always | **Sigrun** and her dragons hold the sky against Meridian's *Gilded Hours* airships, with **Reshiram** beside her. `DOMINAR_SWAYED`: the Ashkaar legions fly with her. |
| always | **Marisol's** fleet evacuates Lower Crownhaven across the caldera lake; **Edda** pilots the lead boat. |
| always | **Tamsin's** silk nets catch falling debris over the stands. |
| `LANTERN_HOLDS` | **The Lantern Hollow** guard the pylons against Directorate techs, led by Rowan, or Teo, or Thistle and Wick. |
| always | **Kaito** holds the arena gate. |
| war outcome | **The war's hijack line** (14): if the truce held without a victor, Ashkaar's riders hold the sky and Isenmar's ice-riders hold the lake shore, together. |

```
V142 = 4.
```

## The tag battle (V142 == 4 → 5)
```
[if !KESTREL_FALLEN]
  (Kestrel vaults the barrier onto the cracking floor, Aegislash out. [if he wears Morwen's Ring] The ring on his hand is lit.)
  [portrait: KESTREL, neutral] Nearest. Mum's rule. Move.
  Script: pbRegisterPartner(:RIVAL_KESTREL, "Kestrel", 21)   # the Redeemed partner team, version 21 (TODO_QUOTA §3; 80–82 are his K8 SF teams)
[else]
  (Juno, over the barrier in her Warden's coat, Tsareena out.)
  [portrait: JUNO, angry] Same dock. Same fight. Let's go.
  Script: pbRegisterPartner(:RIVAL_JUNO, "Juno", Prismfall::Rival.version_for(7))   # J7: no Mega (the side's one Mega is the player's)
BATTLE: TrainerBattle.start(<foe A>, <foe B>) — the two of Marchetti / Quent / Kroll who aren't turned, dead or hijacking ("Ch21 tag foes v21"); `:PRISM_ARENA` (cracking).
(LOSE: retry from the montage.)
V142 = 5.
```
*(If Kestrel wears the ring he got after the SF, it first answers him here. But the side has one Mega, and the player's comes first; the partner AI only uses it if the player hasn't.)*

## The hijacker (V142 == 5 → 6)
```
Script: Prismfall::Festival.next_match   # :HIJACK — Voss (or Quent), cap 100, :PRISM_ARENA cycling
```
**Voss's mid-battle lines:**
- "Your mother wilted for ten years because a god dropped its furniture on her."
- "I'm not your enemy. I'm the only adult in this arena who'll say the true thing out loud: *we don't need it*."

**His ace, Silvally (Project NULL), multi-bar:** its type follows the active field as the arena cycles through the eighteen gym fields. *(Silvally's conduit bar is in TODO_QUOTA §2.)*

**Between bars 2 and 3, if `KESTREL_FALLEN`: `:ch21_reach_kestrel`**
```
(The arena floor opens behind Voss. Harnessed into the Engine under it, Gauntlet fused to the cradle's wrist and burning: Kestrel. His eyes are open. He isn't in them.)
[if CAN_REACH_KESTREL]
  > Reach him. (reach)
    Script: pf_choose(:ch21_reach_kestrel, :reach)
    [if :ch12_letter == :keep or :send]
      \pf[PLAYER,neutral] "Keep them small and safe and far. I'll carry the name."
      \pf[PLAYER,neutral] She carried yours. Put it down.
    [else]
      (You hold up her ring. You say his name. Just his name.)
    (He comes back. You see it happen: he's in his eyes again. The Gauntlet goes dark. He tears himself loose.)
> Burn it off. (burn)
  Script: pf_choose(:ch21_reach_kestrel, :burn)
  (Your shard tears the Gauntlet off him by force. He screams. He lives. His arm will be scarred from wrist to shoulder for the rest of his life.)
> Let go. (let_go)
  Script: pf_choose(:ch21_reach_kestrel, :let_go)
  (You turn back to Voss. Behind you the Engine fires through its conduit, and the conduit burns out.)
```
*(NARRATIVE_KEYS: `:reach` KESTREL+3 YSOLDE+2 RES+1; `:burn` KESTREL+1 RES−3; `:let_go` YSOLDE−5 → `KESTREL_LOST`, which leads to The Empty Lighthouse.)*

**On defeat:**
```
[portrait: VOSS, angry] (on his knees, the harness sparking) No. No — it doesn't stop because I lost. That was never the design.
(He drives his harness-spike into the cradle's palm.)
[portrait: VOSS, neutral] Then *I'll* hold it.
V142 = 6.
```

## Arceus descends (autorun, V142 == 6 → 7)
```
[anim: the sky over Crownhaven goes white and opens like an eye; a shape descends through it; the caldera's tone shifts to Bleed-violet; every map tint in the arena area becomes :BLEED]
(The sky opens. Something is dragged down through it: vast, white, a wheel of eighteen empty places around it, gold chains snapping onto it from the eighteen pylons, one lock to each empty place. It's half-bound. It's in agony. It's the shape from your vision.)
(The whole caldera turns to Bleed.)
[portrait: VOSS, shocked] (at the cradle, the spike in his hand, the god's light on his face) It's — it's *beautiful* —
(Arceus turns its head. Judgment gathers in the wheel and falls, straight down, on the harness.)
> Shield him with the shard. (shield)
  Script: pf_choose(:ch21_spare_voss, :shield)
  (You throw yourself between, and the shard in your chest flares, and the Judgment breaks on it like water on a rock. Voss is thrown clear. He doesn't get up. He's alive.)
> Let it judge. (let_judge)
  Script: pf_choose(:ch21_spare_voss, :let_judge)
  (The light falls. When it's gone, there's a bright place on the arena floor where a man was, and the shape of a man in the light, for a moment, reaching up.)
(The Bleed surge rolls outward from the Ring, towards the stands, towards forty thousand people.)
V142 = 7.
```
*(NARRATIVE_KEYS: `:shield` RES+2 → `PC_SPARED_VOSS`, unless he was discredited; `:let_judge` RES−1.)*

## Valen holds the Ring (autorun, V142 == 7 → 8)
```
(Valen walks into the Concordance Ring. He's picked the Crown up from the cradle's palm where it fell when you tore loose. Cracked. He puts it back on.)
[if VALEN_COLLAPSED] (They carry him to the Ring on his stretcher. He stands up anyway.)
(He takes hold of two pylons, one in each hand, the flesh one and the glass one. The surge hits him. He holds it. His crystal blazes white, all the way up.)
[if ILSA_RECONCILED]
  (Ilsa at his back, her earmuffs gone, her hands on his shoulders.)
  [portrait: ILSA, neutral] I've got you. Little owl's got you.
[portrait: VALEN, neutral] (through his teeth, not looking away from the god) Go. Free it. I'll hold the door. I've had thirty years of practice.
V142 = 8.
```

## The True Finale: Arceus (V142 == 8 → 9; key event 2)
```
Script: Prismfall::Festival.next_match   # :ARCEUS, cap 100; :ARCEUS_FINALE, variant by Draw.arceus_variant
```
**Variants** (NS §6.6; `103_Boss_Arceus.rb`):
- **Bound** (default)
- **Miscalibrated** (`TELEMETRY_SABOTAGED`)
- **War** (`resonance <= -6`: the shard *eats* the types instead of freeing them)
- **Gilded** (`ENGINE_CALIBRATED`): the last bar can't be broken, which is **The Gilded Chain**
- **Judgment** (Ruin Route only)

**Six bars, three locks each, in gym order:**
| Bar | Wardens |
|---|---|
| 1 | Dorian · Tamsin · Marisol |
| 2 | Rook · Sahar · Corvin |
| 3 | Brann · Kaito · Juno |
| 4 | Anja · Odessa · Ilsa |
| 5 | Bastian · Ysolde · Magnus |
| 6 | Nyx · Celestine · Sigrun |

The arena shifts to the matching gym field for each lock.

**Between bars**, those three Wardens kneel at their pylons and **release** their Plate, or **refuse**.
- **Every line** (18 releases, 18 refusals, each refusal tied to the choice that caused it) is in **`story/11_FINALE_LINES.md`**. This script doesn't repeat them.
- A refusal makes the next lock **forced**: Arceus gains +1 to every stat stage for that bar.
- Whether each Warden releases is their consent condition (NARRATIVE_KEYS §6.2). It's the same reading the banners showed on Day 1, white or grey.

**At bar 6, Celestine's lock:**
```
[portrait: CELESTINE, neutral] (kneeling at her pylon, singing, as her lock breaks) "— not chained, not broken, not bought, not crowned: given back, as a gift is found."
(The Gloaming choir in the stands picks it up. Then the Prism Choir in the loft. Then the crowd. Forty thousand people singing a song most of them only learned this week.)
```
**Harmony:** at high Harmony the PC's Pokémon are steadied by the shard (a minor buff, systems).
```
Switch S159 CH21_FINALE_DONE = ON. V142 = 9.
```

## Valen's death (autorun as the final lock breaks; all main-route paths except Gilded; V142 == 9 → 10)
```
(The last lock breaks. The Ring goes quiet.)
(Valen is still holding the pylons. His crystal isn't white any more. It isn't glass. It's light.)
[if ILSA_RECONCILED]
  [portrait: VALEN, happy] (to Ilsa, without turning round) Little owl.
[portrait: VALEN, happy] (to you, your name, the only time he ever says it) \PN.
(Then he's gone. Light, where he was. The Crown falls, empty, onto the arena floor, and rolls a little way, and stops.)
V142 = 10.
```
*(On the Gilded variant, Valen doesn't die here: the Engine holds, and he's left kneeling inside the Ring, crystal to the jaw, as the chain closes (The Gilded Chain).)*

## Arceus speaks (autorun, V142 == 10 → 11)
```
(Arceus, freed, stands over the arena: whole, except at its heart, where there's a space the size of a splinter.)
(Something lifts out of your chest. It doesn't hurt. A splinter of no colour at all, bright, hanging in the air between you and the god, beside the Crown's shard. They touch.)
(The Legend Plate is whole, for the first time in three hundred years.)
[if ILSA_RECONCILED]
  (Ilsa, still kneeling where Valen was, her hand up, her eyes closed, gives the god a voice everyone in the arena can hear.)
[name: Arceus] Little light. You have carried me far.
[name: Arceus] You may give my heart back, and the rest of me with it. Or you may keep what was borrowed, and wear it, and hold this land quiet in your two hands for a hundred years.
[name: Arceus] I will not take what is not given. I learned that here.
```
*(The last sentence is the Ruin Route's hint: Arceus is talking about Judgment.)*

**`:ch21_final`** (the last authored line of the game; availability per NS §6.1):
```
> "Go home. Take them with you." (return)                         [always]
  Script: pf_choose(:ch21_final, :return)
  \pf[PLAYER,neutral] Go home. Take them with you.
> "I'll keep them. I'll keep everyone safe." (keep)              [always]
  Script: pf_choose(:ch21_final, :keep)
  \pf[PLAYER,neutral] I'll keep them. I'll keep everyone safe.
> (You hesitate.) (borrowed)                                      [BORROWED_OPEN]
  Script: pf_choose(:ch21_final, :borrowed)
  [if KESTREL_BEARS]
    (Kestrel steps past you into the light, and picks up the empty Crown.)
    [portrait: KESTREL, neutral] Not you. Let me be nearest.
  [else]
    (Sigrun steps past you into the light, and picks up the empty Crown.)
    [portrait: SIGRUN, neutral] Not you. I was relieved once. Never again.
> "Stay. Stay and power the world." (concord)                     [CONCORD_OPEN]
  Script: pf_choose(:ch21_final, :concord)
  \pf[PLAYER,neutral] Stay. Stay and power the world.
> "No. No more gods." (unmake)                                    [UNMAKE_OPEN]
  Script: pf_choose(:ch21_final, :unmake)
  \pf[PLAYER,angry] No. No more gods.
V142 = 11.
```

## The ending (V142 == 11 → 12)
```
Script: Prismfall.trigger_ending   # 018: Prismfall::Endings.determine, from the matrix in NARRATIVE_KEYS §6.3
V142 = 12.
```
The ending scenes are staged from 08_ACT_V's **THE ENDINGS** (the scene text is authoritative there). The engine form, per ending:
| Ending | ID | Staging |
|---|---|---|
| **Homecoming** (Good) | `END_HOMECOMING` | Arceus ascends; light rain over Crownhaven (a weather overlay). **The wakings** are map vignettes: Verdance and the Bride Tree (Elin), the Lowlight (Dex), Mirefen's Quiet Ward, the Glassfall Scar's forty, and Marrowgate's gate (Kaito). Then the PC alone on the arena floor, a Meridian scanner beside them, reading a faint ordinary colour. **Epilogue, "One Year Later" (Fallmorn, AF 301, the Festival of Seasons):** the slides in 08 order, each a still with one line of text. Last: the Ferrow's Landing rail, the first ferry. Edda: "Don't lean on my rail like that, sprog." |
| **Homecoming, Unfinished** | `END_UNFINISHED` | As Homecoming, but one **Last Shatter** slide per refusing Warden's city, in gym order, with lines from `11_FINALE_LINES.md` §3. The scar stays ash-grey if Resonance is below Harmony. |
| **The Empty Lighthouse** | `END_EMPTY_LIGHTHOUSE` | As Homecoming. Then: Hesper's lamp each night; Ysolde keeps the Ghost seat; the PC reading Morwen's letter aloud at Kestrel's grave beside his mother's; and Kestrel's Aegislash, sheathed, on the PC's belt. |
| **The Long Vigil** (Grey: Keep) | `END_LONG_VIGIL` | The PC wears the Crown; Arceus leaves incomplete and sorrowing. Ten years later, at the next Tuning, the first crystal on the PC's hand, with Juno and Kestrel beside them, swearing to find another door. |
| **The Borrowed Crown** | `END_BORROWED_CROWN` | The bearer crystallizing. The PC on the first ferry home. Kestrel's last slide: his hand on the rail, turning to glass, smiling. Sigrun's last line: "Ten years. Maybe twelve. I was relieved once. Never again." |
| **Concord Dawn** | `END_CONCORD_DAWN` | Arceus half-bound by Magnus's governor, powering the realm; the PC on the Zenith Council. The last slide carries Celestine's voice: "Once upon a time a god was kept in a box. It was quiet. For a while." *(Via `:ch21_hand`, the last slide is the PC reading the arena's output on a Council screen.)* |
| **The Hollow Spring** (Unmake) | `END_HOLLOW_SPRING` | One night of fire and glass; Arceus leaves wounded forever. Rowan plants the first seed in plain soil, or Thistle does if he drowned. Juno doesn't speak to them; if Teo lived, he's the one who won't. |
| **The Gilded Chain** (Bad) | `END_GILDED_CHAIN` | Arceus bound in gold above Crownhaven, a second sun; the PC asleep in the cradle, "the Sovereign Who Sleeps", visited by schoolchildren. The last image is the chipped linesman's mug, steaming. *(Quent variant: Quent's novelty mug, and Voss among the parents, looking up.)* No post-game. |
| **The Unmaking / The One Who Came Back** | (Ruin) | `story/12_RUIN_ROUTE.md` R7. |

**Voss in Homecoming:** if `PC_SPARED_VOSS`, he's alive and crippled, and asks to see the sunrise (a slide: Voss in a wheeled chair on the Basilica roof, facing east). Otherwise the bright place on the arena floor, a man who reached for a god.

**Credits → post-game** (S160 per 018). The post-game scope by ending is NS §6.5: full / partial / none.

---

## Map and event needs (Chapter 21)
The Prism Arena (Crownhaven, unbuilt) carries the whole chapter.

**Field and staging**
- The **floor and Concordance Ring**: 18 pylon events (lock overlays; kneeling Warden events between bars).
- The **cradle**: a rising golden-hand event; the PC-pinned pose (a half-kneel charset frame).
- The **Meridian box** and Voss's descent (a harness charset); the **machine-gallery** (Magnus); the **broadcast gantry** (Rook).
- The **stands**: 40 crowd events, singing at bar 6.
- The **Larch lamp board**: an 11-lamp picture overlay, lit by `tally(:ENGINE_BREAKS)`.
- The **allies montage**: one shot per condition, a 2-second cut each (cutscene plugin).

**Arceus and the endings**
- The **caldera Bleed** tint swap; **Arceus** (a large event sprite with a wheel and chains).
- The **Valen** crystal-to-light sequence; the empty Crown rolling.
- **The ending vignettes** reuse earlier chapters' maps: Verdance's Bride Tree, the Lowlight, Mirefen's Quiet Ward, the Glassfall Scar, Marrowgate's gate, the Ferrow's Landing rail, the Gravenmoor barrows, and the Basilica roof. Each is an autorun with tone, weather and NPC swaps keyed to the ending ID.

## Gaps this chapter depends on (TODO_QUOTA §2 and §3)
- Valen's **Zygarde Complete** bar.
- Voss's **Silvally conduit bar**.
- The **Redeemed Kestrel partner** team (Ch21).
- The Ch21 tag-foe versions (v21) for Marchetti, Quent and Kroll exist in PBS.
- The montage and ending vignette staging (cutscene agent).

**Portrait requests (art, to Gemini):** VALEN `happy` (light); ARCEUS (a bust for the speech, or plain text with no portrait); VOSS in harness `shocked`; ILSA without earmuffs.
