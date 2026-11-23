#===============================================================================
# Prismfall Core - 013 Narrative state: Bonds, Standing, Resonance, Choices
#-------------------------------------------------------------------------------
# Stored in Prismfall.state.narrative (part of the save file; plain Hash of
# Symbols/Integers). Event helpers at the bottom (pf_bond, pf_choose, ...).
#===============================================================================
class Prismfall::SaveState
  attr_writer :narrative

  def narrative
    @narrative = {} if !@narrative.is_a?(Hash)
    n = @narrative
    n[:bonds]      ||= {}
    n[:standing]   ||= {}
    n[:resonance]  ||= Prismfall::Narrative::RESONANCE_START
    n[:choices]    ||= {}
    n[:choice_log] ||= []   # [[key, value, play_time, map_id], ...]
    n[:history]    ||= []   # [[kind, id, old, new], ...] (debug aid, capped)
    n[:passwords]  ||= {}   # password id => true / parameter
    n[:endings]    ||= []   # endings reached in THIS save
    n[:ending]     = nil if !n.has_key?(:ending)
    n[:postgame]   = false if !n.has_key?(:postgame)
    n[:ruin_route] = false if !n.has_key?(:ruin_route)
    return n
  end
end

module Prismfall
  module Narrative
    def self.store
      return Prismfall.state.narrative
    end

    def self.warn(msg)
      return if !WARN_UNREGISTERED || !$DEBUG
      if defined?(Console) && Console.respond_to?(:echo_warn)
        Console.echo_warn("[Prismfall] #{msg}")
      elsif defined?(echoln)
        echoln("[Prismfall] #{msg}")
      end
    end

    def self.tier_for(value, tiers)
      ret = tiers[0][1]
      tiers.each { |bound, tier| ret = tier if value >= bound }
      return ret
    end

    def self.play_time
      return ($stats) ? $stats.play_time.to_i : 0
    end

    def self.record_history(kind, id, old, new)
      h = store[:history]
      h.push([kind, id, old, new])
      h.shift while h.length > HISTORY_LIMIT
      EventHandlers.trigger(:prismfall_narrative_changed, kind, id, old, new)
      refresh_mirrors
    end

    #---------------------------------------------------------------------------
    # Derived flags / tallies (NARRATIVE_KEYS section 5)
    #---------------------------------------------------------------------------
    @flag_stack = []

    def self.flag(name)
      name = name.to_sym
      cond = DERIVED_FLAGS[name]
      if cond.nil?
        warn("Unknown derived flag #{name.inspect}")
        return false
      end
      raise Prismfall::Conditions::Error, "Flag cycle: #{(@flag_stack + [name]).join(' -> ')}" if @flag_stack.include?(name)
      @flag_stack.push(name)
      begin
        return Prismfall::Conditions.evaluate(cond)
      ensure
        @flag_stack.pop
      end
    end

    def self.tally(name)
      list = TALLIES[name.to_sym]
      if !list
        warn("Unknown tally #{name.inspect}")
        return 0
      end
      return list.count { |cond| Prismfall::Conditions.evaluate(cond) }
    end

    # Writes MIRROR_SWITCHES (S193, S221-S232) from their conditions.
    def self.refresh_mirrors
      return if !MIRRORS_ENABLED || !$game_switches
      changed = false
      MIRROR_SWITCHES.each do |sw, cond|
        v = (Prismfall::Conditions.evaluate(cond) rescue false) ? true : false
        next if $game_switches[sw] == v
        $game_switches[sw] = v
        changed = true
      end
      $game_map.need_refresh = true if changed && $game_map
    end

    # Applies an effects string such as "MERIDIAN+2 VOSS+1 RES-1". Shows
    # "X will remember that." for each Bond whose tier changed (if show).
    def self.apply_effects(text, show = true)
      return if text.nil? || text.strip.empty?
      toasts = []
      text.split(/\s+/).each do |tok|
        m = /\A([A-Za-z_]+)([+-]\d+)\z/.match(tok)
        if !m
          warn("Bad effect token #{tok.inspect}")
          next
        end
        id = m[1].upcase.to_sym
        delta = m[2].to_i
        if id == :RES
          Resonance.shift(delta)
        elsif BONDS.has_key?(id)
          old_tier = Bonds.tier(id)
          Bonds.add(id, delta)
          toasts.push(id) if Bonds.tier(id) != old_tier && !toasts.include?(id)
        elsif FACTIONS.has_key?(id)
          Standing.add(id, delta)
        else
          warn("Effect token #{tok.inspect} names no Bond/faction")
        end
      end
      return if !show
      toasts.each do |id|
        text = (Bonds.get(id) >= 0) ? BOND_UP_TEXT : BOND_DOWN_TEXT
        pbMessage("\\se[]" + _INTL(text, Bonds.display_name(id))) if text
      end
    end

    # Shared logic for Bonds and Standing (bounded integer meters).
    module MeterMethods
      def definition(id)
        entry = table[id]
        Prismfall::Narrative.warn("Unregistered #{kind} #{id.inspect}") if !entry
        return defaults.merge(entry || {})
      end

      def get(id)
        id = id.to_sym
        v = Prismfall::Narrative.store[store_key][id]
        return (v.nil?) ? definition(id)[:start] : v
      end

      def set(id, value)
        id = id.to_sym
        d = definition(id)
        old = get(id)
        new = value.to_i.clamp(d[:min], d[:max])
        Prismfall::Narrative.store[store_key][id] = new
        Prismfall::Narrative.record_history(kind, id, old, new) if old != new
        return new
      end

      def add(id, delta)
        return set(id, get(id) + delta.to_i)
      end

      def tier(id)
        return Prismfall::Narrative.tier_for(get(id), tiers)
      end

      def at_least?(id, value)
        return get(id) >= value
      end

      def display_name(id)
        return _INTL(definition(id)[:name] || id.to_s)
      end

      def all
        return table.keys.map { |id| [id, get(id)] }
      end
    end

    module Bonds
      extend MeterMethods
      def self.kind;      return :bond;                 end
      def self.table;     return Narrative::BONDS;        end
      def self.defaults;  return Narrative::BOND_DEFAULT; end
      def self.tiers;     return Narrative::BOND_TIERS;   end
      def self.store_key; return :bonds;                end

      # add with optional "X will remember that." feedback
      def self.change(id, delta, show = false)
        old = get(id)
        new = add(id, delta)
        if show && new != old
          text = (new > old) ? Narrative::BOND_UP_TEXT : Narrative::BOND_DOWN_TEXT
          pbMessage("\\se[]" + _INTL(text, display_name(id))) if text
        end
        return new
      end
    end

    module Standing
      extend MeterMethods
      def self.kind;      return :standing;                 end
      def self.table;     return Narrative::FACTIONS;         end
      def self.defaults;  return Narrative::STANDING_DEFAULT; end
      def self.tiers;     return Narrative::STANDING_TIERS;   end
      def self.store_key; return :standing;                 end
    end

    module Resonance
      def self.value
        return Narrative.store[:resonance]
      end

      def self.set(v)
        old = value
        new = v.to_i.clamp(Narrative::RESONANCE_MIN, Narrative::RESONANCE_MAX)
        Narrative.store[:resonance] = new
        Narrative.record_history(:resonance, :RESONANCE, old, new) if old != new
        return new
      end

      # The 'colorless' password halves every Resonance swing (toward 0).
      def self.shift(delta)
        delta = delta.to_i
        delta = (delta.abs / 2) * (delta <=> 0) if defined?(Prismfall::Passwords) && Prismfall::Passwords.active?(:COLORLESS)
        return set(value + delta)
      end
      def self.harmony(n = 1); return shift(n.abs);            end
      def self.ruin(n = 1);    return shift(-n.abs);           end

      def self.band
        return Narrative.tier_for(value, Narrative::RESONANCE_BANDS)
      end
    end

    module Choices
      # Resolves legacy/map aliases (CHOICE_ALIASES, or an UPPERCASE key whose
      # lowercase form is registered) to the canonical key.
      def self.canonical(key)
        key = key.to_sym
        return Narrative::CHOICE_ALIASES[key] if Narrative::CHOICE_ALIASES.has_key?(key)
        down = key.to_s.downcase.to_sym
        return down if !Narrative::CHOICES.has_key?(key) && Narrative::CHOICES.has_key?(down)
        return key
      end

      def self.legacy_alias?(key)
        return Narrative::CHOICE_ALIASES.has_key?(key.to_sym)
      end

      def self.definition(key)
        key = canonical(key)
        d = Narrative::CHOICES[key]
        Narrative.warn("Unregistered choice #{key.inspect}") if !d
        return d || {}
      end

      def self.get(key)
        return Narrative.store[:choices][canonical(key)]
      end

      def self.made?(key)
        return Narrative.store[:choices].has_key?(canonical(key))
      end

      # Records a decision. Returns false if refused (:once and already made).
      def self.make(key, value, show_effects = true)
        skip_effects = Narrative::LEGACY_ALIASES_SKIP_EFFECTS && legacy_alias?(key)
        key = canonical(key)
        d = definition(key)
        if d[:values] && !d[:values].include?(value)
          raise ArgumentError, "Choice #{key.inspect} doesn't allow #{value.inspect} (allowed: #{d[:values].inspect})" if $DEBUG
          Narrative.warn("Choice #{key.inspect} got unlisted value #{value.inspect}")
        end
        return false if d[:once] && made?(key) && get(key) != value
        old = get(key)
        first_time = !made?(key)
        Narrative.store[:choices][key] = value
        map_id = ($game_map) ? $game_map.map_id : 0
        Narrative.store[:choice_log].push([key, value, Narrative.play_time, map_id])
        Narrative.record_history(:choice, key, old, value) if old != value
        if first_time && !skip_effects
          effects = (Narrative::CHOICE_EFFECTS[key] || {})[value]
          Narrative.apply_effects(effects, show_effects)
        end
        return true
      end

      def self.log
        return Narrative.store[:choice_log]
      end

      def self.clear(key)   # debug / story resets
        Narrative.store[:choices].delete(canonical(key))
      end
    end
  end

  Bonds     = Narrative::Bonds
  Standing  = Narrative::Standing
  Resonance = Narrative::Resonance
  Choices   = Narrative::Choices
