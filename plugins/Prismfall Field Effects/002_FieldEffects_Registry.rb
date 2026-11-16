#===============================================================================
# Prismfall Field Effects - registry, definitions, events, utilities
#-------------------------------------------------------------------------------
# Nothing in this file touches Essentials at load time (plugins are evaluated
# before game data is loaded), only inside methods.
#===============================================================================
module FieldEffects
  @registry      = {}   # id => frozen definition Hash
  @stage_cache   = {}   # [id, stage] => merged definition
  @borrow_cache  = {}   # [id, stage] => borrowable view of definition

  #=============================================================================
  # Registration
  #=============================================================================
  # FieldEffects.register(:ID, { name: ..., backdrop: ..., intro_message: ..., ... })
  # Registering the same ID twice replaces the earlier definition (with a warning).
  def self.register(id, definition)
    raise ArgumentError, "FieldEffects.register: ID must be a Symbol (got #{id.inspect})" if !id.is_a?(Symbol)
    raise ArgumentError, "FieldEffects.register(:#{id}): definition must be a Hash" if !definition.is_a?(Hash)
    raise ArgumentError, "FieldEffects.register: :NONE is reserved" if id == NONE
    problems = self.quick_check(id, definition)
    problems.each { |msg| self.log_warning(msg) }
    self.log_warning("Field :#{id} registered twice; the later definition wins.") if @registry[id]
    defn = definition.dup
    defn[:id] = id
    self.normalize!(defn)
    defn[:stages]&.each_value { |stage_defn| self.normalize!(stage_defn) }
    @registry[id] = defn.freeze
    @stage_cache.delete_if { |k, _v| k[0] == id }
    @borrow_cache.delete_if { |k, _v| k[0] == id }
    return id
  end

  def self.unregister(id)
    @registry.delete(id)
    @stage_cache.delete_if { |k, _v| k[0] == id }
    @borrow_cache.delete_if { |k, _v| k[0] == id }
  end

  def self.exists?(id);  return @registry.key?(id); end
  def self.get(id);      return @registry[id];      end
  def self.[](id);       return @registry[id];      end
  def self.ids;          return @registry.keys;     end
  def self.each(&block); @registry.each(&block);    end

  def self.name_of(id)
    return "" if id.nil? || id == NONE
    return @registry[id] ? @registry[id][:name] : id.to_s
  end

  # Definition with a stage's overrides merged in (stage 1 = base definition).
  def self.definition_for(id, stage = 1)
    base = @registry[id]
    return nil if !base
    return base if stage.nil? || stage <= 1 || !base[:stages] || !base[:stages][stage]
    key = [id, stage]
    return @stage_cache[key] ||= base.merge(base[:stages][stage]).freeze
  end

  # Number of stages a field has (1 if it doesn't use :stages).
  def self.max_stage(id)
    defn = @registry[id]
    return 1 if !defn || !defn[:stages] || defn[:stages].empty?
    return [defn[:stages].keys.max, 1].max
  end

  # The subset of a definition another field may borrow (see :borrow).
  def self.borrowable_view(id, stage = 1)
    key = [id, stage || 1]
    return @borrow_cache[key] if @borrow_cache.key?(key)
    defn = self.definition_for(id, stage)
    return nil if !defn
    view = { :id => id, :name => defn[:name], :borrowed => true }
    BORROWABLE_KEYS.each do |k|
      next if !defn.key?(k)
      if k == :hooks
        hooks = defn[:hooks].select { |hk, _v| BORROWABLE_HOOKS.include?(hk) }
        view[:hooks] = hooks if !hooks.empty?
      else
        view[k] = defn[k]
      end
    end
    return @borrow_cache[key] = view.freeze
  end

  #=============================================================================
  # Normalisation (makes the runtime simpler: lists are always Arrays)
  #=============================================================================
  def self.normalize!(defn)
    RULE_KEYS.each_key do |k|
      next if !defn.key?(k)
      defn[k] = [defn[k]] if defn[k].is_a?(Hash)
      defn[k] = defn[k].map { |rule| self.normalize_rule(rule) }.freeze
    end
    defn[:negated_abilities] = Array(defn[:negated_abilities]).freeze if defn.key?(:negated_abilities)
    [:weather, :terrain].each do |k|
      next if !defn[k]
      spec = defn[k].dup
      spec[:block] = Array(spec[:block]).freeze if spec.key?(:block)
      defn[k] = spec.freeze
    end
    if defn[:borrow]
      b = { :pool => :all, :exclude => [], :interval => 3, :count => 1, :order => :random,
            :start_immediately => true }.merge(defn[:borrow])
      b[:exclude] = Array(b[:exclude])
      defn[:borrow] = b.freeze
    end
    defn[:hooks] = defn[:hooks].dup.freeze if defn[:hooks]
    return defn
  end

  # Rule-level keys whose value may be given as a single element or an Array.
  RULE_ARRAY_KEYS = [:moves, :not_moves, :types, :not_types, :flags, :function_codes,
                     :category, :weather, :terrain, :attack, :defend, :effects].freeze
  # Battler-matcher keys (inside user:/target:/battlers:) that are lists.
  MATCHER_ARRAY_KEYS = [:types, :not_types, :abilities, :not_abilities, :items,
                        :not_items, :status].freeze

  def self.normalize_rule(rule)
    return rule if !rule.is_a?(Hash)
    r = rule.dup
    RULE_ARRAY_KEYS.each { |k| r[k] = Array(r[k]).freeze if r.key?(k) }
    if r.key?(:rewind) && !r[:rewind].is_a?(Hash)
      r[:rewind] = Array(r[:rewind]).map { |tid| [tid, 1] }.to_h.freeze
    end
    [:user, :target, :battlers].each do |k|
      next if !r[k].is_a?(Hash)
      m = r[k].dup
      MATCHER_ARRAY_KEYS.each { |mk| m[mk] = Array(m[mk]).freeze if m.key?(mk) }
      r[k] = m.freeze
    end
    return r.freeze
  end

  # Cheap registration-time checks (the full check is tools/validate_fields.rb).
  def self.quick_check(id, defn)
    ret = []
    REQUIRED_KEYS.each do |k|
      ret.push("Field :#{id} is missing required key :#{k}.") if !defn[k].is_a?(String)
    end
    defn.each_key do |k|
      next if TOP_LEVEL_KEYS.key?(k)
      ret.push("Field :#{id} uses unknown key :#{k} (ignored).")
    end
    RULE_KEYS.each do |k, allowed|
      next if !defn[k]
      Array(defn[k].is_a?(Hash) ? [defn[k]] : defn[k]).each do |rule|
        next if !rule.is_a?(Hash)
        rule.each_key do |rk|
          ret.push("Field :#{id} :#{k} rule uses unknown key :#{rk}.") if !allowed.include?(rk)
        end
      end
    end
    defn[:hooks]&.each_key do |hk|
      ret.push("Field :#{id} uses unknown hook :#{hk}.") if !HOOK_KEYS.include?(hk)
    end
    return ret
  end

  #=============================================================================
  # Events (LOCKED contract)
  #=============================================================================
  # Must be called on every field change. The EBDX Bridge listens to this.
  #   EventHandlers.add(:prismfall_field_changed, :my_key,
  #     proc { |battle, old_id, new_id| ... })
  # NOTE: A stage change (see :stages) also calls this with old_id == new_id.
  def self.notify_change(battle, old_id, new_id)
    EventHandlers.trigger(:prismfall_field_changed, battle, old_id, new_id)
  end

  # Extra (non-LOCKED) event for overlay changes made by :borrow (e.g. :BLEED).
  #   proc { |battle, field_id, old_borrowed_ids, new_borrowed_ids| ... }
  def self.notify_overlay_change(battle, field_id, old_ids, new_ids)
    EventHandlers.trigger(:prismfall_field_overlay_changed, battle, field_id, old_ids, new_ids)
  end

  #=============================================================================
  # Logging and safe proc calls
  #=============================================================================
  def self.log(msg)
    PBDebug.log("[Field Effects] #{msg}") if defined?(PBDebug)
  end

  def self.log_warning(msg)
    if defined?(Console) && Console.respond_to?(:echo_warn)
      Console.echo_warn("[Prismfall Field Effects] #{msg}")
    else
      echoln("[Prismfall Field Effects] WARNING: #{msg}") if defined?(echoln)
    end
  end

  # Calls a definition-supplied Proc. Errors are logged (and re-raised in Debug
  # mode) so a broken field can't silently soft-lock a release build.
  def self.safe_call(callable, *args)
    return nil if !callable
    return callable.call(*args)
  rescue StandardError => e
    self.log("Error in field proc: #{e.class}: #{e.message}\n#{e.backtrace&.first(5)&.join("\n")}")
    raise if $DEBUG
    return nil
  end

  # Formats a definition message with _INTL ({1}, {2}... substitution).
  def self.format(text, *args)
    return nil if text.nil?
    ret = (defined?(_INTL)) ? _INTL(text) : text.dup   # translate first, then fill the placeholders
    return self.fill_placeholders(ret, args)
  end

  # Replaces {1}, {2}... A battler name that starts with "The " ("The wild X",
  # "The opposing X") is lower-cased when its placeholder is not at the start of
  # a sentence, so "Lightning struck {1}!" reads "...struck the opposing X!".
  def self.fill_placeholders(text, args)
    return text.gsub(/\{(\d+)\}/) do
      idx = $1.to_i - 1
      next $~[0] if idx < 0 || idx >= args.length
      str = args[idx].to_s
      before = $~.pre_match
      mid_sentence = !before.strip.empty? && before !~ /[.!?…]\s*\z/
      (mid_sentence && str.start_with?("The ")) ? "the " + str[4..] : str
    end
  end
end
