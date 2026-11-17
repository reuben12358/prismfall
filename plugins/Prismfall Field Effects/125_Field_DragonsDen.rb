#===============================================================================
# DRAGONS_DEN - Gym 18 (Dragon), Wyrmrest in Ashkaar, the Dragonfire Dominion.
# The final gym: a magma-lit lair of dragon bones, wyrm statues and a hoard.
# Dragons are armoured by their lair, fire runs in the floor, the hoard pays
# out. 4 Dragon attacks awaken the den -> stage 2 = Wyrmfire. 3 Water/Ice
# attacks cool it to a CAVE; 3 Fairy attacks tame the dragon (FAIRY_TALE).
# Family: Elemental.
#===============================================================================
FieldEffects.register(:DRAGONS_DEN, (lambda do
  bones = [:BONECLUB, :BONERUSH, :BONEMERANG, :SHADOWBONE]
  hoard = [:POWERGEM, :DIAMONDSTORM, :MAKEITRAIN, :PAYDAY]
  shared_transitions = [
    { :types => [:WATER, :ICE], :category => :damaging, :to => :CAVE, :uses => 3,
      :progress_message => "Steam hisses from the cooling magma... ({1} more)",
      :message => "The magma cooled to stone... The den falls cold and silent." },
    { :types => [:FAIRY], :category => :damaging, :to => :FAIRY_TALE, :uses => 3,
      :progress_message => "The dragon's eyes soften... ({1} more)",
      :message => "The dragon was tamed! The lair blooms into a storybook castle!" }
  ]
  {
    :name          => "Dragon's Den",
    :backdrop      => "field_dragons_den",
    :family        => :elemental,
    :intro_message => "Magma glows beneath a dragon's hoard... Ancient wyrms watch from the stone.",
    :description   => "Dragons are armoured by their lair, fire runs in the floor and the hoard pays out. Dragon attacks awaken the den; Water and Ice cool it; Fairy magic tames it.",
    :notes         => ["Dragon x1.5, Fire x1.3. Water and Ice x0.7 (the lair's heat). Dragon types are armoured by their lair (x0.83 damage taken).",
                       "Pay Day x2; Make It Rain, Dragon Breath x1.5 (Dragon Breath also hits as Fire); Smack Down and Thousand Arrows x2 (onto the magma, also Fire); bone moves, Lava Plume, Magma Storm, Earth Power, Power Gem, Diamond Storm x1.3.",
                       "Dragon Rage deals 140 HP (200 in Wyrmfire). Dragon Rush x1.25 accuracy.",
                       "Magma Armor: immune to Fire, +1 Def and Sp. Def on entry. Multiscale: Dragon weaknesses become neutral. Flash Fire starts lit; Dragon's Maw +1 Attack.",
                       "Dragon Dance also +1 Speed; Noble Roar lowers Atk and Sp. Atk one stage more.",
                       "The hoard protects its own: a Pokemon holding an Amulet Coin can't be given a status condition. Nothing can be frozen.",
                       "Stealth Rock picks up embers: an extra 1/16 Fire-scaled hit on entry.",
                       "Hail can't form; Sun +2 turns. Grassy Terrain burns away.",
                       "4 Dragon attacks awaken the den -> Wyrmfire (stage 2): Dragon x2, Fire x1.5, Water and Ice x0.5; Dragon attacks may burn (20%); Dragons bask in the wyrmfire (1/16 HP a turn).",
                       "3 Water or Ice attacks -> Cave. 3 Fairy attacks tame the dragon -> Fairy Tale.",
                       "Elemental Seed: +1 Attack, +1 Speed and Flash Fire."],
    :nature_power  => :DRAGONPULSE,
    :camouflage    => :DRAGON,
    :secret_power  => 10,
    :type_mods     => { :DRAGON => 1.5, :FIRE => 1.3, :WATER => 0.7, :ICE => 0.7 },
    :type_messages => { :DRAGON => "The ancient wyrms roared in answer to {1}!",
                        :FIRE   => "The magma-lit den blazed with {2}!",
                        :WATER  => "The lair's heat boiled the water away...",
                        :ICE    => "The lair's heat sapped the cold..." },
    :move_mods     => { :PAYDAY => 2.0, :SMACKDOWN => 2.0, :THOUSANDARROWS => 2.0, :MAKEITRAIN => 1.5,
                        :DRAGONBREATH => 1.5, :LAVAPLUME => 1.3, :MAGMASTORM => 1.3, :EARTHPOWER => 1.3,
                        :POWERGEM => 1.3, :DIAMONDSTORM => 1.3 }.merge(bones.map { |m| [m, 1.3] }.to_h),
    :move_messages => { :PAYDAY     => "The dragon's hoard spilled everywhere!",
                        :MAKEITRAIN => "The dragon's hoard glittered!",
                        :POWERGEM   => "The hoard's gems flared!",
                        :SMACKDOWN  => "The foe was slammed down onto the magma!",
                        :BONERUSH   => "The ancient dragon bones rattled!",
                        :BONEMERANG => "The ancient dragon bones rattled!",
                        :SHADOWBONE => "The ancient dragon bones rattled!",
                        :BONECLUB   => "The ancient dragon bones rattled!" },
    :extra_types   => [
      { :moves => [:DRAGONBREATH, :SMACKDOWN, :THOUSANDARROWS], :add => :FIRE, :message => "{1} breathed searing dragonfire!" }
    ],
    :damage_mods   => [
      { :category => :damaging, :target => { :types => [:DRAGON] }, :defense_mult => 1.2 }
    ],
    :effectiveness_mods => [
      { :attack => [:FIRE], :target => { :abilities => [:MAGMAARMOR] }, :set => 0.0 },
      { :attack => [:ICE, :DRAGON, :FAIRY], :defend => [:DRAGON], :target => { :abilities => [:MULTISCALE] }, :set => 1.0 }
    ],
    :accuracy_mods => [{ :moves => [:DRAGONRUSH], :mult => 1.25 }],
    :fixed_damage_mods => [{ :moves => [:DRAGONRAGE], :set => 140, :message => "The ancient wyrms lent {1} their rage!" }],
    :move_stat_boosts => [
      { :moves => [:DRAGONDANCE], :user_stats => { :SPEED => 1 }, :message => "The wyrm statues' eyes followed {1}'s dance!" },
      { :moves => [:NOBLEROAR], :target_stats => { :ATTACK => -1, :SPECIAL_ATTACK => -1 }, :message => "The roar echoed through the lair!" }
    ],
    :status_immunity => [
      { :status => [:FROZEN], :message => "Nothing can freeze in the dragon's lair!" },
      { :battlers => { :items => [:AMULETCOIN] }, :message => "{1}'s Amulet Coin glittered - the hoard protects its own!" }
    ],
    :on_entry      => [
      { :battlers => { :abilities => [:FLASHFIRE] }, :effects => [:flash_fire], :also_on_change => true },
      { :battlers => { :abilities => [:DRAGONSMAW] }, :stats => { :ATTACK => 1 }, :message => "{1}'s maw blazed with draconic power!" },
      { :battlers => { :abilities => [:MAGMAARMOR] }, :stats => { :DEFENSE => 1, :SPECIAL_DEFENSE => 1 },
        :message => "{1}'s armor drank in the lair's magma!" },
      { :battlers => { :not_items => [:HEAVYDUTYBOOTS],
                       :condition => proc { |battle, b| b.pbOwnSide.effects[PBEffects::StealthRock] } },
        :damage => 1/16r, :damage_type => :FIRE, :message => "The stones were red-hot with embers as they struck {1}!" }
    ],
    :weather       => { :block => [:Hail], :block_message => "The dragonfire melted the hail before it fell!",
                        :extend => { :Sun => 2 } },
    :terrain       => { :block => [:Grassy], :block_message => "The undergrowth burned away in the dragonfire!" },
    :transitions   => shared_transitions + [
      { :types => [:DRAGON], :category => :damaging, :stage => 2, :uses => 4,
        :progress_message => "The wyrm statues' eyes begin to glow... ({1} more)",
        :message => "The den has awoken! Wyrmfire surges through the lair!" }
    ],
    :seed => { :item => :ELEMENTALSEED, :stats => { :ATTACK => 1, :SPEED => 1 }, :effects => [:flash_fire],
               :message => "{1}'s {2} kindled dragonfire within it!" },
    :stages => {
      2 => {
        :backdrop      => "field_dragons_den_wyrmfire",
        :intro_message => "Wyrmfire surges through the lair! The den is awake!",
        :description   => "Awakened: Dragon x2, Fire x1.5, Ice halved. Dragon attacks spit wyrmfire; dragons bask in it.",
        :type_mods     => { :DRAGON => 2.0, :FIRE => 1.5, :WATER => 0.5, :ICE => 0.5 },
        :type_messages => { :DRAGON => "The awakened wyrms roared as one with {1}!",
                            :FIRE   => "Wyrmfire engulfed {2}!",
                            :WATER  => "The wyrmfire boiled the water away...",
                            :ICE    => "The wyrmfire melted the ice away..." },
        :fixed_damage_mods => [{ :moves => [:DRAGONRAGE], :set => 200,
                                 :message => "The awakened wyrms poured their fury into {1}!" }],
        :added_effects => [
          { :types => [:DRAGON], :category => :damaging, :chance => 20, :status => :BURN,
            :message => "Wyrmfire licked over {1}!" }
        ],
        :end_of_round  => [
          { :battlers => { :types => [:DRAGON] }, :heal => 1/16r, :message => "{1} basked in the wyrmfire." }
        ],
        :transitions   => shared_transitions
      }
    }
  }
end).call)
