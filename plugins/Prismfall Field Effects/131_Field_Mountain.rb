#===============================================================================
# MOUNTAIN - Velmora's highland ridges and passes. Ice or hail -> SNOWY_MOUNTAIN.
# (Helpers inside the lambda so they don't leak into TOPLEVEL_BINDING.)
#===============================================================================
FieldEffects.register(:MOUNTAIN, (lambda do
  winds = [:GUST, :TWISTER, :RAZORWIND, :AIRCUTTER, :HURRICANE, :ICYWIND, :OMINOUSWIND, :SILVERWIND,
           :FAIRYWIND, :HEATWAVE, :PETALBLIZZARD, :BLIZZARD, :BLEAKWINDSTORM, :WILDBOLTSTORM,
           :SANDSEARSTORM, :SPRINGTIDESTORM]
  {
    :name          => "Mountain",
    :backdrop      => "field_mountain",
    :intro_message => "The wind howls across the mountain ridge!",
    :description   => "High, rocky and windswept: Rock and Flying surge, wind attacks gust harder, Tailwind lingers. Ice or hail buries it in snow.",
    :notes         => ["Boosted: Rock x1.5, Flying x1.2, wind moves x1.3, Avalanche x1.5.",
                       "Hurricane and the Storm moves are more accurate in the steady winds.",
                       "Tailwind lasts 2 turns longer. Wind Rider and Wind Power trigger on entry.",
                       "Sunlight lasts 3 turns longer in the thin air.",
                       "Hail, or 2 big ice moves, turn it into a Snowy Mountain."],
    :nature_power  => :ROCKSLIDE,
    :camouflage    => :ROCK,
    :secret_power  => 7,
    :type_mods     => { :ROCK => 1.5, :FLYING => 1.2 },
    :type_messages => { :ROCK => "Boulders tumbled down the mountainside!" },
    :move_mods     => { :AVALANCHE => 1.5, :SKYATTACK => 1.2 },
    :move_messages => { :AVALANCHE => "Rock and snow thundered down the slope!" },
    :damage_mods   => [
      { :moves => winds, :mult => 1.3, :message => "The mountain wind howled behind {2}!" }
    ],
    :accuracy_mods => [
      { :moves => [:HURRICANE, :BLEAKWINDSTORM, :WILDBOLTSTORM, :SANDSEARSTORM, :SPRINGTIDESTORM], :mult => 1.2 }
    ],
    :on_entry      => [
      { :battlers => { :abilities => [:WINDRIDER] }, :stats => { :ATTACK => 1 }, :also_on_change => true,
        :message => "{1} rode the mountain winds!" },
      { :battlers => { :abilities => [:WINDPOWER] }, :effects => [:charge], :also_on_change => true }
    ],
    :hooks         => {
      :after_move => proc { |battle, user, targets, move, num_hits|
        next if user.lastMoveFailed || move.id != :TAILWIND
        next if user.pbOwnSide.effects[PBEffects::Tailwind] <= 0
        user.pbOwnSide.effects[PBEffects::Tailwind] += 2
        battle.pbDisplay(FieldEffects.format("The mountain gale strengthened the Tailwind!"))
      }
    },
    :weather       => { :extend => { :Sun => 3 } },
    :transitions   => [
      { :weather => [:Hail], :to => :SNOWY_MOUNTAIN, :message => "Snow blanketed the mountain!" },
      { :moves => [:BLIZZARD, :MOUNTAINGALE, :SHEERCOLD, :GLACIATE], :to => :SNOWY_MOUNTAIN, :uses => 2,
        :progress_message => "Frost creeps across the rocks... ({1} more)",
        :message => "A snowstorm swept over the peaks!" }
    ],
    :seed => { :item => :ELEMENTALSEED, :stats => { :SPEED => 1 },
               :message => "{1}'s {2} caught the mountain wind!",
               :proc => proc { |battle, battler|
                 side = battler.pbOwnSide
                 next false if side.effects[PBEffects::Tailwind] > 0
                 side.effects[PBEffects::Tailwind] = 4
                 battle.pbDisplay(FieldEffects.format("The Tailwind blew from behind {1}!", battler.pbTeam(true)))
                 true
               } }
  }
end).call)
