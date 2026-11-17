#===============================================================================
# CORROSIVE_MIRE - Gym 6 (Poison), Mirefen. Toxic runoff pooled under Nadir, the
# City Below. Poison Pokemon weaponise the mire: they fling toxic mud, lace
# every splash with venom and eat through steel. Grass drinks the toxins. Fire
# ignites the marsh gas around the foes - twice and it burns off into a
# WASTELAND. Purify or fairy mist cleanses it (WATER_SURFACE).
# Family: Synthetic.
#===============================================================================
FieldEffects.register(:CORROSIVE_MIRE, (lambda do
  muds = [:MUDSLAP, :MUDSHOT, :MUDBOMB, :MUDDYWATER]
  {
    :name          => "Corrosive Mire",
    :backdrop      => "field_corrosive_mire",
    :family        => :synthetic,
    :intro_message => "Toxic sludge bubbles underfoot... the air reeks of corrosion.",
    :description   => "Poison Pokemon weaponise the mire: venom laces mud and water, toxins eat through steel, and fire turns the marsh gas into a weapon.",
    :notes         => ["Poison x1.5; Poison moves' own added effects x1.5 as likely. Poison moves hit Steel types (neutral).",
                       "Grass drinks the toxins: Grass moves also hit as Poison. Mud moves and Muddy Water also hit as Poison.",
                       "Acid, Acid Spray, Smog x2; Clear Smog, Sludge, mud moves, Barb Barrage x1.5; Sludge Wave, Mortal Spin x1.3; Gunk Shot x1.2.",
                       "Venoshock and Barb Barrage hit grounded targets as if they were already poisoned (x2).",
                       "Gunk Shot x1.25 accuracy; Smog and Poison Gas x1.4; Poison Powder, Stun Spore, Sleep Powder x1.25. Damaging Water moves may poison (20%).",
                       "Each turn, every Poison type may fling toxic mud at a grounded foe (30%: poisons). Poison types are nourished (1/16 HP).",
                       "Toxic Boost is always active. Merciless, Corrosion, Poison Touch +1 Attack on entry; Toxic Debris +1 Defense.",
                       "Fire ignites the marsh gas: Fire x1.3 and every damaging Fire move scorches the user's grounded, non-Fire foes for 1/8 HP.",
                       "Misty Terrain, or 2 Purify, cleanse it -> Water Surface. 2 damaging Fire moves burn the gas off -> Wasteland.",
                       "Synthetic Seed: +1 Attack, +1 Sp. Atk, but the holder is poisoned (Guts, Poison Heal and Toxic Boost love it)."],
    :nature_power  => :ACIDSPRAY,
    :camouflage    => :POISON,
    :secret_power  => 6,
    :activate_abilities => [:TOXICBOOST],
    :type_mods     => { :POISON => 1.5, :FIRE => 1.3 },
    :type_messages => { :POISON => "{1} drew the mire's poison into the attack!",
                        :FIRE   => "The marsh gas flared up with the flames!" },
    :move_mods     => { :ACID => 2.0, :ACIDSPRAY => 2.0, :SMOG => 2.0, :CLEARSMOG => 1.5, :SLUDGE => 1.5,
                        :MUDBOMB => 1.5, :MUDSHOT => 1.5, :MUDSLAP => 1.5, :BARBBARRAGE => 1.5,
                        :SLUDGEWAVE => 1.3, :MORTALSPIN => 1.3, :GUNKSHOT => 1.2 },
    :move_messages => { :ACIDSPRAY  => "The acid hissed everywhere it landed!",
                        :SLUDGEWAVE => "{1} raised a wave of bubbling sludge!",
                        :SMOG       => "The mire's fumes thickened the smog!" },
    :effectiveness_mods => [{ :attack => [:POISON], :defend => [:STEEL], :set => 1.0 }],
    :extra_types   => [
      { :moves => muds, :add => :POISON, :message => "The mud was laced with toxins!" },
      { :types => [:GRASS], :category => :damaging, :add => :POISON,
        :message => "{1}'s plants had drunk deep of the toxins!" }
    ],
    :damage_mods   => [
      { :moves => [:VENOSHOCK, :BARBBARRAGE], :mult => 2.0,
        :target => { :grounded => true, :condition => proc { |battle, b| !b.poisoned? } },
        :message => "The mire's toxins had already seeped into the target!" }
    ],
    :accuracy_mods => [
      { :moves => [:GUNKSHOT], :mult => 1.25 },
      { :moves => [:SMOG, :POISONGAS], :mult => 1.4 },
      { :moves => [:POISONPOWDER, :STUNSPORE, :SLEEPPOWDER], :mult => 1.25 }
    ],
    :added_effects => [
      { :types => [:WATER], :category => :damaging, :chance => 20, :status => :POISON,
        :message => "The murky water poisoned {1}!" }
    ],
    :effect_chance_mods => [{ :types => [:POISON], :mult => 1.5 }],
    :on_entry      => [
      { :battlers => { :abilities => [:MERCILESS, :CORROSION, :POISONTOUCH] }, :stats => { :ATTACK => 1 },
        :message => "{1} reveled in the toxins!" },
      { :battlers => { :abilities => [:TOXICDEBRIS] }, :stats => { :DEFENSE => 1 },
        :message => "{1} armored itself in toxic sludge!" }
    ],
    :end_of_round  => [
      { :battlers => { :types => [:POISON] }, :heal => 1/16r, :message => "The mire nourished {1}." },
      # Poison types weaponise the mire: a splash of toxic mud at a grounded foe
      { :battlers => { :types => [:POISON] }, :chance => 30, :proc => proc { |battle, battler|
          foes = battle.allOtherSideBattlers(battler.index).select do |f|
            !f.fainted? && !f.airborne? && f.pbCanPoison?(battler, false)
          end
          next false if foes.empty?
          foe = foes[battle.pbRandom(foes.length)]
          foe.pbPoison(battler, FieldEffects.format("{1} flung toxic mud at {2}! {2} was poisoned!",
                                                    battler.pbThis, foe.pbThis))
          true
        } }
    ],
    :hooks         => {
      # The attacker sets the marsh gas around its foes alight
      :after_move => proc { |battle, user, targets, move, num_hits|
        next if user.lastMoveFailed || !move.damagingMove? || move.calcType != :FIRE
        foes = battle.allOtherSideBattlers(user.index).select do |b|
          !b.fainted? && !b.airborne? && !b.pbHasType?(:FIRE) && b.takesIndirectDamage?
        end
        next if foes.empty?
        battle.pbDisplay(FieldEffects.format("{1} ignited the marsh gas around its foes!", user.pbThis))
        foes.each do |b|
          b.pbTakeEffectDamage([b.totalhp / 8, 1].max) do |_hp|
            battle.pbDisplay(FieldEffects.format("Flames burst up around {1}!", b.pbThis))
          end
        end
      }
    },
    :transitions   => [
      { :terrain => [:Misty], :to => :WATER_SURFACE,
        :message => "The fairy mist purified the mire into clear water!" },
      { :moves => [:PURIFY], :even_if_failed => true, :to => :WATER_SURFACE, :uses => 2,
        :progress_message => "The sludge grows clearer... ({1} more)",
        :message => "The mire was purified into clear, open water!" },
      { :types => [:FIRE], :category => :damaging, :to => :WASTELAND, :uses => 2,
        :progress_message => "The marsh gas is burning off... ({1} more)",
        :message => "The marsh gas burned off in one roaring flare! Scorched slag is all that's left!" }
    ],
    :seed => { :item => :SYNTHETICSEED, :status => :POISON, :stats => { :ATTACK => 1, :SPECIAL_ATTACK => 1 },
               :message => "{1}'s {2} filled it with corrosive vigor!" }
  }
end).call)
