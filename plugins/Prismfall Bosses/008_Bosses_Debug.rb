#===============================================================================
# Prismfall Bosses - 008 Debug menu: Debug > Prismfall Bosses...
#===============================================================================
if Prismfall::Bosses::DEBUG_MENU
  MenuHandlers.add(:debug_menu, :prismfall_bosses_menu, {
    "name"        => _INTL("Prismfall Bosses..."),
    "parent"      => :main,
    "description" => _INTL("Start the example multi-bar boss battles."),
    "always_show" => true
  })

  MenuHandlers.add(:debug_menu, :prismfall_bosses_wild, {
    "name"        => _INTL("Start a boss battle"),
    "parent"      => :prismfall_bosses_menu,
    "description" => _INTL("Any registered wild boss (Kyogre, Zekrom, Arceus...)."),
    "effect"      => proc {
      ids = Prismfall::Bosses.ids.select { |id| Prismfall::Bosses.get(id)[:species] }
      next pbMessage(_INTL("No wild bosses are registered.")) if ids.empty?
      names = ids.map do |id|
        d = Prismfall::Bosses.get(id)
        _INTL("{1} ({2}, {3} bars)", id.to_s, GameData::Species.get(d[:species]).name, Prismfall::Bosses.bars_for(d))
      end
      cmd = pbMessage(_INTL("Start which boss?"), names, -1)
      next if cmd < 0
      setBattleRule("canLose")
      won = Prismfall::Bosses.wild_battle(ids[cmd])
      r = Prismfall::Bosses.last_result || {}
      pbMessage(_INTL("Result: {1}. Bars broken: {2}. Script result: {3}.",
                      won ? "win" : "loss", r[:breaks] || 0, (r[:result] || "-").to_s))
    }
  })

  MenuHandlers.add(:debug_menu, :prismfall_bosses_finale, {
    "name"        => _INTL("Arceus True Finale (Prism Arena)"),
    "parent"      => :prismfall_bosses_menu,
    "description" => _INTL("The Festival finale boss outside the Festival (Lv 100, canLose)."),
    "effect"      => proc {
      setBattleRule("canLose")
      Prismfall::Bosses.wild_battle(:ARCEUS_FINALE)
    }
  })

  MenuHandlers.add(:debug_menu, :prismfall_bosses_warden, {
    "name"        => _INTL("Hard-mode Warden ace (2 bars)"),
    "parent"      => :prismfall_bosses_menu,
    "description" => _INTL("Ilsa or Celestine's Hard team with a 2-bar ace (any difficulty)."),
    "effect"      => proc {
      cmd = pbMessage(_INTL("Which Warden?"), [_INTL("Ilsa (Gym 12)"), _INTL("Celestine (Gym 17)")], -1)
      next if cmd < 0
      tr = [[:LEADER_ILSA, "Ilsa"], [:LEADER_CELESTINE, "Celestine"]][cmd]
      setBattleRule("canLose")
      Prismfall::Bosses.trainer_battle(tr[0], tr[1], 100, boss: :WARDEN_ACE_2BAR)
    }
  })

  MenuHandlers.add(:debug_menu, :prismfall_bosses_festival, {
    "name"        => _INTL("Toggle Festival boss switch"),
    "parent"      => :prismfall_bosses_menu,
    "description" => _INTL("Whether Core's Festival Arceus stage uses this plugin's boss."),
    "effect"      => proc {
      Prismfall::Bosses.festival_enabled = !Prismfall::Bosses.festival_enabled?
      pbMessage(_INTL("Festival uses Prismfall Bosses: {1}.", Prismfall::Bosses.festival_enabled? ? "ON" : "OFF"))
    }
  })
end
