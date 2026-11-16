#===============================================================================
# Prismfall Core - 005 Level caps
#-------------------------------------------------------------------------------
# Cap = level cap of the first gym whose badge isn't owned (SPINE table).
# With all 18 badges: FESTIVAL_CAP (90), or FESTIVAL_FINALE_CAP (100) once
# Prismfall::LevelCap.unlock_finale! has been called (the Festival manager calls
# it automatically for finale-ruleset stages).
#
# Enforcement (all alias-chained):
#   Battle#pbGainExpOne            no Exp at/above cap; Exp clamped to the cap;
#                                  difficulty Exp multiplier
#   GameData::GrowthRate#add_exp   applies the clamp/multiplier (scoped context)
#   Battle::Battler#pbObedienceCheck?  disobedience above the cap (per mode)
#   Rare Candy / EXP Candy handlers    blocked at cap, quantity limited
#   pbChangeExp                    clamp for EXP Candies (scoped context)
#   DayCare::DayCareSlot#add_exp   Day Care stops at the cap
#   PokemonPauseMenu#pbShowInfo    shows "Level cap / Mode" in the pause menu
#===============================================================================
module Prismfall
  module LevelCap
    @exp_context = nil

    class << self
      attr_reader :exp_context
    end

    def self.max_level
      return GameData::GrowthRate.max_level
    end

    def self.enabled?
      return false if !LEVEL_CAPS_ENABLED
      return false if Prismfall.state.level_caps_disabled
      return true
    end

    def self.finale_unlocked?
      return Prismfall.state.finale_cap_unlocked ? true : false
    end

    # Cap before overrides/difficulty bonus.
    def self.base_cap
      idx = Prismfall.next_gym_index
      return GYMS[idx][:cap] if idx
      return (finale_unlocked?) ? FESTIVAL_FINALE_CAP : FESTIVAL_CAP
    end

    # The active level cap (max level if caps are disabled).
    def self.current
      return max_level if !enabled?
      override = Prismfall.state.level_cap_override
      cap = (override.is_a?(Integer)) ? override : base_cap + (Prismfall::Difficulty.setting(:cap_bonus) || 0)
      return cap.clamp(1, max_level)
    end

    def self.at_cap?(pkmn)
      return false if !pkmn || !enabled?
      return pkmn.level >= current
    end

    # Level above which Pokémon may disobey, or nil if obedience isn't enforced.
    def self.obedience_level
      return nil if !enabled?
      return nil if !Prismfall::Difficulty.setting(:obedience)
      return [current + (Prismfall::Difficulty.setting(:obedience_margin) || 0), max_level].min
    end

    def self.candy_capped?
      return enabled? && !Prismfall::Difficulty.setting(:candy_at_cap)
    end

    def self.exp_capped?
      return enabled? && !Prismfall::Difficulty.setting(:exp_at_cap)
    end

    #---------------------------------------------------------------------------
    # Story controls (event Script calls)
    #---------------------------------------------------------------------------
    # Festival finale: raise the post-Badge-18 cap to FESTIVAL_FINALE_CAP.
    def self.unlock_finale!(announce = false)
      already = finale_unlocked?
      Prismfall.state.finale_cap_unlocked = true
      pbMessage(_INTL("The level cap is now Lv. {1}.", current)) if announce && !already
      return true
    end

    def self.lock_finale!
      Prismfall.state.finale_cap_unlocked = false
    end

    # Force a specific cap (e.g. a story segment). nil clears it.
    def self.set_override(level)
      Prismfall.state.level_cap_override = (level.nil?) ? nil : level.to_i
    end

    def self.clear_override
      set_override(nil)
    end

    def self.disable!; Prismfall.state.level_caps_disabled = true;  end
    def self.enable!;  Prismfall.state.level_caps_disabled = false; end

    #---------------------------------------------------------------------------
    # Display
    #---------------------------------------------------------------------------
    def self.info_text
      cap_text = (enabled?) ? _INTL("Lv. {1}", current) : _INTL("None")
      return _INTL("Level cap: {1}\nMode: {2}", cap_text, Prismfall::Difficulty.label)
    end

    # Event usage: Script: Prismfall::LevelCap.announce
    def self.announce
      if enabled?
        pbMessage(_INTL("The current level cap is Lv. {1}.", current))
      else
        pbMessage(_INTL("There is no level cap right now."))
      end
    end

    #---------------------------------------------------------------------------
    # Scoped Exp context (read by the GrowthRate#add_exp and pbChangeExp hooks)
    #---------------------------------------------------------------------------
    def self.with_exp_context(ceiling, multiplier = nil)
      previous = @exp_context
      @exp_context = { :ceiling => ceiling, :multiplier => multiplier }
      begin
        return yield
      ensure
        @exp_context = previous
      end
    end

    def self.exp_ceiling_for(pkmn, cap = nil)
      cap ||= current
      return pkmn.growth_rate.minimum_exp_for_level(cap.clamp(1, max_level))
    end

    #---------------------------------------------------------------------------
    # Candy handlers (wrapped around the vanilla handlers at load time)
    #---------------------------------------------------------------------------
    def self.cap_block_message(pkmn, cap, scene)
      msg = _INTL("{1} can't grow past the level cap (Lv. {2}) yet.", pkmn.name, cap)
      if scene.respond_to?(:pbDisplay)
        scene.pbDisplay(msg)
      else
        pbMessage(msg)
      end
    end

    def self.use_rare_candy(original, item, qty, pkmn, scene)
      return original.call(item, qty, pkmn, scene) if !candy_capped? || pkmn.shadowPokemon?
      cap = current
      if pkmn.level >= cap
        if RARE_CANDY_EVOLVES_AT_CAP && (new_species = pkmn.check_evolution_on_level_up)
          pbFadeOutInWithMusic do
            evo = PokemonEvolutionScene.new
            evo.pbStartScreen(pkmn, new_species)
            evo.pbEvolution
            evo.pbEndScreen
            scene.pbRefresh if scene.is_a?(PokemonPartyScreen)
          end
          return true
        end
        cap_block_message(pkmn, cap, scene)
        return false
      end
      qty = qty.clamp(1, cap - pkmn.level)
      return original.call(item, qty, pkmn, scene)
    end

    def self.use_exp_candy(original, item, qty, pkmn, scene)
      return original.call(item, qty, pkmn, scene) if !candy_capped? || pkmn.shadowPokemon?
      cap = current
      if pkmn.level >= cap
        cap_block_message(pkmn, cap, scene)
        return false
      end
      return with_exp_context(exp_ceiling_for(pkmn, cap), nil) do
        original.call(item, qty, pkmn, scene)
      end
    end

    def self.install_candy_handlers
      # Rare Candy
      use_proc = ItemHandlers::UseOnPokemon[:RARECANDY]
      max_proc = ItemHandlers::UseOnPokemonMaximum[:RARECANDY]
      if use_proc
        ItemHandlers::UseOnPokemon.add(:RARECANDY, proc { |item, qty, pkmn, scene|
          next Prismfall::LevelCap.use_rare_candy(use_proc, item, qty, pkmn, scene)
        })
      end
      if max_proc
        ItemHandlers::UseOnPokemonMaximum.add(:RARECANDY, proc { |item, pkmn|
          ret = max_proc.call(item, pkmn)
          next ret if !Prismfall::LevelCap.candy_capped?
          next [[ret, Prismfall::LevelCap.current - pkmn.level].min, 1].max
        })
      end
      # EXP Candies
      EXP_CANDY_AMOUNTS.each do |candy, amount|
        candy_use = ItemHandlers::UseOnPokemon[candy]
        candy_max = ItemHandlers::UseOnPokemonMaximum[candy]
        if candy_use
          ItemHandlers::UseOnPokemon.add(candy, proc { |item, qty, pkmn, scene|
            next Prismfall::LevelCap.use_exp_candy(candy_use, item, qty, pkmn, scene)
          })
        end
        next if !candy_max
        ItemHandlers::UseOnPokemonMaximum.add(candy, proc { |item, pkmn|
          ret = candy_max.call(item, pkmn)
          next ret if !Prismfall::LevelCap.candy_capped?
          needed = Prismfall::LevelCap.exp_ceiling_for(pkmn) - pkmn.exp
          next [[ret, (needed / amount.to_f).ceil].min, 1].max
        })
      end
    end
  end

  def self.level_cap
    return LevelCap.current
  end
