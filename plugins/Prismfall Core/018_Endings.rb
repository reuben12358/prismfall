#===============================================================================
# Prismfall Core - 018 Endings
#-------------------------------------------------------------------------------
#   Prismfall::Endings.determine          -> ending ID from ENDING_RULES
#   Prismfall.trigger_ending(:END_RETURN) -> Ledger, post-game state, hooks,
#                                            optional common event + credits
# After Scene_Credits finishes, the map scene returns and the calling event
# continues, so post-game warps/epilogue text can follow the call.
#===============================================================================
module Prismfall
  module Endings
    # Optional global hook: proc { |id, data, first_time| ... }
    HOOK = nil
    POSTGAME_UNLOCKS_FINALE_CAP = true

    def self.registry
      return Prismfall::Narrative::ENDINGS
    end

    def self.determine
      Prismfall::Narrative::ENDING_RULES.each do |id, condition|
        return id if Prismfall::Conditions.evaluate(condition)
      end
      return Prismfall::Narrative::DEFAULT_ENDING
    end

    def self.reached
      return Prismfall.state.narrative[:endings]
    end

    def self.postgame?
      return Prismfall.state.narrative[:postgame] ? true : false
    end

    class << self
      attr_accessor :title_after_credits
    end

    # Writes FLAGS.md S263-S269 for the ending (Narrative::POSTGAME_SWITCHES).
    def self.apply_postgame_switches(id)
      return if !$game_switches
      on = Prismfall::Narrative::POSTGAME_SWITCHES[id] || []
      Prismfall::Narrative::POSTGAME_ALL_SWITCHES.each { |sw| $game_switches[sw] = on.include?(sw) }
      $game_map.need_refresh = true if $game_map
    end

    def self.trigger(id = nil, credits: nil)
      id = (id || determine).to_sym
      data = registry[id]
      raise ArgumentError, "Unknown ending #{id.inspect}" if !data
      first = Prismfall::Ledger.record_ending(id)
      n = Prismfall.state.narrative
      n[:endings].push(id) if !n[:endings].include?(id)
      n[:ending]   = id
      n[:postgame] = id   # truthy; the ending ID (NARRATIVE_KEYS section 12)
      apply_postgame_switches(id)
      Prismfall::LevelCap.unlock_finale! if POSTGAME_UNLOCKS_FINALE_CAP
      $stats.set_time_to_hall_of_fame if $stats.respond_to?(:set_time_to_hall_of_fame)
      EventHandlers.trigger(:prismfall_ending, id, first)
      HOOK.call(id, data, first) if HOOK
      pbCommonEvent(data[:common_event]) if data[:common_event]
      roll = (credits.nil?) ? data[:credits] : credits
      no_postgame = Prismfall::Narrative::NO_POSTGAME_ENDINGS.include?(id)
      if roll
        self.title_after_credits = no_postgame
        $scene = Scene_Credits.new
      elsif no_postgame
        pbMapInterpreter.command_end if pbMapInterpreterRunning?
        $game_temp.title_screen_calling = true
      end
      return id
    end
  end

  def self.trigger_ending(id = nil, **kwargs)
    return Endings.trigger(id, **kwargs)
  end
end

# "credits -> title" for endings without a post-game (e.g. The Gilded Chain).
class Scene_Credits
  alias __prismfall_core_main main unless method_defined?(:__prismfall_core_main)

  def main
    __prismfall_core_main
    return if !Prismfall::Endings.title_after_credits
    Prismfall::Endings.title_after_credits = false
    pbMapInterpreter.command_end if pbMapInterpreterRunning?
    SaveData.mark_values_as_unloaded
    $scene = pbCallTitle
  end
end
