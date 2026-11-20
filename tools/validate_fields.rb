#!/usr/bin/env ruby
# frozen_string_literal: true
#===============================================================================
# Prismfall field definition validator (no Essentials runtime needed).
#
#   ruby tools/validate_fields.rb [PBS_DIR]
#
# Loads the DSL schema (plugin file 001_FieldEffects_Schema.rb, pure data),
# stubs FieldEffects.register, loads every 1xx_Field_*.rb file and checks:
#   * every key is a known DSL key (top level, rules, matchers, hooks, specs)
#   * every type/move/ability/item/flag/function code exists in PBS_DIR
#     (default /home/claude/ref/ebdx/PBS = Essentials 21.1 + Gen 9 Pack) or in
#     our pbs/items_*.txt (seed items)
#   * value shapes (fractions, chances, multipliers, procs, transition targets)
# Exit code 1 if any error was found.
#===============================================================================
ROOT       = File.expand_path("..", __dir__)
PLUGIN_DIR = File.join(ROOT, "plugins", "Prismfall Field Effects")
PBS_DIR    = ARGV[0] || "/home/claude/ref/ebdx/PBS"

load File.join(PLUGIN_DIR, "001_FieldEffects_Schema.rb")

module FieldEffects
  @registered = {}   # id => [definition, file]
  @current_file = nil
  class << self
    attr_reader :registered
    attr_accessor :current_file
  end

  def self.register(id, definition)
    (@registered[id] ||= []).push([definition, @current_file])
    return id
  end
end

#-------------------------------------------------------------------------------
# PBS parsing
#-------------------------------------------------------------------------------
def pbs_sections(path)
  ret = {}
  return ret if !File.exist?(path)
  current = nil
  File.foreach(path, encoding: "bom|utf-8") do |line|
    line = line.strip
    next if line.empty? || line.start_with?("#")
    if line =~ /^\[\s*([^\],]+?)\s*(?:,[^\]]*)?\]$/
      current = (ret[$1.upcase.to_sym] ||= {})
    elsif current && line =~ /^(\w+)\s*=\s*(.*)$/
      current[$1] = $2.strip
    end
  end
  return ret
end

abort("PBS directory not found: #{PBS_DIR}") if !File.directory?(PBS_DIR)
TYPES     = pbs_sections(File.join(PBS_DIR, "types.txt")).keys
MOVES_RAW = pbs_sections(File.join(PBS_DIR, "moves.txt"))
MOVES     = MOVES_RAW.keys
ABILITIES = pbs_sections(File.join(PBS_DIR, "abilities.txt")).keys
ITEMS     = pbs_sections(File.join(PBS_DIR, "items.txt")).keys +
            Dir[File.join(ROOT, "pbs", "items*.txt")].flat_map { |f| pbs_sections(f).keys }
FUNCTION_CODES = MOVES_RAW.values.map { |m| m["FunctionCode"] }.compact.uniq
PBS_FLAGS = MOVES_RAW.values.flat_map { |m| (m["Flags"] || "").split(",").map(&:strip) }.uniq

#-------------------------------------------------------------------------------
# Reporting
#-------------------------------------------------------------------------------
$errors = []
$warnings = []
def err(where, msg);  $errors.push("ERROR   #{where}: #{msg}");  end
def warn!(where, msg); $warnings.push("WARNING #{where}: #{msg}"); end

#-------------------------------------------------------------------------------
# Value checks
#-------------------------------------------------------------------------------
def list(v); v.is_a?(Array) ? v : [v]; end

def check_ids(where, value, valid, kind)
  list(value).each do |id|
    if !id.is_a?(Symbol)
      err(where, "#{kind} #{id.inspect} must be a Symbol")
    elsif !valid.include?(id)
      err(where, "unknown #{kind} :#{id}")
    end
  end
end

def check_enum(where, value, valid, kind)
  list(value).each { |v| err(where, "invalid #{kind} #{v.inspect} (expected one of #{valid.inspect})") if !valid.include?(v) }
end

def check_proc(where, v);   err(where, "must be a Proc (proc { ... })") if !v.is_a?(Proc); end
def check_string(where, v); err(where, "must be a String") if !v.is_a?(String); end
def check_bool(where, v);   err(where, "must be true/false") if v != true && v != false; end

def check_positive(where, v)
  err(where, "must be a positive number (got #{v.inspect})") if !v.is_a?(Numeric) || v <= 0
end