end

#===============================================================================
# Event helpers (Script commands / Conditional Branch > Script)
#===============================================================================
def pf_bond(id);                          return Prismfall::Bonds.get(id);                  end
def pf_bond_add(id, delta, show = false); return Prismfall::Bonds.change(id, delta, show);  end
def pf_bond_set(id, value);               return Prismfall::Bonds.set(id, value);           end
def pf_bond_tier(id);                     return Prismfall::Bonds.tier(id);                 end
def pf_standing(faction);                 return Prismfall::Standing.get(faction);          end
def pf_standing_add(faction, delta);      return Prismfall::Standing.add(faction, delta);   end
def pf_standing_tier(faction);            return Prismfall::Standing.tier(faction);         end
def pf_resonance;                         return Prismfall::Resonance.value;                end
def pf_resonance_add(delta);              return Prismfall::Resonance.shift(delta);         end
def pf_choice(key);                       return Prismfall::Choices.get(key);               end
def pf_choose(key, value);                return Prismfall::Choices.make(key, value);       end
def pf_chose?(key, value);                return Prismfall::Choices.get(key) == value;      end
def pf_cond(text);                        return Prismfall::Conditions.evaluate(text);      end
def pf_flag(name);                        return Prismfall::Narrative.flag(name);           end
def pf_tally(name);                       return Prismfall::Narrative.tally(name);          end
