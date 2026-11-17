#===============================================================================
# VOLCANIC - Gym 7 (Fire), Cindervault in Ashkaar. A caldera floor of flowing
# magma. Fire Pokemon draw fire straight from the magma, winds carry embers,
# rocks come out superheated. Quakes and eruption moves PRIME the volcano: at
# the end of that round it erupts (Rejuvenation's Volcanic Top) - lava rains
# on the unprotected, fire Pokemon ride the blast, hazards are blown away.
# Water, ice, rain or a sandstorm quench it into Cinderglass (ASHEN_WASTE).
# Family: Elemental.
#===============================================================================
FieldEffects.register(:VOLCANIC, (lambda do
  primers = [:ERUPTION, :LAVAPLUME, :MAGMASTORM, :EARTHPOWER, :EARTHQUAKE, :BULLDOZE, :MAGNITUDE, :FISSURE,
             :PRECIPICEBLADES, :HEADLONGRUSH]
  winds   = [:GUST, :TWISTER, :HURRICANE, :AIRCUTTER, :RAZORWIND, :ICYWIND, :SILVERWIND, :OMINOUSWIND,
             :FAIRYWIND, :BLEAKWINDSTORM, :SANDSEARSTORM]
  quench  = [:SURF, :MUDDYWATER, :WATERSPOUT, :HYDROPUMP, :WATERPLEDGE, :SPARKLINGARIA, :ORIGINPULSE,
             :WAVECRASH, :SOAK, :BLIZZARD, :GLACIATE, :SHEERCOLD]
  fireproof = [:FLASHFIRE, :MAGMAARMOR, :FLAMEBODY, :FLAREBOOST, :WATERVEIL, :WATERBUBBLE, :HEATPROOF,
               :WELLBAKEDBODY, :THERMALEXCHANGE]
  erupt = proc { |battle|
    st = FieldEffects.state(battle)
    next if !st[:primed]
    st[:primed] = false
    battle.pbDisplay(FieldEffects.format("The volcano erupted!"))
    battle.pbPriority(true).each do |b|
      next if b.fainted?
      if b.pbHasType?(:FIRE) || b.hasActiveAbility?([:FLASHFIRE, :FLAREBOOST])
        stat = (b.hasActiveAbility?(:FLAREBOOST) || b.spatk >= b.attack) ? :SPECIAL_ATTACK : :ATTACK
        if b.pbCanRaiseStatStage?(stat, b)
          battle.pbDisplay(FieldEffects.format("{1} rode the eruption!", b.pbThis))
          b.pbRaiseStatStage(stat, 1, b)
        end
      elsif b.hasActiveAbility?(:MAGMAARMOR)
        FieldEffects.apply_battler_effect(battle, b, { :stats => { :DEFENSE => 1, :SPECIAL_DEFENSE => 1 },
                                                       :message => "{1}'s armor drank in the lava!" })
      elsif !b.airborne? && !b.hasActiveAbility?(fireproof) && !b.effects[PBEffects::AquaRing]
        FieldEffects.apply_battler_effect(battle, b, { :damage => 1/8r, :damage_type => :FIRE,
                                                       :message => "Lava rained down around {1}!" })
        b.pbFaint if b.fainted?
      end
      if !b.fainted? && b.status == :SLEEP
        b.pbCureStatus(false)
        battle.pbDisplay(FieldEffects.format("{1} was jolted awake by the eruption!", b.pbThis))
      end
    end
    cleared = false
    battle.sides.each do |side|
      [PBEffects::StealthRock, PBEffects::StickyWeb].each { |e| cleared ||= side.effects[e]; side.effects[e] = false }
      [PBEffects::Spikes, PBEffects::ToxicSpikes].each { |e| cleared ||= side.effects[e] > 0; side.effects[e] = 0 }
    end
    battle.pbDisplay(FieldEffects.format("The eruption blasted every hazard off the field!")) if cleared
  }
  {
    :name          => "Volcanic Field",
    :backdrop      => "field_volcanic",
    :family        => :elemental,
    :intro_message => "Magma churns across the battlefield!",
    :description   => "Fire Pokemon draw on the magma; winds carry embers; quakes prime eruptions. Water, ice, rain or sand quench it into black glass.",
    :notes         => ["Fire x1.5, Ice x0.5. Blaze and Flare Boost are always active; Flash Fire starts lit.",
                       "Rock moves come out superheated (also Fire). Wind moves carry embers (also Fire, x1.2).",
                       "Lava Plume, Flame Burst, Fire Spin, Smog, Clear Smog x1.5; Magma Storm, Earth Power, Heat Crash, Torch Song, Scald, Steam Eruption x1.3; Eruption x1.2.",
                       "Smack Down and Thousand Arrows slam the foe onto the glowing crust (x1.5, also Fire). Grass moves wither against grounded targets (x0.5).",
                       "Eruptions: Eruption, Lava Plume, Magma Storm, Earth Power and quakes prime the volcano; at the end of that round it erupts.",
                       "An eruption: Fire types and Flash Fire / Flare Boost users ride it (+1 Atk or Sp. Atk), Magma Armor +1 Def/Sp. Def; lava rains on other grounded Pokemon (1/8, Fire-scaled; Heatproof, Water Veil, Flame Body, Aqua Ring... protect); sleepers wake; all hazards are blown away.",
                       "Will-O-Wisp never misses; damaging Ground moves may burn grounded targets (20%); Smokescreen drops accuracy one stage more.",
                       "Nothing can be frozen. Magma Armor +1 Def on entry and basks in the magma (1/16 HP a turn).",
                       "Hail can't form; Sun +3 turns. Grassy and Misty Terrain burn away.",
                       "Quenching: 2 floods or big ice moves (Surf, Hydro Pump, Water Spout, Muddy Water, Blizzard...), rain or a sandstorm -> Cinderglass.",
                       "Elemental Seed: +1 Attack, +1 Sp. Atk, +1 Speed, but the holder is burned."],
    :nature_power  => :LAVAPLUME,
    :camouflage    => :FIRE,
    :secret_power  => 10,
    :activate_abilities => [:BLAZE, :FLAREBOOST],
    :type_mods     => { :FIRE => 1.5, :ICE => 0.5 },
    :type_messages => { :FIRE => "{1} drew fire up from the magma!",
                        :ICE  => "The ice melted before it could land..." },
    :move_mods     => { :LAVAPLUME => 1.5, :FLAMEBURST => 1.5, :FIRESPIN => 1.5, :SMOG => 1.5, :CLEARSMOG => 1.5,
                        :MAGMASTORM => 1.3, :EARTHPOWER => 1.3, :HEATCRASH => 1.3, :TORCHSONG => 1.3,
                        :SCALD => 1.3, :STEAMERUPTION => 1.3, :ERUPTION => 1.2,
                        :SMACKDOWN => 1.5, :THOUSANDARROWS => 1.5 },
    :move_messages => { :LAVAPLUME   => "The lava surged up with {1}!",
                        :EARTHPOWER  => "Magma erupted from below!",
                        :HEATCRASH   => "{1} crashed down like a lava bomb!",
                        :SCALD       => "The magma brought the water to a boil!",
                        :SMACKDOWN   => "The foe was slammed down onto the glowing crust!",
                        :THOUSANDARROWS => "The foe was slammed down onto the glowing crust!" },
    :damage_mods   => [
      { :moves => winds, :category => :damaging, :mult => 1.2, :message => "The wind whipped up a storm of embers!" },
      { :types => [:GRASS], :category => :damaging, :target => { :grounded => true }, :mult => 0.5,
        :message => "The heat withered {2} before it could land..." }
    ],
    :extra_types   => [
      { :types => [:ROCK], :category => :damaging, :add => :FIRE, :message => "The rocks came out superheated!" },
      { :moves => winds + [:SMACKDOWN, :THOUSANDARROWS, :SMOG, :CLEARSMOG], :category => :damaging, :add => :FIRE }
    ],
    :accuracy_mods => [{ :moves => [:WILLOWISP], :always_hit => true }],
    :added_effects => [
      { :types => [:GROUND], :category => :damaging, :chance => 20, :status => :BURN,
        :target => { :grounded => true }, :message => "Molten rock spattered {1}!" }
    ],
    :move_stat_boosts => [
      { :moves => [:SMOKESCREEN], :target_stats => { :ACCURACY => -1 }, :message => "The volcanic smoke thickened!" }
    ],
    :status_immunity => [{ :status => [:FROZEN], :message => "Nothing can freeze in this heat!" }],
    :on_entry      => [
      { :battlers => { :abilities => [:FLASHFIRE] }, :effects => [:flash_fire], :also_on_change => true },
      { :battlers => { :abilities => [:MAGMAARMOR] }, :stats => { :DEFENSE => 1 },
        :message => "{1}'s armor hardened in the magma!" }
    ],
    :end_of_round  => [
      { :battlers => { :abilities => [:MAGMAARMOR] }, :heal => 1/16r, :message => "{1} basked in the magma." },
      { :battlers => { :status => [:FROZEN] }, :cure_status => true }
    ],
    :weather       => { :block => [:Hail], :block_message => "The heat melted the hail before it fell!",
                        :extend => { :Sun => 3 } },
    :terrain       => { :block => [:Grassy, :Misty],
                        :block_message => "The terrain burned away in the volcanic heat!" },
    :hooks         => {
      :after_move   => proc { |battle, user, targets, move, num_hits|
        next if user.lastMoveFailed || !primers.include?(move.id)
        st = FieldEffects.state(battle)
        next if st[:primed]
        st[:primed] = true
        battle.pbDisplay(FieldEffects.format("The ground heaves... the volcano is about to erupt!"))
      },
      :end_of_round => erupt
    },
    :transitions   => [
      { :moves => quench, :to => :ASHEN_WASTE, :uses => 2, :even_if_failed => true,
        :progress_message => "Steam roars up from the cooling magma... ({1} more)",
        :message => "The magma was quenched! It set into black glass, and steam roars from every crack!" },
      { :weather => [:Rain, :HeavyRain], :to => :ASHEN_WASTE,
        :message => "The rain quenched the magma into black glass! Steam roars from every crack!" },
      { :weather => [:Sandstorm], :to => :ASHEN_WASTE,
        :message => "The sandstorm buried the magma! It cooled into black, glassy dunes!" }
    ],
    :seed => { :item => :ELEMENTALSEED, :status => :BURN,
               :stats => { :ATTACK => 1, :SPECIAL_ATTACK => 1, :SPEED => 1 },
               :message => "{1}'s {2} ignited, filling it with volcanic power!" }
  }
end).call)
