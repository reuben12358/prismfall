# Story Bible 13: Cutscene Storyboards (SPINE Revision 6)

> Shot-by-shot storyboards for the `Prismfall Cutscenes` plugin (DSL spec: `design/CUTSCENES.md` when it lands). Each shot lists **camera**, **sprites/action**, **FX**, **text**. Durations are suggestions at 60 FPS feel. Sprites are battle/overworld Pokémon and trainer sprites; no new painted art is assumed except the listed backdrops.
> Variants are selected by narrative keys (NARRATIVE_KEYS). Proposed keys are marked *(proposed)*.

---

## Portrait use (every script; coordinator ruling, 2026-11-20)

The user: "i dont think we need a portrait for every conversation." These rules apply to every script in `story/` and every
map event built from one.
- **Who gets a portrait:** main and named story characters only. That means the rivals and companions (Juno, Kestrel),
  the Wardens (Kaito, Dorian, Tamsin...), the villains (the Mourner, Voss, Sable...) and key NPCs (Larch, Wenna, Coll, Edda,
  Hesper, Rowan, Vesper...).
- **When:** in story scenes, plus the occasional comedy beat where the face is the joke. A line with an emote such as
  *(shock lines)* or *(sweat drop)* keeps its portrait.
- **Never:** generic NPCs, townsfolk, shopkeepers, route and gym trainers, guards, signs and objects. They get a plain text
  box, with a name box if it helps: `[name: Gym Guide] ...`.
- **Not on every line.** A speaker's portrait goes on their first line in a scene and on any line where their expression
  changes. Their other lines use the name box only: `[name: Juno] ...`. A new scene starts fresh: a new event, an
  `[after X]` variant, or a choice branch.
- **Notation:** `[portrait: NAME, expression]` = face and name box · `[name: X]` = name box only · no tag = narration.
  Map events use `\pf[NAME,expr]` only where the script has a portrait tag.

---

## WAR-1 — "The Beam Clash on the Glass Dunes" (Ch19 climax; ~95 s)

**Staging:** on map 926, the Glass Dunes, with `on_map: true` (the way `013_Scenes_War_OnMap.rb` stages it), or on a stage picture exported from that map until it is built. The legendaries are **overworld-scale acting sheets** in the map's 3/4 view (design/CUTSCENES.md §4), never battle sprites: Primal Kyogre is as long as a rank of soldiers, and Reshiram's wings cover the Siege Camp's earthwork. The armies are charset blocks under banners. Isenmar and Kyogre are on the left (west), Ashkaar and Reshiram on the right (east).

**Backdrop:** the Glass Dunes at dawn. Bone-white dunes under a low sky; the grey line of the Northern Sea along the far (top) edge; the Steamline's wall of steam between the hosts at the top. Far left (west), Skaldfast's rime-white walls at the foot of the Mast Glacier, with the white trench-lines of the Rimed Sands in front of them. Right (east), the Siege Camp's palisade, red banners and dragon pickets. Between the hosts, on a dune crest, the bone-carters' small white banner. Cinder Cape is out of sight, behind the Ashkaar lines.