def check_int(where, v, min = nil, max = nil)
  if !v.is_a?(Integer)
    err(where, "must be an Integer (got #{v.inspect})")
  elsif (min && v < min) || (max && v > max)
    err(where, "must be in #{min}..#{max} (got #{v})")
  end
end

def check_fraction(where, v)
  if v.is_a?(Integer)
    err(where, "fraction #{v.inspect} is an Integer - write 1/8r or 0.125, not 1/8")
  elsif !v.is_a?(Numeric) || v <= 0 || v > 1
    err(where, "must be a fraction of max HP in (0, 1] (got #{v.inspect})")
  end
end

def check_stats(where, v)
  if !v.is_a?(Hash)
    err(where, "must be a Hash { STAT => n }")
    return
  end
  v.each do |stat, n|
    err(where, "unknown stat #{stat.inspect}") if !FieldEffects::STATS.include?(stat)
    err(where, "stage change for #{stat} must be a non-zero Integer") if !n.is_a?(Integer) || n == 0
  end
end

def check_flags(where, v)
  list(v).each do |f|
    name = f.to_s
    if !FieldEffects::MOVE_FLAGS.any? { |x| x.casecmp?(name) }
      err(where, "unknown move flag #{f.inspect}")
    elsif !PBS_FLAGS.any? { |x| x.casecmp?(name) }
      warn!(where, "flag #{f.inspect} is not used by any move in PBS")
    end
  end
end

def check_field_target(where, v, all_ids)
  return if v.is_a?(Proc) || v == :NONE
  if !v.is_a?(Symbol)
    err(where, "transition target must be a field Symbol, :NONE or a Proc")
  elsif !FieldEffects::KNOWN_FIELDS.include?(v) && !all_ids.include?(v)
    err(where, "transition target :#{v} is not in the SPINE roster or registered")
  elsif !all_ids.include?(v)
    warn!(where, "transition target :#{v} is not implemented yet (roster field)")
  end
end

def check_battler_matcher(where, m)
  if !m.is_a?(Hash)
    err(where, "battler matcher must be a Hash")
    return
  end
  m.each do |k, v|
    w = "#{where}[:#{k}]"
    case k
    when :types, :not_types         then check_ids(w, v, TYPES, "type")
    when :abilities, :not_abilities then check_ids(w, v, ABILITIES, "ability")
    when :items, :not_items         then check_ids(w, v, ITEMS, "item")
    when :grounded                  then check_bool(w, v)
    when :status                    then check_enum(w, v, FieldEffects::STATUSES, "status")
    when :condition                 then check_proc(w, v)
    when :hp_below, :hp_above
      err(w, "must be a fraction of max HP in (0, 1]") if !v.is_a?(Numeric) || v <= 0 || v > 1 || v.is_a?(Integer)
    when :in_weather                then check_enum(w, v, FieldEffects::WEATHERS, "weather")
    when :on_terrain                then check_enum(w, v, FieldEffects::TERRAINS, "terrain")
    else err(where, "unknown battler matcher key :#{k}")
    end
  end
end

