# Mega Evolution - headless test (tools/harness/run_mega.rb)

Real Essentials v21.1 battle code with Prismfall Core, Field Effects, Z-Power, Bosses, Trials and Mega; AI on both
sides unless noted. Logic only: the EBDX animation is checked in the real engine (design/MEGA_EVOLUTION.md section 8).

**69/69 checks passed.**

| | Check | Detail |
|---|---|---|
| PASS | Gen 6/7 Mega forms: 48 (47 with a stone + Rayquaza's Dragon Ascent) | VENUSAUR_1,CHARIZARD_1,CHARIZARD_2,BLASTOISE_1,BEEDRILL_1,PIDGEOT_1 |
| PASS | 47 Mega Stone items, each the stone of a form | 47 |
| PASS | the Mega Ring is a key item with the MegaRing flag |  |
| PASS | every stone is placed (44) or listed as unplaced (3) | missing [], unknown [] |
| PASS | every STONES row has a badge gate, a known map and a known method | [] |
| PASS | the Ring comes after Badge 13, like Reborn (13 at the earliest) and Rejuvenation (about 14): Cragholm, Bastian |  |
| PASS | R4 with the Ring: no stone powers up an answer to the next 2 Wardens when it becomes usable |  |
| PASS | stones before the Ring 'hum and wait' (12): Manectite, Glalitite, Ampharosite, Sceptilite, Blastoisinite, Venusaurite, Beedrillite, Altarianite, Slowbronite, Alakazite, Aerodactylite, Pinsirite |  |
| PASS | the strongest stones come late (Reborn 12-17, Rejuvenation 11-15): none before 10 badges | [] |
| PASS | legendary stones are post-game |  |
| PASS | quests, story scenes, bosses and rank rewards hand out their stones at or after the gate |  |
| PASS | rank-reward stones are reachable before the Ring (so the R4 check holds for them) |  |
| PASS | design/TRIAL_EVENTS.yaml places all 25 world stones (pf_mega_stone, badge-gated) and every Mega talk key |  |
| PASS | Prismfall Z-Power is one Z per side too (owner key = side) |  |
| PASS | the player's Camerupt Mega Evolved on turn 1 (ring in the Bag, Cameruptite held) | {:side=>0, :idx=>0, :species=>:CAMERUPT, :form=>1, :ability=>:SHEERFORCE, :old_ability=>:MAGMAARMOR, :turn=>1, :field=>: |
| PASS | the Mega messages and both EBDX-named animations ran |  |
| PASS | the Mega's ability is Sheer Force (form data), and the field saw the change |  |
| PASS | Volcanic showpiece: a Fire-type Mega primes the volcano, which erupts at the end of the round |  |
| PASS | the Mega happens before any move that turn | 17 < 21 |
| PASS | only one Mega in the whole battle (1 turns) |  |
| PASS | Anja's Glalie Mega Evolved on Standard (AI, MEGARING in her items) | {:side=>1, :idx=>1, :species=>:GLALIE, :form=>1, :ability=>:REFRIGERATE, :old_ability=>:INNERFOCUS,  |
| PASS | the AI Mega Evolves the first turn its Glalie can act | 1 turn headers in between |
| PASS | Brann's Camerupt Mega Evolves on Standard at Gym 7 (a designed weak Mega below Lv 50) | {:side=>1, :idx=>1, :species=>:CAMERUPT, :form=>1, :ability=>:SHEERFORCE, :old_ability=>:MAGMAARMOR, |
| PASS | ...on Volcanic, and its Mega primes the eruption as designed (Brann's fight is kept as is, per the user) |  |
| PASS | trainers.txt: every important fight from ace 50 Megas in all modes (36 Std / 36 Hard / 36 Casual) or uses a designed Z (3 / 3 / 3); below it only designed weak Megas; one stone, a ring, no Z-crystal beside it |  |
| PASS | K8 without Morwen's Ring: no ring, no stone (Kestrel has no ring of his own) |  |
| PASS | K8 with Morwen's Ring (:ch18_kestrel_ring = :give_now): the ring, and his Scizor holds the Scizorite | SCIZOR Lv92 @SCIZORITE |
| PASS | the foe used one Mega (Lucario) and one Z-move (Hydro Vortex) in the same battle | megas 1, z [:HYDROVORTEX] |
| PASS | both on turn 1 (the Mega first, before moves; the Z-move in the move phase) |  |
| PASS | the one ring: with only the Mega Ring the player's side used one Mega and one Z-move in one battle | megas [:LUCARIO], z [:HYDROVORTEX] |
| PASS | save compatibility: an old save's Z-Power Ring alone still wakes crystals (not stones) |  |
| PASS | no ring at all: no Z-Power |  |
| PASS | Z-crystals: all 18 type crystals + 2 species crystals placed once, R4 with the Ring, sources and gates (5 ring and wait before 13) |  |
| PASS | a species crystal: Snorlax's Giga Impact becomes Pulverizing Pancake (its own power) | {:side=>0, :idx=>0, :z=>:PULVERIZINGPANCAKE, :turn=>1, :owner=>0} |
| PASS | LIMIT :side - only one of the two foe trainers Mega Evolves in the whole battle | ["LUCARIO@owner0"] |
| PASS | control: with Essentials' per-trainer rule both trainers Mega Evolve | ["LUCARIO@owner0", "METAGROSS@owner1"] |
| PASS | Z_LIMIT :side - one Z-move for the whole foe side | ["HYDROVORTEX@owner0"] |
| PASS | control: with Z-Power's own per-trainer rule each trainer unleashes one | [:GIGAVOLTHAVOC, :HYDROVORTEX] |
| PASS | a side gets one Mega AND one Z-move (different trainers) |  |
| PASS | without the Mega Ring the player's side never Mega Evolves |  |
| PASS | wild Pokemon never Mega Evolve |  |
| PASS | a Pokemon holding a Z-crystal can't Mega Evolve (Rayquaza) |  |
| PASS | control: Rayquaza with Dragon Ascent and no crystal Mega Evolves |  |
| PASS | Grand Stage: the applause rises a stage (1 -> 2) on the Mega | 2 |
| PASS | Frozen Lake: an Ice-type Mega seals every crack (crack meter 2 -> 0) | [0, 3] |
| PASS | Crystal Cavern: the crystals take a Grass Mega's colour (hue Fire -> Grass) | 2 |
| PASS | Hollow Cathedral: a Ghost-type Mega re-haunts a consecrated nave (stage 2 -> 1) | 1 |
| PASS | Factory: a Steel-type Mega's plating is hammered home (+1 Defense) |  |
| PASS | Bleed: the Mega makes the Bleed lurch to new borrowed effects at once | 2 overlay changes |
| PASS | Colosseum: the Mega's new No Guard triggers the field's entry rule (+1 Attack), and the crowd roars |  |
| PASS | Inverse: the Mega's new Magic Bounce triggers the field's entry rule (+1 Sp. Def) |  |
| PASS | ...but not twice: an Absol that already had Magic Bounce got the rule on entry only | {:ATTACK=>0, :DEFENSE=>0, :SPECIAL_ATTACK=>0, :SPECIAL_DEFENSE=>1, :SPEED=>0, :ACCURACY=>0, :EVASION=>0} |
| PASS | Field Notes show the Mega line for all 8 showpiece fields | [] |
| PASS | Field Notes add the new-ability line where a Mega ability has an entry rule (Inverse, Colosseum, Frozen Lake...) |  |
| PASS | The Humming Lamp is locked at 2 badges |  |
| PASS | at 3 badges Hesper gives the Ampharosite, and it hums (no ring yet) |  |
| PASS | a world stone (pf_mega_stone) is received once; a second call gives nothing |  |
| PASS | a world Z-crystal (pf_z_crystal) before the Ring: received once, with its own teaser |  |
| PASS | the Ring-Day is locked before Gym 13 |  |
| PASS | after Gym 13 the Ring-Day is available in Bastian's lamp-room |  |
| PASS | Bastian gives the Mega Ring and the Aggronite; the quest finishes quietly |  |
| PASS | the ring sings, Pip hears it, and the earlier stones stop waiting |  |
| PASS | no early reveal: Bastian never says 'reset' or names the Legend Plate |  |
| PASS | Brann's spare (Cameruptite) waits for 15 badges |  |
| PASS | at 15 badges Brann knows his ring, gives the Cameruptite, and is hurt about the Light Stone (it went to the Dominar) |  |
| PASS | the Old Pincer (a 2-bar wild boss on Silkwood) guards the Pinsirite; beating it pays out | status :won |
| PASS | the player's Charizard Mega Evolved in the boss fight |  |
| PASS | The Brazier Writ: a lie at the brazier burns the writ (no stone, quest still open) |  |
| PASS | ...the truth earns the Salamencite |  |

Megas logged: 20; Z-moves logged: 7. Battle transcripts: `transcript.txt`.
