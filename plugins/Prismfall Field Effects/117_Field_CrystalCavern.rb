#===============================================================================
# CRYSTAL_CAVERN - Gym 13 (Rock), Cragholm in Ossaria, the Bone Sands. A geode
# of prismatic crystals lit from within. Their glow cycles red -> blue ->
# green -> amethyst each round: Rock moves take on the glow's type, moves of
# that type shine brighter, and even Stealth Rock flares with it. Light moves
# refract into dazzling beams; barriers are mirrored and last longer.
# Darkness (or a sandstorm) kills the light (DARK_CRYSTAL); quakes and
# explosions shatter the crystals (CAVE). Family: Magical.
#===============================================================================
FieldEffects.register(:CRYSTAL_CAVERN, (lambda do
  hues   = [:FIRE, :WATER, :GRASS, :PSYCHIC]
  hue    = lambda { |battle| hues[FieldEffects.state(battle)[:cc_hue] || 0] }
  lights = [:AURORABEAM, :SIGNALBEAM, :FLASHCANNON, :LUSTERPURGE, :MISTBALL, :DAZZLINGGLEAM, :MIRRORSHOT,
            :DOOMDESIRE, :MOONGEISTBEAM, :PHOTONGEYSER, :PRISMATICLASER, :POWERGEM, :DIAMONDSTORM, :METEORBEAM,
            :LUMINACRASH, :CHARGEBEAM, :TECHNOBLAST, :ANCIENTPOWER]
  hue_rule = lambda do |idx, type, msg|
    { :types => [:ROCK], :category => :damaging, :add => type, :message => msg,
      :condition => proc { |battle, user, target, move, t| (FieldEffects.state(battle)[:cc_hue] || 0) == idx } }
  end
  {
    :name          => "Crystal Cavern",
    :backdrop      => "field_crystal_cavern",
    :family        => :magical,
    :intro_message => "Prismatic crystals glitter all around!",
    :description   => "The crystals' glow cycles Fire > Water > Grass > Psychic each round: Rock moves (and Stealth Rock) take that type, and that type shines. Light refracts, barriers mirror. Darkness or sand blots out the light.",
    :notes         => ["Rock x1.3, Dragon x1.2 (old wyrms hoarded these crystals). Damaging sound moves x1.2 (the crystals ring).",
                       "The glow cycles each round: red (Fire) > blue (Water) > green (Grass) > amethyst (Psychic), starting at random. Rock moves also hit as the glow's type; moves OF the glow's type are x1.2.",
                       "Stealth Rock flares with the glow: an extra 1/16 hit of that type on entry.",
                       "Light moves refract into dazzling beams (x1.5): Power Gem, Diamond Storm, Flash Cannon, Dazzling Gleam, Aurora Beam, Luster Purge, Mist Ball, Moongeist Beam, Prismatic Laser, Meteor Beam, Lumina Crash, Ancient Power...",
                       "Ancient Power's stat boost is twice as likely. Flash drops accuracy one stage more; Rock Polish also +1 Sp. Atk.",
                       "Reflect, Light Screen and Aurora Veil last 2 turns longer; Aurora Veil works without hail. Prism Armor Pokemon take x0.75 from every hit.",
                       "Dark Pulse, Night Daze, Dark Void, Fiery Wrath or a sandstorm -> Dark Crystal Cavern. An explosion, or 3 quakes -> Cave (the crystals shatter).",
                       "Magical Seed: +1 Sp. Atk and a Light Screen for its side."],
    :nature_power  => :POWERGEM,
    :camouflage    => :ROCK,
    :secret_power  => 8,
    :type_mods     => { :ROCK => 1.3, :DRAGON => 1.2 },
    :type_messages => { :ROCK => "The crystals resonated with {2}!" },
    :move_mods     => lights.map { |m| [m, 1.5] }.to_h,
    :move_messages => { :FLASHCANNON    => "The crystals refracted the light into a dazzling beam!",
                        :DAZZLINGGLEAM  => "The crystals refracted the light into a dazzling beam!",
                        :POWERGEM       => "The crystals refracted the light into a dazzling beam!",
                        :AURORABEAM     => "The crystals refracted the light into a dazzling beam!",
                        :PRISMATICLASER => "The crystals split the beam into every colour at once!" },
    :extra_types   => [
      hue_rule.call(0, :FIRE, "The red crystals set the rock ablaze!"),
      hue_rule.call(1, :WATER, "The blue crystals flooded the rock with water!"),
      hue_rule.call(2, :GRASS, "The green crystals wreathed the rock in vines!"),
      hue_rule.call(3, :PSYCHIC, "The amethyst crystals charged the rock with psychic power!")
    ],
    :damage_mods   => [
      # The glow's own type shines brighter (counterplay: Water/Grass rounds vs. Rock)
      { :category => :damaging, :mult => 1.2,
        :condition => proc { |battle, user, target, move, type| type == hue.call(battle) } },
      { :flags => ["Sound"], :category => :damaging, :mult => 1.2, :message => "The crystals rang with {2}!" },
      { :category => :damaging, :target => { :abilities => [:PRISMARMOR] }, :final_mult => 0.75 }
    ],
    :effect_chance_mods => [{ :moves => [:ANCIENTPOWER], :mult => 2.0 }],
    :move_stat_boosts => [
      { :moves => [:FLASH], :target_stats => { :ACCURACY => -1 }, :message => "The crystals magnified the flash!" },
      { :moves => [:ROCKPOLISH], :user_stats => { :SPECIAL_ATTACK => 1 }, :message => "{1} gleamed like a cut gem!" }
    ],
    :effect_durations => { :REFLECT => [2, "The crystals mirrored the barrier, strengthening it!"],
                           :LIGHTSCREEN => [2, "The crystals mirrored the barrier, strengthening it!"],
                           :AURORAVEIL => [2, "The crystals mirrored the barrier, strengthening it!"] },
    :weather_as    => [{ :moves => [:AURORAVEIL], :as => :Hail }],
    :on_entry      => [
      { :battlers => { :not_items => [:HEAVYDUTYBOOTS],
                       :condition => proc { |battle, b| b.pbOwnSide.effects[PBEffects::StealthRock] } },
        :proc => proc { |battle, b|
          t = hue.call(battle)
          FieldEffects.apply_battler_effect(battle, b, { :damage => 1/16r, :damage_type => t,
                                                         :message => "The crystal shards flared {2} as they struck {1}!" },
                                            GameData::Type.get(t).name)
        } }
    ],
    :hooks         => {
      :on_start => proc { |battle, old_id|
        st = FieldEffects.state(battle)
        st[:cc_hue] = battle.pbRandom(4)
        battle.pbDisplay(FieldEffects.format(["The crystals glow a fiery red.", "The crystals glow a deep ocean blue.",
                                              "The crystals glow a vivid green.", "The crystals glow amethyst."][st[:cc_hue]]))
      },
      :end_of_round => proc { |battle|
        st = FieldEffects.state(battle)
        st[:cc_hue] = ((st[:cc_hue] || 0) + 1) % 4
        battle.pbDisplay(FieldEffects.format(["The crystals flared a fiery red!", "The crystals shifted to ocean blue!",
                                              "The crystals shifted to vivid green!", "The crystals shifted to amethyst!"][st[:cc_hue]]))
      }
    },
    :transitions   => [
      { :moves => [:DARKPULSE, :NIGHTDAZE, :DARKVOID, :FIERYWRATH], :even_if_failed => true, :to => :DARK_CRYSTAL,
        :message => "Darkness swallowed the crystals' light!" },
      { :weather => [:Sandstorm], :to => :DARK_CRYSTAL, :message => "The sandstorm smothered the crystals' light!" },
      { :moves => [:EXPLOSION, :SELFDESTRUCT, :MISTYEXPLOSION], :to => :CAVE, :message => "The blast shattered the crystals!" },
      { :moves => [:EARTHQUAKE, :MAGNITUDE, :BULLDOZE, :FISSURE], :uses => 3, :to => :CAVE,
        :progress_message => "The crystals are cracking! ({1} more)",
        :message => "The quakes shattered the crystals!" }
    ],
    :seed => { :item => :MAGICALSEED, :stats => { :SPECIAL_ATTACK => 1 }, :effects => [:light_screen],
               :message => "{1}'s {2} refracted the crystals' light around it!" }
  }
end).call)
