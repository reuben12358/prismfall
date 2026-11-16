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
- **Effects strings** (§3) are space-separated tokens `ID+n` / `ID-n`: a Bond ID, a faction ID, or `RES` for Resonance. Bond and
  faction IDs never collide, so a token is unambiguous. Events may apply them by hand today (`pf_bond_add` …).

**[CORE+] requests** (each is a few lines; all are referenced below):
1. **`flag(:NAME)`** → evaluates `DERIVED_FLAGS[:NAME]` (a condition string) and returns true/false. Flags may reference other flags;
   validation must reject cycles.
2. **`tally(:NAME)`** → the number of strings in `TALLIES[:NAME]` that evaluate true (an integer).
3. **`drawn(:STAGE)`** → the entrant ID locked for a Festival stage (`state[:draws][stage]`), `nil` if not drawn yet.
4. **`:effects` on CHOICES** (optional): `pf_choose(key, value)` applies `CHOICE_EFFECTS[key][value]` once, with the
   "X will remember that." toast only when a Bond changes tier. Lets events stop hand-applying deltas.
5. **Festival draw extensions** (§8): `:vacates => :ENTRANT` on a candidate (the displaced default takes that entrant's seed; that
   entrant leaves and counts as `eliminated`), and `:live => true` on a stage (seed the default at `Festival.start`, resolve the
   candidate list when the stage's battle starts, like Hijack). Plus `EXHIBITION_EXTRAS` (§8.5) and `ARCEUS_VARIANTS` (§8.6).

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
Titania drawn at `<= -3`; Ruin "war" Arceus and the main-route Unmake option at `<= -6`; harmony battle buff at `>= 6`.

---

## 4. Choices (46 keys; ★ = MAJOR branch decision)

`:once => true` for all of them (a decision can't be re-made). "Gate" = when the prompt is offered (events check it); a value that
is a game-over trigger is not a stored value (the GO fires instead). Values marked *(only if …)* are hidden otherwise.

```ruby
CHOICES = {
  # ---- Prologue / Act I
  :pro_fellowship         => { :values => [:accept, :decline, :silent], :once => true, :description => "P: Voss's Meridian Fellowship card" },
  :ch2_matriarch          => { :values => [:soothe, :silence], :once => true, :description => "Ch2: the beaten Glass Matriarch - wait it out, or force the Imprint out" },
  :ch2_tamsin             => { :values => [:expose, :help_confess, :keep_secret], :once => true, :description => "Ch2: Tamsin's secret Lattice contract" },
  :ch3_juno_talk          => { :values => [:told, :deflect, :silent], :once => true, :description => "Ch3: tell Juno about the NULL scan" },
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
  :ruin_voss              => { :values => [:spare, :abandon], :once => true, :description => "R4: Voss kneels to Theodric's reflection" },
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
| `:ch20_envoy` `:proof` | the PC holds at least two of: Larch Papers (Ch12), Arbiter Blueprints (Ch16), Venam's testimony (Festival Day 2). |
| `:ch20_calla` | only if `choice(:ch16_rook) == :hold` OR `choice(:ch16_magnus) == :conscience` (Calla only defects if someone inside is already moving). |
| `:sq_little_owl` | the quest's earlier steps need `bond(:ILSA) >= 3` by Ch18. `:reconciled` needs `bond(:ILSA) >= 4` at the final step, else the event records `:refused`. |
| `:ch21_hand` | only if `flag(:VOSS_ACCEPTED)`. Without it, taking the hand is `GO_HIS_HAND`. |
| `:ch21_reach_kestrel` `:reach` | `choice(:ch18_kestrel_ring) == :keep` (the PC still has the ring) OR `choice(:ch12_letter) != :burn` (the PC can quote Morwen). |
| `:ch21_final` | `:return` `:keep` always; `:unmake` if `flag(:UNMAKE_OPEN)`; `:concord` if `flag(:CONCORD_OPEN)`; `:borrowed` if `flag(:BORROWED_OPEN)`. |

### 4.2 Effects (transcribe as `CHOICE_EFFECTS`, or apply by hand)

Deferred deltas (applied by a later event that reads the choice) are listed after "→".

```ruby
CHOICE_EFFECTS = {
  :pro_fellowship         => { :accept => "MERIDIAN+2 VOSS+1", :decline => "VOSS+2", :silent => "MERIDIAN+1" },
  :ch2_matriarch          => { :soothe => "RES+1", :silence => "RES-2 ACCORD+1" },
  :ch2_tamsin             => { :expose => "HOLLOW+1 ACCORD+1 MERIDIAN-1", :help_confess => "ACCORD+1", :keep_secret => "MERIDIAN+1" },
  :ch3_juno_talk          => { :told => "JUNO+2", :deflect => "JUNO-1", :silent => "" },
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
  :KESTREL_YSOLDE_RECONCILED=> "!flag(:KESTREL_FALLEN) && bond(:KESTREL) >= 5 && bond(:YSOLDE) >= 4",
  :KESTREL_BEARS            => "!flag(:KESTREL_FALLEN) && bond(:KESTREL) >= 8",
  :SIGRUN_BEARS             => "!flag(:KESTREL_BEARS) && bond(:SIGRUN) >= 6",
  :KESTREL_ACCEPTED_SEAT    => "flag(:KESTREL_YSOLDE_RECONCILED) && !flag(:KESTREL_LOST) && !(choice(:ch21_final) == :borrowed && flag(:KESTREL_BEARS))",
  # Act V
  :DOMINAR_SWAYED           => "choice(:ch19_dominar) == :swayed",
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
  :HARMONY_BUFF             => "resonance >= 6"
}

# Wardens' Consent, gym order (index = gym - 1). A Warden who doesn't consent refuses to release their Plate in the Arceus fight.
WARDEN_CONSENT = [
  "choice(:ch2_tamsin) != :keep_secret",                          #  1 Tamsin  - the pylon still drains Briarwick; she can't afford to let go
  "choice(:ch5_lowlight_testimony) != :mourner",                  #  2 Dorian  - you told the official story on record; he keeps the lie he knows
  "flag(:TEO_SAVED) || bond(:MARISOL) >= 3",                      #  3 Marisol
  "flag(:ROOK_CUTS_GRID) || flag(:MARCHETTI_TURNED)",             #  4 Rook    - the Zap Plate is in Meridian's vault; he can only release what he can reach
  "choice(:ch6_drillsite) != :directorate",                       #  5 Sahar
  "flag(:CORVIN_FREED)",                                          #  6 Corvin  - otherwise a Choir porter carries his Plate and can't release it
  "choice(:ch8_lightstone) != :dominar",                          #  7 Brann
  "flag(:KAITO_TESTIFIED)",                                       #  8 Kaito   - a man who never confessed can't let go
  "bond(:JUNO) >= 0",                                             #  9 Juno
  "choice(:ch11_anja) == :let_confess",                           # 10 Anja    - "Rimeholt drowns without it."
  "choice(:ch12_letter) != :burn",                                # 11 Odessa  - you burned a dead letter
  "flag(:ILSA_RECONCILED) || bond(:ILSA) >= 5",                   # 12 Ilsa
  "choice(:ch14_telemetry) != :leave",                            # 13 Bastian - you walked a Meridian beacon into his seams
  "!flag(:KESTREL_FALLEN) || choice(:ch21_reach_kestrel) == :reach", # 14 Ysolde
  "flag(:MAGNUS_KEPT_FAITH)",                                     # 15 Magnus  - "I won't hand my city's future to a god."
  "flag(:NYX_BARGAIN_TAKEN) || bond(:NYX) >= 4",                  # 16 Nyx
  "resonance >= 2",                                               # 17 Celestine - she hears which key you sing in
  "choice(:ch19_oath) != :keep && choice(:ch19_oath) != :ruin"    # 18 Sigrun
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
