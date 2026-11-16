#===============================================================================
# DRAGONS_DEN - Gym 18 (Dragon), Wyrmrest in Ashkaar, the Dragonfire Dominion.
# The final gym: a magma-lit lair of dragon bones, wyrm statues and a hoard.
# Stage 1 = Dragon's Den. 4 Dragon attacks awaken it -> stage 2 = Wyrmfire
# (Dragon x2, scorching floor). 3 Water/Ice attacks cool it to a CAVE.
#===============================================================================
FieldEffects.register(:DRAGONS_DEN, {
  :name          => "Dragon's Den",
  :backdrop      => "field_dragons_den",
  :intro_message => "Magma glows beneath a dragon's hoard... Ancient wyrms watch from the stone.",
  :description   => "Dragon and Fire are empowered, Ice melts. Dragon attacks awaken the den; Water and Ice cool it to a cave.",
  :notes         => ["Dragon x1.5, Fire x1.3, Ice x0.8. Pay Day x2; Make It Rain, Dragon Breath x1.5; bone moves x1.3.",
                     "Dragon Breath also hits as Fire. Flash Fire activates; Dragon's Maw gives +1 Attack.",
                     "Hail can't form; Sun lasts longer. Grassy Terrain burns away.",
                     "4 Dragon attacks awaken the den: Dragon x2, Fire x1.5, Ice x0.5, and the floor scorches.",
                     "3 Water or Ice attacks cool it into a Cave."],
  :nature_power  => :DRAGONPULSE,
  :camouflage    => :DRAGON,
  :secret_power  => 10,
  :type_mods     => { :DRAGON => 1.5, :FIRE => 1.3, :ICE => 0.8 },
  :type_messages => { :DRAGON => "The ancient wyrms roared in answer!",
                      :FIRE   => "The magma-lit den blazed!",
                      :ICE    => "The den's heat sapped the cold..." },
  :move_mods     => { :PAYDAY => 2.0, :MAKEITRAIN => 1.5, :BONECLUB => 1.3, :BONERUSH => 1.3,
                      :BONEMERANG => 1.3, :SHADOWBONE => 1.3, :LAVAPLUME => 1.3, :MAGMASTORM => 1.3,
                      :DRAGONBREATH => 1.5 },
  :move_messages => { :PAYDAY     => "The dragon's hoard spilled everywhere!",
                      :MAKEITRAIN => "The dragon's hoard glittered!",
                      :BONERUSH   => "The ancient dragon bones rattled!",
                      :BONEMERANG => "The ancient dragon bones rattled!",
                      :SHADOWBONE => "The ancient dragon bones rattled!",
                      :BONECLUB   => "The ancient dragon bones rattled!" },
  :extra_types   => [
    { :moves => [:DRAGONBREATH], :add => :FIRE, :message => "{1} breathed searing dragonfire!" }
  ],
  :accuracy_mods => [{ :moves => [:DRAGONRUSH], :mult => 1.25 }],
  :on_entry      => [
    { :battlers => { :abilities => [:FLASHFIRE] }, :effects => [:flash_fire], :also_on_change => true },
    { :battlers => { :abilities => [:DRAGONSMAW] }, :stats => { :ATTACK => 1 },
      :message => "{1}'s maw blazed with draconic power!" }
  ],
  :end_of_round  => [
    { :battlers => { :status => [:FROZEN] }, :cure_status => true, :message => "The den's heat thawed {1} out!" }
  ],
  :weather       => { :block => [:Hail], :block_message => "The dragonfire melted the hail before it fell!",
                      :extend => { :Sun => 2 } },
  :terrain       => { :block => [:Grassy], :block_message => "The undergrowth burned away in the dragonfire!" },
  :transitions   => [
    { :types => [:WATER, :ICE], :category => :damaging, :to => :CAVE, :uses => 3,
      :progress_message => "Steam hisses from the cooling magma... ({1} more)",
      :message => "The magma cooled to stone... The den falls cold and silent." },
    { :types => [:DRAGON], :category => :damaging, :stage => 2, :uses => 4,
      :progress_message => "The wyrm statues' eyes begin to glow... ({1} more)",
      :message => "The den has awoken! Wyrmfire surges through the lair!" }
  ],
  :seed => { :item => :ELEMENTALSEED, :stats => { :ATTACK => 1, :SPEED => 1 }, :effects => [:flash_fire],
             :message => "{1}'s {2} kindled dragonfire within it!" },
  :stages => {
    2 => {
      :intro_message => "Wyrmfire surges through the lair! The den is awake!",
      :description   => "Awakened: Dragon x2, Fire x1.5, Ice halved; the scorching floor burns grounded non-Dragons.",
      :type_mods     => { :DRAGON => 2.0, :FIRE => 1.5, :ICE => 0.5 },
      :type_messages => { :DRAGON => "The awakened wyrms roared as one!",
                          :FIRE   => "Wyrmfire engulfed the attack!",
                          :ICE    => "The wyrmfire melted the ice away..." },
      :end_of_round  => [
        { :battlers => { :grounded => true, :not_types => [:DRAGON, :FIRE],
                         :not_abilities => [:FLASHFIRE, :MAGMAARMOR, :WATERVEIL, :HEATPROOF, :WELLBAKEDBODY] },
          :damage => 1/16r, :damage_type => :FIRE, :message => "{1} was scorched by the wyrmfire!" },
        { :battlers => { :status => [:FROZEN] }, :cure_status => true, :message => "The den's heat thawed {1} out!" }
      ],
      :transitions   => [
        { :types => [:WATER, :ICE], :category => :damaging, :to => :CAVE, :uses => 3,
          :progress_message => "Steam hisses from the cooling magma... ({1} more)",
          :message => "The wyrmfire was quenched! The den falls cold and silent." }
      ]
    }
  }
})
