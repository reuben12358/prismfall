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
                         "The shard in your pocket hums in time with the waves..."],
           :primal => true, :moves => [:ORIGINPULSE, :ICEBEAM, :THUNDER, :CALMMIND], :clear_hazards => true }
  },
  :on_defeat  => [
    { :condition  => proc { |_battle, _battler, _st| Prismfall::Bosses.harmony_lean? },
      :messages   => ["Your shard flares with a gentle light!", "{1}'s fury ebbs... It calmed down!"],
      :end_battle => 1, :result => :calmed },
    { :messages => ["{1} sank back beneath the waves..."], :result => :defeated }
  ]
})
