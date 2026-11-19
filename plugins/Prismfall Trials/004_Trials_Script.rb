#===============================================================================
# Prismfall Trials - 004 Quest scene scripts
#-------------------------------------------------------------------------------
# A quest's :scenes are plain Arrays, so one source drives the game, the
# headless test and the generated dialogue doc (tools/trials_script.rb).
# Entries:
#   "text"                              narration box
#   [:SPEAKER, :expression, "text"]     a character line (portrait bubble when
#                                       the Cutscenes plugin is installed)
#   { :map => "stage direction" }       doc only (the map event moves people)
#   { :note => "design note" }          doc only
#   { :choice => "prompt" | [:SPK, :expr, "prompt"],
#     :options => [["Label", [entries], "optional condition"], ...], :cancel => i }
#   { :if => "condition", :then => [...], :else => [...] }
#   { :accept => true }                 start the quest (first step)
#   { :step => :id }                    move to a step (quest log updates)
#   { :complete => true | :outcome }    finish + rewards (per-outcome rewards)
#   { :fail => true }                   mark failed
#   { :flag => [:key, value] }  { :count => [:key, n] }
#   { :event_battle => :MON, :caught => [], :won => [], :lost => [], :fled => [] }
#   { :trainer => [:TYPE, "Name", version], :won => [], :lost => [], :field => :ID, :double => true }
#   { :gauntlet => [[:TYPE, "Name", v], ...], :heal_between => false, :won => [], :lost => [] }
#   { :gift => :MON, :variant => :key }  { :join => :MON } (a beaten :boss joins, :joins overrides)
#    { :item => [:ITEM, qty] }  { :take => [:ITEM, qty] }
#   { :money => n }  { :pay => n }  { :effects => "JUNO+1 RES+1" }  { :points => [:TRIAL, n] }
#   { :choice_key => [:registered_choice, :value] }  { :deed => :id }
#   { :chase => :advance | :reset }      { :heal => true }  { :se => "name" }  { :me => "name" }
#   { :wait => seconds }  { :run => :scene }  { :result => :symbol }  { :end => true }
#   { :script => proc { |ctx| ... } }   escape hatch (shown as "(script)" in the doc)
# Conditions are Prismfall::Conditions strings; ":SELF" means this quest.
#===============================================================================
module Prismfall
  module Trials
    # Display names for speakers that have no Portrait registration.
    SPEAKERS = {}

    # Scripted answers for choices (headless tests): consumed before asking.
    @answers = []
    class << self
      attr_accessor :answers
    end

    def self.speaker_name(id)
      return _INTL(SPEAKERS[id]) if SPEAKERS[id]
      if defined?(Prismfall::Portrait) && Prismfall::Portrait.respond_to?(:display_name)
        return Prismfall::Portrait.display_name(id) rescue nil
      end
      return id.to_s.split("_").map(&:capitalize).join(" ")
    end

    # One line of dialogue, optionally with choices. Returns the choice index.
    def self.say(speaker, expression, text, commands = nil, cancel = 0)
      text = _INTL(text)
      if speaker.nil?
        return pick(text, commands, cancel) if commands
        pbMessage(text)
        return 0
      end
      return pick("#{speaker_name(speaker)}: #{text}", commands, cancel, speaker, expression, text) if commands
      if defined?(pf_say) && defined?(Prismfall::Portrait)
        pf_say(speaker, expression || :neutral, text, name: speaker_name(speaker))
      else
        pbMessage("#{speaker_name(speaker)}: #{text}")
      end
      return 0
    end

    def self.pick(message, commands, cancel = 0, speaker = nil, expression = nil, raw = nil)
      labels = commands.map { |c| _INTL(c) }
      if @answers && !@answers.empty?
        ans = @answers.shift
        idx = ans.is_a?(Integer) ? ans : labels.index(ans.to_s)
        raise ArgumentError, "Scripted answer #{ans.inspect} not in #{labels.inspect}" if idx.nil? || idx >= labels.length
        pbMessage(message) if defined?(Harness)   # keep the line in the test log
        return idx
      end
      if speaker && defined?(pf_say) && defined?(Prismfall::Portrait)
        return pf_say(speaker, expression || :neutral, raw, name: speaker_name(speaker), commands: labels, cancel: cancel + 1) || 0
      end
      return pbMessage(message, labels, cancel + 1)
    end

    def self.cond(text, quest_id = nil)
      return true if text.nil? || text.to_s.strip.empty?
      t = text.to_s
      t = t.gsub(":SELF", ":#{quest_id}") if quest_id
      return Prismfall::Conditions.evaluate(t)
    end

    module Script
      class Halt < StandardError; end

      # Runs a scene of quest_id. Returns ctx[:result] (or true).
      def self.run_scene(quest_id, scene)
        q = Prismfall::Trials.get(quest_id)
        raise ArgumentError, "Unknown quest #{quest_id.inspect}" if !q
        list = (q[:scenes] || {})[scene]
        raise ArgumentError, "Quest #{quest_id} has no scene #{scene.inspect}" if !list
        ctx = { :quest => quest_id, :scene => scene, :result => nil, :depth => 0 }
        begin
          exec(list, ctx)
        rescue Halt
        end
        Prismfall::Trials.refresh_map
        return ctx[:result].nil? ? true : ctx[:result]
      end

      def self.exec(list, ctx)
        Array(list).each { |entry| exec_one(entry, ctx) }
      end

      def self.exec_one(e, ctx)
        tr = Prismfall::Trials
        qid = ctx[:quest]
        case e
        when String
          tr.say(nil, nil, e)
          return
        when Array
          tr.say(e[0], e[1], e[2].to_s)
          return
        when Hash
          # handled below
        else
          raise ArgumentError, "Bad script entry #{e.inspect} in #{qid}/#{ctx[:scene]}"
        end
        if e.has_key?(:map) || e.has_key?(:note)
          return
        elsif e.has_key?(:choice)
          opts = (e[:options] || []).select { |o| tr.cond(o[2], qid) }
          labels = opts.map { |o| o[0] }
          prompt = e[:choice]
          cancel = e[:cancel] || (labels.length - 1)
          idx = if prompt.is_a?(Array)
                  tr.say(prompt[0], prompt[1], prompt[2].to_s, labels, cancel)
                else
                  tr.say(nil, nil, prompt.to_s, labels, cancel)
                end
          idx = cancel if idx.nil? || idx < 0
          exec(opts[idx][1], ctx) if opts[idx]
        elsif e.has_key?(:if)
          exec(tr.cond(e[:if], qid) ? e[:then] : e[:else], ctx)
        elsif e[:accept]
          tr.start(qid)
        elsif e.has_key?(:step)
          tr.set_step(qid, e[:step])
        elsif e.has_key?(:complete)
          tr.complete(qid, (e[:complete] == true) ? nil : e[:complete])
        elsif e[:fail]
          tr.fail(qid)
        elsif e.has_key?(:flag)
          tr.set_flag(qid, e[:flag][0], e[:flag][1])
        elsif e.has_key?(:count)
          tr.add_count(qid, e[:count][0], e[:count][1] || 1)
        elsif e.has_key?(:event_battle)
          res = Prismfall::EventMons.battle(e[:event_battle])
          exec(e[res] || [], ctx)
        elsif e.has_key?(:trainer)
          won = tr.trainer_battle(e[:trainer], field: e[:field], double: e[:double], lose_text: e[:lose_text])
          exec(won ? (e[:won] || []) : (e[:lost] || []), ctx)
        elsif e.has_key?(:gauntlet)
          won = tr.gauntlet(e[:gauntlet], heal_between: e[:heal_between], field: e[:field])
          exec(won ? (e[:won] || []) : (e[:lost] || []), ctx)
        elsif e.has_key?(:gift)
          Prismfall::EventMons.gift(e[:gift], e[:variant])
        elsif e.has_key?(:join)
          Prismfall::EventMons.join(e[:join])
        elsif e.has_key?(:item)
          pbReceiveItem(e[:item][0], e[:item][1] || 1)
        elsif e.has_key?(:take)
          $bag.remove(e[:take][0], e[:take][1] || 1) if $bag
        elsif e.has_key?(:money)
          tr.give_money(e[:money])
        elsif e.has_key?(:pay)
          $player.money = [$player.money - e[:pay].to_i, 0].max
        elsif e.has_key?(:effects)
          Prismfall::Narrative.apply_effects(e[:effects])
        elsif e.has_key?(:points)
          tr.add_points(e[:points][0], e[:points][1])
        elsif e.has_key?(:choice_key)
          Prismfall::Choices.make(e[:choice_key][0], e[:choice_key][1])
        elsif e.has_key?(:deed)
          tr.record_deed(e[:deed])
        elsif e.has_key?(:chase)
          (e[:chase] == :reset) ? tr.chase_reset(qid) : tr.chase_advance(qid)
        elsif e[:heal]
          $player.heal_party if $player
        elsif e.has_key?(:se)
          pbSEPlay(e[:se]) rescue nil
        elsif e.has_key?(:me)
          pbMEPlay(e[:me]) rescue nil
        elsif e.has_key?(:wait)
          pbWait(e[:wait].to_f) rescue nil
        elsif e.has_key?(:run)
          raise ArgumentError, "Scene recursion too deep in #{qid}" if ctx[:depth] > 8
          list = (tr.get(qid)[:scenes] || {})[e[:run]]
          raise ArgumentError, "Quest #{qid} has no scene #{e[:run].inspect}" if !list
          ctx[:depth] += 1
          exec(list, ctx)
          ctx[:depth] -= 1
        elsif e.has_key?(:result)
          ctx[:result] = e[:result]
        elsif e[:end]
          raise Halt
        elsif e.has_key?(:script)
          e[:script].call(ctx)
        else
          raise ArgumentError, "Unknown script command #{e.keys.inspect} in #{qid}/#{ctx[:scene]}"
        end
      end
    end
  end
end

# Event usage: Script: pf_quest_run(:EL_TART_THIEF, :offer)
def pf_quest_run(id, scene)
  return Prismfall::Trials::Script.run_scene(id, scene)
end
