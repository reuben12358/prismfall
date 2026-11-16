#===============================================================================
# Prismfall Cutscenes - 014 Debug menu ("Prismfall Cutscenes..." in Debug)
#===============================================================================
if defined?(MenuHandlers)
  MenuHandlers.add(:debug_menu, :prismfall_cutscenes_menu, {
    "name"        => _INTL("Prismfall Cutscenes..."),
    "parent"      => :main,
    "description" => _INTL("Play pixel cutscenes, Festival highlights and portrait bubbles."),
    "always_show" => true
  })

  MenuHandlers.add(:debug_menu, :prismfall_cutscenes_war, {
    "name"        => _INTL("War climax (pick outcome)"),
    "parent"      => :prismfall_cutscenes_menu,
    "description" => _INTL("The Beam Clash on the Shattered Ice, any of the four outcomes."),
    "effect"      => proc {
      variants = [:A, :A2, :B, :C]
      cmd = pbMessage(_INTL("Which outcome?"),
                      [_INTL("A: war stopped"), _INTL("A': both broken"), _INTL("B: Ashkaar won"),
                       _INTL("C: Isenmar won"), _INTL("From this save's flags"), _INTL("Cancel")], 6)
      next if !cmd || cmd < 0 || cmd > 4
      legends = pbConfirmMessage(_INTL("Show the legendaries? (No = the Wardens' aces)"))
      if cmd == 4 then Prismfall::Cutscene.play(:WAR_CLIMAX)
      else Prismfall::Cutscene.play(:WAR_CLIMAX, variant: variants[cmd], legends: legends)
      end
    }
  })

  MenuHandlers.add(:debug_menu, :prismfall_cutscenes_war_demo, {
    "name"        => _INTL("War climax demo"),
    "parent"      => :prismfall_cutscenes_menu,
    "description" => _INTL(":WAR_CLIMAX_DEMO - fixed outcome (both lines broken), ignores the save."),
    "effect"      => proc { Prismfall::Cutscene.play(:WAR_CLIMAX_DEMO) }
  })

  MenuHandlers.add(:debug_menu, :prismfall_cutscenes_highlight, {
    "name"        => _INTL("Sample match highlight"),
    "parent"      => :prismfall_cutscenes_menu,
    "description" => _INTL("Anja vs Brann, the Truce Match (Festival highlight)."),
    "effect"      => proc { Prismfall::Cutscene.play_sample_highlight }
  })

  MenuHandlers.add(:debug_menu, :prismfall_cutscenes_highlight_auto, {
    "name"        => _INTL("Auto highlight (templates)"),
    "parent"      => :prismfall_cutscenes_menu,
    "description" => _INTL("Kestrel vs Juno built from trainers PBS with template moments."),
    "effect"      => proc {
      Prismfall::Cutscene.match_highlight({ :id => :KESTREL, :name => "Kestrel", :trainer_type => :RIVAL_KESTREL },
                                          { :id => :JUNO, :name => "Juno", :trainer_type => :RIVAL_JUNO }, winner: :a)
    }
  })

  MenuHandlers.add(:debug_menu, :prismfall_cutscenes_any, {
    "name"        => _INTL("Play any scene"),
    "parent"      => :prismfall_cutscenes_menu,
    "description" => _INTL("Lists every scene registered with Prismfall::Cutscene.define."),
    "effect"      => proc {
      ids = Prismfall::Cutscene.ids
      cmd = pbMessage(_INTL("Play which scene?"), ids.map(&:to_s) + [_INTL("Cancel")], ids.length + 1)
      Prismfall::Cutscene.play(ids[cmd]) if cmd && cmd >= 0 && cmd < ids.length
    }
  })

  MenuHandlers.add(:debug_menu, :prismfall_cutscenes_portraits, {
    "name"        => _INTL("Portrait bubbles"),
    "parent"      => :prismfall_cutscenes_menu,
    "description" => _INTL("Shows every expression as a portrait speech bubble on the player."),
    "effect"      => proc {
      Prismfall::Portrait::EXPRESSIONS.each_key do |expr|
        pf_say(:PLAYER, expr, _INTL("This is the {1} expression.", expr.to_s), name: _INTL("Tester"))
      end
    }
  })
end
