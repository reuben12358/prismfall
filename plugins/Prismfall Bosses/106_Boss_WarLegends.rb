#===============================================================================
# The war legendaries on the Glass Dunes (map 926, Ch19; SPINE Revision 18).
# story/14_WAR_AND_BLESSING.md "The battle": the PC fights whichever legendary
# is about to fire on the other army - Reshiram by default, Kyogre if backing
# Ashkaar. Both start on 926's own field (DESERT; no :field here) and walk the
# fields team's sequence (Field Effects 106 / 139 / 140):
#   DESERT -> the flood-sea (FLOODED_DUNES) -> the glass (GLASS_DUNES).
# Events (after the WAR-1 cutscene beat that wakes the legend):
#   Script: Prismfall::Bosses.wild_battle(:RESHIRAM_GLASS_DUNES)
#   Script: Prismfall::Bosses.wild_battle(:KYOGRE_GLASS_DUNES)        # backing Ashkaar
#   then Prismfall::Bosses.last_result[:result] == :turned_back
# Neither is caught here: Reshiram goes to Sigrun after the truce, Kyogre back
# to the sea (story/08 and 14).
#
# Balance (trainer designer, round 3): cap 85, the player's six against three
# bars. The flood stacks with rain (Water x1.3 x1.5 = x1.95, Surf x1.2 more)
# and an EV-trained Modest Primal Kyogre one-shot a Lv 85 Reshiram there in the
# fields team's harness, so both legends are built to trade blows, not to
# sweep: Calm natures, no Sp. Atk EVs, HP / Sp. Def EVs, the signature move
# arriving with the break that changes the field, and on Kyogre the rain
# clearing as the sea comes in (the sea holds itself up while Kyogre feeds it
# Water attacks). Hard keeps an edge (Reshiram x1.15 Sp. Atk; both bulkier; Kyogre's last
# bar adds Sp. Atk +1). Neither fight uses the Primal form: Primordial Sea
# over the flood one-shot everything neutral (Hard 0 of 8 in the harness), so
# the Primal is the cutscene's (WAR-1). Reshiram has extra HP (x1.35 Standard):
# it is weak to the Dragon / Ground / Rock moves every late team carries.
# Per-hit damage, Standard, vs a neutral Lv 85 (HP 305, Sp. Def 176):
#   Reshiram: Flamethrower on the sand ~63%; Blue Flare on the flood ~76%, on
#             the glass ~91%, and only ~45% while the sea-storm's rain lasts.
#   Kyogre:   Surf in Drizzle's rain (the dunes bloom) ~79%; Origin Pulse on
#             the flood once the rain is gone ~84%; resisted ~40%.
#===============================================================================
module Prismfall
  module Bosses
    # The sea comes in and the storm that brought it passes: ends rain (not a
    # Primal's heavy rain) so the flood and the rain don't stack.
    WAR_RAIN_PASSES = proc do |battle, _b, _st|
      if [:Rain].include?(battle.field.weather)
        battle.field.weather = :None
        battle.field.weatherDuration = 0
        battle.pbDisplay(_INTL("The rain blows over. The sea stays."))
      end
    end
  end
end

