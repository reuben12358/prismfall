#===============================================================================
# RAINBOW - a cloud field beneath a full double rainbow (story/legendary field;
# also what STORMFRONT becomes when the sun breaks through). Prismatic light
# everywhere: every added effect is twice as likely and colourful moves blaze.
# Sandstorm, hail or Defog blot it out, revealing the land beneath (the field
# the battle had before, else a MEADOW). Family: Magical.
#===============================================================================
FieldEffects.register(:RAINBOW, (lambda do
  colours = { :AURORABEAM => 1.5, :SIGNALBEAM => 1.5, :DAZZLINGGLEAM => 1.5, :MISTBALL => 1.5, :LUSTERPURGE => 1.5,
              :SPARKLINGARIA => 1.5, :SILVERWIND => 1.5, :HEARTSTAMP => 1.5, :SACREDFIRE => 1.5, :TRIATTACK => 1.5,
              :MYSTICALFIRE => 1.5, :JUDGMENT => 1.5, :MULTIATTACK => 1.5, :WEATHERBALL => 1.5, :HIDDENPOWER => 1.5,
              :RELICSONG => 1.5, :FIREPLEDGE => 1.5, :WATERPLEDGE => 1.5, :GRASSPLEDGE => 1.5,
              :PRISMATICLASER => 1.3, :PHOTONGEYSER => 1.3, :FLEURCANNON => 1.3 }
  fade_to = proc { |battle| FieldEffects.previous_field(battle, :MEADOW) }
  {
    :name          => "Rainbow",
    :backdrop      => "field_rainbow",
    :family        => :magical,
    :intro_message => "A brilliant rainbow arcs over the battlefield!",
    :description   => "Prismatic light everywhere: added effects are twice as likely, colourful moves blaze, Normal moves surge and darkness falters.",
    :notes         => ["Every move's own added effect is twice as likely (stacks with Serene Grace).",
                       "Normal x1.5. Dark x0.75 (the light washes it out). Marvel Scale is always active.",
                       "Colours x1.5: Aurora Beam, Signal Beam, Dazzling Gleam, Mist Ball, Luster Purge, Sparkling Aria, Silver Wind, Heart Stamp, Sacred Fire, Tri Attack, Mystical Fire, Judgment, Multi-Attack, Weather Ball, Hidden Power, Relic Song and the Pledges. Prismatic Laser, Photon Geyser, Fleur Cannon x1.3.",
                       "Sonic Boom deals 140 HP. Cosmic Power also +1 Sp. Def. Nightmare fails.",
                       "Sleeping Pokemon have sweet dreams (1/16 HP a turn). Cloud Nine Pokemon float on the clouds (a random stat +1 each turn).",
                       "Misty Terrain lasts 3 turns longer; Aurora Veil works without hail.",
                       "Sandstorm, hail or Defog blot out the rainbow -> the field it replaced (or a Meadow).",
                       "Magical Seed: +1 Sp. Atk, and a wish is made for the holder."],
    :nature_power  => :AURORABEAM,
    :camouflage    => :FAIRY,
    :secret_power  => 2,
    :activate_abilities => [:MARVELSCALE],
    :type_mods     => { :NORMAL => 1.5, :DARK => 0.75 },
    :type_messages => { :NORMAL => "The rainbow's light poured into {2}!",
                        :DARK   => "The rainbow's light washed out the darkness..." },
    :move_mods     => colours,
    :move_messages => { :AURORABEAM  => "The aurora blazed in every colour!",
                        :SACREDFIRE  => "Rainbow flames engulfed the foe!",
                        :TRIATTACK   => "All three colours struck as one!",
                        :FIREPLEDGE  => "The pledge shimmered in seven colours!",
                        :WATERPLEDGE => "The pledge shimmered in seven colours!",
                        :GRASSPLEDGE => "The pledge shimmered in seven colours!" },
    :effect_chance_mods => [{ :category => :damaging, :mult => 2.0 }],
    :fixed_damage_mods  => [{ :moves => [:SONICBOOM], :set => 140, :message => "A rainbow boom split the sky!" }],
    :move_fails    => [{ :moves => [:NIGHTMARE], :message => "No nightmare can take hold beneath the rainbow!" }],
    :move_stat_boosts => [
      { :moves => [:COSMICPOWER], :user_stats => { :SPECIAL_DEFENSE => 1 }, :message => "The rainbow's light gathered around {1}!" }
    ],
    :end_of_round  => [
      { :battlers => { :status => [:SLEEP] }, :heal => 1/16r, :message => "{1} is having sweet dreams beneath the rainbow." },
      { :battlers => { :abilities => [:CLOUDNINE] }, :proc => proc { |battle, b|
          stats = [:ATTACK, :DEFENSE, :SPECIAL_ATTACK, :SPECIAL_DEFENSE, :SPEED].select { |s| b.pbCanRaiseStatStage?(s, b) }
          next false if stats.empty?
          battle.pbDisplay(FieldEffects.format("{1} floated up on the rainbow's clouds!", b.pbThis))
          b.pbRaiseStatStage(stats[battle.pbRandom(stats.length)], 1, b)
        } }
    ],
    :terrain       => { :extend => { :Misty => 3 } },
    :weather_as    => [{ :moves => [:AURORAVEIL], :as => :Hail }],
    :transitions   => [
      { :weather => [:Sandstorm, :Hail], :to => fade_to, :message => "The storm blotted out the rainbow, revealing the land beneath..." },
      { :moves => [:DEFOG], :to => fade_to, :message => "The mist cleared, and the rainbow faded over the land below..." }
    ],
    :seed => { :item => :MAGICALSEED, :stats => { :SPECIAL_ATTACK => 1 }, :effects => [:wish],
               :message => "{1}'s {2} shimmered in every colour!" }
  }
end).call)
