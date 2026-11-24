#===============================================================================
# Pecharunt - the Lightless Deep (844), Chapter 18 "Once Upon a Time"
# (story/37_SCRIPT_CH18.md). The source of Sweetrot: a peach-shell mythical in
# a cavern of pink crystal, tended by smiling thralls, Mother Gutter the first of
# them. Its poison chains mirror the Gilded Chain. Uncatchable (Reuben's rule:
# no main-story legendaries; the capture is the postgame PG_PECHARUNT chain).
#   Conditional Branch > Script: Prismfall::Bosses.wild_battle(:PECHARUNT_DEEP)
#   Afterwards: S150 CH18_PECHARUNT_DONE (whatever the result).
#===============================================================================
Prismfall::Bosses.register(:PECHARUNT_DEEP, {
  :species    => :PECHARUNT,
  :level      => 77,
  :ability    => :POISONPUPPETEER,
  :nature     => :MODEST,
  :ivs        => 31,
  :evs        => { :HP => 252, :SPECIAL_ATTACK => 252, :DEFENSE => 4 },
  :moves      => [:MALIGNANTCHAIN, :SHADOWBALL, :NASTYPLOT, :RECOVER],
  :bars       => { :CASUAL => 2, :default => 3 },
  :stat_mults => { :HARD => { :DEFENSE => 1.15, :SPECIAL_DEFENSE => 1.15 } },
  :field      => :DARK_CRYSTAL,
  :catch      => false,
  :intro      => ["The sweet smell thickens. Something in a peach-coloured shell is smiling at you...",
                  "Pecharunt's chains rattle! The thralls stop tending and turn to watch!"],
  :on_break   => { :cure_status => true, :reset_stats => :negative },
  :breaks     => {
    1 => { :messages => ["{1} pulls on its chains! The pink crystals gutter out one by one...",
                         "Somewhere in the dark, a thrall drops her watering-can."],
           :field => :NEW_MOON, :field_message => "The Lightless Deep goes truly dark!",
           :learn => { 2 => :HEX } },
    2 => { :messages => ["{1}'s shell cracks! The sweet smell turns sour!",
                         "\"Mochi, mochi...\" The chant falters in the dark."],
           :moves => [:MALIGNANTCHAIN, :HEX, :SLUDGEBOMB, :RECOVER], :stats => { :SPECIAL_ATTACK => 1 } }
  },
  :on_defeat  => [
    { :messages => ["{1}'s chains came apart!",
                    "All through the Deep, the thralls blink, and stop smiling, and start to cry."],
      :end_battle => 1, :result => :freed }
  ],
  :description => "Ch18 Lightless Deep (844): Pecharunt, the source of Sweetrot; frees the thralls (S150)"
})
