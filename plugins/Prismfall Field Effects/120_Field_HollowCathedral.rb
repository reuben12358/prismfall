#===============================================================================
# HOLLOW_CATHEDRAL - Gym 14 (Ghost), Gravenmoor, in Antumbra, the Kingdom Behind
# the Glass. A ruined cathedral where the veil between the living and the dead
# is thin. Stage 1 = Haunted (default), stage 2 = Consecrated.
# Consecrate it with holy light (stage 2); Ghost rites bring the spirits back
# (stage 1). Shatter the mirrored glass and the Reverse World pours in (INVERSE).
#===============================================================================
FieldEffects.register(:HOLLOW_CATHEDRAL, {
  :name          => "Hollow Cathedral",
  :backdrop      => "field_hollow_cathedral",
  :intro_message => "Candles gutter in the ruined nave... Restless spirits stir in the gloom.",
  :description   => "Ghosts rule and the veil is thin (Ghost/Normal hit each other). Hymns echo; holy light consecrates it.",
  :notes         => ["Ghost x1.5; Ghost moves' added effects are more likely. Sound moves x1.3.",
                     "The veil is thin: Ghost moves hit Normal types and Normal moves hit Ghost types.",
                     "Fire moves burn with ghostfire and also hit as Ghost. Will-O-Wisp is far more accurate.",
                     "Sleeping non-Ghost Pokemon are tormented each turn.",
                     "3 holy moves (Sacred Fire, Judgment, Purify, Heal Bell, Dazzling Gleam...) consecrate it.",
                     "Topsy-Turvy, or 2 dimension-rending moves, shatter the glass into the Inverse Field."],
  :nature_power  => :SHADOWBALL,
  :camouflage    => :GHOST,
  :secret_power  => 8,
  :type_mods     => { :GHOST => 1.5 },
  :type_messages => { :GHOST => "The restless spirits howled!" },
  :move_mods     => { :ASTONISH => 2.0, :OMINOUSWIND => 1.5, :POLTERGEIST => 1.3, :SPIRITSHACKLE => 1.3,
                      :MYSTICALFIRE => 1.3, :INFERNALPARADE => 1.3 },
  :move_messages => { :OMINOUSWIND => "A chill wind howled through the broken windows!",
                      :POLTERGEIST => "The pews and candlesticks hurled themselves!",
                      :SPIRITSHACKLE => "The shadows pinned the target to the flagstones!" },
  :damage_mods   => [
    { :flags => ["Sound"], :category => :damaging, :mult => 1.3, :message => "{2} echoed through the nave!" },
    { :moves => [:SACREDFIRE, :SACREDSWORD, :JUDGMENT, :DAZZLINGGLEAM, :LIGHTOFRUIN], :mult => 1.3,
      :message => "Light streamed through the stained glass!" }
  ],
  # Ghostfire: the altar candles burn with a spirit flame
  :extra_types   => [
    { :types => [:FIRE], :category => :damaging, :add => :GHOST,
      :message => "The flames burned with an eerie ghostfire!" }
  ],
  # The veil is thin: Ghost and Normal can touch each other
  :effectiveness_mods => [
    { :attack => [:GHOST],  :defend => [:NORMAL], :set => 1.0 },
    { :attack => [:NORMAL], :defend => [:GHOST],  :set => 1.0 }
  ],
  :accuracy_mods => [{ :moves => [:WILLOWISP], :set => 100 }],
  :effect_chance_mods => [{ :types => [:GHOST], :mult => 1.5 }],
  :move_stat_boosts => [
    { :moves => [:SCARYFACE], :target_stats => { :ATTACK => -1 },
      :message => "The shadows twisted into something truly terrifying!" }
  ],
  :on_entry      => [
    { :battlers => { :abilities => [:CURSEDBODY, :PERISHBODY, :WANDERINGSPIRIT, :MUMMY] },
      :stats => { :SPECIAL_DEFENSE => 1 }, :message => "{1} is at home among the restless dead." }
  ],
  :end_of_round  => [
    { :battlers => { :status => [:SLEEP], :not_types => [:GHOST] }, :damage => 1/16r,
      :message => "{1} is tormented by spirits in its sleep!" }
  ],
  :transitions   => [
    { :moves => [:TOPSYTURVY], :to => :INVERSE,
      :message => "The mirrored glass shattered! The Kingdom Behind the Glass pours through!" },
    { :moves => [:BOOMBURST, :SHADOWFORCE, :HYPERSPACEFURY, :HYPERSPACEHOLE], :to => :INVERSE, :uses => 2,
      :progress_message => "Cracks spider across the stained glass... ({1} more)",
      :message => "The mirrored glass shattered! The Kingdom Behind the Glass pours through!" },
    { :moves => [:SACREDFIRE, :SACREDSWORD, :JUDGMENT, :PURIFY, :HEALBELL, :DAZZLINGGLEAM, :LIGHTOFRUIN],
      :stage => 2, :uses => 3,
      :progress_message => "The cathedral bell stirs... ({1} more)",
      :message => "The bell tolled! Holy light fills the nave and the spirits fall silent." }
  ],
  :seed => { :item => :MAGICALSEED, :stats => { :SPECIAL_DEFENSE => 1 },
             :message => "{1}'s {2} let a wandering spirit possess it!",
             :proc => proc { |battle, battler|
               next false if battler.pbHasType?(:GHOST) || !battler.canChangeType?
               battler.effects[PBEffects::ExtraType] = :GHOST
               battle.pbDisplay(FieldEffects.format("{1} became part Ghost type!", battler.pbThis))
               true
             } },
  :stages => {
    2 => {
      :intro_message => "Holy light pours through the stained glass. The cathedral is consecrated!",
      :description   => "Consecrated: Ghost and Dark weakened, Fairy and holy moves strengthened. Ghost rites can undo it.",
      :nature_power  => :DAZZLINGGLEAM,
      :camouflage    => :FAIRY,
      :type_mods     => { :GHOST => 0.8, :DARK => 0.8, :FAIRY => 1.2 },
      :type_messages => { :GHOST => "The holy light held the spirits at bay...",
                          :FAIRY => "The consecrated light shone through {2}!" },
      :move_mods     => {},
      :move_messages => {},
      :damage_mods   => [
        { :flags => ["Sound"], :category => :damaging, :mult => 1.3, :message => "{2} rang out like a hymn!" },
        { :moves => [:SACREDFIRE, :SACREDSWORD, :JUDGMENT, :DAZZLINGGLEAM, :LIGHTOFRUIN], :mult => 1.5,
          :message => "The consecrated light blazed!" }
      ],
      :extra_types   => [],
      :accuracy_mods => [],
      :effect_chance_mods => [],
      :end_of_round  => [],
      :transitions   => [
        { :moves => [:CURSE, :SPITE, :GRUDGE, :NIGHTMARE, :LASTRESPECTS, :DESTINYBOND],
          :user => { :types => [:GHOST] }, :stage => 1, :uses => 2,
          :progress_message => "The candles flicker and dim... ({1} more)",
          :message => "The candles guttered out! The restless spirits return to the nave." },
        { :moves => [:TOPSYTURVY], :to => :INVERSE,
          :message => "The mirrored glass shattered! The Kingdom Behind the Glass pours through!" },
        { :moves => [:BOOMBURST, :SHADOWFORCE, :HYPERSPACEFURY, :HYPERSPACEHOLE], :to => :INVERSE, :uses => 2,
          :progress_message => "Cracks spider across the stained glass... ({1} more)",
          :message => "The mirrored glass shattered! The Kingdom Behind the Glass pours through!" }
      ]
    }
  }
})
