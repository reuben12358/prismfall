#===============================================================================
# Prismfall Z-Power - 003 Choosing and unleashing Z-moves
#-------------------------------------------------------------------------------
# Battle#pbRegisterMove is the one place every move choice goes through: the
# player's Fight menu (Essentials and Elite Battle DX), the AI, and the AI
# playing the player's side (controlPlayer). After a move is registered:
#   * the player is asked "Unleash its Z-Power?" when the move can become a
#     Z-move (Yes/No box; the Fight menu stays as it is)
#   * the AI turns any eligible move it chose into the Z-move; its move scores
#     already favour eligible moves (Battle::AI#pbGetMoveScores below)
# The choice then carries the Z-move object, so priority, targeting and the
# move's use all see the Z-move. The Z-Power is spent when the Z-move is
# actually unleashed (a flinch or sleep keeps it), once per trainer per battle.
#===============================================================================
module PrismfallZ
  # [battler index, Z-move id, base move id] for each Z-move unleashed (tests read it).
  def self.log(battle)
    battle.instance_variable_set(:@prism_z_log, []) if !battle.instance_variable_get(:@prism_z_log)
    return battle.instance_variable_get(:@prism_z_log)
  end

  def self.used(battle)
    battle.instance_variable_set(:@prism_z_used, {}) if !battle.instance_variable_get(:@prism_z_used)
    return battle.instance_variable_get(:@prism_z_used)
  end

  def self.owner_key(battle, idx)
    return [idx & 1, battle.pbGetOwnerIndexFromBattlerIndex(idx)]
  end

  def self.used?(battle, idx)
    return !!used(battle)[owner_key(battle, idx)]
  end

  # The Z-move this battler's held crystal makes of move, or nil.
  def self.zmove_for(battler, move)
    return nil if !battler || !move || !move.id || move.prism_zmove?
    item = battler.item_id
    return nil if !item
    if (ex = EXCLUSIVE[item])
      return nil if !battler.isSpecies?(ex[:species]) || move.id != ex[:move]
      return ex[:zmove]
    end
    type = CRYSTALS[item]
    return nil if !type || !move.damagingMove? || move.type != type
    return TYPE_ZMOVES[type]
  end

  # True if this battler's trainer may unleash Z-Power this turn.
  def self.can_use?(battle, idx)
    b = battle.battlers[idx]
    return false if !b || b.fainted?
    return false if battle.wildBattle? && battle.opposes?(idx)     # wild Pokemon don't
    return false if used?(battle, idx)
    return false if b.effects[PBEffects::Encore] > 0
    if battle.pbOwnedByPlayer?(idx)
      return false if !$bag || !$bag.has?(RING)
    end
    # Only one Z-move per trainer: a partner who already chose one this turn blocks it.
    key = owner_key(battle, idx)
    battle.allBattlers.each do |o|
      next if o.index == idx || owner_key(battle, o.index) != key
      c = battle.choices[o.index]
      return false if c && c[0] == :UseMove && c[2] && c[2].prism_zmove?
    end
    return true
  end

  def self.build(battle, base_move, zid)
    z = Battle::Move.from_pokemon_move(battle, Pokemon::Move.new(zid))
    return z.prism_attach(base_move)
  end

  # Called by Battle#pbRegisterMove once a move is registered.
  def self.after_register(battle, idx, idx_move, show_messages)
    b = battle.battlers[idx]
    move = b.moves[idx_move]
    zid = zmove_for(b, move)
    return if !zid || !GameData::Move.exists?(zid) || !can_use?(battle, idx)
    player_menu = battle.pbOwnedByPlayer?(idx) && !battle.controlPlayer && show_messages
    if player_menu
      zname = GameData::Move.get(zid).name
      return if !battle.pbDisplayConfirm(_INTL("Unleash {1}'s Z-Power? ({2} becomes {3})", b.name, move.name, zname))
    else
      return if !ai_wants?(battle, b, move, zid)
    end
    battle.choices[idx][2] = build(battle, move, zid)
  end

  def self.ai_wants?(battle, b, move, zid)
    return evoboost_worth_it?(b) if zid == :EXTREMEEVOBOOST
    return true
  end

  def self.evoboost_worth_it?(b)
    stages = [:ATTACK, :DEFENSE, :SPECIAL_ATTACK, :SPECIAL_DEFENSE, :SPEED].sum { |s| b.stages[s] }
    return stages < 6 && b.hp * 2 >= b.totalhp
  end

  # Battle::AI#pbGetMoveScores: choices are [idxMove, score, idxTarget, ...].
  def self.ai_adjust(battle, b, choices)
    return if !b || !can_use?(battle, b.index)
    choices.each do |c|
      move = b.moves[c[0]]
      zid = zmove_for(b, move)
      next if !zid
      if zid == :EXTREMEEVOBOOST
        c[1] = [c[1], AI_EVOBOOST_SCORE].max if evoboost_worth_it?(b)
      elsif c[1] >= Battle::AI::MOVE_BASE_SCORE
        c[1] = (c[1] * AI_DAMAGING_MULT).round
      end
    end
  end

  # The Z-move has passed every "can it move?" check: spend the Z-Power.
  def self.on_unleash(battle, user, z)
    base = z.prism_base
    used(battle)[owner_key(battle, user.index)] = true
    log(battle).push([user.index, z.id, base ? base.id : nil])
    battle.pbDisplay(_INTL("{1} surrounded itself with its Z-Power!", user.pbThis))
    battle.pbDisplay(_INTL("{1} unleashed its full-force Z-Move!", user.pbThis))
    if base
      user.pbSetPP(base, base.pp - 1) if base.pp > 0 && base.total_pp > 0
      # Encore, Disable, Choice lock, Copycat and Last Resort see the base move.
      user.instance_variable_set(:@lastMoveUsed, base.id)
      user.instance_variable_set(:@lastRegularMoveUsed, base.id) if user.lastRegularMoveUsed == z.id
      mu = user.instance_variable_get(:@movesUsed)
      if mu
        mu.delete(z.id)
        mu.push(base.id) if !mu.include?(base.id)
      end
      battle.lastMoveUsed = base.id if battle.lastMoveUsed == z.id
    end
    EventHandlers.trigger(:prismfall_zmove_unleashed, battle, user, z)
  end

  # True if target is behind a Protect-style move this turn.
  PROTECT_EFFECTS = [:Protect, :KingsShield, :SpikyShield, :BanefulBunker, :Obstruct, :SilkTrap, :BurningBulwark].freeze
  def self.protecting?(target)
    return false if !target
    PROTECT_EFFECTS.each do |e|
      next if !PBEffects.const_defined?(e)
      return true if target.effects[PBEffects.const_get(e)]
    end
    return true if PBEffects.const_defined?(:MatBlock) && target.pbOwnSide.effects[PBEffects::MatBlock]
    return false
  end
