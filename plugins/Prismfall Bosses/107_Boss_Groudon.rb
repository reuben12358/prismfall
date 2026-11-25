#===============================================================================
# Groudon - the Duneholt Undersands, Chapter 14 "The Deep Seams"
# (story/33_SCRIPT_CH14.md). Woken by Meridian's Drill Nine under Duneholt's
# dry well, in a chamber of Unown glyphs recording King Aurelius's "Year of Two
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
  :moves      => { :CASUAL => [:EARTHQUAKE, :STONEEDGE, :FIREPUNCH, :ROCKTOMB], :default => [:EARTHQUAKE, :STONEEDGE, :FIREPUNCH, :BULKUP] },
  :bars       => { :CASUAL => 2, :default => 3 },
  # Casual only (2026-11-24): eased offence and HP and no setup move; Standard and Hard are as designed (hard on purpose).
  :stat_mults => { :CASUAL => { :HP => 0.75, :ATTACK => 0.6, :SPECIAL_ATTACK => 0.6 }, :HARD => { :DEFENSE => 1.15, :SPECIAL_DEFENSE => 1.15 } },
  :field      => :DESERT,
  :catch      => false,
  :intro      => ["The red rock opens one eye... Groudon has awoken beneath the dry well!",
                  "Sahar: \"The Year of Two Weathers.\" It's here. It's all here."],
  :on_break   => { :cure_status => true, :reset_stats => :negative },
  :breaks     => {
    1 => { :messages => ["Sahar reads: \"In the King's ninth year he summoned the red titan and the blue, saying: 'Remake my soil, beasts, or be broken.'\"",
                         "The glyph chamber grows hot as a forge!"],
           :learn => { 3 => :PRECIPICEBLADES }, :stats => { :ATTACK => 1 } },
    2 => { :messages => ["Sahar reads: \"The land split and the sea boiled, and still the King did not step back from his balcony. When the titans would not obey,\"",
                         "The Earth Plate's hold on the land shatters!",
                         "The scar under your collar burns like a coal..."],
           :primal => true, :moves => [:PRECIPICEBLADES, :HEATCRASH, :STONEEDGE, :BULKUP], :clear_hazards => true }
  },
  :on_defeat  => [
    { :condition  => proc { |_battle, _battler, _st| Prismfall::Bosses.harmony_lean? },
      :messages   => ["Sahar reads: \"...he laughed, turned his eyes to heaven, and called for his goldsmiths.\"",
                      "Your shard flares with a gentle light!", "{1}'s fury ebbs... It calmed down!"],
      :end_battle => 1, :result => :calmed },
    { :messages => ["Sahar reads: \"...he laughed, turned his eyes to heaven, and called for his goldsmiths.\"",
                    "{1} sank back into the earth..."], :result => :defeated }
  ],
  :description => "Ch14 Duneholt Undersands (783): Groudon, woken by the drills; the aquifer refills after"
})
