# CAMEOS — Sister-Game Sidequests (Story lead; SPINE Revision 4)

> The Reborn / Rejuvenation / Desolation cameos are **optional sidequests**, the way Rejuvenation features Reborn's Aya and Adrienn: a small quest somewhere in the world, usually ending in **one tough optional fight**. They are **never** in the Festival, never required, never in the finale. The Festival uses original entrants (03_CAST "Festival Outsiders"; 10_CHOICES_ENDINGS §3). The old Festival default draw in earlier drafts of this file is **obsolete**.
> Trainer type IDs keep the SPINE cameo convention `FESTIVAL_<NAME>`. Versions: **`1`** = the sidequest fight, **`2`** = post-game rematch at level 100 (unless noted). SPINE difficulty offsets (+100 Hard, +200 Casual) apply.
> Facts marked ✔ were checked against web sources (bottom). The rest is our own invention, in the spirit of the source game. Rulings: **Lin's Togekiss keeps Oblivion Wing**; **Amaria's Lapras is "Deliverer"**.

## Why they're in Velmora (in-universe)
Antumbra, the Kingdom Behind the Glass, is the reverse side of the world. Its Glass faces outward too, onto other worlds that already brush against each other:
- ✔ Desolation's Shiv appears in Reborn's post-game.
- ✔ Reborn's Adrienn and Aya help rebuild Aevium.

The Festival once invited champions through Antumbra's **Veil Gate**, but the Synod sealed it in AF 230. Since the Bleed accelerated (AF 289) and above all since the Fault (end of Act III), the Glass has been **leaking**. Travelers from Reborn, Aevium and Ayrith slip through mirrors, puddles, sewer-grates and dreams, and wake up somewhere in Velmora. Each one needs a way home, and the PC, who can walk through Bleed Veils, is the one who can find the right mirror. **Rule of the Glass:** a traveler can bring only what is theirs. Anything bound to their home world's gods stays behind.

## Placement overview (one or two per act before post-game)

| # | Cameo (source) | Act / Ch | Kingdom, area | Unlock | Fight (lv) | ID / version |
|---|---|---|---|---|---|---|
| 1 | Shelly (Reborn) | I / Ch3 | Elowen, Gossamer Deepwood | after Gym 2 | double, ~21 | `FESTIVAL_SHELLY` 1 (2 = PG) |
| 2 | Venam (Rejuvenation) | II / Ch7 | Nadir, Miasma Caverns under Mirefen | after Gym 6 and J2 | ~38 | `FESTIVAL_VENAM` 1 (2) |
| 3 | Garret (Desolation) | II / Ch9 | Nadir, Ironreach's lower shafts | after the Conclave (Gym 8) | ~46 | `FESTIVAL_GARRET` 1 (2) |
| 4 | Melia (Rejuvenation) | III / Ch10 | Elowen, the Royal Chase | after J3 (Gym 9) | ~50 | `FESTIVAL_MELIA` 1 (2) |
| 5 | Alexandra (Rejuvenation) | III / Ch11 | Isenmar, Rimeholt's sunken lower town | after the Thaw and Gym 10 | ~56 | `FESTIVAL_ALEXANDRA` 1 (2) |
| 6 | Amaria + Titania (Reborn) | IV / Ch17 | Nadir, drowned Aurelia's lower galleries | after Gym 16, Dive | double, ~78 | `FESTIVAL_AMARIA` 1, `FESTIVAL_TITANIA` 1 (2) |
| 7 | Shiv (Desolation) | V / Ch18 | Elowen, Gloaming's dusk-chapels | after Gym 17 | ~84 | `FESTIVAL_SHIV` 1 (2) |
| 8 | Lin (Reborn) | Post-game | Ferrow's Landing lighthouse, then the Antumbra Distortion Core antechamber | any ending with a post-game | **superboss, 100** | `FESTIVAL_LIN` 1 |
| 9 | Nova (Desolation) | Ruin Route only | Mirrorwalk dream-road (R5) | Ruin Route | ~90 | `FESTIVAL_NOVA` 1 |

---

