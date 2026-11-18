#===============================================================================
# Prismfall Puzzles - 006 password mirror and Debug menu
#-------------------------------------------------------------------------------
# Core's `puzzleskip` password (020_Passwords.rb, :PUZZLE_SKIP) writes Game Switch 301.
# The mirror below re-applies it on every map entry, so saves made before the
# switch had a System.rxdata name still get it.
#===============================================================================
EventHandlers.add(:on_enter_map, :prismfall_puzzles_skip_mirror,
  proc { |_old_map_id|
    next if !$game_switches || !defined?(Prismfall::Passwords)
    on = Prismfall::Passwords.active?(:PUZZLE_SKIP)
    $game_switches[PrismfallPuzzles::SKIP_SWITCH] = true if on && !$game_switches[PrismfallPuzzles::SKIP_SWITCH]
  }
)

MenuHandlers.add(:debug_menu, :prismfall_puzzles, {
  "name"        => _INTL("Prismfall puzzles..."),
  "parent"      => :main,
  "description" => _INTL("Reset or solve the puzzle room on this map; toggle the puzzle-skip switch."),
  "effect"      => proc {
    here = PrismfallPuzzles::ROOMS.select { |_id, r| r[:map] == $game_map.map_id }.keys
    cmds = here.flat_map { |id| ["Reset #{id}", "Solve #{id}", "Log #{id}"] }
    cmds += ["Toggle puzzle skip (S301)", "Cancel"]
    c = pbMessage(_INTL("Puzzle rooms registered: {1}. Here: {2}.", PrismfallPuzzles::ROOMS.length, here.length), cmds, cmds.length)
    label = cmds[c].to_s
    id = label.split(" ", 2)[1]&.to_sym
    if label.start_with?("Reset ")
      PrismfallPuzzles.reset(id)
    elsif label.start_with?("Solve ")
      PrismfallPuzzles.solve(id)
    elsif label.start_with?("Log ")
      pbMessage(PrismfallPuzzles.room_log(id).inspect)
    elsif label.start_with?("Toggle")
      $game_switches[PrismfallPuzzles::SKIP_SWITCH] = !$game_switches[PrismfallPuzzles::SKIP_SWITCH]
      pbMessage(_INTL("Puzzle skip is now {1}.", $game_switches[PrismfallPuzzles::SKIP_SWITCH] ? "ON" : "OFF"))
    end
  }
})
