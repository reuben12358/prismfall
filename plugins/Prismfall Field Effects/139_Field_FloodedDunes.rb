#===============================================================================
# FLOODED_DUNES - (new, SPINE Revisions 10/18) Kyogre's flood-sea over the Bone
# Sands: the Northern Sea dragged in over Ossaria's western dunes (map 926, the
# Glass Dunes, in the Ch19 war). Seawater fills the hollows between the dune
# crests and the sand under it turns to sucking mud.
#   * Swimmers ride the flood; current races through it; the sea-cold sharpens
#     ice; quakes churn the wet sand into mud and quicksand.
#   * Fire is hissed down to steam - except the white fire of the searing moves
#     (and Turboblaze), which flashes the flood into blinding steam instead.
#   * The tide: the flood drains into the sand after 5 rounds unless rain holds
#     it or Water attacks feed it (sun drains it twice as fast). When it drains,
#     the soaked dunes burst into the Desert's Superbloom (stage 2).
# Blue Flare / Fusion Flare (or 2 other searing moves, even ones the heavy rain
# snuffs) fuse the wet sand into GLASS_DUNES; 3 big Ice moves freeze the flood
# into FROZEN_LAKE. What DESERT becomes under heavy rain or Origin Pulse.
# Family: Elemental.
#===============================================================================
FieldEffects.register(:FLOODED_DUNES, (lambda do
  white_fire = [:BLUEFLARE, :FUSIONFLARE]
  searing    = [:ERUPTION, :BLASTBURN, :MAGMASTORM, :BURNUP, :OVERHEAT, :ARMORCANNON, :VCREATE]
  big_ice    = [:BLIZZARD, :SHEERCOLD, :GLACIATE, :ICEBEAM, :FREEZEDRY, :ICICLECRASH, :MOUNTAINGALE]
  mud        = [:MUDSHOT, :MUDBOMB, :MUDSLAP, :MUDDYWATER]
  tide_max   = 6
  tide_start = 5
  # The tide only runs while this IS the field (a Bleed that borrows these
  # effects keeps the steam but never drains or changes the field).
  on_field = lambda { |battle| FieldEffects.current(battle) == :FLOODED_DUNES }
  after_move = proc { |battle, user, targets, move, num_hits|
    next if user.lastMoveFailed || !move.damagingMove?
    type = move.calcType
    if (white_fire + searing).include?(move.id) && !targets.empty?
      battle.pbDisplay(FieldEffects.format("The white fire flashed the floodwater into scalding steam!"))
      battle.allOtherSideBattlers(user.index).each do |b|
        next if b.fainted? || b.pbHasType?(:FIRE)
        b.pbLowerStatStage(:ACCURACY, 1, user) if b.pbCanLowerStatStage?(:ACCURACY, user)
      end
    end
    next if type != :WATER || !on_field.call(battle)
    st = FieldEffects.state(battle)
    tide = st[:tide] || tide_start
    next if tide >= tide_max
    st[:tide] = tide + 1
    battle.pbDisplay(FieldEffects.format("{1} called the sea back in over the dunes!", user.pbThis)) if tide <= 2
  }
  ebb = proc { |battle|
    next if !on_field.call(battle)
    st = FieldEffects.state(battle)
    tide = st[:tide] || tide_start
    weather = battle.pbWeather
    next if [:Rain, :HeavyRain].include?(weather)   # Kyogre's rain holds the sea in
    tide -= case weather
            when :HarshSun then 3
            when :Sun      then 2
            else                1
            end
    st[:tide] = tide
    if tide > 0
      battle.pbDisplay(FieldEffects.format("The floodwater is sinking into the sand...")) if tide <= 2
      next
    end
    if battle.change_field(:DESERT, "The flood-sea drained away into the sand... and the soaked dunes burst into a superbloom!")
      battle.set_field_stage(2, "")
    end
  }
  ai_keep_tide = proc { |score, move, user, ai, battle|
    next score if !on_field.call(battle) || !move.damagingMove? || move.rough_type != :WATER
    next score if [:Rain, :HeavyRain].include?(battle.pbWeather)
    next score if (FieldEffects.state(battle)[:tide] || tide_start) > 2
    keep = FieldEffects::AIField.field_value(battle, :FLOODED_DUNES, 1, user.battler) -
           FieldEffects::AIField.field_value(battle, :DESERT, 2, user.battler)
    next score + (keep * 20).round.clamp(-12, 12)
  }
  {
    :name          => "Flooded Dunes",
    :backdrop      => "field_flooded_dunes",
    :family        => :elemental,
    :intro_message => "The sea has come to the sand! Floodwater pours in between the dunes!",
    :description   => "Kyogre's flood-sea over the Bone Sands: swimmers ride it between the dune crests, the wet sand turns quakes to mud, and only the white fire can fuse it to glass. It drains away unless rain or Water attacks hold it.",
    :notes         => ["Water x1.3, Ice x1.2 (the cold of the Northern Sea). Electric x1.3 against grounded targets standing in the flood.",
                       "Fire is hissed down to steam: damaging Fire moves x0.5 against grounded targets - except searing moves (Blue Flare, Fusion Flare, Eruption, Blast Burn, Overheat, V-create...) and Turboblaze users.",
                       "A searing move flashes the flood into scalding steam: every foe of the user that isn't Fire type loses 1 accuracy.",
                       "Mud: damaging Ground moves also hit as Water. Mud Shot, Mud Bomb, Mud-Slap, Muddy Water, Whirlpool and Sand Tomb x1.5 (Whirlpool and Sand Tomb more accurate). Physical Ground moves may churn quicksand round a grounded target (30%: Speed -1).",
                       "Wave Crash, Dive, Aqua Step, Flip Turn x1.3; Surf, Surging Strikes x1.2. Spikes, Toxic Spikes and Stealth Rock sink without a trace.",
                       "Wading: grounded Pokemon that aren't Water or Ground type move at x0.75 Speed (Swift Swim, Surge Surfer and Turboblaze aren't slowed). Swift Swim, Torrent, Rain Dish, Hydration and Dry Skin act as if it were raining.",
                       "Grounded Pokemon can't be burned, and the cold water soothes old burns. Water Absorb and Storm Drain drink in the flood (1/16 HP). Water Compaction +1 Def and +1 Sp. Def, Steam Engine +1 Speed on entry.",
                       "Rain lasts 3 turns longer; sandstorms can't blow over the water.",
                       "The tide: the flood drains into the sand after 5 rounds unless it rains; each damaging Water attack feeds it a round (max 6); sun drains it twice as fast. Drained, it leaves the Desert's Superbloom.",
                       "Blue Flare or Fusion Flare (or 2 other searing moves) fuse the wet sand into the Glass Dunes - even when heavy rain snuffs the flame. 3 big Ice moves freeze the flood into a Frozen Lake.",
                       "Elemental Seed: +1 Speed, and the holder is soaked through: it becomes part Water type (no wading, but Electric and Grass hit it harder)."],
    :nature_power  => :MUDDYWATER,
    :camouflage    => :WATER,
    :secret_power  => 4,
    :activate_abilities => [:SWIFTSWIM, :TORRENT, :RAINDISH, :HYDRATION, :DRYSKIN],
    :type_mods     => { :WATER => 1.3, :ICE => 1.2 },
    :type_messages => { :WATER => "{1} rode the flood-sea into the attack!",
                        :ICE   => "{1} drew the sea-cold of the flood into {2}!" },
    :move_mods     => { :WHIRLPOOL => 1.5, :SANDTOMB => 1.5, :MUDDYWATER => 1.5, :MUDSHOT => 1.5, :MUDBOMB => 1.5,
                        :MUDSLAP => 1.5, :WAVECRASH => 1.3, :DIVE => 1.3, :AQUASTEP => 1.3, :FLIPTURN => 1.3,
                        :SURF => 1.2, :SURGINGSTRIKES => 1.2 },
    :move_messages => { :WHIRLPOOL  => "The flood spun into a whirl that dragged at the sand!",
                        :SANDTOMB   => "{1} dragged the wet sand into a sucking whirl!",
                        :MUDDYWATER => "{1} hurled a wall of sand and sea!",
                        :WAVECRASH  => "{1} rode a breaking wave across the dunes!",
                        :DIVE       => "{1} burst up out of a flooded hollow!" },
    :extra_types   => [
      { :types => [:GROUND], :category => :damaging, :add => :WATER,
        :message => "{1} churned the wet sand into a surge of mud!" }
    ],
    :damage_mods   => [
      { :types => [:ELECTRIC], :category => :damaging, :target => { :grounded => true }, :mult => 1.3,
        :message => "The current raced through the floodwater!" },
      { :types => [:FIRE], :category => :damaging, :not_moves => white_fire + searing,
        :user => { :not_abilities => [:TURBOBLAZE] }, :target => { :grounded => true }, :mult => 0.5,
        :message => "The flood hissed the flames down to steam..." }
    ],
    :accuracy_mods => [{ :moves => [:WHIRLPOOL, :SANDTOMB], :mult => 1.25 }],
    :added_effects => [
      { :types => [:GROUND], :category => :physical, :chance => 30, :stats => { :SPEED => -1 },
        :target => { :grounded => true }, :message => "The blow churned quicksand round {1}!" }
    ],
    :move_fails    => [
      { :moves => [:SPIKES, :TOXICSPIKES, :STEALTHROCK], :message => "{2} sank into the floodwater without a trace!" }
    ],
    :speed_mods    => [
      { :battlers => { :grounded => true, :not_types => [:WATER, :GROUND],
                       :not_abilities => [:SWIFTSWIM, :SURGESURFER, :TURBOBLAZE] }, :mult => 0.75 }
    ],
    :status_immunity => [
      { :battlers => { :grounded => true }, :status => [:BURN], :message => "The floodwater kept {1} from burning!" }
    ],
    :on_entry      => [
      { :battlers => { :abilities => [:WATERCOMPACTION] }, :stats => { :DEFENSE => 1, :SPECIAL_DEFENSE => 1 },
        :message => "{1} packed the wet sand tight around itself!" },
      { :battlers => { :abilities => [:STEAMENGINE] }, :stats => { :SPEED => 1 },
        :message => "{1} drew steam from the floodwater!" }
    ],
    :end_of_round  => [
      { :battlers => { :grounded => true, :status => [:BURN] }, :cure_status => true,
        :message => "The cold floodwater soothed {1}'s burn!" },
      { :battlers => { :abilities => [:WATERABSORB, :STORMDRAIN] }, :heal => 1/16r,
        :message => "{1} drank in the flood-sea." }
    ],
    :weather       => { :block => [:Sandstorm], :block_message => "The flood-sea swallowed the sand before it could blow!",
                        :extend => { :Rain => 3 } },
    :terrain       => { :extend => { :Misty => 2 } },
    :hooks         => {
      :on_start     => proc { |battle, old_id| FieldEffects.state(battle)[:tide] = tide_start },
      :after_move   => after_move,
      :end_of_round => ebb,
      :ai_score     => ai_keep_tide
    },
    :transitions   => [
      { :id => :white_fire, :moves => white_fire, :to => :GLASS_DUNES, :even_if_failed => true,
        :message => "The white fire flashed the flood to steam and fused the drowned sand into glass!" },
      { :id => :glassing, :moves => searing, :to => :GLASS_DUNES, :uses => 2, :even_if_failed => true,
        :progress_message => "Steam roars up as the wet sand starts to glaze... ({1} more)",
        :message => "The heat fused the flooded dunes into steaming glass!" },
      { :id => :freeze, :moves => big_ice, :category => :damaging, :to => :FROZEN_LAKE, :uses => 3,
        :progress_message => "Ice is creeping across the floodwater... ({1} more)",
        :message => "The flood-sea froze solid across the dunes!" }
    ],
    :seed => { :item => :ELEMENTALSEED, :stats => { :SPEED => 1 }, :add_type => :WATER,
               :message => "{1}'s {2} soaked it through - it rides the flood like a swimmer!" }
  }
end).call)
