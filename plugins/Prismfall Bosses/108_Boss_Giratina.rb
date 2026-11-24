#===============================================================================
# Giratina - Giratina's Reverse Depths (806), Chapter 15 "The Hollow Cathedral"
# (story/34_SCRIPT_CH15.md). Furious and wounded: the Fault tore the Glass, and
# Kestrel's Gauntlet forced the Spooky Plate to replay AF 290. Altered for the
# first two bars, Origin on the last. Not a hunt: on defeat it doesn't flee. It
# looks at the player and closes the tear (and, on the Ruin Route, R1 has its
# own trial). The Distortion Core is post-game.
#   Conditional Branch > Script: Prismfall::Bosses.wild_battle(:GIRATINA_DEPTHS)
#   Afterwards: S143 CH15_GIRATINA_DONE (whatever the result).
#===============================================================================
Prismfall::Bosses.register(:GIRATINA_DEPTHS, {
  :species    => :GIRATINA,
  :form       => 0,
  :level      => 70,
  :ability    => :PRESSURE,
  :nature     => :CALM,
  :ivs        => 31,
  # Balance 2026-11-23 (cell BGIR): prepared parties won 0% (Calm Mind + the break's +1 Sp. Atk + Ghost x1.2 on the
  # Inverse field). No Sp. Atk EVs, Dragon Tail for Calm Mind, the breaks harden it instead.
  :evs        => { :HP => 252, :DEFENSE => 128, :SPECIAL_DEFENSE => 128 },
  :moves      => [:SHADOWBALL, :DRAGONPULSE, :WILLOWISP, :DRAGONTAIL],
  :bars       => { :CASUAL => 2, :default => 3 },
  :stat_mults => { :CASUAL => { :HP => 0.85, :ATTACK => 0.75, :SPECIAL_ATTACK => 0.75 },
                   :HARD => { :DEFENSE => 1.15, :SPECIAL_DEFENSE => 1.15 } },
  :field      => :INVERSE,
  :catch      => false,
  :intro      => ["The sky below you tears like wet paper...",
                  "Giratina came out of the hole in the world!"],
  :on_break   => { :cure_status => true, :reset_stats => :negative },
  :breaks     => {
    1 => { :messages => ["{1} drags at the torn Glass. The Depths turn over!",
                         "Behind the tear, for a moment: a church, bells, a child in a Choir ribbon..."],
           :learn => { 3 => :HEX }, :stats => { :SPECIAL_DEFENSE => 1 } },
    2 => { :messages => ["The Glass behind {1} gives way completely!",
                         "{1} pulls its true shape through from the other side!"],
           :form => 1, :form_message => "Giratina changed to its Origin Forme!",
           :ability => :LEVITATE,
           :moves => [:POLTERGEIST, :DRAGONCLAW, :SHADOWSNEAK, :EARTHQUAKE],
           :stats => { :DEFENSE => 1 }, :clear_hazards => true }
  },
  :on_defeat  => [
    { :messages => ["{1} stopped fighting.",
                    "It doesn't flee. It looks at you, the way the sea-beast in Isenmar did...",
                    "It knows what you carry. It has been guarding the hole your god left for three hundred years."],
      :end_battle => 1, :result => :yielded }
  ],
  :description => "Ch15 Giratina's Reverse Depths (806): Altered → Origin on the last bar; closes the tear after"
})
