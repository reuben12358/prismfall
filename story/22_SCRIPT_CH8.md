# Script: Chapter 8 — "The Light Stone" (scripted scenes)

> **WITHDRAWN (SPINE Revision 21, 2026-11-20):** the Mega Ring now comes after Badge 13, so the Ring-Day below no longer plays in Ch8. The Mega workstream is choosing its new place and giver and will move this scene (`mapgen/REQUESTS.md`). Until then it's kept as written, for them to reuse. Don't build it.

> **Playable script** for Chapter 8's scripted scenes. The chapter itself (the Sulfur Road, Cindervault, Gym 7, the Caldera Crisis, the Light Stone, Brann's chestnut slip, the herald) is still outline in `story/05_ACT_II.md` Ch8, and its comedy scene "The Hug" is in `15_COMEDY.md`. Each scene here is final; if a plugin plays it, the plugin's strings match this file.
> Conventions as in `story/20_SCRIPT_CH0-2.md` (`[portrait: NAME, expression]`, `> option`, `MOVE:`, `WAIT n`, *(emotes)*).
> Sources: 05_ACT_II Ch8, `design/MEGA_EVOLUTION.md` §1 and §4 (SPINE Revision 20), 09_MYSTERIES #1/#4/#5/#6, 03_CAST (Brann, Larch).

---

## Map 244 — Hearthguild Hall, Cindervault: **"The Ring-Day"** (the morning after the Caldera Crisis)

**When:** 7 badges, `:ch8_caldera` made, no Mega Ring yet. It comes after Brann's chestnut slip the night before ("I reset the Crown's stone myself... It was smaller than it should've been") and before the Dominar's herald (the chapter's cliffhanger).
**Plays as:** the hidden Trials quest `AS_RING_DAY` (`plugins/Prismfall Trials/114_Quests_Megas.rb`) on `pf_trial_talk(:BRANN_HEARTHGUILD)`. It gives `MEGARING` and `AGGRONITE`, and closes quietly (no Trial gong).
**What it must not say:** Brann never names the Legend Plate and never says "reset" (09_MYSTERIES #5 and #6 are revealed in Ch15–17). The only clue is the ring: he cut it "ten years back", it sulks on everyone else, and it sings for the PC.

### Nudge (the inn, morning after the crisis; [NEW] map event, see `mapgen/REQUESTS.md`)
```
[portrait: LARCH, deadpan] Brann wants you at the Hall. He's sober. It's unsettling.
```

### EV "Brann" (Hearthguild Hall, at the great anvil)
```
(Morning. Brann is at the guild's great anvil with a folded cloth. Larch sits on a crate by the door with a book she isn't reading.)

[if :ch8_caldera = :vent]
  (The great forge is cold. One small candle-forge burns on the anvil.)
  [portrait: BRANN, sad] Cold for a season, thanks to you lot. Don't make that face, I've had worse winters. A ring wants a candle, not a caldera.
[if :ch8_caldera = :dampers]
  [portrait: BRANN, happy] Hear that? Every forge in the Vault, roaring. You kept 'em lit, and I won't forget it.
[if :ch8_caldera = :shutdown]
  [portrait: BRANN, happy] You shut a Meridian tap with your bare hands. The Dominar hasn't stopped talking about it. Neither have I.

[if :ch8_lightstone = :dominar]  (optional; not in the plugin yet, see the note below)
  [portrait: BRANN, sad] And the Light Stone... no. Not today. Today I'm in a good mood, and I'm keeping it.

[portrait: BRANN, worried] About last night. A fool talks too much over chestnuts. Forget the fool. Forget the chestnuts too. They were burnt.
[portrait: BRANN, neutral] Here's what a sober man says instead. Hold out your hand.
He opens the cloth: a plain gold band, and set in it a chip of stone with no colour at all.
[portrait: BRANN, neutral] A Warden's ring. 'Mega Ring', the Accord calls it. The guild's cut one for every seat since the Concordance. This one's the odd one out. I cut it ten years back, and it's sulked on every hand I've tried it on.
[portrait: BRANN, neutral] The chip's grind off the Crown's own stone. No colour of its own, so it'll take any colour you put to it. That's how it opens a heartstone.
[portrait: BRANN, neutral] Heartstones. 'Mega Stones', if you're Accord. Leave an Imprint in one kind of Pokemon long enough and it pearls. Your partner holds the stone, you wear the ring, and for one fight it carries its whole Imprint.
[portrait: BRANN, deadpan] One heart at a time, mind. Two rings on the same side ring against each other. One Mega to a side, always. Remember it in a double. ...Right. Let's see if it sulks on you.
He drops the ring into your palm. The colourless chip catches the forge-light... and sings: one clear note, like a wet finger round the rim of a glass.
Somewhere under your ribs, something answers it.
(Cutscene RD-1, `13_CUTSCENES.md`: the note, the PC's scar, Brann's face.)
[portrait: BRANN, shocked] ...
[portrait: BRANN, sad] They don't sing. Thirty years at this anvil, and not one of them has ever sung.
(Larch has lowered her book.)
[portrait: BRANN, worried] ...It's the forge-hum. That's a lie, and lying's a crime in Ashkaar, so you never heard it. Here: an iron heart to start you off.
(Received: MEGA RING. Received: AGGRONITE.)
[if the Bag already held another Mega Stone]
  The other stones in your Bag are warm now, and quiet, as if they had stopped waiting.
[portrait: BRANN, happy] Aron burrow under the Brinecut cliffs. Raise one into an Aggron and it'll know what to do. Now go and show Kaito what a ferry child does with a Warden's ring.
```
*Brann, after (idle):* `Brann hums at the anvil, badly, and very loudly.`
*Larch, after (by the door):* `[portrait: LARCH, deadpan] I heard nothing. I'm writing nothing down. *(she is writing it down)*` **[NEW]**

**Notes**
- **Why it sings (for writers, not players):** Brann cut this ring from the grind of the AF 290 reset, the same break the PC's splinter flew from (01_WORLD_LORE §5). "Ten years back" echoes his chestnut line ("After the accident. Ten years back."). The player can put the two together; nobody says it until Ch17.
- **Lying:** "Say true or say nothing" is Ashkaar law (05_ACT_II Ch8). Brann can't keep the secret and can't bring himself to lie, so he does both and owns up. His Act III line ("Your ring still singing? ...No. Don't tell me.") is the same instinct.
- **The Light Stone line** needs one `:if` entry in `AS_RING_DAY` (Trials owner): `choice(:ch8_lightstone) == :dominar`, after the caldera branches. If the PC told him to give the Light Stone to the Dominar, Brann is hurt (his Act V Consent refusal), and the scene shouldn't read as if nothing happened.
- **Follow-ups:** `AS_FORGE_REMEMBERS` (Act III, Cameruptite); Juno's ring in the Heartgarden after J3 (`EL_BRIDE_TREE_HEART`); Kestrel and Morwen's Ring (Ch18/SF; `design/MEGA_EVOLUTION.md` §1).
