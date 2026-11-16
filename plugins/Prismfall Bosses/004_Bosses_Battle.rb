#===============================================================================
# Prismfall Bosses - 004 Battle-layer hooks (work with or without EBDX)
#
# How a bar breaks: any HP loss that would take a boss with bars left to 0
# stops at 1 HP and marks the bar :pending (the excess is discarded - no
# overflow). Further damage is absorbed until the break resolves at the next
# safe point: after a move (pbUseMove), after effect damage
# (pbTakeEffectDamage), at the end of the round, or before pbJudge. Resolving
# shows the break, refills HP and runs the on-break script (005).
#===============================================================================
module Prismfall
  module Bosses
    def self.reduce_hp(battler, st, amt, anim, register, any_anim)
      amt_i = amt.round
      ds    = battler.damageState
      from_move = !anim && !any_anim && ds && ds.hpLost == amt_i   # pbInflictHPDamage
      if st.pending || (st.defeated && st.end_decision && battler.hp > 0)   # depleted: absorb until it resolves
        st.overflow += [amt_i, 0].max
        if from_move
          ds.totalHPLost -= ds.hpLost
          ds.hpLost = 0
        end
        return 0
      end
      hp = battler.hp
      return battler.prismfall_bosses_pbReduceHP(amt, anim, register, any_anim) if hp <= 0 || amt_i < hp
      if !st.last_bar?
        st.pending = :break
      else
        defeat = survive_defeat_effects(battler.battle, battler, st)
        return battler.prismfall_bosses_pbReduceHP(amt, anim, register, any_anim) if !defeat
        st.pending = :defeat
        st.pending_defeat = defeat
      end
      st.overflow += amt_i - hp
      lost = 0
      if hp > 1
        lost = battler.prismfall_bosses_pbReduceHP(hp - 1, anim, register, any_anim)
      elsif register
        battler.tookDamageThisRound = true if battler.respond_to?(:tookDamageThisRound=)
      end
      if from_move
        ds.totalHPLost -= (ds.hpLost - lost)
        ds.hpLost = lost
      end
      PBDebug.log("[Prismfall Bosses] #{battler.pbThis} bar depleted (#{st.pending}); overflow #{amt_i - hp} discarded")
      return lost
    end

    def self.status_blocked?(battler, status, user = nil)
      st = state_for(battler)
      return false if !st
      return false if user && user.index == battler.index   # Rest, Flame Orb...
      return st.immune_to?(status)
    end

    def self.show_immune(battler)
      battler.battle.pbDisplay(text(IMMUNE_MESSAGE, battler.pbThis))
    end

    # Battle start / entry: intro text, catch rule, EBDX immunity handover.
    def self.on_enter(battle, battler)
      st = state_for(battler)
      return if !st || st.intro_shown
      st.intro_shown = true
      battler.immunity = false if battler.respond_to?(:immunity=)   # we own immunities, not EBDX's metrics
      if battle.wildBattle?
        battle.instance_variable_set(:@prismfall_bosses_balls, battle.disablePokeBalls) if !battle.instance_variable_defined?(:@prismfall_bosses_balls)
        update_ball_rule(battle, st)
      end
      apply_prism_interval(battle)
      Array(resolve(st.data[:intro])).each { |m| battle.pbDisplay(text(m, battler.pbThis)) }
      EventHandlers.trigger(:prismfall_boss_entered, battle, battler, st.id)
    end

    def self.update_ball_rule(battle, st)
      return if !battle.wildBattle? || !battle.respond_to?(:disablePokeBalls=)
      base = battle.instance_variable_get(:@prismfall_bosses_balls)
      battle.disablePokeBalls = (st.catchable?) ? base : true
    end

    # Best-skill AI for wild bosses.
    def self.wild_ai_skill(battle)
      skills = battle.battlers.map do |b|
        next nil if !b || !b.opposes? || !boss_pokemon?(b.pokemon)
        s = resolve(get(b.pokemon.prismfall_boss_id)[:ai_skill])
        (s.is_a?(Integer)) ? s : DEFAULT_AI_SKILL
      end
      return skills.compact.max
    end

    # Pre-scripted moves per bar: :ai_script => { 1 => [:CALMMIND, nil, :JUDGMENT] }
    # (one entry per command phase of that bar; nil = let the AI decide).
    def self.scripted_move(battle, battler)
      st = state_for(battler)
      return nil if !st
      script = resolve(st.data[:ai_script])
      return nil if !script.is_a?(Hash)
      list = Array(resolve(script[st.phase]))
      turn = st.phase_turn
      st.phase_turn += 1
      return nil if list.empty?
      if turn >= list.length
        return nil if !resolve(st.data[:ai_script_loop])
        turn %= list.length
      end
      return list[turn]
    end

    def self.ai_scripted_choice(ai, battle, aiuser, choices)
      return false if !aiuser
      battler = aiuser.battler
      move_id = scripted_move(battle, battler)
      return false if !move_id
      idx = battler.moves.index { |m| m && m.id == move_id }
      return false if !idx || !battle.pbCanChooseMove?(battler.index, idx, false)
      best = choices.select { |c| c[0] == idx }.max_by { |c| c[1] }
      battle.pbRegisterMove(battler.index, idx, false)
      battle.pbRegisterTarget(battler.index, best[2]) if best && best[2] >= 0
      PBDebug.log("[Prismfall Bosses] #{battler.pbThis} uses scripted #{move_id}")
      return true
    end

    def self.record_results(battle)
      states = battle.prismfall_boss_states.values
      return if states.empty?
      list = states.map { |st| st.summary.merge(:decision => battle.decision) }
      @last_result = list.first.merge(:all => list)
      EventHandlers.trigger(:prismfall_boss_battle_ended, battle, @last_result)
    end

    def self.strip_all(battle)
      [0, 1].each { |side| battle.pbParty(side).each { |pkmn| strip(pkmn) } }
    end
  end
