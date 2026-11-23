#===============================================================================
# Groudon - the Duneholt Undersands, Chapter 14 "The Deep Seams"
# (story/33_SCRIPT_CH14.md). Woken by Meridian's Drill Nine under Duneholt's
# dry well, in a chamber of Unown glyphs recording Theodric's "Year of Two
# Weathers". Sahar reads the glyphs between bars. Kyogre's twin: the first
# break brings the harsh sun, the second wakes the Primal form. On a Harmony
# lean the player's shard calms it, as with Kyogre.
#   Conditional Branch > Script: Prismfall::Bosses.wild_battle(:GROUDON_UNDERSANDS)
#   Afterwards: S140 CH14_GROUDON_DONE, V109 DUNEHOLT_WELL = 2 (whatever the result).
#===============================================================================
Prismfall::Bosses.register(:GROUDON_UNDERSANDS, {
  :species    => :GROUDON,
  :level      => 66,
  :ability    => :DROUGHT,
  :nature     => :ADAMANT,
  :ivs        => 31,
  :evs        => { :HP => 252, :ATTACK => 252, :DEFENSE => 4 },
  :moves      => [:EARTHQUAKE, :STONEEDGE, :FIREPUNCH, :BULKUP],
  :bars       => { :CASUAL => 2, :default => 3 },
  :stat_mults => { :HARD => { :DEFENSE => 1.15, :SPECIAL_DEFENSE => 1.15 } },
  :field      => :DESERT,
  :catch      => false,
  :intro      => ["The red rock opens one eye... Groudon has awoken beneath the dry well!",
                  "Sahar: \"The Year of Two Weathers.\" It's here. It's all here."],
  :on_break   => { :cure_status => true, :reset_stats => :negative },
  :breaks     => {
    1 => { :messages => ["Sahar reads: \"In the King's ninth year the red one and the blue one were woken out of the deep and the sea.\"",
                         "The glyph chamber grows hot as a forge!"],
           :learn => { 3 => :PRECIPICEBLADES }, :stats => { :ATTACK => 1 } },
    2 => { :messages => ["Sahar reads: \"The King woke the red one and the blue one to remake the land. When they would not obey,\"",
                         "The Earth Plate's hold on the land shatters!",
                         "The scar under your collar burns like a coal..."],
           :primal => true, :moves => [:PRECIPICEBLADES, :HEATCRASH, :STONEEDGE, :BULKUP], :clear_hazards => true }
  },
  :on_defeat  => [
    { :condition  => proc { |_battle, _battler, _st| Prismfall::Bosses.harmony_lean? },
      :messages   => ["Sahar reads: \"...he turned his eyes to heaven.\"",
                      "Your shard flares with a gentle light!", "{1}'s fury ebbs... It calmed down!"],
      :end_battle => 1, :result => :calmed },
    { :messages => ["Sahar reads: \"...he turned his eyes to heaven.\"",
                    "{1} sank back into the earth..."], :result => :defeated }
  ],
  :description => "Ch14 Duneholt Undersands (783): Groudon, woken by the drills; the aquifer refills after"
})
