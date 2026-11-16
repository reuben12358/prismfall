#===============================================================================
# Prismfall Debug Tools
# Adds a "Prismfall tools..." submenu to the Debug menu (F9 / Debug in pause
# menu while playtesting) so fields, Warden fights and level caps can be tested
# without building any maps.
#
# Works with or without the other Prismfall plugins: every integration point is
# guarded, and the SPINE gym table below is used as a fallback.
#===============================================================================
module PrismfallDebug
  # Fallback copy of the SPINE gym table: [type, warden name, trainer type, field, cap]
  GYMS_FALLBACK = [
    [:BUG,      "Tamsin",    :LEADER_TAMSIN,    :SILKWOOD,         15],
    [:NORMAL,   "Dorian",    :LEADER_DORIAN,    :GRAND_STAGE,      19],
    [:WATER,    "Marisol",   :LEADER_MARISOL,   :WATER_SURFACE,    23],
    [:ELECTRIC, "Rook",      :LEADER_ROOK,      :NEON_GRID,        27],
    [:GROUND,   "Sahar",     :LEADER_SAHAR,     :DESERT,           31],
    [:POISON,   "Corvin",    :LEADER_CORVIN,    :CORROSIVE_MIRE,   35],
    [:FIRE,     "Brann",     :LEADER_BRANN,     :VOLCANIC,         39],
    [:FIGHTING, "Kaito",     :LEADER_KAITO,     :COLOSSEUM,        43],
    [:GRASS,    "Juno",      :LEADER_JUNO,      :FLOWER_GARDEN,    47],
    [:ICE,      "Anja",      :LEADER_ANJA,      :FROZEN_LAKE,      51],
    [:FLYING,   "Odessa",    :LEADER_ODESSA,    :STORMFRONT,       55],
    [:PSYCHIC,  "Ilsa",      :LEADER_ILSA,      :MINDSCAPE,        59],
    [:ROCK,     "Bastian",   :LEADER_BASTIAN,   :CRYSTAL_CAVERN,   63],
    [:GHOST,    "Ysolde",    :LEADER_YSOLDE,    :HOLLOW_CATHEDRAL, 67],
    [:STEEL,    "Magnus",    :LEADER_MAGNUS,    :FACTORY,          71],
    [:DARK,     "Nyx",       :LEADER_NYX,       :NEW_MOON,         75],
    [:FAIRY,    "Celestine", :LEADER_CELESTINE, :FAIRY_TALE,       80],
    [:DRAGON,   "Sigrun",    :LEADER_SIGRUN,    :DRAGONS_DEN,      85]
  ].freeze

  FIELDS_FALLBACK = [
    :SILKWOOD, :GRAND_STAGE, :WATER_SURFACE, :NEON_GRID, :DESERT, :CORROSIVE_MIRE,
    :VOLCANIC, :COLOSSEUM, :FLOWER_GARDEN, :FROZEN_LAKE, :STORMFRONT, :MINDSCAPE,
    :CRYSTAL_CAVERN, :HOLLOW_CATHEDRAL, :FACTORY, :NEW_MOON, :FAIRY_TALE, :DRAGONS_DEN,
    :CAVE, :MOUNTAIN, :SNOWY_MOUNTAIN, :BEACH, :UNDERWATER, :RAINBOW, :WASTELAND,
    :ASHEN_WASTE, :DARK_CRYSTAL, :SCRAPYARD, :INVERSE, :BLEED, :PRISM_ARENA
  ].freeze

  BADGE_COUNT = 18

  module_function

  def field_engine?
    return defined?(FieldEffects) ? true : false
  end

  # Returns [[id, display name], ...] for every field the engine knows about.
  def field_list
    ids = nil
    if field_engine?
      [:all_ids, :ids, :field_ids, :keys].each do |m|
        next if !FieldEffects.respond_to?(m)
        ids = FieldEffects.send(m) rescue nil
        break if ids.is_a?(Array) && !ids.empty?
      end
    end
    ids = FIELDS_FALLBACK if !ids.is_a?(Array) || ids.empty?
    return ids.map { |id| [id, field_name(id)] }
  end

  def field_name(id)
    if field_engine?
      [:get, :data, :field].each do |m|
        next if !FieldEffects.respond_to?(m)
        data = FieldEffects.send(m, id) rescue nil
        next if !data
        name = (data.is_a?(Hash)) ? data[:name] : (data.respond_to?(:name) ? data.name : nil)
        return name if name.is_a?(String) && !name.empty?
      end
    end
    return id.to_s.split("_").map(&:capitalize).join(" ")
  end

  # Ask the player to pick a field. Returns a Symbol, :NONE, or nil if cancelled.
  def choose_field(allow_none = true)
    list = field_list
    cmds = list.map { |entry| entry[1] }
    cmds.unshift(_INTL("[No field]")) if allow_none
    idx = pbMessage(_INTL("Choose a field."), cmds, -1)
    return nil if idx < 0
    return :NONE if allow_none && idx == 0
    return list[allow_none ? idx - 1 : idx][0]
  end

  def apply_field_rule(field)
    return if field.nil? || field == :NONE
    if !field_engine?
      pbMessage(_INTL("Field Effects plugin not installed; battle will have no field."))
      return
    end
    setBattleRule("field", field)
  end

  # [[index (1-based), type, name, trainer_type, field, cap], ...]
  def gyms
    if defined?(Prismfall) && defined?(Prismfall::GYMS)
      ret = []
      Prismfall::GYMS.each_with_index do |g, i|
        if g.is_a?(Hash)
          ret.push([g[:index] || (i + 1), g[:type],
                    (g[:trainer_name] || (g[:warden] || "?").to_s.split(" ")[0]),
                    g[:trainer_type], g[:field], g[:cap] || g[:level_cap]])
        end
      end
      return ret if ret.length == BADGE_COUNT && ret.all? { |g| g[3] }
    end
    return GYMS_FALLBACK.each_with_index.map { |g, i| [i + 1] + g }
  end

  def ensure_badge_array
    return if !$player
    $player.badges[BADGE_COUNT - 1] = false if $player.badges.length < BADGE_COUNT
    $player.badges.map! { |b| b == true }
  end

  def set_badges(count)
    ensure_badge_array
    BADGE_COUNT.times { |i| $player.badges[i] = (i < count) }
  end

  def set_party_level(level)
    $player.party.each do |pkmn|
      next if pkmn.egg?
      pkmn.level = level
      pkmn.calc_stats
      pkmn.heal
    end
  end

  def trainer_exists?(tr_type, name, version)
    return GameData::TrainerType.exists?(tr_type) &&
           GameData::Trainer.exists?(tr_type, name, version)
  end
