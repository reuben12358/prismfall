#===============================================================================
# Prismfall Field Effects - DSL schema (pure data)
#-------------------------------------------------------------------------------
# This file must stay free of any Essentials dependency: tools/validate_fields.rb
# loads it outside the game to validate every field definition.
# The full DSL reference lives in design/FIELD_API.md.
#===============================================================================
module FieldEffects
  VERSION = "1.1.0"

  # The "no field" value of battle.field_effect.
  NONE = :NONE

  # Default field per map: FieldEffects::MAP_FIELDS[map_id] = :FIELD_ID
  # (LOCKED integration contract). Other plugins/files may add entries.
  MAP_FIELDS = {} unless const_defined?(:MAP_FIELDS, false)
  # A value of :NONE (or "none") marks a map as deliberately field-free (Poké Centers,
  # tutorial rooms); a missing entry falls back to the rules below.

  #-----------------------------------------------------------------------------
  # v1.1 "every battle has a field" fallbacks (see design/FIELD_DEFAULTS.yaml)
  #-----------------------------------------------------------------------------
  # Wild battles only: per-map field for wild encounters (overrides MAP_FIELDS).
  MAP_WILD_FIELDS = {} unless const_defined?(:MAP_WILD_FIELDS, false)
  # Interim per-map defaults generated from design/FIELD_DEFAULTS.yaml by
  # tools/field_defaults_to_rb.rb (011_FieldEffects_MapDefaults.rb). Consulted
  # only when MAP_FIELDS / MAP_WILD_FIELDS (written by mapgen) have no entry,
  # so mapgen's output always wins once it consumes the YAML itself.
  MAP_DEFAULT_FIELDS      = {} unless const_defined?(:MAP_DEFAULT_FIELDS, false)
  MAP_DEFAULT_WILD_FIELDS = {} unless const_defined?(:MAP_DEFAULT_WILD_FIELDS, false)
  # Trainer battles with a fixed field regardless of map (tutorial fights,
  # special indoor battles). Keys: trainer type, or [trainer type, version].
  # Value: field (:NONE = no field) or [field, stage]. First opponent decides.
  TRAINER_FIELDS = {} unless const_defined?(:TRAINER_FIELDS, false)
  # Per-map pools for open borrowing fields (:BLEED, :borrow pool :all): on that
  # map they borrow only from these field IDs (FIELD_DEFAULTS.yaml `borrow:`,
  # generated into 011). E.g. the Steamline's Bleed only echoes the war's fields.
  MAP_BORROW_POOLS = {} unless const_defined?(:MAP_BORROW_POOLS, false)
  # Wild battles only: by encounter type. Keys are GameData::EncounterType IDs
  # (:Land, :Cave, :Water, :OldRod...) or their :type (:land, :cave, :water,
  # :fishing, :contest). ID entries win over :type entries. Applied unless the
  # map's own field is listed in ENCOUNTER_KEEP_FIELDS for that key.
  ENCOUNTER_FIELDS = {
    :water   => :WATER_SURFACE,   # surfing
    :fishing => :WATER_SURFACE,   # rods
    :contest => :MEADOW           # Bug-Catching-style contests
  } unless const_defined?(:ENCOUNTER_FIELDS, false)
  # Fields that already ARE the right place for that encounter (no override).
  ENCOUNTER_KEEP_FIELDS = {
    :water   => [:WATER_SURFACE, :UNDERWATER, :CORROSIVE_MIRE, :BLEED, :PRISM_ARENA, :RAINBOW],
    :fishing => [:WATER_SURFACE, :UNDERWATER, :CORROSIVE_MIRE, :FROZEN_LAKE, :BEACH, :BLEED, :RAINBOW]
  } unless const_defined?(:ENCOUNTER_KEEP_FIELDS, false)
  # Wild battles on maps with no field of their own (no MAP_FIELDS /
  # MAP_DEFAULT_FIELDS entry, or :NONE): the encounter type supplies one.
  ENCOUNTER_FALLBACK_FIELDS = {
    :cave => :CAVE                # cave encounters -> Cave
  } unless const_defined?(:ENCOUNTER_FALLBACK_FIELDS, false)
  # Any battle while diving is underwater; while surfing, on the water.
  DIVING_FIELD  = :UNDERWATER
  SURFING_FIELD = :WATER_SURFACE
  # Last resort for maps with no MAP_FIELDS entry: the battle environment
  # (map metadata BattleEnvironment / terrain tag) decides. nil = no field.
  ENVIRONMENT_FIELDS = {
    :Grass => :MEADOW, :TallGrass => :MEADOW, :Forest => :SILKWOOD, :ForestGrass => :SILKWOOD,
    :MovingWater => :WATER_SURFACE, :StillWater => :WATER_SURFACE, :Puddle => :MEADOW,
    :Underwater => :UNDERWATER, :Cave => :CAVE, :Rock => :MOUNTAIN, :Sand => :BEACH,
    :Snow => :SNOWY_MOUNTAIN, :Ice => :FROZEN_LAKE, :Volcano => :VOLCANIC,
    :Graveyard => :HOLLOW_CATHEDRAL, :Sky => :STORMFRONT, :Space => :MINDSCAPE,
    :UltraSpace => :INVERSE
  } unless const_defined?(:ENVIRONMENT_FIELDS, false)

  # Every field ID named in design/SPINE.md (LOCKED). Used by the validator to
  # check transition targets that may not be implemented yet.
  ROSTER = [
    :SILKWOOD, :GRAND_STAGE, :WATER_SURFACE, :NEON_GRID, :DESERT, :CORROSIVE_MIRE,
    :VOLCANIC, :COLOSSEUM, :FLOWER_GARDEN, :FROZEN_LAKE, :STORMFRONT, :MINDSCAPE,
    :CRYSTAL_CAVERN, :HOLLOW_CATHEDRAL, :FACTORY, :NEW_MOON, :FAIRY_TALE, :DRAGONS_DEN,
    :CAVE, :MOUNTAIN, :SNOWY_MOUNTAIN, :BEACH, :UNDERWATER, :RAINBOW, :WASTELAND,
    :ASHEN_WASTE, :DARK_CRYSTAL, :SCRAPYARD, :INVERSE, :BLEED, :PRISM_ARENA
  ].freeze

  # Fields added after the SPINE roster (Revision 10). Valid transition targets
  # and listed after the roster in Field Notes.
  EXTRA_FIELDS = [:WILDFIRE, :MEADOW, :FLOODED_DUNES, :GLASS_DUNES].freeze
  KNOWN_FIELDS = (ROSTER + EXTRA_FIELDS).freeze

  SEED_ITEMS = [:ELEMENTALSEED, :MAGICALSEED, :TELLURICSEED, :SYNTHETICSEED].freeze
  # Field families (Reborn-style): each family reacts to "its" seed.
  FAMILIES     = [:elemental, :telluric, :synthetic, :magical].freeze
  FAMILY_SEEDS = { :elemental => :ELEMENTALSEED, :telluric => :TELLURICSEED,
                   :synthetic => :SYNTHETICSEED, :magical => :MAGICALSEED }.freeze

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
                     :flash_fire, :stockpile,
                     # v1.1: side effects on the battler's own side ...
                     :tailwind, :safeguard, :mist, :lucky_chant, :reflect, :light_screen,
                     # ... battler effects ...
                     :wish, :taunt,
                     # ... and hazards laid on the OPPOSING side
                     :stealth_rock, :spikes, :toxic_spikes, :sticky_web].freeze
  # Abilities :activate_abilities can switch on (they act as if their weather /
  # terrain / HP / status trigger were met). See FIELD_API.md 4.7.
  ACTIVATABLE_ABILITIES = [:BLAZE, :OVERGROW, :TORRENT, :SWARM,
                           :SWIFTSWIM, :CHLOROPHYLL, :SANDRUSH, :SLUSHRUSH, :SURGESURFER, :QUICKFEET,
                           :SANDVEIL, :SNOWCLOAK, :SANDFORCE, :SOLARPOWER, :FLOWERGIFT,
                           :TOXICBOOST, :FLAREBOOST, :GUTS, :MARVELSCALE, :GRASSPELT,
                           :RAINDISH, :ICEBODY, :DRYSKIN, :HYDRATION, :LEAFGUARD].freeze
  # Moves whose lingering effect :effect_durations can extend (see 4.10).
  DURATION_MOVES = [:TAILWIND, :REFLECT, :LIGHTSCREEN, :AURORAVEIL, :SAFEGUARD, :MIST, :LUCKYCHANT,
                    :TRICKROOM, :MAGICROOM, :WONDERROOM, :GRAVITY, :MUDSPORT, :WATERSPORT,
                    :MAGNETRISE, :TELEKINESIS, :TAUNT, :ENCORE, :HEALBLOCK, :EMBARGO,
                    :SUNNYDAY, :RAINDANCE, :SANDSTORM, :HAIL, :SNOWSCAPE,
                    :ELECTRICTERRAIN, :GRASSYTERRAIN, :MISTYTERRAIN, :PSYCHICTERRAIN].freeze
  BORROW_ORDERS = [:random, :sequential].freeze
  APPLY_TO      = [:target, :user].freeze

  #-----------------------------------------------------------------------------
  # Matchers
  #-----------------------------------------------------------------------------
  # Move matcher: every key present must match (AND). Array values match if ANY
  # element matches (OR).
  MOVE_MATCH_KEYS = [:moves, :not_moves, :types, :not_types, :flags, :category,
                     :function_codes, :user, :target, :condition,
                     :in_weather, :on_terrain].freeze
  # Battler matcher (used by user:/target:/battlers:).
  BATTLER_MATCH_KEYS = [:types, :not_types, :abilities, :not_abilities, :items,
                        :not_items, :grounded, :status, :condition,
                        :hp_below, :hp_above, :in_weather, :on_terrain].freeze
  # Things that happen to one battler (end_of_round, on_entry, seed).
  BATTLER_EFFECT_KEYS = [:battlers, :chance, :damage, :damage_type, :heal, :status,
                         :confuse, :cure_status, :stats, :effects, :message,
                         :animation, :proc, :add_type].freeze

  #-----------------------------------------------------------------------------
  # Rule lists: top-level key => allowed keys inside each rule Hash
  #-----------------------------------------------------------------------------
  RULE_KEYS = {
    :damage_mods        => MOVE_MATCH_KEYS + [:mult, :attack_mult, :defense_mult, :final_mult, :message],
    :effectiveness_mods => [:attack, :defend, :moves, :set, :mult, :user, :target],
    :type_changes       => MOVE_MATCH_KEYS + [:to, :message],
    :extra_types        => MOVE_MATCH_KEYS + [:add, :message],
    :accuracy_mods      => MOVE_MATCH_KEYS + [:mult, :evasion_mult, :set, :always_hit],
    :priority_mods      => MOVE_MATCH_KEYS + [:add],
    :crit_mods          => MOVE_MATCH_KEYS + [:add, :always],
    :added_effects      => MOVE_MATCH_KEYS + [:chance, :apply_to, :status, :confuse, :flinch,
                                              :stats, :message, :proc],
    :effect_chance_mods => MOVE_MATCH_KEYS + [:set, :mult],
    :fixed_damage_mods  => MOVE_MATCH_KEYS + [:set, :mult, :message],
    :weather_as         => MOVE_MATCH_KEYS + [:as],
    :move_stat_boosts   => MOVE_MATCH_KEYS + [:user_stats, :target_stats, :message],
    :move_fails         => MOVE_MATCH_KEYS + [:message],
    :end_of_round       => BATTLER_EFFECT_KEYS,
    :on_entry           => BATTLER_EFFECT_KEYS + [:also_on_change],
    :speed_mods         => [:battlers, :mult],
    :transitions        => MOVE_MATCH_KEYS + [:to, :stage, :stage_delta, :message, :uses,
                                              :progress_message, :weather, :terrain, :turns,
                                              :check, :even_if_failed, :strike_turn, :id, :rewind, :boost],
    :seed               => BATTLER_EFFECT_KEYS + [:item],
    :status_immunity    => [:battlers, :status, :message]
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
    :stages            => :stages,
    :family            => :family,            # v1.1 (:elemental/:telluric/:synthetic/:magical)
    :activate_abilities => :ability_list,     # v1.1
    :effect_durations  => :duration_hash      # v1.1 { MOVE => extra turns }
  }.merge(RULE_KEYS.keys.map { |k| [k, :rules] }.to_h).freeze

  REQUIRED_KEYS = [:name, :backdrop, :intro_message].freeze

  # Keys that a borrowing field (e.g. :BLEED) copies from the borrowed field.
  BORROWABLE_KEYS = [:type_mods, :move_mods, :type_messages, :move_messages, :damage_mods,
                     :effectiveness_mods, :inverse, :type_changes, :extra_types,
                     :accuracy_mods, :priority_mods, :crit_mods, :added_effects,
                     :effect_chance_mods, :fixed_damage_mods, :weather_as, :move_stat_boosts, :move_fails, :end_of_round,
                     :on_entry, :speed_mods, :negated_abilities, :weather, :terrain,
                     :hooks, :activate_abilities, :status_immunity, :effect_durations].freeze
  # Hooks a borrowing field copies (lifecycle hooks on_start/on_end are NOT copied).
  BORROWABLE_HOOKS = [:on_entry, :end_of_round, :base_type, :damage, :effectiveness,
                      :accuracy, :after_move, :block_move, :speed, :ai_score].freeze
  # Keys a stage override may NOT contain.
  STAGE_FORBIDDEN_KEYS = [:stages, :borrow].freeze
end