end

#===============================================================================
class Battle::Battler
  alias prismfall_bosses_pbReduceHP pbReduceHP unless method_defined?(:prismfall_bosses_pbReduceHP)
  def pbReduceHP(amt, anim = true, registerDamage = true, anyAnim = true)
    st = Prismfall::Bosses.state_for(self)
    return prismfall_bosses_pbReduceHP(amt, anim, registerDamage, anyAnim) if !st
    return Prismfall::Bosses.reduce_hp(self, st, amt, anim, registerDamage, anyAnim)
  end

  alias prismfall_bosses_pbTakeEffectDamage pbTakeEffectDamage unless method_defined?(:prismfall_bosses_pbTakeEffectDamage)
  def pbTakeEffectDamage(amt, show_anim = true, &block)
    prismfall_bosses_pbTakeEffectDamage(amt, show_anim, &block)
    Prismfall::Bosses.process(@battle)
  end

  alias prismfall_bosses_pbUseMove pbUseMove unless method_defined?(:prismfall_bosses_pbUseMove)
  def pbUseMove(choice, specialUsage = false)
    ret = prismfall_bosses_pbUseMove(choice, specialUsage)
    Prismfall::Bosses.process(@battle)
    return ret
  end

  alias prismfall_bosses_pbFaint pbFaint unless method_defined?(:prismfall_bosses_pbFaint)
  def pbFaint(showMessage = true)
    if fainted? && !@fainted && (st = Prismfall::Bosses.state_for(self)) && !st.defeated
      Prismfall::Bosses.run_defeat(@battle, self, st, nil)
    end
    return prismfall_bosses_pbFaint(showMessage)
  end

  # Status immunities while bars remain.
  alias prismfall_bosses_pbCanInflictStatus? pbCanInflictStatus? unless method_defined?(:prismfall_bosses_pbCanInflictStatus?)
  def pbCanInflictStatus?(newStatus, user, showMessages, move = nil, ignoreStatus = false)
    if Prismfall::Bosses.status_blocked?(self, newStatus, user)
      Prismfall::Bosses.show_immune(self) if showMessages
      return false
    end
    return prismfall_bosses_pbCanInflictStatus?(newStatus, user, showMessages, move, ignoreStatus)
  end

  alias prismfall_bosses_pbCanSynchronizeStatus? pbCanSynchronizeStatus? unless method_defined?(:prismfall_bosses_pbCanSynchronizeStatus?)
  def pbCanSynchronizeStatus?(newStatus, user)
    return false if Prismfall::Bosses.status_blocked?(self, newStatus, user)
    return prismfall_bosses_pbCanSynchronizeStatus?(newStatus, user)
  end

  alias prismfall_bosses_pbCanSleepYawn? pbCanSleepYawn? unless method_defined?(:prismfall_bosses_pbCanSleepYawn?)
  def pbCanSleepYawn?
    return false if Prismfall::Bosses.status_blocked?(self, :YAWN) || Prismfall::Bosses.status_blocked?(self, :SLEEP)
    return prismfall_bosses_pbCanSleepYawn?
  end

  alias prismfall_bosses_pbCanConfuse? pbCanConfuse? unless method_defined?(:prismfall_bosses_pbCanConfuse?)
  def pbCanConfuse?(user = nil, showMessages = true, move = nil, selfInflicted = false)
    if !selfInflicted && Prismfall::Bosses.status_blocked?(self, :CONFUSION, user)
      Prismfall::Bosses.show_immune(self) if showMessages
      return false
    end
    return prismfall_bosses_pbCanConfuse?(user, showMessages, move, selfInflicted)
  end

  alias prismfall_bosses_pbCanAttract? pbCanAttract? unless method_defined?(:prismfall_bosses_pbCanAttract?)
  def pbCanAttract?(user, showMessages = true)
    if Prismfall::Bosses.status_blocked?(self, :ATTRACT, user)
      Prismfall::Bosses.show_immune(self) if showMessages
      return false
    end
    return prismfall_bosses_pbCanAttract?(user, showMessages)
  end
