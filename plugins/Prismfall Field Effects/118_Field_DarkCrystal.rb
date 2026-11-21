#===============================================================================
# DARK_CRYSTAL - CRYSTAL_CAVERN with its light dead: the same geode, crystals
# gone obsidian-violet. Creatures of the dark hunt by feel and hide in it;
# light pierces it and two bright moves rekindle the crystals. Underground: no sun,
# rain or hail (SPINE Rev 24 audit: sunlight used to rekindle it from a cave).
# Also used for Darkglass Mine / Lightless Deep. Family: Magical.
#===============================================================================
FieldEffects.register(:DARK_CRYSTAL, (lambda do
  lights = [:AURORABEAM, :SIGNALBEAM, :FLASHCANNON, :LUSTERPURGE, :MISTBALL, :DAZZLINGGLEAM, :MIRRORSHOT,
            :DOOMDESIRE, :MOONGEISTBEAM, :PHOTONGEYSER, :PRISMATICLASER, :POWERGEM, :DIAMONDSTORM, :METEORBEAM,
            :LUMINACRASH, :CHARGEBEAM, :TECHNOBLAST]
  {
    :name          => "Dark Crystal Cavern",
    :backdrop      => "field_dark_crystal",
    :family        => :magical,
    :intro_message => "Darkness fills the cavern. The crystals have gone black...",
    :description   => "Creatures of the dark hunt by feel and hide in it; obsidian edges cut. Most Pokemon struggle to aim. Light pierces the dark and can rekindle the crystals.",
    :notes         => ["Dark x1.5, Ghost x1.3, Rock x1.2 (obsidian). Dark and Ghost Pokemon melt into the dark: x0.83 damage taken.",
                       "Shadow Sneak, Sucker Punch, Shadow Claw, Night Slash x1.5 (struck from the dark); Stone Edge, Stone Axe x1.2.",
                       "Light moves (Power Gem, Flash Cannon, Dazzling Gleam, Luster Purge, Meteor Beam...) x1.2 - they pierce the dark.",
                       "Damaging moves from Pokemon that aren't Dark, Ghost or Rock are x0.9 accurate (Keen Eye, Illuminate, Mind's Eye, No Guard see fine). Illuminate +1 accuracy on entry.",
                       "Dark and Ghost contact moves: +1 critical-hit stage. Flash drops accuracy one stage more. Solar Beam and Solar Blade fail (no light to gather).",
                       "Prism Armor Pokemon take x0.75 from every hit.",
                       "Underground: Sun, Rain and Hail can't start.",
                       "2 light moves (Flash, Tail Glow and Light of Ruin count too) -> Crystal Cavern. An explosion or 3 quakes -> Cave.",
                       "Magical Seed: +1 Attack, +1 Sp. Atk."],
    :nature_power  => :DARKPULSE,
    :camouflage    => :DARK,
    :secret_power  => 8,
    :type_mods     => { :DARK => 1.5, :GHOST => 1.3, :ROCK => 1.2 },
    :type_messages => { :DARK  => "The darkness gave {1}'s attack teeth!",
                        :GHOST => "The ghosts thickened in the dark around {1}!" },
    :move_mods     => lights.map { |m| [m, 1.2] }.to_h.merge(:SHADOWSNEAK => 1.5, :SUCKERPUNCH => 1.5, :SHADOWCLAW => 1.5,
                                                             :NIGHTSLASH => 1.5, :STONEEDGE => 1.2, :STONEAXE => 1.2),
    :move_messages => { :FLASHCANNON   => "The light pierced the darkness!",
                        :DAZZLINGGLEAM => "The light pierced the darkness!",
                        :POWERGEM      => "The light pierced the darkness!",
                        :SHADOWSNEAK   => "{1} struck from the dark!",
                        :SUCKERPUNCH   => "{1} struck from the dark!",
                        :STONEEDGE     => "Obsidian shards sliced through the dark!" },
    :damage_mods   => [
      { :category => :damaging, :target => { :types => [:DARK, :GHOST] }, :defense_mult => 1.2 },
      { :category => :damaging, :target => { :abilities => [:PRISMARMOR] }, :final_mult => 0.75 }
    ],
    :accuracy_mods => [
      { :category => :damaging, :mult => 0.9,
        :user => { :not_types => [:DARK, :GHOST, :ROCK],
                   :not_abilities => [:KEENEYE, :ILLUMINATE, :MINDSEYE, :NOGUARD] } }
    ],
    :crit_mods     => [{ :types => [:DARK, :GHOST], :flags => ["Contact"], :add => 1 }],
    :move_stat_boosts => [
      { :moves => [:FLASH], :target_stats => { :ACCURACY => -1 }, :message => "The sudden flash was blinding in the dark!" }
    ],
    :move_fails    => [{ :moves => [:SOLARBEAM, :SOLARBLADE], :message => "There's no light here for {1} to gather!" }],
    :weather       => { :block => [:Sun, :Rain, :Hail],
                        :block_message => "There's no sky down here - the weather can't reach the cavern!" },
    :on_entry      => [
      { :battlers => { :abilities => [:ILLUMINATE] }, :stats => { :ACCURACY => 1 },
        :message => "{1} lit up the darkness around it!" }
    ],
    :transitions   => [
      { :moves => lights + [:FLASH, :TAILGLOW, :LIGHTOFRUIN], :even_if_failed => true, :uses => 2, :to => :CRYSTAL_CAVERN,
        :progress_message => "A faint glow stirs within the crystals... ({1} more)",
        :message => "Light flooded the crystals! The cavern glitters once more!" },
      { :moves => [:EXPLOSION, :SELFDESTRUCT, :MISTYEXPLOSION], :to => :CAVE,
        :message => "The blast shattered the dead crystals!" },
      { :moves => [:EARTHQUAKE, :MAGNITUDE, :BULLDOZE, :FISSURE], :uses => 3, :to => :CAVE,
        :progress_message => "The dead crystals are cracking! ({1} more)",
        :message => "The quakes shattered the dead crystals!" }
    ],
    :seed => { :item => :MAGICALSEED, :stats => { :ATTACK => 1, :SPECIAL_ATTACK => 1 },
               :message => "{1}'s {2} drank in the darkness!" }
  }
end).call)