**Variants** (NARRATIVE_KEYS §4.3): A = `WAR_STOPPED`, A′ = `WAR_BOTH_BROKEN` (shots 1–10 as A; then shot 11 is a white-out, shot 12 is cut, and shot 13 shows both lines gone and the two rulers alone on the glass), B = `WAR_ASHKAAR_WON`, C = `WAR_ISENMAR_WON`. **No-legend variant:** if `:war_legend` = `:neither` (the only value that keeps the legendaries away; the plugin's `legends: false` is right), there is no flood-sea. Shots 2–5 use Sigrun's Salamence (Draco Meteor, then Flamethrower) against Anja's Mamoswine, which bursts up out of the Rimed Sands' frozen trench-line, or Marisol's Gyarados, which rises out of the trench-lines' meltwater (Blizzard / Hydro Pump). The clash in shot 6 is unchanged, and in shot 7 the glass comes from frost meeting fire.

| # | Camera | Action | FX | Text |
|---|---|---|---|---|
| 1 | Wide, slow pan left→right across both hosts (4 s) | Isenmar: ice-sledges on frozen sand, Walrein and Mamoswine ranks in the Rimed Sands' trench-lines, Thane Eirik on the lead sledge. The bone-carters' banner on its crest, the carters stopped dead beside it. Ashkaar: riders on Salamence/Charizard in a sky column, the Dominar on the Siege Camp's earthwork | Snow overlay left, ember overlay right; blowing sand where they meet mid-screen | — |
| 2 | Cut: low angle on the sand (3 s) | A rumble from the north. The sea on the horizon stands up. **Kyogre's flood-sea** pours in over the dunes and fills the hollows between them. The water bulges. **Kyogre** rises out of it, Primal markings lit | Rain starts; screen tint blue; rumble; flood-front sheet rolling over sand | Eirik: "Isenmar! The sea has come to the sand!" |
| 3 | Cut: the Siege Camp's earthwork (2 s) | The Dominar lifts the **Light Stone**. It cracks white. **Reshiram** unfolds above him | White flash; heat-haze; tint orange on the right half; the rain hisses to steam over the camp | Hrothgar: "Then let it remember fire." |
| 4 | Split screen, vertical seam (2 s) | Left: Kyogre's mouth gathers a blue sphere, and the flood rises in a wave behind it. Right: Reshiram's tail-turbine ignites blue-white, and the sand under it starts to glow | Charge particles pull inward on both sides; rising whine | — |
| 5 | Wide (1.5 s) | Both fire. **Origin Pulse** (blue-white beam, left) and **Blue Flare** (white-blue fire beam, right) cross the flooded dunes. The wet sand under Blue Flare glasses in a bright trail | Beam sprites extend 12 frames each; glass-trail sheet under the fire beam | — |
| 6 | Center, hard zoom on the meeting point (3 s) | **BEAM CLASH** over the waterline. The beams lock. The clash point shudders left as the flood pushes in, then right as the glass pushes back, then holds | Clash-ball sprite, pulsing; screen shake 6 px; white strobe every 8 frames; wet sand glasses outward in a ring | — |
| 7 | Cut: the dune surface (2 s) | Soldiers on both sides thrown flat. Sand and flood-water turn to **steam-glass** in a spreading circle; a breaking wave sets into glass mid-curl | Steam overlay; glass crackle SFX; `:BLEED` palette shimmer | Soldier: "The Steamline! It's coming this way!" |
| 8 | Pull back, high wide (3 s) | A dome of Bleed light swells from the clash point over both front ranks. Figures at its edge begin to glass. On its crest the bone-carters' white banner glasses where it stands | Dome sprite scales up; color bleed to prismatic | — |
| 9A | Track right, ground level (4 s) | **The PC walks into the dome**, alone, across the glassing sand toward the clash. Their starter beside them | PC's chest glows colorless; dome dims in a circle around them | *(no text; footsteps crunching on glass)* |
| 9B/9C | Track with the PC's mount/boat (4 s) | The PC rides Sigrun's Salamence (B) / stands on the prow of Marisol's sled-boat, riding the flood in (C), straight at the clash | Same glow | Sigrun (B): "Hold on!" / Marisol (C): "Tides take it, kid, *now*!" |
| 10 | Close on the PC, beams overhead (3 s) | The PC raises a hand. The shard's light goes up into the clash-ball | Colorless ring expands; both beams desaturate to white | — |
| 11 | Center (3 s) | The clash-ball **goes silent** and collapses into a single falling mote. Both beams gutter out | All FX cut to silence; one soft chime; the rain turns to snow and falls on glass | — |
| 12 | Two-shot (4 s) | Kyogre and Reshiram both look down at the PC. Hold. Kyogre sinks into its flood, and the flood goes out with it, back over the dunes to the sea. Reshiram banks away | Water draining back over the sand; wingbeat wind | Field Notes pop-up: "It looked at me as if I were very small and very familiar. Again." |
| 13A | Wide, the glass between the armies (5 s) | **Sigrun** lands on one side of the PC, **Anja** walks out on the other. They face their own rulers | Snow; no music | Sigrun: "Father. Enough." Anja: "Eirik. Enough." Both: "The Boon will settle it." |
| 13B/C | Wide (5 s) | The losing host breaks, Isenmar back behind Skaldfast's walls (B) or Ashkaar back over the Siege Camp's earthwork (C). The winner's banners go up over Skaldfast (B) or over the Siege Camp (C) | Smoke | Victor: "It's done." Loser's Warden, to the PC: "I'll remember which side you stood on." |
| 14 | Cut: a sandstone mesa behind the lines (4 s) | **Meridian observers** in white coats fold a brass tripod and box their dials. One is **Dr. Quent**, humming | Sunburst logo glint | Quent: "Lovely reading. Simply lovely." |
| 15 | Slow fade (3 s) | The Glass Dunes at sunrise: steam-glass where the sand was, the flood's last wave standing in it as glass, both armies' glassed dead upright. At the edge the bone-carters raise a new white banner and walk out onto the glass | — | Larch (radio): "That wasn't a battle to them. That was a *reading*." |

**Skippable:** yes, after first viewing. **Replay:** Dream Mist / theater menu.

---

## RD-1 — "The Ring Sings" (Ch8, the Ring-Day; ~8 s)

> **Withdrawn from Ch8 (SPINE Revision 21):** the Mega Ring now comes after Badge 13. The shots still work wherever the Mega workstream moves the scene; change the backdrop to suit.

**Staging:** on map 244, the Hearthguild Hall, `on_map: true`, in the middle of the Ring-Day dialogue (`story/22_SCRIPT_CH8.md`, after "Somewhere under your ribs, something answers it"). It's small on purpose: no beams, no music sting. Its job is to be remembered when the cradle sings in Ch17 (09_MYSTERIES #1).
**Backdrop:** the guild's great anvil, forge-light (or, after `:ch8_caldera` = *vent*, one candle-forge and a cold hearth). Brann at the anvil, the PC facing him, Larch on a crate by the door.

| # | Camera | Sprites / action | FX | Text |
|---|---|---|---|---|
| 1 | Close on the PC's open hand (1.5 s) | The gold ring drops into the palm and settles | Forge-light flicker on the band | — |
| 2 | Extreme close on the chip (2 s) | The colourless chip catches the light and breaks it into eighteen thin colours, then gathers them back to clear | Prism fan, 18 hues, 20 frames out and 20 back; SE: one sustained glass note | — |
| 3 | Mid on the PC (2 s) | The PC's hand goes to their sternum | One colourless star-pulse under the coat (the scar, 03_CAST), 1 frame bright, 30 frames fade; the room desaturates 30% and back | — |
| 4 | Two-shot, Brann and Larch (2.5 s) | Brann's hammer hand stops mid-air. By the door, Larch lowers her book | The glass note fades under the forge's roar (or under silence, after *vent*) | — (dialogue resumes: `[portrait: BRANN, shocked] ...`) |

**Variant:** none by key; only the backdrop follows `:ch8_caldera`. **Skippable:** no (8 s). **Replay:** theater menu.

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
All World names from WORLD.md §8–9 are **adopted** as given: Pyre Keep (Cindervault), the Palace of Glass (Lucent), the Rimed Sands, Skaldfast (Outer Walls, Rime Keep, Great Hall), the Ashkaar Siege Camp, Cinder Cape Warfort, the Steamline, the Glass Dunes, the Dry Tide, the Temple-Arena of the Blessing, the Court of Eight Pavilions, the Ice Vault. Story-side names that now map onto them:
- "Ember Citadel" (Wyrmrest) and "Mirror Palace" → retired in favor of **Pyre Keep** and the **Palace of Glass**.
- "Meridian Prism Arena" = the Temple-Arena of the Blessing's Meridian-era rebuild name (both are used in dialogue).
- Story still uses: **the Holdfast** (the Thane's fortress in Rimeholt), **Briar Keep** (Verdance), **Sandglass Palace** and **Valley of Tombs** (Duneholt), **Council Spire** (Lumen City), **Moon Court** (Underveil). Please adopt or send replacements.
- Requested small maps: the Dominar's command pavilion (Siege Camp interior); the sandstone mesa with Meridian's observers (WAR-1 shot 14); the bone-carters' camp on the Dry Tide (810), where Sigrun sets the PC down.
- Story-side names with no map of their own: **the Elector's Lease** (Kassan's lease of the western dunes) and **the bone-carters** (Ossaria's burial guild), both in 14_WAR_AND_BLESSING Part B.
