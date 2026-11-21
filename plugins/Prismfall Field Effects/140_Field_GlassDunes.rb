#===============================================================================
# GLASS_DUNES - (new, SPINE Revisions 10/18) Steam-glass: dunes that white fire
# has fused into black-green glass, waves of the flood set mid-curl, hollows of
# boiling water steaming between them. What the Bone Sands become under searing
# heat (DESERT) and what Reshiram's Blue Flare makes of Kyogre's flood-sea
# (FLOODED_DUNES) - the climax field of map 926, the Glass Dunes. The Fire and
# Water Imprints that made it are both still locked inside it.
#   * The heat in the glass feeds fire and turns any water that touches it into
#     scalding steam (Water attacks can burn); nothing can freeze.
#   * The glass refracts light beams and throws reflections back harder.
#   * It's brittle: quakes and the thermal shock of big Ice moves shatter the
#     crust and spray shards at the user's foes; 3 shatters break it apart (to
#     the DESERT, or back into the FLOODED_DUNES if it is raining). Fire
#     anneals the cracks.
#   * The sea can drown it again (heavy rain, 2 Origin Pulses, 3 floods).
#   * Beam clash: in two rounds where a great Water beam and a great Fire beam
#     from opposing sides both land, the Imprints tear open into the BLEED.
# Family: Telluric.
#===============================================================================
FieldEffects.register(:GLASS_DUNES, (lambda do
  quakes  = [:EARTHQUAKE, :MAGNITUDE, :BULLDOZE, :FISSURE, :PRECIPICEBLADES, :HEADLONGRUSH, :STOMPINGTANTRUM,
             :HIGHHORSEPOWER, :HEAVYSLAM, :ROCKSMASH]
  chill   = [:BLIZZARD, :ICEBEAM, :SHEERCOLD, :GLACIATE, :FREEZEDRY, :ICICLECRASH, :AVALANCHE, :ICEHAMMER,
             :MOUNTAINGALE, :GLACIALLANCE, :FREEZINGGLARE]
  shatter = quakes + chill
  floods  = [:SURF, :MUDDYWATER, :HYDROPUMP, :WATERSPOUT, :WAVECRASH, :WATERPLEDGE, :HYDROCANNON]
  beams   = [:AURORABEAM, :CHARGEBEAM, :DAZZLINGGLEAM, :FLASHCANNON, :LUSTERPURGE, :MIRRORSHOT, :PHOTONGEYSER,
             :POWERGEM, :PRISMATICLASER, :SIGNALBEAM, :SOLARBEAM]
  sea_beam  = [:ORIGINPULSE, :WATERSPOUT, :HYDROCANNON, :HYDROPUMP, :STEAMERUPTION]
  fire_beam = [:BLUEFLARE, :FUSIONFLARE, :BLASTBURN, :ERUPTION, :VCREATE, :OVERHEAT]
  on_field = lambda { |battle| FieldEffects.current(battle) == :GLASS_DUNES }
  after_move = proc { |battle, user, targets, move, num_hits|
    next if user.lastMoveFailed || !move.damagingMove? || targets.empty?
    if shatter.include?(move.id)
      text = (chill.include?(move.id)) ? "The cold cracked the hot glass! Shards flew up around {1}'s foes!" :
                                         "{1} shattered the glass crust! Shards flew up around its foes!"
      battle.pbDisplay(FieldEffects.format(text, user.pbThis))
      battle.allOtherSideBattlers(user.index).each do |b|
        next if b.fainted? || b.airborne? || b.hasActiveItem?(:HEAVYDUTYBOOTS)
        FieldEffects.apply_battler_effect(battle, b, { :damage => 1/16r, :damage_type => :ROCK,
                                                       :message => "Flying glass caught {1}!" })
        b.pbFaint if b.fainted?
      end
    end
    next if !on_field.call(battle)
    # Beam clash bookkeeping: which side landed a great Water / Fire beam this round
    side = user.index & 1
    st = FieldEffects.state(battle)
    turn = battle.turnCount
    st[:sea_beam]  = [turn, side] if sea_beam.include?(move.id)
    st[:fire_beam] = [turn, side] if fire_beam.include?(move.id)
  }
  clash = proc { |battle|
    st = FieldEffects.state(battle)
    w, f = st[:sea_beam], st[:fire_beam]
    next false if !w || !f || w[0] != battle.turnCount || f[0] != battle.turnCount || w[1] == f[1]
    st[:sea_beam] = st[:fire_beam] = nil
    battle.pbDisplay(FieldEffects.format("The beams locked over the glass! Both Imprints are ringing in it!"))
    true
  }
  {
    :name          => "Glass Dunes",
    :backdrop      => "field_glass_dunes",
    :family        => :telluric,
    :intro_message => "The dunes have fused into glass! Steam rises from every hollow!",
    :description   => "Steam-glass over the Bone Sands: the heat in the glass feeds fire and boils any water into scalding steam, light refracts, and the brittle crust shatters under quakes and sudden cold. Both Imprints that made it are still inside.",
    :notes         => ["Fire x1.2 (the white fire's heat is still in the glass). Ice x0.8 - but big Ice moves crack it (below). Nothing can be frozen.",
                       "Water boils on the hot glass: damaging Water moves may burn a grounded target (20%). Scald and Steam Eruption x1.3 and burn more often.",
                       "Refraction: Aurora Beam, Charge Beam, Dazzling Gleam, Flash Cannon, Luster Purge, Mirror Shot, Photon Geyser, Power Gem, Prismatic Laser, Signal Beam, Solar Beam x1.3. Mirror Shot x1.5 and always lowers accuracy.",
                       "Mirror-dark glass: Mirror Coat strikes back x1.25; Reflect and Light Screen last 3 turns longer. Mirror Armor +1 Def, Prism Armor +1 Sp. Def on entry.",
                       "Shattering: quakes, heavy stomps, Rock Smash (x2) and big Ice moves (thermal shock) crack the crust - shards hit each grounded foe of the user (1/16, Rock-scaled; Heavy-Duty Boots protect). 3 shatters break the glass apart: back to the Desert, or into the Flooded Dunes if it's raining. Each damaging Fire move anneals one crack.",
                       "No sand left: Dig fails, Sand Tomb whips up glass grit (Rock type, x1.2), sandstorms and hail can't form, Grassy Terrain can't take root. Sun lasts 2 turns longer.",
                       "Fire types draw warmth from the glass (1/16 HP a turn). Turboblaze users' Fire moves x1.2 more (the glass rings with the white fire that made it). Steam Engine +1 Speed on entry.",
                       "The sea returns: heavy rain, 2 Origin Pulses or 3 floods (Surf, Hydro Pump, Water Spout, Muddy Water...) -> Flooded Dunes.",
                       "Beam clash: in 2 rounds where opposing sides both land a great Water beam (Origin Pulse, Water Spout, Hydro Cannon, Hydro Pump, Steam Eruption) and a great Fire beam (Blue Flare, Fusion Flare, Blast Burn, Eruption, V-create, Overheat), the Imprints tear open -> the Bleed.",
                       "Telluric Seed: +2 Defense (a glass carapace), but -1 Sp. Def (light passes straight through)."],
    :nature_power  => :POWERGEM,
    :camouflage    => :ROCK,
    :secret_power  => 10,
    :type_mods     => { :FIRE => 1.2, :ICE => 0.8 },
    :type_messages => { :FIRE => "The heat locked in the glass flared up with {2}!",
                        :ICE  => "The ice hissed on the hot glass..." },
    :move_mods     => beams.map { |m| [m, 1.3] }.to_h.merge(
                        :MIRRORSHOT => 1.5, :SCALD => 1.3, :STEAMERUPTION => 1.3, :ROCKSMASH => 2.0, :SANDTOMB => 1.2),
    :move_messages => { :POWERGEM      => "The glass dunes caught {2} and refracted it into a lance of light!",
                        :FLASHCANNON   => "The glass dunes caught {2} and refracted it into a lance of light!",
                        :DAZZLINGGLEAM => "The glass dunes caught {2} and refracted it into a lance of light!",
                        :SOLARBEAM     => "The glass dunes caught {2} and refracted it into a lance of light!",
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
    :damage_mods   => [
      { :types => [:FIRE], :category => :damaging, :user => { :abilities => [:TURBOBLAZE] }, :mult => 1.2,
        :message => "The glass rang with the white fire that made it!" }
    ],
    :fixed_damage_mods => [
      { :moves => [:MIRRORCOAT], :mult => 1.25, :message => "The mirror-dark glass threw {2} back even harder!" }
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
    :effect_durations => { :REFLECT     => [3, "The glass dunes caught the barrier and held it!"],
                           :LIGHTSCREEN => [3, "The glass dunes caught the barrier and held it!"] },
    :on_entry      => [
      { :battlers => { :abilities => [:STEAMENGINE] }, :stats => { :SPEED => 1 },
        :message => "{1} drew on the steam rising off the glass!" },
      { :battlers => { :abilities => [:MIRRORARMOR] }, :stats => { :DEFENSE => 1 },
        :message => "{1}'s armor caught the sheen of the glass!" },
      { :battlers => { :abilities => [:PRISMARMOR] }, :stats => { :SPECIAL_DEFENSE => 1 },
        :message => "{1}'s armor caught the sheen of the glass!" }
    ],
    :end_of_round  => [
      { :battlers => { :types => [:FIRE], :grounded => true }, :heal => 1/16r, :message => "{1} drew warmth from the hot glass." }
    ],
    :weather       => { :block => [:Hail, :Sandstorm],
                        :block_message => "Nothing but steam rises off the hot glass - no hail, no loose sand!",
                        :extend => { :Sun => 2 } },
    :terrain       => { :block => [:Grassy], :block_message => "Nothing can take root in glass!" },
    :hooks         => {
      :on_start   => proc { |battle, old_id| st = FieldEffects.state(battle); st[:sea_beam] = st[:fire_beam] = nil },
      :after_move => after_move
    },
    :transitions   => [
      { :weather => [:HeavyRain], :to => :FLOODED_DUNES,
        :message => "The flood-sea broke back in over the glass dunes!" },
      { :id => :pulse, :moves => [:ORIGINPULSE], :to => :FLOODED_DUNES, :uses => 2,
        :progress_message => "The sea is rising against the glass... ({1} more)",
        :message => "The flood-sea broke back in over the glass dunes!" },
      { :id => :reflood, :moves => floods, :to => :FLOODED_DUNES, :uses => 3, :even_if_failed => true,
        :progress_message => "Water is pooling between the glass dunes... ({1} more)",
        :message => "The flood-sea broke back in over the glass dunes!" },
      { :id => :shatter, :moves => shatter, :category => :damaging, :uses => 3,
        :to => proc { |battle| [:Rain, :HeavyRain].include?(battle.pbWeather) ? :FLOODED_DUNES : :DESERT },
        :progress_message => "Cracks are spreading through the glass... ({1} more)",
        :message => "The glass dunes broke apart!" },
      { :types => [:FIRE], :category => :damaging, :rewind => :shatter,
        :message => "The heat annealed the cracks in the glass!" },
      { :id => :clash, :check => clash, :to => :BLEED, :uses => 2,
        :progress_message => "The glass is singing with both Imprints... ({1} more clash)",
        :message => "The beams met over the glass and the Imprints tore open! The Bleed swells over the dunes!" }
    ],
    :seed => { :item => :TELLURICSEED, :stats => { :DEFENSE => 2, :SPECIAL_DEFENSE => -1 },
               :message => "{1}'s {2} cased it in glass - hard against blows, but light passes straight through!" }
  }
end).call)
