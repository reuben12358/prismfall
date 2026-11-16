# Story Bible 13: Cutscene Storyboards (SPINE Revision 6)

> Shot-by-shot storyboards for the `Prismfall Cutscenes` plugin (DSL spec: `design/CUTSCENES.md` when it lands). Each shot lists **camera**, **sprites/action**, **FX**, **text**. Durations are suggestions at 60 FPS feel. Sprites are battle/overworld Pokémon and trainer sprites; no new painted art is assumed except the listed backdrops.
> Variants are selected by narrative keys (NARRATIVE_KEYS). Proposed keys are marked *(proposed)*.

---

## WAR-1 — "The Beam Clash on the Shattered Ice" (Ch19 climax; ~95 s)

**Backdrop:** the Shattered Ice (broken sea-ice plates, black water between; Skaldfast's walls left, Cinder Cape Warfort right; dawn). **Variants** (NARRATIVE_KEYS §4.3): A = `WAR_STOPPED`, A′ = `WAR_BOTH_BROKEN` (shots 1–10 as A; then shot 11 is a white-out, shot 12 is cut, and shot 13 shows both lines gone and the two rulers alone on the glass), B = `WAR_ASHKAAR_WON`, C = `WAR_ISENMAR_WON`. If `:war_legend` kept the legendaries away, shots 2–5 use Sigrun's Salamence (Draco Meteor, then Flamethrower) against Anja's Mamoswine or Marisol's Gyarados (Blizzard / Hydro Pump); the clash in shot 6 is unchanged.

| # | Camera | Action | FX | Text |
|---|---|---|---|---|
| 1 | Wide, slow pan left→right across both hosts (4 s) | Isenmar: sled-ships, Walrein and Mamoswine ranks, Thane Eirik on the lead prow. Ashkaar: riders on Salamence/Charizard in a sky column, the Dominar on the Warfort wall | Snow overlay left, ember overlay right; they meet mid-screen | — |
| 2 | Cut: low angle on the black water (2 s) | The water bulges. **Kyogre** rises, Primal markings lit | Rain starts; screen tint blue; rumble | Eirik: "Isenmar! The sea remembers it's a sea!" |
| 3 | Cut: the Warfort wall (2 s) | The Dominar lifts the **Light Stone**. It cracks white. **Reshiram** unfolds above him | White flash; heat-haze shader; tint orange on the right half | Hrothgar: "Then let it remember fire." |
| 4 | Split screen, vertical seam (2 s) | Left: Kyogre's mouth gathers a blue sphere. Right: Reshiram's tail-turbine ignites blue-white | Charge particles pull inward on both sides; rising whine | — |
| 5 | Wide (1.5 s) | Both fire. **Origin Pulse** (blue-white beam, left) and **Blue Flare** (white-blue fire beam, right) cross the ice | Beam sprites extend 12 frames each | — |
| 6 | Center, hard zoom on the meeting point (3 s) | **BEAM CLASH.** The beams lock. The clash point shudders left, then right, then holds | Clash-ball sprite, pulsing; screen shake 6 px; white strobe every 8 frames; ice plates crack outward in a ring | — |
| 7 | Cut: ice surface (2 s) | Soldiers on both sides thrown flat. Ice turns to **steam-glass** in a spreading circle | Steam overlay; glass crackle SFX; `:BLEED` palette shimmer | Soldier: "The Steamline! It's coming this way!" |
| 8 | Pull back, high wide (3 s) | A dome of Bleed light swells from the clash point over both front ranks. Figures at its edge begin to glass | Dome sprite scales up; color bleed to prismatic | — |
| 9A | Track right, ground level (4 s) | **The PC walks into the dome**, alone, toward the clash. Their starter beside them | PC's chest glows colorless; dome dims in a circle around them | *(no text; footsteps only)* |
| 9B/9C | Track with the PC's mount/boat (4 s) | The PC rides Sigrun's Salamence (B) / stands on Marisol's prow (C) straight at the clash | Same glow | Sigrun (B): "Hold on!" / Marisol (C): "Tides take it, kid, *now*!" |
| 10 | Close on the PC, beams overhead (3 s) | The PC raises a hand. The shard's light goes up into the clash-ball | Colorless ring expands; both beams desaturate to white | — |
| 11 | Center (3 s) | The clash-ball **goes silent** and collapses into a single falling mote. Both beams gutter out | All FX cut to silence; one soft chime; rain turns to snow | — |
| 12 | Two-shot (4 s) | Kyogre and Reshiram both look down at the PC. Hold. Kyogre sinks. Reshiram banks away | Water ripple; wingbeat wind | Field Notes pop-up: "It looked at me as if I were very small and very familiar. Again." |
| 13A | Wide, the glass between the armies (5 s) | **Sigrun** lands on one side of the PC, **Anja** walks out on the other. They face their own rulers | Snow; no music | Sigrun: "Father. Enough." Anja: "Eirik. Enough." Both: "The Boon will settle it." |
| 13B/C | Wide (5 s) | The losing host breaks. The winner's banners go up over Skaldfast (B) or Cinder Cape (C) | Smoke | Victor: "It's done." Loser's Warden, to the PC: "I'll remember which side you stood on." |
| 14 | Cut: a ridge behind the lines (4 s) | **Meridian observers** in white coats fold a brass tripod and box their dials. One is **Dr. Quent**, humming | Sunburst logo glint | Quent: "Lovely reading. Simply lovely." |
| 15 | Slow fade (3 s) | The steam-glass plain at sunrise, both armies' glassed dead standing in it | — | Larch (radio): "That wasn't a battle to them. That was a *reading*." |

**Skippable:** yes, after first viewing. **Replay:** Dream Mist / theater menu.

---

## Festival highlight cutscenes (companion vs companion)

Offered as "Watch the highlights?" after any NPC-vs-NPC match (~25–35 s each). **Winners and key moments for all twelve companion pairings are data in NARRATIVE_KEYS §6 (`:pair`, `:winner`, `:moments`).** The four below are the fully storyboarded ones; the other eight use the generic three-shot template (entrance, key moment, result) with the listed moments. All on the Temple-Arena backdrop with the active gym field's tint. Outcomes follow the player's choices.

### FH-1 — Juno vs Kestrel (R16 or QF, whenever the bowl pairs Elowen and Zenith)
**Variants:** A = Kestrel Redeemed-track (not `KESTREL_FALLEN`), B = Fallen, C = Juno wins (Kestrel Bond ≥ 5 *and* Juno Bond ≥ 5: he lets himself lose honestly; *(proposed `JUNO_BEATS_KESTREL`)*).

| # | Camera | Action | FX | Text |
|---|---|---|---|---|
| 1 | Wide arena, crowd pan (3 s) | Juno waves at the stands; Kestrel taps two fingers on his sternum | Banner colors: Elowen green, Zenith brass | Announcer: "The Warden of Verdance! The challenger from the lighthouse!" |
| 2 | Close two-shot (3 s) | Tsareena vs Aegislash. Tsareena's Trop Kick; Aegislash drops to Shield | Petal burst; steel clang; `:FLOWER_GARDEN` grows a stage | Juno: "You always go shield first. Since the Sanctuary." |
| 3A | Low angle on Kestrel (3 s) | His Gauntlet lights. He looks at it, then closes his fist and *doesn't use it* | Gauntlet glow dies | Kestrel: "...Not on you." |
| 3B | Low angle on Kestrel (3 s) | The Gauntlet flares. The field cycles under his feet without the arena's cue | Field tint snaps to `:HOLLOW_CATHEDRAL`; crowd gasp | Juno: "Kestrel, your *hand*." |
| 4 | Center (3 s) | Aegislash Blade forme, Sacred Sword through the petals (A/B) — or Tsareena catches the blade on a heel and High Jump Kicks (C) | Slash arc; impact flash; shake 4 px | — |
| 5A | Close (3 s) | Tsareena down. Kestrel offers Juno a hand up. She takes it | — | Juno: "Next time I'm bringing the ogre." |
| 5B | Close (3 s) | Tsareena down hard. Kestrel doesn't look at her. Ogerpon (if present) steps between them | Gauntlet smoke | Juno, quietly: "That wasn't you." |
| 5C | Close (3 s) | Aegislash down. Kestrel laughs, once, surprised | Petals falling | Kestrel: "Huh. Verdance grew teeth." |

### FH-2 — Sigrun vs Valen (default SF; Ashkaar vs the Accord)
| # | Camera | Action | FX | Text |
|---|---|---|---|---|
| 1 | Wide (3 s) | Sigrun in dragonhide, Valen in white, glove off | Crowd hushes; `:DRAGONS_DEN` heat tint | Sigrun: "Yield the Light to me, old man. Spare the child." |
| 2 | Close on Valen (2 s) | He shakes his head | — | Valen: "You'd last ten years. I won't spend you." |
| 3 | Center (3 s) | Salamence Draco Meteor vs Zygarde 50% | Meteor sprites; impact shake | — |
| 4 | Zoom on Valen's arm (3 s) | The crystal creeps to his collarbone as Zygarde's cells gather | Glass crackle; green cell particles converge | Ilsa (stands, if reconciled): "Father, *stop*." |
| 5 | Wide (3 s) | **Zygarde Complete.** Core Enforcer writes a Z across the arena. Salamence falls | Green beam; white flash | — |
| 6 | Two-shot (4 s) | Valen catches himself on one knee. Sigrun stares, furious, then offers her arm. He takes it | — | Sigrun: "You beat me with an arm made of glass." |

### FH-3 — Anja vs Sigrun, "the Truce Match" (R16 or QF; Isenmar vs Ashkaar)
A second, deliberate **beam clash**, this time under rules. **Variants:** A = `WAR_STOPPED`, B = `WAR_ASHKAAR_WON`, C = `WAR_ISENMAR_WON`. (If a kingdom forfeited its second seat, the pairing is Marisol vs Sigrun or Anja vs Brann, with the same shots.) If the Thane or the Dominar replaced a delegate, swap the sprite and lines (Eirik's Walrein / Hrothgar's Charizard).
| # | Camera | Action | FX | Text |
|---|---|---|---|---|
| 1 | Wide, split stands (3 s) | Isenmar furs left, Ashkaar red right. Wardguard line between the blocks | Banners | Hierophant: "Under the Peace of Plates." |
| 2 | Close (2 s) | Mamoswine paws the ice-tinted floor; Salamence circles | `:FROZEN_LAKE` tint; breath fog | Anja: "No sea-beasts today, girl. Just us." |
| 3 | Center (3 s) | **Ice Beam vs Flamethrower. Beam clash**, small and clean | Clash-ball; steam plume; shake 3 px | — |
| 4A | Center (3 s) | Both let the beams drop at the same instant. They walk to the middle and clasp forearms. Forfeit by lot | Steam clears | Sigrun: "Flip for it?" Anja: "Toes." |
| 4B | Center (3 s) | Flame wins the clash; Mamoswine down | Fire wash | Anja: "Skaldfast still stands in here." *(taps chest)* |
| 4C | Center (3 s) | Ice wins; Salamence grounded, wing frosted | Frost burst | Sigrun: "Tell your brother that's the last thing he takes." |
| 5 | Crowd (3 s) | A: both blocks applaud, awkwardly, together. B/C: one block roars, one sits silent | — | — |

### FH-4 — Nyx vs Rook (or Magnus), "Above and Below" (Nadir vs Zenith, R16)
| # | Camera | Action | FX | Text |
|---|---|---|---|---|
| 1 | Wide (3 s) | Nadir's first delegation ever. Sumpborn in the cheap seats on their feet | `:NEW_MOON` darkness falls over half the arena; `:NEON_GRID` glow on the other | Nyx: "Sixteen unknown, darlings. Learn the name." |
| 2 | Close (3 s) | Rook's Rotom drone films; Toxtricity riffs. Nyx's "Honchkrow" lands a hit that makes no sense | Neon bolts; a glitch-flicker on the Honchkrow | Rook: "Chat, that bird just used Night Daze." |
| 3 | Center (3 s) | The illusion breaks: it was **Zoroark**. Rook laughs out loud | Illusion-shatter FX | Rook (if fired in Ch16, replace with Magnus: "Deception is a tolerance failure.") |
| 4 | Close on Nyx (3 s) | She looks up at the Meridian box, not at her opponent, and has Zoroark finish it | Dark pulse; lights out | Nyx: "That one was for the Sump." |
| 5 | Crowd (3 s) | The cheap seats explode. A Directorate officer starts toward them; **Kaito** (or Corvin) stands up, and the officer sits back down | — | — |
| Variant | — | If `:ch17_nyx` = refuse, Nyx is still injured from the Purge and **loses**; shot 4 becomes Rook lowering Toxtricity's guitar and refusing the last hit until she yields | — | Rook: "Not filming this bit." |

---

## Renames / adoptions for the World lead
All World names from WORLD.md §8–9 are **adopted** as given: Pyre Keep (Cindervault), the Palace of Glass (Lucent), Rime Narrows, Skaldfast, the Ashkaar Siege Camp, Cinder Cape Warfort, the Steamline, the Shattered Ice, the Temple-Arena of the Blessing, the Court of Eight Pavilions, the Ice Vault. Story-side names that now map onto them:
- "Ember Citadel" (Wyrmrest) and "Mirror Palace" → retired in favor of **Pyre Keep** and the **Palace of Glass**.
- "Meridian Prism Arena" = the Temple-Arena of the Blessing's Meridian-era rebuild name (both are used in dialogue).
- Story still uses: **the Holdfast** (the Thane's fortress in Rimeholt), **Briar Keep** (Verdance), **Sandglass Palace** and **Valley of Tombs** (Duneholt), **Council Spire** (Lumen City), **Moon Court** (Underveil). Please adopt or send replacements.
- Requested small maps: the Dominar's command pavilion (Siege Camp interior); the ridge with Meridian's observers (WAR-1 shot 14).
