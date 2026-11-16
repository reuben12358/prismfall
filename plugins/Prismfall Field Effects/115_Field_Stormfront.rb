#===============================================================================
# STORMFRONT - Gym 11 (Flying), Skyreach in Zenith. An airship deck at the top
# of the spire, inside the permanent storm wall. Wind moves howl, Tailwinds
# last, and in the rain lightning seeks out whatever flies highest.
# "Skyreach's got one law: the wind doesn't care." - Odessa Gale
#===============================================================================
FieldEffects.register(:STORMFRONT, {
  :name          => "Stormfront",
  :backdrop      => "field_stormfront",
  :intro_message => "Gale-force winds howl across the airship deck!",
  :description   => "Wind and Electric moves surge; Tailwind lasts longer; Hurricane and Thunder never miss. In rain, lightning strikes airborne Pokémon. No sunlight.",
  :nature_power  => :HURRICANE,
  :camouflage    => :FLYING,
  :secret_power  => 0,
  :type_mods     => { :FLYING => 1.2, :ELECTRIC => 1.3 },
  :type_messages => { :ELECTRIC => "The storm supercharged the attack!" },
  :move_mods     => { :FLY => 1.3, :BOUNCE => 1.3, :SKYDROP => 1.3, :SMACKDOWN => 2.0,
                      :THOUSANDARROWS => 1.5 },
  :move_messages => { :SMACKDOWN      => "The gale slammed the target onto the deck!",
                      :THOUSANDARROWS => "The gale slammed the target onto the deck!",
                      :FLY            => "{1} rode the updraft!" },
  :damage_mods   => [
    { :moves => [:GUST, :TWISTER, :HURRICANE, :AIRCUTTER, :RAZORWIND, :ICYWIND, :HEATWAVE,
                 :FAIRYWIND, :SILVERWIND, :OMINOUSWIND, :PETALBLIZZARD, :BLIZZARD,
                 :BLEAKWINDSTORM, :WILDBOLTSTORM, :SANDSEARSTORM, :SPRINGTIDESTORM],
      :mult => 1.2, :message => "The gale whipped {2} into a frenzy!" }
  ],
  :accuracy_mods => [
    { :moves => [:HURRICANE, :THUNDER, :BLEAKWINDSTORM, :WILDBOLTSTORM, :SANDSEARSTORM,
                 :SPRINGTIDESTORM], :always_hit => true }
  ],
  :on_entry      => [
    { :battlers => { :abilities => [:WINDRIDER] }, :stats => { :ATTACK => 1 }, :also_on_change => true,
      :message => "{1} caught the gale!" },
    { :battlers => { :abilities => [:WINDPOWER] }, :effects => [:charge], :also_on_change => true,
      :message => "The howling wind charged {1} with power!" }
  ],
  :end_of_round  => [
    # In the rain the storm breaks: lightning finds the highest target
    { :battlers => { :grounded => false,
                     :not_abilities => [:LIGHTNINGROD, :VOLTABSORB, :MOTORDRIVE],
                     :condition => proc { |battle, b| [:Rain, :HeavyRain].include?(battle.pbWeather) } },
      :chance => 15, :damage => 1/8r, :damage_type => :ELECTRIC, :animation => "Paralysis",
      :message => "Lightning struck {1}!" },
    { :battlers => { :abilities => [:LIGHTNINGROD],
                     :condition => proc { |battle, b| [:Rain, :HeavyRain].include?(battle.pbWeather) } },
      :chance => 15, :stats => { :SPECIAL_ATTACK => 1 }, :message => "{1} drew a lightning bolt!" },
    { :battlers => { :abilities => [:MOTORDRIVE],
                     :condition => proc { |battle, b| [:Rain, :HeavyRain].include?(battle.pbWeather) } },
      :chance => 15, :stats => { :SPEED => 1 }, :message => "{1} drew a lightning bolt!" },
    { :battlers => { :abilities => [:VOLTABSORB],
                     :condition => proc { |battle, b| [:Rain, :HeavyRain].include?(battle.pbWeather) } },
      :chance => 15, :heal => 1/8r, :message => "{1} drew a lightning bolt!" }
  ],
  :weather       => { :block => [:Sun], :block_message => "The storm clouds swallowed the sunlight!" },
  :terrain       => { :extend => { :Electric => 3 } },
  :hooks         => {
    # Tailwind rides the storm: 2 extra turns
    :after_move => proc { |battle, user, targets, move, num_hits|
      next if user.lastMoveFailed || move.id != :TAILWIND
      next if user.pbOwnSide.effects[PBEffects::Tailwind] <= 0
      user.pbOwnSide.effects[PBEffects::Tailwind] += 2
      battle.pbDisplay(FieldEffects.format("The storm will carry the Tailwind for longer!"))
    }
  },
  :seed => { :item => :ELEMENTALSEED, :stats => { :SPEED => 1 }, :effects => [:charge],
             :message => "{1}'s {2} crackled with storm energy!" }
})
