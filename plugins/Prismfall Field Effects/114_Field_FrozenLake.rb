#===============================================================================
# FROZEN_LAKE - Gym 10 (Ice), Rimeholt in Isenmar, the Frozen Sea. Thick blue
# lake ice under the aurora. Skaters glide; heat and heavy blows crack it, and
# when it gives way the battle drops into the water (WATER_SURFACE).
# "Ice remembers. Every crack. Every weight." - Anja Sorrel
#===============================================================================
FieldEffects.register(:FROZEN_LAKE, {
  :name          => "Frozen Lake",
  :backdrop      => "field_frozen_lake",
  :intro_message => "The battle is taking place on a frozen lake!",
  :description   => "Ice strengthens, skaters glide and priority strikes build speed. Fire, quakes and heavy blows crack the ice; sunlight melts it.",
  :nature_power  => :ICEBEAM,
  :camouflage    => :ICE,
  :secret_power  => 9,
  :type_mods     => { :ICE => 1.5 },
  :type_messages => { :ICE => "The frozen lake chilled the attack!" },
  :move_mods     => { :TRIPLEAXEL => 1.3, :ICESPINNER => 1.3, :SPINOUT => 1.3, :RAPIDSPIN => 1.5,
                      :ROLLOUT => 1.5, :ICEBALL => 1.5 },
  :move_messages => { :TRIPLEAXEL => "{1} spun gracefully across the ice!",
                      :ROLLOUT    => "{1} picked up speed on the slick ice!",
                      :ICEBALL    => "{1} picked up speed on the slick ice!" },
  :move_stat_boosts => [
    # Quick strikes send grounded attackers sliding across the ice
    { :moves => [:QUICKATTACK, :EXTREMESPEED, :AQUAJET, :ACCELEROCK, :FEINT, :MACHPUNCH,
                 :BULLETPUNCH, :JETPUNCH, :FIRSTIMPRESSION, :SHADOWSNEAK],
      :user => { :grounded => true }, :user_stats => { :SPEED => 1 },
      :message => "{1} slid across the ice!" },
    { :moves => [:ICYWIND, :GLACIATE], :target_stats => { :SPEED => -1 },
      :message => "The lake's chill bit even deeper!" }
  ],
  :move_fails    => [
    { :moves => [:DIG], :message => "The ice is far too thick to dig through!" }
  ],
  :speed_mods    => [
    { :battlers => { :abilities => [:SLUSHRUSH],
                     :condition => proc { |battle, b| battle.pbWeather != :Hail } }, :mult => 1.5 }
  ],
  :end_of_round  => [
    { :battlers => { :abilities => [:ICEBODY],
                     :condition => proc { |battle, b| battle.pbWeather != :Hail } },
      :heal => 1/16r, :message => "{1} drew strength from the ice." }
  ],
  :weather       => { :extend => { :Hail => 3 } },
  :terrain       => { :block => [:Grassy], :block_message => "Nothing can take root on solid ice!" },
  :transitions   => [
    # One shared "crack meter": fire melts, quakes and heavy bodies split the ice
    { :condition => proc { |battle, user, target, move, type|
        (type == :FIRE && move.damagingMove?) ||
          [:EARTHQUAKE, :MAGNITUDE, :BULLDOZE, :FISSURE, :STOMPINGTANTRUM, :HIGHHORSEPOWER,
           :HEAVYSLAM, :BODYPRESS, :HEADLONGRUSH].include?(move.id)
      },
      :to => :WATER_SURFACE, :uses => 3,
      :progress_message => "The lake ice groaned and cracked! ({1} more)",
      :message => "The ice gave way! The battle plunged into the freezing lake!" },
    { :weather => [:Sun, :HarshSun], :to => :WATER_SURFACE,
      :message => "The sunlight melted the lake ice into open water!" }
  ],
  :seed => { :item => :ELEMENTALSEED, :stats => { :DEFENSE => 1, :SPEED => 1 },
             :message => "{1}'s {2} encased it in a skin of frost!" }
})
