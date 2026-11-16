# CAMEOS — Visiting Champions of the Festival (Story lead)

> Replaces the canon-champion roster (SPINE Rev. 2 §3 / Rev. 3 §3). Owner: Story lead. Trainer teams: trainer/balance agent.
> All cameos come from the sister fangames **Pokémon Reborn**, **Pokémon Rejuvenation** and **Pokémon Desolation**.
> Facts marked ✔ were checked against web sources (listed at the bottom). Anything not marked is our own Festival-flavor invention, written in the spirit of the source.
> The **headline cameo** (default Quarterfinal opponent, replacing Cynthia) is **Lin**.

---

## Why champions of other worlds are in Velmora (in-universe)

The Festival of Champions has always been a **festival of other worlds**. When the Prismfall tore Velmora, it opened a seam behind the forests of Elowen: **Antumbra, the Kingdom Behind the Glass**, Giratina's domain. The Glass is a mirror that faces *outward* as well as inward. Since AF 140, the Accord has sent its invitations through Antumbra's **Veil Gate**, and they reach the champions of worlds that already brush against each other: **Reborn**, **Aevium** and **Ayrith**.

These worlds already leak into one another, so the cameos aren't surprised:
- ✔ Desolation's Champion **Shiv** turns up in Reborn's post-game.
- ✔ Reborn's Adrienn and Aya help rebuild Gearen City in Aevium.
- ✔ Aevium's Flora appears in Reborn.

To them, Velmora is just a new door. That is also why the quarantine doesn't stop them: they don't cross the Hallow Strait, they step through the Glass. The Veiled Synod opens the Gate for Festival week only. Giratina allows it, and Ch20 shows its eye in the Gate as each champion passes.

**Rules of the Glass (story constraint, useful for balance):** a traveler can bring only what is *theirs*. Anything bound to their home world's gods stays behind. That is why Lin arrives **without her Arceus**, and it is the single most important thing she says all week.

---

## Roster (7 + 2 extra candidates + 1 Ruin-only)

Trainer type IDs follow `FESTIVAL_<NAME>`. **Suggested version scheme** (trainer agent decides; SPINE difficulty offsets +100/+200 still apply):
- `1` = Round of 16 / exhibition (lv ~90)
- `2` = Quarterfinal (lv ~92)
- `3` = Semifinal or substitute Final-tier draw (lv ~94)
- `9` = post-game rematch (lv 100)

The Festival bracket is choice-driven (Rev. 3). The "default draw" below is the fallback, and the draw rules belong to `story/10_CHOICES_ENDINGS.md`.

### 1. Lin — "the Meteor Champion" (Reborn) — `FESTIVAL_LIN` — ★ HEADLINE / default QF
- ✔ **Source:** Lin (Lindsey Paraeah) is Reborn's hidden Big Bad. She usurped Team Meteor and is fought as Reborn's **Champion**. ✔ Her signature is a **Togekiss carrying an illegal move (Oblivion Wing)**, and ✔ she **caught Arceus**. ✔ TV Tropes describes her as cynical, blunt, mean-spirited and Jekyll-and-Hyde. ✔ Fans know her late-game speech for being written entirely in lowercase.
- **Why she's here:** Voss's people slipped a second letter into her invitation: *"a god in eighteen pieces, waiting to be collected."* He wanted her expertise. She came to see whether someone was about to make her mistake.
- **Why she's the headline:** She is the one person in Velmora who has *already done* what Voss is trying to do. She is a living warning, a dark mirror for both Voss and the PC, and the source of the key outside confirmation for the Return ending (this replaces Cynthia's old lore role).
- **Voice:** Lowercase whenever she's being honest. It's an homage, so the dialogue box should literally render it that way.
  - *(arrival, Ch20)* "your god's in pieces and your champion's made of glass. cute region."
  - *(QF, mid-battle)* "you're carrying it, aren't you. i can hear it. it's so *loud* in you."
  - *(after the QF)* "you want to know what happens when you put a god in a box? it's quiet. for a while. then it isn't. it doesn't want to be held. nothing that big wants to be held. give it back before someone teaches it to hate you."
