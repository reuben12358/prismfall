# NARRATIVE_KEYS — implementation contract (Narrative Systems → Prismfall Core)

> Owner: Narrative Systems. Design rationale: `story/10_CHOICES_ENDINGS.md`. Built on the story lead's crosswalk
> (`design/FLAGS.md` § "Proposed narrative keys") and the act files 04–08. Key names are kept unless the rename table (§13) says otherwise.
> Formats match `plugins/Prismfall Core/012_Narrative_Data.rb`, `014_Conditions.rb` and `015_Festival_Draw.rb`, so the Ruby blocks
> below can be pasted in. Where Core needs a small addition, it's marked **[CORE+]** and specified in §0.

## 0. Conventions and the five small engine additions

- **Symbols.** Choice keys are lowercase symbols (`:ch9_teo_sable`), values are lowercase symbols. Bond, faction, entrant, game-over
  and ending IDs are UPPERCASE. Unset choice = `nil` (Core treats `nil` as 0 in `< >`, and `choice(:x) != :y` is true when unset).
- **Condition strings** use Core's safe subset exactly (§9 of SYSTEMS.md): `bond(:ID) standing(:F) resonance resonance_band choice(:K)
  made(:K) chose(:K, :V) ruin_route ruin_unlocked gameovers_found eliminated(:ID) festival_stage …`, `&& || !`, `== != >= <= > <`, `+ -`.
- **Effects strings** (§4.2) are space-separated tokens `ID+n` / `ID-n`: a Bond ID, a faction ID, or `RES` for Resonance. Bond and
  faction IDs never collide, so a token is unambiguous. Events may apply them by hand today (`pf_bond_add` …).

**[CORE+] requests** (each is a few lines; all are referenced below):
1. **`flag(:NAME)`** → evaluates `DERIVED_FLAGS[:NAME]` (a condition string) and returns true/false. Flags may reference other flags;
   validation must reject cycles.
2. **`tally(:NAME)`** → the number of strings in `TALLIES[:NAME]` that evaluate true (an integer).
3. **`drawn(:STAGE)`** → the entrant ID locked for a Festival stage (`state[:draws][stage]`), `nil` if not drawn yet.
4. **`:effects` on CHOICES** (optional): `pf_choose(key, value)` applies `CHOICE_EFFECTS[key][value]` once, with the
   "X will remember that." toast only when a Bond changes tier. Lets events stop hand-applying deltas.
5. **Festival draw extensions** (§6): `:live => true` on a stage (seed the default at `Festival.start`, resolve the candidate list when
   the stage's battle starts, like Hijack), `EXHIBITION_EXTRAS` (§6.6) and `ARCEUS_VARIANTS` (§6.7). (`:vacates` is withdrawn.) Rev 6 adds `DELEGATIONS` + `seated()` (§6.1)
   and `MATCH_RULES` (§6.5).

---

## 1. Bonds (10)

Range −10..+10. Tiers are what the player sees (Ties page / toasts), never numbers.

```ruby
BOND_DEFAULT = { :min => -10, :max => 10, :start => 0 }
BONDS = {
  :JUNO    => { :name => "Juno",          :start => 2 },
  :KESTREL => { :name => "Kestrel",       :start => -1 },
  :ROWAN   => { :name => "Rowan Ashby" },          # also the Mourner; :MOURNER sample key is retired
  :VOSS    => { :name => "Aurelian Voss", :start => 1 },
  :VALEN   => { :name => "Valen" },
  :ILSA    => { :name => "Ilsa" },
  :SIGRUN  => { :name => "Sigrun" },
  :NYX     => { :name => "Nyx" },
  :MARISOL => { :name => "Marisol" },
  :YSOLDE  => { :name => "Ysolde" }
}
# hostile -10..-5 | wary -4..-2 | neutral -1..1 | friendly 2..4 | close 5..7 | devoted 8..10
BOND_TIERS = [[-10, :hostile], [-4, :wary], [-1, :neutral], [2, :friendly], [5, :close], [8, :devoted]]
BOND_UP_TEXT   = "{1} will remember that."
BOND_DOWN_TEXT = "{1} will remember that."
```
Thresholds used anywhere in this file: `<= -4` (wary floor / Kestrel falls), `<= -2`, `>= 0`, `>= 3`, `>= 4`, `>= 5` (close), `>= 6`, `>= 8` (devoted).
Every other "Bond" mentioned in the act files (Tamsin, Sahar, Brann, Anja, Rook, Corvin) is **not** a tracked Bond: its effect is carried
by the choice key itself and by that Warden's Consent condition (§5). See §13.

## 2. Standing (3)

```ruby
STANDING_DEFAULT = { :min => -10, :max => 10, :start => 0 }
FACTIONS = {
  :HOLLOW   => { :name => "the Hollow" },
  :MERIDIAN => { :name => "the Meridian Concord", :start => 1 },
  :ACCORD   => { :name => "the Accord", :start => 1 }
}
# enemy -10..-6 | distrusted -5..-2 | neutral -1..1 | trusted 2..4 | ally 5..10
STANDING_TIERS = [[-10, :enemy], [-5, :distrusted], [-1, :neutral], [2, :trusted], [5, :ally]]
```
"High Standing" in the act files = `>= 4` (Ch10 Hollow Sanctuary / Meridian Black Site branches; Ch20 Accord Archive branch).
"Low" = `<= -2`. "Broken" (the Hollow) = `< 0`.

## 3. Resonance

Unchanged from Core: one integer −10 (Ruin) .. +10 (Harmony), start 0.
```ruby
RESONANCE_BANDS = [[-10, :ruin], [-5, :ruin_leaning], [-1, :balanced], [2, :harmony_leaning], [6, :harmony]]
# ruin -10..-6 | ruin_leaning -5..-2 | balanced -1..1 | harmony_leaning 2..5 | harmony 6..10
```
Story checks: Kyogre's last bar calms at `resonance >= 2` (Ch11); Celestine's Consent `>= 2`; Good ending `>= 2`;
Sigrun drawn into your QF at `<= -3`; Ruin "war" Arceus and the main-route Unmake option at `<= -6`; harmony battle buff at `>= 6`.

---

## 4. Choices (48 keys; MAJOR branch decisions are marked in each description)

`:once => true` for all of them (a decision can't be re-made). "Gate" = when the prompt is offered (events check it); a value that
is a game-over trigger is not a stored value (the GO fires instead). Values marked *(only if …)* are hidden otherwise.

```ruby
CHOICES = {
  # ---- Prologue / Act I
  # Revision 14 swapped Saltmere (now Ch2, Gym 1) and Briarwick (now Ch3, Gym 2). Key names keep their old chapter prefixes:
  # IDs never renumber. Only the descriptions and the listing order changed.
  :pro_fellowship         => { :values => [:accept, :decline, :silent], :once => true, :description => "P: Voss's Meridian Fellowship card" },
  :ch3_juno_talk          => { :values => [:told, :deflect, :silent], :once => true, :description => "Ch2: tell Juno about the NULL scan (Saltmere breakwater)" },
  :ch2_tamsin             => { :values => [:expose, :help_confess, :keep_secret], :once => true, :description => "Ch3: Tamsin's secret Lattice contract" },
  :ch2_matriarch          => { :values => [:soothe, :silence], :once => true, :description => "Ch3: the beaten Glass Matriarch - wait it out, or force the Imprint out" },
  :ch4_kestrel_mourner    => { :values => [:kind, :blunt, :silent], :once => true, :description => "Ch4: is the Mourner his mother?" },
  :ch4_teo                => { :values => [:report, :keep_secret, :confront], :once => true, :description => "Ch4: Marisol tipping off Teo's cell" },
  :ch5_lowlight_testimony => { :values => [:mourner, :someone_else, :unknown], :once => true, :description => "Ch5: what the PC tells the Directorate" },
  # ---- Act II
  :ch6_drillsite          => { :values => [:hollow, :directorate, :sanctuary], :once => true, :description => "Ch6: the drill-site children" },
  :ch6_kestrel_rumor      => { :values => [:encourage, :warn, :silent], :once => true, :description => "Ch6: K3, the Mourner rumor" },
  :ch7_ledger             => { :values => [:name_him, :reassure, :ask_corvin], :once => true, :description => "Ch7: J2, Rowan's name in Corvin's ledger" },
  :ch8_caldera            => { :values => [:vent, :dampers, :shutdown], :once => true, :description => "Ch8: the Caldera Crisis" },
  :ch8_lightstone         => { :values => [:hearthguild, :wyrmrest, :dominar], :once => true, :description => "Ch8: who keeps the Light Stone" },
  :ch9_teo_sable          => { :values => [:save_teo, :chase_sable], :once => true, :description => "Ch9 (MAJOR): Teo or Sable's comm-device" },
  :ch9_rowan_words        => { :values => [:why, :look_after, :silent], :once => true, :description => "Ch9: answer to Rowan as he's led away" },
  # ---- Act III
  :ch10_null              => { :values => [:take, :leave], :once => true, :description => "Ch10 (Black Site branch only): take the Type: Null" },
  :ch10_ogre              => { :values => [:ogre, :hesitate], :once => true, :description => "Ch10: the Ogre or the Loyal Three (:three = GO_LOYAL)" },
  :ch10_succession_stance => { :values => [:accord, :kingdoms, :nobody], :once => true, :description => "Ch10: who should own the Plates" },
  :ch11_anja              => { :values => [:expose, :let_confess], :once => true, :description => "Ch11: Anja's suppressed readings" },
  :ch11_strike            => { :values => [:stand, :mediate], :once => true, :description => "Ch11 transit: the Ebbmouth Strike picket" },
  :ch12_letter            => { :values => [:keep, :send, :burn], :once => true, :description => "Ch12: Morwen's dead letter to 'I.'" },
  :ch13_remember          => { :values => [:show, :scared, :not_yet], :once => true, :description => "Ch13: the PC's first authored line, in the Mindscape" },
  :ch13_kaito             => { :values => [:encourage, :spare], :once => true, :description => "Ch13 (MAJOR): Kaito's Marrowgate testimony" },
  :ch13_rowan_testimony   => { :values => [:condemn, :mercy, :refuse], :once => true, :description => "Ch13 (MAJOR): the PC's testimony at Rowan's tribunal" },
  :ch13_fault             => { :values => [:rowan, :marchetti], :once => true, :description => "Ch13 (MAJOR, NEW): the Fault - pull Rowan or Marchetti out" },
  :sq_doctors_cell        => { :values => [:freed, :failed], :once => true, :description => "Side quest 'The Doctor's Cell' (Ch11-13) outcome" },
  # ---- Act IV
  :ch14_telemetry         => { :values => [:destroy, :sabotage, :leave], :once => true, :description => "Ch14 (MAJOR): the badge-case transmitter" },
  :ch14_marchetti         => { :values => [:show_evidence, :none], :once => true, :description => "Ch14: show Marchetti the Splitter Casing / comm-device" },
  :ch15_kestrel           => { :values => [:sorry, :she_chose, :resolve], :once => true, :description => "Ch15: the PC's authored line after K6" },
  :ch15_look_back         => { :values => [:yes, :no], :once => true, :description => "Ch15 (only if ruin_unlocked): look back through the Reverse Depths' glass" },
  :ch16_zekrom            => { :values => [:freed], :once => true, :description => "Ch16: outcome of the Zekrom boss (ZEKROM_FREED)" },
  :ch16_rook              => { :values => [:leak_now, :hold], :once => true, :description => "Ch16: Rook's Spire footage" },
  :ch16_magnus            => { :values => [:expose, :conscience], :once => true, :description => "Ch16 (MAJOR): Magnus and the Arbiter blueprints" },
  :ch17_nyx               => { :values => [:trade, :refuse], :once => true, :description => "Ch17: Nyx's bargain (the PC's secret for the arena schematics)" },
  :ch17_voss_offer        => { :values => [:refuse, :feign, :accept], :once => true, :description => "Ch17 (MAJOR): Voss's offer in the Sun Court" },
  # ---- Act V
  :ch18_kestrel_ring      => { :values => [:give_now, :keep], :once => true, :description => "Ch18 (MAJOR): Morwen's Ring after K7" },
  :ch19_oath              => { :values => [:return, :keep, :open, :ruin], :once => true, :description => "Ch19 (MAJOR): the PC's oath at the Draco brazier (:ruin only if resonance <= -2)" },
  :ch19_dominar           => { :values => [:swayed, :failed], :once => true, :description => "Ch19: petition to the Dominar (DOMINAR_SWAYED)" },
  :ch20_envoy             => { :values => [:proof, :plea], :once => true, :description => "Ch20: what the PC brings Envoy Okoro" },
  :ch20_calla             => { :values => [:shelter, :send_back, :turn_away], :once => true, :description => "Ch20 (NEW): Calla Wren defects at the Night of Masques" },
  :ch20_audience          => { :values => [:return, :keep, :refuse], :once => true, :description => "Ch20 (MAJOR): the PC's answer to Valen's confession" },
  :sq_little_owl          => { :values => [:reconciled, :refused], :once => true, :description => "Ilsa's side quest culmination (ILSA_RECONCILED)" },
  :ch21_crown             => { :values => [:kneel, :stand, :step_back], :once => true, :description => "Ch21: the Coronation (flavor)" },
  :ch21_hand              => { :values => [:take, :refuse], :once => true, :description => "Ch21 (only if VOSS_ACCEPTED): take Voss's hand at the hijack" },
  :ch21_reach_kestrel     => { :values => [:reach, :burn, :let_go], :once => true, :description => "Ch21 (only if KESTREL_FALLEN): Kestrel harnessed in the Engine" },
  :ch21_spare_voss        => { :values => [:shield, :let_judge], :once => true, :description => "Ch21: Arceus's Judgment strikes the hijacker (PC_SPARED_VOSS)" },
  :ch21_final             => { :values => [:return, :keep, :unmake, :concord, :borrowed], :once => true, :description => "Ch21: the final decision, spoken aloud" },
  # ---- Ruin Route
  :ruin_voss              => { :values => [:spare, :abandon], :once => true, :description => "R7: Voss kneels to Aurelius's reflection" },
  :ruin_walk              => { :values => [:me, :reflection], :once => true, :description => "R7: who walks out of the Glass" }
}
```

### 4.1 Gates (when a value is offered)

| Key | Gate |
|---|---|
| `:ch10_null` | Black Site branch only: `standing(:MERIDIAN) >= 4` (takes priority over the Hollow branch if both are high). |
| `:ch13_rowan_testimony` | always; `:mercy` is the only route to R16 Rowan. |
| `:ch14_marchetti` `:show_evidence` | holds the Splitter Casing (always found in Ch12) or the comm-device (`chose(:ch9_teo_sable, :chase_sable)`). |
| `:ch15_look_back` | only if `ruin_unlocked`. `:yes` calls `Prismfall.start_ruin_route` (§11). |
| `:ch19_oath` `:ruin` | only if `resonance <= -2`. The hidden "Whatever you want to hear." is `GO_LIARS_PYRE` (always offered; see §10). |
| `:ch20_envoy` `:proof` | the PC holds at least two of: Larch Papers (Ch12), Arbiter Blueprints (Ch16), testimony that the Fixed still dream (any one of: Teo's, if `TEO_SAVED`; Corvin's Quiet Ward records, if `CORVIN_FREED`; Venam's Testimony from her optional sidequest). |
| `:ch20_calla` | only if `choice(:ch16_rook) == :hold` OR `choice(:ch16_magnus) == :conscience` (Calla only defects if someone inside is already moving). |
| `:sq_little_owl` | the quest's earlier steps need `bond(:ILSA) >= 3` by Ch18. `:reconciled` needs `bond(:ILSA) >= 4` at the final step, else the event records `:refused`. |
| `:ch21_hand` | only if `flag(:VOSS_ACCEPTED)`. Without it, taking the hand is `GO_HIS_HAND`. |
| `:ch21_reach_kestrel` `:reach` | `flag(:CAN_REACH_KESTREL)`: `choice(:ch12_letter)` is `:keep` or `:send` (Morwen's own words; with `:send` he has them too) OR `bond(:KESTREL) >= 0`. The ring alone no longer counts: on the Fallen path the PC always has it. |
| `:ch21_final` | `:return` `:keep` always; `:unmake` if `flag(:UNMAKE_OPEN)`; `:concord` if `flag(:CONCORD_OPEN)`; `:borrowed` if `flag(:BORROWED_OPEN)`. |

### 4.2 Effects (transcribe as `CHOICE_EFFECTS`, or apply by hand)

Deferred deltas (applied by a later event that reads the choice) are listed after "→".

```ruby
CHOICE_EFFECTS = {
  :pro_fellowship         => { :accept => "MERIDIAN+2 VOSS+1", :decline => "VOSS+2", :silent => "MERIDIAN+1" },
  :ch3_juno_talk          => { :told => "JUNO+2", :deflect => "JUNO-1", :silent => "" },                  # Ch2
  :ch2_tamsin             => { :expose => "HOLLOW+1 ACCORD+1 MERIDIAN-1", :help_confess => "ACCORD+1", :keep_secret => "MERIDIAN+1" },   # Ch3
  :ch2_matriarch          => { :soothe => "RES+1", :silence => "RES-2 ACCORD+1" },                          # Ch3
  :ch4_kestrel_mourner    => { :kind => "KESTREL+1", :blunt => "KESTREL-2", :silent => "" },
  :ch4_teo                => { :report => "MERIDIAN+2 HOLLOW-2 MARISOL-4", :keep_secret => "MARISOL+2 HOLLOW+1", :confront => "MARISOL+3" },
  :ch5_lowlight_testimony => { :mourner => "MERIDIAN+1 HOLLOW-1 VOSS+1", :someone_else => "HOLLOW+1 MERIDIAN-1", :unknown => "" },
  :ch6_drillsite          => { :hollow => "HOLLOW+2 MERIDIAN-2", :directorate => "MERIDIAN+2 VOSS+1", :sanctuary => "ACCORD+2" },
  :ch6_kestrel_rumor      => { :encourage => "KESTREL+2", :warn => "KESTREL-1", :silent => "" },     # -> Ch9 unmasking: encourage KESTREL-3, warn KESTREL+2
  :ch7_ledger             => { :name_him => "JUNO-3", :reassure => "JUNO+2", :ask_corvin => "" },     # -> Ch9 unmasking: name_him JUNO+2, reassure JUNO-2
  :ch8_caldera            => { :vent => "HOLLOW+2 MERIDIAN-1 RES+1", :dampers => "MERIDIAN+2 VOSS+1 RES-1", :shutdown => "ACCORD+2 MERIDIAN-3" },
  :ch8_lightstone         => { :hearthguild => "", :wyrmrest => "SIGRUN+2 ACCORD+1", :dominar => "SIGRUN-2 ACCORD-1" },
  :ch9_teo_sable          => { :save_teo => "MARISOL+4 HOLLOW+1 RES+1", :chase_sable => "MARISOL-4 ACCORD+1 RES-1" },
  :ch9_rowan_words        => { :why => "", :look_after => "ROWAN+2 JUNO+1", :silent => "ROWAN+1" },
  :ch10_null              => { :take => "VOSS+2 MERIDIAN+1", :leave => "" },
  :ch10_ogre              => { :ogre => "RES+1 JUNO+1", :hesitate => "RES-1" },
  :ch10_succession_stance => { :accord => "ACCORD+1 VALEN+2", :kingdoms => "ACCORD-1 VALEN-1", :nobody => "HOLLOW+1 VALEN-1 RES+1" },
  :ch11_anja              => { :expose => "ACCORD+1 MERIDIAN-1", :let_confess => "" },
  :ch11_strike            => { :stand => "MARISOL+2 MERIDIAN-1", :mediate => "MARISOL-1 MERIDIAN+1" },  # stand: +1 more MARISOL if Teo died
  :ch12_letter            => { :keep => "", :send => "KESTREL+3 YSOLDE+1", :burn => "RES-2 YSOLDE-2" },
  :ch13_remember          => { :show => "ILSA+1 RES+1", :scared => "ILSA+2 RES+2", :not_yet => "ILSA+1" },
  :ch13_kaito             => { :encourage => "ACCORD-2 VALEN-2 ILSA+2 HOLLOW+1", :spare => "ACCORD+1 VALEN+1" },
  :ch13_rowan_testimony   => { :condemn => "ROWAN-4 JUNO-3 ACCORD+2 HOLLOW-2 VALEN+1", :mercy => "ROWAN+3 JUNO+3 HOLLOW+2 ACCORD-1", :refuse => "ROWAN-1 ILSA+1" },
  :ch13_fault             => { :rowan => "ROWAN+3 JUNO+2 HOLLOW+1", :marchetti => "JUNO-4 HOLLOW-2 MERIDIAN+1" },
  :sq_doctors_cell        => { :freed => "HOLLOW+1", :failed => "" },
  :ch14_telemetry         => { :destroy => "VOSS-3 MERIDIAN-2", :sabotage => "", :leave => "" },
  :ch14_marchetti         => { :show_evidence => "MERIDIAN-1", :none => "" },
  :ch15_kestrel           => { :sorry => "KESTREL+1 YSOLDE+1", :she_chose => "KESTREL-2", :resolve => "KESTREL+2 YSOLDE+2 RES+2" },  # sorry -> SF (if not Fallen): KESTREL+3
  :ch15_look_back         => { :yes => "", :no => "" },
  :ch16_zekrom            => { :freed => "RES+1" },
  :ch16_rook              => { :leak_now => "MERIDIAN-2 HOLLOW+1", :hold => "" },
  :ch16_magnus            => { :expose => "ACCORD+1 MERIDIAN-2 VOSS-1", :conscience => "" },
  :ch17_nyx               => { :trade => "NYX+4", :refuse => "NYX-2" },
  :ch17_voss_offer        => { :refuse => "VOSS-2", :feign => "VOSS+2", :accept => "VOSS+3 MERIDIAN+3 NYX-2 RES-1" },
  :ch18_kestrel_ring      => { :give_now => "KESTREL+3 YSOLDE+2", :keep => "" },
  :ch19_oath              => { :return => "SIGRUN+3 RES+2", :keep => "SIGRUN-1 VALEN+3 ACCORD+1", :open => "SIGRUN+2 RES+1", :ruin => "SIGRUN-3 RES-3" },
  :ch19_dominar           => { :swayed => "SIGRUN+1", :failed => "" },
  :ch20_envoy             => { :proof => "", :plea => "" },
  :ch20_calla             => { :shelter => "RES+1", :send_back => "RES-2", :turn_away => "MERIDIAN+1" },
  :ch20_audience          => { :return => "VALEN+2 RES+1", :keep => "VALEN+3", :refuse => "VALEN+1" },
  :sq_little_owl          => { :reconciled => "ILSA+3 VALEN+3", :refused => "ILSA+1" },
  :ch21_crown             => { :kneel => "VALEN+1", :stand => "", :step_back => "RES+1" },
  :ch21_hand              => { :take => "", :refuse => "VOSS-4" },
  :ch21_reach_kestrel     => { :reach => "KESTREL+3 YSOLDE+2 RES+1", :burn => "KESTREL+1 RES-3", :let_go => "YSOLDE-5" },
  :ch21_spare_voss        => { :shield => "RES+2", :let_judge => "RES-1" },
  :ch21_final             => { :return => "", :keep => "", :unmake => "", :concord => "", :borrowed => "" },
  :ruin_voss              => { :spare => "VOSS+3", :abandon => "VOSS-3" },
  :ruin_walk              => { :me => "", :reflection => "" }
}
```
Quiet Hours relationship scenes (10_CHOICES_ENDINGS §7.1) add `+1` to their Bond when first reaching `friendly` and `close`.

### 4.3 The Ashkaar–Isenmar War (SPINE Revision 6) — proposed keys; the story lead places the chapters (Act III–IV)
```ruby
CHOICES.merge!({
  :war_warning   => { :values => [:warn_isenmar, :warn_ashkaar, :warn_both, :silent], :once => true, :description => "War 1: from Frostfang Pass the PC sees the Dominar's legions massing on Ossaria's western dunes before anyone else knows" },
  :war_convoy    => { :values => [:relief, :arms, :refuse], :once => true, :description => "War 2: Marisol's siege-runners ask the Unimprinted to walk a sledge convoy from Duneholt through the Steamline into besieged Skaldfast: food, or harpoon-guns" },
  :war_prisoner  => { :values => [:free, :exchange, :leave], :once => true, :description => "War 3: a captured Warden (Anja, held in the Ashkaar Siege Camp) and the Dominar's nephew (held by the Thane in Skaldfast)" },
  :war_legend    => { :values => [:calm_kyogre, :wake_reshiram, :neither], :once => true, :description => "War 4: each side begs the PC to bring its legend to the front" },
  :war_climax    => { :values => [:stand_between, :back_ashkaar, :back_isenmar], :once => true, :description => "War 5 (MAJOR): the beam clash on the Glass Dunes" },
  :war_terms     => { :values => [:mercy, :reparations, :occupation], :once => true, :description => "War 6: what the PC argues for at the armistice table in Skaldfast (only if one side won)" },
  # the story lead's two Blessing keys (14_WAR_AND_BLESSING Part A)
  :ch20_colors   => { :values => [:elowen, :zenith, :nadir, :unsworn], :once => true, :description => "Ch20 Day 0: whose colors the Unimprinted challenger wears (flavor + one delta)" },
  :ch21_boon     => { :values => [:end_reparations, :seat_nadir, :dissolve_seat], :once => true, :description => "Ch21: the Blessed's one binding decree. Asked after :ch21_final in the Return, Keep and Borrowed outcomes, BEFORE Prismfall.trigger_ending" }
})
CHOICE_EFFECTS.merge!({
  :war_warning  => { :warn_isenmar => "MARISOL+2 SIGRUN-2", :warn_ashkaar => "SIGRUN+1 MARISOL-2", :warn_both => "ACCORD+2 SIGRUN+1 MARISOL+1", :silent => "RES-1" },
  :war_convoy   => { :relief => "MARISOL+2 RES+1", :arms => "MARISOL+3 SIGRUN-2 RES-1", :refuse => "MARISOL-2" },
  :war_prisoner => { :free => "RES+1 ACCORD-1", :exchange => "ACCORD+2", :leave => "RES-1" },
  :war_legend   => { :calm_kyogre => "RES+2 MARISOL-1", :wake_reshiram => "SIGRUN+1 RES-2", :neither => "" },
  :war_climax   => { :stand_between => "RES+2 ACCORD+1", :back_ashkaar => "SIGRUN+2 MARISOL-4 RES-1", :back_isenmar => "MARISOL+3 SIGRUN-4 RES-1" },
  :war_terms    => { :mercy => "RES+2", :reparations => "ACCORD+1", :occupation => "RES-2 ACCORD-1" },
  :ch20_colors  => { :elowen => "ACCORD-1", :zenith => "MERIDIAN+1", :nadir => "HOLLOW+1", :unsworn => "RES+1" },
  :ch21_boon    => { :end_reparations => "", :seat_nadir => "", :dissolve_seat => "" }
})
TALLIES[:WAR_TRUST] = [                       # what both armies have seen the PC do
  "choice(:war_warning) == :warn_both",
  "choice(:war_convoy) == :relief",
  "choice(:war_prisoner) != :leave",
  "choice(:war_legend) == :calm_kyogre || choice(:war_legend) == :neither",
  "bond(:SIGRUN) >= 4",
  "bond(:MARISOL) >= 3"
]
DERIVED_FLAGS.merge!({
  :WAR_STOPPED       => "choice(:war_climax) == :stand_between && tally(:WAR_TRUST) >= 4",   # both lines hold fire; the beams meet over the PC and part
  :WAR_BOTH_BROKEN   => "choice(:war_climax) == :stand_between && tally(:WAR_TRUST) < 4",    # nobody listens; the clash detonates and breaks both armies
  :WAR_ASHKAAR_WON   => "choice(:war_climax) == :back_ashkaar",
  :WAR_ISENMAR_WON   => "choice(:war_climax) == :back_isenmar",
  :WAR_OCCUPATION    => "choice(:war_terms) == :occupation",
  :BOON_LIFTS_OCCUPATION => "choice(:ch21_boon) == :end_reparations",   # the Blessed can undo their own armistice terms
  :ISENMAR_EMBITTERED => "flag(:WAR_BOTH_BROKEN) || (flag(:WAR_ASHKAAR_WON) && choice(:war_terms) != :mercy)",
  :ASHKAAR_EMBITTERED => "flag(:WAR_BOTH_BROKEN) || (flag(:WAR_ISENMAR_WON) && choice(:war_terms) != :mercy)"
})
```
- **Cutscene variants** (Prismfall Cutscenes): the climax always contains the beam clash, on the Glass Dunes in Ossaria (Rev 18). It is Reshiram's
  Blue Flare vs Kyogre's Origin Pulse out of the flood-sea Kyogre drags into the desert, unless `:war_legend` is `:neither`, the one value that keeps both
  legends away; then there is no flood, and it is Sigrun's Salamence Draco Meteor vs Anja's Mamoswine/Marisol's Gyarados Hydro Pump–Blizzard.
  Ending frame by flag: `WAR_STOPPED` (beams part around the PC), `WAR_BOTH_BROKEN` (white-out, both lines gone), a victor's banner otherwise.
- **Consent:** `WARDEN_CONSENT` entries 3 (Marisol) and 10 (Anja) gain `&& !flag(:ISENMAR_EMBITTERED)`; entries 7 (Brann) and 18 (Sigrun) gain
  `&& !flag(:ASHKAAR_EMBITTERED)`. A beaten, unforgiven kingdom won't give up the last thing it holds. (Applied in §5's array below this note:
  Core should transcribe the four amended strings.)
- **Endings:** `END_UNFINISHED` also fires on `flag(:WAR_OCCUPATION)` (Arceus won't bless a land with a boot on its neck) unless the Boon ends it;
  `:ch21_boon` otherwise only picks epilogue slides (reparations ended / Nadir seated on every council / the Seat dissolved); `DOMINAR_SWAYED` is false
  if `WAR_ISENMAR_WON` without `:mercy` (enforced in the §5 flag); `LANTERN_HOLDS`-style hijack help: the winning side's (or, if stopped, both sides') hosts and legions defend Crownhaven.

---

## 5. Derived flags and tallies [CORE+ `flag()` / `tally()`]

Every outcome name the act files use (`TEO_SAVED`, `MAGNUS_KEPT_FAITH` …) is a **derived flag**, never stored. FLAGS.md's mirror
switches S221–S228 are written from these by Core (`S221 = flag(:TEO_SAVED)` etc.; S228 = `flag(:KESTREL_REDEEMED)`).

```ruby
DERIVED_FLAGS = {
  # Act I-III outcomes
  :TAMSIN_PUBLIC_CONFESSION => "choice(:ch2_tamsin) == :expose",
  :TEO_SAVED                => "choice(:ch9_teo_sable) == :save_teo",
  :IRONREACH_EVIDENCE       => "choice(:ch9_teo_sable) == :chase_sable",
  :KROLL_EXPOSED_CH13       => "flag(:IRONREACH_EVIDENCE)",            # public unmasking at the tribunal needs the comm-device
  :OGERPON_TRUSTED          => "choice(:ch10_ogre) == :ogre",
  :ANJA_EXPOSED             => "choice(:ch11_anja) == :expose",
  :KAITO_TESTIFIED          => "choice(:ch13_kaito) == :encourage",
  :ROWAN_ALIVE              => "choice(:ch13_fault) != :marchetti",
  :ROWAN_RADICAL            => "flag(:ROWAN_ALIVE) && choice(:ch13_rowan_testimony) == :condemn && bond(:ROWAN) <= -2",
  :CORVIN_FREED             => "choice(:sq_doctors_cell) == :freed",
  # Act IV
  :MARCHETTI_TURNED         => "choice(:ch13_fault) == :marchetti || choice(:ch14_marchetti) == :show_evidence",
  :TELEMETRY_SABOTAGED      => "choice(:ch14_telemetry) == :sabotage",
  :ZEKROM_FREED             => "made(:ch16_zekrom)",
  :MAGNUS_EXPOSED           => "choice(:ch16_magnus) == :expose",
  :MAGNUS_KEPT_FAITH        => "choice(:ch16_magnus) == :conscience",
  :ROOK_CUTS_GRID           => "choice(:ch16_rook) == :hold",          # a leaked Rook is fired and loses grid access
  :NYX_BARGAIN_TAKEN        => "choice(:ch17_nyx) == :trade",
  :NYX_PRECISE              => "flag(:NYX_BARGAIN_TAKEN)",
  :VOSS_FEIGNED             => "choice(:ch17_voss_offer) == :feign",
  :VOSS_ACCEPTED            => "choice(:ch17_voss_offer) == :accept",
  :VOSS_DISCREDITED         => "flag(:MAGNUS_EXPOSED) && made(:ch16_rook)", # Rook's leak + Night of Masques + Magnus exposed
  # Kestrel
  :KESTREL_FALLEN           => "choice(:ch18_kestrel_ring) != :give_now && choice(:ch15_kestrel) != :she_chose && (bond(:KESTREL) <= -4 || (bond(:KESTREL) <= 1 && (choice(:ch15_kestrel) == :sorry || standing(:MERIDIAN) >= 5)))",
  :KESTREL_REDEEMED         => "!flag(:KESTREL_FALLEN)",
  :KESTREL_LOST             => "flag(:KESTREL_FALLEN) && choice(:ch21_reach_kestrel) == :let_go",
  :KESTREL_YSOLDE_RECONCILED => "!flag(:KESTREL_FALLEN) && bond(:KESTREL) >= 5 && bond(:YSOLDE) >= 4",
  :KESTREL_BEARS            => "!flag(:KESTREL_FALLEN) && bond(:KESTREL) >= 8",
  :SIGRUN_BEARS             => "!flag(:KESTREL_BEARS) && bond(:SIGRUN) >= 6",
  :KESTREL_ACCEPTED_SEAT    => "flag(:KESTREL_YSOLDE_RECONCILED) && !flag(:KESTREL_LOST) && !(choice(:ch21_final) == :borrowed && flag(:KESTREL_BEARS))",
  # Act V
  :DOMINAR_SWAYED           => "choice(:ch19_dominar) == :swayed && !(flag(:WAR_ISENMAR_WON) && choice(:war_terms) != :mercy)",
  :ENVOY_PERSUADED          => "choice(:ch20_envoy) == :proof",
  :CALLA_ALIVE              => "choice(:ch20_calla) != :send_back",
  :ILSA_RECONCILED          => "choice(:sq_little_owl) == :reconciled",
  :VALEN_COLLAPSED          => "!flag(:ILSA_RECONCILED) && choice(:ch20_audience) == :refuse && bond(:VALEN) <= -2 && choice(:ch14_telemetry) == :leave",
  :LANTERN_HOLDS            => "standing(:HOLLOW) >= 0 && (flag(:ROWAN_ALIVE) || flag(:TEO_SAVED))",
  :PC_SPARED_VOSS           => "choice(:ch21_spare_voss) == :shield && !flag(:VOSS_DISCREDITED)",
  :VOSS_REDEEMED            => "flag(:VOSS_DISCREDITED) && bond(:VOSS) >= 0",  # Quent hijacks; Voss comes down from the gallery
  # Engine and endings
  :ENGINE_CALIBRATED        => "choice(:ch14_telemetry) == :leave && choice(:ch16_magnus) != :conscience && tally(:ENGINE_BREAKS) <= 3",
  :CONCORD_OPEN             => "!ruin_route && (flag(:VOSS_ACCEPTED) || choice(:ch16_magnus) != :conscience)",
  :BORROWED_OPEN            => "!ruin_route && (flag(:KESTREL_BEARS) || flag(:SIGRUN_BEARS))",
  :UNMAKE_OPEN              => "ruin_route || resonance <= -6 || (standing(:HOLLOW) >= 4 && (flag(:ROWAN_RADICAL) || !flag(:KROLL_EXPOSED_CH13)))",
  :HARMONY_BUFF             => "resonance >= 6",
  :ZYGARDE_CHOOSES          => "bond(:VALEN) >= 3 || flag(:ILSA_RECONCILED)",
  :JUNO_ESTRANGED           => "bond(:JUNO) <= -5"   # Ch11: she travels apart; the Thaw partner is Anja
}