Prismfall::Bosses.register(:RESHIRAM_GLASS_DUNES, {
  :species    => :RESHIRAM,
  :level      => 85,
  :ability    => :TURBOBLAZE,
  :nature     => :CALM,
  :ivs        => 31,
  :evs        => { :HP => 252, :SPECIAL_DEFENSE => 252, :SPEED => 4 },
  # Bar 1 on the dry dunes: no searing move yet, so the sand stays sand until the sea comes (story order).
  :moves      => [:FLAMETHROWER, :DRAGONPULSE, :EARTHPOWER, :EXTRASENSORY],
  :bars       => { :CASUAL => 2, :default => 3 },
  # Weak to Dragon, Ground and Rock, which every late team carries: without the extra bulk a Life Orb Garchomp broke a
  # bar per Dragon Claw (3 bars in 4.5 turns in the harness).
  :stat_mults => { :CASUAL => { :HP => 1.15 }, :STANDARD => { :HP => 1.35, :DEFENSE => 1.1, :SPECIAL_DEFENSE => 1.1 },
                   :HARD => { :HP => 1.5, :SPECIAL_ATTACK => 1.15, :DEFENSE => 1.2, :SPECIAL_DEFENSE => 1.2 } },
  :catch      => false,
  :intro      => ["The Light Stone cracks white in the Dominar's hand...",
                  "Reshiram unfolds over the Siege Camp, and turns toward the Isenmar lines!"],
  :on_break   => { :cure_status => true, :reset_stats => :negative },
  :breaks     => {
    # Kyogre's flood-sea arrives with its storm; the Light Stone answers. Blue Flare (white fire) glasses the flood
    # in one (the AI scores it +16 there), even while the rain halves it.
    1 => { :messages => ["The Northern Sea stands up on the horizon - Kyogre's flood-sea is pouring over the dunes!",
                         "The Light Stone blazes white! Reshiram's fire burns white-hot!"],
           :field => :FLOODED_DUNES, :field_message => "", :weather => :Rain,
           :learn => { 0 => :BLUEFLARE } },
    # The last bar (Standard / Hard): Turboblaze rings in the glass.
    2 => { :messages => ["Reshiram roars, and the glass dunes ring with the fire that made them!"],
           :learn => { 3 => :FUSIONFLARE }, :stats => { :SPECIAL_DEFENSE => 1 } }
  },
  :on_defeat  => [
    { :messages => ["{1}'s white fire gutters out...", "It turns away from the armies and climbs into the steam."],
      :end_battle => 1, :result => :turned_back }
  ]
})

Prismfall::Bosses.register(:KYOGRE_GLASS_DUNES, {
  :species    => :KYOGRE,
  :level      => 85,
  :ability    => :DRIZZLE,
  :nature     => :CALM,
  :ivs        => 31,
  :evs        => { :HP => 252, :SPECIAL_DEFENSE => 252, :DEFENSE => 4 },
  # Bar 1: Drizzle's rain soaks the dunes into the Superbloom (Grass x1.5 for the player's answers); Surf is a flood.
  :moves      => [:SURF, :ICEBEAM, :THUNDER, :AQUARING],
  :bars       => { :CASUAL => 2, :default => 3 },
  :stat_mults => { :HARD => { :HP => 1.1, :DEFENSE => 1.1, :SPECIAL_DEFENSE => 1.1 } },   # Sp. Atk x1.15 on Hard: 0 of 8 wins
  :catch      => false,
  :intro      => ["The sea behind Kyogre rises over the Rimed Sands...",
                  "Kyogre comes ashore at the head of its flood, and turns toward the Siege Camp!"],
  :on_break   => { :cure_status => true, :reset_stats => :negative },
  :breaks     => {
    # The flood-sea itself: the field changes, the storm passes (no rain x flood stacking), Origin Pulse arrives.
    1 => { :messages => ["Kyogre drags the Northern Sea in over the dunes!"],
           :field => :FLOODED_DUNES, :field_message => "", :proc => Prismfall::Bosses::WAR_RAIN_PASSES,
           :learn => { 0 => :ORIGINPULSE, 3 => :CALMMIND } },
    # The last bar: the sea armours it (Hard: and it gathers the tide, Sp. Atk +1). No Primal Reversion in the fight:
    # Primordial Sea over the flood is x1.95 before STAB and one-shot everything neutral (Hard 0 of 8 with it); the
    # Primal form is the cutscene's (WAR-1).
    2 => [{ :messages => ["The flood-sea gathers around Kyogre like armour!"],
            :stats => { :DEFENSE => 1, :SPECIAL_DEFENSE => 1 } },
          { :messages => ["The tide rises behind it!"], :stats => { :SPECIAL_ATTACK => 1 },
            :condition => proc { |_battle, _b, _st| Prismfall::Difficulty.hard? } }]
  },
  :on_defeat  => [
    { :messages => ["{1} sinks into its own flood...", "The sea pulls back over the dunes, and Kyogre goes with it."],
      :end_battle => 1, :result => :turned_back }
  ]
})
