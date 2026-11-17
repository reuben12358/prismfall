#===============================================================================
# MINDSCAPE - Gym 12 (Psychic), Lucent in Antumbra, the Kingdom Behind the
# Glass. A dreamscape of floating libraries and mirrored stairs where thought
# is made real. Stage 1 = Dream; dark moves curdle it into stage 2 =
# Nightmare (shadows feed, light falters); soothing moves calm it again.
# Topsy-Turvy - or enough noise - cracks the dream like glass: INVERSE.
# "You're thinking very loudly. Please stop." - Ilsa Marr
# Family: Magical.
#===============================================================================
FieldEffects.register(:MINDSCAPE, (lambda do
  dreamy   = { :DREAMEATER => 1.5, :MIRRORSHOT => 1.5, :PSYBEAM => 1.5, :EXPANDINGFORCE => 1.3,
               :MYSTICALFIRE => 1.3, :EXTRASENSORY => 1.3, :FUTURESIGHT => 1.3, :ESPERWING => 1.3,
               :LUMINACRASH => 1.3, :PSYSHOCK => 1.2, :STOREDPOWER => 1.2 }
  darkness = [:DARKVOID, :NIGHTMARE, :SPITE]
  soothing = [:CALMMIND, :AROMATHERAPY, :HEALBELL, :SWEETKISS, :LUNARBLESSING, :WISH, :MOONLIGHT]
  crack = { :flags => ["Sound"], :category => :damaging, :uses => 3, :to => :INVERSE,
            :progress_message => "The dream rings like glass at the noise... ({1} more)",
            :message => "The noise cracked the dream like glass! Behind it lies the world behind the glass!" }
  flip  = { :moves => [:TOPSYTURVY], :to => :INVERSE,
            :message => "The Mindscape turned inside out, into the world behind the glass!" }
  disciplined = { :types => [:PSYCHIC], :category => :damaging,
                  :target => { :abilities => [:INNERFOCUS, :OWNTEMPO, :OBLIVIOUS] }, :final_mult => 0.75,
                  :message => "The disciplined mind resisted the intrusion!" }
  sound = { :flags => ["Sound"], :category => :damaging, :mult => 1.2, :message => "{2} reverberated through the dreamscape!" }
  rooms = { :TRICKROOM => [2, "The Mindscape folded the dimensions in on themselves!"],
            :MAGICROOM => [2, "The Mindscape folded the dimensions in on themselves!"],
            :WONDERROOM => [2, "The Mindscape folded the dimensions in on themselves!"] }
  {
    # ---- Stage 1: Dream ---------------------------------------------------------
    :name          => "Mindscape",
    :backdrop      => "field_mindscape",
    :family        => :magical,
    :intro_message => "The world dissolves into a sea of drifting thoughts...",
    :description   => "Thought is made real: Psychic surges, nightmares take shape, rooms fold longer, dreams are shallow. Dark moves curdle it into a Nightmare; noise or Topsy-Turvy shatter it.",
    :notes         => ["Dream (stage 1): Psychic x1.5; Dark and Ghost x1.2 (nightmares lurk). Damaging sound moves x1.2.",
                       "Dream Eater, Mirror Shot, Psybeam x1.5; Expanding Force, Mystical Fire, Extrasensory, Future Sight, Esper Wing, Lumina Crash x1.3; Psyshock, Stored Power x1.2.",
                       "A disciplined mind resists: Psychic moves deal x0.75 to Inner Focus, Own Tempo and Oblivious Pokemon.",
                       "Dream-sleep is shallow: sleepers wake twice as fast. Meditate and Kinesis work one stage better.",
                       "Forewarn and Anticipation +1 Sp. Def on entry; Telepathy +1 Speed. Trick Room, Magic Room, Wonder Room +2 turns; Psychic Terrain +3.",
                       "Dark Void, Nightmare or Spite (or 3 Dark attacks) curdle the dream -> Nightmare (stage 2).",
                       "Nightmare: Dark and Ghost x1.5, Psychic x1.2, Fairy x0.8. Hex x1.5, Dream Eater x2; Hypnosis and Dark Void more accurate; Dark and Ghost types feed on the dread (1/16 HP a turn); sleep is no longer shallow. 2 soothing moves (Calm Mind, Heal Bell, Aromatherapy, Sweet Kiss, Wish...) calm it back to a dream.",
                       "Topsy-Turvy, or 3 damaging sound moves, crack the dream -> Inverse Field.",
                       "Magical Seed: +2 Sp. Atk, but the flood of thoughts confuses the holder."],
    :nature_power  => :PSYCHIC,
    :camouflage    => :PSYCHIC,
    :secret_power  => 3,
    :type_mods     => { :PSYCHIC => 1.5, :DARK => 1.2, :GHOST => 1.2 },
    :type_messages => { :PSYCHIC => "The Mindscape gave {1}'s thoughts real shape!",
                        :DARK    => "A nightmare took shape around {2}!" },
    :move_mods     => dreamy,
    :move_messages => { :DREAMEATER => "{1} devoured the dream whole!",
                        :MIRRORSHOT => "The mirrored stairs multiplied the glare!",
                        :PSYBEAM    => "Dream-light rippled down the mirrored stairs!" },
    :damage_mods   => [sound, disciplined],
    :move_stat_boosts => [
      { :moves => [:MEDITATE], :user_stats => { :ATTACK => 1 }, :message => "{1}'s thoughts sharpened like a blade!" },
      { :moves => [:KINESIS], :target_stats => { :ACCURACY => -1 }, :message => "The bent spoon bent the whole dreamscape!" }
    ],
    :effect_durations => rooms,
    :on_entry      => [
      { :battlers => { :abilities => [:FOREWARN, :ANTICIPATION] }, :stats => { :SPECIAL_DEFENSE => 1 },
        :message => "{1} foresaw the danger in the dream!" },
      { :battlers => { :abilities => [:TELEPATHY] }, :stats => { :SPEED => 1 },
        :message => "{1} read the dreamscape's currents!" }
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
    :transitions   => [
      { :moves => darkness, :even_if_failed => true, :stage => 2,
        :message => "The dream curdled into a nightmare!" },
      { :types => [:DARK], :category => :damaging, :uses => 3, :stage => 2,
        :progress_message => "Shadows are creeping into the dream... ({1} more)",
        :message => "The dream curdled into a nightmare!" },
      flip, crack
    ],
    :seed => { :item => :MAGICALSEED, :stats => { :SPECIAL_ATTACK => 2 }, :confuse => true,
               :message => "{1}'s {2} flooded its mind with thoughts!" },
    :stages => {
      # ---- Stage 2: Nightmare --------------------------------------------------
      2 => {
        :backdrop      => "field_mindscape_nightmare",
        :intro_message => "The dream has curdled into a nightmare...",
        :description   => "Nightmare: shadows feed on dread and grow strong; light falters. Soothing moves calm it back into a dream.",
        :type_mods     => { :DARK => 1.5, :GHOST => 1.5, :PSYCHIC => 1.2, :FAIRY => 0.8 },
        :type_messages => { :DARK  => "{1} struck from inside the nightmare!",
                            :GHOST => "The ghosts thickened in the dark around {1}!",
                            :FAIRY => "The nightmare dimmed the fairy light..." },
        :move_mods     => dreamy.merge(:DREAMEATER => 2.0, :HEX => 1.5),
        :move_messages => { :DREAMEATER => "{1} feasted on the nightmare!",
                            :HEX        => "The nightmare amplified the curse!" },
        :accuracy_mods => [{ :moves => [:HYPNOSIS], :mult => 1.25 }, { :moves => [:DARKVOID], :mult => 1.2 }],
        :end_of_round  => [
          { :battlers => { :types => [:DARK, :GHOST] }, :heal => 1/16r, :message => "{1} fed on the dread in the air." }
        ],
        :transitions   => [
          { :moves => soothing, :even_if_failed => true, :stage => 1, :uses => 2,
            :progress_message => "The nightmare is softening... ({1} more)",
            :message => "The nightmare melted back into a gentle dream." },
          flip, crack
        ]
      }
    }
  }
end).call)
