#===============================================================================
# FAIRY_TALE - Gym 17 (Fairy), Gloaming, the heart of Elowen's fairy forest.
# A storybook castle glade of knights, dragons and fairy magic (Reborn homage).
# Rouse the dragon beneath the castle (3 Dragon attacks) -> DRAGONS_DEN.
#===============================================================================
# (Helpers live inside the lambda: plugin files share TOPLEVEL_BINDING.)
FieldEffects.register(:FAIRY_TALE, (lambda do
  prismfall_fairytale_blades = [
    :SACREDSWORD, :SECRETSWORD, :SMARTSTRIKE, :BEHEMOTHBLADE, :LEAFBLADE, :NIGHTSLASH, :PSYCHOCUT,
    :SOLARBLADE, :XSCISSOR, :SLASH, :CUT, :FURYCUTTER, :AIRSLASH, :RAZORSHELL, :CROSSPOISON, :STONEAXE,
    :CEASELESSEDGE, :AQUACUTTER, :BITTERBLADE, :KOWTOWCLEAVE, :PSYBLADE, :MIGHTYCLEAVE, :TACHYONCUTTER
  ]

  {
    :name          => "Fairy Tale",
    :backdrop      => "field_fairy_tale",
    :intro_message => "Once upon a time, in a castle deep in the forest... the story begins!",
    :description   => "Fairies, knights (Steel, blades) and dragons are empowered. Armor and magic shine. Rouse the dragon to burn it.",
    :notes         => ["Fairy x1.5, Dragon x1.5, Steel x1.3. Blade moves x1.3 (x1.56 against Dragons).",
                       "Dragons' Fire moves x1.3. Draining Kiss, Magical Leaf, Fairy Wind x1.5.",
                       "King's Shield, Crafty Shield and Noble Roar are stronger. Armor and Magic abilities shine.",
                       "Sleepers dream sweetly and heal. Misty Terrain lasts longer.",
                       "3 Dragon attacks rouse the dragon beneath the castle: it becomes a Dragon's Den."],
    :nature_power  => :SECRETSWORD,
    :camouflage    => :FAIRY,
    :secret_power  => 2,
    :type_mods     => { :FAIRY => 1.5, :STEEL => 1.3, :DRAGON => 1.5 },
    :type_messages => { :FAIRY  => "The storybook's magic sparkled!",
                        :STEEL  => "{1} charged in like a knight in shining armor!",
                        :DRAGON => "A dragon's roar shook the castle!" },
    :move_mods     => { :DRAININGKISS => 1.5, :MAGICALLEAF => 1.5, :FAIRYWIND => 1.5 },
    :move_messages => { :DRAININGKISS => "True love's kiss!",
                        :MAGICALLEAF  => "The forest's magic guided the leaves!" },
    :damage_mods   => [
      { :moves => prismfall_fairytale_blades, :mult => 1.3, :message => "{1} wielded {2} like a true knight!" },
      { :moves => prismfall_fairytale_blades, :target => { :types => [:DRAGON] }, :mult => 1.2,
        :message => "{1} struck like a dragonslayer!" },
      { :types => [:FIRE], :category => :damaging, :user => { :types => [:DRAGON] }, :mult => 1.3,
        :message => "The dragon breathed fire!" }
    ],
    :accuracy_mods => [{ :moves => [:SWEETKISS], :set => 100 }],
    :move_stat_boosts => [
      { :moves => [:KINGSSHIELD], :user_stats => { :DEFENSE => 1 }, :message => "{1} raised its shield like a royal knight!" },
      { :moves => [:CRAFTYSHIELD], :user_stats => { :SPECIAL_DEFENSE => 1 }, :message => "A fairy's ward shimmered around {1}!" },
      { :moves => [:NOBLEROAR], :target_stats => { :ATTACK => -1, :SPECIAL_ATTACK => -1 },
        :message => "A roar fit for a king!" }
    ],
    :on_entry      => [
      { :battlers => { :abilities => [:BATTLEARMOR, :SHELLARMOR] }, :stats => { :DEFENSE => 1 },
        :message => "{1}'s armor gleamed like a knight's!" },
      { :battlers => { :abilities => [:MAGICGUARD, :MAGICBOUNCE, :MAGICIAN] }, :stats => { :SPECIAL_DEFENSE => 1 },
        :message => "{1}'s magic sparkled in the storybook light!" }
    ],
    :end_of_round  => [
      { :battlers => { :status => [:SLEEP] }, :heal => 1/16r, :message => "{1} dreams of happily ever after." }
    ],
    :terrain       => { :extend => { :Misty => 3 } },
    :transitions   => [
      { :types => [:DRAGON], :category => :damaging, :to => :DRAGONS_DEN, :uses => 3,
        :progress_message => "Something vast stirs beneath the castle... ({1} more)",
        :message => "The dragon has awoken! Dragonfire swallows the storybook castle..." }
    ],
    :seed => { :item => :MAGICALSEED, :stats => { :SPECIAL_ATTACK => 1, :SPECIAL_DEFENSE => 1 },
               :message => "{1}'s {2} granted it a fairy godmother's blessing!" }
  }
end).call)
