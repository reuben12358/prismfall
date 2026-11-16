#===============================================================================
# Prismfall Core - 008 Festival of Champions: data
#-------------------------------------------------------------------------------
# Edit this file to change entrants, seeding, scripted NPC results, rule sets
# and the finale. The player's path (SPINE, LOCKED):
#   R16 Juno -> QF headline cameo -> SF Kestrel -> Final Valen -> Hijack Voss
#   (:PRISM_ARENA) -> True finale Arceus (Lv 100)
# Festival.validate! checks that BRACKET seeding makes this path possible.
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
    # :rating                 used to simulate unscripted NPC-vs-NPC matches.
    # :level_hint             design note only (ace level for the trainer team).
    ENTRANTS = {
      :PLAYER    => { :display => nil, :rating => 0 },   # name = $player.name
      # Velmorans
      :JUNO      => { :display => "Juno",      :trainer_type => :RIVAL_JUNO,       :name => "Juno",      :rival_battle => 4, :rating => 88, :level_hint => 88 },
      :KESTREL   => { :display => "Kestrel",   :trainer_type => :RIVAL_KESTREL,    :name => "Kestrel",   :rival_battle => 8, :rating => 93, :level_hint => 93 },
      :VALEN     => { :display => "Valen",     :trainer_type => :CHAMPION_VALEN,   :name => "Valen",     :version => 0,      :rating => 99, :level_hint => 96 },
      # Wardens (NPC-only in the bracket; version 50 reserved, no trainer data
      # needed unless :exhibition is turned on)
      :KAITO     => { :display => "Kaito",     :trainer_type => :LEADER_KAITO,     :name => "Kaito",     :version => 50, :rating => 82 },
      :YSOLDE    => { :display => "Ysolde",    :trainer_type => :LEADER_YSOLDE,    :name => "Ysolde",    :version => 50, :rating => 83 },
      :NYX       => { :display => "Nyx",       :trainer_type => :LEADER_NYX,       :name => "Nyx",       :version => 50, :rating => 84 },
      :ODESSA    => { :display => "Odessa",    :trainer_type => :LEADER_ODESSA,    :name => "Odessa",    :version => 50, :rating => 83 },
      :CELESTINE => { :display => "Celestine", :trainer_type => :LEADER_CELESTINE, :name => "Celestine", :version => 50, :rating => 85 },
      :SIGRUN    => { :display => "Sigrun",    :trainer_type => :LEADER_SIGRUN,    :name => "Sigrun",    :version => 50, :rating => 87 },
      # Visiting champions (design/CAMEOS.md). Version scheme from CAMEOS.md:
      # 1 = R16/exhibition (~90), 2 = QF (~92), 3 = SF/Final-tier draw (~94),
      # 9 = post-game rematch. Draw candidates may override :version.
      # :exhibition_after_out => only offered once eliminated from the bracket.
      :LIN       => { :display => "Lin",       :trainer_type => :FESTIVAL_LIN,       :name => "Lin",       :version => 2, :rating => 97, :level_hint => 92 },  # headline (QF); post-game rematch only
      :AMARIA    => { :display => "Amaria",    :trainer_type => :FESTIVAL_AMARIA,    :name => "Amaria",    :version => 1, :exhibition => true, :exhibition_after_out => true, :rating => 89 },
      :SHELLY    => { :display => "Shelly",    :trainer_type => :FESTIVAL_SHELLY,    :name => "Shelly",    :version => 1, :exhibition => true, :exhibition_after_out => true, :exhibition_double => true, :rating => 90 },
      :ALEXANDRA => { :display => "Alexandra", :trainer_type => :FESTIVAL_ALEXANDRA, :name => "Alexandra", :version => 1, :exhibition => true, :exhibition_after_out => true, :rating => 92 },
      :VENAM     => { :display => "Venam",     :trainer_type => :FESTIVAL_VENAM,     :name => "Venam",     :version => 1, :exhibition => true, :exhibition_after_out => true, :rating => 90 },
      :SHIV      => { :display => "Shiv",      :trainer_type => :FESTIVAL_SHIV,      :name => "Shiv",      :version => 1, :exhibition => true, :exhibition_after_out => true, :rating => 93 },
      :GARRET    => { :display => "Garret",    :trainer_type => :FESTIVAL_GARRET,    :name => "Garret",    :version => 1, :exhibition => true, :exhibition_after_out => true, :rating => 89 },
      # Extra draw candidates (not seeded; exhibition-only when not drawn)
      :MELIA     => { :display => "Melia",     :trainer_type => :FESTIVAL_MELIA,     :name => "Melia",     :version => 1, :exhibition => true, :rating => 90 },
      :TITANIA   => { :display => "Titania",   :trainer_type => :FESTIVAL_TITANIA,   :name => "Titania",   :version => 1, :exhibition => true, :rating => 90 },
      :NOVA      => { :display => "Nova",      :trainer_type => :FESTIVAL_NOVA,      :name => "Nova",      :version => 3, :rating => 94 },   # Ruin Route only
      # Not a bracket entrant: the hijack
      :VOSS      => { :display => "Aurelian Voss",
                      :trainer_type => [:MERIDIAN_VOSS, :MERIDIAN_AURELIAN, :MERIDIAN_CEO],
                      :name => ["Aurelian", "Voss", "Aurelian Voss"], :version => 0, :rating => 98, :level_hint => 98 }
    }

    #---------------------------------------------------------------------------
    # Default seeding (CAMEOS.md "Default draw"): 16 slots, matches (0,1)
    # (2,3)...; quarters are 4 slots, halves 8. The choice-driven draw
    # (015_Festival_Draw.rb) can re-seat or replace the player's opponents.
    #---------------------------------------------------------------------------
    BRACKET = [
      :PLAYER,    :JUNO,       # R16 m0  (player)
      :LIN,       :NYX,        # R16 m1  -> Lin (QF opponent)
      :KESTREL,   :SHIV,       # R16 m2  -> Kestrel (SF opponent)
      :GARRET,    :KAITO,      # R16 m3  -> Garret
      :VALEN,     :ODESSA,     # R16 m4  -> Valen (Final opponent)
      :ALEXANDRA, :CELESTINE,  # R16 m5  -> Alexandra
      :SHELLY,    :VENAM,      # R16 m6  -> Venam
      :AMARIA,    :SIGRUN      # R16 m7  -> Sigrun
    ]

    # The quarterfinal opponent is "the headline cameo" (CAMEOS.md: Lin).
    HEADLINE_CAMEO = :LIN
    # Default opponent per bracket round (0 = R16 ... 3 = Final). Since
    # Revision 3 this is the FALLBACK of the choice-driven draw.
    PLAYER_PATH = [:JUNO, HEADLINE_CAMEO, :KESTREL, :VALEN]

    ROUND_NAMES = ["Round of 16", "Quarterfinals", "Semifinals", "Final"]

    # Scripted winners of NPC-vs-NPC matches, keyed by [round, match index].
    # Matches involving a drawn path entrant are always won by that entrant
    # (until they meet the player). Unscripted matches are simulated
    # (SIMULATE_UNSCRIPTED) or go to the higher :rating.
    SCRIPTED_WINNERS = {
      [0, 3] => :GARRET,     # Garret vs Kaito
      [0, 5] => :ALEXANDRA,  # Alexandra vs Celestine
      [0, 6] => :VENAM,      # Shelly vs Venam
      [0, 7] => :SIGRUN,     # Amaria vs Sigrun
      [1, 3] => :SIGRUN      # Venam vs Sigrun
    }
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
      { :id => :FINAL,  :round => 3, :name => "Final",        :ruleset => :bracket_final, :field => nil },
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
