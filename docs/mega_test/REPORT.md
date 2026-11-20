# Mega Evolution - headless test (tools/harness/run_mega.rb)

Real Essentials v21.1 battle code with Prismfall Core, Field Effects, Z-Power, Bosses, Trials and Mega; AI on both
sides unless noted. Logic only: the EBDX animation is checked in the real engine (design/MEGA_EVOLUTION.md section 8).

**59/59 checks passed.**

| | Check | Detail |
|---|---|---|
| PASS | Gen 6/7 Mega forms: 48 (47 with a stone + Rayquaza's Dragon Ascent) | VENUSAUR_1,CHARIZARD_1,CHARIZARD_2,BLASTOISE_1,BEEDRILL_1,PIDGEOT_1 |
| PASS | 47 Mega Stone items, each the stone of a form | 47 |
| PASS | the Mega Ring is a key item with the MegaRing flag |  |
| PASS | every stone is placed (44) or listed as unplaced (3) | missing [], unknown [] |
| PASS | every STONES row has a badge gate, a known map and a known method | [] |
| PASS | the Ring-Day is mid-Act II (Cindervault, after Gym 7) |  |
| PASS | R4 with the Ring: no stone powers up an answer to the next 2 Wardens when it becomes usable |  |
| PASS | stones before the Ring-Day are teasers only (5): Absolite, Manectite, Sharpedonite, Ampharosite, Steelixite |  |
| PASS | the strongest stones come late (Reborn 12-17, Rejuvenation 11-15): none before 10 badges | [] |
| PASS | legendary stones are post-game |  |
| PASS | quests, story scenes, bosses and rank rewards hand out their stones at or after the gate |  |
| PASS | rank-reward stones are reachable before the Ring-Day (so the R4 check holds for them) |  |
| PASS | design/TRIAL_EVENTS.yaml places all 25 world stones (pf_mega_stone, badge-gated) and every Mega talk key |  |
| PASS | Prismfall Z-Power is one Z per side too (owner key = side) |  |
| PASS | the player's Camerupt Mega Evolved on turn 1 (ring in the Bag, Cameruptite held) | {:side=>0, :idx=>0, :species=>:CAMERUPT, :form=>1, :ability=>:SHEERFORCE, :old_ability=>:SOLIDROCK, :turn=>1, :field=>:V |
| PASS | the Mega messages and both EBDX-named animations ran |  |
| PASS | the Mega's ability is Sheer Force (form data), and the field saw the change |  |
| PASS | Volcanic showpiece: a Fire-type Mega primes the volcano, which erupts at the end of the round |  |
| PASS | the Mega happens before any move that turn | 14 < 18 |
| PASS | only one Mega in the whole battle (1 turns) |  |
| PASS | Kaito's Lucario Mega Evolved (AI, trainer holds MEGARING in its items) | {:side=>1, :idx=>1, :species=>:LUCARIO, :form=>1, :ability=>:ADAPTABILITY, :old_ability=>:JUSTIFIED, |
| PASS | on the Colosseum (the gym's field): the crowd roars for it, unless it is already in a Frenzy | COLOSSEUM stage 2, kos 3, roared false |
| PASS | the AI Mega Evolves the first turn its Lucario can act | 1 turn headers in between |
| PASS | the foe used one Mega (Lucario) and one Z-move (Hydro Vortex) in the same battle | megas 1, z [:HYDROVORTEX] |
| PASS | both on turn 1 (the Mega first, before moves; the Z-move in the move phase) |  |
| PASS | the player's side used one Mega and one Z-move in one battle | megas [:LUCARIO], z [:HYDROVORTEX] |
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
| PASS | the Ring-Day is locked before Gym 7 |  |
| PASS | ...and at 7 badges until the Caldera Crisis is decided |  |
| PASS | after the Caldera Crisis the Ring-Day is available |  |
| PASS | Brann gives the Mega Ring and the Aggronite; the quest finishes quietly |  |
| PASS | the vent-branch line plays (the cold forge) and the ring sings |  |
| PASS | Brann's spare (Cameruptite) waits for 10 badges |  |
| PASS | the Old Pincer (a 2-bar wild boss on Silkwood) guards the Pinsirite; beating it pays out | status :won |
| PASS | the player's Charizard Mega Evolved in the boss fight |  |
| PASS | The Brazier Writ: a lie at the brazier burns the writ (no stone, quest still open) |  |
| PASS | ...the truth earns the Salamencite |  |

Megas logged: 19; Z-moves logged: 6. Battle transcripts: `transcript.txt`.
