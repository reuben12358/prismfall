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

    def self.trigger(id = nil, credits: nil)
      id = (id || determine).to_sym
      data = registry[id]
      raise ArgumentError, "Unknown ending #{id.inspect}" if !data
      first = Prismfall::Ledger.record_ending(id)
      n = Prismfall.state.narrative
      n[:endings].push(id) if !n[:endings].include?(id)
      n[:ending]   = id
      n[:postgame] = true
      Prismfall::LevelCap.unlock_finale! if POSTGAME_UNLOCKS_FINALE_CAP
      $stats.set_time_to_hall_of_fame if $stats.respond_to?(:set_time_to_hall_of_fame)
      EventHandlers.trigger(:prismfall_ending, id, first)
      HOOK.call(id, data, first) if HOOK
      pbCommonEvent(data[:common_event]) if data[:common_event]
      roll = (credits.nil?) ? data[:credits] : credits
      $scene = Scene_Credits.new if roll
      return id
    end
  end

  def self.trigger_ending(id = nil, **kwargs)
    return Endings.trigger(id, **kwargs)
  end
end
