#===============================================================================
# Reshiram at Wyrmrest's Rift-shrine (Wyrmscar Rift 865, Chapter 19 "The Last Gate";
# story/38_SCRIPT_CH19.md). The `:war_legend == :neither` path: no legend came
# to the Glass Dunes, so the Light Stone stays dark at the front and wakes here,
# after the truce, when it comes home, answering the PC's oath (:ch19_oath).
# Same body as the Glass Dunes Reshiram (106), on the den's own field instead of
# the flood and the glass. Uncatchable (no main-story legendaries): it bows to
# Sigrun and flies ahead to Crownhaven.
#   Script: Prismfall::Bosses.wild_battle(:RESHIRAM_WYRMREST)
#   Afterwards: S154 CH19_RESHIRAM_DONE (whatever the result).
#===============================================================================
Prismfall::Bosses.register(:RESHIRAM_WYRMREST, {
  :species    => :RESHIRAM,
  :level      => 84,
  :ability    => :TURBOBLAZE,
  :nature     => :CALM,
  :ivs        => 31,
  :evs        => { :HP => 252, :SPECIAL_DEFENSE => 252, :SPEED => 4 },
  :moves      => [:FLAMETHROWER, :DRAGONPULSE, :EARTHPOWER, :EXTRASENSORY],
  :bars       => { :CASUAL => 2, :default => 3 },
  :stat_mults => { :CASUAL => { :HP => 1.15 }, :STANDARD => { :HP => 1.35, :DEFENSE => 1.1, :SPECIAL_DEFENSE => 1.1 },
                   :HARD => { :HP => 1.5, :SPECIAL_ATTACK => 1.15, :DEFENSE => 1.2, :SPECIAL_DEFENSE => 1.2 } },
  :field      => :DRAGONS_DEN,
  :catch      => false,
  :intro      => ["The Light Stone cracks white over the Draco Plate's brazier...",
                  "Reshiram unfolds out of the Rift's fire, and weighs you!"],
  :on_break   => { :cure_status => true, :reset_stats => :negative },
  :breaks     => {
    1 => { :messages => ["The den's heat rises! Reshiram's fire burns white-hot!"],
           :learn => { 0 => :BLUEFLARE } },
    2 => { :messages => ["Reshiram roars, and the Rift's walls ring with the truth you spoke!"],
           :learn => { 3 => :FUSIONFLARE }, :stats => { :SPECIAL_DEFENSE => 1 } }
  },
  :on_defeat  => [
    { :condition  => proc { |_battle, _battler, _st| Prismfall::Bosses.harmony_lean? },
      :messages   => ["{1}'s white fire gentles...", "It lowers its head, but not to you."],
      :end_battle => 1, :result => :weighed },
    { :messages => ["{1}'s white fire gutters out...", "It turns from you and lowers its head, but not to you."],
      :end_battle => 1, :result => :weighed }
  ],
  :description => "Ch19 Wyrmscar Rift (865), :war_legend == :neither only: Reshiram weighs the oath; bows to Sigrun"
})
