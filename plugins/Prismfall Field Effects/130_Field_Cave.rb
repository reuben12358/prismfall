#===============================================================================
# CAVE - Velmora's caves, mine tunnels and dungeon routes.
# Stage 1: stable cave. Stage 2: cracked ceiling - the next quake caves it in.
#-------------------------------------------------------------------------------
# Helpers live inside the lambda: Essentials evals every plugin file in
# TOPLEVEL_BINDING, so top-level locals would leak between field files.
#===============================================================================
FieldEffects.register(:CAVE, (lambda do
  quakes = [:EARTHQUAKE, :MAGNITUDE, :BULLDOZE, :FISSURE, :LANDSWRATH, :PRECIPICEBLADES,
            :THOUSANDWAVES, :HEADLONGRUSH]
  cave_in = proc { |battle, user, targets, move, num_hits|
    next if user.lastMoveFailed || !quakes.include?(move.id)
    battle.pbDisplay(FieldEffects.format("The cracked ceiling gave way! Rocks rained down!"))
    battle.pbPriority(true).each do |b|
      next if b.fainted? || b.hasActiveAbility?([:ROCKHEAD, :BULLETPROOF, :OVERCOAT])
      FieldEffects.apply_battler_effect(battle, b, { :damage => 1/8r, :damage_type => :ROCK,
                                                     :message => "{1} was struck by falling rocks!" })
      b.pbFaint if b.fainted?
    end
  }
  {
    :name          => "Cave",
    :backdrop      => "field_cave",
    :intro_message => "The cave walls loom close... every sound echoes.",
    :description   => "Rock surges and sound echoes; ranged Flying moves are stifled. Quakes crack the ceiling - twice, and it caves in.",
    :notes         => ["Boosted: Rock x1.5, sound moves x1.5, Rock Climb x1.5.",
                       "Flying moves that don't make contact x0.5. Sky Drop fails.",
                       "Stealth Rock hits twice as hard. Sun, Rain and Hail can't reach underground.",
                       "A quake move cracks the ceiling; a second one brings it down on everyone."],
    :nature_power  => :ROCKTOMB,
    :camouflage    => :ROCK,
    :secret_power  => 7,
    :type_mods     => { :ROCK => 1.5 },
    :type_messages => { :ROCK => "The cavern rumbled!" },
    :move_mods     => { :ROCKCLIMB => 1.5 },
    :move_messages => { :ROCKCLIMB => "{1} scrambled up the cave wall!" },
    :damage_mods   => [
      { :flags => ["Sound"], :category => :damaging, :mult => 1.5, :message => "{2} echoed through the cave!" },
      { :types => [:FLYING], :category => :damaging, :mult => 0.5,
        :condition => proc { |battle, user, target, move, type| !move.pbContactMove?(user) },
        :message => "There's no room to maneuver in the cramped cave..." }
    ],
    :accuracy_mods => [{ :flags => ["Sound"], :category => :status, :mult => 1.3 }],
    :move_stat_boosts => [
      { :moves => [:FLASH], :target_stats => { :ACCURACY => -1 }, :message => "The flash was blinding in the dark!" },
      { :moves => [:HOWL], :user_stats => { :ATTACK => 1 }, :message => "{1}'s howl echoed back at it!" }
    ],
    :move_fails    => [{ :moves => [:SKYDROP], :message => "The ceiling is too low to fly up!" }],
    :on_entry      => [
      { :battlers => { :not_items => [:HEAVYDUTYBOOTS],
                       :condition => proc { |battle, b| b.pbOwnSide.effects[PBEffects::StealthRock] } },
        :damage => 1/8r, :damage_type => :ROCK, :message => "Loose rocks rained down on {1}!" }
    ],
    :weather       => { :block => [:Sun, :Rain, :Hail],
                        :block_message => "There's no sky down here - the weather can't reach the cave!",
                        :extend => { :Sandstorm => 3 } },
    :transitions   => [
      { :moves => quakes, :stage => 2, :message => "The cave shook violently! Cracks spread across the ceiling..." }
    ],
    :stages        => {
      2 => {
        :intro_message => "Cracks run across the cave ceiling...",
        :description   => "The ceiling is cracked: the next quake move brings it down on every Pokémon.",
        :hooks         => { :after_move => cave_in },
        :transitions   => [{ :moves => quakes, :stage => 1, :message => "The dust slowly settles over the rubble." }]
      }
    },
    :seed => { :item => :TELLURICSEED, :stats => { :DEFENSE => 1 },
               :message => "{1}'s {2} shook stones loose from the ceiling!",
               :proc => proc { |battle, battler|
                 side = battler.pbOpposingSide
                 next false if side.effects[PBEffects::StealthRock]
                 side.effects[PBEffects::StealthRock] = true
                 battle.pbDisplay(FieldEffects.format("Pointed stones float in the air around {1}!",
                                                      battler.pbOpposingTeam(true)))
                 true
               } }
  }
end).call)