end

class Battle
  alias prismfall_z_pbRegisterMove pbRegisterMove unless method_defined?(:prismfall_z_pbRegisterMove)
  def pbRegisterMove(idxBattler, idxMove, showMessages = true)
    ret = prismfall_z_pbRegisterMove(idxBattler, idxMove, showMessages)
    PBDebug.logonerr { PrismfallZ.after_register(self, idxBattler, idxMove, showMessages) } if ret
    return ret
  end
end

class Battle::AI
  alias prismfall_z_pbGetMoveScores pbGetMoveScores unless method_defined?(:prismfall_z_pbGetMoveScores)
  def pbGetMoveScores
    choices = prismfall_z_pbGetMoveScores
    PBDebug.logonerr { PrismfallZ.ai_adjust(@battle, @user.battler, choices) } if choices.is_a?(Array)
    return choices
  end
end

# After the whole move has resolved: :prismfall_zmove_done (field hooks use it).
class Battle::Battler
  alias prismfall_z_pbUseMove pbUseMove unless method_defined?(:prismfall_z_pbUseMove)
  def pbUseMove(choice, specialUsage = false)
    z = choice[2]
    prismfall_z_pbUseMove(choice, specialUsage)
    if z && z.prism_zmove? && z.prism_executed
      EventHandlers.trigger(:prismfall_zmove_done, @battle, self, z)
    end
  end
end
