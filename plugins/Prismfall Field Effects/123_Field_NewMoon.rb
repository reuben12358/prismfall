#===============================================================================
# NEW_MOON - Gym 16 (Dark), Underveil, the heart of Nadir, the City Below.
# A black sky, a dead moon, a cold starfield over the undercity rooftops.
# A darkness ladder (Desolation's Darkness field) with a lit rung:
#   1 New Moon (default)  --dark moves-->  2 Abyss  --light-->  1
#   1 New Moon            --light x3-->    3 Lamplight (Nadir's gaslamps relit)
#   3 Lamplight           --dark x3-->     1
# Creatures of the dark hide and strike from it; stars and true light pierce
# it. Family: Magical.
#===============================================================================
FieldEffects.register(:NEW_MOON, (lambda do
  shadows = [:DARKPULSE, :NIGHTDAZE, :NIGHTSLASH, :FALSESURRENDER, :SHADOWBALL, :SHADOWBONE, :SHADOWCLAW,
             :SHADOWFORCE, :SHADOWSNEAK, :SHADOWPUNCH, :PHANTOMFORCE, :SPIRITSHACKLE, :OMINOUSWIND, :SUCKERPUNCH,
             :THROATCHOP, :MOONGEISTBEAM, :ASTRALBARRAGE, :KOWTOWCLEAVE]
  deepen  = [:DARKPULSE, :NIGHTDAZE, :MOONGEISTBEAM, :OMINOUSWIND, :ASTRALBARRAGE, :NIGHTSHADE]
  lights  = [:FLASH, :TAILGLOW, :DAZZLINGGLEAM, :LIGHTOFRUIN, :PHOTONGEYSER, :PRISMATICLASER, :LUSTERPURGE,
             :MIRRORSHOT, :FLASHCANNON, :LUMINACRASH, :AURORABEAM, :SIGNALBEAM]
  beams   = lights - [:FLASH, :TAILGLOW]
  stars   = { :SWIFT => 1.5, :METEORMASH => 1.3, :METEORBEAM => 1.3 }
  blind = lambda do |mult|
    { :category => :damaging, :mult => mult,
      :user => { :not_types => [:DARK, :GHOST],
                 :not_abilities => [:KEENEYE, :ILLUMINATE, :MINDSEYE, :COMPOUNDEYES, :NOGUARD] } }
  end
  shadow_rule = lambda do |mult, msg|
    { :moves => shadows, :mult => mult, :message => msg }
  end
  {
    # ---- Stage 1: New Moon ------------------------------------------------------
    :name          => "New Moon",
    :backdrop      => "field_new_moon",
    :family        => :magical,
    :intro_message => "The moon has gone dark over Underveil... Something moves in the shadows.",
    :description   => "A darkness ladder. Creatures of the dark hide and strike from it; stars and true light pierce it. Dark moves deepen it into an Abyss; enough light relights Nadir's lamps.",
    :notes         => ["New Moon (stage 1): Dark x1.5; shadow moves (Dark Pulse, Night Slash, Shadow Ball, Shadow Claw, Sucker Punch, Phantom Force...) x1.2.",
                       "Moves from Pokemon that aren't Dark or Ghost are x0.9 accurate (Keen Eye, Illuminate, Mind's Eye, Compound Eyes, No Guard see fine). Night Daze never misses. Illuminate +1 accuracy on entry.",
                       "Stars and light pierce the dark: Swift x1.5; Meteor Mash, Meteor Beam x1.3; light moves (Dazzling Gleam, Flash Cannon, Photon Geyser...) x1.3. Flash blinds one stage more; Cosmic Power also +1 Sp. Atk.",
                       "Feint Attack and Thief x1.5. Moonlight fails and Moonblast loses its glow (x0.75). The sun can't rise here.",
                       "Dark Void, or 3 deepening moves (Dark Pulse, Night Daze, Moongeist Beam, Ominous Wind, Night Shade...) -> Abyss (stage 2).",
                       "Abyss: Dark x1.5, Ghost x1.3, shadow moves x1.4; light moves x0.75; accuracy x0.8 for those who can't see; Solar Beam and Solar Blade fail. 2 light moves push it back to stage 1.",
                       "3 light moves on the New Moon relight Nadir's gaslamps -> Lamplight (stage 3): Dark x1.2, Fire and Electric x1.2 (the lamps), light moves x1.3, thieves x1.5, normal accuracy; Pickpocket and Frisk +1 Speed on entry. 3 Dark attacks snuff the lamps (stage 1).",
                       "Magical Seed: +1 accuracy and Focus Energy - and it draws the shadows in (New Moon -> Abyss; Lamplight -> New Moon)."],
    :nature_power  => :DARKPULSE,
    :camouflage    => :DARK,
    :secret_power  => 8,
    :type_mods     => { :DARK => 1.5 },
    :type_messages => { :DARK => "{1} struck from the depths of the new moon!" },
    :move_mods     => stars.merge(:MOONBLAST => 0.75, :NIGHTDAZE => 1.3, :FEINTATTACK => 1.5, :THIEF => 1.5),
    :move_messages => { :MOONBLAST   => "With no moon in the sky, {2} lost its glow...",
                        :SWIFT       => "A shower of stars rained down!",
                        :METEORMASH  => "The starfield lent {1} its power!",
                        :METEORBEAM  => "The starfield lent {1} its power!",
                        :FEINTATTACK => "{1} struck from the shadows!",
                        :THIEF       => "{1} pilfered under cover of darkness!" },
    :damage_mods   => [
      shadow_rule.call(1.2, "The shadows gathered around {2}!"),
      { :moves => beams, :mult => 1.3, :message => "{2} pierced the darkness!" }
    ],
    :accuracy_mods => [blind.call(0.9), { :moves => [:NIGHTDAZE], :set => 100 }],
    :move_fails    => [{ :moves => [:MOONLIGHT], :message => "But there is no moon in the sky tonight..." }],
    :move_stat_boosts => [
      { :moves => [:FLASH], :target_stats => { :ACCURACY => -1 }, :message => "The sudden flash was blinding in the dark!" },
      { :moves => [:COSMICPOWER], :user_stats => { :SPECIAL_ATTACK => 1 }, :message => "{1} drew power from the cold stars!" }
    ],
    :on_entry      => [
      { :battlers => { :abilities => [:ILLUMINATE] }, :stats => { :ACCURACY => 1 }, :message => "{1}'s glow lit up the darkness!" }
    ],
    :weather       => { :block => [:Sun, :HarshSun], :block_message => "The new moon swallowed the sunlight!" },
    :transitions   => [
      { :moves => [:DARKVOID], :even_if_failed => true, :stage => 2, :message => "Straight into the abyss! The darkness swallows everything!" },
      { :moves => deepen, :uses => 3, :stage => 2,
        :progress_message => "The shadows grow... ({1} more)",
        :message => "The shadows swallowed the stars! The new moon deepened into an abyss!" },
      { :moves => lights, :uses => 3, :stage => 3, :even_if_failed => true,
        :progress_message => "Light pierces the darkness... ({1} more)",
        :message => "Light floods the Underveil! The gaslamps of Nadir flicker back to life!" }
    ],
    :seed => { :item => :MAGICALSEED, :stats => { :ACCURACY => 1 }, :effects => [:focus_energy],
               :message => "{1}'s {2} sharpened its night vision!",
               :proc => proc { |battle, battler| battle.set_field_stage(2, "The seed drew the shadows in! The darkness deepens into an abyss!") } },
    :stages => {
      # ---- Stage 2: Abyss --------------------------------------------------------
      2 => {
        :backdrop      => "field_new_moon_abyss",
        :intro_message => "In an endless sea of darkness, even the stars have gone out...",
        :description   => "Abyss: the darkness is total. Shadows strike hard, light barely carries, the blind can hardly aim.",
        :type_mods     => { :DARK => 1.5, :GHOST => 1.3 },
        :type_messages => { :DARK  => "{1} struck from inside the abyss!",
                            :GHOST => "The ghosts thickened in the dark around {1}!" },
        :move_mods     => { :MOONBLAST => 0.75, :NIGHTDAZE => 1.3, :FEINTATTACK => 1.5, :THIEF => 1.5 },
        :move_messages => { :MOONBLAST => "With no moon in the sky, {2} lost its glow..." },
        :damage_mods   => [
          shadow_rule.call(1.4, "The abyss poured into {2}!"),
          { :moves => beams, :mult => 0.75, :message => "The abyss swallowed most of the light..." }
        ],
        :accuracy_mods => [blind.call(0.8), { :moves => [:NIGHTDAZE], :set => 100 }],
        :move_fails    => [
          { :moves => [:MOONLIGHT], :message => "But there is no moon in the sky tonight..." },
          { :moves => [:SOLARBEAM, :SOLARBLADE], :message => "There isn't a glimmer of light for {1} to gather!" }
        ],
        :transitions   => [
          { :moves => lights, :uses => 2, :stage => 1, :even_if_failed => true,
            :progress_message => "A single ray of light makes its way... ({1} more)",
            :message => "The shadows retreat! The stars glimmer over Underveil again." }
        ],
        :seed => { :item => :MAGICALSEED, :stats => { :ACCURACY => 1 }, :effects => [:focus_energy],
                   :message => "{1}'s {2} sharpened its night vision!" }
      },
      # ---- Stage 3: Lamplight ---------------------------------------------------
      3 => {
        :backdrop      => "field_new_moon_lamplight",
        :intro_message => "The gaslamps of Nadir burn in the dark...",
        :description   => "Lamplight: the undercity's lamps are lit. Lamplighters' fire and current flare, thieves work the shadows between the lamps.",
        :type_mods     => { :DARK => 1.2, :FIRE => 1.2, :ELECTRIC => 1.2 },
        :type_messages => { :DARK => "{1} slipped through the shadows between the lamps!",
                            :FIRE => "The gaslamps flared with {2}!",
                            :ELECTRIC => "The lamp wires crackled with {2}!" },
        :move_mods     => { :THIEF => 1.5, :COVET => 1.5, :FEINTATTACK => 1.5, :KNOCKOFF => 1.2 },
        :move_messages => { :THIEF => "{1} worked the shadows between the lamps!",
                            :COVET => "{1} worked the shadows between the lamps!" },
        :damage_mods   => [{ :moves => beams, :mult => 1.3, :message => "{2} blazed under the lamps!" }],
        :accuracy_mods => [],
        :move_fails    => [],
        :move_stat_boosts => [],
        :on_entry      => [
          { :battlers => { :abilities => [:PICKPOCKET, :FRISK] }, :stats => { :SPEED => 1 },
            :message => "{1} slipped into the crowd under the lamps!" }
        ],
        :transitions   => [
          { :types => [:DARK], :category => :damaging, :uses => 3, :stage => 1,
            :progress_message => "The lamps are guttering... ({1} more)",
            :message => "The lamps went out one by one... The new moon reclaims Underveil." }
        ],
        :seed => { :item => :MAGICALSEED, :stats => { :ACCURACY => 1 }, :effects => [:focus_energy],
                   :message => "{1}'s {2} sharpened its night vision!",
                   :proc => proc { |battle, battler| battle.set_field_stage(1, "The seed drew the shadows in! The lamps gutter out!") } }
      }
    }
  }
end).call)
