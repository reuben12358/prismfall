#===============================================================================
# Prismfall Trials - 011 Debug menu (Debug > Prismfall Trials...)
#===============================================================================
MenuHandlers.add(:debug_menu, :prismfall_trials_menu, {
  "name"        => _INTL("Prismfall Trials..."),
  "parent"      => :main,
  "description" => _INTL("Quests, Trial ranks, event Pokemon and badge tiers."),
  "always_show" => true
})

MenuHandlers.add(:debug_menu, :prismfall_trials_status, {
  "name"        => _INTL("Trials status"),
  "parent"      => :prismfall_trials_menu,
  "description" => _INTL("Show ranks, active quests and the badge tier of this map."),
  "effect"      => proc {
    tr = Prismfall::Trials
    lines = tr::TRIALS.keys.map { |t| "#{tr.trial_name(t)}: #{tr.rank_name(t)} (#{tr.points(t)})" }
    lines.push("Active: #{tr.active_ids.join(', ')}") if !tr.active_ids.empty?
    if $game_map
      m = $game_map.map_id
      lines.push("Map #{m}: tiers #{tr::BadgeTiers.tiers_for(m).inspect}, unlocked #{tr::BadgeTiers.unlocked_tier(m)}")
    end
    lines.each_slice(3) { |sl| pbMessage(sl.join("\n")) }
  }
})

MenuHandlers.add(:debug_menu, :prismfall_trials_quest, {
  "name"        => _INTL("Set quest state..."),
  "parent"      => :prismfall_trials_menu,
  "description" => _INTL("Start, step, complete or reset any registered quest."),
  "effect"      => proc {
    tr = Prismfall::Trials
    ids = tr.quest_ids
    cmd = pbMessage(_INTL("Which quest?"), ids.map { |id| "#{id} [#{tr.state(id)}]" }, -1)
    next if cmd < 0
    id = ids[cmd]
    opts = [_INTL("Start"), _INTL("Next step"), _INTL("Complete"), _INTL("Reset")]
    case pbMessage(_INTL("{1}: {2}", id, tr.state(id)), opts, -1)
    when 0 then tr.start(id)
    when 1
      steps = tr.step_ids(id)
      i = steps.index(tr.step(id)) || -1
      tr.set_step(id, steps[[i + 1, steps.length - 1].min]) if !steps.empty?
    when 2 then tr.complete(id)
    when 3 then tr.reset(id)
    end
  }
})

MenuHandlers.add(:debug_menu, :prismfall_trials_points, {
  "name"        => _INTL("Add Trial points..."),
  "parent"      => :prismfall_trials_menu,
  "description" => _INTL("Give 5 points to a Trial."),
  "effect"      => proc {
    keys = Prismfall::Trials::TRIALS.keys
    cmd = pbMessage(_INTL("Which Trial?"), keys.map { |k| Prismfall::Trials.trial_name(k) }, -1)
    Prismfall::Trials.add_points(keys[cmd], 5) if cmd >= 0
  }
})

MenuHandlers.add(:debug_menu, :prismfall_trials_mon, {
  "name"        => _INTL("Give event Pokemon..."),
  "parent"      => :prismfall_trials_menu,
  "description" => _INTL("Add any registered event Pokemon to the party."),
  "effect"      => proc {
    ids = Prismfall::EventMons.ids
    cmd = pbMessage(_INTL("Which?"), ids.map(&:to_s), -1)
    Prismfall::EventMons.gift(ids[cmd]) if cmd >= 0
  }
})