- **Team spirit:** Reborn endgame. Brutal, coverage-heavy, field-aware.
  - **Ace: Togekiss** (with the Oblivion Wing homage; needs a custom move learn in PBS).
  - The rest should be her "Meteor" heavy hitters, chosen by balance (no Arceus, per the Rules of the Glass). Example concept: Hydreigon, Garchomp, Gardevoir, Ferrothorn, Volcarona.
  - She should feel like the hardest non-story-boss trainer in the game.

### 2. Amaria — "Flotsam Amaria" (Reborn) — `FESTIVAL_AMARIA`
- ✔ **Source:** A late-game Reborn **Water** Gym Leader, famous for her nicknamed team: ✔ **Lapras "Deliverance"** (ace), Starmie "Twinkle", Ludicolo "Indiana", Kingdra "Atlantica". ✔ She rescues the player from a Garchomp, and ✔ her gym is an underwater maze. Her chapter is linked to Titania's (Reborn badges 15–16). She carries a heavy, melancholy history.
- **Why she's here:** Drowned places call to her. She came for the rumor of a city under a city, Aurelia.
- **Velmora hooks:**
  - Bonds with Marisol over working-class water folk.
  - Sits for a long time at the Crownhaven lake.
  - Dorian talks her into voicing **Princess Maren's lament** in the Night of Masques.
- **Voice:** quiet, wry and tired: "Everything sinks eventually. The trick is learning to breathe down there."
- **Team spirit:** Water mono with nicknames intact. **Ace: Lapras "Deliverance."**
- **Default draw:** R16 vs Sigrun (loses). Exhibition available from Day 3.

### 3. Shelly — Champion of Reborn (post-game) (Reborn) — `FESTIVAL_SHELLY`
- ✔ **Source:** Reborn's pink-haired **Bug** Gym Leader, who loves throwing bugs at you in **double battles**. ✔ In Reborn's post-game she has become **Champion** with half her team still partly Bug-type. She insists she is *not* the region's Professor "until her credentials arrive next year."
- **Why she's here:** As a reigning Champion she was formally invited, and she was too polite to say no. She is terrified of crowds.
- **Velmora hooks:** She mentors Tamsin Loom (two shy Bug specialists). In the hijack, she helps Tamsin's silk nets catch falling debris.
- **Voice:** "Oh — um — you don't have to bow, I'm only Champion until somebody better comes along. Which might be you? Sorry."
- **Team spirit:** A Bug core with champion-grade partners. **Her exhibition should be a DOUBLE battle.** Ace concept: Volcarona or Scizor (balance to confirm against her source team).
- **Default draw:** R16 vs Venam (loses). Exhibition from Day 3.

### 4. Alexandra — Acting Champion of Aevium (Rejuvenation) — `FESTIVAL_ALEXANDRA`
- ✔ **Source:** Elite 8 member and **Acting Champion** of Aevium (League ID No. 2), formerly travelling under the aliases April and Krystal. ✔ Her known Pokémon lean Dragon/Psychic: Latias, Dragonite, Altaria, Starmie, Lapras, Sigilyph, Garchomp. ✔ Her mother **Celine**, Aevium's Champion, is **encased in crystal**, in stasis recovering from injuries inflicted by Madame X.
- **Why she's here:** She stands in for her crystal-sealed mother. When she hears Velmora's Bleed turns people to glass, it stops being a tournament for her.
- **Velmora hooks:**
  - She visits Corvin's Quiet Ward and the Lowlight's glass victims.
  - She bonds with Sigrun (Dragon) and with Juno (a fellow inheritor of a seat).
  - Her question, "Can they hear us?", sets up Venam's answer.
- **Voice:** thoughtful and controlled: "My mother has been asleep in crystal for a long time. I'd like to know if yours wake up."
- **Team spirit:** Dragon/Psychic champion team. **Ace: Latias.**
- **Default draw:** R16 vs Celestine (wins), QF vs Valen (loses). Exhibition from Day 5.

