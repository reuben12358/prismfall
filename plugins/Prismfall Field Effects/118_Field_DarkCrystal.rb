#===============================================================================
# DARK_CRYSTAL - CRYSTAL_CAVERN with its light dead: the same geode, crystals
# gone obsidian-violet. Shadows hunt by feel; light pierces it and can rekindle
# the crystals. Also used for Darkglass Mine / Lightless Deep.
#===============================================================================
FieldEffects.register(:DARK_CRYSTAL, {
  :name          => "Dark Crystal Cavern",
  :backdrop      => "field_dark_crystal",
  :intro_message => "Darkness fills the cavern. The crystals have gone black...",
  :description   => "Dark and Ghost moves strengthen; Rock hardens into obsidian. Most Pokémon struggle to aim. Light moves pierce the dark and can rekindle the crystals.",
  :nature_power  => :DARKPULSE,
  :camouflage    => :DARK,
  :secret_power  => 8,
  :type_mods     => { :DARK => 1.5, :GHOST => 1.3, :ROCK => 1.2 },
  :type_messages => { :DARK  => "The darkness gave the attack teeth!",
                      :GHOST => "The shadows lent the attack their strength!" },
  :move_mods     => { :AURORABEAM => 1.2, :SIGNALBEAM => 1.2, :FLASHCANNON => 1.2, :LUSTERPURGE => 1.2,
                      :MISTBALL => 1.2, :DAZZLINGGLEAM => 1.2, :MIRRORSHOT => 1.2, :DOOMDESIRE => 1.2,
                      :MOONGEISTBEAM => 1.2, :PHOTONGEYSER => 1.2, :PRISMATICLASER => 1.2,
                      :POWERGEM => 1.2, :DIAMONDSTORM => 1.2, :METEORBEAM => 1.2, :LUMINACRASH => 1.2,
                      :CHARGEBEAM => 1.2, :TECHNOBLAST => 1.2, :STONEEDGE => 1.2, :STONEAXE => 1.2 },
  :move_messages => { :FLASHCANNON   => "The light pierced the darkness!",
                      :DAZZLINGGLEAM => "The light pierced the darkness!",
                      :POWERGEM      => "The light pierced the darkness!",
                      :STONEEDGE     => "Obsidian shards sliced through the dark!" },
  :accuracy_mods => [
    # Only creatures of the dark (and Rock, who feel the stone) aim true
    { :category => :damaging, :mult => 0.9,
      :user => { :not_types => [:DARK, :GHOST, :ROCK],
                 :not_abilities => [:KEENEYE, :ILLUMINATE, :MINDSEYE, :NOGUARD] } }
  ],
  :crit_mods     => [
    { :types => [:DARK, :GHOST], :flags => ["Contact"], :add => 1 }
  ],
  :move_stat_boosts => [
    { :moves => [:FLASH], :target_stats => { :ACCURACY => -1 },
      :message => "The sudden flash was blinding in the dark!" }
  ],
  :on_entry      => [
    { :battlers => { :abilities => [:ILLUMINATE] }, :stats => { :ACCURACY => 1 },
      :message => "{1} lit up the darkness around it!" }
  ],
  :transitions   => [
    { :moves => [:FLASH, :DAZZLINGGLEAM, :FLASHCANNON, :POWERGEM, :DIAMONDSTORM, :LUSTERPURGE,
                 :PRISMATICLASER, :PHOTONGEYSER, :LUMINACRASH, :AURORABEAM, :MIRRORSHOT, :TAILGLOW,
                 :LIGHTOFRUIN, :METEORBEAM],
      :uses => 2, :to => :CRYSTAL_CAVERN,
      :progress_message => "A faint glow stirs within the crystals... ({1} more)",
      :message => "Light flooded the crystals! The cavern glitters once more!" },
    { :weather => [:Sun, :HarshSun], :to => :CRYSTAL_CAVERN,
      :message => "Sunlight rekindled the crystals!" },
    { :moves => [:EXPLOSION, :SELFDESTRUCT, :MISTYEXPLOSION],
      :to => proc { |battle| FieldEffects.exists?(:CAVE) ? :CAVE : :NONE },
      :message => "The blast shattered the dead crystals!" },
    { :moves => [:EARTHQUAKE, :MAGNITUDE, :BULLDOZE, :FISSURE], :uses => 3,
      :to => proc { |battle| FieldEffects.exists?(:CAVE) ? :CAVE : :NONE },
      :progress_message => "The dead crystals are cracking! ({1} more)",
      :message => "The quakes shattered the dead crystals!" }
  ],
  :seed => { :item => :MAGICALSEED, :stats => { :ATTACK => 1, :SPECIAL_ATTACK => 1 },
             :message => "{1}'s {2} drank in the darkness!" }
})
