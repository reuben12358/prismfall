#===============================================================================
# COLOSSEUM - Gym 8 (Fighting), Ironreach in Nadir, the City Below. A sand pit
# ringed by chain-link in an old mine shaft; the crowd decides who is a hero.
# Kaito's code is "discipline over rage": focus is rewarded, hiding is not.
#===============================================================================
FieldEffects.register(:COLOSSEUM, {
  :name          => "Colosseum",
  :backdrop      => "field_colosseum",
  :intro_message => "The crowd roars as the fighters enter the pit!",
  :description   => "Punches, kicks and throws hit harder; the crowd cheers knockouts and rallies behind the underdog. No hiding, no running.",
  :nature_power  => :BRICKBREAK,
  :camouflage    => :FIGHTING,
  :secret_power  => 7,
  :type_mods     => { :FIGHTING => 1.2 },
  :move_mods     => { :FOCUSPUNCH => 1.5, :REVENGE => 1.3, :PAYBACK => 1.3, :RETALIATE => 1.3,
                      :AVALANCHE => 1.3, :LASHOUT => 1.3 },
  :move_messages => { :FOCUSPUNCH => "{1} struck with perfect discipline!",
                      :REVENGE    => "The crowd loves a comeback!",
                      :RETALIATE  => "The crowd loves a comeback!" },
  :damage_mods   => [
    # Strikes: every punch and kick plays to the crowd (elemental punches too)
    { :flags => ["Punching"], :category => :damaging, :mult => 1.2 },
    { :moves => [:DOUBLEKICK, :JUMPKICK, :HIGHJUMPKICK, :LOWKICK, :ROLLINGKICK, :MEGAKICK,
                 :TRIPLEKICK, :TRIPLEAXEL, :BLAZEKICK, :TROPKICK, :THUNDEROUSKICK, :AXEKICK,
                 :LOWSWEEP, :PYROBALL], :mult => 1.2 },
    # Throws into the chain-link fence
    { :moves => [:CIRCLETHROW, :STORMTHROW, :VITALTHROW, :DRAGONTAIL, :SUBMISSION], :mult => 1.5,
      :message => "{1} slammed its foe into the cage!" },
    # The underdog: at 1/3 HP or less, the crowd rallies behind you
    { :category => :damaging, :final_mult => 1.2,
      :user => { :condition => proc { |battle, b| b.hp * 3 <= b.totalhp } },
      :message => "The crowd rallied behind {1}!" }
  ],
  :accuracy_mods => [{ :moves => [:FOCUSBLAST], :mult => 1.2 }],
  :crit_mods     => [
    { :category => :damaging, :user => { :abilities => [:INNERFOCUS, :STEADFAST] }, :add => 1 }
  ],
  :move_stat_boosts => [
    { :moves => [:FOCUSENERGY], :user_stats => { :ATTACK => 1 },
      :message => "{1} steadied its breathing..." },
    { :moves => [:SANDATTACK], :target_stats => { :ACCURACY => -1 },
      :message => "{1} kicked up a cloud of arena sand!" }
  ],
  :move_fails    => [
    { :moves => [:DOUBLETEAM, :MINIMIZE], :message => "There's nowhere to hide in the pit!" },
    { :moves => [:ROAR, :WHIRLWIND], :message => "The crowd won't let anyone leave the pit!" }
  ],
  :hooks         => {
    # Knockouts whip the crowd into a frenzy: +1 to the stat the finishing blow used
    :after_move => proc { |battle, user, targets, move, num_hits|
      next if user.lastMoveFailed || user.fainted? || !move.damagingMove?
      next if targets.none? { |t| t.index != user.index && t.damageState.fainted }
      stat = (move.physicalMove?(move.calcType)) ? :ATTACK : :SPECIAL_ATTACK
      next if !user.pbCanRaiseStatStage?(stat, user)
      battle.pbDisplay(FieldEffects.format("The crowd went wild for {1}!", user.pbThis))
      user.pbRaiseStatStage(stat, 1, user)
    }
  },
  :seed => { :item => :TELLURICSEED, :stats => { :ATTACK => 1 }, :effects => [:focus_energy],
             :message => "{1}'s {2} fired it up to the roar of the crowd!" }
})