# Wardens' Consent, gym order (index = gym - 1). A Warden who doesn't consent refuses to release their Plate in the Arceus fight.
# Revision 14: Dorian is Gym 1 and Tamsin Gym 2, so their two rows swapped places (must match Core's Prismfall::GYMS order).
WARDEN_CONSENT = [
  "choice(:ch5_lowlight_testimony) != :mourner",                  #  1 Dorian  - you told the official story on record; he keeps the lie he knows
  "choice(:ch2_tamsin) != :keep_secret",                          #  2 Tamsin  - the pylon still drains Briarwick; she can't afford to let go
  "(flag(:TEO_SAVED) || bond(:MARISOL) >= 3) && !flag(:ISENMAR_EMBITTERED)",                    #  3 Marisol
  "flag(:ROOK_CUTS_GRID) || flag(:MARCHETTI_TURNED)",             #  4 Rook    - the Zap Plate is in Meridian's vault; he can only release what he can reach
  "choice(:ch6_drillsite) != :directorate",                       #  5 Sahar
  "flag(:CORVIN_FREED)",                                          #  6 Corvin  - otherwise a Choir porter carries his Plate and can't release it
  "choice(:ch8_lightstone) != :dominar && !flag(:ASHKAAR_EMBITTERED)",                      #  7 Brann
  "flag(:KAITO_TESTIFIED)",                                       #  8 Kaito   - a man who never confessed can't let go
  "bond(:JUNO) >= 0",                                             #  9 Juno
  "choice(:ch11_anja) == :let_confess && !flag(:ISENMAR_EMBITTERED)",                      # 10 Anja    - "Rimeholt drowns without it."
  "choice(:ch12_letter) != :burn",                                # 11 Odessa  - you burned a dead letter
  "flag(:ILSA_RECONCILED) || bond(:ILSA) >= 5",                   # 12 Ilsa
  "choice(:ch14_telemetry) != :leave",                            # 13 Bastian - you walked a Meridian beacon into his seams
  "!flag(:KESTREL_FALLEN) || choice(:ch21_reach_kestrel) == :reach", # 14 Ysolde
  "flag(:MAGNUS_KEPT_FAITH)",                                     # 15 Magnus  - "I won't hand my city's future to a god."
  "flag(:NYX_BARGAIN_TAKEN) || bond(:NYX) >= 4",                  # 16 Nyx
  "resonance >= 2",                                               # 17 Celestine - she hears which key you sing in
  "choice(:ch19_oath) != :keep && choice(:ch19_oath) != :ruin && !flag(:ASHKAAR_EMBITTERED)"    # 18 Sigrun
]

