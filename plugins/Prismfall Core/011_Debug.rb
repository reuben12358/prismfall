#===============================================================================
# Prismfall Core - 011 Debug menu ("Prismfall Core..." in the Debug menu)
#-------------------------------------------------------------------------------
# Complements the separate "Prismfall Debug Tools" plugin (fields, Warden
# battles, badge count); this menu covers Core-only state.
#===============================================================================
MenuHandlers.add(:debug_menu, :prismfall_core_menu, {
  "name"        => _INTL("Prismfall Core..."),
  "parent"      => :main,
  "description" => _INTL("Difficulty, level cap, rival starter and Festival state."),
  "always_show" => true
})

MenuHandlers.add(:debug_menu, :prismfall_core_status, {
  "name"        => _INTL("Show Core status"),
  "parent"      => :prismfall_core_menu,
  "description" => _INTL("Difficulty, cap, starter, Festival stage."),
  "effect"      => proc {
    info = Prismfall::Rival.starter_info
    pbMessage(_INTL("Mode: {1}. Badges: {2}/{3}. Level cap: Lv. {4}.",
                    Prismfall::Difficulty.label, Prismfall.badge_count, Prismfall::BADGE_COUNT,
                    Prismfall::LevelCap.current))
    pbMessage(_INTL("Starter: {1} (Gen {2}, slot {3}{4}).", (info[:species] || "none").to_s, info[:gen],
                    info[:slot], (info[:inferred]) ? ", inferred" : ""))
    if Prismfall::Festival.started?
      pbMessage(_INTL("Festival stage: {1}. Losses: {2}.", (Prismfall::Festival.stage_id || "finished").to_s,
                      Prismfall::Festival.state[:losses]))
    end
    errors = Prismfall::Festival.validate + Prismfall::Rival.missing_species.map { |s| "Missing species #{s}" }
    pbMessage(_INTL("Data check: {1}", (errors.empty?) ? "OK" : errors.join("; ")))
  }
})

MenuHandlers.add(:debug_menu, :prismfall_core_difficulty, {
  "name"        => _INTL("Set difficulty"),
  "parent"      => :prismfall_core_menu,
  "description" => _INTL("Switch Casual / Standard / Hard (ignores the change rule)."),
  "effect"      => proc { Prismfall::Difficulty.choose(cancelable: true) }
})

MenuHandlers.add(:debug_menu, :prismfall_core_starter, {
  "name"        => _INTL("Set player's starter"),
  "parent"      => :prismfall_core_menu,
  "description" => _INTL("Record which starter the player chose (drives rival versions and swaps)."),
  "effect"      => proc {
    species = pbChooseSpeciesList
    next if !species
    if !Prismfall::Rival.lookup(species)
      pbMessage(_INTL("{1} isn't in STARTER_LINES; recorded as Gen 1 slot 0.", GameData::Species.get(species).name))
    end
    info = Prismfall.record_starter(species)
    pbMessage(_INTL("Starter: Gen {1}, slot {2}.", info[:gen], info[:slot]))
  }
})

MenuHandlers.add(:debug_menu, :prismfall_core_cap, {
  "name"        => _INTL("Level cap override"),
  "parent"      => :prismfall_core_menu,
  "description" => _INTL("Force a cap (0 = clear override). Also toggles the Festival finale cap."),
  "effect"      => proc {
    cmd = pbMessage(_INTL("Level cap options."), [_INTL("Set override"), _INTL("Clear override"),
                    _INTL("Toggle finale cap (100)"), _INTL("Toggle caps on/off"), _INTL("Cancel")], 5)
    case cmd
    when 0
      params = ChooseNumberParams.new
      params.setRange(1, GameData::GrowthRate.max_level)
      params.setInitialValue(Prismfall::LevelCap.current)
      params.setCancelValue(0)
      lv = pbMessageChooseNumber(_INTL("Set the level cap."), params)
      Prismfall::LevelCap.set_override(lv) if lv > 0
    when 1 then Prismfall::LevelCap.clear_override
    when 2
      if Prismfall::LevelCap.finale_unlocked?
        Prismfall::LevelCap.lock_finale!
      else
        Prismfall::LevelCap.unlock_finale!
      end
    when 3
      if Prismfall::LevelCap.enabled?
        Prismfall::LevelCap.disable!
      else
        Prismfall::LevelCap.enable!
      end
    end
    pbMessage(Prismfall::LevelCap.info_text) if cmd >= 0 && cmd < 4
  }
})

MenuHandlers.add(:debug_menu, :prismfall_core_festival, {
  "name"        => _INTL("Festival tools"),
  "parent"      => :prismfall_core_menu,
  "description" => _INTL("Start/reset the Festival, skip to a stage, view the bracket, play the next match."),
  "effect"      => proc {
    fe = Prismfall::Festival
    cmds = [_INTL("Start (force)"), _INTL("Reset"), _INTL("Skip to stage..."), _INTL("Show bracket"),
            _INTL("Play next match"), _INTL("Exhibition menu"), _INTL("Cancel")]
    case pbMessage(_INTL("Festival tools."), cmds, cmds.length)
    when 0 then fe.start(force: true)
    when 1 then fe.reset!
    when 2
      ids = fe::STAGES.map { |s| s[:id].to_s }
      idx = pbMessage(_INTL("Skip to which stage?"), ids, -1)
      fe.debug_skip_to(fe::STAGES[idx][:id]) if idx >= 0
    when 3 then fe.show_bracket
    when 4
      fe.start(force: true) if !fe.active?
      fe.next_match
    when 5 then fe.exhibition_menu
    end
  }
})