end

#-------------------------------------------------------------------------------
# Menu entries
#-------------------------------------------------------------------------------
MenuHandlers.add(:debug_menu, :prismfall_menu, {
  "name"        => _INTL("Prismfall tools..."),
  "parent"      => :main,
  "description" => _INTL("Test fields, Warden battles, badges and level caps."),
  "always_show" => true
})

MenuHandlers.add(:debug_menu, :prismfall_field_wild, {
  "name"        => _INTL("Field test: wild battle"),
  "parent"      => :prismfall_menu,
  "description" => _INTL("Pick a field, then a wild species and level."),
  "effect"      => proc {
    field = PrismfallDebug.choose_field
    next false if field.nil?
    species = pbChooseSpeciesList
    next false if !species
    params = ChooseNumberParams.new
    params.setRange(1, GameData::GrowthRate.max_level)
    params.setInitialValue(50)
    params.setCancelValue(0)
    level = pbMessageChooseNumber(_INTL("Set the wild Pokémon's level."), params)
    next false if level <= 0
    $game_temp.encounter_type = nil
    setBattleRule("canLose")
    PrismfallDebug.apply_field_rule(field)
    WildBattle.start(species, level)
    next false
  }
})

MenuHandlers.add(:debug_menu, :prismfall_field_trainer, {
  "name"        => _INTL("Field test: trainer battle"),
  "parent"      => :prismfall_menu,
  "description" => _INTL("Pick a field, then any trainer from trainers.txt."),
  "effect"      => proc {
    field = PrismfallDebug.choose_field
    next false if field.nil?
    trainerdata = pbListScreen(_INTL("SINGLE TRAINER"), TrainerBattleLister.new(0, false))
    next false if !trainerdata
    setBattleRule("canLose")
    PrismfallDebug.apply_field_rule(field)
    TrainerBattle.start(trainerdata[0], trainerdata[1], trainerdata[2])
    next false
  }
})

