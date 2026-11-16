#===============================================================================
# BLEED - Imprints spilling beyond their cities. Unstable: every few rounds it
# borrows the effects of another registered field (any field added later
# joins the pool automatically).
#===============================================================================
FieldEffects.register(:BLEED, {
  :name          => "The Bleed",
  :backdrop      => "field_bleed",
  :intro_message => "Reality frays at the edges... The Bleed is spreading!",
  :description   => "Every 3 rounds it borrows another field's effects. Off-type attacks and stats warp unpredictably.",
  :nature_power  => :TRIATTACK,
  :camouflage    => :PSYCHIC,
  :secret_power  => 4,
  :borrow        => { :pool => :all, :interval => 3, :count => 1, :order => :random,
                      :start_immediately => true,
                      :message => "The Bleed convulses... echoes of the {1} tear through the battlefield!" },
  :damage_mods   => [
    # Raw Imprint energy rewards coverage: non-STAB attacks are strengthened
    { :category => :damaging, :mult => 1.2,
      :condition => proc { |battle, user, target, move, type| type && !user.pbHasType?(type) },
      :message => "The Bleed warped {2} into something stronger!" }
  ],
  :end_of_round  => [
    { :chance => 20, :proc => proc { |battle, battler|
        stats = [:ATTACK, :DEFENSE, :SPECIAL_ATTACK, :SPECIAL_DEFENSE, :SPEED]
        up = stats.delete_at(battle.pbRandom(stats.length))
        down = stats[battle.pbRandom(stats.length)]
        battle.pbDisplay(FieldEffects.format("The Bleed warped {1}'s power!", battler.pbThis))
        FieldEffects.apply_stat_changes(battler, { up => 1, down => -1 }, nil)
        true
      } }
  ],
  :seed => [
    { :item => :MAGICALSEED, :message => "{1}'s {2} drank from the Bleed!",
      :proc => proc { |battle, battler|
        stats = [:ATTACK, :DEFENSE, :SPECIAL_ATTACK, :SPECIAL_DEFENSE, :SPEED]
        FieldEffects.apply_stat_changes(battler, { stats[battle.pbRandom(stats.length)] => 2 }, battler)
      } },
    { :item => :SYNTHETICSEED, :stats => { :DEFENSE => 1, :SPECIAL_DEFENSE => 1 },
      :message => "{1}'s {2} insulated it against the Bleed!" }
  ]
})