end

#===============================================================================
class Battle
  alias prismfall_bosses_pbJudge pbJudge unless method_defined?(:prismfall_bosses_pbJudge)
  def pbJudge
    Prismfall::Bosses.process(self)
    return prismfall_bosses_pbJudge
  end

  alias prismfall_bosses_pbEndOfRoundPhase pbEndOfRoundPhase unless method_defined?(:prismfall_bosses_pbEndOfRoundPhase)
  def pbEndOfRoundPhase
    ret = prismfall_bosses_pbEndOfRoundPhase
    Prismfall::Bosses.process(self)
    return ret
  end

  alias prismfall_bosses_pbOnBattlerEnteringBattle pbOnBattlerEnteringBattle unless method_defined?(:prismfall_bosses_pbOnBattlerEnteringBattle)
  def pbOnBattlerEnteringBattle(battler_index, skip_event_reset = false)
    Array(battler_index).flatten.each do |i|
      b = @battlers[i]
      Prismfall::Bosses.on_enter(self, b) if b && !b.fainted?
    end
    return prismfall_bosses_pbOnBattlerEnteringBattle(battler_index, skip_event_reset)
  end

  alias prismfall_bosses_pbThrowPokeBall pbThrowPokeBall unless method_defined?(:prismfall_bosses_pbThrowPokeBall)
  def pbThrowPokeBall(idxBattler, ball, catch_rate = nil, showPlayer = false)
    target = (opposes?(idxBattler)) ? @battlers[idxBattler] : @battlers[idxBattler].pbDirectOpposing(true)
    target = target.allAllies[0] if target && target.fainted? && target.allAllies[0]
    st = (target && wildBattle?) ? Prismfall::Bosses.state_for(target) : nil
    if st
      if !st.catchable?
        pbDisplayBrief(_INTL("{1} threw a {2}!", pbPlayer.name, GameData::Item.get(ball).name))
        @scene.pbThrowAndDeflect(ball, target.index) if @scene.respond_to?(:pbThrowAndDeflect)
        pbDisplay(Prismfall::Bosses.text(Prismfall::Bosses::BALL_MESSAGE, target.pbThis(true)))
        return
      end
      catch_rate ||= st.catch_rate
    end
    return prismfall_bosses_pbThrowPokeBall(idxBattler, ball, catch_rate, showPlayer)
  end

  alias prismfall_bosses_pbRecordAndStoreCaughtPokemon pbRecordAndStoreCaughtPokemon unless method_defined?(:prismfall_bosses_pbRecordAndStoreCaughtPokemon)
  def pbRecordAndStoreCaughtPokemon
    @caughtPokemon.each { |pkmn| Prismfall::Bosses.strip(pkmn) }
    return prismfall_bosses_pbRecordAndStoreCaughtPokemon
  end

  alias prismfall_bosses_pbEndOfBattle pbEndOfBattle unless method_defined?(:prismfall_bosses_pbEndOfBattle)
  def pbEndOfBattle
    Prismfall::Bosses.record_results(self)
    ret = prismfall_bosses_pbEndOfBattle
    Prismfall::Bosses.strip_all(self)
    return ret
  end
end

#===============================================================================
class Battle::AI::AITrainer
  alias prismfall_bosses_set_up_skill set_up_skill unless method_defined?(:prismfall_bosses_set_up_skill)
  def set_up_skill
    prismfall_bosses_set_up_skill
    return if @trainer || @side != 1
    skill = Prismfall::Bosses.wild_ai_skill(@ai.battle)
    @skill = skill if skill && skill > @skill
  end
end

class Battle::AI
  alias prismfall_bosses_pbChooseMove pbChooseMove unless method_defined?(:prismfall_bosses_pbChooseMove)
  def pbChooseMove(choices)
    return if Prismfall::Bosses.ai_scripted_choice(self, @battle, @user, choices)
    return prismfall_bosses_pbChooseMove(choices)
  end
end
