#===============================================================================
# Prismfall Bosses - 002 Registry, value resolution, boss Pokémon creation
#===============================================================================
module Prismfall
  module Bosses
    DIFFICULTY_KEYS = [:CASUAL, :STANDARD, :HARD, :default]
    KNOWN_KEYS = [:end_after_rounds, :id, :name, :nickname, :species, :level, :form, :moves, :ability, :ability_index, :item, :nature,
                  :ivs, :evs, :gender, :shiny, :bars, :stat_mults, :status_immunity, :immunity_last_bar, :catch,
                  :catch_rate, :can_run, :can_lose, :size, :ai_skill, :ai_script, :ai_script_loop, :field, :weather,
                  :terrain, :music, :intro, :break_message, :on_break, :breaks, :on_defeat, :ebdx, :follow_prism,
                  :prism_interval, :description]
    MAIN_STATS = [:HP, :ATTACK, :DEFENSE, :SPECIAL_ATTACK, :SPECIAL_DEFENSE, :SPEED]

    @registry       = {}
    @trainer_rules  = {}
    @last_result    = nil
    @festival_on    = nil

    class << self
      attr_accessor :last_result
    end

    def self.register(id, data)
      raise ArgumentError, "Boss id must be a Symbol (got #{id.inspect})" if !id.is_a?(Symbol)
      raise ArgumentError, "Boss #{id} needs a Hash" if !data.is_a?(Hash)
      unknown = data.keys - KNOWN_KEYS
      log("register(:#{id}): unknown keys #{unknown.inspect}") if !unknown.empty?
      @registry[id] = data.merge(:id => id).freeze
      return id
    end

    def self.get(id);     return @registry[id];          end
    def self.[](id);      return @registry[id];          end
    def self.exists?(id); return @registry.key?(id);     end
    def self.ids;         return @registry.keys;         end

    def self.festival_enabled?
      return (@festival_on.nil?) ? USE_FOR_FESTIVAL : @festival_on
    end

    def self.festival_enabled=(value)
      @festival_on = value ? true : false
    end

    def self.log(msg)
      echoln("[Prismfall Bosses] #{msg}") if defined?(echoln)
      PBDebug.log("[Prismfall Bosses] #{msg}") if defined?(PBDebug)
    end

    # {1}.. placeholders; a battler name starting with "The " is lower-cased when
    # it lands mid-sentence ("A cable around the wild Zekrom snapped!").
    def self.text(str, *args)
      ret = _INTL(str.to_s)
      return ret.gsub(/\{(\d+)\}/) do
        idx = $1.to_i - 1
        next $~[0] if idx < 0 || idx >= args.length
        val = args[idx].to_s
        before = $~.pre_match
        mid_sentence = !before.strip.empty? && before !~ /[.!?…]\s*\z/
        (mid_sentence && val.start_with?("The ")) ? "the " + val[4..] : val
      end
    end

    def self.difficulty
      return Prismfall::Difficulty.current if defined?(Prismfall::Difficulty) && Prismfall::Difficulty.respond_to?(:current)
      return :STANDARD
    end

    def self.difficulty_hash?(value)
      return value.is_a?(Hash) && !value.empty? && value.keys.all? { |k| DIFFICULTY_KEYS.include?(k) }
    end

    # Resolves a definition value: a proc is called with args, and a Hash keyed by
    # difficulty ({ :CASUAL => 2, :HARD => 4, :default => 3 }) picks the current mode.
    def self.resolve(value, *args)
      value = value.call(*args) if value.is_a?(Proc)
      if difficulty_hash?(value)
        d = difficulty
        value = (value.key?(d)) ? value[d] : (value.key?(:default) ? value[:default] : value[:STANDARD])
      end
      return value
    end

    def self.bars_for(data)
      n = resolve(data[:bars])
      n = DEFAULT_BARS if !n.is_a?(Integer)
      return [n, 1].max
    end

    def self.stat_mults(pkmn)
      data = get(pkmn.prismfall_boss_id)
      return nil if !data
      m = resolve(data[:stat_mults])
      return (m.is_a?(Hash) && !m.empty?) ? m : nil
    end

    def self.harmony_lean?
      return false if !defined?(Prismfall::Resonance)
      if Prismfall::Resonance.respond_to?(:band)
        return [:harmony_leaning, :harmony].include?(Prismfall::Resonance.band)
      end
      return Prismfall::Resonance.value.to_i > 0
    end

    #---------------------------------------------------------------------------
    # Pokémon creation
    #---------------------------------------------------------------------------
    # A fresh boss Pokémon from a definition (species and level required).
    def self.create_pokemon(id, level = nil)
      data = get(id)
      raise ArgumentError, "Unknown boss #{id.inspect}" if !data
      raise ArgumentError, "Boss #{id} has no :species" if !data[:species]
      level ||= resolve(data[:level]) || 50
      pkmn = Pokemon.new(data[:species], level)
      apply_overrides(pkmn, data)
      pkmn.prismfall_boss_id = id
      pkmn.calc_stats
      pkmn.heal
      return pkmn
    end

    # Turns an existing Pokémon (e.g. a trainer's ace) into a boss. Only the
    # definition keys that are present are applied; species/level are kept.
    def self.make_boss(pkmn, id)
      data = get(id)
      raise ArgumentError, "Unknown boss #{id.inspect}" if !data
      return nil if !pkmn || pkmn.egg?
      apply_overrides(pkmn, data)
      pkmn.prismfall_boss_id = id
      pkmn.calc_stats
      pkmn.heal
      return pkmn
    end

    # Removes boss status (after battle / on capture) and recalculates stats.
    def self.strip(pkmn)
      return if !pkmn || !pkmn.respond_to?(:prismfall_boss_id) || !pkmn.prismfall_boss_id
      pkmn.prismfall_boss_id = nil
      pkmn.calc_stats
    end

    def self.apply_overrides(pkmn, data)
      form = resolve(data[:form])
      pkmn.form = form if form.is_a?(Integer)
      pkmn.name = data[:nickname] if data[:nickname]
      pkmn.shiny = resolve(data[:shiny]) ? true : false if data.key?(:shiny)
      g = resolve(data[:gender])
      pkmn.gender = g if g.is_a?(Integer)
      moves = resolve(data[:moves])
      if moves.is_a?(Array) && !moves.empty?
        pkmn.forget_all_moves
        moves.compact.first(Pokemon::MAX_MOVES).each { |m| pkmn.learn_move(m) }
      end
      ai = resolve(data[:ability_index])
      pkmn.ability_index = ai if ai.is_a?(Integer)
      ab = resolve(data[:ability])
      pkmn.ability = ab if ab
      it = resolve(data[:item])
      pkmn.item = it if data.key?(:item)
      nat = resolve(data[:nature])
      pkmn.nature = nat if nat
      ivs = resolve(data[:ivs])
      if ivs.is_a?(Integer)
        GameData::Stat.each_main { |s| pkmn.iv[s.id] = ivs }
      elsif ivs.is_a?(Hash)
        ivs.each { |s, v| pkmn.iv[s] = v }
      end
      evs = resolve(data[:evs])
      evs.each { |s, v| pkmn.ev[s] = v } if evs.is_a?(Hash)
      return pkmn
    end
  end