# Checks one rule of list `key`.
def check_rule(where, key, rule, all_ids)
  if !rule.is_a?(Hash)
    err(where, "rule must be a Hash")
    return
  end
  allowed = FieldEffects::RULE_KEYS[key]
  rule.each do |k, v|
    w = "#{where}[:#{k}]"
    if !allowed.include?(k)
      err(where, "unknown key :#{k} for :#{key} (allowed: #{allowed.join(', ')})")
      next
    end
    case k
    when :moves, :not_moves             then check_ids(w, v, MOVES, "move")
    when :types, :not_types, :attack, :defend, :damage_type then check_ids(w, v, TYPES, "type")
    when :flags                         then check_flags(w, v)
    when :category                      then check_enum(w, v, FieldEffects::CATEGORIES, "category")
    when :function_codes
      list(v).each { |fc| err(w, "unknown function code #{fc.inspect}") if !FUNCTION_CODES.include?(fc) }
    when :user, :target, :battlers      then check_battler_matcher(w, v)
    when :condition, :proc, :check      then check_proc(w, v)
    when :mult, :attack_mult, :defense_mult, :final_mult, :evasion_mult then check_positive(w, v)
    when :message, :progress_message    then check_string(w, v)
    when :animation                     then check_string(w, v)
    when :chance                        then check_int(w, v, 1, 100)
    when :apply_to                      then check_enum(w, v, FieldEffects::APPLY_TO, "apply_to")
    when :status
      check_enum(w, v, FieldEffects::STATUSES - [:NONE], "status")
    when :in_weather                    then check_enum(w, v, FieldEffects::WEATHERS, "weather")
    when :on_terrain                    then check_enum(w, v, FieldEffects::TERRAINS, "terrain")
    when :add_type                      then check_ids(w, v, TYPES, "type")
    when :boost                         then check_bool(w, v)
    when :stats, :user_stats, :target_stats then check_stats(w, v)
    when :damage, :heal                 then check_fraction(w, v)
    when :effects                       then check_enum(w, v, FieldEffects::BATTLER_EFFECTS, "battler effect")
    when :confuse, :flinch, :cure_status, :always_hit, :always, :also_on_change, :even_if_failed, :strike_turn
      check_bool(w, v)
    when :item
      check_ids(w, v, ITEMS, "item")
      warn!(w, ":#{v} is not one of the four field seeds") if !FieldEffects::SEED_ITEMS.include?(v)
    when :weather                       then check_enum(w, v, FieldEffects::WEATHERS - [:None], "weather")
    when :terrain                       then check_enum(w, v, FieldEffects::TERRAINS - [:None], "terrain")
    when :uses, :turns                  then check_int(w, v, 1)
    when :as                            then check_enum(w, v, FieldEffects::WEATHERS - [:None], "weather")
    when :id                            then err(w, "transition :id must be a Symbol") if !v.is_a?(Symbol)
    when :rewind
      ok = v.is_a?(Symbol) || (v.is_a?(Array) && v.all? { |x| x.is_a?(Symbol) }) ||
           (v.is_a?(Hash) && v.all? { |x, n| x.is_a?(Symbol) && n.is_a?(Integer) && n > 0 })
      err(w, ":rewind must be a transition :id, a list of ids or { id => n }") if !ok
    when :stage                         then check_int(w, v, 1)
    when :stage_delta                   then check_int(w, v)
    when :to
      if key == :type_changes
        check_ids(w, v, TYPES, "type")
      else
        check_field_target(w, v, all_ids)
      end
    when :add
      if [:priority_mods, :crit_mods].include?(key)
        check_int(w, v)
      else
        check_ids(w, v, TYPES, "type")
      end
    when :set
      case key
      when :effectiveness_mods then err(w, "must be a number >= 0") if !v.is_a?(Numeric) || v < 0
      when :fixed_damage_mods  then check_int(w, v, 1)
      else                          check_int(w, v, 1, 100)
      end
    end
  end
  # Rule-specific requirements
  case key
  when :damage_mods
    if !(rule.keys & [:mult, :attack_mult, :defense_mult, :final_mult]).any?
      err(where, "damage rule has no multiplier (:mult/:attack_mult/:defense_mult/:final_mult)")
    end
  when :type_changes then err(where, "type change needs :to") if !rule[:to]
  when :extra_types  then err(where, "extra type needs :add") if !rule[:add]
  when :priority_mods then err(where, "priority rule needs :add") if !rule[:add]
  when :speed_mods   then err(where, "speed rule needs :mult") if !rule[:mult]
  when :effectiveness_mods
    err(where, "effectiveness rule needs :set or :mult") if !rule.key?(:set) && !rule[:mult]
  when :fixed_damage_mods
    err(where, "fixed damage rule needs :set or :mult") if !rule[:set] && !rule[:mult]
  when :weather_as
    err(where, "weather_as rule needs :as") if !rule[:as]
  when :move_stat_boosts
    err(where, "needs :user_stats or :target_stats") if !rule[:user_stats] && !rule[:target_stats]
  when :transitions
    if !rule.key?(:to) && !rule[:stage] && !rule[:stage_delta] && !rule[:rewind]
      err(where, "transition needs :to, :stage, :stage_delta or :rewind")
    end
    triggers = [:weather, :terrain, :turns, :check].count { |t| rule.key?(t) }
    move_keys = (rule.keys & FieldEffects::MOVE_MATCH_KEYS)
    if triggers > 1
      err(where, "transition has more than one trigger (:weather/:terrain/:turns/:check)")
    elsif triggers == 0 && move_keys.empty?
      err(where, "transition has no trigger (move matcher keys, :weather, :terrain, :turns or :check)")
    elsif triggers == 1 && !move_keys.empty?
      warn!(where, "move matcher keys are ignored on a non-move transition")
    end
  when :end_of_round, :on_entry, :seed
    err(where, "seed rule needs :item") if key == :seed && !rule[:item]
    actions = [:damage, :heal, :status, :confuse, :cure_status, :stats, :effects, :proc, :add_type]
    err(where, "battler effect does nothing (no #{actions.join('/')})") if (rule.keys & actions).empty?
    warn!(where, ":damage_type without :damage does nothing") if rule[:damage_type] && !rule[:damage]
  end
