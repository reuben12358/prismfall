#===============================================================================
# Prismfall Trials - 010 Script page conditions for map events
#-------------------------------------------------------------------------------
# RMXP page conditions only know switches, variables and self switches. Quest
# state lives in save data, so an event page whose FIRST command is a Comment
#     Condition: quest_step(:EL_TART_THIEF) == :chase && chase(:EL_TART_THIEF) == 2
# is only active while that Prismfall::Conditions string is true (safe parser,
# no eval). Ordinary RMXP conditions on the same page still apply. Pages are
# re-checked whenever $game_map.need_refresh is set; every Trials state change
# sets it. Map builder DSL: commands: [{comment: "Condition: ..."}, ...].
#===============================================================================
module Prismfall
  module Trials
    module PageConditions
      PREFIX = /\A\s*Condition:\s*(.+)\z/i
      @cache = {}

      # The condition text of a page, or nil (cached per page object).
      def self.text_for(page)
        key = page.object_id
        return @cache[key] if @cache.has_key?(key)
        txt = nil
        cmd = page.list && page.list[0]
        if cmd && cmd.code == 108
          m = PREFIX.match(cmd.parameters[0].to_s)
          if m
            txt = m[1].strip
            i = 1
            while page.list[i] && page.list[i].code == 408   # comment continuation lines
              txt += " " + page.list[i].parameters[0].to_s.strip
              i += 1
            end
          end
        end
        @cache[key] = txt
        return txt
      end

      def self.passes?(page)
        txt = text_for(page)
        return true if txt.nil?
        return Prismfall::Conditions.evaluate(txt)
      rescue StandardError => e
        Prismfall::Trials.warn("Bad page condition #{txt.inspect}: #{e.message}")
        return false
      end
    end
  end
end

class Game_Event
  alias __prismfall_trials__refresh refresh unless method_defined?(:__prismfall_trials__refresh)

  def refresh
    pages = @event.pages
    if @erased || pages.none? { |pg| Prismfall::Trials::PageConditions.text_for(pg) }
      return __prismfall_trials__refresh
    end
    @event.pages = pages.select { |pg| Prismfall::Trials::PageConditions.passes?(pg) }
    begin
      __prismfall_trials__refresh
    ensure
      @event.pages = pages
    end
  end
end
