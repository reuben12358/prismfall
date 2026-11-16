#===============================================================================
# Prismfall Core - 021 Debug: narrative, Ledger, endings, passwords
#-------------------------------------------------------------------------------
# Debug menu > Prismfall Core... > Narrative / Ledger tools
#===============================================================================
module Prismfall
  module DebugNarrative
    module_function

    def pick_number(text, min, max, initial)
      params = ChooseNumberParams.new
      params.setRange(min, max)
      params.setInitialValue(initial.clamp(min, max))
      params.setNegativesAllowed(true) if min < 0
      params.setCancelValue(initial)
      return pbMessageChooseNumber(text, params)
    end

    def edit_meter(mod, table)
      ids = table.keys
      return if ids.empty?
      idx = pbMessage(_INTL("Which one?"), ids.map { |id| "#{mod.display_name(id)}: #{mod.get(id)} (#{mod.tier(id)})" }, -1)
      return if idx < 0
      d = mod.definition(ids[idx])
      mod.set(ids[idx], pick_number(_INTL("Set value."), d[:min], d[:max], mod.get(ids[idx])))
    end

    def make_choice
      keys = Prismfall::Narrative::CHOICES.keys
      idx = pbMessage(_INTL("Which choice?"), keys.map { |k| "#{k}: #{Prismfall::Choices.get(k).inspect}" }, -1)
      return if idx < 0
      key = keys[idx]
      vals = Prismfall::Narrative::CHOICES[key][:values] || []
      cmds = vals.map { |v| v.to_s } + [_INTL("(clear)")]
      v = pbMessage(_INTL("Value for {1}?", key.to_s), cmds, -1)
      return if v < 0
      if v >= vals.length
        Prismfall::Choices.clear(key)
      else
        Prismfall::Choices.clear(key)   # debug ignores :once
        Prismfall::Choices.make(key, vals[v])
      end
    end

    def test_condition
      text = pbMessageFreeText(_INTL("Condition to test?"), "", false, 200, Graphics.width)
      return if nil_or_empty?(text)
      ok, err = Prismfall::Conditions.check(text)
      if !ok
        pbMessage(_INTL("Syntax error: {1}", err))
        return
      end
      pbMessage(_INTL("Result: {1}", Prismfall::Conditions.value(text).inspect))
    end
  end
end

MenuHandlers.add(:debug_menu, :prismfall_core_narrative, {
  "name"        => _INTL("Narrative tools"),
  "parent"      => :prismfall_core_menu,
  "description" => _INTL("Bonds, standing, resonance, choices, conditions, endings."),
  "effect"      => proc {
    dn = Prismfall::DebugNarrative
    cmds = [_INTL("Edit bond"), _INTL("Edit standing"), _INTL("Set resonance"), _INTL("Make choice"),
            _INTL("Test condition"), _INTL("Show determined ending"), _INTL("Trigger ending..."),
            _INTL("Passwords (force prompt)"), _INTL("Festival: redraw bracket"), _INTL("Cancel")]
    case pbMessage(_INTL("Narrative tools."), cmds, cmds.length)
    when 0 then dn.edit_meter(Prismfall::Bonds, Prismfall::Narrative::BONDS)
    when 1 then dn.edit_meter(Prismfall::Standing, Prismfall::Narrative::FACTIONS)
    when 2
      n = Prismfall::Narrative
      Prismfall::Resonance.set(dn.pick_number(_INTL("Resonance (- Ruin / + Harmony)."), n::RESONANCE_MIN,
                                              n::RESONANCE_MAX, Prismfall::Resonance.value))
      pbMessage(_INTL("Resonance {1} ({2}).", Prismfall::Resonance.value, Prismfall::Resonance.band.to_s))
    when 3 then dn.make_choice
    when 4 then dn.test_condition
    when 5 then pbMessage(_INTL("Ending: {1}", Prismfall::Endings.determine.to_s))
    when 6
      ids = Prismfall::Narrative::ENDINGS.keys
      idx = pbMessage(_INTL("Trigger which ending?"), ids.map { |i| i.to_s }, -1)
      Prismfall.trigger_ending(ids[idx], credits: false) if idx >= 0
    when 7 then Prismfall::Passwords.prompt(true)
    when 8
      if Prismfall::Festival.active?
        Prismfall::Festival.draw_bracket_stages!
        pbMessage(_INTL("Path: {1}", Prismfall::Festival.path.map { |i| Prismfall::Festival.display_name(i) }.join(", ")))
      else
        pbMessage(_INTL("Start the Festival first."))
      end
    end
  }
})

MenuHandlers.add(:debug_menu, :prismfall_core_ledger, {
  "name"        => _INTL("Ledger tools"),
  "parent"      => :prismfall_core_menu,
  "description" => _INTL("View, fill or clear the cross-save Ledger; test a game over."),
  "effect"      => proc {
    cmds = [_INTL("View Ledger"), _INTL("Mark all game overs found"), _INTL("Clear Ledger"),
            _INTL("Trigger a game over..."), _INTL("Cancel")]
    case pbMessage(_INTL("Ledger: {1}", Prismfall::Ledger.path), cmds, cmds.length)
    when 0 then Prismfall::Ledger.show
    when 1
      Prismfall::Narrative::GAME_OVERS.each_key do |id|
        Prismfall::Ledger.record_game_over(id) if !Prismfall::Ledger.game_over_found?(id)
      end
      pbMessage(_INTL("Ruin Route unlocked: {1}", Prismfall::Ledger.ruin_unlocked?.to_s))
    when 2
      Prismfall::Ledger.clear! if pbConfirmMessageSerious(_INTL("Erase the Ledger for every save?"))
    when 3
      ids = Prismfall::Narrative::GAME_OVERS.keys
      idx = pbMessage(_INTL("Which game over?"), ids.map { |i| i.to_s }, -1)
      Prismfall.game_over(ids[idx]) if idx >= 0
    end
  }
})
