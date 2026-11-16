#===============================================================================
# CRYSTAL_CAVERN - Gym 13 (Rock), Cragholm in Ossaria, the Bone Sands. A geode
# of prismatic crystals lit from within. Their glow cycles red -> blue ->
# green -> amethyst each round: Rock moves take on the glow's type, and moves
# of that type shine brighter. Darkness (or a sandstorm) kills the light
# (DARK_CRYSTAL); quakes and explosions shatter the crystals (CAVE).
#===============================================================================
FieldEffects.register(:CRYSTAL_CAVERN, {
  :name          => "Crystal Cavern",
  :backdrop      => "field_crystal_cavern",
  :intro_message => "Prismatic crystals glitter all around!",
  :description   => "The crystals' glow cycles Fire > Water > Grass > Psychic each round: Rock moves gain that type, and that type is boosted. Light moves dazzle. Darkness or sand blots out the light.",
  :nature_power  => :POWERGEM,
  :camouflage    => :ROCK,
  :secret_power  => 8,
  :type_mods     => { :ROCK => 1.3 },
  :type_messages => { :ROCK => "The crystals resonated with the attack!" },
  :move_mods     => { :AURORABEAM => 1.5, :SIGNALBEAM => 1.5, :FLASHCANNON => 1.5, :LUSTERPURGE => 1.5,
                      :MISTBALL => 1.5, :DAZZLINGGLEAM => 1.5, :MIRRORSHOT => 1.5, :DOOMDESIRE => 1.5,
                      :MOONGEISTBEAM => 1.5, :PHOTONGEYSER => 1.5, :PRISMATICLASER => 1.5,
                      :POWERGEM => 1.5, :DIAMONDSTORM => 1.5, :METEORBEAM => 1.5, :LUMINACRASH => 1.5,
                      :CHARGEBEAM => 1.5, :TECHNOBLAST => 1.5 },
  :move_messages => { :FLASHCANNON    => "The crystals refracted the light into a dazzling beam!",
                      :DAZZLINGGLEAM  => "The crystals refracted the light into a dazzling beam!",
                      :POWERGEM       => "The crystals refracted the light into a dazzling beam!",
                      :AURORABEAM     => "The crystals refracted the light into a dazzling beam!",
                      :PRISMATICLASER => "The crystals refracted the light into a dazzling beam!" },
  # Rock moves take on the current glow (state[:cc_hue]: 0 Fire, 1 Water, 2 Grass, 3 Psychic)
  :extra_types   => [
    { :types => [:ROCK], :category => :damaging, :add => :FIRE,
      :condition => proc { |battle, user, target, move, type| (FieldEffects.state(battle)[:cc_hue] || 0) == 0 },
      :message => "The red crystals set the rock ablaze!" },
    { :types => [:ROCK], :category => :damaging, :add => :WATER,
      :condition => proc { |battle, user, target, move, type| FieldEffects.state(battle)[:cc_hue] == 1 },
      :message => "The blue crystals flooded the rock with water!" },
    { :types => [:ROCK], :category => :damaging, :add => :GRASS,
      :condition => proc { |battle, user, target, move, type| FieldEffects.state(battle)[:cc_hue] == 2 },
      :message => "The green crystals wreathed the rock in vines!" },
    { :types => [:ROCK], :category => :damaging, :add => :PSYCHIC,
      :condition => proc { |battle, user, target, move, type| FieldEffects.state(battle)[:cc_hue] == 3 },
      :message => "The amethyst crystals charged the rock with psychic power!" }
  ],
  :damage_mods   => [
    # The glow's own type shines brighter (counterplay: Water/Grass rounds vs. Rock)
    { :category => :damaging, :mult => 1.2,
      :condition => proc { |battle, user, target, move, type|
        type == [:FIRE, :WATER, :GRASS, :PSYCHIC][FieldEffects.state(battle)[:cc_hue] || 0]
      } },
    { :flags => ["Sound"], :category => :damaging, :mult => 1.2,
      :message => "The crystals rang with {2}!" }
  ],
  :effect_chance_mods => [{ :moves => [:ANCIENTPOWER], :mult => 2.0 }],
  :move_stat_boosts => [
    { :moves => [:FLASH], :target_stats => { :ACCURACY => -1 },
      :message => "The crystals magnified the flash!" }
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
    },
    # The crystals reflect barriers: Reflect / Light Screen / Aurora Veil last 2 extra turns
    :after_move => proc { |battle, user, targets, move, num_hits|
      next if user.lastMoveFailed
      eff = { :REFLECT => PBEffects::Reflect, :LIGHTSCREEN => PBEffects::LightScreen,
              :AURORAVEIL => PBEffects::AuroraVeil }[move.id]
      next if !eff || user.pbOwnSide.effects[eff] <= 0
      user.pbOwnSide.effects[eff] += 2
      battle.pbDisplay(FieldEffects.format("The crystals reflected the barrier, strengthening it!"))
    }
  },
  :transitions   => [
    { :moves => [:DARKPULSE, :NIGHTDAZE, :DARKVOID, :FIERYWRATH], :to => :DARK_CRYSTAL,
      :message => "Darkness swallowed the crystals' light!" },
    { :weather => [:Sandstorm], :to => :DARK_CRYSTAL,
      :message => "The sandstorm choked out the crystals' light!" },
    { :moves => [:EXPLOSION, :SELFDESTRUCT, :MISTYEXPLOSION],
      :to => proc { |battle| FieldEffects.exists?(:CAVE) ? :CAVE : :NONE },
      :message => "The blast shattered the crystals!" },
    { :moves => [:EARTHQUAKE, :MAGNITUDE, :BULLDOZE, :FISSURE], :uses => 3,
      :to => proc { |battle| FieldEffects.exists?(:CAVE) ? :CAVE : :NONE },
      :progress_message => "The crystals are cracking! ({1} more)",
      :message => "The quakes shattered the crystals!" }
  ],
  :seed => { :item => :TELLURICSEED, :stats => { :DEFENSE => 1, :SPECIAL_DEFENSE => 1 },
             :message => "{1}'s {2} grew a crystal shell around it!" }
})
