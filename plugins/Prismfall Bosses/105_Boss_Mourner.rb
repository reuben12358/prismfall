#===============================================================================
# Ch9, the Ironreach reliquary: the Mourner's Trevenant "Glasswood" is a multi-bar
# boss (story/05_ACT_II.md "Boss: Trevenant (multi-bar)"). Trainer data:
# [HOLLOW_MOURNER,Mourner,0] (+100 Hard, +200 Casual), field :COLOSSEUM from
# FieldEffects::TRAINER_FIELDS. Written by the trainer workstream
# (design/TRAINER_FIELD_PLAYBOOK.md section 6). No event change needed: the rule
# fires on trainer load for the ace of every difficulty variant.
#
# He fights defensively ("Not now - get BACK"): each break cures it, clears its
# stat drops and gives it Ingrain-style roots in the pit floor (a heal each turn
# through the field's :ingrain effect) instead of an attack boost.
#===============================================================================
Prismfall::Bosses.register(:MOURNER_TREVENANT, {
  :bars          => { :CASUAL => 2, :STANDARD => 2, :HARD => 3 },
  :break_message => "Glasswood's bark splits... and the glass beneath it holds!",
  :on_break      => { :messages    => ["The Mourner: \"Get BACK!\" Glasswood roots itself into the pit floor."],
                      :cure_status => true, :reset_stats => :negative,
                      :stats       => { :DEFENSE => 1 },
                      :proc        => proc { |battle, battler, _state|
                        next false if battler.effects[PBEffects::Ingrain]
                        battler.effects[PBEffects::Ingrain] = true
                        true
                      } }
})

Prismfall::Bosses.register_trainer_boss(:MOURNER_CH9, {
  :trainer_type => :HOLLOW_MOURNER, :name => "Mourner",
  :versions     => [0, 100, 200],
  :slot         => :ace,
  :boss         => :MOURNER_TREVENANT
})