## 1. "Lost in the Gossamer" — Shelly (Reborn)
- **Source ✔:** Reborn's pink-haired **Bug** Gym Leader, who loves throwing bugs at you in **double battles**. ✔ In Reborn's post-game she becomes **Champion**, and insists she isn't the region's Professor "until her credentials arrive next year".
- **Where/when:** Act I, Ch3, Gossamer Deepwood (`:SILKWOOD`), after Gym 2 (Tamsin's badge and Cut). It's the first cameo and teaches players that the Glass leaks.
- **Premise:**
  - Silk-moth weavers report "a girl who keeps apologizing to the Bugs" deep in the wood.
  - Shelly fell through a dew-pond's reflection and has spent three days lost, because the Silkwood keeps re-weaving the paths.
  - She's terrified of crowds, so Briarwick's busy looms scare her more than the wood does.
  - The PC finds her, walks her through a small Bleed Veil to the dew-pond she came through, and helps her calm a Bleed-glassed Masquerain guarding it.
  - Before she steps back through, she asks for "one practice battle, so I'm not rusty when I get home".
- **Fight:** **double battle**, lv ~21 (after Gym 2 since SPINE Rev 14 swapped Saltmere and Briarwick; trainer data `[FESTIVAL_SHELLY,Shelly,1]`), on `:SILKWOOD`. Bug core with a partner, so it's tough for its placement.
- **Reward:** **Silver Powder** and a TM (Struggle Bug). Lore: "Your forest sounds like home used to, before the city got sick."
- **Post-game (v2):** she comes back through the same pond, at lv 100 in doubles.

## 2. "Sewer Royalty" — Venam (Rejuvenation)
- **Source ✔:** Veronica "Venam" Vasile, 17, a Punk Girl and Aevium's **Poison** Gym Leader (Poison Heart Badge).
  - ✔ She leads East Gearen's teen trainers out of the **Abandoned Sewers**.
  - ✔ **Ace: Seviper**, and ✔ her signature move is **Venam's Kiss** (a Poison move super-effective against Steel).
  - ✔ She was **petrified** and restored by the Spring of Rejuvenation.
- **Where/when:** Act II, Ch7, the **Miasma Caverns** runoff tunnels under Mirefen (`:CORROSIVE_MIRE`), after Gym 6 and J2.
- **Premise:**
  - Wenlow mentions "a loud girl with a snake" helping drag Sweetrot addicts to the Infirmary from the deep tunnels. She fell through a sewer-grate's reflection.
  - Venam loves Nadir within five minutes ("better graffiti than mine, worse air") and hates the Sweet Market vendors on sight.
  - The quest is a tunnel crawl with her as a temporary partner: a partner battle against Mother Gutter's vendors.
  - At the Quiet Ward, she sits with the half-Fixed patients and goes quiet. Then she tells Corvin and the PC about being stone: *"I could hear everything. Everyone who sat with me."* Corvin asks if he can record it.
- **Fight:** the farewell fight at the grate she came through, lv ~38, on `:CORROSIVE_MIRE`. Ace Seviper with a custom Venam's Kiss (if the move team adds it; otherwise a strong Poison move).
- **Reward:** **Venam's Testimony** (Key Item, Corvin's recording).
  - It can be played for Juno at the Bride Tree (Ch10) or in Ch20.
  - It is one of the **three proofs** for Envoy Okoro (`:ch20_envoy`).
  - Also **Black Sludge**.
- **Post-game (v2):** lv 100.

## 3. "Two Lucarios" — Garret (Desolation)
- **Source ✔:** Ayrith's **Fighting** Gym Leader (Cellia South). Gruff, blunt and loyal, and ✔ searching for his kidnapped sister **Eden**. ✔ **Mega Lucario**.
- **Where/when:** Act II, Ch9, Ironreach's lower shafts below the Iron Pit, after the Conclave.
- **Premise:**
  - During the Ironreach Open's undercard, a stranger with a Lucario asks every pit-fighter about a girl named Eden. He walked out of a puddle in the shafts during the Conclave's Bleed burst.
  - Kaito recognizes something in him and lends him a cot.
  - The PC helps him search the old Aurel shafts, where his Lucario senses people sleeping behind the walls. This is a tiny foreshadow of the Quiet Towns and Marrowgate.
  - She isn't here. He wants to fight the PC "to see if this world's worth searching".
- **Fight:** lv ~46 on `:COLOSSEUM`, with Mega Lucario (if Megas are enabled; otherwise Lucario with an item build). Kaito watches.
- **Reward:** **Lucarionite** if Megas are enabled, otherwise a **Riolu** egg. Also Black Belt. Lore: "Talk less. Fight more. Then we'll talk."
- **Post-game (v2):** lv 100, plus the **Marrowgate rumor**: a girl matching Eden's description seen near the Quiet Towns. It's a deliberate dead end and a kindness. We never resolve another game's plot.

