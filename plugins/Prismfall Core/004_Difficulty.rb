#===============================================================================
# Prismfall Core - 004 Difficulty modes (Casual / Standard / Hard)
#-------------------------------------------------------------------------------
# Hooks (all alias-chained, battle/trainer-loading layer only):
#   pbLoadTrainer                                -> picks the +100/+200 variant
#   BattleCreationHelperMethods.prepare_battle   -> Set style, Bag rule
#   Battle#pbItemMenu                            -> blocks the Bag when ruled out
#   Game_Temp#add_battle_rule                    -> "noBagItems"/"allowBagItems"
#   NPCTrainer#skill_level                       -> per-mode AI skill floor/ceiling
#===============================================================================
module Prismfall
  module Difficulty
    module_function

    def current
      mode = Prismfall.state.difficulty
      return (DIFFICULTIES.has_key?(mode)) ? mode : DIFFICULTY_DEFAULT
    end

    def data(mode = nil)
      return DIFFICULTIES[mode || current] || DIFFICULTIES[DIFFICULTY_DEFAULT]
    end

    def setting(key, mode = nil)
      return data(mode)[key]
    end

    def label(mode = nil)
      return _INTL(data(mode)[:name])
    end

    def casual?;   return current == :CASUAL;   end
    def standard?; return current == :STANDARD; end
    def hard?;     return current == :HARD;     end
    def chosen?;   return Prismfall.state.difficulty_chosen ? true : false; end

    # Rank in DIFFICULTY_ORDER (0 = easiest).
    def rank(mode = nil)
      return DIFFICULTY_ORDER.index(mode || current) || DIFFICULTY_ORDER.index(DIFFICULTY_DEFAULT)
    end

    def set(mode)
      mode = mode.to_s.upcase.to_sym if mode.is_a?(String)
      raise ArgumentError, "Unknown difficulty #{mode.inspect}" if !DIFFICULTIES.has_key?(mode)
      st = Prismfall.state
      old = st.difficulty
      st.difficulty = mode
      st.difficulty_chosen = true
      if old != mode
        play_time = ($stats) ? $stats.play_time.to_i : 0
        st.difficulty_log.push([old, mode, play_time])
      end
      EventHandlers.trigger(:prismfall_difficulty_changed, old, mode)
      return mode
    end

    # True if the save has ever been played on an easier mode than `mode`.
    def ever_below?(mode)
      target = DIFFICULTY_ORDER.index(mode) || 0
      return true if rank < target
      return Prismfall.state.difficulty_log.any? do |entry|
        (DIFFICULTY_ORDER.index(entry[0]) || 0) < target || (DIFFICULTY_ORDER.index(entry[1]) || 0) < target
      end
    end

    # Choice window with a description of each mode. Returns the chosen mode, or
    # nil if cancelled (only possible when cancelable is true).
    # Event usage (intro): Script: Prismfall.choose_difficulty
    def choose(cancelable: false, message: nil, modes: nil)
      modes ||= DIFFICULTY_ORDER
      commands = modes.map { |m| _INTL(DIFFICULTIES[m][:name]) }
      helps    = modes.map { |m| _INTL(DIFFICULTIES[m][:description]) }
      default  = modes.index(current) || 0
      message ||= _INTL("Choose a difficulty.")
      loop do
        pbMessage(message) if message && !message.empty?
        cancel_value = (cancelable) ? -1 : 0
        idx = pbShowCommandsWithHelp(nil, commands, helps, cancel_value, default)
        return nil if idx < 0
        mode = modes[idx]
        next if !pbConfirmMessage(_INTL("Play on {1}?", commands[idx]))
        set(mode)
        return mode
      end
    end

    # Menu for an NPC/PC option to change difficulty mid-game (respects
    # DIFFICULTY_CHANGE_RULE). Returns the new mode, or nil if nothing changed.
    def change_menu
      case DIFFICULTY_CHANGE_RULE
      when :locked
        pbMessage(_INTL("The difficulty can't be changed in this save."))
        return nil
      when :lower_only
        modes = DIFFICULTY_ORDER.select { |m| DIFFICULTY_ORDER.index(m) <= rank }
      else
        modes = DIFFICULTY_ORDER.clone
      end
      if modes.length <= 1
        pbMessage(_INTL("There's no other difficulty to switch to."))
        return nil
      end
      old = current
      ret = choose(cancelable: true, modes: modes,
                   message: _INTL("Current difficulty: {1}.", label))
      return nil if ret.nil? || ret == old
      pbMessage(_INTL("Difficulty set to {1}.", label))
      return ret
    end

    def version_offset(mode = nil)
      return setting(:version_offset, mode) || 0
    end

    # Picks the trainers.txt version to load for the active difficulty.
    def resolve_trainer_version(tr_type, tr_name, version)
      version = 0 if version.nil?
      return version if !version.is_a?(Integer) || version < 0 || version >= TRAINER_VARIANT_STRIDE
      offset = version_offset
      return version if offset == 0
      return version if !tr_name.is_a?(String)
      type_data = GameData::TrainerType.try_get(tr_type)
      return version if !type_data
      candidate = version + offset
      return candidate if GameData::Trainer.exists?(type_data.id, tr_name, candidate)
      return version
    end

    # Called from prepare_battle (after vanilla + other plugins have run).
    def apply_battle_rules(battle, rules)
      rules ||= {}
      mode = data
      # Bag in battle
      no_bag = rules["noBagItems"]
      no_bag = (battle.trainerBattle? && !mode[:trainer_bag_items]) if no_bag.nil?
      battle.rules["prismfall_no_bag_items"] = (no_bag) ? true : false
      # Battle style
      battle.switchStyle = false if mode[:force_set_style] && rules["switchStyle"].nil?
      # Snapshot for other plugins/debugging
      battle.rules["prismfall_difficulty"] = current
      battle.rules["prismfall_level_cap"]  = Prismfall::LevelCap.current
    end

    def adjust_ai_skill(skill)
      return skill if !skill.is_a?(Integer)
      lo = setting(:ai_skill_min)
      hi = setting(:ai_skill_max)
      skill = lo if lo && skill < lo
      skill = hi if hi && skill > hi
      return skill
    end
  end

  def self.difficulty;                    return Difficulty.current;             end
  def self.choose_difficulty(**kwargs);   return Difficulty.choose(**kwargs);    end
  def self.set_difficulty(mode);          return Difficulty.set(mode);           end
