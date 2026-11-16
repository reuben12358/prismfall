#===============================================================================
# Prismfall Field Effects - DSL schema (pure data)
#-------------------------------------------------------------------------------
# This file must stay free of any Essentials dependency: tools/validate_fields.rb
# loads it outside the game to validate every field definition.
# The full DSL reference lives in design/FIELD_API.md.
#===============================================================================
module FieldEffects
  VERSION = "1.0.0"

  # The "no field" value of battle.field_effect.
  NONE = :NONE

  # Default field per map: FieldEffects::MAP_FIELDS[map_id] = :FIELD_ID
  # (LOCKED integration contract). Other plugins/files may add entries.
  MAP_FIELDS = {} unless const_defined?(:MAP_FIELDS, false)

  # Every field ID named in design/SPINE.md (LOCKED). Used by the validator to
  # check transition targets that may not be implemented yet.
  ROSTER = [
    :SILKWOOD, :GRAND_STAGE, :WATER_SURFACE, :NEON_GRID, :DESERT, :CORROSIVE_MIRE,
    :VOLCANIC, :COLOSSEUM, :FLOWER_GARDEN, :FROZEN_LAKE, :STORMFRONT, :MINDSCAPE,
    :CRYSTAL_CAVERN, :HOLLOW_CATHEDRAL, :FACTORY, :NEW_MOON, :FAIRY_TALE, :DRAGONS_DEN,
    :CAVE, :MOUNTAIN, :SNOWY_MOUNTAIN, :BEACH, :UNDERWATER, :RAINBOW, :WASTELAND,
    :ASHEN_WASTE, :DARK_CRYSTAL, :SCRAPYARD, :INVERSE, :BLEED, :PRISM_ARENA
  ].freeze

  SEED_ITEMS = [:ELEMENTALSEED, :MAGICALSEED, :TELLURICSEED, :SYNTHETICSEED].freeze

  #-----------------------------------------------------------------------------
  # Enumerations
  #-----------------------------------------------------------------------------
  STATS      = [:ATTACK, :DEFENSE, :SPECIAL_ATTACK, :SPECIAL_DEFENSE, :SPEED, :ACCURACY, :EVASION].freeze
  # :TOXIC is a pseudo-status meaning "badly poisoned".
  STATUSES   = [:NONE, :SLEEP, :POISON, :TOXIC, :BURN, :PARALYSIS, :FROZEN].freeze
  WEATHERS   = [:None, :Sun, :Rain, :Sandstorm, :Hail, :HarshSun, :HeavyRain, :StrongWinds, :ShadowSky].freeze
  TERRAINS   = [:None, :Electric, :Grassy, :Misty, :Psychic].freeze
  CATEGORIES = [:physical, :special, :status, :damaging].freeze
  # Move flags in the base project's PBS/moves.txt (Essentials 21.1 + Gen 9 Pack).
  # Matching is case-insensitive.
  MOVE_FLAGS = ["Contact", "CanProtect", "CanMirrorMove", "ThawsUser", "HighCriticalHitRate",
                "Biting", "Punching", "Sound", "Powder", "Pulse", "Bomb", "Dance",
                "CannotMetronome", "TramplesMinimize", "Slicing", "Wind"].freeze
  # Named battler effects usable in `effects:` (on-entry, end-of-round, seeds).
  BATTLER_EFFECTS = [:ingrain, :aqua_ring, :magnet_rise, :focus_energy, :laser_focus,
                     :charge, :defense_curl, :minimize, :smack_down, :telekinesis,
                     :flash_fire, :stockpile].freeze
  BORROW_ORDERS = [:random, :sequential].freeze
  APPLY_TO      = [:target, :user].freeze

  #-----------------------------------------------------------------------------
  # Matchers
  #-----------------------------------------------------------------------------
  # Move matcher: every key present must match (AND). Array values match if ANY
  # element matches (OR).
  MOVE_MATCH_KEYS = [:moves, :not_moves, :types, :not_types, :flags, :category,
                     :function_codes, :user, :target, :condition].freeze
  # Battler matcher (used by user:/target:/battlers:).
  BATTLER_MATCH_KEYS = [:types, :not_types, :abilities, :not_abilities, :items,
                        :not_items, :grounded, :status, :condition].freeze
  # Things that happen to one battler (end_of_round, on_entry, seed).
  BATTLER_EFFECT_KEYS = [:battlers, :chance, :damage, :damage_type, :heal, :status,
                         :confuse, :cure_status, :stats, :effects, :message,
                         :animation, :proc].freeze

  #-----------------------------------------------------------------------------
  # Rule lists: top-level key => allowed keys inside each rule Hash
  #-----------------------------------------------------------------------------
  RULE_KEYS = {
    :damage_mods        => MOVE_MATCH_KEYS + [:mult, :attack_mult, :defense_mult, :final_mult, :message],
    :effectiveness_mods => [:attack, :defend, :moves, :set, :mult],
    :type_changes       => MOVE_MATCH_KEYS + [:to, :message],
    :extra_types        => MOVE_MATCH_KEYS + [:add, :message],
    :accuracy_mods      => MOVE_MATCH_KEYS + [:mult, :evasion_mult, :set, :always_hit],
    :priority_mods      => MOVE_MATCH_KEYS + [:add],
    :crit_mods          => MOVE_MATCH_KEYS + [:add, :always],
    :added_effects      => MOVE_MATCH_KEYS + [:chance, :apply_to, :status, :confuse, :flinch,
                                              :stats, :message, :proc],
    :effect_chance_mods => MOVE_MATCH_KEYS + [:set, :mult],
    :move_stat_boosts   => MOVE_MATCH_KEYS + [:user_stats, :target_stats, :message],
    :move_fails         => MOVE_MATCH_KEYS + [:message],
    :end_of_round       => BATTLER_EFFECT_KEYS,
    :on_entry           => BATTLER_EFFECT_KEYS + [:also_on_change],
    :speed_mods         => [:battlers, :mult],
    :transitions        => MOVE_MATCH_KEYS + [:to, :stage, :stage_delta, :message, :uses,
                                              :progress_message, :weather, :terrain, :turns,
                                              :check, :even_if_failed],
    :seed               => BATTLER_EFFECT_KEYS + [:item]
  }.freeze

  WEATHER_SPEC_KEYS = [:block, :block_message, :transform, :extend].freeze
  BORROW_KEYS       = [:pool, :exclude, :interval, :count, :order, :message, :start_immediately].freeze
  HOOK_KEYS         = [:on_start, :on_end, :on_entry, :end_of_round, :base_type, :damage,
                       :effectiveness, :accuracy, :after_move, :block_move, :speed,
                       :ai_score].freeze

  # Top-level keys => value kind (interpreted by the validator).
  TOP_LEVEL_KEYS = {
    :name              => :string,      # required
    :backdrop          => :string,      # required
    :intro_message     => :string,      # required
    :description       => :string,
    :notes             => :string_list, # Field Notes lines (else auto-generated)
    :nature_power      => :move,
    :camouflage        => :type,
    :secret_power      => :integer,
    :type_mods         => :type_number_hash,
    :move_mods         => :move_number_hash,
    :type_messages     => :type_string_hash,
    :move_messages     => :move_string_hash,
    :inverse           => :boolean,
    :negated_abilities => :ability_list,
    :weather           => :weather_spec,
    :terrain           => :terrain_spec,
    :borrow            => :borrow_spec,
    :hooks             => :hooks,
    :stages            => :stages
  }.merge(RULE_KEYS.keys.map { |k| [k, :rules] }.to_h).freeze

  REQUIRED_KEYS = [:name, :backdrop, :intro_message].freeze

  # Keys that a borrowing field (e.g. :BLEED) copies from the borrowed field.
  BORROWABLE_KEYS = [:type_mods, :move_mods, :type_messages, :move_messages, :damage_mods,
                     :effectiveness_mods, :inverse, :type_changes, :extra_types,
                     :accuracy_mods, :priority_mods, :crit_mods, :added_effects,
                     :effect_chance_mods, :move_stat_boosts, :move_fails, :end_of_round,
                     :on_entry, :speed_mods, :negated_abilities, :weather, :terrain,
                     :hooks].freeze
  # Hooks a borrowing field copies (lifecycle hooks on_start/on_end are NOT copied).
  BORROWABLE_HOOKS = [:on_entry, :end_of_round, :base_type, :damage, :effectiveness,
                      :accuracy, :after_move, :block_move, :speed, :ai_score].freeze
  # Keys a stage override may NOT contain.
  STAGE_FORBIDDEN_KEYS = [:stages, :borrow].freeze
end
