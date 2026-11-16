#===============================================================================
# WATER_SURFACE - Gym 3 (Water), Ebbmouth. Open water; Dive goes Underwater.
#===============================================================================
FieldEffects.register(:WATER_SURFACE, {
  :name          => "Water Surface",
  :backdrop      => "field_water_surface",
  :intro_message => "The battle is taking place on the open water!",
  :description   => "Water surges, fire fizzles, electricity spreads; grounded non-Water Pokémon wade slowly.",
  :nature_power  => :WHIRLPOOL,
  :camouflage    => :WATER,
  :secret_power  => 5,
  :type_mods     => { :WATER => 1.5, :FIRE => 0.5 },
  :type_messages => { :WATER => "The waves amplified the attack!",
                      :FIRE  => "The water doused the flames..." },
  :move_mods     => { :WHIRLPOOL => 2.0, :DIVE => 1.3, :MUDDYWATER => 1.2, :WATERPLEDGE => 1.5,
                      :SURGINGSTRIKES => 1.2 },
  :move_messages => { :WHIRLPOOL => "The whirlpool grew into a maelstrom!" },
  :damage_mods   => [
    { :types => [:ELECTRIC], :target => { :grounded => true }, :mult => 1.5,
      :message => "The current raced across the water!" },
    { :types => [:WATER], :user => { :abilities => [:TORRENT] }, :mult => 1.5 }
  ],
  :accuracy_mods => [{ :moves => [:WHIRLPOOL], :mult => 1.25 }],
  :move_fails    => [
    { :moves => [:EARTHQUAKE, :MAGNITUDE, :FISSURE, :BULLDOZE, :DIG, :SPIKES, :TOXICSPIKES,
                 :STEALTHROCK, :STOMPINGTANTRUM],
      :message => "{2} sank uselessly beneath the waves!" }
  ],
  :added_effects => [
    { :types => [:WATER], :category => :damaging, :chance => 20, :stats => { :SPEED => -1 },
      :target => { :grounded => true, :not_types => [:WATER] },
      :message => "{1} was swept up by the current!" }
  ],
  :speed_mods    => [
    { :battlers => { :grounded => true, :not_types => [:WATER], :not_abilities => [:SWIFTSWIM] },
      :mult => 0.75 },
    { :battlers => { :abilities => [:SWIFTSWIM] }, :mult => 1.5 }
  ],
  :on_entry      => [
    { :battlers => { :abilities => [:STEAMENGINE, :WATERCOMPACTION] }, :stats => { :DEFENSE => 1 },
      :message => "{1} drew strength from the water!" }
  ],
  :end_of_round  => [
    { :battlers => { :grounded => true, :status => [:BURN] }, :cure_status => true,
      :message => "The cool water soothed {1}'s burn!" },
    { :battlers => { :abilities => [:HYDRATION] }, :cure_status => true },
    { :battlers => { :abilities => [:WATERABSORB, :DRYSKIN] }, :heal => 1/16r,
      :message => "{1} soaked up the spray." }
  ],
  :weather       => { :extend => { :Rain => 3 } },
  :terrain       => { :block => [:Grassy], :block_message => "Nothing can take root on open water!" },
  :transitions   => [
    { :moves => [:DIVE], :to => :UNDERWATER, :message => "The battle plunged beneath the waves!" },
    { :moves => [:BLIZZARD, :SHEERCOLD, :GLACIATE, :ICEBEAM, :FREEZEDRY], :to => :FROZEN_LAKE, :uses => 3,
      :progress_message => "Ice spreads across the water... ({1} more)",
      :message => "The water froze solid!" }
  ],
  :seed => { :item => :ELEMENTALSEED, :stats => { :SPEED => 1 }, :effects => [:aqua_ring],
             :message => "{1}'s {2} wrapped it in a veil of seawater!" }
})