## 4. "What Are You For?" — Melia (Rejuvenation)
- **Source ✔:** The heart of Rejuvenation. Adoptive daughter of Professor Jenner and a reserve **Normal** Gym Leader. ✔ **Hapi** (a Togekiss raised from her treasured Togepi), Zoroark, Mimikyu, Snorlax. ✔ She is Venam's close friend and ex.
- **Where/when:** Act III, Ch10, the **Royal Chase** (Safari-style reserve) outside Verdance, after J3.
- **Premise:**
  - A blonde girl with a Togekiss is searching the reserve for "a friend who fell through a sewer". If the Venam quest is done, the PC can tell her Venam got home safely.
  - The Queen's huntsmen think she's a poacher. The PC vouches for her.
  - She watched Juno's confirmation from the crowd and asks the PC the question nobody else does: *"Everyone keeps telling you what you're* for*. Have you decided yet?"*
  - Her way home is the reflection in the Chase's royal fishpond.
- **Fight:** lv ~50, with **Hapi (Togekiss)** as ace.
- **Reward:** a **Togepi** egg and a Soothe Bell.
  - Bonus if Venam's quest is done: a Gale Post letter from Venam, routed through the Glass ("u owe me a rematch, null kid").
- **Post-game (v2):** lv 100.

## 5. "Crystal Sleep" — Alexandra (Rejuvenation)
- **Source ✔:** Elite 8 member and **Acting Champion** of Aevium. ✔ Her known Pokémon lean Dragon/Psychic: Latias, Dragonite, Altaria, Starmie, Lapras, Sigilyph, Garchomp. ✔ Her mother **Celine**, Aevium's Champion, sleeps **encased in crystal**, recovering from wounds inflicted by Madame X.
- **Where/when:** Act III, Ch11, Rimeholt's **sunken lower town** after the Thaw and Gym 10.
- **Premise:**
  - Among the half-Fixed fishers on the broken ice sits a tall woman with a Latias, asking each one whether they can hear her. She came through the Thaw's black water.
  - Velmora's Fixing looks horribly like her mother's crystal. She has questions for Anja (blunt) and Corvin (by Gale Post).
  - The PC helps her move three Fixing fishers to the heat-tower shelters before the next freeze. She is quietly devastated by how many there are.
  - She leaves through a frozen mirror in the Thane's hall: "My mother has been asleep in crystal for a long time. I'd like to know if yours wake up."
- **Fight:** lv ~56, on a Dragon/Psychic champion team. **Ace: Latias.**
- **Reward:** a **Draco Meteor** tutor and **Celine's Notes** (lore Key Item: an otherworld physician's notes on crystal stasis). Field Notes then adds a line: "the sleepers may be dreaming".
- **Post-game (v2):** lv 100.

## 6. "Deliverer" — Amaria and Titania (Reborn)
- **Source ✔:** **Amaria**, Reborn's late-game **Water** Gym Leader, famous for her nicknamed team, including **Lapras "Deliverer"** (ace, per ruling), Starmie "Twinkle", Ludicolo "Indiana" and Kingdra "Atlantica". ✔ Her gym is an underwater maze. **Titania**, Reborn's **Steel** Gym Leader: ✔ her battle is on the **Fairy Tale field** in a sky castle, and her chapter is paired with Amaria's (badges 15–16). Her team concept is knightly (Aegislash, Mawile).
- **Where/when:** Act IV, Ch17, drowned **Aurelia**'s lower galleries (Seabed / Aurelia maps, Dive), after Gym 16, before the PC leaves Underveil.
- **Premise:**
  - Edda's divers report a woman swimming *without a suit* in the drowned galleries, singing to a Lapras, and an armored knight pacing the drained shallows above who refuses to leave.
  - Amaria followed "a city under a city" through the Glass. Drowned places call to her, and Aurelia is calling hard.
  - Titania followed Amaria.
  - The PC dives a short underwater maze to reach Amaria, who is sitting in a flooded Gilder hall. She says the drowned city "isn't dead, it's *waiting*". This is a Ruin Route hint about Aurelius's reflection.
  - Titania won't let Amaria go home until "someone who can walk through walls" proves the way back is safe.
- **Fight:** **double battle** vs Amaria and Titania, lv ~78, on `:WATER_SURFACE` (Amaria's side; Titania's Steel suffers). Aces: **Lapras "Deliverer"** and **Aegislash**.
- **Reward:** a **Liquidation** TM, an **Assault Vest** from Titania ("a knight's spare"), and a **Lapras** of the PC's own: Deliverer's calf. "She'll carry you out of a flood someday." This echoes Valen's Lapras.
- **Post-game (v2):** both at lv 100.

## 7. "Dreamwalker" — Shiv (Desolation)
- **Source ✔:** The **Champion of Ayrith**. Mysterious and initially shady, ✔ later revealed to be working under Darkrai. ✔ Signature **Aipom → Ambipom** with absurd HP. ✔ He's a trickster, and ✔ he has already crossed worlds, as "Dreamer Shiv" in Reborn's post-game.
- **Where/when:** Act V, Ch18, Gloaming's dusk-chapels, after Gym 17.
- **Premise:**
  - Gloaming's townsfolk keep dreaming the same grinning stranger. He walks dreams, and Gloaming's endless dusk makes the dream-road easy.
  - He greets the PC: *"Met you already. You were standing on a ferry, glowing like a lighthouse."*
  - The quest is three dream-errands for the townsfolk: return a lost name, finish a dead man's sentence, find a child's Pokémon in a dream that isn't hers.
  - He finally admits he's lost: "Dreams leak through your Glass like water through a roof. I followed one too far."