end

Prismfall::LevelCap.install_candy_handlers

#===============================================================================
# Exp clamp + multiplier (only active inside Prismfall::LevelCap.with_exp_context)
#===============================================================================
module GameData
  class GrowthRate
    alias __prismfall_core_add_exp add_exp unless method_defined?(:__prismfall_core_add_exp)

    def add_exp(exp1, exp2)
      ctx = Prismfall::LevelCap.exp_context
      return __prismfall_core_add_exp(exp1, exp2) if !ctx
      mult = ctx[:multiplier]
      exp2 = (exp2 * mult).floor if mult && mult != 1 && exp2 > 0
      ret = __prismfall_core_add_exp(exp1, exp2)
      ceiling = ctx[:ceiling]
      ret = [ret, [ceiling, exp1].max].min if ceiling
      return ret
    end
  end
end

class Battle
  alias __prismfall_core_pbGainExpOne pbGainExpOne unless method_defined?(:__prismfall_core_pbGainExpOne)

  def pbGainExpOne(idxParty, defeatedBattler, numPartic, expShare, expAll, showMessages = true)
    pkmn = pbParty(0)[idxParty]
    ceiling = nil
    if pkmn && Prismfall::LevelCap.exp_capped?
      cap = Prismfall::LevelCap.current
      if pkmn.level >= cap
        pkmn.calc_stats   # EVs gained this battle still apply
        prismfall_show_cap_message(pkmn, cap) if showMessages
        return
      end
      ceiling = Prismfall::LevelCap.exp_ceiling_for(pkmn, cap)
    end
    mult = Prismfall::Difficulty.setting(:exp_multiplier) || 1
    Prismfall::LevelCap.with_exp_context(ceiling, mult) do
      __prismfall_core_pbGainExpOne(idxParty, defeatedBattler, numPartic, expShare, expAll, showMessages)
    end
  end

  def prismfall_show_cap_message(pkmn, cap)
    return if !Prismfall::SHOW_CAP_EXP_MESSAGE
    @prismfall_cap_messages ||= {}
    return if @prismfall_cap_messages[pkmn.personalID]
    @prismfall_cap_messages[pkmn.personalID] = true
    pbDisplayPaused(_INTL("{1} is at the level cap (Lv. {2}) and can't gain Exp. Points.", pkmn.name, cap))
  end
