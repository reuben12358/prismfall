#===============================================================================
# GLASS_DUNES - (SPINE Revisions 10/18/24) The glass the white fire made of the
# Bone Sands. Real glass forms from sand only at extreme heat (lightning, the
# trinitite of a blast site, a meteor's impact glass): here the searing moves of
# the Ch19 war fuse the DESERT, or Reshiram's Blue Flare fuses Kyogre's flood
# (FLOODED_DUNES). The climax field of map 926. Both Imprints are still inside.
#   Stage 1 Hot Glass:    glass holds heat for a long time. It feeds fire,
#                         flashes water to scalding steam (Water attacks can
#                         burn), nothing freezes, and light bends through the
#                         heat haze. Thermal shock: big Ice moves crack it.
#   Stage 2 Mirror Glass: after 4 rounds without a damaging Fire move the glass
#                         cools (sun keeps it hot, rain cools it twice as
#                         fast). The steam clears and the dunes are one great
#                         mirror, Reborn's Mirror Arena: beams ricochet, mirror
#                         images multiply, glare blinds, reflections strike
#                         back harder. A damaging Fire move reheats it.
#   Both stages: glass is brittle. Quakes, heavy blows and loud sound crack it
#     (the Choir tunes Glassfall glass by singing to it; a loud enough voice
#     breaks it). A crack sprays shards at the user's foes and leaves them on
#     the ground on that side (an entry hazard, Rock-scaled, 1/16). 3 cracks
#     break the glass apart (DESERT, or FLOODED_DUNES if it's raining); each
#     damaging Fire move anneals one crack; cooling doesn't mend them. Glass
#     doesn't conduct: Electric is weaker against grounded targets and Electric
#     Terrain can't form. The sea can drown it again; the beam clash tears the
#     Imprints open into the BLEED.
# The cracks, the clash and the flood progress are carried across the stage
# change (set_field_stage clears transition counters; this file restores them).
# Family: Telluric.
#===============================================================================
FieldEffects.register(:GLASS_DUNES, (lambda do
  impacts = [:EARTHQUAKE, :MAGNITUDE, :BULLDOZE, :FISSURE, :PRECIPICEBLADES, :HEADLONGRUSH, :STOMPINGTANTRUM,
             :HIGHHORSEPOWER, :HEAVYSLAM, :ROCKSMASH, :EXPLOSION, :SELFDESTRUCT,
             :BRICKBREAK, :PSYCHICFANGS, :RAGINGBULL]   # barrier-breakers crack glass too (Gemini review 2026-11-21)
  chill   = [:BLIZZARD, :ICEBEAM, :SHEERCOLD, :GLACIATE, :FREEZEDRY, :ICICLECRASH, :AVALANCHE, :ICEHAMMER,
             :MOUNTAINGALE, :GLACIALLANCE, :FREEZINGGLARE]
  floods  = [:SURF, :MUDDYWATER, :HYDROPUMP, :WATERSPOUT, :WAVECRASH, :WATERPLEDGE, :HYDROCANNON]
  light   = [:AURORABEAM, :CHARGEBEAM, :DAZZLINGGLEAM, :FLASHCANNON, :LUSTERPURGE, :MIRRORSHOT, :PHOTONGEYSER,
             :POWERGEM, :PRISMATICLASER, :SIGNALBEAM, :SOLARBEAM]
  beams   = light + [:PSYBEAM, :ICEBEAM, :HYPERBEAM, :MOONGEISTBEAM, :METEORBEAM, :LUMINACRASH]
  blinders      = [:FLASH, :KINESIS, :SANDATTACK, :SMOKESCREEN]
  mirror_images = [:DOUBLETEAM, :MINIMIZE]
  strike_back   = [:COUNTER, :MIRRORCOAT, :METALBURST, :COMEUPPANCE]
  sweepers  = { :RAPIDSPIN => :own, :MORTALSPIN => :own, :DEFOG => :both, :TIDYUP => :both, :COURTCHANGE => :swap }
  sea_beam  = [:ORIGINPULSE, :WATERSPOUT, :HYDROCANNON, :HYDROPUMP, :STEAMERUPTION]
  fire_beam = [:BLUEFLARE, :FUSIONFLARE, :BLASTBURN, :ERUPTION, :VCREATE, :OVERHEAT]
  cool_after = 4
  on_field = lambda { |battle| FieldEffects.current(battle) == :GLASS_DUNES }
  sound    = lambda { |move| move.respond_to?(:soundMove?) && move.soundMove? }
  # What cracks the glass. Fire never does (it anneals), so Torch Song only heats it.
  cracks_hot = lambda { |move, type|
    move.damagingMove? && type != :FIRE && (impacts.include?(move.id) || chill.include?(move.id) || sound.call(move))
  }
  cracks_cool = lambda { |move, type|
    move.damagingMove? && type != :FIRE && (impacts.include?(move.id) || sound.call(move))
  }
  cracks = lambda { |battle, move, type|
    (FieldEffects.stage(battle) == 2) ? cracks_cool.call(move, type) : cracks_hot.call(move, type)
  }
  # set_field_stage clears every transition counter; the glass keeps its cracks (and the flood and clash progress).
  carried = [:pulse, :reflood, :shatter, :clash]
  to_stage = lambda { |battle, stage, msg, anneal|
    prog = carried.map { |tid| [tid, (FieldEffects.transition_progress(battle, tid) || [0])[0]] }.to_h
    healed = anneal > 0 && prog[:shatter] > 0
    prog[:shatter] = [prog[:shatter] - anneal, 0].max
    next false if !battle.set_field_stage(stage, msg)
    raw  = FieldEffects.raw_state(battle)
    list = FieldEffects.transitions(battle)
    prog.each do |tid, n|
      idx = list.index { |r| r[:id] == tid }
      raw[:counters][idx] = n if idx && n > 0
    end
    battle.pbDisplay(FieldEffects.format("The heat annealed the cracks in the glass!")) if healed
    true
  }
  after_move = proc { |battle, user, targets, move, num_hits|
    next if user.lastMoveFailed
    # This move already changed the field when it landed (the third crack, the flood): the glass is gone, and the
    # old field only lingers until the move is done (FieldEffects.move_landed). Nothing more happens to it.
    next if FieldEffects.respond_to?(:lingering?) && FieldEffects.lingering?(battle)
    here = on_field.call(battle)
    st = FieldEffects.state(battle)
    # Rapid Spin, Defog... sweep the broken glass away (Court Change swaps it)
    shards = st[:shards]
    if here && shards && !shards.empty? && (how = sweepers[move.id])
      own = user.index & 1
      if how == :swap
        st[:shards] = { 0 => shards[1], 1 => shards[0] }.reject { |_s, v| !v }
      else
        swept = ((how == :both) ? [0, 1] : [own]).select { |s| shards.delete(s) }
        battle.pbDisplay(FieldEffects.format("{1} swept the broken glass away!", user.pbThis)) if !swept.empty?
      end
    end
    next if !move.damagingMove? || targets.empty?
    type = move.calcType
    # Fire: keeps the glass hot, reheats Mirror Glass, anneals a crack
    if type == :FIRE && here
      st[:fire_turn] = battle.turnCount
      st[:heat] = cool_after
      if FieldEffects.stage(battle) == 2
        to_stage.call(battle, 1, FieldEffects.format("{1}'s fire flooded back into the glass! Steam is rising off the dunes again!",
                                                     user.pbThis), 1)
      elsif (FieldEffects.transition_progress(battle, :shatter) || [0])[0] > 0
        FieldEffects.rewind_transitions(battle, { :shatter => 1 })
        battle.pbDisplay(FieldEffects.format("The heat annealed the cracks in the glass!"))
      end
    end
    # A crack (counted by the :shatter rule when the move landed): shards fly at the user's grounded foes...
    if cracks.call(battle, move, type)
      battle.pbDisplay(FieldEffects.format("Shards flew up around {1}'s foes!", user.pbThis))
      battle.allOtherSideBattlers(user.index).each do |b|
        next if b.fainted? || b.airborne? || b.hasActiveItem?(:HEAVYDUTYBOOTS)
        FieldEffects.apply_battler_effect(battle, b, { :damage => 1/16r, :damage_type => :ROCK,
                                                       :message => "Flying glass caught {1}!" })
        b.pbFaint if b.fainted?
      end
      # ...and stay where they fell (only while this IS the field: a Bleed echo leaves none)
      if here
        st[:shards] ||= {}
        foe_side = 1 - (user.index & 1)
        if !st[:shards][foe_side]
          st[:shards][foe_side] = true
          battle.pbDisplay(FieldEffects.format("Broken glass lies scattered on the ground around {1}!",
                                               user.pbOpposingTeam(true)))
        end
      end
    end
    next if !here
    # Beam clash bookkeeping: which side landed a great Water / Fire beam this round
    side = user.index & 1
    turn = battle.turnCount
    st[:sea_beam]  = [turn, side] if sea_beam.include?(move.id)
    st[:fire_beam] = [turn, side] if fire_beam.include?(move.id)
  }
  # A grounded Pokemon switching in on a side with broken glass steps on it
  step_on = proc { |battle, battler|
    next if !on_field.call(battle) || battler.fainted?
    shards = FieldEffects.state(battle)[:shards]
    next if !shards || !shards[battler.index & 1]
    next if battler.airborne? || battler.hasActiveItem?(:HEAVYDUTYBOOTS)
    FieldEffects.apply_battler_effect(battle, battler, { :damage => 1/16r, :damage_type => :ROCK,
                                                         :message => "{1} stepped on the broken glass!" })
    battler.pbFaint if battler.fainted?
  }
  # Hot Glass cools after 4 rounds without a damaging Fire move (sun holds the heat, rain cools it twice as fast)
  cool = proc { |battle|
    next if !on_field.call(battle) || FieldEffects.stage(battle) != 1
    st = FieldEffects.state(battle)
    if st[:fire_turn] == battle.turnCount
      st[:heat] = cool_after
      next
    end
    weather = battle.pbWeather
    next if [:Sun, :HarshSun].include?(weather)
    st[:heat] = (st[:heat] || cool_after) - (([:Rain, :HeavyRain].include?(weather)) ? 2 : 1)
    if st[:heat] > 0
      battle.pbDisplay(FieldEffects.format("The steam is thinning... the glass is starting to cool.")) if st[:heat] == 2
      battle.pbDisplay(FieldEffects.format("The glass has almost cooled. The sky is beginning to shine in it...")) if st[:heat] == 1
      next
    end
    to_stage.call(battle, 2, "The glass dunes have cooled! The steam has cleared, and the whole sky shines in the glass!", 0)
  }
  clash = proc { |battle|
    st = FieldEffects.state(battle)
    w, f = st[:sea_beam], st[:fire_beam]
    next false if !w || !f || w[0] != battle.turnCount || f[0] != battle.turnCount || w[1] == f[1]
    st[:sea_beam] = st[:fire_beam] = nil
    battle.pbDisplay(FieldEffects.format("The beams locked over the glass! Both Imprints are ringing in it!"))
    true
  }
  shatter_to = proc { |battle| [:Rain, :HeavyRain].include?(battle.pbWeather) ? :FLOODED_DUNES : :DESERT }
  shatter_msg = "The glass dunes shattered into a thousand pieces and sank back into the dunes!"
  # The sea, the cracks and the clash: the same rules (and ids) on both stages, so their progress carries over.
  transitions_for = lambda { |crack_proc|
    [
      { :weather => [:HeavyRain], :to => :FLOODED_DUNES,
        :message => "The flood-sea broke back in over the glass dunes!" },
      { :id => :pulse, :moves => [:ORIGINPULSE], :to => :FLOODED_DUNES, :uses => 2,
        :progress_message => "The sea is rising against the glass... ({1} more)",
        :message => "The flood-sea broke back in over the glass dunes!" },
      { :id => :reflood, :moves => floods, :to => :FLOODED_DUNES, :uses => 3, :even_if_failed => true,
        :progress_message => "Water is pooling between the glass dunes... ({1} more)",
        :message => "The flood-sea broke back in over the glass dunes!" },
      { :id => :shatter, :condition => proc { |battle, user, target, move, type| crack_proc.call(move, type) },
        :uses => 3, :to => shatter_to,
        :progress_message => "The glass cracked! ({1} more and it breaks apart)", :message => shatter_msg },
      { :id => :clash, :check => clash, :to => :BLEED, :uses => 2,
        :progress_message => "The glass is singing with both Imprints... ({1} more clash)",
        :message => "The beams met over the glass and the Imprints tore open! The Bleed swells over the dunes!" }
    ]
  }
  shared_damage = [
    { :types => [:ELECTRIC], :category => :damaging, :target => { :grounded => true }, :mult => 0.8,
      :message => "The glass wouldn't carry the current..." },
    { :flags => ["Sound"], :category => :damaging, :not_types => [:FIRE], :mult => 1.0,
      :message => "{2} set the glass ringing!" }
  ]
  {
    # ---- Stage 1: Hot Glass -------------------------------------------------------
    :name          => "Glass Dunes",
    :backdrop      => "field_glass_dunes",
    :family        => :telluric,
    :intro_message => "The dunes have fused into glass! Steam rises from every hollow!",
    :description   => "The glass the white fire made of the Bone Sands. Hot Glass holds the fire's heat for a long time: it feeds fire, flashes water to steam and bends light. Left alone it cools into Mirror Glass, where beams ricochet and reflections strike back. Both are brittle: quakes, heavy blows and loud sound crack them.",
    :notes         => ["Hot Glass (stage 1): Fire x1.2 (the white fire's heat stays in the glass). Ice x0.8. Nothing can be frozen. Fire types draw warmth from the glass (1/16 HP a turn); Turboblaze users' Fire moves x1.2 more; Steam Engine +1 Speed on entry.",
                       "Hot Glass: water flashes to steam on it - damaging Water moves may burn a grounded target (20%); Scald and Steam Eruption x1.3 and burn more often.",
                       "Hot Glass: light bends through the heat - Aurora Beam, Charge Beam, Dazzling Gleam, Flash Cannon, Luster Purge, Photon Geyser, Power Gem, Prismatic Laser, Signal Beam, Solar Beam x1.3. No hail can form; Sun lasts 2 turns longer.",
                       "Cooling: after 4 rounds without a damaging Fire move the glass cools into Mirror Glass (sunlight keeps it hot; rain cools it twice as fast). A damaging Fire move reheats Mirror Glass.",
                       "Mirror Glass (stage 2): the steam clears and every dune is a mirror. Beams and light (the moves above plus Psybeam, Ice Beam, Hyper Beam, Moongeist Beam, Meteor Beam and Lumina Crash) ricochet: x1.5, and they never miss.",
                       "Mirror Glass: Double Team and Minimize raise evasion one stage more (the mirror images multiply); Flash, Kinesis, Sand Attack and Smokescreen drop accuracy one stage more (the glare). Counter, Mirror Coat, Metal Burst and Comeuppance strike back x1.5.",
                       "Mirror Glass: Reflect, Light Screen and Aurora Veil last 3 turns longer, and Aurora Veil works without hail. Mirror Armor +1 Def, Prism Armor +1 Sp. Def on entry. Hail can fall on the cool glass.",
                       "Both: Mirror Shot x1.5 and always lowers accuracy. Glass doesn't conduct: Electric moves x0.8 against grounded targets, and Electric Terrain can't form. No sand left: Dig fails, Sand Tomb whips up glass grit (Rock type, x1.2), no sandstorm, nothing takes root.",
                       "Cracking: quakes and heavy blows (Earthquake, Bulldoze, Heavy Slam, High Horsepower, Rock Smash x2, Explosion...), damaging sound moves (the Choir tunes glass by singing to it; a loud enough voice breaks it) and, on Hot Glass, big Ice moves (thermal shock). Shards hit the user's grounded foes (1/16, Rock-scaled) and stay on the ground on their side.",
                       "Broken glass: a grounded Pokemon switching in on that side takes 1/16 (Rock-scaled; Heavy-Duty Boots protect). Rapid Spin, Mortal Spin, Defog and Tidy Up sweep it away. It's gone when the glass breaks or floods.",
                       "3 cracks break the glass apart: back to the Desert, or into the Flooded Dunes if it's raining. Each damaging Fire move anneals one crack; cooling doesn't mend them.",
                       "The sea returns: heavy rain, 2 Origin Pulses or 3 floods (Surf, Hydro Pump, Water Spout, Muddy Water...) -> Flooded Dunes.",
                       "Beam clash: in 2 rounds where opposing sides both land a great Water beam (Origin Pulse, Water Spout, Hydro Cannon, Hydro Pump, Steam Eruption) and a great Fire beam (Blue Flare, Fusion Flare, Blast Burn, Eruption, V-create, Overheat), the Imprints tear open -> the Bleed.",
                       "Telluric Seed: +2 Defense (a glass carapace), but -1 Sp. Def (light passes straight through)."],
    :nature_power  => :POWERGEM,
    :camouflage    => :ROCK,
    :secret_power  => 10,
    :type_mods     => { :FIRE => 1.2, :ICE => 0.8 },
    :type_messages => { :FIRE => "The heat locked in the glass flared up with {2}!",
                        :ICE  => "The ice hissed on the hot glass..." },
    :move_mods     => light.map { |m| [m, 1.3] }.to_h.merge(
                        :MIRRORSHOT => 1.5, :SCALD => 1.3, :STEAMERUPTION => 1.3, :ROCKSMASH => 2.0, :SANDTOMB => 1.2),
    :move_messages => { :POWERGEM      => "The hot glass bent {2} into a lance of light!",
                        :FLASHCANNON   => "The hot glass bent {2} into a lance of light!",
                        :DAZZLINGGLEAM => "The hot glass bent {2} into a lance of light!",
                        :SOLARBEAM     => "The hot glass bent {2} into a lance of light!",
                        :MIRRORSHOT    => "{1} flashed the glare of the glass straight into the foe's eyes!",
                        :SCALD         => "The water boiled on the hot glass!",
                        :ROCKSMASH     => "{1} smashed straight through the glass!" },
    :type_changes  => [
      { :moves => [:SANDTOMB], :to => :ROCK, :message => "{1} whipped up a whirl of glass grit!" }
    ],
    :effect_chance_mods => [
      { :moves => [:MIRRORSHOT], :set => 100 },
      { :moves => [:SCALD, :STEAMERUPTION], :mult => 1.5 }
    ],
    :damage_mods   => shared_damage + [
      { :types => [:FIRE], :category => :damaging, :user => { :abilities => [:TURBOBLAZE] }, :mult => 1.2,
        :message => "The glass rang with the white fire that made it!" }
    ],
    :added_effects => [
      { :types => [:WATER], :category => :damaging, :not_moves => [:SCALD, :STEAMERUPTION], :chance => 20,
        :status => :BURN, :target => { :grounded => true }, :message => "Boiling steam off the glass burned {1}!" }
    ],
    :move_fails    => [
      { :moves => [:DIG], :message => "There's no sand left to burrow into - {1} skidded off the glass!" }
    ],
    :status_immunity => [
      { :status => [:FROZEN], :message => "The heat in the glass kept {1} from freezing!" }
    ],
    :on_entry      => [
      { :battlers => { :abilities => [:STEAMENGINE] }, :stats => { :SPEED => 1 },
        :message => "{1} drew on the steam rising off the glass!" }
    ],
    :end_of_round  => [
      { :battlers => { :types => [:FIRE], :grounded => true }, :heal => 1/16r, :message => "{1} drew warmth from the hot glass." }
    ],
    :weather       => { :block => [:Hail, :Sandstorm],
                        :block_message => "Nothing but steam rises off the hot glass - no hail, no loose sand!",
                        :extend => { :Sun => 2 } },
    :terrain       => { :block => [:Grassy, :Electric],
                        :block_message => "Nothing takes root in glass, and glass won't carry a current!" },
    :hooks         => {
      :on_start     => proc { |battle, old_id|
        st = FieldEffects.state(battle)
        st[:sea_beam] = st[:fire_beam] = nil
        st[:heat] = cool_after
        st[:shards] = {}
      },
      :after_move   => after_move,
      :on_entry     => step_on,
      :end_of_round => cool
    },
    :transitions   => transitions_for.call(cracks_hot),
    :seed => { :item => :TELLURICSEED, :stats => { :DEFENSE => 2, :SPECIAL_DEFENSE => -1 },
               :message => "{1}'s {2} cased it in glass - hard against blows, but light passes straight through!" },
    :stages => {
      # ---- Stage 2: Mirror Glass ----------------------------------------------------
      2 => {
        :backdrop      => "field_glass_dunes_mirror",
        :intro_message => "The glass has cooled into a vast mirror! The whole sky shines in the dunes!",
        :description   => "Mirror Glass: the glass has cooled and the steam is gone. Beams ricochet, mirror images multiply, glare blinds and reflections strike back harder. Fire reheats it.",
        :nature_power  => :MIRRORSHOT,
        :secret_power  => 8,
        :type_mods     => {},
        :type_messages => {},
        :move_mods     => beams.map { |m| [m, 1.5] }.to_h.merge(:ROCKSMASH => 2.0, :SANDTOMB => 1.2),
        :move_messages => { :POWERGEM      => "{2} ricocheted from mirror to mirror!",
                            :FLASHCANNON   => "{2} ricocheted from mirror to mirror!",
                            :DAZZLINGGLEAM => "{2} ricocheted from mirror to mirror!",
                            :ICEBEAM       => "{2} ricocheted from mirror to mirror!",
                            :SOLARBEAM     => "{2} ricocheted from mirror to mirror!",
                            :PSYBEAM       => "{2} ricocheted from mirror to mirror!",
                            :MIRRORSHOT    => "{1} flashed the glare of the mirror straight into the foe's eyes!",
                            :ROCKSMASH     => "{1} smashed straight through the glass!" },
        :effect_chance_mods => [{ :moves => [:MIRRORSHOT], :set => 100 }],
        :damage_mods   => shared_damage,
        :accuracy_mods => [{ :moves => beams, :category => :damaging, :always_hit => true }],
        :fixed_damage_mods => [
          { :moves => strike_back, :mult => 1.5, :message => "The mirror glass threw {2} back even harder!" }
        ],
        # Evasion/accuracy stay at normal strength here (the extra +1/-1 was dropped: Gemini review 2026-11-21,
        # RNG cheese); the mirrors only comment on it.
        :move_stat_boosts => [],
        :added_effects => [],
        :status_immunity => [],
        :effect_durations => { :REFLECT     => [3, "The mirror glass caught the barrier and held it!"],
                               :LIGHTSCREEN => [3, "The mirror glass caught the barrier and held it!"],
                               :AURORAVEIL  => [3, "The mirror glass caught the aurora and held it!"] },
        :weather_as    => [{ :moves => [:AURORAVEIL], :as => :Hail }],
        :on_entry      => [
          { :battlers => { :abilities => [:MIRRORARMOR] }, :stats => { :DEFENSE => 1 },
            :message => "{1}'s armor caught the sheen of the mirror glass!" },
          { :battlers => { :abilities => [:PRISMARMOR] }, :stats => { :SPECIAL_DEFENSE => 1 },
            :message => "{1}'s armor caught the sheen of the mirror glass!" }
        ],
        :end_of_round  => [],
        :weather       => { :block => [:Sandstorm], :block_message => "There's no loose sand left to blow - only glass!" },
        :transitions   => transitions_for.call(cracks_cool)
      }
    }
  }
end).call)