end

#===============================================================================
# Pokémon: boss marker (a Symbol only, so it's Marshal-safe) and stat multipliers.
#===============================================================================
class Pokemon
  attr_accessor :prismfall_boss_id

  alias prismfall_bosses_calc_stats calc_stats unless method_defined?(:prismfall_bosses_calc_stats)

  def calc_stats
    old_total = @totalhp || 0
    old_hp    = @hp || 0
    prismfall_bosses_calc_stats
    return if !@prismfall_boss_id
    mults = Prismfall::Bosses.stat_mults(self)
    return if !mults
    hpm = mults[:HP]
    if hpm.is_a?(Numeric) && hpm != 1
      new_total = [(@totalhp * hpm).round, 1].max
      diff = new_total - old_total
      @totalhp = new_total
      @hp = (old_hp > 0 || diff > 0) ? [[old_hp + diff, 1].max, new_total].min : 0
    end
    { :ATTACK => :@attack, :DEFENSE => :@defense, :SPECIAL_ATTACK => :@spatk,
      :SPECIAL_DEFENSE => :@spdef, :SPEED => :@speed }.each do |stat, ivar|
      m = mults[stat]
      next if !m.is_a?(Numeric) || m == 1
      instance_variable_set(ivar, [(instance_variable_get(ivar) * m).round, 1].max)
    end
  end
end