end

#===============================================================================
# Obedience tied to the cap. When caps are disabled the vanilla (badge-based)
# check runs unchanged.
#===============================================================================
class Battle::Battler
  alias __prismfall_core_pbObedienceCheck? pbObedienceCheck? unless method_defined?(:__prismfall_core_pbObedienceCheck?)

  def pbObedienceCheck?(choice)
    return __prismfall_core_pbObedienceCheck?(choice) if !Prismfall::LevelCap.enabled?
    return true if usingMultiTurnAttack?
    return true if choice[0] != :UseMove
    return true if !@battle.internalBattle
    return true if !@battle.pbOwnedByPlayer?(@index)
    disobedient = false
    obey_level = Prismfall::LevelCap.obedience_level
    if obey_level && @level > obey_level
      a = ((@level + obey_level) * @battle.pbRandom(256) / 256).floor
      disobedient |= (a >= obey_level)
    end
    disobedient |= !pbHyperModeObedience(choice[2])
    return true if !disobedient
    return pbDisobey(choice, obey_level || @level)
  end
end

#===============================================================================
# EXP Candy clamp
#===============================================================================
alias __prismfall_core_pbChangeExp pbChangeExp unless defined?(__prismfall_core_pbChangeExp)
def pbChangeExp(pkmn, new_exp, scene)
  ctx = Prismfall::LevelCap.exp_context
  if ctx && ctx[:ceiling] && new_exp > pkmn.exp
    new_exp = [new_exp, [ctx[:ceiling], pkmn.exp].max].min
  end
  return __prismfall_core_pbChangeExp(pkmn, new_exp, scene)
end

#===============================================================================
# Day Care
#===============================================================================
class DayCare
  class DayCareSlot
    alias __prismfall_core_add_exp add_exp unless method_defined?(:__prismfall_core_add_exp)

    def add_exp(amount = 1)
      if Prismfall::DAYCARE_RESPECTS_CAP && Prismfall::LevelCap.exp_capped? && filled?
        ceiling = Prismfall::LevelCap.exp_ceiling_for(@pokemon)
        return if @pokemon.exp >= ceiling
        amount = [amount, ceiling - @pokemon.exp].min
      end
      return __prismfall_core_add_exp(amount)
    end
  end
end

#===============================================================================
# Pause menu info box ("Level cap: Lv. 23 / Mode: Standard")
#===============================================================================
class PokemonPauseMenu
  alias __prismfall_core_pbShowInfo pbShowInfo unless method_defined?(:__prismfall_core_pbShowInfo)

  def pbShowInfo
    __prismfall_core_pbShowInfo
    return if !Prismfall::SHOW_CAP_IN_PAUSE_MENU
    return if defined?(pbInSafari?) && pbInSafari?
    return if defined?(pbInBugContest?) && pbInBugContest?
    @scene.pbShowInfo(Prismfall::LevelCap.info_text)
  end
end
