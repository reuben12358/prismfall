#===============================================================================
# Prismfall Core - 008 Festival of Champions: data
#-------------------------------------------------------------------------------
# Edit this file to change entrants, seeding, scripted NPC results, rule sets
# and the finale. The player's path (SPINE, LOCKED):
#   Default (fallback) path: R16 Juno -> QF Celestine -> SF Kestrel -> Final Valen
#   -> Hijack Voss (:PRISM_ARENA) -> True finale Arceus (Lv 100). The actual
#   opponents come from the choice-driven draw (015_Festival_Draw.rb).
# SPINE Revisions 5-6: the Festival chooses who receives Arceus's Blessing. 16
# seats = the player + 15 kingdom delegates (two per kingdom + the Sovereign),
# all story-met characters; who each kingdom sends depends on the player's
# choices (DELEGATIONS). No cameos or outsiders. Data: NARRATIVE_KEYS.md sec. 6.
# Festival.validate checks that BRACKET seeding makes the default path possible.
#===============================================================================
module Prismfall
  module Festival
    #---------------------------------------------------------------------------
    # Entrants
    #---------------------------------------------------------------------------
    # :trainer_type / :name   may be arrays of candidates; the first combination
    #                         that exists in trainers.txt is used (for the
    #                         version being loaded); otherwise the first one.
    # :version                Standard base version for the bracket battle.
    # :rival_battle           use the rival scheme (N*10 + starter slot) instead.
    # :exhibition             true = can be fought in exhibition matches.
    # :exhibition_version     version for exhibitions (defaults to :version).
    # :double                 with array :trainer_type/:name = a 2-trainer
    #                         double battle (exhibition Pageant Bout).
    # :person                 variants of one character share a person.
    # :rating                 used to simulate unscripted NPC-vs-NPC matches.
    # :level_hint             design note only (ace level for the trainer team).
    ENTRANTS = {
      :PLAYER    => { :display => nil, :rating => 0 },   # name = $player.name
      :JUNO      => { :display => "Juno",    :trainer_type => :RIVAL_JUNO,     :name => "Juno",    :rival_battle => 4, :rating => 88, :level_hint => 90 },   # J4 = 40-42
      :KESTREL   => { :display => "Kestrel", :trainer_type => :RIVAL_KESTREL,  :name => "Kestrel", :rival_battle => 8, :rating => 93, :level_hint => 94 },   # K8 = 80-82
      :VALEN     => { :display => "Valen",   :trainer_type => :CHAMPION_VALEN, :name => "Valen",   :version => 0,      :rating => 99, :level_hint => 96 },
      # Wardens whose teams exist at v92 (QF draws); NPC-only otherwise
      :KAITO     => { :display => "Kaito",   :trainer_type => :LEADER_KAITO,   :name => "Kaito",   :version => 92, :rating => 85, :level_hint => 92 },
      :SIGRUN    => { :display => "Sigrun",  :trainer_type => :LEADER_SIGRUN,  :name => "Sigrun",  :version => 92, :rating => 89, :level_hint => 92 },
      :ODESSA    => { :display => "Odessa",  :trainer_type => :LEADER_ODESSA,  :name => "Odessa",  :version => 92, :rating => 83, :level_hint => 92 },
      :NYX       => { :display => "Nyx",     :trainer_type => :LEADER_NYX,     :name => "Nyx",     :version => 50, :rating => 84 },   # NPC-only (v50 = no team)
      # NARRATIVE_KEYS 6.1 (version 50 = NPC-only, no trainer data)
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
                         :version => 90, :exhibition => true, :rating => 0 },
      # Hijack default
      :VOSS      => { :display => "Aurelian Voss", :trainer_type => :MERIDIAN_VOSS, :name => "Aurelian", :version => 0, :rating => 98, :level_hint => 100 }
    }

    #---------------------------------------------------------------------------
    # Delegations (NARRATIVE_KEYS 6.1): per seat, the first candidate whose
    # condition holds and who isn't seated yet. :FORFEIT = the Accord lends the
    # seat to the first unseated entrant of FORFEIT_POOL (resolved last).
    #---------------------------------------------------------------------------
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
    FORFEIT_POOL = [:DORIAN, :TAMSIN, :ROOK, :ODESSA, :ILSA, :NYX, :CORVIN]

    # Seating when no choice has been made yet (shown before the Festival starts).
    BRACKET = [:PLAYER, :JUNO, :CELESTINE, :SAHAR, :ILSA, :ODESSA, :KAITO, :BASTIAN,
               :VALEN, :KESTREL, :NYX, :MARISOL, :ANJA, :BRANN, :YSOLDE, :SIGRUN]

    ROUND_NAMES = ["Round of 16", "Quarterfinals", "Semifinals", "Final"]

    # NPC-vs-NPC results: drawn path opponents win until they meet the player,
    # then the first MATCH_RULES row (015) for the pair, then SCRIPTED_WINNERS
    # (kept for overrides), then the higher :rating.
    SCRIPTED_WINNERS = {}
    SIMULATE_UNSCRIPTED = false  # false = higher :rating always wins
    SIMULATION_SHARPNESS = 6     # higher = favourites win more often

    #---------------------------------------------------------------------------
    # Rule sets
    #---------------------------------------------------------------------------
    #   :level_cap    party Pokémon above this can't enter (if :enforce_level);
    #                 a cap of FESTIVAL_FINALE_CAP unlocks the finale cap
    #   :bag_items    false = setBattleRule("noBagItems")
    #   :can_lose     true = losing doesn't black out (the match can be retried)
    #   :heal_before / :heal_after  full party heal
    #   :exp          false = setBattleRule("noExp")
    #   :money        false = setBattleRule("noMoney")
    RULESETS = {
      # The cap rises each round to match that round's ace (R16 90 -> QF 92 -> SF 94 -> Final 96).
      :bracket    => { :level_cap => 90,  :enforce_level => true, :bag_items => false, :can_lose => true,
                       :heal_before => true, :heal_after => true, :exp => true, :money => false },
      :bracket_qf => { :level_cap => 92,  :enforce_level => true, :bag_items => false, :can_lose => true,
                       :heal_before => true, :heal_after => true, :exp => true, :money => false },
      :bracket_sf => { :level_cap => 94,  :enforce_level => true, :bag_items => false, :can_lose => true,
                       :heal_before => true, :heal_after => true, :exp => true, :money => false },
      :bracket_final => { :level_cap => 96, :enforce_level => true, :bag_items => false, :can_lose => true,
                          :heal_before => true, :heal_after => true, :exp => true, :money => false },
      :finale     => { :level_cap => 100, :enforce_level => true, :bag_items => false, :can_lose => true,
                       :heal_before => true, :heal_after => true, :exp => true, :money => false },
      # Exhibitions happen between rounds; no level gate so a party raised for later rounds can still enter.
      :exhibition => { :level_cap => nil, :enforce_level => false, :bag_items => false, :can_lose => true,
                       :heal_before => true, :heal_after => true, :exp => true, :money => false }
    }

    #---------------------------------------------------------------------------
    # Player stages (in order). Bracket stages take their opponent from
    # PLAYER_PATH[round]; other stages name an :opponent entrant or a :wild boss.
    #   :field  battle field (needs Prismfall Field Effects; ignored otherwise)
    #---------------------------------------------------------------------------
    STAGES = [
      { :id => :R16,    :round => 0, :name => "Round of 16",  :ruleset => :bracket, :field => nil },
      { :id => :QF,     :round => 1, :name => "Quarterfinal", :ruleset => :bracket_qf, :field => nil },
      { :id => :SF,     :round => 2, :name => "Semifinal",    :ruleset => :bracket_sf, :field => nil },
      { :id => :FINAL,  :round => 3, :name => "Final",        :ruleset => :bracket_final, :field => nil, :live => true },  # drawn on Day 7
      { :id => :HIJACK, :opponent => :VOSS, :name => "The Hijack", :ruleset => :finale, :field => :PRISM_ARENA },
      { :id => :ARCEUS, :wild => :ARCEUS, :level => 100, :name => "True Finale", :ruleset => :finale,
        :field => :PRISM_ARENA, :rules => ["cannotRun", "disablePokeBalls"],
        # With EBDX installed this runs EliteBattle.bossBattle (boss databox,
        # stat boost, status immunities, uncatchable); without EBDX a normal
        # wild battle against ARCEUS_SETUP's Pokémon. :boss => nil disables.
        :boss => { :player_side => 1, :can_catch => false,
                   :options => { :bossboost => { :HP => 2.0, :ATTACK => 1.25, :DEFENSE => 1.25,
                                                 :SPECIAL_ATTACK => 1.25, :SPECIAL_DEFENSE => 1.25, :SPEED => 1.1 } } } }
    ]

    # Called with the Arceus Pokémon object before the boss battle. Story/field
    # teams can replace this (or add an EventHandlers :prismfall_festival_boss
    # handler, which receives the same Pokémon).
    ARCEUS_SETUP = proc { |pkmn|
      GameData::Stat.each_main { |s| pkmn.iv[s.id] = Pokemon::IV_STAT_LIMIT }
      pkmn.calc_stats
      pkmn.heal
    }
  end
end
