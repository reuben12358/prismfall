#===============================================================================
# Prismfall Bosses - 003 Per-battle boss state
# State lives on the battle, keyed by the boss's Pokémon object, so it survives
# switching (a trainer's ace can switch out and back in with its bars intact).
#===============================================================================
module Prismfall
  module Bosses
    class BossState
      attr_reader   :id, :data, :pokemon, :bars
      attr_accessor :bars_left, :pending, :pending_defeat, :phase_turn, :overflow, :defeated,
                    :intro_shown, :result, :end_decision, :breaks_done

      def initialize(id, data, pokemon, bars)
        @id          = id
        @data        = data
        @pokemon     = pokemon
        @bars        = bars
        @bars_left   = bars
        @pending     = nil    # :break / :defeat once the current bar is depleted
        @phase_turn  = 0
        @overflow    = 0      # damage discarded at bar breaks (debug/tests)
        @defeated    = false
        @intro_shown = false
        @breaks_done = 0
      end

      # 1 = first bar, bars = last bar.
      def phase;     return @bars - @bars_left + 1; end
      def last_bar?; return @bars_left <= 1;        end

      def immunities
        v = Bosses.resolve(@data[:status_immunity])
        v = true if v.nil?
        list = case v
               when true  then DEFAULT_IMMUNITIES
               when :all  then ALL_IMMUNITIES
               when Array then v
               else            []
               end
        return list
      end

      def immune_to?(status)
        return false if @defeated
        return false if last_bar? && !Bosses.resolve(@data[:immunity_last_bar])
        status = :POISON if status == :TOXIC
        return immunities.include?(status)
      end

      # false (default) = never, true = always, :last_bar = only on the last bar.
      def catch_rule
        v = Bosses.resolve(@data[:catch])
        return (v.nil?) ? false : v
      end

      def catchable?
        case catch_rule
        when true      then return true
        when :last_bar then return last_bar?
        end
        return false
      end

      def catch_rate
        r = Bosses.resolve(@data[:catch_rate])
        return (r.is_a?(Integer)) ? r : nil
      end

      def summary
        return { :id => @id, :bars => @bars, :bars_left => @bars_left, :breaks => @breaks_done,
                 :defeated => @defeated, :result => @result, :overflow => @overflow }
      end
    end

    #---------------------------------------------------------------------------
    def self.boss_pokemon?(pkmn)
      return pkmn.respond_to?(:prismfall_boss_id) && pkmn.prismfall_boss_id && exists?(pkmn.prismfall_boss_id)
    end

    # The battler's boss state, or nil if it isn't an (opposing) boss.
    def self.state_for(battler)
      return nil if !battler || !battler.respond_to?(:pokemon)
      pkmn = battler.pokemon
      return nil if !boss_pokemon?(pkmn)
      return nil if battler.respond_to?(:opposes?) && !battler.opposes?
      battle = battler.battle
      return nil if !battle || !battle.respond_to?(:prismfall_boss_states)
      states = battle.prismfall_boss_states
      return states[pkmn] if states[pkmn]
      data = get(pkmn.prismfall_boss_id)
      return states[pkmn] = BossState.new(pkmn.prismfall_boss_id, data, pkmn, bars_for(data))
    end

    def self.boss_battlers(battle)
      return [] if !battle
      return battle.battlers.select { |b| b && !b.fainted? && state_for(b) }
    end
  end
end

class Battle
  def prismfall_boss_states
    @prismfall_boss_states ||= {}.compare_by_identity
    return @prismfall_boss_states
  end
end
