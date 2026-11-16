#===============================================================================
# VOLCANIC - Gym 7 (Fire), Cindervault. A caldera floor of flowing magma.
#===============================================================================
FieldEffects.register(:VOLCANIC, {
  :name          => "Volcanic Field",
  :backdrop      => "field_volcanic",
  :intro_message => "Magma churns across the battlefield!",
  :description   => "Fire rages and rocks burn; the grounded are scorched. Water quenches it into ash.",
  :nature_power  => :LAVAPLUME,
  :camouflage    => :FIRE,
  :secret_power  => 10,
  :type_mods     => { :FIRE => 1.5, :ICE => 0.5 },
  :type_messages => { :FIRE => "The magma roared!",
                      :ICE  => "The ice melted in the heat..." },
  :move_mods     => { :LAVAPLUME => 1.5, :MAGMASTORM => 1.3, :FLAMEBURST => 1.5, :FIRESPIN => 1.5,
                      :EARTHPOWER => 1.3, :SCALD => 1.3, :STEAMERUPTION => 1.3, :SMOG => 1.5,
                      :CLEARSMOG => 1.5 },
  :move_messages => { :LAVAPLUME  => "The lava surged!",
                      :EARTHPOWER => "Magma erupted from below!",
                      :SCALD      => "The magma brought the water to a boil!" },
  :damage_mods   => [
    { :types => [:FIRE], :user => { :abilities => [:BLAZE] }, :mult => 1.5 }
  ],
  :extra_types   => [
    { :types => [:ROCK], :category => :damaging, :add => :FIRE,
      :message => "The rocks were superheated by the magma!" }
  ],
  :accuracy_mods => [{ :moves => [:WILLOWISP], :always_hit => true }],
  :added_effects => [
    { :types => [:GROUND], :category => :damaging, :chance => 20, :status => :BURN,
      :target => { :grounded => true }, :message => "{1} was seared by the molten earth!" }
  ],
  :move_stat_boosts => [
    { :moves => [:SMOKESCREEN], :target_stats => { :ACCURACY => -1 },
      :message => "The volcanic smoke thickened!" }
  ],
  :on_entry      => [
    { :battlers => { :abilities => [:FLASHFIRE] }, :effects => [:flash_fire], :also_on_change => true },
    { :battlers => { :abilities => [:MAGMAARMOR] }, :stats => { :DEFENSE => 1 },
      :message => "{1}'s armor hardened in the magma!" }
  ],
  :end_of_round  => [
    { :battlers => { :grounded => true, :not_types => [:FIRE],
                     :not_abilities => [:FLASHFIRE, :MAGMAARMOR, :WATERVEIL, :HEATPROOF, :WELLBAKEDBODY] },
      :damage => 1/16r, :damage_type => :FIRE, :message => "{1} was scorched by the magma!" },
    { :battlers => { :status => [:FROZEN] }, :cure_status => true },
    { :battlers => { :abilities => [:MAGMAARMOR] }, :heal => 1/16r, :message => "{1} basked in the magma." }
  ],
  :weather       => { :block => [:Hail], :block_message => "The heat melted the hail before it fell!",
                      :extend => { :Sun => 3 } },
  :terrain       => { :block => [:Grassy, :Misty],
                      :block_message => "The terrain burned away in the volcanic heat!" },
  :transitions   => [
    { :moves => [:SURF, :MUDDYWATER, :WATERSPOUT, :HYDROPUMP, :WATERPLEDGE, :SPARKLINGARIA, :SOAK],
      :to => :ASHEN_WASTE, :uses => 2,
      :progress_message => "Steam hisses from the cooling magma... ({1} more)",
      :message => "The water quenched the magma! Ash settles over the battlefield." },
    { :weather => [:Rain, :HeavyRain], :to => :ASHEN_WASTE,
      :message => "The rain cooled the magma into ash!" }
  ],
  :seed => { :item => :ELEMENTALSEED, :status => :BURN,
             :stats => { :ATTACK => 1, :SPECIAL_ATTACK => 1, :SPEED => 1 },
             :message => "{1}'s {2} ignited, searing it with volcanic power!" }
})