TALLIES = {
  :CONSENT       => WARDEN_CONSENT,
  :ENGINE_BREAKS => [                                             # Larch's Engine board in Ch20 shows these as lights
    "choice(:ch14_telemetry) != :leave",                          # destroyed or sabotaged: under-calibrated
    "flag(:TELEMETRY_SABOTAGED)",                                 # sabotage counts twice (the strongest single weakening)
    "flag(:ZEKROM_FREED)",
    "flag(:MAGNUS_KEPT_FAITH)",
    "flag(:ROOK_CUTS_GRID)",
    "flag(:NYX_PRECISE)",
    "chose(:ch20_calla, :shelter) || chose(:ch20_calla, :send_back)",
    "chose(:ch20_calla, :send_back)",                             # she went back for the full set, and died for it
    "flag(:MARCHETTI_TURNED)",
    "flag(:LANTERN_HOLDS)",
    "!flag(:KESTREL_LOST)"
  ],
  :WARM_BONDS    => ["bond(:JUNO) >= 5", "bond(:KESTREL) >= 5", "bond(:ROWAN) >= 5", "bond(:VOSS) >= 5", "bond(:VALEN) >= 5",
                     "bond(:ILSA) >= 5", "bond(:SIGRUN) >= 5", "bond(:NYX) >= 5", "bond(:MARISOL) >= 5", "bond(:YSOLDE) >= 5"]
}
```
`tally(:CONSENT) >= 12` is the Good-ending threshold. `ENGINE_CALIBRATED` is evaluated when the True Finale starts (all inputs are known by then).

---

## 6. Festival draw (SPINE Revisions 5–6: kingdom delegations, story-met characters only)

The Festival chooses who receives **Arceus's Blessing**. Sixteen seats: the Unimprinted challenger (the PC) and **fifteen delegates**, two per kingdom
plus the Accord's Sovereign. Who each kingdom sends is decided by the player's choices (§6.1). Every possible opponent is story-met (Rev 5); the
Rev-4 outsiders are retired. Order of operations at `Festival.start`: **(1)** resolve delegations into seats, **(2)** run the draw (§6.3) over the
seated entrants, **(3)** resolve NPC matches by `MATCH_RULES` (§6.5).

### 6.1 Delegations [CORE+ `DELEGATIONS`: per seat, the first candidate whose condition holds and who isn't seated yet]
```ruby
DERIVED_FLAGS.merge!({
  :KESTREL_FOR_ANTUMBRA => "flag(:KESTREL_REDEEMED) && (choice(:ch18_kestrel_ring) == :give_now || bond(:YSOLDE) >= 4)",  # Gravenmoor names him; else he's Meridian's sponsored champion for Zenith
  :ISENMAR_ONE_SEAT     => "flag(:WAR_ASHKAAR_WON) || flag(:WAR_BOTH_BROKEN)",
  :ASHKAAR_ONE_SEAT     => "flag(:WAR_ISENMAR_WON) || flag(:WAR_BOTH_BROKEN)",
  :ISENMAR_KEEPS_ANJA   => "flag(:ANJA_EXPOSED) && (flag(:TEO_SAVED) || bond(:MARISOL) > 2)"   # the one with the open account with you stays
})
DELEGATIONS = {   # seat => ordered [entrant, condition]; nil = always
  :ELOWEN_A   => [[:JUNO, nil]],                                    # Verdance's Warden (she may give the seat to Rowan: R16 draw)
  :ELOWEN_B   => [[:CELESTINE, nil]],                               # Gloaming; the Queen has no say over a Warden who cannot lie
  :ANTUMBRA_A => [[:YSOLDE, nil]],
  :ANTUMBRA_B => [[:KESTREL, "flag(:KESTREL_FOR_ANTUMBRA)"], [:ILSA, nil]],
  :ZENITH_A   => [[:ROOK, "choice(:ch16_rook) == :hold"], [:ODESSA, nil]],     # a fired Rook can't represent Zenith
  :ZENITH_B   => [[:KESTREL, "!flag(:KESTREL_FOR_ANTUMBRA)"], [:MAGNUS, "!flag(:MAGNUS_EXPOSED)"], [:ODESSA, nil], [:ROOK, nil]],
  :NADIR_A    => [[:KAITO, nil]],
  :NADIR_B    => [[:CORVIN, "flag(:CORVIN_FREED) && choice(:ch17_nyx) == :refuse"], [:NYX, nil]],
  :OSSARIA_A  => [[:SAHAR, nil]],
  :OSSARIA_B  => [[:BASTIAN, "choice(:ch14_telemetry) != :leave"], [:FORFEIT, nil]],  # Cragholm raided through your beacon: Bastian stays with his dead
  :ISENMAR_A  => [[:ANJA, "flag(:ISENMAR_ONE_SEAT) && flag(:ISENMAR_KEEPS_ANJA)"], [:MARISOL, nil]],
  :ISENMAR_B  => [[:FORFEIT, "flag(:ISENMAR_ONE_SEAT)"], [:ANJA, nil]],   # :FORFEIT = first unseated entrant of FORFEIT_POOL (the Accord lends the seat)
  :ASHKAAR_A  => [[:SIGRUN, nil]],
  :ASHKAAR_B  => [[:FORFEIT, "flag(:ASHKAAR_ONE_SEAT)"], [:BRANN, nil]],
  :ACCORD     => [[:VALEN, nil]]
}
# Seat template (slot order; R16 pairs are (0,1) (2,3) ...). The draw then swaps path opponents into the player's blocks as it does today.
BRACKET_SEATS = [:PLAYER, :ELOWEN_A, :ELOWEN_B, :OSSARIA_A, :ANTUMBRA_B, :ZENITH_A, :NADIR_A, :OSSARIA_B,
                 :ACCORD, :ZENITH_B, :NADIR_B, :ISENMAR_A, :ISENMAR_B, :ASHKAAR_B, :ANTUMBRA_A, :ASHKAAR_A]
