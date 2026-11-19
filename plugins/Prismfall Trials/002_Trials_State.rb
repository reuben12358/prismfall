#===============================================================================
# Prismfall Trials - 002 Save state
#-------------------------------------------------------------------------------
# Lives in Prismfall.state (Core's SaveState, already registered with SaveData)
# as @trials, a plain Hash of Symbols/Integers/Strings, so old saves load and
# get an empty state. Nothing is kept in Game Switches (SPINE: systems keep
# their own state); events read it through pf_quest_* helpers and the
# "Condition:" page comments (010_Trials_PageConditions.rb).
#===============================================================================
class Prismfall::SaveState
  attr_writer :trials

  def trials
    @trials = {} if !@trials.is_a?(Hash)
    t = @trials
    t[:quests]     ||= {}   # quest id => { :state, :step, :flags, :counts, :outcome, :log, :accepted, :finished }
    t[:points]     ||= {}   # trial id => Integer
    t[:ranks_paid] ||= {}   # trial id => highest rank whose reward was given
    t[:event_mons] ||= {}   # event mon id => :caught / :won / :gifted / :lost / :fled / :declined
    t[:chases]     ||= {}   # chase id => stage (Integer)
    t[:deeds]      ||= {}   # quiet deed id => true (Elowen's unasked kindnesses)
    t[:tiers_seen] ||= {}   # map id => highest badge tier the player has walked into
    t[:rumours]    ||= []   # [[map_id, badge], ...] newest last
    t[:notice]       = nil if !t.has_key?(:notice)
    return t
  end
end

module Prismfall
  module Trials
    def self.store
      return Prismfall.state.trials
    end

    def self.play_time
      return ($stats) ? $stats.play_time.to_i : 0
    end

    def self.refresh_map
      $game_map.need_refresh = true if $game_map && $game_map.respond_to?(:need_refresh=)
    end

    def self.warn(msg)
      return if !$DEBUG
      if defined?(Console) && Console.respond_to?(:echo_warn)
        Console.echo_warn("[Prismfall Trials] #{msg}")
      elsif defined?(echoln)
        echoln("[Prismfall Trials] #{msg}")
      end
    end
  end
end
