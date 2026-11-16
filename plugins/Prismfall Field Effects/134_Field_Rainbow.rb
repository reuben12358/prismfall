#===============================================================================
# RAINBOW - a cloud field beneath a full double rainbow (story/legendary field).
# Sandstorm, hail or Defog blot it out -> no field.
#===============================================================================
FieldEffects.register(:RAINBOW, {
  :name          => "Rainbow",
  :backdrop      => "field_rainbow",
  :intro_message => "A brilliant rainbow arcs over the battlefield!",
  :description   => "Prismatic light everywhere: secondary effects are twice as likely, dazzling moves shine, Normal moves surge and darkness falters.",
  :notes         => ["Every move's secondary effect is twice as likely to happen.",
                     "Boosted: Normal x1.5. Weakened: Dark x0.75.",
                     "Aurora Beam, Dazzling Gleam, Mist Ball, Luster Purge, Sacred Fire and other light moves x1.5.",
                     "Sleeping Pokémon recover 1/16 HP each turn. Misty Terrain lasts 3 turns longer.",
                     "Sandstorm, hail or Defog blot out the rainbow."],
  :nature_power  => :AURORABEAM,
  :camouflage    => :FAIRY,
  :secret_power  => 2,
  :type_mods     => { :NORMAL => 1.5, :DARK => 0.75 },
  :type_messages => { :NORMAL => "The rainbow's light poured into the attack!",
                      :DARK   => "The rainbow's light washed out the darkness..." },
  :move_mods     => { :AURORABEAM => 1.5, :SIGNALBEAM => 1.5, :DAZZLINGGLEAM => 1.5, :MISTBALL => 1.5,
                      :LUSTERPURGE => 1.5, :SPARKLINGARIA => 1.5, :SILVERWIND => 1.5, :HEARTSTAMP => 1.5,
                      :SACREDFIRE => 1.5, :FIREPLEDGE => 1.5, :WATERPLEDGE => 1.5, :GRASSPLEDGE => 1.5,
                      :PRISMATICLASER => 1.3, :PHOTONGEYSER => 1.3, :FLEURCANNON => 1.3 },
  :move_messages => { :AURORABEAM  => "The aurora blazed in every color!",
                      :SACREDFIRE  => "Rainbow flames engulfed the foe!",
                      :FIREPLEDGE  => "The pledge shimmered in seven colors!",
                      :WATERPLEDGE => "The pledge shimmered in seven colors!",
                      :GRASSPLEDGE => "The pledge shimmered in seven colors!" },
  :effect_chance_mods => [{ :category => :damaging, :mult => 2.0 }],
  :move_stat_boosts => [
    { :moves => [:COSMICPOWER], :user_stats => { :SPECIAL_DEFENSE => 1 },
      :message => "The rainbow's light gathered around {1}!" }
  ],
  :end_of_round  => [
    { :battlers => { :status => [:SLEEP] }, :heal => 1/16r,
      :message => "{1} is having sweet dreams beneath the rainbow." }
  ],
  :terrain       => { :extend => { :Misty => 3 } },
  :transitions   => [
    { :weather => [:Sandstorm, :Hail], :to => :NONE, :message => "The storm blotted out the rainbow..." },
    { :moves => [:DEFOG], :to => :NONE, :message => "The mist cleared, and the rainbow faded away..." }
  ],
  :seed => { :item => :MAGICALSEED, :stats => { :SPECIAL_ATTACK => 1, :SPECIAL_DEFENSE => 1 },
             :message => "{1}'s {2} shimmered in every color!" }
})
