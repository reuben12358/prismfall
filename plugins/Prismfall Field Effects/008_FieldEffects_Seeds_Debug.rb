#===============================================================================
# Prismfall Field Effects - seed items and battle debug menu
#===============================================================================
# Seeds (Elemental/Magical/Telluric/Synthetic) activate when their holder
# enters battle on a field whose :seed list has an entry for that item, and for
# battlers already in battle when the field changes. Each field decides what
# its seed does (see design/FIELDS.md). The seed is consumed on activation.
FieldEffects::SEED_ITEMS.each do |seed|
  Battle::ItemEffects::OnSwitchIn.add(seed,
    proc { |item, battler, battle|
      FieldEffects.trigger_seed(battle, battler, item)
    }
  )
end

#===============================================================================
# Battle debug menu: Field -> Field effect
#===============================================================================
MenuHandlers.add(:battle_debug_menu, :prismfall_field_effect, {
  "name"        => _INTL("Field effect"),
  "parent"      => :field,
  "description" => _INTL("Change the Prismfall field effect, stage or borrowed effects."),
  "effect"      => proc { |battle|
    loop do
      cur = FieldEffects.current(battle)
      msg = _INTL("Current field: {1} (stage {2})", FieldEffects.name_of(cur), battle.field_stage)
      borrowed = battle.fe_state[:borrowed]
      msg += "\n" + _INTL("Borrowing: {1}", borrowed.map { |i| FieldEffects.name_of(i) }.join(", ")) if !borrowed.empty?
      cmd = pbMessage("\\ts[]" + msg, [_INTL("Change field"), _INTL("Change stage"),
                                      _INTL("Rotate borrowed effects"), _INTL("Clear field")], -1)
      break if cmd < 0
      case cmd
      when 0
        ids = FieldEffects.ids
        names = ids.map { |i| FieldEffects.name_of(i) }
        choice = pbMessage("\\ts[]" + _INTL("Choose the new field."), names, -1)
        battle.change_field(ids[choice]) if choice >= 0
      when 1
        max = FieldEffects.max_stage(cur)
        params = ChooseNumberParams.new
        params.setRange(1, max)
        params.setDefaultValue(battle.field_stage)
        new_stage = pbMessageChooseNumber("\\ts[]" + _INTL("Choose stage (1-{1}).", max), params)
        battle.set_field_stage(new_stage)
      when 2
        FieldEffects.rotate_borrowed(battle)
      when 3
        battle.change_field(FieldEffects::NONE, "")
      end
    end
  }
})
