#===============================================================================
# Prismfall Trials - 003 Registries: quests and event Pokemon
#-------------------------------------------------------------------------------
# Prismfall::Trials.quest(:ID, { ... })       see QUEST_KEYS below
# Prismfall::EventMons.register(:ID, { ... }) see 006_Trials_EventMons.rb
# Data files (1xx_*.rb) only call these two, so tools/trials_script.rb can load
# them outside the engine to print design/TRIALS_SCRIPT.md.
#===============================================================================
module Prismfall
  module Trials
    QUEST_KEYS = [
      :trial,      # Symbol, key of TRIALS (the board it is posted on)
      :title,      # String
      :giver,      # String (who asks)
      :map,        # Integer, map ID where it is given (current maps.json ID)
      :where,      # String, human description of the place
      :rank,       # Integer 1-5: Trial rank needed to take it (default 1)
      :points,     # Integer: Trial points on completion (default 1)
      :joint,      # { :OTHER_TRIAL => points } extra points to other Trials
      :rec_level,  # Integer: "Rec. Lv." shown on the board
      :chapter,    # Integer: story chapter it first becomes reachable in (info)
      :unlock,     # condition string (Prismfall::Conditions), e.g. "badges >= 1"
      :requires,   # [quest ids] that must be done first
      :expires,    # condition string: once true, an untaken quest is gone
      :board,      # true = listed on the Trial board; false = only given by its NPC
      :summary,    # String shown on the board and in the log
      :steps,      # { step_id => "quest log text" } in order
      :reward,     # { :money, :items => [[ITEM, qty]], :pokemon => EVENT_MON_ID, :effects => "JUNO+1", :text }
      :outcomes,   # { outcome => reward Hash } replaces/extends :reward per outcome
      :scenes,     # { scene_name => script Array } (004_Trials_Script.rb)
      :repeatable, # true = can be taken again after completion
      :stub,       # true = designed only, not wired on a map yet (hidden from boards)
      :tags,       # [Symbols] e.g. [:chase, :boss, :kindness, :cameo]
      :touches,    # String, which choices / bonds / standing it can move (info)
      :hidden,     # true = never listed (unasked kindnesses, secret quests)
      :design      # String: twist / humour / staging notes for stubs (doc only)
    ].freeze

    @quests = {}
    @order  = []

    class << self
      attr_reader :order
    end

    def self.quest(id, data)
      raise ArgumentError, "Quest id must be a Symbol (got #{id.inspect})" if !id.is_a?(Symbol)
      raise ArgumentError, "Quest #{id} needs a Hash" if !data.is_a?(Hash)
      unknown = data.keys - QUEST_KEYS
      warn("quest(:#{id}): unknown keys #{unknown.inspect}") if !unknown.empty?
      raise ArgumentError, "Quest #{id} has no :trial" if !data[:trial]
      @order.push(id) if !@quests.has_key?(id)
      @quests[id] = data.merge(:id => id).freeze
      return id
    end

    def self.get(id);      return @quests[id.to_sym];      end
    def self.exists?(id);  return @quests.has_key?(id.to_sym); end
    def self.quest_ids;    return @order.dup;              end

    def self.quests_for(trial)
      return @order.select { |id| @quests[id][:trial] == trial }
    end

    def self.trial(id)
      return TRIALS[id.to_sym]
    end

    def self.trial_name(id)
      t = trial(id)
      return (t) ? _INTL(t[:name]) : id.to_s
    end

    # Ordered step ids of a quest.
    def self.step_ids(id)
      q = get(id)
      return (q && q[:steps]) ? q[:steps].keys : []
    end
  end

  module EventMons
    KEYS = [
      :species, :level, :form, :gender, :shiny, :nature, :ability, :ability_index, :item, :moves,
      :ivs, :evs, :nickname, :ball, :happiness, :obtain_text, :ot_name,
      :kind,       # :battle (wild, catchable), :gift, :egg, :boss (boss battle, then :joins/:reward)
      :field,      # field for the battle (Symbol) or nil = map default
      :can_run,    # default false for :battle and :boss
      :catchable,  # default true for :battle
      :boss,       # Prismfall Bosses definition Hash (bars, stat_mults, breaks ...)
      :joins,      # after a :boss win: Hash of overrides for the Pokemon that joins (e.g. { :level => 13 })
      :join_choice, # true = the quest script asks first ({ :join => :ID }) instead of joining automatically
      :on_ko,      # :retry (default: can be fought again) or :lost (gone for good)
      :intro,      # message before the battle
      :variants,   # { variant => overrides } (e.g. Smeargle palettes)
      # design info (shown by the doc tool, not used by the engine)
      :where, :map, :chapter, :quest, :why, :trigger,
      :stub,       # true = designed only (not placed yet)
      :special_moves # moves it knows by design though it can't normally learn them (event moves)
    ].freeze

    @mons  = {}
    @order = []

    def self.register(id, data)
      raise ArgumentError, "Event mon id must be a Symbol (got #{id.inspect})" if !id.is_a?(Symbol)
      unknown = data.keys - KEYS
      Prismfall::Trials.warn("EventMons.register(:#{id}): unknown keys #{unknown.inspect}") if !unknown.empty?
      @order.push(id) if !@mons.has_key?(id)
      @mons[id] = data.merge(:id => id).freeze
      return id
    end

    def self.get(id);     return @mons[id.to_sym];          end
    def self.exists?(id); return @mons.has_key?(id.to_sym);  end
    def self.ids;         return @order.dup;                 end
  end
end
