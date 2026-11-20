#===============================================================================
# ASHEN_WASTE - "Cinderglass". The ID is kept (SPINE roster); the place is new.
# A quenched volcano: magma set into black obsidian, steam vents and geysers
# breaking through the glass, dunes of glass-grit, heat glowing underneath.
# What VOLCANIC becomes when quenched, and the field of the Cinderglass Barrens
# (Ashkaar-Ossaria borderland) and the Ashkaar Siege Camp. (A desert glassed by
# searing heat is the GLASS_DUNES instead: sand glass, not volcanic glass.)
#   * Geysers blow on a 3-round cycle (a quake sets them off at once): swimmers
#     and fire Pokemon ride the steam, others get blasted.
#   * Water on hot glass flashes into blinding steam; Scald-type moves boil.
#   * Obsidian edges sharpen Rock moves and Stealth Rock; winds whip up
#     glass-grit storms.
# Big fire re-melts it (VOLCANIC); a flood fills the caldera (WATER_SURFACE).
# Family: Elemental.
#===============================================================================
FieldEffects.register(:ASHEN_WASTE, (lambda do
  quakes  = [:EARTHQUAKE, :MAGNITUDE, :BULLDOZE, :FISSURE, :PRECIPICEBLADES, :HEADLONGRUSH, :DIG, :STOMPINGTANTRUM]
  floods  = [:SURF, :MUDDYWATER, :HYDROPUMP, :WATERSPOUT, :SPARKLINGARIA, :WATERPLEDGE, :WAVECRASH, :ORIGINPULSE]
  remelt  = [:ERUPTION, :LAVAPLUME, :MAGMASTORM, :FIREPLEDGE, :INFERNO, :BLASTBURN, :BURNUP, :FUSIONFLARE, :BLUEFLARE]
  winds   = [:GUST, :TWISTER, :HURRICANE, :AIRCUTTER, :RAZORWIND, :BLEAKWINDSTORM, :SANDSEARSTORM, :HEATWAVE]
  shards  = [:STONEEDGE, :STONEAXE, :ROCKSLIDE, :ROCKTHROW, :POWERGEM, :DIAMONDSTORM, :ROCKWRECKER]
  steamproof = [:WATERVEIL, :WATERBUBBLE, :HEATPROOF, :MAGMAARMOR, :STEAMENGINE, :FLASHFIRE, :WATERABSORB,
                :STORMDRAIN, :DRYSKIN, :THERMALEXCHANGE]
  geyser = lambda do |battle|
    battle.pbDisplay(FieldEffects.format("Geysers of steam blast up through the glass!"))
    battle.pbPriority(true).each do |b|
      next if b.fainted?
      if b.pbHasType?(:WATER) || b.pbHasType?(:FIRE) || b.hasActiveAbility?(:STEAMENGINE)
        if b.pbCanRaiseStatStage?(:SPEED, b)
          battle.pbDisplay(FieldEffects.format("{1} rode the blast of steam!", b.pbThis))
          b.pbRaiseStatStage(:SPEED, 1, b)
        end
      elsif !b.airborne? && !b.hasActiveAbility?(steamproof)
        FieldEffects.apply_battler_effect(battle, b, { :damage => 1/8r, :damage_type => :WATER,
                                                       :message => "A geyser erupted right beneath {1}!" })
        b.pbFaint if b.fainted?
      end
    end
  end
  {
    :name          => "Cinderglass",
    :backdrop      => "field_ashen_waste",
    :family        => :elemental,
    :intro_message => "The magma has set into black glass... and steam roars from every crack!",
    :description   => "A quenched volcano of obsidian, steam and geysers. Swimmers and fire Pokemon ride the steam; water flashes into blinding clouds; obsidian sharpens every rock.",
    :notes         => ["Rock x1.3, Ground x1.2, Fire x1.2 (heat still glows under the glass). Ice x0.7.",
                       "Geysers blow every 3 rounds (a quake or Dig sets them off that round): Water and Fire types and Steam Engine ride the steam (+1 Speed); other grounded Pokemon take a 1/8 blast (Water-scaled; Water Veil, Heatproof, Magma Armor, Water Absorb... are safe).",
                       "Water floods (Surf, Hydro Pump, Muddy Water...) flash into steam: every Pokemon that isn't Water or Fire type loses 1 accuracy.",
                       "Scald, Steam Eruption, Hydro Steam x1.5 and burn more often (x1.5).",
                       "Obsidian shards: Stone Edge, Stone Axe, Rock Slide, Rock Throw, Power Gem, Diamond Storm, Rock Wrecker x1.3. Stealth Rock cuts twice as deep (Heavy-Duty Boots protect).",
                       "Wind moves whip up glass grit: they also hit as Rock and may lower accuracy (30%). Sandstorms become glass storms (+3 turns).",
                       "Sand Rush and Sand Veil work in the glass-grit. Rock Polish also +1 Speed (it polishes on the obsidian); Smokescreen drops accuracy one stage more.",
                       "Steam Engine +1 Speed on entry and every turn. Magma Armor +1 Def on entry. Hail melts in the steam.",
                       "3 big fire moves (Eruption, Lava Plume, Magma Storm, Blast Burn...) re-melt it -> Volcanic Field. 3 floods (even ones that miss) or heavy rain fill the caldera -> Water Surface.",
                       "Elemental Seed: +1 Speed, +1 evasion (a cloak of steam), but -1 accuracy (it can't see out either)."],
    :nature_power  => :SCORCHINGSANDS,
    :camouflage    => :ROCK,
    :secret_power  => 8,
    :activate_abilities => [:SANDRUSH, :SANDVEIL],
    :type_mods     => { :ROCK => 1.3, :GROUND => 1.2, :FIRE => 1.2, :ICE => 0.7 },
    :type_messages => { :ROCK => "{1} hurled shards of razor-edged obsidian!",
                        :FIRE => "The heat beneath the glass flared up with {2}!",
                        :ICE  => "The ice cracked apart on the hot glass..." },
    :move_mods     => { :SCALD => 1.5, :STEAMERUPTION => 1.5, :HYDROSTEAM => 1.5 }.merge(shards.map { |m| [m, 1.3] }.to_h),
    :move_messages => { :SCALD         => "The steam vents brought the water to a boil!",
                        :STEAMERUPTION => "The whole caldera vented with {1}!",
                        :STONEEDGE     => "Obsidian shards sliced through the steam!" },
    :effect_chance_mods => [{ :moves => [:SCALD, :STEAMERUPTION, :HYDROSTEAM], :mult => 1.5 }],
    :extra_types   => [
      { :moves => winds, :category => :damaging, :add => :ROCK, :message => "The wind whipped up a storm of glass grit!" }
    ],
    :damage_mods   => [
      { :moves => winds, :category => :damaging, :in_weather => [:Sandstorm], :mult => 1.2,
        :message => "The glass storm sharpened {2}!" }
    ],
    :added_effects => [
      { :moves => winds, :category => :damaging, :chance => 30, :stats => { :ACCURACY => -1 },
        :message => "Glass grit stung {1}'s eyes!" }
    ],
    :move_stat_boosts => [
      { :moves => [:ROCKPOLISH], :user_stats => { :SPEED => 1 }, :message => "{1} polished itself to a mirror shine on the obsidian!" },
      { :moves => [:SMOKESCREEN], :target_stats => { :ACCURACY => -1 }, :message => "The smoke mixed with the steam!" }
    ],
    :on_entry      => [
      { :battlers => { :abilities => [:STEAMENGINE] }, :stats => { :SPEED => 1 },
        :message => "{1} fired up on the steam vents!" },
      { :battlers => { :abilities => [:MAGMAARMOR] }, :stats => { :DEFENSE => 1 },
        :message => "{1}'s armor set like obsidian!" },
      # Stealth Rock gets obsidian edges: a second Rock-scaled cut on entry
      { :battlers => { :not_items => [:HEAVYDUTYBOOTS],
                       :condition => proc { |battle, b| b.pbOwnSide.effects[PBEffects::StealthRock] } },
        :damage => 1/8r, :damage_type => :ROCK, :message => "The obsidian-edged stones cut deep into {1}!" }
    ],
    :end_of_round  => [
      { :battlers => { :abilities => [:STEAMENGINE] }, :stats => { :SPEED => 1 },
        :message => "{1} drew power from the steam vents!" }
    ],
    :weather       => { :block => [:Hail], :block_message => "The hail melted in the rising steam!",
                        :extend => { :Sandstorm => 3 } },
    :hooks         => {
      :on_start     => proc { |battle, old_id| FieldEffects.state(battle)[:geyser] = 3 },
      :after_move   => proc { |battle, user, targets, move, num_hits|
        next if user.lastMoveFailed
        st = FieldEffects.state(battle)
        if quakes.include?(move.id) && (st[:geyser] || 3) > 1
          st[:geyser] = 1
          battle.pbDisplay(FieldEffects.format("The glass cracked! The geysers are about to blow!"))
        end
        next if !floods.include?(move.id)
        battle.pbDisplay(FieldEffects.format("The water flashed into steam on the hot glass!"))
        battle.allBattlers.each do |b|
          next if b.fainted? || b.pbHasType?(:WATER) || b.pbHasType?(:FIRE)
          b.pbLowerStatStage(:ACCURACY, 1, nil) if b.pbCanLowerStatStage?(:ACCURACY, nil)
        end
      },
      :end_of_round => proc { |battle|
        st = FieldEffects.state(battle)
        st[:geyser] = (st[:geyser] || 3) - 1
        if st[:geyser] <= 0
          geyser.call(battle)
          st[:geyser] = 3
        elsif st[:geyser] == 1
          battle.pbDisplay(FieldEffects.format("The ground hisses... the geysers will blow next turn!"))
        end
      }
    },
    :transitions   => [
      { :moves => remelt, :to => :VOLCANIC, :uses => 3,
        :progress_message => "The glass is glowing red again... ({1} more)",
        :message => "The glass cracked open and magma welled up! The volcano lives again!" },
      { :moves => floods, :to => :WATER_SURFACE, :uses => 3, :even_if_failed => true,
        :progress_message => "Hot water is pooling in the caldera... ({1} more)",
        :message => "The caldera flooded into a steaming hot-spring lake!" },
      { :weather => [:HeavyRain], :to => :WATER_SURFACE,
        :message => "The downpour flooded the caldera into a steaming lake!" }
    ],
    :seed => { :item => :ELEMENTALSEED, :stats => { :SPEED => 1, :EVASION => 1, :ACCURACY => -1 },
               :message => "{1}'s {2} wrapped it in a cloak of steam!" }
  }
end).call)