MenuHandlers.add(:debug_menu, :prismfall_warden, {
  "name"        => _INTL("Warden battle (1-18)"),
  "parent"      => :prismfall_menu,
  "description" => _INTL("Fight any Warden on their signature field. Difficulty variant follows the current mode."),
  "effect"      => proc {
    gyms = PrismfallDebug.gyms
    cmds = gyms.map do |g|
      _INTL("{1}. {2} ({3}) Lv{4}", g[0], g[2], GameData::Type.try_get(g[1])&.name || g[1].to_s, g[5])
    end
    idx = pbMessage(_INTL("Which Warden?"), cmds, -1)
    next false if idx < 0
    g = gyms[idx]
    tr_type, name, field = g[3], g[2], g[4]
    # Prefer Core's gym_battle: it applies the field, difficulty variant and rival versions.
    if defined?(Prismfall) && Prismfall.respond_to?(:gym_battle)
      if pbConfirmMessage(_INTL("Set party to the Lv{1} cap and heal first?", g[5]))
        PrismfallDebug.set_party_level(g[5])
      end
      Prismfall.gym_battle(g[0], can_lose: true)
      next false
    end
    if !PrismfallDebug.trainer_exists?(tr_type, name, 0)
      pbMessage(_INTL("No trainer {1} \"{2}\" (version 0) in trainers.txt. Compile PBS first?", tr_type.to_s, name))
      next false
    end
    if pbConfirmMessage(_INTL("Set party to the Lv{1} cap and heal first?", g[5]))
      PrismfallDebug.set_party_level(g[5])
    end
    setBattleRule("canLose")
    PrismfallDebug.apply_field_rule(field)
    TrainerBattle.start(tr_type, name, 0)
    next false
  }
})

MenuHandlers.add(:debug_menu, :prismfall_badges, {
  "name"        => _INTL("Set badge count (0-18)"),
  "parent"      => :prismfall_menu,
  "description" => _INTL("Owns the first N of the 18 badges. Level cap follows."),
  "effect"      => proc {
    params = ChooseNumberParams.new
    params.setRange(0, PrismfallDebug::BADGE_COUNT)
    params.setInitialValue($player.badge_count)
    params.setCancelValue(-1)
    count = pbMessageChooseNumber(_INTL("How many badges?"), params)
    next false if count < 0
    PrismfallDebug.set_badges(count)
    pbMessage(_INTL("Now holding {1} badge(s).", $player.badge_count))
    next false
  }
})

MenuHandlers.add(:debug_menu, :prismfall_party_level, {
  "name"        => _INTL("Set whole party level"),
  "parent"      => :prismfall_menu,
  "description" => _INTL("Sets every party Pokémon to one level and heals them."),
  "effect"      => proc {
    params = ChooseNumberParams.new
    params.setRange(1, GameData::GrowthRate.max_level)
    params.setInitialValue(50)
    params.setCancelValue(0)
    level = pbMessageChooseNumber(_INTL("Set party level."), params)
    next false if level <= 0
    PrismfallDebug.set_party_level(level)
    pbMessage(_INTL("Party set to Lv{1}.", level))
    next false
  }
})

MenuHandlers.add(:debug_menu, :prismfall_heal, {
  "name"        => _INTL("Heal party"),
  "parent"      => :prismfall_menu,
  "description" => _INTL("Fully heal the party."),
  "effect"      => proc {
    $player.heal_party
    pbMessage(_INTL("Party healed."))
    next false
  }
})
