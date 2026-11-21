# FLAGS — Story Game Switches & Variables Registry (101–300)

> Owner: Story lead. Range per SPINE: **Switches 101–300, Variables 101–300 = story.** Gym puzzles use **301–400** (World lead). Core state is never stored here.
> **What goes here:** *event/world state*, meaning things map events need on page conditions (a map's look, an NPC's presence, a scene already played).
> **What does NOT go here:** player **choices, Bonds, Standing, Resonance, game overs and endings**. Those live in Core save data (`Prismfall.state.narrative`, SYSTEMS.md §8) under keys owned by `design/NARRATIVE_KEYS.md`. Events read them with `pf_choice(:key)`, `pf_bond(:ID)`, `pf_cond("…")`. Never mirror a choice into a switch by hand. If a mirror is ever needed for an event page, add it in the "Core-written mirrors" block below, written by Core only.
> Naming: `S###` switch, `V###` variable. "Set by" is where the story sets it. Reserved gaps are deliberate, so append inside each block.
> **Revision 14 (Saltmere is now Chapter 2 / Gym 1, Briarwick Chapter 3 / Gym 2):** IDs and names never change, so some names carry their old chapter prefix. `CH2_*` switches (S106, S107) are **Chapter 3, Briarwick**, and `CH3_*` switches (S108–S110) are **Chapter 2, Saltmere**. Only the descriptions below changed. Gym puzzle blocks follow the building, not the gym number: 305–309 = the Loomhouse (Gym 2), 310–314 = the Pell Playhouse (Gym 1) (GYM_PUZZLES §1).

## Variables (V101–V140 used, V141–V300 reserved)

