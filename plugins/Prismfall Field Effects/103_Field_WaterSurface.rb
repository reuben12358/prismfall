#===============================================================================
# WATER_SURFACE - Gym 3 (Water), Ebbmouth in Isenmar. Open water and two-way
# currents. Swimmers ride the waves, current races across the surface, flames
# hiss into steam, and the ground is far below. Dive (or Gravity) takes the
# battle Underwater; deep cold freezes it (FROZEN_LAKE); sludge taints it
# (CORROSIVE_MIRE). Family: Elemental.
#===============================================================================
FieldEffects.register(:WATER_SURFACE, (lambda do
  big_ice = [:BLIZZARD, :SHEERCOLD, :GLACIATE, :ICEBEAM, :FREEZEDRY]
  {
    :name          => "Water Surface",
    :backdrop      => "field_water_surface",
    :family        => :elemental,
    :intro_message => "The battle is taking place on the open water!",
    :description   => "Swimmers ride the currents, electricity races across the surface and flames hiss into steam. Nothing touches the ground.",
    :notes         => ["Water x1.5. Electric x1.5 against grounded targets. Fire x0.5 against grounded targets (it hisses into steam).",
                       "Torrent, Swift Swim, Hydration, Rain Dish and Dry Skin act as if it were raining.",
                       "Whirlpool x2 (and more accurate); Water Pledge x1.5; Dive, Wave Crash, Brine, Aqua Step, Flip Turn, Anchor Shot x1.3; Muddy Water, Surging Strikes x1.2.",
                       "Ground moves and hazards sink: Earthquake, Magnitude, Bulldoze, Dig, Fissure, Stomping Tantrum, Spikes, Toxic Spikes, Stealth Rock fail.",
                       "Grounded non-Water Pokemon wade at x0.75 Speed. Water attacks may sweep grounded non-Water targets along (Speed -1).",
                       "The cool water soothes grounded Pokemon's burns. Water Absorb sips 1/16 HP a turn. Water Compaction +1 Def, Propeller Tail +1 Speed on entry.",
                       "Rain lasts 3 turns longer, Misty Terrain 2 turns longer. Grassy Terrain can't take root.",
                       "Dive (on the turn it strikes) or Gravity -> Underwater. 3 big ice moves -> Frozen Lake. 2 Sludge Waves (or Toxic + Sludge Wave) -> Corrosive Mire.",
                       "Elemental Seed: +1 Speed and Aqua Ring."],
    :nature_power  => :WHIRLPOOL,
    :camouflage    => :WATER,
    :secret_power  => 5,
    :activate_abilities => [:TORRENT, :SWIFTSWIM, :HYDRATION, :RAINDISH, :DRYSKIN],
    :type_mods     => { :WATER => 1.5 },
    :type_messages => { :WATER => "{1} rode the waves into the attack!" },
    :move_mods     => { :WHIRLPOOL => 2.0, :WATERPLEDGE => 1.5, :DIVE => 1.3, :WAVECRASH => 1.3, :BRINE => 1.3,
                        :AQUASTEP => 1.3, :FLIPTURN => 1.3, :ANCHORSHOT => 1.3, :MUDDYWATER => 1.2,
                        :SURGINGSTRIKES => 1.2 },
    :move_messages => { :WHIRLPOOL  => "The whirlpool grew into a maelstrom!",
                        :WAVECRASH  => "{1} rode a breaking wave into the foe!",
                        :AQUASTEP   => "{1} danced across the crests of the waves!",
                        :DIVE       => "{1} burst up from the deep!" },
    :damage_mods   => [
      { :types => [:ELECTRIC], :category => :damaging, :target => { :grounded => true }, :mult => 1.5,
        :message => "The current raced across the water!" },
      { :types => [:FIRE], :category => :damaging, :target => { :grounded => true }, :mult => 0.5,
        :message => "The flames hissed into steam on the waves..." }
    ],
    :accuracy_mods => [{ :moves => [:WHIRLPOOL], :mult => 1.25 }],
    :move_fails    => [
      { :moves => [:EARTHQUAKE, :MAGNITUDE, :FISSURE, :BULLDOZE, :DIG, :STOMPINGTANTRUM, :SPIKES, :TOXICSPIKES,
                   :STEALTHROCK],
        :message => "{2} sank beneath the waves without a trace!" }
    ],
    :added_effects => [
      { :types => [:WATER], :category => :damaging, :chance => 20, :stats => { :SPEED => -1 },
        :target => { :grounded => true, :not_types => [:WATER] },
        :message => "{1} was swept along by the current!" }
    ],
    :speed_mods    => [
      { :battlers => { :grounded => true, :not_types => [:WATER], :not_abilities => [:SWIFTSWIM, :SURGESURFER] },
        :mult => 0.75 }
    ],
    :on_entry      => [
      { :battlers => { :abilities => [:WATERCOMPACTION] }, :stats => { :DEFENSE => 1 },
        :message => "{1} packed itself tight against the swell!" },
      { :battlers => { :abilities => [:PROPELLERTAIL] }, :stats => { :SPEED => 1 },
        :message => "{1} churned through the water!" }
    ],
    :end_of_round  => [
      { :battlers => { :grounded => true, :status => [:BURN] }, :cure_status => true,
        :message => "The cool water soothed {1}'s burn!" },
      { :battlers => { :abilities => [:WATERABSORB] }, :heal => 1/16r, :message => "{1} soaked up the spray." }
    ],
    :weather       => { :extend => { :Rain => 3 } },
    :terrain       => { :block => [:Grassy], :block_message => "Nothing can take root on open water!",
                        :extend => { :Misty => 2 } },
    :transitions   => [
      # Dive takes the battle down on the turn it strikes (Reborn), so that hit is the transform strike (x1.3) and one
      # Dive is one change. Surfacing again is not a strike (104_Field_Underwater.rb): the bonus is one-way, no Dive loop.
      { :moves => [:DIVE], :strike_turn => true, :to => :UNDERWATER, :message => "The battle plunged beneath the waves!" },
      { :moves => [:GRAVITY], :to => :UNDERWATER, :message => "Gravity dragged the whole battle under the surface!" },
      { :moves => big_ice, :category => :damaging, :to => :FROZEN_LAKE, :uses => 3,
        :progress_message => "Ice is spreading across the water... ({1} more)",
        :message => "The water froze solid! The battle is on the ice now!" },
      { :moves => [:SLUDGEWAVE, :TOXIC, :ACIDSPRAY], :to => :CORROSIVE_MIRE, :uses => 2, :even_if_failed => true,
        :progress_message => "Sludge is spreading through the water... ({1} more)",
        :message => "The water turned to bubbling toxic murk!" }
    ],
    :seed => { :item => :ELEMENTALSEED, :stats => { :SPEED => 1 }, :effects => [:aqua_ring],
               :message => "{1}'s {2} wrapped it in a veil of seawater!" }
  }
end).call)