end

def check_env_spec(where, spec, valid)
  if !spec.is_a?(Hash)
    err(where, "must be a Hash")
    return
  end
  spec.each do |k, v|
    w = "#{where}[:#{k}]"
    case k
    when :block         then check_enum(w, v, valid, "id")
    when :block_message then check_string(w, v)
    when :transform
      if !v.is_a?(Hash) then err(w, "must be a Hash { from => to }")
      else v.each { |a, b| check_enum(w, [a, b], valid, "id") }
      end
    when :extend
      if !v.is_a?(Hash) then err(w, "must be a Hash { id => turns }")
      else v.each { |a, n| check_enum(w, a, valid, "id"); check_int(w, n, 1) }
      end
    else err(where, "unknown key :#{k} (allowed: #{FieldEffects::WEATHER_SPEC_KEYS.join(', ')})")
    end
  end
end

def check_definition(where, defn, all_ids, stage = false)
  if !defn.is_a?(Hash)
    err(where, "definition must be a Hash")
    return
  end
  if !stage
    FieldEffects::REQUIRED_KEYS.each { |k| err(where, "missing required key :#{k}") if !defn.key?(k) }
  end
  defn.each do |k, v|
    w = "#{where}[:#{k}]"
    kind = FieldEffects::TOP_LEVEL_KEYS[k]
    if !kind
      err(where, "unknown top-level key :#{k}")
      next
    end
    if stage && FieldEffects::STAGE_FORBIDDEN_KEYS.include?(k)
      err(where, ":#{k} is not allowed inside a stage")
      next
    end
    case kind
    when :string  then check_string(w, v)
    when :string_list then list(v).each { |x| check_string(w, x) }
    when :move    then check_ids(w, v, MOVES, "move")
    when :type    then check_ids(w, v, TYPES, "type")
    when :integer then check_int(w, v, 0, 14)
    when :boolean then check_bool(w, v)
    when :ability_list
      check_ids(w, v, ABILITIES, "ability")
      if k == :activate_abilities
        list(v).each { |a| err(w, ":#{a} can't be activated (supported: #{FieldEffects::ACTIVATABLE_ABILITIES.join(', ')})") if a.is_a?(Symbol) && !FieldEffects::ACTIVATABLE_ABILITIES.include?(a) }
      end
    when :family then check_enum(w, v, FieldEffects::FAMILIES, "family")
    when :duration_hash
      if !v.is_a?(Hash)
        err(w, "must be a Hash { MOVE => turns or [turns, \"message\"] }")
        next
      end
      v.each do |mv, val|
        check_ids(w, mv, MOVES, "move")
        err(w, ":#{mv} has no lingering effect to extend") if !FieldEffects::DURATION_MOVES.include?(mv)
        n, msg = val.is_a?(Array) ? val : [val, nil]
        check_int("#{w}[:#{mv}]", n, 1)
        check_string("#{w}[:#{mv}] message", msg) if msg
      end
    when :type_number_hash, :move_number_hash, :type_string_hash, :move_string_hash
      if !v.is_a?(Hash)
        err(w, "must be a Hash")
        next
      end
      ids = (kind.to_s.start_with?("type")) ? TYPES : MOVES
      v.each do |id, val|
        check_ids(w, id, ids, (ids.equal?(TYPES)) ? "type" : "move")
        (kind.to_s.end_with?("number_hash")) ? check_positive("#{w}[:#{id}]", val) : check_string("#{w}[:#{id}]", val)
      end
      if [:type_messages, :move_messages].include?(k)
        mods = defn[(k == :type_messages) ? :type_mods : :move_mods] || {}
        v.each_key { |id| warn!(w, "message for :#{id} but no matching #{(k == :type_messages) ? ':type_mods' : ':move_mods'} entry") if !mods.key?(id) }
      end
    when :weather_spec then check_env_spec(w, v, FieldEffects::WEATHERS - [:None])
    when :terrain_spec then check_env_spec(w, v, FieldEffects::TERRAINS - [:None])
    when :borrow_spec
      if !v.is_a?(Hash)
        err(w, "must be a Hash")
        next
      end
      v.each do |bk, bv|
        bw = "#{w}[:#{bk}]"
        case bk
        when :pool
          if bv != :all
            list(bv).each { |id| err(bw, "unknown field :#{id}") if !FieldEffects::ROSTER.include?(id) && !all_ids.include?(id) }
          end
        when :exclude then list(bv).each { |id| warn!(bw, ":#{id} is not a roster field") if !FieldEffects::ROSTER.include?(id) && !all_ids.include?(id) }
        when :interval, :count then check_int(bw, bv, 1)
        when :order   then check_enum(bw, bv, FieldEffects::BORROW_ORDERS, "order")
        when :message then check_string(bw, bv)
        when :start_immediately then check_bool(bw, bv)
        else err(w, "unknown borrow key :#{bk}")
        end
      end
    when :hooks
      if !v.is_a?(Hash)
        err(w, "must be a Hash")
        next
      end
      v.each do |hk, hv|
        if !FieldEffects::HOOK_KEYS.include?(hk) then err(w, "unknown hook :#{hk}")
        else check_proc("#{w}[:#{hk}]", hv)
        end
      end
    when :stages
      if stage || !v.is_a?(Hash)
        err(w, "must be a Hash { 2 => {...}, ... } at top level")
        next
      end
      v.each do |n, sdef|
        check_int("#{w} key", n, 2)
        check_definition("#{w}[#{n}]", sdef, all_ids, true)
      end
    when :rules
      rules = v.is_a?(Hash) ? [v] : v
      if !rules.is_a?(Array)
        err(w, "must be a rule Hash or an Array of rule Hashes")
        next
      end
      rules.each_with_index { |rule, i| check_rule("#{w}[#{i}]", k, rule, all_ids) }
      if k == :transitions
        tids = rules.map { |r| r.is_a?(Hash) ? r[:id] : nil }.compact
        tids.select { |t| tids.count(t) > 1 }.uniq.each { |t| err(w, "duplicate transition :id :#{t}") }
        rules.each_with_index do |r, i|
          next if !r.is_a?(Hash) || !r[:rewind]
          refs = r[:rewind].is_a?(Hash) ? r[:rewind].keys : list(r[:rewind])
          refs.each { |t| err("#{w}[#{i}][:rewind]", "no transition with :id :#{t} in this list") if !tids.include?(t) }
        end
      end
    end
  end
