#===============================================================================
# Prismfall Core - 008 Festival of Champions: data
#-------------------------------------------------------------------------------
# Edit this file to change entrants, seeding, scripted NPC results, rule sets
# and the finale. The player's path (SPINE, LOCKED):
#   Default (fallback) path: R16 Juno -> QF Isaura -> SF Kestrel -> Final Valen
#   -> Hijack Voss (:PRISM_ARENA) -> True finale Arceus (Lv 100). The actual
#   opponents come from the choice-driven draw (015_Festival_Draw.rb).
# SPINE Revision 4: original characters only (no sister-game cameos; those are
# sidequest fights via Prismfall.cameo_battle). Data: NARRATIVE_KEYS.md sec. 6.
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
      # Rivals / Champion
      :JUNO      => { :display => "Juno",      :trainer_type => :RIVAL_JUNO,       :name => "Juno",      :rival_battle => 4, :rating => 88, :level_hint => 90 },   # J4 = 40-42
      :KESTREL   => { :display => "Kestrel",   :trainer_type => :RIVAL_KESTREL,    :name => "Kestrel",   :rival_battle => 8, :rating => 93, :level_hint => 94 },   # K8 = 80-82
      :VALEN     => { :display => "Valen",     :trainer_type => :CHAMPION_VALEN,   :name => "Valen",     :version => 0,      :rating => 99, :level_hint => 96 },
      # Wardens (version 50 = NPC-only placeholder; draws pass their own :version)
      :KAITO     => { :display => "Kaito",     :trainer_type => :LEADER_KAITO,     :name => "Kaito",     :version => 50, :rating => 85 },
      :NYX       => { :display => "Nyx",       :trainer_type => :LEADER_NYX,       :name => "Nyx",       :version => 50, :rating => 84 },
      :ODESSA    => { :display => "Odessa",    :trainer_type => :LEADER_ODESSA,    :name => "Odessa",    :version => 50, :rating => 83 },
      :CELESTINE => { :display => "Celestine", :trainer_type => :LEADER_CELESTINE, :name => "Celestine", :version => 50, :rating => 87 },
      :SIGRUN    => { :display => "Sigrun",    :trainer_type => :LEADER_SIGRUN,    :name => "Sigrun",    :version => 50, :rating => 89 },
      :MARISOL   => { :display => "Marisol",   :trainer_type => :LEADER_MARISOL,   :name => "Marisol",   :version => 90, :rating => 84, :level_hint => 90 },
      :ANJA      => { :display => "Anja",      :trainer_type => :LEADER_ANJA,      :name => "Anja",      :version => 90, :rating => 84, :level_hint => 90 },
      :YSOLDE    => { :display => "Ysolde",    :trainer_type => :LEADER_YSOLDE,    :name => "Ysolde",    :version => 92, :rating => 86, :level_hint => 92 },
      # Original foreign entrants (Envoy Okoro's Concert delegation) + the Queen's Champion
      :ISAURA    => { :display => "Isaura",    :trainer_type => :FESTIVAL_ISAURA,   :name => "Isaura",   :version => 2, :exhibition => true, :rating => 96, :level_hint => 92 },  # headline (QF)
      :DREY      => { :display => "Drey",      :trainer_type => :FESTIVAL_DREY,     :name => "Matthias", :version => 1, :exhibition => true, :rating => 91, :level_hint => 90 },
      :MIREILLE  => { :display => "Mireille",  :trainer_type => :FESTIVAL_MIREILLE, :name => "Mireille", :version => 2, :exhibition => true, :rating => 88, :level_hint => 92 },
      :THORNE    => { :display => "Thorne",    :trainer_type => :FESTIVAL_THORNE,   :name => "Ivo",      :version => 1, :exhibition => true, :rating => 86, :level_hint => 90 },
      # Draw-only (never in the default seeding)
      :ROWAN     => { :display => "The Gardener",  :trainer_type => :LEADER_ROWAN,  :name => "Rowan", :version => 90, :rating => 88, :level_hint => 90 },
      :DASK      => { :display => "Archseer Dask", :trainer_type => :ARCHSEER_DASK, :name => "Imre",  :version => 92, :rating => 92, :level_hint => 92 },   # Ruin only
      :KESTREL_FALLEN => { :display => "Kestrel", :person => :KESTREL, :trainer_type => :RIVAL_KESTREL, :name => "Kestrel", :rival_battle => 9, :rating => 95, :level_hint => 94 },  # 90-92
      :BRANN     => { :display => "Brann",     :trainer_type => :LEADER_BRANN,     :name => "Brann",     :version => 96, :rating => 90, :level_hint => 96 },
      :VALEN_RUIN => { :display => "Valen",    :person => :VALEN, :trainer_type => :CHAMPION_VALEN, :name => "Valen", :version => 1, :rating => 99, :level_hint => 96 },
      # Hijackers (not bracket entrants)
      :VOSS      => { :display => "Aurelian Voss",
                      :trainer_type => [:MERIDIAN_VOSS, :MERIDIAN_AURELIAN, :MERIDIAN_CEO],
                      :name => ["Aurelian", "Voss", "Aurelian Voss"], :version => 0, :rating => 98, :level_hint => 100 },
      :QUENT     => { :display => "Dr. Quent", :trainer_type => :MERIDIAN_QUENT,  :name => "Percival", :version => 99, :rating => 97, :level_hint => 100 },
      :THEODRIC  => { :display => "Theodric",  :trainer_type => :GILDED_THEODRIC, :name => "Theodric", :version => 0,  :rating => 99, :level_hint => 100 },
      # Exhibition-only (never seeded)
      :MORWEN       => { :display => "Morwen",  :trainer_type => :ECHO_MORWEN,    :name => "Morwen",  :version => 90, :exhibition => true, :rating => 0 },
      :BASTIAN      => { :display => "Bastian", :trainer_type => :LEADER_BASTIAN, :name => "Bastian", :version => 90, :exhibition => true, :rating => 0 },
      :PAGEANT_BOUT => { :display => "Dorian & Rook", :double => true, :trainer_type => [:LEADER_DORIAN, :LEADER_ROOK],
                         :name => ["Dorian", "Rook"], :version => 90, :exhibition => true, :rating => 0 }
    }

    #---------------------------------------------------------------------------
    # Default seeding (NARRATIVE_KEYS 6.2): 16 slots, matches (0,1) (2,3)...;
    # quarters are 4 slots, halves 8. The draw swaps drawn opponents in.
    #---------------------------------------------------------------------------
    BRACKET = [
      :PLAYER,   :JUNO,       # R16 m0  (player; J4)
      :ISAURA,   :NYX,        # R16 m1  -> Isaura (default QF opponent)
      :KESTREL,  :DREY,       # R16 m2  -> Kestrel (Gauntlet)
      :KAITO,    :MARISOL,    # R16 m3
      :VALEN,    :ODESSA,     # R16 m4  -> Valen
      :MIREILLE, :CELESTINE,  # R16 m5
      :YSOLDE,   :ANJA,       # R16 m6
      :THORNE,   :SIGRUN      # R16 m7  -> Sigrun beats the Queen's Champion
    ]

    HEADLINE_OPPONENT = :ISAURA
    # Default opponent per bracket round (0 = R16 ... 3 = Final). Fallback of the draw.
    PLAYER_PATH = [:JUNO, HEADLINE_OPPONENT, :KESTREL, :VALEN]

    ROUND_NAMES = ["Round of 16", "Quarterfinals", "Semifinals", "Final"]

    # Scripted winners of NPC-vs-NPC matches, keyed by [round, match index].
    # Drawn path opponents always win until they meet the player; the rest
    # simulate (SIMULATE_UNSCRIPTED) or go to the higher :rating.
    SCRIPTED_WINNERS = { [0, 3] => :KAITO, [0, 5] => :CELESTINE, [0, 6] => :YSOLDE, [0, 7] => :SIGRUN,
                         [1, 2] => :VALEN, [1, 3] => :SIGRUN }
    SIMULATE_UNSCRIPTED = true   # false = higher :rating always wins
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
