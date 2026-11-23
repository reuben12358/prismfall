#===============================================================================
# Kyogre - Isenmar, Chapter 11 "The Thaw" (story/06_ACT_III.md).
# Fought on breaking ice under Lake Rime. The first break cracks the lake
# (:FROZEN_LAKE -> :WATER_SURFACE), the second wakes its Primal form. On a
# Harmony lean the player's shard calms it instead of knocking it out:
#   Conditional Branch > Script: Prismfall::Bosses.wild_battle(:KYOGRE_ISENMAR)
#     Conditional Branch > Script: Prismfall::Bosses.last_result[:result] == :calmed
#===============================================================================
Prismfall::Bosses.register(:KYOGRE_ISENMAR, {
  :species    => :KYOGRE,
  :level      => 55,
  :ability    => :DRIZZLE,
  :nature     => :MODEST,
  :ivs        => 31,
  :evs        => { :HP => 252, :SPECIAL_ATTACK => 252, :SPECIAL_DEFENSE => 4 },
  :moves      => [:MUDDYWATER, :ICEBEAM, :CALMMIND, :AQUARING],
  :bars       => { :CASUAL => 2, :default => 3 },
  :stat_mults => { :HARD => { :DEFENSE => 1.15, :SPECIAL_DEFENSE => 1.15 } },
  :field      => :FROZEN_LAKE,
  :catch      => false,
  :intro      => ["The frozen sea heaves... Kyogre has awoken beneath the ice!"],
  :on_break   => { :cure_status => true, :reset_stats => :negative },
  :breaks     => {
    1 => { :messages => ["Kyogre thrashes, and the ice beneath it splinters!"],
           :field => :WATER_SURFACE, :field_message => "The frozen lake cracked apart into open water!",
           :learn => { 0 => :WATERSPOUT }, :stats => { :SPECIAL_ATTACK => 1 } },
    2 => { :messages => ["The Icicle Plate's hold on the sea shatters!",
                         "The scar under your collar burns in time with the waves..."],
           :primal => true, :moves => [:ORIGINPULSE, :ICEBEAM, :THUNDER, :CALMMIND], :clear_hazards => true }
  },
  :on_defeat  => [
    { :condition  => proc { |_battle, _battler, _st| Prismfall::Bosses.harmony_lean? },
      :messages   => ["Your shard flares with a gentle light!", "{1}'s fury ebbs... It calmed down!"],
      :end_battle => 1, :result => :calmed },
    { :messages => ["{1} sank back beneath the waves..."], :result => :defeated }
  ]
})

#===============================================================================
# Kyogre - GO_WEATHER "Weather" (Ch11, story/30_SCRIPT_CH11.md). The player
# chose "Fight it now" when the lake breathed. A Primal Kyogre far past the
# level cap that the party can't beat; the event calls Prismfall.game_over(:GO_WEATHER)
# afterwards whatever the result. The battle ends after its first round (:end_after_rounds).
#===============================================================================
Prismfall::Bosses.register(:KYOGRE_WEATHER, {
  :species    => :KYOGRE,
  :form       => 1,
  :level      => 80,
  :ability    => :PRIMORDIALSEA,
  :nature     => :MODEST,
  :ivs        => 31,
  :evs        => { :HP => 252, :SPECIAL_ATTACK => 252, :SPECIAL_DEFENSE => 4 },
  :moves      => [:ORIGINPULSE, :WATERSPOUT, :ICEBEAM, :THUNDER],
  :bars       => { :default => 5 },
  :end_after_rounds => 1,          # one Primal-rain round, then the event's game over (10_CHOICES_ENDINGS)
  :field      => :WATER_SURFACE,
  :catch      => false,
  :can_run    => false,
  :can_lose   => true,
  :intro      => ["The sea itself rises to meet you..."],
  :description => "Ch11 GO_WEATHER: unwinnable; the game over follows either way"
})