end

#-------------------------------------------------------------------------------
# Load field files
#-------------------------------------------------------------------------------
files = Dir[File.join(PLUGIN_DIR, "1*.rb")].sort
abort("No field files found in #{PLUGIN_DIR}") if files.empty?
files.each do |f|
  base = File.basename(f)
  err(base, "field files must be named 1NN_Field_<Name>.rb") if base !~ /\A1\d\d_Field_[A-Za-z0-9_]+\.rb\z/
  before = FieldEffects.registered.values.sum(&:length)
  FieldEffects.current_file = base
  begin
    load f
  rescue Exception => e
    err(base, "failed to load: #{e.class}: #{e.message}")
    next
  end
  added = FieldEffects.registered.values.sum(&:length) - before
  warn!(base, "registers #{added} fields (expected exactly 1)") if added != 1
end

all_ids = FieldEffects.registered.keys
FieldEffects.registered.each do |id, entries|
  if entries.length > 1
    err(":#{id}", "registered #{entries.length} times (#{entries.map(&:last).join(', ')})")
  end
  defn, file = entries.last
  where = "#{file} :#{id}"
  warn!(where, ":#{id} is not in the SPINE roster or EXTRA_FIELDS") if !FieldEffects::KNOWN_FIELDS.include?(id)
  check_definition(where, defn, all_ids)
  if defn.is_a?(Hash) && defn[:family]
    fam_seed = FieldEffects::FAMILY_SEEDS[defn[:family]]
    seeds = list(defn[:seed] || []).map { |r| r.is_a?(Hash) ? r[:item] : nil }.compact
    warn!(where, "no :seed entry for its family seed :#{fam_seed}") if fam_seed && !seeds.include?(fam_seed) && !defn[:borrow]
  end
end

# Seed items must exist in our PBS
FieldEffects::SEED_ITEMS.each do |seed|
  err("pbs/items_fields.txt", "seed item :#{seed} is not defined") if !ITEMS.include?(seed)
end

puts "Prismfall field validator - #{files.length} file(s), #{all_ids.length} field(s): #{all_ids.join(', ')}"
puts "PBS: #{PBS_DIR} (#{TYPES.length} types, #{MOVES.length} moves, #{ABILITIES.length} abilities, #{ITEMS.length} items)"
puts $warnings
puts $errors
puts "#{$errors.length} error(s), #{$warnings.length} warning(s)"
exit($errors.empty? ? 0 : 1)