- **Fight:** lv ~84. Trickster tech (Fake Out, Trick, Taunt, odd abilities). **Ace: Ambipom** with absurd HP (custom stats, balance-approved).
- **Reward:** a **Dusk Stone** and **Dream Mist** (Key Item: re-watch any completed interlude).
- **Ruin hint:** only if the Ledger holds any game over: *"You've done this before, haven't you. I can smell the other nights on you."*
- **Post-game (v2):** lv 100.

## 8. "the meteor champion" — Lin (Reborn) — post-game superboss
- **Source ✔:** Lin (Lindsey Paraeah), Reborn's hidden Big Bad. She usurped Team Meteor and is fought as Reborn's **Champion**.
  - ✔ Signature: a **Togekiss with Oblivion Wing**, a move it can't legally learn (signature beats legality, per ruling).
  - ✔ She **caught Arceus**.
  - ✔ Cynical, blunt, mean-spirited, Jekyll-and-Hyde. Her honest lines are written **in lowercase**, as an homage.
- **Where/when:** post-game, any ending with a post-game. Hesper Vane reports "a woman who talks without capital letters" haunting the Ferrow's Landing lighthouse at night. Found there; fought at the **Distortion Core** antechamber (Antumbra).
- **Premise:**
  - She came through the Glass the night Arceus came down, because she felt it from her world. Per the Rule of the Glass, her own Arceus wouldn't follow.
  - Her lines depend on the ending:
    - Homecoming: "you gave it back. good. i couldn't."
    - Long Vigil: "you kept it. i kept mine too. look at us."
    - Concord Dawn: "it's quiet, isn't it. for a while."
  - With any game over in the Ledger: "you've done this before, haven't you."
- **Fight:** **superboss**, lv 100, the hardest optional fight in the game. **Ace: Togekiss (Oblivion Wing).** The rest are Reborn-endgame heavy hitters, chosen by balance (no Arceus).
- **Reward:** the **Ledger Lens** (Key Item: turns Ledger hints on for this save, the in-game equivalent of the 'ledgerhints' password), plus a lowercase letter left in the lighthouse: "see you in the next one."

## 9. Nova (Desolation) — Ruin Route only
- **Source ✔:** Leader of **Team Crescent**. An anti-villain who wants a dream world where everyone is happy, manipulative but sincere. ✔ Signature: **Gothitelle**.
- **Where/when:** Ruin Route, R5, on the **Mirrorwalk dream-road** between Gloaming and Wyrmrest (`story/12_RUIN_ROUTE.md`).
- **Premise:** drawn to a PC whose Resonance has locked at Ruin, she offers a gentler unmaking: everyone asleep and happy forever. Accepting is `GO_R_SWEET_DREAMS`. Refusing leads to a fight.
- **Fight:** lv ~90. **Ace: Gothitelle.**
- **Reward:** the **Crescent Charm** (Ruin Key Item; Nova's last kindness). In R7 it lets the Reflection speak one extra line.

---

## Sources (checked 2026-11-15)
- TV Tropes, *Pokémon Desolation* characters: https://tvtropes.org/pmwiki/pmwiki.php/Characters/PokemonDesolation
- TV Tropes, *Pokémon Reborn* "Others" and "Postgame Characters": https://tvtropes.org/pmwiki/pmwiki.php/Characters/PokemonRebornOthers · https://tvtropes.org/pmwiki/pmwiki.php/Characters/PokemonRebornPostgameCharacters
- TV Tropes, *Pokémon Rejuvenation*: https://tvtropes.org/pmwiki/pmwiki.php/VideoGame/PokemonRejuvenation · https://www.tvtropes.org/pmwiki/pmwiki.php/Characters/PokemonRejuvenationPastCharacters
- Rejuvenation Wiki: https://rejuvenation.wiki.gg/wiki/Venam · /Melia · /Alexandra · /Celine
- Reborn Rebalance walkthrough (modded teams; used only for identity, field and nickname cross-checks): https://reborn-rebalance-out.pages.dev/walkthroughs/21_titania_amaria · /27_elite_4.html

**Note for the trainer agent:** NARRATIVE_KEYS §7 no longer lists any `FESTIVAL_<cameo>` team as a Festival team. Build the versions in this file instead.