### 5. Venam — Poison Gym Leader of East Gearen (Rejuvenation) — `FESTIVAL_VENAM`
- ✔ **Source:** Veronica "Venam" Vasile, 17, a Punk Girl and Aevium's **Poison** Gym Leader (Poison Heart Badge). ✔ She leads East Gearen's teen trainers out of the **Abandoned Sewers**. ✔ Her **ace is Seviper**, and ✔ her signature move is **Venam's Kiss**, a Poison move super-effective against Steel. ✔ Loud, spunky and welcoming. ✔ She was **petrified** and restored by the Spring of Rejuvenation, and came back less sure of herself.
- **Why she's here:** Her invitation came addressed to "the Gym Leader of the sewers". It was meant for someone else, and she came anyway. Nadir feels like home within five minutes.
- **Velmora hooks (important):** Venam is the **only person in Velmora who has been turned to stone and come back.** She tells Juno and Rowan: *"I could hear everything. Everyone who sat with me. Talk to your aunt. She's listening."* This is the outside confirmation that the Fixed still dream, which sets up Xerneas's role in the Good ending.
- **Voice:** "Your City Below's got better graffiti than mine and worse air. Respect."
- **Team spirit:** Punk Poison. **Ace: Seviper** (custom "Venam's Kiss" if the move team wants it, otherwise a high-power Poison move).
- **Default draw:** R16 vs Shelly (wins), QF vs Sigrun (loses). Exhibition from Day 5.

### 6. Shiv — Champion of Ayrith (Desolation) — `FESTIVAL_SHIV`
- ✔ **Source:** The **Champion of Ayrith**. Mysterious, initially shady, ✔ later revealed to be working under Darkrai. ✔ His signature is an **Aipom (→ Ambipom) with far more HP than any Aipom should have**. ✔ He is a trickster. ✔ He has already crossed worlds, as "Dreamer Shiv" in Reborn's post-game Darkrai quest. ✔ He has a twin, Aurora.
- **Why he's here:** He *delivered* the invitations. Dreams leak through the Glass, and Shiv walks dreams. He knows the PC from a dream he had before they ever stepped off the ferry, and it's the creepiest line of Festival week.
- **Voice:** grinning and evasive: "Met you already. You were standing on a ferry, glowing like a lighthouse. No? Must've been a different night."
- **Team spirit:** Trickster tech (Fake Out, Trick, Taunt, weird abilities). **Ace: Ambipom** with an absurd HP stat (custom EVs/IVs, or a balance-approved stat override).
- **Default draw:** R16 vs Kestrel, losing to Kestrel's Resonance Gauntlet. Afterward: *"Your rival's dreaming somebody else's dream."* Exhibition from Day 3.

### 7. Garret — Fighting Gym Leader of Cellia South (Desolation) — `FESTIVAL_GARRET`
- ✔ **Source:** Ayrith's **Fighting** Gym Leader. Gruff, blunt and loyal, and ✔ searching for his kidnapped sister **Eden**. ✔ Signature: **Mega Lucario**.
- **Why he's here:** A big brother looking for a lost sister will go through any door.
- **Velmora hooks:**
  - Mirror match with **Kaito Ren**, Lucario against Lucario: two men who carry what their Lucario remembers.
  - He is the one who notices in the QF that Kestrel's Pokémon "are being driven by something that isn't him."
  - Optional post-game rumor: a girl matching Eden's description seen near the Quiet Towns. This stays a dead end; we never resolve another game's plot.
- **Voice:** "Talk less. Fight more. Then we'll talk."
- **Team spirit:** Fighting with Mega Lucario (if Megas are enabled; otherwise Lucario with an item build).
- **Default draw:** R16 vs Kaito (wins), QF vs Kestrel (loses). Exhibition from Day 5.

---

### Extra candidates (for the choice-driven draw)

