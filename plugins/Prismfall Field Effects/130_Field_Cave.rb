#===============================================================================
# CAVE - Velmora's caves, mine tunnels and dungeon routes.
# Rock Pokemon own the walls, every sound echoes, the low ceiling grounds the
# fliers. Stage 1: stable cave. Stage 2: cracked ceiling - the next quake
# brings it down on everyone (Reborn's cave collapse). Gems turn the walls to
# crystal (CRYSTAL_CAVERN), magma breaks through (VOLCANIC), draconic energy
# seeps in (DRAGONS_DEN). Family: Telluric.
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
                                                     :message => "Falling rocks crashed down around {1}!" })
      b.pbFaint if b.fainted?
    end
  }
  exits = [
    { :moves => [:POWERGEM, :DIAMONDSTORM], :to => :CRYSTAL_CAVERN, :uses => 2,
      :progress_message => "Crystals are sprouting from the cave walls... ({1} more)",
      :message => "The cave walls bloomed into glittering crystal!" },
    { :moves => [:ERUPTION, :LAVAPLUME, :MAGMASTORM, :FIREPLEDGE, :BLASTBURN], :to => :VOLCANIC, :uses => 2,
      :progress_message => "The cave is heating up... ({1} more)",
      :message => "Magma broke through the cave floor!" },
    { :moves => [:DRACOMETEOR], :to => :DRAGONS_DEN,
      :message => "The meteor tore open a dragon's lair hidden in the deep!" },
    { :moves => [:DRAGONPULSE, :DRAGONENERGY, :CLANGINGSCALES], :to => :DRAGONS_DEN, :uses => 2,
      :progress_message => "Draconic energy seeps in from the deep... ({1} more)",
      :message => "The cave opened into an ancient dragon's lair!" }
  ]
  {
    :name          => "Cave",
    :backdrop      => "field_cave",
    :family        => :telluric,
    :intro_message => "The cave walls loom close... every sound echoes.",
    :description   => "Rock Pokemon own the walls and every sound echoes; the low ceiling grounds fliers. Quakes crack the ceiling - twice, and it caves in. Gems, magma or dragons can open it into somewhere else.",
    :notes         => ["Rock x1.5. Damaging sound moves x1.5 (they echo). Rock Climb, Rock Tomb, Drill Run, Hyper Drill, Drum Beating, Dig x1.5.",
                       "The ceiling is low: Flying moves that don't make contact x0.5; Ground moves hit Flying types; Sky Drop fails.",
                       "Sound-based status moves (Sing, Supersonic, Screech, Metal Sound...) x1.3 accuracy. Flash drops accuracy one stage more; Howl also +1 Attack.",
                       "Stealth Rock hits twice as hard (Heavy-Duty Boots protect).",
                       "Underground: Sun, Rain and Hail can't start. Sandstorm lasts 3 turns longer.",
                       "Cave-in: a quake (Earthquake, Magnitude, Bulldoze, Fissure, Land's Wrath, Precipice Blades, Thousand Waves, Headlong Rush) cracks the ceiling. The next quake brings it down: everyone takes 1/8 HP of Rock-type damage (Rock Head, Bulletproof, Overcoat are safe), and the dust settles.",
                       "2 Power Gems / Diamond Storms -> Crystal Cavern. 2 of Eruption, Lava Plume, Magma Storm, Fire Pledge, Blast Burn -> Volcanic Field. Draco Meteor, or 2 Dragon Pulses -> Dragon's Den.",
                       "Telluric Seed: +1 Defense and scatters Stealth Rock on the opposing side."],
    :nature_power  => :ROCKTOMB,
    :camouflage    => :ROCK,
    :secret_power  => 7,
    :type_mods     => { :ROCK => 1.5 },
    :type_messages => { :ROCK => "The cavern rumbled with {1}'s power!" },
    :move_mods     => { :ROCKCLIMB => 1.5, :ROCKTOMB => 1.5, :DRILLRUN => 1.5, :HYPERDRILL => 1.5, :DRUMBEATING => 1.5,
                        :DIG => 1.5 },
    :move_messages => { :ROCKCLIMB   => "{1} scrambled up the cave wall!",
                        :DRILLRUN    => "{1} tunneled straight through the rock!",
                        :DIG         => "{1} tunneled straight through the rock!",
                        :DRUMBEATING => "The drumbeat boomed through the tunnels!" },
    :damage_mods   => [
      { :flags => ["Sound"], :category => :damaging, :mult => 1.5, :message => "{2} echoed through the cave!" },
      { :types => [:FLYING], :category => :damaging, :mult => 0.5,
        :condition => proc { |battle, user, target, move, type| !move.pbContactMove?(user) },
        :message => "There's no room to maneuver under the low ceiling..." }
    ],
    :effectiveness_mods => [{ :attack => [:GROUND], :defend => [:FLYING], :set => 1.0 }],
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
    ] + exits,
    :stages        => {
      2 => {
        :intro_message => "Cracks run across the cave ceiling...",
        :description   => "The ceiling is cracked: the next quake move brings it down on every Pokemon.",
        :hooks         => { :after_move => cave_in },
        :transitions   => [{ :moves => quakes, :stage => 1, :message => "The dust slowly settles over the rubble." }] + exits
      }
    },
    :seed => { :item => :TELLURICSEED, :stats => { :DEFENSE => 1 }, :effects => [:stealth_rock],
               :message => "{1}'s {2} shook stones loose from the ceiling!" }
  }
end).call)
