#===============================================================================
# GRAND_STAGE - Gym 2 (Normal), Saltmere's Pell Playhouse. The show must go on.
# An applause ladder (Rejuvenation's Concert / Reborn's Big Top logic):
#   1 Opening Night -> 2 Encore -> 3 Standing Ovation
# Showpieces (dances, songs, flourishes, critical hits) win the crowd over;
# stalling (Protect, Substitute, Recover, Rest...) loses it. Family: Synthetic.
#===============================================================================
FieldEffects.register(:GRAND_STAGE, (lambda do
  showpieces = [:CELEBRATE, :ENCORE, :FAKEOUT, :ACROBATICS, :LASTRESORT, :PAYDAY, :DRUMBEATING,
                :TEETERDANCE, :SPOTLIGHT, :FLOWERTRICK, :MAKEITRAIN]
  stalling   = [:PROTECT, :DETECT, :SUBSTITUTE, :REST, :RECOVER, :SLACKOFF, :SOFTBOILED, :MILKDRINK,
                :YAWN, :TEATIME, :SPLASH, :ROOST, :ENDURE, :KINGSSHIELD]

  applause = lambda do |up_msg|
    rules = []
    if up_msg
      rules.push(
        { :flags => ["Dance"], :uses => 2, :stage_delta => 1, :even_if_failed => true, :message => up_msg },
        { :flags => ["Sound"], :category => :damaging, :uses => 2, :stage_delta => 1, :message => up_msg },
        { :moves => showpieces, :uses => 2, :stage_delta => 1, :message => up_msg }
      )
    end
    rules.push({ :moves => stalling, :even_if_failed => true, :stage_delta => -1,
                 :message => "The audience is getting restless..." })
    next rules
  end

  # A critical hit brings the house down (one stage up), from the hooks below.
  crit_hook = proc { |battle, user, targets, move, num_hits|
    next if user.lastMoveFailed || !move.damagingMove?
    next if targets.none? { |t| t.damageState.critical }
    st = FieldEffects.stage(battle)
    next if st >= 3
    battle.set_field_stage(st + 1, (st == 1) ? "What a hit! The audience leaps to its feet!" :
                                              "A breathtaking hit! Standing ovation!")
  }

  sound_conf = { :flags => ["Sound"], :category => :damaging, :chance => 10, :confuse => true,
                 :message => "{1} was dazzled by the roar of the crowd!" }
  dance_boost = { :flags => ["Dance"], :category => :status, :user_stats => { :SPEED => 1 },
                  :message => "The audience cheered {1}'s performance!" }
  celebrate = { :moves => [:CELEBRATE], :user_stats => { :ATTACK => 1, :DEFENSE => 1, :SPECIAL_ATTACK => 1,
                                                          :SPECIAL_DEFENSE => 1, :SPEED => 1 },
                :message => "A standing ovation for {1}!" }
  charm = { :moves => [:CHARM, :CAPTIVATE, :TEARFULLOOK, :BABYDOLLEYES], :target_stats => { :SPECIAL_ATTACK => -1 },
            :message => "{1} won the crowd over!" }
  stage_mods = lambda do |normal, show|
    {
      :type_mods   => { :NORMAL => normal },
      :damage_mods => [
        { :flags => ["Sound"], :category => :damaging, :mult => show, :message => "{2} rang through the opera house!" },
        { :flags => ["Dance"], :category => :damaging, :mult => show, :message => "The spotlight followed {1}'s dance!" },
        { :flags => ["Sound"], :user => { :abilities => [:PUNKROCK, :LIQUIDVOICE] }, :mult => 1.2 }
      ]
    }
  end

  {
    # ---- Stage 1: Opening Night ---------------------------------------------
    :name          => "Grand Stage",
    :backdrop      => "field_grand_stage",
    :family        => :synthetic,
    :intro_message => "The curtain rises! The spotlight blazes over the stage!",
    :description   => "An opera house that plays to the crowd: songs, dances and showpieces build applause in three stages; stalling bores it.",
    :notes         => ["Applause has 3 stages: Opening Night, Encore, Standing Ovation. Starts at 1.",
                       "Up a stage: 2 dances, 2 damaging sound moves, 2 showpieces (Fake Out, Acrobatics, Pay Day, Celebrate, Encore...), or any critical hit.",
                       "Down a stage: stalling - Protect, Detect, Substitute, Recover, Rest, Yawn, Roost, Splash...",
                       "Normal x1.3 / x1.5 / x1.5. Damaging sound and dance moves x1.3 / x1.4 / x1.5 (Punk Rock, Liquid Voice x1.2 more).",
                       "Pay Day x2; Acrobatics, Drum Beating, Fake Out x1.5; Last Resort x1.3. Sound moves may dazzle (10% confusion).",
                       "Status dances also give +1 Speed; Celebrate raises every stat; Charm-style moves also lower Sp. Atk. Encore lasts 2 turns longer.",
                       "Standing Ovation: every attack +1 critical-hit stage, Sing never misses, Normal types and Dancers bask in applause (1/16 HP).",
                       "Dancer +1 Speed, Punk Rock / Liquid Voice +1 Sp. Atk on entry. Indoors: no weather.",
                       "Synthetic Seed: +1 Speed and Laser Focus, but the spotlight Taunts the holder."],
    :nature_power  => :HYPERVOICE,
    :camouflage    => :NORMAL,
    :secret_power  => 0,
    :type_mods     => stage_mods.call(1.3, 1.3)[:type_mods],
    :type_messages => { :NORMAL => "The crowd roared for {1}!" },
    :move_mods     => { :PAYDAY => 2.0, :ACROBATICS => 1.5, :DRUMBEATING => 1.5, :FAKEOUT => 1.5,
                        :LASTRESORT => 1.3 },
    :move_messages => { :PAYDAY      => "Coins rained down onto the stage!",
                        :ACROBATICS  => "{1} dazzled the audience with acrobatics!",
                        :DRUMBEATING => "The drums thundered through the hall!",
                        :FAKEOUT     => "{1} opened with a flourish!",
                        :LASTRESORT  => "The grand finale!" },
    :damage_mods   => stage_mods.call(1.3, 1.3)[:damage_mods],
    :accuracy_mods => [{ :moves => [:SING, :GRASSWHISTLE, :SUPERSONIC, :METALSOUND], :mult => 1.3 }],
    :added_effects => [sound_conf],
    :move_stat_boosts => [dance_boost, celebrate, charm],
    :on_entry      => [
      { :battlers => { :abilities => [:DANCER] }, :stats => { :SPEED => 1 }, :message => "{1} took center stage!" },
      { :battlers => { :abilities => [:PUNKROCK, :LIQUIDVOICE] }, :stats => { :SPECIAL_ATTACK => 1 },
        :message => "{1} warmed up its voice for the crowd!" }
    ],
    :effect_durations => { :ENCORE => [2, "The audience demands an encore!"] },
    :weather       => { :block => [:Sun, :Rain, :Sandstorm, :Hail],
                        :block_message => "The opera house roof keeps the weather out!" },
    :hooks         => { :after_move => crit_hook },
    :transitions   => applause.call("The audience is warming up! Encore!"),
    :seed => { :item => :SYNTHETICSEED, :stats => { :SPEED => 1 }, :effects => [:laser_focus, :taunt],
               :message => "{1}'s {2} put it in the spotlight! It's here to perform!" },
    :stages => {
      # ---- Stage 2: Encore ---------------------------------------------------
      2 => {
        :backdrop      => "field_grand_stage_2",
        :intro_message => "The audience calls for an encore!",
        :type_mods     => stage_mods.call(1.5, 1.4)[:type_mods],
        :damage_mods   => stage_mods.call(1.5, 1.4)[:damage_mods],
        :transitions   => applause.call("Standing ovation! The whole house is on its feet!")
      },
      # ---- Stage 3: Standing Ovation ----------------------------------------
      3 => {
        :backdrop      => "field_grand_stage_3",
        :intro_message => "Standing ovation! The whole house is on its feet!",
        :type_mods     => stage_mods.call(1.5, 1.5)[:type_mods],
        :damage_mods   => stage_mods.call(1.5, 1.5)[:damage_mods],
        :accuracy_mods => [{ :moves => [:SING], :always_hit => true },
                           { :moves => [:GRASSWHISTLE, :SUPERSONIC, :METALSOUND], :mult => 1.3 }],
        :crit_mods     => [{ :category => :damaging, :add => 1 }],
        :end_of_round  => [
          { :battlers => { :types => [:NORMAL] }, :heal => 1/16r, :message => "{1} basked in the applause." },
          { :battlers => { :abilities => [:DANCER], :not_types => [:NORMAL] }, :heal => 1/16r,
            :message => "{1} basked in the applause." }
        ],
        :transitions   => applause.call(nil)
      }
    }
  }
end).call)
