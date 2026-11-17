#===============================================================================
# HOLLOW_CATHEDRAL - Gym 14 (Ghost), Gravenmoor in Antumbra, the Kingdom
# Behind the Glass. A ruined cathedral where the veil between the living and
# the dead is thin. Stage 1 = Haunted (default), stage 2 = Consecrated.
# Ghosts gather in the gloom, candles burn with ghostfire, the ossuary rattles.
# Holy light consecrates it (stage 2); Ghost rites bring the spirits back.
# Shatter the mirrored glass and the Reverse World pours in (INVERSE).
# Family: Magical.
#===============================================================================
FieldEffects.register(:HOLLOW_CATHEDRAL, (lambda do
  holy   = [:SACREDFIRE, :SACREDSWORD, :JUDGMENT, :DAZZLINGGLEAM, :LIGHTOFRUIN]
  rites  = [:CURSE, :SPITE, :GRUDGE, :NIGHTMARE, :LASTRESPECTS, :DESTINYBOND]
  rend   = [:BOOMBURST, :SHADOWFORCE, :HYPERSPACEFURY, :HYPERSPACEHOLE]
  bones  = [:BONECLUB, :BONERUSH, :BONEMERANG, :SHADOWBONE]
  shatter = [
    { :moves => [:TOPSYTURVY], :to => :INVERSE,
      :message => "The mirrored glass shattered! The Kingdom Behind the Glass pours through!" },
    { :moves => rend, :to => :INVERSE, :uses => 2,
      :progress_message => "Cracks spider across the stained glass... ({1} more)",
      :message => "The mirrored glass shattered! The Kingdom Behind the Glass pours through!" }
  ]
  {
    :name          => "Hollow Cathedral",
    :backdrop      => "field_hollow_cathedral",
    :family        => :magical,
    :intro_message => "Candles gutter in the ruined nave... Restless spirits stir in the gloom.",
    :description   => "Ghosts gather in the gloom and the veil is thin (Ghost and Normal hit each other). Hymns echo, candles burn with ghostfire. Holy light consecrates it.",
    :notes         => ["Haunted (stage 1): Ghost x1.5; Ghost moves' own added effects x1.5 as likely. Damaging sound moves x1.3 (the nave echoes).",
                       "The veil is thin: Ghost moves hit Normal types and Normal moves hit Ghost types (neutral).",
                       "Ghostfire: Fire moves also hit as Ghost. Will-O-Wisp never misses.",
                       "Astonish x2; Ominous Wind x1.5 (its boost twice as likely); Poltergeist, Spirit Shackle, Mystical Fire, Infernal Parade and the ossuary's bone moves x1.3. Night Shade x1.5. Lick always paralyzes.",
                       "The spirits crowd around sleepers: Ghost attacks against a sleeping target x1.3. Scary Face also lowers Attack.",
                       "Cursed Body, Perish Body, Wandering Spirit, Mummy +1 Sp. Def on entry; Rattled Pokemon jump at shadows (+1 Speed).",
                       "3 holy acts (Sacred Fire, Sacred Sword, Judgment, Dazzling Gleam, Light of Ruin, Purify, Heal Bell; they count even if they fail) -> Consecrated (stage 2).",
                       "Consecrated: Ghost and Dark x0.8, Fairy x1.2, holy moves x1.5, hymns (sound) x1.3. Normal moves strike Ghost types super effectively. Curses are lifted each turn; Justified +1 Attack on entry. 2 Ghost rites (Curse, Spite, Grudge, Nightmare, Last Respects, Destiny Bond) by a Ghost type bring the spirits back.",
                       "Topsy-Turvy, or 2 dimension-rending moves (Boomburst, Shadow Force, Hyperspace Fury/Hole), shatter the glass -> Inverse Field.",
                       "Magical Seed: +1 Sp. Def, and a wandering spirit makes the holder part Ghost type."],
    :nature_power  => :SHADOWBALL,
    :camouflage    => :GHOST,
    :secret_power  => 8,
    :type_mods     => { :GHOST => 1.5 },
    :type_messages => { :GHOST => "The restless spirits rose up behind {1}!" },
    :move_mods     => { :ASTONISH => 2.0, :OMINOUSWIND => 1.5, :POLTERGEIST => 1.3, :SPIRITSHACKLE => 1.3,
                        :MYSTICALFIRE => 1.3, :INFERNALPARADE => 1.3 }.merge(bones.map { |m| [m, 1.3] }.to_h),
    :move_messages => { :OMINOUSWIND   => "A chill wind howled through the broken windows!",
                        :POLTERGEIST   => "The pews and candlesticks hurled themselves!",
                        :SPIRITSHACKLE => "The shadows pinned the target to the flagstones!",
                        :SHADOWBONE    => "The cathedral's ossuary rattled to life!",
                        :BONERUSH      => "The cathedral's ossuary rattled to life!" },
    :damage_mods   => [
      { :flags => ["Sound"], :category => :damaging, :mult => 1.3, :message => "{2} echoed through the nave!" },
      { :moves => holy, :mult => 1.3, :message => "Light streamed through the stained glass!" },
      { :types => [:GHOST], :category => :damaging, :target => { :status => [:SLEEP] }, :mult => 1.3,
        :message => "The spirits crowded around the sleeper!" }
    ],
    :fixed_damage_mods => [{ :moves => [:NIGHTSHADE], :mult => 1.5, :message => "The shadows stretched long behind {1}!" }],
    # Ghostfire: the altar candles burn with a spirit flame
    :extra_types   => [
      { :types => [:FIRE], :category => :damaging, :add => :GHOST, :message => "The flames burned with an eerie ghostfire!" }
    ],
    # The veil is thin: Ghost and Normal can touch each other
    :effectiveness_mods => [
      { :attack => [:GHOST],  :defend => [:NORMAL], :set => 1.0 },
      { :attack => [:NORMAL], :defend => [:GHOST],  :set => 1.0 }
    ],
    :accuracy_mods => [{ :moves => [:WILLOWISP], :set => 100 }],
    :effect_chance_mods => [{ :types => [:GHOST], :mult => 1.5 }, { :moves => [:OMINOUSWIND], :mult => 2.0 },
                            { :moves => [:LICK], :set => 100 }],
    :move_stat_boosts => [
      { :moves => [:SCARYFACE], :target_stats => { :ATTACK => -1 },
        :message => "The shadows twisted into something truly terrifying!" }
    ],
    :on_entry      => [
      { :battlers => { :abilities => [:CURSEDBODY, :PERISHBODY, :WANDERINGSPIRIT, :MUMMY] },
        :stats => { :SPECIAL_DEFENSE => 1 }, :message => "{1} is at home among the restless dead." },
      { :battlers => { :abilities => [:RATTLED] }, :stats => { :SPEED => 1 },
        :message => "{1} jumped at a shadow - and sped up!" }
    ],
    :transitions   => [
      { :moves => holy + [:PURIFY, :HEALBELL], :even_if_failed => true, :stage => 2, :uses => 3,
        :progress_message => "The cathedral bell stirs... ({1} more)",
        :message => "The bell tolled! Holy light fills the nave and the spirits fall silent." }
    ] + shatter,
    :seed => { :item => :MAGICALSEED, :stats => { :SPECIAL_DEFENSE => 1 }, :add_type => :GHOST,
               :message => "{1}'s {2} let a wandering spirit possess it!" },
    :stages => {
      2 => {
        :backdrop      => "field_hollow_cathedral_consecrated",
        :intro_message => "Holy light pours through the stained glass. The cathedral is consecrated!",
        :description   => "Consecrated: Ghost and Dark weakened, Fairy, hymns and holy moves strengthened, Normal moves smite Ghosts. Ghost rites can undo it.",
        :nature_power  => :DAZZLINGGLEAM,
        :camouflage    => :FAIRY,
        :type_mods     => { :GHOST => 0.8, :DARK => 0.8, :FAIRY => 1.2 },
        :type_messages => { :GHOST => "The holy light held the spirits at bay...",
                            :FAIRY => "The consecrated light shone through {2}!" },
        :move_mods     => {},
        :move_messages => {},
        :damage_mods   => [
          { :flags => ["Sound"], :category => :damaging, :mult => 1.3, :message => "{2} rang out like a hymn!" },
          { :moves => holy, :mult => 1.5, :message => "The consecrated light blazed!" }
        ],
        :fixed_damage_mods => [],
        :extra_types   => [],
        :effectiveness_mods => [
          { :attack => [:GHOST],  :defend => [:NORMAL], :set => 1.0 },
          { :attack => [:NORMAL], :defend => [:GHOST],  :set => 2.0 }
        ],
        :accuracy_mods => [],
        :effect_chance_mods => [],
        :move_stat_boosts => [],
        :on_entry      => [
          { :battlers => { :abilities => [:JUSTIFIED] }, :stats => { :ATTACK => 1 },
            :message => "{1} stood tall in the holy light!" }
        ],
        :end_of_round  => [
          { :battlers => { :condition => proc { |battle, b| b.effects[PBEffects::Curse] } },
            :proc => proc { |battle, b|
              b.effects[PBEffects::Curse] = false
              battle.pbDisplay(FieldEffects.format("The holy light lifted the curse on {1}!", b.pbThis))
              true
            } }
        ],
        :transitions   => [
          { :moves => rites, :user => { :types => [:GHOST] }, :even_if_failed => true, :stage => 1, :uses => 2,
            :progress_message => "The candles flicker and dim... ({1} more)",
            :message => "The candles guttered out! The restless spirits return to the nave." }
        ] + shatter
      }
    }
  }
end).call)