| ID | Name | Values / meaning | Set by |
|---|---|---|---|
| V101 | STORY_ACT | 0 = Prologue, 1–5 = Act, 6 = post-game | Act title cards |
| V102 | STORY_CHAPTER | 0 = Prologue, 1–21 = chapter (2 = Saltmere "Curtain Call", 3 = Briarwick "The Weaver's Debt"), 22 = epilogue, 23 = post-game | Chapter openers / closers (2 at the Ch1 cutscene, 3 at Saltmere's North Gate, 4 at Briarwick's charcoal child) |
| V103 | FESTIVAL_DAY | 0–7 (Ch20–21 scene day; Core's `festival_stage` tracks the bracket separately) | Crownhaven day transitions |
| V104 | LOWLIGHT_STATE | 0 = intact, 1 = Shattered (608 replaces 181), 2 = spreading (Act IV), 3 = healed (Homecoming) | Ch5, Act IV opener, ending |
| V105 | BRIARWICK_GLASSWOOD | 0 = edge, 1 = receded (Matriarch beaten; the Windfall Row forest-road cordon lifts), 2 = at the looms (Act IV), 3 = gone | Ch3, Act IV, ending |
| V106 | VERDANCE_BLOOM | 0 = normal, 1 = runaway (Ch10 arrival), 2 = tamed (Juno confirmed), 3 = autumn (Homecoming) | Ch10, ending |
| V107 | RIMEHOLT_STATE | 0 = frozen, 1 = Thaw (lower town sunk), 2 = rebuilding (epilogue) | Ch11, epilogue |
| V108 | EBB_STATE | 0 = two-way, 1 = stuttering, 2 = stopped (Ch4 night), 3 = restored (Ebbmouth Strike) | Ch4, Ch11 transit |
| V109 | DUNEHOLT_WELL | 0 = sinking, 1 = dry (Act IV), 2 = refilling (Groudon calmed) | Ch6, Ch14 transit |
| V110 | CINDERVAULT_STATE | 0 = normal, 1 = ashen (vented), 2 = overdrawn (dampers) | Ch8 (per choice result) |
| V111 | NADIR_STATE | 0 = normal, 1 = Mandate checkpoints, 2 = Purge, 3 = independent | Ch9, Ch16, Ch17 |
| V112 | GLOAMING_DUSK | 0 = local, 1 = spreading south (Act V), 2 = night sky (Homecoming) | Act V opener, ending |
| V113 | ROWAN_STATUS | 0 = free (Warden), 1 = Meridian custody, 2 = tribunal, 3 = escaped / Lantern Hollow, 4 = at the Festival, 5 = reunited with Elin | Ch9, Ch13, Ch14, Ch20, ending |
| V114 | KESTREL_STAGE | 0 = intro, 1 = hunting the Mourner, 2 = Meridian-sponsored, 3 = post-Gravenmoor, 4 = Festival entrant, 5 = resolved | K1–K8 aftermaths |
| V115 | LARCH_STATUS | 0 = Tidewatch, 1 = in Skyreach, 2 = fugitive (Cragholm), 3 = at the Festival | Ch12, Ch14, Ch20 |
| V116 | VALEN_STATUS | 0 = Sovereign, 1 = dying (post-ceremony), 2 = dead | Ch20, Ch21 |
| V117 | ENGINE_WEAKPOINTS | 0–6 count (telemetry sabotaged, Zekrom freed, governor, grid cut, comms, schematics) for staging lines. Endings read Core keys, not this | Recomputed by Core helper before Ch21 (story mirror) |
| V118 | WARDENS_RELEASED | 0–18 during the Arceus battle staging (Core owns consent logic) | Ch21 battle script |
| V119 | INTERLUDE_ACTIVE | 0 = none, 1 = Kestrel "Lamplight", 2 = Rowan "Bride Tree", 3 = Kestrel "Dead Letters", 4 = Wenlow "Clear Air", 5 = Valen "The Last Night" | Interlude start/end (party swap scripts read it) |
| V120 | UNDERSTUDY_FORM | 0 = Eevee, 1–8 = Eeveelution (for Vesper's line) | Evolution hook / Ch20 |
| V121 | ZYGARDE_CELLS_STORY | Story-placed cells collected (side quest) | Cell events |
| V122–V140 | (reserved: per-chapter scene step counters, one per chapter as needed) | | |

## Switches: progression milestones (S101–S160)

| ID | Name | Meaning |
|---|---|---|
| S101 | PRO_FERRY_DONE | Prologue deck scene finished |
| S102 | PRO_SCANNED_NULL | Dock scan played (customs gate NPC changes) |
| S103 | CH1_STARTER_GOT | Starter received |
| S104 | CH1_K1_DONE | K1 fought |
| S105 | CH1_ORCHARD_DONE | Glassed Orchard tutorial cleared |
| S106 | CH2_THISTLE_DONE | Thistle admin battle at Briarwick's pylon (Ch3) |
| S107 | CH2_MATRIARCH_DONE | Glass Matriarch boss cleared (Ch3, after Gym 2) |
| S108 | CH3_PAGEANT_DONE | Mourner's Saltmere pageant scene (Ch2, after Gym 1; opens the North Gate) |
| S109 | CH3_J1_DONE | J1 on Saltmere's promenade green (Ch2, before Gym 1) |
| S110 | CH3_UNDERSTUDY_GOT | Gift Eevee "Understudy" received (Ch2, right after Gym 1) |
| S111 | CH4_K2_DONE | K2 |
| S112 | CH4_TEO_MET | Teo admin battle |
| S113 | CH5_GALA_DONE | Gala and raid finished |
| S114 | CH5_SHATTER | Lowlight Shattered (see V104) |
| S115 | CH5_MANDATE | Mandate granted (Directorate checkpoint NPCs appear realm-wide) |
| S116 | CH6_OSSUARY_DONE | Unown ruins / murals |
| S117 | CH6_K3_DONE | K3 |
| S118 | CH7_J2_DONE | J2 |
| S119 | CH7_WICK_DONE | Wick met (battle or talk) |
| S120 | CH8_CALDERA_DONE | Caldera Crisis resolved (V110 holds the result) |
| S121 | CH8_WAR_DRUMS | Ashkaar closed the eastern passes (Ashkaar NPC dialogue swaps) |
| S122 | CH9_K4_DONE | K4 (Ironreach Open final) |
| S123 | CH9_CONCLAVE_DONE | Conclave attack finished |
| S124 | CH9_MOURNER_UNMASKED | Rowan unmasked (realm-wide NPC gossip swaps) |
| S125 | CH10_JUNO_WARDEN | Juno confirmed. Verdance gym open as J3 |
| S126 | CH10_ROYAL_CHASE_OPEN | Royal Chase (Safari) opened |
| S127 | CH10_LOYAL_THREE_DONE | Bride Grove boss sequence cleared |
| S128 | CH11_THAW | The Thaw happened |
| S129 | CH11_KYOGRE_DONE | Kyogre boss cleared |
| S130 | CH11_EBB_STRIKE | Ebbmouth Strike scene played |
| S131 | CH12_LARCH_PAPERS | Broadcast happened (NPCs reference it) |
| S132 | CH12_GALE_RAID | Gale Post raided |
| S133 | CH12_K5_DONE | K5 |
| S134 | CH13_ANTUMBRA_ENTERED | Crossed the Glass |
| S135 | CH13_MINDSCAPE_DONE | Mindscape scene played |
| S136 | CH13_TRIBUNAL_DONE | Tribunal finished |
| S137 | CH13_FAULT | **The Fault.** South coast drained, encounter version 1 from Act IV |
| S138 | CH14_TELEMETRY_SCENE | Larch dismantled the badge case |
| S139 | CH14_RAID_DONE | Cragholm raid finished |
| S140 | CH14_GROUDON_DONE | Groudon boss cleared |
| S141 | CH15_ECHO_DONE | Cathedral AF 290 echo played |
| S142 | CH15_K6_DONE | K6 |
| S143 | CH15_GIRATINA_DONE | Reverse Depths boss cleared |
| S144 | CH16_BLUEPRINTS_GOT | Arbiter Blueprints obtained |
| S145 | CH16_ZEKROM_DONE | Zekrom freed (story event; Core key `ZEKROM_FREED` is authoritative) |
| S146 | CH16_PURGE_BEGUN | Sump Purge underway (Nadir maps → Purge state) |
| S147 | CH17_AURELIA_DONE | Sun Court sequence finished |
| S148 | CH17_SHARD_NAMED | The PC knows what they carry (dialogue swaps everywhere) |
| S149 | CH17_NADIR_INDEPENDENT | Nadir independence proclaimed |
| S150 | CH18_PECHARUNT_DONE | Lightless Deep boss cleared (Sweetrot vendors wake) |
| S151 | CH18_HYMN_GOT | Full Hymn received |
| S152 | CH18_K7_DONE | K7 |
| S153 | CH19_OATH_SPOKEN | Sigrun's trial oath given |
| S154 | CH19_RESHIRAM_DONE | Reshiram boss cleared |
| S155 | CH20_VEIL_GATE_OPEN | Champions arrived (cameo NPCs appear in Crownhaven) |
| S156 | CH20_CEREMONY_DONE | Opening ceremony and vision |
| S157 | CH20_MASQUES_DONE | Night of Masques played |
| S158 | CH20_AUDIENCE_DONE | Valen's audience played |
| S159 | CH21_FINALE_DONE | Arceus battle finished. Ending sequence running |
| S160 | POSTGAME | Post-game unlocked (Spire, Warden's Gauntlet, Distortion Core) |

## Switches: world/NPC presence and side content (S161–S220)

| ID | Name | Meaning |
|---|---|---|
| S161 | LARCH_AT_TIDEWATCH | Larch NPC present at Ferrow's Landing (off after Ch12) |
| S162 | EDDA_SMUGGLER | Edda's smuggler boat available (from Ch5 aftermath) |
| S163 | HESPER_WARM | Hesper sends care packages (after Ch15) |
| S164 | DEX_SHRINE | Lowlight shrine event (Act II on) |
| S165 | THORNGUARD_HEARTGARDEN | Thornguard occupy the Heartgarden (Ch10, before confirmation) |
| S166 | THORNGUARD_GLOAMING | Thornguard checkpoint at Gloamwood Verge (Act V, cleared by Celestine) |
| S167 | DOMINAR_LEGIONS | Ashkaar legions camp at Wyrmrest |
| S168 | ISENMAR_MARTIAL_LAW | Isenmar refugee NPCs in Elowen and Cragholm |
| S169 | LANTERN_THEATRE_SHUT | Saltmere theatre closed (Act III–IV) |
| S170 | GLOAMING_DISGUISED_CELESTINE | Ch3 old-woman NPC at Briarwick's Loyal Three shrine (off once Tamsin's badge is won) |
| S171 | HOLLOW_SANCTUARY_OPEN | Branch map 698 entrance visible (set when Core's Standing check passes at Ch10 start) |
| S172 | BLACK_SITE_OPEN | Branch map 699 entrance visible |
| S173 | ACCORD_ARCHIVE_OPEN | Branch map 838 entrance visible |
| S174 | DOCTORS_CELL_QUEST | "The Doctor's Cell" side quest active (Ch11–13) |
| S175 | LITTLE_OWL_QUEST | Ilsa's "Little Owl" quest active (Ch13–20) |
| S176 | THISTLEDOWN_CLEARED | Haunted manor completed (Ch3, on the Weavers' Road) |
| S177 | EEVEE_OCTAVE_DONE | Eeveelution gauntlet cleared (set by the Trials quest `CR_OCTAVE` on the win; SPINE Rev 19) |
| S178 | VANE_HALL_DONE | Vane Hall sequence completed |
| S179 | WENLOW_ALIVE | On until Interlude IV ends (Mirefen NPC page) |
| S180 | TYPE_NULL_GIFT | Black Site Type: Null received |
| S181–S220 | (reserved: per-Warden post-gym side-arc steps, two per Warden = 36, plus 4 spare) | |

## Switches: Core-written mirrors (S221–S260), events read-only

Core writes these from NARRATIVE_KEYS only if an event page condition needs one. The story team adds a row on request, and Narrative Systems confirms the key.

| ID | Mirrors | Why an event needs it |
|---|---|---|
| S221 | Teo alive (`TEO_SAVED`) | Teo NPC pages in Ebbmouth / Lantern Hollow / Festival |
| S222 | Corvin freed (`CORVIN_FREED`) | Corvin vs Wenlow at Cragholm hospital |
| S223 | Ogerpon trusted (`OGERPON_TRUSTED`) | Ogerpon follower / Festival presence |
| S224 | Marchetti turned (`MARCHETTI_TURNED`) | Hijack staging |
| S225 | Magnus kept faith (`MAGNUS_KEPT_FAITH`) | Magnus NPC location in Act V |
| S226 | Dominar swayed (`DOMINAR_SWAYED`) | Legion NPCs at Crownhaven vs gone |
| S227 | Ilsa reconciled (`ILSA_RECONCILED`) | Sanctum door scene |
| S228 | Kestrel redeemed (Narrative Systems' Kestrel state) | SF/hijack staging |
| S229–S260 | (reserved) | |

## Switches: endings and post-game (S261–S300)

| ID | Name | Meaning |
|---|---|---|
| S261 | ENDING_PLAYING | Ending sequence active (blocks menus) |
| S262 | EPILOGUE_DONE | Epilogue slides finished. Post-game map states apply |
| S263 | PG_HOMECOMING_WORLD | Post-game world uses Homecoming map states (fields fading, the Fixed awake). Set from Core's ending ID |
| S264 | PG_VIGIL_WORLD | Post-game uses Long Vigil / Borrowed Crown map states |
| S265 | PG_RUIN_WORLD | Ruin Route aftermath states |
| S266 | PG_SPIRE_OPEN | Concordance Spire (Battle Tower) open |
| S267 | PG_GAUNTLET_OPEN | Warden's Gauntlet open |
| S268 | PG_DISTORTION_OPEN | Distortion Core (910) open |
| S269 | PG_CONCORD_ZERO | Quent's post-game arc started |
| S270–S300 | (reserved) | |

---

## Narrative keys, game overs and endings

**Superseded:** the crosswalk that used to sit here has been adopted and finalized by Narrative Systems. The single source is **`design/NARRATIVE_KEYS.md`**:
- Choice keys are lowercase symbols (`:ch9_teo_sable`, `:war_climax`), §4 and §4.3.
- Derived flags keep their uppercase names (`TEO_SAVED`, `WAR_STOPPED`), §5.
- Game overs are `GO_<NAME>` (23 canonical plus 2 Ruin-only), §9. "Encore" was cut. `GO_WEATHER` and `GO_STAY_OUT` were added.
- Endings: 1 Good, 1 Bad, 6 Grey, 2 Ruin, §12.

Story-side proposals still waiting on Narrative Systems: `:ch20_colors` (the PC's delegation colors, flavor) and `:ch21_boon` (the Blessed's one decree in the Good ending). Both are described in `story/14_WAR_AND_BLESSING.md`.

## Additions since the first registry (Revisions 4–6)

| ID | Name | Meaning |
|---|---|---|
| V122 | WAR_STATE | 0 = tension, 1 = passes closed (Ch8), 2 = war declared (Ch11), 3 = Siege of Skaldfast (Ch15), 4 = Battle of the Glass Dunes fought (Ch19), 5 = Peace of Plates (Festival), 6 = settled (ending) |
| V123 | CAMEO_QUESTS_DONE | Count of sister-game sidequests completed (0–8) for NPC chatter |
| S181 | CAMEO_SHELLY_DONE | "Lost in the Gossamer" complete (Ch3, after Gym 2) |
| S182 | CAMEO_VENAM_DONE | "Sewer Royalty" complete (Venam's Testimony obtained) |
| S183 | CAMEO_GARRET_DONE | "Two Lucarios" complete |
| S184 | CAMEO_MELIA_DONE | "What Are You For?" complete |
| S185 | CAMEO_ALEXANDRA_DONE | "Crystal Sleep" complete |
| S186 | CAMEO_AMARIA_TITANIA_DONE | "Deliverer" complete |
| S187 | CAMEO_SHIV_DONE | "Dreamwalker" complete |
| S188 | CAMEO_LIN_DONE | Lin superboss beaten (post-game) |
| S189 | CAMEO_NOVA_DONE | Nova fought (Ruin Route) |
| S190 | VESPER_MET_SALTMERE | Eevee Octave first meeting (Ch2) |
| S191 | VESPER_MET_LUCENT | Eevee Octave second meeting (Ch13). SPINE Rev 19: the gauntlet no longer needs S190/S191; it opens when all eight singers are helped (Trials state `octave_ready`) |
| S192 | WAR_CUTSCENE_SEEN | WAR-1 has played (enables skip and theater replay) |
| S193 | RUIN_ROUTE_ACTIVE | Event-page mirror of Core's `ruin_route` (Core-written, read-only) |
| S229 | Mirror: Rowan alive (`ROWAN_ALIVE`) | Rowan vs Teo/Thistle NPC pages in Acts IV–V (Core-written) |
| S230 | Mirror: war outcome is a victory for Ashkaar | Banner events at Skaldfast and the Festival pavilions (Core-written) |
| S231 | Mirror: war outcome is a victory for Isenmar | Banner events over the Ashkaar Siege Camp (924) and the Festival pavilions (Core-written) |
| S232 | Mirror: `WAR_BOTH_BROKEN` | Empty pavilions for both kingdoms |

S181–S193 use part of the block previously reserved for per-Warden side-arc steps; S194–S220 remain reserved for those. V122–V123 use two of the reserved chapter counters.

## Chapter step counters (story editor, 2026-11-21; scripts `23_SCRIPT_CH4.md` to `26_SCRIPT_CH7.md`)

From the V122–V140 block reserved for per-chapter scene counters. Events page on `>=`, so a value means "this step and everything before it has played".

| ID | Name | Values |
|---|---|---|
| V124 | CH4_STEP | 0 = on the Hoar Road · 1 = K2 fought on Gullcry Cliffs (with S111) · 2 = met Marisol at the eel stall (comedy scene) · 3 = the strike vote on the Mill Quay (Teo met by day) · 4 = **the Night the Ebb Stopped** played (with S112; V108 goes 1 → 2 → 1 during it) · 5 = the morning after (the quay shows the `:ch4_teo` consequence; the gym opens) · 6 = Gym 3 won · 7 = Larch's confession and Hesper's letter (Chapter 4 closed: the towpath gate east to 580 opens, V102 = 5) |
| V125 | CH5_STEP | 0 = leaving Ebbmouth · 1 = Juno's letter read at Brassfall · 2 = Juno rejoined at the Four Ways on Wallshadow Row · 3 = through Lumen West Gate (GALA INVITATION) · 4 = met Dex on the Lowlight stairs · 5 = the Lowlight blackout fixed (Circuit Gym opens) · 6 = Gym 4 won (the Spire's Gala door opens) · 7 = the Gala started · 8 = the raid: into the service lifts (951) · 9 = the Shatter and the Electivire boss done (with S113, S114; V104 = 1, 608 replaces 181) · 10 = the Lowlight aftermath with Valen done · 11 = testimony given (`:ch5_lowlight_testimony`; S115 with the broadcast) · 12 = Larch's 3 a.m. scene in the vault · 13 = Interlude I done (V101 = 2, V102 = 6) |
| V126 | CH6_STEP | 0 = leaving Lumen · 1 = the Lowlight at dawn (Dex's glass warms; Juno's goodbye) · 2 = the Mandate checkpoint on the Mainline · 3 = arrived at Duneholt's Sandgate · 4 = the deep-works and `:ch6_drillsite` · 5 = Gym 5 won · 6 = the Ossuary door (Sahar's confession) · 7 = the murals (with S116) · 8 = K3 (with S117) · 9 = Juno's letter (chapter closed, V102 = 7) |
| V127 | CH7_STEP | 0 = east on the Marrow Road · 1 = down the Gutterfall (the first descent into Nadir) · 2 = the Infirmary and the Quiet Ward (Wenlow's introductions) · 3 = J2 and the ledger (with S118) · 4 = Wick at the Weeping Fen (with S119) · 5 = Gym 6 won · 6 = the Ward Night · 7 = chapter closed (V102 = 8) |
| V129 | CH8_STEP | 0 = down Leechman's Walk · 1 = Lake Sallow / Scaldwater · 2 = the Pyre Road oath · 3 = Cindervault, "The Hug" · 4 = Hearthguild Hall (envoys, Sigrun) · 5 = Gym 7 won · 6 = the Caldera Crisis (S120, V110) · 7 = the Light Stone · 8 = chestnuts (the slip) · 9 = the herald (S121, V122 = 1) · 10 = chapter closed (`story/29_SCRIPT_CH8.md`) |
| V130 | CH9_STEP | 0 = leaving Cindervault · 1 = Larch's goodbye on the Ashmarch · 2 = down the Long Drop into Ironreach · 3 = the Conclave opens (the roll-call) · 4 = the Open sign-up ("The Bracket") · 5 = K4 won (with S122) · 6 = Gym 8 won (Fly) · 7 = the vote and the attack (the Sable + Brisk tag battle) · 8 = the Mourner unmasked (with S124) · 9 = `:ch9_teo_sable` made · 10 = the aftermath (Rowan led away; S123, V113 = 1, V111 = 1) · 11 = Valen's "Come to Verdance" · 12 = Interlude II done (V101 = 3, V102 = 10) |
| V131 | CH10_STEP | 0 = the Act III opener (Ironreach) · 1 = the Lift Road branch (Black Site / Hollow Sanctuary / refugees) · 2 = Kestrel at the Lift's top station · 3 = arrived in Verdance (S165, V106 = 1) · 4 = the testament (Juno named; the ring) · 5 = the Bride Tree with Juno · 6 = into the Bride Grove · 7 = the Loyal Three done (S127) · 8 = the Plate accepts Juno (S125, V106 = 2, S165 off) · 9 = Gym 9 won (J3) · 10 = Juno's first act and `:ch10_succession_stance` · 11 = the Royal Chase opened (S126) and the Queen's garden · 12 = "Dear Uncle Rowan" (chapter closed, V102 = 11) |
| V128 | SWEETROT_TAKEN | 0–3: Sweetrot offers accepted in Ch7 (the third acceptance is GO_SWEET_TOOTH; NARRATIVE_KEYS §10). Event state, not a choice |

Existing IDs these scripts set: S111 CH4_K2_DONE, S112 CH4_TEO_MET (the night), V108 EBB_STATE (1 stuttering from Ch4 arrival, 2 during the night, back to 1), V114 KESTREL_STAGE = 1 (K2), S113 CH5_GALA_DONE, S114 CH5_SHATTER, S115 CH5_MANDATE, V104 LOWLIGHT_STATE = 1, V119 INTERLUDE_ACTIVE = 1 then 0, S162 EDDA_SMUGGLER (Interlude I), S164 DEX_SHRINE (from Act II), S116 CH6_OSSUARY_DONE, S117 CH6_K3_DONE, S118 CH7_J2_DONE, S119 CH7_WICK_DONE. No new switches: choices stay in Core (`:ch4_kestrel_mourner`, `:ch4_teo`, `:ch5_lowlight_testimony`), and one-off scenes use self switches.

Chapters 9–10 (`27_SCRIPT_CH9.md`, `28_SCRIPT_CH10.md`) set these existing IDs: S122 CH9_K4_DONE, S123 CH9_CONCLAVE_DONE, S124 CH9_MOURNER_UNMASKED, V113 ROWAN_STATUS = 1, V111 NADIR_STATE = 1, V119 INTERLUDE_ACTIVE = 2 then 0 (Interlude II, Rowan), V101 STORY_ACT = 3, S165 THORNGUARD_HEARTGARDEN (on at arrival, off when the Plate accepts Juno), V106 VERDANCE_BLOOM = 1 then 2, S125 CH10_JUNO_WARDEN, S126 CH10_ROYAL_CHASE_OPEN, S127 CH10_LOYAL_THREE_DONE, S171 HOLLOW_SANCTUARY_OPEN or S172 BLACK_SITE_OPEN (the branch), S180 TYPE_NULL_GIFT (`:ch10_null == :take`). They read S182 CAMEO_VENAM_DONE (Venam's Testimony under the Bride Tree) and V345 (Gym 9's hedges, for J3's field stage). No new switches: the choices stay in Core (`:ch9_teo_sable`, `:ch9_rowan_words`, `:ch10_null`, `:ch10_ogre`, `:ch10_succession_stance`), and Ch9 applies the deferred Bond deltas of `:ch6_kestrel_rumor` and `:ch7_ledger` by hand at the unmasking (NARRATIVE_KEYS §4.2).

## Pointer rows: puzzle IDs the story touches (outside 101–300)

These IDs belong to the puzzle blocks (gyms 301–494, GYM_PUZZLES §1; dungeons 501–600, DUNGEON_PUZZLES §0). Their names
and owners live in **`mapgen/flags.yaml`**. They are listed here only because story scripts and story staging read them.
Story events never set them. **A switch and a variable with the same number are different objects** (S305 is not V305).

| ID | Name | Meaning | Owner / where |
|---|---|---|---|
| V305 | CANOPY_WEB_A | Gym 2, the Canopy (131): the bottom Joltik web. 0 = as built (slack), 1 = flipped. The gold Joltik (ledge 3) flips A and B | Loomhouse block (Tamsin); `mapgen/puzzles/canopy.py`, runtime `008_Puzzles_Webs.rb`; script `21_SCRIPT_CH3.md` Map 131 |
| V306 | CANOPY_WEB_B | The middle web, on both strands: the gold Joltik and the blue Joltik (west perch) each flip it | as V305 |
| V307 | CANOPY_WEB_C | The top web. The blue Joltik flips B and C. Solved = A 1, B 0, C 1 (spark both Joltik once each); Pim's reset sets all three to 0 | as V305 |
| V313 | STAGE_AUDIENCE | Gym 1, the Saltmere audience: Saltmere townsfolk met (each counts once) plus Saltmere Trial-board quests done. 0–6 → the Grand Stage starts at stage 1 (Opening Night), 7–13 → stage 2 (Encore), 14+ → stage 3 (Standing Ovation). Map 154's seats fill by it. From 7, your fans cheer for **your** side (your Pokémon bask in the applause), and at Standing Ovation the house cheers you, not Dorian (his troupe loses the bask; his Normal moves stay ×1.5). Pays $150 a head after the win | Playhouse block (Dorian); `plugins/Prismfall Puzzles/007_Puzzles_SaltmereCrowd.rb`, the townsfolk call `pfm_audience(:key)`; script `20_SCRIPT_CH0-2.md` Saltmere |
| S531 | D7_CURTAIN_1 | Dungeon D7, the Rimewood's Frost Loom (562): icicle curtain 1 broken. The left thread cracks curtains 1+2, the middle one 2+3, the right one 3. A thread refreezes any curtain on its line that's already broken | D7 block 531–535; `design/DUNGEON_PUZZLES.md` D7 |
| S532 | D7_CURTAIN_2 | Curtain 2 broken | as S531 |
| S533 | D7_CURTAIN_3 | Curtain 3 broken. All three = the trapper's cache (Snowball ×2) on the east side path. Unique answer: left + right | as S531 |

*Not in this list:* S305–S309 are the Loomhouse's switches (S305–S307 are the Upper Lofts cords α/brass/γ, S308
Granny's Knot), V309 is the Upper Lofts bridge, and 310–314 are the Playhouse backstage. See `mapgen/flags.yaml`.
