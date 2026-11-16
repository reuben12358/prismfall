#===============================================================================
# CORROSIVE_MIRE - Gym 6 (Poison), Mirefen. Toxic runoff pooled beneath Lumen.
#===============================================================================
FieldEffects.register(:CORROSIVE_MIRE, {
  :name          => "Corrosive Mire",
  :backdrop      => "field_corrosive_mire",
  :intro_message => "Toxic sludge bubbles underfoot... the air reeks of corrosion.",
  :description   => "Poison eats through Steel, mud and water carry toxins, fire ignites the fumes.",
  :nature_power  => :ACIDSPRAY,
  :camouflage    => :POISON,
  :secret_power  => 6,
  :type_mods     => { :POISON => 1.5, :GRASS => 0.75 },
  :type_messages => { :POISON => "The toxic sludge bubbled up!",
                      :GRASS  => "The plants withered in the corrosion..." },
  :move_mods     => { :ACID => 2.0, :ACIDSPRAY => 2.0, :SMOG => 2.0, :CLEARSMOG => 1.5,
                      :SLUDGEWAVE => 1.3, :MUDBOMB => 1.5, :MUDSHOT => 1.5, :MUDSLAP => 1.5 },
  :move_messages => { :ACIDSPRAY => "The acid sprayed everywhere!" },
  :effectiveness_mods => [{ :attack => [:POISON], :defend => [:STEEL], :set => 1.0 }],
  :extra_types   => [
    { :moves => [:MUDSLAP, :MUDSHOT, :MUDBOMB, :MUDDYWATER], :add => :POISON,
      :message => "The mud was laced with toxins!" }
  ],
  :accuracy_mods => [
    { :moves => [:GUNKSHOT], :mult => 1.25 },
    { :moves => [:SMOG, :POISONGAS], :mult => 1.4 }
  ],
  :added_effects => [
    { :types => [:WATER], :category => :damaging, :chance => 20, :status => :POISON,
      :message => "The murky water poisoned {1}!" }
  ],
  :effect_chance_mods => [{ :types => [:POISON], :mult => 1.5 }],
  :on_entry      => [
    { :battlers => { :abilities => [:MERCILESS, :CORROSION, :POISONTOUCH] }, :stats => { :ATTACK => 1 },
      :message => "{1} reveled in the toxins!" }
  ],
  :end_of_round  => [
    { :battlers => { :types => [:POISON] }, :heal => 1/16r, :message => "The mire nourished {1}." },
    { :battlers => { :grounded => true, :types => [:STEEL], :not_types => [:POISON] }, :damage => 1/16r,
      :message => "The mire is corroding {1}'s metal!" },
    { :battlers => { :grounded => true, :not_types => [:POISON, :STEEL] }, :chance => 20,
      :status => :POISON, :message => "{1} was poisoned by the corrosive mire!" }
  ],
  :hooks         => {
    # Fire ignites the toxic fumes: everyone not Fire-type is caught in the blast
    :after_move => proc { |battle, user, targets, move, num_hits|
      next if user.lastMoveFailed || !move.damagingMove? || move.calcType != :FIRE
      battle.pbDisplay(FieldEffects.format("The toxic fumes ignited in an explosion!"))
      battle.pbPriority(true).each do |b|
        next if b.fainted? || b.pbHasType?(:FIRE) || !b.takesIndirectDamage?
        b.pbTakeEffectDamage([b.totalhp / 8, 1].max) do |_hp|
          battle.pbDisplay(FieldEffects.format("{1} was caught in the blast!", b.pbThis))
        end
      end
    }
  },
  :transitions   => [
    { :terrain => [:Misty], :to => :WATER_SURFACE,
      :message => "The fairy mist purified the mire into clear water!" },
    { :moves => [:PURIFY], :to => :WATER_SURFACE, :uses => 2,
      :progress_message => "The sludge grows clearer... ({1} more)",
      :message => "The mire was purified into clear water!" },
    { :types => [:FIRE], :category => :damaging, :to => :WASTELAND, :uses => 2,
      :message => "The flames consumed the mire, leaving a blasted wasteland!" }
  ],
  :seed => { :item => :SYNTHETICSEED, :status => :POISON, :stats => { :ATTACK => 1, :SPECIAL_ATTACK => 1 },
             :message => "{1}'s {2} filled it with corrosive vigor!" }
})
