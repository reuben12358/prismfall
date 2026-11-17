#===============================================================================
# MOUNTAIN - Velmora's highland ridges and passes. Rock Pokemon send boulders
# down the slopes, fliers ride the ridge winds, throws send foes down the
# mountainside. Ice or hail buries it in snow (SNOWY_MOUNTAIN); magma breaks
# through the peak (VOLCANIC). Family: Telluric.
# (Helpers inside the lambda so they don't leak into TOPLEVEL_BINDING.)
#===============================================================================
FieldEffects.register(:MOUNTAIN, (lambda do
  winds = [:GUST, :TWISTER, :RAZORWIND, :AIRCUTTER, :HURRICANE, :ICYWIND, :OMINOUSWIND, :SILVERWIND,
           :FAIRYWIND, :HEATWAVE, :PETALBLIZZARD, :BLIZZARD, :BLEAKWINDSTORM, :WILDBOLTSTORM,
           :SANDSEARSTORM, :SPRINGTIDESTORM]
  throws = [:VITALTHROW, :CIRCLETHROW, :STORMTHROW, :SEISMICTOSS]
  {
    :name          => "Mountain",
    :backdrop      => "field_mountain",
    :family        => :telluric,
    :intro_message => "The wind howls across the mountain ridge!",
    :description   => "High, rocky and windswept: boulders tumble, fliers ride the ridge winds, throws send foes down the slope and Tailwind lingers. Ice buries it in snow; magma can break through the peak.",
    :notes         => ["Rock x1.5, Flying x1.2. Wind moves x1.3. Avalanche x1.5; throws (Vital Throw, Circle Throw, Storm Throw) x1.5; Sky Attack, Hyper Voice x1.2. Seismic Toss x1.25.",
                       "Hurricane and the Storm moves x1.2 accuracy; Thunder never misses on the peaks.",
                       "Tailwind lasts 2 turns longer. Wind Rider +1 Attack and Wind Power charged on entry (and when the field appears).",
                       "Sunlight lasts 3 turns longer in the thin air.",
                       "Hail, or 2 big ice moves (Blizzard, Mountain Gale, Sheer Cold, Glaciate) -> Snowy Mountain. 2 of Eruption, Lava Plume, Magma Storm, Fire Pledge -> Volcanic Field.",
                       "Telluric Seed: +1 Speed and a Tailwind for the holder's side."],
    :nature_power  => :ROCKSLIDE,
    :camouflage    => :ROCK,
    :secret_power  => 7,
    :type_mods     => { :ROCK => 1.5, :FLYING => 1.2 },
    :type_messages => { :ROCK => "Boulders tumbled down the mountainside!",
                        :FLYING => "{1} rode the ridge winds!" },
    :move_mods     => { :AVALANCHE => 1.5, :SKYATTACK => 1.2, :HYPERVOICE => 1.2 }.merge(throws.first(3).map { |m| [m, 1.5] }.to_h),
    :move_messages => { :AVALANCHE  => "Rock and snow thundered down the slope!",
                        :HYPERVOICE => "{2} echoed off every peak!",
                        :CIRCLETHROW => "{1} hurled its foe down the slope!",
                        :STORMTHROW  => "{1} hurled its foe down the slope!",
                        :VITALTHROW  => "{1} hurled its foe down the slope!" },
    :fixed_damage_mods => [{ :moves => [:SEISMICTOSS], :mult => 1.25, :message => "{1} hurled its foe down the slope!" }],
    :damage_mods   => [
      { :moves => winds, :category => :damaging, :mult => 1.3, :message => "The mountain wind howled behind {2}!" }
    ],
    :accuracy_mods => [
      { :moves => [:HURRICANE, :BLEAKWINDSTORM, :WILDBOLTSTORM, :SANDSEARSTORM, :SPRINGTIDESTORM], :mult => 1.2 },
      { :moves => [:THUNDER], :always_hit => true }
    ],
    :effect_durations => { :TAILWIND => [2, "The mountain gale strengthened the Tailwind!"] },
    :on_entry      => [
      { :battlers => { :abilities => [:WINDRIDER] }, :stats => { :ATTACK => 1 }, :also_on_change => true,
        :message => "{1} rode the mountain winds!" },
      { :battlers => { :abilities => [:WINDPOWER] }, :effects => [:charge], :also_on_change => true }
    ],
    :weather       => { :extend => { :Sun => 3 } },
    :transitions   => [
      { :weather => [:Hail], :to => :SNOWY_MOUNTAIN, :message => "Snow blanketed the mountain!" },
      { :moves => [:BLIZZARD, :MOUNTAINGALE, :SHEERCOLD, :GLACIATE], :to => :SNOWY_MOUNTAIN, :uses => 2,
        :progress_message => "Frost creeps across the rocks... ({1} more)",
        :message => "A snowstorm swept over the peaks!" },
      { :moves => [:ERUPTION, :LAVAPLUME, :MAGMASTORM, :FIREPLEDGE], :to => :VOLCANIC, :uses => 2,
        :progress_message => "The mountain rumbles from deep within... ({1} more)",
        :message => "The mountain erupted! Magma pours down the slopes!" }
    ],
    :seed => { :item => :TELLURICSEED, :stats => { :SPEED => 1 }, :effects => [:tailwind],
               :message => "{1}'s {2} caught the mountain wind!" }
  }
end).call)
