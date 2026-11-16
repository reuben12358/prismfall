#===============================================================================
# Prismfall Core - 012 Narrative data
#-------------------------------------------------------------------------------
# Transcribed from design/NARRATIVE_KEYS.md (Narrative Systems; rationale in
# story/10_CHOICES_ENDINGS.md). Section numbers below refer to that file.
# Re-transcribe when it changes; Prismfall::NarrativeCheck.run (debug menu
# "Show Core status") validates the tables (NARRATIVE_KEYS section 15).
# Festival draw data lives in 015_Festival_Draw.rb.
#===============================================================================
module Prismfall
  module Narrative
    WARN_UNREGISTERED = true   # console warning for keys missing from the tables
    HISTORY_LIMIT     = 300    # entries kept in the change history (debug aid)

    #---------------------------------------------------------------------------
    # 1. Bonds (10)
    #---------------------------------------------------------------------------
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

    #---------------------------------------------------------------------------
    # 2. Standing
    #---------------------------------------------------------------------------
    STANDING_DEFAULT = { :min => -10, :max => 10, :start => 0 }
    FACTIONS = {
      :HOLLOW   => { :name => "the Hollow" },
      :MERIDIAN => { :name => "the Meridian Concord", :start => 1 },
      :ACCORD   => { :name => "the Accord", :start => 1 }
    }
    # enemy -10..-6 | distrusted -5..-2 | neutral -1..1 | trusted 2..4 | ally 5..10
    STANDING_TIERS = [[-10, :enemy], [-5, :distrusted], [-1, :neutral], [2, :trusted], [5, :ally]]

    #---------------------------------------------------------------------------
    # 3. Resonance: -10 (Ruin) .. +10 (Harmony)
    #---------------------------------------------------------------------------
    RESONANCE_MIN   = -10
    RESONANCE_MAX   = 10
    RESONANCE_START = 0
    RESONANCE_BANDS = [[-10, :ruin], [-5, :ruin_leaning], [-1, :balanced], [2, :harmony_leaning], [6, :harmony]]
    # ruin -10..-6 | ruin_leaning -5..-2 | balanced -1..1 | harmony_leaning 2..5 | harmony 6..10

    #---------------------------------------------------------------------------
    # 4. Choices (48, all :once). Gates (4.1) are checked by events.
    #---------------------------------------------------------------------------
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

    # 4.2 Effects, applied once by pf_choose (tokens ID+n / ID-n; RES = Resonance).
    # Toast "X will remember that." only when a Bond changes tier.
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

    # Legacy / map-builder keys -> canonical keys (design/MAPGEN.md). Events using
    # a LEGACY alias already apply their own deltas, so CHOICE_EFFECTS are not
    # auto-applied for them (avoids double counting) until they're migrated.
    CHOICE_ALIASES = {
      :PRO_FELLOWSHIP      => :pro_fellowship,
      :CH2_TAMSIN          => :ch2_tamsin,
      :CH3_JUNO_TALK       => :ch3_juno_talk,
      :CH4_KESTREL_MOURNER => :ch4_kestrel_mourner,
      :CH4_TEO             => :ch4_teo
    }
    LEGACY_ALIASES_SKIP_EFFECTS = true

    #---------------------------------------------------------------------------
    # 5. Derived flags (flag(:X)) and tallies (tally(:X))
    #---------------------------------------------------------------------------
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
      :HARMONY_BUFF             => "resonance >= 6",
      :ZYGARDE_CHOOSES          => "bond(:VALEN) >= 3 || flag(:ILSA_RECONCILED)",
      :JUNO_ESTRANGED           => "bond(:JUNO) <= -5"   # Ch11: she travels apart; the Thaw partner is Anja
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

    # Core-written mirror switches (design/FLAGS.md S221-S228), refreshed on every
    # narrative change. Events read them, never write them.
    MIRROR_SWITCHES = {
      221 => "flag(:TEO_SAVED)",
      222 => "flag(:CORVIN_FREED)",
      223 => "flag(:OGERPON_TRUSTED)",
      224 => "flag(:MARCHETTI_TURNED)",
      225 => "flag(:MAGNUS_KEPT_FAITH)",
      226 => "flag(:DOMINAR_SWAYED)",
      227 => "flag(:ILSA_RECONCILED)",
      228 => "flag(:KESTREL_REDEEMED)"
    }
    MIRRORS_ENABLED = true

    #---------------------------------------------------------------------------
    # 9. Game overs (23 canonical + 2 Ruin-only, :ruin_exempt)
    #---------------------------------------------------------------------------
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
                                :epitaph => "You knelt. The Aureate Kingdom stepped through the Glass, golden and starving, and Theodric finished his sentence." }
    }

    # Map-builder IDs -> canonical game-over IDs (design/MAPGEN.md).
    GAME_OVER_ALIASES = {
      :GO_LAST_FERRY => :GO_HOMEWARD,
      :GO_BLEED_TIDE => :GO_ORCHARD
    }

    #---------------------------------------------------------------------------
    # 12. Endings (1 good, 1 bad, 6 grey, 2 ruin) + rules
    #---------------------------------------------------------------------------
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
      [:END_UNFINISHED,       "choice(:ch21_final) == :return && (tally(:CONSENT) < 12 || resonance < 2)"],
      [:END_EMPTY_LIGHTHOUSE, "choice(:ch21_final) == :return && flag(:KESTREL_LOST)"],
      [:END_HOMECOMING,       "choice(:ch21_final) == :return"]
    ]
    DEFAULT_ENDING = :END_UNFINISHED   # unreachable in play; a safe fallback for debug jumps

    # Post-game switches (design/FLAGS.md S263-S269) set by trigger_ending.
    # 263 HOMECOMING_WORLD, 264 VIGIL_WORLD, 265 RUIN_WORLD, 266 Spire,
    # 267 Gauntlet, 268 Distortion, 269 Concord Zero.
    POSTGAME_SWITCHES = {
      :END_HOMECOMING       => [263, 266, 267, 268, 269],
      :END_UNFINISHED       => [263, 266, 267, 268, 269],
      :END_EMPTY_LIGHTHOUSE => [263, 266, 267, 268, 269],
      :END_LONG_VIGIL       => [264, 266, 267, 268],
      :END_BORROWED_CROWN   => [264, 266, 267, 268],
      :END_HOLLOW_SPRING    => [266, 267],
      :END_CONCORD_DAWN     => [266, 269],
      :END_GILDED_CHAIN     => [],
      :END_UNMAKING         => [265, 266, 267, 268],
      :END_REFLECTION       => [265, 266, 267, 268]
    }
    POSTGAME_ALL_SWITCHES = (263..269).to_a
    # Endings with no post-game: credits, then back to the title.
    NO_POSTGAME_ENDINGS = [:END_GILDED_CHAIN]

    #---------------------------------------------------------------------------
    # Sidequest cameo fights (SPINE Revision 4: not in the Festival).
    # trainer type => display name; Ledger records the first win of each.
    #---------------------------------------------------------------------------
    CAMEOS = {
      :FESTIVAL_LIN       => "Lin",
      :FESTIVAL_AMARIA    => "Amaria",
      :FESTIVAL_SHELLY    => "Shelly",
      :FESTIVAL_ALEXANDRA => "Alexandra",
      :FESTIVAL_VENAM     => "Venam",
      :FESTIVAL_SHIV      => "Shiv",
      :FESTIVAL_GARRET    => "Garret",
      :FESTIVAL_MELIA     => "Melia",
      :FESTIVAL_TITANIA   => "Titania",
      :FESTIVAL_NOVA      => "Nova"
    }
  end
end
