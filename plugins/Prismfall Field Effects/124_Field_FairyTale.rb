#===============================================================================
# FAIRY_TALE - Gym 17 (Fairy), Gloaming, the heart of Elowen's fairy forest.
# A storybook castle glade of knights, dragons and fairy magic (Reborn homage).
# Fairies cast spells, knights draw gleaming blades, dragons breathe dragonfire
# and true love's kiss wakes any sleeper. Rouse the dragon beneath the castle
# (3 Dragon attacks) -> DRAGONS_DEN. Family: Magical.
#===============================================================================
FieldEffects.register(:FAIRY_TALE, (lambda do
  blades = [:SACREDSWORD, :SECRETSWORD, :SMARTSTRIKE, :BEHEMOTHBLADE, :LEAFBLADE, :NIGHTSLASH, :PSYCHOCUT,
            :SOLARBLADE, :XSCISSOR, :SLASH, :CUT, :FURYCUTTER, :AIRSLASH, :RAZORSHELL, :CROSSPOISON, :STONEAXE,
            :CEASELESSEDGE, :AQUACUTTER, :BITTERBLADE, :KOWTOWCLEAVE, :PSYBLADE, :MIGHTYCLEAVE, :TACHYONCUTTER]
  spells = { :DRAININGKISS => 2.0, :MAGICALLEAF => 1.5, :FAIRYWIND => 1.5, :MYSTICALFIRE => 1.5, :ANCIENTPOWER => 1.5,
             :RELICSONG => 1.5, :SPARKLINGARIA => 1.5, :FLEURCANNON => 1.5, :MOONGEISTBEAM => 1.3,
             :BEHEMOTHBASH => 1.3 }
  {
    :name          => "Fairy Tale",
    :backdrop      => "field_fairy_tale",
    :family        => :magical,
    :intro_message => "Once upon a time, in a castle deep in the forest... the story begins!",
    :description   => "Fairies cast spells, knights draw gleaming blades and dragons breathe dragonfire. Armour and magic shine; true love's kiss wakes any sleeper. Rouse the dragon to change the story.",
    :notes         => ["Fairy x1.5, Dragon x1.5, Steel x1.3. Marvel Scale is always active.",
                       "Knights: blade moves x1.3, and x1.2 more against Dragons; Steel moves strike Dragons like a dragonslayer (x1.5). Cut and Slash become gleaming Steel blades.",
                       "Dragonfire: Fire moves also hit as Dragon.",
                       "Spells: Draining Kiss x2; Magical Leaf, Fairy Wind, Mystical Fire, Ancient Power, Relic Song, Sparkling Aria, Fleur Cannon x1.5; Moongeist Beam, Behemoth Bash x1.3.",
                       "True love's kiss: Draining Kiss and Sweet Kiss wake a sleeping target. Sweet Kiss never misses.",
                       "King's Shield +1 Def, Crafty Shield +1 Sp. Def, Flower Shield +1 Def and Sp. Def; Noble Roar lowers Atk and Sp. Atk one stage more.",
                       "On entry: Battle Armor, Shell Armor +1 Def; Magic Guard, Magic Bounce, Mirror Armor, Pastel Veil +1 Sp. Def; Magician +1 Sp. Atk.",
                       "Sleepers dream of happily ever after (1/16 HP a turn). Misty Terrain lasts 3 turns longer.",
                       "3 Dragon attacks rouse the dragon beneath the castle -> Dragon's Den.",
                       "Magical Seed: +1 Sp. Atk and +1 Sp. Def (a fairy godmother's blessing)."],
    :nature_power  => :SECRETSWORD,
    :camouflage    => :FAIRY,
    :secret_power  => 2,
    :activate_abilities => [:MARVELSCALE],
    :type_mods     => { :FAIRY => 1.5, :STEEL => 1.3, :DRAGON => 1.5 },
    :type_messages => { :FAIRY  => "The storybook's magic sparkled through {2}!",
                        :STEEL  => "{1} charged in like a knight in shining armor!",
                        :DRAGON => "A dragon's roar shook the castle!" },
    :move_mods     => spells,
    :move_messages => { :DRAININGKISS => "True love's kiss!",
                        :MAGICALLEAF  => "The forest's magic guided the leaves!",
                        :ANCIENTPOWER => "{1} wove an ancient spell!",
                        :RELICSONG    => "The old song echoed off the castle walls!" },
    :type_changes  => [
      { :moves => [:CUT, :SLASH], :to => :STEEL, :message => "{1} drew a gleaming blade!" }
    ],
    :extra_types   => [
      { :types => [:FIRE], :category => :damaging, :add => :DRAGON, :message => "{1} breathed searing dragonfire!" }
    ],
    :damage_mods   => [
      { :moves => blades, :mult => 1.3, :message => "{1} wielded {2} like a true knight!" },
      { :moves => blades, :target => { :types => [:DRAGON] }, :mult => 1.2 },
      { :types => [:STEEL], :category => :damaging, :target => { :types => [:DRAGON] }, :mult => 1.5,
        :message => "{1} struck like a dragonslayer!" }
    ],
    :accuracy_mods => [{ :moves => [:SWEETKISS], :set => 100 }],
    :added_effects => [
      { :moves => [:DRAININGKISS], :proc => proc { |battle, user, target, move|
          next if target.fainted? || target.status != :SLEEP
          target.pbCureStatus(false)
          battle.pbDisplay(FieldEffects.format("True love's kiss woke {1}!", target.pbThis))
        } }
    ],
    :move_stat_boosts => [
      { :moves => [:KINGSSHIELD], :user_stats => { :DEFENSE => 1 }, :message => "{1} raised its shield like a royal knight!" },
      { :moves => [:CRAFTYSHIELD], :user_stats => { :SPECIAL_DEFENSE => 1 }, :message => "A fairy's ward shimmered around {1}!" },
      { :moves => [:FLOWERSHIELD], :user_stats => { :DEFENSE => 1, :SPECIAL_DEFENSE => 1 },
        :message => "A bower of enchanted roses closed around {1}!" },
      { :moves => [:NOBLEROAR], :target_stats => { :ATTACK => -1, :SPECIAL_ATTACK => -1 }, :message => "A roar fit for a king!" }
    ],
    :hooks         => {
      # Sweet Kiss wakes a sleeper too (status moves have no hits, so this runs after the move)
      :after_move => proc { |battle, user, targets, move, num_hits|
        next if user.lastMoveFailed || move.id != :SWEETKISS
        targets.each do |t|
          next if t.fainted? || t.status != :SLEEP
          t.pbCureStatus(false)
          battle.pbDisplay(FieldEffects.format("True love's kiss woke {1}!", t.pbThis))
        end
      }
    },
    :on_entry      => [
      { :battlers => { :abilities => [:BATTLEARMOR, :SHELLARMOR] }, :stats => { :DEFENSE => 1 },
        :message => "{1}'s armor gleamed like a knight's!" },
      { :battlers => { :abilities => [:MAGICGUARD, :MAGICBOUNCE, :MIRRORARMOR, :PASTELVEIL] },
        :stats => { :SPECIAL_DEFENSE => 1 }, :message => "{1}'s magic sparkled in the storybook light!" },
      { :battlers => { :abilities => [:MAGICIAN] }, :stats => { :SPECIAL_ATTACK => 1 },
        :message => "{1} conjured a storybook spell!" }
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