end

#===============================================================================
# Trainer variant selection (works for TrainerBattle, partners, debug battles).
#===============================================================================
alias __prismfall_core_pbLoadTrainer pbLoadTrainer unless defined?(__prismfall_core_pbLoadTrainer)
def pbLoadTrainer(tr_type, tr_name, tr_version = 0)
  tr_version = Prismfall::Difficulty.resolve_trainer_version(tr_type, tr_name, tr_version)
  return __prismfall_core_pbLoadTrainer(tr_type, tr_name, tr_version)
end

#===============================================================================
# Battle rules: setBattleRule("noBagItems") / setBattleRule("allowBagItems")
#===============================================================================
class Game_Temp
  alias __prismfall_core_add_battle_rule add_battle_rule unless method_defined?(:__prismfall_core_add_battle_rule)

  def add_battle_rule(rule, var = nil)
    case rule.to_s.downcase
    when "nobagitems", "nobag"
      self.battle_rules["noBagItems"] = true
      return
    when "allowbagitems", "bagitems"
      self.battle_rules["noBagItems"] = false
      return
    end
    __prismfall_core_add_battle_rule(rule, var)
  end
end

module BattleCreationHelperMethods
  class << self
    alias __prismfall_core_prepare_battle prepare_battle unless method_defined?(:__prismfall_core_prepare_battle)
  end

  def self.prepare_battle(battle)
    __prismfall_core_prepare_battle(battle)
    Prismfall::Difficulty.apply_battle_rules(battle, $game_temp.battle_rules)
  end
end

#===============================================================================
# Bag lock (mechanics layer, so it works with the vanilla scene and EBDX).
#===============================================================================
class Battle
  alias __prismfall_core_pbItemMenu pbItemMenu unless method_defined?(:__prismfall_core_pbItemMenu)

  def pbItemMenu(idxBattler, firstAction)
    if @rules.is_a?(Hash) && @rules["prismfall_no_bag_items"]
      pbDisplay(_INTL("Items from the Bag can't be used in this battle!"))
      return false
    end
    return __prismfall_core_pbItemMenu(idxBattler, firstAction)
  end
end

#===============================================================================
# AI skill per difficulty.
#===============================================================================
class NPCTrainer
  alias __prismfall_core_skill_level skill_level unless method_defined?(:__prismfall_core_skill_level)

  def skill_level
    return Prismfall::Difficulty.adjust_ai_skill(__prismfall_core_skill_level)
  end
end
