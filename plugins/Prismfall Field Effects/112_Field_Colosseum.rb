#===============================================================================
# COLOSSEUM - Gym 8 (Fighting), Ironreach in Nadir, the City Below. A sand pit
# ringed by chain-link in an old mine shaft; the crowd decides who is a hero.
# Kaito's code is "discipline over rage": focus is rewarded, hiding is not.
# Two knockouts whip the crowd into stage 2 "Frenzy"; stalling bores it back.
# Three quakes bring the old mine shaft down (CAVE). Family: Synthetic.
#===============================================================================
FieldEffects.register(:COLOSSEUM, (lambda do
  kicks  = [:DOUBLEKICK, :JUMPKICK, :HIGHJUMPKICK, :LOWKICK, :ROLLINGKICK, :MEGAKICK, :TRIPLEKICK, :TRIPLEAXEL,
            :BLAZEKICK, :TROPKICK, :THUNDEROUSKICK, :AXEKICK, :LOWSWEEP, :PYROBALL]
  throws = [:CIRCLETHROW, :STORMTHROW, :VITALTHROW, :DRAGONTAIL, :SUBMISSION, :SEISMICTOSS]
  quakes = [:EARTHQUAKE, :MAGNITUDE, :BULLDOZE, :FISSURE, :HEADLONGRUSH]
  stalling = [:PROTECT, :DETECT, :REST, :RECOVER, :SLACKOFF, :SUBSTITUTE, :SPIKYSHIELD, :KINGSSHIELD]

  # Knockouts: the crowd rewards the finisher (+1 to the stat the blow used) and keeps count.
  crowd_hook = proc { |battle, user, targets, move, num_hits|
    next if user.lastMoveFailed || user.fainted? || !move.damagingMove?
    kos = targets.count { |t| t.index != user.index && t.damageState.fainted }
    next if kos == 0
    FieldEffects.state(battle)[:kos] = (FieldEffects.state(battle)[:kos] || 0) + kos
    stat = (move.physicalMove?(move.calcType)) ? :ATTACK : :SPECIAL_ATTACK
    next if !user.pbCanRaiseStatStage?(stat, user)
    battle.pbDisplay(FieldEffects.format("The crowd went wild for {1}!", user.pbThis))
    user.pbRaiseStatStage(stat, 1, user)
  }
  fighting_rules = lambda do |strike, underdog|
    [
      { :flags => ["Punching"], :category => :damaging, :mult => strike },
      { :moves => kicks, :mult => strike },
      { :moves => throws, :category => :damaging, :mult => 1.5, :message => "{1} slammed its foe into the cage!" },
      { :category => :damaging, :final_mult => underdog, :user => { :hp_below => 1/3r },
        :message => "The crowd rallied behind {1}!" },
      { :types => [:PSYCHIC], :category => :special, :mult => 0.8, :message => "The crowd jeered at {1}'s mind games!" }
    ]
  end
  {
    :name          => "Colosseum",
    :backdrop      => "field_colosseum",
    :family        => :synthetic,
    :intro_message => "The crowd roars as the fighters enter the pit!",
    :description   => "The crowd decides: punches, kicks and throws land harder, knockouts are rewarded, underdogs are cheered and mind games booed. No hiding, no running.",
    :notes         => ["Fighting x1.2 (x1.5 in a Frenzy). Punching moves and kicks x1.2 (x1.3 in a Frenzy); throws into the cage (Circle Throw, Storm Throw, Vital Throw, Dragon Tail, Submission, Seismic Toss) x1.5.",
                       "Focus Punch x1.5; Revenge, Payback, Retaliate, Avalanche, Lash Out, Reversal x1.3; Beat Up, Fell Stinger, Pay Day x2 (the crowd throws coins).",
                       "The crowd: knocking out a foe gives +1 Attack (physical finisher) or Sp. Atk (special). An underdog at 1/3 HP or less deals x1.2 (x1.3 in a Frenzy). Special Psychic mind games are booed (x0.8).",
                       "Inner Focus and Steadfast: +1 critical-hit stage. Focus Blast x1.2 accuracy. Focus Energy also +1 Attack; No Retreat also +1 Speed; Sand Attack drops accuracy one stage more.",
                       "No Guard and Justified +1 Attack, Battle Armor and Shell Armor +1 Defense on entry.",
                       "Double Team and Minimize fail (nowhere to hide); Roar and Whirlwind fail (no one leaves the pit).",
                       "Frenzy (stage 2): after 2 knockouts. Every attack +1 critical-hit stage. 2 stalling moves (Protect, Recover, Rest, Substitute...) calm the crowd again.",
                       "3 quakes bring the old mine shaft down -> Cave.",
                       "Synthetic Seed: +1 Attack and Focus Energy, but the crowd's roar Taunts the holder."],
    :nature_power  => :BRICKBREAK,
    :camouflage    => :FIGHTING,
    :secret_power  => 7,
    :type_mods     => { :FIGHTING => 1.2 },
    :type_messages => { :FIGHTING => "The pit erupted as {1} pressed the attack!" },
    :move_mods     => { :FOCUSPUNCH => 1.5, :REVENGE => 1.3, :PAYBACK => 1.3, :RETALIATE => 1.3, :AVALANCHE => 1.3,
                        :LASHOUT => 1.3, :REVERSAL => 1.3, :BEATUP => 2.0, :FELLSTINGER => 2.0, :PAYDAY => 2.0 },
    :move_messages => { :FOCUSPUNCH => "{1} struck with perfect discipline!",
                        :REVENGE    => "The crowd loves a comeback!",
                        :RETALIATE  => "The crowd loves a comeback!",
                        :REVERSAL   => "The crowd loves a comeback!",
                        :PAYDAY     => "The crowd showered the pit with coins!",
                        :BEATUP     => "The whole gang piled in!" },
    :damage_mods   => fighting_rules.call(1.2, 1.2),
    :accuracy_mods => [{ :moves => [:FOCUSBLAST], :mult => 1.2 }],
    :crit_mods     => [{ :category => :damaging, :user => { :abilities => [:INNERFOCUS, :STEADFAST] }, :add => 1 }],
    :move_stat_boosts => [
      { :moves => [:FOCUSENERGY], :user_stats => { :ATTACK => 1 }, :message => "{1} steadied its breathing..." },
      { :moves => [:NORETREAT], :user_stats => { :SPEED => 1 }, :message => "The crowd stamped for {1}'s last stand!" },
      { :moves => [:SANDATTACK], :target_stats => { :ACCURACY => -1 }, :message => "{1} kicked up a cloud of arena sand!" }
    ],
    :move_fails    => [
      { :moves => [:DOUBLETEAM, :MINIMIZE], :message => "There's nowhere to hide in the pit!" },
      { :moves => [:ROAR, :WHIRLWIND], :message => "The crowd won't let anyone leave the pit!" }
    ],
    :on_entry      => [
      { :battlers => { :abilities => [:NOGUARD, :JUSTIFIED] }, :stats => { :ATTACK => 1 },
        :message => "The crowd chanted for {1}!" },
      { :battlers => { :abilities => [:BATTLEARMOR, :SHELLARMOR] }, :stats => { :DEFENSE => 1 },
        :message => "{1} squared up in its armor!" }
    ],
    :hooks         => { :after_move => crowd_hook },
    :transitions   => [
      { :check => proc { |battle|
          st = FieldEffects.state(battle)
          next false if (st[:kos] || 0) < 2
          st[:kos] = 0   # the next Frenzy needs two fresh knockouts
          true
        }, :stage => 2,
        :message => "Two down! The crowd is in a frenzy!" },
      { :moves => quakes, :to => :CAVE, :uses => 3,
        :progress_message => "Dust rains from the old mine shaft... ({1} more)",
        :message => "The old mine shaft gave way! The pit caved in!" }
    ],
    :seed => { :item => :SYNTHETICSEED, :stats => { :ATTACK => 1 }, :effects => [:focus_energy, :taunt],
               :message => "{1}'s {2} fired it up to the roar of the crowd!" },
    :stages => {
      2 => {
        :intro_message => "The crowd is in a frenzy!",
        :description   => "Frenzy: the crowd is wild - every attack is likelier to crit and the fighters hit harder.",
        :type_mods     => { :FIGHTING => 1.5 },
        :damage_mods   => fighting_rules.call(1.3, 1.3),
        :crit_mods     => [{ :category => :damaging, :add => 1 },
                           { :category => :damaging, :user => { :abilities => [:INNERFOCUS, :STEADFAST] }, :add => 1 }],
        :transitions   => [
          { :moves => stalling, :stage => 1, :uses => 2, :even_if_failed => true,
            :progress_message => "The crowd is losing interest... ({1} more)",
            :message => "The crowd settled back into its seats." },
          { :moves => quakes, :to => :CAVE, :uses => 3,
            :progress_message => "Dust rains from the old mine shaft... ({1} more)",
            :message => "The old mine shaft gave way! The pit caved in!" }
        ]
      }
    }
  }
end).call)
