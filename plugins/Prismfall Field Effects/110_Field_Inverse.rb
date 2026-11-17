#===============================================================================
# INVERSE - Antumbra, the Kingdom Behind the Glass. Giratina's mirrored realm:
# the type chart turns upside down and everything that reflects grows strong.
# Topsy-Turvy rights the world again (back to the field it came from).
# Family: Magical.
#===============================================================================
FieldEffects.register(:INVERSE, {
  :name          => "Inverse Field",
  :backdrop      => "field_inverse",
  :family        => :magical,
  :intro_message => "The world turns inside out... Type matchups are reversed!",
  :description   => "The Reverse World: the type chart is inverted, reflections strike back harder, and creatures of mind and shadow move freely.",
  :notes         => ["Inverse type chart: immunities and resistances become weaknesses (x2); weaknesses become resistances (x0.5). Airborne Pokemon still dodge Ground moves.",
                     "Ghost, Psychic and Dark x1.2. Shadow Force, Mirror Shot x1.5; Phantom Force, Foul Play x1.3; Psyshock x1.2.",
                     "Reflections strike back harder: Counter, Mirror Coat, Metal Burst and Comeuppance deal x1.25. Mirror Shot always lowers accuracy.",
                     "Psychic attacks may turn the target's thoughts inside out (10% confusion). Confuse Ray, Hypnosis, Dark Void x1.2 accuracy.",
                     "Contrary Pokemon feel at home (+1 Speed on entry). Magic Bounce and Mirror Armor +1 Sp. Def / Def on entry.",
                     "Trick Room, Magic Room and Wonder Room last 3 turns longer; Psychic Terrain 3 turns longer. Topsy-Turvy also gives +1 Speed.",
                     "Topsy-Turvy rights the world -> the field it came from (or the Mindscape).",
                     "Magical Seed: +1 Attack, +1 Sp. Atk, but -2 Speed (perfect under Trick Room)."],
  :nature_power  => :TRIATTACK,
  :camouflage    => :GHOST,
  :secret_power  => 4,
  :inverse       => true,
  :type_mods     => { :GHOST => 1.2, :PSYCHIC => 1.2, :DARK => 1.2 },
  :type_messages => { :GHOST => "The Reverse World answers {1}'s call!" },
  :move_mods     => { :SHADOWFORCE => 1.5, :MIRRORSHOT => 1.5, :PHANTOMFORCE => 1.3, :FOULPLAY => 1.3,
                      :PSYSHOCK => 1.2 },
  :move_messages => { :SHADOWFORCE => "The Distortion surged through {2}!",
                      :MIRRORSHOT  => "A thousand mirrored shards flared at once!",
                      :FOULPLAY    => "{1} turned the foe's strength against it!" },
  :fixed_damage_mods => [
    { :moves => [:COUNTER, :MIRRORCOAT, :METALBURST, :COMEUPPANCE], :mult => 1.25,
      :message => "The mirror world magnified the reflection!" }
  ],
  :accuracy_mods => [{ :moves => [:CONFUSERAY, :HYPNOSIS, :DARKVOID], :mult => 1.2 }],
  :effect_chance_mods => [{ :moves => [:MIRRORSHOT], :set => 100 }],
  :added_effects => [
    { :types => [:PSYCHIC], :category => :damaging, :chance => 10, :confuse => true,
      :message => "{1}'s thoughts were turned inside out!" }
  ],
  :move_stat_boosts => [
    { :moves => [:TOPSYTURVY], :user_stats => { :SPEED => 1 }, :message => "{1} moves freely in the upside-down world!" }
  ],
  :effect_durations => { :TRICKROOM => [3, "The Reverse World twisted the dimensions even further!"],
                         :MAGICROOM => [3, "The Reverse World twisted the dimensions even further!"],
                         :WONDERROOM => [3, "The Reverse World twisted the dimensions even further!"] },
  :on_entry      => [
    { :battlers => { :abilities => [:CONTRARY] }, :stats => { :SPEED => -1 },
      :message => "{1} feels right at home in the reversed world!" },
    { :battlers => { :abilities => [:MAGICBOUNCE] }, :stats => { :SPECIAL_DEFENSE => 1 },
      :message => "{1} shimmered like the glass around it!" },
    { :battlers => { :abilities => [:MIRRORARMOR] }, :stats => { :DEFENSE => 1 },
      :message => "{1}'s armor mirrored the world behind the glass!" }
  ],
  :terrain       => { :extend => { :Psychic => 3 } },
  :transitions   => [
    { :moves => [:TOPSYTURVY], :to => proc { |battle| FieldEffects.previous_field(battle, :MINDSCAPE) },
      :message => "The world flipped right side up again!" }
  ],
  :seed => { :item => :MAGICALSEED, :stats => { :SPEED => -2, :ATTACK => 1, :SPECIAL_ATTACK => 1 },
             :message => "{1}'s {2} turned its world upside down!" }
})
