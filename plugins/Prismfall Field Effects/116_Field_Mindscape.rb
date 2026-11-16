#===============================================================================
# MINDSCAPE - Gym 12 (Psychic), Lucent in Antumbra, the Kingdom Behind the
# Glass. A dreamscape of floating libraries and mirrored stairs where thought
# is made real. Nightmares take shape; loud noise can wake everyone up.
# "You're thinking very loudly. Please stop." - Ilsa Marr
#===============================================================================
FieldEffects.register(:MINDSCAPE, {
  :name          => "Mindscape",
  :backdrop      => "field_mindscape",
  :intro_message => "The world dissolves into a sea of drifting thoughts...",
  :description   => "Psychic surges; nightmares (Dark, Ghost) take shape; dimension rooms last longer. Sleepers wake sooner. Loud Sound moves can shatter the dream.",
  :nature_power  => :PSYCHIC,
  :camouflage    => :PSYCHIC,
  :secret_power  => 3,
  :type_mods     => { :PSYCHIC => 1.5, :DARK => 1.2, :GHOST => 1.2 },
  :type_messages => { :PSYCHIC => "The Mindscape amplified the thought!",
                      :DARK    => "A nightmare took shape!" },
  :move_mods     => { :DREAMEATER => 1.5, :MYSTICALFIRE => 1.3, :EXTRASENSORY => 1.3,
                      :FUTURESIGHT => 1.3, :MIRRORSHOT => 1.5, :PSYSHOCK => 1.2, :STOREDPOWER => 1.2 },
  :move_messages => { :DREAMEATER => "{1} devoured the dream whole!",
                      :MIRRORSHOT => "The mirrored stairs multiplied the glare!" },
  :damage_mods   => [
    # Loud noise jars the dreamscape
    { :flags => ["Sound"], :category => :damaging, :mult => 1.2,
      :message => "{2} reverberated through the dreamscape!" },
    # A disciplined mind is hard to intrude upon
    { :types => [:PSYCHIC], :category => :damaging,
      :target => { :abilities => [:INNERFOCUS, :OWNTEMPO, :OBLIVIOUS] }, :final_mult => 0.75,
      :message => "The disciplined mind resisted the intrusion!" }
  ],
  :on_entry      => [
    { :battlers => { :abilities => [:FOREWARN, :ANTICIPATION] }, :stats => { :SPECIAL_DEFENSE => 1 },
      :message => "{1} foresaw the danger in the dream!" }
  ],
  :end_of_round  => [
    # Dream-sleep is shallow: sleepers wake twice as fast
    { :battlers => { :status => [:SLEEP] }, :proc => proc { |battle, battler|
        next false if battler.statusCount <= 1
        battler.statusCount -= 1
        battle.pbDisplay(FieldEffects.format("{1} is stirring in its dream...", battler.pbThis))
        next true
      } }
  ],
  :terrain       => { :extend => { :Psychic => 3 } },
  :hooks         => {
    # Thought bends space: Trick Room, Magic Room and Wonder Room last 2 extra turns
    :after_move => proc { |battle, user, targets, move, num_hits|
      next if user.lastMoveFailed
      eff = { :TRICKROOM => PBEffects::TrickRoom, :MAGICROOM => PBEffects::MagicRoom,
              :WONDERROOM => PBEffects::WonderRoom }[move.id]
      next if !eff || battle.field.effects[eff] <= 0
      battle.field.effects[eff] += 2
      battle.pbDisplay(FieldEffects.format("The Mindscape folded the dimensions in on themselves!"))
    }
  },
  :transitions   => [
    { :flags => ["Sound"], :category => :damaging, :uses => 3, :to => :NONE,
      :progress_message => "The dreamscape trembles at the noise... ({1} more)",
      :message => "The noise jolted everyone awake! The Mindscape collapsed." },
    { :moves => [:TOPSYTURVY], :to => :INVERSE,
      :message => "The Mindscape turned inside out, into the world behind the glass!" }
  ],
  :seed => { :item => :MAGICALSEED, :stats => { :SPECIAL_ATTACK => 2 }, :confuse => true,
             :message => "{1}'s {2} flooded its mind with thoughts!" }
})