#### 8. Melia (Rejuvenation) — `FESTIVAL_MELIA`
- ✔ **Source:** The heart of Rejuvenation. Adoptive daughter of Professor Jenner and a reserve **Normal**-type Gym Leader. ✔ She owns **Hapi, a Togekiss** raised from her treasured Togepi, plus Zoroark, Mimikyu and Snorlax. ✔ She was presumed dead and later infiltrated Blacksteeple Castle under the alias "Emma". ✔ She grew from childlike innocence into someone more cautious and goal-focused. ✔ She is Venam's close friend and ex.
- **Use:** A warm draw for a player with high Bonds who has been kind to the people around them. She comes with Venam.
- **Voice:** "Everyone keeps telling you what you're *for*. Have you decided yet?"
- **Ace:** Togekiss "Hapi". (Lin also uses Togekiss. If both appear in one run, that's a deliberate echo: two Togekiss, two very different women.)

#### 9. Titania (Reborn) — `FESTIVAL_TITANIA`
- ✔ **Source:** Reborn's **Steel** Gym Leader. Her battle is on the **Fairy Tale field** in a sky castle, and her chapter is paired with Amaria's. Her team concept is knightly: Aegislash, Mawile and heavy Steel.
- **Use:** A draw tied to Celestine's Gloaming and the Fairy Tale field. She arrives with Amaria and is fiercely protective of her.
- **Voice:** "I came to guard someone, not to play in your tournament. Fine. En garde."
- **Ace concept:** Aegislash. If Kestrel is in the same bracket, there's a rival-mirror line, sword against sword.

#### 10. (Ruin Route only) Nova (Desolation) — `FESTIVAL_NOVA`
- ✔ **Source:** Leader of **Team Crescent**. An anti-villain who wants a dream world where everyone is happy, manipulative but sincere. ✔ Signature: **Gothitelle**.
- **Use:** Appears **only on the Ruin Route** (see 10_CHOICES_ENDINGS.md), drawn to a PC whose Resonance has tipped to Ruin. She offers to help them unmake the waking world.
- **Voice:** "You could make it so nobody ever has to wake up into this again. I'd help."

---

## Default draw (fallback when no choice rule fires)

| R16 match | Winner | QF | SF | Final |
|---|---|---|---|---|
| PC vs Juno | PC | PC vs **Lin** | PC vs Kestrel | PC vs Valen |
| Lin vs Nyx | Lin | | | |
| Kestrel vs Shiv | Kestrel | Kestrel vs Garret | | |
| Garret vs Kaito | Garret | | | |
| Valen vs Odessa | Valen | Valen vs Alexandra | Valen vs Sigrun | |
| Alexandra vs Celestine | Alexandra | | | |
| Shelly vs Venam | Venam | Sigrun vs Venam | | |
| Amaria vs Sigrun | Sigrun | | | |

**Exhibitions** (optional, Festival week; cameos become available once eliminated):
- Day 3: Shiv, Amaria, Shelly (Shelly's is a double battle).
- Day 5: Garret, Alexandra, Venam.
- **Lin:** post-game rematch only.
- **Melia/Titania:** exhibition-only when not drawn.

## Sources (checked 2026-11-15)
- TV Tropes, *Pokémon Desolation* characters: https://tvtropes.org/pmwiki/pmwiki.php/Characters/PokemonDesolation
- TV Tropes, *Pokémon Reborn* "Others" and "Postgame Characters" tabs: https://tvtropes.org/pmwiki/pmwiki.php/Characters/PokemonRebornOthers · https://tvtropes.org/pmwiki/pmwiki.php/Characters/PokemonRebornPostgameCharacters
- TV Tropes, *Pokémon Rejuvenation* (game page and Past Characters tab): https://tvtropes.org/pmwiki/pmwiki.php/VideoGame/PokemonRejuvenation · https://www.tvtropes.org/pmwiki/pmwiki.php/Characters/PokemonRejuvenationPastCharacters
- Rejuvenation Wiki: https://rejuvenation.wiki.gg/wiki/Venam · /Melia · /Alexandra · /Celine · /Tesla
- Reborn walkthrough (Rebalance mod; teams there are *modded*, used only for identity, field and nickname cross-checks): https://reborn-rebalance-out.pages.dev/walkthroughs/21_titania_amaria · /27_elite_4.html

**Caveat for the trainer agent:** canon source teams vary by game version and route. Treat the aces above as identity anchors and build the rest "in the spirit" of each source, using Velmora's caps.