HEADLINE_OPPONENT = :CELESTINE
PLAYER_PATH = [:JUNO, :CELESTINE, :KESTREL, :VALEN]   # fallback only
```
`FORFEIT_POOL = [:DORIAN, :TAMSIN, :ROOK, :ODESSA, :ILSA, :NYX, :CORVIN]` (seven names for at most three forfeits, so one is always free; a victor
gets terms, never a third delegate). Seats resolve in hash order, forfeits last. Guarantees: every seat ends in an unconditional candidate or `:FORFEIT`; Kestrel, Juno, Celestine, Kaito, Ysolde, Sigrun and Valen are **always seated**.
New function **[CORE+] `seated(:ENTRANT)`** → true if that entrant holds a seat this run.

New/changed entrants (all story-met; NPC-only unless a team is listed in §7):
```ruby
ENTRANTS.merge!({
  :CELESTINE => { :display => "Celestine", :trainer_type => :LEADER_CELESTINE, :name => "Celestine", :version => 92, :rating => 92, :level_hint => 92 },
  :YSOLDE    => { :display => "Ysolde",    :trainer_type => :LEADER_YSOLDE,    :name => "Ysolde",    :version => 92, :rating => 86, :level_hint => 92 },
  :MARISOL   => { :display => "Marisol",   :trainer_type => :LEADER_MARISOL,   :name => "Marisol",   :version => 90, :exhibition => true, :rating => 84, :level_hint => 90 },
  :ANJA      => { :display => "Anja",      :trainer_type => :LEADER_ANJA,      :name => "Anja",      :version => 90, :rating => 84, :level_hint => 90 },
  :BRANN     => { :display => "Brann",     :trainer_type => :LEADER_BRANN,     :name => "Brann",     :version => 96, :rating => 88, :level_hint => 96 },
  :ILSA      => { :display => "Ilsa",      :trainer_type => :LEADER_ILSA,      :name => "Ilsa",      :version => 50, :rating => 85 },
  :MAGNUS    => { :display => "Magnus",    :trainer_type => :LEADER_MAGNUS,    :name => "Magnus",    :version => 50, :rating => 86 },
  :CORVIN    => { :display => "Corvin",    :trainer_type => :LEADER_CORVIN,    :name => "Corvin",    :version => 50, :rating => 83 },
  :BASTIAN   => { :display => "Bastian",   :trainer_type => :LEADER_BASTIAN,   :name => "Bastian",   :version => 50, :rating => 80 },
  :SAHAR     => { :display => "Sahar",     :trainer_type => :LEADER_SAHAR,     :name => "Sahar",     :version => 50, :rating => 83 },
  :TAMSIN    => { :display => "Tamsin",    :trainer_type => :LEADER_TAMSIN,    :name => "Tamsin",    :version => 50, :rating => 78 },
  :DORIAN    => { :display => "Dorian",    :trainer_type => :LEADER_DORIAN,    :name => "Dorian",    :version => 50, :rating => 80 },
  :ROOK      => { :display => "Rook",      :trainer_type => :LEADER_ROOK,      :name => "Rook",      :version => 50, :rating => 82 },
  :ROWAN     => { :display => "The Gardener", :trainer_type => :LEADER_ROWAN,  :name => "Rowan",     :version => 90, :rating => 88, :level_hint => 90 },
  :DASK      => { :display => "Archseer Dask", :trainer_type => :ARCHSEER_DASK, :name => "Imre",     :version => 92, :rating => 92, :level_hint => 92 },
  :KESTREL_FALLEN => { :display => "Kestrel", :person => :KESTREL, :trainer_type => :RIVAL_KESTREL, :name => "Kestrel", :rival_battle => 9, :rating => 95, :level_hint => 94 },
  :VALEN_RUIN=> { :display => "Valen",     :person => :VALEN, :trainer_type => :CHAMPION_VALEN, :name => "Valen", :version => 1, :rating => 99, :level_hint => 96 },
  :QUENT     => { :display => "Dr. Quent", :trainer_type => :MERIDIAN_QUENT,   :name => "Percival",  :version => 99, :rating => 97, :level_hint => 100 },
  :THEODRIC  => { :display => "Gilded King Aurelius", :trainer_type => :GILDED_THEODRIC, :name => "Aurelius",  :version => 0, :rating => 99, :level_hint => 100 },
  :MORWEN       => { :display => "Morwen", :trainer_type => :ECHO_MORWEN, :name => "Morwen", :version => 90, :exhibition => true, :rating => 0 },
  :PAGEANT_BOUT => { :display => "Dorian & Rook", :double => true, :trainer_type => [:LEADER_DORIAN, :LEADER_ROOK], :name => ["Dorian", "Rook"],
                     :version => 90, :exhibition => true, :rating => 0 }
})
# Remove every cameo entrant, the Rev-4 outsiders (:ISAURA :DREY :MIREILLE :THORNE) and the samples :SUCCESSOR, :MOURNER.
```

### 6.2 Where the player met every possible opponent (Rev 5 audit)
Juno, Kestrel, Valen, Rowan, Voss: throughout. Marisol: Ch4, Ch9, Ch11, the war. Anja: Ch11, the war (prisoner). Celestine: Ch3 (disguised), Ch9, Ch18.
Sigrun: Ch8, the war, Ch19. Kaito: Ch9, Ch13. Ysolde: Ch15 (gym, echo, K6 aftermath). Odessa: Ch12, Ch14–16. Brann: Ch8, Ch17. Quent: Ch8, Ch10, Ch14, Ch16.
Dorian/Rook (exhibition): Ch2, Ch17 / Ch5, Ch16. Morwen's Echo: Ch13 memory, Ch15 echo. Ruin only: Dask (Ch13, R1, R4), Aurelius (R3, R6).

### 6.3 Draw lists (first match wins; the stage default is the appended fallback)
```ruby
DRAWS = {
  :R16 => [   # default :JUNO (J4)
    { :opponent => :MARISOL, :condition => "!ruin_route && seated(:MARISOL) && !flag(:TEO_SAVED) && bond(:MARISOL) <= 2" },
    { :opponent => :ANJA,    :condition => "!ruin_route && seated(:ANJA) && flag(:ANJA_EXPOSED)" },
    { :opponent => :ROWAN,   :condition => "!ruin_route && flag(:ROWAN_ALIVE) && choice(:ch13_rowan_testimony) == :mercy && standing(:HOLLOW) >= 4" }
  ],
  :QF => [    # default :CELESTINE (v92)
    { :opponent => :DASK,   :condition => "ruin_route" },
    { :opponent => :SIGRUN, :condition => "resonance <= -3 || flag(:WAR_ISENMAR_WON)",       :version => 92 },   # she weighs you again, or comes for the one who broke her father's legions
    { :opponent => :KAITO,  :condition => "choice(:ch19_oath) == :keep",                     :version => 92 },
    { :opponent => :YSOLDE, :condition => "flag(:KESTREL_FALLEN)" },
    { :opponent => :ODESSA, :condition => "seated(:ODESSA) && tally(:WARM_BONDS) >= 5 && resonance >= 2", :version => 92 }
  ],
  :SF => [    # default :KESTREL (K8, 80-82); Ruin Route: same team, Ruin dialogue
    { :opponent => :KESTREL_FALLEN, :condition => "!ruin_route && flag(:KESTREL_FALLEN)" }
  ],
  :FINAL => [ # default :VALEN. :live => true [CORE+]: drawn when the Final starts (Day 7)
    { :opponent => :VALEN_RUIN, :condition => "ruin_route" },
    { :opponent => :BRANN,      :condition => "flag(:VALEN_COLLAPSED)" }
  ],
  :HIJACK => [ # default :VOSS (drawn live)
    { :opponent => :THEODRIC, :condition => "ruin_route" },
    { :opponent => :QUENT,    :condition => "flag(:VOSS_DISCREDITED)" }
  ]
}
```
Kestrel's banner in the SF is Gravenmoor's (`KESTREL_FOR_ANTUMBRA`) or Meridian's sunburst; the team is the same. Brann may stand in for Valen
whether or not he held Ashkaar's second seat ("I lost in the first round. He asked me anyway.").

### 6.4 Who is displaced, and where they go
| Drawn | Default displaced | Result | Story reason |
|---|---|---|---|
| R16 Marisol / Anja | Juno | **swap** seats; Juno plays on as an NPC | the **Right of Grievance** (Marisol); Anja asks the Pageant-Master for "the child who threw me to the court" |
| R16 Rowan | Juno | **Juno leaves the bracket by design** | she gives "the Gardener" Elowen's seat; Garden Match exhibition offered |
| QF Sigrun / Kaito / Ysolde / Odessa | Celestine | **swap**; Celestine plays on | each asks the Hierophant for the challenger's quarter (lines in 10_CHOICES_ENDINGS §3.2) |
| QF Dask (Ruin) | Celestine | **Celestine leaves** | "I cannot lie, so I won't pretend this is a game." |
| SF / Final variants, Brann's stand-in | — | same seat | — |

### 6.5 Companion matches: winner rules and highlight data [CORE+ `MATCH_RULES`, consumed by Prismfall Cutscenes]
Resolution order for any NPC match: a drawn path opponent always wins until they meet the player → the first `MATCH_RULES` row for that pair
whose condition holds → higher `:rating`. Each row carries 2–4 key moments: `[actor, pokemon, event, caption]`, where event is one of
`:send_out :attack :beam :beam_clash :dodge :faint :switch :field_shift :taunt :forfeit :finish`.
```ruby
MATCH_RULES = [
  { :pair => [:KESTREL, :KAITO], :winner => :KESTREL, :condition => nil, :moments => [
      [:KAITO,   :LUCARIO,   :send_out,   "Kaito: \"Stand up. Again.\""],
      [:KESTREL, :AEGISLASH, :attack,     "The Gauntlet flares; the arena's field surges on its own."],
      [:KAITO,   :LUCARIO,   :dodge,      "Lucario flinches from something that isn't the blade."],
      [:KESTREL, :AEGISLASH, :finish,     "Kaito, after: \"Lucario felt it. That isn't him fighting.\""] ] },
  { :pair => [:KESTREL, :ROOK], :winner => :KESTREL, :condition => nil, :moments => [
      [:ROOK,    :ROTOM,     :send_out,   "Rook: \"Chat says you're gonna lose.\""],
      [:KESTREL, :STARAPTOR, :attack,     "Brave Bird through a Thunderbolt, live on every screen in Zenith."],
      [:ROOK,    :TOXTRICITY,:faint,      "Rook, off-mic: \"...Chat's wrong a lot.\""] ] },
  { :pair => [:KESTREL, :ODESSA], :winner => :KESTREL, :condition => nil, :moments => [
      [:ODESSA,  :CORVIKNIGHT, :send_out, "Odessa: \"Hold onto something.\""],
      [:KESTREL, :AEGISLASH,   :attack,   "King's Shield, then the counter."],
      [:ODESSA,  :CORVIKNIGHT, :forfeit,  "She salutes and loses with style."] ] },
  { :pair => [:ANJA, :BRANN], :winner => :ANJA, :condition => "flag(:WAR_ISENMAR_WON) || (flag(:WAR_STOPPED) && choice(:war_prisoner) == :free)", :moments => [
      [:BRANN, :COALOSSAL, :send_out,     "Two Wardens who were on opposite sides of the Steamline a season ago."],
      [:ANJA,  :MAMOSWINE, :beam_clash,   "Blizzard meets Flamethrower: the war's beam clash, in miniature, and this time nobody dies."],
      [:BRANN, :COALOSSAL, :faint,        "Brann laughs until he coughs. \"Aye. Ice remembers.\""] ] },
  { :pair => [:ANJA, :BRANN], :winner => :BRANN, :condition => nil, :moments => [
      [:ANJA,  :MAMOSWINE, :send_out,     "Anja doesn't bow."],
      [:BRANN, :COALOSSAL, :beam_clash,   "Flamethrower against Blizzard; steam hides the whole arena."],
      [:ANJA,  :MAMOSWINE, :faint,        "Brann offers a hand. Whether she takes it depends on the armistice (ISENMAR_EMBITTERED)."] ] },
  { :pair => [:MARISOL, :BRANN], :winner => :MARISOL, :condition => "!flag(:WAR_ASHKAAR_WON)", :moments => [
      [:MARISOL, :GYARADOS, :send_out,    "\"Tides take it. Let's go, old man.\""],
      [:MARISOL, :GYARADOS, :beam,        "Hydro Pump douses the forge-field: :VOLCANIC cools to :ASHEN_WASTE."],
      [:BRANN,   :ARCANINE, :faint,       "Brann: \"Forged to break right.\""] ] },
  { :pair => [:YSOLDE, :SIGRUN], :winner => :SIGRUN, :condition => nil, :moments => [
      [:YSOLDE, :CHANDELURE, :field_shift, "The Cathedral's candles follow her in."],
      [:SIGRUN, :SALAMENCE,  :attack,      "Salamence dives through the dark."],
      [:YSOLDE, :CHANDELURE, :faint,       "Ysolde: \"The dead say you fight like someone with nothing to bury.\""] ] },
  { :pair => [:JUNO, :SIGRUN], :winner => :SIGRUN, :condition => nil, :moments => [
      [:JUNO,   :TSAREENA,  :send_out,     "Juno, displaced by a Grievance, fights anyway."],
      [:JUNO,   :TSAREENA,  :field_shift,  "The Flower Garden reaches stage five for the first time in her life."],
      [:SIGRUN, :HAXORUS,   :finish,       "Sigrun kneels to her afterward. Nobody has seen her do that."] ] },
  { :pair => [:JUNO, :YSOLDE], :winner => :JUNO, :condition => "bond(:JUNO) >= 5", :moments => [
      [:YSOLDE, :GENGAR,    :taunt,        "\"Your aunt is listening, you know.\""],
      [:JUNO,   :WHIMSICOTT,:attack,       "Juno, crying, doesn't miss."],
      [:YSOLDE, :GENGAR,    :faint,        "Ysolde smiles. It was a kindness, and it worked."] ] },
  { :pair => [:CELESTINE, :MARISOL], :winner => :CELESTINE, :condition => nil, :moments => [
      [:CELESTINE, :TOGEKISS, :send_out,   "\"Once upon a time, a dockworker fought a fairy tale.\""],
      [:MARISOL,   :GYARADOS, :attack,     "\"I don't do stories. Waterfall.\""],
      [:CELESTINE, :TOGEKISS, :finish,     "The story wins. Marisol swears for a full caption box."] ] },
  { :pair => [:VALEN, :SIGRUN], :winner => :VALEN, :condition => nil, :moments => [
      [:SIGRUN, :SALAMENCE, :send_out,     "She entered to take the Blessing so the child wouldn't have to."],
      [:VALEN,  :ZYGARDE,   :attack,       "His crystal arm spreads to the collarbone with the order."],
      [:SIGRUN, :SALAMENCE, :faint,        "\"He beat me with an arm made of glass.\""] ] },
  { :pair => [:VALEN, :KAITO], :winner => :VALEN, :condition => nil, :moments => [
      [:KAITO, :LUCARIO, :send_out,        "The man who sealed Marrowgate, and the man who ordered it."],
      [:KAITO, :LUCARIO, :attack,          "Kaito's first Aura Sphere is aimed a hand's width wide. On purpose."],
      [:VALEN, :ZYGARDE, :finish,          "If KAITO_TESTIFIED: Valen bows first."] ] }
]
```
"Notable" = involves Juno or Kestrel, the war's two sides, or Valen. Other NPC matches show a one-line result only.

### 6.6 Exhibitions (story-met only) [CORE+ `EXHIBITION_EXTRAS`]
The **Eevee Octave** is not in this list: it is a Trials quest line (SPINE Rev 19, `design/EEVEE_OCTAVE.md`) whose gauntlet opens in the Glassfall Memorial Garden once all eight singers are helped, on every route, including the Ruin Route, where it is the only exhibition.
```ruby
EXHIBITION_EXTRAS = [
  { :entrant => :PAGEANT_BOUT, :condition => "!ruin_route", :from_day => 3 },                                    # Dorian & Rook double
  { :entrant => :JUNO,         :condition => "!ruin_route && drawn(:R16) != :JUNO", :from_day => 3 },            # Garden Match (J4 team)
  { :entrant => :MARISOL,      :condition => "!ruin_route && drawn(:R16) != :MARISOL && flag(:TEO_SAVED) && bond(:MARISOL) >= 5", :from_day => 3 },
  { :entrant => :MORWEN,       :condition => "!ruin_route && flag(:KESTREL_YSOLDE_RECONCILED) && choice(:ch15_kestrel) == :resolve", :from_day => 5 }
]
```

### 6.7 True Finale variants [CORE+ `ARCEUS_VARIANTS`, read by Prismfall Bosses]
Bars = locks. Default bar *k* (1–6) holds the Plates of gyms 3k−2..3k; between bars those three Wardens' release (or refusal) beats play.
Each Warden in the coming bar whose `WARDEN_CONSENT` is false makes it a **forced lock**: Arceus starts that bar with +1 to every stat stage per refusal.
```ruby
ARCEUS_VARIANTS = [
  { :id => :ARCEUS_JUDGMENT,      :condition => "ruin_route",                  :bars => 7, :player_side => 2 },  # Ruin: Giratina-Origin partner; bar 7 on :INVERSE
  { :id => :ARCEUS_GILDED,        :condition => "flag(:ENGINE_CALIBRATED)",    :bars => 6 },  # bar 6 refills 3x, then scripted binding -> END_GILDED_CHAIN
  { :id => :ARCEUS_WAR,           :condition => "resonance <= -6",             :bars => 7 },  # the shard eats types: no release beats, every lock forced
  { :id => :ARCEUS_MISCALIBRATED, :condition => "flag(:TELEMETRY_SABOTAGED)",  :bars => 5 },  # bar 5 covers gyms 13-18; Larch: "It's reaching for a shard that isn't where it thinks!"
  { :id => :ARCEUS_BOUND,         :condition => nil,                           :bars => 6 }
]
# HARMONY_BUFF (resonance >= 6): at every bar break the PC's active Pokemon recovers 25% HP and its stat drops are cleared.
```

---

## 7. Festival trainer teams the trainer agent must build (complete list, Revision 5)

Version = the Standard base; Core adds +100 (Hard) / +200 (Casual) when those exist. Rival entries are ×3 (one per starter slot).
Festival-only Warden/NPC teams use **version = ace level** (90/92/96/99) so they never collide with story versions.

| # | Stage | Entrant | `[TYPE, Name, Version]` | Ace | Status |
|---|---|---|---|---|---|
| 1 | R16 | Juno (J4, default; also Garden Match) | `[RIVAL_JUNO, Juno, 40/41/42]` | 90 | planned |
| 2 | R16 | Marisol (Grievance; also Ebb Guild match) | `[LEADER_MARISOL, Marisol, 90]` | 90 | **NEW** |
| 3 | R16 | Anja (exposed) | `[LEADER_ANJA, Anja, 90]` | 90 | **NEW** |
| 4 | R16 | Rowan, "the Gardener" | `[LEADER_ROWAN, Rowan, 90]` | 90 | **NEW** (replaces Core's sample v50) |
| 5 | QF | **Celestine** (default) | `[LEADER_CELESTINE, Celestine, 92]` | 92 | **NEW** |
| 6 | QF | Sigrun (Resonance ≤ −3, or Isenmar won the war) | `[LEADER_SIGRUN, Sigrun, 92]` | 92 | **NEW** (replaces the Rev-4 v96 stand-in team) |
| 7 | QF | Kaito (Keep oath) | `[LEADER_KAITO, Kaito, 92]` | 92 | **NEW** |
| 8 | QF | Ysolde (Kestrel fallen) | `[LEADER_YSOLDE, Ysolde, 92]` | 92 | **NEW** |
| 9 | QF | Odessa (warm draw) | `[LEADER_ODESSA, Odessa, 92]` | 92 | **NEW** |
| 10 | QF (Ruin) | Archseer Imre Dask | `[ARCHSEER_DASK, Imre, 92]` | 92 | **NEW** (new trainer type) |
| 11 | SF | Kestrel (Redeemed, K8, default) | `[RIVAL_KESTREL, Kestrel, 80/81/82]` | 94 | planned |
| 12 | SF | Kestrel (Fallen) | `[RIVAL_KESTREL, Kestrel, 90/91/92]` | 94 | **NEW** (`rival_battle 9`) |
| 13 | Final | Valen (default) | `[CHAMPION_VALEN, Valen, 0]` | 96 | planned |
| 14 | Final | Brann (stand-in) | `[LEADER_BRANN, Brann, 96]` | 96 | **NEW** |
| 15 | Final (Ruin) | Valen, the Last Tuning | `[CHAMPION_VALEN, Valen, 1]` | 96 | **NEW** |
| 16 | Hijack | Voss (default) | `[MERIDIAN_VOSS, Aurelian, 0]` | 100 | planned |
| 17 | Hijack | Dr. Quent | `[MERIDIAN_QUENT, Percival, 99]` | 100 | **NEW** (Voss's Silvally team in Quent's hands) |
| 18 | Hijack (Ruin) | Aurelius, the Gilded Reflection | `[GILDED_THEODRIC, Aurelius, 0]` | 100 | **NEW** (new trainer type) |
| 19 | Exhibition | Pageant Bout: Dorian + Rook (double) | `[LEADER_DORIAN, Dorian, 90]` + `[LEADER_ROOK, Rook, 90]` | 90 | **NEW** ×2 |
| 20 | Exhibition | Morwen's Echo | `[ECHO_MORWEN, Morwen, 90]` | 90 | **NEW** (new trainer type) |
| B1–B5 | True Finale | Arceus | boss configs `ARCEUS_BOUND` (planned), `_MISCALIBRATED`, `_WAR`, `_GILDED`, `_JUDGMENT` | 100 | 4 **NEW** |

**Total new Festival teams: 19** (+4 Arceus boss configs). New trainer types: `ARCHSEER_DASK`, `GILDED_THEODRIC`, `ECHO_MORWEN` (plus `LEADER_ROWAN` if
it doesn't exist yet). Seeded NPC-only entrants needing **no** trainer data: Dorian, Rook, Tamsin, Sahar, Nyx (and the QF/R16 Wardens when not drawn).

Rev 6 adds **no** teams: delegation seats that aren't draw candidates (Ilsa, Magnus, Corvin, Bastian, Sahar, Tamsin, Dorian, Rook, Nyx) are NPC-only
and resolve by `MATCH_RULES`.

**Retired team IDs (no longer Festival teams):**
- Rev 4 outsiders, withdrawn before anyone built them: `[FESTIVAL_ISAURA, Isaura, 2]`, `[FESTIVAL_DREY, Matthias, 1]`, `[FESTIVAL_MIREILLE, Mireille, 2]`,
  `[FESTIVAL_THORNE, Ivo, 1]`, `[LEADER_BASTIAN, Bastian, 90]`, `[LEADER_SIGRUN, Sigrun, 96]`. The trainer types `FESTIVAL_ISAURA/DREY/MIREILLE/THORNE` are not needed.
- Rev 3 draws: `[FESTIVAL_MELIA, Melia, 2]`, `[FESTIVAL_TITANIA, Titania, 2]`, `[FESTIVAL_ALEXANDRA, Alexandra, 2]`, `[FESTIVAL_GARRET, Garret, 2]`, `[FESTIVAL_NOVA, Nova, 2]`.
- Every cameo Festival team: `FESTIVAL_LIN`, `_AMARIA`, `_SHELLY`, `_ALEXANDRA`, `_VENAM`, `_SHIV`, `_GARRET`, `_MELIA`, `_TITANIA`, `_NOVA` at versions 1, 2 and 3.
  They belong to the story lead's optional sidequests now, at whatever levels those set.

**Non-Festival teams this spec adds** (story battles):

| `[TYPE, Name, Version]` | Where | Why |
|---|---|---|
| `[RIVAL_JUNO, Juno, 70/71/72]` | Ch21 tag-battle partner | replaces Kestrel when `KESTREL_FALLEN` |
| `[MERIDIAN_KROLL, Sabine, 21]` + `[MERIDIAN_MARCHETTI, Helene, 21]` + `[MERIDIAN_QUENT, Percival, 21]` | Ch21 tag foes | Quent + Kroll (default), Marchetti + Quent (Marchetti not turned); if Quent is the hijacker: Marchetti + Kroll, or Kroll + `[MERIDIAN_DIRECTORATE, Captain, 21]` when Marchetti is turned |
| `[LEADER_MAGNUS, Magnus, 1]`, `[LEADER_NYX, Nyx, 1]`, `[LEADER_CELESTINE, Celestine, 1]`, `[LEADER_SIGRUN, Sigrun, 1]` | Ruin Route Gyms 15–18 | Ruin versions (10_CHOICES_ENDINGS §5) |
| `[REFLECTION, ???, 0]` | Ruin R1 | generated at battle start from `$player.party`; the PBS team is only a fallback |
| boss config `GIRATINA_ORIGIN_TRIAL` | Ruin R1 | Giratina tests the Renegade on `:INVERSE` |
| boss config `KYOGRE_WEATHER` | Ch11 `GO_WEATHER` | the existing Kyogre at a fixed lv 80, unwinnable, no catch |

## 8. Story-battle variants in the finale (not Festival stages)

- **Tag battle partner:** Kestrel if `flag(:KESTREL_REDEEMED)`, else Juno.
- **Tag foes:** see the table above.
- **Fallen Kestrel in the hijack** is **not** a stage opponent (the draw forbids fighting a person twice). Voss harnesses him into the Engine as a
  proxy conduit; between Voss's bars 2 and 3 the event offers `:ch21_reach_kestrel`. `:reach`/`:burn` break the conduit (Voss loses his bar-3
  regeneration); `:let_go` sets `KESTREL_LOST` (he burns out as the Engine fires).
- **`VOSS_FEIGNED`:** the hijack opens with Voss's Silvally at −1 to all stats for 3 turns ("You were *close*. You let me get close."). Same team.
- **`VOSS_ACCEPTED`:** at the hijack, Voss offers his hand (`:ch21_hand`). `:take` skips the hijack battle and the True Finale and triggers
  `END_CONCORD_DAWN`. `:refuse` plays the hijack normally, with the line "You promised."

---

## 9. Game overs (23 canonical + 2 Ruin-only)

Ledger unlock = all 23 canonical found (`:ruin_exempt => true` entries don't count). The story lead's GO-20 "Encore" is **cut** (it overlaps
GO_INTO_THE_LINE and needed four conditions). Two are **new**: `GO_WEATHER` (the one "battle you were told to flee") and `GO_STAY_OUT`.
```ruby
LEDGER_SHOW_HINTS = false   # the 'ledgerhints' password, or any seen ending, turns hints on (see §14)
GAME_OVERS = {
  # Act I
  :GO_HOMEWARD         => { :title => "Homeward",           :hint => "Prologue. Edda asks twice.",
                            :epitaph => "You went home. The lights went out one by one, and you watched them from the other shore." },
  :GO_ORCHARD          => { :title => "Two in the Orchard", :hint => "Ch1. Some hands shouldn't be held through a Veil.",
                            :epitaph => "She trusted you. That was the whole problem." },
  :GO_CURTAIN_CALL     => { :title => "Curtain Call",       :hint => "Ch3. The butler mouths a word.",
                            :epitaph => "Your notices were excellent. The run has not closed. It never will." },
  :GO_LIVE_WIRE        => { :title => "Live Wire",          :hint => "Ch5. Rook shouts about hands.",
                            :epitaph => "Even you weren't made to hold lightning bare." },
  # Act II
  :GO_SINKFIELD        => { :title => "Sinkfield",          :hint => "Ch6. Walk the bones, never the sand.",
                            :epitaph => "The desert kept you. Somewhere else." },
  :GO_SWEET_TOOTH      => { :title => "Sweet Tooth",        :hint => "Ch7. The third offer is the sweetest.",
                            :epitaph => "You were so happy. You never wondered why again." },
  :GO_LET_THEM_LISTEN  => { :title => "Let Them Listen",    :hint => "Ch8. A Hammer offers you the last word.",
                            :epitaph => "They listened. There was no one left to tell." },
  :GO_PULL_THE_NAIL    => { :title => "Pull the Nail",      :hint => "Ch9. Only the Hollow's friends are asked.",
                            :epitaph => "You pulled the nail. The whole house came down." },
  # Act III
  :GO_LOYAL            => { :title => "Loyal",              :hint => "Ch10. Side with the heroes of the pageant.",
                            :epitaph => "You believed the story everyone told. So did the people who wrote it." },
  :GO_WEATHER          => { :title => "Weather",            :hint => "Ch11. When the lake breathes, run.",
                            :epitaph => "You tried to fight the sea. The sea didn't notice. In spring, Rimeholt carved your name on the ice wall, and the thaw took that too." },
  :GO_THIN_ICE         => { :title => "Thin Ice",           :hint => "Ch11. Ice remembers every weight.",
                            :epitaph => "You went back for the proof. The lake kept it, and you." },
  :GO_FINE_PRINT       => { :title => "Read the Fine Print", :hint => "Interlude III. Calla glances at a drawer.",
                            :epitaph => "Kestrel Vane was reported missing the next morning. Meridian offered a reward." },
  :GO_LOOKING_BACK     => { :title => "Looking Back",       :hint => "Ch13. Dask's one rule.",
                            :epitaph => "You looked back. Now you're the reflection, and something else is wearing your face to the Festival." },
  # Act IV
  :GO_WILLING          => { :title => "Willing",            :hint => "Ch14. Never, ever let them examine you.",
                            :epitaph => "The exam was painless, as promised. You've been asleep since. Meridian sends flowers." },
  :GO_ECHO             => { :title => "Echo",               :hint => "Ch15. Echoes are a door that opens one way.",
                            :epitaph => "You stayed for the song. Gravenmoor has one more echo now. It sings harmony." },
  :GO_OVERTIME         => { :title => "Overtime",           :hint => "Ch16. We go when the whistle goes.",
                            :epitaph => "You stayed past the whistle. Strade Works issued a statement about an industrial accident." },
  :GO_INTO_THE_LINE    => { :title => "Into the Line",      :hint => "Ch17. Don't make them choose.",
                            :epitaph => "They didn't choose. The bullet did. Meridian called it a tragic accident, and meant it." },
  :GO_THE_THRONE       => { :title => "The Throne",         :hint => "Ch17. Don't touch anything gold.",
                            :epitaph => "You fit perfectly. That was the problem the Gilders were trying to solve." },
  # Act V
  :GO_FAIR_BARGAIN     => { :title => "Fair Bargain",       :hint => "Ch18. Ask what it costs before you say yes.",
                            :epitaph => "The price was your name. You are very happy now, as a lantern-moth, and you will glow at every dusk." },
  :GO_STAY_OUT         => { :title => "Somebody Else's Story", :hint => "Ch18. Do what Kestrel asks.",
                            :epitaph => "You did what everyone had told you since the ferry. The Engine took Kestrel instead. He lasted eleven minutes. Velmora lasted a week." },
  :GO_LIARS_PYRE       => { :title => "Liar's Pyre",        :hint => "Ch19. Say true or say nothing.",
                            :epitaph => "Ashkaar burns liars. It is the oldest law, and the dragons remember it even when men forget." },
  :GO_EARLY_CROWN      => { :title => "Early Crown",        :hint => "Ch20. Don't let him hand you anything tonight.",
                            :epitaph => "The Crown was whole for one second. Then it was Meridian's." },
  :GO_HIS_HAND         => { :title => "His Hand",           :hint => "Ch21. Not chained, not bought.",
                            :epitaph => "It didn't hurt. That was the cruelest part." },
  # Ruin Route only (not needed for the unlock)
  :GO_R_WELCOME_BEHIND => { :title => "Welcome, Behind",   :hint => "Ruin. The Archseer's kindness.", :ruin_exempt => true,
                            :epitaph => "You stayed behind the Glass. It remembers those who stay perfectly, and forgets them a little more each day." },
  :GO_R_KNEEL          => { :title => "Long Live the King", :hint => "Ruin. A king asks you to kneel.", :ruin_exempt => true,
                            :epitaph => "You knelt. The Aureate Kingdom stepped through the Glass, golden and unrepentant, and King Aurelius finished his sentence." }
}
```

## 10. Game-over triggers and checkpoints

Call `Prismfall.checkpoint` at the listed point (a real save, placed **before** the trigger's event page), then `Prismfall.game_over(:ID)`
on the trigger. Every trigger is a deliberate player choice with at least one confirm or repeated prompt; none fire from a cumulative stat alone.

| ID | Ch | Type | Trigger | Foreshadowing (must be on screen first) | Checkpoint |
|---|---|---|---|---|---|
| GO_HOMEWARD | P | defy / joke | tell Edda you want to go back; confirm at her 2nd "Last chance, sprog" | Edda asks twice | after the badge-case scene |
| GO_ORCHARD | 1 | defy | "Pull me through?" → Yes | Larch: "Never take a tinted person past a Veil"; Juno's burning line | Glassed Orchard entrance |
| GO_CURTAIN_CALL | 3 | joke | accept "join the company forever" (Thistledown Manor, on the Weavers' Road) | butler-ghost mouths *don't* | Thistledown attic stairs |
| GO_LIVE_WIRE | 5 | defy | "Grab the cracked Plate and run" (Electivire interlude prompt) | the Mourner's smoking glove; Rook: "Don't touch it with your hands!" | Plate Vault door |
| GO_SINKFIELD | 6 | defy | step off the fossil path for the glint (after Sahar's 3 warnings) | sinking sandal; Field Notes | Sinkfield entrance |
| GO_SWEET_TOOTH | 7 | defy / joke | accept Sweetrot the 3rd time | Wenlow's warning after the 1st | Mirefen Pokémon Center (before the 3rd vendor) |
| GO_LET_THEM_LISTEN | 8 | betrayal | take the Hammer's detonator | Field Notes on Shatters; the Lowlight's glass | caldera floor (before CH8_CALDERA) |
| GO_PULL_THE_NAIL | 9 | betrayal (offered only if `standing(:HOLLOW) >= 4`) | agree to plant Sable's charge | Wick's Ch7 line; Sable's broadcast | Ironreach shafts |
| GO_LOYAL | 10 | choice | `:ch10_ogre` → "Stand with the Three" | the Mourner's Ch2 line; Celestine's Ch3 rhyme; poison collars | Bride Grove gate |
| GO_WEATHER | 11 | fight-when-told-to-flee (NEW) | when the lake breathes: "Fight it now" vs "Get to the towers"; scripted unwinnable Kyogre lv 80 | Anja: "That's not a Pokémon, that's weather. *Towers!*" | start of the Thaw |
| GO_THIN_ICE | 11 | defy / failed escape | go back for the Lattice data core | Anja's line; the cracking-tile gym tutorial | start of the Thaw (same save) |
| GO_FINE_PRINT | 12 | defy (Interlude III, as Kestrel) | open Voss's desk drawer | Calla's glance | interlude start |
| GO_LOOKING_BACK | 13 | defy | "Look back?" → Yes on the Threshold | Dask's rule ×2, signpost in mirror-writing | Mirror Mere |
| GO_WILLING | 14 | capture | accept Quent's "painless" removal | Larch: "Never, ever let them examine you." | before the raid |
| GO_ECHO | 15 | defy | "Stay and listen?" ×3 | Ysolde's warning; translucent hand on the 2nd | Hollow Cathedral nave |
| GO_OVERTIME | 16 | timed (klaxon 3) | keep copying blueprints past the whistle | Rook ×2: "no heroics" | core-chamber door |
| GO_INTO_THE_LINE | 17 | defy | "Step between them?" → Yes | Nyx's courier ×2 | Underveil barricade |
| GO_THE_THRONE | 17 | capture | "Sit on the Gilded King's throne?" → Yes | Sahar: "Don't touch anything gold"; open-hand armrests | Sun Court antechamber |
| GO_FAIR_BARGAIN | 18 | joke / defy | accept the moth-stall bargain without asking the price | Celestine on arrival | Gloaming market gate |
| GO_STAY_OUT | 18 | choice-based (NEW) | after K7: "Stay out of Crownhaven?" → Yes → "He's already walking away. Let him go?" → Yes | Celestine ("It says *walker*"), Sigrun's summons, Larch's letter all say it must be the PC | after K7 |
| GO_LIARS_PYRE | 19 | defy | the hidden 5th oath "Whatever you want to hear." (always offered; no lie-tracking needed) | gate-guard: "say true or say nothing"; the brazier oath | Rift heart |
| GO_EARLY_CROWN | 20 | betrayal (Valen's) | accept the crown tonight | Ilsa: "Don't let him hand you anything tonight." | Sanctum door |
| GO_HIS_HAND | 21 | betrayal | take Voss's hand (any path without `VOSS_ACCEPTED`) | Larch: "Don't let him make you a part. He's very good at parts."; K7 speech; Celestine | before the Coronation |
| GO_R_WELCOME_BEHIND | R6 | Ruin | accept Dask's offer to stay behind the Glass | Dask's own mirrored pitch | Ruin QF |
| GO_R_KNEEL | R7 | Ruin | kneel to Aurelius | Voss kneels first; Giratina's warning | before the Ruin hijack |

## 11. Ruin Route keys

- **Unlock:** `ruin_unlocked` (Core: all non-exempt game overs in the Ledger).
- **In-story trigger:** Ch15, immediately after the Giratina boss in the Reverse Depths. Only if `ruin_unlocked`, a pane of the Depths shows
  Juno calling the PC's name (the GO_LOOKING_BACK image). Prompt `:ch15_look_back`. `:yes` → `Prismfall.start_ruin_route` (sets `ruin_route`),
  resonance set to `min(resonance, -6)`, warp to R1. `:no` → main story continues; the prompt never returns on this save.
- **Route chapters:** R1–R7 (10_CHOICES_ENDINGS §5). On the Ruin Route every main-route prompt after Ch15 is skipped except `:ch16_zekrom`,
  `:ch16_magnus`, `:ch17_nyx`, `:ch18_kestrel_ring`, `:ch19_oath` (only `:ruin` is offered) and `:ch21_crown`, whose Ruin scenes reuse the keys.
  Ruin game overs that reuse main-route triggers (Overtime, The Throne, Fair Bargain …) still fire and still count.
- **Choices:** `:ruin_voss`, `:ruin_walk`. Game overs: `GO_R_WELCOME_BEHIND`, `GO_R_KNEEL` (exempt).
- **Gyms 15–18** use version 1 of each leader (see §7). Badges are still awarded with `Prismfall.award_badge(n)` (caps unchanged); the badge
  art swaps to the black "Reflection" set when `ruin_route`.

---

## 12. Endings (1 good, 1 bad, 6 grey, 2 ruin)

```ruby
ENDINGS = {
  :END_HOMECOMING       => { :name => "Homecoming",             :kind => :good, :credits => true },
  :END_GILDED_CHAIN     => { :name => "The Gilded Chain",       :kind => :bad,  :credits => true },
  :END_UNFINISHED       => { :name => "Homecoming, Unfinished", :kind => :grey, :credits => true },
  :END_EMPTY_LIGHTHOUSE => { :name => "The Empty Lighthouse",   :kind => :grey, :credits => true },   # NEW
  :END_LONG_VIGIL       => { :name => "The Long Vigil",         :kind => :grey, :credits => true },
  :END_BORROWED_CROWN   => { :name => "The Borrowed Crown",     :kind => :grey, :credits => true },
  :END_HOLLOW_SPRING    => { :name => "The Hollow Spring",      :kind => :grey, :credits => true },
  :END_CONCORD_DAWN     => { :name => "Concord Dawn",           :kind => :grey, :credits => true },
  :END_UNMAKING         => { :name => "The Unmaking",           :kind => :ruin, :credits => true },
  :END_REFLECTION       => { :name => "The One Who Came Back",  :kind => :ruin, :credits => true }    # NEW, secret
}
ENDING_RULES = [
  [:END_REFLECTION,       "ruin_route && choice(:ruin_walk) == :reflection"],
  [:END_UNMAKING,         "ruin_route"],
  [:END_CONCORD_DAWN,     "choice(:ch21_hand) == :take || choice(:ch21_final) == :concord"],
  [:END_GILDED_CHAIN,     "flag(:ENGINE_CALIBRATED)"],
  [:END_HOLLOW_SPRING,    "choice(:ch21_final) == :unmake"],
  [:END_BORROWED_CROWN,   "choice(:ch21_final) == :borrowed"],
  [:END_LONG_VIGIL,       "choice(:ch21_final) == :keep"],
  [:END_UNFINISHED,       "choice(:ch21_final) == :return && (tally(:CONSENT) < 12 || resonance < 2 || (flag(:WAR_OCCUPATION) && !flag(:BOON_LIFTS_OCCUPATION)))"],
  [:END_EMPTY_LIGHTHOUSE, "choice(:ch21_final) == :return && flag(:KESTREL_LOST)"],
  [:END_HOMECOMING,       "choice(:ch21_final) == :return"]
]
DEFAULT_ENDING = :END_UNFINISHED   # unreachable in play; a safe fallback for debug jumps
```
Call sites: `END_CONCORD_DAWN` right after `:ch21_hand == :take`; `END_GILDED_CHAIN` when the `ARCEUS_GILDED` fight's scripted binding plays;
every other ending after `:ch21_final` (main) or `:ruin_walk` (Ruin). Each is `Prismfall.trigger_ending` with no ID.

**Post-game state** (Core writes FLAGS.md S263–S269 from the ending; `narrative[:postgame]` = the ending ID):

| Ending | S263 HOMECOMING_WORLD | S264 VIGIL_WORLD | S265 RUIN_WORLD | S266 Spire | S267 Gauntlet | S268 Distortion | S269 Concord Zero | Post-game? |
|---|---|---|---|---|---|---|---|---|
| HOMECOMING | ✓ | | | ✓ | ✓ | ✓ | ✓ | full |
| UNFINISHED | ✓ (refusing cities use Bleed-scar states) | | | ✓ | ✓ (refusers absent) | ✓ | ✓ | full |
| EMPTY_LIGHTHOUSE | ✓ | | | ✓ | ✓ | ✓ | ✓ | full (Kestrel absent; Hesper's lighthouse scene) |
| LONG_VIGIL | | ✓ | | ✓ | ✓ | ✓ | | full (the PC is Sovereign) |
| BORROWED_CROWN | | ✓ | | ✓ | ✓ (bearer absent) | ✓ | | full |
| HOLLOW_SPRING | | | | ✓ | ✓ | | | partial: no legendary rematches except Ogerpon/Loyal Three |
| CONCORD_DAWN | | | | ✓ | | | ✓ | partial: Spire only; the Wardens are pensioned off |
| GILDED_CHAIN | | | | | | | | none: credits → title (Ledger records it) |
| UNMAKING | | | ✓ | ✓ | ✓ | ✓ | | full (Antumbra mirrors open) |
| REFLECTION | | | ✓ | ✓ | ✓ | ✓ | | full, played as the Reflection |

## 13. Renames and changes vs the FLAGS.md crosswalk

| Crosswalk | Final | Why |
|---|---|---|
| `CH*_…` / `PRO_…` uppercase keys | same names, lowercase symbols (`:ch9_teo_sable`) | Core's choice keys are lowercase symbols |
| `CH13_REMEMBER` values `show / scared / not_yet` | unchanged | — |
| `CH19_OATH :ruin` | gated on `resonance <= -2` | needs a rule |
| `CH21_FINAL` | unchanged values; availability via `UNMAKE_OPEN`, `CONCORD_OPEN`, `BORROWED_OPEN` | — |
| outcome-only `ZEKROM_FREED` | `:ch16_zekrom => :freed` + `flag(:ZEKROM_FREED)` | Core stores choices only |
| outcome-only `CORVIN_FREED` | `:sq_doctors_cell` + flag | same |
| outcome-only `ILSA_RECONCILED` | `:sq_little_owl` + flag | same |
| outcome-only `DOMINAR_SWAYED` | `:ch19_dominar` + flag | same |
| outcome-only `ENVOY_PERSUADED` | `:ch20_envoy` + flag | same |
| outcome-only `PC_SPARED_VOSS` | `:ch21_spare_voss` + flag | same |
| outcome-only `KESTREL_ACCEPTED_SEAT`, `KESTREL_YSOLDE_RECONCILED`, `TAMSIN_PUBLIC_CONFESSION` | derived flags only | computed from Bonds/choices |
| `VOSS_FEIGNED`, `VOSS_ACCEPTED`, `TEO_SAVED`, `IRONREACH_EVIDENCE`, `ANJA_EXPOSED`, `KAITO_TESTIFIED`, `TELEMETRY_SABOTAGED`, `MAGNUS_EXPOSED`, `MAGNUS_KEPT_FAITH`, `NYX_BARGAIN_TAKEN`, `OGERPON_TRUSTED`, `MARCHETTI_TURNED` | derived flags of the same name | — |
| GO-01 … GO-22 | `GO_<NAME>` IDs in §9 | descriptive IDs; GO-20 Encore cut |
| (Rev 4–5) cameo entrants, `HEADLINE_CAMEO = :LIN`, the cameo draws, the Rev-4 outsiders (`:ISAURA :DREY :MIREILLE :THORNE`), Sigrun as Final stand-in, `GO_R_SWEET_DREAMS` | `HEADLINE_OPPONENT = :CELESTINE`, the Warden QF pool (§6.3), Brann sole stand-in, `GO_R_WELCOME_BEHIND` | Rev 4: cameos are sidequests; Rev 5: only established characters |
| (new) | `:ch2_matriarch`, `:ch11_strike`, `:ch13_fault`, `:ch20_calla`, `:ch21_hand`, `:ch21_reach_kestrel`, `:ch15_look_back`, `:ruin_voss`, `:ruin_walk`, `GO_WEATHER`, `GO_STAY_OUT`, `END_EMPTY_LIGHTHOUSE`, `END_REFLECTION` | see 10_CHOICES_ENDINGS |
| Core samples `:MOURNER` bond, `:SUCCESSOR`, `:MOURNER` entrant, `LEADER_ROWAN v50`, `KESTREL_FALLEN` conditions, all sample CHOICES/GAME_OVERS/ENDINGS | retired / replaced | — |
| (Rev 14) Saltmere/Briarwick chapter swap | **no renames.** `:ch3_juno_talk` (now Ch2), `:ch2_tamsin` and `:ch2_matriarch` (now Ch3) keep their names; only descriptions changed. `WARDEN_CONSENT` rows 1 and 2 swapped (Dorian, then Tamsin), with Core's `GYMS` | keys and IDs are stable across revisions; the consent list follows gym order |

## 14. Password additions (append to `Passwords::TABLE`)

| Word | ID | Effect |
|---|---|---|
| `ledgerhints` | :LEDGER_HINTS | the Ledger shows `:hint` for unfound game overs (also on automatically after any ending is seen) |
| `nomercy` | :NO_MERCY | `Prismfall.checkpoint` does nothing: a story game over sends you to your last *manual* save |
| `openbook` | :OPEN_BOOK | the Ties page shows numbers next to tiers (accessibility / theorycrafting) |
| `colorless` | :COLORLESS | Resonance deltas are halved (rounded toward 0): Harmony and Ruin are both harder to reach |
| `secondferry` | :SECOND_FERRY | only accepted if the Ledger has an ending: New Game+ carryover (10_CHOICES_ENDINGS §7.5) |

## 15. Validation checklist (for a Core debug command)

1. Every `choice(:k)`, `chose(:k, :v)`, `made(:k)` in any condition names a key in CHOICES, and `:v` is in its `:values`.
2. Every `flag()` / `tally()` name exists; no flag cycle.
3. Every Bond / faction ID in CHOICE_EFFECTS exists.
4. DRAWS: persons disjoint across stages (Core already checks); every candidate except `:ROWAN`, `:BRANN` and `:DASK` is seeded in BRACKET; no cameo or Rev-4 outsider entrant remains.
5. ENDING_RULES: the last main-route rule `choice(:ch21_final) == :return` plus the Concord/Gilded/other `:ch21_final` rules cover every value of `:ch21_final`.
6. `WARDEN_CONSENT.size == 18`.
